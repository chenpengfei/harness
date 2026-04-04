# /audit 命令设计文档

**日期**：2026-03-29  
**状态**：已批准

---

## 概述

`/audit` 命令检查 harness 仓库自身的设计哲学一致性，确保仓库内容不偏离核心原则。命令通过三轮分维度扫描识别问题，暂停询问用户授权后自动修复。

---

## 运行环境

命令仅在 harness 仓库中运行。启动时检查根目录是否存在 `INSTALL.md` + `ARCHITECTURE.md`，若不存在则报错退出并提示用户。

---

## 三轮扫描

### 第一轮：术语一致性

扫描全仓库 Markdown 文件，检查：

- 同一概念是否使用了不同词（如"回路"/"反馈回路"/"Feedback Loop"混用）
- E-K-C-F 四个维度的中英文对应是否一致
- 关键缩写首次出现时是否有展开说明

### 第二轮：结构完整性

- `docs/install/phase-0-preflight.md` 至 `phase-7-agent-team.md` 是否全部存在
- `INSTALL.md` 中引用的所有 phase 文件是否都存在于磁盘
- `docs/design-docs/index.md` 是否存在

### 第三轮：原则遵守

内置原则（6 条）：

1. 仓库不含可执行代码（无 `.js`、`.py`、`.ts` 等代码文件）
2. 安装后无运行时依赖（`INSTALL.md` 和 `.claude/commands/` 下的命令文件不依赖外部 URL 才能执行，`/harness` 命令可离线运行）
3. `INSTALL.md` 是单一真相来源（phase 文件不与 `INSTALL.md` 矛盾）
4. 文档使用符号名称而非硬链接（无 `[text](../other.md)` 形式的内部跨文件链接）
5. 关键节点必须有人类审批（`do.md` 流程中审批检查点完整存在）
6. 设计变更须有对应 `docs/design-docs/` 记录

---

## 报告格式

```
## 哲学一致性审查报告

### 第一轮：术语一致性  [N 个问题]
- [文件名:行号] 问题描述 → 建议修改为 X

### 第二轮：结构完整性  [N 个问题]
- [缺失] docs/install/phase-6-finalize.md 未找到
- [字段缺失] harness-config.json 缺少 teamSize 字段

### 第三轮：原则遵守  [N 个问题]
- [违反原则 3] docs/install/phase-2.md 引用了外部 URL

---
共发现 X 个问题
```

无问题时输出：`✓ 未发现哲学一致性问题，当前工程状态健康。`

---

## 修复授权流程

三轮扫描完成、报告输出后，使用 `AskUserQuestion` 暂停，提供以下选项：

- 全部修复
- 选择轮次修复（仅第一轮 / 仅第二轮 / 仅第三轮）
- 仅查看报告，不修复

修复完成后输出变更摘要（修改了哪些文件、哪些行）。

---

## 文件

命令文件：`.claude/commands/audit.md`  
allowed-tools：`Read, Glob, Grep, AskUserQuestion, Edit`

---

## 约束

- 命令只修改文档内容，不创建新文件、不删除文件
- 无法自动判断的问题（如"内容是否为实质性内容"）标记为 `[需人工确认]`，不纳入自动修复范围
- 修复前必须获得用户授权，不可自动静默修改
- `INSTALL.md` 中若发现与 phase 文件的矛盾，以 `INSTALL.md` 为准，建议修改 phase 文件
