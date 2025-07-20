"""
测试字形提供器性能
"""

import cProfile
import os
import sys
import time
from functools import cache
from pathlib import Path

import psutil

sys.path.insert(0, str(Path("./src").absolute()))

from writtenbookeditor.plugins.lib_minecraft.font.genernal_loader import FontContext
from writtenbookeditor.plugins.lib_minecraft.font.types import ProviderFilter

context = FontContext([Path("./data/test/font/")], [Path("./data/test/font/textures/")])
bare_provider = context.create_reference_provider("default")
cached_provider = cache(context.create_reference_provider("default"))
text = Path("./data/test/text/从百草园到三味书屋.txt").read_text("utf-8")
text += Path("data/test/text/romeo_and_juliet.txt").read_text(encoding="utf-8")


def test_bare():
    for char in text:
        bare_provider(char, ProviderFilter.default())


def test_cached():
    for char in text:
        cached_provider(char, ProviderFilter.default())


if __name__ == "__main__":
    start = time.time()
    cProfile.run("test_bare()", sort="tottime")
    bare_used = time.time() - start

    start = time.time()
    cProfile.run("test_cached()", sort="tottime")
    cached_used = time.time() - start

    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()

    print(f"bare: {bare_used:.2f}s")
    print(f"about {len(text) / 1000 / bare_used:.2f}k chars per second")
    print(f"cached: {cached_used:.2f}s")
    print(f"memery usage: {mem_info.rss / 1024 / 1024:.2f}MB")
