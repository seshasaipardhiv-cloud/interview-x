"""Candidate intelligence and topic evidence models."""

from enum import Enum

from pydantic import BaseModel, Field

from app.models.candidate import CandidateSignals


class MissionStatus(str, Enum):
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"


class TopicEvidence(BaseModel):
    day: int
    topic: str
    status: MissionStatus
    attempts: int | None = None
    first_try: bool = False
    evidence_strength: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Deterministic learning-history evidence strength (not mastery proof)",
    )
    uncertainty: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Higher values indicate greater interview uncertainty",
    )
    interview_priority: float = Field(
        default=0.0,
        description="Rank score for interview investigation (higher = probe sooner)",
    )
    priority_factors: dict[str, float] = Field(
        default_factory=dict,
        description="Explainability breakdown of priority score components",
    )


class CandidateIntelligence(BaseModel):
    candidate_id: str
    name: str
    job_role: str
    years_experience: int
    education: str
    cohort_status: str
    completed_topics: list[int] = Field(default_factory=list)
    failed_topics: list[int] = Field(default_factory=list)
    skipped_topics: list[int] = Field(default_factory=list)
    attempt_counts: dict[int, int] = Field(default_factory=dict)
    first_try_signals: list[int] = Field(default_factory=list)
    completion_signals: dict[str, int | float] = Field(default_factory=dict)
    topic_evidence: list[TopicEvidence] = Field(default_factory=list)
    aggregate_signals: CandidateSignals


class InterviewPriorityTopic(BaseModel):
    day: int
    topic: str
    status: MissionStatus
    interview_priority: float
    evidence_strength: float
    uncertainty: float
    priority_factors: dict[str, float] = Field(default_factory=dict)
    rationale: list[str] = Field(default_factory=list)
