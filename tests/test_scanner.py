from typing import Self

import pytest

from plox.errors import ListErrorReporter, TextErrorReporter
from plox.scanner import Scanner
from plox.token import Token
from plox.token_type import TokenType


class TestScanner:
    @pytest.mark.parametrize(
        ("source", "expected_tokens"),
        [
            pytest.param(
                "+-*/(){},.;",
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
                        type=TokenType.LEFT_PAREN,
                        lexeme="(",
                        literal=None,
                        line=1,
                    ),
                    Token(
                        type=TokenType.RIGHT_PAREN,
                        lexeme=")",
                        literal=None,
                        line=1,
                    ),
                    Token(
                        type=TokenType.LEFT_BRACE,
                        lexeme="{",
                        literal=None,
                        line=1,
                    ),
                    Token(
                        type=TokenType.RIGHT_BRACE,
                        lexeme="}",
                        literal=None,
                        line=1,
                    ),
                    Token(
                        type=TokenType.COMMA,
                        lexeme=",",
                        literal=None,
                        line=1,
                    ),
                    Token(
                        type=TokenType.DOT,
                        lexeme=".",
                        literal=None,
                        line=1,
                    ),
                    Token(
                        type=TokenType.SEMICOLON,
                        lexeme=";",
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
                id="basic tokens",
            ),
            pytest.param(
                "= == < <= >= != !",
                [
                    Token(
                        type=TokenType.EQUAL,
                        lexeme="=",
                        literal=None,
                        line=1,
                    ),
                    Token(
                        type=TokenType.EQUAL_EQUAL,
                        lexeme="==",
                        literal=None,
                        line=1,
                    ),
                    Token(
                        type=TokenType.LESS,
                        lexeme="<",
                        literal=None,
                        line=1,
                    ),
                    Token(
                        type=TokenType.LESS_EQUAL,
                        lexeme="<=",
                        literal=None,
                        line=1,
                    ),
                    Token(
                        type=TokenType.GREATER_EQUAL,
                        lexeme=">=",
                        literal=None,
                        line=1,
                    ),
                    Token(
                        type=TokenType.BANG_EQUAL,
                        lexeme="!=",
                        literal=None,
                        line=1,
                    ),
                    Token(
                        type=TokenType.BANG,
                        lexeme="!",
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
                id="one or two character tokens",
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
                """
                + /* first comment line
                     second comment line */
                """,
                [
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
                        line=4,
                    ),
                ],
                id="multi-line comment",
            ),
            pytest.param(
                '"this is a string"',
                [
                    Token(
                        type=TokenType.STRING,
                        lexeme='"this is a string"',
                        literal="this is a string",
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
                "111.",
                [
                    Token(
                        type=TokenType.NUMBER,
                        lexeme="111",
                        literal=111,
                        line=1,
                    ),
                    Token(
                        type=TokenType.DOT,
                        lexeme=".",
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
                id="integer and dot",
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
                """
                and class else false for
                fun if nil or print return
                super this true var while
                """,
                [
                    Token(
                        type=TokenType.AND,
                        lexeme="and",
                        literal=None,
                        line=2,
                    ),
                    Token(
                        type=TokenType.CLASS,
                        lexeme="class",
                        literal=None,
                        line=2,
                    ),
                    Token(
                        type=TokenType.ELSE,
                        lexeme="else",
                        literal=None,
                        line=2,
                    ),
                    Token(
                        type=TokenType.FALSE,
                        lexeme="false",
                        literal=None,
                        line=2,
                    ),
                    Token(
                        type=TokenType.FOR,
                        lexeme="for",
                        literal=None,
                        line=2,
                    ),
                    Token(
                        type=TokenType.FUN,
                        lexeme="fun",
                        literal=None,
                        line=3,
                    ),
                    Token(
                        type=TokenType.IF,
                        lexeme="if",
                        literal=None,
                        line=3,
                    ),
                    Token(
                        type=TokenType.NIL,
                        lexeme="nil",
                        literal=None,
                        line=3,
                    ),
                    Token(
                        type=TokenType.OR,
                        lexeme="or",
                        literal=None,
                        line=3,
                    ),
                    Token(
                        type=TokenType.PRINT,
                        lexeme="print",
                        literal=None,
                        line=3,
                    ),
                    Token(
                        type=TokenType.RETURN,
                        lexeme="return",
                        literal=None,
                        line=3,
                    ),
                    Token(
                        type=TokenType.SUPER,
                        lexeme="super",
                        literal=None,
                        line=4,
                    ),
                    Token(
                        type=TokenType.THIS,
                        lexeme="this",
                        literal=None,
                        line=4,
                    ),
                    Token(
                        type=TokenType.TRUE,
                        lexeme="true",
                        literal=None,
                        line=4,
                    ),
                    Token(
                        type=TokenType.VAR,
                        lexeme="var",
                        literal=None,
                        line=4,
                    ),
                    Token(
                        type=TokenType.WHILE,
                        lexeme="while",
                        literal=None,
                        line=4,
                    ),
                    Token(
                        type=TokenType.EOF,
                        lexeme="",
                        literal=None,
                        line=5,
                    ),
                ],
                id="keywords",
            ),
        ],
    )
    def test_scans_tokens(
        self: Self,
        source: str,
        expected_tokens: list[Token],
    ) -> None:
        error_reporter = ListErrorReporter()

        scanner = Scanner(
            source=source,
            error_reporter=error_reporter,
        )

        tokens = scanner.scan_tokens()

        assert error_reporter.had_error is False
        assert tokens == expected_tokens

    @pytest.mark.parametrize(
        ("source", "expected_errors"),
        [
            pytest.param(
                "@",
                ["[line 1] Error : Unexpected character: '@'."],
                id="unexpected character",
            ),
            pytest.param(
                '"this is a string',
                ["[line 1] Error : Unterminated string."],
                id="unterminated string",
            ),
        ],
    )
    def test_reports_errors(
        self: Self,
        source: str,
        expected_errors: list[str],
    ) -> None:
        error_reporter = ListErrorReporter()

        scanner = Scanner(
            source=source,
            error_reporter=error_reporter,
        )

        scanner.scan_tokens()

        assert error_reporter.had_error is True
        assert error_reporter.errors == expected_errors
