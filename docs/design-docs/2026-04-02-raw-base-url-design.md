# 设计决策：支持可配置 rawBaseUrl 以加速 harness 文件下载

**日期**：2026-04-02
**状态**：已采纳

---

## 背景

在中国大陆等地区，`raw.githubusercontent.com` 访问缓慢甚至不可达。Harness 的安装流程（Phase 6）和 `/harness` 更新（步骤 5.5）均通过 WebFetch 从该域名拉取文件，导致用户体验差。

## 决定

### 方案：可配置 rawBaseUrl + jsDelivr CDN 作为推荐替代

1. **`harness-config.json` 新增可选字段 `rawBaseUrl`**
   - 该字段存储 raw 文件下载的 URL 前缀，优先级高于从 `harnessRepo` 推导的默认地址
   - 空字符串或字段缺失 = 保持原有行为（向后兼容）

2. **推荐使用 jsDelivr CDN**
   URL 格式：`https://cdn.jsdelivr.net/gh/owner/repo@main`
   jsDelivr 是知名公共 CDN，免费镜像 GitHub 公开仓库，在中国大陆访问快速。

3. **README.md 并列提供两条安装指令**
   国际版使用 raw.githubusercontent.com，中国大陆版使用 jsDelivr。

4. **Phase 6 指引补充 URL 一致性原则**
   Agent 应使用与加载 INSTALL.md 相同的 URL 前缀拉取后续文件。

### 候选方案及放弃理由

| 方案 | 放弃理由 |
|------|---------|
| ghproxy / ghfast 等第三方代理 | 可靠性无保障，随时可能失效 |
| Gitee 镜像仓库 | 需持续维护镜像同步，增加运营负担 |
| 多源自动重试 | 文档指令难以描述重试逻辑，对 Agent 不友好 |
| 硬编码 jsDelivr 为唯一地址 | 丧失灵活性，未来若 CDN 服务变化则需改代码 |

## 后果

**正面**：
- 中国大陆用户安装体验显著改善
- 向后兼容：现有安装无需任何修改
- 可配置，用户可替换为任意可访问的 raw URL 前缀

**负面**：
- jsDelivr 有最长约 24 小时的 CDN 缓存，安装的不一定是最新提交（对稳定发布的 main 分支影响极小）
- 用户需手动在 `rawBaseUrl` 中替换实际的 `owner/repo` 坐标（当前提示中有占位符说明）
