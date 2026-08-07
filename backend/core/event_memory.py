import json
import os
from datetime import datetime


class EventMemoryManager:
    """Persist world events in the runtime memory directory."""

    DESCRIPTIONS = {
        "help": "玩家帮助 NPC",
        "chat": "玩家与 NPC 交流",
        "gift": "玩家赠送物品",
        "conflict": "玩家与 NPC 发生冲突",
    }

    def __init__(self, project_root=None):
        self.project_root = project_root or os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../..")
        )
        self.events_dir = os.path.join(
            self.project_root, "memory", "events"
        )
        self.events_file = os.path.join(
            self.events_dir, "current.json"
        )

    def load_events(self):
        if not os.path.exists(self.events_file):
            return []

        try:
            with open(self.events_file, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (OSError, ValueError):
            return []

        events = data.get("events", []) if isinstance(data, dict) else []
        return events if isinstance(events, list) else []

    def save_event(self, event):
        event = event or {}
        event_record = {
            "time": event.get("time") or datetime.now().isoformat(),
            "event_type": event.get("event_type", ""),
            "actor": event.get("actor", event.get("source", "player")),
            "target": event.get("target", ""),
            "value": event.get("value", 0),
            "description": event.get(
                "description",
                self.DESCRIPTIONS.get(
                    event.get("event_type", ""),
                    "玩家发生了一次世界事件"
                )
            ),
        }

        events = self.load_events()
        events.append(event_record)
        os.makedirs(self.events_dir, exist_ok=True)

        with open(self.events_file, "w", encoding="utf-8") as file:
            json.dump(
                {"events": events},
                file,
                ensure_ascii=False,
                indent=2
            )

        return event_record

    def get_recent_events(self, limit=10):
        if limit <= 0:
            return []
        return self.load_events()[-limit:]
