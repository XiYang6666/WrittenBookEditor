from typing import Sequence


def param(*args, **kwargs) -> tuple[Sequence, dict]:
    return args, kwargs
