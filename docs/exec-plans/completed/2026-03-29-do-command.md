# /do 命令与 Agent Team 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 创建 `/do` 命令和完整的 agent-team skill 文件集，使 harness 项目可通过 `/do <任务描述>` 启动多 Agent 协作流水线；并将该系统嵌入 INSTALL.md 供目标项目安装。

**Architecture:** 瘦协调器模式（Option B）——`do.md` 注入上下文并建立 TaskList，`orchestrator.md` 只负责路由（任务类型 → 阶段顺序），每个 agent 文件自洽包含完整工作流。

**Tech Stack:** Claude Code slash commands (`.claude/commands/`), Claude Code skills (`.claude/skills/`), TaskCreate/TaskList/TaskUpdate tools, AskUserQuestion tool, Markdown

---

## 文件映射

| 操作 | 路径 | 职责 |
|------|------|------|
| 新建 | `.claude/skills/agent-team/orchestrator.md` | 任务类型检测、流水线映射表、检查点规则 |
| 新建 | `.claude/skills/agent-team/feature-developer.md` | 新功能设计（工作流 A）与实现（工作流 B） |
| 新建 | `.claude/skills/agent-team/maintenance-developer.md` | Bug 诊断（工作流 A）与修复/重构实现（工作流 B） |
| 新建 | `.claude/skills/agent-team/test-engineer.md` | 测试编写（A）、覆盖率分析（B）、覆盖率验证（C） |
| 新建 | `.claude/skills/agent-team/code-reviewer.md` | 代码质量审查，输出 PASS/PASS_WITH_SUGGESTIONS/FAIL |
| 新建 | `.claude/skills/agent-team/security-auditor.md` | 安全审计，输出 PASS/WARNING/FAIL |
| 新建 | `.claude/skills/agent-team/documentation-keeper.md` | CLAUDE.md、API 文档、ADR 更新 |
| 新建 | `.claude/skills/agent-team/devops-engineer.md` | 预发布检查（A）与版本发布（B） |
| 新建 | `.claude/skills/agent-team/monitor.md` | 测试健康度与覆盖率趋势监控 |
| 新建 | `.claude/commands/do.md` | /do 命令入口 |
| 修改 | `INSTALL.md` | 追加 Phase 7（Agent Team，可选） |

---

## Task 1：创建 orchestrator.md

**Files:**
- Create: `.claude/skills/agent-team/orchestrator.md`

- [ ] **Step 1: 创建目录并写入 orchestrator.md**

```bash
mkdir -p .claude/skills/agent-team
```

文件内容（`.claude/skills/agent-team/orchestrator.md`）：

````markdown
# Agent Team 协调器

## 角色

你是 Agent Team 的协调器，负责：
1. 识别任务类型
2. 确定流水线阶段列表
3. 管理人类检查点
4. 指导阶段切换协议

**注意**：协调器不执行具体业务逻辑，只负责路由和协调。

---

## 任务类型识别

根据用户的任务描述，按以下规则识别任务类型：

| 类型 | 触发关键词 |
|------|-----------|
| feature | 新功能、add、feature、implement、新增、开发、创建功能 |
| bugfix | bug、fix、error、issue、修复、错误、问题、故障 |
| refactor | refactor、重构、optimize、优化、clean、清理、性能 |
| test | test、测试、coverage、覆盖率、补测、单测 |
| docs | doc、文档、readme、claude.md、api文档、更新文档 |
| deploy | deploy、release、发布、部署、上线 |
| parallel | 多个任务、并行、同时、批量 |

如果无法确定类型，使用 AskUserQuestion 询问：
> "这个任务属于哪种类型？feature（新功能）/ bugfix（修复）/ refactor（重构）/ test（测试）/ docs（文档）/ deploy（部署）"

---

## 流水线映射表

### feature（新功能）

```
阶段 #1：需求分析与设计（feature-developer，工作流 A）
阶段 #2：设计方案审批（人类审批）          ← 暂停点
阶段 #3：代码实现（feature-developer，工作流 B）
阶段 #4：实现完成确认（人类检查点）         ← 暂停点
阶段 #5：单元测试（test-engineer，工作流 A）
阶段 #6：代码审查（code-reviewer）
阶段 #7：安全审计（security-auditor）
阶段 #8：文档更新（documentation-keeper）
阶段 #9：PR 合并审批（人类审批）            ← 暂停点
```

### bugfix（修复）

```
阶段 #1：问题诊断（maintenance-developer，工作流 A）
阶段 #2：修复实现（maintenance-developer，工作流 B）
阶段 #3：修复确认（人类检查点）             ← 暂停点
阶段 #4：回归测试（test-engineer，工作流 A）
阶段 #5：代码审查（code-reviewer）
阶段 #6：安全审计（security-auditor）
阶段 #7：PR 合并审批（人类审批）            ← 暂停点
```

