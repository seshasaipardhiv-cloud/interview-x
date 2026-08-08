# Adaptive Interview Concept

This document describes the intended adaptive interview pipeline. **Not implemented in the scaffold.**

## Pipeline

```
Candidate profile
       │
       ▼
Interview compiler ──► Interview plan (topics, weak areas, min coverage)
       │
       ▼
Candidate state (live knowledge / evidence)
       │
       ▼
Question selection ◄── Adaptive engine (difficulty, depth, follow-ups)
       │
       ▼
Candidate answers
       │
       ▼
Answer analysis (understanding, uncertainty, contradictions)
       │
       ▼
State update (evidence timeline, gaps, strengths)
       │
       ▼
Next question OR final feedback
```

## Inputs

- **31-day AI Cohort curriculum** — day-level topics and learning objectives
- **Candidate profile** — background, focus areas, cohort metadata
- **Learning history** — completed/failed missions, attempts, skipped topics, completion and first-try signals

## Adaptive Behaviors (Future)

- Dynamic question selection (not a fixed questionnaire)
- Follow-ups that depend on previous answers
- Difficulty adaptation based on evidence
- Weak-area and uncertainty detection
- Contradiction / depth probing (later)
- Production incident scenarios (later)

## Output

Final feedback must include:

- **Summary** — overall performance narrative
- **Strengths** — evidence-backed positives
- **Gaps** — areas needing improvement
- **Next** — recommended next steps aligned with curriculum

## Constraints

- Minimum 8 questions per interview
- Questions must span at least 4 different curriculum days
- `sessionId` maintains state across HTTP requests
- Single primary endpoint: `POST /api/interview`
