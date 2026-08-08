import unittest

from backend.core.event_detector import EventDetector


class EventDetectorTest(unittest.TestCase):

    def setUp(self):
        self.detector = EventDetector()

    def test_help_event_with_momo_target(self):
        event = self.detector.detect("我帮助沫沫修理咖啡机")
        self.assertEqual(event["event_type"], "help")
        self.assertEqual(event["target"], "N_Momo")
        self.assertEqual(event["value"], 5)
        self.assertEqual(event["source"], "player")

    def test_chat_event(self):
        event = self.detector.detect("你好沫沫")
        self.assertEqual(event["event_type"], "chat")
        self.assertEqual(event["target"], "N_Momo")
        self.assertEqual(event["value"], 1)

    def test_gift_event(self):
        event = self.detector.detect("送给沫沫一份礼物")
        self.assertEqual(event["event_type"], "gift")
        self.assertEqual(event["target"], "N_Momo")
        self.assertEqual(event["value"], 3)

    def test_conflict_event_without_target(self):
        event = self.detector.detect("我很生气")
        self.assertEqual(event["event_type"], "conflict")
        self.assertEqual(event["target"], "")
        self.assertEqual(event["value"], 5)

    def test_npc_aliases_are_normalized(self):
        for text in ("momo", "Momo", "MOMO", "N_Momo", "沫沫"):
            self.assertEqual(
                self.detector.detect("你好" + text)["target"],
                "N_Momo"
            )

    def test_unmatched_input_is_safe(self):
        event = self.detector.detect("我看着窗外")
        self.assertEqual(event["event_type"], "")
        self.assertEqual(event["target"], "")
        self.assertEqual(event["value"], 0)
        self.assertEqual(event["source"], "player")


if __name__ == "__main__":
    unittest.main()
