"""Tests for candidate intelligence and topic priority."""

from app.models.intelligence import MissionStatus
from app.services.candidate_intelligence import (
    CandidateIntelligenceBuilder,
    build_candidate_intelligence,
    rank_interview_priorities,
)
from app.services.topic_evidence import compute_evidence_strength, compute_uncertainty


def test_build_candidate_intelligence_structure() -> None:
    intelligence = build_candidate_intelligence("CAND-001")
    assert intelligence.candidate_id == "CAND-001"
    assert intelligence.job_role == "Senior Data Engineer"
    assert 29 in intelligence.skipped_topics
    assert len(intelligence.topic_evidence) == 10


def test_first_try_and_attempt_evidence() -> None:
    strength_first_try = compute_evidence_strength(MissionStatus.PASSED, 1)
    strength_many_attempts = compute_evidence_strength(MissionStatus.PASSED, 4)
    assert strength_first_try > strength_many_attempts

    skipped_uncertainty = compute_uncertainty(MissionStatus.SKIPPED, None)
    first_try_uncertainty = compute_uncertainty(MissionStatus.PASSED, 1)
    assert skipped_uncertainty > first_try_uncertainty


def test_skipped_topic_has_low_evidence_high_priority() -> None:
    intelligence = build_candidate_intelligence("CAND-001")
    skipped = next(item for item in intelligence.topic_evidence if item.day == 29)
    assert skipped.status == MissionStatus.SKIPPED
    assert skipped.evidence_strength == 0.0
    assert skipped.uncertainty >= 0.9
    assert skipped.interview_priority > 50


def test_failed_topics_rank_above_easy_passes() -> None:
    priorities = rank_interview_priorities("CAND-010", top_n=10)
    top_days = [item.day for item in priorities[:3]]
    assert 8 in top_days or 10 in top_days or 22 in top_days


def test_topic_priority_calculation_is_deterministic() -> None:
    builder = CandidateIntelligenceBuilder()
    first = builder.rank_topic_priorities("CAND-004", top_n=5)
    second = builder.rank_topic_priorities("CAND-004", top_n=5)
    assert [item.model_dump() for item in first] == [item.model_dump() for item in second]


def test_priority_factors_present() -> None:
    priorities = rank_interview_priorities("CAND-006", top_n=3)
    for topic in priorities:
        assert topic.interview_priority > 0
        assert topic.priority_factors
        assert topic.rationale
