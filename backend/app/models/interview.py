"""Interview request/response, session, and plan models."""

from enum import Enum
from typing import Any
from pydantic import BaseModel, Field

from app.models.candidate import CandidateRecord
from app.models.feedback import FeedbackReport


class InterviewSessionStatus(str, Enum):
    """High-level interview lifecycle state."""

    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class InterviewPhase(str, Enum):
    """Phases of an adaptive interview progression."""

    BASELINE = "baseline"
    CORE_CONCEPT = "core_concept"
    APPLICATION = "application"
    DEEP_PROBE = "deep_probe"
    CROSS_TOPIC = "cross_topic"
    PRODUCTION_SCENARIO = "production_scenario"
    WEAK_AREA = "weak_area"
    FINAL_SYNTHESIS = "final_synthesis"


class QuestionType(str, Enum):
    CONCEPTUAL = "conceptual"
    EXPLANATION = "explanation"
    APPLICATION = "application"
    TRADEOFF = "tradeoff"
    DEBUGGING = "debugging"
    ARCHITECTURE = "architecture"
    PRODUCTION_INCIDENT = "production_incident"
    COUNTERFACTUAL = "counterfactual"
    DEEP_PROBE = "deep_probe"
    CROSS_TOPIC = "cross_topic"


class Difficulty(str, Enum):
    FOUNDATIONAL = "foundational"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    PRODUCTION = "production"


class FollowUpStrategy(str, Enum):
    CLARIFY = "clarify"
    DEPTH = "depth"
    TRADEOFF = "tradeoff"
    FAILURE_MODE = "failure_mode"
    COUNTERFACTUAL = "counterfactual"
    EVIDENCE_CHALLENGE = "evidence_challenge"


class InterviewQuestionSlot(BaseModel):
    """A planned but un-generated interview question slot."""

    slot_id: str
    phase: InterviewPhase
    curriculum_day: int | None
    secondary_curriculum_day: int | None = None
    topic: str
    secondary_topic: str | None = None
    objective: str
    question_type: QuestionType
    target_difficulty: Difficulty
    priority: float
    reason: dict[str, Any] = Field(default_factory=dict)
    expected_evidence: str
    allows_follow_up: bool
    follow_up_strategy: FollowUpStrategy


class CoverageRequirement(BaseModel):
    """Constraints that a valid interview plan must meet."""

    minimum_questions: int = 8
    minimum_curriculum_days: int = 4


class InterviewPlanSummary(BaseModel):
    candidate_id: str
    total_questions: int
    curriculum_days_covered: list[int]
    topics_covered: list[str]
    high_uncertainty_topics_targeted: list[str]
    phases: list[str]
    difficulty_distribution: dict[str, int]
    question_type_distribution: dict[str, int]


class InterviewPlan(BaseModel):
    """The complete deterministic plan compiled for a candidate."""

    candidate_id: str
    slots: list[InterviewQuestionSlot]
    summary: InterviewPlanSummary


class AnswerAnalysis(BaseModel):
    """Structured analysis of a candidate's answer."""
    conceptual_correctness: float
    completeness: float
    technical_depth: float
    reasoning_quality: float
    practical_understanding: float
    confidence: float
    detected_strengths: list[str]
    detected_gaps: list[str]
    misconceptions: list[str]
    missing_concepts: list[str]
    evidence_level: float
    recommended_action: str


class InterviewRequest(BaseModel):
    """POST /api/interview request body."""
    session_id: str = Field(alias="sessionId")
    candidate: CandidateRecord | None = None
    message: str | None = None


class InterviewResponse(BaseModel):
    """POST /api/interview response body."""
    reply: str
    done: bool = False
    feedback: FeedbackReport | None = None
    question_count: int = 0
    curriculum_days_covered: list[int] = Field(default_factory=list)
    current_phase: str = ""
    is_adapting: bool = False
