#!/usr/bin/env python3
"""doors: a part of test_words_doors.py, split by tools/test_split.py (TD-11c). The shared helpers are in words_doors_common."""
import json
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import SCRIPTS, check, check_eq, check_in, check_not_in, cleanup, finish, run_script, temp_project, use_project
sys.path.insert(0, str(SCRIPTS))
import person_words  # noqa: E402
import refusal_registry as RR  # noqa: E402
import stage_done  # noqa: E402
import stage_guard  # noqa: E402
import test_gate_preflight as GP  # noqa: E402
import test_obligation_join as OJ  # noqa: E402
import test_s0_close_order as S0  # noqa: E402
from words_doors_common import (  # noqa: E402
    FLAG, PENDING, WORDS, captured, critic_story, hits_in, open_door, overrides_of, plan_story, project_env,
    recorded, s5_story, story_with,
)


def part_doors_hold_the_whole_words_clause() -> None:
    """GW1-1 G-3: every printed door with `<part of the line>` carries `person_words.WHOLE_PART` right after its closing backtick
    (the check refuses a cut inside a word, so the text must not invite one); one row per door."""
    clause = person_words.WHOLE_PART
    check_in("the clause says whole words and no cut inside a word", "never a cut inside a word", clause)
    # `s5_precheck.py` left the list (FV1-30a): its door names the finding's tag or whole id, not a part of the line
    for name in ("branch_accounting.py", "controller.py", "critic_rollcall.py", "planning_contract.py"):
        text = (SCRIPTS / name).read_text(encoding="utf-8")
        at = [m.start() for m in re.finditer(r'<part of the line>', text) if "--block" in text[max(0, m.start() - 60):m.start()]]
        check(f"G-3 {name}: a printed `<part of the line>` door exists", bool(at))
        check(f"G-3 {name}: and the clause follows each (within the same statement)",
              all("WHOLE_PART" in text[i:i + 260] for i in at), name)
    check_in("G-3 the registry's WAIVER holds the one clause", clause, RR.WAIVER)


def whole_cut(text: str, n: int = 30) -> str:
    """The door's `<part of the line>` is whole words: at most `n` characters, never ending inside a word. A text
    shorter than `n` stays whole; with no space within the cut the first word is taken whole."""
    if len(text) <= n:
        return text
    cut = text[:n]
    word = re.compile(r"[A-Za-z0-9_-]")
    if word.match(text[n]) and word.match(cut[-1]):
        space = cut.rfind(" ")
        if space > 0:
            return cut[:space]
        return text.split(" ", 1)[0]
    return cut


def row_13_rehearsal() -> None:
    root = GP.story("qa-words-door-rehearsal-")
    try:
        use_project(root)
        ticket = "TP1-15045"

        def close():
            return captured(lambda: stage_done.run(ticket, "S4", "done", "qa-case-critic", "cases reviewed", True))
        code, _, err = close()
        check_eq("13 rehearsal: S4 is refused while the factory owes itself a repair", code, stage_done.EXIT_BAD_ARGS)
        check_in("13 rehearsal: every finding carries the block word the door advises (F-6)",
                 "gate rehearsal: ", err)
        done, _, _ = open_door(root, err, ticket, "S4")
        recorded("13 rehearsal", done, root, ticket, "S4", "gate rehearsal")
        code, _, err = close()
        check_eq("13 rehearsal: the refusing code no longer refuses", code, 0)
    finally:
        cleanup(root)


def row_14_still_running() -> None:
    root = temp_project("qa-words-door-running-")
    try:
        use_project(root)
        art = S0.story(root)
        pipeline = json.loads((art / "pipeline.json").read_text(encoding="utf-8"))
        pipeline["stages"] = {"S5": {"status": "running", "role": None, "digest": ""}}
        (art / "pipeline.json").write_text(json.dumps(pipeline), encoding="utf-8")

        def close():
            return captured(lambda: stage_done.run(S0.TASK, "S9", "done", None, "retro done", True))
        code, _, err = close()
        check_eq("14 still running: S9 refuses to close over a running stage", code, stage_done.EXIT_BAD_ARGS)
        done, _, _ = open_door(root, err, S0.TASK, "S9")
        recorded("14 still running", done, root, S0.TASK, "S9", "still running")
        # 0.8.1 added checks of its own to the close of S9 (sizing, the report, the stages before it), so
        # the fixture's story is refused for THOSE even after the person's word: the claim here is that
        # the block the door names is lifted and the word is quoted, not that S9 closes.
        _, out, err = close()
        check_not_in("14 still running: the refusing code no longer refuses over the running stage",
                     "is still running", err)
        check_in("14 still running: and it says it closes over it on the person's word",
                 "closing S9 over a running stage on the person's word", err)
    finally:
        cleanup(root)


