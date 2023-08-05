import abc
from typing import Any, Awaitable, Tuple

import aio_pika

from ...quru_logger import logger
from ...words.packet import Packet


class UpperLayerABC(metaclass=abc.ABCMeta):

    @abc.abstractproperty
    def layer_name(self) -> str:
        raise NotImplementedError

    @abc.abstractclassmethod
    async def callback(self) -> Any:
        raise NotImplementedError

    async def _real_teardown(self) -> None:
        if hasattr(self, "_teardown"):
            await getattr(self, '_teardown')()

    async def _real_setup(self) -> None:
        if hasattr(self, "_setup"):
            await getattr(self, '_setup')()

    @property
    def test_mode(self) -> bool:
        return self._base_layer.test_mode

    @property
    def name(self) -> str:
        return self._base_layer.name

    @property
    def queue(self) -> aio_pika.channel.Queue:
        return self._base_layer.queue

    @name.setter
    def name(self, value: aio_pika.channel.Queue):
        self._base_layer.name = value

    @queue.setter
    def queue(self, value):
        self._base_layer.queue = value

    async def consume(self, exg_name: str, exg_type: str,
                      q_name: str, rtn_k: str, prefetch_counter: int = 10,
                      auto_delete: bool = False, exclusive: bool = False,
                      arguments=None) -> Tuple[
                          aio_pika.Queue, aio_pika.Channel, str]:
        '''Add one more consuming queue.
        '''
        return await self._base_layer.consume(exg_name, exg_type, q_name,
                                              rtn_k, prefetch_counter,
                                              auto_delete, exclusive,
                                              arguments)


class BasableLayerABC(metaclass=abc.ABCMeta):
    '''An abstract interface that defines what a basable layer
    (the layer that can be piled upon) should be.
    '''

    def __init__(self):
        self._setup_chain = []
        self._teardown_chain = []
        self._routing_table = {}

    def add_teardown(self, teardown: Awaitable[None]):
        self._teardown_chain.insert(0, teardown)

    def add_setup(self, setup: Awaitable[None]):
        self._setup_chain.append(setup)

    async def _real_teardown(self) -> None:
        for sub_teardown in self._teardown_chain:
            await sub_teardown
        if hasattr(self, "_teardown"):
            await getattr(self, '_teardown')()

    async def _real_setup(self) -> None:
        if hasattr(self, "_setup"):
            await getattr(self, '_setup')()
        for sub_setup in self._setup_chain:
            await sub_setup

    def pile(self, upper_layer: UpperLayerABC):
        self._routing_table[upper_layer.layer_name] = upper_layer.callback
        self.add_setup(upper_layer._real_setup())
        self.add_teardown(upper_layer._real_teardown())

    async def _dispatch(self, packet: Packet, *args) -> bool:
        '''Demultiplex packet into upper layers.
        '''
        inner_protl = packet.inner_protl
        if inner_protl not in self._routing_table:
            logger.error(
                "Cannot_find_specified_upper_layer.",
                name=self.name,
                upr_layer=inner_protl)
            return False
        else:
            upper_callback = self._routing_table.get(inner_protl)
            return await upper_callback(packet.payload, *args)


class Layer1ABC(BasableLayerABC):

    @abc.abstractproperty
    def name(self):
        raise NotImplementedError

    @abc.abstractproperty
    def queue(self):
        raise NotImplementedError

    @abc.abstractproperty
    def loop(self):
        raise NotImplementedError

    @abc.abstractproperty
    def test_mode(self):
        raise NotImplementedError

    @abc.abstractclassmethod
    async def send(self, dst: str, payload: dict):
        raise NotImplementedError
