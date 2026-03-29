# Phase 4：C — 约束

**Agent 执行步骤：**

根据 `PROJECT_STAGE` 调整约束严格程度。

### 4.1 创建 docs/constraints/ 目录

### 4.2 创建 docs/constraints/README.md

基础模板（所有配置通用）：

    # 约束

    <PROJECT_NAME> 的架构规则和边界。

如果 `PROJECT_STAGE = exploration`，在标题后追加：

    > 早期探索阶段，以下约束为指导原则而非硬性规定，随系统演化持续更新。

如果 `PROJECT_STAGE = production`，在标题后追加：

    > 生产系统。违反以下约束前请团队评审。

所有配置追加以下内容：

    ## 模块边界

    > 描述模块结构和允许的依赖关系。随架构演化填写。

    ## 依赖方向

    > 描述哪些模块可以依赖哪些模块（例如：UI → Business Logic → Data Access）。

    ## 禁止模式

    > 发现反模式时在此记录，附上原因。

    | 模式 | 原因 | 替代方案 |
    |------|------|----------|
    | _(暂无)_ | | |

    ## 命名约定

    > 关键命名规则。详细编码规范参见 `coding-rules.md`。

    ## Agent 友好性

    Agent 在此代码库中工作时依赖以下四条原则维持可靠性：

    1. **测试即合约**：测试是代码行为的唯一可信定义。无测试覆盖等于未定义合约，Agent 无法安全修改。
    2. **文档与代码一致**：文档与实现矛盾时，Agent 会在两者之间犯错。文档过时等同于 bug。
    3. **防止错误复合**：Agent 会在错误基础上叠加错误。第一步代码必须自洽，错误须在边界处尽早暴露。
    4. **设计模式统一**：同一问题有两种做法时，Agent 无法判断选哪个。选定模式后全库统一。

    详细规则参见 `coding-rules.md`。

### 4.3 创建 docs/constraints/coding-rules.md

基础模板（所有配置通用）：

    # 编码规范

    <PROJECT_NAME> 的编码规范和禁止模式。

如果 `PROJECT_STAGE = exploration`，追加：

    > 早期阶段：规范从实践中提炼，发现需要固定的模式时在此记录。

如果 `PROJECT_STAGE = production`，追加：

    > 生产代码标准：所有新代码必须遵守，重构旧代码时顺手改正。

所有配置追加通用规则：

    ## 通用规则

    - 函数单一职责：一个函数只做一件事
    - 不超过 3 层嵌套：超过时提取函数
    - 魔法数字必须命名为常量

    ## Agent 友好性规则

    | 原则 | 规则 |
    |------|------|
    | 测试即合约 | 新功能须有测试；修改已有逻辑时同步更新测试，不允许无测试覆盖的公开接口 |
    | 文档与代码一致 | 改接口或行为时同步更新对应文档；注释与实现矛盾视为 bug |
    | 防止错误复合 | 在系统边界验证输入，不向深层传递无效状态；宁可提前失败，不留隐患蔓延 |
    | 设计模式统一 | 新增模式前检查现有用法；同类问题只用一种解法，例外须注释说明原因 |

如果 `TECH_TYPE = nodejs`，追加：

    ## TypeScript / JavaScript 规则

    - 使用 `const` 优先于 `let`，禁止 `var`
    - 异步代码使用 `async/await`，不用 `.then()` 链
    - catch 块必须记录错误，不允许空 catch

如果 `TECH_TYPE = python`，追加：

    ## Python 规则

    - 遵循 PEP 8
    - 新函数必须有类型注解
    - 捕获具体异常类型，不允许裸 `except:`

如果 `TECH_TYPE = go`，追加：

    ## Go 规则

    - 错误必须处理，不允许 `_ = err`
    - 接口定义在使用方，不在实现方
    - 避免 panic，使用 error 返回值

如果 `TECH_TYPE = java`，追加：

    ## Java 规则

    - 遵循 Google Java Style Guide
    - 使用 Optional 替代 null 返回
    - Checked exception 用于可恢复错误，unchecked 用于编程错误

所有配置追加：

    ## 禁止模式记录

    | 模式 | 原因 | 替代方案 |
    |------|------|----------|
    | _(发现问题时在此记录)_ | | |

### 4.4 确认点

向用户展示已创建的文件：
> "C（约束）维度安装完成，创建了以下文件：
> - `docs/constraints/README.md`
> - `docs/constraints/coding-rules.md`
>
> 是否继续安装 F（回路）维度？"

等待确认后继续 Phase 5。
