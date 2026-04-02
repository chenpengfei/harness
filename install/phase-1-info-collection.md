# Phase 1：信息收集

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

### 问题 5：Harness 仓库地址

> "请提供 harness 仓库的 Git 地址（用于拉取 `.harness/` 模板目录并在后续通过 `/harness` 同步最新内容）。"
>
> 例如：`git@github.com:chenpengfei/harness.git`
>
> 若暂不需要此功能，可直接回车跳过（留空）。

记录为：`HARNESS_REPO`（可为空）

### 写入配置文件

收集完 5 个答案后，创建 `.harness/` 目录（若不存在），然后创建 `.harness/harness-config.json`：

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
  "projectStage": "<PROJECT_STAGE>",
  "harnessRepo": "<HARNESS_REPO>"
}
```

向用户展示配置摘要，询问：
> "以上信息是否正确？确认后将开始安装第一个维度（E - 环境）。"

等待确认后继续 Phase 2。

### 拉取 .harness/ 模板目录

**若 `HARNESS_REPO` 非空**，在创建配置文件后，将 harness 仓库的 `.harness/` 目录拉取到目标工程：

```bash
# 使用 git sparse-checkout 仅拉取 .harness/ 目录
git clone --depth=1 --filter=blob:none --sparse <HARNESS_REPO> /tmp/harness_pull_tmp
cd /tmp/harness_pull_tmp
git sparse-checkout set .harness
cd -
# 将 .harness/ 中的文件复制到目标项目（保留 harness-config.json，不覆盖）
rsync -av --exclude='harness-config.json' /tmp/harness_pull_tmp/.harness/ .harness/
rm -rf /tmp/harness_pull_tmp
```

若 git 命令执行失败或 `HARNESS_REPO` 为空，跳过此步骤；后续 Phase 2–5 会直接在 `.harness/` 下生成所需文件。

> **说明**：此步骤将 harness 仓库的 E-K-C-F 模板文件预填充到 `.harness/` 中，后续各 Phase 会根据项目实际情况覆盖或补充这些文件的内容。
