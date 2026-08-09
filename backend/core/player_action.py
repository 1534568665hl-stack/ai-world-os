from backend.core.event_detector import EventDetector


class PlayerActionProcessor:
    """Convert a detected player event into a deterministic action result."""

    TIME_COSTS = {
        "help": 30,
        "chat": 5,
        "gift": 10,
        "conflict": 20,
    }

    def __init__(self, event_detector=None):
        self.event_detector = event_detector or EventDetector()

    def process(self, user_input):
        event = self.event_detector.detect(user_input)
        event_type = event.get("event_type", "")
        relation_change = {}

        if event_type == "help":
            relation_change = {"trust": 5}
        elif event_type == "chat":
            relation_change = {"familiarity": 1}
        elif event_type == "conflict":
            relation_change = {
                "trust": -event.get("value", 0)
            }

        return {
            "event": event,
            "time_cost": self.TIME_COSTS.get(event_type, 0),
            "relation_change": relation_change,
        }
