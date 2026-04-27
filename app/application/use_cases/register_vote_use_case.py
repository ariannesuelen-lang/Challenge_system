# app/application/use_cases/register_vote_use_case.py
from __future__ import annotations

from app.application.dtos.vote_dtos import (
    RegisterVoteInputDTO,
    VoteOutputDTO,
    VoteStatisticsOutputDTO,
    VoteListOutputDTO,
)
from app.domain.services.voting_service import VotingService


class RegisterVoteUseCase:
    """
    Use Case de registro de voto.
    Encapsula o fluxo de aplicacao completo.
    """

    def __init__(self, voting_service: VotingService) -> None:
        self._voting_service = voting_service

    def execute(self, input_dto: RegisterVoteInputDTO) -> VoteOutputDTO:
        vote = self._voting_service.register_vote(
            input_dto.score, input_dto.student_name
        )
        return VoteOutputDTO(
            vote_id=str(vote.vote_id),
            score=vote.score_value,
            created_at=vote.created_at.isoformat(),
        )


class GetAllVotesForTeacherUseCase:
    """Use Case que retorna todos os votos incluindo o nome do aluno.
    Deve ser protegido e utilizado somente pelo professor.
    """

    def __init__(self, voting_service: VotingService) -> None:
        self._voting_service = voting_service

    def execute(self):
        votes = self._voting_service.get_all_votes()
        vote_dtos = [
            VoteOutputDTO(
                vote_id=str(v.vote_id),
                score=v.score_value,
                created_at=v.created_at.isoformat(),
            )
            for v in votes
        ]

        # Additionally return raw objects for teacher view (including student_name)
        # The presentation layer will access student_name directly from entities.
        return votes


class GetAllVotesUseCase:
    """Use Case para listar todos os votos."""

    def __init__(self, voting_service: VotingService) -> None:
        self._voting_service = voting_service

    def execute(self) -> VoteListOutputDTO:
        votes = self._voting_service.get_all_votes()
        vote_dtos = [
            VoteOutputDTO(
                vote_id=str(v.vote_id),
                score=v.score_value,
                created_at=v.created_at.isoformat(),
            )
            for v in votes
        ]
        return VoteListOutputDTO(votes=vote_dtos, total=len(vote_dtos))


class GetVoteStatisticsUseCase:
    """Use Case para obter estatisticas de votacao."""

    def __init__(self, voting_service: VotingService) -> None:
        self._voting_service = voting_service

    def execute(self) -> VoteStatisticsOutputDTO:
        stats = self._voting_service.get_statistics()
        return VoteStatisticsOutputDTO(**stats)