from ..font import get_char_info


def calc_char_width(char: str, unicode: bool = False, jp: bool = False) -> int:
    char_info = get_char_info(char, unicode, jp)
    char_width = char_info.bitmap.shape[1] * char_info.scale
    if char != " ":  # 空格后不加间隔
        char_width += 2 - char_width % 2  # 字符间隔, 下一个字符起始位置恒为2的倍数
    return char_width
