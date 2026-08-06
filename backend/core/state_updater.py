import os
import json


class StateUpdater:

    def __init__(self):
        pass


    def load_location_relations(self, location_id):

        path = (
            f"world/location/{location_id}/relations.json"
        )

        if not os.path.exists(path):
            return {}


        try:

            with open(
                path,
                "r",
                encoding="utf-8"
            ) as f:

                return json.load(f)

        except Exception:

            return {}



    def detect(self, user_input):

        result = {}


        location_keywords = {

            "暖阳角落咖啡店":
                "L_Warm_Corner",

            "暖阳角落":
                "L_Warm_Corner",

            "咖啡店":
                "L_Warm_Corner"

        }



        for keyword, location_id in location_keywords.items():

            if keyword in user_input:

                result["location"] = location_id


                relations = (
                    self.load_location_relations(
                        location_id
                    )
                )


                if "default_npcs" in relations:

                    result["active_npc"] = (
                        relations["default_npcs"]
                    )


                break



        npc_keywords = {

            "沫沫":
                "momo",

            "momo":
                "momo"

        }


        for keyword, npc_id in npc_keywords.items():

            if keyword in user_input:

                result.setdefault(
                    "active_npc",
                    []
                )


                if npc_id not in result["active_npc"]:

                    result["active_npc"].append(
                        npc_id
                    )


        return result
