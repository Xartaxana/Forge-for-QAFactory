#!/usr/bin/env python3
"""cc: a part of test_story_run_refusals.py, split by tools/test_split.py (TD-11c). The shared helpers are in story_run_refusals_common."""
import contextlib
import io
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from harness import check, check_eq, check_in  # noqa: E402
from story_run_common import driver_for, jsonl, run_scenarios, seed


# --- C2-8 (t-745): a stage the CODE closes with no role gets a move ------------------------------------------------------------------
CC_MEASURED = ("stage_done: S9 is a controller-managed stage and the controller has not accepted it, so `--status done` would record a "
               "completion no evidence stands behind. A stage a ROLE ran is closed by accepting its dispatch first. If a person decided "
               "to close it anyway: `waiver.py --task QA-9 --stage S9 --block \"no accepted controller stage\" --words-file <file>`.")


class CCRig:
    """A driver whose `stage_done --status` is refused with `text` (a refusal when `check`), whose conductor and waiver are recorded."""

    def __init__(self, text: str = "boom"):
        import story_run
        self.story_run, self.task = story_run, "QA-9"
        self.root, self.task_root, self.env = seed(self.task)
        self.driver = driver_for(self.root, self.env, self.task)
        self.text, self.calls, self.seen, self.scripts = text, [], [], []
        self.driver.conductor = lambda text, *, words="", files=None, words_file=None: self.calls.append(text) or {"action": "continue", "did": "stub"}
        real = self.driver.py

        def py(script, *args, check=False, expect=""):      # C1-7c Q-3: the real `py`'s signature; a G site's `expect` is forwarded
            self.scripts.append((script, [str(a) for a in args]))
            if script == "stage_done.py" and "--status" in args and self.text:
                self.seen.append(list(args))
                if check:
                    retry = lambda: py(script, *args, check=True, expect=expect)      # noqa: E731
                    raise (story_run.gate_refusal(script, 1, self.text, expect, retry) if expect else
                           story_run.Refusal(f"stage_done.py {' '.join(str(a) for a in args[:6])} (exit 1):\n{self.text}", retry=retry))
                return 1, self.text
            if script == "stage_done.py" and "--status" in args and not self.text:
                return 0, ""                                   # the record goes through once the refusal is lifted
            if script in ("waiver.py", "project_decisions.py") and self.waiver is not None:
                if check and self.waiver:      # C1-7c Q-3: a failing script under `check=True` raises what the real `py` raises
                    raise (story_run.gate_refusal(script, self.waiver, "waiver said no", expect) if expect else
                           story_run.Refusal(f"{script} {' '.join(str(a) for a in args[:6])} (exit {self.waiver}):\nwaiver said no"))
                return self.waiver, "waiver said no"
            return real(script, *args, check=check, expect=expect)
        self.waiver = None
        self.driver.py = py

    def controller(self, **stages) -> None:
        self.driver.controller_state = lambda: {"stages": {k: dict(v) for k, v in stages.items()}, "dispatches": {}}

    def pipeline(self, **stages) -> None:
        path = self.task_root / "pipeline.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["stages"].update({k: {"status": v} for k, v in stages.items()})
        path.write_text(json.dumps(data), encoding="utf-8")

    def lift(self, refusal, boundary: str):
        """What `handle_refusal` makes of `refusal`: ('person', the Person) or ('outcome', the string)."""
        self.driver.boundary = boundary
        with contextlib.redirect_stdout(io.StringIO()):
            try:
                return "outcome", self.driver.handle_refusal(refusal)
            except self.story_run.Person as person:
                return "person", person

    def refusal(self, site: str, stage: str, *args, **kwargs):
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                self.driver.record_close(site, stage, *args, **kwargs)
        except self.story_run.Refusal as refusal:
            return refusal
        raise AssertionError("record_close did not refuse")

    def defects(self) -> int:
        return len([e for e in jsonl(self.root / "qa-factory" / "records" / "journal.jsonl") if e.get("event") == "defect_found"])

    def done(self) -> None:
        harness.cleanup(self.root)


