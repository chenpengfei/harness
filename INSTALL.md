# Harness 安装指南

> **本文件供 Agent 阅读执行。**
>
> 将本仓库 URL 提供给 Claude Code（或任何支持 WebFetch 的 Agent），告知其"按照该仓库的 INSTALL.md 指引安装 Harness 能力"，Agent 读取本文件后按阶段执行。

Harness 是一个 Agent-First 工程支架，通过 **E-K-C-F** 四个维度提升工程对 Agent 的友好度：

- **E**（Environment / 环境）：让 Agent 能运行、调试、测试、观察系统
- **K**（Knowledge / 知识）：文档和设计决策在仓库内可检索可维护
- **C**（Constraints / 约束）：架构规则约束演化方向
- **F**（Feedback / 回路）：日志、指标、评审直接反馈给 Agent

---

## Phase 0：前置检查

**Agent 执行步骤：**

1. 确认当前工作目录是目标项目的根目录。若不确定，向用户询问：
   > "当前目录是否为你希望安装 Harness 的项目根目录？（当前路径：[显示当前路径]）"

2. 检查 `.claude/harness-config.json` 是否存在：
   - **不存在**：这是首次安装，告知用户："准备在该项目中首次安装 Harness 能力，将涉及 4 个维度（E-K-C-F）的文档和 Claude Code 配置。"
   - **存在**：这是更新流程，告知用户上次安装时间和配置摘要，然后直接执行 Phase 1（走重新评估流程）。

3. 向用户确认：
   > "是否开始安装？（回复'是'继续，或告知需要调整的内容）"

4. 用户确认后，继续 Phase 1。
