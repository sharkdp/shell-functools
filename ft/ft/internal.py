import sys
import ft.termcolor

from ft.types import TypedValue, T_ARRAY, T_PATH, T_STRING, T_INT, T_BOOL, T_VOID, \
    TypeConversionError


def typed(type_in, type_out):
    def wrap(fn):
        def fn_typecheck(*args):
            inp = args[-1]

            if type_in is not None:
                try:
                    inp = type_in.create_from(inp)
                except TypeConversionError as e:
                    panic("incompatible input type: expected '{}', got '{}'".format(e.type_to,
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


def colored(inp, col):
    if sys.stdout.isatty():
        return ft.termcolor.colored(inp, col)
    return inp


def panic(msg):
    sys.stderr.write("{}: {}\n".format(colored("functools error", "red"), msg))
    sys.exit(1)


def ftformat(val):
    if val.fttype == T_ARRAY:
        return "\t".join(map(ftformat, val.value))
    elif val.fttype == T_PATH:
        return colored(val.value, 'cyan')
    elif val.fttype == T_STRING:
        return colored(val.value, 'yellow')
    elif val.fttype == T_INT:
        return colored(val.value, 'blue')
    elif val.fttype == T_BOOL:
        return colored(val.value, 'magenta')
    elif val.fttype == T_VOID:
        return None

    return val.value


def try_convert_int(inp):
    try:
        return int(inp)
    except ValueError:
        return None


def add_dynamic_type(inp):
    value_int = try_convert_int(inp)

    if value_int:
        return TypedValue(value_int, T_INT)

    elif inp in ["True", "true", "False", "false"]:
        if inp in ["True", "true"]:
            return TypedValue(True, T_BOOL)
        else:
            return TypedValue(False, T_BOOL)

    elif "\t" in inp:
        return TypedValue(list(map(add_dynamic_type, inp.split("\t"))), T_ARRAY)

    else:
        return TypedValue(inp, T_STRING)


def input_values():
    for line in sys.stdin:
        # Strip newline symbols
        if line.endswith("\r\n"):
            line = line[:-2]
        if line.endswith("\n"):
            line = line[:-1]

        value = add_dynamic_type(line)

        yield value
