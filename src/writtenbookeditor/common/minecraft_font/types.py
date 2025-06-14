from dataclasses import dataclass
from typing import Callable

import numpy as np

type Bitmap = np.ndarray[np._2D, np.dtype[np.bool]]


@dataclass(frozen=True)
class FontConf:
    unifont: bool
    jp: bool


@dataclass(frozen=True)
class CharInfo:
    bitmap: Bitmap
    scale: int = 1
    offset: int = 0


type Font = Callable[[str, FontConf], CharInfo]
