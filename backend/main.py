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



# ==========================
# World State Update
# ==========================

def update_world_state(
    state_manager,
    user_input,
    world_state
):

    rules = {

        "暖阳角落":
        {
            "location":
                "L_Warm_Corner",

            "active_npc":
                [
                    "momo"
                ]
        },


        "咖啡店":
        {
            "location":
                "L_Warm_Corner",

            "active_npc":
                [
                    "momo"
                ]
        },


        "沫沫":
        {
            "location":
                "L_Warm_Corner",

            "active_npc":
                [
                    "momo"
                ]
        }

    }



    for keyword, data in rules.items():

        if keyword in user_input:

            print(
                f"[State] Trigger matched: {keyword}"
            )


            new_state = state_manager.update(
                **data
            )


            print(
                "[State] Saved:"
            )


            print(
                new_state
            )


            return new_state



    print(
        "[State] No update triggered."
    )


    return world_state





def main():


    print(
        "====== 🤖 Welcome to AI World OS (Terminal Engine v1.0) ======"
    )



    # ==========================
    # Load World
    # ==========================


    world_dir = "./world"


    if not os.path.exists(world_dir):

        print(
            f"❌ 找不到世界目录: {world_dir}"
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
    # Modules
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



    print(
        "[State File]"
    )


    print(
        state_manager.path
    )



    # ==========================
    # Current State
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
            "输入编码错误"
        )

        return



    if not user_input.strip():

        return



    # ==========================
    # Update State
    # ==========================


    world_state = update_world_state(
        state_manager,
        user_input,
        world_state
    )



    print(
        "[DEBUG] Current State:"
    )

    print(
        world_state
    )



    # ==========================
    # Memory
    # ==========================


    memory_manager.add_message(
        "user",
        user_input
    )



    # ==========================
    # Context
    # ==========================


    user_context = {

        "message":
            user_input,

        "time":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M"
            ),

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
        user_context,
        retrieved_data
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



    system_instruction = """

你是 AI World OS 世界运行核心。

规则：

1. World 数据是真实来源。
2. 禁止创造不存在的NPC和地点。
3. 不允许声称修改后台数据库。
4. 保持世界状态连续。
5. 不暴露代码、API、服务器。

"""



    ai_response = llm_client.generate_response(
        final_prompt,
        system_instruction
    )



    if (
        ai_response
        and
        not ai_response.startswith("Error:")
    ):

        memory_manager.add_message(
            "assistant",
            ai_response
        )



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
        "[Pipeline] 5/5. Execution complete."
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
