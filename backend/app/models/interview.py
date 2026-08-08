"""Interview request/response and session models (placeholder — future implementation)."""

from enum import Enum

from pydantic import BaseModel, Field


class InterviewPhase(str, Enum):
    """High-level interview lifecycle phase."""

    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class InterviewRequest(BaseModel):
    """Stub for POST /api/interview request body."""

    session_id: str | None = Field(
        default=None,
        description="Existing session; omit to start a new interview",
    )
    candidate_id: str | None = Field(
        default=None,
        description="Required when starting a new session",
    )
    answer: str | None = Field(
        default=None,
        description="Candidate answer for the current question",
    )
    # TODO: full contract (actions, metadata)


class InterviewQuestion(BaseModel):
    """Stub for a single interview question."""

    question_id: str
    text: str
    curriculum_day: int | None = None
    # TODO: difficulty, follow-up context, evidence tags


class InterviewResponse(BaseModel):
    """Stub for POST /api/interview response body."""

    session_id: str
    phase: InterviewPhase = InterviewPhase.IN_PROGRESS
    question: InterviewQuestion | None = None
    message: str | None = None
    # TODO: progress, evidence snapshot, feedback when complete


class InterviewSessionState(BaseModel):
    """Placeholder for persisted session state shape."""

    session_id: str
    candidate_id: str
    phase: InterviewPhase = InterviewPhase.NOT_STARTED
    question_count: int = 0
    curriculum_days_covered: list[int] = Field(default_factory=list)
    # TODO: conversation history, evidence timeline, adaptive state
