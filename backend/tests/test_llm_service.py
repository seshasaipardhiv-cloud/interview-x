"""Tests for OpenAILLMService."""

from unittest.mock import MagicMock, patch
import pytest

from app.models.feedback import FeedbackReport
from app.models.interview import AnswerAnalysis, InterviewPhase, InterviewQuestionSlot, QuestionType, Difficulty, FollowUpStrategy
from app.services.openai_llm_service import OpenAILLMService
from app.services.llm_service import GeneratedQuestion

@pytest.fixture
def mock_openai_client():
    with patch("app.services.openai_llm_service.OpenAI") as mock_openai:
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        yield mock_client

@pytest.fixture
def openai_service(mock_openai_client):
    return OpenAILLMService(api_key="test-key", model="gpt-4o-mini")

def test_generate_question(openai_service, mock_openai_client):
    mock_parse = MagicMock()
    mock_message = MagicMock()
    mock_message.message.parsed = GeneratedQuestion(question_text="Tell me about testing.")
    mock_parse.choices = [mock_message]
    mock_openai_client.beta.chat.completions.parse.return_value = mock_parse

    slot = InterviewQuestionSlot(
        slot_id="123",
        phase=InterviewPhase.CORE_CONCEPT,
        curriculum_day=1,
        topic="Testing",
        objective="Assess knowledge of pytest",
        question_type=QuestionType.CONCEPTUAL,
        target_difficulty=Difficulty.INTERMEDIATE,
        priority=1.0,
        expected_evidence="Can write a test",
        allows_follow_up=True,
        follow_up_strategy=FollowUpStrategy.CLARIFY
    )

    result = openai_service.generate_question(
        slot=slot, 
        context={
            "candidate_role": "Backend", 
            "years_experience": 2,
            "objective": slot.objective,
            "expected_evidence": slot.expected_evidence,
            "reason": slot.reason,
            "history": []
        }, 
        is_followup=False
    )

    assert result.question_text == "Tell me about testing."
    mock_openai_client.beta.chat.completions.parse.assert_called_once()
    kwargs = mock_openai_client.beta.chat.completions.parse.call_args.kwargs
    assert kwargs["response_format"] == GeneratedQuestion
    assert "pytest" in kwargs["messages"][0]["content"]

def test_analyze_answer(openai_service, mock_openai_client):
    mock_parse = MagicMock()
    mock_message = MagicMock()
    mock_message.message.parsed = AnswerAnalysis(
        conceptual_correctness=0.8,
        completeness=0.8,
        technical_depth=0.7,
        reasoning_quality=0.8,
        practical_understanding=0.9,
        confidence=0.8,
        detected_strengths=["Good"],
        detected_gaps=[],
        misconceptions=[],
        missing_concepts=[],
        evidence_level=0.8,
        recommended_action="STRONG"
    )
    mock_parse.choices = [mock_message]
    mock_openai_client.beta.chat.completions.parse.return_value = mock_parse

    result = openai_service.analyze_answer(
        question="What is pytest?", 
        answer="A testing framework.", 
        objective="Assess testing knowledge."
    )

    assert result.recommended_action == "STRONG"
    mock_openai_client.beta.chat.completions.parse.assert_called_once()
    kwargs = mock_openai_client.beta.chat.completions.parse.call_args.kwargs
    assert kwargs["response_format"] == AnswerAnalysis
    assert "pytest" in kwargs["messages"][0]["content"]

def test_generate_feedback(openai_service, mock_openai_client):
    mock_parse = MagicMock()
    mock_message = MagicMock()
    mock_message.message.parsed = FeedbackReport(
        summary="Great job",
        strengths=["Testing"],
        gaps=["Docker"],
        next_steps=["Learn Docker"]
    )
    mock_parse.choices = [mock_message]
    mock_openai_client.beta.chat.completions.parse.return_value = mock_parse

    history = [{"role": "candidate", "content": "Hello"}]
    
    result = openai_service.generate_feedback(history=history, intelligence=None)

    assert result.summary == "Great job"
    mock_openai_client.beta.chat.completions.parse.assert_called_once()
    kwargs = mock_openai_client.beta.chat.completions.parse.call_args.kwargs
    assert kwargs["response_format"] == FeedbackReport
    assert "Hello" in kwargs["messages"][0]["content"]
