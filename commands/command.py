import sys
import termcolor

from fttypes import TypedValue, T_ARRAY, T_PATH, T_STRING, T_INT


def colored(inp, col):
    if sys.stdout.isatty():
        return termcolor.colored(inp, col)
    return inp


def panic(msg):
    sys.stderr.write("{}: {}\n".format(colored("functools error", "red"), msg))
    sys.exit(1)


def typed(type_in, type_out):
    def wrap(fn):
        def fn_typecheck(*args):
            inp = args[-1]
            inp_casted = type_in.create_from(inp)
            if len(args) > 1:
                result = fn(*args[0:-1], inp_casted.value)
            else:
                result = fn(inp_casted.value)
            return TypedValue(result, type_out)

        return fn_typecheck
    return wrap


def ftformat(val):
    if val.fttype == T_ARRAY:
        return "\t".join(map(ftformat, val.value))
    elif val.fttype == T_PATH:
        return colored(val.value, 'cyan')
    elif val.fttype == T_STRING:
        return colored(val.value, 'yellow')
    elif val.fttype == T_INT:
        return colored(val.value, 'blue')

    return val.value