def refusal_cc_the_record_of_a_stage_the_code_closed_is_asked_not_called() -> None:
    """CC1, CC8, CC10, CC11 (t-745): a refused `stage_done` after the code's own receipt (S6/S7) is put to the person with `retry` / `stop`
    (no `go on`: no word passes it), no conductor call, ONE defect; the deferred record is written only over its own receipt, at most
    twice idle, then the question comes back with the stage as the boundary."""
    from story_run_common import human_broken
    rig = CCRig()
    try:
        refusal = rig.refusal("s6.nothing", "S6", "--status", "done", "--digest", "nothing to execute", "--no-journal", receipt="S6-code-only-1")
        check_eq("CC1: record_close marks the refusal: site, stage, step", [refusal.close[k] for k in ("site", "stage", "step")],
                 ["s6.nothing", "S6", "record"])
        got, person = rig.lift(refusal, "S6")
        check_eq("CC1: the person is asked (kind code_close), the conductor is not called", (got, person.kind, rig.calls), ("person", "code_close", []))
        check_in("CC1: the question names `retry`, `stop` and says going on is not possible", "Going on as it is is not possible here", person.text)
        check_eq("CC1: its options are retry and stop", person.state_options if hasattr(person, "state_options") else
                 rig.driver.state["code_close"]["S6"]["offer"], ["retry", "stop"])
        check_eq("CC1: the question obeys the human-text rules", human_broken(person.text), [])
        check_eq("CC1: ONE defect_found; the deferred record is kept with the receipt",
                 (rig.defects(), rig.driver.state["code_close"]["S6"]["pending"]["receipt"]), (1, "S6-code-only-1"))
        rig.lift(refusal, "S6")
        check_eq("CC1: the same refusal again files no second defect", rig.defects(), 1)

        # CC10: the receipt was opened again -> nothing is written behind the person's back
        pending = rig.driver.state["code_close"]["S6"]["pending"]
        before = len(rig.seen)
        rig.controller(S6={"status": "running"})
        with contextlib.redirect_stdout(io.StringIO()):
            moved = rig.driver.code_close_step()
        check_eq("CC10: a stage open again drops the record and writes nothing", (moved, pending is not None, len(rig.seen),
                 rig.driver.state["code_close"]["S6"]["pending"]), (False, True, before, None))
        # CC10 (the receipt itself): completed under ANOTHER receipt than the one this record waited for -> dropped, nothing written
        rig.driver.state["code_close"]["S6"]["pending"] = dict(pending, idle=0)
        rig.controller(S6={"status": "completed", "receipt_id": "S6-code-only-2"})
        with contextlib.redirect_stdout(io.StringIO()):
            moved = rig.driver.code_close_step()
        check_eq("CC10: a stage completed under another receipt drops the record and writes nothing",
                 (moved, len(rig.seen) - before, rig.driver.state["code_close"]["S6"]["pending"]), (False, 0, None))
        # CC11: pipeline.json already `done` -> dropped
        rig.driver.state["code_close"]["S6"]["pending"] = dict(pending, idle=1)
        rig.controller(S6={"status": "completed", "receipt_id": "S6-code-only-1"})
        rig.pipeline(S6="done")
        with contextlib.redirect_stdout(io.StringIO()):
            moved = rig.driver.code_close_step()
        check_eq("CC11: a record already on file is dropped", (moved, rig.driver.state["code_close"]["S6"]["pending"]), (False, None))
        # CC8: the ceiling AT and BEYOND: two idle turns (a known refusal that continues), the third turn asks
        rig.pipeline(S6="running")
        rig.driver.state["code_close"]["S6"]["pending"] = dict(pending, idle=0)
        rig.text = "stage already completed"
        turns = []
        for _ in range(2):
            with contextlib.redirect_stdout(io.StringIO()):
                rig.driver.guarded(lambda: turns.append(rig.driver.code_close_step()), {"action": "code_close"})
        check_eq("CC8: two idle turns are tried (the known refusal continues each)", (turns, len(rig.seen) - before),
                 ([], 2))
        got = None
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                rig.driver.guarded(lambda: turns.append(rig.driver.code_close_step()), {"action": "code_close"})
        except rig.story_run.Person as person:
            got = person
        check("CC8: the third turn asks instead of trying (no fourth write)", got is not None and got.kind == "code_close" and len(rig.seen) - before == 2,
              str(got))
        check_in("CC8: the question says the record was tried twice", "tried to record it twice", got.text)
        check_eq("CC8: the boundary is the stage, not `no_trace`", rig.driver.boundary, "S6")
        check_eq("CC8: `retry` resets the count", (rig.driver._answer_code_close("retry", got.text, "S6", ""),
                 rig.driver.state["code_close"]["S6"]["pending"]["idle"]), (True, 0))
    finally:
        rig.done()


