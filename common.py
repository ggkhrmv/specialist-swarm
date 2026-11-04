"""
Shared plumbing for the Specialist Swarm scripts.

- Credentials come from ./.env (a value exported in your shell wins), the same
  convention the Basecamp exercises use.
- Profiles pick the models, effort and spend cap: `demo` on main, `dev` (cheaper,
  faster) on every other branch. Override with SWARM_PROFILE=demo|dev.
- The namespace (from the git branch, or SWARM_NAMESPACE) tags everything this
  checkout creates in the cloud, so four people sharing one workspace can tell
  their environments, skills, agents and sessions apart in the Console.
- Every ID a checkout creates lives in its own .swarm_state.json. That file is
  what makes a checkout the OWNER of its cloud resources: never copy it into
  another checkout or worktree, or that copy will update someone else's agents.
  Delete it to start from scratch.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

try:
    import anthropic
    from dotenv import load_dotenv
except ImportError as exc:  # pragma: no cover - environment guard
    raise SystemExit(
        f"'{exc.name}' isn't installed for {sys.executable}.\n"
        "From this folder run:  uv sync   (or: pip install -r requirements.txt)\n"
        "then run scripts with:  uv run python <script>.py"
    )

HERE = Path(__file__).resolve().parent
load_dotenv(HERE / ".env")  # does not override variables already set in the shell


# ── Checkout identity: branch and namespace ──────────────────────────────────

def _git(*args: str) -> str:
    try:
        result = subprocess.run(["git", *args], cwd=HERE, capture_output=True,
                                text=True, timeout=5)
    except (OSError, subprocess.SubprocessError):
        return ""
    return result.stdout.strip() if result.returncode == 0 else ""


BRANCH = _git("branch", "--show-current")  # "" when detached or not a git checkout
NAMESPACE = (os.environ.get("SWARM_NAMESPACE")
             or re.sub(r"[^a-z0-9]+", "-", BRANCH.lower()).strip("-")[:48]
             or "local")


# ── Profiles: models, effort, spend cap ──────────────────────────────────────
# The coordinator plans, delegates and synthesises; specialists do narrow,
# reading-heavy work. `dev` trades quality for speed and cost while you iterate on
# prompts and plumbing; judge output quality on `demo` before merging a prompt change.
# Budgets are in CENTS: "1000" is $10.00 for the whole session, all threads included.
PROFILES = {
    "demo": {
        "coordinator": "claude-opus-5-5",
        "specialist": "claude-sonnet-5-5",
        "fast": "claude-haiku-5-5",
        "effort": {},  # model defaults
        "budget_cents": "1000",
    },
    "dev": {
        "coordinator": "claude-sonnet-5-5",
        "specialist": "claude-haiku-5-5",
        "fast": "claude-haiku-5-5",
        "effort": {"coordinator": "medium", "specialist": "low", "fast": "low"},
        "budget_cents": "300",
    },
}
PROFILE = os.environ.get("SWARM_PROFILE") or ("demo" if BRANCH == "main" else "dev")
if PROFILE not in PROFILES:
    raise SystemExit(f"SWARM_PROFILE must be one of {sorted(PROFILES)}, not {PROFILE!r}.")


def model_for(role: str):
    """The agent `model` for a role ('coordinator' | 'specialist' | 'fast')."""
    profile = PROFILES[PROFILE]
    effort = profile["effort"].get(role)
    return {"id": profile[role], "effort": effort} if effort else profile[role]


def agent_metadata(role: str) -> dict:
    return {"track": "specialist-swarm", "role": role, "namespace": NAMESPACE,
            "profile": PROFILE}


# ── Paths ─────────────────────────────────────────────────────────────────────
# Inside the session container: uploaded files are mounted read-only under
# /mnt/session/uploads/; only files written to /mnt/session/outputs/ can be
# downloaded after the run.
INPUTS_DIR = "/mnt/session/uploads/inputs"
OUTPUTS_DIR = "/mnt/session/outputs"

# Local, per checkout (all gitignored):
STATE_FILE = HERE / ".swarm_state.json"
LOCAL_OUTPUTS = HERE / "outputs"
RUNS_LOG = HERE / "runs.jsonl"
PROMPTS_DIR = HERE / "prompts"


# ── Client ────────────────────────────────────────────────────────────────────

CLIENT_FACTORY = anthropic.Anthropic  # tests/offline_check.py swaps in a fake


def get_client() -> anthropic.Anthropic:
    """A Claude client from your environment / .env.

    Managed Agents is an Anthropic API feature: it does not run on Amazon Bedrock
    or through most company gateways.
    """
    if not (os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN")):
        print("  note: ANTHROPIC_API_KEY isn't set in your shell or .env; "
              "trying other credential sources (e.g. `ant auth login`).")
    return CLIENT_FACTORY()


# ── Prompts ───────────────────────────────────────────────────────────────────

def load_prompt(name: str, **values: str) -> str:
    """prompts/<name>.md, sent verbatim, with its {{placeholders}} filled in."""
    text = (PROMPTS_DIR / f"{name}.md").read_text()
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    unfilled = sorted(set(re.findall(r"\{\{\s*(\w+)\s*\}\}", text)))
    if unfilled:
        raise SystemExit(f"prompts/{name}.md has unfilled placeholder(s): {', '.join(unfilled)}")
    return re.sub(r"\n{3,}", "\n\n", text).strip()  # empty sections leave no gaps


# ── Local state (.swarm_state.json) ──────────────────────────────────────────

def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}


def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")


def require(state: dict, key: str, run_first: str):
    if not state.get(key):
        raise SystemExit(f"Nothing saved for '{key}' in this checkout yet. Run `{run_first}` first.")
    return state[key]


def sha256_of(*paths: Path) -> str:
    """Content hash of one or more files/directories, to tell when they changed."""
    digest = hashlib.sha256()
    for root in paths:
        files = sorted(p for p in root.rglob("*") if p.is_file()) if root.is_dir() else [root]
        for f in files:
            digest.update(str(f.relative_to(root.parent)).encode())
            digest.update(f.read_bytes())
    return digest.hexdigest()


# ── Agent config helpers ─────────────────────────────────────────────────────

def agent_toolset(only: tuple[str, ...] | None = None) -> list[dict]:
    """The prebuilt agent toolset with the `auto` permission policy.

    only=None   -> every tool except the web tools (the coordinator needs bash and
                   write to build the docx; nothing in this exercise needs the web).
    only=(...)  -> just those tools, e.g. ("read", "glob", "grep") for read-only
                   specialists.
    """
    if only:
        return [{
            "type": "agent_toolset_20260401",
            "default_config": {"enabled": False, "permission_policy": {"type": "auto"}},
            "configs": [{"name": name, "enabled": True} for name in only],
        }]
    return [{
        "type": "agent_toolset_20260401",
        "default_config": {"enabled": True, "permission_policy": {"type": "auto"}},
        "configs": [{"name": name, "enabled": False} for name in ("web_fetch", "web_search")],
    }]


# ── CRM MCP (past wins as a remote MCP server, e.g. on Render) ───────────────
# MCP_CRM_URL is the server's /mcp endpoint; MCP_TOKEN is the bearer token (it goes
# into a Vault at run time, never into an agent or this repo). Unset -> no CRM, and
# the Pricing Specialist falls back to the mounted past-wins.json.
CRM_NAME = "crm"


def crm_url() -> str:
    return os.environ.get("MCP_CRM_URL", "").strip()


def crm_mcp() -> dict:
    """Agent fields (`mcp_servers`, extra `tools`) that connect an agent to the CRM MCP.

    Read-only server, so every tool is always_allow (the default policy is always_ask,
    which would pause each call).
    """
    if not crm_url():
        return {"mcp_servers": [], "tools": []}
    return {
        "mcp_servers": [{"type": "url", "name": CRM_NAME, "url": crm_url()}],
        "tools": [{"type": "mcp_toolset", "mcp_server_name": CRM_NAME,
                   "default_config": {"permission_policy": {"type": "always_allow"}}}],
    }


def crm_vault_ids(client: anthropic.Anthropic, state: dict) -> list[str]:
    """Vault holding the CRM bearer token, created once per URL+token (cached in state).

    The token is read from MCP_TOKEN and sent to the API; only a fingerprint of it is
    saved locally. Vault credentials are matched to the agent's server by URL.
    """
    url, token = crm_url(), os.environ.get("MCP_TOKEN", "").strip()
    if not url:
        return []
    if not token:
        raise SystemExit("MCP_CRM_URL is set but MCP_TOKEN isn't. Add MCP_TOKEN to .env "
                         "(the same value as on Render), or unset MCP_CRM_URL.")
    fingerprint = hashlib.sha256(f"{url}\n{token}".encode()).hexdigest()
    saved = state.get("crm_vault")
    if saved and saved.get("fingerprint") == fingerprint:
        return [saved["id"]]
    vault = client.beta.vaults.create(display_name=f"CRM MCP · {NAMESPACE}",
                                      metadata={"track": "specialist-swarm", "namespace": NAMESPACE})
    client.beta.vaults.credentials.create(
        vault_id=vault.id, display_name="CRM MCP bearer token",
        auth={"type": "static_bearer", "mcp_server_url": url, "token": token})
    state["crm_vault"] = {"id": vault.id, "fingerprint": fingerprint}
    save_state(state)
    print(f"  created   CRM vault {vault.id}")
    return [vault.id]


def multiagent_block(agent_ids: list[str], kind: str = "multiagent_20261001") -> dict:
    """The coordinator's roster.

    multiagent_20261001 (current): the coordinator may delegate only to the listed
    agents (no ad-hoc inline agents), and may start a dynamic workflow run over the
    same agents. Its prompt (prompts/coordinator.workflows.md) says when.

    coordinator (older type): fallback for organisations that don't have the newer
    type yet. Delegation only, no workflow runs.
    """
    if kind == "coordinator":
        return {"type": "coordinator",
                "agents": [{"type": "agent", "id": agent_id} for agent_id in agent_ids]}
    return {
        "type": "multiagent_20261001",
        "subagents": {"type": "enabled", "predefined_agents": list(agent_ids),
                      "inline_agents": {"type": "disabled"}},
        "workflows": {"type": "enabled", "predefined_agents": list(agent_ids),
                      "inline_agents": {"type": "disabled"}},
    }


def upsert_agent(client: anthropic.Anthropic, existing_id: str | None, **config):
    """Create the agent, or update it in place if this checkout already made one.

    Agents can't be deleted (only archived), so re-running a setup step updates the
    saved agent instead of piling up duplicates. An update makes a new version
    under the same ID; new sessions use it.
    """
    if existing_id:
        current = client.beta.agents.retrieve(existing_id)
        return client.beta.agents.update(existing_id, version=current.version, **config), "updated"
    return client.beta.agents.create(**config), "created"


# ── Session helpers ──────────────────────────────────────────────────────────

def approve_tool_call(event) -> bool:
    """Decide on a tool call the server paused for review.

    Asks the person at the terminal; when nobody is there (no TTY), denies.
    Never blanket-approve paused calls.
    """
    name = getattr(event, "name", "?")
    if not sys.stdin.isatty():
        print(f"\n  [paused tool call: {name}] no terminal attached, denying", flush=True)
        return False
    preview = json.dumps(getattr(event, "input", {}) or {}, default=str)[:400]
    answer = input(f"\n  [paused tool call: {name}] {preview}\n  Allow? [y/N] ")
    return answer.strip().lower() in ("y", "yes")


def download_outputs(client: anthropic.Anthropic, session_id: str,
                     out_dir: Path | None = None, attempts: int = 4) -> list[Path]:
    """Download every file the session wrote to /mnt/session/outputs/.

    The session's listing also holds the input files we uploaded (the RFP,
    past-wins.json). The API marks those `downloadable=False` and rejects a
    download, so they are skipped. Outputs show up a few seconds after the session
    goes idle, so a listing with no downloadable file is retried a few times
    before giving up.
    """
    out_dir = out_dir or LOCAL_OUTPUTS
    files = []
    for attempt in range(attempts):
        # Listing by scope_id needs the managed-agents beta, which files.list
        # doesn't add on its own.
        listing = client.beta.files.list(scope_id=session_id,
                                         betas=["managed-agents-2026-04-01"]).data
        files = [f for f in listing if f.downloadable is not False]
        if files:
            break
        if attempt < attempts - 1:
            time.sleep(2)

    out_dir.mkdir(exist_ok=True)
    saved = []
    for f in files:
        target = out_dir / Path(f.filename).name
        client.beta.files.download(f.id).write_to_file(str(target))
        print(f"  {f.filename}  ->  {os.path.relpath(target)}")
        saved.append(target)
    return saved


def record_run(entry: dict) -> list[dict]:
    """Append one run to runs.jsonl (local to this checkout) and return the history."""
    with RUNS_LOG.open("a") as fh:
        fh.write(json.dumps(entry, sort_keys=True) + "\n")
    return [json.loads(line) for line in RUNS_LOG.read_text().splitlines() if line.strip()]


def session_url(session_id: str) -> str:
    # Swap 'default' for your workspace ID if your key isn't in the Default workspace.
    return f"https://platform.claude.com/workspaces/default/sessions/{session_id}"
