import json
import os
import shutil
import tempfile
import unittest

from backend.core.npc_event_generator import NPCEventGenerator
from backend.core.npc_state_manager import NPCStateManager
from backend.core.schedule_manager import ScheduleManager
from backend.core.time_manager import TimeManager


class NPCEventGeneratorTest(unittest.TestCase):

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
                        "start": "08:00",
                        "end": "12:00",
                        "activity": "work",
                        "location": "L_Warm_Corner",
                    }
                ]
            }, file)

        self.time_manager = TimeManager(self.project_root)
        self.time_manager.save({
            "world_time": "2026-08-09T09:30:00",
            "last_update": "2026-08-09T09:30:00",
        })
        self.schedule_manager = ScheduleManager(self.project_root)
        self.npc_state_manager = NPCStateManager(
            time_manager=self.time_manager,
            schedule_manager=self.schedule_manager
        )
        self.generator = NPCEventGenerator()

    def tearDown(self):
        shutil.rmtree(self.project_root)

    def test_generates_daily_event_from_runtime_state(self):
        world_time = self.time_manager.get_current_time()
        npc_states = self.npc_state_manager.get_states(
            ["N_Momo"],
            world_time
        )

        events = self.generator.generate(npc_states, world_time)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["npc_id"], "N_Momo")
        self.assertEqual(events[0]["event_type"], "daily")
        self.assertEqual(events[0]["activity"], "work")
        self.assertEqual(events[0]["location"], "L_Warm_Corner")
        self.assertEqual(events[0]["description"], "娌搏姝ｅ湪鍜栧暋搴楀伐浣?)

    def test_does_not_generate_duplicate_event(self):
        state = {
            "npc_id": "N_Momo",
            "activity": "work",
            "location": "L_Warm_Corner",
        }

        self.assertIsNotNone(self.generator.generate_event(state))
        self.assertIsNone(self.generator.generate_event(state))

        changed_state = dict(state)
        changed_state["activity"] = "rest"
        changed_state["location"] = "catnip_apt_302"
        self.assertIsNotNone(self.generator.generate_event(changed_state))

    def test_empty_runtime_state_is_ignored(self):
        self.assertEqual(
            self.generator.generate([
                {
                    "npc_id": "N_Momo",
                    "activity": "",
                    "location": "",
                }
            ]),
            []
        )
        print("NPC_EVENT_GENERATOR_OK")


if __name__ == "__main__":
    unittest.main()
