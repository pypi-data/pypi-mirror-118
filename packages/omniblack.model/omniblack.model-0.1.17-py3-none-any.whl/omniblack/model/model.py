"""
    @public
"""
from __future__ import annotations

from dataclasses import dataclass, field as data_field
from types import SimpleNamespace
from asyncio import create_task
from functools import wraps

from public import public
from rx.core.typing import Scheduler

from .coercion import coerce_from, coerce_to
from .format_registry import FormatRegistry
from .struct import StructRegistry
from .type_registry import TypeRegistry
from .promise import Promise


@public
@dataclass
class Model:
    name: str
    scheduler: Scheduler = None
    types: SimpleNamespace = data_field(init=False, repr=False)
    structs: StructRegistry = data_field(init=False, repr=False)
    formats: FormatRegistry = data_field(init=False, repr=False)

    coerce_from = coerce_from
    coerce_to = coerce_to

    def __hash__(self):
        return hash(id(self))

    def __post_init__(self):
        self.types = TypeRegistry(self)
        self.structs = StructRegistry(self)
        self.formats = FormatRegistry(self)
        self.__load = None

    def start_load(self, coro):
        task = create_task(coro, name=f'Model {self.name} load')
        prom = Promise.from_task(task)
        self.__load = prom

    def require(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if self.__load is None:
                raise TypeError('Model load not started')
            else:
                await self.__load
                return await func(*args, **kwargs)

        return wrapper
