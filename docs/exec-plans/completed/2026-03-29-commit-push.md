# /commit-push 命令实现记录

**日期**：2026-03-29
**状态**：已完成

---

## 目标

创建 `.claude/commands/commit-push.md`，提供一键提交并推送的 Agent 命令。

---

## 变更清单

| 操作 | 文件 | 说明 |
|------|------|------|
| Create | `.claude/commands/commit-push.md` | `/commit-push` 命令完整脚本 |

---

## 实现内容

命令文件包含：
- `allowed-tools` frontmatter 限制为 git 相关操作
- `## Context` 注入 git status / diff / branch / log
- `## Your task` 两步操作：生成提交信息 → 暂存提交推送

---

## 验证

命令文件已存在于 `.claude/commands/commit-push.md`，内容符合设计文档规范。
