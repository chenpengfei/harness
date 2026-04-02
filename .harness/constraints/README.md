# Harness 开发约束

本文档定义 harness 仓库的开发约束和禁止模式，是对 ARCHITECTURE.md 中设计原则的可操作细化。

---

## 核心约束

### 约束 1：文档使用符号名称而非硬链接

文档内部引用使用文件名或标题等符号名称：

- 禁止：`[文本](../other-file.md)` 形式的跨文件硬链接
- 允许：直接引用文件名（如「详见 `phase-3-knowledge.md`」）

### 约束 2：INSTALL.md 是单一真相来源

- 所有安装步骤必须可从 INSTALL.md 追溯到对应 phase 文件
- Phase 文件标题须与 INSTALL.md 安装流程地图表格中的描述一致
- 不在 phase 文件中引入与 INSTALL.md 矛盾的阶段目的

### 约束 3：设计变更先于实现

- `feat:` 或 `refactor:` 类提交须有对应的 `docs/design-docs/` 文档
- 设计文档日期须 ≤ 提交日期（设计先于或同日实现）

---

## 命名规范

| 类型 | 格式 | 示例 |
|------|------|------|
| 设计文档 | `docs/design-docs/YYYY-MM-DD-<name>-design.md` | `2026-03-29-do-command-design.md` |
| 执行计划 | `docs/exec-plans/completed/YYYY-MM-DD-<name>.md` | `2026-03-29-do-command.md` |
| Phase 文件 | `install/phase-N-<slug>.md` | `phase-3-knowledge.md` |

---

## 验证方式

运行 `/govern` 可自动检查上述约束的遵守情况。
