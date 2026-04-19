# app/presentation/schemas/vote_schema.py

from pydantic import BaseModel, Field
from typing import Optional, Dict
from enum import Enum


# =========================
# ENUM
# =========================
class VoteOption(str, Enum):
    BOM = "BOM"
    REGULAR = "REGULAR"
    RUIM = "RUIM"


# =========================
# REQUEST
# =========================
class VoteRequestSchema(BaseModel):
    """Schema de entrada para registro de voto."""

    score: VoteOption = Field(
        ...,
        description="Escolha entre: BOM, REGULAR ou RUIM.",
    )

    class Config:
        json_schema_extra = {
            "example": {"score": "BOM"}
        }


# =========================
# RESPONSE
# =========================
class VoteResponseSchema(BaseModel):
    """Schema de resposta com dados do voto registrado."""

    vote_id: str
    score: float
    created_at: str
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "vote_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                "score": 10.0,
                "created_at": "2025-01-01T00:00:00+00:00",
                "message": "Voto 'BOM' registrado com sucesso.",
            }
        }


# =========================
# STATS (EVOLUÍDO E COMPATÍVEL)
# =========================
class VoteStatsResponseSchema(BaseModel):
    """Schema de resposta com estatisticas completas."""

    # CAMPOS ORIGINAIS (mantidos)
    total_votes: int
    average_score: float
    min_score: float
    max_score: float

    # NOVOS CAMPOS (integração)
    count: Optional[Dict[str, int]] = None
    percentage: Optional[Dict[str, float]] = None
    category_average: Optional[Dict[str, float]] = None
    difference: Optional[Dict[str, Dict[str, float]]] = None


# =========================
# LIST
# =========================
class VoteListResponseSchema(BaseModel):
    """Schema de resposta com lista de votos."""

    votes: list['VoteResponseSchema']
    total: int


# =========================
# ERROR
# =========================
class ErrorResponseSchema(BaseModel):
    """Schema de resposta para erros."""

    error: str
    message: str
    status_code: int


# Resolve forward refs
VoteListResponseSchema.model_rebuild()
