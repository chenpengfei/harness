# Harness 安装系统设计文档

**日期**：2026-03-29
**状态**：已批准

---

## 概述

Harness 是一个 Agent-First 工程支架脚手架。用户将本仓库的 GitHub 地址提供给 Agent，Agent 通过读取 `INSTALL.md` 并按剧本执行，在目标工程中安装 E-K-C-F（环境、知识、约束、反馈）四个维度的工程能力。安装完成后，目标工程中会生成 `/harness` 命令，用户随时可运行该命令对 Harness 能力进行重新评估和更新。

---

## 整体架构

### harness 仓库职责

纯内容仓库，不含可执行代码。Agent 通过 WebFetch/Read 读取 `INSTALL.md`，该文件是完整的安装剧本，内嵌所有文件模板内容。安装完成后，harness 仓库与目标项目之间安装后无依赖。

### harness 仓库结构

```
harness/
├── README.md        # 项目介绍与 E-K-C-F 概念说明
├── INSTALL.md       # Agent 安装剧本（核心文件）
└── docs/            # 模板内容库（由 INSTALL.md 引用）
    └── design-docs/ # 设计文档
```

### 目标工程安装后结构

```
目标项目/
├── CLAUDE.md                          # K 维度：Agent 核心指令文件
├── docs/
│   ├── environment/                   # E 维度：环境文档
│   │   ├── README.md                  # 启动、运行、调试说明
│   │   └── setup.md                   # 本地环境搭建步骤
│   ├── knowledge/                     # K 维度：架构知识
│   │   ├── architecture.md            # 系统架构概述
│   │   └── decisions/
│   │       └── README.md              # ADR 索引
│   ├── constraints/                   # C 维度：架构约束
│   │   ├── README.md                  # 约束总览（模块边界、依赖方向）
│   │   └── coding-rules.md            # 编码规范和禁止模式
│   └── feedback/                      # F 维度：反馈机制
│       ├── review-checklist.md        # Code review 检查清单
│       └── retro-template.md          # 复盘模板
├── .harness/
│   └── harness-config.json            # Harness 配置（4 个问题的答案）
└── .claude/
    ├── commands/
    │   ├── harness.md                 # /harness 更新命令
    │   └── harness-feedback.md        # /harness-feedback 改进反馈命令
    └── skills/
        ├── harness-env.md             # skill：辅助维护环境文档
        ├── harness-knowledge.md       # skill：辅助维护知识文档
        └── harness-feedback.md        # skill：辅助记录问题和改进点
```

---

## INSTALL.md 安装剧本结构

安装分 6 个阶段，每阶段结束有明确确认点。Agent 展示"已创建的文件清单"后询问用户是否继续，用户可选择继续、跳过或修改。

### 阶段 0 — 前置检查
- 确认目标工作目录
- 检测 `.harness/harness-config.json` 是否存在，判断首次安装或更新
- 告知用户即将执行的操作，获得开始许可

### 阶段 1 — 信息收集
向用户逐一询问 4 个问题：
1. **项目名称**：项目名称和一句话描述
2. **技术栈**：主要编程语言和框架
3. **团队规模**：solo / 小团队（2-5人）/ 大团队（6人+）
4. **项目阶段**：早期探索 / 产品迭代 / 生产运营

收集完成后，将答案写入 `.harness/harness-config.json`。

### 阶段 2 — E（环境）
创建 `docs/environment/README.md` 和 `docs/environment/setup.md`，根据技术栈定制内容。
创建 `.claude/skills/harness-env.md`。
完成后展示文件清单，确认后继续。

### 阶段 3 — K（知识）
创建/更新 `CLAUDE.md`（若已存在则追加 Harness 相关部分）。
创建 `docs/knowledge/architecture.md` 和 `docs/knowledge/decisions/README.md`。
创建 `.claude/skills/harness-knowledge.md`。
完成后展示文件清单，确认后继续。

### 阶段 4 — C（约束）
创建 `docs/constraints/README.md` 和 `docs/constraints/coding-rules.md`，根据项目阶段调整严格程度（早期探索宽松，生产运营严格）。
完成后展示文件清单，确认后继续。

### 阶段 5 — F（反馈）
创建 `docs/feedback/review-checklist.md` 和 `docs/feedback/retro-template.md`，根据团队规模调整内容深度（solo 简化，大团队完整）。
创建 `.claude/skills/harness-feedback.md`。
完成后展示文件清单，确认后继续。

### 阶段 6 — 收尾
生成 `.claude/commands/harness.md`（`/harness` 命令的完整剧本）。
打印安装摘要（共创建 N 个文件，涵盖 E-K-C-F 四个维度）。
告知用户如何使用：`在 Claude Code 中运行 /harness 可随时更新 Harness 能力`。

---

## 内容定制规则

各维度文件内容根据阶段 1 的 4 个问题动态调整：

| 问题 | 影响维度 | 示例 |
|------|---------|------|
| 技术栈 | E、K | `docs/environment/README.md` 中的命令对应具体语言 |
| 团队规模 | K、F | solo 项目的 CLAUDE.md 简洁；大团队包含协作约定 |
| 项目阶段 | C、F | 早期探索的约束宽松；生产运营包含完整 review checklist |
| 项目名称 | 全部 | 所有文件标题和 CLAUDE.md 中的项目描述 |

---

## `/harness` 命令更新流程

`/harness` 命令内嵌完整更新剧本，安装后离线可用，不依赖外部网络请求。

### 步骤 1 — 读取现状
读取 `.harness/harness-config.json`，加载上次安装时记录的 4 个答案。

### 步骤 2 — 重新评估
重新向用户逐一询问同样的 4 个问题，展示上次的答案，用户可回车确认或输入新值。

### 步骤 3 — 差异分析
对比新旧答案，找出变化项，确定需要更新的维度。示例：
- 团队规模 solo → 小团队：加强 K 维度协作文档、加深 F 维度 review checklist
- 项目阶段 早期探索 → 生产运营：加强 C 和 F 维度

### 步骤 4 — 呈现变更计划
向用户展示建议更新的文件清单及变更理由，获得确认后再执行。若无变化，告知"当前配置已是最新，无需更新"。

### 步骤 5 — 执行更新
按确认范围更新文件，更新 `.harness/harness-config.json`，打印变更摘要。

---

## 数据结构

### `.harness/harness-config.json`

```json
{
  "version": "1.0",
  "installedAt": "2026-03-29T00:00:00Z",
  "updatedAt": "2026-03-29T00:00:00Z",
  "project": {
    "name": "项目名称",
    "description": "一句话描述"
  },
  "techStack": "例如：TypeScript / Next.js / PostgreSQL",
  "teamSize": "solo | small | large",
  "projectStage": "exploration | iteration | production",
  "harnessRepo": "git@github.com:chenpengfei/harness.git"
}
```

---

## 边界与约束

- harness 安装只创建/修改文档和 `.claude/` 内的文件，不触碰项目的 lint、CI、测试配置
- 若 `CLAUDE.md` 已存在，追加而非覆盖，追加内容用注释标识来源（`<!-- harness -->`）
- 所有生成内容为模板起点，用户和 Agent 后续可自由编辑
- `/harness` 命令更新时不删除用户已自定义的内容，只追加或提示用户手动处理冲突
