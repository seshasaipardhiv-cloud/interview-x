import sys
import json
from app.services.candidate_intelligence import build_candidate_intelligence, rank_interview_priorities

def main():
    candidate_id = "CAND-011"
    intelligence = build_candidate_intelligence(candidate_id)
    print(f"Candidate: {intelligence.name}")
    print(f"Role: {intelligence.job_role}")
    print(f"Experience: {intelligence.years_experience} years\n")
    
    print(f"Top completed topics: {intelligence.completed_topics[:5]}")
    
    uncertain_topics = [t.topic for t in sorted(intelligence.topic_evidence, key=lambda x: -x.uncertainty)]
    print(f"Top uncertain topics: {uncertain_topics[:5]}\n")
    
    print("Top 5 interview priorities:")
    priorities = rank_interview_priorities(candidate_id, 5)
    for idx, p in enumerate(priorities, 1):
        print(f"{idx}. Day {p.day} - {p.topic} (Priority: {p.interview_priority})")
        print(f"   Rationale: {' '.join(p.rationale)}\n")
        
    print("Full CandidateIntelligence dump:")
    print(intelligence.model_dump_json(indent=2))

if __name__ == "__main__":
    main()
