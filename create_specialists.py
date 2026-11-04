"""
Step 3 — create the four Deal Desk specialists (Scenario Card A).

Each specialist gets:
- its system prompt from prompts/<key>.md (sent verbatim: edit the file, not code),
- read-only tools (read / glob / grep): specialists read the mounted RFP and data
  files from the shared container, they don't write anything,
- the custom skills mapped to it in SKILL_OWNERS, attached at creation (run
  upload_skills.py first),
- the model for its role in the current profile (see PROFILES in common.py).

The coordinator picks whom to brief from each specialist's `name` and
`description` below, so keep the descriptions accurate.

Safe to re-run: saved specialists are updated in place (a new version under the
same ID). After changing a specialist, re-run create_coordinator.py (or just
setup_swarm.py) so the coordinator's roster points at the new version.

To add a specialist: add an entry to SPECIALISTS, write prompts/<key>.md, and
(optionally) map a skill to it in SKILL_OWNERS.

Usage:
    uv run python create_specialists.py
"""

import os

from common import (PROFILE, agent_metadata, agent_toolset, get_client, load_prompt,
                    load_state, model_for, require, save_state, upsert_agent)

READ_ONLY = ("read", "glob", "grep")

# Past wins from a CRM MCP server instead of past-wins.json. Set CRM_MCP_URL (shell or
# .env) to the PUBLIC https URL of the server, e.g. a tunnel to synthetic_crm_mcp.py:
# managed agents run in Anthropic's cloud and cannot reach localhost.
CRM_MCP_URL = os.environ.get("CRM_MCP_URL", "").strip()


def mcp_config(spec_key: str) -> dict:
    """Extra agent config that attaches the CRM MCP server to the Pricing Specialist."""
    if spec_key != "pricing" or not CRM_MCP_URL:
        return {}
    return {
        "mcp_servers": [{"type": "url", "name": "synthetic-crm", "url": CRM_MCP_URL}],
        "mcp_toolset": {"type": "mcp_toolset", "mcp_server_name": "synthetic-crm",
                        "default_config": {"permission_policy": {"type": "auto"}}},
    }

# skill folder name -> keys of the agents that carry it. Keys are specialist keys,
# plus "coordinator" and "critic". The first four are the Deal Desk domain skills;
# the rest come from the asset-forge suite (see README). asset-forge itself stays
# out: its gates wait for a human sign-off, and these agents run unattended.
SKILL_OWNERS = {
    "pricing-playbook": ("pricing",),
    "legal-checklist": ("legal",),
    "product-overview": ("technical_fit",),
    "competitive-intel": ("competitive",),
    "positioning": ("coordinator", "technical_fit", "competitive"),
    "storyline": ("coordinator",),
    "voice": ("coordinator",),
    "asset-review": ("critic",),
    "deal-deck": ("coordinator",),  # S7: the 5-slide HTML pitch deck
}


def skills_for(owner: str) -> list[str]:
    """The skill folders an agent carries, in SKILL_OWNERS order."""
    return [skill for skill, owners in SKILL_OWNERS.items() if owner in owners]


def skill_refs(owner: str, uploaded: dict) -> list[dict]:
    """The agent `skills` entries for an owner, from the uploaded skills in state."""
    owned = skills_for(owner)
    missing = [s for s in owned if s not in uploaded]
    if missing:
        raise SystemExit(f"Skill(s) {missing} not uploaded. Run upload_skills.py first.")
    return [{"type": "custom", "skill_id": uploaded[s]["id"], "version": "latest"}
            for s in owned]

# key -> prompts/<key>.md; role -> which model of the profile it runs on
SPECIALISTS = [
    {
        "key": "pricing",
        "name": "Pricing Specialist",
        "description": ("Recommends commercial terms for an RFP: tier, list price, discount "
                        "band, payment terms, concessions. Give it the RFP path"
                        + (" (past wins come from the CRM MCP)." if CRM_MCP_URL
                           else " and the past-wins.json path.")),
        "role": "specialist",
    },
    {
        "key": "legal",
        "name": "Legal Reviewer",
        "description": ("Flags RFP clauses that conflict with our standard contract positions "
                        "and proposes counter-positions. Give it the RFP path."),
        "role": "specialist",
    },
    {
        "key": "technical_fit",
        "name": "Technical Fit Specialist",
        "description": ("Assesses how well our product covers the RFP's requirements, using "
                        "the product capability map. Give it the RFP path."),
        "role": "specialist",
    },
    {
        "key": "competitive",
        "name": "Competitive Intel Analyst",
        "description": ("Identifies the likely competitors on an RFP and how to position "
                        "against them. Give it the RFP path."),
        "role": "fast",  # a quick battlecard lookup: the cheap model is enough
    },
]


def main() -> None:
    client = get_client()
    state = load_state()
    skills = require(state, "skills", "uv run python upload_skills.py")
    saved: dict = state.setdefault("specialists", {})

    for spec in SPECIALISTS:
        owned = skills_for(spec["key"])
        mcp = mcp_config(spec["key"])
        mcp_toolset = mcp.pop("mcp_toolset", None)  # goes into `tools`; mcp_servers stays
        agent, action = upsert_agent(
            client, saved.get(spec["key"]),
            name=spec["name"],
            description=spec["description"],
            model=model_for(spec["role"]),
            system=load_prompt(spec["key"]),
            tools=agent_toolset(only=READ_ONLY) + ([mcp_toolset] if mcp_toolset else []),
            **mcp,
            skills=skill_refs(spec["key"], skills),
            metadata=agent_metadata(spec["key"]),
        )
        saved[spec["key"]] = agent.id
        state["profile"] = PROFILE
        save_state(state)
        print(f"  {action:7s} {spec['name']:28s} {agent.id}  (v{agent.version}, "
              f"skills: {', '.join(owned) or 'none'})")

    print(f"\nProfile: {PROFILE}. Next: uv run python create_coordinator.py")


if __name__ == "__main__":
    main()
