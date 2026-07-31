import os
import json
from datetime import datetime


class MemoryManager:

    def __init__(self, base_path="memory"):

        self.base_path = base_path

        self.conversation_dir = os.path.join(
            self.base_path,
            "conversations"
        )

        self.long_term_dir = os.path.join(
            self.base_path,
            "long_term"
        )

        self.conversation_file = os.path.join(
            self.conversation_dir,
            "current.json"
        )

        self._init_storage()


    def _init_storage(self):

        os.makedirs(
            self.conversation_dir,
            exist_ok=True
        )

        os.makedirs(
            self.long_term_dir,
            exist_ok=True
        )


    # ==========================
    # 短期连续对话
    # ==========================

    def load_conversation(self):

        if not os.path.exists(
            self.conversation_file
        ):
            return []


        try:

            with open(
                self.conversation_file,
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)

                return data.get(
                    "messages",
                    []
                )

        except Exception:

            return []


    def save_conversation(
        self,
        messages
    ):

        data = {

            "updated_at":
                datetime.now().isoformat(),

            "messages":
                messages

        }


        with open(
            self.conversation_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=2
            )


    def add_message(
        self,
        role,
        content
    ):

        messages = self.load_conversation()


        messages.append({

            "role": role,

            "content": content,

            "time":
                datetime.now().isoformat()

        })


        self.save_conversation(
            messages
        )


    def clear_conversation(self):

        self.save_conversation([])



    # ==========================
    # 长期实体记忆
    # ==========================

    def save_entity_memory(
        self,
        entity_id,
        content,
        importance=1
    ):

        file_path = os.path.join(
            self.long_term_dir,
            entity_id + ".json"
        )


        data = {

            "entity_id": entity_id,

            "memories": []

        }


        if os.path.exists(file_path):

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)


        data["memories"].append({

            "content": content,

            "importance": importance,

            "created_at":
                datetime.now().isoformat()

        })


        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=2
            )


    def load_entity_memory(
        self,
        entity_id
    ):

        file_path = os.path.join(
            self.long_term_dir,
            entity_id + ".json"
        )


        if not os.path.exists(file_path):

            return []


        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

            return data.get(
                "memories",
                []
            )


    # ==========================
    # 提供给 Prompt Builder
    # ==========================

    def get_context_memory(
        self,
        entity_id=None
    ):

        result = {

            "conversation":
                self.load_conversation(),

            "entity_memory":
                []

        }


        if entity_id:

            result["entity_memory"] = (
                self.load_entity_memory(entity_id)
            )


        return result
