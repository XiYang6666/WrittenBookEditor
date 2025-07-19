import json
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, cast

import numpy as np
from PIL import Image, ImageFont

from writtenbookeditor.plugins.lib_minecraft.font.types import (
    BaseGlyphProviderJson,
    BitmapGlyphProviderJson,
    FontProviderFileJson,
    Glyph,
    GlyphProvider,
    ProviderFilter,
    RawGlyphProvider,
    ReferenceGlyphProviderJson,
    SpaceGlyphProviderJson,
    TTFGlyphProviderJson,
    UnihexGlyphProviderSizeoverrideJson,
    UnihexProviderJson,
)
from writtenbookeditor.plugins.lib_minecraft.font.utils import as_glyph_provider, check_filter, trim_bitmap_margins


@dataclass
class FontContext:
    font_path: Path
    font_texture_path: Path
    loaded: dict[str, "ReferenceGlyphProvider"] = dict()

    def get_provider_path(self, id: str) -> Path:
        # 我为什么要 tmd 考虑minecraft 以外的命名空间?
        real_filename = id.removesuffix("minecraft:") + ".json"
        return self.font_path / real_filename

    def get_font_path(self, file: str) -> Path:
        real_filename = file.removesuffix("minecraft:")
        return self.font_path / real_filename

    def get_texture_path(self, file: str) -> Path:
        real_relative_path = Path(file.removesuffix("minecraft:")).relative_to("font/")
        return self.font_texture_path / real_relative_path

    def create_reference_provider(self, id: str) -> "ReferenceGlyphProvider":
        if id in self.loaded:
            return self.loaded[id]
        provider = ReferenceGlyphProvider(self, id=id)
        self.loaded[id] = provider
        return provider


class BitmapGlyphProvider(RawGlyphProvider):
    def __init__(
        self,
        context: FontContext,
        *,
        file: str,
        chars: list[str],
        height: Optional[int],
        ascent: int,
    ):
        self.chars = chars
        self.height = height if height is not None else 8
        self.ascent = ascent
        # preload
        bitmap_path = context.get_texture_path(file)
        self.bitmap = np.array(Image.open(bitmap_path).convert("RGBA").getchannel("A")) > 0
        assert self.chars, "chars is empty"
        line_char_count = len(self.chars[0])
        assert self.bitmap.shape[1] % line_char_count == 0, "bitmap width is not divisible by char width"
        self.width = self.bitmap.shape[1] // line_char_count

    def find_char(self, char: str) -> Optional[tuple[int, int]]:
        for y, line in enumerate(self.chars):
            x = line.find(char)
            if x != -1:
                return x, y
        else:
            return None

    def __call__(self, char: str) -> Optional[Glyph]:
        char_pos = self.find_char(char)
        if not char_pos:
            return None
        x, y = char_pos
        left = x * self.width
        upper = y * self.height
        right = left + self.width
        lower = right + self.height
        cropped = self.bitmap[upper:lower, left:right]
        return Glyph(char, cropped, self.ascent)


class ReferenceGlyphProvider(GlyphProvider):
    def __init__(
        self,
        context: FontContext,
        *,
        id: str,
    ):
        file_path = context.get_provider_path(id)
        data: FontProviderFileJson = json.loads(file_path.read_text())
        self.providers: list[GlyphProvider] = [self.load_provider(context, provider_json) for provider_json in data["providers"]]

    def load_provider(self, context: FontContext, provider_json: BaseGlyphProviderJson) -> GlyphProvider:
        filter_json = provider_json.get("filter", {})
        filter = ProviderFilter(jp=filter_json.get("jp", None), unifont=filter_json.get("unifont", None))
        if provider_json["type"] == "bitmap":
            provider_json = cast(BitmapGlyphProviderJson, provider_json)
            provider = BitmapGlyphProvider(
                context,
                file=provider_json["file"],
                chars=provider_json["chars"],
                height=provider_json.get("height"),
                ascent=provider_json["ascent"],
            )
            return as_glyph_provider(filter)(provider)
        elif provider_json["type"] == "reference":
            provider_json = cast(ReferenceGlyphProviderJson, provider_json)
            provider = context.create_reference_provider(provider_json["id"])
            return check_filter(filter)(provider)
        elif provider_json["type"] == "space":
            provider_json = cast(SpaceGlyphProviderJson, provider_json)
            provider = SpaceGlyphProvider(advances=provider_json["advances"])
            return as_glyph_provider(filter)(provider)
        elif provider_json["type"] == "ttf":
            provider_json = cast(TTFGlyphProviderJson, provider_json)
            provider = TTFGlyphProvider(
                context,
                file=provider_json["file"],
                oversample=provider_json.get("oversample"),
                size=provider_json.get("size"),
                shift=provider_json.get("shift"),
                skip=provider_json.get("skip"),
            )
            return as_glyph_provider(filter)(provider)
        elif provider_json["type"] == "unihex":
            provider_json = cast(UnihexProviderJson, provider_json)
            provider = UnihexGlyphProvider(
                context,
                hex_file=provider_json["hex_file"],
                size_overrides=provider_json.get("size_overrides"),
            )
            return as_glyph_provider(filter)(provider)
        else:
            raise ValueError(f"unknown provider type: {provider_json['type']}")

    def __call__(self, char: str, filter: ProviderFilter) -> Optional[Glyph]:
        return next((glyph for provider in self.providers if (glyph := provider(char, filter)) is not None), None)


