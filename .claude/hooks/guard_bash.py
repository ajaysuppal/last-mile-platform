"""PreToolUse hook: block dangerous git commands before Claude runs them.

Reads the hook payload (JSON) from stdin. Exit code 2 blocks the command and shows the reason to Claude.
Stdlib only and Python 3.9-compatible so it runs with any system python3 (macOS, Linux, Windows).
"""

import json
import re
import sys

RULES = [
    (
        r"\bgit\s+push\b.*(\s--force(-with-lease)?\b|\s-f\b)",
        "Force-push is not allowed; main history is protected.",
    ),
    (
        r"\bgit\s+push\b.*\s(origin\s+)?(HEAD:)?(refs/heads/)?main\b",
        "Push a feature branch and open a PR instead of pushing to main.",
    ),
    (r"\bgit\s+commit\b.*--no-verify", "Do not skip hooks; fix the failing check instead."),
    (r"\bgit\s+reset\s+--hard\b", "git reset --hard discards work; ask the user first."),
    (r"\bgit\s+add\b.*(\s|/)\.env(\s|$)", "Never stage .env files."),
]


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0
    command = (payload.get("tool_input") or {}).get("command") or ""
    for pattern, reason in RULES:
        if re.search(pattern, command):
            print(f"Blocked by .claude/hooks/guard_bash.py: {reason}", file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
