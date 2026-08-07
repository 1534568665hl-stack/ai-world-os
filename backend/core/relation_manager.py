import copy
import json
import os


class RelationManager:
    """Load location and NPC relationship data from the world directory."""

    DEFAULT_RELATIONSHIP = {
        "trust": 0,
        "familiarity": 0,
        "emotion": "neutral",
    }

    def __init__(self, project_root=None):
        self.project_root = project_root or os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../..")
        )
        self.location_dir = os.path.join(
            self.project_root, "world", "location"
        )
        self.npc_dir = os.path.join(self.project_root, "world", "npc")

    def _read_json(self, path):
        try:
            with open(path, "r", encoding="utf-8") as file:
                return json.load(file)
        except (OSError, json.JSONDecodeError):
            return {}

    def _find_location_dir(self, location_id):
        if not os.path.isdir(self.location_dir):
            return None

        for name in os.listdir(self.location_dir):
            directory = os.path.join(self.location_dir, name)
            info = self._read_json(os.path.join(directory, "info.json"))
            if info.get("id") == location_id:
                return directory

        return None

    def _npc_aliases(self):
        aliases = {}
        if not os.path.isdir(self.npc_dir):
            return aliases

        for name in os.listdir(self.npc_dir):
            directory = os.path.join(self.npc_dir, name)
            info = self._read_json(os.path.join(directory, "info.json"))
            entity_id = info.get("id")
            if not entity_id:
                continue

            aliases[name.casefold()] = entity_id
            aliases[entity_id.casefold()] = entity_id
            if info.get("name"):
                aliases[info["name"].casefold()] = entity_id

        return aliases

    def _canonical_npc_id(self, npc_id):
        if not isinstance(npc_id, str):
            return npc_id

        aliases = self._npc_aliases()
        canonical = aliases.get(npc_id.casefold())
        if canonical:
            return canonical

        for alias, entity_id in aliases.items():
            if alias and alias in npc_id.casefold():
                return entity_id

        return npc_id

    def load_location_relations(self, location_id):
        """Return the raw relation document, or an empty dict if unavailable."""
        directory = self._find_location_dir(location_id)
        if not directory:
            return {}
        return self._read_json(os.path.join(directory, "relations.json"))

    def _relation_records(self, document):
        records = document.get("relations")
        if records is None:
            records = document.get("relationships", [])

        if isinstance(records, list):
            return records

        if isinstance(records, dict):
            result = []
            for npc_id, value in records.items():
                if isinstance(value, dict):
                    item = dict(value)
                    item.setdefault("npc", npc_id)
                    result.append(item)
            return result

        return []

    def get_relations(self, location_id, npc_ids, player_id="player"):
        """Return normalized relationship records for active NPCs."""
        document = self.load_location_relations(location_id)
        if not document:
            return []

        default_npcs = {
            self._canonical_npc_id(npc_id)
            for npc_id in document.get("default_npcs", [])
        }
        records = self._relation_records(document)
        result = []

        for npc_id in npc_ids or []:
            canonical_npc_id = self._canonical_npc_id(npc_id)
            relationship = copy.deepcopy(self.DEFAULT_RELATIONSHIP)
            matched = False

            for record in records:
                record_npc = record.get("npc", record.get("npc_id"))
                record_player = record.get("player", record.get("player_id"))
                if self._canonical_npc_id(record_npc) != canonical_npc_id:
                    continue
                if record_player and record_player != player_id:
                    continue

                relationship.update(record.get("relationship", {}))
                matched = True
                break

            if matched or canonical_npc_id in default_npcs:
                result.append({
                    "npc": canonical_npc_id,
                    "player": player_id,
                    "relationship": relationship,
                })

        return result