def refusal_cc_the_s9_record_and_the_door_of_s0() -> None:
    """CC2 (B2), CC3, CC4, CC7, CC12, CC13, CC16, CC23 (t-745): the measured text of the retro's record is no S0 boundary; the first
    moves of code stay code's; the blocks are read from the state; `go on` / `full retro` / `retry` have one executor."""
    import story_run
    rig = CCRig(CC_MEASURED)
    try:
        rig.controller()                                           # a controller-managed story whose S9 the controller has not accepted
        rig.driver.controller_state = lambda: {"stages": {"S9": {"status": "pending"}}, "dispatches": {}}
        made = []
        rig.driver.code_only = lambda *args, **kwargs: made.append(args)
        refusal = rig.refusal("s9.numbers", "S9", "--status", "done", "--digest", "retro: numbers only")
        got, person = rig.lift(refusal, "S9")
        check_eq("CC2: the measured text on the S9 boundary does NOT answer with the move of S0", (made, got, person.kind), ([], "person", "code_close"))
        rec = rig.driver.state["code_close"]["S9"]
        check_eq("CC13: the block is read from the state; `full retro`, `go on`, `stop` are offered, `retry` is named absent",
                 (rec["block"], rec["offer"]), ("no accepted controller stage", ["full retro", "go on", "stop"]))
        check_in("CC13: and the question says why trying again changes nothing", "Trying again changes nothing here", person.text)
        control = story_run.Refusal(CC_MEASURED)
        rig.lift(control, "S0:ticket")
        check_eq("CC2 control: the same text on the boundary of S0 still answers with the move of S0, once", len(made), 1)
        # CC13 / CC7 / CC23: the executors
        rig.driver.state["asked"] = {"kind": "code_close", "stage": "S9", "dispatch": ""}
        rig.waiver = 1
        got = None
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                rig.driver._answer_code_close("go on", person.text, "S9", "")
        except story_run.Person as held:
            got = held
        check_eq("CC23: a pass the writer refused is held, the block is marked refused", (got is not None, rec["refused"], rec["passed"]),
                 (True, ["no accepted controller stage"], []))
        rig.lift(refusal, "S9")
        check_eq("CC23: the next question has no `go on`", rec["offer"], ["full retro", "stop"])
        check_in("CC23: and says why", "your word could not be recorded against it", rig.driver.state["code_close"]["S9"]["lead"])
        rig.waiver = 0
        rec["refused"] = []
        rig.lift(refusal, "S9")
        with contextlib.redirect_stdout(io.StringIO()):
            took = rig.driver._answer_code_close("go on", "q", "S9", "")
        waivers = [a for s, a in rig.scripts if s == "waiver.py"]
        check_eq("CC7: `go on` writes ONE waiver for the stage and the block, and the block is passed",
                 (took, waivers[-1][:6], rec["passed"]), (True, ["--task", "QA-9", "--stage", "S9", "--block", "no accepted controller stage"],
                                                          ["no accepted controller stage"]))
        rig.lift(refusal, "S9")
        check_eq("CC7: after the pass the block is not offered again", rec["offer"], ["full retro", "stop"])
        check_in("CC7: and the question says the word is recorded", "your word for it is already recorded", rec["lead"])
        # CC13: `full retro` -> stage_done --set retro_mode=full, the record is gone
        with contextlib.redirect_stdout(io.StringIO()):
            took = rig.driver._answer_code_close("full retro", "q", "S9", "")
        sets = [a for s, a in rig.scripts if s == "stage_done.py" and "--set" in a]
        check_eq("CC13: `full retro` sets the retro to its role and drops the record", (took, sets[-1][-2:], "S9" in rig.driver.state["code_close"]),
                 (True, ["--set", "retro_mode=full"], False))
        # CC16: the stage is `skipped` already -> the words are recorded, nothing is executed
        rig.text = "boom"
        refusal = rig.refusal("s9.skip", "S9", "--status", "skipped", "--digest", "retro skipped: x")
        rig.lift(refusal, "S9")
        rig.pipeline(S9="skipped")
        sets_before = len(rig.scripts)
        with contextlib.redirect_stdout(io.StringIO()):
            took = rig.driver._answer_code_close("retry", "q", "S9", "")
        check_eq("CC16: an answer to a stage skipped already executes nothing but the record of the words", (took, [s for s, _a in rig.scripts[sets_before:]]),
                 (True, ["log_append.py"]))
        rig.pipeline(S9="pending")
        # CC12: a step left `running` is settled by code ONCE (recover), then the person is asked with the block `still running`
        rig.pipeline(S6="running")
        rig.driver.state.pop("code_close", None)
        recovered = []
        rig.driver.controller = lambda operation, *args, **kwargs: recovered.append(operation) or {}
        refusal = rig.refusal("s9.skip", "S9", "--status", "skipped", "--digest", "retro skipped: x")
        got, outcome = rig.lift(refusal, "S9")
        check_eq("CC12: the first refusal with a tail runs `recover` once and retries", (got, outcome, recovered), ("outcome", "retry", ["recover"]))
        got, person = rig.lift(refusal, "S9")
        rec = rig.driver.state["code_close"]["S9"]
        check_eq("CC12: the second asks, with the block `still running` and `go on`, `retry`, `stop`",
                 (got, recovered, rec["block"], rec["offer"], rig.calls), ("person", ["recover"], "still running", ["go on", "retry", "stop"], []))
        # CC3 / CC4: the known rows of code keep their move; the second report check is the conductor's
        rig.driver.state.pop("code_close", None)
        budget = rig.refusal("s7.no_failures", "S7", "--status", "done", "--digest", "d", "--no-journal")
        budget.text = "STORY BUDGET: past its ceiling"
        got, person = rig.lift(budget, "S7")
        check_eq("CC3: the story budget keeps its own question", (got, person.kind), ("person", "refusal"))
        check_eq("CC3: and no seam record was made", rig.driver.state.get("code_close", {}).get("S7"), None)
        report = rig.refusal("s9.skip", "S9", "--status", "skipped", "--digest", "d")
        report.text = "report check: damaged"
        rig.driver.state["report_rebuilds"] = {"S9": 1}
        rig.pipeline(S6="done")
        rig.lift(report, "S9")
        check_eq("CC4: the second `report check:` goes to the conductor, not to the seam", (len(rig.calls), rig.driver.state.get("code_close", {}).get("S9")),
                 (1, None))
    finally:
        rig.done()


