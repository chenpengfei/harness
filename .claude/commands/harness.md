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

### 步骤 5.5：刷新 Harness 文件

从配置中读取 `rawBaseUrl` 字段：

**若 `rawBaseUrl` 为空**，打印提示并跳过本步骤：
> "未配置 rawBaseUrl，跳过文件刷新。如需同步最新内容，请在 `.harness/harness-config.json` 中填写 `rawBaseUrl` 字段（例如 `https://cdn.jsdelivr.net/gh/chenpengfei/harness@main`）。"

**否则**，直接将 `rawBaseUrl` 作为 raw 文件 URL 前缀（例如 `https://cdn.jsdelivr.net/gh/owner/repo@main`）。

> **提示**：如果 `raw.githubusercontent.com` 访问缓慢（例如中国大陆），可将 `rawBaseUrl` 设置为 `https://cdn.jsdelivr.net/gh/owner/repo@main` 以使用 jsDelivr CDN 加速。

通过 WebFetch 依次拉取以下文件，并覆盖目标项目中对应文件（强制覆盖，不保留旧版本）：

| 拉取路径（拼接到前缀后） | 目标工程路径 |
|----------------------|------------|
| `/.claude/commands/commit.md` | `.claude/commands/commit.md` |
| `/.claude/commands/push.md` | `.claude/commands/push.md` |
| `/.claude/commands/harness.md` | `.claude/commands/harness.md` |
| `/.claude/hooks/validate-commit-msg.py` | `.claude/hooks/validate-commit-msg.py` |
| `/.harness/constraints/README.md` | `.harness/constraints/README.md` |
| `/.harness/environment/README.md` | `.harness/environment/README.md` |
| `/.harness/feedback/README.md` | `.harness/feedback/README.md` |
| `/.harness/knowledge/README.md` | `.harness/knowledge/README.md` |

若某个文件 WebFetch 失败（网络错误、仓库私有等），记录该文件路径，继续处理其余文件；所有文件处理完毕后，在步骤 6 的摘要中汇报哪些文件刷新失败。

> **说明**：上述文件由 harness 统一维护，目标项目不应手动修改，每次 `/harness` 更新时强制覆盖以获取最新版本。

### 步骤 6：打印摘要

> "Harness 更新完成。
>
> 更新了 N 个文件：
> - [文件路径]
> - ...
>
> 当前配置：[techStack] | [teamSize] | [projectStage]"
