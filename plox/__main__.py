import argparse
import os
import pathlib
import sys
from typing import Self

from plox.errors import ErrorReporter


class Lox:
    def __init__(self: Self, error_reporter: ErrorReporter) -> None:
        self._error_reporter = error_reporter

    def run_file(self: Self, path: str) -> None:
        self.run(pathlib.Path(path).read_text())

    def run_prompt(self: Self) -> None:
        while True:
            try:
                line = input("> ")
            except EOFError:
                break

            self.run(line)
            self._error_reporter.had_error = False

    def run(self: Self, _: str) -> None:
        if self._error_reporter.had_error is True:
            sys.exit(os.EX_DATAERR)


def main() -> None:
    parser = argparse.ArgumentParser("plox")
    parser.add_argument("script", nargs="?")
    args = parser.parse_args()

    lox = Lox()

    if args.script is not None:
        lox.run_file(args.script)
    else:
        lox.run_prompt()


if __name__ == "__main__":
    main()
