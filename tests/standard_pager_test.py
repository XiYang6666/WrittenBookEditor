from pathlib import Path

# import sys

# sys.path.insert(0, "./src")

from writtenbookeditor.core.utils.text import empty_escaper
from writtenbookeditor.core.standard.pager import standard_pager
from writtenbookeditor.core.standard.text import CommonTextSegment


def test_optimize_space_wrap():
    """
    测试优化空格换行逻辑
    """

    def width_getter(char: str) -> int:
        return 1

    text = Path("data/test/romeo_and_juliet.txt").read_text(encoding="utf-8")[:1000]
    # text = "1111122223333344444 1110 12 3456"
    # text = "you are not located the United States"
    # text = "1\n2\n3\n4\n5\n6\n"
    # text = "ns\nwhatsoever. You may copy it, give it "
    segments = [CommonTextSegment({}, text, 0, len(text), empty_escaper)]
    pages_1 = standard_pager(segments, width_getter, page_line=5, page_width=5, space_wrap_optimize=True)
    pages_2 = standard_pager(segments, width_getter, page_line=5, page_width=5, space_wrap_optimize=False)

    # for i, page_1 in enumerate(pages_1):
    #     if page_1 != pages_2[i]:
    #         print(f"page {i} is different")
    #         print(f"page 1: \n{page_1}")
    #         print(f"page 2: \n{pages_2[i]}")

    # with open("1.txt", "w", encoding="utf-8") as f:
    #     f.write(str(pages_1))
    # with open("2.txt", "w", encoding="utf-8") as f:
    #     f.write(str(pages_2))

    assert pages_1 == pages_2


if __name__ == "__main__":
    test_optimize_space_wrap()
