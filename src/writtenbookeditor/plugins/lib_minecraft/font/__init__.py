"""
Minecraft 字体
"""

from functools import cache
from pathlib import Path
from typing import Optional

from writtenbookeditor.plugins.lib_minecraft.font.loader import FontContext
from writtenbookeditor.plugins.lib_minecraft.font.types import GlyphProvider

__all__ = [
    "VERSIONS",
    "get_font_by_version",
]

VERSIONS = [
    "1.6.2",
    "1.7.3",
    "1.9",
    "1.13",
    "1.16",
    "1.20",
    "1.20.3",
    "1.20.5",
    "1.21",
    "1.21.4",
    "1.21.6",
]


@cache
def get_font_by_version(version: str) -> Optional[GlyphProvider]:
    """
    获取 Minecraft 字体
    """
    version_tuple = tuple(map(int, version.split(".")))
    for v in VERSIONS:
        if version_tuple < tuple(map(int, v.split("."))):
            continue
        idx = VERSIONS.index(v)
        font_paths = [Path(f"./data/font/minecraft_{p}/") for p in reversed(VERSIONS[: idx + 1])]
        texture_paths = [p / "textures" for p in font_paths]
        context = FontContext(font_paths, texture_paths)
        if version_tuple < (1, 20, 5):
            return context.create_reference_provider("simulated")
        else:
            return context.create_reference_provider("default")
    return None
