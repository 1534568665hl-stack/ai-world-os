AI World OS

AI World OS 是一个面向连续世界模拟的模块化运行时。它把世界实体、地点状态、NPC 关系、事件记忆、世界时间和 NPC 日程组合成统一上下文，再交给 LLM 生成当前场景的回应。

本项目仍处于早期迭代阶段，但基础运行链路已经可以工作。主人可以从终端启动一次世界回合，输入玩家行动，并观察状态、关系、事件和时间如何被保存下来。

## 当前进度

当前开发节点已经完成以下最小可运行能力：

- WorldLoader：加载 `world/` 下的 NPC、地点、物品和规则实体。
- Retriever：根据运行时地点和活动 NPC 过滤相关世界数据。
- StateManager：持久化 `memory/world_state.json`。
- StateUpdater：识别地点和 NPC 别名，并使用真实实体 ID，例如 `N_Momo`。
- RelationManager：读取地点关系文件中的默认 NPC 关系。
- RelationUpdater：根据玩家事件更新运行时关系，不覆盖世界模板。
- EventDetector：使用纯 Python 规则检测帮助、交流、赠送和冲突事件。
- EventMemoryManager：保存事件并提供最近事件查询。
- TimeManager：持久化世界时间，支持初始化、读取、保存和分钟级推进。
- ContextBuilder：合并运行时、世界、记忆、关系、事件和 NPC 状态。
- PromptBuilder：将当前地点、NPC、关系、事件、世界时间和 NPC 日程状态注入最终 Prompt。
- ScheduleManager：读取 NPC `schedule.json`，按世界时间解析当前活动和地点。
- MemoryManager：保存短期对话记忆和长期实体记忆。

当前阶段的重点是保持模块之间的边界清晰，采用最小增量方式继续扩展世界模拟能力。版本号暂不人为跳跃，以代码和测试实际状态为准，哼。

## 运行链路

一次终端回合的主要数据流如下：

```text
程序启动
  ↓
TimeManager.load()
  ↓
读取玩家输入
  ↓
EventDetector.detect()
  ↓
EventMemoryManager.save_event()
  ↓
RelationUpdater.update()
  ↓
TimeManager.advance()
  ↓
StateUpdater.detect()
  ↓
StateManager.update()
  ↓
Retriever.retrieve()
  ↓
ContextBuilder.build()
  ↓
PromptBuilder.build()
  ↓
LLMClient.generate_response()
```

没有识别到事件时，会跳过事件记忆、关系更新和事件驱动的时间推进，原有上下文生成流程继续执行。

## 核心目录

```text
ai-world-os/
├── backend/
│   ├── main.py
│   ├── api.py
│   ├── core/
│   │   ├── world_loader.py
│   │   ├── retriever.py
│   │   ├── state_manager.py
│   │   ├── state_updater.py
│   │   ├── relation_manager.py
│   │   ├── relation_updater.py
│   │   ├── event_detector.py
│   │   ├── event_memory.py
│   │   ├── time_manager.py
│   │   ├── schedule_manager.py
│   │   ├── context_builder.py
│   │   ├── prompt_builder.py
│   │   ├── memory_manager.py
│   │   ├── memory_extractor.py
│   │   └── llm/client.py
│   └── tests/
├── world/
│   ├── npc/
│   ├── location/
│   ├── item/
│   └── rule/
├── memory/
├── .env
└── README.md
```

## 世界数据

世界数据以实体目录组织。实体通常由以下文件描述：

```text
world/<category>/<entity>/
├── info.json
├── tags.json
└── description.md
```

目前已有的基础实体包括：

- NPC：沫沫，实体 ID 为 `N_Momo`。
- 地点：暖阳角落咖啡店，实体 ID 为 `L_Warm_Corner`。
- 物品和规则：由 `world/item/` 与 `world/rule/` 中的实体提供。

关系默认值从地点关系文件读取，例如：

```text
world/location/warm_corner/relations.json
```

运行时关系保存到 `memory/relations/`，因此不会修改 NPC 或地点的原始世界模板。

## 运行时数据

运行过程中会使用以下文件保存可持续状态：

```text
memory/
├── world_state.json
├── world_time.json
├── conversations/
│   └── current.json
├── events/
│   └── current.json
├── relations/
│   └── player_<npc_id>.json
└── long_term/
    └── <entity_id>.json
```

这些文件属于运行时数据，不应被当作世界模板。尤其是 `memory/conversations/current.json`，它保存短期对话连续性，测试时可以保留，也可以在明确需要时单独清理。

