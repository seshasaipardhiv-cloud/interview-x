"""Compile personalized interview plans from candidate context.

Responsibilities:
- Determine interview structure based on candidate intelligence
- Select topics ensuring curriculum coverage and diversity
- Generate a validated, deterministic InterviewPlan
"""

import uuid
from typing import Any

from app.models.curriculum import CurriculumDay
from app.models.intelligence import CandidateIntelligence, InterviewPriorityTopic
from app.models.interview import (
    CoverageRequirement,
    Difficulty,
    FollowUpStrategy,
    InterviewPhase,
    InterviewPlan,
    InterviewPlanSummary,
    InterviewQuestionSlot,
    QuestionType,
)
from app.services.candidate_intelligence import build_candidate_intelligence, rank_interview_priorities
from app.services.curriculum_service import CurriculumService, get_curriculum_service


class InterviewCompilerError(Exception):
    """Raised when plan compilation fails validation and cannot be repaired."""


class InterviewCompiler:
    """Deterministic engine to generate InterviewPlans."""

    def __init__(self, curriculum_service: CurriculumService | None = None) -> None:
        self.curriculum_service = curriculum_service or get_curriculum_service()
        self.requirements = CoverageRequirement()

    def _determine_base_difficulty(self, years_experience: int) -> Difficulty:
        if years_experience >= 8:
            return Difficulty.PRODUCTION
        if years_experience >= 4:
            return Difficulty.ADVANCED
        if years_experience >= 2:
            return Difficulty.INTERMEDIATE
        return Difficulty.FOUNDATIONAL

    def _adjust_difficulty_for_topic(self, base: Difficulty, topic: InterviewPriorityTopic) -> Difficulty:
        """Slightly adjust difficulty based on uncertainty, but do not drop too low."""
        levels = [Difficulty.FOUNDATIONAL, Difficulty.INTERMEDIATE, Difficulty.ADVANCED, Difficulty.PRODUCTION]
        base_idx = levels.index(base)
        
        # High uncertainty does not necessarily mean easy, but maybe one level down to probe foundational gaps.
        if topic.uncertainty > 0.8 and base_idx > 0:
            return levels[base_idx - 1]
        
        # Extremely strong evidence? Maybe push up one level if not at max
        if topic.evidence_strength > 0.9 and base_idx < len(levels) - 1:
            return levels[base_idx + 1]
            
        return base

    def _create_slot(
        self,
        phase: InterviewPhase,
        topic: InterviewPriorityTopic,
        question_type: QuestionType,
        target_difficulty: Difficulty,
        reason: dict[str, Any],
        expected_evidence: str,
        follow_up_strategy: FollowUpStrategy,
        allows_follow_up: bool = True,
        secondary_curriculum_day: int | None = None,
        secondary_topic: str | None = None,
        objective_override: str | None = None
    ) -> InterviewQuestionSlot:
        return InterviewQuestionSlot(
            slot_id=str(uuid.uuid4()),
            phase=phase,
            curriculum_day=topic.day,
            secondary_curriculum_day=secondary_curriculum_day,
            topic=topic.topic,
            secondary_topic=secondary_topic,
            objective=objective_override or f"Assess {topic.topic}",
            question_type=question_type,
            target_difficulty=target_difficulty,
            priority=topic.interview_priority,
            reason=reason,
            expected_evidence=expected_evidence,
            allows_follow_up=allows_follow_up,
            follow_up_strategy=follow_up_strategy
        )

    def _find_cross_topic(self, priorities: list[InterviewPriorityTopic]) -> tuple[InterviewPriorityTopic | None, CurriculumDay | None]:
        """Find a high priority topic that has related days in the curriculum."""
        for p in priorities:
            related = self.curriculum_service.get_related_days(p.day)
            if related:
                return p, related[0]
        return None, None

    def _build_initial_slots(self, intelligence: CandidateIntelligence, priorities: list[InterviewPriorityTopic]) -> list[InterviewQuestionSlot]:
        slots = []
        base_diff = self._determine_base_difficulty(intelligence.years_experience)
        
        # Ensure we don't run out of priorities; fallback to reusing if needed
        pool = priorities.copy()
        def get_topic() -> InterviewPriorityTopic:
            return pool.pop(0) if pool else priorities[0]
            
        def find_weak_area() -> InterviewPriorityTopic:
            weak = sorted(priorities, key=lambda x: -x.uncertainty)
            return weak[0] if weak else get_topic()

        # Slot 1: BASELINE
        t1 = get_topic()
        slots.append(self._create_slot(
            phase=InterviewPhase.BASELINE,
            topic=t1,
            question_type=QuestionType.CONCEPTUAL,
            target_difficulty=self._adjust_difficulty_for_topic(base_diff, t1),
            reason={"primary": "baseline_establishment", "signals": ["top_priority"]},
            expected_evidence="Basic understanding of core concepts",
            follow_up_strategy=FollowUpStrategy.CLARIFY
        ))

        # Slot 2: CORE_CONCEPT
        t2 = get_topic()
        slots.append(self._create_slot(
            phase=InterviewPhase.CORE_CONCEPT,
            topic=t2,
            question_type=QuestionType.EXPLANATION,
            target_difficulty=self._adjust_difficulty_for_topic(base_diff, t2),
            reason={"primary": "core_knowledge", "signals": ["high_priority"]},
            expected_evidence="Clear articulation of the mechanism",
            follow_up_strategy=FollowUpStrategy.DEPTH
        ))

        # Slot 3: APPLICATION
        t3 = get_topic()
        slots.append(self._create_slot(
            phase=InterviewPhase.APPLICATION,
            topic=t3,
            question_type=QuestionType.APPLICATION,
            target_difficulty=self._adjust_difficulty_for_topic(base_diff, t3),
            reason={"primary": "practical_application", "signals": ["high_priority"]},
            expected_evidence="Ability to apply knowledge to a concrete problem",
            follow_up_strategy=FollowUpStrategy.TRADEOFF
        ))

        # Slot 4: DEEP_PROBE
        t4 = get_topic()
        slots.append(self._create_slot(
            phase=InterviewPhase.DEEP_PROBE,
            topic=t4,
            question_type=QuestionType.DEEP_PROBE,
            target_difficulty=self._adjust_difficulty_for_topic(base_diff, t4),
            reason={"primary": "depth_testing", "signals": ["high_priority"]},
            expected_evidence="Understanding of underlying tradeoffs and edge cases",
            follow_up_strategy=FollowUpStrategy.FAILURE_MODE
        ))

        # Slot 5: CROSS_TOPIC
        t5, related_day = self._find_cross_topic(priorities)
        if not t5:
            t5 = get_topic()
            
        if t5 in pool: pool.remove(t5)
        
        sec_day = related_day.day if related_day else None
        sec_topic = related_day.title if related_day else None
        obj = f"Assess synthesis between {t5.topic} and {sec_topic}" if sec_topic else f"Assess {t5.topic}"
        
        slots.append(self._create_slot(
            phase=InterviewPhase.CROSS_TOPIC,
            topic=t5,
            question_type=QuestionType.CROSS_TOPIC,
            target_difficulty=self._adjust_difficulty_for_topic(base_diff, t5),
            reason={"primary": "synthesis", "signals": ["related_curriculum_days"]},
            expected_evidence="Ability to connect multiple concepts together",
            follow_up_strategy=FollowUpStrategy.DEPTH,
            secondary_curriculum_day=sec_day,
            secondary_topic=sec_topic,
            objective_override=obj
        ))

        # Slot 6: PRODUCTION_SCENARIO
        t6 = get_topic()
        levels = [Difficulty.FOUNDATIONAL, Difficulty.INTERMEDIATE, Difficulty.ADVANCED, Difficulty.PRODUCTION]
        base_idx = levels.index(base_diff)
        
        # Controlled stretch: +1 level maximum, but at least intermediate
        prod_idx = min(base_idx + 1, len(levels) - 1)
        prod_diff = levels[prod_idx]
        if prod_diff == Difficulty.FOUNDATIONAL:
            prod_diff = Difficulty.INTERMEDIATE
            
        slots.append(self._create_slot(
            phase=InterviewPhase.PRODUCTION_SCENARIO,
            topic=t6,
            question_type=QuestionType.PRODUCTION_INCIDENT,
            target_difficulty=prod_diff,
            reason={"primary": "production_readiness", "signals": ["role_relevance", "high_priority", "controlled_stretch"]},
            expected_evidence="Architectural and debugging mindset in production",
            follow_up_strategy=FollowUpStrategy.FAILURE_MODE
        ))

        # Slot 7: WEAK_AREA
        t7 = find_weak_area()
        if t7 in pool: pool.remove(t7)
        signals = ["high_uncertainty"]
        if t7.status.value == "skipped":
            signals.append("topic_skipped")
            signals.append("no_learning_history_evidence")
        slots.append(self._create_slot(
            phase=InterviewPhase.WEAK_AREA,
            topic=t7,
            question_type=QuestionType.DEBUGGING,
            target_difficulty=self._adjust_difficulty_for_topic(base_diff, t7),
            reason={"primary": "high_uncertainty", "signals": signals},
            expected_evidence="Diagnostic check on unproven or failed areas",
            follow_up_strategy=FollowUpStrategy.EVIDENCE_CHALLENGE
        ))

        # Slot 8: FINAL_SYNTHESIS
        t8 = get_topic()
        slots.append(self._create_slot(
            phase=InterviewPhase.FINAL_SYNTHESIS,
            topic=t8,
            question_type=QuestionType.ARCHITECTURE,
            target_difficulty=self._adjust_difficulty_for_topic(base_diff, t8),
            reason={"primary": "final_evaluation", "signals": ["high_priority"]},
            expected_evidence="Holistic architectural thinking",
            follow_up_strategy=FollowUpStrategy.COUNTERFACTUAL
        ))
        
        return slots

    def _resolve_redundancy(self, slots: list[InterviewQuestionSlot], priorities: list[InterviewPriorityTopic]) -> list[InterviewQuestionSlot]:
        """Ensure we don't test the exact same thing twice (day + type + objective)."""
        seen = set()
        resolved = []
        for slot in slots:
            sig = (slot.curriculum_day, slot.question_type)
            if sig in seen:
                # Find a replacement topic that we haven't overly tested in this question type
                for p in priorities:
                    if (p.day, slot.question_type) not in seen:
                        slot.curriculum_day = p.day
                        slot.topic = p.topic
                        slot.objective = f"Assess {p.topic}"
                        slot.priority = p.interview_priority
                        break
            seen.add((slot.curriculum_day, slot.question_type))
            resolved.append(slot)
        return resolved

    def _repair_coverage(self, slots: list[InterviewQuestionSlot], priorities: list[InterviewPriorityTopic]) -> list[InterviewQuestionSlot]:
        """Ensure minimum day coverage is met."""
        unique_days = {s.curriculum_day for s in slots if s.curriculum_day is not None}
        if len(unique_days) >= self.requirements.minimum_curriculum_days:
            return slots

        # Greedily swap redundant day slots for unused high priority days
        day_counts = {}
        for s in slots:
            day_counts[s.curriculum_day] = day_counts.get(s.curriculum_day, 0) + 1
        
        unused_topics = [p for p in priorities if p.day not in unique_days]
        
        for slot in reversed(slots):
            if len(unique_days) >= self.requirements.minimum_curriculum_days:
                break
            # If this slot's day appears more than once and it's not our weak area or cross topic
            if day_counts[slot.curriculum_day] > 1 and slot.phase not in (InterviewPhase.WEAK_AREA, InterviewPhase.CROSS_TOPIC):
                if unused_topics:
                    new_topic = unused_topics.pop(0)
                    day_counts[slot.curriculum_day] -= 1
                    slot.curriculum_day = new_topic.day
                    slot.topic = new_topic.topic
                    slot.priority = new_topic.interview_priority
                    slot.objective = f"Assess {new_topic.topic}"
                    unique_days.add(new_topic.day)
                    day_counts[new_topic.day] = 1
        return slots

    def validate_interview_plan(self, slots: list[InterviewQuestionSlot]) -> bool:
        """Validate if the plan meets all deterministic requirements."""
        if len(slots) < self.requirements.minimum_questions:
            return False
            
        unique_days = {s.curriculum_day for s in slots if s.curriculum_day is not None}
        if len(unique_days) < self.requirements.minimum_curriculum_days:
            return False
            
        phases = {s.phase for s in slots}
        if InterviewPhase.WEAK_AREA not in phases:
            return False
        if InterviewPhase.CROSS_TOPIC not in phases:
            return False
        if InterviewPhase.PRODUCTION_SCENARIO not in phases:
            return False
            
        qtypes = {s.question_type for s in slots}
        if QuestionType.APPLICATION not in qtypes and QuestionType.DEEP_PROBE not in qtypes:
            return False

        return True

    def compile_plan(self, candidate_id: str) -> InterviewPlan:
        """Build and validate an interview plan for a candidate."""
        intelligence = build_candidate_intelligence(candidate_id)
        # We fetch top 15 to ensure we have enough topics for 8 slots + replacements
        priorities = rank_interview_priorities(candidate_id, top_n=15)

        slots = self._build_initial_slots(intelligence, priorities)
        slots = self._resolve_redundancy(slots, priorities)
        slots = self._repair_coverage(slots, priorities)

        if not self.validate_interview_plan(slots):
            # In a real system, we might attempt a more aggressive repair or fallback
            raise InterviewCompilerError("Failed to build a valid interview plan")

        # Build summary
        unique_days = list({s.curriculum_day for s in slots if s.curriculum_day is not None})
        topics_covered = list({s.topic for s in slots})
        phases = [s.phase.value for s in slots]
        
        diff_dist = {}
        type_dist = {}
        for s in slots:
            diff_dist[s.target_difficulty.value] = diff_dist.get(s.target_difficulty.value, 0) + 1
            type_dist[s.question_type.value] = type_dist.get(s.question_type.value, 0) + 1

        weak_area_slots = [s for s in slots if s.phase == InterviewPhase.WEAK_AREA]
        
        summary = InterviewPlanSummary(
            candidate_id=candidate_id,
            total_questions=len(slots),
            curriculum_days_covered=sorted(unique_days),
            topics_covered=topics_covered,
            high_uncertainty_topics_targeted=[s.topic for s in weak_area_slots],
            phases=phases,
            difficulty_distribution=diff_dist,
            question_type_distribution=type_dist
        )

        return InterviewPlan(
            candidate_id=candidate_id,
            slots=slots,
            summary=summary
        )


def compile_interview_plan(candidate_id: str) -> InterviewPlan:
    """Convenience wrapper for InterviewCompiler."""
    return InterviewCompiler().compile_plan(candidate_id)
