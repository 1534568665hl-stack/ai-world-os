import os
import json
import logging
import requests
from typing import Optional

logger = logging.getLogger(__name__)

class LLMClient:
    """
    LLM 客户端通信层
    
    职责：负责通过 HTTP 请求与符合 OpenAI 规范的聊天模型 API 终结点进行通信。
    该模块完全不感知任何业务领域知识（如 NPC 设定、世界规则等），只关注输入 Prompt 并投递给模型，返回最终文本。
    """
    def __init__(
        self, 
        api_key: Optional[str] = None, 
        model: Optional[str] = None, 
        base_url: Optional[str] = None
    ):
        """
        初始化客户端配置，优先使用显式传入的参数，其次读取系统环境变量。
        
        :param api_key: API 密钥
        :param model: 模型名称（如 gpt-4o、gpt-4o-mini 等）
        :param base_url: API 基础路径，允许接入各类兼容 OpenAI 的第三方/中转或本地模型网关
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o")
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

    def generate_response(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        """
        将构建完毕的 Prompt 字符串投递至大语言模型并返回生成的文本结果。
        
        :param prompt: 完整的上下文拼装后的用户提示词字符串
        :param system_instruction: 可选的系统级指导指令（System Prompt）
        :return: 模型返回的纯文本字符串，若发生异常则返回清晰的错误提示信息
        """
        # 错误检查：校验凭证是否存在
        if not self.api_key:
            return "Error: [LLMClient] API Key is missing. Please set the OPENAI_API_KEY environment variable or pass it during initialization."

        # 构建标准的 Chat Completions 消息流结构
        messages = []
        if system_instruction and system_instruction.strip():
            messages.append({
                "role": "system",
                "content": system_instruction.strip()
            })
        
        messages.append({
            "role": "user",
            "content": prompt
        })

        # 规整请求终结点 URL
        target_url = f"{self.base_url.rstrip('/')}/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7
        }

        try:
            # 发起网络同步请求，设定 60 秒超时防止请求无限挂起
            response = requests.post(target_url, json=payload, headers=headers, timeout=60)
            
            # 检查 HTTP 状态码是否触发异常（如 401, 403, 404, 500 等）
            response.raise_for_status()
            
            response_data = response.json()
            
            # 解析响应 JSON 体并安全返回最终文本
            return response_data["choices"][0]["message"]["content"]
            
        except requests.exceptions.Timeout:
            error_msg = "Error: [LLMClient] Request timed out after 60 seconds."
            logger.error(error_msg)
            return error_msg
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Error: [LLMClient] Network or HTTP Request failed: {str(e)}"
            logger.error(error_msg)
            return error_msg
            
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            error_msg = f"Error: [LLMClient] Failed to parse API response format: {str(e)}"
            logger.error(error_msg)
            return error_msg
