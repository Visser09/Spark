import json, os
from collections import Counter
from datetime import datetime

class Memory:
    """
    Stores conversation history plus lightweight
    interest & project tracking for each child.
    """

    def __init__(self, directory: str):
        os.makedirs(directory, exist_ok=True)
        self.path = os.path.join(directory, "default_profile.json")
        self.data = self._load()

    # ---------- public ---------- #
    def update(self, user_input: str, spark_reply: str):
        topic = self._extract_topic(user_input)
        self._log_history(user_input, spark_reply, topic)
        self._bump_interest(topic)
        self._save()

    def top_interests(self, n=3):
        return [t for t, _ in Counter(self.data["interests"]).most_common(n)]

    # ---------- internal ---------- #
    def _load(self):
        if os.path.exists(self.path):
            with open(self.path) as f:
                return json.load(f)
        return {"history": [], "interests": [], "projects": []}

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=2)

    def _log_history(self, user, spark, topic):
        self.data["history"].append({
            "ts": datetime.utcnow().isoformat(), "user": user,
            "spark": spark, "topic": topic
        })

    def _bump_interest(self, topic):
        if topic:
            self.data["interests"].append(topic)

    @staticmethod
    def _extract_topic(text: str) -> str:
        # naïve first pass – use first noun‑ish word
        tokens = text.lower().split()
        for t in tokens:
            if t.isalpha() and len(t) > 3:
                return t
        return ""
