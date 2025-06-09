import numpy as np

from .types import Bitmap, CharInfo

MISSING_FONT_BITMAP: Bitmap = np.array(
    [
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1],
    ],
    dtype=np.bool,
)  # type: ignore

MISSING_FONT = CharInfo(
    MISSING_FONT_BITMAP,
    2,
    0,
)
