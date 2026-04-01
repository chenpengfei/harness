# Phase 6：收尾

**Agent 执行步骤：**

### 6.1a 创建 .claude/commands/commit.md

从 harness 仓库读取 `.claude/commands/commit.md` 并创建到目标项目。

> **Agent 注意**：通过 WebFetch 或 Read 从 harness 仓库对应路径读取文件内容，完全复制，不做任何修改。

### 6.1b 创建 .claude/commands/push.md

从 harness 仓库读取 `.claude/commands/push.md` 并创建到目标项目。

> **Agent 注意**：通过 WebFetch 或 Read 从 harness 仓库对应路径读取文件内容，完全复制，不做任何修改。

### 6.1c 创建 .claude/hooks/validate-commit-msg.py

1. 在目标项目中创建 `.claude/hooks/` 目录（若不存在）
2. 从 harness 仓库读取 `.claude/hooks/validate-commit-msg.py` 并创建到目标项目
3. 设置可执行权限：`chmod +x .claude/hooks/validate-commit-msg.py`

> **Agent 注意**：通过 WebFetch 或 Read 从 harness 仓库对应路径读取文件内容，完全复制，不做任何修改。

### 6.1d 写入或合并 .claude/settings.json

检查目标项目是否存在 `.claude/settings.json`：

**若不存在**，创建文件，内容如下：

    {
      "hooks": {
        "PreToolUse": [
          {
            "matcher": "Bash",
            "hooks": [
              {
                "type": "command",
                "command": "python3 .claude/hooks/validate-commit-msg.py"
              }
            ]
          }
        ]
      }
    }

**若已存在**，读取现有内容，在 `hooks.PreToolUse` 数组中追加以下对象（若相同 matcher 的 hook 尚不存在）：

    {
      "matcher": "Bash",
      "hooks": [
        {
          "type": "command",
          "command": "python3 .claude/hooks/validate-commit-msg.py"
        }
      ]
    }

写回文件，保持原有配置不变。

### 6.1.5 创建 .claude/commands/harness-feedback.md

从 harness 仓库读取 `.claude/commands/harness-feedback.md` 并创建到目标项目。

> **Agent 注意**：通过 WebFetch 或 Read 从 harness 仓库对应路径读取文件内容，完全复制，不做任何修改。

### 6.1.8 更新 .gitignore

在目标项目根目录的 `.gitignore` 文件末尾追加以下内容（若 `.gitignore` 不存在则创建）：

    # Harness 改进建议草稿（本地存档，不提交到目标项目代码库）
    .harness/proposals/
    .harness/submitted/

### 6.2 创建 .claude/commands/harness.md

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

    更新 `.harness/harness-config.json`：
    - 更新 `updatedAt` 为当前时间戳
    - 更新所有变化的字段

    ### 步骤 5.5：刷新 Harness 命令文件

    从配置中读取 `harnessRepo` 字段：

    **若 `harnessRepo` 为空**，打印提示并跳过本步骤：
    > "未配置 harnessRepo，跳过命令文件刷新。如需同步最新命令，请在 `.harness/harness-config.json` 中填写 `harnessRepo` 字段。"

    **若 `harnessRepo` 非空**，先构造 raw 文件 URL 的前缀：
    - 若格式为 `git@github.com:owner/repo.git`，提取 `owner/repo`，前缀为 `https://raw.githubusercontent.com/owner/repo/main`
    - 若格式为 HTTPS 地址（含 `github.com/`），提取 `github.com/` 后的 `owner/repo`（去掉 `.git` 后缀），前缀同上

    再通过 WebFetch 依次拉取以下文件，并覆盖目标项目中对应文件（强制覆盖，不保留旧版本）：

    | 拉取路径（拼接到前缀后） | 目标工程路径 |
    |----------------------|------------|
    | `/.claude/commands/commit.md` | `.claude/commands/commit.md` |
    | `/.claude/commands/push.md` | `.claude/commands/push.md` |
    | `/.claude/commands/harness-feedback.md` | `.claude/commands/harness-feedback.md` |
    | `/.claude/hooks/validate-commit-msg.py` | `.claude/hooks/validate-commit-msg.py` |

    若某个文件 WebFetch 失败（网络错误、仓库私有等），记录该文件路径，继续处理其余文件；所有文件处理完毕后，在步骤 6 的摘要中汇报哪些文件刷新失败。

    > **说明**：上述文件由 harness 统一维护，目标项目不应手动修改，每次 `/harness` 更新时强制覆盖以获取最新版本。

    > **注意**：`harness.md`（本命令自身）在当前执行中无法自我更新，下次运行 `/harness` 时才会使用新版本。若需立即生效，可在获取到 `harness.md` 的最新内容后手动覆盖 `.claude/commands/harness.md`。

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
> - `.harness/harness-config.json`
> - `.claude/commands/commit.md`
> - `.claude/commands/push.md`
> - `.claude/hooks/validate-commit-msg.py`
> - `.claude/settings.json`
> - `.claude/commands/harness.md`
> - `.claude/commands/harness-feedback.md`
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
> 3. 随项目演化，运行 `/harness` 持续更新配置
> 4. 运行 `/harness-feedback` 随时记录实践中发现的改进点"
