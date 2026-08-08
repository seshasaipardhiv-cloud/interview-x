# INTERVIEW-X

## Problem

Technical interviews for AI engineering cohorts often rely on static question banks that ignore what candidates have actually learned, where they struggled, and how they perform under follow-up pressure. This produces interviews that feel generic, fail to surface real gaps, and offer little actionable feedback tied to a structured curriculum.

## Solution: INTERVIEW-X

INTERVIEW-X is an evidence-driven, self-adaptive technical interview agent. It compiles each candidate's learning journey (curriculum progress, mission outcomes, and behavioral signals) into a personalized interview plan, maintains live knowledge/evidence state during the conversation, dynamically selects and adapts questions with context-aware follow-ups, and generates evidence-backed final feedback with strengths, gaps, and next steps.

**Judge Mode**: The UI is optimized for demonstrations and evaluations. It allows instant loading of specific candidate profiles and beautifully tracks the backend's hidden adaptive decisions—like follow-ups, curriculum coverage, and phase advancements—in real time.

## Architecture

```text
Candidate Profile + Learning History
        │
        ▼
Interview Compiler ──► Session State (In-Memory)
        │
        ▼
Question Engine ◄──► Adaptive Engine (Follow-Ups/Advance/Finish)
        │
        ▼
Answer Analyzer ──► Evidence Engine ──► Feedback Engine
        │
        ▼
POST /api/interview (multi-turn, min 8 questions, 4+ curriculum days)
```

- **Backend:** Python, FastAPI, Pydantic, structured logging, safe exception handling.
- **Frontend:** React + Vite, responsive sleek glassmorphism UI.
- **State:** In-memory session store (suitable for hackathon/demonstration deployment).

## Setup & Running

### Local Development

**Backend (Python 3.11+)**:
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```
Health check: `GET http://localhost:8000/health`

**Frontend (Node 20+)**:
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

### Production / Docker Setup

You can easily launch the entire stack using Docker Compose:

```bash
docker compose up --build
```
- Frontend will be available at: `http://localhost:5173`
- Backend API is running on: `http://localhost:8000`

## Demo Instructions

1. Start the application (via local dev servers or Docker).
2. Open the frontend in your browser.
3. You will see the **Judge Mode** entry screen.
4. Select one of the three real candidates (e.g., Sarah Johnson).
5. A Candidate Preview card will appear, showing their experience and the dynamic strategy prepared.
6. Click **Initialize Interview Session**.
7. Chat with the AI! Watch the right panel dynamically update as the backend adapts to your answers.
8. Finish the interview to see the detailed Feedback Report and metrics.

## Documentation

- [Architecture](docs/architecture.md)
- [Adaptive Interview Concept](docs/adaptive-interview.md)
- [Deployment Guide](docs/deployment.md)
