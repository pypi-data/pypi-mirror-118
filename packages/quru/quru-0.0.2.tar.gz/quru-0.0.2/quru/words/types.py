import abc
import hashlib
import json

import aiozipkin as az

from ..quru_logger import logger
from ..redis_clt import redis_client

_type_pool = {}


class TransmittableABC(abc.ABCMeta):
    def __init__(cls, name, bases, clsdict):
        if cls.__name__ != "Transmittable" and issubclass(cls, Transmittable):
            _type_pool[cls.__name__] = cls
        pass


class Transmittable(metaclass=TransmittableABC):
    '''Instance of class whose super class is this one would be able to
    be transmitted bewteen quru services. 
    '''
    @abc.abstractclassmethod
    def deserialize(cls):
        pass

    @abc.abstractmethod
    def serialize(self):
        pass


class InternalTransmittable(Transmittable):
    def __init__(self, body):
        self._body = body

    def serialize(self):
        return self._body

    @classmethod
    def deserialize(cls, body):
        return cls(body=body)


class RedisObj(InternalTransmittable):
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

    @classmethod
    def deserialize(cls, data):
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


class TraceContext(InternalTransmittable):
    def serialize(self):
        return self._body.make_headers()

    @classmethod
    def deserialize(cls, data):
        return cls(az.make_context(data))


class TransmittableException(Exception, InternalTransmittable):
    def __init__(self, msg=""):
        Exception.__init__(self, msg)
        body = {'msg': msg}
        InternalTransmittable.__init__(self, body)

    @classmethod
    def deserialize(cls, data):
        return cls(data['msg'])


class TransacException(TransmittableException):
    @classmethod
    def deserialize(cls, data):
        return cls(data['msg'])


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


class QuruJSONEncoder(json.JSONEncoder):
    '''Encoding class to serialize Python object
    into dict.
    '''
    def default(self, obj):
        '''
        Args:
            obj (any): Any objects that exposes a serialize
            method to serialize itself into json format.
        '''
        if isinstance(obj, set):
            new_obj = {
                'MARKER::CLASS': "set",
                'MARKER::DATA': list(obj)
            }
            return new_obj
        if isinstance(obj, Transmittable):
            new_obj = {
                'MARKER::CLASS': obj.__class__.__name__,
                'MARKER::DATA': obj.serialize()
            }
            return new_obj
        try:
            return json.JSONEncoder.default(self, obj)
        except Exception as e:
            print(e)
            pass


def quru_load_hook(item):
    '''Used by packet when loading json to recover
    the serialized Python object.
    Args:
        item (dict): the dict encoding a Python object.
    '''
    if "MARKER::CLASS" in item:
        if item["MARKER::CLASS"] == "set":
            return set(item["MARKER::DATA"])
        obj = _type_pool[item['MARKER::CLASS']].deserialize(item['MARKER::DATA'])
        if item["MARKER::CLASS"] == "RedisObj":
            return json.loads(obj, object_hook=quru_load_hook)
        else:
            return obj
    return item
