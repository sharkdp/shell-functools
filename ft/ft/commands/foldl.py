#!/usr/bin/env python3

from ft.types import T_ARRAY
from ft.internal import ftformat, add_dynamic_type
from ft.command import Command
from ft.error import panic


class Foldl(Command):
    def __init__(self):
        super().__init__("foldl")
        self.use_currying = False

    def initialize(self):
        # Initial value
        if len(self.arguments) != 1:
            panic("Initial value to foldl is required")

        self.acc = add_dynamic_type(self.arguments[0])

    def handle_input(self, value):
        if value.fttype == T_ARRAY and self.column is not None:
            idx = self.column - 1
            self.acc = self.function(value.value[idx], self.acc)
        else:
            self.acc = self.function(value, self.acc)

    def finalize(self):
        out = ftformat(self.acc)

        if out:
            print(out)
