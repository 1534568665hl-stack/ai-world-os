from backend.core.context_builder import ContextBuilder
from backend.core.player_runtime import PlayerRuntime
from backend.core.prompt_builder import PromptBuilder


class WorldController:
    """Coordinate player execution, context construction, and prompt rendering."""

    def __init__(
        self,
        player_runtime=None,
        context_builder=None,
        prompt_builder=None
    ):
        self.player_runtime = player_runtime or PlayerRuntime()
        self.context_builder = context_builder or ContextBuilder()
        self.prompt_builder = prompt_builder or PromptBuilder()

    def _run_player_runtime(self, user_input):
        process = getattr(self.player_runtime, "process", None)
        if callable(process):
            return process(user_input)
        return self.player_runtime.execute(user_input)

    def _build_user_context(self, user_input, player_result):
        world = player_result.get("world", {})
        world_time = world.get("time", {})
        npc_states = world.get("npc_states", [])
        active_npc = [
            state.get("npc_id", "")
            for state in npc_states
            if state.get("npc_id", "")
        ]
        current_location = ""
        for state in npc_states:
            if state.get("location", ""):
                current_location = state["location"]
                break

        return {
            "message": user_input,
            "time": world_time.get("world_time", "")
            if isinstance(world_time, dict) else world_time,
            "world_time": world_time,
            "current_location": current_location,
            "active_npc": active_npc,
        }

    def process(self, user_input):
        """Run the player-to-prompt pipeline and return all intermediate results."""
        player_result = self._run_player_runtime(user_input)
        user_context = self._build_user_context(
            user_input,
            player_result
        )
        retrieved_data = {
            "location": [],
            "npc": [],
            "item": [],
            "rule": [],
        }
        context = self.context_builder.build(
            user_context=user_context,
            retrieved_data=retrieved_data
        )
        prompt = self.prompt_builder.build(context)

        return {
            "player_result": player_result,
            "context": context,
            "prompt": prompt,
        }
