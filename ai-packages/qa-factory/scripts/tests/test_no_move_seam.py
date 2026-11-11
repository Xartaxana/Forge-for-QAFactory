#!/usr/bin/env python3
"""The one seam "no move" (conductor/1, C1-1): `Driver.no_move` and the pure half in `no_move.py`.

In-process, with `conductor` stubbed on the driver (no `claude`, no network): the cases are N1 one `why` at a time, N2 the moves
filter (one positive and one negative per row, every adversarial input on the safe side), N3 `options` authoritative, N4 the
cap AT and BEYOND, N5 the gate kinds, N9 the edges, and the pins that tie the carriers (MOVE_FACTS keys == moves[].id; the labels
of `price_lines` == item 6 of human-questions.md)."""
import contextlib
import io
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from harness import check, check_eq, check_in, check_not_in  # noqa: E402
from story_run_common import driver_for, jsonl, seam_option, seed  # noqa: E402

import human_text  # noqa: E402
import no_move as NM  # noqa: E402
import story_run  # noqa: E402

TWO = (("retry", "person_does"), ("stop", "stop_here"))
QUESTION = "What should happen? `retry` once you have dealt with it, or `stop`."


def verdict(tokens=TWO, question=QUESTION, action="ask_person", **extra):
    # RN1-9: a conductor question names a class and what it read; the DEFAULT keeps every key of this file on the road of a usable answer,
    # and a case that wants the refusal overrides it (`why_person=None`, `checked=""`)
    return dict({"action": action, "did": "looked", "question": question, "why_person": "access", "checked": "the refusal",
                 "options": [seam_option(token, move) for token, move in tokens]}, **extra)


def rig(task="QA-9", answers=None):
    """A driver whose conductor is a stub: `answers` is the list of verdicts it gives; `calls` collects the prompts."""
    root, task_root, env = seed(task)
    driver = driver_for(root, env, task)
    driver.calls, driver.defects = [], []
    queue = list(answers or [])

    def conductor(text, *, words="", files=None, words_file=None):
        count = driver.conductor_calls.get(driver.boundary, 0)
        if count >= story_run.CONDUCTOR_CALLS_PER_BOUNDARY:
            raise story_run.ConductorSpent(count, text)
        driver.calls.append({"text": text, "words": words, "words_file": words_file})
        driver.conductor_calls[driver.boundary] = count + 1
        return queue.pop(0) if queue else verdict()
    driver.conductor = conductor
    real_py = driver.py
    driver.py = lambda script, *a, **k: (driver.defects.append(a), (0, ""))[1] if script == "log_append.py" and "defect_found" in a else real_py(script, *a, **k)
    return root, task_root, driver


def raised(driver, state, moves=None):
    try:
        return driver.no_move(state, moves), None
    except story_run.Person as person:
        return None, person


def n1_one_why_at_a_time() -> None:
    root, task_root, driver = rig()
    try:
        driver.boundary = "S5:S5-qa-automator-1"
        for why in ("refusal", "stop", "unread_answer", "by_hand", "chosen"):
            driver.conductor_calls.clear()
            driver.calls.clear()
            state = {"why": why, "kind": "conductor", "stage": "S5", "dispatch": "", "text": "the factory's words", "words": "w",
                     "move": "person_does", "token": "retry"}
            result, person = raised(driver, state)
            check(f"N1 {why}: a Person of kind conductor", person is not None and person.kind == "conductor")
            check_eq(f"N1 {why}: offered = the tokens", list(person.offered), ["retry", "stop"])
            check_eq(f"N1 {why}: the conductor was called once", len(driver.calls), 1)
            for token in ("retry", "stop"):
                check_in(f"N1 {why}: `{token}` is followed by the three labels",
                         "\nthe factory: nothing runs now\nyou: work of yours outside the factory: the thing named above\nthe story: ", person.text)
            check_eq(f"N1 {why}: the factory's words are the details", person.details, "the factory's words")
            check_eq(f"N1 {why}: the price lines pass price_problems", human_text.price_problems(person.text, list(person.offered)), [])
        for why in ("cap", "threshold"):
            driver.calls.clear()
            driver.defects.clear()
            _, person = raised(driver, {"why": why, "kind": "refusal", "call": False, "text": "t"})
            check_eq(f"N1 {why} with call=False: the conductor was called 0 times", len(driver.calls), 0)
            if why == "cap":
                check("N1 cap: the defect names the refusal cap, not the conductor's",
                      len(driver.defects) == 1 and "the refusal cap was reached" in " ".join(driver.defects[0])
                      and "conductor cap" not in " ".join(driver.defects[0]), str(driver.defects))
            check_eq(f"N1 {why}: the fallback offers retry / go on / stop", list(person.offered), ["retry", "go on", "stop"])
            check_eq(f"N1 {why}: kind kept", person.kind, "refusal")
        driver.ask(person)
        asked = driver.state["asked"]
        check_eq("N1: ask() writes offered / options / why", (asked["offered"], asked["why"], asked["options"][0]),
                 (["retry", "go on", "stop"], "threshold", {"token": "retry", "move": "person_does",
                                                            "says": "you deal with what is in the way, and the factory looks again"}))     # C2-6: `says` travels (§4.3)
    finally:
        harness.cleanup(root)


def n2_the_filter() -> None:
    base = {"dispatch_status": "running", "session": True, "running": False, "closed": False, "attempts": 0,
            "rework_stages": ["S5"], "stand_authorized": True, "live_exclusions": True, "gate": "", "gate_decided": None}
    every = NM.move_ids()
    check_eq("N2: MOVE_FACTS keys == moves[].id of conductor-actions.json", sorted(NM.MOVE_FACTS), sorted(every))
    check_eq("N2: every move but `approve_gate` is open on a clean state outside a gate (that one needs a gate)",
             sorted(NM.open_moves(base, every)), sorted(set(every) - {"approve_gate"}))
    cases = [("rework_stage", {"rework_stages": []}), ("rework_stage", {"running": True}), ("rework_stage", {"closed": True}),
             ("rework_stage", {"attempts": 1}), ("rework_stage", {"attempts": None}), ("rework_stage", {"closed": None}),
             ("resume_with_words", {"dispatch_status": "accepted"}), ("resume_with_words", {"dispatch_status": "released_by_person"}),
             ("resume_with_words", {"dispatch_status": "never_started"}), ("resume_with_words", {"dispatch_status": "superseded"}),
             ("resume_with_words", {"dispatch_status": "stale"}), ("resume_with_words", {"dispatch_status": None}),
             ("resume_with_words", {"session": False}), ("release_and_restart", {"attempts": 1}),
             ("release_and_restart", {"dispatch_status": "superseded"}), ("stand_prepare", {"stand_authorized": False}),
             ("stand_prepare", {"stand_authorized": None}), ("revoke_exclusion", {"live_exclusions": False}),
             ("revoke_exclusion", {"live_exclusions": None})]
    for move, change in cases:
        check(f"N2 negative: {move} removed by {change}", move not in NM.open_moves(dict(base, **change), every))
    at_gate = dict(base, gate="B", gate_decided=False)
    check_eq("N2 (C1-4b): at a gate with no current decision `approve_gate` is open and `go_on_as_is` is not - at a gate the one pass is "
             "`approve`, two moves never pass one gate",
             sorted(NM.open_moves(at_gate, every)), sorted((set(every) - {"go_on_as_is"})))
    for label, change in (("gate decided", {"gate_decided": True}), ("gate decision unreadable", {"gate_decided": None}),
                          ("not at a gate", {"gate": ""}), ("a gate that is no gate", {"gate": "C"})):
        check(f"N2 negative (C1-4b): approve_gate removed by {label}", "approve_gate" not in NM.open_moves(dict(at_gate, **change), every))
    check("N2 negative (C1-4b): go_on_as_is removed at gate A as well, and by an unreadable gate fact",
          "go_on_as_is" not in NM.open_moves(dict(at_gate, gate="A"), every) and "go_on_as_is" not in NM.open_moves(dict(base, gate=None), every))
    check("N2: a raising predicate removes only its move",
          NM.open_moves(None, ["person_does"]) == ["person_does"] and "x" not in NM.open_moves(base, ["x"]))
    check("N2: no_trace is not a fact the filter reads (FR-36): the table has no such key", "no_trace" not in json.dumps(sorted(NM.MOVE_FACTS)))


def n3_options_authoritative() -> None:
    normalize = story_run.Driver.s0_normalize
    spec, words, open_ids = NM.data(), {"no": {"head": "Verdict: not ready to ship as is."}}, ["person_does", "stop_here", "release_and_restart"]
    ok, rule = NM.validate_options(verdict(), open_ids, spec, normalize, words)
    check("N3: the clean verdict is valid", ok is not None and rule == "", rule)
    bad = {"duplicate tokens": verdict((("retry", "person_does"), ("retry", "person_does")), question="What should happen? `retry`?"),
           "a token outside the move": verdict((("retry", "person_does"), ("go on", "stop_here"))),
           "a move not open": verdict((("retry", "person_does"), ("prepare the stand", "stand_prepare"))),
           "prose/options mismatch": verdict(question="What should happen? `retry` or `stop` or `go on`?"),
           "one option": verdict((("retry", "person_does"),)),
           "token dash": verdict((("retry", "person_does"), ("—", "rework_stage"))),
           "story as a plain string": dict(verdict(), options=[dict(seam_option("retry", "person_does"), story="x"), seam_option("stop", "stop_here")]),
           "a wrong action": verdict(action="wait")}
    for label, candidate in bad.items():
        options, rule = NM.validate_options(candidate, open_ids, spec, normalize, words)
        check(f"N3 {label}: not used ({rule})", options is None and rule)
    root, task_root, driver = rig(answers=[verdict((("retry", "person_does"), ("retry", "person_does")), question="What now? `retry`?")])
    try:
        driver.boundary = "S5:x"
        _, person = raised(driver, {"why": "refusal", "text": "t"})
        check_eq("N3: a duplicate-token verdict renders the fallback", list(person.offered), ["retry", "go on", "stop"])
        check_eq("N3: and exactly one defect_found is journalled", len(driver.defects), 1)
    finally:
        harness.cleanup(root)
    root, task_root, driver = rig(answers=[dict(verdict(), action="continue")])
    try:
        driver.boundary = "S5:x"
        _, person = raised(driver, {"why": "refusal", "text": "t"})
        check("N3: `continue` with options is not a move", person is not None and len(driver.defects) == 1)
    finally:
        harness.cleanup(root)


def n4_the_cap() -> None:
    root, task_root, driver = rig()
    try:
        driver.boundary = "S5:x"
        cap = story_run.CONDUCTOR_CALLS_PER_BOUNDARY
        driver.conductor_calls[driver.boundary] = cap - 1
        _, person = raised(driver, {"why": "refusal", "text": "t"})
        check_eq("N4 AT the cap - 1: the conductor is called", len(driver.calls), 1)
        driver.conductor_calls[driver.boundary] = cap
        driver.calls.clear()
        _, person = raised(driver, {"why": "refusal", "text": "t"})
        check_eq("N4 AT the cap: no call", len(driver.calls), 0)
        check("N4 AT the cap: the defect names the conductor cap",
              len(driver.defects) == 1 and "the conductor cap was reached" in " ".join(driver.defects[0]), str(driver.defects))
        check_not_in("N4: and never the old text", "What should happen?", person.text)
        check_in("N4: but the fallback with its prices", "## What each answer costs and does", person.text)
    finally:
        harness.cleanup(root)


def n5_gate_kinds_carry_their_moves() -> None:
    """N5 (flipped by C1-4b): the gates left EXCLUDED_KINDS. A gate kind is called with the moves open at the gate and its priced
    options, offers what the conductor offers within them, and its fallback (cap, unreadable answer) is `retry` / `stop`."""
    root, task_root, driver = rig(answers=[verdict(question="What now? `retry` once you changed it, or `stop`?")])
    try:
        driver.boundary = "S8:answer"
        _, person = raised(driver, {"why": "unread_answer", "kind": "gate_B", "stage": "S8", "text": "t", "words": "w"})
        check_eq("N5: a gate kind now carries offered - the conductor's two options", list(person.offered), ["retry", "stop"])
        check_eq("N5: and keeps the gate's own kind", person.kind, "gate_B")
        check_in("N5: the call carried the moves section", "## Moves open here", driver.calls[0]["text"])
        check_in("N5: and the options of this gate with their price lines (data rows `gate_B`)", "## The options at this gate",
                 driver.calls[0]["text"])
        driver.conductor_calls[driver.boundary] = story_run.CONDUCTOR_CALLS_PER_BOUNDARY
        driver.calls.clear()
        _, person = raised(driver, {"why": "unread_answer", "kind": "gate_A", "stage": "S4", "text": "t", "words": "w"})
        check_eq("N5d: the cap at a gate: no call, the gate's own kind, and the gate fallback `retry` / `stop`",
                 (len(driver.calls), person.kind, list(person.offered)), (0, "gate_A", ["retry", "stop"]))
        check_not_in("N5d: never today's free 'What should happen?'", "What should happen?", person.text)
        check_in("N5d: and the fallback's priced lines", "## What each answer costs and does", person.text)
    finally:
        harness.cleanup(root)
    root, task_root, driver = rig(answers=[verdict((("retry", "person_does"), ("go on", "go_on_as_is")), question="Which? `retry` or `go on`?")])
    try:
        driver.boundary = "S4:answer"
        _, person = raised(driver, {"why": "unread_answer", "kind": "gate_A", "stage": "S4", "text": "t", "words": "w"})
        check_eq("N5c: a `go on` the conductor offers at a gate is not valid (the move is closed there): the gate fallback, one defect",
                 (list(person.offered), len(driver.defects)), (["retry", "stop"], 1))
    finally:
        harness.cleanup(root)


