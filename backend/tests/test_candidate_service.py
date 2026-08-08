"""Tests for CandidateService."""

import pytest

from app.services.candidate_service import CandidateNotFoundError, CandidateService


def test_get_all_candidates(candidate_service: CandidateService) -> None:
    candidates = candidate_service.get_all_candidates()
    assert len(candidates) == 20
    assert candidates[0].member.id == "CAND-001"


def test_get_candidate(candidate_service: CandidateService) -> None:
    candidate = candidate_service.get_candidate("CAND-003")
    assert candidate.member.name == "Emily Chen"
    assert candidate.member.jobRole == "AI Engineer"


def test_get_candidate_not_found(candidate_service: CandidateService) -> None:
    with pytest.raises(CandidateNotFoundError):
        candidate_service.get_candidate("CAND-999")


def test_get_completed_missions(candidate_service: CandidateService) -> None:
    completed = candidate_service.get_completed_missions("CAND-001")
    assert all(mission.passed is True for mission in completed)
    assert len(completed) == 9


def test_get_skipped_missions(candidate_service: CandidateService) -> None:
    skipped = candidate_service.get_skipped_missions("CAND-001")
    assert len(skipped) == 1
    assert skipped[0].day == 29
    assert skipped[0].skipped is True


def test_get_failed_missions(candidate_service: CandidateService) -> None:
    failed = candidate_service.get_failed_missions("CAND-010")
    assert len(failed) == 3
    assert all(mission.passed is False for mission in failed)
    failed_days = {mission.day for mission in failed}
    assert failed_days == {8, 10, 22}


def test_get_attempt_statistics(candidate_service: CandidateService) -> None:
    stats = candidate_service.get_attempt_statistics("CAND-002")
    assert stats["passed_count"] == 10
    assert stats["failed_count"] == 0
    assert stats["skipped_count"] == 0
    assert stats["total_attempts"] > 0
    assert stats["by_day"][12]["attempts"] == 5


def test_get_learning_signals(candidate_service: CandidateService) -> None:
    signals = candidate_service.get_learning_signals("CAND-006")
    assert signals["organizer_signals"]["missionsFirstTry"] == 2
    assert signals["derived"]["skipped_count"] == 2
    skipped_missions = [
        mission for mission in signals["missions"] if mission["status"] == "skipped"
    ]
    assert len(skipped_missions) == 2
