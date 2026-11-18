#!/usr/bin/env python3
"""sites: a part of test_no_move_seam.py, split by tools/test_split.py (TD-11c). The shared helpers are in no_move_seam_common."""
import contextlib
import io
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from harness import check, check_eq, check_in, check_not_in  # noqa: E402
from story_run_common import driver_for, seed  # noqa: E402
import human_text  # noqa: E402
import no_move as NM  # noqa: E402
import story_run  # noqa: E402
from no_move_seam_common import (  # noqa: E402
    SITE_Q, _site_ok, answer, logged_rig, raised, rig, seam_asked, take, verdict,
)


def site_state(driver, *, doors=("read",), **extra):
    """The state a CLOSED question's site hands the seam (C1-3): its own words as `site_doors`, its own question as `site_fallback`."""
    again = lambda lead: story_run.Person("halt", lead + "\n\nthe site's own question", "S0")
    return dict({"why": "unread_answer", "kind": "halt", "stage": "S0", "dispatch": "", "text": "the factory's words", "words": "w",
                 "lead": "LEAD: nothing has moved yet.", "site_doors": tuple(doors), "site_fallback": again}, **extra)


def n16_site_doors() -> None:
    normalize = story_run.Driver.s0_normalize
    spec, words = NM.data(), {"no": {"head": "Verdict: not ready to ship as is."}}
    open_ids = ["person_does", "stop_here", "go_on_as_is", "release_and_restart", "stand_prepare"]
    site_verdict = verdict((("read", NM.SITE_DOOR), ("stop", "stop_here")), question=SITE_Q)
    ok, rule = NM.validate_options(site_verdict, open_ids, spec, normalize, words, ("read",))
    check("N16: a door of the site is valid as a `site_door`", ok is not None and rule == "", rule)
    options, rule = NM.validate_options(site_verdict, open_ids, spec, normalize, words, ("skip",))
    check("N16: a door NOT in the site is invalid", options is None and "does not read" in rule, rule)
    options, rule = NM.validate_options(site_verdict, open_ids, spec, normalize, words, ())
    check("N16: an empty site rejects every `site_door`", options is None and rule, rule)
    options, rule = NM.validate_options(site_verdict, open_ids, spec, normalize, words)
    check("N16: and so does a call that passes no site at all (today's callers)", options is None and rule, rule)
    for token in sorted(NM.reserved_tokens(spec, normalize)):                # all five tokens of `moves` (restart, prepare the stand ...) + stop
        two = verdict(((token, NM.SITE_DOOR), ("read", NM.SITE_DOOR)), question=f"Which? `{token}` or `read`?")
        options, rule = NM.validate_options(two, open_ids, spec, normalize, words, (token, "read"))
        check(f"N16 G7: `{token}` offered as a `site_door` is invalid even when the site names it (it is a move's own word)",
              options is None and "move's own word" in rule, rule)
    check_eq("N16 G7: the reserved words are the seven tokens of `moves` (C1-4b added `rework` and `approve`) and the standing three",
             sorted(NM.reserved_tokens(spec, normalize)),
             ["approve", "go on", "prepare the stand", "restart", "retry", "rework", "stop"])
    for name in ("Stop", "retry", " Go On ", "restart", "Prepare the stand"):
        try:
            NM.site_check((name,), spec, normalize)
            shown = False
        except NM.DataUnreadable as exc:
            shown = normalize(name) in str(exc)
        check(f"N16 G7: a site door `{name.strip()}` is DataUnreadable and the error names it", shown)
    check_eq("N16: a plain stand name is a door, normalized", NM.site_check(("Local", "new text"), spec, normalize), ["local", "new text"])
    # through the seam: the conductor offers a site word as `site_door` and it becomes the option
    root, task_root, driver = rig(answers=[site_verdict])
    try:
        driver.boundary = "S0:x"
        _, person = raised(driver, site_state(driver), ["stop_here"])
        check_eq("N16: the seam question carries the site's word and `stop`", (list(person.offered), person.kind), (["read", "stop"], "halt"))
        check_in("N16: the conductor was told what the question already takes", "## Answers this question already takes", driver.calls[0]["text"])
        check_in("N16: ... naming `read`", "`read`", driver.calls[0]["text"].split("## Answers this question already takes")[1])
        check_in("N16: and the site's lead goes first", "LEAD: nothing has moved yet.", driver.calls[0]["text"].split("## Moves open here")[0])
    finally:
        harness.cleanup(root)
    # a stand named `Stop`: the site cannot name it as a door; the seam falls back to the SITE's question, ONE defect, no conductor call
    root, task_root, driver = rig()
    try:
        driver.boundary = "S0:x"
        _, person = raised(driver, site_state(driver, doors=("Stop", "local")), ["stop_here"])
        check_eq("N16 G7: a reserved site door -> the site's own question, no conductor call, one defect naming it",
                 (person.text.endswith("the site's own question"), len(driver.calls), len(driver.defects), "stop" in " ".join(driver.defects[0])),
                 (True, 0, 1, True))
    finally:
        harness.cleanup(root)


