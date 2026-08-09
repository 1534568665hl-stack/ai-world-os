import unittest

from backend.core.runtime_response import RuntimeResponse


class RuntimeResponseTest(unittest.TestCase):

    def test_to_dict_returns_unified_response(self):
        player_result = {
            "action": {"time_cost": 30},
            "relation": {"trust": 5},
            "world": {},
            "events": [],
        }
        context = {"runtime": {"active_npc": ["N_Momo"]}}
        prompt = "鏈€缁?Prompt"

        response = RuntimeResponse(
            player_result,
            context,
            prompt
        )

        self.assertEqual(
            response.to_dict(),
            {
                "player_result": player_result,
                "context": context,
                "prompt": prompt,
            }
        )
        print("RUNTIME_RESPONSE_OK")


if __name__ == "__main__":
    unittest.main()
