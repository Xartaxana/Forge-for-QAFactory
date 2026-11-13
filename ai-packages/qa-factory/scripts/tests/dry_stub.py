"""The stub role of the dry world (P1-b spec section 4.1, node N0): the executable the REAL driver runs in place of `claude -p`.

    STORY_RUN_CLAUDE=<this file>      the driver runs `python dry_stub.py <the arguments of claude -p>` (a `.py` path, as the tests' stubs)
    python -B dry_stub.py --selftest  the table of cases of the stub and of `dry_world.load_types()` (the only local run)

A role call: the stub reads the handover form the controller wrote (`work/handoffs/<dispatch>.yaml`), fills it with the P1-a filler
(`form_filler.fill_form`, the contract named in the form's own `contract:` line, the verdict from the row's control or the
vocabulary's first word), writes every output of the stage whose writer is THIS role with `fill_artifact`, and runs the command the
role would run for an output code builds from it. Everything the filler cannot fill is a `live_only` row of the stub's journal with
its reason - never a hand-written text (E13). The stub decides nothing: verdict, result text and the moves of a conductor come from
the row's control (`dry-stub-control.json`) or the closed list the prompt itself offers.

The journal `state/dry-stub.jsonl` (written only here) starts with one line holding the value of STORY_RUN_CLASS the stub saw: the
walker checks it before the first step (E18) - a dry run is never counted as a live one.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
import harness  # noqa: E402
import story_run_common as T  # noqa: E402

COMMANDS = {"context_bundle.py": ["--manifest", "{task_root}/work/context-manifest.json", "--output", "{task_root}/work/context-bundle.json"]}
MOVE_LINE = re.compile(r"^- `(\w+)`(?: — token `([^`]+)`)?;")
FORM_CONTRACT = re.compile(r"^contract:\s*(\S+)", re.M)
FORM_STAGE = re.compile(r"^stage:\s*(\S+)", re.M)


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def parse_moves(prompt: str) -> list:
    """`[(move, token)]` of the section `## Moves open here` of a conductor's prompt (`no_move.moves_section`): the moves a person may be
    offered. The section is read as the prompt prints it; no section is no move (the caller says so, it never guesses one)."""
    moves, inside = [], False
    for line in prompt.splitlines():
        if line.startswith("## "):
            inside = line.strip() == "## Moves open here"
        elif inside:
            found = MOVE_LINE.match(line)
            if found and found.group(2):
                moves.append((found.group(1), found.group(2)))
    return moves


def conductor_verdict(prompt: str, control: dict) -> dict:
    """The conductor stub, deterministic: the row's `conductor` control when it has one, else `ask_person` offering EVERY open move of the
    prompt's own list, else `stop` naming that the prompt offered none."""
    if control.get("conductor"):
        return dict(control["conductor"])
    moves = parse_moves(prompt)
    if not moves:
        return {"action": "stop", "did": "stub: the prompt lists no open move to offer", "question": ""}
    return {"action": "ask_person", "did": "stub: offered every open move", "question": "Which of these should happen?",
            "why_person": "access", "checked": "the refusal",
            "options": [T.seam_option(token, move) for move, token in moves]}


def role_plan(role: str, stage: str, ff) -> list:
    """`[(output, kind)]` of the stage's outputs this role writes: `fill` (a role output with a template), `live_only:<why>` (the
    filler has no kind for it, E13), `command:<script>` (code builds it from the role's file; the role runs the command)."""
    plan = []
    for stage_id, out in ff.stage_outputs():
        if stage_id != stage:
            continue
        try:
            writer = ff.writer_of(out)
            kind = ff.classify(out)
        except ff.Unclassified as exc:
            plan.append((out, f"live_only:{exc.why}"))
            continue
        if writer == f"{role}{ff.ROLE_WRITER}":
            plan.append((out, "fill" if kind == "role" else f"live_only:{ff.rules()['not_covered'].get(out, 'no filler kind')}"))
        elif writer in COMMANDS and role == "qa-scout":
            plan.append((out, f"command:{writer}"))
    return plan


def run_class_problem(rows: list) -> str:
    """"" when the first row of the stub journal says the run class reached the stub as `dry`; else the red line (E18)."""
    first = rows[0] if rows else {}
    if first.get("run_class") != "dry":
        return f"run class not propagated: the stub saw STORY_RUN_CLASS={first.get('run_class')!r}, expected 'dry'"
    return ""


