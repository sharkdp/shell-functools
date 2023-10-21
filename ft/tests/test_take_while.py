from mock_command import mock
from ft.commands.take_while import TakeWhile


def test_take_while_const_false():
    cmd = mock(TakeWhile, ("const", ["false"], ["3", "5"]))
    assert cmd.output() == []


def test_take_while_const_true():
    cmd = mock(TakeWhile, ("const", ["true"], ["3", "5"]))
    assert cmd.output() == ["3", "5"]


def test_take_while_lower_equals():
    cmd = mock(TakeWhile, ("le", ["3"], ["3", "2", "5", "4", "1"]))
    assert cmd.output() == ["3", "2"]
