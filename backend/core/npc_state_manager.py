from datetime import datetime

from backend.core.schedule_manager import ScheduleManager
from backend.core.time_manager import TimeManager


class NPCStateManager:
    """Build runtime NPC state from world time and schedule data."""

    def __init__(self, time_manager=None, schedule_manager=None):
        self.time_manager = time_manager or TimeManager()
        self.schedule_manager = schedule_manager or ScheduleManager()

    def get_state(self, npc_id, world_time=None):
        """Return the current runtime state for one NPC."""
        current_time = world_time
        if current_time is None or current_time == "":
            current_time = self.time_manager.get_current_time()

        schedule_state = self.schedule_manager.get_current_state(
            npc_id,
            current_time
        )

        return {
            "npc_id": npc_id,
            "location": schedule_state.get("location", ""),
            "activity": schedule_state.get("activity", ""),
            "updated_at": datetime.now().isoformat(),
        }

    def get_states(self, npc_ids, world_time=None):
        """Return runtime states for all supplied NPC IDs."""
        return [
            self.get_state(npc_id, world_time)
            for npc_id in (npc_ids or [])
        ]