def n17_site_fallback() -> None:
    """G2: with `site_fallback` EVERY exit of the seam without a usable conductor answer raises the SITE's question; the recursion floor
    is the generic three, once. G8: ONE `defect_found` per failure."""
    unusable = [{"action": "_unreadable", "did": "", "question": ""}]
    cases = (("an unreadable conductor answer", unusable, {}, None),
             ("a verdict that breaks the options rule", [verdict((("retry", "person_does"), ("retry", "person_does")), question="What? `retry`?")], {}, None),
             ("the cap", [], {}, "cap"))
    for label, answers, extra, special in cases:
        root, task_root, driver = rig(answers=answers)
        try:
            driver.boundary = "S0:x"
            if special == "cap":
                driver.conductor_calls[driver.boundary] = story_run.CONDUCTOR_CALLS_PER_BOUNDARY
            _, person = raised(driver, site_state(driver, **extra), ["person_does", "stop_here"])
            # t-1936 F2: refused options with a conductor question put that question (verbatim) between the lead and the site's question
            found = "What the conductor found:\nWhat? `retry`?\n\n" if label == "a verdict that breaks the options rule" else ""
            check_eq(f"N17 {label}: the SITE's question with the lead above it, never the generic three",
                     (person.text, list(person.offered)), (f"LEAD: nothing has moved yet.\n\n{found}the site's own question", []))
            check_eq(f"N17 {label}: exactly one defect_found", len(driver.defects), 1)
            check_eq(f"N17 {label}: exit 3 (EXIT_PERSON): a conductor `stop` is the only road to 4", person.code, story_run.EXIT_PERSON)
        finally:
            harness.cleanup(root)
    # D-0041: a rerun with NO words is the no-call road (`call: False`): the site's question again, no conductor call, no defect
    root, task_root, driver = rig()
    try:
        driver.boundary = "S0:x"
        _, person = raised(driver, site_state(driver, call=False, words=""), None)
        check_eq("N17 D-0041: a rerun with no `--answer` -> no call, the same site question, no defect",
                 (len(driver.calls), person.text.endswith("the site's own question"), len(driver.defects)), (0, True, 0))
        # ... and every `--answer` is new words: the conductor is called once EACH time, on an identical finding set
        driver.conductor_calls.clear()
        for words in ("first words", "first words"):
            driver.calls.clear()
            raised(driver, site_state(driver, words=words), None)
            check_eq(f"N17 D-0041: an unread answer `{words}` is exactly ONE conductor call", len(driver.calls), 1)
    finally:
        harness.cleanup(root)
    # a conductor `stop` with no usable options: the site's question, exit 4 (the only road to it)
    root, task_root, driver = rig(answers=[{"action": "stop", "did": "gave up", "question": "no"}])
    try:
        driver.boundary = "S0:x"
        _, person = raised(driver, site_state(driver), None)
        check_eq("N17: a conductor `stop` that carries no options: the site question, exit 4", (person.text.endswith("the site's own question"), person.code),
                 (True, story_run.EXIT_GAVE_UP))
    finally:
        harness.cleanup(root)
    # LabelsUnreadable: the site's question WITHOUT prices, ONE defect that carries the price reason too (G8)
    real = human_text.rules()
    short = dict(real, price_lines={"labels": real["price_lines"]["labels"][:1]})
    root, task_root, driver = rig(answers=unusable)
    try:
        driver.boundary = "S0:x"
        opts = [{"answer": "retry", "token": "retry", "says": "look again"}, {"answer": "stop", "token": "stop", "says": "stop here"}]
        state = site_state(driver)
        state["site_fallback"] = lambda lead: story_run.Person("halt", driver.closed_question("s0.ticket_auth", lead, opts), "S0")
        human_text.rules = lambda: short
        try:
            _, person = raised(driver, state, ["person_does", "stop_here"])
        finally:
            human_text.rules = real_rules
        check_not_in("N17 LabelsUnreadable: the site question is shown WITHOUT its price lines (a question is never withheld for them, FR-41)",
                     "the factory:", person.text)
        check_in("N17 LabelsUnreadable: ... but with its options and the lead", "`retry`", person.text)
        check_eq("N17 LabelsUnreadable: ONE defect_found for the failure", len(driver.defects), 1)
        check_in("N17 LabelsUnreadable (G8): and its note carries the price reason as well", "prices of the question `s0.ticket_auth` could not be read", " ".join(driver.defects[0]))
        driver.boundary = "S0:x"
    finally:
        human_text.rules = real_rules
        harness.cleanup(root)
    # the recursion floor: a site that cannot rebuild its question (or returns no Person) -> the generic three, ONCE, ONE defect
    for label, builder in (("raises", lambda lead: (_ for _ in ()).throw(ValueError("broken"))), ("returns a string", lambda lead: "not a person")):
        root, task_root, driver = rig(answers=unusable)
        try:
            driver.boundary = "S0:x"
            _, person = raised(driver, site_state(driver, site_fallback=builder), ["person_does", "stop_here"])
            check_eq(f"N17 floor ({label}): the generic retry / go on / stop, once", list(person.offered), ["retry", "go on", "stop"])
            check_eq(f"N17 floor ({label}): the two failures are TWO defects (the answer, and the site's question), none more", len(driver.defects), 2)
        finally:
            harness.cleanup(root)
    # the re-entry guard and a Refusal while rendering both end in the site's question too
    root, task_root, driver = rig()
    try:
        driver.boundary = "S0:x"
        driver._in_no_move = True
        _, person = raised(driver, site_state(driver), None)
        driver._in_no_move = False
        check_eq("N17: re-entry renders the SITE's question (the recursion floor does not skip the site)",
                 (person.text.endswith("the site's own question"), len(driver.calls)), (True, 0))
        driver.no_move_facts = lambda state: (_ for _ in ()).throw(story_run.Refusal("rendering broke"))
        _, person = raised(driver, site_state(driver), None)
        check("N17: a Refusal raised while rendering: the site's question again", person.text.endswith("the site's own question"), person.text)
    finally:
        harness.cleanup(root)
    # a valid conductor verdict whose price labels cannot be read ends in the last resort: the site's question there as well
    root, task_root, driver = rig(answers=[verdict((("read", NM.SITE_DOOR), ("stop", "stop_here")), question=SITE_Q)])
    try:
        driver.boundary = "S0:x"
        human_text.rules = lambda: short
        try:
            _, person = raised(driver, site_state(driver), ["stop_here"])
        finally:
            human_text.rules = real_rules
        check("N17: unreadable labels after a valid verdict: the site's question, not the generic three",
              person.text.endswith("the site's own question") and list(person.offered) == [], person.text)
    finally:
        human_text.rules = real_rules
        harness.cleanup(root)
    # F-7 (critic t-689): the same road with a site that RENDERS PRICES - the last resort and the site's own rendering fail for ONE
    # cause (the labels), and that is ONE defect_found, carrying both the seam's rule and the price reason
    priced_opts = [{"answer": "retry", "token": "retry", "says": "look again"}, {"answer": "stop", "token": "stop", "says": "stop here"}]
    for label, answers, extra in (("a valid verdict, then unreadable labels", [verdict((("read", NM.SITE_DOOR), ("stop", "stop_here")), question=SITE_Q)], {}),
                                  ("a Refusal while rendering", [verdict((("read", NM.SITE_DOOR), ("stop", "stop_here")), question=SITE_Q)], {"refuse": True})):
        root, task_root, driver = rig(answers=answers)
        try:
            driver.boundary = "S0:x"
            state = site_state(driver)
            state["site_fallback"] = lambda lead: story_run.Person("halt", driver.closed_question("s0.ticket_auth", lead, priced_opts), "S0")
            if extra.get("refuse"):
                driver.no_move_facts = lambda state: (_ for _ in ()).throw(story_run.Refusal("rendering broke"))
            human_text.rules = lambda: short
            try:
                _, person = raised(driver, state, ["stop_here"])
            finally:
                human_text.rules = real_rules
            check_not_in(f"N17 F-7 ({label}): the priced site question is shown WITHOUT its price lines", "the factory:", person.text)
            check_eq(f"N17 F-7 ({label}): exactly ONE defect_found, not one per layer", len(driver.defects), 1)
            check_in(f"N17 F-7 ({label}): and its note carries the price reason as well", "prices of the question `s0.ticket_auth` could not be read",
                     " ".join(driver.defects[0]))
        finally:
            human_text.rules = real_rules
            harness.cleanup(root)


real_rules = human_text.rules


