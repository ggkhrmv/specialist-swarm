# Option 3 — Specialist Swarm

**Concept landed:** Skills, plugins & sub-agents
**Tech:** [Claude Managed Agents multi-agent](https://platform.claude.com/docs/en/managed-agents/multi-agent) + [custom Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) + the pre-built [docx skill](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/quickstart)
**Time:** 60 minutes
**Output:** A coordinator agent that fans work out to 3-5 specialist sub-agents, each with its own skills, that assemble a real branded Word document.

## The pitch

This is the architecture that wins the next $50M transformation deal: **coordinator + specialists + skills**. It maps directly to how every services firm structures real work. A senior partner orchestrates; specialists (legal, pricing, technical) own their lanes; the senior partner synthesises and delivers.

You're going to build exactly that, in 60 minutes, around a Deal Desk scenario. Drop an RFP in, get a branded response doc out, watch the parallelism happen in real time on the events stream.

## Setup (5 min)

You need an Anthropic API key from the Console. Managed Agents runs on the Anthropic API only: Bedrock keys and most company gateways won't work here. Multi-agent sessions may need to be enabled for your workspace.

```bash
uv sync                          # creates .venv with Python 3.10+ and the packages
echo 'ANTHROPIC_API_KEY=sk-ant-...' > .env   # or export it in your shell (the shell wins)
```

`.env` is gitignored. No uv? Use `pip install -r requirements.txt` in a Python 3.10+ venv, then run the scripts with `python` instead of `uv run python`.

## Pick a scenario card

Three cards in [`scenario-cards.md`](./scenario-cards.md). Each gives you a coordinator + a different roster of specialists. Pick one. Different teams should pick different cards.

**This team builds Card A: Deal Desk.** A Senior Partner coordinator turns the Acme Corp RFP into a branded proposal docx, using four specialists, each backed by its own skill:

| Specialist | Skill | Also reads |
| --- | --- | --- |
| Pricing Specialist | `pricing-playbook` | `past-wins.json` |
| Legal Reviewer | `legal-checklist` | |
| Technical Fit Specialist | `product-overview` | |
| Competitive Intel Analyst | `competitive-intel` | |

All four read the RFP.

## Team workflow (4 people, worktrees)

Every change happens in its own git worktree, and each worktree runs its own swarm in the cloud. Nobody's experiment touches a teammate's agents or the demo swarm.

```bash
# in the main checkout (stays on main: pull, demo, start worktrees)
git pull
claude -w alex-legal-redlines        # or: python3 scripts/wt.py new alex-legal-redlines

# inside the worktree
uv run python tests/offline_check.py # $0, seconds: run after every change
uv run python setup_swarm.py         # once per worktree, then after every prompt or skill edit
uv run python run_deal_desk.py       # a real run (dev profile: cheaper models, $3 cap)
python3 scripts/wt.py ship --merge   # rebase on main, check, push, PR, squash-merge
```

[`CLAUDE.md`](./CLAUDE.md) has the full rules: lanes, profiles, gotchas and the demo checklist.

## Core build (25 min)

**Fast path:** `uv run python setup_swarm.py` runs steps 1-4 in order, then step 5 is `uv run python run_deal_desk.py`. To understand the pieces, run them one at a time:

1. **Create the environment.** `uv run python setup_environment.py` creates the cloud environment that each session's container comes from.

2. **Upload the skills.** `uv run python upload_skills.py` packages each folder in `skills/` and uploads it through the Skills API. If you edit a `SKILL.md` and re-run, a new version is uploaded.

3. **Create the specialists.** `uv run python create_specialists.py` creates Pricing, Legal, Technical Fit and Competitive Intel. Each gets read-only tools, its system prompt from `prompts/<key>.md`, and the skill for its domain (table above).

4. **Create the coordinator.** `uv run python create_coordinator.py` creates the Senior Partner. It lists the specialists as its roster (`multiagent_20261001`) and carries Anthropic's pre-built `docx` skill. If your organisation doesn't have that multiagent type yet, the script falls back to the older `coordinator` type.

5. **Run the deal.** `uv run python run_deal_desk.py`:
   - Uploads the RFP and `past-wins.json`, then mounts them read-only at `/mnt/session/uploads/inputs/`. Every thread shares the container, so each specialist reads the files itself. Specialists never see the coordinator's conversation.
   - Starts a session with a spend cap: **$10 on the `demo` profile, $3 on `dev`** (`PROFILES` in `common.py`)
   - Streams the events so you can watch the parallel fan-out, and asks you in the terminal if the server pauses a tool call for review
   - Downloads everything written to `/mnt/session/outputs/` into `outputs/`, including `proposal-response.docx`

By minute 30 you have a Word document in `outputs/`, generated by a coordinator + specialists who each used their own skill.

**Iterating:** every step is safe to re-run. It reuses or updates what it made before instead of creating duplicates, and all IDs live in `.swarm_state.json`. After editing a specialist, re-run `create_coordinator.py` (or just `setup_swarm.py`) so the roster points at the new version. Delete `.swarm_state.json` to start fresh.

**Dynamic workflows** are on for the coordinator, limited to the four specialists. Its prompt tells it to start a workflow run only when asked to handle several RFPs at once; a single RFP is briefed directly. Every agent in a run uses tokens, which is one reason for the session cap. To turn runs off, set `"workflows": {"type": "disabled"}` in `multiagent_block()` in `common.py` and re-run `create_coordinator.py`.

## Stretch goals (20 min)

See [`stretch-goals.md`](./stretch-goals.md). The big ones:

- **Custom firm-voice skill** — codify your own firm's voice (every services firm has one)
- **Critic sub-agent** — add a fifth agent that reviews the coordinator's draft before it's finalised
- **Memory across deals** — coordinator remembers past wins and re-uses the right ones
- **Synthetic MCP for past wins** — wire up a fake CRM to the pricing specialist

## Two-minute demo

Two-monitor setup:
- **Monitor 1:** the events stream from the coordinator session, scrolling. You'll see `session.thread_created` × 4, parallel `running`, then `agent.thread_message_received` flowing back. The visible parallelism IS the demo.
- **Monitor 2:** open `outputs/proposal-response.docx`. Real document, branded, ready to send.

Narrate the events stream while it runs. The room will get it.

## What's in this folder

```
specialist-swarm/
├── README.md
├── scenario-cards.md
├── stretch-goals.md
├── pyproject.toml / requirements.txt
├── CLAUDE.md                      (team rules, architecture, gotchas: read this)
├── common.py                      (client, profiles, namespace, saved IDs, shared helpers)
├── prompts/                       (every agent's system prompt, sent verbatim)
├── setup_swarm.py                 (runs steps 1-4 in order)
├── setup_environment.py           (1: cloud environment)
├── upload_skills.py               (2: uploads custom skills via the Skills API)
├── create_specialists.py          (3: the four specialists, skills attached)
├── create_coordinator.py          (4: the coordinator, roster + docx skill)
├── run_deal_desk.py               (5: runs the full swarm against the RFP)
├── download_deliverable.py        (re-download a session's output files)
├── stretch_critic_subagent.py     (stretch S2: critic agent)
├── tests/offline_check.py         ($0 fake-client run of the whole pipeline; CI runs it)
├── demo/                          (demo kit: pitch, Acme answer key, run of show, real data; scorecard.py)
├── scripts/wt.py                  (worktrees: new / ls / ship / clean)
├── .claude/                       (team settings: hooks, permissions)
├── skills/                        (Deal Desk skills, one per specialist, + the asset-forge suite)
│   ├── pricing-playbook/SKILL.md
│   ├── legal-checklist/SKILL.md
│   ├── product-overview/SKILL.md  (the capability map, for Technical Fit)
│   ├── competitive-intel/SKILL.md
│   └── (asset-forge suite + presentation-websites, see below)
└── synthetic-data/
    ├── rfp-acme-corp.md           (the RFP that triggers the swarm)
    └── past-wins.json             (used by pricing specialist)
```

## Asset-forge skill suite

`skills/` also carries a general-purpose suite for building consulting assets (proposals, RfP/RfQ responses, pitch decks, readouts, presentation sites, capability maps). These are standard Agent Skills (`SKILL.md` + `references/` + `evals/`). Copy them into `~/.claude/skills/` for Claude Code, or upload them with the Skills API the same way `upload_skills.py` does. `upload_skills.py` uploads only the skills mapped to agents in `SKILL_OWNERS` (`create_specialists.py`). From this suite those are `positioning` (coordinator, Technical Fit, Competitive Intel), `storyline` and `voice` (coordinator) and `asset-review` (Critic). The orchestrator, `asset-forge`, stays local because its gates wait for a human.

| Skill | What it does |
|---|---|
| `asset-forge` | Orchestrator. Intake → Qualify → Frame → Storyline → Build → Review → Rework, with a living-log state file and gates |
| `positioning` | Win themes, discriminators, scope options, compliance matrix and claims register |
| `storyline` | SCQA / Minto pyramid, governing thought, action titles, exec summary |
| `asset-review` | Multi-persona review board merged into a page-by-page redline, plus claims and number checks |
| `voice` | Author-voice matching, DACH/German localization, de-slop pass for marked-up copy |
| `evidence` | Measuring claims from an organisation's own systems (tickets, repos, logs) defensibly |
| `diagram-spec` | Hand-built SVG diagrams that are semantically right and geometrically verified |
| `capability-map` | A reusable, fillable capability/maturity assessment as one HTML file |
| `presentation-websites` | Brand-agnostic, self-contained single-file presentation sites: you supply the brand kit (tokens, fonts, logo) |

Examples in the suite use `[FIRM]`, `[CLIENT]` and `[REFERENCE-x]` placeholders, and every worked case is fictional. Some skills optionally call `humanizer`, `writing`, `dataviz` or `smd-review` when they're installed; none of them require these.

To try the presentation framework: copy `skills/presentation-websites/template.html`, fill the `BRAND:` tokens and LOGO SLOTs, put your licensed font files in `assets/fonts/` (git-ignored), and run `python3 skills/presentation-websites/embed-fonts.py yourpage.html`.

