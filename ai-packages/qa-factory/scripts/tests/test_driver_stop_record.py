#!/usr/bin/env python3
"""TR4-11 (t-2222 items 11.1 and 11.2, part B1): the person's stop is a record, and the driver's journal goes through the one appender.

Expectations are the spec's (docs/tasks/specs/t-2222-tr4-10-11-s5-windows-leftovers.md items 11.1, 11.2) and the plan critic's F-1, F-3, F-8
(docs/tasks/specs/reviews/t-2227-tr4-10-11-plan-critic.md), not what the code prints (FR-58).

11.1  Ctrl-C on either road of `Driver.run` writes ONE `stopped_by_person` row to driver-runs.jsonl through `journal_run`, with
      `since` (the process start) and `cut` (the calls this process launched and saw no end for); the interrupt is re-raised.
      No story folder -> nothing written; a failed write -> one note, still re-raised; a second Ctrl-C while writing -> no traceback past
      `run`, a record already written is kept; an interrupt inside a run-level handler (funnel) writes it too (F-3).
      `collect_stall` clears exactly the rows in `cut` (round trip with a real `Driver`; the id form is a twin of K3's, tied here).
11.2  `_append_jsonl` is `hooklib.append_jsonl_line`: a torn tail is repaired, no private `open(..., "a")` is left in the driver set,
      a journal of mixed CRLF / LF lines (the Windows text-mode rows of before) is read whole by every reader of the file (F-8).

Nothing here reaches the network, a model or a subprocess.

Run:  python -B scripts/tests/test_driver_stop_record.py
"""
import contextlib
import io
import json
import re
import subprocess
import sys
import threading
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from harness import SCRIPTS, check, check_eq, cleanup, finish, temp_dir  # noqa: E402

sys.path.insert(0, str(SCRIPTS))
import collect_stall as CS  # noqa: E402
import detector_verdict as DV  # noqa: E402
import driver_journal as DJ  # noqa: E402
import story_run as SR  # noqa: E402
from role_cli import REPAIR_MARKER  # noqa: E402

NAME = "driver-runs.jsonl"


def rig(root: Path, with_state_dir: bool = True):
    """A bare Driver whose `run` can be driven: every step before the loop is a no-op, the loop asks `where` and `boundary_step`."""
    d = SR.Driver.__new__(SR.Driver)
    d.task = "QA-STOP"
    d.task_root = root / "artifacts" / "QA-STOP"
    d.state_dir = d.task_root / "state"
    d.task_root.mkdir(parents=True)
    (d.task_root / "pipeline.json").write_text("{}", encoding="utf-8")
    if with_state_dir:
        d.state_dir.mkdir()
    d.state, d.flags, d.answer_kind, d.max_boundaries, d.until = {}, SimpleNamespace(answer=None), None, 3, None
    d.progress_line = lambda: None
    d.reconcile_question = lambda: None
    for name in ("owed_rows_step", "adopt_legacy_snapshot", "check_run_mode", "report_gap_class_problem", "skip_sources_late",
                 "ticket_freshness_entry", "accept_no_trace"):
        setattr(d, name, lambda *a, **k: None)
    for name in ("ticket_rework_step", "seam_rework_step", "answer_rework_step", "code_close_step", "consumer_word_step"):
        setattr(d, name, lambda *a, **k: False)
    d.guarded = lambda fn, record=None: fn()
    d.where = lambda: {"action": "dispatch"}
    d.until_reached = lambda action: False
    d.boundary_step = lambda action: None
    return d


def rows_of(d):
    path = d.state_dir / NAME
    return [json.loads(line) for line in path.read_text(encoding="utf-8").split("\n") if line.strip()] if path.is_file() else []


def stops(d):
    return [r for r in rows_of(d) if r.get("kind") == "stopped_by_person"]


def run_catching(d):
    """`d.run()`; what it raised (the case reads it) and what it printed."""
    out, error = io.StringIO(), None
    with contextlib.redirect_stdout(out):
        try:
            d.run()
        except BaseException as exc:  # noqa: BLE001 - the interrupt itself is the thing under test
            error = exc
    return error, out.getvalue()


def launch(d, call="role", dispatch="S5-x-1", at="2026-11-10T10:00:00+00:00"):
    d.journal_run({"kind": "launched", "call": call, "role": "r", "dispatch_id": dispatch, "stage": "S5", "started_at": at})


def end(d, kind="role", dispatch="S5-x-1"):
    d.journal_run({"kind": kind, "role": "r", "dispatch": dispatch, "stage": "S5", "exit_code": 0, "is_error": False, "infra": None})


# --- 11.1 ----------------------------------------------------------------------------------------------------------------------------
def ctrl_c_serial_writes_one_stop_record(tmp):
    d = rig(tmp / "serial")

    def interrupt():
        raise KeyboardInterrupt()
    d.reconcile_question = interrupt
    error, out = run_catching(d)
    found = stops(d)
    check("ctrl_c_serial_writes_one_stop_record: the interrupt is re-raised", isinstance(error, KeyboardInterrupt), repr(error))
    check_eq("ctrl_c_serial_writes_one_stop_record: ONE row of kind stopped_by_person", len(found), 1)
    row = found[0] if found else {}
    check("ctrl_c_serial_writes_one_stop_record: who, since, at, ts, empty cut",
          row.get("who") == "person" and row.get("since") == d.run_started and row.get("at") and row.get("ts") and row.get("cut") == [], str(row))
    check("ctrl_c_serial_writes_one_stop_record: none of the keys the outcome readers bind on",
          not any(k in row for k in ("dispatch", "session_id", "total_cost_usd", "exit_code", "is_error", "infra", "call", "dispatch_id")), str(row))
    check_eq("ctrl_c_serial_writes_one_stop_record: no console line of its own", out, "")


def ctrl_c_parallel_road_writes_one_stop_record(tmp):
    d = rig(tmp / "parallel")

    def boundary_step(action):
        """What `run_chains` does on Ctrl-C: two chain threads each launched a call, one of them ended, the interrupt comes out."""
        def chain(dispatch):
            launch(d, dispatch=dispatch, at="2026-11-10T10:00:01+00:00")
        threads = [threading.Thread(target=chain, args=(x,)) for x in ("S5-w1-1", "S5-w2-1")]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        end(d, dispatch="S5-w1-1")
        raise KeyboardInterrupt()
    d.boundary_step = boundary_step
    error, _out = run_catching(d)
    found = stops(d)
    check("ctrl_c_parallel_road_writes_one_stop_record: re-raised", isinstance(error, KeyboardInterrupt), repr(error))
    check_eq("ctrl_c_parallel_road_writes_one_stop_record: ONE row", len(found), 1)
    check_eq("ctrl_c_parallel_road_writes_one_stop_record: `cut` is the call that has no end row",
             found[0]["cut"] if found else None, ["S5-w2-1@2026-11-10T10:00:01+00:00"])


def ctrl_c_in_run_level_handler_writes_one_stop_record(tmp):
    d = rig(tmp / "handler")
    d.boundary = "where"

    def refuse():
        raise SR.Refusal("a script said no")
    d.reconcile_question = refuse
    d.settle_unread_answer = lambda: ""
    d.refusal_lines = lambda refusal: []
    d.question_from_refusal = lambda refusal, boundary: "q"
    d._answer = {}

    def funnel(question):
        launch(d, call="conductor", dispatch="", at="2026-11-10T10:00:02+00:00")      # the paid conductor call began, then Ctrl-C
        raise KeyboardInterrupt()
    d.funnel = funnel
    error, _out = run_catching(d)
    found = stops(d)
    check("ctrl_c_in_run_level_handler_writes_one_stop_record: a Ctrl-C inside `except Refusal` -> funnel is re-raised", isinstance(error, KeyboardInterrupt), repr(error))
    check_eq("ctrl_c_in_run_level_handler_writes_one_stop_record: ONE row, naming the conductor call",
             [r["cut"] for r in found], [["conductor@2026-11-10T10:00:02+00:00"]])


def no_state_dir_writes_nothing(tmp):
    d = rig(tmp / "nostate", with_state_dir=False)

    def interrupt():
        raise KeyboardInterrupt()
    d.reconcile_question = interrupt
    error, out = run_catching(d)
    check("no_state_dir_writes_nothing: re-raised", isinstance(error, KeyboardInterrupt), repr(error))
    check("no_state_dir_writes_nothing: the story's state folder is not created", not d.state_dir.exists(), str(d.state_dir))
    check_eq("no_state_dir_writes_nothing: no console line", out, "")


