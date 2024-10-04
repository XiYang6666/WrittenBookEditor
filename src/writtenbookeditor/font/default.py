from typing import Optional
import json

import numpy as np
from PIL import Image

from .util import calc_bitmap_side


nonlatin_european_font_img = Image.open("./data/textures/nonlatin_european.png").convert("RGBA")
accented_font_img = Image.open("./data/textures/accented.png").convert("RGBA")
ascii_font_img = Image.open("./data/textures/ascii.png").convert("RGBA")

with open("./data/default_chars.json") as f:
    default_chars = json.load(f)


nonlatin_european_font_chars: list[str] = default_chars["nonlatin_european"]
accented_font_chars: list[str] = default_chars["accented"]
ascii_font_chars: list[str] = default_chars["ascii"]


def get_char_default_bitmap_and_offset(char: str) -> Optional[tuple[np.ndarray, int]]:
    for img, chars, [width, height, ascent] in [
        (nonlatin_european_font_img, nonlatin_european_font_chars, (8, 8, 7)),
        (accented_font_img, accented_font_chars, (9, 12, 10)),
        (ascii_font_img, ascii_font_chars, (8, 8, 7)),
    ]:
        for y, line in enumerate(chars):
            if char in line:
                x = line.find(char)
                break
        else:
            continue
        bitmap_img = img.crop((x * width, y * height, x * width + width, y * height + height))
        bitmap_alpha_array = np.array(bitmap_img)[:, :, 3]
        bitmap_array = np.where(bitmap_alpha_array > 0, 1, 0)
        left, right = calc_bitmap_side(bitmap_array)
        result_array = bitmap_array[:, left : right + 1]
        return result_array, ascent - height
    return None
