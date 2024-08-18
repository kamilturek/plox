from typing import Self

from plox.token import Token
from plox.token_type import TokenType


class TestToken:
    def test_str(self: Self) -> None:
        token = Token(
            type=TokenType.NUMBER,
            lexeme="123.56",
            literal=123.56,
            line=1,
        )

        assert str(token) == "TokenType.NUMBER 123.56 123.56"
