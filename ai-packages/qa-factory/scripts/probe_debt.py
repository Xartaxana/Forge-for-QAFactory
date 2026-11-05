#!/usr/bin/env python3
"""probe_debt.py — a live probe ran and passed, but no receipt for the test as it is now stands.

On TP1-13797 (cmp1) the critic's first window probed 16 instances: every probe said
`intended_failure`, and not one receipt was published, because the probe measured the test file
at one sha256 while the manifest bound the row to another (`probe_by_code.attach_receipt` writes a
receipt only when the two are equal). "Proven" fell from 24 to 8 on the factory's own bookkeeping,
not on anything the product did. This module names that state and gets out of it by code:

  probe_debt.py --task T [--dispatch ID] [--json]
      read-only: the DEBT - every manifest row that is required to have a live check
      (`proof_level.proof_required`), reaches no level (`proof_level.reached`), and has a probe
      record that says `intended_failure` (published or not: a receipt measured on other bytes than
      the test has now is debt too). Each item carries the exact `probe_by_code.py` line that
      clears it. A record of a row that is NOT required is listed as `info`, with no action.
  probe_debt.py --task T --settle --dispatch <open S5 qa-code-critic dispatch id>
      clears what code may clear, in order, per item: rebind the row to the current bytes
      (`manifest_from_tests.py`, a subprocess) when they differ, then a FRESH `probe_by_code.py`
      (a subprocess) on the record's own test, mutation and oracle. What is left - and what each
      step did - is recorded in `work/probe-debt.json`, which the code critic reads as its work.

What code decides and what it leaves (FR-47). Code REPLAYS the record's own probe: its test node,
its mutation, and the oracle function it named (`--oracle <file>::<function>`). An oracle chosen
further out than code can see - a function that is gone, a mutation this tool does not make, a
record that names no test - is the critic's, and the item says so. A replay is a FRESH probe on
the CURRENT bytes: it is valid through `probe_by_code`'s own receipt equality, never through this
module. Nothing here writes a receipt or a manifest field (the manifest write of a rebind is
`manifest_from_tests.py`'s own, in its own process); `find` writes nothing at all (FR-45).

Stopping (V1). One probe can take minutes, and `story_step start` runs this through a shell call
that times out: the settle has a WALL-CLOCK budget (`SETTLE_BUDGET_S`, or `--budget-s`, which is
what `start` passes: what is left of ITS budget), checked before each item. The budget bounds the
whole call, so a probe is started only when it can be expected to fit: the FIRST one always runs,
a later one only when the time left is not less than the longest probe of this settle so far. A
probe that has begun is never killed (it mutates the author's file in place and restores it in a
`finally`, which a kill skips): it is given the time left as its OWN `--timeout`, so it ends by
itself, restores, and reports `not_executed`. The stand is checked ONCE first; the first
`not_executed` probe stops it; an item whose bytes are the ones a `not_executed` attempt already
failed on is not probed again (`same_bytes`); `SETTLE_LIMIT` is a second cap. Every item not done
goes to the critic's list with the reason (`budget`, `stand`, `limit`, ...). Exit 0 always - code
tells, it does not stop the factory (P1) - and 2 only for arguments that cannot be used.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import contract as C  # noqa: E402
import probe_by_code as PBC  # noqa: E402
import proof_level as PL  # noqa: E402
from event_store import atomic_json  # noqa: E402
from hooklib import sorted_paths  # noqa: E402

DEBT_REL = "work/probe-debt.json"
SCHEMA_VERSION = 1
# About 90 s: the skill road runs `story_step start` through a shell call that times out at 120 s
# (critic of t-134, V1). A count of probes cannot protect that call - one probe may take 1860 s.
SETTLE_BUDGET_S = 90
# The second cap, in probes started: a bound even when every probe is fast. The budget is the stop.
SETTLE_LIMIT = 25
# A probe's own run may take RUN_TIMEOUT_S; the process gets that plus a margin. The settle's budget
# never kills a probe that has begun - it shortens the probe's OWN `--timeout` (see `settle`), so the
# probe restores the author's bytes and ends by itself; only a HUNG process is given up on, at the
# time left plus the margin.
PROBE_PROCESS_MARGIN_S = 120
PROBE_PROCESS_TIMEOUT_S = PBC.RUN_TIMEOUT_S + PROBE_PROCESS_MARGIN_S
MANIFEST_PROCESS_TIMEOUT_S = 120

# `PROBE_DEBT_PROBE_SCRIPT` / `PROBE_DEBT_MANIFEST_SCRIPT` replace the two tools (tests): like
# `PROBE_RUN_SUITE` for `probe_by_code`, the settle never has to launch the real ones to be tested.
PROBE_SCRIPT_ENV = "PROBE_DEBT_PROBE_SCRIPT"
MANIFEST_SCRIPT_ENV = "PROBE_DEBT_MANIFEST_SCRIPT"

REBIND_AND_REPROBE, REPROBE, LEAVE_TO_CRITIC = "rebind_and_reprobe", "reprobe", "leave_to_critic"
ACTIONS = (REBIND_AND_REPROBE, REPROBE, LEAVE_TO_CRITIC)

# The door of a rebind that code will not do (FR-1): who acts and with what.
REBIND_LEFT = ("the author re-runs manifest_from_tests.py (with --collect if the ids come from a "
               "collect)")


# --- reading ---------------------------------------------------------------------------------------

def _short(sha) -> str:
    return str(sha or "")[:12] or "none"


def _posix(text) -> str:
    return str(text or "").replace("\\", "/")


def _same_file(named: str, other: str) -> bool:
    a, b = _posix(named).strip("/"), _posix(other).strip("/")
    return bool(a and b) and (a == b or a.endswith("/" + b) or b.endswith("/" + a))


def _project_of(project):
    if project is not None:
        return Path(project)
    try:
        from hooklib import project_root
        return project_root()
    except Exception:  # no project to read from: the bytes are unknown, never guessed
        return None


def _read_manifest(task_root) -> dict:
    try:
        return C.load_json(C.artifact(Path(task_root), "automation-manifest.json"))
    except Exception:
        return {}


def _read_json_file(path: Path):
    """(value, "") or (None, why): a record that cannot be read is told, never taken for absent."""
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as exc:
        return None, f"{type(exc).__name__}"
    if not isinstance(value, dict):
        return None, "not a JSON object"
    return value, ""


def _aliases(row) -> list:
    return [i for i in C.instance_id_aliases(row) if i]


def _case_of(row: dict, record: dict) -> str:
    links = C.manifest_test_links(row)
    return str(row.get("case") or (links[0] if links else "") or record.get("case") or "")


def _bound_sha(row: dict) -> str:
    binding = row.get("trace_binding")
    return str(binding.get("test_content_sha") or "") if isinstance(binding, dict) else ""


def _quote(value) -> str:
    """One argument of a shell line a person or a role copies. Bare when it is plainly safe; double
    quotes when nothing in it is special to a shell; else single quotes (an id can carry `$[?(` -
    TP1-15045 collected `[malformed-$[?(unterminated-True]`)."""
    text = str(value)
    if re.fullmatch(r"[A-Za-z0-9_./:\\-]+", text):
        return text
    if not re.search(r'["$`\\]', text):
        return f'"{text}"'
    if "'" not in text:
        return f"'{text}'"
    return '"' + re.sub(r'(["\\`$])', r"\\\1", text) + '"'


def _probe_args(task: str, dispatch: str, node: str, iid: str, mutation: str, oracle: str, at="") -> list:
    """The probe's own flags. `at` is the line a probe of a test that is not Python was pointed at (B-373: the
    assertion to invert, and which declaration when a name repeats): without it the replay would pick the
    FIRST assertion again, which is not the assertion that probe proved."""
    args = ["--task", task, "--dispatch", dispatch, "--test", node, "--instance", iid,
            "--mutation", mutation]
    if oracle:
        args += ["--oracle", oracle]
    if str(at or "").strip():
        args += ["--at", str(at).strip()]
    return args + ["--json"]


def _command(args: list) -> str:
    """The exact line, in the shape the critic's tooling card gives `probe_by_code.py`."""
    out, index = ["probe_by_code.py"], 0
    while index < len(args):
        flag = args[index]
        if flag == "--json":
            out.append(flag)
            index += 1
        else:
            out += [flag, _quote(args[index + 1])]
            index += 2
    return " ".join(out)


