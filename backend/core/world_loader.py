import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional

# 配置简单的日志输出，用于提示加载错误
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class WorldLoader:
    def __init__(self, world_base_path: str):
        """
        初始化世界加载器
        :param world_base_path: world 目录的根路径，例如 "ai-world-os/world"
        """
        self.world_path = Path(world_base_path)
        # 根据目录结构，支持读取的顶级实体分类
        self.supported_categories = ["npc", "location", "item", "rule"]

    def _read_json(self, file_path: Path) -> Dict[str, Any]:
        """安全地读取 JSON 文件，如果不存在或解析失败则返回空字典"""
        if not file_path.exists():
            return {}
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"JSON 解析失败 [{file_path}]: {e}")
            return {}
        except Exception as e:
            logger.error(f"读取文件失败 [{file_path}]: {e}")
            return {}

    def _read_markdown(self, file_path: Path) -> str:
        """安全地读取 Markdown 文件，如果不存在则返回空字符串"""
        if not file_path.exists():
            return ""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            logger.error(f"读取文件失败 [{file_path}]: {e}")
            return ""

    def load_entity(self, entity_dir: Path) -> Optional[Dict[str, Any]]:
        """
        加载单个实体目录中的所有数据 (info.json, tags.json, description.md)
        """
        if not entity_dir.is_dir():
            return None

        info_path = entity_dir / "info.json"
        
        # 强制要求实体必须至少包含 info.json 才能被识别为有效实体
        if not info_path.exists():
            logger.warning(f"跳过无效实体目录 (缺少 info.json): {entity_dir}")
            return None

        # 加载三大核心文件
        info_data = self._read_json(info_path)
        tags_data = self._read_json(entity_dir / "tags.json")
        description_data = self._read_markdown(entity_dir / "description.md")

        # 提取核心标识：优先使用 info.json 中的数据，如果没有则回退使用目录名
        entity_id = info_data.get("id", entity_dir.name)
        entity_type = info_data.get("type", entity_dir.parent.name)

        # 组合为统一的返回格式
        return {
            "id": entity_id,
            "type": entity_type,
            "info": info_data,
            "tags": tags_data,
            "description": description_data
        }

    def load_category(self, category_name: str) -> List[Dict[str, Any]]:
        """
        加载特定类别（如 npc, location）下的所有实体
        """
        category_path = self.world_path / category_name
        entities = []

        if not category_path.exists() or not category_path.is_dir():
            logger.warning(f"找不到类别目录: {category_path}")
            return entities

        # 遍历类别目录下的所有子目录 (例如 world/npc/momo)
        for item in category_path.iterdir():
            if item.is_dir():
                entity_data = self.load_entity(item)
                if entity_data:
                    entities.append(entity_data)

        return entities

    def load_all(self) -> List[Dict[str, Any]]:
        """
        加载 world 目录下所有受支持类别的所有实体
        """
        all_entities = []
        if not self.world_path.exists():
            logger.error(f"World 根目录不存在: {self.world_path}")
            return all_entities

        for category in self.supported_categories:
            all_entities.extend(self.load_category(category))
            
        return all_entities

