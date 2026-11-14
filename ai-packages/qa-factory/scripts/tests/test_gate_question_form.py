"""A gate-A question carries its readings, or the factory rewrites it before the gate is shown.

TP1-15045 asked the owner, once, `Where must a removed node appear when the YAML has no
layout meta (code falls back to {0,0})?` — no quote of the source, no readings, no consequence.
Nobody answered it. The factory then tested the letter of AC-4 ("shown at its former position")
with a 1 px coordinate check, while the implementing developer's comment on the parent ticket
said the diff re-lays the nodes out and the coordinates mean nothing; the contradiction matrix
had scored that requirement against the parent story as `silent`. The result was a bug that was
not a bug. Put as "the source says X; reading a, from the AC; reading b, from the developer's
comment; what changes with each", the same question was answered in one minute.

So: a question built from the register's matrix carries both readings with their origins, the
brief prints it as a card and not as a clipped line, and a question nobody can answer as it
stands is a repair the FACTORY owes itself before the gate — passed, like every block in this
factory, by the person's own recorded word.
"""
import collections
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import check, check_eq, check_in, check_not_in, cleanup, finish, temp_dir, write_register, SCRIPTS  # noqa: E402

sys.path.insert(0, str(SCRIPTS))

import contract  # noqa: E402
import gate_brief  # noqa: E402
import gate_preflight  # noqa: E402
import human_text  # noqa: E402
import planning_contract  # noqa: E402
import question_register as QR  # noqa: E402
import question_stop as QS  # noqa: E402

EM_DASH = chr(0x2014)  # built, never typed: the package is ASCII-clean (FR-30)

# The 15045 register as S2 would write it once the matrix compares R-4 with the parent
# ticket's comments as well as with its AC.
REGISTER = """---
task: TP1-15045
---

## Register

| R | Requirement (one verifiable statement) | source | derived_from | verifiable | ac_ref | observable | impact |
|---|---|---|---|---|---|---|---|
| R-3 | A restored node keeps its identity | ac | - | yes | AC-3 | diff:Diff.tsx:80 | degraded |
| R-4 | A removed node is shown at its former position | ac | - | yes | AC-4 | diff:Diff.tsx:120 | cosmetic |

## Contradiction matrix

| R | parent story/feature | comments of the ticket and its parent | area open bugs |
|---|---|---|---|
| R-3 | ok:TP1-14482 | silent | silent |
| R-4 | silent | contradicts:"the position of elements displayed in the diff does not correspond to the position of the real restoration state" (TP1-14482 comment, 2026-09-09) | silent |
"""

PLAN = [{"id": "TS-4", "requirement_ids": ["R-4"], "level": "e2e-ui",
         "disposition": "automate", "oracle_unknown": True}]


def story(prefix: str, questions=None, pipeline_extra=None) -> Path:
    base = temp_dir(prefix) / "qa-factory"
    task_root = base / "artifacts" / "TP1-15045"
    (task_root / "work").mkdir(parents=True)
    (task_root / "state").mkdir(parents=True)
    (base / "config.json").write_text("{}", encoding="utf-8")
    write_register(task_root, REGISTER, head="")
    (task_root / "work" / "test-plan.json").write_text(json.dumps(PLAN), encoding="utf-8")
    (task_root / "work" / "requirements-readiness.json").write_text(
        json.dumps({"verdict": "ready", "open_questions": questions or []}), encoding="utf-8")
    (task_root / "pipeline.json").write_text(json.dumps(
        dict({"ticket": "TP1-15045"}, **(pipeline_extra or {}))), encoding="utf-8")
    return base


def test_readings_are_built_from_the_matrix() -> None:
    base = story("qa-question-readings-")
    task_root = base / "artifacts" / "TP1-15045"
    try:
        readings = planning_contract.register_contradiction_readings(REGISTER)
        check_in("the matrix row is read back", "R-4", readings)
        check_eq("and it names the column the requirement disagrees with",
                 readings["R-4"]["against"], "comments of the ticket and its parent")
        check_eq("which is where the second reading comes from",
                 readings["R-4"]["origin"], "comment")
        check_eq("the requirement's own text is the first reading",
                 readings["R-4"]["statement"],
                 "A removed node is shown at its former position")
        check_eq("and its AC is where that one comes from", readings["R-4"]["ac_ref"], "AC-4")
        check_not_in("a row the matrix does not contradict is not a question", "R-3", readings)

        questions = gate_brief.contradiction_questions(task_root, PLAN)
        check_eq("the contradicted plan row makes exactly one question", len(questions), 1)
        question = questions[0]
        check_eq("which a person can answer as it stands",
                 contract.question_errors(question), [])
        check_eq("it carries two readings, not one", len(question["readings"]), 2)
        check_eq("the first from the acceptance criterion",
                 question["readings"][0]["from"], "acceptance_criteria:AC-4")
        check_eq("the second from the developer's comment",
                 question["readings"][1]["from"], "comment")
        check("each reading says what follows from it",
              all("TS-4" in r["if_chosen"] for r in question["readings"]))
        check_in("and the coordinates reading is quoted, not paraphrased",
                 "does not correspond to the position",
                 json.dumps(question["source_says"]))

        text = gate_brief.render({"task": "TP1-15045", "open_questions": questions})
        check_in("the brief prints the quote", "the source says:", text)
        check_in("the readings are lettered for the answer", "- a) ", text)
        check_in("with the second beside it", "- b) ", text)
        check_in("and what each answer costs", "if chosen:", text)
        check_in("the person's own wording is offered without being a third reading",
                 "or your own wording", text)
        check_eq("and readings[] holds only what the sources say",
                 len(question["readings"]), 2)
        check("the question is no longer clipped to one line",
              len([line for line in text.splitlines() if line.startswith("  - ")]) >= 4)
    finally:
        cleanup(base.parent)


def test_a_bare_question_is_the_factorys_to_rewrite() -> None:
    """A story in flight, written by an older build: one finding, and a person's word passes it."""
    bare = [{"id": "Q-3", "severity": "major", "owner_role": "po_ba",
             "question": "Where must a removed node appear when the YAML has no layout meta?"}]
    base = story("qa-question-bare-", questions=bare)
    task_root = base / "artifacts" / "TP1-15045"
    try:
        rehearsal = gate_preflight.Rehearsal(task_root, "A")
        rehearsal.check_open_questions()
        check_eq("a bare question is exactly one finding", len(rehearsal.findings), 1)
        finding = rehearsal.findings[0]
        check_eq("owned by the factory, not by the person",
                 finding["class"], gate_preflight.FACTORY_FIXABLE)
        check_in("it names the question", "Q-3", finding["message"])
        check_in("and the role that rewrites it",
                 "qa-requirements-tester", finding["message"])
        check_in("the person's word passes it, as a line they write (t-357: no script named)",
                 f"write `{finding['id']}: accept` with your reason", finding["fix"])

        check_eq("the rehearsal writes nothing",
                 json.loads((task_root / "pipeline.json").read_text(encoding="utf-8")),
                 {"ticket": "TP1-15045"})
    finally:
        cleanup(base.parent)

    waived = {"stage_overrides": [{"stage": "S5", "match": "Q-3",
                                  "decision": "I know what I meant; go on",
                                  "at": "2026-09-24T09:00:00+00:00"}]}
    base = story("qa-question-waived-", questions=bare, pipeline_extra=waived)
    task_root = base / "artifacts" / "TP1-15045"
    try:
        rehearsal = gate_preflight.Rehearsal(task_root, "A")
        rehearsal.check_open_questions()
        check_eq("a waiver naming the question id silences it for good",
                 rehearsal.findings, [])
    finally:
        cleanup(base.parent)

    answered = [dict(bare[0], answer="the place in the structure")]
    base = story("qa-question-answered-", questions=answered)
    task_root = base / "artifacts" / "TP1-15045"
    try:
        rehearsal = gate_preflight.Rehearsal(task_root, "A")
        rehearsal.check_open_questions()
        check_eq("an answered question is not rewritten either", rehearsal.findings, [])
    finally:
        cleanup(base.parent)


def test_a_bare_question_still_reaches_the_person() -> None:
    """Backward compatibility: the brief shows a pre-0.7.16 question, it never drops it."""
    bare = {"question": "Where must a removed node appear?", "severity": "minor",
            "owner_role": "po_ba"}
    text = gate_brief.render({"task": "TP1-15045", "open_questions": [bare]})
    check_in("the old question is printed as it stands", "Where must a removed node appear?", text)
    check_not_in("with no invented reading beside it", "- a) ", text)


# --- t-155 (A2): what each answer changes, and the question's status from the register ----------
# B-216 / B-181. Stories here are shaped like TP1-13797 (cmp1): the project's FULL case id form
# `TP1-13797_TC_009`, manual rows a reading would take out of manual, and the person's
# answers kept in `authorization_source` of the gate record.

TICKET = "TP1-13797"
CASE_FORM = {"case_id_form": "{ticket}_TC_{nnn}"}
SHORT_TOKEN = re.compile(r"(?<![\w-])TC_[0-9]+: (?:manual|automate)")  # a short id in a token


def full_id(number: int) -> str:
    return f"{TICKET}_TC_{number:03d}"


def question(qid: str, count: int = 2, **extra) -> dict:
    row = {"id": qid, "question": f"What must happen for {qid}?", "severity": "major",
           "owner_role": "dev_arch",
           "readings": [{"reading": f"reading {i + 1} of {qid}", "from": "description",
                         "if_chosen": f"{qid} goes by reading {i + 1}"} for i in range(count)]}
    row.update(extra)
    return row


def plan_row(row_id: str, disposition: str = "manual-human", **extra) -> dict:
    row = {"id": row_id, "requirement_ids": ["R-21"], "level": "", "disposition": disposition}
    row.update(extra)
    return row


def case_text(number: int, plan_row_id: str, title: str, thens: list, question_thens=None,
              raw_question_thens=None) -> str:
    front = [f"id: {full_id(number)}", f"title: {title}", "area: webhook", "channel: manual-human",
             f"task: {TICKET}", f"plan_row: {plan_row_id}"]
    if raw_question_thens is not None:
        front.append("question_thens: " + raw_question_thens)
    elif question_thens is not None:
        front.append("question_thens: " + json.dumps(question_thens))
    body = [f"Requirements: R-{number}", f"Plan row: {plan_row_id}", "", "## Then"]
    body += [f"{n}. {text}" for n, text in enumerate(thens, start=1)]
    return "---\n" + "\n".join(front) + "\n---\n" + "\n".join(body) + "\n"


def gate_story(prefix: str, questions: list, rows=None, cases=None, pipeline=None,
               register: bool = True, with_register_md: bool = False) -> Path:
    base = temp_dir(prefix) / "qa-factory"
    task_root = base / "artifacts" / TICKET
    (task_root / "work" / "test-cases" / "webhook").mkdir(parents=True)
    (task_root / "state").mkdir(parents=True)
    (base / "config.json").write_text(json.dumps(CASE_FORM), encoding="utf-8")
    if register:
        (task_root / "work" / "requirements-readiness.json").write_text(
            json.dumps({"verdict": "ready", "open_questions": questions}), encoding="utf-8")
    if with_register_md:
        write_register(task_root, REGISTER, head="")
    (task_root / "work" / "test-plan.json").write_text(json.dumps(rows or []), encoding="utf-8")
    for number, text in (cases or {}).items():
        (task_root / "work" / "test-cases" / "webhook" / f"{full_id(number)}.md").write_text(
            text, encoding="utf-8")
    (task_root / "pipeline.json").write_text(
        json.dumps(dict({"ticket": TICKET}, **(pipeline or {}))), encoding="utf-8")
    return task_root


def drop(task_root: Path) -> None:
    cleanup(task_root.parents[2])


def packet(task_root: Path) -> str:
    return gate_brief.render(gate_brief.collect(TICKET, task_root))


def card_of(text: str, qid: str) -> str:
    """The lines of ONE question's card inside a rendered packet."""
    start = text.find(f"- **{qid}**")
    if start < 0:
        return ""  # a missing card is a FAIL line of the check that reads it, not a crash
    ends = [i for i in (text.find("\n- **", start + 1), text.find("\n## ", start + 1)) if i >= 0]
    return text[start:min(ends) if ends else len(text)]


def reading_of(card: str, letter: str) -> str:
    """The lines under ONE reading of a card (its sub-bullets included); "" when it has none."""
    parts = card.split(f"\n  - {letter}) ", 1)
    return parts[1].split("\n  - ", 1)[0] if len(parts) == 2 else ""


