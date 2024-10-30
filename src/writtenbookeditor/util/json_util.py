from typing import Union

JsonSerializable = Union[str, int, float, bool, None, dict, list]


def remove_dict_none_value(d: dict) -> dict:
    return {k: v for k, v in d.items() if v is not None}


def remove_dict_false_value(d: dict) -> dict:
    return {k: v for k, v in d.items() if v is not False}
