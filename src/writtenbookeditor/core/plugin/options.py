"""
配置字段

包装 core.interface.option 中的配置字段, 使编写插件时类型检查不报错.
"""

from typing import Any, Literal, Optional, Type, overload

from writtenbookeditor.core.interface.option import (BoolOptionField, ChoiceOptionField, FloatOptionField, IntOptionField,
                                                     StringOptionField)

# 注: 这里返回值都是为了骗过类型检查的假类型
# 实际上返回的都是 BaseOption 或 OptionConfigMeta[T] (


@overload
def option(
    type: Literal["str"],
    default: str = "",
    *,
    hide: bool = False,
) -> str: ...


@overload
def option(
    type: Literal["int"],
    default: int = 0,
    *,
    hide: bool = False,
    max_value: Optional[int] = None,
    min_value: Optional[int] = None,
) -> int: ...


@overload
def option(
    type: Literal["float"],
    default: float = 0.0,
    *,
    hide: bool = False,
    max_value: Optional[float] = None,
    min_value: Optional[float] = None,
) -> float: ...


@overload
def option(
    type: Literal["bool"],
    default: bool = False,
    *,
    hide: bool = False,
) -> bool: ...


@overload
def option(
    type: Literal["choice"],
    choices: list[str],
    default: Optional[str] = None,
    *,
    editable: bool = False,
    hide: bool = False,
) -> str: ...


@overload
def option[T](
    type: Literal["table"],
    table: Type[T],
) -> T: ...


def option(type: str | type, *args, **kwargs) -> Any:
    def get_arg(name: str, pos: Optional[int] = None) -> Any:
        if pos is not None and pos < len(args):
            return args[pos]
        else:
            return kwargs.get(name, None)

    if type == "str" or type is str:
        return StringOptionField(
            default=get_arg("default", 0),
            hide=get_arg("hide"),
        )
    elif type == "int" or type is int:
        return IntOptionField(
            default=get_arg("default", 0),
            hide=get_arg("hide"),
            max_value=get_arg("max_value"),
            min_value=get_arg("min_value"),
        )
    elif type == "float" or type is float:
        return FloatOptionField(
            default=get_arg("default", 0),
            hide=get_arg("hide"),
            max_value=get_arg("max_value"),
            min_value=get_arg("min_value"),
        )
    elif type == "bool" or type is bool:
        return BoolOptionField(
            default=get_arg("default", 0),
            hide=get_arg("hide"),
        )
    elif type == "choice":
        return ChoiceOptionField(
            choices=get_arg("choices", 0),
            default=get_arg("default", 1),
            editable=get_arg("editable"),
            hide=get_arg("hide"),
        )
    elif type == "table":
        meta = getattr(get_arg("table", 0), "__option_meta__", None)
        assert meta is not None, f"Unregisted option table: {get_arg('table', 0).__name__}"
        return meta
    else:
        assert False, f"Invalid option type: {type}"