def n18_package_unread() -> None:
    """G1 at `package`: the RETURN after the seam is safe - nothing recorded, `package_question` kept, no pass, no waiver."""
    for what, own in (("hooks", "retry"), ("mode", "desktop")):
        pending = {"what": what, "text": "the package question", "details": "the copies differ", "stage": "S1", "driver_root": "a", "hook_roots": ["b"]}
        # a conductor `continue`: back to the caller, nothing passed
        root, task_root, driver = logged_rig(answers=[{"action": "continue", "did": "looked", "question": ""}])
        try:
            driver.state["package_question"] = dict(pending)
            driver.boundary = "S1:S1-x-1"
            seen = []
            real_py = driver.py
            driver.py = lambda script, *a, **k: (seen.append(script), real_py(script, *a, **k))[1]
            got = take_package(driver, "no idea what to do")
            check_eq(f"N18 {what}: a conductor `continue` returns (no Person); the question is kept; nothing passed or waived",
                     (got, "package_question" in driver.state, "package_pass" in driver.state, "waiver.py" in seen),
                     ("returned", True, False, False))
            check_eq(f"N18 {what}: the unread words are on the record (a human_answer), and no defect", (any("human_answer" in a for a in driver.logged), len(driver.defects)), (True, 0))
            check_eq(f"N18 {what}: ONE conductor call", len(driver.calls), 1)
        finally:
            harness.cleanup(root)
        # offered options are a subset of {own, go on, stop}
        root, task_root, driver = logged_rig(answers=[verdict(((own, "person_does" if own == "retry" else NM.SITE_DOOR), ("stop", "stop_here")),
                                                              question=f"Which? `{own}` or `stop`?")])
        try:
            driver.state["package_question"] = dict(pending)
            driver.boundary = "S1:S1-x-1"
            person = take_package(driver, "gibberish")
            ok = story_run.Person is type(person) or isinstance(person, story_run.Person)
            check(f"N18 {what}: a usable verdict raises the seam question, kind `package`, offered within {{{own}, go on, stop}}",
                  ok and person.kind == "package" and set(person.offered) <= {own, "go on", "stop"} and "package_question" in driver.state, repr(person))
        finally:
            harness.cleanup(root)
        # nothing usable: the site's question with the lead, never "I could not tell which answer yours was"
        root, task_root, driver = logged_rig(answers=[{"action": "_unreadable", "did": "", "question": ""}])
        try:
            driver.state["package_question"] = dict(pending)
            driver.boundary = "S1:S1-x-1"
            person = take_package(driver, "gibberish")
            check(f"N18 {what}: a fallback shows the package question again with the one lead, the old sentence gone",
                  isinstance(person, story_run.Person) and person.kind == "package" and "nothing has moved yet." in person.text
                  and person.text.rstrip().endswith("the package question") and "could not tell which" not in person.text, repr(person))
        finally:
            harness.cleanup(root)


def take_package(driver, words):
    """`take_package_answer`: 'returned' when it came back, else the Person the seam raised from inside it."""
    try:
        driver.take_package_answer(words, "# q\n", "S1", "S1-x-1")
        return "returned"
    except story_run.Person as person:
        return person


def n19_ticket_changed_unread() -> None:
    """G1 at `ticket_changed`: a conductor `continue` raises the question again from the files - never `--adopt`, never a decline."""
    again = lambda lead="": story_run.Person("ticket_changed", lead + "the changed-ticket question", "S0")
    for label, answers in (("continue", [{"action": "continue", "did": "x", "question": ""}]), ("unreadable", [{"action": "_unreadable", "did": "", "question": ""}]),
                           ("a word the question does not take", [verdict((("retry", "person_does"), ("stop", "stop_here")))])):
        root, task_root, driver = logged_rig(answers=answers)
        try:
            driver.boundary = "S0:ticket"
            driver.ticket_changed_from_files = again
            adapter = []
            driver.py_stdout = lambda *a, **k: (adapter.append(a), (0, "{}", ""))[1]
            try:
                driver.take_ticket_answer("I do not know", "# q\n", "S0", "")
                person = None
            except story_run.Person as raised_person:
                person = raised_person
            check(f"N19 {label}: the changed-ticket question comes back with the one lead, the question under it",
                  person is not None and person.kind == "ticket_changed" and "nothing has moved yet." in person.text
                  and person.text.endswith("the changed-ticket question"), repr(person))
            check_eq(f"N19 {label}: no adapter call at all (never `--adopt`, never `--decline`), ONE conductor call", (adapter, len(driver.calls)), ([], 1))
            check_eq(f"N19 {label}: the words are recorded first (a human_answer)", any("human_answer" in a for a in driver.logged), True)
        finally:
            harness.cleanup(root)


def n20_the_funnel_reads_new_words() -> None:
    """t-671 Q12 (P22 sibling): the funnel at the end of `run()` calls the conductor when the state carries an answer's words file."""
    base = {"why": "refusal", "kind": "conductor", "text": "t", "lead": "L"}
    for label, extra, calls in (("an answer's words file is set", {"words_file": "state/driver-answers/a.md", "words": "w"}, 1),
                                ("no words file (a refusal of the run itself)", {}, 0)):
        root, task_root, driver = rig(answers=[verdict()])
        try:
            driver.boundary = "S5:S5-x-1"
            printed = io.StringIO()
            with contextlib.redirect_stdout(printed):
                code = driver.funnel(dict(base, **extra))
            check_eq(f"N20 funnel, {label}: {calls} conductor call(s), a question (exit 3)", (len(driver.calls), code), (calls, story_run.EXIT_PERSON))
        finally:
            harness.cleanup(root)
    root, task_root, driver = rig(answers=[{"action": "continue", "did": "x", "question": ""}])
    try:
        driver.boundary = "S5:S5-x-1"
        with contextlib.redirect_stdout(io.StringIO()):
            code = driver.funnel(dict(base, words_file="state/driver-answers/a.md", words="w"))
        check_eq("N20 funnel: a conductor `continue` returns to the free question (exit 3), nothing lost", (len(driver.calls), code), (1, story_run.EXIT_PERSON))
    finally:
        harness.cleanup(root)


def n21_keep_at_the_stuck_threshold() -> None:
    """Q2 (G15): the stuck threshold (`where` said the same four times) passes `keep` = the stage's place, so the lead goes above the
    conductor's prose when the prose drops it; the refusal-cap site (`call: False`) passes none (`keep` is read only on the conductor's road)."""
    root, task_root, env = seed("QA-9")
    driver = driver_for(root, env, "QA-9", max_boundaries=50)
    try:
        seen = []

        def seam(state, moves=None):
            seen.append(state)
            raise story_run.Stop(story_run.EXIT_DONE, "end of test")
        driver.no_move = seam
        driver.where = lambda: {"action": "prepare_stage", "stage": "S5", "revision": 1}
        driver.boundary_step = lambda action: None
        with contextlib.redirect_stdout(io.StringIO()):
            driver.run()
        check_eq("N21: the fifth identical `where` reaches the seam once, as the stuck threshold", [s.get("why") for s in seen], ["threshold"])
        check_eq("N21: with `keep` = the stage's place, and the stuck text as the lead",
                 (seen[0].get("keep"), seen[0].get("lead") == driver.stuck_text("S5"), "call" in seen[0]), ([driver.stage_place("S5")], True, False))
    finally:
        harness.cleanup(root)
    # the generic lead-above-prose rule that `keep` feeds (the conductor's prose drops the place)
    place = "S5 / qa-automator"
    root, task_root, driver = rig(answers=[verdict(question="What should happen? `retry` once you have dealt with it, or `stop`.")])
    try:
        driver.boundary = "S5:x"
        _, person = raised(driver, {"why": "threshold", "kind": "refusal", "stage": "S5", "lead": f"The run is stuck at {place}.", "text": "sig",
                                    "keep": [place]})
        check("N21: a prose that drops the kept place gets the lead above it", person.text.startswith(f"The run is stuck at {place}."), person.text[:200])
    finally:
        harness.cleanup(root)


GATE_WORDS = b"the automation needs changes - the export test checks only the status code\r\nplease check the body too\r\n"


GATE_FOUR = (("rework", "rework_stage"), ("approve", "approve_gate"), ("retry", "person_does"), ("stop", "stop_here"))