def question_part(text: str) -> str:
    """From the `Open questions` heading to the end of the `How to answer` block."""
    start = text.index("## Open questions")
    how = text.index("## How to answer", start)
    rest = text[how + 1:]
    stop = re.search(r"\n(?:## |_\(brief truncated)", rest)
    return text[start:how + 1 + stop.start()] if stop else text[start:]


def test_a_card_shows_what_each_answer_changes() -> None:
    """R8 items 1-3: the consequence under each reading, the token that keeps a case manual, and
    the answer grammar once, in the `how to answer` block."""
    questions = [question("Q1"), question("Q4")]
    rows = [plan_row("TS-9", what_we_verify="array filter on an object field",
                     if_answered={"Q4": {"*": {"disposition": "automate", "level": "api"}}}),
            plan_row("TS-6")]
    cases = {
        9: case_text(9, "TS-9", "Array-filter syntax on an object field",
                     ["The root-anchored filter saves and its delivery creates one execution.",
                      "The array filter on an object field: per the owner's decision."],
                     question_thens=[{"question": "Q4", "then": 2, "readings": {
                         "a": "The array filter on an object field saves and never matches: no execution.",
                         "b": "The array filter on an object field is rejected at save time: 422, nothing stored."}}]),
        6: case_text(6, "TS-6", "A disallowed event type is acknowledged", ["The delivery is acknowledged."],
                     question_thens=[{"question": "Q1", "then": 1, "readings": {
                         "a": "HTTP 200 and no execution.", "b": ""}}])}
    task_root = gate_story("qa-a2-card-", questions, rows, cases)
    try:
        data = gate_brief.collect(TICKET, task_root)
        text = gate_brief.render(data)
        q4 = card_of(text, "Q4")
        token = f"`{full_id(9)}: manual`"
        for letter, then_text in (("a", "saves and never matches: no execution."),
                                  ("b", "rejected at save time: 422, nothing stored.")):
            block = reading_of(q4, letter)
            check_in(f"R8-1 Q4 reading {letter}: the changed Then is printed with its case and number",
                     f"Then 2 of {full_id(9)} (Array-filter syntax on an object field) would read:", block)
            check_in(f"R8-1 Q4 reading {letter}: with THIS reading's text", then_text, block)
            check_in(f"R8-2 Q4 reading {letter}: the `*` patch reaches every reading - the case "
                     "leaves manual and the card says the factory does not switch it yet, how it is "
                     "checked is decided again from an automated test, and the report says what",
                     "The factory does not switch it by itself yet: after your answer, how it is checked "
                     "is decided again, starting from an automated test, and the report says what was "
                     "decided. To keep it checked by hand, write", block)
            check_in(f"R8-2 Q4 reading {letter}: the token that keeps it manual carries the FULL case id",
                     token, block)
        check_not_in("R8-1 the Then's own punctuation is not doubled", '.".', q4)
        check_in("R8-2 the token closes the block: what the case says comes first",
                 "would read:", q4.split("TP1-13797_TC_009 (Array-filter syntax on an object field) would no longer")[0])
        check_not_in("R8-2 conflict: the spec's 'would move to automate' is not what the card says",
                     "move to automate", text)
        check_not_in("R8-2 and it does not promise `automated by default` either (P19)", "by default", text)
        # the switch of a plan row after the answer is not built yet (owner, 01.10): no promise of it.
        # The positive control is the check above: the new words ARE in the card, so the absence is not a miscall.
        check_not_in("t-199 the old promise `decide anew` is absent from the rendered card", "decide anew", text)
        check_not_in("t-199 and so is its other form, `will decide`", "will decide", text)
        check("R8-2 no token of the packet carries a short case id",
              SHORT_TOKEN.search(text) is None, SHORT_TOKEN.search(text) and SHORT_TOKEN.search(text).group(0))
        q1 = card_of(text, "Q1")
        check_in("R8-1 an empty reading text is printed as nothing asserted, the Then keeps its number",
                 f"Then 1 of {full_id(6)} (A disallowed event type is acknowledged): "
                 "nothing is asserted here for this answer.", reading_of(q1, "b"))
        check_in("R8-1 Q1 reading a prints its own text", "HTTP 200 and no execution.", reading_of(q1, "a"))
        check_not_in("R8-2 a case no reading takes out of manual is offered no token",
                     f"{full_id(6)}: manual", text)
        check_in("R8-1 the structured effect carries the same fact (the applier's twin reads fields)",
                 "leaves_manual", json.dumps(data["question_effects"]["Q4"]["a"]))
        # item 3: the grammar, once, in its own block, and it is the strict one.
        check_eq("R8-3 the `how to answer` block appears once", text.count("## How to answer"), 1)
        check_eq("R8-3 and the letter form is stated once in the whole packet",
                 text.count("`<question id>: <letter>`"), 1)
        how = text[text.index("## How to answer"):]
        for form in ("`<question id>: <letter>`", "`<question id>: not needed`",
                     "`<full case id>: manual`", "`<full case id>: automate`",
                     "Write each answer on its own line",
                     gate_brief.ANYTHING_ELSE_SENTENCE):
            check_in(f"R8-3 the block says: {form}", form, how)
        check_not_in("R8-3 no other form is advertised: not the lenient `(a)`", "(a)", how)
        check("R8-3 the block comes after every card", text.index("## How to answer") > text.index("- **Q4**"))
        # the printed grammar is the one the register's parser reads (FR-10): feed it the tokens.
        words = f"Q4: a\nQ1: b\n{full_id(9)}: manual\n"
        parsed = QR.parse_choices(words, questions, [full_id(9), full_id(6)])
        check_eq("R8-3 what the card prints is what the parser reads: choices",
                 parsed["choices"], {"Q4": "a", "Q1": "b"})
        check_eq("R8-3 and the case token parses to the full id",
                 [(t["case"], t["decision"]) for t in parsed["case_tokens"]], [(full_id(9), "manual")])
        # FR-6: the text a person reads breaks no rule of human-questions.md.
        check_eq("R8 the question cards and the block obey human-questions.md",
                 [p["rule"] for p in human_text.problems(question_part(text))], [])
    finally:
        drop(task_root)


def test_the_star_patch_a_letter_override_and_not_needed() -> None:
    """R8 / Q12: `*` applies to every reading and a letter's own patch wins; `not needed` prints
    its consequence only when a patch exists for it; an answer that changes nothing says so."""
    rows = [plan_row("TS-7", if_answered={"Q2": {"*": {"disposition": "automate", "level": "api"},
                                                 "b": {"disposition": "manual-human"},
                                                 "not_needed": {"disposition": "automate"}}}),
            plan_row("TS-5", "automate", level="api", what_we_verify="the size limit on a payload",
                     if_answered={"Q2": {"*": {"disposition": "manual-agent"},
                                         "b": {"disposition": "automate"}}})]
    cases = {7: case_text(7, "TS-7", "Dispatched only for the listed event", ["One execution."]),
             5: case_text(5, "TS-5", "Payload size limit", ["The payload is refused."])}
    task_root = gate_story("qa-a2-star-", [question("Q2")], rows, cases)
    try:
        text = packet(task_root)
        card = card_of(text, "Q2")
        a, b = reading_of(card, "a"), reading_of(card, "b")
        check_in("R8 reading a: the case TS-7 leaves manual and the full token is offered",
                 f"`{full_id(7)}: manual`", a)
        check_in("R8 reading a: a row that stays checked but changes how is one plain line",
                 "the size limit on a payload: an automated test becomes a check by an agent, by hand "
                 f"(cases: {full_id(5)}).", a)
        check_in("R8 reading b: both letter patches restore what the row already was - it says nothing changes",
                 "nothing in the plan or the cases changes.", b)
        check_not_in("R8 reading b: and offers no token", f"{full_id(7)}: manual", b)
        check_eq("R8 `not needed` has its own block because a patch exists for it",
                 card.count("if you write `Q2: not needed`, what changes:"), 1)
        check_in("R8 and it offers the token for the case that would leave manual",
                 f"`{full_id(7)}: manual`", card.split("what changes:")[-1])
    finally:
        drop(task_root)
    # No patch for `not needed` anywhere: no such block.
    plain = gate_story("qa-a2-star2-", [question("Q2")],
                       [plan_row("TS-7", if_answered={"Q2": {"a": {"disposition": "automate"}}})],
                       {7: case_text(7, "TS-7", "Dispatched", ["One."])})
    try:
        check_not_in("R8 no `not needed` patch, no `not needed` block",
                     "what changes:", card_of(packet(plain), "Q2").split("- or your own wording")[-1])
    finally:
        drop(plain)


def test_a_story_from_before_the_fields_reads_as_it_did() -> None:
    """E-9: no `question_refs`, `if_answered` or `question_thens` anywhere: the card is today's card."""
    task_root = gate_story("qa-a2-legacy-", [question("Q1")], [plan_row("TS-9")],
                           {9: case_text(9, "TS-9", "Array filter", ["One."])})
    try:
        data = gate_brief.collect(TICKET, task_root)
        check_eq("E-9 nothing is computed for a story without the fields", data["question_effects"], {})
        check_eq("E-9 and nothing is unreadable", data["question_effect_problems"], [])
        expected = ["- **Q1** [major, owner dev_arch] What must happen for Q1?",
                    "  - a) reading 1 of Q1 (from the ticket's description)", "    if chosen: Q1 goes by reading 1",
                    "  - b) reading 2 of Q1 (from the ticket's description)", "    if chosen: Q1 goes by reading 2",
                    f"  - or your own wording {EM_DASH} the readings are what the sources say, "
                    "not a closed list of answers.",
                    "  - Answer: `Q1: a`, `Q1: b` or `Q1: not needed`"]        # GW1-32: the one line added to the card of before
        check_eq("E-9 the card is exactly the card of before, line for line, plus its Answer line",
                 gate_brief.question_card(data["open_questions"][0], 1, data["question_effects"]), expected)
        text = gate_brief.render(data)
        check_not_in("E-9 no consequence lines", "what changes", text)
        check_not_in("E-9 and no offer to keep anything manual", "kept checked by hand", text)
    finally:
        drop(task_root)


def test_what_cannot_be_read_is_named_not_raised() -> None:
    """Edges: a patch with no case to show; a Then number beyond the case's list; a case whose
    `question_thens` is not JSON. Each says what is known and what could not be read."""
    rows = [plan_row("TS-3", what_we_verify="the retry limit",
                     if_answered={"Q3": {"*": {"disposition": "automate"}}}),
            plan_row("TS-4", "automate", what_we_verify="the size limit")]
    cases = {4: case_text(4, "TS-4", "Size limit", ["One.", "Two."],
                          question_thens=[{"question": "Q3", "then": 5, "readings": {"a": "Five is refused."}}]),
             8: case_text(8, "TS-8", "Broken fields", ["One."], raw_question_thens="[not json")}
    task_root = gate_story("qa-a2-unread-", [question("Q3")], rows, cases)
    try:
        text = packet(task_root)
        a = reading_of(card_of(text, "Q3"), "a")
        check_in("edge: a patch whose row has no case file says it could not read one",
                 "the retry limit would no longer be kept checked by hand. The factory does not switch "
                 "it by itself yet: after your answer, how it is checked is decided again, starting "
                 "from an automated test, and the report says what was decided. No case of it could "
                 "be read here", a)
        check_not_in("t-199 edge: the label branch does not promise `decide anew` either", "decide anew", text)
        check_in("edge: a Then number beyond the case's list says what the case has",
                 "the case has no Then 5 (its Thens are 1, 2)", a)
        check_in("edge: and the reading's own text is still shown", "Five is refused.", a)
        check_in("edge: a case whose per-answer texts are not JSON is named, once",
                 f"Not read, so not shown above: {full_id(8)}: its per-answer Then texts could not be read",
                 text)
        check_eq("edge: and named once, not once per reading", text.count(full_id(8)), 1)
        check_in("edge: the packet still ends in the answer block", "## How to answer", text)
    finally:
        drop(task_root)


