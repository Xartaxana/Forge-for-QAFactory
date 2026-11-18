#!/usr/bin/env python3
"""flight launcher: a part of test_words_doors.py, split by tools/test_split.py (TD-11c). The shared helpers are in words_doors_common."""
import io
import json
import subprocess
import sys
from contextlib import redirect_stderr
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import PLUGIN_ROOT, SCRIPTS, check, check_eq, check_in, check_not_in, cleanup, finish, run_script, temp_dir, temp_project, use_project
sys.path.insert(0, str(SCRIPTS))
import person_words  # noqa: E402
import stage_done  # noqa: E402
import stage_guard  # noqa: E402
import waiver  # noqa: E402
import test_gate_preflight as GP  # noqa: E402
import test_obligation_join as OJ  # noqa: E402
import test_s0_close_order as S0  # noqa: E402
from words_doors_common import (  # noqa: E402
    FLAG, LAUNCHER, TICKET, WIN, WORDS, captured, ctrl_project, hits_in, overrides_of, project_env,
    refused_text, story_with,
)


# --- (c) a story in flight ---------------------------------------------------------------------

OLD_KEYWORDS = (("design review", "S4"), ("empty scope", "S3"), ("still running", "S9"),
                ("no accepted controller stage", "S0"), ("obligation-id", "S5"),
                ("story budget", "S5"), ("tracker route", "S1"), ("*", "S4"),
                # the controller's own advice of 0.7.x: each keyword is a substring of the error it
                # answers, and the new text keeps every byte before the words part
                ("empty scope", "S4"), ("empty scope", "S5"), ("mechanical repair round", "S5"),
                ("repair round", "S5"), ("not receipted", "S5"), ("mechanical round", "S5"),
                ("derived scope", "S6"))


def part_in_flight() -> None:
    """A pipeline.json recorded under the OLD advice still passes the NEW texts: invariant A (every
    byte before the words part is unchanged) means the advised `--block` keyword is still a
    substring of the error."""
    overrides = [{"stage": stage, "match": match, "decision": "recorded before the file form",
                  "at": "2026-09-30T10:00:00+00:00", "by": "human"} for match, stage in OLD_KEYWORDS]
    pipeline = {"ticket": "QA-1", "stages": {}, "stage_overrides": overrides}
    for keyword, stage in OLD_KEYWORDS:
        head = f"2 problem(s) about the {keyword if keyword != '*' else 'plan'} of this story"
        advised = person_words.door(f'waiver.py --task QA-1 --stage {stage} --block "{keyword}"')
        _, passed = waiver.split_overridden([f"{head}. A person's word passes it: `{advised}`."], pipeline, stage)
        check_eq(f"in flight: an override recorded under `{keyword}` passes a text with the file-form door",
                 len(passed), 1)
    # and the real texts of this node, with the real stage logic
    root = temp_project("qa-words-inflight-")
    try:
        use_project(root)
        art = S0.story(root)
        data = json.loads((art / "pipeline.json").read_text(encoding="utf-8"))
        data["stage_overrides"] = overrides
        data["stages"] = {"S5": {"status": "running", "role": None, "digest": ""}}
        (art / "pipeline.json").write_text(json.dumps(data), encoding="utf-8")
        code, _, err = captured(lambda: stage_done.run(S0.TASK, "S9", "done", None, "retro done", True))
        # (0.8.1: the close of S9 has checks of its own that this fixture does not satisfy - see row 14; the
        # old override is read when the refusal about the running stage is gone and the word is quoted)
        check_not_in("in flight: S9 no longer refuses over a running stage on the old `still running` override",
                     "is still running", err)
        check_in("in flight: and closes over it on the person's word",
                 "closing S9 over a running stage on the person's word", err)
        S0.initialize(art)
        data = json.loads((art / "pipeline.json").read_text(encoding="utf-8"))
        data["stages"]["S0"] = {"status": "running", "role": None, "digest": ""}
        (art / "pipeline.json").write_text(json.dumps(data), encoding="utf-8")
        check_eq("in flight: a managed stage closes on the old `no accepted controller stage` override",
                 S0.close(art)[0], 0)
        story = {"ticket": "QA-1", "stage_overrides": overrides}
        hinted = stage_guard.waiver_hint("QA-1", "S1", "dispatching qa-scout (S1) is blocked — tracker route x")
        check_eq("in flight: the old `tracker route` override passes the guard's hint-carrying text",
                 len(waiver.split_overridden(["dispatching qa-scout (S1) is blocked — tracker route x " + hinted],
                                             story, "S1")[1]), 1)
        import story_budget
        check_eq("in flight: the old `story budget` override is read by the budget",
                 bool(story_budget.override(story)), True)
    finally:
        cleanup(root)
    root, task = OJ.make_story()
    try:
        (task / "pipeline.json").write_text(json.dumps({"ticket": OJ.TICKET, "stage_overrides": overrides}),
                                            encoding="utf-8")
        fragment = {"obligation_bindings": [{"obligation_id": "OB-1", "instance_ids": ["test_ok"]}]}
        check_eq("in flight: the old `obligation-id` override passes manifest_put", OJ.put(root, fragment).returncode, 0)
    finally:
        cleanup(root)


# --- (d) the real launcher -----------------------------------------------------------------------

def part_launcher() -> None:
    if not WIN:
        print("SKIPPED: not Windows (the cmd route was not run)")
        return
    root = temp_project("qa-words-launcher-")
    work = temp_dir("qa words launcher ")
    env = dict(project_env(root), QA_FACTORY_PYTHON=sys.executable)
    env.pop("QA_FACTORY_LAUNCHER", None)
    try:
        story_with(root, "QA-1", {})

        def launch(tail: str):
            proc = subprocess.run(f'"{LAUNCHER}" waiver.py --task QA-1 --stage S1 {tail}', shell=True,
                                  capture_output=True, cwd=str(work), env=env, timeout=300)
            return proc.returncode, proc.stdout.decode("utf-8", "replace"), proc.stderr.decode("utf-8", "replace")
        words = work / "the words.txt"
        words.write_bytes(WORDS.encode("utf-8"))
        code, out, err = launch(f'--block "x" {FLAG} "{words}"')
        check("launcher: the file door records through run-py.cmd", code == 0, f"{code} {out} {err}")
        check_eq("launcher: the override carries the file's words whole",
                 [o["decision"] for o in overrides_of(root, "QA-1") if o["match"] == "x"], [WORDS.strip()])
        code, out, err = launch('--block "y" --decision "one line"')
        check("launcher: the same door with inline words is refused", code != 0, f"{code} {out} {err}")
        check_in("launcher: and the refusal names the file form", FLAG, err)
        check_eq("launcher: nothing was recorded for it", [o for o in overrides_of(root, "QA-1") if o["match"] == "y"], [])
    finally:
        cleanup(work)
        cleanup(root)


def row_settle_order() -> None:
    """GB-1a (t-1509): `settle_order` takes a person's words through `person_words.read` like `release` does - `--words-file` whole,
    both options at once refused before any event - and the refusal of a cancel with neither words nor a coded reason prints the
    file form of its door."""
    import test_gate_b_orders as GB
    root = temp_project("qa-words-settle-")
    try:
        c = GB.synthetic(root, drafts=("a",), mr="open")
        words = root / "state" / "words" / "settle-1.txt"
        words.parent.mkdir(parents=True, exist_ok=True)
        words.write_bytes(WORDS.encode("utf-8"))
        revision = c.state()["revision"]
        base = ("controller.py", "--task-root", str(root), "--operation", "settle_order", "--order", "mr", "--outcome", "cancelled")
        both = run_script(*base, "--words", "inline", FLAG, str(words), cwd=root, env=project_env(root))
        check("settle: both options at once are refused (exit 2) before any event", both.returncode == 2, both.stderr[-300:])
        none = run_script(*base, cwd=root, env=project_env(root))
        check("settle: no words and no coded reason is refused, naming the file form of the door",
              none.returncode == 2 and f"--operation settle_order --order <order> --outcome cancelled {FLAG} <file>" in none.stderr, none.stderr[-400:])
        check_eq("and nothing was written", c.state()["revision"], revision)
        done = run_script(*base, FLAG, str(words), cwd=root, env=project_env(root))
        check("settle: the file form passes", done.returncode == 0, done.stderr[-300:])
        check_eq("and the record holds the file's words whole (FR-8)",
                 c.state()["decisions"]["gateB-" + root.name]["orders_settled"]["mr"]["words"], WORDS)
    finally:
        cleanup(root)


