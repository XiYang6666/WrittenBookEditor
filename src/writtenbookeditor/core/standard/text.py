"""
包装核心接口, 实现具体的文本段落类
"""

from abc import abstractmethod
from functools import cache
from typing import Iterator, Optional, Sequence, override

from ..utils.debug import assert_while_debugging
from ..interface.text import Stylesheet, Escaper, TextSegment, SegmentSequence, Page
from ..utils.text import escape_text, map_escaped_pos_to_bare

__all__ = [
    "StandardTextSegment",
    "CorrespondingTextSegment",
    "UnrelatedTextSegment",
    "CommonTextSegment",
    "PlaceholderTextSegment",
    "VariableTextSegment",
    "CommonPage",
]


# ---------- TextSegment implementations ----------

# 抽象类


class CorrespondingTextSegment(TextSegment):
    """
    对应文本段落

    段落由原始文本产生, 需提供对应位置.
    """

    def __init__(
        self,
        origin: str,
        start: int,
        end: int,
    ):
        self._origin = origin
        self._position = (start, end)

    @property
    @override
    def position(self) -> tuple[int, int]:
        return self._position

    def __eq__(self, other) -> bool:
        return type(other) is self.__class__ and self._origin == other._origin and self._position == other._position


class StandardTextSegment(TextSegment):
    """
    标准文本段落

    含样式,文本并且可分割的段落.
    """

    def __init__(self, style: Stylesheet):
        self._style = style

    @property
    @abstractmethod
    def text(self) -> Optional[str]: ...

    @abstractmethod
    def half(self, pos: int, is_cross_page: bool) -> "tuple[StandardTextSegment,Optional[StandardTextSegment]]":
        """
        一分为二

        以段落对应的文本为基础进行分割,
        并返回两个 Segment, 分别为左右两部分.
        如果返回的右部分为 None 则表示不应分割出右部分.

        这个方法在处理需转义字符时可能更高效.
        """

    @abstractmethod
    def __eq__(self, other) -> bool: ...

    @abstractmethod
    def __hash__(self) -> int: ...

    @property
    def style(self) -> Stylesheet:
        return self._style

    def is_empty(self) -> bool:
        return not bool(self.text)

    def __iter__(self) -> Iterator[str]:
        yield from self.text or ""

    def __repr__(self):
        return f"<{self.__class__.__name__} style={self._style}>{self.text}</{self.__class__.__name__}>"


class UnrelatedTextSegment(StandardTextSegment):
    """
    不相关文本段落

    段落文本与原始文本不相关, 需要提供文本内容.
    """

    @override
    def __init__(
        self,
        style: Stylesheet,
        text: str,
    ):
        StandardTextSegment.__init__(self, style)
        self._text = text

    @property
    @override
    def text(self) -> str:
        return self._text

    @override
    def __eq__(self, other) -> bool:
        return type(other) is self.__class__ and self._style == other._style and self._text == other._text

    @override
    def __hash__(self) -> int:
        return hash((frozenset(self._style), self._text))


# 具体类


