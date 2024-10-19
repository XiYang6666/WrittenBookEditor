from typing import Optional
from dataclasses import dataclass, field


from .tag import TagInfo, parse_tag, parse_double_tag, parse_single_tag, get_tag_type
from .style import Style, StyleText
from .text_component import TextComponent


@dataclass
class MiniMessageElement:
    name: str
    args: list[str] = field(default_factory=list)
    children: list["MiniMessageElement | str"] = field(default_factory=list)


def parse_minimessage(message: str) -> list[TextComponent]:
    result, _ = parse_content(message, 0, None, Style())
    return [TextComponent()] + result  # 防止继承样式


def parse_content(message: str, pos: int, current_tag: Optional[TagInfo], style: Style) -> tuple[list[TextComponent], int]:
    result: list[TextComponent] = []
    current_string = ""
    pos = pos
    while pos < len(message):
        # parse tag
        if message.startswith("<", pos):
            if current_string:
                result += StyleText(current_string, style).to_components()
                current_string = ""
            end = message.find(">", pos)
            if end == -1:
                # 标签未闭合, 无法解析, 直接当做普通字符串处理
                current_string += message[pos:]
                pos = len(message)
                continue
            tag_content = message[pos : end + 1]
            tag_info = parse_tag(tag_content)
            if tag_info is None:
                # 无法解析标签, 当做普通字符串处理
                current_string += tag_content
                pos = end + 1
                continue
            # 闭标签
            if tag_info.is_end:
                if current_tag is None:
                    # 未匹配到开始标签, 不匹配, 当做普通字符串处理
                    current_string += tag_content
                    pos = end + 1
                    continue
                if current_tag.name != tag_info.name:
                    # 闭标签与当前标签不匹配, 不匹配, 当做普通字符串处理
                    current_string += tag_content
                    pos = end + 1
                    continue
                if len(current_tag.args) < len(tag_info.args):
                    # 闭标签参数比当前标签参数多, 不匹配, 当做普通字符串处理
                    current_string += tag_content
                    pos = end + 1
                    continue
                for i in range(len(tag_info.args)):
                    if current_tag.args[i] != tag_info.args[i]:
                        break
                else:
                    # 闭标签参数与当前标签参数匹配, 结束标签
                    return result, end + 1
                # 闭标签参数与当前标签参数不匹配, 当做普通字符串处理
                current_string += tag_content
                pos = end + 1
                continue
            # 开标签
            if not tag_info.is_end:
                tag_type = get_tag_type(tag_info)
                if tag_type == "single" or tag_info.is_single:
                    # 单标签, 直接处理
                    parse_result = parse_single_tag(tag_info)
                    if parse_result is None:
                        # 无法解析单标签, 当做普通字符串处理
                        current_string += tag_content
                        pos = end + 1
                        continue
                    result.append(parse_result)
                elif tag_type == "double":
                    sub_style = parse_double_tag(tag_info)
                    if sub_style is not None:
                        sub_style = style.cover(sub_style)
                    else:
                        sub_style = style
                    children, pos = parse_content(message, end + 1, tag_info, sub_style)
                    result += children
                elif tag_type == "control":
                    if tag_info.name == "reset":
                        style = Style()
                    else:
                        current_string += tag_content
                        pos = end + 1
                        continue
                else:
                    # 无法识别标签类型, 当做普通字符串处理
                    current_string += tag_content
                    pos = end + 1
                    continue
                pos = end + 1
                continue
        # 其他字符
        current_string += message[pos]
        pos += 1
    if current_string:
        result += StyleText(current_string, style).to_components()
    return result, pos
