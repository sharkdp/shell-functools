from mock_command import mock_command
from ft.commands.foldl1 import Foldl1

def test_max():
    test_foldl1 = mock_command(Foldl1)
    test_foldl1.set_input("max", [], ["1", "7", "0", "5"])
    test_foldl1.assert_output(["7"])


def test_max_column():
    test_foldl1 = mock_command(Foldl1)
    test_foldl1.set_input("max", [], ["a\t1", "b\t7", "c\t0", "d\t5"])

    # set `--column 2`
    test_foldl1.column = 2

    test_foldl1.assert_output(["7"])


def test_min():
    test_foldl1 = mock_command(Foldl1)
    test_foldl1.set_input("min", [], ["-1", "-3", "0", "-5"])
    test_foldl1.assert_output(["-5"])

def test_max_column():
    test_foldl1 = mock_command(Foldl1)
    test_foldl1.set_input("min", [], ["a\t1", "b\t7", "c\t0", "d\t5"])

    # set `--column 2`
    test_foldl1.column = 2
    
    test_foldl1.assert_output(["0"])