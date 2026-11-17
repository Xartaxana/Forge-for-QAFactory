#!/usr/bin/env python3
"""The doors the controller's blocks name are doors that exist, and the four families open.

`design/controller-blocks.md` gives every block a route; for many of them the route is a
command the block's own message names. Naming a door is not opening one - that is how
`S3 structured test plan invalid` and `S1 source collection pending/invalid` both came to
advertise `waiver.py --stage ... --block` while the stage stayed shut whatever the person said
(five conductor sessions and $1.94 in TP1-13797 run 5).

Two checks, in the order they pay:

  1. Every command named in the walk EXISTS - an operation the controller knows, or a script in
     the package. Cheap, and it covers every `command` row at once: a door that is not there
     cannot open, and a rename elsewhere in the factory is caught here instead of in a run.
  2. The four door families actually open (`DOOR_FAMILIES`, one row each: `checkpoint`,
     `gate-decision`, `semantic_reopen`, `recover`): the block fires, the door is called, and the
     same request goes through or the door leaves the state its walk row promises. A family proved
     end to end is worth more than a hundred asserted by reading. Each row names its world: the
     recorded story `fixtures/stories/cart-1/` where the block is reachable from the recorded
     state, the `BASE` synthetic world otherwise.
"""
import contextlib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
from harness import check, check_eq, check_in  # noqa: E402

sys.path.insert(0, str(harness.SCRIPTS))
import controller as C  # noqa: E402
from controller import Controller, StateConflict  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_controller_state as BASE  # noqa: E402

WALK = harness.PLUGIN_ROOT / "design" / "controller-blocks.md"
OPERATION_RE = re.compile(r"--operation ([a-z_-]+)")
SCRIPT_RE = re.compile(r"`?([a-z][a-z0-9_]*\.py)")


def command_rows() -> list:
    rows = []
    for line in WALK.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| `"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split(" | ")]
        if len(cells) == 5 and cells[3].strip("`") == "command":
            rows.append((cells[0].strip("`"), cells[2], cells[4]))
    return rows


# --- the four door families, end to end ---------------------------------------------------------
# One row per family (P16: the red line names the family). Each row: its world, the walk row that
# holds its block (found by block text, never by line number: lines move, the needle does not), the
# token its "way through" cell must name, and `run(needle, task)`. Expectations come from the walk
# row's own cells, never from the controller's output. Each row runs on its own copy of its world;
# a row that raises is a red line of its own family and does not hide the others.

@contextlib.contextmanager
def pinned(project):
    """The hook layer reads THIS project for the length of the block; env and cache are restored (E5)."""
    import hooklib
    with hooklib.selftest_root_restored():
        hooklib.pin_project_root(project)
        yield


@contextlib.contextmanager
def synthetic_world():
    """The `BASE` world: a fresh project with one initialized story (scope TC-1, source revision `src-1`)."""
    root = harness.temp_dir("qa-controller-doors-")
    try:
        with pinned(root):
            harness.mark_project(root)
            task = root / "qa-factory" / "artifacts" / root.name
            (task / "work").mkdir(parents=True)
            Controller(task).apply("initialize", {"scope": ["TC-1"], "source_revision": "src-1",
                                                  "known_paths": {"root": str(task)}, "idempotency_key": "init"})
            yield task
    finally:
        harness.cleanup(root)


@contextlib.contextmanager
def recorded_world():
    """A copy of the recorded story `cart-1` (a task root in its own project); its Gate A is approved and current."""
    import scenario_walk
    world = scenario_walk.build_world(scenario_walk.load_story("cart-1"))
    copy = scenario_walk.copy_world(world)
    try:
        with pinned(copy.parents[2]):
            yield copy
    finally:
        harness.cleanup(copy.parents[2])


def refusal_of(call) -> str:
    """The text of the refusal `call` raises (any class: DerivedViewStale is not a StateConflict), '' when it went through."""
    try:
        call()
    except Exception as refusal:
        return str(refusal)
    return ""


def gate_a_statuses(controller) -> list:
    return [d["status"] for d in controller.state()["decisions"].values() if d.get("gate") == "A"]


