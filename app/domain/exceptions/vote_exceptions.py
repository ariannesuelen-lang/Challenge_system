# app/domain/exceptions/vote_exceptions.py
from __future__ import annotations


class VoteDomainError(Exception):
    """Excecao base para erros de dominio de votacao."""

    pass


class VoteBelowMinimumError(VoteDomainError):
    """Erro quando a nota e menor que o minimo permitido (0.2)."""

    def __init__(self, minimum: float, provided: float) -> None:
        self.minimum = minimum
        self.provided = provided
        message = (
            f"A nota informada ({provided}) e inferior ao minimo permitido "
            f"({minimum}). O valor minimo para registro de voto e {minimum}."
        )
        super().__init__(message)


class VoteAboveMaximumError(VoteDomainError):
    """Erro quando a nota e maior que o maximo permitido (10.0)."""

    def __init__(self, maximum: float, provided: float) -> None:
        self.maximum = maximum
        self.provided = maximum
        message = (
            f"A nota informada ({provided}) e superior ao maximo permitido "
            f"({maximum}). O valor maximo para registro de voto e {maximum}."
        )
        super().__init__(message)


class VoteNotFoundError(VoteDomainError):
    """Erro quando nenhum voto e encontrado."""

    def __init__(self) -> None:
        message = "Nenhum voto registrado no sistema."
        super().__init__(message)