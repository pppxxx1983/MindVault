# GameRuntime 项目文档

> **版本**: v0.6.0  
> **最后更新**: 2026-04-27  
> **GitHub**: https://github.com/pppxxx1983/GameRuntime  
> **许可证**: MIT

---

## 📋 一、项目概览

GameRuntime 是一个**基于 GameState 的游戏运行时与自动化引擎**，将游戏自动化拆分为四层核心管线：

```
感知 (Perception) → 状态 (StateFusion) → 事件 (EventEngine) → 决策与执行 (AgentOrchestrator)
```

### 核心特性

| 特性 | 说明 |
|------|------|
| **多模态感知** | OCR / YOLO / VLM / Simulator 产生 Observation |
| **状态融合** | StateFusion 把多源观测融合成统一 GameState |
| **事件驱动** | EventEngine 从状态变化生成 Event |
| **技能系统** | AgentOrchestrator 选择技能并执行 |
| **三种模式** | observe（只观察）/ assist（建议+ 确认）/ auto（自动执行） |

### 当前完成度

| 模块 | 状态 | 说明 |
|------|------|------|
| 核心状态与事件链路 | ✅ 已完成 | GameState / StateFusion / EventEngine |
| 技能与调度 | ✅ 已完成 | AgentOrchestrator + 技能注册表 |
| Mock / Simulator 闭环 | ✅ 已完成 | 可无设备运行 |
| FastAPI / WebSocket 服务 | ✅ 已完成 | REST + Editor / Phone WS |
| Editor 监控台 | ✅ 已完成 | NiceGUI 仪表盘 |
| KnowledgeGap 闭环 | ✅ 已完成 | resolve / research / validate |
| 测试基线 | ✅ 已完成 | 119 个测试通过 |
| 代码质量基线 | ✅ 已完成 | 关键改动 ruff 通过 |
| 真实设备感知 | 🚧 部分完成 | 需要模型文件 / API Key / Android 端配合 |
| Android 客户端产品化 | 🚧 部分完成 | 基础链路存在，仍需 UI 和发布完善 |

---

## 🏗️ 二、系统架构

### 2.1 整体架构图

```
┌─────────────┐     ScreenSync      ┌──────────────────────┐
│  Android APK │ ◄════════════════► │                      │
│  (Kotlin)    │    WebSocket        │   GameRuntime Engine  │
└─────────────┘                     │   (FastAPI + Python)  │
                                     │                      │
┌─────────────┐    WebSocket        │  ┌──────────────────┐ │
│    Editor    │ ◄════════════════► │  │   GameState       │ │
│  (NiceGUI)   │    实时状态/控制     │  │   (核心状态对象)   │ │
└─────────────┘                     │  └─────────────────┘ │
                                     │           │           │
                                     │  ┌────────▼─────────┐ │
                                     │  │  PerceptionLayer  │ │
                                     │  │  OCR/YOLO/VLM/Sim │ │
                                     │  └────────┬─────────┘ │
                                     │           │           │
                                     │  ┌────────▼─────────┐ │
                                     │  │   StateFusion     │ │
                                     │  │  (多源加权融合)    │ │
                                     │  └────────┬─────────┘ │
                                     │           │           │
                                     │  ┌────────▼─────────┐ │
                                     │  │   EventEngine     │ │
                                     │  │  (状态变化→事件)  │ │
                                     │  └────────┬─────────┘ │
                                     │           │           │
                                     │  ┌────────▼─────────┐ │
                                     │  │ AgentOrchestrator │ │
                                     │  │  (事件→技能映射)  │ │
                                     │  └────────┬─────────┘ │
                                     │           │           │
                                     │  ┌────────▼─────────┐ │
                                     │  │  Skill + Adapter  │ │
                                     │  │  (技能执行层)     │ │
                                     │  └──────────────────┘ │
                                     └──────────────────────┘
```

### 2.2 三种运行模式

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| **observe** | 只观察，不执行任何操作 | 调试、监控 |
| **assist** | 建议操作，等待用户确认后执行（默认） | 人机协作 |
| **auto** | 白名单技能自动执行，高风险需确认 | 全自动运行 |

---

## 📁 三、项目结构

