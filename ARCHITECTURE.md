# Architecture

> 参考：matklad，[ARCHITECTURE.md](https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html)，2021

---

## 问题概述

Harness 是一个 Agent-First 工程脚手架，用来把「E-K-C-F」（环境、知识、约束、反馈）四类工程能力安装到任意代码仓库。

---

## Codemap

Harness 仓库本身是一个**内容优先仓库**，以 Markdown 文件为主，辅以必要的工具脚本（如 git hooks）。

```
harness/
├── README.md       # 项目介绍 + 安装入口
├── INSTALL.md      # Agent 安装剧本（核心文件）
├── ARCHITECTURE.md # 本文件
├── .claude/        # Claude Code 工具配置
│   ├── commands/       # 斜杠命令定义（/do /commit /push /govern /harness）
│   ├── skills/         # Agent Team 技能库（orchestrator、feature-developer 等）
│   ├── hooks/          # PreToolUse 钩子脚本
│   └── settings.json   # hook 注册配置
├── .harness/       # E-K-C-F 四维度文档（同时作为目标项目安装模板）
│   ├── constraints/    # C 维度：开发约束
│   ├── environment/    # E 维度：环境说明
│   ├── feedback/       # F 维度：反馈机制
│   └── knowledge/      # K 维度：架构知识
└── docs/
    ├── design-docs/    # 设计文档
    ├── exec-plans/     # 执行计划
    ├── references/     # 参考文献
    └── install/        # INSTALL.md 各阶段详细剧本
```

**INSTALL.md** 是整个系统的入口点，也是最重要的文件。Agent 读取它、按剧本在目标项目中安装能力。安装完成后 harness 仓库与目标项目之间安装后无依赖。

**`docs/install/`** 把 INSTALL.md 的每个安装阶段拆分为独立文件（`phase-0-preflight.md` 至 `phase-7-agent-team.md`），供 INSTALL.md 引用或 Agent 按需读取。

**`.harness/`** 存放 harness 仓库自身的 E-K-C-F 四维度文档，同时作为目标项目安装时的内容模板。安装过程（Phase 1）通过 git sparse-checkout 将此目录拉取到目标项目，后续各阶段在此基础上定制内容。

**`docs/design-docs/`** 存放影响仓库结构或安装行为的设计决策文档，文件名以日期开头（`YYYY-MM-DD-*.md`）。

**`docs/exec-plans/`** 存放执行计划，分 `active/` 和 `completed/` 两个子目录。

---

## 架构不变式

- **INSTALL.md 是单一真相来源**。`docs/install/` 下的阶段文件服务于 INSTALL.md，INSTALL.md 是安装行为的权威定义。两者出现矛盾时，以 INSTALL.md 为准。

- **内容不链接代码**。文档中使用符号名称（文件名、模块名）而非硬链接，避免链接失效。

- **`.harness/` 纳入目标项目版本控制**。安装流程不得将 `.harness/` 加入目标项目的 `.gitignore`；E-K-C-F 文档是目标项目代码库的一部分，不是临时文件。

---

## 横切关注点

**E-K-C-F 框架**贯穿所有安装阶段和文档内容：
- E（环境）：让 Agent 能运行、调试、观察系统
- K（知识）：文档和设计决策在仓库内可检索
- C（约束）：规则和边界约束架构演化
- F（反馈）：日志、评审、失败直接反馈给 Agent

**内容定制**：安装阶段收集的四个答案（项目名称、技术栈、团队规模、项目阶段）决定所有生成内容的深度和风格。这四个维度是贯穿整个安装流程的全局上下文。
