"""retro_numbers.py: the resumes of role sessions, counted per stage with their wall time (t-342, B-273; FR-26, FR-41).

man1 02.10: the S7 analyst was resumed twice (0.9 and 0.6 min) and the S8 scribe once (2.4 min) - about five minutes of
22 - and the retro said nothing of it. The retro now carries, per stage, how many times a role's session was resumed, the
wall time of those calls and the reason each gave (`resume_reason`, written by the driver since B-273), counted from the
driver's own journal (`state/driver-runs.jsonl`: rows of `kind: role` with `resumed: true`), and how many handoffs the
driver built by code instead of resuming (`state/driver-runs/<dispatch>.json` with `assembled_by: code`).

What is held here: the numbers add up from a journal written by hand; a row from before the reason field reads as
`no reason recorded`; a row with no usable duration is counted and never read as zero seconds; a story with no journal
at all is `unknown`, not "no resumes"; the line names its carrier; facts written before the key existed render nothing.

Run on its own: `python -B scripts/tests/test_retro_numbers.py`.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import SCRIPTS, check, check_eq, check_in, check_not_in, cleanup, finish, temp_dir  # noqa: E402

sys.path.insert(0, str(SCRIPTS))
import retro_numbers as RN  # noqa: E402
import run_counters as RC  # noqa: E402
import driver_journal as DJ  # noqa: E402
import driver_timing as DT  # noqa: E402
import friction as FR  # noqa: E402

CLASS_FORM = "the role's final message is not the handoff form"
CLASS_HANDOVER = "the handover form is not complete"


def row(stage: str, role: str, session: str, **extra) -> dict:
    base = {"kind": "role", "role": role, "dispatch": f"{stage}-{role}-1", "stage": stage, "session_id": session,
            "num_turns": 5, "total_cost_usd": 1.0, "resumed": False, "ts": "2026-10-02T10:00:00+00:00"}
    base.update(extra)
    return base


def project() -> tuple:
    root = temp_dir("qa-retro-numbers-")
    base = root / "qa-factory"
    troot = base / "artifacts" / "QA-1"
    (base / "state" / "cost").mkdir(parents=True)
    (troot / "work").mkdir(parents=True)
    (troot / "state" / "driver-runs").mkdir(parents=True)
    (base / "config.json").write_text("{}", encoding="utf-8")
    (troot / "pipeline.json").write_text(json.dumps({"ticket": "QA-1", "size": "M", "stages": {}}), encoding="utf-8")
    (troot / "work" / "test-plan.json").write_text("[]", encoding="utf-8")
    return root, base, troot


def write_journal(troot: Path, rows: list) -> None:
    (troot / "state" / "driver-runs.jsonl").write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")


def the_resumes_add_up_per_stage() -> None:
    root, base, troot = project()
    try:
        write_journal(troot, [
            row("S2", "qa-requirements-tester", "a", duration_ms=600000),
            row("S2", "qa-requirements-tester", "a", resumed=True, duration_ms=54000, resume_reason=CLASS_FORM),
            row("S7", "qa-failure-analyst", "b", duration_ms=300000),
            row("S7", "qa-failure-analyst", "b", resumed=True, duration_ms=36000, resume_reason=CLASS_HANDOVER),
            row("S7", "qa-failure-analyst", "b", resumed=True, duration_ms=54000, resume_reason=CLASS_HANDOVER),
            # a row from before the reason field, and one with no duration at all
            row("S8", "qa-doc-scribe", "c", resumed=True, duration_ms=144000),
            row("S8", "qa-doc-scribe", "c", resumed=True),
            # not role resumes: a conductor call, a resumed flag that is not the boolean, a launch
            {"kind": "conductor", "role": "", "stage": "S2", "session_id": "k", "resumed": True, "duration_ms": 999000},
            row("S9", "qa-retro-analyst", "d", resumed="true", duration_ms=999000),
        ])
        (troot / "state" / "driver-runs" / "S2-qa-requirements-tester-1.json").write_text(
            json.dumps({"result": "x", "assembled_by": "code"}), encoding="utf-8")
        (troot / "state" / "driver-runs" / "S7-qa-failure-analyst-1.done.json").write_text(
            json.dumps({"result": "x", "assembled_by": "code"}), encoding="utf-8")
        (troot / "state" / "driver-runs" / "S8-qa-doc-scribe-1.json").write_text(
            json.dumps({"result": "x"}), encoding="utf-8")
        data = RN.numbers("QA-1", base, troot)
        got = data["resumes"]
        check_eq("the journal is the carrier, and the story's key says so", got["known"], True)
        check_in("named with the rows it counts", "state/driver-runs.jsonl", got["carrier"])
        check_eq("F6: the cost of a resume is unknown, not a guess (a resumed session's total is cumulative)", got["cost"], "unknown (B-219)")
        check_eq("five resumes of role sessions (the conductor and a non-boolean flag are not)", got["count"], 5)
        check_eq("their wall time is the sum of the calls that carry a duration", got["wall_s"], 288)
        check_eq("one call has no duration: counted, never zero seconds", got["wall_unmeasured"], 1)
        check_eq("two rows name no reason (a row from before the field, and the one with no duration)", got["no_reason"], 2)
        check_eq("S2: one resume, 54 s, its reason", (got["by_stage"]["S2"]["count"], got["by_stage"]["S2"]["wall_s"], got["by_stage"]["S2"]["reasons"]),
                 (1, 54, {CLASS_FORM: 1}))
        check_eq("S7: two resumes, 90 s, one reason twice", (got["by_stage"]["S7"]["count"], got["by_stage"]["S7"]["wall_s"], got["by_stage"]["S7"]["reasons"]),
                 (2, 90, {CLASS_HANDOVER: 2}))
        check_eq("S8: two resumes, 144 s measured, one not, both with `no reason recorded`",
                 (got["by_stage"]["S8"]["count"], got["by_stage"]["S8"]["wall_s"], got["by_stage"]["S8"]["wall_unmeasured"], got["by_stage"]["S8"]["reasons"]),
                 (2, 144, 1, {"no reason recorded": 2}))
        check_eq("a stage with no resume is not listed", sorted(got["by_stage"]), ["S2", "S7", "S8"])
        check_eq("two handoffs were assembled by code instead of resuming, by the stage the dispatch names",
                 (got["assembled_by_code"], got["assembled_by_stage"]), (2, {"S2": 1, "S7": 1}))
        lines = RN.resume_lines(got)
        text = "\n".join(lines)
        check_in("the headline: the count, the wall time, the unmeasured call, the carrier",
                 "**Resumes of role sessions:** 5, 4m 48s of wall time (1 call has no recorded duration) — counted from state/driver-runs.jsonl", text)
        check_in("S2's line carries its reason", f"- S2: 1 · 0m 54s — {CLASS_FORM} ×1", text)
        check_in("S7's line carries the repeat", f"- S7: 2 · 1m 30s — {CLASS_HANDOVER} ×2", text)
        check_in("a row with no reason says so", "no reason recorded ×2", text)
        check_in("the resumes that did not happen are counted", "handoffs the driver assembled by code instead of resuming the role: 2 (S2 1, S7 1)", text)
        check_in("the retro's own render carries the block", "**Resumes of role sessions:** 5", RN.render(data))
        check_in("and so does the JSON form of the facts", '"resumes"', json.dumps(data, default=str))
    finally:
        cleanup(root)


def the_unknown_and_the_empty_are_not_the_same() -> None:
    root, base, troot = project()
    try:
        none = RN.numbers("QA-1", base, troot)["resumes"]
        check_eq("no driver journal: the measurement is unknown, not zero", (none["known"], "no driver journal" in none["reason"]), (False, True))
        text = "\n".join(RN.resume_lines(none))
        check_in("and the line says unknown, with the carrier", "**Resumes of role sessions:** unknown", text)
        check_in("naming where it would have been counted", "state/driver-runs.jsonl", text)
        write_journal(troot, [row("S2", "qa-requirements-tester", "a", duration_ms=1000)])
        zero = RN.numbers("QA-1", base, troot)["resumes"]
        check_eq("a journal with launches and no resume: known, zero", (zero["known"], zero["count"], zero["wall_s"], zero["by_stage"]), (True, 0, 0, {}))
        line = "\n".join(RN.resume_lines(zero))
        check_in("zero resumes is said as a count", "**Resumes of role sessions:** 0 — counted from", line)
        check_not_in("with no wall time invented", "wall time", line)
        # the odd durations of a hand-written or damaged row
        write_journal(troot, [row("S3", "qa-test-strategist", "e", resumed=True, duration_ms=value) for value in
                              (True, -5, "9", None, 1500)])
        odd = RN.numbers("QA-1", base, troot)["resumes"]
        check_eq("a boolean, a negative, a text and a null duration are not seconds; 1500 ms is", (odd["count"], odd["wall_unmeasured"], odd["wall_s"]), (5, 4, 2))
        # a garbage line in the journal does not take the retro down
        (troot / "state" / "driver-runs.jsonl").write_text('not json\n[1, 2]\n' + json.dumps(row("S3", "qa-test-strategist", "e", resumed=True, duration_ms=2000)) + "\n", encoding="utf-8")
        check_eq("an unreadable line is skipped", RN.numbers("QA-1", base, troot)["resumes"]["count"], 1)
        # facts written before the key existed render nothing, and no exception
        check_eq("facts without the key render no line", RN.resume_lines(None), [])
        check_eq("and a render of such facts still works", "Resumes of role sessions" in RN.render({k: v for k, v in RN.numbers("QA-1", base, troot).items() if k != "resumes"}), False)
    finally:
        cleanup(root)


DIGEST_HEAD = "digest: your final message is not the handoff form. The orchestrator reads it whole on every later turn"


def write_records_journal(base: Path, rows: list) -> None:
    path = base / "records" / "journal.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")


def block(first: str, n: int = 1, event: str = "gate_block") -> dict:
    return {"event": event, "agent": "exit_gate", "notes": f"block 1/1; broken artifacts: {n}; first: {first}"}


def the_class_of_a_gate_block_has_one_reader() -> None:
    """R1 + B-4 (F6-51): the class is the FIRST finding, cut at '; ' then 60 characters, from ONE function the dashboard calls."""
    import factory_dashboard as D
    notes = "block 1/1; broken artifacts: %d; first: s5_precheck.py: REAL exit 1 on the gate re-run"
    check_eq("R1: the three cases of test_retry_reason.py give the same results through the new function",
             (RN.gate_block_class(notes % 1) == RN.gate_block_class(notes % 2),
              RN.gate_block_class("something else entirely")), (True, "something else entirely"))
    check_eq("R1: and the dashboard's reader IS that function's answer",
             [D.gate_block_finding(n) for n in (notes % 1, "something else entirely", "", None)],
             [RN.gate_block_class(n) for n in (notes % 1, "something else entirely", "", None)])
    check_eq("E13: empty notes are counted under a class of their own, not dropped", RN.gate_block_class(""), "(no finding text)")
    check_eq("E13: a missing notes field too", RN.gate_block_class(None), "(no finding text)")
    check_eq("E13: a `first: ` with nothing after it", RN.gate_block_class("block 1/1; first: "), "(no finding text)")
    long = "x" * 100
    check_eq("E13: notes longer than 60 characters after `first: ` are cut AT 60", RN.gate_block_class("first: " + long), "x" * 60)
    check_eq("E13: 59 and 60 characters are kept whole",
             (RN.gate_block_class("first: " + "y" * 59), RN.gate_block_class("first: " + "y" * 60)), ("y" * 59, "y" * 60))
    one = "s5_precheck.py: REAL exit 1 on the gate re-run"
    check_eq("B-4: the same first finding followed by different second findings is ONE class (the under-count side is closed)",
             {RN.gate_block_class(f"block 1/1; first: {one}; witness: run-report.json is stale"),
              RN.gate_block_class(f"block 1/1; first: {one}; case TC-003: no basis"),
              RN.gate_block_class(f"block 1/1; first: {one}")}, {one})


def the_gate_block_line_is_measured_not_assumed() -> None:
    import stage_joints as SJ
    root, base, troot = project()
    saved = SJ.DATA
    try:
        write_records_journal(base, [{"event": "compact", "notes": "x"}])
        counted = RN.numbers("QA-1", base, troot)["journal"]
        check_eq("R2/E10: a journal with no gate_block: known, no class, no worst, no signal",
                 (counted["known"], counted["gate_block_classes"]["classes"], counted["gate_block_classes"]["worst"],
                  counted["gate_block_classes"]["signal"]), (True, {}, None, False))
        check_in("R2: the line is a measured zero", "**Gate blocks by class:** none (0) (records/journal.jsonl).", "\n".join(RN.journal_lines(counted)))
        check_in("R2: and the old counts print as numbers", "**gate blocks:** 0 (the norm is zero)", "\n".join(RN.journal_lines(counted)))
        digest = [block(DIGEST_HEAD + f" — one row per item for role {role}", n) for n, role in
                  zip(range(1, 18), ["qa-scout", "qa-runner", "qa-doc-scribe"] * 6)]
        write_records_journal(base, digest)
        data = RN.numbers("QA-1", base, troot)
        classes = data["journal"]["gate_block_classes"]
        check_eq("R3: 17 digest blocks from three roles, the real 12586 refusal head: ONE class x17 and the signal",
                 (list(classes["classes"].values()), classes["worst"][1], classes["signal"]), ([17], 17, True))
        check_in("R3: the retro prints the class line", "**Gate blocks by class:** " + DIGEST_HEAD[:60] + " ×17", RN.render(data))
        check_in("R3: and the observation, with the rule it breaks", "17 gate blocks of one class", "\n".join(RN.observations(data)))
        check_in("R3: naming the cause is the factory's", "not of the role; it is a finding", "\n".join(RN.observations(data)))
        for count, signal in ((3, True), (2, False), (4, True), (1, False)):
            write_records_journal(base, [block("one finding")] * count)
            got = RN.numbers("QA-1", base, troot)
            check_eq(f"R4/E12: {count} blocks of one class at threshold 3: signal {signal}",
                     got["journal"]["gate_block_classes"]["signal"], signal)
            check_eq(f"R4: and the observation follows the signal ({count})",
                     any("gate blocks of one class" in line for line in RN.observations(got)), signal)
        write_records_journal(base, [block("a")] * 2 + [block("b")] * 2 + [block("c")] * 2)
        check_eq("R4: six blocks in three classes of two each are NOT a signal (the class is the unit)",
                 RN.numbers("QA-1", base, troot)["journal"]["gate_block_classes"]["signal"], False)
        write_records_journal(base, [block("one finding")] * 2 + [block("one finding", event="unsafe_completion")] * 5)
        got = RN.numbers("QA-1", base, troot)["journal"]
        check_eq("R4/E14: unsafe_completion rows are not a class (the existing total still counts them)",
                 (got["gate_block_classes"]["classes"], got["gate_blocks"], got["gate_block_classes"]["signal"]),
                 ({"one finding": 2}, 7, False))
        # R6/E9: the threshold unreadable -> the line says so, no observation, no hidden number
        write_records_journal(base, [block("one finding")] * 9)
        tmp = temp_dir("qa-thr-")
        try:
            (tmp / "no-friction.json").write_text(json.dumps({"joints": []}), encoding="utf-8")
            SJ.DATA = tmp / "no-friction.json"
            got = RN.numbers("QA-1", base, troot)
            check_in("R6/E9: with no threshold the classes are printed and the line says `threshold unknown`",
                     "one finding ×9 (records/journal.jsonl) · threshold unknown (references/stage-joints.json).", RN.render(got))
            check_eq("R6: and no observation is made from a number nobody set", (got["journal"]["gate_block_classes"]["signal"],
                     any("gate blocks of one class" in line for line in RN.observations(got))), (False, False))
        finally:
            SJ.DATA = saved
            cleanup(tmp)
    finally:
        SJ.DATA = saved
        cleanup(root)


def a_missing_journal_prints_unknown_beside_no_zero() -> None:
    """R5 + B-3 (FR-10, FR-41): ONE `known` for the journal line; an absent journal prints `unknown` for every count."""
    root, base, troot = project()
    try:
        data = RN.numbers("QA-1", base, troot)
        journal = data["journal"]
        check_eq("R5/E11: no journal file: known False, no signal", (journal["known"], journal["gate_block_classes"]["known"],
                 journal["gate_block_classes"]["signal"]), (False, False, False))
        text = RN.render(data)
        check_in("R5: the class line says unknown, with its carrier", "**Gate blocks by class:** unknown — no journal (records/journal.jsonl).", text)
        check_in("R5b: and the rejects/gate blocks/compacts line says unknown for each", "**Rejects:** unknown · **gate blocks:** unknown · **compacts:** unknown", text)
        check_not_in("R5b: no zero is printed beside the unknown (the norm-is-zero sentence is for a measured zero)", "(the norm is zero)", text)
        check_eq("R5b: and the observations stay silent about gate blocks", any("gate block" in line for line in RN.observations(data)), False)
        facts_before = {k: v for k, v in data["journal"].items() if k not in ("known", "carrier", "gate_block_classes")}
        check_in("a facts file written before `known` existed prints its counts as before",
                 "**gate blocks:** 3 (the norm is zero)", "\n".join(RN.journal_lines({**facts_before, "gate_blocks": 3})))
        write_records_journal(base, [block("one finding")])
        check_eq("R5 (positive control): the same project WITH a journal is known", RN.numbers("QA-1", base, troot)["journal"]["known"], True)
    finally:
        cleanup(root)


def the_rules_cost_is_never_silently_smaller_than_the_whole() -> None:
    """RC1-14 B-2 (FR-41, AR-22): a role the measure could not read is named beside the total; an unreadable role-load.json
    is an `unknown` line with its reason, never a line that vanishes."""
    import role_load as RL
    rows = [{"role": "qa-scout", "requests": 10}, {"role": "qa-runner", "requests": 10}]
    whole = RN.rules_weight(rows, "claude-sonnet-4-5")
    check_eq("K-B2: with both roles readable nothing is unmeasured", ("unmeasured_roles" in whole, sorted(whole["by_role"])),
             (False, ["qa-runner", "qa-scout"]))
    real = RL.static_load

    def partly_unreadable(role, *args, **kw):
        load = real(role, *args, **kw)
        if role == "qa-runner":      # some of the charter's files could not be read: bytes of the readable ones, measured false
            for layer in load["layers"]:
                if layer["name"] == "charter":
                    layer["measured"] = False
        return load

    RL.static_load = partly_unreadable
    try:
        partial = RN.rules_weight(rows, "claude-sonnet-4-5")
    finally:
        RL.static_load = real
    check_eq("K-B2: a PARTLY unreadable layer is unmeasured, not priced as a whole", (sorted(partial["by_role"]), partial["unmeasured_roles"]),
             (["qa-scout"], ["qa-runner"]))
    text = RN.render({"task": "T", "story": {"usd": 1.0, "tokens": 1}, "orchestrator_share_percent": None, "rules_weight": partial})
    check_in("K-B2: the retro prints the unmeasured role beside the total", "Not measured, so left out of this total: qa-runner", text)
    check_in("K-B2: ... next to the priced sentence", "The rules cost", text)
    nowhere = RN.render({"task": "T", "story": {"usd": 1.0, "tokens": 1}, "orchestrator_share_percent": None, "rules_weight": whole})
    check_not_in("K-B2: with every role measured the line is not there", "Not measured, so left out", nowhere)
    unrated = dict(partial, rate_per_mtok=None, usd=None, by_layer=None, reason="no rate")
    check_in("K-B2: an unknown-rate line names the unmeasured role too", "qa-runner",
             RN.render({"task": "T", "story": {"usd": 1.0, "tokens": 1}, "orchestrator_share_percent": None, "rules_weight": unrated}))
    # the except: an unreadable role-load.json
    real_settings = RL.settings

    def broken(*args, **kw):
        raise RL.RoleLoadError("references/role-load.json could not be read - the role start load was not measured")

    RL.settings = broken
    try:
        unknown = RN.rules_weight(rows, "claude-sonnet-4-5")
    finally:
        RL.settings = real_settings
    check("K-B2: an unreadable role-load.json is an `unknown` answer with the reason, not {}",
          bool(unknown.get("unknown")) and "role-load.json could not be read" in unknown["unknown"], str(unknown))
    text = RN.render({"task": "T", "story": {"usd": 1.0, "tokens": 1}, "orchestrator_share_percent": None, "rules_weight": unknown})
    check_in("K-B2: the retro says the rules' cost is not known, and why", "The rules' cost is not known", text)
    check_in("K-B2: ... with the 'unknown' word and the reason", "unknown: role-load.json or the role files could not be read", text)
    # every role unmeasured: said, not dropped
    RL.static_load = lambda role, *a, **kw: dict(real(role, *a, **kw), layers=[dict(l, bytes=None) for l in real(role, *a, **kw)["layers"]])
    try:
        allgone = RN.rules_weight(rows, "claude-sonnet-4-5")
    finally:
        RL.static_load = real
    check_eq("K-B2: every role unmeasured is an unknown naming them all", (bool(allgone.get("unknown")), allgone.get("unmeasured_roles")),
             (True, ["qa-runner", "qa-scout"]))


def the_retro_prints_the_knowledge_table_beside_the_question_count() -> None:
    """t-2277 FL-8 F1: `retro_numbers.render` shows the question count with its counter-metrics and the table "reached / used / not used"
    (`report_facts`' words, one reader); a story with no such facts renders none of it; an unreadable count is `unmeasured`, never 0."""
    root, base, troot = project()
    try:
        older = RN.numbers("QA-1", base, troot)
        check_eq("F1 CONTROL: a story with no first look and no registry has no knowledge block", "knowledge" in older, False)
        check_not_in("F1 CONTROL: ... and the render prints no such line", "Questions put to the person", RN.render(older))
        (base / "records").mkdir()
        (base / "records" / "project-knowledge.json").write_text(json.dumps({"schema_version": 1, "facts": [
            {"id": "PK-1", "key": "product.roles", "environment": "", "element": "auditor", "state": "known", "scope": "project",
             "value": {"sign_in": "account"}, "provenance": {"source": "person", "words": "w", "story": "T-0", "by": "conductor", "where": ""},
             "at": "2026-11-01T10:00:00+00:00"}]}), encoding="utf-8")
        (troot / "pipeline.json").write_text(json.dumps({"ticket": "QA-1", "size": "M", "stages": {}, "created_at": "2026-11-05T09:00:00+00:00"}),
                                             encoding="utf-8")
        data = RN.numbers("QA-1", base, troot)
        check_in("F1: a story that knew a fact before it began carries the knowledge block", "knowledge_use", data["knowledge"]["facts"])
        text = RN.render(data)
        check_in("F1: the render prints the question count (no register: unmeasured, not 0) with its counter-metrics",
                 "**Questions put to the person: unmeasured: the story has no question register", text)
        check_in("F1: ... and the table of what the story knew, a line per fact", "- registry product.roles auditor: unmeasured: briefs are not kept; unmeasured: ", text)
        (troot / "work" / "requirements-readiness.json").write_text(json.dumps({"open_questions": []}), encoding="utf-8")
        zero = RN.render(RN.numbers("QA-1", base, troot))
        check_in("F1: a register read with no question: ZERO is printed only WITH the counter-metrics",
                 "**Questions put to the person: 0; known facts no brief carried: unmeasured: briefs are not kept", zero)
        check_eq("F1: facts of an older shape (no key) render nothing", RN.knowledge_lines(None), [])
        check_in("F1: a block that could not be built is one `unmeasured` line", "unmeasured: boom", "\n".join(RN.knowledge_lines({"problem": "boom"})))
    finally:
        cleanup(root)


# ----------------------------------------------------------------------------- run_counters (P1-v N4)

from datetime import datetime, timedelta, timezone  # noqa: E402

T0 = datetime(2026, 11, 13, 10, 0, 0, tzinfo=timezone.utc)
MONEY_WORDS = ("usd", "cost", "price", "money", "priced")


def at(seconds) -> str:
    return (T0 + timedelta(seconds=seconds)).isoformat()


def role_row(end_s, wall_s, dispatch="S1-x-1", session="s1", **extra) -> dict:
    ms = None if wall_s is None else int(wall_s * 1000)
    base = {"ts": at(end_s), "kind": "role", "role": "x", "dispatch": dispatch, "stage": "S1", "session_id": session, "num_turns": 3,
            "total_cost_usd": 0.4, "duration_ms": ms, "wall_ms": ms, "resumed": False, "exit_code": 0, "is_error": False,
            "infra": None, "retry": 0}
    base.update(extra)
    return base


def conductor_row(end_s, wall_s, session="c1") -> dict:
    return {"ts": at(end_s), "kind": "conductor", "role": "", "dispatch": "", "stage": "S1", "session_id": session, "num_turns": 1,
            "total_cost_usd": 0.1, "duration_ms": int(wall_s * 1000), "wall_ms": int(wall_s * 1000), "resumed": False,
            "exit_code": 0, "is_error": False, "infra": None, "retry": 0}


def p_start(s, **extra) -> dict:
    return {"ts": at(s), "kind": "process", "event": "start", "since": at(s), "package": "p1", "config_sha": "c1",
            "answer_file": False, "run_class": "live", **extra}


def p_end(since_s, end_s, **extra) -> dict:
    return {"ts": at(end_s), "kind": "process", "event": "end", "since": at(since_s), "process_code": 0, "question_kind": None,
            "package": "p1", "config_sha": "c1", "answer_file": False, "run_class": "live", "start_row_written": True, **extra}


def write_state(troot: Path, name: str, rows: list, raw: str = "") -> None:
    (troot / "state" / name).write_text("".join(json.dumps(r) + "\n" for r in rows) + raw, encoding="utf-8")


def counted(troot: Path, friction_result=None) -> dict:
    """`run_counters.counters` with `friction.story_friction` stubbed (no transcript hunt in the user's home)."""
    real = FR.story_friction
    FR.story_friction = lambda *a, **k: friction_result or {"status": "unknown", "reason": "stubbed: no transcripts"}
    try:
        return RC.counters(troot)
    finally:
        FR.story_friction = real


def tree_digest(troot: Path) -> list:
    return sorted((str(p.relative_to(troot)), p.read_bytes()) for p in troot.rglob("*") if p.is_file())


def every_key(value) -> list:
    if isinstance(value, dict):
        return [str(k) for k in value] + [k for v in value.values() for k in every_key(v)]
    if isinstance(value, (list, tuple)):
        return [k for v in value for k in every_key(v)]
    return []


def run_counters_time_rows() -> None:
    root, base, troot = project()
    write_state(troot, "driver-runs.jsonl", [role_row(100, 100, session="a"), role_row(160, 100, dispatch="S1-x-2", session="b"),
                                             conductor_row(180, 30), role_row(300, None, dispatch="S2-x-1", session="c")])
    d = counted(troot)
    check_eq("T2 union of overlapping role calls counts the overlap once", d["T2"]["union_s"], 160.0)
    check_eq("T2 per-session sum counts every session's own time", d["T2"]["sum_s"], 200.0)
    check_eq("T2 a call with no wall is counted as unknown, never 0 s", d["T2"]["calls_wall_unknown"], 1)
    check_eq("T3 conductor time not overlapped by a role (30 s call, 10 s inside the role union)", d["T3"]["not_overlapped_s"], 20.0)
    check_eq("T3 the conductor's own union is kept beside it", d["T3"]["union_s"], 30.0)
    check_eq("T1 with no process rows: the fallback is named, the end is not recorded",
             (d["T1"]["state"], d["T1"]["basis"].startswith("fallback"), d["T1"]["end_recorded"]), ("measured", True, False))
    # T8 AT and BEYOND the one threshold
    write_state(troot, "driver-runs.jsonl", [role_row(500, 130, duration_ms=10000, wall_ms=130000, session="a"),
                                             role_row(900, 130, dispatch="S1-x-2", session="b", duration_ms=9999, wall_ms=130000),
                                             role_row(1000, 5, dispatch="S1-x-3", session="c", duration_ms=None)])
    t8 = counted(troot)["T8"]
    check_eq("T8 wall - duration exactly 120000 ms is not hung; 120001 is (AT and BEYOND)", t8["n"], 1)
    check_eq("T8 the excess seconds are the wall minus the CLI's own count", t8["excess_s"], 120.0)
    check_eq("T8 a call with no duration is unmeasurable, not hung and not fine", t8["unmeasurable"], 1)
    check_eq("T8 the threshold is the one in driver_timing", t8["threshold_ms"], DT.WALL_NOTE_OVER_MS)
    # no journal: every journal row unknown, no crash
    root2, base2, troot2 = project()
    d2 = counted(troot2)
    check_eq("no journal: T1 T2 T3 T6 T7 T8 F1 G1 G2 are all unknown",
             sorted(k for k in ("T1", "T2", "T3", "T6", "T7", "T8", "F1", "G1", "G2") if d2[k]["state"] == "unknown"),
             sorted(("T1", "T2", "T3", "T6", "T7", "T8", "F1", "G1", "G2")))
    check_eq("no journal: no question and no answer record, no process row -> Q1 Q2 Q3 unknown (7.2: a missing file is never 0)",
             [d2[k]["state"] for k in ("Q1", "Q2", "Q3")], ["unknown"] * 3)
    # T4 / T5 only through driver_timing.report
    check_eq("T4 no timings recorded is unknown", d2["T4"]["state"], "unknown")
    (troot / "state" / "driver-timings.jsonl").write_text(
        json.dumps({"ts": at(100), "stage": "S1", "dispatch": "S1-x-1", "step": "handoff", "seconds": 4.0}) + "\n", encoding="utf-8")
    d3 = counted(troot)
    check_eq("T4 the step totals ARE driver_timing.report's", d3["T4"]["step_totals"], DT.report(troot)["step_totals"])
    cleanup(root)
    cleanup(root2)


def run_counters_windows_and_gaps() -> None:
    # (a) 7.1 run died mid-stage
    root, base, troot = project()
    launched = {"ts": at(290), "kind": "launched", "call": "role", "role": "x", "dispatch_id": "S2-x-1", "stage": "S2",
                "started_at": at(290), "model": "m", "retry": 0}
    write_state(troot, "driver-runs.jsonl", [p_start(0), role_row(100, 100), launched])
    d = counted(troot)
    check_eq("7.1 died: T1 is measured to the last record, end not recorded",
             (d["T1"]["wall_s"], d["T1"]["end_recorded"], d["T1"]["end_note"]), (290.0, False, "end not recorded"))
    check_eq("7.1 died: the open call is `cut` with its known start and an unknown wall",
             [(c["call"], c["started_at"], c["wall_s"]) for c in d["T1"]["cut_calls"]], [("S2-x-1", at(290), None)])
    check_eq("7.1 died: the open call adds no invented seconds to T2", d["T2"]["union_s"], 100.0)
    check_eq("7.1 died: a process with no end row is counted as such", d["run"]["processes_without_end"], 1)
    # (b) 7.3 restarts: a table of (previous end row kwargs, next start kwargs, previous has end row) -> class
    cases = {
        "a question then an answer file": (dict(question_kind="halt"), dict(answer_file=True), True, "person"),
        "a question then no answer file": (dict(question_kind="halt"), dict(answer_file=False), True, "operator"),
        "a question, answer file not recorded": (dict(question_kind="halt"), dict(answer_file=None), True, "not_recorded"),
        "no question posted": (dict(), dict(), True, "operator"),
        "package changed (question and answer file present)": (dict(question_kind="halt"), dict(answer_file=True, package="p2"), True, "operator"),
        "config changed": (dict(), dict(config_sha="c2"), True, "operator"),
        "package unknown on one side is not a change": (dict(question_kind="halt", package=None), dict(answer_file=True), True, "person"),
        "the earlier process left no end row": (dict(), dict(), False, "not_recorded"),
    }
    for name, (end_kw, start_kw, has_end, expected) in cases.items():
        root, base, troot = project()
        rows = [p_start(0), role_row(50, 50, session="shared")]
        rows += [p_end(0, 60, **end_kw)] if has_end else []
        rows += [p_start(160, **{k: v for k, v in start_kw.items()}), role_row(200, 40, dispatch="S1-x-2", session="shared"), p_end(160, 210, **start_kw)]
        write_state(troot, "driver-runs.jsonl", rows)
        d = counted(troot)
        bucket = {"person": d["T6"].get("n"), "operator": d["T7"].get("n"), "not_recorded": d["T7"].get("not_recorded", {}).get("n")}
        check_eq(f"T6/T7 gap class: {name} -> {expected}, in exactly one row", {k: v for k, v in bucket.items() if v}, {expected: 1})
        if expected == "person":
            check_eq("T6 the gap is last end -> next start (100 s), not model time", d["T6"]["seconds"], 100.0)
        if has_end:
            check_eq(f"7.3 {name}: a session reused across windows is one session, its time counted once",
                     (list(d["T2"]["per_session_s"]), d["T2"]["sum_s"]), (["shared"], 90.0))
    # (c) an open question at the end of the run
    root, base, troot = project()
    write_state(troot, "driver-runs.jsonl", [p_start(0), role_row(50, 50), p_end(0, 60, question_kind="exit_limit")])
    d = counted(troot)
    check_eq("T6 a question still open at the end is named, no seconds invented", (d["T6"]["n"], d["T6"]["open_question_kind"]), (0, "exit_limit"))
    # (d) a fresh single-process run: NO start row, the END row is the row it works from
    root, base, troot = project()
    write_state(troot, "driver-runs.jsonl", [role_row(50, 50), p_end(0, 60, run_class="dry")])
    d = counted(troot)
    check_eq("an end row alone: the window starts at `since`, the run class is read from the end row",
             (d["T1"]["basis"], d["T1"]["first"], d["T1"]["wall_s"], d["T1"]["end_recorded"], d["run"]["run_class"]),
             ("process rows", at(0), 60.0, True, "dry"))
    cleanup(root)


def run_counters_run_class() -> None:
    sessions = {"s": "plain-session", "stub": "stub-S1-x-1-1"}
    cases = [
        ("live in start and end", [p_start(0), p_end(0, 9)], "s", "live"),
        ("dry in start and end", [p_start(0, run_class="dry"), p_end(0, 9, run_class="dry")], "s", "dry"),
        ("smoke in the end row only", [p_end(0, 9, run_class="smoke")], "s", "smoke"),
        ("unknown stays unknown", [p_start(0, run_class="unknown"), p_end(0, 9, run_class="unknown")], "s", "unknown"),
        ("mixed: start live, end dry (one process)", [p_start(0), p_end(0, 9, run_class="dry")], "s", "mixed"),
        ("mixed: two windows, dry then smoke", [p_start(0, run_class="dry"), p_end(0, 9, run_class="dry"), p_start(20, run_class="smoke"),
                                                p_end(20, 30, run_class="smoke")], "s", "mixed"),
        ("no process row: never live by default", [], "s", "unknown"),
        ("live run with stub sessions: the safety net", [p_start(0), p_end(0, 9)], "stub", "unknown"),
        ("dry run with stub sessions is dry", [p_start(0, run_class="dry"), p_end(0, 9, run_class="dry")], "stub", "dry"),
        ("a non-string class is not a class", [p_start(0, run_class=7), p_end(0, 9, run_class=None)], "s", "unknown"),
    ]
    for name, process_rows, sid, expected in cases:
        root, base, troot = project()
        write_state(troot, "driver-runs.jsonl", process_rows + [role_row(5, 5, session=sessions[sid])])
        d = counted(troot)
        check_eq(f"run_class: {name} -> {expected}", d["run"]["run_class"], expected)
        if name.startswith("live run with stub"):
            check_in("run_class: the stub safety net says so in U1", "stub sessions in a run marked live", d["U1"]["lines"])
            check_eq("run_class: the stub sessions are counted", d["U1"]["stub_sessions"], 1)
        if expected == "dry":
            check_eq("dry run: T9 T10 R1r are n/a (stub roles), decided by the class not the prefix",
                     [d[k]["state"] for k in ("T9", "T10", "R1r")], ["n/a"] * 3)
        if expected == "live":
            check_eq("live run: T9 and T10 are unknown here (node N4b), R1r is read", [d[k]["state"] for k in ("T9", "T10")], ["unknown"] * 2)
        cleanup(root)


def run_counters_resumes_and_checks() -> None:
    root, base, troot = project()
    ids = ["s5_precheck:manifest", "handoff_check:header.verdict"]
    rows = [role_row(10, 10, session="a"),
            role_row(30, 20, session="a", resumed=True, resume_kind="handoff_findings", checks=ids, checks_n={ids[0]: 3, ids[1]: 1}),
            role_row(60, 30, dispatch="S1-x-2", session="b", resumed=True, resume_kind="paid_round", checks=["unknown"], checks_n={"unknown": 1}),
            role_row(70, 10, dispatch="S1-x-3", session="c", resumed=True, resume_kind="person_answer"),
            role_row(80, 10, dispatch="S1-x-4", session="d", resumed=True, resume_kind="made_up_token", checks="a string"),
            role_row(90, 10, dispatch="S1-x-5", session="e", resumed=True, resume_kind="unclassified", checks=[])]
    write_state(troot, "driver-runs.jsonl", rows)
    d = counted(troot)
    f1, g1 = d["F1"], d["G1"]
    check_eq("F1 first pass and resumed calls are split, their seconds are role wall", (f1["first_pass"]["calls"], f1["first_pass"]["role_s"], f1["resumed"]["calls"], f1["resumed"]["role_s"]), (1, 10.0, 5, 80.0))
    check_eq("F1 resumed calls by token as written; a token outside the table is `unclassified`",
             {k: v["calls"] for k, v in f1["resumed"]["by_kind"].items()}, {"handoff_findings": 1, "paid_round": 1, "person_answer": 1, "unclassified": 2})
    check_eq("7.12 a call naming two checks counts one return for EACH", (g1["by_check"][ids[0]]["returns"], g1["by_check"][ids[1]]["returns"]), (1, 1))
    check_eq("7.12 its role seconds go in full to each check, labelled shared", (g1["by_check"][ids[0]]["role_s_shared"], g1["by_check"][ids[1]]["role_s_shared"]), (20.0, 20.0))
    check_eq("7.12 the de-duplicated total of resumed seconds is printed once (20+30+10+10)", g1["resumed_s_total"], 70.0)
    check_in("7.12 the shared label is on the row", "do not sum", g1["shared_note"])
    check_eq("7.12 a refusal with no id, a broken list and an empty list are each ONE `unknown` return, never dropped",
             g1["by_check"]["unknown"]["returns"], 3)
    check_eq("G1 findings per check come from checks_n", g1["by_check"][ids[0]]["findings"], 3)
    check_eq("G1 a resume with no checks key (the person's answer) is not an unknown refusal", g1["resumed_without_checks"], 1)
    check_eq("U1 the unknown check share is printed", (g1["unknown_check"]["returns"], g1["unknown_check"]["of"], g1["unknown_check"]["malformed_rows"]), (3, 5, 2))
    check_eq("U1 unclassified resume kinds are counted", d["U1"]["unclassified_resume_kinds"], 2)
    # QUEUE-1: a retried caller resume writes two rows; one resume plus one retry
    rows = [role_row(10, 10, resumed=True, resume_kind="handoff_findings", checks=ids, infra="transient"),
            role_row(30, 10, resumed=True, resume_kind="handoff_findings", checks=ids, retry=1)]
    write_state(troot, "driver-runs.jsonl", rows)
    d = counted(troot)
    check_eq("a retried caller resume counts ONE resume and one retry, one return per check",
             (d["F1"]["resumed"]["calls"], d["F1"]["retries"], d["G1"]["by_check"][ids[0]]["returns"]), (1, 1, 1))
    # the transient in-call retry writes `unclassified` after a caller's resume: counted by token as written, as a resume
    rows = [role_row(10, 10, resumed=True, resume_kind="handoff_findings", checks=ids),
            role_row(30, 10, resumed=True, resume_kind="unclassified", retry=1)]
    write_state(troot, "driver-runs.jsonl", rows)
    d = counted(troot)
    check_eq("a retry row with a different token is its own resume (no special case)",
             {k: v["calls"] for k, v in d["F1"]["resumed"]["by_kind"].items()}, {"handoff_findings": 1, "unclassified": 1})
    # 7.6 / 7.11 old rows: no resume_kind, no checks
    rows = [role_row(10, 10), role_row(30, 10, resumed=True, resume_reason="free text that no code reads")]
    write_state(troot, "driver-runs.jsonl", rows, raw="not json\n[1]\n")
    d = counted(troot)
    check_eq("7.6 old resumed rows: kind not recorded (never parsed from the text), G1 unknown", (d["F1"]["resumed"]["kind_not_recorded"], d["F1"]["resumed"]["by_kind"], d["G1"]["state"]), (1, {}, "unknown"))
    check_eq("7.6 broken lines are counted in U1", d["U1"]["bad_lines"]["driver_runs"], 2)
    check_eq("7.6 an old run: no process rows, T6 and T7 unknown", (d["T6"]["state"], d["T7"]["state"], d["B1"]["state"]), ("unknown",) * 3)
    # the table cannot be read: every kind is `unclassified`, with its note in U1
    rows = [role_row(10, 10, resumed=True, resume_kind="handoff_findings", checks=ids)]
    write_state(troot, "driver-runs.jsonl", rows)
    real = DJ.run_record
    DJ.run_record = lambda path=None: ({}, "note: the run record could not be read (stub)")
    try:
        d = counted(troot)
    finally:
        DJ.run_record = real
    check_eq("7.11 an unreadable table: the token counts under `unclassified`, the note reaches U1",
             (list(d["F1"]["resumed"]["by_kind"]), d["U1"]["lines"][0].startswith("note: the run record")), (["unclassified"], True))
    cleanup(root)


def run_counters_questions_briefs_and_quality() -> None:
    root, base, troot = project()
    write_state(troot, "driver-runs.jsonl", [p_start(0), p_end(0, 9)])
    d = counted(troot)
    check_eq("7.2 the process rows prove the driver ran: no questions is 0 (measured)", (d["Q1"]["state"], d["Q1"]["n"], d["Q3"]["state"], d["Q3"]["n"]), ("measured", 0, "measured", 0))
    write_state(troot, "driver-runs.jsonl", [role_row(5, 5)])
    check_eq("7.2 no process rows and no question file: unknown", counted(troot)["Q1"]["state"], "unknown")
    write_state(troot, "driver-questions.jsonl", [])
    check_eq("7.2 an empty question file is 0, measured", (counted(troot)["Q1"]["state"], counted(troot)["Q1"]["n"]), ("measured", 0))
    write_state(troot, "driver-questions.jsonl", [{"ts": at(1), "kind": "halt", "stage": "S0"}, {"ts": at(2), "kind": "halt", "stage": "S5"}, {"ts": at(3), "stage": "S5"}])
    q1 = counted(troot)["Q1"]
    check_eq("Q1 by kind and stage; a row with no kind is counted under `unknown`, never dropped", (q1["by_kind"], q1["by_stage"]), ({"halt": 2, "unknown": 1}, {"S0": 1, "S5": 2}))
    # Q3 repeats
    answers = [{"ts": at(1), "kind": "halt", "question_sha": "aa"}, {"ts": at(2), "kind": "halt", "question_sha": "aa"},
               {"ts": at(3), "kind": "refusal", "question_sha": "bb"}, {"ts": at(4), "kind": "conductor", "question_sha": "bb"},
               {"ts": at(5), "kind": "halt", "question_sha": "aa"}, {"ts": at(6), "kind": "halt"}, {"ts": at(7), "kind": "halt", "question_sha": 5}]
    write_state(troot, "driver-answers.jsonl", answers[:1])
    check_eq("Q3 one answer is no repeat", counted(troot)["Q3"]["n"], 0)
    write_state(troot, "driver-answers.jsonl", answers[:2])
    check_eq("Q3 AT: two answers with the same sha -> 1 repeat, under their kind", (counted(troot)["Q3"]["n"], counted(troot)["Q3"]["by_kind"]), (1, {"halt": 1}))
    write_state(troot, "driver-answers.jsonl", answers[2:4])
    check_eq("Q3 a different kind with the same sha is counted under the LATER row's kind", counted(troot)["Q3"]["by_kind"], {"conductor": 1})
    write_state(troot, "driver-answers.jsonl", answers)
    q3 = counted(troot)["Q3"]
    check_eq("Q3 a third answer with the same sha is a second repeat; rows with no usable sha are counted aside, never as repeats",
             (q3["by_kind"], q3["answers_without_sha"]), ({"conductor": 1, "halt": 2}, 2))
    # gates passed by the person's word, gate repairs
    write_state(troot, "passed-by-person.jsonl", [{"ts": at(1), "block": "x"}, {"ts": at(2), "block": "y"}])
    check_eq("Q2 counts the rows of the carrier", counted(troot)["Q2"]["n"], 2)
    write_state(troot, "driver-runs.jsonl", [{"ts": at(1), "kind": "gate_repair", "gate": "A", "moves": ["x", "y"]}, {"ts": at(2), "kind": "gate_repair", "gate": "A", "moves": 3}, {"ts": at(3)}, {"ts": "2026-11-13T10:00:04"}])
    d = counted(troot)
    check_eq("G2 gate repairs by gate with their moves", (d["G2"]["n"], d["G2"]["by_gate"], d["G2"]["moves"]), (2, {"A": 2}, 5))
    check_eq("U1 a row with no kind and a time with no offset are counted", (d["U1"]["rows_without_kind"], d["U1"]["naive_timestamps"]), (2, 1))
    # B1 at and beyond the ceiling
    write_state(troot, "brief-sizes.jsonl", [{"role": "a", "budget_bytes": 6144, "ceiling": 6144}, {"role": "a", "budget_bytes": 6145, "ceiling": 6144},
                                             {"role": "b", "budget_bytes": 100, "ceiling": 6144}, {"role": "b", "budget_bytes": 7}, {"role": "b", "budget_bytes": True, "ceiling": 1}])
    b1 = counted(troot)["B1"]
    check_eq("B1 AT the ceiling is not over, BEYOND (6145) is", (b1["by_role"]["a"]["n"], b1["by_role"]["a"]["over"]), (2, 1))
    check_eq("B1 mean and max of the budget bytes per role", (b1["by_role"]["a"]["mean_budget_bytes"], b1["by_role"]["a"]["max_budget_bytes"]), (6144.5, 6145))
    check_eq("B1 rows with no ceiling or a bool size are counted aside", b1["unreadable_rows"], 2)
    check_eq("B1 no record: unknown", counted(project()[2])["B1"]["state"], "unknown")
    # a dry run: counts stay, nothing is written
    write_state(troot, "driver-runs.jsonl", [p_start(0, run_class="dry"), role_row(5, 5, session="stub-S1-x-1-1", resumed=True, resume_kind="refusal_resume", checks=["exit_gate:scoped"]), p_end(0, 9, run_class="dry")])
    before = tree_digest(troot)
    d = counted(troot)
    check_eq("7.9 a dry run: the counts stay (returns per check, questions, briefs)", (d["G1"]["by_check"]["exit_gate:scoped"]["returns"], d["Q1"]["state"], d["B1"]["state"]), (1, "measured", "measured"))
    check_eq("7.9 `counters` writes nothing (the whole state tree is byte-identical)", tree_digest(troot), before)
    cleanup(root)


def run_counters_friction_and_money() -> None:
    root, base, troot = project()
    money_row = {"dispatches": 2, "sessions": 2, "sessions_unreachable": 0, "turns": 40, "fric_turns": 10, "priced_turns": 40, "priced_cost": 1.5,
                 "fric_cost": 0.5, "unpriced": 0, "kinds": {"guard": 6, "usage": 4}, "helpers": [{"path": "C:/stand/x.py", "call": "x"}],
                 "turn_share": 25.0, "money_share": 33.3, "reachable": 2}
    stub = {"status": "ok", "reason": "", "sessions": 2, "sessions_unreachable": 0, "unpriced": 0, "method": "m", "sources": {"cost file": 2},
            "roles": {"qa-automator": money_row, "qa-case-critic": dict(money_row, turns=10, fric_turns=1, turn_share=10.0)},
            "total": {"turns": 50, "fric_turns": 11, "priced_turns": 50, "priced_cost": 1.9, "fric_cost": 0.6, "unpriced": 0, "turn_share": 22.0, "money_share": 31.0}}
    # the cumulative total_cost_usd of a resumed session rises (0.424 -> 0.455): no money key anywhere in the dict
    write_state(troot, "driver-runs.jsonl", [role_row(10, 10, total_cost_usd=0.424), role_row(30, 10, resumed=True, total_cost_usd=0.455, resume_kind="person_answer")])
    d = counted(troot, stub)
    r1r = d["R1r"]
    check_eq("R1r keeps turns, shares, kinds and counts only: no key of the money vocabulary in the row",
             [k for k in every_key(r1r) if any(w in k.lower() for w in MONEY_WORDS)], [])
    check_eq("R1r drops the helpers' paths and keeps their count (AR-4)", ("helpers" in every_key(r1r), r1r["roles"]["qa-automator"]["helpers_n"]), (False, 1))
    check_eq("R1r turn_share equals story_friction's per role", {k: v["turn_share"] for k, v in r1r["roles"].items()}, {k: v["turn_share"] for k, v in stub["roles"].items()})
    check_eq("R1r turn_share equals story_friction's total", r1r["total"]["turn_share"], stub["total"]["turn_share"])
    check_eq("R1r the other counts are story_friction's", (r1r["roles"]["qa-automator"]["turns"], r1r["roles"]["qa-automator"]["kinds"], r1r["total"]["fric_turns"]), (40, {"guard": 6, "usage": 4}, 11))
    check_eq("the whole dict carries no key of the money vocabulary (a rising total_cost_usd and a money-rich friction result in)",
             [k for k in every_key(d) if any(w in k.lower() for w in MONEY_WORDS)], [])
    # the real story_friction on a journal whose transcripts are absent: unknown with its reason, not 0 %
    real = FR.story_friction
    FR.story_friction = lambda *a, **k: (_ for _ in ()).throw(RuntimeError("boom"))
    try:
        broken = RC.counters(troot)["R1r"]
    finally:
        FR.story_friction = real
    check_eq("R1r a failure of the friction reader is unknown with its text, never a crash", (broken["state"], "boom" in broken["why"]), ("unknown", True))
    check_eq("R1r no transcript reachable is unknown, not 0 %", counted(troot)["R1r"]["state"], "unknown")
    cleanup(root)


def run_counters_one_road_and_cli() -> None:
    text = (SCRIPTS / "run_counters.py").read_text(encoding="utf-8")
    for needle in ("json.loads(", "open(", ".read_text(", "splitlines("):
        check_not_in(f"AR-13 run_counters parses no carrier of its own: no `{needle}`", needle, text)
    check_in("AR-13 positive control: the same needle shape finds `json.loads(` in the one reader", "json.loads(", (SCRIPTS / "driver_journal.py").read_text(encoding="utf-8"))
    for survivor in ("DJ.read_rows_counted(", "DJ.question_rows", "DJ.answer_rows", "DJ.parse_ts(", "DJ.run_record()", "driver_timing.report(",
                     "friction.story_friction(", "retro_numbers.dispatch_rounds(", "driver_timing.WALL_NOTE_OVER_MS"):
        check_in(f"AR-15 the survivor is called, not copied: {survivor}", survivor, text)
    # the counted readers
    root, base, troot = project()
    path = troot / "state" / "driver-runs.jsonl"
    path.write_bytes(b"\xef\xbb\xbf" + json.dumps({"a": 1}).encode() + b"\nnot json\n[1]\n\n" + json.dumps({"b": 2}).encode() + b"\n")
    check_eq("read_rows_counted: rows, and the lines left out (a broken line, a non-object)", DJ.read_rows_counted(path), ([{"a": 1}, {"b": 2}], 2))
    check_eq("read_rows is the same loop without the count", DJ.read_rows(path), [{"a": 1}, {"b": 2}])
    check_eq("an absent file is ([], 0) for the counted reader", DJ.read_rows_counted(troot / "state" / "nope.jsonl"), ([], 0))
    write_state(troot, "driver-questions.jsonl", [{"kind": "k"}], raw="bad\n")
    write_state(troot, "driver-answers.jsonl", [{"kind": "k"}, {"kind": "j"}])
    check_eq("question_rows / answer_rows read their carriers with the count", (DJ.question_rows(troot), DJ.answer_rows(troot)), (([{"kind": "k"}], 1), ([{"kind": "k"}, {"kind": "j"}], 0)))
    # the CLI prints the same dict as `counters`
    import subprocess
    write_state(troot, "driver-runs.jsonl", [p_start(0), role_row(5, 5), p_end(0, 9)])
    done = subprocess.run([sys.executable, "-B", str(SCRIPTS / "run_counters.py"), "--task-root", str(troot), "--json"],
                          capture_output=True, text=True, encoding="utf-8")
    check_eq("CLI --task-root --json: exit 0, one JSON object, the run class and T2 as `counters` reads them",
             (done.returncode, json.loads(done.stdout)["run"]["run_class"], json.loads(done.stdout)["T2"]["union_s"]), (0, "live", 5.0))
    check_eq("CLI writes nothing to the state folder", sorted(p.name for p in (troot / "state").iterdir()),
             sorted(["driver-runs", "driver-runs.jsonl", "driver-questions.jsonl", "driver-answers.jsonl"]))
    cleanup(root)


def main() -> None:
    run_counters_time_rows()
    run_counters_windows_and_gaps()
    run_counters_run_class()
    run_counters_resumes_and_checks()
    run_counters_questions_briefs_and_quality()
    run_counters_friction_and_money()
    run_counters_one_road_and_cli()
    the_retro_prints_the_knowledge_table_beside_the_question_count()
    the_resumes_add_up_per_stage()
    the_unknown_and_the_empty_are_not_the_same()
    the_class_of_a_gate_block_has_one_reader()
    the_gate_block_line_is_measured_not_assumed()
    a_missing_journal_prints_unknown_beside_no_zero()
    the_rules_cost_is_never_silently_smaller_than_the_whole()
    finish("test_retro_numbers")


if __name__ == "__main__":
    main()
