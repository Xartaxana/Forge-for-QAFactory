#!/usr/bin/env python3
"""The one reader of a story's open questions: their status, the answers file, the strict parser.

    question_register.py --task T --show
    question_register.py --task T --answer Q1 --reading a --words "<the person's words>" \\
        --where "gate A" --by conductor --register-hash <row_hash that --show printed for Q1>
    question_register.py --task T --not-needed Q1 --words "<words>" --where ... --by ... --register-hash ...
    question_register.py --task T --reopen Q1 --words "<words>" --where ... --by ...   # back to open
    question_register.py --task T --defer Q3 --words-file <path> --where ... --by ... --register-hash ...
        # `Q3: until the report`: kept open on the person's word, not asked again, listed by the report
    question_register.py --task T --keep-manual <full case id> --words "<words>" --where ... --by ...
    question_register.py --task T --automate <full case id> --words "<words>" --where ... --by ...
    question_register.py --task T --raise --case-file <case.md> --then N --question-file <q.json>
        # a before/now question after S2 (t-227, P20): the id and the two readings are code's, the rest the author's
    question_register.py --task T --repeat Q16 --same-as Q7 --words-file <why> --where "stage ran" --by conductor
        # FV1-9: Q16 asks what Q7 asks; it is hidden while Q7 stands unchanged and nothing else rests on Q16
    question_register.py --task T --reword Q7 --question-file <q.json> --where "stage ran" --by conductor
        # FV1-9: an unanswered question the person was shown is asked again in clearer words (the id stays)
    question_register.py --task T --note Q7 --words-file <file> --where "stage ran" --by conductor
        # FV1-9: what helps the person answer Q7, written by the conductor; shown on its card while the row is as it was
    (--words-file <path> instead of --words for long words; exactly one of the two)
    (--where and --by have no default: the values are the closed lists of question-vocabulary.json)

TP1-13797 (cmp1): the person answered all five register questions at gate A, by name, and gate
B still listed the five as unanswered - the reader looked for the id in `words`/`decision` while
the answer sat in `authorization_source`, and matched `Q1` inside `Q10` as a substring (B-181).
Every question carried four spellings (`Q1`, `Q-1`, `R-14`, `Q-R14`) and nothing resolved the
three role-invented ones. This module is the ONE place that says whether a question is open:

  * ids: the register id (`work/requirements-readiness.json` `open_questions[].id`), matched
    exactly and case-sensitively after trimming. No substring, prefix or alias resolution.
  * status: `open` (no record), `answered`, `not_needed`, `with_designer`, `deferred_to_report` - from
    the code-owned, append-only `work/question-answers.jsonl`, the LAST record per id winning - and,
    for a question with NO record, `named`: the exact id stands (as a word, not inside a URL, a path or
    a file name) in the person's recorded gate words. `named` is not `answered` (FR-41): an id
    mentioned is not a question settled.
  * the ONE definition of the words the readers share (AR-13): `settled` (answered or not needed, on
    the bytes the person saw), `is_open` (asked again: no record, or a record whose row changed since,
    or whose `before` value is still missing), `open_blocker` (open, and not marked `major`/`minor`),
    `answer_key` (the letter or `not_needed` a settled question follows). The error direction of all
    of them is "open": an unknown status, a missing severity or an unreadable store never reads as
    settled (FR-59). A different answer on a settled id is refused until the id is reopened (H6).
  * `row_hash`: each register row has its own fingerprint. A record stores the hash of the row AS
    IT WAS SHOWN; `changed_since_answer` says the row is not the one the person saw (E-14).
  * case decisions: `<full case id>: manual|automate` are the person's explicit word (P13), kept as
    records of `kind: case`, separate from the question records.
  * `parse_choices`: closed tokens only (`Q1: a`, `Q1: not needed`, `<case id>: manual|automate|accept as blocked`),
    each the WHOLE line, read as structure, never as meaning (FR-12). It errs only toward NOT seeing
    a choice: a question it cannot read stays with the conductor, a role that reads meaning.

The closed lists (statuses, where-values, who-recorded, stop reasons) live in
`references/question-vocabulary.json` (FR-13). Reading and answering call nothing else in the
factory; only `--raise` reads `contract` and `s5_precheck` (the case's own oracle fields and Then
numbers). Nobody has to call this first.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
import re
import string
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
VOCAB_PATH = HERE.parent / "references" / "question-vocabulary.json"
READINESS_REL = ("work", "requirements-readiness.json")
ANSWERS_REL = ("work", "question-answers.jsonl")
LOCK_NAME = ".question-answers.lock"
CASE_LINKS_REL = ("state", "story-case-links.json")
LETTERS = string.ascii_lowercase
COMMAND = "question_register.py"
LOCK_WAIT_SECONDS = 30.0

# `authorization_source` first: on cmp1 it is the ONLY key of a gate record that holds the
# person's words (there is no `words` key, and `decision` is the bare word "approved").
GATE_WORD_KEYS = ("authorization_source", "words", "decision")
GATE_WHERE = {"A": "gate A", "B": "gate B"}
BOM = chr(0xFEFF)  # built, not typed: FR-29, and a literal BOM in a source file is invisible
NBSP = chr(0xA0)   # a no-break space is a space for the strict grammar: a chat client types it
SPACES = " \t" + NBSP
# Bullets a chat client or a document editor puts where markdown has `-` (built, never typed: FR-30).
BULLETS = "".join(chr(c) for c in (0x2022, 0x2023, 0x25E6, 0x25CF, 0x25AA, 0x2043, 0xB7))
HASH_TEXT = re.compile(r"[0-9a-f]{64}")
# The statuses the readers share (AR-13): a question the factory asks again, and a question the person settled.
OPEN_STATUSES = ("open", "named")
SETTLED_STATUSES = ("answered", "not_needed")
DEFERRED = "deferred_to_report"      # kept open on the person's word: not asked again, listed by the report
UNTIL_THE_REPORT = "until the report"  # the token that records it
NOT_BLOCKING = ("major", "minor")    # any other severity (or none) is blocking: the error goes toward asking
WHERE_UNKNOWN = "earlier"            # the words for a `where` the vocabulary does not know
REPEAT = "repeat"                    # FV1-9: a question declared to ask what an earlier one asks; hidden only through `hidden_repeat`
NOTE_MAX = 2000                      # characters of a conductor's note: a card is a card
REWORD_ARTIFACT_KINDS = ("cases", "plan_rows")   # the artifact kinds `reword_own_artifacts` may name for a role
DRIVER_STATE_REL = ("state", "driver-state.json")


class Refused(ValueError):
    """A request the register will not write; the text says what is wrong, what was expected."""


def vocabulary() -> dict:
    """The closed lists, from the data file. A missing or malformed file is a package defect."""
    keys = ("statuses", "recorded_statuses", "where", "by", "case_decisions", "stop_reasons")
    try:
        data = json.loads(VOCAB_PATH.read_text(encoding="utf-8-sig"))
        for key in keys:
            if not (isinstance(data[key], list) and data[key] and all(isinstance(x, str) for x in data[key])):
                raise ValueError(f"`{key}` must be a non-empty list of texts")
        words = data["where_words"]
        if not (isinstance(words, dict) and all(isinstance(words.get(w), str) and words[w].strip() for w in data["where"])):
            raise ValueError("`where_words` must give every value of `where` a non-empty text (what a person reads)")
        origins = data.get("reading_origin_words", {})      # FV1-9 rows: optional, but when present they must be usable
        if not (isinstance(origins, dict) and all(isinstance(k, str) and isinstance(v, str) and v.strip() for k, v in origins.items())):
            raise ValueError("`reading_origin_words` must map each origin word to a non-empty text (what a person reads)")
        own = data.get("reword_own_artifacts", {})
        if not (isinstance(own, dict) and all(isinstance(k, str) and v in REWORD_ARTIFACT_KINDS for k, v in own.items())):
            raise ValueError("`reword_own_artifacts` must map a role to one of " + ", ".join(REWORD_ARTIFACT_KINDS))
        return data
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise RuntimeError(f"{VOCAB_PATH} is unusable ({type(exc).__name__}: {exc}); it holds the "
                           f"closed lists {', '.join(keys)} and `where_words` - restore it from the package") from exc


def where_words(where) -> str:
    """How a person reads a `where` value ("when the requirements were checked"): the data file's words,
    `earlier` for a value it does not know. The raw value ("S2 stop") never reaches a person (FR-6, FR-13)."""
    found = vocabulary()["where_words"].get(where) if isinstance(where, str) else None
    return found if isinstance(found, str) and found.strip() else WHERE_UNKNOWN


def origin_words(origin) -> str:
    """How a person reads the origin of a reading (`from`, the part before any `:`): the data file's words (`reading_origin_words`,
    FR-13), `""` for a word the file does not know and for a blank one - the caller prints an unknown word plainly and a blank one not
    at all. The raw word (`parent_ticket`) never reaches a person from here."""
    word = str(origin or "").split(":")[0].strip()
    found = vocabulary().get("reading_origin_words", {}).get(word) if word else None
    return found.strip() if isinstance(found, str) and found.strip() else ""


# --------------------------------------------------------------------------------------------
# reading
# --------------------------------------------------------------------------------------------

def _register(root: Path) -> tuple:
    """(rows, problems, present, hash): the register as the S2 role wrote it, never raising."""
    path = root.joinpath(*READINESS_REL)
    try:
        raw = path.read_bytes().decode("utf-8-sig", errors="replace")
    except FileNotFoundError:
        return [], [], False, ""
    except OSError as exc:
        return [], [f"{path} could not be read ({type(exc).__name__}: {exc})"], True, ""
    if not raw.strip():
        return [], [f"{path} is empty: no questions can be read from it"], True, ""
    try:
        data = json.loads(raw)
    except (ValueError, RecursionError):
        return [], [f"{path} is not valid JSON: no questions can be read from it"], True, ""
    if not isinstance(data, dict):
        return [], [f"{path} holds {type(data).__name__}, expected an object with `open_questions`"], True, ""
    rows = data.get("open_questions")
    if rows is None:
        return [], [], True, _hash([])
    if not isinstance(rows, list):
        return [], [f"`open_questions` in {path} is {type(rows).__name__}, expected a list"], True, ""
    return rows, [], True, _hash(rows)


def _hash(value) -> str:
    """The fingerprint of a register row (or of the whole register): its content, key order aside.
    "" when the content cannot be serialised - never an exception, never a made-up value."""
    try:
        text = json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":"), default=str)
    except (ValueError, TypeError, RecursionError):
        return ""
    return hashlib.sha256(text.encode("ascii")).hexdigest()


def _answers(root: Path, ids: set, vocab: dict) -> tuple:
    """(last question record per id, last case record per case id, skipped counts, file present, extras).
    A bad line is counted, never raised. A valid case record is not a skipped line. A file that EXISTS and cannot
    be read (a folder, no permission) is `unreadable_file: 1`: without it that case looked like an empty file.
    `extras` (FV1-9): `repeats` - every `repeat` record of an id in `ids`, `(id, record)` in file order, whether or not a later
    record replaced it (the retro's record); `notes` - {id: [every valid `note` record in file order]}. A `note` is neither a
    question record (it never wins an id) nor a skipped line."""
    skipped = {"broken_lines": 0, "non_object_lines": 0, "unknown_id": 0, "invalid": 0, "unreadable_file": 0}
    extras: dict = {"repeats": [], "notes": {}}
    path = root.joinpath(*ANSWERS_REL)
    try:
        text = path.read_bytes().decode("utf-8-sig", errors="replace")
    except FileNotFoundError:
        return {}, {}, skipped, False, extras
    except OSError:
        skipped["unreadable_file"] = 1
        return {}, {}, skipped, True, extras
    last: dict = {}
    cases: dict = {}
    for line in text.split("\n"):  # JSON escapes newlines inside a record, so "\n" is a boundary
        if not line.strip():
            continue
        try:
            rec = json.loads(line)
        except (ValueError, RecursionError):
            skipped["broken_lines"] += 1
            continue
        if not isinstance(rec, dict):
            skipped["non_object_lines"] += 1
            continue
        kind = rec.get("kind", "question")  # a record with no `kind` is a question record
        if kind == "case":
            case = rec.get("case")
            if not isinstance(case, str) or not case.strip() or rec.get("decision") not in vocab["case_decisions"]:
                skipped["invalid"] += 1
                continue
            cases[case.strip()] = rec
            continue
        rid = rec.get("id")
        if kind == "note":
            if not isinstance(rid, str) or not isinstance(rec.get("words"), str) or not rec["words"].strip():
                skipped["invalid"] += 1
            elif rid.strip() not in ids:
                skipped["unknown_id"] += 1
            else:
                extras["notes"].setdefault(rid.strip(), []).append(rec)
            continue
        if kind != "question" or not isinstance(rid, str) or rec.get("status") not in vocab["recorded_statuses"]:
            skipped["invalid"] += 1
            continue
        rid = rid.strip()
        if rid not in ids:
            skipped["unknown_id"] += 1
            continue
        last[rid] = rec
        if rec["status"] == REPEAT:
            extras["repeats"].append((rid, rec))
    return last, cases, skipped, True, extras


def _lines(text: str) -> list:
    return re.split(r"\r\n|\r|\n", text)


ID_BOUNDARY_BEFORE = r"(?<![\w/.#-])"      # the one whole-id boundary: planning_contract and gate_brief read it from here
ID_BOUNDARY_AFTER = r"(?![\w/.#-])"


def _mention(qid: str):
    """The id as a word: bounded by the line's ends, whitespace or punctuation - but not by a word
    character or by `/ . # -`. `Q1` is not in `Q10`, `Q-1`, `Q1-x`, `R-Q1`, `Q3.md`, `#Q4`,
    `Q5/other` or `http://x/browse/Q1`: an id inside a URL, a path or a file name is not the person
    naming the question. The direction of the error is toward not naming - except one place: a
    backslash right before the id (one or two of them, a markdown escape) is NOT in the excluded
    class, so it is a boundary, and the person named the question all the same. The class must not
    grow a backslash (test_question_register.py, edge 8, pins it beside `aQ1`, which is not found)."""
    return re.compile(ID_BOUNDARY_BEFORE + re.escape(qid) + ID_BOUNDARY_AFTER)


def _line_with(text: str, qid: str) -> str:
    pattern = _mention(qid)
    for line in _lines(text):
        if pattern.search(line):
            return line
    return ""


def _gate_words(root: Path) -> list:
    """[(where, words)] of the gates whose record holds the person's words, in gate order A, B."""
    try:
        pipeline = json.loads(root.joinpath("pipeline.json").read_bytes().decode("utf-8-sig", errors="replace"))
    except (OSError, ValueError, RecursionError):
        return []
    gates = pipeline.get("gates") if isinstance(pipeline, dict) else None
    out = []
    for key in ("A", "B"):
        record = gates.get(key) if isinstance(gates, dict) else None
        if not isinstance(record, dict):
            continue
        for field in GATE_WORD_KEYS:
            value = record.get(field)
            if isinstance(value, str) and value.strip():
                out.append((GATE_WHERE[key], value))
                break
    return out


def _merge(qid: str, row: dict, rec, gates=None, notes=None) -> dict:
    """One register row and the record that wins for it (None: no record) as the question `load` returns.

    The ONE place that says what a row's status, hash and `changed_since_answer` are: `load` merges the register
    on disk with it, `statuses_for` merges the rows of a file that is not on disk yet (a publish). `gates` is a
    callable giving the gate words, asked only for a row with no record; None means "do not look" (`named` is
    an open status all the same). `notes` (FV1-9) are the `note` records of this id in file order: the LAST one stored
    for the bytes of this row as they are TODAY becomes `note` ({words, by, at}); a note measured on other bytes never counts.
    The keys `_resolve_repeats` computes (`follows`, `repeat_problem`, `repeated_by`) and `note` are code's: a register row
    that carries a key of such a name does not keep it."""
    readings = row.get("readings")
    count = len(readings) if isinstance(readings, list) else 0
    question = dict(row)
    for computed in ("follows", "repeat_problem", "repeated_by", "note"):
        question.pop(computed, None)
    question.update({"id": qid, "status": "open", "reading": "", "words": "", "where": "", "at": "",
                     "line": "", "readings_count": count, "letters": LETTERS[:count],
                     "row_hash": _hash(row), "record_row_hash": "", "changed_since_answer": False})
    mine = [n for n in (notes or []) if n.get("row_hash") == question["row_hash"]]
    if mine:
        question["note"] = {"words": mine[-1]["words"], "by": str(mine[-1].get("by") or ""), "at": str(mine[-1].get("at") or "")}
    if rec is not None:
        words = rec.get("words") if isinstance(rec.get("words"), str) else ""
        stored = rec.get("row_hash")
        stored = stored if isinstance(stored, str) and stored else ""
        question.update({"status": rec["status"], "words": words, "line": _line_with(words, qid),
                         "where": str(rec.get("where") or ""), "at": str(rec.get("at") or ""),
                         "record_row_hash": stored,
                         "changed_since_answer": (stored != question["row_hash"]) if stored else None})
        if rec["status"] == REPEAT:      # what the declaration said (never the row's own keys: a row cannot declare a repeat)
            for key in ("same_as", "declared_by", "target_hash"):
                question[key] = rec.get(key)
        if rec["status"] == "answered":
            question["reading"] = str(rec.get("reading") or "")
            stamp = rec.get("before_from_thens")
            if isinstance(stamp, dict) and isinstance(stamp.get("cases"), list) and stamp["cases"]:
                question["before_from_thens"] = True     # RN1-11: `record` saw the cases write a real text for this letter
    elif gates is not None:
        for where, words in gates():
            line = _line_with(words, qid)
            if line:
                question.update({"status": "named", "words": words, "line": line, "where": where})
                break
    return question


def load(task_root) -> dict:
    """Every question of the register with its status. Never raises on the story's own data.

    Returns {"questions": [...], "register_present": bool, "register_hash": str,
             "answers_present": bool, "skipped": {...}, "problems": [str], "duplicates": [id],
             "case_decisions": {case id: {decision, words, where, by, at}}}.
    Each question is the register row plus: `status` (open | answered | not_needed |
    with_designer | deferred_to_report | named), `reading` (the letter, only when answered by one), `words`, `where`,
    `at`, `line` (the line of the words that carries the id, "" when none), `readings_count`,
    `letters`, `row_hash` (the fingerprint of this row TODAY - what a card passes back when the
    person answers), `record_row_hash` (the one stored with the winning record, "" when none) and
    `changed_since_answer`: True when the row today is not the row that record was shown; False
    when it is, or when there is no record; None when the record stores no hash. The status is what
    was recorded, the flag is the fact: the readers decide what a changed row means.
    `open` with a record behind it is a reopen: `words`/`where`/`at` are the reopening ones.
    `named` is computed per question that has NO record, whether or not an answers file exists.
    """
    root = Path(task_root)
    vocab = vocabulary()
    rows, problems, present, register_hash = _register(root)
    kept, duplicates, seen = [], [], set()
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            problems.append(f"open_questions[{index}] is {type(row).__name__}, not an object: skipped")
            continue
        qid = row.get("id")
        if not isinstance(qid, str) or not qid.strip():
            problems.append(f"open_questions[{index}] has no id: skipped (a question is addressed by its `id`)")
            continue
        qid = qid.strip()
        if qid in seen:
            duplicates.append(qid)
            problems.append(f"open_questions[{index}] repeats the id `{qid}`: the first one is kept, "
                            "this one is not merged (ids are unique - the S2 role must renumber it)")
            continue
        seen.add(qid)
        kept.append((qid, row))
    last, case_last, skipped, answers_present, extras = _answers(root, seen, vocab)
    gate_cache: list = []

    def gates() -> list:  # read once, and only when a question with no record asks for them
        if not gate_cache:
            gate_cache.append(_gate_words(root))
        return gate_cache[0]

    questions = [_merge(qid, row, last.get(qid), gates, extras["notes"].get(qid)) for qid, row in kept]
    _resolve_repeats(questions)
    decisions = {}
    for case, rec in case_last.items():
        decisions[case] = {"decision": rec["decision"], "words": rec.get("words") if isinstance(rec.get("words"), str) else "",
                           "where": str(rec.get("where") or ""), "by": str(rec.get("by") or ""),
                           "at": str(rec.get("at") or "")}
    return {"questions": questions, "register_present": present, "register_hash": register_hash,
            "answers_present": answers_present, "skipped": skipped, "problems": problems,
            "duplicates": duplicates, "case_decisions": decisions, "repeat_history": extras["repeats"]}


def _resolve_repeats(questions) -> None:
    """The one pass after merging (`load` and `statuses_for`; FV1-9): for each question whose status is `repeat`, walk `same_as`
    through the `repeat` rows to the first row that is not one. Found, and every hop's stored `target_hash` equals the row_hash
    of the hop's target: it gets `follows` (the id found), and - when it is hidden (`hidden_repeat`) - joins `repeated_by` of
    that target. Otherwise `follows` is "" and `repeat_problem` says why: `gone` (no such id, or no usable `same_as`), `cycle`
    (the walk met an id twice), `target_changed` (a hop's target is not the row the declaration saw, or the record stores no
    `target_hash`). Computed here, never stored. A question that is no object, or has no id, is left alone."""
    by_id: dict = {}
    resolved: dict = {}
    for q in questions:
        if isinstance(q, dict) and isinstance(q.get("id"), str):
            by_id.setdefault(q["id"], q)
    for q in questions:
        if not isinstance(q, dict) or q.get("status") != REPEAT or not isinstance(q.get("id"), str):
            continue
        found, problem, current, seen = "", "", q, {q.get("id")}
        while True:
            target_id = current.get("same_as")
            target = by_id.get(target_id.strip()) if isinstance(target_id, str) else None
            if target is None:
                problem = "gone"
            elif target["id"] in seen:
                problem = "cycle"
            elif not (isinstance(current.get("target_hash"), str) and current["target_hash"]
                      and current["target_hash"] == target.get("row_hash")):
                problem = "target_changed"
            if problem:
                break
            seen.add(target["id"])
            if target.get("status") != REPEAT:
                found = target["id"]
                break
            current = target
        q["follows"], q["repeat_problem"] = found, problem
        resolved[q["id"]] = found
    for q in questions:
        if isinstance(q, dict) and q.get("id") in resolved and hidden_repeat(q):
            by_id[resolved[q["id"]]].setdefault("repeated_by", []).append(q["id"])


def hidden_repeat(question) -> bool:
    """Is this question a declared repeat that the person is not asked, because it asks what its target asks (FV1-9)? The ONE reader of
    that fact (AR-13): `is_open`, `still_open`, the report, the brief and the rehearsal all ask this. True only for status `repeat`
    whose chain was resolved by `_resolve_repeats` (`follows` set, no `repeat_problem`) AND whose own row is the one declared
    (`changed_since_answer is False`: a record with no stored hash proves nothing about the bytes). The ERROR DIRECTION is "shown":
    a missing key, a dict built outside `load`, a gone or changed target, a cycle, a changed row are all not hidden."""
    return (isinstance(question, dict) and question.get("status") == REPEAT and bool(question.get("follows"))
            and not question.get("repeat_problem") and question.get("changed_since_answer") is False)


# --------------------------------------------------------------------------------------------
# the words the readers share (AR-13): settled, open, a blocker, the key of an answer
# --------------------------------------------------------------------------------------------

def _contract():
    """`contract`, imported when a predicate first needs it: reading and answering call nothing else in the
    factory at import time, and `contract` must be free to import this module."""
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    import contract as C
    return C


def _person_words():
    """`person_words` (the one reader of words from a file and the one renderer of the command that records them)."""
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    import person_words
    return person_words


def _holds(question: dict) -> bool:
    """Does the record behind this question still stand? Not when the row is not the one the person saw
    (`changed_since_answer is True`), and not when they chose `before` and nobody wrote that value down
    (`contract.before_value_needed`, the test gate A and the resolver already share). A record that stores no
    hash (`None`) holds, as at gate A: only a hash that DIFFERS is a change."""
    return question.get("changed_since_answer") is not True and not _contract().before_value_needed(question)


def settled(question) -> bool:
    """Has the person settled this question on the bytes they saw? `answered` or `not_needed` AND the record
    holds. `deferred_to_report` is not settled (it is kept open); neither is `with_designer`. The answer to
    every "may the plan follow it", "may the exit say ready", "is a different answer a change" asks this."""
    return isinstance(question, dict) and question.get("status") in SETTLED_STATUSES and _holds(question)


def row_answered(row) -> bool:
    """Does this readiness row itself carry an answer (`answer` / `answered` / `resolution`, non-blank)? The ONE own-answer test
    (AR-13) gate A and the gate brief's open list share; a row that is no object is not answered (toward asking)."""
    return isinstance(row, dict) and any(str(row.get(key) or "").strip() for key in ("answer", "answered", "resolution"))


def matches(rows, view) -> list:
    """The register question (`load`'s shape, from `view`) each of `rows` is, in order: the ONE place the first-row-of-an-id rule
    lives (AR-13). The register keeps the FIRST row of an id and its answer belongs to that row, so only the first row of an id
    in `rows` is matched (by the id stripped of surrounding whitespace, then exactly and case-sensitively, as `load` keys it); a later row of the same id, a row with no usable id, a row
    that is no object, an id the register does not hold and a `view` that is None (a register nobody could read) give None -
    the caller judges such a row as it stands (FR-41, FR-59: the error goes toward asking). Callers ask `settled` of the match."""
    by_id = {str(q.get("id")): q for q in ((view or {}).get("questions") or []) if isinstance(q, dict)}
    out, seen = [], set()
    for row in rows or []:
        qid = row.get("id").strip() if isinstance(row, dict) and isinstance(row.get("id"), str) else ""
        out.append(by_id.get(qid) if qid and qid not in seen else None)
        if qid:
            seen.add(qid)
    return out


def closes(question) -> bool:
    """Does the person's answer to this register question CLOSE a card that rests on it? `settled` (the one definition of
    settled, AR-13) AND the answer is on the exact bytes of the row it was given on (`changed_since_answer is False`: a
    record that stores no readable hash proves nothing about which text was answered) AND the record says when. This is
    `settled` in a new, GATING role - "do not ask" - so the error direction is only toward asking (FR-41, H41): a
    deferred, `with_designer`, changed, unhashed or undated answer does not close."""
    return (isinstance(question, dict) and settled(question) and question.get("changed_since_answer") is False
            and bool(str(question.get("at") or "").strip()))


def answer_text(item) -> tuple:
    """`(text, is_words)`: the ONE rendering of an `answers_for_brief` item as text, squeezed to one line and NEVER cut (the
    caller decides any clip and says so). `not needed`; else the chosen reading's text; else the person's own words
    (`is_words` True; a leading copy of the answered id is dropped); else `reading <letter>`; else `""` (nothing recorded)."""
    item = item if isinstance(item, dict) else {}
    if item.get("status") == "not_needed":
        return "not needed", False
    reading_text = " ".join(str(item.get("reading_text") or "").split())
    if item.get("reading") and reading_text:
        return reading_text, False
    words = str(item.get("words") or "")
    qid = str(item.get("id") or "")
    if qid and words.startswith(qid) and not words[len(qid):len(qid) + 1].isalnum():
        words = words[len(qid):].lstrip(" :,.-")      # the words typed start with the id answered
    words = " ".join(words.split())
    if words:
        return words, True
    return (f"reading {item['reading']}" if item.get("reading") else ""), False


def is_open(question) -> bool:
    """Is this question one the factory asks (again)? `open` / `named`, a record whose row changed since or whose
    `before` value is missing (answered, not needed or deferred alike), and anything it cannot read - a missing
    or unknown status, a row that is no object. The ERROR DIRECTION is "open" (FR-59): only `with_designer`
    (it has an owner), a settled question and a deferred one whose record holds are not open."""
    if not isinstance(question, dict):
        return True
    status = question.get("status")
    if status == "with_designer":
        return False
    if status in SETTLED_STATUSES + (DEFERRED,):
        return not _holds(question)
    if status == REPEAT:
        return not hidden_repeat(question)     # FV1-9: a declared repeat that stands is not asked; anything unresolved is
    return True


def open_blocker(question) -> bool:
    """Is this an open question that blocks? Open by `is_open`, and `severity` anything but `major` / `minor`:
    a missing severity, `Blocker`, `critical` and a row that is no object block (the error goes toward asking)."""
    if not isinstance(question, dict):
        return True
    return is_open(question) and question.get("severity") not in NOT_BLOCKING


def driver_owned(question) -> bool:
    """Is this a role's question (`asked_by`) with NO person class (`why_person`)? Such a row belongs to the conductor (it settles it from
    the files or leaves it as a gap in the run's notes): it is never listed to a person at a gate (t-1815 F2, E-B7 "a question with no
    class never reaches a person"). A row that is no object, a question of the readiness file (no `asked_by`) and a role question
    WITH a class are not driver-owned: the error direction is toward asking."""
    return isinstance(question, dict) and bool(question.get("asked_by")) and not question.get("why_person")


def answer_key(question):
    """The key a settled question's answer has in a plan row's `if_answered` and a case's `question_thens`:
    the reading letter, or `not_needed`; None when the question is not settled or was answered in words only."""
    if not settled(question):
        return None
    if question.get("status") == "not_needed":
        return "not_needed"
    return str(question.get("reading") or "") or None


def statuses_for(task_root, rows) -> list:
    """The merged question (`load`'s shape) of each row of `rows`, in order: the rows of a register that is NOT on
    disk yet (a publish), read against the answers file by the row's id and fingerprinted from the row HERE,
    so `changed_since_answer` is the data's, not the disk's. A row that is no object gives None (`open_blocker`
    reads it as blocking); a row with no usable id has no record and is `open`. An unreadable file gives every
    row as open. Never raises on the story's data."""
    root = Path(task_root)
    ids = {r["id"].strip() for r in rows if isinstance(r, dict) and isinstance(r.get("id"), str) and r["id"].strip()}
    last, _cases, _skipped, _present, extras = _answers(root, ids, vocabulary())
    out = []
    for row in rows:
        if not isinstance(row, dict):
            out.append(None)
            continue
        qid = row["id"].strip() if isinstance(row.get("id"), str) else ""
        out.append(_merge(qid, row, last.get(qid) if qid else None, notes=extras["notes"].get(qid) if qid else None))
    _resolve_repeats(out)
    return out


class _EveryId:
    """A set that holds every id: `_answers` keeps the records of ids the register does not hold."""

    def __contains__(self, item) -> bool:
        return True


def readiness_drift(task_root) -> list:
    """One problem (T6) per question that has a settled or deferred record in the answers file and no row in
    `work/requirements-readiness.json`: an answered question stays in the register with its id, so a role that
    drops the row (or renumbers it) loses the thing the person said. [] with no answers file, with no register
    to compare to, and when the register cannot be read (an unreadable register is its own finding). Never raises."""
    root = Path(task_root)
    rows, problems, present, _hash_of = _register(root)
    if problems or not present:
        return []
    last, _cases, _skipped, _present, _extras = _answers(root, _EveryId(), vocabulary())
    held = {r["id"].strip() for r in rows if isinstance(r, dict) and isinstance(r.get("id"), str)}
    out = []
    for qid, rec in last.items():
        if qid in held or rec["status"] not in SETTLED_STATUSES + (DEFERRED,):
            continue
        if rec["status"] == "not_needed":
            said = "not needed"
        elif rec["status"] == DEFERRED:
            said = UNTIL_THE_REPORT
        else:
            said = str(rec.get("reading") or "") or "in the person's own words"
        out.append(f"{qid} has an answer recorded at {rec.get('where') or 'an unrecorded place'} ({said}) but is missing "
                   "from open_questions: an answered question stays in the register with its id. Expected: restore the "
                   "row as it was; the factory reads its status from the answers file.")
    return out


# --------------------------------------------------------------------------------------------
# the strict parser
# --------------------------------------------------------------------------------------------

_NUMBERED = re.compile(r"[0-9]{1,4}[.)][ \t\xa0]")
# `<id>`, optional markdown emphasis closing the id (`**Q1**: a`), spaces, `:` or `=`, the value.
_TOKEN = re.compile(r"(?P<id>[^\s:=*`]{1,64})[*`]*[ \t\xa0]*[:=][ \t\xa0]*(?P<value>.*)", re.DOTALL)
# The value is the WHOLE rest of the line: after it only spaces, at most one of `. , ;`, spaces.
# A letter followed by a word ("Q1: a question for later"), a second value ("a, b"), prose
# ("a, but only if...") or another token ("a; Q2: b") is NOT a choice.
_TAIL = r"(?:[ \t\xa0]*[.,;])?[ \t\xa0]*"
_QUESTION_VALUE = re.compile(r"(?P<value>[a-z]|not needed|" + re.escape(UNTIL_THE_REPORT) + r")" + _TAIL)
# `accept as blocked` (O6): the stand cards of gate A offer it per case, and it is read ONLY as this whole
# line - never as a substring of prose ("TC_014: do not accept as blocked" is no token). It is read here
# and executed by `planning_contract.apply_gate_answers`; it is not a `case_decisions` value of the
# register (that list holds what `record_case` may write).
BLOCKED_DECISION = "accept as blocked"
_CASE_DECISION = re.compile(r"(?P<value>manual|automate|" + re.escape(BLOCKED_DECISION) + r")" + _TAIL)


def _is_fence(line: str) -> bool:
    return line.lstrip(SPACES).startswith("```")


def _content(line: str) -> str:
    """The line without its list marker and markdown emphasis: leading spaces, `-`, `*`, a bullet
    character, backticks and `1. ` / `1) `, trailing spaces, `*` and backticks. One pass over
    indexes, so a 200 KB line of `- - - -` costs one scan, not one slice per marker."""
    skip = SPACES + "-*`" + BULLETS
    i, n = 0, len(line)
    while i < n:
        if line[i] in skip:
            i += 1
            continue
        numbered = _NUMBERED.match(line, i)
        if numbered:
            i = numbered.end()
            continue
        break
    return line[i:].rstrip(SPACES + "\r*`")


def _question_value(value: str):
    """The letter, "not needed" or "until the report" the value spells in the strict form, else None."""
    found = _QUESTION_VALUE.fullmatch(value)
    return found.group("value") if found else None


FENCED_NOTICE = "a decision inside a code block is not read: {line}"
MAX_NOTICE_LINE = 160


def is_case_decision(value: str) -> bool:
    """Is `value` (the text after `<case id>:`) one of the case decisions `manual` | `automate` | `accept as blocked`, in the
    strict form `parse_choices` reads? The one reader for a caller outside the register (GW1-33 F7, AR-13)."""
    return _CASE_DECISION.fullmatch(str(value or "").strip(SPACES + "`*")) is not None


def _decision_shaped(content: str, readings: dict) -> bool:
    """Would this (marker-stripped) line be a decision token outside a fence? A register id with a letter or
    `not needed`, or any id with a case decision (`manual` | `automate` | `accept as blocked`). Shape only: the
    notice must not need to know the story's case ids."""
    found = _TOKEN.fullmatch(content)
    if not found:
        return False
    ident, value = found.group("id"), found.group("value")
    if ident in readings:
        return _question_value(value) is not None
    return _CASE_DECISION.fullmatch(value) is not None


def fence_notices(parsed) -> list:
    """The one line per decision `parse_choices` found inside a fenced block (`parsed["fenced"]`), for the caller to
    print next to the lines it prints for what it did apply: `a decision inside a code block is not read: <line>`.
    [] for a parse that found none. A very long line is cut for the notice only; the words are never altered."""
    out = []
    for line in (parsed or {}).get("fenced") or []:
        shown = line if len(line) <= MAX_NOTICE_LINE else line[:MAX_NOTICE_LINE - 3] + "..."
        out.append(FENCED_NOTICE.format(line=shown))
    return out


def _fence_walk(words):
    """THE walk of the person's words that every reader of a token shares (F-10): `(raw line, inside a fence)` for every line that is not
    itself a fence line. A BOM is the file's, not a line's content; a fence never closed swallows what follows."""
    text = words if isinstance(words, str) else ("" if words is None else str(words))
    in_fence = False
    for raw in _lines(text[1:] if text[:1] == BOM else text):
        if _is_fence(raw):
            in_fence = not in_fence
            continue
        yield raw, in_fence


def _quoted(raw: str) -> bool:
    """A quoted line (`>` first, before or after a list marker) is never a token."""
    return raw.lstrip(SPACES).startswith(">") or _content(raw).startswith(">")


def _plain_lines(words):
    """`(raw, content)` of the lines outside every fence and every quote: where a token can stand."""
    for raw, in_fence in _fence_walk(words):
        if not in_fence and not _quoted(raw):
            yield raw, _content(raw)


def parse_choices(words, questions, case_ids) -> dict:
    """Read the person's words for closed tokens. The words are never altered or shortened.

    `questions` are the register rows (`load()["questions"]`: each needs `id` and `readings`);
    `case_ids` are the FULL case ids of this story. A token is a WHOLE line: it starts with the id
    (after a list marker and markdown emphasis) and ends with the value - `<qid>: <letter>` (`=`
    also), `<qid>: not needed`, `<qid>: until the report`, `<case id>: manual|automate|accept as blocked` - followed by nothing but
    spaces and at most one of `. , ;`. Lines inside a fenced block (between two lines that start with three
    backticks) and quoted lines (starting with `>`) are never tokens. A short case id (`TC_009`)
    resolves only when exactly one of `case_ids` ends with `_` + it. Returns
      choices            {qid: letter}
      not_needed         [qid]
      deferred           [qid]  `<qid>: until the report`: kept open on the person's word (neither a choice nor untokened)
      case_tokens       [{"case": full id, "decision": "manual"|"automate"|"accept as blocked",
                           "written": id as typed}]
      conflicts          [{"id": qid or case id, "values": [...]}]  nothing is chosen for these
      unknown_ids        [id as typed]  looks like `<id-with-a-digit>: <token>` but is no register id
      out_of_range       [{"id", "letter", "readings"}]  the letter is beyond the question's readings
      untokened_questions[qid]  every register question with neither a choice nor `not needed`
                                (conflicts and out-of-range ones included: they stay with the conductor)
      unresolved_short_ids [{"id", "candidates": [full ids]}]
      fenced             [line]  decision-shaped lines inside a fenced block (or after a fence that is never
                         closed): applied to nothing; `fence_notices` turns them into the one line each
                         caller prints
    Error direction: it may fail to see a choice; it never returns one the person did not write
    as a whole-line token.
    """
    readings, order = {}, []
    for question in questions or []:
        qid = question.get("id") if isinstance(question, dict) else None
        qid = qid.strip() if isinstance(qid, str) else ""
        if qid and qid not in readings:
            listed = question.get("readings")
            readings[qid] = len(listed) if isinstance(listed, list) else 0
            order.append(qid)
    fulls = list(dict.fromkeys(str(c).strip() for c in (case_ids or []) if str(c).strip()))
    full_set = set(fulls)
    said: dict = {}       # qid -> [values in order seen]
    case_said: dict = {}  # full case id -> [decisions]
    written: dict = {}    # full case id -> the id as first typed
    unknown, unresolved, fenced = [], [], []
    for raw, in_fence in _fence_walk(words):    # the fence lines are never tokens, and what stands between them either
        if in_fence:
            # t-269 F6: a line that WOULD be a decision outside the fence is reported, never applied: the
            # person is told it was not read instead of finding the answer silently missing. A fence that
            # is never closed swallows everything after it - the same line, said the same way.
            line = raw.strip()
            if _decision_shaped(_content(raw), readings) and line not in fenced:
                fenced.append(line)
            continue
        if _quoted(raw):
            continue
        content = _content(raw)
        found = _TOKEN.fullmatch(content)
        if not found:
            continue
        ident, value = found.group("id"), found.group("value")
        if ident in readings:  # a register id takes only question tokens, never a case one
            spoken = _question_value(value)
            if spoken is not None:
                said.setdefault(ident, []).append(spoken)
            continue
        decision = _CASE_DECISION.fullmatch(value)
        if decision:
            if ident in full_set:
                full = ident
            else:
                candidates = [c for c in fulls if c.endswith("_" + ident)]
                if len(candidates) != 1:
                    if not any(u["id"] == ident for u in unresolved):
                        unresolved.append({"id": ident, "candidates": candidates})
                    continue
                full = candidates[0]
            case_said.setdefault(full, []).append(decision.group("value"))
            written.setdefault(full, ident)
            continue
        if _question_value(value) is not None and re.search(r"[0-9]", ident) and ident not in unknown:
            unknown.append(ident)
    out = {"choices": {}, "not_needed": [], "deferred": [], "case_tokens": [], "conflicts": [], "unknown_ids": unknown,
           "out_of_range": [], "untokened_questions": [], "unresolved_short_ids": unresolved, "fenced": fenced}
    for qid in order:
        values = list(dict.fromkeys(said.get(qid, [])))
        if not values:
            out["untokened_questions"].append(qid)
        elif len(values) > 1:
            out["conflicts"].append({"id": qid, "values": values})
            out["untokened_questions"].append(qid)
        elif values[0] == "not needed":
            out["not_needed"].append(qid)
        elif values[0] == UNTIL_THE_REPORT:
            out["deferred"].append(qid)
        elif LETTERS.index(values[0]) >= readings[qid]:
            out["out_of_range"].append({"id": qid, "letter": values[0], "readings": readings[qid]})
            out["untokened_questions"].append(qid)
        else:
            out["choices"][qid] = values[0]
    for full, decisions in case_said.items():
        values = list(dict.fromkeys(decisions))
        if len(values) > 1:
            out["conflicts"].append({"id": full, "values": values})
        else:
            out["case_tokens"].append({"case": full, "decision": values[0], "written": written[full]})
    return out


# The line the driver puts between a second answer at a gate and the first one (`Driver.EARLIER_ANSWER`, story_run.py): what stands
# after it is an answer the person has since replaced, so no reader of the CURRENT answer takes a word from it.
EARLIER_ANSWER_MARK = "\n\nEarlier answer at this gate:\n"


def risk_reason_of(words) -> dict:
    """The person's decision to deliver over a verdict that is not `yes`, read from their gate B words (HF8-23): `{"found": bool,
    "reason": str, "conflict": bool}`. The word is the vocabulary's `risk_word` (`deliver with known gaps`); a token is a WHOLE line
    outside fences and quotes (the lines, the fence and the markers are `parse_choices`' own helpers), the word alone or followed by
    `:` and the reason (the reason as written, only its outer blanks cut). Case is not read; the answer's `Earlier answer at this gate:`
    tail is not read. `found` with an empty `reason` is a token that gave no reason (the caller refuses it: a reason is never invented);
    two tokens with different reasons are a `conflict`: nothing is returned as the reason.
    ERROR DIRECTION: it may miss the word; it never returns a yes for words that did not say it. Not found, each: `do not deliver with
    known gaps`, `deliver with known gaps?`, `deliver with known gaps later: x`, `Bug 1: deliver with known gaps`, a quoted line, a
    line inside a fence, the word in the middle of a sentence. A vocabulary with no `risk_word` finds nothing (FR-59: no word, no yes)."""
    word = vocabulary().get("risk_word")
    word = word.strip().casefold() if isinstance(word, str) else ""
    text = words if isinstance(words, str) else ("" if words is None else str(words))
    text = text.split(EARLIER_ANSWER_MARK, 1)[0]
    if not word:
        return {"found": False, "reason": "", "conflict": False}
    reasons = []
    for _raw, content in _plain_lines(text):
        if content[:len(word)].casefold() != word:
            continue
        rest = content[len(word):].lstrip(SPACES)
        if rest and not rest.startswith(":"):
            continue            # `deliver with known gaps later`, `...?`: another sentence, not the word
        reason = rest[1:].strip(SPACES + "\r")
        if reason not in reasons:
            reasons.append(reason)
    if not reasons:
        return {"found": False, "reason": "", "conflict": False}
    if len(reasons) > 1:
        return {"found": True, "reason": "", "conflict": True}
    return {"found": True, "reason": reasons[0], "conflict": False}


# --------------------------------------------------------------------------------------------
# writing
# --------------------------------------------------------------------------------------------

def _valid_ids(view: dict) -> str:
    ids = [q["id"] for q in view["questions"]]
    if ids:
        return "Register ids (exact, case-sensitive; aliases such as Q-1 or Q-R14 are not ids): " + ", ".join(ids)
    if not view["register_present"]:
        return "The story has no work/requirements-readiness.json, so it has no register ids yet"
    return "The register holds no readable question"


@contextlib.contextmanager
def answers_lock(task_root, wait: float = LOCK_WAIT_SECONDS):
    """Hold the answers file's writer lock: two writers never interleave a line.

    The package's own `EventStore.lock` was not reused: it fails at once when another writer holds
    it (an answer would be refused instead of waiting), it creates `state/` and takes `events.lock`
    - the controller's lock for its own commits, so an answer would collide with a running
    controller. This is the package's one file lock (`event_store.take_file_lock`: one byte of a lock
    file, released when the process dies, so no stale lock) on a file of its own, retried until `wait`
    seconds. The file is in the story's tracked work folder: no holder is recorded in it."""
    path = Path(task_root).joinpath(*ANSWERS_REL)
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    from event_store import LockBroken, LockBusy, take_file_lock
    try:
        held = take_file_lock(path.parent / LOCK_NAME, wait, record_holder=False, poll_s=0.02)
    except LockBusy as exc:
        raise Refused(f"- another writer has held {path} for {wait:g} s: nothing was written. "
                      "Expected: try again in a moment; " + exc.holder_clause) from exc
    except LockBroken as exc:
        raise Refused("- " + str(exc) + " Expected: the file must be writable") from exc
    try:
        yield
    finally:
        held.release()


def _append(root: Path, rec: dict) -> None:
    """Append ONE record line under the writer lock. The words are stored whole (FR-8)."""
    try:
        data = json.dumps(rec, ensure_ascii=False).encode("utf-8")
    except UnicodeEncodeError:  # a lone surrogate from a terminal: escape it rather than lose the answer
        data = json.dumps(rec, ensure_ascii=True).encode("ascii")
    path = root.joinpath(*ANSWERS_REL)
    with answers_lock(root):
        lead = b""
        if path.is_file() and path.stat().st_size:
            with path.open("rb") as handle:  # a crash may have left a line without its newline
                handle.seek(-1, 2)
                if handle.read(1) != b"\n":
                    lead = b"\n"
        with path.open("ab") as handle:
            handle.write(lead + data + b"\n")


def _common_problems(vocab: dict, words, where, by) -> list:
    problems = []
    if not isinstance(words, str) or not words.strip():
        problems.append("the words are blank. Expected the person's own words, whole, so the answer "
                        "stays attributable (pass them with --words or --words-file)")
    for value, key, flag, what in ((where, "where", "--where", "where it was asked"),
                                   (by, "by", "--by", "who recorded it")):
        if not value:
            problems.append(f"{flag} is missing: say {what} (there is no default). Valid: " + ", ".join(vocab[key]))
        elif value not in vocab[key]:
            problems.append(f"{key} {value!r} is not a known value. Valid: " + ", ".join(vocab[key]))
    return problems


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()) + "+00:00"


