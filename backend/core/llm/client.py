import os
import json
import logging
import requests
from typing import Optional

from dotenv import load_dotenv


logger = logging.getLogger(__name__)


# ==========================
# 加载项目根目录 .env
# ==========================

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../../"
    )
)

ENV_FILE = os.path.join(
    BASE_DIR,
    ".env"
)

load_dotenv(
    ENV_FILE,
    override=True
)



class LLMClient:
    """
    LLM 客户端通信层
    
    职责：
    负责通过 HTTP 请求与符合 OpenAI 规范的聊天模型 API 终结点通信。
    """

    def __init__(
        self, 
        api_key: Optional[str] = None, 
        model: Optional[str] = None, 
        base_url: Optional[str] = None
    ):


        self.api_key = (
            api_key
            or os.getenv("OPENAI_API_KEY")
        )


        self.model = (
            model
            or os.getenv(
                "OPENAI_MODEL",
                "gpt-4o"
            )
        )


        self.base_url = (
            base_url
            or os.getenv(
                "OPENAI_BASE_URL",
                "https://api.openai.com/v1"
            )
        )


        # 调试配置，确认实际读取值
        print(
            "[LLM Config]"
        )

        print(
            "MODEL:",
            self.model
        )

        print(
            "BASE_URL:",
            self.base_url
        )



    def generate_response(
        self,
        prompt: str,
        system_instruction: Optional[str] = None
    ) -> str:


        if not self.api_key:

            return (
                "Error: [LLMClient] "
                "API Key is missing."
            )



        messages = []


        if (
            system_instruction
            and system_instruction.strip()
        ):

            messages.append(
                {
                    "role": "system",
                    "content":
                        system_instruction.strip()
                }
            )


        messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )



        target_url = (
            f"{self.base_url.rstrip('/')}"
            "/chat/completions"
        )


        headers = {

            "Authorization":
                f"Bearer {self.api_key}",

            "Content-Type":
                "application/json"

        }



        payload = {

            "model":
                self.model,

            "messages":
                messages,

            "temperature":
                0.7

        }



        try:

            response = requests.post(
                target_url,
                json=payload,
                headers=headers,
                timeout=60
            )


            response.raise_for_status()


            response_data = response.json()


            return (
                response_data["choices"][0]
                ["message"]
                ["content"]
            )



        except requests.exceptions.Timeout:

            error_msg = (
                "Error: [LLMClient] "
                "Request timed out after 60 seconds."
            )

            logger.error(error_msg)

            return error_msg



        except requests.exceptions.RequestException as e:

            error_msg = (
                f"Error: [LLMClient] "
                f"Network or HTTP Request failed: {str(e)}"
            )

            logger.error(error_msg)

            return error_msg



        except (
            KeyError,
            IndexError,
            json.JSONDecodeError
        ) as e:

            error_msg = (
                f"Error: [LLMClient] "
                f"Failed to parse API response format: {str(e)}"
            )

            logger.error(error_msg)

            return error_msg
