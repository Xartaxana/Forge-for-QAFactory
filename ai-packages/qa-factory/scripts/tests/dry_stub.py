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

COMMANDS = {"context_bundle.py": ["--manifest", "{task_root}/work/context-manifest.json", "--output", "{task_root}/work/context-bundle.json",
                                      "--root", "{task_root}"]}
# The commands a role runs that BUILD a file code owns but that is no output of the stage (the scout's source collection: skills/qa-story/phases/s1.md
# "Source collection", the one writer of work/source-inventory.json is ticket_adapter.py). Only a step that decides nothing is here: recording the task is
# a read by the tracker's own client; the judging of a mentioned ticket (`assess`) is the role's and stays with no step (E13).
ROLE_STEPS = {"qa-scout": [("work/source-inventory.json", "ticket_adapter.py",
                            ["collect", "{task}", "--relation", "task", "--output", "{task_root}/work/source-inventory.json", "--summary"])]}
MOVE_LINE =re.compile(r"^- `(\w+)`(?: — token `([^`]+)`)?;")
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


def source_key(item: dict) -> str:
    """The tracker key of an inventory source: the tail of its canonical ref (the rule of `source_inventory._key`)."""
    return str(item.get("canonical_ref") or item.get("source_id") or "").rsplit("/browse/", 1)[-1]


def read_sources(inventory: Path):
    """`(sources, "")` of the inventory read through the package's one reader (`source_inventory.load_inventory`, AR-13), or `([], why)`."""
    import source_inventory as SI
    try:
        return [s for s in SI.load_inventory(inventory).get("sources") or [] if isinstance(s, dict)], ""
    except (OSError, ValueError):
        return [], "work/source-inventory.json is missing or unreadable after the collect step"


def awaiting(sources: list) -> tuple:
    """`(unjudged, uncollected)`: the required sources whose relevance is still `pending` (a mention the scout must `peek` and `assess`), and the
    kept ones (`relevant`) whose full collection has not replaced the pending status yet (`source_inventory.record_relevance_assessment`)."""
    unjudged = [s for s in sources if s.get("required") and s.get("relevance") == "pending"]
    uncollected = [s for s in sources if s.get("required") and s.get("relevance") == "relevant" and s.get("status") == "pending"]
    return unjudged, uncollected


def pending_judgments(inventory: Path, skip=()) -> str:
    """"" when the inventory holds no source awaiting the scout (`awaiting`), else the live_only reason, naming each source: an unjudged mention is
    the role's judgment - a key the type's `stub.source_relevance` does not name gets no value from the stub (E13, AR-29) and the exit gate's own refusal
    stands; a kept source left uncollected has no read step that closed it. `skip` holds the keys a command already reported with its own text."""
    sources, why = read_sources(inventory)
    if why:
        return why
    unjudged, uncollected = awaiting(sources)
    parts = []
    refs = [s.get("canonical_ref") or s.get("source_id") for s in unjudged if source_key(s) not in skip]
    if refs:
        parts.append(f"{len(refs)} mentioned source(s) await the scout's judgment ({', '.join(map(str, refs[:5]))}): `ticket_adapter.py peek` then `assess "
                     "--relevance` is role judgment and the type holds no closed answer for it")
    kept = [s.get("canonical_ref") or s.get("source_id") for s in uncollected if source_key(s) not in skip]
    if kept:
        parts.append(f"{len(kept)} kept source(s) left pending after `assess` with no read step that closes them ({', '.join(map(str, kept[:5]))})")
    return "; ".join(parts)


def run_script(project: Path, script: str, args: list) -> tuple:
    """`(exit code, stdout+stderr)` of `python -B <package script> <args>` run in the project, as the role runs it."""
    done = subprocess.run([sys.executable, "-B", str(harness.SCRIPTS / script), *args], cwd=str(project), capture_output=True, text=True,
                          encoding="utf-8", errors="replace")
    return done.returncode, (done.stderr or done.stdout)


