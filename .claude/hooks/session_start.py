#!/usr/bin/env python3
"""SessionStart hook: make the checkout runnable and tell Claude where it is.

- Runs `uv sync` when .venv is missing or older than uv.lock (a fresh worktree).
- Prints one status line, which Claude Code adds to the session's context:
  main checkout vs worktree, branch, profile, whether this checkout has a swarm
  and a .env yet.
Never fails the session.
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def git(cwd: Path, *args: str) -> str:
    try:
        result = subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, text=True,
                                timeout=5)
    except (OSError, subprocess.SubprocessError):
        return ""
    return result.stdout.strip() if result.returncode == 0 else ""


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except ValueError:
        data = {}
    cwd = Path(data.get("cwd") or os.getcwd())
    top = git(cwd, "rev-parse", "--show-toplevel")
    if not top:
        return
    root = Path(top)
    if not (root / "common.py").exists() or not (root / "pyproject.toml").exists():
        return  # not a specialist-swarm checkout

    # Re-sync when .venv is missing or the lock/pyproject changed since our last sync.
    marker = root / ".venv" / ".session-hook-synced"
    sources = [p for p in (root / "uv.lock", root / "pyproject.toml") if p.exists()]
    stale = not marker.exists() or any(p.stat().st_mtime > marker.stat().st_mtime for p in sources)
    synced = "ready"
    if stale and shutil.which("uv"):
        result = subprocess.run(["uv", "sync", "--quiet"], cwd=root, capture_output=True,
                                text=True, timeout=180)
        if result.returncode == 0:
            marker.touch()
            synced = "synced now"
        else:
            synced = "uv sync FAILED (run `uv sync`)"
    elif stale:
        synced = "missing or stale (install uv, then `uv sync`)"

    branch = git(root, "branch", "--show-current") or "(detached)"
    linked = git(root, "rev-parse", "--git-dir") != git(root, "rev-parse", "--git-common-dir")
    profile = os.environ.get("SWARM_PROFILE") or ("demo" if branch == "main" else "dev")
    where = (f"worktree {root.name} on branch {branch}" if linked
             else f"MAIN checkout on branch {branch} (pull, demo and create worktrees here; "
                  "edits are blocked)")
    swarm = "set up" if (root / ".swarm_state.json").exists() else \
        "not set up in this checkout yet (`uv run python setup_swarm.py`, free)"
    env = "present" if (root / ".env").exists() else "MISSING (copy .env from the main checkout)"
    print(f"specialist-swarm: {where} · profile {profile} · swarm {swarm} · .env {env} · "
          f".venv {synced}")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:  # never block a session start
        print(f"specialist-swarm session hook skipped: {error}")
