import tomllib
from pathlib import Path

translate_dict = {}
language = "en_US"


def set_lang(lang: str):
    global language
    global translate_dict
    language = lang

    lang_file_path = Path(f"./data/lang/{language}.toml")
    if not lang_file_path.exists():
        translate_dict = {}
    with lang_file_path.open("rb") as f:
        translate_dict = tomllib.load(f)


def get_lang() -> str:
    return language


def translate(key: str) -> str:
    value = translate_dict
    for k in key.split("."):
        if not isinstance(value, dict):
            return key
        value = value.get(k)
        if value is None:
            return key
    if not isinstance(value, str):
        return key
    return value
