import os
import shutil
import tempfile
import unittest
from unittest.mock import patch

from backend.core.system_check import SystemCheck


class SystemCheckTest(unittest.TestCase):

    def setUp(self):
        self.project_root = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.project_root, "world"))

    def tearDown(self):
        shutil.rmtree(self.project_root)

    def test_system_check_returns_ok(self):
        with patch.dict(
            os.environ,
            {"OPENAI_API_KEY": "test-key"},
            clear=False
        ):
            result = SystemCheck(self.project_root).run()

        self.assertEqual(result["status"], "ok")
        self.assertEqual(
            result["checks"],
            {
                "world": True,
                "memory": True,
                "llm": True,
                "imports": True,
            }
        )
        self.assertTrue(os.path.isdir(os.path.join(self.project_root, "memory")))
        print("SYSTEM_CHECK_OK")

    def test_missing_world_or_llm_config_fails(self):
        missing_world_root = tempfile.mkdtemp()
        try:
            with patch.dict(os.environ, {"OPENAI_API_KEY": ""}, clear=False):
                result = SystemCheck(missing_world_root).run()
            self.assertEqual(result["status"], "error")
            self.assertFalse(result["checks"]["world"])
            self.assertFalse(result["checks"]["llm"])
        finally:
            shutil.rmtree(missing_world_root)


if __name__ == "__main__":
    unittest.main()
