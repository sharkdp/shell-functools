from mock_command import mock_command
from ft.commands.take_while import TakeWhile


def test_take_while_const_false():
    test_take_while = mock_command(TakeWhile)
    test_take_while.set_input("const", ["false"], ["3", "5"])
    test_take_while.assert_output([])


def test_take_while_const_true():
    test_take_while = mock_command(TakeWhile)
    test_take_while.set_input("const", ["true"], ["3", "5"])
    test_take_while.assert_output(["3", "5"])


def test_take_while_lower_equals():
    test_take_while = mock_command(TakeWhile)
    test_take_while.set_input("le", ["3"], ["3", "2", "5", "4", "1"])
    test_take_while.assert_output(["3", "2"])
