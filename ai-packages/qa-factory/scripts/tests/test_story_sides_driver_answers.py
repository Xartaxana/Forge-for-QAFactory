"""answers: a part of test_story_sides_driver.py, split by tools/test_split.py (TD-11c). The shared helpers are in story_sides_driver_common."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from harness import check  # noqa: E402
sys.path.insert(0, str(harness.SCRIPTS))
from story_sides_common import ABSENT, SUBSTITUTED  # noqa: E402
import project_knowledge as PK
from story_run_common import eq as check_eq   # this one takes a detail text (the process output) as a fourth argument
from story_run_common import s0_answer, s0_pipeline, s0_project, s0_run, s0_state, stub_calls
from story_sides_driver_common import product_default, repos, stands  # noqa: E402


def writer_two():
    root, task_root, env = s0_project("PROJ-1", config=repos)
    try:
        s0_run(root, env, "PROJ-1", "--side", "backend=substituted")
        out = s0_answer(root, env, "PROJ-1", "another team's")
        row = PK.state(root, PK.SIDES_KEY, "", "backend")["row"] or {}
        check_eq("writer 2: the answer is a project row, by driver, source person, state known",
                 (out.returncode, row.get("value"), (row.get("provenance") or {}).get("by"), (row.get("provenance") or {}).get("source"), row.get("state")),
                 (0, {"deliverable": False, "settles_by": ""}, "driver", "person", "known"))
    finally:
        harness.cleanup(root)


def no_trace_answer():
    root, task_root, env = s0_project("PROJ-1", config=repos)
    try:
        s0_run(root, env, "PROJ-1", "--no-trace", "--side", "backend=substituted")
        out = s0_answer(root, env, "PROJ-1", "ours", "--no-trace")
        check_eq("a no_trace story keeps the answer in pipeline.sides (source person)",
                 (out.returncode, {k: s0_pipeline(task_root)["sides"]["backend"][k] for k in ("deliverable", "source")}),
                 (0, {"deliverable": True, "source": "person"}), out.stdout[-400:] + out.stderr[-300:])
        line = "your answer about backend was kept for this story only (an experiment leaves no trace)"
        check("... says the one line", line in out.stdout, out.stdout[-400:])
        check("... and the line is a warning of the story's record too (F5)", line in s0_pipeline(task_root)["warnings"],
              s0_pipeline(task_root)["warnings"])
        check_eq("... and records nothing in the registry", PK.record_path(root).exists(), False)
    finally:
        harness.cleanup(root)


def c15_spelling():
    root, task_root, env = s0_project("PROJ-1", config=repos)
    try:
        PK.record(root, key=PK.SIDES_KEY, environment="", element="ui", state="known", scope="project", value={"deliverable": True},
                  words="ours", source="person", story="S-0", by="conductor")
        out = s0_run(root, env, "PROJ-1", "--side", "UI=substituted")
        check_eq("C15: `UI` beside a recorded `ui` is refused, S0 is not recorded", (task_root / "pipeline.json").exists(), False,
                 out.stdout[-400:] + out.stderr[-300:])
        # the guard hands a refusal to the conductor, so the refusal text is the prompt of the conductor call (no default that holds the name)
        prompts = [call.get("prompt", "") for call in stub_calls(root) if call.get("kind") == "conductor"]
        check("... the refusal (the conductor's prompt) names the recorded name and the flag that is the door",
              any("`ui`" in text and "Start again with --side" in text for text in prompts), prompts[-1][-600:] if prompts else "no conductor call")
        check_eq("... the offending name is not kept in launch (the corrected flag is the door)",
                 "UI" in ((s0_state(task_root).get("launch") or {}).get("side") or {}), False)
        out = s0_run(root, env, "PROJ-1", "--side", "ui=real")
        check_eq("... and the recorded spelling goes through", (out.returncode, (task_root / "pipeline.json").exists()), (0, True),
                 out.stdout[-400:] + out.stderr[-300:])
    finally:
        harness.cleanup(root)


def product_default_fresh():
    import contract
    first, second = contract.product_default_entry(), contract.product_default_entry()
    first["settles_by"] = "x"
    check_eq("product_default_entry: the values, and a fresh dict on every call", (second, first is second), (product_default, False))


def w2_later_word():
    # t-2277 batch 2b W2 (1, 2): the answer is the PROJECT's (a registry row) and a later word overwrites it; the next story reads the latest
    root, task_root, env = s0_project("PROJ-1", config=repos)
    try:
        PK.record(root, key=PK.SIDES_KEY, environment="", element="backend", state="known", scope="project", value={"deliverable": False, "settles_by": ""},
                  words="another team's", source="person", story="S-0", by="driver")
        PK.record(root, key=PK.SIDES_KEY, environment="", element="backend", state="known", scope="project", value={"deliverable": True, "settles_by": ""},
                  words="no, this backend is ours", source="person", story="S-1", by="conductor")
        out = s0_run(root, env, "PROJ-1", "--side", "backend=substituted")
        entry = s0_pipeline(task_root)["sides"]["backend"]
        check_eq("W2 (2): the later word overwrites: the story reads `ours`, and is asked nothing",
                 (out.returncode, s0_state(task_root).get("s0_block"), entry["deliverable"]), (0, None, True), out.stdout[-400:] + out.stderr[-300:])
        row = PK.state(root, PK.SIDES_KEY, "", "backend")["row"]
        check_eq("... the registry's latest row carries the person's words, who and when",
                 (row["provenance"]["words"], row["provenance"]["story"], bool(row["at"])), ("no, this backend is ours", "S-1", True))
    finally:
        harness.cleanup(root)


def f2_stand_selected():
    root, task_root, env = s0_project("PROJ-1", config=stands)
    try:
        PK.record(root, key=PK.SIDES_KEY, environment="", element="backend", state="known", scope="project",
                  value={"deliverable": False, "settles_by": ""}, words="theirs", source="person", story="S-0", by="conductor")
        PK.record(root, key=PK.STAND_SIDES_KEY, environment="dev", element="backend", state="known", scope="stand",
                  value={"reality": SUBSTITUTED}, words="the stand", source="person", story="S-0", by="conductor")
        out = s0_run(root, env, "PROJ-1")
        pipeline = s0_pipeline(task_root)
        entry = (pipeline.get("sides") or {}).get("backend") or {}
        check_eq("F2: no --env, the stand `dev` selected: its substituted row reaches pipeline.sides (never read as real)",
                 (out.returncode, pipeline.get("environment"), entry.get("reality"), entry.get("deliverable")),
                 (0, "dev", SUBSTITUTED, False), out.stdout[-500:] + out.stderr[-300:])
        check("F6: no side of the story is a real side of this team (backend is substituted, another team's), so `product` is implied in pipeline.sides",
              "product" in (pipeline.get("sides") or {}), sorted(pipeline.get("sides") or {}))
    finally:
        harness.cleanup(root)


def f2_stand_only_asked():
    root, task_root, env = s0_project("PROJ-1", config=stands)
    try:
        PK.record(root, key=PK.STAND_SIDES_KEY, environment="dev", element="backend", state="known", scope="stand",
                  value={"reality": ABSENT}, words="the stand", source="person", story="S-0", by="conductor")
        out = s0_run(root, env, "PROJ-1")
        check_eq("F2 sibling: a side known only from the selected stand's row is asked sides.deliverable (never silently ours)",
                 (out.returncode != 0 or s0_state(task_root).get("s0_block") is not None, (task_root / "pipeline.json").exists(),
                  str(s0_state(task_root).get("s0_block"))), (True, False, "deliverable:backend"), out.stdout[-500:] + out.stderr[-300:])
    finally:
        harness.cleanup(root)


def main() -> None:
    writer_two()
    no_trace_answer()
    c15_spelling()
    product_default_fresh()
    w2_later_word()
    f2_stand_selected()
    f2_stand_only_asked()
    harness.finish("test_story_sides_driver_answers")


# split: runner piece 1
# split: runner piece 1
if __name__ == "__main__":
    main()
