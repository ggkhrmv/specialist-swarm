#!/usr/bin/env python3
"""
Worktree helper for the specialist-swarm team.

Uses the same layout as Claude Code's native `claude -w <name>`, so the two mix:

    .claude/worktrees/<name>/   on branch   worktree-<name>   (from origin/main)

Run from anywhere inside the repo (the main checkout or any worktree):

    python3 scripts/wt.py new <you>-<topic>    worktree + .env copy + uv sync (no Claude needed;
                                               with Claude Code, `claude -w <you>-<topic>` does this)
    python3 scripts/wt.py ls                   every worktree: branch, ahead/behind main, dirty, swarm
    python3 scripts/wt.py ship [--merge]       from a worktree: rebase on origin/main -> offline check
                                               -> push -> open (or reuse) the PR; --merge squash-merges
    python3 scripts/wt.py clean                remove worktrees whose PR was merged (asks first)

`ship` and `clean` take --dry-run to print what they would do. Stdlib only.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

BASE = "origin/main"
NAME = re.compile(r"^[a-z0-9][a-z0-9-]{1,47}$")


# ── helpers ───────────────────────────────────────────────────────────────────

def run(cmd: list[str], cwd: Path | None = None, check: bool = True,
        capture: bool = True) -> subprocess.CompletedProcess:
    result = subprocess.run(cmd, cwd=cwd, text=True, capture_output=capture)
    if check and result.returncode != 0:
        detail = (result.stderr or result.stdout or "").strip() if capture else ""
        raise SystemExit(f"$ {' '.join(cmd)}\n{detail}")
    return result


def git(*args: str, cwd: Path | None = None, check: bool = True) -> str:
    return run(["git", *args], cwd=cwd, check=check).stdout.strip()


def ok(cmd: list[str], cwd: Path | None = None) -> bool:
    return run(cmd, cwd=cwd, check=False).returncode == 0


def main_root() -> Path:
    """The main checkout (the one that holds .git), from any worktree."""
    return Path(git("rev-parse", "--path-format=absolute", "--git-common-dir")).parent


def strip_ref(ref: str) -> str:
    prefix = "refs/heads/"
    return ref[len(prefix):] if ref.startswith(prefix) else ref


def worktrees(root: Path) -> list[dict]:
    items, current = [], {}
    for line in git("worktree", "list", "--porcelain", cwd=root).splitlines() + [""]:
        if not line:
            if current:
                items.append(current)
            current = {}
            continue
        key, _, value = line.partition(" ")
        current[key] = value or True
    return items


def counts(path: Path) -> tuple[int, int]:
    """(ahead, behind) of HEAD relative to origin/main."""
    out = git("rev-list", "--left-right", "--count", f"HEAD...{BASE}", cwd=path, check=False)
    ahead, behind = (out.split() + ["0", "0"])[:2]
    return int(ahead), int(behind)


def step(message: str) -> None:
    print(f"\n── {message}", flush=True)


def act(cmd: list[str], cwd: Path, dry_run: bool) -> None:
    """Run a command that changes something (or print it under --dry-run)."""
    if dry_run:
        print(f"   would run: {' '.join(cmd)}")
        return
    if run(cmd, cwd=cwd, check=False, capture=False).returncode != 0:
        raise SystemExit(f"Failed: {' '.join(cmd)}")


def copy_includes(root: Path, target: Path) -> list[str]:
    """Copy the gitignored files listed in .worktreeinclude, as Claude Code does."""
    include = root / ".worktreeinclude"
    copied = []
    if not include.exists():
        return copied
    for raw in include.read_text().splitlines():
        pattern = raw.strip()
        if not pattern or pattern.startswith(("#", "!")):
            continue
        for source in root.glob(pattern.lstrip("/")):
            rel = source.relative_to(root)
            if source.is_file() and ok(["git", "check-ignore", "-q", str(rel)], cwd=root):
                (target / rel).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target / rel)
                copied.append(str(rel))
    return copied


# ── commands ──────────────────────────────────────────────────────────────────

def cmd_new(args: argparse.Namespace) -> None:
    name = args.name
    if not NAME.match(name):
        raise SystemExit("Name it <you>-<topic>: lowercase letters, digits and dashes, "
                         "e.g. alex-legal-redlines.")
    root = main_root()
    path = root / ".claude" / "worktrees" / name
    branch = f"worktree-{name}"
    if path.exists():
        print(f"Already exists: {path}\n  cd {path}   (or from the main checkout: claude -w {name})")
        return

    if not ok(["git", "fetch", "origin", "--quiet"], cwd=root):
        print("  warning: couldn't fetch origin; branching from the last fetched origin/main")
    if ok(["git", "rev-parse", "--verify", "--quiet", f"refs/heads/{branch}"], cwd=root):
        git("worktree", "add", str(path), branch, cwd=root)  # reuse a kept branch
    else:
        git("worktree", "add", "--no-track", "-b", branch, str(path), BASE, cwd=root)

    copied = copy_includes(root, path)
    print(f"Worktree ready: {path}\n  branch {branch} from {BASE}"
          + (f"; copied {', '.join(copied)}" if copied else "; no .env copied (none in main checkout)"))
    if shutil.which("uv"):
        run(["uv", "sync", "--quiet"], cwd=path, check=False, capture=False)
        print("  .venv ready (uv sync)")
    else:
        print("  install uv, then run `uv sync` there")
    print(f"\nNext:\n  cd {path} && claude\n  uv run python setup_swarm.py   # once: this worktree's own swarm")


def cmd_ls(args: argparse.Namespace) -> None:
    root = main_root()
    here = Path(git("rev-parse", "--show-toplevel")).resolve()
    print(f"  {'BRANCH':34s} {'AHEAD':>5s} {'BEHIND':>6s}  {'DIRTY':5s} {'SWARM':5s}  PATH")
    for item in worktrees(root):
        path = Path(item["worktree"]).resolve()
        branch = strip_ref(str(item.get("branch", ""))) or "(detached)"
        ahead, behind = counts(path)
        dirty = "yes" if git("status", "--porcelain", cwd=path, check=False) else "no"
        swarm = "yes" if (path / ".swarm_state.json").exists() else "-"
        mark = "*" if path == here else " "
        rel = "." if path == root.resolve() else str(path.relative_to(root.resolve()))
        print(f"{mark} {branch:34s} {ahead:5d} {behind:6d}  {dirty:5s} {swarm:5s}  {rel}")


def cmd_ship(args: argparse.Namespace) -> None:
    root = Path(git("rev-parse", "--show-toplevel"))
    branch = git("branch", "--show-current", cwd=root)
    if branch in ("", "main", "master"):
        raise SystemExit("Ship from a worktree branch, not main. Start one: claude -w <you>-<topic>")
    if git("status", "--porcelain", cwd=root):
        raise SystemExit("You have uncommitted changes. Commit them first, then ship.")

    step("fetch origin")
    git("fetch", "origin", "--quiet", cwd=root)
    ahead, behind = counts(root)
    if ahead == 0:
        raise SystemExit("Nothing to ship: no commits ahead of origin/main.")

    if behind:
        step(f"rebase onto {BASE} ({behind} new commit(s) on main)")
        if args.dry_run:
            print(f"   would run: git rebase {BASE}")
        elif not ok(["git", "rebase", BASE], cwd=root):
            conflicts = git("diff", "--name-only", "--diff-filter=U", cwd=root, check=False)
            run(["git", "rebase", "--abort"], cwd=root, check=False)
            raise SystemExit(f"Conflicts with main in:\n{conflicts}\nRebase aborted, your branch "
                             f"is unchanged. Resolve with `git rebase {BASE}`, then ship again.")

    if not args.no_check:
        step("offline check ($0)")
        if run(["uv", "run", "python", "tests/offline_check.py"], cwd=root, check=False,
               capture=False).returncode != 0:
            raise SystemExit("Offline check failed: not shipping.")

    step("push")
    act(["git", "push", "--force-with-lease", "-u", "origin", "HEAD"], root, args.dry_run)

    if not shutil.which("gh"):
        remote = git("remote", "get-url", "origin", cwd=root)
        slug = re.sub(r"^.*github\.com[:/]|\.git$", "", remote)
        print(f"\nOpen the PR: https://github.com/{slug}/compare/main...{branch}?expand=1")
        return

    step("pull request")
    existing = run(["gh", "pr", "view", "--json", "url", "-q", ".url"], cwd=root, check=False)
    if existing.returncode == 0 and existing.stdout.strip():
        print(f"   updated: {existing.stdout.strip()}")
    else:
        act(["gh", "pr", "create", "--base", "main", "--fill"], root, args.dry_run)
    if args.merge:
        step("squash-merge")
        act(["gh", "pr", "merge", "--squash"], root, args.dry_run)
        print("\nMerged. Teammates: `git pull` in the main checkout. Remove this worktree when you're "
              "done: exit Claude and choose remove, or `python3 scripts/wt.py clean`.")


def merged(branch: str, root: Path) -> bool:
    if shutil.which("gh"):
        out = run(["gh", "pr", "list", "--state", "merged", "--head", branch, "--json", "number",
                   "-q", "length"], cwd=root, check=False).stdout.strip()
        return out not in ("", "0")
    # Without gh: shipped at some point (a remote-tracking branch exists) and fully on main.
    # A fresh worktree that was never pushed is never treated as merged.
    if not ok(["git", "rev-parse", "--verify", "--quiet", f"refs/remotes/origin/{branch}"], cwd=root):
        return False
    return not git("rev-list", f"{BASE}..{branch}", cwd=root, check=False)


def cmd_clean(args: argparse.Namespace) -> None:
    root = main_root()
    git("fetch", "origin", "--quiet", cwd=root, check=False)
    candidates = 0
    for item in worktrees(root):
        path = Path(item["worktree"])
        branch = strip_ref(str(item.get("branch", "")))
        if path.resolve() == root.resolve() or ".claude/worktrees/" not in path.as_posix() + "/":
            continue
        if git("status", "--porcelain", cwd=path, check=False):
            print(f"  keep    {branch}: uncommitted changes")
            continue
        if not branch or not merged(branch, root):
            print(f"  keep    {branch or path.name}: not merged")
            continue
        candidates += 1
        extras = [p for p in ("outputs", ".swarm_state.json", "runs.jsonl") if (path / p).exists()]
        note = f" (deletes its {', '.join(extras)})" if extras else ""
        if args.dry_run:
            print(f"  remove  {branch}{note}  [dry run]")
            continue
        if not args.yes and input(f"  remove  {branch}{note}? [y/N] ").strip().lower() != "y":
            continue
        # Only ignored files (.venv, .env, outputs, state) remain, so --force is safe here.
        act(["git", "worktree", "remove", "--force", str(path)], root, False)
        act(["git", "branch", "-D", branch], root, False)
    if not candidates:
        print("Nothing to clean.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[1],
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    new = sub.add_parser("new", help="create a worktree (like `claude -w <name>`)")
    new.add_argument("name", help="<you>-<topic>, e.g. alex-legal-redlines")
    new.set_defaults(func=cmd_new)
    sub.add_parser("ls", help="list worktrees").set_defaults(func=cmd_ls)
    ship = sub.add_parser("ship", help="rebase, check, push, PR")
    ship.add_argument("--merge", action="store_true", help="squash-merge the PR right away")
    ship.add_argument("--no-check", action="store_true", help="skip the offline check")
    ship.add_argument("--dry-run", action="store_true")
    ship.set_defaults(func=cmd_ship)
    clean = sub.add_parser("clean", help="remove worktrees whose PR was merged")
    clean.add_argument("--yes", action="store_true", help="don't ask for each worktree")
    clean.add_argument("--dry-run", action="store_true")
    clean.set_defaults(func=cmd_clean)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