def n22_the_gate_raised_again_over_an_open_seam_question() -> None:
    """H14 edge 11 (C1-4b): a relaunch without an answer while the gate's SEAM question is open. `await_gate` shows the gate packet again
    (`gate()` -> `ask()`), and `ask()` overwrites the open question: its `offered` / `options` / `words_file` are gone, so the next answer is
    read as an answer AT THE GATE (the approval word, the conductor for any other words), never as a token of the old options. The original
    answer's words survive in their file. Invariant: nothing is recorded for the person by the relaunch."""
    root, task_root, driver = logged_rig()
    try:
        rel = "state/words/driver-answer-original.txt"
        (task_root / rel).parent.mkdir(parents=True, exist_ok=True)
        (task_root / rel).write_bytes(GATE_WORDS)
        driver.gate_text = lambda gate: "the packet of gate B"
        seen = []
        driver.record_by_code = lambda kind, stage, words, again=False, approved_by="": seen.append((kind, stage, words, approved_by)) or True
        seam_asked(driver, GATE_FOUR, stage="S8", dispatch="", kind="gate_B", words_file=rel)
        check_eq("N22 control: the open question is the seam's, with its options and the original words' file",
                 (driver.state["asked"].get("offered"), driver.state["asked"].get("words_file")), (["rework", "approve", "retry", "stop"], rel))
        try:
            driver.gate("B")
            person = None
        except story_run.Person as raised_person:
            person = raised_person
        check("N22: the relaunch's gate is a Person of the gate's kind", person is not None and person.kind == "gate_B", str(person))
        with contextlib.redirect_stdout(io.StringIO()):
            driver.ask(person)
        asked = driver.state["asked"]
        check_eq("N22: ask() overwrote the question: the gate's own, with no `offered`, no `options`, no `words_file`",
                 (asked["kind"], any(key in asked for key in ("offered", "options", "words_file", "why"))), ("gate_B", False))
        check_eq("N22: the original words survive in the words file, byte for byte", (task_root / rel).read_bytes(), GATE_WORDS)
        check_eq("N22: and the relaunch recorded nothing and called no conductor", (seen, driver.calls), ([], []))
        check_eq("N22: the next answer is read AT THE GATE: the approval word is recorded by code as the word, not as the option's choice",
                 take(driver, answer(task_root, "g.md", b"approve\r\n")), None)
        check_eq("N22: one record, with the gate's words and no `approved_by`", seen, [("gate_B", "S8", "approve", "")])
    finally:
        harness.cleanup(root)


def n23_a_conductor_continue_at_a_gate_shows_the_gate_again() -> None:
    """H14 edge 12 (C1-4b): the conductor answers `continue` at a gate WITHOUT registering anything. The words were not an approval, so
    nothing is recorded or kept; the loop goes back, the gate is raised again and - its text being the same - carries the FR-7 block that
    says the person answered it before. Invariant: the run never stalls (a Person is raised, an exit code returned) and never records."""
    root, task_root, driver = logged_rig(answers=[{"action": "continue", "did": "looked, registered nothing"}])
    try:
        driver.gate_text = lambda gate: "the packet of gate B"
        seen, inner = [], driver.py          # the REAL recorder, its controller call spied: it records only an approval
        driver.py = lambda script, *a, **k: (seen.append(a), (0, "recorded"))[1] if script == "controller.py" else inner(script, *a, **k)

        def show():
            try:
                driver.gate("B")
            except story_run.Person as person:
                with contextlib.redirect_stdout(io.StringIO()):
                    return driver.ask(person)
        check_eq("N23 control: the first show asks (exit 3)", show(), story_run.EXIT_PERSON)
        check_not_in("N23 control: and carries no FR-7 block", "answered this exact question before", (driver.state_dir / "driver-question.md").read_text(encoding="utf-8"))
        check_eq("N23: the answer in the person's own words comes back (the conductor's `continue`)",
                 take(driver, answer(task_root, "g.md", b"the export test is wrong, fix it\r\n")), None)
        check_eq("N23: the conductor was called once, nothing was recorded and nothing is kept as an approval",
                 (len(driver.calls), seen, driver.state.get("gate_answer_kept"), driver.state.get("asked")), (1, [], None, {}))
        check_eq("N23: the loop shows the gate again: a question, an exit code - the run does not stall", show(), story_run.EXIT_PERSON)
        text = (driver.state_dir / "driver-question.md").read_text(encoding="utf-8")
        check_in("N23: and the identical packet says it was answered before (FR-7)", "You have answered this exact question before", text)
        check_in("N23: with the person's words", "the export test is wrong, fix it", text)
    finally:
        harness.cleanup(root)


OPEN_FOR_PROSE = ["person_does", "stop_here", "go_on_as_is", "release_and_restart", "stand_prepare"]


RESTART_STOP = (("restart", "release_and_restart"), ("stop", "stop_here"))


# The question of the live cmp3 S1 verdict (state/conductor.jsonl line 7, 13.10.2026), verbatim: the tokens in apostrophes, `retry` named
# although the conductor offered `restart` / `stop` / `go on` only ("the driver resumes the scout" - `retry` runs `person_does`).
LIVE_S1_QUESTION = ("The S1 exit gate refuses because three sources the scout read (TP1-13797, TP1-8384, TP1-13288) have no "
                    "inspection receipts. They have 0 attachments, or 0 reachable ones, and the scout's job S1-qa-scout-1 is still the live "
                    "dispatch. I can't write these receipts myself: the scout owns them, and the factory forbids cancelling that job. How do "
                    "you want to go on? 'retry': the driver resumes the scout, which records the receipts. 'restart': I free the dispatch on "
                    "your words and the scout starts S1 again, which costs a full scout round. 'stop': stop here.")


def prose_of(question, tokens=RESTART_STOP, site=()):
    """`validate_options` of a verdict whose prose is `question`: `(options, rule)`."""
    return NM.validate_options(verdict(tokens, question=question), OPEN_FOR_PROSE, NM.data(), story_run.Driver.s0_normalize,
                               {"no": {"head": "Verdict: not ready to ship as is."}}, site)


def el12_site_doors_are_not_moves() -> None:
    normalize, spec = story_run.Driver.s0_normalize, NM.data()
    check_eq("EL12: `round` and `fresh` are no move's word", sorted({"round", "fresh"} & NM.reserved_tokens(spec, normalize)), [])
    check_eq("EL12: so a site may name them as doors", NM.site_check(("Round", "fresh", "new text"), spec, normalize), ["round", "fresh", "new text"])
    try:
        NM.site_check(("round", "restart"), spec, normalize)
        shown = False
    except NM.DataUnreadable as exc:
        shown = "`restart`" in str(exc) and "round" not in str(exc)
    check("EL12: `restart` as a door is DataUnreadable and the error names it (not `round`)", shown)


def n_next_the_repair_limit_doors_are_not_moves() -> None:
    """C1-5b1 (t-698 §6 N-next): the doors of the S5 repair-limit questions (`round`, `debt`, `fixed`, `review`) are no move's own word, so the
    question may offer them back as `site_door`; `stop` is the standing token and is never a door. A door that WAS a move's word is refused."""
    normalize, spec = story_run.Driver.s0_normalize, NM.data()
    doors = ("round", "debt", "fixed", "review")
    check_eq("N-next: none of the repair-limit doors is a move's word", sorted(set(doors) & NM.reserved_tokens(spec, normalize)), [])
    check_eq("N-next: so the site may name all four", NM.site_check(doors, spec, normalize), list(doors))
    check("N-next negative control: `retry` as a door of the same question is refused",
          not _site_ok(("round", "retry"), spec, normalize))


