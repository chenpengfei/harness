# Claude Code 源码：12 个递进的 Harness 机制

**来源**：`sanbuphy/claude-code-source-code`（`@anthropic-ai/claude-code` v2.1.88 逆向解析，约 1884 个 TypeScript 源文件）

---

## 被包裹的对象：最小 Agent 循环

```
用户 → messages[] → Claude API → 流式响应
                                    |
                       流中出现 tool_use 块?
                         /                  \
                       yes                   no（end_turn）
                        |                       |
                  执行工具                    返回文本
                  追加 tool_result
                  继续循环 ──────────→ messages[]
```

> "That is the minimal agent loop. Claude Code wraps this loop with a production-grade harness: permissions, streaming, concurrency, compaction, sub-agents, persistence, and MCP."

**根本约束：12 个机制全部在这个循环外层叠加，不修改循环本身。**

---

## s01 — THE LOOP

**口号**：`"One loop & Bash is all you need"`

**实现**：`query.ts`

`while(true)` 循环调用 Claude API，检测 `tool_use` 事件，执行工具，追加 `tool_result`，继续下一轮。这是 Agent 系统不可再化简的内核。

**源码细节**：
- 循环通过**流式检测** `tool_use` 块触发工具调用，设置内部 `needsFollowUp = true` 标志，而非等待 API 返回后检查 `stop_reason` 字段——工具调用在 Claude 输出过程中即开始处理，延迟更低。
- `stop_reason == "end_turn"` 才是真正的循环退出条件；`stop_reason == "tool_use"` 在实现中实际上不被直接使用。
- **错误处理三层梯级**：`FallbackTriggeredError`（清空孤立消息，切换备用模型重试）→ `max_output_tokens`（三次重试，逐步升级到 `ESCALATED_MAX_TOKENS`）→ `prompt_too_long`（触发 reactive compact 压缩后继续）。

**设计意义**：理解这个循环，后续所有机制都可以被理解为"如何在不改变循环的前提下扩展它"。

---

## s02 — TOOL DISPATCH

**口号**：`"Adding a tool = adding one handler"`

**实现**：`Tool.ts` + `tools.ts`

所有工具注册到调度表（dispatch map），Loop 通过工具名查表调用。`buildTool()` 工厂函数提供安全默认值，开发者只需实现业务逻辑。添加 40 个工具，Loop 代码一行不变。

**源码细节**：
- `buildTool()` 工厂注入 `TOOL_DEFAULTS`：`isEnabled → true`、`isConcurrencySafe → false`（假设不可并发）、`isReadOnly → false`（假设有写入）、`checkPermissions → allow`。业务代码只覆盖需要改变的字段。
- `assembleToolPool()` 合并内置工具 + MCP 工具后**按名称字母序排序**，确保每次生成的工具列表顺序一致，最大化提示缓存命中率。
- `filterToolsByDenyRules()` 在渲染 API 请求前过滤黑名单工具，模型完全看不到被拒绝的工具——防止模型尝试调用无权限的工具。
- `isConcurrencySafe(input)` 返回 `true` 的工具（如只读工具）可被 `StreamingToolExecutor` 并发执行；返回 `false` 的工具串行执行，保护写操作。
- 每个 Tool 对象还包含 React/Ink 渲染方法（`renderToolUseMessage`、`renderToolResultMessage`），负责终端 UI 的可视化输出——工具不仅是执行者，也是完整的 UI 单元。

**设计意义**：Loop 与 Tool 完全解耦。工具是能力的容器，Loop 是调度器，两者互不感知具体细节。

---

## s03 — PLANNING

**口号**：`"An agent without a plan drifts"`

**实现**：`EnterPlanModeTool` + `ExitPlanModeTool` + `TodoWriteTool`

强制 Agent 在执行前先将目标分解成步骤列表：EnterPlanMode（锁定，禁止直接执行写操作工具）→ 列步骤 → 确认 → ExitPlanMode（解锁）→ 按计划逐步执行。

**声称效果**：将任务完成率翻倍（doubles completion rate）。