def before_run_no_record(tmp):
    """Ctrl-C in `__init__` / argparse is outside `run`: nothing calls `person_stop_record` (no call was launched either)."""
    d = rig(tmp / "before")
    check("before_run: a driver that never ran `run` has written no row", rows_of(d) == [], str(rows_of(d)))
    d.progress_line = lambda: (_ for _ in ()).throw(KeyboardInterrupt())    # the header line of `run` itself
    error, _out = run_catching(d)
    # re-pin (Lead, t-502 fix round, option a): the row is about STOP records; the process rows that ARE there are asserted too
    check("before_run: an interrupt in the header line is re-raised and writes no stop record (no call could have been launched)",
          isinstance(error, KeyboardInterrupt) and stops(d) == [], f"{error!r} {rows_of(d)}")
    check_eq("before_run: the process rows that are there: start and end with start_row_written true",
             [(r["event"], r.get("start_row_written", "-")) for r in rows_of(d)], [("start", "-"), ("end", True)])


def failed_write_is_one_note(tmp):
    d = rig(tmp / "failwrite")
    real = SR._append_jsonl

    def interrupt():
        raise KeyboardInterrupt()
    d.reconcile_question = interrupt

    def broken(path, record):
        raise PermissionError("denied")
    SR._append_jsonl = broken
    try:
        error, out = run_catching(d)
    finally:
        SR._append_jsonl = real
    check("failed_write_is_one_note: the KeyboardInterrupt still re-raises", isinstance(error, KeyboardInterrupt), repr(error))
    # re-pin (Lead, t-502 fix round, option b): ONE note for the STOP record; a failed process row prints its own note, asserted too
    lines = [line for line in out.splitlines() if line.strip()]
    stop_lines = [line for line in lines if "stop by the person" in line]
    check("failed_write_is_one_note: ONE `note:` line for the stop record, naming the error",
          len(stop_lines) == 1 and stop_lines[0].startswith("note:") and "PermissionError" in stop_lines[0], out)
    check("failed_write_is_one_note: one note for the start row and one for the end row, each naming its row",
          len(lines) == 3 and sum("start of the process" in line for line in lines) == 1
          and sum("end of the process" in line for line in lines) == 1 and all(line.startswith("note:") for line in lines), out)


def second_ctrl_c_while_writing(tmp):
    real_append = SR._append_jsonl
    # (a) the second interrupt comes BEFORE the row is on disk: the record is absent, nothing raises past `person_stop_record`
    d = rig(tmp / "second-a")

    def first_then_second_before(path, record):
        raise KeyboardInterrupt()
    SR._append_jsonl = first_then_second_before
    try:
        d.run_started = SR._now()
        returned = d.person_stop_record()
    finally:
        SR._append_jsonl = real_append
    check("second_ctrl_c (before the write): person_stop_record returns, raises nothing, the record is absent", returned is None and stops(d) == [], str(stops(d)))

    # (b) the second interrupt comes AFTER the row is written: the record stays, and `run` still ends with the FIRST interrupt only
    d = rig(tmp / "second-b")

    def interrupt():
        raise KeyboardInterrupt("first")
    d.reconcile_question = interrupt

    def write_then_interrupt(path, record):
        real_append(path, record)
        if record.get("kind") == "stopped_by_person":       # re-pin (Lead, t-502 fix round, option a): the stub is keyed on the STOP record
            raise KeyboardInterrupt("second")
    SR._append_jsonl = write_then_interrupt
    try:
        error, _out = run_catching(d)
    finally:
        SR._append_jsonl = real_append
    check("second_ctrl_c (after the write): the record already written is kept", len(stops(d)) == 1, str(stops(d)))
    check("second_ctrl_c (after the write): `run` ends with a KeyboardInterrupt, no other error", isinstance(error, KeyboardInterrupt), repr(error))


def cut_list_follows_journal_run(tmp):
    d = rig(tmp / "cut")
    launch(d, dispatch="S5-a-1", at="T1")
    launch(d, dispatch="S5-b-1", at="T2")
    launch(d, call="conductor", dispatch="", at="T3")
    end(d, dispatch="S5-a-1")
    d.run_started = SR._now()
    d.person_stop_record()
    check_eq("cut: calls launched and not ended, sorted; the ended one is gone", stops(d)[0]["cut"], ["S5-b-1@T2", "conductor@T3"])
    end(d, kind="conductor", dispatch="")
    d.person_stop_record()
    check_eq("cut: a conductor call is ended by its own outcome row (key = kind)", stops(d)[1]["cut"], ["S5-b-1@T2"])
    # a stop row, a note, a trace row are not launches and not ends
    d.journal_run({"kind": "note", "note": "x"})
    d.person_stop_record()
    check_eq("cut: a non-launch, non-outcome row changes nothing", stops(d)[2]["cut"], ["S5-b-1@T2"])
    # a launched row that could not be written is not a cut call (the file has no such row)
    real = SR._append_jsonl
    SR._append_jsonl = lambda path, record: (_ for _ in ()).throw(OSError("full"))
    try:
        try:
            launch(d, dispatch="S5-lost-1", at="T9")
        except OSError:
            pass
    finally:
        SR._append_jsonl = real
    d.person_stop_record()
    check_eq("cut: a launched row whose write failed is not named", stops(d)[3]["cut"], ["S5-b-1@T2"])
    d2 = rig(tmp / "cut-fresh")
    d2.run_started = SR._now()
    d2.person_stop_record()
    check_eq("cut: a process that launched nothing cuts nothing", stops(d2)[0]["cut"], [])


def round_trip_with_the_collector(tmp):
    """The id form of `journal_run` / `person_stop_record` is the twin of `collect_stall._k3_k4`'s: tied by a real driver and a real verdict."""
    d = rig(tmp / "roundtrip")
    old = {"kind": "launched", "call": "role", "role": "r", "dispatch_id": "S5-dead-1", "stage": "S5",
           "started_at": "2020-01-01T00:00:00+00:00", "ts": "2020-01-01T00:00:00+00:00"}
    (d.state_dir / NAME).write_text(json.dumps(old) + "\n", encoding="utf-8")        # a driver that died on its own, long ago
    launch(d, dispatch="S5-x-1", at=SR._now())
    launch(d, call="conductor", dispatch="", at=SR._now())
    d.run_started = "2020-06-01T00:00:00+00:00"
    d.person_stop_record()
    rows = CS._jsonl_rows(d.state_dir / NAME, NAME, [])
    now = 1_900_000_000          # far later than every row: the quiet window is no excuse
    verdict = CS.judge({"closed": True, "unreadable": [], "driver_runs": rows}, None, now, 0)
    where = sorted(s["where"] for s in verdict["signals"])
    check_eq("round trip: the row of the earlier dead driver stays K3, the two calls this process cut are cleared", where,
             ["driver-runs.jsonl launched S5-dead-1"])
    check_eq("round trip: the two cleared rows are named in `ignored` for the stop", sum("stopped by the person" in i["why"] for i in verdict["ignored"]), 2)
    check("round trip: the verdict has no unreadable reason", verdict["unreadable_reasons"] == [], str(verdict["unreadable_reasons"]))
    # the record is not an outcome for any K4 / K3 matching
    check("round trip: the stop row is no outcome row of the collector", not CS._is_outcome(rows[-1]), str(rows[-1]))


# --- 11.2 ----------------------------------------------------------------------------------------------------------------------------
def append_jsonl_repairs_torn_tail(tmp):
    path = tmp / "torn" / "state" / NAME
    path.parent.mkdir(parents=True)
    path.write_bytes(b'{"kind": "a"}\n{"kind": "tor')          # a crash mid-line: no newline at the end
    SR._append_jsonl(path, {"kind": "b", "text": "caf\u00e9 \u4e2d"})
    raw = path.read_bytes()
    lines = raw.split(b"\n")
    check_eq("append_jsonl_repairs_torn_tail: the new row starts on its own line (torn line, then the row, then the end)", len(lines), 4)
    check("append_jsonl_repairs_torn_tail: the new row parses and keeps its non-ASCII text (ensure_ascii False, UTF-8)",
          json.loads(lines[2]) == {"kind": "b", "text": "caf\u00e9 \u4e2d"} and raw.endswith(b"\n"), repr(raw))
    check("append_jsonl_repairs_torn_tail: the line ends in a bare LF, never CRLF", b"\r" not in raw)
    fresh = tmp / "made" / "deep" / "state" / NAME
    SR._append_jsonl(fresh, {"kind": "first"})
    check_eq("append_jsonl: an absent file and folder are created", fresh.read_bytes(), b'{"kind": "first"}\n')
    try:
        SR._append_jsonl(tmp / "torn" / "state" / NAME / "inside", {"kind": "x"})        # a path under a FILE: an OSError, as before
        raised = None
    except OSError as exc:
        raised = exc
    check("append_jsonl: an OSError reaches the caller", raised is not None, "nothing raised")


APPEND_OPEN = re.compile(r"""\.open\(\s*["'][aA][bt+]*["']|\bopen\([^)\n]*(?:,\s*|\bmode\s*=\s*)["'][aA][bt+]*["']""")


