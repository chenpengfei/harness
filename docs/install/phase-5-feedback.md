# Phase 5：F — 反馈

**Agent 执行步骤：**

根据 `TEAM_SIZE` 调整内容深度：solo 使用简化版，small/large 使用完整版。

### 5.1 创建 .harness/feedback/ 目录

### 5.2 创建 .harness/feedback/review-checklist.md

**如果 TEAM_SIZE = solo：**

    # 自检清单

    提交代码前快速过一遍。

    ## 正确性
    - [ ] 是否实现了预期功能？
    - [ ] 边界条件处理了吗？

    ## 代码质量
    - [ ] 代码可读吗？
    - [ ] 有没有遗留调试代码（console.log、print、断点）？

    ## 测试
    - [ ] 核心逻辑有测试覆盖吗？
    - [ ] 测试通过了吗？

    ## 文档
    - [ ] 重要决策记录了吗？

**如果 TEAM_SIZE = small 或 large：**

    # Code Review 清单

    每个 PR/变更 Review 时使用本清单。

    ## 正确性
    - [ ] 是否实现了预期功能？
    - [ ] 边界条件是否处理？
    - [ ] 有没有明显的 bug？

    ## 代码质量
    - [ ] 可读性和自文档性
    - [ ] 是否遵循 `.harness/constraints/coding-rules.md`
    - [ ] 有无不必要的复杂度
    - [ ] 函数/类是否职责单一

    ## 测试
    - [ ] 是否有测试？
    - [ ] 测试是否覆盖主要行为和关键边界条件？
    - [ ] 测试通过了吗？

    ## 安全
    - [ ] 是否有敏感信息硬编码？
    - [ ] 输入是否有合适的验证？

    ## 文档
    - [ ] 重要设计决策是否记录在 `.harness/knowledge/decisions/`？
    - [ ] CLAUDE.md 是否仍然准确且保持在 200 行以内？

### 5.3 创建 .harness/feedback/retro-template.md

**如果 TEAM_SIZE = solo：**

    # 复盘模板

    > 每隔 1-2 周，或完成一个重要里程碑后使用。

    日期：YYYY-MM-DD
    主题：[这次复盘涵盖什么]

    ## 做得好的
    -

    ## 遇到的问题
    -

    ## 下次改进
    -

    ## Harness 改进
    - [ ] 有没有文档需要更新？
    - [ ] 有没有约束需要添加？
    - [ ] Agent 工作是否顺畅？

**如果 TEAM_SIZE = small 或 large：**

    # 复盘模板

    > Sprint/里程碑结束后使用。

    日期：YYYY-MM-DD
    Sprint/里程碑：[名称]
    参与者：[人员列表]

    ## 数据
    - 计划完成：X 项
    - 实际完成：Y 项
    - 未完成原因：

    ## 做得好的
    -

    ## 遇到的问题
    -

    ## 行动项
    | 行动 | 负责人 | 截止日期 |
    |------|--------|----------|
    | | | |

    ## Harness 改进
    - [ ] 有没有文档需要更新？（运行 `/harness` 重新评估）
    - [ ] 有没有新的编码约束需要加入 `.harness/constraints/`？
    - [ ] Agent 执行质量如何？有没有明显的知识缺口？
    - [ ] 反馈是否有效？

### 5.5 确认点

向用户展示已创建的文件：
> "F（反馈）维度安装完成，创建了以下文件：
> - `.harness/feedback/review-checklist.md`
> - `.harness/feedback/retro-template.md`
>
> 所有 4 个维度已安装完成！最后一步：生成 `/harness` 更新命令。是否继续？"

等待确认后继续 Phase 6。