### refactor（重构）

```
阶段 #1：现状分析（maintenance-developer，工作流 A）
阶段 #2：重构实现（maintenance-developer，工作流 B）
阶段 #3：实现确认（人类检查点）             ← 暂停点
阶段 #4：测试验证（test-engineer，工作流 A）
阶段 #5：代码审查（code-reviewer）
阶段 #6：文档更新（documentation-keeper）
阶段 #7：PR 合并审批（人类审批）            ← 暂停点
```

### test（补测）

```
阶段 #1：覆盖率分析（test-engineer，工作流 B）
阶段 #2：测试编写（test-engineer，工作流 A）
阶段 #3：覆盖率确认（人类检查点）           ← 暂停点
阶段 #4：覆盖率验证（monitor）
```

### docs（文档）

```
阶段 #1：文档分析（documentation-keeper）
阶段 #2：文档更新（documentation-keeper）
阶段 #3：文档确认（人类检查点）             ← 暂停点
```

### deploy（部署）

```
阶段 #1：预发布检查（devops-engineer，工作流 A）
阶段 #2：版本发布（devops-engineer，工作流 B）
阶段 #3：发布确认（人类审批）               ← 暂停点
```

### parallel（并行）

```
阶段 #1：任务分解（协调器分析子任务）
阶段 #2：并行执行（根据子任务类型调度各 agent）
阶段 #3：结果汇总（协调器汇总各 agent 输出）
阶段 #4：汇总确认（人类检查点）             ← 暂停点
```

---

## 阶段切换三步曲协议

每个阶段开始和结束都必须严格遵守：

```
开始阶段：
1. TaskUpdate(taskId, status: "in_progress")
2. Read(".claude/skills/agent-team/<agent-file>.md")
3. 按 agent 文件的工作流执行

结束阶段：
4. TaskUpdate(taskId, status: "completed")
5. TaskList  ← 查看剩余任务
6. 输出进度报告：
   ── 阶段进度 ──
   已完成：[阶段名列表]
   下一步：[阶段名 + agent 名]
   剩余阶段数：[数量]
   ── 继续执行 ──
```

---

## 人类检查点规则

### 检查点：设计审批

在设计完成后（feature 阶段 #2），使用以下格式暂停：

```
AskUserQuestion:
  问题："设计方案已完成，请确认是否开始实现"
  选项 1："批准，开始实现"
  选项 2："需要修改设计"（用户说明后重新执行设计阶段）
  选项 3："暂停"
```

**只有选项 1 被选中后才继续实现阶段。**

### 检查点：实现确认

实现完成后展示 TaskList，然后：

```
AskUserQuestion:
  问题："代码实现已完成，如何继续后续质量流程？"
  选项 1："继续全部"（测试 + 代码审查 + 安全审计 + 文档更新）
  选项 2："仅测试 + 代码审查"（跳过安全审计和文档更新）
  选项 3："暂停，手动检查代码"
```

若选项 2：将安全审计和文档更新对应任务标记 `completed`（已跳过）后继续。
若选项 3：停止，等待用户在后续对话中重新触发。

### 检查点：PR 合并审批

所有质量阶段 completed 后：

```
AskUserQuestion:
  问题："所有流程已完成，是否批准合并 PR？"
  选项 1："批准合并"
  选项 2："暂不合并，等待人工检查"
```

---

## 并行执行规则

阶段 #6（代码审查）、#7（安全审计）、#8（文档更新）可以并行：

- 如果在一次 agent 响应中同时执行三个阶段，每个阶段的 TaskUpdate 和进度报告仍需独立完成。
- 并行执行时，按 #6 → #7 → #8 顺序依次标记 completed。

---

## 约束

- 不可跳过人类检查点（AskUserQuestion 是唯一合法的暂停机制）
- 不可在未读取 agent 文件的情况下执行该阶段
- TaskList 必须在每阶段完成后执行（这是防止遗忘的唯一机制）
- 所有任务 completed 后才能输出最终完成报告，禁止提前宣布完成
````

- [ ] **Step 2: 验证文件结构完整**

```bash
grep -c "## " .claude/skills/agent-team/orchestrator.md
```

