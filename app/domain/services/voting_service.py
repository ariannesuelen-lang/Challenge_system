# app/domain/services/voting_service.py
from __future__ import annotations

from typing import List

from app.domain.entities.vote import Vote
from app.domain.repositories.vote_repository import VoteRepository
from app.domain.value_objects.vote_score import VoteScore


class VotingService:
    """
    Domain Service responsavel pelas regras de negocio de votacao.
    Centraliza logica que envolve entidades e repositorios.
    """

    def __init__(self, vote_repository: VoteRepository) -> None:
        self._repository = vote_repository

    def register_vote(self, score_value: float) -> Vote:
        """
        Cria e persiste um novo voto.
        """
        score = VoteScore.from_float(score_value)
        vote = Vote(score=score)
        return self._repository.save(vote)

    def get_all_votes(self) -> List[Vote]:
        """Retorna todos os votos registrados."""
        return self._repository.find_all()

    def get_statistics(self) -> dict:
        """Retorna estatisticas agregadas dos votos."""
        votes = self._repository.find_all()
        if not votes:
            return {
                "total_votes": 0,
                "average_score": 0.0,
                "min_score": 0.0,
                "max_score": 0.0,
            }

        scores = [vote.score_value for vote in votes]
        return {
            "total_votes": len(scores),
            "average_score": round(sum(scores) / len(scores), 2),
            "min_score": min(scores),
            "max_score": max(scores),
        }