def row_checkpoint(needle, task):
    """The request goes through `controller.apply("checkpoint", ...)`: the operation's body, not the CLI flags of `--operation checkpoint`."""
    controller = Controller(task)
    BASE.accept_stage(controller, task, "S0")
    controller.apply("dispatch", {"id": "d-live", "stage": "S1", "role": "qa-scout",
                                  "scope": ["TC-1"], "input_hash": "ctx", "budget": {},
                                  "known_paths": {}, "idempotency_key": "d-live"})
    revise = {"scope": ["TC-1", "TC-2"], "plan_revision": "plan-2",
              "reason": "the person added a case at the gate",
              "idempotency_key": "revise-1"}
    try:
        controller.apply("revise_plan", dict(revise))
        check("checkpoint: active work blocks a scope revision", False)
    except (StateConflict, ValueError) as refusal:
        check_in("checkpoint: and the block names the door", needle, str(refusal))

    controller.apply("checkpoint", {"id": "d-live", "status": "paused",
                                    "checkpoint": {"completed": [], "next": "resume the scout"},
                                    "reason": "the person is revising the scope",
                                    "idempotency_key": "cp-1"})
    controller.apply("revise_plan", dict(revise, idempotency_key="revise-2"))
    state = controller.state()
    check_eq("checkpoint: after the door the same request goes through",
             sorted(state.get("scope") or []), ["TC-1", "TC-2"])
    check_eq("checkpoint: and the dispatch is where the door left it",
             (state["dispatches"]["d-live"] or {}).get("status"), "paused")


def row_gate_decision(needle, task):
    controller = Controller(task)
    for number in range(5):
        BASE.accept_stage(controller, task, f"S{number}")
    BASE.seed_plan(task)
    hand_built = BASE.bind_gate_a(task, {
        "id": "A", "gate": "A", "action": "approve", "status": "approved", "authorization_source": "human",
        "source_revision": "stale-rev", "scope": ["TC-1"], "input_revision": "src-1", "idempotency_key": "A"})
    check_in("gate-decision: a decision bound to a stale source revision is refused, naming the block", needle,
             refusal_of(lambda: controller.apply("decision", dict(hand_built))))
    check_eq("gate-decision: and nothing is recorded", gate_a_statuses(controller), [])
    # the door itself: `--operation gate-decision` (pins the project, builds the request from the revision the story holds now, records)
    words = task / "work" / "gate-a-words.txt"
    words.write_text("approve - the person's word (fixture)", encoding="utf-8")
    code, out, err = harness.run_controller_inprocess(
        ["--task-root", str(task), "--operation", "gate-decision", "--gate", "A", "--words-file", str(words)], task.parents[2])
    check("gate-decision: the door exits 0", code == 0, f"exit {code}: {err[-300:]}")
    check_eq("gate-decision: after the door the same decision is recorded", gate_a_statuses(controller), ["approved"])


def row_semantic_reopen(needle, task):
    controller = Controller(task)
    events = len(controller.store.read())
    request = {"kind": "key_order", "semantic_hash": "changed", "previous_semantic_hash": "changed",
               "idempotency_key": "tn-1"}
    check_in("semantic_reopen: a normalisation whose plan content really changed is refused, naming the door", needle,
             refusal_of(lambda: controller.apply("technical_normalize", dict(request))))
    check_eq("semantic_reopen: and the refusal wrote no event", len(controller.store.read()), events)
    check_eq("semantic_reopen: the recorded Gate A is approved before the door", gate_a_statuses(controller), ["approved"])
    affected = (controller.state().get("scope") or [])[:1]
    controller.apply("semantic_reopen", {"reason": "the plan content changed", "affected_scope": affected,
                                         "idempotency_key": "so-1"})
    # The walk row's way through is "semantic_reopen, then a new gate decision": the door itself opens and leaves
    # the Gate A stale (a normalisation cannot keep a Gate A whose content has left it).
    check_eq("semantic_reopen: the door is one committed event", len(controller.store.read()), events + 1)
    check_eq("semantic_reopen: and it leaves the Gate A stale, ready for a new gate decision",
             gate_a_statuses(controller), ["stale"])


