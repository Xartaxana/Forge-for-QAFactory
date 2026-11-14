#!/usr/bin/env python3
"""question_register.py: the one reader of a story's question status, the answers file, the strict
answer parser and the CLI (t-113 piece A1, B-216 / B-181).

The class of defect held here: an id found by substring or alias, a status guessed from a mention,
and a parser that errs toward APPLYING an answer the person did not write. On cmp1 the person
answered Q1..Q5 by name at gate A and gate B still called all five unanswered; the same words, read
by a lenient grammar, would have applied readings ("Q1: a question for later" reads Q1=a).
One named check per edge of the piece, then the adversarial battery, then the real cmp1 words.
"""
import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from harness import (check, check_eq, check_in, cleanup, finish,  # noqa: E402
                     temp_dir, temp_project, use_project)

sys.path.insert(0, str(harness.SCRIPTS))
import question_register as QR  # noqa: E402

# Every non-ASCII character is BUILT with chr(): the package holds no Cyrillic (FR-30) and a literal
# BOM or no-break space in a source file is invisible.
CYR_A = chr(0x430)        # Cyrillic small a: looks like the Latin one
FULL_COLON = chr(0xFF1A)  # full-width colon
FULL_A = chr(0xFF41)      # full-width Latin a
NBSP = chr(0xA0)
BULLET = chr(0x2022)      # a bullet character
BOM = chr(0xFEFF)
ACUTE = chr(0x301)        # a combining accent
E_ACUTE = chr(0xE9)
CYR_TS = chr(0x422) + chr(0x421)                    # look-alikes of the Latin T and C
HELLO = "".join(chr(c) for c in (0x43F, 0x440, 0x438, 0x432, 0x435, 0x442))            # a Russian word
THEN = "".join(chr(c) for c in (0x43F, 0x43E, 0x442, 0x43E, 0x43C))                    # another
ALPHABET = "".join(chr(c) for c in (0x43A, 0x438, 0x440, 0x438, 0x43B, 0x43B, 0x438, 0x446, 0x430))  # a third
CASES = [f"TP1-13797_TC_{n:03d}" for n in range(1, 13)]

# The person's gate A answer of the cmp1 run, verbatim (experiments/measurers/answers/cmp1-gate-a.md).
CMP1_GATE_A = """Gate A: **approved.** The plan (14 rows) and the 12 pinned cases go to S5 as they stand - no edits, no re-dispatch. Size XXL, budget 47 against a cap of 28: **test it as one story, do not decompose.** The critic's `approve_with_fixes` verdict stands; its two exact replacements (TC_005 When step 1, TC_008 Given bullet 1) are applied by code - `critic_rollcall.py --apply-fixes` - and the cases re-pinned, no designer dispatch.

The items under "After your approval", by name:

1. **vcs-1, dirty working tree (26 uncommitted changes on `HEAD`, 97a6de8331f9)** - go on, on this branch as it is. Nothing is committed or stashed on my behalf.
2. **case_environment-1, TS-14's declared gap (no observable)** - accept the gap: the row stays in the plan as unverifiable, nothing is invented for it.
3. **s5_toolchain-1, the tests cannot be collected** - install what is missing, on my word, then re-collect and go on. The worktree already has `poetry install` done; if the collection still dies, it is the interpreter the check uses (system python instead of the poetry environment) - run the collection through poetry and record what you changed. S5 does not write code nothing can run, and "not executed" for a dependency of our own making is not accepted.
4. **s5_reporter-1, stand gap RP-api** - **apply**: the card's own diagnosis says the runner passes `--junitxml` itself, so the missing report has the same cause as item 3 (collection dies in conftest). After item 3, re-probe the card; only if a run still leaves no readable report change `qa-factory/config.json:profiles[api].commands.one_test`, and record what you changed.
5. **s5_environment-1, credentials and accounts** - accept the gap. `AWS_ACCESS_KEY`, `AWS_SECRET_KEY`, `AWS_PROFILE` are not set and the `auditor`, `default_scoped_user`, `project_scoped_user` accounts are not provisioned. The cases that need them are reported as not executed, by name, never as passed; nothing writes a value anywhere.

The open questions, by name (the register's Q-R ids are the same questions):

- **Q1 / Q-R14 / R-9 (event-type mismatch: 400 or 200 ACK)** - reading **(a)**: the 200 ACK with no dispatch is intended - AC-9 means valid deliveries keep working, and a 200 keeps GitHub from disabling the webhook. R-14 is asserted as 200/no dispatch; TS-5 keeps its disposition with the register's own reading of R-9; the old 400 is not tested and no bug is filed for it.
- **Q2 / Q-R15 (payload over 25,000,000 bytes)** - reading **(a)**: the size guard fails open by design; R-15 is asserted as dispatched with the bypass metric recorded. If S5 finds the metric is not emitted, that is a local bug proposal, not a test oracle change.
- **Q3 / Q-R7 (UI field for the JSON path filter)** - this is **missed scope, not a deferral**: the ticket's AC-7 stands, and nothing ships the UI half (`settingsUIConfig.ts` has no `github_json_path_filter`). AC-7 is unmet as shipped and is reported as a discrepancy against the acceptance criteria: a **local bug proposal under `qa-factory/bugs`, nothing to Jira or any tracker**. No UI or e2e row this cycle - there is nothing to observe yet; TC_011 stays manual-human and is reported as not executed with this reason.
- **Q4 / Q-R21 (`$.pull_request[?(@.draft==false)]` never matches)** - reading **(a)**: a documented limitation; only syntax errors are invalid. R-21 is asserted as "saves and never matches"; TC_009 keeps its disposition.
- **Q5 / Q-R22 (filter without a webhook secret)** - reading **(a)**: test with and without a secret; the unfiltered no-secret case is recorded as a gap in the report, not asserted either way, and not a bug.

The warnings:

- **ticket_adapter: unknown** - run the read-only probe; it is the factory's own receipt.
- **config_schema: not_configured** - leave it. This is an experiment copy; no migration decision tonight. Carry it as a warning to the end.

**Sources found after the S1 review** - TP1-13289 stays left out, the reason given is right.

Standing for the rest of the run, unchanged: bugs stay **local proposal files under `qa-factory/bugs`** and are not submitted anywhere; a merge request, if the pipeline reaches one, is **Draft only** on a branch with the suffix -c; the remote branches `TP1-13797_github-webhook-json-path-filter` and `-b` are ignored entirely - not a source, not existing coverage, not a precedent.
"""


def q(qid, n=2, text=None):
    return {"id": qid, "question": text or f"question {qid}?", "severity": "major",
            "readings": [{"reading": f"reading {i}", "from": "code", "if_chosen": "x"} for i in range(n)]}


def write_story(root: Path, questions=None, answers=None, pipeline=None, readiness_raw=None):
    """A task root with the files the register reads. `answers` are RAW lines (a test may break one)."""
    (root / "work").mkdir(parents=True, exist_ok=True)
    if readiness_raw is not None:
        (root / "work" / "requirements-readiness.json").write_text(readiness_raw, encoding="utf-8")
    elif questions is not None:
        (root / "work" / "requirements-readiness.json").write_text(
            json.dumps({"verdict": "blocked", "open_questions": questions}), encoding="utf-8")
    if answers is not None:
        (root / "work" / "question-answers.jsonl").write_bytes("\n".join(answers).encode("utf-8"))
    if pipeline is not None:
        (root / "pipeline.json").write_text(json.dumps(pipeline), encoding="utf-8")
    return root


HASH = "a" * 64  # a well-formed row hash that is no row's hash today


def rec(qid, status="answered", **extra):
    base = {"id": qid, "status": status, "words": f"words for {qid}", "by": "person", "where": "gate A",
            "at": "2026-09-30T10:00:00+00:00", "row_hash": HASH}
    base.update(extra)
    return json.dumps(base)


def case_rec(case, decision="manual", **extra):
    base = {"kind": "case", "case": case, "decision": decision, "words": f"{case}: {decision}", "where": "gate A",
            "by": "person", "at": "2026-09-30T10:00:00+00:00"}
    base.update(extra)
    return json.dumps(base)


def row_hash_of(root, qid):
    return next(x["row_hash"] for x in QR.load(root)["questions"] if x["id"] == qid)


def put(root, qid, status, words, hash_from="row", reading="", where="gate A", by="person"):
    """QR.record() with the hash the card would pass back: the row's own hash today, unless given."""
    shown = row_hash_of(root, qid) if hash_from == "row" else hash_from
    return QR.record(root, qid, status, words, where, by, shown, reading=reading)


def status_of(view, qid):
    return next(x["status"] for x in view["questions"] if x["id"] == qid)


def row_of(view, qid):
    return next(x for x in view["questions"] if x["id"] == qid)


def safe(fn, *args):
    try:
        return fn(*args), None
    except Exception as exc:  # the register must never raise on a story's own data
        return None, exc


def snapshot(root: Path) -> dict:
    return {str(p.relative_to(root)): p.read_bytes() for p in sorted(root.rglob("*")) if p.is_file()}


def parse(words, questions=("Q1", "Q2"), cases=CASES, readings=2):
    return QR.parse_choices(words, [q(x, readings) for x in questions], list(cases))


# ------------------------------------------------------------------------------------------------
# E1 - ONE id, exact
# ------------------------------------------------------------------------------------------------

def test_e1_exact_id(tmp):
    root = write_story(tmp / "e1", [q("Q1"), q("Q10", 3), q("Q3")],
                       answers=[rec("Q10"), rec("q1"), rec("Q-1"), rec("Q-R14"), rec(" Q3 ")])
    view = QR.load(root)
    check_eq("E1 an answer for Q10 does not answer Q1 (no prefix or substring match)",
             (status_of(view, "Q1"), status_of(view, "Q10")), ("open", "answered"))
    check_eq("E1 lower-case q1 and the aliases Q-1 / Q-R14 resolve to nothing: three records skipped as unknown ids",
             view["skipped"]["unknown_id"], 3)
    check_eq("E1 the id in a record is trimmed and then exact: ' Q3 ' answers Q3", status_of(view, "Q3"), "answered")

    words = {"gate A": "we settled Q10 as a group, reading a", "alias": "Q-R14 and Q-1 are the same as R-9",
             "glued": "see Q1-x and R-Q1 and Q1_a and Q1a"}
    for name, text in words.items():
        pipe = {"gates": {"A": {"decision": "approved", "authorization_source": text}}}
        v = QR.load(write_story(tmp / ("e1n-" + name.replace(" ", "")), [q("Q1"), q("Q10")], pipeline=pipe))
        check_eq(f"E1 the id inside other text is not named ({name}): Q1 stays open", status_of(v, "Q1"), "open")
    check_eq("E1 ... while the exact token Q10 in the same words is named",
             status_of(QR.load(write_story(tmp / "e1n-q10", [q("Q1"), q("Q10")],
                                           pipeline={"gates": {"A": {"authorization_source": words["gate A"]}}})), "Q10"),
             "named")

    got = parse("Q10: a\nQ1: b", questions=("Q1", "Q10"))
    check_eq("E1 parser: Q10 and Q1 are different questions", got["choices"], {"Q1": "b", "Q10": "a"})
    got = parse("Q10: a", questions=("Q1",))
    check_eq("E1 parser: Q10 is not Q1 (unknown, Q1 untokened)", (got["choices"], got["unknown_ids"], got["untokened_questions"]),
             ({}, ["Q10"], ["Q1"]))
    for alias in ("Q-1", "Q-R14", "R-14", "q1", "Q 1", "Q01", "TS-6"):
        got = parse(f"{alias}: a", questions=("Q1", "Q2"))
        ok = got["choices"] == {} and got["untokened_questions"] == ["Q1", "Q2"]
        check(f"E1 parser: the alias {alias!r} chooses nothing", ok, str(got))
    for alias in ("Q-1", "Q-R14", "q1"):
        check_eq(f"E1 parser: {alias!r} is reported as an unknown id", parse(f"{alias}: b")["unknown_ids"], [alias])
    check_eq("E1 parser: an id with surrounding spaces in the REGISTER is trimmed, exact after that",
             QR.parse_choices("Q1: a", [{"id": " Q1 ", "readings": [1, 2]}], [])["choices"], {"Q1": "a"})


# ------------------------------------------------------------------------------------------------
# E2 - load(): statuses and fields
# ------------------------------------------------------------------------------------------------

def test_e2_load(tmp):
    vocab = QR.vocabulary()
    check_eq("E2 the statuses are the closed list of the data file",
             vocab["statuses"], ["open", "answered", "not_needed", "with_designer", "named", "deferred_to_report", "repeat"])
    check("E2 `named` is never a recordable status", "named" not in vocab["recorded_statuses"])
    # HF2-7 P5a (t-108, accepted): `S4 stop` joined the closed list (and `where_words`) - the S4 stop is a place a person answers
    check_eq("E2 the where-values are the owner's closed list",
             vocab["where"], ["gate A", "gate B", "S2 stop", "S3 stop", "S4 stop", "waiver", "remark", "conductor", "stage ran"])
    check_eq("E2 the stop reasons are in the data file (Q5)", vocab["stop_reasons"],
             ["scope_or_structure", "no_readings", "dependent", "over_threshold", "low_confidence", "blocking"])
    check_eq("E2 who-recorded is a closed list of the data file (edge 4)", vocab["by"],
             ["person", "conductor", "driver", "orchestrator"])
    check_eq("E2 the case decisions are a closed list of the data file", vocab["case_decisions"], ["manual", "automate"])
    check("E2 the data file has no default `where` (a write must say where)", "default_where" not in vocab)

    answers = [rec("Q2", reading="b", words="Q2: b - because", where="S2 stop"),
               rec("Q3", "not_needed", words="not needed: out of scope Q3"),
               rec("Q4", "with_designer", words="the designer will reword Q4"),
               rec("Q5"), rec("Q5", "open", words="reopened Q5", where="conductor")]
    root = write_story(tmp / "e2", [q("Q1"), q("Q2"), q("Q3"), q("Q4"), q("Q5")], answers=answers)
    view = QR.load(root)
    check_eq("E2 statuses: no record open, answered, not_needed, with_designer, reopened open",
             [status_of(view, x) for x in ("Q1", "Q2", "Q3", "Q4", "Q5")],
             ["open", "answered", "not_needed", "with_designer", "open"])
    q2 = row_of(view, "Q2")
    check_eq("E2 an answered question carries reading, words, where, at and the line with its id",
             (q2["reading"], q2["words"], q2["where"], q2["at"], q2["line"]),
             ("b", "Q2: b - because", "S2 stop", "2026-09-30T10:00:00+00:00", "Q2: b - because"))
    check_eq("E2 not_needed carries no reading", (row_of(view, "Q3")["reading"], row_of(view, "Q3")["line"]),
             ("", "not needed: out of scope Q3"))
    q1 = row_of(view, "Q1")
    check_eq("E2 an open question with no record has empty words/where/at/line/reading",
             (q1["reading"], q1["words"], q1["where"], q1["at"], q1["line"]), ("", "", "", "", ""))
    check_eq("E2 a reopen keeps the reopening words and place, and the status is open",
             (row_of(view, "Q5")["status"], row_of(view, "Q5")["words"], row_of(view, "Q5")["where"]),
             ("open", "reopened Q5", "conductor"))
    check("E2 every returned status is in the closed list", all(x["status"] in vocab["statuses"] for x in view["questions"]))
    check_eq("E2 the record's line is empty when the words do not carry the id",
             row_of(QR.load(write_story(tmp / "e2b", [q("Q1")], answers=[rec("Q1", words="a plain reading")])), "Q1")["line"], "")
    check_eq("E2 the register row keeps its own keys (readings, severity)", (q1["severity"], len(q1["readings"]), q1["readings_count"], q1["letters"]),
             ("major", 2, 2, "ab"))

    # named: a story with NO answers file, the exact id in the person's recorded gate words
    pipe = {"gates": {"A": {"id": "g1", "decision": "approved", "authorization_source": CMP1_GATE_A},
                      "B": {"decision": "approved", "authorization_source": ""}}}
    cmp_q = [q(f"Q{i}") for i in range(1, 6)]
    named = QR.load(write_story(tmp / "e2n", cmp_q, pipeline=pipe))
    check_eq("E2 no answers file + the id in authorization_source: all five are `named`, none `answered`",
             [status_of(named, f"Q{i}") for i in range(1, 6)], ["named"] * 5)
    n1 = row_of(named, "Q1")
    check("E2 `named` carries the line of the words that has the id, the words whole and where=gate A",
          n1["line"].startswith("- **Q1 / Q-R14 / R-9") and n1["words"] == CMP1_GATE_A and n1["where"] == "gate A"
          and n1["reading"] == "" and n1["at"] == "")
    check_eq("E2 the answers file is reported absent", named["answers_present"], False)
    check_eq("E2 a question with no record has changed_since_answer False and no stored hash",
             (n1["changed_since_answer"], n1["record_row_hash"]), (False, ""))
    for key, text in (("words", "Q2: a"), ("decision", "answered Q2 as a")):
        v = QR.load(write_story(tmp / f"e2-{key}", [q("Q2")], pipeline={"gates": {"A": {key: text}}}))
        check_eq(f"E2 the recorded words are also read from `{key}`", status_of(v, "Q2"), "named")
    v = QR.load(write_story(tmp / "e2-order", [q("Q2"), q("Q3")],
                            pipeline={"gates": {"A": {"authorization_source": "about Q3", "words": "about Q2", "decision": "Q2"}}}))
    check_eq("E2 authorization_source first, then words, then decision (the first non-empty one is the words)",
             (status_of(v, "Q2"), status_of(v, "Q3")), ("open", "named"))
    v = QR.load(write_story(tmp / "e2-gb", [q("Q2")], pipeline={"gates": {"B": {"authorization_source": "settled Q2"}}}))
    check_eq("E2 gate B words name it too, and say so", (status_of(v, "Q2"), row_of(v, "Q2")["where"]), ("named", "gate B"))
    v = QR.load(write_story(tmp / "e2-other", [q("Q2")], pipeline={"gates": {"C": {"authorization_source": "Q2"}},
                                                                    "gate_waivers": [{"requirement": "Q2", "decision": "Q2"}],
                                                                    "remarks": [{"text": "Q2"}]}))
    check_eq("E2 only gate words name a question (a waiver or a remark does not)", status_of(v, "Q2"), "open")
    v = QR.load(write_story(tmp / "e2-file", [q("Q2"), q("Q3")], answers=[rec("Q3")],
                            pipeline={"gates": {"A": {"authorization_source": "Q2 reading a"}}}))
    check_eq("E2 edge 8: with an answers file, `named` is still computed for the question with NO record: Q2 named, Q3 answered",
             (status_of(v, "Q2"), status_of(v, "Q3")), ("named", "answered"))
    v = QR.load(write_story(tmp / "e2-one", cmp_q, answers=[rec("Q3")], pipeline=pipe))
    check_eq("E2 edge 8: one recorded answer (Q3) does not turn the other four named questions into plain open",
             [status_of(v, f"Q{i}") for i in range(1, 6)], ["named", "named", "answered", "named", "named"])
    v = QR.load(write_story(tmp / "e2-empty-file", [q("Q2")], answers=[""],
                            pipeline={"gates": {"A": {"authorization_source": "Q2 reading a"}}}))
    check_eq("E2 edge 8: an EMPTY answers file is a file with no record: the named question stays named",
             (status_of(v, "Q2"), v["answers_present"]), ("named", True))
    v = QR.load(write_story(tmp / "e2-reopen", [q("Q2")], answers=[rec("Q2", "open", words="reopened")],
                            pipeline={"gates": {"A": {"authorization_source": "Q2 reading a"}}}))
    check_eq("E2 a reopened question HAS a record: open, never named again", status_of(v, "Q2"), "open")
    check("E2 a mention never yields `answered` (the error direction of the reader is toward open)",
          all(x["status"] != "answered" for x in named["questions"]))


# ------------------------------------------------------------------------------------------------
# E3 - the answers file
# ------------------------------------------------------------------------------------------------

def test_e3_answers_file(tmp):
    root = write_story(tmp / "e3", [q("Q1"), q("Q2")], answers=[
        rec("Q1", reading="a"), rec("Q1", reading="b", words="second"), rec("Q2")])
    check_eq("E3 the LAST record per id wins", (row_of(QR.load(root), "Q1")["reading"], row_of(QR.load(root), "Q1")["words"]),
             ("b", "second"))
    root = write_story(tmp / "e3b", [q("Q1")], answers=[rec("Q1"), "{not json", "[1, 2]", "\"text\"", "5", "null", "",
                                                        rec("Q99"), json.dumps({"id": "Q1"}), json.dumps({"status": "answered"}),
                                                        json.dumps({"id": 5, "status": "answered"}),
                                                        json.dumps({"id": "Q1", "status": "invented"}),
                                                        "\x00\x01 garbage", "{" * 5000])
    view, exc = safe(QR.load, root)
    check("E3 broken, non-object, unknown-id and malformed lines never raise", exc is None, repr(exc))
    check_eq("E3 they are counted: 3 broken, 4 non-object ([1,2], string, 5, null), 1 unknown id, 4 invalid",
             view["skipped"], {"broken_lines": 3, "non_object_lines": 4, "unknown_id": 1, "invalid": 4, "unreadable_file": 0})
    check_eq("E3 the good record before them still stands", status_of(view, "Q1"), "answered")
    check_eq("E3 a broken line after the good one does not hide it (last VALID record wins)",
             status_of(QR.load(write_story(tmp / "e3c", [q("Q1")], answers=[rec("Q1"), "{oops"])), "Q1"), "answered")
    bom = write_story(tmp / "e3d", [q("Q1")])
    (bom / "work" / "question-answers.jsonl").write_bytes(b"\xef\xbb\xbf" + (rec("Q1") + "\r\n" + rec("Q1", "not_needed") + "\r\n").encode())
    check_eq("E3 a BOM and CRLF line ends in the answers file are read", status_of(QR.load(bom), "Q1"), "not_needed")
    raw = write_story(tmp / "e3e", [q("Q1")])
    (raw / "work" / "question-answers.jsonl").write_bytes(b"\xff\xfe\xfa\n" + rec("Q1").encode() + b"\n")
    view, exc = safe(QR.load, raw)
    check("E3 invalid UTF-8 in a line is skipped, the rest is read", exc is None and status_of(view, "Q1") == "answered", repr(exc))

    # what the writer puts in a record, and a file whose last line has no newline
    tail = write_story(tmp / "e3f", [q("Q1"), q("Q2")], answers=[rec("Q1")])  # no trailing newline, as after a crash
    written = put(tail, "Q2", "answered", "Q2: a", reading="a", by="conductor")
    lines = (tail / "work" / "question-answers.jsonl").read_text(encoding="utf-8").split("\n")
    check_eq("E3 an append after a line with no newline starts a new line (two records, then the final newline)",
             (len(lines), lines[-1], json.loads(lines[1])["id"]), (3, "", "Q2"))
    check_eq("E3 a record carries kind, id, status, reading, words, by, where, at and row_hash",
             sorted(written), sorted(["kind", "id", "status", "reading", "words", "by", "where", "at", "row_hash"]))
    check_eq("E3 the record's kind is `question`", written["kind"], "question")
    check_eq("E3 the row_hash of the record is the hash of the row it was shown (64 hex)",
             (written["row_hash"], len(written["row_hash"])), (row_hash_of(tail, "Q2"), 64))
    check_eq("E3 with no reading the key is absent", "reading" in put(tail, "Q1", "not_needed", "no"), False)


# ------------------------------------------------------------------------------------------------
# E4 - the register file
# ------------------------------------------------------------------------------------------------

def test_e4_register(tmp):
    view = QR.load(tmp / "nothing-here")
    check_eq("E4 a story with no readiness file: no questions, register_present false, no exception",
             (view["questions"], view["register_present"], view["answers_present"]), ([], False, False))
    for name, raw in (("empty", ""), ("blank", "  \n"), ("not json", "{oops"), ("a list", "[1, 2]"),
                      ("a string", "\"x\""), ("deep", "[" * 100000), ("null", "null")):
        view, exc = safe(QR.load, write_story(tmp / ("e4-" + name.replace(" ", "")), readiness_raw=raw))
        check(f"E4 a readiness file that is {name}: no exception, no questions, one problem stated",
              exc is None and view["questions"] == [] and len(view["problems"]) == 1, f"{exc!r} {view}")
    bom = write_story(tmp / "e4-bom", readiness_raw=BOM + json.dumps({"open_questions": [q("Q1")]}))
    check_eq("E4 a BOM on the readiness file is read", [x["id"] for x in QR.load(bom)["questions"]], ["Q1"])
    for name, value in (("missing", None), ("null", None), ("a dict", {"a": 1}), ("a string", "Q1"), ("a number", 3)):
        body = {"verdict": "blocked"} if name in ("missing",) else {"open_questions": value}
        view, exc = safe(QR.load, write_story(tmp / ("e4o-" + name.replace(" ", "")), readiness_raw=json.dumps(body)))
        expected_problems = 1 if name in ("a dict", "a string", "a number") else 0
        check(f"E4 open_questions {name}: no exception, no questions, {expected_problems} problem(s)",
              exc is None and view["questions"] == [] and len(view["problems"]) == expected_problems, f"{exc!r} {view}")
    rows = [q("Q1"), "text", None, 5, {"question": "no id"}, {"id": ""}, {"id": "   "}, {"id": 7}, {"id": ["Q"]}, q("Q2"),
            {"id": "Q1", "question": "the duplicate"}, {"id": " Q2 ", "question": "another duplicate, trimmed"}, q("Q3", 0)]
    view, exc = safe(QR.load, write_story(tmp / "e4-rows", readiness_raw=json.dumps({"open_questions": rows})))
    check("E4 rows that are not objects or carry no usable id: no exception", exc is None, repr(exc))
    check_eq("E4 only the rows with an id are questions; duplicates are not merged (the first is kept)",
             [x["id"] for x in view["questions"]], ["Q1", "Q2", "Q3"])
    check_eq("E4 the kept Q1 is the FIRST one", row_of(view, "Q1")["question"], "question Q1?")
    check_eq("E4 duplicates are reported by id", view["duplicates"], ["Q1", "Q2"])
    check("E4 every skipped row and duplicate is stated in problems (2 duplicates + 8 unusable rows)", len(view["problems"]) == 10,
          "\n".join(view["problems"]))
    check_eq("E4 a question with no readings has readings_count 0 and no letters", (row_of(view, "Q3")["readings_count"], row_of(view, "Q3")["letters"]), (0, ""))
    check_eq("E4 readings that are not a list count as none",
             row_of(QR.load(write_story(tmp / "e4-rd", [{"id": "Q1", "readings": "ab"}])), "Q1")["readings_count"], 0)
    check_eq("E4 an answer for a register with no questions: the record is skipped as unknown",
             QR.load(write_story(tmp / "e4-none", [], answers=[rec("Q1")]))["skipped"]["unknown_id"], 1)
    check_eq("E4 load() takes a str as well as a Path", len(QR.load(str(write_story(tmp / "e4-str", [q("Q1")])))["questions"]), 1)


# ------------------------------------------------------------------------------------------------
# E5 - the strict parser
# ------------------------------------------------------------------------------------------------

