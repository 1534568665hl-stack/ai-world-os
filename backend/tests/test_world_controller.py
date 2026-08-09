import unittest
from unittest.mock import MagicMock

from backend.core.world_controller import WorldController


class WorldControllerTest(unittest.TestCase):

    def test_process_coordinates_player_to_prompt(self):
        player_runtime = MagicMock()
        player_runtime.process.return_value = {
            "action": {
                "event": {"event_type": "help"},
                "time_cost": 30,
            },
            "relation": {"relationship": {"trust": 5}},
            "world": {
                "time": {
                    "world_time": "2026-08-09T10:00:00",
                    "day_period": "morning",
                },
                "npc_states": [
                    {
                        "npc_id": "N_Momo",
                        "location": "L_Warm_Corner",
                        "activity": "work",
                    }
                ],
            },
            "events": [],
        }

        context_builder = MagicMock()
        context_builder.build.return_value = {
            "runtime": {"current_location": "L_Warm_Corner"}
        }
        prompt_builder = MagicMock()
        prompt_builder.build.return_value = "鏈€缁?Prompt"

        controller = WorldController(
            player_runtime=player_runtime,
            context_builder=context_builder,
            prompt_builder=prompt_builder
        )
        result = controller.process("鎴戝府鍔╂搏娌慨鐞嗗挅鍟℃満")

        player_runtime.process.assert_called_once_with(
            "鎴戝府鍔╂搏娌慨鐞嗗挅鍟℃満"
        )
        context_builder.build.assert_called_once()
        prompt_builder.build.assert_called_once_with(
            context_builder.build.return_value
        )
        self.assertEqual(result["player_result"]["action"]["time_cost"], 30)
        self.assertEqual(
            result["context"]["runtime"]["current_location"],
            "L_Warm_Corner"
        )
        self.assertEqual(result["prompt"], "鏈€缁?Prompt")
        print("WORLD_CONTROLLER_OK")


if __name__ == "__main__":
    unittest.main()
