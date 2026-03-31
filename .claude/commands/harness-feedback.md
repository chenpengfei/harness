---
allowed-tools: Read, Glob, Write, Edit, Bash(gh:*), Bash(mkdir:*), Bash(mv:*), AskUserQuestion
description: 记录改进建议并可选提交到 harness 仓库
---

## 前置检查

用 Glob 检查 `.harness/harness-config.json` 是否存在。

若不存在，停止执行并输出：
> 错误：未找到 Harness 配置文件（`.harness/harness-config.json`）。
> 请先通过安装流程初始化 Harness。

## 模式选择

使用 AskUserQuestion 询问：
> 请选择操作：
> - **记录改进建议**：将发现的改进点写入本地 `.harness/proposals/`
> - **查看并提交**：列出已记录的建议，可选提交到 harness 仓库

---

## 模式：记录改进建议

### 步骤 1：改进类型

使用 AskUserQuestion：
> 改进类型：
> - **模板/脚本**：harness 生成的模板内容、安装脚本、命令文件
> - **理念/架构**：Agent-First 工程思路、E-K-C-F 框架、设计原则

记录为 `PROPOSAL_TYPE`（`template` 或 `philosophy`）。

### 步骤 2：标题

使用 AskUserQuestion：
> 请用一句话描述这条改进建议（将作为 GitHub Issue 标题）：

记录为 `PROPOSAL_TITLE`。

### 步骤 3：背景

使用 AskUserQuestion：
> 当前遇到了什么问题或场景？为什么需要改进？

记录为 `PROPOSAL_BACKGROUND`。

### 步骤 4：建议改法

使用 AskUserQuestion：
> 具体建议怎么改？（可附上示例内容）

记录为 `PROPOSAL_SUGGESTION`。

### 步骤 5：写入草稿文件

生成 slug：若标题仅含 ASCII 字符，转为小写并将空格和特殊字符替换为连字符；若标题含中文或其他非 ASCII 字符，使用 `proposal` 作为 slug。截取前 40 个字符。

文件名格式：`<今日日期 YYYY-MM-DD>-<slug>.md`

创建目录（若不存在）：
```bash
mkdir -p .harness/proposals
```

创建 `.harness/proposals/<文件名>`，内容：

```markdown
---
date: <今日日期>
type: <PROPOSAL_TYPE>
title: <PROPOSAL_TITLE>
status: draft
---

## 背景

<PROPOSAL_BACKGROUND>

## 建议改法

<PROPOSAL_SUGGESTION>
```

输出确认：
> 已记录：`.harness/proposals/<文件名>`
> 运行 `/harness-feedback` 并选择「查看并提交」，可将此建议提交到 harness 仓库。

---

## 模式：查看并提交

### 步骤 1：列出草稿

用 Glob 列出 `.harness/proposals/` 下所有 `.md` 文件。

若无文件，输出：
> 暂无待提交的改进建议。运行 `/harness-feedback` 并选择「记录改进建议」来添加。

然后停止执行。

读取每个文件的 `title` frontmatter，输出清单：
```
待提交的改进建议：
1. YYYY-MM-DD-xxx.md — <标题>
2. ...
```

### 步骤 2：选择提交项

使用 AskUserQuestion：
> 请输入要提交的建议编号（多个用逗号分隔，如 1,3）：

### 步骤 3：获取 harness 仓库地址

读取 `.harness/harness-config.json`，检查 `harnessRepo` 字段是否存在且非空。

若缺失，使用 AskUserQuestion：
> 请提供 harness 仓库的 Git 地址：
> 例如：`git@github.com:chenpengfei/harness.git`

先用 Read 读取 `.harness/harness-config.json` 的现有内容，将 `harnessRepo` 字段设为用户输入的地址，将 `updatedAt` 更新为当前时间戳，然后用 Write 完整写回（保留文件中其他所有字段不变）。

### 步骤 4：提交方式

使用 AskUserQuestion：
> 是否通过 `gh issue create` 提交到 harness 仓库？
> - **是**（需要本地已安装并登录 `gh` CLI）
> - **否**（我将手动创建 Issue）

### 步骤 5A：通过 gh CLI 提交

从 `harnessRepo` 提取 `owner/repo`：
  - 若格式为 `git@github.com:owner/repo.git`，去掉 `git@github.com:` 前缀和 `.git` 后缀
  - 若格式为 HTTPS 克隆地址（含 `github.com/` 路径），提取 `github.com/` 后的部分并去掉 `.git` 后缀

对每条选中的建议：
1. 用 Read 读取文件完整内容
2. 从 frontmatter 提取 `title` 字段作为 `PROPOSAL_TITLE`
3. 从 `## 背景` 章节下的正文提取 `PROPOSAL_BACKGROUND`
4. 从 `## 建议改法` 章节下的正文提取 `PROPOSAL_SUGGESTION`
5. 执行：

```bash
gh issue create \
  --repo <owner/repo> \
  --title "<PROPOSAL_TITLE>" \
  --body "## 背景\n\n<PROPOSAL_BACKGROUND>\n\n## 建议改法\n\n<PROPOSAL_SUGGESTION>"
```

若执行成功：
1. `mkdir -p .harness/submitted`
2. `mv .harness/proposals/<文件名> .harness/submitted/<文件名>`
3. 输出：`✓ 已提交 Issue：<issue URL>`

若 `gh` 命令失败（未安装或未登录），自动降级到步骤 5B。

### 步骤 5B：手动提交

对每条选中的建议，展示：
> 请前往 harness 仓库（`harnessRepo` 字段对应的 GitHub 仓库）的 Issues 页面，手动创建 Issue：
>
> **标题**：\<PROPOSAL_TITLE\>
>
> **内容**：
> ## 背景
>
> \<PROPOSAL_BACKGROUND\>
>
> ## 建议改法
>
> \<PROPOSAL_SUGGESTION\>

询问用户是否已提交：
> 是否已手动创建 Issue？
> - **是**：将草稿移入 `.harness/submitted/` 存档
> - **否**：保留在 `.harness/proposals/` 中，下次继续

若用户选择"是"：
1. `mkdir -p .harness/submitted`
2. `mv .harness/proposals/<文件名> .harness/submitted/<文件名>`
3. 输出：`✓ 已存档：.harness/submitted/<文件名>`
