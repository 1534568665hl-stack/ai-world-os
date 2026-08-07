import copy
import json
import os


class RelationUpdater:
    """Persist runtime relationship state without changing world data."""

    DEFAULT_RELATIONSHIP = {
        "trust": 0,
        "familiarity": 0,
        "emotion": "neutral",
    }

    def __init__(self, project_root=None):
        self.project_root = project_root or os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../..")
        )
        self.relations_dir = os.path.join(
            self.project_root, "memory", "relations"
        )

    def _path(self, npc_id, player_id="player"):
        filename = "{}_{}.json".format(player_id, npc_id)
        return os.path.join(self.relations_dir, filename)

    def _read(self, path):
        try:
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (OSError, ValueError):
            return {}

        if not isinstance(data, dict):
            return {}
        return data

    def load_runtime_relation(self, npc_id, player_id="player"):
        """Return saved runtime data, or an empty dict when it is absent."""
        return self._read(self._path(npc_id, player_id))

    def load(self, npc_id, player_id="player"):
        """Return a normalized runtime relation with neutral defaults."""
        data = self.load_runtime_relation(npc_id, player_id)
        relationship = copy.deepcopy(self.DEFAULT_RELATIONSHIP)
        relationship.update(data.get("relationship", {}))

        return {
            "npc": data.get("npc", npc_id),
            "player": data.get("player", player_id),
            "relationship": relationship,
        }

    def _apply_event(self, relationship, event_type, value):
        if event_type == "help":
            relationship["trust"] += value
            relationship["familiarity"] += 2
        elif event_type == "chat":
            relationship["familiarity"] += 1
        elif event_type == "gift":
            relationship["trust"] += value
        elif event_type == "conflict":
            relationship["trust"] -= abs(value)

    def _update_emotion(self, relationship):
        trust = relationship["trust"]
        if trust > 0:
            relationship["emotion"] = "positive"
        elif trust < 0:
            relationship["emotion"] = "negative"
        else:
            relationship["emotion"] = "neutral"

    def update(self, npc_id, event_type, value, player_id="player"):
        """Apply one event and save the resulting player/NPC relation."""
        relation = self.load(npc_id, player_id)
        relationship = relation["relationship"]
        self._apply_event(relationship, event_type, value)
        self._update_emotion(relationship)

        relation["npc"] = npc_id
        relation["player"] = player_id
        os.makedirs(self.relations_dir, exist_ok=True)
        with open(self._path(npc_id, player_id), "w", encoding="utf-8") as file:
            json.dump(relation, file, ensure_ascii=False, indent=2)

        return relation
