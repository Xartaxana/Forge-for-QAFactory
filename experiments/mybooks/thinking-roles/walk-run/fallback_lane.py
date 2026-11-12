#!/usr/bin/env python3
"""fallback_lane.py - ONE walk lane by script, for the day the driver's N5s is not in the package (t-2006 sec 5). Serial: one process per lane.

    python fallback_lane.py --lane G1 --project <copy> --package <package dir> [--task LOCAL-1] [--model claude-sonnet-5-5] [--dry-run]
    python fallback_lane.py --list

What the driver's `walk_before` / `run_role` / `walk_after` will do, in this order (each step is a line of sec 5):
  1 story_step.py start (registers the running dispatch W, prepares the requests)
  2 app_card.py build; walk_session.py open ... --parent-pid <THIS process's pid>   (the server dies with its parent, so the parent must outlive the lane)
  3 brief_pack.py (the real brief, walk lines since the record exists)
  4 a `launched` row in state/driver-runs.jsonl    5 claude -p on the qa-runner role, the prompt through stdin    6 the result row
  7 walk_session.py close; a missing verdict -> write_verdict(None); manual_evidence.record_from_walk; finalize_task.py; the `after_end` timing line
  8 controller.py --operation checkpoint --status incomplete
`--dry-run` prints the commands and runs nothing. No credential value is written anywhere: actors are handles. A lane whose server does not
open ends here with exit 3 (the road of today's role is not a walk and is never taken in this proof). The label of what this proves is in sec 5.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import make_walk_cases as MW  # noqa: E402

ROLE_TOOLS = "Bash,Read,Write,Edit,MultiEdit,Glob,Grep"
SECOND_BROWSER = "env:USER_EMAIL/USER_PASSWORD"      # names of variables, never values
PROMPT = "Your brief: qa-factory/artifacts/{task}/work/briefs/{walk}.md. Read it and do the work."
ROLE_TIMEOUT_S = 3000


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def lanes(data) -> dict:
    """{lane: [case dict, ...]} in card order."""
    out = {}
    for case in sorted(data["cases"], key=lambda c: c["card"]):
        out.setdefault(case["lane"], []).append(case)
    return out


def lane_actors(cases) -> tuple:
    """(actor, actor2 or None): `user` first when the lane names it; a second browser of the same user is `env:USER_EMAIL/USER_PASSWORD`."""
    handles = []
    for case in cases:
        for actor in case.get("actors") or []:
            handle = actor.get("stand_account") or SECOND_BROWSER
            if handle not in handles:
                handles.append(handle)
    if not handles:
        return "guest", None
    handles.sort(key=lambda h: (h != "user", h))
    return handles[0], (handles[1] if len(handles) > 1 else None)


class Lane:
    def __init__(self, args, data):
        self.args = args
        self.cases = lanes(data)[args.lane]
        self.ids = [MW.case_id(data["ticket"], c["card"]) for c in self.cases]
        self.project = Path(args.project)
        self.package = Path(args.package)
        self.scripts = self.package / "scripts"
        self.task_root = self.project / "qa-factory" / "artifacts" / args.task
        self.walk = "<W>"
        self.log = []

    def sh(self, cmd, stdin=None, timeout=300):
        cmd = [str(c) for c in cmd]
        self.log.append(" ".join(cmd))
        print("+ " + " ".join(cmd), flush=True)
        if self.args.dry_run:
            return 0, ""
        done = subprocess.run(cmd, input=stdin, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(self.project),
                              timeout=timeout)
        if done.stderr.strip():
            print(done.stderr.strip()[-1500:], file=sys.stderr)
        return done.returncode, done.stdout

    def py(self, script, *rest, **kw):
        return self.sh([sys.executable, "-B", self.scripts / script, *rest], **kw)

    def append(self, path, row):
        print(f"+ append to {path.name}: {json.dumps(row)[:160]}", flush=True)
        if not self.args.dry_run:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("a", encoding="utf-8", newline="\n") as handle:
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    def run(self) -> int:
        a, task = self.args, self.args.task
        code, out = self.py("story_step.py", "start", "--task", task, "--stage", "S6", "--role", "qa-runner", "--execution-kind", "manual",
                            "--scope", ",".join(self.ids))
        found = re.search(r"dispatched (\S+)", out)
        if a.dry_run:
            self.walk = "<W>"
        elif code != 0 or not found:
            print(f"start refused (exit {code}): {out.strip()[-600:]}")
            return 2
        else:
            self.walk = found.group(1)
        actor, actor2 = lane_actors(self.cases)
        self.py("app_card.py", "build", "--task-root", self.task_root)
        opener = ["walk_session.py", "open", "--task-root", self.task_root, "--walk", self.walk, "--items", ",".join(self.ids),
                  "--actor", actor] + (["--actor2", actor2] if actor2 else []) + ["--parent-pid", str(os.getpid())]
        code, out = self.py(*opener, timeout=150)
        if not a.dry_run and (code != 0 or '"ready"' not in out):
            print(f"open did not give a ready server (exit {code}): {out.strip()[-600:]}")
            return 3
        self.py("brief_pack.py", "--task", task, "--stage", "S6", "--role", "qa-runner", "--dispatch", self.walk)
        runs = self.task_root / "state" / "driver-runs.jsonl"
        started = now()
        self.append(runs, {"ts": started, "kind": "launched", "call": "role", "role": "qa-runner", "dispatch_id": self.walk, "stage": "S6",
                           "started_at": started, "model": a.model, "retry": 0})
        claude = shutil.which("claude") or "claude"
        code, out = self.sh([claude, "-p", "--output-format", "json", "--permission-mode", "acceptEdits", "--model", a.model,
                             "--allowedTools", ROLE_TOOLS, "--plugin-dir", self.package, "--agent", "qa-factory:qa-runner"],
                            stdin=PROMPT.format(task=task, walk=self.walk), timeout=a.role_timeout)
        try:
            result = json.loads(out) if out.strip() else {}
        except ValueError:
            result = {}
        self.append(runs, {"ts": now(), "kind": "role", "role": "qa-runner", "dispatch": self.walk, "stage": "S6", "model": a.model,
                           "session_id": result.get("session_id"), "num_turns": result.get("num_turns"), "total_cost_usd": result.get("total_cost_usd"),
                           "duration_ms": result.get("duration_ms"), "resumed": False, "exit_code": code,
                           "is_error": bool(result.get("is_error")) if result else code != 0, "retry": 0})
        self.after()
        self.py("controller.py", "--task-root", self.task_root, "--operation", "checkpoint", "--dispatch", self.walk, "--status", "incomplete",
                "--reason", "t-2006 fallback lane closed by its script")
        print(json.dumps({"lane": a.lane, "walk": self.walk, "cases": self.ids, "claude_exit": code}))
        return 0

    def after(self):
        """Step 7: close the server, then the records of the items from disk (idempotent: a record already written is kept)."""
        self.py("walk_session.py", "close", "--task-root", self.task_root, "--walk", self.walk)
        if self.args.dry_run:
            print("+ in-process: write_verdict(None) for an item with no record; record_from_walk; finalize_task.py; after_end line")
            return
        sys.path.insert(0, str(self.scripts))
        import manual_evidence as ME  # noqa: WPS433
        import walk_session as WS  # noqa: WPS433
        folder = self.task_root / "work" / "walks" / self.walk
        for item in self.ids:
            path = folder / f"{item}.json"
            record = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else WS.write_verdict(self.task_root, self.walk, item, None)
            answer = ME.record_from_walk(self.task_root, item, record)
            if isinstance(answer, dict) and answer.get("refused"):
                print(f"record_from_walk refused {item}: {str(answer['refused'])[:300]}")
        self.py("finalize_task.py", self.task_root)
        self.append(folder / "timing.jsonl", {"after_end": now()})


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--lane")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--project", help="the copy of the stand project (the folder that holds qa-factory/)")
    parser.add_argument("--package", help="the frozen package folder (ai-packages/qa-factory)")
    parser.add_argument("--task", default="LOCAL-1")
    parser.add_argument("--model", default="claude-sonnet-5-5")
    parser.add_argument("--role-timeout", type=int, default=ROLE_TIMEOUT_S)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--data", default=str(MW.DATA))
    args = parser.parse_args(argv)
    data = json.loads(Path(args.data).read_text(encoding="utf-8"))
    table = lanes(data)
    if args.list or not args.lane:
        for name, cases in table.items():
            print(f"{name}: " + ", ".join(MW.case_id(data["ticket"], c["card"]) for c in cases) + f"  actors={lane_actors(cases)}")
        return 0
    if args.lane not in table or not args.project or not args.package:
        print(f"--lane is one of {', '.join(table)}; --project and --package are required")
        return 2
    return Lane(args, data).run()


if __name__ == "__main__":
    sys.exit(main())
