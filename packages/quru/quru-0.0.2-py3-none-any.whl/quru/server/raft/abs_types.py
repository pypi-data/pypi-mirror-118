import abc
import typing

from aiozipkin.span import SpanAbc

from ...server.protocol.abs_types import UpperLayerABC
from ...words.types import RaftLogABC


class LodgeABC(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def apply(self, log: RaftLogABC):
        raise NotImplementedError


class LedgerABC(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def find_term_start(self, term: int) -> typing.Tuple[int, int]:
        '''Starting from the end, find the head entry
        whose term <= passed-in term
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def replace(self, start_idx: int, logs: typing.List[RaftLogABC]):
        raise NotImplementedError

    @abc.abstractmethod
    def append(self, log: RaftLogABC):
        raise NotImplementedError

    @abc.abstractmethod
    def __getitem__(self, idx: int) -> RaftLogABC:
        raise NotImplementedError

    @abc.abstractmethod
    def __setitem__(self, idx: int, value: RaftLogABC):
        raise NotImplementedError

    @abc.abstractmethod
    def __len__(self):
        raise NotImplementedError


class CoreABC(UpperLayerABC):
    @abc.abstractproperty
    def role(self) -> str:
        raise NotImplementedError

    @abc.abstractproperty
    def ledger(self) -> LedgerABC:
        raise NotImplementedError

    @abc.abstractproperty
    def last_applied(self) -> RaftLogABC:
        '''Return the last log index and the last log term
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def to_candidate(self):
        raise NotImplementedError

    @abc.abstractmethod
    def to_leader(self):
        raise NotImplementedError

    @abc.abstractmethod
    def to_follower(self):
        raise NotImplementedError

    @abc.abstractmethod
    def create_trace(self, name="anonymous", span_name="unknown")\
            -> typing.Tuple[SpanAbc, SpanAbc]:
        raise NotImplementedError

    @abc.abstractmethod
    def new_child(self, trace: SpanAbc)\
            -> SpanAbc:
        raise NotImplementedError

    @abc.abstractproperty
    def quorum(self):
        raise NotImplementedError

    @abc.abstractproperty
    def quorum_size(self) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def in_quorum(self, peer: str) -> bool:
        raise NotImplementedError

    @abc.abstractproperty
    def cohort(self) -> typing.Generator:
        raise NotImplementedError

    @abc.abstractproperty
    def cohort_size(self) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def in_cohort(self, peer: str) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    async def call(self, dst: str, mode: str, data: dict, span=None):
        raise NotImplementedError

    @abc.abstractmethod
    def apply(self, log: RaftLogABC):
        raise NotImplementedError
