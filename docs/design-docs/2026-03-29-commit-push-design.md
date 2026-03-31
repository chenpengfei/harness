# /commit-push 命令设计文档

**日期**：2026-03-29
**状态**：已批准

---

## 概述

`/commit-push` 是一个 Agent 工具命令，安装到目标项目的 `.claude/commands/commit-push.md`，供用户一键完成"暂存所有变更 → 生成提交信息 → 推送到远端"流程，无需手动编写 git 命令。

---

## 设计目标

- **零手动操作**：用户运行 `/commit-push` 后，Agent 自动读取变更、生成提交信息、推送，无需用户介入
- **风格一致**：提交信息参照仓库近期 commit 历史，保持格式统一
- **最小权限**：命令只允许使用 git 相关 bash 操作，不允许任何其他 shell 命令

---

## 行为规范

1. 读取 `git status`、`git diff HEAD`、当前分支、最近 10 条 commit
2. 根据变更内容和历史风格，自动生成一条提交信息
3. 暂存所有变更（`git add -A`），提交，推送到 origin
4. 不创建新分支，不创建 PR，不输出多余文本

---

## allowed-tools 限制

```yaml
allowed-tools:
  - Bash(git add:*)
  - Bash(git status:*)
  - Bash(git commit:*)
  - Bash(git push:*)
  - Bash(git log:*)
  - Bash(git diff:*)
  - Bash(git branch:*)
```

限制目的：防止 Agent 在提交流程之外执行非预期的 shell 操作。

---

## 约束

- 不在 `/commit-push` 执行期间修改任何文件
- 推送失败时输出错误信息，不重试
- 不支持多分支、cherry-pick、rebase 等复杂操作，只做直线推送
