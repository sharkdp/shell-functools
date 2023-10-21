from mock_command import mock
from ft.commands.filter import Filter


def test_filter_const_false():
    cmd = mock(Filter, ("const", ["false"], ["3", "5"]))
    assert cmd.output() == []


def test_filter_const_true():
    cmd = mock(Filter, ("const", ["true"], ["3", "5"]))
    assert cmd.output() == ["3", "5"]


def test_filter_greater_equals():
    cmd = mock(Filter, ("greater_equals", ["3"], ["3", "2", "5", "4", "1"]))
    assert cmd.output() == ["3", "5", "4"]


def test_filter_negate_predicate():
    cmd = mock(Filter, ("even", [], ["1", "2", "3", "4"]), negate_predicate=True)
    assert cmd.output() == ["1", "3"]
