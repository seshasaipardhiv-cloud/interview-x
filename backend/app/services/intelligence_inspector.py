"""Internal inspection helpers for candidate intelligence (testing / debugging).

Not exposed as public HTTP endpoints. Use in tests, scripts, or REPL.
"""

from __future__ import annotations

from app.services.candidate_intelligence import (
    build_candidate_intelligence,
    rank_interview_priorities,
)
from app.services.candidate_service import get_candidate_service


def inspect_candidate_profile(candidate_id: str) -> dict[str, object]:
    """Return raw profile and organizer signals for a candidate."""
    service = get_candidate_service()
    member = service.get_member(candidate_id)
    return {
        "profile": member.model_dump(),
        "signals": service.get_signals(candidate_id).model_dump(),
        "attempt_statistics": service.get_attempt_statistics(candidate_id),
        "learning_signals": service.get_learning_signals(candidate_id),
    }


def inspect_candidate_intelligence(candidate_id: str) -> dict[str, object]:
    """Return structured candidate intelligence as a JSON-serializable dict."""
    intelligence = build_candidate_intelligence(candidate_id)
    return intelligence.model_dump()


def inspect_topic_priorities(candidate_id: str, top_n: int = 5) -> list[dict[str, object]]:
    """Return top-N interview priority topics with rationale."""
    priorities = rank_interview_priorities(candidate_id, top_n=top_n)
    return [item.model_dump() for item in priorities]
