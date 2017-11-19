from functools import partial

from ft.functions import commands
from ft.error import panic


def get_command(name, args):
    try:
        command = commands[name]
    except KeyError:
        panic("Command not found: '{}'".format(name))

    # Partially apply the command
    if len(args) > 0:
        command = partial(command, *args)

    return command
