#!/usr/bin/env python3
"""controller: a part of test_words_doors.py, split by tools/test_split.py (TD-11c). The shared helpers are in words_doors_common."""
import io
import json
import re
import sys
from contextlib import redirect_stderr
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import SCRIPTS, check, check_eq, check_in, check_not_in, cleanup, finish, run_script, s5_apply
sys.path.insert(0, str(SCRIPTS))
import stage_guard  # noqa: E402
import waiver  # noqa: E402
from words_doors_common import (  # noqa: E402
    FLAG, SPAN, TICKET, WORDS, captured, critic_review, ctrl_project, open_door, project_env, recorded,
    refused_text, story_pipeline,
)


def waiver_door(root: Path, task: Path, label: str, text: str, stage: str, block: str, head: str = "") -> None:
    """The printed waiver door, opened through the real waiver.py: records `block` for `stage`."""
    check_in(f"{label}: the refusal prints a waiver door", "waiver.py", text)
    story_pipeline(task)
    done, _, _ = open_door(root, text, TICKET, stage, head)
    recorded(label, done, root, TICKET, stage, block)


def span_with(text: str, needle: str) -> str:
    spans = [s for s in SPAN.findall(text) if needle in s]
    return spans[-1] if spans else ""


def run_printed(root: Path, task: Path, label: str, span: str, words: Path, extra: tuple = ()):
    """Run a printed `controller.py ...` / `--operation ...` span through the real CLI, the file
    placeholder replaced by the words file. `extra` is what the printed text leaves to the caller."""
    check_in(f"{label}: the printed door is the file form", f"{FLAG} <file>", span)
    head = span[:span.index(FLAG)].split()
    argv = head if head and head[0] == "controller.py" else ["controller.py", "--task-root", str(task)] + head
    words.parent.mkdir(parents=True, exist_ok=True)
    words.write_bytes(WORDS.encode("utf-8"))
    return run_script(argv[0], *argv[1:], *extra, FLAG, str(words), cwd=root, env=project_env(root))


def row_1_2_design_review() -> None:
    from controller import Controller
    root, task = ctrl_project("qa-words-door-design-")
    try:
        import test_controller_gate_decision as GATE
        c = GATE.story(task)
        # One story: both refusals are read first (a recorded `design review` word would pass the
        # second), then row 2's waiver is opened, then row 1's CLI records the decision.
        built = c.build_gate_decision("A", WORDS)
        built["design_reviews"] = [dict(built["design_reviews"][0], verdict="rejected")]
        text = "\n".join(str(p) for p in c.check_decision(built))
        check_in("2 design review: a critic's own rejection is refused", "declared verdict is 'rejected'", text)
        broken = dict(built, design_reviews=[])
        missing = "\n".join(str(p) for p in c.check_decision(broken))
        check_in("1 design review: the missing-review refusal is printed", "requires an independent design review",
                 missing)
        waiver_door(root, task, "2 design review", text, "S4", "design review")
        check_eq("2 design review: the refusing code no longer refuses",
                 [p for p in c.check_decision(built) if "design review" in str(p)], [])
        span = span_with(missing, "gate-decision")
        result = run_printed(root, task, "1 design review", span, task / "state" / "words" / "door.txt")
        check("1 design review: the real controller records the gate decision from the file (exit 0)",
              result.returncode == 0, f"{result.returncode} {result.stdout[-300:]} {result.stderr[-300:]}")
        decisions = (Controller(task).state().get("decisions") or {}).values()
        check_eq("1 design review: the decision carries the person's words from the file, whole",
                 [d.get("authorization_source") for d in decisions if d.get("gate") == "A"], [WORDS])
    finally:
        cleanup(root)


def row_3_empty_scope_at_gate_a() -> None:
    import test_controller_state as BASE
    import test_controller_rework_scope as SCOPED
    from controller import Controller
    root, task = ctrl_project("qa-words-door-empty-a-")
    try:
        c = Controller(task)
        c.apply("initialize", {"scope": ["TC-1"], "source_revision": "src-1",
                               "known_paths": {"root": str(task)}, "idempotency_key": "init"})
        for number in range(5):
            BASE.accept_stage(c, task, f"S{number}")
        BASE.seed_plan(task, [SCOPED.plan_row(1, "automate")])
        c.apply("revise_plan", {"scope": [], "plan_revision": "plan-2",
                                "reason": "scope recorded empty by mistake", "idempotency_key": "revise"})
        decision = {"id": "gate-a", "gate": "A", "action": "approve", "status": "approved",
                    "authorization_source": "human", "source_revision": "src-1", "scope": [],
                    "input_revision": "plan-2", "idempotency_key": "gate-a"}
        decision.update(c.gate_inputs())
        text = refused_text(lambda: c.apply("decision", dict(decision)))
        check_in("3 empty scope (gate A): an empty scope under a plan with rows is refused", "empty scope", text)
        waiver_door(root, task, "3 empty scope (gate A)", text, "S4", "empty scope")
        check_eq("3 empty scope (gate A): the refusing code no longer refuses",
                 refused_text(lambda: c.apply("decision", dict(decision))), "")
    finally:
        cleanup(root)


def settle(c, task: Path, dispatch_id: str) -> None:
    """Accept a running S5 author dispatch (open work), so the next dispatch of the story may start."""
    import test_s5_process as S5
    c.apply("accept", {"id": dispatch_id, "status": "accepted", "stage_complete": False, "unresolved": True,
                       "reason": "the window's repair round is still open",
                       "evidence_refs": [S5.evidence(task, dispatch_id + ".txt")],
                       "idempotency_key": dispatch_id + "-settled"})


