# Harness 安装系统实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 创建完整的 `INSTALL.md` 安装剧本，使 Agent 能够通过 WebFetch 读取本仓库并为目标工程安装 E-K-C-F Harness 能力；同时更新 README.md 提供快速开始指引。

**Architecture:** 所有安装逻辑集中在 `INSTALL.md` 单一文件中，内嵌 6 个安装阶段的指令和所有文件模板。Agent 读取后线性执行，每阶段结束确认。`/harness` 命令的完整更新剧本内嵌在 Phase 6 生成的 `.claude/commands/harness.md` 模板中，安装后离线可用。

**Tech Stack:** Markdown, JSON

---

## 文件概览

| 文件 | 操作 | 说明 |
|------|------|------|
| `INSTALL.md` | 创建 | 主安装剧本，6 个阶段 + 所有模板 |
| `README.md` | 修改 | 补充安装快速开始部分 |

---

### Task 1: 创建 INSTALL.md 骨架 + Phase 0（前置检查）

**Files:**
- Create: `INSTALL.md`

- [ ] **Step 1: 创建 INSTALL.md，写入文件头和 Phase 0**

写入以下内容到 `INSTALL.md`（完整内容，从第一行开始）：

```
# Harness 安装指南

> **本文件供 Agent 阅读执行。**
>
> 将本仓库 URL 提供给 Claude Code（或任何支持 WebFetch 的 Agent），告知其"按照该仓库的 INSTALL.md 指引安装 Harness 能力"，Agent 读取本文件后按阶段执行。

Harness 是一个 Agent-First 工程支架，通过 **E-K-C-F** 四个维度提升工程对 Agent 的友好度：

- **E**（Environment / 环境）：让 Agent 能运行、调试、测试、观察系统
- **K**（Knowledge / 知识）：文档和设计决策在仓库内可检索可维护
- **C**（Constraints / 约束）：架构规则约束演化方向
- **F**（Feedback / 反馈）：日志、指标、评审直接反馈给 Agent

---

## Phase 0：前置检查

**Agent 执行步骤：**

1. 确认当前工作目录是目标项目的根目录。若不确定，向用户询问：
   > "当前目录是否为你希望安装 Harness 的项目根目录？（当前路径：[显示当前路径]）"

2. 检查 `.harness/harness-config.json` 是否存在：
   - **不存在**：这是首次安装，告知用户："准备在该项目中首次安装 Harness 能力，将涉及 4 个维度（E-K-C-F）的文档和 Claude Code 配置。"
   - **存在**：这是更新流程，告知用户上次安装时间和配置摘要，然后直接执行 Phase 1（走重新评估流程）。

3. 向用户确认：
   > "是否开始安装？（回复'是'继续，或告知需要调整的内容）"

4. 用户确认后，继续 Phase 1。
```

- [ ] **Step 2: 验证文件创建成功**

```bash
wc -l /Users/chenpengfei/projects/harness/INSTALL.md
```

期望：输出行数 > 30，无报错。

- [ ] **Step 3: 提交**

```bash
git -C /Users/chenpengfei/projects/harness add INSTALL.md
git -C /Users/chenpengfei/projects/harness commit -m "feat: add INSTALL.md skeleton and Phase 0 (preflight check)"
```

---

### Task 2: 追加 Phase 1（信息收集）

**Files:**
- Modify: `INSTALL.md`

- [ ] **Step 1: 在 INSTALL.md 末尾追加 Phase 1 内容**

追加以下内容（从 `---` 分隔线开始）：

