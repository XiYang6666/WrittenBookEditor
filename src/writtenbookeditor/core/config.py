"""
核心配置
"""

from dataclasses import dataclass


@dataclass
class CoreConfig:
    debug: bool = False  # 调试模式下会校验许多数据, 性能严重下降.


config = CoreConfig()


def get_core_config():
    return config


def update_core_config(new_config: CoreConfig):
    global config
    config = new_config