def test_a_register_row_without_ac_ref_is_signed_by_its_source() -> None:
    """G1-0 (t-928, P23): a requirement of a task with no AC has no `ac_ref`; the first reading of its contradiction was signed
    `description` whatever it came from. Now the register's `source` word decides (`REGISTER_SOURCE_ORIGINS`), the AC id still wins when
    there is one, `derived` and an unknown word stay `description`, and every value is an origin `question_errors` accepts."""
    import grammar
    head = ("## Register\n\n| R | Requirement | source | derived_from | verifiable | ac_ref | observable |\n|---|---|---|---|---|---|---|\n")
    rows = {"R-1": ("discussion", "-"), "R-2": ("feature", "-"), "R-3": ("story", "-"), "R-4": ("ac", "AC-4"),
            "R-5": ("ac", "-"), "R-6": ("derived", "-"), "R-7": ("somethingnew", "-")}
    register = head + "".join(f"| {r} | text of {r} | {src} | - | yes | {ac} | - |\n" for r, (src, ac) in rows.items())
    register += ("\n## Contradiction matrix\n\n| R | comment |\n|---|---|\n"
                 + "".join(f"| {r} | contradicts: other {r} |\n" for r in rows))
    got = {r: v["first_from"] for r, v in planning_contract.register_contradiction_readings(register).items()}
    check_eq("the first reading is signed by the source word when there is no ac_ref; the AC id wins; derived and unknown stay description",
             got, {"R-1": "comment", "R-2": "parent_ticket", "R-3": "description", "R-4": "acceptance_criteria:AC-4",
                   "R-5": "acceptance_criteria", "R-6": "description", "R-7": "description"})
    check("every origin is a word `question_errors` accepts", all(v.split(":")[0] in contract.READING_ORIGINS for v in got.values()))
    check_eq("REGISTER_SOURCE_ORIGINS plus `derived` is exactly grammar.REQ_SOURCES: a new source word fails here, loudly (G1-3)",
             set(planning_contract.REGISTER_SOURCE_ORIGINS) | {"derived"}, set(grammar.REQ_SOURCES))


def test_a_row_that_names_its_register_question_is_not_asked_twice() -> None:
    """R8 item 4 and its position invariant."""
    row = {"id": "TS-4", "requirement_ids": ["R-4"], "level": "e2e-ui", "disposition": "automate",
           "oracle_unknown": True}
    task_root = gate_story("qa-a2-dupes-", [question("Q1")], [row], with_register_md=True)
    try:
        def asked(question_refs, plan=None):
            rows = [dict(row, **({"question_refs": question_refs} if question_refs is not None else {}))]
            return [q["id"] for q in gate_brief.contradiction_questions(task_root, plan or rows)]

        check_eq("item 4 control: a row with no `question_refs` still produces its question", asked(None), ["R-4"])
        check_eq("item 4: every ref resolves to a register id - no duplicate R-n question", asked(["Q1"]), [])
        check_eq("item 4 invariant: one ref resolves and one does not - the question stays", asked(["Q1", "Q99"]), ["R-4"])
        check_eq("item 4 invariant: a ref that resolves nowhere - the question stays", asked(["Q99"]), ["R-4"])
        check_eq("item 4: ids are case-sensitive - `q1` is not Q1", asked(["q1"]), ["R-4"])
        check_eq("item 4: an empty list resolves nothing", asked([]), ["R-4"])
        check_eq("item 4: a ref that is not a list resolves nothing", asked("Q1"), ["R-4"])
        rows_with = [dict(row, question_refs=["Q1"])]
        (task_root / "work" / "test-plan.json").write_text(json.dumps(rows_with), encoding="utf-8")
        text = packet(task_root)
        check_in("item 4: the register question is on the card", "- **Q1**", text)
        check_not_in("item 4: and its twin `R-4` is not", "- **R-4**", text)
        (task_root / "work" / "test-plan.json").write_text(json.dumps([row]), encoding="utf-8")
        check_in("item 4: without the ref the twin is asked, as before", "- **R-4**", packet(task_root))
    finally:
        drop(task_root)
    bare = gate_story("qa-a2-dupes2-", [], [dict(row, question_refs=["Q1"])], register=False,
                      with_register_md=True)
    try:
        check_eq("item 4 invariant: no register at all - nothing resolves, the question stays",
                 [q["id"] for q in gate_brief.contradiction_questions(
                     bare, [dict(row, question_refs=["Q1"])])], ["R-4"])
    finally:
        drop(bare)


def test_no_question_and_no_reading_is_cut() -> None:
    """R8 item 5 and E-13: every open question gets a card; readings up to z; over 26 is a finding."""
    many = [question(f"Q{n}", 2) for n in range(1, 13)]
    task_root = gate_story("qa-a2-many-", many)
    try:
        text = packet(task_root)
        check_in("item 5: the count is the count", "## Open questions (12)", text)
        for n in (1, 6, 7, 12):
            check_in(f"item 5: question {n} of 12 has its card, with its last reading",
                     f"reading 2 of Q{n}", card_of(text, f"Q{n}"))
        check_eq("item 5: twelve cards, not six", len(re.findall(r"(?m)^- \*\*Q[0-9]+\*\*", text)), 12)
        check_not_in("item 5: nothing is cut by the brief's line cap", "brief truncated", text)
        check_eq("item 5: and the answer block is still there, once", text.count("## How to answer"), 1)
    finally:
        drop(task_root)
    for count in (8, 9, 26):
        lines = gate_brief.question_card(question("Q1", count), 1)
        lettered = [line for line in lines if re.match(r"  - [a-z]\) ", line)]
        last = "abcdefghijklmnopqrstuvwxyz"[count - 1]
        check_eq(f"E-13 {count} readings: {count} lettered lines", len(lettered), count)
        check_in(f"E-13 {count} readings: the last one is lettered {last} and keeps its text",
                 f"  - {last}) reading {count} of Q1 (from the ticket's description)", lines)
    nine = gate_story("qa-a2-nine-", [question("Q1", 9)])
    try:
        check_in("E-13 nine readings in the packet: the ninth has letter i",
                 "  - i) reading 9 of Q1", packet(nine))
    finally:
        drop(nine)
    over = gate_brief.question_card(question("Q1", 27), 1)
    check_eq("E-13 27 readings: no letters at all", [l for l in over if re.match(r"  - [a-z]\) ", l)], [])
    check_in("E-13 27 readings: the card says it is the factory's own defect, not the person's",
             "The factory wrote 27 readings for this question, more than it can letter (26). "
             "That is the factory's own defect, not yours", over)
    check_in("E-13 27 readings: and offers the person's own words", "answer in your own words", over)
    check_in("E-13 27 readings: no reading is cut", "reading 27: reading 27 of Q1 (from the ticket's description)", over)


def test_the_decision_text_holds_the_words_where_they_are_stored() -> None:
    """R12 / item 6 (B-181): the gate record keeps the answer in `authorization_source`."""
    gate = {"gates": {"A": {"decision": "approved", "authorization_source": "R-4: a\ngo on"}}}
    check_in("item 6: `authorization_source` is read", "R-4: a", gate_brief._decision_text(gate))
    check_not_in("item 6: a caller that asks for the non-gate decisions does not get the gate's words",
                 "R-4: a", gate_brief._decision_text(gate, with_gates=False))
    row = {"id": "TS-4", "requirement_ids": ["R-4"], "level": "e2e-ui", "disposition": "automate",
           "oracle_unknown": True}
    task_root = gate_story("qa-a2-words-", [], [row], pipeline=gate, with_register_md=True)
    try:
        check_eq("item 6: the gate's words name R-4, so the fork is not asked again",
                 gate_brief.contradiction_questions(task_root, [row]), [])
    finally:
        drop(task_root)
    other = gate_story("qa-a2-words2-", [], [row], with_register_md=True,
                       pipeline={"gates": {"A": {"decision": "approved", "authorization_source": "R-44: b"}}})
    try:
        check_eq("item 6 class: `R-44` is not `R-4` - an id is never matched as a substring",
                 [q["id"] for q in gate_brief.contradiction_questions(other, [row])], ["R-4"])
    finally:
        drop(other)


class Tolerant(dict):
    """A row that answers "" for a key it lacks: a question missing from a listing is a FAIL line
    of the check that reads it, never a crash that hides the other checks."""

    def __missing__(self, key):
        return ""


def test_question_status_comes_from_the_register() -> None:
    """R12 / item 7: `answered` and `not_needed` are not listed; `named` is, with its note; ids exact."""
    ids = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q10"]
    questions = [question(qid) for qid in ids] + [{"question": "a bare question with no id",
                                                   "severity": "minor", "owner_role": "po_ba"}]
    words = "go on\nlet us see about Q5\nQ10: a\nq6: a"   # GW1-47: a line STARTING with an id is read as a stray line (`q6: a`); Q5 is only named mid-line
    task_root = gate_story("qa-a2-status-", questions,
                           pipeline={"gates": {"A": {"decision": "approved", "authorization_source": words}}})
    try:
        shown = {q["id"]: q["row_hash"] for q in QR.load(task_root)["questions"]}
        stale = "0" * 64
        QR.record(task_root, "Q2", "answered", "Q2: a", "gate A", "person", shown["Q2"], reading="a")
        QR.record(task_root, "Q3", "not_needed", "Q3: not needed", "gate A", "person", shown["Q3"])
        QR.record(task_root, "Q4", "answered", "Q4: a", "gate A", "person", stale, reading="a")
        QR.record(task_root, "Q7", "not_needed", "Q7: not needed", "gate A", "person", stale)
        got = gate_brief.unanswered_questions(task_root)
        by_id = collections.defaultdict(Tolerant, {q.get("id"): Tolerant(q) for q in got})
        check_eq("item 7: listed are open, changed, named and the row the register cannot place; "
                 "`answered` Q2 and `not_needed` Q3 are not",
                 [q.get("id") for q in got], ["Q1", "Q4", "Q5", "Q6", "Q7", "Q10", None])
        check_eq("item 7: an `open` question carries no note", by_id["Q1"]["status_note"], "")
        named = "named in your gate A words; the factory recorded no answer"
        check_eq("item 7: `named` Q5 says exactly that", by_id["Q5"]["status_note"], named)
        check_eq("item 7: `named` Q10 says exactly that", by_id["Q10"]["status_note"], named)
        check_eq("item 7: and is `named`, never `answered`", by_id["Q5"]["status"], "named")
        check_not_in("item 7: the suffix `answered at` is not attached to a named question",
                     "answered at", by_id["Q5"]["status_note"])
        check_eq("item 7: ids are exact - Q10 named does not make Q1 named", by_id["Q1"]["status"], "open")
        check_eq("item 7: ids are case-sensitive - `q6: a` does not name Q6", by_id["Q6"]["status"], "open")
        check_in("item 7: a changed `answered` question says its text changed and is asked again",
                 "its text changed after your answer, so it is asked again", by_id["Q4"]["status_note"])
        check_in("item 7: and only an `answered` one carries the suffix `answered at gate A`",
                 "(answered at gate A)", by_id["Q4"]["status_note"])
        check_in("item 7: a changed `not_needed` question says its text changed",
                 "its text changed after your answer", by_id["Q7"]["status_note"])
        check_not_in("item 7: but it does not carry the `answered` suffix", "answered at",
                     by_id["Q7"]["status_note"])
        check_in("item 7: a question with no id is listed as it stands, not dropped",
                 "a bare question with no id", json.dumps(by_id[None]))
        shown_packet = packet(task_root)
        check_in("item 7: the gate A card of a named question carries the note too", named + ".",
                 card_of(shown_packet, "Q5"))
        check_in("item 7: the card of a changed question says so", "its text changed after your answer",
                 card_of(shown_packet, "Q4"))
        check_not_in("item 7 (FR-7): an answered question has no card to be asked again", "- **Q2**", shown_packet)
        check_not_in("item 7 (FR-7): nor a `not_needed` one", "- **Q3**", shown_packet)
        lines = gate_brief.open_before_mr(task_root)
        blob = "\n".join(lines)
        check_in("item 7: the MR list carries the named note", named, blob)
        check_not_in("item 7: and does not list the answered question", "What must happen for Q2?", blob)
        check_eq("item 7 (FR-10): the gate A packet lists the same questions as the MR list",
                 [q.get("id") for q in gate_brief.collect(TICKET, task_root)["open_questions"]],
                 [q.get("id") for q in got])
    finally:
        drop(task_root)


