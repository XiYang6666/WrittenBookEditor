from dataclasses import dataclass
from typing import Annotated, Literal, NotRequired, Optional, Protocol, TypedDict

import numpy as np
import numpy.typing as npt

type Bitmap = Annotated[npt.NDArray[np.bool_], Literal["N", "N"]]


@dataclass(frozen=True)
class Glyph:
    char: str
    bitmap: Bitmap
    ascent: int


class RawGlyphProvider(Protocol):
    def __call__(self, char: str) -> Optional[Glyph]: ...


class GlyphProvider(Protocol):
    def __call__(self, char: str, filter: "ProviderFilter") -> Optional[Glyph]: ...


@dataclass(frozen=True)
class ProviderFilter:
    jp: Optional[bool] = None
    unifont: Optional[bool] = None

    def match(self, other: "ProviderFilter"):
        assert other.jp is not None and other.unifont is not None
        if self.jp is not None and self.jp != other.jp:
            return False
        if self.unifont is not None and self.unifont != other.unifont:
            return False
        return True

    @classmethod
    def empty(cls):
        return cls(jp=None, unifont=None)

    @classmethod
    def default(cls):
        return cls(jp=False, unifont=False)


class ProviderFilterJson(TypedDict):
    jp: NotRequired[bool]
    unifont: NotRequired[bool]


class BaseGlyphProviderJson(TypedDict):
    type: Literal["bitmap", "reference", "space", "ttf", "unihex"]
    filter: NotRequired[ProviderFilterJson]


class BitmapGlyphProviderJson(BaseGlyphProviderJson):
    file: str
    chars: list[str]
    height: NotRequired[int]
    ascent: int


class ReferenceGlyphProviderJson(BaseGlyphProviderJson):
    id: str


class SpaceGlyphProviderJson(BaseGlyphProviderJson):
    advances: dict[str, int]


class TTFGlyphProviderJson(BaseGlyphProviderJson):
    file: str
    oversample: NotRequired[float]
    size: NotRequired[float]
    shift: NotRequired[list[float] | tuple[float, float]]  # [float, float]
    skip: NotRequired[str | list[str]]


UnihexGlyphProviderSizeoverrideJson = TypedDict(
    "UnihexGlyphProviderSizeoverrideJson", {"from": str, "to": str, "left": int, "right": int}
)


class UnihexGlyphProviderJson(BaseGlyphProviderJson):
    hex_file: str
    size_overrides: NotRequired[list[UnihexGlyphProviderSizeoverrideJson]]


class LegcyUnicodeGlyphProviderJson(BaseGlyphProviderJson):
    sizes: str
    template: str


class FontProviderFileJson(TypedDict):
    providers: list[BaseGlyphProviderJson]
