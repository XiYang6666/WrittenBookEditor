import re
from dataclasses import dataclass
from typing import Optional, Literal, Callable

import nbtlib

from .style import Style
from .segment import TextSegment, TextSegmentSequence
from .text_component import ClickEvent, HoverEvent, Score, TextComponent
from ..util.color import parse_color, hsl_to_rgb, rgb_to_hex, validate_color, interpolate_colors
from ..util.json_util import remove_dict_none_value


# text


def unescape_text(text: str) -> str:
    return text.replace(r"\<", "<")


def parse_string(arg: str) -> str:
    arg = arg.strip()
    if arg.startswith('"') and arg.endswith('"'):
        return arg[1:-1].replace('"', '"')
    elif arg.startswith("'") and arg.endswith("'"):
        return arg[1:-1].replace("'", "'")
    else:
        return arg


def parse_int(arg: str) -> Optional[int]:
    if re.match(r"^[+-]?\d+$", arg):
        return int(arg)
    else:
        return None


def parse_float(arg: str) -> Optional[float]:
    if re.match(r"^[+-]?(\d+(\.\d*)?|\.\d+)$", arg):
        return float(arg)


# tag

double_tags = (
    "color",
    "bold",
    "b",
    "italic",
    "em",
    "i",
    "underlined",
    "u",
    "strikethrough",
    "st",
    "obfuscated",
    "obf",
    "click",
    "hover",
    "insertion",
    "rainbow",
    "gradient",
    "transition",
    "font",
)

single_tags = (
    "keybind",
    "lang",
    "tr" "translate",
    "newline",
    "br",
    "selector",
    "sel",
    "score",
    "nbt",
)

ext_tags = (
    "rainbow",
    "gradient",
    "transition",
)

control_tags = ("reset",)


@dataclass
class TagInfo:
    name: str
    is_end: bool
    is_single: bool
    args: list[str]


def parse_tag(tag: str) -> Optional[TagInfo]:
    if not tag.endswith(">"):
        return None
    tag = tag.removesuffix(">")
    if tag.startswith("</"):
        is_end = True
        tag = tag.removeprefix("</")
    elif tag.startswith("<"):
        is_end = False
        tag = tag.removeprefix("<")
    else:
        return None
    if tag.endswith("/"):
        tag = tag.removesuffix("/")
        is_single = True
    else:
        is_single = False
    if is_end and is_single:
        return None
    split_result = tag.split(":")
    name = split_result[0].lower()
    args = split_result[1:]
    if is_end and args:  # 闭标签不能有参数
        return None
    return TagInfo(name, is_end, is_single, args)


def parse_double_tag(tag_info: TagInfo) -> Optional[Style]:
    result = Style()
    if tag_info.name in ("bold", "b", "italic", "em", "i", "underlined", "u", "strikethrough", "st", "obfuscated", "obf") and len(tag_info.args) != 0:
        return None
    # color
    if validate_color(tag_info.name):
        result.color = tag_info.name
    if tag_info.name == "color":
        if len(tag_info.args) != 1:
            return None
        if not validate_color(tag_info.args[0]):
            return None
        result.color = tag_info.args[0]
    # decorations
    elif tag_info.name in ("bold", "b"):
        result.bold = True
    elif tag_info.name in ("italic", "em", "i"):
        result.italic = True
    elif tag_info.name in ("underlined", "u"):
        result.underlined = True
    elif tag_info.name in ("strikethrough", "st"):
        result.strikethrough = True
    elif tag_info.name in ("obfuscated", "obf"):
        result.obfuscated = True
    # click
    elif tag_info.name == "click":
        if len(tag_info.args) != 2:
            return None
        action, value = tag_info.args
        value = parse_string(value)  # TODO: 要处理 MiniMessage
        if action not in ("open_url", "open_file", "run_command", "change_page", "copy_to_clipboard", "suggest_command"):
            return None
        result.click_event = ClickEvent(action=action, value=value)
    # hover
    elif tag_info.name == "hover":  # TODO: 有问题 (https://docs.advntr.dev/minimessage/format.html#hover)
        if len(tag_info.args) < 2:
            return None
        action = tag_info.args[0]
        if action == "show_text":
            if len(tag_info.args) != 2:
                return None
            value: str = parse_string(tag_info.args[1])  # TODO: 要处理 MiniMessage
        elif action == "show_item":
            type = tag_info.args[1]
            if len(tag_info.args) > 4:
                return None
            count = parse_int(tag_info.args[2]) if len(tag_info.args) >= 3 else 1
            tag = parse_string(tag_info.args[3]) if len(tag_info.args) == 4 else nbtlib.Compound()
            value = nbtlib.Compound({"id": type, "Count": count, "tag": tag}).snbt()
        elif action == "show_entity":
            if not 3 <= len(tag_info.args) <= 4:
                return None
            type = tag_info.args[1]
            uuid = tag_info.args[2]
            name = parse_string(tag_info.args[3]) if len(tag_info.args) == 4 else None
            json_data = remove_dict_none_value({"name": name, "type": type, "id": uuid})
            value = nbtlib.Compound(json_data).snbt()
        if action not in ("show_text", "show_item", "show_entity"):
            return None

        value = parse_string(value)  # TODO: 要处理 MiniMessage
        result.hover_event = HoverEvent(action=action, value=value)
    # insertion
    elif tag_info.name == "insertion":
        if len(tag_info.args) != 1:
            return None
        result.insertion = tag_info.args[0]
    # font(unsupported style)
    elif tag_info.name == "font":
        pass
    # unsupported tag
    else:
        return None
    return result


