import re
from typing import Generator, Optional

from .style import Style
from .text_component import TextComponent
from .segment import TextSegmentSequence


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


def iterate_segments(
    segments: TextSegmentSequence,
    original_text: str,
    start_index: int = 0,
    end_index: Optional[int] = None,
) -> Generator[tuple[str, Style], None, None]:
    if not segments:
        return
    end_index = end_index or len(segments)
    for segment in segments:
        if segment.end <= start_index:
            continue
        if segment.start >= end_index:
            break
        if segment.type == "text":
            text = original_text[max(segment.start, start_index) : min(segment.end, end_index)]
            for char in unescape_text(text):
                yield char, segment.style
        elif segment.type == "single_tag":
            assert segment.text_component is not None
            if segment.text_component.type == "text":
                assert segment.text_component._text is not None
                for char in segment.text_component._text:
                    yield char, segment.style
            else:
                for char in segment.text_component.placeholder_str():
                    yield char, segment.style


def text_segment_sequence_to_text_components(original_text: str, text_segment_sequence: TextSegmentSequence) -> list[TextComponent]:
    text_components = []
    for segment in text_segment_sequence:
        if segment.type == "text":
            component = TextComponent.text(unescape_text(original_text[segment.start : segment.end]))
            segment.style.apply_to_component(component)
            text_components.append(component)
        elif segment.type == "single_tag":
            assert segment.text_component is not None
            component = segment.text_component.clone()
            segment.style.apply_to_component(component)
            text_components.append(component)
    return text_components