def n5c_approve_is_open_only_at_a_gate_with_no_decision() -> None:
    """N5c: the facts of `Driver.no_move_facts` over a stubbed controller state - `gate` from the SITE's kind alone, `gate_decided` from
    an approved decision of that gate on the story's current source revision, `go on` never open at a gate."""
    root, task_root, driver = rig()
    try:
        ctl = {"dispatches": {}, "decisions": {}, "source_revision": "r1"}
        driver.controller_state = lambda: ctl
        moves = NM.move_ids()

        def opened(kind):
            return driver.open_moves({"kind": kind, "dispatch": ""}, moves)
        for kind in ("gate_A", "gate_B"):
            check(f"N5c: {kind} with no decision: `approve_gate` open, `go_on_as_is` closed",
                  "approve_gate" in opened(kind) and "go_on_as_is" not in opened(kind), str(opened(kind)))
        check("N5c: a question that is no gate: `go_on_as_is` open, `approve_gate` closed",
              "go_on_as_is" in opened("conductor") and "approve_gate" not in opened("conductor"))
        driver.state["asked"] = {"kind": "gate_B"}
        check_eq("N5c: the gate is never read from `asked` (C1-1 F1): a conductor site is no gate whatever was asked",
                 driver.no_move_facts({"kind": "conductor", "dispatch": ""})["gate"], "")
        ctl["decisions"] = {"g": {"gate": "A", "status": "approved", "source_revision": "r1"}}
        check("N5c: gate A decided: `approve_gate` closed at gate A, still open at gate B",
              "approve_gate" not in opened("gate_A") and "approve_gate" in opened("gate_B"))
        ctl["decisions"]["g"]["status"] = "stale"
        check("N5c: a stale decision is no decision: open again", "approve_gate" in opened("gate_A"))
        ctl["decisions"]["g"].update(status="approved", source_revision="r0")
        check("N5c: a decision on another source revision is no current decision: open again", "approve_gate" in opened("gate_A"))
        driver.controller_state = lambda: {}
        check("N5c: an unreadable controller state removes `approve_gate` (the safe side, FR-59) and still not `go_on_as_is`'s closure",
              "approve_gate" not in opened("gate_B") and "go_on_as_is" not in opened("gate_B"))
    finally:
        harness.cleanup(root)


def n2c_the_stages_a_rework_may_name() -> None:
    """N2c (C1-4b): `stages_open` - S5-S8 once gate A is decided, S1-S4 before it; a later accepted stage no longer closes an earlier one
    (the person-word rework stamps the later stages to run again, C1-4a)."""
    root, task_root, driver = rig()
    try:
        ctl = {"dispatches": {f"d{n}": {"status": "accepted", "stage": f"S{n}"} for n in range(1, 8)}, "decisions": {}, "source_revision": "r1"}
        driver.controller_state = lambda: ctl
        read = lambda: driver.no_move_facts({"kind": "gate_B", "dispatch": ""})["rework_stages"]
        check_eq("N2c: gate A undecided: S1-S4 only, S5-S7 absent", read(), ["S1", "S2", "S3", "S4"])
        ctl["decisions"] = {"a": {"gate": "A", "status": "approved", "source_revision": "r1"}}
        check_eq("N2c: gate A decided: S5-S7, S4 absent, and S5 is open although S6 and S7 are accepted (the old rule closed it)",
                 read(), ["S5", "S6", "S7"])
        ctl["dispatches"]["d9"] = {"status": "accepted", "stage": "S9"}
        ctl["dispatches"]["d8"] = {"status": "accepted", "stage": "S8"}
        check_eq("N2c: S8 is the last stage a rework may name; S9 never", read(), ["S5", "S6", "S7", "S8"])
        ctl["dispatches"]["d6"]["status"] = "stale"
        check_eq("N2c: a stale dispatch names no stage", read(), ["S5", "S7", "S8"])
        ctl["decisions"]["a"]["status"] = "stale"
        check_eq("N2c: gate A made stale: back to S1-S4", read(), ["S1", "S2", "S3", "S4"])
    finally:
        harness.cleanup(root)


def n9_edges_and_ties() -> None:
    labels = human_text.price_labels()
    item6 = re.search(r"6\. \*\*Price and consequences, per option\.\*\*(.*)", (Path(story_run.__file__).resolve().parent.parent
                                                                             / "references" / "human-questions.md").read_text(encoding="utf-8"))
    check("N9: the three labels of price_lines are the ones item 6 names", item6 and all(f"`{label}`" in item6.group(1) for label in labels), str(labels))
    check_eq("N9: TOKEN_MOVES == the tokens of the data", {m["token"]: m["id"] for m in NM.data()["moves"] if m["token"] in NM.TOKEN_MOVES},
             NM.TOKEN_MOVES)
    root, task_root, driver = rig()
    try:
        driver.boundary = "S5:x"
        orig = NM.fallback_options
        NM.fallback_options = lambda *a, **k: (_ for _ in ()).throw(story_run.Refusal("rendering broke"))
        try:
            _, person = raised(driver, {"why": "refusal", "call": False, "text": "t"})
        finally:
            NM.fallback_options = orig
        check_eq("N9: a rendering failure still ends in a question (the last resort, no price lines)", list(person.offered), ["retry", "go on", "stop"])
        check_eq("N9: the seam is free again after it (reset in a finally)", driver._in_no_move, False)
        check_eq("N9: one defect_found", len(driver.defects), 1)
        driver._in_no_move = True
        _, person = raised(driver, {"why": "refusal", "text": "t"})
        driver._in_no_move = False
        check("N9: re-entry renders the last resort and never recurses", person is not None and not driver.calls)
        long6000, long6001 = "x" * 6000, "x" * 6001
        driver.conductor = story_run.Driver.conductor.__get__(driver)
        driver.run_claude = lambda *a, **k: {"result": json.dumps({"action": "continue", "did": "d"}), "session_id": "s", "stderr": "",
                                              "total_cost_usd": 0, "num_turns": 1}
        driver.step = lambda *a, **k: "next: nothing"
        driver._answer = {"text": long6001, "rel": None}
        seen = []
        driver.run_claude = lambda kind, prompt, **k: (seen.append(prompt), {"result": '{"action": "continue", "did": "d"}', "session_id": "s",
                                                                             "stderr": "", "total_cost_usd": 0, "num_turns": 1})[1]
        driver.conductor("r", words=long6000)
        driver.conductor("r", words=long6001, words_file=driver.answer_file())
        check_not_in("N9: 6000 characters are not cut", "(cut;", seen[0])
        check_in("N9: 6001 characters are cut, with the pointer to the whole file", "(cut; the whole answer is in", seen[1])
        check_eq("N9: the words file keeps the answer whole (CRLF kept)", (task_root / driver.answer_file()).read_bytes(), long6001.encode())
    finally:
        harness.cleanup(root)


FACTS = {"dispatch_status": "blocked", "session": True, "running": False, "closed": False, "attempts": 0,
         "rework_stages": [], "stand_authorized": False, "live_exclusions": False}


def seam_asked(driver, options=TWO, *, stage="S5", dispatch="S5-qa-x-1", block="", kind="conductor", words_file="", why="unread_answer"):
    """Open a question the way the seam raises one (a Person carrying `offered`), through `ask()` as the run does."""
    person = story_run.Person(kind, "What now? `retry` or `stop`?\n\n(a) `retry` - looks again", stage, dispatch)
    person.offered = tuple(token for token, _ in options)
    person.options = [{"token": token, "move": move} for token, move in options]
    person.words_file, person.why, person.block = words_file, why, block
    driver.ask(person)


def answer(task_root, name, data: bytes):
    path = task_root / name
    path.write_bytes(data)
    return path


def take(driver, path):
    """`take_answer`: None when it came back, else the Person the seam raised from inside it."""
    try:
        driver.take_answer(path)
        return None
    except story_run.Person as person:
        return person


def logged_rig(answers=None):
    """`rig` with every `log_append` call collected in `driver.logged` (and the judge of the reply switched off)."""
    root, task_root, driver = rig(answers=answers)
    driver.logged, inner = [], driver.py
    driver.py = lambda script, *a, **k: (driver.logged.append(a), inner(script, *a, **k))[1] if script == "log_append.py" else inner(script, *a, **k)
    driver.judged_reply = lambda *a, **k: ""
    driver.no_move_facts = lambda state: dict(FACTS)
    return root, task_root, driver


def n2b_the_facts_are_read_from_the_project() -> None:
    root, task_root, driver = rig()
    try:
        facts = driver.no_move_facts({"dispatch": ""})
        check_eq("N2b: a clean project: not closed, nothing running, no attempt, no dispatch, no exclusion",
                 (facts["closed"], facts["running"], facts["attempts"], facts["dispatch_status"], facts["live_exclusions"]),
                 (False, False, 0, None, False))
        moves = NM.move_ids()
        check("N2b: a dispatch id the controller does not know removes the dispatch-tied moves",
              not {"resume_with_words", "release_and_restart"} & set(driver.open_moves({"dispatch": "S5-nope"}, moves)))
        driver.state["delivery_attempts"] = [{"status": "in_flight"}]
        check("N2b: a delivery attempt in flight removes rework_stage and release_and_restart",
              not {"rework_stage", "release_and_restart"} & set(NM.open_moves(driver.no_move_facts({"dispatch": ""}), moves)))
        driver.controller_state = lambda: {}
        broken = driver.no_move_facts({"dispatch": "S5-x"})
        check("N2b: an unreadable controller.json: every controller fact is None",
              all(broken[name] is None for name in ("dispatch_status", "session", "running", "closed", "rework_stages")), str(broken))
        check("N2b: and the moves that need them are removed",
              not {"rework_stage", "resume_with_words", "release_and_restart"} & set(NM.open_moves(broken, moves)))
        check_eq("N2b: the standing moves stay", sorted({"person_does", "stop_here"} & set(NM.open_moves(broken, moves))),
                 ["person_does", "stop_here"])
    finally:
        harness.cleanup(root)


def n5b_a_token_never_reaches_a_gate_recorder() -> None:
    root, task_root, driver = logged_rig()
    try:
        driver.boundary = "gate_A"
        seen = []
        driver.record_by_code = lambda *a, **k: seen.append(a) or True
        seam_asked(driver, stage="S4", dispatch="")
        check_eq("N5b: a `retry` to an options question raised at the gate boundary is read by the seam branch, nothing else",
                 take(driver, answer(task_root, "g.md", b"retry\r\n")), None)
        check_eq("N5b: record_by_code was called 0 times", seen, [])
        check_eq("N5b: and the conductor 0 times", driver.calls, [])
    finally:
        harness.cleanup(root)


def n6_s1_review_keeps_today() -> None:
    root, task_root, driver = logged_rig(answers=[{"action": "ask_person", "did": "x", "question": "Which source did you mean?",
                                                   "why_person": "access", "checked": "the refusal"}])      # RN1-9: the legacy road needs a class too (E-8)
    try:
        recorded = []
        driver.record_review = lambda words: (recorded.append(words), True)[1]
        driver.state["asked"] = {"kind": "s1_review", "stage": "S1", "dispatch": "S1-qa-scout-1"}
        check_eq("N6: an answer record_review reads is recorded as today", take(driver, answer(task_root, "r1.md", b"accepted as is\r\n")), None)
        check_eq("N6: record_review was called once with the words", recorded, ["accepted as is"])
        check_eq("N6: the conductor was not called, the words are filed for the dispatch",
                 (driver.calls, driver.state["pending_words"].get("S1-qa-scout-1")), ([], "accepted as is"))
        driver.record_review = lambda words: False
        driver.state["asked"] = {"kind": "s1_review", "stage": "S1", "dispatch": "S1-qa-scout-1"}
        person = take(driver, answer(task_root, "r2.md", b"something else entirely"))
        check("N6: an answer it cannot read goes to the conductor and back as the conductor's own question, with no options",
              person is not None and (person.kind, person.text, bool(person.offered)) == ("s1_review", "Which source did you mean?", False))
        check_not_in("N6: and the call carried no moves section", "## Moves open here", driver.calls[0]["text"])
    finally:
        harness.cleanup(root)


def n7_the_words_file_round_trip() -> None:
    raw = b"please look at the second window\r\nit is the stand, I think\r\n"
    root, task_root, driver = logged_rig(answers=[verdict((("retry", "person_does"), ("restart", "release_and_restart")),
                                                          question="What now? `retry` or `restart`?"),
                                                  {"action": "continue", "did": "restarted"}])
    try:
        driver.ask(story_run.Person("conductor", "What should happen at the plan stage?", "S5", "S5-qa-x-1"))
        person = take(driver, answer(task_root, "a1.md", raw))
        check("N7: a free two-line CRLF answer reaches the seam and comes back as an options question",
              person is not None and list(person.offered) == ["retry", "restart"])
        rel = person.words_file
        check("N7: the words file is task-root relative", rel.startswith("state/words/") and not Path(rel).is_absolute(), rel)
        check_eq("N7: and holds the answer's raw bytes", (task_root / rel).read_bytes(), raw)
        check_eq("N7: the conductor got the words with plain newlines", driver.calls[0]["words"],
                 "please look at the second window\nit is the stand, I think")
        check_eq("N7: the seam handed that very file to the conductor", driver.calls[0]["words_file"], rel)
        driver.ask(person)
        check_eq("N7: ask() keeps it in asked.words_file", driver.state["asked"]["words_file"], rel)
        driver.calls.clear()
        token_file = answer(task_root, "a2.md", b"restart\r\n")
        released = []
        real_release = story_run.waiver.run_release
        story_run.waiver.run_release = lambda task_root, dispatch, **kw: (released.append((dispatch, kw)), (0, "released"))[1]
        try:
            check_eq("N7: the token `restart` is read against the offered options and moves", take(driver, token_file), None)
        finally:
            story_run.waiver.run_release = real_release
        # C2-6 (t-722 §4.4): `restart` is executed by CODE through waiver.run_release with the ORIGINAL words' file, no conductor call
        check_eq("N7 (C2-6, t-873 F-1): `restart` released the dispatch the question names with the ORIGINAL file and the DRIVER'S env (UTF-8), and the conductor was not called",
                 (released, driver.calls), ([("S5-qa-x-1", {"words_file": str(driver.task_root / rel), "env": driver.env})], []))
        check_not_in("N7: the token is not filed into pending_words", "restart", json.dumps(driver.state["pending_words"]))
        row = jsonl(task_root / "state" / "driver-answers.jsonl")[-1]
        check_eq("N7: the driver-answers row has the token", row["token"], "restart")
        check_eq("N7: and the file of that very answer", (task_root / row["words_file"]).read_bytes(), b"restart\r\n")
        check_eq("N7: the question is closed", driver.state["asked"], {})
    finally:
        harness.cleanup(root)