def test_a_register_that_cannot_be_read_is_said_and_never_read_as_answered() -> None:
    """Edge: `question_register.load` raising, or the register file absent: today's behaviour
    plus one line saying question status could not be read."""
    words = {"gates": {"A": {"decision": "approved", "authorization_source": "Q1: a"}}}
    task_root = gate_story("qa-a2-broken-", [question("Q1"), question("Q2")], pipeline=words)
    real = QR.load

    def broken(_root):
        raise RuntimeError("the register is unreadable on purpose")

    QR.load = broken
    try:
        data = gate_brief.collect(TICKET, task_root)
        text = gate_brief.render(data)
        check_eq("edge: both questions are still carded", [q["id"] for q in data["open_questions"]], ["Q1", "Q2"])
        check_eq("edge: one line says question status could not be read",
                 text.count("Question status could not be read"), 1)
        check_in("edge: and says the questions are shown as they stand",
                 "so every question below is shown as it stands.", text)
        check_eq("edge: the listing does not call any of them answered",
                 [q.get("status") for q in gate_brief.unanswered_questions(task_root)], [None, None])
        check_in("edge: the MR list carries its own one line",
                 "question status could not be read", "\n".join(gate_brief.open_before_mr(task_root)))
    finally:
        QR.load = real
        drop(task_root)
    absent = gate_story("qa-a2-absent-", [], [{"id": "TS-4", "requirement_ids": ["R-4"], "level": "e2e-ui",
                                                "disposition": "automate", "oracle_unknown": True}],
                        register=False, with_register_md=True)
    try:
        text = packet(absent)
        check_in("edge: no register file, a question from the plan row: the one line",
                 "Question status could not be read (the story has no questions register file)", text)
        check_in("edge: and the question is still carded", "- **R-4**", text)
    finally:
        drop(absent)


def test_an_empty_register_and_a_question_with_no_readings() -> None:
    """Edge: nothing to ask prints nothing; a question no reading can be named for asks for words."""
    empty = gate_story("qa-a2-empty-", [])
    try:
        text = packet(empty)
        check_not_in("edge: an empty register prints no question section", "## Open questions", text)
        check_not_in("edge: and no answer block", "## How to answer", text)
    finally:
        drop(empty)
    lonely = question("Q5", 0, readings_unnameable=True)
    card = gate_brief.question_card(lonely, 1)
    check_eq("edge: a zero-reading question has no letters", [l for l in card if re.match(r"  - [a-z]\) ", l)], [])
    check_in("edge: and asks for the person's own words", "No reading can be named for this one. "
             "Answer in your own words, or write `Q5: not needed`.", card)
    task_root = gate_story("qa-a2-lonely-", [lonely])
    try:
        text = packet(task_root)
        check_in("edge: it is carded in the packet", "- **Q5**", text)
        how = text[text.index("## How to answer"):]
        check_not_in("edge: with no letter form offered, there being no letter to choose", "<letter>", how)
        check_in("edge: `not needed` is still offered", "`<question id>: not needed`", how)
    finally:
        drop(task_root)


def test_a_before_now_question_shows_both_and_asks_the_fixed_pair() -> None:
    """t-227 (P20): TC_015 asked for the code P-multi returns and no question existed; the 403 came
    from the diff. A behaviour claim's question carries `before` and `now`, each `{value, where}`,
    and its two readings are the fixed pair, both `from: claim` (never `from: code`)."""
    fixtures = Path(__file__).resolve().parent / "fixtures" / "oracle-provenance"
    asked = {q["id"]: q for q in json.loads(
        (fixtures / "requirements-readiness.json").read_text(encoding="utf-8"))["open_questions"]}
    q1, q7 = asked["Q1"], asked["Q7"]
    check_eq("a question written before t-227 (the verbatim cmp2 Q1) is still answerable as it stands",
             contract.question_errors(q1), [])
    check_eq("a before/now question is answerable as it stands", contract.question_errors(q7), [])
    check("`claim` is a reading origin", "claim" in contract.READING_ORIGINS)
    # the fixture predates the `claim` field (HF4-7): the texts are the code's pair, and the question is READ as it
    check_eq("the fixture's Q7 readings are the fixed pair the code builds (less the `claim` mark it predates)",
             q7["readings"], [{k: v for k, v in r.items() if k != "claim"} for r in contract.claim_readings("unknown", "400")])
    check_eq("...and a pair of the code's is recognised by its texts: now = a, before = b",
             (contract.claim_reading_index(q7, "now"), contract.claim_reading_index(q7, "before")), (0, 1))
    check_eq("both readings come from `claim`", [r["from"] for r in q7["readings"]], ["claim", "claim"])
    check_in("with the base revision unreadable, reading (b) says so and asks what it was",
             "the behaviour before the change is the expected one - unknown; say what it was",
             q7["readings"][1]["reading"])
    known = contract.claim_readings("400", "403")
    check_in("with a known before, reading (b) names it", "(400)", known[1]["reading"])
    check_in("and reading (a) names the behaviour now as data", "(403)", known[0]["reading"])
    check_eq("two readings, no third: the person's own wording is always open to them, never written",
             len(known), 2)

    only_before = {k: v for k, v in q7.items() if k != "now"}
    check_in("`before` without `now` asks nothing", "carries `before` but no `now`",
             contract.question_errors(only_before))
    no_where = dict(q7, now={"value": "400", "where": " "})
    check_in("a `now` with no `where` is refused", "question.now needs value and where",
             contract.question_errors(no_where))
    check_in("a `before` that is not an object is refused", "question.before needs value and where",
             contract.question_errors(dict(q7, before="400")))
    from_code = json.loads(json.dumps(q7))
    from_code["readings"][0]["from"] = "code"
    check_in("a reading `from: code` on a before/now question is refused (NOW is data, not a source)",
             "readings[0].from must be `claim`", contract.question_errors(from_code))
    ordinary = json.loads(json.dumps(q1))
    ordinary["readings"][0]["from"] = "code"
    check_eq("while an ordinary question may still cite the code", contract.question_errors(ordinary), [])


# --- GW1-32: ONE list of the forms of an answer ---------------------------------------------------------------------------------

LINE_ITEM = {"id": "fx-1", "check": "fx", "class": "person_decides", "message": "the stand lacks a second user", "fix": "write the line",
             "waives": [{"block": "stand gap: TC-1", "stage": "S5", "option": "accept"}]}
WORDS_ITEM = {"id": "fx-2", "check": "fx", "class": "person_decides", "message": "a words item", "fix": "say it"}
RENUMBERED = dict(LINE_ITEM, id="fx-9")


def forms_data(questions=None, findings=None, cards=None, example="") -> dict:
    return {"task": TICKET, "open_questions": questions or [], "case_id_example": example, "stand_gap_cards": cards or [],
            "rehearsal": ({"gate": "A", "next_stage": "S5", "can_proceed": False, "by_class": {}, "findings": findings}
                          if findings is not None else {})}


def read_by(row: dict, data: dict, questions: list):
    """Feed the row's `example` to the function its `reader` names; the answer is the reader's own count of what it took."""
    import story_run
    example, reader = row["example"], row["reader"]
    if reader == "parse_choices":
        parsed = QR.parse_choices(example, questions, [full_id(9)])
        return len(parsed["choices"]) + len(parsed["not_needed"]) + len(parsed["case_tokens"])
    if reader == "read_stand_gap_answers":
        return len(gate_brief.read_stand_gap_answers(example, [{"id": "g-1", "case_id": full_id(9)}])["read"])
    driver = story_run.Driver.__new__(story_run.Driver)
    if reader == "Driver.as_is_word":
        return int(driver.as_is_word("gate_A", example))
    if reader == "Driver.read_finding_doors":
        findings = [f for f in data["rehearsal"]["findings"] if f.get("waives")]
        shown = "\n".join(f"- [{f['id']}] {f['message']}" for f in findings)
        doors = {f["id"]: f["waives"] for f in findings}
        return len(driver.read_finding_doors(example, findings, shown, doors)["read"])
    return -1       # a reader this test does not know is a red line, not a pass


def test_answer_forms_are_one_list_and_each_has_its_reader() -> None:
    """GW1-32: every form with an example is taken by the reader it names (FR-11, AR-24); a line outside the list is taken by none."""
    questions = [question("Q1"), question("Q4")]
    findings = [LINE_ITEM, WORDS_ITEM, dict(WORDS_ITEM, id="cp-1", check="case_preconditions", message=full_id(9) + ": needs a user")]
    gap = {"id": "g-1", "case_id": full_id(9)}
    cards = ["## Stand gaps (1)"] + gate_brief._answer_words([gap], ["g-1"], gate_brief.stand_gap_words(), {"g-1": full_id(9)},
                                                             gate_brief.stand_gap_word_of())
    data = forms_data(questions, findings, cards, full_id(9))
    forms = gate_brief.answer_forms(data, questions)
    names = [row["form"] for row in forms]
    check_eq("GW1-32 each form is on the list once (one line per form)", len(names), len(set(names)))
    for expected in ("<question id>: <letter>", "<question id>: not needed", "<full case id>: manual", "<full case id>: automate",
                     "<full case id>: accept as blocked", gate_brief.STAND_GAP_FORM, "<item id>: accept <your reason>", "approve as is"):
        check_in(f"GW1-32 the list holds {expected}", expected, names)
    for row in forms:
        check_eq(f"GW1-32 a row carries exactly the five keys: {row['form']}", sorted(row), ["example", "form", "reader", "says", "where"])
        check(f"GW1-32 the example of `{row['form']}` is taken by {row['reader']}", read_by(row, data, questions) == 1,
              f"{row['example']!r} -> {read_by(row, data, questions)}")
    # the negative control: a line that is on no form is read by none of the readers (the controls share the readers' own shape)
    check_eq("GW1-32 control: `Q1: maybe` is no choice and no `not needed`", read_by(
        {"example": "Q1: maybe", "reader": "parse_choices"}, data, questions), 0)
    check_eq("GW1-32 control: a stand-gap line with an unlisted word is not read", read_by(
        {"example": f"{full_id(9)}: maybe", "reader": "read_stand_gap_answers"}, data, questions), 0)
    check_eq("GW1-32 control: an item line with an unlisted word is not read", read_by(
        {"example": "fx-1: maybe", "reader": "Driver.read_finding_doors"}, data, questions), 0)
    check_eq("GW1-32 control: `approve as is, but fix X` is not the as-is word", read_by(
        {"example": "approve as is, but fix X", "reader": "Driver.as_is_word"}, data, questions), 0)


def test_answer_forms_edges() -> None:
    """GW1-32 edges: nothing to answer, no letters, a door that is none, a renumbered id, the block outliving the cap."""
    check_eq("GW1-32 edge: no question, no item, no gap - no form", gate_brief.answer_forms(forms_data(), []), [])
    check_eq("GW1-32 edge: and no section", "## How to answer" in gate_brief.render(forms_data()), False)
    check_eq("GW1-32 edge: no form, no block lines", gate_brief.how_to_answer_lines([]), [])
    lonely = question("Q5", 0, readings_unnameable=True)
    names = [row["form"] for row in gate_brief.answer_forms(forms_data([lonely]), [lonely])]
    check_not_in("GW1-32 edge: questions with no letter offer no letter form", "<question id>: <letter>", names)
    check_in("GW1-32 edge: ...only `not needed` (and the case words)", "<question id>: not needed", names)
    three = [question("Q1"), question("Q2"), question("Q3")]
    text = gate_brief.render(forms_data(three, example=full_id(9)))
    check_eq("GW1-32 edge: three questions with the same example - one line per form", text.count("`<question id>: not needed`"), 1)
    # a door of kind none gets no line form, only the as-is word
    none_item = dict(WORDS_ITEM, id="fx-3", message="x" * 80)          # one word longer than 60: no door that passes its own check
    rows = gate_brief.answer_forms(forms_data(findings=[none_item]), [])
    check_eq("GW1-32 edge: an item with no line door - only `approve as is`", [row["form"] for row in rows], ["approve as is"])
    check_eq("GW1-32 edge: ...and no item at all - none", gate_brief.answer_forms(forms_data(findings=[]), []), [])
    # the renumbered id: the example carries the id of THIS rehearsal, and the old id is read by nobody
    rows = gate_brief.answer_forms(forms_data(findings=[RENUMBERED]), [])
    line = next(row for row in rows if row["reader"] == "Driver.read_finding_doors")
    check_in("GW1-32 edge: the example carries the real id of the item", "fx-9: ", line["example"])
    import story_run
    d = story_run.Driver.__new__(story_run.Driver)
    shown = f"- [fx-9] {RENUMBERED['message']}"
    stale = d.read_finding_doors("fx-1: accept known", [RENUMBERED], shown, {"fx-9": RENUMBERED["waives"]})
    check_eq("GW1-32 edge: a renumbered (old) id is read by nobody", (stale["read"], stale["unread"]), ([], []))
    # (the block outliving the cap, with and without a question, is pinned on the golden packet in test_gate_brief_and_retro.py)


