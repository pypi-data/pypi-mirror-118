import asyncio
import random
import typing

from aiozipkin.span import SpanAbc

from ....quru_logger import logger
from ....env import HEARTBEAT_INTERVAL
from ....words import RaftLog
from ..timer import Timer
from .base import BaseState, log_consistency_check, candidate_qualification


class Follower(BaseState):

    def start(self) -> asyncio.Task:
        if self._trace is not None:
            self._trace.finish()
            self._trace = None
        logger.info("Listening_as_a_follower...", name=self._core.name)
        lower = HEARTBEAT_INTERVAL * 3
        upper = HEARTBEAT_INTERVAL * 5
        self._election_timer = Timer(
            lambda: random.randint(lower, upper) * 0.001,
            self._to_candidate)
        return self._election_timer.start()

    def stop(self):
        self._leader_id = None
        self._voted_for = None
        self._election_timer.stop()

    async def on_request_store(self, data, span: SpanAbc = None):
        return await self._core.call(
            self._leader_id,
            "reqsto",
            data,
            span
        )

    async def _to_candidate(self):
        logger.info(
            "Not_receiving_hb_from_leader_for_long_time.",
            name=self._core.name,
            leader=self._leader_id)
        self._core.to_candidate()

    @candidate_qualification
    def on_request_vote(self, data, span: SpanAbc):
        term = data['term']
        candidate_id = data['candidate_id']
        self._current_term = term
        self._voted_for = candidate_id
        self._election_timer.reset()
        logger.info(
            "Vote_for_{}".format(candidate_id),
            i_am=self._core.name,
            state=self.__class__.__name__,
            span=span)
        return True

    @log_consistency_check
    def on_append_entries(self, data: dict, span: SpanAbc):
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
        self._election_timer.reset()
        logger.debug(
            "Rec_good_appent_from_{}".format(data['leader_id']), span=span)
        return True, []