def n7a_a_lone_cr_still_makes_one_words_file() -> None:
    """F-3: the file is NAMED by the seam, not worked out from the text: a lone CR (which `take_answer` reads as a newline) is
    where the old string comparison failed and a second file was written."""
    raw = b"a\rb"
    root, task_root, driver = logged_rig()
    try:
        seen = []
        driver.conductor = story_run.Driver.conductor.__get__(driver)
        driver.step = lambda *a, **k: "next: nothing"
        driver.run_claude = lambda kind, prompt, **k: (seen.append(prompt), {"result": '{"action": "continue", "did": "d"}', "session_id": "s",
                                                                             "stderr": "", "total_cost_usd": 0, "num_turns": 1})[1]
        driver.ask(story_run.Person("conductor", "What should happen at the plan stage?", "S5", "S5-qa-x-1"))
        check_eq("N7a: a lone-CR answer is taken", take(driver, answer(task_root, "cr.md", raw)), None)
        files = sorted(path for path in (task_root / "state" / "words").glob("*") if path.is_file())
        check_eq("N7a: ONE words file is written, with the raw bytes", [path.read_bytes() for path in files], [raw])
        row = jsonl(task_root / "state" / "driver-answers.jsonl")[-1]
        check("N7a: the prompt names it", len(seen) == 1 and str(driver.task_root / row["words_file"]) in seen[0], str(seen[:1])[:300])
        check_eq("N7a: and the driver-answers row names the same file", (task_root / row["words_file"]).resolve(), files[0].resolve())
    finally:
        harness.cleanup(root)


def n7b_tokens_by_code() -> None:
    root, task_root, driver = logged_rig(answers=[verdict(), {"action": "continue", "did": "took the move"}])
    try:
        seam_asked(driver)
        check_eq("N7b: `retry` goes back to where, no conductor", (take(driver, answer(task_root, "t1.md", b"retry")), driver.calls), (None, []))
        check("N7b: and is recorded as the person's answer", any("human_answer" in a for a in driver.logged))
        seam_asked(driver)
        person = take(driver, answer(task_root, "t2.md", b"stop"))
        check("N7b: `stop` brings the question back changed (exit 3), tokens kept, nothing called",
              person is not None and "You said to stop" in person.text and person.offered == ("retry", "stop") and not driver.calls)
        head = person.text.split("\n\n")[0]
        check_in("N7b: the stop re-ask names the offered token minus `stop`", "answer `retry`.", head)
        check_not_in("N7b: and not a token the question did not offer", "`go on`", head)
        seam_asked(driver, (("retry", "person_does"), ("go on", "go_on_as_is"), ("stop", "stop_here")))
        head = take(driver, answer(task_root, "t2b.md", b"stop")).text.split("\n\n")[0]
        check_in("N7b: with three offered tokens it names the two others", "answer `retry` or `go on`.", head)
        seam_asked(driver)
        person = take(driver, answer(task_root, "t3.md", b"go on"))
        check("N7b: a standing word the question did not offer is not a token: the seam reads it as words",
              person is not None and len(driver.calls) == 1 and driver.calls[0]["words"] == "go on")
        driver.calls.clear()
        waivers = []
        inner = driver.py
        driver.py = lambda script, *a, **k: (waivers.append(a), (0, ""))[1] if script == "waiver.py" else inner(script, *a, **k)
        seam_asked(driver, (("retry", "person_does"), ("go on", "go_on_as_is")), block="stand not confirmed")
        check_eq("N7b: `go on` with a block code knows runs waiver.py by code",
                 (take(driver, answer(task_root, "t4.md", b"go on\r\n")), driver.calls), (None, []))
        flat = list(waivers[0]) if waivers else []
        check("N7b: with the block and the file of THIS answer", "--block" in flat and "stand not confirmed" in flat and "--words-file" in flat
              and Path(flat[flat.index("--words-file") + 1]).read_bytes() == b"go on\r\n", str(flat))
        waivers.clear()
        seam_asked(driver, (("retry", "person_does"), ("go on", "go_on_as_is")), block="")
        check("N7b: `go on` with no block known is the conductor's (chosen), never a waiver by code",
              take(driver, answer(task_root, "t5.md", b"go on")) is None and not waivers and len(driver.calls) == 1)
        driver.calls.clear()
        driver.pipeline = lambda: {"stages": {"S5": {"status": "done"}}}
        seam_asked(driver, (("retry", "person_does"), ("restart", "release_and_restart")))
        logged = len(driver.logged)
        check_eq("N7b: a token at a stage that is already done is recorded and moves nothing",
                 (take(driver, answer(task_root, "t6.md", b"restart")), driver.calls), (None, []))
        check("N7b: it is recorded as the person's answer", len(driver.logged) > logged and "human_answer" in driver.logged[-1])
    finally:
        harness.cleanup(root)


def n7c_a_delivery_flag_cannot_capture_a_seam_answer() -> None:
    root, task_root, driver = logged_rig(answers=[verdict()])
    try:
        driver.state["delivery_question"] = True
        seam_asked(driver, stage="S8")
        person = take(driver, answer(task_root, "d.md", b"no delivery"))
        check("N7c: `no delivery` to a seam question at S8 is not the delivery branch's: no declined mark, the seam read the words",
              person is not None and "delivery" not in driver.state and len(driver.calls) == 1)
    finally:
        harness.cleanup(root)


def n8_by_hand_becomes_an_option() -> None:
    root, task_root, driver = logged_rig(answers=[verdict(), {"action": "ask_person", "did": "x", "question": "What now?"}])
    try:
        receipt = "state/environment-jobs/job-1.json"
        (task_root / receipt).parent.mkdir(parents=True, exist_ok=True)
        (task_root / receipt).write_text(json.dumps({"idempotency_key": "k-1"}), encoding="utf-8")
        inner = driver.py
        driver.py = lambda script, *a, **k: (0, json.dumps({"status": "blocked", "settled": False, "uncertain_process": True,
                                                            "job": {"steps": [{"name": "build", "status": "running"}], "phase": "up"}})
                                             ) if script == "environment_preparation.py" else inner(script, *a, **k)
        def job_question():
            try:
                driver.environment_job({"job_id": "job-1", "receipt_ref": receipt, "stage": "S5"})
            except story_run.Person as raised_person:
                return raised_person
        person = job_question()
        check("N8: the uncertain-process job ends in a closed question of kind environment",
              person is not None and person.kind == "environment" and {"retry", "stop"} <= set(person.offered))
        prompt = driver.calls[0]["text"]
        check("N8: the conductor reads the site's own account (the lead) BEFORE the moves section",
              "did NOT start it again" in prompt and "the process that owned it is gone" in prompt
              and prompt.index("did NOT start it again") < prompt.index("## Moves open here"), prompt[:300])
        path = f"qa-factory/artifacts/QA-9/{receipt}"
        check("N8: the options came back without the record path: the person's question keeps the lead above them",
              path in person.text and "did NOT start it again" in person.text
              and person.text.index("did NOT start it again") < person.text.index("## What each answer costs and does"))
        check_not_in("N8: the body carries no `reconcile`", "reconcile", person.text)
        check_not_in("N8: and no `.py`", ".py", person.text)
        check_in("N8: the command is in answer_note", "reconcile", person.answer_note)
        # the conductor's second answer has no options: the fallback shows the factory's own sentences (the lead) as the body
        fallback = job_question()
        check("N8: with no usable conductor answer the body (the lead) still carries no command",
              fallback is not None and list(fallback.offered) == ["retry", "go on", "stop"] and "did NOT start it again" in fallback.text
              and "reconcile" not in fallback.text and ".py" not in fallback.text, repr(fallback and fallback.text[:300]))
        check_in("N8: and the command is in answer_note", "reconcile", fallback.answer_note)
        driver.ask(person)
        shown = (driver.state_dir / "driver-question.md").read_text(encoding="utf-8")
        body, _, block = shown.partition("\n---\nAnswer:")
        check("N8: the question body has no command (no `reconcile`, no `.py`)", "reconcile" not in body and ".py" not in body)
        check("N8: the answer block carries the answer command and the probe command", "--answer" in block and "reconcile" in block and "--probe" in block)
    finally:
        harness.cleanup(root)


def n8b_the_lead_is_shown_only_when_the_prose_drops_a_kept_fact() -> None:
    path = "qa-factory/artifacts/QA-9/state/job.json"
    state = {"why": "by_hand", "kind": "environment", "stage": "S5", "text": "d", "keep": [path],
             "lead": f"THE FACTORY SAW a stopped job.\n- the record: {path}"}
    cases = [("the prose names the kept path", verdict(question=f"What now? `retry` or `stop`? The record is {path}."), state, False),
             ("the prose drops it", verdict(), state, True),
             ("the site kept nothing", verdict(), dict(state, keep=[]), False),
             ("a stop that drops it", verdict(action="stop"), state, True)]
    for label, answer_verdict, case_state, shown in cases:
        root, task_root, driver = rig(answers=[answer_verdict])
        try:
            driver.boundary = "S5:x"
            _, person = raised(driver, case_state)
            check_eq(f"N8b {label}: the lead is shown above the conductor's question", "THE FACTORY SAW" in person.text, shown)
            if shown:
                check("N8b: and it comes first", person.text.startswith("THE FACTORY SAW")
                      and person.text.index("THE FACTORY SAW") < person.text.index("What should happen?"))
        finally:
            harness.cleanup(root)


def n10_infra_inside_the_call_is_an_exit() -> None:
    root, task_root, env = seed("QA-9")
    driver = driver_for(root, env, "QA-9")
    try:
        def down(text, *, words="", files=None, words_file=None):
            raise story_run.InfraStop("auth", "the login is gone")
        driver.conductor = down
        driver.where = lambda: (_ for _ in ()).throw(story_run.Refusal("the moon is down"))
        code = driver.run()
        check_eq("N10: an InfraStop inside the conductor call is exit 5", code, story_run.EXIT_INFRA)
        check("N10: and no question file", not (driver.state_dir / "driver-question.md").exists())
        check_eq("N10: nothing is asked, the seam is free again", (driver.state.get("asked") or {}, driver._in_no_move), ({}, False))
    finally:
        harness.cleanup(root)


def n11_a_refusal_outside_guarded_is_a_question() -> None:
    root, task_root, env = seed("QA-9")
    first = driver_for(root, env, "QA-9")
    try:
        person = story_run.Person("environment", "Which stand should the story use?", "S5")
        person.stand_stage = "S5"
        first.ask(person)
        reply = answer(task_root, "stand.md", b"Local\r\n")
        driver = driver_for(root, env, "QA-9", answer=str(reply))
        driver.stand_names = lambda: ["Local"]
        inner = driver.py

        def py(script, *a, check=False, expect=""):      # C1-7c Q-3: the real `py`'s signature; a G site's `expect` is forwarded
            if script == "stage_done.py" and check:
                raise (story_run.gate_refusal(script, 1, "the pipeline is locked", expect) if expect else
                       story_run.Refusal("stage_done.py --task QA-9 (exit 1): the pipeline is locked", retry=None))
            return inner(script, *a, check=check, expect=expect)
        driver.py = py
        code = driver.run()
        check_eq("N11: a Refusal raised by py(check=True) inside take_answer is exit 3 (a question), not a traceback", code, story_run.EXIT_PERSON)
        shown = (driver.state_dir / "driver-question.md").read_text(encoding="utf-8")
        check_in("N11: the question file carries the priced options", "## What each answer costs and does", shown)
        check_not_in("N11: and not the refusal's own words", "pipeline is locked", shown)
        check_in("N11: those stay in the details file", "pipeline is locked", (driver.state_dir / "driver-question-details.md").read_text(encoding="utf-8"))
        check_eq("N11: asked carries what the seam offered", driver.state["asked"]["offered"], ["retry", "go on", "stop"])
        asked = driver.state["asked"]
        check("N11: asked.words_file names the file of the answer the refusal came out of, which holds its raw bytes",
              bool(asked.get("words_file")) and (task_root / asked["words_file"]).read_bytes() == b"Local\r\n", str(asked.get("words_file")))
        rows = jsonl(task_root / "state" / "driver-answers.jsonl")
        check_eq("N11: the person's word is on the record (one row: the words, no token, that very file)",
                 [(row["words"], row["token"], row["words_file"]) for row in rows], [("Local", "", asked["words_file"])])
        check_eq("N11: an answer already on the record is not settled twice", (driver.settle_unread_answer(), len(jsonl(task_root / "state" / "driver-answers.jsonl"))), ("", 1))
    finally:
        harness.cleanup(root)