```

---

## Phase 1：信息收集

**Agent 执行步骤：**

逐一向用户提问，等待回答后再问下一个。将所有答案记录在内存中供后续阶段使用。

### 问题 1：项目名称

> "请告诉我这个项目的名称，以及一句话描述它是做什么的。"
>
> 例如：「acr-service — 医院 AI 审核服务，自动化保险理赔审核流程」

记录为：`PROJECT_NAME` 和 `PROJECT_DESCRIPTION`

### 问题 2：技术栈

> "这个项目主要使用什么技术栈？（编程语言、主要框架）"
>
> 例如：「TypeScript / Next.js / PostgreSQL」或「Python / FastAPI / Redis」

记录为：`TECH_STACK`

技术栈类型识别规则（用于后续模板生成）：
- 含 node / npm / typescript / javascript / next / react / vue → `TECH_TYPE = nodejs`
- 含 python / fastapi / django / flask / uvicorn → `TECH_TYPE = python`
- 含 go / golang → `TECH_TYPE = go`
- 含 java / spring / maven / gradle → `TECH_TYPE = java`
- 其他 → `TECH_TYPE = generic`

### 问题 3：团队规模

> "项目团队规模是多少？"
>
> A. Solo（只有我一人）
> B. 小团队（2-5 人）
> C. 大团队（6 人以上）

记录为：`TEAM_SIZE`（solo / small / large）

### 问题 4：项目阶段

> "项目目前处于哪个阶段？"
>
> A. 早期探索（MVP/原型，快速变化）
> B. 产品迭代（功能稳定，持续迭代）
> C. 生产运营（线上系统，稳定性优先）

记录为：`PROJECT_STAGE`（exploration / iteration / production）

### 写入配置文件

收集完 4 个答案后，创建 `.harness/` 目录（若不存在），然后创建 `.harness/harness-config.json`：

```json
{
  "version": "1.0",
  "installedAt": "<当前 ISO 8601 时间戳，如 2026-03-29T10:00:00Z>",
  "updatedAt": "<当前 ISO 8601 时间戳>",
  "project": {
    "name": "<PROJECT_NAME>",
    "description": "<PROJECT_DESCRIPTION>"
  },
  "techStack": "<TECH_STACK>",
  "techType": "<TECH_TYPE>",
  "teamSize": "<TEAM_SIZE>",
  "projectStage": "<PROJECT_STAGE>"
}
```

向用户展示配置摘要，询问：
> "以上信息是否正确？确认后将开始安装第一个维度（E - 环境）。"

等待确认后继续 Phase 2。
```

注意：上方代码块内的 ```json 是 INSTALL.md 中用于展示 JSON 结构的代码块，写入时保留原样。

- [ ] **Step 2: 验证追加成功**

```bash
grep -n "## Phase" /Users/chenpengfei/projects/harness/INSTALL.md
```

期望输出：出现 `Phase 0` 和 `Phase 1` 两行。

- [ ] **Step 3: 提交**

```bash
git -C /Users/chenpengfei/projects/harness add INSTALL.md
git -C /Users/chenpengfei/projects/harness commit -m "feat: add Phase 1 (info collection) to INSTALL.md"
```

---

### Task 3: 追加 Phase 2（E — 环境）

**Files:**
- Modify: `INSTALL.md`

- [ ] **Step 1: 在 INSTALL.md 末尾追加 Phase 2 内容**

追加以下内容：

```

---

## Phase 2：E — 环境

**Agent 执行步骤：**

根据 Phase 1 收集的 `TECH_TYPE` 选择对应模板。

### 2.1 创建目录

在目标项目中创建 `.harness/environment/` 目录（若不存在）。

### 2.2 创建 .harness/environment/README.md

**如果 TECH_TYPE = nodejs，**文件内容为：

    # Environment

    ## Quick Start

        npm install
        npm run dev

    ## Running Tests

        npm test

    ## Debugging

        # 启动 Node.js inspector
        node --inspect src/index.js
        # 然后在 Chrome 中打开 chrome://inspect

    ## Observability

    Check console output for logs.

**如果 TECH_TYPE = python，**文件内容为：

    # Environment

    ## Quick Start

        pip install -r requirements.txt
        # 或使用 uv：
        uv sync

        python main.py
        # 或：
        uvicorn main:app --reload

    ## Running Tests

        pytest

    ## Debugging

        # 在代码中设置断点：
        import pdb; pdb.set_trace()

    ## Observability

    Check console output. Configure log level via LOG_LEVEL env var.

**如果 TECH_TYPE = go，**文件内容为：

    # Environment

    ## Quick Start

        go mod download
        go run ./cmd/main.go

    ## Running Tests

        go test ./...

    ## Debugging

        go install github.com/go-delve/delve/cmd/dlv@latest
        dlv debug ./cmd/main.go

    ## Observability

    Check stdout for logs. Use `slog` for structured logging.

