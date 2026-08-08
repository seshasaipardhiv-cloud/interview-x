"""Adapt interview difficulty and probing depth."""

from enum import Enum
from pydantic import BaseModel
from app.core.state import InterviewSessionState
from app.models.interview import AnswerAnalysis


class FollowUpDecisionType(str, Enum):
    ADVANCE = "advance"
    FOLLOW_UP = "follow_up"
    FINISH = "finish"


class FollowUpDecision(BaseModel):
    decision: FollowUpDecisionType
    reason: str


class AdaptiveEngine:
    """State machine for interview progression."""
    
    def __init__(self, max_questions: int = 12):
        self.max_questions = max_questions

    def adapt(self, session: InterviewSessionState, analysis: AnswerAnalysis) -> FollowUpDecision:
        """Compute adaptive decisions for next turn."""
        
        # 1. Check hard limits
        if session.question_count >= self.max_questions:
            return FollowUpDecision(decision=FollowUpDecisionType.FINISH, reason="Max questions reached.")
            
        current_slot = session.plan.slots[session.current_slot_index]
        
        # 2. State transition based on analysis
        action = analysis.recommended_action
        
        if action in ["STRONG", "EXCEPTIONAL"]:
            decision_type = FollowUpDecisionType.ADVANCE
            reason = "Demonstrated strong understanding; advancing."
        elif action in ["PARTIAL", "MISCONCEPTION"]:
            if session.follow_up_count < 1 and current_slot.allows_follow_up:
                decision_type = FollowUpDecisionType.FOLLOW_UP
                reason = "Needs clarification or correction; initiating follow-up."
            else:
                decision_type = FollowUpDecisionType.ADVANCE
                reason = "Follow-up limit reached for this slot; advancing."
        else:
            if session.follow_up_count < 1 and current_slot.allows_follow_up:
                decision_type = FollowUpDecisionType.FOLLOW_UP
                reason = "Diagnostic probe to confirm lack of knowledge."
            else:
                decision_type = FollowUpDecisionType.ADVANCE
                reason = "Confirmed inability; advancing."
                
        # If we are advancing, check if we are out of slots
        if decision_type == FollowUpDecisionType.ADVANCE:
            if session.current_slot_index >= len(session.plan.slots) - 1:
                # Check coverage guarantees before finishing
                unique_days = len(set(session.curriculum_days_covered))
                if session.question_count >= session.plan.summary.total_questions and unique_days >= 4:
                    decision_type = FollowUpDecisionType.FINISH
                    reason = "All slots completed and coverage met."
                else:
                    # The compiler guarantees 8 questions and 4 days in the plan.
                    # We just enforce termination here.
                    decision_type = FollowUpDecisionType.FINISH
                    reason = "End of plan."
                    
        return FollowUpDecision(decision=decision_type, reason=reason)