def parse_single_tag(tag_info: TagInfo) -> Optional[TextComponent]:
    result = TextComponent()
    # keybind(single tag)
    if tag_info.name == "keybind":
        if len(tag_info.args) != 1:
            return None
        result.type = "keybind"
        result._keybind = tag_info.args[0]
    # translatable(single tag)
    elif tag_info.name in ("lang", "tr", "translate"):
        if len(tag_info.args) < 1:
            return None
        result.type = "translatable"
        result._translate = tag_info.args[0]
        with_ = [parse_string(i) for i in tag_info.args[1:]]  # TODO: 要处理 MiniMessage
        if with_:
            result._with = with_
    # newline(single tag)
    elif tag_info.name in ("newline", "br"):
        if len(tag_info.args) != 0:
            return None
        result.type = "text"
        result._text = "\n"
    # selector(single tag) (unsupported component)
    elif tag_info.name == "score":
        if len(tag_info.args) != 2:
            return None
        result.type = "score"
        result._score = Score(tag_info.args[0], tag_info.args[1])
    # nbt(single tag)
    elif tag_info.name == "nbt":
        if not (3 <= len(tag_info.args) <= 5):
            return None
        result.type = "nbt"
        source = tag_info.args[0]
        id = parse_string(tag_info.args[1])
        path = tag_info.args[2]
        separator = tag_info.args[3] if len(tag_info.args) >= 4 else None
        interpret = tag_info.args[4] if len(tag_info.args) == 5 else None
        if source == "block":
            result._block = id
        elif source == "entity":
            result._entity = id
        elif source == "storage":
            result._storage = id
        result._nbt = path
        result._separator = separator
        result._interpret = interpret == "true"
    else:
        return None
    return result


def get_tag_type(tag_info: TagInfo) -> Literal["double", "single", "control", None]:
    if validate_color(tag_info.name):
        return "double"
    elif tag_info.name in single_tags:
        return "single"
    elif tag_info.name in control_tags:
        return "control"
    return None


def validate_ext_tag(tag_info: TagInfo) -> bool:
    if tag_info.name == "rainbow":
        return bool(len(tag_info.args) == 0 or (len(tag_info.args) == 1 and re.match(r"^!?[0-9]*$", tag_info.args[0])))
    elif tag_info.name in ("gradient", "transition"):
        if len(tag_info.args) < 2:
            return False
        for i, arg in enumerate(tag_info.args):
            if validate_color(arg):
                continue
            elif (
                i == len(tag_info.args) - 1
                and re.match(r"^[+-]?([0-9]+(\.[0-9]*)?|\.[0-9]+)$", tag_info.args[-1])
                and -1 <= float(tag_info.args[-1]) <= 1
            ):
                continue
            else:
                return False
        return True
    else:
        return False


# minimessage


@dataclass
class ParseContentResult:
    segments: TextSegmentSequence
    not_covered_text_segments: TextSegmentSequence
    end_pos: int
    return_level: int = 0