def row_leave_unlaunched() -> None:
    """C1-6a (t-1151, A3 and A11): the two ops that take a person's words for the work a closed story held back read them through
    `person_words.read` like `release` does - `--words-file` whole, both options at once refused before any event - and the closure
    refusal prints the file form of its door. The `rework` refusal for a LIVE dispatch names both of the conductor's own doors."""
    import test_story_closed as CLOSED
    root, task = ctrl_project("qa-words-leave-")
    try:
        controller = CLOSED.closed_story(task)
        CLOSED.never_started(controller, "S6-qa-runner-9", stage="S6", role="qa-worker", rework_of="S6-qa-runner-1")
        door = refused_text(lambda: controller.apply("dispatch", dict(CLOSED.packet("S3-x-1"), idempotency_key="k1")))
        check_in("leave: the closure refusal prints the file form of its door", f"--operation reopen_story --dispatch <the held dispatch ids> {FLAG} <file>", door)
        words = task / "state" / "words" / "leave-1.txt"
        words.parent.mkdir(parents=True, exist_ok=True)
        revision = controller.state()["revision"]
        words.write_bytes(WORDS.encode("utf-8"))
        both = run_script("controller.py", "--task-root", str(task), "--operation", "leave_unlaunched", "--dispatch", "S6-qa-runner-9",
                          "--words", "inline", FLAG, str(words), cwd=root, env=project_env(root))
        check("leave: both options at once are refused (exit 2) before any event", both.returncode == 2, both.stderr[-300:])
        none = run_script("controller.py", "--task-root", str(task), "--operation", "leave_unlaunched", "--dispatch", "S6-qa-runner-9",
                          cwd=root, env=project_env(root))
        check("leave: no words at all is refused as well", none.returncode != 0, none.stderr[-300:])
        check_eq("and nothing was written", controller.state()["revision"], revision)
        done = run_script("controller.py", "--task-root", str(task), "--operation", "leave_unlaunched", "--dispatch", "S6-qa-runner-9",
                          FLAG, str(words), cwd=root, env=project_env(root))
        check("leave: the file form passes", done.returncode == 0, done.stderr[-300:])
        check_eq("and the record holds the file's words whole (FR-8)", controller.state()["dispatches"]["S6-qa-runner-9"].get("left_by_person"), WORDS)
        # A11: the rework refusal when a LIVE dispatch of the role exists on the stage, and today's text when there is none
        CLOSED.stray(controller, "S4-qa-live-1", stage="S4", role="qa-live")
        live = refused_text(lambda: controller.build_rework_request("S4", "qa-live", [], "x"))
        check_in("rework: a live dispatch is named with its status", "S4-qa-live-1 is running, not accepted", live)
        check_in("rework: and the resume door", "answer `continue`", live)
        check_in("rework: and the release door in the file form", "release --dispatch S4-qa-live-1 --words-file <their words>", live)
        plain = refused_text(lambda: controller.build_rework_request("S4", "qa-nobody", [], "x"))
        check("rework: a role with no dispatch on the stage keeps today's text", "no accepted qa-nobody dispatch on S4 to rework; accepted roles on S4:" in plain
              and "is running" not in plain, plain)
    finally:
        cleanup(root)


def row_words_carry() -> None:
    """GW1-40 (AR-24): `waiver.py --carry-from` copies words that were already recorded, so it needs no `--words-file` and prints no door of
    words: nothing it prints (success, partial, any refusal) holds an inline words part, and the conductor's row for it (`words_carry` in
    the `actions` of conductor-actions.json, not in `moves`) holds none either."""
    row = next((a for a in json.loads((PLUGIN_ROOT / "references" / "conductor-actions.json").read_text(encoding="utf-8"))["actions"]
                if a.get("id") == "words_carry"), None)
    check("carry: the conductor has a row `words_carry` among the actions", row is not None)
    check_eq("carry: ... and it is not among the `moves` (whose key set another table holds equal)",
             any(m.get("id") == "words_carry" for m in json.loads((PLUGIN_ROOT / "references" / "conductor-actions.json").read_text(
                 encoding="utf-8"))["moves"]), False)
    for field in ("says", "run"):
        check_eq(f"carry: the row's `{field}` carries no inline words part", hits_in(str((row or {}).get(field) or "")), [])
    check_in("carry: the row names the form", "waiver.py --carry-from <old key> --task <new key>", (row or {}).get("run", ""))
    root = temp_project("qa-words-door-carry-")
    try:
        use_project(root)
        old = story_with(root, "OLD-1", {})
        pipeline = json.loads((old / "pipeline.json").read_text(encoding="utf-8"))
        pipeline["stage_overrides"] = [{"stage": "S1", "match": "source material unavailable", "decision": "go on", "at": "2026-10-01T10:00:00+00:00"},
                                       {"stage": "S5", "match": "executor unavailable: e2e-ui", "decision": "mine", "at": "2026-10-01T10:00:00+00:00"}]
        (old / "pipeline.json").write_text(json.dumps(pipeline), encoding="utf-8")
        story_with(root, "NEW-1", {})
        texts = []
        for args in (("--carry-from", "OLD-1", "--task", "NEW-1"), ("--carry-from", "OLD-1", "--task", "NEW-1"),
                     ("--carry-from", "NOPE", "--task", "NEW-1"), ("--carry-from", "OLD-1", "--task", "OLD-1"),
                     ("--carry-from", "../x", "--task", "NEW-1"), ("--carry-from", "OLD-1", "--task", "NO-STORY"),
                     ("--carry-from", "OLD-1", "--stage", "S1", "--task", "NEW-1")):
            done = run_script("waiver.py", *args, cwd=root, env=project_env(root))
            texts.append(done.stdout + "\n" + done.stderr)
        check_eq("carry: the carry ran (a line `carried:` printed once, then `already carried`)",
                 ("carried: S1 · source material unavailable" in texts[0], "already carried:" in texts[1]), (True, True))
        check_eq("carry: every refusal printed something to read", [bool(t.strip()) for t in texts], [True] * len(texts))
        for n, text in enumerate(texts):
            check_eq(f"carry: output {n} holds no inline words part (the form needs no words file)", hits_in(text), [])
            if not text.lstrip().startswith("usage:"):      # argparse's own usage line lists every option of the CLI: not a door
                check_not_in(f"carry: output {n} names no words option", "--words-file", text)
    finally:
        cleanup(root)


