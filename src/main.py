import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from intent_detector import detect_intent
from knowledge_manager import get_knowledge
from response_generator import generate_response
from conversation_manager import ConversationManager

FOLLOW_UPS = {
    "COMPANY_SERVICES":     "Would you like to know more about any specific service?",
    "WORKSHOPS":            "Would you like to know the duration or schedule of any workshop?",
    "COLLEGE_PLACEMENTS":   "Would you like to know which companies visited recently?",
    "COLLEGE_DEPARTMENTS":  "Would you like to know more about a specific department?",
    "COLLEGE_FACILITIES":   "Would you like to know about hostel or sports facilities specifically?",
    "COMPANY_PRODUCTS":     "Would you like to know more about Codorythm?",
    "COMPANY_TEAM":         "Would you like to know more about what the team has built?",
}

def run():
    context = ConversationManager()
    print("=" * 60)
    print("  PyGenicArc Robot Brain — Conversation Simulator")
    print("  Type 'quit' to exit | Type 'context' to see memory")
    print("=" * 60)

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except KeyboardInterrupt:
            print("\nRobot: Goodbye! Have a great day!")
            break

        if not user_input:
            continue

        if user_input.lower() == "quit":
            print("Robot: Goodbye! Have a great day!")
            break

        if user_input.lower() == "context":
            print(f"[CONTEXT] {context.get_context_summary()}")
            continue

        # Check timeout
        if context.is_timed_out():
            context.reset()
            print("[CONTEXT] Session reset due to inactivity.")

        # Detect intent
        intent, score = detect_intent(user_input)

        # Resolve using context if UNKNOWN
        resolved_intent = context.resolve_intent(intent)

        # Get knowledge
        knowledge = get_knowledge(resolved_intent)

        # Generate response
        response = generate_response(resolved_intent, knowledge)

        # Update context
        context.update(resolved_intent, user_input, response)

        # Print response
        print(f"Robot: {response}")

        # Optional follow-up
        follow_up = FOLLOW_UPS.get(resolved_intent)
        if follow_up:
            print(f"Robot: {follow_up}")


if __name__ == "__main__":
    run()