# app/domain/value_objects/vote_score.py
from __future__ import annotations

from app.config import settings
from app.domain.exceptions.vote_exceptions import (
    VoteBelowMinimumError,
    VoteAboveMaximumError,
)


class VoteScore:
    """
    Value Object que encapsula a validacao da nota de votacao.
    Regras:
      - Nota minima valida: 0.2
      - Nota maxima valida: 10.0
      - Qualquer valor abaixo de 0.2 gera VoteBelowMinimumError
      - Qualquer valor acima de 10.0 gera VoteAboveMaximumError
    """

    def __init__(self, value: float) -> None:
        self._validate(value)
        self._value = value

    @classmethod
    def from_float(cls, value: float) -> VoteScore:
        return cls(value)

    def _validate(self, value: float) -> None:
        if value < settings.min_vote_score:
            raise VoteBelowMinimumError(
                minimum=settings.min_vote_score,
                provided=value,
            )
        if value > settings.max_vote_score:
            raise VoteAboveMaximumError(
                maximum=settings.max_vote_score,
                provided=value,
            )

    @property
    def value(self) -> float:
        return self._value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, VoteScore):
            return NotImplemented
        return self._value == other._value

    def __repr__(self) -> str:
        return f"VoteScore(value={self._value})"

    def __hash__(self) -> int:
        return hash(self._value)