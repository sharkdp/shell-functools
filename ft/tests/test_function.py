from mock_command import mock
from ft.commands.foldl1 import Foldl1


def test_max():
    cmd = mock(Foldl1, ("max", [], ["1", "7", "0", "5"]))
    assert cmd.output() == ["7"]


def test_max_column():
    cmd = mock(Foldl1, ("max", [], ["a\t1", "b\t7", "c\t0", "d\t5"]), column=2)
    assert cmd.output() == ["7"]


def test_min():
    cmd = mock(Foldl1, ("min", [], ["-1", "-3", "0", "-5"]))
    assert cmd.output() == ["-5"]


def test_min_column():
    cmd = mock(Foldl1, ("min", [], ["a\t1", "b\t7", "c\t0", "d\t5"]), column=2)
    assert cmd.output() == ["0"]
