"""
注册器

包装 core.registry, 从类中获取元数据后注册.
"""

from typing import Callable, Collection, Optional, Type

from writtenbookeditor.core.injector import get_option_table_info
from writtenbookeditor.core.interface.adapter import Adapter
from writtenbookeditor.core.interface.exporter import Exporter
from writtenbookeditor.core.interface.formatter import Formatter
from writtenbookeditor.core.interface.option import OptionTableMeta
from writtenbookeditor.core.registry import add_adapter, add_exporter, add_formatter

__all__ = ["register_adapter", "register_formatter", "register_option_table"]


def register_formatter[T: Formatter](
    name: str,
    *,
    producted_features: Optional[list[str]] = None,
) -> Callable[[Type[T]], Type[T]]:
    """
    注册格式化器
    """

    def decorator(cls: Type[T]):
        options, sub_tables = get_option_table_info(cls)
        add_formatter(name, cls, options, sub_tables, producted_features or [])
        return cls

    return decorator


def register_adapter[T: Adapter](
    name: str,
    *,
    required_features: Optional[Collection[str]] = None,
    producted_features: Optional[Collection[str]] = None,
) -> Callable[[Type[T]], Type[T]]:
    """
    注册适配器
    """

    def decorator(cls: Type[T]):
        options, sub_tables = get_option_table_info(cls)

        add_adapter(name, cls, options, sub_tables, required_features or [], producted_features or [])
        return cls

    return decorator


def register_exporter[T: Exporter](
    name: str,
    *,
    required_features: Optional[Collection[str]] = None,
) -> Callable[[Type[T]], Type[T]]:
    """
    注册导出器
    """

    def decorator(cls: Type[T]):
        options, sub_tables = get_option_table_info(cls)

        add_exporter(name, cls, options, sub_tables, required_features or [])
        return cls

    return decorator


def register_option_table[T](name: str) -> Callable[[Type[T]], Type[T]]:
    """
    注册配置表
    """

    # 将配置表元数据保存到类属性中, 方便后续使用
    # 其实这个装饰器完全没有必要, 可以在 core.plugin.options:option 中获取配置表元数据
    # 但为了明确语义, 还是保留这个装饰器
    # 并且这个实现也可以避免重复获取配置表元数据, 略微提升性能.

    def decorator(cls: Type[T]) -> Type[T]:
        options, sub_tables = get_option_table_info(cls)
        meta = OptionTableMeta(name, cls, options, sub_tables)
        setattr(cls, "__option_meta__", meta)
        return cls

    return decorator