**如果 TECH_TYPE = java，**文件内容为：

    # Environment

    ## Quick Start

        ./mvnw install -DskipTests
        ./mvnw spring-boot:run

    ## Running Tests

        ./mvnw test

    ## Debugging

        ./mvnw spring-boot:run -Dspring-boot.run.jvmArguments="-Xdebug -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=5005"

    ## Observability

    Check application logs. Spring Boot Actuator at /actuator.

**如果 TECH_TYPE = generic，**文件内容为：

    # Environment

    ## Quick Start

        # 在此填写安装依赖的命令
        # 在此填写启动项目的命令

    ## Running Tests

        # 在此填写测试命令

    ## Debugging

        > 描述本项目的调试工作流。

    ## Observability

        > 描述如何查看日志和观察系统状态。

### 2.3 创建 .harness/environment/setup.md

所有技术栈通用，将 `[PROJECT_NAME]` 替换为实际项目名：

    # Local Setup

    ## Prerequisites

    > 列出运行本项目前需要安装的工具和版本。

    - [工具 1 及版本]
    - [工具 2 及版本]

    ## First-Time Setup

    1. Clone 仓库
    2. [步骤 2]
    3. [步骤 3]

    ## Environment Variables

    在项目根目录创建 `.env` 文件：

        # 必填
        [VAR_NAME]=[说明]

        # 选填
        [VAR_NAME]=[说明]（默认值：[value]）

    ## Common Issues

    > 记录本地搭建时遇到的问题和解决方案。

    | 问题 | 解决方案 |
    |------|----------|
    | _(暂无)_ | |

### 2.4 创建 .claude/skills/harness-env.md

创建 `.claude/skills/` 目录（若不存在），然后创建 `.claude/skills/harness-env.md`：

    ---
    name: harness-env
    description: Use this skill when updating or auditing the environment documentation for this project.
    ---

    # Environment Documentation Maintenance

    When asked to update environment documentation:
    1. Read `.harness/environment/README.md` and `.harness/environment/setup.md`
    2. Check what has changed (new dependencies, scripts, env vars)
    3. Update the relevant sections
    4. Ask the user to verify the commands are still accurate

    When auditing environment documentation:
    1. Check if the commands in `.harness/environment/README.md` are current
    2. Check if prerequisites in `.harness/environment/setup.md` are complete
    3. Report outdated or missing information

### 2.5 确认点

向用户展示已创建的文件：
> "E（环境）维度安装完成，创建了以下文件：
> - `.harness/environment/README.md`
> - `.harness/environment/setup.md`
> - `.claude/skills/harness-env.md`
>
> 是否继续安装 K（知识）维度？"

等待确认后继续 Phase 3。
```

- [ ] **Step 2: 验证**

```bash
grep -c "## Phase" /Users/chenpengfei/projects/harness/INSTALL.md
```

期望输出：`3`

- [ ] **Step 3: 提交**

```bash
git -C /Users/chenpengfei/projects/harness add INSTALL.md
git -C /Users/chenpengfei/projects/harness commit -m "feat: add Phase 2 (E - Environment) to INSTALL.md"
```

---

### Task 4: 追加 Phase 3（K — 知识）

**Files:**
- Modify: `INSTALL.md`

- [ ] **Step 1: 在 INSTALL.md 末尾追加 Phase 3 内容**

追加以下内容：

```

---

## Phase 3：K — 知识

**Agent 执行步骤：**

### 3.1 创建或更新 CLAUDE.md

检查目标项目根目录是否存在 `CLAUDE.md`：

**如果不存在**，根据 `TEAM_SIZE` 和 `PROJECT_STAGE` 创建 `CLAUDE.md`：

基础模板（所有配置通用部分）：

    # <PROJECT_NAME>

    <PROJECT_DESCRIPTION>

    ## 技术栈
    <TECH_STACK>

    ## 项目结构
    > 随项目演化更新此部分。

    ## 关键约定
    > 在此记录编码约定和模式。

如果 `TEAM_SIZE = small` 或 `large`，在"关键约定"后追加：

    ## 协作约定
    - PR 必须通过 review-checklist 检查后才能合并
    - 重要设计决策记录在 `.harness/knowledge/decisions/`
    - 团队共识在合并前确认

所有配置追加以下内容：

    ## 运行项目
    参见 `.harness/environment/README.md`。

    ## 架构
    参见 `.harness/knowledge/architecture.md`。

    ## 约束
    参见 `.harness/constraints/README.md`。

    ## Agent 指令
    - 修改代码前先阅读 `docs/` 中的相关文档
    - 写代码前检查 `.harness/constraints/coding-rules.md`
    - Review 时使用 `.harness/feedback/review-checklist.md`
    - 重大设计决策记录在 `.harness/knowledge/decisions/`

