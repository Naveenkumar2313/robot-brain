import json
import os

# Load intents once
INTENTS_PATH = os.path.join(os.path.dirname(__file__), '..', 'intents', 'intents.json')

with open(INTENTS_PATH, 'r') as f:
    INTENTS_DATA = json.load(f)['intents']


def detect_intent(user_input: str) -> tuple[str, float]:
    text = user_input.lower().strip()
    
    best_intent = "UNKNOWN"
    best_score = 0.0

    for intent, data in INTENTS_DATA.items():
        if intent == "UNKNOWN":
            continue
        
        keywords = data.get("keywords", [])
        hits = sum(1 for kw in keywords if kw in text)
        
        if hits == 0:
            continue
        
        score = hits / len(keywords)
        
        if hits > best_score or (hits == best_score and score > 0):
            best_intent = intent
            best_score = hits

    return best_intent, best_score


if __name__ == "__main__":
    test_questions = [
        "Hello there",
        "What services do you provide?",
        "Tell me about placements",
        "Who are the founders?",
        "What workshops do you conduct?",
        "What is the vision of PyGenicArc?",
        "Who is the principal?",
        "What courses are available?",
        "Goodbye",
        "What is the meaning of life?"
    ]

    print(f"{'Question':<45} {'Intent':<25} {'Score'}")
    print("-" * 80)
    for q in test_questions:
        intent, score = detect_intent(q)
        print(f"{q:<45} {intent:<25} {score:.2f}")