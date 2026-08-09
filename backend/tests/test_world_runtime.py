import unittest
from unittest.mock import MagicMock

from backend.core.world_runtime import WorldRuntime


class WorldRuntimeTest(unittest.TestCase):

    def test_advance_wraps_world_tick(self):
        time_manager = MagicMock()
        world_event_manager = MagicMock()
        world_tick_engine = MagicMock()
        world_tick_engine.tick.return_value = {
            "time": {
                "world_time": "2026-08-09T10:00:00",
                "day_period": "morning",
            },
            "events": [
                {
                    "npc_id": "N_Momo",
                    "event_type": "daily",
                }
            ],
            "npc_states": [
                {
                    "npc_id": "N_Momo",
                    "activity": "work",
                    "location": "L_Warm_Corner",
                }
            ],
        }

        runtime = WorldRuntime(
            time_manager=time_manager,
            world_tick_engine=world_tick_engine,
            world_event_manager=world_event_manager
        )
        result = runtime.advance(minutes=20)

        world_tick_engine.tick.assert_called_once_with(20)
        self.assertEqual(
            result["time"]["world_time"],
            "2026-08-09T10:00:00"
        )
        self.assertEqual(result["events"][0]["event_type"], "daily")
        self.assertEqual(result["npc_states"][0]["npc_id"], "N_Momo")
        print("WORLD_RUNTIME_OK")


if __name__ == "__main__":
    unittest.main()