如果 `PROJECT_STAGE = exploration`，在"Agent 指令"末尾追加：

    - 可以大胆探索，但在 `.harness/knowledge/decisions/` 记录为什么做了这个选择

如果 `PROJECT_STAGE = production`，在"Agent 指令"末尾追加：

    - 修改生产代码前确认影响范围，不确定时先询问

**如果 CLAUDE.md 已存在**，在文件末尾追加（保留原有内容不变）：

    <!-- harness:start -->
    ## Harness 文档索引
    - 环境搭建：`.harness/environment/README.md`
    - 系统架构：`.harness/knowledge/architecture.md`
    - 架构约束：`.harness/constraints/README.md`
    - Review 清单：`.harness/feedback/review-checklist.md`
    - 设计决策：`.harness/knowledge/decisions/`
    <!-- harness:end -->

### 3.2 创建目录结构

在目标项目中创建：
- `.harness/knowledge/`
- `.harness/knowledge/decisions/`

### 3.3 创建 .harness/knowledge/architecture.md

    # Architecture

    > 随系统演化保持此文档更新。

    ## 系统概述

    [描述这个系统做什么]

    ## 关键组件

    | 组件 | 职责 |
    |------|------|
    | _(待填写)_ | |

    ## 数据流

    [描述数据如何在系统中流动]

    ## 外部依赖

    [列出关键外部服务、API 或第三方库]

    ## 设计决策

    参见 `.harness/knowledge/decisions/` 的架构决策记录（ADR）。

### 3.4 创建 .harness/knowledge/decisions/README.md

    # 架构决策记录（ADR）

    本目录记录 <PROJECT_NAME> 的重大设计决策。

    ## 格式

    每个 ADR 为独立的 Markdown 文件，命名格式：`YYYY-MM-DD-<topic>.md`

    ### ADR 模板

        # [决策标题]

        **日期**：YYYY-MM-DD
        **状态**：提议 / 已采纳 / 已废弃

        ## 背景
        [为什么需要做这个决策？]

        ## 选项
        1. [选项 A]
        2. [选项 B]

        ## 决策
        选择 [选项 X]。

        ## 理由
        [为什么选择这个方案]

        ## 后果
        [这个决策带来的影响]

    ## 索引

    | 文件 | 主题 | 状态 |
    |------|------|------|
    | _(暂无)_ | | |

### 3.5 创建 .claude/skills/harness-knowledge.md

    ---
    name: harness-knowledge
    description: Use this skill when updating architecture documentation or recording design decisions.
    ---

    # Knowledge Documentation Maintenance

    When recording a design decision:
    1. Create `.harness/knowledge/decisions/YYYY-MM-DD-<topic>.md` using the ADR template
    2. Add an entry to the index in `.harness/knowledge/decisions/README.md`

    When updating architecture documentation:
    1. Read `.harness/knowledge/architecture.md`
    2. Identify what has changed (new components, changed data flow, new dependencies)
    3. Update relevant sections and confirm with the user

    When reviewing documentation completeness:
    1. Check if all major components are listed in `.harness/knowledge/architecture.md`
    2. Check if significant recent decisions are recorded in `.harness/knowledge/decisions/`
    3. Report gaps

### 3.6 确认点

向用户展示已创建/更新的文件：
> "K（知识）维度安装完成，创建/更新了以下文件：
> - `CLAUDE.md`（新建或追加了 Harness 索引）
> - `.harness/knowledge/architecture.md`
> - `.harness/knowledge/decisions/README.md`
> - `.claude/skills/harness-knowledge.md`
>
> 是否继续安装 C（约束）维度？"

等待确认后继续 Phase 4。
```

- [ ] **Step 2: 验证**

```bash
grep -c "## Phase" /Users/chenpengfei/projects/harness/INSTALL.md
```

期望输出：`4`

- [ ] **Step 3: 提交**

```bash
git -C /Users/chenpengfei/projects/harness add INSTALL.md
git -C /Users/chenpengfei/projects/harness commit -m "feat: add Phase 3 (K - Knowledge) to INSTALL.md"
```

---

### Task 5: 追加 Phase 4（C — 约束）

**Files:**
- Modify: `INSTALL.md`

- [ ] **Step 1: 在 INSTALL.md 末尾追加 Phase 4 内容**

追加以下内容：

```

