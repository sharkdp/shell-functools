from ft.types import T_ARRAY
from ft.internal import ftformat
from ft.command import Command


class Map(Command):
    def __init__(self):
        super().__init__("map")

    def handle_input(self, value):
        if value.fttype == T_ARRAY and self.column is not None:
            idx = self.column - 1
            value.value[idx] = self.function(value.value[idx])
            result = value
        else:
            result = self.function(value)

        out = ftformat(result)

        if out:
            print(out)
