import os
import subprocess

from ft.types import T_STRING, T_ARRAY, T_BOOL, T_PATH, T_INT, T_VOID, TypeConversionError, \
    dynamic_cast
from ft.internal import TypedValue, add_dynamic_type
from ft.error import panic

function_list = {}


def register(*names):
    if len(names) == 0 or type(names[0]) != str:
        panic("Called @register without arguments")

    def wrap(fn):
        global function_list

        for n in names:
            function_list[n] = fn

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
    return inp + dynamic_cast(T_STRING, suffix).value


@register("prepend")
@typed(T_STRING, T_STRING)
def prepend(prefix, inp):
    return dynamic_cast(T_STRING, prefix).value + inp


@register("take")
@typed(T_STRING, T_STRING)
def take(num, inp):
    num = dynamic_cast(T_INT, num).value
    return inp[0:int(num)]


@register("drop")
@typed(T_STRING, T_STRING)
def drop(num, inp):
    num = dynamic_cast(T_INT, num).value
    return inp[int(num):]


@register("capitalize")
@typed(T_STRING, T_STRING)
def capitalize(inp):
    return inp.capitalize()


@register("to_lower")
@typed(T_STRING, T_STRING)
def to_lower(inp):
    return inp.lower()


@register("to_upper")
@typed(T_STRING, T_STRING)
def to_upper(inp):
    return inp.upper()


@register("replace")
@typed(T_STRING, T_STRING)
def replace(old, new, inp):
    old = dynamic_cast(T_STRING, old)
    new = dynamic_cast(T_STRING, new)
    return inp.replace(old.value, new.value)


@register("split")
@typed(T_STRING, T_ARRAY)
def split(sep, inp):
    sep = dynamic_cast(T_STRING, sep)
    return map(add_dynamic_type, inp.split(sep.value))


@register("join")
@typed(T_ARRAY, T_STRING)
def join(sep, inp):
    sep = dynamic_cast(T_STRING, sep).value
    vals = map(lambda x: T_STRING.create_from(x).value, inp)
    return sep.join(vals)


@register("index", "at")
@typed(T_ARRAY, T_STRING)
def index(idx, inp):
    idx = dynamic_cast(T_INT, idx).value
    try:
        return T_STRING.create_from(inp[idx]).value
    except IndexError:
        panic("array index out of range")


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
    new_ext = dynamic_cast(T_STRING, new_ext).value
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
    b = dynamic_cast(T_INT, b).value
    return a + b


@register("mul")
@typed(T_INT, T_INT)
def mul(b, a):
    b = dynamic_cast(T_INT, b).value
    return a * b


@register("duplicate")
@typed(T_STRING, T_ARRAY)
def duplicate(inp):
    return [TypedValue(inp, T_STRING), TypedValue(inp, T_STRING)]


@register("run")
@typed(T_ARRAY, T_VOID)
def run(cmd, inp):
    cmd = dynamic_cast(T_STRING, cmd).value
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
    substr = dynamic_cast(T_STRING, substr).value
    return substr in inp


@register("nonempty")
@typed(T_STRING, T_BOOL)
def nonempty(inp):
    return inp.strip() != ""


@register("equal", "equals", "eq")
@typed(None, T_BOOL)
def equal(b, a):
    return b.value == a