```text
GameRuntime/
├── engine/                     # Python 引擎核心
│   ├── main.py                 # 统一入口 (--mock/--mode/--config/--profile)
│   ├── api/
│   │   └── server.py           # FastAPI + WebSocket 服务器
│   ├── core/
│   │   ├── schemas/            # Pydantic 数据模型
│   │   │   ├── game_state.py   # GameState 核心状态
│   │   │   ├── event.py        # Event 事件对象
│   │   │   ├── observation.py  # Observation 感知输出
│   │   │   └── knowledge_gap.py # KnowledgeGap 知识缺口
│   │   ├── state_fusion.py     # 多源状态融合
│   │   └── event_engine.py     # 事件触发引擎
│   ├── perception/
│   │   ├── manager.py          # 感知管理器 (统一调度 OCR/YOLO/VLM/Sim)
│   │   ├── fusion.py           # 加权融合引擎
│   │   ├── simulator.py        # Mock 感知模拟器 (状态机驱动)
│   │   ├── paddleocr_adapter.py # PaddleOCR 适配器
│   │   └── yolo_adapter.py     # YOLOv8 适配器
│   ├── agent/
│   │   ├── orchestrator.py     # Agent 调度中枢
│   │   ├── skills/             # 技能系统
│   │   │   ├── base_skill.py   # Skill 基类 + SkillResult
│   │   │   ├── registry.py     # 技能注册表
│   │   │   └── game_skills.py  # 通用技能实现
│   │   ├── execution/
│   │   │   └── execution_adapter.py # 执行适配器 (ADB/Hub)
│   │   ├── vlm_client.py       # GLM-4V VLM
│   │   ├── qwen_vlm_client.py  # Qwen-VL
│   │   ├── kimi_vlm_client.py  # Kimi VL
│   │   └── deepseek_vlm_client.py # DeepSeek VL2
│   ├── knowledge/
│   │   └── gap_manager.py      # 知识缺口管理器
│   ├── storage/
│   │   └── datastore.py        # SQLite 数据存储 (WAL 模式)
│   ├── observability/
│   │   └── metrics.py          # 指标收集器
│   ├── profiles/
│   │   └── loader.py           # 游戏 Profile 加载器
│   ├── runtime/
│   │   └── config_loader.py    # 统一配置加载 (${VAR} 插值)
│   ├── utils/
│   │   ├── log_manager.py      # 线程安全日志管理器
│   │   └── logging.py          # JSON 格式日志
│   └── adapters/               # 适配器层 (预留)
│
├── editor/                     # NiceGUI 监控台
│   ├── app.py                  # 主入口
│   ├── ws_client.py            # WebSocket 客户端 (异步)
│   ├── pages/
│   │   ├── dashboard.py        # 仪表盘主页面
│   │   └── frame_analyzer.py   # 帧分析调试页面
│   └── components/
│       └── ui_base.py          # StatusBadge / MetricCard 组件
│
├── android/                    # Android 客户端 (Kotlin)
│   ├── screensync/             # ScreenSync 连接管理
│   ├── capture/                # MediaProjection 屏幕捕获
│   ├── control/                # RemoteGestureService 远程手势
│   ├── diff/                   # 帧差检测
│   ├── encode/                 # WebP 区域编码
│   ├── pipeline/               # ScreenSync 管道
│   ├── protocol/               # 协议消息定义
│   └── ui/                     # Activity / Fragment
│
├── vendor/screensync/          # ScreenSync 协议 Python 实现
│   ├── messages.py             # 协议消息类型
│   ├── phone_client.py         # 设备端 WS 客户端
│   ├── registry.py             # 远程客户端注册表
│   └── reconnect.py            # 指数退避重连策略
│
├── profiles/game/
│   ├── profile.yaml            # 游戏配置模板
│   └── mock_scenario.yaml      # Mock 场景模板
│
├── config.yaml                 # 主配置文件
├── scripts/
│   ├── run.py                  # 服务管理器 (Windows)
│   ├── download_model.py       # YOLO 模型下载
│   └── help.py                 # 控制台帮助
├── tests/
│   ├── test_game_runtime.py    # 核心模块测试
│   ├── test_architecture.py    # 架构契约测试
│   └── test_mock_mode.py       # Mock 模式集成测试
└── data/
    ├── game.db                 # SQLite 数据库
    ├── frames/                 # 帧缓存
    └── logs/                   # 运行日志
```

