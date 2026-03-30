# Phase 7：Agent Team（可选）

安装 `/do` 命令和 agent-team skill 文件集，为目标项目提供多 Agent 协作流水线能力。

用户通过 `/do <任务描述>` 启动协作流水线，支持 feature / bugfix / refactor / test / docs / deploy 六种任务类型，全程带人类审批检查点。

**Agent 执行步骤：**

1. 向用户介绍 Agent Team 能力：
   > "Phase 7（可选）：安装 `/do` 命令，支持多 Agent 协作执行开发任务（新功能、修复、重构、测试、文档、部署），全程带人类审批检查点。"

2. 询问用户是否安装：
   > "是否安装 Agent Team 能力？（回复'是'继续，或回复'跳过'略过此 Phase）"

3. 若用户选择跳过，直接跳至安装摘要输出。

4. 若用户确认安装，依次创建以下文件：

### 7.1–7.9 复制 agent-team skill 文件

> **Agent 注意**：以下各文件通过 WebFetch 或 Read 从 harness 仓库对应的
> `.claude/skills/agent-team/` 目录下的同名文件中获取，内容完全复制，不做任何修改。

| 目标路径 | 来源路径 |
|---------|---------|
| `.claude/skills/agent-team/orchestrator.md` | harness 仓库同路径 |
| `.claude/skills/agent-team/feature-developer.md` | harness 仓库同路径 |
| `.claude/skills/agent-team/maintenance-developer.md` | harness 仓库同路径 |
| `.claude/skills/agent-team/test-engineer.md` | harness 仓库同路径 |
| `.claude/skills/agent-team/code-reviewer.md` | harness 仓库同路径 |
| `.claude/skills/agent-team/security-auditor.md` | harness 仓库同路径 |
| `.claude/skills/agent-team/documentation-keeper.md` | harness 仓库同路径 |
| `.claude/skills/agent-team/devops-engineer.md` | harness 仓库同路径 |
| `.claude/skills/agent-team/monitor.md` | harness 仓库同路径 |

### 7.10 创建 .claude/commands/do.md

从 harness 仓库读取 `.claude/commands/do.md` 并创建到目标项目。

### 7.11 确认点

向用户展示已安装文件并输出摘要：
> "Agent Team 安装完成！
>
> **已创建的文件**：
> - `.claude/commands/do.md`
> - `.claude/skills/agent-team/` （9 个 skill 文件）
>
> **使用方式**：
> - `/do 添加用户登录功能` → 启动 feature 流水线
> - `/do 修复首页加载缓慢问题` → 启动 bugfix 流水线
> - `/do 重构数据库查询层` → 启动 refactor 流水线"

更新 `.harness/harness-config.json`，将 `agentTeam` 字段设为 `true`。
