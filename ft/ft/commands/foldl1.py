#!/usr/bin/env python3

from ft.types import T_ARRAY
from ft.commands.foldl import Foldl


class Foldl1(Foldl):
    def __init__(self):
        super().__init__("foldl1")

    def initialize(self):
        self.acc = None

    def handle_input(self, value):
        if value.fttype == T_ARRAY and self.column is not None:
            idx = self.column - 1
            val = self.value[idx]
        else:
            val = value

        if self.acc is None:
            self.acc = val
        else:
            self.acc = self.function(val, self.acc)
