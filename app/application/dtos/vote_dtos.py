# app/application/dtos/vote_dtos.py
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class RegisterVoteInputDTO:
    score: float
    student_name: Optional[str] = None


@dataclass
class VoteOutputDTO:
    vote_id: str
    score: float
    created_at: str


@dataclass
class VoteWithStudentOutputDTO:
    vote_id: str
    score: float
    created_at: str
    student_name: Optional[str]


@dataclass
class VoteStatisticsOutputDTO:
    total_votes: int
    average_score: float
    min_score: float
    max_score: float


@dataclass
class VoteListOutputDTO:
    votes: List[VoteOutputDTO]
    total: int