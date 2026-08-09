import json
import os
import shutil
import tempfile
import unittest

from backend.core.npc_event_generator import NPCEventGenerator
from backend.core.npc_state_manager import NPCStateManager
from backend.core.schedule_manager import ScheduleManager
from backend.core.time_manager import TimeManager
from backend.core.world_event_manager import WorldEventManager
from backend.core.world_tick import WorldTickEngine


class WorldTickEngineTest(unittest.TestCase):

    def setUp(self):
        self.project_root = tempfile.mkdtemp()
        npc_dir = os.path.join(self.project_root, "world", "npc", "momo")
        os.makedirs(npc_dir)

        with open(os.path.join(npc_dir, "info.json"), "w", encoding="utf-8") as file:
            json.dump({"id": "N_Momo"}, file)

        with open(os.path.join(npc_dir, "schedule.json"), "w", encoding="utf-8") as file:
            json.dump({
                "schedule": [
                    {
                        "start": "10:00",
                        "end": "12:00",
                        "activity": "work",
                        "location": "L_Warm_Corner",
                    }
                ]
            }, file)

        self.time_manager = TimeManager(self.project_root)
        self.time_manager.save({
            "world_time": "2026-08-09T09:50:00",
            "last_update": "2026-08-09T09:50:00",
        })
        self.schedule_manager = ScheduleManager(self.project_root)
        self.npc_state_manager = NPCStateManager(
            time_manager=self.time_manager,
            schedule_manager=self.schedule_manager
        )
        self.world_event_manager = WorldEventManager(self.project_root)
        self.engine = WorldTickEngine(
            npc_ids=["N_Momo"],
            time_manager=self.time_manager,
            npc_state_manager=self.npc_state_manager,
            npc_event_generator=NPCEventGenerator(),
            world_event_manager=self.world_event_manager
        )

    def tearDown(self):
        shutil.rmtree(self.project_root)

    def test_tick_coordinates_world_update(self):
        result = self.engine.tick(minutes=10)

        self.assertEqual(
            result["time"]["world_time"],
            "2026-08-09T10:00:00"
        )
        self.assertEqual(result["npc_states"][0]["npc_id"], "N_Momo")
        self.assertEqual(result["npc_states"][0]["activity"], "work")
        self.assertEqual(result["events"][0]["event_type"], "daily")
        self.assertEqual(
            result["events"][0]["description"],
            "娌搏姝ｅ湪鍜栧暋搴楀伐浣?
        )
        self.assertEqual(len(self.world_event_manager.load_events()), 1)

    def test_same_state_does_not_save_duplicate_event(self):
        first = self.engine.tick(minutes=10)
        second = self.engine.tick(minutes=10)

        self.assertEqual(len(first["events"]), 1)
        self.assertEqual(second["events"], [])
        self.assertEqual(len(self.world_event_manager.load_events()), 1)
        print("WORLD_TICK_OK")


if __name__ == "__main__":
    unittest.main()
