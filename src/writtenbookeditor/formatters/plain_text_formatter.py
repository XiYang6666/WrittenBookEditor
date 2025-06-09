from typing import override


from ..core.interface.formatter import Formatter
from ..core.registry import register_formatter
from ..core.standard.text import SegmentSequence, CommonTextSegment
from ..core.utils.text import create_escaper


@register_formatter("plain_text", features=["segment:standard"])
class PlainTextFormatter(Formatter):
    @override
    def format(self, text: str) -> SegmentSequence:
        return [CommonTextSegment({}, text, 0, len(text), create_escaper({}))]


# TIP:
# feature系统: 标识该部分支持的特性, 在该框架中, 数据在各个部分被处理然后交给下个部分
# 下游处理器必须支持上游的所有特性才能正常工作.
