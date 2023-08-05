import asyncio

from aiozipkin.span import SpanAbc

from ..quru_logger import logger
from ..words import TransacException


class Transactifier:
    def __init__(self, func, undo_func=None, span: SpanAbc = None):
        self._func = func
        if undo_func is None:
            undo_func = func
        self._undo_func = undo_func
        self._undo_args = []
        self._running_tasks = []
        self._span = span

    async def _deputy(self, *args, **kwargs):
        data = None
        dst_method = "default"
        if args:
            dst = args[0]
        elif "dst" in kwargs:
            dst = kwargs['dst']
        if len(args) > 1:
            data = args[1]
        elif "data" in kwargs:
            data = kwargs["data"]
        if len(args) > 2:
            dst_method = args[2]
        elif "task" in kwargs:
            dst_method = kwargs["task"]
        self._undo_args.append([dst, data, "undo_" + dst_method])
        task = asyncio.create_task(self._func(*args, **kwargs))
        self._running_tasks.append(task)
        await task
        return task.result()

    async def __aenter__(self):
        return self._deputy

    async def __aexit__(self, exc_type, exc_val, traceback):
        if isinstance(exc_val, TransacException):
            # Has to wait for all running tasks done, then start
            # create undo request, otherwise there will be the possibility
            # where "undo" comes before "do".
            logger.warning("Got_TransacException_in_sub_calling.",
                           error=str(exc_val), span=self._span)
            tks_res = await \
                asyncio.gather(*self._running_tasks,
                               return_exceptions=True)
            undo_tks = []
            logger.warning("Sending_undo_requests.", span=self._span)
            for i, tk_res in enumerate(tks_res):
                # if not isinstance(tk_res, TransacException): # This line should be un-comment
                # if the transaction is fine with DB transaction.
                undo_tks.append(asyncio.create_task(
                    self._undo_func(*self._undo_args[i])))
            await asyncio.gather(*undo_tks)
            logger.debug("Undo_done.", span=self._span)
        return False
