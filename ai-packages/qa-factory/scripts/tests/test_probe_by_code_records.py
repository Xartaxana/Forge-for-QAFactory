"""records: a part of test_probe_by_code.py, split by tools/test_split.py (TD-11c). The shared helpers are in probe_by_code_common."""
import json
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import SCRIPTS, check, check_eq, check_in, cleanup, finish, run_script, temp_dir, use_project
sys.path.insert(0, str(SCRIPTS))
import probe_by_code as PBC  # noqa: E402
import proof_level as PL  # noqa: E402
import probe_entries  # noqa: E402
del probe_entries  # split: imported for its sys.path effect
from probe_by_code_common import (  # noqa: E402
    CALC, DISPATCH, FAKE_RUN_SUITE, TASK, TEST_FILE_REL, env_for, fresh, give_word, manifest_of,
    model_entries, read_record, row_of, run, snapshot, task_of, write_json,
)


ANSWER_KEYS = ["verdict", "instance_id", "by", "level", "receipt_ref", "record", "prior_verdict",
               "recorded_at", "holds", "words", "block"]


def stamp_record(root: Path, instance: str, **fields) -> dict:
    """Rewrite fields of the probe's own record (a fixture's way to say 'recorded long ago', or 'said
    no_failure'): the record is plain JSON and the test file, not the tool, is under test here."""
    path = task_of(root) / "work" / "probes" / f"{instance}.json"
    body = json.loads(path.read_text(encoding="utf-8"))
    body.update(fields)
    write_json(path, body)
    return body


# t-2064 P4b: the key set of a WALK's aggregate (was the first-check record's: `author_run_block` and `run` are gone; the plan's `checks`,
# `mutated_files`, `plan_runs`, `plan_remaining`, `plan_unfinished` and `words` are new). `publish` / `binding` / `receipt*` are the
# receipt's: they stand until item 4 attaches a receipt to the aggregate. `judgment_owed` and `walk_ended` are the aggregate's own,
# each with a reader (named at its line below).
INVERT_RECORD_KEYS = [
    "actual_location", "actual_reason", "assertion_id", "binding", "case", "checks", "defect_location",
    "dispatch_id", "evidence_ref", "evidence_refs", "expected_location", "expected_reason", "failure_kind",
    "input_hash", "input_hash_source", "instance_content_sha", "instance_id", "instance_identity",
    "judgment_owed",     # `_judgment_fold`, always written; read by `proof_level.probe_record_state` -> `probe_plain_call_owed`
    "manifest_fields_missing", "mutated_file", "mutated_files", "mutation", "mutation_detail", "mutation_kind", "notes",
    "obligation_hash", "obligation_ids", "obligation_refs", "observed", "plan_remaining", "plan_runs", "plan_unfinished",
    "probe_tool", "proof_level",
    "proved_by",     # t-2064 N3b step 5: an `intended_failure` the code proved says how (`marker`, the token read in the row)
    "publish", "receipt", "receipt_missing", "record", "recorded_at", "request", "restore", "schema_version", "target",
    "task", "test_code_sha", "test_file_sha256", "test_node", "verdict",
    "walk_ended",        # `_aggregate_record`; read by `_refold` (the judge's rebuild of the aggregate: `walk["ended"]`)
    "window_probe", "words"]


def the_record_and_the_answer_are_pinned(stub: Path) -> None:
    """B-426 D1 characterisation: `_probe` is split into helpers, and what it hands back must not move. The
    written record's sorted key set and its notes on the invert path, the key set and notes of the
    `already_probed` answer, and the notes of a manifest row that names another file (the repeat check is not
    made, the record binds the bytes measured here) are compared with the values the unsplit function gave."""
    with fresh() as root:
        proc, first = run(root, stub, f"{TEST_FILE_REL}::test_add", "test_add")
        written = read_record(root, "test_add")
        check_eq("pinned invert: exit 0, intended_failure", (proc.returncode, written.get("verdict")),
                 (0, "intended_failure"))
        check_eq("pinned invert: the written record's key set", sorted(written), INVERT_RECORD_KEYS)
        check_eq("pinned invert: the answer printed is the record written", sorted(first), sorted(written))
        check_eq("pinned invert: its notes", written.get("notes"),
                 [# t-2064 P4b: no `assertion_id` note - the default road walks every check and never chooses a target by the id
                  "command, fingerprint file list and runtime probe are those of this story's last typed run on "
                  "profile unit"])
        proc, answer = run(root, stub, f"{TEST_FILE_REL}::test_add", "test_add")
        # t-2064 fix round A, B3: a second call over the same bytes and entries of a WHOLE walk (receipt on the row, every proved per-check
        # record readable) is answered `already_probed`: the walk's repeat is the old road's one question. These two checks add what the
        # "twice" check (a subset test) does not: the EXACT key set of that answer, `_repeat_answer`'s keys plus `notes`.
        check_eq("pinned answer: exit 0, the walk's repeat is answered already_probed (B3)", (proc.returncode, answer.get("verdict")),
                 (0, "already_probed"))
        check_eq("pinned answer: the key set is the already_probed answer's", sorted(answer), sorted(ANSWER_KEYS + ["notes"]))
    with fresh() as root:
        manifest = manifest_of(root)
        for row in manifest["tests"]:
            if row["instance_id"] == "test_dead_assert":
                row["file"] = "tests/nope.py"
        write_json(task_of(root) / "work" / "automation-manifest.json", manifest)
        proc, got = run(root, stub, f"{TEST_FILE_REL}::test_dead_assert", "test_dead_assert")
        check_eq("pinned mismatch: the probe runs", (proc.returncode, got.get("verdict")), (0, "no_failure"))
        # t-2064 P4b: the walk makes no repeat check (so no "not the file the row names" note), chooses no target by the id, and the
        # missing manifest fields are the aggregate's `manifest_fields_missing`, not a note
        check_eq("pinned mismatch: the notes, in order", read_record(root, "test_dead_assert").get("notes"), [
            "command, fingerprint file list and runtime probe are those of this story's last typed run on "
            "profile unit"])


