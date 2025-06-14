"""
测试标准分页器性能

用于分析分页器的实现是否存在性能问题.
"""

import cProfile
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path("./src").absolute()))

from writtenbookeditor.core.standard.pager import PagerContext, standard_pager
from writtenbookeditor.core.standard.text import CommonTextSegment
from writtenbookeditor.core.utils.text import empty_escaper

page_line = 15
page_width = 20


def width_getter(char: str) -> int:
    if char == "\n":
        return 0
    return 1


text = Path("data/test/romeo_and_juliet.txt").read_text(encoding="utf-8") * 5
segments = [CommonTextSegment({}, text, 0, len(text), empty_escaper)]
ctx = PagerContext(segments, width_getter, page_line_count=page_line, page_width=page_width)


def test():
    standard_pager(ctx)


start_time = time.time()
cProfile.run("test()")
end_time = time.time()
print(f"text length: {len(text)}")
print(f"time elapsed: {end_time - start_time:.2f}s")
print(f"about {len(text) / (end_time - start_time) / 1000:.0f}k chars per second.")