# --- the oracle a replay would name ----------------------------------------------------------------

def _oracle_gone(project, rel: str, function: str) -> str:
    """"" when `function` is defined exactly once in the project's `rel`; else the reason it cannot be
    replayed. `probe_by_code.locate` is the probe's own lookup, so code never replays what the probe
    would refuse."""
    if project is None:
        return "the project root cannot be found, so the oracle file cannot be read"
    path = Path(project) / rel
    try:
        data = path.read_bytes() if path.is_file() else None
    except OSError:
        data = None
    if data is None:
        return f"the file {rel} is gone"
    if not str(rel).endswith(".py"):
        return (f"{rel} is not a Python file, and code replays only the oracle it can locate by AST; a helper of "
                "another language is named again with --oracle")
    try:
        import ast
        text = data[3:] if data.startswith(b"\xef\xbb\xbf") else data
        tree = ast.parse(text.decode("utf-8"))
    except (SyntaxError, UnicodeDecodeError, ValueError) as exc:
        return f"{rel} does not parse ({type(exc).__name__})"
    try:
        PBC.locate(tree, [], function)
    except PBC.Refusal as exc:
        return str(exc)
    return ""


def _replay_plan(record: dict, project) -> tuple:
    """(node, mutation, oracle, at, why_left): what `probe_by_code.py` is called with to replay this
    record's own probe, or why code does not (V6: `--oracle <file>::<function>` whenever the record
    has an oracle function; the critic's only when that function is gone). `at` is the `--at` line the
    probe of a test that is not Python was given (`mutation_detail.at`), "" when it had none."""
    node = _posix(record.get("test_node")).strip()
    mutation = record.get("mutation")
    if "::" not in node:
        return node, "", "", "", ("the record names no test node (test_node), and code does not guess "
                                  "which test to probe")
    if mutation not in PBC.MUTATIONS:
        return node, "invert", "", "", (f"the record's mutation {mutation!r} is not one this tool "
                                        f"replays ({', '.join(PBC.MUTATIONS)})")
    detail = record.get("mutation_detail") if isinstance(record.get("mutation_detail"), dict) else {}
    at = detail.get("at")
    at = str(at) if isinstance(at, int) and not isinstance(at, bool) else ""
    function = str(detail.get("oracle_function") or "")
    test_file = node.split("::", 1)[0]
    named = str(detail.get("file") or "")
    if not function:
        if named and not _same_file(named, test_file):
            return node, mutation, "", at, (f"the probe mutated {named}, not the test, and the record names "
                                            "no oracle function to replay")
        return node, mutation, "", at, ""
    moved = record.get("mutated_file") if isinstance(record.get("mutated_file"), dict) else {}
    where = _posix(moved.get("path") or named or test_file)
    gone = _oracle_gone(project, where, function)
    if gone:
        return node, mutation, "", at, (f"the oracle function {function} cannot be replayed from {where} "
                                        f"({gone}); the critic names where the expectation lives now "
                                        "(--oracle [<file>::]<function>)")
    return node, mutation, f"{where}::{function}", at, ""


