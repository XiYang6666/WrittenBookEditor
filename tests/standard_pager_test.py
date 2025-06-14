from pathlib import Path

# import sys

# sys.path.insert(0, "./src")

from writtenbookeditor.core.utils.text import empty_escaper
from writtenbookeditor.core.standard.pager import PagerContext, standard_pager
from writtenbookeditor.core.standard.text import CommonTextSegment, CommonPage, StandardTextSegment


def test_pager():
    """
    测试分页逻辑
    """

    page_line = 10
    page_width = 10

    def width_getter(char: str) -> int:
        if char == "\n":
            return 0
        return 1

    text = Path("data/test/romeo_and_juliet.txt").read_text(encoding="utf-8")[:1000]
    segments = [CommonTextSegment({}, text, 0, len(text), empty_escaper)]
    ctx = PagerContext(segments, width_getter, page_line_count=page_line, page_width=page_width)
    pages = standard_pager(ctx)

    for i, page in enumerate(pages):
        assert isinstance(page, CommonPage)
        assert len(page.lines) <= page_line, f"page {i} lines {len(page.lines)} > page line {page_line}"
        for j, line in enumerate(page.lines):
            width = 0
            for seg in line:
                assert isinstance(seg, StandardTextSegment)
                width += sum(width_getter(c) for c in seg.text or "")
                print(len(seg.text or ""))
            assert width <= page_width, f"page {i} line {j} width {width} > page width {page_width}"