def row_recover(needle, task):
    """The door is `controller.recover()`: the operation's body (`--operation recover` calls exactly it)."""
    import dashboard_refresh
    controller = Controller(task)
    original = dashboard_refresh.refresh_for_task
    fresh = []

    def failing(_task):
        raise RuntimeError("the render died")

    def current(task_root):
        fresh.append(str(task_root))
        return {"status": "current"}

    marker = task / "state" / "dashboard-deferred.json"
    try:
        dashboard_refresh.refresh_for_task = failing
        stale = refusal_of(lambda: controller.apply("dispatch", {
            "id": "d1", "stage": "S0", "role": "qa-scout", "scope": ["TC-1"], "input_hash": "h", "budget": {},
            "known_paths": {}, "idempotency_key": "d1"}))
        check_in("recover: a failed refresh after a commit is refused, naming the block", needle, stale)
        check("recover: and the view is recorded as stale", marker.is_file())
        committed = len(controller.store.read())
        dashboard_refresh.refresh_for_task = current
        controller.recover()
    finally:
        dashboard_refresh.refresh_for_task = original
    check("recover: after the door the view is fresh (refreshed, and the stale marker is gone)",
          bool(fresh) and not marker.exists(), f"refreshed={fresh} marker={marker.exists()}")
    check_eq("recover: and the committed action is NOT repeated (the event count is unchanged)",
             len(controller.store.read()), committed)


# family -> (world, block text of its walk row, token the row's way-through cell names, the row)
DOOR_FAMILIES = {
    "checkpoint": (synthetic_world, "checkpoint active work before revising scope", "--operation checkpoint", row_checkpoint),
    "gate-decision": (synthetic_world, "decision references stale source revision", "gate-decision", row_gate_decision),
    "semantic_reopen": (recorded_world, "semantic content changed; use semantic_reopen", "semantic_reopen", row_semantic_reopen),
    "recover": (synthetic_world, "event committed; derived view not refreshed", "--operation recover", row_recover),
}


def doors_open_end_to_end(rows) -> None:
    for family, (world, key, token, run) in DOOR_FAMILIES.items():
        found = [(block, way) for _, block, way in rows if key in block]
        check(f"{family}: the walk holds a `command` row for its block", bool(found), key)
        if not found:
            continue                    # E3: the family fails by name, never silently green
        block, way = found[0]
        check_in(f"{family}: and its way-through cell names the door", token, way)
        needle = block.split("{")[0].strip()
        try:
            with world() as task:
                run(needle, task)
        except Exception as error:      # a row that cannot run is its own family's red line
            check(f"{family}: the row ran to its end", False, f"{type(error).__name__}: {error}")


# --- T9c: the conductor's launch is told what code will check in it (mech 2.9, card T9c) ---------------------------------
# Expected values: the heading order and the row ids come from mech 2.9 / 5.5 (`conductor_answer` rows hold on every launch, `move:<id>`
# rows when the move is open); the refusal texts are the OLD no_move.py's output, captured from a byte copy before the edit (EC-1).
LAUNCH_HEAD = "## What code will check in this launch"
CONDUCTOR_FACTS = {"rework_stages": ["S5"], "rework_roles": {"S5": ["qa-automator"]}, "scope": ["TC-1", "TC-2"], "causes": ["test_defect"]}
GOOD_ARGS = {"stage": "S5", "role": "qa-automator", "cases": ["TC-1"], "cause": "test_defect"}
SECTION_ROWS = {      # open moves, site words -> the row ids the section lists, in order
    "rework-open": (["rework_stage", "person_does"], ("read",), ["no_move:options", "no_move:prose", "no_move:class", "no_move:args"]),
    "no-rework": (["stop_here"], (), ["no_move:options", "no_move:prose", "no_move:class"]),
    "no-move-open": ([], (), ["no_move:options", "no_move:prose", "no_move:class"]),
}


