"""
Step 4 — create the coordinator ("Senior Partner") that orchestrates the swarm.

- Its system prompt is prompts/coordinator.md. The {{roster}} placeholder is filled
  from the specialists' own names and descriptions; {{workflows}} and {{critic}} are
  filled from prompts/coordinator.workflows.md and prompts/coordinator.critic.md
  when they apply.
- Its roster is every specialist saved in .swarm_state.json (plus the Critic, if
  you've run stretch_critic_subagent.py).
- It carries Anthropic's pre-built docx skill, so it can produce the Word document.
- It uses the current multiagent type (multiagent_20261001). If your organisation
  doesn't have that type yet, it falls back to the older `coordinator` type.

Safe to re-run: the saved coordinator is updated in place. Re-run it after
changing any specialist so the roster points at the specialists' new versions.

Usage:
    uv run python create_coordinator.py
"""

import anthropic

from common import (OUTPUTS_DIR, PROFILE, agent_metadata, agent_toolset, get_client,
                    load_prompt, load_state, model_for, multiagent_block, require, save_state,
                    upsert_agent)


def build_system(roster_lines: list[str], workflows: bool, critic: bool) -> str:
    return load_prompt(
        "coordinator",
        roster="\n".join(roster_lines),
        outputs=OUTPUTS_DIR,
        workflows=load_prompt("coordinator.workflows") if workflows else "",
        critic=load_prompt("coordinator.critic") if critic else "",
    )


def main() -> None:
    client = get_client()
    state = load_state()
    specialists: dict = require(state, "specialists", "uv run python create_specialists.py")
    agent_ids = list(specialists.values())

    # The roster section is built from the specialists' own names and descriptions.
    roster_lines = []
    for agent_id in agent_ids:
        agent = client.beta.agents.retrieve(agent_id)
        roster_lines.append(f"- {agent.name}: {agent.description}" if agent.description
                            else f"- {agent.name}")

    has_critic = "critic" in specialists
    existing_id = (state.get("coordinator") or {}).get("id")
    common_config = dict(
        name="Deal Desk Senior Partner",
        description="Runs a Deal Desk: briefs the specialists, synthesises, delivers the docx.",
        model=model_for("coordinator"),
        tools=agent_toolset(),  # bash + file tools, to build the docx; no web
        skills=[{"type": "anthropic", "skill_id": "docx"}],
        metadata=agent_metadata("coordinator"),
    )

    kind = "multiagent_20261001"
    try:
        agent, action = upsert_agent(
            client, existing_id,
            system=build_system(roster_lines, workflows=True, critic=has_critic),
            multiagent=multiagent_block(agent_ids, kind),
            **common_config,
        )
    except anthropic.BadRequestError as error:
        if "multiagent" not in str(error.message):
            raise
        # The org (or beta header) doesn't accept multiagent_20261001 yet.
        kind = "coordinator"
        print("  multiagent_20261001 isn't available to this organisation yet; "
              "using the older `coordinator` type (delegation only, no workflow runs).")
        agent, action = upsert_agent(
            client, existing_id,
            system=build_system(roster_lines, workflows=False, critic=has_critic),
            multiagent=multiagent_block(agent_ids, kind),
            **common_config,
        )

    state["coordinator"] = {"id": agent.id, "multiagent_type": kind}
    state["profile"] = PROFILE
    save_state(state)
    print(f"Coordinator {action}: {agent.id} (v{agent.version}, {kind}, profile {PROFILE})")
    print(f"Roster: {', '.join(specialists)}")
    print("\nNext: uv run python run_deal_desk.py")


if __name__ == "__main__":
    main()