def the_repeat_is_answered(stub: Path) -> None:
    logs = temp_dir("qa-probe-logs-")

    def go(root, name, node, iid, mutation="invert", **extra):
        return run(root, stub, f"{TEST_FILE_REL}::{node}", iid, mutation,
                   PROBE_STUB_LOG=str(logs / f"{name}.log"), **extra)

    def launches(name) -> int:
        path = logs / f"{name}.log"
        return len(path.read_text(encoding="utf-8").splitlines()) if path.is_file() else 0

    try:
        # AC1: the same bytes twice - the runner ran ONCE, and nothing was launched the second time.
        # t-2064 P4b: the subject is a PROVED check (`test_add`, `intended_failure`): the walk skips a check proved on the same bytes of its
        # file with the same entry (spec section 14), so the one launch and "nothing launched or written but the aggregate" hold. The ANSWER
        # of the repeat is `already_probed` by the receipt (t-2064 fix round A, B3; the spec's keys, `by`, block and words, one printed
        # line). The old subject, a `no_failure` check, is not a proof
        # and is walked again: see the "no_failure" group below (PRODUCT QUESTION 2).
        with fresh() as root:
            authored = (root / TEST_FILE_REL).read_bytes()
            aggregate = "work/probes/test_add.json"
            proc, first = go(root, "twice", "test_add", "test_add")
            check_eq("twice: the first probe runs and proves the check", (proc.returncode, first.get("verdict")),
                     (0, "intended_failure"))
            quiet = snapshot(root)
            proc, second = go(root, "twice", "test_add", "test_add")
            check("twice: exit 0", proc.returncode == 0, proc.stdout + proc.stderr)
            check_eq("twice: the fake runner was launched ONCE", launches("twice"), 1)
            check_eq("twice: nothing launched or written but the aggregate (requests, jobs, check records, receipts, manifest)",
                     {k: v for k, v in snapshot(root).items() if k != aggregate}, {k: v for k, v in quiet.items() if k != aggregate})
            check_eq("twice: the test file was never touched", (root / TEST_FILE_REL).read_bytes(), authored)
            check_eq("twice: answered, not probed (spec; PRODUCT QUESTION 1)", second.get("verdict"), "already_probed")
            check_eq("twice: the answer carries every key (spec; PRODUCT QUESTION 1)", [k for k in ANSWER_KEYS if k in second],
                     ANSWER_KEYS)
            check_eq("twice: by the receipt, saying what it said (spec; PRODUCT QUESTION 1)", (second.get("by"), second.get("prior_verdict")),
                     ("receipt", "intended_failure"))
            check_eq("twice: the block is the constant a person's word matches (spec; PRODUCT QUESTION 1)", second.get("block"),
                     PL.PROBE_BLOCK)
            check_in("twice: the words name the door (the person's word, the stage, the block) (spec; PRODUCT QUESTION 1)",
                     'waiver.py, stage S5, block "already probed on these bytes"', second.get("words", ""))
            # without --json it is ONE line (spec; the road prints the verdict's usual text)
            plain = run_script("probe_by_code.py", "--task", TASK, "--dispatch", DISPATCH, "--test",
                               f"{TEST_FILE_REL}::test_add", "--instance", "test_add",
                               cwd=root, env=env_for(root, stub, PROBE_STUB_LOG=str(logs / "twice.log")))
            check_eq("twice, no --json: exit 0 and one line (spec; PRODUCT QUESTION 1)",
                     (plain.returncode, len(plain.stdout.strip().splitlines())), (0, 1))
            check_in("twice, no --json: it says already_probed (spec; PRODUCT QUESTION 1)", "already_probed", plain.stdout)
            check_eq("twice: still one launch", launches("twice"), 1)
            # the non-JSON reader and the JSON reader see the same answer
            check_eq("twice: nothing launched or written after the printed answer either",
                     {k: v for k, v in snapshot(root).items() if k != aggregate}, {k: v for k, v in quiet.items() if k != aggregate})

        # AC1/AC2: a comment, or ANOTHER test edited, keeps the answer; the test's own code, or the module
        # skeleton, does not (D5: one test's fix never makes another test's proof stale)
        # t-2064 P4b: the walk skips a check by the sha256 of the WHOLE file it lives in (section 14), so a comment or another test's edit changes
        # that sha and the check runs again: the first two pins (a comment, another test edited) are the old repeat's (the instance's code,
        # D5) and stay red as PRODUCT QUESTION 3 of the report, unbent. An edit of the check itself, and a module-wide skip, run it: green,
        # counted as launches SINCE the previous call (the counts are no longer 1, 2, 3).
        with fresh() as root:
            proc, first = go(root, "edit", "test_add", "test_add")
            check_eq("edits: the first probe holds a receipt", (first.get("verdict"), bool(first.get("receipt"))),
                     ("intended_failure", True))
            test_file = root / TEST_FILE_REL
            body = test_file.read_bytes()
            test_file.write_bytes(body + b"\n# a comment at the end of the file\n")
            proc, got = go(root, "edit", "test_add", "test_add")
            check_eq("a comment: answered by the receipt (spec D5; PRODUCT QUESTION 3)", (got.get("verdict"), got.get("by")),
                     ("already_probed", "receipt"))
            check_eq("a comment: it holds by the code of the test (spec D5; PRODUCT QUESTION 3)", got.get("holds"), "instance_code")
            check_in("a comment: and the words say so (FR-41) (spec D5; PRODUCT QUESTION 3)", PL.code_unchanged_words(), got.get("words", ""))
            check_eq("a comment: no launch (spec D5; PRODUCT QUESTION 3)", launches("edit"), 1)
            test_file.write_bytes(body.replace(b"total = add(1, 1)", b"total = add(1, 1) + 0"))
            proc, got = go(root, "edit", "test_add", "test_add")
            check_eq("another test edited: answered, and it holds as the same test (spec D5; PRODUCT QUESTION 3)",
                     (got.get("verdict"), got.get("holds")), ("already_probed", "instance"))
            check_eq("another test edited: no comment-only words", PL.comment_only_words() in got.get("words", ""),
                     False)
            seen = launches("edit")
            test_file.write_bytes(body.replace(b'== 4, "sum must be 4"', b'== 5, "sum must be 4"'))
            proc, got = go(root, "edit", "test_add", "test_add")
            check_eq("an assert changed: the probe runs (its verdict is whatever the run says: the assert now "
                     "holds, so the inverted one never fires)", (got.get("verdict"), launches("edit") - seen),
                     ("no_failure", 1))
            seen = launches("edit")
            test_file.write_bytes(body + b"\npytestmark = []\n")
            proc, got = go(root, "edit", "test_add", "test_add")
            check_eq("pytestmark added: the probe runs (a module-wide skip is never kept)",
                     (got.get("verdict"), launches("edit") - seen), ("intended_failure", 1))

        # AC2: verdicts of the probe's own failure never block, and neither does a receipt-less intended failure
        with fresh() as root:
            proc, got = go(root, "notexec", "test_add", "test_add", PROBE_STUB_CRASH="1")
            check_eq("not_executed first", got.get("verdict"), "not_executed")
            proc, got = go(root, "notexec", "test_add", "test_add")
            check_eq("...does not block: the probe runs", (got.get("verdict"), launches("notexec")),
                     ("intended_failure", 2))
        with fresh() as root:
            # N3b: the judge no longer writes `wrong_location` (a throw before the check is `incomplete`, `cause: judgment`); the judged
            # survivor of the same shape is a pass of the dead assert, `no_failure`
            proc, got = go(root, "dead", "test_dead_assert", "test_dead_assert")
            check_eq("no_failure first", got.get("verdict"), "no_failure")
            proc, got = go(root, "dead", "test_dead_assert", "test_dead_assert")
            # t-2064 TR2-14 (F3): a survivor (`no_failure`) is carried by the walk, never answered `already_probed`: the repeat answers
            # `no_failure` again, with no `prior_verdict`, and the launches stay at the one of the first call
            check_eq("no_failure, then the same call on the same bytes and the same target: the survivor is carried, not answered (F3)",
                     (got.get("verdict"), got.get("prior_verdict"), launches("dead")),
                     ("no_failure", None, 1))
        with fresh() as root:
            write_json(task_of(root) / "work" / "automation-manifest.json", {"tests": [
                dict(next(t for t in manifest_of(root)["tests"] if t["instance_id"] == "test_add"),
                     trace_binding={"test_content_sha": "0" * 64})]})
            proc, got = go(root, "stale", "test_add", "test_add")
            check_eq("intended_failure with a stale trace_binding writes no receipt",
                     (got.get("verdict"), got.get("receipt")), ("intended_failure", None))
            proc, got = go(root, "stale", "test_add", "test_add")
            # t-2064 P4b: the check is PROVED (intended_failure on these bytes), so the repeat skips its run (launches stay 1) and answers
            # the aggregate; the receipt waits for the author's rebind (the a_rerun test pins that a complete walk then names one)
            check_eq("...and a repeat is not refused: the proved check is not run again and nothing is blocked (edge 16)",
                     (got.get("verdict"), got.get("receipt"), launches("stale")), ("intended_failure", None, 1))
        with fresh() as root:
            write_json(task_of(root) / "work" / "test-plan.json", {"rows": [{
                "id": "TS-1", "schema_version": 2, "coverage_obligations": [{"obligation_id": "OB-OTHER", "text": "x"}]}]})
            proc, got = go(root, "refused", "test_add", "test_add")
            check_eq("a publish refused by manifest_put leaves the receipt unpublished",
                     ((got.get("publish") or {}).get("published"), "sensitivity_proof" in row_of(root)), (False, False))
            proc, got = go(root, "refused", "test_add", "test_add")
            # t-2064 P4b: the proved check is not run again (launches stay 1); the call is not refused and answers the aggregate, and the
            # row is still unpublished (the manifest_put refusal stands: the plan names an obligation the row does not)
            check_eq("...and the repeat is not refused: the proved check is skipped, the publish is tried again",
                     (got.get("verdict"), launches("refused"), (got.get("publish") or {}).get("published")),
                     ("intended_failure", 1, False))

        # AC2: an oracle in a helper - the verdict was measured on other oracle bytes once the helper changed
        with fresh() as root:
            proc, got = go(root, "oracle", "test_via_helper", "test_via_helper")
            check_eq("oracle in a helper: recorded with the helper as the mutated file",
                     ((got.get("mutated_file") or {}).get("path"), got.get("verdict")),
                     ("tests/expectations.py", "intended_failure"))
            proc, got = go(root, "oracle", "test_via_helper", "test_via_helper")
            check_eq("the helper unchanged: the proved check is not run again", (got.get("verdict"), launches("oracle")),
                     ("intended_failure", 1))
            helper = root / "tests" / "expectations.py"
            helper.write_bytes(helper.read_bytes().replace(b'"sum must match"', b'"sum differs"'))
            proc, got = go(root, "oracle", "test_via_helper", "test_via_helper")
            check_eq("the helper (the oracle) changed: the probe runs", (got.get("verdict"), launches("oracle")),
                     ("intended_failure", 2))

        # AC2: a record nobody can read is absent, with a note
        with fresh() as root:
            # t-2064 P4b: the record that says a check is PROVED is the per-check record, so that is the one made unreadable (the old pin
            # corrupted the single record of a survivor, which is re-run anyway); an unreadable per-check record answers no repeat
            # (`_repeat_same_entries`, t-041 F2) and is not a proof on the walk (`_check_standing`, AR-28): the check runs again, and the
            # aggregate is rewritten readable
            go(root, "corrupt", "test_add", "test_add")
            checks_dir = task_of(root) / "work" / "probes" / "checks"
            for broken in checks_dir.glob("test_add--*.json"):
                broken.write_text("{not json", encoding="utf-8")
            proc, got = go(root, "corrupt", "test_add", "test_add")
            check_eq("a corrupt record: the check is not proved, so the probe runs again",
                     (got.get("verdict"), launches("corrupt")), ("intended_failure", 2))
            check_eq("...and the aggregate it leaves is readable", read_record(root, "test_add").get("verdict"), "intended_failure")

        # B-373 R10 / E23 + F3: a stored `incomplete` (the tool could not read the run) answers nothing, so the probe runs again; the walk
        # reads the PER-CHECK record, so that one is stamped too (a stored `incomplete` per-check record reruns; a survivor is carried);
        # only no_failure / wrong_location stand (a gap of the factory's is never a standing verdict on the test)
        with fresh() as root:
            go(root, "incompl", "test_dead_assert", "test_dead_assert")
            stamp_record(root, "test_dead_assert", verdict="incomplete")
            for one in (task_of(root) / "work" / "probes" / "checks").glob("test_dead_assert--*.json"):
                stored = json.loads(one.read_text(encoding="utf-8"))
                stored["verdict"] = "incomplete"
                write_json(one, stored)
            proc, got = go(root, "incompl", "test_dead_assert", "test_dead_assert")
            check_eq("an incomplete record does not answer a repeat: the probe runs",
                     (got.get("verdict"), launches("incompl")), ("no_failure", 2))

        # t-2064 P4b, THE GROUPS BELOW (levels and budget unavailable, a person's word, a product record, legacy records) pin the old repeat's
        # readers: `proof_level.already_probed` through `_repeat_check`, which the plain road no longer calls (the walk skips a check by its
        # per-check record, section 14, and never reads a person's word, a product record or a legacy aggregate). Their ANSWER pins stay
        # as they are: the answer is B3's `already_probed`; a `no_failure` is walked again on every call
        # (PRODUCT QUESTION 2). A pin of "the probe runs (no_failure, N)" that passes below passes ONLY because a survivor is re-run on
        # every call - not for the reason it names (the note it carries is the red pin next to it); the report lists them by name.
        # AC2: the vocabulary of levels, and the run budget, unavailable: the probe runs, with a note (in this
        # process: the file the two readers look at is a module setting)
        with fresh() as root:
            go(root, "unavail", "test_dead_assert", "test_dead_assert")
            saved_levels, saved_budget = PL.LEVELS_FILE, None
            import execution_request as ER
            os.environ["PROBE_RUN_SUITE"] = str(stub)
            os.environ["PROBE_STUB_LOG"] = str(logs / "unavail.log")
            try:
                PL.LEVELS_FILE = root / "no-such-levels.json"
                PL._reset()
                got = PBC.probe(TASK, DISPATCH, f"{TEST_FILE_REL}::test_dead_assert", "test_dead_assert", "invert")
                # t-2064 TR2-14 (F3): the survivor is carried, so the launches stay at the first call's one in every call below
                check_eq("LevelsUnavailable: the probe runs", (got.get("verdict"), launches("unavail")),
                         ("no_failure", 1))
                check_in("...with a note", "proof levels cannot be read", " ".join(got.get("notes") or []))
                PL.LEVELS_FILE = saved_levels
                PL._reset()
                saved_budget = ER.RUN_BUDGET_FILE
                ER.RUN_BUDGET_FILE = "no-such-run-budget.json"
                got = PBC.probe(TASK, DISPATCH, f"{TEST_FILE_REL}::test_dead_assert", "test_dead_assert", "invert")
                check_eq("an unreadable run-budget.json: the probe runs", (got.get("verdict"), launches("unavail")),
                         ("no_failure", 1))
                check_in("...with the budget's own note", "run-budget.json", " ".join(got.get("notes") or [])
                         .replace("no-such-run-budget.json", "run-budget.json"))
                ER.RUN_BUDGET_FILE = saved_budget
                got = PBC.probe(TASK, DISPATCH, f"{TEST_FILE_REL}::test_dead_assert", "test_dead_assert", "invert")
                check_eq("the budget back: the survivor is carried again (F3: no_failure, still one launch)",
                         (got.get("verdict"), launches("unavail")), ("no_failure", 1))
            finally:
                PL.LEVELS_FILE = saved_levels
                PL._reset()
                if saved_budget is not None:
                    ER.RUN_BUDGET_FILE = saved_budget
                os.environ.pop("PROBE_RUN_SUITE", None)
                os.environ.pop("PROBE_STUB_LOG", None)

        # A person's word passes ONE repeat: AT the record's time it is spent, one second after it passes, and
        # the repeat's own record (newer) spends it
        with fresh() as root:
            # t-2064 TR2-14 (B3/F3): the subject is a PROVED check (`test_add`): only a proved check is answered `already_probed`
            # (a survivor is carried, never answered), so the person's word has something to pass
            go(root, "word", "test_add", "test_add")
            stamp_record(root, "test_add", recorded_at="2026-09-01T00:00:00+00:00")
            give_word(root, "2026-09-01T00:00:00+00:00")
            proc, got = go(root, "word", "test_add", "test_add")
            check_eq("a word said AT the record's time is spent: answered", (got.get("verdict"), launches("word")),
                     ("already_probed", 1))
            give_word(root, "2026-09-01T00:00:01+00:00")
            proc, got = go(root, "word", "test_add", "test_add")
            check_eq("one second after: it passes, the probe runs", (got.get("verdict"), launches("word")),
                     ("intended_failure", 2))
            check_in("...and the note records the word", "probe it again, I asked", " ".join(got.get("notes") or []))
            proc, got = go(root, "word", "test_add", "test_add")
            check_eq("the third call: the repeat's own record spent the word, answered",
                     (got.get("verdict"), launches("word")), ("already_probed", 2))
            give_word(root, "2999-01-01T00:00:00+00:00", match="another block")
            proc, got = go(root, "word", "test_add", "test_add")
            check_eq("a word for another block passes nothing", got.get("verdict"), "already_probed")

        # AC2: the product level's record answers too - and it stops answering when the product file changed
        with fresh() as root:
            use_project(root)
            row = row_of(root, "test_dead_assert")
            now = PL.instance_identity(row, task_of(root), root)
            calc = root / "calc.py"
            product = {"schema_version": 1, "probe_tool": "red_sandbox.py", "instance_id": "test_dead_assert",
                       "verdict": "survived", "recorded_at": "2026-09-20T10:00:00+00:00",
                       "test_file_sha256": now["input_hash"], "test_code_sha": now["test_code_sha"],
                       "instance_identity": now["instance_identity"],
                       "mutated_files": [{"path": "calc.py", "sha256": PBC.sha256(calc.read_bytes()),
                                          "code_sha": PL.code_sha(calc.read_bytes(), "calc.py")}]}
            write_json(task_of(root) / "work" / "probes" / "product" / "test_dead_assert.json", product)
            proc, got = go(root, "product", "test_dead_assert", "test_dead_assert")
            check_eq("a product `survived` record on the same bytes answers the live probe",
                     (got.get("verdict"), got.get("by"), got.get("prior_verdict"), launches("product")),
                     ("already_probed", "product_record", "survived", 0))
            calc.write_bytes(calc.read_bytes().replace(b"a + b", b"b + a"))
            proc, got = go(root, "product", "test_dead_assert", "test_dead_assert")
            check_eq("...and the product file changed since: the probe runs", (got.get("verdict"), launches("product")),
                     ("no_failure", 1))
            calc.write_bytes(CALC.encode("utf-8"))

        # a record from before per-test binding: the raw file rule, or the file's code where it recorded one
        with fresh() as root:
            raw = PBC.sha256((root / TEST_FILE_REL).read_bytes())
            legacy = {"schema_version": 1, "probe_tool": "probe_by_code.py", "instance_id": "test_dead_assert",
                      "verdict": "no_failure", "recorded_at": "2026-09-20T10:00:00+00:00",
                      "test_file_sha256": raw, "instance_content_sha": "the-old-conftest-only-derivation",
                      "mutation_detail": {"line": 12}}
            write_json(task_of(root) / "work" / "probes" / "test_dead_assert.json", legacy)
            proc, got = go(root, "legacy", "test_dead_assert", "test_dead_assert")
            check_eq("a legacy record, raw bytes equal: answered", (got.get("verdict"), got.get("holds"), launches("legacy")),
                     ("already_probed", "raw", 0))
            test_file = root / TEST_FILE_REL
            test_file.write_bytes(test_file.read_bytes().replace(b"total > 100", b"total > 101"))
            proc, got = go(root, "legacy", "test_dead_assert", "test_dead_assert")
            check_eq("a legacy record, other bytes and no code sha: the probe runs",
                     (got.get("verdict"), launches("legacy")), ("no_failure", 1))
        with fresh() as root:
            body = (root / TEST_FILE_REL).read_bytes()
            raw = PBC.sha256(body)
            legacy = {"schema_version": 1, "probe_tool": "probe_by_code.py", "instance_id": "test_dead_assert",
                      "verdict": "no_failure", "recorded_at": "2026-09-20T10:00:00+00:00",
                      "test_file_sha256": raw, "test_code_sha": PL.code_sha(body, "test_calc.py"),
                      "mutation_detail": {"line": 12}}
            write_json(task_of(root) / "work" / "probes" / "test_dead_assert.json", legacy)
            (root / TEST_FILE_REL).write_bytes(body + b"\n# comment only\n")
            proc, got = go(root, "legacy2", "test_dead_assert", "test_dead_assert")
            check_eq("a legacy record that recorded test_code_sha holds over a comment (file_code)",
                     (got.get("verdict"), got.get("holds"), launches("legacy2")), ("already_probed", "file_code", 0))
        # a legacy record whose oracle lay OUTSIDE the test, with no mutated_file key: it cannot say which bytes
        # it measured, and never blocks
        with fresh() as root:
            body = (root / TEST_FILE_REL).read_bytes()
            legacy = {"schema_version": 1, "probe_tool": "probe_by_code.py", "instance_id": "test_via_helper",
                      "verdict": "no_failure", "recorded_at": "2026-09-20T10:00:00+00:00",
                      "test_file_sha256": PBC.sha256(body), "test_code_sha": PL.code_sha(body, "test_calc.py"),
                      "mutation_detail": {"line": 2, "file": "tests/expectations.py"}}
            write_json(task_of(root) / "work" / "probes" / "test_via_helper.json", legacy)
            proc, got = go(root, "outside", "test_via_helper", "test_via_helper")
            check_eq("a legacy record with an oracle outside the test and no mutated_file never blocks",
                     (got.get("verdict"), launches("outside")), ("intended_failure", 1))
    finally:
        cleanup(logs)