预期输出：`≥ 7`（应包含：角色、任务类型识别、流水线映射表、三步曲协议、人类检查点规则、并行执行规则、约束）

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/agent-team/orchestrator.md
git commit -m "feat: add agent-team orchestrator skill"
```

---

## Task 2：创建 feature-developer.md

**Files:**
- Create: `.claude/skills/agent-team/feature-developer.md`

- [ ] **Step 1: 写入 feature-developer.md**

文件内容（`.claude/skills/agent-team/feature-developer.md`）：

````markdown
# Feature Developer

## 角色

设计并实现新功能。在设计阶段产出设计方案供人类审批；在实现阶段按审批后的设计编写代码。

## 当前任务判断

读取当前 `in_progress` 的 TaskList 条目，判断执行哪个工作流：
- 任务名含"设计"/"分析"/"方案" → 执行【工作流 A：需求分析与设计】
- 任务名含"实现"/"开发"/"代码" → 执行【工作流 B：代码实现】

---

## 工作流 A：需求分析与设计

### 输入
- 用户的任务描述（来自 /do 的 $ARGUMENTS 或对话上下文）
- 当前代码库状态（git status, 相关文件）

### 步骤

**步骤 1：理解需求**

重读任务描述，明确：
- 核心功能（What）：要做什么
- 用户场景（Why）：为什么要做
- 边界（What NOT）：明确不做什么

**步骤 2：探索代码库**

使用以下工具分析相关代码：
- `Glob` 查找相似功能的文件（如搜索 `**/*.md`, `**/*.json`）
- `Grep` 搜索相关关键词
- `Read` 阅读核心文件

重点关注：现有架构模式、命名惯例、与新功能的集成点。

**步骤 3：产出设计文档**

输出以下格式（必须完整填写，不可省略任何节）：

```
## 功能设计：[功能名称]

### 需求摘要
[1-2 句话描述要做什么]

### 实现方案
[描述技术方案，包括：使用哪些现有组件、新建哪些文件/函数、数据流向]

### 涉及文件
- 新建：[文件路径] — [职责]
- 修改：[文件路径] — [修改内容]
- 不动：[不需要修改的相关文件（避免误改）]

### 接口设计
[函数签名或 API 设计，含参数类型和返回值]

### 边界与异常处理
[哪些情况返回什么结果]

### 测试策略
[关键测试用例列表，含输入/预期输出，供 test-engineer 参考]
```

---

## 工作流 B：代码实现

### 前提条件

设计方案已经过人类审批（检查 TaskList，设计审批任务状态为 `completed`）。

### 输入
- 审批后的设计文档（在对话上下文中）
- 当前代码库状态

### 步骤

**步骤 1：逐一读取涉及文件**

对设计文档"涉及文件"列表中的每个文件，先 `Read` 再修改。禁止跳过此步骤。

**步骤 2：按设计实现**

- 严格按照设计文档中的"涉及文件"列表操作
- 不修改设计文档中未列出的文件
- 遵循现有代码风格和命名惯例
- 实现代码，测试由 test-engineer 负责（不需要在此阶段写测试）

**步骤 3：自检**

实现完成后检查：
- [ ] 设计文档中的所有文件是否都已处理
- [ ] 接口签名是否与设计一致
- [ ] 没有引入 `console.log`、`debugger` 或 `TODO` 注释

**步骤 4：产出实现摘要**

```
## 实现摘要

### 已创建/修改的文件
- [文件路径]：[修改内容一句话描述]

### 接口变更
[列出新增/修改的函数签名]

### 已知限制
[已知但暂未处理的边界情况，如有]

### 下一步
测试工程师请重点覆盖：[列出关键测试场景]
```

## 禁止事项

- 禁止修改设计文档未列出的文件
- 禁止在代码中留下 TODO/FIXME
- 禁止跳过"逐一读取涉及文件"步骤直接修改
- 禁止更改项目的技术栈或架构层次
````

- [ ] **Step 2: 验证**

```bash
grep -c "工作流" .claude/skills/agent-team/feature-developer.md
```

预期输出：`≥ 3`（工作流 A、工作流 B、当前任务判断各提及一次以上）

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/agent-team/feature-developer.md
git commit -m "feat: add feature-developer agent skill"
```

---

## Task 3：创建 maintenance-developer.md

**Files:**
- Create: `.claude/skills/agent-team/maintenance-developer.md`

- [ ] **Step 1: 写入 maintenance-developer.md**

文件内容（`.claude/skills/agent-team/maintenance-developer.md`）：

````markdown
# Maintenance Developer

## 角色

负责 bug 修复、代码重构和性能优化。分析问题根因，提出最小化修复方案并实现。

## 当前任务判断

读取当前 `in_progress` 的 TaskList 条目：
- 任务名含"诊断"/"分析"/"现状" → 执行【工作流 A：诊断/分析】
- 任务名含"修复"/"实现"/"重构" → 执行【工作流 B：实现】

---

## 工作流 A：问题诊断（bugfix 诊断阶段 / refactor 分析阶段）

### 步骤

**步骤 1：复现问题**

- 阅读任务描述中的错误信息/问题描述
- 用 `Grep` 搜索相关代码路径
- 用 `Read` 读取涉及文件

**步骤 2：追溯根因**

- 定位问题的直接原因（代码哪行）
- 识别深层原因（为什么会写出这段代码，是否有设计问题）

