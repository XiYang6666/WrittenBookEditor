"""
注册器

使用元数据注册适配器和格式化器.
"""

from dataclasses import dataclass
from typing import Mapping, Sequence, Type

from writtenbookeditor.core.interface.adapter import Adapter
from writtenbookeditor.core.interface.formatter import Formatter
from writtenbookeditor.core.interface.option import OptionField, OptionTableMeta


@dataclass(frozen=True)
class AdapterMeta(OptionTableMeta[Adapter]):
    """
    适配器元数据
    """

    features: Sequence[str]


@dataclass(frozen=True)
class FormatterMeta(OptionTableMeta[Formatter]):
    """
    格式化器元数据
    """

    features: Sequence[str]


adapters: dict[str, AdapterMeta] = {}
formatters: dict[str, FormatterMeta] = {}


def add_adapter(
    name: str,
    type: Type[Adapter],
    option_fields: Mapping[str, OptionField],
    sub_tables: Mapping[str, OptionTableMeta],
    features: Sequence[str],
) -> AdapterMeta:
    meta = AdapterMeta(name, type, option_fields, sub_tables, features)
    adapters[name] = meta
    return meta


def add_formatter(
    name: str,
    type: Type[Formatter],
    option_fields: Mapping[str, OptionField],
    sub_tables: Mapping[str, OptionTableMeta],
    features: Sequence[str],
) -> FormatterMeta:
    meta = FormatterMeta(name, type, option_fields, sub_tables, features)
    formatters[name] = meta
    return meta
