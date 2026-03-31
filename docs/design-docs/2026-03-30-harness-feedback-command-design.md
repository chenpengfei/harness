# /harness-feedback 命令设计文档

**日期**：2026-03-30
**状态**：已批准

---

## 概述

在目标工程实践过程中，用户会不断发现对 harness 本身的改进点（无论是模板内容还是工程理念）。本设计新增独立命令 `/harness-feedback`，为用户提供"本地记录 → 可选提交"的分层反馈机制，使改进得以回流到 harness 仓库。

---

## 整体架构

新增一个独立命令 `/harness-feedback`，安装到目标项目的 `.claude/commands/harness-feedback.md`，与现有 `/harness` 命令完全独立、互不干扰。

### 两层处理

| 层级 | 操作 | 产物 |
|------|------|------|
| 第一层：记录 | 用户描述改进 | `.harness/proposals/YYYY-MM-DD-<slug>.md` |
| 第二层：提交 | 通过 `gh` CLI 提交 | GitHub Issue（草稿移入 `.harness/submitted/`） |

### `.harness/` 目录结构

```
.harness/
├── harness-config.json   # Harness 配置（提交至 git）
├── proposals/            # 改进草稿（gitignored）
│   └── YYYY-MM-DD-*.md
└── submitted/            # 已提交存档（gitignored）
    └── YYYY-MM-DD-*.md
```

`.gitignore` 中精确排除子目录，`harness-config.json` 正常提交：

```
.harness/proposals/
.harness/submitted/
```

---

## `/harness-feedback` 命令流程

命令启动后，展示模式选择：

```
请选择操作：
1. 记录一条改进建议
2. 查看并提交已记录的建议
```

### 模式 1 — 记录改进建议

1. 询问改进类型：`模板/脚本`（影响 harness 生成的内容）或 `理念/架构`（影响 harness 的设计思路）
2. 询问一句话标题
3. 询问具体描述（背景、当前问题、建议改法）
4. 写入 `.harness/proposals/YYYY-MM-DD-<slug>.md`，打印确认

### 模式 2 — 查看并提交

1. 列出 `.harness/proposals/` 下所有草稿，展示标题
2. 用户选择一条或多条
3. 询问是否通过 `gh issue create` 提交到 harness 仓库
   - 读取 `.harness/harness-config.json` 中的 `harnessRepo` 字段
   - 若字段缺失，向用户询问并写入配置
4. 提交成功后将草稿移入 `.harness/submitted/`

---

## 数据结构

### `.harness/harness-config.json`

```json
{
  "version": "1.0",
  "installedAt": "2026-03-30T00:00:00Z",
  "updatedAt": "2026-03-30T00:00:00Z",
  "harnessRepo": "git@github.com:chenpengfei/harness.git",
  "project": {
    "name": "项目名称",
    "description": "一句话描述"
  },
  "techStack": "例如：TypeScript / Next.js / PostgreSQL",
  "teamSize": "solo | small | large",
  "projectStage": "exploration | iteration | production"
}
```

**注**：`harness-config.json` 位置从旧版 `.claude/harness-config.json` 迁移至 `.harness/harness-config.json`。

### 改进建议文档格式

路径：`.harness/proposals/YYYY-MM-DD-<slug>.md`

```markdown
---
date: 2026-03-30
type: template | philosophy
title: 一句话标题
status: draft
---

## 背景

（当前遇到的问题或场景）

## 建议改法

（具体建议）
```

---

## 安装变更

### Phase 1 — 信息收集（新增问题）

在现有 4 个问题后新增第 5 题：

> **问题 5：Harness 仓库地址**
> 请提供 harness 仓库的 Git 地址（用于后续提交改进建议）。
> 例如：`git@github.com:chenpengfei/harness.git`

答案写入 `harness-config.json` 的 `harnessRepo` 字段。

### Phase 6 — 收尾（变更）

1. 创建 `.harness/` 目录
2. 将 `harness-config.json` 写入 `.harness/harness-config.json`（不再写 `.claude/harness-config.json`）
3. 在 `.gitignore` 中追加：
   ```
   .harness/proposals/
   .harness/submitted/
   ```
4. 新增：创建 `.claude/commands/harness-feedback.md`（`/harness-feedback` 命令完整脚本）
5. 安装摘要更新：列出 `.harness/harness-config.json` 和 `.claude/commands/harness-feedback.md`

### harness 仓库需要更新的文件

| 文件 | 变更内容 |
|------|---------|
| `docs/install/phase-1-info-collection.md` | 增加第 5 题（harnessRepo） |
| `docs/install/phase-6-finalize.md` | 更新 `harness.md` 模板读取路径；增加 `harness-feedback.md` 创建步骤；更新 `.gitignore` 追加逻辑 |
| `INSTALL.md` | 安装后文件结构图更新（`.harness/` 替代 `.claude/harness-config.json`） |
| `docs/design-docs/2026-03-29-harness-design.md` | 同步更新数据结构章节 |

---

## 边界与约束

- `/harness-feedback` 只操作 `.harness/` 目录，不修改目标项目的任何其他文件
- 提交到 GitHub 需要本地已安装并登录 `gh` CLI；若未安装，提示用户手动创建 Issue 并提供草稿内容
- 改进建议属于对 harness 仓库的贡献，不属于目标项目代码，故草稿目录 gitignored
- `harnessRepo` 字段缺失时，命令在模式 2 执行时补问，不阻断模式 1 的记录功能
