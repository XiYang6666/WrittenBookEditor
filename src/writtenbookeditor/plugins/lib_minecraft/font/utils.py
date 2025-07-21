from pathlib import Path
from typing import Sequence

import numpy as np

from .types import Bitmap, GlyphProvider, ProviderFilter, RawGlyphProvider

__all__ = [
    "calc_bitmap_margins",
    "trim_bitmap_margins",
    "view_bitmap",
    "print_bitmap",
    "get_resource_by_paths",
    "as_glyph_provider",
    "check_filter",
]


def calc_bitmap_margins(bitmap: Bitmap) -> tuple[int, int]:
    col_mask = np.any(bitmap, axis=0)
    if not np.any(col_mask):
        return 0, bitmap.shape[1] - 1
    left = int(np.argmax(col_mask))
    right = int(len(col_mask) - np.argmax(col_mask[::-1]) - 1)
    return left, right


def trim_bitmap_margins(bitmap: Bitmap) -> Bitmap:
    left, right = calc_bitmap_margins(bitmap)
    return bitmap[:, left : right + 1]


def view_bitmap(bitmap: Bitmap):
    """
    将 2D 位图转换为可在控制台中显示的字符串
    """
    rows = bitmap.shape[0]
    cols = bitmap.shape[1]
    result = ""
    for y in range(rows):
        for x in range(cols):
            if bitmap[y, x]:
                result += "██"
            else:
                result += "  "
        result += "\n"
    return result


def print_bitmap(bitmap: Bitmap):
    """
    将 2D 位图输出到控制台
    """
    print("┌─", end="")
    print("┬─" * (bitmap.shape[1] - 1), end="")
    print("┐")
    print(view_bitmap(bitmap))


def get_resource_by_paths(resource_paths: Sequence[str | Path], file: str | Path):
    assert not Path(file).is_absolute(), "file must be a relative path"
    for path in resource_paths:
        filepath = Path(path) / file
        if filepath.exists():
            return filepath
    raise FileNotFoundError(f"Cannot find {file} in {resource_paths}")


def as_glyph_provider(request_filter: ProviderFilter):
    def decorator(provider: RawGlyphProvider) -> GlyphProvider:
        def wrapper(char: str, filter: ProviderFilter):
            if not request_filter.match(filter):
                return None

            return provider(char)

        return wrapper

    return decorator


def check_filter(request_filter: ProviderFilter):
    def decorator(provider: GlyphProvider) -> GlyphProvider:
        def wrapper(char: str, filter: ProviderFilter):
            if not request_filter.match(filter):
                return None

            return provider(char, filter)

        return wrapper

    return decorator