def process_ext_tags(
    tag_info: Optional[TagInfo], original_text: str, segments: TextSegmentSequence, not_covered_text_segments: TextSegmentSequence
) -> TextSegmentSequence:
    print("segments", segments, "not_covered_text_segments", not_covered_text_segments)
    if not tag_info or not segments or not not_covered_text_segments:
        return segments

    def process_gradient_like(color_callback: Callable[[int, int], str]) -> TextSegmentSequence:
        result: TextSegmentSequence = []
        start_pos = segments[0].start
        end_pos = segments[-1].end
        size = end_pos - start_pos
        for segment in segments:
            if segment.type == "text":
                size -= original_text[segment.start : segment.end].count("\\<")
            else:
                size -= segment.end - segment.start
        current_segment_index = 0
        offset = 0

        for segment in not_covered_text_segments:
            current_segment = segments[current_segment_index]
            while segment != current_segment:
                result.append(current_segment)
                if current_segment.type != "text":
                    offset += current_segment.end - current_segment.start
                current_segment_index += 1
                current_segment = segments[current_segment_index]
                continue
            pos = segment.start
            while segment.start <= pos < segment.end:
                relative_pos = pos - start_pos - offset
                color = color_callback(relative_pos, size)
                style = Style()
                style.color = color
                style = segment.style.cover(style)
                if original_text.startswith("\\<", pos):
                    result.append(TextSegment.text(pos, pos + 2, style))
                    offset += 1
                    pos += 2
                else:
                    result.append(TextSegment.text(pos, pos + 1, style))
                    pos += 1
            current_segment_index += 1
        return result

    if tag_info.name == "rainbow":
        if len(tag_info.args) < 1:
            reverse = False
            phase = 0
        else:
            arg = tag_info.args[0]
            reverse = arg.startswith("!")
            arg = arg.removeprefix("!")
            phase = parse_int(arg)
            if phase is None and arg != "":  # 参数错误, 跳过
                return segments
            phase = phase or 0

            def rainbow_color_callback(relative_pos: int, size: int) -> str:
                if reverse:
                    color_index = size - relative_pos
                else:
                    color_index = relative_pos
                hue = (color_index / size + phase / 10) % 1
                return rgb_to_hex(*hsl_to_rgb(hue, 1, 1))

            return process_gradient_like(rainbow_color_callback)
    elif tag_info.name == "gradient":
        if len(tag_info.args) < 2:
            return segments
        if len(tag_info.args) >= 3 and (phase := parse_float(tag_info.args[-1])) is not None:
            colors = [parse_color(i) for i in tag_info.args[:-1]]
        else:
            colors = [parse_color(i) for i in tag_info.args]
        if None in colors:  # 颜色解析错误, 跳过
            return segments
        phase = abs(phase or 0)
        if phase > 1:
            return segments

        def gradient_color_callback(relative_pos: int, size: int) -> str:
            ratio = relative_pos / size
            color = interpolate_colors(colors, ratio)  # type: ignore
            return rgb_to_hex(*color)

        return process_gradient_like(gradient_color_callback)
    elif tag_info.name == "transition":
        if len(tag_info.args) < 2:
            return segments
        if len(tag_info.args) >= 3 and (phase := parse_float(tag_info.args[-1])) is not None:
            colors = [parse_color(i) for i in tag_info.args[:-1]]
        else:
            colors = [parse_color(i) for i in tag_info.args]
        if None in colors:  # 颜色解析错误, 跳过
            return segments
        phase = abs(phase or 0)
        color = interpolate_colors(colors, phase)  # type: ignore
        style = Style()
        style.color = rgb_to_hex(*color)
        result = [
            TextSegment(
                segment.type,
                segment.start,
                segment.end,
                segment.style.cover(style),
                segment.text_component,
            )
            for segment in segments
        ]
        return result
    return segments


def parse_minimessage(origin_text: str) -> TextSegmentSequence:
    result = parse_content(origin_text, 0, [], Style())
    return result.segments


