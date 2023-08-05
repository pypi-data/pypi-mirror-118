from __future__ import annotations
from functools import wraps
from asyncio import Task, Future

from anyio import Event


def to_iter(func):
    @wraps(func)
    def method(*args, **kwargs):
        value = yield from func(*args, **kwargs).__await__()
        return value

    return method


class Promise:
    def __init__(self):
        self.__value = None
        self.__error = None
        self.__event = Event()

    @to_iter
    async def __await__(self):
        await self.__event.wait()
        if self.__error is not None:
            raise self.__error

        return self.__value

    def resolve(self, value):
        if self.__event.is_set():
            raise TypeError('Promise has already been settled')

        self.__value = value
        self.__event.set()

    def reject(self, error):
        if self.__event.is_set():
            raise TypeError('Promise has already been settled')

        self.__error = error
        self.__event.set()

    def __task_done(self, future: Future) -> None:
        try:
            result = future.result()
        except Exception as err:
            self.reject(err)
        else:
            self.resolve(result)

    @classmethod
    def from_task(cls, task: Task) -> Promise:
        prom = cls()
        task.add_done_callback(prom.__task_done)
        return prom
