#!/usr/bin/env python3

from ft.types import T_BOOL, T_ARRAY
from ft.error import panic
from ft.command import Command


class Filter(Command):
    def __init__(self, name="filter"):
        super().__init__(name)
        self.exit_when_false = False
        self.negate_predicate = False

    def add_command_arguments(self, parser):
        parser.add_argument(
            "--negate", "-n", action="store_true", help="negate predicate"
        )
        return parser

    def parse_additional_command_arguments(self, args):
        self.negate_predicate = args.negate

    def handle_input(self, value):
        val_to_test = value
        if self.column and value.fttype == T_ARRAY:
            val_to_test = value.value[self.column - 1]

        result = self.function(val_to_test)

        if result.fttype == T_BOOL:
            if self.negate_predicate:
                result.value = not result.value
            if result.value:
                self.print_formatted(value)
            else:
                if self.exit_when_false:
                    self.exit_early = True
        else:
            panic(
                "The function argument to '{}' needs to return a 'Bool', got '{}'".format(
                    self.name, result.fttype
                )
            )
