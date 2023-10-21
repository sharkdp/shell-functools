import sys
import ft.termcolor
import re

from ft.types import TypedValue, T_ARRAY, T_PATH, T_STRING, T_INT, T_BOOL, T_VOID


def colored(inp, col):
    if sys.stdout.isatty():
        return ft.termcolor.colored(inp, col)
    return str(inp)


def ftformat(val):
    if val.fttype == T_ARRAY:
        return "\t".join(map(ftformat, val.value))
    elif val.fttype == T_PATH:
        return colored(val.value, "cyan")
    elif val.fttype == T_STRING:
        return colored(val.value, "yellow")
    elif val.fttype == T_INT:
        return colored(val.value, "blue")
    elif val.fttype == T_BOOL:
        return colored(val.value, "magenta")
    elif val.fttype == T_VOID:
        return None

    return str(val.value)


def try_convert_int(inp):
    # Make sure that the input *only* consists of a number (no added spaces..)
    if not re.match(r"^[+-]?\d+$", inp):
        return None

    try:
        return int(inp)
    except ValueError:
        return None


def add_dynamic_type(inp):
    value_int = try_convert_int(inp)

    if value_int is not None:
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
