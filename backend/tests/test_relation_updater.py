import json
import os
import shutil
import tempfile
import unittest

from backend.core.context_builder import ContextBuilder
from backend.core.relation_manager import RelationManager
from backend.core.relation_updater import RelationUpdater


class RelationUpdaterTest(unittest.TestCase):

    def setUp(self):
        self.project_root = tempfile.mkdtemp()
        self.updater = RelationUpdater(self.project_root)

    def tearDown(self):
        shutil.rmtree(self.project_root)

    def test_initial_relation(self):
        relation = self.updater.load("N_Momo")
        self.assertEqual(relation["npc"], "N_Momo")
        self.assertEqual(relation["relationship"]["trust"], 0)
        self.assertEqual(relation["relationship"]["emotion"], "neutral")

    def test_update_increases_trust(self):
        relation = self.updater.update("N_Momo", "help", 5)
        self.assertEqual(relation["relationship"]["trust"], 5)
        self.assertEqual(relation["relationship"]["familiarity"], 2)
        self.assertEqual(relation["relationship"]["emotion"], "positive")

    def test_relation_file_is_saved(self):
        self.updater.update("N_Momo", "help", 5)
        path = os.path.join(
            self.project_root,
            "memory",
            "relations",
            "player_N_Momo.json"
        )
        self.assertTrue(os.path.exists(path))
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
        self.assertEqual(data["npc"], "N_Momo")
        self.assertEqual(data["relationship"]["trust"], 5)

    def test_context_prefers_runtime_relation(self):
        self.updater.update("N_Momo", "help", 5)
        context_builder = ContextBuilder()
        context_builder.relation_updater = RelationUpdater(self.project_root)
        context_builder.relation_manager = RelationManager(self.project_root)

        context = context_builder.build(
            {
                "current_location": "L_Warm_Corner",
                "active_npc": ["N_Momo"],
                "message": "hello",
            },
            {"location": [], "npc": [], "item": [], "rule": []}
        )

        self.assertEqual(context["relations"]["npc"], "N_Momo")
        self.assertEqual(
            context["relations"]["relationship"]["trust"],
            5
        )


if __name__ == "__main__":
    unittest.main()
