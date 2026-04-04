# Harness 安装指南

> **本文件供 Agent 阅读执行。**
>
> 将本仓库 URL 提供给 Claude Code（或任何支持 WebFetch 的 Agent），告知其"按照该仓库的 INSTALL.md 指引安装 Harness 能力"，Agent 读取本文件后按阶段执行。

Harness 是一个 Agent-First 工程支架，通过 **E-K-C-F** 四个维度提升工程对 Agent 的友好度：

- **E**（Environment / 环境）：让 Agent 能运行、调试、测试、观察系统
- **K**（Knowledge / 知识）：文档和设计决策在仓库内可检索可维护
- **C**（Constraints / 约束）：架构规则约束演化方向
- **F**（Feedback / 反馈）：日志、指标、评审直接反馈给 Agent

---

## 安装流程地图

按顺序执行以下各 Phase，每个 Phase 完成后向用户确认再继续。

| Phase | 内容 | 详细指引 |
|-------|------|---------|
| Phase 0 | 前置检查：确认目录、检查已有配置 | `install/phase-0-preflight.md` |
| Phase 1 | 信息收集：项目名、技术栈、团队规模、项目阶段 | `install/phase-1-info-collection.md` |
| Phase 2 | E — 环境：创建 `.harness/environment/` 文档和 harness-env skill | `install/phase-2-environment.md` |
| Phase 3 | K — 知识：创建/更新 CLAUDE.md、架构文档、ADR 目录 | `install/phase-3-knowledge.md` |
| Phase 4 | C — 约束：创建架构约束和编码规范文档 | `install/phase-4-constraints.md` |
| Phase 5 | F — 反馈：创建 Review 清单和复盘模板 | `install/phase-5-feedback.md` |
| Phase 6 | 收尾：创建 `/harness` 更新命令，打印安装摘要 | `install/phase-6-finalize.md` |
| Phase 7 | Agent Team（可选）：安装 `/do` 多 Agent 协作流水线 | `install/phase-7-agent-team.md` |

---

## 安装后的文件结构

```
目标项目/
├── CLAUDE.md                          # 文档地图（保持 200 行以内）
├── .harness/
│   ├── harness-config.json            # Harness 配置（版本、技术栈、阶段等）
│   ├── environment/
│   │   ├── README.md                  # 运行、测试、调试命令
│   │   └── setup.md                   # 本地环境搭建
│   ├── knowledge/
│   │   ├── architecture.md            # 系统架构
│   │   └── decisions/                 # ADR 架构决策记录
│   ├── constraints/
│   │   ├── README.md                  # 模块边界、禁止模式
│   │   └── coding-rules.md            # 编码规范
│   └── feedback/
│       ├── review-checklist.md        # Review / 自检清单
│       └── retro-template.md          # 复盘模板
└── .claude/
    ├── commands/
    │   ├── commit.md                  # /commit 命令
    │   ├── push.md                    # /push 命令
    │   ├── harness.md                 # /harness 更新命令
    │   ├── govern.md                  # /govern 治理命令
    │   └── do.md                      # /do 命令（Phase 7 可选）
    ├── hooks/
    │   └── validate-commit-msg.py     # Semantic Commit 格式验证 hook
    ├── settings.json                  # Claude Code hook 注册配置
    └── skills/
        ├── harness-env.md
        ├── harness-knowledge.md
        └── agent-team/                # Phase 7 可选
            └── *.md
```

---

## 更新已安装的 Harness

安装完成后，通过 `/harness` 命令重新评估并更新配置。更新逻辑详见 `install/phase-6-finalize.md` 中的步骤 6.2。

---

## 参考文献

参见 `docs/references/README.md`。