def row_repo_words_cli() -> None:
    """FG7-8 B2 `repo_words.py main`, both forms, through the real CLI: the person's answer comes by `--words-file` and must be EXACTLY the word
    (a sentence, a question, an empty or blank file, another word are refused with exit 2 and nothing is done); with no stored record of what
    gate A showed it exits 3 and prints how to show it again; the exact word runs the executor on the STORED door, records the person's word
    with `waiver.py` and prints the line told to the person; every refusal of the executor prints the command with `--words-file`;
    `--reminder` prints one JSON line and exits 0 whatever happens."""
    import gate_brief
    root, task_root = GP.words_repo("qa-words-door-repo-")
    try:
        GP.words_dirty(root, staged=False)
        env = project_env(root)

        def say(text: str) -> Path:
            path = task_root / "state" / "answer.txt"
            path.write_text(text, encoding="utf-8")
            return path

        def cli(word: str, text: str):
            return run_script("repo_words.py", "--task", "TP1-15045", "--word", word, "--words-file", say(text), cwd=root, env=env)
        none = cli("commit", "vcs-test-repo: commit")
        check_eq("cli: no stored record of what gate A showed: exit 3", none.returncode, 3)
        check_in("cli: ...and it says how to show gate A again", "gate_brief.py --task TP1-15045 --gate A", none.stdout)
        rehearsal = GP.gate_preflight.Rehearsal(task_root, "A")
        rehearsal.check_vcs()
        gate_brief.keep_shown_doors(task_root, {f["id"]: f["waives"] for f in rehearsal.findings if f.get("waives")})
        before = GP._porcelain(root)
        for label, word, text, code in (("a sentence", "commit", "vcs-test-repo: commit please", 2), ("a question", "commit", "vcs-test-repo: commit?", 2),
                                        ("another word's line", "commit", "vcs-test-repo: stash", 2), ("a word of no question", "maybe", "maybe", 2),
                                        ("an empty file", "commit", "", 2), ("a blank file", "commit", "  \n\t\n", 2)):
            done = cli(word, text)
            check_eq(f"cli: {label} is refused with exit 2", done.returncode, code)
            check_not_in(f"cli: {label} prints no traceback", "Traceback", done.stdout + done.stderr)
            check_eq(f"cli: {label} leaves the repository as it was", GP._porcelain(root), before)
        check_in("cli: a question is named as one, never consent", "a question is never consent", cli("commit", "vcs-test-repo: commit?").stdout)
        done = cli("commit", "commit")
        check_eq("cli: the exact word alone is carried out (exit 0)", done.returncode, 0)
        check_in("cli: the printed line is the one told to the person", "uncommitted change(s) are now commit", done.stdout)
        pipeline = json.loads((task_root / "pipeline.json").read_text(encoding="utf-8"))
        check("cli: the person's word is recorded with the line quoted", any("the person wrote: commit" in str(o.get("decision")) for o in pipeline.get("stage_overrides") or []),
              str(pipeline.get("stage_overrides")))
        again = cli("commit", "vcs-test-repo: commit")
        check_eq("cli: asked again, nothing is left to take: exit 3", again.returncode, 3)
        check_in("cli: a refusal prints the command with the words file, to run again", "--words-file", again.stdout)
        check_in("cli: ...and says what it did not do", "Nothing of yours is uncommitted", again.stdout)
        reminder = run_script("repo_words.py", "--reminder", "--task", "TP1-15045", cwd=root, env=env)
        check_eq("cli: the reminder is one JSON line, exit 0", (reminder.returncode, list(json.loads(reminder.stdout))), (0, ["line"]))
        check_in("cli: ...naming the commit", "your changes were committed as", json.loads(reminder.stdout)["line"])
        lost = run_script("repo_words.py", "--reminder", "--task", "NO-SUCH-STORY", cwd=root, env=env)
        check_eq("cli: the reminder of a story that does not exist is the empty line, exit 0", (lost.returncode, json.loads(lost.stdout)), (0, {"line": ""}))
    finally:
        cleanup(root)
    root, task_root = GP.words_repo("qa-words-door-repo-wrong-")
    try:
        GP.words_dirty(root, staged=False)
        hook = root / ".git" / "hooks" / "pre-commit"
        with open(hook, "w", encoding="utf-8", newline="\n") as stream:
            stream.write("#!/bin/sh\necho extra > extra.txt\ngit add extra.txt\n")
        hook.chmod(0o755)
        rehearsal = GP.gate_preflight.Rehearsal(task_root, "A")
        rehearsal.check_vcs()
        gate_brief.keep_shown_doors(task_root, {f["id"]: f["waives"] for f in rehearsal.findings if f.get("waives")})
        path = task_root / "state" / "answer.txt"
        path.write_text("vcs-test-repo: commit", encoding="utf-8")
        landed = run_script("repo_words.py", "--task", "TP1-15045", "--word", "commit", "--words-file", path, cwd=root, env=project_env(root))
        check_eq("cli: a commit that landed wrong exits 3 (F-5) with the problem and the door", (landed.returncode, "nothing is passed" in landed.stdout,
                 "--words-file" in landed.stdout), (3, True, True))
        pipeline = json.loads((task_root / "pipeline.json").read_text(encoding="utf-8"))
        check_eq("cli: ...and the person's word is kept as a remark, with no override that passes", (len(pipeline.get("remarks") or []), pipeline.get("stage_overrides") or []),
                 (1, []))
    finally:
        cleanup(root)


def _committed(c, state, dispatch_id="a2"):
    """`c._record_s5_word_passes` the way `apply` runs a validate (RD1-31): the passes are NOTED while the event is judged and written
    once it stands. Called with no collector (outside `apply`) the helper writes no row."""
    c._passes = []
    try:
        c._record_s5_word_passes({"id": dispatch_id, "scope": ["TC-1"]}, state)
    finally:
        noted, c._passes = c._passes, None
    c._record_noted_passes(dispatch_id, noted)


def _s5_completion(prefix: str, word_passes):
    """FV1-30a fixture: a real controller story whose S5 completion by the author's mechanical dispatch is accepted once its green run
    exists. `word_passes` replaces `s5_precheck.word_passes` (a list of rows, or an exception to raise): the selection of the word is
    the rows of `test_s5_precheck`; what is judged HERE is where the controller records it. Returns `(task root, controller,
    complete, journal lines)`: `complete(key)` applies the completion, `journal()` reads `state/passed-by-person.jsonl`."""
    import hashlib
    import s5_precheck as P
    import test_s5_process as S5
    from event_store import content_hash
    root, task = ctrl_project(prefix)
    c = S5.s5_task(task, ("TC-1",))
    S5.dispatch(c, task, "a1", scope=("TC-1",))
    S5.dispatch(c, task, "k1", role="qa-code-critic", scope=("TC-1",))
    S5.dispatch(c, task, "a2", scope=("TC-1",), accept=False, repair_cause="mechanical", reason="TC-1: a sleep -> a wait")
    obligation = next(ob for row in json.loads((task / "work" / "test-plan.json").read_text(encoding="utf-8"))["rows"]
                      for ob in row.get("coverage_obligations") or [])
    refs = [{"obligation_id": obligation["obligation_id"], "obligation_hash": content_hash(obligation)}]
    proof = S5.evidence(task, "proof.json")

    def complete(rounded: bool, key: str):
        probe = {"verdict": "intended_failure", "input_hash": "H0", "expected_location": "a", "actual_location": "a",
                 "expected_reason": "r", "actual_reason": "r", "failure_kind": "assertion", "mutation_kind": "assertion",
                 "proof_level": "live", "obligation_ids": [obligation["obligation_id"]], "obligation_refs": refs,
                 "obligation_hash": content_hash(refs), "assertion_id": "t.py:9", "defect_location": "src.py:4",
                 "evidence_ref": proof["path"]}
        record = {"schema_version": 2, "input_hash": "h", "required_quality_checks": [], "author_dispatch_id": "a1",
                  "reviewer_dispatch_id": "k1", "quality_receipts": [], "scope_instances": {"TC-1": ["test_x"]},
                  "instances": [{"schema_version": 2, "instance_id": "test_x", "input_hash": "H1", "outcome": "passed",
                                 "execution_fingerprint": "fp-1", "review": {"verdict": "approved", "input_hash": "H0"},
                                 "change_disposition": "new_or_changed", "change_basis_ref": "diff",
                                 "obligation_ids": [obligation["obligation_id"]], "obligation_refs": refs,
                                 "obligation_hash": content_hash(refs), "assertion_id": "t.py:9", "defect_location": "src.py:4",
                                 "probe": probe, "evidence_refs": [proof]}]}
        if rounded:
            record["mechanical_round"] = S5.ROUND
        (task / "work" / "s5-window.json").write_text(json.dumps(record), encoding="utf-8")
        receipt = {"path": "work/s5-window.json", "sha256": hashlib.sha256((task / "work" / "s5-window.json").read_bytes()).hexdigest()}
        return c.apply("accept", {"id": "a2", "status": "accepted", "stage_complete": True, "window": record,
                                  "evidence_refs": [proof, receipt], "idempotency_key": key})

    def fake(*_args, **_kwargs):
        if isinstance(word_passes, Exception):
            raise word_passes
        return list(word_passes)
    P.word_passes = fake
    return root, task, c, complete, S5


