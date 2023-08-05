from enum import Enum

from volt.utils.abstracts import JsonObject
from volt.utils.type_hint import JSON


class EmbedType(Enum):
    pass


class Embed(JsonObject):
    """
    discord embed object.
    """

    @classmethod
    def from_json(cls, data: JSON) -> 'JsonObject':
        pass

    def __init__(
            self,
            title: str
    ):
        pass

    def to_json(self) -> JSON:
        pass
