import os
import sys
from datetime import datetime


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



def main():

    print(
        "====== 🤖 Welcome to AI World OS (Terminal Engine v1.0) ======"
    )


    # ==========================
    # 初始化
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



    retriever = Retriever(
        entities=entities
    )


    context_builder = ContextBuilder()


    prompt_builder = PromptBuilder()


    llm_client = LLMClient()


    memory_manager = MemoryManager()


    memory_extractor = MemoryExtractor()



    # ==========================
    # 输入
    # ==========================

    print(
        "\n--------------------------------------------------------------"
    )


    user_input = input(
        "请输入你想对这个世界说的话/做出的行动:\n> "
    )


    if not user_input.strip():

        print(
            "[System] 输入不能为空，程序退出。"
        )

        return



    # ==========================
    # 保存玩家输入
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
            "",

        "active_npc":
            []

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
    # Context
    # ==========================

    print(
        "[Pipeline] 2/5. Building unified Context Object..."
    )


    context_object = context_builder.build(
        user_context=user_context,
        retrieved_data=retrieved_data
    )



    # ==========================
    # Prompt
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

        "请结合给定的世界数据、角色特征、"
        "历史记忆与运行状态，"

        "以沉浸式且符合逻辑的方式推进世界。"

    )


    ai_response = llm_client.generate_response(
        prompt=final_prompt,
        system_instruction=system_instruction
    )



    # ==========================
    # 保存AI回复
    # ==========================

    if not ai_response.startswith("Error:"):

        memory_manager.add_message(
            "assistant",
            ai_response
        )

    else:

        print(
            "[Memory] Skip saving failed LLM response."
        )



    # ==========================
    # 提取长期记忆
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
    # 输出
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