def _different_answer_text(row: dict, qid: str) -> str:
    """The refusal of a DIFFERENT answer on a settled question, with its `--reopen` door: the ONE text (`record` refuses with it, and
    the answer of a gate decision names it in `unread`, AR-13)."""
    said = ("not needed" if row["status"] == "not_needed"
            else f"reading {row['reading']}" if row["reading"] else "answered in words")
    return (f"{qid} is already settled ({said}, at {row['where'] or 'an unrecorded place'} {row['at']}): "
            "a different answer is not recorded over it. Expected: if the person changed their answer, "
            "reopen it first (" + _person_words().door(f"{COMMAND} --task <T> --reopen {qid}")
            + " --where ... --by ...), then record the new answer; the plan rows that followed the "
            "first answer are reworked")


def record(task_root, qid, status, words, where, by, shown_hash, reading="", at=None, *,
           same_as=None, declared_by=None, target_hash=None, stage=None, texts=None) -> dict:
    """Append ONE answer record and return it. Raises `Refused` (text: what is wrong, what was
    expected, the valid values) and writes nothing when any argument is unusable.

    `shown_hash` is the `row_hash` of the question AS IT WAS SHOWN to the person (`load()` /
    `--show` print it). It is stored as given; the current hash is never stamped in its place - a
    register that changed between showing and answering must stay visible (`changed_since_answer`).
    It is required for every status except `open` (a reopen); pass "" there. `where` and `by` have
    no default. The words are stored exactly as given (CRLF, BOM, any script): FR-8.

    A DIFFERENT answer (another status or letter) on a question that is `settled` is refused (H6): `load` takes
    the last record and the plan follows the first, so a second answer would split them. `--reopen` (status
    `open`) is the door; the same answer again (another hash, other words) is appended as it always was; an
    answer on a question that is not settled - deferred, `with_designer`, or one whose row changed since - is
    written.

    FV1-9: status `repeat` is written by `declare_repeat` only; its keyword fields `same_as`, `declared_by`, `target_hash`,
    `stage` and `texts` ({question, same_as_question}: both texts as they stood) are stored on a `repeat` record and on no other."""
    root = Path(task_root)
    vocab = vocabulary()
    view = load(root)
    problems = []
    wanted = qid.strip() if isinstance(qid, str) else ""
    row = next((q for q in view["questions"] if q["id"] == wanted), None)
    if row is None:
        problems.append(f"no question with id {qid!r}. {_valid_ids(view)}")
    elif status != "open" and status in vocab["recorded_statuses"] and settled(row) \
            and (status, reading or "") != (row["status"], row["reading"]):
        problems.append(_different_answer_text(row, wanted))
    if status not in vocab["recorded_statuses"]:
        problems.append(f"status {status!r} cannot be recorded. Valid: " + ", ".join(vocab["recorded_statuses"]))
    problems.extend(_common_problems(vocab, words, where, by))
    shown = shown_hash if isinstance(shown_hash, str) else ""
    if shown and not HASH_TEXT.fullmatch(shown):
        problems.append(f"the register hash {shown!r} is not a sha256 (64 lower-case hex digits). Expected the "
                        "`row_hash` that --show printed for this question")
    elif not shown and status != "open":
        problems.append("the register hash is missing. Expected the `row_hash` that --show printed for this "
                        "question when the person was shown it (--register-hash): without it a register that "
                        "changed before the answer cannot be seen")
    if reading:
        if status != "answered":
            problems.append(f"a reading letter goes only with an answer, not with status {status!r}")
        elif not (isinstance(reading, str) and re.fullmatch(r"[a-z]", reading)):
            problems.append(f"reading {reading!r} is not one Latin letter a-z (a Cyrillic look-alike or "
                            "an uppercase letter is not one)")
        elif row is not None and LETTERS.index(reading) >= row["readings_count"]:
            valid = ", ".join(row["letters"]) if row["letters"] else "none - the question has no readings; answer in words"
            problems.append(f"reading {reading!r} is beyond the {row['readings_count']} readings of "
                            f"{row['id']}. Valid: {valid}")
    if problems:
        raise Refused("\n".join(f"- {p}" for p in problems))
    rec = {"kind": "question", "id": wanted, "status": status}
    if reading:
        rec["reading"] = reading
    rec.update({"words": words, "by": by, "where": where, "at": at or _now()})
    if shown:
        rec["row_hash"] = shown
    if status == REPEAT:
        rec.update({k: v for k, v in (("same_as", same_as), ("declared_by", declared_by), ("target_hash", target_hash),
                                      ("stage", stage), ("texts", texts)) if v not in (None, "")})
    stamp = _before_from_thens(root, row, status, reading)
    if stamp:
        rec["before_from_thens"] = {"cases": stamp}
    _append(root, rec)
    return rec