def row_fv130a_the_controller_records_what_the_word_passed() -> None:
    """FV1-30a (4): an ACCEPTED S5 completion records every finding a person's word passed, by name, through the one writer; a
    refused completion writes nothing; no word writes nothing; a recording that cannot be made leaves the completion accepted and
    says so on stderr; the cuts of the writer lose nothing (AT and BEYOND: `decision` 1000/1001, `finding_id` 400/401)."""
    import s5_precheck as P
    real = P.word_passes
    at = "2026-10-01T10:00:00+00:00"
    finding = "bindings:TC-1:no-bindings"
    try:
        # one accepted completion with a word by tag: exactly one line, `block` = the finding id, `word_at` = the word's `at`
        root, task, c, complete, S5 = _s5_completion("qa-words-door-fv30a-",
                                                       [{"finding_id": finding, "decision": "go on, the person knows", "at": at}])
        try:
            journal = task / "state" / "passed-by-person.jsonl"
            lines = lambda: [json.loads(x) for x in journal.read_text(encoding="utf-8").splitlines()] if journal.is_file() else []  # noqa: E731
            check_in("a completion with no mechanical round is refused", "mechanical_round", refused_text(lambda: complete(False, "no-round")))
            check_eq("a REFUSED completion writes nothing (the call sits after the refusals)", lines(), [])
            check_in("a completion with no green run is refused too", "mechanical_green", refused_text(lambda: complete(True, "no-green")))
            check_eq("...and writes nothing", lines(), [])
            S5.run_block(task, "b1", "a2", "fp-1", "H1", "test_x")
            check_eq("the ACCEPTED completion goes through", refused_text(lambda: complete(True, "done")), "")
            got = [line for line in lines() if line["block"] == finding]
            check_eq("ONE line, the stage and the dispatch, the finding id as the block, the word's own time as `word_at`",
                     [(x["stage"], x["dispatch"], x["block"], x["decision"], x["word_at"], x["by"]) for x in got],
                     [("S5", "a2", finding, "go on, the person knows", at, "human")])
            # AT / BEYOND, the writer's cuts: `decision` 1000 whole / 1001 cut, `finding_id` 400 whole / 401 cut with the whole beside it
            state = c.state()
            for label, rows, expect in (
                    ("decision of 1000", [{"finding_id": finding, "decision": "d" * 1000, "at": at}],
                     lambda x: len(x["decision"]) == 1000 and x["word_at"] == at and "finding_id" not in x),
                    ("decision of 1001", [{"finding_id": finding, "decision": "d" * 1001, "at": at}],
                     lambda x: len(x["decision"]) == 1000 and x["word_at"] == at),
                    ("a 24 KB decision", [{"finding_id": finding, "decision": "d" * 24 * 1024, "at": at}],
                     lambda x: len(x["decision"]) == 1000 and x["word_at"] == at),
                    ("finding id of 400", [{"finding_id": "b:" + "c" * 398, "decision": "x", "at": at}],
                     lambda x: len(x["block"]) == 400 and "finding_id" not in x),
                    ("finding id of 401", [{"finding_id": "b:" + "c" * 399, "decision": "x", "at": at}],
                     lambda x: len(x["block"]) == 400 and x["finding_id"] == "b:" + "c" * 399)):
                P.word_passes = lambda *_a, **_k: rows
                before = len(lines())
                c._record_s5_word_passes({"id": "a2", "scope": ["TC-1"]}, state)
                check_eq(f"{label}: the helper outside `apply` writes no row", len(lines()), before)
                _committed(c, state)
                added = lines()[before:]
                check(f"{label}: one line, cut as the writer cuts it, with the pointer to the whole", len(added) == 1 and expect(added[0]), str(added))
            P.word_passes = lambda *_a, **_k: []
            before = len(lines())
            c._record_s5_word_passes({"id": "a2", "scope": ["TC-1"]}, state)
            check_eq("no word passed anything: no line", len(lines()), before)
            # a recording that cannot be made: never silent, never a failed step
            for why, make in (("word_passes raises", lambda: RuntimeError("boom")), ):
                def raising(*_a, **_k):
                    raise make()
                P.word_passes = raising
                err = io.StringIO()
                with redirect_stderr(err):
                    c._record_s5_word_passes({"id": "a2", "scope": ["TC-1"]}, state)
                check_in(f"{why}: one stderr line", "passed-by-person: not recorded (RuntimeError: boom)", err.getvalue())
                check_eq(f"{why}: and no line", len(lines()), before)
            saved = sys.modules.get("s5_precheck")
            sys.modules["s5_precheck"] = None
            err = io.StringIO()
            try:
                with redirect_stderr(err):
                    c._record_s5_word_passes({"id": "a2", "scope": ["TC-1"]}, state)
            finally:
                sys.modules["s5_precheck"] = saved
            check_in("s5_precheck does not import: one stderr line", "passed-by-person: not recorded (", err.getvalue())
            check_eq("...and no line", len(lines()), before)
        finally:
            P.word_passes = real
            cleanup(root)
        # the completion is accepted although the recording failed
        root, task, c, complete, S5 = _s5_completion("qa-words-door-fv30a2-", RuntimeError("boom"))
        try:
            S5.run_block(task, "b1", "a2", "fp-1", "H1", "test_x")
            err = io.StringIO()
            with redirect_stderr(err):
                text = refused_text(lambda: complete(True, "done"))
            check_eq("a recording that fails: the completion is ACCEPTED", (text, c.state()["stages"]["S5"]["status"]), ("", "completed"))
            check_in("...and says so on stderr", "passed-by-person: not recorded (RuntimeError: boom)", err.getvalue())
        finally:
            P.word_passes = real
            cleanup(root)
    finally:
        P.word_passes = real