def launch_section() -> None:
    import no_move as NM
    for label, (open_ids, site, ids) in SECTION_ROWS.items():
        text = NM.moves_section(NM.data(), open_ids, CONDUCTOR_FACTS, site)
        got = re.findall(r"^- \[([a-z_]+:[a-z_]+)\]", text.split(LAUNCH_HEAD)[-1], re.M)
        check_eq(f"launch-section/{label}: the rows of the open moves, after the conductor_answer rows", got, ids)
        heads = [h for h in ("## Moves open here", "## Answers this question already takes", LAUNCH_HEAD) if h in text]
        check_eq(f"launch-section/{label}: the headings keep their order, the new one last (E-T9c-5)", [text.index(h) for h in heads],
                 sorted(text.index(h) for h in heads))
        check_eq(f"launch-section/{label}: all three or two headings by the site words", len(heads), 3 if site else 2)
    import stage_joints as SJ
    rows, _why = SJ.load_rows()
    bare = harness.temp_dir("qa-launch-none-") / "stage-joints.json"
    import json
    bare.write_text(json.dumps(dict(rows, joints=[r for r in rows["joints"] if not str(r.get("check")).startswith("no_move:")])), encoding="utf-8")
    real = SJ.DATA
    try:
        SJ.DATA = bare
        text = NM.moves_section(NM.data(), ["stop_here"], CONDUCTOR_FACTS)
    finally:
        SJ.DATA = real
    check_eq("launch-section/nothing: no row holds -> the `none` line (E24, E-T9c-4)", text.split(LAUNCH_HEAD)[-1].strip(), NM.NOTHING_CHECKED)


UNREADABLE_ROWS = {      # what the rows file holds -> the reason the first line of the section ends with (t-1087, FR-41 / FR-59)
    "absent": (None, "absent.json cannot be read (FileNotFoundError))."),
    "empty-file": ("", "empty-file.json is not valid JSON"),
    "not-json": ("{nope", "not-json.json is not valid JSON"),
    "not-object": ("[]", "not-object.json is not an object)."),
    "joints-not-list": ('{"schema_version": 2, "joints": 5}', "stage-joints.json `joints` is not a list)."),
    "readable-no-rows": ('{"schema_version": 2, "joints": []}', None),
}
ARGS_KINDS = {           # what `check_args` accepts after stage, role and cause (the branches of its code) -> (args extras, stage, accepted)
    "cases": ({"cases": ["TC-1"]}, "S5", True),
    "plan-rows": ({"rows": ["row-1"]}, "S2", True),
    "candidates": ({"candidates": ["bug-1"]}, "S7", True),
    "candidates-before-S7": ({"candidates": ["bug-1"]}, "S5", False),
    "candidates-with-cases": ({"candidates": ["bug-1"], "cases": ["TC-1"]}, "S7", False),
    "cases-with-rows": ({"cases": ["TC-1"], "rows": ["row-1"]}, "S5", False),
    "none-at-S5": ({}, "S5", False),
    "none-at-S2": ({}, "S2", True),         # F1: S1-S3 accept args naming no work (`rework_args_list`: "or neither"); the row says so
}


def launch_unknown() -> None:
    """t-1087: an unreadable rows file is told as NOT KNOWN with the reader's reason; a readable file with no row keeps the `none` line."""
    import no_move as NM
    import stage_joints as SJ
    folder, real = harness.temp_dir("qa-launch-unknown-"), SJ.DATA
    try:
        for label, (content, expected) in UNREADABLE_ROWS.items():
            SJ.DATA = folder / f"{label}.json"
            if content is not None:
                SJ.DATA.write_text(content, encoding="utf-8")
            first = NM.moves_section(NM.data(), ["stop_here"], CONDUCTOR_FACTS).split(LAUNCH_HEAD)[-1].strip().splitlines()[0]
            if expected is None:
                check_eq(f"launch-unknown/{label}: readable, no rows -> the `none` line", first, NM.NOTHING_CHECKED)
            else:
                check(f"launch-unknown/{label}: NOT KNOWN with the reader's reason, never `none`", first.startswith("NOT KNOWN: the rows of what code checks could not be read (" + expected), first)
    finally:
        SJ.DATA = real
    rows, _why = SJ.load_rows()
    sentence = next(r["requirement"] for r in rows["joints"] if r.get("check") == "no_move:args")
    check("args-row: the sentence names every kind check_args accepts (cases, plan rows, candidates)",
          all(word in sentence for word in ("cases", "plan row", "candidates", "S7")), sentence)
    facts = dict(CONDUCTOR_FACTS, rework_stages=["S2", "S5", "S7"], candidates=["bug-1"],
                 rework_roles={"S2": ["qa-planner"], "S5": ["qa-automator"], "S7": ["qa-analyst"]})
    roles = {"S2": "qa-planner", "S5": "qa-automator", "S7": "qa-analyst"}
    for label, (extra, stage, accepted) in ARGS_KINDS.items():
        got, _why = NM.check_args(dict({"stage": stage, "role": roles[stage], "cause": "test_defect"}, **extra), facts)
        check_eq(f"args-kinds/{label}: check_args accepts it", got is not None, accepted)


