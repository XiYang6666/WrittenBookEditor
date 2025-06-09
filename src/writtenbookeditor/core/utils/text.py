import re
from typing import Callable, Iterator, Mapping


from ..interface.text import Escaper


def create_escaper(
    rules: Mapping[str | re.Pattern, str | Callable[[str], str]],
) -> Escaper:
    """
    创建转义器

    输入一个映射表，返回一个转义器函数
    """

    def escaper(text: str) -> Iterator[tuple[str, str]]:
        ptr = 0
        length = len(text)

        while ptr < length:
            for key, replacement in rules.items():
                if isinstance(key, str) and text.startswith(key, ptr):
                    escaped = replacement(key) if callable(replacement) else replacement
                    yield key, escaped
                    ptr += len(key)
                    break
                elif isinstance(key, re.Pattern):
                    if not (match := key.match(text, ptr)):
                        continue
                    s = match.group()
                    escaped = replacement(s) if callable(replacement) else replacement
                    yield s, escaped
                    ptr += len(s)
                    break
            else:
                s = text[ptr]
                yield s, s
                ptr += 1

    return escaper


def empty_escaper(text: str) -> Iterator[tuple[str, str]]:
    """
    空转义器

    什么都不做，直接返回输入文本
    """
    yield from ((c, c) for c in text)


def escape_text(bare_text: str, escaper: Escaper) -> str:
    """
    转义文本

    使用转义器对文本进行转义
    """
    return "".join(t[1] for t in escaper(bare_text))


def map_escaped_pos_to_bare(bare_text: str, escaper: Escaper, *pos: int) -> tuple[int, ...]:
    """
    将转义后的位置映射到原文本的位置
    """
    max_pos = max(pos)
    result: list[None | int] = [0 if p == 0 else None for p in pos]
    o_ptr = 0
    e_ptr = 0
    for o, e in escaper(bare_text):
        o_ptr += len(o)
        e_ptr += len(e)
        if e_ptr in pos:
            pos_idxs = [j for j, p in enumerate(pos) if p == e_ptr]
            for j in pos_idxs:
                result[j] = o_ptr
        if e_ptr >= max_pos:
            break
    assert None not in result
    return tuple(result)  # type: ignore