**源码细节**：
- 计划模式通过**权限系统状态机**实现锁定：`EnterPlanModeTool` 在 `AppState.toolPermissionContext` 中设置 `mode: 'plan'`，保存旧模式到 `prePlanMode`；此后所有写操作类工具的 `checkPermissions()` 返回拒绝。`ExitPlanModeTool` 恢复 `mode: prePlanMode ?? 'default'`。
- `EnterPlanMode` 的 `tool_result` 直接包含明确指令：`"Entered plan mode. DO NOT write or edit any files..."`，同时列出 5 步规划流程要求——指令写在 tool_result 而非 system prompt，确保 Agent 在切换时看到。
- **TodoWriteTool 存储位置**：`todos` 写入 **`AppState`**（内存状态），按 `agentId` 隔离，支持多 Agent 并发使用；不写磁盘，会随上下文压缩而丢失（这是设计意图：todo 是"当前规划的进度"，不是跨会话持久化的目标）。
- **团队审批流**：团队成员调用 `ExitPlanMode` 时，若 `isPlanModeRequired()` 为 true，则构建 `plan_approval_request` 消息写入共享邮箱，异步等待 Lead Agent 审批；Lead 审批/拒绝通过 `SendMessageTool` 回应，不阻塞主循环。
- **AutoMode 熔断器**：从 plan 模式恢复时，若旧模式为 `'auto'` 但 `isAutoModeGateEnabled()` 为 false，则降级恢复到 `'default'`——防止意外激活自动权限模式。

**设计意义**：将全局目标显式化。没有规划的 Agent 在长任务中会"漂移"——每次工具调用都是局部最优，累积下来偏离目标。

---

## s04 — SUB-AGENTS

**口号**：`"Break big tasks; clean context per subtask"`

**实现**：`AgentTool` + `forkSubagent.ts`

每个子 Agent 获得独立的 `messages[]`，主 Agent 的长历史不污染子任务执行。主 Agent 对话历史越长，每次 API 调用越贵、越慢、模型注意力越分散。

**源码细节**：
- **Fork 子 Agent 的初始消息不是空的**：`forkSubagent.ts` 的 `buildForkedMessages()` 为 fork 子 Agent 构建最小化但有意义的初始历史：`[完整助手消息（含所有 tool_use 块）, 用户消息（所有 tool_use 对应的占位符 tool_result + 任务指令）]`。这比空历史更有效，因为子 Agent 有上下文知道自己是谁、被派来做什么。
- **提示缓存共享的关键设计**：所有 fork 子 Agent 的 `tool_result` 块使用**相同的占位符文本** `'Fork started — processing in background'`，与父消息的助手部分（相同）一起构成所有 fork 请求的公共前缀——所有并发子 Agent 命中同一批提示缓存，大幅降低 API 费用。只有最后的任务指令文本不同，缓存失效范围最小。
- **子 Agent 指令设计**：`buildChildMessage()` 生成的指令以 `"STOP. READ THIS FIRST."` 开头，列出 10 条不可违反规则（不要派生子代理、不要插话、工具静默调用、500 词内报告等），输出格式固定为 `Scope / Result / Key files / Files changed / Issues`。
- **`setAppState` 对异步子 Agent 是 no-op**：异步 Agent 的 `setAppState()` 被替换为空操作，防止子 Agent 修改父进程的权限模式（如从 plan mode 中意外退出）。
- **非 fork 子 Agent**（通过 Task/AgentTool 创建）获得 `messages: []` 真正的空历史，与 fork 子 Agent 不同。

**与 s03 配合**：规划（s03）决定分解成哪些步骤，子 Agent（s04）用干净上下文执行每步。

**设计意义**：上下文预算管理的核心手段。上下文越干净，模型注意力越集中。

---

## s05 — KNOWLEDGE ON DEMAND

**口号**：`"Load knowledge when you need it"`

**实现**：`SkillTool` + `memdir/` + 懒加载 `CLAUDE.md`

知识通过 `tool_result` 注入到 `messages[]`，而不是写死在 `system prompt`。`CLAUDE.md` 懒加载：Agent 进入某目录时才加载该目录的 `CLAUDE.md`，而非启动时全量加载。

