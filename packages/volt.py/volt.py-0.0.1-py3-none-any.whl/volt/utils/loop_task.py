import asyncio
from datetime import timedelta, time, timezone, datetime
from typing import Optional, Coroutine, Type
from src.utils.type_hint import CoroutineFunction
from src.utils.dtutil import utcnow, is_leap_year


class ZeroSecondsTaskNotSupported(Exception):
    def __init__(self):
        super(ZeroSecondsTaskNotSupported, self).__init__('LoopTask with 0 seconds delay is not supported due to performance issue.')


class LoopTask:
    __slots__ = (
        'loop',
        '_callback',
        '_args',
        '_kwargs',
        '_ignored_exceptions',
        '_task',
        '_days',
        '_hours',
        '_minutes',
        '_seconds',
        '_running',
        '_before_hook',
        '_after_hook'
    )

    def __init__(self, coro: CoroutineFunction, args, kwargs, days: int, hours: int, minutes: int, seconds: int):
        try:
            self.loop = asyncio.get_running_loop()
        except RuntimeError:
            self.loop = asyncio.get_event_loop()
        # Callback info
        self._callback = coro
        self._args = args
        self._kwargs = kwargs or {}     # You can use keyword-arguments dictionary as namespace to pass on callback functions (before&after invoke, callback)
        self._ignored_exceptions: list[Type[Exception]] = []
        self._task = None

        # Looping delay info
        self._days = days
        self._hours = hours
        self._minutes = minutes
        self._hours = hours
        self._minutes = minutes
        self._seconds = seconds

        # Flags
        self._running: bool = False

        # Hook coroutine functions.
        self._before_hook: Optional[CoroutineFunction] = None
        self._after_hook: Optional[CoroutineFunction] = None

    @property
    def total_delay(self) -> timedelta:
        return timedelta(days=self._days, hours=self._hours, minutes=self._minutes, seconds=self._seconds)

    @property
    def is_running(self) -> bool:
        return self._running

    def __call__(self, *args, **kwargs) -> Coroutine:
        """
        Call callback coroutine function without any hooks.
        :param args:
        :param kwargs:
        """
        return self._callback(*args, **kwargs)

    def before_invoke(self, coro: CoroutineFunction):
        if not asyncio.iscoroutinefunction(coro):
            raise TypeError(f'LoopTask.before_invoke must be coroutine function, not {type(coro)}.')
        self._before_hook = coro

    def after_invoke(self, coro: CoroutineFunction):
        if not asyncio.iscoroutinefunction(coro):
            raise TypeError(f'LoopTask.after_invoke must be coroutine function, not {type(coro)}.')
        self._after_hook = coro

    async def _handle_exceptions(self, exc_type: Type[Exception], exc_value: Exception, traceback):
        """
        Default exception handler. Can be replaced by `@LoopTask.handle_exception` decorator.
        :param exc_type: Exception type.
        :param exc_value: Exception object.
        :param traceback: Exception traceback object.
        """
        from sys import stderr
        print(f'{exc_type.__name__} exception has been occurred while running youtube.LoopTask! Gracefully stop task.', file=stderr)
        self.cancel()

    async def _run(self):
        args = self._args or tuple()
        kwargs = self._kwargs or {}
        if self._before_hook:
            await self._before_hook(*args, **kwargs)
        while self._running:
            try:
                await self._callback(*args, **kwargs)
            except self._ignored_exceptions as e:
                await self._handle_exceptions(e.__class__, e, e.__traceback__)
            finally:
                await asyncio.sleep(delay=self.total_delay.total_seconds())
        if self._after_hook:
            await self._after_hook(*args, **kwargs)

    def start(self, *args, **kwargs):
        if args:
            self._args = args
        if kwargs:
            self._kwargs = kwargs
        self._running = True
        self._task = self.loop.create_task(self._run(), name=f'LoopTask.run(id={id(self)})')
        return self._task

    def cancel(self):
        self._running = False


def loop(days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0):
    def wrapper(coro: CoroutineFunction):
        if not asyncio.iscoroutinefunction(coro):
            raise TypeError('YoutubeEventLoop.LoopTask.callback must be coroutine function.')
        if not any((days, hours, minutes, seconds)):
            # total_delay = 0. Why we use this callback as LoopTask? just call it.
            raise ZeroSecondsTaskNotSupported()

        task: LoopTask = LoopTask(coro, None, None, days, hours, minutes, seconds)
        return task
    return wrapper


class CronLikeTask(LoopTask):
    def __init__(self, coro: CoroutineFunction, args, kwargs, cron_time: time, days=0, hours=0, minutes=0, seconds=0):
        if not any((days, hours, minutes, seconds)):
            # If all delay params are 0, then set delay to 1 day.
            days = 1
        super(CronLikeTask, self).__init__(coro, args, kwargs, days, hours, minutes, seconds)
        if cron_time.tzinfo is None:
            # Assume as UTC.
            cron_time.replace(tzinfo=timezone.utc)
        self.cron_time: time = cron_time

    def start(self, *args, **kwargs):
        self.loop.call_later(self._calc_delay().total_seconds(), lambda: super(CronLikeTask, self).start())

    def _calc_delay(self) -> timedelta:
        now = utcnow()
        year = now.year + 1 if now.month == 12 and now.day == 31 and now.time() > self.cron_time else now.year
        if now.month in (1, 3, 5, 7, 8, 10, 12):
            month = now.month + 1 if now.day == 31 and now.time() > self.cron_time else now.month
        elif now.month in (4, 6, 9, 11):
            month = now.month + 1 if now.day == 30 and now.time() > self.cron_time else now.month
        else:
            max_day = 29 if is_leap_year(now.year) else 28
            month = now.month + 1 if now.day == max_day and now.time() > self.cron_time else now.month

        day = now.day + 1 if now.time() > self.cron_time else now.day
        start_dt = datetime(year, month, day, hour=self.cron_time.hour, minute=self.cron_time.minute,
                            second=self.cron_time.second)
        return start_dt - utcnow()


def cron(hour: int, minute: int, second: int):
    def wrapper(coro: CoroutineFunction):
        if not asyncio.iscoroutinefunction(coro):
            raise TypeError('YoutubeEventLoop.LoopTask.callback must be coroutine function.')
        if not any((hour, minute, second)):
            # total_delay = 0. Why we use this callback as LoopTask? just call it.
            raise ZeroSecondsTaskNotSupported()
        return CronLikeTask(coro, None, None, time(hour, minute, second))
    return wrapper
