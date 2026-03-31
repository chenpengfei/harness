# Harness 开发环境

本文档描述如何在 harness 仓库中进行开发和贡献。

---

## 仓库性质

harness 是**纯内容仓库**，不含可执行代码，无构建步骤、无测试运行器、无依赖安装。

---

## 工作方式

所有变更均为 Markdown 文件的创建或编辑，可直接用文本编辑器完成：

```bash
# 查看当前变更
git status
git diff

# 预览文件结构
ls docs/install/
ls .claude/commands/
ls .claude/skills/agent-team/
```

---

## 一致性验证

修改完成后，在 Claude Code 中运行 `/audit` 命令验证哲学一致性：

```
/audit
```

`/audit` 会检查：
- 术语一致性（E-K-C-F 框架名称、中文维度名、人类掌舵表述）
- 结构完整性（phase 文件、命令闭环、知识目录）
- 原则遵守（无可执行代码、无外部 URL、无内部硬链接）

---

## 提交规范

遵循 Conventional Commits 格式：`feat:` / `fix:` / `docs:` / `refactor:`

```bash
# 一键提交并推送
/commit-push
```

---

## 贡献 harness 本身的改进

在**目标项目**中运行 `/harness-feedback` 记录对 harness 的改进建议，可选通过 `gh` CLI 提交为 GitHub Issue。
