from typing import Any, Callable, Mapping, Sequence, Type, Optional


from .interface.adapter import Adapter
from .interface.formatter import Formatter
from .types import AdapterMeta, FormatterMeta, OptionConfigMeta
from .injector import get_option_meta, inject_options

adapters: dict[str, AdapterMeta] = {}
formatters: dict[str, FormatterMeta] = {}


def add_adapter(
    name: str,
    creater: Callable[[Mapping], Adapter],
    features: Optional[Sequence[str]] = None,
    options: Optional[OptionConfigMeta] = None,
) -> AdapterMeta:
    meta = AdapterMeta(name, creater, features or [], options)
    adapters[name] = meta
    return meta


def add_formatter(
    name: str,
    creater: Callable[[Mapping], Formatter],
    features: Optional[Sequence[str]] = None,
    options: Optional[OptionConfigMeta] = None,
) -> FormatterMeta:
    meta = FormatterMeta(name, creater, features or [], options)
    formatters[name] = meta
    return meta


def register_adapter[T: Adapter](
    name: str,
    *,
    features: Optional[list[str]] = None,
) -> Callable[[Type[T]], Type[T]]:
    """
    注册适配器
    """

    def decorator(cls: Type[T]):
        option_meta = get_option_meta(cls)

        def creater(config: Mapping[str, Any]):
            instance = cls()
            return inject_options(instance, option_meta, config)

        add_adapter(name, creater, features)
        return cls

    return decorator


def register_formatter[T: Formatter](
    name: str,
    *,
    features: Optional[list[str]] = None,
) -> Callable[[Type[T]], Type[T]]:
    """
    注册格式器
    """

    def decorator(cls: Type[T]):
        option_meta = get_option_meta(cls)

        def creater(config: Mapping[str, Any]):
            instance = cls()
            return inject_options(instance, option_meta, config)

        add_formatter(name, creater, features)
        return cls

    return decorator


def register_option_table[T](name: str) -> Callable[[Type[T]], Type[T]]:
    """
    注册配置表
    """

    def decorator(cls: Type[T]) -> Type[T]:
        meta = get_option_meta(cls, name)
        setattr(cls, "__option_meta__", meta)
        return cls

    return decorator
