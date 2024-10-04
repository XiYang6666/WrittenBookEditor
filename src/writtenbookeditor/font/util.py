import numpy as np


def calc_bitmap_side(bitmap: np.ndarray) -> tuple[int, int]:
    has_point: set[int] = set()
    for x, col in enumerate(bitmap.T):
        if np.any(col):
            has_point.add(x)
    if len(has_point) == 0:
        return 0, 15
    return min(has_point), max(has_point)
