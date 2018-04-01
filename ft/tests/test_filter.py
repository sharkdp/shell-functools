from mock_command import mock_command
from ft.commands.filter import Filter

test_filter = mock_command(Filter)


def test_filter_const_false():
    test_filter.set_input("const", ["false"], ["3", "5"])
    test_filter.assert_output([])


def test_filter_const_true():
    test_filter.set_input("const", ["true"], ["3", "5"])
    test_filter.assert_output(["3", "5"])


def test_filter_greater_equals():
    test_filter.set_input("greater_equals", ["3"], ["3", "2", "5", "4", "1"])
    test_filter.assert_output(["3", "5", "4"])
