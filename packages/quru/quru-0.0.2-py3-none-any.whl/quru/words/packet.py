# standard python package
import json

import aiozipkin as az

# self-defined package
from .types import (InternalTransmittable, QuruJSONEncoder, RedisObj,
                    TraceContext, quru_load_hook)


class _PacketBase(InternalTransmittable):
    def __init__(self,
                 header: dict = None,
                 body: dict = None):
        '''
        Args:
            header (str): The message header.
            payload (Any): The message body.
        '''
        if body is None:
            if header is None:
                header = {}
            body = {"header": header}
        super().__init__(body)

    def __getitem__(self, key):
        return self._body[key]

    def __setitem__(self, key, value):
        self._body[key] = value

    def __contains__(self, key):
        return key in self._body

    @property
    def header(self) -> dict:
        return self['header']

    @property
    def inner_protl(self) -> str:
        return self['inner_protl']

    @inner_protl.setter
    def inner_protl(self, value: str):
        self['inner_protl'] = value

    @property
    def payload(self):
        return self['payload']

    @payload.setter
    def payload(self, value):
        self['payload'] = value


class RPCPacket(_PacketBase):

    @property
    def receipt_id(self):
        '''receipt_id will be None for packet of send mode,
        will be a uuid for packet of receipt/call mode.
        '''
        return self.header.get('receipt_id', None)

    @receipt_id.setter
    def receipt_id(self, value):
        self.header['receipt_id'] = value

    @property
    def mode(self):
        '''Is one of the value of [call, send, receipt]

        call -> Telling that this packet is meant to return a receipt
        to the caller, whether by this node or by anyone else.

        send -> Telling that this packet is not need to be return a receipt.

        receipt -> Telling that this packet is a receipt for a calling.
        '''
        return self.header.get('mode', None)

    @mode.setter
    def mode(self, value):
        '''Must be one of the value of [call, send, receipt]

        call -> Telling that this packet is meant to return a receipt
        to the caller, whether by this node or by anyone else.

        send -> Telling that this packet is not need to be return a receipt.

        receipt -> Telling that this packet is a receipt for a calling.
        '''
        self.header['mode'] = value

    @property
    def source(self):
        '''Denote where this packet comes from, useful for RPC.
        '''
        return self.header.get("source", None)

    @source.setter
    def source(self, value):
        self.header['source'] = value


class TracedPacket(_PacketBase):

    @property
    def trace_context(self) -> az.helpers.TraceContext:
        if 'trace_context' in self.header:
            return self.header['trace_context']._body
        return None

    @trace_context.setter
    def trace_context(self, value: az.helpers.TraceContext):
        self.header['trace_context'] = TraceContext(value)


class WorkerPacket(_PacketBase):

    @property
    def task(self) -> str:
        return self.header.get('task', None)

    @task.setter
    def task(self, value: str):
        self.header['task'] = value

    @property
    def priority(self) -> int:
        return self.header.get('priority', 0)

    @priority.setter
    def priority(self, value: int):
        self.header['priority'] = value


class RaftPacket(_PacketBase):

    @property
    def mode(self) -> str:
        '''Is one of the value of [appent, reqvot, reqsto]

        appent -> Append entries RPC

        reqvot -> Request vote RPC

        reqsto -> Request to store value in lodge.
        '''
        return self.header.get('mode', None)

    @mode.setter
    def mode(self, value):
        '''Must be one of the value of [appent, reqvot, reqsto]

        appent -> Append entries RPC

        reqvot -> Request vote RPC

        reqsto -> Request to store value in lodge.
        '''
        self.header['mode'] = value


class Packet(_PacketBase):
    '''A packet is an object that abstract the transmitted message.
    '''

    def from_bytes(self, msg: bytes):
        # msg = str(msg, encoding="utf-8")
        self._body = json.loads(msg, object_hook=quru_load_hook)

    def wrap(self) -> bytes:
        '''Return the serialized data in bytes so that it
        could be transported by MQ broker.
        '''
        msg_str = json.dumps(self._body, cls=QuruJSONEncoder)
        if len(msg_str) > 2000:
            msg_str = json.dumps(RedisObj(msg_str), cls=QuruJSONEncoder)
        return bytes(msg_str, encoding="utf-8")
