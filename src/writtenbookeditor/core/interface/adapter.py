from abc import ABC, abstractmethod

from PIL import Image

from .text import PageSequence, SegmentSequence


class Adapter(ABC):
    """
    适配器

    用于将 SegmentSequence 分割, 渲染为图片, 导出等.
    """

    @abstractmethod
    def split(self, segment_sequence: SegmentSequence) -> PageSequence:
        """
        将 SegmentSequence 分割为 PageSequence

        即按页分割文本序列.
        """

    @abstractmethod
    def render(self, page: SegmentSequence) -> Image.Image:
        """
        渲染 Page为图片
        """
