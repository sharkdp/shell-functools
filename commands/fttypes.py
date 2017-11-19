class TypeConversionError(Exception):
    pass


class TypedValue:
    def __init__(self, value, fttype):
        self.value = value
        self.fttype = fttype


class FtType:
    def __init__(self):
        pass

    def create_from(self, inp):
        raise NotImplementedError


class FtString(FtType):
    def create_from(self, inp):
        if inp.fttype == T_STRING:
            return inp
        elif inp.fttype == T_ARRAY:
            return TypedValue("\t".join(map(T_STRING.create_from, inp.value), T_ARRAY))
        else:
            return TypedValue([inp.value], T_ARRAY)


class FtArray(FtType):
    def create_from(self, inp):
        if inp.fttype == T_ARRAY:
            return inp
        elif inp.fttype == T_STRING:
            return TypedValue(inp.value.split("\t"), T_ARRAY)
        else:
            return TypedValue([inp.value], T_ARRAY)


class FtPath(FtType):
    def create_from(self, inp):
        return TypedValue(inp.value, T_PATH)  # TODO


class FtBool(FtType):
    def create_from(self, inp):
        if inp.fttype == T_BOOL:
            return inp
        elif inp.fttype == T_STRING:
            val = False
            if inp.value == "true" or inp.value == "True":
                val = True
            return TypedValue(val, T_BOOL)
        else:
            raise TypeConversionError


class FtInt(FtType):
    def create_from(self, inp):
        if inp.fttype == T_INT:
            return inp
        elif inp.fttype == T_STRING:
            try:
                return TypedValue(int(inp.value), T_INT)
            except ValueError:
                raise TypeConversionError
        else:
            raise TypeConversionError


T_STRING = FtString()
T_ARRAY = FtArray()
T_PATH = FtPath()
T_BOOL = FtBool()
T_INT = FtInt()
