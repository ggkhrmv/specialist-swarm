"""
Step 5 — run the Deal Desk swarm against the synthetic RFP.

1. Uploads the RFP + supporting files (once; re-uploads only if they change) and
   mounts them read-only in the session container, where the coordinator AND every
   specialist thread can read them.
2. Starts a session against this checkout's coordinator, capped at the budget of the
   profile the agents were set up with (PROFILES in common.py).
3. Streams the events so you can watch the fan-out live. This is the demo: narrate it.
4. Saves the coordinator's transcript, downloads every file the swarm wrote to
   /mnt/session/outputs/ (the proposal docx) into outputs/, and appends the run to
   runs.jsonl, printing the recent history so you can compare iterations.

Ctrl-C interrupts the session so it stops spending, then downloads whatever exists.

Usage:
    uv run python run_deal_desk.py
    DEAL_RFP=~/private/rfp.md uv run python run_deal_desk.py   # another RFP (.md / .txt)

Keep real RFPs outside this repo: it is public. See demo/README.md, "Running it on real data".
"""

import os
import time
from datetime import datetime, timezone
from pathlib import Path

import common
from common import (BRANCH, HERE, crm_vault_ids, INPUTS_DIR, NAMESPACE, OUTPUTS_DIR, PROFILE, PROFILES,
                    approve_tool_call, download_outputs, get_client, load_state, record_run,
                    require, save_state, session_url, sha256_of)

DATA = HERE / "synthetic-data"
RFP = DATA / "rfp-acme-corp.md"
if os.environ.get("DEAL_RFP"):  # run the swarm on another RFP, e.g. real data for a demo
    RFP = Path(os.environ["DEAL_RFP"]).expanduser().resolve()
    if not RFP.is_file():
        raise SystemExit(f"DEAL_RFP: no such file: {RFP}")
    if RFP.suffix.lower() not in (".md", ".txt"):
        raise SystemExit(f"DEAL_RFP must be .md or .txt (got {RFP.suffix}). Convert it first, "
                         "e.g. `pdftotext -layout rfp.pdf rfp.txt` or `pandoc rfp.docx -o rfp.md`.")
INPUT_FILES = [RFP, DATA / "past-wins.json"]  # the capability map is a skill (product-overview)


def upload_inputs(client, state: dict) -> list[dict]:
    """Session resources that mount each input file at INPUTS_DIR/<name>."""
    cache: dict = state.setdefault("input_files", {})
    resources = []
    for path in INPUT_FILES:
        digest = sha256_of(path)
        entry = cache.get(path.name)
        if entry and entry["sha256"] == digest:
            print(f"  reusing   {path.name}")
        else:
            with path.open("rb") as fh:
                uploaded = client.files.upload(file=(path.name, fh, "text/plain"))
            entry = cache[path.name] = {"id": uploaded.id, "sha256": digest}
            save_state(state)
            print(f"  uploaded  {path.name}")
        # mount_path is rooted under /mnt/session/uploads/
        resources.append({"type": "file", "file_id": entry["id"],
                          "mount_path": f"/inputs/{path.name}"})
    return resources


def kickoff_message() -> str:
    return (
        "An RFP has just landed. Run the standard Deal Desk process.\n\n"
        "Files (read-only; every specialist can read these paths too):\n"
        f"- RFP: {INPUTS_DIR}/{RFP.name}\n"
        f"- Past wins, for Pricing: {INPUTS_DIR}/past-wins.json"
        + (" (fallback only: Pricing must query the CRM MCP first)" if common.crm_url() else "")
        + "\n\n"
        f"Deliverable: {OUTPUTS_DIR}/proposal-response.docx\n"
        "Move fast: the RFP deadline is real."
    )


def stream_session(client, session_id: str, transcript: list[str]) -> str:
    """Send the kickoff and print the event stream until the swarm is done.

    Returns why it stopped: "done", "budget_reached", "retries_exhausted",
    "terminated", or "stream closed".
    """
    open_runs: set[str] = set()

    # Open the stream first, then send: the stream only carries events from the
    # moment it opens.
    with client.beta.sessions.events.stream(session_id) as stream:
        client.beta.sessions.events.send(
            session_id,
            events=[{"type": "user.message",
                     "content": [{"type": "text", "text": kickoff_message()}]}],
        )
        for event in stream:
            t = event.type

            # ── The fan-out: this is what to narrate ──
            if t == "session.thread_created":
                print(f"\n  [thread spawned]   {event.agent_name}", flush=True)
            elif t == "session.thread_status_running":
                print(f"  [thread running]   {event.agent_name}", flush=True)
            elif t == "session.thread_status_idle":
                print(f"  [thread idle]      {event.agent_name}", flush=True)
            elif t == "agent.thread_message_sent":
                print(f"  [brief →]          {event.to_agent_name}", flush=True)
            elif t == "agent.thread_message_received":
                print(f"  [report ←]         {event.from_agent_name}", flush=True)

            # ── The coordinator's own work ──
            elif t == "agent.message":
                for block in event.content:
                    if getattr(block, "type", None) == "text":
                        transcript.append(block.text)
                        print(block.text, end="", flush=True)
            elif t in ("agent.tool_use", "agent.mcp_tool_use"):
                print(f"\n  [tool: {event.name}]", flush=True)
                # Under the `auto` policy the server may pause a call for review.
                if getattr(event, "evaluated_permission", None) == "ask":
                    client.beta.sessions.events.send(session_id, events=[{
                        "type": "user.tool_confirmation",
                        "tool_use_id": event.id,
                        "result": "allow" if approve_tool_call(event) else "deny",
                    }])

            # ── Dynamic workflow runs (only if the coordinator starts one) ──
            elif t == "workflow_run.created":
                open_runs.add(event.workflow_run_id)
                print(f"\n  [workflow run]     {event.name}", flush=True)
            elif t == "workflow_run.status_ended":
                open_runs.discard(event.workflow_run_id)
                print(f"\n  [workflow ended]   {event.result.type}", flush=True)

            # ── Errors and the end of the run ──
            elif t == "session.error":
                print(f"\n  [session error] {getattr(event, 'error', event)}", flush=True)
            elif t == "session.status_idle":
                reason = event.stop_reason.type
                if reason == "requires_action":
                    continue  # waiting on a tool confirmation, answered above
                if reason == "end_turn":
                    if open_runs:
                        continue  # a workflow run is still going
                    return "done"
                return reason  # budget_reached / retries_exhausted
            elif t == "session.status_terminated":
                return "terminated"
    return "stream closed"


