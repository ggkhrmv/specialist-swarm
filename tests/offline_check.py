"""
Offline check: runs the whole pipeline against a fake client. $0, a few seconds, no
network. Run it before every push (CI runs it on every PR):

    uv run python tests/offline_check.py        # -v prints every script's output

What it covers:
- setup_swarm (first run creates, second run updates: no duplicates),
- run_deal_desk against a scripted event stream (fan-out, a paused tool call that
  gets denied, early stop at end_turn, downloads, runs.jsonl history),
- the memory stretch (one store, attached read-write to later sessions with its
  instructions, --rfp / --no-memory, outcomes created then replaced),
- the critic stretch (roster grows, prompt gains the critic section),
- the fallback to the older `coordinator` multiagent type,
- the deal-deck skill: its example builds through its own gates, and bad slides fail,
- every request's arguments checked against the installed anthropic SDK's type
  hints, so API drift (renamed fields, wrong shapes) fails here instead of costing
  a real run.

It never touches this checkout's .swarm_state.json, outputs/ or runs.jsonl.
"""

from __future__ import annotations

import inspect
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import traceback
import types
import typing
from contextlib import redirect_stdout
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
os.environ["SWARM_NAMESPACE"] = "offline-check"  # deterministic, whatever the branch
os.environ["SWARM_PROFILE"] = "dev"

import anthropic  # noqa: E402
import httpx2  # noqa: E402
from anthropic.resources.beta.agents.agents import Agents  # noqa: E402
from anthropic.resources.beta.environments.environments import Environments  # noqa: E402
from anthropic.resources.beta.memory_stores.memories import Memories  # noqa: E402
from anthropic.resources.beta.memory_stores.memory_stores import MemoryStores  # noqa: E402
from anthropic.resources.beta.sessions.events import Events  # noqa: E402
from anthropic.resources.beta.sessions.sessions import Sessions  # noqa: E402
from anthropic.resources.beta.vaults.credentials import Credentials  # noqa: E402
from anthropic.resources.beta.vaults.vaults import Vaults  # noqa: E402
from anthropic.resources.files import Files  # noqa: E402
from anthropic.resources.messages.messages import Messages  # noqa: E402
from anthropic.resources.skills.skills import Skills  # noqa: E402
from anthropic.resources.skills.versions import Versions  # noqa: E402
from typing_extensions import is_typeddict  # noqa: E402

import common  # noqa: E402

VERBOSE = "-v" in sys.argv
PROBLEMS: list[str] = []


# ── Request validation against the SDK's type hints ──────────────────────────

def _check(value, hint, where: str) -> bool:
    origin, args = typing.get_origin(hint), typing.get_args(hint)
    if hint is typing.Any or hint is object:
        return True
    if origin is typing.Union or isinstance(hint, types.UnionType):
        return any(_quiet(value, member, where) for member in args)
    if origin is typing.Literal:
        return value in args
    if hint is type(None):
        return value is None
    if origin is typing.Annotated:
        return _check(value, args[0], where)
    if is_typeddict(hint):
        if not isinstance(value, dict):
            return False
        hints = typing.get_type_hints(hint)
        extra = set(value) - set(hints)
        if extra:
            PROBLEMS.append(f"{where}: unknown keys {sorted(extra)} for {hint.__name__}")
            return False
        missing = set(getattr(hint, "__required_keys__", set())) - set(value)
        if missing:
            PROBLEMS.append(f"{where}: missing required {sorted(missing)} for {hint.__name__}")
            return False
        return all(_check(value[k], hints[k], f"{where}.{k}") for k in value)
    if origin in (list, tuple, set) or getattr(origin, "__name__", "") in (
            "Iterable", "Sequence", "SequenceNotStr"):
        if isinstance(value, (str, bytes, dict)):
            return False
        return all(_check(v, args[0] if args else typing.Any, f"{where}[]") for v in value)
    if origin is dict:
        return isinstance(value, dict)
    if isinstance(hint, type):
        if hint.__name__ in ("Omit", "NotGiven"):
            return False
        try:
            return isinstance(value, hint)
        except TypeError:
            return True
    return True  # FileTypes and other aliases: don't second-guess


