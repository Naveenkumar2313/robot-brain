import json
import os

BASE = os.path.join(os.path.dirname(__file__), '..', 'knowledge')

def _load(filename):
    with open(os.path.join(BASE, filename), 'r') as f:
        return json.load(f)

def get_knowledge(intent: str) -> dict:
    company  = _load('company.json')
    college  = _load('college.json')
    faqs     = _load('faq.json')

    mapping = {
        "COMPANY_NAME":         {"key": "name",          "data": company,  "label": "Company Name"},
        "COMPANY_SERVICES":     {"key": "services",      "data": company,  "label": "Services"},
        "COMPANY_VISION":       {"key": "vision",        "data": company,  "label": "Vision"},
        "COMPANY_MISSION":      {"key": "mission",       "data": company,  "label": "Mission"},
        "COMPANY_PRODUCTS":     {"key": "products",      "data": company,  "label": "Products"},
        "COMPANY_TEAM":         {"key": "founders",      "data": company,  "label": "Founders"},
        "WORKSHOPS":            {"key": "workshops",     "data": company,  "label": "Workshops"},
        "COLLEGE_INFO":         {"key": "name",          "data": college,  "label": "College"},
        "COLLEGE_PRINCIPAL":    {"key": "principal",     "data": college,  "label": "Principal"},
        "COLLEGE_DEPARTMENTS":  {"key": "departments",   "data": college,  "label": "Departments"},
        "COLLEGE_FACILITIES":   {"key": "facilities",    "data": college,  "label": "Facilities"},
        "COLLEGE_PLACEMENTS":   {"key": "placements",    "data": college,  "label": "Placements"},
        "COLLEGE_COURSES":      {"key": "courses",       "data": college,  "label": "Courses"},
        "COLLEGE_FACULTY":      {"key": "faculty",       "data": college,  "label": "Faculty"},
    }

    if intent not in mapping:
        return {"found": False, "intent": intent}

    entry = mapping[intent]
    value = entry["data"].get(entry["key"], None)

    return {
        "found": True,
        "intent": intent,
        "label": entry["label"],
        "value": value
    }


if __name__ == "__main__":
    test_intents = [
        "COMPANY_SERVICES",
        "COMPANY_VISION",
        "WORKSHOPS",
        "COLLEGE_PLACEMENTS",
        "COLLEGE_DEPARTMENTS",
        "UNKNOWN"
    ]

    for intent in test_intents:
        result = get_knowledge(intent)
        print(f"\nIntent : {result['intent']}")
        if result['found']:
            print(f"Label  : {result['label']}")
            print(f"Value  : {result['value']}")
        else:
            print("Result : No knowledge found.")