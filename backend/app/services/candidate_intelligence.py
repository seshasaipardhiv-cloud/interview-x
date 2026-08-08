"""Build deterministic candidate intelligence from curriculum + learning history."""

from __future__ import annotations

from app.models.intelligence import (
    CandidateIntelligence,
    InterviewPriorityTopic,
    MissionStatus,
    TopicEvidence,
)
from app.services.candidate_service import CandidateService, get_candidate_service
from app.services.curriculum_service import CurriculumService, get_curriculum_service
from app.services.topic_evidence import (
    compute_evidence_strength,
    compute_uncertainty,
    is_first_try_pass,
    resolve_topic_title,
)
from app.services.topic_priority import (
    build_priority_rationale,
    compute_interview_priority,
)


class CandidateIntelligenceBuilder:
    """Compose candidate intelligence and ranked interview priorities."""

    def __init__(
        self,
        candidate_service: CandidateService | None = None,
        curriculum_service: CurriculumService | None = None,
    ) -> None:
        self._candidates = candidate_service or get_candidate_service()
        self._curriculum = curriculum_service or get_curriculum_service()

    def build(self, candidate_id: str) -> CandidateIntelligence:
        """Build full candidate intelligence for one candidate."""
        candidate = self._candidates.get_candidate(candidate_id)
        member = candidate.member
        stats = self._candidates.get_attempt_statistics(candidate_id)

        completed_topics: list[int] = []
        failed_topics: list[int] = []
        skipped_topics: list[int] = []
        attempt_counts: dict[int, int] = {}
        first_try_signals: list[int] = []
        topic_evidence: list[TopicEvidence] = []

        max_mission_day = max((mission.day for mission in candidate.missions), default=0)

        for mission in candidate.missions:
            status = self._candidates.mission_status(mission)
            curriculum_day = self._curriculum.get_day(mission.day)
            topic_title = resolve_topic_title(
                mission,
                curriculum_day.title if curriculum_day else None,
            )

            if status == MissionStatus.PASSED:
                completed_topics.append(mission.day)
            elif status == MissionStatus.FAILED:
                failed_topics.append(mission.day)
            elif status == MissionStatus.SKIPPED:
                skipped_topics.append(mission.day)

            if mission.attempts is not None:
                attempt_counts[mission.day] = mission.attempts
            if is_first_try_pass(mission, status):
                first_try_signals.append(mission.day)

            evidence = TopicEvidence(
                day=mission.day,
                topic=topic_title,
                status=status,
                attempts=mission.attempts,
                first_try=is_first_try_pass(mission, status),
                evidence_strength=compute_evidence_strength(status, mission.attempts),
                uncertainty=compute_uncertainty(status, mission.attempts),
            )

            priority, factors = compute_interview_priority(
                evidence,
                curriculum_day,
                member.jobRole,
                max_mission_day,
            )
            evidence.interview_priority = priority
            evidence.priority_factors = factors
            topic_evidence.append(evidence)

        completion_signals = {
            "commit_days": candidate.signals.commitDays,
            "missions_completed": candidate.signals.missionsCompleted,
            "missions_first_try": candidate.signals.missionsFirstTry,
            "recorded_pass_count": stats["passed_count"],
            "recorded_fail_count": stats["failed_count"],
            "recorded_skip_count": stats["skipped_count"],
            "recorded_first_try_pass_count": stats["first_try_pass_count"],
        }

        return CandidateIntelligence(
            candidate_id=member.id,
            name=member.name,
            job_role=member.jobRole,
            years_experience=member.yearsExperience,
            education=member.education,
            cohort_status=member.status,
            completed_topics=sorted(completed_topics),
            failed_topics=sorted(failed_topics),
            skipped_topics=sorted(skipped_topics),
            attempt_counts=attempt_counts,
            first_try_signals=sorted(first_try_signals),
            completion_signals=completion_signals,
            topic_evidence=sorted(topic_evidence, key=lambda item: item.day),
            aggregate_signals=candidate.signals,
        )

    def rank_topic_priorities(
        self,
        candidate_id: str,
        top_n: int | None = None,
    ) -> list[InterviewPriorityTopic]:
        """Return topics sorted by interview priority (descending)."""
        intelligence = self.build(candidate_id)
        ranked = sorted(
            intelligence.topic_evidence,
            key=lambda item: (-item.interview_priority, item.day),
        )
        if top_n is not None:
            ranked = ranked[:top_n]

        results: list[InterviewPriorityTopic] = []
        for evidence in ranked:
            results.append(
                InterviewPriorityTopic(
                    day=evidence.day,
                    topic=evidence.topic,
                    status=evidence.status,
                    interview_priority=evidence.interview_priority,
                    evidence_strength=evidence.evidence_strength,
                    uncertainty=evidence.uncertainty,
                    priority_factors=evidence.priority_factors,
                    rationale=build_priority_rationale(evidence, evidence.priority_factors),
                )
            )
        return results


def build_candidate_intelligence(candidate_id: str) -> CandidateIntelligence:
    """Convenience wrapper for intelligence construction."""
    return CandidateIntelligenceBuilder().build(candidate_id)


def rank_interview_priorities(candidate_id: str, top_n: int = 5) -> list[InterviewPriorityTopic]:
    """Convenience wrapper for priority ranking."""
    return CandidateIntelligenceBuilder().rank_topic_priorities(candidate_id, top_n=top_n)
