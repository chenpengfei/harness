# Phase 2：E — 环境

**Agent 执行步骤：**

根据 Phase 1 收集的 `TECH_TYPE` 选择对应模板。

### 2.1 创建目录

在目标项目中创建 `.harness/environment/` 目录（若不存在）。

### 2.2 创建 .harness/environment/README.md

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

### 2.3 创建 .harness/environment/setup.md

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
    1. Read `.harness/environment/README.md` and `.harness/environment/setup.md`
    2. Check what has changed (new dependencies, scripts, env vars)
    3. Update the relevant sections
    4. Ask the user to verify the commands are still accurate

    When auditing environment documentation:
    1. Check if the commands in `.harness/environment/README.md` are current
    2. Check if prerequisites in `.harness/environment/setup.md` are complete
    3. Report outdated or missing information

### 2.5 确认点

向用户展示已创建的文件：
> "E（环境）维度安装完成，创建了以下文件：
> - `.harness/environment/README.md`
> - `.harness/environment/setup.md`
> - `.claude/skills/harness-env.md`
>
> 是否继续安装 K（知识）维度？"

等待确认后继续 Phase 3。