def test_answer_line_and_the_helper_sentence() -> None:
    """GW1-32: the last line of a card is its own `Answer:`; one sentence names the assistant; the text a person reads obeys the rules."""
    q1, q5 = question("Q1"), question("Q5", 0, readings_unnameable=True)
    check_eq("GW1-32 the card ends with the forms of THIS question, with its own id",
             gate_brief.question_card(q1, 1)[-1], "  - Answer: `Q1: a`, `Q1: b` or `Q1: not needed`")
    check_eq("GW1-32 a question with no reading is offered `not needed` alone",
             gate_brief.question_card(q5, 1)[-1], "  - Answer: `Q5: not needed`")
    many = question("Q6", len(gate_brief.QUESTION_LETTERS) + 1)
    check_eq("GW1-32 more readings than letters: `not needed` alone", gate_brief.question_card(many, 1)[-1], "  - Answer: `Q6: not needed`")
    data = forms_data([q1, q5], [LINE_ITEM, WORDS_ITEM], example=full_id(9))
    text = gate_brief.render(data)
    for needle in ("a person's helper", "read by a helper", "a helper turns"):
        check_not_in(f"GW1-32 the old helper wording is gone: {needle}", needle, text)
        check_not_in(f"GW1-32 ...and from the constants: {needle}", needle, gate_brief.APPROVAL_FIRST_LINE_TAIL + gate_brief.ANYTHING_ELSE_SENTENCE)
    check_in("GW1-32 the one sentence names the assistant", "the assistant running this story", gate_brief.ANYTHING_ELSE_SENTENCE)
    check_in("GW1-32 the approval-word boundary is kept", "unless your answer starts with the word that approves this gate",
             gate_brief.APPROVAL_FIRST_LINE_TAIL)
    check_eq("GW1-32 the answer block obeys human-questions.md",
             [p["rule"] for p in human_text.problems(text[text.index("## Open questions"):])], [])


def vcs_repo(prefix: str, dirty: tuple = (), pipeline_text=None, state_of=None):
    """A temp project whose tests folder is its own git repository: one committed file, `dirty` untracked paths, and the factory's own
    folder (`qa-factory/`, untracked) beside them. Returns (task_root, head). `pipeline_text` replaces pipeline.json as written."""
    import os
    import subprocess
    root = temp_dir(prefix)
    task_root = root / "qa-factory" / "artifacts" / "TP1-15045"
    (task_root / "state").mkdir(parents=True)
    (root / "qa-factory" / "config.json").write_text("{}", encoding="utf-8")
    (task_root / "pipeline.json").write_text(pipeline_text if pipeline_text is not None else json.dumps({"ticket": "TP1-15045"}), encoding="utf-8")
    env = dict(os.environ, GIT_AUTHOR_NAME="qa", GIT_AUTHOR_EMAIL="qa@example.invalid", GIT_COMMITTER_NAME="qa",
               GIT_COMMITTER_EMAIL="qa@example.invalid")
    (root / "base.py").write_text("x = 1\n", encoding="utf-8")
    for args in (["init", "-b", "main"], ["add", "base.py"], ["commit", "-m", "base", "--no-gpg-sign"]):
        subprocess.run(["git", *args], cwd=str(root), env=env, capture_output=True, text=True)
    for name in dirty:
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("y = 2\n", encoding="utf-8")
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(root), capture_output=True, text=True).stdout.strip()
    return task_root, head


def vcs_finding(task_root: Path) -> dict:
    """The `vcs-test-repo` finding of a rehearsal's `check_vcs`, or {}."""
    rehearsal = gate_preflight.Rehearsal(task_root, "A")
    rehearsal.check_vcs()
    return next((f for f in rehearsal.findings if f.get("id") == "vcs-test-repo"), {})


def read_vcs_line(finding: dict, words: str):
    """What `Driver.read_finding_doors` takes of `words` for this finding, shown as the packet shows it: [(word option, door option)]."""
    import story_run
    driver = story_run.Driver.__new__(story_run.Driver)
    shown = f"- [{finding['id']}] {finding['message']}"
    got = driver.read_finding_doors(words, [finding], shown, {finding["id"]: finding["waives"]})
    return [(r["word"], r["door"]["option"]) for r in got["read"]], [u["line"] for u in got["unread"]]


def test_the_test_repository_question_offers_its_words_with_prices() -> None:
    """FG7-8 B1: a dirty tree is one finding whose doors are `accept` (HEAD block, as before), `go on` and - on the block of the changes
    shown - `commit` and `stash`; the `answers` list every path whole, then each word with its three price lines (B-5); each word is
    read by the driver's reader, a question or a longer sentence is read as nothing (I-3)."""
    task_root, head = vcs_repo("qa-vcs-words-", ("u.py", "d/v.py"))
    found = vcs_finding(task_root)
    head12 = head[:12]
    check_eq("the message is today's, over the person's paths from the `-z` read (the factory's folder left out)", found["message"],
             f"the test repository has 2 uncommitted change(s) on branch `main` (HEAD {head12}), and S5 writes test code into it: d/v.py, u.py")
    doors = found["waives"]
    check_eq("doors in order: accept on the HEAD block as today, go on on it too, then commit and stash on the block of the changes",
             [(d["option"], d["block"].startswith("test repository changes")) for d in doors],
             [("accept", False), ("vcs_go_on", False), ("vcs_commit", True), ("vcs_stash", True)])
    check_eq("the accept door is byte-equal to today's", doors[0], {"block": f"test repository state: {head12}", "stage": "S5", "option": "accept"})
    check_eq("the writing words' block is `test repository changes: <head12> <digest of the list>`", doors[2]["block"].split(" ")[:4],
             ["test", "repository", "changes:", head12])
    check_eq("both writing words stand on one block", doors[2]["block"], doors[3]["block"])
    answers = found["answers"]
    check_eq("every path is listed whole, under the header that says what takes them", answers[:3],
             ["your uncommitted changes (2), all listed - commit and stash take exactly these:", "  - d/v.py", "  - u.py"])
    labels = gate_brief._price_labels()
    for word in ("commit", "stash", "go on"):
        at = next(i for i, line in enumerate(answers) if line.startswith(f"`vcs-test-repo: {word}` - "))
        check_eq(f"`{word}` is followed by its three price lines, in order",
                 [line.strip().startswith(label) for line, label in zip(answers[at + 1:at + 4], labels)], [True, True, True])
    check_eq("the answers obey the rules of text a person reads", [p["rule"] for p in human_text.problems("\n".join(answers), kind="report")], [])
    check_in("the fix is one line that points at the words under the item", "answer with one of the words listed under this item - ", found["fix"])
    check_eq("it is one line", "\n" in found["fix"], False)
    for word, option in (("commit", "vcs_commit"), ("stash", "vcs_stash"), ("go on", "vcs_go_on"), ("`vcs-test-repo`: `commit`", "vcs_commit"),
                         ("- vcs-test-repo: Stash them", "vcs_stash")):
        text = word if word.startswith(("`", "-")) else f"vcs-test-repo: {word}"
        check_eq(f"`{text}` is read by the driver with its option", read_vcs_line(found, text)[0], [(option, option)])
    check_eq("`maybe` is read by none", read_vcs_line(found, "vcs-test-repo: maybe")[0], [])
    check_eq("`commit please` is read by none (a repository write is never taken out of a sentence)", read_vcs_line(found, "vcs-test-repo: commit please")[0], [])
    check_eq("two lines `commit` then `commit?`: both unread, the earlier set aside", read_vcs_line(found, "vcs-test-repo: commit\nvcs-test-repo: commit?")[0], [])
    check_eq("`go on` with the person's reason is read, the reason kept", read_vcs_line(found, "vcs-test-repo: go on, the branch is mine")[0], [("vcs_go_on", "vcs_go_on")])
    forms = gate_brief.answer_forms(forms_data(findings=[found]), [])
    names = [row["form"] for row in forms]
    for word in ("commit", "stash", "go on"):
        check_in(f"the forms list holds `<item id>: {word}`", f"<item id>: {word}", names)
    for row in forms:
        if row["reader"] == "Driver.read_finding_doors" and row["form"] != "<item id>: accept <your reason>":
            check_eq(f"the example `{row['example']}` is read by the driver", len(read_vcs_line(found, row["example"])[0]), 1)
    product = dict(LINE_ITEM, id="gap-1", waives=[{"block": "x gap", "stage": "S5", "option": "product_gap"}, LINE_ITEM["waives"][0]])
    check_in("a product-gap item gets its own form by the same rule", "<item id>: product gap",
             [row["form"] for row in gate_brief.answer_forms(forms_data(findings=[product]), [])])


def test_the_words_are_offered_only_where_they_can_be_carried_out() -> None:
    """FG7-8 B1 edges: the cap is 20 (20 lists all and offers the words, 21 lists none and offers only `go on` and `accept`); a run that
    leaves no trace or whose pipeline cannot be read offers no writing word; no HEAD, no door; a clean tree is today's question."""
    writes = ("vcs_commit", "vcs_stash")

    def options(found):
        return [d["option"] for d in found["waives"]]
    task_root, _ = vcs_repo("qa-vcs-cap20-", tuple(f"f{n:02d}.py" for n in range(20)))
    found = vcs_finding(task_root)
    check_eq("20 person entries: the writing words are offered", [o for o in options(found) if o in writes], list(writes))
    check_eq("...and all 20 paths are listed", len([a for a in found["answers"] if a.startswith("  - ")]), 20)
    task_root, _ = vcs_repo("qa-vcs-cap21-", tuple(f"f{n:02d}.py" for n in range(21)))
    found = vcs_finding(task_root)
    check_eq("21 person entries: only accept and go on", options(found), ["accept", "vcs_go_on"])
    check_eq("...no path is listed", [a for a in found["answers"] if a.startswith("  - ")], [])
    check_in("...the over-cap sentence says how many there are and what to do", "your uncommitted changes (21) are more than the 20 this question can list",
             found["answers"][0])
    check_in("...and names the item's own word", f"answer `{found['id']}: go on`", found["answers"][0])
    check_eq("...and `commit` is read by none", read_vcs_line(found, "vcs-test-repo: commit")[0], [])
    for label, pipeline in (("no-trace", json.dumps({"ticket": "TP1-15045", "no_trace": True})), ("unreadable pipeline", "{not json")):
        task_root, _ = vcs_repo("qa-vcs-closed-", ("u.py",), pipeline_text=pipeline)
        found = vcs_finding(task_root)
        check_eq(f"{label}: only accept and go on", options(found), ["accept", "vcs_go_on"])
        check_in(f"{label}: the hint names go on and no list", "`vcs-test-repo: go on`", "\n".join(found["answers"]))
        check_eq(f"{label}: `commit` is read by none", read_vcs_line(found, "vcs-test-repo: commit")[0], [])
    task_root, _ = vcs_repo("qa-vcs-clean-")
    clean = vcs_finding(task_root)
    check_eq("a clean tree is today's question: one accept door, no answers", ([d["option"] for d in clean["waives"]], "answers" in clean), (["accept"], False))
    real = gate_brief.finding_door_words
    try:
        gate_brief.finding_door_words = lambda: []
        task_root, _ = vcs_repo("qa-vcs-novocab-", ("u.py",))
        found = vcs_finding(task_root)
        check_eq("an unreadable vocabulary: only accept, plain-words fix, no answers", (options(found), "answers" in found, "listed under" in found["fix"]),
                 (["accept"], False, False))
    finally:
        gate_brief.finding_door_words = real
    import tempfile
    nowhere = Path(tempfile.mkdtemp(prefix="qa-vcs-none-"))
    try:
        check_eq("no repository: nothing to decide", gate_preflight.vcs_changes(nowhere, {}, nowhere), None)
    finally:
        cleanup(nowhere)


