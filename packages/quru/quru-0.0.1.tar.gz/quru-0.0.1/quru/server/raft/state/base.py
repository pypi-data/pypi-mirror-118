import abc
import asyncio

from aiozipkin.span import SpanAbc

from ..abs_types import CoreABC
from ....quru_logger import logger


def candidate_qualification(func):
    '''Check whether the candidate's last log is at least as updated
    as the subject.
    '''
    def wrap(self: BaseState, data: dict, span: SpanAbc = None):
        term = data['term']
        candidate_id = data['candidate_id']
        last_log_term: int = data['prev_log'].term \
            if data['prev_log'] is not None else float('-inf')
        last_log_index: int = data['prev_log'].index \
            if data['prev_log'] is not None else float('-inf')
        if term < self._current_term:
            logger.info(
                "Your_term_is_outdated._No!",
                refusing=candidate_id,
                my_term=self._current_term,
                your_term=term,
                span=span)
            return False
        elif term == self._current_term and\
            (self._voted_for is not None or
             candidate_id != self._voted_for):
            logger.info(
                "I've_already_voted._No!",
                span=span,
                refusing=candidate_id,
                voted_for=self._voted_for)
            return False
        elif last_log_term < self._core.ledger[-1].term or\
            (last_log_term == self._core.ledger[-1].term and
             last_log_index < self._core.last_applied.index):
            logger.info(
                "Your_log_is_outdated._No!",
                refusing=candidate_id,
                your_log_date="({}, {})".format(last_log_term, last_log_index),
                my_log_date="({}, {})".format(
                    self._core.ledger[-1].term, self._core.last_applied.index),
                span=span)
            # paper 5.4.1
            return False
        return func(self, data, span)
    return wrap


def log_consistency_check(func):
    '''Check and find the diverge of the leader's log and subject's log.
    '''
    def wrap(self: BaseState, data: dict, span: SpanAbc = None):
        logger.debug("Received_appent.", source=data['leader_id'])
        last_log_term: int = data['prev_log'].term \
            if data['prev_log'] is not None else float('-inf')
        last_log_index: int = data['prev_log'].index \
            if data['prev_log'] is not None else float('-inf')
        try:
            self_probe_log = self._core.ledger[last_log_index]
        except IndexError:
            self_probe_log = self._core.last_applied
        if self_probe_log.term > last_log_term:
            term, idx = self._core.ledger.find_term_start(last_log_term)
            logger.info(
                "My_last_log_term_is_fresher._No!",
                span=span,
                term_info="{}_vs_{}".format(
                    self_probe_log.term, last_log_term))
            return False, [term, idx]
        elif self_probe_log.term < last_log_term:
            term, idx = self._core.ledger.find_term_start(
                self_probe_log.term)
            logger.info(
                "Your_last_log_term_is_too_fresher._No!",
                span=span,
                term_info="{}_vs_{}".format(term, last_log_term))
            return False, [term, idx]
        elif self_probe_log.index < last_log_index:
            logger.info(
                "We're_different._No!",
                span=span,
                idx_info="{}_vs_{}".format(
                    self_probe_log.index,
                    last_log_index
                ))
            return False, [last_log_term, self_probe_log.index]
        return func(self, data, span)
    return wrap


class BaseState(metaclass=abc.ABCMeta):
    def __init__(self, core: CoreABC):
        self._current_term = -1
        self._voted_for = None
        self._leader_id = None

        self._commit_index = 0
        self._core: CoreABC = core

        self._trace: SpanAbc = None

    @abc.abstractmethod
    def on_request_vote(self, data):
        raise NotImplementedError

    @abc.abstractmethod
    def on_append_entries(self, data):
        raise NotImplementedError

    @abc.abstractmethod
    def start(self) -> asyncio.Task:
        raise NotImplementedError

    @abc.abstractmethod
    def stop(self):
        raise NotImplementedError

    # def on_broadcast(self, data, span: SpanAbc = None):
    #     logger.info("Keep_silent.", span=span)
    #     return None