def n12_unreadable_conductor_answer() -> None:
    root, task_root, driver = logged_rig(answers=[{"action": "_unreadable", "did": "", "question": ""}])
    try:
        driver.boundary = "S5:x"
        _, person = raised(driver, {"why": "refusal", "text": "t"})
        check_eq("N12: an unreadable answer renders the fallback", list(person.offered), ["retry", "go on", "stop"])
        check_eq("N12: with exactly one defect_found", len(driver.defects), 1)
    finally:
        harness.cleanup(root)
    root, task_root, driver = logged_rig(answers=[{"action": "_unreadable", "did": "", "question": ""}])
    try:
        driver.boundary = "S8:answer"
        result, person = raised(driver, {"why": "unread_answer", "kind": "gate_B", "stage": "S8", "text": "t", "words": "w"})
        check_eq("N12 (flipped by C1-4b): at a gate kind it is the gate fallback `retry` / `stop` (one defect_found), never raw output "
                 "as a question and no longer a silent `continue`",
                 (result, person.kind, list(person.offered), len(driver.defects)), (None, "gate_B", ["retry", "stop"], 1))
    finally:
        harness.cleanup(root)
    root, task_root, driver = logged_rig()
    try:
        driver.conductor = story_run.Driver.conductor.__get__(driver)
        driver.step = lambda *a, **k: "next: nothing"
        driver.run_claude = lambda kind, prompt, **k: {"result": "I looked at it for a long while and wrote no line of json.", "session_id": "s",
                                                       "stderr": "", "total_cost_usd": 0, "num_turns": 1}
        got = driver.conductor("r")
        check_eq("N12: Driver.conductor with no JSON line answers `_unreadable` with no question (the raw end is not a question)",
                 (got["action"], got["question"]), ("_unreadable", ""))
    finally:
        harness.cleanup(root)


def n12b_the_defect_row_reaches_the_real_journal() -> None:
    """t-668: `log_append` requires `ref` for `defect_found`; the seam's call carried none and the rejection was ignored, so no row was
    ever written. No stub on `log_append` here: the REAL script writes the row into the task's journal."""
    for site, state in (("the fallback", {"why": "refusal", "text": "t", "dispatch": "S5-qa-x-1"}),
                        ("the fallback with no dispatch", {"why": "refusal", "text": "t"}),
                        ("a gate kind", {"why": "unread_answer", "kind": "gate_B", "stage": "S8", "dispatch": "S8-gate", "text": "t", "words": "w"}),
                        ("a gate kind with no dispatch", {"why": "unread_answer", "kind": "gate_B", "stage": "S8", "text": "t", "words": "w"})):
        root, task_root, env = seed("QA-9")
        driver = driver_for(root, env, "QA-9")
        driver.conductor = lambda text, **k: {"action": "_unreadable", "did": "", "question": ""}
        driver.no_move_facts = lambda state: dict(FACTS)
        try:
            driver.boundary = "S8:answer"
            err = io.StringIO()
            with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
                raised(driver, state)
            rows = [r for r in jsonl(root / "qa-factory" / "records" / "journal.jsonl") if r.get("event") == "defect_found"]
            check_eq(f"N12b {site}: exactly one defect_found row in the real journal", len(rows), 1)
            row = rows[0] if rows else {}
            check(f"N12b {site}: the row has a non-empty ref and the factory's owner mark",
                  bool(row.get("ref")) and str(row.get("notes", "")).startswith("owner: factory"), str(row))
            check_eq(f"N12b {site}: ref = the state's dispatch, else the boundary", row.get("ref"), state.get("dispatch") or "S8:answer")
            check_eq(f"N12b {site}: nothing was rejected, so nothing is said on stderr", err.getvalue(), "")
        finally:
            harness.cleanup(root)
    # a journal that rejects the write is said once on stderr and the run goes on
    root, task_root, env = seed("QA-9")
    driver = driver_for(root, env, "QA-9")
    try:
        driver.py = lambda script, *a, **k: (1, "JOURNAL: record rejected:\n- event 'defect_found' requires field 'ref'")
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            driver.file_defect("", "owner: factory — x")
        lines = err.getvalue().splitlines()
        check("N12b: a rejected write is one stderr line naming the rejection and does not raise",
              len(lines) == 1 and "requires field 'ref'" in lines[0], err.getvalue())
    finally:
        harness.cleanup(root)


def n13_a_megabyte_answer() -> None:
    root, task_root, driver = rig()
    try:
        big = "x" * 1_000_000
        driver.conductor = story_run.Driver.conductor.__get__(driver)
        driver.step = lambda *a, **k: "next: nothing"
        seen = []
        driver.run_claude = lambda kind, prompt, **k: (seen.append(prompt), {"result": '{"action": "continue", "did": "d"}', "session_id": "s",
                                                                             "stderr": "", "total_cost_usd": 0, "num_turns": 1})[1]
        driver._answer = {"text": big, "rel": None}
        driver.conductor("r", words=big, words_file=driver.answer_file())
        check("N13: a 1 MB answer: the prompt is cut at the limit", len(seen[0]) < story_run.NO_MOVE_WORDS_IN_PROMPT + 40000, str(len(seen[0])))
        check_eq("N13: and the words file holds all of it", len((task_root / driver.answer_file()).read_bytes()), 1_000_000)
    finally:
        harness.cleanup(root)


def n14_price_labels_that_cannot_be_read() -> None:
    real = human_text.rules()
    for count in (0, 1, 2):
        short = dict(real, price_lines={"labels": real["price_lines"]["labels"][:count]})
        try:
            human_text.price_labels(short)
            raised_it = False
        except human_text.LabelsUnreadable:
            raised_it = True
        check(f"N14: price_labels with {count} of the 3 labels raises", raised_it)
    try:
        human_text.price_labels({k: v for k, v in real.items() if k != "price_lines"})
        raised_it = False
    except human_text.LabelsUnreadable:
        raised_it = True
    check("N14: a rules file with no price_lines raises too", raised_it)
    check_eq("N14: and the three labels are returned whole", human_text.price_labels(real), ["the factory:", "you:", "the story:"])
    short = dict(real, price_lines={"labels": ["the factory:", "you:"]})
    check_eq("N14: price_problems (a detector) never raises on the same data", human_text.price_problems("(a) `retry` - x", ["retry"], short), [])
    original = human_text.rules
    for label, answers, state in (("the fallback", [], {"why": "refusal", "call": False, "text": "t"}),
                                  ("the conductor's own options", [verdict()], {"why": "refusal", "text": "t"})):
        root, task_root, driver = rig(answers=answers)
        try:
            driver.boundary = "S5:x"
            human_text.rules = lambda: short
            try:
                _, person = raised(driver, state)
            finally:
                human_text.rules = original
            check_eq(f"N14 {label}: unreadable labels end in the last-resort question (the three standing words)",
                     list(person.offered), ["retry", "go on", "stop"])
            check_not_in(f"N14 {label}: with no half-priced options", "## What each answer costs and does", person.text)
            check(f"N14 {label}: and exactly one defect_found", len(driver.defects) == 1, str(driver.defects))
        finally:
            human_text.rules = original
            harness.cleanup(root)


def n15_a_gave_up_stop_files_the_free_answer_for_its_dispatch() -> None:
    for boundary, expected in (("S5:S5-qa-code-critic-2", "S5-qa-code-critic-2"), ("gate_A", "")):
        root, task_root, env = seed("QA-9")
        driver = driver_for(root, env, "QA-9")
        try:
            def give_up():
                driver.boundary = boundary
                raise story_run.Stop(story_run.EXIT_GAVE_UP, "the conductor gave up on this step")
            driver.where = give_up
            with contextlib.redirect_stdout(io.StringIO()):
                code = driver.run()
            check_eq(f"N15 {boundary}: the exit code is the gave-up one", code, story_run.EXIT_GAVE_UP)
            check_eq(f"N15 {boundary}: the question names the dispatch of the boundary (a free answer is filed for it)",
                     driver.state["asked"].get("dispatch"), expected)
        finally:
            harness.cleanup(root)


SITE_Q = "Which of these should happen? `read` or `stop`?"


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


def _site_ok(doors, spec, normalize) -> bool:
    try:
        NM.site_check(doors, spec, normalize)
        return True
    except NM.DataUnreadable:
        return False


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


def main() -> None:
    for scenario in (rd1_20_the_s8_summary_run_has_its_door, cc15_the_offers_of_a_stage_closed_by_code, k4_the_refusal_is_read_as_its_problems, el12_site_doors_are_not_moves, n_next_the_repair_limit_doors_are_not_moves, n_next_the_s7_doors_are_never_a_move_word, el16_the_prose_names_no_extra_token, el16b_edges_of_the_prose_reader,
n22_the_gate_raised_again_over_an_open_seam_question, n23_a_conductor_continue_at_a_gate_shows_the_gate_again,
                     n21_keep_at_the_stuck_threshold,n16_site_doors, n17_site_fallback, n18_package_unread, n19_ticket_changed_unread, n20_the_funnel_reads_new_words,n1_one_why_at_a_time, n2_the_filter, n2b_the_facts_are_read_from_the_project, n2c_the_stages_a_rework_may_name, n3_options_authoritative, n4_the_cap,
                     n5_gate_kinds_carry_their_moves, n5c_approve_is_open_only_at_a_gate_with_no_decision, n5b_a_token_never_reaches_a_gate_recorder, n6_s1_review_keeps_today,
                     n7_the_words_file_round_trip, n7a_a_lone_cr_still_makes_one_words_file, n7b_tokens_by_code, n7c_a_delivery_flag_cannot_capture_a_seam_answer,
                     n8_by_hand_becomes_an_option, n9_edges_and_ties, n10_infra_inside_the_call_is_an_exit,
                     n11_a_refusal_outside_guarded_is_a_question, n12_unreadable_conductor_answer, n12b_the_defect_row_reaches_the_real_journal,
                     n13_a_megabyte_answer,
                     n8b_the_lead_is_shown_only_when_the_prose_drops_a_kept_fact, n14_price_labels_that_cannot_be_read,
                     n15_a_gave_up_stop_files_the_free_answer_for_its_dispatch):
        scenario()
    harness.finish("no_move seam")


# --- t-764 (C1-5d2, EL12 on the REAL data): ONE block, at the end of the file ---------------------------------------------------------------------


def el12_the_exit_limit_questions_own_doors_are_no_moves_word() -> None:
    """EL12: the doors of the question that really is raised (`exit.resume_limit` of question-prices.json, read directly; the seam's offer is pinned to it in test_story_run_exit_limit.py EL1) are
    read through the seam's door check as the Driver passes them (`site_doors`: every answer that is not a standing token). `fresh`, not
    `restart`: `restart` is the token of the move `release_and_restart`, and a site door that is a move's word is refused (G7)."""
    normalize, spec = story_run.Driver.s0_normalize, NM.data()
    answers = [row["answer"] for row in NM.load_question_prices()["exit.resume_limit"]]
    check_eq("EL12 (data): the question's answers, read from the data itself, in order", answers, ["round", "fresh", "go on", "stop"])
    doors = tuple(t for t in answers if t not in NM.TOKEN_MOVES)
    check_eq("EL12 (data): its site doors are round and fresh (go on and stop are standing tokens)", doors, ("round", "fresh"))
    check("EL12 (data): and the seam accepts them as doors - none is a move's word", _site_ok(doors, spec, normalize))
    renamed = tuple("restart" if t == "fresh" else t for t in doors)
    check("EL12 negative control: the same door check refuses `fresh` renamed `restart`", not _site_ok(renamed, spec, normalize))


# --- t-835 (C2-5s, class K4): the driver's record of the standing refusal: ONE block at the end of the file ----------------------------------------------------

CTRL_BODY = ("the qa-code-critic window is not receipted: no review receipt for TC-1; no window record for TC-2: the probe receipt cannot be read. "
             "These are the review's own receipts, not the person's to produce. If a person accepts the window without them: "
             "`waiver.py --task QA-9 --stage S5 --block \"not receipted\" --words-file <file>`.")
CTRL_REFUSAL = "story_step finish S5-qa-code-critic-1 (exit 3):\n" + CTRL_BODY


def k4s_rig(answers=None):
    root, task_root, driver = rig(answers=answers)
    return root, task_root, driver, task_root / "state" / "standing-refusal.json"


def k4s_fresh(driver, state):
    """`raised` on a fresh boundary: the per-boundary cap of conductor calls is not under test here."""
    driver.conductor_calls = {}
    return raised(driver, state)


def k4s_record(path):
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else None


def k4s_state(lines, **extra):
    return dict({"why": "refusal", "kind": "refusal", "call": False, "stage": "S5", "dispatch": "", "lead": "The step was refused.",
                 "text": CTRL_REFUSAL, "lines": lines}, **extra)


def k4s_lines_are_the_readers() -> None:
    """q1 (t-782): `refusal_lines` is the C2-1 reader (`DV.refusal_text` transport, `DV.split_items`) then `waiver.refusal_parts` - no second stripper."""
    import waiver
    lines = story_run.Driver.refusal_lines(story_run.Refusal(CTRL_REFUSAL))
    check_eq("K4s: the controller's joined problems come out apart, the header of the driver cut, the first one whole", lines[0],
             "the qa-code-critic window is not receipted: no review receipt for TC-1")
    check("K4s (negative pin, finding 9): the door in backticks is in no line - 'waiver.py --task' is nowhere", all("waiver.py --task" not in l for l in lines), str(lines))
    head = "2 problems - the request is refused whole, every one is listed:"
    check_eq("K4s: a combined refusal is read by its head (C2-1), the number cut", story_run.Driver.refusal_lines(
        story_run.Refusal("story_step: refused - " + head + "\n1) alpha\n2) beta")), ["alpha", "beta"])
    check_eq("K4s: ...the JSON transport of `--operation decision` is taken off first", story_run.Driver.refusal_lines(
        story_run.Refusal(json.dumps({"error": head + "\n1) alpha\n2) beta"}))), ["alpha", "beta"])
    check_eq("K4s: ...an item that goes on over several lines stays ONE item", story_run.Driver.refusal_lines(
        story_run.Refusal(head + "\n1) alpha\n   with more\n2) beta")), ["alpha\n   with more", "beta"])
    check_eq("K4s: the raiser's own findings win; `items` win over them", (story_run.Driver.refusal_lines(story_run.Refusal("x\ny", findings=["f1; f2"])),
             story_run.Driver.refusal_lines(story_run.Refusal("x\ny", findings=["f1"]), items=["i1"])), (["f1", "f2"], ["i1"]))
    check_eq("K4s edge: one line of text has no 'below the first line': the text whole", story_run.Driver.refusal_lines(story_run.Refusal("just this")), ["just this"])
    check_eq("K4s edge: all door in backticks normalises to nothing and is returned as it is (never empty, exit_limit needs a line)",
             story_run.Driver.refusal_lines(None, items=["`waiver.py --task QA-1`"]), ["`waiver.py --task QA-1`"])
    check_eq("K4s: the same normalisation as the writer's (one builder)", story_run.Driver.refusal_lines(None, items=[CTRL_BODY]), waiver.refusal_parts([CTRL_BODY]))


