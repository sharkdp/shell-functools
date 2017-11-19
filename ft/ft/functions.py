import os
import subprocess

from ft.types import T_STRING, T_ARRAY, T_BOOL, T_PATH, T_INT, T_VOID, TypeConversionError
from ft.internal import TypedValue
from ft.error import panic

commands = {}


def register(*names):
    if len(names) == 0 or type(names[0]) != str:
        panic("Called @register without arguments")

    def wrap(fn):
        global commands

        for n in names:
            commands[n] = fn

    return wrap


def typed(type_in, type_out):
    def wrap(fn):
        def fn_typecheck(*args):
            inp = args[-1]

            if type_in is not None:
                try:
                    inp = type_in.create_from(inp)
                except TypeConversionError as e:
                    panic("Incompatible input type: expected '{}', got '{}'".format(e.type_to,
                                                                                    e.type_from))

            if len(args) > 1:
                result = fn(*args[0:-1], inp.value)
            else:
                result = fn(inp.value)

            if type_out is None:
                return TypedValue(result, inp.fttype)

            return TypedValue(result, type_out)

        return fn_typecheck

    return wrap


@register("strip")
@typed(T_STRING, T_STRING)
def strip(inp):
    return inp.strip()


@register("append")
@typed(T_STRING, T_STRING)
def append(suffix, inp):
    return inp + suffix


@register("prepend")
@typed(T_STRING, T_STRING)
def prepend(prefix, inp):
    return prefix + inp


@register("take")
@typed(T_STRING, T_STRING)
def take(num, inp):
    return inp[0:int(num)]


@register("drop")
@typed(T_STRING, T_STRING)
def drop(num, inp):
    return inp[int(num):]


@register("length")
@typed(T_STRING, T_INT)
def length(inp):
    return len(inp)


@register("basename")
@typed(T_PATH, T_PATH)
def basename(path):
    return os.path.basename(path)


@register("abspath")
@typed(T_PATH, T_PATH)
def abspath(path):
    return os.path.abspath(path)


@register("dirname")
@typed(T_PATH, T_PATH)
def dirname(path):
    return os.path.dirname(path)


@register("replace_ext")
@typed(T_PATH, T_PATH)
def replace_ext(new_ext, path):
    (base, ext) = os.path.splitext(path)
    if ext != "":
        return base + "." + new_ext
    return path


@register("strip_ext")
@typed(T_PATH, T_STRING)
def strip_ext(path):
    return os.path.splitext(path)[0]


@register("id", "identity")
@typed(None, None)
def id(inp):
    return inp


@register("add")
@typed(T_INT, T_INT)
def add(b, a):
    try:
        return a + int(b)
    except:
        panic("Argument to 'add' must be an integer")


@register("duplicate")
@typed(T_STRING, T_ARRAY)
def duplicate(inp):
    return [TypedValue(inp, T_STRING), TypedValue(inp, T_STRING)]


@register("run")
@typed(T_ARRAY, T_VOID)
def run(cmd, inp):
    args = map(T_STRING.create_from, inp)
    args = list(map(lambda v: v.value, args))

    print("Running '{}' with arguments {}".format(cmd, args))
    subprocess.call([cmd] + args)


@register("exists")
@typed(T_PATH, T_BOOL)
def exists(path):
    return os.path.exists(path)


@register("is_dir")
@typed(T_PATH, T_BOOL)
def is_dir(path):
    return os.path.isdir(path)


@register("is_file")
@typed(T_PATH, T_BOOL)
def is_file(path):
    return os.path.isfile(path)


@register("is_link")
@typed(T_PATH, T_BOOL)
def is_link(path):
    return os.path.islink(path)


@register("contains")
@typed(T_STRING, T_BOOL)
def contains(substr, inp):
    return substr in inp


@register("nonempty")
@typed(T_STRING, T_BOOL)
def nonempty(inp):
    return inp.strip() != ""
