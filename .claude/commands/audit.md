---
allowed-tools: Read, Glob, Grep, AskUserQuestion, Edit, Bash(git log:*)
description: 检查 harness 仓库设计哲学、思想的一致性
---

## 环境检查

用 Glob 检查根目录是否同时存在 `INSTALL.md` 和 `ARCHITECTURE.md`。

若两者不同时存在，停止执行并输出以下错误：

    错误：当前目录不是 harness 仓库。
    /audit 命令仅适用于 harness 仓库本身，请在 harness 仓库根目录下运行。
