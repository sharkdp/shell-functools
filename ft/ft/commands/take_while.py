#!/usr/bin/env python3

from ft.commands.filter import Filter


class TakeWhile(Filter):
    def __init__(self):
        super().__init__("take_while")
        self.exit_when_false = True
