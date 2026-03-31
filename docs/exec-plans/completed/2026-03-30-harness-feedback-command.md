# /harness-feedback 命令实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 新增独立命令 `/harness-feedback`，让用户在目标工程中随时记录改进建议并可选提交到 harness 仓库。

**Architecture:** 创建命令文件 `.claude/commands/harness-feedback.md`，通过 Phase 6 安装到目标项目；更新 Phase 1 收集 `harnessRepo`；更新 INSTALL.md 和设计文档保持一致。本仓库为纯内容仓库，无可执行代码，验证方式为 Grep 内容检查。

**Tech Stack:** Markdown（Claude Code 命令格式）、`gh` CLI（目标项目 Issue 提交）

---

## 文件变更清单

| 操作 | 文件 | 内容 |
|------|------|------|
| Create | `.claude/commands/harness-feedback.md` | `/harness-feedback` 命令完整脚本 |
| Modify | `docs/install/phase-1-info-collection.md` | 新增问题 5：harnessRepo |
| Modify | `docs/install/phase-6-finalize.md` | 新增 harness-feedback.md 安装步骤 + .gitignore 更新 + 摘要更新 |
| Modify | `INSTALL.md` | 更新文件结构图（`.harness/` + `harness-feedback.md`） |
| Modify | `docs/design-docs/2026-03-29-harness-design.md` | 同步文件结构和数据结构章节 |

---

## Task 1：创建 `/harness-feedback` 命令文件

**Files:**
- Create: `.claude/commands/harness-feedback.md`

- [ ] **步骤 1：确认文件不存在**

  ```bash
  ls .claude/commands/
  ```
  预期输出：列出 `audit.md`、`commit-push.md`、`do.md`，无 `harness-feedback.md`

- [ ] **步骤 2：创建命令文件**

  创建 `.claude/commands/harness-feedback.md`，内容如下：

  ````markdown
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

  生成 slug：将 `PROPOSAL_TITLE` 转为小写，空格和特殊字符替换为连字符，截取前 40 个字符。

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

  将答案写入 `.harness/harness-config.json` 的 `harnessRepo` 字段，同时更新 `updatedAt` 为当前时间戳。

  ### 步骤 4：提交方式

  使用 AskUserQuestion：
  > 是否通过 `gh issue create` 提交到 harness 仓库？
  > - **是**（需要本地已安装并登录 `gh` CLI）
  > - **否**（我将手动创建 Issue）

  ### 步骤 5A：通过 gh CLI 提交

  从 `harnessRepo`（格式：`git@github.com:owner/repo.git`）提取 `owner/repo`：
  去掉 `git@github.com:` 前缀和 `.git` 后缀。

  对每条选中的建议，读取文件完整内容后执行：

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
  > 请在 `https://github.com/<owner/repo>/issues/new` 手动创建 Issue：
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
  ````

- [ ] **步骤 3：验证文件内容关键字**

  ```bash
  grep -c "AskUserQuestion\|harness-config.json\|proposals\|submitted" .claude/commands/harness-feedback.md
  ```
  预期：输出大于 0 的数字（多个关键词均存在）

- [ ] **步骤 4：提交**

  ```bash
  git add .claude/commands/harness-feedback.md
  git commit -m "feat: add /harness-feedback command"
  ```

---

## Task 2：Phase 1 新增 harnessRepo 问题

**Files:**
- Modify: `docs/install/phase-1-info-collection.md`

- [ ] **步骤 1：确认当前末尾内容**

  ```bash
  grep -n "harnessRepo\|问题 5" docs/install/phase-1-info-collection.md
  ```
  预期：无匹配（字段尚不存在）

- [ ] **步骤 2：在「写入配置文件」章节前新增问题 5**

  在文件中找到 `### 写入配置文件` 标题行，在其**前方**插入：

  ```markdown
  ### 问题 5：Harness 仓库地址

  > "请提供 harness 仓库的 Git 地址（用于后续通过 `/harness-feedback` 提交改进建议）。"
  >
  > 例如：`git@github.com:chenpengfei/harness.git`
  >
  > 若暂不需要此功能，可直接回车跳过（留空）。

  记录为：`HARNESS_REPO`（可为空）

  ```