# --- HF3-6 part 6a: the probe of the code close of S6, with no dispatch open ----------------------------

def open_the_close(root: Path, **over) -> None:
    """The story's state AT the code close of S6: the critic's dispatch accepted, S0..S5 completed, S6 not started
    (the shape `s6_reprobed_close` meets after the runner and the critic are done). `over` replaces top-level keys."""
    path = task_of(root) / "state" / "controller.json"
    state = json.loads(path.read_text(encoding="utf-8"))
    state["dispatches"][DISPATCH]["status"] = "accepted"
    state["stages"] = {f"S{i}": {"status": "completed"} for i in range(6)}
    state["scope"] = list(state["dispatches"][DISPATCH]["scope"])
    state.update(over)
    write_json(path, state)


def run_close(root: Path, stub: Path, test: str, instance: str, **extra):
    proc = run_script("probe_by_code.py", "--task", TASK, "--s6-close", "--test", test, "--instance", instance,
                      "--json", cwd=root, env=env_for(root, stub, **extra))
    lines = [ln for ln in proc.stdout.splitlines() if ln.strip()]
    try:
        payload = json.loads("\n".join(lines)) if lines and lines[0].startswith("{") else {}
    except ValueError:
        payload = {}
    return proc, payload


def project_bytes(root: Path) -> dict:
    """{path: sha256} of every file of the project outside the story's artifacts: the author's files and the state."""
    found = {}
    for path in sorted(root.rglob("*")):
        if path.is_file():
            found[path.relative_to(root).as_posix()] = PBC.sha256(path.read_bytes())
    return found