def _quiet(value, hint, where: str) -> bool:
    before = len(PROBLEMS)
    ok = _check(value, hint, where)
    if not ok:
        del PROBLEMS[before:]
    return ok


def validate(method, kwargs: dict, label: str) -> bool:
    hints = typing.get_type_hints(method)
    params = inspect.signature(method).parameters
    ok = True
    for key, value in kwargs.items():
        if key not in params:
            PROBLEMS.append(f"{label}: unexpected argument '{key}'")
            ok = False
        elif key in hints and not _check(value, hints[key], f"{label}({key})"):
            PROBLEMS.append(f"{label}: '{key}' doesn't match the SDK type {hints[key]}")
            ok = False
    return ok


# ── Fake client ───────────────────────────────────────────────────────────────

class Obj(types.SimpleNamespace):
    pass


def bad_request(message: str) -> anthropic.BadRequestError:
    request = httpx2.Request("POST", "https://api.anthropic.com/v1/agents")
    return anthropic.BadRequestError(message, response=httpx2.Response(400, request=request),
                                     body=None)


class FakeClient:
    """Just enough of anthropic.Anthropic for these scripts; validates every call."""

    def __init__(self, events=(), reject_new_multiagent=False, served_model="claude-haiku-5-5"):
        self.calls: list[tuple] = []
        self.sent: list[dict] = []
        self.agents_db: dict[str, Obj] = {}
        self.judge_readout: dict = {}  # what the fake judge (messages.create) returns
        fake = self

        class _Agents:
            def create(self, **kw):
                validate(Agents.create, kw, "agents.create")
                fake.calls.append(("agents.create", kw))
                if reject_new_multiagent and (kw.get("multiagent") or {}).get("type") == "multiagent_20261001":
                    raise bad_request("multiagent: Extra inputs are not permitted")
                agent_id = f"agent_{len(fake.agents_db) + 1}"
                fake.agents_db[agent_id] = Obj(id=agent_id, version=1, name=kw["name"],
                                               description=kw.get("description"))
                return fake.agents_db[agent_id]

            def retrieve(self, agent_id, **kw):
                return fake.agents_db[agent_id]

            def update(self, agent_id, **kw):
                validate(Agents.update, {"agent_id": agent_id, **kw}, "agents.update")
                fake.calls.append(("agents.update", kw))
                agent = fake.agents_db[agent_id]
                agent.version += 1
                agent.name = kw.get("name", agent.name)
                agent.description = kw.get("description", agent.description)
                return agent

        class _Environments:
            def create(self, **kw):
                validate(Environments.create, kw, "environments.create")
                fake.calls.append(("environments.create", kw))
                return Obj(id="env_1")

        class _Versions:
            def create(self, skill_id, **kw):
                validate(Versions.create, {"skill_id": skill_id, **kw}, "skills.versions.create")
                fake.calls.append(("skills.versions.create", skill_id))

        class _Skills:
            versions = _Versions()

            def create(self, **kw):
                validate(Skills.create, kw, "skills.create")
                names = [f[0] for f in kw["files"]]
                assert all("/" in n for n in names), f"skill files need a top-level dir: {names}"
                fake.calls.append(("skills.create", kw))
                return Obj(id=f"skill_{len(fake.calls)}")

        class _Files:
            def upload(self, **kw):
                validate(Files.upload, kw, "files.upload")
                fake.calls.append(("files.upload", kw["file"][0]))
                return Obj(id=f"file_{kw['file'][0]}")

        class _BetaFiles:
            def list(self, **kw):
                fake.calls.append(("beta.files.list", kw))
                # Like the real listing: our uploaded inputs come back too, and the
                # API refuses to download them.
                return Obj(data=[
                    Obj(id="file_in", filename="rfp-acme-corp.md", downloadable=False),
                    Obj(id="file_out", filename="proposal-response.docx", downloadable=True),
                    Obj(id="file_deck", filename="pitch-deck.html", downloadable=True),
                ])

            def download(self, file_id):
                assert file_id != "file_in", "downloaded an input file (API returns 400)"
                return Obj(write_to_file=lambda path: Path(path).write_bytes(b"PK fake docx"))

        class _Stream:
            def __enter__(self):
                return iter(events)

            def __exit__(self, *exc):
                return False

        class _Events:
            def stream(self, session_id, **kw):
                return _Stream()

            def send(self, session_id, **kw):
                validate(Events.send, {"session_id": session_id, **kw}, "sessions.events.send")
                fake.sent.extend(kw["events"])

        class _Sessions:
            events = _Events()

            def create(self, **kw):
                validate(Sessions.create, kw, "sessions.create")
                fake.calls.append(("sessions.create", kw))
                return Obj(id="sesn_1")

            def retrieve(self, session_id, **kw):
                return Obj(usage=Obj(list_cost=Obj(amount="123", currency="USD"),
                                     input_tokens=900, output_tokens=300),
                           agent=Obj(model=Obj(id=served_model), version=3))

        class _Messages:  # the eval judge
            def create(self, **kw):
                validate(Messages.create, kw, "messages.create")
                fake.calls.append(("messages.create", kw))
                return Obj(model=kw["model"], stop_reason="end_turn",
                           content=[Obj(type="text", text=json.dumps(fake.judge_readout))],
                           usage=Obj(input_tokens=1000, output_tokens=200))

        self.memories_db: dict[str, Obj] = {}

        class _Memories:
            def list(self, memory_store_id, **kw):
                validate(Memories.list, {"memory_store_id": memory_store_id, **kw},
                         "memory_stores.memories.list")
                prefix = kw.get("path_prefix", "/")
                # The API's rule: a prefix is a directory, "/" or "/a/b/", never a file.
                if not re.fullmatch(r"(/([^/\x00]+/)*)?", prefix):
                    raise bad_request("path_prefix: does not match regex pattern "
                                      "`^(/([^/\\x00]+/)*)?$`")
                return [m for m in fake.memories_db.values() if m.path.startswith(prefix)]

            def create(self, memory_store_id, **kw):
                validate(Memories.create, {"memory_store_id": memory_store_id, **kw},
                         "memory_stores.memories.create")
                fake.calls.append(("memories.create", kw))
                memory_id = f"mem_{len(fake.memories_db) + 1}"
                fake.memories_db[memory_id] = Obj(
                    type="memory", id=memory_id, path=kw["path"], content=kw["content"],
                    content_size_bytes=len(kw["content"].encode()),
                    updated_at=datetime(2026, 11, 4, 12, 0))
                return fake.memories_db[memory_id]

            def update(self, memory_id, **kw):
                validate(Memories.update, {"memory_id": memory_id, **kw},
                         "memory_stores.memories.update")
                fake.calls.append(("memories.update", kw))
                fake.memories_db[memory_id].content = kw["content"]
                return fake.memories_db[memory_id]

        class _MemoryStores:
            memories = _Memories()

            def create(self, **kw):
                validate(MemoryStores.create, kw, "memory_stores.create")
                fake.calls.append(("memory_stores.create", kw))
                return Obj(id="memstore_1")

        class _Credentials:
            def create(self, vault_id, **kw):
                validate(Credentials.create, {"vault_id": vault_id, **kw}, "vaults.credentials.create")
                fake.calls.append(("vaults.credentials.create", {"vault_id": vault_id, **kw}))
                return Obj(id="vcrd_1")

        class _Vaults:
            credentials = _Credentials()

            def create(self, **kw):
                validate(Vaults.create, kw, "vaults.create")
                fake.calls.append(("vaults.create", kw))
                return Obj(id="vlt_1")

        self.beta = Obj(agents=_Agents(), environments=_Environments(), sessions=_Sessions(),
                        files=_BetaFiles(), memory_stores=_MemoryStores(), vaults=_Vaults())
        self.skills = _Skills()
        self.files = _Files()
        self.messages = _Messages()

    def of(self, name: str) -> list:
        return [call for call in self.calls if call[0] == name]


