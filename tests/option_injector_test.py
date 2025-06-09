from writtenbookeditor.core.registry import register_option_table
from writtenbookeditor.core.options import option
from writtenbookeditor.core.injector import get_option_meta, inject_options


@register_option_table("table_a")
class TableA:
    a: int = option("int")
    b: str = option("str")
    c: float = option("float")
    d: bool = option("bool")
    e: str = option("choice", ["a", "b", "c"], default="a")


@register_option_table("table_b")
class TableB:
    a: int = option("int")
    b: str = option("str")
    c: float = option("float")
    d: bool = option("bool")
    e: str = option("choice", ["a", "b", "c"], default="a")
    f = option("table", TableA)


class TestClass:
    a: int = option("int")
    b: str = option("str")
    c: float = option("float")
    d: bool = option("bool")
    e: str = option("choice", ["a", "b", "c"], default="a")
    f = option("table", TableB)


def test_option_injector():
    """
    测试配置项注入
    """
    meta = get_option_meta(TestClass)
    instant = TestClass()
    instant = inject_options(
        instant,
        meta,
        {
            "a": 1,
            "b": "2",
            "c": 3.0,
            "d": True,
            "e": "test",
            "table_b:a": 2,
            "table_b:b": "3",
            "table_b:c": 4.0,
            "table_b:d": False,
            "table_b:e": "test_b",
            "table_a:a": 5,
            "table_a:b": "6",
            "table_a:c": 7.0,
            "table_a:d": True,
            "table_a:e": "test_a",
        },
    )
    assert instant.a == 1
    assert instant.b == "2"
    assert instant.c == 3.0
    assert instant.d == True  # noqa: E712
    assert instant.e == "test"
    assert isinstance(instant.f, TableB)
    assert instant.f.a == 2
    assert instant.f.b == "3"
    assert instant.f.c == 4.0
    assert instant.f.d == False  # noqa: E712
    assert instant.f.e == "test_b"
    assert isinstance(instant.f.f, TableA)
    assert instant.f.f.a == 5
    assert instant.f.f.b == "6"
    assert instant.f.f.c == 7.0
    assert instant.f.f.d == True  # noqa: E712
    assert instant.f.f.e == "test_a"
