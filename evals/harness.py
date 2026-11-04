"""
Run one eval case against this checkout's real, stored agents (Claude Managed Agents).

- Specialists and the Critic: one session per case against that agent alone, with the
  case's RFP (and files) mounted where the coordinator would put them, and the brief
  the coordinator would send. That tests the agent's real prompt, skills, tools and
  model; nothing is re-implemented.
- Coordinator: the full swarm via run_deal_desk's own upload, kickoff and event loop,
  without the S3 memory store: past deals would leak into the score, and an eval
  run must not write into the team's deal memory.

Paused tool calls are denied (nobody is watching an eval). Every session has a spend
cap and a hard wall-clock ceiling. Failures that aren't the agent's answer (not set
up, timeout, budget, served-model mismatch) raise EvalError with a failure class, so
promptfoo shows them as ERROR, never as a failed answer.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile
import threading
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))

import common  # noqa: E402
import run_deal_desk  # noqa: E402
from common import NAMESPACE, PROFILES, get_client, load_state  # noqa: E402
from create_specialists import SPECIALISTS  # noqa: E402

RUNS = HERE / ".runs"
SPECIALIST_BUDGET_CENTS = "100"  # $1.00 cap per specialist case
ROLE = {**{s["key"]: s["role"] for s in SPECIALISTS}, "critic": "coordinator", "coordinator": "coordinator"}


class EvalError(Exception):
    def __init__(self, failure_class: str, message: str):
        super().__init__(message)
        self.failure_class = failure_class


def _deny(event) -> bool:
    return False


def _write_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(f".{os.getpid()}.tmp")
    tmp.write_text(text)
    tmp.replace(path)


def _file_id(client, name: str, text: str) -> str:
    """Upload once per content; a file per cache entry, so parallel workers never clash."""
    sha = hashlib.sha256(name.encode() + b"\0" + text.encode()).hexdigest()
    cached = RUNS / "files" / f"{sha}.id"
    if cached.exists():
        return cached.read_text().strip()
    file_id = client.files.upload(file=(name, text.encode(), "text/plain")).id
    _write_atomic(cached, file_id)
    return file_id


def _follow(client, session_id: str, message: str, timeout_s: float):
    """run_deal_desk's event loop, with a hard ceiling on total case time."""
    transcript, events, box = [], [], {}
    fan = run_deal_desk.FanOut()

    def work():
        try:
            box["outcome"] = run_deal_desk.stream_session(
                client, session_id, transcript, fan, message, on_event=events.append,
                approve=_deny, echo=False)
        except Exception as error:  # noqa: BLE001 - surfaced below as a harness error
            box["error"] = error

    worker = threading.Thread(target=work, daemon=True)
    worker.start()
    worker.join(timeout_s)
    if worker.is_alive():
        try:
            client.beta.sessions.events.send(session_id, events=[{"type": "user.interrupt"}])
        except Exception:  # noqa: BLE001
            pass
        raise EvalError("timeout", f"no end of turn after {timeout_s:.0f}s (session {session_id})")
    if "error" in box:
        raise EvalError("harness_error", f"{type(box['error']).__name__}: {box['error']}")
    events.append(fan)  # last item: the fan-out timing (run_deal_desk.FanOut)
    return box["outcome"], transcript, events


def _text(blocks) -> str:
    return "".join(getattr(b, "text", "") for b in blocks or [] if getattr(b, "type", None) == "text")


def _finish(case: dict, state: dict, session_id: str, info, outcome: str, started: float) -> dict:
    expected = PROFILES[state.get("profile", common.PROFILE)][ROLE[case["agent"]]]
    served = info.agent.model.id
    if served != expected:
        raise EvalError("served_model_mismatch",
                        f"{case['agent']} runs {served}, but this checkout's profile expects {expected}. "
                        "Re-run `uv run python setup_swarm.py`.")
    if outcome != "done":
        raise EvalError(outcome, f"session {session_id} stopped with {outcome}")
    usage = info.usage
    return {
        "session_id": session_id, "agent_model": served, "agent_version": info.agent.version,
        "latency_s": round(time.monotonic() - started, 1),
        "cost_usd": int(usage.list_cost.amount) / 100 if usage and usage.list_cost else None,
        "input_tokens": getattr(usage, "input_tokens", 0) or 0,
        "output_tokens": getattr(usage, "output_tokens", 0) or 0,
        "trace": common.session_url(session_id),
    }


