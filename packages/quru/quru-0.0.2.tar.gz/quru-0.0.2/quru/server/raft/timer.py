import asyncio
import concurrent
import traceback
import types


class Timer:
    """Scheduling periodic callbacks"""
    def __init__(self, interval, callback):
        self.interval = interval
        self.callback = callback
        self.loop = asyncio.get_event_loop()

        self.is_active = False
        self._running_task = None

    def start(self, at_once=False) -> asyncio.Task:
        self.is_active = True
        self._running_task = self.loop.create_task(self._run(at_once))
        return self._running_task

    async def _run(self, at_once):
        if not at_once:
            await asyncio.sleep(self.get_interval())
        while self.is_active:
            try:
                if isinstance(self.callback, types.CoroutineType):
                    await self.callback
                else:
                    tmp = self.callback()
                    if isinstance(tmp, types.CoroutineType):
                        await tmp
            except concurrent.futures._base.CancelledError:
                pass
            except Exception:
                traceback.print_exc()
                raise
            await asyncio.sleep(self.get_interval())

    def stop(self):
        if self._running_task is not None \
         and not self._running_task.done():
            self._running_task.cancel()
        self.is_active = False

    def reset(self):
        self.stop()
        self.start()

    def get_interval(self):
        return self.interval() if callable(self.interval) else self.interval
