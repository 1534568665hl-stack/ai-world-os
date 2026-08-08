import json
import os
import shutil
import tempfile
import unittest

from backend.core.context_builder import ContextBuilder
from backend.core.prompt_builder import PromptBuilder
from backend.core.schedule_manager import ScheduleManager


class ScheduleManagerTest(unittest.TestCase):

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
                    },
                    {
                        "start": "18:00",
                        "end": "22:00",
                        "activity": "rest",
                        "location": "catnip_apt_302",
                    },
                ]
            }, file)

        self.manager = ScheduleManager(self.project_root)

    def tearDown(self):
        shutil.rmtree(self.project_root)

    def test_load_and_resolve_schedule(self):
        schedule = self.manager.load_schedule("N_Momo")
        self.assertEqual(len(schedule), 2)

        state = self.manager.get_current_state(
            "N_Momo",
            "2026-08-07T09:30:00"
        )
        self.assertEqual(state["activity"], "work")
        self.assertEqual(state["location"], "L_Warm_Corner")

    def test_evening_schedule(self):
        state = self.manager.get_current_state(
            "N_Momo",
            "2026-08-07T19:00:00"
        )
        self.assertEqual(state["activity"], "rest")
        self.assertEqual(state["location"], "catnip_apt_302")

    def test_context_builder_and_prompt_receive_npc_state(self):
        context_builder = ContextBuilder()
        context_builder.schedule_manager = self.manager
        context = context_builder.build(
            {
                "message": "hello",
                "current_location": "L_Warm_Corner",
                "active_npc": ["N_Momo"],
                "world_time": {
                    "world_time": "2026-08-07T09:30:00",
                    "day_period": "morning",
                },
            },
            {"location": [], "npc": [], "item": [], "rule": []}
        )

        self.assertEqual(context["npc_state"]["npc_id"], "N_Momo")
        self.assertEqual(context["npc_state"]["activity"], "work")
        self.assertEqual(context["npc_state"]["location"], "L_Warm_Corner")

        prompt = PromptBuilder().build(context)
        self.assertIn("NPC当前状态", prompt)
        self.assertIn("L_Warm_Corner", prompt)
        self.assertIn("NPC行为必须符合当前日程", prompt)
        print("SCHEDULE_MANAGER_OK")


if __name__ == "__main__":
    unittest.main()
