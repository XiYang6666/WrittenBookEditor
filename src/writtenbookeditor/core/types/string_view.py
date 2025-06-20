from typing import Any, Iterator, Optional, overload

from writtenbookeditor.core.utils.function import instance_method_cache


class StringView:
    """
    字符串视图

    高性能场景下应使用该类型代替 str.
    该类型优化了字符串分割, 避免字符串切片造成的性能损失.
    """

    __slots__ = ("_source", "_start", "_end")

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

    # pos

    def normalize_index(self, index: int, validate: bool = True) -> int:
        """
        规范化索引, 使其在 [0, len(self)] 范围内.
        """
        if index < 0:
            index += len(self)
        assert not validate or 0 <= index <= len(self)
        return index

    def map_pos_to_source(self, *pos: int) -> tuple[int, ...]:
        """
        计算 pos 在 source 中的位置.
        """
        return tuple(self._start + self.normalize_index(p) for p in pos)

    def map_start_end_to_source(self, start: int = 0, end: Optional[int] = None) -> tuple[int, int]:
        """
        计算 start, end 在 source 中的位置.
        """
        start = self.normalize_index(start)
        end = self.normalize_index(end) if end is not None else len(self)
        assert start <= end
        return self._start + start, self._start + end

    # eq

    def __eq__(self, other: Any) -> bool:
        """
        不保证内容相同的两个 StringView 相等.
        与 str 比较时会发生字符串切片. 高性能场景下尽量不要和长字符串比较.
        """
        if isinstance(other, StringView):
            return self._source is other._source and self._start == other._start and self._end == other._end
        elif isinstance(other, str):
            return len(self) == len(other) and str(self) == other  # 先判断长度, 尽量避免字符串切片
        return False

    def content_equals(self, other: str) -> bool:
        """
        依据内容判断是否相等.
        """
        if isinstance(other, StringView):
            return len(self) == len(other) and str(self) == str(other)
        elif isinstance(other, str):
            return len(self) == len(other) and str(self) == other
        else:
            return str(self) == other

    # hash
    def __hash__(self) -> int:
        """
        不保证内容相同的两个StringView的hash值相同.
        """
        return hash((id(self._source), self._start, self._end))

    # get_item & slice

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

    # other

    def __len__(self) -> int:
        return self._end - self._start

    def __iter__(self) -> Iterator[str]:
        for i in range(self._start, self._end):
            yield self._source[i]

    def __repr__(self) -> str:
        return f"StringView({self._source!r}, {self._start}, {self._end})"

    # to_string

    @instance_method_cache
    def to_string(self) -> str:
        """
        转为字符串.

        调用该方法会引发字符串切片并缓存结果, 频繁使用可能引起性能下降或内存占用过高等问题.
        """
        return self._source[self._start : self._end]

    def __str__(self) -> str:
        """
        转为字符串. 与 to_string 等价.

        调用该方法会引发字符串切片并缓存结果, 频繁使用可能引起性能下降或内存占用过高等问题.
        """
        return self.to_string()

    # string utils
    # str 中不会发生字符串切片的常用方法.
    # 如需调用其他方法, 请自行编写相关函数或调用 str() 或 to_string() 后再调用对应方法.

    def startswith(self, prefix: str, start: int = 0, end: Optional[int] = None) -> bool:
        return self._source.startswith(prefix, *self.map_start_end_to_source(start, end))

    def endswith(self, suffix: str, start: int = 0, end: Optional[int] = None) -> bool:
        return self._source.endswith(suffix, *self.map_start_end_to_source(start, end))

    def find(self, sub: str, start: int = 0, end: Optional[int] = None) -> int:
        return self._source.find(sub, *self.map_start_end_to_source(start, end))

    def rfind(self, sub: str, start: int = 0, end: Optional[int] = None) -> int:
        return self._source.rfind(sub, *self.map_start_end_to_source(start, end))

    def strip(self, chars: str = " \t\n\r") -> "StringView":
        start = self._start
        end = self._end
        for start in range(self._start, self._end):
            if self._source[start] not in chars:
                break
        else:
            return StringView(self._source, self._end, self._end)
        for end in range(self._end - 1, start - 1, -1):
            if self._source[end] not in chars:
                return StringView(self._source, start, end + 1)
        else:
            return StringView(self._source, self._start, self._end)

    def lstrip(self, chars: str = " \t\n\r") -> "StringView":
        for i in range(self._start, self._end):
            if self._source[i] not in chars:
                return StringView(self._source, i, self._end)
        return self  # 不可变对象, 没必要创建副本

    def rstrip(self, chars: str = " \t\n\r") -> "StringView":
        for i in range(self._end - 1, self._start - 1, -1):
            if self._source[i] not in chars:
                return StringView(self._source, self._start, i + 1)
        return self  # 不可变对象, 没必要创建副本

    def removeprefix(self, prefix: str) -> "StringView":
        if self.startswith(prefix):
            return StringView(self._source, self._start + len(prefix), self._end)
        return self

    def removesuffix(self, suffix: str) -> "StringView":
        if self.endswith(suffix):
            return StringView(self._source, self._start, self._end - len(suffix))
        return self

    def index(self, sub: str, start: int = 0, end: Optional[int] = None) -> int:
        return self._source.index(sub, *self.map_start_end_to_source(start, end))

    def rindex(self, sub: str, start: int = 0, end: Optional[int] = None) -> int:
        return self._source.rindex(sub, *self.map_start_end_to_source(start, end))

    def count(self, sub: str, start: int = 0, end: Optional[int] = None) -> int:
        return self._source.count(sub, *self.map_start_end_to_source(start, end))
