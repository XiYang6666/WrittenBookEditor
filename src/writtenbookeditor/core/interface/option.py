from dataclasses import dataclass, field
from typing import Any, Optional


__all__ = [
    "BaseOption",
    "StringOption",
    "IntOption",
    "FloatOption",
    "BoolOption",
    "ChoiceOption",
]


@dataclass
class BaseOption:
    default: Any
    description: Optional[str] = None
    hide: bool = False

    def __post_init__(self):
        if type(self) is BaseOption:
            raise NotImplementedError()


@dataclass
class StringOption(BaseOption):
    default: str = ""


@dataclass
class IntOption(BaseOption):
    default: int = 0
    max_value: Optional[int] = None
    min_value: Optional[int] = None


@dataclass
class FloatOption(BaseOption):
    default: float = 0.0
    max_value: Optional[float] = None
    min_value: Optional[float] = None


@dataclass
class BoolOption(BaseOption):
    default: bool = False
    hide: bool = False


@dataclass
class ChoiceOption(BaseOption):
    choices: list[str] = field(default_factory=list)
    default: str = None  # type: ignore
    editable: bool = False
    hide: bool = False

    def __post_init__(self):
        assert self.choices, "ChoiceOption must have at least one choice"
        self.default = self.choices[0]
