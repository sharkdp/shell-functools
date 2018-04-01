#!/usr/bin/env python3

from ft.types import T_BOOL, T_ARRAY
from ft.error import panic
from ft.command import Command


class Filter(Command):
    def __init__(self):
        super().__init__("filter")

    def handle_input(self, value):
        val_to_test = value
        if self.column and value.fttype == T_ARRAY:
            val_to_test = value.value[self.column - 1]

        result = self.function(val_to_test)

        if result.fttype == T_BOOL:
            if result.value:
                self.print_formatted(value)
        else:
            panic("The filter function needs to return a 'Bool', got '{}'".format(result.fttype))
