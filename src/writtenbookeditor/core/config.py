"""
核心配置
"""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class CoreConfig:
    # debug mode
    debug: bool = False  # 调试模式下会校验许多数据, 性能严重下降.
    # plugins
    load_internal_plugins: bool = True  # 是否加载内置插件.
    plugin_namespace: str = "writtenbookeditor.plugins"  # 插件命名空间.
    plugin_dirs: list[Path] = field(default_factory=lambda: [Path("./plugins")])  # 插件目录列表.


# config = None
config = CoreConfig()


def get_core_config():
    assert config is not None, "core config not initialized, please call update_core_config() first."
    return config


def update_core_config(new_config: CoreConfig):
    global config
    config = new_config