def story_run_has_no_private_appender():
    fixture = ('with path.open("a", encoding="utf-8") as handle:\n    handle.write(line)\nwith open(p, "a") as h:\n    pass\n'
               'with open(p, mode="a") as h:\n    pass\nwith open(p, mode=\'a\') as h:\n    pass\nwith open(p, mode="a+") as h:\n    pass\n')
    check_eq("story_run_has_no_private_appender (positive control): the scan finds the positional and the keyword forms in a fixture string",
             len(APPEND_OPEN.findall(fixture)), 5)
    check_eq("story_run_has_no_private_appender (negative control): a read mode is not matched",
             len(APPEND_OPEN.findall('with open(p, mode="r") as h:\n    pass\nwith open(p, "r") as h:\n    pass\n')), 0)
    sources = harness.driver_sources()
    found = [(path.name, text.count("\n", 0, m.start()) + 1, m.group(0)) for path, text in sources for m in APPEND_OPEN.finditer(text)]
    check("story_run_has_no_private_appender: no file of the driver set opens a file for append", found == [], str(found))


def mixed_line_endings_are_read_whole(tmp):
    """F-8: rows written in text mode on Windows ended CRLF; the one appender writes LF. A journal holding both is read whole by the readers."""
    path = tmp / "mixed" / "state" / NAME
    path.parent.mkdir(parents=True)
    first, second = {"kind": "role", "dispatch": "d1", "session_id": "s1", "exit_code": 0, "ts": "2026-11-10T10:00:00+00:00"}, {"kind": "launched", "call": "role", "dispatch_id": "d2", "started_at": "2026-11-10T10:01:00+00:00"}
    path.write_bytes((json.dumps(first) + "\r\n" + json.dumps(second) + "\r\n").encode("utf-8"))
    SR._append_jsonl(path, {"kind": "stopped_by_person", "who": "person", "at": "x", "since": "y", "cut": []})
    raw = path.read_bytes()
    check("mixed endings: the file holds both CRLF and bare LF lines", raw.count(b"\r\n") == 2 and raw.count(b"\n") == 3, repr(raw[-80:]))
    for label, rows in (("story_run._read_jsonl", SR._read_jsonl(path)), ("driver_journal.read_rows", DJ.read_rows(path)),
                        ("collect_stall._jsonl_rows", CS._jsonl_rows(path, NAME, []))):
        check_eq(f"mixed endings: {label} reads all three rows", [r["kind"] for r in rows], ["role", "launched", "stopped_by_person"])
    reasons: list = []
    check_eq("mixed endings: collect_stall names no broken line", (CS._jsonl_rows(path, NAME, reasons), reasons)[1], [])


# --- P1-v N0 (spec docs/tasks/specs/20261113-p1v-run-scoreboard-spec.md §2 W0, §7.11-7.13): the id of the check on every resume road -----
def _rec(check, text="s5_precheck.py: [manifest manifest:TC-1:a] one", script="s5_precheck.py"):
    return DV.Record(text, script=script, check=check)


def refusal_checks_cases():
    a1, a2, d1 = _rec("s5_precheck:manifest"), _rec("s5_precheck:manifest", text="two"), _rec("exit_gate:digest", script="")
    got = SR.Refusal("head", findings=[d1, a1, a2])
    check_eq("(d) the ids are the sorted unique `check_id` of the finding RECORDS, with their counts",
             (got.checks, got.checks_n), (("exit_gate:digest", "s5_precheck:manifest"), {"exit_gate:digest": 1, "s5_precheck:manifest": 2}))
    check_eq("(d) the findings are stringified as before (byte equality with today's `str` list)", got.findings, [str(d1), str(a1), str(a2)])
    check_eq("(d) a plain str finding is the id `unknown`", SR.Refusal("h", findings=["plain"]).checks, ("unknown",))
    check_eq("(d) a record with a script and no check is `<stem>:unlabelled`; a mixed set keeps both ids",
             SR.Refusal("h", findings=[DV.Record("x", script="p/s5_precheck.py"), "plain"]).checks, ("s5_precheck:unlabelled", "unknown"))
    check_eq("(d) no findings and no `checks=`: ONE `unknown`", (SR.Refusal("h").checks, SR.Refusal("h", findings=[]).checks), (("unknown",),) * 2)

    class Skips(SR.Refusal):
        def __init__(self):          # skips super().__init__: the class defaults answer
            Exception.__init__(self, "x")
    check_eq("(d) a subclass that skips `super().__init__` reads empty", (Skips().checks, Skips().checks_n or {}), ((), {}))
    check("(d) two refusals never share one `checks_n` dict", SR.Refusal("h").checks_n is not SR.Refusal("h").checks_n)
    many = SR.Refusal("h", findings=[_rec("s5_precheck:manifest", text=f"f{i}") for i in range(200)])
    check_eq("(h) a refusal of 200 findings of one family: one id, checks_n 200", (many.checks, many.checks_n),
             (("s5_precheck:manifest",), {"s5_precheck:manifest": 200}))
    check_eq("(d) `checks=` wins over the findings' own ids, sorted and unique",
             SR.Refusal("h", findings=[a1], checks=["b:x", "a:y", "b:x"]).checks, ("a:y", "b:x"))
    check_eq("(d) `checks=` as one bare string is one id, not its letters", SR.Refusal("h", checks="a:y").checks, ("a:y",))
    check_eq("(d) an empty `checks=` reads like none: ONE `unknown`, never dropped", SR.Refusal("h", findings=[], checks=[]).checks, ("unknown",))


def _take(out):
    printed = io.StringIO()
    with contextlib.redirect_stdout(printed):
        text, ids = SR.Driver.take_checks_line(out)
    return text, ids, [ln for ln in printed.getvalue().splitlines() if ln.startswith("note:")]


def take_checks_line_cases():
    body = "story_step: r handed d off (2 finding(s))\n- one\n- two\n  Doors: x\n  [repair marker]."
    line = 'checks: ["s5_precheck:manifest", "exit_gate:digest"]'
    check_eq("(e) a valid line is taken out whole, the text is byte-identical, the ids sorted, no note",
             _take(body + "\n" + line), (body, ("exit_gate:digest", "s5_precheck:manifest"), []))
    check_eq("(e) stderr after the line: only the line leaves, the blank line and the stderr stay byte for byte",
             _take(body + "\n" + line + "\n\nwarn: x")[0], body + "\n\nwarn: x")
    two = _take(body + "\nchecks: [\"early:one\"]\n- a later finding\n" + line)
    check_eq("(h) two `checks:` lines: the LAST is the machine line, the earlier one stays in the text",
             (two[0], two[1]), (body + "\nchecks: [\"early:one\"]\n- a later finding", ("exit_gate:digest", "s5_precheck:manifest")))
    unknown = ("unknown",)
    check_eq("(e) no line at all: the text is unchanged, `unknown`, ONE note", _take(body)[0:2], (body, unknown))
    check_eq("(e) ... and exactly one note", len(_take(body)[2]), 1)
    for name, bad in (("broken JSON", "checks: [\"a:b\""), ("a nested object", 'checks: [{"a": 1}]'), ("an object", 'checks: {"a": "b"}'),
                      ("an empty list", "checks: []"), ("an empty id", 'checks: [""]'), ("a number", "checks: [1]"),
                      ("a replacement character (bytes that were not UTF-8)", 'checks: ["a:\ufffd"]'), ("not JSON", "checks: nope")):
        text, ids, notes = _take(body + "\n" + bad)
        check_eq(f"(h) a `checks:` line with {name}: `unknown`, one note, the line still leaves the text",
                 (text, ids, len(notes)), (body, unknown, 1))
    check_eq("(e) `finding_key` of the text is the one it was before the line existed",
             SR.finding_key(_take(body + "\n" + line)[0].splitlines()), SR.finding_key(body.splitlines()))


def gate_refusal_line_cases(tmp):
    """The seam story_step -> driver: `_gate_refusal` PRINTS the machine line last, `Driver.finish`'s reader takes it out (the join row
    belongs here, not in `test_story_step.py`, which holds no check of its own - the five parts are not this node's)."""
    import argparse
    import story_step
    args = argparse.Namespace(task="QA-700", dispatch_id="d-1")
    blocking = [_rec("s5_precheck:manifest"), _rec("s5_precheck:manifest", text="two"), "a plain str", _rec("exit_gate:digest", script="")]
    text = story_step._gate_refusal(args, tmp / "gate", {"stage": "S5", "role": "qa-automator"}, blocking)
    rows = text.split("\n")
    check_eq("(e) `_gate_refusal` prints `checks:` LAST: nothing after it, the repair marker line before it",
             (rows[-1], rows[-2]), ('checks: ["exit_gate:digest", "s5_precheck:manifest", "unknown"]', f"  {REPAIR_MARKER}."))
    check("(e) the head of the text is today's", rows[0].startswith("story_step: qa-automator handed d-1 off while the exit gate of S5 still refuses it (4 finding(s))"))
    back, ids, notes = _take(text)
    check_eq("(e) the driver's reader gives back the text WITHOUT its last line, byte for byte, and the ids", (back, ids, notes),
             ("\n".join(rows[:-1]), ("exit_gate:digest", "s5_precheck:manifest", "unknown"), []))
    check_eq("(e) a refusal of one family prints one id", story_step._gate_refusal(args, tmp / "gate", {"stage": "S5", "role": "r"},
                                                                                  [_rec("s5_precheck:manifest")]).split("\n")[-1], 'checks: ["s5_precheck:manifest"]')


