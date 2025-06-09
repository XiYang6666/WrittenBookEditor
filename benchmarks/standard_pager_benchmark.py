"""
测试标准分页器性能

用于分析分页器的实现是否存在性能问题.
"""

import cProfile
import sys
from pathlib import Path

sys.path.insert(0, str(Path("./src").absolute()))

from writtenbookeditor.core.standard.text import CommonTextSegment
from writtenbookeditor.core.standard.pager import standard_pager
from writtenbookeditor.core.utils.text import empty_escaper


def test():
    text = "Hello, world!\nThis is a test.awf ahjfdhjgdhjsgfhjsg  djfh jkd d djsfh jkh ksd "
    text += "\n aaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaa aaaaaaaa aaaaaaaaa\n"
    text += "You are right, but Genshin Impact is a brand new open world adventure game independently developed by miHoYo. "
    text += 'The game takes place in a fantasy world called "Teyvat",'
    text += ' where those chosen by God will be granted the "Eye of God" to guide the power of elements. '
    text += 'You will play a mysterious character named "Traveler" and meet companions with different '
    text += "personalities and unique abilities during your free travel. "
    text += "Together with them, you will defeat powerful enemies and find your lost relatives "
    text += '- at the same time, gradually discover the truth of "Genshin Impact".'
    text += "a" * 304
    # len(text) == 1000
    text *= 10 * 100

    segments = [CommonTextSegment({}, text, 0, len(text), empty_escaper)]

    def width_getter(text: str) -> int:
        return 8

    standard_pager(segments, width_getter, page_line=14, page_width=228)


cProfile.run("test()")