def _before_from_thens(root: Path, row, status: str, reading: str) -> list:
    """RN1-11 (the ONE writer of the stamp, AR-14): the sorted ids of the cases whose Thens carry the text of `reading`, when
    the answer is the before/now question's "before" letter, the question's own `before` value is empty or `unknown`, and AT
    LEAST ONE case entry exists whose every Then text for that letter is a real one (not empty, not `unknown`). [] otherwise
    - an empty text asserts nothing and never stands as an expected value (E-A2), and a case that cannot be read gives no
    stamp and never an exception (E-A3). The stamp is measured on the case bytes of THIS record: a later record recomputes it."""
    try:
        contract = _contract()
        if status != "answered" or not isinstance(row, dict) or not reading:
            return []
        before = row.get("before")
        if not isinstance(before, dict) or str(before.get("value") or "").strip().lower() not in ("", contract.CLAIM_UNKNOWN):
            return []
        if reading != contract._claim_letter(row, contract.CLAIM_KEYS[1]):
            return []
        import gate_brief
        cases, problems = gate_brief.story_cases(root)
        if problems:  # a case that could not be read may have said `unknown` (AR-28): no stamp
            return []
        found = []
        for cid, case in cases.items():
            entries = [e for e in (case.get("thens") or []) if isinstance(e, dict) and str(e.get("question") or "").strip() == row["id"]]
            for entry in entries:
                text = contract.question_then_text(row, entry, reading)[0]
                if not isinstance(text, str) or text.strip().lower() in ("", contract.CLAIM_UNKNOWN):
                    return []
            if entries:
                found.append(str(cid))
        return sorted(found)
    except Exception:
        return []


