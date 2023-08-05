from abc import ABCMeta, abstractmethod
from functools import wraps

from .utils.type_hint import JSON


class JsonObject(metaclass=ABCMeta):
    """
    ABC for JSON-parsed python objects.
    """
    @classmethod
    @abstractmethod
    def from_json(cls, data: JSON) -> 'JsonObject':     ...

    @abstractmethod
    def to_json(self) -> JSON:  ...


class SingletonMeta(type):
    __classes__: dict[str, type] = {}
    __instances__: dict[type, object] = {}
    __init_required__: list['SingletonMeta'] = []

    def __new__(mcs, name: str, bases, namespace: dict):
        if name in mcs.__classes__:
            return mcs.__classes__.get(name)
        cls = mcs.__classes__[name] = super().__new__(mcs, name, bases, namespace)

        original_new = cls.__new__
        original_init = cls.__init__

        @wraps(original_new)
        def __new__(cls: type, *args, **kwargs):
            # instance = mcs.__instances__.get(mcs.__classes__.get(cls.__name__))
            instance = mcs.__instances__.get(cls)
            # print('Checking instance in __new__ :', instance)
            if instance is None:
                # print('Entered original __new__ call.')
                instance = mcs.__instances__[cls] = original_new(cls) if original_new.__qualname__ == object.__new__.__qualname__ else original_new(cls, *args, **kwargs)
                mcs.__init_required__.append(cls)
            return instance

        cls.__new__ = __new__

        @wraps(original_init)
        def __init__(self, *args, **kwargs):
            # instance = mcs.__instances__.get(mcs.__classes__.get(self.__class__.__name__))
            instance = mcs.__instances__.get(self.__class__)
            # print('Checking instance in __init__ :', instance)
            if self.__class__ in mcs.__init_required__:
                # print('Entered original __init__ call.')
                original_init(self, *args, **kwargs)
                mcs.__init_required__.remove(self.__class__)

        cls.__init__ = __init__

        return cls


class Snowflake:
    __slots__ = ('id',)
    id: int