def test_e5_parser(tmp):
    # edge 1: a strict token is the WHOLE line - after the value only spaces, at most one of . , ;
    positive = {
        "Q1: a": "a", "Q1: a.": "a", "Q1: a;": "a", "Q1: a,": "a", "Q1:a": "a", "Q1 : a": "a", "Q1 = a": "a",
        "Q1 = b": "b", "Q1=b": "b", "- Q1: a": "a", "* Q1: a": "a", "1. Q1: a": "a", "12. Q1: a": "a",
        "1) Q1: a": "a", "2) Q1: b": "b", "- 3) Q1: a": "a",
        "**Q1: a**": "a", "**Q1**: a": "a", "`Q1`: a": "a", "`Q1: a`": "a", "- **Q1: a**": "a", "  - `Q1: b`": "b",
        "- **Q1**: a.": "a", "Q1: a .": "a", "Q1: a  ;  ": "a",
        "Q1:\ta": "a", "Q1: a   ": "a", "Q1: a\r": "a", "- - Q1: a": "a", BOM + "Q1: a": "a",
        BULLET + " Q1: a": "a", BULLET + BULLET + "Q1: a": "a",
        "Q1:" + NBSP + "a": "a", "Q1" + NBSP + ": a": "a", NBSP + "Q1: a": "a", "Q1: a" + NBSP: "a",
        "Q1: a" + NBSP + ".": "a", NBSP + "- Q1: a": "a", "-" + NBSP + "Q1: a": "a", "1." + NBSP + "Q1: a": "a",
    }
    for text, letter in positive.items():
        got = parse(text)
        check_eq(f"E5 edge 1: {text!r} IS a choice Q1={letter}", got["choices"], {"Q1": letter})
    for text in ("Q1: not needed", "- Q1: not needed.", "**Q1: not needed**", "Q1: not needed;", "Q1 = not needed ,",
                 "Q1:" + NBSP + "not needed", "Q1: not needed" + NBSP):
        got = parse(text)
        check_eq(f"E5 edge 1: {text!r} IS `not needed`", (got["not_needed"], got["choices"]), (["Q1"], {}))

    negative = [
        # edge 1: text after the value makes the line prose, not a token
        "Q1: a, b or not needed", "Q1: a, but only if the API allows it", "Q1: a.k.a. the old flow", "Q1: a, b",
        "Q1: not needed. Actually it is needed", "Q1: a; Q2: b", "Q1: a, no wait, b", "Q1: a. The rest is prose",
        "Q1: a, because the ticket says so", "Q1: a.,", "Q1: a..", "Q1: a,;", "Q1: not needed, out of scope",
        "Q1 = not needed, out of scope", "Q1: a. b", "Q1: a; b",
        "Q1 a", "Q3 a scope question for the owner", "Q1 - reading (a)", "Q1: a question for later", "Q1: a b",
        "Q1: (a)", "Q1: a)", "reading (a) for Q1", "I think Q1: a", "not Q1: a", "Q1 not a", "(a) Q1", "a) Q1",
        "Q1: A", "Q1: ab", "Q1: ", "Q1:", "Q1: 1", "Q1: -a", "Q1: not needed at all", "Q1: not neededness", "Q1: notneeded",
        "Q1: Not needed", "> Q1: a", "     - a) the first reading is intended", "Q1 :: a", "Q1:: a",
        "Q1: " + CYR_A, "Q1" + FULL_COLON + "a", "Q1" + FULL_COLON + " a", "Q1: " + FULL_A, "Q1: a" + ACUTE + "x", "Q1 / Q-R14: a",
        "Q1: a a", "Q1: a -", "Q1: a and Q2: b", "Q1: a" + NBSP + "b", "Q1: a" + FULL_COLON,
    ]
    for text in negative:
        got = parse(text)
        check(f"E5 edge 1: {text!r} is NOT a token: nothing chosen, nothing reported", got["choices"] == {} and got["not_needed"] == []
              and got["conflicts"] == [] and got["out_of_range"] == [], str(got))
    got = parse("Q1: a; Q2: b")
    check_eq("E5 edge 1: `Q1: a; Q2: b` (two tokens on one line) takes neither, and both ids are reported untokened",
             (got["choices"], got["untokened_questions"]), ({}, ["Q1", "Q2"]))
    got = parse("Q1: a, b or not needed")
    check_eq("E5 edge 1: `Q1: a, b or not needed` chooses nothing and Q1 is untokened",
             (got["choices"], got["not_needed"], got["untokened_questions"]), ({}, [], ["Q1", "Q2"]))
    got = parse("Q1: a, but only if the API allows it")
    check_eq("E5 edge 1: `Q1: a, but only if the API allows it` chooses nothing (the text after the value)",
             got["choices"], {})
    for text in (f"{CASES[8]}: automate, not manual", f"{CASES[8]}: manual because it is slow", f"{CASES[8]}: manual, automate",
                 f"{CASES[8]}: automate. Then again no"):
        check_eq(f"E5 edge 1: case line {text!r} is NOT a case token", parse(text)["case_tokens"], [])
    for text, decision in ((f"{CASES[8]}: automate", "automate"), (f"{CASES[8]}: manual.", "manual"),
                           (f"- **{CASES[8]}**: manual;", "manual"), (f"{CASES[8]}" + NBSP + ": automate", "automate")):
        got = parse(text)
        check_eq(f"E5 edge 1: case line {text!r} IS a case token", [(t["case"], t["decision"]) for t in got["case_tokens"]],
                 [(CASES[8], decision)])
    check_eq("E5 a Cyrillic look-alike letter is not the Latin one", parse("Q1: " + CYR_A)["untokened_questions"], ["Q1", "Q2"])
    check_eq("E5 a full-width colon is not the separator", parse("Q1" + FULL_COLON + "a")["choices"], {})
    check_eq("E5 the same letter twice is one choice, not a conflict",
             (parse("Q1: a\nQ1: a")["choices"], parse("Q1: a\nQ1: a")["conflicts"]), ({"Q1": "a"}, []))
    got = parse("Q1: a\nQ1: b")
    check_eq("E5 two different letters for one id: a conflict, nothing chosen, the question stays untokened",
             (got["choices"], got["conflicts"], got["untokened_questions"]),
             ({}, [{"id": "Q1", "values": ["a", "b"]}], ["Q1", "Q2"]))
    got = parse("Q1: a\nQ1: not needed")
    check_eq("E5 a letter and `not needed` for one id conflict", (got["conflicts"], got["not_needed"], got["choices"]),
             ([{"id": "Q1", "values": ["a", "not needed"]}], [], {}))
    got = parse("Q1: c\nQ2: b")
    check_eq("E5 a letter beyond the readings is out_of_range and chooses nothing",
             (got["choices"], got["out_of_range"], got["untokened_questions"]),
             ({"Q2": "b"}, [{"id": "Q1", "letter": "c", "readings": 2}], ["Q1"]))
    check_eq("E5 the boundary: the last letter of 8 readings is in range, the ninth is not",
             (parse("Q1: h", readings=8)["choices"], parse("Q1: i", readings=8)["out_of_range"]),
             ({"Q1": "h"}, [{"id": "Q1", "letter": "i", "readings": 8}]))
    check_eq("E5 nine readings give the letter i; 26 give z; the 27th letter does not exist",
             (parse("Q1: i", readings=9)["choices"], parse("Q1: z", readings=26)["choices"], parse("Q1: z", readings=25)["out_of_range"] != []),
             ({"Q1": "i"}, {"Q1": "z"}, True))
    check_eq("E5 a question with no readings takes no letter", parse("Q1: a", readings=0)["out_of_range"],
             [{"id": "Q1", "letter": "a", "readings": 0}])
    check_eq("E5 a question with 'not needed' needs no readings", parse("Q1: not needed", readings=0)["not_needed"], ["Q1"])
    got = parse("Q1: a\nQ2: b\nQ7: a", questions=("Q1", "Q2", "Q3"))
    check_eq("E5 untokened lists the register questions nobody spoke of (Q3), unknown ids are reported (Q7)",
             (got["untokened_questions"], got["unknown_ids"]), (["Q3"], ["Q7"]))
    check_eq("E5 an id-less 'Note: a' is not reported as an unknown id (no digit in it)", parse("Note: a")["unknown_ids"], [])

    # case tokens
    full = CASES[8]  # TP1-13797_TC_009
    got = parse(f"{full}: manual\n{CASES[5]}: automate")
    check_eq("E5 `<full case id>: manual|automate` are case tokens",
             got["case_tokens"], [{"case": full, "decision": "manual", "written": full},
                                  {"case": CASES[5], "decision": "automate", "written": CASES[5]}])
    got = parse("- **TC_009: manual**\n1. TC_010: automate.")
    check_eq("E5 a short case id resolves when exactly one given case id ends with _<it>",
             [(t["case"], t["decision"], t["written"]) for t in got["case_tokens"]],
             [(full, "manual", "TC_009"), (CASES[9], "automate", "TC_010")])
    got = parse("TC_009: manual", cases=[full, "OTHER-1_TC_009"])
    check_eq("E5 a short id that two case ids end with is unresolved, with its candidates",
             (got["case_tokens"], got["unresolved_short_ids"]),
             ([], [{"id": "TC_009", "candidates": [full, "OTHER-1_TC_009"]}]))
    got = parse("TC_099: manual\nTC_099: automate")
    check_eq("E5 a short id no case ends with is unresolved (once), not guessed",
             (got["case_tokens"], got["unresolved_short_ids"]), ([], [{"id": "TC_099", "candidates": []}]))
    check_eq("E5 a short id is matched after the underscore only: TC_9 is not TC_009",
             parse("TC_9: manual")["case_tokens"], [])
    check_eq("E5 a Cyrillic look-alike in a case id resolves nothing",
             parse(CYR_TS + "_009: manual")["case_tokens"], [])
    got = parse(f"{full}: manual\n{full}: automate")
    check_eq("E5 manual and automate for one case conflict; no case token", (got["case_tokens"], got["conflicts"]),
             ([], [{"id": full, "values": ["manual", "automate"]}]))
    got = parse(f"{full}: manual\nTC_009: manual")
    check_eq("E5 the full and the short form of one case, same decision: one token", len(got["case_tokens"]), 1)
    check_eq("E5 a case token needs the strict tail: 'manual because' and '(manual)' are not tokens",
             (parse(f"{full}: manual because it is slow")["case_tokens"], parse(f"{full}: (manual)")["case_tokens"]), ([], []))
    check_eq("E5 'Q1: manual' is no case token and no choice",
             (parse("Q1: manual")["case_tokens"], parse("Q1: manual")["choices"], parse("Q1: manual")["unresolved_short_ids"]), ([], {}, []))
    check_eq("E5 a letter after a case id is no token, and the id is reported unknown",
             (parse(f"{full}: a")["case_tokens"], parse(f"{full}: a")["unknown_ids"]), ([], [full]))
    check_eq("E5 the parser handles no case ids at all", parse("TC_009: manual", cases=[])["unresolved_short_ids"],
             [{"id": "TC_009", "candidates": []}])

    # never alters the words; tolerates any input
    words = "  - Q1: a\r\n" + BOM + E_ACUTE + " " + HELLO + "\n"
    kept = str(words)
    parse(words)
    check_eq("E5 the words are not altered (a str is immutable; the parser returns no copy of them)", words, kept)
    for odd in (None, "", "   ", 5, b"Q1: a"):
        got, exc = safe(parse, odd)
        check(f"E5 input {odd!r}: no exception, nothing chosen", exc is None and got["choices"] == {}, repr(exc))
    got, exc = safe(QR.parse_choices, "Q1: a", None, None)
    check("E5 no questions and no case ids: an empty result", exc is None and got["untokened_questions"] == [], repr(exc))
    got, exc = safe(QR.parse_choices, "Q1: a", [None, "Q1", {"id": None}, {"id": ""}, {"readings": [1]}, q("Q1")], [None, "", 5])
    check("E5 malformed question rows and case ids are ignored", exc is None and got["choices"] == {"Q1": "a"}, repr(exc))


# ------------------------------------------------------------------------------------------------
# E6 - the CLI
# ------------------------------------------------------------------------------------------------

def cli(*args):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            code = QR.main(list(args))
        except SystemExit as exc:
            code = exc.code
    return code, out.getvalue(), err.getvalue()


def test_e6_cli(tmp):
    proj = temp_project("qa-question-register-")
    try:
        use_project(proj)
        task = proj / "qa-factory" / "artifacts" / "QA-9"
        write_story(task, [q("Q1"), q("Q10", 3), q("Q3")])
        answers = task / "work" / "question-answers.jsonl"

        before = snapshot(proj)
        code, out, err = cli("--task", "QA-9", "--show")
        shown = json.loads(out)
        check_eq("E6 --show exits 0 and prints ONE JSON document on stdout (stderr empty)", (code, err), (0, ""))
        check_eq("E6 --show lists the questions with their status", [(x["id"], x["status"]) for x in shown["questions"]],
                 [("Q1", "open"), ("Q10", "open"), ("Q3", "open")])
        check_eq("E6 --show writes nothing (every byte of the project is as it was, no answers file)",
                 (snapshot(proj) == before, answers.exists()), (True, False))

        def hash_args(qid):
            return ["--register-hash", next(x["row_hash"] for x in shown["questions"] if x["id"] == qid)]

        base = ["--where", "gate A", "--by", "conductor"]
        check_eq("E6 edge 3: --show prints each row's own hash (64 hex, distinct per row)",
                 (all(len(x["row_hash"]) == 64 for x in shown["questions"]), len({x["row_hash"] for x in shown["questions"]})),
                 (True, 3))
        code, out, err = cli("--task", "QA-9", "--answer", "Q1", "--reading", "a", "--words", "Q1: a - the ACK is intended",
                             *base, *hash_args("Q1"))
        got = json.loads(out)
        check_eq("E6 --answer with a reading records an answered question", (code, got["question"]["status"], got["question"]["reading"]),
                 (0, "answered", "a"))
        check_eq("E6 the record carries where and by as given, kind `question`, and the hash passed back (--register-hash)",
                 (got["recorded"]["where"], got["recorded"]["by"], got["recorded"]["kind"], got["recorded"]["row_hash"]),
                 ("gate A", "conductor", "question", hash_args("Q1")[1]))
        check_eq("E6 edge 3: the row is as it was shown, so changed_since_answer is False",
                 got["question"]["changed_since_answer"], False)
        code, out, _ = cli("--task", "QA-9", "--answer", "Q10", "--words", "the designer's new Then", "--where", "S2 stop",
                           "--by", "driver", *hash_args("Q10"))
        got = json.loads(out)
        check_eq("E6 --answer with no --reading is legal (the designer road): answered, empty reading, where as given",
                 (code, got["question"]["status"], got["question"]["reading"], got["question"]["where"]), (0, "answered", "", "S2 stop"))
        code, out, _ = cli("--task", "QA-9", "--not-needed", "Q3", "--words", "not needed, the ticket drops it", "--where", "gate A",
                           "--by", "person", *hash_args("Q3"))
        check_eq("E6 --not-needed records not_needed", (code, json.loads(out)["question"]["status"]), (0, "not_needed"))
        code, out, _ = cli("--task", "QA-9", "--reopen", "Q1", "--words", "the person changed their mind", *base)
        got = json.loads(out)
        check_eq("E6 --reopen puts it back to open and keeps the reopening words; the hash is optional for it",
                 (code, got["question"]["status"], got["question"]["words"], got["question"]["changed_since_answer"]),
                 (0, "open", "the person changed their mind", None))
        code, out, _ = cli("--task", "QA-9", "--answer", "Q1", "--reading", "b", "--words", "- Q1: b", *base, *hash_args("Q1"))
        got = json.loads(out)
        check_eq("E6 an answer after a reopen wins; words that START WITH A HYPHEN are taken whole, not read as an option",
                 (code, got["question"]["status"], got["question"]["reading"], got["question"]["words"]), (0, "answered", "b", "- Q1: b"))
        # HF2-7: Q1 is settled (b), so another answer needs the door first (`--reopen`); this key is about the words
        cli("--task", "QA-9", "--reopen", "Q1", "--words", "the person changed their mind again", *base)
        code, out, _ = cli("--task", "QA-9", "--answer", "Q1", "--reading", "a", "--words", "-x", *base, *hash_args("Q1"))
        check_eq("E6 a bare '-x' as the words is a value too", (code, json.loads(out)["recorded"]["words"]), (0, "-x"))

        file_before = answers.read_bytes()
        ok_hash = hash_args("Q1")
        refusals = [
            ("a letter out of range", ["--answer", "Q1", "--reading", "c", "--words", "w"], ["beyond the 2 readings of Q1", "Valid: a, b"]),
            ("a letter for a question with more readings still bounded", ["--answer", "Q10", "--reading", "d", "--words", "w"], ["Valid: a, b, c"]),
            ("an uppercase letter", ["--answer", "Q1", "--reading", "A", "--words", "w"], ["one Latin letter a-z"]),
            ("a Cyrillic letter", ["--answer", "Q1", "--reading", CYR_A, "--words", "w"], ["one Latin letter a-z"]),
            ("two letters", ["--answer", "Q1", "--reading", "ab", "--words", "w"], ["one Latin letter a-z"]),
            ("an unknown id", ["--answer", "Q9", "--words", "w"], ["no question with id 'Q9'", "Q1, Q10, Q3", "exact, case-sensitive"]),
            ("a lower-case id", ["--answer", "q1", "--words", "w"], ["no question with id 'q1'"]),
            ("an alias id", ["--answer", "Q-R14", "--words", "w"], ["no question with id 'Q-R14'", "aliases"]),
            ("a prefix of an id", ["--answer", "Q", "--words", "w"], ["no question with id 'Q'"]),
            ("a longer id", ["--answer", "Q1x", "--words", "w"], ["no question with id 'Q1x'"]),
            ("blank words", ["--answer", "Q1", "--words", "   "], ["the words are blank", "--words"]),
            ("empty words", ["--answer", "Q1", "--words", ""], ["the words are blank"]),
            ("newline-only words", ["--not-needed", "Q1", "--words", "\n\t\r\n"], ["the words are blank"]),
            ("no words at all", ["--answer", "Q1"], ["the words are blank"]),
            ("an unknown --where", ["--answer", "Q1", "--words", "w", "--where", "gate_A"],
             ["where 'gate_A' is not a known value", "gate A, gate B, S2 stop, S3 stop, S4 stop, waiver, remark, conductor, stage ran"]),
            ("edge 4: a missing --where (no default)", ["--answer", "Q1", "--words", "w"],
             ["--where is missing", "no default", "gate A, gate B, S2 stop, S3 stop, S4 stop, waiver, remark, conductor, stage ran"], ("--where",)),
            ("edge 4: a missing --where on --reopen", ["--reopen", "Q1", "--words", "w"], ["--where is missing", "no default"], ("--where",)),
            ("edge 4: a missing --by", ["--answer", "Q1", "--words", "w"],
             ["--by is missing", "no default", "person, conductor, driver, orchestrator"], ("--by",)),
            ("edge 4: an unknown --by", ["--answer", "Q1", "--words", "w", "--by", "the intern"],
             ["by 'the intern' is not a known value", "person, conductor, driver, orchestrator"]),
            ("edge 4: an empty --by", ["--answer", "Q1", "--words", "w", "--by", ""], ["--by is missing", "person, conductor"]),
            ("edge 3: --answer with no --register-hash", ["--answer", "Q1", "--words", "w"],
             ["register hash is missing", "row_hash", "--register-hash"], ("--register-hash",)),
            ("edge 3: --not-needed with no --register-hash", ["--not-needed", "Q1", "--words", "w"],
             ["register hash is missing"], ("--register-hash",)),
            ("edge 3: a register hash that is not a sha256", ["--answer", "Q1", "--words", "w", "--register-hash", "h"],
             ["is not a sha256", "row_hash"]),
            ("edge 3: a reopen with a malformed hash", ["--reopen", "Q1", "--words", "w", "--register-hash", "xyz"],
             ["is not a sha256"]),
            ("edge 6: both --words and --words-file", ["--answer", "Q1", "--words", "w", "--words-file", "whatever.txt"],
             ["exactly one of --words and --words-file"]),
            ("edge 6: neither --words nor --words-file", ["--answer", "Q1"], ["exactly one of --words and --words-file"]),
            ("edge 6: a --words-file that does not exist", ["--answer", "Q1", "--words-file", "no-such-file-here.txt"],
             ["could not be read", "UTF-8"]),
            ("edge 5: --keep-manual with a reading", ["--keep-manual", "TP1-13797_TC_009", "--words", "w", "--reading", "a"],
             ["only with an answer"]),
            ("edge 5: --keep-manual with no words", ["--keep-manual", "TP1-13797_TC_009"], ["the words are blank"]),
            ("edge 5: --keep-manual with no --where", ["--keep-manual", "TP1-13797_TC_009", "--words", "w"],
             ["--where is missing"], ("--where",)),
            ("edge 5: --automate with no --by", ["--automate", "TP1-13797_TC_009", "--words", "w"],
             ["--by is missing"], ("--by",)),
            ("edge 5: --case-ids-file with a question operation", ["--answer", "Q1", "--words", "w", "--case-ids-file", "x.txt"],
             ["--case-ids-file has no meaning"]),
            ("edge 5: --keep-manual and --automate together", ["--keep-manual", "A_TC_1", "--automate", "A_TC_2", "--words", "w"],
             ["exactly one operation", "got 2"]),
            ("a reading with --not-needed", ["--not-needed", "Q1", "--reading", "a", "--words", "w"], ["only with an answer"]),
            ("a reading with --reopen", ["--reopen", "Q1", "--reading", "a", "--words", "w"], ["only with an answer"]),
            ("no operation", ["--words", "w"], ["exactly one operation", "got 0"]),
            ("two operations", ["--answer", "Q1", "--reopen", "Q3", "--words", "w"], ["exactly one operation", "got 2"]),
            ("--show with words", ["--show", "--words", "w"], ["--show writes nothing", "--words"]),
            ("a task id that is a path", ["--answer", "Q1", "--words", "w", "--task", "../QA-9"], ["(got '../QA-9')"]),
        ]
        defaults = {"--where": "gate A", "--by": "person", "--register-hash": ok_hash[1]}
        for name, argv, needles, *omit in refusals:
            argv = list(argv)
            if "--task" not in argv:
                argv = ["--task", "QA-9"] + argv
            if "--show" not in argv:  # every refusal above is about ONE thing: the rest of the call is well-formed
                for flag, value in defaults.items():
                    if flag not in argv and flag not in (omit[0] if omit else ()):
                        if flag == "--register-hash" and any(op in argv for op in ("--reopen", "--keep-manual", "--automate")):
                            continue
                        argv += [flag, value]
            code, out, err = cli(*argv)
            check(f"E6 refused: {name} -> exit 2, stdout empty, the message says what is wrong and what is valid",
                  code == 2 and out == "" and all(n in err for n in needles), f"{code} out={out!r} err={err!r}")
        check_eq("E6 no refusal wrote anything", answers.read_bytes(), file_before)

        (proj / "qa-factory" / "artifacts" / "QA-NEW").mkdir()      # the story exists (S0 made it) and has no register yet
        code, out, err = cli("--task", "QA-NEW", "--answer", "Q1", "--words", "w", *base, *ok_hash)
        check("E6 a story with no register: refused, and the message says there are no register ids yet",
              code == 2 and "no register ids yet" in err, err)
        check_eq("E6 ... and nothing was created in it", list((proj / "qa-factory" / "artifacts" / "QA-NEW").iterdir()), [])
        code, out, err = cli("--task", "QA-9", "--answer", "Q1", "--words", "w", *base, *ok_hash, "--nonsense")
        check_eq("E6 an unknown option is argparse's own refusal (exit 2)", code, 2)
        code, out, err = cli("--answer", "Q1", "--words", "w")
        check_eq("E6 --task is required (exit 2)", code, 2)
        code, out, err = cli("--task", "QA-9", "--sho")
        check_eq("E6 an abbreviated option is refused, never guessed", code, 2)
    finally:
        cleanup(proj)


def test_e6_cli_subprocess(tmp):
    proj = temp_project("qa-question-register-sub-")
    try:
        task = proj / "qa-factory" / "artifacts" / "QA-9"
        write_story(task, [q("Q1"), q("Q2")])
        env = dict(os.environ, CLAUDE_PROJECT_DIR=str(proj), PYTHONDONTWRITEBYTECODE="1")
        script = str(harness.SCRIPTS / "question_register.py")

        def run(*args):
            return subprocess.run([sys.executable, "-B", script, *args], capture_output=True, encoding="utf-8",
                                  errors="replace", cwd=str(proj), env=env, timeout=120)

        proc = run("--task", "QA-9", "--show")
        check_eq("E6 subprocess: --show exits 0 and stdout is exactly one JSON document",
                 (proc.returncode, [x["id"] for x in json.loads(proc.stdout)["questions"]]), (0, ["Q1", "Q2"]))
        shown = {x["id"]: x["row_hash"] for x in json.loads(proc.stdout)["questions"]}
        tail = ["--where", "gate A", "--by", "conductor", "--register-hash", shown["Q1"]]
        words = BOM + "- Q1: a\r\n- Q2: not needed " + HELLO + " " + E_ACUTE + "\r\n"
        proc = run("--task", "QA-9", "--answer", "Q1", "--reading", "a", "--words", words, *tail)
        line = (task / "work" / "question-answers.jsonl").read_bytes().decode("utf-8").split("\n")[0]
        check_eq("E6 subprocess: BOM, CRLF and non-ASCII words are stored whole, byte for byte",
                 (proc.returncode, json.loads(line)["words"]), (0, words))
        proc = run("--task", "QA-9", "--answer", "Q1", "--reading", "z", "--words", "w", *tail)
        check("E6 subprocess: a refusal is exit 2 with an empty stdout and the message on stderr",
              proc.returncode == 2 and proc.stdout == "" and "beyond the 2 readings" in proc.stderr, proc.stderr)
        proc = run("--task", "QA-9", "--answer", "Q1", "--words", "w", "--by", "person", "--register-hash", shown["Q1"])
        check("E6 edge 4 subprocess: no --where is exit 2, the valid values are named, stdout is empty",
              proc.returncode == 2 and proc.stdout == "" and "--where is missing" in proc.stderr and "gate A, gate B" in proc.stderr,
              proc.stderr)
        long_file = tmp / "words-from-file.txt"
        long_words = BOM + ("- Q2: not needed " + HELLO + " " + E_ACUTE + "\r\n" + "x" * 100 + "\r\n") * 600
        long_file.write_bytes(long_words.encode("utf-8"))
        check("E6 edge 6: the words file is longer than a Windows command line (about 32 KB)", len(long_words.encode("utf-8")) > 60000)
        proc = run("--task", "QA-9", "--answer", "Q2", "--words-file", str(long_file), "--where", "gate B", "--by", "person",
                   "--register-hash", shown["Q2"])
        last = (task / "work" / "question-answers.jsonl").read_bytes().decode("utf-8").split("\n")
        check_eq("E6 edge 6 subprocess: --words-file words are stored whole, BOM and CRLF and non-ASCII kept",
                 (proc.returncode, json.loads(last[-2])["words"] == long_words, last[-1]), (0, True, ""))
        listed = tmp / "case-ids.txt"
        listed.write_bytes(("TP1-9_TC_001\n\nTP1-9_TC_002\n").encode("utf-8"))
        proc = run("--task", "QA-9", "--keep-manual", "TP1-9_TC_001", "--words", "w", "--where", "gate A", "--by", "person",
                   "--case-ids-file", str(listed))
        got = json.loads(proc.stdout) if proc.stdout else {}
        check_eq("E6 edge 5 subprocess: --keep-manual with a case ids file records the decision and says what it checked against",
                 (proc.returncode, got.get("recorded", {}).get("kind"), got.get("case_ids_checked_against")),
                 (0, "case", "--case-ids-file"))
        empty = temp_dir("qa-question-register-none-")  # outside any project: no marker on the way up
        try:
            proc = subprocess.run([sys.executable, "-B", script, "--task", "QA-9", "--show"], capture_output=True,
                                  encoding="utf-8", errors="replace", cwd=str(empty),
                                  env={k: v for k, v in env.items() if k != "CLAUDE_PROJECT_DIR"}, timeout=120)
        finally:
            cleanup(empty)
        check("E6 subprocess: outside a project the refusal is the project-marker one (exit 3), nothing on stdout",
              proc.returncode == 3 and proc.stdout == "", f"{proc.returncode} {proc.stderr}")
    finally:
        cleanup(proj)


