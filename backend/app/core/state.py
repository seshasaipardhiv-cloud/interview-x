"""In-memory session state store (placeholder).

Future implementation will persist interview sessions keyed by sessionId,
including conversation history, evidence timeline, question progress, and
adaptive engine state across POST /api/interview requests.
"""

from typing import Any
from uuid import uuid4


class SessionStateStore:
    """Placeholder for session-scoped interview state."""

    def __init__(self) -> None:
        self._sessions: dict[str, dict[str, Any]] = {}

    def create_session(self, initial: dict[str, Any] | None = None) -> str:
        """Create a new session and return its sessionId."""
        session_id = str(uuid4())
        self._sessions[session_id] = initial or {}
        return session_id

    def get(self, session_id: str) -> dict[str, Any] | None:
        """Retrieve session state by sessionId."""
        return self._sessions.get(session_id)

    def set(self, session_id: str, state: dict[str, Any]) -> None:
        """Replace session state for sessionId."""
        self._sessions[session_id] = state

    def delete(self, session_id: str) -> None:
        """Remove a session."""
        self._sessions.pop(session_id, None)


# Module-level singleton for future use by interview services
session_store = SessionStateStore()