def refusal_cc_the_factory_file_and_the_words_that_are_not_a_token() -> None:
    """CC14, CC6, CC19, CC20 (t-745): a file of the factory's own that the close needs is the factory's defect (`retry` / `stop`, never
    `go on`); words that are no token go back to the question; the record's retry repeats the tail once."""
    import story_run
    rig = CCRig("")
    try:
        refusal = story_run.Refusal("S7 repairs: the declaration cannot be read", close={"site": "s7.repair_verdicts", "stage": "S7", "step": "entry"})
        got, person = rig.lift(refusal, "S7")
        rec = rig.driver.state["code_close"]["S7"]
        check_eq("CC14: the entry of S7 asks `code_close.factory_file`: retry / stop, one defect", (got, rec["key"], rec["offer"], rig.defects()),
                 ("person", "code_close.factory_file", ["retry", "stop"], 1))
        check_in("CC14: `retry` says the factory's own file is repaired by whoever maintains the factory", "whoever maintains the factory", person.text)
        check_in("CC14: and going on is named as not possible", "the step would stay undone", person.text)
        # CC6: an answer that is no token reaches `unread` with the doors of the question
        sent = {}
        rig.driver.unread = lambda *args, **kwargs: sent.update(kwargs, args=args)
        took = rig.driver._answer_code_close("please look at it", "qtext", "S7", "")
        check_eq("CC6: no token -> the doors are the options, with `again` to show the question", (took, sent["doors"], callable(sent.get("again"))),
                 (False, ("retry", "stop"), True))
        # CC19: the conductor's options of this kind reach the SAME executor
        called = []
        rig.driver._answer_code_close = lambda *args, **kwargs: called.append(args[0]) or True
        asked = {"kind": "code_close", "options": [{"token": "full retro", "move": "site_door"}], "words_file": ""}
        with contextlib.redirect_stdout(io.StringIO()):
            took = rig.driver.take_seam_answer("full retro", asked, "q", "S9", "")
        check_eq("CC19: take_seam_answer hands a code_close token to the one executor", (took, called), (True, ["full retro"]))
        # CC20: a known `retry` of the record repeats the WHOLE record, the tail once
        del rig.driver._answer_code_close
        rig.text = "expected_revision 4"
        tail = [["--event", "dispatch_skipped", "--task", "QA-9", "--reason", "S7: no failures to triage"]]
        answers = iter([True])
        original = rig.driver.py

        def py(script, *args, check=False, expect=""):      # C1-7c Q-3: the real `py`'s signature; `expect` reaches the stub it wraps
            if script == "stage_done.py" and next(answers, False) is False:
                rig.text = ""
            return original(script, *args, check=check, expect=expect)
        rig.driver.py = py
        rig.scripts.clear()
        with contextlib.redirect_stdout(io.StringIO()):
            rig.driver.guarded(lambda: rig.driver.record_close("s7.no_failures", "S7", "--status", "done", "--digest", "d", "--no-journal",
                                                               tail=tail, receipt="S7-code-only-1"), {"action": "x"})
        check_eq("CC20: the retried record writes the stage and the tail ONCE each",
                 [s for s, _a in rig.scripts if s in ("stage_done.py", "log_append.py")].count("log_append.py"), 1)
    finally:
        rig.done()


