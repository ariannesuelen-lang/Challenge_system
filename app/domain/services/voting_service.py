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
    """Retorna estatisticas agregadas completas dos votos."""
    votes = self._repository.find_all()

    if not votes:
        return {
            "total_votes": 0,
            "average_score": 0.0,
            "min_score": 0.0,
            "max_score": 0.0,
            "count": {"BOM": 0, "REGULAR": 0, "RUIM": 0},
            "percentage": {"BOM": 0.0, "REGULAR": 0.0, "RUIM": 0.0},
            "category_average": {"BOM": 0.0, "REGULAR": 0.0, "RUIM": 0.0},
            "difference": {
                "BOM": {"BOM": 0.0, "REGULAR": 0.0, "RUIM": 0.0},
                "REGULAR": {"BOM": 0.0, "REGULAR": 0.0, "RUIM": 0.0},
                "RUIM": {"BOM": 0.0, "REGULAR": 0.0, "RUIM": 0.0},
            },
        }

    scores = [vote.score_value for vote in votes]

    total = len(scores)

    # =========================
    # CONTAGEM POR CATEGORIA
    # =========================
    count = {
        "BOM": 0,
        "REGULAR": 0,
        "RUIM": 0,
    }

    for score in scores:
        if score == 10.0:
            count["BOM"] += 1
        elif score == 5.0:
            count["REGULAR"] += 1
        elif score == 1.0:
            count["RUIM"] += 1

    # =========================
    # PORCENTAGEM
    # =========================
    percentage = {
        k: round((count[k] / total) * 100, 2)
        for k in count
    }

    # =========================
    # MÉDIA GERAL
    # =========================
    average = round(sum(scores) / total, 2)

    # =========================
    # MÉDIA POR CATEGORIA
    # =========================
    category_average = {
        "BOM": 10.0 if count["BOM"] else 0.0,
        "REGULAR": 5.0 if count["REGULAR"] else 0.0,
        "RUIM": 1.0 if count["RUIM"] else 0.0,
    }

    # =========================
    # DIFERENÇA ENTRE CATEGORIAS
    # =========================
    difference = {}
    for k1 in percentage:
        difference[k1] = {}
        for k2 in percentage:
            difference[k1][k2] = round(
                percentage[k1] - percentage[k2],
                2
            )

    return {
        # =========================
        # CAMPOS ANTIGOS (MANTIDOS)
        # =========================
        "total_votes": total,
        "average_score": average,
        "min_score": min(scores),
        "max_score": max(scores),

        # =========================
        # CAMPOS NOVOS (INTEGRAÇÃO)
        # =========================
        "count": count,
        "percentage": percentage,
        "category_average": category_average,
        "difference": difference,
    }