def k4s_the_writer() -> None:
    import waiver
    root, task_root, driver, path = k4s_rig()
    lines = story_run.Driver.refusal_lines(story_run.Refusal(CTRL_REFUSAL))
    check_eq("K4s: the record is where the reader reads it", path.resolve(), waiver.standing_path("QA-9").resolve())
    _, person = raised(driver, k4s_state(lines))
    check("K4s: the seam raised its Person", person is not None)
    record = k4s_record(path)
    check_eq("K4s: a seam entry with `lines` writes the record: stage, lines, doors - exactly those", (sorted(record), record["stage"], record["lines"], record["doors"]),
             (["doors", "lines", "stage"], "S5", lines, ["not receipted"]))
    check("K4s (axis 8): the record carries no absolute path", str(root) not in path.read_text(encoding="utf-8"))
    check("K4s: a Person raised - the record LIVES with the open question (it is not erased)", path.is_file())
    raised(driver, k4s_state(["a different problem"], stage="S5", text="no door here"))
    check_eq("K4s: a second refusal REPLACES the record (never merged); no door line: doors []", k4s_record(path), {"stage": "S5", "lines": ["a different problem"], "doors": []})
    raised(driver, k4s_state(["another stage's problem"], stage="S6"))
    check_eq("K4s: ...also when it is another stage's", (k4s_record(path)["stage"], k4s_record(path)["lines"]), ("S6", ["another stage's problem"]))
    many = [f"problem {n}" for n in range(1, 26)]
    raised(driver, k4s_state(many))
    check_eq("K4s edge: a list of 25 is recorded WHOLE (the ceiling 20 is the listing's, not the record's)", len(k4s_record(path)["lines"]), 25)
    driver._in_no_move = True
    raised(driver, k4s_state(["from inside the seam"]))
    driver._in_no_move = False
    check_eq("K4s: a call from INSIDE the seam never rewrites the outer one's record", k4s_record(path)["lines"], many)
    for why, extra in (("unread_answer", {}), ("chosen", {"token": "go on", "move": "go_on_as_is"}), ("by_hand", {}), ("stop", {})):
        raised(driver, {"why": why, "kind": "conductor", "stage": "S5", "dispatch": "", "text": "t", "call": False, **extra})
        check_eq(f"K4s: why={why} carries no `lines` and leaves the record as it was", k4s_record(path)["lines"], many)
    raised(driver, k4s_state([]))
    check_eq("K4s edge: an empty `lines` is not written (the old record is the old refusal's, untouched)", k4s_record(path)["lines"], many)
    driver.dry = True
    raised(driver, k4s_state(["dry"]))
    check_eq("K4s: a dry run writes nothing ...", k4s_record(path)["lines"], many)
    driver.drop_standing()
    check("K4s: ... and erases nothing", path.is_file())
    driver.dry = False
    pipeline = task_root / "pipeline.json"
    base = json.loads(pipeline.read_text(encoding="utf-8"))
    pipeline.write_text(json.dumps(dict(base, stages={"S4": {"status": "done"}, "S5": {"status": "running"}})), encoding="utf-8")
    raised(driver, k4s_state(["funnel"], stage=""))
    check_eq("K4s: with no stage (`funnel`) the ONE running stage of pipeline.json is the record's", (k4s_record(path)["stage"], k4s_record(path)["lines"]), ("S5", ["funnel"]))
    pipeline.write_text(json.dumps(dict(base, stages={"S5": {"status": "running"}, "S6": {"status": "running"}})), encoding="utf-8")
    raised(driver, k4s_state(["two running"], stage=""))
    check("K4s edge: two running stages - the stage is unknown: no record, and the old one goes (FR-59)", not path.is_file())
    raised(driver, k4s_state(["no running"], stage="where"))
    check("K4s edge: a stage that is no stage id - no record", not path.is_file())


def k4s_the_erasers() -> None:
    root, task_root, driver, path = k4s_rig([{"action": "continue", "did": "moved"}, {"action": "retry", "did": "again"}])
    stand = lambda: path.write_text(json.dumps({"stage": "S5", "lines": ["x"], "doors": []}), encoding="utf-8")   # noqa: E731
    stand()
    result, _ = raised(driver, k4s_state(["y"], call=True))
    check_eq("K4s E1: the conductor `continue` returns", result, "continue")
    check("K4s E1: ... and the record is erased", not path.is_file())
    stand()
    result, _ = raised(driver, k4s_state(["y"], call=True))
    check_eq("K4s E1: `retry` too", (result, path.is_file()), ("retry", False))
    stand()
    driver.guarded(lambda: None, {"stage": "S5"})
    check("K4s E2: a step that went through erases the record (it does not outlive its stage)", not path.is_file())
    stand()
    calls = []
    driver.handle_refusal = lambda refusal, **k: "retry"
    driver.guarded(lambda: (_ for _ in ()).throw(story_run.Refusal("again", retry=lambda: calls.append(1))), {"stage": "S5"})
    check_eq("K4s E2: a retried step that went through erases it too", (calls, path.is_file()), ([1], False))
    stand()
    seam_asked(driver)
    check("K4s: ask() leaves the record (the question about the refusal is open)", path.is_file())
    check("K4s E3: the answer closes the question and erases the record", take(driver, answer(task_root, "a.txt", b"retry")) is None and not path.is_file())
    stand()
    driver.state["asked"] = {}
    driver.reconcile_question()
    check("K4s E4: no question open at start - the record a crash left is erased", not path.is_file())
    stand()
    seam_asked(driver)
    driver.reconcile_question()
    check("K4s E4: ... a question that IS open keeps it", path.is_file())
    stand()
    driver.dry = True
    driver.guarded(lambda: None, {"stage": "S5"})
    check("K4s: dry run - no eraser acts", path.is_file())


def k4s_the_go_on_note() -> None:
    import waiver
    root, task_root, driver, path = k4s_rig([verdict(), verdict(), verdict()])
    chosen = {"why": "chosen", "kind": "conductor", "stage": "S5", "dispatch": "", "token": "go on", "move": "go_on_as_is", "text": "t", "words_file": "", "block": ""}
    k4s_fresh(driver, chosen)
    check_in("K4s 3.4: with no record the note says so and names the door", "No refusal is recorded as standing here; if their words pass nothing, keep them with --remark.", driver.calls[-1]["text"])
    path.write_text(json.dumps({"stage": "S5", "lines": ["first problem", "second problem"], "doors": []}), encoding="utf-8")
    k4s_fresh(driver, chosen)
    note = driver.calls[-1]["text"]
    check_in("K4s 3.4: the record's lines are the closed list, numbered", "  1. first problem\n  2. second problem", note)
    check_in("K4s 3.4: ... one --block per line, the line whole; the writer refuses any other", "one waiver.py --block per line, the line whole", note)
    check_in("K4s 3.4: ... and says waiver.py refuses a block in none of them", "waiver.py refuses a block that is in none of them.", note)
    path.write_text(json.dumps({"stage": "S5", "lines": [f"problem {n}" for n in range(1, 22)], "doors": []}), encoding="utf-8")
    k4s_fresh(driver, chosen)
    note = driver.calls[-1]["text"]
    check_in("K4s 3.4 edge: 21 lines - the 20th whole, the ceiling named with the file", "  20. problem 20\n  (+1 more: " + str(waiver.standing_path("QA-9")) + ")", note)
    check_not_in("K4s 3.4 edge: ... and the 21st is not listed", "  21. problem 21", note)
    k4s_fresh(driver, dict(chosen, stage="S6"))
    check_in("K4s 3.4 edge: a record of ANOTHER stage is no record here", "No refusal is recorded as standing here", driver.calls[-1]["text"])
    k4s_fresh(driver, dict(chosen, move="person_does", token="retry"))
    check_not_in("K4s 3.4: the list belongs to `go on` only", "has these lines", driver.calls[-1]["text"])


def k4s_wr7_live_and_the_cross_node_pins() -> None:
    """WR7 end to end with the driver as the writer (§L-7, the dormant branch gone), and the two cross-node pins of t-778/t-782."""
    import waiver
    root, task_root, driver, path = k4s_rig()
    stage_overrides = lambda: json.loads((task_root / "pipeline.json").read_text(encoding="utf-8")).get("stage_overrides") or []   # noqa: E731
    run = lambda block: harness.run_script("waiver.py", "--task", "QA-9", "--stage", "S5", "--block", block, "--decision", "go on", cwd=root,   # noqa: E731
                                           env=dict(os.environ, CLAUDE_PROJECT_DIR=str(root)))
    done = run("some block the driver never saw")
    check_eq("K4s WR7 (before): no record - the writer records, 'not verified', never 'block lifted'", (done.returncode, len(stage_overrides()), "not verified" in done.stdout, "block lifted" in done.stdout), (0, 1, True, False))
    lines = story_run.Driver.refusal_lines(story_run.Refusal(CTRL_REFUSAL))
    raised(driver, k4s_state(lines))
    refused = run("window_record.py --review-receipt")
    check_eq("K4s WR7 (live): the driver's record is there - a block in none of its lines is REFUSED, nothing written", (refused.returncode, len(stage_overrides())), (waiver.EXIT_BAD_ARGS, 1))
    check_in("K4s WR7 (live): ... with the record's first line listed whole after the guard's (the closed options)", ". " + lines[0], refused.stderr)
    held = run("not receipted")
    check_eq("K4s WR7 (live): the door the refusal printed is recorded on its own door", (held.returncode, len(stage_overrides())), (0, 2))
    check_not_in("K4s WR7 (live): ... and not called lifted", "block lifted", held.stdout)
    part = run("no review receipt for TC-1")
    check_eq("K4s WR7 (live): a part only one line holds is recorded against the record", (part.returncode, "recorded against the refusal standing at S5" in part.stdout), (0, True))
    # cross-node pin 1 (t-778): d2's exit-limit `go on` writes one waiver row per line that REACHED the seam - raw handoff lines, whole
    whole = "case identity: a case file's `id` is its file name - 2 file(s) break that: bad.md -> `TC-2.md` with `id: TC-2`; other.md -> `TC-3.md` with `id: TC-3`. Way on: write each case again. A person's word passes this check"
    second = "journal: entry 4 has no `ts`"
    dispatch = "S5-qa-code-critic-1"
    caller_lines = story_run.Driver.refusal_lines(None, items=[whole, second])      # normalised once, by the caller (t-842 F3)
    raised_by_seam = lambda: driver.exit_limit("S5", "qa-code-critic", dispatch, caller_lines, sid="", why="handoff")   # noqa: E731
    try:
        raised_by_seam()
    except story_run.Person:
        pass
    check_eq("K4s cross-node: the exit-limit seam writes the record from the same lines (one builder)", k4s_record(path)["lines"], waiver.refusal_parts([whole, second]))
    before = len(stage_overrides())
    (task_root / "state" / "words").mkdir(parents=True, exist_ok=True)
    (task_root / "state" / "words" / "w.txt").write_text("go on", encoding="utf-8")
    driver._exit_go_on(driver.exit_record(dispatch), "S5", dispatch, "state/words/w.txt", "go on")
    check_eq("K4s cross-node (t-778 Q8): d2's `go on` rows are written against the record - one per line the caller handed the seam (here the "
             "3 parts of `refusal_lines`), every one passes it (no held question)", len(stage_overrides()) - before, len(caller_lines))
    # cross-node pin 2 (t-782 Q7): the seam's own `go on` WITH asked.block is an own-form constant - never judged against the record
    seam_asked(driver, options=(("go on", "go_on_as_is"), ("stop", "stop_here")), block=waiver.STAND_NOT_CONFIRMED_BLOCK)
    before = len(stage_overrides())
    check("K4s cross-node (t-782 Q7): `go on` with asked.block passes while the record of the stage holds other lines",
          take(driver, answer(task_root, "g.txt", b"go on")) is None and len(stage_overrides()) == before + 1)


