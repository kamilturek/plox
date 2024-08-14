from typing import Protocol, Self


class ErrorReporter(Protocol):
    had_error: bool

    def error(self: Self, line: int, message: str) -> None: ...


class StdoutErrorReporter(ErrorReporter):
    def __init__(self: Self) -> None:
        self.had_error = False

    def error(self: Self, line: int, message: str) -> None:
        self._report(line=line, where="", message=message)

    def _report(self: Self, line: int, where: str, message: str) -> None:
        print(f"[line {line}] Error {where}: {message}")
        self.had_error = True
