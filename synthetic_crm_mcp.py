"""
Synthetic CRM MCP server (stretch goal S5).

Exposes synthetic-data/past-wins.json as two MCP tools instead of a static file:
  - search_past_deals(industry, competitor, outcome, min_annual_usd, max_annual_usd)
  - get_deal(customer)

Pure standard library (works on Python 3.9, no `mcp` package needed). Speaks
MCP over streamable HTTP (JSON-RPC via POST /mcp). Every tool call is printed
to the console, so this terminal doubles as a live "who queried the CRM" view
during the demo.

Usage:
    python synthetic_crm_mcp.py            # listens on http://localhost:8765/mcp

Managed agents run in Anthropic's cloud, so they cannot reach localhost.
Deploy this (see Dockerfile) to any host that gives you a public https URL and
set CRM_MCP_URL=https://<host><MCP_PATH> before create_specialists.py.
"""

import json
import os
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = json.loads((HERE / "synthetic-data" / "past-wins.json").read_text())["comparable_deals"]
PORT = int(os.environ.get("PORT", 8765))  # cloud hosts inject PORT
# Set MCP_PATH to an unguessable value (e.g. /mcp-7f3a9c) when deployed
# publicly: the agent config only takes a URL, so the path acts as the secret.
MCP_PATH = os.environ.get("MCP_PATH", "/mcp")

TOOLS = [
    {
        "name": "search_past_deals",
        "description": (
            "Search the CRM for past comparable deals (wins and losses). All "
            "filters are optional; omit them all to list every deal."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "industry": {"type": "string", "description": "Substring match, e.g. 'Industrial'"},
                "competitor": {"type": "string", "description": "e.g. 'Databricks'"},
                "outcome": {"type": "string", "enum": ["won", "lost"]},
                "min_annual_usd": {"type": "number"},
                "max_annual_usd": {"type": "number"},
            },
        },
    },
    {
        "name": "get_deal",
        "description": "Get the full CRM record for one customer, including notes.",
        "inputSchema": {
            "type": "object",
            "properties": {"customer": {"type": "string"}},
            "required": ["customer"],
        },
    },
]


def search_past_deals(industry=None, competitor=None, outcome=None,
                      min_annual_usd=None, max_annual_usd=None):
    results = []
    for d in DATA:
        won = d["lost_on"] is None
        if industry and industry.lower() not in d["industry"].lower():
            continue
        if competitor and not any(competitor.lower() in c.lower() for c in d["primary_competitors"]):
            continue
        if outcome and (outcome == "won") != won:
            continue
        if min_annual_usd is not None and d["deal_size_annual_usd"] < min_annual_usd:
            continue
        if max_annual_usd is not None and d["deal_size_annual_usd"] > max_annual_usd:
            continue
        results.append(d)
    return results


def get_deal(customer):
    for d in DATA:
        if d["customer"].lower() == customer.lower():
            return d
    return {"error": f"No deal found for '{customer}'"}


HANDLERS = {"search_past_deals": search_past_deals, "get_deal": get_deal}


def handle_rpc(msg):
    """Return a JSON-RPC response dict, or None for notifications."""
    method, mid, params = msg.get("method"), msg.get("id"), msg.get("params") or {}
    if mid is None:  # notification, e.g. notifications/initialized
        return None
    if method == "initialize":
        result = {
            "protocolVersion": params.get("protocolVersion", "2025-03-26"),
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "synthetic-crm", "version": "0.1.0"},
        }
    elif method == "tools/list":
        result = {"tools": TOOLS}
    elif method == "tools/call":
        name, args = params.get("name"), params.get("arguments") or {}
        stamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{stamp}] CRM query: {name}({json.dumps(args)})", flush=True)
        if name not in HANDLERS:
            return {"jsonrpc": "2.0", "id": mid,
                    "error": {"code": -32602, "message": f"Unknown tool {name}"}}
        try:
            out = HANDLERS[name](**args)
            result = {"content": [{"type": "text", "text": json.dumps(out, indent=2)}]}
            n = len(out) if isinstance(out, list) else 1
            print(f"           -> {n} record(s)", flush=True)
        except TypeError as e:
            result = {"content": [{"type": "text", "text": f"Bad arguments: {e}"}], "isError": True}
    elif method == "ping":
        result = {}
    else:
        return {"jsonrpc": "2.0", "id": mid,
                "error": {"code": -32601, "message": f"Method not found: {method}"}}
    return {"jsonrpc": "2.0", "id": mid, "result": result}


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path.rstrip("/") != MCP_PATH.rstrip("/"):
            self.send_error(404)
            return
        body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
        batch = body if isinstance(body, list) else [body]
        responses = [r for r in (handle_rpc(m) for m in batch) if r is not None]
        if not responses:
            self.send_response(202)
            self.end_headers()
            return
        payload = json.dumps(responses if isinstance(body, list) else responses[0]).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        if self.path in ("/", "/healthz"):  # health check for the cloud host
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ok")
        else:  # no server-initiated SSE stream
            self.send_error(405)

    def log_message(self, *args):  # silence default per-request logging
        pass


if __name__ == "__main__":
    print(f"Synthetic CRM MCP listening on port {PORT}, path {MCP_PATH} "
          f"({len(DATA)} deals loaded)", flush=True)
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