def k4s_fix_round() -> None:
    """The fix round of t-835 (critic t-842, Lead's §L-8): F1 the window case, F2 the key, F3 the lines `exit_limit` is given."""
    import waiver
    # F1: the record carries the REAL line of the window's set, not the comparison form (`<dispatch>` for an id)
    root, task_root, driver, path = k4s_rig()
    line = "S5-qa-code-critic-1 has no review receipt for case TC-3"
    refusal = story_run.Refusal("story_step finish S5-qa-code-critic-1 (exit 3):\n" + line, dispatch="S5-qa-code-critic-1", window_findings=[line])
    driver.window_round_gate(refusal, "S5")                                   # round 1 goes to the conductor: no record
    check("K4s F1: round 1 (the conductor's) writes no record", not path.is_file())
    try:
        driver.window_round_gate(refusal, "S5")                               # the same set again: the person is asked
        raised_here = None
    except story_run.Person as person:
        raised_here = person
    check("K4s F1: the same set a second time raises the person's question", raised_here is not None)
    record = k4s_record(path)
    check_eq("K4s F1: the record carries the real line, the id in it (not `<dispatch> has no ...`)", record["lines"], [line])
    check("K4s F1 (negative control): the comparison form is a different string - the bug would have recorded it", story_run.finding_lines([line]) != [line])
    done = harness.run_script("waiver.py", "--task", "QA-9", "--stage", "S5", "--block", line, "--decision", "go on", cwd=root, env=dict(os.environ, CLAUDE_PROJECT_DIR=str(root)))
    check_eq("K4s F1: the writer ACCEPTS the real line (carrier), nothing refused", (done.returncode, "recorded against the refusal standing at S5" in done.stdout), (0, True))
    check_eq("K4s F1: the reader clears exactly that line", waiver._reads(record["lines"], "S5", line), [line])
    # F2: the key of a finding set tells two problems that differ only in a final span apart (the same function as the record's)
    two = [story_run.Driver.refusal_lines(story_run.Refusal("head:\nno test is bound to case `TC-" + n + "`")) for n in ("3", "7")]
    check("K4s F2: two refusals differing only in their final `TC-n` span have two keys", story_run.finding_key(two[0]) != story_run.finding_key(two[1]), str(two))
    # F3: `exit_limit` records the lines it is GIVEN (normalised once, by the caller); an empty list is a Person, not an AttributeError
    root, task_root, driver, path = k4s_rig()
    for label, given in (("[]", []), ("None", None)):
        try:
            driver.exit_limit("S5", "qa-code-critic", "S5-qa-code-critic-1", given, sid="", why="handoff")
            outcome = "returned"
        except story_run.Person:
            outcome = "Person"
        except Exception as exc:                                              # noqa: BLE001 - the pin names the wrong kind of failure
            outcome = type(exc).__name__
        check_eq(f"K4s F3: exit_limit(..., {label}) raises the person's question (the generic text), nothing else", outcome, "Person")
        check("K4s F3: ... and writes no record (no lines)", not path.is_file())
    raw = "x `waiver.py --a`"
    try:
        driver.exit_limit("S5", "qa-code-critic", "S5-qa-code-critic-1", [raw], sid="", why="handoff")
    except story_run.Person:
        pass
    check_eq("K4s F3: exit_limit does not normalise a second time - the record is the line it was given", k4s_record(path)["lines"], [raw])
    inputs = ["missing `a` `b`", "problem one. If a person accepts it: `waiver.py --task QA-9 --block \"x\"`.", "1) alpha; beta"]
    once = story_run.Driver.refusal_lines(None, items=inputs)
    check_eq("K4s F3: the caller's normalisation is idempotent (``missing `a` `b` `` among the inputs)", story_run.Driver.refusal_lines(None, items=once), once)
    check_eq("K4s F3: refusal_lines(None, items=[]) is no lines, the refusal is not read", story_run.Driver.refusal_lines(None, items=[]), [])


def k4s_run() -> None:
    for scenario in (k4s_lines_are_the_readers, k4s_the_writer, k4s_the_erasers, k4s_the_go_on_note, k4s_wr7_live_and_the_cross_node_pins, k4s_fix_round):
        scenario()


# --- t-856 (C2-6): the `rework` option carries "args", the token carries the person's words ------------------------------------------------------
C26_FACTS = dict(FACTS, rework_stages=["S4", "S5"], rework_roles={"S4": ["qa-case-designer"], "S5": ["qa-automator", "qa-code-critic"]},
                 scope=["TC-1", "TC-2"], causes=["test_defect", "mechanical"])
C26_ARGS = {"stage": "S5", "role": "qa-automator", "cases": ["TC-1"], "cause": "test_defect"}


def c26_option(**args) -> dict:
    return dict(seam_option("rework", "rework_stage"), args=args)


def c26_verdict(options, **extra) -> dict:
    return {"action": "ask_person", "did": "looked", "question": "Which one?", "why_person": "access", "checked": "the refusal",   # RN1-9 default class
            "options": options, **extra}


def c26_validate(options, facts=C26_FACTS, chosen=False, move=""):
    try:
        return NM.validate_options(c26_verdict(options), ["rework_stage", "person_does", "stop_here"], NM.data(), lambda s: s.strip().lower(),
                                   {}, facts=facts, chosen=chosen, chosen_move=move)[0] and "ok"
    except NM.ArgsRefused as refused:
        return "args: " + refused.rule


def c26_args_are_validated_and_carried() -> None:
    other = seam_option("retry", "person_does")
    check_eq("C26: good args pass and are kept on the option", NM.validate_options(
        c26_verdict([c26_option(**C26_ARGS), other]), ["rework_stage", "person_does"], NM.data(), lambda s: s.strip().lower(), {},
        facts=C26_FACTS)[0][0]["args"], C26_ARGS)
    bad = {"stage not listed": dict(C26_ARGS, stage="S7"), "role of another stage": dict(C26_ARGS, role="qa-case-designer"),
           "case outside scope": dict(C26_ARGS, cases=["TC-9"]), "cases and rows": dict(C26_ARGS, rows=["TS-1"]),
           "no case on S5": dict(C26_ARGS, cases=[]), "cause not listed": dict(C26_ARGS, cause="whim")}
    for label, args in bad.items():
        check(f"C26: {label} -> ArgsRefused", c26_validate([c26_option(**args), other]).startswith("args: "), c26_validate([c26_option(**args), other]))
    check("C26: no args at all -> ArgsRefused", c26_validate([seam_option("rework", "rework_stage"), other]).startswith("args: "))
    check("C26: a fact that was not read -> ArgsRefused (FR-59)", c26_validate([c26_option(**C26_ARGS), other], dict(C26_FACTS, scope=None)).startswith("args: "))
    # t-1936 F2 (Fork 3-B): `args` on a move whose column is null is DROPPED, the option kept (it was malformed, a refused answer, before)
    kept = NM.validate_options(
        c26_verdict([c26_option(**C26_ARGS), dict(other, args={"stage": "S5"})]), ["rework_stage", "person_does"], NM.data(), lambda s: s.strip().lower(), {},
        facts=C26_FACTS)[0]
    check("C26 (F2): args on another move is dropped, not ArgsRefused and not malformed: the option stays, without `args`",
          kept is not None and "args" not in kept[1] and kept[1].get("args_dropped") is True and kept[0]["args"] == C26_ARGS, str(kept))
    # the lone option (L-5, L-6 (b)): only at a chosen call for `rework`
    check_eq("C26: one rework option with good args is legal at a chosen call", c26_validate([c26_option(**C26_ARGS)], chosen=True, move="rework_stage"), "ok")
    check_eq("C26: ...not outside a chosen call", c26_validate([c26_option(**C26_ARGS)]), None)
    check_eq("C26: ...not at a chosen call of another move (L-6 b)", c26_validate([c26_option(**C26_ARGS)], chosen=True, move="go_on_as_is"), None)
    check_eq("C26: one option of another move is never legal", c26_validate([other], chosen=True, move="rework_stage"), None)
    check_eq("C26 F-4: a chosen call whose move is unknown opens no lone option (a bool and a move id, not a tri-state)", c26_validate([c26_option(**C26_ARGS)], chosen=True), None)
    listing = NM.rework_args_list(dict(C26_FACTS, scope=[f"TC-{n}" for n in range(61)]))
    for needle in ('"args" from these values only', "S5 → qa-automator | qa-code-critic", "(+1 more: state/controller.json \"scope\")", "cause: test_defect | mechanical"):
        check_in(f"C26: the closed list says {needle}", needle, listing)
    check_in("C26: the moves section carries the list, not the old stages line", "S4 → qa-case-designer", NM.moves_section(NM.data(), ["rework_stage"], C26_FACTS))


def c26_rig(answers):
    root, task_root, driver = rig(answers=answers)
    driver.no_move_facts = lambda state: dict(C26_FACTS)
    return root, task_root, driver


def c26_a_chosen_call_runs_or_asks_literally() -> None:
    chosen = {"why": "chosen", "kind": "conductor", "stage": "S5", "dispatch": "", "text": "t", "token": "rework", "move": "rework_stage",
              "says": "the automator changes the test", "words": "change the export test", "words_file": ""}
    root, task_root, driver = c26_rig([c26_verdict([c26_option(**C26_ARGS)]), c26_verdict([c26_option(**C26_ARGS)])])
    try:
        rel = driver.words_file("change the export test", "answer").relative_to(driver.task_root).as_posix()
        result, person = raised(driver, dict(chosen, words_file=rel))
        check_eq("C26: one rework option with args at a chosen call -> `continue`, no Person, the record is written",
                 (result, person, (driver.state.get("seam_rework") or {}).get("words_file")), ("continue", None, rel))
        prompt = driver.calls[0]["text"]
        check_in("C26: the prompt carries what the option says and that the words are the instruction", 'The person chose `rework` (move `rework_stage`): "the automator changes the test".', prompt)
        check_in("C26: ...and the one-option answer the code can run", "answer ask_person with exactly one option", prompt)
        check_eq("C26: ...and the conductor got the ORIGINAL words and file", (driver.calls[0]["words"], driver.calls[0]["words_file"]), ("change the export test", rel))
        driver.state.pop("seam_rework")
        # no words on file: held, no record
        _, held = raised(driver, dict(chosen, words_file=""))
        check("C26: a lone rework option with no words on file -> held, no record", held is not None and "none are on file" in held.text and "seam_rework" not in driver.state)
    finally:
        harness.cleanup(root)
    root, task_root, driver = c26_rig([c26_verdict([seam_option("retry", "person_does"), seam_option("stop", "stop_here")])])
    try:
        _, person = raised(driver, dict(chosen, words_file="x"))
        check("C26 (1): two usable options -> the person is asked, no record", person is not None and list(person.offered) == ["retry", "stop"] and "seam_rework" not in driver.state)
    finally:
        harness.cleanup(root)
    root, task_root, driver = c26_rig([{"action": "stop", "did": "x", "question": "No.", "why_person": "access", "checked": "the refusal",
                                        "options": [seam_option("retry", "person_does"), seam_option("stop", "stop_here")]}])
    try:
        _, person = raised(driver, dict(chosen, words_file="x"))
        check_eq("C26 (2): `stop` -> the story stops (exit 4), no record", (person.code, "seam_rework" in driver.state), (story_run.EXIT_GAVE_UP, False))
    finally:
        harness.cleanup(root)
    root, task_root, driver = c26_rig([c26_verdict([seam_option("retry", "person_does")]), c26_verdict([seam_option("retry", "person_does")])])
    try:
        _, person = raised(driver, dict(chosen, words_file="x"))
        check_eq("C26 (3): a malformed answer -> a defect, the conductor again with the rule, then the fallback question, no record",
                 (len(driver.calls), len(driver.defects) >= 1, "Your options were refused" in driver.calls[-1]["text"], person is not None and "seam_rework" in driver.state),
                 (2, True, True, False))
    finally:
        harness.cleanup(root)
    root, task_root, driver = c26_rig([c26_verdict([c26_option(**dict(C26_ARGS, role="nobody")), seam_option("retry", "person_does")]),
                                       c26_verdict([c26_option(**C26_ARGS), seam_option("retry", "person_does")])])
    try:
        _, person = raised(driver, dict(chosen, why="refusal", words_file="x"))
        check_eq("C26 p.4: bad args -> ONE repeat to the conductor with the rule and the closed list; the good answer is shown to the person",
                 (len(driver.calls), "did no accepted work" in driver.calls[1]["text"], '"args" from these values only' in driver.calls[1]["text"],
                  person.options[0].get("args")), (2, True, True, C26_ARGS))
    finally:
        harness.cleanup(root)


def c26_restart_refused_is_held_and_the_conductor_is_not_called() -> None:
    """t-722 §4.4 (owed pin): the controller REFUSED the release the person chose with `restart`: the question comes back held, with
    the controller's own words as its details, the same tokens; the conductor is not called and no other road releases the dispatch."""
    root, task_root, driver = logged_rig(answers=[verdict((("retry", "person_does"), ("restart", "release_and_restart")),
                                                          question="What now? `retry` or `restart`?")])
    try:
        driver.ask(story_run.Person("conductor", "What should happen at the plan stage?", "S5", "S5-qa-x-1"))
        person = take(driver, answer(task_root, "a1.md", b"start that step again, please\r\n"))
        driver.ask(person)
        driver.calls.clear()
        released = []
        real_release = story_run.waiver.run_release
        story_run.waiver.run_release = lambda task_root, dispatch, **kw: (released.append(dispatch), (1, "the controller refuses: S5-qa-x-1 is already accepted"))[1]
        try:
            held = take(driver, answer(task_root, "a2.md", b"restart\r\n"))
        finally:
            story_run.waiver.run_release = real_release
        check("C26 restart refused: the question is held, with the controller's words, the same tokens",
              held is not None and "could not be carried out, so nothing was released" in held.text
              and "is already accepted" in held.details and list(held.offered) == ["retry", "restart"], str(held))
        check_eq("C26 restart refused: the release was tried once, the conductor was not called, the question is still open",
                 (released, driver.calls, bool(driver.state["asked"])), (["S5-qa-x-1"], [], True))
    finally:
        harness.cleanup(root)


def c26_a_refused_rework_goes_to_the_conductor_through_the_seam() -> None:
    """t-722 §4.2 p.8 (owed pin): the controller refuses the rework the person chose (`ReworkRefused` in `seam_rework_step`): the record
    is dropped (nothing was registered), and the refusal reaches the CONDUCTOR through the one seam, with the refusal's words, the
    person's ORIGINAL words and file, and the closed list of what `args` may name; the conductor's options are the person's question."""
    root, task_root, driver = c26_rig([c26_verdict([c26_option(**C26_ARGS), seam_option("retry", "person_does")])])
    try:
        words = "change the export test and check the body too"
        rel = driver.words_file(words, "answer").relative_to(driver.task_root).as_posix()
        (driver.state_dir / "controller.json").write_text(json.dumps({"dispatches": {}}), encoding="utf-8")
        driver.controller_state = lambda: {"dispatches": {}}

        def refuse(*a, **k):
            raise story_run.ReworkRefused("the controller refuses the rework: S5 is not open for it")
        driver.rework = refuse
        driver.state["seam_rework"] = dict(C26_ARGS, words_file=rel, at="then", before=[])
        shown = io.StringIO()
        person = None
        try:
            with contextlib.redirect_stdout(shown):
                driver.seam_rework_step()
        except story_run.Person as raised_person:
            person = raised_person
        call = (driver.calls or [{}])[0]
        check_eq("C26 ReworkRefused: the record is dropped and the conductor was called ONCE", ("seam_rework" in driver.state, len(driver.calls)), (False, 1))
        check("C26 ReworkRefused: the call carries the refusal, the closed list and the person's original words and file",
              "S5 is not open for it" in call.get("text", "") and '"args" from these values only' in call.get("text", "")
              and (call.get("words"), call.get("words_file")) == (words, rel), str(call)[:400])
        check("C26 ReworkRefused: the conductor's options are the person's question (a Person, with `rework` offered)",
              person is not None and "rework" in person.offered, str(person))
    finally:
        harness.cleanup(root)


