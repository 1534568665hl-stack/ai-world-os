import os
import shutil
import tempfile
import unittest

from backend.core.time_manager import TimeManager


class TimeManagerTest(unittest.TestCase):

    def setUp(self):
        self.project_root = tempfile.mkdtemp()
        self.manager = TimeManager(self.project_root)

    def tearDown(self):
        shutil.rmtree(self.project_root)

    def test_initialization(self):
        current = self.manager.get_current_time()
        self.assertTrue(current["world_time"])
        self.assertIn(
            current["day_period"],
            ("morning", "afternoon", "night")
        )
        self.assertTrue(os.path.exists(self.manager.time_file))

    def test_save_and_load(self):
        self.manager.save({
            "world_time": "2026-08-07T09:30:00",
            "last_update": "2026-08-07T09:30:00",
        })
        state = self.manager.load()
        self.assertEqual(state["world_time"], "2026-08-07T09:30:00")
        self.assertEqual(state["last_update"], "2026-08-07T09:30:00")

    def test_advance(self):
        self.manager.save({
            "world_time": "2026-08-07T11:55:00",
            "last_update": "2026-08-07T11:55:00",
        })
        current = self.manager.advance(minutes=10)
        self.assertEqual(current["world_time"], "2026-08-07T12:05:00")

    def test_day_period(self):
        cases = (
            ("2026-08-07T08:00:00", "morning"),
            ("2026-08-07T14:00:00", "afternoon"),
            ("2026-08-07T22:00:00", "night"),
        )
        for world_time, expected_period in cases:
            self.manager.save({
                "world_time": world_time,
                "last_update": world_time,
            })
            self.assertEqual(
                self.manager.get_current_time()["day_period"],
                expected_period
            )


if __name__ == "__main__":
    unittest.main()
