"""Deterministic topic evidence scoring from learning-history signals.

These scores reflect mission outcomes only — they are NOT proof of mastery.
Formulas are intentionally simple and modular for later refinement.
"""

from app.models.candidate import Mission
from app.models.intelligence import MissionStatus
from app.services.candidate_service import CandidateService

# Passed mission evidence: strength decays as attempts increase.
PASSED_BASE_STRENGTH = 1.0
PASSED_ATTEMPT_DECAY = 0.22
PASSED_MIN_STRENGTH = 0.25

# Status baselines
FAILED_EVIDENCE_STRENGTH = 0.15
SKIPPED_EVIDENCE_STRENGTH = 0.0

# Uncertainty baselines
SKIPPED_UNCERTAINTY = 0.95
FAILED_UNCERTAINTY = 0.85
PASSED_BASE_UNCERTAINTY = 0.15
PASSED_ATTEMPT_UNCERTAINTY_STEP = 0.14
PASSED_MAX_UNCERTAINTY = 0.72


def compute_evidence_strength(status: MissionStatus, attempts: int | None) -> float:
    """Return evidence strength in [0, 1] from mission status and attempts."""
    if status == MissionStatus.SKIPPED:
        return SKIPPED_EVIDENCE_STRENGTH
    if status == MissionStatus.FAILED:
        return FAILED_EVIDENCE_STRENGTH

    attempt_count = attempts or 1
    strength = PASSED_BASE_STRENGTH - (attempt_count - 1) * PASSED_ATTEMPT_DECAY
    return round(max(PASSED_MIN_STRENGTH, min(1.0, strength)), 3)


def compute_uncertainty(status: MissionStatus, attempts: int | None) -> float:
    """Return uncertainty in [0, 1]; higher means less confidence in demonstrated knowledge."""
    if status == MissionStatus.SKIPPED:
        return SKIPPED_UNCERTAINTY
    if status == MissionStatus.FAILED:
        return FAILED_UNCERTAINTY

    attempt_count = attempts or 1
    uncertainty = PASSED_BASE_UNCERTAINTY + (attempt_count - 1) * PASSED_ATTEMPT_UNCERTAINTY_STEP
    return round(min(PASSED_MAX_UNCERTAINTY, uncertainty), 3)


def is_first_try_pass(mission: Mission, status: MissionStatus) -> bool:
    return status == MissionStatus.PASSED and mission.attempts == 1


def resolve_topic_title(mission: Mission, curriculum_title: str | None) -> str:
    """Prefer curriculum title when available; fall back to mission title."""
    return curriculum_title or mission.title
