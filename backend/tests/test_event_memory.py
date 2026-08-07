import os
import shutil
import tempfile
import unittest

from backend.core.context_builder import ContextBuilder
from backend.core.event_memory import EventMemoryManager


class EventMemoryManagerTest(unittest.TestCase):

    def setUp(self):
        self.project_root = tempfile.mkdtemp()
        self.manager = EventMemoryManager(self.project_root)

    def tearDown(self):
        shutil.rmtree(self.project_root)

    def test_save_event_successfully(self):
        event = self.manager.save_event({
            "event_type": "help",
            "target": "N_Momo",
            "value": 5,
            "source": "player",
        })

        self.assertEqual(event["event_type"], "help")
        self.assertEqual(event["description"], "玩家帮助 NPC")
        self.assertTrue(os.path.exists(self.manager.events_file))

    def test_load_events_successfully(self):
        self.manager.save_event({"event_type": "chat"})
        events = self.manager.load_events()
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["event_type"], "chat")

    def test_get_recent_events_limits_count(self):
        for index in range(12):
            self.manager.save_event({
                "event_type": "chat",
                "value": index,
            })

        events = self.manager.get_recent_events(10)
        self.assertEqual(len(events), 10)
        self.assertEqual(events[0]["value"], 2)
        self.assertEqual(events[-1]["value"], 11)

    def test_context_builder_reads_recent_events(self):
        self.manager.save_event({
            "event_type": "help",
            "target": "N_Momo",
            "value": 5,
        })

        context_builder = ContextBuilder()
        context_builder.event_memory_manager = self.manager
        context = context_builder.build(
            {
                "current_location": "",
                "active_npc": [],
                "message": "hello",
            },
            {"location": [], "npc": [], "item": [], "rule": []}
        )

        self.assertEqual(len(context["events"]), 1)
        self.assertEqual(context["events"][0]["event_type"], "help")


if __name__ == "__main__":
    unittest.main()
