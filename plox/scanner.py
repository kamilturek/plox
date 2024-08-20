from typing import Any, Final, Self

from plox.errors import ErrorReporter
from plox.token import Token
from plox.token_type import TokenType

_KEYWORDS: Final[dict[str, TokenType]] = {
    "and": TokenType.AND,
    "class": TokenType.CLASS,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "for": TokenType.FOR,
    "fun": TokenType.FUN,
    "if": TokenType.IF,
    "nil": TokenType.NIL,
    "or": TokenType.OR,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "super": TokenType.SUPER,
    "this": TokenType.THIS,
    "true": TokenType.TRUE,
    "var": TokenType.VAR,
    "while": TokenType.WHILE,
}


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
        return self._current >= len(self._source)

    def _scan_token(self: Self) -> None:
        char = self._advance()
        match char:
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
                self._add_token(TokenType.STAR)
            case "!":
                self._add_token(
                    TokenType.BANG_EQUAL if self._match("=") else TokenType.BANG,
                )
            case "=":
                self._add_token(
                    TokenType.EQUAL_EQUAL if self._match("=") else TokenType.EQUAL,
                )
            case "<":
                self._add_token(
                    TokenType.LESS_EQUAL if self._match("=") else TokenType.LESS,
                )
            case ">":
                self._add_token(
                    TokenType.GREATER_EQUAL if self._match("=") else TokenType.GREATER,
                )
            case "/":
                # Ignore comments.
                if self._match("/"):
                    while self._peek() != "\n" and not self._is_at_end():
                        self._advance()
                elif self._match("*"):
                    self._scan_multiline_comment()
                else:
                    self._add_token(TokenType.SLASH)
            case " " | "\r" | "\t":
                pass
            case "\n":
                self._line += 1
            case '"':
                self._scan_string()
            case _:
                if char.isdigit():
                    self._scan_number()
                elif char.isalpha():
                    self._scan_identifier()
                else:
                    # TODO @kamilturek: Coalesce a run of invalid characters into
                    # a single error.
                    self._error_reporter.error(
                        self._line,
                        f"Unexpected character: {char!r}.",
                    )

    def _advance(self: Self) -> str:
        char = self._source[self._current]
        self._current += 1
        return char

    def _match(self: Self, expected: str) -> bool:
        if self._is_at_end() is True:
            return False

        if self._source[self._current] != expected:
            return False

        self._current += 1
        return True

    def _peek(self: Self) -> str:
        if self._is_at_end():
            return ""

        return self._source[self._current]

    def _peek_next(self: Self) -> str:
        if self._current + 1 >= len(self._source):
            return ""

        return self._source[self._current + 1]

    def _add_token(self: Self, token_type: TokenType, literal: Any = None) -> None:
        self._tokens.append(
            Token(
                type=token_type,
                lexeme=self._source[self._start : self._current],
                literal=literal,
                line=self._line,
            ),
        )

    def _scan_string(self: Self) -> None:
        while self._peek() != '"' and not self._is_at_end():
            if self._peek() == "\n":
                self._line += 1

            self._advance()

        if self._is_at_end():
            self._error_reporter.error(self._line, "Unterminated string.")
            return

        # Move behind the closing quote.
        self._advance()

        self._add_token(
            token_type=TokenType.STRING,
            # Trim the surrounding quotes.
            literal=self._source[self._start + 1 : self._current - 1],
        )

    def _scan_multiline_comment(self: Self) -> None:
        while (
            self._peek() != "*" or self._peek_next() != "/"
        ) and not self._is_at_end():
            if self._peek() == "\n":
                self._line += 1

            self._advance()

        if self._is_at_end():
            self._error_reporter.error(self._line, "Unterminated comment.")
            return

        # Move behind `*/`.
        self._advance()
        self._advance()

    def _scan_number(self: Self) -> None:
        while self._peek().isdigit():
            self._advance()

        # Look for a fractional part.
        if self._peek() == "." and self._peek_next().isdigit():
            # Consume the dot.
            self._advance()

            while self._peek().isdigit():
                self._advance()

        self._add_token(
            token_type=TokenType.NUMBER,
            literal=float(self._source[self._start : self._current]),
        )

    def _scan_identifier(self: Self) -> None:
        while self._peek().isalpha():
            self._advance()

        value = self._source[self._start : self._current]

        self._add_token(
            token_type=_KEYWORDS.get(value, TokenType.IDENTIFIER),
        )
