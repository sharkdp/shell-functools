from nose.tools import assert_equals

from ft.internal import ftformat
from ft.functions import function_list


def mock_command(cmd):
    def set_input(self, function_name, arguments, input_lines):
        self.function = function_list[function_name]
        self.arguments = arguments
        self.input = input_lines
        self.output = []

    def parse_args(self):
        pass

    def input_lines(self):
        for line in self.input:
            yield line

    def print_formatted(self, value):
        self.output.append(ftformat(value))

    def assert_output(self, expected):
        self.run()
        assert_equals(expected, self.output)

    cmd.set_input = set_input
    cmd.parse_args = parse_args
    cmd.print_formatted = print_formatted
    cmd.input_lines = input_lines
    cmd.assert_output = assert_output

    return cmd()
