# Phase 6：收尾

**Agent 执行步骤：**

### 6.1 创建 .claude/commands/commit-push.md

从 harness 仓库读取 `.claude/commands/commit-push.md` 并创建到目标项目。

> **Agent 注意**：通过 WebFetch 或 Read 从 harness 仓库对应路径读取文件内容，完全复制，不做任何修改。

### 6.2 创建 .claude/commands/harness.md

创建 `.claude/commands/` 目录（若不存在），然后创建 `.claude/commands/harness.md`，内容如下（这是用户之后运行 `/harness` 时 Agent 将执行的完整脚本）：

    # Harness 更新

    本命令用于重新评估项目的 Harness 配置并更新已安装的能力。

    ## 步骤

    ### 步骤 1：读取现有配置

    读取 `.claude/harness-config.json`，加载上次记录的配置：
    - 项目信息（名称、描述）
    - 技术栈（techStack、techType）
    - 团队规模（teamSize）
    - 项目阶段（projectStage）

    若 `.claude/harness-config.json` 不存在，告知用户：
    > "未找到 Harness 配置文件。请先通过安装流程初始化 Harness。"
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
    | 技术栈变化 | `docs/environment/README.md`、`docs/constraints/coding-rules.md` |
    | teamSize: solo → small/large | `CLAUDE.md`（添加协作约定）、`docs/feedback/review-checklist.md`（升级完整版）、`docs/feedback/retro-template.md`（升级完整版）|
    | teamSize: small/large → solo | `CLAUDE.md`（移除协作约定）、`docs/feedback/` 文件简化 |
    | projectStage: exploration → iteration/production | `docs/constraints/README.md`（加强约束描述）、`docs/constraints/coding-rules.md`（加强规范）、`CLAUDE.md`（更新 Agent 指令）|
    | projectStage: production/iteration → exploration | `docs/constraints/README.md`（放宽描述）、`CLAUDE.md`（更新 Agent 指令）|

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

    更新 `.claude/harness-config.json`：
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

### 6.3 打印安装摘要

向用户展示完整的安装摘要：
> "Harness 安装完成！
>
> **项目**：<PROJECT_NAME>
> **安装的维度**：E（环境）/ K（知识）/ C（约束）/ F（回路）
>
> **已创建的文件**：
> - `.claude/harness-config.json`
> - `.claude/commands/commit-push.md`
> - `.claude/commands/harness.md`
> - `.claude/skills/harness-env.md`
> - `.claude/skills/harness-knowledge.md`
> - `.claude/skills/harness-feedback.md`
> - `CLAUDE.md`
> - `docs/environment/README.md`
> - `docs/environment/setup.md`
> - `docs/knowledge/architecture.md`
> - `docs/knowledge/decisions/README.md`
> - `docs/constraints/README.md`
> - `docs/constraints/coding-rules.md`
> - `docs/feedback/review-checklist.md`
> - `docs/feedback/retro-template.md`
>
> **下一步建议**：
> 1. 填写 `CLAUDE.md` 中的项目结构和关键约定
> 2. 更新 `docs/environment/README.md` 中的具体命令（若有占位符）
> 3. 随项目演化，运行 `/harness` 持续更新配置"