def row_fv130a_no_second_question() -> None:
    """FV1-30a: an instance whose no-run-row finding a person's word passed at the S5 exit is not refused a second time by the window
    gap check (`_s5_gap_problems`, FR-7) and an instance not passed still is; `_plan_refusal` records nothing (F4)."""
    import acceptance
    import s5_precheck as P
    import test_s5_process as S5
    root, task = ctrl_project("qa-words-door-fv30a3-")
    real_validate, real_passes = acceptance.validate_window, P.word_passes
    try:
        c = S5.s5_task(task, ("TC-1",))
        acceptance.validate_window = lambda window, root_: ["product:test_x", "product:test_y", "stale_run:test_x"]
        d, p = {"id": "a2", "scope": ["TC-1"]}, {}
        # FV1-30b: the let-go reads the window item (the no-run shape the writer builds) and the pass's `subjects` (the producer's
        # own list, `s5_precheck._finding(subjects=)`): a pass that names no instance lets nothing go
        no_run = {"evidence_refs": []}
        window = {"instances": [dict(no_run, instance_id="test_x"), dict(no_run, instance_id="test_y")]}
        P.word_passes = lambda *_a, **_k: []
        text = " ".join(m for _cls, m in c._s5_gap_problems(d, p, window))
        check("no word: both instances are refused", "product:test_x" in text and "product:test_y" in text, text)
        P.word_passes = lambda *_a, **_k: [{"finding_id": "run_mapping:TC-1:no-row-test_x", "check": "run_mapping", "case": "TC-1",
                                            "tag": "no-row-test_x", "decision": "go on", "at": "t",
                                            "subjects": [{"instance_id": "test_x"}]}]
        text = " ".join(m for _cls, m in c._s5_gap_problems(d, p, window))
        check("the passed instance is not refused a second time; the other still is; another gap of the passed one still is",
              "product:test_x" not in text and "product:test_y" in text and "stale_run:test_x" in text, text)
        P.word_passes = lambda *_a, **_k: [{"finding_id": "bindings:TC-1:no-bindings", "check": "bindings", "case": "TC-1",
                                            "tag": "no-bindings", "decision": "go on", "at": "t"}]
        text = " ".join(m for _cls, m in c._s5_gap_problems(d, p, window))
        check("a pass of ANOTHER finding (`no-bindings`) lets no instance go", "product:test_x" in text and "product:test_y" in text, text)
        P.word_passes = lambda *_a, **_k: [{"finding_id": "run_mapping:TC-1:no-row-test_x", "check": "run_mapping", "case": "TC-1",
                                            "tag": "no-row-test_x", "decision": "go on", "at": "t"}]
        text = " ".join(m for _cls, m in c._s5_gap_problems(d, p, window))
        check("(E4, E13) a pass of a line written before `subjects` names no instance: nothing goes on a guess",
              "product:test_x" in text and "product:test_y" in text, text)

        def boom(*_a, **_k):
            raise RuntimeError("boom")
        P.word_passes = boom
        text = " ".join(m for _cls, m in c._s5_gap_problems(d, p, window))
        check("a reader that cannot answer lets nothing go (the refusing direction)", "product:test_x" in text and "product:test_y" in text, text)
        # critic F4: `_plan_refusal` (it runs inside `validate`, on probes and refused requests) records nothing: the recording of
        # its pass is queued by the Lead
        journal = task / "state" / "passed-by-person.jsonl"
        (task / "pipeline.json").write_text(json.dumps({"ticket": TICKET, "stage_overrides": [
            {"stage": "S5", "match": "plan before windows", "decision": "the person lets it", "at": "2026-10-01T10:00:00+00:00"}]}),
            encoding="utf-8")
        check_eq("a word passes the plan refusal (as before)", c._plan_refusal("plan before windows", "no plan yet", "Door: x."), [])
        check_eq("...and `_plan_refusal` writes no record (F4: queued)", journal.is_file(), False)
    finally:
        acceptance.validate_window, P.word_passes = real_validate, real_passes
        cleanup(root)


def row_fv130b_the_journal_line_carries_the_subjects() -> None:
    """FV1-30b N0 (f), (g), E9, E13: the line of a pass carries `check`, `case`, `tag` and `subjects` (each only when it has a value);
    `subjects` is cut at 200 entries with `subjects_cut` beside it, AT (200) and BEYOND (201, 5000), and the reader names only the
    entries listed; a line written before this node (no such key) is read as before."""
    import s5_precheck as P
    real = P.word_passes
    at = "2026-10-01T10:00:00+00:00"
    root, task, c, complete, S5 = _s5_completion("qa-words-door-fv30b-", [])
    try:
        journal = task / "state" / "passed-by-person.jsonl"
        lines = lambda: [json.loads(x) for x in journal.read_text(encoding="utf-8").splitlines()] if journal.is_file() else []  # noqa: E731
        state = c.state()
        with_subjects = {"finding_id": "run_mapping:TC-1:no-row-test_x", "check": "run_mapping", "case": "TC-1", "tag": "no-row-test_x",
                         "decision": "go on", "at": at, "subjects": [{"instance_id": "test_x"}]}
        case_less = {"finding_id": "plan:-:plan-unreadable", "check": "plan", "case": "", "tag": "plan-unreadable", "decision": "d", "at": at,
                     "subjects": []}
        P.word_passes = lambda *_a, **_k: [with_subjects, case_less]
        c._record_s5_word_passes({"id": "a2", "scope": ["TC-1"]}, state)
        check_eq("(f) the recording called outside `apply` (no collector) writes no row, and does not raise", lines(), [])
        _committed(c, state)
        got = lines()
        check_eq("(f) a pass with subjects: check, case, tag and subjects on the line, no cut mark",
                 [(x["check"], x["case"], x["tag"], x["subjects"], "subjects_cut" in x) for x in got[:1]],
                 [("run_mapping", "TC-1", "no-row-test_x", [{"instance_id": "test_x"}], False)])
        check_eq("(f) a case-less pass with no subjects: check and tag, and NO `case`, `subjects`, `subjects_cut` (written only when non-empty)",
                 [(x.get("check"), x.get("tag"), "case" in x, "subjects" in x, "subjects_cut" in x) for x in got[1:]],
                 [("plan", "plan-unreadable", False, False, False)])
        # (g) the cut, AT and BEYOND
        for count, cut in ((1, False), (200, False), (201, True), (5000, True)):
            rows = [dict(with_subjects, subjects=[{"instance_id": f"i{n}"} for n in range(count)])]
            P.word_passes = lambda *_a, **_k: rows
            before = len(lines())
            _committed(c, state)
            line = lines()[before]
            check_eq(f"(g) {count} subjects: {min(count, 200)} on the line, `subjects_cut` {'= ' + str(count) if cut else 'absent'}",
                     (len(line["subjects"]), line.get("subjects_cut")), (min(count, 200), count if cut else None))
        passes, why = waiver.person_passes(task)
        index = waiver.word_passed_index(passes)
        check_eq("(g) the reader names the 200 listed instances", [bool(index.instance("not_run", f"i{n}")) for n in (0, 199)], [True, True])
        check_eq("(g) ...and passes none of the 4800 cut: a cut never passes an unnamed instance",
                 [bool(index.instance("not_run", f"i{n}")) for n in (200, 201, 4999)], [False, False, False])
        cut_pass = next(p for p in index.all() if p.get("subjects_cut"))
        check_eq("(g) ...and the pass carries the whole count for the report's `and N more`", cut_pass["subjects_cut"], 5000)
        # E13: a line written before this node
        old = {"ts": "2026-10-01T10:00:00+00:00", "stage": "S5", "dispatch": "a2", "block": "bindings:TC-1:no-bindings", "decision": "go", "by": "human"}
        with journal.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(old) + "\n")
        passes, why = waiver.person_passes(task)
        old_row = next(p for p in passes if p["finding_id"] == "bindings:TC-1:no-bindings")
        check_eq("E13: an old line is read: its parts from the block, no subjects", (old_row["check"], old_row["case"], old_row["tag"], old_row["subjects"]),
                 ("bindings", "TC-1", "no-bindings", []))
        check_eq("E13: ...and it matches no Then (an old record never lets a gate go on a guess)",
                 waiver.word_passed_index(passes).then("TC-1", 1), None)
    finally:
        P.word_passes = real
        cleanup(root)


