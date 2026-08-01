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



    # ==========================
    # World Loader
    # ==========================


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



    # ==========================
    # Core Modules
    # ==========================


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
    # Load World State
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



    # ==========================
    # Input
    # ==========================


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
    # Save User Memory
    # ==========================


    memory_manager.add_message(
        "user",
        user_input
    )



    # ==========================
    # Runtime Context
    # ==========================


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



    # ==========================
    # Retriever
    # ==========================


    print(
        "[Pipeline] 1/5. Running Retriever filtering..."
    )


    retrieved_data = retriever.retrieve(
        user_context
    )



    # ==========================
    # Context Builder
    # ==========================


    print(
        "[Pipeline] 2/5. Building unified Context Object..."
    )


    context_object = context_builder.build(
        user_context=user_context,
        retrieved_data=retrieved_data
    )



    # ==========================
    # Prompt Builder
    # ==========================


    print(
        "[Pipeline] 3/5. Rendering final System Prompt..."
    )


    final_prompt = prompt_builder.build(
        context_object
    )



    # ==========================
    # LLM
    # ==========================


    print(
        "[Pipeline] 4/5. Dispatching payload to LLM Client..."
    )


    system_instruction = (

        "你是 AI World OS 的世界运行核心控制台。"

        "请结合世界数据、角色设定、"
        "历史记忆和当前世界状态推进剧情。"

        "保持世界连续性。"

        "不要虚构不存在的系统错误。"

        "不要向玩家暴露API、代码、服务器细节。"

    )



    ai_response = llm_client.generate_response(
        prompt=final_prompt,
        system_instruction=system_instruction
    )



    # ==========================
    # Save Assistant Memory
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
    # Long Term Memory
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



    # ==========================
    # Output
    # ==========================


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
