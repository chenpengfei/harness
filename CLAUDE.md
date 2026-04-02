# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 仓库性质

Harness 是一个**内容优先仓库**，以 Markdown 文件为主，辅以必要的工具脚本（如 `.claude/hooks/`）。Agent 通过读取文件来使用内容。无构建、无测试命令、无依赖安装。

## 核心文件

- **INSTALL.md** — 系统入口，Agent 安装剧本（单一真相来源）
- **ARCHITECTURE.md** — 设计不变式与 Codemap
- **README.md** — 项目介绍与安装入口（面向用户）
- **docs/install/** — INSTALL.md 各阶段详细剧本（phase-0 至 phase-7）

## 可用命令

在 Claude Code 中可直接运行的斜杠命令（定义于 `.claude/commands/`）：

| 命令 | 用途 |
|------|------|
| `/do` | 启动 Agent Team 协调器，分析任务并调度专业 agents |
| `/govern` | 持续治理——扫描仓库健康状态，逐项协商处理发现的问题 |
| `/commit` | 按 Conventional Commits 规范创建语义化 git 提交 |
| `/push` | 将当前分支推送到 origin |
| `/harness` | 重新评估并更新已安装的 Harness 配置 |

## 架构不变式

改动任何文档前须遵守：

1. **INSTALL.md 是权威**：`docs/install/` 阶段文件若与 INSTALL.md 矛盾，以 INSTALL.md 为准
2. **不使用硬链接**：文档中用符号名称（文件名、模块名）引用，避免链接失效
3. **哲学自洽**：运行 `/govern` 验证修改不引入概念矛盾

## 文件存放约定

新建文件时遵守以下路径规则：

| 文件类型 | 存放路径 | 命名格式 |
|---------|---------|---------|
| 设计文档（specs/design） | `docs/design-docs/` | `YYYY-MM-DD-<name>-design.md` |
| 执行计划（plans） | `docs/exec-plans/active/`（进行中）或 `completed/`（已完成） | `YYYY-MM-DD-<name>.md` |

## 文档结构

```
.harness/
├── constraints/     # 架构规则、编码规范（C 维度）
├── environment/     # 环境搭建文档（E 维度）
├── feedback/        # 评审清单、复盘模板（F 维度）
└── knowledge/       # 设计哲学、架构决策（K 维度）

docs/
├── install/         # 8 个安装阶段剧本（phase-0 至 phase-7）
├── design-docs/     # 设计决策文档（文件名以 YYYY-MM-DD- 开头）
├── exec-plans/      # 执行计划（active/ 和 completed/ 子目录）
└── references/      # 参考文献与理论基础
```

## E-K-C-F 框架

贯穿所有安装阶段的核心概念：
- **E（Environment）**：Agent 能运行、调试、观察系统
- **K（Knowledge）**：文档和设计决策在仓库内可检索
- **C（Constraints）**：规则约束架构演化方向
- **F（Feedback）**：日志、评审、失败直接反馈给 Agent
