# Harness 开发环境

本文档描述如何在 harness 仓库中进行开发和贡献。

---

## 仓库性质

harness 是**内容优先仓库**，以 Markdown 文件为主，无构建步骤、无测试运行器、无依赖安装。

---

## 工作方式

所有变更均为 Markdown 文件的创建或编辑，可直接用文本编辑器完成：

```bash
# 查看当前变更
git status
git diff

# 预览文件结构
ls install/
ls .claude/commands/
ls .claude/skills/agent-team/
ls .harness/
```

---

## 持续治理

修改完成后，在 Claude Code 中运行 `/govern` 命令进行治理扫描：

```
/govern
```

`/govern` 会扫描并逐项协商：
- 术语一致性（E-K-C-F 框架名称、中文维度名、人类掌舵表述）
- 结构完整性（phase 文件、命令闭环、知识目录）
- 原则遵守（无外部 URL、无内部硬链接）
- Agent 友好性（可观测性、可搜索性、约束显式化、反馈闭环）

---

## 提交规范

遵循 Conventional Commits 格式：`feat:` / `fix:` / `docs:` / `refactor:`

```bash
# 一键提交并推送
/commit
/push
```
