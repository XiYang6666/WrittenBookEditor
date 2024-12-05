import json

from writtenbookeditor.text.util import text_segment_sequence_to_text_components
from writtenbookeditor.text.text_component import text_component_like_to_json_serializable
from writtenbookeditor.text.minimessage import parse_minimessage


def test_style_text():
    text = (
        "<b>Bold text</b>and<i>italic text</i><red>awa<rainbow>12345678901234567890aaaaaa114514114514</red>abcdefg<br>"
        "<rainbow>1234567890aaaaaa114514114514</rainbow><br>"
        "<rainbow>1234567890<black>aaaaaa</black>114514114514</rainbow><br>"
        "<rainbow>1234567890aaaaaa114514114514</rainbow><br>"
        "<rainbow:!>1234567890aaaaaa114514114514</rainbow><br>"
        "<rainbow:2>1234567890aaaaaa114514114514</rainbow><br>"
        "<rainbow:!2>1234567890aaaaaa114514114514</rainbow><br>"
        "<yellow>Woo: <rainbow>||||||||||||||||||||||||</rainbow>!\n"
        "<yellow>Woo: <rainbow:!>||||||||||||||||||||||||</rainbow>!\n"
        "<yellow>Woo: <rainbow:2>||||||||||||||||||||||||</rainbow>!\n"
        "<yellow>Woo: <rainbow:!2>||||||||||||||||||||||||</rainbow>!\n"
    )

    segments = parse_minimessage(text)
    components = text_segment_sequence_to_text_components(text, segments)
    json_data = text_component_like_to_json_serializable(components)
    json_str = json.dumps(json_data)
    print(json_str)
