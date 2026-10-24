"""PostToolUse hook: format and auto-fix Python files that Claude just edited.

Never blocks: if ruff or uv is unavailable the hook exits quietly. Stdlib only, Python 3.9-compatible.
"""

import json
import shutil
import subprocess
import sys


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0
    path = (payload.get("tool_input") or {}).get("file_path") or ""
    if not path.endswith(".py") or shutil.which("uv") is None:
        return 0
    for args in (["ruff", "format", path], ["ruff", "check", "--fix", "--quiet", path]):
        subprocess.run(["uv", "run", "--no-sync", *args], capture_output=True, check=False)  # noqa: S603, S607
    return 0


if __name__ == "__main__":
    sys.exit(main())