def journal(task_dir: Path, row: dict) -> None:
    path = task_dir / "state" / "dry-stub.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.is_file():
        path.write_text(json.dumps({"first": True, "ts": now(), "run_class": os.environ.get("STORY_RUN_CLASS", "")}) + "\n", encoding="utf-8")
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row) + "\n")


def calls_before(task_dir: Path, key: str) -> int:
    path = task_dir / "state" / "dry-stub.jsonl"
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()] if path.is_file() else []
    return len([r for r in rows if (r.get("dispatch") or r.get("conductor")) == key])


def fill_role(role: str, prompt: str, control: dict, project: Path, task_dir: Path) -> tuple:
    """`(dispatch, result text, journal row)` of one role call; see the module text."""
    import form_filler as FF
    dispatch = re.search(r"Dispatch: (\S+)\.", prompt)
    dispatch = dispatch.group(1) if dispatch else ""
    row = {"role": role, "wrote": [], "live_only": []}
    form = task_dir / "work" / "handoffs" / f"{dispatch}.yaml"
    text = form.read_text(encoding="utf-8") if form.is_file() else ""
    contract, stage = FORM_CONTRACT.search(text), FORM_STAGE.search(text)
    stage = stage.group(1) if stage else ""
    row["stage"] = stage
    mine = (control.get("stub") or {}).get(role) or {}
    task = control.get("task", "")
    ctx = FF.FillContext(task_key=task, dispatch_id=dispatch)
    if not contract:
        row["live_only"].append({"output": f"work/handoffs/{dispatch}.yaml", "why": "no form with a `contract:` line at that path"})
    else:
        filled = FF.fill_form(contract.group(1), ctx, verdict=mine.get("verdict"))
        if filled.unfillable:
            first = filled.unfillable[0]
            row["live_only"].append({"output": f"form {contract.group(1)}", "why": f"{first.path}: {first.why} (and {len(filled.unfillable) - 1} more)"})
        else:
            form.write_bytes(filled.text.encode("utf-8"))
            row["wrote"].append(f"work/handoffs/{dispatch}.yaml")
    for out, kind in role_plan(role, stage, FF):
        if kind == "fill":
            try:
                FF.write_outputs(task_dir, project, FF.fill_artifact(out, ctx).require())
                row["wrote"].append(out)
            except (FF.NotFillable, FF.Unclassified, ValueError) as exc:
                row["live_only"].append({"output": out, "why": str(exc)[:240]})
        elif kind.startswith("command:"):
            argv = [a.format(task_root=str(task_dir)) for a in COMMANDS[kind[8:]]]
            done = subprocess.run([sys.executable, "-B", str(harness.SCRIPTS / kind[8:]), *argv], cwd=str(project), capture_output=True,
                                  text=True, encoding="utf-8", errors="replace")
            (row["wrote"] if done.returncode == 0 else row["live_only"]).append(
                out if done.returncode == 0 else {"output": out, "why": f"{kind[8:]} exit {done.returncode}: {(done.stderr or done.stdout)[-200:]}"})
        else:
            row["live_only"].append({"output": out, "why": kind[len("live_only:"):]})
    default = f"{role} {stage} {task} - the stub filled the handover form of {dispatch}; nothing else to say"
    return dispatch, mine.get("result_text") or default, row