**步骤 3：产出诊断报告**

```
## 诊断报告

### 问题描述
[用户描述的问题一句话复述]

### 根因定位
- 文件：[路径:行号]
- 根因：[技术原因]
- 触发条件：[什么情况下会触发]

### 修复方案
**方案 A（推荐）**：[最小化修改，影响范围小]
- 修改文件：[路径]
- 修改方式：[具体改什么]
- 风险：[可能影响哪些地方]

**方案 B（备选）**：[如有备选方案]

### 重构范围（仅 refactor 类型）
[如果是重构，列出当前存在的代码质量问题，和建议的重构边界]
```

---

## 工作流 B：修复/重构实现

### 前提

诊断报告已确认（`in_progress` 任务前序任务状态为 `completed`）。

### 步骤

**步骤 1：逐一读取涉及文件**

对诊断报告中列出的所有修改文件，先 `Read` 再修改。

**步骤 2：实施最小化修复**

- bugfix：只改能修复问题的最少代码
- refactor：按事先确定的重构边界，不超范围

**步骤 3：运行测试（如有）**

从 `CLAUDE.md` 获取测试命令并运行，记录结果。

**步骤 4：产出修复摘要**

```
## 修复摘要

### 修改的文件
- [文件路径:行号范围]：[修改内容]

### 验证结果
[测试命令输出，或"项目无自动化测试"]

### 影响范围
[此次修改可能影响的其他功能点，供测试工程师参考]
```

## 禁止事项

- 禁止在修复 bug 时顺手重构无关代码
- 禁止在重构时修改功能逻辑
- 禁止在未读原始文件的情况下直接修改
````

- [ ] **Step 2: Commit**

```bash
git add .claude/skills/agent-team/maintenance-developer.md
git commit -m "feat: add maintenance-developer agent skill"
```

---

## Task 4：创建 test-engineer.md

**Files:**
- Create: `.claude/skills/agent-team/test-engineer.md`

- [ ] **Step 1: 写入 test-engineer.md**

文件内容（`.claude/skills/agent-team/test-engineer.md`）：

````markdown
# Test Engineer

## 角色

为代码变更编写和执行测试。遵循 TDD 原则，优先覆盖边界条件和失败路径。

## 当前任务判断

读取当前 `in_progress` 的 TaskList 条目：
- 任务名含"单元测试"/"回归测试"/"测试编写" → 执行【工作流 A：测试编写】
- 任务名含"覆盖率分析" → 执行【工作流 B：覆盖率分析】
- 任务名含"覆盖率验证" → 执行【工作流 C：覆盖率验证】

---

## 工作流 A：测试编写

### 步骤

**步骤 1：读取涉及文件**

读取上一阶段实现摘要中提到的所有修改文件。

**步骤 2：识别测试场景**

对每个函数/方法，列出：
- 正常路径（Happy Path）：标准输入 → 预期输出
- 边界条件：空值、最大值、最小值、空字符串
- 异常路径：错误输入、依赖失败

**步骤 3：查找现有测试文件**

用 `Glob` 查找现有测试文件：`**/*.test.*`、`**/*.spec.*`、`tests/**/*`。

遵循项目现有的测试框架和文件命名惯例。

**步骤 4：编写测试**

- 每个测试独立，不依赖其他测试的状态
- 测试名称描述行为：`test_当xxx时_应该xxx` 或 `it("should xxx when xxx")`
- 覆盖步骤 2 列出的所有场景

**步骤 5：运行测试（如有测试命令）**

从 `CLAUDE.md` 获取测试命令并运行，记录输出。

**步骤 6：产出测试报告**

```
## 测试报告

### 新增测试文件
- [文件路径]：[测试数量] 个测试

### 测试场景覆盖
| 场景 | 测试名称 | 状态 |
|------|---------|------|
| 正常路径 | test_xxx | PASS |
| 边界条件 | test_yyy | PASS |
| 异常路径 | test_zzz | PASS |

### 未覆盖场景（及原因）
[如有无法自动化的场景，说明原因]

### 测试命令
[运行所有相关测试的命令]
```

---

## 工作流 B：覆盖率分析

### 步骤

1. 查找项目的覆盖率工具（`CLAUDE.md`、`package.json`、`pytest.ini` 等）
2. 运行覆盖率命令，获取当前数据
3. 列出当前未覆盖的代码行/函数（重点标注公开接口）
4. 产出覆盖率分析报告：

```
## 覆盖率分析报告

### 当前覆盖率
- 总覆盖率：[XX%]
- 未覆盖的关键路径：
  - [文件路径:行号范围]：[该路径描述]

### 建议优先补测
[按重要性排列，最多 5 条]
```

---

## 工作流 C：覆盖率验证

