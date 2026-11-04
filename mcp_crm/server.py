"""Read-only MCP server ("CRM") over past-wins.json, for remote use by a Managed Agent.

Transport: Streamable HTTP at /mcp. Unauthenticated GET /health for Render.
Auth: every request except /health needs `Authorization: Bearer <MCP_TOKEN>`.

Env:  MCP_TOKEN (required), PORT (default 8000)
Run:  python server.py
"""

from __future__ import annotations

import hmac
import json
import os
import sys
from pathlib import Path
from typing import Annotated, Any

from mcp.server.fastmcp import FastMCP
from pydantic import Field
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse

DATA_FILE = Path(__file__).with_name("past-wins.json")


def _load_deals() -> list[dict[str, Any]]:
    try:
        deals = json.loads(DATA_FILE.read_text(encoding="utf-8"))["comparable_deals"]
    except (OSError, KeyError, ValueError) as exc:
        sys.exit(f"FEHLER: {DATA_FILE} nicht lesbar oder ohne 'comparable_deals': {exc}")
    if not isinstance(deals, list):
        sys.exit(f"FEHLER: 'comparable_deals' in {DATA_FILE} ist keine Liste.")
    return deals


DEALS = _load_deals()

mcp = FastMCP(
    "past-wins-crm",
    instructions=(
        "Read-only CRM of our past won deals (comparable_deals). Use search_past_wins to find "
        "comparable deals by industry, competitor or annual deal size, get_deal to read one deal "
        "in full, and pricing_stats for the overall discount benchmark."
    ),
    host="0.0.0.0",  # non-localhost host: no localhost-only Host-header check (Render uses its own hostname)
    port=int(os.environ.get("PORT", "8000")),
    stateless_http=True,  # no server-side sessions: survives restarts / multiple instances
    json_response=True,
)


@mcp.custom_route("/health", methods=["GET"])
async def health(_: Request) -> PlainTextResponse:
    return PlainTextResponse("ok")


@mcp.tool()
def search_past_wins(
    industry: Annotated[str | None, Field(description="Case-insensitive substring of the deal's industry, e.g. 'manufacturing' or 'retail'.")] = None,
    competitor: Annotated[str | None, Field(description="Competitor name (case-insensitive, substring match against primary_competitors), e.g. 'Snowflake'.")] = None,
    min_annual_usd: Annotated[int | None, Field(description="Minimum annual deal size in USD (inclusive).")] = None,
    max_annual_usd: Annotated[int | None, Field(description="Maximum annual deal size in USD (inclusive).")] = None,
) -> list[dict[str, Any]]:
    """Search our past won deals ("comparable deals") to find precedents for pricing a new deal.

    All filters are optional and combined with AND; with no filters every deal is returned.
    Each hit is the full deal record: customer, industry, deal_size_annual_usd, tier, term_years,
    discount_from_list (0.18 = 18% off list), payment_terms, primary_competitors, won_on, lost_on,
    closed, notes. Returns an empty list if nothing matches. Read-only.
    """
    if min_annual_usd is not None and max_annual_usd is not None and min_annual_usd > max_annual_usd:
        raise ValueError(f"min_annual_usd ({min_annual_usd}) is greater than max_annual_usd ({max_annual_usd}).")
    ind = industry.strip().lower() if industry else None
    comp = competitor.strip().lower() if competitor else None
    hits = []
    for d in DEALS:
        size = d.get("deal_size_annual_usd")
        if ind and ind not in str(d.get("industry", "")).lower():
            continue
        if comp and not any(comp in str(c).lower() for c in d.get("primary_competitors") or []):
            continue
        if min_annual_usd is not None and (size is None or size < min_annual_usd):
            continue
        if max_annual_usd is not None and (size is None or size > max_annual_usd):
            continue
        hits.append(d)
    return hits


@mcp.tool()
def get_deal(
    customer: Annotated[str, Field(description="Exact customer name of the deal, e.g. 'Globex Manufacturing' (case-insensitive).")],
) -> dict[str, Any]:
    """Return one past won deal in full (all fields, including notes) by customer name.

    Use after search_past_wins when you need the complete record. If no deal exists for that
    customer, the call fails with an error message that lists the available customer names.
    """
    key = customer.strip().lower()
    for d in DEALS:
        if str(d.get("customer", "")).strip().lower() == key:
            return d
    names = ", ".join(str(d.get("customer")) for d in DEALS)
    raise ValueError(f"No deal found for customer '{customer}'. Available customers: {names}.")


@mcp.tool()
def pricing_stats() -> dict[str, Any]:
    """Discount benchmark over ALL past deals: average, minimum and maximum discount_from_list.

    Discounts are fractions of list price (0.18 = 18% off). Also names the deals at the extremes.
    Use as a sanity check for a proposed discount; use search_past_wins for like-for-like comparison.
    """
    rows = [(d["discount_from_list"], d.get("customer")) for d in DEALS if d.get("discount_from_list") is not None]
    if not rows:
        raise ValueError("No deals with a discount_from_list value.")
    values = [v for v, _ in rows]
    lo, hi = min(rows, key=lambda r: r[0]), max(rows, key=lambda r: r[0])
    return {
        "deal_count": len(rows),
        "avg_discount_from_list": round(sum(values) / len(values), 4),
        "min_discount_from_list": lo[0],
        "min_discount_customer": lo[1],
        "max_discount_from_list": hi[0],
        "max_discount_customer": hi[1],
    }


class BearerAuth:
    """Pure-ASGI middleware: 401 unless `Authorization: Bearer <token>` matches (except /health)."""

    def __init__(self, app, token: str):
        self.app = app
        self.token = token.encode()

    async def __call__(self, scope, receive, send):
        # lifespan / websocket pass straight through; /health stays open for Render
        if scope["type"] != "http" or scope["path"] == "/health":
            return await self.app(scope, receive, send)
        auth = dict(scope["headers"]).get(b"authorization", b"")
        scheme, _, supplied = auth.partition(b" ")
        if scheme.lower() == b"bearer" and hmac.compare_digest(supplied.strip(), self.token):
            return await self.app(scope, receive, send)
        response = JSONResponse(
            {"error": "unauthorized"}, status_code=401, headers={"WWW-Authenticate": "Bearer"}
        )
        await response(scope, receive, send)


def create_app() -> BearerAuth:
    token = os.environ.get("MCP_TOKEN", "").strip()
    if not token:
        sys.exit("FEHLER: Umgebungsvariable MCP_TOKEN fehlt oder ist leer. Server startet nicht ohne Token.")
    return BearerAuth(mcp.streamable_http_app(), token)


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