def test_the_blockers_name_what_the_words_cannot_take() -> None:
    """FG7-8 B1: `vcs_blockers` per class (the Lead's decisions on the B0-2 measurement): staged changes and submodules block the stash
    alone, a detached HEAD the commit alone, intent-to-add, conflicts, an operation, a nested repository, a guard separator, a path
    under the factory's folder and an unknown home block both."""
    def state(*entries, **more):
        person = [{"xy": xy, "path": path, "orig": orig} for xy, path, orig in entries]
        return dict({"person": person, "home": ("qa-factory/", ""), "head": "a" * 40, "branch": "main", "modes": {}, "ops": []}, **more)
    blockers = gate_preflight.vcs_blockers
    for label, built, commit, stash in (
            ("plain untracked, modified, deleted", state(("??", "a", ""), (" M", "b", ""), (" D", "c", "")), False, False),
            ("a staged entry `M `", state(("M ", "a", "")), False, True), ("`MM`", state(("MM", "a", "")), False, True),
            ("`D `", state(("D ", "a", "")), False, True), ("`R ` (new then old)", state(("R ", "new", "old")), False, True),
            ("a submodule by mode", state((" M", "sub", ""), modes={"sub": "160000"}), False, True),
            ("`.gitmodules`", state((" M", "sub/.gitmodules", "")), False, True),
            ("intent-to-add", state((" A", "a", "")), True, True), ("a conflict", state(("UU", "a", "")), True, True),
            ("an operation in progress", state(("??", "a", ""), ops=["REVERT_HEAD"]), True, True),
            ("a nested repository", state(("??", "x/", "")), True, True), ("a guard separator", state(("??", "a;b", "")), True, True),
            ("a rename out of the factory's folder", state(("R ", "src/y", "qa-factory/x")), True, True),
            ("an unknown home", state(("??", "a", ""), home=("", "unknown")), True, True),
            ("no home in this tree", state(("??", "a", ""), home=("", "outside")), False, False),
            ("a detached HEAD", state(("??", "a", ""), branch="HEAD"), True, False),
            ("no commit yet", state(("??", "a", ""), head=""), True, True),
            ("more than 20", state(*[("??", f"f{n}", "") for n in range(21)]), True, True)):
        check_eq(f"{label}: commit blocked / stash blocked", (bool(blockers(built)["commit"]), bool(blockers(built)["stash"])), (commit, stash))


def test_the_shown_doors_have_one_writer_and_one_reader() -> None:
    """FG7-8 B1: `keep_shown_doors` / `shown_doors_of` - the driver's form (its state dict), the skill form (the state file), the three
    no-write guards, and unreadable reads as None (I-2, AR-28)."""
    doors = {"vcs-test-repo": [{"block": "b", "stage": "S5", "option": "accept"}]}
    state: dict = {"other": 1}
    gate_brief.keep_shown_doors(None, doors, state=state)
    check_eq("driver form: the doors are in the dict, the rest of it kept", (state["shown_doors"], state["other"]), ({"A": doors}, 1))
    check_eq("...and read back from the dict", gate_brief.shown_doors_of(state=state), doors)
    folder = temp_dir("qa-shown-doors-")
    (folder / "state").mkdir()
    gate_brief.keep_shown_doors(folder, doors)
    check_eq("skill form: written into state/driver-state.json, read back", gate_brief.shown_doors_of(folder), doors)
    (folder / "state" / "driver-state.json").write_text(json.dumps({"shown_attachments": {"A": []}, "shown_doors": {"B": {"x": []}}}), encoding="utf-8")
    gate_brief.keep_shown_doors(folder, doors)
    held = json.loads((folder / "state" / "driver-state.json").read_text(encoding="utf-8"))
    check_eq("...keeping the other keys and the other gate's doors", (held["shown_attachments"], held["shown_doors"]), ({"A": []}, {"B": {"x": []}, "A": doors}))
    check_eq("a gate that stored nothing reads as None", gate_brief.shown_doors_of(folder, gate="Z"), None)
    absent = temp_dir("qa-shown-doors-absent-") / "T"
    gate_brief.keep_shown_doors(absent, doors)
    check_eq("guard: a story folder that does not exist is not created", absent.exists(), False)
    decided = temp_dir("qa-shown-doors-decided-")
    (decided / "state").mkdir()
    (decided / "state" / "controller.json").write_text(json.dumps({"source_revision": "r", "decisions": {"d": {"gate": "A", "status": "approved", "source_revision": "r"}}}), encoding="utf-8")
    gate_brief.keep_shown_doors(decided, doors)
    check_eq("guard: an approved gate A decision stands - nothing is written", (decided / "state" / "driver-state.json").exists(), False)
    (decided / "state" / "controller.json").write_text("{broken", encoding="utf-8")
    gate_brief.keep_shown_doors(decided, doors)
    check_eq("guard: a decision that cannot be read - nothing is written", (decided / "state" / "driver-state.json").exists(), False)
    broken = temp_dir("qa-shown-doors-broken-")
    (broken / "state").mkdir()
    (broken / "state" / "driver-state.json").write_text("[1, 2]", encoding="utf-8")
    gate_brief.keep_shown_doors(broken, doors)
    check_eq("guard: a state file that is not an object is left as it was, and reads as None",
             ((broken / "state" / "driver-state.json").read_text(encoding="utf-8"), gate_brief.shown_doors_of(broken)), ("[1, 2]", None))
    check_eq("unreadable: no file reads as None", gate_brief.shown_doors_of(temp_dir("qa-shown-doors-none-")), None)


def test_the_answers_are_printed_whole_on_both_roads() -> None:
    """FG7-8 B1: a row with `answers` is printed whole under its row by `brief_lines` (never cut by `limit`, which counts the other rows),
    by `render` indented under `fix`, and `gate_brief.render` grows its cap by their lines; a row with none is byte-identical to before."""
    answers = ["your uncommitted changes (2), all listed - x takes exactly these:", "  - a.py", "`<check-id>: go on` - go on", "  the factory: nothing."]
    rows = [{"id": f"p-{n}", "check": "p", "class": gate_preflight.PERSON_DECIDES, "message": f"plain {n}", "fix": "f"} for n in range(1, 7)]
    rows.append({"id": "vcs-test-repo", "check": "vcs", "class": gate_preflight.PERSON_DECIDES, "message": "the tree", "fix": "one line", "answers": answers})
    result = {"gate": "A", "next_stage": "S5", "can_proceed": False, "by_class": {gate_preflight.PERSON_DECIDES: 7}, "findings": rows, "info": []}
    lines = gate_preflight.brief_lines(result)
    check_eq("the 7th of 7 rows is shown with every answers line under it", lines[lines.index("- [your call] the tree") + 1:][:4], [f"  {a}" for a in answers])
    check_in("the limit counted the OTHER rows: one of them is `+1 more`", "- (+1 more", "\n".join(lines))
    text = gate_preflight.render(result)
    check_in("render: the answers are indented under fix", "      fix: one line\n          your uncommitted changes (2)", text)
    plain = dict(result, findings=rows[:6])
    check_eq("no answers: brief_lines is the five rows and `+1 more` as before", gate_preflight.brief_lines(plain)[-1].startswith("- (+1 more"), True)
    check_eq("no answers: render prints the one-line fix as before", "      fix: f\n  - [p-2]" in gate_preflight.render(plain), True)
    many = ["your uncommitted changes (30), all listed - x takes exactly these:"] + [f"  - file{n}.py" for n in range(30)] + ["`<check-id>: go on` - go on"]
    cover = gate_brief.render(forms_data(findings=[dict(rows[-1], answers=many)]))
    check_eq("gate_brief.render keeps every line of a long list under the cover sheet's cap", all(f"file{n}.py" in cover for n in range(30)), True)
    check_not_in("...with no truncation marker", "brief truncated", cover)


# --- FV1-9 N2: the card helps, the target says it was raised twice, the gate's top and the rehearsal leave a carded question alone ---

def help_question(**extra) -> dict:
    row = {"id": "Q1", "question": "What is the import limit?", "severity": "major", "owner_role": "dev_arch"}
    row.update(extra)
    return row


def readings_row(count: int = 2, **each) -> list:
    return [dict({"reading": f"reading {i + 1}"}, **each) for i in range(count)]


def test_fv19_card_help_fields() -> None:
    """D5: each help field H1..H7 present ALONE gives its line, absent gives none; T6 only when nothing helps (H5 only without H1)."""
    note = {"words": "The ticket says 100 in its description.", "by": "conductor", "at": "2026-11-14T10:20:30"}
    effects = {"Q1": {"a": [], "b": []}}
    field_lines = {
        "H1": ('the source says: "limit is 100"', help_question(source_says=[{"quote": "limit is 100", "where": "AC-2"}]), None),
        "H2": ("before the change: 100", help_question(before={"value": "100", "where": "code"}, now={"value": "1000", "where": "diff"}), None),
        "H3": ("if chosen: goes by 1", help_question(readings=readings_row(2, if_chosen="goes by 1")), None),
        "H4": ("what changes if you choose a:", help_question(readings=readings_row(2)), effects),
        "H5": ('the requirement it is about (R-8): "Imports over 100 files are refused"',
               help_question(requirement_help={"id": "R-8", "text": "Imports over 100 files are refused"}), None),
        "H6": ("what may help you answer, from the factory's helper, who read the sources for it (written 2026-11-14; "
               "it does not say which answer is right - you decide): The ticket says 100 in its description.",
               help_question(note=note), None),
        "H7": ("(from the ticket's description)", help_question(readings=readings_row(2, **{"from": "description"})), None),
    }
    sentinel = {"H1": "the source says", "H2": "before the change:", "H5": "the requirement it is about", "H6": "what may help you",
                "H7": "(from"}
    for name, (line, row, eff) in field_lines.items():
        lines = [l.strip() for l in gate_brief.question_card(row, 1, eff)]
        check(f"fv19_card_help_fields {name}: present alone, its line is on the card", any(line in l for l in lines))
        for other, marker in sentinel.items():
            if other != name:
                check(f"fv19_card_help_fields {name}: the line of {other} is not printed beside it", not any(marker in l for l in lines))
        check(f"fv19_card_help_fields {name}: never a `?` origin", not any("(from ?)" in l for l in lines))
    bare = gate_brief.question_card(help_question(), 1)
    for name, marker in sentinel.items():
        check(f"fv19_card_help_fields {name}: absent gives no line (no heading over nothing)", not any(marker in l for l in bare))
    both = gate_brief.question_card(help_question(source_says=[{"quote": "limit is 100", "where": "AC-2"}],
                                                 requirement_help={"id": "R-8", "text": "Imports over 100 files are refused"}), 1)
    check("fv19_card_help_fields H5: suppressed when the card has a source quote", not any("the requirement it is about" in l for l in both))
    blank_quote = gate_brief.question_card(help_question(source_says=[{"quote": "  ", "where": "AC-2"}],
                                                        requirement_help={"id": "R-8", "text": "Imports over 100 files are refused"}), 1)
    check("fv19_card_help_fields H5: a blank quote is no H1 - the requirement text is printed",
          any("the requirement it is about (R-8)" in l for l in blank_quote))
    undated = gate_brief.question_card(help_question(note={"words": "Words only.", "by": "conductor", "at": ""}), 1)
    check_in("fv19_card_help_fields H6: a note with no usable date has no `written` clause",
             "  - what may help you answer, from the factory's helper, who read the sources for it "
             "(it does not say which answer is right - you decide): Words only.", undated)
    cuts = []
    for n in (240, 241):
        card = gate_brief.question_card(help_question(requirement_help={"id": "R-8", "text": "r" * n}), 1)
        cuts.append(len(next(l for l in card if "(R-8)" in l).split('"')[1]))
    check_eq("fv19_card_help_fields H5: the requirement text is cut at 240 characters (AT 240 whole, BEYOND 240 plus the three dots)", cuts, [240, 243])
    ends = [next(l for l in gate_brief.question_card(help_question(requirement_help={"id": "R-8", "text": "r" * n}), 1) if "(R-8)" in l)
            for n in (240, 241)]
    check_eq("fv19_card_help_fields H5: AT 240 no `...`, BEYOND 240 `...` inside the quote (the same cut rule as T3)",
             ['..."' in ends[0], '..."' in ends[1]], [False, True])