def parse_content(original_text: str, pos: int, tag_stack: list[TagInfo], style: Style) -> ParseContentResult:
    print("--> tag_stack", [i.name for i in tag_stack])
    current_tag = tag_stack[-1] if tag_stack else None
    result: TextSegmentSequence = []
    not_covered_text_segments: TextSegmentSequence = []
    not_covered = True
    string_start = pos
    string_end = pos
    pos = pos
    while pos < len(original_text):
        # parse escape
        if original_text.startswith(r"\<", pos):
            pos += 2
            continue
        # parse tag
        if original_text.startswith("<", pos):
            # 处理标签
            tag_start = pos
            pos += 1
            in_quote = False
            quote = None
            while pos < len(original_text):
                if in_quote and quote and original_text.startswith(rf"\{quote}", pos):
                    pos += 2
                    continue
                if in_quote and original_text[pos] == quote:
                    in_quote = False
                    quote = None
                    pos += 1
                    continue
                if original_text[pos] == '"' and quote is None:
                    quote = '"'
                    in_quote = True
                    pos += 1
                    continue
                if original_text[pos] == "'" and quote is None:
                    quote = "'"
                    in_quote = True
                    pos += 1
                    continue
                if original_text[pos] == ">" and not in_quote:
                    pos += 1
                    break
                pos += 1
            if in_quote:  # 标签未闭合, 无法解析, 跳过
                continue
            tag_end = pos
            tag_content = original_text[tag_start:tag_end]
            tag_info = parse_tag(tag_content)
            if tag_info is None:  # 无法解析标签, 跳过
                continue
            # 闭标签
            if tag_info.is_end:
                # 从后往前遍历标签栈, 找到匹配的开始标签
                for i, stack_tag_info in enumerate(tag_stack[::-1]):
                    if stack_tag_info.name != tag_info.name:
                        continue
                    # 闭标签与当前标签匹配, 结束标签
                    string_end = tag_start
                    text_seg = TextSegment.text(string_start, string_end, style)
                    if string_end != string_start:
                        result.append(text_seg)
                    if string_end != string_start and not_covered:
                        not_covered_text_segments.append(text_seg)
                    result.append(TextSegment.end_tag(tag_start, tag_end))
                    return ParseContentResult(
                        process_ext_tags(current_tag, original_text, result, not_covered_text_segments),
                        not_covered_text_segments,
                        pos,
                        i,
                    )
                else:  # 未找到匹配的开始标签, 不匹配, 跳过, 当做字符串
                    print("no match tag, skip")
                    continue
            # 开标签
            if not tag_info.is_end:
                tag_type = get_tag_type(tag_info)
                if tag_type == "single" or tag_info.is_single:
                    # 单标签, 直接处理
                    parse_result = parse_single_tag(tag_info)
                    if parse_result is None:
                        # 无法解析单标签, 跳过
                        continue
                    string_end = tag_start
                    text_seg = TextSegment.text(string_start, string_end, style)
                    if string_end != string_start:
                        result.append(text_seg)
                    if string_end != string_start and not_covered:
                        not_covered_text_segments.append(text_seg)
                    string_start = tag_end
                    string_end = tag_end
                    result.append(TextSegment.single_tag(tag_start, tag_end, style, parse_result))
                    continue
                elif tag_type == "double":
                    # 双标签, 递归处理
                    string_end = tag_start
                    text_seg = TextSegment.text(string_start, string_end, style)
                    if string_end != string_start:
                        result.append(text_seg)
                    if string_end != string_start and not_covered:
                        not_covered_text_segments.append(text_seg)
                    result.append(TextSegment.start_tag(tag_start, tag_end))
                    # 解析样式
                    sub_style = parse_double_tag(tag_info)
                    if sub_style is None and tag_info.name not in ext_tags:  # 格式错误的标签, 跳过
                        continue
                    sub_style = style.cover(sub_style) if sub_style is not None else style
                    # 递归内容
                    print("--> open tag, tag: ", tag_info.name, "style: ", style, "sub_style: ", sub_style)
                    parse_result = parse_content(original_text, tag_end, tag_stack + [tag_info], sub_style)
                    # 更新数据
                    pos = parse_result.end_pos
                    string_start = pos
                    string_end = pos
                    result += parse_result.segments
                    if (sub_style and sub_style.color) is None:
                        not_covered_text_segments += parse_result.not_covered_text_segments
                    # 返回多层
                    if parse_result.return_level > 0:
                        print("<-- return level", parse_result.return_level, "tag: ", current_tag and current_tag.name)
                        return ParseContentResult(
                            process_ext_tags(current_tag, original_text, result, not_covered_text_segments),
                            not_covered_text_segments,
                            pos,
                            parse_result.return_level - 1,
                        )
                    continue
                elif tag_type == "control" and tag_info.name == "reset":
                    # 控制标签
                    string_end = tag_start
                    text_seg = TextSegment.text(string_start, string_end, style)
                    if string_end != string_start:
                        result.append(text_seg)
                    if string_end != string_start and not_covered:
                        not_covered_text_segments.append(text_seg)
                    string_start = tag_end
                    string_end = tag_end
                    result.append(TextSegment.single_tag(tag_start, tag_end))
                    style = Style()
                    not_covered = False
                    continue
                else:
                    # 无法识别标签类型, 跳过
                    continue
        # 其他字符
        pos += 1
        string_end = pos + 1
    # 结束标签未闭合, 处理剩余字符串
    pos = min(pos, len(original_text))
    text_seg = TextSegment.text(string_start, string_end, style)
    if string_end != string_start:
        result.append(text_seg)
    if string_end != string_start and not_covered:
        not_covered_text_segments.append(text_seg)
    return ParseContentResult(
        process_ext_tags(current_tag, original_text, result, not_covered_text_segments),
        not_covered_text_segments,
        pos,
        0,
    )
