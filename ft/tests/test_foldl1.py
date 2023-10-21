from mock_command import mock
from ft.commands.foldl1 import Foldl1


def test_foldl1_alphanum():
    cmd = mock(Foldl1, ("append", [], ["a", "b", "c", "d"]))
    assert cmd.output() == ["abcd"]


def test_foldl1_numeric():
    cmd = mock(Foldl1, ("mul", [], ["1", "-2", "3", "-4"]))
    assert cmd.output() == ["24"]


def test_foldl1_column():
    cmd = mock(Foldl1, ("mul", [], ["a\t1", "b\t2", "c\t3", "d\t4"]), column=2)
    assert cmd.output() == ["24"]
