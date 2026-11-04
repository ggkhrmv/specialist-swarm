"""
Download every file a Deal Desk session wrote to /mnt/session/outputs/.

Defaults to the last session run_deal_desk.py started; pass a session ID to grab
the files from any older session.

Usage:
    uv run python download_deliverable.py                  # last run
    uv run python download_deliverable.py sesn_01ABC...    # a specific session
"""

import sys

from common import download_outputs, get_client, load_state, session_url


def main() -> None:
    session_id = sys.argv[1].strip() if len(sys.argv) > 1 else load_state().get("last_session_id")
    if not session_id:
        raise SystemExit("No session saved yet.\n"
                         "Usage: uv run python download_deliverable.py <session_id>")

    print(f"Listing files for session {session_id}...")
    if not download_outputs(get_client(), session_id):
        print(f"No files found. Check the session trace:\n  {session_url(session_id)}")


if __name__ == "__main__":
    main()
