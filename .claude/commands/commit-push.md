---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*), Bash(git push:*), Bash(git log:*), Bash(git diff:*), Bash(git branch:*)
description: Create a git commit and push to remote
---

## Context

- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`

## Your task

Based on the above changes:

1. Create a single git commit with an appropriate message (follow the commit message style of recent commits)
2. Push the current branch to origin

You have the capability to call multiple tools in a single response. Stage files and create the commit first, then push to origin. Do not create a new branch. Do not create a pull request. Do not use any other tools or do anything else. Do not send any other text or messages besides these tool calls.
