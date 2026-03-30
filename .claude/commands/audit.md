---
allowed-tools: Read, Glob, Grep, AskUserQuestion, Edit, Bash(git log:*)
description: 检查 harness 仓库设计哲学、思想的一致性
---

## 环境检查

用 Glob 检查根目录是否同时存在 `INSTALL.md` 和 `ARCHITECTURE.md`。

若两者不同时存在，停止执行并输出以下错误：

    错误：当前目录不是 harness 仓库。
    /audit 命令仅适用于 harness 仓库本身，请在 harness 仓库根目录下运行。

若两者均存在，继续执行后续区块。

---

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
若发现 `人类控制`、`用户控制`、`人工介入`，标记为 `[需人工确认] <文件名:行号> 使用了 "X"，请确认是否应统一为"人类掌舵"`

**术语组 4 — Agent 执行表述**
标准写法：`Agent 执行`（`智能体执行` 在 README 标语中为合法变体，不标记）
标记不一致：`AI 执行`、`自动执行`

**术语组 5 — 安装后依赖表述**
标准写法：`安装后无依赖` 或 `安装后无运行时依赖`
用 Grep 搜索 `无运行时依赖`、`安装后脱离依赖` 等变体，若与标准写法在不同文件中混用，记录：`[文件名:行号] 发现 "X"，全仓库通用表述为 "安装后无依赖"`

每个发现记录格式：`[文件名:行号] 发现 "X"，全仓库通用表述为 "Y"`
无问题时记录：`✓ 术语一致性检查通过`

---

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

读取 `INSTALL.md`，用 Grep 搜索模式 `docs/install/phase-[0-9]+-[a-z-]+\.md` 提取所有 phase 文件路径引用，去重后逐一用 Glob 检查对应文件是否存在。

每个"INSTALL.md 引用但磁盘不存在"的路径记录：
`[引用断裂] INSTALL.md 引用了 <路径>，但该文件不存在`

### 2.3 设计文档索引

用 Glob 检查 `docs/design-docs/index.md` 是否存在。若不存在，记录：
`[缺失] docs/design-docs/index.md 不存在`

无问题时记录：`✓ 结构完整性检查通过`

---

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

无问题时记录：`✓ 原则遵守检查通过`

---
