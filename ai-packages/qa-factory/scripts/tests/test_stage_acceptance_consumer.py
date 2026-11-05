#!/usr/bin/env python3
"""X7-6 (t-1765, spec node X7-6): the outcome of S6 is accepted by its CONSUMER, the failure analyst of S7; S6 closes by that record.

The controller side is driven on a patched table (S2 plays the author whose acceptor is a role of S3: the same shape as S6 -> S7 without the
gates A/B and the stand); the writer (`stage_done.record_acceptance`) is driven into the consumer's form; the driver pieces (`s6_awaits`,
`s6_need_record`, `s7_consumer_completion`) are called on a stub `self`. Cases 1-6 of the node:
(1) S6 without a record is not closed, the analyst is dispatched into S7 while S6 awaits, any other role is refused with the door;
(2) `accept` with no quote closes S6; (3) `reject` -> the analyst's finish is `stage_superseded`, the runner's repair is owed;
(4) the repair cap spent -> the conductor's seam (`stage_review_exhausted`), never a code decision; (5) a record for an earlier dispatch of
the author does not count; (6) before the key (no `acceptance_by`) nothing refuses.
"""
import json
import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import SCRIPTS, check, check_eq, check_in, cleanup, finish  # noqa: E402

sys.path.insert(0, str(SCRIPTS))
import acceptance as A  # noqa: E402
import hooklib  # noqa: E402
import stage_done  # noqa: E402
import stage_guard  # noqa: E402
import story_run as SR  # noqa: E402
from event_store import StateConflict  # noqa: E402

import test_controller_stage_acceptance as T  # noqa: E402  (the X2 fixtures: story, dispatch, refused, Patched, quiet, record)

AUTHOR, CONSUMER, OTHER = "qa-requirements-tester", "qa-failure-analyst", "qa-test-strategist"
AUTHOR_STAGE = {"id": "S2", "roles": [AUTHOR], "acceptance_by": CONSUMER}
NEXT_STAGE = {"id": "S3", "roles": [CONSUMER, OTHER]}
FORM = ("inputs_read:\n  - path: work/handoffs/{reviewed}.yaml\n    version: abc\n"
        "header:\n  role: qa-failure-analyst\n  stage: S3\n  window: QA-1\n  verdict: {word}\n{section}")
SECTION = ("stage_acceptance:\n  failure_class: capability\n  quote: \"work/run-report.json#TC-1 has no result row\"\n"
           "  witness_paths: [work/run-report.json]\n")


def awaiting(c, task, did="dA"):
    """The author stops with the open-work word: accepted, stage_complete false, `unresolved` carries the word."""
    receipt = T.dispatch(c, task, did, AUTHOR)
    c.apply("accept", dict(receipt, stage_complete=False, unresolved=A.AWAITS_WORD, reason="S2 awaits the acceptance of the analyst"))


def consumer_state(task):
    return json.loads((task / "pipeline.json").read_text(encoding="utf-8"))


