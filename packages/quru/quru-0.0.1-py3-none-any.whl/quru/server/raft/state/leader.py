import asyncio
import typing

from aiozipkin.span import SpanAbc

from ....quru_logger import logger
from ....env import HEARTBEAT_INTERVAL
from ....words import RaftCommand, RaftLog, RaftQuorumLog
from ...protocol import RPCTimeoutError
from ..timer import Timer
from .base import BaseState, candidate_qualification, log_consistency_check

TRACE_SEGMENT_SIZE = int(300 / (HEARTBEAT_INTERVAL * 0.001))


class Leader(BaseState):
    def start(self, registered_task: typing.List = None) -> asyncio.Task:
        if self._trace is not None:
            self._trace.annotate("Become leader.")

        self._next_index = {}
        self._running_task = []
        self._trace_refresh_counter = 0
        self._trace_segments = 0

        # init quorum
        hb_at_once = True
        if self._core._lodge_map[RaftQuorumLog][self._core.name][0]:
            hb_at_once = False  # enlarging_quorum as the first heartbeat.
            raft_cmd = RaftCommand().as_set(self._core.name, [False, 2])
            span = self._core.new_child(self._trace)
            span.name("enlarging_quorum")
            span.start()
            asyncio.create_task(
                self._update_quorum(raft_cmd, span))

        if registered_task:
            for task in registered_task:
                self._running_task.append(
                    asyncio.create_task(task(lambda: self._trace)))

        self._heartbeat_timer = Timer(
            HEARTBEAT_INTERVAL * 0.001,
            self.heart_beat)
        return self._heartbeat_timer.start(at_once=hb_at_once)

    async def heart_beat(self):
        self._trace_refresh_counter += 1
        if self._trace_refresh_counter >= TRACE_SEGMENT_SIZE:
            self._trace_segments += 1
            self._trace_refresh_counter = 0
            self._trace.finish()
            span, self._trace = self._core.create_trace(
                "Term:{} Seg:{}".format(
                    self._current_term,
                    self._trace_segments
                    )
                )
            self._trace.start()
        else:
            span = self._core.new_child(self._trace)
        span.name("Heart beat.")
        with span as span:
            await self._append_entries(span)

    def stop(self):
        for task in self._running_task:
            try:
                task.cancel()
            except Exception:
                pass
        self._running_task = []
        if self._trace is not None:
            self._trace.finish()
            self._trace = None
        self._heartbeat_timer.stop()

    async def on_request_store(
        self, command: RaftCommand, span: SpanAbc = None
    ):
        if span:
            span.annotate("Received request.")
        log = RaftLog()
        log.term = self._current_term
        la_raft_log_idx = self._core.last_applied.index
        log.index = la_raft_log_idx + 1
        log.command = command
        self._core.ledger.append(log)
        return await self._append_entries(span)

    @candidate_qualification
    def on_request_vote(self, data, span: SpanAbc = None):
        term = data['term']
        candidate_id = data['candidate_id']
        self._current_term = term
        self._voted_for = candidate_id
        logger.info(
            "Vote_for_{}".format(candidate_id),
            i_am=self._core.name,
            state=self.__class__.__name__,
            span=span)
        self._core.to_follower()
        return True

    @log_consistency_check
    def on_append_entries(self, data: dict, span: SpanAbc = None):
        self._leader_id = data['leader_id']
        if self._voted_for is not None:
            self._voted_for = None
        entries: typing.List[RaftLog] = data['entries']
        leader_commit: int = data['leader_commit']
        self._core.ledger.replace(data['prev_log'].index + 1, entries)
        if self._commit_index < leader_commit:
            for i in range(self._commit_index, leader_commit + 1):
                log = self._core.ledger[i]
                self._core.apply(log)
                self._commit_index += 1
        self._current_term = data['term']
        logger.debug(
            "Good_appent_from_{}.".format(data['leader_id']),
            span=span)
        self._core.to_follower()
        return True, []

    async def _append_entries(self, span: SpanAbc = None) -> bool:
        tks = []
        last_idx = self._core.last_applied.index
        for peer, _ in self._core.quorum:
            if peer == self._core.name:
                continue
            if peer not in self._next_index:
                self._next_index[peer] = last_idx + 1
            data = {
                'prev_log': self._core.ledger[self._next_index[peer] - 1],
                'leader_id': self._core.name,
                'entries': self._core.ledger[self._next_index[peer]:],
                'leader_commit': self._commit_index,
                'term': self._current_term,
            }
            tks.append(
                asyncio.create_task(
                    self._append_entries_to_one(peer, data, span)
                    )
                )
        logger.debug(
            "Sending_appent...", term=self._current_term,
            leader=self._core.name, span=span)
        suc_cnt = 1
        for fu in asyncio.as_completed(tks):
            is_success, peer = await fu
            if is_success and self._core.in_cohort(peer):
                suc_cnt += 1
                if suc_cnt > self._core.cohort_size // 2:
                    for i in range(self._commit_index + 1, last_idx + 1):
                        self._core.apply(self._core.ledger[i])
                    self._commit_index = last_idx
                    return True
        return False if tks else True

    async def _append_entries_to_one(
        self,
        peer: str,
        data: dict,
        span: SpanAbc = None
    ) -> bool:
        try:
            is_success, info = await self._core.call(
                peer, "appent", data, span)
        except RPCTimeoutError:
            return False, peer
        if is_success:
            if data['entries']:
                self._next_index[peer] = \
                    data['entries'][-1].index + 1
            if not self._core.in_cohort(peer):
                self._add_cohort(peer)
        else:
            peer_la_lo_term, peer_la_lo_idx = info
            probe_log: RaftLog = self._core.ledger[peer_la_lo_idx]
            old_nx_idx = self._next_index[peer]
            if probe_log.term == peer_la_lo_term:
                self._next_index[peer] = peer_la_lo_idx + 1
            elif probe_log.term > peer_la_lo_term:
                _, idx = self._core.ledger.find_term_start(peer_la_lo_term)
                self._next_index[peer] = idx + 1
            else:
                _, idx = self._core.ledger.find_term_start(probe_log.term)
                self._next_index[peer] = idx + 1
            logger.debug(
                "Adjust_next_index.",
                for_=peer,
                fr_=old_nx_idx,
                to_=self._next_index[peer],
                span=span)
        return is_success, peer

    def _add_cohort(self, peer: str, span: SpanAbc = None):
        logger.info("Add_cohort.", target=peer, span=span)
        cmd = RaftCommand().as_change(peer, [False, 2])
        asyncio.create_task(self._update_quorum(cmd, span))

    async def _update_quorum(
        self, command: RaftCommand, span: SpanAbc = None
    ):
        log = RaftQuorumLog()
        log.term = self._current_term
        la_log_idx = self._core.last_applied.index
        log.index = la_log_idx + 1
        log.command = command
        log.ignore_exc = True
        self._core.apply(log)  # Very important! Otherwise, \
        # will lead to _append_entries->_append_entries_to_one->_update_quorum\
        # indefinite recursion
        self._core.ledger.append(log)
        res = await self._append_entries(span)
        if span is not None:
            span.finish()
        return res