def refusal_cc_the_moves_of_code_stay_and_the_unknown_is_asked_with_what_is_known() -> None:
    """CC5, CC12 (recover failed), CC21, CC22 and the dry run (t-745): a refusal whose own `recover` refused goes to the conductor with both
    texts; a `recover` that refused at S9 is not run twice and its words stay beside the question; a key with no price rows is asked
    without prices and files ONE more defect; the refusal of S0's record is not this kind; a dry run writes nothing."""
    import no_move as NM
    import story_run
    rig = CCRig("event committed; the dispatch is recorded already")
    try:
        # CC5: a known `recover` row that refused falls through to the conductor, with both texts
        def refuse(operation, *args, **kwargs):
            raise story_run.Refusal("controller recover: nothing to recover here")
        rig.driver.controller = refuse
        refusal = rig.refusal("s7.no_failures", "S7", "--status", "done", "--digest", "d", "--no-journal")
        got, outcome = rig.lift(refusal, "S7")
        check_eq("CC5: the conductor is called once, the seam is not asked", (got, len(rig.calls), rig.driver.state.get("code_close")), ("outcome", 1, None))
        check("CC5: and it is shown both texts", "event committed;" in rig.calls[0] and "nothing to recover here" in rig.calls[0], rig.calls[0][:300])
        # CC22: the record of S0 is no code_close site (B1): an unmarked refusal takes the road of the conductor
        rig.calls.clear()
        rig.text = "boom"
        plain = story_run.Refusal("stage_done.py --task QA-9 --stage S0 (exit 1):\nboom")
        got, outcome = rig.lift(plain, "S0")
        check_eq("CC22: S0's record is the conductor's, as before", (got, len(rig.calls), rig.driver.state.get("code_close")), ("outcome", 1, None))
        # CC12 (recover failed): asked, ONE recover only, its words in the details beside the refusal
        rig.pipeline(S6="running")
        recovers = []

        def refuse_once(operation, *args, **kwargs):
            recovers.append(operation)
            raise story_run.Refusal("controller recover: the checkpoint is not readable")
        rig.driver.controller = refuse_once
        marked = rig.refusal("s9.skip", "S9", "--status", "skipped", "--digest", "retro skipped: x")
        got, person = rig.lift(marked, "S9")
        rec = rig.driver.state["code_close"]["S9"]
        check_eq("CC12: recover refused -> the person is asked, with `go on` for the block still running",
                 (got, recovers, rec["block"], rec["offer"]), ("person", ["recover"], "still running", ["go on", "retry", "stop"]))
        check_in("CC12: the lead says the factory could not settle it", "could not settle that by itself", rec["lead"])
        check_in("CC12: the writer's own words are beside the refusal (details)", "the checkpoint is not readable", rec["details"])
        rig.lift(marked, "S9")
        check_eq("CC12: a second refusal does not run `recover` again", recovers, ["recover"])
        # the dry run: the deferred record is announced and nothing is written
        pending = {"site": "s6.nothing", "args": ["--status", "done", "--digest", "x"], "tail": [], "receipt": "S6-code-only-1", "idle": 0}
        rig.driver.state["code_close"]["S6"] = {"site": "s6.nothing", "step": "record", "key": "code_close.stage", "block": "", "offer": ["retry", "stop"],
                                                "passed": [], "refused": [], "filed": [], "pending": pending}
        rig.controller(S6={"status": "completed", "receipt_id": "S6-code-only-1"})
        rig.pipeline(S6="running")
        rig.driver.dry = True
        before = len(rig.seen)
        printed = io.StringIO()
        with contextlib.redirect_stdout(printed):
            moved = rig.driver.code_close_step()
        check_eq("dry run: the turn is spent, nothing is written", (moved, len(rig.seen) - before), (True, 0))
        check_in("dry run: and the line says so", "dry run: the deferred record of S6 is not written", printed.getvalue())
    finally:
        rig.done()
    # CC21: no price rows for the key -> the question without prices and ONE more defect (FR-41)
    rig = CCRig()
    saved = NM.load_question_prices
    try:
        NM.load_question_prices = lambda: {}
        entry = story_run.Refusal("S7 repairs: the declaration cannot be read", close={"site": "s7.repair_verdicts", "stage": "S7", "step": "entry"})
        got, person = rig.lift(entry, "S7")
        check_eq("CC21: the question is shown (kind code_close) with the option lines, no price lines",
                 (got, person.kind, "`retry`" in person.text, "the factory: nothing runs" in person.text), ("person", "code_close", True, False))
        check_eq("CC21: the close's own defect and ONE for the missing prices", rig.defects(), 2)
    finally:
        NM.load_question_prices = saved
        rig.done()