# ------------------------------------------------------------------------------------------------
# E7 - the adversarial battery (parser and CLI)
# ------------------------------------------------------------------------------------------------

def timed(fn):
    start = time.perf_counter()
    result = fn()
    return result, time.perf_counter() - start


def test_e7_battery(tmp):
    got = parse("")
    check_eq("E7 empty words: nothing chosen, every question untokened", (got["choices"], got["untokened_questions"]), ({}, ["Q1", "Q2"]))
    check_eq("E7 CRLF line ends: each token is on its own line", parse("Q1: a\r\nQ2: b\r\n")["choices"], {"Q1": "a", "Q2": "b"})
    check_eq("E7 old-Mac CR line ends work too", parse("Q1: a\rQ2: b")["choices"], {"Q1": "a", "Q2": "b"})
    check_eq("E7 a BOM at the start of the words", parse(BOM + "Q1: a\nQ2: b")["choices"], {"Q1": "a", "Q2": "b"})
    check_eq("E7 non-ASCII prose around a token: the token line is read, the prose is not",
             parse(HELLO + " " + E_ACUTE + "\nQ1: a\n" + THEN + " " + ALPHABET + "\n")["choices"], {"Q1": "a"})
    check_eq("E7 non-ASCII text AFTER the value on the token line makes it prose",
             parse("Q1: a, " + THEN + " " + ALPHABET + "\n")["choices"], {})

    echoed = ("## Open questions (2)\n\n- **Q1** Is the mismatch intended?\n"
              "  - a) intended: 200 ACK\n  - b) unintended: stays 400\n    - a) nested echo\n"
              "  - a) TC_006 is automated at api and asserts 200\n     - b) keeps it manual\n\n"
              "Answer each question as `Q1: a` or `Q1: not needed`, or in your own words.")
    got = parse(echoed)
    check("E7 the gate text echoed back: '  - a)' lines and the question line are no choice",
          got["choices"] == {} and got["not_needed"] == [] and got["case_tokens"] == [], str(got))
    check_eq("E7 (the echo of the grammar hint alone, mid-sentence, is no token either)", parse("write `Q1: a` for reading a")["choices"], {})

    big = ("- Q1: a.  \n" + HELLO + " " + E_ACUTE + " a line of prose, then a second sentence\n") * 6000
    check("E7 the 200 KB body is at least 200000 characters", len(big) >= 200000)
    got, seconds = timed(lambda: parse(big))
    check("E7 200 KB of token lines parse in linear time (well under 10 s) and read Q1=a once", seconds < 10 and got["choices"] == {"Q1": "a"}, f"{seconds:.2f}s")
    shapes = {"markers": "- " * 100000 + "Q1: a", "asterisks": "*" * 200000, "one word": "x" * 200000,
              "spaces before colon": "Q1" + " " * 200000 + ": a", "numbered": "1. " * 70000 + "Q1: a",
              "backticks tail": "Q1: a" + "`" * 200000, "colons": ":" * 200000, "equals": "Q1" + "=" * 200000,
              "long id": "Q" * 200000 + ": a", "many short lines": "\n".join(["q"] * 100000), "only newlines": "\n" * 200000,
              "fence lines": "\n".join(["```"] * 70000), "quote marks": ">" * 200000, "no-break spaces": NBSP * 200000 + "Q1: a",
              "spaces after value": "Q1: a" + " " * 200000 + ".", "unclosed fence": "```\n" + "Q1: a\n" * 50000}
    for name, text in shapes.items():
        got, seconds = timed(lambda text=text: parse(text))
        check(f"E7 hostile shape '{name}' (200 KB) parses in linear time, no exception", seconds < 10, f"{seconds:.2f}s")
    check_eq("E7 the marker prefix of 100000 dashes still reads the token behind it", parse(shapes["markers"])["choices"], {"Q1": "a"})
    check_eq("E7 the numbered prefix ('1. ' repeated) is stripped in one pass", parse(shapes["numbered"])["choices"], {"Q1": "a"})
    check_eq("E7 a 200 KB id is no id", parse(shapes["long id"])["unknown_ids"], [])

    # the CLI with 200 KB words: in-process, because a Windows command line holds 32 KB
    proj = temp_project("qa-question-register-big-")
    try:
        use_project(proj)
        task = proj / "qa-factory" / "artifacts" / "QA-9"
        write_story(task, [q("Q1"), q("Q2")])
        def wh(qid):
            return ["--where", "gate A", "--by", "conductor", "--register-hash", row_hash_of(task, qid)]

        (code, out, err), seconds = timed(lambda: cli("--task", "QA-9", "--answer", "Q1", "--reading", "a", "--words", big, *wh("Q1")))
        stored = QR.load(task)
        check("E7 CLI: 200 KB of words is recorded in linear time and kept WHOLE (compared to the last character)",
              code == 0 and seconds < 10 and row_of(stored, "Q1")["words"] == big, f"{code} {seconds:.2f}s {err[:200]}")
        line = (task / "work" / "question-answers.jsonl").read_bytes().split(b"\n")
        check_eq("E7 CLI: the 200 KB answer is ONE line of the answers file", (len(line), line[1]), (2, b""))
        crlf = "\r\n".join(["- Q2: not needed", "", "and " + ALPHABET + " " + E_ACUTE, ""])
        code, out, _ = cli("--task", "QA-9", "--not-needed", "Q2", "--words", crlf, *wh("Q2"))
        got = row_of(QR.load(task), "Q2")["words"]
        check("E7 CLI: CRLF and non-ASCII words are stored whole", code == 0 and got == crlf, f"{code} {got[:80]!r}")
        bom = BOM + "- Q1: a"
        # HF2-7: Q1 is settled with reading `a`; the keys below are about the WORDS, so they repeat the same answer (`--reading a`),
        # which is appended as it always was - a different answer would need `--reopen` first
        code, out, _ = cli("--task", "QA-9", "--answer", "Q1", "--reading", "a", "--words", bom, *wh("Q1"))
        got = row_of(QR.load(task), "Q1")["words"]
        check("E7 CLI: a BOM in the words is stored, not eaten", code == 0 and got == bom, f"{code} {got[:80]!r}")
        echo = "  - a) intended: 200 ACK\n  - b) unintended\n"
        code, out, _ = cli("--task", "QA-9", "--answer", "Q1", "--reading", "a", "--words", echo, *wh("Q1"))
        got = row_of(QR.load(task), "Q1")["words"]
        check("E7 CLI: the gate text echoed inside the words is kept whole, and it is no choice for the parser",
              code == 0 and got == echo and parse(echo)["choices"] == {}, f"{code} {got[:80]!r}")
        code, out, err = cli("--task", "QA-9", "--answer", "Q1", "--reading", "a", "--words", chr(0xD800) + " lone surrogate", *wh("Q1"))
        check_eq("E7 CLI: a lone surrogate in the words does not lose the answer (escaped, exit 0)", code, 0)
        view, exc = safe(QR.load, task)
        check("E7 ... and the file still reads after it", exc is None and view["skipped"]["broken_lines"] == 0, repr(exc))
        words_file = tmp / "big-words.txt"
        words_file.write_bytes(big.encode("utf-8"))
        (code, out, err), seconds = timed(lambda: cli("--task", "QA-9", "--not-needed", "Q2", "--words-file", str(words_file), *wh("Q2")))
        check("E7 edge 6 CLI: 200 KB of words through --words-file are recorded and kept WHOLE",
              code == 0 and seconds < 10 and row_of(QR.load(task), "Q2")["words"] == big, f"{code} {seconds:.2f}s {err[:200]}")
    finally:
        cleanup(proj)


# ------------------------------------------------------------------------------------------------
# edge 2 - fences and quotes are never tokens
# ------------------------------------------------------------------------------------------------

def test_edge2_fence_and_quote(tmp):
    cases = {
        "a token inside a fence": ("```\nQ1: a\n```", {}),
        "a fence with a language tag": ("```text\nQ1: a\n```\nQ2: b", {"Q2": "b"}),
        "tokens before and after a fence, none inside": ("Q1: a\n```\nQ2: b\n```", {"Q1": "a"}),
        "an indented fence": ("  ```\nQ1: a\n  ```", {}),
        "an unclosed fence hides the rest": ("```\nQ1: a\nQ2: b", {}),
        "two fences, the token between them is read": ("```\nQ1: a\n```\nQ2: b\n```\nQ1: b\n```", {"Q2": "b"}),
        "a fence with CRLF line ends": ("```\r\nQ1: a\r\n```\r\nQ2: b\r\n", {"Q2": "b"}),
        "a one-line fence": ("```Q1: a```", {}),
        "a quote": ("> Q1: a", {}),
        "an indented quote": ("   > Q1: a", {}),
        "a nested quote": ("> > Q1: a", {}),
        "a quote after a list marker": ("- > Q1: a", {}),
        "a quote with no space": (">Q1: a", {}),
        "a quote among tokens": ("> Q1: a\nQ2: b\n> Q2: a", {"Q2": "b"}),
    }
    for name, (text, expected) in cases.items():
        got = parse(text)
        check_eq(f"E2b edge 2: {name}", got["choices"], expected)
        check(f"E2b edge 2: {name} - nothing else is read from it (no unknown id, not needed, conflict)",
              got["unknown_ids"] == [] and got["not_needed"] == [] and got["conflicts"] == [], str(got))
    got = parse("```\nQ1: not needed\n" + CASES[8] + ": manual\nQ7: a\n```\n> Q2: not needed\n> " + CASES[8] + ": automate")
    check_eq("E2b edge 2: `not needed`, case tokens and unknown ids inside a fence or a quote are not read either",
             (got["not_needed"], got["case_tokens"], got["unknown_ids"], got["untokened_questions"]), ([], [], [], ["Q1", "Q2"]))
    check_eq("E2b edge 2: a single-backtick line is not a fence: `Q1: a` is still a choice",
             parse("`Q1: a`")["choices"], {"Q1": "a"})


# ------------------------------------------------------------------------------------------------
# edge 3 - each row has its own hash; a record stores the hash of the row AS SHOWN
# ------------------------------------------------------------------------------------------------

def test_edge3_row_hash(tmp):
    import inspect
    check("E3h edge 3: record() has a REQUIRED shown_hash argument (no default)",
          inspect.signature(QR.record).parameters["shown_hash"].default is inspect.Parameter.empty)
    root = write_story(tmp / "e3h", [q("Q1"), q("Q2")])
    view = QR.load(root)
    h1, h2 = row_of(view, "Q1")["row_hash"], row_of(view, "Q2")["row_hash"]
    check_eq("E3h each row has its OWN hash: 64 hex, different rows differ", (len(h1), len(h2), h1 != h2), (64, 64, True))
    same = QR.load(write_story(tmp / "e3h-same", [q("Q1")]))
    reordered = {"readings": q("Q1")["readings"], "severity": "major", "question": "question Q1?", "id": "Q1"}
    other = QR.load(write_story(tmp / "e3h-order", [reordered]))
    check_eq("E3h the hash is the row's content: the same row in another story, or with its keys in another order, is the same hash",
             (row_of(same, "Q1")["row_hash"], row_of(other, "Q1")["row_hash"]), (h1, h1))

    # the person is shown Q1 (hash h1); the register changes Q1 before the answer is recorded
    write_story(root, [q("Q1", 3), q("Q2")])
    now = row_hash_of(root, "Q1")
    check("E3h the changed row has a different hash today", now != h1)
    written = QR.record(root, "Q1", "answered", "Q1: a", "gate A", "person", h1, reading="a")
    check_eq("E3h record() stores the hash of the row AS SHOWN, not the current one", written["row_hash"], h1)
    row = row_of(QR.load(root), "Q1")
    check_eq("E3h the changed row: status as recorded (answered) PLUS changed_since_answer true; the stored hash is exposed",
             (row["status"], row["changed_since_answer"], row["record_row_hash"], row["row_hash"]), ("answered", True, h1, now))
    written = put(root, "Q2", "answered", "Q2: b", reading="b")
    check_eq("E3h a row shown and not changed: changed_since_answer is False", row_of(QR.load(root), "Q2")["changed_since_answer"], False)
    write_story(root, [q("Q1", 4), q("Q2")])
    v = QR.load(root)
    check_eq("E3h changing ANOTHER row does not flag this one (per-row hash, not one hash for the register)",
             (row_of(v, "Q2")["changed_since_answer"], row_of(v, "Q2")["status"]), (False, "answered"))
    write_story(root, [q("Q1", 4), q("Q2", 3)])
    check_eq("E3h ... and a change to its own row does", row_of(QR.load(root), "Q2")["changed_since_answer"], True)
    fresh = put(root, "Q2", "answered", "Q2: b again", reading="b")
    check_eq("E3h answering again with the hash of the row as shown NOW clears the flag",
             (row_of(QR.load(root), "Q2")["changed_since_answer"], fresh["row_hash"]), (False, row_hash_of(root, "Q2")))

    # a record with no stored hash
    old = write_story(tmp / "e3h-old", [q("Q1"), q("Q2"), q("Q3")], answers=[
        json.dumps({"id": "Q1", "status": "answered", "words": "w", "by": "t", "where": "gate A",
                    "at": "2026-09-30T10:00:00+00:00", "register_hash": "h"})])
    QR.record(old, "Q2", "open", "reopened", "conductor", "person", "")
    v = QR.load(old)
    check_eq("E3h a record written before this change (no row_hash) reads changed_since_answer null",
             row_of(v, "Q1")["changed_since_answer"], None)
    check_eq("E3h a reopen recorded with no hash reads null, and its record carries no row_hash key",
             (row_of(v, "Q2")["changed_since_answer"], "row_hash" in json.loads(
                 (old / "work" / "question-answers.jsonl").read_text(encoding="utf-8").split("\n")[-2])), (None, False))
    check_eq("E3h a question with no record reads False, not null", row_of(v, "Q3")["changed_since_answer"], False)

    # refusals
    clean = write_story(tmp / "e3h-refuse", [q("Q1")])
    good = row_hash_of(clean, "Q1")
    for name, status, shown in (("answered", "answered", ""), ("not_needed", "not_needed", ""),
                                ("with_designer", "with_designer", ""), ("answered", "answered", None),
                                ("a short hash", "answered", "abc"), ("an upper-case hash", "answered", good.upper()),
                                ("a hash with a stray space", "answered", good + " "), ("a reopen with a malformed hash", "open", "xyz")):
        try:
            QR.record(clean, "Q1", status, "w", "gate A", "person", shown)
            problem = None
        except QR.Refused as exc:
            problem = str(exc)
        check(f"E3h refused: {name} with hash {shown!r}: nothing written, the text names the register hash",
              problem is not None and "register hash" in problem and not (clean / "work" / "question-answers.jsonl").exists(),
              str(problem))
    QR.record(clean, "Q1", "open", "reopened without a hash", "conductor", "person", "")
    check("E3h a reopen needs no hash: it is recorded", (clean / "work" / "question-answers.jsonl").exists())


# ------------------------------------------------------------------------------------------------
# edge 4 - where and by are required, closed lists
# ------------------------------------------------------------------------------------------------

def test_edge4_where_by(tmp):
    root = write_story(tmp / "e4wb", [q("Q1")])
    good = row_hash_of(root, "Q1")
    answers = root / "work" / "question-answers.jsonl"
    for label, where, by, needles in (
            ("no where", "", "person", ["--where is missing", "no default", "gate A, gate B"]),
            ("no by", "gate A", "", ["--by is missing", "person, conductor, driver, orchestrator"]),
            ("an unknown where", "gate C", "person", ["where 'gate C' is not a known value", "gate A, gate B"]),
            ("an unknown by", "gate A", "somebody", ["by 'somebody' is not a known value", "person, conductor"]),
            ("neither", None, None, ["--where is missing", "--by is missing"])):
        try:
            QR.record(root, "Q1", "answered", "w", where or "", by or "", good)
            text = ""
        except QR.Refused as exc:
            text = str(exc)
        check(f"E4wb edge 4: {label} is refused naming the valid values, and nothing is written",
              text != "" and all(n in text for n in needles) and not answers.exists(), text)
    for by in QR.vocabulary()["by"]:
        got = QR.record(root, "Q1", "answered", "w", "gate A", by, good)
        check_eq(f"E4wb edge 4: by={by!r} is a valid value and is recorded as given", got["by"], by)
    for where in QR.vocabulary()["where"]:
        got = QR.record(root, "Q1", "answered", "w", where, "person", good)
        check_eq(f"E4wb edge 4: where={where!r} is a valid value and is recorded as given", got["where"], where)


# ------------------------------------------------------------------------------------------------
# edge 5 - case decisions: --keep-manual / --automate
# ------------------------------------------------------------------------------------------------

def test_edge5_case_decisions(tmp):
    full = CASES[8]
    root = write_story(tmp / "e5", [q("Q1")], answers=[rec("Q1"), json.dumps({"kind": "question", **json.loads(rec("Q1", "not_needed"))})])
    check_eq("E5c a record with kind `question` and a record with no kind are both question records: the last wins",
             status_of(QR.load(root), "Q1"), "not_needed")
    first = QR.record_case(root, full, "manual", full + ": manual", "gate A", "person")
    check_eq("E5c a case record is {kind, case, decision, words, where, by, at}",
             (sorted(first), first["kind"], first["case"], first["decision"], first["where"], first["by"]),
             (sorted(["kind", "case", "decision", "words", "where", "by", "at"]), "case", full, "manual", "gate A", "person"))
    view = QR.load(root)
    check_eq("E5c load() returns case_decisions {case id: {decision, words, where, by, at}}",
             view["case_decisions"], {full: {"decision": "manual", "words": full + ": manual", "where": "gate A", "by": "person",
                                             "at": first["at"]}})
    check_eq("E5c a case record is NOT counted under skipped (all four counters stay 0)",
             view["skipped"], {"broken_lines": 0, "non_object_lines": 0, "unknown_id": 0, "invalid": 0, "unreadable_file": 0})
    check_eq("E5c a case record makes no question: the register's questions are as before", [x["id"] for x in view["questions"]], ["Q1"])
    QR.record_case(root, full, "automate", "on my word, automate " + full, "gate B", "driver")
    QR.record_case(root, CASES[5], "manual", "the other one", "conductor", "conductor")
    view = QR.load(root)
    check_eq("E5c the LAST case record per case wins; another case is its own entry",
             ({k: (v["decision"], v["where"], v["by"]) for k, v in view["case_decisions"].items()}),
             {full: ("automate", "gate B", "driver"), CASES[5]: ("manual", "conductor", "conductor")})
    check_eq("E5c still nothing skipped after three case records", sum(view["skipped"].values()), 0)
    raw = write_story(tmp / "e5-raw", [q("Q1")], answers=[
        json.dumps({"kind": "case", "decision": "manual", "words": "w"}), json.dumps({"kind": "case", "case": full, "decision": "maybe"}),
        json.dumps({"kind": "case", "case": 5, "decision": "manual"}), json.dumps({"kind": "weird", "id": "Q1", "status": "answered"}),
        case_rec(full, "manual")])
    v = QR.load(raw)
    check_eq("E5c malformed case records and an unknown kind are counted as invalid (4), the good one is read",
             (v["skipped"]["invalid"], list(v["case_decisions"])), (4, [full]))
    check_eq("E5c a case record does not answer a question of the same name",
             status_of(QR.load(write_story(tmp / "e5-same", [q("Q1")], answers=[case_rec("Q1", "manual")])), "Q1"), "open")

    # the ids the caller gives
    file_before = (root / "work" / "question-answers.jsonl").read_bytes()
    for label, ids, case in (("an id that is not one of the story's", CASES, "TP1-13797_TC_099"),
                             ("a short id (only full ids are recorded)", CASES, "TC_009"),
                             ("any id when the story has NO case ids", [], full), ("a blank id", CASES, "   ")):
        try:
            QR.record_case(root, case, "manual", "w", "gate A", "person", case_ids=ids)
            text = ""
        except QR.Refused as exc:
            text = str(exc)
        check(f"E5c refused: {label} -> nothing written", text != "" and (root / "work" / "question-answers.jsonl").read_bytes() == file_before, text)
    try:
        QR.record_case(root, "TP1-13797_TC_099", "manual", "w", "gate A", "person", case_ids=CASES)
    except QR.Refused as exc:
        check("E5c the refusal names the valid full case ids", CASES[0] in str(exc) and "no case with id" in str(exc), str(exc))
    QR.record_case(root, "ANY_1", "manual", "w", "gate A", "person", case_ids=None)
    check("E5c with no case ids given (None) any non-empty id is accepted", "ANY_1" in QR.load(root)["case_decisions"])
    file_mid = (root / "work" / "question-answers.jsonl").read_bytes()
    for label, kwargs in (("a decision that is not manual/automate", {"decision": "skip"}), ("blank words", {"words": " "}),
                          ("no where", {"where": ""}), ("no by", {"by": ""}), ("a bad hash", {"shown_hash": "nope"})):
        args = {"decision": "manual", "words": "w", "where": "gate A", "by": "person"}
        args.update(kwargs)
        try:
            QR.record_case(root, full, args.pop("decision"), args.pop("words"), args.pop("where"), args.pop("by"), **args)
            text = ""
        except QR.Refused as exc:
            text = str(exc)
        check(f"E5c refused: {label} -> nothing written", text != "" and (root / "work" / "question-answers.jsonl").read_bytes() == file_mid, text)
    stored = QR.record_case(root, CASES[1], "manual", "w", "gate A", "person", shown_hash=HASH)
    check_eq("E5c an optional shown hash is stored as row_hash when given, and absent when not",
             ("row_hash" in stored, stored.get("row_hash"), "row_hash" in first), (True, HASH, False))


def test_edge5_case_cli(tmp):
    proj = temp_project("qa-question-register-case-")
    try:
        use_project(proj)
        task = proj / "qa-factory" / "artifacts" / "QA-9"
        write_story(task, [q("Q1")])
        answers = task / "work" / "question-answers.jsonl"
        full = "TP1-9_TC_009"
        common = ["--where", "gate A", "--by", "person"]
        code, out, err = cli("--task", "QA-9", "--keep-manual", full, "--words", full + ": manual", *common)
        got = json.loads(out) if out else {}
        check_eq("E5c CLI: with no case store and no --case-ids-file any non-empty id is accepted, and the output SAYS the ids were not checked",
                 (code, got.get("recorded", {}).get("decision"), got.get("case_ids_checked_against", "")[:5]), (0, "manual", "none:"))
        check_eq("E5c CLI: the record and the read-back agree", (got["recorded"]["case"], got["case_decision"]["decision"]), (full, "manual"))
        code, out, err = cli("--task", "QA-9", "--automate", full, "--words", "on my word", *common)
        got = json.loads(out)
        check_eq("E5c CLI: --automate is the twin: the last decision wins", (code, got["recorded"]["decision"], got["case_decision"]["decision"]),
                 (0, "automate", "automate"))
        (task / "state").mkdir(parents=True, exist_ok=True)
        (task / "state" / "story-case-links.json").write_text(json.dumps(
            {"links": [{"case_id": "TP1-9_TC_001", "version": "v1"}, {"case_id": full, "version": "v1"}, "junk", {"case_id": 5}]}),
            encoding="utf-8")
        before = answers.read_bytes()
        code, out, err = cli("--task", "QA-9", "--keep-manual", "TP1-9_TC_777", "--words", "w", *common)
        check("E5c CLI: the story's case links are read: an id that is not one of the story's is refused (exit 2), nothing written",
              code == 2 and out == "" and "no case with id" in err and "TP1-9_TC_001" in err and answers.read_bytes() == before, err)
        code, out, err = cli("--task", "QA-9", "--keep-manual", "TC_009", "--words", "w", *common)
        check("E5c CLI: a short case id is refused too (only full ids are recorded)", code == 2 and answers.read_bytes() == before, err)
        code, out, err = cli("--task", "QA-9", "--keep-manual", "TP1-9_TC_001", "--words", "w", *common)
        got = json.loads(out)
        check_eq("E5c CLI: a case id of the story is recorded, and the output names what it was checked against",
                 (code, got["case_ids_checked_against"]), (0, "state/story-case-links.json"))
        ids = tmp / "e5-case-ids.txt"
        ids.write_bytes(("TP1-9_TC_500\r\n\r\n  TP1-9_TC_501  \r\n").encode("utf-8"))
        code, out, err = cli("--task", "QA-9", "--automate", "TP1-9_TC_001", "--words", "w", *common, "--case-ids-file", str(ids))
        check("E5c CLI: --case-ids-file wins over the story's links: TC_001 is not in it, refused", code == 2 and "TP1-9_TC_500" in err, err)
        code, out, err = cli("--task", "QA-9", "--automate", "TP1-9_TC_501", "--words", "w", *common, "--case-ids-file", str(ids))
        check_eq("E5c CLI: an id of the file (trimmed) is recorded", (code, json.loads(out)["case_ids_checked_against"]), (0, "--case-ids-file"))
        empty = tmp / "e5-empty-ids.txt"
        empty.write_bytes(b"\n\n")
        code, out, err = cli("--task", "QA-9", "--automate", "TP1-9_TC_501", "--words", "w", *common, "--case-ids-file", str(empty))
        check("E5c CLI: an EMPTY case ids file refuses every id (it says the story has none), nothing is guessed",
              code == 2 and "no case ids" in err or "none - the story has no case ids" in err, err)
        view = QR.load(task)
        check_eq("E5c CLI: the decisions read back, none of them a skipped line",
                 (sorted(view["case_decisions"]), sum(view["skipped"].values())),
                 (sorted([full, "TP1-9_TC_001", "TP1-9_TC_501"]), 0))
        code, out, err = cli("--task", "QA-9", "--show")
        check("E5c CLI: --show prints case_decisions", code == 0 and full in json.loads(out)["case_decisions"], err)
    finally:
        cleanup(proj)


# ------------------------------------------------------------------------------------------------
# edge 6 - words from a file
# ------------------------------------------------------------------------------------------------

