"""In-memory session state store."""

from typing import Any
from uuid import uuid4
from pydantic import BaseModel, Field

from app.models.candidate import CandidateRecord
from app.models.intelligence import CandidateIntelligence, TopicEvidence
from app.models.interview import InterviewPlan, InterviewSessionStatus, InterviewQuestionSlot, AnswerAnalysis
from app.models.feedback import FeedbackReport


class ConversationTurn(BaseModel):
    role: str
    content: str


class InterviewSessionState(BaseModel):
    session_id: str
    candidate_id: str
    candidate: CandidateRecord
    intelligence: CandidateIntelligence
    plan: InterviewPlan
    
    current_slot_index: int = 0
    asked_slots: list[InterviewQuestionSlot] = Field(default_factory=list)
    answered_slots: list[InterviewQuestionSlot] = Field(default_factory=list)
    
    conversation_history: list[ConversationTurn] = Field(default_factory=list)
    answer_evaluations: list[AnswerAnalysis] = Field(default_factory=list)
    topic_evidence_updates: list[TopicEvidence] = Field(default_factory=list)
    
    follow_up_count: int = 0
    total_follow_ups: int = 0
    question_count: int = 0
    curriculum_days_covered: list[int] = Field(default_factory=list)
    
    status: InterviewSessionStatus = InterviewSessionStatus.NOT_STARTED
    feedback: FeedbackReport | None = None


class SessionStateStore:
    """In-memory session store."""

    def __init__(self) -> None:
        self._sessions: dict[str, InterviewSessionState] = {}

    def create_session(self, state: InterviewSessionState) -> str:
        """Create a new session and return its sessionId."""
        self._sessions[state.session_id] = state
        return state.session_id

    def get(self, session_id: str) -> InterviewSessionState | None:
        """Retrieve session state by sessionId."""
        return self._sessions.get(session_id)

    def set(self, session_id: str, state: InterviewSessionState) -> None:
        """Replace session state for sessionId."""
        self._sessions[session_id] = state

    def delete(self, session_id: str) -> None:
        """Remove a session."""
        self._sessions.pop(session_id, None)


# Module-level singleton for interview services
session_store = SessionStateStore()
