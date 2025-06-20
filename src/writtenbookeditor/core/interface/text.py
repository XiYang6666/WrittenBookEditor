"""
Text核心接口
"""

from abc import ABC, abstractmethod
from typing import Any, Callable, Iterator, Optional, Sequence

from writtenbookeditor.core.types.string_view import StringView

type StringLike = str | StringView
type Stylesheet = dict[str, Any]
type Escaper = Callable[[StringLike], Iterator[tuple[str, str]]]


class TextSegment(ABC):
    """
    文本段落接口
    """

    @property
    @abstractmethod
    def position(self) -> Optional[tuple[int, int]]:
        """
        返回段落相对于原始字符串的起始位置与结束位置
        """


type SegmentSequence = Sequence[TextSegment]


class Page(ABC):
    """
    页面接口

    必须至少包含一个有相对于原始字符串位置段落.
    否则 segments 属性返回 None.

    segment 为 None 时, 该页面为占位页.
    """

    @property
    @abstractmethod
    def segments(self) -> Optional[SegmentSequence]: ...


type PageSequence = Sequence[Page]