运行覆盖率命令，对比补测前后的数字，输出是否达标：

```
## 覆盖率验证报告

补测前：[XX%]
补测后：[YY%]
变化：[+ZZ%]
结论：[达标（>= 目标值）/ 未达标（原因）]
```

## 禁止事项

- 禁止写只测试框架本身的"假测试"（如 `assert true`）
- 禁止测试私有实现细节（只测公开接口/行为）
- 禁止因测试难写而跳过边界条件
````

- [ ] **Step 2: Commit**

```bash
git add .claude/skills/agent-team/test-engineer.md
git commit -m "feat: add test-engineer agent skill"
```

---

## Task 5：创建 code-reviewer.md

**Files:**
- Create: `.claude/skills/agent-team/code-reviewer.md`

- [ ] **Step 1: 写入 code-reviewer.md**

文件内容（`.claude/skills/agent-team/code-reviewer.md`）：

````markdown
# Code Reviewer

## 角色

审查代码变更的质量。检查可读性、设计合理性、是否违反项目约束，给出具体可操作的修改建议。

---

## 工作流

### 步骤

**步骤 1：获取变更内容**

```bash
git diff HEAD
```

**步骤 2：读取 CLAUDE.md**

如果存在，读取 `CLAUDE.md` 中的约束和禁止事项。

**步骤 3：逐文件审查**

对每个变更文件，检查以下维度：

**可读性**
- [ ] 函数/变量命名是否自解释
- [ ] 单个函数是否超过 50 行（如是，标注）
- [ ] 是否有未删除的调试语句（`console.log`、`print`、`debugger`）

**设计合理性**
- [ ] 是否有重复代码（DRY 原则）
- [ ] 是否符合单一职责（一个函数只做一件事）
- [ ] 是否有魔法数字或魔法字符串（应定义为常量）
- [ ] 是否有不必要的全局状态

**项目约束合规**
- [ ] 是否违反 CLAUDE.md 中的禁止事项
- [ ] 是否引入了未经授权的新依赖
- [ ] 是否符合项目的架构分层规则

**步骤 4：产出审查报告**

```
## 代码审查报告

### 结论：[PASS / PASS_WITH_SUGGESTIONS / FAIL]

### 严重问题（必须修复，FAIL 的原因）
（格式：`[文件路径:行号] 问题描述。建议：具体怎么改。`）

### 建议改进（PASS_WITH_SUGGESTIONS，可选修复）
（同上格式）

### 亮点（值得保留或推广的写法）

### CLAUDE.md 合规：[合规 / 不合规（原因）]
```

**结论标准：**
- FAIL：存在任何严重问题（违反约束、安全漏洞、功能 bug）
- PASS_WITH_SUGGESTIONS：无严重问题，但有可改进之处
- PASS：代码质量良好，符合所有约束

## 禁止事项

- 禁止因个人偏好否决符合项目约束的代码
- 禁止在报告中只说"这里需要改进"而不给出具体建议
- 审查结论为 FAIL 时，必须列出 FAIL 的具体原因（文件路径 + 行号）
````

- [ ] **Step 2: Commit**

```bash
git add .claude/skills/agent-team/code-reviewer.md
git commit -m "feat: add code-reviewer agent skill"
```

---

## Task 6：创建 security-auditor.md

**Files:**
- Create: `.claude/skills/agent-team/security-auditor.md`

- [ ] **Step 1: 写入 security-auditor.md**

文件内容（`.claude/skills/agent-team/security-auditor.md`）：

````markdown
# Security Auditor

## 角色

审计代码变更的安全性和隐私合规性。重点关注数据泄露、认证缺失、依赖漏洞。

---

## 工作流

### 步骤

**步骤 1：获取变更内容**

```bash
git diff HEAD
```

**步骤 2：安全扫描**

逐变更文件检查以下维度：

**凭证与密钥**
- [ ] 是否有硬编码的密码、API Key、Token、Secret
- [ ] 是否有数据库连接字符串包含凭证
- [ ] 是否有私钥或证书内容

**数据安全**
- [ ] 是否有 PII（姓名、手机、身份证、邮箱）写入日志
- [ ] 敏感数据是否加密传输（HTTP vs HTTPS）
- [ ] 用户输入是否经过验证和清理（防 XSS、SQL 注入）

**认证与授权**
- [ ] 新增 API 端点是否有认证保护
- [ ] 是否有越权访问风险（A 用户能否操作 B 用户的数据）

**依赖安全**
- [ ] 是否新增了已知漏洞的依赖（如可运行 `npm audit` / `pip audit`，则运行并记录）

**步骤 3：产出安全审计报告**