def _only_tokens(words, token_ids) -> bool:
    """Is EVERY non-blank line of `words` one token of a question in `token_ids`? A line in or after a fence, a
    quoted line, prose, a case word, an id the register does not hold and a blank-only text are not."""
    text = words if isinstance(words, str) else ""
    if text[:1] == BOM:
        text = text[1:]
    seen = False
    for raw in _lines(text):
        if not raw.strip():
            continue
        content = _content(raw)
        found = _TOKEN.fullmatch(content)
        if (_is_fence(raw) or raw.lstrip(SPACES).startswith(">") or content.startswith(">") or not found
                or found.group("id") not in token_ids or _question_value(found.group("value")) is None):
            return False
        seen = True
    return seen


def record_answers(task_root, words, where, by, shown=None, case_ids=None) -> dict:
    """The ONE move that turns a person's words into answer records: read the closed tokens of `words` against
    EVERY question of the register (an id that is not in it is an unknown id, never a guess), and write what they
    say. Returns {"recorded": ["Q1: b", "Q2: not needed"], "unread": [text], "unknown_ids": [id as typed],
    "deferred": [qid], "all_tokens": bool, "fenced": [line]}.

    `shown` is {qid: row_hash as it was shown}; an id it does not name is stamped with the row's hash today (what
    `--show` prints). The rule per id: a question that is not settled (open, named, `with_designer`, deferred, or
    one whose row changed since the answer) takes the answer; the SAME answer on the same bytes as the record
    already holds is skipped - repeating words writes nothing (H6b); a DIFFERENT answer on a settled id is the
    `record` refusal, said in `unread` (H6); two different answers for one id write neither (H5); a record
    another writer holds for more than 30 s is a line in `unread`, the question stays open (H18). `all_tokens`
    is true only when there is at least one token, every non-blank line is a question token, and nothing is
    left in `unread`, `unknown_ids` or `fenced`: then no word is left for a role to read (C14). The words
    themselves are stored whole with each record (FR-8)."""
    root = Path(task_root)
    rows = load(root)["questions"]
    by_id = {q["id"]: q for q in rows}
    parsed = parse_choices(words, rows, case_ids or [])
    shown = shown if isinstance(shown, dict) else {}
    todo = [(qid, "answered", letter) for qid, letter in parsed["choices"].items()]
    todo += [(qid, "not_needed", "") for qid in parsed["not_needed"]]
    todo += [(qid, DEFERRED, "") for qid in parsed["deferred"]]
    out = {"recorded": [], "unread": [], "unknown_ids": list(parsed["unknown_ids"]), "deferred": [],
           "all_tokens": False, "fenced": list(parsed["fenced"])}
    for qid, status, letter in todo:
        row = by_id[qid]
        stamp = shown.get(qid) if isinstance(shown.get(qid), str) and shown.get(qid) else row["row_hash"]
        same = (status, letter) == (row["status"], row["reading"]) and row["record_row_hash"] == stamp
        if same and not is_open(row):
            continue
        try:
            record(root, qid, status, words, where, by, stamp, reading=letter)
        except Refused as exc:
            out["unread"].append(" ".join(str(exc).split()).removeprefix("- "))
            continue
        if status == DEFERRED:
            out["deferred"].append(qid)
        else:
            out["recorded"].append(f"{qid}: {letter or 'not needed'}")
    out["unread"] += [f"{c['id']} (two different answers: {', '.join(c['values'])})" for c in parsed["conflicts"]
                      if c["id"] in by_id]
    out["unread"] += [f"{o['id']} (the letter {o['letter']} is beyond its {o['readings']} readings)"
                      for o in parsed["out_of_range"]]
    token_ids = set(parsed["choices"]) | set(parsed["not_needed"]) | set(parsed["deferred"])
    out["all_tokens"] = (_only_tokens(words, token_ids) and not out["unread"] and not out["unknown_ids"]
                         and not out["fenced"])
    return out


def _shown_line(line: str) -> str:
    """One line of the person's words for a view: squeezed, cut at `MAX_NOTICE_LINE` with the cut shown."""
    line = " ".join(str(line).split())
    return line if len(line) <= MAX_NOTICE_LINE else line[:MAX_NOTICE_LINE - 3] + "..."


# GW1-42: the value of a line `_stray_lines` returned, read for a HINT: one letter right after the colon, then not a word (`a question`
# is a word, `apple` too) and not a second value (`a, b`, `a / b`). A hint for the conductor's closed question, never a record.
_NEAR = re.compile(r"(?P<value>[a-z])(?![A-Za-z0-9])(?![ \t\xa0]*[,;/][ \t\xa0]*[a-z](?![A-Za-z0-9]))")


def near_answer(value, letters):
    """The one letter a stray line (`Q1: a (see the ticket)`) seems to answer with, or None. `value` is `_TOKEN`'s value of a line
    `_stray_lines` returned; `letters` are the question's readings (`load()` row `letters`). A letter outside them, two values, a
    word that only starts with a letter, an empty or non-text value: None. A HINT for the conductor to confirm with the person in
    a closed question (P22); the code never records it as a choice (FR-12, `parse_choices` stays strict)."""
    found = _NEAR.match(value) if isinstance(value, str) else None
    letter = found.group("value") if found else None
    return letter if letter and letter in (letters or "") else None


def _token_outcomes(tokens: list, now_rows: dict, before_rows: dict) -> tuple:
    """`(recorded, already, unread)` of the read tokens `(qid, status, letter, line)`: what THIS call settled, what was settled before with the
    same answer, and what the register still does not hold (a different answer over a settled one, or a token the call did not record)."""
    recorded, already, unread = [], [], []
    for qid, status, letter, line in tokens:
        row, old = now_rows[qid], before_rows.get(qid)
        got = (status, letter)
        if (row["status"], row["reading"]) == got:
            (already if old is not None and (old["status"], old["reading"]) == got else recorded).append(line)
            continue
        why = (_different_answer_text(row, qid) if settled(row)
               else "this call did not record it, so the register still shows the question as it was")
        unread.append({"id": qid, "line": line, "why": why})
    return recorded, already, unread


# GW1-47: where a line STARTS with an id, whatever follows it (a space, `-`, `.`, `)`, `:`, `=`, the end): the id is compared with the
# register's ids by `casefold`. Known gap: a register id outside `[A-Za-z][\w-]{0,63}` (`Q-3.1`, a non-ASCII start) is seen only by the
# `_TOKEN` road of `_stray_lines`, as before.
_LINE_START = re.compile(r"[\s\-*•>]*[*`]*(?P<id>[A-Za-z][\w-]{0,63})(?=[\s:=.,\-)*`]|$)")


def _stray_lines(text: str, now_rows: dict) -> list:
    """`[(register id, the line)]`: a line outside fences and quotes that STARTS with a register id and is no token (`Q1: a Q2: a`).
    Two roads: the `_TOKEN` shape with a register id and a value that is no answer (as before), and (GW1-47) a line that starts with
    the id in any case followed by any boundary (`q3: x`, `Q3 - x`, `Q3 is unclear`) - the error goes toward showing the person what was
    not recorded (FR-59). A line `_TOKEN` accepts with the id EXACTLY as the register spells it and a strict value is a token, not stray.
    The id returned is the register's spelling (an exact match, else the first key by the register's order). A BOM at a line's start is
    not part of it. No register rows: nothing."""
    out = []
    if not now_rows:
        return out
    for _raw, content in _plain_lines(text):
        content = content.lstrip(BOM)
        found = _TOKEN.fullmatch(content)
        if found and found.group("id") in now_rows:
            if _question_value(found.group("value")) is None:
                out.append((found.group("id"), content))
            continue
        start = _LINE_START.match(content)
        if not start:
            continue
        written = start.group("id")
        ident = written if written in now_rows else next((k for k in now_rows if str(k).casefold() == written.casefold()), None)
        if ident is not None:
            out.append((ident, content))
    return out


def stray_line(qid, words) -> str:
    """The line of the person's `words` that STARTS with the id `qid` and is no token (`Q1: a (see the ticket)`), shown (`_shown_line`),
    or "" when there is none. The ONE reader (AR-13) of that fact for every view that must not say "the factory recorded no answer"
    of a question the person did write about (FR-10, FR-41): the gate's note, the report's two sections, the stop's card. The tail after
    `EARLIER_ANSWER_MARK` (an answer the person has replaced) is not read; no id, no words, a non-text value: ""."""
    ident = str(qid or "")
    text = words if isinstance(words, str) else ""
    if not ident or not text:
        return ""
    text = text.split(EARLIER_ANSWER_MARK, 1)[0]
    return next((_shown_line(line) for found, line in _stray_lines(text, {ident: True}) if found == ident), "")


def question_lines_unread(words, questions) -> list:
    """`[{id, line}]`: lines of the person's words that NAME a question of the register still to be settled (`is_open`) and are no token
    (GW1-34): `Q1:` with nothing after it, `Q1: a (note)`, `Q1: a Q2: b`. The plan is sealed by the gate decision, so such a line must be
    read BEFORE the decision is recorded (AR-24); the code never guesses its letter (FR-12). The one reader of a stray line is
    `_stray_lines` (AR-13). Not counted: a question already settled or kept open `until the report`, a line in a fence or a quote
    (its own road, `fenced`), and the tail after `EARLIER_ANSWER_MARK` (an answer the person has replaced). `questions` are
    `load()["questions"]`; a caller that could not load them does not call this (an unknown is not an empty list, FR-59)."""
    text = words if isinstance(words, str) else ("" if words is None else str(words))
    text = text.split(EARLIER_ANSWER_MARK, 1)[0]
    now_rows = {q["id"]: q for q in questions if isinstance(q, dict) and q.get("id") and is_open(q)}
    return [{"id": ident, "line": _shown_line(content)} for ident, content in _stray_lines(text, now_rows)]


def gate_words_view(task_root, words, before, case_ids=None) -> dict:
    """What a gate's words did to the register, for the answer of a gate decision (DC1-19): READ ONLY, never writes, never raises.

    `words` are the answer's own lines (no `Earlier answer at this gate:` tail: that is the caller's to cut, else a correction reads as
    two answers); `before` is `load()`'s view taken BEFORE the call recorded anything (None: every token the register now holds is told as recorded). Returns
      recorded           ["Q1: a"]  settled (or kept open `until the report`) by THIS call
      already            ["Q1: a"]  settled before it, with the same answer, and named here again
      unread             [{id, line, why}]  a token that records nothing and says why: two answers, a letter out of range, an id the
                         register does not hold, a token in a fence, a different answer over a settled one (the `--reopen` door), a
                         line that STARTS with a register id and is no token (`Q1: a Q2: a`: each answer goes on a line of its own),
                         a token the call did not record
      named_not_recorded [{id, line}]  an id named on a line of neither kind (`_line_with`), no record
    or `{"unknown": <why>}` when the register or the answers file cannot be read: an unknown is never an empty list (FR-41, AR-28).
    A story with no register is the four empty lists."""
    root = Path(task_root)
    now = load(root)
    if now["skipped"]["unreadable_file"] or (now["problems"] and not now["questions"]):
        return {"unknown": (now["problems"] or ["the answers file could not be read"])[0]}
    text = words if isinstance(words, str) else ("" if words is None else str(words))
    now_rows = {q["id"]: q for q in now["questions"]}
    parsed = parse_choices(text, now["questions"], case_ids or [])
    tokens = [(qid, "answered", letter, f"{qid}: {letter}") for qid, letter in parsed["choices"].items()]
    tokens += [(qid, "not_needed", "", f"{qid}: not needed") for qid in parsed["not_needed"]]
    tokens += [(qid, DEFERRED, "", f"{qid}: {UNTIL_THE_REPORT}") for qid in parsed["deferred"]]
    recorded, already, unread = _token_outcomes(tokens, now_rows, {q["id"]: q for q in (before or {}).get("questions") or []})
    for conflict in parsed["conflicts"]:
        if conflict["id"] in now_rows:
            unread.append({"id": conflict["id"], "line": " | ".join(f"{conflict['id']}: {v}" for v in conflict["values"]),
                           "why": "two different answers for it; none was recorded"})
    for item in parsed["out_of_range"]:
        unread.append({"id": item["id"], "line": f"{item['id']}: {item['letter']}",
                       "why": f"the letter {item['letter']} is beyond its {item['readings']} readings"})
    for ident in parsed["unknown_ids"]:
        unread.append({"id": ident, "line": _shown_line(_line_with(text, ident) or ident),
                       "why": "not a question of this story, so nothing is recorded for it"})
    for line in parsed["fenced"]:
        found = _TOKEN.fullmatch(_content(line))
        unread.append({"id": found.group("id") if found else "", "line": _shown_line(line), "why": "a decision inside a code block is not read"})
    stray = _stray_lines(text, now_rows)
    unread += [{"id": ident, "line": _shown_line(content),
                "why": "this line is no answer of the form `Q1: <letter>` or `Q1: not needed`: each answer goes on a line "
                       "of its own, with nothing else on it"} for ident, content in stray]
    stray = {content for _ident, content in stray}
    covered = {entry["id"] for entry in unread} | {qid for qid, _s, _l, _t in tokens}
    named = []
    for qid, row in now_rows.items():
        line = _line_with(text, qid)
        if line and qid not in covered and not settled(row) and _content(line) not in stray:
            named.append({"id": qid, "line": _shown_line(line)})
    return {"recorded": recorded, "already": already, "unread": unread, "named_not_recorded": named}


def answers_for_brief(task_root) -> dict:
    """What the next role is told the person already decided: {"answers": [...], "unreadable": bool}. One entry per
    question that is settled (answered, not needed) or kept open until the report, and whose record holds -
    `id, question, status, reading, reading_text, where, at, words` (the words whole: a reader that cuts them says
    so). A question that is asked again (open, changed since, `with_designer`) has no entry. `unreadable` is true
    when the answers file has a broken line, a line that is no object, or cannot be read at all (an `answers_applied`
    row is no such line): the brief says once that some answers may be missing. No file: ([], False)."""
    view = load(task_root)
    skipped = view["skipped"]
    out = []
    for q in view["questions"]:
        if q["status"] not in SETTLED_STATUSES + (DEFERRED,) or is_open(q):
            continue
        readings, text = q.get("readings"), ""
        if q["reading"] and q["reading"] in LETTERS and isinstance(readings, list) and LETTERS.index(q["reading"]) < len(readings):
            item = readings[LETTERS.index(q["reading"])]
            text = str(item.get("reading") or "") if isinstance(item, dict) else str(item)
        out.append({"id": q["id"], "question": str(q.get("question") or ""), "status": q["status"], "reading": q["reading"],
                    "reading_text": text, "where": q["where"], "at": q["at"], "words": q["words"]})
    unreadable = bool(skipped["broken_lines"] + skipped["non_object_lines"] + skipped["unreadable_file"])
    return {"answers": out, "unreadable": unreadable}


def last_stop_shown(task_root) -> dict:
    """What the LAST question stop showed, `{"stage", "at", "shown": {id: row_hash as shown}}`, read from the driver's state
    (`state/driver-state.json`, key `question_stop`; overwritten at every stop). `{"shown": {}}` when the file or the key is absent
    or unreadable, or `shown` is no object; an entry whose hash is not a text is left out. Read-only, never raises. The ONE reader
    of that record outside the driver (AR-13): the brief's `shown_at_last_stop` and `reword`'s one-reword-per-showing rule."""
    try:
        data = json.loads(Path(task_root).joinpath(*DRIVER_STATE_REL).read_bytes().decode("utf-8-sig", errors="replace"))
    except (OSError, ValueError, RecursionError):
        return {"shown": {}}
    stop = data.get("question_stop") if isinstance(data, dict) else None
    shown = stop.get("shown") if isinstance(stop, dict) else None
    if not isinstance(shown, dict):
        return {"shown": {}}
    return {"stage": str(stop.get("stage") or ""), "at": str(stop.get("at") or ""),
            "shown": {k: v for k, v in shown.items() if isinstance(k, str) and isinstance(v, str) and v}}


def asked_for_brief(task_root) -> dict:
    """What a role is told about the questions already asked of the person, BEFORE it raises one (FV1-9, D1):
    `{"open": [{id, question, repeated_by: [ids], shown_at_last_stop: bool, reworded: int}], "repeats": [{id, same_as, target_settled,
    declared_by}], "unreadable": bool, "present": bool}`. `open` is every question `is_open` says the person is (still) asked, in register
    order (`shown_at_last_stop`: the last question stop showed it on its CURRENT bytes; `reworded`: how many times it was asked
    again in other words); `repeats` is every declared repeat that is hidden (`repeated_by` of its target), in register order, with the
    target it stands behind and whether that target is settled. `present` is False with no register file; `unreadable` is True
    when the register or the answers file has a broken part, so the list may be incomplete. Never raises on the story's data."""
    view = load(task_root)
    skipped = view["skipped"]
    shown = last_stop_shown(task_root)["shown"]
    questions = [q for q in view["questions"] if isinstance(q, dict)]
    by_id = {q["id"]: q for q in questions}
    order = {q["id"]: i for i, q in enumerate(questions)}
    open_rows = [{"id": q["id"], "question": str(q.get("question") or ""), "repeated_by": list(q.get("repeated_by") or []),
                  "shown_at_last_stop": shown.get(q["id"]) == q["row_hash"],
                  "reworded": len(q["reworded"]) if isinstance(q.get("reworded"), list) else 0} for q in questions if is_open(q)]
    repeats = sorted(({"id": rid, "same_as": target["id"], "target_settled": settled(target),
                       "declared_by": str(by_id[rid].get("declared_by") or "")}
                      for target in questions for rid in target.get("repeated_by") or []), key=lambda e: order[e["id"]])
    unreadable = bool(view["problems"] or skipped["broken_lines"] + skipped["non_object_lines"] + skipped["unreadable_file"])
    return {"open": open_rows, "repeats": repeats, "unreadable": unreadable, "present": view["register_present"]}


