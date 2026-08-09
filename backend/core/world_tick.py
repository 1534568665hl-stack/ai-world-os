from backend.core.npc_event_generator import NPCEventGenerator
from backend.core.npc_state_manager import NPCStateManager
from backend.core.time_manager import TimeManager
from backend.core.world_event_manager import WorldEventManager


class WorldTickEngine:
    """Coordinate one deterministic world-time tick."""

    def __init__(
        self,
        npc_ids=None,
        time_manager=None,
        npc_state_manager=None,
        npc_event_generator=None,
        world_event_manager=None
    ):
        self.npc_ids = list(npc_ids or [])
        self.time_manager = time_manager or TimeManager()
        self.npc_state_manager = (
            npc_state_manager or NPCStateManager()
        )
        self.npc_event_generator = (
            npc_event_generator or NPCEventGenerator()
        )
        self.world_event_manager = (
            world_event_manager or WorldEventManager()
        )

    def tick(self, minutes=10):
        """Advance time, refresh NPC states, and persist new daily events."""
        self.time_manager.advance(minutes)
        current_time = self.time_manager.get_current_time()

        npc_states = self.npc_state_manager.get_states(
            self.npc_ids,
            current_time
        )
        generated_events = self.npc_event_generator.generate(
            npc_states,
            current_time
        )

        saved_events = []
        for event in generated_events:
            saved_event = self.world_event_manager.save_event(event)
            if saved_event is not None:
                saved_events.append(saved_event)

        return {
            "time": current_time,
            "npc_states": npc_states,
            "events": saved_events,
        }
