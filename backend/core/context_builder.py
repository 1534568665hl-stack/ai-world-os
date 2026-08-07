import logging
from datetime import datetime
from typing import Dict, Any, List

from backend.core.memory_manager import MemoryManager
from backend.core.relation_manager import RelationManager
from backend.core.relation_updater import RelationUpdater
from backend.core.event_memory import EventMemoryManager
from backend.core.schedule_manager import ScheduleManager


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
        self.relation_manager = RelationManager()
        self.relation_updater = RelationUpdater()
        self.event_memory_manager = EventMemoryManager()
        self.schedule_manager = ScheduleManager()

    def _format_world_time(self, world_time):
        if isinstance(world_time, dict):
            value = world_time.get("world_time", "")
            period = world_time.get("day_period", "")
        else:
            value = world_time or ""
            period = ""

        current = None
        for time_format in (
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
        ):
            try:
                current = datetime.strptime(value, time_format)
                break
            except (TypeError, ValueError):
                continue

        if current is None:
            return {
                "date": "",
                "time": "",
                "period": period,
            }

        if not period:
            if 5 <= current.hour < 12:
                period = "morning"
            elif 12 <= current.hour < 18:
                period = "afternoon"
            else:
                period = "night"

        return {
            "date": current.strftime("%Y-%m-%d"),
            "time": current.strftime("%H:%M:%S"),
            "period": period,
        }



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
                ),

            "world_time":
                self._format_world_time(
                    user_context.get("world_time", "")
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

        default_relation_records = self.relation_manager.get_relations(
            location_id=user_context.get("current_location", ""),
            npc_ids=active_npc,
            player_id=user_context.get("player_id", "player")
        )

        player_id = user_context.get("player_id", "player")
        default_by_npc = {
            relation["npc"]: relation
            for relation in default_relation_records
        }
        relation_records = []

        for npc_id in active_npc:
            runtime_relation = self.relation_updater.load_runtime_relation(
                npc_id,
                player_id
            )
            if runtime_relation:
                relation_records.append(
                    self.relation_updater.load(npc_id, player_id)
                )
            elif npc_id in default_by_npc:
                relation_records.append(default_by_npc[npc_id])

        if len(relation_records) == 1:
            relations = relation_records[0]
        else:
            relations = relation_records

        recent_events = self.event_memory_manager.get_recent_events(10)

        npc_states = [
            self.schedule_manager.get_current_state(
                npc_id,
                user_context.get("world_time", "")
            )
            for npc_id in active_npc
        ]
        if len(npc_states) == 1:
            npc_state = npc_states[0]
        else:
            npc_state = npc_states



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


            "relations":
                relations,


            "events":
                recent_events,


            "npc_state":
                npc_state

        }


        return context_object
