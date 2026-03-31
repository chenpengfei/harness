# Harness 反馈机制

本文档描述 harness 的反馈回路：改进如何从实践中流回 harness 仓库。

---

## 两层反馈

| 层级 | 触发者 | 机制 |
|------|--------|------|
| 使用反馈 | 目标项目用户 | `/harness-feedback` 命令记录改进建议 |
| 开发反馈 | harness 贡献者 | `/audit` 命令检查哲学一致性 |

---

## `/harness-feedback` 使用反馈

安装 harness 后，目标项目中会出现 `/harness-feedback` 命令。用户在实践中发现改进点时：

1. 运行 `/harness-feedback` → 选择「记录改进建议」
2. 填写改进类型（模板/脚本 或 理念/架构）、标题、背景、建议改法
3. 建议保存在 `.harness/proposals/` 下（gitignored，本地存档）
4. 运行 `/harness-feedback` → 选择「查看并提交」可通过 `gh` CLI 提交到 harness 仓库的 GitHub Issues

设计文档：`docs/design-docs/2026-03-30-harness-feedback-command-design.md`

---

## `/audit` 一致性审查

在 harness 仓库开发过程中，`/audit` 命令作为质量回路：

- 检查三轮：术语一致性、结构完整性、原则遵守
- 发现偏差后可选自动修复（第一轮）或输出需人工处理的清单
- 每次 `feat:` 或重大修改后建议运行

---

## 改进建议处理流程

```
目标项目实践 → /harness-feedback 记录 → GitHub Issue 提交
                                                  ↓
                                    harness 维护者评审 / 讨论
                                                  ↓
                                    docs/design-docs/ 设计更新
                                                  ↓
                                    docs/install/phase-*.md 实现
```

---

## /audit 检查点

每次发布前建议通过 `/audit` 零问题状态：

```
✓ 未发现哲学一致性问题，当前 harness 仓库状态健康。
```