def the_s6_close_context(stub: Path) -> None:
    node, iid = f"{TEST_FILE_REL}::test_add", "test_add"
    # A-K8: while a dispatch is running the context is refused BEFORE anything is read or mutated (position (g))
    with fresh() as root:
        before, story = project_bytes(root), snapshot(root)
        proc, got = run_close(root, stub, node, iid)
        check_eq("A-K8 running dispatch: exit 2, one JSON line, status refused", (proc.returncode, got.get("status")),
                 (2, "refused"))
        check_in("A-K8 the refusal names the open dispatch and its door", f"`--dispatch {DISPATCH}`",
                 got.get("error", ""))
        check_eq("A-K8 the test file, the oracle and the whole project are byte for byte as they were",
                 project_bytes(root), before)
        check("A-K8 no byte copy folder was made", not PBC.copy_dir(root).exists(), str(PBC.copy_dir(root)))
        check("A-K8 no request, no job, no record", not (task_of(root) / "work" / "probe-requests").exists()
              and not (task_of(root) / "work" / "probes" / f"{iid}.json").exists())
        check_eq("A-K8 the story's probe artifacts are the snapshot's", snapshot(root), story)
        # in-process: the refusal comes before the dead probes are settled, a lock is taken or the test is read
        calls = []
        saved = (PBC.scan_copies, PBC.claim_key, PBC._test_path)
        PBC.scan_copies = lambda *a, **k: calls.append("scan_copies")
        PBC.claim_key = lambda *a, **k: calls.append("claim_key")
        PBC._test_path = lambda *a, **k: calls.append("_test_path")
        try:
            try:
                PBC.probe(TASK, "", node, iid, "invert", s6_close=True)
                raised = False
            except PBC.Refusal:
                raised = True
        finally:
            PBC.scan_copies, PBC.claim_key, PBC._test_path = saved
        check_eq("A-K8 position: refused before _test_path, scan_copies and any lock", (raised, calls), (True, []))
    # A-K9: in the close context the probe runs under the context's id and answers as under a dispatch
    with fresh() as root:
        open_the_close(root)
        authored = (root / TEST_FILE_REL).read_bytes()
        proc, got = run_close(root, stub, node, iid)
        check_eq("A-K9 the close context: exit 0, the verdict of a probe under a dispatch, and the same places (F-4)",
                 (proc.returncode, got.get("verdict"), got.get("expected_location"), got.get("actual_location")),
                 (0, "intended_failure", f"{TEST_FILE_REL}:6", f"{TEST_FILE_REL}:6"))
        check_eq("A-K9 the record names the context", read_record(root, iid).get("dispatch_id"), "S6-close-r1")
        check_eq("A-K9 the author's test is back as it was", (root / TEST_FILE_REL).read_bytes(), authored)
        check_eq("A-K9 the request is the context's", json.loads(
            (task_of(root) / "work" / "probe-requests" / f"probe-walk-{iid}-1.json").read_text(encoding="utf-8")   # a walk's request, per run
        ).get("dispatch_id"), "S6-close-r1")
    with fresh() as root:
        proc, under = run(root, stub, node, iid)
        check_eq("A-K9 the same fixture under --dispatch gives the same verdict and places",
                 (under.get("verdict"), under.get("expected_location"), under.get("actual_location")),
                 ("intended_failure", f"{TEST_FILE_REL}:6", f"{TEST_FILE_REL}:6"))
    # the repeat over the same bytes is answered, and a person's word for it is looked up under S6
    # t-2064 P4b: the three repeat/stage groups below (this one and the two spies) pin `PL.already_probed(stage=...)`, which the walk road
    # does not call at all, and a survivor (`no_failure`) is walked again: they stay red and unbent - PRODUCT QUESTION 1 (the answer and
    # the person's-word door under S5 and S6) and 2 (a survivor repeat), see the report.
    with fresh() as root:
        open_the_close(root)
        # t-2064 TR2-14 (B3/F3): the subject is a PROVED check - a survivor is carried, never answered `already_probed`
        proc, first = run_close(root, stub, f"{TEST_FILE_REL}::test_add", "test_add")
        check_eq("A-K9 repeat: the first probe runs", (proc.returncode, first.get("verdict")), (0, "intended_failure"))
        proc, second = run_close(root, stub, f"{TEST_FILE_REL}::test_add", "test_add")
        check_eq("A-K9 repeat: answered, not probed", (proc.returncode, second.get("verdict")), (0, "already_probed"))
        check_in("A-K9 repeat: the person's word is asked for under stage S6", "waiver.py, stage S6,",
                 second.get("words", ""))
    with fresh() as root:
        open_the_close(root)
        seen = {}
        saved = PL.already_probed

        def spy(*args, **kwargs):
            seen.update(kwargs)
            return {"probed": False, "notes": []}
        PL.already_probed = spy
        try:
            os.environ["PROBE_RUN_SUITE"] = str(stub)
            PBC.probe(TASK, "", node, iid, "invert", s6_close=True)
        finally:
            PL.already_probed = saved
            os.environ.pop("PROBE_RUN_SUITE", None)
        check_eq("A-K9 already_probed is called with stage='S6' in the close context", seen.get("stage"), "S6")
    with fresh() as root:
        seen = {}
        saved = PL.already_probed

        def spy_plain(*args, **kwargs):
            seen.update(kwargs)
            return {"probed": False, "notes": []}
        PL.already_probed = spy_plain
        model_entries(root, stub, node, iid)
        try:
            os.environ["PROBE_RUN_SUITE"] = str(stub)
            PBC.probe(TASK, DISPATCH, node, iid, "invert")
        finally:
            PL.already_probed = saved
            os.environ.pop("PROBE_RUN_SUITE", None)
        check_eq("A-K9 under a dispatch the stage stays empty (as before)", seen.get("stage"), "")
    # the context is refused when S6 is closed, or the case is not the story's: nothing changes
    for label, over, needle in (
            ("S6 completed", {"stages": {**{f"S{i}": {"status": "completed"} for i in range(6)},
                                         "S6": {"status": "completed", "receipt_id": "S6-code-only-1"}}},
             "S6 is already closed (S6-code-only-1)"),
            ("S5 not completed", {"stages": {**{f"S{i}": {"status": "completed"} for i in range(5)},
                                             "S5": {"status": "running"}}}, "S6 has not started: S5 is running"),
            ("a case outside the scope", {"scope": ["TC-101"]}, "TC-100 is not in the story's approved scope"),
            ("an empty scope", {"scope": []}, "is not in the story's approved scope")):
        with fresh() as root:
            open_the_close(root)
            open_the_close(root, **over)
            before = project_bytes(root)
            proc, got = run_close(root, stub, node, iid)
            check_eq(f"{label}: exit 2, refused, the project is byte for byte as it was",
                     (proc.returncode, got.get("status"), project_bytes(root)), (2, "refused", before))
            check_in(f"{label}: the refusal says why", needle, got.get("error", ""))