def event(type_: str, **fields) -> Obj:
    return Obj(type=type_, **fields)


# ── Scenarios ─────────────────────────────────────────────────────────────────

def step(label: str, fn) -> None:
    buffer = io.StringIO()
    try:
        with redirect_stdout(buffer):
            fn()
    except BaseException:
        print(f"FAIL  {label}\n{buffer.getvalue()}")
        raise
    print(f"ok    {label}")
    if VERBOSE:
        print("      " + buffer.getvalue().rstrip().replace("\n", "\n      "))


def check_evals(tmp: Path, swarm: FakeClient) -> None:
    """evals/: every case's reference answer passes its checks and an empty one fails;
    the judge call and the eval session match the SDK's types; reuse re-grades from
    the readout cache; infra problems come back as promptfoo errors, not failures."""
    sys.path.insert(0, str(REPO / "evals"))
    import cases as eval_cases
    import grading
    import harness
    import oracles
    import provider
    grading.CACHE, harness.RUNS = tmp / "eval-extract", tmp / "eval-runs"

    def strict(schema: dict, where: str) -> None:  # what structured outputs requires
        if schema.get("type") == "object":
            assert schema.get("additionalProperties") is False, f"{where}: additionalProperties must be false"
            assert schema.get("required") == list(schema["properties"]), f"{where}: all properties required"
            for key, sub in schema["properties"].items():
                strict(sub, f"{where}.{key}")
        if schema.get("type") == "array":
            strict(schema["items"], f"{where}[]")

    for case in eval_cases.ALL:
        strict(grading.schema_for(case), case["id"])
        ref, gold, blank, empty = oracles.run(case), grading.gold(case), grading.blank(case), oracles.empty_run(case)
        assert set(gold) == set(grading.schema_for(case)["properties"]), f"{case['id']}: gold field outside schema"
        assert ("substantive", {}) in case["checks"], f"{case['id']}: every case needs `substantive`"
        for name, params in case["checks"]:
            assert name in grading.CHECKS, f"{case['id']}: unknown check {name}"
            ok, reason = grading.run_check(name, gold, ref["text"], ref, params)
            assert ok, f"{case['id']} {name}: the reference answer fails ({reason})"
        assert not grading.run_check("substantive", blank, "", empty, {})[0]
    tests = eval_cases.create_tests({"flows": ["pricing", "legal", "technical_fit", "competitive", "coordinator"]})
    assert tests and all(t["assert"] and t["vars"]["case_id"] in eval_cases.BY_ID for t in tests)

    def ask(case_id: str, mode: str) -> dict:
        os.environ["EVAL_MODE"] = mode
        try:
            return provider.answer({"vars": {"case_id": case_id}, "repeatIndex": 0})
        finally:
            os.environ.pop("EVAL_MODE", None)

    assert ask("pricing-acme", "fake-oracle")["metadata"]["extraction"]["tier"] == "Enterprise"
    assert ask("legal-acme", "fake-null")["metadata"]["extraction"]["substantive"] is False
    assert ask("critic-clean-draft", "live")["error"].startswith("[not_set_up]"), "no Critic in this swarm"

    # A live specialist case through the fake sessions API and the fake judge.
    case = eval_cases.BY_ID["pricing-acme"]
    answer_events = [event("agent.message", content=[Obj(type="text", text=oracles.run(case)["text"])]),
                     event("session.status_idle", stop_reason=Obj(type="end_turn"))]
    client = FakeClient(events=answer_events)
    client.judge_readout = grading.gold(case)
    use(client, tmp, "fallback")  # the swarm set up in step 4
    result = ask("pricing-acme", "live")
    assert "error" not in result, result
    session = client.of("sessions.create")[-1][1]
    assert {r["mount_path"] for r in session["resources"]} == {"/inputs/rfp.md", "/inputs/past-wins.json"}
    assert session["budget"]["max_list_cost"]["amount"] == harness.SPECIALIST_BUDGET_CENTS
    judge = client.of("messages.create")
    assert len(judge) == 1 and judge[0][1]["model"] != "claude-haiku-5-5", "judge must differ from the agent"
    for name, params in case["checks"]:
        ok, reason = grading.run_check(name, result["metadata"]["extraction"], result["output"],
                                       result["metadata"]["run"], params)
        assert ok, f"live path {name}: {reason}"
    again = ask("pricing-acme", "reuse")  # saved run + cached readout: no agent, no judge call
    assert len(client.of("messages.create")) == 1 and again["metadata"]["judge"].get("cached")

    wrong = FakeClient(events=answer_events, served_model="claude-opus-5-5")
    use(wrong, tmp, "fallback")
    assert ask("pricing-acme", "live")["error"].startswith("[served_model_mismatch]")


