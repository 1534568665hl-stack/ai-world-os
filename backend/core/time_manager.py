import json
import os
from datetime import datetime, timedelta


class TimeManager:
    """Manage the independent world clock."""

    def __init__(self, project_root=None):
        self.project_root = project_root or os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../..")
        )
        self.time_file = os.path.join(
            self.project_root, "memory", "world_time.json"
        )

    def _now(self):
        return datetime.now().replace(microsecond=0)

    def _format_time(self, value):
        return value.isoformat(timespec="seconds")

    def _parse_time(self, value):
        if not value:
            return None

        for time_format in (
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
        ):
            try:
                return datetime.strptime(value, time_format)
            except ValueError:
                continue

        return None

    def _initialize(self):
        current = self._format_time(self._now())
        state = {
            "world_time": current,
            "last_update": current,
        }
        self.save(state)
        return state

    def load(self):
        if not os.path.exists(self.time_file):
            return self._initialize()

        try:
            with open(self.time_file, "r", encoding="utf-8") as file:
                state = json.load(file)
        except (OSError, ValueError):
            return self._initialize()

        if not isinstance(state, dict) or not self._parse_time(
            state.get("world_time", "")
        ):
            return self._initialize()

        return {
            "world_time": state["world_time"],
            "last_update": state.get("last_update", ""),
        }

    def save(self, state=None):
        if state is None:
            current = self._format_time(self._now())
            state = {
                "world_time": current,
                "last_update": current,
            }

        world_time = state.get("world_time", "")
        if not self._parse_time(world_time):
            world_time = self._format_time(self._now())

        saved_state = {
            "world_time": world_time,
            "last_update": state.get(
                "last_update",
                self._format_time(self._now())
            ),
        }

        os.makedirs(os.path.dirname(self.time_file), exist_ok=True)
        with open(self.time_file, "w", encoding="utf-8") as file:
            json.dump(saved_state, file, ensure_ascii=False, indent=2)

        return saved_state

    def _day_period(self, value):
        hour = value.hour
        if 5 <= hour < 12:
            return "morning"
        if 12 <= hour < 18:
            return "afternoon"
        return "night"

    def get_current_time(self):
        state = self.load()
        current = self._parse_time(state["world_time"])
        return {
            "world_time": state["world_time"],
            "day_period": self._day_period(current),
        }

    def advance(self, minutes=10):
        state = self.load()
        current = self._parse_time(state["world_time"])
        advanced = current + timedelta(minutes=minutes)
        self.save({
            "world_time": self._format_time(advanced),
            "last_update": self._format_time(self._now()),
        })
        return self.get_current_time()
