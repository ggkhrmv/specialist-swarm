"""
Stretch S2 — add a Critic to the coordinator's roster.

The Critic (prompt: prompts/critic.md) reviews the coordinator's draft before the
docx is built and leads with one verdict: SHIP IT, REVISE, or STOP.

This script creates (or updates) the Critic, saves it with the specialists, then
re-runs create_coordinator.py, which adds it to the roster and fills the
{{critic}} section of the coordinator's prompt from prompts/coordinator.critic.md.
Re-run run_deal_desk.py to see it in action.

Usage:
    uv run python stretch_critic_subagent.py
"""

import create_coordinator
from common import (agent_metadata, agent_toolset, get_client, load_prompt, load_state,
                    model_for, require, save_state, upsert_agent)


def main() -> None:
    client = get_client()
    state = load_state()
    specialists = require(state, "specialists", "uv run python create_specialists.py")

    critic, action = upsert_agent(
        client, specialists.get("critic"),
        name="Deal Desk Critic",
        description=("Reviews the coordinator's draft proposal before it ships and returns "
                     "SHIP IT, REVISE or STOP. Give it the draft path and the RFP path."),
        model=model_for("coordinator"),  # the critic needs to be as sharp as the coordinator
        system=load_prompt("critic"),
        tools=agent_toolset(only=("read", "glob", "grep")),
        metadata=agent_metadata("critic"),
    )
    specialists["critic"] = critic.id
    save_state(state)
    print(f"Critic {action}: {critic.id}\n")

    create_coordinator.main()  # roster + prompt now include the Critic


if __name__ == "__main__":
    main()
