"""
调试工具模块
"""

from typing import Callable, Optional

from ..config import get_core_config


def run_while_debugging(func: Callable):
    if get_core_config().debug:
        func()


def assert_while_debugging(condition: bool | Callable, message: Optional[str] = None):
    if get_core_config().debug:
        value = condition() if callable(condition) else condition
        if message is None:
            assert value
        else:
            assert value, message
