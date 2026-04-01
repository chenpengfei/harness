---
allowed-tools: Bash(git push:*), Bash(git branch:*), Bash(git remote:*)
description: 将当前分支推送到 origin
---

## 上下文

- 当前分支：!`git branch --show-current`
- 远端状态：!`git remote -v`

## 你的任务

将当前分支推送到 origin：

1. 检查当前分支是否有 upstream tracking 分支
2. 若有：执行 `git push`
3. 若无：执行 `git push -u origin <branch>`

不要创建分支，不要创建 PR，不要做其他任何事情。