---

## Phase 4：C — 约束

**Agent 执行步骤：**

根据 `PROJECT_STAGE` 调整约束严格程度。

### 4.1 创建 .harness/constraints/ 目录

### 4.2 创建 .harness/constraints/README.md

基础模板（所有配置通用）：

    # 约束

    <PROJECT_NAME> 的架构规则和边界。

如果 `PROJECT_STAGE = exploration`，在标题后追加：

    > 早期探索阶段，以下约束为指导原则而非硬性规定，随系统演化持续更新。

如果 `PROJECT_STAGE = production`，在标题后追加：

    > 生产系统。违反以下约束前请团队评审。

所有配置追加以下内容：

    ## 模块边界

    > 描述模块结构和允许的依赖关系。随架构演化填写。

    ## 依赖方向

    > 描述哪些模块可以依赖哪些模块（例如：UI → Business Logic → Data Access）。

    ## 禁止模式

    > 发现反模式时在此记录，附上原因。

    | 模式 | 原因 | 替代方案 |
    |------|------|----------|
    | _(暂无)_ | | |

    ## 命名约定

    > 关键命名规则。详细编码规范参见 `coding-rules.md`。

### 4.3 创建 .harness/constraints/coding-rules.md

基础模板（所有配置通用）：

    # 编码规范

    <PROJECT_NAME> 的编码规范和禁止模式。

如果 `PROJECT_STAGE = exploration`，追加：

    > 早期阶段：规范从实践中提炼，发现需要固定的模式时在此记录。

如果 `PROJECT_STAGE = production`，追加：

    > 生产代码标准：所有新代码必须遵守，重构旧代码时顺手改正。

所有配置追加通用规则：

    ## 通用规则

    - 函数单一职责：一个函数只做一件事
    - 不超过 3 层嵌套：超过时提取函数
    - 魔法数字必须命名为常量

如果 `TECH_TYPE = nodejs`，追加：

    ## TypeScript / JavaScript 规则

    - 使用 `const` 优先于 `let`，禁止 `var`
    - 异步代码使用 `async/await`，不用 `.then()` 链
    - catch 块必须记录错误，不允许空 catch

如果 `TECH_TYPE = python`，追加：

    ## Python 规则

    - 遵循 PEP 8
    - 新函数必须有类型注解
    - 捕获具体异常类型，不允许裸 `except:`

如果 `TECH_TYPE = go`，追加：

    ## Go 规则

    - 错误必须处理，不允许 `_ = err`
    - 接口定义在使用方，不在实现方
    - 避免 panic，使用 error 返回值

如果 `TECH_TYPE = java`，追加：

    ## Java 规则

    - 遵循 Google Java Style Guide
    - 使用 Optional 替代 null 返回
    - Checked exception 用于可恢复错误，unchecked 用于编程错误

所有配置追加：

    ## 禁止模式记录

    | 模式 | 原因 | 替代方案 |
    |------|------|----------|
    | _(发现问题时在此记录)_ | | |

### 4.4 确认点

向用户展示已创建的文件：
> "C（约束）维度安装完成，创建了以下文件：
> - `.harness/constraints/README.md`
> - `.harness/constraints/coding-rules.md`
>
> 是否继续安装 F（反馈）维度？"

等待确认后继续 Phase 5。
```

- [ ] **Step 2: 验证**

```bash
grep -c "## Phase" /Users/chenpengfei/projects/harness/INSTALL.md
```

期望输出：`5`

- [ ] **Step 3: 提交**

```bash
git -C /Users/chenpengfei/projects/harness add INSTALL.md
git -C /Users/chenpengfei/projects/harness commit -m "feat: add Phase 4 (C - Constraints) to INSTALL.md"
```

---

### Task 6: 追加 Phase 5（F — 反馈）

**Files:**
- Modify: `INSTALL.md`

- [ ] **Step 1: 在 INSTALL.md 末尾追加 Phase 5 内容**

追加以下内容：

```

---

## Phase 5：F — 反馈

**Agent 执行步骤：**

