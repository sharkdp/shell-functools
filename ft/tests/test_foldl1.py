from mock_command import mock_command
from ft.commands.foldl1 import Foldl1


def test_foldl1_alphanum():
    test_foldl1 = mock_command(Foldl1)
    test_foldl1.set_input("append", [], ["a", "b", "c", "d"])
    test_foldl1.assert_output(["abcd"])


def test_foldl1_numeric():
    test_foldl1 = mock_command(Foldl1)
    test_foldl1.set_input("mul", [], ["1", "-2", "3", "-4"])
    test_foldl1.assert_output(["24"])


def test_foldl1_column():
    test_foldl1 = mock_command(Foldl1)
    test_foldl1.set_input("mul", [], ["a\t1", "b\t2", "c\t3", "d\t4"])

    # set `--column 2`
    test_foldl1.column = 2

    test_foldl1.assert_output(["24"])
