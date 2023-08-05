import asyncio
from typing import Coroutine

from .type_hint import CoroutineFunction, AnyFunction


async def _scheduled_task(delay: int, coro: Coroutine):
    await asyncio.sleep(delay)
    await coro


async def async_callback_handler(coro: CoroutineFunction, callback: CoroutineFunction):
    setattr(coro, '__callback__', callback)
    result = await coro()
    await callback(result)
    del coro.__callback__


def async_schedule_task(delay: int, coro: CoroutineFunction, callback: AnyFunction) -> asyncio.Task:
    if asyncio.iscoroutinefunction(callback):
        coro = async_callback_handler(coro, callback)
        return asyncio.get_event_loop().create_task(_scheduled_task(delay, coro))
    elif callable(callback):
        task = asyncio.get_event_loop().create_task(_scheduled_task(delay, coro()))
        task.add_done_callback(callback)
        return task