---

## 🔄 四、核心数据流

### 4.1 主处理循环

```
帧注入 (Mock/手机)
    │
    ▼
_frame_queue (asyncio.Queue, maxsize=10)
    │
    ▼
_perception_worker() ──► PerceptionManager.perceive(frame)
    │                        │
    │                   ┌────┴────┐
    │                   │ Sim?    │ 真实感知
    │                   │simulator│ OCR + YOLO + VLM
    │                   └────┬────┘
    │                        │
    │                   list[Observation]
    │                        │
    ▼                        ▼
_process_frame() ────► StateFusion.fuse_observations()
                         │
                         ▼
                    GameState (updated)
                         │
                    ┌────┴────┐
                    │         │
               EventEngine  _broadcast_to_editors()
                    │
                    ▼
               list[Event]
                    │
                    ▼
          AgentOrchestrator.on_event()
                    │
                    ▼
              ActionPlan (intent + skill)
                    │
               ┌────┴────┐
               │ assist? │ auto?
               │ 等确认  │ 直接执行
               └────┬────┘
                    │
                    ▼
             Skill.execute(state, args)
                    │
                    ▼
              ExecutionAdapter (ADB/Hub)
                    │
                    ▼
              SkillResult → GapManager (失败时)
```

### 4.2 数据模型关系

| 模型 | 作用 | 关键字段 |
|------|------|----------|
| **Observation** | 感知输出 | obs_type (OCR/YOLO/VLM), confidence, source, bbox, text |
| **GameState** | 唯一状态源 | player, ui, world, inventory, system_confidence, extra |
| **Event** | 状态变化触发 | event_type, priority, reason, dedupe_key |
| **ActionPlan** | 技能执行计划 | skill_name, confidence, requires_confirmation, args |
| **KnowledgeGap** | 知识缺口 | gap_type, status, question, answer, validated_at |

---

## 🎯 五、核心模块详解

### 5.1 GameState (`engine/core/schemas/game_state.py`)

系统唯一的状态核心，Pydantic BaseModel。

| 子模型 | 字段 | 说明 |
|--------|------|------|
| **PlayerState** | level, health, energy, currency, stuck | 玩家状态 |
| **UIState** | main_screen_type, modal_dialog_present, loading | UI 状态 |
| **WorldState** | in_combat, current_location, combat_result | 世界状态 |
| **InventoryState** | capacity, is_full, key_items | 背包状态 |
| **SystemConfidence** | overall, fields, conflicting_sources | 置信度 |
| **extra** | dict | 游戏特定数据 |

### 5.2 PerceptionManager (`engine/perception/manager.py`)

统一调度感知层，支持两种模式：

- **Mock 模式**：使用 Simulator 生成模拟观测（状态机驱动，支持场景转换）
- **真实感知**：PaddleOCR (文字) + YOLOv8 (检测) + VLM (视觉理解)

配置驱动：`config.yaml → perception.use_simulator`

### 5.3 StateFusion (`engine/core/state_fusion.py`)

将多个 Observation 融合为一个 GameState：

- 多源加权融合（权重从 config.yaml 读取）
- 冲突检测（差异超过阈值时记录）
- 屏幕类型优先级（COMBAT > LOADING > DIALOG > SHOP > ...）
- Observation 历史记录（审计性）

### 5.4 EventEngine (`engine/core/event_engine.py`)

从 GameState 变化产生 Event：

- 10 条默认规则（能量低、战斗开始/结束、弹窗、界面变化等）
- 去重冷却（按事件类型区分冷却时间）
- 事件处理器注册

### 5.5 AgentOrchestrator (`engine/agent/orchestrator.py`)

事件到技能的映射中枢：

- 事件 → ActionPlan（意图 + 技能名 + 参数）
- Profile 白名单控制 Auto 模式自动执行的技能
- 感知质量检查（置信度低时降级或创建 Gap）
- Gap 回调：执行失败时自动创建 KnowledgeGap

### 5.6 Skill 系统 (`engine/agent/skills/`)

