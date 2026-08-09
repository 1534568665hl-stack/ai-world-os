from backend.core.time_manager import TimeManager
from backend.core.world_event_manager import WorldEventManager
from backend.core.world_tick import WorldTickEngine


class WorldRuntime:
    """Small facade for advancing the existing world runtime pipeline."""

    def __init__(
        self,
        npc_ids=None,
        time_manager=None,
        world_tick_engine=None,
        world_event_manager=None
    ):
        self.time_manager = time_manager or TimeManager()
        self.world_event_manager = (
            world_event_manager or WorldEventManager()
        )
        self.world_tick_engine = world_tick_engine or WorldTickEngine(
            npc_ids=npc_ids,
            time_manager=self.time_manager,
            world_event_manager=self.world_event_manager
        )

    def advance(self, minutes=10):
        """Advance the world through the existing tick engine."""
        result = self.world_tick_engine.tick(minutes)
        return {
            "time": result.get("time", {}),
            "events": result.get("events", []),
            "npc_states": result.get("npc_states", []),
        }
