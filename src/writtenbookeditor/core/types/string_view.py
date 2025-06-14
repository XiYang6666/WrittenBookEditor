from functools import cache
from typing import Any, Iterator, Optional, overload

# 越写越 jb 麻烦.
# 盲猜没人会大量处理 100k+ 字符的文本.
# 现阶段先在局部使用 StringView 代替 str 实现性能优化.
# 后续有需要再重构字符串处理代码.


class StringView:
    """
    字符串视图

    高性能场景下应使用该类型代替 str.
    该类型优化了字符串分割, 避免字符串切片造成的性能损失.
    """

    __slots__ = ("_source", "_start", "_end")

    @classmethod
    def empty(cls, source: str = "") -> "StringView":
        return cls(source, 0, 0)

    def __init__(self, source: str, start: int = 0, end: Optional[int] = None):
        self._source = source
        self._start = self.normalize_index(start, validate=False)
        self._end = self.normalize_index(end, validate=False) if end is not None else len(source)
        assert 0 <= self._start <= self._end <= len(source)

    @property
    def source(self) -> str:
        return self._source

    @property
    def pos(self) -> tuple[int, int]:
        return self._start, self._end

    @cache
    def to_string(self) -> str:
        """
        会缓存结果, 引起性能下降, 内存占用过高. 请谨慎调用.
        """
        return self._source[self._start : self._end]

    def calc_offset(self, *pos: int) -> tuple[int, ...]:
        """
        计算偏移量.
        """
        return tuple(self._start + self.normalize_index(p) for p in pos)

    def normalize_index(self, index: int, validate: bool = True) -> int:
        if index < 0:
            index += len(self)
        assert not validate or 0 <= index <= len(self)
        return index

    def __eq__(self, other: Any) -> bool:
        """
        不保证内容相同的两个StringView相等.
        尽量不要和 str 比较.
        """
        if isinstance(other, StringView) and self._source is other._source:
            return self._start == other._start and self._end == other._end
        if isinstance(other, str):
            return str(self) == other
        return False

    def __hash__(self) -> int:
        """
        hash不保证内容相同的两个StringView的hash值相同.
        """
        return hash((id(self._source), self._start, self._end))

    @overload
    def __getitem__(self, index: int) -> str: ...

    @overload
    def __getitem__(self, index: slice) -> "StringView": ...

    def __getitem__(self, index: int | slice) -> "str|StringView":
        if isinstance(index, int):
            index = self.normalize_index(index)
            return self._source[self._start + index]
        else:
            assert index.step is None or index.step == 1
            start = self.normalize_index(index.start) if index.start is not None else 0
            end = self.normalize_index(index.stop) if index.stop is not None else len(self)
            assert start <= end
            return StringView(self._source, self._start + start, self._start + end)

    def __repr__(self) -> str:
        return f"StringView({self._source!r}, {self._start}, {self._end})"

    # str methods
    # 会发生字符串切片但常用的方法

    def __str__(self) -> str:
        """
        会缓存结果,引起性能下降, 内存占用过高. 请谨慎调用.
        """
        return self.to_string()

    def __len__(self) -> int:
        return self._end - self._start

    def __iter__(self) -> Iterator[str]:
        for i in range(self._start, self._end):
            yield self._source[i]

    # str methods
    # 不会发生字符串切片的常用方法.
    # 如需实现其他方法, 请自行编写函数或调用str方法后再调用对应方法.

    def endswith(self, suffix: str, start: int = 0, end: Optional[int] = None) -> bool:
        start = self.normalize_index(start)
        end = self.normalize_index(end) if end is not None else len(self)
        assert start <= end
        return self._source.endswith(suffix, self._start + start, self._start + end)

    def find(self, sub: str, start: int = 0, end: Optional[int] = None) -> int:
        start = self.normalize_index(start)
        end = self.normalize_index(end) if end is not None else len(self)
        assert start <= end
        return self._source.find(sub, self._start + start, self._start + end)

    def index(self, sub: str, start: int = 0, end: Optional[int] = None) -> int:
        start = self.normalize_index(start)
        end = self.normalize_index(end) if end is not None else len(self)
        assert start <= end
        return self._source.index(sub, self._start + start, self._start + end)

    def lstrip(self, chars: str = " \t\n\r") -> "StringView":
        for i in range(self._start, self._end):
            if self._source[i] not in chars:
                return StringView(self._source, i, self._end)
        return self  # 不可变对象, 没必要创建副本

    def removeprefix(self, prefix: str) -> "StringView":
        if self.startswith(prefix):
            return StringView(self._source, self._start + len(prefix), self._end)
        return self

    def removesuffix(self, suffix: str) -> "StringView":
        if self.endswith(suffix):
            return StringView(self._source, self._start, self._end - len(suffix))
        return self

    def rfind(self, sub: str, start: int = 0, end: Optional[int] = None) -> int:
        start = self.normalize_index(start)
        end = self.normalize_index(end) if end is not None else len(self)
        assert start <= end
        return self._source.rfind(sub, self._start + start, self._start + end)

    def rstrip(self, chars: str = " \t\n\r") -> "StringView":
        for i in range(self._end - 1, self._start - 1, -1):
            if self._source[i] not in chars:
                return StringView(self._source, self._start, i + 1)
        return self  # 不可变对象, 没必要创建副本

    def startswith(self, prefix: str, start: int = 0, end: Optional[int] = None) -> bool:
        start = self.normalize_index(start)
        end = self.normalize_index(end) if end is not None else len(self)
        assert start <= end
        return self._source.startswith(prefix, self._start + start, self._start + end)