- [ ] **步骤 3：在「写入配置文件」章节的 JSON 模板中新增 harnessRepo 字段**

  在 `harness-config.json` 模板的 `"projectStage"` 字段行之后插入：

  ```json
    "harnessRepo": "<HARNESS_REPO>"
  ```

  最终 JSON 结构末尾应为：
  ```json
    "teamSize": "<TEAM_SIZE>",
    "projectStage": "<PROJECT_STAGE>",
    "harnessRepo": "<HARNESS_REPO>"
  }
  ```

- [ ] **步骤 4：验证**

  ```bash
  grep -n "harnessRepo\|问题 5\|HARNESS_REPO" docs/install/phase-1-info-collection.md
  ```
  预期：输出 3 行以上，包含问题标题、记录变量名、JSON 字段

- [ ] **步骤 5：提交**

  ```bash
  git add docs/install/phase-1-info-collection.md
  git commit -m "feat: add harnessRepo question to phase-1 info collection"
  ```

---

## Task 3：Phase 6 新增 harness-feedback 安装步骤

**Files:**
- Modify: `docs/install/phase-6-finalize.md`

- [ ] **步骤 1：确认当前 harness-feedback 相关内容不存在**

  ```bash
  grep -n "harness-feedback\|gitignore\|proposals\|submitted" docs/install/phase-6-finalize.md
  ```
  预期：无匹配

- [ ] **步骤 2：在 6.1 和 6.2 之间新增 6.1.5 步骤**

  在 `### 6.2 创建 .claude/commands/harness.md` 标题行前插入：

  ```markdown
  ### 6.1.5 创建 .claude/commands/harness-feedback.md

  从 harness 仓库读取 `.claude/commands/harness-feedback.md` 并创建到目标项目。

  > **Agent 注意**：通过 WebFetch 或 Read 从 harness 仓库对应路径读取文件内容，完全复制，不做任何修改。

  ### 6.1.8 更新 .gitignore

  在目标项目根目录的 `.gitignore` 文件末尾追加以下内容（若 `.gitignore` 不存在则创建）：

  ```
  # Harness 改进建议草稿（本地存档，不提交到目标项目代码库）
  .harness/proposals/
  .harness/submitted/
  ```

  ```

- [ ] **步骤 3：在 6.3 安装摘要的文件清单中新增两行**

  在摘要文件列表中 `- \`.claude/commands/harness.md\`` 行之后插入：

  ```
  > - `.claude/commands/harness-feedback.md`
  ```

  并在下一步建议末尾新增：
  ```
  > 4. 运行 `/harness-feedback` 随时记录实践中发现的改进点
  ```

- [ ] **步骤 4：验证**

  ```bash
  grep -n "harness-feedback\|gitignore\|proposals\|submitted" docs/install/phase-6-finalize.md
  ```
  预期：输出 4 行以上，覆盖新增的三处内容

- [ ] **步骤 5：提交**

  ```bash
  git add docs/install/phase-6-finalize.md
  git commit -m "feat: update phase-6 to install harness-feedback and update .gitignore"
  ```

---

## Task 4：更新 INSTALL.md 文件结构图

**Files:**
- Modify: `INSTALL.md`

- [ ] **步骤 1：确认当前结构图**

  ```bash
  grep -n "harness-config\|harness-feedback\|\.harness" INSTALL.md
  ```
  预期：找到 `.claude/` 下的 `harness-config.json`，无 `.harness/` 目录，无 `harness-feedback.md`

