import abc
import hashlib

import aiozipkin as az

from ..quru_logger import logger
from ..redis_clt import redis_client


class MsgObj(object):
    def __init__(self, body):
        self._body = body

    def serialize(self):
        return self._body

    @classmethod
    def deserialize(cls, body):
        return cls(body=body)


class RedisObj(MsgObj):
    def __init__(self, v):
        if isinstance(v, str):
            key = hashlib.sha256(bytes(v, encoding="utf-8")).hexdigest()
            body = {
                "key": key,
                "type": "STRING",
            }
            redis_client.set(key, v, ex=600)
            logger.debug("Saved_in_redis.", key=key)
        elif isinstance(v, list):
            v = "|||".join(v)
            key = hashlib.sha256(bytes(v, encoding="utf-8")).hexdigest()
            body = {
                "key": key,
                "type": "LIST",
            }
            redis_client.set(key, v, ex=600)
            logger.debug("Saved_in_redis.", key=key)
        else:
            raise ValueError("Only accept list or str type")
        super(RedisObj, self).__init__(body)

    @staticmethod
    def deserialize(data):
        key = data['key']
        value = redis_client.get(key)
        if value is None:
            logger.error("Message_in_redis_expired.", key=key)
            raise IOError("Payload in redis expired.")
        if isinstance(value, bytes):
            value = str(value, encoding="utf-8")
        if data['type'] == "LIST":
            value = value.split("|||")
        logger.debug("Fetched_in_redis.", key=key)
        return value


class TraceContext(MsgObj):
    def serialize(self):
        return self._body.make_headers()

    @staticmethod
    def deserialize(data):
        return TraceContext(az.make_context(data))


class TransmittableException(Exception, MsgObj):
    def __init__(self, msg=""):
        Exception.__init__(self, msg)
        body = {'msg': msg}
        MsgObj.__init__(self, body)

    @staticmethod
    def deserialize(data):
        return TransmittableException(data['msg'])


class TransacException(TransmittableException):

    @staticmethod
    def deserialize(data):
        return TransacException(data['msg'])


class RaftLogABC(metaclass=abc.ABCMeta):
    @abc.abstractproperty
    def index(self):
        raise NotImplementedError

    @abc.abstractproperty
    def term(self):
        raise NotImplementedError

    @abc.abstractproperty
    def command(self):
        raise NotImplementedError

    @abc.abstractproperty
    def ignore_exc(self):
        raise NotImplementedError