def repeat_records(task_root) -> dict:
    """The retro's record of every merge (FV1-9, owner 14.11): `{"records": [{id, same_as, declared_by, by, why, stage, at, texts,
    standing}], "unreadable": bool}`, one entry per `repeat` record of the answers file in file order, an undone one included.
    `texts` are the two questions as they stood when the record was written. `standing` says what became of it: `merged` (the id is
    a hidden repeat now), `shown again: gone|cycle|target_changed|its words changed`, `answered by the person`, `reopened`,
    `replaced by a later merge` (a later `repeat` record of the same id, a carried-over one included). `present` is True when the
    story has a register at all (F3: with one, "no merge" is a fact the retro says; without one it says nothing). `unreadable` is True when
    the answers file has a broken line or cannot be read: a merge may be missing. The ONE reader of `repeat_history` (AR-13)."""
    view = load(task_root)
    skipped = view["skipped"]
    by_id = {q["id"]: q for q in view["questions"] if isinstance(q, dict)}
    history = view["repeat_history"]
    newest = {rid: rec for rid, rec in history}
    records = []
    for rid, rec in history:
        question = by_id.get(rid)
        if rec is not newest[rid]:
            standing = "replaced by a later merge"
        elif question is None:
            standing = "shown again: gone"
        elif question.get("status") == REPEAT:
            standing = ("merged" if hidden_repeat(question) else f"shown again: {question['repeat_problem']}"
                        if question.get("repeat_problem") else "shown again: its words changed")
        else:
            standing = "reopened" if question.get("status") == "open" else "answered by the person"
        records.append({"id": rid, "same_as": str(rec.get("same_as") or ""), "declared_by": str(rec.get("declared_by") or ""),
                        "by": str(rec.get("by") or ""), "why": str(rec.get("words") or ""), "stage": str(rec.get("stage") or ""),
                        "at": str(rec.get("at") or ""), "texts": dict(rec["texts"]) if isinstance(rec.get("texts"), dict) else {},
                        "standing": standing})
    return {"records": records, "present": view["register_present"],
            "unreadable": bool(skipped["broken_lines"] + skipped["non_object_lines"] + skipped["unreadable_file"])}


# --------------------------------------------------------------------------------------------
# FV1-9: a question asked once - repeats declared, questions asked again in clearer words, a note that helps
# --------------------------------------------------------------------------------------------

def _dependants_in_plan(root: Path, qid: str, out: dict) -> None:
    import planning_contract as PC
    path, _document, rows, problem = PC._plan_state(root)
    if path is None:
        return
    if problem:
        out["unknown"].append(f"{problem}, so what rests on {qid} in it cannot be told")
        return
    for row in rows:
        if not isinstance(row, dict):
            continue
        refs = row.get("question_refs")
        refs = [x.strip() for x in refs if isinstance(x, str)] if isinstance(refs, list) else []
        branches = row.get("if_answered")
        reason = row.get("reason")
        found = {"refs": qid in refs,
                 "branch": isinstance(branches, dict) and any(str(k).strip() == qid for k in branches),
                 "reason": isinstance(reason, str) and bool(PC._id_token(qid).search(reason))}
        if any(found.values()):
            out["plan_rows"].append(dict(found, id=str(row.get("id") or "").strip()))


def _dependants_in_cases(root: Path, qid: str, out: dict) -> None:
    import gate_brief
    C = _contract()
    cases, problems = gate_brief.story_cases(root)
    out["unknown"].extend(problems)
    for case_id, case in cases.items():
        try:
            text = Path(case["path"]).read_text(encoding="utf-8", errors="replace")
        except OSError:
            out["unknown"].append(f"{case_id} could not be read, so what it rests on cannot be told")
            continue
        oracles, why = C.then_oracles_from_text(text)
        if oracles is None and why:
            out["unknown"].append(f"{case_id}: its `then_oracles` could not be read ({why})")
        by_oracle = [e.get("then") for e in oracles or [] if e.get("source") in ("person", "unknown") and str(e.get("ref") or "").strip() == qid]
        by_letter = [t.get("then") for t in case.get("thens") or [] if str(t.get("question") or "").strip() == qid]
        if by_oracle or by_letter:
            out["cases"].append({"id": str(case_id), "oracle_thens": by_oracle, "question_thens": by_letter})


def dependants(task_root, qid) -> dict:
    """Everything that still rests on the question `qid` besides the register (FV1-9, B1): `{"plan_rows": [{id, refs, branch, reason}],
    "cases": [{id, oracle_thens, question_thens}], "unknown": [what could not be read]}`. A plan row rests on it when it names the id in
    `question_refs` (`refs`), as a key of `if_answered` (`branch`: its answers are keyed by letter) or as a whole token of `reason`;
    a case when a `then_oracles` entry with source `person` or `unknown` names it, or a `question_thens` entry does (`question_thens`:
    its Then texts are keyed by letter). The ONE reader of who keys an id (AR-13): `declare_repeat` and `reword` ask it. The ERROR
    DIRECTION is "a dependant exists": a plan or a case that cannot be read is an `unknown` entry, never "nothing rests on it".
    No plan, no cases: empty lists. Never raises."""
    root, qid = Path(task_root), str(qid or "").strip()
    out: dict = {"plan_rows": [], "cases": [], "unknown": []}
    for read, what in ((_dependants_in_plan, "the test plan"), (_dependants_in_cases, "the test cases")):
        try:
            read(root, qid, out)
        except Exception as exc:  # noqa: BLE001 - an unreadable source is an unknown, never a silence
            out["unknown"].append(f"{what} could not be read ({type(exc).__name__}), so what rests on {qid} in it cannot be told")
    return out


def _dependant_lines(deps: dict, *, bare_ok: bool) -> list:
    """One phrase per dependant (`plan row TS-3 (its answers branch)`, `case TC-9 (Then 2)`), the unreadable ones as they are said.
    `bare_ok`: a plan row that names the id in `question_refs` only is left out (`repoint_bare_ref` moves it)."""
    lines = []
    for row in deps["plan_rows"]:
        if bare_ok and row["refs"] and not row["branch"] and not row["reason"]:
            continue
        lines.append(f"plan row {row['id'] or '(no id)'} (" + ("its answers branch" if row["branch"] else "its reason" if row["reason"]
                                                             else "its question_refs") + ")")
    for case in deps["cases"]:
        thens = sorted({str(n) for n in case["oracle_thens"] + case["question_thens"]})
        lines.append(f"case {case['id']} (Then {', '.join(thens)})")
    return lines + list(deps["unknown"])


def _reaches(by_id: dict, start: str, goal: str) -> bool:
    """Does walking `same_as` from `start` through the `repeat` rows reach `goal`? (the cycle `declare_repeat` refuses)"""
    current, seen = start, set()
    while current and current not in seen:
        if current == goal:
            return True
        seen.add(current)
        row = by_id.get(current)
        current = row["same_as"].strip() if row is not None and row.get("status") == REPEAT and isinstance(row.get("same_as"), str) else ""
    return False


def _unusable_register(view: dict) -> str:
    """"" when the register and the answers file can be read, else what is wrong (the ONE preamble of the FV1-9 writers)."""
    if not view["register_present"]:
        return "the story has no work/requirements-readiness.json, so there is no register"
    if view["problems"] and not view["questions"]:
        return view["problems"][0]
    if view["skipped"]["unreadable_file"]:
        return "work/question-answers.jsonl exists and cannot be read"
    return ""


def declare_repeat(task_root, qid, same_as, why, *, by, declared_by, stage) -> dict:
    """Declare that question `qid` asks what question `same_as` asks (FV1-9, D3): the person is then asked once. Appends ONE `repeat`
    record (the retro's record: who declared, both ids, both texts as they stand, the why, the stage, the time) and returns it; a
    declaration that already stands (the same target, the target's row unchanged) returns its record and writes nothing. Raises
    `Refused` and writes nothing when: the register or the answers file cannot be read; `qid` or `same_as` is no id of the register, or
    they are the same; `why` is blank; `qid` is settled, deferred or with the designer; `same_as` leads back to `qid` (a cycle); or
    something else still rests on `qid` (`dependants`: a plan row that keys its answers by it, a case that names it, anything that
    could not be read). A plan row that only lists `qid` in `question_refs` is moved to `same_as` first (`repoint_bare_ref`; no
    letter is ever mapped). Whether the two questions ask the same thing is the DECLARING ROLE's judgment, judged afterwards from
    the retro; this checks ids, bytes and dependants only."""
    root = Path(task_root)
    view = load(root)
    wanted = qid.strip() if isinstance(qid, str) else ""
    target_id = same_as.strip() if isinstance(same_as, str) else ""
    unusable = _unusable_register(view)
    if unusable:
        raise Refused(f"- {unusable}. Expected: a story whose register and answers file can be read, before a question is marked as a repeat")
    by_id = {q["id"]: q for q in view["questions"]}
    row, target = by_id.get(wanted), by_id.get(target_id)
    if row is not None and target is not None and hidden_repeat(row) and row.get("same_as") == target_id \
            and row.get("target_hash") == target["row_hash"]:
        return next(rec for rid, rec in reversed(view["repeat_history"]) if rid == wanted)
    problems = []
    if row is None:
        problems.append(f"no question with id {qid!r}. {_valid_ids(view)}")
    if not target_id:
        problems.append("`same_as` is missing: name the id of the question this one repeats")
    elif target is None:
        problems.append(f"`same_as` {same_as!r} is no id of the register. {_valid_ids(view)}")
    elif target_id == wanted:
        problems.append(f"{wanted} cannot be marked as a repeat of itself. Expected: the id of the EARLIER question it repeats")
    elif _reaches(by_id, target_id, wanted):
        problems.append(f"{target_id} is itself marked as a repeat that leads back to {wanted}: a cycle. Expected: the id of the "
                        "question both stand behind")
    if not (isinstance(why, str) and why.strip()):
        problems.append("`why` is blank. Expected one line saying what the two questions both ask")
    if row is not None and (settled(row) or row["status"] in (DEFERRED, "with_designer")):
        problems.append(f"{wanted} is {row['status']}: a question the person already settled or left with the designer is not marked as a "
                        "repeat. Expected: point the work at the question that is open instead")
    if problems:
        raise Refused("\n".join(f"- {p}" for p in problems))
    deps = dependants(root, wanted)
    notes = []
    if not _dependant_lines(deps, bare_ok=True) and deps["plan_rows"]:
        for entry in deps["plan_rows"]:
            _written, line = _plan_module().repoint_bare_ref(root, entry["id"], wanted, target_id, f"{wanted} merged into {target_id}")
            if line:
                notes.append(line)
        deps = dependants(root, wanted)
    left = _dependant_lines(deps, bare_ok=False)
    if left:
        raise Refused(f"- {wanted} cannot be merged into {target_id} while these still rest on {wanted}: {'; '.join(left)}"
                      + ("".join(f" ({n})" for n in notes))
                      + ". Expected: repoint them first - the test planner's rework for a plan row, the case designer for a case - "
                        "then declare the repeat again")
    texts = {"question": str(row.get("question") or ""), "same_as_question": str(target.get("question") or "")}
    return record(root, wanted, REPEAT, why.strip(), "stage ran", by, row["row_hash"], same_as=target_id,
                  declared_by=declared_by, target_hash=target["row_hash"], stage=stage, texts=texts)


def _plan_module():
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    import planning_contract
    return planning_contract


def _reading_texts(row) -> list:
    return [str(r.get("reading") or "") if isinstance(r, dict) else str(r) for r in (row.get("readings") if isinstance(row.get("readings"), list) else [])]


def _squeeze(text) -> str:
    return " ".join(str(text or "").split())


def _may_reword(role: str, row: dict, deps: dict, own: dict) -> bool:
    """Who may ask a question again (owner 14.11, F-10): the conductor always; a role whose own artifact kind (`reword_own_artifacts`)
    names the id or whose carrier raised the row; any other role only a question it asked itself (`asked_by`)."""
    if role == "conductor":
        return True
    kind = own.get(role)
    raised = row.get("raised_for") if isinstance(row.get("raised_for"), dict) else {}
    if kind == "cases":
        return bool(deps["cases"]) or bool(raised.get("case"))
    if kind == "plan_rows":
        return bool(deps["plan_rows"]) or raised.get("origin") == "S3-plan"
    return bool(role) and str(row.get("asked_by") or "").strip() == role


def reword(task_root, qid, spec, *, role, by, stage) -> dict:
    """Ask the unanswered question `qid` again in clearer words (FV1-9, D4): the id stays, the row's `question` (and, when `spec` gives
    them, the text of each reading) is replaced, and `reworded` gains `{at, by, role, stage, why, was[, was_readings]}` so the person
    sees the earlier wording. `spec` is `{"question", "readings"?, "why"}`. Returns the row as `load` shows it afterwards. Each hidden
    repeat of the row is declared again against its new bytes, so a reword never shows two questions at once. Raises `Refused` and
    writes nothing when: no such id or the register cannot be read; the row is not `open`/`named`; the last question stop did not
    show the row on its current bytes (ONE reword per showing); `role` may not (the conductor always; a role whose own work cites
    the id; any other only a question it asked); `readings` are given and a plan row or a case answers them by letter for another
    role, or that could not be read (the question text alone is then allowed); the count of readings differs or one is blank; the new
    row fails `contract.question_errors`; nothing changed; `why` is blank. A reword whose words already stand, or stood as the result of
    an earlier reword, is done: nothing is written (a replay after a crash); a history match counts only for the same `role` and `why`
    that produced those words. Whether the meaning was kept is the rewording role's stage
    critic's judgment; this checks ids, shape, showings and dependants."""
    root = Path(task_root)
    view = load(root)
    wanted = qid.strip() if isinstance(qid, str) else ""
    unusable = _unusable_register(view)
    if unusable:
        raise Refused(f"- {unusable}. Expected: a story whose register can be read, before a question is asked again")
    row = next((q for q in view["questions"] if q["id"] == wanted), None)
    if row is None:
        raise Refused(f"- no question with id {qid!r}. {_valid_ids(view)}")
    spec = spec if isinstance(spec, dict) else {}
    text = spec["question"].strip() if isinstance(spec.get("question"), str) else ""
    given = spec.get("readings")
    why = spec["why"].strip() if isinstance(spec.get("why"), str) else ""
    role, own = str(role or "").strip(), vocabulary().get("reword_own_artifacts", {})
    # REPLAY (P6): words that already stand, or stood as the result of the same party's earlier reword for the same reason, are DONE.
    # It sits before every other check: a done reword changed the row's bytes, so the showing check would refuse its replay forever.
    # Never turns a no-op request into a success: the ORIGINAL words were produced by no reword and match nothing here.
    if text and (given is None or isinstance(given, list)):
        history = row.get("reworded") if isinstance(row.get("reworded"), list) else []
        if history and _squeeze(text) == _squeeze(row.get("question")) and (
                given is None or [_squeeze(x) for x in given] == [_squeeze(x) for x in _reading_texts(row)]):
            return row
        for k in range(len(history) - 1):
            made, later = history[k], history[k + 1]
            if (isinstance(made, dict) and isinstance(later, dict) and isinstance(later.get("was"), str)
                    and _squeeze(text) == _squeeze(later["was"]) and str(made.get("role") or "").strip() == role
                    and _squeeze(made.get("why")) == _squeeze(why)):
                return row
    deps = dependants(root, wanted)
    problems = []
    if row["status"] not in OPEN_STATUSES:
        problems.append(f"{wanted} is {row['status']}: only a question nobody has answered is asked again in other words. Expected: for an "
                        "answered one, the person reopens it first")
    if last_stop_shown(root)["shown"].get(wanted) != row["row_hash"]:
        problems.append(f"{wanted} was not shown to the person in these words since it was last worded; it can be asked again in other "
                        "words after the person has seen it")
    if not _may_reword(role, row, deps, own):
        problems.append(f"`{role}` does not cite {wanted} in its own work: raise a question of your own, or cite {wanted} by its id instead")
    old_readings = _reading_texts(row)
    new_readings = old_readings
    if given is not None:
        if not (isinstance(given, list) and len(given) == len(old_readings)
                and all(isinstance(x, str) and x.strip() for x in given)):
            problems.append(f"`readings` must be {len(old_readings)} texts, one for each reading of {wanted}, none blank")
        else:
            new_readings = [x.strip() for x in given]
        kind = own.get(role) if role != "conductor" else None
        frozen = [r["id"] for r in deps["plan_rows"] if r["branch"] and kind != "plan_rows"]
        frozen += [c["id"] for c in deps["cases"] if c["question_thens"] and kind != "cases"]
        if frozen or deps["unknown"]:
            problems.append(f"the readings of {wanted} are what {' / '.join(frozen) or 'something that could not be read'} answer by letter: "
                            "reword the question only, or ask their owner to repoint first")
    if not why:
        problems.append("`why` is blank. Expected one line saying what the earlier words did not make clear")
    changed_readings = [_squeeze(a) for a in new_readings] != [_squeeze(b) for b in old_readings]
    if not text:
        problems.append("`question` is blank. Expected the question in clearer words")
    elif _squeeze(text) == _squeeze(row.get("question")) and not changed_readings:
        problems.append(f"nothing changed: the question and every reading are the words {wanted} already has")
    if text and not problems:
        candidate = dict(row, question=text, readings=[dict(r, reading=new_readings[i]) if isinstance(r, dict) else r
                                                       for i, r in enumerate(row["readings"])])
        errors = _contract().question_errors(candidate)
        if errors:
            problems.append("the reworded question does not pass the shape check of a question: " + "; ".join(errors))
    if problems:
        raise Refused("\n".join(f"- {p}" for p in problems))
    carry = [q for q in view["questions"] if q.get("status") == REPEAT and isinstance(q.get("same_as"), str)
             and q["same_as"].strip() == wanted and hidden_repeat(q)]
    path = root.joinpath(*READINESS_REL)
    with answers_lock(root):
        try:
            data = json.loads(path.read_bytes().decode("utf-8-sig"))
            rows = data["open_questions"]
            stored = next(r for r in rows if isinstance(r, dict) and isinstance(r.get("id"), str) and r["id"].strip() == wanted)
        except (OSError, ValueError, RecursionError, KeyError, TypeError, StopIteration):
            raise Refused(f"- {path} could not be read again for {wanted}: nothing was written")
        if _hash(stored) != row["row_hash"]:
            raise Refused(f"- {wanted} changed while it was being reworded: nothing was written. Expected: look at it again")
        entry = {"at": _now(), "by": by, "role": role, "stage": stage, "why": why, "was": str(stored.get("question") or "")}
        stored["question"] = text
        if changed_readings:
            entry["was_readings"] = old_readings
            for item, new in zip(stored["readings"], new_readings):
                item["reading"] = new
        stored["reworded"] = (stored["reworded"] if isinstance(stored.get("reworded"), list) else []) + [entry]
        _write_readiness(path, data)
    after = {q["id"]: q for q in load(root)["questions"]}
    for q in carry:      # the target's bytes moved: each repeat that stood behind it stands behind the new words (F-13)
        try:
            record(root, q["id"], REPEAT, f"carried over: {wanted} was asked again in clearer words", "stage ran", by, q["row_hash"],
                   same_as=wanted, declared_by=q.get("declared_by") or "", target_hash=after[wanted]["row_hash"], stage=stage,
                   texts={"question": str(q.get("question") or ""), "same_as_question": str(after[wanted].get("question") or "")})
        except Refused:
            continue         # not carried: the repeat shows again (`target_changed`), the error goes toward asking
    return after[wanted]


