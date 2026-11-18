"""unreadable: a part of test_story_sides_driver.py, split by tools/test_split.py (TD-11c). The shared helpers are in story_sides_driver_common."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
sys.path.insert(0, str(harness.SCRIPTS))
from story_sides_common import SUBSTITUTED  # noqa: E402
import project_knowledge as PK
from story_run_common import eq as check_eq   # this one takes a detail text (the process output) as a fourth argument
from story_run_common import s0_pipeline, s0_project, s0_run, s0_state
from story_sides_driver_common import break_registry, product_default, repos, stands  # noqa: E402


def unreadable_registry():
    root, task_root, env = s0_project("PROJ-1", config=repos)
    try:
        PK.record_path(root).parent.mkdir(parents=True, exist_ok=True)
        PK.record_path(root).write_text("{not json", encoding="utf-8")
        out = s0_run(root, env, "PROJ-1", "--side", "ui=real")
        pipeline = s0_pipeline(task_root)
        check_eq("an unreadable registry: S0 ends with pipeline.sides_unknown written and no side recorded as real",
                 (out.returncode, sorted(pipeline.get("sides_unknown") or {}), "sides" in pipeline), (0, ["at", "why"], False),
                 out.stdout[-400:] + out.stderr[-300:])
        first_at = pipeline["sides_unknown"]["at"]
        out = s0_run(root, env, "PROJ-1")
        check_eq("F1 (b): the file still unreadable on the relaunch: the mark is kept, its `at` unchanged",
                 (out.returncode, (s0_pipeline(task_root).get("sides_unknown") or {}).get("at")), (0, first_at),
                 out.stdout[-400:] + out.stderr[-300:])
    finally:
        harness.cleanup(root)


def f1_repaired_registry():
    root, task_root, env = s0_project("PROJ-1", config=stands)
    try:
        PK.record_path(root).parent.mkdir(parents=True, exist_ok=True)
        PK.record_path(root).write_text("{not json", encoding="utf-8")
        s0_run(root, env, "PROJ-1")
        check_eq("F1 (a): S0 over an unreadable registry gives sides_unknown", bool(s0_pipeline(task_root).get("sides_unknown")), True)
        PK.record_path(root).unlink()
        PK.record(root, key=PK.SIDES_KEY, environment="", element="backend", state="known", scope="project",
                  value={"deliverable": False, "settles_by": "platform team"}, words="theirs", source="person", story="S-0", by="conductor")
        PK.record(root, key=PK.STAND_SIDES_KEY, environment="dev", element="backend", state="known", scope="stand",
                  value={"reality": SUBSTITUTED}, words="the stand", source="person", story="S-0", by="conductor")
        out = s0_run(root, env, "PROJ-1")
        pipeline = s0_pipeline(task_root)
        entry = (pipeline.get("sides") or {}).get("backend") or {}
        check_eq("F1 (a): the repaired registry on the relaunch clears the mark and records the substituted side (source registry)",
                 (out.returncode, bool(pipeline.get("sides_unknown")), entry.get("reality"), entry.get("deliverable"), entry.get("source")),
                 (0, False, SUBSTITUTED, False, "registry"), out.stdout[-400:] + out.stderr[-300:])
        check_eq("F1 (a): ... and the re-read carries the implicit `product` as the default, as S0 spells it (K-b2, AR-19)",
                 {k: v for k, v in ((pipeline.get("sides") or {}).get("product") or {}).items() if k != "at"}, product_default)
        check_eq("... and a third launch with no mark does nothing more (the record is as it was)", (s0_run(root, env, "PROJ-1").returncode,
                 s0_pipeline(task_root)["sides"]), (0, pipeline["sides"]))
    finally:
        harness.cleanup(root)


def w2_no_deliverable():
    # t-2277 batch 2b W2 (4): a relaunch re-read of a side with NO recorded deliverable answer keeps the default `ours` (the owner accepted it)
    root, task_root, env = s0_project("PROJ-1", config=stands)
    try:
        PK.record_path(root).parent.mkdir(parents=True, exist_ok=True)
        PK.record_path(root).write_text("{not json", encoding="utf-8")
        s0_run(root, env, "PROJ-1")
        PK.record_path(root).unlink()
        PK.record(root, key=PK.STAND_SIDES_KEY, environment="dev", element="backend", state="known", scope="stand",
                  value={"reality": SUBSTITUTED}, words="the stand", source="person", story="S-0", by="conductor")
        out = s0_run(root, env, "PROJ-1")
        pipeline = s0_pipeline(task_root)
        entry = (pipeline.get("sides") or {}).get("backend") or {}
        check_eq("W2 (4): the re-read records the stand's reality and writes NO deliverable for a side nobody answered (source registry)",
                 (out.returncode, bool(pipeline.get("sides_unknown")), entry.get("reality"), "deliverable" in entry, entry.get("source")),
                 (0, False, SUBSTITUTED, False, "registry"), out.stdout[-400:] + out.stderr[-300:])
        import contract
        check_eq("... and the readers take it as ours (default true), the question is not raised by the re-read",
                 (contract.story_sides(pipeline)["backend"]["deliverable"], s0_state(task_root).get("s0_block")), (True, None))
    finally:
        harness.cleanup(root)


def reread_lifts_mark():
    for case, rows_after in (("reread-all-real-registry", (("ui", True, ""),)), ("reread-empty-registry", ())):
        root, task_root, env = s0_project("PROJ-1", config=stands)
        try:
            break_registry(root)
            s0_run(root, env, "PROJ-1")
            PK.record_path(root).unlink()
            for name, deliverable, settles_by in rows_after:
                PK.record(root, key=PK.SIDES_KEY, environment="", element=name, state="known", scope="project",
                          value={"deliverable": deliverable, "settles_by": settles_by}, words="ours", source="person", story="S-0", by="conductor")
            out = s0_run(root, env, "PROJ-1")
            pipeline = s0_pipeline(task_root)
            check_eq(f"{case}: no non-real side and no reference: the mark lifts, no side (`product` included) is written",
                     (out.returncode, bool(pipeline.get("sides_unknown")), "sides" in pipeline), (0, False, False), out.stdout[-400:] + out.stderr[-300:])
        finally:
            harness.cleanup(root)


def main() -> None:
    unreadable_registry()
    f1_repaired_registry()
    w2_no_deliverable()
    reread_lifts_mark()
    harness.finish("test_story_sides_driver_unreadable")


# split: runner piece 1
# split: runner piece 1
if __name__ == "__main__":
    main()
