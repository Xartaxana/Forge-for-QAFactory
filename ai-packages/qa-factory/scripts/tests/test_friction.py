#!/usr/bin/env python3
"""Friction with the factory's own code is measured in the S9 retro, from the roles' transcripts (FR-55).

TP1-13797 run 5: friction was 15.5 % of turns, 44.2 % for the code critic, and it was measured
only when someone ran `experiments/measurers/code_friction.py` by hand. This file holds the measurer
(FR-28): one synthetic transcript with a turn of every kind, priced by the package's own valuation;
the journal and the transcript lookup around it; and the retro section that must say `unknown`
wherever the evidence is missing (FR-41) and never a share of 0.0 %.

Every name below that starts with `edge_` answers one line of the B-011 EDGES list.
"""
import datetime
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import (SCRIPTS, check, check_eq, check_in, check_not_in, cleanup, finish,  # noqa: E402
                     temp_dir, temp_project)

sys.path.insert(0, str(SCRIPTS))
import cost_capture  # noqa: E402
import friction as F  # noqa: E402
import retro_numbers as RN  # noqa: E402

TASK = "T-1"
PRICED = "claude-sonnet-5-5"          # in 2 / out 10 USD per Mtok in references/model-rates.json
UNKNOWN = "claude-mystery-9"          # in no catalogue
USAGE = {"input_tokens": 1000, "output_tokens": 100}
TURN_USD = 0.003                      # 1000 * 2 / 1e6 + 100 * 10 / 1e6
TRACEBACK = ('Traceback (most recent call last):\n  File "scripts/probe.py", line 9, in main\n'
             "KeyError: 'source_sha'")


def assistant(mid, model=PRICED, calls=(), usage=USAGE, text="working", ts=None):
    content = [{"type": "text", "text": text}]
    for call_id, name, arg in calls:
        key = "command" if name == "Bash" else "file_path"
        content.append({"type": "tool_use", "id": call_id, "name": name, "input": {key: arg}})
    rec = {"type": "assistant",
           "message": {"id": mid, "model": model, "usage": usage, "content": content}}
    return rec if ts is None else dict(rec, timestamp=ts)


def result(call_id, text, as_list=False, ts=None, error=None):
    body = [{"type": "text", "text": text}] if as_list else text
    block = {"type": "tool_result", "tool_use_id": call_id, "content": body}
    if error is not None:
        block["is_error"] = error
    rec = {"type": "user", "message": {"content": [block]}}
    return rec if ts is None else dict(rec, timestamp=ts)