def record_note(task_root, qid, words, *, by, where) -> dict:
    """Record what helps the person answer question `qid`, written by the conductor from the sources (FV1-9, D5): ONE `note` record
    bound to the bytes of the row as they are now (`row_hash`), so a card shows it only while the row is as it was. The words are
    1..`NOTE_MAX` characters (outer blanks cut); `human_text.problems` finds nothing in them (no plugin path, no field name reaches the
    person); `by` and `where` are values of the vocabulary. The note is the helper's, never the person's words. Raises `Refused`
    and writes nothing otherwise."""
    root = Path(task_root)
    vocab = vocabulary()
    view = load(root)
    wanted = qid.strip() if isinstance(qid, str) else ""
    row = next((q for q in view["questions"] if q["id"] == wanted), None)
    problems = [] if row is not None else [f"no question with id {qid!r}. {_valid_ids(view)}"]
    problems.extend(_common_problems(vocab, words, where, by))
    text = words.strip() if isinstance(words, str) else ""
    if len(text) > NOTE_MAX:
        problems.append(f"the note is {len(text)} characters and a card carries at most {NOTE_MAX}. Expected: the one thing that helps the "
                        "person answer, shorter")
    elif text:
        if str(HERE) not in sys.path:
            sys.path.insert(0, str(HERE))
        import human_text
        found = human_text.problems(text, kind="report")
        if found:
            problems.append("the note breaks the rules for a text a person reads: " + "; ".join(f"{p['rule']} ({p['found']})" for p in found)
                            + ". Expected: plain words, with no path or field name of the factory in them")
    if problems:
        raise Refused("\n".join(f"- {p}" for p in problems))
    rec = {"kind": "note", "id": wanted, "words": text, "by": by, "where": where, "at": _now(), "row_hash": row["row_hash"]}
    _append(root, rec)
    return rec


REWORD_ENTRY_FORM = ('{"question": "Q<n>", "text": "<the question in clearer words>", "readings": ["<text>", ...] (optional), '
                      '"why": "<one line>"}')


def reword_entry(item) -> tuple:
    """`(qid, spec, problem)` of ONE `reword_questions` entry (FV1-9 F4): the one check and the one spec build the case carrier
    (`rewords_for_case`) and the plan carrier (`planning_contract._reword_plan_entries`) share. `problem` is "" for a well-formed entry
    (then `qid` is the target and `spec` is `reword`'s argument), else why not, with the expected form, and `qid`/`spec` are None."""
    if not isinstance(item, dict):
        return None, None, f"is not an object. Expected: {REWORD_ENTRY_FORM}"
    qid, text, why, readings = (item.get(k) for k in ("question", "text", "why", "readings"))
    if not all(isinstance(x, str) and x.strip() for x in (qid, text, why)) or not (readings is None or isinstance(readings, list)):
        return None, None, f"needs `question`, `text` and `why` as texts (`readings` a list when given). Expected: {REWORD_ENTRY_FORM}"
    return qid, {"question": text, "why": why, **({"readings": readings} if readings is not None else {})}, ""


def _apply_case_key(case_text: str, case_id: str, key: str, apply) -> dict:
    """The shared walk of a case front-matter key that holds a list of entries the S4 exit executes (`question_repeats`,
    `reword_questions`): `apply(entry)` returns "" when the entry is done, else why not. `{"text", "done", "problems"}`: `text` is the
    case with the done entries dropped from the key (the key itself when none is left), None when nothing was done; a refused entry
    stays in the key and says why; a key that is not one line of JSON holding a list of objects is one problem and is kept."""
    C = _contract()
    out = {"text": None, "done": [], "problems": []}
    entries, why = C.parse_json_list(C.front_line(case_text, key))
    if entries is None:
        if why:
            out["problems"].append(f"{case_id}: `{key}` was not read ({why}); it is kept and nothing was done for it")
        return out
    left = []
    for entry in entries:
        line = apply(entry)
        if line:
            out["problems"].append(f"{case_id}: {line}")
            left.append(entry)
        else:
            out["done"].append(entry)
    if out["done"]:
        out["text"] = C.set_front_line(case_text, key, json.dumps(left, ensure_ascii=False) if left else None)
    return out


def repeats_for_case(task_root, case_text: str, case_id: str) -> dict:
    """The S4-exit half of declaring a repeat (FV1-9, D3): execute the case designer's `question_repeats` entries
    (`{"question": "Q16", "same_as": "Q7", "why": "<one line>"}`) through `declare_repeat` (role `qa-case-designer`, by `driver`, stage S4)
    and return `{"text", "recorded": [{question, same_as}], "problems": [line]}`. Done entries (a replay included) are dropped from
    the key; a refused or malformed one stays and says why; a `same_as` of `raise` is malformed. Never raises on the case's own data."""
    C = _contract()
    recorded = []

    def one(entry) -> str:
        question, target, why = (entry.get(k) for k in ("question", "same_as", "why"))
        if not all(isinstance(x, str) and x.strip() for x in (question, target, why)):
            return "a `question_repeats` entry needs `question`, `same_as` and `why`, each a text"
        if target.strip() == C.RAISE_REF:
            return f"{question.strip()}: `same_as` is `{C.RAISE_REF}`; name the id of a question the register already holds"
        try:
            declare_repeat(task_root, question, target, why, by="driver", declared_by="qa-case-designer", stage="S4")
        except Refused as exc:
            return f"{question.strip()} -> {target.strip()} was not recorded: {_squeeze(exc)}"
        recorded.append({"question": question.strip(), "same_as": target.strip()})
        return ""

    out = _apply_case_key(case_text, case_id, "question_repeats", one)
    return {"text": out["text"], "recorded": recorded, "problems": out["problems"]}


def rewords_for_case(task_root, case_text: str, case_id: str) -> dict:
    """The S4-exit half of asking a question again (FV1-9, D4): execute the case designer's `reword_questions` entries
    (`{"question": "Q7", "text": "<clearer words>", "readings": [...]?, "why": "<one line>"}`) through `reword` (role `qa-case-designer`,
    by `driver`, stage S4); the same shape and rules as `repeats_for_case`: `{"text", "reworded": [{question}], "problems": [line]}`."""
    reworded = []

    def one(entry) -> str:
        question, spec, problem = reword_entry(entry)
        if problem:
            return f"a `reword_questions` entry {problem}"
        try:
            reword(task_root, question, spec, role="qa-case-designer", by="driver", stage="S4")
        except Refused as exc:
            return f"{question.strip()} was not asked again: {_squeeze(exc)}"
        reworded.append({"question": question.strip()})
        return ""

    out = _apply_case_key(case_text, case_id, "reword_questions", one)
    return {"text": out["text"], "reworded": reworded, "problems": out["problems"]}


def record_case(task_root, case_id, decision, words, where, by, case_ids=None, shown_hash="", at=None) -> dict:
    """Append ONE case-decision record (`<full case id>: manual|automate`, the person's explicit
    word) and return it. `case_ids` are the story's case ids when the caller has them: an id that is
    not one of them is refused (an empty list refuses every id); None means the caller has none, and
    any non-empty id is accepted. `shown_hash` is optional here and stored only when given."""
    root = Path(task_root)
    vocab = vocabulary()
    problems = []
    wanted = case_id.strip() if isinstance(case_id, str) else ""
    if not wanted:
        problems.append("the case id is blank. Expected the FULL case id, e.g. TP1-13797_TC_009")
    elif case_ids is not None and wanted not in set(case_ids):
        listed = ", ".join(list(case_ids)[:12]) or "none - the story has no case ids"
        problems.append(f"no case with id {case_id!r} in this story. Valid full case ids: {listed}"
                        + (", ..." if len(case_ids) > 12 else ""))
    if decision not in vocab["case_decisions"]:
        problems.append(f"decision {decision!r} cannot be recorded. Valid: " + ", ".join(vocab["case_decisions"]))
    problems.extend(_common_problems(vocab, words, where, by))
    shown = shown_hash if isinstance(shown_hash, str) else ""
    if shown and not HASH_TEXT.fullmatch(shown):
        problems.append(f"the register hash {shown!r} is not a sha256 (64 lower-case hex digits)")
    if problems:
        raise Refused("\n".join(f"- {p}" for p in problems))
    rec = {"kind": "case", "case": wanted, "decision": decision, "words": words, "where": where,
           "by": by, "at": at or _now()}
    if shown:
        rec["row_hash"] = shown
    _append(root, rec)
    return rec


# --------------------------------------------------------------------------------------------
# raising a question after S2 (t-227 F8, P20)
# --------------------------------------------------------------------------------------------

_QUESTION_ID = re.compile(r"Q([0-9]+)")


def _next_question_id(rows: list) -> str:
    """`Q<n>` with n one past the largest numbered id of the register (`Q1` when there is none)."""
    numbers = [int(m.group(1)) for r in rows if isinstance(r, dict) and isinstance(r.get("id"), str)
               for m in [_QUESTION_ID.fullmatch(r["id"].strip())] if m]
    return f"Q{max(numbers, default=0) + 1}"


def raise_question(task_root, case_file, then, spec) -> dict:
    """Add ONE before/now question to `open_questions` of the story's readiness file and return it.

    TC_015 of TP1-15045 asked for the code P-multi returns, and no S2 question existed for it:
    the expected 403 was taken from the diff. The author of a case that meets such a Then raises
    the question here, with what the behaviour is NOW and what it was BEFORE (`unknown` when the
    base revision cannot be read - never a guess), and then writes the Then as `unknown` with the
    new id. `spec` is the author's content: `{"question", "source_says", "severity", "owner_role",
    "before": {"value", "where"}, "now": {"value", "where"}}`; the id and the two readings (the
    fixed pair, `contract.claim_readings`) are the code's. Raises `Refused` and writes nothing when
    the Then already has an oracle other than `unknown` (a Then that has one is not asked about),
    when the Then is not under `## Then`, or when the question would not pass `question_errors`.

    Keyed by (case, Then) (O4): the row carries `raised_for {case, then}` and a second raise for the same
    pair with the SAME before/now returns that row and writes nothing, so a step that ran twice (a crash
    between the raise and the case rewrite, a relaunch) never asks the person the same question twice (FR-7);
    with a DIFFERENT before/now it is refused, naming the existing id and both texts (t-269 F5)."""
    sys.path.insert(0, str(HERE))
    import contract as C
    try:
        case_text = Path(case_file).read_bytes().decode("utf-8-sig")
    except (OSError, UnicodeDecodeError) as exc:
        raise Refused(f"- --case-file {str(case_file)!r} could not be read as UTF-8 text ({type(exc).__name__}). "
                      "Expected the path of the case the question is for")
    declared = (C.front_line(case_text, "id") or "").strip().strip("\"'")
    return _raise(task_root, case_text, declared or Path(case_file).stem, then, spec)


def _shown(row) -> str:
    """The facts a question puts in front of the person, as ONE comparable sentence: `before <value> (<where>),
    now <value> (<where>)`, whitespace collapsed. Two questions that print the same sentence ask the same thing."""
    def side(name: str) -> str:
        item = row.get(name) if isinstance(row, dict) else None
        item = item if isinstance(item, dict) else {}
        value = " ".join(str(item.get("value") or "").split())
        where = " ".join(str(item.get("where") or "").split())
        return f"{name} {value or 'not recorded'}" + (f" ({where})" if where else "")
    return f"{side('before')}, {side('now')}"


def _raise(task_root, case_text: str, case_id: str, then, spec) -> dict:
    """`raise_question` on the case's text (the S4 exit has it already, and writes it after)."""
    root = Path(task_root)
    sys.path.insert(0, str(HERE))
    import contract as C
    from s5_precheck import then_clauses
    problems = []
    numbers = [number for number, _ in then_clauses(case_text)]
    if not isinstance(then, int) or isinstance(then, bool) or then not in numbers:
        problems.append(f"Then {then!r} is not an item under `## Then` of that case "
                        f"(it has {', '.join(map(str, numbers)) or 'none'})")
    entries, why = C.then_oracles_from_text(case_text)
    if entries is None and why:
        problems.append(f"the case's `then_oracles` cannot be read ({why}); repair it first, one line of JSON")
    for entry in entries or []:
        if entry.get("then") == then and str(entry.get("source") or "") != "unknown":
            problems.append(f"Then {then} already has the oracle `{entry.get('source')}:{entry.get('ref')}`: a Then "
                            "that has an oracle is not asked about")
    question, found = C.claim_question(spec, "the question file")
    problems.extend(found)
    if problems:
        raise Refused("\n".join(f"- {p}" for p in problems))
    path = root.joinpath(*READINESS_REL)
    with answers_lock(root):  # two raises never take the same id
        try:
            data = json.loads(path.read_bytes().decode("utf-8-sig"))
        except FileNotFoundError:
            raise Refused(f"- {path} does not exist: there is no register to add the question to. Expected the "
                          "story's work/requirements-readiness.json (S2 writes it)")
        except (OSError, ValueError, RecursionError):
            raise Refused(f"- {path} is not valid JSON: repair it before a question is added")
        rows = data.get("open_questions") if isinstance(data, dict) else None
        if not isinstance(data, dict) or not (rows is None or isinstance(rows, list)):
            raise Refused(f"- {path} does not hold an object with an `open_questions` list")
        rows = rows or []
        key_pair = {"case": case_id, "then": then}
        row, earlier = _question_row(rows, question, key_pair)
        if earlier is not None:
            # Keyed by (case, Then): this pair was raised already. The SAME before/now is the same question
            # (a crash that lost the case rewrite replays here: one id, idempotent). A DIFFERENT before/now
            # is not: dropping it silently would leave the person's question showing facts the designer no
            # longer holds (t-269 F5), so it is refused, naming the question that exists and both texts.
            old, new = _shown(earlier), _shown(question)
            if old != new:
                raise Refused(f"- Then {then} of {case_id} was already raised as {earlier.get('id')} showing {old}; "
                              f"this entry shows {new}. One Then has one question, so nothing was added or changed. "
                              f"Expected: either the same before/now as {earlier.get('id')}, or no `raise_questions` "
                              f"entry for this Then and the ref `{earlier.get('id')}` in `then_oracles` (if the facts "
                              f"changed, the requirements tester updates {earlier.get('id')}'s before/now in "
                              "requirements-readiness.json, and the person is asked again)")
            return earlier
        data["open_questions"] = rows + [row]
        _write_readiness(path, data)
    return row


QUESTION_KEYS = ("question", "source_says", "readings", "severity", "owner_role", "before", "now")