def rows_4_5_11_dispatch_doors() -> None:
    """One S5 story: an empty scope (row 4), a dispatch the stage guard holds (row 11), a reviewer for
    a mechanical round (row 5). Their block words differ, so each override passes only its own."""
    import test_s5_process as S5
    root, task = ctrl_project("qa-words-door-dispatch-")
    real = stage_guard.dispatch_errors
    bare = "stage S5 is held by a rule of the guard that prints no command of its own"

    def stand_in(pipeline, stage_id, **_):
        # `stage_guard_errors` adds its door ONLY to a message that carries none, and the real
        # `dispatch_errors` always appends its own hint: a rule that returns bare text stands in for
        # it here, passed through the same `waiver.split_overridden` the real one uses.
        return waiver.split_overridden([bare], pipeline, stage_id)[0]
    try:
        c = S5.s5_task(task)
        request = {"id": "empty-s5", "stage": "S5", "role": "qa-automator", "scope": [], "input_hash": "h",
                   "budget": {}, "known_paths": {}, "idempotency_key": "empty-s5"}
        text = refused_text(lambda: s5_apply(c, dict(request)))
        check_in("4 empty scope (dispatch): an empty S5 scope is refused", "empty scope", text)
        waiver_door(root, task, "4 empty scope (dispatch)", text, "S5", "empty scope")
        check_eq("4 empty scope (dispatch): the refusing code no longer refuses",
                 refused_text(lambda: s5_apply(c, dict(request))), "")
        settle(c, task, "empty-s5")
        guarded = {"id": "guarded", "stage": "S5", "role": "qa-automator", "scope": ["TC-1", "TC-2"],
                   "input_hash": "h2", "budget": {}, "known_paths": {}, "idempotency_key": "guarded"}
        stage_guard.dispatch_errors = stand_in
        text = refused_text(lambda: s5_apply(c, dict(guarded)))
        check_in("11 stage guard: the dispatch is refused with the guard's own words", bare, text)
        check_in("11 stage guard: the controller adds the person's-word door", "a person's word passes this", text)
        # `<part of the line>` is the person's to fill: any part of the refused line
        waiver_door(root, task, "11 stage guard", text, "S5", "prints no command of its own",
                    head="prints no command of its own")
        check_eq("11 stage guard: the refusing code no longer refuses",
                 refused_text(lambda: s5_apply(c, dict(guarded))), "")
        stage_guard.dispatch_errors = real
        settle(c, task, "guarded")

        def critic():
            return S5.dispatch(c, task, "k1", role="qa-code-critic", repair_cause="mechanical",
                               reason="check the sleep fix", accept=False)
        text = refused_text(critic)
        check_in("5 mechanical repair round (critic): a reviewer for a mechanical round is refused",
                 "not dispatched for a mechanical repair round", text)
        # C1-5a: the door is the pass of THAT round (`mechanical pass <n> for <role> on <stage>:<hash>`), the line's first words
        waiver_door(root, task, "5 mechanical repair round (critic)", text, "S5", pass_blocks(text)[0])
        check_eq("5 mechanical repair round (critic): the refusing code no longer refuses",
                 refused_text(critic), "")
    finally:
        stage_guard.dispatch_errors = real
        cleanup(root)


def rows_6_7_repair_rounds() -> None:
    """One S5 story, two refusals: the mechanical cap, then the cap on plain rounds. The block word
    `mechanical repair round` is not in the plain cap's text, and `repair round` is recorded last."""
    import test_s5_process as S5
    root, task = ctrl_project("qa-words-door-rounds-")
    try:
        c = S5.s5_task(task)
        S5.dispatch(c, task, "a1")
        S5.dispatch(c, task, "m1", repair_cause="mechanical", reason="TC-1: a sleep -> a wait")

        def again():
            return S5.dispatch(c, task, "m2", repair_cause="mechanical", reason="again")
        text = refused_text(again)
        check_in("6 mechanical repair round (cap): a second mechanical round is refused",
                 "mechanical repair round(s); the cap is 1", text)
        waiver_door(root, task, "6 mechanical repair round (cap)", text, "S5", pass_blocks(text)[0])
        check_eq("6 mechanical repair round (cap): the refusing code no longer refuses",
                 refused_text(again), "")

        text = ""
        for number in range(8):  # plain rounds about the test, until the cap says no
            text = refused_text(lambda: S5.dispatch(c, task, f"p{number}"))
            if text:
                break
        check_in("7 repair round (cap): the rounds about the test run out", "repair round(s) about the test", text)
        # C1-5a: two doors, the author's pass first and the critic's second; the author's opens its own round
        blocks = pass_blocks(text)
        check_eq("7 repair round (cap): the refusal prints a pass for each of the two roles",
                 [b.split(" on ")[0].split(" for ")[1] for b in blocks], ["qa-automator", "qa-code-critic"])
        waiver_door(root, task, "7 repair round (cap)", f"`{door_spans(text)[0]}`", "S5", blocks[0])
        check_eq("7 repair round (cap): the refusing code no longer refuses",
                 refused_text(lambda: S5.dispatch(c, task, f"p{number}")), "")
    finally:
        cleanup(root)


