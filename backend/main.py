import os
import sys


# ==========================
# UTF-8 淇
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
    """Keep Retriever in the controller path without changing core modules."""

    def __init__(self, context_builder, retriever, world_state):
        self.context_builder = context_builder
        self.retriever = retriever
        self.world_state = world_state

    def build(self, user_context, retrieved_data):
        merged_context = dict(user_context)
        if not merged_context.get("current_location"):
            merged_context["current_location"] = self.world_state.get(
                "location",
                ""
            )
        if not merged_context.get("active_npc"):
            merged_context["active_npc"] = self.world_state.get(
                "active_npc",
                []
            )

        retrieved = self.retriever.retrieve(merged_context)
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
        npc_ids=world_state.get("active_npc", []),
        time_manager=time_manager,
        world_event_manager=world_event_manager
    )
    # time_manager.advance(minutes) is delegated through WorldRuntime.tick().
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
        "====== 馃 Welcome to AI World OS (Terminal Engine v1.0) ======"
    )

    # ==========================
    # System Initialization
    # ==========================

    world_dir = "./world"
    if not os.path.exists(world_dir):
        print(
            f"鉂?閿欒: 鎵句笉鍒颁笘鐣屾暟鎹洰褰?'{world_dir}'"
        )
        return

    print("[System] Loading world entities...")
    loader = WorldLoader(world_base_path=world_dir)
    entities = loader.load_all()
    print(
        f"[System] Successfully loaded {len(entities)} world entities."
    )

    retriever = Retriever(entities=entities)
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

    # Keep existing state/event modules initialized for the runtime boundary.
    _ = state_updater
    _ = event_memory_manager

    print("[World State]")
    print(f"LOCATION: {world_state.get('location', '')}")
    print(f"ACTIVE NPC: {world_state.get('active_npc', [])}")

    print("[LLM Config]")
    print(f"MODEL: {llm_client.model}")
    print(f"BASE_URL: {llm_client.base_url}")
    print("\n--------------------------------------------------------------")

    # ==========================
    # User Input
    # ==========================

    try:
        user_input = input(
            "璇疯緭鍏ヤ綘鎯冲杩欎釜涓栫晫璇寸殑璇?鍋氬嚭鐨勮鍔?\n> "
        )
    except UnicodeDecodeError:
        print("[System] 杈撳叆缂栫爜閿欒锛岃閲嶆柊杈撳叆銆?)
        return

    if not user_input.strip():
        print("[System] 杈撳叆涓嶈兘涓虹┖锛岀▼搴忛€€鍑恒€?)
        return

    # The current user turn is available to ContextBuilder's Memory system.
    memory_manager.add_message("user", user_input)

    # ==========================
    # WorldController
    # ==========================

    print("[Pipeline] Running WorldController...")
    controller_result = world_controller.process(user_input)

    runtime_response = RuntimeResponse(
        player_result=controller_result.get("player_result", {}),
        context=controller_result.get("context", {}),
        prompt=controller_result.get("prompt", "")
    )
    response_data = runtime_response.to_dict()

    # ==========================
    # LLM
    # ==========================

    system_instruction = (
        "浣犳槸 AI World OS 鐨勪笘鐣岃繍琛屾牳蹇冦€?
        "\n\n鏍规嵁涓栫晫鏁版嵁銆丯PC璧勬枡銆佸湴鐐逛俊鎭€佽鍒欏拰璁板繂鐢熸垚杩炵画涓栫晫銆?
        "\n\n瑙勫垯锛?
        "\n1. 鍙兘浣跨敤鎻愪緵鐨勬暟鎹€?
        "\n2. 涓嶈铏氭瀯鏁版嵁搴撲笉瀛樺湪鐨勪俊鎭€?
        "\n3. 涓嶈澹扮О淇敼鍚庡彴鐘舵€併€?
        "\n4. NPC鍙兘渚濇嵁宸叉湁璁惧畾琛屽姩銆?
        "\n5. 淇濇寔娌夋蹈寮忎笘鐣屾ā鎷熼鏍笺€?
        "\n6. 涓嶆毚闇叉湇鍔″櫒銆丄PI銆佷唬鐮佺粏鑺傘€?
    )

    print("[Pipeline] Dispatching RuntimeResponse to LLM Client...")
    ai_response = llm_client.generate_response(
        prompt=response_data["prompt"],
        system_instruction=system_instruction
    )

    if ai_response and not ai_response.startswith("Error:"):
        memory_manager.add_message("assistant", ai_response)

    memories = memory_extractor.extract(user_input)
    for memory in memories:
        memory_manager.save_entity_memory(
            "player",
            memory["content"],
            memory["importance"]
        )

    print("[Pipeline] Execution complete. Response received:\n")
    print("====== 馃寣 AI WORLD OS RESPONSE ======")
    print(ai_response)
    print("=====================================")


if __name__ == "__main__":
    main()
