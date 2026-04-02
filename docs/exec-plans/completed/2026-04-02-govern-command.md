# /govern 命令实现计划

**Goal:** 将 harness 仓库的 `/audit` 命令升级为 `/govern`，增加逐项协商机制（AskUserQuestion 暂停、可自动修复路径、协商完成摘要），并同步更新 `CLAUDE.md`、`INSTALL.md`、`.harness/` 文档及 `docs/design-docs/index.md`。

**Architecture:** 单文件 Markdown 命令，无可执行代码。命令文件分六个逻辑区块：环境检查、三轮扫描（术语/结构/原则）、简报输出、逐项协商、协商完成摘要。从 `/audit` 的"一次性扫描+批量报告"模式演进为"扫描+逐项交互协商"模式，体现人类掌舵原则。

**Tech Stack:** Claude Code command（Markdown），工具：Read, Glob, Grep, AskUserQuestion, Edit, Bash(git log:*)

---

## 文件清单

| 操作 | 路径 | 说明 |
|------|------|------|
| 创建 | `.claude/commands/govern.md` | /govern 命令完整脚本 |
| 删除 | `.claude/commands/audit.md` | 由 govern 替代 |
| 修改 | `CLAUDE.md` | 命令表更新：/audit → /govern |
| 修改 | `.harness/environment/README.md` | 更新 govern 相关描述 |
| 修改 | `.harness/constraints/README.md` | 删除"命令不依赖外部 URL"约束，重新编号 |
| 修改 | `docs/design-docs/index.md` | 补录设计文档和 govern 执行计划 |

---

## 完成状态

所有任务已完成。以下记录实际执行过程中的关键决策：

### Task 1：从 /audit 演进到 /govern

**已完成**。核心变化：
- `/audit` 采用"扫描 → 输出完整报告 → 一次性列出所有发现"模式
- `/govern` 采用"静默扫描 → 简报数字 → 逐项协商"模式
- 新增 `AskUserQuestion` 暂停机制，可自动修复/不可自动修复分两路选项
- 新增"协商完成摘要"（已修复/已处理/跳过/标记偏差 计数）
- 原则 1（命令不依赖外部 URL）在设计审查中删除（见设计文档决策 3）

### Task 2：删除 /audit，更新命令表

**已完成**。
- 删除 `.claude/commands/audit.md`（git status 中显示为 `D .claude/commands/audit.md`）
- `CLAUDE.md` 命令表已更新为 `/govern`

### Task 3：更新 .harness/constraints/README.md

**已完成**（本次 /govern 运行中执行）。
- 删除"约束 1：命令文件不依赖外部 URL"
- 重新编号：旧约束 2→1、3→2、4→3
- 验证指令由 `/audit` 改为 `/govern`

### Task 4：同步设计文档索引

**已完成**（本次 /govern 运行中执行）。
- 补录 `2026-04-01-semantic-commit-commands-design.md`
- 补录 `2026-04-02-govern-command-design.md`

---

## 验证（已通过）

```
Glob(".claude/commands/govern.md")    → 存在 ✓
Glob(".claude/commands/audit.md")     → 不存在（已删除）✓
Grep("govern", "CLAUDE.md")           → 命令表中存在 /govern ✓
Grep("audit", "CLAUDE.md")            → 不存在 ✓
Glob("docs/design-docs/*govern*")     → 2026-04-02-govern-command-design.md ✓
Glob("docs/exec-plans/completed/*govern*") → 本文件 ✓
```
