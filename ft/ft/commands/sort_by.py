from ft.types import T_ARRAY
from ft.command import Command


class SortBy(Command):
    def __init__(self):
        super().__init__("sort_by")
        self.arr = []

    def handle_input(self, value):
        if value.fttype == T_ARRAY and self.column is not None:
            result = self.function(value.value[self.column - 1])
        else:
            result = self.function(value)

        self.arr.append((value, result))

    def finalize(self):
        arr = sorted(self.arr, key=lambda x: x[1])
        list(map(lambda x: self.print_formatted(x[0]), arr))
