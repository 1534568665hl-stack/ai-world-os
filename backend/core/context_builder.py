import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class ContextBuilder:
    """
    统一上下文构建器
    
    职责：作为承上启下的中间层，将前端或系统传入的实时运行状态（User Context）
    与检索器过滤出的实体数据（Retrieval Result）进行结构化拼装，
    生成供后续 Prompt 生成器直接消费的统一 Context Object。
    """
    def __init__(self):
        pass

    def build(
        self, 
        user_context: Dict[str, Any], 
        retrieved_data: Dict[str, List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        """
        组合用户状态和检索到的实体数据，生成标准 Context Object
        
        :param user_context: 包含用户当前信息（时间、地点、活动NPC、消息）的字典
        :param retrieved_data: 来自 retriever.py 检索过滤后的世界实体字典
        :return: 包含完整运行状态与上下文数据的统一 Context 字典
        """
        # 提取并映射实时运行状态 (Runtime State 优先)
        runtime_state = {
            "time": user_context.get("time", ""),
            "current_location": user_context.get("current_location", ""),
            "active_npc": user_context.get("active_npc", []),
            "user_message": user_context.get("message", "")
        }

        # 映射检索到的世界实体，严守数据隔离，直接透传保留数据来源结构
        world_context = {
            "location": retrieved_data.get("location", []),
            "npc": retrieved_data.get("npc", []),
            "item": retrieved_data.get("item", []),
            "rule": retrieved_data.get("rule", [])
        }

        # 拼装为系统约定的统一标准 Context Object 结构
        context_object = {
            "runtime": runtime_state,
            "world": world_context,
            # 为未来记忆系统与事件系统预留的空接口
            "memory": [],
            "events": []
        }

        return context_object
