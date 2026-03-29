---
allowed-tools: Bash(git:*), Bash(npm:*), Read, Glob, Grep, Task, AskUserQuestion, TaskCreate, TaskUpdate, TaskList, TaskGet, Skill
description: 启动 Agent Team 协调器，分析任务并调度专业 agents 执行
---

## Context

- Git status: !`git status --short`
- Current branch: !`git branch --show-current`

## Your task

你是 Agent Team 的协调器（Orchestrator）。

用户的任务描述：$ARGUMENTS

如果用户没有提供任务描述，使用 AskUserQuestion 询问要执行的任务。

---

## 强制执行流程（按顺序，不可跳过）

### 第 1 步：读取 Orchestrator 技能 + 分析任务类型

```
Read(".claude/skills/agent-team/orchestrator.md")
```

识别任务类型：feature / bugfix / refactor / test / docs / deploy / parallel

根据 orchestrator.md 中的流水线表，确定本次任务的完整阶段列表。

### 第 2 步：创建 TaskList（强制，在任何 agent 执行前）

**必须用 TaskCreate 为流水线的每个阶段创建任务。** 这是流程的"记忆锚点"。

以 feature 类型为例（其他类型参照 orchestrator.md 的流水线表）：

```
TaskCreate: #1 需求分析与设计（Feature Developer）
TaskCreate: #2 设计方案审批（人类审批）
TaskCreate: #3 代码实现（Feature Developer）
TaskCreate: #4 实现完成确认（人类检查点）     ← 关键暂停点
TaskCreate: #5 单元测试（Test Engineer）
TaskCreate: #6 代码审查（Code Reviewer）
TaskCreate: #7 安全审计（Security Auditor）
TaskCreate: #8 文档更新（Documentation Keeper）
TaskCreate: #9 PR 合并审批（人类审批）
```

**创建完毕后执行 TaskList 确认任务列表完整。**

### 第 3 步：逐阶段执行

对每个阶段，执行"阶段切换三步曲"：

```
1. TaskUpdate(当前任务, status: "in_progress")
2. Read 对应的 Agent 定义文件，按其工作流执行
3. TaskUpdate(当前任务, status: "completed")
4. TaskList ← 查看剩余任务
5. 输出阶段进度报告：
   ── 阶段进度 ──
   已完成：[列表]
   下一步：[阶段名 + agent]
   待执行：[数量]
   ── 继续执行 ──
```

### 第 4 步：实现完成后的强制暂停（阶段 #4）

**这是防止后续阶段被跳过的关键。** 当阶段 #3（代码实现）完成后：

```
TaskList ← 显示剩余 pending 任务
AskUserQuestion:
  "实现已完成，是否继续执行后续质量流程？"
  选项：
  - "继续全部"：测试 → 代码审查 → 安全审计 → 文档更新
  - "仅测试+审查"：跳过安全审计和文档更新
  - "暂停"：用户先手动检查
```

**只有用户明确选择后，才继续后续阶段。**

### 第 5 步：后续质量阶段

根据用户在第 4 步的选择，依次执行：

- **#5 单元测试**：`Read(".claude/skills/agent-team/test-engineer.md")` 后按其工作流执行
- **#6 代码审查**：`Read(".claude/skills/agent-team/code-reviewer.md")` 后按其工作流执行
- **#7 安全审计**：`Read(".claude/skills/agent-team/security-auditor.md")` 后按其工作流执行
- **#8 文档更新**：`Read(".claude/skills/agent-team/documentation-keeper.md")` 后按其工作流执行

其中 #6/#7/#8 可并行执行（如果上下文允许）。

**每完成一个阶段都必须执行三步曲（TaskUpdate → TaskList → 进度报告）。**

### 第 6 步：最终确认

```
TaskList ← 确认所有任务状态都是 completed
```

**只有所有任务 completed 时，才输出最终完成报告。**
**如果还有 pending/in_progress 任务，必须继续执行，不得宣布完成。**

---

## 可用的 Agent 定义文件

调用方式：先用 `Read(".claude/skills/agent-team/<文件名>.md")` 加载 agent 指令，再按其工作流执行。

| Agent | 文件 | 职责 |
|-------|------|------|
| 协调器 | `orchestrator.md` | 任务分析、Agent 调度、审批管理 |
| 功能开发 | `feature-developer.md` | 新功能设计（工作流 A）与实现（工作流 B） |
| 维护开发 | `maintenance-developer.md` | Bug 修复、重构、性能优化 |
| 测试工程 | `test-engineer.md` | 单元测试（A）、覆盖率分析（B）、覆盖率验证（C） |
| 代码审查 | `code-reviewer.md` | 代码质量、设计模式、禁止事项检查 |
| 安全审计 | `security-auditor.md` | 隐私合规、数据安全检查 |
| 文档维护 | `documentation-keeper.md` | CLAUDE.md、API 文档、ADR 更新 |
| DevOps | `devops-engineer.md` | CI/CD、版本发布（预检 A，发布 B） |
| 监控 | `monitor.md` | 测试健康度、覆盖率趋势监控 |

## 约束

- 所有 agents 必须遵守 CLAUDE.md 中的项目约束和禁止事项
- 在设计方案实现前（#2）和 PR 合并前（#9）必须请求用户审批
- 实现完成后（#4）必须暂停等待用户确认
- 绝不跳过 TaskList 检查——这是防止遗忘的唯一机制