def n_next_the_s7_doors_are_never_a_move_word() -> None:
    """C1-5b2 (t-698 §6 N-next): the doors of the S7 repair-limit question - what `s7_limit_facts` offers at the cap (`round`, `debt`) and with
    no count (`debt`) - are rows of the data key `s7.repair_limit`, are no move's own word, and `site_check` takes them; there is NO `fixed`
    (FR-9: re-running a test after the person's edit is S6's run) and no `review`. A move's word as a door of the same question is refused."""
    normalize, spec = story_run.Driver.s0_normalize, NM.data()
    root, _task_root, env = seed("QA-9")
    try:
        driver = driver_for(root, env, "QA-9")
        passes = {"qa-automator": "round pass 3 for qa-automator on S5:aaaaaaaaaaaa", "qa-code-critic": "round pass 3 for qa-code-critic on S5:bbbbbbbbbbbb"}
        rows = [row["answer"] for row in NM.load_question_prices()["s7.repair_limit"]]
        for label, budget, expected in (("the cap", {"counted": 2, "cap": 2, "passes": passes}, ["round", "debt", "stop"]),
                                        ("no count", None, ["debt", "stop"])):
            offer = driver.s7_limit_facts("S7-x-2", "tests/test_a.py::test_one", "inst_7", ["inst_7"], True, "TC-1", budget, "S7-qa-failure-analyst-1")["offer"]
            doors = tuple(token for token in offer if token != "stop")
            check_eq(f"N-next S7 ({label}): the offer is the expected answers", offer, expected)
            check_eq(f"N-next S7 ({label}): every offered answer is a row of `s7.repair_limit`", sorted(set(offer) - set(rows)), [])
            check_eq(f"N-next S7 ({label}): none of the doors is a move's word", sorted(set(doors) & NM.reserved_tokens(spec, normalize)), [])
            check_eq(f"N-next S7 ({label}): `site_check` takes the doors", NM.site_check(doors, spec, normalize), list(doors))
        check("N-next S7: `fixed` and `review` are in no S7 offer", not ({"fixed", "review"} & set(rows)))
        check("N-next S7 negative control: `retry` as a door of the same question is refused", not _site_ok(("round", "retry"), spec, normalize))
    finally:
        harness.cleanup(root)


def el16_the_prose_names_no_extra_token() -> None:
    """t-698 A3: the prose is refused only for a token of the closed vocabulary that is not an option; any quote style; fewer tokens
    than the options is shown as it is; an apostrophe inside a word is no quote."""
    options, rule = prose_of(LIVE_S1_QUESTION)
    check("EL16 (a): the live S1 question (`retry` named, not offered) is refused", options is None, rule)
    check_eq("EL16 (a): and the reason names the extra token", rule, "the question names `retry`, which is not one of its options")
    options, rule = prose_of(LIVE_S1_QUESTION, (("retry", "person_does"),) + RESTART_STOP)
    check("EL16 (a) control: the same question with `retry` among the options is used", options is not None and rule == "", rule)
    for label, opening, closing in (("single quotes", "'", "'"), ("double quotes", '"', '"'), ("backticks", "`", "`"),
                                    ("typographic single", "‘", "’"), ("typographic double", "“", "”")):
        wrap = lambda token: f"{opening}{token}{closing}"
        ok, rule = prose_of(f"How do you want to go on? {wrap('restart')}: start again. {wrap('stop')}: stop here.")
        check(f"EL16 (b): the tokens of the options in {label} are used", ok is not None and rule == "", rule)
        bad, rule = prose_of(f"How do you want to go on? {wrap('restart')}, {wrap('stop')} or {wrap('retry')}?")
        check(f"EL16 (b): an extra token in {label} is refused and named", bad is None and "`retry`" in rule, rule)
    ok, rule = prose_of("What now? `stop` only, or the other one.")
    check("EL16 (c): a prose that names fewer tokens than the options is used as it is", ok is not None and rule == "", rule)
    ok, rule = prose_of("What should happen next?")
    check("EL16 (c): ... and one that names none", ok is not None and rule == "", rule)
    # The two apostrophes around ` retry` sit inside words ("scouts'" and "retry's"): read as a span they would name `retry`, which is
    # not an option. The scout's session follows so the plain possessive is in the sentence too.
    ok, rule = prose_of("The scouts' retry's outcome is unknown and the scout's session is gone. Say `stop` or `restart`.")
    check("EL16 (d): an apostrophe inside a word is no quote (\"the scouts' retry's\" does not name `retry`)", ok is not None and rule == "", rule)
    ok, rule = prose_of("The scout can't go on. Say 'stop' or 'restart', the scout's job is open.")
    check("EL16 (d): a contraction next to real quoted tokens changes nothing", ok is not None and rule == "", rule)
    ok, rule = prose_of("Look at `source-inventory.json` in S1, then say `stop` or `restart`.")
    check("EL16 (e): a quoted span that is no token of the vocabulary is ignored", ok is not None and rule == "", rule)


def el16b_edges_of_the_prose_reader() -> None:
    empty, rule = prose_of("")
    blank, blank_rule = prose_of("  \n ")
    check("EL16 edge: an EMPTY question is refused, as before (the person would be shown the options alone)",
          empty is None and blank is None and "empty" in rule and "empty" in blank_rule, f"{rule} / {blank_rule}")
    ok, rule = prose_of("Say `stop`, `Stop`, 'stop' or `restart`.")
    check("EL16 edge: a token named many times counts once", ok is not None and rule == "", rule)
    bad, rule = prose_of("Say 'retry' or `retry` or \"retry\" or `restart` or `stop`.")
    check_eq("EL16 edge: an extra token named many times is named once", (bad, rule.count("`retry`")), (None, 1))
    bad, rule = prose_of("Say `retry`, `go on`, `restart` or `stop`.")
    check("EL16 edge: two extra tokens are both named", bad is None and "`go on`" in rule and "`retry`" in rule and "are not" in rule, rule)
    site_verdict_tokens = (("read", NM.SITE_DOOR), ("stop", "stop_here"))
    ok, rule = prose_of("Say `read` or `stop`.", site_verdict_tokens, ("read", "skip"))
    check("EL16 edge: a site door among the options is used", ok is not None and rule == "", rule)
    bad, rule = prose_of("Say `read`, `skip` or `stop`.", site_verdict_tokens, ("read", "skip"))
    check("EL16 edge: a site door the prose names but the options do not offer is refused (the site set is in the vocabulary)",
          bad is None and "`skip`" in rule, rule)
    ok, rule = prose_of("Say `read`, `skip` or `stop`.", site_verdict_tokens, ("read",))
    check("EL16 edge: ... and a word that is no door of THIS site is only a quoted span", ok is not None and rule == "", rule)


