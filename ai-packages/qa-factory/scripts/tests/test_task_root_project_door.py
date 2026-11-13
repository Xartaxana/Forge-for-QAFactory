#!/usr/bin/env python3
"""A script that takes `--task-root` finds the project of the story by the one walk (`runtime_paths.nearest_project`), never by
`parents[n]` arithmetic (t-217, AR-13; sibling of OF4-27 / B-348). One table: every site x two layouts (`artifact_root:
qa-artifacts`, the default) derives `<project>/qa-factory` (or the project); a story under no project keeps the old arithmetic."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import SCRIPTS, check_eq, cleanup, finish, temp_dir, temp_project  # noqa: E402

sys.path.insert(0, str(SCRIPTS))
import branch_accounting  # noqa: E402
import judge_diff  # noqa: E402
import judge_results  # noqa: E402
import walk_timing  # noqa: E402


def _cost_story(home: Path, task: Path):
    cost = home / "state" / "cost"
    cost.mkdir(parents=True, exist_ok=True)
    (cost / "conductor.json").write_text(json.dumps({"by_task": {task.name: 1}, "requests": [
        {"valuation": {"pricing_coverage": "complete", "subtotal_usd": 1.25}}]}), encoding="utf-8")
    return task


def _diff_task(home: Path, task: Path):
    (home / "d").mkdir(exist_ok=True)
    (home / "d" / "x.diff").write_text("diff\n", encoding="utf-8")
    return task


# site -> (what it derives from a story folder, expected from (home, project))
SITES = {
    "judge_results._project_bugs_dir:275": (lambda t: judge_results._project_bugs_dir(t), lambda h, p: h / "bugs", None),
    "judge_diff._diff_files:68": (lambda t: judge_diff._diff_files({"implementations": [{"diff_path": "d/x.diff"}]}, t),
                                  lambda h, p: [h / "d" / "x.diff"], _diff_task),
    "walk_timing.walk_report:171": (lambda t: walk_timing._home_and_project(t), lambda h, p: (h, p), None),
    "walk_timing.conductor_spend:214": (lambda t: walk_timing.conductor_spend(t), lambda h, p: 1.25, _cost_story),
    "branch_accounting.story_home:2335": (lambda t: branch_accounting.story_home(t), lambda h, p: h, None),
}


def main() -> None:
    for layout, artifact_root in (("artifact_root: qa-artifacts", "qa-artifacts"), ("default layout", None)):
        root = temp_project("qa-factory-t217-")
        try:
            config = root / "qa-factory" / "config.json"
            cfg = json.loads(config.read_text(encoding="utf-8-sig"))
            cfg.pop("artifact_root", None)
            if artifact_root:
                cfg["artifact_root"] = artifact_root
            config.write_text(json.dumps(cfg), encoding="utf-8")
            project, home = root.resolve(), root.resolve() / "qa-factory"
            task = (project / artifact_root if artifact_root else home / "artifacts") / "STORY-T217"
            task.mkdir(parents=True)
            for site, (derive, expect, prepare) in SITES.items():
                if prepare:
                    prepare(home, task)
                check_eq(f"t-217 ({layout}) {site}: derived from the project", derive(task), expect(home, project))
        finally:
            cleanup(root)
    bare = temp_dir("qa-factory-t217-bare-")          # NOT a project on purpose: the old arithmetic stays
    try:
        lone = (bare / "a" / "b" / "STORY-T217").resolve()
        lone.mkdir(parents=True)
        check_eq("t-217 (no project) judge_results: two levels up", judge_results._project_bugs_dir(lone), lone.parent.parent / "bugs")
        check_eq("t-217 (no project) walk_timing: parents 1 and 2", walk_timing._home_and_project(lone), (lone.parents[1], lone.parents[2]))
        check_eq("t-217 (no project) branch_accounting: two levels up", branch_accounting.story_home(lone), lone.parents[1])
    finally:
        cleanup(bare)
    finish("task_root_project_door")


if __name__ == "__main__":
    main()