def row_fv130b_person_passes() -> None:
    """FV1-30b N0 (h): `waiver.person_passes` - no file, unreadable, torn, old, repeated (E1-E5)."""
    root = Path(temp_dir("qa-words-door-fv30b-pp-"))
    try:
        (root / "state").mkdir()
        journal = root / "state" / "passed-by-person.jsonl"

        def put(*lines, raw=b"") -> None:
            journal.write_bytes(raw + "".join(json.dumps(x, ensure_ascii=False) + "\n" for x in lines).encode("utf-8"))

        check_eq("E1: no file: no pass, no reason", waiver.person_passes(root), ([], ""))
        journal.mkdir()
        rows, why = waiver.person_passes(root)
        check("E2: the path cannot be read (a directory): `(None, why)`, never a pass", rows is None and "could not be read" in why, str((rows, why)))
        journal.rmdir()
        at = "2026-10-01T10:00:00+00:00"
        (root / "pipeline.json").write_text(json.dumps({"stage_overrides": [
            {"stage": "S5", "match": "*", "decision": "the person's whole word " + "w" * 3000, "at": at}]}), encoding="utf-8")
        good = {"ts": "2026-10-01T10:05:00+00:00", "stage": "S5", "dispatch": "a2", "block": "run_mapping:TC-1:no-row-x", "decision": "short",
                "by": "human", "word_at": at, "check": "run_mapping", "case": "TC-1", "tag": "no-row-x", "subjects": [{"instance_id": "x"}]}
        # E3: a torn line, a non-object, a line with no block, bytes that are no UTF-8: each skipped, the others stay
        put(good, raw=b'{"stage": "S5", "block": "torn\n[1, 2]\n\xff\xfe not text\n' + json.dumps({"stage": "S5", "decision": "no block"}).encode() + b"\n")
        rows, why = waiver.person_passes(root)
        check_eq("E3: the good line survives four bad ones", [r["finding_id"] for r in rows], ["run_mapping:TC-1:no-row-x"])
        for line_no in ("line 1 ", "line 2 ", "line 3 ", "line 4 "):
            check_in(f"E3: the one reason names {line_no.strip()}", line_no, why)
        check_eq("E3: one reason, not one per line", why.count("were skipped"), 1)
        check_eq("the word is the person's WHOLE word from stage_overrides by `word_at`, not the cut decision",
                 (len(rows[0]["word"]), rows[0]["word_recorded"], rows[0]["decision"]), (3024, True, "short"))
        check_eq("...`at` is the `word_at`; `ts` and `by` are the line's", (rows[0]["at"], rows[0]["ts"], rows[0]["by"]), (at, good["ts"], "human"))
        # E11: word_at names no word in the record: the decision stands, marked not recorded
        put(dict(good, word_at="2026-01-01T00:00:00+00:00"))
        check_eq("E11: `word_at` names no recorded word: the decision, `word_recorded` False",
                 [(r["word"], r["word_recorded"]) for r in waiver.person_passes(root)[0]], [("short", False)])
        (root / "pipeline.json").write_text("{torn", encoding="utf-8")
        put(good)
        check_eq("`pipeline.json` unreadable: the decision, not a failure", [(r["word"], r["word_recorded"]) for r in waiver.person_passes(root)[0]],
                 [("short", False)])
        # E4: an old line (no check, case, tag, subjects, word_at): parts from the block, split once
        old = {"ts": "2026-10-01T10:00:00+00:00", "stage": "S5", "dispatch": "a1", "block": "manifest:-:row-fields-missing", "decision": "go", "by": "human"}
        old2 = dict(old, block="bindings:TC-1:unbound-2", dispatch="a1")
        colon = dict(old, block="oracle:TC-1:changed-after-red-a.py:12")
        put(old, old2, colon)
        rows, why = waiver.person_passes(root)
        check_eq("E4: old lines are taken apart from the block: a `-` case is empty, a tag keeps its colon",
                 [(r["check"], r["case"], r["tag"], r["subjects"], r["at"]) for r in rows],
                 [("manifest", "", "row-fields-missing", [], ""), ("bindings", "TC-1", "unbound-2", [], ""), ("oracle", "TC-1", "changed-after-red-a.py:12", [], "")])
        check_eq("E4: and the index maps them to their facts but names no Then or instance",
                 ([p["fact"] for p in waiver.word_passed_index(rows).all()], waiver.word_passed_index(rows).then("TC-1", 2)),
                 (["row_fields_unestablished", "then_unbound", "other"], None))
        # a block cut at 400 with the whole id beside it: the whole id is the finding
        long_id = "bindings:TC-1:" + "t" * 500
        put(dict(old, block=long_id[:400], finding_id=long_id))
        check_eq("a cut block: the whole `finding_id` is read", [r["finding_id"] for r in waiver.person_passes(root)[0]], [long_id])
        # stages: only S5
        put(dict(old, stage="S4"), old)
        check_eq("a line of another stage is no S5 pass", len(waiver.person_passes(root)[0]), 1)
        # E5: repeats of (dispatch, block, word_at) collapse; another dispatch or word is another pass
        put(old, dict(old, ts="2026-10-01T12:00:00+00:00", decision="again"), dict(old, dispatch="a2"), dict(old, word_at="2026-10-02T00:00:00+00:00"))
        rows, _why = waiver.person_passes(root)
        check_eq("E5: two lines of the same (dispatch, block, word_at) are one pass, the later; another dispatch / word_at is its own",
                 sorted((r["dispatch"], r["at"], r["decision"]) for r in rows),
                 sorted([("a1", "", "again"), ("a2", "", "go"), ("a1", "2026-10-02T00:00:00+00:00", "go")]))
        check_eq("E5: the index collapses the same repeat too", len(waiver.word_passed_index(rows + rows).all()), len(rows))
        late = waiver.word_passed_index([
            {"finding_id": "plan:-:plan-unreadable", "decision": "old", "ts": "2026-10-01T09:00:00+00:00", "dispatch": "a1", "at": "t1"},
            {"finding_id": "plan:-:plan-unreadable", "decision": "new", "ts": "2026-10-01T10:00:00+00:00", "dispatch": "a2", "at": "t2"},
            {"finding_id": "plan:-:plan-unreadable", "decision": "mid", "ts": "2026-10-01T09:30:00+00:00", "dispatch": "a3", "at": "t3"}])
        check_eq("E5: three passes of one fact, the latest by ts answers", (len(late.all()), late.s5_plan()["decision"]), (3, "new"))
    finally:
        cleanup(root)


