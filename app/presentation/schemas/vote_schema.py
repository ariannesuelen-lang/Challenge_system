# app/presentation/schemas/vote_schema.py
from pydantic import BaseModel, Field, model_validator
from typing import Optional


class VoteRequestSchema(BaseModel):
    """Schema de entrada para registro de voto."""

    score: float = Field(
        ...,
        ge=0.0,
        le=10.0,
        description="Nota de 0 a 10. O minimo aceito para registro e 0.2.",
    )

    @model_validator(mode='after')
    def validate_minimum_score(self) -> 'VoteRequestSchema':
        """Validacao adicional: nota minima para registro e 0.2"""
        from app.config import settings
        if self.score < settings.min_vote_score:
            raise ValueError(
                f"A nota informada ({self.score}) e inferior ao minimo permitido "
                f"({settings.min_vote_score})."
            )
        return self

    class Config:
        json_schema_extra = {
            "example": {"score": 8.5}
        }


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
                "score": 8.5,
                "created_at": "2025-01-01T00:00:00+00:00",
                "message": "Voto registrado com sucesso.",
            }
        }


class VoteStatsResponseSchema(BaseModel):
    """Schema de resposta com estatisticas."""

    total_votes: int
    average_score: float
    min_score: float
    max_score: float


class VoteListResponseSchema(BaseModel):
    """Schema de resposta com lista de votos."""

    votes: list['VoteResponseSchema']
    total: int


class ErrorResponseSchema(BaseModel):
    """Schema de resposta para erros."""

    error: str
    message: str
    status_code: int


# Forca a reconstrucao dos schemas para resolver forward references
VoteListResponseSchema.model_rebuild()