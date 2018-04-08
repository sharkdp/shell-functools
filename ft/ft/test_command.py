from ft.types import T_BOOL, T_INT, T_ARRAY, T_STRING
from ft.internal import add_dynamic_type


def test_add_dynamic_type_bool():
    assert add_dynamic_type("True").fttype == T_BOOL
    assert add_dynamic_type("False").fttype == T_BOOL


def test_add_dynamic_type_int():
    assert add_dynamic_type("0").fttype == T_INT
    assert add_dynamic_type("1223").fttype == T_INT
    assert add_dynamic_type("-1223").fttype == T_INT
    assert add_dynamic_type("+1223").fttype == T_INT


def test_add_dynamic_type_array():
    assert add_dynamic_type("foo\tbar").fttype == T_ARRAY
    assert add_dynamic_type("foo\tbar\tbaz").fttype == T_ARRAY


def test_add_dynamic_type_string():
    assert add_dynamic_type("foo").fttype == T_STRING
    assert add_dynamic_type("foo bar").fttype == T_STRING


def test_add_dynamic_type():
    assert add_dynamic_type("a ").value == "a "
