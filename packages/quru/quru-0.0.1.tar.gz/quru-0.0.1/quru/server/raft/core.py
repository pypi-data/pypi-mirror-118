import asyncio
import random
import typing

import aio_pika
import aiozipkin as az

from ... import words
from ...quru_logger import logger
from ...env import MAIN_EXCHANGE_NAME  # SPAN_SAMPLE_RATE, ZIPKIN_ADDR,
from ...env import BROADCAST_EXCHANGE_NAME, DIR_RPC_TIMEOUT, HEARTBEAT_INTERVAL
# from ...redis_clt import redis_client
from ...words import RaftLog, RaftQuorumLog
from ..protocol.layer4_actor import Layer4Actor
from .abs_types import CoreABC
from .list_ledger import ListLedger
from .mem_lodge import MemLodge
from .state import BaseState, Candidate, Follower, Leader, Learner
from .timer import Timer

DIR_RPC_TIMEOUT_IN_SEC = DIR_RPC_TIMEOUT * 0.001


class Core(CoreABC):
    layer_name = "rafter"

    def __init__(self, base_layer: Layer4Actor, duty_radio_for_leader=1):
        self._base_layer: Layer4Actor = base_layer
        self._base_layer.pile(self)
        self._state: BaseState = None
        self._duty_radio_for_leader = duty_radio_for_leader
        self._layer4_job_queue_changed = False

        self._lodge_map = {
            RaftLog: MemLodge(),
            RaftQuorumLog: MemLodge()
        }
        self._ledger = ListLedger()

        self._registered_task = []
        self._running_task = []

    @property
    def role(self) -> str:
        return self._base_layer._role

    @property
    def ledger(self) -> ListLedger:
        return self._ledger

    @property
    def quorum_size(self) -> int:
        return len(list(self.quorum))  # "- 1" is because [x: None] excluded

    @property
    def quorum(self):
        for peer, info in self._lodge_map[RaftQuorumLog].items():
            yield peer, info

    def in_quorum(self, peer: str) -> bool:
        return peer in self._lodge_map[RaftQuorumLog]

    @property
    def cohort(self):
        for peer, info in self.quorum:
            if not info[0]:
                yield peer

    @property
    def cohort_size(self) -> int:
        return len(list(self.cohort))

    def in_cohort(self, peer: str) -> bool:
        return peer in self._lodge_map[RaftQuorumLog] \
            and not self._lodge_map[RaftQuorumLog][peer][0]

    def apply(self, log: RaftLog):
        self._lodge_map[log.__class__].apply(log)

    def register(self, func):
        '''Register a handled that only got executed on one node of the actors.
        '''
        self._registered_task.append(func)

    def to_follower(self):
        if self._layer4_job_queue_changed:
            asyncio.create_task(self._rearange_layer4_job_queue(
                1
            ))
            self._layer4_job_queue_changed = False
        logger.info(
            "Change_state",
            fr=self._state.__class__.__name__,
            to="Follower")
        self._state.stop()
        self._state.__class__ = Follower
        self._state.start()

    def to_candidate(self):
        logger.info(
            "Change_state",
            fr=self._state.__class__.__name__,
            to="Candidate")
        self._state.stop()
        self._state.__class__ = Candidate
        self._state.start()

    async def to_leader(self):
        if 0 <= self._duty_radio_for_leader < 1:
            await self._rearange_layer4_job_queue(
                self._duty_radio_for_leader)
            self._layer4_job_queue_changed = True
        logger.info(
            "Change_state",
            fr=self._state.__class__.__name__,
            to="Leader")
        self._state.stop()
        self._state.__class__ = Leader
        self._state.start(self._registered_task)

    @property
    def last_applied(self) -> RaftLog:
        '''Return the last log
        '''
        return self.ledger[-1]

    async def callback(self, packet: words.RaftPacket,
                       span: az.span.SpanAbc):
        if packet.mode == "appent":
            span.name("on_append_entries")
            return self._state.on_append_entries(packet.payload, span)
        elif packet.mode == "reqvot":
            span.name("on_request_vote")
            return self._state.on_request_vote(packet.payload, span)
        elif packet.mode == "reqsto":
            span.name("on_request_store")
            return await self._state.on_request_store(packet.payload, span)
        elif packet.mode == "brdcst":
            span.name("on_broadcast")
            return self._on_broadcast_existence(packet.payload, span)
        else:
            raise words.TransmittableException(
                "Unknown raft RPC [{}].".format(packet.mode)
                )

    async def call(self, dst: str, mode: str, data: dict, span=None):
        packet = words.RaftPacket()
        packet.payload = data
        packet.mode = mode
        if dst.endswith(".*"):
            dst = dst[:-2]
            return await self._base_layer.call(
                dst=dst,
                data=packet,
                inner_protl=self.layer_name,
                span=span,
                timeout=DIR_RPC_TIMEOUT_IN_SEC,
                exg_name=BROADCAST_EXCHANGE_NAME
            )
        else:
            return await self._base_layer.call(
                dst=dst,
                data=packet,
                inner_protl=self.layer_name,
                span=span,
                timeout=DIR_RPC_TIMEOUT_IN_SEC
            )

    async def send(self, dst: str, mode: str, data: dict, span=None):
        packet = words.RaftPacket()
        packet.payload = data
        packet.mode = mode
        if dst.endswith(".*"):
            dst = dst[:-2]
            return await self._base_layer.send(
                dst=dst,
                data=packet,
                inner_protl=self.layer_name,
                span=span,
                exg_name=BROADCAST_EXCHANGE_NAME
            )
        else:
            return await self._base_layer.send(
                dst=dst,
                data=packet,
                inner_protl=self.layer_name,
                span=span
            )

    def create_trace(self, name="", span_name="")\
            -> typing.Tuple[az.span.SpanAbc, az.span.SpanAbc]:
        return self._base_layer._base_layer._create_trace(
            name, span_name)

    def new_child(self, trace: az.span.SpanAbc) -> az.span.SpanAbc:
        if trace is None:
            return None
        return self._base_layer._base_layer._tracer.new_child(trace.context)

    async def _setup(self):
        logger.info("Setting_up_layer5_rafter...", name=self.name)
        if self.role is not None:
            await self.consume(
                    exg_name=BROADCAST_EXCHANGE_NAME,
                    exg_type=aio_pika.ExchangeType.TOPIC,
                    q_name=self.name,
                    rtn_k="#.{}.#".format(self.role)
                )
        lower = HEARTBEAT_INTERVAL * 4
        midder = HEARTBEAT_INTERVAL * 5
        upper = HEARTBEAT_INTERVAL * 6
        self._broadcast_timer = Timer(
            lambda: random.randint(lower, midder) * 0.001,
            self._broadcast_existence
            )
        self._clear_quorum_timer = Timer(
            lambda: random.randint(midder, upper) * 0.001,
            self._clear_quorum
            )
        self._broadcast_timer.start(at_once=True)
        self._clear_quorum_timer.start()
        self._state = Learner(self)
        self._state.start()

    async def _broadcast_existence(self):
        span, _ = self.create_trace()
        await self.send(
                self.role + '.*',
                mode="brdcst",
                data=[self.name, True],
                span=span)

    def _on_broadcast_existence(self, data, span: az.span.SpanAbc):
        source, is_joining = data
        if not is_joining:
            if self.in_quorum(source):
                logger.debug("Drop_peer.", dropped_peer=source, span=span)
                self._lodge_map[RaftQuorumLog].pop(source)
        else:
            if not self.in_quorum(source):
                logger.debug("Add_peer.", added_peer=source, span=span)
                self._lodge_map[RaftQuorumLog][source] = [True, 2]
            else:
                self._lodge_map[RaftQuorumLog][source][1] = 2

    def _clear_quorum(self):
        dropped_peers = []
        for peer, info in self._lodge_map[RaftQuorumLog].items():
            info[1] -= 1
            if info[1] <= 0:
                dropped_peers.append(peer)
        for dropped_peer in dropped_peers:
            logger.debug("Drop_peer.", dropped_peer=dropped_peer)
            self._lodge_map[RaftQuorumLog].pop(dropped_peer)

    async def _teardown(self):
        logger.info(
            "Tearing_down_layer5_rafter...", name=self.name)
        await self.send(
                self.role + '.*',
                mode="brdcst",
                data=[self.name, False],
                span=None)
        if self.role is not None:
            if self._state._trace is not None:
                self._state._trace.finish()

    async def _rearange_layer4_job_queue(self, duty_radio):
        if self._base_layer.job_queue is not None:
            await self._base_layer.job_queue.cancel(
                    self.name)
        if duty_radio != 0:
            arguments = {"x-max-priority": 3} \
                if self._base_layer._priority_queue else None
            self._base_layer.job_queue, _, _ = \
                await self.consume(
                    MAIN_EXCHANGE_NAME,
                    aio_pika.ExchangeType.DIRECT,
                    self.role,
                    self.role,
                    int(self._base_layer._prefetch_counter *
                        duty_radio),
                    self.test_mode,
                    False,
                    arguments
                )
