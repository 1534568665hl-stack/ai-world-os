import json
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class PromptBuilder:
    """
    Prompt 构建器

    职责：
    接收 ContextBuilder 生成的统一 Context Object，
    按照固定优先级生成发送给 LLM 的最终 Prompt。
    """


    def __init__(self):
        pass



    def _format_entity(
        self,
        entity: Dict[str, Any]
    ) -> str:
        """
        格式化世界实体
        """

        if not entity:
            return ""


        entity_id = entity.get(
            "id",
            "unknown_id"
        )

        entity_type = entity.get(
            "type",
            "unknown_type"
        )

        info = entity.get(
            "info",
            {}
        )

        tags = entity.get(
            "tags",
            {}
        )

        description = entity.get(
            "description",
            ""
        ).strip()


        display_name = info.get(
            "name",
            entity_id
        )


        lines = [

            f"### 实名/标识：{display_name} (ID: {entity_id})",

            f"* **类型属性**: {entity_type}",

            f"* **元数据信息 (info)**: "
            f"{json.dumps(info, ensure_ascii=False)}",

            f"* **索引标签 (tags)**: "
            f"{json.dumps(tags, ensure_ascii=False)}",

            "* **核心特征描述 (description)**:",

            description,

            "---"

        ]


        return "\n".join(lines)



    def build(
        self,
        context: Dict[str, Any]
    ) -> str:
        """
        根据 Context Object 生成最终 Prompt
        """


        prompt_sections = []


        runtime = context.get(
            "runtime",
            {}
        )

        world = context.get(
            "world",
            {}
        )

        memory = context.get(
            "memory",
            {}
        )

        events = context.get(
            "events",
            []
        )

        relations = context.get(
            "relations",
            {}
        )

        npc_state = context.get(
            "npc_state",
            {}
        )



        # ==================================================
        # 1 Runtime
        # ==================================================

        prompt_sections.append(
            "# [1/8] Runtime State (运行状态环境)"
        )


        prompt_sections.append(
            f"* **当前系统时间**: "
            f"{runtime.get('time', '未知时间')}"
        )

        prompt_sections.append(
            f"* **当前世界时间**: "
            f"{json.dumps(runtime.get('world_time', {}), ensure_ascii=False)}"
        )

        prompt_sections.append(
            "* **时间行为规则**: NPC行为必须符合当前世界时间；"
            "凌晨时NPC可能休息，白天可能工作，晚上可能回家。"
        )


        prompt_sections.append(
            f"* **当前定位地点 ID**: "
            f"{runtime.get('current_location', '未知地点')}"
        )


        active_npcs = ", ".join(
            runtime.get(
                "active_npc",
                []
            )
        ) or "无"


        prompt_sections.append(
            f"* **当前活动交互中的 NPC**: "
            f"{active_npcs}"
        )

        prompt_sections.append(
            f"* **NPC当前状态**: "
            f"{json.dumps(npc_state, ensure_ascii=False)}"
        )

        prompt_sections.append(
            "* **日程行为规则**: NPC行为必须符合当前日程。"
        )


        prompt_sections.append("")


        # ==================================================
        # 4 Relationship
        # ==================================================

        prompt_sections.append(
            "# [4/9] NPC Relationship (NPC与玩家关系)"
        )

        relation_records = (
            relations
            if isinstance(relations, list)
            else [relations] if relations else []
        )

        if relation_records:
            for relation in relation_records:
                prompt_sections.append(
                    json.dumps(relation, ensure_ascii=False)
                )
        else:
            prompt_sections.append("（当前没有可用的NPC关系数据）")

        prompt_sections.append("")



        # ==================================================
        # 2 Location
        # ==================================================

        prompt_sections.append(
            "# [2/8] Current Location Details (当前场景空间)"
        )


        locations = world.get(
            "location",
            []
        )


        if locations:

            for loc in locations:

                prompt_sections.append(
                    self._format_entity(loc)
                )

        else:

            prompt_sections.append(
                "（当前没有关于此地点的详细数据说明）"
            )


        prompt_sections.append("")



        # ==================================================
        # 3 NPC
        # ==================================================

        prompt_sections.append(
            "# [3/8] Active NPC Details (当前对话角色特征)"
        )


        npcs = world.get(
            "npc",
            []
        )


        if npcs:

            for npc in npcs:

                prompt_sections.append(
                    self._format_entity(npc)
                )

        else:

            prompt_sections.append(
                "（当前场景内无处于激活交互状态的NPC角色）"
            )


        prompt_sections.append("")



        # ==================================================
        # 4 Items
        # ==================================================

        prompt_sections.append(
            "# [5/9] Related Items (当前环境关联物品)"
        )


        items = world.get(
            "item",
            []
        )


        if items:

            for item in items:

                prompt_sections.append(
                    self._format_entity(item)
                )

        else:

            prompt_sections.append(
                "（没有检索到相关物品定义）"
            )


        prompt_sections.append("")



        # ==================================================
        # 5 Rules
        # ==================================================

        prompt_sections.append(
            "# [6/9] Related Rules (世界运行底层规则/物理法则)"
        )


        rules = world.get(
            "rule",
            []
        )


        if rules:

            for rule in rules:

                prompt_sections.append(
                    self._format_entity(rule)
                )

        else:

            prompt_sections.append(
                "（无特殊触发的环境或行为限制规则）"
            )


        prompt_sections.append("")



        # ==================================================
        # 6 Memory
        # ==================================================

        prompt_sections.append(
            "# [7/9] Memory Records (长短期记忆片段)"
        )


        conversation_memory = memory.get(
            "conversation",
            []
        )


        long_term_memory = memory.get(
            "long_term",
            []
        )



        if conversation_memory:

            prompt_sections.append(
                "## 最近对话记录"
            )


            for idx, msg in enumerate(
                conversation_memory[-10:],
                1
            ):

                if isinstance(
                    msg,
                    dict
                ):

                    prompt_sections.append(
                        f"{idx}. "
                        f"{msg.get('role','unknown')}: "
                        f"{msg.get('content','')}"
                    )

        else:

            prompt_sections.append(
                "（暂无近期对话记录）"
            )



        if long_term_memory:

            prompt_sections.append(
                "\n## 长期记忆"
            )


            for idx, mem in enumerate(
                long_term_memory,
                1
            ):

                prompt_sections.append(
                    f"{idx}. "
                    f"{json.dumps(mem, ensure_ascii=False)}"
                )

        else:

            prompt_sections.append(
                "（暂无长期记忆）"
            )


        prompt_sections.append("")



        # ==================================================
        # 7 Events
        # ==================================================

        prompt_sections.append(
            "# [8/9] Dynamic Events (突发事件快照)"
        )


        if events:

            for idx, event in enumerate(
                events,
                1
            ):

                prompt_sections.append(
                    f"{idx}. "
                    f"{json.dumps(event, ensure_ascii=False)}"
                )

        else:

            prompt_sections.append(
                "（世界线平稳，当前无正在发生的动态事件）"
            )


        prompt_sections.append("")



        # ==================================================
        # 8 User Message
        # ==================================================

        prompt_sections.append(
            "# [9/9] User Message (玩家最新交互输入)"
        )


        prompt_sections.append(
            f'玩家行为/发言："{runtime.get("user_message","")}"'
        )


        prompt_sections.append("")



        prompt_sections.append(
            "请基于以上完整的世界观背景、角色设定、"
            "场景限制、历史记忆与运行规则，"
            "生成符合逻辑的下一步世界演进响应。"
        )


        return "\n".join(
            prompt_sections
        )