| 技能 | 风险等级 | 说明 |
|------|----------|------|
| `ui.close_modal` | safe | 关闭弹窗 |
| `ui.press_back` | safe | 返回 |
| `combat.collect_reward` | medium | 领取奖励 |
| `combat.retry` | medium | 重试战斗 |
| `player.use_sanity_potion` | high | 使用体力药 |
| `quest.complete` | medium | 完成任务 |

### 5.7 GapManager (`engine/knowledge/gap_manager.py`)

知识缺口管理：

- 创建/更新/查询 Gap
- 持久化到 SQLite
- 回调通知（新 Gap 创建时广播给 Editor）

---

## 📡 六、通信协议

### 6.1 ScreenSync (Android ↔ Engine)

基于 WebSocket 的二进制协议，从 GameTools C# 移植。

**消息类型**:
- Phone → Server: hello, frame_delta, heartbeat, command, error
- Server → Editor: phone_connected, frame_delta, command_result
- Editor → Server: editor_pointer, editor_command, heartbeat

**握手流程**: `hello → hello_ack → frame_ack → phone_connected`

### 6.2 Engine ↔ Editor WebSocket

JSON 消息，Engine 在 `/ws/editor` 端点：

```json
// Engine → Editor
{"type": "state_updated", "state": {...}}
{"type": "event_triggered", "event": {...}}
{"type": "action_plan", "plan": {...}}
{"type": "skill_result", "result": {...}}
{"type": "gap_created", "gap": {...}}
{"type": "perception_status", "status": {...}}

// Editor → Engine
{"type": "confirm_action", "plan_id": "..."}
{"type": "reject_action", "plan_id": "..."}
{"type": "manual_correction", "field": "...", "value": "..."}
{"type": "set_run_mode", "mode": "assist"}
```

### 6.3 REST API

| 端点 | 方法 | 说明 |
|------|------|------|
| `/health` | GET | 健康检查 |
| `/state` | GET | 当前 GameState |
| `/events` | GET | 最近事件 |
| `/skills` | GET | 已注册技能 |
| `/gaps` | GET | 知识缺口 |
| `/frames` | GET | 最近帧信息 |
| `/mode` | POST | 切换运行模式 |

**认证**: `X-API-Key` Header（未配置时免认证）

---

## ⚙️ 七、配置系统

### 7.1 配置优先级

```
CLI 参数 > 环境变量 > config.yaml > 内置默认值
```

### 7.2 环境变量插值

config.yaml 支持 `${VAR}` 和 `${VAR:-default}` 语法：

```yaml
perception:
  use_simulator: ${USE_SIMULATOR:-false}
llm:
  api_key: ${LLM_API_KEY:-}
```

### 7.3 Profile 系统

`profiles/game/profile.yaml` 定义游戏特定配置：

- `known_regions`: UI 区域坐标（按钮位置等）
- `skill_whitelist_auto`: Auto 模式自动执行的技能
- `event_rules`: 自定义事件规则
- `capture_adapter` / `execution_adapter`: 适配器选择

### 7.4 核心配置项

```yaml
# 运行时配置
runtime:
  default_mode: assist
  profile_path: profiles/game/profile.yaml
  mock_mode: false
  execution_countdown_seconds: 3

# 感知层配置
perception:
  use_simulator: false
  frame_diff_threshold: 0.05
  ocr:
    engine: paddleocr
    lang: ch
  detection:
    engine: yolov8
    model_path: models/game_yolo.pt
  vlm:
    engine: ollama
    model: qwen3-vl:8b

# LLM 配置
llm:
  provider: ollama
  api_key: ollama
  base_url: http://localhost:11434/v1
  model: qwen3-vl:8b

# 安全配置
safety:
  block_high_risk_auto: true
  confirm_medium_risk: true
  auto_skill_whitelist:
    - ui.close_modal
    - ui.press_back
    - combat.collect_reward
```

---

## 🚀 八、快速开始

### 8.1 安装

```bash
# 基础安装
pip install -e .

# 开发依赖
pip install -e ".[dev]"

# Editor 依赖
pip install -e ".[editor]"
```

### 8.2 启动 Mock 模式（推荐）

```bash
# 方式 1: 直接启动
python -m engine.main --mock

# 方式 2: 使用管理脚本
python manage.py restart-engine --mock
```

