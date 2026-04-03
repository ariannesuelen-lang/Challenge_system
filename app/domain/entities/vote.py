# app/domain/entities/vote.py
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone

from app.domain.value_objects.vote_score import VoteScore


@dataclass
class Vote:
    """
    Entidade raiz do agregado de Votacao.
    Representa um unico voto com identificacao unica, nota e timestamp.
    """

    score: VoteScore = field(repr=False)
    vote_id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc),
        repr=False,
    )

    @property
    def score_value(self) -> float:
        return self.score.value

    def __post_init__(self) -> None:
        if not isinstance(self.score, VoteScore):
            raise TypeError("score must be an instance of VoteScore")