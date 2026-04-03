# tests/__init__.py
# Tests package

# tests/test_vote_endpoint.py
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)


class TestVoteEndpoint:
    """
    Testes de integracao para o endpoint de votacao.
    Cobre os fluxos principais e casos de erro.
    """

    def test_create_vote_valid_score(self, client: TestClient) -> None:
        response = client.post(
            "/api/v1/votes/", json={"score": 7.5}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["score"] == 7.5
        assert data["message"] == "Voto registrado com sucesso."
        assert "vote_id" in data
        assert "created_at" in data

    def test_create_vote_minimum_allowed(self, client: TestClient) -> None:
        response = client.post(
            "/api/v1/votes/", json={"score": 0.2}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["score"] == 0.2

    def test_create_vote_maximum_allowed(self, client: TestClient) -> None:
        response = client.post(
            "/api/v1/votes/", json={"score": 10.0}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["score"] == 10.0

    def test_create_vote_below_minimum_returns_400(
        self, client: TestClient
    ) -> None:
        response = client.post(
            "/api/v1/votes/", json={"score": 0.1}
        )
        assert response.status_code == 400
        data = response.json()["detail"]
        assert data["error"] == "NOTA_ABAIXO_DO_MINIMO"
        assert "0.2" in data["message"]

    def test_create_vote_zero_returns_400(self, client: TestClient) -> None:
        response = client.post(
            "/api/v1/votes/", json={"score": 0.0}
        )
        assert response.status_code == 400
        data = response.json()["detail"]
        assert data["error"] == "NOTA_ABAIXO_DO_MINIMO"

    def test_create_vote_negative_returns_400(self, client: TestClient) -> None:
        response = client.post(
            "/api/v1/votes/", json={"score": -1.5}
        )
        assert response.status_code == 400
        data = response.json()["detail"]
        assert data["error"] == "NOTA_ABAIXO_DO_MINIMO"

    def test_create_vote_above_maximum_returns_400(
        self, client: TestClient
    ) -> None:
        response = client.post(
            "/api/v1/votes/", json={"score": 10.1}
        )
        assert response.status_code == 400
        data = response.json()["detail"]
        assert data["error"] == "NOTA_ACIMA_DO_MAXIMO"

    def test_create_vote_above_maximum_high_returns_400(
        self, client: TestClient
    ) -> None:
        response = client.post(
            "/api/v1/votes/", json={"score": 15.0}
        )
        assert response.status_code == 400
        data = response.json()["detail"]
        assert data["error"] == "NOTA_ACIMA_DO_MAXIMO"

    def test_create_vote_invalid_type_returns_422(
        self, client: TestClient
    ) -> None:
        response = client.post(
            "/api/v1/votes/", json={"score": "nota_invalida"}
        )
        assert response.status_code == 422

    def test_create_vote_missing_field_returns_422(
        self, client: TestClient
    ) -> None:
        response = client.post("/api/v1/votes/", json={})
        assert response.status_code == 422

    def test_list_votes_empty(self, client: TestClient) -> None:
        app = create_app()
        fresh_client = TestClient(app)
        response = fresh_client.get("/api/v1/votes/")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["votes"] == []

    def test_list_votes_after_creation(self, client: TestClient) -> None:
        client.post("/api/v1/votes/", json={"score": 5.0})
        client.post("/api/v1/votes/", json={"score": 8.0})

        response = client.get("/api/v1/votes/")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2

    def test_statistics_empty(self, client: TestClient) -> None:
        app = create_app()
        fresh_client = TestClient(app)
        response = fresh_client.get("/api/v1/votes/statistics")
        assert response.status_code == 200
        data = response.json()
        assert data["total_votes"] == 0
        assert data["average_score"] == 0.0

    def test_statistics_after_votes(self, client: TestClient) -> None:
        client.post("/api/v1/votes/", json={"score": 4.0})
        client.post("/api/v1/votes/", json={"score": 6.0})
        client.post("/api/v1/votes/", json={"score": 10.0})

        response = client.get("/api/v1/votes/statistics")
        assert response.status_code == 200
        data = response.json()
        assert data["total_votes"] == 3
        assert data["average_score"] == 6.67
        assert data["min_score"] == 4.0
        assert data["max_score"] == 10.0

    def test_health_check(self, client: TestClient) -> None:
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestVoteDomain:
    """Testes unitarios da camada de dominio."""

    def test_vote_score_accepts_minimum(self) -> None:
        from app.domain.value_objects.vote_score import VoteScore

        score = VoteScore(0.2)
        assert score.value == 0.2

    def test_vote_score_rejects_below_minimum(self) -> None:
        from app.domain.value_objects.vote_score import VoteScore
        from app.domain.exceptions.vote_exceptions import VoteBelowMinimumError

        with pytest.raises(VoteBelowMinimumError):
            VoteScore(0.1)

    def test_vote_score_rejects_zero(self) -> None:
        from app.domain.value_objects.vote_score import VoteScore
        from app.domain.exceptions.vote_exceptions import VoteBelowMinimumError

        with pytest.raises(VoteBelowMinimumError):
            VoteScore(0.0)

    def test_vote_score_rejects_negative(self) -> None:
        from app.domain.value_objects.vote_score import VoteScore
        from app.domain.exceptions.vote_exceptions import VoteBelowMinimumError

        with pytest.raises(VoteBelowMinimumError):
            VoteScore(-5.0)

    def test_vote_score_accepts_maximum(self) -> None:
        from app.domain.value_objects.vote_score import VoteScore

        score = VoteScore(10.0)
        assert score.value == 10.0

    def test_vote_score_rejects_above_maximum(self) -> None:
        from app.domain.value_objects.vote_score import VoteScore
        from app.domain.exceptions.vote_exceptions import VoteAboveMaximumError

        with pytest.raises(VoteAboveMaximumError):
            VoteScore(10.1)

    def test_vote_creation(self) -> None:
        from app.domain.value_objects.vote_score import VoteScore
        from app.domain.entities.vote import Vote

        score = VoteScore(7.5)
        vote = Vote(score=score)
        assert vote.score_value == 7.5
        assert vote.vote_id is not None
        assert vote.created_at is not None

    def test_repository_save_and_find(self) -> None:
        from app.domain.value_objects.vote_score import VoteScore
        from app.domain.entities.vote import Vote
        from app.infrastructure.repositories.in_memory_vote_repository import (
            InMemoryVoteRepository,
        )

        repo = InMemoryVoteRepository()
        score = VoteScore(8.0)
        vote = Vote(score=score)
        saved = repo.save(vote)

        assert saved.vote_id == vote.vote_id
        all_votes = repo.find_all()
        assert len(all_votes) == 1
        assert all_votes[0].score_value == 8.0

    def test_repository_count(self) -> None:
        from app.domain.value_objects.vote_score import VoteScore
        from app.domain.entities.vote import Vote
        from app.infrastructure.repositories.in_memory_vote_repository import (
            InMemoryVoteRepository,
        )

        repo = InMemoryVoteRepository()
        assert repo.count() == 0

        repo.save(Vote(score=VoteScore(5.0)))
        repo.save(Vote(score=VoteScore(7.0)))
        assert repo.count() == 2

    def test_repository_average(self) -> None:
        from app.domain.value_objects.vote_score import VoteScore
        from app.domain.entities.vote import Vote
        from app.infrastructure.repositories.in_memory_vote_repository import (
            InMemoryVoteRepository,
        )

        repo = InMemoryVoteRepository()
        assert repo.average() == 0.0

        repo.save(Vote(score=VoteScore(4.0)))
        repo.save(Vote(score=VoteScore(6.0)))
        assert repo.average() == 5.0