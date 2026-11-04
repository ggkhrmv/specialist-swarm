# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A hackathon build of **Partner Basecamp Option 3, Scenario Card A: Deal Desk**, made by four people working in parallel. A
"Senior Partner" coordinator agent reads the Acme Corp RFP (`synthetic-data/rfp-acme-corp.md`), briefs four specialist
sub-agents in parallel, and turns their reports into a branded `proposal-response.docx`. It runs on **Claude Managed
Agents** (multiagent sessions + Skills). Cards B and C in `scenario-cards.md` are out of scope.

| Agent | Prompt | Skill | Model (demo / dev) |
| --- | --- | --- | --- |
| Deal Desk Senior Partner (coordinator) | `prompts/coordinator.md` | Anthropic `docx` + `positioning`, `storyline`, `voice` | Opus 5.5 / Sonnet 5.5 |
| Pricing Specialist | `prompts/pricing.md` | `pricing-playbook` (+ mounted `past-wins.json`) | Sonnet 5.5 / Haiku 5.5 |
| Legal Reviewer | `prompts/legal.md` | `legal-checklist` | Sonnet 5.5 / Haiku 5.5 |
| Technical Fit Specialist | `prompts/technical_fit.md` | `product-overview` + `positioning` | Sonnet 5.5 / Haiku 5.5 |
| Competitive Intel Analyst | `prompts/competitive.md` | `competitive-intel` + `positioning` | Haiku 5.5 / Haiku 5.5 |
| Deal Desk Critic (stretch S2, optional) | `prompts/critic.md` | `asset-review` | Opus 5.5 / Sonnet 5.5 |

## Commands

Run from the checkout root (main checkout or worktree) with `uv run`. Every checkout has its own `.venv`, and the
SessionStart hook runs `uv sync` when one is missing.

| Command | Cost | What it does |
| --- | --- | --- |
| `uv run python tests/offline_check.py [-v]` | $0, seconds | Runs the whole pipeline against a fake client and validates every request against the installed SDK's types. Run it after every change. CI runs it on every PR. |
| `uv run python setup_swarm.py` | $0 | Creates or updates this checkout's environment, skills, specialists and coordinator. Idempotent. Re-run it after any prompt, skill, description or profile change. |
| `uv run python run_deal_desk.py` | **real money**, capped per profile | Runs one session against the RFP: streams events, downloads `outputs/`, appends to `runs.jsonl` and prints the run history. `DEAL_RFP=<path.md\|.txt>` swaps in another RFP (keep real ones outside this public repo). |
| `uv run python download_deliverable.py [sesn_…]` | $0 | Re-downloads a session's output files. |
| `uv run python demo/scorecard.py [file] [--show]` | $0 | Scores the docx against the 13 traps in the Acme RFP. `demo/README.md` is the demo kit: pitch, answer key, run of show, real-data plan. |
| `uv run python stretch_critic_subagent.py` | $0 | Adds the Critic to the roster and the prompt. |
| `python3 scripts/wt.py new\|ls\|ship [--merge]\|clean` | ship pushes | Worktree lifecycle (see Team workflow). |

There is no linter or unit-test suite; `tests/offline_check.py` is the gate.

**Rules for Claude:**
- Never run `run_deal_desk.py` unless the user asks for a run: it spends money. `.claude/settings.json` forces a prompt for it.
- `setup_swarm.py` is free, but it creates persistent cloud agents that can only be archived, never deleted. Run it once per worktree, and again when config changes.
- Never read, print or edit `.env`. The repo is **public** (github.com/ggkhrmv/specialist-swarm).

## Architecture

- **Control plane vs data plane.** The setup scripts (`setup_environment` → `upload_skills` → `create_specialists` →
  `create_coordinator`, chained by `setup_swarm.py`) create persistent cloud objects. Their IDs go in this checkout's
  `.swarm_state.json`. `run_deal_desk.py` only creates a session against the saved coordinator.
- **`common.py` is the hub:** client factory, `PROFILES` / `model_for()`, `NAMESPACE`, state helpers, `load_prompt()`,
  `agent_toolset()`, `multiagent_block()` and `upsert_agent()` (update in place if the ID is saved, else create).
- **Prompts are files, sent verbatim.** `load_prompt()` fills the `{{placeholders}}` and fails on any it can't fill. In
  `coordinator.md`, `{{roster}}` is generated from each specialist's `name` + `description` in `create_specialists.py`.
  The coordinator decides whom to brief from those lines, so keep the descriptions accurate. `{{workflows}}` and
  `{{critic}}` pull in `coordinator.workflows.md` and `coordinator.critic.md` when they apply.
- **Skills:** only the skills mapped in `SKILL_OWNERS` (`create_specialists.py`) are uploaded, once per checkout, and
  attached to every agent listed for them (specialist keys, `coordinator`, `critic`). A changed skill gets a new
  version, and agents reference `"latest"`. Four of the asset-forge suite skills are mapped (`positioning`,
  `storyline`, `voice`, `asset-review`). The rest stay a library for Claude Code: `asset-forge` waits for human
  sign-offs at its gates, and the others don't apply to a docx deliverable. Skill descriptions must be ≤ 1024
  characters to upload.
- **Runtime data flow:** the RFP and `past-wins.json` are uploaded once (cached by content hash) and mounted read-only
  at `/mnt/session/uploads/inputs/`. All threads share that container's filesystem but **not** conversation history,
  so every brief must carry file paths. The deliverable must be written to `/mnt/session/outputs/`, the only directory
  `download_outputs()` can fetch.
