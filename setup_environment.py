"""
Step 1 — create the cloud Environment the Deal Desk sessions run in.

Each session gets its own container from this environment; the coordinator and
every specialist thread share that container's filesystem.

Safe to re-run: an environment saved in .swarm_state.json is reused.

Usage:
    uv run python setup_environment.py
"""

from common import NAMESPACE, get_client, load_state, save_state


def main() -> None:
    state = load_state()
    if state.get("environment_id"):
        print(f"Environment already exists: {state['environment_id']} (reusing)")
        return

    client = get_client()
    environment = client.beta.environments.create(
        name=f"specialist-swarm-{NAMESPACE}",
        config={
            "type": "cloud",
            # No open internet: the agents only read mounted files and build a docx.
            # Package managers stay reachable in case the docx skill installs a library.
            "networking": {"type": "limited", "allow_package_managers": True},
        },
    )
    state["environment_id"] = environment.id
    save_state(state)
    print(f"Environment created: {environment.id}")


if __name__ == "__main__":
    main()