根据 `TEAM_SIZE` 调整内容深度：solo 使用简化版，small/large 使用完整版。

### 5.1 创建 .harness/feedback/ 目录

### 5.2 创建 .harness/feedback/review-checklist.md

**如果 TEAM_SIZE = solo：**

    # 自检清单

    提交代码前快速过一遍。

    ## 正确性
    - [ ] 是否实现了预期功能？
    - [ ] 边界条件处理了吗？

    ## 代码质量
    - [ ] 代码可读吗？
    - [ ] 有没有遗留调试代码（console.log、print、断点）？

    ## 测试
    - [ ] 核心逻辑有测试覆盖吗？
    - [ ] 测试通过了吗？

    ## 文档
    - [ ] 重要决策记录了吗？

**如果 TEAM_SIZE = small 或 large：**

    # Code Review 清单

    每个 PR/变更 Review 时使用本清单。

    ## 正确性
    - [ ] 是否实现了预期功能？
    - [ ] 边界条件是否处理？
    - [ ] 有没有明显的 bug？

    ## 代码质量
    - [ ] 可读性和自文档性
    - [ ] 是否遵循 `.harness/constraints/coding-rules.md`
    - [ ] 有无不必要的复杂度
    - [ ] 函数/类是否职责单一

    ## 测试
    - [ ] 是否有测试？
    - [ ] 测试是否覆盖主要行为和关键边界条件？
    - [ ] 测试通过了吗？

    ## 安全
    - [ ] 是否有敏感信息硬编码？
    - [ ] 输入是否有合适的验证？

    ## 文档
    - [ ] 重要设计决策是否记录在 `.harness/knowledge/decisions/`？
    - [ ] CLAUDE.md 是否仍然准确？

### 5.3 创建 .harness/feedback/retro-template.md

**如果 TEAM_SIZE = solo：**

    # 复盘模板

    > 每隔 1-2 周，或完成一个重要里程碑后使用。

    日期：YYYY-MM-DD
    主题：[这次复盘涵盖什么]

    ## 做得好的
    -

    ## 遇到的问题
    -

    ## 下次改进
    -

    ## Harness 改进
    - [ ] 有没有文档需要更新？
    - [ ] 有没有约束需要添加？
    - [ ] Agent 工作是否顺畅？

**如果 TEAM_SIZE = small 或 large：**

    # 复盘模板

    > Sprint/里程碑结束后使用。

    日期：YYYY-MM-DD
    Sprint/里程碑：[名称]
    参与者：[人员列表]

    ## 数据
    - 计划完成：X 项
    - 实际完成：Y 项
    - 未完成原因：

    ## 做得好的
    -

    ## 遇到的问题
    -

    ## 行动项
    | 行动 | 负责人 | 截止日期 |
    |------|--------|----------|
    | | | |

    ## Harness 改进
    - [ ] 有没有文档需要更新？（运行 `/harness` 重新评估）
    - [ ] 有没有新的编码约束需要加入 `.harness/constraints/`？
    - [ ] Agent 执行质量如何？有没有明显的知识缺口？
    - [ ] 反馈是否有效？

### 5.4 创建 .claude/skills/harness-feedback.md

    ---
    name: harness-feedback
    description: Use this skill when recording issues, improvements, or feedback about the project or Harness setup.
    ---

    # Feedback and Retrospective Maintenance

    When asked to record an issue or improvement:
    1. Ask: "Is this a coding issue, a process issue, or a Harness/docs issue?"
    2. Coding issue → suggest adding to `.harness/constraints/coding-rules.md` if it's a pattern to avoid
    3. Process issue → suggest adding to `.harness/feedback/retro-template.md` as a standing agenda item
    4. Harness/docs issue → fix the relevant docs file directly

    When running a retrospective:
    1. Copy `.harness/feedback/retro-template.md` to `.harness/feedback/retro-YYYY-MM-DD.md`
    2. Walk through each section with the user
    3. For Harness improvement items, run or schedule `/harness`

    When reviewing whether Harness is working:
    1. Ask: "Are agents able to find what they need in docs/?"
    2. Ask: "Are there recurring questions from agents that should be documented?"
    3. Suggest specific files to update based on gaps

### 5.5 确认点