def write_jsonl(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")


def scout_transcript():
    """Twelve turns: crash, stand, guard (unpriced model), usage, validator, success, a Write of a
    helper, a retry of a script that refused (no result recorded), a plain turn on an unknown model,
    a Bash helper, a numbered listing of a document about refusals, and a repeated line of turn 1."""
    first = assistant("m1", calls=[("c1", "Bash", "python scripts/probe.py")])
    return [
        first,
        result("c1", TRACEBACK, as_list=True),
        first,                                            # the same streamed message, again
        assistant("m2", calls=[("c2", "Bash", "python scripts/run_suite.py")]),
        result("c2", '{"execution_status": "broken_run", "error_head": "ModuleNotFoundError"}\n'
                     + TRACEBACK),
        assistant("m3", model=UNKNOWN, calls=[("c3", "Bash", "python scripts/manifest_put.py")]),
        result("c3", "PRE-TOOL GUARD refused the call: a person's word is not recorded"),
        assistant("m4", calls=[("c4", "Bash", "python scripts/ticket_adapter.py")]),
        result("c4", "usage: ticket_adapter.py [-h] {get,diff} ...\nticket_adapter.py: error: bad"),
        assistant("m5", calls=[("c5", "Bash", "python scripts/check_x.py")]),
        result("c5", "Story artifact is not ready: work/test-plan.json missing required key"),
        assistant("m6", calls=[("c6", "Bash", "python scripts/ok.py")]),
        result("c6", '{"ok": true}'),
        assistant("m7", calls=[("c7", "Write", "work/_patch_manifest.py")]),
        result("c7", "File created successfully at work/_patch_manifest.py"),
        assistant("m8", calls=[("c8", "Bash", "python scripts/probe.py --fix")]),   # no result
        assistant("m9", model=UNKNOWN, calls=[], text="thinking"),
        assistant("m10", calls=[("c10", "Bash", "python work/_try_rows.py")]),
        result("c10", "3 rows"),
        assistant("m11", calls=[("c11", "Read", "references/human-questions.md")]),
        result("c11", "1\tThis document refuses a question with no answer form.\n2\t..."),
        assistant("m12", calls=[("c12", "Write", "work/_patch_manifest.py")]),      # same helper again
        result("c12", "File overwritten"),
    ]


def journal_row(role, sid, dispatch, resumed=False, kind="role", stage="S1"):
    return {"kind": kind, "role": role, "dispatch": dispatch, "stage": stage, "session_id": sid,
            "resumed": resumed, "num_turns": 5, "total_cost_usd": 9.99, "model": PRICED,
            "ts": "2026-09-29T10:00:00"}


def build(root, roles):
    """A temp project with one story: `roles` is [(role, sid, [transcript rows] or None, via)]; `via`
    is "cost" (a cost file names the transcript) or "host" (only the host folder has it)."""
    base = root / "qa-factory"
    troot = base / "artifacts" / TASK
    (troot / "state").mkdir(parents=True)
    home = root / "home"
    slug = cost_capture.project_slug(root)
    rows = []
    for role, sid, transcript, via in roles:
        rows.append(journal_row(role, sid, f"S1-{role}-1"))
        if transcript is None:
            continue
        if via == "cost":
            cost_file_transcript(root, base, sid, transcript)
        else:
            write_jsonl(home / ".claude" / "projects" / slug / f"{sid}.jsonl", transcript)
    return base, troot, home, rows


def cost_file_transcript(root, base, sid, transcript):
    """A transcript under `elsewhere/` that only the session's cost file knows about."""
    target = root / "elsewhere" / f"{sid}.jsonl"
    write_jsonl(target, transcript)
    (base / "state" / "cost").mkdir(parents=True, exist_ok=True)
    (base / "state" / "cost" / f"{sid}.json").write_text(json.dumps(
        {"session_id": sid, "transcript": str(target), "by_task": {TASK: {"cost": 1.0}}}),
        encoding="utf-8")


def write_journal(troot, rows):
    (troot / "state" / "driver-runs.jsonl").write_text(
        "\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")


def priced():
    return F.package_price({})


def classification_of_every_kind_and_its_boundaries():
    m = F.load_markers()
    check_eq("a traceback is a crash", F.classify(TRACEBACK, m), "crash")
    check_eq("a traceback inside a typed broken_run result is the stand", F.classify(
        '{"execution_status": "broken_run"}\n' + TRACEBACK, m), "stand")
    check_eq("a pre-tool guard refusal is the guard", F.classify("PRE-TOOL GUARD: no", m), "guard")
    check_eq("a hook error is the guard", F.classify("Hook error: exit 2", m), "guard")
    check_eq("argparse's own dump is usage", F.classify("usage: probe_by_code.py [-h] --x", m), "usage")
    check_eq("a hand-written usage line with an angle bracket is the form, not friction",
             F.classify("usage: ticket_adapter.py <get|diff> --old <path>", m), None)
    check_eq("a validator refusal in the head", F.classify("The plan is not ready: x", m), "validator")
    check_eq("a numbered file listing is never a validator refusal",
             F.classify("1\tthis reference refuses things", m), None)
    check_eq("a result that is not friction", F.classify('{"ok": true}', m), None)
    check_eq("nothing at all is not friction", F.classify(None, m), None)
    at = "x" * (300 - len("refuses")) + "refuses"           # the phrase ends AT the 300th character
    beyond = "x" * (301 - len("refuses")) + "refuses"        # and one character BEYOND it
    check_eq("a validator phrase ending at character 300 counts", F.classify(at, m), "validator")
    check_eq("one ending at character 301 does not", F.classify(beyond, m), None)
    for rid, text, want in (
            ("single-line-must-be-one-of", "stage must be one of s0, s1, s2", "validator"),
            ("compound-multi-line-keeps-class",
             "plan.yaml is refused:\n  - stage must be one of s0, s1\n  - missing required field: id", "validator"),
            ("prose-one-of-is-not-friction", "the answer came back as one of the usual values", None),
            ("empty-text", "", None)):
        check_eq(f"a refusal spelled `must be one of` [{rid}]", F.classify(text, m), want)
    check("the story's own tests are not ours", F.is_project_test("test_login.py", m)
          and F.is_project_test("login_test.py", m) and not F.is_project_test("probe.py", m))


def the_synthetic_transcript_is_measured():
    root = temp_dir("qa-friction-")
    try:
        path = root / "scout.jsonl"
        write_jsonl(path, scout_transcript())
        f = F.friction(path, priced())
        check_eq("twelve unique turns, the repeated streamed line counted once", f["turns"], 12)
        check_eq("one turn of each kind; three turns wrote or ran a helper (two distinct scripts)",
                 dict(f["tally"]), {"crash": 1, "stand": 1, "guard": 1, "usage": 1, "validator": 1,
                                    "adhoc": 3, "recovery": 1})
        check_eq("nine friction turns of twelve", f["fric_turns"], 9)
        check_eq("the success turn, the plain turn and the listing are not friction (one kind each)",
                 sum(f["tally"].values()), 9)
        check_eq("two turns on a model the catalogue does not hold are unpriced", f["unpriced"], 2)
        check_eq("priced dollars are the ten priced turns", round(f["cost"], 6), round(10 * TURN_USD, 6))
        check_eq("friction dollars leave the unpriced guard turn out: 8 priced friction turns",
                 round(f["fric_cost"], 6), round(8 * TURN_USD, 6))
        check_eq("the Write of work/_patch_manifest.py and the Bash helper are listed once each",
                 sorted((h["path"], h["call"]) for h in f["helpers"]),
                 [("work/_patch_manifest.py", "Write"), ("work/_try_rows.py", "Bash")])
        check("a Read of a document is never listed as a helper",
              all("human-questions" not in h["path"] for h in f["helpers"]))
        check_eq("an unpriced friction turn is still a friction turn: the guard is in the tally",
                 f["tally"]["guard"], 1)
    finally:
        cleanup(root)


def pricing_never_turns_an_unknown_into_zero():
    price = priced()
    check_eq("a known model is priced by the package's own valuation", round(price(PRICED, USAGE), 9),
             TURN_USD)
    check_eq("an unknown model is None, never 0.0", price(UNKNOWN, USAGE), None)
    check_eq("no model at all is None", price(None, USAGE), None)
    check_eq("a synthetic marker with tokens is unpriced", price("<synthetic>", USAGE), None)
    check_eq("a turn that used no tokens costs nothing whatever its model", price("<synthetic>", {
        "input_tokens": 0, "output_tokens": 0}), 0.0)
    partial = F.package_price({"rate_overrides": [{"model_id": "m-half", "rates": {"input": 1}}]})
    check_eq("a rate entry without a key the turn uses is unpriced",
             partial("m-half", {"input_tokens": 10, "output_tokens": 10}), None)
    check_eq("and priced when the turn uses only the keys it has",
             round(partial("m-half", {"input_tokens": 10}), 9), 0.00001)


def edge_no_journal_is_unknown_never_zero_percent():
    root = temp_project()
    try:
        base = root / "qa-factory"
        troot = base / "artifacts" / TASK
        (troot / "state").mkdir(parents=True)
        data = F.story_friction(troot, base, root, {})
        check_eq("no driver journal -> unknown", data["status"], "unknown")
        text = "\n".join(F.section_lines(data, RN.money))
        check_in("the retro says so in the spec's words",
                 "Friction: unknown — this story has no driver journal", text)
        check_not_in("and never prints a share", "%", text)
        empty = troot / "state" / "driver-runs.jsonl"
        empty.write_text(json.dumps(journal_row("", "", "", kind="conductor")) + "\n", encoding="utf-8")
        check_eq("a journal with no role session is unknown too",
                 F.story_friction(troot, base, root, {})["status"], "unknown")
    finally:
        cleanup(root)


def edge_a_resumed_duplicate_session_counts_once_and_two_roads_to_a_transcript():
    root = temp_project()
    try:
        base, troot, home, rows = build(root, [
            ("qa-scout", "sess-scout", scout_transcript(), "cost"),
            ("qa-automator", "sess-host", [assistant("h1", calls=[("k1", "Bash", "python x.py")]),
                                           result("k1", "fine"), assistant("h2")], "host")])
        # the scout's session appears again as a resume, and once more as a repeated row
        rows.append(journal_row("qa-scout", "sess-scout", "S1-qa-scout-1", resumed=True))
        rows.append(journal_row("qa-scout", "sess-scout", "S1-qa-scout-1", resumed=True))
        # A real conductor row carries a REAL session id and role "" (kind is what says it is not a
        # role's); its transcript exists, so a measurer that let it in would count its turns.
        cost_file_transcript(root, base, "sess-conductor", [assistant("k1"), assistant("k2")])
        rows.append(journal_row("", "sess-conductor", "", kind="conductor"))
        # The same kind test must hold on its own, whatever the role field says.
        cost_file_transcript(root, base, "sess-conductor-2", [assistant("q1")])
        rows.append(journal_row("qa-ghost", "sess-conductor-2", "S1-qa-ghost-1", kind="conductor"))
        # One session present on BOTH roads with different content: the cost file's transcript (2
        # turns) must be the one read, not the host folder's (3 turns) - F11-2's order.
        both = [assistant("b1"), assistant("b2")]
        cost_file_transcript(root, base, "sess-both", both)
        write_jsonl(home / ".claude" / "projects" / cost_capture.project_slug(root) / "sess-both.jsonl",
                    both + [assistant("b3")])
        rows.append(journal_row("qa-both", "sess-both", "S1-qa-both-1"))
        write_journal(troot, rows)
        data = F.story_friction(troot, base, root, {}, home=home)
        scout = data["roles"]["qa-scout"]
        check_eq("all sessions reachable -> ok", data["status"], "ok")
        check_eq("a resumed / repeated session id is read once: 12 turns, not 36", scout["turns"], 12)
        check_eq("one session, one dispatch for the scout", (scout["sessions"], scout["dispatches"]),
                 (1, 1))
        check_eq("a conductor's session is not a role's, with role '' or with a role named",
                 sorted(data["roles"]), ["qa-automator", "qa-both", "qa-scout"])
        check_eq("a session on both roads is read through the cost file: 2 turns, not 3",
                 data["roles"]["qa-both"]["turns"], 2)
        check_eq("the cost file was the first road, the host folder the second and both are printed",
                 data["sources"], {"cost file": 2, "host projects folder": 1})
        check_eq("turn share is friction turns over all turns, one decimal", scout["turn_share"], 75.0)
        check_eq("money share is friction dollars over priced dollars: 8 of 10 priced turns",
                 scout["money_share"], 80.0)
        check_eq("the unpriced turns are counted for the role", scout["unpriced"], 2)
        automator = data["roles"]["qa-automator"]
        check_eq("a clean role reads 0 friction turns of 2 - a measured zero, not an unknown",
                 (automator["turns"], automator["fric_turns"], automator["turn_share"]), (2, 0, 0.0))
        check_eq("the journal's total_cost_usd (9.99) is not the money used",
                 scout["priced_cost"], round(10 * TURN_USD, 6))
        check_eq("totals are over the same reachable sessions", data["total"]["turns"], 16)
        lines = "\n".join(F.section_lines(data, RN.money))
        check_in("the section names the method and its record", "not from the CLI's", lines)
        check_in("the section prints the unpriced count", "Unpriced turns: 2", lines)
        check_in("the helper scripts are named with their role",
                 "qa-scout — work/_patch_manifest.py", lines)
        check_in("and the sources", "via cost file", lines)
    finally:
        cleanup(root)


def edge_a_missing_transcript_is_partial_or_unknown_and_never_a_zero():
    root = temp_project()
    try:
        base, troot, home, rows = build(root, [
            ("qa-scout", "sess-scout", scout_transcript(), "cost"),
            ("qa-code-critic", "sess-gone", None, "cost")])
        write_journal(troot, rows)
        data = F.story_friction(troot, base, root, {}, home=home)
        check_eq("one of two sessions unreachable -> partial", data["status"], "partial")
        check_eq("n of m is counted", (data["sessions_unreachable"], data["sessions"]), (1, 2))
        check_eq("the role whose transcript is missing has no reachable session",
                 data["roles"]["qa-code-critic"]["reachable"], 0)
        check_eq("shares are over the reachable session only", data["total"]["turns"], 12)
        text = "\n".join(F.section_lines(data, RN.money))
        check_in("the unreachable count is printed", "1 of 2 sessions unreachable", text)
        check_in("the role's row says unknown", "| qa-code-critic | unknown |", text)
        check("no zero share is printed for the unreachable role (a bare 0.0%, not the tail of 80.0%)",
              not re.search(r"(?<![0-9.])0\.0%", text), text)
        only = [r for r in rows if r["role"] == "qa-code-critic"]
        write_journal(troot, only)
        data = F.story_friction(troot, base, root, {}, home=home)
        check_eq("every session unreachable -> unknown", data["status"], "unknown")
        text = "\n".join(F.section_lines(data, RN.money))
        check_in("the text says unknown", "unknown", text)
        check_not_in("and never 0.0%", "0.0%", text)
        check_eq("locate names what it tried", F.locate("sess-gone", base, root, home=home)[0], None)
        check_in("its source says where it looked",
                 "absent", F.locate("sess-gone", base, root, home=home)[1])
    finally:
        cleanup(root)


def edge_no_priced_turn_leaves_the_money_share_unknown_and_the_turn_share_printed():
    root = temp_project()
    try:
        transcript = [assistant("u1", model=UNKNOWN, calls=[("a", "Bash", "python scripts/x.py")]),
                      result("a", TRACEBACK), assistant("u2", model=UNKNOWN)]
        base, troot, home, rows = build(root, [("qa-scout", "sess-u", transcript, "cost")])
        write_journal(troot, rows)
        data = F.story_friction(troot, base, root, {}, home=home)
        scout = data["roles"]["qa-scout"]
        check_eq("an unpriced friction turn counts in turns", (scout["turns"], scout["fric_turns"]), (2, 1))
        check_eq("turn share is printed", scout["turn_share"], 50.0)
        check_eq("money share is unknown", scout["money_share"], None)
        check_eq("and no dollar figure exists", (scout["priced_cost"], scout["fric_cost"]), (None, None))
        text = "\n".join(F.section_lines(data, RN.money))
        check_in("the row prints the turn share", "1 (50.0%)", text)
        check_in("and unknown for the dollar share", "not priced (unknown)", text)
        check_in("and the unpriced count", "Unpriced turns: 2", text)
    finally:
        cleanup(root)


def the_markers_are_data_and_their_absence_is_reported_with_what_is_expected():
    m = json.loads((SCRIPTS.parent / "references" / "friction-markers.json").read_text(encoding="utf-8"))
    check("the marker file holds every key the spec names", all(k in m for k in (
        "traceback", "stand_markers", "guard_markers", "usage_regex", "validator_head_phrases",
        "validator_head_chars", "listing_prefix", "adhoc_path_regexes", "project_test_regex")))
    check("the file is English (FR-30)", all(ord(ch) < 128 for ch in json.dumps(m, ensure_ascii=False)))
    root = temp_dir("qa-friction-markers-")
    try:
        try:
            F.load_markers(root / "absent.json")
            raised = ""
        except ValueError as exc:
            raised = str(exc)
        check_in("an absent marker file says what was expected (FR-1)", "expected the package file", raised)
        # a marker changed in data changes the classification: nothing is decided in code (FR-13)
        custom = root / "m.json"
        custom.write_text(json.dumps(dict(m, guard_markers=["custom refusal"])), encoding="utf-8")
        check_eq("a spelling added to the data file is recognised", F.classify(
            "Custom Refusal here", F.load_markers(custom)), "guard")
        check_eq("and the shipped table does not know it", F.classify("Custom Refusal here"), None)
    finally:
        cleanup(root)


def edge_the_retro_carries_the_section_and_friction_never_fails_it():
    root = temp_project()
    try:
        base, troot, home, rows = build(root, [("qa-scout", "sess-scout", scout_transcript(), "cost")])
        write_journal(troot, rows)
        data = RN.numbers(TASK, base, troot)
        check_eq("numbers carries the measurement", data["friction"]["status"], "ok")
        check_eq("of the transcript the cost file named", data["friction"]["roles"]["qa-scout"]["turns"], 12)
        text = RN.render(data)
        check_in("the render carries the section", "Friction with the factory's own code", text)
        check_in("with the role's row", "| qa-scout | 12 | 9 (75.0%) |", text)
        check_in("and the helper line", "Helper scripts a role wrote for itself: qa-scout — "
                 "work/_patch_manifest.py; qa-scout — work/_try_rows.py.", text)
        json.dumps(data)                                    # the facts file must stay serialisable
        check_eq("a story with no journal prints unknown in the retro", "Friction: unknown — this "
                 "story has no driver journal" in RN.render(dict(data, friction={
                     "status": "unknown", "reason": "this story has no driver journal"})), True)
        check_in("numbers computed before the section existed still render it, as unknown",
                 "Friction: unknown", RN.render({k: v for k, v in data.items() if k != "friction"}))

        real = F.locate

        def failing(*args, **kwargs):
            raise RuntimeError("the transcript folder cannot be listed")
        F.locate = failing
        try:
            broken = RN.numbers(TASK, base, troot)
        finally:
            F.locate = real
        check_eq("a failing locate does not raise out of numbers: unknown", broken["friction"]["status"],
                 "unknown")
        check_in("with its reason", "RuntimeError: the transcript folder cannot be listed",
                 broken["friction"]["reason"])
        check_eq("the other numbers are intact", broken["story"], data["story"])
        check_in("and the retro says why", "Friction: unknown — RuntimeError", RN.render(broken))

        real_markers = F.MARKERS_PATH
        F.MARKERS_PATH = root / "no-such-markers.json"
        try:
            gone = RN.numbers(TASK, base, troot)
        finally:
            F.MARKERS_PATH = real_markers
        check_eq("an absent marker file is unknown with what is expected too", gone["friction"]["status"],
                 "unknown")
        check_in("naming the file", "friction-markers.json", gone["friction"]["reason"])
    finally:
        cleanup(root)


def edge_the_real_reason_a_transcript_is_unreachable_is_printed():
    root = temp_project()
    try:
        base, troot, home, rows = build(root, [
            ("qa-scout", "sess-scout", scout_transcript(), "cost"),
            ("qa-code-critic", "sess-del", None, "cost")])
        cost_file_transcript(root, base, "sess-del", [assistant("d1")])
        (root / "elsewhere" / "sess-del.jsonl").unlink()          # the cost file now names a deleted file
        write_journal(troot, rows)
        text = "\n".join(F.section_lines(F.story_friction(troot, base, root, {}, home=home), RN.money))
        check_in("partial line names the file the cost file points at", "sess-del.jsonl", text)
        check_in("and says it is absent", "is absent", text)
        check_in("and which role's session it was", "qa-code-critic: session sess-del", text)
        write_journal(troot, [r for r in rows if r["role"] == "qa-code-critic"])
        text = "\n".join(F.section_lines(F.story_friction(troot, base, root, {}, home=home), RN.money))
        check_in("the unknown line carries the same reason", "Friction: unknown", text)
        check_in("naming the missing file", "elsewhere", text)
        check_not_in("and not the old fixed sentence", "no cost file names one", text)
    finally:
        cleanup(root)


def edge_the_configs_cost_block_prices_a_model_only_an_override_knows():
    root = temp_project()
    try:
        transcript = [assistant("o1", model=UNKNOWN), assistant("o2", model=UNKNOWN)]
        base, troot, home, rows = build(root, [("qa-scout", "sess-o", transcript, "cost")])
        write_journal(troot, rows)
        check_eq("without an override the model is unpriced",
                 RN.numbers(TASK, base, troot)["friction"]["unpriced"], 2)
        cfg = json.loads((base / "config.json").read_text(encoding="utf-8"))
        cfg["cost"] = {"rate_overrides": [{"model_id": UNKNOWN, "rates": {"input": 2, "output": 10}}]}
        (base / "config.json").write_text(json.dumps(cfg), encoding="utf-8")
        got = RN.numbers(TASK, base, troot)["friction"]
        check_eq("cost.rate_overrides from config.json prices it: 0 unpriced", got["unpriced"], 0)
        check_eq("at the override's rate: 2 turns of $0.003", got["roles"]["qa-scout"]["priced_cost"],
                 round(2 * TURN_USD, 6))
    finally:
        cleanup(root)


def edge_the_rendered_retro_of_a_story_with_no_reachable_transcript_says_unknown():
    root = temp_project()
    try:
        base, troot, home, rows = build(root, [("qa-scout", "sess-gone-9", None, "cost")])
        write_journal(troot, rows)
        text = RN.render(RN.numbers(TASK, base, troot))
        section = text.split("**Friction with the factory's own code**")[1].split("| Stage |")[0]
        check_in("the section is there and says unknown", "Friction: unknown —", section)
        check_not_in("and prints no 0.0%", "0.0%", section)
    finally:
        cleanup(root)


def stamp(sec):
    """An ISO timestamp the way the host writes it, `sec` seconds after a fixed start (a str, or the raw
    value a test hands over to make it unreadable)."""
    if isinstance(sec, str):
        return sec
    base = datetime.datetime(2026, 11, 12, 10, 0, 0, tzinfo=datetime.timezone.utc)
    return (base + datetime.timedelta(seconds=sec)).strftime("%Y-%m-%dT%H:%M:%S.000Z")


def timed_transcript():
    """A role's session with times: bookkeeping calls (manifest_put, a two-call message with
    handoff_check, calls cut off or with an unreadable stamp), refused calls of three kinds (a guard
    refusal, a crash, a failure no spelling names), and calls that are neither (a refusal-shaped result
    with no `is_error`, a Read and a cat of a bookkeeping script, an unlisted script)."""
    prompt = {"type": "user", "timestamp": stamp(0), "message": {"content": "start"}}

    def line(mid, sec, call_id, arg, name="Bash"):
        return assistant(mid, calls=[(call_id, name, arg)], ts=stamp(sec))

    return [
        prompt,
        line("t1", 4, "k1", "python scripts/manifest_put.py --fragment x"),
        result("k1", '{"ok": true}', ts=stamp(7)),
        line("t2", 9, "k2", "python scripts/run_suite.py"),
        result("k2", "PRE-TOOL GUARD refused the call", ts=stamp(12), error=True),
        line("t3", 14, "k3", "python scripts/handoff_check.py --task T"),      # one message, two calls
        line("t3", 15, "k4", "python scripts/probe.py"),
        result("k3", "ok", ts=stamp(16)),
        result("k4", TRACEBACK, ts=stamp(20), error=True),
        line("t4", 22, "k5", "python scripts/ticket.py"),
        result("k5", "ticket call failed: network down", ts=stamp(25), error=True),
        line("t5", 27, "k6", "python scripts/check_x.py"),
        result("k6", "Story artifact is not ready: plan missing required key", ts=stamp(29)),
        line("t6", 30, "k7", "scripts/manifest_put.py", name="Read"),
        result("k7", "1\tdef main(): ...", ts=stamp(31)),
        line("t7", 33, "k8", "cat scripts/other_tool.py"),
        result("k8", "text", ts=stamp(34)),
        line("t8", 40, "k9", "python scripts/manifest_from_tests.py"),         # the session was cut: no result
        line("t9", 45, "k10", "python scripts/manifest_put.py"),
        result("k10", "merged", ts=None),                                       # a result line with no stamp
        line("t10", 50, "k11", "python scripts/manifest_put.py"),
        result("k11", "merged", ts="not-a-time"),                               # an unreadable stamp
    ]


def row_of(tally, *keys):
    return {k: (round(tally[k], 3) if isinstance(tally[k], float) else tally[k]) for k in keys}


T_KEYS = ("calls", "exec_s", "exec_unmeasured", "turn_s", "turn_unmeasured")


def call_time_rows():
    """One table: every row is (what, got, want); a red line names the row."""
    root = temp_dir("qa-friction-calls-")
    try:
        path = root / "role.jsonl"
        write_jsonl(path, timed_transcript())
        spans = F.call_spans(path)
        book, refused = spans["bookkeeping"], spans["refused"]
        by_id = {c["id"]: c for c in spans["calls"]}
        shipped_doc = json.loads((SCRIPTS.parent / "references" / "friction-markers.json").read_text(
            encoding="utf-8"))
        no_list = {}
        for why, value in (("absent", None), ("a string", "manifest_put.py"), ("empty", []),
                           ("rows without a script", [{"why": "x"}, "manifest_put.py", 3])):
            doc = dict(shipped_doc)
            doc.pop("bookkeeping_scripts")
            if why != "absent":
                doc["bookkeeping_scripts"] = value
            marker_file = root / (why.replace(" ", "-") + ".json")
            marker_file.write_text(json.dumps(doc), encoding="utf-8")
            no_list[why] = F.load_markers(marker_file)
        back = root / "back.jsonl"          # a result stamped BEFORE its call
        write_jsonl(back, [{"type": "user", "timestamp": stamp(0), "message": {"content": "go"}},
                           assistant("b1", calls=[("b", "Bash", "python scripts/manifest_put.py")], ts=stamp(10)),
                           result("b", "ok", ts=stamp(5))])
        backwards = F.call_spans(back)["calls"][0]
        rows = [
            # (a) bookkeeping count and both seconds rows
            ("bookkeeping: 5 calls, the cut-off, unstamped and unreadable ones counted and unmeasured",
             row_of(book, *T_KEYS, "state"),
             dict(calls=5, exec_s=5.0, exec_unmeasured=3, turn_s=11.0, turn_unmeasured=3, state="measured")),
            ("execution seconds: tool_use line to tool_result line (manifest_put 3 s, handoff_check 2 s)",
             (by_id["k1"]["exec_s"], by_id["k3"]["exec_s"]), (3.0, 2.0)),
            ("turn-attributed seconds: previous line to the result (manifest_put 0 -> 7 s)",
             by_id["k1"]["turn_s"], 7.0),
            ("a two-call message: its window 12 -> 20 s split evenly, 4 s to each; execution from own lines",
             (by_id["k3"]["turn_s"], by_id["k4"]["turn_s"], by_id["k4"]["exec_s"]), (4.0, 4.0, 5.0)),
            ("the cut-off call is counted, its seconds unknown, not 0",
             (by_id["k9"]["bookkeeping"], by_id["k9"]["exec_s"], by_id["k9"]["turn_s"]), (True, None, None)),
            ("a result line with no stamp: unknown, not 0",
             (by_id["k10"]["exec_s"], by_id["k10"]["turn_s"]), (None, None)),
            ("an unreadable stamp: unknown, not 0", (by_id["k11"]["exec_s"], by_id["k11"]["turn_s"]), (None, None)),
            ("a result stamped before its call: execution unknown (not negative, not 0); the turn window "
             "runs from the previous line, so it still reads",
             (backwards["exec_s"], backwards["turn_s"]), (None, 5.0)),
            ("a Read of a bookkeeping script, a cat of an unlisted one, an unlisted script: not bookkeeping",
             [by_id[k]["bookkeeping"] for k in ("k7", "k8", "k2", "k5", "k6")], [False] * 5),
            # (b) refused / failed by is_error, split by classify
            ("refused: the 3 calls with is_error, seconds from their own lines",
             row_of(refused, *T_KEYS), dict(calls=3, exec_s=11.0, exec_unmeasured=0, turn_s=14.0,
                                            turn_unmeasured=0)),
            ("refused split by kind: guard, crash, and `failed, cause not recorded` for what no spelling names",
             {k: row_of(v, "calls", "exec_s", "turn_s") for k, v in sorted(refused["by_kind"].items())},
             {"guard": dict(calls=1, exec_s=3.0, turn_s=5.0), "crash": dict(calls=1, exec_s=5.0, turn_s=4.0),
              "failed, cause not recorded": dict(calls=1, exec_s=3.0, turn_s=5.0)}),
            ("is_error absent is not an error, whatever the result text says",
             (by_id["k6"]["is_error"], by_id["k6"]["kind"]), (False, None)),
            # (c) edges: no list, in every shape it can be missing
            *[(f"bookkeeping list {why}: `unknown: no bookkeeping list`, no zero calls; refused unchanged",
               (lambda s: (s["bookkeeping"]["state"], s["bookkeeping"]["reason"], s["refused"]["calls"]))(
                   F.call_spans(path, markers)),
               ("unknown", "unknown: no bookkeeping list", 3)) for why, markers in no_list.items()],
            ("seconds are printed exact, as `at least`, or as unknown",
             (F.seconds_text(5.0, 0), F.seconds_text(11.0, 3, 8), F.seconds_text(0.0, 2, 2)),
             ("5.0 s", "at least 11.0 s (3 calls unmeasured)", "unknown (2 calls unmeasured)")),
        ]
        for what, got, want in rows:
            check_eq(what, got, want)
        shipped = F.load_markers()
        check_eq("the shipped list is the Lead's six scripts",
                 sorted(shipped["bookkeeping_scripts"]),
                 ["handoff_check.py", "handoff_init.py", "manifest_from_tests.py", "manifest_put.py",
                  "manifest_view.py", "s5_precheck.py"])
        check_eq("the shipped fragment pattern list is the Lead's one pattern", shipped["bookkeeping_fragment_patterns"],
                 ["*.values.yaml"])
        real_path = F.MARKERS_PATH
        F.MARKERS_PATH = root / "no-such-markers.json"
        try:
            lost = F.call_spans(path)
        finally:
            F.MARKERS_PATH = real_path
        check_eq("an unreadable markers file: bookkeeping unknown, refused counted, kind not named",
                 (lost["bookkeeping"]["state"], lost["refused"]["calls"], sorted(lost["refused"]["by_kind"])),
                 ("unknown", 3, ["failed, cause not recorded"]))
    finally:
        cleanup(root)


OLD_SCRIPT = re.compile(r"([a-z_]+\.py)")             # the shape before round 2: no digit in a name

# (what, command, scripts it invokes in command order, the listed script the call is attributed to)
INVOCATION_SHAPES = (
    ("invoked with flags", "python -B scripts/manifest_put.py --fragment x",
     ["manifest_put.py"], "manifest_put.py"),
    ("invoked by an absolute Windows path with a digit in the name",
     r'python3 "C:\pkg dir\scripts\s5_precheck.py" --task T', ["s5_precheck.py"], "s5_precheck.py"),
    ("invoked by an absolute interpreter and script path", "/usr/bin/python3.12 -u /abs/scripts/handoff_check.py",
     ["handoff_check.py"], "handoff_check.py"),
    ("invoked through the py launcher with its flag", "py -3 scripts/manifest_view.py",
     ["manifest_view.py"], "manifest_view.py"),
    ("invoked as the command itself", "scripts/handoff_init.py --task T", ["handoff_init.py"],
     "handoff_init.py"),
    ("interpreter flag with its own argument", "python -W ignore scripts/manifest_put.py",
     ["manifest_put.py"], "manifest_put.py"),
    ("after cd, in a subshell, with an env prefix", "( cd d && FOO=1 python -B x/handoff_check.py )",
     ["handoff_check.py"], "handoff_check.py"),
    ("with a pipe and a redirect after it", "python scripts/s5_precheck.py --task T 2>&1 | tail -5",
     ["s5_precheck.py"], "s5_precheck.py"),
    ("named only as an argument of another program (not counted)",
     "python scripts/other.py manifest_put.py", ["other.py"], None),
    ("named as the argument of grep (not counted)", "grep manifest_put.py scripts/x.txt", [], None),
    ("named as the argument of cat (not counted)", "cat scripts/s5_precheck.py", [], None),
    ("named as the argument of an editor (not counted)", "vim scripts/manifest_put.py", [], None),
    ("named inside quoted text (not counted)", 'echo "python scripts/manifest_put.py"', [], None),
    ("named in code after -c (not counted)", 'python -c "import manifest_put.py"', [], None),
    ("two invoked scripts joined by && are ONE call, attributed to the first in the command",
     "python scripts/manifest_put.py && python scripts/handoff_check.py",
     ["manifest_put.py", "handoff_check.py"], "manifest_put.py"),
    ("an unlisted script first and a listed one second: the call is the listed one's",
     "python scripts/other.py && python scripts/s5_precheck.py", ["other.py", "s5_precheck.py"],
     "s5_precheck.py"),
    ("an empty command", "", [], None),
    # round 3 (B1): the one shell reader (hooklib), the four real shapes the critic cited, reduced
    ("a heredoc BODY naming scripts is text, not a command (not counted)",
     "cat > notes.md <<'E'\nrun manifest_put.py later\npython s5_precheck.py was refused\nE", [], None),
    ("an apostrophe inside a heredoc body does not hide the real call after it",
     "cat > n.md <<'E'\nthe guard didn't run\nE\npython scripts/manifest_put.py --fragment f.json",
     ["manifest_put.py"], "manifest_put.py"),
    ("a real call with its flags after a heredoc",
     "cat > fix.md <<'E'\nnotes: it's done\nE\npython /abs/scripts/handoff_check.py --file x.yaml --fix",
     ["handoff_check.py"], "handoff_check.py"),
    ("a quoted absolute path with spaces after a heredoc",
     'cat > t.md <<EOF\ndon\'t\nEOF\npython "C:\\my dir\\scripts\\manifest_put.py" --task LOCAL-1 --fragment f.json',
     ["manifest_put.py"], "manifest_put.py"),
    ("a command that is only a heredoc", "python - <<'E'\nimport manifest_put.py\nE", [], None),
    ("nested quotes in an argument of another command, then a real call",
     "echo \"a 'b' c\" && python scripts/handoff_check.py", ["handoff_check.py"], "handoff_check.py"),
    ("a very long command (20000 words) ending in a real call",
     "echo " + "w " * 20000 + "&& python scripts/manifest_put.py", ["manifest_put.py"], "manifest_put.py"),
    ("a program behind a wrapper is NOT read (a named limit in CALL_TIME_METHOD: the count is a floor)",
     "timeout 120 python scripts/manifest_put.py", [], None),
)


def round2_rows():
    """The Lead's six answers to round 1, one table per answer; a red line names the row."""
    root = temp_dir("qa-friction-round2-")
    try:
        book_doc = json.loads((SCRIPTS.parent / "references" / "friction-markers.json").read_text(encoding="utf-8"))
        # answer 1: the name shape allows digits; older readers only gain the correctly named script
        no_digit = [x["input"].get("command") or x["input"].get("file_path") or ""
                    for rec in scout_transcript() if rec["type"] == "assistant"
                    for x in rec["message"]["content"] if x.get("type") == "tool_use"] + [
            "python -B scripts/manifest_put.py --fragment x", "cat scripts/other_tool.py", "py -3 a_b.py c.py", ""]
        recover = [assistant("r1", calls=[("a", "Bash", "python scripts/s5_precheck.py")]),
                   result("a", "PRE-TOOL GUARD refused the call"),
                   assistant("r2", calls=[("b", "Bash", "python scripts/s6_precheck.py")]), result("b", "ok"),
                   assistant("r3", calls=[("c", "Bash", "python scripts/s5_precheck.py --fix")])]
        rpath = root / "recover.jsonl"
        write_jsonl(rpath, recover)
        after = dict(F.friction(rpath, priced())["tally"])
        F.SCRIPT = OLD_SCRIPT
        try:
            before = dict(F.friction(rpath, priced())["tally"])
            scout = root / "scout.jsonl"
            write_jsonl(scout, scout_transcript())
            before_scout = F.friction(scout, priced())
        finally:
            F.SCRIPT = re.compile(r"([a-z0-9_]+\.py)")
        after_scout = F.friction(scout, priced())
        for what, got, want in (
                ("a digit is part of a script name now: s5_precheck.py is one name",
                 F.SCRIPT.findall("python scripts/s5_precheck.py --x"), ["s5_precheck.py"]),
                ("it was read as _precheck.py before", OLD_SCRIPT.findall("python scripts/s5_precheck.py"),
                 ["_precheck.py"]),
                ("commands with no digit in a name read the same under both shapes (the fixture's own calls)",
                 [F.SCRIPT.findall(a.lower()) for a in no_digit], [OLD_SCRIPT.findall(a.lower()) for a in no_digit]),
                ("friction() on the existing fixture: output unchanged",
                 (after_scout["tally"], after_scout["fric_turns"], after_scout["helpers"]),
                 (before_scout["tally"], before_scout["fric_turns"], before_scout["helpers"])),
                ("friction(), a refused digit-named script retried later: before (name read as _precheck.py, a "
                 "different digit-named script closed the repair) -> after (its own name is tracked: recovery)",
                 (before, after), ({"guard": 1}, {"guard": 1, "recovery": 1}))):
            check_eq(what, got, want)
        # answer 2: invocation, one row per shape (the commands and the call-level attribution)
        lines = [{"type": "user", "timestamp": stamp(0), "message": {"content": "go"}}]
        for i, (_, cmd, _, _) in enumerate(INVOCATION_SHAPES):
            lines += [assistant(f"s{i}", calls=[(f"s{i}", "Bash", cmd)], ts=stamp(10 * i + 1)),
                      result(f"s{i}", "ok", ts=stamp(10 * i + 3))]
        spath = root / "shapes.jsonl"
        write_jsonl(spath, lines)
        by_id = {c["id"]: c for c in F.call_spans(spath)["calls"]}
        for i, (what, cmd, invoked, attributed) in enumerate(INVOCATION_SHAPES):
            check_eq(f"invocation [{what}]: scripts invoked", F.invoked_scripts(cmd), invoked)
            check_eq(f"invocation [{what}]: bookkeeping attribution", by_id[f"s{i}"]["script"], attributed)
        check_eq("a joined command is counted once, not twice", F.call_spans(spath)["bookkeeping"]["calls"],
                 sum(1 for s in INVOCATION_SHAPES if s[3]))
        # answer 3: fragment writes, their own row; the pattern list in every shape it can be missing
        frag = [{"type": "user", "timestamp": stamp(0), "message": {"content": "go"}}]
        for i, (name, target) in enumerate((
                ("Write", "work/handoffs/S5-qa-automator.values.yaml"), ("Edit", r"C:\w\HANDOFFS\S5.Values.YAML"),
                ("Write", "work/handoffs/S5.yaml"), ("Write", "work/notes.values.yaml.bak"), ("Read", "a.values.yaml"),
                ("Bash", "cat a.values.yaml"), ("Bash", "python scripts/manifest_put.py"))):
            frag += [assistant(f"f{i}", calls=[(f"f{i}", name, target)], ts=stamp(10 * i + 1)),
                     result(f"f{i}", "ok", ts=stamp(10 * i + 4))]
        fpath = root / "frag.jsonl"
        write_jsonl(fpath, frag)
        got = F.call_spans(fpath)
        no_frag = {}
        for why, value in (("absent", None), ("a string", "*.values.yaml"), ("empty", []), ("no usable pattern", [3, ""])):
            doc = dict(book_doc)
            doc.pop("bookkeeping_fragment_patterns")
            if why != "absent":
                doc["bookkeeping_fragment_patterns"] = value
            marker_file = root / ("frag-" + why.replace(" ", "-") + ".json")
            marker_file.write_text(json.dumps(doc), encoding="utf-8")
            no_frag[why] = F.call_spans(fpath, F.load_markers(marker_file))
        for what, got_, want in (
                ("fragment writes: a Write and an Edit matching the pattern, case-insensitive, 2 calls, 3 s each",
                 row_of(got["fragment_writes"], "calls", "exec_s", "state"), dict(calls=2, exec_s=6.0, state="measured")),
                ("a Write of another file, a name that merely contains the pattern, a Read, a cat: not fragment writes",
                 [c["fragment_write"] for c in got["calls"]], [True, True, False, False, False, False, False]),
                ("the script row holds only the script run, never a fragment write",
                 (got["bookkeeping"]["calls"], got["bookkeeping"]["state"]), (1, "measured")),
                *[(f"fragment pattern list {why}: `unknown: no fragment pattern list`, the script row unaffected",
                   (s["fragment_writes"]["state"], s["fragment_writes"]["reason"], s["fragment_writes"]["calls"],
                    s["bookkeeping"]["state"], s["bookkeeping"]["calls"]),
                   ("unknown", "unknown: no fragment pattern list", 0, "measured", 1))
                  for why, s in no_frag.items()]):
            check_eq(what, got_, want)
        # round 3 (B2): refused calls are the host's `is_error` flag and nothing else; no second row, no total
        tpath = root / "role.jsonl"
        write_jsonl(tpath, timed_transcript())
        spans = F.call_spans(tpath)
        flagged = spans["refused"]
        by_t = {c["id"]: c for c in spans["calls"]}
        looks = root / "looks.jsonl"             # calls the host did not flag whose results LOOK like refusals
        write_jsonl(looks, [
            {"type": "user", "timestamp": stamp(0), "message": {"content": "go"}},
            assistant("h1", calls=[("h1", "Bash", "python scripts/manifest_put.py --help")], ts=stamp(2)),
            result("h1", "usage: manifest_put.py [-h] --task TASK [--fragment F]\n" + "  --x  flag\n" * 20, ts=stamp(4)),
            assistant("h2", calls=[("h2", "Bash", "tail -5 tests/api/cart/cart_add.spec.ts")], ts=stamp(6)),
            result("h2", "it('invalid input is refused with one error class', () => {})", ts=stamp(7)),
            assistant("h3", calls=[("h3", "Bash", "python scripts/manifest_put.py")], ts=stamp(9)),
            result("h3", "refused: no task", ts=stamp(10), error=True)])
        got_looks = F.call_spans(looks)
        for what, got_, want in (
                ("refused: the 3 host-flagged calls of the fixture, and the key set has no second row or total",
                 (row_of(flagged, "calls"), sorted(spans)),
                 (dict(calls=3), ["bookkeeping", "calls", "fragment_writes", "method", "refused"])),
                ("a flagged guard refusal is refused; the refusal-shaped result k6 with no flag is not",
                 (by_t["k2"]["is_error"], by_t["k2"]["kind"], by_t["k6"]["is_error"], by_t["k6"]["kind"],
                  sorted(by_t["k6"])),
                 (True, "guard", False, None,
                  ["bookkeeping", "exec_s", "fragment_write", "id", "is_error", "kind", "name", "script", "turn_s"])),
                ("a voluntary --help call (argparse usage text) and a role's own text with `is refused` are NOT "
                 "refusals; only the flagged call is",
                 (got_looks["refused"]["calls"], [c["is_error"] for c in got_looks["calls"]],
                  [c["kind"] for c in got_looks["calls"]]),
                 (1, [False, False, True], [None, None, "failed, cause not recorded"]))):
            check_eq(what, got_, want)
        # answer 5: an empty bookkeeping list stays unknown (the rows of call_time_rows cover the other shapes)
        doc = dict(book_doc, bookkeeping_scripts=[])
        empty_file = root / "empty-book.json"
        empty_file.write_text(json.dumps(doc), encoding="utf-8")
        empty = F.call_spans(tpath, F.load_markers(empty_file))["bookkeeping"]
        check_eq("an empty bookkeeping list is not a statement that there is no bookkeeping",
                 (empty["state"], empty["reason"], empty["calls"]), ("unknown", "unknown: no bookkeeping list", 0))
        # answer 6: a message of 3 calls, 1 cut: its window split evenly among ALL three
        cut = [{"type": "user", "timestamp": stamp(0), "message": {"content": "go"}},
               assistant("w1", calls=[("w1", "Bash", "python scripts/manifest_put.py")], ts=stamp(2)),
               assistant("w1", calls=[("w2", "Bash", "python scripts/handoff_check.py")], ts=stamp(3)),
               assistant("w1", calls=[("w3", "Bash", "python scripts/s5_precheck.py")], ts=stamp(4)),
               result("w1", "ok", ts=stamp(6)), result("w2", "ok", ts=stamp(12))]       # w3: the session was cut
        cpath = root / "cut.jsonl"
        write_jsonl(cpath, cut)
        got = F.call_spans(cpath)
        cut_book = got["bookkeeping"]
        for what, got_, want in (
                ("3 calls, 1 cut: window 0 -> 12 s split among all 3, 4 s each, the cut call unknown",
                 [c["turn_s"] for c in got["calls"]], [4.0, 4.0, None]),
                ("the sum is `at least`: 8 s over 2 of 3 calls",
                 (row_of(cut_book, *T_KEYS), F.seconds_text(cut_book["turn_s"], cut_book["turn_unmeasured"],
                                                           cut_book["calls"])),
                 (dict(calls=3, exec_s=13.0, exec_unmeasured=1, turn_s=8.0, turn_unmeasured=1),
                  "at least 8.0 s (1 calls unmeasured)"))):
            check_eq(what, got_, want)
    finally:
        cleanup(root)


def story_call_time_rows():
    """The story-level reader: per role, partial and unreachable sessions, and stub roles."""
    root = temp_project()
    try:
        base, troot, home, rows = build(root, [
            ("qa-automator", "sess-a", timed_transcript(), "cost"),
            ("qa-scout", "sess-gone", None, "cost")])
        write_journal(troot, rows)
        data = F.story_calls(troot, base, root, {}, home=home)
        auto = data["roles"]["qa-automator"]
        stub_root = temp_project()
        try:
            sbase, stroot, shome, srows = build(stub_root, [("qa-automator", "stub-1", None, "cost"),
                                                           ("qa-scout", "stub-2", None, "cost")])
            write_journal(stroot, srows)
            stub = F.story_calls(stroot, sbase, stub_root, {}, home=shome)
            write_journal(stroot, srows[:1] + [journal_row("qa-critic", "sess-lost", "S1-qa-critic-1")])
            mixed = F.story_calls(stroot, sbase, stub_root, {}, home=shome)
        finally:
            cleanup(stub_root)
        empty = temp_project()
        try:
            ebase = empty / "qa-factory"
            (ebase / "artifacts" / TASK / "state").mkdir(parents=True)
            nothing = F.story_calls(ebase / "artifacts" / TASK, ebase, empty, {})
        finally:
            cleanup(empty)
        for what, got, want in (
                ("one session of two unreachable: partial", (data["status"], data["sessions_unreachable"]),
                 ("partial", 1)),
                ("the role's calls and bookkeeping rows are its reachable session's",
                 (auto["calls"], auto["bookkeeping"]["calls"], auto["bookkeeping"]["state"]), (11, 5, "measured")),
                ("the role's seconds carry their unmeasured count",
                 row_of(auto["bookkeeping"], "exec_s", "exec_unmeasured", "turn_s", "turn_unmeasured"),
                 dict(exec_s=5.0, exec_unmeasured=3, turn_s=11.0, turn_unmeasured=3)),
                ("refused rows are summed with their kinds", (auto["refused"]["calls"],
                                                              sorted(auto["refused"]["by_kind"])),
                 (3, ["crash", "failed, cause not recorded", "guard"])),
                ("the role whose transcript is missing has no reachable session, no figure",
                 (data["roles"]["qa-scout"]["reachable"], data["roles"]["qa-scout"]["calls"],
                  data["roles"]["qa-scout"]["bookkeeping"]["state"]), (0, None, "unknown")),
                ("B3: that role's refused row is unknown with its reason (not 0), as the other rows are; the "
                 "reachable role's refused row is measured",
                 ([data["roles"]["qa-scout"][k]["state"] for k in ("bookkeeping", "fragment_writes", "refused")],
                  data["roles"]["qa-scout"]["refused"]["reason"], auto["refused"]["state"]),
                 (["unknown"] * 3, "unknown: no session could be read", "measured")),
                ("the total is over the reachable session", (data["total"]["calls"],
                                                             data["total"]["bookkeeping"]["calls"]), (11, 5)),
                ("the role has refused, bookkeeping and fragment rows only (no named-by-marker row, no total)",
                 (sorted(k for k in auto if isinstance(auto[k], dict)), auto["fragment_writes"]["state"]),
                 (["bookkeeping", "fragment_writes", "refused"], "measured")),
                ("the total of a story with one reachable role: its calls and a measured refused row",
                 (data["total"]["calls"], data["total"]["refused"]["state"]), (11, "measured")),
                ("stub roles with no transcript: n/a, never 0", (stub["status"], stub["reason"][:15]),
                 ("n/a", "n/a: stub roles")),
                ("a lost real session next to a stub one is unknown, not n/a", mixed["status"], "unknown"),
                ("a story with no driver journal is unknown", nothing["status"], "unknown")):
            check_eq(what, got, want)
        json.dumps(data)
    finally:
        cleanup(root)


def unreadable_role_sessions_are_unknown_and_a_true_zero_is_zero():
    """B3: absent, unreadable, torn and empty transcripts give `unknown` (calls None) for every row; a readable
    transcript with no bookkeeping and no refused call gives a measured 0."""
    root = temp_project()
    try:
        zero = [{"type": "user", "timestamp": stamp(0), "message": {"content": "go"}},
                assistant("z1", calls=[("z1", "Read", "notes.md")], ts=stamp(2)), result("z1", "text", ts=stamp(3))]
        base, troot, home, rows = build(root, [
            ("qa-absent", "sess-absent", None, "host"), ("qa-empty", "sess-empty", None, "host"),
            ("qa-torn", "sess-torn", None, "host"), ("qa-oserror", "sess-oserror", zero, "host"),
            ("qa-zero", "sess-zero", zero, "host")])
        write_journal(troot, rows)
        folder = home / ".claude" / "projects" / cost_capture.project_slug(root)
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "sess-empty.jsonl").write_text("", encoding="utf-8")
        (folder / "sess-torn.jsonl").write_text('{"type": "assis\n{broken\nnot json at all\n', encoding="utf-8")
        real = F.call_spans

        def flaky(path, markers=None):
            if "sess-oserror" in str(path):
                raise PermissionError("transcript cannot be opened")
            return real(path, markers)

        F.call_spans = flaky
        try:
            data = F.story_calls(troot, base, root, {}, home=home)
        finally:
            F.call_spans = real
        got = {role: (r["reachable"], r["calls"], [r[k]["state"] for k in ("bookkeeping", "fragment_writes", "refused")],
                      r["refused"]["reason"]) for role, r in data["roles"].items()}
        unknown = (0, None, ["unknown"] * 3, "unknown: no session could be read")
        for what, got_, want in (
                ("absent transcript: unknown, calls None", got["qa-absent"], unknown),
                ("empty transcript file: unknown, calls None", got["qa-empty"], unknown),
                ("torn transcript (no line is a record): unknown, calls None", got["qa-torn"], unknown),
                ("unreadable transcript (the open fails): unknown, calls None", got["qa-oserror"], unknown),
                ("a readable transcript with no such call: a measured 0, not unknown",
                 got["qa-zero"], (1, 1, ["measured"] * 3, "")),
                ("the story is partial and the total counts only the readable session",
                 (data["status"], data["sessions_unreachable"], data["total"]["calls"],
                  data["total"]["refused"]["state"]), ("partial", 4, 1, "measured"))):
            check_eq(what, got_, want)
        check_in("an empty or torn transcript says why it is unreachable", "no readable record",
                 data["roles"]["qa-torn"]["unreachable_because"])
        # one transcript straight through call_spans
        for name, text in (("empty", ""), ("torn", "{broken\n")):
            (folder / f"direct-{name}.jsonl").write_text(text, encoding="utf-8")
            spans = F.call_spans(folder / f"direct-{name}.jsonl")
            check_eq(f"call_spans of an {name} file: every row unknown, no call",
                     ([spans[k]["state"] for k in ("bookkeeping", "fragment_writes", "refused")], spans["calls"]),
                     (["unknown"] * 3, []))
    finally:
        cleanup(root)


