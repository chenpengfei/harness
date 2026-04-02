# Phase 3：K — 知识

**Agent 执行步骤：**

### 3.1 创建或更新 CLAUDE.md

> **设计原则**：CLAUDE.md 是地图，不是内容。所有细节放在 `docs/` 下的专项文件中，CLAUDE.md 只保留指针和必须立即可见的约定。**保持 200 行以内**，避免淹没上下文。

检查目标项目根目录是否存在 `CLAUDE.md`：

**如果不存在**，创建 `CLAUDE.md`：

    # <PROJECT_NAME>

    <PROJECT_DESCRIPTION>

    ## 技术栈
    <TECH_STACK>

    ## 文档地图

    | 主题 | 文件 |
    |------|------|
    | 环境搭建与运行 | `.harness/environment/README.md` |
    | 本地配置 | `.harness/environment/setup.md` |
    | 系统架构 | `.harness/knowledge/architecture.md` |
    | 设计决策 | `.harness/knowledge/decisions/` |
    | 架构约束 | `.harness/constraints/README.md` |
    | 编码规范 | `.harness/constraints/coding-rules.md` |
    | Review 清单 | `.harness/feedback/review-checklist.md` |

    ## Agent 指令
    - 改动前先查上方文档地图中的相关条目
    - 写代码前检查 `.harness/constraints/coding-rules.md`
    - 重大设计决策记录在 `.harness/knowledge/decisions/`
    - **此文件保持 200 行以内**：细节放到 `docs/` 下对应文件

如果 `TEAM_SIZE = small` 或 `large`，在"Agent 指令"后追加：

    ## 协作约定
    - PR 必须通过 `.harness/feedback/review-checklist.md` 检查后才能合并
    - 重要设计决策记录在 `.harness/knowledge/decisions/`
    - 团队共识在合并前确认

如果 `PROJECT_STAGE = exploration`，在"Agent 指令"末尾追加一行：

    - 可以大胆探索，但在 `.harness/knowledge/decisions/` 记录选择理由

如果 `PROJECT_STAGE = production`，在"Agent 指令"末尾追加一行：

    - 修改生产代码前确认影响范围，不确定时先询问

**如果 CLAUDE.md 已存在**，在文件末尾追加：

    <!-- harness:start -->
    ## Harness 文档索引

    | 主题 | 文件 |
    |------|------|
    | 环境搭建与运行 | `.harness/environment/README.md` |
    | 本地配置 | `.harness/environment/setup.md` |
    | 系统架构 | `.harness/knowledge/architecture.md` |
    | 设计决策 | `.harness/knowledge/decisions/` |
    | 架构约束 | `.harness/constraints/README.md` |
    | 编码规范 | `.harness/constraints/coding-rules.md` |
    | Review 清单 | `.harness/feedback/review-checklist.md` |

    > 保持此文件 200 行以内，细节放到 `docs/` 下对应文件。
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
