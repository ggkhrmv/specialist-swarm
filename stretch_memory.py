"""
Stretch S3: memory across deals.

Creates this checkout's memory store (once) and saves its ID in .swarm_state.json.
From then on, run_deal_desk.py attaches the store to every session with read-write
access. The store is mounted under /mnt/memory/, and the coordinator reads it before
it briefs and writes what it learned after it delivers. The instructions for that
are in prompts/coordinator.memory.md and travel with the attachment, so the
coordinator agent doesn't change and nothing else needs re-running.

What the store holds:
    playbook.md              lessons across deals, each citing the deals behind it
    deals/<customer>.md      the coordinator's own notes on each deal it ran
    outcomes/<customer>.md   how a deal actually went, recorded by you (record_outcome.py)

Demo, two deals from different customers:
    uv run python stretch_memory.py
    uv run python run_deal_desk.py                                  # deal 1: Acme
    uv run python record_outcome.py "Acme Corp" "Won. ..."          # what happened
    uv run python run_deal_desk.py --rfp synthetic-data/rfp-kestrel-logistics.md
    uv run python stretch_memory.py --show                          # what it learned

Usage:
    uv run python stretch_memory.py           # create (or reuse) the store and list it
    uv run python stretch_memory.py --show    # also print every memory in full
"""

from __future__ import annotations

import sys

from common import agent_metadata, get_client, load_prompt, load_state, require, save_state

# The mount directory (/mnt/memory/<slug>/) is derived from the name, so keep it fixed.
# The namespace goes in metadata, which is how you tell checkouts' stores apart.
STORE_NAME = "Deal Desk Memory"
STORE_DESCRIPTION = ("The Deal Desk's memory across deals: lessons that hold across deals "
                     "(playbook.md), notes on each past deal (deals/), and how deals "
                     "actually went (outcomes/).")


def memory_resource(state: dict) -> dict | None:
    """The session resource that attaches this checkout's store, or None if there isn't one."""
    store = state.get("memory_store")
    if not store:
        return None
    return {"type": "memory_store", "memory_store_id": store["id"], "access": "read_write",
            "instructions": load_prompt("coordinator.memory")}


def require_store(state: dict) -> str:
    return require(state, "memory_store", "uv run python stretch_memory.py")["id"]


def list_memories(client, store_id: str, full: bool = False) -> list:
    page = client.beta.memory_stores.memories.list(store_id, view="full" if full else "basic")
    return [item for item in page if item.type == "memory"]


def main(argv: list[str] | None = None) -> None:
    argv = argv or []
    client = get_client()
    state = load_state()

    store = state.get("memory_store")
    if store:
        print(f"Memory store already exists: {store['id']} (reusing)")
    else:
        created = client.beta.memory_stores.create(
            name=STORE_NAME, description=STORE_DESCRIPTION, metadata=agent_metadata("memory"))
        store = state["memory_store"] = {"id": created.id}
        save_state(state)
        print(f"Memory store created: {created.id}")
        print("run_deal_desk.py now attaches it to every session (--no-memory to skip).")

    show = "--show" in argv
    memories = list_memories(client, store["id"], full=show)
    if not memories:
        print("\nThe store is empty: the first deal you run fills it.")
        return
    print(f"\n{len(memories)} memories:")
    for memory in sorted(memories, key=lambda m: m.path):
        print(f"  {memory.path:40s} {memory.content_size_bytes:>6d} B  "
              f"updated {memory.updated_at:%Y-%m-%d %H:%M}")
        if show:
            print("    " + (memory.content or "").rstrip().replace("\n", "\n    ") + "\n")


if __name__ == "__main__":
    main(sys.argv[1:])
