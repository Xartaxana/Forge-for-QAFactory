#!/usr/bin/env python3
"""OF4-19 (AR-4, AR-13, AR-15): the readers that took the project from a story folder by depth (`parents[2]`) take it through
`runtime_paths.project_for_task`. One table of layouts built here, two readers:

  - `walk_timing.report`: the project's `qa-factory/config.json` reaches `walk_report` (it prices the walk by it);
  - `gate_brief._proved_warnings`: `host_capabilities.inspect` is asked about the story's own project.

Layouts: the default `<project>/qa-factory/artifacts/<T>`; a project whose config sets `artifact_root: "stories"` (story at
`<project>/stories/<T>`); a story outside any project (every reader answers its "absent" value, never reads from the folder
`parents[2]` would have named). The expectation comes from the layout built here, not from the resolver.
"""
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from harness import check, cleanup, finish, temp_dir  # noqa: E402

sys.path.insert(0, str(harness.SCRIPTS))
import gate_brief  # noqa: E402
import host_capabilities  # noqa: E402
import walk_timing  # noqa: E402

MARK = "of4-19-marker"
S0_FINISHED = "2026-01-01T00:00:00+00:00"
PROVED_AT = "2026-06-01T00:00:00+00:00"
LINE = "host_hooks: unknown"


def same(a, b) -> bool:
    return os.path.normcase(os.path.realpath(str(a))) == os.path.normcase(os.path.realpath(str(b)))


def build(base: Path, where: str, artifact_root) -> Path:
    """A project at `base/proj` whose config carries MARK (and `artifact_root` when given); the story folder under `where`."""
    project = harness.mark_project(base / "proj")
    path = project / "qa-factory" / "config.json"
    cfg = json.loads(path.read_text(encoding="utf-8"))
    cfg["marker"] = MARK
    if artifact_root:
        cfg["artifact_root"] = artifact_root
    path.write_text(json.dumps(cfg), encoding="utf-8")
    story = project / where / "T-1"
    (story / "work" / "walks" / "W1").mkdir(parents=True)
    (story / "work" / "walks" / "W1" / "timing.jsonl").write_text(json.dumps({"item": "a", "index": 0}) + "\n", encoding="utf-8")
    (story / "pipeline.json").write_text(json.dumps({"stages": {"S0": {"finished": S0_FINISHED}}}), encoding="utf-8")
    return story


def build_outside(base: Path) -> Path:
    """A story folder no project holds: deliberately NO marker anywhere above it (a fixture of the 'no project' road)."""
    story = base / "nowhere" / "a" / "b" / "T-1"
    (story / "work" / "walks" / "W1").mkdir(parents=True)
    (story / "work" / "walks" / "W1" / "timing.jsonl").write_text(json.dumps({"item": "a", "index": 0}) + "\n", encoding="utf-8")
    (story / "pipeline.json").write_text(json.dumps({"stages": {"S0": {"finished": S0_FINISHED}}}), encoding="utf-8")
    return story


def timing_config(story: Path) -> dict:
    """The config `walk_timing.report` hands to `walk_report` (replaced by a recorder for the run)."""
    seen = []
    real = walk_timing.walk_report
    walk_timing.walk_report = lambda task_root, walk, timed, config, problems: (
        seen.append(config) or {"walk": walk, "items": 0, "rows": [], "per_item_wall_s": None, "per_item_role_wall_s": None})
    try:
        walk_timing.report(story)
    finally:
        walk_timing.walk_report = real
    return seen[0] if seen else {"__not_called__": True}


def gate_project(story: Path) -> tuple:
    """(lines kept, lines proved, the project `host_capabilities.inspect` was asked about or None)."""
    asked = []
    real_inspect, real_proved = host_capabilities.inspect, host_capabilities.hooks_proved
    host_capabilities.inspect = lambda project, *a, **k: asked.append(Path(project)) or {"role_context": {"observed_at": PROVED_AT}}
    host_capabilities.hooks_proved = lambda answer: True
    try:
        kept, proved = gate_brief._proved_warnings(story, [LINE])
    finally:
        host_capabilities.inspect, host_capabilities.hooks_proved = real_inspect, real_proved
    return kept, proved, (asked[0] if asked else None)


def main() -> None:
    base = temp_dir("qa-of4-19-").resolve()
    cwd0 = os.getcwd()
    rows = (  # (id, where the story sits, artifact_root in the config)
        ("default layout", "qa-factory/artifacts", None),
        ("artifact_root: stories", "stories", "stories"),
    )
    try:
        for n, (label, where, root) in enumerate(rows):
            story = build(base / f"l{n}", where, root)
            project = story.parent.parent.parent if where == "qa-factory/artifacts" else story.parent.parent
            cfg = timing_config(story)
            check(f"walk_timing: {label}: the story's own project config is read", cfg.get("marker") == MARK, f"got {cfg!r}")
            kept, proved, asked = gate_project(story)
            check(f"gate_brief: {label}: the capability proved by the story's own project lifts the line",
                  kept == [] and [p["capability"] for p in proved] == ["host_hooks"], f"kept={kept!r} proved={proved!r}")
            got = None
            if asked is not None:
                got = json.loads((asked / "qa-factory" / "config.json").read_text(encoding="utf-8")).get("marker")
            check(f"gate_brief: {label}: the project asked is the story's own", asked is not None and same(asked, project) and got == MARK,
                  f"asked {asked!r}, expected {project!r}, marker {got!r}")
        story = build_outside(base / "out")
        cfg = timing_config(story)
        check("walk_timing: outside any project: config absent ({}), no traceback", cfg == {}, f"got {cfg!r}")
        kept, proved, asked = gate_project(story)
        check("gate_brief: outside any project: the line stays, nothing is asked", kept == [LINE] and proved == [] and asked is None,
              f"kept={kept!r} proved={proved!r} asked={asked!r}")
    finally:
        os.chdir(cwd0)
        cleanup(base)
    finish("test_project_for_task_readers")


if __name__ == "__main__":
    main()
