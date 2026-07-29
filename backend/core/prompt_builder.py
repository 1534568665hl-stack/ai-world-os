import json
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class PromptBuilder:
    """
    Prompt 构建器
    
    职责：接收来自 context_builder.py 的统一标准 Context Object，
    严格按照业务约定的优先级顺序与层级结构，组装拼接成最终发送给大语言模型（LLM）的 Prompt 字符串。
    """
    def __init__(self):
        pass

    def _format_entity(self, entity: Dict[str, Any]) -> str:
        """
        统一格式化世界实体的基础组件，完整保留 info, tags 和 description 来源
        """
        if not entity:
            return ""
            
        entity_id = entity.get("id", "unknown_id")
        entity_type = entity.get("type", "unknown_type")
        info = entity.get("info", {})
        tags = entity.get("tags", {})
        description = entity.get("description", "").strip()
        
        # 优先展示可读名称，如果没有则使用 ID 替代
        display_name = info.get("name", entity_id)
        
        lines = [
            f"### 实名/标识：{display_name} (ID: {entity_id})",
            f"* **类型属性**: {entity_type}",
            f"* **元数据信息 (info)**: {json.dumps(info, ensure_ascii=False)}",
            f"* **索引标签 (tags)**: {json.dumps(tags, ensure_ascii=False)}",
            f"* **核心特征描述 (description)**:",
            f"{description}",
            "---"
        ]
        return "\n".join(lines)

    def build(self, context: Dict[str, Any]) -> str:
        """
        将 Context Object 按照严格优先级转换为 Markdown 格式的 Prompt 文本
        
        :param context: 由 context_builder 生成的标准上下文对象
        :return: 序列化后的最终 Prompt 字符串
        """
        prompt_sections = []

        # 分离各个顶层上下文节点
        runtime = context.get("runtime", {})
        world = context.get("world", {})
        memory = context.get("memory", [])
        events = context.get("events", [])

        # ----------------------------------------------------------------------
        # 优先级 1: Runtime State
        # ----------------------------------------------------------------------
        prompt_sections.append("# [1/8] Runtime State (运行状态环境)")
        prompt_sections.append(f"* **当前系统时间**: {runtime.get('time', '未知时间')}")
        prompt_sections.append(f"* **当前定位地点 ID**: {runtime.get('current_location', '未知地点')}")
        active_npcs = ", ".join(runtime.get("active_npc", [])) or "无"
        prompt_sections.append(f"* **当前活动交互中的 NPC**: {active_npcs}")
        prompt_sections.append("")

        # ----------------------------------------------------------------------
        # 优先级 2: Current Location
        # ----------------------------------------------------------------------
        prompt_sections.append("# [2/8] Current Location Details (当前场景空间)")
        locations = world.get("location", [])
        if locations:
            for loc in locations:
                prompt_sections.append(self._format_entity(loc))
        else:
            prompt_sections.append("（当前没有关于此地点的详细数据说明）")
        prompt_sections.append("")

        # ----------------------------------------------------------------------
        # 优先级 3: Active NPC
        # ----------------------------------------------------------------------
        prompt_sections.append("# [3/8] Active NPC Details (当前对话角色特征)")
        npcs = world.get("npc", [])
        if npcs:
            for npc in npcs:
                prompt_sections.append(self._format_entity(npc))
        else:
            prompt_sections.append("（当前场景内无处于激活交互状态的NPC角色）")
        prompt_sections.append("")

        # ----------------------------------------------------------------------
        # 优先级 4: Related Items
        # ----------------------------------------------------------------------
        prompt_sections.append("# [4/8] Related Items (当前环境关联物品)")
        items = world.get("item", [])
        if items:
            for item in items:
                prompt_sections.append(self._format_entity(item))
        else:
            prompt_sections.append("（没有检索到相关的物品定义）")
        prompt_sections.append("")

        # ----------------------------------------------------------------------
        # 优先级 5: Related Rules
        # ----------------------------------------------------------------------
        prompt_sections.append("# [5/8] Related Rules (世界运行底层规则/物理法则)")
        rules = world.get("rule", [])
        if rules:
            for rule in rules:
                prompt_sections.append(self._format_entity(rule))
        else:
            prompt_sections.append("（无特殊触发的环境或行为限制规则）")
        prompt_sections.append("")

        # ----------------------------------------------------------------------
        # 优先级 6: Memory
        # ----------------------------------------------------------------------
        prompt_sections.append("# [6/8] Memory Records (长短期记忆片段)")
        if memory:
            for idx, mem in enumerate(memory, 1):
                if isinstance(mem, dict):
                    prompt_sections.append(f"{idx}. {json.dumps(mem, ensure_ascii=False)}")
                else:
                    prompt_sections.append(f"{idx}. {mem}")
        else:
            prompt_sections.append("（记忆空白，暂无与当前上下文相关的历史记忆痕迹）")
        prompt_sections.append("")

        # ----------------------------------------------------------------------
        # 优先级 7: Events
        # ----------------------------------------------------------------------
        prompt_sections.append("# [7/8] Dynamic Events (突发事件快照)")
        if events:
            for idx, event in enumerate(events, 1):
                if isinstance(event, dict):
                    prompt_sections.append(f"{idx}. {json.dumps(event, ensure_ascii=False)}")
                else:
                    prompt_sections.append(f"{idx}. {event}")
        else:
            prompt_sections.append("（世界线平稳，当前无正在发生的动态外部事件）")
        prompt_sections.append("")

        # ----------------------------------------------------------------------
        # 优先级 8: User Message
        # ----------------------------------------------------------------------
        prompt_sections.append("# [8/8] User Message (玩家最新交互输入)")
        prompt_sections.append(f"玩家行为/发言：\"{runtime.get('user_message', '')}\"")
        prompt_sections.append("")
        
        prompt_sections.append("请基于以上完整的世界观背景、角色设定、场景限制与运行规则，生成符合逻辑的下一步世界演进响应。")

        return "\n".join(prompt_sections)
