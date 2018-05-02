#!/usr/bin/env python3

from ft.types import T_BOOL, T_ARRAY
from ft.error import panic
from ft.command import Command
from ft.functions import function_list

class Filter(Command):
    def __init__(self, name="filter"):
        super().__init__(name)
        self.exit_when_false = False


    def add_command_arguments(self, parser):
        parser.add_argument('--negate', '-n',
                            action='store_true',
                            help='negate predicate')
        return parser

    def parse_args(self):
        parser = self.get_argument_parser()

        args = parser.parse_args()

        self.column = args.column
        self.arguments = args.args
        self.negate_predicate = args.negate

        function_name = args.function
        try:
            self.function = function_list[function_name]
        except KeyError:
            panic("Function not found: '{}'".format(function_name))

    def handle_input(self, value):
        val_to_test = value
        if self.column and value.fttype == T_ARRAY:
            val_to_test = value.value[self.column - 1]

        result = self.function(val_to_test)

        if result.fttype == T_BOOL:
            if hasattr(self, 'negate_predicate'):
                if self.negate_predicate:
                    result.value = not result.value
            if result.value:
                self.print_formatted(value)
            else:
                if self.exit_when_false:
                    self.exit_early = True
        else:
            panic("The function argument to '{}' needs to return a 'Bool', got '{}'"
                  .format(self.name, result.fttype))