两种错误方式：
- ❌ 全量塞入 system prompt → 上下文浪费，无关知识干扰推理
- ❌ 不提供知识 → Agent 凭空猜测，产生幻觉

**源码细节**：
- `memdir/` 中的记忆检索使用 **Sonnet 模型**（非当前对话模型）通过 `sideQuery()` 函数执行语义选择：给定当前任务描述，Sonnet 从记忆索引中选出最相关的记忆文件，再由 SkillTool 加载其内容注入到主对话。
- 这意味着知识检索是一次独立的 API 调用（`sideQuery`），不在主对话的 `messages[]` 中留下痕迹。

**设计意义**：知识是动态的、按需替换的；system prompt 是静态全局配置。

---

## s06 — CONTEXT COMPRESSION

**口号**：`"Context fills up; make room"`

**实现**：`services/compact/`

三层策略（侵入程度递增）：

| 策略 | 机制 | 代价 | Feature Flag |
|------|------|------|-------------|
| autoCompact | 额外 API 调用生成摘要，`[摘要] + [最近 N 条消息]` | 一次 API 调用费用 | 默认启用 |
| snipCompact | 移除僵尸消息（过期标记、无效工具调用） | 极低 | `HISTORY_SNIP` |
| contextCollapse | 重新组织整个对话结构，高密度压缩 | 较高 | `CONTEXT_COLLAPSE` |

**源码细节**：
- **触发阈值**：`autoCompact` 在 `当前 token 数 > context_window - 13000` 时触发——预留 13K token 作为安全余量，确保压缩请求本身有足够空间完成。
- **熔断机制**：连续压缩失败 3 次后激活 **circuit breaker**，停止自动压缩并告警，避免在不可压缩的对话中无限重试浪费 API 调用。
- 压缩后的摘要以特殊标记写入 `messages[]` 头部，Loop 无需任何感知，直接使用压缩后的历史继续对话。

**设计意义**：上下文窗口是 Agent 的工作内存，是有限资源，必须主动管理。

---

## s07 — PERSISTENT TASKS

**口号**：`"Big goals → small tasks → disk"`

**实现**：`TaskCreate` + `TaskUpdate` + `TaskGet` + `TaskList`

任务图写到磁盘，完全独立于 `messages[]`。数据结构包含 `id`、`subject`、`status`（pending → in_progress → completed）、`blockedBy`、`blocks`、`owner`。

**与 s03 的区别**：

| | s03 TodoWriteTool | s07 TaskCreate |
|--|------------------|---------------|
| 作用范围 | 当前任务内的步骤列表 | 跨会话、跨 Agent 的目标追踪 |
| 类比 | 计划 | 项目管理 |
| 存活条件 | 依赖当前上下文 | 完全独立于上下文 |

**设计意义**：上下文压缩了、Agent 重启了、换 Agent 了，任务都还在。

---

## s08 — BACKGROUND TASKS

**口号**：`"Slow ops in background; agent keeps thinking"`

**实现**：`DreamTask`（抽象基类）+ `LocalShellTask`（本地 Shell 实现）

后台守护线程运行慢操作，完成时将通知反馈给主循环。

```
主循环 → 派发 LocalShellTask（构建命令）→ 继续做其他事
                 ↓（后台守护线程）
                 运行中...完成
                 → 通知主循环
主循环下一次迭代看到通知 → 处理结果
```

**源码细节**：
- 后台任务完成后，通知通过 **`AppState`**（全局应用状态）而非直接写入 `messages[]` 来传递——主循环在每次迭代开始时读取 AppState 中的待处理通知，再将其转换为 `tool_result` 形式注入到对话中。
- 这一设计将"何时通知"的决策权交给主循环（拉模式），而非后台任务直接推送，避免了线程竞争问题。

**设计意义**：慢 I/O 不阻塞主循环，且完全符合 Loop 统一数据流模型。

---

## s09 — AGENT TEAMS

**口号**：`"Too big for one → delegate to teammates"`

**实现**：`TeamCreate` + `TeamDelete` + `InProcessTeammateTask`

