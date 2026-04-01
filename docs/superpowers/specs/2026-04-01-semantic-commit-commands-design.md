# 设计文档：/commit 与 /push 命令及 Semantic Commit Messages 支持

**日期**：2026-04-01
**状态**：已批准

---

## 背景

原有 `/commit-push` 命令将暂存、提交、推送合并在一个命令中，且无语义化格式约束。本设计将其拆分为独立的 `/commit` 和 `/push` 命令，并通过 Conventional Commits 规范和 Claude Code PreToolUse Hook 实现语义化提交消息的强制验证，同时将此能力通过安装流程部署到目标工程。

---

## 变更范围

### 删除

- `.claude/commands/commit-push.md`

### 新建（harness 自身）

- `.claude/commands/commit.md` — 语义化提交向导
- `.claude/commands/push.md` — 推送到 origin
- `.claude/hooks/validate-commit-msg.sh` — PreToolUse 验证 hook
- `.claude/settings.json` — hook 注册配置

### 修改

- `docs/install/phase-6-finalize.md` — 安装步骤更新
- `INSTALL.md` — 文件结构说明更新
- `CLAUDE.md` — 可用命令表更新

---

## 命令设计

### `/commit`

**allowed-tools**：`Bash(git add:*)`, `Bash(git status:*)`, `Bash(git commit:*)`, `Bash(git diff:*)`, `Bash(git log:*)`

**行为：**

1. 读取 `git status`、`git diff HEAD`、最近 10 条提交历史
2. 分析变更性质，推断合适的 type
3. 构造符合以下格式的提交消息（描述使用中文）：
   ```
   <type>[scope][!]: <中文描述>
   ```
4. 执行 `git add` 暂存变更，然后 `git commit -m "<message>"`
5. PreToolUse hook 自动拦截并验证消息格式

**支持的 type：**

| type | 含义 |
|------|------|
| `feat` | 新功能 |
| `fix` | Bug 修复 |
| `docs` | 文档变更 |
| `style` | 代码格式（不影响逻辑） |
| `refactor` | 重构 |
| `perf` | 性能优化 |
| `test` | 测试相关 |
| `build` | 构建/依赖变更 |
| `ci` | CI 配置变更 |
| `chore` | 其他维护性工作 |
| `revert` | 回滚 |

**示例消息：**
```
feat(auth): 新增 OAuth2 登录支持
fix(ui): 修复按钮点击后状态未更新的问题
docs: 更新 README 安装步骤
refactor(api): 重构用户服务以提升可维护性
```

---

### `/push`

**allowed-tools**：`Bash(git push:*)`, `Bash(git branch:*)`, `Bash(git remote:*)`

**行为：**

1. 读取当前分支名
2. 执行 `git push origin <branch>`
3. 若当前分支无 upstream，使用 `git push -u origin <branch>`

---

## Hook 设计

### 文件：`.claude/hooks/validate-commit-msg.sh`

**触发：** PreToolUse，matcher = `Bash`

**验证正则：**
```
^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\(.+\))?(!)?: .+
```

**逻辑：**

```
stdin JSON
  → 提取 tool_input.command
  → 包含 git commit？
      否 → exit 0（放行）
      是 → 提取 -m 消息
          → 正则验证
              合规 → exit 0
              不合规 → exit 2 + 打印中文说明
```

**拒绝时输出：**
```
提交消息不符合 Conventional Commits 规范。
格式：<type>[scope][!]: <中文描述>
类型：feat fix docs style refactor perf test build ci chore revert
示例：feat(auth): 新增 OAuth2 登录支持
```

### 文件：`.claude/settings.json`

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash .claude/hooks/validate-commit-msg.sh"
          }
        ]
      }
    ]
  }
}
```

---

## 安装流程调整

### `docs/install/phase-6-finalize.md` 变更

原步骤 6.1（复制 `commit-push.md`）替换为：

**6.1a** 复制 `.claude/commands/commit.md` 到目标项目
**6.1b** 复制 `.claude/commands/push.md` 到目标项目
**6.1c** 复制 `.claude/hooks/validate-commit-msg.sh`，创建 `.claude/hooks/` 目录，设置可执行权限（`chmod +x`）
**6.1d** 写入或合并 `.claude/settings.json`：
- 若文件不存在：直接写入完整 settings.json
- 若文件已存在：合并 `hooks.PreToolUse` 数组，不覆盖已有配置

### `INSTALL.md` 文件结构更新

```
.claude/
├── commands/
│   ├── commit.md              # /commit 命令
│   ├── push.md                # /push 命令
│   ├── harness.md
│   ├── harness-feedback.md
│   └── do.md                  # Phase 7 可选
└── hooks/
    └── validate-commit-msg.sh # Semantic Commit 格式验证
```

### Phase 6 安装摘要（6.3）更新

移除 `commit-push.md`，新增：
- `.claude/commands/commit.md`
- `.claude/commands/push.md`
- `.claude/hooks/validate-commit-msg.sh`
- `.claude/settings.json`

---

## 影响范围

| 文件 | 操作 |
|------|------|
| `.claude/commands/commit-push.md` | 删除 |
| `.claude/commands/commit.md` | 新建 |
| `.claude/commands/push.md` | 新建 |
| `.claude/hooks/validate-commit-msg.sh` | 新建 |
| `.claude/settings.json` | 新建 |
| `docs/install/phase-6-finalize.md` | 修改 |
| `INSTALL.md` | 修改 |
| `CLAUDE.md` | 修改 |
