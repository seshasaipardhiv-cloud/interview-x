"""Load and query organizer-provided candidate learning history."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from app.models.candidate import CandidateRecord, CandidateSignals, Member, Mission
from app.models.intelligence import MissionStatus

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "candidates.json"


class CandidateNotFoundError(KeyError):
    """Raised when a candidate id is not present in candidates.json."""


class CandidateService:
    """Read-only access to candidates.json."""

    def __init__(self, data_path: Path | None = None) -> None:
        self._data_path = data_path or DATA_PATH
        self._candidates: list[CandidateRecord] | None = None
        self._by_id: dict[str, CandidateRecord] = {}

    def _load(self) -> None:
        if self._candidates is None:
            with self._data_path.open(encoding="utf-8") as handle:
                payload = json.load(handle)
            self._candidates = [
                CandidateRecord.model_validate(record) for record in payload["candidates"]
            ]
            self._by_id = {record.member.id: record for record in self._candidates}

    @staticmethod
    def mission_status(mission: Mission) -> MissionStatus:
        if mission.skipped is True:
            return MissionStatus.SKIPPED
        if mission.passed is False:
            return MissionStatus.FAILED
        return MissionStatus.PASSED

    def get_all_candidates(self) -> list[CandidateRecord]:
        """Return all candidate records."""
        self._load()
        assert self._candidates is not None
        return list(self._candidates)

    def get_candidate(self, candidate_id: str) -> CandidateRecord:
        """Return a candidate by id."""
        self._load()
        try:
            return self._by_id[candidate_id]
        except KeyError as exc:
            raise CandidateNotFoundError(candidate_id) from exc

    def get_completed_missions(self, candidate_id: str) -> list[Mission]:
        """Return missions marked passed."""
        candidate = self.get_candidate(candidate_id)
        return [mission for mission in candidate.missions if mission.passed is True]

    def get_skipped_missions(self, candidate_id: str) -> list[Mission]:
        """Return missions marked skipped."""
        candidate = self.get_candidate(candidate_id)
        return [mission for mission in candidate.missions if mission.skipped is True]

    def get_failed_missions(self, candidate_id: str) -> list[Mission]:
        """Return missions marked failed."""
        candidate = self.get_candidate(candidate_id)
        return [mission for mission in candidate.missions if mission.passed is False]

    def get_attempt_statistics(self, candidate_id: str) -> dict[str, object]:
        """Return deterministic attempt statistics for a candidate."""
        candidate = self.get_candidate(candidate_id)
        passed = self.get_completed_missions(candidate_id)
        failed = self.get_failed_missions(candidate_id)
        skipped = self.get_skipped_missions(candidate_id)

        attempts_values = [
            mission.attempts
            for mission in candidate.missions
            if mission.attempts is not None
        ]
        first_try_passes = [
            mission for mission in passed if mission.attempts == 1
        ]

        by_day: dict[int, dict[str, object]] = {}
        for mission in candidate.missions:
            by_day[mission.day] = {
                "title": mission.title,
                "status": self.mission_status(mission).value,
                "attempts": mission.attempts,
                "skipped": mission.skipped is True,
                "passed": mission.passed,
            }

        average_attempts = (
            sum(attempts_values) / len(attempts_values) if attempts_values else 0.0
        )

        return {
            "candidate_id": candidate_id,
            "total_missions_recorded": len(candidate.missions),
            "passed_count": len(passed),
            "failed_count": len(failed),
            "skipped_count": len(skipped),
            "total_attempts": sum(attempts_values),
            "average_attempts_on_recorded": round(average_attempts, 2),
            "first_try_pass_count": len(first_try_passes),
            "max_attempts": max(attempts_values) if attempts_values else 0,
            "by_day": by_day,
        }

    def get_learning_signals(self, candidate_id: str) -> dict[str, object]:
        """Return organizer signals plus derived per-mission learning signals."""
        candidate = self.get_candidate(candidate_id)
        stats = self.get_attempt_statistics(candidate_id)

        per_mission_signals = []
        for mission in candidate.missions:
            status = self.mission_status(mission)
            per_mission_signals.append(
                {
                    "day": mission.day,
                    "title": mission.title,
                    "status": status.value,
                    "attempts": mission.attempts,
                    "first_try_pass": mission.passed is True and mission.attempts == 1,
                    "completion_signal": status == MissionStatus.PASSED,
                }
            )

        return {
            "candidate_id": candidate_id,
            "organizer_signals": candidate.signals.model_dump(),
            "derived": {
                "recorded_missions": stats["total_missions_recorded"],
                "passed_count": stats["passed_count"],
                "failed_count": stats["failed_count"],
                "skipped_count": stats["skipped_count"],
                "first_try_pass_count": stats["first_try_pass_count"],
            },
            "missions": per_mission_signals,
        }

    def get_member(self, candidate_id: str) -> Member:
        """Return candidate identity fields."""
        return self.get_candidate(candidate_id).member

    def get_signals(self, candidate_id: str) -> CandidateSignals:
        """Return organizer-provided aggregate signals."""
        return self.get_candidate(candidate_id).signals


@lru_cache(maxsize=1)
def get_candidate_service() -> CandidateService:
    """Shared candidate service instance."""
    service = CandidateService()
    service._load()
    return service