def launch_prompt() -> None:
    """The prompt body the driver hands `conductor` (the one caller of `moves_section`) for a boundary holds the section after the moves."""
    import story_run
    from types import SimpleNamespace
    import no_move as NM
    facts = dict(CONDUCTOR_FACTS, running=False, closed=False, attempts=0, gate="")
    open_ids = NM.open_moves(facts, NM.move_ids())
    text = story_run.Driver._conductor_text(SimpleNamespace(), {"lead": "", "text": "STATE TEXT"}, facts, open_ids, (), False)
    check("launch-prompt: the conductor's prompt holds the section, with the rework row while a rework is open",
          LAUNCH_HEAD in text and "[no_move:args]" in text and "rework_stage" in open_ids, text[:200])
    check("launch-prompt: the section stands between the moves and the state text",
          text.index("## Moves open here") < text.index(LAUNCH_HEAD) < text.index("STATE TEXT"))


def verdict_of(options, **more) -> dict:
    return dict({"action": "ask_person", "question": "Which one?", "why_person": "access", "checked": "the probe record", "options": options}, **more)


def an_option(token, move, **more) -> dict:
    return dict({"token": token, "move": move, "says": "does it", "factory": "stages_again", "person": "none",
                 "story": {"unverified": "none", "report": "none", "delivery": "unchanged"}}, **more)


REFUSALS = {     # case -> (verdict, expected text = the OLD file's output, the row id the Record carries)
    "options-one": (verdict_of([an_option("retry", "person_does")]), "options: fewer than two, or not a list of objects", "no_move:options"),
    "options-dup": (verdict_of([an_option("retry", "person_does"), an_option("Retry", "stop_here")]),
                    "two options carry the token `retry`", "no_move:options"),
    "options-closed": (verdict_of([an_option("retry", "person_does"), an_option("approve", "approve_gate")]),
                       "the option `approve` names the move `approve_gate`, which is not open here", "no_move:options"),
    "prose": (verdict_of([an_option("retry", "person_does"), an_option("stop", "stop_here")], question="Say `go on` or `retry`?"),
              "the question names `go on`, which is not one of its options", "no_move:prose"),
    "args": (verdict_of([an_option("retry", "person_does"), an_option("rework", "rework_stage", args=dict(GOOD_ARGS, cause="nope"))]),
             "\"args\" cause `nope` is not one of the causes listed", "no_move:args"),
    "empty-question": (verdict_of([an_option("retry", "person_does"), an_option("stop", "stop_here")], question=" "),
                       "the question is empty", "no_move:prose"),
    "story-empty": (verdict_of([an_option("retry", "person_does"), an_option("stop", "stop_here", story={})]),
                    "the option `stop` lacks its says / factory / person / story lines (story is a dict)", "no_move:options"),
}
CLASS_HEAD = "a question to a person needs a class and what you read: `why_person` is absent and `checked` is empty; the classes are `access`"


