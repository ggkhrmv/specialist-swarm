"""
Connect the Pricing Specialist to the remote CRM MCP server (mcp_crm/ on Render).

What it does (idempotent, safe to re-run):
1. Creates a vault with a static_bearer credential for the MCP server URL
   (the token never enters the agent definition or the sandbox) -> .vault_id
2. Updates the existing Pricing Specialist: adds the MCP server + an mcp_toolset
   (read-only, so always_allow: no approval pauses mid-demo) and points its
   prompt at the CRM tools instead of past-wins.json.

run_deal_desk.py picks up .vault_id automatically and attaches the vault to the session.

Usage:
    export ANTHROPIC_API_KEY="sk-ant-..."
    export MCP_CRM_URL="https://<your-service>.onrender.com/mcp"
    export MCP_TOKEN="<same token as on Render>"
    python connect_crm.py
"""

import json
import os
from pathlib import Path

from anthropic import Anthropic

SERVER_NAME = "past-wins-crm"
OLD_INPUT_LINE = "- past-wins.json (recent comparable deals)\n"
CRM_INPUT_LINE = (
    "- A live CRM of past won deals via the 'past-wins-crm' MCP tools: "
    "search_past_wins (filter by industry / competitor / annual deal size), "
    "get_deal (full record for one customer), pricing_stats (overall discount benchmark). "
    "Query the CRM yourself before recommending a discount; ignore any inlined past-wins.json.\n"
)


def main() -> None:
    url = os.environ.get("MCP_CRM_URL", "").strip()
    token = os.environ.get("MCP_TOKEN", "").strip()
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("Set ANTHROPIC_API_KEY before running.")
    if not url.startswith("https://") or not url.rstrip("/").endswith("/mcp"):
        raise SystemExit("Set MCP_CRM_URL to the public MCP endpoint, e.g. https://<service>.onrender.com/mcp")
    if not token:
        raise SystemExit("Set MCP_TOKEN to the bearer token configured on Render.")

    ids_path = Path(".specialist_ids.json")
    if not ids_path.exists():
        raise SystemExit("Run create_specialists.py first (.specialist_ids.json missing).")
    pricing_id = json.loads(ids_path.read_text())["pricing"]

    client = Anthropic()

    # 1. Vault + credential (keyed by MCP server URL)
    vault_path = Path(".vault_id")
    if vault_path.exists():
        print(f"  vault exists ({vault_path.read_text().strip()}) - delete .vault_id to recreate")
    else:
        vault = client.beta.vaults.create(display_name="Deal Desk CRM")
        client.beta.vaults.credentials.create(
            vault.id,
            display_name="CRM MCP bearer token",
            auth={"type": "static_bearer", "mcp_server_url": url, "token": token},
        )
        vault_path.write_text(vault.id)
        print(f"  vault created: {vault.id}")

    # 2. Update the Pricing Specialist (arrays are replaced wholesale -> keep existing entries)
    agent = client.beta.agents.retrieve(pricing_id)
    mcp_servers = [s for s in (agent.mcp_servers or []) if s.name != SERVER_NAME]
    mcp_servers.append({"type": "url", "name": SERVER_NAME, "url": url})
    mcp_servers = [s if isinstance(s, dict) else {"type": "url", "name": s.name, "url": s.url} for s in mcp_servers]

    tools = [t.to_dict() if hasattr(t, "to_dict") else t for t in agent.tools]
    tools = [t for t in tools if not (t.get("type") == "mcp_toolset" and t.get("mcp_server_name") == SERVER_NAME)]
    tools.append({
        "type": "mcp_toolset",
        "mcp_server_name": SERVER_NAME,
        "default_config": {"enabled": True, "permission_policy": {"type": "always_allow"}},  # read-only server
    })

    system = agent.system or ""
    if OLD_INPUT_LINE in system:
        system = system.replace(OLD_INPUT_LINE, CRM_INPUT_LINE)
    elif "past-wins-crm" not in system:
        system += "\n\n" + CRM_INPUT_LINE

    updated = client.beta.agents.update(
        pricing_id,
        version=agent.version,
        mcp_servers=mcp_servers,
        tools=tools,
        system=system,
    )
    print(f"  Pricing Specialist {updated.id} updated to version {updated.version}")
    print("Next: python run_deal_desk.py")


if __name__ == "__main__":
    main()