def row_fv130b_the_one_reader() -> None:
    """FV1-30b N0 (i), (j), (k), (l), E18, E20, E26: `waiver.word_passed_index` and `waiver.row_fields`."""
    def rows_of(*rows):
        return waiver.word_passed_index(list(rows))

    def pass_row(finding_id, subjects=None, **extra):
        return dict({"finding_id": finding_id, "decision": "go on", "at": "2026-10-01T10:00:00+00:00", "subjects": subjects or []}, **extra)

    # (i) .then: case_matches, a sibling case misses; the number must be a real Then number
    then = rows_of(pass_row("bindings:TC-1:no-bindings", [{"case": "TC-1", "then": 1}, {"case": "TC-1", "then": 3}]))
    check_eq("(i) .then hits a named Then", [bool(then.then("TC-1", n)) for n in (1, 3)], [True, True])
    check_eq("(i) .then misses an unnamed Then and a sibling case", [bool(then.then("TC-1", 2)), bool(then.then("TC-2", 1)), bool(then.then("TC-10", 1))],
             [False, False, False])
    check_eq("(i) .then reads `then` as the contract does: `\"3\"` hits, 0 / True / junk miss",
             [bool(then.then("TC-1", v)) for v in ("3", 0, True, None, "x", [3])], [True, False, False, False, False, False])
    check_eq("(i) .then: a bare id matches any area (`case_matches`), and an empty case matches nothing",
             [bool(then.then("feedback-api/TC-1", 1)), bool(then.then("", 1))], [True, False])
    unbound = rows_of(pass_row("bindings:TC-1:unbound-2", [{"case": "TC-1", "then": 2}]))
    check_eq("(i) `unbound-2` is a then_unbound pass", (unbound.all()[0]["fact"], bool(unbound.then("TC-1", 2))), ("then_unbound", True))
    check_eq("(i) .then asks only the then_unbound fact: a not_run pass naming a Then answers nothing",
             rows_of(pass_row("run_mapping:TC-1:no-row-A", [{"case": "TC-1", "then": 1}])).then("TC-1", 1), None)
    # (i) .instance: an alias hits, a parameter-label prefix misses
    inst = rows_of(pass_row("run_mapping:TC-1:no-row-TC-1::test_x[eu]", [{"instance_id": "TC-1::test_x[eu]"}]))
    check_eq("(i) .instance hits the id itself and its bare alias",
             [bool(inst.instance("not_run", i)) for i in ("TC-1::test_x[eu]", "test_x[eu]")], [True, True])
    check_eq("(i) .instance misses a prefix, another label, another case's spelling and the wrong fact",
             [bool(inst.instance("not_run", i)) for i in ("test_x", "test_x[eu2]", "TC-2::test_x[eu]", "test_x[eu][neg]", "")] +
             [bool(inst.instance("row_fields_unestablished", "test_x[eu]"))], [False] * 6)
    label = rows_of(pass_row("run_mapping:TC-1:no-row-A", [{"instance_id": "A"}]))
    check_eq("(j) a pass for `no-row-A` does not pass the instance `A[neg]` (30a B1)",
             (bool(label.instance("not_run", "A")), label.instance("not_run", "A[neg]"), label.instance("not_run", "A[neg]x")), (True, None, None))
    # (i) unknown (check, tag) is `other`; unmatched-A is no fact; a prefix needs something after it
    odd = rows_of(pass_row("bindings:TC-1:contradicted-1"), pass_row("run_mapping:TC-1:unmatched-A", [{"instance_id": "A"}]),
                  pass_row("run_mapping:TC-1:no-row-"), pass_row("bindings:TC-1:no-bindings-extra"), pass_row("manifest:-:row-fields-missing-x"),
                  pass_row("oracle:TC-1:no-row-A"), pass_row("plan:-:plan-unreadable"))
    check_eq("(i) unknown (check, tag), `unmatched-A`, a bare prefix, a longer exact tag and a tag of another check are `other`; the plan is its fact",
             [p["fact"] for p in odd.all()], ["other"] * 6 + ["s5_plan_unread"])
    check_eq("(i) ...and `unmatched-A` answers no lookup of a fact a gate asks (it is `other`: a report line only)",
             [odd.instance(f, "A") for f in ("not_run", "row_fields_unestablished", "then_unbound")] + [odd.then("TC-1", 1)], [None] * 4)
    check_eq("(i) .s5_plan answers the plan pass, and None without one", (bool(odd.s5_plan()), rows_of().s5_plan()), (True, None))
    facts = rows_of(pass_row("bindings:TC-1:no-bindings"), pass_row("bindings:TC-1:unbound-7"), pass_row("run_mapping:TC-1:no-row-x"),
                    pass_row("manifest:-:row-fields-missing"), pass_row("plan:-:plan-unreadable"))
    check_eq("(i) the table maps each of its five rows", [p["fact"] for p in facts.all()],
             ["then_unbound", "then_unbound", "not_run", "row_fields_unestablished", "s5_plan_unread"])
    check_eq("(i) a pass is the keys of the spec", sorted(facts.all()[0]), sorted(["finding_id", "check", "case", "tag", "fact", "decision", "at", "by", "ts", "fields"]))
    # (k) a field the table does not pass is never passed, though the subject names it
    named = pass_row("manifest:-:row-fields-missing", [{"instance_id": "A", "fields": ["obligation_refs", "change_disposition", "input_hash", "no_such_field"]}])
    fields = rows_of(named)
    # (N1 added the `profile_id` row, so the field with NO row is a name the table never had)
    check_eq("(k) .instance with `obligation_refs` hits; `change_disposition`, `input_hash` and a field with NO row (`no_such_field`) miss",
             [bool(fields.instance("row_fields_unestablished", "A", field=f)) for f in ("obligation_refs", "change_disposition", "input_hash", "no_such_field", "other_field")],
             [True, False, False, False, False])
    check_eq("(k) .instance with no field names the instance", bool(fields.instance("row_fields_unestablished", "A")), True)
    check_eq("(k) another instance is named by nothing", [fields.instance("row_fields_unestablished", "B", field="obligation_refs"), fields.passed_fields("B")], [None, []])
    check_eq("(k) passed_fields lists only `obligation_refs` for a subject of [obligation_refs, change_disposition]",
             rows_of(pass_row("manifest:-:row-fields-missing", [{"instance_id": "A", "fields": ["obligation_refs", "change_disposition"]}])).passed_fields("A"),
             ["obligation_refs"])
    check_eq("(k) ...and the pass says every field the subjects name (the table decides what passes)",
             fields.all()[0]["fields"], ["obligation_refs", "change_disposition", "input_hash", "no_such_field"])
    check_eq("(k) a subject whose `fields` is no list names no field", rows_of(pass_row("manifest:-:row-fields-missing", [{"instance_id": "A", "fields": "obligation_refs"}])).passed_fields("A"), [])
    # E20: the same, through the deletion-loop's view - a pass naming only excluded fields passes nothing
    check_eq("E20: a pass naming only `change_disposition` / `input_hash` lets no field go",
             rows_of(pass_row("manifest:-:row-fields-missing", [{"instance_id": "A", "fields": ["change_disposition", "input_hash"]}])).passed_fields("A"), [])
    # (l) / E26: the table unreadable or without its section: facts still map, no field passes
    tmp = Path(temp_dir("qa-words-door-fv30b-rf-"))
    try:
        absent = tmp / "absent.json"
        broken = tmp / "broken.json"
        broken.write_text("{torn", encoding="utf-8")
        nosection = tmp / "nosection.json"
        nosection.write_text(json.dumps({"facts": [{"check": "manifest", "tag": "row-fields-missing", "match": "exact", "fact": "row_fields_unestablished"}]}), encoding="utf-8")
        notobject = tmp / "notobject.json"
        notobject.write_text(json.dumps({"row_fields": ["obligation_refs"]}), encoding="utf-8")
        toplist = tmp / "toplist.json"
        toplist.write_text("[1]", encoding="utf-8")
        good = tmp / "good.json"
        good.write_text(json.dumps({"row_fields": {"obligation_refs": {"pass": True}, "bad_row": "x", "falsy": {"pass": "yes"}}}), encoding="utf-8")
        for label, path in (("the file absent", absent), ("the file not JSON", broken), ("the file a directory (unreadable)", tmp),
                            ("the section absent", nosection), ("the section not an object", notobject), ("the file not an object", toplist)):
            got, why = waiver.row_fields(path)
            check(f"(l) {label}: `({{}}, why)`", got == {} and bool(why), str((got, why)))
        got, why = waiver.row_fields(good)
        check_eq("(l) a good file: the rows that are objects; the section is read as is", (sorted(got), why), (["falsy", "obligation_refs"], ""))
        table = {"facts": [{"check": "manifest", "tag": "row-fields-missing", "match": "exact", "fact": "row_fields_unestablished"}]}
        for label, tb in (("no `row_fields`", table), ("a `row_fields` list", dict(table, row_fields=["obligation_refs"])),
                          ("a `row_fields` null", dict(table, row_fields=None)), ("`pass` that is not True", dict(table, row_fields={"obligation_refs": {"pass": "yes"}}))):
            idx = waiver.word_passed_index([named], tb)
            check_eq(f"E26: {label}: the fact still maps, no field passes",
                     (idx.all()[0]["fact"], idx.passed_fields("A"), idx.instance("row_fields_unestablished", "A", field="obligation_refs")),
                     ("row_fields_unestablished", [], None))
    finally:
        cleanup(tmp)
    real, none_why = waiver.row_fields()
    check_eq("(l) the shipped table: obligation_refs passes, the two measured exclusions do not",
             (real["obligation_refs"]["pass"], real["change_disposition"]["pass"], real["input_hash"]["pass"], none_why), (True, False, False, ""))
    check_eq("(l) ...and the shipped table carries the keys N1 reads", (sorted(real["obligation_refs"]["window_keys"]), real["obligation_refs"]["tier4_gaps"]),
             (["obligation_hash", "obligation_ids", "obligation_refs"], ["obligation_binding", "obligation_hash"]))
    # a table that is unreadable maps every pass to `other` (the reader never raises)
    for label, tb in (("an empty table", {}), ("facts not a list", {"facts": "x"}), ("a facts row with no tag", {"facts": [{"check": "manifest"}]}),
                      ("a match that is neither exact nor prefix", {"facts": [{"check": "manifest", "tag": "row-fields-missing", "match": "regex", "fact": "f"}]})):
        check_eq(f"{label}: every pass is `other`", [p["fact"] for p in waiver.word_passed_index([named], tb).all()], ["other"])
    # never raises, counts what is no pass
    junk = waiver.word_passed_index([None, 5, "x", {}, {"subjects": [1]}, pass_row("bindings:TC-1:no-bindings", "not a list"),
                                     pass_row("bindings:TC-1:no-bindings", [None, 3, {"case": 7, "then": "x"}, {"instance_id": None}], at="t2")])
    check_eq("junk rows are counted, not raised: five are no pass, two are passes that name nobody",
             (junk.skipped, len(junk.all()), junk.then("TC-1", 1), junk.instance("not_run", "A")), (5, 2, None, None))
    check_eq("rows that are not a list (the record could not be read: None) name nobody", [waiver.word_passed_index(v).all() for v in (None, 5, "x", {})], [[]] * 4)
    check_eq("lookups on junk arguments answer None / []", (junk.then(None, None), junk.instance(None, None), junk.passed_fields(None), junk.instance("not_run", [1])),
             (None, None, [], None))


