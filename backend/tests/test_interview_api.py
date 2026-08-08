import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.core.state import session_store
from app.models.candidate import CandidateRecord

client = TestClient(app)

@pytest.fixture
def clean_session():
    # Clear out sessions before tests
    session_store._sessions = {}


def test_interview_lifecycle(clean_session):
    # 1. Start interview
    payload = {
        "sessionId": "test-session-123",
        "candidate": {
            "member": {
                "id": "CAND-001",
                "name": "Sarah Johnson",
                "jobRole": "Senior Data Engineer",
                "yearsExperience": 6,
                "education": "BS Computer Science",
                "status": "Active"
            },
            "missions": [],
            "signals": {
                "commitDays": 10,
                "missionsCompleted": 5,
                "missionsFirstTry": 3
            }
        }
    }
    
    response = client.post("/api/interview", json=payload)
    assert response.status_code == 200, response.json()
    data = response.json()
    assert data["done"] is False
    assert "reply" in data
    assert len(data["reply"]) > 0

    # 2. Continue interview multiple turns to completion
    # The mock LLM does alternating STRONG/PARTIAL/MISCONCEPTION so it will adapt.
    # We will simulate enough turns to finish the interview.
    # The plan guarantees 8 questions, so we might need ~8-12 turns.
    
    turns = 0
    max_turns = 15
    while turns < max_turns:
        turns += 1
        payload = {
            "sessionId": "test-session-123",
            "message": f"My mock answer {turns}"
        }
        res = client.post("/api/interview", json=payload)
        assert res.status_code == 200, res.json()
        data = res.json()
        
        if data["done"]:
            # Check feedback
            assert "feedback" in data
            assert data["feedback"] is not None
            assert "summary" in data["feedback"]
            assert "strengths" in data["feedback"]
            assert "gaps" in data["feedback"]
            assert "next_steps" in data["feedback"]
            break
            
    assert turns < max_turns, "Interview did not complete within expected turns."