def row_round_pass_keys() -> None:
    """C1-5a (A2, A3, F3; t-700 Q1): a person's word passes ONE round with its own key. `waiver.split_overridden` matches a word by
    substring, case-folded, and never uses it up, so a stage-wide `repair round` passed every later round of the window. The key
    `round pass {n} for {role} on {stage}:{hash12}` names the round; hash12 comes from the window's ledger key and its life (F2:
    `content_hash(ledger_key + "|" + life)[:12]`, the life "" for the first; a changed case list must not change it); neither key form holds a live keyword; an old stage-wide record keeps its old power (edge 3, temporal)."""
    import test_s5_process as S5
    from controller import ledger_key, mechanical_pass_key, repair_pass_key, repair_passes
    from event_store import content_hash
    root, task = ctrl_project("qa-words-door-pass-")
    try:
        c = S5.s5_task(task)
        window = {"stage": "S5", "role": "qa-automator", "scope": ["TC-1", "TC-2"]}
        for name in ("a1", "a2", "a3"):                      # the opener and two rounds about the test: the author's cap is spent
            S5.dispatch(c, task, name)
        for name in ("k1", "k2", "k3"):                      # the same for the critic
            S5.dispatch(c, task, name, role="qa-code-critic")
        text = refused_text(lambda: S5.dispatch(c, task, "a4"))
        author, critic = blocks = pass_blocks(text)
        packet = c.prepare(dict(window))
        check_eq("pass keys: the refusal prints the keys `repair_budget` carries, for both roles, in its order (never rebuilt)",
                 blocks, list(packet["repair_budget"]["passes"].values()))
        check_eq("pass keys: round 3 for each role (counted 2 each)", [b.split(" on ")[0] for b in blocks],
                 ["round pass 3 for qa-automator", "round pass 3 for qa-code-critic"])
        check("pass keys: the refused line STARTS with the author's own key, then today's sentence",
              text.startswith(author + ": qa-automator has already had 2 repair round(s) about the test"), text[:160])
        check_not_in("pass keys: the refused line does not carry the other role's key (a word matches by substring)",
                     critic, text.split(" If a person wants one more round")[0])
        mechanical = mechanical_pass_key(c.state()["dispatches"], window)
        for key in (author, critic, mechanical):
            for live in ("repair round", "mechanical round"):
                check_not_in(f"pass keys: `{key[:34]}...` holds no live keyword `{live}`", live, key.lower())
        check("pass keys: the mechanical key is its own form", mechanical.startswith("mechanical pass 1 for qa-automator on S5:"), mechanical)
        check("pass keys: round 1 is not a substring of round 10 (the ` for ` after the number)",
              repair_pass_key("S5", "qa-automator", 1, "k") not in repair_pass_key("S5", "qa-automator", 10, "k"))
        check_eq("pass keys: hash12 = content_hash(ledger_key(p) + '|' + life)[:12], the first life being '' (F2: the key ends with the bar)",
                 author.rsplit(":", 1)[1], content_hash(ledger_key(window) + "|")[:12])
        check("pass keys: ...which is not the hash of the scope list", author.rsplit(":", 1)[1] != content_hash(sorted(window["scope"]))[:12])
        designer = {"stage": "S4", "role": "qa-case-designer", "scope": ["TC-1"]}
        check_eq("pass keys: a changed case list does not change the S4 designer's key (its ledger key is story-wide)",
                 repair_passes({}, designer)["qa-case-designer"],
                 repair_passes({}, dict(designer, scope=["TC-1", "TC-2", "TC-3"]))["qa-case-designer"])
        check_eq("pass keys: an empty scope still has a key (the ledger hashes the empty list, no `no key` branch)",
                 sorted(repair_passes({}, dict(window, scope=[]))), ["qa-automator", "qa-code-critic"])
        story_pipeline(task)
        done, _, _ = open_door(root, f"`{door_spans(text)[1]}`", TICKET, "S5")
        recorded("pass keys: the critic's pass", done, root, TICKET, "S5", critic)
        check_in("pass keys: the critic's pass alone does not pass the author's round", author,
                 refused_text(lambda: S5.dispatch(c, task, "a4")))
        done, _, _ = open_door(root, f"`{door_spans(text)[0]}`", TICKET, "S5")
        recorded("pass keys: the author's pass", done, root, TICKET, "S5", author)
        check_eq("pass keys: the author's pass opens its round (3)", refused_text(lambda: S5.dispatch(c, task, "a4")), "")
        again = refused_text(lambda: S5.dispatch(c, task, "a5"))
        check("pass keys: the word passes exactly ONE round - round 4 is refused with its own key",
              again.startswith("round pass 4 for qa-automator on S5:"), again[:120])
        check_eq("pass keys: the critic's own round 3 passes with its pass", refused_text(lambda: S5.dispatch(c, task, "k4", role="qa-code-critic")), "")
        check("pass keys: ...and its round 4 is refused with its own key",
              refused_text(lambda: S5.dispatch(c, task, "k5", role="qa-code-critic")).startswith("round pass 4 for qa-code-critic on S5:"))
    finally:
        cleanup(root)
    root, task = ctrl_project("qa-words-door-oldpass-")
    try:
        c = S5.s5_task(task)
        S5.dispatch(c, task, "a1")
        S5.dispatch(c, task, "m1", repair_cause="mechanical", reason="TC-1: a sleep -> a wait")
        for name in ("a2", "a3"):
            S5.dispatch(c, task, name)
        story_pipeline(task)
        path = task / "pipeline.json"
        pipeline = json.loads(path.read_text(encoding="utf-8"))
        def old_record(match: str) -> None:                           # a word recorded by an OLD door, stage-wide
            waiver.apply_stage_override(pipeline, "S5", match, "an old word", waiver.now_iso())
            path.write_text(json.dumps(pipeline), encoding="utf-8")
        old_record("mechanical repair round")
        check_eq("pass keys, temporal: an OLD `mechanical repair round` record still passes the mechanical cap",
                 refused_text(lambda: S5.dispatch(c, task, "m2", repair_cause="mechanical", reason="again")), "")
        check("pass keys, temporal: ...and is not the plain cap's word (that text does not hold it)",
              refused_text(lambda: S5.dispatch(c, task, "a4")).startswith("round pass 3 for qa-automator on S5:"))
        old_record("repair round")
        check_eq("pass keys, temporal: an OLD `repair round` record still passes the cap, round after round (the sentence after the key holds it)",
                 [refused_text(lambda: S5.dispatch(c, task, name)) for name in ("a4", "a5")], ["", ""])
    finally:
        cleanup(root)


