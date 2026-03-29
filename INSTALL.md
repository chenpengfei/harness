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

---

## Phase 1：信息收集

**Agent 执行步骤：**

逐一向用户提问，等待回答后再问下一个。将所有答案记录在内存中供后续阶段使用。

### 问题 1：项目名称

> "请告诉我这个项目的名称，以及一句话描述它是做什么的。"
>
> 例如：「acr-service — 医院 AI 审核服务，自动化保险理赔审核流程」

记录为：`PROJECT_NAME` 和 `PROJECT_DESCRIPTION`

### 问题 2：技术栈

> "这个项目主要使用什么技术栈？（编程语言、主要框架）"
>
> 例如：「TypeScript / Next.js / PostgreSQL」或「Python / FastAPI / Redis」

记录为：`TECH_STACK`

技术栈类型识别规则（用于后续模板生成）：
- 含 node / npm / typescript / javascript / next / react / vue → `TECH_TYPE = nodejs`
- 含 python / fastapi / django / flask / uvicorn → `TECH_TYPE = python`
- 含 go / golang → `TECH_TYPE = go`
- 含 java / spring / maven / gradle → `TECH_TYPE = java`
- 其他 → `TECH_TYPE = generic`

### 问题 3：团队规模

> "项目团队规模是多少？"
>
> A. Solo（只有我一人）
> B. 小团队（2-5 人）
> C. 大团队（6 人以上）

记录为：`TEAM_SIZE`（solo / small / large）

### 问题 4：项目阶段

> "项目目前处于哪个阶段？"
>
> A. 早期探索（MVP/原型，快速变化）
> B. 产品迭代（功能稳定，持续迭代）
> C. 生产运营（线上系统，稳定性优先）

记录为：`PROJECT_STAGE`（exploration / iteration / production）

### 写入配置文件

收集完 4 个答案后，创建 `.claude/` 目录（若不存在），然后创建 `.claude/harness-config.json`：

```json
{
  "version": "1.0",
  "installedAt": "<当前 ISO 8601 时间戳，如 2026-03-29T10:00:00Z>",
  "updatedAt": "<当前 ISO 8601 时间戳>",
  "project": {
    "name": "<PROJECT_NAME>",
    "description": "<PROJECT_DESCRIPTION>"
  },
  "techStack": "<TECH_STACK>",
  "techType": "<TECH_TYPE>",
  "teamSize": "<TEAM_SIZE>",
  "projectStage": "<PROJECT_STAGE>"
}
```

向用户展示配置摘要，询问：
> "以上信息是否正确？确认后将开始安装第一个维度（E - 环境）。"

等待确认后继续 Phase 2。

---

## Phase 2：E — 环境

**Agent 执行步骤：**

根据 Phase 1 收集的 `TECH_TYPE` 选择对应模板。

### 2.1 创建目录

在目标项目中创建 `docs/environment/` 目录（若不存在）。

### 2.2 创建 docs/environment/README.md

**如果 TECH_TYPE = nodejs，**文件内容为：

    # Environment

    ## Quick Start

        npm install
        npm run dev

    ## Running Tests

        npm test

    ## Debugging

        # 启动 Node.js inspector
        node --inspect src/index.js
        # 然后在 Chrome 中打开 chrome://inspect

    ## Observability

    Check console output for logs.

**如果 TECH_TYPE = python，**文件内容为：

    # Environment

    ## Quick Start

        pip install -r requirements.txt
        # 或使用 uv：
        uv sync

        python main.py
        # 或：
        uvicorn main:app --reload

    ## Running Tests

        pytest

    ## Debugging

        # 在代码中设置断点：
        import pdb; pdb.set_trace()

    ## Observability

    Check console output. Configure log level via LOG_LEVEL env var.

**如果 TECH_TYPE = go，**文件内容为：

    # Environment

    ## Quick Start

        go mod download
        go run ./cmd/main.go

    ## Running Tests

        go test ./...

    ## Debugging

        go install github.com/go-delve/delve/cmd/dlv@latest
        dlv debug ./cmd/main.go

    ## Observability

    Check stdout for logs. Use `slog` for structured logging.

**如果 TECH_TYPE = java，**文件内容为：

    # Environment

    ## Quick Start

        ./mvnw install -DskipTests
        ./mvnw spring-boot:run

    ## Running Tests

        ./mvnw test

    ## Debugging

        ./mvnw spring-boot:run -Dspring-boot.run.jvmArguments="-Xdebug -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=5005"

    ## Observability

    Check application logs. Spring Boot Actuator at /actuator.

**如果 TECH_TYPE = generic，**文件内容为：

    # Environment

    ## Quick Start

        # 在此填写安装依赖的命令
        # 在此填写启动项目的命令

    ## Running Tests

        # 在此填写测试命令

    ## Debugging

        > 描述本项目的调试工作流。

    ## Observability

        > 描述如何查看日志和观察系统状态。

### 2.3 创建 docs/environment/setup.md

所有技术栈通用，将 `[PROJECT_NAME]` 替换为实际项目名：

    # Local Setup

    ## Prerequisites

    > 列出运行本项目前需要安装的工具和版本。

    - [工具 1 及版本]
    - [工具 2 及版本]

    ## First-Time Setup

    1. Clone 仓库
    2. [步骤 2]
    3. [步骤 3]

    ## Environment Variables

    在项目根目录创建 `.env` 文件：

        # 必填
        [VAR_NAME]=[说明]

        # 选填
        [VAR_NAME]=[说明]（默认值：[value]）

    ## Common Issues

    > 记录本地搭建时遇到的问题和解决方案。

    | 问题 | 解决方案 |
    |------|----------|
    | _(暂无)_ | |

### 2.4 创建 .claude/skills/harness-env.md

创建 `.claude/skills/` 目录（若不存在），然后创建 `.claude/skills/harness-env.md`：

    ---
    name: harness-env
    description: Use this skill when updating or auditing the environment documentation for this project.
    ---

    # Environment Documentation Maintenance

    When asked to update environment documentation:
    1. Read `docs/environment/README.md` and `docs/environment/setup.md`
    2. Check what has changed (new dependencies, scripts, env vars)
    3. Update the relevant sections
    4. Ask the user to verify the commands are still accurate

    When auditing environment documentation:
    1. Check if the commands in `docs/environment/README.md` are current
    2. Check if prerequisites in `docs/environment/setup.md` are complete
    3. Report outdated or missing information

### 2.5 确认点

向用户展示已创建的文件：
> "E（环境）维度安装完成，创建了以下文件：
> - `docs/environment/README.md`
> - `docs/environment/setup.md`
> - `.claude/skills/harness-env.md`
>
> 是否继续安装 K（知识）维度？"

等待确认后继续 Phase 3.