class SpaceGlyphProvider(RawGlyphProvider):
    def __init__(self, *, advances: dict[str, int]):
        self.advances = advances

    def __call__(self, char: str) -> Optional[Glyph]:
        width = self.advances.get(char)
        if width is None:
            return None
        return Glyph(char, np.zeros((1, width), dtype=np.bool_), 0)


class TTFGlyphProvider(RawGlyphProvider):
    """
    注: 懒得写了, 让 AI 写了半天每一个能用的...
    """

    def __init__(
        self,
        context: FontContext,
        *,
        file: str,
        oversample: Optional[float],
        size: Optional[float],
        shift: Optional[list[float] | tuple[float, float]],
        skip: Optional[str | list[str]],
    ):
        self.oversample = oversample if oversample is not None else 1.0
        self.size = size if size is not None else 11.0
        self.shift = shift if shift is not None else [0.0, 0.0]
        shift_x, shift_y = self.shift
        assert -512 <= shift_x <= 512 and -512 <= shift_y <= 512, "shift must be in range [-512, 512]"
        skip = skip if skip is not None else ""
        self.skip = set(skip) if isinstance(skip, str) else set("".join(skip))
        # preload
        ttf_path = context.get_font_path(file)
        self.font = ImageFont.truetype(str(ttf_path), int(self.size * self.oversample))

    def __call__(self, char: str) -> Optional[Glyph]:
        if char in self.skip:
            return None
        raise NotImplementedError("我懒得写")  # 欢迎 pr (大雾)


class UnihexGlyphProvider(RawGlyphProvider):
    def __init__(
        self,
        context: FontContext,
        *,
        hex_file: str,
        size_overrides: Optional[list[UnihexGlyphProviderSizeoverrideJson]],
    ):
        self.size_overrides = size_overrides if size_overrides is not None else []
        self.mapping: dict[str, Glyph] = {}
        hex_zip_path = context.get_font_path(hex_file)

        for line in self.read_hex_data(hex_zip_path):
            char_hex, bitmap_hex = line.split(":")
            char_code = int(char_hex, 16)
            char = chr(char_code)

            bitmap_data = bytes.fromhex(bitmap_hex)
            bits = np.unpackbits(np.frombuffer(bitmap_data, dtype=np.uint8))
            width = bits.size // 16
            bitmap = bits.reshape((16, width)).astype(np.bool_)

            for override in self.size_overrides:
                if override["from"] <= ord(char) <= override["to"]:
                    bitmap = bitmap[:, override["left"] : override["right"]]
                    break
            else:
                bitmap = trim_bitmap_margins(bitmap)

            self.mapping[char] = Glyph(char, bitmap, -2)

    @staticmethod
    def read_hex_data(hex_zip_path: Path):
        with zipfile.ZipFile(hex_zip_path, "r") as zip_ref:
            hex_files = [name for name in zip_ref.namelist() if name.endswith(".hex")]
            assert len(hex_files) == 1, "hex file must contain exactly one file"
            with zip_ref.open(hex_files[0], "r") as f:
                yield from (line.decode() for line in f)

    def __call__(self, char: str) -> Optional[Glyph]:
        return self.mapping.get(char)


def load_provider(context: FontContext, id: str):
    """
    加载字形提供器

    对于同一种字形的不同文件应使用同一个 context 以保证缓存的正确性.
    """
    # “无论被包含多少次，该类型字体提供器也只会加载一次.”
    # [wiki](https://zh.minecraft.wiki/w/自定义字体#reference)
    context.create_reference_provider(id)
