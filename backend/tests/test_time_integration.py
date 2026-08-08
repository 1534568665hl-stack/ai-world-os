import os
import shutil
import tempfile
import unittest

from backend.core.context_builder import ContextBuilder
from backend.core.event_memory import EventMemoryManager
from backend.core.prompt_builder import PromptBuilder
from backend.core.time_manager import TimeManager


class TimeIntegrationTest(unittest.TestCase):

    def setUp(self):
        self.project_root = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.project_root)

    def test_time_context_flow(self):
        time_manager = TimeManager(self.project_root)
        time_manager.save({
            "world_time": "2026-08-07T11:55:00",
            "last_update": "2026-08-07T11:55:00",
        })

        startup_time = time_manager.load()
        self.assertEqual(
            startup_time["world_time"],
            "2026-08-07T11:55:00"
        )

        world_time = time_manager.advance(minutes=30)
        self.assertEqual(world_time["world_time"], "2026-08-07T12:25:00")

        context_builder = ContextBuilder()
        context_builder.event_memory_manager = EventMemoryManager(
            self.project_root
        )
        context = context_builder.build(
            {
                "message": "hello",
                "current_location": "L_Warm_Corner",
                "active_npc": [],
                "world_time": world_time,
            },
            {"location": [], "npc": [], "item": [], "rule": []}
        )

        self.assertEqual(
            context["runtime"]["world_time"],
            {
                "date": "2026-08-07",
                "time": "12:25:00",
                "period": "afternoon",
            }
        )

        prompt = PromptBuilder().build(context)
        self.assertIn("当前世界时间", prompt)
        self.assertIn("2026-08-07", prompt)
        self.assertIn("NPC行为必须符合当前世界时间", prompt)

        main_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "main.py"
        )
        repository_main_path = os.path.abspath(main_path)
        with open(repository_main_path, "r", encoding="utf-8") as file:
            main_source = file.read()
        self.assertIn("from backend.core.time_manager import TimeManager", main_source)
        self.assertIn("time_manager.advance", main_source)
        print("TIME_CONTEXT_OK")


if __name__ == "__main__":
    unittest.main()
