"""table: a part of test_story_sides_driver.py, split by tools/test_split.py (TD-11c). The shared helpers are in story_sides_driver_common."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
sys.path.insert(0, str(harness.SCRIPTS))
from story_sides_common import SUBSTITUTED, copy_registry  # noqa: E402
import project_knowledge as PK
from story_run_common import eq as check_eq   # this one takes a detail text (the process output) as a fourth argument
from story_run_common import s0_answer, s0_pipeline, s0_project, s0_run, s0_state
from story_sides_driver_common import product_default, repos, strip  # noqa: E402


ours, theirs = (("ui", True, ""),), (("backend", False, "platform team"),)


# id, registry rows (name, deliverable, settles_by), launch flags, the answer to sides.deliverable (None: not asked), `product`, `backend`
rows = (
    ("own-answer", (), ("--side", "backend=substituted"), "another team's", product_default, (SUBSTITUTED, False, "")),
    ("other-story-row", theirs, ("--side", "backend=substituted"), None, product_default, (SUBSTITUTED, False, "platform team")),
    ("real-side-named", ours, ("--side", "backend=substituted"), "another team's", None, None),
    ("other-team-real", (("ui", False, ""),), ("--side", "backend=substituted"), "another team's", product_default, None),
    ("reference-only", (), ("--reference", "ui=old"), None, None, None),
    ("second-story", (), ("--side", "backend=substituted"), "another team's", product_default, (SUBSTITUTED, False, "")),
)


def story_one(row, *extra):
    """A fresh project, the registry rows seeded, the launch and the answer; `(root, task_root, env, out)` - the caller cleans up."""
    root, task_root, env = s0_project("PROJ-1", config=repos)
    for name, deliverable, settles_by in row[1]:
        PK.record(root, key=PK.SIDES_KEY, environment="", element=name, state="known", scope="project",
                  value={"deliverable": deliverable, "settles_by": settles_by}, words="the person said", source="person", story="S-0", by="conductor")
    out = s0_run(root, env, "PROJ-1", *extra, *row[2])
    if row[3]:
        out = s0_answer(root, env, "PROJ-1", row[3], *extra)
    return root, task_root, env, out


def sides_table():
    """t-2181 PC-1b in the driver at S0: the second story is not asked; the answer is recorded once (writer 2); a no_trace story
    keeps it in `pipeline.sides` with the line; C15; an unreadable registry is `sides_unknown`."""
    for row in rows:
        name, found = row[0], {}
        for mode, extra in (("traced", ()), ("no-trace", ("--no-trace",))):
            if name == "second-story" and extra:
                continue
            root, task_root, env, out = story_one(row, *extra)
            try:
                found[mode] = strip(s0_pipeline(task_root)["sides"])
                check_eq(f"{name} ({mode}): S0 ends and nothing is left asked", (out.returncode, s0_state(task_root).get("s0_block")), (0, None),
                         out.stdout[-500:] + out.stderr[-300:])
                check_eq(f"{name} ({mode}): `product` is as the rule says", found[mode].get("product"), row[4])
                if row[5]:
                    got = found[mode]["backend"]
                    check_eq(f"{name} ({mode}): the registry's deliverable and settles_by are recorded with the launch's reality",
                             (got["reality"], got["deliverable"], got.get("settles_by", "")), row[5])
                if name == "second-story":      # story 2 of the project: the same launch, a copy of the registry, nothing asked
                    root2, task_root2, env2 = s0_project("PROJ-2", config=repos)
                    try:
                        copy_registry(root, root2)
                        out2 = s0_run(root2, env2, "PROJ-2", *row[2])
                        second = strip(s0_pipeline(task_root2)["sides"])
                        check_eq(f"{name}: story 2 is not asked", (out2.returncode, s0_state(task_root2).get("s0_block")), (0, None),
                                 out2.stdout[-500:] + out2.stderr[-300:])
                        check_eq(f"{name}: story 2 carries story 1's `product`, whole", second.get("product"), found[mode]["product"])
                        check_eq(f"{name}: story 2's backend equals story 1's on reality and deliverable (its source differs by design)",
                                 {k: second["backend"][k] for k in ("reality", "deliverable")},
                                 {k: found[mode]["backend"][k] for k in ("reality", "deliverable")})
                    finally:
                        harness.cleanup(root2)
            finally:
                harness.cleanup(root)
        if "no-trace" in found:
            check_eq(f"{name}: the traced and the `--no-trace` records are equal without `at`", found["traced"], found["no-trace"])


def main() -> None:
    sides_table()
    harness.finish("test_story_sides_driver_table")


# split: runner piece 1
# split: runner piece 1
if __name__ == "__main__":
    main()
