from mock_command import mock
from ft.commands.map import Map


# test cases for Arithmetic operations
def test_map_add3():
    cmd = mock(Map, ("add", ["3"], ["3", "5"]))
    assert cmd.output() == ["6", "8"]


def test_map_sub3():
    cmd = mock(Map, ("sub", ["3"], ["1", "3", "4"]))
    assert cmd.output() == ["-2", "0", "1"]


def test_map_mul3():
    cmd = mock(Map, ("mul", ["3"], ["0", "-1", "3"]))
    assert cmd.output() == ["0", "-3", "9"]


def test_map_id():
    cmd = mock(Map, ("id", [], ["3", "5"]))
    assert cmd.output() == ["3", "5"]


def test_map_split_ext():
    cmd = mock(Map, ("split_ext", [], ["file.txt", "dir/image.jpg"]))
    assert cmd.output() == ["file\ttxt", "dir/image\tjpg"]


def test_map_format_string():
    cmd = mock(Map, ("format", ["{:>5}"], ["abc", "b"]))
    assert cmd.output() == ["  abc", "    b"]


def test_map_format_int():
    cmd = mock(Map, ("format", ["{:02x}"], ["3", "11", "255"]))
    assert cmd.output() == ["03", "0b", "ff"]
