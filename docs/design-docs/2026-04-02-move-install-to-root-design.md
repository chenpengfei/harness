# 设计文档：将 install/ 目录移至项目根目录

**日期**：2026-04-02
**类型**：refactor
**状态**：已实施

## 背景

原目录结构将安装阶段剧本放在 `docs/install/` 下，与设计文档、执行计划等同属 `docs/` 层级。但 `install/` 在功能上与 `INSTALL.md` 强绑定，是整个系统的核心内容；将其埋在 `docs/` 下层次偏深，也使 `docs/` 目录语义混杂（文档 vs. 可执行剧本）。

## 决定

将 `docs/install/` 整体移动到项目根目录，变为 `install/`，与 `INSTALL.md` 同级。

## 影响范围

**正面影响：**
- `install/` 与 `INSTALL.md` 同级，层次关系更直观
- `docs/` 目录职责更纯粹（仅含设计文档、执行计划、参考文献）
- Agent 读取 `INSTALL.md` 后，按路径引用 `install/phase-N-*.md` 更直接

**负面影响 / 代价：**
- 历史文档（`docs/exec-plans/completed/`、`docs/design-docs/`）中仍保留旧路径 `docs/install/`，这是预期的（历史记录不应被改写）

## 变更文件

共更新 9 个活跃文件中的路径引用，保留 6 个历史记录文件不变。详见对应 refactor commit。