def test_edge6_words_file(tmp):
    proj = temp_project("qa-question-register-wf-")
    try:
        use_project(proj)
        task = proj / "qa-factory" / "artifacts" / "QA-9"
        write_story(task, [q("Q1")])
        answers = task / "work" / "question-answers.jsonl"
        tail = ["--where", "gate A", "--by", "person", "--register-hash", row_hash_of(task, "Q1")]
        text = BOM + "- Q1: a\r\n" + HELLO + " " + E_ACUTE + "\r\n" + "y" * 70000
        target = tmp / "wf-words.txt"
        target.write_bytes(text.encode("utf-8"))
        code, out, err = cli("--task", "QA-9", "--answer", "Q1", "--reading", "a", "--words-file", str(target), *tail)
        check_eq("E6w edge 6: --words-file words (BOM, CRLF, non-ASCII, longer than 32 KB) are stored whole",
                 (code, row_of(QR.load(task), "Q1")["words"] == text), (0, True))
        before = answers.read_bytes()
        bad = tmp / "wf-bad.txt"
        bad.write_bytes(b"Q1: a\xff\xfe broken")
        code, out, err = cli("--task", "QA-9", "--answer", "Q1", "--words-file", str(bad), *tail)
        check("E6w edge 6: a words file that is not UTF-8 is refused, the message says what is expected, nothing written",
              code == 2 and "not UTF-8" in err and answers.read_bytes() == before, err)
        utf16 = tmp / "wf-utf16.txt"
        utf16.write_bytes("Q1: a".encode("utf-16"))
        code, out, err = cli("--task", "QA-9", "--answer", "Q1", "--words-file", str(utf16), *tail)
        check("E6w edge 6: a UTF-16 words file (what a Windows shell redirect writes) is refused, not misread",
              code == 2 and answers.read_bytes() == before, err)
        blank = tmp / "wf-blank.txt"
        blank.write_bytes(b" \r\n\t\r\n")
        code, out, err = cli("--task", "QA-9", "--answer", "Q1", "--words-file", str(blank), *tail)
        check("E6w edge 6: a blank words file is a blank-words refusal", code == 2 and "the words are blank" in err and answers.read_bytes() == before, err)
        code, out, err = cli("--task", "QA-9", "--answer", "Q1", "--words", "w", "--words-file", str(target), *tail)
        check("E6w edge 6: both --words and --words-file -> exit 2", code == 2 and answers.read_bytes() == before, err)
        code, out, err = cli("--task", "QA-9", "--show", "--words-file", str(target))
        check("E6w edge 6: --words-file with --show is meaningless and refused", code == 2 and "--words-file" in err, err)
    finally:
        cleanup(proj)


# ------------------------------------------------------------------------------------------------
# edge 7 - appends are serialised
# ------------------------------------------------------------------------------------------------

WRITER = '''
import sys
sys.path.insert(0, sys.argv[1])
import question_register as QR
root, tag, count, size = sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
for n in range(count):
    QR.record(root, "Q1", "answered", tag + ":" + str(n) + ":" + "z" * size, "gate A", "person", "a" * 64, reading="a")
'''


def test_edge7_lock(tmp):
    root = write_story(tmp / "e7", [q("Q1"), q("Q2")])
    answers = root / "work" / "question-answers.jsonl"
    problems = []

    def writer():
        try:
            QR.record(root, "Q2", "answered", "held back", "gate A", "person", HASH)
        except Exception as exc:  # reported through the check below
            problems.append(repr(exc))

    with QR.answers_lock(root):
        thread = threading.Thread(target=writer)
        thread.start()
        time.sleep(0.5)
        check("E7l edge 7: a second writer WAITS while the lock is held: nothing is written, the writer has not returned",
              thread.is_alive() and not answers.exists(), f"alive={thread.is_alive()} file={answers.exists()}")
        check("E7l ... and a reader is not blocked by the writer lock", len(QR.load(root)["questions"]) == 2)
        try:
            with QR.answers_lock(root, wait=0.2):
                waited = False
        except QR.Refused as exc:
            waited = "another writer" in str(exc)
        check("E7l a writer that cannot get the lock in time says so (Refused) and writes nothing", waited and not answers.exists())
    thread.join(20)
    check("E7l after the lock is released the waiting writer writes its record",
          not thread.is_alive() and not problems and status_of(QR.load(root), "Q2") == "answered", str(problems))

    script = tmp / "e7-writer.py"
    script.write_text(WRITER, encoding="utf-8")
    count, size, procs = 12, 60000, 4
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    running = [subprocess.Popen([sys.executable, "-B", str(script), str(harness.SCRIPTS), str(root), f"w{i}", str(count), str(size)],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env) for i in range(procs)]
    codes = []
    for proc in running:
        _, err = proc.communicate(timeout=300)
        codes.append((proc.returncode, err.decode("utf-8", errors="replace")[-300:] if proc.returncode else ""))
    check_eq("E7l edge 7: four concurrent writer processes all finish cleanly", codes, [(0, "")] * procs)
    lines = [ln for ln in answers.read_bytes().decode("utf-8").split("\n") if ln]
    parsed, broken = [], 0
    for ln in lines:
        try:
            parsed.append(json.loads(ln))
        except ValueError:
            broken += 1
    check_eq("E7l two concurrent writers never interleave a line: every line is one whole JSON record, none broken",
             (broken, len(parsed)), (0, 1 + procs * count))
    mine = [r for r in parsed if str(r.get("words", "")).startswith("w")]
    check("E7l every concurrent record arrived whole (its words end with the full run of z)",
          len(mine) == procs * count and all(r["words"].endswith("z" * size) and len(r["words"]) > size for r in mine))
    per_writer = {}
    for r in mine:
        tag, n, _ = r["words"].split(":", 2)
        per_writer.setdefault(tag, []).append(int(n))
    check_eq("E7l each writer's own records are all there, in its own order",
             {k: v for k, v in sorted(per_writer.items())}, {f"w{i}": list(range(count)) for i in range(procs)})
    check_eq("E7l the file reads back with nothing skipped", sum(QR.load(root)["skipped"].values()), 0)


# ------------------------------------------------------------------------------------------------
# edge 8 - `named`: the id is a word, not a piece of a URL, a path or a file name
# ------------------------------------------------------------------------------------------------

def test_edge8_named(tmp):
    def named_of(name, text, qid):
        pipe = {"gates": {"A": {"decision": "approved", "authorization_source": text}}}
        root = write_story(tmp / ("e8-" + name), [q("Q1"), q("Q3"), q("Q4"), q("Q5")], pipeline=pipe)
        return status_of(QR.load(root), qid)

    not_named = {
        "url": ("see http://x/browse/Q1 for the ticket", "Q1"), "https url": ("https://tracker.example/issue/Q1?x=1", "Q1"),
        "file name": ("the details are in Q3.md", "Q3"), "path": ("docs/Q3/notes.txt and Q3/other", "Q3"),
        "hash sign": ("see #Q4", "Q4"), "path continues": ("Q5/other", "Q5"), "path before": ("x/Q5", "Q5"),
        "dot before": ("a.Q1", "Q1"), "dot after with a digit": ("Q1.5 is the release", "Q1"), "hyphen before": ("R-Q1", "Q1"),
        "hyphen after": ("Q1-x", "Q1"), "underscore": ("Q1_a and Q1a", "Q1"),
        "a longer id": ("Q10 is settled", "Q1"), "an id inside a word": ("aQ1", "Q1"),
    }
    for name, (text, qid) in not_named.items():
        check_eq(f"E8n edge 8: an id inside {name} ({text!r}) is NOT named", named_of(name, text, qid), "open")
    named = {
        "bare": ("Q1", "Q1"), "in brackets": ("(Q1) is settled", "Q1"), "before a comma": ("Q1, Q3 and Q4", "Q3"),
        "bold": ("**Q1** - reading a", "Q1"), "before a colon": ("Q1: a", "Q1"), "list dash and spaces": ("- Q1 - reading (a)", "Q1"),
        "slash-separated ids with spaces": ("Q1 / Q-R14 / R-9 (event-type mismatch)", "Q1"),
        "in quotes": ("\"Q4\" is fine", "Q4"), "in backticks": ("`Q5` is fine", "Q5"), "first word": ("Q3 stays", "Q3"),
        "after a colon": ("answers:Q4", "Q4"),
    }
    for name, (text, qid) in named.items():
        check_eq(f"E8n edge 8: an id standing as a word ({name}: {text!r}) IS named", named_of("p-" + name, text, qid), "named")
    # A backslash right before an id is a boundary, not a word character: a chat client or an editor
    # escapes markdown (`\Q1`), and the person named the question all the same. Built from chr(92), never typed (FR-29).
    bs = chr(92)
    for name, text in (("a markdown escape", bs + "Q1 is settled"), ("an escaped backslash", bs * 2 + "Q1 is settled"),
                       ("after a space and a backslash", "see " + bs + "Q1"), ("a backslash on both sides", bs + "Q1" + bs)):
        check_eq(f"E8n edge 8: a backslash before an id is a boundary ({name}: {text!r}) - the id is found",
                 named_of("bs-" + name, text, "Q1"), "named")
        check_eq(f"E8n edge 8: the line finder reads the same ({name})", QR._line_with(text, "Q1"), text)
    check_eq("E8n edge 8: negative control - a letter before the id is still no boundary (`aQ1`)",
             QR._line_with("aQ1", "Q1"), "")
    check_eq("E8n edge 8: ... nor is a backslash before an id that goes on (`" + bs + "Q10`)",
             QR._line_with(bs + "Q10", "Q1"), "")
    root = write_story(tmp / "e8-mix", [q("Q1"), q("Q3")], answers=[rec("Q3")],
                       pipeline={"gates": {"A": {"authorization_source": "Q1 is fine; also http://x/browse/Q3"}}})
    check_eq("E8n edge 8: with an answers file the question with no record is named, the recorded one is answered",
             (status_of(QR.load(root), "Q1"), status_of(QR.load(root), "Q3")), ("named", "answered"))
    check_eq("E8n the line of the words carries only the real mention", row_of(QR.load(root), "Q1")["line"], "Q1 is fine; also http://x/browse/Q3")


# ------------------------------------------------------------------------------------------------
# the real cmp1 gate A words
# ------------------------------------------------------------------------------------------------

def test_cmp1(tmp):
    questions = [q(f"Q{i}") for i in range(1, 6)]
    got = QR.parse_choices(CMP1_GATE_A, questions, CASES)
    print("cmp1 gate A words ->", json.dumps(got, sort_keys=True))
    check_eq("cmp1 the strict grammar reads NO choice from the person's gate A words", got["choices"], {})
    check_eq("cmp1 ... no `not needed`, no case token, no conflict, no unknown id, no out-of-range letter, nothing unresolved",
             (got["not_needed"], got["case_tokens"], got["conflicts"], got["unknown_ids"], got["out_of_range"], got["unresolved_short_ids"]),
             ([], [], [], [], [], []))
    check_eq("cmp1 ... and all five questions are untokened (they go to the conductor, a role that reads meaning)",
             got["untokened_questions"], ["Q1", "Q2", "Q3", "Q4", "Q5"])
    check("cmp1 the fixture is the words verbatim: 4360 characters, no Cyrillic", len(CMP1_GATE_A) == 4360 and all(ord(c) < 128 for c in CMP1_GATE_A))
    pipe = {"gates": {"A": {"decision": "approved", "authorization_source": CMP1_GATE_A}}}
    view = QR.load(write_story(tmp / "cmp1", questions, pipeline=pipe))
    check_eq("cmp1 the reader: the five questions are `named` (the ids stand in authorization_source), never answered",
             [status_of(view, f"Q{i}") for i in range(1, 6)], ["named"] * 5)
    check_eq("cmp1 the line of the words that carries Q3", row_of(view, "Q3")["line"][:60], "- **Q3 / Q-R7 (UI field for the JSON path filter)** - this i")


# ------------------------------------------------------------------------------------------------
# t-256 O6: `<case id>: accept as blocked` is a whole-line token of the parser
# ------------------------------------------------------------------------------------------------

def test_t256_o6_accept_as_blocked_is_a_whole_line_case_token(tmp):
    got = parse("TC_003: accept as blocked\nTP1-13797_TC_004: accept as blocked.\n- **TC_005**: manual\n")
    check_eq("O6: the register's parser reads the token, a short id resolved, with the id as typed",
             [(t["case"], t["decision"], t["written"]) for t in got["case_tokens"]],
             [("TP1-13797_TC_003", "accept as blocked", "TC_003"), ("TP1-13797_TC_004", "accept as blocked", "TP1-13797_TC_004"),
              ("TP1-13797_TC_005", "manual", "TC_005")])
    for label, words in (("a negation", "TC_003: do not accept as blocked"), ("a second case on the line", "TC_003: accept as blocked; TC_004 runs"),
                         ("the card's old words", "TC_003: accept them as blocked"), ("prose around it", "I think TC_003: accept as blocked")):
        check_eq(f"O6: {label} is no token", parse(words)["case_tokens"], [])
    got = parse("TC_003: accept as blocked\nTC_003: manual")
    check_eq("O6: two different words for one case: a conflict, no token", (got["case_tokens"], [c["values"] for c in got["conflicts"]]),
             ([], [["accept as blocked", "manual"]]))
    check_eq("O6: a register id takes only question tokens - `Q1: accept as blocked` is no case token",
             parse("Q1: accept as blocked")["case_tokens"], [])
    check_eq("O6: an unknown short id is `unresolved`, not guessed", parse("TC_099: accept as blocked")["unresolved_short_ids"],
             [{"id": "TC_099", "candidates": []}])
    check_eq("the register's recorded case decisions are still only manual | automate (record_case writes what a card applies)",
             json.loads((QR.VOCAB_PATH).read_text(encoding="utf-8"))["case_decisions"], ["manual", "automate"])


# ------------------------------------------------------------------------------------------------
# t-256 O4: the S4-exit half of `--raise` - keyed by (case, Then), idempotent
# ------------------------------------------------------------------------------------------------

def test_t256_o4_raise_for_case_is_keyed_by_case_and_then(tmp):
    import contract as C
    fixtures = Path(__file__).resolve().parent / "fixtures" / "oracle-provenance"
    readiness = (fixtures / "requirements-readiness.json").read_text(encoding="utf-8")
    tc015 = (fixtures / "TP1-15045_TC_015.md").read_text(encoding="utf-8").replace("updated: 2026-10-01", "updated: 2026-10-02")
    spec = {"then": 4, "question": "Which status code must PUT return for a body that breaks two checks at once?",
            "source_says": [{"quote": "returns the same results and error codes as before", "where": "register R-19"}],
            "severity": "major", "owner_role": "po_ba", "before": {"value": "unknown", "where": "the base revision is not in the hunk"},
            "now": {"value": "400", "where": "observed by the S5 run"}}
    oracles = [{"then": 1, "source": "ac", "ref": "R-13"}, {"then": 2, "source": "ac", "ref": "R-13"},
               {"then": 3, "source": "ac", "ref": "R-13"}, {"then": 4, "source": "unknown", "ref": "raise"}]
    qthens = [{"question": "raise", "then": 4, "readings": {"a": "HTTP 400, the behaviour now", "b": ""}, "not_needed": ""}]

    def case_with(oracles=oracles, qthens=qthens, raise_questions=(spec,)):
        extra = f"then_oracles: {json.dumps(oracles)}\nquestion_thens: {json.dumps(qthens)}\n"
        if raise_questions:
            extra += f"raise_questions: {json.dumps(list(raise_questions))}\n"
        return tc015.replace("plan_row: TS-15\n", extra + "plan_row: TS-15\n", 1)

    story = tmp / "t256-raise"
    (story / "work").mkdir(parents=True)
    ready = story / "work" / "requirements-readiness.json"
    ready.write_text(readiness, encoding="utf-8")
    text = case_with()
    done = QR.raise_for_case(story, text, "TP1-15045_TC_015")
    check_eq("O4: one question raised for the Then that said `raise`", done["raised"],
             [{"case": "TP1-15045_TC_015", "then": 4, "question": "Q8"}])
    check_eq("...and nothing was refused", done["problems"], [])
    new = done["text"]
    check_eq("the then_oracles line now names the new id", C.then_oracles_from_text(new)[0][3], {"then": 4, "source": "unknown", "ref": "Q8"})
    check_eq("the question_thens entry that said `raise` names it too", C.question_thens_from_text(new)[0][0]["question"], "Q8")
    check_eq("the raise_questions line is gone", C.front_line(new, "raise_questions"), None)
    check_eq("every other line of the case is byte for byte as it was",
             [ln for ln in new.splitlines() if not ln.startswith(("then_oracles:", "question_thens:"))],
             [ln for ln in text.splitlines() if not ln.startswith(("then_oracles:", "question_thens:", "raise_questions:"))])
    rows = json.loads(ready.read_text(encoding="utf-8"))["open_questions"]
    check_eq("the readiness file holds it after the old ones, keyed by (case, Then)",
             [(r["id"], r.get("raised_for")) for r in rows], [("Q1", None), ("Q7", None), ("Q8", {"case": "TP1-15045_TC_015", "then": 4})])
    check_eq("it passes the shape check and shows before/now", (C.question_errors(rows[2]), rows[2]["before"]["value"]), ([], "unknown"))
    # idempotent: the case rewrite was lost (a crash between the raise and the write); the SAME text raises nothing twice
    again = QR.raise_for_case(story, text, "TP1-15045_TC_015")
    check_eq("O4: the same (case, Then) again returns the question it raised", again["raised"],
             [{"case": "TP1-15045_TC_015", "then": 4, "question": "Q8"}])
    check_eq("...and the readiness file is untouched: no duplicate", len(json.loads(ready.read_text(encoding="utf-8"))["open_questions"]), 3)
    check_eq("the rewritten case has nothing left to raise (text None, nothing raised)",
             {k: v for k, v in QR.raise_for_case(story, new, "TP1-15045_TC_015").items() if k != "problems"},
             {"text": None, "raised": []})
    other = QR.raise_for_case(story, text, "TP1-15045_TC_016")
    check_eq("another case with the same Then number is another question (Q9)", [r["question"] for r in other["raised"]], ["Q9"])
    # what it refuses: the Then stays `raise` and one sentence says why
    no_entry = QR.raise_for_case(story, case_with(raise_questions=()), "TP1-15045_TC_017")
    check_eq("a `raise` with no raise_questions entry: nothing raised, no text, one problem", (no_entry["raised"], no_entry["text"], len(no_entry["problems"])),
             ([], None, 1))
    check_in("...naming the Then", "Then 4 is `unknown` with the ref `raise` but the case has no `raise_questions` entry for it", no_entry["problems"][0])
    bad = QR.raise_for_case(story, case_with(raise_questions=({k: v for k, v in spec.items() if k != "now"},)), "TP1-15045_TC_018")
    check_eq("an entry the register would refuse: nothing raised", (bad["raised"], bad["text"]), ([], None))
    check_in("...with the register's own sentence", "needs `now` as an object", bad["problems"][0])
    check_eq("...and the readiness file holds the four questions it should (Q1, Q7, Q8, Q9)",
             [r["id"] for r in json.loads(ready.read_text(encoding="utf-8"))["open_questions"]], ["Q1", "Q7", "Q8", "Q9"])
    # a Then that already has a settled oracle is never asked about
    settled = case_with(oracles=oracles[:3] + [{"then": 4, "source": "ac", "ref": "R-13"}], qthens=[])
    check_eq("no `raise` ref: nothing to do", QR.raise_for_case(story, settled, "TP1-15045_TC_019")["raised"], [])
    # set_front_line: the one line only, line endings kept, a body line never touched
    crlf = "---\r\nid: x\r\nraise_questions: [1]\r\nthen_oracles: [2]\r\n---\r\nraise_questions: [body]\r\n"
    check_eq("set_front_line removes one front-matter line and keeps the CRLF of the others",
             C.set_front_line(crlf, "raise_questions", None), "---\r\nid: x\r\nthen_oracles: [2]\r\n---\r\nraise_questions: [body]\r\n")
    check_eq("...and rewrites one in place", C.set_front_line(crlf, "then_oracles", "[3]").splitlines()[3], "then_oracles: [3]")
    check_eq("...removing the LAST front-matter line leaves no blank line", C.set_front_line("---\nid: x\nraise_questions: [1]\n---\nbody\n", "raise_questions", None),
             "---\nid: x\n---\nbody\n")
    check_eq("a text with no such line is returned unchanged", C.set_front_line("---\nid: x\n---\n", "nothing", None), "---\nid: x\n---\n")


def test_g1_13_question_row_keys_never_meet_and_the_readiness_writer_keeps_its_bytes(tmp):
    """G1-13: `_question_row` is the one row step of `_raise` and of the S3 claim projector. A claim key and a case key with the same
    numbers never meet; `taken` hands out contiguous ids; `_write_readiness` writes the bytes `_raise` always wrote."""
    question = {key: f"v-{key}" for key in QR.QUESTION_KEYS}
    rows = [{"id": "Q1", "raised_for": {"case": "R-28", "then": 1}}, {"id": "Q7"}]
    row, earlier = QR._question_row(rows, question, {"claim": "R-28", "origin": "S3-grounding"})
    check_eq("a claim key is not the case key of the same numbers: a new row, Q8, the keys in order",
             (earlier, row["id"], list(row)), (None, "Q8", ["id", *QR.QUESTION_KEYS, "raised_for"]))
    again, found = QR._question_row(rows + [row], question, {"claim": "R-28", "origin": "S3-grounding"})
    check_eq("the same claim key finds its row and makes no second one", (again, found is row), (None, True))
    case_row, case_found = QR._question_row(rows, question, {"case": "R-28", "then": 1})
    check_eq("the case key still finds the case row", (case_row, case_found), (None, rows[0]))
    check_eq("`taken` makes a batch contiguous without rescanning its own rows",
             [QR._question_row(rows, question, {"claim": f"R-{n}", "origin": "x"}, taken=top)[0]["id"] for n, top in ((1, 0), (2, 8), (3, 9))],
             ["Q8", "Q9", "Q10"])
    path = tmp / "g1-13-readiness.json"
    data = {"verdict": "ready", "open_questions": [{"id": "Q1", "text": "é"}]}
    QR._write_readiness(path, data)
    check_eq("_write_readiness: the file is the indent-2 JSON with ensure_ascii False and a final newline, no staged file left",
             (path.read_bytes().decode("utf-8").replace("\r\n", "\n"), path.with_name(path.name + ".tmp").exists()),
             (json.dumps(data, ensure_ascii=False, indent=2) + "\n", False))


# ------------------------------------------------------------------------------------------------
# HF2-7 part 1 (GW1-21): the store keeps what a person said and says it with ONE vocabulary
# ------------------------------------------------------------------------------------------------

OWN_WORDS = "".join(chr(c) for c in (0x43e, 0x441, 0x442, 0x430, 0x432, 0x44c, 0x20, 0x43e, 0x442, 0x43a, 0x440, 0x44b, 0x442, 0x44b,
                                      0x43c, 0x20, 0x434, 0x43e, 0x20, 0x43e, 0x442, 0x447, 0x451, 0x442, 0x430))   # "leave it open until the report"
WORDS_1 = "Q1: b\nQ2: a\nQ3: until the report\nQ4: a\nQ5: a\n"
WORDS_2 = "Q1 b, Q3 " + OWN_WORDS
SPEC_ROOT = Path(__file__).resolve().parents[2]


def f12586_rows(q4_severity=None) -> list:
    """The F-12586 register: Q1 major, Q2 minor, Q3 blocker, Q4 with no severity (or `q4_severity`), Q5 blocker; two readings each."""
    def row(qid, severity):
        out = q(qid)
        out.pop("severity")
        out.update({"owner_role": "qa"})
        if severity:
            out["severity"] = severity
        return out
    return [row("Q1", "major"), row("Q2", "minor"), row("Q3", "blocker"), row("Q4", q4_severity), row("Q5", "blocker")]


def f12586(q4_severity=None, verdict="blocked") -> dict:
    return {"verdict": verdict, "goal_summary": "Check the filter of the webhook payload end to end, by its paths",
            "aspects": {"functional": {"status": "ready"}}, "register": {"total": 3, "by_source": {"story": 2, "ac": 1}},
            "open_questions": f12586_rows(q4_severity)}


def f12586_story(path: Path, q4_severity=None, answers=None) -> Path:
    return write_story(path, readiness_raw=json.dumps(f12586(q4_severity)), answers=answers)


def test_hf2_7_p1_vocabulary_and_parser(tmp):
    vocab = QR.vocabulary()
    check("K1 hf2-7: deferred_to_report is in statuses and in recorded_statuses; blocking is a stop reason",
          "deferred_to_report" in vocab["statuses"] and "deferred_to_report" in vocab["recorded_statuses"]
          and "blocking" in vocab["stop_reasons"], str(vocab["statuses"]))
    # P1 pinned `S4 stop` as absent "until P5a adds it with the S4 code"; P5a (t-108, accepted) added it to `where` and `where_words`
    check("K1 hf2-7: `S4 stop` is in where and in where_words (P5a, t-108)",
          "S4 stop" in vocab["where"] and bool(vocab["where_words"].get("S4 stop")), str(vocab["where"]))
    check_eq("K1 hf2-7: every value of `where` has its words", [w for w in vocab["where"] if not vocab["where_words"].get(w)], [])
    check_eq("K12 where_words: S2 stop, gate A (the pinned form), an unknown value and a value that is no text",
             [QR.where_words("S2 stop"), QR.where_words("gate A"), QR.where_words("zzz"), QR.where_words(None), QR.where_words("note")],
             ["when the requirements were checked", "at gate A", "earlier", "earlier", "earlier"])
    rows = f12586_rows()
    got = QR.parse_choices(WORDS_1, rows, [])
    check_eq("K2 hf2-7: words 1 -> four choices, Q3 deferred, and Q3 is neither a choice nor untokened",
             (got["choices"], got["deferred"], "Q3" in got["untokened_questions"], got["unknown_ids"]),
             ({"Q1": "b", "Q2": "a", "Q4": "a", "Q5": "a"}, ["Q3"], False, []))
    fenced = QR.parse_choices("```\nQ3: until the report\n```\n", rows, [])
    check_eq("K2 hf2-7: the token inside a code block is said (fenced), not read", (fenced["deferred"], fenced["fenced"]),
             ([], ["Q3: until the report"]))
    quoted = QR.parse_choices("> Q3: until the report\n", rows, [])
    check_eq("K2 hf2-7: a quoted token is not read", (quoted["deferred"], "Q3" in quoted["untokened_questions"]), ([], True))
    check_eq("K2 hf2-7: `Q50: until the report` is an unknown id", QR.parse_choices("Q50: until the report", rows, [])["unknown_ids"], ["Q50"])
    check_eq("K2 hf2-7: a trailing full stop and a list dash keep the token whole", QR.parse_choices("- Q3: until the report.", rows, [])["deferred"], ["Q3"])
    check_eq("K2 hf2-7: prose after the words is no token (`until the report, please`)", QR.parse_choices("Q3: until the report, please", rows, [])["deferred"], [])
    check_eq("K2 hf2-7: two different answers for Q3 write neither (a conflict, still untokened)",
             (QR.parse_choices("Q3: a\nQ3: until the report", rows, [])["conflicts"][0]["id"],
              QR.parse_choices("Q3: a\nQ3: until the report", rows, [])["deferred"]), ("Q3", []))
    crlf = QR.parse_choices(BOM + WORDS_1.replace("\n", "\r\n"), rows, [])
    check_eq("K2 battery: CRLF and a BOM read the same five tokens", (crlf["choices"], crlf["deferred"]), (got["choices"], got["deferred"]))
    for label, text in (("a full-width colon", f"Q1{FULL_COLON}a"), ("a Cyrillic a", f"Q1: {CYR_A}"), ("a lower-case id", "q1: a"),
                        ("nothing", ""), ("spaces only", "   \n \t \n"), ("a colon with no value", "Q1:")):
        read = QR.parse_choices(text, rows, [])
        check_eq(f"K2 battery: {label} is no token", (read["choices"], read["not_needed"], read["deferred"]), ({}, [], []))
    many = QR.parse_choices("\n".join(f"Q{n}: a" for n in range(1, 61)), [q(f"Q{n}") for n in range(1, 61)], [])
    check_eq("K2 battery: 60 lines are all read (no limit)", len(many["choices"]), 60)


