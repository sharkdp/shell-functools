from ft.types import T_BOOL, T_INT, T_ARRAY, T_STRING
import ft.command


def test_add_dynamic_type():
    assert ft.command.add_dynamic_type("True").fttype == T_BOOL
    assert ft.command.add_dynamic_type("-1223").fttype == T_INT
    assert ft.command.add_dynamic_type("foo\tbar").fttype == T_ARRAY
    assert ft.command.add_dynamic_type("foo bar").fttype == T_STRING