def row_pass_key_counting_and_life() -> None:
    """t-708 (F1, F2; integration critic t-706), on the pure functions and a hand-built journal. F1: the reviewer's mechanical pass
    number counts with the ledger's predicate (A1) - a round an own-stage `reviews` stamp set aside is a PAID round, or the old
    word would pass a second reviewer mechanical round (I2); one an earlier stage's rework set aside opens a new window. F2: the
    window's LIFE (the latest earlier-stage rework that set it aside) is in the hash, "" for the first life."""
    from controller import (apply_rerun_after, mechanical_pass_key, mechanical_rounds, repair_pass_key,
                            repair_passes, window_life)
    from event_store import content_hash

    def state_of(rework_stage):
        def d(identifier, role, stage="S5", **extra):
            return dict({"id": identifier, "stage": stage, "role": role, "scope": ["TC-1"], "status": "accepted"}, **extra)
        return {"dispatches": {"a1": d("a1", "qa-automator"), "m1": d("m1", "qa-automator", repair_cause="mechanical"),
                               "k1": d("k1", "qa-code-critic", repair_cause="mechanical"),
                               "r": d("r", "qa-automator" if rework_stage == "S5" else "qa-worker", stage=rework_stage,
                                      status="running", rework_of="x")},
                "stages": {"S5": {"status": "completed"}}, "decisions": {}}
    critic = {"stage": "S5", "role": "qa-code-critic", "scope": ["TC-1"]}
    author = dict(critic, role="qa-automator")
    fresh = state_of("S5")["dispatches"]
    before = {role: mechanical_pass_key(fresh, window) for role, window in (("critic", critic), ("author", author))}
    check("F1 fixture: the reviewer has had one mechanical dispatch (k1), the author one (m1): both next passes are number 2",
          before["critic"].startswith("mechanical pass 2 for qa-code-critic on S5:")
          and before["author"].startswith("mechanical pass 2 for qa-automator on S5:"), str(before))
    own = state_of("S5")
    apply_rerun_after(own, "r", "S5", {"stages": [], "reviews": ["k1"], "decisions": []})
    check_eq("F1 fixture: the S5 rework staled the reviewer's k1 through the `reviews` stamp, with the mark",
             (own["dispatches"]["k1"]["status"], own["dispatches"]["k1"].get("stale_by_rework")), ("stale", "r"))
    check_eq("F1: an own-stage stale keeps the reviewer's mechanical pass number (2, the same key - the old word does not pass a "
             "second reviewer mechanical round)", mechanical_pass_key(own["dispatches"], critic), before["critic"])
    check_eq("F1: ...ONE counter - `mechanical_rounds` by role says 1, as before the stale",
             mechanical_rounds(own["dispatches"], critic, by_role=True), 1)
    check_eq("F1: the author's key is not touched by the reviewer's stale (the AUTHOR branch is unchanged)",
             mechanical_pass_key(own["dispatches"], author), before["author"])
    earlier = state_of("S4")
    apply_rerun_after(earlier, "r", "S4", {"stages": ["S5"], "reviews": [], "decisions": []})
    after = {role: mechanical_pass_key(earlier["dispatches"], window) for role, window in (("critic", critic), ("author", author))}
    check("F1: an EARLIER stage's rework opens a new window for both roles: mechanical pass 1, counted 0",
          after["critic"].startswith("mechanical pass 1 for qa-code-critic on S5:")
          and after["author"].startswith("mechanical pass 1 for qa-automator on S5:"), str(after))
    check_eq("F2: a window never set aside has the first life ''", window_life(fresh, critic), "")
    check_eq("F2: a rework of the window's OWN stage is no new life", window_life(own["dispatches"], critic), "")
    check_eq("F2: the earlier-stage rework that set it aside is the life - for both roles of the loop",
             (window_life(earlier["dispatches"], critic), window_life(earlier["dispatches"], author)), ("r", "r"))
    check_eq("F2: the first life hashes the ledger key with the bar and nothing after it",
             before["critic"].rsplit(":", 1)[1], content_hash("S5:qa-code-critic:" + content_hash(["TC-1"]) + "|")[:12])
    check_eq("F2: the new life's hash is the key, the bar and the rework's id",
             after["critic"].rsplit(":", 1)[1], content_hash("S5:qa-code-critic:" + content_hash(["TC-1"]) + "|r")[:12])
    check("F2: so the same round has another key in the new life (the old word stops matching)",
          repair_passes(fresh, critic)["qa-automator"].rsplit(":", 1)[1]
          != repair_passes(earlier["dispatches"], critic)["qa-automator"].rsplit(":", 1)[1])
    check("F2: the key builder's life argument is the only thing that moves the hash",
          repair_pass_key("S5", "qa-automator", 3, "k") != repair_pass_key("S5", "qa-automator", 3, "k", life="rw-1"))

    def stale(identifier, mark, **extra):
        return dict({"id": identifier, "stage": "S5", "role": "qa-automator", "scope": ["TC-1"], "status": "stale",
                     "stale_by_rework": mark}, **extra)
    def rework(identifier, stage):
        return {"id": identifier, "stage": stage, "role": "qa-worker", "scope": ["TC-1"], "status": "accepted"}
    twice = {"a1": stale("a1", "r4"), "r4": rework("r4", "S4"), "n1": stale("n1", "r3"), "r3": rework("r3", "S3")}
    check_eq("F2 edge: a window staled twice by earlier-stage reworks takes the LATEST in the journal's order",
             window_life(twice, author), "r3")
    check_eq("F2 edge: ...and the order is the journal's, not the id's",
             window_life({"a1": twice["a1"], "n1": twice["n1"], "r3": twice["r3"], "r4": twice["r4"]}, author), "r4")
    anonymous = {"a1": stale("a1", "r"), "r": {key: value for key, value in rework("r", "S4").items() if key != "id"}}
    life, _, err = captured(lambda: window_life(anonymous, author))
    check_eq("F2 edge: a rework record with no id field is the first life, not a KeyError", life, "")
    check_eq("F2 edge: ...and one defect line is printed", len([line for line in err.splitlines() if "no id field" in line]), 1)
    check_eq("F2 edge: a stale mark naming no record is the first life (an old journal), nothing printed",
             captured(lambda: window_life({"a1": stale("a1", "gone")}, author))[::2], ("", ""))


