# Harness 安装指南

> **本文件供 Agent 阅读执行。**
>
> 将本仓库 URL 提供给 Claude Code（或任何支持 WebFetch 的 Agent），告知其"按照该仓库的 INSTALL.md 指引安装 Harness 能力"，Agent 读取本文件后按阶段执行。

Harness 是一个 Agent-First 工程支架，通过 **E-K-C-F** 四个维度提升工程对 Agent 的友好度：

- **E**（Environment / 环境）：让 Agent 能运行、调试、测试、观察系统
- **K**（Knowledge / 知识）：文档和设计决策在仓库内可检索可维护
- **C**（Constraints / 约束）：架构规则约束演化方向
- **F**（Feedback / 回路）：日志、指标、评审直接反馈给 Agent

---

## Phase 0：前置检查

**Agent 执行步骤：**

1. 确认当前工作目录是目标项目的根目录。若不确定，向用户询问：
   > "当前目录是否为你希望安装 Harness 的项目根目录？（当前路径：[显示当前路径]）"

2. 检查 `.claude/harness-config.json` 是否存在：
   - **不存在**：这是首次安装，告知用户："准备在该项目中首次安装 Harness 能力，将涉及 4 个维度（E-K-C-F）的文档和 Claude Code 配置。"
   - **存在**：这是更新流程，告知用户上次安装时间和配置摘要，然后直接执行 Phase 1（走重新评估流程）。

3. 向用户确认：
   > "是否开始安装？（回复'是'继续，或告知需要调整的内容）"

4. 用户确认后，继续 Phase 1。

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

收集完 4 个答案后，创建 `.claude/` 目录（若不存在），然后创建 `.claude/harness-config.json`：

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

---

## Phase 2：E — 环境

**Agent 执行步骤：**

根据 Phase 1 收集的 `TECH_TYPE` 选择对应模板。

### 2.1 创建目录

在目标项目中创建 `docs/environment/` 目录（若不存在）。

### 2.2 创建 docs/environment/README.md

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

### 2.3 创建 docs/environment/setup.md

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
    1. Read `docs/environment/README.md` and `docs/environment/setup.md`
    2. Check what has changed (new dependencies, scripts, env vars)
    3. Update the relevant sections
    4. Ask the user to verify the commands are still accurate

    When auditing environment documentation:
    1. Check if the commands in `docs/environment/README.md` are current
    2. Check if prerequisites in `docs/environment/setup.md` are complete
    3. Report outdated or missing information

### 2.5 确认点

向用户展示已创建的文件：
> "E（环境）维度安装完成，创建了以下文件：
> - `docs/environment/README.md`
> - `docs/environment/setup.md`
> - `.claude/skills/harness-env.md`
>
> 是否继续安装 K（知识）维度？"

等待确认后继续 Phase 3.


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
    - 重要设计决策记录在 `docs/knowledge/decisions/`
    - 团队共识在合并前确认

所有配置追加以下内容：

    ## 运行项目
    参见 `docs/environment/README.md`。

    ## 架构
    参见 `docs/knowledge/architecture.md`。

    ## 约束
    参见 `docs/constraints/README.md`。

    ## Agent 指令
    - 修改代码前先阅读 `docs/` 中的相关文档
    - 写代码前检查 `docs/constraints/coding-rules.md`
    - Review 时使用 `docs/feedback/review-checklist.md`
    - 重大设计决策记录在 `docs/knowledge/decisions/`

如果 `PROJECT_STAGE = exploration`，在"Agent 指令"末尾追加：

    - 可以大胆探索，但在 `docs/knowledge/decisions/` 记录为什么做了这个选择

如果 `PROJECT_STAGE = production`，在"Agent 指令"末尾追加：

    - 修改生产代码前确认影响范围，不确定时先询问

**如果 CLAUDE.md 已存在**，在文件末尾追加（保留原有内容不变）：

    <!-- harness:start -->
    ## Harness 文档索引
    - 环境搭建：`docs/environment/README.md`
    - 系统架构：`docs/knowledge/architecture.md`
    - 架构约束：`docs/constraints/README.md`
    - Review 清单：`docs/feedback/review-checklist.md`
    - 设计决策：`docs/knowledge/decisions/`
    <!-- harness:end -->

