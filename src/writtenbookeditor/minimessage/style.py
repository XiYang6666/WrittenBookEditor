import copy
from dataclasses import dataclass
from typing import Optional, Literal

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
        # extra
        self.color_mode: Optional[Literal["rainbow", "gradient", "transition"]] = None
        self.rainbow_reverse: Optional[bool] = None
        self.rainbow_phase: Optional[int] = None
        self.gradient_colors: Optional[list[str]] = None
        self.gradient_phase: Optional[int] = None
        self.transition_colors: Optional[list[str]] = None
        self.transition_phase: Optional[int] = None

    def cover(self, other: "Style"):
        result = copy.deepcopy(self)
        result.color = other.color if other.color is not None else self.color
        result.font = other.font if other.font is not None else self.font
        result.bold = other.bold if other.bold is not None else self.bold
        result.italic = other.italic if other.italic is not None else self.italic
        result.underlined = other.underlined if other.underlined is not None else self.underlined
        result.strikethrough = other.strikethrough if other.strikethrough is not None else self.strikethrough
        result.obfuscated = other.obfuscated if other.obfuscated is not None else self.obfuscated
        result.insertion = other.insertion if other.insertion is not None else self.insertion
        result.click_event = other.click_event if other.click_event is not None else self.click_event
        result.hover_event = other.hover_event if other.hover_event is not None else self.hover_event
        # extra
        result.color_mode = other.color_mode if other.color_mode is not None else self.color_mode
        result.rainbow_reverse = other.rainbow_reverse if other.rainbow_reverse is not None else self.rainbow_reverse
        result.rainbow_phase = other.rainbow_phase if other.rainbow_phase is not None else self.rainbow_phase
        result.gradient_colors = other.gradient_colors if other.gradient_colors is not None else self.gradient_colors
        result.gradient_phase = other.gradient_phase if other.gradient_phase is not None else self.gradient_phase
        result.transition_colors = other.transition_colors if other.transition_colors is not None else self.transition_colors
        result.transition_phase = other.transition_phase if other.transition_phase is not None else self.transition_phase
        return result


def set_component_style(component: TextComponent, style: Style):
    component.color = style.color
    component.font = style.font
    component.bold = style.bold
    component.italic = style.italic
    component.underlined = style.underlined
    component.strikethrough = style.strikethrough
    component.obfuscated = style.obfuscated
    component.insertion = style.insertion
    component.click_event = style.click_event
    component.hover_event = style.hover_event


# TODO: written by ChatGPT, not validated yet, need to test and optimize in the future.


# Helper functions for color conversion and interpolation
def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore


def rgb_to_hex(rgb_color: tuple[int, int, int]) -> str:
    return "#{:02x}{:02x}{:02x}".format(*rgb_color)


def interpolate_color(c1: tuple[int, int, int], c2: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return (int(c1[0] + (c2[0] - c1[0]) * t), int(c1[1] + (c2[1] - c1[1]) * t), int(c1[2] + (c2[2] - c1[2]) * t))


@dataclass
class StyleText:
    text: str
    style: Style

    def to_components(self) -> list[TextComponent]:
        result = []

        if self.style.color_mode == "rainbow":
            result = self._apply_rainbow()
        elif self.style.color_mode == "gradient":
            result = self._apply_gradient()
        elif self.style.color_mode == "transition":
            result = self._apply_transition()
        else:
            # No color mode, just apply basic style to the whole text
            component = TextComponent(self.text)
            set_component_style(component, self.style)
            result.append(component)

        return result

    def _apply_rainbow(self) -> list[TextComponent]:
        rainbow_colors = [
            (255, 0, 0),  # Red
            (255, 165, 0),  # Orange
            (255, 255, 0),  # Yellow
            (0, 255, 0),  # Green
            (0, 0, 255),  # Blue
            (75, 0, 130),  # Indigo
            (238, 130, 238),  # Violet
        ]
        num_colors = len(rainbow_colors)
        phase = self.style.rainbow_phase or 1
        reverse = self.style.rainbow_reverse or False

        if (phase % 2 == 0 and not reverse) or (phase % 2 != 0 and reverse):
            rainbow_colors = list(reversed(rainbow_colors))

        return self._apply_color_cycle(rainbow_colors, phase, total_cycles=phase * num_colors)

    def _apply_gradient(self) -> list[TextComponent]:
        if not self.style.gradient_colors:
            return [TextComponent(self.text)]

        colors = [hex_to_rgb(color) for color in self.style.gradient_colors]
        return self._apply_color_cycle(colors, self.style.gradient_phase or 0)

    def _apply_transition(self) -> list[TextComponent]:
        if not self.style.transition_colors or len(self.style.transition_colors) < 2:
            return [TextComponent(self.text)]

        colors = [hex_to_rgb(color) for color in self.style.transition_colors]
        phase = self.style.transition_phase or 0
        phase_pos = abs(phase)  # Normalize phase from [-1, 1] to [0, 1]
        return self._apply_color_cycle(colors, phase_pos)

    def _apply_color_cycle(self, colors: list[tuple[int, int, int]], phase: float, total_cycles: float = 1) -> list[TextComponent]:
        num_colors = len(colors)
        result = []
        text_length = len(self.text)

        for i, char in enumerate(self.text):
            pos = (i / text_length) * total_cycles
            color_index = int(pos) % num_colors
            next_color_index = (color_index + 1) % num_colors
            t = pos - int(pos)  # Fractional part for interpolation

            interpolated_color = interpolate_color(colors[color_index], colors[next_color_index], t)
            color_hex = rgb_to_hex(interpolated_color)

            component = TextComponent()
            if i == 0:  # 后续组件会继承第一个组件的样式
                set_component_style(component, self.style)
            component.text = char
            component.color = color_hex
            result.append(component)

        return result