def finish_refusal_cases(tmp):
    def drive(printed, name, code=3):
        d = SR.Driver.__new__(SR.Driver)
        d.task, d.state, d.state_dir = "QA-C", {}, tmp / name / "state"
        d.timed = lambda *a, **k: contextlib.nullcontext()
        d.py = lambda script, *args, **k: (code, printed)
        said = io.StringIO()
        try:
            with contextlib.redirect_stdout(said):
                d.finish("S1-r-1", "digest", complete=False, role="r", stage="S1")
        except SR.Refusal as refusal:
            refusal.said = said.getvalue()
            return refusal
        raise AssertionError("finish did not refuse")
    text = "story_step: r handed S1-r-1 off (1 finding(s))\n- one\n  [repair marker]."
    got = drive(text + '\nchecks: ["s5_precheck:manifest"]', "with")
    check_eq("(e) `finish`: the refusal text is today's, byte for byte, and the ids are the line's",
             (got.text, got.checks), (f"story_step finish S1-r-1 (exit 3):\n{text}".strip(), ("s5_precheck:manifest",)))
    absent = drive(text, "without")
    check_eq("(e) `finish` with no line: the text is today's and the ids are `unknown`", (absent.text, absent.checks),
             (f"story_step finish S1-r-1 (exit 3):\n{text}".strip(), ("unknown",)))
    # F2: only exit 3 has a writer of the line, so any other code keeps its text whole (a quoted `checks:` line stays), reads `unknown`, no note
    for code in (2, 1):
        quoted = drive(text + '\nchecks: ["x:y"]', f"exit{code}", code)
        check_eq(f"(e) `finish` at exit {code} with a valid-looking `checks:` line: the text stays whole, `unknown`, no note",
                 (quoted.text, quoted.checks, "note:" in quoted.said),
                 (f"story_step finish S1-r-1 (exit {code}):\n{text}\nchecks: [\"x:y\"]".strip(), ("unknown",), False))
    bare = drive(text, "exit2-bare", 2)
    check_eq("(e) `finish` at exit 2 with no line at all: no note, `unknown`", (bare.checks, "note:" in bare.said), (("unknown",), False))


def claude_rig(name, rows, tmp):
    d = SR.Driver.__new__(SR.Driver)
    d.claude, d.model, d.host, d.infra_rules, d.state = "x", "m", "claude", [], {"sessions": {}}
    d.task_root, d.state_dir = tmp / name, tmp / name / "state"
    d.claude_cmd, d.host_prompt = (lambda *a, **k: ["x"]), (lambda *a, **k: "")
    d.journal_run, d.package_check, d.mark_host, d.save_state = rows.append, (lambda *a, **k: None), (lambda: None), (lambda: None)
    answer = json.dumps({"session_id": "s2", "result": "ok", "num_turns": 3, "total_cost_usd": 0.1})
    d.launch = lambda cmd, prompt, dispatch="", resume="": subprocess.CompletedProcess(cmd, 0, answer, "")
    return d


def resumed_row_cases(tmp):
    rows: list = []
    d = claude_rig("rows", rows, tmp)

    def row(**kw):
        rows.clear()
        with contextlib.redirect_stdout(io.StringIO()):
            d.run_claude("role", "p", role="r", dispatch="D1", stage="S5", **kw)
        return [r for r in rows if r.get("kind") == "role"][0]
    both = row(resume="s1", resume_reason="why", checks=("b:x", "a:y"), checks_n={"a:y": 3, "b:x": 1})
    check_eq("(f) a resumed row carries `checks` and `checks_n`", (both["checks"], both["checks_n"]), (["a:y", "b:x"], {"a:y": 3, "b:x": 1}))
    part = row(resume="s1", resume_reason="why", checks=("a:y", "b:x"), checks_n={"a:y": 3})
    check_eq("(f) an id whose count the caller does not know has no entry in `checks_n`", (part["checks"], part["checks_n"]), (["a:y", "b:x"], {"a:y": 3}))
    check_eq("(f) `checks=()` is ONE `unknown`", row(resume="s1", resume_reason="why", checks=())["checks"], ["unknown"])
    person = row(resume="s1", resume_reason="the person answered")
    check_eq("(f) R-3: a resume with no `checks` carries neither key", ("checks" in person, "checks_n" in person, person["resumed"]), (False, False, True))
    plain = row(checks=("a:y",))
    check_eq("(f) a call that is not a resume carries no key whatever the caller passed", ("checks" in plain, "resumed" in plain and plain["resumed"]), (False, False))
    d.state["interrupted"] = {"D1": {"worked": True, "session_id": "s0"}}
    cut = row(checks=("a:y",))
    check_eq("(f) R-9: the driver's own resume of a cut call has a `resume_reason` and no `checks`",
             ("resume_reason" in cut, "checks" in cut, "checks_n" in cut), (True, False, False))


def ladder_cases():
    d = SR.Driver.__new__(SR.Driver)
    mech = DV.Record("a.py: [m x] bad (" + REPAIR_MARKER + ")", script="a.py", check="a:m")
    calls, limits = [], []
    d.task_root = Path("task-root")
    d.refusal_sid, d.resume_record, d.note_resume = (lambda dispatch, sid: sid), (lambda dispatch, sid: {}), (lambda *a: None)
    d.exit_ask, d.digest_of, d.keep_resumed_result = (lambda *a, **k: "ask"), (lambda text: "digest"), (lambda *a: None)
    d.run_claude = lambda kind, prompt, **kw: calls.append(kw) or {"result": "x", "session_id": "s2"}
    d.exit_errors, d.form_errors, d.shorten_form = (lambda role, digest, dispatch=None: [mech]), (lambda dispatch: []), (lambda *a, **k: 0)
    d.role_has_bash, d.listed, d.s1_person = (lambda role: True), (lambda *a, **k: ("L", False, "")), (lambda *a, **k: None)
    first = [_rec("s5_precheck:manifest"), _rec("s5_precheck:manifest", text="b"), _rec("handoff_check:header.verdict", text="c")]
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            d.handoff_ladder("r", "S5", "S5-x-1", {"session_id": "s1"}, "dig", first, "")
        raised = None
    except SR.Refusal as refusal:
        raised = refusal
    check_eq("(f) R-1: the first resume carries the ids and counts of the findings it answers",
             (calls[0]["checks"], calls[0]["checks_n"]), (("handoff_check:header.verdict", "s5_precheck:manifest"),
                                                          {"handoff_check:header.verdict": 1, "s5_precheck:manifest": 2}))
    check_eq("(f) R-2: the mechanical third turn carries the RECOMPUTED errors' ids", (calls[1]["checks"], calls[1]["checks_n"]),
             (("a:m",), {"a:m": 1}))
    check_eq("(f) the ladder's own refusal carries the ids of what is still wrong", raised.checks if raised else None, ("a:m",))
    d.resume_record = lambda dispatch, sid: {SR.finding_key(first): "handoff"}
    d.exit_limit = lambda *a, **k: limits.append(k)
    d.handoff, d.saved_result = (lambda *a: "again"), (lambda dispatch: {})
    with contextlib.redirect_stdout(io.StringIO()):
        d.handoff_ladder("r", "S5", "S5-x-1", {"session_id": "s1"}, "dig", first, "")
    check_eq("(f) the seam call of the ladder passes the ids", limits[0]["checks"], ("handoff_check:header.verdict", "s5_precheck:manifest"))


def form_record_cases(tmp):
    d = SR.Driver.__new__(SR.Driver)
    d.task, d.task_root, d.config = "QA-F", tmp / "form", {}
    (d.task_root / "work" / "handoffs").mkdir(parents=True)
    (d.task_root / "work" / "handoffs" / "D1.yaml").write_text("x: 1\n", encoding="utf-8")
    report = {"problems": [{"path": "scope[2].reason", "problem": "too long"}, {"path": "header.verdict", "problem": "bad"},
                           {"path": "scope[10].rows[3].id", "problem": "empty"}, {"path": "", "problem": "none"}]}
    d.py = lambda *a, **k: (1, json.dumps(report))
    _rep, lines = d.form_report("D1")
    check_eq("(a) the handoff form's problems are records: `handoff_check:` + the path with list indices dropped",
             [DV.check_id(x) for x in lines], ["handoff_check:scope[].reason", "handoff_check:header.verdict",
                                               "handoff_check:scope[].rows[].id", "handoff_check:unlabelled"])
    check_eq("(b) ... and their text is today's", str(lines[0]), "handover form D1.yaml - scope[2].reason: too long")
    d.py = lambda *a, **k: (2, "no json here")
    check_eq("(a) no readable answer from handoff_check: `handoff_check:unreadable`", [DV.check_id(x) for x in d.form_report("D1")[1]],
             ["handoff_check:unreadable"])


