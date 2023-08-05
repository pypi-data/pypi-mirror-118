import asyncio
import concurrent
import signal
import threading
import traceback
import uuid
from typing import Tuple, Any

import aio_pika

from ...words import Packet
from ...quru_logger import logger
from ...env import DEBUG, MAIN_EXCHANGE_NAME
from ..mq_client import AsyncMqClient
from .abs_types import Layer1ABC


'''
Layer 1 packet format
{
    "header": str,
    "payload": Packet
}
'''


class Layer1(Layer1ABC):
    '''Service base.
    '''
    layer_name = "layer1"

    def __init__(self,
                 name=None,
                 prefetch=10,
                 loop=None,
                 test_mode=False):
        '''
        Args:

            name (str): The name of the server. Randomly generate one if
            not specified.

            prefetch (int): Number of direct msgs to be buffered.

            loop (asyncio.loop): A param for testing.

            test_mode (bool): In test mode, msg will be auto acked.
            Any queue created will be auto deleted.
        '''
        super().__init__()
        self._name = str(uuid.uuid4()) if name is None else name
        self._prefetch = prefetch
        self._test_mode = test_mode
        self._loop = loop
        self._mq_client = AsyncMqClient(loop=self._loop)
        self._queue = None

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value) -> str:
        self._name = value

    @property
    def loop(self):
        return self._loop

    @property
    def test_mode(self):
        return self._test_mode

    @property
    def queue(self):
        return self._queue

    @queue.setter
    def queue(self, value: aio_pika.channel.Queue):
        self._queue = value

    async def consume(self, exg_name: str, exg_type: str,
                      q_name: str, rtn_k: str, prefetch_counter: int = 10,
                      auto_delete: bool = False, exclusive: bool = False,
                      arguments=None) -> Tuple[
                          aio_pika.Queue, aio_pika.Channel, str]:
        await self._mq_client.\
            declare_exchange(name=exg_name,
                             type=exg_type)
        q, channel, consumer_tag = await self._mq_client.\
            declare_queue(name=q_name,
                          bind_exchange=exg_name,
                          routing_key=rtn_k,
                          callback=self.callback,
                          prefetch_count=prefetch_counter,
                          arguments=arguments,
                          auto_delete=auto_delete,
                          exclusive=exclusive,
                          no_ack=False,
                          consumer_tag=self.name)
        return q, channel, consumer_tag

    def switch_mode(self):
        '''Switch this node server mode to between normal and test.
        Do NOT switch mode after setup() is called.
        '''
        self._test_mode = not self._test_mode

    def run(self):
        '''Run the server.
        '''
        if self._loop is None:
            self._loop = asyncio.get_event_loop()
            # self._loop.set_debug(DEBUG)
        try:
            self._loop.run_until_complete(self._real_setup())
        except Exception as e:
            logger.error("Error", name=self._name)
            raise e

        try:
            self._loop.run_forever()
        except Exception:
            self._loop.run_until_complete(self._real_teardown())

    async def send(self, routing_key: str, payload: Any, inner_protl: str,
                   props, exg_name: str = None):
        packet = Packet()
        packet.inner_protl = inner_protl
        packet.payload = payload
        if exg_name is None:
            exg_name = MAIN_EXCHANGE_NAME
        await self._mq_client.publish(
            body=packet.wrap(),
            exchange=exg_name,
            routing_key=routing_key,
            properties=props)

    async def callback(self, async_message: aio_pika.IncomingMessage) -> None:
        '''A callback function for handling received message.
        '''
        logger.debug("Msg_size.", size=async_message.body_size)
        try:
            packet: Packet = self._parse_async_msg(async_message)
        except Exception:
            logger.error("Message_malformed.",
                         error=traceback.format_exc())
            async_message.reject()
            return
        logger.debug("Packet_received.", name=self.name)
        try:
            requeue = await self._dispatch(packet)
            if requeue:
                logger.debug("Requeuing...")
                async_message.nack(requeue=True)
            else:
                async_message.ack()
        except concurrent.futures._base.CancelledError:
            async_message.nack(requeue=True)
        except Exception:
            logger.error("Process_packet_error.",
                         error=traceback.format_exc())
            if not self.test_mode:
                if DEBUG:
                    logger.debug("Requeuing...")
                else:
                    logger.debug("Wont_requeue.")
                async_message.nack(requeue=DEBUG)
            if DEBUG:
                logger.warning('Stop_consuming.')
                await self._real_teardown()
        await asyncio.sleep(0.01 * self._prefetch)

    @staticmethod
    def _parse_async_msg(async_message:
                         aio_pika.IncomingMessage) -> Packet:
        '''Parse message into dataflow.
        '''
        try:
            packet = Packet()
            packet.from_bytes(async_message.body)
        except IOError as e:
            logger.error(str(e))
            raise e
        return packet

    def _ask_exit(self, signame):
        logger.warning("Got_signal_exit.", signame=signame, name=self._name)
        logger.warning("Tearing_down...", name=self._name)
        self._loop.create_task(self._real_teardown())

    async def _setup(self):
        '''Set up MQ channel, queue.
        '''
        if self._loop is None:
            self._loop = asyncio.get_running_loop()
        logger.info("Setting_up_layer1...", name=self.name)
        if threading.current_thread() is threading.main_thread():
            signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
            for s in signals:
                self._loop.add_signal_handler(
                    s, lambda s=s: self._ask_exit(s)
                    )
        await self._mq_client.setup()
        self._queue, _, _ = await self.consume(
            exg_name=MAIN_EXCHANGE_NAME,
            exg_type=aio_pika.ExchangeType.DIRECT,
            q_name=self.name,
            rtn_k=self.name,
            prefetch_counter=20,
            auto_delete=True,
            exclusive=False,
            arguments=None)

    async def _teardown(self):
        logger.info("Tearing_down_layer1...", name=self.name)
        await self._mq_client.close()
        self._loop.stop()
