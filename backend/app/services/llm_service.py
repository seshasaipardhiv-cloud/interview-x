"""LLM integration layer for question generation, analysis, and feedback."""

import os
from typing import Any, Protocol

from pydantic import BaseModel
from app.models.feedback import FeedbackReport
from app.models.interview import AnswerAnalysis, InterviewQuestionSlot


class GeneratedQuestion(BaseModel):
    """Structured question output from LLM."""
    question_text: str


class LLMProvider(Protocol):
    """Protocol for LLM interactions."""
    
    def generate_question(self, slot: InterviewQuestionSlot, context: dict[str, Any], is_followup: bool = False) -> GeneratedQuestion:
        ...
        
    def analyze_answer(self, question: str, answer: str, objective: str) -> AnswerAnalysis:
        ...
        
    def generate_feedback(self, history: list[dict[str, Any]], intelligence: Any) -> FeedbackReport:
        ...


class MockLLMService:
    """Deterministic mock provider for tests and local dev."""
    
    def __init__(self):
        self._turn_counter = 0

    def generate_question(self, slot: InterviewQuestionSlot, context: dict[str, Any], is_followup: bool = False) -> GeneratedQuestion:
        if is_followup:
            return GeneratedQuestion(question_text=f"[FOLLOW-UP] Can you elaborate on your approach to {slot.topic}?")
        return GeneratedQuestion(question_text=f"[QUESTION] How would you handle {slot.topic}?")

    def analyze_answer(self, question: str, answer: str, objective: str) -> AnswerAnalysis:
        self._turn_counter += 1
        
        # Cycle through deterministic responses
        mod = self._turn_counter % 3
        
        if mod == 1:
            return AnswerAnalysis(
                conceptual_correctness=0.9, completeness=0.9, technical_depth=0.8,
                reasoning_quality=0.9, practical_understanding=0.9, confidence=0.9,
                detected_strengths=["Clear articulation"], detected_gaps=[],
                misconceptions=[], missing_concepts=[], evidence_level=0.9,
                recommended_action="STRONG"
            )
        elif mod == 2:
            return AnswerAnalysis(
                conceptual_correctness=0.6, completeness=0.5, technical_depth=0.5,
                reasoning_quality=0.6, practical_understanding=0.5, confidence=0.6,
                detected_strengths=["Basic idea"], detected_gaps=["Missing edge cases"],
                misconceptions=[], missing_concepts=["Error handling"], evidence_level=0.5,
                recommended_action="PARTIAL"
            )
        else:
            return AnswerAnalysis(
                conceptual_correctness=0.2, completeness=0.2, technical_depth=0.1,
                reasoning_quality=0.2, practical_understanding=0.1, confidence=0.3,
                detected_strengths=[], detected_gaps=["Fundamental misunderstanding"],
                misconceptions=["Confused X with Y"], missing_concepts=["Core mechanism"], evidence_level=0.1,
                recommended_action="MISCONCEPTION"
            )

    def generate_feedback(self, history: list[dict[str, Any]], intelligence: Any) -> FeedbackReport:
        return FeedbackReport(
            summary="Candidate showed strong understanding in early topics but struggled with advanced synthesis.",
            strengths=["Clear articulation of core concepts"],
            gaps=["Missing production edge case knowledge"],
            next_steps=["Review deployment strategies"]
        )


def get_llm_service() -> LLMProvider:
    """Factory to get the configured LLM provider."""
    # For hackathon/tests we return the Mock provider
    return MockLLMService()
