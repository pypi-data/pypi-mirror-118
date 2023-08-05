import asyncio
import typing

from aiozipkin.span import SpanAbc

from ....quru_logger import logger
from ....env import HEARTBEAT_INTERVAL
from ....words import RaftLog
from ..timer import Timer
# from ...protocol import RPCTimeoutError
from .base import BaseState, log_consistency_check, candidate_qualification


def reset_to_fol_timer(func):
    def wrap(self, data, span: SpanAbc):
        self._to_fol_timer.reset()
        return func(self, data, span)
    return wrap


class Learner(BaseState):

    def start(self) -> asyncio.Task:
        # logger.info("Broadcasting_self...", name=self._core.name)
        self._to_fol_timer = Timer(
            HEARTBEAT_INTERVAL * 2 * 0.001,
            self._to_follower)
        return self._to_fol_timer.start()
        # self._broadcasting_timer = Timer(
        #     DIR_RPC_TIMEOUT * 1 * 0.001,
        #     self._broadcast
        # )
        # return self._broadcasting_timer.start(at_once=True)

    def stop(self):
        self._to_fol_timer.stop()
        # self._broadcasting_timer.stop()

    # async def _broadcast(self):
    #     span, trace = self._core.create_trace(
    #         "Broadcast",
    #         span_name="Broadcast"
    #     )
    #     with trace:
    #         with span as span:
    #             try:
    #                 self._leader_id = await self._core.call(
    #                     dst=self._core.role + ".*",
    #                     mode="brdcst",
    #                     data=self._core.name,
    #                     span=span
    #                 )
    #                 logger.info("Recd_resp.", fro=self._leader_id, span=span)
    #                 # self._broadcasting_timer.stop()
    #             except RPCTimeoutError:
    #                 logger.info("No_resp.", span=span)
    #                 pass

    async def on_request_store(self, data, span: SpanAbc = None):
        if self._leader_id is None:
            return
        return await self._core.call(
            self._leader_id,
            "reqsto",
            data,
            span
        )

    async def _to_follower(self):
        logger.info(
            "Not_receiving_hb_from_leader_for_long_time.",
            name=self._core.name,
            leader=self._leader_id)
        self._core.to_follower()

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
        return True

    @reset_to_fol_timer
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
        logger.debug(
            "Rec_good_appent_from_{}.".format(data['leader_id']),
            span=span)
        self._core.to_follower()
        return True, []
