import asyncio
import typing
from datetime import timedelta
from .type_hint import CoroutineFunction, AnyNumber


__all__ = (
    'LoopTask',
    'loop'
)


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

    def __init__(self, coro: CoroutineFunction, args, kwargs, days: int, hours: int, minutes: int, seconds: AnyNumber):
        try:
            self.loop = asyncio.get_running_loop()
        except RuntimeError:
            self.loop = asyncio.get_event_loop()
        # Callback info
        self._callback = coro
        self._args = args
        self._kwargs = kwargs or {}     # You can use keyword-arguments dictionary as namespace to pass on callback functions (before&after invoke, callback)
        self._ignored_exceptions: typing.List[typing.Type[Exception]] = []
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
        self._before_hook: typing.Optional[CoroutineFunction] = None
        self._after_hook: typing.Optional[CoroutineFunction] = None

    @property
    def total_delay(self) -> timedelta:
        return timedelta(days=self._days, hours=self._hours, minutes=self._minutes, seconds=self._seconds)

    @property
    def is_running(self) -> bool:
        return self._running

    @property
    def args(self) -> typing.Tuple:
        return self._args

    @args.setter
    def args(self, new: typing.Tuple):
        self._args = new

    @property
    def kwargs(self) -> typing.Mapping[str, typing.Any]:
        return self._kwargs     # Maybe we need to freeze kwargs dict to control dictionary mutation.

    @kwargs.setter
    def kwargs(self, new: typing.Mapping[str, typing.Any]):
        self._kwargs = new

    def __call__(self, *args, **kwargs) -> typing.Coroutine:
        """
        Call callback coroutine function without any hooks.
        :param args:
        :param kwargs:
        """
        return self._callback(*self._args, **self._kwargs)

    def before_invoke(self, coro: CoroutineFunction):
        if not asyncio.iscoroutinefunction(coro):
            raise TypeError(f'LoopTask.before_invoke must be coroutine function, not {type(coro)}.')
        self._before_hook = coro

    def after_invoke(self, coro: CoroutineFunction):
        if not asyncio.iscoroutinefunction(coro):
            raise TypeError(f'LoopTask.after_invoke must be coroutine function, not {type(coro)}.')
        self._after_hook = coro

    async def _handle_exceptions(self, exc_type: typing.Type[Exception], exc_value: Exception, traceback):
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
            if self._args is not None:
                self._args += args
            else:
                self._args = args
        if kwargs:
            if self._kwargs is not None:
                self._kwargs.update(kwargs)
            else:
                self._kwargs = kwargs
        self._running = True
        self._task = self.loop.create_task(self._run(), name=f'LoopTask.run(id={id(self)})')
        return self._task

    def cancel(self):
        self._running = False


def loop(days: int = 0, hours: int = 0, minutes: int = 0, seconds: AnyNumber = 0) -> typing.Callable[[CoroutineFunction], LoopTask]:
    def wrapper(coro: CoroutineFunction) -> LoopTask:
        if not asyncio.iscoroutinefunction(coro):
            raise TypeError('YoutubeEventLoop.LoopTask.callback must be coroutine function.')
        if not any((days, hours, minutes, seconds)):
            # total_delay = 0. Why we use this callback as LoopTask? just call it.
            raise ZeroSecondsTaskNotSupported()

        task: LoopTask = LoopTask(coro, None, None, days, hours, minutes, seconds)
        return task
    return wrapper
