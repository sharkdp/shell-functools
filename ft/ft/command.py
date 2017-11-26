import argparse
from functools import partial

from ft.functions import function_list
from ft.internal import add_dynamic_type, input_values
from ft.error import panic


class Command:
    def __init__(self, name):
        self.name = name
        self.use_currying = True
        self.parser = argparse.ArgumentParser(description=self.name)

    def add_common_arguments(self):
        self.parser.add_argument('function', help='the function to run for each input')
        self.parser.add_argument('args', help='optional arguments', nargs='*')
        self.parser.add_argument('--column', '-c', type=int,
                                 help='apply function to a specific column')

    def add_command_arguments(self):
        pass

    def parse_args(self):
        self.add_common_arguments()
        self.add_command_arguments()

        args = self.parser.parse_args()

        function_name = args.function
        self.column = args.column
        self.arguments = args.args

        try:
            self.function = function_list[function_name]
        except KeyError:
            panic("Function not found: '{}'".format(function_name))

        if self.use_currying:
            # Partially apply the command
            if len(args.args) > 0:
                args = map(add_dynamic_type, args.args)
                self.function = partial(self.function, *args)

    def handle_input(self, value):
        raise NotImplementedError

    def initialize(self):
        pass

    def finalize(self):
        pass

    def run(self):
        self.parse_args()

        self.initialize()

        for value in input_values():
            self.handle_input(value)

        self.finalize()
