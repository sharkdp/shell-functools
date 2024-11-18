import sys
import argparse
import signal

from functools import partial

from ft.functions import function_list
from ft.internal import add_dynamic_type, ftformat
from ft.error import panic


class Command:
    def __init__(self, name):
        self.name = name
        self.column = None
        self.arguments = None
        self.function = None
        self.exit_early = False

        self.configure_broken_pipe()

    @staticmethod
    def configure_broken_pipe():
        # Use the default behavior (exit quietly) when catching SIGPIPE
        if hasattr(signal, 'SIGPIPE'):
            signal.signal(signal.SIGPIPE, signal.SIG_DFL)

    def get_argument_parser(self):
        parser = argparse.ArgumentParser(description=self.name)
        parser.add_argument("function", help="the function to run for each input")
        parser.add_argument("args", help="optional arguments", nargs="*")
        parser.add_argument(
            "--column", "-c", type=int, help="apply function to a specific column"
        )

        parser = self.add_command_arguments(parser)

        return parser

    def add_command_arguments(self, parser):
        return parser

    def parse_additional_command_arguments(self, args):
        pass

    def parse_args(self):
        parser = self.get_argument_parser()

        args = parser.parse_args()
        self.column = args.column
        self.arguments = args.args

        self.parse_additional_command_arguments(args)

        function_name = args.function
        try:
            self.function = function_list[function_name]
        except KeyError:
            panic("Function not found: '{}'".format(function_name))

    def partial_application(self):
        # Partially apply the command to the given arguments
        if len(self.arguments) > 0:
            args = map(add_dynamic_type, self.arguments)
            self.function = partial(self.function, *args)

    def input_lines(self):
        for line in sys.stdin:
            # Strip newline symbols
            if line.endswith("\r\n"):
                line = line[:-2]
            if line.endswith("\n"):
                line = line[:-1]

            yield line

    def print_formatted(self, result):
        if result.value is not None:
            formatted = ftformat(result)
            print(formatted, flush=True)

    def handle_input(self, value):
        raise NotImplementedError

    def initialize(self):
        pass

    def finalize(self):
        pass

    def run(self):
        # Handle command line arguments
        self.parse_args()
        self.partial_application()

        self.initialize()

        # Read from standard input
        for line in self.input_lines():
            value = add_dynamic_type(line)

            self.handle_input(value)

            if self.exit_early:
                break

        self.finalize()

    @classmethod
    def main(cls):
        return cls().run()