def row_15_16_controller_stage() -> None:
    root = temp_project("qa-words-door-managed-")
    try:
        use_project(root)
        art = S0.story(root)
        S0.initialize(art)
        code, err = S0.close(art)
        check_eq("15 not accepted: a managed stage the controller has not accepted is refused",
                 code, stage_done.EXIT_BAD_ARGS)
        done, _, _ = open_door(root, err, S0.TASK, "S0")
        recorded("15 not accepted", done, root, S0.TASK, "S0", "no accepted controller stage")
        check_eq("15 not accepted: the refusing code no longer refuses", S0.close(art)[0], 0)
    finally:
        cleanup(root)
    root = temp_project("qa-words-door-reopen-")
    try:
        use_project(root)
        art = S0.story(root)
        S0.initialize(art)
        import hashlib
        from controller import Controller
        Controller(art).apply("code_only", {
            "id": "s0-preflight", "stage": "S0", "reason": "no role runs preflight",
            "evidence_refs": [{"path": "pipeline.json",
                               "sha256": hashlib.sha256((art / "pipeline.json").read_bytes()).hexdigest()}],
            "idempotency_key": "code-only-S0"})
        code, err = S0.close(art, status="running")
        check_eq("16 reopen: lowering a stage the controller accepted is refused", code, stage_done.EXIT_BAD_ARGS)
        done, _, _ = open_door(root, err, S0.TASK, "S0")
        recorded("16 reopen", done, root, S0.TASK, "S0", "already accepted by the controller")
        check_eq("16 reopen: the refusing code no longer refuses", S0.close(art, status="running")[0], 0)
    finally:
        cleanup(root)


def row_17_stage_guard_hint() -> None:
    root = temp_project("qa-words-door-hint-")
    try:
        use_project(root)
        story_with(root, "QA-1", {})

        def pipeline():
            return json.loads((root / "qa-factory" / "artifacts" / "QA-1" / "pipeline.json").read_text(encoding="utf-8"))
        errors = stage_guard.dispatch_errors(pipeline(), "S2", journal=False)
        check_eq("17 hint: S2 is refused while S1 is not done", len(errors), 1)
        if errors:
            check_in("17 hint: the refusal still starts with its own words", "required stages are not done", errors[0])
            # 0.8.1: `waiver_hint` is a plain `door()` (spec t-428 L7): the stage guard's refusal is read by the
            # orchestrator, whose placeholder is `<file>`; the person's form is the one of the gate packets.
            check_in("17 hint: the hint is the plain file form (a `door()`, not the person's placeholder)",
                     f"{FLAG} <file>", errors[0])
            check_not_in("17 hint: and carries no person's placeholder", "<file with your words>", errors[0])
            check_in("17 hint: the hint keeps its prefix", stage_guard.WAIVER_HINT_PREFIX, errors[0])
            done, _, _ = open_door(root, errors[0], "QA-1", "S2")
            recorded("17 hint", done, root, "QA-1", "S2", "required stages are not done")
            check_eq("17 hint: the refusing code no longer refuses",
                     stage_guard.dispatch_errors(pipeline(), "S2", journal=False), [])
    finally:
        cleanup(root)


def detector_row(label: str, script: str, agent: str, stage: str, make_story) -> None:
    """Rows 19-21: the gate re-runs the detector script; its last line is the door."""
    root = temp_project(f"qa-words-door-{script[:6]}-")
    try:
        use_project(root)
        make_story(root)
        run = run_script(script, cwd=root, env=project_env(root))
        check_eq(f"{label}: the detector refuses", run.returncode, 1)
        lines = [line for line in run.stdout.strip().splitlines() if line.strip()]
        check_in(f"{label}: the last line is the person's-word door", "waiver.py", lines[-1] if lines else "")
        head = whole_cut(lines[-2].strip().lstrip("- ")) if len(lines) > 1 else ""
        import exit_gate
        before = exit_gate.detector_errors(agent)
        check(f"{label}: the gate's own re-run refuses", bool(before), str(run.stdout)[-300:])
        done, _, _ = open_door(root, run.stdout, "QA-1", stage, head)
        recorded(label, done, root, "QA-1", stage, head)
        pipeline = json.loads((root / "qa-factory" / "artifacts" / "QA-1" / "pipeline.json").read_text(encoding="utf-8"))
        # C2-1: the rule of the gate is `judge_words` (a record is judged by whoever produced it), no longer
        # `split_overridden` over the whole output
        records = exit_gate.detector_errors(agent)
        blocking, passed = exit_gate.judge_words(records, pipeline, stage)
        check_eq(f"{label}: the refusing code no longer refuses (the gate re-run is passed over)", blocking, [])
        check(f"{label}: and the pass names the words", bool(passed) and passed[0]["decision"] == WORDS.strip(),
              str(passed))
        # a word taken from one finding's line passes that finding only; the word of the summary line (row 20) none
        # of them by itself but, for one release, the whole detector
        findings = [r for r in records if getattr(r, "kind", "") == "finding"]
        if len(findings) > 1:
            part = str(findings[0]).split(": ", 1)[1]
            part = whole_cut(part)
            one = {"stage_overrides": [{"stage": stage, "match": part, "decision": "x", "at": "2026-10-01T10:00:00"}]}
            blocking, passed = exit_gate.judge_words(records, one, stage)
            check_eq(f"{label}: a word from the line of one finding passes that finding and none of the others",
                     (len(passed), len(blocking)), (sum(1 for f in findings if part.lower() in f.lower()),
                                                     len(findings) - sum(1 for f in findings if part.lower() in f.lower())))
    finally:
        cleanup(root)


