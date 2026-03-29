# /do 命令与 Agent Team 设计文档

**日期**：2026-03-29
**状态**：已批准

---

## 概述

`/do` 命令是 Harness 工程支架的 Agent Team 协调入口。用户通过 `/do <任务描述>` 启动多 Agent 协作流水线，由协调器分析任务类型并按阶段调度专业 Agent 执行，全程带人类审批检查点。

该系统同时安装在 harness 仓库本身（供开发使用）和目标项目（通过 INSTALL.md Phase X 安装）。

---

## 设计目标

- 人类掌舵：关键节点（设计审批、实现确认、PR 合并）必须暂停等待用户确认
- 流程可见：TaskCreate/TaskList 提供任务进度的"记忆锚点"
- Agent 专业化：每个 Agent 文件自洽，职责单一，可独立理解和维护
- 可安装：整套文件通过 INSTALL.md 安装到任意目标工程

---

## 架构：Option B — 瘦协调器 + 自洽 Agent 文件

协调器只负责路由（任务类型 → 流水线阶段顺序），专业 Agent 文件负责执行细节。

```
/do <task>
      │
      ▼
do.md          ← 注入上下文 (git 状态、分支、任务)
      │           TaskCreate 所有流水线阶段
      │           读取 orchestrator.md
      ▼
orchestrator.md  ← 流水线映射表 + 人类检查点规则
      │
      ▼ (按阶段)
agent/*.md       ← 自洽：角色、输入/输出、决策规则、步骤、输出格式
```

---

## 文件结构

```
.claude/
├── commands/
│   └── do.md                          # /do 命令入口
└── skills/
    └── agent-team/
        ├── orchestrator.md            # 流水线映射 + 路由规则
        ├── feature-developer.md       # 新功能设计与实现
        ├── maintenance-developer.md   # Bug 修复 / 重构 / 性能优化
        ├── test-engineer.md           # 单元测试 + E2E + 覆盖率
        ├── code-reviewer.md           # 代码质量 + 设计模式 + 反模式
        ├── security-auditor.md        # 隐私合规 + 数据安全
        ├── documentation-keeper.md    # CLAUDE.md + API 文档 + ADR
        ├── devops-engineer.md         # CI/CD + 版本发布 + 部署
        └── monitor.md                 # 测试健康度 + 覆盖率趋势
```

---

## do.md 职责

1. 注入执行上下文（git status、当前分支）
2. 接收 `$ARGUMENTS`（任务描述）
3. 若无任务描述，使用 `AskUserQuestion` 询问
4. 读取 `orchestrator.md`，识别任务类型
5. 用 `TaskCreate` 为流水线每个阶段建立任务
6. 按阶段执行"三步曲"：TaskUpdate(in_progress) → 执行 → TaskUpdate(completed) → TaskList → 进度报告
7. 在人类检查点暂停

**allowed-tools:** Bash(git:*), Bash(npm:*), Read, Glob, Grep, Task, AskUserQuestion, TaskCreate, TaskUpdate, TaskList, TaskGet, Skill

---

## orchestrator.md 职责

包含以下内容（不包含执行细节）：

### 任务类型识别规则
- 关键词 → 任务类型（feature / bugfix / refactor / test / docs / deploy / parallel）

### 流水线映射表

| 任务类型 | 阶段列表 |
|----------|----------|
| feature | 设计→审批→实现→确认→测试→审查→安全→文档→PR审批 |
| bugfix | 诊断→实现→确认→测试→审查→安全→PR审批 |
| refactor | 分析→实现→确认→测试→审查→文档→PR审批 |
| test | 分析→补测→确认→覆盖率检查 |
| docs | 分析→更新→确认 |
| deploy | 预检→发布→确认 |
| parallel | 分析→并行执行→汇总→确认 |

### 阶段切换三步曲协议
```
1. TaskUpdate(当前任务, in_progress)
2. Read 对应 Agent 文件，按其工作流执行
3. TaskUpdate(当前任务, completed)
4. TaskList
5. 输出进度报告
```

### 人类检查点规则
- **#2 设计审批**：展示设计方案，AskUserQuestion 等待批准后才实现
- **#4 实现确认**：展示 TaskList，AskUserQuestion 选择后续质量流程范围
- **#9 PR 合并审批**：展示最终清单，AskUserQuestion 等待批准

---

## Agent 文件规范（每个文件的结构）

每个 agent 文件包含以下 sections：

1. **角色与职责**：一句话描述这个 agent 做什么
2. **输入**：从上下文中读取的信息（代码文件、任务描述等）
3. **工作流**：编号的步骤列表，含决策分支
4. **输出格式**：具体的 markdown 输出模板
5. **质量标准**：通过/不通过的判断规则
6. **禁止事项**：绝不能做的事

---

## 人类检查点详细设计

### 检查点 #2：设计审批

```
AskUserQuestion:
  "已完成设计方案，请审阅后决定是否继续实现"
  选项：
  - "批准，开始实现"
  - "需要修改：[用户填写]"
  - "暂停，稍后继续"
```

### 检查点 #4：实现确认

```
AskUserQuestion:
  "实现已完成。后续质量流程包括：测试 / 代码审查 / 安全审计 / 文档更新"
  选项：
  - "继续全部"
  - "仅测试 + 代码审查"（跳过安全和文档）
  - "暂停，手动检查"
```

### 检查点 #9：PR 合并审批

```
AskUserQuestion:
  "所有流程已完成，是否批准合并 PR？"
  选项：
  - "批准合并"
  - "暂不合并，等待人工检查"
```

---

## INSTALL.md 集成

在现有 Phase 5（F 回路）之后添加 **Phase 6 — Agent Team（可选）**：

- 阶段性质：可选，用户可跳过
- 安装内容：`.claude/commands/do.md` + `.claude/skills/agent-team/` 全部 9 个文件
- 确认模式：与其他 Phase 一致，展示已创建文件清单后询问是否继续
- 文件内容：INSTALL.md 中以代码块形式内嵌所有文件的完整内容

---

## 实现顺序

1. 创建 `.claude/skills/agent-team/` 目录和 9 个 agent 文件（各含完整工作流）
2. 创建 `.claude/commands/do.md`（引用上述 agent 文件）
3. 更新 INSTALL.md，添加 Phase 6，内嵌所有文件内容
4. 验证：在 harness 项目中执行 `/do` 命令测试流程

---

## 约束

- 所有 agent 文件必须可独立阅读理解（不依赖其他 agent 文件的内容）
- 人类检查点不可跳过（不能在代码中硬编码"自动批准"）
- `do.md` 本身不包含任何业务逻辑，全部委托给 orchestrator.md 和 agent 文件
- INSTALL.md 中的文件内容与 `.claude/` 目录中的实际文件内容保持一致
