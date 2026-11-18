"""reread: a part of test_story_sides_driver.py, split by tools/test_split.py (TD-11c). The shared helpers are in story_sides_driver_common."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
sys.path.insert(0, str(harness.SCRIPTS))
from story_sides_common import SUBSTITUTED  # noqa: E402
import project_knowledge as PK
from story_run_common import eq as check_eq   # this one takes a detail text (the process output) as a fourth argument
from story_run_common import s0_answer, s0_pipeline, s0_project, s0_run, s0_state
from story_sides_driver_common import break_registry, product_default, stands, strip  # noqa: E402


# PC3-1 (t-057 N1, N6): the re-read after a registry repair records what S0 would have recorded with a readable registry -
# same merge (registry + launch words + the person's answers), same `product` default. Ids name the case in every label.
def seed_backend_theirs(root):
    PK.record(root, key=PK.SIDES_KEY, environment="", element="backend", state="known", scope="project",
              value={"deliverable": False, "settles_by": "platform team"}, words="theirs", source="person", story="S-0", by="conductor")
    PK.record(root, key=PK.STAND_SIDES_KEY, environment="dev", element="backend", state="known", scope="stand",
              value={"reality": SUBSTITUTED}, words="the stand", source="person", story="S-0", by="conductor")


def reread_launch_words():
    root, task_root, env = s0_project("PROJ-1", config=stands)
    try:
        seed_backend_theirs(root)
        control = s0_run(root, env, "PROJ-1", "--side", "ui=real")
        control_sides = strip(s0_pipeline(task_root)["sides"])
        check_eq("reread-launch-words (control): a readable registry at S0 with `--side ui=real` records ui, backend, and no `product`",
                 (control.returncode, sorted(control_sides)), (0, ["backend", "ui"]), control.stdout[-400:] + control.stderr[-300:])
    finally:
        harness.cleanup(root)
    root, task_root, env = s0_project("PROJ-1", config=stands)
    try:
        break_registry(root)
        s0_run(root, env, "PROJ-1", "--side", "ui=real")
        out = s0_run(root, env, "PROJ-1")
        pipeline = s0_pipeline(task_root)
        check_eq("reread-still-unreadable: the registry still broken keeps the mark and records no side",
                 (out.returncode, bool(pipeline.get("sides_unknown")), "sides" in pipeline), (0, True, False), out.stdout[-400:] + out.stderr[-300:])
        PK.record_path(root).unlink()
        seed_backend_theirs(root)
        out = s0_run(root, env, "PROJ-1")
        pipeline = s0_pipeline(task_root)
        check_eq("reread-launch-words: the launch's `--side ui=real` survives the repair, so the re-read equals S0 with a readable registry",
                 (out.returncode, bool(pipeline.get("sides_unknown")), strip(pipeline.get("sides") or {})), (0, False, control_sides),
                 out.stdout[-400:] + out.stderr[-300:])
    finally:
        harness.cleanup(root)


def reread_person_answer():
    root, task_root, env = s0_project("PROJ-1", config=stands)
    try:
        break_registry(root)
        s0_run(root, env, "PROJ-1", "--side", "ui=substituted")      # the registry is unreadable: the question stands
        s0_answer(root, env, "PROJ-1", "another team's", "--side", "ui=real")    # the person said `another team's` before the repair
        PK.record_path(root).unlink()
        seed_backend_theirs(root)
        out = s0_run(root, env, "PROJ-1")
        sides = strip(s0_pipeline(task_root).get("sides") or {})
        check_eq("reread-person-answer: an answer given before the repair reaches the record (ui another team's, source person) and `product` follows",
                 (out.returncode, sides.get("ui"), sides.get("product")),
                 (0, {"reality": "real", "deliverable": False, "source": "person"}, product_default), out.stdout[-400:] + out.stderr[-300:])
    finally:
        harness.cleanup(root)


def reread_case_twin():
    root, task_root, env = s0_project("PROJ-1", config=stands)
    try:
        break_registry(root)
        s0_run(root, env, "PROJ-1", "--side", "UI=real")     # names are empty while the registry is unreadable, so C15 cannot fire
        PK.record_path(root).unlink()
        PK.record(root, key=PK.SIDES_KEY, environment="", element="ui", state="known", scope="project",
                  value={"deliverable": False, "settles_by": "web team"}, words="theirs", source="person", story="S-0", by="conductor")
        out = s0_run(root, env, "PROJ-1")
        pipeline = s0_pipeline(task_root)
        log = (root / "stub-log.jsonl").read_text(encoding="utf-8") if (root / "stub-log.jsonl").is_file() else ""
        check_eq("reread-case-twin: `--side UI=real` beside a registry `ui` is the C15 refusal as at S0 (the mark stays, no side is written, "
                 "the name is dropped from the kept launch)",
                 ("side names are compared exactly" in out.stdout + out.stderr + log, bool(pipeline.get("sides_unknown")), "sides" in pipeline,
                  (s0_state(task_root).get("launch") or {}).get("side")),
                 (True, True, False, {}), out.stdout[-400:] + out.stderr[-300:] + log[-400:])
    finally:
        harness.cleanup(root)


def main() -> None:
    reread_launch_words()
    reread_person_answer()
    reread_case_twin()
    harness.finish("test_story_sides_driver_reread")


# split: runner piece 1
# split: runner piece 1
if __name__ == "__main__":
    main()