def resume_with_cases(tmp):
    d = SR.Driver.__new__(SR.Driver)
    seen, limits = [], []
    d.progress_line, d.dispatch_role, d.save_state = (lambda: None), (lambda x: "r"), (lambda: None)
    d.state, d.state_dir = {"pending_words": {}}, tmp / "rw" / "state"
    d.run_claude = lambda kind, prompt, **kw: seen.append(kw) or {"result": "ok", "is_error": False}
    refusal = SR.Refusal("t", findings=[_rec("s5_precheck:manifest"), _rec("s5_precheck:manifest", text="b")], dispatch="D1")
    d.resume_with(refusal, "S5", "D1", "s1", "lead ")
    check_eq("(f) R-4 (and R-5/R-6/R-7 through it): `resume_with` passes the refusal's ids and counts",
             (seen[0]["checks"], seen[0]["checks_n"]), (("s5_precheck:manifest",), {"s5_precheck:manifest": 2}))
    d.run_claude = lambda kind, prompt, **kw: {"result": "", "is_error": True, "stderr": "gone"}
    d.refusal_lines = SR.Driver.refusal_lines
    d.exit_limit = lambda *a, **k: limits.append(k)
    d.resume_with(SR.Refusal("t", checks=["a:y"], dispatch="D1"), "S5", "D1", "s1", "lead ")
    check_eq("(f) a session that is gone: the seam call carries the refusal's ids", limits[0]["checks"], ("a:y",))


def exit_record_cases(tmp):
    class Seam(Exception):
        pass

    def no_move(state):
        raise Seam()
    d = SR.Driver.__new__(SR.Driver)
    d.state, d.save_state, d.revoke_passes_of_dead = {"pending_words": {}}, (lambda: None), (lambda *a, **k: None)
    d.exit_limit_facts, d.no_move = (lambda *a, **k: {"lead": "l", "details": "d", "offer": []}), no_move
    for checks, expected in ((("c:d", "a:b"), ["a:b", "c:d"]), (None, ["unknown"]), ((), ["unknown"])):
        d.state["exit_limit"] = {}
        try:
            d.exit_limit("S5", "r", "D1", ["a line"], sid="", why="handoff", **({} if checks is None else {"checks": checks}))
        except Seam:
            pass
        check_eq(f"(f) R-7: `exit_limit` stores the ids in the exit record ({checks!r})", d.state["exit_limit"]["D1"]["checks"], expected)
    made = []
    d.exit_ask = lambda *a, **k: "ask"
    d.task_root = tmp / "er"
    d.resume_with = lambda refusal, *a, **k: made.append(refusal)
    for rec_checks, expected in ((["a:b"], ("a:b",)), (None, ("unknown",))):
        rec = {"rounds": {"k": {"granted": 1, "spent": 0, "words_file": ""}}}
        if rec_checks is not None:
            rec["checks"] = rec_checks
        with contextlib.redirect_stdout(io.StringIO()):
            d.exit_round("S5", "r", "D1", ["a line"], "s1", rec, "k")
        check_eq(f"(g) `exit_round` reads `rec[\"checks\"]` (absent key: `unknown`, TEMPORAL) - {rec_checks}", made[-1].checks, expected)


def machine_ids_cases():
    class Seam(Exception):
        pass
    limits, runs = [], []
    d = SR.Driver.__new__(SR.Driver)
    refusal = SR.Refusal("t", findings=[_rec("s5_precheck:manifest")], dispatch="S5-x-1")
    d.close_by_doors, d.refusal_dispatch, d.dispatch_role = (lambda *a: ""), (lambda r: "S5-x-1"), (lambda x: "r")
    d.exit_limit = lambda *a, **k: limits.append(k) or (_ for _ in ()).throw(Seam())
    for sid, record in (("", {}), ("s1", {SR.finding_key(d.refusal_lines(refusal)): "refusal", "k2": "stand"})):
        d.refusal_sid, d.resume_record = (lambda *a, _s=sid: _s), (lambda *a, _r=record: _r)
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                d.resume_on_refusal(refusal, "S5", "S5-x-1")
        except Seam:
            pass
    check_eq("(f) R-5/R-6 seams (`exit_limit` at both sites of `resume_on_refusal`) pass `refusal.checks`",
             [k["checks"] for k in limits], [("s5_precheck:manifest",)] * 2)
    d2 = SR.Driver.__new__(SR.Driver)
    d2.boundary, d2.state = "S5:S5-x-1", {"sessions": {"S5-x-1": "s1"}}
    d2.journal_conductor, d2.save_state, d2.controller_state = (lambda **k: None), (lambda: None), (lambda: {})
    d2.run_claude = lambda kind, prompt, **kw: runs.append(kw) or {}
    text = "story_step: refused - S5 structured artifact invalid: x"
    with contextlib.redirect_stdout(io.StringIO()):
        out = d2.handle_refusal(SR.Refusal(text, dispatch="S5-x-1"))
    check_eq("(f) R-8: the structured-artifact resume carries `unknown` (the controller prints no id, F18)",
             (out, runs[0]["checks"] if runs else None), ("retry", ("unknown",)))


# --- P1-v N2 (spec §2 W2, §7, §8 row N2): `resume_kind` on every resumed row ---------------------------------------------------------
KINDS = ("handoff_findings", "handoff_findings_mechanical", "person_answer", "refusal_resume", "stand_answers", "paid_round",
         "structured_refusal", "service_cut", "unclassified")


def kind_rows(tmp, name, **state):
    rows: list = []
    d = claude_rig(name, rows, tmp)
    d.state.update(state)
    notes: list = []

    def row(**kw):
        rows.clear()
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            d.run_claude("role", "p", role="r", dispatch="D1", stage="S5", **kw)
        notes.extend(line for line in out.getvalue().splitlines() if line.startswith("note:"))
        return [r for r in rows if r.get("kind") == "role"][0]
    return d, row, notes


def resume_kind_row_cases(tmp):
    data, why = DJ.run_record()
    check_eq("(c) the real table names the nine tokens of the spec, loaded by the one loader", (data.get("resume_kinds"), why), (list(KINDS), ""))
    d, row, notes = kind_rows(tmp, "kinds")
    for token in KINDS[:7]:
        got = row(resume="s1", resume_reason="why", resume_kind=token)
        check_eq(f"(a) the row of a resume that names `{token}` carries it", got["resume_kind"], token)
    check_eq("(a) a token of the table is no note", notes, [])
    plain = row()
    resumed = row(resume="s1", resume_reason="why", resume_kind="paid_round")
    check_eq("(d) a row that is not a resume has no `resume_kind` KEY (absence, not null)", "resume_kind" in plain, False)
    check_eq("(d) a non-resume call that names a kind still carries no key", "resume_kind" in row(resume_kind="paid_round"), False)
    check_eq("POSITIONAL: a resumed row is the old key set plus exactly `resume_kind`",
             set(resumed) - set(plain), {"resume_reason", "resume_kind"})
    check_eq("POSITIONAL: every old key of a resumed row keeps its value (the same call without the new keyword)",
             {k: v for k, v in resumed.items() if k not in ("resume_kind", "wall_ms", "duration_ms")},
             {k: v for k, v in row(resume="s1", resume_reason="why").items() if k not in ("resume_kind", "wall_ms", "duration_ms")})
    d2, row2, notes2 = kind_rows(tmp, "kinds-cut", interrupted={"D1": {"worked": True, "session_id": "s0"}})
    cut = row2()
    check_eq("(a) R-9: the driver's own resume of a cut call is `service_cut` whatever the call names", (cut["resume_kind"], notes2), ("service_cut", []))
    check_eq("(a) R-9: a caller's own resume over a cut-call record keeps the CALLER's token",
             row2(resume="s1", resume_reason="why", resume_kind="person_answer")["resume_kind"], "person_answer")
    # (b) a token outside the table -> `unclassified` and ONE note; the run goes on
    d3, row3, notes3 = kind_rows(tmp, "kinds-bad")
    for n, token in enumerate(("bogus", "bogus", "Paid_Round", "x" * 5000)):
        got = row3(resume="s1", resume_reason="why", resume_kind=token)
        check_eq(f"(b) token {token[:12]!r} outside the table is `unclassified`", got["resume_kind"], "unclassified")
    check_eq("(b) ONE note per distinct token (bogus twice, Paid_Round, 5000 x): 3 notes, the long one quoted short",
             (len(notes3), max(len(x) for x in notes3) < 300), (3, True))
    # a road that passes no token (an old caller): `unclassified` + the note
    d4, row4, notes4 = kind_rows(tmp, "kinds-none")
    check_eq("an old caller that passes no token: `unclassified` + the note",
             (row4(resume="s1", resume_reason="why")["resume_kind"], len(notes4)), ("unclassified", 1))
    check_eq("a token of a wrong type (None, 7) is `unclassified`, never an exception",
             [row4(resume="s1", resume_reason="why", resume_kind=bad)["resume_kind"] for bad in (None, 7)], ["unclassified"] * 2)