默认地址：
- API: `http://localhost:8000`
- Health: `http://localhost:8000/health`

### 8.3 启动 Editor

```bash
python editor/app.py
```

默认地址：
- Editor: `http://localhost:8501`

### 8.4 运行测试

```bash
python -m pytest -q
```

### 8.5 常用命令

```bash
# Mock 闭环
python -m engine.main --mock

# 指定运行模式
python -m engine.main --mode assist
python -m engine.main --mode auto

# 指定配置
python -m engine.main --config configs/dev.yaml
python -m engine.main --config configs/mock.yaml

# 指定 profile
python -m engine.main --profile profiles/game/profile.yaml

# 运行测试
python -m pytest -q
```

---

## 🧪 九、测试

| 测试文件 | 覆盖范围 | 测试数量 |
|----------|----------|----------|
| `test_game_runtime.py` | StateFusion, EventEngine, Orchestrator, Perception | ~30 |
| `test_architecture.py` | 事件 - 技能契约，配置加载，API 安全策略 | ~8 |
| `test_mock_mode.py` | Mock 感知，全链路集成 | ~15 |

**总计**: 119 个测试通过

**运行测试**:
```bash
# 全部测试
pytest tests/ -v

# Mock 模式专项测试
pytest tests/test_mock_mode.py -v

# 特定测试类
pytest tests/test_game_runtime.py::TestStateFusion -v
```

---

##  十、部署

### 10.1 Docker

```bash
# 生产环境
docker-compose up engine editor

# 开发环境（挂载源码）
docker-compose --profile dev up dev

# 含 Redis 缓存
docker-compose --profile cache up
```

### 10.2 数据持久化

| 路径 | 说明 |
|------|------|
| `data/game.db` | SQLite 数据库 |
| `data/frames/` | 帧缓存 |
| `logs/` | 运行日志 |

---

## 📊 十一、工程路线图

### M1: Stable Runtime Base（基本完成）

- ✅ 保持启动流程一致
- ✅ 保持 Mock 模式确定性
- ✅ 保持测试和运行时质量稳定
- 🔄 继续减少服务层重复代码

### M2: Better Operational Surface（进行中）

- 🔄 改进可观测性和诊断
- 🔄 增强 Editor 检查流程
- 🔄 改进 Android 客户端文档和集成流程
- 🔄 保持配置和 profile 行为明确

### M3: Planner and Agent Expansion（未开始）

- ⏳ 更清晰的规划器边界
- ⏳ 更丰富的任务/目标抽象
- ⏳ 更可控的 VLM 降级策略
- ⏳ 更强的执行历史和知识反馈使用

---

## ⚠️ 十二、已知限制

1. **真实 OCR / YOLO / VLM** 依赖外部模型、环境或 API Key
2. **Android 端** 虽然协议链路存在，但仍未整理成完整的面向发布版本的客户端文档与流程
3. **历史归档文档** 仍保存在 `docs/old/`，仅供追溯，不作为当前事实来源

---

## 📚 十三、文档索引

| 文档 | 说明 |
|------|------|
| [README.md](../README.md) | 项目概览 |
| [ARCHITECTURE.md](../docs/ARCHITECTURE.md) | 架构说明 |
| [API.md](../docs/API.md) | API 文档 |
| [RUNBOOK.md](../docs/RUNBOOK.md) | 运行手册 |
| [DEV_GUIDE.md](../DEV_GUIDE.md) | 开发者指南 |
| [DESIGN.md](../DESIGN.md) | 设计指南 |
| [PROGRESS.md](../docs/PROGRESS.md) | 当前进度 |
| [TODO.md](../docs/TODO.md) | 后续待办 |
| [CHANGELOG.md](../docs/CHANGELOG.md) | 变更日志 |

---

## 🔑 十四、核心设计原则

1. **GameState 是唯一状态源** — 所有模块通过 GameState 交换信息，禁止直接模块间调用
2. **事件驱动** — 状态变化自动触发事件，事件映射到技能
3. **Mock 优先** — 开发测试优先使用 Mock 模式，无需真实设备
4. **安全优先** — 高风险技能禁止自动执行，中风险需确认
5. **可观测性** — 所有操作有日志、指标、审计记录

---

*最后更新：2026-04-27*