def row_fv130b_the_two_survivors() -> None:
    """FV1-30b topic fix (F3, F5): `s5_precheck.live_word_index` and `waiver.record_word_index` never raise; None names nobody, an
    empty read is an empty index (not None); the live one forwards its scope; `_finding_tag` is the waiver splitter's tag."""
    import s5_precheck
    root = Path(temp_dir("qa-words-door-fv30b-sv-"))
    real, seen = s5_precheck.word_passes, []
    named = {"finding_id": "run_mapping:TC-1:no-row-A", "check": "run_mapping", "case": "TC-1", "tag": "no-row-A", "decision": "go on",
             "at": "t1", "subjects": [{"instance_id": "A"}]}
    try:
        def fake(task_root, scope=None, dispatch_id=None):
            seen.append((str(task_root), scope, dispatch_id))
            return [named]
        s5_precheck.word_passes = fake
        index = s5_precheck.live_word_index(root, ["TC-1"], "d1")
        check_eq("live: the passes read as facts, the scope and the dispatch forwarded",
                 (bool(index.instance("not_run", "A")), seen), (True, [(str(root), ["TC-1"], "d1")]))
        check_eq("live: an empty scope is None (every case), as `word_passes` reads it", (s5_precheck.live_word_index(root, [])
                 and seen[-1][1]), None)
        s5_precheck.word_passes = lambda *_a, **_k: (_ for _ in ()).throw(RuntimeError("unreadable artifact"))
        check_eq("live: a reader that raises -> None (names nobody, never a pass)", s5_precheck.live_word_index(root), None)
    finally:
        s5_precheck.word_passes = real
    try:
        check_eq("live: no live S5 word -> an empty index, not None", s5_precheck.live_word_index(root).all(), [])
        check_eq("record: no file -> an empty index, not None", waiver.record_word_index(root).all(), [])
        (root / "state").mkdir()
        journal = root / "state" / "passed-by-person.jsonl"
        journal.write_text(json.dumps({"ts": "2026-10-01T10:05:00+00:00", "stage": "S5", "dispatch": "a2", "block": "run_mapping:TC-1:no-row-A",
                                       "decision": "short", "by": "human", "subjects": [{"instance_id": "A"}]}) + "\n", encoding="utf-8")
        check_eq("record: a line -> the index names the instance", bool(waiver.record_word_index(root).instance("not_run", "A")), True)
        journal.unlink()
        journal.mkdir()
        check_eq("record: a path that cannot be read -> None (names nobody)", waiver.record_word_index(root), None)
        check_eq("record: a task root that is no path at all -> None, never a raise", waiver.record_word_index(object()), None)
    finally:
        cleanup(root)
    check_eq("F5: `_finding_tag` is the waiver splitter's tag (a tag carries `file.py:79`), and \"\" for no id",
             [s5_precheck._finding_tag({"id": i}) for i in ("bindings:TC-1:x.py:79", "bindings:-:t", "bindings", "")] + [s5_precheck._finding_tag({})],
             ["x.py:79", "t", "", "", ""])
    check_eq("F2: `waiver.same_instance` is public: an alias is the instance, another case's spelling is not",
             [waiver.same_instance("TC-1::x", "x"), waiver.same_instance("TC-1::x", "TC-2::x")], [True, False])


def row_fv130b_n1_the_not_run_section_and_the_field_rows() -> None:
    """FV1-30b N1 (n): `waiver.not_run_lets_go()` is `({}, why)` for a file absent / not JSON / a directory / not an object / a section
    absent / a section that is no object (nothing is let go, E30), and the section as it is otherwise; the shipped `change_basis_ref` row is
    not passable and says why."""
    tmp = Path(temp_dir("qa-words-door-fv30b-nr-"))
    try:
        absent, broken, toplist = tmp / "absent.json", tmp / "broken.json", tmp / "toplist.json"
        broken.write_text("{torn", encoding="utf-8")
        toplist.write_text("[1]", encoding="utf-8")
        nosection, notobject, good = tmp / "nosection.json", tmp / "notobject.json", tmp / "good.json"
        nosection.write_text(json.dumps({"row_fields": {}}), encoding="utf-8")
        notobject.write_text(json.dumps({"not_run": ["product"]}), encoding="utf-8")
        good.write_text(json.dumps({"not_run": {"tier4_gaps": ["product"]}}), encoding="utf-8")
        for label, path in (("the file absent", absent), ("the file not JSON", broken), ("the file a directory (unreadable)", tmp),
                            ("the file not an object", toplist), ("the section absent", nosection), ("the section not an object", notobject)):
            got, why = waiver.not_run_lets_go(path)
            check(f"(n) {label}: `({{}}, why)`", got == {} and bool(why), str((got, why)))
        check_eq("(n) a good file: the section as it is", waiver.not_run_lets_go(good), ({"tier4_gaps": ["product"]}, ""))
    finally:
        cleanup(tmp)
    # (F10: the shipped table's VALUES are data, pinned by no row here; the behaviour they drive is rows (g)/(l) and test_window_record)
    rows, _why = waiver.row_fields()
    check_eq("the shipped rows: change_basis_ref is NOT passable and says why", (rows["change_basis_ref"]["pass"], bool(rows["change_basis_ref"].get("why"))), (False, True))


def main() -> None:
    row_fv130b_n1_the_not_run_section_and_the_field_rows()
    row_fv130b_the_two_survivors()
    row_fv130b_the_journal_line_carries_the_subjects()
    row_fv130b_person_passes()
    row_fv130b_the_one_reader()
    row_fv130a_the_controller_records_what_the_word_passed()
    row_fv130a_no_second_question()
    row_repo_words_cli()
    row_words_carry()
    row_settle_order()
    row_leave_unlaunched()
    part_in_flight()
    part_launcher()
    finish("test_words_doors_flight_launcher")


# split: runner piece 1
if __name__ == "__main__":
    main()
