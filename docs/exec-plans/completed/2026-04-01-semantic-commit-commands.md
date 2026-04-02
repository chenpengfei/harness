# Semantic Commit Commands 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 `/commit-push` 拆分为 `/commit`（Conventional Commits 语义化提交向导）和 `/push`（推送），并通过 Claude Code PreToolUse Hook 在 harness 及目标工程中强制验证提交消息格式。

**Architecture:** 新增 `.claude/commands/commit.md`、`push.md` 两个命令文件，新增 `.claude/hooks/validate-commit-msg.py` 作为 PreToolUse hook 拦截 `git commit` 命令并验证 Conventional Commits 格式，`.claude/settings.json` 注册 hook。安装流程（phase-6）同步更新，将上述四个文件部署到目标工程。

**Tech Stack:** Markdown（命令文件）、Python 3（hook 脚本）、JSON（settings 配置）

---

## 文件变更地图

| 操作 | 文件 |
|------|------|
| 新建 | `.claude/commands/commit.md` |
| 新建 | `.claude/commands/push.md` |
| 新建 | `.claude/hooks/validate-commit-msg.py` |
| 新建 | `.claude/settings.json` |
| 删除 | `.claude/commands/commit-push.md` |
| 修改 | `docs/install/phase-6-finalize.md` |
| 修改 | `INSTALL.md` |
| 修改 | `CLAUDE.md` |

---

## Task 1：创建 `/commit` 命令

**Files:**
- Create: `.claude/commands/commit.md`

- [ ] **Step 1：创建文件，写入完整内容**

创建 `.claude/commands/commit.md`，内容如下：

```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*), Bash(git diff:*), Bash(git log:*)
description: 按 Conventional Commits 规范创建语义化 git 提交
---

## 上下文

- 当前状态：!`git status`
- 当前变更：!`git diff HEAD`
- 最近提交：!`git log --oneline -10`

## 你的任务

基于以上变更，执行语义化提交。

### 第 1 步：选择 type

| type | 使用场景 |
|------|---------|
| `feat` | 新增功能或特性 |
| `fix` | 修复 bug |
| `docs` | 文档变更（含 README、注释） |
| `style` | 代码格式调整（不影响逻辑） |
| `refactor` | 代码重构（非 feat/fix） |
| `perf` | 性能优化 |
| `test` | 添加或修改测试 |
| `build` | 构建系统或外部依赖变更 |
| `ci` | CI 配置变更 |
| `chore` | 其他维护性工作 |
| `revert` | 回滚提交 |

### 第 2 步：构造提交消息

格式：`<type>[scope][!]: <中文描述>`

- scope 可选，描述影响范围（如模块名、文件名）
- `!` 表示破坏性变更（BREAKING CHANGE）
- 描述使用**中文**，祈使句

示例：
```
feat(auth): 新增 OAuth2 登录支持
fix(ui): 修复按钮点击后状态未更新的问题
docs: 更新 README 安装步骤
refactor(api): 重构用户服务以提升可维护性
chore: 升级依赖版本
```

### 第 3 步：暂存并提交

在单次响应中依次执行，不发送任何文字消息：

1. `git add` 暂存相关文件
2. `git commit -m "<构造好的消息>"`

不要创建分支，不要推送，不要做其他任何事情。
```

- [ ] **Step 2：验证文件存在且内容完整**

```bash
head -5 .claude/commands/commit.md
```

预期输出包含 `allowed-tools:` frontmatter 行。

- [ ] **Step 3：提交**

```bash
git add .claude/commands/commit.md
git commit -m "feat: 新增 /commit 语义化提交命令"
```

---

## Task 2：创建 `/push` 命令

**Files:**
- Create: `.claude/commands/push.md`

- [ ] **Step 1：创建文件，写入完整内容**

创建 `.claude/commands/push.md`，内容如下：

```markdown
---
allowed-tools: Bash(git push:*), Bash(git branch:*), Bash(git remote:*)
description: 将当前分支推送到 origin
---

## 上下文

- 当前分支：!`git branch --show-current`
- 远端状态：!`git remote -v`

## 你的任务

将当前分支推送到 origin：

1. 检查当前分支是否有 upstream tracking 分支
2. 若有：执行 `git push`
3. 若无：执行 `git push -u origin <branch>`

不要创建分支，不要创建 PR，不要做其他任何事情。
```

- [ ] **Step 2：验证文件存在**

```bash
head -5 .claude/commands/push.md
```

