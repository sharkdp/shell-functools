import sys


class TypeConversionError(Exception):
    pass


def panic(msg):
    sys.stderr.write("fps error: {}\n".format(msg))
    sys.exit(1)


class FpsType:
    def __init__(self):
        pass

    def create_from(self, inp):
        raise NotImplementedError


class FpsString(FpsType):
    def create_from(self, inp):
        return TypedValue(inp.value, T_STRING)  # TODO


class FpsPath(FpsType):
    def create_from(self, inp):
        return TypedValue(inp.value, T_STRING)  # TODO


class FpsBool(FpsType):
    def create_from(self, inp):
        if inp.fpstype == T_BOOL:
            return inp
        elif inp.fpstype == T_STRING:
            val = False
            if inp.value == "true" or inp.value == "True":
                val = True
            return TypedValue(val, T_BOOL)
        else:
            raise TypeConversionError


class FpsInt(FpsType):
    def create_from(self, inp):
        if inp.fpstype == T_INT:
            return inp
        elif inp.fpstype == T_STRING:
            try:
                return TypedValue(int(inp.value), T_INT)
            except ValueError:
                raise TypeConversionError
        else:
            raise TypeConversionError


T_STRING = FpsString()
T_PATH = FpsPath()
T_BOOL = FpsBool()
T_INT = FpsInt()


class TypedValue:
    def __init__(self, value, fpstype):
        self.value = value
        self.fpstype = fpstype


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
