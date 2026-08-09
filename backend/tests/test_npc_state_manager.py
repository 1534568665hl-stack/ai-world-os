import json
import os
import shutil
import tempfile
import unittest

from backend.core.context_builder import ContextBuilder
from backend.core.npc_state_manager import NPCStateManager
from backend.core.prompt_builder import PromptBuilder
from backend.core.schedule_manager import ScheduleManager
from backend.core.time_manager import TimeManager


class NPCStateManagerTest(unittest.TestCase):

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
            "world_time": "2026-08-07T09:30:00",
            "last_update": "2026-08-07T09:30:00",
        })
        self.schedule_manager = ScheduleManager(self.project_root)
        self.manager = NPCStateManager(
            time_manager=self.time_manager,
            schedule_manager=self.schedule_manager
        )

    def tearDown(self):
        shutil.rmtree(self.project_root)

    def test_runtime_state_uses_time_and_schedule(self):
        state = self.manager.get_state("N_Momo")
        self.assertEqual(state["npc_id"], "N_Momo")
        self.assertEqual(state["location"], "L_Warm_Corner")
        self.assertEqual(state["activity"], "work")
        self.assertTrue(state["updated_at"])

    def test_context_contains_npc_states(self):
        context_builder = ContextBuilder()
        context_builder.schedule_manager = self.schedule_manager
        context_builder.npc_state_manager = self.manager

        context = context_builder.build(
            {
                "message": "hello",
                "current_location": "L_Warm_Corner",
                "active_npc": ["N_Momo"],
                "world_time": self.time_manager.get_current_time(),
            },
            {"location": [], "npc": [], "item": [], "rule": []}
        )

        self.assertEqual(len(context["npc_states"]), 1)
        self.assertEqual(context["npc_states"][0]["activity"], "work")

    def test_prompt_contains_runtime_state(self):
        context_builder = ContextBuilder()
        context_builder.schedule_manager = self.schedule_manager
        context_builder.npc_state_manager = self.manager
        context = context_builder.build(
            {
                "message": "hello",
                "current_location": "L_Warm_Corner",
                "active_npc": ["N_Momo"],
                "world_time": self.time_manager.get_current_time(),
            },
            {"location": [], "npc": [], "item": [], "rule": []}
        )

        prompt = PromptBuilder().build(context)
        self.assertIn("NPC瀹炴椂鐘舵€?, prompt)
        self.assertIn("L_Warm_Corner", prompt)
        self.assertIn("work", prompt)
        print("NPC_STATE_OK")


if __name__ == "__main__":
    unittest.main()
