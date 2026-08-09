from backend.core.player_action import PlayerActionProcessor
from backend.core.relation_updater import RelationUpdater
from backend.core.world_runtime import WorldRuntime


class PlayerRuntime:
    """Coordinate one complete player action execution."""

    def __init__(
        self,
        player_action_processor=None,
        relation_updater=None,
        world_runtime=None
    ):
        self.player_action_processor = (
            player_action_processor or PlayerActionProcessor()
        )
        self.relation_updater = relation_updater or RelationUpdater()
        self.world_runtime = world_runtime or WorldRuntime()

    def execute(self, user_input):
        """Process action, update relation, advance world, and return results."""
        action = self.player_action_processor.process(user_input)
        event = action.get("event", {})
        event_type = event.get("event_type", "")
        target = event.get("target", "")

        relation = {}
        if event_type and target:
            relation = self.relation_updater.update(
                target,
                event_type,
                event.get("value", 0)
            )

        world = self.world_runtime.advance(
            action.get("time_cost", 0)
        )

        return {
            "action": action,
            "relation": relation,
            "world": world,
            "events": world.get("events", []),
        }