def resume_kind_table_cases(tmp):
    bad = tmp / "kinds-table"
    bad.mkdir()
    cases = {"absent": None, "not JSON": "{not json", "not an object": "[1, 2]", "no key": '{"run_classes": ["dry"]}',
             "key is not a list": '{"resume_kinds": "paid_round"}', "list of numbers": '{"resume_kinds": [1, 2]}',
             "empty list": '{"resume_kinds": []}'}
    real = DJ.RUN_RECORD_PATH
    try:
        for label, text in cases.items():
            path = bad / (label.replace(" ", "-") + ".json")
            if text is not None:
                path.write_text(text, encoding="utf-8")
            DJ.RUN_RECORD_PATH = path
            d, row, notes = kind_rows(tmp, "kt-" + label.replace(" ", "-"))
            got = [row(resume="s1", resume_reason="why", resume_kind="paid_round")["resume_kind"] for _ in range(3)]
            check_eq(f"(c) run-record.json {label}: every resumed row is `unclassified`, ONE note per process, no exception",
                     (got, len(notes)), (["unclassified"] * 3, 1))
            check_eq(f"(c) run-record.json {label}: a non-resumed row still has no key", "resume_kind" in row(), False)
    finally:
        DJ.RUN_RECORD_PATH = real


def resume_kind_road_cases(tmp):
    """One row per road R-1..R-9 at the CALL SITE: the token the site passes (R-9 is in `resume_kind_row_cases`)."""
    d = SR.Driver.__new__(SR.Driver)
    calls = []
    mech = DV.Record("a.py: [m x] bad (" + REPAIR_MARKER + ")", script="a.py", check="a:m")
    d.task_root = Path("task-root")
    d.refusal_sid, d.resume_record, d.note_resume = (lambda dispatch, sid: sid), (lambda dispatch, sid: {}), (lambda *a: None)
    d.exit_ask, d.digest_of, d.keep_resumed_result = (lambda *a, **k: "ask"), (lambda text: "digest"), (lambda *a: None)
    d.run_claude = lambda kind, prompt, **kw: calls.append(kw) or {"result": "x", "session_id": "s2"}
    d.exit_errors, d.form_errors, d.shorten_form = (lambda role, digest, dispatch=None: [mech]), (lambda dispatch: []), (lambda *a, **k: 0)
    d.role_has_bash, d.listed, d.s1_person = (lambda role: True), (lambda *a, **k: ("L", False, "")), (lambda *a, **k: None)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            d.handoff_ladder("r", "S5", "S5-x-1", {"session_id": "s1"}, "dig", [_rec("s5_precheck:manifest")], "")
    except SR.Refusal:
        pass
    check_eq("(a) R-1: the first resume of the handoff ladder", calls[0].get("resume_kind"), "handoff_findings")
    check_eq("(a) R-2: the mechanical third turn", calls[1].get("resume_kind"), "handoff_findings_mechanical")
    # R-3: `resume_role`
    calls.clear()

    class Seam(Exception):
        pass

    def stop_here(*a, **k):
        raise Seam()
    d3 = SR.Driver.__new__(SR.Driver)
    d3.state, d3.state_dir = {"pending_words": {}}, tmp / "r3" / "state"
    d3.session_of, d3.record_running, d3.walk_reopen = (lambda stage, dispatch: "s1"), (lambda *a, **k: None), (lambda dispatch: (None, ""))
    d3.s7_is_triage, d3.progress_line, d3.survey_after = (lambda *a: False), (lambda: None), (lambda *a: None)
    d3.run_claude = lambda kind, prompt, **kw: calls.append(kw) or {"result": "x"}
    d3.handoff, d3.save_state = stop_here, (lambda: None)
    (tmp / "r3" / "state" / "driver-runs").mkdir(parents=True)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            d3.resume_role("S5", "r", "S5-x-1", "yes")
    except Seam:
        pass
    check_eq("(a) R-3: the person's answer", calls[0].get("resume_kind") if calls else None, "person_answer")
    # R-4: `resume_with` hands its `kind` on as it is (none given: the empty name, which the row reads as `unclassified`)
    calls.clear()
    d4 = SR.Driver.__new__(SR.Driver)
    d4.progress_line, d4.dispatch_role, d4.save_state = (lambda: None), (lambda x: "r"), (lambda: None)
    d4.state, d4.state_dir = {"pending_words": {}}, tmp / "r4" / "state"
    d4.run_claude = lambda kind, prompt, **kw: calls.append(kw) or {"result": "ok", "is_error": False}
    refusal = SR.Refusal("t", findings=[_rec("s5_precheck:manifest")], dispatch="D1")
    d4.resume_with(refusal, "S5", "D1", "s1", "lead ", kind="stand_answers")
    d4.resume_with(refusal, "S5", "D1", "s1", "lead ")
    check_eq("(a) R-4: `resume_with` passes its `kind`, and the empty name when a caller gives none",
             [c.get("resume_kind") for c in calls], ["stand_answers", ""])
    # R-7: `exit_round` -> `resume_with(kind=paid_round)`
    made = []
    d7 = SR.Driver.__new__(SR.Driver)
    d7.state, d7.save_state, d7.exit_ask, d7.task_root = {"pending_words": {}}, (lambda: None), (lambda *a, **k: "ask"), tmp / "r7"
    d7.resume_with = lambda refusal, *a, **k: made.append(k)
    rec = {"rounds": {"k": {"granted": 1, "spent": 0, "words_file": ""}}}
    with contextlib.redirect_stdout(io.StringIO()):
        d7.exit_round("S5", "r", "D1", ["a line"], "s1", rec, "k")
    check_eq("(a) R-7: the paid round", made[0].get("kind"), "paid_round")
    # R-5 and R-6: `resume_on_refusal`
    seen = []
    d5 = SR.Driver.__new__(SR.Driver)
    r5 = SR.Refusal("t", findings=[_rec("s5_precheck:manifest")], dispatch="S5-x-1")
    d5.close_by_doors, d5.refusal_dispatch, d5.dispatch_role = (lambda *a: ""), (lambda r: "S5-x-1"), (lambda x: "r")
    d5.refusal_sid, d5.note_resume = (lambda *a: "s1"), (lambda *a: None)
    d5.resume_with = lambda refusal, *a, **k: seen.append(k.get("kind"))
    d5.resume_record = lambda *a: {}
    with contextlib.redirect_stdout(io.StringIO()):
        d5.resume_on_refusal(r5, "S5", "S5-x-1")
    d5.resume_record = lambda *a, _k=SR.finding_key(d5.refusal_lines(r5)): {_k: "refusal"}
    d5.stand_probe = lambda dispatch: (["a"], "out")
    with contextlib.redirect_stdout(io.StringIO()):
        d5.resume_on_refusal(r5, "S5", "S5-x-1")
    check_eq("(a) R-5 then R-6: the first resume of a refusal, the stand that answers now", seen, ["refusal_resume", "stand_answers"])
    # R-8: `handle_refusal`
    runs = []
    d8 = SR.Driver.__new__(SR.Driver)
    d8.boundary, d8.state = "S5:S5-x-1", {"sessions": {"S5-x-1": "s1"}}
    d8.journal_conductor, d8.save_state, d8.controller_state = (lambda **k: None), (lambda: None), (lambda: {})
    d8.run_claude = lambda kind, prompt, **kw: runs.append(kw) or {}
    with contextlib.redirect_stdout(io.StringIO()):
        d8.handle_refusal(SR.Refusal("story_step: refused - S5 structured artifact invalid: x", dispatch="S5-x-1"))
    check_eq("(a) R-8: the structured-artifact resume", runs[0].get("resume_kind") if runs else None, "structured_refusal")


# --- P1-v N1 (spec §2 W1, §7.10, §7.11): the `process` start and end rows, and the run class -------------------------------------------
START_KEYS = {"ts", "kind", "event", "since", "package", "config_sha", "answer_file", "run_class"}
END_KEYS = {"ts", "kind", "event", "since", "process_code", "question_kind", "package", "config_sha", "answer_file", "run_class",
            "start_row_written"}
FORBIDDEN = ("dispatch", "dispatch_id", "session_id", "exit_code", "is_error", "infra", "call", "total_cost_usd", "cost", "cost_usd", "usd")


