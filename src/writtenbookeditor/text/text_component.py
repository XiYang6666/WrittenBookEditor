import json
from dataclasses import dataclass
from typing import Union, Optional, Literal, Sequence, Self

from ..util.json_util import JsonSerializable, remove_dict_false_value, remove_dict_none_value


# types

ClickEventAction = Literal["open_url", "open_file", "run_command", "suggest_command", "change_page", "copy_to_clipboard"]
HoverEventAction = Literal["show_text", "show_item", "show_entity"]


@dataclass
class ClickEvent:
    action: ClickEventAction
    value: str

    def to_json_serializable(self) -> "JsonSerializable":
        return {"action": self.action, "value": self.value}


@dataclass
class HoverEvent:
    action: HoverEventAction
    # contents: "TextComponentType"  # 懒得写除了 show_text 以外的类型了, 反正 minimessage 只用 value, 不如注释了, (https://zh.minecraft.wiki/w/文本组件#悬停事件)
    value: Union["TextComponentLike", str]

    def to_json_serializable(self) -> "JsonSerializable":
        return {
            "action": self.action,
            "value": text_component_like_to_json_serializable(self.value) if self.action == "show_text" else self.value,
        }


@dataclass
class Score:
    name: str
    objective: str
    value: Optional[str] = None

    def to_json_serializable(self) -> "JsonSerializable":
        return {
            "name": self.name,
            "objective": self.objective,
            "value": self.value,
        }


# text component

TextComponentType = Literal["text", "translatable", "score", "selector", "keybind", "nbt"]

TextComponentLike = Union[str, "TextComponent", Sequence["TextComponentLike"]]


