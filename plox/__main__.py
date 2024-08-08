import argparse
import os
import pathlib
import sys
from typing import Self


class Lox:
    def __init__(self: Self) -> None:
        self._had_error = False

    def run_file(self: Self, path: str) -> None:
        self.run(pathlib.Path(path).read_text())

    def run_prompt(self: Self) -> None:
        while True:
            try:
                line = input("> ")
            except EOFError:
                break

            self.run(line)
            self.had_error = False

    def run(self: Self, _: str) -> None:
        if self.had_error is True:
            sys.exit(os.EX_DATAERR)

    def error(self: Self, line: int, message: str) -> None:
        self.report(line=line, where="", message=message)

    def report(self: Self, line: int, where: str, message: str) -> None:
        print(f"[line {line}] Error {where}: {message}")
        self.had_error = True


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