def refusal_texts() -> None:
    """EC-1: the texts of `validate_options` are the old file's, byte for byte; the Record carries the row id (EC-2: the id is written at
    the caller of `check_args`, a helper with several callers)."""
    import no_move as NM
    spec, norm = NM.data(), lambda s: s.strip().lower()
    open_ids = ["rework_stage", "person_does", "stop_here", "resume_with_words"]
    for label, (verdict, text, check_id) in REFUSALS.items():
        try:
            _options, rule = NM.validate_options(verdict, open_ids, spec, norm, {}, (), facts=CONDUCTOR_FACTS)
        except NM.ArgsRefused as refused:        # a bad `args` is raised once the rest of the verdict is valid
            rule = refused.rule
        check_eq(f"refusal-text/{label}: the text, the id the Record carries", (str(rule), getattr(rule, "check", "")), (text, check_id))
    both = verdict_of([an_option("retry", "person_does"), an_option("rework", "rework_stage", args=dict(GOOD_ARGS, cause="nope"))],
                      why_person="", checked="")
    for label, verdict, ids in (("class", verdict_of([an_option("retry", "person_does"), an_option("stop", "stop_here")], why_person="", checked=""),
                                ["no_move:class"]), ("args-and-class", both, ["no_move:args", "no_move:class"])):
        try:
            NM.validate_options(verdict, open_ids, spec, norm, {}, (), facts=CONDUCTOR_FACTS)
            check(f"refusal-text/{label}: refused", False)
        except NM.ArgsRefused as exc:
            import detector_verdict as DV
            check(f"refusal-text/{label}: the text begins as before", str(exc).startswith(
                ("\"args\" cause `nope` is not one of the causes listed; " if label == "args-and-class" else "") + CLASS_HEAD), str(exc)[:160])
            check_eq(f"refusal-text/{label}: one id per problem", [r["check"] for r in DV.told_fields(exc).get("told", [])], ids)


REPAIR_END = ". This is a repair, not a question for the person: return it to {role} in one message"


def road_b_units() -> None:
    """T9a (mech 5.3a): the five role-resumed units of controller.py write their row id at the site; the text is the OLD file's, byte for
    byte (literal expectations, REPAIR_MARKER kept: the driver reads it). One row per unit; the id is read off the Record the site carries."""
    with synthetic_world() as task:
        ctl = Controller(task)
        (task / "work" / "s5-plan.json").write_text("{not json", encoding="utf-8")        # the plan cannot be read
        (task / "work" / "test-plan.json").write_text('{"rows": [{}]}', encoding="utf-8")   # a plan with a row that holds nothing
        plan = {"stage": "S5", "id": "S5-qa-automator-1", "role": "qa-automator", "purpose": C.S5_PLAN}
        review = dict(plan, id="S5-qa-code-critic-1", role="qa-code-critic")

        def s3_gate():
            try:
                ctl._s3_completion_gate({"stage": "S3", "id": "S3-qa-test-strategist-1", "role": "qa-test-strategist"},
                                        {"stage_complete": True}, ctl.state())
            except StateConflict as refused:
                return [(StateConflict, refused.args[0])]
            return []

        def receipts():
            ctl._code_review_problems = lambda p: ["the review names no findings file"]      # what the unit refuses with is its input
            return ctl._code_review_refusal({"stage": "S5", "role": "qa-code-critic"}, {})

        rows = {      # unit -> (the call, the texts that open/close the problems it returns, ids it carries in order)
            "s3": (s3_gate, "S3 structured test plan invalid: ", ["controller:s3_plan"]),
            "receipts": (receipts, "the review names no findings file. These are the review's own receipts, not the person's to produce. "
                                   "This is a repair, not a question for the person. If a person accepts the window without them: `",
                         ["controller:code_review_receipts"]),
            "accept": (lambda: ctl._s5_plan_accept_problems(plan, {"stage_complete": True}, ctl.state()),
                       "a plan never closes S5 (accepting S5-qa-automator-1 with stage_complete: true): accept it with `story_step.py finish` "
                       "and no `--complete`, the windows follow" + REPAIR_END.format(role="qa-automator"),
                       ["controller:s5_plan_accept", "controller:s5_plan_gaps"]),
            "rework-rows": (lambda: ctl._plan_rework_rows_problems(ctl.state(), ""), "", ["controller:s5_plan_gaps.rework_rows"]),
            "review": (lambda: ctl._plan_review_problems(review, ctl.state(), REPAIR_END.format(role="qa-code-critic")),
                       "the review contradicts itself: the verdict is `approved` but the form lists 1 remark(s) (PR-1)" + REPAIR_END.format(role="qa-code-critic"),
                       ["controller:s5_plan_review"] * 3),
        }
        import s5_plan as SP
        held = {name: getattr(SP, name) for name in ("review_of", "reviews", "plan_sha256")}
        element = {"unreadable": "", "dispatch": "S5-qa-code-critic-0", "outcome": "approved", "plan_sha256": "old", "remarks": [{"id": "PR-1", "kind": "remark"}]}
        for label, (call, text, want) in rows.items():
            if label == "review":      # a readable review that contradicts itself, is stamped on other bytes and repeats an id
                SP.review_of, SP.reviews, SP.plan_sha256 = (lambda *_a: element), (lambda *_a: [element]), (lambda *_a: "new")
            try:
                found = call()
            except Exception as exc:      # noqa: BLE001 - a unit that raises is a red row of its own, the others still run
                check(f"road-b/{label}: the unit returns its problems", False, f"{type(exc).__name__}: {str(exc)[:160]}")
                continue
            finally:
                for name, original in held.items():
                    setattr(SP, name, original)
            ids = [getattr(problem, "check", "") for _cls, problem in found]
            check_eq(f"road-b/{label}: class and id of each problem", ([cls for cls, _p in found], ids), ([StateConflict] * len(want), want))
            if text:
                check(f"road-b/{label}: the first text is the old file's", str(found[0][1]).startswith(text), str(found[0][1])[:200])
            check(f"road-b/{label}: the row's expected sentence rides on the Record", all(getattr(p, "expected", "") for _c, p in found), str(found)[:160])


