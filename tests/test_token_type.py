from typing import Self

from plox.token_type import TokenType


class TestTokenType:
    def test_repr(self: Self) -> None:
        assert repr(TokenType.NUMBER) == "TokenType.NUMBER"