def claude_main(argv: list) -> int:
    """The stub `claude -p`: one JSON line on stdout, the shape the driver's `run_claude` reads."""
    def opt(name):
        return argv[argv.index(name) + 1] if name in argv else ""
    prompt = sys.stdin.buffer.read().decode("utf-8")
    control_path = os.environ.get("DRY_STUB_CONTROL", "")
    control = json.loads(Path(control_path).read_text(encoding="utf-8")) if control_path and Path(control_path).is_file() else {}
    project = Path(os.environ.get("CLAUDE_PROJECT_DIR") or ".").resolve()
    task_dir = project / "qa-factory" / "artifacts" / control.get("task", "")
    agent, resume = opt("--agent"), opt("--resume")
    role = agent.split(":")[-1]
    if resume or agent:
        dispatch = re.search(r"Dispatch: (\S+)\.", prompt)
        key = dispatch.group(1) if dispatch else (opt("--resume") or role)
        n = calls_before(task_dir, key) + 1
        if resume:        # a repair resume: the stub has no judgment to repair with, so it answers as before and writes nothing
            result, row, session = (control.get("stub") or {}).get(role, {}).get("result_text") or "", {"role": role, "resume": True, "wrote": [], "live_only": []}, resume
            dispatch_id = key
        else:
            dispatch_id, result, row = fill_role(role, prompt, control, project, task_dir)
            session = f"stub-{dispatch_id}-{n}"
        journal(task_dir, dict(row, ts=now(), dispatch=dispatch_id, n=n, prompt_sha=hashlib.sha256(
            prompt.replace(dispatch_id, "<dispatch>").encode("utf-8")).hexdigest(), run_class=os.environ.get("STORY_RUN_CLASS", "")))
    else:
        n = calls_before(task_dir, "conductor") + 1
        verdict = conductor_verdict(prompt, control)
        result, session = "I looked.\n" + json.dumps(verdict), f"stub-conductor-{n}"
        journal(task_dir, {"ts": now(), "conductor": "conductor", "n": n, "role": "", "wrote": [], "live_only": [], "action": verdict.get("action"),
                           "prompt_sha": hashlib.sha256(prompt.encode("utf-8")).hexdigest(), "run_class": os.environ.get("STORY_RUN_CLASS", "")})
    ns: dict = {}
    exec(T.RECEIPT, ns)
    ns["write_receipt"](session, None)
    print(json.dumps({"type": "result", "subtype": "success", "is_error": False, "session_id": session, "num_turns": 3,
                      "total_cost_usd": 0.0, "duration_ms": 1, "result": result}))
    sys.stdout.flush()
    return 0


