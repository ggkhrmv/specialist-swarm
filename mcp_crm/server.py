"""Synthetic CRM MCP: past wins as a queryable, read-only API.

Remote MCP server (Streamable HTTP) for Claude Managed Agents.
  MCP endpoint : /mcp   (needs  Authorization: Bearer <MCP_TOKEN>)
  Health check : /health (no auth)
Env: MCP_TOKEN (required), PORT (default 8000).
"""

import hmac
import json
import os
import sys
from pathlib import Path

import uvicorn
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

TOKEN = os.environ.get("MCP_TOKEN", "")
if not TOKEN:
    sys.exit("MCP_TOKEN is not set. Set it as an environment variable.")

PORT = int(os.environ.get("PORT", "8000"))
DEALS = json.loads((Path(__file__).parent / "past-wins.json").read_text())["comparable_deals"]

mcp = FastMCP(
    "crm",
    host="0.0.0.0",
    port=PORT,
    # Behind Render's proxy the Host header is the public domain; bearer auth protects us.
    transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
)


@mcp.tool()
def search_past_wins(
    industry: str | None = None,
    competitor: str | None = None,
    min_annual_usd: int | None = None,
    max_annual_usd: int | None = None,
) -> list[dict]:
    """Search closed comparable deals (past wins) in the CRM.

    All filters are optional and combined with AND.
    industry: case-insensitive substring of the deal's industry (e.g. "manufacturing").
    competitor: case-insensitive substring of a primary competitor (e.g. "snowflake").
    min_annual_usd / max_annual_usd: range on annual deal size in USD.
    Returns full deal records incl. tier, term, discount_from_list, payment_terms,
    competitors, won_on and notes.
    """
    out = []
    for d in DEALS:
        if industry and industry.lower() not in d["industry"].lower():
            continue
        if competitor and not any(competitor.lower() in c.lower() for c in d["primary_competitors"]):
            continue
        if min_annual_usd is not None and d["deal_size_annual_usd"] < min_annual_usd:
            continue
        if max_annual_usd is not None and d["deal_size_annual_usd"] > max_annual_usd:
            continue
        out.append(d)
    return out


@mcp.tool()
def get_deal(customer: str) -> dict:
    """Get one past deal by customer name (case-insensitive, partial match ok)."""
    matches = [d for d in DEALS if customer.lower() in d["customer"].lower()]
    if not matches:
        return {"error": f"No deal found for '{customer}'.",
                "known_customers": [d["customer"] for d in DEALS]}
    return matches[0]


@mcp.tool()
def pricing_stats() -> dict:
    """Aggregate discount and deal-size stats over all past deals."""
    disc = [d["discount_from_list"] for d in DEALS]
    size = [d["deal_size_annual_usd"] for d in DEALS]
    return {
        "deals": len(DEALS),
        "discount_from_list": {"min": min(disc), "max": max(disc), "avg": round(sum(disc) / len(disc), 3)},
        "deal_size_annual_usd": {"min": min(size), "max": max(size), "avg": round(sum(size) / len(size))},
    }


class BearerAuth:
    """ASGI middleware: /health open, everything else needs the bearer token."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        if scope["path"] == "/health":
            return await self._reply(send, 200, b"ok")
        headers = dict(scope["headers"])
        supplied = headers.get(b"authorization", b"").decode()
        if not hmac.compare_digest(supplied, f"Bearer {TOKEN}"):
            return await self._reply(send, 401, b"unauthorized")
        return await self.app(scope, receive, send)

    @staticmethod
    async def _reply(send, status, body):
        await send({"type": "http.response.start", "status": status,
                    "headers": [(b"content-type", b"text/plain")]})
        await send({"type": "http.response.body", "body": body})


app = BearerAuth(mcp.streamable_http_app())

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
