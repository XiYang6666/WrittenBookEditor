"""
配置&配置字段&配置表
"""

from dataclasses import dataclass, field
from typing import Any, Mapping, Optional, Type

__all__ = [
    "OptionField",
    "StringOptionField",
    "IntOptionField",
    "FloatOptionField",
    "BoolOptionField",
    "ChoiceOptionField",
    "OptionTableMeta",
]


@dataclass
class OptionField:
    default: Any
    description: Optional[str] = None
    hide: bool = False

    def __post_init__(self):
        if type(self) is OptionField:
            raise NotImplementedError()


@dataclass
class StringOptionField(OptionField):
    default: str = ""


@dataclass
class IntOptionField(OptionField):
    default: int = 0
    max_value: Optional[int] = None
    min_value: Optional[int] = None


@dataclass
class FloatOptionField(OptionField):
    default: float = 0.0
    max_value: Optional[float] = None
    min_value: Optional[float] = None


@dataclass
class BoolOptionField(OptionField):
    default: bool = False
    hide: bool = False


@dataclass
class ChoiceOptionField(OptionField):
    choices: list[str] = field(default_factory=list)
    default: str = None  # type: ignore
    editable: bool = False
    hide: bool = False

    def __post_init__(self):
        assert self.choices, "ChoiceOption must have at least one choice"
        self.default = self.choices[0]


type ConfigData = Mapping[str, Any]


@dataclass(frozen=True)
class OptionTableMeta[T]:
    name: str
    type: Type[T]
    option_fields: Mapping[str, OptionField]
    sub_tables: "Mapping[str, OptionTableMeta[Any]]"
