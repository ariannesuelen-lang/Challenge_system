# app/presentation/routes/vote_router.py
from fastapi import APIRouter, HTTPException, Request, status, Depends
from typing import cast, Annotated

from app.application.dtos.vote_dtos import (
    RegisterVoteInputDTO,
    VoteStatisticsOutputDTO,
    VoteListOutputDTO,
)
from app.application.use_cases.register_vote_use_case import (
    RegisterVoteUseCase,
    GetAllVotesUseCase,
    GetVoteStatisticsUseCase,
)
from app.domain.exceptions.vote_exceptions import (
    VoteBelowMinimumError,
    VoteAboveMaximumError,
    VoteDomainError,
)
from app.presentation.schemas.vote_schema import (
    VoteRequestSchema,
    VoteResponseSchema,
    VoteStatsResponseSchema,
    VoteListResponseSchema,
    ErrorResponseSchema,
)
from app.infrastructure.rate_limiter.rate_limit_config import limiter

vote_router = APIRouter(prefix="/api/v1/votes", tags=["Votacao"])


def _get_register_use_case(request: Request) -> RegisterVoteUseCase:
    return cast(RegisterVoteUseCase, request.app.state.register_vote_use_case)


def _get_list_use_case(request: Request) -> GetAllVotesUseCase:
    return cast(GetAllVotesUseCase, request.app.state.get_all_votes_use_case)


def _get_stats_use_case(request: Request) -> GetVoteStatisticsUseCase:
    return cast(
        GetVoteStatisticsUseCase,
        request.app.state.get_vote_statistics_use_case,
    )


@vote_router.post(
    "/",
    response_model=VoteResponseSchema,
    responses={
        400: {"model": ErrorResponseSchema, "description": "Nota invalida"},
        422: {
            "model": ErrorResponseSchema,
            "description": "Erro de validacao do payload",
        },
        429: {
            "model": ErrorResponseSchema,
            "description": "Limite de requisicoes excedido",
        },
    },
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("10/minute")
async def create_vote(
    request: Request,
    payload: Annotated[VoteRequestSchema, Depends()],
):
    """
    Registra um novo voto com nota de 0 a 10.
    O minimo aceito para registro e 0.2.
    """
    use_case = _get_register_use_case(request)

    try:
        input_dto = RegisterVoteInputDTO(score=payload.score)
        result = use_case.execute(input_dto)
        return VoteResponseSchema(
            vote_id=result.vote_id,
            score=result.score,
            created_at=result.created_at,
            message="Voto registrado com sucesso.",
        )
    except VoteBelowMinimumError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "NOTA_ABAIXO_DO_MINIMO",
                "message": str(exc),
                "status_code": 400,
            },
        )
    except VoteAboveMaximumError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "NOTA_ACIMA_DO_MAXIMO",
                "message": str(exc),
                "status_code": 400,
            },
        )
    except VoteDomainError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "ERRO_DE_DOMINIO",
                "message": str(exc),
                "status_code": 400,
            },
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error": "VALIDACAO_FALHOU",
                "message": str(exc),
                "status_code": 422,
            },
        )


@vote_router.get(
    "/",
    response_model=VoteListResponseSchema,
    responses={
        200: {"model": VoteListResponseSchema, "description": "Lista de votos"},
    },
)
@limiter.limit("20/minute")
async def list_votes(request: Request):
    """Retorna todos os votos registrados."""
    use_case = _get_list_use_case(request)
    result = use_case.execute()
    vote_responses = [
        VoteResponseSchema(
            vote_id=v.vote_id,
            score=v.score,
            created_at=v.created_at,
            message="",
        )
        for v in result.votes
    ]
    return VoteListResponseSchema(votes=vote_responses, total=result.total)


@vote_router.get(
    "/statistics",
    response_model=VoteStatsResponseSchema,
    responses={
        200: {
            "model": VoteStatsResponseSchema,
            "description": "Estatisticas de votacao",
        },
    },
)
@limiter.limit("30/minute")
async def get_statistics(request: Request):
    """Retorna estatisticas agregadas dos votos."""
    use_case = _get_stats_use_case(request)
    result = use_case.execute()
    return VoteStatsResponseSchema(
        total_votes=result.total_votes,
        average_score=result.average_score,
        min_score=result.min_score,
        max_score=result.max_score,
    )