"""Select and generate interview questions dynamically.

Future responsibility:
- Pick next question from plan based on current state
- Generate context-aware follow-up questions from prior answers
- Respect min question count and curriculum day coverage rules
"""


class QuestionEngine:
    """Placeholder for question selection and generation."""

    def select_next_question(self, session_state: object) -> None:
        """Select or generate the next question. Not implemented."""
        raise NotImplementedError("QuestionEngine.select_next_question")