class _env:
    """STORY_RUN_CLASS set (or removed with None) for the block, restored after."""
    def __init__(self, value):
        self.value, self.had = value, None

    def __enter__(self):
        import os
        self.had = os.environ.get(DJ.RUN_CLASS_ENV)
        if self.value is None:
            os.environ.pop(DJ.RUN_CLASS_ENV, None)
        else:
            os.environ[DJ.RUN_CLASS_ENV] = self.value

    def __exit__(self, *exc):
        import os
        if self.had is None:
            os.environ.pop(DJ.RUN_CLASS_ENV, None)
        else:
            os.environ[DJ.RUN_CLASS_ENV] = self.had


def note_lines(out):
    """The `note:` lines of a run's console output (the run's own pause line is not one)."""
    return [line for line in out.splitlines() if line.startswith("note:")]


def process_rows(d):
    return [r for r in rows_of(d) if r.get("kind") == "process"]


def process_row_cases(tmp):
    # (a) a scenario run writes exactly ONE start row and ONE end row; keys exactly as §2 W1 lists; the rows frame the run's other rows
    d = rig(tmp / "p-normal")
    with _env(None):
        error, out = run_catching(d)
    rows = rows_of(d)
    kinds = [r.get("event") or r["kind"] for r in rows]
    check_eq("(a) a normal run: exactly one start row then one end row, nothing else", (error, kinds), (None, ["start", "end"]))
    start, end_row = rows[0], rows[-1]
    check_eq("(a) start row: keys exactly the listed ones", set(start), START_KEYS)
    check_eq("(a) end row: keys exactly the listed ones", set(end_row), END_KEYS)
    check_eq("(a) both rows name the process start in `since`", (start["since"], end_row["since"]), (d.run_started, d.run_started))
    check("(a) start row values: answer_file false, run_class live, config_sha null (no project), a package fingerprint string",
          start["answer_file"] is False and start["run_class"] == "live" and start["config_sha"] is None
          and isinstance(start["package"], str) and start["package"], str(start))
    check("(a) end row values: process_code is the int `run` returned, no question posted", isinstance(end_row["process_code"], int)
          and not isinstance(end_row["process_code"], bool) and end_row["question_kind"] is None, str(end_row))
    check_eq("(a) no note on a clean start and end", note_lines(out), [])
    # (b) none of the forbidden keys, each asserted absent by name; the end key is process_code, never exit_code
    for key in FORBIDDEN:
        check(f"(b) no `{key}` key in either process row", key not in start and key not in end_row, f"{start} {end_row}")
    check("(b) a process row is no outcome row of the collector", not CS._is_outcome(start) and not CS._is_outcome(end_row), str(rows))
    # (b) collect_stall K3 gives the same verdict on a journal with process rows as without
    old = {"kind": "launched", "call": "role", "role": "r", "dispatch_id": "S5-dead-1", "stage": "S5",
           "started_at": "2020-01-01T00:00:00+00:00", "ts": "2020-01-01T00:00:00+00:00"}
    plain = [old]
    framed = [dict(start, ts="2020-01-01T00:00:00+00:00"), old, dict(end_row, ts="2020-01-01T00:00:01+00:00")]
    verdicts = [CS.judge({"closed": True, "unreadable": [], "driver_runs": got}, None, 1_900_000_000, 0) for got in (plain, framed)]
    check_eq("(b) collect_stall K3: the same signals, ignored rows and unreadable reasons with and without process rows",
             [(v["signals"], v["ignored"], v["unreadable_reasons"]) for v in verdicts][0],
             [(v["signals"], v["ignored"], v["unreadable_reasons"]) for v in verdicts][1])
    check("(b) K3 positive control: the dead launch is a signal in both journals", all(len(v["signals"]) == 1 for v in verdicts), str(verdicts))

    # (c) the fingerprint cannot be read / is absent / is not JSON: package null, ONE note, the run goes on
    import runtime_paths as RP
    real = RP._package_fingerprint

    def raising(exc):
        def fail(plugin):
            raise exc
        return fail
    for n, (label, seam) in enumerate((("an OSError (cannot be read)", raising(OSError("denied"))),
                                       ("a ValueError (not JSON)", raising(ValueError("Expecting value"))),
                                       ("an empty value (absent)", lambda plugin: ""), ("None", lambda plugin: None))):
        d = rig(tmp / f"p-fp-{n}")
        RP._package_fingerprint = seam
        try:
            with _env(None):
                error, out = run_catching(d)
        finally:
            RP._package_fingerprint = real
        notes = note_lines(out)
        check("(c) fingerprint failure, " + label + ": package null, ONE note line, the run goes on and ends",
              error is None and process_rows(d)[0]["package"] is None and len(notes) == 1 and notes[0].startswith("note:")
              and "fingerprint" in notes[0] and [r["event"] for r in process_rows(d)] == ["start", "end"], f"{error!r} {out} {process_rows(d)}")

    # (d) Ctrl-C: the stopped_by_person row first, then the end row with process_code null
    d = rig(tmp / "p-ctrl-c")

    def interrupt():
        raise KeyboardInterrupt()
    d.reconcile_question = interrupt
    with _env(None):
        error, _out = run_catching(d)
    rows = rows_of(d)
    check_eq("(d) Ctrl-C: start, stopped_by_person, end - in this order", [r.get("event") or r["kind"] for r in rows], ["start", "stopped_by_person", "end"])
    check("(d) Ctrl-C: the end row's process_code is null and the interrupt is re-raised", rows[-1]["process_code"] is None
          and isinstance(error, KeyboardInterrupt), f"{error!r} {rows[-1]}")

    # an exception other than Ctrl-C: the end row is written, process_code null, the exception propagates unchanged
    d = rig(tmp / "p-error")
    boom = RuntimeError("a bug nobody planned for")

    def explode(action):
        raise boom
    d.boundary_step = explode
    with _env(None):
        error, _out = run_catching(d)
    check("an exception other than Ctrl-C propagates unchanged (the same object)", error is boom, repr(error))
    check_eq("an exception: start row then end row with process_code null",
             [(r["event"], r.get("process_code", "-")) for r in process_rows(d)], [("start", "-"), ("end", None)])

    # the journal cannot be written at the start row: the OSError of the one writer reaches the caller (as for a first `launched`
    # row today); the end row is still attempted, its failure is ONE note and never replaces the error in flight
    d = rig(tmp / "p-readonly")
    real_append = SR._append_jsonl
    SR._append_jsonl = lambda path, record: (_ for _ in ()).throw(PermissionError("read-only"))
    try:
        with _env(None):
            error, out = run_catching(d)
    finally:
        SR._append_jsonl = real_append
    notes = note_lines(out)
    check("start row unwritable (journal read-only): one note for the start row, one for the end row, the run goes on, no row on disk",
          error is None and len(notes) == 2 and notes[0].startswith("note: the start of the process")
          and notes[1].startswith("note: the end of the process") and rows_of(d) == [], f"{error!r} {out} {rows_of(d)}")
    # only the START row fails: ONE note, the run goes on, the end row is written and says start_row_written false
    d = rig(tmp / "p-start-fails")

    def fail_start(path, record):
        if record.get("event") == "start":
            raise PermissionError("denied")
        return real_append(path, record)
    SR._append_jsonl = fail_start
    try:
        with _env(None):
            error, out = run_catching(d)
    finally:
        SR._append_jsonl = real_append
    notes = note_lines(out)
    check("start row OSError: ONE note naming the start row, the run goes on, the end row says start_row_written false",
          error is None and len(notes) == 1 and notes[0].startswith("note: the start of the process")
          and [(r["event"], r["start_row_written"]) for r in process_rows(d)] == [("end", False)], f"{error!r} {out} {rows_of(d)}")

    # the four FOLDER cases (Lead decision 2: a process row never creates the story's state folder)
    d = rig(tmp / "f-absent-start-present-end", with_state_dir=False)
    d.boundary_step = lambda action: d.state_dir.mkdir(exist_ok=True)          # the story's own writer makes the folder during the run
    with _env(None):
        error, _out = run_catching(d)
    check_eq("folder absent at start, present at end: no start row, one end row with start_row_written false and the start time",
             (error, [(r["event"], r.get("start_row_written", "-"), r["since"]) for r in process_rows(d)]),
             (None, [("end", False, d.run_started)]))
    d = rig(tmp / "f-absent-both", with_state_dir=False)
    with _env(None):
        error, _out = run_catching(d)
    check("folder absent at start AND at end: no rows, and the folder does not exist after `run`",
          error is None and not d.state_dir.exists(), f"{error!r} {d.state_dir.exists()}")
    d = rig(tmp / "f-present-both")
    with _env(None):
        error, _out = run_catching(d)
    check_eq("folder present at both: both rows, start_row_written true",
             (error, [(r["event"], r.get("start_row_written", "-")) for r in process_rows(d)]), (None, [("start", "-"), ("end", True)]))
    d = rig(tmp / "f-removed-before-end")
    import shutil

    real_guarded = d._run_guarded

    def remove_folder():
        code = real_guarded()
        shutil.rmtree(d.state_dir)           # after the run's own work, right before the end row
        return code
    d._run_guarded = remove_folder
    with _env(None):
        error, _out = run_catching(d)
    check("folder present at start, removed before the end: no end row, no exception, the folder is not re-created",
          error is None and not d.state_dir.exists(), f"{error!r} {d.state_dir.exists()}")

    # the end row is the one the mutation removes: a process that is killed has a start row and no end row (what no code can fix)
    # config_sha: sha256 of the bytes; absent -> null; unreadable -> null and ONE note
    import hashlib
    project = tmp / "p-project"
    (project / "qa-factory").mkdir(parents=True)
    config = project / "qa-factory" / "config.json"
    config.write_bytes(b'{"driver": {}}\r\n')
    d = rig(tmp / "p-config")
    d.project = project
    with _env(None):
        run_catching(d)
    check_eq("config_sha is the sha256 of the config bytes", process_rows(d)[0]["config_sha"], hashlib.sha256(b'{"driver": {}}\r\n').hexdigest())
    config.unlink()
    config.mkdir()                 # a folder where the file should be: not absent, not readable
    d = rig(tmp / "p-config-bad")
    d.project = project
    with _env(None):
        _error, out = run_catching(d)
    check("config_sha unreadable: null and ONE note", process_rows(d)[0]["config_sha"] is None
          and len(note_lines(out)) == 1, out)
    d = rig(tmp / "p-config-none")
    d.project = tmp / "p-no-such-project"
    with _env(None):
        _error, out = run_catching(d)
    check("config_sha absent file: null, no note", process_rows(d)[0]["config_sha"] is None and note_lines(out) == [], out)

    # question_kind: the `kind:` line of the posted question file; none posted -> null; a file with no kind line -> null and ONE note
    d = rig(tmp / "p-question")
    (d.state_dir / "driver-question.md").write_text("# Driver question - X\nkind: gate_b\nstage: S9\n", encoding="utf-8")
    with _env(None):
        run_catching(d)
    check_eq("question_kind names the kind of the open question", process_rows(d)[1]["question_kind"], "gate_b")
    d = rig(tmp / "p-question-bad")
    (d.state_dir / "driver-question.md").write_text("no head here\n", encoding="utf-8")
    with _env(None):
        _error, out = run_catching(d)
    check("question file with no kind line: null and ONE note", process_rows(d)[1]["question_kind"] is None
          and len(note_lines(out)) == 1, out)
    d = rig(tmp / "p-answer")
    d.flags = SimpleNamespace(answer="answer.txt")
    d.take_answer = lambda path: None
    with _env(None):
        run_catching(d)
    check_eq("answer_file is true when --answer was given", process_rows(d)[0]["answer_file"], True)
    # TEMPORAL: a journal written before this node has no process rows - the readers read it as before
    check("a journal with no process rows is read whole by the readers that exist (DJ.read_rows, CS.judge)",
          len(DJ.read_rows(d.state_dir / NAME)) == len(rows_of(d)) and len(verdicts[0]["signals"]) == 1, "")


