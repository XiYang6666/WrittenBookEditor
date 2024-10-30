import re
from typing import Optional

predefined_colors = {
    "black": "#000000",
    "dark_blue": "#0000AA",
    "dark_green": "#00AA00",
    "dark_aqua": "#00AAAA",
    "dark_red": "#AA0000",
    "dark_purple": "#AA00AA",
    "gold": "#FFAA00",
    "gray": "#AAAAAA",
    "dark_gray": "#555555",
    "blue": "#5555FF",
    "green": "#55FF55",
    "aqua": "#55FFFF",
    "red": "#FF5555",
    "light_purple": "#FF55FF",
    "yellow": "#FFFF55",
    "white": "#FFFFFF",
}


def validate_color(color: str) -> bool:
    return bool(color in predefined_colors or re.match(r"#[0-9a-fA-F]{6}", color))


def hsl_to_rgb(hue: float, saturation: float, value: float) -> tuple[int, int, int]:
    h = hue * 360
    s = saturation
    v = value
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c
    if 0 <= h < 60:
        r, g, b = c, x, 0
    elif 60 <= h < 120:
        r, g, b = x, c, 0
    elif 120 <= h < 180:
        r, g, b = 0, c, x
    elif 180 <= h < 240:
        r, g, b = 0, x, c
    elif 240 <= h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x
    return (int((r + m) * 255), int((g + m) * 255), int((b + m) * 255))


def rgb_to_hex(r: int, g: int, b: int) -> str:
    return f"#{r:02x}{g:02x}{b:02x}"


def hex_to_rgb(hex_code: str) -> Optional[tuple[int, int, int]]:
    if not hex_code.startswith("#") or len(hex_code) != 7:
        return None
    hex_code = hex_code.removeprefix("#")
    r, g, b = int(hex_code[:2], 16), int(hex_code[2:4], 16), int(hex_code[4:], 16)
    return (r, g, b)


def parse_color(color: str) -> Optional[tuple[int, int, int]]:
    return hex_to_rgb(predefined_colors.get(color, color))


def interpolate_color(color1: tuple[int, int, int], color2: tuple[int, int, int], factor: float) -> tuple[int, int, int]:
    r = int(color1[0] + (color2[0] - color1[0]) * factor)
    g = int(color1[1] + (color2[1] - color1[1]) * factor)
    b = int(color1[2] + (color2[2] - color1[2]) * factor)
    return (r, g, b)


def interpolate_colors(colors: list[tuple[int, int, int]], ratio: float) -> tuple[int, int, int]:
    segment_count = len(colors) - 1
    scaled_ratio = ratio * segment_count
    start_index = int(scaled_ratio)
    end_index = min(start_index + 1, segment_count)

    color_start = colors[start_index]
    color_end = colors[end_index]

    local_ratio = scaled_ratio - start_index
    return interpolate_color(color_start, color_end, local_ratio)
