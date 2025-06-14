"""
标准分页器

适用于标准段落实现的分页器
"""

from dataclasses import dataclass
from typing import Callable, Iterator, Optional

from writtenbookeditor.core.interface.text import PageSequence, SegmentSequence, TextSegment

from .text import CommonPage, StandardTextSegment, TagTextSegment


@dataclass
class PagerContext:
    origin: SegmentSequence
    width_getter: Callable[[str], int]
    page_line_count: int
    page_width: int

    def __post_init__(self):
        self._current_segment_idx: int = -1
        self._current_segment: Optional[TextSegment] = None
        self._pages: list[list[list[TextSegment]]] = []
        self._current_page_lines: list[list[TextSegment]] = []
        self._current_line: list[TextSegment] = []
        self._current_line_width: int = 0
        self._last_space_status: Optional[tuple[int, int, int]] = None

    def next_segment(self) -> Optional[TextSegment]:
        self._current_segment_idx += 1
        if self._current_segment_idx >= len(self.origin):
            return None
        self._current_segment = self.origin[self._current_segment_idx]
        return self._current_segment

    # current_segment

    @property
    def current_segment(self):
        assert self._current_segment is not None, "current segment is None, you should call next_segment() first"
        return self._current_segment

    @current_segment.setter
    def current_segment(self, value: Optional[TextSegment]):
        self._current_segment = value

    def clear_current_segment(self):
        """
        清除当前段落
        """
        self._current_segment = None

    def has_current_segment(self) -> bool:
        """
        测试是否有当前段落
        """
        return self._current_segment is not None

    def iter_current_segment(self) -> Iterator[tuple[str, int, int]]:
        """
        遍历当前段落内字符

        返回 (char, width, char_idx)
        """
        assert isinstance(self.current_segment, StandardTextSegment), "current segment must be StandardTextSegment"
        for i, char in enumerate(self.current_segment):
            yield char, self.width_getter(char), i

    # current_line

    @property
    def current_line(self) -> SegmentSequence:  # 注: 返回 Sequence 以保证不在外部被修改
        return self._current_line

    def update_current_line(
        self,
        line: SegmentSequence,
        width: int = 0,
        last_space_status: Optional[tuple[int, int, int]] = None,
    ):
        """
        更新当前行

        **注意**: 请自行检查 line 是否有效
        """
        self._current_line = list(line)
        self._current_line_width = width
        self._last_space_status = last_space_status

    # current_line_width

    @property
    def current_line_width(self) -> int:
        return self._current_line_width

    def add_width(self, width: int):
        """
        增加宽度到当前行
        """
        self._current_line_width += width

    # last_space_status

    @property
    def last_space_status(self) -> tuple[int, int, int]:
        assert self._last_space_status is not None, "last space status is None, you should set it first"
        return self._last_space_status

    @last_space_status.setter
    def last_space_status(self, value: tuple[int, int, int]):
        self._last_space_status = value

    def clear_last_space_status(self):
        """
        清除上一个空格状态
        """
        self._last_space_status = None

    def has_last_space_status(self) -> bool:
        """
        测试是否有上一个空格状态
        """
        return self._last_space_status is not None

    # utils
    def is_cross_page(self) -> bool:
        """
        测试要换行的情况下是否跨页
        """
        return len(self._current_page_lines) + 1 >= self.page_line_count

    def test_full_line(self, width: int) -> bool:
        """
        测试是否满行
        """
        return self._current_line_width + width > self.page_width

    # operations

    def add_segment(self, segment: TextSegment):
        """
        添加段落到当前行
        """
        self._current_line.append(segment)

    def add_current_segment(self):
        """
        添加当前段落到当前行, 并清空当前段落
        """
        self.add_segment(self.current_segment)
        self.clear_current_segment()

    def clear_line(self):
        """
        清空当前行
        """
        self._current_line = []
        self._current_line_width = 0
        self.clear_last_space_status()

    def new_line(self):
        """
        新建一行
        """
        # 为保证通用性, 暂时不处理页尾标签, 处理完所有页后统一处理
        self._current_page_lines.append(self._current_line)
        assert len(self._current_page_lines) <= self.page_line_count, "line too long"
        if len(self._current_page_lines) == self.page_line_count:
            self._pages.append(self._current_page_lines)
            self._current_page_lines = []
            self.clear_line()
        self.clear_line()

    def add_line(self, line: SegmentSequence):
        """
        添加一行到当前页

        **注意**: 请自行检查 line 是否有效
        """
        self._current_page_lines.append(list(line))
        assert len(line) <= self.page_line_count, "line too long"
        if len(self._current_page_lines) == self.page_line_count:
            # 页满, 保存当前页
            self._pages.append(self._current_page_lines)
            self._current_page_lines = []

    def new_page(self):
        """
        新建一页
        """
        if self.is_cross_page():
            # 新建一行会跨页, 直接新建一行就行了
            self.new_line()
        else:
            # 保存当前行
            self.new_line()
            # 保存当前页
            self._pages.append(self._current_page_lines)
            # 新建一页
            self._current_page_lines = []

    # end process

    def save_last(self):
        """
        保存最后一行和最后一页
        """
        if self._current_line:
            # 保存最后一行
            self.new_line()
        if self._current_page_lines:
            # 保存最后一页
            self._pages.append(self._current_page_lines)

    def process_tags(self):
        """
        处理页尾标签
        """
        result_pages = []
        carry_tags = []  # 携带到下一页的标签
        for page in self._pages:
            lines = page.copy()
            if not lines:
                if carry_tags:
                    result_pages.append(CommonPage([carry_tags]))
                    carry_tags = []
                else:
                    result_pages.append(CommonPage([]))
                continue

            if carry_tags:
                lines[0] = carry_tags + lines[0]
                carry_tags = []

            last_line = lines[-1]
            collected = []
            for seg in reversed(last_line):
                if isinstance(seg, TagTextSegment) and seg.is_prefer_header():
                    collected.insert(0, seg)
                else:
                    break
            if collected:
                lines[-1] = last_line[: -len(collected)]
                carry_tags = collected + carry_tags

            # 清理空行
            # lines = [line for line in lines if line]

            result_pages.append(lines)

        # 处理最后一页
        if carry_tags:
            result_pages.append(CommonPage([carry_tags]))

    def export_pages(self) -> PageSequence:
        """
        导出所有页
        """
        result = []
        for page in self._pages:
            result.append(CommonPage(page))
        return result


