import os
import subprocess

from fttypes import T_STRING, T_ARRAY, T_BOOL, T_PATH, T_INT
from command import typed, panic, TypedValue


@typed(T_STRING, T_STRING)
def strip(inp):
    return inp.strip()


@typed(T_STRING, T_STRING)
def append(suffix, inp):
    return inp + suffix


@typed(T_STRING, T_STRING)
def prepend(prefix, inp):
    return prefix + inp


@typed(T_STRING, T_STRING)
def take(num, inp):
    return inp[0:int(num)]


@typed(T_STRING, T_STRING)
def drop(num, inp):
    return inp[int(num):]


@typed(T_STRING, T_INT)
def length(inp):
    return len(inp)


@typed(T_PATH, T_PATH)
def basename(path):
    return os.path.basename(path)


@typed(T_PATH, T_PATH)
def abspath(path):
    return os.path.abspath(path)


@typed(T_PATH, T_PATH)
def dirname(path):
    return os.path.dirname(path)


@typed(T_PATH, T_PATH)
def replace_ext(new_ext, path):
    (base, ext) = os.path.splitext(path)
    if ext != "":
        return base + "." + new_ext
    return path


@typed(T_PATH, T_STRING)
def strip_ext(path):
    return os.path.splitext(path)[0]


@typed(None, None)
def identity(inp):
    return inp


@typed(T_INT, T_INT)
def add(b, a):
    try:
        return a + int(b)
    except:
        panic("Argument to 'add' must be an integer")


@typed(T_STRING, T_ARRAY)
def duplicate(inp):
    return [TypedValue(inp, T_STRING), TypedValue(inp, T_STRING)]


@typed(T_ARRAY, T_STRING)
def run(cmd, inp):
    subprocess.call([cmd, *inp])
    return "Running '{}' with arguments {}".format(cmd, inp)


@typed(T_PATH, T_BOOL)
def exists(path):
    return os.path.exists(path)


@typed(T_PATH, T_BOOL)
def is_dir(path):
    return os.path.isdir(path)


@typed(T_PATH, T_BOOL)
def is_file(path):
    return os.path.isfile(path)


@typed(T_PATH, T_BOOL)
def is_link(path):
    return os.path.islink(path)


@typed(T_STRING, T_BOOL)
def contains(substr, inp):
    return substr in inp


@typed(T_STRING, T_BOOL)
def nonempty(inp):
    return inp.strip() != ""


commands = {
    "abspath": abspath,
    "add": add,
    "append": append,
    "basename": basename,
    "contains": contains,
    "dirname": dirname,
    "drop": drop,
    "duplicate": duplicate,
    "exists": exists,
    "id": identity,
    "identity": identity,
    "is_dir": is_dir,
    "is_file": is_file,
    "is_link": is_link,
    "length": length,
    "nonempty": nonempty,
    "prepend": prepend,
    "replace_ext": replace_ext,
    "run": run,
    "strip": strip,
    "strip_ext": strip_ext,
    "take": take,
    "trim": strip,
}
