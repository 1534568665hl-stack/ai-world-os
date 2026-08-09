import unittest

from backend.core.player_action import PlayerActionProcessor


class PlayerActionProcessorTest(unittest.TestCase):

    def setUp(self):
        self.processor = PlayerActionProcessor()

    def test_help_action(self):
        result = self.processor.process("鎴戝府鍔╂搏娌慨鐞嗗挅鍟℃満")
        self.assertEqual(result["event"]["event_type"], "help")
        self.assertEqual(result["event"]["target"], "N_Momo")
        self.assertEqual(result["time_cost"], 30)
        self.assertEqual(result["relation_change"], {"trust": 5})

    def test_chat_gift_and_conflict_actions(self):
        chat = self.processor.process("浣犲ソ娌搏")
        self.assertEqual(chat["time_cost"], 5)
        self.assertEqual(chat["relation_change"], {"familiarity": 1})

        gift = self.processor.process("閫佺粰娌搏涓€浠界ぜ鐗?)
        self.assertEqual(gift["time_cost"], 10)
        self.assertEqual(gift["relation_change"], {})

        conflict = self.processor.process("鎴戝緢鐢熸皵")
        self.assertEqual(conflict["time_cost"], 20)
        self.assertEqual(conflict["relation_change"], {"trust": -5})

    def test_unmatched_input_has_no_cost_or_relation_change(self):
        result = self.processor.process("鎴戠湅鐪嬬獥澶?)
        self.assertEqual(result["event"]["event_type"], "")
        self.assertEqual(result["time_cost"], 0)
        self.assertEqual(result["relation_change"], {})
        print("PLAYER_ACTION_OK")


if __name__ == "__main__":
    unittest.main()