def run_agent(case: dict, timeout_s: float = 840) -> dict:
    """A specialist or the Critic, alone, on the case's RFP and brief."""
    state = load_state()
    agent_id = (state.get("specialists") or {}).get(case["agent"])
    if not state.get("environment_id") or not agent_id:
        hint = " and `uv run python stretch_critic_subagent.py`" if case["agent"] == "critic" else ""
        raise EvalError("not_set_up", f"no {case['agent']} agent in this checkout: run "
                                      f"`uv run python setup_swarm.py`{hint} first")
    client = get_client()
    files = {"rfp.md": case["rfp"], **case.get("files", {})}
    session = client.beta.sessions.create(
        agent=agent_id, environment_id=state["environment_id"],
        title=f"eval · {case['id']} · {NAMESPACE}",
        resources=[{"type": "file", "file_id": _file_id(client, name, text), "mount_path": f"/inputs/{name}"}
                   for name, text in files.items()],
        budget={"type": "limit", "max_list_cost": {"amount": SPECIALIST_BUDGET_CENTS, "currency": "USD"}},
    )
    started = time.monotonic()
    outcome, transcript, events = _follow(client, session.id, case["brief"], timeout_s)
    run = _finish(case, state, session.id, client.beta.sessions.retrieve(session.id), outcome, started)
    run["text"] = "".join(transcript)
    run["tool_calls"] = sum(getattr(e, "type", None) == "agent.tool_use" for e in events)
    return run


def run_coordinator(case: dict, timeout_s: float = 2280) -> dict:
    """The whole swarm on the Acme RFP, through run_deal_desk's own pieces."""
    if run_deal_desk.RFP.name != "rfp-acme-corp.md":
        raise EvalError("config", "unset DEAL_RFP: the end-to-end eval is scored against the Acme answer key")
    state = load_state()
    if not state.get("environment_id") or not state.get("coordinator"):
        raise EvalError("not_set_up", "no swarm in this checkout: run `uv run python setup_swarm.py` first")
    client = get_client()
    resources = run_deal_desk.upload_inputs(client, state)
    budget = PROFILES[state.get("profile", common.PROFILE)]["budget_cents"]
    session = client.beta.sessions.create(
        agent=state["coordinator"]["id"], environment_id=state["environment_id"],
        title=f"eval · {case['id']} · {NAMESPACE}", resources=resources,
        budget={"type": "limit", "max_list_cost": {"amount": budget, "currency": "USD"}},
    )
    started = time.monotonic()
    outcome, transcript, events = _follow(client, session.id, run_deal_desk.kickoff_message(), timeout_s)
    run = _finish(case, state, session.id, client.beta.sessions.retrieve(session.id), outcome, started)

    from demo import scorecard  # the team's docx reader and 13-trap answer key
    fan = events.pop()
    downloads = common.download_outputs(client, session.id, out_dir=Path(tempfile.mkdtemp(prefix="eval-e2e-")))
    docx = next((f for f in downloads if f.suffix.lower() == ".docx"), None)
    notes = next((f for f in downloads if f.name == "internal-deal-notes.md"), None)
    run.update({
        # The scorecard reads the proposal plus the internal deal notes; so do the traps.
        "text": "\n".join(scorecard.read_text(f) for f in (docx, notes) if f),
        "docx_path": str(docx) if docx else None,
        "files": [f.name for f in downloads],
        "summary": "".join(transcript)[-3000:],
        "expected_specialists": [s["name"] for s in SPECIALISTS],
        "briefs": [{"to": e.to_agent_name, "text": _text(e.content)[:4000], "at": i}
                   for i, e in enumerate(events) if e.type == "agent.thread_message_sent"],
        "reports": [{"from": e.from_agent_name, "at": i}
                    for i, e in enumerate(events) if e.type == "agent.thread_message_received"],
        "tool_calls": sum(e.type == "agent.tool_use" for e in events),
        **fan.record(),
    })
    return run


def run(case: dict) -> dict:
    return run_coordinator(case) if case["flow"] == "coordinator" else run_agent(case)


# ── Saved runs: EVAL_MODE=reuse re-grades these without running agents ───────

def save_run(case: dict, rep: int, run: dict) -> None:
    _write_atomic(RUNS / f"{case['id']}_rep{rep}.json", json.dumps(run, indent=2, default=str))


def load_run(case: dict, rep: int) -> dict:
    path = RUNS / f"{case['id']}_rep{rep}.json"
    if not path.exists():
        raise EvalError("no_saved_run", f"no saved run for {case['id']} rep {rep}: run it live first")
    return json.loads(path.read_text())