class TextComponent:
    def __init__(self):
        self.type: TextComponentType = "text"
        # style
        self._color: Optional[str] = None
        self._font: Optional[str] = None
        self._bold: Optional[bool] = None
        self._italic: Optional[bool] = None
        self._underlined: Optional[bool] = None
        self._strikethrough: Optional[bool] = None
        self._obfuscated: Optional[bool] = None
        self._insertion: Optional[str] = None
        self._click_event: Optional[ClickEvent] = None
        self._hover_event: Optional[HoverEvent] = None
        # self.extra: Optional[list["TextComponentType"]] = None  # 用不上, 懒得写, 注释了
        # text
        self._text: Optional[str] = None
        # translatable
        self._translate: Optional[str] = None
        self._fallback: Optional[str] = None
        self._with: Optional[Sequence[TextComponentLike]] = None
        # score
        self._score: Optional[Score] = None
        # selector
        self._selector: Optional[str] = None
        self._separator: Optional[TextComponentLike] = None
        # keybind
        self._keybind: Optional[str] = None
        # nbt
        self._source: Optional[Literal["block", "entity", "storage"]] = None
        self._nbt: Optional[str] = None
        self._interpret: Optional[bool] = None
        self._separator: Optional[TextComponentLike] = None
        self._block: Optional[str] = None
        self._entity: Optional[str] = None
        self._storage: Optional[str] = None

    def __repr__(self) -> str:
        return f"TextComponent({self.to_string()})"

    def clone(self) -> "TextComponent":
        result = TextComponent()
        result.type = self.type
        result._color = self._color
        result._font = self._font
        result._bold = self._bold
        result._italic = self._italic
        result._underlined = self._underlined
        result._strikethrough = self._strikethrough
        result._obfuscated = self._obfuscated
        result._insertion = self._insertion
        result._click_event = self._click_event
        result._hover_event = self._hover_event
        # text
        result._text = self._text
        # translatable
        result._translate = self._translate
        result._fallback = self._fallback
        result._with = self._with
        # score
        result._score = self._score
        # selector
        result._selector = self._selector
        result._separator = self._separator
        # keybind
        result._keybind = self._keybind
        # nbt
        result._source = self._source
        result._nbt = self._nbt
        result._interpret = self._interpret
        result._separator = self._separator
        result._block = self._block
        result._entity = self._entity
        result._storage = self._storage
        return result

    def placeholder_str(self) -> str:
        if self.type == "text":
            assert self._text is not None
            return self._text
        elif self.type == "translatable":
            assert self._translate is not None
            return self._translate
        elif self.type == "score":
            return "[score]"
        elif self.type == "selector":
            return "[selector]"
        elif self.type == "keybind":
            return "[keybind]"
        elif self.type == "nbt":
            return "[nbt]"
        else:
            raise ValueError(f"Invalid type: {self.type}")

    def to_string(self):
        result = self.to_json_serializable()
        return json.dumps(result)

    def to_json_serializable(self) -> "JsonSerializable":
        style_dict = {
            "color": self._color,
            "font": self._font,
            "bold": self._bold,
            "italic": self._italic,
            "underlined": self._underlined,
            "strikethrough": self._strikethrough,
            "obfuscated": self._obfuscated,
            "click_event": self._click_event and self._click_event.to_json_serializable(),
            "hover_event": self._hover_event and self._hover_event.to_json_serializable(),
        }
        style_dict = remove_dict_false_value(style_dict)

        if self.type == "text":
            assert self._text is not None
            result = {
                "text": self._text,
                **style_dict,
            }
        elif self.type == "translatable":
            assert self._translate is not None
            result = {
                "translate": self._translate,
                "fallback": self._fallback,
                "with": self._with,
                **style_dict,
            }
        elif self.type == "score":
            assert self._score is not None
            result = {
                "score": self._score.to_json_serializable(),
                **style_dict,
            }
        elif self.type == "selector":
            assert self._selector is not None
            result = {
                "selector": self._selector,
                "separator": self._separator,
                **style_dict,
            }
        elif self.type == "keybind":
            assert self._keybind is not None
            result = {
                "keybind": self._keybind,
                **style_dict,
            }
        elif self.type == "nbt":
            assert self._nbt is not None
            result = {
                "nbt": self._nbt,
                "source": self._source,
                "separator": self._separator,
                "block": self._block,
                "entity": self._entity,
                "storage": self._storage,
                **style_dict,
            }
        else:
            raise ValueError(f"Invalid type: {self.type}")
        return remove_dict_none_value(result)

    @classmethod
    def text(cls, text: str) -> Self:
        result = cls()
        result.type = "text"
        result._text = text
        return result

    @classmethod
    def translatable(
        cls,
        translate: str,
        fallback: Optional[str] = None,
        with_: Optional[Sequence[TextComponentLike]] = None,
    ) -> Self:
        result = cls()
        result.type = "translatable"
        result._translate = translate
        result._fallback = fallback
        result._with = with_
        return result

    @classmethod
    def score(cls, name: str, objective: str, value: Optional[str] = None) -> Self:
        result = cls()
        result.type = "score"
        result._score = Score(name, objective, value)
        return result

    @classmethod
    def selector(cls, selector: str, separator: TextComponentLike) -> Self:
        result = cls()
        result.type = "selector"
        result._selector = selector
        result._separator = separator
        return result

    @classmethod
    def keybind(cls, keybind: str) -> Self:
        result = cls()
        result.type = "keybind"
        result._keybind = keybind
        return result

    @classmethod
    def nbt(
        cls,
        nbt: str,
        source: Literal["block", "entity", "storage"],
        separator: TextComponentLike,
        block: Optional[str] = None,
        entity: Optional[str] = None,
        storage: Optional[str] = None,
    ) -> Self:
        result = cls()
        result.type = "nbt"
        result._nbt = nbt
        result._source = source
        result._separator = separator
        result._block = block
        result._entity = entity
        result._storage = storage
        return result


def text_component_like_to_json_serializable(value: TextComponentLike) -> JsonSerializable:
    if isinstance(value, str):
        return value
    elif isinstance(value, TextComponent):
        return value.to_json_serializable()
    elif isinstance(value, list):
        return [text_component_like_to_json_serializable(v) for v in value]