# --- the detector ----------------------------------------------------------------------------------

def _scan(task_root, manifest, project=None, dispatch: str = "") -> dict:
    """`find`'s work, with the private handle `settle` needs (`_args`) still on the items."""
    out = {"items": [], "info": []}
    if not isinstance(manifest, dict):
        return out
    task_root = Path(task_root)
    task = task_root.name
    project = _project_of(project)
    shown_dispatch = dispatch or "<the open S5 qa-code-critic dispatch id>"
    claimed, seen = set(), set()
    for row in C.manifest_tests(manifest):
        aliases = _aliases(row)
        claimed.update(PL.probe_record_path(task_root, a).name for a in aliases)
        if not aliases or seen & set(aliases):   # the same instance under another spelling: one item
            continue
        seen.update(aliases)
        path = next((p for p in (PL.probe_record_path(task_root, a) for a in aliases) if p.is_file()), None)
        if path is None:
            continue
        rel = path.relative_to(task_root).as_posix()
        iid = aliases[0]
        record, why = _read_json_file(path)
        if record is None:
            out["info"].append({"instance_id": iid, "record": rel, "recorded_at": "",
                                "why": f"unreadable: the probe record {rel} cannot be read ({why}); "
                                       "no action is taken on it"})
            continue
        if record.get("verdict") != "intended_failure":
            continue
        try:
            if not PL.proof_required(row, manifest):
                reason = PL.not_required_why(row, manifest)
                out["info"].append({
                    "instance_id": iid, "record": rel, "recorded_at": str(record.get("recorded_at") or ""),
                    "why": (f"a live probe passed, but this row is not required to have one "
                            f"({reason or 'not required'}): no action")})
                continue
            now = PL.instance_identity(row, task_root, project)
            if PL.reached(row, manifest, task_root, now=now)["level"] is not None:
                continue
            out["items"].append(_item(task, shown_dispatch, task_root, project, row, iid, record, rel))
        except Exception as exc:  # an unknown is told, never a fact (FR-41) and never a stop (P1)
            out["info"].append({"instance_id": iid, "record": rel,
                                "recorded_at": str(record.get("recorded_at") or ""),
                                "why": f"could not be checked ({type(exc).__name__}: {str(exc)[:160]}): "
                                       "no action is taken on it"})
    records_dir = PL.probe_record_path(task_root, "x").parent
    for path in sorted_paths(records_dir.glob("*.json")) if records_dir.is_dir() else []:
        if path.name in claimed:
            continue
        rel = path.relative_to(task_root).as_posix()
        record, why = _read_json_file(path)
        if record is None:
            out["info"].append({"instance_id": "", "record": rel, "recorded_at": "",
                                "why": f"unreadable: the probe record {rel} cannot be read ({why}); "
                                       "no action is taken on it"})
        elif record.get("verdict") == "intended_failure":
            out["info"].append({
                "instance_id": str(record.get("instance_id") or ""), "record": rel,
                "recorded_at": str(record.get("recorded_at") or ""),
                "why": (f"row gone: the manifest has no row for "
                        f"{record.get('test_node') or record.get('instance_id') or 'this record'} "
                        "any more: no action")})
    return out


def _item(task, dispatch, task_root, project, row, iid, record, rel) -> dict:
    measured = str(record.get("test_file_sha256") or "")
    bound = _bound_sha(row)
    current = PL.current_test_sha(row, project)
    node, mutation, oracle, at, left = _replay_plan(record, project)
    args = _probe_args(task, dispatch, node, iid, mutation or "invert", oracle, at) if "::" in node else []
    if not current:
        left = left or (f"the test file {PL.test_file_of(row) or '(the row names none)'} cannot be found "
                        "under the project: there are no current bytes to probe")
    if left:
        action, why = LEAVE_TO_CRITIC, left
    elif bound != current:
        action = REBIND_AND_REPROBE
        why = (f"the row binds test bytes {_short(bound)} but the file is now {_short(current)} (the "
               f"probe measured {_short(measured)}): rebind the row with manifest_from_tests.py, then "
               "probe the current bytes again")
    else:
        action = REPROBE
        why = (f"a live probe passed on {_short(measured)} but no valid receipt stands for the current "
               f"bytes {_short(current)}: probe them again (a fresh probe is valid through the "
               "receipt's own equality check)")
    return {"instance_id": iid, "case": _case_of(row, record), "record": rel,
            "recorded_at": str(record.get("recorded_at") or ""), "measured_sha": measured,
            "bound_sha": bound, "current_sha": current, "action": action, "why": why,
            "command": _command(args) if args else "", "_args": args}


def _public(item: dict) -> dict:
    return {k: v for k, v in item.items() if not k.startswith("_")}