def c26_a_release_by_any_road_hands_its_words_to_the_relaunch() -> None:
    """t-698 §12.2.4 (owed pin; `relaunch_reason` is unchanged by C2-6): a dispatch released by the conductor's `restart` - NO exit-limit
    `fresh_line` anywhere - hands the person's words, whole, to the role that starts again; the packet's reason follows them; with no
    release and no line the old sentence stays."""
    root, task_root, driver = rig()
    try:
        closed = "S5-qa-x-1"
        driver.controller_state = lambda: {"dispatches": {closed: {"released_by_person": "start it again\r\nand read the body twice"}}}
        reason = driver.relaunch_reason({"relaunch_of": closed, "reason": "the packet's own reason"}, {})
        check("C26 relaunch: the released dispatch's words reach the role, whole, with the packet's reason after them",
              "set aside by the person" in reason and "The person's words, whole:\nstart it again\r\nand read the body twice" in reason
              and reason.index("read the body twice") < reason.index("the packet's own reason"), reason)
        driver.controller_state = lambda: {"dispatches": {closed: {}}}
        check_in("C26 relaunch negative: no release - today's line", "never reached an agent", driver.relaunch_reason({"relaunch_of": closed}, {}))
    finally:
        harness.cleanup(root)


def c26_fix_round_t873() -> None:
    """t-873 fix round: F-2 (one chosen note), F-5 (the exit code of an unusable `continue`/`retry` with options), F-7 (the own dispatch
    of a rework has an ORIGIN: the person's words by file, or the driver's `ticket_changed` reason), and the one words reader."""
    root, task_root, driver = rig()
    try:
        state = {"token": "rework", "move": "rework_stage", "says": "", "words": "change it"}
        shut, live = driver.chosen_note(state, ["person_does", "stop_here"]), driver.chosen_note(state, ["rework_stage", "person_does"])
        check("C26 F-2: a `rework` that is no longer open says so and does not order the one rework option",
              "no longer open" in shut and "exactly one option" not in shut, shut)
        check("C26 F-2: ...an open `rework` orders the one option and does not call itself closed",
              "exactly one option" in live and "no longer open" not in live, live)
        # the one words reader: `person_words.read` (CRLF kept, a BOM dropped, UTF-16 / not UTF-8 / empty / missing = lost, no file = none)
        words = task_root / "state" / "words"
        words.mkdir(parents=True, exist_ok=True)
        arrow = "→"
        files = {"crlf-bom.txt": b"\xef\xbb\xbfone\r\ntwo " + arrow.encode("utf-8"), "blank.txt": b"  \r\n\r\n", "utf16.txt": "one two".encode("utf-16"),
                 "latin1.txt": b"caf\xe9 \xff"}
        for name, raw in files.items():
            (words / name).write_bytes(raw)
        got = {name: driver.original_words({"words_file": f"state/words/{name}"}) for name in (*files, "missing.txt")}
        check_eq("C26 words reader: a BOM is dropped, CRLF and a non-ASCII sign are kept", got["crlf-bom.txt"], ("state/words/crlf-bom.txt", "one\r\ntwo " + arrow))
        check_eq("C26 words reader: blank, UTF-16, not UTF-8 and missing are the words LOST (None), never replacement characters",
                 [got[n] for n in ("blank.txt", "utf16.txt", "latin1.txt", "missing.txt")], [None] * 4)
        check_eq("C26 words reader: no file named is no words, not a loss", driver.original_words({"words_file": ""}), ("", ""))
    finally:
        harness.cleanup(root)
    for why, code in (("stop", story_run.EXIT_GAVE_UP), ("refusal", story_run.EXIT_PERSON)):
        for action in ("continue", "retry"):
            root, task_root, driver = rig(answers=[dict(verdict(), action=action)])
            try:
                driver.boundary = "S5:x"
                _, person = raised(driver, {"why": why, "text": "t"})
                check_eq(f"C26 F-5: `{action}` with options at why={why} -> the state's own exit code (what it was before C2-6)", person.code, code)
            finally:
                harness.cleanup(root)
    root, task_root, driver = c26_rig([])
    try:
        rel = driver.words_file("change the export test", "answer").relative_to(driver.task_root).as_posix()
        record = dict(C26_ARGS, cause="ticket_changed", words_file=rel, at="then", before=[])
        calls = []
        driver.rework = lambda *a, **k: calls.append((a, k)) or ("", "")
        # a `ticket_changed` rework in the controller is the driver's own (`--reason`, no `person_words`): it is NOT the record's own dispatch
        origins = {"ticket": {"stage": "S5", "repair_cause": "ticket_changed", "status": "accepted"},
                   "person": {"stage": "S5", "repair_cause": "ticket_changed", "status": "accepted", "person_words": True}}
        for origin, held, expected in (("ticket", origins["ticket"], 1), ("person", origins["person"], 0)):
            driver.state["seam_rework"] = dict(record)
            calls.clear()
            driver.controller_state = lambda held=held: {"dispatches": {"S5-qa-automator-3": held}}
            with contextlib.redirect_stdout(io.StringIO()):
                driver.seam_rework_step()
            check_eq(f"C26 F-7: the dispatch of the {origin}'s origin: the person's rework is {'still owed (run once)' if expected else 'already registered (not run)'}",
                     (len(calls), "seam_rework" in driver.state), (expected, False))
        # ... and the other way: the person's rework of S2 is not the ticket re-run's own, so the owed re-run still starts
        driver.state["ticket_rework"] = {"stages": ["S2"], "words": "new text", "at": "then", "before": []}
        driver.controller_state = lambda: {"dispatches": {
            "S2-qa-analyst-1": {"stage": "S2", "role": "qa-analyst", "status": "accepted"},
            "S2-qa-analyst-2": {"stage": "S2", "role": "qa-analyst", "repair_cause": "ticket_changed", "status": "accepted", "person_words": True}}}
        calls.clear()
        with contextlib.redirect_stdout(io.StringIO()):
            moved = driver.ticket_rework_step()
        check_eq("C26 F-7: a `ticket_changed` rework by the person's words is not taken for the ticket re-run's own", (moved, len(calls)), (True, 1))
    finally:
        harness.cleanup(root)


# --- t-834 (C1-8): the seam set A27 exempts is the seam the Driver has -------------------------------------------------------------------------


def n24_the_seam_set_is_the_seam() -> None:
    """A27 (audit_factory.NO_MOVE_SEAM) exempts the members of the seam from its census. The AST cannot see what a runtime
    `getattr` can: that each name is a function of the LIVE `Driver`. A name of the set the Driver does not have would
    exempt nothing, and a member renamed in `story_run.py` would leave a stale exemption that reads as covered."""
    import audit_factory as A
    members = sorted(A.NO_MOVE_SEAM)
    missing = [m for m in members if not callable(getattr(story_run.Driver, m.split(".", 1)[1], None))]
    check("N24: every member of A27's NO_MOVE_SEAM is a function of the live Driver (" + str(len(members)) + " members)", not missing, str(missing))
    check_eq("N24: the entries of the seam are exactly no_move, unread and funnel", sorted(A.NO_MOVE_ENTRIES), ["funnel", "no_move", "unread"])
    check("N24: every entry is a member", all("Driver." + e in A.NO_MOVE_SEAM for e in A.NO_MOVE_ENTRIES))
    integrity = [f for f in A.a27_findings(harness.PLUGIN_ROOT) if f.startswith("A27 seam") or f.startswith("A27 I-one")]
    check("N24: A27 finds no seam-integrity and no I-one finding on the live driver", not integrity, "\n".join(integrity))


# --- t-884 (C2-7): the fallback site carries the site's words (t-722 §5.1, §5.2) --------------------------------------------------------------
G27 = dict(C26_FACTS, gate="A", gate_decided=False)


def g27_state(**extra) -> dict:
    return dict({"why": "unread_answer", "kind": "gate_A", "stage": "S4", "dispatch": "", "lead": "Your answer was not read.",
                 "words_file": "state/words/driver-answer-x.txt"}, **extra)


def g27_the_fallback_question_at_a_gate() -> None:
    """§5.1: the fallback at a gate offers what has an executor and is open - `approve` (code, the original answer on file),
    `rework` (no `args`; the conductor names the stage), `retry`, `stop` - from the ONE table `GATE_OPTIONS`, the stages in the story's
    words; what is not offered is said in one line of the lead; a fact that cannot be read removes its move and is not told as a reason."""
    root, task_root, driver = rig()
    try:
        def person_for(facts, **extra):
            driver.no_move_facts = lambda state: dict(facts)
            return driver.fallback_person(g27_state(**extra))
        full = person_for(G27)
        check_eq("C27: with the answer on file and the gate open: approve / rework / retry / stop, each with its move",
                 ([(o["token"], o["move"]) for o in full.options]),
                 [("rework", "rework_stage"), ("approve", "approve_gate"), ("retry", "person_does"), ("stop", "stop_here")])
        check_eq("C27: ...and no option carries `args` (the code never picks the stage, P1)", [o for o in full.options if "args" in o], [])
        named = " or ".join(driver.stage_place(s) for s in G27["rework_stages"])
        check_in("C27: the stages slot names the stages in words, once", f"the stage the conductor names — {named} — and the stages after it up to this gate", full.text)
        check_not_in("C27: ...and no bare stage id stands alone", " S4 ", full.text.replace(driver.stage_place("S4"), ""))
        check_in("C27: the site's lead is the body", "Your answer was not read.", full.text)
        check_in("C27: the three price lines follow each option (rule 6)", "the factory:", full.text)
        for label, facts, extra, line in (
                ("no words on file", G27, {"words_file": ""}, driver.NO_APPROVE_WORDS),
                ("a step running", dict(G27, running=True), {}, "Sending a stage back is not open now: a step of the story is still running."),
                ("a delivery attempt", dict(G27, attempts=1), {}, "a delivery attempt is already recorded"),
                ("the story closed", dict(G27, closed=True), {}, "the story is closed"),
                ("no stage with accepted work", dict(G27, rework_stages=[]), {}, "no stage before this gate has accepted work to send back"),
                ("a fact that could not be read", dict(G27, running=None), {}, NM.REWORK_UNREAD),
                ("the controller state unreadable", {"gate": "A"}, {}, NM.REWORK_UNREAD)):
            person = person_for(facts, **extra)
            gone = "approve" if label == "no words on file" else "rework"
            check(f"C27 {label}: `{gone}` is not offered and the lead says why, in one line", gone not in person.offered and line in person.text
                  and "retry" in person.offered and "stop" in person.offered, str(person.offered) + person.text[:200])
        undecided = person_for(dict(G27, gate_decided=None))
        check("C27: a gate decision that cannot be read: no `approve` (FR-59)", "approve" not in undecided.offered, str(undecided.offered))
        check_not_in("C27: no stand card shown, no line about cards", "are read in this answer too", full.text)
        driver.state.setdefault("shown_gaps", {})["A"] = {"gaps": [{"id": "g"}]}
        check_in("C27: the lead names the open stand cards when the packet shown had them (one line, §6 p.21)",
                 "Your answers to the stand cards of this gate, one per line as `<case>: <word>`, are read in this answer too.", person_for(G27).text)
    finally:
        harness.cleanup(root)


def g27_the_floor_at_a_gate() -> None:
    """§5.2: the floor of a gate has `approve` only with the original answer on file and the gate open; `rework` never; the text is
    the one with or without the `approve` line."""
    root, task_root, driver = rig()
    try:
        def floor(facts, **extra):
            driver.no_move_facts = lambda state: dict(facts)
            state = g27_state(**extra)
            return driver.last_resort(state, "the floor", lead=state["lead"])
        with_words = floor(G27)
        check_eq("C27 floor: approve / retry / stop with the answer on file", [o["token"] for o in with_words.options], ["approve", "retry", "stop"])
        check_in("C27 floor: the text says what `approve` does", "`approve` — the gate is recorded as approved with the answer you gave before;", with_words.text)
        check_in("C27 floor: ...and the door to a change", "To change something, write what to change in your own words.", with_words.text)
        for label, person in (("no words file", floor(G27, words_file="")), ("gate decided", floor(dict(G27, gate_decided=True))),
                              ("decision unreadable", floor(dict(G27, gate_decided=None))), ("facts unreadable", floor({}))):
            check(f"C27 floor {label}: no `approve` in the options or the text, `rework` never",
                  list(person.offered) == ["retry", "stop"] and "`approve`" not in person.text and "rework" not in person.text, str(person.offered))
    finally:
        harness.cleanup(root)


