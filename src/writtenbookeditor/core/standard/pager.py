"""
标准分页器

适用于标准段落实现的分页器
"""

from itertools import takewhile
from typing import Callable, Optional


from writtenbookeditor.core.utils.debug import assert_while_debugging

from ..interface.text import TextSegment, SegmentSequence, Page, PageSequence
from .text import StandardTextSegment, CommonPage, TagTextSegment


def standard_pager(
    segment_sequence: SegmentSequence,
    width_getter: Callable[[str], int],
    *,
    page_line: int,
    page_width: int,
    allow_space_wrap_line: bool = True,
    space_wrap_optimize: bool = False,  # 仅在 width_getter 开销较大时效果明显(都带缓存了哪来的开销)
) -> PageSequence:
    if not segment_sequence:
        return []

    pages: list[Page] = []
    page_lines: list[SegmentSequence] = []
    line: list[TextSegment] = []
    line_width: int = 0

    # 保存上一个空格的状态
    # segment 序号(相对于 line), char 序号, 空格后宽度
    # 如果为开启空格折行功能, 该变量始终为 None
    last_space_status: Optional[tuple[int, int, int]] = None

    def new_line(preset_line: Optional[list[TextSegment]] = None):
        """
        新建一行

        预设行必须 0 宽度
        """
        nonlocal line, line_width, last_space_status
        # 验证预设行是否 0 宽度
        assert_while_debugging(
            lambda: all(s.is_empty() for s in preset_line or [] if isinstance(s, StandardTextSegment)),
            "present line must be 0 width",
        )

        line = preset_line or []
        line_width = 0
        last_space_status = None

    def save_page():
        """
        新建一页
        """
        nonlocal pages, page_lines, line, line_width, last_space_status
        # 提取开头标签
        header_line = list(
            takewhile(
                lambda seg: isinstance(seg, TagTextSegment) and seg.is_prefer_header(),
                reversed(line),
            )
        )
        header_line.reverse()
        # 保存当前页
        pages.append(CommonPage(page_lines))
        # 新建一页
        page_lines = []
        # 新建一行, 保存开头
        new_line(header_line)

    def save_line():
        """
        保存当前行
        """
        nonlocal pages, page_lines, line, line_width, last_space_status
        # 保存当前行
        page_lines.append(line)
        if len(page_lines) >= page_line:
            # 超过一页的行数, 保存当前页
            return save_page()
        # 新建一行
        new_line()

    def add_segment(segment: Optional[TextSegment]):
        """
        添加段落到当前行
        """
        nonlocal line, line_width, last_space_status
        if segment is None:
            return
        if isinstance(segment, StandardTextSegment) and segment.is_empty():
            return
        line.append(segment)

    segment_pos = -1
    current_segment: Optional[StandardTextSegment] = None

    # 遍历所有 Segment
    while True:
        if current_segment is None or current_segment.is_empty():  # 处理完一个 Segment 了, 开始处理下一个 Segment.
            segment_pos += 1
            if segment_pos >= len(segment_sequence):
                # 处理完所有 Segment 了
                break
            segment = segment_sequence[segment_pos]
            if not isinstance(segment, StandardTextSegment):
                # 非标准段落, 无法获取宽度, 认为 0 宽, 直接添加
                add_segment(segment)
                continue

            # 当前段落, 如果遍历获取到的 Segment 被分割过则会被更新为分割后半段
            # 注: 按当前逻辑每当 current_segment 被更新都应 break
            current_segment = segment

        # 段落内遍历字符
        for i, char in enumerate(current_segment):
            char_width = width_getter(char)
            if char == "\n":
                is_cross_page = len(page_lines) + 1 >= page_line
                # 换行符导致的换行, 在换行符后分割段落
                former_seg, latter_seg = current_segment.half(i + 1, is_cross_page)
                add_segment(former_seg)
                save_line()
                current_segment = latter_seg
                break
            elif line_width + char_width > page_width:
                # 满行导致的换行
                # 如果没有空格则在字符前分割
                # 有空格则在空格后分割(刚好适配了连续空格)
                if last_space_status is None:
                    # 无空格或未开启空格折行功能, 空格前分割
                    is_cross_page = len(page_lines) + 1 >= page_line
                    former_seg, latter_seg = current_segment.half(i, is_cross_page)
                    add_segment(former_seg)
                    save_line()
                    current_segment = latter_seg
                    break
                # 有空格, 空格后分割
                segment_pos, char_pos, pre_space_width = last_space_status
                latter_width = line_width - pre_space_width
                if segment_pos == len(line):
                    # if current_segment.text.startswith("Yo"):
                    #
                    # 空格就在当前segment内
                    space_segment = current_segment
                    is_cross_page = len(page_lines) + 1 >= page_line
                    if space_wrap_optimize:
                        # 空格折行优化
                        # 在当前segment处理的字符后分割一次以方便下一轮处理使用宽度信息.
                        # 避免了直接 break 导致的宽度信息丢失, 重复计算宽度.
                        # 但这样是非换行导致的分割, 更考验 Segment 实现的正确性.

                        # TIP: 优化你麻痹, 写了一天跑完 benchmark 比优化前还慢了 0.几秒
                        former_seg, mid_and_latter_seg = current_segment.half(char_pos + 1, is_cross_page)
                        add_segment(former_seg)
                        save_line()
                        assert mid_and_latter_seg is not None
                        # pos 实际是 (i + 1) - (char_pos + 1) 的化简
                        mid_seg, latter_seg = mid_and_latter_seg.half(i - char_pos, False)
                        add_segment(mid_seg)
                        current_segment = latter_seg
                        line_width = latter_width + char_width
                        if char == " ":
                            last_space_status = (0, i - char_pos - 1, line_width)
                        break

                    # 未开启空格折行优化, break 后会重新计算当前 segment.
                    # 如果强行不 break 继续处理, i 指向的位置会错位.
                    # 应该在配置中处理
                    former_seg, latter_seg = space_segment.half(char_pos + 1, is_cross_page)
                    add_segment(former_seg)
                    save_line()
                    current_segment = latter_seg
                    break
                else:
                    # 空格在之前的 segment 中
                    space_segment = line[segment_pos]
                    assert isinstance(space_segment, StandardTextSegment)
                    is_cross_page = len(page_lines) + 1 >= page_line
                    former_seg, latter_seg = space_segment.half(char_pos + 1, is_cross_page)
                    former_line = line[:segment_pos] + [former_seg]
                    latter_line = line[segment_pos + 1 :]
                    assert latter_seg is not None  # 不可能为None, 即使为空也必须插入
                    latter_line.insert(0, latter_seg)
                    line = former_line
                    save_line()
                    line = latter_line
                    # 没更新 current_segment, 只是换了一行, 继续遍历当前 segment.
                    line_width = latter_width + char_width
                    if char == " ":
                        last_space_status = (len(line), 0, line_width)
                    continue
            else:
                # 正常字符, 直接添加到当前行
                line_width += char_width
                if char == " " and allow_space_wrap_line:
                    last_space_status = (len(line), i, line_width)
        else:
            # 遍历完一个 Segment 了, 开始处理下一个 Segment.
            add_segment(current_segment)
            current_segment = None

    # 处理最后一页
    if line:
        save_line()
    if line:
        # 跨页并且有开标签, line 不为空
        save_line()
    if page_lines:
        pages.append(CommonPage(page_lines))

    return pages
