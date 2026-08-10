# -*- coding: utf-8 -*-

import os
import sys


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
from backend.core.state_updater import StateUpdater

from backend.core.event_detector import EventDetector
from backend.core.relation_updater import RelationUpdater
from backend.core.event_memory import EventMemoryManager

from backend.core.time_manager import TimeManager
from backend.core.world_event_manager import WorldEventManager

from backend.core.player_action import PlayerActionProcessor
from backend.core.player_runtime import PlayerRuntime
from backend.core.world_runtime import WorldRuntime

from backend.core.world_controller import WorldController
from backend.core.runtime_response import RuntimeResponse


class _RetrieverContextBuilder:
    """
    保持 Retriever 接入 Controller 流程
    """

    def __init__(
        self,
        context_builder,
        retriever,
        world_state
    ):
        self.context_builder = context_builder
        self.retriever = retriever
        self.world_state = world_state


    def build(
        self,
        user_context,
        retrieved_data
    ):

        merged_context = dict(user_context)

        if not merged_context.get("current_location"):
            merged_context["current_location"] = (
                self.world_state.get(
                    "location",
                    ""
                )
            )

        if not merged_context.get("active_npc"):
            merged_context["active_npc"] = (
                self.world_state.get(
                    "active_npc",
                    []
                )
            )


        retrieved = self.retriever.retrieve(
            merged_context
        )


        return self.context_builder.build(
            user_context=merged_context,
            retrieved_data=retrieved
        )



def _build_controller(
    retriever,
    context_builder,
    prompt_builder,
    state_manager,
    event_detector,
    relation_updater,
    time_manager,
    world_event_manager
):

    world_state = state_manager.load()


    player_action = PlayerActionProcessor(
        event_detector=event_detector
    )


    world_runtime = WorldRuntime(
        npc_ids=world_state.get(
            "active_npc",
            []
        ),
        time_manager=time_manager,
        world_event_manager=world_event_manager
    )


    player_runtime = PlayerRuntime(
        player_action_processor=player_action,
        relation_updater=relation_updater,
        world_runtime=world_runtime
    )


    controller_context_builder = _RetrieverContextBuilder(
        context_builder,
        retriever,
        world_state
    )


    return WorldController(
        player_runtime=player_runtime,
        context_builder=controller_context_builder,
        prompt_builder=prompt_builder
    )



def main():

    print(
        "====== 🤖 Welcome to AI World OS (Terminal Engine v1.0) ======"
    )


    world_dir = "./world"


    if not os.path.exists(world_dir):

        print(
            f"错误: 找不到世界数据目录 '{world_dir}'"
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

    state_updater = StateUpdater()

    event_detector = EventDetector()

    relation_updater = RelationUpdater()

    event_memory_manager = EventMemoryManager()


    time_manager = TimeManager()

    time_manager.load()


    world_event_manager = WorldEventManager()



    world_state = state_manager.load()


    world_controller = _build_controller(
        retriever=retriever,
        context_builder=context_builder,
        prompt_builder=prompt_builder,
        state_manager=state_manager,
        event_detector=event_detector,
        relation_updater=relation_updater,
        time_manager=time_manager,
        world_event_manager=world_event_manager
    )


    _ = state_updater
    _ = event_memory_manager



    print("[World State]")

    print(
        f"LOCATION: {world_state.get('location','')}"
    )

    print(
        f"ACTIVE NPC: {world_state.get('active_npc',[])}"
    )


    print("[LLM Config]")

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



    memory_manager.add_message(
        "user",
        user_input
    )



    print(
        "[Pipeline] Running WorldController..."
    )


    controller_result = (
        world_controller.process(
            user_input
        )
    )



    runtime_response = RuntimeResponse(
        player_result=controller_result.get(
            "player_result",
            {}
        ),
        context=controller_result.get(
            "context",
            {}
        ),
        prompt=controller_result.get(
            "prompt",
            ""
        )
    )


    response_data = runtime_response.to_dict()



    system_instruction = (
        "你是 AI World OS 的世界运行核心。\n\n"
        "根据世界数据、NPC资料、地点信息、规则和记忆生成连续世界。\n\n"
        "规则：\n"
        "1. 只能使用提供的数据。\n"
        "2. 不要虚构不存在的信息。\n"
        "3. 不要暴露后台状态。\n"
        "4. NPC必须符合已有设定。\n"
        "5. 保持沉浸式世界模拟风格。\n"
        "6. 不暴露服务器、API和代码细节。"
    )


    print(
        "[Pipeline] Dispatching RuntimeResponse to LLM Client..."
    )


    ai_response = llm_client.generate_response(
        prompt=response_data["prompt"],
        system_instruction=system_instruction
    )



    if ai_response and not ai_response.startswith("Error:"):

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
        "[Pipeline] Execution complete. Response received:\n"
    )

    print(
        "====== 🌌 AI WORLD OS RESPONSE ======"
    )

    print(ai_response)

    print(
        "====================================="
    )



if __name__ == "__main__":

    main()