def row_pass_life_end_to_end() -> None:
    """t-708 (F2, R15's second direction) through the real controller, waiver.py and the real stamp: a word recorded for round 3
    of the OLD life of a window does not open round 3 of the NEW life an earlier stage's person-word rework starts."""
    import test_controller_rework as REWORK
    import test_controller_state as BASE
    import test_s5_process as S5
    root, task = ctrl_project("qa-words-door-life-")
    try:
        c = REWORK.story_to_s8(task)
        window = ("TC-1",)
        for name in ("a2", "a3"):                                  # the old life: the opener dS5-author and two rounds
            S5.dispatch(c, task, name, scope=window)
        text = refused_text(lambda: S5.dispatch(c, task, "a4", scope=window))
        old_author, old_critic = pass_blocks(text)
        story_pipeline(task)
        done, _, _ = open_door(root, f"`{door_spans(text)[0]}`", TICKET, "S5")
        recorded("life: the old life's round 3 pass", done, root, TICKET, "S5", old_author)
        check_eq("life: the recorded pass opens round 3 of the OLD life", refused_text(lambda: S5.dispatch(c, task, "a4", scope=window)), "")
        request = c.build_rework_request("S4", "qa-worker", ["TC-1"], REWORK.WORDS, words_given=True)
        check_eq("life fixture: a person's rework of S4 stamps S5 to run again", (request.get("rerun_after") or {}).get("stages")[:1], ["S5"])
        s5_apply(c, dict(request))
        REWORK.settle(c, task, request)
        state = c.state()
        check_eq("life fixture: the old life's dispatches are stale under the S4 rework's mark (counted 0 from here, A1)",
                 [(state["dispatches"][i]["status"], state["dispatches"][i].get("stale_by_rework")) for i in ("a2", "a3", "a4")],
                 [("stale", request["id"])] * 3)
        REWORK.redo(c, task, "S4", "dS4-again")
        c.apply("decision", BASE.bind_gate_a(task, {
            "id": "gate-a2", "gate": "A", "action": "approve", "status": "approved", "authorization_source": "human",
            "source_revision": "src-1", "scope": list(window), "input_revision": "src-1", "idempotency_key": "gate-a2"}))
        check_eq("life: the new life runs its opener and two rounds",
                 [refused_text(lambda: S5.dispatch(c, task, name, scope=window)) for name in ("n1", "n2", "n3")], ["", "", ""])
        again = refused_text(lambda: S5.dispatch(c, task, "n4", scope=window))
        check("life: round 3 of the new life IS refused (the old life's word is not read as this life's)", bool(again),
              "n4 went through: the old life's round 3 pass opened round 3 of the new life")
        if not again:
            return
        new_author, new_critic = pass_blocks(again)
        check("life: round 3 of the NEW life is refused although the old life's round 3 pass is recorded (old key "
              f"{old_author!r}, new key {new_author!r})", again.startswith(new_author + ": qa-automator has already had 2"), again[:160])
        check("life: the refusal prints the NEW key - round 3 again, another hash", new_author.startswith("round pass 3 for qa-automator on S5:")
              and new_author != old_author, f"old {old_author!r} new {new_author!r}")
        check("life: ...and the critic's pass has another hash too (round 1 in both lives)",
              new_critic.split(":")[0] == old_critic.split(":")[0] and new_critic != old_critic, f"old {old_critic!r} new {new_critic!r}")
        done, _, _ = open_door(root, f"`{door_spans(again)[0]}`", TICKET, "S5")
        recorded("life: the new life's round 3 pass", done, root, TICKET, "S5", new_author)
        check_eq("life: the new key opens round 3 of the new life", refused_text(lambda: S5.dispatch(c, task, "n4", scope=window)), "")
    finally:
        cleanup(root)


