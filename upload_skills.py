"""
Step 2 — upload the Deal Desk skills through the Skills API.

Only the skills an agent uses are uploaded: the keys of SKILL_OWNERS in
create_specialists.py, which attaches each one to the specialist that owns that
domain. The rest of skills/ (the asset-forge suite, see README) is a library for
Claude Code and stays out of the cloud setup until someone maps it to an agent.

Every checkout uploads its OWN copy of each skill and tracks its ID in
.swarm_state.json, so a teammate editing a SKILL.md in their worktree never
changes the skill your agents use. Display names carry the checkout's namespace
so you can tell the copies apart in the Console (display names aren't unique).

Safe to re-run: an unchanged skill is reused; a skill whose files changed gets a
new version, which agents pinned to "latest" pick up in their next session.

Usage:
    uv run python upload_skills.py
"""

from anthropic.lib import files_from_dir

from common import HERE, NAMESPACE, get_client, load_state, save_state, sha256_of
from create_specialists import SKILL_OWNERS

SKILLS_DIR = HERE / "skills"


def main() -> None:
    client = get_client()
    state = load_state()
    saved: dict = state.setdefault("skills", {})

    missing = [name for name in SKILL_OWNERS if not (SKILLS_DIR / name / "SKILL.md").exists()]
    if missing:
        raise SystemExit(f"SKILL_OWNERS maps skills with no skills/<name>/SKILL.md: {missing}")

    for name in sorted(SKILL_OWNERS):
        skill_dir = SKILLS_DIR / name
        digest = sha256_of(skill_dir)
        known = saved.get(name)

        if known and known["sha256"] == digest:
            print(f"  {name:20s} unchanged  ({known['id']})")
            continue

        if known:
            client.skills.versions.create(known["id"], files=files_from_dir(str(skill_dir)))
            skill_id = known["id"]
            print(f"  {name:20s} new version uploaded  ({skill_id})")
        else:
            skill = client.skills.create(display_name=f"{name} · {NAMESPACE}",
                                         files=files_from_dir(str(skill_dir)))
            skill_id = skill.id
            print(f"  {name:20s} uploaded  ({skill_id})")

        saved[name] = {"id": skill_id, "sha256": digest}
        save_state(state)

    print(f"\n{len(saved)} custom skill(s) ready. Next: uv run python create_specialists.py")


if __name__ == "__main__":
    main()