def main() -> None:
    rows = command_rows()
    check(f"the walk has a `command` route to check ({len(rows)} rows)", len(rows) > 50, str(len(rows)))

    known = set(C.OPERATIONS)
    # M-B6 (CX1-18 I6): the names say the route, not "read"/"write", and the old names are NOT aliases.
    check("M-B6: READ_OPERATIONS and WRITE_OPERATIONS are gone, not aliased",
          not hasattr(C, "READ_OPERATIONS") and not hasattr(C, "WRITE_OPERATIONS"))
    check("M-B6: `recover` is routed, `initialize` is applied, OPERATIONS is both",
          "recover" in C.ROUTED_OPERATIONS and "initialize" in C.APPLY_OPERATIONS
          and C.OPERATIONS == C.ROUTED_OPERATIONS + C.APPLY_OPERATIONS
          and not set(C.ROUTED_OPERATIONS) & set(C.APPLY_OPERATIONS))
    # `gate-decision` and friends are routed operations that PRINT a request; the CLI takes both.
    unknown_ops, missing_scripts = [], []
    for where, block, way in rows:
        for operation in OPERATION_RE.findall(way):
            if operation not in known:
                unknown_ops.append((block[:50], operation))
        for script in SCRIPT_RE.findall(way):
            if not (harness.SCRIPTS / script).is_file():
                missing_scripts.append((block[:50], script))
    check("every operation a block names is one the controller knows", not unknown_ops,
          "; ".join(f"{block}: --operation {op}" for block, op in unknown_ops[:6]))
    check("and every script a block names is in the package", not missing_scripts,
          "; ".join(f"{block}: {name}" for block, name in missing_scripts[:6]))

    # K1 (F-5): the problems a request collects and `_raise_all` refuses whole are blocks too, so their
    # doors are looked up with the rest - the Gate A receipt rows name `--operation gate-inputs`.
    receipt_rows = [(block, way) for _, block, way in rows if block.startswith("Gate A receipt must bind")]
    check("the collected Gate A receipt problems are walked, each with a door the controller knows",
          len(receipt_rows) >= 4 and all(OPERATION_RE.search(way) and
                                         OPERATION_RE.search(way).group(1) in known for _, way in receipt_rows),
          str(receipt_rows[:2]))
    # How many of the rows name a door this test can even look up. The rest say what to do in
    # words ("accept the successor first"), which is a route and not a command - counted, not
    # judged, so the number moves when somebody makes a row more precise.
    looked_up = sum(1 for _, _, way in rows if OPERATION_RE.search(way) or SCRIPT_RE.search(way))
    print(f"  (of {len(rows)} `command` rows, {looked_up} name a command this test resolves; "
          f"{len(rows) - looked_up} name the move in words)")
    check("most of the command rows name something lookable-up", looked_up >= len(rows) // 3,
          f"{looked_up} of {len(rows)}")

    doors_open_end_to_end(rows)
    launch_section()
    launch_unknown()
    launch_prompt()
    refusal_texts()
    road_b_units()

    harness.finish("test_controller_doors")


if __name__ == "__main__":
    main()