def refusal_cc_fix_round_two_blocks_two_episodes_full_retro_and_s6_closes() -> None:
    """The fix round of t-914 (t-907 attempt 2): F-1 the two blocks of one S9 record come as TWO questions, in that order (spec 3.6(3));
    F-5 a record that went through leaves no stale facts, so the next episode of the stage is a clean one (I8); F-7 `full retro` is followed
    by the retro analyst's own session; F-6 the S6 closes go through `close_by_code(finalize=False)` and keep today's order and texts."""
    import story_run
    rig = CCRig(CC_MEASURED)
    try:
        rig.pipeline(S3="running")
        rig.driver.controller_state = lambda: {"stages": {"S9": {"status": "pending"}}, "dispatches": {}}
        recovers = []

        def refuse(operation, *args, **kwargs):
            recovers.append(operation)
            raise story_run.Refusal("controller recover: the checkpoint is not readable")
        rig.driver.controller = refuse
        refusal = rig.refusal("s9.numbers", "S9", "--status", "done", "--digest", "retro: numbers only")
        # F-1 step 1: the tail is non-empty and `recover` refused -> the question with the block `still running`
        got, first = rig.lift(refusal, "S9")
        rec = rig.driver.state["code_close"]["S9"]
        check_eq("F-1: the first question is `still running`, with `go on`, `retry`, `stop`", (got, rec["block"], rec["offer"], rig.calls),
                 ("person", "still running", ["go on", "retry", "stop"], []))
        # step 2: `go on` passes it
        rig.driver.state["asked"] = {"kind": "code_close", "stage": "S9", "dispatch": ""}
        rig.waiver = 0
        with contextlib.redirect_stdout(io.StringIO()):
            took = rig.driver._answer_code_close("go on", first.text, "S9", "")
        check_eq("F-1: `go on` passes `still running`", (took, rec["passed"]), (True, ["still running"]))
        # steps 3-4: the same record is refused again, now for the controller's stage; the pipeline still holds the tail
        got, second = rig.lift(refusal, "S9")
        check_eq("F-1: the SECOND question is `no accepted controller stage` with `full retro`, `go on`, `stop` (a pass is not asked twice)",
                 (got, rec["block"], rec["offer"], recovers, rig.calls),
                 ("person", "no accepted controller stage", ["full retro", "go on", "stop"], ["recover"], []))
        check("F-1: and it is another question than the first", second.text != first.text and "Trying again changes nothing here" in second.text,
              second.text[:200])
        with contextlib.redirect_stdout(io.StringIO()):
            rig.driver._answer_code_close("go on", second.text, "S9", "")
        rig.lift(refusal, "S9")
        check_eq("F-1: with both passed only `full retro` and `stop` remain", (rec["passed"], rec["offer"]),
                 (["still running", "no accepted controller stage"], ["full retro", "stop"]))
        # F-5: the record goes through -> the facts of the episode are gone; the next episode runs `recover` again and asks afresh
        rig.text = ""
        with contextlib.redirect_stdout(io.StringIO()):
            rig.driver.record_close("s9.numbers", "S9", "--status", "done", "--digest", "retro: numbers only")
        check_eq("F-5: a record that went through drops the stage's facts", "S9" in rig.driver.state.get("code_close", {}), False)
        rig.text = CC_MEASURED
        again = rig.refusal("s9.numbers", "S9", "--status", "done", "--digest", "retro: numbers only")
        got, third = rig.lift(again, "S9")
        fresh = rig.driver.state["code_close"]["S9"]
        check_eq("F-5: the second episode runs `recover` again and offers `go on` for `still running` afresh",
                 (got, recovers, fresh["passed"], fresh["block"], fresh["offer"]),
                 ("person", ["recover", "recover"], [], "still running", ["go on", "retry", "stop"]))
        # F-7 (CC13, second half): `full retro` sets the mode, and the next S9 step calls the retro analyst
        rig.pipeline(S3="done")
        rig.driver.state.pop("code_close", None)
        got, last = rig.lift(rig.refusal("s9.numbers", "S9", "--status", "done", "--digest", "retro: numbers only"), "S9")
        with contextlib.redirect_stdout(io.StringIO()):
            took = rig.driver._answer_code_close("full retro", last.text, "S9", "")
        ran, original = [], rig.driver.py
        rig.driver.after_gate_B, rig.driver.rebuild_report = (lambda: None), (lambda *a, **k: None)
        rig.driver.state["retro_asked"] = True
        rig.driver.run_role = lambda *args, **kwargs: ran.append(args)
        rig.driver.py = lambda script, *args, check=False, expect="": ((0, "") if script == "retro_numbers.py"
                                                                         else original(script, *args, check=check, expect=expect))   # C1-7b: G5 passes `expect`
        with contextlib.redirect_stdout(io.StringIO()):
            rig.driver.stage_S9()
        check_eq("F-7: after `full retro` the next S9 step runs the retro analyst, and no numbers-only record is made",
                 (took, rig.driver.pipeline().get("retro_mode"), ran, "S9" in rig.driver.state.get("code_close", {})),
                 (True, "full", [("S9", "qa-retro-analyst")], False))
    finally:
        rig.done()
    # F-6: the three S6 closes are `close_by_code(finalize=False)` after the site's OWN finalize; the order and the refusal texts stand
    rig = CCRig("")
    try:
        rig.driver.stage_scope = lambda stage, kind="": {"scope": []}
        rig.driver.controller_state = lambda: {"stages": {"S6": {"status": "pending"}}, "dispatches": {}}
        rig.driver.code_only = lambda stage, reason, evidence: "S6-code-only-1"
        finalize = [(0, "")]
        original = rig.driver.py

        def py(script, *args, check=False, expect=""):      # C1-7c Q-3: the real `py`'s signature; honours `check` (neutral today: no finalize_task.py call passes it)
            if script == "finalize_task.py":
                rig.scripts.append((script, list(args)))
                if check and finalize[0][0]:
                    raise (story_run.gate_refusal(script, finalize[0][0], finalize[0][1], expect) if expect else
                           story_run.Refusal(f"{script} (exit {finalize[0][0]}):\n{finalize[0][1]}"))
                return finalize[0]
            return original(script, *args, check=check, expect=expect)
        rig.driver.py = py
        with contextlib.redirect_stdout(io.StringIO()):
            rig.driver.stage_S6()
        order = [s for s, _a in rig.scripts if s in ("finalize_task.py", "stage_done.py")]
        record = next(a for s, a in rig.scripts if s == "stage_done.py" and "--status" in a)
        check_eq("F-6: S6 with nothing to execute: ONE finalize, then the record (same words, no journal row of its own)",
                 (order, record[record.index("--digest"):]), (["finalize_task.py", "stage_done.py"], ["--digest", "nothing to execute", "--no-journal"]))
        finalize[0] = (1, "report not buildable")
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                rig.driver.stage_S6()
            raised = None
        except story_run.Refusal as refusal:
            raised = refusal
        check_eq("F-6: a finalize that fails keeps S6's own refusal text, unmarked (the conductor's)",
                 (raised is not None and raised.text, raised is not None and not raised.close),
                 ("S6 nothing to execute: finalize_task.py exit 1: report not buildable", True))
        finalize[0] = (0, "")
        rig.text = "boom"
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                rig.driver.stage_S6()
            marked = None
        except story_run.Refusal as refusal:
            marked = refusal
        check_eq("F-6: a refused record is marked with the site (the seam's)", marked is not None and marked.close and
                 [marked.close[k] for k in ("site", "stage", "step")], ["s6.nothing", "S6", "record"])
    finally:
        rig.done()
    # F-3: ONE short-circuit for an answer after the stage is done; its words are the four old callers' words, byte for byte
    rig = CCRig("")
    try:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rig.driver.after_close("S9", "  my words ")
        row = [a for s, a in rig.scripts if s == "log_append.py"][-1]
        check_eq("F-3: the helper prints the old line and files the journal row, its note by a file",
                 (out.getvalue(), row[:5]), ("S9 is done already; recording the words and going on\n",
                                             ["--event", "human_answer", "--task", "QA-9", "--notes-file"]))
        check_eq("F-3: the file named holds the note whole", Path(row[5]).read_text(encoding="utf-8"),
                 story_run._answer_note("S9 (after close): ", "my words"))
    finally:
        rig.done()


