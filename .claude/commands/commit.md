---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*), Bash(git diff:*), Bash(git log:*)
description: 按 Conventional Commits 规范创建语义化 git 提交
---

## 上下文

- 当前状态：!`git status`
- 当前变更：!`git diff HEAD`
- 最近提交：!`git log --oneline -10`

## 你的任务

基于以上变更，执行语义化提交。

### 第 1 步：选择 type

| type | 使用场景 |
|------|---------|
| `feat` | 新增功能或特性 |
| `fix` | 修复 bug |
| `docs` | 文档变更（含 README、注释） |
| `style` | 代码格式调整（不影响逻辑） |
| `refactor` | 代码重构（非 feat/fix） |
| `perf` | 性能优化 |
| `test` | 添加或修改测试 |
| `build` | 构建系统或外部依赖变更 |
| `ci` | CI 配置变更 |
| `chore` | 其他维护性工作 |
| `revert` | 回滚提交 |

### 第 2 步：构造提交消息

格式：`<type>[scope][!]: <中文描述>`

- scope 可选，描述影响范围（如模块名、文件名）
- `!` 表示破坏性变更（BREAKING CHANGE）
- 描述使用**中文**，祈使句

示例：
```
feat(auth): 新增 OAuth2 登录支持
fix(ui): 修复按钮点击后状态未更新的问题
docs: 更新 README 安装步骤
refactor(api): 重构用户服务以提升可维护性
chore: 升级依赖版本
```

### 第 3 步：暂存并提交

在单次响应中依次执行，不发送任何文字消息：

1. `git add` 暂存相关文件
2. `git commit -m "<构造好的消息>"`

不要创建分支，不要推送，不要做其他任何事情。
