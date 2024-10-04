from typing import Optional


def get_char_space_width(char: str) -> Optional[int]:
    if char == " ":
        return 4
    if char == "\u200c":
        return 0
    else:
        return None
