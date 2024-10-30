from typing import Optional, Self

from .text_component import ClickEvent, HoverEvent, TextComponent


class Style:
    def __init__(self):
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

    def __repr__(self) -> str:
        value_dict = {
            "color": self.color,
            "font": self.font,
            "bold": self.bold,
            "italic": self.italic,
            "underlined": self.underlined,
            "strikethrough": self.strikethrough,
            "obfuscated": self.obfuscated,
            "insertion": self.insertion,
            "click_event": self.click_event,
            "hover_event": self.hover_event,
        }
        return "Style(" + ", ".join([f"{key}={value}" for key, value in value_dict.items() if value is not None]) + ")"

    def clone(self) -> "Style":
        result = Style()
        result.color = self.color
        result.font = self.font
        result.bold = self.bold
        result.italic = self.italic
        result.underlined = self.underlined
        result.strikethrough = self.strikethrough
        result.obfuscated = self.obfuscated
        result.insertion = self.insertion
        result.click_event = self.click_event
        result.hover_event = self.hover_event
        return result

    def cover(self, other: "Style"):
        result = Style()
        result.color = other.color if other.color is not None else self.color
        result.font = other.font if other.font is not None else self.font
        result.bold = other.bold if other.bold is not None else self.bold
        result.italic = other.italic if other.italic is not None else self.italic
        result.underlined = other.underlined if other.underlined is not None else self.underlined
        result.strikethrough = other.strikethrough if other.strikethrough is not None else self.strikethrough
        result.obfuscated = other.obfuscated if other.obfuscated is not None else self.obfuscated
        self.insertion = other.insertion if other.insertion is not None else self.insertion
        result.click_event = other.click_event if other.click_event is not None else self.click_event
        result.hover_event = other.hover_event if other.hover_event is not None else self.hover_event
        return result

    def apply_to_component(self, component: TextComponent, force: bool = False):
        component._color = self.color if self.color is not None or force else component._color
        component._font = self.font if self.font is not None or force else component._font
        component._bold = self.bold if self.bold is not None or force else component._bold
        component._italic = self.italic if self.italic is not None or force else component._italic
        component._underlined = self.underlined if self.underlined is not None or force else component._underlined
        component._strikethrough = self.strikethrough if self.strikethrough is not None or force else component._strikethrough
        component._obfuscated = self.obfuscated if self.obfuscated is not None or force else component._obfuscated
        component._insertion = self.insertion if self.insertion is not None or force else component._insertion
        component._click_event = self.click_event if self.click_event is not None or force else component._click_event
        component._hover_event = self.hover_event if self.hover_event is not None or force else component._hover_event

    @classmethod
    def from_component(cls, component: TextComponent) -> Self:
        result = cls()
        result.color = component._color
        result.font = component._font
        result.bold = component._bold
        result.italic = component._italic
        result.underlined = component._underlined
        result.strikethrough = component._strikethrough
        result.obfuscated = component._obfuscated
        result.insertion = component._insertion
        result.click_event = component._click_event
        result.hover_event = component._hover_event
        return result