# --- RH1-8 B3: the critic path asks for the open dispatch before its first byte ---------------------------

def run_dispatch(root: Path, stub: Path, test: str, instance: str, dispatch: str, task: str = TASK):
    # the model file is world, not the probe's work: a test that compares the project's bytes before and after the call writes it
    # first (`model_entries`, same bytes), so the comparison still covers everything the PROBE could write
    model_entries(root, stub, test, instance, dispatch, task)
    proc = run_script("probe_by_code.py", "--task", task, "--dispatch", dispatch, "--test", test,
                      "--instance", instance, "--mutation", "invert", "--json", cwd=root, env=env_for(root, stub))
    lines = [ln for ln in proc.stdout.splitlines() if ln.strip()]
    try:
        payload = json.loads("\n".join(lines)) if lines and lines[0].startswith("{") else {}
    except ValueError:
        payload = {}
    return proc, payload


def set_dispatch_state(root: Path, mutate) -> None:
    path = task_of(root) / "state" / "controller.json"
    state = json.loads(path.read_text(encoding="utf-8"))
    mutate(state)
    write_json(path, state)


def rh1_8_dispatch_asked_first(stub: Path) -> None:
    node, iid = f"{TEST_FILE_REL}::test_add", "test_add"

    def close_it(state):
        state["dispatches"][DISPATCH]["status"] = "accepted"

    # P1, P1b, P1-text: nothing open -> refused before any byte
    with fresh() as root:
        set_dispatch_state(root, close_it)
        model_entries(root, stub, node, iid)
        before, story = project_bytes(root), snapshot(root)
        proc, got = run_dispatch(root, stub, node, iid, DISPATCH)
        check_eq("RH1-8 P1 no open dispatch: exit 2, status refused", (proc.returncode, got.get("status")),
                 (2, "refused"))
        check_eq("RH1-8 P1 the project is byte for byte as it was", project_bytes(root), before)
        check("RH1-8 P1 no copy dir, no request, no record", not PBC.copy_dir(root).exists()
              and not (task_of(root) / "work" / "probe-requests").exists()
              and not (task_of(root) / "work" / "probes" / f"{iid}.json").exists()
              and snapshot(root) == story)
        error = got.get("error", "")
        check("RH1-8 P1-text names cause: tooling, tooling_findings and unverified, and no reopen promise",
              all(s in error for s in ("cause: tooling", "tooling_findings", "unverified", "Nothing was read or changed",
                                       f"no open dispatch {DISPATCH} in story {TASK}"))
              and "reopen" not in error, error)
        check("RH1-8 F5 the Detail keeps the reason and names no door of the --mine caller (FR-2)",
              "Detail: no active dispatch in story" in error and not any(
                  s in error for s in ("controller.py", "--operation", "--task", "--label", "orchestrator opens")), error)
        calls = []
        saved = (PBC.scan_copies, PBC.claim_key, PBC._test_path)
        PBC.scan_copies = lambda *a, **k: calls.append("scan_copies")
        PBC.claim_key = lambda *a, **k: calls.append("claim_key")
        PBC._test_path = lambda *a, **k: calls.append("_test_path")
        prior = os.environ.get("CLAUDE_PROJECT_DIR")
        os.environ["CLAUDE_PROJECT_DIR"] = str(root)
        try:
            try:
                PBC.probe(TASK, DISPATCH, node, iid, "invert")
                raised = False
            except PBC.Refusal:
                raised = True
        finally:
            PBC.scan_copies, PBC.claim_key, PBC._test_path = saved
            if prior is None:
                os.environ.pop("CLAUDE_PROJECT_DIR", None)
            else:
                os.environ["CLAUDE_PROJECT_DIR"] = prior
        check_eq("RH1-8 P1b position: refused before _test_path, scan_copies and any lock", (raised, calls),
                 (True, []))
    # P1c, P14: a stored intended_failure record, then the dispatch closes
    with fresh() as root:
        proc, first = run_dispatch(root, stub, node, iid, DISPATCH)
        check_eq("RH1-8 P1c the first probe runs", (proc.returncode, first.get("verdict")), (0, "intended_failure"))
        record_path = task_of(root) / "work" / "probes" / f"{iid}.json"
        stored = record_path.read_bytes()
        set_dispatch_state(root, close_it)
        model_entries(root, stub, node, iid)
        before = project_bytes(root)
        proc, got = run_dispatch(root, stub, node, iid, DISPATCH)
        check_eq("RH1-8 P14 an already probed instance with no open dispatch -> refused, not already_probed",
                 (proc.returncode, got.get("status"), got.get("verdict")), (2, "refused", None))
        check_eq("RH1-8 P1c a stored intended_failure record is untouched",
                 (record_path.read_bytes(), project_bytes(root)), (stored, before))
    # P2: a parent_retry ancestor id still probes and keeps the passed id
    with fresh() as root:
        def resumed(state):
            state["dispatches"][DISPATCH]["parent_retry"] = "S5-qa-code-critic-0"
            state["dispatches"]["S5-qa-code-critic-0"] = {"id": "S5-qa-code-critic-0", "stage": "S5",
                                                          "role": "qa-code-critic", "status": "blocked"}
        set_dispatch_state(root, resumed)
        proc, got = run_dispatch(root, stub, node, iid, "S5-qa-code-critic-0")
        request = json.loads((task_of(root) / "work" / "probe-requests" / f"probe-walk-{iid}-1.json").read_text(
            encoding="utf-8"))   # a walk's request, per run
        check_eq("RH1-8 P2 a parent_retry ancestor id still probes, and the idempotency_key starts with the passed id",
                 (proc.returncode, got.get("verdict"),
                  str(request.get("idempotency_key", "")).startswith("S5-qa-code-critic-0:")),
                 (0, "intended_failure", True))
    # P3: two open; the case narrows
    with fresh() as root:
        def two_open(state):
            state["dispatches"]["S5-qa-code-critic-2"] = {"id": "S5-qa-code-critic-2", "stage": "S5",
                                                          "role": "qa-code-critic", "status": "running",
                                                          "scope": ["TC-999"], "budget": {"requests": 50}}
        set_dispatch_state(root, two_open)
        model_entries(root, stub, node, iid)
        os.environ["PROBE_RUN_SUITE"] = str(stub)
        try:
            # the model file is read by the PASSED dispatch id only (`_models_standing`: `if ctx.dispatch and file.is_file()`, P4b); an
            # empty id passes the context check by narrowing but finds no model, so the call names the open dispatch whose scope holds the case
            got = PBC.probe(TASK, DISPATCH, node, iid, "invert")
        finally:
            os.environ.pop("PROBE_RUN_SUITE", None)
        check_eq("RH1-8 P3 two open, the case narrows: probes", got.get("verdict"), "intended_failure")
    with fresh() as root:
        def two_wide(state):
            state["dispatches"]["S5-qa-code-critic-2"] = dict(state["dispatches"][DISPATCH],
                                                              id="S5-qa-code-critic-2")
        set_dispatch_state(root, two_wide)
        before = project_bytes(root)
        try:
            PBC.probe(TASK, "", node, iid, "invert")
            error = ""
        except PBC.Refusal as exc:
            error = str(exc)
        check_eq("RH1-8 P3 two open, the case does not narrow: refused early",
                 (bool(error), project_bytes(root)), (True, before))
        check_in("RH1-8 P3 the several-dispatches wording", f"several dispatches are open in story {TASK}", error)
        check("RH1-8 F5 and the several-dispatches Detail drops the --dispatch/--task door", "say which one" not in error
              and "--dispatch" not in error and "--task" not in error, error)
    # P4: unreadable controller.json
    for label, text in (("garbage", "{not json"), ("array", "[]")):
        with fresh() as root:
            (task_of(root) / "state" / "controller.json").write_text(text, encoding="utf-8")
            model_entries(root, stub, node, iid)
            before = project_bytes(root)
            proc, got = run_dispatch(root, stub, node, iid, DISPATCH)
            check_eq(f"RH1-8 P4 unreadable controller.json ({label}) -> refused before any byte",
                     (proc.returncode, got.get("status"), project_bytes(root)), (2, "refused", before))
    # P5: the dispatch belongs to another story
    with fresh() as root:
        set_dispatch_state(root, close_it)
        write_json(root / "qa-factory" / "artifacts" / "OTHER-1" / "state" / "controller.json", {
            "schema_version": "2", "revision": "1", "dispatches": {"S5-qa-code-critic-9": {
                "id": "S5-qa-code-critic-9", "stage": "S5", "role": "qa-code-critic", "status": "running",
                "scope": ["TC-100"], "budget": {"requests": 50}}}})
        model_entries(root, stub, node, iid, "S5-qa-code-critic-9")
        before = project_bytes(root)
        proc, got = run_dispatch(root, stub, node, iid, "S5-qa-code-critic-9")
        check_eq("RH1-8 P5 a dispatch of another story -> refused",
                 (proc.returncode, got.get("status"), project_bytes(root)), (2, "refused", before))


def records_flow() -> None:
    stub_dir = temp_dir("qa-probe-stub-")
    stub = stub_dir / "fake_run_suite.py"
    stub.write_text(FAKE_RUN_SUITE, encoding="utf-8")
    try:
        the_record_and_the_answer_are_pinned(stub)
        the_repeat_is_answered(stub)
        the_s6_close_context(stub)
        rh1_8_dispatch_asked_first(stub)
    finally:
        cleanup(stub_dir)


def main() -> None:
    records_flow()
    finish("test_probe_by_code_records")


# split: runner piece 1
if __name__ == "__main__":
    main()