def judge_sources(inventory: Path, declared: dict, runner) -> tuple:
    """`(ran, judged, live_only)` of the scout's source work after `collect`: for each required source with `relevance: pending` whose key IS in
    `declared` (the type row's `stub.source_relevance`, data the stub only READS - AR-29) run `ticket_adapter.py peek <KEY>` then `assess` with exactly
    the declared value and the `assessment_ref` peek wrote; a key not named is left alone (`live_only` by the caller, no command); each kept source
    (`relevant`, still pending) gets the complete collector `collect <KEY> --relation referenced`, a read that decides nothing. A command that fails
    is a `live_only` with its text cut at 400 and is never retried with another value (E-R4). `runner(script, args) -> (exit, text)`."""
    ran, judged, live_only, tried = [], [], [], set()
    out = str(inventory)
    for _round in range(8):         # a collected ticket names further tickets, each needing peek+assess then its collection: a bounded few rounds, then what is left is reported
        sources, why = read_sources(inventory)
        if why:
            live_only.append({"output": "work/source-inventory.json", "why": why})
            break
        unjudged, uncollected = awaiting(sources)
        moved = False
        for item in unjudged:
            key = source_key(item)
            decl = declared.get(key)
            if not decl or ("judge", key) in tried:
                continue
            tried.add(("judge", key))
            moved = True
            code, text = runner("ticket_adapter.py", ["peek", key, "--output", out])
            ran.append(f"peek {key} exit {code}")
            after = next((s for s in read_sources(inventory)[0] if s.get("source_id") == item.get("source_id")), {})
            if after.get("relevance") != "pending" or not after.get("assessment_ref"):
                live_only.append({"output": "work/source-inventory.json", "key": key,
                                  "why": f"peek {key} left nothing to cite for `assess` (exit {code}): {' '.join(text.split())[:400]}"})
                continue
            code, text = runner("ticket_adapter.py", ["assess", "--output", out, "--source-id", item["source_id"], "--relevance", decl["relevance"],
                                                      "--reason", decl["reason"], "--assessment-ref", after["assessment_ref"]])
            ran.append(f"assess {key} {decl['relevance']} exit {code}")
            if code == 0:
                judged.append(key)
            else:
                live_only.append({"output": "work/source-inventory.json", "key": key,
                                  "why": f"assess {key} refused (exit {code}): {' '.join(text.split())[:400]}"})
        for item in uncollected:
            key = source_key(item)
            if key not in judged or ("collect", key) in tried:
                continue            # kept before this call (not by a declared value): the stub does not collect what it did not judge
            tried.add(("collect", key))
            moved = True
            code, text = runner("ticket_adapter.py", ["collect", key, "--relation", "referenced", "--output", out, "--summary"])
            ran.append(f"collect {key} referenced exit {code}")
            if code != 0:
                live_only.append({"output": "work/source-inventory.json", "key": key,
                                  "why": f"collect {key} refused (exit {code}): {' '.join(text.split())[:400]}"})
        if not moved:
            break
    return ran, judged, live_only


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
    import dry_world as W
    ctx = FF.FillContext(task_key=task, dispatch_id=dispatch, impl_diff=W.mr_diff(W.type_row(control.get("type"))) if control.get("type") else "")
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
    for out, script, args in ROLE_STEPS.get(role, []) if stage == "S1" else []:
        done = subprocess.run([sys.executable, "-B", str(harness.SCRIPTS / script), *[a.format(task=task, task_root=str(task_dir)) for a in args]],
                              cwd=str(project), capture_output=True, text=True, encoding="utf-8", errors="replace")
        (row["wrote"] if done.returncode == 0 else row["live_only"]).append(
            out if done.returncode == 0 else {"output": out, "why": f"{script} exit {done.returncode}: {' '.join((done.stderr or done.stdout).split())[:400]}"})
    if stage == "S1" and role in ROLE_STEPS:
        inventory = task_dir / "work" / "source-inventory.json"
        ran, judged, failed = judge_sources(inventory, (control.get("stub") or {}).get("source_relevance") or {},
                                            lambda script, args: run_script(project, script, args))
        row["ran"], row["judged"] = ran, judged
        row["live_only"].extend(failed)
        gap = pending_judgments(inventory, skip={f["key"] for f in failed if f.get("key")})
        if gap:
            row["live_only"].append({"output": "work/source-inventory.json", "why": gap})
    for out, kind in role_plan(role, stage, FF):
        if kind == "fill":
            try:
                FF.write_outputs(task_dir, project, FF.fill_artifact(out, ctx).require())
                row["wrote"].append(out)
                for where, why in (FF._row_of(out).get("synthetic") or {}).items():       # a value the row declares synthetic is named, not passed as a fact
                    row.setdefault("synthetic", []).append({"output": out, "field": where, "why": why[:120]})
            except (FF.NotFillable, FF.Unclassified, ValueError) as exc:
                row["live_only"].append({"output": out, "why": str(exc)[:240]})
        elif kind.startswith("command:"):
            argv = [a.format(task_root=str(task_dir)) for a in COMMANDS[kind[8:]]]
            done = subprocess.run([sys.executable, "-B", str(harness.SCRIPTS / kind[8:]), *argv], cwd=str(project), capture_output=True,
                                  text=True, encoding="utf-8", errors="replace")
            (row["wrote"] if done.returncode == 0 else row["live_only"]).append(
                out if done.returncode == 0 else {"output": out, "why": f"{kind[8:]} exit {done.returncode}: {' '.join((done.stderr or done.stdout).split())[:400]}"})
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
    check_eq("round 2: impl-diff.txt and context-manifest.json are filled, the bundle is built by its command",
             (plan.get("work/impl-diff.txt"), plan.get("work/context-manifest.json"), plan.get("work/context-bundle.json")),
             ("fill", "fill", "command:context_bundle.py"))
    row_type = W.type_row()
    diff = W.mr_diff(row_type)
    check("round 2: the type's merge request diff is the raw file, byte for byte", diff.startswith("diff --git ") and diff.encode("utf-8") ==
          (W.STORIES / row_type["input"] / "tracker" / "mr-4566.diff").read_bytes(), diff[:40])
    check_eq("round 2: the diff lands in work/impl-diff.txt as the world holds it", FF.fill_artifact("work/impl-diff.txt", FF.FillContext(impl_diff=diff)).files["work/impl-diff.txt"], diff)
    check_eq("E13: a world with no diff leaves impl-diff.txt unfillable, nothing is written",
             [u.hint for u in FF.fill_artifact("work/impl-diff.txt", FF.FillContext()).unfillable], ["<the diff text>"])
    inv = tmp / "inv.json"
    for name, body, expect in (("a pending required mention", {"sources": [{"required": True, "relevance": "pending", "canonical_ref": "https://x/browse/A-1"}]}, "await the scout's judgment (https://x/browse/A-1)"),
                               ("only the task, read", {"sources": [{"required": True, "relevance": "relevant"}]}, ""),
                               ("no source", {"sources": []}, "")):
        inv.write_text(json.dumps(body), encoding="utf-8")
        check(f"round 2: inventory with {name}", expect in pending_judgments(inv) and bool(pending_judgments(inv)) == bool(expect), pending_judgments(inv))
    check("round 2: an inventory that is not there is named, never read as no pending source", "missing or unreadable" in pending_judgments(tmp / "nope.json"))
    # round 3: the declared judgment is data the stub reads (AR-29, E-R1..E-R5)
    mention = {"source_id": "SRC-a", "canonical_ref": "https://x/browse/A-1", "required": True, "relevance": "pending", "status": "pending"}
    declared = {"A-1": {"relevance": "relevant", "reason": "explicit required source", "from": "x"}}

    class FakeRole:
        """A runner standing in for `ticket_adapter.py`: it records every call and changes the inventory as the real commands would."""
        def __init__(self, path, assess_exit=0, peek_ref="sources/SRC-a/assessment/ticket.json"):
            self.path, self.calls, self.assess_exit, self.peek_ref = path, [], assess_exit, peek_ref

        def __call__(self, script, args):
            self.calls.append([script, *args])
            body = json.loads(self.path.read_text(encoding="utf-8"))
            item = body["sources"][0]
            if args[0] == "peek":
                item["assessment_ref"] = self.peek_ref
            elif args[0] == "assess" and self.assess_exit == 0:
                item.update(relevance=args[args.index("--relevance") + 1], relevance_reason=args[args.index("--reason") + 1])
            elif args[0] == "collect":
                item["status"] = "read"
            self.path.write_text(json.dumps(body), encoding="utf-8")
            return (self.assess_exit, "assess refused: the person left it out") if args[0] == "assess" and self.assess_exit else (0, "")

    def fresh(name, **kw):
        path = tmp / f"{name}.json"
        path.write_text(json.dumps({"sources": [dict(mention)]}), encoding="utf-8")
        return path, FakeRole(path, **kw)

    path, role = fresh("named")
    ran, judged, gap = judge_sources(path, declared, role)
    check_eq("round 3: a named key runs peek then assess then the collector, argv exactly the data values",
             role.calls, [["ticket_adapter.py", "peek", "A-1", "--output", str(path)],
                          ["ticket_adapter.py", "assess", "--output", str(path), "--source-id", "SRC-a", "--relevance", "relevant", "--reason",
                           "explicit required source", "--assessment-ref", "sources/SRC-a/assessment/ticket.json"],
                          ["ticket_adapter.py", "collect", "A-1", "--relation", "referenced", "--output", str(path), "--summary"]])
    check_eq("round 3: a judged and collected source leaves no gap", (judged, gap, pending_judgments(path)), (["A-1"], [], ""))
    path, role = fresh("unnamed")
    ran, judged, gap = judge_sources(path, {}, role)
    check_eq("E-R1 / AR-29: a pending source the data does not name gets no command (no peek, no assess) and is a live_only naming it",
             (role.calls, ran, judged, "https://x/browse/A-1" in pending_judgments(path)), ([], [], [], True))
    path, role = fresh("refused", assess_exit=1)
    ran, judged, gap = judge_sources(path, declared, role)
    check("E-R4: an assess refused is a live_only with the refusal verbatim, no second attempt with another value",
          "assess A-1 refused (exit 1): assess refused: the person left it out" in gap[0]["why"] and [c[1] for c in role.calls] == ["peek", "assess"] and not judged, f"{gap} {role.calls}")
    path, role = fresh("noref", peek_ref=None)
    ran, judged, gap = judge_sources(path, declared, role)
    check("E-R5: a peek that left no assessment to cite is a live_only and no assess runs", "left nothing to cite" in gap[0]["why"] and [c[1] for c in role.calls] == ["peek"], f"{gap} {role.calls}")
    path = tmp / "kept.json"
    path.write_text(json.dumps({"sources": [dict(mention, relevance="relevant")]}), encoding="utf-8")
    check("round 3: a kept source left pending after `assess relevant` with no read step is named by pending_judgments",
          "left pending after `assess`" in pending_judgments(path) and "https://x/browse/A-1" in pending_judgments(path), pending_judgments(path))
    check_eq("round 3: judge_sources does not collect a kept source it did not judge", judge_sources(path, {}, FakeRole(path))[0], [])
    cut_gap = judge_sources(fresh("cut")[0], declared, lambda s, a: (1, "x" * 900))[2]
    check("E-R10: the command text a live_only carries is cut at 400 characters and keeps its head", "x" * 400 in cut_gap[0]["why"] and "x" * 401 not in cut_gap[0]["why"], cut_gap[0]["why"][:80])
    check_eq("E-R2: a declared key no source took is a NOTE", W.unused_judgments({"A-1": {}, "B-2": {}}, [{"judged": ["A-1"]}, {}]),
             ["NOTE: unused judgment B-2 (the stub never judged a source with that key)"])
    check_eq("item 2: the row's own value wins over the type's, key by key; the type's other keys stay",
             W.merge_stub({"source_relevance": {"A-1": {"relevance": "relevant"}, "B-2": {"relevance": "unknown"}}, "qa-scout": {"verdict": "x"}},
                          {"source_relevance": {"A-1": {"relevance": "not_relevant"}}}),
             {"source_relevance": {"A-1": {"relevance": "not_relevant"}, "B-2": {"relevance": "unknown"}}, "qa-scout": {"verdict": "x"}})
    check_eq("item 2: the main pass reads the type's stub alone", W.merge_stub({"source_relevance": {"A-1": {}}}, None), {"source_relevance": {"A-1": {}}})
    # E-R3 / A1-E4: a declared judgment that cannot be trusted is red before the world is built
    good_j = {"relevance": "relevant", "reason": "r", "from": "f"}
    for n, (name, stub, needle) in enumerate((
            ("a row without `stub` (the round-2 table) loads (control)", None, "ok"),
            ("a good judgment loads (control)", {"source_relevance": {"A-1": good_j}}, "ok"),
            ("`stub` not a mapping", ["x"], "`stub` is not a mapping"),
            ("a value outside the closed list", {"source_relevance": {"A-1": dict(good_j, relevance="maybe")}}, "relevance 'maybe'"),
            ("an empty reason", {"source_relevance": {"A-1": dict(good_j, reason="  ")}}, "has no `reason`"),
            ("a key twice, case-folded", {"source_relevance": {"A-1": good_j, "a-1": good_j}}, "repeats a key"),
            ("`source_relevance` not a mapping", {"source_relevance": []}, "is not a mapping"))):
        got = table(f"s{n}", json.dumps({"default": "a", "types": [one("a", **({} if stub is None else {"stub": stub}))], "gaps": []}), ("in-a",))
        check(f"load_types (E-R3): {name}", got == "ok" if needle == "ok" else needle in got and "'a'" in got, f"got {got!r}")
    real = W.type_row()
    check_eq("item 1: the real type declares the recorded verdict of TP1-15791", (real["stub"]["source_relevance"]["TP1-15791"]["relevance"],
             real["stub"]["source_relevance"]["TP1-15791"]["from"].split(":")[0]), ("relevant", "investigation-14857/TP1-14857/work/source-inventory.json"))
    # AR-28: a gate verdict only when S3 is done; E-R8: a byte change in a snapshot is red
    all_done = {"S0": "done", "S1": "done", "S2": "done", "S3": "done"}
    check("AR-28: S3 done prints the numbers verdict", W.gate_line(all_done, {}, 10, 5, 8).startswith("gate: continue ("), W.gate_line(all_done, {}, 10, 5, 8))
    early = W.gate_line(dict(all_done, S2="running", S3="absent"), {"S2": "running - live_only: " + "y" * 300}, 10, 5, 8)
    check("AR-28 / E-R7: S3 not done prints `undecided` with the stage, the cut outcome and the measured part",
          early.startswith("gate: undecided -- the road ended at S2: running - live_only: y") and "measured: S0..S2 10.0 s, row median 5.0 s" in early
          and "y" * 20 in early and "y" * 300 not in early and len(early.split(": ", 2)[2].split("; measured")[0]) <= 160, early)
    check("AR-28: an undecided line never reads `continue`", "continue" not in early, early)
    snap_dir = tmp / "snapdir"
    snap_dir.mkdir()
    (snap_dir / "a.txt").write_bytes(b"one")
    before = W.tree_hash(snap_dir)
    check_eq("E-R8: an untouched tree is not red", W.snapshot_red("row1", before, snap_dir), "")
    (snap_dir / "a.txt").write_bytes(b"onE")
    check_eq("E-R8: a byte change between the two hashes is red naming the row", W.snapshot_red("row1", before, snap_dir), "red: snapshot changed by a row: row1")
    check_eq("round 2: the answers of the road are the words of the first row naming the kind", W.closed_answers([{"answers": {"a": "x"}}, {"answers": {"a": "y", "b": "z"}}]), {"a": "x", "b": "z"})
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
