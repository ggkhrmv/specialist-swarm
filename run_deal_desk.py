"""
Step 5 — run the Deal Desk swarm against the synthetic RFP.

1. Uploads the RFP + supporting files (once; re-uploads only if they change) and
   mounts them read-only in the session container, where the coordinator AND every
   specialist thread can read them.
2. Starts a session against this checkout's coordinator, capped at the budget of the
   profile the agents were set up with (PROFILES in common.py).
3. Streams the events so you can watch the fan-out live. This is the demo: narrate it.
4. Saves the coordinator's transcript, downloads every file the swarm wrote to
   /mnt/session/outputs/ (the proposal docx and the pitch deck) into outputs/, and appends the run to
   runs.jsonl, printing the recent history so you can compare iterations.

If you've run stretch_memory.py (stretch S3), this checkout's memory store is attached
as well, read-write: the coordinator reads past deals before it briefs and records
this one after it delivers.

Ctrl-C interrupts the session so it stops spending, then downloads whatever exists.

Usage:
    uv run python run_deal_desk.py                       # the Acme Corp RFP
    uv run python run_deal_desk.py --rfp synthetic-data/rfp-kestrel-logistics.md
    uv run python run_deal_desk.py --no-memory           # don't attach the memory store
    DEAL_RFP=~/private/rfp.md uv run python run_deal_desk.py   # default RFP (.md / .txt)

--rfp wins over DEAL_RFP. Keep real RFPs outside this repo: it is public. See
demo/README.md, "Running it on real data".
"""

import argparse
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import common
from common import (BRANCH, HERE, INPUTS_DIR, NAMESPACE, OUTPUTS_DIR, PROFILE, PROFILES,
                    approve_tool_call, download_outputs, get_client, load_state, record_run,
                    require, save_state, session_url, sha256_of)
from stretch_memory import memory_resource

DATA = HERE / "synthetic-data"
def checked_rfp(path: Path, source: str) -> Path:
    path = path.expanduser().resolve()
    if not path.is_file():
        raise SystemExit(f"{source}: no such file: {path}")
    if path.suffix.lower() not in (".md", ".txt"):
        raise SystemExit(f"{source} must be .md or .txt (got {path.suffix}). Convert it first, "
                         "e.g. `pdftotext -layout rfp.pdf rfp.txt` or `pandoc rfp.docx -o rfp.md`.")
    return path


RFP = DATA / "rfp-acme-corp.md"  # the default deal; DEAL_RFP or --rfp picks another
if os.environ.get("DEAL_RFP"):  # run the swarm on another RFP, e.g. real data for a demo
    RFP = checked_rfp(Path(os.environ["DEAL_RFP"]), "DEAL_RFP")
PAST_WINS = DATA / "past-wins.json"  # the capability map is a skill (product-overview)


def input_files(rfp: Path = RFP) -> list[Path]:
    return [rfp, PAST_WINS]


def upload_inputs(client, state: dict, rfp: Path = RFP) -> list[dict]:
    """Session resources that mount each input file at INPUTS_DIR/<name>."""
    cache: dict = state.setdefault("input_files", {})
    resources = []
    for path in input_files(rfp):
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


def kickoff_message(rfp: Path = RFP, memory: bool = False) -> str:
    memory_line = ("Your deal memory is attached (see the memory section of your "
                   "instructions): read it before you brief, and update it once the docx "
                   "is saved.\n\n") if memory else ""
    return (
        "An RFP has just landed. Run the standard Deal Desk process.\n\n"
        "Files (read-only; every specialist can read these paths too):\n"
        f"- RFP: {INPUTS_DIR}/{rfp.name}\n"
        f"- Past wins, for Pricing: {INPUTS_DIR}/{PAST_WINS.name}\n\n"
        f"{memory_line}"
        f"Deliverables: {OUTPUTS_DIR}/proposal-response.docx and {OUTPUTS_DIR}/pitch-deck.html\n"
        "Move fast: the RFP deadline is real."
    )