def k4_the_refusal_is_read_as_its_problems() -> None:
    """t-722 C2-5 (K4): the lines of the standing refusal the driver records are built by FORM, one normalisation that the
    writer applies to the block too (`waiver.refusal_parts`; the driver's `refusal_lines` calls it, C2-5s: `k4s_*` below)."""
    import waiver
    problems = ["the qa-code-critic window is not receipted: no review receipt for TC-1", "no window record for TC-2"]
    door = 'waiver.py --task QA-1 --stage S5 --block "not receipted" --words-file <file>'
    text = "; ".join(problems) + ". These are the review's own receipts, not the person's to produce. If a person accepts the window without them: `" + door + "`."
    parts = waiver.refusal_parts([text])
    check_eq("K4: the controller's joined problems come out apart, the first one whole", parts[0], problems[0])
    check("K4 (negative pin, finding 9): the door in backticks is cut - 'waiver.py --task' is in no line", all("waiver.py --task" not in p for p in parts), str(parts))
    check_eq("K4: ...and the door's block name travels apart", waiver.door_blocks(text), ["not receipted"])
    check_eq("K4: the hint of the guard is cut, then the number of a list item", waiver.refusal_parts(
        ["2) first problem; second problem Your word passes this: `waiver.py --task QA-1 --stage S5 --block \"x\"`."]), ["first problem", "second problem"])
    check_eq("K4: a line that is only a door in backticks has no part; repeats and empties are dropped",
             (waiver.refusal_parts(["`waiver.py --task QA-1`"]), waiver.refusal_parts(["a; a; ; b"])), ([], ["a", "b"]))
    check_eq("K4 (t-842 F2): a line that is only a code span which is no door keeps it - it is the problem's own text", waiver.refusal_parts(["`only code`"]), ["`only code`"])


def cc15_the_offers_of_a_stage_closed_by_code() -> None:
    """CC15, CC21 (C2-8, t-745): `NM.code_close_offer` over every key and every combination of its facts - at least two tokens, `stop`
    always, `go on` only for a non-empty block in neither `passed` nor `refused`, `full retro` only at the missing controller stage, a
    token is a move's word or the site's door (never another reserved word), and every offered token has a PRICE ROW in the data."""
    import itertools
    import no_move as NM
    spec, normalize = NM.data(), (lambda word: " ".join(str(word).lower().split()))
    prices = NM.load_question_prices()
    blocks = ("", NM.BLOCK_RUNNING, NM.BLOCK_NO_STAGE)
    for key in NM.CODE_CLOSE_OFFERS:
        for block, passed, refused, cap in itertools.product(blocks, ([], [NM.BLOCK_RUNNING, NM.BLOCK_NO_STAGE]), ([], [NM.BLOCK_NO_STAGE]),
                                                             (False, True)):
            facts = {"block": block, "passed": passed, "refused": refused, "idle_cap": cap}
            tokens, absent = NM.code_close_offer(key, facts)
            name = f"CC15 {key} {facts}"
            check(f"{name}: at least two tokens and `stop`", len(tokens) >= 2 and "stop" in tokens, str(tokens))
            spent = block in passed or block in refused
            go_on = key == "code_close.closed_story" and bool(block) and not spent
            check_eq(f"{name}: `go on` exactly when a block can be passed", "go on" in tokens, go_on)
            check_eq(f"{name}: `full retro` only at the missing controller stage of the retro",
                     "full retro" in tokens, key == "code_close.closed_story" and block == NM.BLOCK_NO_STAGE)
            check(f"{name}: an absent option is said (FR-42)", ("go on" in tokens) or any("Going on as it is" in line for line in absent), str(absent))
            check(f"{name}: every token has a price row", all(t in {row["answer"] for row in prices[key]} for t in tokens), str(tokens))
            NM.site_check([t for t in tokens if t not in NM.TOKEN_MOVES], spec, normalize)       # a door is no move's word (raises otherwise)
    try:
        NM.code_close_offer("code_close.nothing", {})
        refused = False
    except NM.DataUnreadable:
        refused = True
    check("CC15: an unknown key raises DataUnreadable", refused)
    bad = NM.priced_options("code_close.stage", [{"answer": "retry", "token": "retry", "says": "x"}], spec, {})
    check("CC21 control: the data resolves for a key that has its rows", len(bad) == 1)
    try:
        NM.priced_options("code_close.missing_key", [{"answer": "retry", "token": "retry", "says": "x"}], spec, {})
        unresolved = False
    except NM.DataUnreadable:
        unresolved = True
    check("CC21: a key with no rows is DataUnreadable (the driver then shows the question without prices and files one defect)", unresolved)


def rd1_20_the_s8_summary_run_has_its_door() -> None:
    """RD1-20: the delivery summary S8 writes again after the rebuild is a script run whose result is only printed. It carries its
    door (`# remains: <reason>`), and the baseline does not grow for it (AR-17, AR-20). Kills: the `# remains:` line removed from
    `stage_S8` (the run is then a [NEW] site)."""
    import audit_factory as AF
    scan = AF.a27_scan(Path(story_run.__file__).resolve().parent.parent)
    mine = [s for s in scan.sites if s.qual == "Driver.stage_S8" and s.disc == "delivery_summary.py"]
    check_eq("the summary run in stage_S8 is one site", len(mine), 1)
    check_eq("and it is a door, not a counted state without a move", [s.verdict for s in mine], ["door"])
    check_in("with its reason", "S9 writes the summary again", mine[0].reason if mine else "")
    check_eq("no [NEW] site names it", [n for n in scan.news if "stage_S8" in n or "delivery_summary.py" in n], [])


def u7_r9_s0_readiness_pays_no_conductor_turn() -> None:
    """U7 stream 3 (r9, F-11 = a), a PIN of `Driver.s0_rest`: no row of `conductor-actions.json` settles a missing machine tool, credentials,
    a tests folder or a config, so a required capability `missing` is the person's `s0.readiness` question and the conductor is called 0
    times; a readiness exit that is a refusal (2) is the factory's own fault, a `gate_refusal`, and never a Person (AR-17, AR-25)."""
    missing = json.dumps({"capabilities": {
        "test_repo": {"status": "missing", "note": "tests_root /nope does not exist", "owner": "person"},
        "vcs": {"status": "ok", "note": "git", "owner": "person"},
        "config_schema": {"status": "ok", "note": "valid", "owner": "person"}}})
    for label, code, out, want in (("missing test_repo -> the s0.readiness question, conductor calls 0", 1, missing, "person"),
                                   ("exit 2 -> gate_refusal, no Person", 2, "usage error", "refusal")):
        root, task_root, driver = rig()
        try:
            driver.boundary = "S0:readiness"
            driver.s0_is_local = lambda: True
            real_py = driver.py
            driver.py = lambda script, *a, **k: (code, out) if script == "readiness.py" else real_py(script, *a, **k)
            got = None
            try:
                driver.s0_rest(None, False, [], None, "", True, [])
            except story_run.Person as person:
                got = ("person", person)
            except story_run.Refusal as refusal:
                got = ("refusal", refusal)
            check_eq(f"U7 r9 {label}: the road taken", got[0] if got else None, want)
            check_eq(f"U7 r9 {label}: the conductor was called 0 times", len(driver.calls), 0)
            if want == "person":
                person = got[1]
                check_eq(f"U7 r9 {label}: the block is `readiness`, the Person is S0's, taking retry / go on / stop",
                         (driver.state.get("s0_block"), person.stage, sorted(driver.state["s0_ask"]["doors"])),
                         ("readiness", "S0", ["go on", "retry", "stop"]))
                check_in(f"U7 r9 {label}: the question is the s0.readiness text", "something required is missing", person.text)
                check_in(f"U7 r9 {label}: and the report names the folder", "tests_root /nope does not exist", person.details)
            else:
                refusal = got[1]
                check_eq(f"U7 r9 {label}: a gate_refusal (not a known refusal), naming the exit", (refusal.known, "readiness.py did not complete (exit 2)" in str(refusal)),
                         (False, True))
        finally:
            harness.cleanup(root)


