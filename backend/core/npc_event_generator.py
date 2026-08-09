class NPCEventGenerator:
    """Generate deterministic daily events from NPC runtime states."""

    NPC_NAMES = {
        "N_Momo": "娌搏",
    }

    LOCATION_NAMES = {
        "L_Warm_Corner": "鍜栧暋搴?,
    }

    ACTIVITY_TEXT = {
        "work": "姝ｅ湪{location}宸ヤ綔",
        "rest": "姝ｅ湪{location}浼戞伅",
        "sleep": "姝ｅ湪{location}鐫¤",
        "eat": "姝ｅ湪{location}鐢ㄩ",
        "shop": "姝ｅ湪{location}璐墿",
    }

    def __init__(self):
        self._last_signatures = {}

    def _world_time_value(self, world_time):
        if isinstance(world_time, dict):
            return world_time.get("world_time", "")
        return world_time or ""

    def _date_key(self, world_time):
        value = self._world_time_value(world_time)
        if isinstance(value, str):
            return value[:10]
        return ""

    def _signature(self, state, world_time):
        return (
            state.get("npc_id", ""),
            state.get("activity", ""),
            state.get("location", ""),
            self._date_key(world_time),
        )

    def _description(self, state):
        npc_id = state.get("npc_id", "")
        activity = state.get("activity", "")
        location_id = state.get("location", "")
        npc_name = self.NPC_NAMES.get(npc_id, npc_id)
        location_name = self.LOCATION_NAMES.get(
            location_id,
            location_id
        )
        template = self.ACTIVITY_TEXT.get(
            activity,
            "姝ｅ湪{location}{activity}"
        )
        return npc_name + template.format(
            location=location_name,
            activity=activity
        )

    def generate_event(self, npc_state, world_time=None):
        """Generate one daily event, or return None for empty/duplicate state."""
        state = npc_state or {}
        npc_id = state.get("npc_id", "")
        activity = state.get("activity", "")
        location = state.get("location", "")
        if not npc_id or not activity or not location:
            return None

        signature = self._signature(state, world_time)
        if self._last_signatures.get(npc_id) == signature:
            return None

        self._last_signatures[npc_id] = signature
        return {
            "npc_id": npc_id,
            "event_type": "daily",
            "activity": activity,
            "location": location,
            "description": self._description(state),
        }

    def generate(self, npc_states, world_time=None):
        """Generate non-duplicate daily events for all NPC runtime states."""
        events = []
        for npc_state in npc_states or []:
            event = self.generate_event(npc_state, world_time)
            if event:
                events.append(event)
        return events
