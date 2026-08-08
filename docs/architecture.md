# INTERVIEW-X Architecture

High-level architecture for the evidence-driven, self-adaptive technical interview system.

## Goals

- Conduct realistic multi-turn technical interviews (minimum 8 questions, 4+ curriculum days)
- Personalize using cohort curriculum, candidate profiles, and learning history
- Maintain conversation context and session state via `sessionId`
- Remain modular for live feature-steer challenges during the hackathon finals

## System Overview

```
┌─────────────┐     POST /api/interview      ┌──────────────────────────────┐
│   React     │ ◄──────────────────────────► │         FastAPI              │
│   (Vite)    │         sessionId            │  api/ │ core/ │ models/      │
└─────────────┘                              └──────────────┬───────────────┘
                                                            │
                    ┌───────────────────────────────────────┼───────────────────────┐
                    ▼                                       ▼                       ▼
            candidate_service                          state (sessions)      curriculum_service
            interview_compiler                         evidence_engine       question_engine
            answer_analyzer                            adaptive_engine       feedback_engine
                                                       llm_service
```

## Backend Layers

| Layer | Responsibility |
|-------|----------------|
| `api/` | HTTP routes, request/response validation, error handling |
| `models/` | Pydantic schemas for candidates, interview turns, feedback |
| `core/` | Configuration, session state store (placeholder) |
| `services/` | Business logic modules (data ingestion, intelligence, interview engines) |
| `data/` | Organizer-provided `curriculum.json` and `candidates.json` (source of truth) |

## Data Ingestion & Candidate Intelligence (Implemented)

This layer is **deterministic Python** — no LLM, vector DB, graph DB, Redis, or agent frameworks.

```
curriculum.json
      +
candidates.json
      ↓
CurriculumService
      +
CandidateService
      ↓
Candidate Intelligence  (candidate_intelligence.py)
      ↓
Topic Evidence          (topic_evidence.py — strength & uncertainty scoring)
      ↓
Interview Priority      (topic_priority.py — ranked investigation targets)
```

### Module responsibilities

| Module | Role |
|--------|------|
| `curriculum_service.py` | Load/query curriculum modules, days, topic index, related days |
| `candidate_service.py` | Load/query candidates, missions, attempt stats, learning signals |
| `topic_evidence.py` | Deterministic evidence strength & uncertainty from mission outcomes |
| `topic_priority.py` | Weighted, modular priority scoring (replaceable weights) |
| `candidate_intelligence.py` | Compose full intelligence + ranked priorities per candidate |
| `intelligence_inspector.py` | Internal inspection helpers for tests/debug (not public HTTP) |

### Scoring notes

- Mission outcomes are **learning-history evidence**, not proof of mastery.
- Skipped missions → low evidence, high uncertainty, high interview priority.
- Failed missions → low evidence, high uncertainty, high interview priority.
- Multi-attempt passes → lower evidence strength than first-try passes.
- Priority weights live in `topic_priority.py` and are intended to be refined later.

## Frontend Layers

| Layer | Responsibility |
|-------|----------------|
| `pages/` | Route-level views (Home, Interview) |
| `components/` | Reusable UI: selector, panel, state, timeline, progress, feedback |
| `services/` | API client for backend communication |

## Session Flow (Planned)

1. Client starts or resumes interview with `sessionId`
2. Backend loads or creates session state for the candidate
3. Interview compiler builds plan from profile + learning history
4. Question engine selects next question; adaptive engine adjusts difficulty
5. Answer analyzer processes response; evidence engine updates state
6. Repeat until interview completes; feedback engine produces final report

## Non-Goals (Scaffold / Hackathon Scope)

- Authentication, voice, mobile apps
- Vector DB, graph DB, Redis, Kafka, LangChain, CrewAI (unless clearly needed later)
- Microservices split beyond modular monolith

## Deployment

- `backend/Dockerfile` — production-ready FastAPI container
- `docker-compose.yml` — local orchestration of backend + frontend dev server
