from typing import Any, TypeGuard

import numpy as np

from .types import Bitmap


def is_bitmap(bitmap: Any) -> TypeGuard[Bitmap]:
    return True
    return isinstance(bitmap, np.ndarray) and bitmap.dtype == np.bool and len(bitmap.shape) == 2


def calc_bitmap_side(bitmap: Bitmap) -> tuple[int, int]:
    has_point: set[int] = set()
    for x, col in enumerate(bitmap.T):
        if np.any(col):
            has_point.add(x)
    if len(has_point) == 0:
        return 0, 15
    return min(has_point), max(has_point)
