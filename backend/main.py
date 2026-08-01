import os
import sys
from datetime import datetime


# ==========================
# UTF-8 修复
# ==========================

try:
    sys.stdin = open(
        sys.stdin.fileno(),
        mode="r",
        encoding="utf-8",
        buffering=1
    )
except Exception:
    pass



sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)



from backend.core.world_loader import WorldLoader
from backend.core.retriever import Retriever
from backend.core.context_builder import ContextBuilder
from backend.core.prompt_builder import PromptBuilder
from backend.core.llm.client import LLMClient

from backend.core.memory_manager import MemoryManager
from backend.core.memory_extractor import MemoryExtractor

from backend.core.state_manager import StateManager



def main():

    print(
        "====== 🤖 Welcome to AI World OS (Terminal Engine v1.0) ======"
    )


    world_dir = "./world"


    if not os.path.exists(world_dir):

        print(
            f"❌ 错误: 找不到世界数据目录 '{world_dir}'"
        )

        return



    print(
        "[System] Loading world entities..."
    )


    loader = WorldLoader(
        world_base_path=world_dir
    )


    entities = loader.load_all()


    print(
        f"[System] Successfully loaded {len(entities)} world entities."
    )



    retriever = Retriever(
        entities=entities
    )


    context_builder = ContextBuilder()

    prompt_builder = PromptBuilder()

    llm_client = LLMClient()

    memory_manager = MemoryManager()

    memory_extractor = MemoryExtractor()

    state_manager = StateManager()



    # ==========================
    # World State
    # ==========================


    world_state = state_manager.load()


    print(
        "[World State]"
    )


    print(
        f"LOCATION: {world_state.get('location','')}"
    )


    print(
        f"ACTIVE NPC: {world_state.get('active_npc',[])}"
    )



    print(
        "[LLM Config]"
    )


    print(
        f"MODEL: {llm_client.model}"
    )


    print(
        f"BASE_URL: {llm_client.base_url}"
    )



    print(
        "\n--------------------------------------------------------------"
    )


    try:

        user_input = input(
            "请输入你想对这个世界说的话/做出的行动:\n> "
        )


    except UnicodeDecodeError:

        print(
            "[System] 输入编码错误，请重新输入。"
        )

        return



    if not user_input.strip():

        print(
            "[System] 输入不能为空，程序退出。"
        )

        return



    # ==========================
    # Save User Message
    # ==========================


    memory_manager.add_message(
        "user",
        user_input
    )



    current_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M"
    )


    user_context = {

        "message":
            user_input,

        "time":
            current_time,

        "current_location":
            world_state.get(
                "location",
                ""
            ),

        "active_npc":
            world_state.get(
                "active_npc",
                []
            )

    }



    print(
        "[Pipeline] 1/5. Running Retriever filtering..."
    )


    retrieved_data = retriever.retrieve(
        user_context
    )



    print(
        "[Pipeline] 2/5. Building unified Context Object..."
    )


    context_object = context_builder.build(
        user_context=user_context,
        retrieved_data=retrieved_data
    )



    print(
        "[Pipeline] 3/5. Rendering final System Prompt..."
    )


    final_prompt = prompt_builder.build(
        context_object
    )



    print(
        "[Pipeline] 4/5. Dispatching payload to LLM Client..."
    )



    system_instruction = (

        "你是 AI World OS 的世界运行核心。"

        "\n\n你的任务："
        "根据提供的世界数据、NPC资料、地点信息、规则和记忆，"
        "生成连续、合理的世界响应。"


        "\n\n【重要运行规则】"


        "\n1. 数据真实性："
        "只能把 Prompt 中提供的数据视为真实存在。"
        "不要假装拥有不存在的数据库记录。"


        "\n2. 状态限制："
        "你不能声称已经修改世界状态。"
        "禁止输出："
        "‘状态已更新’、"
        "‘永久保存成功’、"
        "‘好感度已经提升’、"
        "‘NPC记忆已经写入’"
        "等后台操作结果。"


        "\n3. 事件描述："
        "可以描述当前剧情中发生的事情，"
        "但必须明确这是当前叙事，而不是数据库修改。"


        "\n4. 记忆规则："
        "玩家询问过去信息时，"
        "必须依据 Memory Records。"
        "没有找到记录时必须说明没有相关记忆。"


        "\n5. NPC规则："
        "NPC只能使用已有设定。"
        "未知背景不要自行编造成既定事实。"


        "\n6. 输出风格："
        "保持沉浸式世界模拟风格。"
        "不要暴露服务器、API、代码实现细节。"

    )



    ai_response = llm_client.generate_response(
        prompt=final_prompt,
        system_instruction=system_instruction
    )



    # ==========================
    # Save AI Memory
    # ==========================


    if (
        ai_response
        and
        not ai_response.startswith("Error:")
    ):

        memory_manager.add_message(
            "assistant",
            ai_response
        )

    else:

        print(
            "[Memory] Error response ignored."
        )



    # ==========================
    # Extract Long Memory
    # ==========================


    memories = memory_extractor.extract(
        user_input
    )


    for memory in memories:

        memory_manager.save_entity_memory(
            "player",
            memory["content"],
            memory["importance"]
        )



    print(
        "[Pipeline] 5/5. Execution complete. Response received:\n"
    )


    print(
        "====== 🌌 AI WORLD OS RESPONSE ======"
    )


    print(
        ai_response
    )


    print(
        "====================================="
    )



if __name__ == "__main__":

    main()
