from ft.internal import ftformat
from ft.functions import function_list


def mock(cmd, input=None, **params):
    def set_input(self, function_name, arguments, input_lines):
        self.function = function_list[function_name]
        self.arguments = arguments
        self._input = input_lines
        self._output = []

    def parse_args(self):
        pass

    def input_lines(self):
        for line in self._input:
            yield line

    def print_formatted(self, value):
        self._output.append(ftformat(value))

    def output(self):
        self.run()
        return self._output

    cmd.set_input = set_input
    cmd.parse_args = parse_args
    cmd.print_formatted = print_formatted
    cmd.input_lines = input_lines
    cmd.output = output

    cmd = cmd()
    if input:
        cmd.set_input(*input)
    for k, v in params.items():
        setattr(cmd, k, v)
    return cmd
