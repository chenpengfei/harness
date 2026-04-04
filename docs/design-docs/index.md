# 设计文档索引

本目录存放 harness 仓库自身的设计决策文档，按时间倒序排列。

| 文件 | 日期 | 状态 | 描述 |
|------|------|------|------|
| [2026-04-02-raw-base-url-design.md](2026-04-02-raw-base-url-design.md) | 2026-04-02 | 已采纳 | 支持可配置 rawBaseUrl：以 jsDelivr CDN 加速 harness 文件下载，解决中国大陆访问慢问题 |
| [2026-04-02-govern-command-design.md](2026-04-02-govern-command-design.md) | 2026-04-02 | 已批准 | `/govern` 命令重新设计：四轮扫描对应 Agent 友好性四原则，适用于 harness 仓库和所有目标工程 |
| [2026-04-02-move-install-to-root-design.md](2026-04-02-move-install-to-root-design.md) | 2026-04-02 | 已实施 | 将 `install/` 目录从 `docs/install/` 移至项目根目录 |
| [2026-04-01-semantic-commit-commands-design.md](2026-04-01-semantic-commit-commands-design.md) | 2026-04-01 | 已批准 | `/commit` 与 `/push` 命令及 Semantic Commit Messages 支持设计 |
| [2026-03-30-harness-feedback-command-design.md](2026-03-30-harness-feedback-command-design.md) | 2026-03-30 | 已批准 | `/harness-feedback` 命令设计：本地记录改进建议并可选提交到 harness 仓库 |
| [2026-03-29-do-command-design.md](2026-03-29-do-command-design.md) | 2026-03-29 | 已批准 | `/do` 命令与 Agent Team 设计：多 Agent 协作流水线，含三个人类审批检查点 |
| [2026-03-29-audit-command-design.md](2026-03-29-audit-command-design.md) | 2026-03-29 | 已归档 | `/audit` 命令设计（已被 `/govern` 取代）：一致性检查，仅负责术语、结构与原则遵守的静态审查 |
| [2026-03-29-commit-push-design.md](2026-03-29-commit-push-design.md) | 2026-03-29 | 已批准 | `/commit-push` 命令设计：自动提交并推送到远端 |
| [2026-03-29-harness-design.md](2026-03-29-harness-design.md) | 2026-03-29 | 已批准 | Harness 安装系统整体设计：E-K-C-F 四维度、阶段式安装、安装后无运行时依赖 |
