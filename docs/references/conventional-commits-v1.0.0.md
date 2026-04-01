# Conventional Commits 1.0.0

> **来源**：https://www.conventionalcommits.org/en/v1.0.0/
> **许可**：[Creative Commons - CC BY 3.0](https://creativecommons.org/licenses/by/3.0/)

---

## 摘要（Summary）

Conventional Commits 规范是一种基于提交消息的轻量级约定，提供了一套简单的规则来创建清晰的提交历史，便于构建自动化工具。该约定与 [SemVer](http://semver.org/) 相辅相成，通过提交消息描述功能新增、Bug 修复和破坏性变更。

提交消息的结构如下：

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

结构化元素说明：

1. **fix:** 类型为 `fix` 的提交修复了代码库中的 Bug（对应 SemVer 的 `PATCH`）。
2. **feat:** 类型为 `feat` 的提交为代码库引入了新功能（对应 SemVer 的 `MINOR`）。
3. **BREAKING CHANGE:** 在 footer 中包含 `BREAKING CHANGE:`，或在 type/scope 后追加 `!`，表示引入了破坏性 API 变更（对应 SemVer 的 `MAJOR`）。可出现在任意类型的提交中。
4. 除 `fix:` 和 `feat:` 外，还允许使用其他类型，例如 `build:`、`chore:`、`ci:`、`docs:`、`style:`、`refactor:`、`perf:`、`test:` 等（参考 [@commitlint/config-conventional](https://github.com/conventional-changelog/commitlint/tree/master/%40commitlint/config-conventional) 及 Angular 约定）。
5. 除 `BREAKING CHANGE: <description>` 外，还可以提供其他 footer，遵循类似 [git trailer format](https://git-scm.com/docs/git-interpret-trailers) 的约定。

scope 可以附加在 type 之后，提供额外的上下文信息，包含在括号内，例如 `feat(parser): add ability to parse arrays`。

---

## 示例（Examples）

**包含 description 和 breaking change footer：**
```
feat: allow provided config object to extend other configs

BREAKING CHANGE: `extends` key in config file is now used for extending other config files
```

**用 `!` 标注 breaking change：**
```
feat!: send an email to the customer when a product is shipped
```

**带 scope 和 `!`：**
```
feat(api)!: send an email to the customer when a product is shipped
```

**同时包含 `!` 和 BREAKING CHANGE footer：**
```
feat!: drop support for Node 6

BREAKING CHANGE: use JavaScript features not available in Node 6.
```

**无 body：**
```
docs: correct spelling of CHANGELOG
```

**带 scope：**
```
feat(lang): add Polish language
```

**多段 body 和多个 footer：**
```
fix: prevent racing of requests

Introduce a request id and a reference to latest request. Dismiss
incoming responses other than from latest request.

Remove timeouts which were used to mitigate the racing issue but are
obsolete now.

Reviewed-by: Z
Refs: #123
```

---

## 规范（Specification）

本文件中的关键词 "MUST"、"MUST NOT"、"REQUIRED"、"SHALL"、"SHALL NOT"、"SHOULD"、"SHOULD NOT"、"RECOMMENDED"、"MAY"、"OPTIONAL" 按 [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt) 解释。

1. 提交消息**必须（MUST）**以 type 作为前缀，type 由名词组成（如 `feat`、`fix` 等），后接可选的 scope、可选的 `!`，以及**必须（REQUIRED）**的冒号和空格。
2. 当提交为应用或库新增功能时，**必须（MUST）**使用 `feat` 类型。
3. 当提交为应用修复 Bug 时，**必须（MUST）**使用 `fix` 类型。
4. scope **可以（MAY）**跟在 type 之后，**必须（MUST）**由括号内的名词组成，描述代码库的某个部分，例如 `fix(parser):`。
5. description **必须（MUST）**紧跟在 type/scope 前缀的冒号和空格之后，是对代码变更的简短摘要。
6. 在 description 之后**可以（MAY）**提供更长的 body，提供额外的上下文信息。body **必须（MUST）**在 description 后空一行开始。
7. commit body 为自由格式，**可以（MAY）**由任意数量的换行分隔段落组成。
8. 一个或多个 footer **可以（MAY）**在 body 后空一行处提供。每个 footer **必须（MUST）**由一个 word token 组成，后接 `:<space>` 或 `<space>#` 分隔符，再后接字符串值（参考 [git trailer convention](https://git-scm.com/docs/git-interpret-trailers)）。
9. footer 的 token **必须（MUST）**用 `-` 代替空白字符，例如 `Acked-by`（以区分 footer 和多段 body）。`BREAKING CHANGE` 是例外，**可以（MAY）**用作 token。
10. footer 的值**可以（MAY）**包含空格和换行，当观察到下一个有效的 footer token/分隔符对时，解析**必须（MUST）**终止。
11. breaking change **必须（MUST）**在提交的 type/scope 前缀中或作为 footer 条目注明。
12. 如果作为 footer 注明，breaking change **必须（MUST）**包含大写文本 `BREAKING CHANGE`，后接冒号、空格和描述，例如 `BREAKING CHANGE: environment variables now take precedence over config files`。
13. 如果在 type/scope 前缀中注明，breaking change **必须（MUST）**在 `:` 之前紧接 `!`。使用 `!` 时，footer 中**可以（MAY）**省略 `BREAKING CHANGE:`，此时提交 description 用于描述 breaking change。
14. `feat` 和 `fix` 以外的其他类型**可以（MAY）**用于提交消息，例如 `docs: update ref docs.`。
15. Conventional Commits 的各信息单元对于实现者**不得（MUST NOT）**区分大小写，`BREAKING CHANGE` 例外，**必须（MUST）**大写。
16. `BREAKING-CHANGE` 在用作 footer token 时**必须（MUST）**与 `BREAKING CHANGE` 同义。

---

## 为什么使用 Conventional Commits

- 自动生成 CHANGELOG
- 自动确定语义版本号升级（基于提交类型）
- 向团队成员、公众及其他利益相关者传达变更的性质
- 触发构建和发布流程
- 通过提供更结构化的提交历史，降低他人参与贡献的门槛
