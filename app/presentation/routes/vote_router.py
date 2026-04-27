# app/presentation/routes/vote_router.py

from fastapi import APIRouter, HTTPException, Request, status, Depends, Header
from typing import cast, Annotated, Dict, Optional
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
    StudentVoteRequestSchema,
    TeacherVoteListResponseSchema,
)
from app.config import settings
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
# ENDPOINT: CRIAR VOTO DO ALUNO (informa nome)
# =========================
@vote_router.post(
    "/student",
    response_model=VoteResponseSchema,
    responses={400: {"model": ErrorResponseSchema}, 422: {"model": ErrorResponseSchema}},
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("10/minute")
async def create_student_vote(
    request: Request,
    payload: Annotated[StudentVoteRequestSchema, Depends()],
):
    use_case = _get_register_use_case(request)

    try:
        mapped_score = VOTE_MAPPING[payload.score]

        input_dto = RegisterVoteInputDTO(score=mapped_score, student_name=payload.student_name)
        result = use_case.execute(input_dto)

        return VoteResponseSchema(
            vote_id=result.vote_id,
            score=result.score,
            created_at=result.created_at,
            message=f"Voto registrado com sucesso (anônimo publicamente).",
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


# =========================
# ENDPOINT: LISTAR VOTOS (SOMENTE PROFESSOR)
# =========================
@vote_router.get(
    "/teacher",
    response_model=TeacherVoteListResponseSchema,
)
@limiter.limit("5/minute")
async def get_votes_for_teacher(request: Request, x_teacher_secret: Optional[str] = Header(None)):
    # Validar segredo simples do professor
    if not x_teacher_secret or x_teacher_secret != settings.teacher_secret:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "UNAUTHORIZED",
                "message": "Credenciais do professor invalidas.",
                "status_code": 401,
            },
        )

    use_case = cast(
        "GetAllVotesForTeacherUseCase",
        request.app.state.get_all_votes_for_teacher_use_case,
    )

    votes = use_case.execute()

    teacher_votes = [
        {
            "vote_id": str(v.vote_id),
            "score": v.score_value,
            "created_at": v.created_at.isoformat(),
            "student_name": getattr(v, "student_name", None),
        }
        for v in votes
    ]

    return TeacherVoteListResponseSchema(votes=teacher_votes, total=len(teacher_votes))


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
