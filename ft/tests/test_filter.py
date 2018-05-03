from mock_command import mock_command
from ft.commands.filter import Filter


def test_filter_const_false():
    test_filter = mock_command(Filter)
    test_filter.set_input("const", ["false"], ["3", "5"])
    test_filter.assert_output([])


def test_filter_const_true():
    test_filter = mock_command(Filter)
    test_filter.set_input("const", ["true"], ["3", "5"])
    test_filter.assert_output(["3", "5"])


def test_filter_greater_equals():
    test_filter = mock_command(Filter)
    test_filter.set_input("greater_equals", ["3"], ["3", "2", "5", "4", "1"])
    test_filter.assert_output(["3", "5", "4"])


def test_filter_negate_predicate():
    test_filter = mock_command(Filter)
    test_filter.negate_predicate = True
    test_filter.set_input("even", [], ["1", "2", "3", "4"])
    test_filter.assert_output(["1", "3"])