向用户展示已创建的文件：
> "F（反馈）维度安装完成，创建了以下文件：
> - `.harness/feedback/review-checklist.md`
> - `.harness/feedback/retro-template.md`
> - `.claude/skills/harness-feedback.md`
>
> 所有 4 个维度已安装完成！最后一步：生成 `/harness` 更新命令。是否继续？"

等待确认后继续 Phase 6。
```

- [ ] **Step 2: 验证**

```bash
grep -c "## Phase" /Users/chenpengfei/projects/harness/INSTALL.md
```

期望输出：`6`

- [ ] **Step 3: 提交**

```bash
git -C /Users/chenpengfei/projects/harness add INSTALL.md
git -C /Users/chenpengfei/projects/harness commit -m "feat: add Phase 5 (F - Feedback) to INSTALL.md"
```

---

### Task 7: 追加 Phase 6（收尾 + /harness 命令模板）

**Files:**
- Modify: `INSTALL.md`

- [ ] **Step 1: 在 INSTALL.md 末尾追加 Phase 6 内容**

追加以下内容：

```

---

## Phase 6：收尾

**Agent 执行步骤：**

### 6.1 创建 .claude/commands/harness.md

创建 `.claude/commands/` 目录（若不存在），然后创建 `.claude/commands/harness.md`，内容如下（这是用户之后运行 `/harness` 时 Agent 将执行的完整脚本）：

    # Harness 更新

    本命令用于重新评估项目的 Harness 配置并更新已安装的能力。

    ## 步骤

    ### 步骤 1：读取现有配置

    读取 `.harness/harness-config.json`，加载上次记录的配置：
    - 项目信息（名称、描述）
    - 技术栈（techStack、techType）
    - 团队规模（teamSize）
    - 项目阶段（projectStage）

    若 `.harness/harness-config.json` 不存在，告知用户：
    > "未找到 Harness 配置文件。请先通过安装流程初始化 Harness（参见 https://github.com/[repo]/harness）。"
    然后停止执行。

    ### 步骤 2：重新评估

    逐一向用户提问，展示上次的答案，用户可直接回车确认或输入新值：

    > **重新评估 Harness 配置**（上次更新：[读取 updatedAt 字段]）
    >
    > 问题 1：项目名称和描述
    > 上次：[project.name] — [project.description]
    > （直接回车确认，或输入新值）

    > 问题 2：技术栈
    > 上次：[techStack]
    > （直接回车确认，或输入新值）

    > 问题 3：团队规模（solo / 小团队 / 大团队）
    > 上次：[teamSize]
    > （直接回车确认，或输入新值）

    > 问题 4：项目阶段（早期探索 / 产品迭代 / 生产运营）
    > 上次：[projectStage]
    > （直接回车确认，或输入新值）

    ### 步骤 3：差异分析

    对比新旧答案，确定需要更新的文件：

    | 变化 | 受影响的文件 |
    |------|------------|
    | 技术栈变化 | `.harness/environment/README.md`、`.harness/constraints/coding-rules.md` |
    | teamSize: solo → small/large | `CLAUDE.md`（添加协作约定）、`.harness/feedback/review-checklist.md`（升级完整版）、`.harness/feedback/retro-template.md`（升级完整版）|
    | teamSize: small/large → solo | `CLAUDE.md`（移除协作约定）、`.harness/feedback/` 文件简化 |
    | projectStage: exploration → iteration/production | `.harness/constraints/README.md`（加强约束描述）、`.harness/constraints/coding-rules.md`（加强规范）、`CLAUDE.md`（更新 Agent 指令）|
    | projectStage: production/iteration → exploration | `.harness/constraints/README.md`（放宽描述）、`CLAUDE.md`（更新 Agent 指令）|

    ### 步骤 4：呈现变更计划

    向用户展示建议更新的文件清单：
    > "根据以上变化，建议更新以下文件：
    > 1. [文件路径] — [更新理由]
    > 2. [文件路径] — [更新理由]
    >
    > 是否执行更新？"

    若无任何变化，告知：
    > "当前配置与上次完全一致，无需更新。"
    然后停止。

    ### 步骤 5：执行更新

    更新原则：
    - 不删除用户已自定义的内容
    - 找到 Harness 生成的标记区域（如 `<!-- harness:start -->` ... `<!-- harness:end -->`）进行替换
    - 无法确定是否用户自定义内容时，向用户询问

    更新 `.harness/harness-config.json`：
    - 更新 `updatedAt` 为当前时间戳
    - 更新所有变化的字段

    ### 步骤 6：打印摘要

    > "Harness 更新完成。
    >
    > 更新了 N 个文件：
    > - [文件路径]
    > - ...
    >
    > 当前配置：[techStack] | [teamSize] | [projectStage]"

