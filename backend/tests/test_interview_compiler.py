"""Tests for the InterviewCompiler logic."""

import pytest

from app.models.interview import InterviewPhase, QuestionType
from app.services.interview_compiler import InterviewCompiler, compile_interview_plan


def test_compiler_minimum_requirements():
    """Test that compiler generates at least 8 questions and 4 days."""
    plan = compile_interview_plan("CAND-001")
    
    assert plan.summary.total_questions >= 8
    assert len(plan.summary.curriculum_days_covered) >= 4


def test_weak_area_targeting():
    """Test that a high-uncertainty topic is selected as a WEAK_AREA."""
    plan = compile_interview_plan("CAND-011") # This candidate has multiple skipped
    
    weak_area_slots = [s for s in plan.slots if s.phase == InterviewPhase.WEAK_AREA]
    assert len(weak_area_slots) == 1
    slot = weak_area_slots[0]
    
    assert slot.reason["primary"] == "high_uncertainty"
    assert "high_uncertainty" in slot.reason["signals"]


def test_cross_topic_slot():
    """Test that a cross-topic slot exists."""
    plan = compile_interview_plan("CAND-004")
    
    cross_topic_slots = [s for s in plan.slots if s.phase == InterviewPhase.CROSS_TOPIC]
    assert len(cross_topic_slots) == 1
    assert cross_topic_slots[0].question_type == QuestionType.CROSS_TOPIC


def test_production_scenario():
    """Test that production scenario slot exists for experienced candidate."""
    plan = compile_interview_plan("CAND-015") # 20 years exp
    
    prod_slots = [s for s in plan.slots if s.phase == InterviewPhase.PRODUCTION_SCENARIO]
    assert len(prod_slots) == 1
    assert prod_slots[0].question_type == QuestionType.PRODUCTION_INCIDENT


def test_multiple_question_types():
    """Test that multiple question types are utilized."""
    plan = compile_interview_plan("CAND-005")
    
    assert len(plan.summary.question_type_distribution) > 3


def test_redundancy_prevention():
    """Test that no two slots share the same day and question type."""
    plan = compile_interview_plan("CAND-006")
    
    seen = set()
    for slot in plan.slots:
        sig = (slot.curriculum_day, slot.question_type)
        assert sig not in seen, f"Redundancy found: {sig}"
        seen.add(sig)


def test_personalization():
    """Test that different candidates get different plans."""
    plan_c1 = compile_interview_plan("CAND-001")
    plan_c2 = compile_interview_plan("CAND-011")
    
    assert plan_c1.summary.topics_covered != plan_c2.summary.topics_covered
    assert plan_c1.summary.difficulty_distribution != plan_c2.summary.difficulty_distribution