- **Event stream:** the session stream shows the coordinator's turn plus thread lifecycle.
  `agent.thread_message_sent` is a brief going out and `agent.thread_message_received` is a report coming back.
  Specialists' own tool calls appear only in the Console trace (the URL is printed at run start).

## Invariants and gotchas

- **`.swarm_state.json` = ownership of cloud resources.** Never copy it between checkouts. A copy makes a worktree
  update the main checkout's demo agents. `.worktreeinclude` copies only `.env` on purpose. Delete the file to start
  fresh; the old agents linger in the Console, harmlessly.
- **Roster versions are pinned when the coordinator is saved.** After changing any specialist, re-run
  `create_coordinator.py` (`setup_swarm.py` does both).
- **Profiles:** branch `main` → `demo`; any other branch → `dev` (cheaper models, lower effort, $3 cap instead of $10).
  Override on the command line, e.g. `SWARM_PROFILE=demo uv run python setup_swarm.py`. Don't put it in `.env`, which
  is copied into every worktree. The profile is baked into the agents at setup, and runs use the budget of the profile
  recorded in state. Use `dev` for plumbing; judge output quality on `demo` before merging a prompt change.
- **Namespace** (from the branch, or `SWARM_NAMESPACE`) tags the environment name, skill display names, agent
  metadata and session titles, so you can find your own resources in the shared workspace.
- **API shapes (anthropic SDK ≥ 2.4) that stale examples get wrong:** `client.skills` / `client.files` are stable (not
  `beta`); skills take `display_name`, not `display_title`, and display names are not unique. The multiagent type is
  `multiagent_20261001`, and `create_coordinator.py` falls back to `coordinator` if the org lacks it. Session-scoped
  `client.beta.files.list(scope_id=…)` needs `betas=["managed-agents-2026-04-01"]`. Model IDs are `claude-opus-5-5` /
  `claude-sonnet-5-5` / `claude-haiku-5-5`, with no date suffix. The offline check catches shape drift against the
  installed SDK, so run it after any SDK bump.
- **Limits:** at most 20 roster entries, one level of delegation (a rostered agent can't have `multiagent`), and 25
  child threads per session.
- **Managed Agents runs on the Anthropic API only:** no Bedrock keys, no company gateways.
- Under the `auto` permission policy the server may pause a tool call. `run_deal_desk.py` asks at the terminal and
  denies when there is no TTY.

## Team workflow

- **The main checkout stays on `main`, clean:** pull, run the demo, start worktrees there. A PreToolUse hook
  (`.claude/hooks/guard_main.py`) blocks Claude's edits on `main`; mid-session, use EnterWorktree instead. Starting
  Claude with `ALLOW_MAIN_EDITS=1` overrides the block.
- **One worktree per change:** `claude -w <person>-<topic>` (or `python3 scripts/wt.py new <person>-<topic>` without
  Claude) creates `.claude/worktrees/<person>-<topic>` on branch `worktree-<person>-<topic>` from `origin/main`, and
  copies `.env`. Prefix the name with your own name so pushed branches never collide.
- **Iterate:** edit → offline check → `setup_swarm.py` → `run_deal_desk.py` → read the docx and the run history.
- **Ship small and often:** commit, then `python3 scripts/wt.py ship` (rebase on `origin/main` → offline check →
  push → open or update the PR). `--merge` squash-merges right away. If the rebase conflicts, `ship` aborts and lists
  the files.
- **Lanes**, to keep conflicts rare. Fill in the owners:

| Lane | Owner | Files | Stretch picks |
| --- | --- | --- | --- |
| Senior Partner and deliverable | | `prompts/coordinator*.md`, `create_coordinator.py` | S1 firm-voice skill, S7 pptx deck |
| Commercial (Pricing + Legal) | | `prompts/{pricing,legal}.md`, `skills/{pricing-playbook,legal-checklist}/`, `synthetic-data/past-wins.json` | S5 CRM MCP for past wins, S9 legal voting |
| Solution (Technical Fit + Competitive) | | `prompts/{technical_fit,competitive}.md`, `skills/{product-overview,competitive-intel}/` | S2 Critic |
| Run, demo and platform | | `run_deal_desk.py`, `common.py`, `tests/`, `scripts/`, `.claude/` | S4 parallelism visual, demo rehearsal |

- **Hot files** are shared across lanes: `common.py`, the `SPECIALISTS` / `SKILL_OWNERS` tables in
  `create_specialists.py`, `README.md` and this file. Keep edits to them tiny and ship them on their own, first.
- **Adding a specialist:** add an entry to `SPECIALISTS`, write `prompts/<key>.md`, and optionally map a skill in
  `SKILL_OWNERS`. The offline check derives its counts from these tables.

## Demo checklist (Card A)

1. After the last merge, in the main checkout: `git pull`, then `uv run python setup_swarm.py` (the `demo` profile on
   `main`).
2. Do one full rehearsal with `uv run python run_deal_desk.py`. Keep a copy of the best `outputs/proposal-response.docx`
   outside `outputs/`, because the next run overwrites it.
3. Use two screens: the terminal event stream (`[brief →]` × 4 in parallel, then `[report ←]`) and the docx. Keep the
   Console trace URL open to show the specialist threads.
