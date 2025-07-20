import sys
from functools import cache
from pathlib import Path

import pytest

if __name__ == "__main__":
    sys.path.insert(0, "./src")

from writtenbookeditor.plugins.lib_minecraft.font.genernal_loader import FontContext
from writtenbookeditor.plugins.lib_minecraft.font.types import ProviderFilter


def test_provider():
    context = FontContext([Path("./data/test/font/")], [Path("./data/test/font/textures/")])
    provider = context.create_reference_provider("default")
    provider = cache(provider)
    if __name__ == "__main__":
        str = "Hello, world! 日々私たちが過ごしている日常は、実は、奇跡の連続なのかもしれない。"
    else:
        str = Path("./data/test/text/从百草园到三味书屋.txt").read_text("utf-8")
        str += Path("./data/test/text/romeo_and_juliet.txt").read_text("utf-8")
    for char in str:
        glyph = provider(char, ProviderFilter.default())
        assert glyph is not None


VERSIONS = [
    "1.6.2",
    "1.7.3",
    "1.9",
    "1.13",
    "1.16",
    "1.20",
    "1.20.3",
    "1.20.5",
    "1.21",
    "1.21.4",
    "1.21.6",
]


@pytest.mark.parametrize("version_string", VERSIONS)
def test_version_providers(version_string: str):
    print(f"Testing {version_string}")
    version = tuple(int(j) for j in version_string.split("."))
    i = VERSIONS.index(version_string)
    font_paths = [Path(f"./data/font/minecraft_{p}") for p in reversed(VERSIONS[: i + 1])]
    texture_paths = [p / "textures" for p in font_paths]
    context = FontContext(font_paths, texture_paths)
    if version < (1, 20, 5):
        provider = cache(context.create_reference_provider("simulated"))
    else:
        provider = cache(context.create_reference_provider("default"))
    if __name__ == "__main__":
        str = "Hello, world! 日々私たちが過ごしている日常は、実は、奇跡の連続なのかもしれない。"
    else:
        str = Path("./data/test/text/从百草园到三味书屋.txt").read_text("utf-8")
        str += Path("./data/test/text/romeo_and_juliet.txt").read_text("utf-8")
    for char in str:
        glyph = provider(char, ProviderFilter.default())
        assert glyph is not None
    for char in str:
        glyph = provider(char, ProviderFilter(False, True))
        assert glyph is not None


if __name__ == "__main__":
    test_provider()
    for version in VERSIONS:
        test_version_providers(version)
