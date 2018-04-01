from mock_command import mock_command
from ft.commands.sort_by import SortBy


def test_sort_by_id_alphanum():
    test_sort_by = mock_command(SortBy)
    test_sort_by.set_input("id", [], ["c", "a", "b"])
    test_sort_by.assert_output(["a", "b", "c"])


def test_sort_by_id_numeric():
    test_sort_by = mock_command(SortBy)
    test_sort_by.set_input("id", [], ["3", "1", "-2"])
    test_sort_by.assert_output(["-2", "1", "3"])


def test_sort_by_length():
    test_sort_by = mock_command(SortBy)
    test_sort_by.set_input("length", [], ["aaa", "a", "aa"])
    test_sort_by.assert_output(["a", "aa", "aaa"])


def test_sort_by_column():
    test_sort_by = mock_command(SortBy)

    test_sort_by.set_input("id", [], ["a\t3", "b\t1", "c\t2"])

    # set `--column 2`
    test_sort_by.column = 2

    test_sort_by.assert_output(["b\t1", "c\t2", "a\t3"])