def row_person_rework_round_pass() -> None:
    """t-708 (F3; the t-698 spec 6 Q-b / R14 / edge 10 pin) through the REAL person-word rework (`--operation rework --words-file`,
    so the `reviews` stamp of an S5 rework stales the S5 critic): two reworks within the cap, the third refused with the key,
    the round-3 pass opens exactly round 3, and the critic's re-review past ITS cap passes with the same answer - the stamp's
    staling of the critic's reviews does not reset the critic's count (A1), which the plain dispatches of `row_round_pass_keys`
    never reach. Lives here, not in the test_controller_rework parts: the pass is recorded through the real waiver.py door, and the
    door helpers (`open_door`, `recorded`, `pass_blocks`) are this file's."""
    import test_controller_rework as REWORK
    from controller import Controller, repair_passes
    root, task = ctrl_project("qa-words-door-rework-")
    try:
        REWORK.story_to_s8(task)
        words = REWORK.words_file(task)
        window = ("TC-1",)
        critic_window = {"stage": "S5", "role": "qa-code-critic", "scope": list(window)}

        def rework_cli():
            """The person's words rework of S5 through the real CLI: (exit code, the new dispatch's id or the refusal's text)."""
            done = run_script("controller.py", "--task-root", str(task), "--operation", "rework", "--stage", "S5", "--role",
                              "qa-automator", "--cases", "TC-1", "--words-file", str(words), cwd=root, env=project_env(root))
            if done.returncode == 0:
                return 0, json.loads(done.stdout)["request"]["id"]
            return done.returncode, json.loads(done.stderr.strip().splitlines()[-1]).get("error", done.stderr)

        def settle_it(identifier):
            REWORK.settle(Controller(task), task, {"id": identifier})

        def review(name):
            return refused_text(lambda: critic_review(Controller(task), task, name, window))

        code, first = rework_cli()
        check_eq("rework: the first person's rework is accepted by the CLI", code, 0)
        settle_it(first)
        check_eq("rework: the critic's re-review is dispatched (its round 1)", review("k2"), "")
        code, second = rework_cli()
        check_eq("rework: the second person's rework is within the cap", code, 0)
        state = Controller(task).state()
        check_eq("rework: its stamp staled the critic's re-review (own stage: a paid round), with the mark",
                 (state["dispatches"]["k2"]["status"], state["dispatches"]["k2"].get("stale_by_rework")), ("stale", second))
        settle_it(second)
        check_eq("rework: the critic's second re-review is dispatched (its round 2: the critic is at its cap)", review("k3"), "")
        code, text = rework_cli()
        check("rework: the third rework is refused with the author's round 3 key",
              code != 0 and str(text).startswith("round pass 3 for qa-automator on S5:"), f"{code} {str(text)[:160]}")
        author, critic = pass_blocks(text)
        check_eq("rework: ...and the refusal prints the critic's own round 3 key as the second door",
                 critic.split(" on ")[0], "round pass 3 for qa-code-critic")
        story_pipeline(task)
        for index, key in enumerate((author, critic)):
            done, _, _ = open_door(root, f"`{door_spans(text)[index]}`", TICKET, "S5")
            recorded(f"rework: the pass {key.split(' on ')[0]}", done, root, TICKET, "S5", key)
        code, third = rework_cli()
        check_eq("rework: the author's pass opens round 3 (the rework is accepted by the CLI)", code, 0)
        state = Controller(task).state()
        check_eq("rework: its stamp staled the critic's k3 under the third rework's mark (the stamp was applied to this very rework)",
                 (state["dispatches"]["k3"]["status"], state["dispatches"]["k3"].get("stale_by_rework")), ("stale", third))
        settle_it(third)
        code, text = rework_cli()
        check("rework: ...exactly round 3 - the fourth rework is refused with round 4's own key",
              code != 0 and str(text).startswith("round pass 4 for qa-automator on S5:"), f"{code} {str(text)[:160]}")
        check_eq("rework: the critic's key now is the one printed before the stamp staled k3 (the staling reset nothing)",
                 repair_passes(Controller(task).state()["dispatches"], critic_window)["qa-code-critic"], critic)
        check_eq("rework: the critic's re-review past its cap passes with the same answer (its round 3)", review("k4"), "")
        check("rework: ...and its round 4 is refused with its own key", review("k5").startswith("round pass 4 for qa-code-critic on S5:"))
    finally:
        cleanup(root)


def door_spans(text: str) -> list:
    """Every waiver command a printed refusal carries, in the order printed."""
    return [s for s in SPAN.findall(text) if "waiver.py" in s]


def pass_blocks(text: str) -> list:
    """The `--block` word of each waiver door in a printed refusal (C1-5a: the round passes), in the order printed."""
    return [m.group(1) for span in door_spans(text) for m in [re.search(r'--block "([^"]+)"', span)] if m]