def test_fv19_card_no_help_line() -> None:
    """D5, FR-41: nothing helps (no H1, H2, H5, H6 and no reading with a known origin) -> T6 and no `?`; one known origin is help enough."""
    t6 = ("  - where these readings come from is not recorded, and the factory has found nothing more than what is shown here; "
          "answer from what you know of the product, or in your own words.")
    t6_bare = ("  - the factory has found nothing more than what is shown here; answer from what you know of the product, "
               "or in your own words.")
    for label, row, expected in (("a bare question (F1: no readings, so no readings clause)", help_question(), t6_bare),
                                 ("readings with a blank origin", help_question(readings=readings_row(2, **{"from": ""})), t6),
                                 ("readings with no origin key", help_question(readings=readings_row(2)), t6)):
        lines = gate_brief.question_card(row, 1)
        check_in(f"fv19_card_no_help_line {label}: T6 is printed", expected, lines)
        check_eq(f"fv19_card_no_help_line {label}: `these readings` only where there are readings",
                 any("these readings" in l for l in lines), bool(row.get("readings")))
        check(f"fv19_card_no_help_line {label}: no `(from ?)`", not any("(from ?)" in l for l in lines))
        check_eq(f"fv19_card_no_help_line {label}: the answer line stays last", lines[-1].startswith("  - Answer: "), True)
        check_eq(f"fv19_card_no_help_line {label}: T6 is before the answer line", lines.index(expected) < len(lines) - 1, True)
    spec = gate_brief.question_card(help_question(readings=readings_row(2, **{"from": "spec"})), 1)
    check_eq("fv19_card_no_help_line (F1, FR-10): a reading whose origin the data file does not know is printed `(from: spec)` and T6 "
             "does not say the origin is unrecorded", (any("(from: spec)" in l for l in spec), any("not recorded" in l for l in spec)), (True, False))
    bare_lines = gate_brief.question_card(help_question(), 1)
    check_eq("fv19_card_no_help_line: a bare card has no `?` but the question's own",
             [l for l in bare_lines if "?" in l], ["- **Q1** [major, owner dev_arch] What is the import limit?"])
    known = gate_brief.question_card(help_question(readings=readings_row(2, **{"from": "code"})), 1)
    check_not_in("fv19_card_no_help_line: one reading with a known origin word is help - no T6", t6, known)
    many = gate_brief.question_card(help_question(readings=readings_row(27, **{"from": ""})), 1)
    check_in("fv19_card_no_help_line: the unlettered branch (27 readings) says it too", t6, many)
    check_eq("fv19_card_no_help_line: and prints no `(from ?)`", [l for l in many if "(from ?)" in l], [])


def test_fv19_origin_words_on_card() -> None:
    """T7: every word of `contract.READING_ORIGINS` is printed as the data file's words; an unknown word plainly; a detail kept; blank: nothing."""
    words = QR.vocabulary()["reading_origin_words"]
    for origin in contract.READING_ORIGINS:
        lines = gate_brief.question_card(help_question(readings=readings_row(1, **{"from": origin})), 1)
        check_in(f"fv19_origin_words_on_card {origin}: printed as the person's words", f"  - a) reading 1 (from {words[origin]})", lines)
    unknown = gate_brief.question_card(help_question(readings=readings_row(1, **{"from": "x"})), 1)
    check_in("fv19_origin_words_on_card: an unknown word is printed plainly as `(from: x)`", "  - a) reading 1 (from: x)", unknown)
    detail = gate_brief.question_card(help_question(readings=readings_row(1, **{"from": "comment:Alice"})), 1)
    check_in("fv19_origin_words_on_card: a known word with a detail keeps the detail", "  - a) reading 1 (from a comment on the ticket: Alice)", detail)
    blank = gate_brief.question_card(help_question(readings=readings_row(1, **{"from": "   "})), 1)
    check_in("fv19_origin_words_on_card: a blank origin has no parenthetical", "  - a) reading 1", blank)


def test_fv19_target_card_says_also_raised() -> None:
    """T2 on the target's card and nothing else: the hidden twin has no card, no twin text, no split door (owner 14.11)."""
    task_root = gate_story("qa-fv19-target-", [question("Q7"), question("Q16")])
    try:
        QR.declare_repeat(task_root, "Q16", "Q7", "both ask the limit", by="driver", declared_by="qa-case-designer", stage="S4")
        text = packet(task_root)
        card = card_of(text, "Q7")
        check_in("fv19_target_card_says_also_raised: the target's card says it was raised twice and the answer covers both",
                 "  - this question was raised twice in this story; it is asked once, here, and your answer is the answer to both.", card)
        check_not_in("fv19_target_card_says_also_raised: the hidden twin has no card", "- **Q16**", text)
        check_not_in("fv19_target_card_says_also_raised: no twin text and no id of it on the target's card", "Q16", card)
        for door in ("split", "separately", "ask again", "not the same"):
            check_not_in(f"fv19_target_card_says_also_raised: no split door ({door})", door, card.lower())
        check_eq("fv19_target_card_says_also_raised: a card with no repeat carries no such line",
                 [l for l in gate_brief.question_card(question("Q8"), 1) if "raised twice" in l], [])
    finally:
        drop(task_root)


def test_fv19_card_says_asked_again() -> None:
    """T3: a reworded open question says it is the same question, shows what it read before (cut at 240, `...` when cut) and the changed readings."""
    def reworded(was: str, was_readings=None, status="open") -> list:
        entry = {"at": "2026-11-14T09:00:00", "by": "conductor", "role": "conductor", "stage": "S4", "why": "w", "was": was}
        if was_readings is not None:
            entry["was_readings"] = was_readings
        return gate_brief.question_card(question("Q1", 2, reworded=[entry], status=status), 1)
    lead = "  - asked again in clearer words: this is the same question as before, which had no answer yet. Earlier it read: "
    check_in("fv19_card_says_asked_again: AT 240 characters the earlier wording is whole, no `...`",
             lead + '"' + "w" * 240 + '"', reworded("w" * 240))
    check_in("fv19_card_says_asked_again: BEYOND 240 it is cut and says so with `...`",
             lead + '"' + "w" * 240 + '..."', reworded("w" * 241))
    check_in("fv19_card_says_asked_again: whitespace is squeezed", lead + '"the old words"', reworded("  the   old\nwords "))
    changed = reworded("old", ["old a", "reading 2 of Q1"])
    check_in("fv19_card_says_asked_again: a changed reading gets one line with its letter", '    earlier, reading a read: "old a"', changed)
    check_eq("fv19_card_says_asked_again: an unchanged reading gets none", [l for l in changed if "earlier, reading b" in l], [])
    check_in("fv19_card_says_asked_again: an earlier reading is cut at 200",
             '    earlier, reading a read: "' + "x" * 200 + '"', reworded("old", ["x" * 201, "reading 2 of Q1"]))
    check_eq("fv19_card_says_asked_again: no was_readings, no reading lines", [l for l in reworded("old") if "earlier, reading" in l], [])
    check_eq("fv19_card_says_asked_again: a settled status is not an asked-again card",
             [l for l in reworded("old", status="answered") if "asked again in clearer words" in l], [])
    check_eq("fv19_card_says_asked_again: an old row with no `reworded` key has no line",
             [l for l in gate_brief.question_card(question("Q1"), 1) if "clearer words" in l], [])
    check_eq("fv19_card_says_asked_again: a `reworded` that is not a list is no line, never a crash",
             [l for l in gate_brief.question_card(question("Q1", 2, reworded="oops"), 1) if "clearer words" in l], [])


def test_fv19_note_on_card() -> None:
    """T4: the helper's note shows on the gate A card with its date and the "you decide" clause, only on the bytes it was written for."""
    task_root = gate_story("qa-fv19-note-", [question("Q1", 2)])
    try:
        rec = QR.record_note(task_root, "Q1", "The ticket says 100 in its description.", by="conductor", where="stage ran")
        card = card_of(packet(task_root), "Q1")
        check_in("fv19_note_on_card: date, helper, the clause that it does not pick an answer, and the words",
                 "  - what may help you answer, from the factory's helper, who read the sources for it (written "
                 + rec["at"][:10] + "; it does not say which answer is right - you decide): The ticket says 100 in its description.", card)
        check_eq("fv19_note_on_card: a note is help - no T6", "where these readings come from is not recorded" in card, False)
        (task_root / "work" / "requirements-readiness.json").write_text(
            json.dumps({"verdict": "ready", "open_questions": [question("Q1", 2, question="Other words?")]}), encoding="utf-8")
        check_not_in("fv19_note_on_card: a note measured on other bytes is not shown", "what may help you answer", card_of(packet(task_root), "Q1"))
    finally:
        drop(task_root)


def test_fv19_repeat_shown_again_note() -> None:
    """T14: a repeat that does not stand is asked, with the reason as its status note (card line), per `repeat_problem`."""
    base = {"status": "repeat", "same_as": "Q7", "follows": "", "changed_since_answer": False}
    for label, extra, expected in (
            ("gone", {"repeat_problem": "gone"}, "it was marked as the same question as Q7, which the factory no longer has, so it is asked here"),
            ("cycle", {"repeat_problem": "cycle"}, "it was marked as the same question as another one that points back to it, so it is asked here"),
            ("target_changed", {"repeat_problem": "target_changed"}, "it was marked as the same question as Q7, whose words have changed since, so it is asked here"),
            ("its own words changed", {"repeat_problem": "", "changed_since_answer": True},
             "it was marked as the same question as Q7, but its own words have changed since, so it is asked here")):
        check_eq(f"fv19_repeat_shown_again_note {label}: the note", gate_brief.question_note(dict(base, **extra)), expected)
    check_eq("fv19_repeat_shown_again_note: a repeat that stands has no note",
             gate_brief.question_note(dict(base, follows="Q7", repeat_problem="")), "")
    task_root = gate_story("qa-fv19-again-", [question("Q7"), question("Q16")])
    try:
        QR.declare_repeat(task_root, "Q16", "Q7", "both ask the limit", by="driver", declared_by="qa-case-designer", stage="S4")
        (task_root / "work" / "requirements-readiness.json").write_text(
            json.dumps({"verdict": "ready", "open_questions": [question("Q7", question="New words for Q7?"), question("Q16")]}), encoding="utf-8")
        text = packet(task_root)
        check_in("fv19_repeat_shown_again_note: the target changed -> the twin has its own card with the reason",
                 "it was marked as the same question as Q7, whose words have changed since, so it is asked here.", card_of(text, "Q16"))
        check_not_in("fv19_repeat_shown_again_note: and the target's card does not claim a twin that is shown", "raised twice", card_of(text, "Q7"))
    finally:
        drop(task_root)


def test_fv19_still_open_skips_hidden_repeat() -> None:
    """P2: a hidden repeat is not listed and copies `repeated_by` onto its target; a row with no register match is listed."""
    rows = [question("Q7"), question("Q16"), {"question": "no id here", "severity": "minor", "owner_role": "po_ba"}]
    task_root = gate_story("qa-fv19-still-", rows)
    try:
        QR.declare_repeat(task_root, "Q16", "Q7", "both ask the limit", by="driver", declared_by="qa-case-designer", stage="S4")
        got = gate_brief.unanswered_questions(task_root)
        check_eq("fv19_still_open_skips_hidden_repeat: the hidden twin is not listed, the unmatched row is",
                 [q.get("id") for q in got], ["Q7", None])
        check_eq("fv19_still_open_skips_hidden_repeat: the target carries the twin's id", got[0].get("repeated_by"), ["Q16"])
        check_eq("fv19_still_open_skips_hidden_repeat: an unmatched row carries none", "repeated_by" in got[1], False)
        QR.record(task_root, "Q7", "answered", "Q7: a", "gate A", "person", QR.load(task_root)["questions"][0]["row_hash"], reading="a")
        check_eq("fv19_still_open_skips_hidden_repeat: a target the person answered is not listed and its hidden twin stays out",
                 [q.get("id") for q in gate_brief.unanswered_questions(task_root)], [None])
    finally:
        drop(task_root)


def test_fv19_stop_and_gate_cards_print_the_same_help() -> None:
    """H5 on both cards: one question through gate A's list and the question stop prints the same requirement line (one reader); the
    absent-register and no-requirement-id rows add no line and never raise."""
    line_of = lambda lines: [l for l in lines if "the requirement it is about" in l]
    for label, extra, register, expected in (
            ("`requirement` names an R id", {"requirement": "R-4"}, True, ['  - the requirement it is about (R-4): "A removed node is shown at its former position" — work/requirements-register.md']),
            ("`raised_for.requirement`", {"raised_for": {"requirement": "R-3"}}, True, ['  - the requirement it is about (R-3): "A restored node keeps its identity" — work/requirements-register.md']),
            ("an id the register lacks", {"requirement": "R-99"}, True, []),
            ("no requirement id", {}, True, []),
            ("the register is absent", {"requirement": "R-4"}, False, [])):
        task_root = gate_story("qa-fv19-h5-", [question("Q1", 2, **extra)], with_register_md=register)
        try:
            gate_card = gate_brief.question_card(gate_brief.unanswered_questions(task_root)[0], 1)
            stop_card = QS.open_cards(task_root)
            check_eq(f"fv19_stop_gate_help {label}: gate A card help lines", line_of(gate_card), expected)
            check_eq(f"fv19_stop_gate_help {label}: the stop's card prints the same help lines", line_of(stop_card), line_of(gate_card))
        finally:
            drop(task_root)


