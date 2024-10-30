from typing import Literal, Optional

from .style import Style
from .text_component import TextComponent


SegmentType = Literal["text", "start_tag", "end_tag", "single_tag"]


class TextSegment:
    def __init__(self, type: SegmentType, start: int, end: int, style: Optional[Style] = None, text_component: Optional[TextComponent] = None):
        self.type: SegmentType = type
        self.start: int = start
        self.end: int = end
        self.style: Style = style or Style()
        self.text_component: Optional[TextComponent] = text_component

    def __repr__(self):
        return f"TextSegment(type={self.type}, start={self.start}, end={self.end}, style={self.style})"

    def clone(self):
        return TextSegment(self.type, self.start, self.end, self.style.clone(), self.text_component)

    @classmethod
    def text(cls, start: int, end: int, style: Optional[Style] = None):
        return cls("text", start, end, style)

    @classmethod
    def start_tag(cls, start: int, end: int):
        return cls("start_tag", start, end)

    @classmethod
    def end_tag(cls, start: int, end: int):
        return cls("end_tag", start, end)

    @classmethod
    def single_tag(cls, start: int, end: int, style: Optional[Style] = None, text_component: Optional[TextComponent] = None):
        instance = cls("single_tag", start, end, style, text_component)
        if instance.text_component is not None:
            instance.style.apply_to_component(instance.text_component)
        return instance


TextSegmentSequence = list[TextSegment]
