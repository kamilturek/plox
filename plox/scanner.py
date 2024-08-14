from typing import Any, Self

from plox.errors import ErrorReporter
from plox.token import Token
from plox.token_type import TokenType


class Scanner:
    def __init__(self: Self, source: str, error_reporter: ErrorReporter) -> None:
        self._source = source
        self._error_reporter = error_reporter

        self._tokens: list[Token] = []
        self._start = 0
        self._current = 0
        self._line = 1

    def scan_tokens(self: Self) -> list[Token]:
        while not self._is_at_end():
            self._start = self._current
            self._scan_token()

        self._tokens.append(
            Token(
                type=TokenType.EOF,
                lexeme="",
                literal=None,
                line=self._line,
            ),
        )

        return self._tokens

    def _is_at_end(self: Self) -> bool:
        return self.current >= len(self._source)

    def _scan_token(self: Self) -> None:
        match self._advance():
            case "(":
                self._add_token(TokenType.LEFT_PAREN)
            case ")":
                self._add_token(TokenType.RIGHT_PAREN)
            case "{":
                self._add_token(TokenType.LEFT_BRACE)
            case "}":
                self._add_token(TokenType.RIGHT_BRACE)
            case ",":
                self._add_token(TokenType.COMMA)
            case ".":
                self._add_token(TokenType.DOT)
            case "-":
                self._add_token(TokenType.MINUS)
            case "+":
                self._add_token(TokenType.PLUS)
            case ";":
                self._add_token(TokenType.SEMICOLON)
            case "*":
                self._add_token(TokenType.SEMICOLON)
            case _:
                self._error_reporter.error(self._line, "Unexpected character.")

    def _advance(self: Self) -> str:
        char = self._source[self._current]
        self._current += 1
        return char

    def _add_token(self: Self, token_type: TokenType, literal: Any = None) -> None:
        self._tokens.append(
            Token(
                type=token_type,
                lexeme=self._source[self._start : self._current],
                literal=literal,
                line=self._line,
            ),
        )
