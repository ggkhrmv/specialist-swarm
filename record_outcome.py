"""
Stretch S3: tell the Deal Desk how a deal actually went.

The coordinator only knows what it proposed. Whether the deal was won or lost, and
why, is something the deal team knows, so you record it here between runs. It is
written to the memory store as outcomes/<customer>.md. The next session's
coordinator reads it, treats it as ground truth and turns it into a [confirmed]
lesson in playbook.md. $0: this is a direct API write, no session.

Recording the same customer again replaces its outcome.

Usage:
    uv run python record_outcome.py "Acme Corp" "Won. Signed 2026-06-30: ..."

Example outcome for the Acme demo deal (edit to taste):
    "Won. Signed 2026-06-30: 3-year term plus 2-year option, 25% off list (they
    demanded 35%), CPI+2% escalator capped at 4% from year 2, annual upfront Net 60,
    no MFN. Their CDO said our 5-year TCO model beat Snowflake and Fabric once
    Microsoft consulting hours were counted; headline price was never the decider.
    Data-breach liability capped at 24 months of fees; licence-back on custom work
    instead of IP assignment."
"""

from __future__ import annotations

import re
import sys
from datetime import date

from common import get_client, load_state
from stretch_memory import require_store


def outcome_path(customer: str) -> str:
    return "/outcomes/" + re.sub(r"[^a-z0-9]+", "-", customer.lower()).strip("-") + ".md"


def main(argv: list[str] | None = None) -> None:
    argv = argv or []
    if len(argv) != 2 or not all(arg.strip() for arg in argv):
        raise SystemExit('Usage: uv run python record_outcome.py "<Customer>" "<what happened>"')
    customer, outcome = (arg.strip() for arg in argv)

    client = get_client()
    store_id = require_store(load_state())
    memories = client.beta.memory_stores.memories
    path = outcome_path(customer)
    content = (f"# Outcome: {customer}\n\n"
               f"Recorded {date.today().isoformat()} by the deal team. Ground truth: "
               f"this is what happened, not the coordinator's read of it.\n\n{outcome}\n")

    existing = [m for m in memories.list(store_id, path_prefix=path)
                if m.type == "memory" and m.path == path]
    if existing:
        memories.update(existing[0].id, memory_store_id=store_id, content=content)
        print(f"Outcome replaced: {path}")
    else:
        memories.create(store_id, path=path, content=content)
        print(f"Outcome recorded: {path}")
    print("The next run_deal_desk.py session reads it before briefing the specialists.")


if __name__ == "__main__":
    main(sys.argv[1:])
