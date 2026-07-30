import os
import sys
from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel


# ==================================
# Python路径修正
# ==================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(PROJECT_ROOT)


# ==================================
# 导入核心模块
# ==================================

from backend.core.world_loader import WorldLoader
from backend.core.retriever import Retriever
from backend.core.context_builder import ContextBuilder
from backend.core.prompt_builder import PromptBuilder
from backend.llm.client import LLMClient



# ==================================
# 创建API服务
# ==================================

app = FastAPI(
    title="AI World OS API",
    description="AI World OS 世界交互后端",
    version="0.1.0"
)



# ==================================
# 初始化世界系统
# ==================================

print("====== AI World OS Starting ======")


WORLD_PATH = os.path.join(
    PROJECT_ROOT,
    "world"
)


print("[System] Loading world data...")


loader = WorldLoader(
    world_base_path=WORLD_PATH
)


entities = loader.load_all()


print(
    f"[System] Loaded {len(entities)} entities"
)



# 初始化核心模块

retriever = Retriever(
    entities
)


context_builder = ContextBuilder()


prompt_builder = PromptBuilder()


llm_client = LLMClient()



print("[System] AI World OS Ready")



# ==================================
# 数据模型
# ==================================

class ChatRequest(BaseModel):

    message: str



class ChatResponse(BaseModel):

    response: str



# ==================================
# 首页检测
# ==================================

@app.get("/")
def index():

    return {

        "name":
        "AI World OS",

        "status":
        "running",

        "version":
        "0.1.0",

        "entities":
        len(entities)

    }



# ==================================
# 核心聊天接口
# ==================================

@app.post(
    "/chat",
    response_model=ChatResponse
)
def chat(
    request: ChatRequest
):

    user_message = request.message


    print(
        "[User]",
        user_message
    )


    # ------------------------------
    # 1. Runtime状态
    # ------------------------------

    user_context = {

        "message":
        user_message,


        "time":
        datetime.now()
        .strftime(
            "%Y-%m-%d %H:%M"
        ),


        # 第一版固定测试场景
        "current_location":
        "L_Warm_Corner",


        "active_npc":
        [
            "N_Momo"
        ]

    }



    # ------------------------------
    # 2. Retriever检索
    # ------------------------------

    print(
        "[Pipeline] Retrieving..."
    )


    retrieved_data = retriever.retrieve(
        user_context
    )



    # ------------------------------
    # 3. Context构建
    # ------------------------------

    print(
        "[Pipeline] Building context..."
    )


    context = context_builder.build(

        user_context,

        retrieved_data

    )



    # ------------------------------
    # 4. Prompt生成
    # ------------------------------

    print(
        "[Pipeline] Building prompt..."
    )


    prompt = prompt_builder.build(
        context
    )



    # ------------------------------
    # 5. 调用LLM
    # ------------------------------

    print(
        "[Pipeline] Calling LLM..."
    )


    response = llm_client.generate_response(

        prompt=prompt,


        system_instruction=
        """
你是 AI World OS 的世界运行核心。

你的任务：

1. 严格遵守世界设定。
2. 保持NPC人格一致。
3. 根据当前地点和角色状态生成自然互动。
4. 不解释系统，不跳出世界。
5. 让世界像真实生活一样运行。

"""

    )



    print(
        "[AI]",
        response[:100]
    )



    return {

        "response":
        response

    }