def row_19_20_21_detectors() -> None:
    detector_row("19 critic_rollcall", "critic_rollcall.py", "qa-case-critic", "S4", critic_story)
    detector_row("20 planning_contract", "planning_contract.py", "qa-test-strategist", "S3", plan_story)
    root = temp_project("qa-words-door-s5pre-")
    try:
        use_project(root)
        s5_story(root)
        run = run_script("s5_precheck.py", cwd=root, env=project_env(root))
        check_eq("21 s5_precheck: the detector refuses", run.returncode, 1)
        lines = [line for line in run.stdout.strip().splitlines() if line.strip()]
        # C2-1 (§6 row 21): the word is taken from a PRINTED line. The fixture gives four findings: two of the
        # `obligations` family (a word passes them, at the source) and two of `run_mapping`/`bindings` (no word
        # passes them, `*` included: their lines carry `WORDS_REFUSED_AT_SOURCE ... family`).
        # FV1-30a: one road for every family - the word is the finding's TAG (or its whole id, or `*`), never a part of its printed
        # line - so the word is the tag of the first `obligations` finding; the other three findings stand and no word is `family`
        wanted = next(line for line in lines if line.startswith("- [obligations "))
        head = re.search(r"\[obligations (\S+)\]", wanted).group(1).split(":", 2)[2]
        import exit_gate
        check("21 s5_precheck: the gate's own re-run refuses", bool(exit_gate.detector_errors("qa-automator")))
        done, _, _ = open_door(root, run.stdout, OJ.TICKET, "S5", head)
        recorded("21 s5_precheck", done, root, OJ.TICKET, "S5", head)
        pipeline = json.loads((root / "qa-factory" / "artifacts" / OJ.TICKET / "pipeline.json")
                              .read_text(encoding="utf-8"))
        records = exit_gate.detector_errors("qa-automator")
        blocking, passed = exit_gate.judge_words(records, pipeline, "S5")
        check_eq("21 s5_precheck: the tag word passed its finding at the SOURCE; the other three stand, none is `family` "
                 "(every family is passable now), and the gate passes nothing itself",
                 ([b.refused for b in blocking], passed), (["", "", ""], []))
        star = {"stage_overrides": [{"stage": "S5", "match": "*", "decision": "all of it",
                                     "at": "2026-10-01T10:00:00"}]}
        blocking, passed = exit_gate.judge_words(records, star, "S5")
        check_eq("21 s5_precheck: `*` at the gate passes the three standing records, as it always passed a source's records",
                 ([b.refused for b in blocking], len(passed)), ([], 3))
        bound = next(line for line in lines if line.startswith("- [bindings "))
        word = {"stage_overrides": [{"stage": "S5", "match": whole_cut(bound.lstrip("- ")), "decision": "x",
                                     "at": "2026-10-01T10:00:00"}]}
        blocking, passed = exit_gate.judge_words(records, word, "S5")
        check_eq("21 s5_precheck: a word taken from the printed line of a finding is judged at the SOURCE only: the gate leaves "
                 "all three blocked", ([b.refused for b in blocking], passed), (["", "", ""], []))
    finally:
        cleanup(root)


