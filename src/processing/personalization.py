import json
import os

PROFILE_PATH = "data/user_profile.json"

def load_profile():
    if os.path.exists(PROFILE_PATH):
        with open(PROFILE_PATH, "r") as f:
            return json.load(f)
    return {
        "name": "Student",
        "mode": "Standard",
        "quiz_scores": [],
        "topics_studied": []
    }

def save_profile(profile):
    os.makedirs(os.path.dirname(PROFILE_PATH), exist_ok=True)
    with open(PROFILE_PATH, "w") as f:
        json.dump(profile, f, indent=4)

def record_quiz_score(topic, score, total):
    profile = load_profile()
    profile["quiz_scores"].append({
        "topic": topic,
        "score": score,
        "total": total,
        "percentage": (score / total) * 100 if total > 0 else 0
    })
    save_profile(profile)

def add_topic_studied(topic):
    profile = load_profile()
    if topic not in profile["topics_studied"]:
        profile["topics_studied"].append(topic)
    save_profile(profile)

def get_weaknesses():
    profile = load_profile()
    weaknesses = []
    # Simple logic: average scores per topic, if < 60% it's a weakness
    topic_scores = {}
    for entry in profile.get("quiz_scores", []):
        t = entry["topic"]
        if t not in topic_scores:
            topic_scores[t] = []
        topic_scores[t].append(entry["percentage"])
        
    for t, scores in topic_scores.items():
        avg = sum(scores) / len(scores)
        if avg < 60:
            weaknesses.append((t, avg))
            
    # Sort by lowest average
    weaknesses.sort(key=lambda x: x[1])
    return [w[0] for w in weaknesses]