| | 子 Agent（s04） | 团队成员（s09） |
|--|---------------|--------------|
| 生命周期 | 临时，用完销毁 | 持久化 |
| 通信方式 | 同步等待结果 | 异步邮箱 |
| 执行模式 | 串行 | 并行 |
| 互通能力 | 不能互通 | 可互发消息 |

**源码细节**：
- `InProcessTeammateTask` 通过 Node.js 的 **`AsyncLocalStorage`** 为每个队员在同一进程内维护独立的异步上下文——每个队员的工具调用、权限检查、日志都在各自的 AsyncLocalStorage 域中执行，互不干扰，成本远低于进程级隔离（无需序列化、无 IPC 开销）。
- `TeammateContext` 类型包含：`agentId`（如 `"researcher@my-team"`）、`agentName`、`teamName`、`planModeRequired`（是否强制规划审批）、`abortController`（独立生命周期控制）。
- **上下文查询优先级**：AsyncLocalStorage（in-process 队员）> dynamicTeamContext（tmux/CLI 参数）> 环境变量（遗留支持）——三路查询，自动降级。
- 队员的邮箱（mailbox）存储在文件系统或内存（按团队名称索引），支持跨进程和进程内两种部署模式；`TeamFile` 中记录每个成员的 `tmuxPaneId`、`color`、`mode`、`isActive` 等元数据。

**设计意义**：突破单 Agent 上下文和时间限制，实现真正的并行工作流。

---

## s10 — TEAM PROTOCOLS

**口号**：`"Shared communication rules"`

**实现**：`SendMessageTool`

`SendMessageTool` 定义所有 Agent 间交互的消息类型：

| 类型 | 用途 |
|------|------|
| `message` | 普通 DM |
| `broadcast` | 广播给所有成员 |
| `shutdown_request` / `shutdown_response` | 优雅关闭协商 |
| `plan_approval_request` / `plan_approval_response` | 计划审批 |

**设计约束**：禁止 Agent 直接发送自定义 JSON 状态消息；所有协调通过类型系统约束，而不是约定俗成的"大家发 JSON"。`plan_approval_request` 在协议层定义（从 `ExitPlanMode` 发出），`plan_approval_response` 由 Lead 通过 `SendMessageTool` 回应。

**源码细节**：
- 消息类型使用 **Zod discriminated union**（`z.discriminatedUnion('type', [...])`) 静态验证，三种结构化消息：`shutdown_request`、`shutdown_response`、`plan_approval_response`；普通 DM 使用纯文本字段。
- **Shutdown 握手流程**：Lead 发送 `shutdown_request`（含唯一 `requestId`）→ 队员选择 approve/reject → 若 in-process 且 approve，`SendMessageTool` 直接调用该队员 `AbortController.abort()`；若 tmux，等待后台进程自行退出。
- **跨会话防护**：Bridge 跨会话消息被明确禁止发送结构化协议消息——防止恶意 prompt 注入利用协议消息进行权限提升。

**设计意义**：自由通信导致消息格式不统一无法可靠解析；协议让每种交互有明确语义，错误时可以定位是哪个环节失败。

---

## s11 — AUTONOMOUS AGENTS

**口号**：`"Teammates scan and claim tasks themselves"`

**实现**：`coordinator/coordinatorMode.ts`

协调者模式定义了 Coordinator 的工作角色和工作流：

```
Research（Workers 并行）→ Synthesis（Coordinator 理解发现）
  → Implementation（Workers 执行）→ Verification（Workers 验证）
```

Worker 结果以 XML 格式传入 Coordinator 的用户消息，Coordinator 在 Synthesis 阶段必须**主动理解**（而非委托理解），生成有具体文件路径和行号的实施方案，再派发 Workers 执行。

