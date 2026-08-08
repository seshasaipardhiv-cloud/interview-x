import json
from app.services.interview_compiler import compile_interview_plan
from app.services.candidate_intelligence import build_candidate_intelligence

def inspect_candidate(candidate_id: str):
    intelligence = build_candidate_intelligence(candidate_id)
    plan = compile_interview_plan(candidate_id)
    
    weak = sorted(intelligence.topic_evidence, key=lambda x: -x.uncertainty)
    top_uncertainty = weak[0].topic if weak else "None"
    
    print("-" * 50)
    print(f"Candidate: {intelligence.name} ({candidate_id})")
    print(f"Role: {intelligence.job_role}")
    print(f"Top uncertainty: {top_uncertainty}")
    print(f"Selected curriculum days: {plan.summary.curriculum_days_covered}")
    
    print("\nQuestion slots:")
    for idx, slot in enumerate(plan.slots, 1):
        print(f"  Slot {idx} [{slot.phase.value.upper()}] - Day {slot.curriculum_day}: {slot.topic}")
        if slot.secondary_curriculum_day:
            print(f"    Secondary: Day {slot.secondary_curriculum_day}: {slot.secondary_topic}")
        print(f"    Objective: {slot.objective}")
        print(f"    Type: {slot.question_type.value}")
        print(f"    Difficulty: {slot.target_difficulty.value}")
        print(f"    Reason: {slot.reason}")
        
    return plan, intelligence.name

def main():
    candidates = ["CAND-001", "CAND-007", "CAND-011"]
    results = {}
    
    for c_id in candidates:
        plan, name = inspect_candidate(c_id)
        results[name] = plan.summary.topics_covered
        
    print("=" * 50)
    print("CONCISE COMPARISON")
    print("=" * 50)
    for name, topics in results.items():
        print(f"{name}:")
        print(f"selected topics = {topics}\n")

if __name__ == "__main__":
    main()
