from typing import Any, Mapping, Optional, Type

from .types import OptionConfigMeta
from .interface.option import BaseOption


def get_option_meta(cls: Type, name: Optional[str] = None) -> OptionConfigMeta:
    """
    获取配置项元数据
    """
    options = {}
    tables = {}

    # 遍历属性
    for attr_name, attr_value in cls.__dict__.items():
        if attr_name.startswith("_"):
            # 跳过私有属性
            continue

        if isinstance(attr_value, BaseOption):
            options[attr_name] = attr_value

        if isinstance(attr_value, OptionConfigMeta):
            tables[attr_name] = attr_value

    return OptionConfigMeta(name, cls, options, tables)


def inject_options[T](obj: T, meta: OptionConfigMeta, config: Mapping[str, Any], prefix: Optional[str] = None) -> T:
    """
    注入配置项
    """
    # 注入配置
    for origin_name, _ in meta.options.items() if meta.options else {}:
        name = f"{prefix}:{origin_name}" if prefix else origin_name
        assert name in config, f"Option {name} is not in config"
        setattr(obj, origin_name, config[name])

    # 注入配置表
    for name, table in meta.tables.items() if meta.tables else {}:
        table_instance = table.creater()
        inject_options(table_instance, table, config, table.name)
        setattr(obj, name, table_instance)

    return obj
