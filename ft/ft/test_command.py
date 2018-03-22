from ft.types import T_BOOL, T_INT, T_ARRAY, T_STRING
from ft.internal import add_dynamic_type


def test_add_dynamic_type():
    assert add_dynamic_type("True").fttype == T_BOOL
    assert add_dynamic_type("-1223").fttype == T_INT
    assert add_dynamic_type("foo\tbar").fttype == T_ARRAY
    assert add_dynamic_type("foo bar").fttype == T_STRING

    assert add_dynamic_type("a ").value == "a "
