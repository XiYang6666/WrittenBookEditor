"""
动态插件加载器
"""

import importlib
import importlib.util
import sys
from pathlib import Path
from types import ModuleType

from writtenbookeditor.core.config import get_core_config
from writtenbookeditor.core.constants import PROJECR_NAME
from writtenbookeditor.core.logger import loader_logger as logger


def load_builtin_plugins():
    """
    加载内置插件
    """
    load_plugins(get_inernal_plugins_path())


def load_plugin_dirs():
    """
    加载插件目录
    """
    for plugin_dir in get_core_config().plugin_dirs:
        load_plugins(plugin_dir)


def load_plugins(path: str | Path):
    """
    加载指定路径下的插件
    """

    path = Path(path)
    create_namespace()
    sys.modules[get_core_config().plugin_namespace].__path__.insert(0, str(path.absolute()))

    logger.info(f"Loading plugins from {path}.")
    if not path.is_dir():
        logger.warning(f"Plugins path {path} does not exist or is not a directory.")
        return
    sys.path.insert(0, str(path.absolute()))
    for plugin_path in path.iterdir():
        if plugin_path.name.startswith("__"):
            continue
        elif plugin_path.is_dir() and (plugin_path / "__init__.py").is_file():
            load_module(plugin_path.name, plugin_path / "__init__.py")
        elif plugin_path.is_file() and plugin_path.suffix == ".py":
            load_module(plugin_path.stem, plugin_path)
    if sys.path[0] == str(path.absolute()):
        sys.path.pop(0)


def create_namespace():
    """
    创建命名空间
    """
    namespace = get_core_config().plugin_namespace
    if namespace in sys.modules:
        module = sys.modules[namespace]
        module.__path__ = list(module.__path__)
        logger.debug("Plugin namespace already exists and loaded.")
        return
    try:
        module = importlib.import_module(namespace)
        module.__path__ = list(module.__path__)
        logger.debug("Plugin namespace already exists but not loaded, loading.")
    except ImportError:
        module = ModuleType(namespace)
        module.__path__ = list(module.__path__)
        sys.modules[namespace] = module
        logger.debug("Created plugin namespace.")


def get_inernal_plugins_path():
    if getattr(sys, "frozen", False):
        # 运行于 PyInstaller 打包后的 exe 文件
        base_path = sys._MEIPASS  # type: ignore
        return Path(base_path).absolute() / PROJECR_NAME / "plugins"
    else:
        # 运行于 Python 解释器
        return Path(__file__).absolute().parent.parent / "plugins"


def format_plugin_path(
    path: Path,
) -> str:
    parent_path = path.parent
    if path.name == "__init__.py":
        parent_path = parent_path.parent
    if parent_path == get_inernal_plugins_path():
        return "built-in plugins"
    else:
        return str(path)


def load_module(module_name: str, file_path: Path):
    full_module_name = f"{get_core_config().plugin_namespace}.{module_name}"
    if full_module_name in sys.modules:
        logger.debug(f"Plugin module already loaded: {full_module_name}, skipping.")
        logger.success(f"Successfully loaded plugin {module_name} from {format_plugin_path(file_path)} plugins.")
        return
    try:
        spec = importlib.util.spec_from_file_location(full_module_name, file_path)
        if spec is None:
            logger.error(f"Failed to create spec for {file_path}.")
            return
        assert spec.loader is not None, "spec.loader is None"
        module = importlib.util.module_from_spec(spec)
        sys.modules[full_module_name] = module
        spec.loader.exec_module(module)
        logger.success(f"Successfully loaded plugin {module_name} from {format_plugin_path(file_path)}.")
    except Exception as e:
        logger.exception(f"Failed to load plugin {module_name} from {format_plugin_path(file_path)}: {e}")
