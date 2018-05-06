#!/usr/bin/env python3

from ft.commands.foldl import Foldl


class Foldl1(Foldl):
    def __init__(self):
        super().__init__("foldl1")

    def initialize(self):
        self.acc = None
