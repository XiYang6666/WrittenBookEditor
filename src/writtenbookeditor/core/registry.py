"""
注册器

使用元数据注册适配器和格式化器.
"""

from dataclasses import dataclass
from typing import Collection, Mapping, Type

from writtenbookeditor.core.interface.adapter import Adapter
from writtenbookeditor.core.interface.exporter import Exporter
from writtenbookeditor.core.interface.formatter import Formatter
from writtenbookeditor.core.interface.option import OptionField, OptionTableMeta


@dataclass(frozen=True)
class FormatterMeta(OptionTableMeta[Formatter]):
    """
    格式化器元数据
    """

    producted_features: set[str]


@dataclass(frozen=True)
class AdapterMeta(OptionTableMeta[Adapter]):
    """
    适配器元数据
    """

    required_features: set[str]
    producted_features: set[str]


@dataclass(frozen=True)
class ExporterMeta(OptionTableMeta[Exporter]):
    """
    导出器元数据
    """

    required_features: set[str]


formatters: dict[str, FormatterMeta] = {}
adapters: dict[str, AdapterMeta] = {}
exporters: dict[str, ExporterMeta] = {}


def add_formatter(
    name: str,
    type: Type[Formatter],
    option_fields: Mapping[str, OptionField],
    sub_tables: Mapping[str, OptionTableMeta],
    producted_features: Collection[str],
) -> FormatterMeta:
    meta = FormatterMeta(name, type, option_fields, sub_tables, set(producted_features))
    formatters[name] = meta
    return meta


def add_adapter(
    name: str,
    type: Type[Adapter],
    option_fields: Mapping[str, OptionField],
    sub_tables: Mapping[str, OptionTableMeta],
    required_features: Collection[str],
    producted_features: Collection[str],
) -> AdapterMeta:
    meta = AdapterMeta(name, type, option_fields, sub_tables, set(required_features), set(producted_features))
    adapters[name] = meta
    return meta


def add_exporter(
    name: str,
    type: Type[Exporter],
    option_fields: Mapping[str, OptionField],
    sub_tables: Mapping[str, OptionTableMeta],
    required_features: Collection[str],
) -> ExporterMeta:
    meta = ExporterMeta(name, type, option_fields, sub_tables, set(required_features))
    exporters[name] = meta
    return meta
