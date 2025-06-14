"""
配置注入器
"""

from typing import Any, Mapping, Type

from writtenbookeditor.core.interface.option import ConfigData, OptionField, OptionTableMeta


def get_option_table_info(cls: Type[Any]) -> tuple[Mapping[str, OptionField], Mapping[str, OptionTableMeta]]:
    """
    从类中读取配置表信息
    """
    options = {}
    sub_tables = {}

    # 遍历属性
    for attr_name, attr_value in cls.__dict__.items():
        if attr_name.startswith("_"):
            # 跳过私有属性
            continue

        if isinstance(attr_value, OptionField):
            options[attr_name] = attr_value

        if isinstance(attr_value, OptionTableMeta):
            sub_tables[attr_name] = attr_value

    return options, sub_tables


def expand_option_field(meta: OptionTableMeta[Any]) -> Mapping[str, OptionField]:
    """
    从配置表元数据中展开配置字段
    """
    config = {}
    for name, option in meta.option_fields.items():
        config[f"{meta.name}:{name}"] = option
    for name, table_meta in meta.sub_tables.items():
        sub_config = expand_option_field(table_meta)
        config.update(sub_config)
    return config


def create_object[T](
    meta: OptionTableMeta[T],
    config: ConfigData,
) -> T:
    """
    根据配置表元数据和配置数据创建对象
    """
    # 创建对象
    try:
        obj = meta.type()
    except TypeError:
        info = f"Failed to create object of type {meta.type.__name__}, please make sure it has a default constructor."
        raise RuntimeError(info)
    # 注入配置
    for origin_name, _ in meta.option_fields.items() if meta.option_fields else {}:
        name = f"{meta.name}:{origin_name}"
        assert name in config, f"Option {name} is not in config"
        setattr(obj, origin_name, config[name])

    # 注入配置表
    for name, table_meta in meta.sub_tables.items() if meta.sub_tables else {}:
        table = create_object(table_meta, config)
        setattr(obj, name, table)

    return obj