class FanOut:
    """Times the fan-out so the parallelism is visible on screen (stretch S4).

    The fan-out is every specialist briefed before the first report comes back.
    Briefs sent after that (follow-ups, the Critic) are timed but not counted in it.
    """

    def __init__(self) -> None:
        self.started = time.monotonic()
        self.briefed: dict[str, float] = {}   # agent -> seconds since kickoff, first brief
        self.reported: dict[str, float] = {}  # agent -> seconds since kickoff, first report
        self.fanout: list[str] = []

    def now(self) -> float:
        return time.monotonic() - self.started

    def brief(self, agent: str) -> str:
        t = self.now()
        self.briefed.setdefault(agent, t)
        if not self.reported and agent not in self.fanout:
            self.fanout.append(agent)
        return self.stamp(t)

    @staticmethod
    def stamp(t: float) -> str:
        return f"{f'+{t:.1f}s':>7s}"

    def report(self, agent: str) -> str:
        t = self.now()
        summary = ""
        if not self.reported and len(self.fanout) > 1:
            summary = (f"  [fan-out]          {len(self.fanout)} specialists briefed within "
                       f"{self.spread():.1f}s, all working in parallel\n")
        elif not self.reported:
            summary = ("  [fan-out]          NOT PARALLEL: a report came back before a second "
                       "specialist was briefed\n")
        self.reported.setdefault(agent, t)
        took = f" ({t - self.briefed[agent]:.0f}s after its brief)" if agent in self.briefed else ""
        return f"{summary}  [report ←] {self.stamp(t)} {agent}{took}"

    def spread(self) -> float:
        times = [self.briefed[a] for a in self.fanout]
        return max(times) - min(times) if times else 0.0

    def fan_in_line(self) -> str | None:
        """After the run: wall time of the fan-out vs. the work done in it."""
        done = [a for a in self.fanout if a in self.reported]
        if not done:
            return None
        wall = max(self.reported[a] for a in done) - min(self.briefed[a] for a in done)
        work = sum(self.reported[a] - self.briefed[a] for a in done)
        return (f"  [fan-in]           {len(done)} reports in {wall:.0f}s of wall time "
                f"for {work:.0f}s of specialist work")

    def record(self) -> dict:
        return {"fanout_agents": len(self.fanout), "fanout_spread_s": round(self.spread(), 1)}


def stream_session(client, session_id: str, transcript: list[str], fan: FanOut,
                   kickoff: str, *, on_event=None, approve=approve_tool_call,
                   echo: bool = True) -> str:
    """Send the kickoff and print the event stream until the swarm is done.

    `on_event` sees every event (the evals record them), `approve` decides tool calls
    the server paused for review (the evals deny them all), and `echo=False` keeps it
    quiet. Returns why it stopped: "done", "budget_reached", "retries_exhausted",
    "terminated", or "stream closed".
    """
    say = print if echo else (lambda *a, **k: None)
    open_runs: set[str] = set()

    # Open the stream first, then send: the stream only carries events from the
    # moment it opens.
    with client.beta.sessions.events.stream(session_id) as stream:
        client.beta.sessions.events.send(
            session_id,
            events=[{"type": "user.message",
                     "content": [{"type": "text", "text": kickoff}]}],
        )
        for event in stream:
            t = event.type
            if on_event:
                on_event(event)

            # ── The fan-out: this is what to narrate ──
            if t == "session.thread_created":
                say(f"\n  [thread spawned]   {event.agent_name}", flush=True)
            elif t == "session.thread_status_running":
                say(f"  [thread running]   {event.agent_name}", flush=True)
            elif t == "session.thread_status_idle":
                say(f"  [thread idle]      {event.agent_name}", flush=True)
            elif t == "agent.thread_message_sent":
                say(f"  [brief →]  {fan.brief(event.to_agent_name)} {event.to_agent_name}",
                      flush=True)
            elif t == "agent.thread_message_received":
                say(fan.report(event.from_agent_name), flush=True)

            # ── The coordinator's own work ──
            elif t == "agent.message":
                for block in event.content:
                    if getattr(block, "type", None) == "text":
                        transcript.append(block.text)
                        # End the line so the next [tag] doesn't run into the text.
                        say(block.text, end="" if block.text.endswith("\n") else "\n",
                              flush=True)
            elif t in ("agent.tool_use", "agent.mcp_tool_use"):
                say(f"\n  [tool: {event.name}]", flush=True)
                # Under the `auto` policy the server may pause a call for review.
                if getattr(event, "evaluated_permission", None) == "ask":
                    client.beta.sessions.events.send(session_id, events=[{
                        "type": "user.tool_confirmation",
                        "tool_use_id": event.id,
                        "result": "allow" if approve(event) else "deny",
                    }])

            # ── Dynamic workflow runs (only if the coordinator starts one) ──
            elif t == "workflow_run.created":
                open_runs.add(event.workflow_run_id)
                say(f"\n  [workflow run]     {event.name}", flush=True)
            elif t == "workflow_run.status_ended":
                open_runs.discard(event.workflow_run_id)
                say(f"\n  [workflow ended]   {event.result.type}", flush=True)

            # ── Errors and the end of the run ──
            elif t == "session.error":
                say(f"\n  [session error] {getattr(event, 'error', event)}", flush=True)
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