预期输出包含 `allowed-tools:` frontmatter 行。

- [ ] **Step 3：提交**

```bash
git add .claude/commands/push.md
git commit -m "feat: 新增 /push 推送命令"
```

---

## Task 3：创建 PreToolUse Hook 脚本

**Files:**
- Create: `.claude/hooks/validate-commit-msg.py`

- [ ] **Step 1：创建 hooks 目录**

```bash
mkdir -p .claude/hooks
```

- [ ] **Step 2：创建 hook 脚本**

创建 `.claude/hooks/validate-commit-msg.py`，内容如下：

```python
#!/usr/bin/env python3
"""
validate-commit-msg.py

Claude Code PreToolUse hook。
当 Bash 工具执行 git commit 命令时，验证提交消息是否符合
Conventional Commits 规范。不合规则拦截（exit 2）并打印说明。

Hook 输入（stdin）：
  {"session_id": "...", "tool_name": "Bash", "tool_input": {"command": "..."}}

退出码：
  0 — 放行
  2 — 拦截，并向 stdout 输出错误说明
"""
import sys
import json
import re


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    command: str = data.get("tool_input", {}).get("command", "")

    # 仅处理 git commit 命令
    if "git commit" not in command:
        sys.exit(0)

    # 提取 -m 参数的消息（支持单引号和双引号）
    m = re.search(r'-m\s+["\'](.+?)["\']', command)
    if not m:
        # 无 -m 参数（如编辑器模式），放行
        sys.exit(0)

    msg = m.group(1)

    # 验证 Conventional Commits 格式
    pattern = r'^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\(.+\))?(!)?: .+'
    if not re.match(pattern, msg):
        print("提交消息不符合 Conventional Commits 规范。")
        print("格式：<type>[scope][!]: <中文描述>")
        print("类型：feat  fix  docs  style  refactor  perf  test  build  ci  chore  revert")
        print("示例：feat(auth): 新增 OAuth2 登录支持")
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
```

- [ ] **Step 3：设置可执行权限**

```bash
chmod +x .claude/hooks/validate-commit-msg.py
```

- [ ] **Step 4：冒烟测试——合规消息**

```bash
echo '{"tool_name":"Bash","tool_input":{"command":"git commit -m \"feat(auth): 新增登录功能\""}}' \
  | python3 .claude/hooks/validate-commit-msg.py
echo "exit: $?"
```

预期输出：
```
exit: 0
```

- [ ] **Step 5：冒烟测试——不合规消息**

```bash
echo '{"tool_name":"Bash","tool_input":{"command":"git commit -m \"update something\""}}' \
  | python3 .claude/hooks/validate-commit-msg.py
echo "exit: $?"
```

预期输出：
```
提交消息不符合 Conventional Commits 规范。
格式：<type>[scope][!]: <中文描述>
类型：feat  fix  docs  style  refactor  perf  test  build  ci  chore  revert
示例：feat(auth): 新增 OAuth2 登录支持
exit: 2
```

- [ ] **Step 6：冒烟测试——非 commit 命令放行**

```bash
echo '{"tool_name":"Bash","tool_input":{"command":"git status"}}' \
  | python3 .claude/hooks/validate-commit-msg.py
echo "exit: $?"
```

预期输出：
```
exit: 0
```

- [ ] **Step 7：提交**

```bash
git add .claude/hooks/validate-commit-msg.py
git commit -m "feat: 新增 Conventional Commits 格式验证 hook"
```

---

## Task 4：注册 Hook 到 settings.json

**Files:**
- Create: `.claude/settings.json`

- [ ] **Step 1：创建 settings.json**

创建 `.claude/settings.json`，内容如下：

```json
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
```

- [ ] **Step 2：验证 JSON 格式合法**

```bash
python3 -c "import json; json.load(open('.claude/settings.json')); print('JSON valid')"
```

预期输出：
```
JSON valid
```

- [ ] **Step 3：提交**

```bash
git add .claude/settings.json
git commit -m "feat: 注册 PreToolUse hook 验证提交消息格式"
```

---

## Task 5：删除 `/commit-push` 命令

**Files:**
- Delete: `.claude/commands/commit-push.md`

- [ ] **Step 1：删除文件**

```bash
git rm .claude/commands/commit-push.md
```

- [ ] **Step 2：提交**

```bash
git commit -m "chore: 移除 /commit-push 命令（已拆分为 /commit 和 /push）"
```

