from functools import wraps
from typing import Callable, Concatenate, Sequence
from weakref import WeakKeyDictionary


def param(*args, **kwargs) -> tuple[Sequence, dict]:
    return args, kwargs


def instance_method_cache[T, **P, R](func: Callable[Concatenate[T, P], R]) -> Callable[Concatenate[T, P], R]:
    """
    缓存实例方法的装饰器.

    示例必须支持弱引用.
    """
    cache: WeakKeyDictionary[T, dict[tuple, R]] = WeakKeyDictionary()

    @wraps(func)
    def wrapper(obj: T, *args: P.args, **kwargs: P.kwargs) -> R:
        obj_cache = cache.setdefault(obj, {})
        key = (args, frozenset(kwargs.items()))
        if key in obj_cache:
            return obj_cache[key]
        result = func(obj, *args, **kwargs)
        obj_cache[key] = result
        return result

    return wrapper
