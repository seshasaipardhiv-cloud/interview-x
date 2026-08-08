"""Pydantic models matching candidates.json schema."""

from pydantic import BaseModel, Field


class Member(BaseModel):
    id: str
    name: str
    jobRole: str
    yearsExperience: int
    education: str
    status: str


class Mission(BaseModel):
    """Mission record — fields vary by outcome (passed, failed, or skipped)."""

    day: int
    title: str
    passed: bool | None = None
    attempts: int | None = None
    skipped: bool | None = None


class CandidateSignals(BaseModel):
    commitDays: int
    missionsCompleted: int
    missionsFirstTry: int


class CandidateRecord(BaseModel):
    member: Member
    missions: list[Mission]
    signals: CandidateSignals