RUN_CLASS_ROWS = (   # (what the variable holds, None = absent, the class, notes)
    (None, "live", 0), ("", "live", 0), ("   ", "live", 0), ("\t\n", "live", 0),
    ("dry", "dry", 0), ("smoke", "smoke", 0),
    ("DRY", "unknown", 1), ("Dry ", "unknown", 1), (" dry ", "unknown", 1), ("live", "unknown", 1), ("test", "unknown", 1),
    ("x" * 10240, "unknown", 1), ("".join(map(chr, (0x434, 0x440, 0x430, 0x439))), "unknown", 1), ("dry\nsmoke", "unknown", 1), ("dry\x00", "unknown", 1),
    ("d" * 60, "unknown", 1), ("d" * 61, "unknown", 1),
)


def run_class_cases(tmp):
    # (e) one variant row per input of §7.10; an input outside the table is `unknown` with ONE note; the others have none
    for value, want, n_notes in RUN_CLASS_ROWS:
        notes: list = []
        got = DJ.run_class({} if value is None else {DJ.RUN_CLASS_ENV: value}, notes)
        label = "absent" if value is None else repr(value[:20]) + (f" (+{len(value) - 20} chars)" if len(value) > 20 else "")
        check_eq(f"(e) run_class {label}: the class and the number of notes", (got, len(notes)), (want, n_notes))
        if n_notes:
            check(f"(e) run_class {label}: the note is one line and quotes at most 60 characters of the value",
                  "\n" not in notes[0] and "\x00" not in notes[0] and notes[0].startswith("note:") and ("x" * 61) not in notes[0]
                  and ("d" * 61) not in notes[0], notes[0][:200])
    # AT and BEYOND the 60-character quote: 60 characters are quoted whole and say nothing of a cut; 61 are cut and say so
    at, beyond = [], []
    DJ.run_class({DJ.RUN_CLASS_ENV: "d" * 60}, at)
    DJ.run_class({DJ.RUN_CLASS_ENV: "d" * 61}, beyond)
    check("(e) AT 60 characters: quoted whole, no cut remark", ("d" * 60) in at[0] and "characters)" not in at[0], at[0])
    check("(e) BEYOND (61): 60 quoted, the cut and the full length named", ("d" * 60) in beyond[0] and ("d" * 61) not in beyond[0]
          and "of 61 characters" in beyond[0], beyond[0])
    # a note is printed when no list is given
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        DJ.run_class({DJ.RUN_CLASS_ENV: "bogus"})
    check("(e) without a notes list the one note is printed", out.getvalue().count("note:") == 1, out.getvalue())
    # the table is data: the real file names dry and smoke; the loader is the one reader of the file
    data, why = DJ.run_record()
    check_eq("(e) run_record: the real table and no note", (data.get("run_classes"), why), (["dry", "smoke"], ""))
    # run-record.json missing / unreadable / without the key / wrong shape -> unknown plus ONE note, for every value, never a crash, never live
    bad = tmp / "run-record-bad"
    bad.mkdir()
    cases = {"absent": None, "not JSON": "{not json", "not an object": "[1, 2]", "no key": '{"schema_version": 1}',
             "key is not a list": '{"run_classes": "dry"}', "list of numbers": '{"run_classes": [1, 2]}'}
    real_path = DJ.RUN_RECORD_PATH
    try:
        for label, text in cases.items():
            path = bad / (label.replace(" ", "-") + ".json")
            if text is not None:
                path.write_text(text, encoding="utf-8")
            DJ.RUN_RECORD_PATH = path
            for value in (None, "dry", "bogus"):
                notes = []
                got = DJ.run_class({} if value is None else {DJ.RUN_CLASS_ENV: value}, notes)
                check_eq(f"(e) run-record.json {label}, variable {value!r}: unknown and ONE note, never live", (got, len(notes)), ("unknown", 1))
    finally:
        DJ.RUN_RECORD_PATH = real_path
    # the process start row carries the class; a dry run and an unknown class end up in the row, and a mistyped one never reads live
    for n, (value, want) in enumerate((("dry", "dry"), ("smoke", "smoke"), ("DRY", "unknown"), (None, "live"))):
        d = rig(tmp / f"p-class-{n}")
        with _env(value), contextlib.redirect_stdout(io.StringIO()):
            run_catching(d)
        check_eq(f"(e) the start row's run_class for STORY_RUN_CLASS={value!r}", process_rows(d)[0]["run_class"], want)


def main():
    tmp = temp_dir("qa-stop-record-")
    try:
        process_row_cases(tmp)
        run_class_cases(tmp)
        refusal_checks_cases()
        take_checks_line_cases()
        gate_refusal_line_cases(tmp)
        finish_refusal_cases(tmp)
        resumed_row_cases(tmp)
        ladder_cases()
        form_record_cases(tmp)
        resume_with_cases(tmp)
        exit_record_cases(tmp)
        machine_ids_cases()
        resume_kind_row_cases(tmp)
        resume_kind_table_cases(tmp)
        resume_kind_road_cases(tmp)
        ctrl_c_serial_writes_one_stop_record(tmp)
        ctrl_c_parallel_road_writes_one_stop_record(tmp)
        ctrl_c_in_run_level_handler_writes_one_stop_record(tmp)
        no_state_dir_writes_nothing(tmp)
        before_run_no_record(tmp)
        failed_write_is_one_note(tmp)
        second_ctrl_c_while_writing(tmp)
        cut_list_follows_journal_run(tmp)
        round_trip_with_the_collector(tmp)
        append_jsonl_repairs_torn_tail(tmp)
        story_run_has_no_private_appender()
        mixed_line_endings_are_read_whole(tmp)
    finally:
        cleanup(tmp)
    finish("test_driver_stop_record")


if __name__ == "__main__":
    main()