def row_22_manifest_put() -> None:
    root, task = OJ.make_story()
    try:
        fragment = {"tests": [{"case": "TC-005", "file": "tests/t.py", "instance_id": "test_ok",
                               "covers": ["TC-005"]}],
                    "obligation_bindings": [{"obligation_id": "OB-1", "instance_ids": ["test_ok"]}]}
        refused = OJ.put(root, fragment)
        import manifest_put
        check_eq("22 manifest_put: an obligation id the plan does not name is refused",
                 refused.returncode, manifest_put.EXIT_BAD_FRAGMENT)
        (task / "pipeline.json").write_text(json.dumps({"ticket": OJ.TICKET, "stages": {}}), encoding="utf-8")
        done, _, _ = open_door(root, refused.stderr, OJ.TICKET, "S5")
        recorded("22 manifest_put", done, root, OJ.TICKET, "S5", "obligation-id")
        check_eq("22 manifest_put: the refusing code no longer refuses", OJ.put(root, fragment).returncode, 0)
    finally:
        cleanup(root)


def row_23_24_story_budget() -> None:
    import story_budget
    root = temp_project("qa-words-door-budget-")
    try:
        use_project(root)
        base = root / "qa-factory"
        troot = story_with(root, "QA-1", {})
        (base / "state" / "cost").mkdir(parents=True, exist_ok=True)
        (base / "config.json").write_text(json.dumps({"budget": {"story_usd": 10, "warn_at": [0.5]}}), encoding="utf-8")
        # 0.8.1 (FR-24): a story's spend is the sessions its OWN driver journal names, so the session is bound
        # the way the price function reads it (the journal row with the running total; a `by_task` tag of
        # the cost file binds nothing), as test_window_and_budgets.bind_session does.
        (troot / "state").mkdir(parents=True, exist_ok=True)
        (troot / "state" / "driver-runs.jsonl").write_text(json.dumps(
            {"kind": "role", "role": "qa-scout", "dispatch": "S1-qa-scout-1", "stage": "S1", "session_id": "s-1",
             "num_turns": 3, "total_cost_usd": 11.0, "ts": "2026-09-30T10:00:00+00:00"}) + "\n", encoding="utf-8")
        (base / "state" / "cost" / "s-1.json").write_text(json.dumps(
            {"session_id": "s-1", "by_task": {"QA-1": {"tokens": 10}}, "agents": []}), encoding="utf-8")
        state = story_budget.check("QA-1", base, troot)
        check_eq("24 story_budget: past the ceiling the story stops and asks", state["stop"], True)
        done, _, _ = open_door(root, state["notice"], "QA-1", "S5")
        recorded("24 story_budget", done, root, "QA-1", "S5", "story budget")
        story_budget.marker_path("QA-1", base).unlink()
        again = story_budget.check("QA-1", base, troot)
        check_eq("24 story_budget: the refusing code no longer stops the story", again["stop"], False)
        check_eq("24 story_budget: and it quotes the person's words",
                 (again["overridden"] or {}).get("decision"), WORDS.strip())
        doc = (SCRIPTS / "story_budget.py").read_text(encoding="utf-8").split('"""')[1]
        check_in("23 story_budget: its own docstring shows the file form", f'--block "story budget" {FLAG} <file>', doc)
    finally:
        cleanup(root)


def row_block_names() -> None:
    """conductor/4 C4-3 (FR-2): the doors the roles are taught for the block NAMES a reader acts on - `keep it local` (s8.md),
    `executor unavailable: <profile>` (s4.md, SKILL.md) - open through the real waiver.py while the driver's record of that
    stage holds another line; a text that is no name (the NO_ADAPTER wording `keep local`) is refused as before."""
    import contract
    import external_writes
    root = temp_project("qa-words-door-names-")
    try:
        use_project(root)
        task = story_with(root, "QA-1", {})
        state = task / "state"
        state.mkdir(parents=True, exist_ok=True)
        for stage, block in (("S8", "keep it local"), ("S5", f"{contract.HANDED_MATCH_PREFIX} e2e-ui")):
            (state / "standing-refusal.json").write_text(json.dumps(
                {"stage": stage, "lines": ["a problem that is not the person's word to pass"]}), encoding="utf-8")
            door = person_words.door(f'waiver.py --task <T> --stage {stage} --block "{block}"')
            done, _, _ = open_door(root, f"the roles are taught: `{door}`", "QA-1", stage)
            recorded(f"names: `{block}` at {stage}, another line standing", done, root, "QA-1", stage, block)
        check_eq("names: the reader of `keep it local` acts on what was recorded",
                 bool(external_writes.local_only_decision("QA-1")), True)
        check_eq("names: the reader of the handed profile acts on what was recorded",
                 sorted(contract.handed_profiles(json.loads((task / "pipeline.json").read_text(encoding="utf-8")))), ["e2e-ui"])
        (state / "standing-refusal.json").write_text(json.dumps(
            {"stage": "S8", "lines": ["a problem that is not the person's word to pass"]}), encoding="utf-8")
        before = overrides_of(root, "QA-1")
        door = person_words.door('waiver.py --task <T> --stage S8 --block "keep local"')
        done, _, _ = open_door(root, f"`{door}`", "QA-1", "S8")
        check_eq("names: `keep local` (the NO_ADAPTER wording) is no name: the real waiver.py refuses it (exit 2)",
                 done is not None and done.returncode, 2)
        check_eq("names: ...and records nothing", overrides_of(root, "QA-1"), before)
        # t-894 F-1: words after the prefix are no profile id - the real waiver.py refuses them, the reader never sees them
        (state / "standing-refusal.json").write_text(json.dumps(
            {"stage": "S5", "lines": ["a problem that is not the person's word to pass"]}), encoding="utf-8")
        before = overrides_of(root, "QA-1")
        door = person_words.door(f'waiver.py --task <T> --stage S5 --block "{contract.HANDED_MATCH_PREFIX} e2e ui"')
        done, _, _ = open_door(root, f"`{door}`", "QA-1", "S5")
        check_eq("names: `executor unavailable: e2e ui` (words, not one profile) is no name: the real waiver.py refuses it (exit 2)",
                 done is not None and done.returncode, 2)
        check_eq("names: ...and records nothing", overrides_of(root, "QA-1"), before)
    finally:
        cleanup(root)


