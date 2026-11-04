#!/usr/bin/env python3
"""PreToolUse hook (Edit|Write|NotebookEdit): block Claude's file edits on `main`.

This team works in worktrees (`claude -w <you>-<topic>`); the main checkout is for
pulling, demo runs and creating worktrees. Only files inside this repository (any
of its worktrees) are guarded. Start Claude with ALLOW_MAIN_EDITS=1 to override.
"""

import json
import os
import subprocess
import sys


def git(cwd: str, *args: str) -> str:
    try:
        result = subprocess.run(["git", "-C", cwd, *args], capture_output=True, text=True,
                                timeout=5)
    except (OSError, subprocess.SubprocessError):
        return ""
    return result.stdout.strip() if result.returncode == 0 else ""


def main() -> int:
    if os.environ.get("ALLOW_MAIN_EDITS") == "1":
        return 0
    try:
        data = json.load(sys.stdin)
    except ValueError:
        return 0
    tool_input = data.get("tool_input") or {}
    path = tool_input.get("file_path") or tool_input.get("notebook_path")
    if not path:
        return 0

    directory = os.path.dirname(os.path.abspath(path))
    while not os.path.isdir(directory):  # a new file may be in a new directory
        parent = os.path.dirname(directory)
        if parent == directory:
            return 0
        directory = parent

    project = os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or ""
    ours = git(project, "rev-parse", "--path-format=absolute", "--git-common-dir")
    theirs = git(directory, "rev-parse", "--path-format=absolute", "--git-common-dir")
    if not ours or ours != theirs:
        return 0  # not this repository
    if git(directory, "branch", "--show-current") not in ("main", "master"):
        return 0

    print(f"Blocked: {path} is on branch main. This team never edits main directly. "
          "Use the EnterWorktree tool (name it <person>-<topic>) or ask the user to start "
          "`claude -w <person>-<topic>`, then make the edit there. "
          "(To override for a session, start Claude with ALLOW_MAIN_EDITS=1.)",
          file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