class CommonTextSegment(StandardTextSegment, CorrespondingTextSegment):
    """
    普通文本段落

    仅记录文本与样式.

    文本严格对应原始文本的转义结果, 需要一个转义器.

    分割: 跨页完全分割, 跨行后续段落皆为 ShadowTextSegment
    """

    def __init__(
        self,
        style: Stylesheet,
        origin: str,
        start: int,
        end: int,
        escaper: Escaper,
    ):
        StandardTextSegment.__init__(self, style)
        CorrespondingTextSegment.__init__(self, origin, start, end)
        self._escaper = escaper

    @property
    @override
    @cache
    def text(self) -> str:
        """
        **注意: 该方法会转义所有文本, 引起性能严重下降, 不应在非调试时调用**
        """
        bare_text = self._origin[self._position[0] : self._position[1]]
        return escape_text(bare_text, self._escaper)

    @override
    def half(self, pos, is_cross_page=False):
        assert_while_debugging(lambda: pos >= 0 and pos <= len(self.text))
        bare_text = self._origin[self._position[0] : self._position[1]]
        (o_pos,) = map_escaped_pos_to_bare(bare_text, self._escaper, pos)
        first_half = CommonTextSegment(
            self._style,
            self._origin,
            self.position[0],
            self.position[0] + o_pos,
            self._escaper,
        )
        second_half = (
            CommonTextSegment(
                self._style,
                self._origin,
                self.position[0] + o_pos,
                self.position[1],
                self._escaper,
            )
            if is_cross_page
            else MarkTextSegment(
                self._style,
                self._origin,
                self.position[0] + o_pos,
                self.position[1],
                self._escaper,
            )
        )
        return first_half, second_half

    @override
    def is_empty(self) -> bool:
        """优化空判断"""
        return self.position[0] == self.position[1]

    @override
    def __iter__(self) -> Iterator[str]:
        """优化迭代器"""
        bare_text = self._origin[self._position[0] : self._position[1]]
        for t in self._escaper(bare_text):
            yield t[1]

    @override
    def __eq__(self, other) -> bool:
        return CorrespondingTextSegment.__eq__(self, other) and self._style == other._style and self._escaper == other._escaper

    def __hash__(self) -> int:
        return hash((frozenset(self._style), self._origin, self._position, self._escaper))


class MarkTextSegment(StandardTextSegment, CorrespondingTextSegment):
    """
    标记文本段落

    由 RichTextSegment 生成的占位符, 对应原始文本某部分并且段落文本是原始文本的转义,
    用于占位和标记如何分割 RichTextSegment.

    分割规则: 跨页产生的后半段为新的 RichTextSegment
    """

    def __init__(
        self,
        style: Stylesheet,
        origin: str,
        start: int,
        end: int,
        escaper: Escaper,
    ):
        StandardTextSegment.__init__(self, style)
        CorrespondingTextSegment.__init__(self, origin, start, end)
        self._escaper = escaper

    @property
    @override
    @cache
    def text(self) -> str:
        """
        **注意: 该方法会转义所有文本, 引起性能严重下降, 不应在非调试时调用**
        """
        bare_text = self._origin[self._position[0] : self._position[1]]
        return escape_text(bare_text, self._escaper)

    @override
    def half(self, pos, is_cross_page=False):
        assert_while_debugging(lambda: pos >= 0 and pos <= len(self.text))
        bare_text = self._origin[self._position[0] : self._position[1]]
        (o_pos,) = map_escaped_pos_to_bare(bare_text, self._escaper, pos)
        first_half = MarkTextSegment(
            self._style,
            self._origin,
            self.position[0],
            self.position[0] + o_pos,
            self._escaper,
        )
        second_half = (
            CommonTextSegment(
                self._style,
                self._origin,
                self.position[0] + o_pos,
                self.position[1],
                self._escaper,
            )
            if is_cross_page
            else MarkTextSegment(
                self._style,
                self._origin,
                self.position[0] + o_pos,
                self.position[1],
                self._escaper,
            )
        )
        return first_half, second_half

    @override
    def is_empty(self) -> bool:
        """优化空判断"""
        return self.position[0] == self.position[1]

    @override
    def __iter__(self) -> Iterator[str]:
        """优化迭代器"""
        bare_text = self._origin[self._position[0] : self._position[1]]
        for t in self._escaper(bare_text):
            yield t[1]

    @override
    def __eq__(self, other) -> bool:
        return CorrespondingTextSegment.__eq__(self, other) and self._style == other._style and self._escaper == other._escaper

    def __hash__(self) -> int:
        return hash((frozenset(self._style), self._origin, self._position, self._escaper))