def print_thread_tools(client, session_id: str) -> None:
    """After the run: what each specialist thread called (the live stream only shows the
    coordinator). MCP calls are marked so you can see the CRM being queried."""
    threads = getattr(client.beta.sessions, "threads", None)
    if threads is None:
        return
    print("\nSPECIALIST TOOL CALLS")
    try:
        for thread in threads.list(session_id).data:
            name = getattr(getattr(thread, "agent", None), "name", None) or thread.id
            calls = []
            for e in threads.events.list(thread.id, session_id=session_id):
                if e.type == "agent.mcp_tool_use":
                    calls.append(f"MCP {getattr(e, 'mcp_server_name', '?')}:{e.name}")
                elif e.type == "agent.tool_use":
                    calls.append(e.name)
            print(f"  {name:28s} {', '.join(calls) or '-'}")
    except Exception as exc:  # display only: never fail a finished run over it
        print(f"  (could not read thread events: {exc})")


def print_history(history: list[dict], last: int = 5) -> None:
    print(f"\nRUN HISTORY (this checkout, last {min(last, len(history))} of {len(history)})")
    print(f"  {'when (UTC)':16s} {'profile':7s} {'outcome':16s} {'cost':>7s} {'time':>6s}  docx")
    for run in history[-last:]:
        cost = f"${run['cost_usd']:.2f}" if run.get("cost_usd") is not None else "?"
        docx = "yes" if any(f.endswith(".docx") for f in run.get("files", [])) else "no"
        print(f"  {run['when'][:16]:16s} {run['profile']:7s} {run['outcome']:16s} "
              f"{cost:>7s} {run['seconds']:>5.0f}s  {docx}")


def main() -> None:
    client = get_client()
    state = load_state()
    environment_id = require(state, "environment_id", "uv run python setup_swarm.py")
    coordinator = require(state, "coordinator", "uv run python setup_swarm.py")

    profile = state.get("profile", PROFILE)  # what the agents were actually set up with
    if profile != PROFILE:
        print(f"  note: this checkout's agents use profile '{profile}' (current: '{PROFILE}'). "
              f"Run `SWARM_PROFILE={PROFILE} uv run python setup_swarm.py` to switch.")
    budget_cents = PROFILES[profile]["budget_cents"]

    print("Preparing input files...")
    resources = upload_inputs(client, state)
    vault_ids = crm_vault_ids(client, state)  # [] unless MCP_CRM_URL is set

    session = client.beta.sessions.create(
        agent=coordinator["id"],
        environment_id=environment_id,
        title=f"Deal Desk: {RFP.stem} · {NAMESPACE}",
        resources=resources,
        **({"vault_ids": vault_ids} if vault_ids else {}),
        budget={"type": "limit", "max_list_cost": {"amount": budget_cents, "currency": "USD"}},
    )
    state["last_session_id"] = session.id
    save_state(state)
    print(f"\nSession {session.id}  (profile {profile}, cap ${int(budget_cents) / 100:.2f})")
    print(f"Full trace, every thread: {session_url(session.id)}")
    print("\n=== EVENT STREAM ===")

    started = time.monotonic()
    transcript: list[str] = []
    try:
        outcome = stream_session(client, session.id, transcript)
    except KeyboardInterrupt:
        print("\n\nInterrupted: stopping every thread so the session stops spending...")
        client.beta.sessions.events.send(session.id, events=[{"type": "user.interrupt"}])
        outcome = "interrupted"
    seconds = time.monotonic() - started

    print(f"\n\n[swarm stopped: {outcome}]")
    if outcome == "budget_reached":
        print(f"  Hit the ${int(budget_cents) / 100:.2f} cap. Raise budget_cents for the "
              f"'{profile}' profile in common.py for the next run.")

    common.LOCAL_OUTPUTS.mkdir(exist_ok=True)
    transcript_path = common.LOCAL_OUTPUTS / "coordinator-transcript.md"
    transcript_path.write_text("".join(transcript))
    print(f"Coordinator transcript: {os.path.relpath(transcript_path)}")

    print("\nDownloading deliverables...")
    files = download_outputs(client, session.id)
    if not files:
        print("  No files found. Open the trace above to see what the coordinator did, or "
              "retry later with: uv run python download_deliverable.py")

    print_thread_tools(client, session.id)

    usage = client.beta.sessions.retrieve(session.id).usage
    cost = int(usage.list_cost.amount) / 100 if usage and usage.list_cost else None
    if cost is not None:
        print(f"\nSession cost (list price): ${cost:.2f}")

    history = record_run({
        "when": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "branch": BRANCH, "namespace": NAMESPACE, "profile": profile,
        "session_id": session.id, "outcome": outcome, "seconds": round(seconds, 1),
        "cost_usd": cost, "files": [f.name for f in files],
    })
    print_history(history)


if __name__ == "__main__":
    main()
