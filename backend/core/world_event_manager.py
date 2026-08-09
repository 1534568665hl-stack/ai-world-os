import copy
import json
import os
from datetime import datetime


class WorldEventManager:
    """Persist autonomous NPC world events without changing other event data."""

    def __init__(self, project_root=None):
        self.project_root = project_root or os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../..")
        )
        self.events_dir = os.path.join(
            self.project_root,
            "memory",
            "events"
        )
        self.events_file = os.path.join(
            self.events_dir,
            "world_events.json"
        )

    def _read_date(self, event):
        date = event.get("date", "")
        if isinstance(date, str) and date:
            return date[:10]

        for key in ("time", "world_time"):
            value = event.get(key, "")
            if isinstance(value, dict):
                value = value.get("world_time", value.get("date", ""))
            if isinstance(value, str) and value:
                return value[:10]

        return datetime.now().strftime("%Y-%m-%d")

    def _signature(self, event):
        return (
            event.get("npc_id", ""),
            event.get("event_type", ""),
            event.get("activity", ""),
            event.get("location", ""),
            event.get("date", ""),
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
        """Save one event, returning None when the same event already exists."""
        if not isinstance(event, dict):
            return None

        event_record = copy.deepcopy(event)
        event_record["date"] = self._read_date(event_record)
        signature = self._signature(event_record)

        events = self.load_events()
        if any(self._signature(saved) == signature for saved in events):
            return None

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