@contextlib.contextmanager
def e7_world(cases=("TC-1",), ended="2020-01-01T00:00:00+00:00", why="start a second browser session", status="completed", need=True, stand="staging"):
    """A driver over a run report whose cases carry a need record (stand `staging`); `rework`, `walk_before` and `failures_to_triage` are stand-ins."""
    from unittest import mock
    import manual_evidence as ME
    root, task_root, driver = logged_rig()
    try:
        marker = dict({"reason": ME.NEED_REASON}, **({"need": "another_instance", "need_why": why} if need else {}))
        rows = [{"case": c, "current_obligation_ids": ["OB-1"], "attempt_ended_at": ended, "unprepared": dict(marker)} for c in cases]
        (task_root / "work").mkdir(exist_ok=True)
        (task_root / "work" / "run-report.json").write_text(json.dumps({"current_manual_checks": rows}), encoding="utf-8")
        driver.triaged, driver.reworks, driver.refuse = [], [], False
        driver.failures_to_triage = lambda awaiting="": driver.triaged.append(1) or "manual " + ",".join(cases)
        driver.controller_state = lambda: {"stages": {"S6": {"status": status}}, "dispatches": {}}
        driver.walk_before = lambda lane, did, assigned=None: {"walking": False, "report_last": False}
        driver.manual_request_paths = lambda block: ["request.json"]
        driver.role_lines = lambda stage, role: ["ROLE"]

        def rework(stage, role, block, reason, **kw):
            if driver.refuse:
                raise story_run.ReworkRefused("controller refused\nsecond line")
            kw["on_request"]("S6-qa-runner-9")
            driver.reworks.append((stage, role, list(block), kw.get("complete"), list(kw["extra"])))
        driver.rework = rework
        with mock.patch("stand_gaps.stand_name", lambda tr: stand):
            yield root, task_root, driver
    finally:
        harness.cleanup(root)


def e7_step(driver, awaiting=""):
    try:
        return driver.s7_extra_instance_step(driver.controller_state(), True, awaiting)
    except story_run.Person as person:
        return person


def e7_answer(root, yes=True, words="yes"):
    import project_knowledge as PK
    return PK.record(root, key=PK.EXTRA_INSTANCE_KEY, environment="staging", element="another_instance", state=PK.KNOWN, scope="stand",
                     value={"authorized": yes}, words=words, source="person", story="QA-9", by="conductor")[0]


