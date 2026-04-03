# app/infrastructure/repositories/in_memory_vote_repository.py
from __future__ import annotations

from typing import List

from app.domain.entities.vote import Vote
from app.domain.repositories.vote_repository import VoteRepository


class InMemoryVoteRepository(VoteRepository):
    """
    Implementacao concreta de repositorio usando vetor (lista) em memoria.
    Ideal para prototipacao e testes. Pode ser substituida por implementacao
    com banco de dados sem alterar a camada de dominio.
    """

    def __init__(self) -> None:
        self._votes: List[Vote] = []

    def save(self, vote: Vote) -> Vote:
        self._votes.append(vote)
        return vote

    def find_all(self) -> List[Vote]:
        return list(self._votes)

    def count(self) -> int:
        return len(self._votes)

    def average(self) -> float:
        if not self._votes:
            return 0.0
        total = sum(vote.score_value for vote in self._votes)
        return total / len(self._votes)