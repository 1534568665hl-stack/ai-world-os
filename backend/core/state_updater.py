import os
import json


class StateUpdater:

    NPC_ALIASES = {
        "沫沫": "N_Momo",
        "momo": "N_Momo",
        "n_momo": "N_Momo",
    }

    def __init__(self):
        pass

    def _canonical_npc_id(self, npc_id):
        if not isinstance(npc_id, str):
            return npc_id
        return self.NPC_ALIASES.get(
            npc_id.casefold(),
            npc_id
        )

    def load_location_relations(self, location_id):
        location_root = "world/location"
        if not os.path.isdir(location_root):
            return {}

        relations_path = ""
        for directory_name in os.listdir(location_root):
            directory = os.path.join(
                location_root,
                directory_name
            )
            info_path = os.path.join(directory, "info.json")
            if not os.path.isdir(directory) or not os.path.exists(info_path):
                continue

            try:
                with open(info_path, "r", encoding="utf-8") as file:
                    info = json.load(file)
            except Exception:
                continue

            if info.get("id") == location_id:
                relations_path = os.path.join(
                    directory,
                    "relations.json"
                )
                break

        if not relations_path or not os.path.exists(relations_path):
            return {}

        try:
            with open(
                relations_path,
                "r",
                encoding="utf-8"
            ) as file:
                return json.load(file)
        except Exception:
            return {}

    def detect(self, user_input):
        result = {}

        location_keywords = {
            "暖阳角落咖啡店": "L_Warm_Corner",
            "暖阳角落": "L_Warm_Corner",
            "咖啡店": "L_Warm_Corner",
        }

        for keyword, location_id in location_keywords.items():
            if keyword in user_input:
                result["location"] = location_id
                relations = self.load_location_relations(location_id)
                if "default_npcs" in relations:
                    result["active_npc"] = [
                        self._canonical_npc_id(npc_id)
                        for npc_id in relations["default_npcs"]
                    ]
                break

        npc_keywords = self.NPC_ALIASES
        normalized_input = user_input.casefold()

        for keyword, npc_id in npc_keywords.items():
            if keyword in normalized_input:
                result.setdefault("active_npc", [])
                if npc_id not in result["active_npc"]:
                    result["active_npc"].append(npc_id)

        return result
