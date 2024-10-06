from typing import Optional
from io import StringIO
import json

import nbtlib

from .util import calc_char_width

PAGE_WIDTH = 228
PAGE_LINES = 14
PAGE_LINE_HEIGHT = 18


class Page:
    def __init__(
        self,
        lines: Optional[list] = None,
        *,
        unicode: bool = False,
        jp: bool = False,
        allow_page_split: bool = False,
        force_no_wrap: bool = False,
    ):
        self.lines: list[str] = lines or []
        self.unicode: bool = unicode
        self.jp: bool = jp
        self.allow_page_split: bool = allow_page_split
        self.force_no_wrap: bool = force_no_wrap

    @classmethod
    def from_plaintext_stream(
        cls,
        stream: StringIO,
        *,
        unicode: bool = False,
        jp: bool = False,
        allow_page_split: bool = False,
        force_no_wrap: bool = False,
    ):
        lines: list[str] = []
        line: str = ""
        width: int = 0
        while True:
            # 处理翻页
            if len(lines) >= PAGE_LINES:
                stream.seek(stream.tell() - len(line))
                break
            # 读取字符
            char = stream.read(1)
            if char == "":  # 流结束
                if line:
                    lines.append(line)
                break
            # 处理换行符
            if char == "\r":  # 忽略 \r
                line += char
                continue
            if char == "\n":
                lines.append(line + "\n")
                line = ""
                width = 0
                continue
            # 处理字符
            char_width = calc_char_width(char, unicode, jp)
            # 单个空格在末尾不换行
            if char == " " and line and line[-1] != " ":
                line += char
                width += char_width
                continue
            # 处理换行 折行
            if width + char_width > PAGE_WIDTH:
                pos = line.rfind(" ")
                # 找不到空格, 换行
                if pos == -1:
                    lines.append(line)
                    line = char
                    width = char_width
                    continue
                # 折行，但(允许书页分隔单词且在最后一行)或者强制不折行
                if allow_page_split and len(lines) + 1 >= PAGE_LINES or force_no_wrap:
                    lines.append(line)
                    line = char
                    width = char_width
                    continue
                #  折行
                lines.append(line[: pos + 1])
                line = line[pos + 1 :] + char
                # 重新计算宽度
                width = 0
                for c in line:
                    char_width = calc_char_width(c, unicode, jp)
                    width += char_width
                continue
            line += char
            width += char_width
        return cls(
            lines,
            unicode=unicode,
            jp=jp,
            allow_page_split=allow_page_split,
            force_no_wrap=force_no_wrap,
        )

    def __str__(self):
        return "<Page\n" + "\n".join([line.removesuffix("\n") for line in self.lines]) + "\n>"

    def origin_text(self):
        return "".join(self.lines)

    def text(self):
        return "".join(self.processed_lines())

    def processed_lines(self):  # 统一使用 LF
        return [line.replace("\r\n", "\n") for line in self.lines]

    def to_nbt(self, *, text_component: bool = True, filter: bool = False) -> nbtlib.Compound | nbtlib.String:
        if self.force_no_wrap:
            text = "".join([line.removesuffix("\n") + "\n" for line in self.processed_lines()])
        else:
            text = self.text()
        if text_component:
            nbt = nbtlib.String(json.dumps({"text": text}, ensure_ascii=False))
        else:
            nbt = nbtlib.String(text.replace("\n", "\\n"))  # 并没有什么用, 不用TextComponent换不了行
        if filter:
            return nbtlib.Compound({"raw": nbt})
        else:
            return nbt
