from ft.types import T_ARRAY
from ft.command import Command


class SortBy(Command):
    def __init__(self):
        super().__init__("sort_by")
        self.arr = []

    def handle_input(self, value):
        val = value
        if value.fttype == T_ARRAY and self.column is not None:
            val = value.value[self.column - 1]

        result = self.function(val)
        self.arr.append((val, result))

    def finalize(self):
        arr = sorted(self.arr, key=lambda x: x[1])
        list(map(lambda x: self.print_formatted(x[0]), arr))
