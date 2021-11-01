from enum import IntEnum, unique
from typing import Any, List, Tuple


@unique
class IntChoice(IntEnum):
    @classmethod
    def choices(cls) -> Tuple[Tuple[int, str], ...]:
        return tuple((i.value, i.name) for i in cls)

    @classmethod
    def name_from_value(cls, value: int) -> Any:
        for item in cls:
            if item.value == value:
                return item.name
        return ""

    @classmethod
    def enum_member_by_name(cls, name: str) -> Any:
        return cls[name]

    @classmethod
    def enum_member_by_value(cls, value: int) -> Any:
        return cls[cls.name_from_value(value)]

    @classmethod
    def values(cls) -> List[int]:
        return [i.value for i in cls]
