from typing import override


from ..core.interface.formatter import Formatter
from ..core.registry import register_formatter
from ..core.standard.text import SegmentSequence, CommonTextSegment
from ..core.utils.text import create_escaper


@register_formatter("plain_text")
class PlainTextFormatter(Formatter):
    @override
    def format(self, text: str) -> SegmentSequence:
        return [CommonTextSegment({}, text, 0, len(text), create_escaper({}))]
