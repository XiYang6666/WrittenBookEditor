import sys
from json import load

from loguru import logger

from writtenbookeditor.core.config import get_core_config


def load_logger():
    logger.remove()
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<blue>{extra[module]:<6}</blue> | "
        "<level>{level: <8}</level> | "
        # "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )
    logger.add(sys.stdout, colorize=True, format=log_format, level="DEBUG" if get_core_config().debug else "INFO")


def get_logger(module_name: str):
    return logger.bind(module=module_name)


load_logger()
core_logger = get_logger("core")
loader_logger = get_logger("loader")
