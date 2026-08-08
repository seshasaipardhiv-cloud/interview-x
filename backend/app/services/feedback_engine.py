"""Generate evidence-backed final interview feedback."""

from typing import Any
from app.models.feedback import FeedbackReport
from app.services.llm_service import get_llm_service


class FeedbackEngine:
    """Generates final feedback report."""

    def __init__(self):
        self.llm = get_llm_service()

    def generate(self, history: list[dict[str, Any]], intelligence: Any) -> FeedbackReport:
        """Generate final feedback report from history and intelligence."""
        return self.llm.generate_feedback(history, intelligence)