CC9_WATCHED = {"stage_S6", "manual_close", "stage_S7", "s7_close", "stage_S9", "close_by_code"}


CC9_SITE_FREE = {"record_close", "close_by_code", "code_close_step"}      # retry lambda, pass-through, replay of a deferred record's own site


CC9_SITE_ARG = {"close_receipt": 0, "record_close": 0}                    # the position of `site` where it is positional; close_by_code: keyword only


def cc9_findings(source, sites) -> list:
    """THE predicate of CC9 (used by the census of the driver set AND by the planted controls): what is wrong in `source` (a text, or a list of texts).
    (1) a watched function that does not exist; (2) in a watched function a bare `self.code_only(` or `self.py("stage_done.py", ... "--status")`;
    (3) anywhere, a `close_by_code` / `close_receipt` / `record_close` call whose `site` is not a LITERAL non-empty key of `sites`
    (except inside `CC9_SITE_FREE`)."""
    import ast
    texts = [source] if isinstance(source, str) else list(source)      # one text, or the text of every file of the driver set (parsed apart)
    functions = [n for text in texts for n in ast.walk(ast.parse(text)) if isinstance(n, ast.FunctionDef)]
    problems = [f"missing:{name}" for name in sorted(CC9_WATCHED - {f.name for f in functions})]
    owner = {}
    for fn in functions:                                         # BFS: the outermost function owns a nested call
        for call in ast.walk(fn):
            owner.setdefault(id(call), fn.name)
    for fn in functions:
        for call in ast.walk(fn):
            if not (isinstance(call, ast.Call) and isinstance(call.func, ast.Attribute) and isinstance(call.func.value, ast.Name)
                    and call.func.value.id == "self") or owner.get(id(call)) != fn.name:
                continue
            attr = call.func.attr
            strings = [a.value for a in call.args if isinstance(a, ast.Constant) and isinstance(a.value, str)]
            if fn.name in CC9_WATCHED and (attr == "code_only" or (attr == "py" and "stage_done.py" in strings and "--status" in strings)):
                problems.append(f"bypass:{fn.name}:{call.lineno}")
            if attr in ("close_by_code", "close_receipt", "record_close") and fn.name not in CC9_SITE_FREE:
                given = next((k.value for k in call.keywords if k.arg == "site"), None)
                if given is None and attr in CC9_SITE_ARG and len(call.args) > CC9_SITE_ARG[attr]:
                    given = call.args[CC9_SITE_ARG[attr]]
                if not (isinstance(given, ast.Constant) and isinstance(given.value, str) and given.value in sites):
                    problems.append(f"site:{fn.name}:{call.lineno}:{attr}")
    return problems


