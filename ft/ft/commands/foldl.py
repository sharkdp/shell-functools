#!/usr/bin/env python3

from ft.types import T_ARRAY
from ft.internal import add_dynamic_type
from ft.command import Command
from ft.error import panic


class Foldl(Command):
    def __init__(self, name="foldl"):
        super().__init__(name)

    def partial_application(self):
        # Skip partial application
        pass

    def initialize(self):
        # Initial value
        if len(self.arguments) != 1:
            panic("Initial value to foldl is required")

        self.acc = add_dynamic_type(self.arguments[0])

    def handle_input(self, inp):
        if inp.fttype == T_ARRAY and self.column is not None:
            idx = self.column - 1
            value = inp.value[idx]
        else:
            value = inp

        if self.acc is None:
            self.acc = value
        else:
            self.acc = self.function(value, self.acc)

    def finalize(self):
        self.print_formatted(self.acc)
