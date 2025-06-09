from abc import ABC, abstractmethod

from .text import SegmentSequence


class Formatter(ABC):
    """
    格式化器

    将文本转为 SegmentSequence.
    """

    @abstractmethod
    def format(self, text: str) -> SegmentSequence:
        """
        将文本转为 SegmentSequence.
        """
