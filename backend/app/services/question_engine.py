"""Select and generate interview questions dynamically."""

from typing import Any
from app.models.interview import InterviewQuestionSlot
from app.services.llm_service import get_llm_service


class QuestionEngine:
    """Generates context-aware questions utilizing the LLM service."""

    def __init__(self):
        self.llm = get_llm_service()

    def generate_question(
        self,
        slot: InterviewQuestionSlot,
        candidate_role: str,
        years_experience: int,
        history: list[dict[str, Any]],
        is_followup: bool = False
    ) -> str:
        """Generate a contextual question based on the plan slot."""
        context = {
            "candidate_role": candidate_role,
            "years_experience": years_experience,
            "history": history,
            "objective": slot.objective,
            "expected_evidence": slot.expected_evidence,
            "reason": slot.reason
        }
        
        result = self.llm.generate_question(slot, context, is_followup)
        return result.question_text
