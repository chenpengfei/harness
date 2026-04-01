# Claude Code 源码：12 个递进的 Harness 机制

**来源**：`sanbuphy/claude-code-source-code`（`@anthropic-ai/claude-code` v2.1.88 逆向解析，约 1884 个 TypeScript 源文件）

---

## 被包裹的对象：最小 Agent 循环

```
用户 → messages[] → Claude API → response
                                    |
                          stop_reason == "tool_use"?
                         /                          \
                       yes                           no
                        |                             |
                  执行工具                          返回文本
                  追加 tool_result
                  继续循环 ──────────────→ messages[]
```

> "That is the minimal agent loop. Claude Code wraps this loop with a production-grade harness: permissions, streaming, concurrency, compaction, sub-agents, persistence, and MCP."

**根本约束：12 个机制全部在这个循环外层叠加，不修改循环本身。**

---

## s01 — THE LOOP

**口号**：`"One loop & Bash is all you need"`

**实现**：`query.ts`

`while(true)` 循环调用 Claude API，检测 `tool_use` 事件，执行工具，追加 `tool_result`，继续下一轮。这是 Agent 系统不可再化简的内核。

**源码细节**：
- 循环通过**流式检测** `tool_use` 事件触发工具调用，而非等待完整响应后检查 `stop_reason`——这意味着工具调用在 Claude 输出过程中即开始处理，延迟更低。
- `stop_reason == "end_turn"` 才是真正的循环退出条件；`tool_use` 是循环延续的信号。

**设计意义**：理解这个循环，后续所有机制都可以被理解为"如何在不改变循环的前提下扩展它"。

---

## s02 — TOOL DISPATCH

**口号**：`"Adding a tool = adding one handler"`

**实现**：`Tool.ts` + `tools.ts`

所有工具注册到调度表（dispatch map），Loop 通过工具名查表调用。`buildTool()` 工厂函数提供安全默认值，开发者只需实现业务逻辑。添加 40 个工具，Loop 代码一行不变。

**源码细节**：
- 每个 Tool 对象包含 `inputSchema`（JSON Schema）、`call()` 处理函数、权限检查钩子。
- `buildTool()` 工厂注入统一的错误处理和权限拦截，业务逻辑不需要重复实现。

**设计意义**：Loop 与 Tool 完全解耦。工具是能力的容器，Loop 是调度器，两者互不感知具体细节。

---

## s03 — PLANNING

**口号**：`"An agent without a plan drifts"`

**实现**：`EnterPlanModeTool` + `ExitPlanModeTool` + `TodoWriteTool`

强制 Agent 在执行前先将目标分解成步骤列表：EnterPlanMode（锁定，禁止直接执行工具）→ 列步骤 → 确认 → ExitPlanMode（解锁）→ 按计划逐步执行。计划写到磁盘文件，不消耗 `messages[]` 上下文。

**声称效果**：将任务完成率翻倍（doubles completion rate）。

**源码细节**：
- 计划模式通过**权限系统状态机**实现锁定：`EnterPlanModeTool` 设置全局权限标志，所有写操作类工具在此标志激活时返回 `"permission denied"`；`ExitPlanModeTool` 清除该标志。
- 状态机路径：`default → plan_mode（只读）→ default（可执行）`，Agent 无法跳过规划阶段直接执行。
- `TodoWriteTool` 将 checklist 写入磁盘 JSON 文件，`messages[]` 中只记录"已写入文件"的事实，不含完整任务内容，节省上下文预算。

**设计意义**：将全局目标显式化。没有规划的 Agent 在长任务中会"漂移"——每次工具调用都是局部最优，累积下来偏离目标。

---

## s04 — SUB-AGENTS

**口号**：`"Break big tasks; clean context per subtask"`

**实现**：`AgentTool` + `forkSubagent.ts`

每个子 Agent 获得全新的空 `messages[]`，主 Agent 的长历史不污染子任务执行。主 Agent 对话历史越长，每次 API 调用越贵、越慢、模型注意力越分散。

**源码细节**：
- `forkSubagent.ts` 使用**统一占位符文本**（uniform placeholder text）作为 system prompt 前缀，使所有子 Agent 的 prompt 结构相同，命中 Anthropic 服务端的**提示缓存**（prompt cache）——多个并发子 Agent 共享同一批缓存的 token，大幅降低 API 费用。
- 子 Agent 的 system prompt = 占位符前缀 + 任务专属指令；占位符部分跨调用不变，是缓存命中的关键。

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
- 队员的邮箱（mailbox）是写在磁盘的 JSON 文件，主 Agent 和队员都通过文件 I/O 通信，天然持久化。

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

**设计约束**：禁止 Agent 直接发送自定义 JSON 状态消息；所有协调通过类型系统约束，而不是约定俗成的"大家发 JSON"。

**设计意义**：自由通信导致消息格式不统一无法可靠解析；协议让每种交互有明确语义，错误时可以定位是哪个环节失败。

---

## s11 — AUTONOMOUS AGENTS

**口号**：`"Teammates scan and claim tasks themselves"`

**实现**：`coordinator/coordinatorMode.ts`

协调者模式的核心循环：

```
while (true) {
  tasks = TaskList()
  available = tasks.filter(t =>
    t.status === "pending" &&
    t.owner === null &&
    t.blockedBy.every(dep => dep.status === "completed")
  )
  if (available.length > 0) {
    task = available[0]  // 按 ID 顺序优先
    TaskUpdate(task.id, { owner: myName, status: "in_progress" })
    execute(task)
    TaskUpdate(task.id, { status: "completed" })
  } else {
    idle()
  }
}
```

**源码细节**：
- `coordinatorMode.ts` 是**编译时 feature gate** 控制的功能：该模块通过编译标志决定是否激活，而非运行时配置——这意味着在标准发布版中此模式不可见，只在特定构建目标中启用。
- 任务认领使用乐观锁（optimistic locking）语义：两个队员同时认领同一任务时，后到者的 `TaskUpdate` 会因版本冲突失败，需重新扫描任务列表。

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
- **清理保护**：worktree 清理脚本使用**正则模式**匹配 harness 自动创建的 worktree 名称（如 `task-\d+`），只删除符合模式的目录，显式跳过用户手动命名的 worktree——防止误删用户工作区。
- **无自动合并**：`ExitWorktreeTool` 只提供两种策略：`keep`（保留 worktree 供人工处理）或 `remove`（直接删除）。没有自动 merge 逻辑——合并是有歧义的操作，Claude Code 选择不替用户做这个决策。

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