def g27_a_rework_from_the_fallback_goes_to_the_conductor_with_the_original_words() -> None:
    """§5.1 / §6 p.29: the person answers `rework` to the fallback question: the conductor gets the ORIGINAL words and file and the line
    'Which stage, role and cases is your judgement', answers with the one `rework` option carrying args, and the record is written with
    NO second question (the person is not asked again)."""
    root, task_root, driver = c26_rig([c26_verdict([c26_option(**C26_ARGS)])])
    try:
        words = "the export test checks only the status code, check the body"
        rel = driver.words_file(words, "answer").relative_to(driver.task_root).as_posix()
        driver.no_move_facts = lambda state: dict(G27)
        with contextlib.redirect_stdout(io.StringIO()):
            driver.ask(driver.fallback_person(g27_state(words_file=rel)))
            person = take(driver, answer(task_root, "token.md", b"rework"))
        call = (driver.calls or [{}])[0]
        check_eq("C27: the token is read, no Person is raised, the conductor was called once with the original words and file",
                 (person, len(driver.calls), call.get("words"), call.get("words_file")), (None, 1, words, rel))
        check_in("C27: ...and told that the stage is its judgement", "Which stage, role and cases is your judgement", call.get("text", ""))
        check_eq("C27: the record of the rework is written with the original file", (driver.state.get("seam_rework") or {}).get("words_file"), rel)
    finally:
        harness.cleanup(root)


def rd1_19_gate_b_assert_stricter_road_is_open() -> None:
    """RD1-19: the words `_assert_stricter_how` hands a person ("tell the delivery gate in your own words") lead to the
    conductor, who may offer a `rework` of the accepted automator for a case in scope at gate B. This key proves ONLY that the
    road is open - `check_args` refuses nothing for those facts - not that the rework restores a removed Then (it cannot after
    gate A; that is the conductor's cost-and-consequence line, FR-9)."""
    facts = dict(C26_FACTS, gate="B", gate_decided=False)
    clean, rule = NM.check_args(dict(C26_ARGS), facts)
    check_eq("RD1-19 gate B, an accepted automator, a case in scope: the args are clean", (clean, rule), (C26_ARGS, ""))
    refused, why = NM.check_args(dict(C26_ARGS, cases=["TC-9"]), facts)
    check("RD1-19 negative control: a case outside the scope is refused by the same call", refused is None and "outside the approved scope" in why, why)


# --- t-1936 F2 (N3): which move takes `args` and which is never an option are DATA columns of `moves`: ONE block at the end of the file ----------
# These are plain `test_*` functions with asserts: pytest collects them, and `f2_run` below runs them in the file's own script mode too.
import copy  # noqa: E402

F2_OPEN = ["person_does", "stop_here", "release_and_restart", "go_on_as_is", "rework_stage", "resume_with_words", "story_fact", "revoke_exclusion"]
F2_DASH = {"resume_with_words": "run on the person's own words, never an option: a token answer carries no words",
           "revoke_exclusion": "run on the person's own words, never an option: a token answer carries no words",
           "story_fact": "the conductor's own move: it runs it with a value a script or the person named; never a person's choice"}


def f2_spec(**rows) -> dict:
    """A copy of the real `conductor-actions.json` with the named rows' keys changed (`{move id: {key: value}}`; a value `...` drops the key)."""
    spec = copy.deepcopy(NM.data())
    for row in spec["moves"]:
        for key, value in rows.get(row["id"], {}).items():
            if value is ...:
                row.pop(key, None)
            else:
                row[key] = value
    return spec


def f2_check(options, spec=None, open_ids=None, **extra):
    verdict_ = dict(verdict(()), options=options, question="What should happen next?", **extra)
    return NM.validate_options(verdict_, F2_OPEN if open_ids is None else open_ids, NM.data() if spec is None else spec,
                               story_run.Driver.s0_normalize, {}, facts=C26_FACTS)


def test_args_column_reads_data() -> None:
    rework = dict(seam_option("rework", "rework_stage"), args=dict(C26_ARGS))
    goon = dict(seam_option("go on", "go_on_as_is"), args=dict(C26_ARGS))
    # today's data: the column of rework_stage is "rework" (checked), the column of go_on_as_is is null (dropped)
    options, rule = f2_check([rework, goon])
    assert rule == "" and options is not None, rule
    assert options[0]["args"] == C26_ARGS and "args" not in options[1] and options[1].get("args_dropped") is True, options
    # the COLUMN decides, not the literal move id: swap them and the answers swap
    swapped = f2_spec(rework_stage={"args": None}, go_on_as_is={"args": "rework"})
    options, rule = f2_check([rework, goon], spec=swapped)
    assert rule == "" and "args" not in options[0] and options[0].get("args_dropped") is True, options
    assert options[1]["args"] == C26_ARGS and "args_dropped" not in options[1], options
    # an "args" column still checks the closed list (the invariant of E2.1): a bad stage is the same ArgsRefused
    bad = dict(goon, args=dict(C26_ARGS, stage="S9"))
    try:
        f2_check([rework, bad], spec=swapped)
    except NM.ArgsRefused as refused:
        assert "stage" in refused.rule, refused.rule
    else:
        raise AssertionError("a bad `args` on a move whose column is `rework` was not refused")


def test_args_on_null_column_dropped_and_journaled() -> None:
    options, rule = f2_check([dict(seam_option("retry", "person_does"), args={"dispatch": "S2-x-1"}), seam_option("stop", "stop_here")])
    assert rule == "" and "args" not in options[0] and options[0]["args_dropped"] is True and "args_dropped" not in options[1], (rule, options)
    # E2.3: dropping `args` never relaxes another rule: the same option with a token that is not its move's own is still refused
    options, rule = f2_check([dict(seam_option("go on", "person_does"), args={"x": 1}), seam_option("stop", "stop_here")])
    assert options is None and "is not the token of the move" in rule, rule
    # the driver: the option reaches the person without `args`, and conductor.jsonl says which tokens lost it
    root, task_root, driver = rig(answers=[dict(verdict(), options=[dict(seam_option("retry", "person_does"), args={"dispatch": "S2-x-1"}),
                                                                    seam_option("stop", "stop_here")])])
    try:
        driver.boundary = "S2:S2-qa-case-critic-1"
        _, person = raised(driver, {"why": "refusal", "text": "t", "stage": "S2"})
        assert list(person.offered) == ["retry", "stop"] and person.source == "conductor", (person.offered, person.source)
        assert all("args" not in option for option in person.options), person.options
        lines = jsonl(driver.state_dir / "conductor.jsonl")
        assert [row.get("args_dropped") for row in lines if row.get("action") == "args_dropped"] == [["retry"]], lines
        assert not [row for row in lines if row.get("action") == "unusable"] and not driver.defects, (lines, driver.defects)
    finally:
        harness.cleanup(root)


def test_missing_column_compat_rework_only() -> None:
    bare = f2_spec(**{move["id"]: {"args": ..., "offerable": ..., "not_offered": ...} for move in NM.data()["moves"]})
    for row in bare["moves"]:
        assert "args" not in row and "offerable" not in row, row
    # before the columns exist (E2.1): only rework_stage takes args; a token-`—` move is not offerable, every other one is
    got = {row["id"]: NM.move_columns(row)[:2] for row in bare["moves"]}
    assert got["rework_stage"] == ("rework", True), got
    assert {move: cols for move, cols in got.items() if cols[0] is not None} == {"rework_stage": ("rework", True)}, got
    assert sorted(move for move, cols in got.items() if not cols[1]) == sorted(F2_DASH), got
    rework = dict(seam_option("rework", "rework_stage"), args=dict(C26_ARGS))
    goon = dict(seam_option("go on", "go_on_as_is"), args={"stage": "S2"})
    options, rule = f2_check([rework, goon], spec=bare)
    assert rule == "" and options[0]["args"] == C26_ARGS and options[1].get("args_dropped") is True, (rule, options)
    try:
        f2_check([dict(rework, args=dict(C26_ARGS, cause="invented")), goon], spec=bare)
    except NM.ArgsRefused as refused:
        assert "cause" in refused.rule, refused.rule
    else:
        raise AssertionError("the closed list was not checked in the world without the columns")
    options, rule = f2_check([seam_option("resume", "resume_with_words"), seam_option("stop", "stop_here")], spec=bare)
    assert options is None and "never an option" in rule, rule


def test_bad_column_value_unreadable() -> None:
    for move, change in (("stop_here", {"args": "everything"}), ("person_does", {"offerable": "yes"}), ("stop_here", {"args": ["rework"]})):
        spec = f2_spec(**{move: change})
        token = "stop" if move == "stop_here" else "retry"
        try:
            f2_check([seam_option(token, move), seam_option("go on", "go_on_as_is")], spec=spec)
        except NM.DataUnreadable as unreadable:
            assert move in str(unreadable) and next(iter(change)) in str(unreadable), str(unreadable)
        else:
            raise AssertionError(f"a bad column value {change} on {move} passed silently")
    # the prompt's moves section must never fail on the same data: it reads the safe side
    assert "## Moves open here" in NM.moves_section(f2_spec(stop_here={"offerable": "yes"}), ["stop_here"], {})
    # the driver turns it into an unusable answer with the conductor's question shown - never an exception out of the seam
    root, task_root, driver = rig(answers=[verdict((("retry", "person_does"), ("stop", "stop_here")), question="Do you want to stop here?")])
    real, bad_spec = NM.data, f2_spec(person_does={"offerable": "yes"})
    NM.data = lambda: bad_spec
    try:
        driver.boundary = "S2:x"
        _, person = raised(driver, {"why": "refusal", "text": "t"})
        assert person is not None and "What the conductor found:\nDo you want to stop here?" in person.text, person.text
        assert len(driver.defects) == 1 and "person_does" in " ".join(driver.defects[0]), driver.defects
    finally:
        NM.data = real
        harness.cleanup(root)


def test_dash_moves_not_offerable() -> None:
    rows = {row["id"]: row for row in NM.data()["moves"]}
    for move, why in F2_DASH.items():
        assert NM.move_columns(rows[move]) == (None, False, why), (move, NM.move_columns(rows[move]))
        assert rows[move]["token"] == "—", move                  # no new token (fork 4 reversed)
    for move in set(rows) - set(F2_DASH):
        assert NM.move_columns(rows[move])[1] is True, move
        assert str(rows[move]["token"]) != "—", move
    for move in F2_DASH:
        options, rule = f2_check([seam_option("resume", move), seam_option("stop", "stop_here")])
        assert options is None and f"which is never an option: {F2_DASH[move]}" in rule, rule
    # the invariant that stays: an option whose move is not in the table is still refused
    options, rule = f2_check([seam_option("fly", "teleport"), seam_option("stop", "stop_here")], open_ids=F2_OPEN + ["teleport"])
    assert options is None and "not open here" in rule, rule


def test_not_offered_refusal_quotes_row_reason() -> None:
    spec = f2_spec(story_fact={"not_offered": "THE ROW'S OWN REASON"})
    options, rule = f2_check([seam_option("fact", "story_fact"), seam_option("stop", "stop_here")], spec=spec)
    assert options is None and rule == "the option `fact` names the move `story_fact`, which is never an option: THE ROW'S OWN REASON", rule
    gone = f2_spec(story_fact={"not_offered": ...})
    options, rule = f2_check([seam_option("fact", "story_fact"), seam_option("stop", "stop_here")], spec=gone)
    assert options is None and NM.NOT_OFFERED_DEFAULT in rule, rule


def test_moves_section_says_args_and_never_an_option() -> None:
    section = NM.moves_section(NM.data(), list(F2_OPEN) + ["approve_gate", "stand_prepare"], C26_FACTS)
    assert '- `rework_stage` — token `rework`; its option carries "args" from these values only:' in section, section
    assert '- `go_on_as_is` — token `go on`; option carries no "args"' in section, section
    assert '- `release_and_restart` — token `restart`; option carries no "args"' in section, section
    assert '- `stand_prepare` — token `prepare the stand`; option carries no "args"' in section, section
    assert "- `resume_with_words` — run on the person's own words, never an option" in section, section
    assert "- `revoke_exclusion` — run on the person's own words, never an option" in section, section
    assert "- `story_fact` — yours to run, never an option" in section, section
    assert "resume_with_words` — token" not in section and "story_fact` — token" not in section, section
    # a table where go_on_as_is takes args prints the rework list for it: the section reads the column
    swapped = NM.moves_section(f2_spec(go_on_as_is={"args": "rework"}, rework_stage={"args": None}), ["go_on_as_is", "rework_stage"], C26_FACTS)
    assert 'option carries "args" from these values only' in swapped and "`rework_stage` — token `rework`; option carries no" in swapped, swapped


F2_TESTS = (test_args_column_reads_data, test_args_on_null_column_dropped_and_journaled, test_missing_column_compat_rework_only,
            test_bad_column_value_unreadable, test_dash_moves_not_offerable, test_not_offered_refusal_quotes_row_reason,
            test_moves_section_says_args_and_never_an_option)


def f2_run() -> None:
    for scenario in F2_TESTS:
        try:
            scenario()
            check(f"F2 {scenario.__name__}", True)
        except AssertionError as exc:
            check(f"F2 {scenario.__name__}", False, str(exc)[:600])


if __name__ == "__main__":
    f2_run()                                                         # t-1936 F2: one block at the end, so the merge with another node is clean
    rd1_19_gate_b_assert_stricter_road_is_open()                     # RD1-19: one block at the end, so the merge with another node is clean
    g27_the_fallback_question_at_a_gate()                          # t-884 (C2-7): one block at the end, so the merge with another node is clean
    g27_the_floor_at_a_gate()
    g27_a_rework_from_the_fallback_goes_to_the_conductor_with_the_original_words()
    c26_args_are_validated_and_carried()                             # t-856 (C2-6): one block at the end, so the merge with another node is clean
    c26_a_chosen_call_runs_or_asks_literally()
    c26_restart_refused_is_held_and_the_conductor_is_not_called()
    c26_a_refused_rework_goes_to_the_conductor_through_the_seam()
    c26_a_release_by_any_road_hands_its_words_to_the_relaunch()
    c26_fix_round_t873()
    k4s_run()                                                       # t-835: one block at the end, so the merge with another node is clean
    el12_the_exit_limit_questions_own_doors_are_no_moves_word()     # t-764: one block at the end, so the merge with another node is clean
    n24_the_seam_set_is_the_seam()                                  # t-834: after el12_..., before main() finishes the run
    main()