### 3.2 创建目录结构

在目标项目中创建：
- `docs/knowledge/`
- `docs/knowledge/decisions/`

### 3.3 创建 docs/knowledge/architecture.md

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

    参见 `docs/knowledge/decisions/` 的架构决策记录（ADR）。

### 3.4 创建 docs/knowledge/decisions/README.md

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
    1. Create `docs/knowledge/decisions/YYYY-MM-DD-<topic>.md` using the ADR template
    2. Add an entry to the index in `docs/knowledge/decisions/README.md`

    When updating architecture documentation:
    1. Read `docs/knowledge/architecture.md`
    2. Identify what has changed (new components, changed data flow, new dependencies)
    3. Update relevant sections and confirm with the user

    When reviewing documentation completeness:
    1. Check if all major components are listed in `docs/knowledge/architecture.md`
    2. Check if significant recent decisions are recorded in `docs/knowledge/decisions/`
    3. Report gaps

### 3.6 确认点

向用户展示已创建/更新的文件：
> "K（知识）维度安装完成，创建/更新了以下文件：
> - `CLAUDE.md`（新建或追加了 Harness 索引）
> - `docs/knowledge/architecture.md`
> - `docs/knowledge/decisions/README.md`
> - `.claude/skills/harness-knowledge.md`
>
> 是否继续安装 C（约束）维度？"

等待确认后继续 Phase 4.


---

## Phase 4：C — 约束

**Agent 执行步骤：**

根据 `PROJECT_STAGE` 调整约束严格程度。

### 4.1 创建 docs/constraints/ 目录

### 4.2 创建 docs/constraints/README.md

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

### 4.3 创建 docs/constraints/coding-rules.md

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
> - `docs/constraints/README.md`
> - `docs/constraints/coding-rules.md`
>
> 是否继续安装 F（回路）维度？"

等待确认后继续 Phase 5.

---

## Phase 5：F — 回路

**Agent 执行步骤：**

根据 `TEAM_SIZE` 调整内容深度：solo 使用简化版，small/large 使用完整版。

### 5.1 创建 docs/feedback/ 目录

### 5.2 创建 docs/feedback/review-checklist.md

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
    - [ ] 是否遵循 `docs/constraints/coding-rules.md`
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
    - [ ] 重要设计决策是否记录在 `docs/knowledge/decisions/`？
    - [ ] CLAUDE.md 是否仍然准确？

### 5.3 创建 docs/feedback/retro-template.md

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
    - [ ] 有没有新的编码约束需要加入 `docs/constraints/`？
    - [ ] Agent 执行质量如何？有没有明显的知识缺口？
    - [ ] 回路是否有效？

### 5.4 创建 .claude/skills/harness-feedback.md

    ---
    name: harness-feedback
    description: Use this skill when recording issues, improvements, or feedback about the project or Harness setup.
    ---

    # Feedback and Retrospective Maintenance

    When asked to record an issue or improvement:
    1. Ask: "Is this a coding issue, a process issue, or a Harness/docs issue?"
    2. Coding issue → suggest adding to `docs/constraints/coding-rules.md` if it's a pattern to avoid
    3. Process issue → suggest adding to `docs/feedback/retro-template.md` as a standing agenda item
    4. Harness/docs issue → fix the relevant docs file directly

    When running a retrospective:
    1. Copy `docs/feedback/retro-template.md` to `docs/feedback/retro-YYYY-MM-DD.md`
    2. Walk through each section with the user
    3. For Harness improvement items, run or schedule `/harness`

    When reviewing whether Harness is working:
    1. Ask: "Are agents able to find what they need in docs/?"
    2. Ask: "Are there recurring questions from agents that should be documented?"
    3. Suggest specific files to update based on gaps

### 5.5 确认点

向用户展示已创建的文件：
> "F（回路）维度安装完成，创建了以下文件：
> - `docs/feedback/review-checklist.md`
> - `docs/feedback/retro-template.md`
> - `.claude/skills/harness-feedback.md`
>
> 所有 4 个维度已安装完成！最后一步：生成 `/harness` 更新命令。是否继续？"

等待确认后继续 Phase 6.
