"""Tests for CurriculumService."""

from app.services.curriculum_service import CurriculumService


def test_load_curriculum(curriculum_service: CurriculumService) -> None:
    curriculum = curriculum_service.load_curriculum()
    assert curriculum.cohort.startswith("AI Cohort")
    assert len(curriculum.modules) == 8
    assert len(curriculum.days) == 31


def test_get_all_modules(curriculum_service: CurriculumService) -> None:
    modules = curriculum_service.get_all_modules()
    assert modules[0].n == 1
    assert modules[-1].n == 8


def test_get_all_days(curriculum_service: CurriculumService) -> None:
    days = curriculum_service.get_all_days()
    assert days[0].day == 1
    assert days[-1].day == 31
    assert all(days[index].day <= days[index + 1].day for index in range(len(days) - 1))


def test_get_day(curriculum_service: CurriculumService) -> None:
    day = curriculum_service.get_day(22)
    assert day is not None
    assert "Multi-Agent" in day.title


def test_get_module(curriculum_service: CurriculumService) -> None:
    module = curriculum_service.get_module(6)
    assert module is not None
    assert module.title == "Agentic AI & MCP"
    assert module.days == [21, 24]
    assert curriculum_service.get_module_for_day(22) == module


def test_get_topic_days(curriculum_service: CurriculumService) -> None:
    topics = curriculum_service.get_topic_days()
    assert len(topics) == 31
    assert topics[7].title == "Embeddings Explained"


def test_get_related_days(curriculum_service: CurriculumService) -> None:
    related = curriculum_service.get_related_days(22)
    related_days = [day.day for day in related]
    assert 21 in related_days
    assert 23 in related_days
    assert 22 not in related_days
