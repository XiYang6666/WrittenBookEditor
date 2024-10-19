import re
from typing import Optional, Literal
from dataclasses import dataclass

from .style import Style
from .text_component import ClickEvent, HoverEvent, Score, TextComponent


@dataclass
class TagInfo:
    name: str
    is_end: bool
    is_single: bool
    args: list[str]


color_name = (
    "black",
    "dark_blue",
    "dark_green",
    "dark_aqua",
    "dark_red",
    "dark_purple",
    "gold",
    "gray",
    "dark_gray",
    "blue",
    "green",
    "aqua",
    "red",
    "light_purple",
    "yellow",
    "white",
)

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

control_tags = ("reset",)


def parse_tag(tag: str) -> Optional[TagInfo]:
    if not tag.endswith(">"):
        return None
    tag.removesuffix(">")
    if tag.startswith("</"):
        is_end = True
        tag.removeprefix("</")
    elif tag.startswith("<"):
        is_end = False
        tag.removeprefix("<")
    else:
        return None
    if tag.endswith("/"):
        tag.removesuffix("/")
        is_single = True
    else:
        is_single = False
    if is_end and is_single:
        return None
    split_result = tag.split(":")
    name = split_result[0].lower()
    return TagInfo(name, is_end, is_single, split_result[1:])


def parse_double_tag(tag_info: TagInfo) -> Style:
    result = Style()
    # color
    if tag_info.name in color_name or re.match(r"#[0-9a-fA-F]{6}", tag_info.name):
        result.color = tag_info.name
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
            return result
        action, value = tag_info.args

        if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
            value = value[1:-1]
        if action not in ("open_url", "open_file", "run_command", "suggest_command", "change_page", "copy_to_clipboard"):
            return result
        result.click_event = ClickEvent(action=action, value=value)
    # hover
    elif tag_info.name == "hover":
        if len(tag_info.args) != 2:
            return result
        action, value = tag_info.args
        if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
            value = value[1:-1]
        if action not in ("show_text", "show_item", "show_entity"):
            return result
        result.hover_event = HoverEvent(action=action, value=value)
    # insertion
    elif tag_info.name == "insertion":
        if len(tag_info.args) != 1:
            return result
        result.insertion = tag_info.args[0]
    # rainbow(ext style)
    elif tag_info.name == "rainbow":
        if len(tag_info.args) != 1:
            return result
        reverse = tag_info.args[0].startswith("!")
        phase = int(tag_info.args[0][1:] if reverse else tag_info.args[0])
        result.color_mode = "rainbow"
        result.rainbow_reverse = reverse
        result.rainbow_phase = phase
    # gradient(ext style)
    elif tag_info.name == "gradient":
        if len(tag_info.args) < 2:
            return result
        if len(tag_info.args) > 3 and re.match(r"[0-9]+", tag_info.args[-1]):
            result.gradient_phase = int(tag_info.args[-1])
            result.gradient_colors = tag_info.args[:-1]
        else:
            result.gradient_colors = tag_info.args
        result.color_mode = "gradient"
    # transition(ext style)
    elif tag_info.name == "transition":
        if len(tag_info.args) < 1:
            return result
        if len(tag_info.args) > 1 and re.match(r"[0-9]+", tag_info.args[-1]):
            result.transition_phase = int(tag_info.args[-1])
            result.transition_colors = tag_info.args[:-1]
        else:
            result.transition_colors = tag_info.args
        result.color_mode = "transition"
    # font(unsupported style)
    # unsupported tag
    return result


def parse_single_tag(tag_info: TagInfo) -> Optional[TextComponent]:
    result = TextComponent()
    # reset(single tag & control tag)
    # keybind(single tag)
    if tag_info.name == "keybind":
        if len(tag_info.args) != 1:
            return None
        result.type = "keybind"
        result.keybind = tag_info.args[0]
    # translatable(single tag)
    elif tag_info.name in ("lang", "tr", "translate"):
        if len(tag_info.args) < 1:
            return None
        result.type = "translatable"
        result.translate = tag_info.args[0]
        with_ = tag_info.args[1:]
        if with_:
            result.with_ = with_
    # newline(single tag)
    elif tag_info.name in ("newline", "br"):
        result.type = "text"
        result.text = "\n"
    # selector(single tag)
    elif tag_info.name in ("selector", "sel"):
        if len(tag_info.args) < 1:
            return None
        result.type = "selector"
        result.selector = tag_info.args[0]
        if len(tag_info.args) >= 2:
            result.separator = tag_info.args[1]
    # score(single tag)
    elif tag_info.name == "score":
        if len(tag_info.args) != 2:
            return None
        result.type = "score"
        result.score = Score(tag_info.args[0], tag_info.args[1])
    # nbt(single tag)
    elif tag_info.name == "nbt":
        if len(tag_info.args) < 3:
            return None
        result.type = "nbt"
        source = tag_info.args[0]
        id = tag_info.args[1]
        path = tag_info.args[2]
        if len(tag_info.args) >= 4:
            separator = tag_info.args[3]
        else:
            separator = None
        if len(tag_info.args) >= 5:
            interpret = tag_info.args[4]
        else:
            interpret = None
        if source == "block":
            result.block = id
        elif source == "entity":
            result.entity = id
        elif source == "storage":
            result.storage = id
        result.nbt = path
        result.separator = separator
        result.interpret = interpret == "true"
    return result


def get_tag_type(tag_info: TagInfo) -> Literal["double", "single", "control", None]:
    if tag_info.name in color_name or re.match(r"#[0-9a-fA-F]{6}", tag_info.name) or tag_info.name in double_tags:
        return "double"
    elif tag_info.name in single_tags:
        return "single"
    elif tag_info.name in control_tags:
        return "control"
    return None
