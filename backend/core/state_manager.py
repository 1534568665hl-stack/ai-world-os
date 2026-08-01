import os
import json
from datetime import datetime


class StateManager:
    """
    世界运行状态管理器

    保存:
    - 当前地点
    - 当前NPC
    - 世界事件
    - 时间状态
    """


    def __init__(self, path="memory/world_state.json"):

        self.path = path

        folder = os.path.dirname(self.path)

        if folder:
            os.makedirs(
                folder,
                exist_ok=True
            )


        self.default_state = {

            "location": "",

            "active_npc": [],

            "events": [],

            "updated_at": ""

        }



    def load(self):

        if not os.path.exists(self.path):

            return self.default_state.copy()


        try:

            with open(
                self.path,
                "r",
                encoding="utf-8"
            ) as f:

                return json.load(f)


        except Exception:

            return self.default_state.copy()



    def save(self, state):

        state["updated_at"] = (
            datetime.now().isoformat()
        )


        with open(
            self.path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                state,
                f,
                ensure_ascii=False,
                indent=2
            )



    def update(self, **kwargs):

        state = self.load()


        for key,value in kwargs.items():

            state[key] = value


        self.save(state)


        return state
