"""
Step 1 — create the cloud Environment the Deal Desk sessions run in.

Each session gets its own container from this environment; the coordinator and
every specialist thread share that container's filesystem.

Safe to re-run: an environment saved in .swarm_state.json is reused.

Usage:
    uv run python setup_environment.py
"""

from urllib.parse import urlparse

from common import NAMESPACE, crm_url, get_client, load_state, save_state


def networking() -> dict:
    """No open internet. Package managers stay reachable in case the docx skill installs a
    library. With a CRM MCP configured, its host (and only it) is allowed too: a session
    fails to start (400) when the environment blocks an agent's MCP server."""
    net = {"type": "limited", "allow_package_managers": True}
    if crm_url():
        net["allowed_hosts"] = [urlparse(crm_url()).hostname]
    return net


def main() -> None:
    state = load_state()
    if state.get("environment_id"):
        if crm_url():  # let an environment made before the CRM MCP reach its host
            get_client().beta.environments.update(state["environment_id"],
                                                  config={"type": "cloud", "networking": networking()})
        print(f"Environment already exists: {state['environment_id']} (reusing)")
        return

    client = get_client()
    environment = client.beta.environments.create(
        name=f"specialist-swarm-{NAMESPACE}",
        config={
            "type": "cloud",
            "networking": networking(),
        },
    )
    state["environment_id"] = environment.id
    save_state(state)
    print(f"Environment created: {environment.id}")


if __name__ == "__main__":
    main()
