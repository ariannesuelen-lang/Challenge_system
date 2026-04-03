# app/main.py
from __future__ import annotations

import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.config import settings
from app.infrastructure.repositories.in_memory_vote_repository import (
    InMemoryVoteRepository,
)
from app.domain.services.voting_service import VotingService
from app.application.use_cases.register_vote_use_case import (
    RegisterVoteUseCase,
    GetAllVotesUseCase,
    GetVoteStatisticsUseCase,
)
from app.presentation.routes.vote_router import vote_router
from app.infrastructure.rate_limiter.rate_limit_config import limiter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(settings.app_name)


def create_app() -> FastAPI:
    """
    Composition Root: monta todas as dependencias e injeta na aplicacao.
    Segue Dependency Inversion e Injecao de Dependencia.
    """
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Sistema de Votacao com Clean Architecture",
    )

    # Setup rate limiter
    app.state.limiter = limiter
    app.add_exception_handler(
        RateLimitExceeded, _rate_limit_exceeded_handler
    )

    # Infrastructure
    vote_repository = InMemoryVoteRepository()

    # Domain
    voting_service = VotingService(vote_repository=vote_repository)

    # Application
    register_use_case = RegisterVoteUseCase(voting_service=voting_service)
    list_use_case = GetAllVotesUseCase(voting_service=voting_service)
    stats_use_case = GetVoteStatisticsUseCase(voting_service=voting_service)

    # Inject dependencies into app state
    app.state.register_vote_use_case = register_use_case
    app.state.get_all_votes_use_case = list_use_case
    app.state.get_vote_statistics_use_case = stats_use_case

    # Routes
    app.include_router(vote_router)

    @app.get("/health")
    async def health_check() -> dict:
        return {
            "status": "healthy",
            "service": settings.app_name,
            "version": settings.app_version,
        }

    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        logger.exception("Unhandled exception: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "ERRO_INTERNO",
                "message": "Ocorreu um erro interno no servidor.",
                "status_code": 500,
            },
        )

    logger.info("Application started successfully.")
    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        port=8000,
        reload=settings.debug,
        log_level="info",
    )