# app/presentation/routes/vote_router.py

from fastapi import APIRouter, HTTPException, Request, status, Depends
from typing import cast, Annotated, Dict
from enum import Enum
from pydantic import BaseModel

from app.application.dtos.vote_dtos import (
    RegisterVoteInputDTO,
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
    VoteResponseSchema,
    VoteStatsResponseSchema,
    VoteListResponseSchema,
    ErrorResponseSchema,
)
from app.infrastructure.rate_limiter.rate_limit_config import limiter


vote_router = APIRouter(prefix="/api/v1/votes", tags=["Votacao"])


# =========================
# ENUM + SCHEMA DE ENTRADA
# =========================
class VoteOption(str, Enum):
    BOM = "BOM"
    REGULAR = "REGULAR"
    RUIM = "RUIM"


class VoteRequestSchema(BaseModel):
    score: VoteOption


# =========================
# MAPEAMENTO
# =========================
VOTE_MAPPING = {
    VoteOption.RUIM: 1.0,
    VoteOption.REGULAR: 5.0,
    VoteOption.BOM: 10.0,
}


# =========================
# FUNÇÕES AUXILIARES
# =========================
def _get_register_use_case(request: Request) -> RegisterVoteUseCase:
    return cast(RegisterVoteUseCase, request.app.state.register_vote_use_case)


def _get_list_use_case(request: Request) -> GetAllVotesUseCase:
    return cast(GetAllVotesUseCase, request.app.state.get_all_votes_use_case)


def _get_stats_use_case(request: Request) -> GetVoteStatisticsUseCase:
    return cast(
        GetVoteStatisticsUseCase,
        request.app.state.get_vote_statistics_use_case,
    )


# =========================
# ENDPOINT: CRIAR VOTO
# =========================
@vote_router.post(
    "/",
    response_model=VoteResponseSchema,
    responses={
        400: {"model": ErrorResponseSchema},
        422: {"model": ErrorResponseSchema},
        429: {"model": ErrorResponseSchema},
    },
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("10/minute")
async def create_vote(
    request: Request,
    payload: Annotated[VoteRequestSchema, Depends()],
):
    use_case = _get_register_use_case(request)

    try:
        mapped_score = VOTE_MAPPING[payload.score]

        input_dto = RegisterVoteInputDTO(score=mapped_score)
        result = use_case.execute(input_dto)

        return VoteResponseSchema(
            vote_id=result.vote_id,
            score=result.score,
            created_at=result.created_at,
            message=f"Voto '{payload.score}' registrado com sucesso.",
        )

    except VoteBelowMinimumError as exc:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "NOTA_ABAIXO_DO_MINIMO",
                "message": str(exc),
                "status_code": 400,
            },
        )
    except VoteAboveMaximumError as exc:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "NOTA_ACIMA_DO_MAXIMO",
                "message": str(exc),
                "status_code": 400,
            },
        )
    except VoteDomainError as exc:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "ERRO_DE_DOMINIO",
                "message": str(exc),
                "status_code": 400,
            },
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "VALIDACAO_FALHOU",
                "message": str(exc),
                "status_code": 422,
            },
        )


# =========================
# ENDPOINT: ESTATÍSTICAS
# =========================
@vote_router.get(
    "/statistics",
    response_model=VoteStatsResponseSchema,
)
@limiter.limit("30/minute")
async def get_statistics(request: Request):
    use_case = _get_stats_use_case(request)
    result = use_case.execute()

    return VoteStatsResponseSchema(
        total_votes=result.total_votes,
        average_score=result.average_score,
        min_score=result.min_score,
        max_score=result.max_score,
    )


# =========================
# SUMMARY (INTEGRADO)
# =========================
class VoteSummaryResponseSchema(BaseModel):
    total: int
    count: Dict[str, int]
    percentage: Dict[str, float]
    average: float
    category_average: Dict[str, float]
    difference: Dict[str, Dict[str, float]]


@vote_router.get(
    "/summary",
    response_model=VoteSummaryResponseSchema,
)
@limiter.limit("30/minute")
async def get_vote_summary(request: Request):
    """
    Retorna estatisticas completas (Google Forms style),
    reutilizando o Domain Service via UseCase.
    """

    use_case = _get_stats_use_case(request)
    result = use_case.execute()

    return VoteSummaryResponseSchema(
        total=result.total_votes,
        count=result.count,
        percentage=result.percentage,
        average=result.average_score,
        category_average=result.category_average,
        difference=result.difference,
    )
