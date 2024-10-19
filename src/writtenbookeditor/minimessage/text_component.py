import json
from dataclasses import dataclass
from typing import Union, Optional, Literal, Sequence


TextType = Literal["text", "translatable", "score", "selector", "keybind", "nbt"]

ClickEventActions = Literal["open_url", "open_file", "run_command", "suggest_command", "change_page", "copy_to_clipboard"]


@dataclass
class ClickEvent:
    action: ClickEventActions
    value: str


HoverEventActions = Literal["show_text", "show_item", "show_entity"]


@dataclass
class HoverEvent:
    action: HoverEventActions
    # contents: "TextComponentType" # 为支持全部版本，使用旧版的的 value 而非较新的 contents
    value: Union["TextComponentType", str]


@dataclass
class Score:
    name: str
    objective: str


TextComponentType = Union[str, "TextComponent", list["TextComponentType"]]


class TextComponent:
    def __init__(self, text: Optional[str] = None):
        self.type: TextType = "text"
        # style
        self.color: Optional[str] = None
        self.font: Optional[str] = None
        self.bold: Optional[bool] = None
        self.italic: Optional[bool] = None
        self.underlined: Optional[bool] = None
        self.strikethrough: Optional[bool] = None
        self.obfuscated: Optional[bool] = None
        self.insertion: Optional[str] = None
        self.click_event: Optional[ClickEvent] = None
        self.hover_event: Optional[HoverEvent] = None
        self.extra: Optional[list[TextComponentType]] = None
        # text
        self.text: Optional[str] = text
        # translatable
        self.translate: Optional[str] = None
        self.fallback: Optional[str] = None
        self.with_: Optional[Sequence[TextComponentType]] = None
        # score
        self.score: Optional[Score] = None
        # selector
        self.selector: Optional[str] = None
        self.separator: Optional[TextComponentType] = None
        # keybind
        self.keybind: Optional[str] = None
        # nbt
        self.source: Optional[Literal["block", "entity", "storage"]] = None
        self.nbt: Optional[str] = None
        self.interpret: Optional[bool] = None
        self.separator: Optional[TextComponentType] = None
        self.block: Optional[str] = None
        self.entity: Optional[str] = None
        self.storage: Optional[str] = None

    def __str__(self):
        return self.to_string()

    def to_string(self):
        result = self.to_dict()
        return json.dumps(result)

    def to_dict(self):
        generic_dict = {
            "color": self.color,
            "font": self.font,
            "bold": self.bold,
            "italic": self.italic,
            "underlined": self.underlined,
            "strikethrough": self.strikethrough,
            "obfuscated": self.obfuscated,
            "insertion": self.insertion,
            "click_event": {"action": self.click_event.action, "value": self.click_event.value} if self.click_event is not None else None,
            "hover_event": (
                {
                    "action": self.hover_event.action,
                    "value": text_component_type_to_json(self.hover_event.value),
                }
                if self.hover_event is not None
                else None
            ),
            "extra": self.extra,
        }
        if self.type == "text":
            if self.text is None:
                raise ValueError("text is None")
            value = {
                "text": self.text,
                **generic_dict,
            }
        elif self.type == "translatable":
            if self.translate is None:
                raise ValueError("translate is None")
            value = {
                "translate": self.translate,
                **generic_dict,
            }
            if self.fallback is not None:
                value["fallback"] = self.fallback
            if self.with_ is not None:
                value["with"] = self.with_
        elif self.type == "score":
            if self.score is None:
                raise ValueError("score is None")
            value = {
                "score": {
                    "name": self.score.name,
                    "objective": self.score.objective,
                },
                **generic_dict,
            }
        elif self.type == "selector":
            if self.selector is None:
                raise ValueError("selector is None")
            value = {
                "selector": self.selector,
                **generic_dict,
            }
            if self.separator is not None:
                value["separator"] = self.separator
        elif self.type == "keybind":
            if self.keybind is None:
                raise ValueError("keybind is None")
            value = {
                "keybind": self.keybind,
                **generic_dict,
            }
        elif self.type == "nbt":
            if self.nbt is None:
                raise ValueError("nbt is None")
            if self.block is None and self.entity is None and self.storage is None:
                raise ValueError("block, entity, and storage are all None")
            value = {
                "nbt": self.nbt,
                **generic_dict,
            }
            value["score"] = self.score
            value["interpret"] = self.interpret
            value["separator"] = self.separator
            value["block"] = self.block
            value["entity"] = self.entity
            value["storage"] = self.storage
        else:
            raise ValueError(f"unknown type: {self.type}")
        result = {k: v for k, v in value.items() if v is not None}
        return result


def text_component_type_to_text_component(value: TextComponentType) -> TextComponent:
    if isinstance(value, str):
        return TextComponent(value)
    elif isinstance(value, TextComponent):
        return value
    elif isinstance(value, list):
        if len(value) < 1:
            return TextComponent()
        result = text_component_type_to_text_component(value[0])
        result.extra = [text_component_type_to_text_component(v) for v in value[1:]]
        return result


def text_component_type_to_json(value: TextComponentType) -> dict | list | str:
    if isinstance(value, str):
        return value
    elif isinstance(value, TextComponent):
        return value.to_dict()
    elif isinstance(value, list):
        return [text_component_type_to_json(v) for v in value]
