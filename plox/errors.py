from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, Self

if TYPE_CHECKING:
    from _typeshed import SupportsWrite


class ErrorReporter(Protocol):
    had_error: bool

    def error(self: Self, line: int, message: str) -> None: ...


class TextErrorReporter(ErrorReporter):
    def __init__(self: Self, out: SupportsWrite[str]) -> None:
        self.had_error = False
        self._out = out

    def error(self: Self, line: int, message: str) -> None:
        self._report(line=line, where="", message=message)

    def _report(self: Self, line: int, where: str, message: str) -> None:
        print(f"[line {line}] Error {where}: {message}", file=self._out)
        self.had_error = True


class ListErrorReporter(ErrorReporter):
    def __init__(self: Self) -> None:
        self.had_error = False
        self.errors = []

    def error(self: Self, line: int, message: str) -> None:
        self._report(line=line, where="", message=message)

    def _report(self: Self, line: int, where: str, message: str) -> None:
        self.errors.append(f"[line {line}] Error {where}: {message}")
        self.had_error = True
