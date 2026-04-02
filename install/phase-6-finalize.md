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

### 6.1.8 更新 .gitignore

检查目标项目根目录的 `.gitignore` 文件，确保其中 **不存在** 忽略 `.harness/` 目录的规则（如 `.harness/` 或 `.harness`）。

若存在此类规则，将其删除。

> **说明**：`.harness/` 目录包含 E-K-C-F 四维度文档及 Harness 配置，必须纳入目标项目的版本控制。

### 6.2 创建 .claude/commands/harness.md

从 harness 仓库读取 `.claude/commands/harness.md` 并创建到目标项目。

> **Agent 注意**：通过 WebFetch 或 Read 从 harness 仓库对应路径读取文件内容，完全复制，不做任何修改。

### 6.3 打印安装摘要

向用户展示完整的安装摘要：
> "Harness 安装完成！
>
> **项目**：<PROJECT_NAME>
> **安装的维度**：E（环境）/ K（知识）/ C（约束）/ F（反馈）
>
> **已创建的文件**：
> - `.harness/harness-config.json`
> - `.harness/environment/README.md`
> - `.harness/environment/setup.md`
> - `.harness/knowledge/architecture.md`
> - `.harness/knowledge/decisions/README.md`
> - `.harness/constraints/README.md`
> - `.harness/constraints/coding-rules.md`
> - `.harness/feedback/review-checklist.md`
> - `.harness/feedback/retro-template.md`
> - `.claude/commands/commit.md`
> - `.claude/commands/push.md`
> - `.claude/commands/harness.md`
> - `.claude/hooks/validate-commit-msg.py`
> - `.claude/settings.json`
> - `.claude/skills/harness-env.md`
> - `.claude/skills/harness-knowledge.md`
> - `CLAUDE.md`
>
> **下一步建议**：
> 1. 填写 `CLAUDE.md` 中的项目结构和关键约定
> 2. 更新 `.harness/environment/README.md` 中的具体命令（若有占位符）
> 3. 随项目演化，运行 `/harness` 持续更新配置"
