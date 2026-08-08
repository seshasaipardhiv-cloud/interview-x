"""Maintain live candidate knowledge and evidence state.

Future responsibility:
- Update evidence timeline after each answer
- Track strengths, gaps, and confidence per topic/day
- Provide evidence snapshots for UI and final feedback
"""


class EvidenceEngine:
    """Placeholder for evidence state management."""

    def update(self, session_state: object, analysis: object) -> None:
        """Update evidence state from answer analysis. Not implemented."""
        raise NotImplementedError("EvidenceEngine.update")