# ------------------------------------------------------------------------------------------------ the selftest
def selftest() -> int:
    from harness import check, check_eq, finish
    import dry_world as W
    import form_filler as FF
    tmp = Path(tempfile.mkdtemp(prefix="qa-dry-selftest-"))

    def table(name, content, folders=(), expect=None):
        folder = tmp / name
        folder.mkdir()
        for f in folders:
            (folder / f).mkdir()
            (folder / f / "routes.json").write_text("{}", encoding="utf-8")
        (folder / "dry-types.json").write_text(content, encoding="utf-8")
        try:
            W.load_types(folder / "dry-types.json")
            return "ok"
        except W.TypesError as exc:
            return str(exc)

    def one(tid, **extra):
        return dict({"id": tid, "input": f"in-{tid}", "task": "T-1", "tracker": {"kind": "jira", "routes": "routes.json"}}, **extra)

    good = json.dumps({"default": "a", "types": [one("a")], "gaps": []})
    # A1-E4: every broken table is red naming the file and the id; the good one passes (control)
    cases = {
        "a good table loads (control)": (good, ("in-a",), "ok"),
        "an empty file": ("", (), "dry-types.json: the file is empty"),
        "a type without its folder": (good, (), "type 'a' names the folder 'in-a'"),
        "two types with one id": (json.dumps({"default": "a", "types": [one("a"), one("a")], "gaps": []}), ("in-a",), "share the id 'a'"),
        "default not among the types": (json.dumps({"default": "zz", "types": [one("a")], "gaps": []}), ("in-a",), "`default` is 'zz'"),
        "not JSON": ("{nope", (), "not valid JSON"),
        "no types": (json.dumps({"default": "a", "types": []}), (), "`types` is missing or empty"),
        "an unknown tracker kind": (json.dumps({"default": "a", "types": [one("a", tracker={"kind": "x"})], "gaps": []}), ("in-a",), "tracker kind 'x'"),
    }
    for n, (name, (content, folders, needle)) in enumerate(cases.items()):
        got = table(f"t{n}", content, folders)
        check(f"load_types: {name}", got == "ok" if needle == "ok" else needle in got, f"got {got!r}")
    types, gaps = W.load_types()
    check_eq("load_types: the real table holds the one type and both gaps", ([t["id"] for t in types], [g["id"] for g in gaps]),
             (["codemie-14857"], ["mybooks-local-1", "no-autotests"]))
    # A1-E8 / A1-E9: a known route answers its file, an absent one 404, a repeat answers the same and is counted
    server = W.tracker_server(W.type_row())
    try:
        import urllib.error
        import urllib.request
        def get(path):
            try:
                with urllib.request.urlopen(server.base_url + path, timeout=10) as r:
                    return r.status, r.read()
            except urllib.error.HTTPError as exc:
                return exc.code, b""
        known, again = get("/rest/api/2/issue/TP1-14857?fields=*all"), get("/rest/api/2/issue/TP1-14857?fields=*all")
        missing = get("/rest/api/2/issue/TP1-14857/remotelink")
        check_eq("tracker: the ticket route answers 200 with the issue key", (known[0], json.loads(known[1])["key"]), (200, "TP1-14857"))
        check_eq("tracker: a repeated request gets the same bytes", again, known)
        check_eq("tracker: a route the world does not hold answers 404", missing[0], 404)
        check_eq("tracker: the request count is printed per path", server.counts["/rest/api/2/issue/TP1-14857?fields=*all"], 2)
        check("tracker: the summary names the path without a route", "remotelink" in server.summary())
    finally:
        server.stop()
    # E13: an output the filler has no kind for is live_only and nothing is written; a form the filler can fill is written whole
    plan = dict(role_plan("qa-scout", "S1", FF))
    check_eq("E13: impl-diff.txt is live_only with the filler's own reason", plan.get("work/impl-diff.txt", "")[:10], "live_only:")
    check_eq("E13: context-manifest.json is filled, the bundle is built by its command", (plan.get("work/context-manifest.json"), plan.get("work/context-bundle.json")),
             ("fill", "command:context_bundle.py"))
    # the conductor stub offers every open move the prompt lists, and stops when it lists none
    prompt = "x\n## Moves open here\n\nintro\n- `retry` — token `again`; option carries no \"args\"\n- `story_fact` — yours to run, never an option\n- `stop_here` — token `stop`; option carries no \"args\"\n\n## Other\n- `no` — token `no`;"
    check_eq("conductor: the open moves of the prompt, in order", parse_moves(prompt), [("retry", "again"), ("stop_here", "stop")])
    verdict = conductor_verdict(prompt, {})
    check_eq("conductor: ask_person with every open move as an option", (verdict["action"], [o["token"] for o in verdict["options"]]), ("ask_person", ["again", "stop"]))
    check_eq("conductor: no section, no move: stop", conductor_verdict("no section", {})["action"], "stop")
    # E18: the class the stub saw
    check("E18: dry as the first line passes", run_class_problem([{"first": True, "run_class": "dry"}]) == "")
    check("E18: a missing class is red", "run class not propagated" in run_class_problem([{"first": True, "run_class": ""}]))
    check("E18: an empty journal is red", "run class not propagated" in run_class_problem([]))
    # E16: a snapshot not made by this run, and one that is not there
    world = W.World({"id": "t", "task": "T-1"}, tmp / "proj", {}, None, tmp / "snaps")
    (tmp / "proj").mkdir()
    snap = W.snapshot(world, "S0")
    check("E16: a snapshot of this run is copied", W.from_snapshot(world, "S0").root.is_dir())
    marker = snap / ".dry-snapshot.json"
    marker.write_text(json.dumps({"label": "other", "from": str(tmp / "proj")}), encoding="utf-8")
    try:
        W.from_snapshot(world, "S0")
        got = "no refusal"
    except W.SnapshotError as exc:
        got = str(exc)
    check("E16: a snapshot of another run is refused", "snapshot not from this run" in got, got)
    try:
        W.from_snapshot(world, "S9")
        got = "no refusal"
    except W.SnapshotError as exc:
        got = str(exc)
    check("E16: a snapshot the main pass never made is named missing", "not found" in got, got)
    check_eq("gate: the numbers of the spec", (W.gate_verdict(100, 10, 15), W.gate_verdict(200, 10, 15), W.gate_verdict(100, 30, 40), W.gate_verdict(301, 5, 5), W.gate_verdict(10, 5, 61)),
             ("continue", "narrow", "narrow", "stop", "stop"))
    shutil.rmtree(tmp, ignore_errors=True)
    finish("dry_stub --selftest")
    return 0


def main(argv: list) -> int:
    if "--selftest" in argv:
        return selftest()
    if "--spike" in argv:
        import dry_world
        return dry_world.main(argv)
    return claude_main(argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