## 事件与关系

`EventDetector` 当前支持以下基础事件：

| 事件 | 示例关键词 | 默认影响 |
| --- | --- | --- |
| `help` | 帮助、帮忙、修理、解决、协助、救 | trust `+5`，familiarity `+2` |
| `chat` | 你好、聊天、聊聊、说话、交流 | familiarity `+1` |
| `gift` | 送你、礼物、赠送、给你 | trust `+3` |
| `conflict` | 讨厌、生气、争吵、攻击 | trust `-5` |

玩家对沫沫的称呼 `沫沫`、`momo`、`Momo`、`MOMO` 和 `N_Momo` 会统一解析到真实实体 ID `N_Momo`。运行时关系示例：

```json
{
  "npc": "N_Momo",
  "player": "player",
  "relationship": {
    "trust": 5,
    "familiarity": 2,
    "emotion": "positive"
  }
}
```

## 世界时间

`TimeManager` 使用 `memory/world_time.json` 保存世界时间。首次运行时，如果文件不存在，会以当前现实时间初始化；事件发生后按事件类型推进：

| 事件 | 时间推进 |
| --- | --- |
| `chat` | 5 分钟 |
| `help` | 30 分钟 |
| `gift` | 10 分钟 |
| `conflict` | 20 分钟 |

上下文中的时间结构为：

```json
{
  "date": "2026-08-07",
  "time": "09:30:00",
  "period": "morning"
}
```

## NPC 日程

`ScheduleManager` 支持从 NPC 目录读取可选的 `schedule.json`，并根据世界时间返回当前活动和地点：

```text
world/npc/<npc>/schedule.json
```

文件示例：

```json
{
  "schedule": [
    {
      "start": "08:00",
      "end": "12:00",
      "activity": "work",
      "location": "L_Warm_Corner"
    },
    {
      "start": "18:00",
      "end": "22:00",
      "activity": "rest",
      "location": "catnip_apt_302"
    }
  ]
}
```

如果某个 NPC 尚未配置 `schedule.json`，系统会返回空的活动和地点，不会阻塞主链路。当前仓库已经具备日程解析模块和测试；后续只需按既有世界数据约定补充具体 NPC 日程即可。

## 安装与运行

建议从项目根目录执行命令：

```bash
python -m pip install requests python-dotenv
python -m backend.main
```

仓库当前未提供 `requirements.txt`，因此依赖按运行环境自行安装。若只运行不触发 LLM 的单元测试，可直接执行下方测试命令。

主程序依赖项目根目录下的 `world/` 和 `memory/`，从其他目录启动可能导致相对路径无法正确定位，因此请在仓库根目录运行。

环境变量可以放在项目根目录的 `.env` 中，LLM 客户端会读取模型和服务地址配置。不要把真实 API Key 提交到仓库。

## 测试与编译检查

运行全部测试：

```bash
python -m unittest discover -s backend/tests -v
```

执行 Python 编译检查：

```bash
python -m compileall -q backend
```

测试覆盖当前的事件检测、事件记忆、关系更新、世界时间、时间上下文和 NPC 日程解析。成功时相关测试会输出：

```text
SCHEDULE_MANAGER_OK
TIME_CONTEXT_OK
PY_COMPILE_OK
```

## 当前限制与后续方向

- 当前 EventDetector 使用关键词规则，尚未覆盖复杂语义、否定句和多目标事件。
- 当前 ScheduleManager 已支持读取和解析日程，但具体 NPC 是否有日程取决于世界目录中是否存在对应 `schedule.json`。
- 关系和事件已经持久化，但尚未实现更复杂的衰减、冲突解决和多玩家隔离策略。
- Retriever 当前是结构化过滤器，向量检索、数据库存储和更复杂的记忆召回仍可独立扩展。
- `backend/main.py` 是当前主要的终端入口；API 入口仍属于早期接口，需结合部署环境补齐依赖与校验。

后续扩展应优先保持现有数据结构、实体 ID 和模块 API 兼容，避免为了单个功能重写主运行链路。

## 设计原则

1. 世界模板与运行时状态分离。
2. 所有 NPC、地点和物品优先使用真实实体 ID。
3. 底层状态检测采用确定性规则，不依赖 LLM。
4. 上下文统一由 `ContextBuilder` 组装，再由 `PromptBuilder` 渲染。
5. 新功能采用独立模块和最小接入，保持 Python 3.6 兼容。
