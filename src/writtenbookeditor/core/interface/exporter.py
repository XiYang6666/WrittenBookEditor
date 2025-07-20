from abc import ABC, abstractmethod

from .text import PageSequence


class Exporter(ABC):
    """
    导出器

    将分割后的 PageSequence 转换为输出文件.
    """

    @abstractmethod
    def export(self, pages: PageSequence) -> None: ...
