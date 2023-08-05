from ...words import RaftLog
from .abs_types import LodgeABC


class MemLodge(LodgeABC, dict):

    def apply(self, log: RaftLog):
        assert isinstance(log, RaftLog)
        for cmd in log.command.cmds:
            try:
                if cmd[0] == "change":
                    if cmd[1][0] in self:
                        self[cmd[1][0]] = cmd[1][1]
                    else:
                        raise KeyError("[{}] not exist.".format(cmd[1][0]))
                else:
                    getattr(self, cmd[0])(*(cmd[1]))
            except Exception as e:
                if not log.ignore_exc:
                    raise e