def use(client: FakeClient, tmp: Path, tag: str) -> None:
    common.CLIENT_FACTORY = lambda: client
    common.STATE_FILE = tmp / f"state-{tag}.json"
    common.LOCAL_OUTPUTS = tmp / f"outputs-{tag}"
    common.RUNS_LOG = tmp / f"runs-{tag}.jsonl"


def check_deal_deck(tmp: Path) -> None:
    """Build the skill's example with its own script, as the coordinator would."""
    skill = REPO / "skills" / "deal-deck"
    script = skill / "scripts" / "build_deck.py"

    def build(slides: Path, out: Path) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, "-I", str(script), str(slides), str(out),
                               "--title", "Offline check", "--context", "Offline check"],
                              capture_output=True, text=True, timeout=60)

    out = tmp / "deck" / "pitch-deck.html"
    result = build(skill / "examples" / "example-slides.html", out)
    print(result.stdout + result.stderr)
    assert result.returncode == 0 and "deck OK" in result.stdout, "example deck failed its gates"
    built = out.read_text()
    assert "{{" not in built and built.count("@font-face") == 7
    assert "https://" not in built and "http://" not in built, "deck is not self-contained"

    # The gates must bite: a raw colour and a missing slide both fail the build.
    bad = tmp / "deck" / "bad-slides.html"
    bad.write_text('<section class="slide"><h2 class="title" style="color:#ff0000">x</h2></section>')
    result = build(bad, tmp / "deck" / "bad.html")
    assert result.returncode == 1 and "raw hex colour" in result.stdout and "expected 5" in result.stdout, \
        result.stdout


