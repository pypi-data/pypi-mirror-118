import asyncio
import random
import typing

from aiozipkin.span import SpanAbc

from ....quru_logger import logger
from ....env import HEARTBEAT_INTERVAL
from ....words import RaftLog
from ..timer import Timer
from .base import BaseState, log_consistency_check, candidate_qualification
from ...protocol.layer2 import RPCTimeoutError


class Candidate(BaseState):

    def start(self) -> asyncio.Task:
        lower = HEARTBEAT_INTERVAL * 2
        upper = HEARTBEAT_INTERVAL * 4
        self._election_timer = Timer(
            lambda: random.randint(lower, upper) * 0.001,
            self._poll)
        return self._election_timer.start(at_once=True)

    async def _poll(self):
        span, self._trace = self._core.create_trace(
            "Term:{} Seg:0".format(
                self._current_term + 1
                ),
            "poll")
        self._trace.start()
        with span as span:
            if self.__class__.__name__ != "Candidate":
                logger.warn("Role_leak.", span=span)
                return
            self._voted_for = self._core.name
            self._current_term += 1
            for _ in range(2):
                logger.info(
                    "Starting_poll...",
                    name=self._core.name,
                    term=self._current_term,
                    span=span)
                votes = await self.request_vote(span)
                pros = sum(votes) + 1
                total = self._core.cohort_size or self._core.quorum_size
                if pros <= total // 2:
                    logger.info(
                        "Polling_fails.",
                        pros=pros,
                        total=total,
                        i_am=self._core.name,
                        term=self._current_term,
                        span=span
                    )
                else:
                    # Might be a polling succeeding, if there's no role leak.
                    break
            else:
                # Let the election timer goes to the polling of next term.
                return
            if self.__class__.__name__ == "Candidate":
                logger.info(
                    "Polling_succeeds!",
                    pros=pros,
                    total=total,
                    i_am=self._core.name,
                    span=span
                )
                await self._core.to_leader()
                # From now on, 'self' is Leader type.

    async def request_vote(self, span: SpanAbc = None):
        prev_log = self._core.ledger[-1] \
            if len(self._core.ledger) > 0 else None
        data = {
            "term": self._current_term,
            "candidate_id": self._core.name,
            "prev_log": prev_log,
        }
        tks = []
        if self._core.cohort_size == 0:
            # No cluster exists
            for peer, _ in self._core.quorum:
                if peer == self._core.name:
                    continue
                tk = asyncio.create_task(
                    self._request_single_vote(
                        peer,
                        data,
                        span
                    )
                )
                tks.append(tk)
            return await asyncio.gather(*tks)
        else:
            for peer in self._core.cohort:
                if peer == self._core.name:
                    continue
                tk = asyncio.create_task(
                    self._request_single_vote(
                        peer,
                        data,
                        span
                    )
                )
                tks.append(tk)
            return await asyncio.gather(*tks)

    async def _request_single_vote(self, peer, data, span: SpanAbc = None):
        logger.debug("Requesting_vote_from_{}.".format(peer), span=span)
        try:
            vo = await self._core.call(peer, "reqvot", data, span)
            logger.debug("Got_{}_from_{}.".format(vo, peer), span=span)
            return vo
        except RPCTimeoutError:
            logger.warn(
                "Not_receiving_resp_for_voting.",
                fro=peer, iam=self._core.name)
            logger.debug("Got_none_from_{}.".format(peer), span=span)
            return False

    def stop(self):
        self._election_timer.stop()

    async def on_request_store(self, data, span: SpanAbc = None):
        logger.info("Rev_store_request_on_election_phase.", span=span)
        await asyncio.sleep(3)  # Sleep to wait for\
        # self-changing to follower/leader
        return await self.on_request_store(data, span)

    @candidate_qualification
    def on_request_vote(self, data, span: SpanAbc):
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
    def on_append_entries(
        self,
        data: dict,
        span: SpanAbc = None
    ):
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