def find(task_root, manifest, project=None, dispatch: str = "") -> dict:
    """{"items": [...], "info": [...]}: the probe debt of a story. Read-only - nothing is written,
    and no receipt or manifest field is made here (FR-45). `manifest` that is not an object gives
    the empty result. `dispatch` only spells the `command` of each item (the critic's own id);
    without it the command carries a placeholder."""
    found = _scan(task_root, manifest, project, dispatch)
    return {"items": [_public(i) for i in found["items"]], "info": found["info"]}


# --- the processes ---------------------------------------------------------------------------------

def run_process(argv: list, *, cwd, timeout) -> tuple:
    """(returncode, stdout, stderr). The one place a subprocess is started; tests inject their own."""
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    if cwd:
        env["CLAUDE_PROJECT_DIR"] = str(cwd)
    proc = subprocess.run(argv, cwd=str(cwd) if cwd else None, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", timeout=timeout, env=env)
    return proc.returncode, proc.stdout or "", proc.stderr or ""


def _script(env_name: str, name: str) -> str:
    return os.environ.get(env_name) or str(Path(__file__).resolve().parent / name)


def _json_of(text: str):
    text = str(text or "").strip()
    for start in (0, text.find("{")):
        if start < 0:
            continue
        try:
            value = json.loads(text[start:])
        except ValueError:
            continue
        return value
    return None


def _fold(text, limit: int = 240) -> str:
    text = " ".join(str(text or "").split())
    return text if len(text) <= limit else text[:limit - 3] + "..."


def stand_state(project) -> tuple:
    """(busy, words): is the stand leased by a live run right now? Read-only. `run_suite` holds the
    stand through `stand_lease.hold` (it waits, then gives up with `StandBusy`); waiting for it is
    exactly what a settle must not do, so this asks `stand_lease.status` the same question - a lease
    whose holder is not proven gone keeps the stand (`_holder_alive`). A stand that takes parallel
    runs has no lease and is never busy here. Anything that cannot be asked is "not busy": the first
    probe's own outcome is then the check (V1)."""
    try:
        cfg = json.loads((Path(project) / "qa-factory" / "config.json").read_text(encoding="utf-8-sig"))
    except (OSError, ValueError, TypeError):
        cfg = {}
    try:
        import run_suite
        if not run_suite.stand_is_serial(cfg if isinstance(cfg, dict) else {}):
            return False, ""
        import stand_lease
        held = [lease for lease in stand_lease.status(project).get("leases") or []
                if isinstance(lease, dict) and lease.get("holder") != "gone"]
    except Exception:
        return False, ""
    if not held:
        return False, ""
    lease = held[0]
    return True, (f"the stand {lease.get('environment') or 'default'} is held by run "
                  f"{lease.get('job_id') or '?'} (pid {lease.get('pid') or '?'}, since "
                  f"{lease.get('acquired_at') or '?'})")


# --- controller state ------------------------------------------------------------------------------

def _controller(task_root) -> dict:
    value, _why = _read_json_file(Path(task_root) / "state" / "controller.json")
    return value or {}


def _dispatch_rows(task_root) -> list:
    rows = _controller(task_root).get("dispatches")
    return [d for d in rows.values() if isinstance(d, dict)] if isinstance(rows, dict) else []


def open_critic_dispatch(task_root, dispatch_id: str) -> tuple:
    """(record or None, words): is `dispatch_id` an open (running) S5 qa-code-critic dispatch?"""
    rows = _controller(task_root).get("dispatches")
    record = rows.get(dispatch_id) if isinstance(rows, dict) else None
    if isinstance(record, dict) and (record.get("status"), record.get("stage"), record.get("role")) == (
            "running", "S5", "qa-code-critic"):
        return record, ""
    if isinstance(record, dict):
        seen = (f"it is {record.get('role') or '?'} on {record.get('stage') or '?'}, status "
                f"{record.get('status') or '?'}")
    else:
        seen = "the story's controller state has no such dispatch"
    open_ones = [str(d.get("id")) for d in _dispatch_rows(task_root)
                 if d.get("status") == "running" and d.get("stage") == "S5"
                 and d.get("role") == "qa-code-critic"]
    return None, (f"--dispatch {dispatch_id!r} is not an open S5 qa-code-critic dispatch ({seen}). "
                  "Pass the id `story_step.py start` registered for the critic"
                  + (f" (open now: {', '.join(open_ones)})" if open_ones else " (none is open now)"))


def _author_dispatch(task_root) -> str:
    """The latest ACCEPTED S5 qa-automator WINDOW dispatch: the controller's own order (`prior[-1]`), the window kind of it.
    The PLAN author (SC1-14 B1a) wrote no test the probe debt could be about, so it is never the author a rebind is made in
    the name of: `controller.s5_part_of` is the one reader of the kind."""
    from controller import s5_part_of
    found = [d for d in _dispatch_rows(task_root)
             if d.get("stage") == "S5" and d.get("role") == "qa-automator" and d.get("status") == "accepted"
             and s5_part_of(d) != "plan"]
    return str(found[-1].get("id") or "") if found else ""


# --- the settle ------------------------------------------------------------------------------------

def _live_ids(manifest: dict) -> set:
    """Every spelling of every row the manifest still holds (a retracted one is not one)."""
    ids = set()
    for row in C.manifest_tests(manifest):
        ids.update(PL.without_retracted(_aliases(row), manifest))
    return ids


def _row_named(manifest: dict, iid: str):
    for row in C.manifest_tests(manifest):
        if iid in _aliases(row):
            return row
    return None


class RebindBudget(Exception):
    """A rebind step that could not finish inside what is left of the settle's budget."""


def _rebind_call(ctx: dict, argv: list, what: str) -> tuple:
    """One `manifest_from_tests.py` subprocess, bounded by the time LEFT of the settle's budget (and by
    MANIFEST_PROCESS_TIMEOUT_S): the budget bounds the whole `story_step start`, and a rebind used to be
    free to take 2 x 120 s. No time left, or a timeout, is `RebindBudget`; the item keeps its old binding
    and is left with reason `budget`. (A kill of the write is safe for the manifest only as far as
    manifest_put's own atomic write is - `_rebind` re-reads the row afterwards and trusts nothing else.)"""
    left = ctx["budget_s"] - (ctx["clock"]() - ctx["begun"])
    if left <= 0:
        raise RebindBudget(f"the settle's time budget of {ctx['budget_s']:g} s was used up before the rebind "
                           f"{what} could start: " + REBIND_LEFT)
    try:
        return ctx["runner"](argv, cwd=ctx["project"], timeout=min(MANIFEST_PROCESS_TIMEOUT_S, left))
    except subprocess.TimeoutExpired:
        raise RebindBudget(f"the rebind {what} did not finish in the {left:.0f} s left of the settle's time "
                           "budget: " + REBIND_LEFT) from None


def _rebind(ctx: dict, item: dict) -> tuple:
    """(ok, words). Bring the row's binding to the file's current bytes through
    `manifest_from_tests.py`, a subprocess - and write ONLY when the dry run would write ids the
    manifest already holds under some alias: a source-spelled id that is not a collected one would
    make a ghost row beside the collected ones (FR-16). Anything else keeps the item."""
    task_root, project = ctx["task_root"], ctx["project"]
    manifest = _read_manifest(task_root)
    row = _row_named(manifest, item["instance_id"])
    if row is None:
        return False, "the row is gone from the manifest: " + REBIND_LEFT
    current = PL.current_test_sha(row, project)
    if current and _bound_sha(row) == current:
        return True, "the row already binds the current bytes (an earlier rebind of the same file)"
    if not ctx["author"]:
        return False, ("no accepted S5 qa-automator dispatch to attribute the rebind to: "
                       + REBIND_LEFT)
    files = [f for f in row.get("generated_from") or [] if isinstance(f, str) and f.strip()] \
        if isinstance(row.get("generated_from"), list) else []
    files = files or [PL.test_file_of(row)]
    head = [sys.executable, "-B", ctx["manifest_script"], "--task", ctx["task"],
            "--dispatch", ctx["author"]]
    for name in files:
        head += ["--file", name]
    try:
        rc, out, err = _rebind_call(ctx, head + ["--dry-run", "--json"], "dry run")
    except RebindBudget:
        raise
    except Exception as exc:
        return False, f"the rebind dry run did not run ({type(exc).__name__}: {_fold(exc)}): " + REBIND_LEFT
    dry = _json_of(out)
    if rc != 0 or not isinstance(dry, dict) or dry.get("ok") is not True:
        said = (dry.get("refusal") if isinstance(dry, dict) and dry.get("refusal") else
                (err or out or "no output"))
        return False, f"the rebind dry run failed (exit {rc}: {_fold(said)}): " + REBIND_LEFT
    fragment = dry.get("fragment") if isinstance(dry.get("fragment"), dict) else {}
    wanted = [str(t.get("instance_id") or "") for t in fragment.get("tests") or [] if isinstance(t, dict)]
    if not wanted or not (set(_aliases(row)) & set(wanted)):
        return False, ("the dry run would not write this instance, so it would not rebind it: "
                       + REBIND_LEFT)
    unknown = sorted(i for i in wanted if i not in _live_ids(manifest))
    if unknown:
        return False, (f"the dry run would write {len(unknown)} id(s) the manifest does not hold "
                       f"({', '.join(unknown[:3])}{'...' if len(unknown) > 3 else ''}): a new spelling "
                       "of an id would make a ghost row: " + REBIND_LEFT)
    try:
        rc, out, err = _rebind_call(ctx, head, "write")
    except RebindBudget:
        raise
    except Exception as exc:
        return False, f"the rebind did not run ({type(exc).__name__}: {_fold(exc)}): " + REBIND_LEFT
    if rc != 0:
        return False, f"the rebind was refused (exit {rc}: {_fold(err or out)}): " + REBIND_LEFT
    again = _row_named(_read_manifest(task_root), item["instance_id"])
    if again is None or _bound_sha(again) != PL.current_test_sha(again, project):
        return False, ("the rebind ran but the row still does not bind the current bytes, so no probe "
                       "is made on other bytes: " + REBIND_LEFT)
    return True, f"rebound by manifest_from_tests.py ({', '.join(files)})"


def _scope_word(task_root, dispatch_record, case: str, dispatch: str, scope: list) -> str:
    """The person's recorded word that passes the scope block for this case, or "". `build_mine_request`
    looks it up with the block's own sentence (`execution_request.person_passed`, matched by whole words
    against the stage's `stage_overrides[]`); the same sentence is built here from the same constant,
    so a waiver that passes the probe's refusal passes this pre-check too - a pre-check stricter than
    the tool would leave to the critic what a person already let through."""
    try:
        import execution_request as ER
        stage = str((dispatch_record or {}).get("stage") or "S5")
        return ER.person_passed(Path(task_root), stage, ER.scope_refusal([case], dispatch, scope, stage))
    except Exception:   # a lookup that cannot be made is "no word": the item goes to the critic
        return ""


def _outside_scope_door(task_root, dispatch_record, item, dispatch: str, scope: list) -> str:
    """Which door lets an item of a case OUTSIDE the dispatch's scope through: "stale" (the row's live check went
    stale - `proof_level.reprobe_admitted`, FB-10: re-probed by the critic of the window that finds it; its review is
    not re-checked), "word" (a person's recorded word, `_scope_word`), or "" (none). Asked in `build_mine_request`'s
    order, on the manifest read NOW (the probe subprocess reads it when it starts, after every rebind that came
    before it, so the two askings see the same rows). A stale item that also holds a word keeps the word when the
    stale door closed. Anything that cannot be told is "no": the item goes to the critic with the refusal."""
    try:
        manifest = _read_manifest(task_root)
        row = _row_named(manifest, item["instance_id"])
        if row is not None and PL.reprobe_admitted(row, manifest, task_root)[0]:
            return "stale"
    except Exception:
        pass
    return "word" if _scope_word(task_root, dispatch_record, item["case"], dispatch, scope) else ""


def _scope_left(outcomes: list, leave, item: dict, dispatch_record, dispatch: str, scope: list) -> None:
    """The item stays with the critic: `outside_scope`, in the one sentence of `execution_request.scope_refusal`."""
    import execution_request as ER
    words = ER.scope_refusal([item["case"] or "(no case)"], dispatch, scope,
                             str((dispatch_record or {}).get("stage") or "S5"))
    outcomes.append({"instance_id": item["instance_id"], "step": "probe", "result": "outside_scope", "words": words})
    leave(item, "scope", words)


def _classify(rc: int, out: str, err: str) -> dict:
    """What one `probe_by_code.py --json` call did: {result, words, settled, stop}."""
    data = _json_of(out)
    if not isinstance(data, dict):
        return {"result": "error", "settled": False, "stop": False,
                "words": f"exit {rc}, stdout is not the probe's JSON: {_fold(err or out or 'no output')}"}
    if data.get("status") == "refused":
        return {"result": "refused", "settled": False, "stop": False,
                "words": f"the probe refused: {_fold(data.get('error'))}"}
    verdict = str(data.get("verdict") or "")
    if verdict == "already_probed":
        return {"result": "already_probed", "settled": data.get("by") == "receipt", "stop": False,
                "words": _fold(data.get("words"))}
    notes = [str(n) for n in data.get("notes") or []]
    unrestored = not (data.get("restore") or {}).get("verified")
    if verdict == "intended_failure":
        published = (data.get("publish") or {}).get("published") is True \
            and isinstance(data.get("receipt"), dict)
        if published:
            return {"result": "published", "settled": True, "stop": unrestored,
                    "words": f"receipt {data['receipt'].get('path')}"}
        missing = ", ".join(data.get("receipt_missing") or [])
        return {"result": "unpublished", "settled": False, "stop": unrestored,
                "words": "the probe passed but no receipt was published"
                         + (f" (missing: {missing})" if missing else "")
                         + (f": {_fold(notes[-1])}" if notes else "")}
    if verdict == "not_executed":
        return {"result": "not_executed", "settled": False, "stop": True,
                "words": "nothing ran" + (f": {_fold(notes[-1])}" if notes else "")}
    return {"result": verdict or "error", "settled": False, "stop": unrestored,
            "words": (f"the probe said {verdict}" if verdict else f"exit {rc}, no verdict")
                     + (f": {_fold(notes[-1])}" if notes else "")}


def _previous_attempts(task_root) -> dict:
    """{instance_id: entry} - the items an earlier settle probed that ended `not_executed`, each with
    the bytes it was probed on (`current_sha`), read from the debt file that settle left. Anything that
    cannot be read is "no memory": the item is probed again, which errs toward running."""
    doc, _why = _read_json_file(Path(task_root) / DEBT_REL)
    out = {}
    for entry in (doc or {}).get("last_attempts") or []:
        if (isinstance(entry, dict) and entry.get("instance_id") and entry.get("current_sha")
                and entry.get("result") == "not_executed"):
            out[str(entry["instance_id"])] = entry
    return out


def settle(task: str, task_root, project, dispatch: str, *, dispatch_record: dict | None = None,
           runner=None, clock=None, stand=None, budget_s: float = SETTLE_BUDGET_S,
           limit: int = SETTLE_LIMIT) -> dict:
    """Clear the probe debt that code may clear; return (and record) what happened.

    Per item, in order: rebind (when the row binds other bytes than the file has), then a fresh
    probe. `runner(argv, cwd=, timeout=) -> (returncode, stdout, stderr)`, `clock() -> seconds` and
    `stand() -> (busy, words)` are injected by tests; the defaults are real.
    The doc returned is what `work/probe-debt.json` holds: `outcomes` (what each step did), `left`
    (the items still owed, each with its `reason` and `reason_words`), `info`, `budget`, and
    `last_attempts` (the items whose probe ended `not_executed`, with the bytes they were probed on:
    the next settle does not probe the same bytes again)."""
    runner = runner or run_process
    clock = clock or time.monotonic
    task_root, project = Path(task_root), _project_of(project)
    begun = clock()
    previous = _previous_attempts(task_root)   # read BEFORE this settle rewrites the file
    attempts, longest = [], 0.0
    manifest = _read_manifest(task_root)
    found = _scan(task_root, manifest, project, dispatch)
    ctx = {"task": task, "task_root": task_root, "project": project, "runner": runner,
           "clock": clock, "begun": begun, "budget_s": budget_s,
           "author": _author_dispatch(task_root),
           "manifest_script": _script(MANIFEST_SCRIPT_ENV, "manifest_from_tests.py")}
    probe_script = _script(PROBE_SCRIPT_ENV, "probe_by_code.py")
    scope = None
    if isinstance(dispatch_record, dict):   # what build_mine_request checks before it builds a run
        scope = [str(s) for s in dispatch_record.get("scope") or []]
    outcomes, left, attempted, stopped = [], [], 0, ("", "")

    def leave(item, reason, words):
        left.append({**_public(item), "reason": reason, "reason_words": words})

    actionable = [i for i in found["items"] if i["action"] != LEAVE_TO_CRITIC]
    busy, busy_words = (False, "")
    if actionable:
        try:
            busy, busy_words = (stand or (lambda: stand_state(project)))()
        except Exception:
            busy, busy_words = False, ""
    for item in found["items"]:
        iid = item["instance_id"]
        if item["action"] == LEAVE_TO_CRITIC:
            leave(item, "critic", item["why"])
            continue
        last = previous.get(iid)
        if last and last["current_sha"] == item["current_sha"]:
            # An attempt on THESE bytes already ended not_executed (a stand down, a run cut short): the
            # same call would end the same way, so it is not repeated at every critic start. Carried
            # forward as it was; a changed file has a new sha and is probed again.
            attempts.append(last)
            leave(item, "same_bytes", f"same bytes as the last attempt ({_short(last['current_sha'])}), which "
                  f"ended not_executed at {last.get('recorded_at') or '?'}: nothing was started; the critic "
                  "runs its command")
            continue
        if busy:
            leave(item, "stand", f"the stand is busy, nothing was started: {busy_words}")
            continue
        if stopped[0]:
            leave(item, stopped[0], stopped[1])
            continue
        if attempted >= limit:
            stopped = ("limit", f"the settle probes at most {limit} instances in one go")
            leave(item, *stopped)
            continue
        remaining = budget_s - (clock() - begun)
        if remaining <= 0:
            stopped = ("budget", f"the settle's time budget of {budget_s:g} s was used up")
            leave(item, *stopped)
            continue
        if attempted and remaining < longest:
            # The budget bounds the WHOLE call (the skill road's shell call times out), and a probe that
            # begins is not cut short: so one that cannot be expected to fit does not begin. The longest
            # probe of this settle is the estimate; the first one has none and always runs.
            stopped = ("budget", f"the settle's time budget of {budget_s:g} s has {remaining:.0f} s left, and "
                                 f"the longest probe so far took {longest:.0f} s: the next one would not fit")
            leave(item, *stopped)
            continue
        door = ""
        if scope is not None and item["case"] not in scope:
            door = _outside_scope_door(task_root, dispatch_record, item, dispatch, scope)
            if not door:
                _scope_left(outcomes, leave, item, dispatch_record, dispatch, scope)
                continue
        if item["action"] == REBIND_AND_REPROBE:
            try:
                ok, words = _rebind(ctx, item)
            except RebindBudget as exc:   # the budget ended inside the rebind: nothing is probed on other bytes
                outcomes.append({"instance_id": iid, "step": "rebind", "result": "kept", "words": str(exc)})
                stopped = ("budget", str(exc))
                leave(item, *stopped)
                continue
            except Exception as exc:
                ok, words = False, f"the rebind failed ({type(exc).__name__}: {_fold(exc)}): " + REBIND_LEFT
            outcomes.append({"instance_id": iid, "step": "rebind", "result": "rebound" if ok else "kept",
                             "words": words})
            if not ok:   # other bytes than the row binds would produce a receipt nobody can use
                leave(item, "rebind", words)
                continue
            if door == "stale" and not _outside_scope_door(task_root, dispatch_record, item, dispatch, scope):
                # R6b: ask again after the rebind (it may re-pin the case or drop the novelty); the word door is
                # asked in the same call, so a stale item that holds a person's word goes on
                _scope_left(outcomes, leave, item, dispatch_record, dispatch, scope)
                continue
        remaining = budget_s - (clock() - begun)   # a rebind above took time of its own
        if remaining <= 0:
            stopped = ("budget", f"the settle's time budget of {budget_s:g} s was used up by the rebind")
            leave(item, *stopped)
            continue
        attempted += 1
        # The probe's OWN `--timeout` is the time left (at least one second): when it runs out the probe
        # restores the author's bytes and ends `not_executed`. Killing the process instead would skip
        # that restore - probe_by_code.probe() mutates the file in place and puts it back in a `finally`.
        # The process timeout is only the net under a HUNG probe. `--timeout` goes after `--json`, and
        # only here: the `command` the critic copies (`_args`) keeps the probe's own default.
        remaining = max(1, int(remaining))
        started = clock()
        try:
            rc, out, err = runner([sys.executable, "-B", probe_script, *item["_args"], "--timeout",
                                   str(remaining)], cwd=project,
                                  timeout=min(PROBE_PROCESS_TIMEOUT_S, remaining + PROBE_PROCESS_MARGIN_S))
            result = _classify(rc, out, err)
        except Exception as exc:   # an OSError or a hung probe: told, and the next item goes on
            result = {"result": "exception", "settled": False, "stop": False,
                      "words": f"the probe did not run ({type(exc).__name__}: {_fold(exc)})"}
        longest = max(longest, clock() - started)
        if result["result"] == "not_executed":
            attempts.append({"instance_id": iid, "current_sha": item["current_sha"], "result": "not_executed",
                             "recorded_at": datetime.now(timezone.utc).isoformat(timespec="seconds")})
        outcomes.append({"instance_id": iid, "step": "probe", "result": result["result"],
                         "words": result["words"]})
        if not result["settled"]:
            leave(item, result["result"], result["words"])
        if result["stop"]:
            stopped = ("stopped", f"an earlier probe ended {result['result']} ({item['instance_id']}): "
                                  "nothing more is started")
    doc = {"schema_version": SCHEMA_VERSION, "task": task, "dispatch": dispatch,
           "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "outcomes": outcomes, "left": left, "info": found["info"], "last_attempts": attempts,
           "budget": {"budget_s": budget_s, "elapsed_s": round(clock() - begun, 1), "limit": limit,
                      "probes_started": attempted, "stand_busy": bool(busy)}}
    path = task_root / DEBT_REL
    if found["items"] or found["info"]:   # no item and no info row: no file is CREATED
        atomic_json(path, doc)
    elif path.is_file():
        # A file an earlier settle left is REWRITTEN, empty: the reader adds it to the critic's inputs
        # whenever it exists, and what it lists is done (Lead, t-177 Q2).
        doc["settled_at"] = doc["generated_at"]
        atomic_json(path, doc)
    return doc


# --- the command line ------------------------------------------------------------------------------

def _print_find(result: dict) -> None:
    print(f"probe debt: {len(result['items'])} item(s), {len(result['info'])} info row(s)")
    for item in result["items"]:
        print(f"  {item['instance_id']} - {item['action']}: {item['why']}")
        if item["command"]:
            print(f"    command: {item['command']}")
    for row in result["info"]:
        print(f"  info {row['instance_id'] or row['record']}: {row['why']}")


def _print_settle(doc: dict) -> None:
    print(f"probe debt settle: {len(doc['outcomes'])} step(s), {len(doc['left'])} left for the critic, "
          f"{len(doc['info'])} info row(s)")
    for one in doc["outcomes"]:
        print(f"  {one['instance_id']} {one['step']} - {one['result']}: {one['words']}")
    for item in doc["left"]:
        print(f"  left {item['instance_id']} ({item['reason']}): {item['reason_words']}")
        if item["command"]:
            print(f"    command: {item['command']}")


def main(argv=None, **injected) -> int:
    C.force_utf8()
    ap = argparse.ArgumentParser(description="probe debt: a live probe passed, no receipt stands")
    ap.add_argument("--task", required=True, help="the ticket id")
    ap.add_argument("--settle", action="store_true",
                    help="rebind and re-probe what code may, record the rest in work/probe-debt.json")
    ap.add_argument("--dispatch", default="",
                    help="the open S5 qa-code-critic dispatch id (required with --settle)")
    ap.add_argument("--budget-s", type=float, default=None, dest="budget_s",
                    help=f"--settle only: the wall-clock seconds the whole settle may take (default "
                         f"{SETTLE_BUDGET_S}); `story_step.py start` passes what is left of its own")
    ap.add_argument("--json", action="store_true", help="print JSON, and nothing else, on stdout")
    ns = ap.parse_args(argv)
    if ns.settle and not ns.dispatch:
        ap.error("--settle needs --dispatch <open S5 qa-code-critic dispatch id> (the one "
                 "`story_step.py start` registered for the critic)")
    if ns.budget_s is not None:
        if not ns.settle:
            ap.error("--budget-s belongs to --settle: add --settle --dispatch <id>, or leave it out")
        if not 0 < ns.budget_s < float("inf"):
            ap.error(f"--budget-s must be a number of seconds above 0 (got {ns.budget_s:g}); leave it out "
                     f"for the default of {SETTLE_BUDGET_S}")
    if ns.budget_s is not None:
        injected = dict(injected, budget_s=ns.budget_s)
    try:
        from hooklib import artifacts_dir
        task_root = artifacts_dir(ns.task)
    except ValueError as exc:
        print(f"probe_debt: {exc}", file=sys.stderr)
        return 2
    if not task_root.is_dir():
        print(f"probe_debt: no story folder {task_root}: --task is the ticket id of a story the "
              "factory has started", file=sys.stderr)
        return 2
    record = None
    if ns.settle:
        record, words = open_critic_dispatch(task_root, ns.dispatch)
        if record is None:
            print("probe_debt: " + words, file=sys.stderr)
            return 2
    try:
        if ns.settle:
            doc = settle(ns.task, task_root, None, ns.dispatch, dispatch_record=record, **injected)
            result = doc
        else:
            result = find(task_root, _read_manifest(task_root), None, ns.dispatch)
    except Exception as exc:   # code tells; it does not stop the factory (P1)
        print(f"probe_debt: could not finish ({type(exc).__name__}: {_fold(exc)})", file=sys.stderr)
        return 0
    if ns.json:
        print(json.dumps(result, ensure_ascii=False, indent=1))
    elif ns.settle:
        _print_settle(result)
    else:
        _print_find(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