def test_hf2_7_p1_record_answers(tmp):
    root = f12586_story(tmp / "k3")
    answers = root / "work" / "question-answers.jsonl"
    got = QR.record_answers(root, WORDS_1, "S2 stop", "person")
    stored = [json.loads(x) for x in answers.read_text(encoding="utf-8").splitlines()]
    check_eq("K3 hf2-7: words 1 -> four answers recorded, Q3 deferred, all tokens, nothing unread",
             (got["recorded"], got["deferred"], got["all_tokens"], got["unread"], got["unknown_ids"], got["fenced"]),
             (["Q1: b", "Q2: a", "Q4: a", "Q5: a"], ["Q3"], True, [], [], []))
    check_eq("K3 hf2-7: five records in the file; Q3 is `deferred_to_report` with no reading; each keeps the words whole",
             ([(r["id"], r["status"], r.get("reading", "")) for r in stored], {r["words"] for r in stored}, {r["where"] for r in stored}),
             ([("Q1", "answered", "b"), ("Q2", "answered", "a"), ("Q4", "answered", "a"), ("Q5", "answered", "a"),
               ("Q3", "deferred_to_report", "")], {WORDS_1}, {"S2 stop"}))
    view = QR.load(root)
    check_eq("K4 hf2-7: load reads Q3 back as deferred_to_report", status_of(view, "Q3"), "deferred_to_report")
    again = QR.record_answers(root, WORDS_1, "S2 stop", "person")
    check_eq("K3 hf2-7: the same words again write nothing (H6b), and are still all tokens",
             (len(answers.read_text(encoding="utf-8").splitlines()), again["recorded"], again["deferred"], again["all_tokens"]), (5, [], [], True))
    root2 = f12586_story(tmp / "k3b")
    two = QR.record_answers(root2, WORDS_2, "S2 stop", "person")
    check_eq("K3 hf2-7: words 2 (no token on a line of its own) write nothing and are not all tokens",
             (two["recorded"], two["deferred"], two["all_tokens"], (root2 / "work" / "question-answers.jsonl").exists()), ([], [], False, False))
    for label, text in (("empty", ""), ("spaces", "  \n  "), ("a lone colon", "Q1:")):
        r3 = QR.record_answers(root2, text, "S2 stop", "person")
        check_eq(f"K3 hf2-7: {label} words write nothing and are not all tokens (C14)",
                 (r3["recorded"], r3["all_tokens"], (root2 / "work" / "question-answers.jsonl").exists()), ([], False, False))
    mixed = QR.record_answers(root2, "Q1: a\nplease also look at the logs\n", "S2 stop", "person")
    check_eq("K3 hf2-7: a token with prose on another line is recorded, but not all tokens (the role reads the rest)",
             (mixed["recorded"], mixed["all_tokens"]), (["Q1: a"], False))
    unknown = QR.record_answers(root2, "Q50: a\nQ2: b", "S2 stop", "person")
    check_eq("H4 hf2-7: an id not in the register is an unknown id, nothing is recorded for it; the other token is",
             (unknown["unknown_ids"], unknown["recorded"], unknown["all_tokens"]), (["Q50"], ["Q2: b"], False))
    conflict = QR.record_answers(f12586_story(tmp / "h5"), "Q1: a\nQ1: b\nQ2: a", "S2 stop", "person")
    check_eq("H5 hf2-7: two different answers for one id write neither and are said", (conflict["recorded"], conflict["all_tokens"],
             [u for u in conflict["unread"] if u.startswith("Q1")]), (["Q2: a"], False, ["Q1 (two different answers: a, b)"]))
    beyond = QR.record_answers(f12586_story(tmp / "range"), "Q1: z", "S2 stop", "person")
    check_eq("H4 hf2-7: a letter beyond the readings is said, not recorded", (beyond["recorded"], beyond["unread"]),
             ([], ["Q1 (the letter z is beyond its 2 readings)"]))
    fenced = QR.record_answers(f12586_story(tmp / "fence"), "```\nQ1: a\n```\n", "S2 stop", "person")
    check_eq("H25 hf2-7: a token in a code block is `fenced`, nothing recorded, not all tokens",
             (fenced["recorded"], fenced["fenced"], fenced["all_tokens"]), ([], ["Q1: a"], False))
    shown = QR.record_answers(f12586_story(tmp / "bad-hash"), "Q1: a", "S2 stop", "person", shown={"Q1": "not-a-hash"})
    check_eq("H18 hf2-7: a refusal of one record is a line in unread (the question stays open), not an exception",
             (shown["recorded"], len(shown["unread"]), "sha256" in shown["unread"][0]), ([], 1, True))
    root3 = write_story(tmp / "c13", [q("Q7")], answers=[rec("Q7", "with_designer")])
    check_eq("C13 hf2-7: a token for a question that is with the designer is recorded (the exact id is the person's word)",
             QR.record_answers(root3, "Q7: a", "S2 stop", "person")["recorded"], ["Q7: a"])


def test_hf2_7_p1_record_rules(tmp):
    root = f12586_story(tmp / "k4b")
    answers = root / "work" / "question-answers.jsonl"
    put(root, "Q5", "answered", "Q5: a", reading="a")
    before = answers.read_bytes()
    try:
        put(root, "Q5", "answered", "Q5: b", reading="b")
        refused = ""
    except QR.Refused as exc:
        refused = str(exc)
    check("K4b hf2-7: a DIFFERENT answer on a settled question is refused with the door (reopen, words by file) and the reason",
          "Q5 is already settled (reading a, at gate A" in refused and "--reopen Q5 --words-file <file>" in refused
          and "the plan rows that followed the first answer are reworked" in refused, refused)
    check("K4b hf2-7: ...and nothing was written", answers.read_bytes() == before)
    try:
        put(root, "Q5", "not_needed", "Q5: not needed")
        other = ""
    except QR.Refused as exc:
        other = str(exc)
    check("K4b hf2-7: `not needed` over a letter is a different answer too", "already settled" in other, other)
    put(root, "Q5", "open", "back to open", hash_from="")
    put(root, "Q5", "answered", "Q5: b", reading="b")
    check_eq("K4b hf2-7: after --reopen (status open) the new answer is written", row_of(QR.load(root), "Q5")["reading"], "b")
    count = len(answers.read_text(encoding="utf-8").splitlines())
    put(root, "Q5", "answered", "Q5: b again, other words", hash_from="c" * 64, reading="b")
    check_eq("K4b hf2-7: the SAME answer with another hash and other words is appended (H6b; the old pins stay)",
             len(answers.read_text(encoding="utf-8").splitlines()), count + 1)
    put(root, "Q3", "deferred_to_report", "later", reading="")
    put(root, "Q3", "answered", "Q3: a", reading="a")
    check_eq("K4b hf2-7: an answer over deferred_to_report is written (H6c: a deferred question is not settled)", row_of(QR.load(root), "Q3")["reading"], "a")
    try:
        put(root, "Q3", "deferred_to_report", "later", reading="")
        late = ""
    except QR.Refused as exc:
        late = str(exc)
    check("K4b hf2-7: `until the report` over a settled answer is a different answer: refused", "already settled" in late, late)
    # the row moved after the answer: the answer was given on other bytes, so the question is asked again and answers freely (H6d)
    root2 = write_story(tmp / "h6d", [q("Q1")], answers=[rec("Q1", "answered", reading="a")])
    check_eq("H6d hf2-7: the record carries a hash that is not the row's -> changed_since_answer", row_of(QR.load(root2), "Q1")["changed_since_answer"], True)
    put(root2, "Q1", "answered", "Q1: b", reading="b")
    check_eq("H6d hf2-7: a new answer on a changed row is written without --reopen", row_of(QR.load(root2), "Q1")["reading"], "b")
    row = dict(q("Q6"), before={"value": "unknown", "where": "x"}, now={"value": "403", "where": "y"})
    root3 = write_story(tmp / "bvn", [row])
    put(root3, "Q6", "answered", "Q6: b", reading="b")
    put(root3, "Q6", "answered", "Q6: a", reading="a")
    check_eq("H6d hf2-7: an answer `b` while the before value is missing does not settle: another answer is written",
             row_of(QR.load(root3), "Q6")["reading"], "a")
    try:
        QR.record(root, "Q1", "deferred_to_report", "later", "gate A", "person", row_hash_of(root, "Q1"), reading="a")
        letter = ""
    except QR.Refused as exc:
        letter = str(exc)
    check("K4 hf2-7: a reading with `until the report` is refused; without a reading it is written (above)", "reading letter goes only with an answer" in letter, letter)


def test_hf2_7_p1_predicates(tmp):
    def mk(status="open", severity="blocker", **extra):
        out = {"id": "Q", "status": status, "reading": "", "changed_since_answer": False}
        if severity is not None:
            out["severity"] = severity
        out.update(extra)
        return out
    table = [
        ("Q3 open", mk(), (False, True, True, None)),
        ("Q3 named", mk("named"), (False, True, True, None)),
        ("Q3 deferred", mk("deferred_to_report"), (False, False, False, None)),
        ("Q3 deferred + changed", mk("deferred_to_report", changed_since_answer=True), (False, True, True, None)),
        ("Q5 answered a", mk("answered", reading="a"), (True, False, False, "a")),
        ("Q5 answered a + changed", mk("answered", reading="a", changed_since_answer=True), (False, True, True, None)),
        ("Q5 answered a, hash not stored (None)", mk("answered", reading="a", changed_since_answer=None), (True, False, False, "a")),
        ("Q6 answered b, before unknown", mk("answered", reading="b", before={"value": "unknown"}), (False, True, True, None)),
        ("Q6 answered b, before empty", mk("answered", reading="b", before={"value": ""}), (False, True, True, None)),
        ("Q6 answered b, before known", mk("answered", reading="b", before={"value": "400"}), (True, False, False, "b")),
        ("Q2 not_needed", mk("not_needed"), (True, False, False, "not_needed")),
        ("answered with no letter", mk("answered"), (True, False, False, None)),
        ("with_designer", mk("with_designer"), (False, False, False, None)),
        ("an unknown status", mk("invented"), (False, True, True, None)),
        ("no status at all", {"id": "Q", "severity": "blocker"}, (False, True, True, None)),
    ]
    for label, question, want in table:
        got = (QR.settled(question), QR.is_open(question), QR.open_blocker(question), QR.answer_key(question))
        check_eq(f"K9 hf2-7: {label} -> settled/is_open/open_blocker/answer_key", got, want)
    for label, severity in (("no severity (Q4)", None), ("`Blocker`", "Blocker"), ("`critical`", "critical"), ("a list", ["major"])):
        check(f"K9 hf2-7: an open question with {label} is a blocker (the error goes toward asking)", QR.open_blocker(mk(severity=severity)))
    check("K9 hf2-7: an open question marked major or minor is not a blocker",
          not QR.open_blocker(mk(severity="major")) and not QR.open_blocker(mk(severity="minor")))
    check_eq("K9 hf2-7: a row that is no object: not settled, open, a blocker", (QR.settled(None), QR.is_open("Q1"), QR.open_blocker(7)), (False, True, True))
    # K9b: a publish reads rows that are not on disk; the hash is the data's, and load gets the same answer through _merge
    root = f12586_story(tmp / "k9b")
    QR.record_answers(root, WORDS_1, "S2 stop", "person")
    data = f12586_rows()
    same = QR.statuses_for(root, data)
    check_eq("K9b hf2-7: unchanged data rows read as load reads them", same, QR.load(root)["questions"])
    data[4] = dict(data[4], question="Q5 with other words?")
    moved = QR.statuses_for(root, data)
    check_eq("K9b hf2-7: Q5 with another text in the DATA is changed_since_answer (the hash is the data's, not the disk's)",
             (moved[4]["changed_since_answer"], moved[4]["status"], QR.settled(moved[4]), QR.open_blocker(moved[4])), (True, "answered", False, True))
    f12586_story(tmp / "k9b-disk")
    (tmp / "k9b-disk" / "work" / "question-answers.jsonl").write_bytes((root / "work" / "question-answers.jsonl").read_bytes())
    (tmp / "k9b-disk" / "work" / "requirements-readiness.json").write_text(json.dumps({"open_questions": data}), encoding="utf-8")
    check_eq("K9b hf2-7: ...and load on a disk register holding those rows says the same (one _merge)",
             QR.load(tmp / "k9b-disk")["questions"], moved)
    odd = QR.statuses_for(root, ["x", {"question": "no id?"}])
    check_eq("K9b hf2-7: a row that is no object gives None, a row with no id has no record and is open", (odd[0], odd[1]["status"]), (None, "open"))
    nothing = QR.statuses_for(tmp / "no-such-story", data)
    check("H1 hf2-7: with no answers file every row is open", all(x["status"] == "open" for x in nothing))
    unreadable = write_story(tmp / "h2-dir", f12586_rows())
    (unreadable / "work" / "question-answers.jsonl").mkdir()
    check("H2 hf2-7: an answers file that cannot be read (a folder): every row open, no exception",
          all(x["status"] == "open" for x in QR.statuses_for(unreadable, f12586_rows())))


def test_hf2_7_p1_brief_and_drift(tmp):
    root = write_story(tmp / "k5", f12586_rows() + [q("Q6")])    # Q6 is the question nobody answers: it stays open
    check_eq("K5 hf2-7: no answers file -> no answers, not unreadable (H1)", QR.answers_for_brief(root), {"answers": [], "unreadable": False})
    QR.record_answers(root, WORDS_1 + "Q60: a\n", "S2 stop", "person")
    brief = QR.answers_for_brief(root)
    check_eq("K5 hf2-7: the settled and the deferred are listed, in register order, nothing open",
             [(a["id"], a["status"], a["reading"], a["reading_text"]) for a in brief["answers"]],
             [("Q1", "answered", "b", "reading 1"), ("Q2", "answered", "a", "reading 0"), ("Q3", "deferred_to_report", "", ""),
              ("Q4", "answered", "a", "reading 0"), ("Q5", "answered", "a", "reading 0")])
    check_eq("K5 hf2-7: an entry carries id, question, status, reading, reading_text, where, at, words (whole)",
             sorted(brief["answers"][0]), sorted(["id", "question", "status", "reading", "reading_text", "where", "at", "words"]))
    check_eq("K5 hf2-7: the words are the whole text", brief["answers"][0]["words"], WORDS_1 + "Q60: a\n")
    check_eq("K5 hf2-7: Q6 is open (nobody answered it) and has no entry; Q60 is no register id and has none either",
             [a["id"] for a in brief["answers"] if a["id"] in ("Q6", "Q60")], [])
    sick = f12586_story(tmp / "k5-broken")
    good = rec("Q1", "answered", reading="a", row_hash=row_hash_of(sick, "Q1"))   # the hash the row has today: the answer holds
    (sick / "work" / "question-answers.jsonl").write_text(good + "\n{ not json", encoding="utf-8")
    check_eq("K5 hf2-7: one broken line -> unreadable, the good record is kept (H2)",
             (QR.answers_for_brief(sick)["unreadable"], [a["id"] for a in QR.answers_for_brief(sick)["answers"]]), (True, ["Q1"]))
    applied = f12586_story(tmp / "k5-applied")
    (applied / "work" / "question-answers.jsonl").write_text(
        rec("Q1", "answered", reading="a", row_hash=row_hash_of(applied, "Q1")) + "\n"
        + json.dumps({"kind": "answers_applied", "id": "Q1", "at": "2026-10-26T10:00:00+00:00"}), encoding="utf-8")
    check_eq("K5 hf2-7: an `answers_applied` line is no breakage (N7): unreadable False",
             QR.answers_for_brief(applied)["unreadable"], False)
    folder = f12586_story(tmp / "k5-dir")
    (folder / "work" / "question-answers.jsonl").mkdir()
    check_eq("K5 hf2-7: an answers file that is a folder -> unreadable and skipped.unreadable_file == 1",
             (QR.answers_for_brief(folder)["unreadable"], QR.load(folder)["skipped"]["unreadable_file"]), (True, 1))
    changed = f12586_story(tmp / "k5-changed", answers=[rec("Q1", "answered", reading="a")])
    check_eq("K5 hf2-7: an answer given on other bytes (the row changed) is asked again, so it is not listed", QR.answers_for_brief(changed)["answers"], [])
    # K6: an answered question stays in the register
    drift_root = f12586_story(tmp / "k6")
    QR.record_answers(drift_root, WORDS_1, "S2 stop", "person")
    check_eq("K6 hf2-7: every row present -> no drift", QR.readiness_drift(drift_root), [])
    kept = [r for r in f12586_rows() if r["id"] != "Q5"]
    (drift_root / "work" / "requirements-readiness.json").write_text(json.dumps({"open_questions": kept}), encoding="utf-8")
    check_eq("K6 hf2-7: Q5 answered a but gone from open_questions -> ONE problem, in the T6 words",
             QR.readiness_drift(drift_root),
             ["Q5 has an answer recorded at S2 stop (a) but is missing from open_questions: an answered question stays in the register with "
              "its id. Expected: restore the row as it was; the factory reads its status from the answers file."])
    kept = [r for r in f12586_rows() if r["id"] not in ("Q3",)]
    (drift_root / "work" / "requirements-readiness.json").write_text(json.dumps({"open_questions": kept}), encoding="utf-8")
    check("K6 hf2-7: a deferred question gone from the register is named with `until the report`",
          any(p.startswith("Q3 has an answer recorded at S2 stop (until the report)") for p in QR.readiness_drift(drift_root)))
    (drift_root / "work" / "requirements-readiness.json").write_text("{ not json", encoding="utf-8")
    check_eq("K6 hf2-7: a register that cannot be read -> [] (its own finding)", QR.readiness_drift(drift_root), [])
    check_eq("K6 hf2-7: no register file at all -> []", QR.readiness_drift(tmp / "nowhere"), [])
    check_eq("K6 hf2-7: an empty answers file or none -> []", QR.readiness_drift(f12586_story(tmp / "k6-none")), [])


def test_hf2_7_p1_cli_defer(tmp):
    proj = temp_project("qa-question-register-")
    try:
        use_project(proj)
        task = proj / "qa-factory" / "artifacts" / "QA-9"
        write_story(task, f12586_rows())
        shown = json.loads(cli("--task", "QA-9", "--show")[1])
        digest = next(x["row_hash"] for x in shown["questions"] if x["id"] == "Q3")
        words = proj / "words.txt"
        words.write_bytes((BOM + "Q3: until the report\r\nI will come back to it").encode("utf-8"))
        code, out, err = cli("--task", "QA-9", "--defer", "Q3", "--words-file", str(words), "--where", "S2 stop", "--by", "person",
                             "--register-hash", digest)
        written = json.loads(out)["recorded"] if code == 0 else {}
        check_eq("K7 hf2-7: --defer writes a deferred_to_report record; the words are read by person_words (BOM off, CRLF kept)",
                 (code, written.get("status"), written.get("words"), written.get("reading")),
                 (0, "deferred_to_report", "Q3: until the report\r\nI will come back to it", None))
        check_eq("K7 hf2-7: ...and --show reads it back", next(x["status"] for x in json.loads(cli("--task", "QA-9", "--show")[1])["questions"] if x["id"] == "Q3"),
                 "deferred_to_report")
        empty = proj / "empty.txt"
        empty.write_bytes(b"")
        code, out, err = cli("--task", "QA-9", "--defer", "Q3", "--words-file", str(empty), "--where", "S2 stop", "--by", "person", "--register-hash", digest)
        check("K7 hf2-7: an empty words file is person_words' refusal (named option, nothing recorded)", code == 2 and "--words-file" in err and "is empty" in err, err)
        code, out, err = cli("--task", "QA-9", "--defer", "Q3", "--words", "w", "--words-file", str(words), "--where", "S2 stop", "--by", "person",
                             "--register-hash", digest)
        check("K7 hf2-7: both --words and --words-file are refused", code == 2 and "exactly one" in err, err)
        code, out, err = cli("--task", "QA-9", "--defer", "Q3", "--words-file", str(words), "--where", "S2 stop", "--by", "person")
        check("K7 hf2-7: --defer without the register hash is the register's refusal", code == 2 and "register hash is missing" in err, err)
        code, out, err = cli("--task", "QA-9", "--defer", "Q3", "--answer", "Q1", "--words", "w")
        check("K7 hf2-7: two operations are refused", code == 2 and "exactly one operation" in err and "--defer" in err, err)
        h1 = next(x["row_hash"] for x in shown["questions"] if x["id"] == "Q1")
        base = ["--where", "gate A", "--by", "person"]
        code, out, err = cli("--task", "QA-9", "--answer", "Q1", "--reading", "a", "--words", "Q1: a", *base, "--register-hash", h1)
        code2, out2, err2 = cli("--task", "QA-9", "--answer", "Q1", "--reading", "b", "--words", "Q1: b", *base, "--register-hash", h1)
        check("H6 hf2-7: the CLI refuses a different answer on a settled question and prints the reopen door with the words by file",
              code == 0 and code2 == 2 and "already settled" in err2 and "--reopen Q1 --words-file <file>" in err2, err2)
        code, out, err = cli("--task", "QA-9", "--reopen", "Q3", "--words", "asked now", *base)
        check_eq("K8 hf2-7: --reopen puts a deferred question back to open",
                 (code, next(x["status"] for x in json.loads(cli("--task", "QA-9", "--show")[1])["questions"] if x["id"] == "Q3")), (0, "open"))
    finally:
        cleanup(proj)


def test_hf2_7_p1_state_exit_row(tmp):
    walk = (SPEC_ROOT / "design" / "state-exits.md").read_text(encoding="utf-8")
    line = next((x for x in walk.splitlines() if x.startswith("| `deferred_to_report`")), "")
    check("K8 hf2-7: design/state-exits.md has a row for deferred_to_report whose exit is `question_register.py ... --reopen <id>`",
          "question_register.py --task <T> --reopen <id>" in line, line[:200])


def test_hf2_7_p1_readiness_rules(tmp):
    import check_witness as CW
    import human_text
    root = f12586_story(tmp / "k10")
    blocked, ready = f12586(verdict="blocked"), f12586(verdict="ready")
    t12b = ("open blocker questions (Q3, Q4, Q5) or blocked aspects with verdict 'ready' - contradiction. "
            "Expected: verdict 'blocked' while a blocker question is still open")
    check_eq("K10 hf2-7: before any answer, `ready` is T12b and `blocked` passes",
             (CW.readiness_rules(ready, root), CW.readiness_rules(blocked, root)), ([t12b], []))
    QR.record_answers(root, WORDS_1, "S2 stop", "person")
    t12a = ("verdict 'blocked' with no open blocker question and no blocked aspect - contradiction: Q3, Q4, Q5 are answered, not needed or "
            "kept open by the person. Expected: verdict 'ready', or a blocked aspect named")
    check_eq("K10 hf2-7: after words 1 (Q3 deferred, Q4 and Q5 answered) `blocked` is T12a and `ready` passes",
             (CW.readiness_rules(blocked, root), CW.readiness_rules(ready, root)), ([t12a], []))
    check_eq("K10 hf2-7: a blocked ASPECT keeps `blocked` legitimate and makes `ready` wrong, answers or not",
             (CW.readiness_rules(dict(blocked, aspects={"a": {"status": "blocked"}}), root),
              CW.readiness_rules(dict(ready, aspects={"a": {"status": "blocked"}}), root)),
             ([], ["open blocker questions (none) or blocked aspects with verdict 'ready' - contradiction. Expected: verdict 'blocked' "
                   "while a blocker question is still open"]))
    moved = dict(ready, open_questions=[dict(r, question="Q5 changed?") if r["id"] == "Q5" else r for r in ready["open_questions"]])
    check_eq("K10b hf2-7: Q5's text changed since its answer -> Q5 is an open blocker again: `ready` is T12b (Q5), `blocked` passes",
             (CW.readiness_rules(moved, root), CW.readiness_rules(dict(moved, verdict="blocked"), root)),
             (["open blocker questions (Q5) or blocked aspects with verdict 'ready' - contradiction. Expected: verdict 'blocked' while a "
               "blocker question is still open"], []))
    full = CW.readiness_check(blocked, root)
    check("K10c hf2-7: readiness_check on F-12586 -> the FORM error of Q4 (no severity) plus the consistency error",
          any(e.startswith("open_questions[3]: needs question, severity") for e in full["errors"]) and t12a in full["errors"]
          and full["not_checked"] == [], str(full))
    sev_root = f12586_story(tmp / "k10c-sev", q4_severity="minor")
    QR.record_answers(sev_root, WORDS_1, "S2 stop", "person")
    only = CW.readiness_check(f12586(q4_severity="minor"), sev_root)
    check_eq("K10c hf2-7: on F-12586-sev only the consistency error remains (T12a names Q3 and Q5)",
             only["errors"], ["verdict 'blocked' with no open blocker question and no blocked aspect - contradiction: Q3, Q5 are answered, "
                              "not needed or kept open by the person. Expected: verdict 'ready', or a blocked aspect named"])
    # main derives the root from the artifact path: work/ -> its parent
    script = str(harness.SCRIPTS / "check_witness.py")
    for verdict, code in (("blocked", 1), ("ready", 0)):
        artifact = sev_root / "work" / "requirements-readiness.json"
        artifact.write_text(json.dumps(f12586(q4_severity="minor", verdict=verdict)), encoding="utf-8")
        run = subprocess.run([sys.executable, "-B", script, str(artifact)], capture_output=True, text=True, encoding="utf-8", cwd=str(tmp))
        check(f"K10c hf2-7: check_witness main on the artifact: verdict {verdict} -> exit {code}",
              run.returncode == code and (("contradiction" in run.stdout) == (code == 1)), run.stdout + run.stderr)
    check_eq("K10 hf2-7: RULES[...] with no root errs only on what needs no answers file (H32)",
             [e for e in CW.RULES["requirements-readiness.json"](f12586(q4_severity="minor")) if "contradiction" in e], [])
    # FR-6: the phrases a person reads from where_words, inside the sentences that carry them (T4, T5, the card suffix)
    sentences = []
    for where in QR.vocabulary()["where"]:
        words = QR.where_words(where)
        sentences += [f"Q3 is kept open until the report, on your word {words}; it is not asked again here.",
                      f"Q3 (kept open on your word {words}; the factory did not guess an answer)",
                      f"Q3 (answered {words})"]
    broke = [(s, [x["rule"] for x in human_text.problems(s, kind="report")]) for s in sentences]
    check_eq("FR-6 hf2-7: human_text.problems(kind=report) finds nothing in the sentences the where_words phrases go into",
             [b for b in broke if b[1]], [])


