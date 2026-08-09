import json
import os
import shutil
import tempfile
import unittest

from backend.core.world_event_manager import WorldEventManager


class WorldEventManagerTest(unittest.TestCase):

    def setUp(self):
        self.project_root = tempfile.mkdtemp()
        self.manager = WorldEventManager(self.project_root)
        self.event = {
            "npc_id": "N_Momo",
            "event_type": "daily",
            "activity": "work",
            "location": "L_Warm_Corner",
            "description": "娌搏姝ｅ湪鍜栧暋搴楀伐浣?,
            "date": "2026-08-09",
        }

    def tearDown(self):
        shutil.rmtree(self.project_root)

    def test_save_and_load_events(self):
        saved = self.manager.save_event(self.event)
        self.assertIsNotNone(saved)
        self.assertTrue(os.path.exists(self.manager.events_file))

        events = self.manager.load_events()
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["npc_id"], "N_Momo")
        self.assertEqual(events[0]["date"], "2026-08-09")

    def test_duplicate_event_is_not_saved(self):
        self.assertIsNotNone(self.manager.save_event(self.event))
        self.assertIsNone(self.manager.save_event(dict(self.event)))
        self.assertEqual(len(self.manager.load_events()), 1)

        next_day = dict(self.event)
        next_day["date"] = "2026-08-10"
        self.assertIsNotNone(self.manager.save_event(next_day))
        self.assertEqual(len(self.manager.load_events()), 2)

    def test_recent_events_limit(self):
        for index in range(12):
            event = dict(self.event)
            event["date"] = "2026-08-{:02d}".format(index + 1)
            self.manager.save_event(event)

        recent = self.manager.get_recent_events(10)
        self.assertEqual(len(recent), 10)
        self.assertEqual(recent[0]["date"], "2026-08-03")
        self.assertEqual(recent[-1]["date"], "2026-08-12")
        self.assertEqual(self.manager.get_recent_events(0), [])
        print("WORLD_EVENT_MANAGER_OK")


if __name__ == "__main__":
    unittest.main()
