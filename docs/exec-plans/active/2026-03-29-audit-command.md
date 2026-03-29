# /audit 命令实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 创建 `.claude/commands/audit.md` 命令，在 harness 仓库中通过三轮扫描检查设计哲学一致性，暂停询问用户授权后自动修复。

**Architecture:** 单文件 Markdown 命令，无可执行代码。命令文件分五个逻辑区块：环境检查、三轮扫描（术语/结构/原则）、报告输出、修复授权。Agent 读取命令后按区块顺序执行，使用 Glob/Grep/Read 收集信息，AskUserQuestion 获取修复授权，Edit 执行修复。

**Tech Stack:** Claude Code command（Markdown），工具：Read, Glob, Grep, AskUserQuestion, Edit, Bash(git log:*)

> **注意：** 本计划不涉及传统单元测试（harness 是纯内容仓库）。每个任务的"验证"步骤通过直接读取产出文件、检查内容完整性来替代。端到端验证在最后一个任务中通过运行命令完成。

---

## 文件清单

| 操作 | 路径 |
|------|------|
| 创建 | `.claude/commands/audit.md` |

---

### Task 1：命令骨架 + 环境检查区块

**Files:**
- Create: `.claude/commands/audit.md`

- [ ] **Step 1：创建文件，写入 front matter 和环境检查区块**

创建 `.claude/commands/audit.md`，内容如下：

```markdown
---
allowed-tools: Read, Glob, Grep, AskUserQuestion, Edit, Bash(git log:*)
description: 检查 harness 仓库设计哲学、思想的一致性
---

## 环境检查

用 Glob 检查根目录是否同时存在 `INSTALL.md` 和 `ARCHITECTURE.md`。

若两者不同时存在，停止执行并输出以下错误：

```
错误：当前目录不是 harness 仓库。
/audit 命令仅适用于 harness 仓库本身，请在 harness 仓库根目录下运行。
```

---
```

- [ ] **Step 2：验证文件已创建，front matter 正确**

读取 `.claude/commands/audit.md`，确认：
- front matter 包含 `allowed-tools` 和 `description`
- 环境检查区块包含"停止执行"分支

- [ ] **Step 3：提交**

```bash
git add .claude/commands/audit.md
git commit -m "feat: add /audit command skeleton with environment check"
```

---

### Task 2：第一轮扫描——术语一致性

**Files:**
- Modify: `.claude/commands/audit.md`

- [ ] **Step 1：在 Task 1 内容末尾追加第一轮扫描区块**

在 `audit.md` 的 `---` 分隔线后追加：