```
## 安全审计报告

### 结论：[PASS / WARNING / FAIL]

### 高危问题（FAIL 的原因，必须修复）
（格式：`[文件路径:行号] 风险描述。修复建议：具体怎么做。`）

### 中危问题（WARNING，建议修复）
（同上）

### 低危提醒（可忽略或记录技术债）

### 已检查项（已确认安全的项目）
```

**结论标准：**
- FAIL：有高危问题（凭证泄露、未认证接口、注入漏洞等）
- WARNING：有中危问题（日志 PII、不必要的权限等）
- PASS：无安全问题

## 禁止事项

- 禁止因"项目内部使用"就跳过认证检查
- 禁止在报告中只写"存在安全风险"而不定位具体文件和行号
- 禁止在无法确认时假设"应该是安全的"
````

- [ ] **Step 2: Commit**

```bash
git add .claude/skills/agent-team/security-auditor.md
git commit -m "feat: add security-auditor agent skill"
```

---

## Task 7：创建 documentation-keeper.md

**Files:**
- Create: `.claude/skills/agent-team/documentation-keeper.md`

- [ ] **Step 1: 写入 documentation-keeper.md**

文件内容（`.claude/skills/agent-team/documentation-keeper.md`）：

````markdown
# Documentation Keeper

## 角色

保持项目文档与代码同步。更新 CLAUDE.md、API 文档和架构决策记录（ADR）。

---

## 工作流

### 步骤

**步骤 1：获取变更内容**

```bash
git diff HEAD
```

了解此次变更的范围。

**步骤 2：判断 CLAUDE.md 是否需要更新**

**需要更新的情况：**
- 新增了项目约束或禁止事项
- 修改了项目的技术栈或关键依赖
- 新增了重要的开发流程规范

**不需要更新的情况：**
- 只是普通功能实现
- 仅修改测试

**步骤 3：判断 API 文档是否需要更新**

如果变更包含：
- 新增函数/方法的公开接口 → 更新 `docs/knowledge/` 或相关文档
- 修改了现有接口的参数/返回值 → 更新对应文档
- 删除了接口 → 标记为废弃

**步骤 4：判断是否需要新 ADR**

**需要记录 ADR 的情况：**
- 做了重要的技术选型（选了 A 而不是 B）
- 修改了架构层次或模块边界
- 接受了某个技术债务

**ADR 格式：**

```markdown
## ADR-[编号]：[标题]

**日期**：YYYY-MM-DD
**状态**：已采纳

### 背景
[为什么要做这个决定]

### 决定
[做了什么决定]

### 后果
[这个决定带来的影响（正面和负面）]
```

**步骤 5：产出文档更新报告**

```
## 文档更新报告

### 已更新文件
- [文件路径]：[更新内容描述]

### 未更新（及原因）
- CLAUDE.md：[不需要更新的原因]

### 新增 ADR
[如有新增 ADR，列出编号和标题]
```

## 禁止事项

- 禁止更新与本次变更无关的文档
- 禁止在 CLAUDE.md 中加入过于细碎的规则（5 行以下的临时约定不值得记录）
- 禁止在"不需要更新"时强行修改文档凑数
````

- [ ] **Step 2: Commit**

```bash
git add .claude/skills/agent-team/documentation-keeper.md
git commit -m "feat: add documentation-keeper agent skill"
```

---

## Task 8：创建 devops-engineer.md

**Files:**
- Create: `.claude/skills/agent-team/devops-engineer.md`

- [ ] **Step 1: 写入 devops-engineer.md**

文件内容（`.claude/skills/agent-team/devops-engineer.md`）：

````markdown
# DevOps Engineer

## 角色

负责 CI/CD 预检、版本发布和部署流程。确保代码安全进入生产环境。

## 当前任务判断

- 任务名含"预检"/"检查" → 执行【工作流 A：预发布检查】
- 任务名含"发布"/"部署"/"release" → 执行【工作流 B：版本发布】

---

## 工作流 A：预发布检查

### 步骤

**步骤 1：检查测试状态**

如果 `CLAUDE.md` 有测试命令，运行并确认全绿。如果 CI/CD 配置文件存在（`.github/workflows/`、`Jenkinsfile` 等），读取并说明当前状态。

**步骤 2：检查变更完整性**

```bash
git status
```

确认：
- 没有未提交的变更（working tree clean）
- 没有遗留的 untracked 重要文件

**步骤 3：获取当前版本**

读取 `package.json` / `pyproject.toml` / `pom.xml` / `Cargo.toml` 等获取当前版本号。

根据此次变更类型建议下一个版本（遵循 semver）：
- PATCH（修复）：`x.y.Z+1`
- MINOR（新功能，向后兼容）：`x.Y+1.0`
- MAJOR（破坏性变更）：`X+1.0.0`

**步骤 4：产出预检报告**

