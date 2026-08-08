"""End-to-end mock interview simulator."""

import json
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def run_mock_interview():
    print("==================================================")
    print("STARTING END-TO-END MOCK INTERVIEW")
    print("==================================================")
    
    # 1. Start interview
    session_id = "mock-session-999"
    payload = {
        "sessionId": session_id,
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
    data = response.json()
    
    print(f"\n[INTERVIEWER]: {data['reply']}")
    
    turns = 0
    feedback = None
    
    while not data.get("done") and turns < 15:
        turns += 1
        msg = f"This is my answer for turn {turns}"
        print(f"\n[CANDIDATE]: {msg}")
        
        res = client.post("/api/interview", json={
            "sessionId": session_id,
            "message": msg
        })
        
        data = res.json()
        print(f"\n[INTERVIEWER]: {data['reply']}")
        
        if data.get("done"):
            feedback = data.get("feedback")
            break

    print("\n==================================================")
    print("INTERVIEW COMPLETE")
    print("==================================================")
    
    from app.core.state import session_store
    session = session_store.get(session_id)
    
    print(f"Candidate: {session.candidate.member.name} ({session.candidate.member.id})")
    print(f"Session: {session.session_id}")
    print(f"Questions asked: {session.question_count}")
    print(f"Unique curriculum days: {len(set(session.curriculum_days_covered))}")
    
    total_follow_ups = len(session.conversation_history) // 2 - session.question_count
    # actually a better way to count follow-ups is comparing total asked questions vs base slots completed
    print(f"Follow-ups: {max(0, total_follow_ups)}")
    print("Final feedback:")
    print(json.dumps(feedback, indent=2))


if __name__ == "__main__":
    run_mock_interview()
