"""
Minecraft 字体处理
"""

from typing import Mapping

from .font_1_21 import get_char_info as get_char_info_1_21
from .types import Font

all_fonts: Mapping[str, Font] = {"1.21": get_char_info_1_21}
