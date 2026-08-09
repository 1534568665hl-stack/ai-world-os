import os
import unittest


class MainControllerIntegrationTest(unittest.TestCase):

    def test_main_uses_controller_and_runtime_response(self):
        main_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "main.py"
        )
        with open(os.path.abspath(main_path), "r", encoding="utf-8") as file:
            source = file.read()

        self.assertIn("WorldController", source)
        self.assertIn("RuntimeResponse", source)
        self.assertIn("world_controller.process", source)
        self.assertIn("runtime_response.to_dict", source)
        self.assertIn("llm_client.generate_response", source)
        print("MAIN_CONTROLLER_INTEGRATION_OK")


if __name__ == "__main__":
    unittest.main()