def main() -> None:
    sys.stdin = io.StringIO()  # no TTY: paused tool calls must be denied
    tmp = Path(tempfile.mkdtemp(prefix="swarm-offline-"))

    import create_specialists
    import record_outcome
    import run_deal_desk
    import setup_swarm
    import stretch_critic_subagent
    import stretch_memory

    n_specialists = len(create_specialists.SPECIALISTS)
    names = [s["name"] for s in create_specialists.SPECIALISTS]

    # 0. The validator itself must catch a bad request, or every check below is vacuous.
    assert not validate(Agents.create, {"name": "x", "model": "m", "display_title": "x"}, "self-test")
    assert not validate(Sessions.create, {"agent": "a", "environment_id": "e", "budget": {
        "type": "limit", "max_list_cost": {"amount": 10, "currency": "USD"}}}, "self-test")
    PROBLEMS.clear()
    print("ok    validator self-test (catches unknown args and wrong types)")

    # 1. Setup twice: the second run must update in place, never duplicate.
    events = (
        [event("session.thread_created", agent_name=n) for n in names]
        + [event("agent.thread_message_sent", to_agent_name=n) for n in names]
        + [event("agent.tool_use", id="sevt_1", name="bash", input={"command": "ls"},
                 evaluated_permission="ask"),
           event("session.status_idle", stop_reason=Obj(type="requires_action"))]
        + [event("agent.thread_message_received", from_agent_name=n) for n in names]
        + [event("agent.message", content=[Obj(type="text", text="Proposal saved.")]),
           event("session.status_idle", stop_reason=Obj(type="end_turn")),
           event("agent.message", content=[Obj(type="text", text="NOT READ: after end_turn")])]
    )
    fake = FakeClient(events=events)
    use(fake, tmp, "main")
    step("setup_swarm (first run creates)", setup_swarm.main)
    step("setup_swarm (re-run updates, no duplicates)", setup_swarm.main)
    assert len(fake.of("agents.create")) == n_specialists + 1, fake.of("agents.create")
    assert len(fake.of("agents.update")) == n_specialists + 1, fake.of("agents.update")
    assert len(fake.of("environments.create")) == 1
    assert len(fake.of("skills.create")) == len(create_specialists.SKILL_OWNERS)
    assert all(c[1]["display_name"].endswith("· offline-check") for c in fake.of("skills.create"))

    creates = [c[1] for c in fake.of("agents.create")]
    coordinator = creates[-1]
    assert coordinator["skills"][0] == {"type": "anthropic", "skill_id": "docx"}
    assert len(coordinator["skills"]) == 1 + len(create_specialists.skills_for("coordinator"))
    assert all(s["type"] == "custom" for s in coordinator["skills"][1:])
    assert "deal-deck" in create_specialists.skills_for("coordinator")
    assert coordinator["multiagent"]["type"] == "multiagent_20261001"
    assert len(coordinator["multiagent"]["subagents"]["predefined_agents"]) == n_specialists
    assert coordinator["model"] == {"id": "claude-sonnet-5-5", "effort": "medium"}  # dev profile
    assert coordinator["metadata"]["namespace"] == "offline-check"
    system = coordinator["system"]
    assert "{{" not in system and "# Workflow runs" in system and "# Critic review" not in system
    assert f"{common.OUTPUTS_DIR}/pitch-deck.html" in system, "coordinator prompt lost the deck step"
    assert all(f"- {n}:" in system for n in names), "roster lines missing from coordinator prompt"
    for spec, cfg in zip(create_specialists.SPECIALISTS, creates):
        assert cfg["system"] == common.load_prompt(spec["key"]), spec["key"]
        owned = create_specialists.skills_for(spec["key"])
        assert len(cfg["skills"]) == len(owned), (spec["key"], cfg["skills"])

    # 2. Run the deal against the scripted stream.
    step("run_deal_desk (scripted stream)", run_deal_desk.main)
    session = fake.of("sessions.create")[0][1]
    assert session["budget"]["max_list_cost"]["amount"] == common.PROFILES["dev"]["budget_cents"]
    assert session["title"].endswith("· offline-check")
    assert {r["mount_path"] for r in session["resources"]} == {
        f"/inputs/{p.name}" for p in run_deal_desk.input_files()}  # no memory store yet
    assert fake.sent[0]["type"] == "user.message"
    assert "memory" not in fake.sent[0]["content"][0]["text"]
    confirmations = [e for e in fake.sent if e["type"] == "user.tool_confirmation"]
    assert confirmations == [{"type": "user.tool_confirmation", "tool_use_id": "sevt_1",
                              "result": "deny"}], confirmations
    outputs = common.LOCAL_OUTPUTS
    assert (outputs / "coordinator-transcript.md").read_text() == "Proposal saved."
    assert (outputs / "proposal-response.docx").exists()
    assert (outputs / "pitch-deck.html").exists()
    assert "pitch-deck.html" in fake.sent[0]["content"][0]["text"], "kickoff lost the deck"
    uploads = len(fake.of("files.upload"))
    step("run_deal_desk (second run reuses uploads)", run_deal_desk.main)
    assert len(fake.of("files.upload")) == uploads == len(run_deal_desk.input_files())
    runs = common.RUNS_LOG.read_text().splitlines()
    assert len(runs) == 2 and '"outcome": "done"' in runs[-1], runs
    assert f'"fanout_agents": {n_specialists}' in runs[-1], runs  # S4: one parallel fan-out

    # 2b. S4 fan-out timing: briefs after the first report (follow-ups, the Critic) are not
    # part of the fan-out, and a one-at-a-time coordinator is flagged as not parallel.
    fan = run_deal_desk.FanOut()
    for n in names:
        fan.brief(n)
    assert "all working in parallel" in fan.report(names[0])
    fan.brief("Deal Desk Critic")
    assert fan.record()["fanout_agents"] == n_specialists, fan.record()
    serial = run_deal_desk.FanOut()
    serial.brief(names[0])
    assert "NOT PARALLEL" in serial.report(names[0])
    serial.brief(names[1])
    assert serial.record()["fanout_agents"] == 1
    print("ok    fan-out timing (S4)")

    # 2b. Memory stretch (S3): one store, attached read-write to every later session,
    #     a second customer's RFP, and outcomes written straight into the store.
    step("stretch_memory (creates the store)", lambda: stretch_memory.main([]))
    step("stretch_memory (re-run reuses it)", lambda: stretch_memory.main([]))
    assert len(fake.of("memory_stores.create")) == 1
    assert fake.of("memory_stores.create")[0][1]["metadata"]["namespace"] == "offline-check"

    kestrel = run_deal_desk.DATA / "rfp-kestrel-logistics.md"
    sent_before = len(fake.sent)
    step("run_deal_desk --rfp kestrel (memory attached)",
         lambda: run_deal_desk.main(["--rfp", str(kestrel)]))
    session = fake.of("sessions.create")[-1][1]
    stores = [r for r in session["resources"] if r["type"] == "memory_store"]
    assert stores == [{"type": "memory_store", "memory_store_id": "memstore_1",
                       "access": "read_write",
                       "instructions": common.load_prompt("coordinator.memory")}], stores
    assert len(stores[0]["instructions"]) <= 4096  # the API's limit for attachment instructions
    assert {r["mount_path"] for r in session["resources"] if r["type"] == "file"} == {
        f"/inputs/{p.name}" for p in run_deal_desk.input_files(kestrel)}
    assert "rfp-kestrel-logistics" in session["title"]
    kickoff = fake.sent[sent_before]["content"][0]["text"]
    assert "rfp-kestrel-logistics.md" in kickoff and "memory is attached" in kickoff, kickoff
    assert '"memory": true' in common.RUNS_LOG.read_text().splitlines()[-1]

    step("run_deal_desk --no-memory", lambda: run_deal_desk.main(["--no-memory"]))
    session = fake.of("sessions.create")[-1][1]
    assert all(r["type"] == "file" for r in session["resources"]), session["resources"]

    step("record_outcome (creates)", lambda: record_outcome.main(["Acme Corp", "Won on TCO."]))
    step("record_outcome (replaces)", lambda: record_outcome.main(["Acme Corp", "Won, 25% off."]))
    assert [c[1]["path"] for c in fake.of("memories.create")] == ["/outcomes/acme-corp.md"]
    assert len(fake.of("memories.update")) == 1
    assert "Won, 25% off." in fake.memories_db["mem_1"].content
    step("stretch_memory --show", lambda: stretch_memory.main(["--show"]))
    try:
        record_outcome.main(["Acme Corp"])
        raise AssertionError("record_outcome accepted a missing outcome")
    except SystemExit:
        pass

    # 3. Critic stretch: roster grows by one, prompt gains the critic section.
    step("stretch_critic_subagent", stretch_critic_subagent.main)
    last_coordinator = fake.of("agents.update")[-1][1]
    assert len(last_coordinator["multiagent"]["subagents"]["predefined_agents"]) == n_specialists + 1
    assert "# Critic review" in last_coordinator["system"]
    assert "not part of the fan-out" in last_coordinator["system"]
    critic = fake.of("agents.create")[-1][1]
    assert critic["name"] == "Deal Desk Critic"
    assert len(critic["skills"]) == len(create_specialists.skills_for("critic"))

    # 4. Org without multiagent_20261001: fall back to the older coordinator type.
    fallback = FakeClient(reject_new_multiagent=True)
    use(fallback, tmp, "fallback")
    step("setup_swarm (org without multiagent_20261001)", setup_swarm.main)
    coordinator = fallback.of("agents.create")[-1][1]
    assert coordinator["multiagent"]["type"] == "coordinator", coordinator["multiagent"]
    assert "# Workflow runs" not in coordinator["system"]

    # 4b. CRM MCP: only Pricing gets the server + toolset; the token goes to a Vault, not state.
    crm_url = "https://crm.example.com/mcp"
    os.environ.update(MCP_CRM_URL=crm_url, MCP_TOKEN="offline-secret")
    try:
        crm = FakeClient(events=events)
        use(crm, tmp, "crm")
        step("setup_swarm (CRM MCP on Pricing)", setup_swarm.main)
        by_name = {c[1]["name"]: c[1] for c in crm.of("agents.create")}
        pricing = by_name["Pricing Specialist"]
        assert pricing["mcp_servers"] == [{"type": "url", "name": "crm", "url": crm_url}], pricing
        assert any(t["type"] == "mcp_toolset" and t["mcp_server_name"] == "crm"
                   for t in pricing["tools"]), pricing["tools"]
        others = [c for n, c in by_name.items() if n != "Pricing Specialist"]
        assert all(not c.get("mcp_servers") for c in others), "CRM leaked to another agent"
        step("run_deal_desk (CRM vault)", run_deal_desk.main)
        cred = crm.of("vaults.credentials.create")[0][1]
        assert cred["auth"] == {"type": "static_bearer", "mcp_server_url": crm_url,
                                "token": "offline-secret"}, cred
        assert crm.of("sessions.create")[0][1]["vault_ids"] == ["vlt_1"]
        assert "offline-secret" not in common.STATE_FILE.read_text(), "token saved to state"
        step("run_deal_desk (CRM vault reused)", run_deal_desk.main)
        assert len(crm.of("vaults.create")) == 1, "vault should be reused"
    finally:
        os.environ.pop("MCP_CRM_URL", None)
        os.environ.pop("MCP_TOKEN", None)

    # 5. The demo profile resolves to the full models.
    common.PROFILE = "demo"
    assert common.model_for("coordinator") == "claude-opus-5-5"
    assert common.model_for("specialist") == "claude-sonnet-5-5"
    common.PROFILE = "dev"

    # 6. The deal-deck skill builds its own example, and its gates reject bad slides.
    step("deal-deck builds the example deck", lambda: check_deal_deck(tmp))

    # 7. Evals: cases, grader, harness and promptfoo provider, all at $0.
    step("evals (oracle passes, null fails, judge + session shapes, error path)",
         lambda: check_evals(tmp, fallback))

    if PROBLEMS:
        print("\nREQUEST SHAPE PROBLEMS (would fail against the real API):")
        for problem in dict.fromkeys(PROBLEMS):
            print(f"  - {problem}")
        sys.exit(1)
    print(f"\nPASS: all requests match anthropic {anthropic.__version__} types; no network used.")


if __name__ == "__main__":
    try:
        main()
    except AssertionError:
        traceback.print_exc()
        sys.exit(1)
