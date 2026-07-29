import logging
from typing import List, Dict, Any, Set

logger = logging.getLogger(__name__)

class Retriever:
    """
    实体检索器
    
    职责：基于用户输入与上下文状态，利用标签、名称、类型过滤等基础文本匹配规则，
    从全量加载的世界实体中检索并过滤出最相关的上下文。
    """
    def __init__(self, entities: List[Dict[str, Any]]):
        """
        初始化检索器
        :param entities: 已经通过 world_loader 加载的全部实体列表
        """
        self.all_entities = entities
        
        # 建立基于 ID 的 O(1) 快速索引字典
        self.entity_dict: Dict[str, Dict[str, Any]] = {
            e.get("id"): e for e in entities if e.get("id")
        }
        
        # 按类型预先分组，加速后续针对性检索，支持 npc, location, item, rule[span_0](start_span)[span_0](end_span)
        self.by_type: Dict[str, List[Dict[str, Any]]] = {
            "npc": [],
            "location": [],
            "item": [],
            "rule": []
        }
        for entity in entities:
            entity_type = entity.get("type")
            if entity_type in self.by_type:
                self.by_type[entity_type].append(entity)

    def retrieve(self, context: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        """
        执行检索与上下文过滤
        :param context: 包含 message, current_location, active_npc 的字典
        :return: 结构化的检索结果字典
        """
        message: str = context.get("message", "").lower()
        current_location_id: str = context.get("current_location", "")
        active_npc_ids: List[str] = context.get("active_npc", [])

        # 统一输出格式，限制返回实体并分类
        result: Dict[str, List[Dict[str, Any]]] = {
            "npc": [],
            "location": [],
            "item": [],
            "rule": []
        }
        
        # 记录已处理的实体 ID，避免重复 (Context Filtering: 避免重复)
        seen_ids: Set[str] = set()

        # ==========================================
        # 阶段 1：强制相关性提取 (Priority 1 & 2)[span_1](start_span)[span_1](end_span)
        # ==========================================
        
        # 优先级 1: 当前活动 NPC (限制最大 3 个)
        for npc_id in active_npc_ids:
            if len(result["npc"]) >= 3:
                break
            if npc_id in self.entity_dict and npc_id not in seen_ids:
                result["npc"].append(self.entity_dict[npc_id])
                seen_ids.add(npc_id)

        # 优先级 2: 当前所在地点 (限制最大 1 个)
        if current_location_id and current_location_id in self.entity_dict:
            if current_location_id not in seen_ids and len(result["location"]) < 1:
                result["location"].append(self.entity_dict[current_location_id])
                seen_ids.add(current_location_id)

        # ==========================================
        # 阶段 2：基于用户输入的语义推断与匹配 (Priority 3, 4, 5)[span_2](start_span)[span_2](end_span)
        # ==========================================
        
        def is_relevant(entity: Dict[str, Any]) -> bool:
            """检查单个实体是否与当前 message 相关"""
            if not message:
                return False
                
            info = entity.get("info", {})
            tags_data = entity.get("tags", {})
            
            # 1. 匹配实体 ID
            if entity.get("id", "").lower() in message:
                return True
                
            # 2. 匹配人类可读名称 (name)
            name = info.get("name", "").lower()
            if name and name in message:
                return True
                
            # 3. 匹配检索标签 (tags/categories/attributes)
            # tags_data 期望遵循 tags.schema.json，包含 'tags' 列表[span_3](start_span)[span_3](end_span)
            tags_list = tags_data.get("tags", [])
            for tag in tags_list:
                if str(tag).lower() in message:
                    return True
                    
            categories_list = tags_data.get("categories", [])
            for category in categories_list:
                if str(category).lower() in message:
                    return True
                    
            return False

        # 优先级 3: 相关的 Items (限制最大 5 个)
        for item in self.by_type["item"]:
            if len(result["item"]) >= 5:
                break
            if item["id"] not in seen_ids and is_relevant(item):
                result["item"].append(item)
                seen_ids.add(item["id"])

        # 优先级 4: 相关的 Rules (不设硬性上限，只返回相关的即可)[span_4](start_span)[span_4](end_span)
        for rule in self.by_type["rule"]:
            if rule["id"] not in seen_ids and is_relevant(rule):
                result["rule"].append(rule)
                seen_ids.add(rule["id"])

        # 优先级 5: 相关的其他背景角色与地点 (填充剩余额度)
        for npc in self.by_type["npc"]:
            if len(result["npc"]) >= 3:
                break
            if npc["id"] not in seen_ids and is_relevant(npc):
                result["npc"].append(npc)
                seen_ids.add(npc["id"])

        for loc in self.by_type["location"]:
            if len(result["location"]) >= 1:
                break
            if loc["id"] not in seen_ids and is_relevant(loc):
                result["location"].append(loc)
                seen_ids.add(loc["id"])

        return result