class PlaceholderTextSegment(UnrelatedTextSegment):
    """
    占位符文本段落

    由 VariableTextSegment 生成的占位符, 不对应原始文本任何部分, 仅用于占位.

    分割规则: 不可跨页
    """

    @override
    def __init__(
        self,
        style: Stylesheet,
        text: str,
    ):
        UnrelatedTextSegment.__init__(self, style, text)

    @property
    @override
    def position(self) -> None:
        return None

    @override
    def half(self, pos, is_cross_page=False):
        assert pos >= 0 and pos <= len(self.text)
        first_half = PlaceholderTextSegment(
            self._style,
            self._text[:pos],
        )
        second_half = (
            None
            if is_cross_page
            else PlaceholderTextSegment(
                self._style,
                self._text[pos:],
            )
        )
        return first_half, second_half


class VariableTextSegment[T](UnrelatedTextSegment, CorrespondingTextSegment):
    """
    变量文本段落

    对应原始文本的一部分, 但对应的字符不是原始文本的转义.
    包含额外数据, 用于保存额外信息.

    分割: 不可跨页, 跨行后续段落皆为占位符
    """

    @override
    def __init__(
        self,
        style: Stylesheet,
        origin: str,
        start: int,
        end: int,
        text: str,
        data: T,
    ):
        UnrelatedTextSegment.__init__(self, style, text)
        CorrespondingTextSegment.__init__(self, origin, start, end)

        self._data = data

    @property
    @override
    def position(self) -> tuple[int, int]:
        return self._position

    @override
    def half(self, pos, is_cross_page=False):
        assert pos >= 0 and pos <= len(self.text)
        first_half = VariableTextSegment(
            self._style,
            self._origin,
            self.position[0],
            self.position[1],
            self._text[:pos],
            self._data,
        )
        second_half = (
            None
            if is_cross_page
            else PlaceholderTextSegment(
                self._style,
                self._text[pos:],
            )
        )
        return first_half, second_half

    @property
    def data(self) -> T:
        return self._data


class TagTextSegment(CorrespondingTextSegment):
    """
    标签文本段落

    由原始文本产生, 对应原始文本的标记部分.
    """

    @override
    def __init__(
        self,
        origin: str,
        start: int,
        end: int,
        prefer_header: bool = False,
    ):
        CorrespondingTextSegment.__init__(self, origin, start, end)
        self._is_prefer_header = prefer_header

    def is_prefer_header(self) -> bool:
        """
        标签在页尾时的行为.

        用于确定标签应被放在页首还是页尾.
        """
        return self._is_prefer_header

    def __repr__(self):
        return f"<{self.__class__.__name__} behavior={self._is_prefer_header}>"


# ---------- Page mplementations ----------


class BasePage(Page):
    """
    基础页面

    由行组成的页面
    """

    def __init__(self, lines: Sequence[SegmentSequence]):
        self._lines = lines

    @property
    def lines(self) -> Sequence[SegmentSequence]:
        return self._lines

    def __repr__(self) -> str:
        text = f"<{self.__class__.__name__}>\n"
        for line in self._lines:
            for seg in line:
                text += f"{seg}"
            text += "<br>\n"
        text += f"</{self.__class__.__name__}>"
        return text


class CommonPage(BasePage):
    """
    普通页面

    基于核心实现包的页面实现.
    """

    @property
    @override
    def segments(self) -> SegmentSequence:
        all_segments = [seg for line in self._lines for seg in line]
        result = []

        for seg in all_segments:
            if seg.position is None:
                # 占位符, 跳过
                continue
            elif isinstance(seg, MarkTextSegment) and result and isinstance(result[-1], CommonTextSegment):
                # 合并 MarkTextSegment 到前一个 CommonTextSegment
                start_pos = result[-1].position[0]
                end_pos = seg.position[1]
                result[-1] = CommonTextSegment(seg.style, seg._origin, start_pos, end_pos, seg._escaper)
                continue
            elif isinstance(seg, MarkTextSegment):
                # 错误的段落序列
                assert False, "Invalid segment sequence. MarkTextSegment not followed by RichTextSegment."
            else:
                # 正常段落
                result.append(seg)
        return result

    def __eq__(self, other) -> bool:
        """
        仅判断处理后的 segment 是否等价, 不保证每行的 segment 均相同.
        """
        return type(other) is self.__class__ and self.segments == other.segments