def row_8_not_receipted() -> None:
    import test_controller_rework_scope as SCOPED
    import test_controller_state as BASE
    import test_controller_release as REL
    root, task = ctrl_project("qa-words-door-receipt-")
    try:
        c = SCOPED.gate_a_task(task)
        s5_apply(c, {"id": "S5-qa-code-critic-1", "stage": "S5", "role": "qa-code-critic",
                             "scope": ["TC-1"], "input_hash": "s5", "budget": {}, "known_paths": {},
                             "idempotency_key": "d-critic"})
        REL.manifest(task)
        accept = {"id": "S5-qa-code-critic-1", "status": "accepted", "stage_complete": False, "unresolved": True,
                  "reason": "the window's second half is not reviewed yet",
                  "evidence_refs": [BASE.evidence_ref(task, "digest.txt")], "idempotency_key": "a-critic"}
        text = refused_text(lambda: c.apply("accept", dict(accept)))
        check_in("8 not receipted: a review with no receipts is refused", "not the person's to produce", text)
        waiver_door(root, task, "8 not receipted", text, "S5", "not receipted")
        check_eq("8 not receipted: the refusing code no longer refuses",
                 refused_text(lambda: c.apply("accept", dict(accept))), "")
    finally:
        cleanup(root)


def row_9_mechanical_round() -> None:
    import test_s5_process as S5
    from event_store import content_hash
    root, task = ctrl_project("qa-words-door-mround-")
    try:
        c = S5.s5_task(task, ("TC-1",))
        S5.dispatch(c, task, "a1", scope=("TC-1",))
        S5.dispatch(c, task, "k1", role="qa-code-critic", scope=("TC-1",))
        S5.dispatch(c, task, "a2", scope=("TC-1",), accept=False, repair_cause="mechanical",
                    reason="TC-1: a sleep -> a wait")
        plan = json.loads((task / "work" / "test-plan.json").read_text(encoding="utf-8"))
        obligation = next(ob for row in plan["rows"] for ob in row.get("coverage_obligations") or [])
        refs = [{"obligation_id": obligation["obligation_id"], "obligation_hash": content_hash(obligation)}]
        proof = S5.evidence(task, "proof.json")
        # a window reviewed and probed on its final bytes (H0 = H0): the author's mechanical dispatch
        # completes it only with the `mechanical_round` record, and this record has none
        instance = {"schema_version": 2, "instance_id": "test_x", "input_hash": "H0", "outcome": "passed",
                    "execution_fingerprint": "fp-1", "review": {"verdict": "approved", "input_hash": "H0"},
                    "change_disposition": "new_or_changed", "change_basis_ref": "diff",
                    "obligation_ids": [obligation["obligation_id"]], "obligation_refs": refs,
                    "obligation_hash": content_hash(refs), "assertion_id": "t.py:9", "defect_location": "src.py:4",
                    "probe": {"verdict": "intended_failure", "input_hash": "H0", "expected_location": "a",
                              "actual_location": "a", "expected_reason": "r", "actual_reason": "r",
                              "failure_kind": "assertion", "mutation_kind": "real_behavior",
                              "obligation_ids": [obligation["obligation_id"]], "obligation_refs": refs,
                              "obligation_hash": content_hash(refs), "assertion_id": "t.py:9",
                              "defect_location": "src.py:4", "evidence_ref": proof["path"]},
                    "evidence_refs": [proof]}
        record = {"schema_version": 2, "input_hash": "h", "required_quality_checks": [],
                  "author_dispatch_id": "a1", "reviewer_dispatch_id": "k1", "quality_receipts": [],
                  "scope_instances": {"TC-1": ["test_x"]}, "instances": [instance]}
        (task / "work").mkdir(exist_ok=True)
        (task / "work" / "s5-window.json").write_text(json.dumps(record), encoding="utf-8")
        import hashlib
        receipt = {"path": "work/s5-window.json",
                   "sha256": hashlib.sha256((task / "work" / "s5-window.json").read_bytes()).hexdigest()}

        def complete():
            return c.apply("accept", {"id": "a2", "status": "accepted", "stage_complete": True, "window": record,
                                      "evidence_refs": [proof, receipt], "idempotency_key": "done"})
        text = refused_text(complete)
        check_in("9 mechanical round: an author's window with no `mechanical_round` record is refused",
                 "no well-formed `mechanical_round`", text)
        waiver_door(root, task, "9 mechanical round", text, "S5", "mechanical round")
        check_eq("9 mechanical round: the refusing code no longer refuses", refused_text(complete), "")
    finally:
        cleanup(root)


def row_10_derived_scope() -> None:
    import test_fixes_13797 as FIX
    root, task = ctrl_project("qa-words-door-derived-")
    try:
        c = FIX.s6_story(task)
        text = FIX.runner(c, task, "S6-auto", "automation", ["TC-1"], True)
        check_in("10 derived scope: the automation half cannot complete S6 alone", "manual-agent case TC-2", text)
        waiver_door(root, task, "10 derived scope", text, "S6", "derived scope")
        check_eq("10 derived scope: the refusing code no longer refuses",
                 FIX.runner(c, task, "S6-auto", "automation", ["TC-1"], True), "")
    finally:
        cleanup(root)


