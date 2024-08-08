from dataclasses import dataclass
from typing import Any, Self

from plox.token_type import TokenType


@dataclass(frozen=True)
class Token:
    type: TokenType
    lexeme: str
    literal: Any
    line: int

    def __str__(self: Self) -> str:
        return f"{self.type} {self.lexeme} {self.literal}"