class TopStub:
    """What `DriverGates.unrepaired_text` and `conductor_text` read of a driver: the task id and the case critic's findings file."""
    task = "T-1"
    task_root = Path(".")

    def s4_findings(self):
        return None


def test_fv19_gate_top_skips_carded_question() -> None:
    """P6: an `open_questions` finding tagged `on_card` True is not at the gate's top; False, an old finding without the tag and
    every other check are; the header is unchanged; nothing left prints no block."""
    import driver_gates
    unrepaired = driver_gates.DriverGates.unrepaired_text

    def finding(**extra):
        return dict({"check": "open_questions", "class": "factory_fixable", "message": "Q1 cannot be answered as it stands (x)", "fix": "f"}, **extra)
    other = {"check": "gate_decision", "class": "factory_fixable", "message": "the gate decision is open", "fix": "f"}
    header = "## What the factory could not repair before asking you"
    cases = (("on_card True", [finding(on_card=True, question="Q1"), other], False),
             ("on_card False", [finding(on_card=False, question="Q1"), other], True),
             ("an old finding with no keys", [finding(), other], True),
             ("on_card as the text `true` is not True", [finding(on_card="true"), other], True))
    for label, fixable, printed in cases:
        text = unrepaired(TopStub(), "A", fixable)
        check_eq(f"fv19_gate_top_skips_carded_question {label}: the question line is {'printed' if printed else 'left out'}",
                 "Q1 cannot be answered" in text, printed)
        check_in(f"fv19_gate_top_skips_carded_question {label}: the other finding stays", "- the gate decision is open", text)
        check_in(f"fv19_gate_top_skips_carded_question {label}: the header is unchanged",
                 header + "\n\nThese are the factory's own to repair, not questions for you:", text)
    check_eq("fv19_gate_top_skips_carded_question: only carded findings -> no block at all, never a heading over nothing",
             unrepaired(TopStub(), "A", [finding(on_card=True, question="Q1")]), "")
    same = unrepaired(TopStub(), "A", [finding(on_card=True), finding(on_card=True, message="Q2 cannot be answered as it stands (y)"), other])
    check_eq("fv19_gate_top_skips_carded_question: every carded finding goes, not the first only", "cannot be answered" in same, False)


def test_fv19_rehearsal_skips_hidden_repeat() -> None:
    """P8: the rehearsal raises no finding for a hidden repeat; the others carry `question` and `on_card`."""
    bare = [{"id": "Q7", "severity": "major", "owner_role": "po_ba", "question": "Where must a removed node appear?"},
            {"id": "Q16", "severity": "major", "owner_role": "po_ba", "question": "Where does a removed node go?"},
            {"id": "Q20", "severity": "major", "owner_role": "po_ba", "question": "A third bare one?"}]
    base = story("qa-fv19-rehearse-", questions=bare)
    task_root = base / "artifacts" / "TP1-15045"
    try:
        before = gate_preflight.Rehearsal(task_root, "A")
        before.check_open_questions()
        check_eq("fv19_rehearsal_skips_hidden_repeat control: with no repeat every bare question is a finding",
                 [f["question"] for f in before.findings], ["Q7", "Q16", "Q20"])
        QR.declare_repeat(task_root, "Q16", "Q7", "both ask where", by="driver", declared_by="qa-case-designer", stage="S4")
        rehearsal = gate_preflight.Rehearsal(task_root, "A")
        rehearsal.check_open_questions()
        check_eq("fv19_rehearsal_skips_hidden_repeat: the hidden twin has no finding",
                 [f["question"] for f in rehearsal.findings], ["Q7", "Q20"])
        check_eq("fv19_rehearsal_skips_hidden_repeat: `on_card` is True for a question the person is shown",
                 [f["on_card"] for f in rehearsal.findings], [True, True])
        check_in("fv19_rehearsal_skips_hidden_repeat: and the finding text is as before",
                 "Q7 cannot be answered as it stands", rehearsal.findings[0]["message"])
        QR.record(task_root, "Q20", "with_designer", "with the designer", "stage ran", "driver", QR.load(task_root)["questions"][2]["row_hash"])
        owned = gate_preflight.Rehearsal(task_root, "A")
        owned.check_open_questions()
        check_eq("fv19_rehearsal_skips_hidden_repeat (F2): a `with_designer` row IS in gate A's list (`still_open`), so `on_card` is True",
                 {f["question"]: f["on_card"] for f in owned.findings}, {"Q7": True, "Q20": True})
    finally:
        cleanup(base.parent)


def test_fv19_conductor_text_note_door() -> None:
    """P7: T10 only with an `open_questions` finding among `rest`; the closing paragraph stays last."""
    import driver_gates
    conductor_text = driver_gates.DriverGates.conductor_text
    finding = {"check": "open_questions", "id": "open_questions-1", "message": "Q1 cannot be answered as it stands (x)", "fix": "back to S2"}
    other = {"check": "gate_decision", "id": "gate_decision-1", "message": "the gate decision is open", "fix": "f"}
    t10 = ("For each `open_questions` finding above: when `controller.py --operation rework --stage S2 --role qa-requirements-tester` is "
           "refused by the repair cap, do not try again. Read the sources and write what helps the person answer that question - where each "
           "reading comes from, the source line, what each answer changes, an answered question it rests on - with `question_register.py "
           "--task T-1 --note <id> --words-file <file> --by conductor --where \"stage ran\"`. Do not say which reading is right: the "
           "person decides. Do not rewrite the question; its card shows your note.")
    with_it = conductor_text(TopStub(), "A", "the cap", [finding, other], "a rework")
    check_in("fv19_conductor_text_note_door: with an open_questions finding T10 is present, word for word", t10, with_it)
    class NoTask(TopStub):
        task = ""
    check_in("fv19_conductor_text_note_door (F5): with no task id the placeholder `<T>` stays", "--task <T> --note <id>",
             conductor_text(NoTask(), "A", "the cap", [finding], ""))
    check_eq("fv19_conductor_text_note_door: T10 comes after the findings",
             with_it.index(t10) > with_it.index("the gate decision is open"), True)
    check_eq("fv19_conductor_text_note_door: the closing paragraph stays last",
             with_it.rindex("Repair what you can") > with_it.index(t10)
             and with_it.endswith("only for a finding that needs a decision of theirs."), True)
    without = conductor_text(TopStub(), "A", "the cap", [other], "")
    check_not_in("fv19_conductor_text_note_door: with no open_questions finding there is no T10", "--note <id>", without)
    check_eq("fv19_conductor_text_note_door: nothing else of the text changes", with_it.replace("\n\n" + t10, "").count("Repair what you can"), 1)


def card_problems(text: str) -> list:
    """`human_text.problems` of a card alone: the card is a block of the packet, whose how-to-answer block is the packet's own, so that
    one rule is not asked of a block."""
    return [p for p in human_text.problems(text) if p.get("rule") != "no_how_to_answer"]


def test_fv19_human_text_passes() -> None:
    """FR-6: the new card lines pass `human_text.problems` - a card with every new line, and the gate A packet that carries them."""
    task_root = gate_story("qa-fv19-human-", [question("Q7"), question("Q16")])
    try:
        QR.declare_repeat(task_root, "Q16", "Q7", "both ask the limit", by="driver", declared_by="qa-case-designer", stage="S4")
        QR.record_note(task_root, "Q7", "The ticket says 100 in its description.", by="conductor", where="stage ran")
        card = card_of(packet(task_root), "Q7")
        check_in("fv19_human_text_passes: the card under test carries T2", "raised twice", card)
        check_in("fv19_human_text_passes: and T4", "what may help you answer", card)
        check_eq("fv19_human_text_passes: that card has no human-text problem", card_problems(card), [])
    finally:
        drop(task_root)
    full = "\n".join(gate_brief.question_card(help_question(
        readings=readings_row(2, **{"from": "comment:Alice"}),
        requirement_help={"id": "R-8", "text": "Imports over 100 files are refused"}, repeated_by=["Q16"],
        reworded=[{"was": "old words", "was_readings": ["old a", "reading 2"]}],
        note={"words": "Helpful words.", "by": "conductor", "at": "2026-11-14T10:00:00"}), 1))
    check_eq("fv19_human_text_passes: a card with every new line has no human-text problem", card_problems(full), [])
    bare = "\n".join(gate_brief.question_card(help_question(), 1))
    check_eq("fv19_human_text_passes: nor the card with T6", card_problems(bare), [])
    repeat_note = "\n".join(gate_brief.question_card(help_question(status_note=gate_brief.question_note(
        {"status": "repeat", "same_as": "Q7", "repeat_problem": "gone", "follows": ""})), 1))
    check_eq("fv19_human_text_passes: nor a card with T14", card_problems(repeat_note), [])


def test_fv19_card_old_row_without_keys() -> None:
    """TEMPORAL: a row with none of the new keys renders as before - no KeyError, no empty help line, no line over nothing."""
    row = question("Q1")
    lines = gate_brief.question_card(row, 1)
    check_eq("fv19 temporal: no empty or whitespace-only line", [l for l in lines if not l.strip()], [])
    check_eq("fv19 temporal: no line mentions a twin, a note or an earlier wording",
             [l for l in lines if any(w in l for w in ("raised twice", "helper", "clearer words", "requirement it is about"))], [])
    for odd in ({"note": "text"}, {"note": None}, {"note": {"words": "  "}}, {"repeated_by": []}, {"reworded": []},
                {"requirement_help": "x"}, {"requirement_help": {"id": "R-1", "text": ""}}):
        check_eq(f"fv19 temporal: a malformed value {odd} is no line and no crash", gate_brief.question_card(dict(row, **odd), 1), lines)


if __name__ == "__main__":
    test_the_test_repository_question_offers_its_words_with_prices()
    test_the_words_are_offered_only_where_they_can_be_carried_out()
    test_the_blockers_name_what_the_words_cannot_take()
    test_the_shown_doors_have_one_writer_and_one_reader()
    test_the_answers_are_printed_whole_on_both_roads()
    test_answer_forms_are_one_list_and_each_has_its_reader()
    test_answer_forms_edges()
    test_answer_line_and_the_helper_sentence()
    test_a_before_now_question_shows_both_and_asks_the_fixed_pair()
    test_readings_are_built_from_the_matrix()
    test_a_bare_question_is_the_factorys_to_rewrite()
    test_a_bare_question_still_reaches_the_person()
    test_a_card_shows_what_each_answer_changes()
    test_the_star_patch_a_letter_override_and_not_needed()
    test_a_story_from_before_the_fields_reads_as_it_did()
    test_what_cannot_be_read_is_named_not_raised()
    test_a_register_row_without_ac_ref_is_signed_by_its_source()
    test_a_row_that_names_its_register_question_is_not_asked_twice()
    test_no_question_and_no_reading_is_cut()
    test_the_decision_text_holds_the_words_where_they_are_stored()
    test_question_status_comes_from_the_register()
    test_a_register_that_cannot_be_read_is_said_and_never_read_as_answered()
    test_an_empty_register_and_a_question_with_no_readings()
    test_fv19_card_help_fields()
    test_fv19_card_no_help_line()
    test_fv19_origin_words_on_card()
    test_fv19_target_card_says_also_raised()
    test_fv19_card_says_asked_again()
    test_fv19_note_on_card()
    test_fv19_repeat_shown_again_note()
    test_fv19_still_open_skips_hidden_repeat()
    test_fv19_stop_and_gate_cards_print_the_same_help()
    test_fv19_gate_top_skips_carded_question()
    test_fv19_rehearsal_skips_hidden_repeat()
    test_fv19_conductor_text_note_door()
    test_fv19_human_text_passes()
    test_fv19_card_old_row_without_keys()
    finish("gate question form")