- [ ] **步骤 2：替换文件结构图**

  找到 INSTALL.md 中的文件结构代码块（从 ` ```  ` 到目标项目结构结束），将 `.claude/harness-config.json` 移至 `.harness/` 目录，并新增 `harness-feedback.md`。

  新结构图：

  ````
  ```
  目标项目/
  ├── CLAUDE.md                          # 文档地图（保持 200 行以内）
  ├── .harness/
  │   └── harness-config.json            # Harness 配置（版本、技术栈、阶段等）
  ├── .claude/
  │   ├── commands/
  │   │   ├── commit-push.md             # /commit-push 命令
  │   │   ├── harness.md                 # /harness 更新命令
  │   │   ├── harness-feedback.md        # /harness-feedback 改进反馈命令
  │   │   └── do.md                      # /do 命令（Phase 7 可选）
  │   └── skills/
  │       ├── harness-env.md
  │       ├── harness-knowledge.md
  │       ├── harness-feedback.md
  │       └── agent-team/                # Phase 7 可选
  │           └── *.md
  └── docs/
      ├── environment/
      │   ├── README.md                  # 运行、测试、调试命令
      │   └── setup.md                   # 本地环境搭建
      ├── knowledge/
      │   ├── architecture.md            # 系统架构
      │   └── decisions/                 # ADR 架构决策记录
      ├── constraints/
      │   ├── README.md                  # 模块边界、禁止模式
      │   └── coding-rules.md            # 编码规范
      └── feedback/
          ├── review-checklist.md        # Review / 自检清单
          └── retro-template.md          # 复盘模板
  ```
  ````

- [ ] **步骤 3：验证**

  ```bash
  grep -n "\.harness\|harness-feedback" INSTALL.md
  ```
  预期：找到 `.harness/` 目录行和 `harness-feedback.md` 行

- [ ] **步骤 4：提交**

  ```bash
  git add INSTALL.md
  git commit -m "docs: update INSTALL.md file structure for .harness/ and harness-feedback"
  ```

---

## Task 5：同步设计文档

**Files:**
- Modify: `docs/design-docs/2026-03-29-harness-design.md`

- [ ] **步骤 1：确认当前状态**

  ```bash
  grep -n "harness-config\|harness-feedback\|\.harness" docs/design-docs/2026-03-29-harness-design.md
  ```
  预期：找到 `.claude/harness-config.json`，无 `.harness/`，无 `harness-feedback`

- [ ] **步骤 2：更新「目标工程安装后结构」代码块**

  在设计文档的文件结构图中：
  - 将 `├── .claude/` 下的 `harness-config.json` 一行删除
  - 在 `├── CLAUDE.md` 下方新增 `.harness/` 目录块：
    ```
    ├── .harness/
    │   └── harness-config.json            # Harness 配置（4 个问题的答案）
    ```
  - 在 `commands/` 下的 `harness.md` 行后新增：
    ```
    │   │   └── harness-feedback.md        # /harness-feedback 反馈命令
    ```

- [ ] **步骤 3：更新「数据结构」章节的 JSON 示例**

  找到 `### \`.claude/harness-config.json\`` 标题，将其改为 `### \`.harness/harness-config.json\``。

  在 JSON 示例的 `"projectStage"` 字段后新增：
  ```json
    "harnessRepo": "git@github.com:chenpengfei/harness.git"
  ```

- [ ] **步骤 4：更新「/harness 命令更新流程」章节开头说明**

  找到描述「读取 `.claude/harness-config.json`」的句子（步骤 1），确认已是 `.harness/harness-config.json`（phase-6 的 harness.md 模板已更新，此处同步）。若仍为旧路径则替换。

- [ ] **步骤 5：验证**

  ```bash
  grep -n "\.harness\|harness-feedback\|harnessRepo" docs/design-docs/2026-03-29-harness-design.md
  ```
  预期：三个关键词均有匹配

- [ ] **步骤 6：提交**

  ```bash
  git add docs/design-docs/2026-03-29-harness-design.md
  git commit -m "docs: sync harness-design.md for .harness/ directory and harness-feedback command"
  ```

---

## Task 6：运行 /audit 验证一致性

- [ ] **步骤 1：运行 /audit**

  在 harness 仓库根目录运行：
  ```
  /audit
  ```

- [ ] **步骤 2：处理发现的问题**

  - `[违反原则 X]` 类问题：按报告说明修复
  - `[需人工确认]` 类问题：逐一判断是否需要处理
  - 若发现与本次改动相关的一致性问题，当场修复并追加到对应的最近一次 commit（`git commit --amend`）或新建 commit

- [ ] **步骤 3：确认最终状态**

  ```bash
  git log --oneline -6
  ```
  预期：看到 Task 1-5 的 5 条 commit，加上 spec 文档的 commit
