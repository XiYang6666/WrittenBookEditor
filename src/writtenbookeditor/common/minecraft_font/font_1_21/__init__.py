from functools import cache

import numpy as np


from .space import get_char_space_width
from .default import get_char_default_bitmap_and_offset
from .unifont import get_char_unifont_bitmap
from ..types import CharInfo, FontConf
from ..constants import MISSING_FONT


@cache
def get_char_info(char: str, conf: FontConf) -> CharInfo:
    unifont = conf.unifont
    jp = conf.jp
    # space
    width = get_char_space_width(char)
    if width is not None:
        return CharInfo(np.zeros((16, width), dtype=np.bool), 2)
    # default
    if not unifont:
        result = get_char_default_bitmap_and_offset(char)
        if result is not None:
            bitmap, offset = result
            return CharInfo(bitmap, 2, offset)
    # unifont
    bitmap = get_char_unifont_bitmap(char, jp)
    if bitmap is not None:
        return CharInfo(bitmap, 1, -2)
    return MISSING_FONT
