from mock_command import mock_command
from ft.commands.filter import Filter

map_filter = mock_command(Filter)


def test_filter_const_false():
    map_filter.set_input("const", ["false"], ["3", "5"])
    map_filter.assert_output([])


def test_filter_const_true():
    map_filter.set_input("const", ["true"], ["3", "5"])
    map_filter.assert_output(["3", "5"])


def test_filter_greater_equals():
    map_filter.set_input("greater_equals", ["3"], ["3", "2", "5", "4", "1"])
    map_filter.assert_output(["3", "5", "4"])
