import asyncio
import time
import typing

import aio_pika
import pika
import aiormq

from ..quru_logger import logger
from ..env import (BROADCAST_EXCHANGE_NAME, MAIN_EXCHANGE_NAME, MQ_HOST,
                   MQ_PORT, MQ_RETRY, RABBITMQ_PASSWORD, RABBITMQ_USERNAME,
                   RPC_EXCHANGE_NAME)


class BaseMqClient:
    def __init__(self,
                 mq_host=MQ_HOST,
                 mq_port=MQ_PORT,
                 mq_username=RABBITMQ_USERNAME,
                 mq_password=RABBITMQ_PASSWORD,
                 retry=MQ_RETRY):
        self._mq_host = mq_host
        self._mq_port = mq_port
        self._mq_username = mq_username
        self._mq_password = mq_password
        self._URL = 'amqp://{}:{}@{}:{}'.format(
                        self._mq_username,
                        self._mq_password,
                        self._mq_host,
                        self._mq_port)
        self._param = pika.URLParameters(self._URL)
        self._retry = retry

    def connect(self) -> pika.BlockingConnection:
        if self._retry == 0:
            upper_bound = float('inf')
        else:
            upper_bound = self._retry
        counter = 0
        while counter < upper_bound:
            try:
                connection = pika.BlockingConnection(self._param)
                break
            except Exception:
                time.sleep(10)
            counter += 1
        else:
            raise TimeoutError('connect failed.')
        if connection is None:
            raise ConnectionError
        logger.info("Succeded_in_connecting_MQ.")
        return connection


class AsyncMqClient(BaseMqClient):
    '''Async MQ logic wrapper.
    '''

    EXCHANGE_PROPERTY = {
        MAIN_EXCHANGE_NAME: {
            "type": aio_pika.ExchangeType.DIRECT
        },
        RPC_EXCHANGE_NAME: {
            "type": aio_pika.ExchangeType.DIRECT
        },
        BROADCAST_EXCHANGE_NAME: {
            "type": aio_pika.ExchangeType.TOPIC
        },
    }

    def __init__(self,
                 loop,
                 mq_host=MQ_HOST,
                 mq_port=MQ_PORT,
                 mq_username=RABBITMQ_USERNAME,
                 mq_password=RABBITMQ_PASSWORD,
                 retry=MQ_RETRY):
        super().__init__(mq_host=MQ_HOST,
                         mq_port=MQ_PORT,
                         mq_username=RABBITMQ_USERNAME,
                         mq_password=RABBITMQ_PASSWORD,
                         retry=MQ_RETRY)
        self._connection = None
        self._loop = loop
        self._q_pool = {}

    async def setup(self):
        await self._async_connect()
        self._pub_channel = \
            await self._connection.channel(publisher_confirms=False)

    async def _async_connect(self) -> aio_pika.RobustConnection:
        if self._retry == 0:
            upper_bound = float('inf')
        else:
            upper_bound = self._retry
        counter = 0
        while counter < upper_bound:
            try:
                self._connection = aio_pika.RobustConnection(
                    self._URL,
                    loop=self._loop
                )
                await self._connection.connect()
                break
            except Exception:
                await asyncio.sleep(10)
                counter += 1
        else:
            raise TimeoutError('connect failed.')
        if self._connection is None:
            raise ConnectionError
        logger.info("Succeded_in_connecting_MQ.")
        return self._connection

    async def publish(self, **kwargs):
        err = None
        for i in range(3):
            try:
                await self._pub_channel.channel.basic_publish(**kwargs)
                break
            except Exception as e:
                err = e
                await self.setup()
        else:
            raise err

    async def declare_exchange(self,
                               name,
                               type,
                               arguments=None,

                               bind_exchange=None,
                               routing_key=None,

                               channel=None):
        '''A broker function to declare an exchange. This function abstract out 
        a lot details of communicating with the mq server.
        '''
        if channel is None:
            channel: aio_pika.Channel = await self._connection.channel(
                publisher_confirms=False)
        exchange = await channel.declare_exchange(
            name=name, type=type,
            arguments=arguments)
        if bind_exchange is not None:
            assert routing_key is not None
            await channel.declare_exchange(
                name=bind_exchange,
                **self.EXCHANGE_PROPERTY[bind_exchange])
            await exchange.bind(bind_exchange, routing_key=routing_key)
        return exchange, channel

    async def declare_queue(
        self,
        name,
        bind_exchange,
        routing_key,
        callback,
        prefetch_count,
        arguments=None,
        auto_delete=False,
        exclusive=False,
        no_ack=True,
        channel=None,
        consumer_tag=None
    ) -> typing.Tuple[aio_pika.Queue, aio_pika.Channel, str]:
        '''A broker function to declare a queue. This function abstract out
        a lot details of communicating with the mq server.
        '''
        if name in self._q_pool:
            queue, channel, consumer_tag = self._q_pool[name]
        else:
            if channel is None:
                channel: aio_pika.Channel = await self._connection.channel(
                    publisher_confirms=False)
            if arguments is None:
                arguments = {}
            arguments["x-max-length"] = 30000
            queue: aio_pika.Queue = await channel.declare_queue(
                name=name,
                arguments=arguments,
                auto_delete=auto_delete,
                exclusive=exclusive)
            self._q_pool[queue.name] = consumer_tag
        try:
            await channel.set_qos(prefetch_count=prefetch_count)
            consumer_tag = await queue.consume(
                callback, no_ack=no_ack,
                consumer_tag=consumer_tag)
        except aiormq.exceptions.DuplicateConsumerTag:
            pass
        self._q_pool[queue.name] = (queue, channel, consumer_tag)
        await queue.bind(bind_exchange, routing_key=routing_key)
        return queue, channel, consumer_tag

    async def close(self):
        if self._connection is None:
            return
        await self._connection.close()