---

## Task 6：更新 phase-6-finalize.md

**Files:**
- Modify: `docs/install/phase-6-finalize.md`

原步骤 6.1（"创建 .claude/commands/commit-push.md"）替换为四个子步骤。

- [ ] **Step 1：将 6.1 节替换为新的四个步骤**

将 `docs/install/phase-6-finalize.md` 中从 `### 6.1 创建 .claude/commands/commit-push.md` 到 `### 6.1.5` 之前的内容替换为：

```markdown
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

```

- [ ] **Step 2：更新 6.3 安装摘要中的文件列表**

在 6.3 节的"已创建的文件"列表中：
- 将 `> - \`.claude/commands/commit-push.md\`` 这一行替换为以下四行：
  ```
  > - `.claude/commands/commit.md`
  > - `.claude/commands/push.md`
  > - `.claude/hooks/validate-commit-msg.py`
  > - `.claude/settings.json`
  ```

- [ ] **Step 3：提交**

```bash
git add docs/install/phase-6-finalize.md
git commit -m "docs: 更新 phase-6 安装步骤以支持 /commit、/push 和 Semantic Commit hook"
```

---

## Task 7：更新 INSTALL.md 文件结构

**Files:**
- Modify: `INSTALL.md`

- [ ] **Step 1：替换 .claude/ 文件树部分**

将 `INSTALL.md` 中的 `.claude/` 文件树段落：

```
├── .claude/
│   ├── commands/
│   │   ├── commit-push.md             # /commit-push 命令
│   │   ├── harness.md                 # /harness 更新命令
│   │   ├── harness-feedback.md        # /harness-feedback 改进反馈命令
│   │   └── do.md                      # /do 命令（Phase 7 可选）
│   └── skills/
```

替换为：

```
├── .claude/
│   ├── commands/
│   │   ├── commit.md                  # /commit 命令
│   │   ├── push.md                    # /push 命令
│   │   ├── harness.md                 # /harness 更新命令
│   │   ├── harness-feedback.md        # /harness-feedback 改进反馈命令
│   │   └── do.md                      # /do 命令（Phase 7 可选）
│   ├── hooks/
│   │   └── validate-commit-msg.py     # Semantic Commit 格式验证 hook
│   ├── settings.json                  # Claude Code hook 注册配置
│   └── skills/
```

- [ ] **Step 2：提交**

```bash
git add INSTALL.md
git commit -m "docs: 更新 INSTALL.md 文件结构，反映新命令和 hook"
```

---

## Task 8：更新 CLAUDE.md 命令表

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1：替换命令表**

将 `CLAUDE.md` 中的命令表：

```markdown
| 命令 | 用途 |
|------|------|
| `/do` | 启动 Agent Team 协调器，分析任务并调度专业 agents |
| `/audit` | 检查仓库设计哲学与思想一致性（术语、硬链接、结构） |
| `/commit-push` | 创建 git commit 并推送到远端 |
| `/harness-feedback` | 记录改进建议并可选提交到仓库 |
```

替换为：

```markdown
| 命令 | 用途 |
|------|------|
| `/do` | 启动 Agent Team 协调器，分析任务并调度专业 agents |
| `/audit` | 检查仓库设计哲学与思想一致性（术语、硬链接、结构） |
| `/commit` | 按 Conventional Commits 规范创建语义化 git 提交 |
| `/push` | 将当前分支推送到 origin |
| `/harness-feedback` | 记录改进建议并可选提交到仓库 |
```

- [ ] **Step 2：提交**

```bash
git add CLAUDE.md
git commit -m "docs: 更新 CLAUDE.md 命令表，替换 /commit-push 为 /commit 和 /push"
```

---

## 完成验证

所有 task 完成后执行：

```bash
# 确认新文件存在
ls .claude/commands/commit.md .claude/commands/push.md
ls .claude/hooks/validate-commit-msg.py .claude/settings.json

# 确认旧文件已删除
ls .claude/commands/commit-push.md 2>&1 | grep -q "No such file" && echo "commit-push.md 已删除"

# 验证 hook 脚本仍可正常工作
echo '{"tool_name":"Bash","tool_input":{"command":"git commit -m \"feat: 验证\""}}' \
  | python3 .claude/hooks/validate-commit-msg.py && echo "hook OK"

# 验证 settings.json 格式合法
python3 -c "import json; json.load(open('.claude/settings.json')); print('settings.json OK')"
```
