import json
import os
import random

TEMPLATES_PATH = os.path.join(os.path.dirname(__file__), '..', 'knowledge', 'response_templates.json')

with open(TEMPLATES_PATH, 'r') as f:
    TEMPLATES = json.load(f)


def _format_value(value) -> str:
    if isinstance(value, list):
        return ", ".join(str(v) for v in value)
    return str(value)


def generate_response(intent: str, knowledge: dict) -> str:
    templates = TEMPLATES.get(intent, TEMPLATES["UNKNOWN"])
    template = random.choice(templates)

    # Intents with no knowledge value needed
    if intent in ("GREETING", "GOODBYE", "THANK_YOU", "UNKNOWN"):
        return template

    # Special case: placements has nested keys
    if intent == "COLLEGE_PLACEMENTS" and knowledge.get("found"):
        value = knowledge.get("value", {})
        rate = value.get("rate", "N/A")
        companies = ", ".join(value.get("companies", []))
        return template.format(rate=rate, companies=companies)

    # General case
    if knowledge.get("found"):
        value = _format_value(knowledge.get("value", ""))
        return template.format(value=value)

    return random.choice(TEMPLATES["UNKNOWN"])


if __name__ == "__main__":
    from intent_detector import get_knowledge

    test_intents = [
        "GREETING",
        "COMPANY_SERVICES",
        "COMPANY_VISION",
        "WORKSHOPS",
        "COLLEGE_PLACEMENTS",
        "COLLEGE_DEPARTMENTS",
        "GOODBYE",
        "UNKNOWN"
    ]

    print("=" * 60)
    for intent in test_intents:
        knowledge = get_knowledge(intent)
        response = generate_response(intent, knowledge)
        print(f"Intent   : {intent}")
        print(f"Response : {response}")
        print("-" * 60)