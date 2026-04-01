#!/usr/bin/env python3
"""
validate-commit-msg.py

Claude Code PreToolUse hook。
当 Bash 工具执行 git commit 命令时，验证提交消息是否符合
Conventional Commits 规范。不合规则拦截（exit 2）并打印说明。

Hook 输入（stdin）：
  {"session_id": "...", "tool_name": "Bash", "tool_input": {"command": "..."}}

退出码：
  0 — 放行
  2 — 拦截，并向 stdout 输出错误说明
"""
import sys
import json
import re


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    command: str = data.get("tool_input", {}).get("command", "")

    # 仅处理 git commit 命令
    if "git commit" not in command:
        sys.exit(0)

    # 提取 -m 参数的消息（支持单引号和双引号）
    m = re.search(r'-m\s+["\'](.+?)["\']', command)
    if not m:
        # 无 -m 参数（如编辑器模式），放行
        sys.exit(0)

    msg = m.group(1)

    # 验证 Conventional Commits 格式
    pattern = r'^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\(.+\))?(!)?: .+'
    if not re.match(pattern, msg):
        print("提交消息不符合 Conventional Commits 规范。")
        print("格式：<type>[scope][!]: <中文描述>")
        print("类型：feat  fix  docs  style  refactor  perf  test  build  ci  chore  revert")
        print("示例：feat(auth): 新增 OAuth2 登录支持")
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
