import sys
from ft.termcolor import colored


def panic(msg):
    sys.stderr.write("{} {}\n".format(colored("[functools error]", "red"), msg))
    sys.exit(1)
