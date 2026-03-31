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
| **F** — 回路 | Feedback | 日志、指标、评审直接反馈给 Agent |

---

## 仓库架构

```
harness/
├── README.md              # 项目介绍（面向人类）
├── INSTALL.md             # Agent 安装剧本（核心文件，面向 Agent）
├── ARCHITECTURE.md        # 本仓库架构决策（面向维护者）
├── .claude/
│   ├── commands/          # harness 自用的 Claude Code 命令
│   │   ├── audit.md       # /audit — 哲学一致性审查
│   │   ├── commit-push.md # /commit-push — 提交并推送
│   │   ├── do.md          # /do — Agent Team 协调器
│   │   └── harness-feedback.md # /harness-feedback — 改进反馈
│   └── skills/agent-team/ # /do 命令使用的 Agent 专业技能
└── docs/
    ├── install/           # 8 个安装阶段的详细指引（Phase 0-7）
    ├── design-docs/       # 设计决策文档（含 index.md）
    ├── exec-plans/        # 执行计划（active/ 和 completed/）
    ├── references/        # 外部参考资料
    ├── environment/       # 本文档所在目录（E 维度）
    ├── knowledge/         # 架构知识（K 维度，本目录）
    ├── constraints/       # 开发约束（C 维度）
    └── feedback/          # 反馈机制（F 维度）
```

---

## 关键设计决策

所有设计决策记录于 `docs/design-docs/`，参见 [index.md](../design-docs/index.md)。

主要决策：
- harness 为**纯内容仓库**，绝不含可执行代码
- **INSTALL.md 是单一真相来源**，所有安装逻辑在此集中
- **安装后无依赖**：安装完成后目标项目不依赖 harness 仓库
- 命令文件不依赖外部 URL，确保离线可用

---

## 安装流程概览

INSTALL.md 将安装分为 8 个阶段（Phase 0–7），每阶段对应 `docs/install/` 下的详细指引文件。详见 INSTALL.md 的安装流程地图表格。