def print_history(history: list[dict], last: int = 5) -> None:
    print(f"\nRUN HISTORY (this checkout, last {min(last, len(history))} of {len(history)})")
    print(f"  {'when (UTC)':16s} {'profile':7s} {'outcome':16s} {'cost':>7s} {'time':>6s}  "
          f"{'fan-out':>11s}  docx  deck  memory  rfp")
    for run in history[-last:]:
        cost = f"${run['cost_usd']:.2f}" if run.get("cost_usd") is not None else "?"
        docx = "yes" if any(f.endswith(".docx") for f in run.get("files", [])) else "no"
        deck = "yes" if any(f.endswith("pitch-deck.html") for f in run.get("files", [])) else "no"
        fanout = (f"{run['fanout_agents']} in {run['fanout_spread_s']:.0f}s"
                  if "fanout_agents" in run else "?")
        memory = "yes" if run.get("memory") else "no"
        print(f"  {run['when'][:16]:16s} {run['profile']:7s} {run['outcome']:16s} "
              f"{cost:>7s} {run['seconds']:>5.0f}s  {fanout:>11s}  {docx:4s}  {deck:4s}  {memory:6s}  "
              f"{run.get('rfp', '?')}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Deal Desk swarm against one RFP.")
    parser.add_argument("--rfp", type=Path, default=RFP,
                        help=f"the RFP, .md or .txt (default: {os.path.relpath(RFP)}, "
                             "or $DEAL_RFP if set)")
    parser.add_argument("--no-memory", action="store_true",
                        help="don't attach the memory store, even if stretch_memory.py made one")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv or [])
    rfp = checked_rfp(args.rfp, "--rfp")
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
    resources = upload_inputs(client, state, rfp)
    memory = None if args.no_memory else memory_resource(state)
    if memory:
        resources.append(memory)
        print(f"  attached  memory store {memory['memory_store_id']} (read-write)")

    session = client.beta.sessions.create(
        agent=coordinator["id"],
        environment_id=environment_id,
        title=f"Deal Desk: {rfp.stem} · {NAMESPACE}",
        resources=resources,
        budget={"type": "limit", "max_list_cost": {"amount": budget_cents, "currency": "USD"}},
    )
    state["last_session_id"] = session.id
    save_state(state)
    print(f"\nSession {session.id}  (profile {profile}, cap ${int(budget_cents) / 100:.2f})")
    print(f"Full trace, every thread: {session_url(session.id)}")
    print("\n=== EVENT STREAM ===")

    started = time.monotonic()
    transcript: list[str] = []
    fan = FanOut()
    try:
        outcome = stream_session(client, session.id, transcript, fan,
                                 kickoff_message(rfp, memory=bool(memory)))
    except KeyboardInterrupt:
        print("\n\nInterrupted: stopping every thread so the session stops spending...")
        client.beta.sessions.events.send(session.id, events=[{"type": "user.interrupt"}])
        outcome = "interrupted"
    seconds = time.monotonic() - started

    print(f"\n\n[swarm stopped: {outcome}]")
    if fan_in := fan.fan_in_line():
        print(fan_in)
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

    usage = client.beta.sessions.retrieve(session.id).usage
    cost = int(usage.list_cost.amount) / 100 if usage and usage.list_cost else None
    if cost is not None:
        print(f"\nSession cost (list price): ${cost:.2f}")

    history = record_run({
        "when": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "branch": BRANCH, "namespace": NAMESPACE, "profile": profile,
        "session_id": session.id, "outcome": outcome, "seconds": round(seconds, 1),
        "cost_usd": cost, "files": [f.name for f in files], **fan.record(),
        "rfp": rfp.name, "memory": bool(memory),
    })
    print_history(history)


if __name__ == "__main__":
    main(sys.argv[1:])