def standard_pager(
    ctx: PagerContext,
    *,
    allow_space_wrap_line: bool = True,
):
    """
    标准分页器
    """

    while True:
        if (not ctx.has_current_segment()) and (not ctx.next_segment()):
            # 没有当前段落的情况下尝试获取下一个段落
            # 如果无法获取下一个段落(即遍历完所有段落), 则退出循环
            break
        if not isinstance(ctx.current_segment, StandardTextSegment):
            # 非标准段落, 直接添加
            ctx.add_current_segment()
            continue

        # 遍历标准段落内字符
        for char, char_width, char_idx in ctx.iter_current_segment():
            if char == "\n":
                # 换行符导致的换行, 在换行符后分割段落
                former, latter = ctx.current_segment.half(char_idx + 1, ctx.is_cross_page())
                ctx.add_segment(former)
                ctx.new_line()
                ctx.current_segment = None if latter and latter.is_empty() else latter  # 可能为空
                break
            if ctx.test_full_line(char_width) and (not ctx.has_last_space_status() or not allow_space_wrap_line):
                # 满行导致的换行, 并且无空格或未开启空格折行功能. 当前字符前分割
                former, latter = ctx.current_segment.half(char_idx, ctx.is_cross_page())
                ctx.add_segment(former)
                ctx.new_line()
                ctx.current_segment = latter
                break
            if ctx.test_full_line(char_width) and ctx.has_last_space_status() and allow_space_wrap_line:
                # 满行导致的换行, 有空格且开启空格折行功能. 空格后分割
                segment_pos, char_pos, pre_space_width = ctx.last_space_status
                latter_width = ctx._current_line_width - pre_space_width
                if segment_pos == len(ctx.current_line):
                    # 空格在当前 segment 中
                    former, latter = ctx.current_segment.half(char_pos + 1, ctx.is_cross_page())
                    ctx.add_segment(former)
                    ctx.new_line()
                    ctx.current_segment = latter  # 不可能为空
                    # 无法利用宽度信息, 分割并回溯到空格后.
                    break
                else:
                    # 空格在之前的 segment 中
                    space_segment = ctx.current_line[segment_pos]
                    assert isinstance(space_segment, StandardTextSegment)
                    former, latter = space_segment.half(char_pos + 1, ctx.is_cross_page())
                    former_line = list(ctx.current_line[:segment_pos])
                    former_line.append(former)
                    latter_line = list(ctx.current_line[segment_pos + 1 :])
                    if latter is not None:
                        latter_line.insert(0, latter)
                    ctx.add_line(former_line)
                    ctx.update_current_line(latter_line, latter_width)
                    # 可利用宽度信息, 继续遍历当前 segment.
            if char == " ":
                # 更新空格状态
                ctx.last_space_status = (len(ctx.current_line), char_idx, ctx._current_line_width)
            ctx.add_width(char_width)

        else:
            # 遍历完了段落内所有字符, 没有换行, 直接添加
            ctx.add_current_segment()

    # 处理最后一行与最后一页
    ctx.save_last()
    # 处理页尾标签
    ctx.process_tags()
    # 导出所有页
    return ctx.export_pages()
