import sys
from pathlib import Path
from timeit import timeit

sys.path.insert(0, str(Path("./src").absolute()))

from writtenbookeditor.core.standard.pager import standard_pager
from writtenbookeditor.core.standard.text import CommonTextSegment
from writtenbookeditor.core.utils.text import empty_escaper


text = Path("data/test/romeo_and_juliet.txt").read_text(encoding="utf-8")
text_segments = [CommonTextSegment({}, text, 0, len(text), empty_escaper)]


def width_getter(char: str) -> int:
    return 1


unoptimized_time = timeit(
    lambda: standard_pager(text_segments, width_getter, page_line=10, page_width=10, space_wrap_optimize=False),
    number=10,
)

optimized_time = timeit(
    lambda: standard_pager(text_segments, width_getter, page_line=10, page_width=10, space_wrap_optimize=True),
    number=10,
)

print(f"Unoptimized time: {unoptimized_time:.5f}s")
print(f"Optimized time: {optimized_time:.5f}s")
