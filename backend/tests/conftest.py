"""Shared pytest fixtures."""

import pytest

from app.services.candidate_service import CandidateService
from app.services.curriculum_service import CurriculumService


@pytest.fixture
def curriculum_service() -> CurriculumService:
    return CurriculumService()


@pytest.fixture
def candidate_service() -> CandidateService:
    return CandidateService()
