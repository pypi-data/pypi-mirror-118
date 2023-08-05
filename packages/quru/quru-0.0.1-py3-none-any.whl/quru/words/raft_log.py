from .types import RaftLogABC, MsgObj


class RaftCommand(MsgObj):
    def __init__(self, body=None):
        if body is None:
            body = []
        super().__init__(body)

    def as_set(self, key, value):
        cmd = ["__setitem__", [key, value]]
        self._body.append(cmd)
        return self

    def as_change(self, key, value):
        cmd = ["change", [key, value]]
        self._body.append(cmd)
        return self

    def as_pop(self, key):
        cmd = ["pop", [key]]
        self._body.append(cmd)
        return self

    @property
    def cmds(self):
        for cmd in self._body:
            yield cmd


class RaftLog(RaftLogABC, MsgObj):
    def __init__(self, body=None):
        if body is None:
            body = {}
        super().__init__(body)

    @property
    def index(self):
        return self._body['index']

    @index.setter
    def index(self, value):
        self._body['index'] = value

    @property
    def term(self):
        return self._body['term']

    @property
    def command(self) -> RaftCommand:
        if 'command' not in self._body:
            self.command = RaftCommand()
        return self._body['command']

    @command.setter
    def command(self, value):
        self._body['command'] = value

    @term.setter
    def term(self, value):
        self._body['term'] = value

    @property
    def ignore_exc(self):
        '''Configure whether to ignore the exception when apply this log into lodge.
        '''
        if "ignore_exc" in self._body:
            return self._body['ignore_exc']
        else:
            return False

    @ignore_exc.setter
    def ignore_exc(self, value):
        self._body['ignore_exc'] = value


class RaftQuorumLog(RaftLog):
    '''Note that the command in RaftQuorumLog must be
    indempotent.
    '''
    pass
