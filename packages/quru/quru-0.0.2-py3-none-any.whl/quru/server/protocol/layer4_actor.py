import asyncio
import functools
import inspect
import types
import typing
from typing import List

import aio_pika
import aiozipkin as az
from pamqp import specification as spec

from ... import words
from ...quru_logger import logger
from ...env import MAIN_EXCHANGE_NAME, SHUTDOWN_GRACE_PERIOD
from .abs_types import BasableLayerABC, UpperLayerABC
from .layer3 import Layer3


class Layer4Actor(BasableLayerABC,
                  UpperLayerABC):
    layer_name = "layer4_actor"

    def __init__(self, role, base_layer: Layer3,
                 prefetch_counter=20, priority_queue=False):
        super().__init__()
        self._base_layer = base_layer
        self._role = role
        if self._role is not None:
            self.name = "{}_{}".format(self._role, self.name)
        self._base_layer.pile(self)
        self._handler_table = {}
        self._job_queue = None
        self._prefetch_counter = prefetch_counter
        self._priority_queue = priority_queue

    @property
    def job_queue(self) -> aio_pika.channel.Queue:
        return self._job_queue

    @job_queue.setter
    def job_queue(self, value: aio_pika.channel.Queue):
        self._job_queue = value

    def register(self, arg="", transaction=False):
        '''A decorator to register a processor, the first registered processor
        is also used as a default one.

        Processor should be callable function. The return value will be
        forwarded to caller service if it wants. Arguments that passed
        into processor are strictly defined as one or more of:

            data (any): The data attribute of coming task.
            call (function): The function that partially built by self.call
            with ori_dataflow passed in.
            send (function): The function that partially build by self.send
            with ori_dataflow passed in.
            task (Task): The coming task.
            META (dict): The meta of the coming dataflow. 
        '''
        def do_regi(name, processor):
            self._handler_table[name] \
                = (
                    processor,
                    inspect.getfullargspec(processor).args,
                    transaction)
        if isinstance(arg, str):
            def wrap(processor):
                assert not processor.__name__.startswith("undo_")
                if arg == "default":
                    do_regi("default", processor)
                do_regi(processor.__name__, processor)
            return wrap
        else:
            if "default" not in self._handler_table \
               and not arg.__name__.startswith("undo_"):
                do_regi("default", arg)
            if arg.__name__.startswith("undo_") \
               and "default" in self._handler_table:
                undo_defu_prcr: str = "undo_" + self._handler_table["default"][0].__name__
                if arg.__name__ == undo_defu_prcr:
                    do_regi("undo_default", arg)
            do_regi(arg.__name__, arg)

    async def callback(self, packet: words.WorkerPacket,
                       span: az.span.SpanAbc):
        if packet.inner_protl is not None:
            return await self._dispatch(packet, span)
        else:
            return await self._run_processor(
                packet.task, packet.payload,
                span, packet.priority)

    async def call(
        self,
        dst,
        data=None,
        task="default",
        priority=0,
        header=None,
        inner_protl: str = None,
        span=None,
        timeout=None,
        exg_name=None
    ):
        '''Helper function to build and send task to other services that needs
        a receipt.

        Args:
            dst (string): The destination service role.
            data (any): Sending data.
            task (string): Destination service handler.
            priority (int): A priority level between 0-2. Higher value means \
                a higher priority.
            header (header): The header.
            span (SpanAbc): The coming span.
        '''
        routing_key = dst
        packet = words.WorkerPacket()
        packet.task = task
        packet.payload = data
        packet.priority = priority
        packet.inner_protl = inner_protl
        props = spec.Basic.Properties(delivery_mode=1,
                                      priority=priority,
                                      headers=header)
        return await self._base_layer.call(routing_key, packet,
                                           self.layer_name,
                                           props, span=span,
                                           timeout=timeout,
                                           exg_name=exg_name)

    async def send(
        self,
        dst,
        data=None,
        task="default",
        priority=0,
        header=None,
        inner_protl: str = None,
        span=None,
        exg_name=None
    ):
        '''Helper function to build and send task to other services that doesn't
        need a receipt.

        Args:
            dst (string): The destination service role.
            data (any): Sending data.
            dst_method (string): Destination service method.
            priority (int): A priority level between 0-2. Higher value means \
                higher priority.
            header (header): The header.
            span (SpanAbc): The coming span.
        '''
        routing_key = dst
        packet = words.WorkerPacket()
        packet.task = task
        packet.payload = data
        packet.priority = priority
        packet.inner_protl = inner_protl
        props = spec.Basic.Properties(delivery_mode=1,
                                      priority=priority,
                                      headers=header)
        await self._base_layer.send(routing_key, packet,
                                    self.layer_name,
                                    props, span,
                                    exg_name=exg_name)

    def passto(
        self,
        dst,
        data=None,
        task="defualt",
        priority=0,
        header=None,
        inner_protl: str = None,
        span=None
    ):
        '''Helper function to re-assign the task to another service.

        Args:
            dst (string): The destination service role.
            data (any): Sending data.
            dst_method (string): Destination service method.
            priority (int): A priority level between 0-2. Higher value means \
                higher priority.
            header (header): The header.
            span (SpanAbc): The coming span.
        '''
        routing_key = dst
        packet = words.WorkerPacket()
        packet.task = task
        packet.payload = data
        packet.priority = priority
        packet.inner_protl = inner_protl
        props = spec.Basic.Properties(delivery_mode=1,
                                      priority=priority,
                                      headers=header)
        return self._base_layer.passto(routing_key, packet,
                                       self.layer_name,
                                       props, span)

    def _run_processor_inner(
        self, handler: str, data: typing.Any,
        span: az.span.SpanAbc, priority: int,
        args: List[str],
        processor
    ):
        '''Inspect the processor args and feed them.
        '''
        procr_args = []
        for arg in args:
            if arg == "data":
                procr_args.append(data)
            elif arg == "call":
                call = functools.partial(
                    self.call, span=span,
                    priority=priority)
                procr_args.append(call)
            elif arg == "call_without_priority":
                call = functools.partial(
                    self.call, span=span)
                procr_args.append(call)
            elif arg == "send":
                send = functools.partial(
                    self.send, span=span,
                    priority=priority)
                procr_args.append(send)
            elif arg == "send_without_priority":
                send = functools.partial(self.send, span=span)
                procr_args.append(send)
            elif arg == "passto":
                passby = functools.partial(
                    self.passto, span=span,
                    priority=priority)
                procr_args.append(passby)
            elif arg == "passto_without_priority":
                passby = functools.partial(self.passto, span=span)
                procr_args.append(passby)
            elif arg == "span":
                procr_args.append(span)
            elif arg == "priority":
                procr_args.append(priority)
            else:
                raise ValueError("Unrecognized parameter: {}".format(arg))
        return processor(*procr_args)

    async def _run_processor(
        self, handler: str, data: typing.Any,
        span: az.span.SpanAbc, priority: int
    ):
        if handler not in self._handler_table:
            if handler.startswith("undo_"):
                logger.warning(
                    "No_undo_method_defined.", span=span, undo=handler)
                return False
            else:
                return words.TransmittableException(
                    "No handler found "
                    "for task {}"
                    ".".format(handler))
        processor, args, transaction = \
            self._handler_table.get(handler)
        span.name(processor.__name__)
        logger.debug('Start_processing.', processor=processor.__name__)
        try:
            proc_artifact = self._run_processor_inner(
                handler, data,
                span, priority, args,
                processor)
            if isinstance(proc_artifact, types.CoroutineType):
                proc_artifact = await proc_artifact
            assert not isinstance(proc_artifact, types.CoroutineType),\
                "Async processor should not further return a coroutine."
            logger.debug("Finish_task.")
            return proc_artifact
        except Exception as e:
            if handler.startswith("undo_"):
                # If the procedure itself is an undo,
                # just ignore the exception. Cuz we dont
                # want run into the infinite exception loop
                logger.warning(
                    "Undo_processor_failed.", span=span,
                    undo=handler, exc=str(e))
                return False
            if transaction:
                await self._run_processor(
                    "undo_" + handler, data,
                    span, priority)
            raise e

    async def _setup(self):
        if self._role is not None:
            logger.info("Setting_up_layer4...", name=self.name)
            arguments = {"x-max-priority": 3} if self._priority_queue else None
            self._job_queue, _, _ = \
                await self.consume(MAIN_EXCHANGE_NAME,
                                   aio_pika.ExchangeType.DIRECT,
                                   self._role,
                                   self._role,
                                   self._prefetch_counter,
                                   self.test_mode,
                                   False,
                                   arguments)

    async def _teardown(self):
        logger.info("Tearing_down_layer4...", name=self.name)
        if self._role is not None:
            try:
                await self._job_queue.cancel(self.name)
            except Exception:
                pass
        await asyncio.sleep(SHUTDOWN_GRACE_PERIOD)
