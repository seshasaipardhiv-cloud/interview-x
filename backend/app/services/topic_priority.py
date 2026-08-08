"""Deterministic interview priority scoring for curriculum topics.

Priority ranks topics that deserve investigation during an interview.
Higher score = probe sooner. Weights are modular and replaceable.
"""

from __future__ import annotations

from app.models.curriculum import CurriculumDay
from app.models.intelligence import MissionStatus, TopicEvidence

# --- Configurable weights (replaceable in later iterations) ---
WEIGHT_SKIPPED = 40.0
WEIGHT_FAILED = 35.0
WEIGHT_ATTEMPT_STRUGGLE = 6.0
WEIGHT_LOW_EVIDENCE = 20.0
WEIGHT_UNCERTAINTY = 15.0
WEIGHT_CURRICULUM_IMPORTANCE = 12.0
WEIGHT_ROLE_RELEVANCE = 10.0
WEIGHT_RECENCY = 5.0

DAY_TYPE_IMPORTANCE = {
    "CAPSTONE": 1.0,
    "SHIP_IT": 0.9,
    "BUILD": 0.75,
    "AI_CORE": 0.8,
    "OPTIMIZE": 0.7,
    "LEARN": 0.6,
    "SETUP": 0.45,
}

ROLE_KEYWORDS: dict[str, tuple[str, ...]] = {
    "devops": ("docker", "kubernetes", "deployment", "monitoring", "observability", "logging"),
    "data": ("pandas", "sql", "sqlite", "embeddings", "vector", "retrieval", "data"),
    "ai": ("langchain", "agent", "mcp", "rag", "embedding", "prompt", "llm", "fine-tuning"),
    "backend": ("fastapi", "api", "backend", "streaming", "integration"),
    "frontend": ("react", "vite", "streamlit", "frontend"),
    "security": ("security", "guardrail", "privacy", "authentication"),
    "architect": ("deployment", "kubernetes", "docker", "orchestration", "capstone"),
}


def curriculum_importance(day: CurriculumDay | None, day_number: int) -> float:
    """Score curriculum importance using day position and day type."""
    type_weight = 0.65
    if day is not None:
        type_weight = DAY_TYPE_IMPORTANCE.get(day.type, 0.65)
    progression = day_number / 31.0
    return round((progression * 0.4 + type_weight * 0.6), 3)


def role_relevance(job_role: str, day: CurriculumDay | None, topic_title: str) -> float:
    """Estimate role relevance via keyword overlap (deterministic)."""
    role_lower = job_role.lower()
    haystack = topic_title.lower()
    if day is not None:
        haystack += " " + " ".join(day.tools).lower()
        haystack += " " + day.title.lower()

    matched_buckets = 0
    matched_keywords = 0
    for bucket, keywords in ROLE_KEYWORDS.items():
        bucket_hit = any(token in role_lower for token in bucket.split("_"))
        if not bucket_hit and bucket not in role_lower:
            # also allow direct keyword presence in role string
            bucket_hit = bucket.replace("_", " ") in role_lower or bucket in role_lower
        if not bucket_hit:
            continue
        hits = sum(1 for keyword in keywords if keyword in haystack)
        if hits:
            matched_buckets += 1
            matched_keywords += hits

    if matched_keywords == 0:
        return 0.2
    score = min(1.0, 0.35 + matched_buckets * 0.15 + matched_keywords * 0.08)
    return round(score, 3)


def recency_factor(day_number: int, max_mission_day: int) -> float:
    """Proxy for 'demonstrated recently' using curriculum day ordering.

    Without timestamps, later mission days in the candidate record are treated
    as more recent exposure within the program sequence.
    """
    if max_mission_day <= 0:
        return 0.0
    return round(day_number / max_mission_day, 3)


def compute_priority_factors(
    evidence: TopicEvidence,
    curriculum_day: CurriculumDay | None,
    job_role: str,
    max_mission_day: int,
) -> dict[str, float]:
    """Compute explainable priority factor components."""
    factors: dict[str, float] = {}

    if evidence.status == MissionStatus.SKIPPED:
        factors["skipped_boost"] = WEIGHT_SKIPPED
    if evidence.status == MissionStatus.FAILED:
        factors["failed_boost"] = WEIGHT_FAILED

    if evidence.attempts and evidence.attempts > 1 and evidence.status == MissionStatus.PASSED:
        factors["attempt_struggle_boost"] = (evidence.attempts - 1) * WEIGHT_ATTEMPT_STRUGGLE

    factors["low_evidence_boost"] = (1.0 - evidence.evidence_strength) * WEIGHT_LOW_EVIDENCE
    factors["uncertainty_boost"] = evidence.uncertainty * WEIGHT_UNCERTAINTY

    importance = curriculum_importance(curriculum_day, evidence.day)
    factors["curriculum_importance_boost"] = importance * WEIGHT_CURRICULUM_IMPORTANCE

    relevance = role_relevance(job_role, curriculum_day, evidence.topic)
    factors["role_relevance_boost"] = relevance * WEIGHT_ROLE_RELEVANCE

    recency = recency_factor(evidence.day, max_mission_day)
    # Skipped/failed topics get recency boost (recent gaps in advanced sections matter)
    if evidence.status in {MissionStatus.SKIPPED, MissionStatus.FAILED}:
        factors["recency_boost"] = recency * WEIGHT_RECENCY
    elif evidence.attempts and evidence.attempts >= 3:
        factors["recency_boost"] = recency * (WEIGHT_RECENCY * 0.6)

    return {key: round(value, 3) for key, value in factors.items()}


def compute_interview_priority(
    evidence: TopicEvidence,
    curriculum_day: CurriculumDay | None,
    job_role: str,
    max_mission_day: int,
) -> tuple[float, dict[str, float]]:
    """Return total priority score and factor breakdown."""
    factors = compute_priority_factors(evidence, curriculum_day, job_role, max_mission_day)
    total = round(sum(factors.values()), 3)
    return total, factors


def build_priority_rationale(
    evidence: TopicEvidence,
    factors: dict[str, float],
) -> list[str]:
    """Human-readable rationale from factor breakdown."""
    rationale: list[str] = []

    if evidence.status == MissionStatus.SKIPPED:
        rationale.append("Mission was skipped — no learning-history evidence recorded.")
    elif evidence.status == MissionStatus.FAILED:
        rationale.append("Mission was failed — increases interview uncertainty.")
    elif evidence.first_try:
        rationale.append("Passed on first try — relatively stronger learning-history signal.")
    elif evidence.attempts and evidence.attempts > 1:
        rationale.append(
            f"Passed after {evidence.attempts} attempts — weaker completion signal than first-try pass."
        )

    if factors.get("curriculum_importance_boost", 0) >= 8:
        rationale.append("Topic sits in a high-importance curriculum segment.")
    if factors.get("role_relevance_boost", 0) >= 5:
        rationale.append("Topic aligns with the candidate's job role keywords.")
    if factors.get("recency_boost", 0) >= 2:
        rationale.append("Topic appears in the candidate's later mission sequence (recency proxy).")

    return rationale