def _question_row(rows: list, question: dict, raised_for: dict, *, taken: int = 0) -> tuple:
    """`(row | None, earlier | None)`: the ONE step that turns a built before/now question into a register row (PURE, no I/O).

    `earlier` is the row of `rows` whose `raised_for` equals `raised_for` (the key of the thing that raised it: `{case, then}` from an
    S4 case, `{claim, origin}` from an S3 claim, `{requirement | row, origin}` from a grounding line - the key spaces never compare
    equal), and then `row` is None: the caller decides
    whether the earlier question shows the same facts (`_shown`). Otherwise `row` is the new one: the next free `Q<n>` (`taken` is
    the highest number the caller has already handed out in the same move, so a batch of rows gets contiguous ids without a
    rescan of its own rows), the keys of QUESTION_KEYS the question carries, in that order (all seven for a claim and an S4 case; a
    grounding row's question has no before/now, G2-2), and `raised_for`. Every writer of a raised question -
    `_raise` here and the S3 claim projector - calls it, so a row has one shape."""
    earlier = next((r for r in rows if isinstance(r, dict) and r.get("raised_for") == raised_for), None)
    if earlier is not None:
        return None, earlier
    number = int(_next_question_id(rows)[1:])
    row = {"id": f"Q{max(number, taken + 1)}"}
    for key in QUESTION_KEYS:
        if key in question:              # a grounding row's question shows no before/now (G2-2); `C.before_now_errors` is silent on neither
            row[key] = question[key]
    row["raised_for"] = raised_for
    return row, None


def _write_readiness(path, data: dict) -> None:
    """The ONE writer of `work/requirements-readiness.json` for a raised question: the whole file, staged and replaced, in the
    serialisation the S4 door has always used (indent 2, `ensure_ascii=False`, a final newline). The caller holds `answers_lock`."""
    path = Path(path)
    staged = path.with_name(path.name + ".tmp")
    staged.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(staged, path)


def raise_for_case(task_root, case_text: str, case_id: str) -> dict:
    """The S4-exit half of O4: raise every question the case's `raise_questions` carries for a Then
    whose oracle is `unknown` with the ref `raise`, and return {"text", "raised", "problems"}.

    `text` is the case with each `raise` rewritten to its new id (in `then_oracles` and in the
    `question_thens` entry that said `raise`), and the `raise_questions` entries it used dropped (the
    line itself when none is left); None when nothing was raised, so the caller writes and re-pins only
    a case that changed. `raised` is [{case, then, question}]; `problems` one sentence per Then that
    could not be raised (no entry, a question the register refuses): that Then keeps its `raise` and the
    gate A rehearsal says so. `plan_notes` (present when something was raised) is one line per question the plan row could
    not be told about, each naming the question and the plan file; the S4 exit step prints it (FR-59). Never raises on the
    case's own data. Idempotent by (case, Then)."""
    sys.path.insert(0, str(HERE))
    import contract as C
    out = {"text": None, "raised": [], "problems": []}
    entries, _why = C.then_oracles_from_text(case_text)
    waiting = [i for i, e in enumerate(entries or []) if e.get("source") == "unknown"
               and str(e.get("ref") or "").strip() == C.RAISE_REF
               and isinstance(e.get("then"), int) and not isinstance(e.get("then"), bool)]
    if not waiting:
        return out
    asked, _why = C.parse_json_list(C.front_line(case_text, "raise_questions"))
    by_then = {a.get("then"): a for a in asked or []}
    ids: dict = {}
    replaces: dict = {}      # new question id -> the plan-row question the designer DECLARED it replaces (RN1-2)
    for index in waiting:
        then = entries[index]["then"]
        spec = by_then.get(then)
        if spec is None:
            out["problems"].append(f"{case_id}: Then {then} is `unknown` with the ref `{C.RAISE_REF}` but the case "
                                   "has no `raise_questions` entry for it")
            continue
        try:
            row = _raise(task_root, case_text, case_id, then, spec)
        except Refused as exc:
            out["problems"].append(f"{case_id}: Then {then}: {' '.join(str(exc).split())}")
            continue
        ids[then] = row["id"]
        declared = spec.get("replaces")
        if isinstance(declared, str) and declared.strip():
            replaces[row["id"]] = declared.strip()
        out["raised"].append({"case": case_id, "then": then, "question": row["id"]})
    if not ids:
        return out
    rewritten = [dict(e, ref=ids[e["then"]]) if i in waiting and e["then"] in ids else e
                 for i, e in enumerate(entries)]
    text = C.set_front_line(case_text, "then_oracles", json.dumps(rewritten, ensure_ascii=False))
    thens, _why = C.parse_json_list(C.front_line(text, "question_thens"))
    if thens is not None:
        text = C.set_front_line(text, "question_thens", json.dumps(
            [dict(t, question=ids[t["then"]]) if str(t.get("question") or "").strip() == C.RAISE_REF
             and t.get("then") in ids else t for t in thens], ensure_ascii=False))
    left = [a for a in asked or [] if a.get("then") not in ids]
    text = C.set_front_line(text, "raise_questions", json.dumps(left, ensure_ascii=False) if left else None)
    out["text"] = text
    out["plan_notes"] = _name_in_plan_row(task_root, case_text, case_id, list(dict.fromkeys(ids.values())), replaces)
    return out


def _case_plan_row(case_text: str) -> str:
    """The plan row a case belongs to: its front-matter `plan_row`, else the body line `Plan row: TS-n` - the two
    spellings `gate_brief._read_case` reads (the case reader of record; this is its twin for a text in memory)."""
    import contract as C
    row = str(C.front_line(case_text, "plan_row") or "").strip().strip("\"'")
    if row:
        return row
    found = re.search(r"(?m)^Plan row:[ \t]*(\S+)", str(case_text or ""))
    return found.group(1).strip() if found else ""


def _name_in_plan_row(task_root, case_text: str, case_id: str, question_ids: list, replaces=None) -> list:
    """HF4-9: the questions this call raised join the `question_refs` of the case's plan row, so gate A shows ONE card for
    the row's consequence (`gate_brief.contradiction_questions` skips a row whose every ref is a register id) and not
    a second one beside it. The write is `planning_contract.append_question_ref` (the code writer of the plan, one
    row-level write each; what it does not write it leaves as it was). A raise NEVER fails for the plan's sake; what was
    not written comes back as lines (the writer's reason + the plan file), which the S4 exit step prints (FR-59: no silent
    failure). This call rewrites `raise` to the new id, so it cannot run again for the same Then - there is no retry.

    RN1-2: `replaces` is `{new id: old id}` - the case designer's DECLARATION that the new question takes the place of a
    question the plan row rested on (the designer's assertion; code never infers it). For such a question the writer is
    `planning_contract.repoint_question_ref`, which moves the row's branch only between readings of the same MEANING and
    otherwise appends as above and says why the strategist's rework sets the branch."""
    notes = []
    row_id = _case_plan_row(case_text)
    where = " [plan file: work/test-plan.json]"
    try:
        import planning_contract as PC
        for qid in question_ids:
            if replaces and qid in replaces:
                _written, line = PC.repoint_question_ref(task_root, row_id, replaces[qid], qid, case_id)
            else:
                _written, line = PC.append_question_ref(task_root, row_id, qid, case_id)
            if line:
                notes.append(line + where)
    except Exception as exc:  # noqa: BLE001 - the question is raised either way
        notes.append(f"{', '.join(question_ids)} raised for {case_id}: the plan row could not be told about it "
                     f"({type(exc).__name__}: {' '.join(str(exc).split())[:160]}), so the plan is unchanged{where}")
    return notes


# --------------------------------------------------------------------------------------------
# a question a ROLE of S1-S4 raises (X2-6, t-1765): the same register, the same answers file, no second carrier (AR-13)
# --------------------------------------------------------------------------------------------

ROLE_QUESTION_STAGES = ("S1", "S2", "S3", "S4")
ROLE_OPTIONS_MIN, ROLE_OPTIONS_MAX = 2, 5
ROLE_READING_ORIGIN = "person"   # a role's option carries no origin of its own; the person's choice is its source (contract.READING_ORIGINS)


def _person_classes() -> list:
    """The ids of the person-owned classes through THE reader (`person_owned.class_ids`); [] when it cannot be read."""
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    import person_owned
    try:
        return list(person_owned.class_ids())
    except person_owned.PersonOwnedUnreadable:
        return []


def role_question_errors(spec, *, stage, asked_by) -> list:
    """Why a question a role wrote on its form (`questions[]`) cannot be raised; [] when it can. FORM ONLY (class `shape`): `question` is not
    empty; `stage` is one of S1-S4; `asked_by` is a role file of the package (`agents/<role>.md`); `options` are 2-5, each with a `reading`
    and an `if_chosen`; `severity` and `owner_role` are not blank (the rule of the S4 raise, `contract.claim_question`); `why_person` is
    `null` or an id of the person-owned classes; `read` is a list of texts (an empty one is legal: the row is raised with
    `read_missing`, a lost question is worse than an incomplete row); `recommendation` is a text when given. Whether the question is
    needed, or is answered on disk, is judged by the role and the conductor, never here (FR-12)."""
    spec = spec if isinstance(spec, dict) else {}
    problems = []
    if not str(spec.get("question") or "").strip():
        problems.append("question is empty: write the question itself, in the story's words")
    if stage not in ROLE_QUESTION_STAGES:
        problems.append(f"stage {stage!r} is not one of {', '.join(ROLE_QUESTION_STAGES)}")
    if not (isinstance(asked_by, str) and asked_by.strip() and (HERE.parent / "agents" / f"{asked_by.strip()}.md").is_file()):
        problems.append(f"asked_by {asked_by!r} is not a role of the package (a file agents/<role>.md)")
    options = spec.get("options")
    if not isinstance(options, list) or not ROLE_OPTIONS_MIN <= len(options) <= ROLE_OPTIONS_MAX:
        problems.append(f"options must be {ROLE_OPTIONS_MIN}-{ROLE_OPTIONS_MAX} answers (got "
                        f"{len(options) if isinstance(options, list) else 'none'}): one possible answer is a report, not a question")
    else:
        for i, option in enumerate(options):
            for key in ("reading", "if_chosen"):
                if not (isinstance(option, dict) and str(option.get(key) or "").strip()):
                    problems.append(f"options[{i}].{key} is empty")
    for key in ("severity", "owner_role"):
        if not str(spec.get(key) or "").strip():
            problems.append(f"{key} is blank")
    why = spec.get("why_person")
    if why is not None and why not in _person_classes():
        problems.append(f"why_person {why!r} is not a class of the person-owned list (`person_owned.class_ids`): null, or one of "
                        + (", ".join(_person_classes()) or "none readable"))
    read = spec.get("read", [])
    if not (isinstance(read, list) and all(isinstance(x, str) and x.strip() for x in read)):
        problems.append("read must be a list of `<path>#<anchor>` texts (it may be empty)")
    if "recommendation" in spec and not isinstance(spec["recommendation"], str):
        problems.append("recommendation must be a text: what you do until it is answered")
    return problems


def _same_question(a, b) -> bool:
    return " ".join(str(a or "").split()) == " ".join(str(b or "").split())


def raise_role_question(task_root, spec, *, stage, asked_by, raised_from) -> tuple:
    """`(row, written)`: add ONE role question to `open_questions` of the readiness file, or return the row that was raised for the same
    `raised_from` (`{dispatch, row}`) with the same text and write nothing (FR-7, E-X2-6c). The same `raised_from` with ANOTHER text is
    refused, naming both. The id and the readings are code's (`Q<n>`, from `options`); the text is the role's `question` key (one key for
    one fact). Raises `Refused` and writes nothing on a spec `role_question_errors` names."""
    root = Path(task_root)
    problems = role_question_errors(spec, stage=stage, asked_by=asked_by)
    if problems:
        raise Refused("\n".join(f"- {p}" for p in problems))
    path = root.joinpath(*READINESS_REL)
    with answers_lock(root):
        try:
            data = json.loads(path.read_bytes().decode("utf-8-sig"))
        except FileNotFoundError:
            raise Refused(f"- {path} does not exist: there is no register to add the question to. Expected the story's "
                          "work/requirements-readiness.json (S2 writes it)")
        except (OSError, ValueError, RecursionError):
            raise Refused(f"- {path} is not valid JSON: repair it before a question is added")
        rows = data.get("open_questions") if isinstance(data, dict) else None
        if not isinstance(data, dict) or not (rows is None or isinstance(rows, list)):
            raise Refused(f"- {path} does not hold an object with an `open_questions` list")
        rows = rows or []
        earlier = next((r for r in rows if isinstance(r, dict) and r.get("raised_from") == raised_from), None)
        if earlier is not None:
            if _same_question(earlier.get("question"), spec.get("question")):
                return earlier, False
            raise Refused(f"- {raised_from['row']} of {raised_from['dispatch']} was already raised as {earlier.get('id')}: "
                          f"{earlier.get('question')!r}; this entry says {spec.get('question')!r}. One entry is one question, so "
                          "nothing was added or changed (a changed question is a new entry on the next dispatch)")
        row = {"id": _next_question_id(rows), "question": str(spec["question"]).strip(),
               "readings": [{"reading": str(o["reading"]).strip(), "from": str(o.get("from") or ROLE_READING_ORIGIN),
                             "if_chosen": str(o["if_chosen"]).strip()} for o in spec["options"]],
               "severity": spec["severity"], "owner_role": spec["owner_role"], "asked_by": asked_by.strip(), "stage": stage,
               "read": list(spec.get("read") or []), "recommendation": str(spec.get("recommendation") or ""),
               "why_person": spec.get("why_person"), "raised_from": raised_from}
        if isinstance(spec.get("source_says"), list):
            row["source_says"] = spec["source_says"]
        if not row["read"]:
            row["read_missing"] = True
        data["open_questions"] = rows + [row]
        _write_readiness(path, data)
    return row, True


def _task_path(task_root, given):
    """The one reader of a path the driver passes in the task-relative form the role sees (`work/handoffs/<dispatch>.yaml`): an absolute
    path stays as it is, a relative one is read against the story folder, never the process cwd. A blank `given` is None (a bare
    `Path("")` is the cwd, which is never a form)."""
    text = str(given)
    if not text.strip():
        return None
    path = Path(text)
    return path if path.is_absolute() else Path(os.path.abspath(task_root)) / path


def raise_from_handoff(task_root, handoff_file, *, stage, asked_by) -> dict:
    """Raise every entry of `questions[]` of the role's handoff form (`work/handoffs/<dispatch>.yaml`) and return `{"raised": [rows written],
    "already": [rows that stood], "dispatch": id}`. ALL OR NOTHING over the form's own errors: one entry `role_question_errors` names refuses the
    call and nothing is written (a replay that changes an entry's text is refused row by row, `raise_role_question`). A form with no `questions` (or an empty list) raises nothing - the empty outcome is declared (AR-23)."""
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    import handoff
    path = _task_path(task_root, handoff_file)
    try:
        if path is None:
            raise ValueError("the path is empty")
        data = handoff.parse(path.read_text(encoding="utf-8")).data
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        raise Refused(f"- --from-handoff {str(handoff_file)!r} could not be read ({type(exc).__name__}). "
                      "Expected the role's form, work/handoffs/<dispatch>.yaml")
    entries = data.get("questions") if isinstance(data, dict) else None
    entries = entries if isinstance(entries, list) else []
    # F1 (B-11): a row whose `question` is still the contract's placeholder is the sample, not a question (the row index stays the
    # form's own, so `raised_from` of a later real row does not move).
    # Only a NON-EMPTY `<...>` text is the sample: an empty or missing `question` is still a defective entry the shape check names.
    entries = [None if (isinstance(e, dict) and isinstance(e.get("question"), str) and e["question"].strip()
                        and handoff.PLACEHOLDER.match(e["question"].strip())) else e for e in entries]
    # FV1-9 (P9): an item with `rewords` asks an existing question again; it is taken out BEFORE the shape check, so a reword's timing or
    # a malformed one never refuses the form, and run AFTER the raises (a `rewords` naming an id raised in this very form is found).
    # The index of every other entry stays the form's own.
    rewords = [(i, e) for i, e in enumerate(entries) if isinstance(e, dict) and "rewords" in e]
    entries = [None if isinstance(e, dict) and "rewords" in e else e for e in entries]
    problems = []
    for i, entry in enumerate(entries):
        if entry is None:
            continue
        problems += [f"questions[{i}]: {p}" for p in role_question_errors(entry, stage=stage, asked_by=asked_by)]
    if problems:
        raise Refused("\n".join(f"- {p}" for p in problems))
    out = {"dispatch": path.stem, "raised": [], "already": []}
    for i, entry in enumerate(entries):
        if entry is None:
            continue
        row, written = raise_role_question(task_root, entry, stage=stage, asked_by=asked_by,
                                           raised_from={"dispatch": path.stem, "row": f"questions[{i}]"})
        out["raised" if written else "already"].append(row)
    if rewords:
        out["rewords"], out["reword_problems"] = [], []
        for i, entry in rewords:
            target = entry.get("rewords")
            if not (isinstance(target, str) and target.strip()):
                out["reword_problems"].append(f"questions[{i}]: `rewords` must be the id of the question asked again")
                continue
            spec = {k: entry[k] for k in ("question", "readings", "why") if k in entry}
            try:
                reword(task_root, target, spec, role=asked_by, by="driver", stage=stage)
                out["rewords"].append(target.strip())
            except Refused as exc:
                out["reword_problems"].append(f"questions[{i}]: {target.strip()} was not asked again: {_squeeze(exc)}")
    return out


# --------------------------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------------------------

_VALUE_OPTIONS = ("--task", "--answer", "--not-needed", "--reopen", "--defer", "--keep-manual", "--automate", "--reading",
                  "--words", "--words-file", "--where", "--by", "--register-hash", "--case-ids-file",
                  "--case-file", "--then", "--question-file", "--stage", "--asked-by", "--from-handoff",
                  "--repeat", "--same-as", "--reword", "--note")
_ALL_OPTIONS = _VALUE_OPTIONS + ("--show", "--raise", "-h", "--help")


