# app/domain/repositories/vote_repository.py
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from app.domain.entities.vote import Vote


class VoteRepository(ABC):
    """
    Interface de repositorio seguindo Dependency Inversion Principle.
    A camada de dominio nao deve depender de implementacoes concretas.
    """

    @abstractmethod
    def save(self, vote: Vote) -> Vote:
        """Persiste um voto e retorna o voto salvo."""

    @abstractmethod
    def find_all(self) -> List[Vote]:
        """Retorna todos os votos armazenados."""

    @abstractmethod
    def count(self) -> int:
        """Retorna a quantidade total de votos."""

    @abstractmethod
    def average(self) -> float:
        """Retorna a media das notas. Retorna 0.0 se nao houver votos."""