### 6.2 打印安装摘要

向用户展示完整的安装摘要：
> "Harness 安装完成！
>
> **项目**：<PROJECT_NAME>
> **安装的维度**：E（环境）/ K（知识）/ C（约束）/ F（反馈）
>
> **已创建的文件**：
> - `.harness/harness-config.json`
> - `.claude/commands/harness.md`
> - `.claude/skills/harness-env.md`
> - `.claude/skills/harness-knowledge.md`
> - `.claude/skills/harness-feedback.md`
> - `CLAUDE.md`
> - `.harness/environment/README.md`
> - `.harness/environment/setup.md`
> - `.harness/knowledge/architecture.md`
> - `.harness/knowledge/decisions/README.md`
> - `.harness/constraints/README.md`
> - `.harness/constraints/coding-rules.md`
> - `.harness/feedback/review-checklist.md`
> - `.harness/feedback/retro-template.md`
>
> **下一步建议**：
> 1. 填写 `CLAUDE.md` 中的项目结构和关键约定
> 2. 更新 `.harness/environment/README.md` 中的具体命令（若有占位符）
> 3. 随项目演化，运行 `/harness` 持续更新配置"
```

- [ ] **Step 2: 验证 INSTALL.md 完整性**

```bash
grep -c "## Phase" /Users/chenpengfei/projects/harness/INSTALL.md
```

期望输出：`7`（Phase 0 至 Phase 6）

```bash
grep "harness.md" /Users/chenpengfei/projects/harness/INSTALL.md | head -5
```

期望：出现 `.claude/commands/harness.md` 相关内容。

- [ ] **Step 3: 提交**

```bash
git -C /Users/chenpengfei/projects/harness add INSTALL.md
git -C /Users/chenpengfei/projects/harness commit -m "feat: add Phase 6 (wrap-up + /harness command template) to INSTALL.md"
```

---

### Task 8: 更新 README.md 安装指引

**Files:**
- Modify: `README.md`

- [ ] **Step 1: 读取当前 README.md**

读取 `/Users/chenpengfei/projects/harness/README.md`，确认末尾有 `# 安装指南` 标题但内容为空。

- [ ] **Step 2: 将 README.md 中空的安装指南部分替换为完整内容**

找到文件末尾的以下内容：

```
---
# 安装指南
```

替换为：

```
---

# 安装指南

将以下指令复制给你的 Agent（Claude Code 或其他支持 WebFetch 的 Agent）：

```
请读取 https://raw.githubusercontent.com/<your-username>/harness/main/INSTALL.md
并按照其中的指引，在当前项目目录下安装 Harness 能力。
```

Agent 会自动完成安装，过程中会逐步向你确认每个阶段。

## 更新已安装的 Harness

安装完成后，在 Claude Code 中运行：

```
/harness
```

该命令会重新评估你的项目配置，并根据变化更新相应的文档和配置。

## 手动参考

若需了解安装详情，可直接查阅 INSTALL.md。
```

- [ ] **Step 3: 验证**

```bash
grep -n "安装指南" /Users/chenpengfei/projects/harness/README.md
grep "raw.githubusercontent" /Users/chenpengfei/projects/harness/README.md
```

期望：两个命令都有匹配输出。

- [ ] **Step 4: 提交**

```bash
git -C /Users/chenpengfei/projects/harness add README.md
git -C /Users/chenpengfei/projects/harness commit -m "docs: add installation quickstart to README.md"
```

---

## 完成验证

所有任务完成后，运行以下检查：

```bash
# 检查 INSTALL.md 有 7 个 Phase
grep -c "## Phase" /Users/chenpengfei/projects/harness/INSTALL.md

# 检查 README.md 有安装说明
grep -c "INSTALL.md" /Users/chenpengfei/projects/harness/README.md

# 查看提交历史
git -C /Users/chenpengfei/projects/harness log --oneline -10
```

期望：
- 第一条命令输出 `7`
- 第二条命令输出 > 0
- 第三条命令显示 8 个新提交
