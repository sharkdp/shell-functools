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
                result = fn(*args[0:-1], inp=inp.value)
            else:
                result = fn(inp=inp.value)

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


@register("substr")
@typed(T_STRING, T_STRING)
def substr(i1, i2, inp):
    i1 = dynamic_cast(T_INT, i1).value
    i2 = dynamic_cast(T_INT, i2).value
    return inp[i1:i2]


@register("replace")
@typed(T_STRING, T_STRING)
def replace(old, new, inp):
    old = dynamic_cast(T_STRING, old)
    new = dynamic_cast(T_STRING, new)
    return inp.replace(old.value, new.value)


@register("starts_with", "startswith")
@typed(T_STRING, T_BOOL)
def starts_with(pattern, inp):
    pattern = dynamic_cast(T_STRING, pattern).value
    return inp.startswith(pattern)


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
def basename(inp):
    return os.path.basename(inp)


@register("abspath")
@typed(T_PATH, T_PATH)
def abspath(inp):
    return os.path.abspath(inp)


@register("dirname")
@typed(T_PATH, T_PATH)
def dirname(inp):
    return os.path.dirname(inp)


@register("replace_ext")
@typed(T_PATH, T_PATH)
def replace_ext(new_ext, inp):
    new_ext = dynamic_cast(T_STRING, new_ext).value
    (base, ext) = os.path.splitext(inp)
    if ext != "":
        return base + "." + new_ext
    return inp


@register("strip_ext")
@typed(T_PATH, T_STRING)
def strip_ext(inp):
    return os.path.splitext(inp)[0]


@register("has_ext")
@typed(T_PATH, T_BOOL)
def has_ext(ext, inp):
    ext = dynamic_cast(T_STRING, ext).value
    (_, file_ext) = os.path.splitext(inp)
    file_ext = file_ext[1:]  # strip leading dot
    return file_ext == ext


@register("id", "identity")
@typed(None, None)
def id(inp):
    return inp


@register("add")
@typed(T_INT, T_INT)
def add(b, inp):
    b = dynamic_cast(T_INT, b).value
    return inp + b


@register("mul")
@typed(T_INT, T_INT)
def mul(b, inp):
    b = dynamic_cast(T_INT, b).value
    return inp * b


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
def exists(inp):
    return os.path.exists(inp)


@register("is_dir")
@typed(T_PATH, T_BOOL)
def is_dir(inp):
    return os.path.isdir(inp)


@register("is_file")
@typed(T_PATH, T_BOOL)
def is_file(inp):
    return os.path.isfile(inp)


@register("is_link")
@typed(T_PATH, T_BOOL)
def is_link(inp):
    return os.path.islink(inp)


@register("contains")
@typed(T_STRING, T_BOOL)
def contains(substr, inp):
    substr = dynamic_cast(T_STRING, substr).value
    return substr in inp


@register("nonempty", "non_empty")
@typed(None, T_BOOL)
def nonempty(inp):
    if type(inp) == list:
        return bool(inp)
    elif type(inp) == str:
        return inp.strip() != ""

    return True


@register("equal", "equals", "eq")
@typed(None, T_BOOL)
def equal(b, inp):
    return b.value == inp
