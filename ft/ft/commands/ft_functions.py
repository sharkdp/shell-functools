from ft.types import T_VOID
from ft.functions import function_list
from ft.termcolor import colored

type_color = {
    "String": "yellow",
    "Path": "cyan",
    "Int": "blue",
    "Bool": "magenta",
    "Array": "red",
    "*": "white",
    "!": "red"
}


def with_color(typename):
    if typename in type_color:
        return colored(typename, type_color[typename])

    return typename


def main():
    for name, fn in sorted(function_list.items()):
        type_in = fn.type_in
        type_out = fn.type_out

        if type_in is None:
            type_in = with_color("*")
        else:
            type_in = with_color(str(type_in))

        if type_out is None:
            type_out = with_color("*")
        elif type_out == "returned":
            type_out = with_color("*")
        elif type_out == T_VOID:
            type_out = with_color("!")
        else:
            type_out = with_color(str(type_out))

        arg_names = fn.inner_argspec.args[:-1]

        name_and_args = colored(name, "green")

        if len(arg_names) > 0:
            name_and_args += " " + " ".join(arg_names)

        print("{name_and_args:<28} :: {type_in:<15} → {type_out}".format(
            name_and_args=name_and_args,
            type_in=type_in,
            type_out=type_out))


if __name__ == "__main__":
    main()
