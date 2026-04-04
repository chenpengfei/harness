# Harness 架构知识

本文档是 harness 仓库的架构概述，为维护者和贡献者提供全局视图。

---

## 核心概念

**harness** 是一个 Agent-First 工程支架，通过 **E-K-C-F** 四个维度提升工程对 Agent 的友好度：

| 维度 | 含义 | 作用 |
|------|------|------|
| **E** — 环境 | Environment | Agent 可运行、调试、测试、观察系统 |
| **K** — 知识 | Knowledge | 文档和设计决策在仓库内可检索可维护 |
| **C** — 约束 | Constraints | 架构规则约束演化方向 |
| **F** — 反馈 | Feedback | 日志、指标、评审直接反馈给 Agent |

---

## 仓库架构

```
harness/
├── README.md              # 项目介绍（面向人类）
├── INSTALL.md             # Agent 安装剧本（核心文件，面向 Agent）
├── ARCHITECTURE.md        # 本仓库架构决策（面向维护者）
├── .harness/              # E-K-C-F 四维度文档（也作为目标项目模板）
│   ├── constraints/       # C 维度：开发约束
│   ├── environment/       # E 维度：环境说明
│   ├── feedback/          # F 维度：反馈机制（本目录）
│   └── knowledge/         # K 维度：架构知识
├── .claude/
│   ├── commands/          # harness 自用的 Claude Code 命令
│   │   ├── commit.md      # /commit — 语义化提交
│   │   ├── do.md          # /do — Agent Team 协调器
│   │   ├── govern.md      # /govern — 持续治理
│   │   ├── harness.md     # /harness — Harness 更新
│   │   └── push.md        # /push — 推送到远程
│   └── skills/agent-team/ # /do 命令使用的 Agent 专业技能
└── docs/
    ├── design-docs/       # 设计决策文档（含 index.md）
    ├── exec-plans/        # 执行计划（active/ 和 completed/）
    └── references/        # 外部参考资料
└── install/               # 8 个安装阶段的详细指引（Phase 0-7）
```

---

## 关键设计决策

所有设计决策记录于 `docs/design-docs/`，参见 `docs/design-docs/index.md`。

主要决策：
- **INSTALL.md 是单一真相来源**，所有安装逻辑在此集中
- **`.harness/` 即安装产物**：安装过程通过拉取 `.harness/` 目录到目标工程实现，目标工程提交 `.harness/` 进入版本控制

---

## 安装流程概览

INSTALL.md 将安装分为 8 个阶段（Phase 0–7），每阶段对应 `install/` 下的详细指引文件。详见 INSTALL.md 的安装流程地图表格。
