# INTERVIEW-X

## Problem

Technical interviews for AI engineering cohorts often rely on static question banks that ignore what candidates have actually learned, where they struggled, and how they perform under follow-up pressure. This produces interviews that feel generic, fail to surface real gaps, and offer little actionable feedback tied to a structured curriculum.

## Proposed Solution

INTERVIEW-X is an evidence-driven, self-adaptive technical interview agent. It compiles each candidate's learning journey (curriculum progress, mission outcomes, and behavioral signals) into a personalized interview plan, maintains live knowledge/evidence state during the conversation, dynamically selects and adapts questions with context-aware follow-ups, and generates evidence-backed final feedback with strengths, gaps, and next steps.

## Current Development Stage

**Scaffold only.** The repository contains modular backend and frontend structure, placeholder services, Pydantic models, and documentation. The adaptive interview engine, curriculum integration, and full API contract are not implemented yet.

## Planned Architecture

```
Candidate profile + learning history
        │
        ▼
Interview compiler ──► Session state (sessionId)
        │
        ▼
Question engine ◄──► Adaptive engine
        │
        ▼
Answer analyzer ──► Evidence engine ──► Feedback engine
        │
        ▼
POST /api/interview (multi-turn, min 8 questions, 4+ curriculum days)
```

- **Backend:** Python, FastAPI, Pydantic, modular services under `backend/app/services/`
- **Frontend:** React + Vite, interview UI components under `frontend/src/`
- **State:** In-memory session store (placeholder in `core/state.py`); no external infra at scaffold stage

## Local Setup (Placeholder)

### Backend

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your settings
uvicorn app.main:app --reload --port 8000
```

Health check: `GET http://localhost:8000/health`

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

### Docker (optional)

```bash
docker compose up --build
```

## Documentation

- [Architecture](docs/architecture.md)
- [Adaptive Interview Concept](docs/adaptive-interview.md)
- [Demo Script (placeholder)](docs/demo-script.md)
- [AI Usage Log](AI_USAGE_LOG.md)