**源码细节**：
- **双层 feature gate**：`isCoordinatorMode()` 同时检查 **`feature('COORDINATOR_MODE')`**（编译时死代码消除）和**环境变量 `CLAUDE_CODE_COORDINATOR_MODE`**（运行时开关）——两者都需为 true 才激活，标准发布版不可见。
- **会话恢复**：`matchSessionMode()` 恢复会话时若模式不匹配，会自动翻转 `CLAUDE_CODE_COORDINATOR_MODE` 环境变量使其与保存的会话模式一致。
- **任务扫描由提示驱动**，不是独立后台线程：Coordinator 的 system prompt 描述了扫描-合成-派发-验证四阶段，Coordinator 在每轮 Loop 迭代中自主决策派发哪些 Workers。
- **Scratchpad 门控**：`isScratchpadGateEnabled()` 为 true 时，Workers 可在专用目录读写不触发权限提示，用于传递中间结果。
- **反模式告警**：system prompt 明确标记 `"Based on your findings"` 为懒惰委托反模式——Coordinator 必须亲自理解 Worker 报告，而非再派一个 Worker 来理解。

**从 s09 的演进**：Lead Agent 从"微观指派每个任务"解放为"只关注任务拆分和依赖关系的正确性"。

**设计意义**：去中心化任务分配；Lead Agent 的瓶颈消失。

---

## s12 — WORKTREE ISOLATION

**口号**：`"Each works in its own directory"`

**实现**：`EnterWorktreeTool` + `ExitWorktreeTool`

每个任务 ID 绑定一个独立的 Git Worktree，Agent 在自己的目录副本里工作：

```
主仓库 /project/
    └── .worktrees/
           ├── task-001/src/  ← Agent-1 的独立副本
           └── task-002/src/  ← Agent-2 的独立副本
```

**关键分离**：

| 维度 | 负责内容 |
|------|---------|
| 任务（s07） | 做什么、做到什么程度（目标维度） |
| Worktree（s12） | 在哪里做（文件系统维度） |

两者通过 Task ID 绑定，关注点完全分离。

**源码细节**：
- **路径安全**：`validateWorktreeSlug()` 验证 slug 防止路径穿越攻击；支持用户自定义 VCS hook（`hasWorktreeCreateHook()`），允许替换默认 git 实现。
- **Sparse-checkout 支持**：大型仓库可在创建 worktree 时应用 sparse-checkout，只检出相关路径（`usedSparsePaths` 记录是否已应用），大幅减少 I/O。
- **清理的三层架构**：
  1. Runtime（`ExitWorktreeTool`）：用户触发，`remove` 策略需显式设置 `discard_changes: true` 才能删除有未提交改动的 worktree——fail-closed 设计。
  2. Session（`gracefulShutdown`）：会话正常退出时自动清理本次会话创建的 worktree。
  3. Background（30 天扫描）：`cleanupStaleAgentWorktrees()` 按**正则模式**识别临时 worktree（`/^agent-a[0-9a-f]{7}$/`、`/^wf_[0-9a-f]{8}-[0-9a-f]{3}-\d+$/`、`/^bridge-[A-Za-z0-9_]+/`），跳过用户自命名 worktree；任何 git 命令失败则拒绝删除（fail-closed）。
- **无自动合并**：`ExitWorktreeTool` 只提供 `keep`（保留）或 `remove`（删除）；`remove` 前检查未提交文件数和未推送提交数，需用户明确确认才能丢弃。合并决策留给人类。

**设计意义**：并行 Agent 的文件系统冲突终极解决方案。

---

## 12 层递进问题链

每一层解决上一层引入的新问题，层层递进，无一冗余：

| 层 | 引入能力 | 随之出现的问题 | 下一层解决 |
|----|---------|------------|---------|
| s01 | Agent 循环 | 工具怎么接入？ | s02 |
| s02 | 工具系统 | Agent 会迷失方向 | s03 |
| s03 | 规划 | 大任务上下文不够 | s04 |
| s04 | 子 Agent | 知识怎么给？ | s05 |
| s05 | 按需知识 | 上下文还是会满 | s06 |
| s06 | 压缩 | 目标丢失了 | s07 |
| s07 | 持久任务 | 慢操作阻塞 | s08 |
| s08 | 后台任务 | 一个 Agent 不够 | s09 |
| s09 | 多 Agent | 通信混乱 | s10 |
| s10 | 通信协议 | 人工分配太慢 | s11 |
| s11 | 自主认领 | 文件冲突 | s12 |
| s12 | Worktree 隔离 | — | 完成 |
