import logging
from typing import Dict, Any, List

from backend.core.memory_manager import MemoryManager


logger = logging.getLogger(__name__)


class ContextBuilder:
    """
    统一上下文构建器

    职责：
    将实时运行状态、世界实体、历史记忆、事件状态
    组合成统一 Context Object，供 PromptBuilder 使用。
    """


    def __init__(self):

        self.memory_manager = MemoryManager()



    def build(
        self,
        user_context: Dict[str, Any],
        retrieved_data: Dict[str, List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        """
        生成标准 Context Object
        """


        # ==========================
        # Runtime State
        # ==========================

        runtime_state = {

            "time":
                user_context.get(
                    "time",
                    ""
                ),

            "current_location":
                user_context.get(
                    "current_location",
                    ""
                ),

            "active_npc":
                user_context.get(
                    "active_npc",
                    []
                ),

            "user_message":
                user_context.get(
                    "message",
                    ""
                )
        }



        # ==========================
        # World Context
        # ==========================

        world_context = {

            "location":
                retrieved_data.get(
                    "location",
                    []
                ),

            "npc":
                retrieved_data.get(
                    "npc",
                    []
                ),

            "item":
                retrieved_data.get(
                    "item",
                    []
                ),

            "rule":
                retrieved_data.get(
                    "rule",
                    []
                )

        }



        # ==========================
        # Memory Context
        # ==========================

        conversation_memory = (
            self.memory_manager.load_conversation()
        )


        memory_context = {

            "conversation":
                conversation_memory,

            "long_term":
                []

        }


        # 如果当前存在NPC，则读取NPC记忆

        active_npc = user_context.get(
            "active_npc",
            []
        )


        if active_npc:

            npc_id = active_npc[0]

            memory_context["long_term"] = (
                self.memory_manager.load_entity_memory(
                    npc_id
                )
            )



        # ==========================
        # Final Context Object
        # ==========================

        context_object = {


            "runtime":
                runtime_state,


            "world":
                world_context,


            "memory":
                memory_context,


            "events":
                []

        }


        return context_object
