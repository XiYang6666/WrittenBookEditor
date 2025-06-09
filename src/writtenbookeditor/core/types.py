from dataclasses import dataclass
from typing import Any, Callable, Mapping, Optional, Protocol, Sequence, get_args

from .interface.adapter import Adapter
from .interface.formatter import Formatter
from .interface.option import BaseOption


class OptionTable(Protocol):
    _option_table_name: str


@dataclass(frozen=True)
class OptionConfigMeta[T]:
    name: Optional[str]
    creater: Callable[[], T]
    options: "Optional[Mapping[str,BaseOption]]"
    tables: "Optional[Mapping[str,OptionConfigMeta]]"


T_type = get_args(OptionConfigMeta[int])[0]


@dataclass(frozen=True)
class AdapterMeta:
    name: str
    creater: Callable[[Mapping[str, Any]], Adapter]
    features: Sequence[str]
    options: Optional[OptionConfigMeta]


@dataclass(frozen=True)
class FormatterMeta:
    name: str
    creater: Callable[[Mapping[str, Any]], Formatter]
    features: Sequence[str]
    options: Optional[OptionConfigMeta]
