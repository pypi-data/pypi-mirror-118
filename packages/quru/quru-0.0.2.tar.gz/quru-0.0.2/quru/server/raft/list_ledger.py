import typing
from collections import deque

from .abs_types import LedgerABC
from ...words import RaftLog, RaftCommand


class ListLedger(LedgerABC):
    def __init__(self, max_cap=4380):
        self._max_cap = max_cap
        self._data: typing.Deque[RaftLog] = deque(maxlen=self._max_cap)
        first_log = RaftLog()
        first_log.term = 0
        first_log.index = 0
        cmd = RaftCommand().as_set("x", None)
        first_log.command = cmd
        self.append(first_log)
        self._offset = 0

    def find_term_start(self, term) -> typing.Tuple[int, int]:
        if term < 0:
            raise ValueError("Term value cannot be less than 0.")
        cur_pos = len(self._data) - 1
        while cur_pos >= 0:
            cur_log: RaftLog = self._data[cur_pos]
            if cur_log.term <= term:
                break
            cur_pos -= 1
        found_term = cur_log.term
        while cur_pos >= 1 and self._data[cur_pos - 1].term == found_term:
            cur_pos -= 1
        return self._data[cur_pos].term, self._data[cur_pos].index

    def append(self, log: RaftLog):
        if len(self._data) == self._max_cap:
            self._offset += 1
        self._data.append(log)

    def replace(self, start_idx: int, logs: typing.List[RaftLog]):
        start_idx -= self._offset
        if start_idx < 0:
            raise ValueError("This node is behind too much, "
                             "cannot be recovered!")
        start_idx = len(self._data) if start_idx > len(self._data) \
            else start_idx
        while len(self._data) > start_idx:
            self._data.pop()
        dropped_logs = max(0, len(logs) + len(self._data) - self._max_cap)
        self._offset += dropped_logs
        for i in range(len(logs)):
            self._data.append(logs[i])
        return

    def __getitem__(self, idx) -> RaftLog:
        if isinstance(idx, int):
            return self._getitem_int(idx)
        elif isinstance(idx, slice):
            assert idx.stop is None, "Only accpet [x:] slicing."
            res = []
            if idx.start < 0:
                for i in range(idx.start, 0):
                    res.append(self._getitem_int(i))
            else:
                for i in range(idx.start, len(self)):
                    res.append(self._getitem_int(i))
            return res
        raise IndexError("Unaccepted_idx_type.")

    def _getitem_int(self, idx: int) -> RaftLog:
        if idx < 0:
            return self._data[idx] if len(self._data) >= -idx else None
        real_idx = idx - self._offset
        if real_idx < 0:
            raise IndexError("This node only has logs with "
                             "index larger than {}, less "
                             "than {}. You're accessing {}.".format(
                                self._offset,
                                self._offset + len(self._data),
                                real_idx))
        elif len(self._data) < real_idx:
            raise IndexError("This node only has logs with "
                             "index larger than {}, less "
                             "than {}. You're accessing {}.".format(
                                self._offset,
                                self._offset + len(self._data),
                                real_idx))
        else:
            return self._data[real_idx]

    def __setitem__(self, idx: int, value: RaftLog):
        if idx < 0:
            if len(self._data) >= -idx:
                self._data[idx] = value
            return
        real_idx = idx - self._offset
        if real_idx < 0:
            raise ValueError("Cannot set this log. "
                             "This node only has logs with "
                             "index larger than {}, less "
                             "than {}".format(self._offset,
                                              self._offset + len(self._data)))
        elif len(self._data) < real_idx:
            raise ValueError("The slot does not exist. "
                             "This node only has logs with "
                             "index larger than {}, less "
                             "than {}".format(self._offset,
                                              self._offset + len(self._data)))
        else:
            self._data[real_idx] = value

    def __len__(self):
        return self._offset + len(self._data)
