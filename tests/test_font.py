import sys
from functools import cache
from pathlib import Path

if __name__ == "__main__":
    sys.path.insert(0, "./src")

from writtenbookeditor.plugins.lib_minecraft.font.genernal_loader import FontContext
from writtenbookeditor.plugins.lib_minecraft.font.types import ProviderFilter
from writtenbookeditor.plugins.lib_minecraft.font.utils import print_bitmap

context = FontContext([Path("./data/test/font/")], [Path("./data/test/font/textures/")])


def test_bitmap_provider():
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
        if __name__ == "__main__":
            print_bitmap(glyph.bitmap)


if __name__ == "__main__":
    test_bitmap_provider()
