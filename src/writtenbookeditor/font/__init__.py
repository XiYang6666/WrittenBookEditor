from dataclasses import dataclass

import numpy as np

from .space import get_char_space_width
from .default import get_char_default_bitmap_and_offset
from .unifont import get_char_unifont_bitmap


@dataclass
class CharInfo:
    bitmap: np.ndarray
    scale: int = 1
    offset: int = 0


missing_glyph = CharInfo(
    np.array(
        [
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1],
        ]
    ),
    2,
    0,
)


def calc_char_info(char: str, unicode: bool = False, jp: bool = False) -> CharInfo:
    # space
    width = get_char_space_width(char)
    if width is not None:
        return CharInfo(np.zeros((16, width)), 2)
    # default
    if not unicode:
        result = get_char_default_bitmap_and_offset(char)
        if result is not None:
            bitmap, offset = result
            return CharInfo(bitmap, 2, offset)
    # unifont
    bitmap = get_char_unifont_bitmap(char, jp)
    if bitmap is not None:
        return CharInfo(bitmap, 1, -2)
    return missing_glyph


char_info_cache: dict[tuple[str, bool, bool], CharInfo] = {}


def get_char_info(char: str, unicode: bool = False, jp: bool = False):
    key = (char, unicode, jp)
    if key in char_info_cache:
        return char_info_cache[key]
    result = calc_char_info(char, unicode, jp)
    char_info_cache[key] = result
    return result