def old_keys_of_turns_of_are_unchanged():
    """experiments/measurers/code_friction.py imports SCRIPT, classify, is_project_test, turns_of and
    friction from here and reads the rows' `cost`, `calls`, `mid` and each call's `id`, `name`, `arg`
    and the results by id as lists of text: all of that still returns what it returned."""
    root = temp_dir("qa-friction-compat-")
    try:
        path = root / "scout.jsonl"
        write_jsonl(path, scout_transcript())
        rows, results = F.turns_of(path, lambda model, usage: 0.5)
        first = rows[0]
        for what, got, want in (
                ("the names code_friction imports exist", [callable(getattr(F, n)) for n in (
                    "classify", "is_project_test", "turns_of", "friction")] + [hasattr(F.SCRIPT, "findall")],
                 [True] * 5),
                ("the old keys of a row are all still there", {"cost", "calls", "mid"} <= set(first), True),
                ("the old keys of a call are all still there", {"id", "name", "arg"} <= set(first["calls"][0]),
                 True),
                ("a row's old values", (first["mid"], first["cost"], first["calls"][0]["id"],
                                        first["calls"][0]["name"], first["calls"][0]["arg"]),
                 ("m1", 0.5, "c1", "Bash", "python scripts/probe.py")),
                ("results by id are still a list of text", results["c1"], [TRACEBACK]),
                ("twelve unique turns as before", len(rows), 12),
                ("a transcript with no timestamps reads as before and its calls have no seconds",
                 (first["calls"][0]["ts"], first["calls"][0]["has_result"]), (None, True))):
            check_eq(what, got, want)
        check_eq("friction() keeps its old keys", sorted(F.friction(path, priced())), sorted([
            "turns", "cost", "fric_turns", "fric_cost", "tally", "money", "unpriced", "helpers"]))
    finally:
        cleanup(root)


def main():
    call_time_rows()
    round2_rows()
    story_call_time_rows()
    unreadable_role_sessions_are_unknown_and_a_true_zero_is_zero()
    old_keys_of_turns_of_are_unchanged()
    classification_of_every_kind_and_its_boundaries()
    the_synthetic_transcript_is_measured()
    pricing_never_turns_an_unknown_into_zero()
    edge_no_journal_is_unknown_never_zero_percent()
    edge_a_resumed_duplicate_session_counts_once_and_two_roads_to_a_transcript()
    edge_a_missing_transcript_is_partial_or_unknown_and_never_a_zero()
    edge_no_priced_turn_leaves_the_money_share_unknown_and_the_turn_share_printed()
    the_markers_are_data_and_their_absence_is_reported_with_what_is_expected()
    edge_the_retro_carries_the_section_and_friction_never_fails_it()
    edge_the_real_reason_a_transcript_is_unreachable_is_printed()
    edge_the_configs_cost_block_prices_a_model_only_an_override_knows()
    edge_the_rendered_retro_of_a_story_with_no_reachable_transcript_says_unknown()
    finish("test_friction")


if __name__ == "__main__":
    main()
