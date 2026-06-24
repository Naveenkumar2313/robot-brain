import time

class ConversationManager:
    CONTEXT_TIMEOUT = 300  # 5 minutes in seconds

    def __init__(self):
        self.reset()

    def reset(self):
        self.current_topic = None
        self.previous_topic = None
        self.last_question = None
        self.last_answer = None
        self.conversation_stage = "idle"
        self.timestamp = None

    def update(self, intent: str, question: str, answer: str):
        self.previous_topic = self.current_topic
        self.current_topic = intent
        self.last_question = question
        self.last_answer = answer
        self.conversation_stage = "active"
        self.timestamp = time.time()

    def is_timed_out(self) -> bool:
        if self.timestamp is None:
            return False
        return (time.time() - self.timestamp) > self.CONTEXT_TIMEOUT

    def resolve_intent(self, detected_intent: str) -> str:
        """
        If intent is UNKNOWN but we have an active topic,
        try to stay in context instead of giving up.
        """
        if detected_intent == "UNKNOWN" and self.current_topic:
            return self.current_topic
        return detected_intent

    def get_context_summary(self) -> str:
        if self.current_topic is None:
            return "No active context."
        return (
            f"Topic: {self.current_topic} | "
            f"Previous: {self.previous_topic} | "
            f"Stage: {self.conversation_stage}"
        )