def _glue(argv: list) -> list:
    """`--words "- Q1: a"` -> `--words=- Q1: a`. argparse takes a value that starts with a hyphen for
    an option and refuses it; the person's words very often start with a list dash."""
    out, i = [], 0
    while i < len(argv):
        arg = argv[i]
        if arg in _VALUE_OPTIONS and i + 1 < len(argv) and argv[i + 1] not in _ALL_OPTIONS:
            out.append(f"{arg}={argv[i + 1]}")
            i += 2
        else:
            out.append(arg)
            i += 1
    return out


def _refuse(message: str) -> int:
    print(f"{COMMAND}: refused.\n{message}", file=sys.stderr)
    return 2


def _read_text_file(option: str, name: str):
    """(text, problem): the file's text, whole (a BOM and CRLF kept), or what is wrong with it."""
    try:
        raw = Path(name).read_bytes()
    except OSError as exc:
        return None, f"{option} {name!r} could not be read ({type(exc).__name__}). Expected the path of a UTF-8 text file"
    try:
        return raw.decode("utf-8"), ""
    except UnicodeDecodeError:
        return None, f"{option} {name!r} is not UTF-8 text. Expected a UTF-8 file (save it as UTF-8, not UTF-16)"


def _story_case_ids(root: Path) -> list:
    """The full case ids of the story from its pinned links - a light JSON read, no other module."""
    try:
        data = json.loads(root.joinpath(*CASE_LINKS_REL).read_bytes().decode("utf-8-sig", errors="replace"))
    except (OSError, ValueError, RecursionError):
        return []
    links = data.get("links") if isinstance(data, dict) else None
    ids = [link["case_id"].strip() for link in (links if isinstance(links, list) else [])
           if isinstance(link, dict) and isinstance(link.get("case_id"), str) and link["case_id"].strip()]
    return list(dict.fromkeys(ids))


def _checked_stage(value: str):
    """(stage, problem) for a `--stage` value: "" for a blank one (never refused), the stripped id when `stages.json` names it
    (read through `acceptance.stage_def_of`, no case folding), else "" and what is wrong with it, what was expected and the ids."""
    stage = (value or "").strip()
    if not stage:
        return "", ""
    import acceptance
    import null_outcomes
    if acceptance.stage_def_of(stage):
        return stage, ""
    shown = repr(stage if len(stage) <= 80 else stage[:80] + "...")
    ids = sorted(null_outcomes.stage_ids(), key=lambda i: (int(re.sub(r"\D", "", i) or 0), i))
    if not ids:
        return "", (f"--stage {shown} cannot be checked: the stage table could not be read (references/stages.json). "
                    "Expected a stage id; leave --stage out to record none")
    return "", f"--stage {shown} is not a stage of the factory. Valid: " + ", ".join(ids) + " (or leave --stage out)"


def _main_fv19(root: Path, ns, operation: str) -> int:
    """The three FV1-9 operations of the CLI (the conductor's door; a role reaches the same writers through its form):
    `--repeat QID --same-as QID`, `--reword QID --question-file`, `--note QID`. The role is `conductor`; the stage is the
    conductor's `--stage` (a stage id of stages.json; blank records "", as an older hand-over did), `--note` has none."""
    flag = f"--{operation}"
    stray = [name for name, value in (("--reading", ns.reading), ("--register-hash", ns.register_hash),
                                      ("--case-ids-file", ns.case_ids_file), ("--case-file", ns.case_file), ("--then", ns.then),
                                      ("--question-file", ns.question_file if operation != "reword" else ""),
                                      ("--words", ns.words if operation == "reword" else None),
                                      ("--words-file", ns.words_file if operation == "reword" else "")) if value]
    vocab = vocabulary()
    problems = [f"{name} has no meaning with {flag}; drop it" for name in stray]
    stage = ""
    if operation != "note":                      # `main`'s guard already refused a `--stage` with `--note`
        stage, why = _checked_stage(ns.stage)
        if why:
            problems.append(why)
    for value, key, name, what in ((ns.where, "where", "--where", "where it was written"), (ns.by, "by", "--by", "who wrote it")):
        if not value:
            problems.append(f"{name} is missing: say {what} (there is no default). Valid: " + ", ".join(vocab[key]))
        elif value not in vocab[key]:
            problems.append(f"{key} {value!r} is not a known value. Valid: " + ", ".join(vocab[key]))
    words, spec = None, None
    if operation == "reword":
        if not ns.question_file:
            problems.append("--reword needs --question-file: a JSON object {question, why, readings?}")
        else:
            text, why = _read_text_file("--question-file", ns.question_file)
            try:
                spec = json.loads(text) if not why else None
            except (ValueError, RecursionError):
                spec, why = None, f"--question-file {ns.question_file!r} is not valid JSON. Expected one object"
            if why:
                problems.append(why)
    else:
        if operation == "repeat" and not ns.same_as:
            problems.append("--repeat needs --same-as: the id of the earlier question it repeats")
        if ns.words_file and ns.words is not None:
            problems.append("give the words with exactly one of --words and --words-file, not both")
        elif ns.words_file:
            words, why = _read_text_file("--words-file", ns.words_file)
            if why:
                problems.append(why)
        elif ns.words is None:
            problems.append("the words are blank. Expected " + ("the why, one line: what both questions ask" if operation == "repeat"
                                                               else "what helps the person answer") + " (pass them with exactly one of --words and --words-file)")
        else:
            words = ns.words
    if problems:
        return _refuse("\n".join(f"- {p}" for p in problems))
    target = ns.repeat or ns.reword or ns.note
    try:
        if operation == "repeat":
            rec = declare_repeat(root, target, ns.same_as, words, by=ns.by, declared_by="conductor", stage=stage)
            print(json.dumps({"recorded": rec}, ensure_ascii=False, indent=2))
        elif operation == "reword":
            row = reword(root, target, spec, role="conductor", by=ns.by, stage=stage)
            print(json.dumps({"reworded": row}, ensure_ascii=False, indent=2))
        else:
            rec = record_note(root, target, words, by=ns.by, where=ns.where)
            print(json.dumps({"recorded": rec}, ensure_ascii=False, indent=2))
    except Refused as exc:
        return _refuse(str(exc))
    return 0


def main(argv=None) -> int:
    try:
        import console_io
        console_io.utf8_stdio()
    except ImportError:
        pass
    sys.path.insert(0, str(HERE))
    import hooklib  # noqa: E402  (the parser's one spelling of "exact flags" is hooklib's)
    ap = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    ap.add_argument("--task", required=True, help="the ticket id")
    ap.add_argument("--show", action="store_true", help="print every question with its status and row_hash; writes nothing")
    ap.add_argument("--answer", default="", metavar="QID", help="record an answer (add --reading a|b|... when the person chose one)")
    ap.add_argument("--not-needed", dest="not_needed", default="", metavar="QID", help="record `not needed`")
    ap.add_argument("--reopen", default="", metavar="QID", help="put the question back to open")
    ap.add_argument("--defer", default="", metavar="QID",
                    help="record `until the report`: the question stays open on the person's word, is not asked again, "
                         "and the report lists it (--reopen puts it back)")
    ap.add_argument("--keep-manual", dest="keep_manual", default="", metavar="CASE_ID",
                    help="record the person's word `<full case id>: manual`")
    ap.add_argument("--automate", default="", metavar="CASE_ID", help="record the person's word `<full case id>: automate`")
    ap.add_argument("--reading", default="", help="the letter of the chosen reading (with --answer)")
    ap.add_argument("--words", default=None, help="the person's words, whole (a write needs this or --words-file)")
    ap.add_argument("--words-file", dest="words_file", default="", metavar="PATH",
                    help="a UTF-8 file holding the person's words, whole (instead of --words; a command line is short)")
    ap.add_argument("--where", default="", help="REQUIRED with a write: where it was asked; a value of references/question-vocabulary.json")
    ap.add_argument("--by", default="", help="REQUIRED with a write: who recorded it; a value of references/question-vocabulary.json")
    ap.add_argument("--register-hash", dest="register_hash", default="", metavar="HASH",
                    help="the `row_hash` --show printed for the question when it was shown (required with --answer and --not-needed)")
    ap.add_argument("--case-ids-file", dest="case_ids_file", default="", metavar="PATH",
                    help="the story's full case ids, one per line (with --keep-manual / --automate; else the story's case links are read)")
    ap.add_argument("--raise", dest="raise_question", action="store_true",
                    help="add a before/now question after S2 (with --case-file, --then and --question-file)")
    ap.add_argument("--case-file", dest="case_file", default="", metavar="PATH", help="the case the question is for (with --raise)")
    ap.add_argument("--then", dest="then", default="", metavar="N", help="the number of the Then the question is for (with --raise)")
    ap.add_argument("--question-file", dest="question_file", default="", metavar="PATH",
                    help="a UTF-8 JSON file {question, source_says, severity, owner_role, before: {value, where}, "
                         "now: {value, where}} (with --raise)")
    ap.add_argument("--stage", default="", help="with --raise --from-handoff, --repeat or --reword: the stage (a stage id of "
                                                "references/stages.json, e.g. S3) the question was asked at; blank = not recorded")
    ap.add_argument("--asked-by", dest="asked_by", default="", metavar="ROLE", help="with --raise --from-handoff: the role that asked")
    ap.add_argument("--from-handoff", dest="from_handoff", default="", metavar="PATH",
                    help="with --raise: raise every `questions[]` entry of this role's form work/handoffs/<dispatch>.yaml "
                         "(instead of --case-file/--then/--question-file)")
    ap.add_argument("--repeat", default="", metavar="QID",
                    help="mark the question as asking what --same-as asks (the words are the why; --where, --by); the person is asked once")
    ap.add_argument("--same-as", dest="same_as", default="", metavar="QID", help="with --repeat: the id of the earlier question it repeats")
    ap.add_argument("--reword", default="", metavar="QID",
                    help="ask an unanswered question the person was shown again in clearer words (--question-file: a JSON object "
                         "{question, why, readings?}; --where, --by); the id stays")
    ap.add_argument("--note", default="", metavar="QID",
                    help="record what helps the person answer the question (the words; --where, --by); shown on its card while the row is as it was")
    ns = hooklib.exact_options(ap).parse_args(_glue(list(sys.argv[1:] if argv is None else argv)))
    operations = [("show", ns.show), ("answer", ns.answer), ("not-needed", ns.not_needed), ("reopen", ns.reopen),
                  ("defer", ns.defer), ("keep-manual", ns.keep_manual), ("automate", ns.automate), ("raise", ns.raise_question),
                  ("repeat", ns.repeat), ("reword", ns.reword), ("note", ns.note)]
    chosen = [name for name, value in operations if value]
    if len(chosen) != 1:
        return _refuse("- name exactly one operation: --show, --answer QID, --not-needed QID, --reopen QID, "
                       "--defer QID, --keep-manual CASE_ID, --automate CASE_ID, --raise, --repeat QID, --reword QID or --note QID "
                       f"(got {len(chosen)}: {', '.join(chosen) or 'none'})")
    try:
        vocabulary()
    except RuntimeError as exc:
        print(f"{COMMAND}: {exc}", file=sys.stderr)
        return 1
    from hooklib import story_root  # noqa: E402  (only the CLI needs the project)
    try:
        root = story_root(ns.task, "question_register.py --task")     # the story EXISTS, or a refusal and nothing written
    except ValueError as exc:
        return _refuse(f"- {exc}")
    is_case = chosen[0] in ("keep-manual", "automate")
    guard = ([] if ns.raise_question or not (ns.asked_by or ns.from_handoff)
             else ["--asked-by and --from-handoff go with --raise only"])
    if ns.stage and not (ns.raise_question or chosen[0] in ("repeat", "reword")):
        guard.append("--stage goes with --raise --from-handoff, --repeat or --reword only")
    if guard:
        return _refuse("\n".join(f"- {line}" for line in guard))
    if ns.raise_question and ns.from_handoff:
        stray = [flag for flag, value in (("--words", ns.words), ("--words-file", ns.words_file), ("--reading", ns.reading),
                                          ("--where", ns.where), ("--by", ns.by), ("--register-hash", ns.register_hash),
                                          ("--case-ids-file", ns.case_ids_file), ("--case-file", ns.case_file), ("--then", ns.then),
                                          ("--question-file", ns.question_file)) if value]
        missing = [flag for flag, value in (("--stage", ns.stage.strip()), ("--asked-by", ns.asked_by)) if not value]
        if stray or missing:
            return _refuse((f"- --raise --from-handoff needs {', '.join(missing)}" if missing else "")
                           + ("\n" if stray and missing else "")
                           + (f"- {', '.join(stray)} has no meaning with --raise --from-handoff; drop it" if stray else ""))
        stage, why = _checked_stage(ns.stage)
        if why:
            return _refuse(f"- {why}")
        try:
            result = raise_from_handoff(root, ns.from_handoff, stage=stage, asked_by=ns.asked_by)
        except Refused as exc:
            return _refuse(str(exc))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    if ns.raise_question:
        stray = [flag for flag, value in (("--words", ns.words), ("--words-file", ns.words_file), ("--reading", ns.reading),
                                          ("--where", ns.where), ("--by", ns.by), ("--register-hash", ns.register_hash),
                                          ("--case-ids-file", ns.case_ids_file), ("--stage", ns.stage),
                                          ("--asked-by", ns.asked_by)) if value]
        missing = [flag for flag, value in (("--case-file", ns.case_file), ("--then", ns.then),
                                            ("--question-file", ns.question_file)) if not value]
        if stray or missing:
            return _refuse((f"- --raise needs {', '.join(missing)}" if missing else "")
                           + ("\n" if stray and missing else "")
                           + (f"- {', '.join(stray)} has no meaning with --raise; drop it" if stray else ""))
        text, why = _read_text_file("--question-file", ns.question_file)
        try:
            spec = json.loads(text) if not why else None
        except (ValueError, RecursionError):
            spec, why = None, f"--question-file {ns.question_file!r} is not valid JSON. Expected one object"
        if why:
            return _refuse(f"- {why}")
        try:
            number = int(ns.then)
        except ValueError:
            return _refuse(f"- --then {ns.then!r} is not a number. Expected the number of the item under `## Then`")
        try:
            row = raise_question(root, ns.case_file, number, spec)
        except Refused as exc:
            return _refuse(str(exc))
        print(json.dumps({"raised": row, "case_file": ns.case_file, "then": number}, ensure_ascii=False, indent=2))
        return 0
    if ns.show:
        stray = [flag for flag, value in (("--words", ns.words), ("--words-file", ns.words_file), ("--reading", ns.reading),
                                          ("--where", ns.where), ("--by", ns.by), ("--register-hash", ns.register_hash),
                                          ("--case-ids-file", ns.case_ids_file)) if value]
        if stray:
            return _refuse(f"- --show writes nothing, so {', '.join(stray)} has no meaning with it; drop it")
        print(json.dumps(load(root), ensure_ascii=False, indent=2))
        return 0
    if ns.same_as and not ns.repeat:
        return _refuse("- --same-as goes with --repeat only")
    if chosen[0] in ("repeat", "reword", "note"):
        return _main_fv19(root, ns, chosen[0])
    problems = []
    words = ns.words
    if ns.words_file and ns.words is not None:
        problems.append("give the words with exactly one of --words and --words-file, not both")
    elif ns.words_file and chosen[0] == "defer":
        try:   # the person's words by file, through the one reader (BOM off, UTF-8 strict, an empty file refused)
            words = _person_words().read(None, ns.words_file, "--words")
        except ValueError as exc:   # person_words.WordsRefused
            problems.append(str(exc))
    elif ns.words_file:
        words, why = _read_text_file("--words-file", ns.words_file)
        if why:
            problems.append(why)
    elif ns.words is None:
        problems.append("the words are blank. Expected the person's own words, whole, so the answer stays "
                        "attributable (pass them with exactly one of --words and --words-file)")
    if ns.case_ids_file and not is_case:
        problems.append("--case-ids-file has no meaning with a question operation; drop it")
    if is_case and ns.reading:
        problems.append("a reading letter goes only with an answer, not with a case decision")
    case_ids, source = None, "none: no case ids found, any non-empty id was accepted"
    if is_case and not problems:
        if ns.case_ids_file:
            text, why = _read_text_file("--case-ids-file", ns.case_ids_file)
            if why:
                problems.append(why)
            else:
                case_ids = list(dict.fromkeys(x.strip() for x in _lines(text.lstrip(BOM)) if x.strip()))
                source = "--case-ids-file"
        else:
            case_ids = _story_case_ids(root) or None
            if case_ids is not None:
                source = "state/story-case-links.json"
    if problems:
        return _refuse("\n".join(f"- {p}" for p in problems))
    try:
        if is_case:
            target = ns.keep_manual or ns.automate
            rec = record_case(root, target, "manual" if ns.keep_manual else "automate", words if words is not None else "",
                              ns.where, ns.by, case_ids=case_ids, shown_hash=ns.register_hash)
            decision = load(root)["case_decisions"].get(rec["case"])
            print(json.dumps({"recorded": rec, "case_decision": decision, "case_ids_checked_against": source},
                             ensure_ascii=False, indent=2))
            return 0
        status = {"answer": "answered", "not-needed": "not_needed", "reopen": "open", "defer": DEFERRED}[chosen[0]]
        qid = ns.answer or ns.not_needed or ns.reopen or ns.defer
        rec = record(root, qid, status, words if words is not None else "", ns.where, ns.by, ns.register_hash,
                     reading=ns.reading)
    except Refused as exc:
        return _refuse(str(exc))
    after = next((q for q in load(root)["questions"] if q["id"] == rec["id"]), None)
    print(json.dumps({"recorded": rec, "question": after}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
