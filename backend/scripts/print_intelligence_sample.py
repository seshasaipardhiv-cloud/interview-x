"""Print sample candidate intelligence output for manual inspection."""

import json
import sys

from app.services.intelligence_inspector import (
    inspect_candidate_intelligence,
    inspect_topic_priorities,
)

CANDIDATE_ID = sys.argv[1] if len(sys.argv) > 1 else "CAND-001"

print(f"=== CANDIDATE INTELLIGENCE: {CANDIDATE_ID} ===")
print(json.dumps(inspect_candidate_intelligence(CANDIDATE_ID), indent=2))
print()
print("=== TOP 5 INTERVIEW PRIORITIES ===")
priorities = inspect_topic_priorities(CANDIDATE_ID, top_n=5)
for index, topic in enumerate(priorities, start=1):
    print(
        f"{index}. Day {topic['day']} - {topic['topic']} "
        f"(priority={topic['interview_priority']})"
    )
    print(
        f"   status={topic['status']}, evidence={topic['evidence_strength']}, "
        f"uncertainty={topic['uncertainty']}"
    )
    print(f"   factors={json.dumps(topic['priority_factors'])}")
    print("   rationale:")
    for line in topic["rationale"]:
        print(f"     - {line}")
    print()
