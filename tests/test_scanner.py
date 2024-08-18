from typing import Self

import pytest

from plox.errors import StdoutErrorReporter
from plox.scanner import Scanner
from plox.token import Token
from plox.token_type import TokenType


class TestScanner:
    @pytest.mark.parametrize(
        ("source", "expected_tokens"),
        [
            pytest.param(
                "+-*/",
                [
                    Token(
                        type=TokenType.PLUS,
                        lexeme="+",
                        literal=None,
                        line=1,
                    ),
                    Token(
                        type=TokenType.MINUS,
                        lexeme="-",
                        literal=None,
                        line=1,
                    ),
                    Token(
                        type=TokenType.STAR,
                        lexeme="*",
                        literal=None,
                        line=1,
                    ),
                    Token(
                        type=TokenType.SLASH,
                        lexeme="/",
                        literal=None,
                        line=1,
                    ),
                    Token(
                        type=TokenType.EOF,
                        lexeme="",
                        literal=None,
                        line=1,
                    ),
                ],
                id="basic operators",
            ),
            pytest.param(
                "+// comment\n+",
                [
                    Token(
                        type=TokenType.PLUS,
                        lexeme="+",
                        literal=None,
                        line=1,
                    ),
                    Token(
                        type=TokenType.PLUS,
                        lexeme="+",
                        literal=None,
                        line=2,
                    ),
                    Token(
                        type=TokenType.EOF,
                        lexeme="",
                        literal=None,
                        line=2,
                    ),
                ],
                id="comment",
            ),
            pytest.param(
                '+ "this is a string" +',
                [
                    Token(
                        type=TokenType.PLUS,
                        lexeme="+",
                        literal=None,
                        line=1,
                    ),
                    Token(
                        type=TokenType.STRING,
                        lexeme='"this is a string"',
                        literal="this is a string",
                        line=1,
                    ),
                    Token(
                        type=TokenType.PLUS,
                        lexeme="+",
                        literal=None,
                        line=1,
                    ),
                    Token(
                        type=TokenType.EOF,
                        lexeme="",
                        literal=None,
                        line=1,
                    ),
                ],
                id="single-line string",
            ),
            pytest.param(
                '"first line\nsecond line"',
                [
                    Token(
                        type=TokenType.STRING,
                        lexeme='"first line\nsecond line"',
                        literal="first line\nsecond line",
                        line=2,
                    ),
                    Token(
                        type=TokenType.EOF,
                        lexeme="",
                        literal=None,
                        line=2,
                    ),
                ],
                id="multi-line string",
            ),
            pytest.param(
                "111",
                [
                    Token(
                        type=TokenType.NUMBER,
                        lexeme="111",
                        literal=111.0,
                        line=1,
                    ),
                    Token(
                        type=TokenType.EOF,
                        lexeme="",
                        literal=None,
                        line=1,
                    ),
                ],
                id="integer number",
            ),
            pytest.param(
                "111.222",
                [
                    Token(
                        type=TokenType.NUMBER,
                        lexeme="111.222",
                        literal=111.222,
                        line=1,
                    ),
                    Token(
                        type=TokenType.EOF,
                        lexeme="",
                        literal=None,
                        line=1,
                    ),
                ],
                id="floating point number",
            ),
            pytest.param(
                "one two three",
                [
                    Token(
                        type=TokenType.IDENTIFIER,
                        lexeme="one",
                        literal=None,
                        line=1,
                    ),
                    Token(
                        type=TokenType.IDENTIFIER,
                        lexeme="two",
                        literal=None,
                        line=1,
                    ),
                    Token(
                        type=TokenType.IDENTIFIER,
                        lexeme="three",
                        literal=None,
                        line=1,
                    ),
                    Token(
                        type=TokenType.EOF,
                        lexeme="",
                        literal=None,
                        line=1,
                    ),
                ],
                id="identifiers",
            ),
            pytest.param(
                "var else class if",
                [
                    Token(
                        type=TokenType.VAR,
                        lexeme="var",
                        literal=None,
                        line=1,
                    ),
                    Token(
                        type=TokenType.ELSE,
                        lexeme="else",
                        literal=None,
                        line=1,
                    ),
                    Token(
                        type=TokenType.CLASS,
                        lexeme="class",
                        literal=None,
                        line=1,
                    ),
                    Token(
                        type=TokenType.IF,
                        lexeme="if",
                        literal=None,
                        line=1,
                    ),
                    Token(
                        type=TokenType.EOF,
                        lexeme="",
                        literal=None,
                        line=1,
                    ),
                ],
                id="keywords",
            ),
        ],
    )
    def test_scan_tokens(self: Self, source: str, expected_tokens: list[Token]) -> None:
        error_reporter = StdoutErrorReporter()

        scanner = Scanner(
            source=source,
            error_reporter=error_reporter,
        )

        tokens = scanner.scan_tokens()

        assert error_reporter.had_error is False
        assert tokens == expected_tokens
