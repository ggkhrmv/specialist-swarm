"""
Run every setup step, in order:

    1. setup_environment.py   cloud environment for the sessions
    2. upload_skills.py       custom skills -> Skills API
    3. create_specialists.py  four specialists, each with its skill attached
    4. create_coordinator.py  the Senior Partner, with the roster + docx skill

Every step is safe to re-run (it reuses or updates what it made before), so this
is also how you push prompt or skill edits. Then run:  uv run python run_deal_desk.py

Usage:
    uv run python setup_swarm.py
"""

import create_coordinator
import create_specialists
import setup_environment
import upload_skills

STEPS = [
    ("Environment", setup_environment.main),
    ("Skills", upload_skills.main),
    ("Specialists", create_specialists.main),
    ("Coordinator", create_coordinator.main),
]


def main() -> None:
    for number, (title, step) in enumerate(STEPS, start=1):
        print(f"\n── {number}/{len(STEPS)} {title} " + "─" * 40)
        step()
    print("\nSwarm ready. Run it with:  uv run python run_deal_desk.py")


if __name__ == "__main__":
    main()
