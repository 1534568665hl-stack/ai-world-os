import unittest
from unittest.mock import MagicMock

from backend.core.player_runtime import PlayerRuntime


class PlayerRuntimeTest(unittest.TestCase):

    def test_execute_coordinates_action_relation_and_world(self):
        action_processor = MagicMock()
        action_processor.process.return_value = {
            "event": {
                "event_type": "help",
                "target": "N_Momo",
                "value": 5,
            },
            "time_cost": 30,
            "relation_change": {"trust": 5},
        }

        relation_updater = MagicMock()
        relation_updater.update.return_value = {
            "npc": "N_Momo",
            "relationship": {"trust": 5},
        }

        world_runtime = MagicMock()
        world_runtime.advance.return_value = {
            "time": {"world_time": "2026-08-09T10:00:00"},
            "npc_states": [],
            "events": [
                {
                    "npc_id": "N_Momo",
                    "event_type": "daily",
                }
            ],
        }

        runtime = PlayerRuntime(
            player_action_processor=action_processor,
            relation_updater=relation_updater,
            world_runtime=world_runtime
        )
        result = runtime.execute("鎴戝府鍔╂搏娌慨鐞嗗挅鍟℃満")

        action_processor.process.assert_called_once_with(
            "鎴戝府鍔╂搏娌慨鐞嗗挅鍟℃満"
        )
        relation_updater.update.assert_called_once_with(
            "N_Momo",
            "help",
            5
        )
        world_runtime.advance.assert_called_once_with(30)
        self.assertEqual(result["action"]["time_cost"], 30)
        self.assertEqual(result["relation"]["npc"], "N_Momo")
        self.assertEqual(result["world"]["time"]["world_time"], "2026-08-09T10:00:00")
        self.assertEqual(result["events"][0]["event_type"], "daily")
        print("PLAYER_RUNTIME_OK")

    def test_action_without_target_skips_relation_update(self):
        action_processor = MagicMock()
        action_processor.process.return_value = {
            "event": {
                "event_type": "conflict",
                "target": "",
                "value": 5,
            },
            "time_cost": 20,
            "relation_change": {"trust": -5},
        }
        relation_updater = MagicMock()
        world_runtime = MagicMock()
        world_runtime.advance.return_value = {
            "time": {},
            "npc_states": [],
            "events": [],
        }

        runtime = PlayerRuntime(
            player_action_processor=action_processor,
            relation_updater=relation_updater,
            world_runtime=world_runtime
        )
        result = runtime.execute("鎴戝緢鐢熸皵")

        relation_updater.update.assert_not_called()
        world_runtime.advance.assert_called_once_with(20)
        self.assertEqual(result["relation"], {})
        self.assertEqual(result["events"], [])


if __name__ == "__main__":
    unittest.main()
