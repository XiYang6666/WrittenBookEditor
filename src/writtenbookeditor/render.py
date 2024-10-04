import numpy as np
from PySide6.QtGui import QImage, QPainter

from .font import get_char_info
from .book import Page
from .book import calc_char_width
from .book import PAGE_WIDTH, PAGE_LINES, PAGE_LINE_HEIGHT

RENDERED_PAGE_WIDTH = PAGE_WIDTH
RENDERED_PAGE_HEIGHT = PAGE_LINES * PAGE_LINE_HEIGHT + 4


def render_page(page: Page, unicode: bool = False, jp: bool = False) -> QImage:
    image = QImage(RENDERED_PAGE_WIDTH, RENDERED_PAGE_HEIGHT, QImage.Format.Format_RGBA8888)
    image.fill(0)
    painter = QPainter(image)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
    for i, line in enumerate(page.processed_lines()):
        x = 0
        for char in line.removesuffix("\n"):
            char_info = get_char_info(char, unicode, jp)
            char_scale = char_info.scale
            char_bitmap = char_info.bitmap
            height, width = char_bitmap.shape
            char_array = np.zeros((height, width, 4), dtype=np.uint8)
            char_array[char_bitmap == 1] = [0, 0, 0, 255]
            char_img = QImage(char_array.copy().data, width, height, QImage.Format.Format_RGBA8888)
            char_img = char_img.scaled(width * char_scale, height * char_scale)
            y = i * PAGE_LINE_HEIGHT + 18 - height * char_scale - char_info.offset * char_scale
            painter.drawImage(x, y, char_img)
            char_width = calc_char_width(char, unicode, jp)
            x += char_width
    painter.end()
    return image
