from mock_command import mock
from ft.commands.sort_by import SortBy


def test_sort_by_id_alphanum():
    cmd = mock(SortBy, ("id", [], ["c", "a", "b"]))
    assert cmd.output() == ["a", "b", "c"]


def test_sort_by_id_numeric():
    cmd = mock(SortBy, ("id", [], ["3", "1", "-2"]))
    assert cmd.output() == ["-2", "1", "3"]


def test_sort_by_length():
    cmd = mock(SortBy, ("length", [], ["aaa", "a", "aa"]))
    assert cmd.output() == ["a", "aa", "aaa"]


def test_sort_by_column():
    cmd = mock(SortBy, ("id", [], ["a\t3", "b\t1", "c\t2"]), column=2)
    assert cmd.output() == ["b\t1", "c\t2", "a\t3"]
