import argparse

from ft.types import T_ARRAY
from ft.command import Command

class Max(Command):
    def __init__(self):
        super().__init__("max")
        self.max_value = None

    def handle_input(self, value):
        # We can pretty much ignore the value return by self.function
        # since we use the `identity` function
        if value.fttype == T_ARRAY and self.column is not None:
            idx = self.column - 1
            value.value[idx] = self.function(value.value[idx])
            result = value
        else:
            result = self.function(value)

        if self.max_value is None:
            self.max_value = result
        else:
            self.max_value = max(self.max_value, result)

    def finalize(self):
        self.print_formatted(self.max_value)

    # def add_command_arguments(self, parser):
    #     # Let's monkey-patch the function argument to the `identity` function. 
    #     # `max` do not take any function.
    #     parser.add_argument('function', help='the function to run for each input',
    #                         default='identity', nargs='?')
    #     return parser