import json
import os
from datetime import datetime


class ScheduleManager:
    """Read NPC schedules and resolve their current runtime state."""

    def __init__(self, project_root=None):
        self.project_root = project_root or os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../..")
        )
        self.npc_dir = os.path.join(self.project_root, "world", "npc")

    def _read_json(self, path):
        try:
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (OSError, ValueError):
            return {}
        return data if isinstance(data, dict) else {}

    def _find_npc_dir(self, npc_id):
        if not os.path.isdir(self.npc_dir):
            return None

        for name in os.listdir(self.npc_dir):
            directory = os.path.join(self.npc_dir, name)
            if not os.path.isdir(directory):
                continue

            info = self._read_json(os.path.join(directory, "info.json"))
            if info.get("id", "").casefold() == npc_id.casefold():
                return directory
            if name.casefold() == npc_id.casefold():
                return directory

        return None

    def load_schedule(self, npc_id):
        """Load schedule entries for an NPC, or return an empty list."""
        npc_dir = self._find_npc_dir(npc_id)
        if not npc_dir:
            return []

        document = self._read_json(os.path.join(npc_dir, "schedule.json"))
        entries = document.get("schedule", document.get("activities", []))
        if not isinstance(entries, list):
            return []
        return [entry for entry in entries if isinstance(entry, dict)]

    def _parse_time(self, value):
        if isinstance(value, dict):
            value = value.get("world_time", value.get("time", ""))
        if isinstance(value, datetime):
            return value
        if not isinstance(value, str):
            return None

        for time_format in (
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
            "%H:%M",
            "%H:%M:%S",
        ):
            try:
                return datetime.strptime(value, time_format)
            except ValueError:
                continue
        return None

    def _minutes(self, value):
        parsed = self._parse_time(value)
        if not parsed:
            return None
        return parsed.hour * 60 + parsed.minute

    def _matches(self, current_minutes, entry):
        start = self._minutes(entry.get("start", "00:00"))
        end = self._minutes(entry.get("end", "23:59"))
        if start is None or end is None:
            return False

        if start <= end:
            return start <= current_minutes < end
        return current_minutes >= start or current_minutes < end

    def get_current_state(self, npc_id, world_time):
        """Return the active schedule state for an NPC."""
        parsed = self._parse_time(world_time)
        state = {
            "npc_id": npc_id,
            "activity": "",
            "location": "",
        }
        if not parsed:
            return state

        current_minutes = parsed.hour * 60 + parsed.minute
        for entry in self.load_schedule(npc_id):
            if self._matches(current_minutes, entry):
                state["activity"] = entry.get("activity", "")
                state["location"] = entry.get("location", "")
                break
        return state

    def get_current_activity(self, npc_id, world_time):
        return self.get_current_state(npc_id, world_time)["activity"]

    def get_current_location(self, npc_id, world_time):
        return self.get_current_state(npc_id, world_time)["location"]
