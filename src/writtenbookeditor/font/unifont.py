from typing import Optional, TypedDict, Any
import json

import numpy as np

from .util import calc_bitmap_side


unifont_map: dict[str, np.ndarray] = {}
unifont_jp_map: dict[str, np.ndarray] = {}

with open("./data/unifont/unifont_all_no_pua-15.1.05.hex") as f:
    for line in f.readlines():
        [char_hex, bitmap_hex] = line.split(":")
        char = chr(int(char_hex, 16))
        bitmap_data = bytes.fromhex(bitmap_hex)
        bitmap_array = np.unpackbits(np.frombuffer(bitmap_data, dtype=np.uint8))
        bitmap_array.resize((16, len(bitmap_array) // 16))
        unifont_map[char] = bitmap_array  # type: ignore


with open("./data/unifont_jp/unifont_jp_patch-15.1.05.hex") as f:
    unifont_jp_data = f.readlines()
    for line in unifont_jp_data:
        [char_hex, bitmap_hex] = line.split(":")
        char = chr(int(char_hex, 16))
        bitmap_data = bytes.fromhex(bitmap_hex)
        bitmap_array = np.unpackbits(np.frombuffer(bitmap_data, dtype=np.uint8))
        bitmap_array.resize((16, len(bitmap_array) // 16))
        unifont_jp_map[char] = bitmap_array

with open("./data/unifont_force_width_chars.json") as f:
    unifont_force_width_chars: list[dict[str, Any]] = json.load(f)

with open("./data/unifont_jp_force_width_chars.json") as f:
    unifont_jp_force_width_chars: list[dict[str, Any]] = json.load(f)


def get_char_unifont_bitmap(char: str, jp: bool = False) -> Optional[np.ndarray]:
    bitmap = unifont_jp_map.get(char) if jp else None
    bitmap = bitmap if bitmap is not None else unifont_map.get(char)
    if bitmap is None:
        return None
    left: Optional[int] = None
    right: Optional[int] = None
    char_ord = ord(char)
    if jp:
        for size_override in unifont_jp_force_width_chars:
            from_char = size_override["from"]
            to_char = size_override["to"]
            from_ord = ord(from_char)
            to_ord = ord(to_char)
            if from_ord <= char_ord <= to_ord:
                left = size_override["left"]
                right = size_override["right"]
                break
    for size_override in unifont_force_width_chars:
        from_char = size_override["from"]
        to_char = size_override["to"]
        from_ord = ord(from_char)
        to_ord = ord(to_char)
        if from_ord <= char_ord <= to_ord:
            left = size_override["left"]
            right = size_override["right"]
            break
    if left is None or right is None:
        left, right = calc_bitmap_side(bitmap)
    return bitmap[:, left : right + 1]
