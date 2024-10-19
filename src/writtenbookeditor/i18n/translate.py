import json
import tomllib
from pathlib import Path

translate_dict = {}
translate_dict_mc = {}
language = "en_US"


def set_lang(lang: str):
    global language
    global translate_dict
    global translate_dict_mc
    language = lang

    lang_file_path = Path(f"./data/lang/{language}.toml")
    if not lang_file_path.exists():
        translate_dict = {}
    with lang_file_path.open("rb") as f:
        translate_dict = tomllib.load(f)

    lang_file_path = Path(f"./data/lang/{language.lower()}.json")
    if not lang_file_path.exists():
        translate_dict_mc = {}
    with lang_file_path.open("r", encoding="utf-8") as f:
        translate_dict_mc = json.load(f)


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


def translate_mc(key: str) -> str:
    return translate_dict_mc.get(key, key)