```markdown
## 第一轮：术语一致性

用 Glob 列出全仓库所有 `.md` 文件（`**/*.md`，排除 `.git/` 目录），逐一读取，检查以下五组术语的一致性：

**术语组 1 — E-K-C-F 框架名称**
标准写法：`E-K-C-F`
标记不一致：`EKCF`、`E/K/C/F`、`ekc-f` 等不同写法同时出现在仓库中

**术语组 2 — 四个维度中文名称**
标准对应：E=环境、K=知识、C=约束、F=回路
标记不一致：将 F 对应"反馈"而非"回路"，或将 C 对应"限制"而非"约束"

**术语组 3 — 人类主导表述**
标准写法：`人类掌舵`
标记不一致：在明显应使用"人类掌舵"概念的语境中出现`人类控制`、`用户控制`、`人工介入`

**术语组 4 — Agent 执行表述**
标准写法：`Agent 执行`
标记不一致：`AI 执行`、`智能体执行`、`自动执行`

**术语组 5 — 安装后依赖表述**
标准写法：`安装后无依赖` 或 `安装后无运行时依赖`
标记不一致：含义相同但措辞明显不同的表述同时出现

每个发现记录格式：`[文件名:行号] 发现 "X"，全仓库通用表述为 "Y"`
无问题时记录：`✓ 术语一致性检查通过`

---
```

- [ ] **Step 2：验证追加内容完整**

读取 `audit.md`，确认五组术语条目和记录格式均存在。

- [ ] **Step 3：提交**

```bash
git add .claude/commands/audit.md
git commit -m "feat: add Round 1 terminology consistency check to /audit"
```

---

### Task 3：第二轮扫描——结构完整性

**Files:**
- Modify: `.claude/commands/audit.md`

- [ ] **Step 1：追加第二轮扫描区块**

在 `audit.md` 末尾追加：

```markdown
## 第二轮：结构完整性

### 2.1 Phase 文件完整性

用 Glob 检查以下 8 个文件是否存在：

- `docs/install/phase-0-preflight.md`
- `docs/install/phase-1-info-collection.md`
- `docs/install/phase-2-environment.md`
- `docs/install/phase-3-knowledge.md`
- `docs/install/phase-4-constraints.md`
- `docs/install/phase-5-feedback.md`
- `docs/install/phase-6-finalize.md`
- `docs/install/phase-7-agent-team.md`

每个缺失的文件记录：`[缺失] <路径> 不存在`

### 2.2 INSTALL.md 引用完整性

读取 `INSTALL.md`，用 Grep 提取所有 `docs/install/phase-*.md` 格式的路径引用，逐一用 Glob 检查对应文件是否存在。

每个"INSTALL.md 引用但磁盘不存在"的路径记录：
`[引用断裂] INSTALL.md 引用了 <路径>，但该文件不存在`

### 2.3 设计文档索引

用 Glob 检查 `docs/design-docs/index.md` 是否存在。若不存在，记录：
`[缺失] docs/design-docs/index.md 不存在`

无问题时记录：`✓ 结构完整性检查通过`

---
```

- [ ] **Step 2：验证追加内容完整**

读取 `audit.md`，确认三个子检查（2.1/2.2/2.3）和所有 8 个 phase 文件路径均存在。

- [ ] **Step 3：提交**

```bash
git add .claude/commands/audit.md
git commit -m "feat: add Round 2 structural completeness check to /audit"
```

---

### Task 4：第三轮扫描——原则遵守

**Files:**
- Modify: `.claude/commands/audit.md`

- [ ] **Step 1：追加第三轮扫描区块（6 条原则）**

在 `audit.md` 末尾追加：

```markdown
## 第三轮：原则遵守

### 原则 1：仓库不含可执行代码

用 Glob 搜索全仓库（排除 `.git/`）中以下扩展名的文件：
`.js`、`.ts`、`.jsx`、`.tsx`、`.py`、`.sh`、`.rb`、`.go`、`.java`、`.rs`、`.c`、`.cpp`

若发现匹配文件，记录：`[违反原则 1] 发现可执行代码文件：<路径>`

### 原则 2：命令文件不依赖外部 URL

用 Grep 在 `INSTALL.md` 和 `.claude/commands/` 下所有 `.md` 文件中搜索 `http://` 或 `https://`。

若发现外部 URL，记录：`[违反原则 2] <文件名:行号> 含外部 URL：<URL>`

### 原则 3：INSTALL.md 是单一真相来源

读取 `INSTALL.md` 中的"安装流程地图"表格，提取各 Phase 行的名称和描述。
读取每个 `docs/install/phase-*.md` 的首行标题（`#` 开头的行）。

若某 phase 文件的标题与 INSTALL.md 对应行描述明显矛盾（如阶段目的不同），记录：
`[违反原则 3] <phase 文件> 标题与 INSTALL.md 描述不匹配：INSTALL.md 写 "<A>"，文件写 "<B>"`

无法机械判断的情况标记为：`[需人工确认] 请核查 <phase 文件> 与 INSTALL.md 的一致性`

### 原则 4：文档使用符号名称而非硬链接

用 Grep 搜索所有 `.md` 文件中形如 `](../` 且目标以 `.md)` 结尾的内容，以及形如 `](./` 且目标以 `.md)` 结尾的内容。

若发现，记录：`[违反原则 4] <文件名:行号> 使用了内部硬链接：<链接完整文本>`

### 原则 5：do.md 保留完整人类审批检查点

读取 `.claude/commands/do.md`，用 Grep 检查以下三个检查点的特征词是否存在：

- 设计审批：`设计方案审批` 或 `批准，开始实现`
- 实现确认：`实现已完成` 或 `继续全部`
- PR 审批：`PR 合并审批` 或 `批准合并`

若任一特征词均不存在（两个关键词都找不到），记录：
`[违反原则 5] do.md 缺少 <检查点名称>（特征词 "<词1>" 和 "<词2>" 均未找到）`

### 原则 6：设计变更有对应记录

执行 `git log --oneline -20` 获取最近 20 条提交记录。
用 Glob 读取 `docs/design-docs/` 下所有文件名（格式为 `YYYY-MM-DD-*.md`）。

对每条包含 `feat:` 或 `refactor:` 前缀的提交，检查 `docs/design-docs/` 中是否存在日期相近（提交日期 ±3 天以内）的设计文档。

若无对应文档，标记为：
`[需人工确认] 提交 "<提交信息>" 是否需要 docs/design-docs/ 记录？`

---
```

- [ ] **Step 2：验证 6 条原则均已写入**

读取 `audit.md`，确认原则 1-6 标题和检查逻辑均存在。

- [ ] **Step 3：提交**

```bash
git add .claude/commands/audit.md
git commit -m "feat: add Round 3 principle adherence check to /audit (6 principles)"
```

---

### Task 5：报告输出 + 修复授权区块

**Files:**
- Modify: `.claude/commands/audit.md`

- [ ] **Step 1：追加报告输出和修复授权区块**

在 `audit.md` 末尾追加：

```markdown
## 输出报告

汇总三轮扫描结果，按以下格式输出（将 N 替换为实际问题数量）：

---
## 哲学一致性审查报告

### 第一轮：术语一致性  [N 个问题]
（列出所有发现；无问题时写"✓ 未发现问题"）

### 第二轮：结构完整性  [N 个问题]
（列出所有发现；无问题时写"✓ 未发现问题"）

### 第三轮：原则遵守  [N 个问题]
（列出所有发现，含 [违反原则X] 和 [需人工确认] 两类；无问题时写"✓ 未发现问题"）

---
共发现 X 个问题（其中 Y 项需人工确认）
---

若三轮均无任何问题，输出替换为：

✓ 未发现哲学一致性问题，当前 harness 仓库状态健康。

---

## 修复授权

若三轮中存在**可自动修复**的问题（即 [违反原则X] 或术语不一致类，非 [需人工确认] 类），使用 AskUserQuestion 暂停：

问题：是否执行自动修复？
选项：
- 全部修复（修复三轮中所有可自动修复的问题）
- 选择轮次修复（由用户指定修复第几轮）
- 仅查看报告，不修复

根据用户选择，使用 Edit 工具执行具体修复（替换不一致术语、修正引用路径等）。

修复完成后输出：

---
## 修复摘要
修改了 N 个文件，共 M 处变更：
- <文件名>：<修改描述>
---

若所有问题均为 [需人工确认]，跳过 AskUserQuestion，直接输出需手动处理的项目清单后结束。
```

- [ ] **Step 2：验证报告模板和修复流程均已写入**

读取 `audit.md`，确认"输出报告"和"修复授权"两个区块存在，AskUserQuestion 三个选项均在文件中。

- [ ] **Step 3：提交**

```bash
git add .claude/commands/audit.md
git commit -m "feat: add report format and fix authorization flow to /audit"
```

---

### Task 6：端到端验证

**Files:**
- Read: `.claude/commands/audit.md`（最终状态核查）

- [ ] **Step 1：读取并核查完整命令文件**

读取 `.claude/commands/audit.md`，逐区块确认：
1. front matter 包含正确的 allowed-tools 和 description
2. 环境检查区块存在
3. 第一轮含 5 组术语定义
4. 第二轮含 2.1/2.2/2.3 三个子检查
5. 第三轮含原则 1-6（各含具体检查指令）
6. 报告模板完整（含三轮子标题格式）
7. 修复授权含三个选项

- [ ] **Step 2：在 harness 仓库运行命令，观察输出**

在 Claude Code 中运行 `/audit`，确认命令：
- 通过环境检查（INSTALL.md + ARCHITECTURE.md 存在）
- 完成三轮扫描并输出报告
- 对任何可自动修复的发现触发 AskUserQuestion

- [ ] **Step 3：最终提交**

```bash
git add .claude/commands/audit.md
git commit -m "feat: complete /audit philosophy consistency command"
```
