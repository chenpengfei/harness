# 参考文献

Harness 设计的理论与实践来源。

---

- Ryan Lopopolo（OpenAI），[工程技术：在智能体优先的世界中利用 Codex](https://openai.com/zh-Hans-CN/index/harness-engineering/)，2026年2月11日
  > "要给 Codex 的是一张地图，而不是一本 1,000 页的说明书。"
  > 一份简短的 AGENTS.md（大约 100 行）被注入到情境中，主要用作地图，并指向其他地方更深层次的真实信息来源。

- matklad（JetBrains），[ARCHITECTURE.md](https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html)，2021年2月6日
  > "要写一张地图，而不是各州地图的地图集（A codemap is a map of a country, not an atlas of maps of its states）。"
  > 架构文档的核心是 codemap：粗粒度模块及其关系，回答"做 X 的代码在哪里"。命名重要的文件、模块和类型，但不直接链接（链接会过期）。显式声明架构不变式，尤其是缺席关系（某层刻意不依赖某层）。简短是关键——每个反复贡献者都必须读它，越短越不容易被未来的变更废弃。

- Conventional Commits，[Conventional Commits 1.0.0 规范](https://www.conventionalcommits.org/en/v1.0.0/)，2019年
  > "A specification for adding human and machine readable meaning to commit messages."
  > 基于提交消息的轻量级约定，提供结构化规则以创建清晰的提交历史，与 SemVer 配合实现自动化版本管理。完整规范见 `docs/references/conventional-commits-v1.0.0.md`。

- sanbuphy，[claude-code-source-code](https://github.com/sanbuphy/claude-code-source-code)（`@anthropic-ai/claude-code` v2.1.88 逆向解析），2025年
  > Claude Code 约 1884 个 TypeScript 源文件的逆向工程版本。基于此整理的 12 个 Harness 机制源码解读见 `docs/references/claude-code-12-mechanisms.md`。

- 宝玉，[从写代码到管 Agent：斯坦福首门 AI 软件开发课的讲师说，大多数工程师还没准备好](https://mp.weixin.qq.com/s/Jq6Rgr0DZSneVn_TdWbMpw)，2026年2月28日
  > "Agent 只能基于显式定义的合约来运作。如果你没有足够的测试覆盖，你就没有给你的软件定义合约。"
  > Agent 友好的代码库，其实就是对人也友好的代码库。好的工程实践没有变，只是在 Agent 时代变成了硬性要求。