def test_gw1_47_stray_line_starts_with_an_open_register_id(tmp):
    """GW1-47: a line outside fences and quotes that STARTS with the id of an open question (any case, any separator) and is no token is
    read by `question_lines_unread` (over `_stray_lines`, AR-13), the id in the REGISTER's spelling; a real token is not touched."""
    fence = "`" * 3
    rows = [{"id": "Q3"}, {"id": "Q1"}]
    table = [
        ("lower-case id with colon", "q3: x", [("Q3", "q3: x")]),
        ("dash separator", "Q3 - x", [("Q3", "Q3 - x")]),
        ("space separator", "Q3 x", [("Q3", "Q3 x")]),
        ("dot separator", "Q3. x", [("Q3", "Q3. x")]),
        ("no-break space separator", "Q3\xa0x", [("Q3", "Q3 x")]),
        ("leading BOM", "﻿Q3 - x", [("Q3", "Q3 - x")]),
        ("leading BOM then a real token (`x` is a letter): the token rule wins", "﻿Q3: x", []),
        ("leading BOM of a later line", "Q1: a\n﻿q3 x", [("Q3", "q3 x")]),
        ("BOM only", "﻿", []),
        ("closing paren", "Q3) x", [("Q3", "Q3) x")]),
        ("id alone on the line", "Q3", [("Q3", "Q3")]),
        ("list marker and emphasis", "- **q3** is unclear", [("Q3", "q3** is unclear")]),
        ("prose after the id is still stray", "Q3 is unclear", [("Q3", "Q3 is unclear")]),
        ("a real token is no stray line", "Q3: a", []),
        ("a real token with a note is stray as before", "Q3: a (see the ticket)", [("Q3", "Q3: a (see the ticket)")]),
        ("control: another id", "Q30: x", []),
        ("control: a word that only starts like an id", "Quote: x", []),
        ("control: the id in the middle of a line", "I think Q3 is unclear", []),
        ("control: in a fence", f"{fence}\nQ3 - x\n{fence}", []),
        ("control: in a quote", "> Q3 - x", []),
        ("control: in a list quote", "- > Q3 - x", []),
        ("empty text", "", []),
        ("only whitespace", "  \n\t\n", []),
    ]
    for label, words, want in table:
        got = [(x["id"], x["line"]) for x in QR.question_lines_unread(words, rows)]
        check_eq(f"GW1-47 {label}", got, want)
    twin = [{"id": "q3"}, {"id": "Q3"}]
    check_eq("GW1-47 two ids that differ in case: the exact spelling wins, one row",
             [x["id"] for x in QR.question_lines_unread("Q3 x", twin)], ["Q3"])
    check_eq("GW1-47 two ids that differ in case: no exact one -> the first by the register's order, one row",
             [x["id"] for x in QR.question_lines_unread("ab x", [{"id": "aB"}, {"id": "Ab"}])], ["aB"])
    check_eq("GW1-47 an empty register sees nothing, no exception", QR.question_lines_unread("Q3 x", []), [])
    check_eq("GW1-47 a settled question is not counted", QR.question_lines_unread("Q3 x", [{"id": "Q3", "status": "with_designer"}]), [])
    long = "Q3 " + "w" * 400
    shown = QR.question_lines_unread(long, rows)[0]["line"]
    check_eq("GW1-47 a very long line is cut with the cut shown, as before", (len(shown), shown.endswith("...")), (QR.MAX_NOTICE_LINE, True))
    check_eq("GW1-47 the gate view tells the same line (one reader)",
             QR.stray_line("Q3", "q3 - x"), "q3 - x")


