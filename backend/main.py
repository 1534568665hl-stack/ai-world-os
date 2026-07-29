import os
import sys
from datetime import datetime

# 确保以模块化方式运行时，可以正确索引到根目录及各类子包
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from world_loader import WorldLoader
from backend.core.retriever import Retriever
from backend.core.context_builder import ContextBuilder
from backend.core.prompt_builder import PromptBuilder
from backend.llm.client import LLMClient

def main():
    print("====== 🤖 Welcome to AI World OS (Terminal Engine v1.0) ======")
    
    # 1. 初始化 WorldLoader，指向项目根目录下的 world 文件夹
    world_dir = "./world"
    if not os.path.exists(world_dir):
        print(f"❌ 错误: 找不到世界数据目录 '{world_dir}'。请确保在项目根目录下运行程序。")
        return
        
    print("[System] Loading world entities...")
    loader = WorldLoader(world_base_path=world_dir)
    
    # 2. 加载所有世界实体
    entities = loader.load_all()
    print(f"[System] Successfully loaded {len(entities)} world entities.")
    
    # 3. 初始化核心中游组件
    retriever = Retriever(entities=entities)
    context_builder = ContextBuilder()
    prompt_builder = PromptBuilder()
    llm_client = LLMClient()
    
    # 4. 接收终端用户输入
    print("\n--------------------------------------------------------------")
    user_input = input("请输入你想对这个世界说的话/做出的行动:\n> ")
    if not user_input.strip():
        print("[System] 输入不能为空，程序退出。")
        return
        
    # 5. 构造实时运行状态 (Runtime Context)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # 第一版默认留空环境状态，依靠消息体内的文本触发 Retriever 的关键词与标签命中
    user_context = {
        "message": user_input,
        "time": current_time,
        "current_location": "", 
        "active_npc": []
    }
    
    print("\n[Pipeline] 1/5. Running Retriever filtering...")
    # 6. 调用 Retriever 过滤相关实体
    retrieved_data = retriever.retrieve(user_context)
    
    print("[Pipeline] 2/5. Building unified Context Object...")
    # 7. 调用 ContextBuilder 组装统一上下文
    context_object = context_builder.build(
        user_context=user_context, 
        retrieved_data=retrieved_data
    )
    
    print("[Pipeline] 3/5. Rendering final System Prompt...")
    # 8. 调用 PromptBuilder 渲染状态文本
    final_prompt = prompt_builder.build(context_object)
    
    print("[Pipeline] 4/5. Dispatching payload to LLM Client...")
    # 9. 调用 LLMClient 与大模型安全收发通信
    system_instruction = (
        "你是 AI World OS 的世界运行核心控制台。请结合给定的世界数据、"
        "角色特征与运行状态，以极具沉浸感和逻辑严密性的文字驱动接下来的剧情发展。"
    )
    ai_response = llm_client.generate_response(
        prompt=final_prompt,
        system_instruction=system_instruction
    )
    
    # 10. 打印最终 AI 的世界线演进回复
    print("[Pipeline] 5/5. Execution complete. Response received:\n")
    print("====== 🌌 AI WORLD OS RESPONSE ======")
    print(ai_response)
    print("=====================================")

if __name__ == "__main__":
    main()