def run() -> None:
    old = hooklib._PROJECT_ROOT_CACHE
    # --- (1) the author stopped awaiting: the consumer is let in, nobody else; `next` names the consumer's stage
    root, task, c = T.story()
    hooklib._PROJECT_ROOT_CACHE = root
    try:
        with T.Patched({"S2": AUTHOR_STAGE, "S3": NEXT_STAGE}):
            check_eq("before the author ran: awaits_acceptance is empty", A.awaits_acceptance(c.state(), "S2"), "")
            awaiting(c, task)
            check_eq("(1) the author's accept with the open-work word keeps S2 open", c.state()["stages"]["S2"]["status"], "pending")
            check_eq("(1) awaits_acceptance (the one reader) names the author's last dispatch", A.awaits_acceptance(c.state(), "S2", consumer_state(task)), "dA")
            check_eq("(1) `next` names S3, the consumer's stage, while S2 awaits", (c.next_action().get("action"), c.next_action().get("stage")),
                     ("prepare_stage", "S3"))
            try:
                T.dispatch(c, task, "dX", OTHER, "S3")
                other = ""
            except StateConflict as exc:
                other = str(exc)
            check_in("(1) any other role into S3 is refused by the controller while S2 awaits", "required prior logical stage incomplete", other)
            text = stage_guard.dispatch_errors(consumer_state(task), "S3", task_root=task, role=OTHER)
            check_in("(1) ... and by the guard, naming the consumer and the door", "S2 awaits the acceptance of qa-failure-analyst", " ".join(text))
            check_in("(1) ... with the command that records the verdict", "--acceptance work/handoffs/", " ".join(text))
            ok = stage_guard.dispatch_errors(consumer_state(task), "S3", task_root=task, role=CONSUMER)
            check_eq("(1) the guard lets the consumer in", [m for m in ok if "S2" in m], [])
            analyst = T.dispatch(c, task, "dN", CONSUMER, "S3")
            check_eq("(1) the analyst is dispatched into S3 while S2 awaits", T.refused(c, analyst, False), "")
            refusal = A.consumer_close_refusal(consumer_state(task), c.state(), "S2")
            check_in("(1) S2 without a record is not closed: stage_done --status done is owed the record", "none stands for dA", refusal)
            # the author's OWN stage_complete=true finish is refused by E-B11 with the consumer's door (E-8), not "the stage critic"
            d = {"stage": "S2", "role": AUTHOR, "id": "dA"}
            said, _ = A.stage_acceptance_refusal(consumer_state(task), d, c.state(), lambda s, e: (e, []))
            check_in("(1) the author's own closing finish names the consumer's dispatch and form", "dispatch `qa-failure-analyst`", said)
            check("(1) ... and does not speak of the stage critic", "stage critic" not in said, said[:200])

            # --- (2) accept with no quote closes S2 (the record is written from the consumer's form)
            handoffs = task / "work" / "handoffs"
            handoffs.mkdir(parents=True, exist_ok=True)
            (handoffs / "dN.yaml").write_text(FORM.format(reviewed="dA", word="ok", section=""), encoding="utf-8")
            code, said = T.quiet(stage_done.record_acceptance, "QA-1", "S2", "work/handoffs/dN.yaml")
            check_eq("(2) a clean `ok` with no quote is recorded (exit 0)", code, 0)
            rec = A.stage_acceptance(consumer_state(task), "S2")
            check_eq("(2) the record: verdict, acceptor, reviewed dispatch, no failure class",
                     (rec["verdict"], rec["acceptor"], rec["reviewed_dispatch"], rec["failure_class"], rec["quote"]), ("accept", CONSUMER, "dA", None, ""))
            check_eq("(2) the stage no longer awaits (the record stands)", A.awaits_acceptance(c.state(), "S2", consumer_state(task)), "")
            check_eq("(2) stage_done --status done is owed nothing", A.consumer_close_refusal(consumer_state(task), c.state(), "S2"), "")
    finally:
        hooklib._PROJECT_ROOT_CACHE = old
        cleanup(root)

    # --- (3) reject: the record is a reject, the stage still awaits, the analyst's finish is `stage_superseded`, the repair is owed
    root, task, c = T.story()
    hooklib._PROJECT_ROOT_CACHE = root
    try:
        with T.Patched({"S2": AUTHOR_STAGE, "S3": NEXT_STAGE}):
            awaiting(c, task)
            c.apply("accept", dict(T.dispatch(c, task, "dN", CONSUMER, "S3"), stage_complete=False, unresolved="stage_superseded", reason="sent back"))
            handoffs = task / "work" / "handoffs"
            handoffs.mkdir(parents=True, exist_ok=True)
            (handoffs / "dN.yaml").write_text(FORM.format(reviewed="dA", word="concerns", section=SECTION), encoding="utf-8")
            code, _ = T.quiet(stage_done.record_acceptance, "QA-1", "S2", "work/handoffs/dN.yaml")
            rec = A.stage_acceptance(consumer_state(task), "S2")
            check_eq("(3) a `concerns` form is recorded as a reject with its class and quote", (code, rec["verdict"], rec["failure_class"]), (0, "reject", "capability"))
            check_eq("(3) a reject does not close: S2 still awaits", A.awaits_acceptance(c.state(), "S2", consumer_state(task)), "dA")
            check_in("(3) ... and stage_done --status done is refused", "none stands for dA", A.consumer_close_refusal(consumer_state(task), c.state(), "S2"))
            # (3) the analyst's finish through the driver piece: a round left -> OpenWork(stage_superseded)
            calls = []
            fake = SimpleNamespace(last_dispatch="dN", stage_verdict_known=lambda form: True,
                                   stage_acceptance_write=lambda stage, dispatch: calls.append((stage, dispatch)),
                                   pipeline=lambda: {"acceptance": {"S6": [T.record("dA", "reject", stage="S6", acceptor=CONSUMER, quote="run-report.json#TC-1")]}},
                                   stage_review_exhausted=lambda *a, **k: calls.append(("exhausted", a[3] is not None)) or "SEAM")
            complete = SR.Driver.s7_consumer_completion(fake, "INNER", 0, 2)
            out = complete("digest")
            check_eq("(3) reject with a round left: the analyst's finish is OpenWork stage_superseded (its work is stale)",
                     (type(out).__name__, out.unresolved), ("OpenWork", "stage_superseded"))
            check_eq("(3) ... the record was written first, from the analyst's own form", calls, [("S6", "dN")])
            # --- (4) the cap spent: the ONE seam decides, never code
            calls.clear()
            out = SR.Driver.s7_consumer_completion(fake, "INNER", 2, 2)("digest")
            check_eq("(4) reject on the last round: the conductor's seam is asked (no_move), its answer is the finish", (out, calls[-1]), ("SEAM", ("exhausted", True)))
            out = SR.Driver.s7_consumer_completion(fake, "INNER", None, None)("digest")
            check_eq("(4) a cap nobody can read is the last round, not a free retry", out, "SEAM")
            # an accept goes to the analyst's own completion
            (handoffs / "dN.yaml").write_text(FORM.format(reviewed="dA", word="ok", section=""), encoding="utf-8")
            fake.pipeline = lambda: {"acceptance": {"S6": [T.record("dA", "accept", stage="S6", acceptor=CONSUMER)]}}
            fake.stage_acceptance_write = lambda stage, dispatch: None
            check_eq("(2) an accept record: the analyst's finish goes on as its own completion", SR.Driver.s7_consumer_completion(fake, "INNER", 0, 2)("d"), "INNER")
            fake.stage_verdict_known = lambda form: False
            calls.clear()
            check_eq("an unknown verdict word goes to the seam, not to a guess", SR.Driver.s7_consumer_completion(fake, "INNER", 0, 2)("d"), "SEAM")

            # --- (5) a record for an earlier dispatch of the author does not count
            awaiting(c, task, "dB")          # the runner repaired: dB is now its last accepted dispatch
            T.write_pipeline(task, acceptance={"S2": [T.record("dA", "accept", stage="S2", role=AUTHOR, acceptor=CONSUMER)]})
            check_eq("(5) the accept for dA does not stop S2 awaiting dB", A.awaits_acceptance(c.state(), "S2", consumer_state(task)), "dB")
            check_in("(5) ... nor does it satisfy stage_done --status done", "none stands for dB", A.consumer_close_refusal(consumer_state(task), c.state(), "S2"))
    finally:
        hooklib._PROJECT_ROOT_CACHE = old
        cleanup(root)

    # --- the three S6 close sites and the open-work wrapper, with and without a consumer
    state = {"stages": {"S6": {"status": "pending"}}, "dispatches": {"S6-qa-runner-1": {"id": "S6-qa-runner-1", "stage": "S6", "role": "qa-runner",
                                                                                      "status": "accepted"}}}
    accepted = {"acceptance": {"S6": [{"verdict": "accept", "reviewed_dispatch": "S6-qa-runner-1"}]}}
    for label, consumer, pipe, want in (("no consumer (the world before the key)", "", {}, False), ("a consumer and no record", CONSUMER, {}, True),
                                        ("a consumer and its accept record", CONSUMER, accepted, False)):
        fake = SimpleNamespace(s6_consumer=lambda consumer=consumer: consumer, controller_state=lambda: state, pipeline=lambda pipe=pipe: pipe,
                               task="QA-1")
        fake.s6_accepted_pending = lambda fake=fake: SR.Driver.s6_accepted_pending(fake)
        raised = False
        try:
            for site in ("s6_reentry", "s6_reprobed_close", "manual_close"):
                SR.Driver.s6_need_record(fake, site)
        except SR.Refusal as exc:
            raised = True
            said = str(exc)
        check_eq(f"close sites, {label}: " + ("refused" if want else "close as today"), raised, want)
        if want:
            check_in("... naming the missing record, the dispatch and the door", "no accept record of qa-failure-analyst stands for S6-qa-runner-1", said)
        fake.s6_awaits = lambda closes, fake=fake: SR.Driver.s6_awaits(fake, closes)
        out = fake.s6_awaits(True)
        check_eq(f"the runner's finish, {label}: " + ("awaits the acceptance" if consumer else "completes as today"),
                 getattr(out, "unresolved", out), A.AWAITS_WORD if consumer else True)
        check_eq(f"... a non-closing finish is passed through, {label}", fake.s6_awaits(False), False)

    # --- (6) before the key: nothing refuses, nothing awaits (E-2), on the shipped-shape table without the key
    root, task, c = T.story()
    hooklib._PROJECT_ROOT_CACHE = root
    try:
        with T.Patched({"S2": {"id": "S2", "roles": [AUTHOR]}, "S3": NEXT_STAGE}):
            awaiting(c, task)
            check_eq("(6) no acceptance_by: nothing awaits", A.awaits_acceptance(c.state(), "S2", consumer_state(task)), "")
            check_eq("(6) ... stage_done owes no record", A.consumer_close_refusal(consumer_state(task), c.state(), "S2"), "")
            check_eq("(6) ... the closing finish of the author is not refused", A.stage_acceptance_refusal(consumer_state(task), {"stage": "S2", "role": AUTHOR, "id": "dA"}, c.state(), lambda s, e: (e, [])), ("", []))
            check_eq("(6) ... `next` stays on S2", c.next_action().get("stage"), "S2")
            try:
                T.dispatch(c, task, "dN", CONSUMER, "S3")
                said = ""
            except StateConflict as exc:
                said = str(exc)
            check_in("(6) ... the consumer is not let in (as before)", "required prior logical stage incomplete", said)
    finally:
        hooklib._PROJECT_ROOT_CACHE = old
        cleanup(root)
    check_eq("the shipped table: S6 is accepted by the analyst, S7 is not yet (X7-6b)",
             (A.consumer_of("S6"), A.consumer_of("S7")), (CONSUMER, ""))


if __name__ == "__main__":
    run()
    finish("test_stage_acceptance_consumer")