def test_x2_6_role_questions(tmp):
    """X2-6 (t-1765): a question a role of S1-S4 raises goes into THE register (`open_questions`), idempotent by (dispatch, entry); the
    driver's `--answer ... --by driver --where "stage ran"` closes it from disk; the S4 `--raise --case-file --then` form is untouched."""
    import person_owned
    proj = temp_project("qa-question-register-x26-")
    try:
        use_project(proj)
        task = proj / "qa-factory" / "artifacts" / "QA-9"
        write_story(task, [q("Q1")])
        forms = task / "work" / "handoffs"
        forms.mkdir(parents=True)

        def entry(text="Is the import limit 100 or 1000?", **over):
            base = {"question": text, "read": ["work/requirements-register.md#R-7"], "recommendation": "plan on 100",
                    "options": [{"reading": "100", "if_chosen": "the plan checks 100"}, {"reading": "1000", "if_chosen": "the plan checks 1000"}],
                    "severity": "blocker", "owner_role": "po_ba", "why_person": "requirement_intent"}
            base.update(over)
            return base

        def form(name, *entries):
            """The role's handoff form with its questions[] (flow maps, one per line: the YAML subset of handoff.py)."""
            lines = ["header: {role: qa-requirements-tester, stage: S2, window_or_scope: S2, verdict: concerns}", "questions:"]
            for e in entries:
                lines.append("  - " + json.dumps(e, ensure_ascii=False))
            path = forms / (name + ".yaml")
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            return path

        classes = person_owned.class_ids()
        check("X2-6 the classes come from person-owned.json `classes[].id`", "requirement_intent" in classes and "access" in classes)
        # the form check: one named edge each
        errors = lambda spec, **kw: QR.role_question_errors(spec, **dict({"stage": "S2", "asked_by": "qa-requirements-tester"}, **kw))
        check_eq("X2-6 a good entry has no problem", errors(entry()), [])
        check_eq("X2-6 why_person null is legal (the conductor settles it)", errors(entry(why_person=None)), [])
        check_in("X2-6 why_person `opinion` -> refused with the classes", "requirement_intent", " ".join(errors(entry(why_person="opinion"))))
        check_in("X2-6 one option -> refused", "options must be 2-5", " ".join(errors(entry(options=[{"reading": "a", "if_chosen": "b"}]))))
        check_eq("X2-6 five options pass, six do not", (errors(entry(options=[{"reading": str(i), "if_chosen": "x"} for i in range(5)])) == [],
                                                       bool(errors(entry(options=[{"reading": str(i), "if_chosen": "x"} for i in range(6)])))), (True, True))
        check_in("X2-6 an empty question -> refused", "question is empty", " ".join(errors(entry(question="  "))))
        check_in("X2-6 a stage outside S1-S4 -> refused", "stage 'S5'", " ".join(errors(entry(), stage="S5")))
        check_in("X2-6 a name that is no role file -> refused", "not a role of the package", " ".join(errors(entry(), asked_by="nobody")))
        check_in("X2-6 an option without if_chosen -> refused", "options[0].if_chosen", " ".join(errors(entry(options=[{"reading": "a"}, {"reading": "b", "if_chosen": "x"}]))))
        check_eq("X2-6 an empty `read` is legal in the form", errors(entry(read=[])), [])

        # raising
        path = form("S2-qa-requirements-tester-1", entry())
        code, out, err = cli("--task", "QA-9", "--raise", "--stage", "S2", "--asked-by", "qa-requirements-tester", "--from-handoff", str(path))
        check_eq("X2-6 --raise --from-handoff exits 0", (code, err), (0, ""))
        view = QR.load(task)
        row = row_of(view, "Q2")
        check_eq("X2-6 one new row after the old one, with asked_by, stage, read, raised_from",
                 (len(view["questions"]), row["asked_by"], row["stage"], row["read"], row["raised_from"], row["why_person"]),
                 (2, "qa-requirements-tester", "S2", ["work/requirements-register.md#R-7"],
                  {"dispatch": "S2-qa-requirements-tester-1", "row": "questions[0]"}, "requirement_intent"))
        check_eq("X2-6 the readings are the options, lettered by position", [r["reading"] for r in row["readings"]], ["100", "1000"])
        check("X2-6 the new row is open and blocking (severity is the role's, not `major`/`minor`)", QR.is_open(row) and QR.open_blocker(row))
        before = snapshot(proj)
        code, out, err = cli("--task", "QA-9", "--raise", "--stage", "S2", "--asked-by", "qa-requirements-tester", "--from-handoff", str(path))
        check_eq("X2-6 the same form again writes nothing (FR-7)", (code, snapshot(proj) == before, len(json.loads(out)["already"])), (0, True, 1))
        form("S2-qa-requirements-tester-1", entry("Is the import limit 50?"))
        before = snapshot(proj)
        code, out, err = cli("--task", "QA-9", "--raise", "--stage", "S2", "--asked-by", "qa-requirements-tester", "--from-handoff", str(path))
        check_eq("X2-6 the same (dispatch, entry) with another text -> refused, nothing written", (code, snapshot(proj) == before), (2, True))
        check_in("X2-6 ... naming both texts", "import limit 100", err)
        check_in("X2-6 ... and the new one", "import limit 50", err)
        bad = form("S2-bad", entry(), entry(why_person="opinion"))
        before = snapshot(proj)
        code, out, err = cli("--task", "QA-9", "--raise", "--stage", "S2", "--asked-by", "qa-requirements-tester", "--from-handoff", str(bad))
        check_eq("X2-6 one bad entry refuses the whole form, nothing written", (code, snapshot(proj) == before), (2, True))
        check_in("X2-6 ... naming the entry", "questions[1]", err)
        empty = form("S2-none")
        before = snapshot(proj)
        code, out, err = cli("--task", "QA-9", "--raise", "--stage", "S2", "--asked-by", "qa-requirements-tester", "--from-handoff", str(empty))
        check_eq("X2-6 a form with no questions raises nothing (declared empty outcome)", (code, json.loads(out)["raised"], snapshot(proj) == before), (0, [], True))
        # a read-less entry is raised with read_missing; two roles asking the same thing are two rows (dedup is the conductor's)
        none_read = form("S3-qa-test-strategist-1", entry("Same words?", read=[]))
        code, out, err = cli("--task", "QA-9", "--raise", "--stage", "S3", "--asked-by", "qa-test-strategist", "--from-handoff", str(none_read))
        row = row_of(QR.load(task), json.loads(out)["raised"][0]["id"])
        check_eq("X2-6 an empty `read` -> the row is raised with read_missing", (code, row.get("read_missing"), row["read"]), (0, True, []))
        twin = form("S3-qa-case-critic-1", entry("Same words?", read=[]))
        code, out, err = cli("--task", "QA-9", "--raise", "--stage", "S3", "--asked-by", "qa-case-critic", "--from-handoff", str(twin))
        check_eq("X2-6 the same question from two roles -> two rows", len([x for x in QR.load(task)["questions"] if x.get("question") == "Same words?"]), 2)
        # S1 is a stage a role may ask in
        s1 = form("S1-qa-scout-1", entry("Which source is meant?"))
        code, out, err = cli("--task", "QA-9", "--raise", "--stage", "S1", "--asked-by", "qa-scout", "--from-handoff", str(s1))
        check_eq("X2-6 a raise from S1 is accepted", code, 0)

        # the driver's form: the path the role sees, relative to the story folder, with the process cwd somewhere else (g10)
        elsewhere = Path(tempfile.mkdtemp(prefix="qa-question-register-g10-cwd-"))
        try:
            rel_env = dict(os.environ, CLAUDE_PROJECT_DIR=str(proj), PYTHONDONTWRITEBYTECODE="1")

            def rel_run(handoff):
                return subprocess.run([sys.executable, "-B", str(harness.SCRIPTS / "question_register.py"), "--task", "QA-9", "--raise",
                                       "--stage", "S2", "--asked-by", "qa-case-critic", "--from-handoff", handoff],
                                      capture_output=True, encoding="utf-8", errors="replace", cwd=str(elsewhere), env=rel_env, timeout=120)
            form("S2-qa-case-critic-g10", entry("Is the export limit 10 or 20?"))
            proc = rel_run("work/handoffs/S2-qa-case-critic-g10.yaml")
            check_eq("g10 a task-relative --from-handoff, cwd not the story folder -> exit 0, one question raised",
                     (proc.returncode, len(json.loads(proc.stdout)["raised"]) if proc.returncode == 0 else proc.stderr), (0, 1))
            proc = rel_run("work/handoffs/S2-qa-case-critic-9.yaml")
            check_eq("g10 the same relative path with no such form -> exit 2", proc.returncode, 2)
            check_in("g10 ... the refusal quotes the path as given", "'work/handoffs/S2-qa-case-critic-9.yaml' could not be read", proc.stderr)
            proc = rel_run("  ")
            check_eq("g10 a blank --from-handoff is refused, never read as the cwd", proc.returncode, 2)
        finally:
            shutil.rmtree(elsewhere, ignore_errors=True)

        # the driver closes from disk: --by driver, the source in the words; the closed row is not open
        qid = "Q2"
        shown = row_hash_of(task, qid)
        code, out, err = cli("--task", "QA-9", "--answer", qid, "--reading", "a", "--by", "driver", "--where", "stage ran", "--register-hash", shown,
                             "--words", "work/requirements-register.md#R-7: the limit is 100")
        closed = row_of(QR.load(task), qid)
        check_eq("X2-6 the driver's answer is recorded (by driver, where `stage ran`)", (code, closed["status"], closed["where"], closed["reading"]), (0, "answered", "stage ran", "a"))
        check("X2-6 ... the row is no longer open and its words name the source", not QR.is_open(closed) and "requirements-register.md#R-7" in closed["words"])
        check_eq("X2-6 `stage ran` reads as `while the stage ran` to a person", QR.where_words("stage ran"), "while the stage ran")
        raw = [json.loads(line) for line in (task / "work" / "question-answers.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
        check_eq("X2-6 ... the answers file holds by=driver", raw[-1]["by"], "driver")

        # t-1815 F2: the questions come from the CRITIC's form; its contract template is what role_question_errors accepts; a classless question
        # is the conductor's and is never listed to a person at gate A
        import handoff
        import gate_brief
        contracts = Path(QR.__file__).resolve().parent.parent / "handoffs"
        for name in ("s2-stage-critic-to-tester", "s3-stage-critic-to-strategist", "s4-case-critic-to-designer"):
            template = handoff.parse((contracts / f"{name}.yaml").read_text(encoding="utf-8")).data["questions"][0]
            check_eq(f"F2 {name}: the template's severity words are blocker|major|minor, `read` is a list, every option has if_chosen",
                     (template["severity"], isinstance(template["read"], list), all("if_chosen" in o for o in template["options"])),
                     ("<blocker|major|minor>", True, True))
            filled = dict(template, why_person=None, severity="blocker", question="Is it 100?", owner_role="po_ba")
            check_eq(f"F2 {name}: the template, filled in, is raised without a refusal", QR.role_question_errors(
                filled, stage=name[:2].upper(), asked_by="qa-case-critic"), [])
        check_eq("F2: `major` and `minor` do not block, `blocker` does (the words the template offers)",
                 [QR.open_blocker({"severity": s}) for s in ("blocker", "major", "minor")], [True, False, False])
        critic_form = form("S2-qa-case-critic-1", entry("Is the cap per file or per run?", why_person=None, severity="major"),
                           entry("Who owns the import limit?"))
        code, out, err = cli("--task", "QA-9", "--raise", "--stage", "S2", "--asked-by", "qa-case-critic", "--from-handoff", str(critic_form))
        raised = json.loads(out)["raised"]
        check_eq("F2: the critic's form raises its two questions, asked_by the critic", (code, [r["asked_by"] for r in raised]), (0, ["qa-case-critic"] * 2))
        classless, classed = raised[0], raised[1]
        view = QR.load(task)
        check_eq("F2: the classless row is driver-owned, the classed one is not", (QR.driver_owned(row_of(view, classless["id"])),
                                                                                   QR.driver_owned(row_of(view, classed["id"]))), (True, False))
        listed = [str(x.get("id")) for x in gate_brief.unanswered_questions(task, {})]
        check_eq("F2: gate A lists the classed role question and NOT the classless one", (classed["id"] in listed, classless["id"] in listed), (True, False))
        check("F2: ...while the classless row stays in the register, open, for the conductor", QR.is_open(row_of(QR.load(task), classless["id"])))
        check_eq("F2: a readiness question (no asked_by) is never driver-owned; a non-object is not either", (QR.driver_owned(q("Q9")), QR.driver_owned("x")),
                 (False, False))
        empty_critic = form("S2-qa-case-critic-2")
        before = snapshot(proj)
        code, out, err = cli("--task", "QA-9", "--raise", "--stage", "S2", "--asked-by", "qa-case-critic", "--from-handoff", str(empty_critic))
        check_eq("F2: a critic form with an empty questions[] raises nothing and is no error", (code, json.loads(out)["raised"], snapshot(proj) == before), (0, [], True))
        no_text = form("S2-qa-case-critic-3", entry(question="", why_person="requirement_intent"))
        code, out, err = cli("--task", "QA-9", "--raise", "--stage", "S2", "--asked-by", "qa-case-critic", "--from-handoff", str(no_text))
        check_eq("F2: a question with a class and no text -> shape refusal naming the entry", (code, "questions[0]" in err and "question is empty" in err), (2, True))

        # regression: the S4 form is refused with the new flags, and the old form's own refusal text is unchanged
        code, out, err = cli("--task", "QA-9", "--raise", "--case-file", "x.md", "--then", "1", "--question-file", "q.json", "--stage", "S4")
        check_eq("X2-6 --raise --case-file with --stage is refused", code, 2)
        code, out, err = cli("--task", "QA-9", "--raise")
        check_eq("X2-6 the old `--raise` alone keeps its refusal text byte for byte",
                 err, "question_register.py: refused.\n- --raise needs --case-file, --then, --question-file\n")
        code, out, err = cli("--task", "QA-9", "--stage", "S2", "--show")
        check_eq("X2-6 --stage without --raise is refused", code, 2)
    finally:
        cleanup(proj)


def test_placeholder_question_row_dropped(tmp):
    """t-1936 F1 (B-11): a `questions[]` row whose `question` is still the contract's placeholder is the sample, not a question: it is
    not raised and not refused; a real row beside it keeps its own form index in `raised_from`."""
    proj = temp_project("qa-question-register-b11-")
    try:
        use_project(proj)
        task = proj / "qa-factory" / "artifacts" / "QA-9"
        write_story(task, [q("Q1")])
        forms = task / "work" / "handoffs"
        forms.mkdir(parents=True)
        sample = {"question": "<the question, in plain words>", "read": ["<path#anchor the critic read before asking>"],
                  "recommendation": "<what the work goes on with meanwhile>", "options": [], "severity": "<blocker|major|minor>"}
        real = {"question": "Is the import limit 100 or 1000?", "read": ["work/requirements-register.md#R-7"], "recommendation": "plan on 100",
                "options": [{"reading": "100", "if_chosen": "the plan checks 100"}, {"reading": "1000", "if_chosen": "the plan checks 1000"}],
                "severity": "blocker", "owner_role": "po_ba", "why_person": "requirement_intent"}

        def form(name, *entries):
            lines = ["header: {role: qa-case-critic, stage: S2, window_or_scope: S2, verdict: ok}", "questions:"]
            lines += ["  - " + json.dumps(e, ensure_ascii=False) for e in entries]
            path = forms / (name + ".yaml")
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            return path

        only_sample = form("S2-qa-case-critic-1", sample)
        before = (task / "work" / "requirements-readiness.json").read_bytes()
        result = QR.raise_from_handoff(task, only_sample, stage="S2", asked_by="qa-case-critic")
        check_eq("F1 a form holding only the template row raises nothing and is no refusal",
                 (result["raised"], result["already"], (task / "work" / "requirements-readiness.json").read_bytes() == before), ([], [], True))
        both = form("S2-qa-case-critic-2", sample, real)
        result = QR.raise_from_handoff(task, both, stage="S2", asked_by="qa-case-critic")
        check_eq("F1 beside a real row the template row is dropped and the real one keeps its form index",
                 (len(result["raised"]), result["raised"][0]["raised_from"]), (1, {"dispatch": "S2-qa-case-critic-2", "row": "questions[1]"}))
    finally:
        cleanup(proj)


def test_answers_lock_busy_names_the_holder(tmp=None):
    """TR4-2 part B: the answers lock is the package's one file lock. Busy = the old head + the holder clause (the file is in
    the story's tracked work folder: none recorded); broken = Refused with the LockBroken sentence and the writable door,
    never the busy head."""
    import tempfile
    with tempfile.TemporaryDirectory(prefix="qa-answers-lock-") as td:
        root = Path(td) / "story"
        with QR.answers_lock(root):
            try:
                with QR.answers_lock(root, wait=0.1):
                    raise AssertionError("a second writer got the answers lock")
            except QR.Refused as exc:
                text = str(exc)
        assert text.startswith("- another writer has held "), text
        assert "nothing was written. Expected: try again in a moment; no holder recorded - released when that process ends: wait and repeat" in text, text
        assert (root / "work" / QR.LOCK_NAME).read_bytes() == b"0", "no holder is written into the story's work folder"
        folder_root = Path(td) / "other"
        (folder_root / "work" / QR.LOCK_NAME).mkdir(parents=True)
        try:
            with QR.answers_lock(folder_root, wait=0.1):
                raise AssertionError("a folder at the lock path was taken as a lock")
        except QR.Refused as exc:
            text = str(exc)
        assert text.startswith("- ") and "cannot be locked" in text and text.endswith("Expected: the file must be writable"), text
        assert "has held" not in text and "try again in a moment" not in text and "holder" not in text, text


# ------------------------------------------------------------------------------------------------
# FV1-9 N1: a question asked once - `repeat`, `reword`, `note`, `dependants`, the brief list, the S4 exit, the form item
# ------------------------------------------------------------------------------------------------

def fv_row(qid, text=None, n=2, **extra):
    """A register row that passes `contract.question_errors` (quotes, readings with `from` and `if_chosen`)."""
    row = {"id": qid, "question": text or f"What does {qid} ask about the limit?", "source_says": [{"quote": "the limit is 100", "where": "R-1"}],
           "readings": [{"reading": f"reading {i}", "from": "code", "if_chosen": "x"} for i in range(n)],
           "severity": "major", "owner_role": "po_ba"}
    row.update(extra)
    return row


def fv_story(tmp, name, rows=None, answers=None):
    return write_story(tmp / name, rows if rows is not None else [fv_row("Q7"), fv_row("Q16")], answers=answers)


def declare(root, qid="Q16", target="Q7", why="both ask the limit", by="driver", declared_by="qa-case-designer", stage="S4"):
    return QR.declare_repeat(root, qid, target, why, by=by, declared_by=declared_by, stage=stage)


def refusal(fn, *args, **kwargs):
    """The text of the `Refused` the call raises, or None when it returned."""
    try:
        fn(*args, **kwargs)
    except QR.Refused as exc:
        return str(exc)
    return None


def state_shown(root, **hashes):
    """The driver's saved last question stop: what it showed, with the hash of each row as shown."""
    (root / "state").mkdir(parents=True, exist_ok=True)
    (root / "state" / "driver-state.json").write_text(
        json.dumps({"question_stop": {"stage": "S4", "at": "2026-11-14T10:00:00+00:00", "shown": hashes}}), encoding="utf-8")


def show_now(root, *ids):
    state_shown(root, **{i: row_hash_of(root, i) for i in ids})


def write_plan(root, rows, approved=False):
    (root / "work").mkdir(parents=True, exist_ok=True)
    (root / "work" / "test-plan.json").write_text(json.dumps({"rows": rows}), encoding="utf-8")
    if approved:
        (root / "pipeline.json").write_text(json.dumps({"gates": {"A": {"gate": "A", "status": "approved", "decision": "approved"}}}), encoding="utf-8")


def write_case(root, name, **front):
    folder = root / "work" / "test-cases"
    folder.mkdir(parents=True, exist_ok=True)
    lines = [f"id: {name}"] + [f"{key}: {value}" for key, value in front.items()]
    (folder / f"{name}.md").write_text("---\n" + "\n".join(lines) + "\n---\n## Then\n1. x\n", encoding="utf-8")
    return folder / f"{name}.md"


def repeat_line(qid, same_as, target_hash, row_hash, **extra):
    """A raw `repeat` record as the answers file holds it (a test may leave a key out with None)."""
    base = {"kind": "question", "id": qid, "status": "repeat", "words": "same", "by": "driver", "where": "stage ran", "at": "2026-11-14T10:00:00+00:00",
            "row_hash": row_hash, "same_as": same_as, "declared_by": "qa-case-designer", "target_hash": target_hash, "stage": "S4"}
    base.update(extra)
    return json.dumps({k: v for k, v in base.items() if v is not None})


def test_fv19_repeat_hidden_while_target_resolves(tmp):
    root = fv_story(tmp, "fv19-hidden")
    rec = declare(root)
    view = QR.load(root)
    q16, q7 = row_of(view, "Q16"), row_of(view, "Q7")
    check_eq("fv19_repeat_hidden_while_target_resolves: Q16 is a repeat of Q7: not open, Q7 lists it, the record is the retro's",
             (q16["status"], QR.is_open(q16), QR.hidden_repeat(q16), q7["repeated_by"], QR.is_open(q7), rec["texts"]["same_as_question"], rec["declared_by"]),
             ("repeat", False, True, ["Q16"], True, q7["question"], "qa-case-designer"))
    check_eq("fv19_repeat_hidden_while_target_resolves: a hidden repeat is no blocker and is counted nowhere as open",
             (QR.open_blocker(q16), [x["id"] for x in view["questions"] if QR.is_open(x)]), (False, ["Q7"]))
    put(root, "Q7", "answered", "a", hash_from=HASH, reading="a")      # answered on other bytes than the row's: the answer is stale
    stale = QR.load(root)
    check_eq("fv19_repeat_hidden_while_target_resolves (m8): the target's ANSWER went stale - Q7 is asked again, Q16 stays hidden behind it",
             (row_of(stale, "Q7")["changed_since_answer"], QR.is_open(row_of(stale, "Q7")), QR.hidden_repeat(row_of(stale, "Q16"))), (True, True, True))
    moved = write_story(tmp / "fv19-hidden-moved", [fv_row("Q7"), fv_row("Q16")])
    declare(moved)
    (moved / "work" / "requirements-readiness.json").write_text(
        json.dumps({"open_questions": [fv_row("Q7", "What does Q7 ask in other words?"), fv_row("Q16")]}), encoding="utf-8")
    after = QR.load(moved)
    check_eq("fv19_repeat_hidden_while_target_resolves (m3): the target's ROW changed - Q16 is shown again, `target_changed`, Q7 lists nobody",
             (QR.is_open(row_of(after, "Q16")), row_of(after, "Q16")["repeat_problem"], "repeated_by" in row_of(after, "Q7")), (True, "target_changed", False))
    chain = fv_story(tmp, "fv19-chain", [fv_row("Q7"), fv_row("Q15"), fv_row("Q16")])
    declare(chain, "Q15", "Q7")
    declare(chain, "Q16", "Q15")
    both = QR.load(chain)
    check_eq("fv19_repeat_hidden_while_target_resolves: a repeat of a repeat resolves to the end; the last target lists both",
             (row_of(both, "Q7")["repeated_by"], QR.is_open(row_of(both, "Q16")), QR.is_open(row_of(both, "Q15"))), (["Q15", "Q16"], False, False))
    published = QR.statuses_for(root, [fv_row("Q7"), fv_row("Q16")])
    check_eq("fv19_repeat_hidden_while_target_resolves: statuses_for (the publish twin of load) resolves the repeat too",
             (published[1]["status"], QR.hidden_repeat(published[1]), published[0].get("repeated_by")), ("repeat", True, ["Q16"]))


def test_fv19_repeat_of_settled_listed_for_brief(tmp):
    root = fv_story(tmp, "fv19-settled")
    put(root, "Q7", "answered", "Q7: a", reading="a")
    declare(root)
    brief = QR.asked_for_brief(root)
    check_eq("fv19_repeat_of_settled_listed_for_brief: the repeat of an answered question is listed with its target settled and who declared it",
             (brief["repeats"], [x["id"] for x in brief["open"]]), ([{"id": "Q16", "same_as": "Q7", "target_settled": True, "declared_by": "qa-case-designer"}], []))


def test_fv19_repeat_unresolved_shown(tmp):
    rows = [fv_row("Q7"), fv_row("Q16"), fv_row("Q17"), fv_row("Q18")]
    base = fv_story(tmp, "fv19-hash", rows)
    h = {i: row_hash_of(base, i) for i in ("Q7", "Q16", "Q17", "Q18")}
    table = [
        ("same_as gone", [repeat_line("Q16", "Q99", h["Q7"], h["Q16"])]),
        ("2-cycle", [repeat_line("Q16", "Q17", h["Q17"], h["Q16"]), repeat_line("Q17", "Q16", h["Q16"], h["Q17"])]),
        ("3-cycle", [repeat_line("Q16", "Q17", h["Q17"], h["Q16"]), repeat_line("Q17", "Q18", h["Q18"], h["Q17"]),
                     repeat_line("Q18", "Q16", h["Q16"], h["Q18"])]),
        ("own row changed since", [repeat_line("Q16", "Q7", h["Q7"], HASH)]),
        ("record with no row hash", [repeat_line("Q16", "Q7", h["Q7"], None)]),
        ("record with no target_hash", [repeat_line("Q16", "Q7", None, h["Q16"])]),
        ("non-string same_as", [repeat_line("Q16", 7, h["Q7"], h["Q16"])]),
        ("a repeat of itself", [repeat_line("Q16", "Q16", h["Q16"], h["Q16"])]),
        ("same_as with blanks resolves, so it is the one control that hides",
         [repeat_line("Q16", " Q7 ", h["Q7"], h["Q16"])]),
    ]
    for label, lines in table:
        root = fv_story(tmp, "fv19-unres-" + str(abs(hash(label)) % 10**6), rows, answers=lines)
        q16 = row_of(QR.load(root), "Q16")
        want_open = not label.startswith("same_as with blanks")
        check_eq(f"fv19_repeat_unresolved_shown: {label}", (QR.is_open(q16), QR.hidden_repeat(q16)), (want_open, not want_open))
    check_eq("fv19_repeat_unresolved_shown: a dict built outside `load` (no `follows`) is open; so is a row that is no object",
             (QR.is_open({"id": "Q16", "status": "repeat", "changed_since_answer": False, "same_as": "Q7"}), QR.is_open(None)), (True, True))
    old_package = fv_story(tmp, "fv19-old", rows, answers=[repeat_line("Q16", "Q7", h["Q7"], h["Q16"], status="repeated")])
    check_eq("fv19_repeat_unresolved_shown: a record with a status the vocabulary does not know is set aside and the row is shown",
             (QR.is_open(row_of(QR.load(old_package), "Q16")), QR.load(old_package)["skipped"]["invalid"]), (True, 1))


def test_fv19_repeat_write_refusals(tmp):
    root = fv_story(tmp, "fv19-refuse", [fv_row("Q7"), fv_row("Q16"), fv_row("Q17"), fv_row("Q18"), fv_row("Q19")])
    put(root, "Q17", "answered", "Q17: a", reading="a")
    put(root, "Q18", "deferred_to_report", "Q18: until the report")
    before = snapshot(root)
    declare(root, "Q19", "Q16")                      # Q19 -> Q16, so Q16 -> Q19 is a cycle
    table = [
        ("no same_as", dict(target=""), "`same_as` is missing"),
        ("self", dict(target="Q16"), "cannot be marked as a repeat of itself"),
        ("unknown id", dict(target="Q99"), "is no id of the register"),
        ("unknown question", dict(qid="Q98"), "no question with id 'Q98'"),
        ("cycle", dict(qid="Q16", target="Q19"), "a cycle"),
        ("settled row", dict(qid="Q17"), "Q17 is answered"),
        ("deferred row", dict(qid="Q18"), "Q18 is deferred_to_report"),
        ("blank why", dict(why="  "), "`why` is blank"),
    ]
    for label, kwargs, expected in table:
        text = refusal(declare, root, **kwargs)
        check(f"fv19_repeat_write_refusals: {label} is refused with what was expected ({expected})", text is not None and expected in text, str(text))
    check_eq("fv19_repeat_write_refusals: only the control declaration wrote anything (one record)",
             len((root / "work" / "question-answers.jsonl").read_text(encoding="utf-8").splitlines()) - 2, 1)
    check("fv19_repeat_write_refusals: nothing else of the story changed", all(snapshot(root).get(k) == v for k, v in before.items()
                                                                            if not k.endswith("question-answers.jsonl")))
    bad = write_story(tmp / "fv19-unreadable", readiness_raw="{ not json")
    text = refusal(declare, bad)
    check("fv19_repeat_write_refusals: a register that cannot be read is refused, naming it, and no answers file is made",
          text is not None and "not valid JSON" in text and not (bad / "work" / "question-answers.jsonl").exists(), str(text))
    nothing = tmp / "fv19-no-register"
    check("fv19_repeat_write_refusals: no register at all is refused too", "no work/requirements-readiness.json" in str(refusal(declare, nothing)))


def test_fv19_repeat_refused_with_dependants(tmp):
    def story(name, **parts):
        root = fv_story(tmp, name)
        if "plan" in parts:
            write_plan(root, parts["plan"], approved=parts.get("approved", False))
        for case_name, front in parts.get("cases", {}).items():
            write_case(root, case_name, **front)
        return root
    branch = {"id": "TS-3", "question_refs": ["Q16"], "if_answered": {"Q16": {"a": {"disposition": "automate"}}}, "reason": "per Q16"}
    table = [
        ("a plan row keys its answers by Q16", dict(plan=[branch]), ("plan row TS-3 (its answers branch)",)),
        ("another case names it as an unknown oracle", dict(cases={"TC_9": {"then_oracles": json.dumps([{"then": 2, "source": "unknown", "ref": "Q16"}])}}),
         ("case TC_9 (Then 2)",)),
        ("a question_thens entry names it", dict(cases={"TC_8": {"question_thens": json.dumps([{"question": "Q16", "then": 1, "readings": {"a": "x"}}])}}),
         ("case TC_8 (Then 1)",)),
        ("a person oracle names it", dict(cases={"TC_7": {"then_oracles": json.dumps([{"then": 1, "source": "person", "ref": "Q16"}])}}),
         ("case TC_7 (Then 1)",)),
        ("a plan row that only names it in its reason", dict(plan=[{"id": "TS-4", "reason": "see Q16"}]), ("plan row TS-4 (its reason)",)),
        ("a case that cannot be read", dict(cases={"TC_6": {"question_thens": "{ not a list"}}), ("per-answer Then texts could not be read",)),
        ("a plan that cannot be read", dict(plan=None), ("could not be read",)),
        ("an approved plan with a bare ref", dict(plan=[{"id": "TS-5", "question_refs": ["Q16"], "reason": "r"}], approved=True), ("plan row TS-5 (its question_refs)",)),
    ]
    for label, parts, needles in table:
        if parts.get("plan", 1) is None:
            root = story("fv19-dep-" + str(abs(hash(label)) % 10**6))
            (root / "work").mkdir(exist_ok=True)
            (root / "work" / "test-plan.json").write_text("{ not json", encoding="utf-8")
        else:
            root = story("fv19-dep-" + str(abs(hash(label)) % 10**6), **parts)
        plan_before = (root / "work" / "test-plan.json").read_bytes() if (root / "work" / "test-plan.json").exists() else b""
        text = refusal(declare, root)
        check(f"fv19_repeat_refused_with_dependants: {label} -> refused, naming it and the door", text is not None and all(n in text for n in needles)
              and "Expected: repoint them first" in text, str(text))
        check_eq(f"fv19_repeat_refused_with_dependants: {label} -> nothing recorded, row stays open",
                 (QR.is_open(row_of(QR.load(root), "Q16")), (root / "work" / "question-answers.jsonl").exists()), (True, False))
        if label.startswith("an approved"):
            check_eq("fv19_repeat_refused_with_dependants: the approved plan is byte for byte as the person saw it",
                     (root / "work" / "test-plan.json").read_bytes(), plan_before)
    bare = story("fv19-dep-bare", plan=[{"id": "TS-3", "question_refs": ["Q1", "Q16"], "reason": "r"}, {"id": "TS-4", "question_refs": ["Q16", "Q7"], "reason": "r"}])
    rec = declare(bare)
    plan = {r["id"]: r for r in json.loads((bare / "work" / "test-plan.json").read_text(encoding="utf-8"))["rows"]}
    check_eq("fv19_repeat_refused_with_dependants: bare question_refs are moved to Q7 (once, no duplicate) and the repeat is declared",
             (plan["TS-3"]["question_refs"], plan["TS-4"]["question_refs"], rec["same_as"], QR.hidden_repeat(row_of(QR.load(bare), "Q16"))),
             (["Q1", "Q7"], ["Q7"], "Q7", True))
    check_eq("fv19_repeat_refused_with_dependants: no letter is mapped - the rows kept every other key",
             {k: v for k, v in plan["TS-3"].items() if k != "question_refs"}, {"id": "TS-3", "reason": "r"})


def test_fv19_repeat_replay_noop(tmp):
    root = fv_story(tmp, "fv19-replay")
    first = declare(root)
    before = (root / "work" / "question-answers.jsonl").read_bytes()
    again = declare(root, why="another words")
    check_eq("fv19_repeat_replay_noop: the same declaration returns its record and writes nothing", (again == first, (root / "work" / "question-answers.jsonl").read_bytes() == before), (True, True))


def test_fv19_person_answer_beats_repeat(tmp):
    root = fv_story(tmp, "fv19-person")
    declare(root)
    done = QR.record_answers(root, "Q16: b\n", "S4 stop", "person")
    q16 = row_of(QR.load(root), "Q16")
    check_eq("fv19_person_answer_beats_repeat: the person's word to the hidden id is recorded and wins (last record)",
             (done["recorded"], q16["status"], q16["reading"], QR.is_open(q16), QR.hidden_repeat(q16)), (["Q16: b"], "answered", "b", False, False))


def test_fv19_reopen_undoes_repeat(tmp):
    proj = temp_project("qa-question-register-fv19-reopen-")
    try:
        use_project(proj)
        root = write_story(proj / "qa-factory" / "artifacts" / "QA-9", [fv_row("Q7"), fv_row("Q16")])
        declare(root)
        code, out, err = cli("--task", "QA-9", "--reopen", "Q16", "--words", "ask it", "--where", "conductor", "--by", "conductor")
        q16 = row_of(QR.load(root), "Q16")
        check_eq("fv19_reopen_undoes_repeat: --reopen puts a hidden repeat back to open; the target lists nobody",
                 (code, q16["status"], QR.is_open(q16), "repeated_by" in row_of(QR.load(root), "Q7")), (0, "open", True, False))
    finally:
        cleanup(proj)


def test_fv19_repeat_records_history(tmp):
    proj = temp_project("qa-question-register-fv19-")
    try:
        use_project(proj)
        root = write_story(proj / "qa-factory" / "artifacts" / "QA-9", [fv_row("Q7"), fv_row("Q16"), fv_row("Q17")])
        declare(root, "Q16", "Q7")
        show_now(root, "Q7")
        QR.reword(root, "Q7", {"question": "What is the limit of the filter?", "why": "clearer"}, role="conductor", by="conductor", stage="")
        declare(root, "Q17", "Q7")
        QR.record_answers(root, "Q17: a\n", "S4 stop", "person")
        history = QR.repeat_records(root)
        got = [(r["id"], r["same_as"], r["standing"], r["by"], r["declared_by"]) for r in history["records"]]
        check_eq("fv19_repeat_records_history: three records in file order - the first replaced by the carried one, Q17 undone by the person's answer",
                 got, [("Q16", "Q7", "replaced by a later merge", "driver", "qa-case-designer"), ("Q16", "Q7", "merged", "conductor", "qa-case-designer"),
                       ("Q17", "Q7", "answered by the person", "driver", "qa-case-designer")])
        check_eq("fv19_repeat_records_history: the texts are as they stood - the first before the reword, the carried one and Q17's after it",
                 [r["texts"]["same_as_question"] for r in history["records"]],
                 ["What does Q7 ask about the limit?", "What is the limit of the filter?", "What is the limit of the filter?"])
        check_eq("fv19_repeat_records_history: nothing unreadable; the why is the record's words", (history["unreadable"], history["records"][0]["why"]),
                 (False, "both ask the limit"))
        code, out, err = cli("--task", "QA-9", "--reopen", "Q16", "--words", "ask it", "--where", "conductor", "--by", "conductor")
        check_eq("fv19_repeat_records_history: after a reopen the same record reads `reopened`",
                 QR.repeat_records(root)["records"][1]["standing"], "reopened")
        (root / "work" / "question-answers.jsonl").write_text((root / "work" / "question-answers.jsonl").read_text(encoding="utf-8") + "{ broken\n", encoding="utf-8")
        check_eq("fv19_repeat_records_history: a broken line makes the answer `unreadable`, never an empty history", QR.repeat_records(root)["unreadable"], True)
        check_eq("fv19_repeat_records_history: no answers file -> no records, readable", QR.repeat_records(tmp / "nowhere"), {"records": [], "present": False, "unreadable": False})
        check_eq("fv19_repeat_records_history (F3): a story with a readiness file says `present`", QR.repeat_records(root)["present"], True)
    finally:
        cleanup(proj)


def rw(root, qid="Q7", role="conductor", **spec):
    """`QR.reword` as the conductor by default: `(row, refusal text)`."""
    spec = dict({"question": "What is the exact limit of the import?", "why": "the first words did not say which limit"}, **spec)
    try:
        return QR.reword(root, qid, spec, role=role, by="conductor", stage="S4"), None
    except QR.Refused as exc:
        return None, str(exc)


def rw_story(tmp, name, rows=None, **parts):
    root = fv_story(tmp, name, rows)
    if "plan" in parts:
        write_plan(root, parts["plan"])
    for case_name, front in parts.get("cases", {}).items():
        write_case(root, case_name, **front)
    show_now(root, *[r["id"] for r in QR.load(root)["questions"]])
    return root


def test_fv19_reword_keeps_id(tmp):
    root = rw_story(tmp, "fv19-reword")
    old_hash = row_hash_of(root, "Q7")
    row, why = rw(root, readings=["the limit is 100 files", "the limit is 1000 files"])
    check_eq("fv19_reword_keeps_id: the id stays and no second row stands; the hash moved; no answer record so nothing changed since",
             (why, row["id"], len(QR.load(root)["questions"]), row["row_hash"] != old_hash, row["changed_since_answer"], row["question"]),
             (None, "Q7", 2, True, False, "What is the exact limit of the import?"))
    entry = row["reworded"][0]
    check_eq("fv19_reword_keeps_id: the earlier wording is kept whole, with who, when and why", (entry["was"], entry["was_readings"], entry["role"], entry["by"], entry["stage"], entry["why"]),
             ("What does Q7 ask about the limit?", ["reading 0", "reading 1"], "conductor", "conductor", "S4", "the first words did not say which limit"))
    check_eq("fv19_reword_keeps_id: the readings' facts are the producer's (`from`, `if_chosen` untouched)",
             [(r["reading"], r["from"], r["if_chosen"]) for r in row["readings"]], [("the limit is 100 files", "code", "x"), ("the limit is 1000 files", "code", "x")])
    other = rw_story(tmp, "fv19-reword-question-only")
    row2, _ = rw(other)
    check_eq("fv19_reword_keeps_id: a reword of the question alone has no `was_readings`", ("was_readings" in row2["reworded"][0], row2["readings"][0]["reading"]), (False, "reading 0"))
    # an answer typed against the OLD card carries the old shown hash: it reads changed-since and the question is asked again
    stale = rw_story(tmp, "fv19-reword-stale")
    old = row_hash_of(stale, "Q7")
    rw(stale)
    QR.record_answers(stale, "Q7: a\n", "S4 stop", "person", shown={"Q7": old})
    check_eq("fv19_reword_keeps_id: an answer given on the old words is asked again with the new ones",
             (QR.is_open(row_of(QR.load(stale), "Q7")), row_of(QR.load(stale), "Q7")["changed_since_answer"]), (True, True))


def test_fv19_reword_refusals(tmp):
    def story(label, rows=None):
        return rw_story(tmp, "fv19-rr-" + str(abs(hash(label)) % 10**6), rows)
    def after_status(status):
        def make(label):
            root = story(label)
            put(root, "Q7", status, "Q7: a" if status != "deferred_to_report" else "Q7: until the report", reading="a" if status == "answered" else "")
            return root
        return make
    def repeat_of_q16(label):
        root = story(label)
        declare(root, "Q7", "Q16")
        return root
    def not_shown(label):
        root = story(label)
        (root / "state" / "driver-state.json").unlink()
        return root
    def shown_other(label):
        root = story(label)
        state_shown(root, Q7=HASH)
        return root
    def twice(label):
        root = story(label)
        rw(root)
        return root
    broken = lambda label: write_story(tmp / ("fv19-rr-" + str(abs(hash(label)) % 10**6)), readiness_raw="{ not json")
    table = [
        ("answered", after_status("answered"), {}, "Q7 is answered"),
        ("not_needed", after_status("not_needed"), {}, "Q7 is not_needed"),
        ("deferred", after_status("deferred_to_report"), {}, "Q7 is deferred_to_report"),
        ("with_designer", after_status("with_designer"), {}, "Q7 is with_designer"),
        ("repeat", repeat_of_q16, {}, "Q7 is repeat"),
        ("not shown at the last stop", not_shown, {}, "was not shown to the person in these words"),
        ("shown on other bytes", shown_other, {}, "was not shown to the person in these words"),
        ("second reword before a new showing", twice, {}, "was not shown to the person in these words"),
        ("readings count", story, {"readings": ["only one"]}, "must be 2 texts"),
        ("blank reading", story, {"readings": ["x", "  "]}, "none blank"),
        ("readings not a list", story, {"readings": "x"}, "must be 2 texts"),
        ("unchanged text", story, {"question": "  What does Q7 ask   about the limit? "}, "nothing changed"),
        ("blank question", story, {"question": " "}, "`question` is blank"),
        ("blank why", story, {"why": " "}, "`why` is blank"),
        ("question_errors fails", lambda label: story(label, [fv_row("Q7", source_says=[])]), {}, "does not pass the shape check"),
        ("register unreadable", broken, {}, "not valid JSON"),
    ]
    for label, make, spec, expected in table:
        root = make(label)
        before = {k: v for k, v in snapshot(root).items()} if root.exists() else {}
        row, why = rw(root, **spec)
        check(f"fv19_reword_refusals: {label} -> refused ({expected}), nothing written", why is not None and expected in why
              and (label == "second reword before a new showing" or snapshot(root) == before), str(why))
    check_eq("fv19_reword_refusals: an unknown id is refused naming the ids", "no question with id 'Q98'" in str(rw(story("unknown"), qid="Q98")[1]), True)


def test_fv19_reword_who_may(tmp):
    case = {"TC_9": {"then_oracles": json.dumps([{"then": 1, "source": "unknown", "ref": "Q7"}])}}
    plan = [{"id": "TS-3", "question_refs": ["Q7"], "reason": "r"}]
    table = [
        ("conductor", dict(), "conductor", True),
        ("case designer, a case cites Q7", dict(cases=case), "qa-case-designer", True),
        ("case designer, no case cites Q7", dict(), "qa-case-designer", False),
        ("case designer, the row was raised for its case", dict(rows=[fv_row("Q7", raised_for={"case": "TC_1", "then": 1})]), "qa-case-designer", True),
        ("planner, a plan row cites Q7", dict(plan=plan), "qa-test-strategist", True),
        ("planner, nothing cites Q7", dict(), "qa-test-strategist", False),
        ("planner, the row was raised at S3", dict(rows=[fv_row("Q7", raised_for={"claim": "R-1", "origin": "S3-plan"})]), "qa-test-strategist", True),
        ("acceptor that asked Q7", dict(rows=[fv_row("Q7", asked_by="qa-case-critic")]), "qa-case-critic", True),
        ("acceptor that did not ask Q7", dict(rows=[fv_row("Q7", asked_by="qa-scout")]), "qa-case-critic", False),
        ("a role that is blank", dict(), "", False),
    ]
    for label, parts, role, allowed in table:
        root = rw_story(tmp, "fv19-who-" + str(abs(hash(label)) % 10**6), **parts)
        row, why = rw(root, role=role)
        check(f"fv19_reword_who_may: {label} -> {'allowed' if allowed else 'refused with the door'}",
              (why is None) if allowed else (why is not None and "does not cite Q7 in its own work" in why and "raise a question of your own" in why), str(why))


def test_fv19_reword_readings_frozen(tmp):
    readings = ["the limit is 100 files", "the limit is 1000 files"]
    branch = [{"id": "TS-3", "question_refs": ["Q7"], "if_answered": {"Q7": {"a": {"disposition": "automate"}}}, "reason": "r"}]
    letters = {"TC_9": {"question_thens": json.dumps([{"question": "Q7", "then": 1, "readings": {"a": "x"}}])}}
    table = [
        ("designer: a plan row answers by letter -> readings refused", dict(plan=branch), "qa-case-designer", True, "answer by letter", None),
        ("designer: the question text alone is accepted", dict(plan=branch, cases={"TC_5": {"then_oracles": json.dumps([{"then": 1, "source": "unknown", "ref": "Q7"}])}}), "qa-case-designer", False, None, True),
        ("planner: a case answers by letter -> readings refused", dict(cases=letters), "qa-test-strategist", True, "TC_9", None),
        ("planner: its own plan row's branch is its own -> readings accepted", dict(plan=branch), "qa-test-strategist", True, None, True),
        ("conductor: any letter-keyed dependant -> readings refused", dict(plan=branch), "conductor", True, "TS-3", None),
        ("dependants unknown (the plan cannot be read) -> readings refused", dict(), "conductor", True, "could not be read", None),
    ]
    for label, parts, role, with_readings, needle, ok in table:
        root = rw_story(tmp, "fv19-fz-" + str(abs(hash(label)) % 10**6), **({k: v for k, v in parts.items()} if parts else {}))
        if label.startswith("dependants unknown"):
            (root / "work").mkdir(exist_ok=True)
            (root / "work" / "test-plan.json").write_text("{ not json", encoding="utf-8")
        row, why = rw(root, role=role, **({"readings": readings} if with_readings else {}))
        if needle:
            check(f"fv19_reword_readings_frozen: {label}", why is not None and needle in why, str(why))
        else:
            check(f"fv19_reword_readings_frozen: {label}", why is None, str(why))
        if needle and why:
            check(f"fv19_reword_readings_frozen: {label} - the row was not touched", row_of(QR.load(root), "Q7")["question"] == "What does Q7 ask about the limit?")


def test_fv19_reword_carries_repeats(tmp):
    root = fv_story(tmp, "fv19-carry")
    declare(root)
    show_now(root, "Q7")
    row, why = rw(root)
    view = QR.load(root)
    q16 = row_of(view, "Q16")
    check_eq("fv19_reword_carries_repeats: the target was reworded - Q16 is still hidden behind it, with a new record on the new hash",
             (why, QR.hidden_repeat(q16), row_of(view, "Q7")["repeated_by"], q16["target_hash"] == row["row_hash"]), (None, True, ["Q16"], True))
    lines = [json.loads(x) for x in (root / "work" / "question-answers.jsonl").read_text(encoding="utf-8").splitlines()]
    check_eq("fv19_reword_carries_repeats: two repeat records, the second carried over by the reword's executor, the declarer kept",
             [(x["by"], x["declared_by"], x["words"].startswith("carried over")) for x in lines],
             [("driver", "qa-case-designer", False), ("conductor", "qa-case-designer", True)])
    republished = fv_story(tmp, "fv19-carry-republish")
    declare(republished)
    (republished / "work" / "requirements-readiness.json").write_text(json.dumps({"open_questions": [fv_row("Q7", "Another tester's words?"), fv_row("Q16")]}), encoding="utf-8")
    check_eq("fv19_reword_carries_repeats: a tester's republish is NOT carried - the repeat shows again",
             row_of(QR.load(republished), "Q16")["repeat_problem"], "target_changed")


def test_fv19_reword_after_reopen_allowed(tmp):
    root = rw_story(tmp, "fv19-reopen-reword")
    put(root, "Q7", "answered", "Q7: a", reading="a")
    check("fv19_reword_after_reopen_allowed: while the answer stands the reword is refused", "Q7 is answered" in str(rw(root)[1]))
    put(root, "Q7", "open", "the person asks again", hash_from="")
    row, why = rw(root)
    check_eq("fv19_reword_after_reopen_allowed: after a reopen record the row is open again and may be reworded (it was shown on these bytes)",
             (why, row["question"] if row else None), (None, "What is the exact limit of the import?"))


def test_fv19_note_bound_to_bytes(tmp):
    root = fv_story(tmp, "fv19-note")
    rec = QR.record_note(root, "Q7", "The ticket says 100 in the description.", by="conductor", where="stage ran")
    row = row_of(QR.load(root), "Q7")
    check_eq("fv19_note_bound_to_bytes: a note shows on the same bytes (words, who, when) and is no skipped line",
             (row["note"]["words"], row["note"]["by"], row["note"]["at"] == rec["at"], QR.load(root)["skipped"]), ("The ticket says 100 in the description.", "conductor", True,
                                                                                                                       {"broken_lines": 0, "non_object_lines": 0, "unknown_id": 0, "invalid": 0, "unreadable_file": 0}))
    check_eq("fv19_note_bound_to_bytes: a note is no answer - the row stays open, and a later note supersedes",
             (QR.is_open(row), row["status"]), (True, "open"))
    QR.record_note(root, "Q7", "A later note.", by="conductor", where="stage ran")
    check_eq("fv19_note_bound_to_bytes: the latest note on these bytes wins", row_of(QR.load(root), "Q7")["note"]["words"], "A later note.")
    (root / "work" / "requirements-readiness.json").write_text(json.dumps({"open_questions": [fv_row("Q7", "Other words?"), fv_row("Q16")]}), encoding="utf-8")
    check_eq("fv19_note_bound_to_bytes: a note measured on other bytes is dropped after a row change", "note" in row_of(QR.load(root), "Q7"), False)
    ok = QR.record_note(root, "Q16", "x" * QR.NOTE_MAX, by="conductor", where="stage ran")
    check_eq("fv19_note_bound_to_bytes: AT 2000 characters is accepted", len(ok["words"]), 2000)
    check("fv19_note_bound_to_bytes: BEYOND, 2001 characters, is refused", "2001 characters" in str(refusal(QR.record_note, root, "Q16", "x" * 2001, by="conductor", where="stage ran")))
    for label, words, expected in (("blank", "   ", "words are blank"), ("a plugin path", "See ${CLAUDE_PLUGIN_ROOT}/scripts/x.py for it", "plugin_path"),
                                   ("a form field name", "person.review_recorded is set", "form_field")):
        check(f"fv19_note_bound_to_bytes: {label} is refused", expected in str(refusal(QR.record_note, root, "Q16", words, by="conductor", where="stage ran")))
    check("fv19_note_bound_to_bytes: an unknown id and a `by` or `where` the vocabulary lacks are refused",
          all(x is not None for x in (refusal(QR.record_note, root, "Q99", "fine words", by="conductor", where="stage ran"),
                                      refusal(QR.record_note, root, "Q16", "fine words", by="nobody", where="stage ran"),
                                      refusal(QR.record_note, root, "Q16", "fine words", by="conductor", where="nowhere"))))
    stray = fv_story(tmp, "fv19-note-stray", answers=[json.dumps({"kind": "note", "id": "Q99", "words": "w"}), json.dumps({"kind": "note", "id": "Q7", "words": " "})])
    check_eq("fv19_note_bound_to_bytes: a note of an id the register lacks, and a blank one, are counted as skipped lines (nothing is lost silently)",
             (QR.load(stray)["skipped"]["unknown_id"], QR.load(stray)["skipped"]["invalid"]), (1, 1))


def test_fv19_asked_for_brief_empty_and_unreadable(tmp):
    check_eq("fv19_asked_for_brief_empty_and_unreadable: no register file -> nothing asked, not present, not unreadable",
             QR.asked_for_brief(tmp / "fv19-none"), {"open": [], "repeats": [], "unreadable": False, "present": False})
    empty = write_story(tmp / "fv19-empty", [])
    check_eq("fv19_asked_for_brief_empty_and_unreadable: an empty register -> present, nothing asked", (QR.asked_for_brief(empty)["present"], QR.asked_for_brief(empty)["open"]), (True, []))
    bad = write_story(tmp / "fv19-bad", readiness_raw="{ not json")
    check_eq("fv19_asked_for_brief_empty_and_unreadable: a register that cannot be read -> unreadable, so the list may be incomplete", QR.asked_for_brief(bad)["unreadable"], True)
    root = fv_story(tmp, "fv19-brief", [fv_row("Q7"), fv_row("Q8"), fv_row("Q16")])
    declare(root, "Q16", "Q7")
    show_now(root, "Q7")
    brief = QR.asked_for_brief(root)
    check_eq("fv19_asked_for_brief_empty_and_unreadable: the open rows in register order with repeated_by, shown_at_last_stop and the reword count",
             [(x["id"], x["repeated_by"], x["shown_at_last_stop"], x["reworded"]) for x in brief["open"]], [("Q7", ["Q16"], True, 0), ("Q8", [], False, 0)])
    check_eq("fv19_asked_for_brief_empty_and_unreadable: the repeat of an open row is listed with its target unsettled", brief["repeats"],
             [{"id": "Q16", "same_as": "Q7", "target_settled": False, "declared_by": "qa-case-designer"}])
    rw(root)
    check_eq("fv19_asked_for_brief_empty_and_unreadable: after a reword the row is no longer 'shown on its bytes' and counts one reword",
             [(x["id"], x["shown_at_last_stop"], x["reworded"]) for x in QR.asked_for_brief(root)["open"]][0], ("Q7", False, 1))
    no_state = fv_story(tmp, "fv19-brief-nostate")
    check_eq("fv19_asked_for_brief_empty_and_unreadable: no driver state -> shown_at_last_stop False, readable",
             ([x["shown_at_last_stop"] for x in QR.asked_for_brief(no_state)["open"]], QR.last_stop_shown(no_state)), ([False, False], {"shown": {}}))
    (no_state / "state").mkdir()
    for label, text in (("not json", "{ nope"), ("shown not a dict", json.dumps({"question_stop": {"shown": [1]}})), ("no key", "{}")):
        (no_state / "state" / "driver-state.json").write_text(text, encoding="utf-8")
        check_eq(f"fv19_asked_for_brief_empty_and_unreadable: driver state {label} -> shown is empty, no raise", QR.last_stop_shown(no_state), {"shown": {}})
    (no_state / "state" / "driver-state.json").write_text(json.dumps({"question_stop": {"stage": "S2", "at": "t", "shown": {"Q7": "h", "Q8": 5}}}), encoding="utf-8")
    check_eq("fv19_asked_for_brief_empty_and_unreadable: an entry whose hash is no text is left out", QR.last_stop_shown(no_state), {"stage": "S2", "at": "t", "shown": {"Q7": "h"}})


class _Pins:
    """`critic_rollcall.raise_pending` on a story with no real case store: the three seams it uses are replaced and restored."""
    def __init__(self, source):
        self.source, self.pinned = source, []

    def __enter__(self):
        import case_versions as V
        import contract as C
        import critic_rollcall as CR
        self.mods = (V, C, CR)
        self.saved = (V.store_root, V.create_version, V.pin, C.story_case_links, CR._resolve_source)
        V.store_root = lambda root: Path(root) / "store"
        V.create_version = lambda store, source: {"id": "cv_new"}
        V.pin = lambda root, record, expected_previous_version=None: self.pinned.append(record["id"])
        C.story_case_links = lambda root: [{"case_id": self.source.stem, "version": "cv_old"}]
        CR._resolve_source = lambda root, link: self.source
        return self

    def __exit__(self, *exc):
        V, C, CR = self.mods
        V.store_root, V.create_version, V.pin, C.story_case_links, CR._resolve_source = self.saved


def test_fv19_raise_pending_records_repeats(tmp):
    import critic_rollcall as CR
    root = fv_story(tmp, "fv19-rp")
    entries = [{"question": "Q16", "same_as": "Q7", "why": "both ask the limit"}]
    source = write_case(root, "TC_1", question_repeats=json.dumps(entries))
    with _Pins(source) as pins:
        out = CR.raise_pending(root)
    check_eq("fv19_raise_pending_records_repeats: a case with only `question_repeats` is read: recorded, key dropped, re-pinned once",
             (out["repeats"], out["question_notes"], "question_repeats" in source.read_text(encoding="utf-8"), pins.pinned, QR.hidden_repeat(row_of(QR.load(root), "Q16"))),
             ([{"question": "Q16", "same_as": "Q7"}], [], False, ["cv_new"], True))
    refused = fv_story(tmp, "fv19-rp-refused")
    bad = [{"question": "Q16", "same_as": "Q99", "why": "w"}, {"question": "Q16", "same_as": "raise", "why": "w"}, {"question": "Q16", "same_as": "Q7"}]
    source = write_case(refused, "TC_1", question_repeats=json.dumps(bad))
    before = source.read_bytes()
    with _Pins(source) as pins:
        out = CR.raise_pending(refused)
    check_eq("fv19_raise_pending_records_repeats: refused and malformed entries keep the key and say why, one line each; nothing is written or pinned",
             (len(out["question_notes"]), out["repeats"], source.read_bytes() == before, pins.pinned), (3, [], True, []))
    check("fv19_raise_pending_records_repeats: the lines name the entry and the register's own reason",
          "no id of the register" in out["question_notes"][0] and "`raise`" in out["question_notes"][1] and "needs `question`, `same_as` and `why`" in out["question_notes"][2])
    mixed = fv_story(tmp, "fv19-rp-mixed")
    source = write_case(mixed, "TC_1", question_repeats=json.dumps([entries[0], bad[0]]))
    with _Pins(source):
        out = CR.raise_pending(mixed)
    check_eq("fv19_raise_pending_records_repeats: a done entry leaves the key, a refused one stays beside it",
             (len(out["repeats"]), json.loads(source.read_text(encoding="utf-8").split("question_repeats: ")[1].splitlines()[0])), (1, [bad[0]]))
    malformed = fv_story(tmp, "fv19-rp-malformed")
    source = write_case(malformed, "TC_1", question_repeats="{ not a list")
    with _Pins(source):
        out = CR.raise_pending(malformed)
    check("fv19_raise_pending_records_repeats: a key that is not one line of JSON is one note and is kept", len(out["question_notes"]) == 1 and "was not read" in out["question_notes"][0])
    plain = fv_story(tmp, "fv19-rp-none")
    source = write_case(plain, "TC_1", title="no keys of ours here")
    stamp = os.stat(source).st_mtime_ns
    with _Pins(source) as pins:
        out = CR.raise_pending(plain)
    check_eq("fv19_raise_pending_records_repeats: a case with none of the three keys is not written (mtime unchanged) and nothing is pinned",
             (os.stat(source).st_mtime_ns == stamp, pins.pinned, out["question_notes"]), (True, [], []))
    replay = fv_story(tmp, "fv19-rp-replay")
    declare(replay)
    source = write_case(replay, "TC_1", question_repeats=json.dumps(entries))
    with _Pins(source):
        out = CR.raise_pending(replay)
    check_eq("fv19_raise_pending_records_repeats: a replay of a standing declaration is a no-op that still drops the key",
             (len(out["repeats"]), "question_repeats" in source.read_text(encoding="utf-8"), len((replay / "work" / "question-answers.jsonl").read_text(encoding="utf-8").splitlines())), (1, False, 1))


def test_fv19_raise_pending_rewords(tmp):
    import critic_rollcall as CR
    root = rw_story(tmp, "fv19-rpw", [fv_row("Q7")], cases={})
    entry = {"question": "Q7", "text": "What is the exact limit of the import?", "why": "the first words did not say"}
    source = write_case(root, "TC_1", then_oracles=json.dumps([{"then": 1, "source": "unknown", "ref": "Q7"}]), reword_questions=json.dumps([entry]))
    with _Pins(source) as pins:
        out = CR.raise_pending(root)
    row = row_of(QR.load(root), "Q7")
    check_eq("fv19_raise_pending_rewords: `reword_questions` is executed (role the designer, by driver, S4) and the entry is dropped; the case is re-pinned",
             (out["rewords"], row["question"], row["reworded"][0]["role"], row["reworded"][0]["by"], "reword_questions" in source.read_text(encoding="utf-8"), pins.pinned),
             ([{"question": "Q7"}], "What is the exact limit of the import?", "qa-case-designer", "driver", False, ["cv_new"]))
    again = rw_story(tmp, "fv19-rpw-refused", [fv_row("Q7")])
    source = write_case(again, "TC_9", reword_questions=json.dumps([entry]))        # no case cites Q7: the designer may not
    before = source.read_bytes()
    with _Pins(source) as pins:
        out = CR.raise_pending(again)
    check_eq("fv19_raise_pending_rewords: a refused entry is kept with a line that says why; nothing is written", (len(out["question_notes"]), source.read_bytes() == before, pins.pinned),
             (1, True, []))
    check("fv19_raise_pending_rewords: ...in the register's words", "does not cite Q7 in its own work" in out["question_notes"][0])


def test_fv19_handoff_rewords_item(tmp):
    proj = temp_project("qa-question-register-fv19-form-")
    try:
        use_project(proj)
        root = write_story(proj / "qa-factory" / "artifacts" / "QA-9", [fv_row("Q7", asked_by="qa-case-critic")])
        show_now(root, "Q7")
        forms = root / "work" / "handoffs"
        forms.mkdir(parents=True)
        new = {"question": "Is the import limit 100 or 1000?", "read": ["work/requirements-register.md#R-7"], "recommendation": "plan on 100",
               "options": [{"reading": "100", "if_chosen": "the plan checks 100"}, {"reading": "1000", "if_chosen": "the plan checks 1000"}],
               "severity": "blocker", "owner_role": "po_ba", "why_person": "requirement_intent"}
        item = {"rewords": "Q7", "question": "What is the exact limit of the import?", "why": "unclear first words"}
        def form(name, *entries):
            lines = ["header: {role: qa-case-critic, stage: S2, window_or_scope: S2, verdict: ok}", "questions:"] + ["  - " + json.dumps(e) for e in entries]
            path = forms / (name + ".yaml")
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            return path
        done = QR.raise_from_handoff(root, form("S2-qa-case-critic-1", new, item), stage="S2", asked_by="qa-case-critic")
        view = QR.load(root)
        check_eq("fv19_handoff_rewords_item: a `rewords` item asks Q7 again (role = the form's asker), the other entry is raised, the index stays the form's own",
                 (done["rewords"], done["reword_problems"], row_of(view, "Q7")["question"], row_of(view, "Q7")["reworded"][0]["role"],
                  done["raised"][0]["raised_from"]["row"]), (["Q7"], [], "What is the exact limit of the import?", "qa-case-critic", "questions[0]"))
        refused = QR.raise_from_handoff(root, form("S2-qa-case-critic-2", new, item), stage="S2", asked_by="qa-case-critic")
        check("fv19_handoff_rewords_item: a refused reword (not shown since it was last worded) is a `reword_problems` line and the form is not refused",
              len(refused["reword_problems"]) == 1 and "was not shown to the person" in refused["reword_problems"][0] and len(refused["already"]) == 0, str(refused))
        odd = QR.raise_from_handoff(root, form("S2-qa-case-critic-3", {"rewords": 5, "question": "x"}, {"rewords": "Q99", "question": "y", "why": "z"}),
                                    stage="S2", asked_by="qa-case-critic")
        check_eq("fv19_handoff_rewords_item: a malformed item (and an unknown id) never refuses the form; each is a line", (odd["raised"], len(odd["reword_problems"])), ([], 2))
        none = QR.raise_from_handoff(root, form("S2-qa-case-critic-4", new), stage="S2", asked_by="qa-case-critic")
        check_eq("fv19_handoff_rewords_item: a form with no `rewords` item has the result it always had (no new key)", sorted(none), ["already", "dispatch", "raised"])
        other = QR.raise_from_handoff(root, form("S2-qa-case-critic-5", {"rewords": "Q7", "question": "z", "why": "w"}), stage="S2", asked_by="qa-scout")
        check("fv19_handoff_rewords_item: a role that did not ask the question may not reword it - a line, not a refusal", "does not cite Q7" in other["reword_problems"][0])
    finally:
        cleanup(proj)


def test_fv19_origin_words_unknown_default(tmp):
    table = [("acceptance_criteria", "the acceptance criteria"), ("parent_ticket", "the parent ticket"), ("claim", "the change under test (before / now)"),
             ("person", "what you said earlier"), ("comment:TP-1", "a comment on the ticket"), ("not-an-origin", ""), ("", ""), (None, ""), ("  attachment ", "an attachment")]
    for word, want in table:
        check_eq(f"fv19_origin_words_unknown_default: {word!r}", QR.origin_words(word), want)
    import contract as C
    check_eq("fv19_origin_words_unknown_default: every origin word of the contract has its words in the data file",
             [w for w in C.READING_ORIGINS if not QR.origin_words(w)], [])


def test_fv19_cli_repeat_reword_note(tmp):
    proj = temp_project("qa-question-register-fv19-cli-")
    try:
        use_project(proj)
        root = write_story(proj / "qa-factory" / "artifacts" / "QA-9", [fv_row("Q7"), fv_row("Q16")])
        base = ["--where", "stage ran", "--by", "conductor"]
        why = proj / "why.txt"
        why.write_text("both ask the limit", encoding="utf-8")
        code, out, err = cli("--task", "QA-9", "--repeat", "Q16", "--same-as", "Q7", "--words-file", str(why), *base)
        check_eq("fv19_cli_repeat_reword_note: --repeat exits 0 and records it", (code, json.loads(out)["recorded"]["same_as"], QR.hidden_repeat(row_of(QR.load(root), "Q16"))), (0, "Q7", True))
        code, out, err = cli("--task", "QA-9", "--repeat", "Q7", "--same-as", "Q16", "--words", "w", *base)
        check("fv19_cli_repeat_reword_note: --repeat that the register refuses (a cycle) exits 2 with its text", code == 2 and "a cycle" in err, err)
        code, out, err = cli("--task", "QA-9", "--repeat", "Q7", "--words", "w", *base)
        check("fv19_cli_repeat_reword_note: --repeat without --same-as is refused naming it", code == 2 and "--repeat needs --same-as" in err, err)
        code, out, err = cli("--task", "QA-9", "--reopen", "Q16", "--same-as", "Q7", "--words", "w", *base)
        check("fv19_cli_repeat_reword_note: --same-as without --repeat is refused", code == 2 and "--same-as goes with --repeat only" in err, err)
        show_now(root, "Q7")
        spec = proj / "q.json"
        spec.write_text(json.dumps({"question": "What is the exact limit of the import?", "why": "unclear"}), encoding="utf-8")
        code, out, err = cli("--task", "QA-9", "--reword", "Q7", "--question-file", str(spec), *base)
        check_eq("fv19_cli_repeat_reword_note: --reword exits 0, the conductor is the role, the id stays", (code, json.loads(out)["reworded"]["id"], row_of(QR.load(root), "Q7")["reworded"][0]["role"]), (0, "Q7", "conductor"))
        code, out, err = cli("--task", "QA-9", "--reword", "Q7", "--question-file", str(spec), *base)
        check("fv19_cli_repeat_reword_note: a second --reword before a new showing exits 2", code == 2 and "was not shown to the person" in err, err)
        code, out, err = cli("--task", "QA-9", "--reword", "Q7", *base)
        check("fv19_cli_repeat_reword_note: --reword needs --question-file", code == 2 and "--reword needs --question-file" in err, err)
        words = proj / "note.txt"
        words.write_text("The ticket says 100 in its description.", encoding="utf-8")
        code, out, err = cli("--task", "QA-9", "--note", "Q16", "--words-file", str(words), *base)
        check_eq("fv19_cli_repeat_reword_note: --note exits 0 and the card data carries it", (code, json.loads(out)["recorded"]["kind"], row_of(QR.load(root), "Q16").get("note", {}).get("words")),
                 (0, "note", "The ticket says 100 in its description."))
        code, out, err = cli("--task", "QA-9", "--note", "Q16", "--words", "x" * 2001, *base)
        check("fv19_cli_repeat_reword_note: --note beyond 2000 characters exits 2", code == 2 and "2001 characters" in err, err)
        code, out, err = cli("--task", "QA-9", "--note", "Q16", "--words", "fine words", "--where", "nowhere", "--by", "conductor")
        check("fv19_cli_repeat_reword_note: a `where` outside the vocabulary exits 2", code == 2 and "not a known value" in err, err)
        code, out, err = cli("--task", "QA-9", "--note", "Q16", "--reword", "Q7", "--words", "w", *base)
        check("fv19_cli_repeat_reword_note: the exactly-one-operation rule names the three new operations",
              code == 2 and all(x in err for x in ("--repeat QID", "--reword QID", "--note QID")) and "got 2" in err, err)
        code, out, err = cli("--task", "QA-9", "--note", "Q16", "--words", "w", "--question-file", "x.json", *base)
        check("fv19_cli_repeat_reword_note: a flag with no meaning for the operation is refused", code == 2 and "--question-file has no meaning with --note" in err, err)
    finally:
        cleanup(proj)


def test_fv19_cli_stage_on_repeat_and_reword(tmp):
    """`--stage` on `--repeat`, `--reword` and `--raise --from-handoff`: one value rule, one table (FV1-9 tail card C)."""
    import acceptance
    import null_outcomes
    valid_list = "S0, S1, S2, S3, S4, S5, S6, S7, S8, S9"
    wide = "S" + "9" * 299
    bad = [("S99", "S99"), ("s3 lower case", "s3"), ("stage3", "stage3"), ("gate A", "gate A"), ("S10", "S10"), ("300 chars", wide),
           ("non-ASCII look-alike of S", chr(1057) + "3"), ("inner newline", "S\n3"), ("inner tab", "S\t3")]
    good = [("S3", "S3", "S3"), ("padded", " S3 ", "S3"), ("S4", "S4", "S4"), ("absent", None, ""), ("empty", "", ""), ("spaces", "   ", "")]
    for op in ("repeat", "reword", "handoff"):
        def run(stage, patched=False):
            proj = temp_project("qa-question-register-fv19-stage-")
            try:
                use_project(proj)
                root = write_story(proj / "qa-factory" / "artifacts" / "QA-9", [fv_row("Q7", asked_by="qa-case-critic"), fv_row("Q16")])
                show_now(root, "Q7")
                why = proj / "why.txt"
                why.write_text("both ask the limit", encoding="utf-8")
                spec = proj / "q.json"
                spec.write_text(json.dumps({"question": "What is the exact limit of the import?", "why": "unclear"}), encoding="utf-8")
                form = root / "work" / "handoffs" / "S2-qa-case-critic-1.yaml"
                form.parent.mkdir(parents=True)
                form.write_text("header: {role: qa-case-critic, stage: S2, window_or_scope: S2, verdict: ok}\nquestions:\n  - "
                                + json.dumps({"rewords": "Q7", "question": "What is the exact limit of the import?", "why": "unclear"}) + "\n",
                                encoding="utf-8")
                args = {"repeat": ["--repeat", "Q16", "--same-as", "Q7", "--words-file", str(why), "--where", "stage ran", "--by", "conductor"],
                        "reword": ["--reword", "Q7", "--question-file", str(spec), "--where", "stage ran", "--by", "conductor"],
                        "handoff": ["--raise", "--from-handoff", str(form), "--asked-by", "qa-case-critic"]}[op]
                if stage is not None:
                    args += ["--stage", stage]
                real = (acceptance.stage_def_of, null_outcomes.stage_ids)
                if patched:
                    acceptance.stage_def_of, null_outcomes.stage_ids = (lambda *a, **k: {}), (lambda: set())
                try:
                    code, out, err = cli("--task", "QA-9", *args)
                finally:
                    acceptance.stage_def_of, null_outcomes.stage_ids = real
                view = QR.load(root)
                q7, q16 = row_of(view, "Q7"), row_of(view, "Q16")
                recorded = {"repeat": (q16.get("repeats") or q16.get("repeat") or {}), "reword": (q7.get("reworded") or [{}])[-1],
                            "handoff": (q7.get("reworded") or [{}])[-1]}[op]
                return code, out, err, recorded
            finally:
                cleanup(proj)
        for label, given, want in good:
            if op == "handoff" and not (given or "").strip():
                code, out, err, _rec = run(given)
                check(f"fv19_cli_stage_on_repeat_and_reword[{op}/{label}]: a blank --stage on --raise --from-handoff is still the missing flag",
                      code == 2 and "needs --stage" in err, err)
                continue
            code, out, err, rec = run(given)
            if op == "repeat":      # `record` drops an empty field: a blank stage is a record with no `stage` key
                stage_seen = (json.loads(out).get("recorded") or {}).get("stage", "") if code == 0 else None
            else:
                stage_seen = rec.get("stage")
            check_eq(f"fv19_cli_stage_on_repeat_and_reword[{op}/{label}]: accepted and recorded as {want!r}", (code, stage_seen), (0, want))
        for label, given in bad:
            code, out, err, _rec = run(given)
            check(f"fv19_cli_stage_on_repeat_and_reword[{op}/{label}]: refused (exit 2), names the valid ids, nothing written",
                  code == 2 and "is not a stage of the factory" in err and valid_list in err and out == "", f"{code} {err}")
            if len(given) > 80:
                check(f"fv19_cli_stage_on_repeat_and_reword[{op}/{label}]: the value is shown cut to 80 characters", wide not in err, err[:300])
        code, out, err, _rec = run("S3", patched=True)
        check(f"fv19_cli_stage_on_repeat_and_reword[{op}/unreadable table]: a non-blank --stage is refused saying the table could not be read",
              code == 2 and "the stage table could not be read" in err, f"{code} {err}")
        if op != "handoff":
            code, out, err, _rec = run(None, patched=True)
            check_eq(f"fv19_cli_stage_on_repeat_and_reword[{op}/unreadable table]: a blank --stage still succeeds", code, 0)
    proj = temp_project("qa-question-register-fv19-stage-guard-")
    try:
        use_project(proj)
        write_story(proj / "qa-factory" / "artifacts" / "QA-9", [fv_row("Q7"), fv_row("Q16")])
        words = ["--words", "w", "--where", "stage ran", "--by", "conductor"]
        for label, args, text in (("--note", ["--note", "Q16"], "--stage goes with --raise --from-handoff, --repeat or --reword only"),
                                  ("--answer", ["--answer", "Q16", "--register-hash", "h"], "--stage goes with --raise --from-handoff, --repeat or --reword only"),
                                  ("--show", ["--show"], "--stage goes with --raise --from-handoff, --repeat or --reword only"),
                                  ("--raise alone", ["--raise", "--case-file", "c.md", "--then", "1", "--question-file", "q.json"], "--stage has no meaning with --raise")):
            code, out, err = cli("--task", "QA-9", *args, *words, "--stage", "S3")
            check(f"fv19_cli_stage_on_repeat_and_reword[guard/{label}]: refused with the guard's text", code == 2 and text in err, f"{code} {err}")
    finally:
        cleanup(proj)


TESTS = [test_fv19_repeat_hidden_while_target_resolves, test_fv19_repeat_of_settled_listed_for_brief, test_fv19_repeat_unresolved_shown,
         test_fv19_repeat_write_refusals, test_fv19_repeat_refused_with_dependants, test_fv19_repeat_replay_noop, test_fv19_person_answer_beats_repeat,
         test_fv19_reopen_undoes_repeat, test_fv19_repeat_records_history, test_fv19_reword_keeps_id, test_fv19_reword_refusals, test_fv19_reword_who_may,
         test_fv19_reword_readings_frozen, test_fv19_reword_carries_repeats, test_fv19_reword_after_reopen_allowed, test_fv19_note_bound_to_bytes,
         test_fv19_asked_for_brief_empty_and_unreadable, test_fv19_raise_pending_records_repeats, test_fv19_raise_pending_rewords,
         test_fv19_handoff_rewords_item, test_fv19_origin_words_unknown_default, test_fv19_cli_repeat_reword_note,
         test_fv19_cli_stage_on_repeat_and_reword,
         test_gw1_47_stray_line_starts_with_an_open_register_id, test_answers_lock_busy_names_the_holder, test_placeholder_question_row_dropped, test_x2_6_role_questions,test_g1_13_question_row_keys_never_meet_and_the_readiness_writer_keeps_its_bytes, test_e1_exact_id, test_e2_load, test_e3_answers_file, test_e4_register, test_e5_parser, test_e6_cli,
         test_e6_cli_subprocess, test_e7_battery, test_edge2_fence_and_quote, test_edge3_row_hash, test_edge4_where_by,
         test_edge5_case_decisions, test_edge5_case_cli, test_edge6_words_file, test_edge7_lock, test_edge8_named,
         test_cmp1, test_t256_o6_accept_as_blocked_is_a_whole_line_case_token, test_t256_o4_raise_for_case_is_keyed_by_case_and_then,
         test_hf2_7_p1_vocabulary_and_parser, test_hf2_7_p1_record_answers, test_hf2_7_p1_record_rules,
         test_hf2_7_p1_predicates, test_hf2_7_p1_brief_and_drift, test_hf2_7_p1_cli_defer, test_hf2_7_p1_state_exit_row,
         test_hf2_7_p1_readiness_rules]


def main() -> None:
    tmp = temp_dir("qa-question-register-test-")
    try:
        for test in TESTS:
            test(tmp)
    finally:
        cleanup(tmp)
    finish("question_register")


if __name__ == "__main__":
    main()
