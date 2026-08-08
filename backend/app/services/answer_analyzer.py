"""Analyze candidate answers for understanding and signals."""

from app.models.interview import AnswerAnalysis
from app.services.llm_service import get_llm_service


class AnswerAnalyzer:
    """Evaluates candidate answers via LLM."""

    def __init__(self):
        self.llm = get_llm_service()

    def analyze(self, question: str, answer: str, objective: str) -> AnswerAnalysis:
        """Analyze a candidate answer against the objective."""
        return self.llm.analyze_answer(question, answer, objective)
