"""Interview API routes."""

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
import logging

from app.models.interview import InterviewRequest, InterviewResponse, InterviewSessionStatus
from app.core.state import session_store, InterviewSessionState, ConversationTurn
from app.services.interview_compiler import compile_interview_plan
from app.services.candidate_intelligence import build_candidate_intelligence
from app.services.candidate_service import get_candidate_service
from app.services.question_engine import QuestionEngine
from app.services.answer_analyzer import AnswerAnalyzer
from app.services.adaptive_engine import AdaptiveEngine, FollowUpDecisionType
from app.services.feedback_engine import FeedbackEngine

router = APIRouter()
logger = logging.getLogger("interview")

question_engine = QuestionEngine()
answer_analyzer = AnswerAnalyzer()
adaptive_engine = AdaptiveEngine()
feedback_engine = FeedbackEngine()


@router.post("/interview", response_model=InterviewResponse)
async def conduct_interview(request: InterviewRequest) -> InterviewResponse:
    """Handle multi-turn adaptive interview."""
    session_id = request.session_id
    session = session_store.get(session_id)

    # 1. New Session Initialization
    if request.candidate is not None:
        if session is not None:
            logger.warning(f"Session already exists: {session_id}")
            raise HTTPException(status_code=400, detail="Session already exists.")
            
        candidate_id = request.candidate.member.id
        
        # Verify candidate exists in our data
        candidate_service = get_candidate_service()
        candidate = candidate_service.get_candidate(candidate_id)
        if not candidate:
            # Fallback to the provided candidate if not in DB (for tests)
            candidate = request.candidate
            
        # We need candidate intelligence
        intelligence = build_candidate_intelligence(candidate_id)
            
        try:
            plan = compile_interview_plan(candidate_id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to compile plan: {str(e)}")
            
        session = InterviewSessionState(
            session_id=session_id,
            candidate_id=candidate_id,
            candidate=candidate,
            intelligence=intelligence,
            plan=plan,
            status=InterviewSessionStatus.IN_PROGRESS
        )
        session_store.create_session(session)
        
        # Generate first question
        slot = session.plan.slots[0]
        question_text = question_engine.generate_question(
            slot=slot,
            candidate_role=candidate.member.jobRole,
            years_experience=candidate.member.yearsExperience,
            history=[],
            is_followup=False
        )
        
        session.asked_slots.append(slot)
        session.conversation_history.append(ConversationTurn(role="interviewer", content=question_text))
        
        # We start with 1 question count (the one just generated)
        session.question_count = 1
        
        logger.info(f"Session started | session_id={session_id} candidate_id={candidate_id} first_slot={slot.phase.value}")
        
        return InterviewResponse(
            reply=question_text, 
            done=False,
            question_count=session.question_count,
            curriculum_days_covered=list(set(session.curriculum_days_covered)),
            current_phase=slot.phase.value,
            is_adapting=False
        )

    # 2. Existing Session Continuation
    if session is None:
        logger.warning(f"Session not found: {session_id}")
        raise HTTPException(status_code=404, detail="Session not found.")
        
    if session.status == InterviewSessionStatus.COMPLETED:
        logger.warning(f"Attempt to continue completed session: {session_id}")
        raise HTTPException(status_code=400, detail="Interview already completed.")
        
    if not request.message:
        raise HTTPException(status_code=400, detail="Message is required for continuation.")
        
    logger.info(f"Interview turn | session_id={session_id} phase={session.plan.slots[session.current_slot_index].phase.value}")
        
    session.conversation_history.append(ConversationTurn(role="candidate", content=request.message))
    
    current_slot = session.plan.slots[session.current_slot_index]
    last_question = session.conversation_history[-2].content
    
    # Analyze Answer
    analysis = answer_analyzer.analyze(
        question=last_question,
        answer=request.message,
        objective=current_slot.objective
    )
    session.answer_evaluations.append(analysis)
    
    logger.info(f"Answer analyzed | session_id={session_id} evidence_level={analysis.evidence_level}")
    
    # Adaptive Decision
    decision = adaptive_engine.adapt(session, analysis)
    
    if decision.decision == FollowUpDecisionType.FOLLOW_UP:
        session.follow_up_count += 1
        session.total_follow_ups += 1
        
        followup_text = question_engine.generate_question(
            slot=current_slot,
            candidate_role=session.candidate.member.jobRole,
            years_experience=session.candidate.member.yearsExperience,
            history=[h.model_dump() for h in session.conversation_history],
            is_followup=True
        )
        
        session.conversation_history.append(ConversationTurn(role="interviewer", content=followup_text))
        
        logger.info(f"Decision: FOLLOW_UP | session_id={session_id} total_follow_ups={session.total_follow_ups}")
        
        return InterviewResponse(
            reply=followup_text, 
            done=False,
            question_count=session.question_count,
            curriculum_days_covered=list(set(session.curriculum_days_covered)),
            current_phase=current_slot.phase.value,
            is_adapting=True
        )
        
    elif decision.decision == FollowUpDecisionType.ADVANCE:
        # Finalize slot metrics
        session.answered_slots.append(current_slot)
        if current_slot.curriculum_day not in session.curriculum_days_covered:
            session.curriculum_days_covered.append(current_slot.curriculum_day)
        session.question_count += 1
        session.follow_up_count = 0
        
        # Move to next slot
        session.current_slot_index += 1
        next_slot = session.plan.slots[session.current_slot_index]
        
        next_q_text = question_engine.generate_question(
            slot=next_slot,
            candidate_role=session.candidate.member.jobRole,
            years_experience=session.candidate.member.yearsExperience,
            history=[h.model_dump() for h in session.conversation_history],
            is_followup=False
        )
        
        session.asked_slots.append(next_slot)
        session.conversation_history.append(ConversationTurn(role="interviewer", content=next_q_text))
        
        logger.info(f"Decision: ADVANCE | session_id={session_id} next_phase={next_slot.phase.value}")
        
        return InterviewResponse(
            reply=next_q_text, 
            done=False,
            question_count=session.question_count,
            curriculum_days_covered=list(set(session.curriculum_days_covered)),
            current_phase=next_slot.phase.value,
            is_adapting=False
        )
        
    elif decision.decision == FollowUpDecisionType.FINISH:
        # Finalize slot metrics for the last answer
        session.answered_slots.append(current_slot)
        if current_slot.curriculum_day not in session.curriculum_days_covered:
            session.curriculum_days_covered.append(current_slot.curriculum_day)
        session.question_count += 1
        
        session.status = InterviewSessionStatus.COMPLETED
        
        # Generate feedback
        feedback = feedback_engine.generate(
            history=[h.model_dump() for h in session.conversation_history],
            intelligence=session.intelligence
        )
        feedback.questions_completed = session.question_count
        feedback.curriculum_areas_assessed = len(session.curriculum_days_covered)
        feedback.adaptive_follow_ups = session.total_follow_ups
        session.feedback = feedback
        
        logger.info(f"Decision: FINISH | session_id={session_id} questions_completed={session.question_count}")
        
        return InterviewResponse(
            reply="Interview completed.", 
            done=True, 
            feedback=feedback,
            question_count=session.question_count,
            curriculum_days_covered=list(set(session.curriculum_days_covered)),
            current_phase=current_slot.phase.value,
            is_adapting=False
        )