```
## 预发布检查报告

### 测试状态：[全绿 / 有失败（N 个）/ 无测试]
### Git 状态：[干净 / 有未提交变更（说明）]
### 当前版本：[x.y.z]
### 建议版本：[x.y.z]（变更类型：PATCH/MINOR/MAJOR）
### 是否可以发布：[是 / 否（原因）]
```

---

## 工作流 B：版本发布

### 前提

预检报告显示"可以发布"，且人类已通过检查点确认。

### 步骤

**步骤 1**：更新版本号（`package.json` 或对应文件）

**步骤 2**：提交版本变更

```bash
git add <version-file>
git commit -m "chore: bump version to x.y.z"
```

**步骤 3**：创建 git tag

```bash
git tag -a vx.y.z -m "Release vx.y.z"
```

**步骤 4**：如有 `CHANGELOG.md`，更新本版本的变更说明

**步骤 5**：产出发布摘要

```
## 发布摘要

### 版本：v[x.y.z]
### Tag：v[x.y.z]
### 变更摘要：[本版本主要变更 3 条以内]
### 下一步：git push && git push --tags（需要人工执行）
```

## 禁止事项

- 禁止在测试失败时执行发布
- 禁止跳过预检直接进入发布工作流
- 禁止在人类未确认发布检查点的情况下创建 tag
- 禁止执行 `git push`（只做本地操作，推送由人工完成）
````

- [ ] **Step 2: Commit**

```bash
git add .claude/skills/agent-team/devops-engineer.md
git commit -m "feat: add devops-engineer agent skill"
```

---

## Task 9：创建 monitor.md

**Files:**
- Create: `.claude/skills/agent-team/monitor.md`

- [ ] **Step 1: 写入 monitor.md**

文件内容（`.claude/skills/agent-team/monitor.md`）：

````markdown
# Monitor

## 角色

监控测试健康度和代码覆盖率趋势。提供可量化的质量基准，标记回归风险。

---

## 工作流

### 步骤

**步骤 1：运行测试与覆盖率**

从 `CLAUDE.md` 或项目配置文件获取覆盖率命令并运行。如果无覆盖率工具，仅运行测试并记录通过/失败数。

**步骤 2：读取历史基准（如有）**

查找 `docs/feedback/coverage-baseline.md`，读取上次记录的覆盖率数据。

**步骤 3：计算变化**

```
当前覆盖率：XX%
基准覆盖率：YY%（上次记录时间：YYYY-MM-DD）
变化：[上升 +ZZ% / 下降 -ZZ% / 持平]
```

**步骤 4：标记回归**

如果覆盖率下降超过 5%，标记为"需要关注"并列出原因（哪些文件未覆盖）。

**步骤 5：更新基准**

将当前覆盖率和日期写入 `docs/feedback/coverage-baseline.md`：

```markdown
# 覆盖率基准

最后更新：YYYY-MM-DD

| 指标 | 数值 |
|------|------|
| 总覆盖率 | XX% |
| 通过测试数 | N |
| 失败测试数 | N |
```

**步骤 6：产出监控报告**

```
## 测试健康报告

### 测试结果
- 通过：[N] 个
- 失败：[N] 个
- 跳过：[N] 个

### 覆盖率
- 当前：[XX%]
- 基准：[YY%]
- 趋势：[上升↑ / 下降↓ / 持平→]

### 需要关注
[如有覆盖率下降或测试失败，列出具体问题]

### 基准已更新
docs/feedback/coverage-baseline.md（YYYY-MM-DD）
```

## 禁止事项

- 禁止在无覆盖率工具时伪造覆盖率数据（应写"无覆盖率工具"）
- 禁止跳过"更新基准"步骤
- 禁止只输出通过/失败数而不分析趋势
````

- [ ] **Step 2: Commit**

```bash
git add .claude/skills/agent-team/monitor.md
git commit -m "feat: add monitor agent skill"
```

---

## Task 10：创建 do.md 命令

**Files:**
- Create: `.claude/commands/do.md`

- [ ] **Step 1: 写入 do.md**

文件内容（`.claude/commands/do.md`）：

````markdown
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
````

- [ ] **Step 2: 验证命令文件结构**

```bash
head -5 .claude/commands/do.md
```

预期输出应包含 `allowed-tools:` 和 `description:` frontmatter。

- [ ] **Step 3: Commit**

```bash
git add .claude/commands/do.md
git commit -m "feat: add /do agent team command"
```

---

## Task 11：更新 INSTALL.md（添加 Phase 7）

**Files:**
- Modify: `INSTALL.md`（在文件末尾追加）

- [ ] **Step 1: 在 INSTALL.md 末尾追加 Phase 7**

在 INSTALL.md 当前最后一行（第 891 行）之后追加以下内容：

````markdown


---

## Phase 7：Agent Team（可选）