def refusal_cc9_every_close_of_s6_s7_s9_goes_through_the_one_record() -> None:
    """CC9 (t-745 detector): in the stage functions that close a stage by code, no `stage_done.py --status` call and no bare `self.code_only(`
    is left - the close is `record_close` / `close_receipt` (or `close_by_code`, which holds them) - and every such call carries a LITERAL
    `site` that is a key of `CODE_CLOSE_SITES` (an unmarked refusal would go to the conductor in silence). The watched names must exist."""
    import story_run
    sites = set(story_run.CODE_CLOSE_SITES)
    source = harness.driver_text()
    check_eq("CC9: no close of S6/S7/S9 by code bypasses record_close / close_receipt, every call carries its site, every watched name exists",
             cc9_findings([text for _path, text in harness.driver_sources()], sites), [])
    check_eq("F-3: the after-close line lives in the one helper, and its four callers call it",
             (source.count("is done already; recording the words and going on"), source.count("self.after_close(")), (1, 4))
    # the negative controls: the SAME predicate sees each planted defect (and passes the planted good call)
    def planted(line: str, others: bool = True) -> str:
        rest = "".join(f"    def {name}(self):\n        pass\n" for name in sorted(CC9_WATCHED - {"stage_S6"})) if others else ""
        return "class D:\n    def stage_S6(self):\n        " + line + "\n" + rest

    plants = {
        "a stage_done call returned to py": ("self.py('stage_done.py', '--task', t, '--status', 'done', check=True)", "bypass:stage_S6"),
        "a bare code_only": ("self.code_only('S6', r, e)", "bypass:stage_S6"),
        "close_by_code with site=''": ("self.close_by_code('S6', r, e, finalize=False, site='')", "site:stage_S6"),
        "close_by_code with no site": ("self.close_by_code('S6', r, e, finalize=False)", "site:stage_S6"),
        "close_by_code with a site that is no key": ("self.close_by_code('S6', r, e, finalize=False, site='s6.nope')", "site:stage_S6"),
        "record_close with a variable site": ("self.record_close(site, 'S6', '--status', 'done')", "site:stage_S6"),
        "close_receipt with an empty positional site": ("self.close_receipt('', 'S6', r, e)", "site:stage_S6"),
    }
    for label, (line, expect) in plants.items():
        got = cc9_findings(planted(line), sites)
        check(f"CC9 control: {label} is red", any(p.startswith(expect) for p in got), str(got))
    check_eq("CC9 control: the planted good call is green",
             cc9_findings(planted("self.close_by_code('S6', r, e, finalize=False, site='s6.nothing')"), sites), [])
    check_eq("CC9 control: a renamed watched function is red",
             cc9_findings(planted("self.close_by_code('S6', r, e, finalize=False, site='s6.nothing')", others=False), sites),
             [f"missing:{name}" for name in sorted(CC9_WATCHED - {"stage_S6"})])


def main() -> None:
    run_scenarios([], [
        refusal_cc_the_record_of_a_stage_the_code_closed_is_asked_not_called,
        refusal_cc_the_s9_record_and_the_door_of_s0,
        refusal_cc_the_factory_file_and_the_words_that_are_not_a_token,
        refusal_cc_the_moves_of_code_stay_and_the_unknown_is_asked_with_what_is_known,
        refusal_cc_fix_round_two_blocks_two_episodes_full_retro_and_s6_closes,
        refusal_cc9_every_close_of_s6_s7_s9_goes_through_the_one_record,
    ])
    harness.finish("test_story_run_refusals_cc")


# split: runner piece 1
if __name__ == "__main__":
    main()
