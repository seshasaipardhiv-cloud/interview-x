"""OpenAI implementation of the LLM provider."""

import json
from typing import Any

from openai import OpenAI

from app.models.feedback import FeedbackReport
from app.models.interview import AnswerAnalysis, InterviewQuestionSlot
from app.services.llm_service import GeneratedQuestion, LLMProvider


class OpenAILLMService(LLMProvider):
    """OpenAI-backed LLM provider utilizing Structured Outputs."""

    def __init__(self, api_key: str, model: str = "gpt-4o-mini") -> None:
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate_question(
        self, slot: InterviewQuestionSlot, context: dict[str, Any], is_followup: bool = False
    ) -> GeneratedQuestion:
        prompt = (
            "You are an expert technical interviewer.\n"
            f"Candidate Role: {context.get('candidate_role')}\n"
            f"Years Experience: {context.get('years_experience')}\n"
            f"Objective: {context.get('objective')}\n"
            f"Expected Evidence: {context.get('expected_evidence')}\n"
            f"Reasoning: {json.dumps(context.get('reason', {}))}\n"
            f"Is Follow-up: {is_followup}\n"
            "\nConversation History:\n"
        )
        
        for h in context.get("history", []):
            prompt += f"{h['role']}: {h['content']}\n"
            
        prompt += "\nBased on the history and the objective, generate the exact text of the next question to ask the candidate."
        
        completion = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=[{"role": "system", "content": prompt}],
            response_format=GeneratedQuestion,
        )
        return completion.choices[0].message.parsed

    def analyze_answer(self, question: str, answer: str, objective: str) -> AnswerAnalysis:
        prompt = (
            "You are evaluating a candidate's answer to a technical interview question.\n"
            f"Question: {question}\n"
            f"Answer: {answer}\n"
            f"Objective: {objective}\n\n"
            "Analyze the answer thoroughly.\n"
            "For 'recommended_action', you MUST use one of the following exact string values: "
            "'STRONG', 'EXCEPTIONAL', 'PARTIAL', 'MISCONCEPTION', or 'LACK_OF_KNOWLEDGE'."
        )
        completion = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=[{"role": "system", "content": prompt}],
            response_format=AnswerAnalysis,
        )
        return completion.choices[0].message.parsed

    def generate_feedback(self, history: list[dict[str, Any]], intelligence: Any) -> FeedbackReport:
        prompt = "You are an expert technical interviewer generating a final feedback report.\n\nConversation History:\n"
        for h in history:
            prompt += f"{h['role']}: {h['content']}\n"
            
        prompt += "\nBased on the conversation, provide a detailed summary, key strengths, knowledge gaps, and recommended next steps."
        
        completion = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=[{"role": "system", "content": prompt}],
            response_format=FeedbackReport,
        )
        return completion.choices[0].message.parsed