安装 `/do` 命令和 agent-team skill 文件集，为目标项目提供多 Agent 协作流水线能力。

用户通过 `/do <任务描述>` 启动协作流水线，支持 feature / bugfix / refactor / test / docs / deploy 七种任务类型，全程带人类审批检查点。

**Agent 执行步骤：**

1. 向用户介绍 Agent Team 能力：
   > "Phase 7（可选）：安装 `/do` 命令，支持多 Agent 协作执行开发任务（新功能、修复、重构、测试、文档、部署），全程带人类审批检查点。"

2. 询问用户是否安装：
   > "是否安装 Agent Team 能力？（回复'是'继续，或回复'跳过'略过此 Phase）"

3. 若用户选择跳过，直接跳至安装摘要输出。

4. 若用户确认安装，依次创建以下文件：

### 7.1 创建 `.claude/skills/agent-team/orchestrator.md`

    ---
    （内容与 .claude/skills/agent-team/orchestrator.md 完全一致，
     参见 harness 仓库的同名文件）
    ---

> **Agent 注意**：以下各小节的文件内容，从 harness 仓库对应的
> `.claude/skills/agent-team/` 目录下的同名文件中 WebFetch/Read 获取，
> 内容完全复制，不做任何修改。

### 7.2 创建 `.claude/skills/agent-team/feature-developer.md`

从 harness 仓库读取 `.claude/skills/agent-team/feature-developer.md` 并创建。

### 7.3 创建 `.claude/skills/agent-team/maintenance-developer.md`

从 harness 仓库读取 `.claude/skills/agent-team/maintenance-developer.md` 并创建。

### 7.4 创建 `.claude/skills/agent-team/test-engineer.md`

从 harness 仓库读取 `.claude/skills/agent-team/test-engineer.md` 并创建。

### 7.5 创建 `.claude/skills/agent-team/code-reviewer.md`

从 harness 仓库读取 `.claude/skills/agent-team/code-reviewer.md` 并创建。

### 7.6 创建 `.claude/skills/agent-team/security-auditor.md`

从 harness 仓库读取 `.claude/skills/agent-team/security-auditor.md` 并创建。

### 7.7 创建 `.claude/skills/agent-team/documentation-keeper.md`

从 harness 仓库读取 `.claude/skills/agent-team/documentation-keeper.md` 并创建。

### 7.8 创建 `.claude/skills/agent-team/devops-engineer.md`

从 harness 仓库读取 `.claude/skills/agent-team/devops-engineer.md` 并创建。

### 7.9 创建 `.claude/skills/agent-team/monitor.md`

从 harness 仓库读取 `.claude/skills/agent-team/monitor.md` 并创建。

### 7.10 创建 `.claude/commands/do.md`

从 harness 仓库读取 `.claude/commands/do.md` 并创建。

### 7.11 更新安装摘要

向用户展示已安装文件：
> "Agent Team 安装完成！
>
> **已创建的文件**：
> - `.claude/commands/do.md`
> - `.claude/skills/agent-team/orchestrator.md`
> - `.claude/skills/agent-team/feature-developer.md`
> - `.claude/skills/agent-team/maintenance-developer.md`
> - `.claude/skills/agent-team/test-engineer.md`
> - `.claude/skills/agent-team/code-reviewer.md`
> - `.claude/skills/agent-team/security-auditor.md`
> - `.claude/skills/agent-team/documentation-keeper.md`
> - `.claude/skills/agent-team/devops-engineer.md`
> - `.claude/skills/agent-team/monitor.md`
>
> **使用方式**：
> - `/do 添加用户登录功能` → 启动 feature 流水线
> - `/do 修复首页加载缓慢问题` → 启动 bugfix 流水线
> - `/do 重构数据库查询层` → 启动 refactor 流水线"

> 是否继续？（安装已完成，这是最后一个 Phase）"
````

- [ ] **Step 2: 验证追加结果**

```bash
grep -n "Phase 7" INSTALL.md
```

预期输出：`892:## Phase 7：Agent Team（可选）`（行号约为 893 附近）

- [ ] **Step 3: Commit**

```bash
git add INSTALL.md
git commit -m "feat: add Phase 7 (Agent Team) to INSTALL.md"
```

---

## 自检清单

完成以上所有任务后，运行以下验证：

```bash
# 验证所有 agent 文件都已创建
ls .claude/skills/agent-team/
# 预期：orchestrator.md feature-developer.md maintenance-developer.md
#        test-engineer.md code-reviewer.md security-auditor.md
#        documentation-keeper.md devops-engineer.md monitor.md

# 验证 /do 命令已创建
ls .claude/commands/
# 预期：commit-push.md do.md

# 验证 INSTALL.md 包含 Phase 7
grep "Phase 7" INSTALL.md
# 预期：## Phase 7：Agent Team（可选）
```
