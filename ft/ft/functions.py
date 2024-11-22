import inspect
import os
import subprocess

from ft.types import (
    T_STRING,
    T_ARRAY,
    T_BOOL,
    T_PATH,
    T_INT,
    T_VOID,
    TypeConversionError,
    dynamic_cast,
)
from ft.internal import TypedValue, add_dynamic_type
from ft.error import panic

function_list = {}


def register(*names):
    if len(names) == 0 or not isinstance(names[0], str):
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
                    panic(
                        "Incompatible input type: expected '{}', got '{}'".format(
                            e.type_to, e.type_from
                        )
                    )

            if len(args) > 1:
                result = fn(*args[0:-1], inp=inp.value)
            else:
                result = fn(inp=inp.value)

            if type_out is None:
                return TypedValue(result, inp.fttype)
            elif type_out == "returned":
                return result

            return TypedValue(result, type_out)

        fn_typecheck.type_in = type_in
        fn_typecheck.type_out = type_out
        fn_typecheck.inner_argspec = inspect.getfullargspec(fn)

        return fn_typecheck

    return wrap


@register("max")
@typed(T_INT, T_INT)
def max(value, inp):
    v = dynamic_cast(T_INT, value).value
    return inp if inp > v else v


@register("min")
@typed(T_INT, T_INT)
def min(value, inp):
    v = dynamic_cast(T_INT, value).value
    return inp if inp < v else v


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
def take(count, inp):
    count = dynamic_cast(T_INT, count).value
    return inp[0 : int(count)]


@register("drop")
@typed(T_STRING, T_STRING)
def drop(count, inp):
    count = dynamic_cast(T_INT, count).value
    return inp[int(count) :]


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
def substr(start, end, inp):
    start = dynamic_cast(T_INT, start).value
    end = dynamic_cast(T_INT, end).value
    return inp[start:end]


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


@register("ends_with", "endswith")
@typed(T_STRING, T_BOOL)
def ends_with(pattern, inp):
    pattern = dynamic_cast(T_STRING, pattern).value
    return inp.endswith(pattern)


@register("split")
@typed(T_STRING, T_ARRAY)
def split(separator, inp):
    separator = dynamic_cast(T_STRING, separator)
    return map(add_dynamic_type, inp.split(separator.value))


@register("join")
@typed(T_ARRAY, T_STRING)
def join(separator, inp):
    separator = dynamic_cast(T_STRING, separator).value
    vals = map(lambda x: T_STRING.create_from(x).value, inp)
    return separator.join(vals)


@register("index", "at")
@typed(T_ARRAY, T_STRING)
def index(idx, inp):
    idx = dynamic_cast(T_INT, idx).value
    try:
        return T_STRING.create_from(inp[idx]).value
    except IndexError:
        panic("array index out of range")


@register("length", "len")
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


@register("filesize")
@typed(T_PATH, T_INT)
def filesize(inp):
    return os.path.getsize(inp)


@register("file_ext")
@typed(T_PATH, T_STRING)
def file_ext(inp):
    return os.path.splitext(inp)[1]


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


@register("split_ext")
@typed(T_PATH, T_ARRAY)
def split_ext(inp):
    parts = os.path.splitext(inp)
    return [TypedValue(parts[0], T_STRING), TypedValue(parts[1][1:], T_STRING)]


@register("id", "identity")
@typed(None, None)
def id(inp):
    return inp


@register("const")
@typed(None, "returned")
def const(value, inp):
    return value


@register("add")
@typed(T_INT, T_INT)
def add(num, inp):
    num = dynamic_cast(T_INT, num).value
    return inp + num


@register("sub")
@typed(T_INT, T_INT)
def sub(num, inp):
    num = dynamic_cast(T_INT, num).value
    return inp - num


@register("pow")
@typed(T_INT, T_INT)
def power(num, inp):
    num = dynamic_cast(T_INT, num).value
    return pow(inp, num)


@register("mul")
@typed(T_INT, T_INT)
def mul(num, inp):
    num = dynamic_cast(T_INT, num).value
    return inp * num


@register("even")
@typed(T_INT, T_BOOL)
def even(inp):
    return inp % 2 == 0


@register("odd")
@typed(T_INT, T_BOOL)
def odd(inp):
    return inp % 2 == 1


@register("duplicate")
@typed(T_STRING, T_ARRAY)
def duplicate(inp):
    return [TypedValue(inp, T_STRING), TypedValue(inp, T_STRING)]


@register("run")
@typed(T_ARRAY, T_VOID)
def run(command, inp):
    command = dynamic_cast(T_STRING, command).value
    args = map(T_STRING.create_from, inp)
    args = list(map(lambda v: v.value, args))

    print("Running '{}' with arguments {}".format(command, args))
    subprocess.call([command] + args)


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


@register("is_executable")
@typed(T_PATH, T_BOOL)
def is_executable(inp):
    return os.path.isfile(inp) and os.access(inp, os.X_OK)


@register("contains")
@typed(T_STRING, T_BOOL)
def contains(substring, inp):
    substring = dynamic_cast(T_STRING, substring).value
    return substring in inp


@register("nonempty", "non_empty")
@typed(None, T_BOOL)
def nonempty(inp):
    if type(inp) is list:
        return bool(inp)
    elif type(inp) is str:
        return inp.strip() != ""

    return True


@register("equal", "equals", "eq")
@typed(None, T_BOOL)
def equal(other, inp):
    return other.value == inp


@register("not_equal", "not_equals", "ne")
@typed(None, T_BOOL)
def not_equals(other, inp):
    return other.value != inp


@register("greater", "greater_than", "gt")
@typed(T_INT, T_BOOL)
def greater_than(i, inp):
    i = dynamic_cast(T_INT, i).value
    return inp > i


@register("greater_equal", "greater_equals", "ge")
@typed(T_INT, T_BOOL)
def greater_equals(i, inp):
    i = dynamic_cast(T_INT, i).value
    return inp >= i


@register("less", "less_than", "lt")
@typed(T_INT, T_BOOL)
def less_than(i, inp):
    i = dynamic_cast(T_INT, i).value
    return inp < i


@register("less_equal", "less_equals", "le")
@typed(T_INT, T_BOOL)
def less_equals(i, inp):
    i = dynamic_cast(T_INT, i).value
    return inp <= i


@register("format")
@typed(None, T_STRING)
def format(format_str, inp):
    try:
        return format_str.value.format(inp)
    except ValueError:
        panic(
            "Incorrect format string '{}' for input '{}'.".format(format_str.value, inp)
        )


@register("reverse")
@typed(None, None)
def reverse(inp):
    # slice arrays and string from start to finish in reversed order
    if type(inp) is str or type(inp) is list:
        return inp[::-1]

    # treat integers as strings
    elif type(inp) is int:
        return str(inp)[::-1]

    # booleans can not be reversed
    elif type(inp) is bool:
        panic("Cannot reverse bool value")

    # we got something unexpected
    else:
        panic("Unexpected type '{}' for input '{}'.".format(type(inp).__name__, inp))