def rows_12_30_release() -> None:
    """The spawn guard prints the release command for a receipt that still blocks (row 30) and
    `next` prints the same one for a dispatch nobody is doing (row 12): both name `--words-file
    <file>`, and the real controller releases the dispatch from the file. One S5 story; the
    release of the first dispatch frees the second."""
    import test_s5_process as S5
    from controller import Controller
    from unittest.mock import patch
    root, task = ctrl_project("qa-words-door-release-")
    try:
        c = S5.s5_task(task)
        S5.dispatch(c, task, "S5-qa-automator-1", accept=False)
        folder = root / "qa-factory" / "state" / "host-dispatches"
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "a.json").write_text(json.dumps({
            "agent_id": "a", "agent_type": "qa-automator", "task_id": TICKET, "status": "running",
            "dispatch_id": "S5-qa-automator-1"}), encoding="utf-8")

        def spawn():
            event = {"tool_name": "spawn_agent", "tool_input": {"agent_type": "qa-automator", "message": "x"}}
            code, err = 0, io.StringIO()
            with patch("hooklib.project_root", return_value=root), \
                    patch("stage_guard.requested_ticket", return_value=TICKET), \
                    patch("host_capabilities.inspect", return_value={"story_ready": True}), \
                    redirect_stderr(err):
                import worker_lifecycle
                try:
                    worker_lifecycle.guard(event)
                except SystemExit as stop:
                    code = stop.code
            return code, err.getvalue()
        code, text = spawn()
        check_eq("30 release (spawn guard): a receipt that still blocks refuses the duplicate", code, 2)
        span = span_with(text, "--operation release")
        result = run_printed(root, task, "30 release (spawn guard)", span, task / "state" / "words" / "door.txt")
        check("30 release (spawn guard): the real controller releases from the file (exit 0)",
              result.returncode == 0, f"{result.returncode} {result.stdout[-300:]} {result.stderr[-300:]}")
        check_eq("30 release (spawn guard): the refusing code no longer refuses", spawn()[0], 0)
        # row 12: a second dispatch nobody is doing; `next` prints the door
        S5.dispatch(c, task, "S5-qa-automator-2", accept=False)
        action = Controller(task).next_action()
        check_eq("12 release (next): a running dispatch is waited on", action.get("action"), "wait_existing_job")
        span = action.get("release") or ""
        check("12 release (next): the field is the bare command (no backticks)", "`" not in span, span)
        result = run_printed(root, task, "12 release (next)", span, task / "state" / "words" / "door.txt")
        check("12 release (next): the real controller releases from the file (exit 0)",
              result.returncode == 0, f"{result.returncode} {result.stdout[-300:]} {result.stderr[-300:]}")
        done = json.loads(result.stdout) if result.returncode == 0 else {}
        check_eq("12 release (next): and says what it freed", done.get("dispatch_id"), "S5-qa-automator-2")
        check_eq("12 release (next): the refusing state no longer holds",
                 Controller(task).next_action().get("action") != "wait_existing_job", True)
        check_eq("12 release (next): the dispatch carries the person's words from the file, whole",
                 Controller(task).state()["dispatches"]["S5-qa-automator-2"].get("released_by_person"), WORDS)
    finally:
        cleanup(root)


def row_31_source_preflight() -> None:
    from source_preflight import check_source_inventory
    import test_ticket_adapter as TA
    root, task = ctrl_project("qa-words-door-gap-")
    try:
        work = task / "work"
        work.mkdir()
        path = work / "source-inventory.json"
        path.write_text(json.dumps({"schema_version": 1, "sources": [TA.gap_source()]}), encoding="utf-8")
        pipeline = {"source_inventory_required": True}
        errors = check_source_inventory(task, pipeline)["errors"]
        text = next((e for e in errors if "SRC-gap" in e and "not accepted by a person" in e), "")
        check("31 accept-gap: the S1 check refuses a source nobody accepted", bool(text), str(errors)[:300])
        span = span_with(text, "accept-gap")
        check_in("31 accept-gap: the printed door is the file form", f"{FLAG} <file>", span)
        # the door is run as printed: it names the inventory (`--output`, which ticket_adapter
        # requires) and the source id; only the `<id>` placeholder is filled
        check_in("31 accept-gap: the printed door names the inventory the check read", f"--output {path}", span)
        head = span[:span.index(FLAG)].replace("<id>", "SRC-gap").split()
        words = task / "state" / "words" / "door.txt"
        words.parent.mkdir(parents=True)
        words.write_bytes(WORDS.encode("utf-8"))
        done = run_script(head[0], *head[1:], FLAG, str(words), cwd=root, env=project_env(root))
        check("31 accept-gap: the real ticket_adapter records the printed door (exit 0)", done.returncode == 0,
              f"{done.returncode} {done.stdout} {done.stderr}")
        after = check_source_inventory(task, pipeline)["errors"]
        check_eq("31 accept-gap: the refusing code no longer refuses that source",
                 [e for e in after if "SRC-gap" in e and "not accepted by a person" in e], [])
    finally:
        cleanup(root)


def main() -> None:
    row_1_2_design_review()
    row_3_empty_scope_at_gate_a()
    rows_4_5_11_dispatch_doors()
    rows_6_7_repair_rounds()
    row_round_pass_keys()
    row_pass_key_counting_and_life()
    row_pass_life_end_to_end()
    row_person_rework_round_pass()
    row_8_not_receipted()
    row_9_mechanical_round()
    row_10_derived_scope()
    rows_12_30_release()
    row_31_source_preflight()
    finish("test_words_doors_controller")


# split: runner piece 1
if __name__ == "__main__":
    main()
