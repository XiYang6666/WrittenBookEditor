import json
import tomllib
from pathlib import Path
from typing import Optional

translate_dict_app = {}
translate_dict_mc = {}
language = "en_US"


def set_lang(lang: str):
    global language
    global translate_dict_app
    global translate_dict_mc
    language = lang

    lang_file_path = Path(f"./data/lang/{language}.toml")
    if not lang_file_path.exists():
        translate_dict_app = {}
    with lang_file_path.open("rb") as f:
        translate_dict_app = tomllib.load(f)

    lang_file_path = Path(f"./data/lang/{language.lower()}.json")
    if not lang_file_path.exists():
        translate_dict_mc = {}
    with lang_file_path.open("r", encoding="utf-8") as f:
        translate_dict_mc = json.load(f)


def get_lang() -> str:
    return language


def translate_app(key: str) -> Optional[str]:
    split_result = key.split(".")
    if len(split_result) != 2:
        return None
    value = translate_dict_app.get(split_result[0], {}).get(split_result[1], None)
    return value


def translate_mc(key: str) -> Optional[str]:
    return translate_dict_mc.get(key, None)


def translate(key: str) -> str:
    return translate_app(key) or translate_mc(key) or key