def row_25_readiness_and_tracker_route() -> None:
    import readiness
    cap = readiness.session_route("jira", "mcp_tool", "jira_get_issue")
    steps = " | ".join(cap["remedy"]["steps"])
    # 0.8.1 (spec t-428): the remedy of an unproven tracker route is upstream's text, which names the
    # script on the action line and takes the words inline (`--decision "<your words>"`). It is the
    # one inline door of the readiness doctor, listed in PENDING (B-387), so the check here is that
    # the pending text is the one the code prints - the file form is the stage guard's refusal below.
    check_in("25 readiness: the remedy is upstream's text, the pending door of the detector",
             PENDING["scripts/readiness.py"][0], steps)
    root = temp_project("qa-words-door-tracker-")
    try:
        use_project(root)
        story_with(root, "QA-1", {"S0": {"status": "done"}})
        (root / "qa-factory" / "readiness.json").write_text(json.dumps(
            {"capabilities": {"ticket_adapter": dict(cap, status="not_configured")}}), encoding="utf-8")
        pipeline = json.loads((root / "qa-factory" / "artifacts" / "QA-1" / "pipeline.json").read_text(encoding="utf-8"))
        refusal = stage_guard.rule_tracker_route("QA-1", "qa-scout", "S1", pipeline)
        check("25 tracker route: S1 is refused while the route is not proven", bool(refusal), str(refusal))
        done, _, _ = open_door(root, refusal or "", "QA-1", "S1")
        recorded("25 tracker route", done, root, "QA-1", "S1", "tracker route")
        pipeline = json.loads((root / "qa-factory" / "artifacts" / "QA-1" / "pipeline.json").read_text(encoding="utf-8"))
        check_eq("25 tracker route: the refusing code no longer refuses",
                 stage_guard.rule_tracker_route("QA-1", "qa-scout", "S1", pipeline), None)
    finally:
        cleanup(root)


def registry_texts() -> None:
    by_id = {entry["id"]: entry for entry in RR.REGISTRY}
    check_in("registry: WAIVER names the file form", f'--block "<part of the line>" {FLAG} <file>', RR.WAIVER)
    check_in("registry: SG-tracker-route names the file form", f'--block "tracker route" {FLAG} <file>',
             by_id["SG-tracker-route"]["override"])
    blocked = by_id["CTRL-next-blocked"]["override"]
    check_in("registry: CTRL-next-blocked names the file form", f'--block "wait_existing_job" {FLAG} <file>', blocked)
    check_in("registry: and says route_release passes the same words on to release",
             "--operation release", blocked)
    check_in("registry: through the file the person's words came in", "route_release", blocked)
    for eid, entry in by_id.items():
        check_eq(f"registry: {eid} carries no inline words part", hits_in(str(entry.get("override") or "")), [])


def main() -> None:
    registry_texts()
    row_13_rehearsal()
    row_14_still_running()
    row_15_16_controller_stage()
    row_17_stage_guard_hint()
    row_19_20_21_detectors()
    row_22_manifest_put()
    row_23_24_story_budget()
    row_block_names()
    row_25_readiness_and_tracker_route()
    part_doors_hold_the_whole_words_clause()
    finish("test_words_doors_doors")


# split: runner piece 1
if __name__ == "__main__":
    main()
