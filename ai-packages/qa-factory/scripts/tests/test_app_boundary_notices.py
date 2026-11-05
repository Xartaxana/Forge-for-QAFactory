#!/usr/bin/env python3
"""RH1-5 B8: `guard_app_under_test` says its advice to the person through `hooklib.person_signal` (a `hook_signal` line in the
journal), never to a silent stderr at exit 0. H4 (protected paths not on disk), H5 (test_locations could not be checked), H6
(test_locations problems), H7 (protected_app_paths empty), H8 (test-path pass recorded), H9 (stand-gap pass recorded). The
blocks still block (control)."""
import contextlib
import io
import json
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import SCRIPTS, check, check_eq, check_in, cleanup, finish, temp_project, use_project  # noqa: E402

sys.path.insert(0, str(SCRIPTS))
import guard_app_under_test as GA  # noqa: E402
import hooklib  # noqa: E402
import runtime_paths as RP  # noqa: E402


def write_config(root: Path, protected, locations=None) -> dict:
    cfg = {"app_root": ".", "tests_root": "tests", "protected_app_paths": list(protected)}
    if locations is not None:
        cfg["test_locations"] = locations
    (root / "qa-factory" / "config.json").write_text(json.dumps(cfg), encoding="utf-8")
    return cfg


def signals(root: Path) -> list:
    path = RP.record(root, "journal.jsonl")
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()] if path.is_file() else []
    return [r for r in rows if r.get("event") == "hook_signal"]


RUN = uuid.uuid4().hex[:8]       # the once-per-session marker lives in the OS temp: a fresh session id per run


def call(root: Path, cfg: dict, tool="Write", path="tests/x.py", sid="sess-b"):
    event = {"hook_event_name": "PreToolUse", "session_id": f"{sid}-{RUN}", "cwd": str(root), "tool_name": tool,
             "tool_input": {"file_path": str(root / path)}}
    err = io.StringIO()
    code = None
    with contextlib.redirect_stderr(err):
        try:
            GA.check(event, cfg)
        except SystemExit as exc:
            code = exc.code
    return code, err.getvalue(), event


def main() -> None:
    root = temp_project("qa-boundary-notices-")
    try:
        use_project(root)
        # H4: a protected path that is not on disk
        cfg = write_config(root, ["no_such_dir"])
        code, err, event = call(root, cfg, sid="h4")
        rows = [r for r in signals(root) if "protected paths not found" in r["notes"]]
        check_eq("H4: one config signal, nothing on stderr", (len(rows), rows[0]["kind"] if rows else None, err), (1, "config", ""))
        call(root, cfg, sid="h4")
        check_eq("H4: once per session: the second call adds none", len([r for r in signals(root) if "protected paths not found" in r["notes"]]), 1)
        # H7: protected_app_paths empty (the config exists)
        cfg = write_config(root, [])
        code, err, _e = call(root, cfg, sid="h7")
        rows = [r for r in signals(root) if "protected_app_paths is empty" in r["notes"]]
        check_eq("H7: a config signal, nothing on stderr, no block", (len(rows), err, code), (1, "", None))
        # H6 / H5: test_locations
        import test_locations as TL
        write_config(root, ["src"], [""])
        cfg = write_config(root, ["src"], [""])
        (root / "src").mkdir(exist_ok=True)
        code, err, _e = call(root, cfg, sid="h6")
        rows = [r for r in signals(root) if "test_locations in qa-factory/config.json" in r["notes"]]
        check_eq("H6: the problems of test_locations are a config signal; nothing on stderr", (len(rows) >= 1, err), (True, ""))
        real = TL.location_problems
        TL.location_problems = lambda *a, **k: (_ for _ in ()).throw(RuntimeError("cannot check"))
        try:
            code, err, _e = call(root, cfg, sid="h5")
        finally:
            TL.location_problems = real
        rows = [r for r in signals(root) if "could not be checked (RuntimeError)" in r["notes"]]
        check_eq("H5: a location check that raised is SAID (config signal naming the exception type)", (len(rows), err), (1, ""))
        # blocks still block (control): a write inside a protected path
        cfg = write_config(root, ["src"])
        code, err, _e = call(root, cfg, path="src/app.py", sid="ctl")
        check_eq("control: a write into a protected application path still blocks (exit 2)", code, 2)
        check_in("control: with the boundary text on stderr (a refusal is shown at exit 2)", "APP-UNDER-TEST BOUNDARY", err)
        # H8 / H9: the pass records go to the journal, not to stderr
        import test_path_grants
        real_grant = test_path_grants.grant_for
        test_path_grants.grant_for = lambda *a, **k: {"pattern": "src/**", "words": "ok go on", "at": "2026-10-28T10:00:00"}
        real_ticket, real_story = GA._automator_story, GA._story_pipeline
        GA._automator_story = lambda event: ("QA-B1", {})
        GA._story_pipeline = lambda event, ticket: {}
        try:
            (root / "src").mkdir(exist_ok=True)
            (root / "src" / "app.py").write_text("old\n", encoding="utf-8")
            event = {"hook_event_name": "PreToolUse", "session_id": "h8", "cwd": str(root), "tool_name": "Write",
                     "agent_type": "qa-factory:qa-automator",
                     "tool_input": {"file_path": str(root / "src/app.py"), "content": "new\n"}}
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                passed, added = GA.permission_pass(str(root / "src/app.py").replace("\\", "/"), "src/app.py", "Write", event, cfg, root / "src/app.py")
        finally:
            test_path_grants.grant_for = real_grant
            GA._automator_story, GA._story_pipeline = real_ticket, real_story
        rows = [r for r in signals(root) if r["kind"] == "pass_recorded"]
        check_eq("H8: a permission pass is recorded as a pass_recorded signal on the story, nothing on stderr",
                 (passed, len(rows), rows[-1]["task"] if rows else None, err.getvalue()), (True, 1, "QA-B1", ""))
        import stand_gaps
        real_apply, real_used, real_rec = stand_gaps.apply_grant, stand_gaps.grant_used, stand_gaps.record_grant
        stand_gaps.apply_grant = lambda *a, **k: {"gap": "PC-1", "task": "QA-B2", "file": "src/app.py", "words": "apply x", "stage": "S5"}
        stand_gaps.grant_used = lambda *a, **k: None
        stand_gaps.record_grant = lambda *a, **k: None
        try:
            event = {"hook_event_name": "PreToolUse", "session_id": "h9", "cwd": str(root), "tool_name": "Write", "tool_input": {}}
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                passed = GA.stand_gap_pass(str(root / "src/app.py"), "src/app.py", "Write", event, cfg)
        finally:
            stand_gaps.apply_grant, stand_gaps.grant_used, stand_gaps.record_grant = real_apply, real_used, real_rec
        rows = [r for r in signals(root) if r["kind"] == "pass_recorded" and r["task"] == "QA-B2"]
        check_eq("H9: a stand-gap pass is recorded as a signal, nothing on stderr", (passed, len(rows), err.getvalue()), (True, 1, ""))
        check("no use of the silent warning left in the module", "warn_once" not in Path(GA.__file__).read_text(encoding="utf-8"))
    finally:
        cleanup(root)
        hooklib._PROJECT_ROOT_CACHE = None
    finish("test_app_boundary_notices")


if __name__ == "__main__":
    main()