def e7_extra_instance_trigger() -> None:
    """E7-3b (spec U7 / E7 r2 §2.1-§2.5, amendments M1, M5, M8): a need record with no answer about another instance is ONE closed question at S7
    entry (no conductor turn, no analyst, no close); a known yes walks the older checks again once per (case, answer); a no is a note; the answers
    are the driver's registry row; the re-walk's restart never makes S6 complete (AR-13, AR-16, AR-17, AR-24, AR-25)."""
    import acceptance
    import project_knowledge as PK
    for label, cases, more in (("11 cases BEYOND the cap", [f"TC-{n}" for n in range(1, 12)], True), ("10 cases AT the cap", [f"TC-{n}" for n in range(1, 11)], False)):
        for world_name, status, awaiting in (("A", "running", "S6-qa-runner-2"), ("B", "completed", "")):
            with e7_world(cases, status=status, why='start it with password: "abcdefghijklmnopqrstuvwx"') as (root, task_root, driver):
                driver.run_role = driver.s7_close = lambda *a, **k: (_ for _ in ()).throw(AssertionError("a role or a close ran over a need"))
                person = e7_step(driver, awaiting)
                text = str(getattr(person, "text", ""))
                check_eq(f"E7 {label}, world {world_name}: ONE Person `extra_instance`, conductor calls 0", (getattr(person, "kind", None), len(driver.calls)), ("extra_instance", 0))
                check(f"E7 {label}: the lead names the stand and the cases, the doors are priced", "`staging`" in text and all(d in text for d in ("start it", "by hand", "stop")))
                check_eq(f"E7 {label}: 10 case lines, and `and 1 more` only beyond the cap", (text.count("\n- TC-"), "- and 1 more (the report lists them all)" in text), (10, more))
                check("E7 N8: a secret-like need_why is masked, never shown", "abcdefghijklmnop" not in text and "(not shown: they look like a secret)" in text)
    with e7_world(need=False) as (root, task_root, driver):
        check_eq("E7 M12-3: a record with no need (a refused need record) -> no question, `failures_to_triage` never called", (e7_step(driver, "S6-x"), driver.triaged), (False, []))
    with e7_world() as (root, task_root, driver):
        driver.failures_to_triage = lambda awaiting="": (_ for _ in ()).throw(story_run.Refusal("S7 entry: run-report.json execution_status is `broken_run`"))
        try:
            e7_step(driver)
            raised_refusal = False
        except story_run.Refusal:
            raised_refusal = True
        check("E7 (i): a halted run with a need raises its Refusal, no Person", raised_refusal)
    for label, status, awaiting in (("A", "running", "S6-qa-runner-2"), ("B", "completed", "")):
        with e7_world(status=status) as (root, task_root, driver):
            row = e7_answer(root)
            check_eq(f"E7 {label}: a known yes and an older record -> one re-walk, no question, no conductor turn", (e7_step(driver, awaiting), len(driver.reworks), len(driver.calls)), (True, 1, 0))
            stage, role, block, complete, lines = driver.reworks[0]
            check_eq(f"E7 {label}: rework of S6 qa-runner over the case", (stage, role, block), ("S6", "qa-runner", ["TC-1"]))
            check(f"E7 {label}: complete is the awaits word in A and False in B, never True",
                  (getattr(complete, "unresolved", None) == acceptance.AWAITS_WORD) if awaiting else complete is False, repr(complete))
            check(f"E7 {label}: the lines hold the finalize line, the allowed line and the role lines",
                  any("finalize_task.py" in x for x in lines) and ALLOWED in lines and lines[-1] == "ROLE", str(lines))
            check_eq(f"E7 {label} N7: one re-walk per (case, answer): the next entry walks nothing", (e7_step(driver, awaiting), len(driver.reworks)), (False, 1))
            driver.controller_state = lambda: {"stages": {"S6": {"status": status}}, "dispatches": {}}
            check_eq(f"E7 {label} M1: a restart of the re-walk is never complete (A: awaits word, B: False), S6 not re-planned",
                     (type(driver.completion_for("S6", "qa-runner", {"id": "S6-qa-runner-9"})).__name__, driver.state["extra_instance_rewalk"] == {f"TC-1|{row['id']}": "S6-qa-runner-9"}),
                     ("OpenWork" if awaiting else "bool", True))
            PK.revoke(root, row["id"], "changed my mind")
            check("E7 N7: revoked -> the next need asks again", getattr(e7_step(driver, awaiting), "kind", "") == "extra_instance")
            e7_answer(root, words="yes again")
            check_eq("E7 N7: a new yes has a new id, so the re-walk is owed again", (e7_step(driver, awaiting), len(driver.reworks)), (True, 2))
    for label, ended in (("equal moments", None), ("an unreadable moment", "not a time"), ("a need newer than the yes", "2999-01-01T00:00:00+00:00")):
        with e7_world(ended=ended or "") as (root, task_root, driver):
            row = e7_answer(root)
            if ended is None:
                (task_root / "work" / "run-report.json").write_text(json.dumps({"current_manual_checks": [{"case": "TC-1", "attempt_ended_at": row["at"], "unprepared": {
                    "reason": "needs another instance of the stand or device; not started without the person's word", "need": "another_instance", "need_why": "w"}}]}), encoding="utf-8")
            check_eq(f"E7 M5: {label} -> not owed, no rework, no question", (e7_step(driver, "S6-x"), len(driver.reworks)), (False, 0))
            check_in(f"E7 M15: {label} -> a note of the case", "TC-1", (task_root / "work" / "extra-instance.json").read_text(encoding="utf-8"))
    with e7_world() as (root, task_root, driver):
        e7_answer(root, yes=False)
        check_eq("E7: a known no -> no Person, no rework, a note", (e7_step(driver, "S6-x"), len(driver.reworks), "the person said the factory may not start one" in (task_root / "work" / "extra-instance.json").read_text(encoding="utf-8")), (False, 0, True))
    with e7_world() as (root, task_root, driver):
        e7_answer(root)
        driver.refuse = True
        check_eq("E7: ReworkRefused -> counted `refused`, a line, False", (e7_step(driver, "S6-x"), list(driver.state["extra_instance_rewalk"].values())), (False, ["refused"]))
    for token, want in (("Start It", True), ('"by hand"', False), ("  start it ", True)):
        with e7_world() as (root, task_root, driver):
            check("E7: the question is asked", getattr(e7_step(driver, "S6-x"), "kind", "") == "extra_instance")
            if token.startswith(" "):       # F2: through the machine's own answer door (`take_answer`, kind `extra_instance`)
                driver.state["asked"] = {"kind": "extra_instance", "stage": "S7", "dispatch": ""}
                take(driver, answer(task_root, "ans.txt", token.encode()))
            else:
                driver._answer = {"text": token, "rel": None}
                driver._answer_extra_instance(token, "", "S7", "")
            got = PK.instance_answer(root, "staging", "another_instance")
            check_eq(f"E7 AR-24: `{token}` -> the driver's registry row, the words whole", (got["authorized"], got["row"]["provenance"]["words"], got["row"]["provenance"]["by"]), (want, token.strip(), "driver"))
    with e7_world() as (root, task_root, driver):
        e7_step(driver, "S6-x")
        driver._answer = {"text": "stop", "rel": None}
        try:
            driver._answer_extra_instance("stop", "", "S7", "")
            held = None
        except story_run.Person as person:
            held = person
        check_eq("E7: `stop` -> held, no row", (held is not None, PK.instance_answer(root, "staging", "another_instance")["authorized"]), (True, None))
        check("E7: the rerun lead starts `You answered `stop` earlier.`", str(e7_step(driver, "S6-x").text).startswith("You answered `stop` earlier."))
        driver._answer = {"text": "what?", "rel": None}
        calls = len(driver.calls)
        try:
            driver._answer_extra_instance("what do you mean", "", "S7", "")
        except story_run.Person:
            pass
        check_eq("E7: free words -> the `unread` road once, no row", (len(driver.calls) - calls, PK.instance_answer(root, "staging", "another_instance")["authorized"]), (1, None))
    with e7_world(stand="this stand") as (root, task_root, driver):        # F3: no stand chosen -> the answer is held for this story
        person = e7_step(driver, "S6-x")
        text = str(person.text)
        check("E7 F3: the story-only lead and door words", "on the stand of this story" in text and "holds for this story only" in text
              and "for this story only; the checks above" in text and "`ask again`" not in text)
        driver._answer = {"text": "start it", "rel": None}
        driver._answer_extra_instance("start it", "", "S7", "")
        held = driver.state.get("extra_instance_held", {}).get("this stand|another_instance", {})
        check_eq("E7 F3: no registry row, the yes is held under the key the step reads", (PK.instance_answer(root, "this stand", "another_instance")["authorized"], held.get("authorized")), (None, True))
        check_eq("E7 F3: the NEXT step reads the held yes and starts the one re-walk", (e7_step(driver, "S6-x"), len(driver.reworks)), (True, 1))
    with e7_world() as (root, task_root, driver):        # F1: the real stage_S7, world B (S6 completed, an accepted fresh triage), a need with no answer
        def never(*a, **k):
            raise AssertionError("a close, a repair or an analyst ran over a need")
        driver.run_role = driver.s7_repairs = driver.s7_close = driver.close_by_code = never
        driver.pipeline, driver.s7_fresh, driver.consumer_pending = (lambda: {}), (lambda: True), (lambda stage: False)
        triaged = {"S7-qa-failure-analyst-1": {"stage": "S7", "role": "qa-failure-analyst", "status": "accepted"}}
        driver.controller_state = lambda: {"stages": {"S6": {"status": "completed"}}, "dispatches": triaged}
        for label, pending in (("accepted fresh triage", False), ("M9: a scribe accept pending", True)):
            driver.consumer_pending = lambda stage, pending=pending: pending
            try:
                driver.stage_S7()
                kind = None
            except story_run.Person as person:
                kind = person.kind
            check_eq(f"E7 F1: stage_S7, world B, {label} -> the Person, no close, no analyst", kind, "extra_instance")
    with e7_world() as (root, task_root, driver):
        driver.run_role = lambda *a, **k: None
        driver.pipeline = lambda: {}
        for name in ("s7_repair_rows", "s7_rejudge_rows"):
            setattr(driver, name, lambda: [])
        driver.s7_life, driver.s7_decided, driver.s7_plan = (lambda: "L"), (lambda life=None: {}), (lambda rows, life: [])
        driver.s7_close = lambda *a, **k: (_ for _ in ()).throw(AssertionError("S7 closed over a need"))
        try:
            driver.s7_repairs()
            kind = None
        except story_run.Person as person:
            kind = person.kind
        check_eq("E7 F-r2-1: a need written inside the re-judge round -> the second call asks before any close", kind, "extra_instance")


ALLOWED = ("The person allowed the factory to start another instance of the stand or device for these checks: start it with the project's own "
           "actions, write what you started in `tried.md`, and walk the checks again.")


def test_e7_extra_instance_trigger() -> None:
    n = len(harness.RESULTS)
    e7_extra_instance_trigger()
    assert all(ok for ok, _ in harness.RESULTS[n:]), [name for ok, name in harness.RESULTS[n:] if not ok]


def main() -> None:
    for scenario in (
        e7_extra_instance_trigger,
        u7_r9_s0_readiness_pays_no_conductor_turn,
        rd1_20_the_s8_summary_run_has_its_door,
        cc15_the_offers_of_a_stage_closed_by_code,
        k4_the_refusal_is_read_as_its_problems,
        el12_site_doors_are_not_moves,
        n_next_the_repair_limit_doors_are_not_moves,
        n_next_the_s7_doors_are_never_a_move_word,
        el16_the_prose_names_no_extra_token,
        el16b_edges_of_the_prose_reader,
        n22_the_gate_raised_again_over_an_open_seam_question,
        n23_a_conductor_continue_at_a_gate_shows_the_gate_again,
        n21_keep_at_the_stuck_threshold,
        n16_site_doors,
        n17_site_fallback,
        n18_package_unread,
        n19_ticket_changed_unread,
        n20_the_funnel_reads_new_words,
    ):
        scenario()
    harness.finish("no_move seam_sites")


# split: runner piece 1
if __name__ == "__main__":
    main()
