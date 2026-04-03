# app/config.py
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str = "Voting System API"
    app_version: str = "1.0.0"
    min_vote_score: float = 0.2
    max_vote_score: float = 10.0
    rate_limit_default: str = "10/minute"
    debug: bool = False


settings = Settings()