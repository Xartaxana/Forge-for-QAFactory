#!/usr/bin/env python3
"""An obligation id is the plan's, and an unbound obligation is named while the window is open.

Every shape here is TP2-2553's own. The plan spelled `TS-1-O1`; every fragment the
automator wrote spelled `OB-1`. `coverage_projection` joins by exact equality, so twelve green
instances produced `unique_instances: 0` and nine coverage gaps — read by everyone downstream
as missing product coverage. Window 2 then spent two repair rounds on bindings for `OB-6..OB-9`
that had never existed, and nothing said so until delivery.

So: `manifest_put.py` refuses a spelling the plan does not name (and a person's word passes
it), `s5_precheck.py` names an unbound obligation of the dispatch scope before the handoff,
and `migrate_artifacts.py --if-older` renames the `OB-n` a 0.7.9 story already wrote.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from harness import (check, check_eq, check_in, check_not_in, cleanup, finish,  # noqa: E402
                     run_script, temp_project)

import coverage_contract as CC  # noqa: E402
from event_store import content_hash  # noqa: E402
import manifest_put as M  # noqa: E402
import s5_precheck as P  # noqa: E402

TICKET = "TP2-2553"

# Three obligations over two plan rows — the smallest shape that tells a positional rename
# (OB-2 -> TS-1-O2) apart from a per-row one.
PLAN_ROWS = [
    {"id": "TS-1", "schema_version": 2, "coverage_obligations": [
        {"obligation_id": "TS-1-O1", "decision": "automate", "execution_scope": "current_task"},
        {"obligation_id": "TS-1-O2", "decision": "automate", "execution_scope": "current_task"}]},
    {"id": "TS-2", "schema_version": 2, "coverage_obligations": [
        {"obligation_id": "TS-2-O1", "decision": "automate", "execution_scope": "current_task"}]},
]

CASE_MD = """---
id: {case}
status: Draft
---
Plan row: {row}

## Given
A request.

## When
Call it.

## Then
1. The body carries `status_ok`.
"""


def make_story(rows=PLAN_ROWS, legacy_plan=False):
    """A project with one story, its plan and two cases (TC-005 on TS-1, TC-006 on TS-2)."""
    root = temp_project("qa-obligation-join-")
    task = root / "qa-factory" / "artifacts" / TICKET
    (task / "work" / "test-cases").mkdir(parents=True)
    plan = [{"id": "TS-1", "schema_version": 1}] if legacy_plan else rows
    (task / "work" / "test-plan.json").write_text(json.dumps({"rows": plan}), encoding="utf-8")
    for case, row in (("TC-005", "TS-1"), ("TC-006", "TS-2")):
        (task / "work" / "test-cases" / f"{case}.md").write_text(
            CASE_MD.format(case=case, row=row), encoding="utf-8")
    return root, task


def put(root, fragment):
    path = root / "fragment.json"
    path.write_text(json.dumps(fragment), encoding="utf-8")
    return run_script("manifest_put.py", "--task", TICKET, "--fragment", str(path), cwd=root,
                      env={**dict(__import__("os").environ), "CLAUDE_PROJECT_DIR": str(root)})


def _word_line(iid="test_five", fields=("obligation_refs",)) -> str:
    """One line of `state/passed-by-person.jsonl` for the `manifest:-:row-fields-missing` finding, as the controller writes it."""
    return json.dumps({"ts": "2026-11-13T10:00:00+00:00", "stage": "S5", "dispatch": "d1", "block": "manifest:-:row-fields-missing",
                       "finding_id": "manifest:-:row-fields-missing", "check": "manifest", "tag": "row-fields-missing",
                       "subjects": [{"instance_id": iid, "fields": list(fields)}], "decision": "go on",
                       "word_at": "2026-11-13T09:59:00Z", "by": "human"}) + "\n"


def fv1_30b_n2_refs_words() -> None:
    """FV1-30b R5 (c1)-(c7) on CONSTRUCTED rows (S1 Q5, not measured: no real TP1-13797 manifest was read; these fixtures stand in):
    the words are only ADDED to an obligation whose binding names an instance the record passed for `obligation_refs` and whose
    row still has bad refs; `verified`, `person_debt`, `execution_state`, `sensitivity`, `code_validity` never move."""
    stable = ("verified", "person_debt", "execution_state", "sensitivity", "code_validity", "design_assessment", "instance_ids")
    plan_hash = content_hash(PLAN_ROWS[0]["coverage_obligations"][0])

    def manifest(refs="absent", bindings=None, extra_tests=()):
        row = {"case": "TC-005", "file": "tests/t.py", "instance_id": "test_five", "covers": ["TC-005"], "status": "green"}
        if refs != "absent":
            row["obligation_refs"] = refs
        binding = [{"obligation_id": "TS-1-O1", "instance_ids": ["test_five"], "obligation_hash": plan_hash}]
        return {"tests": [row, *extra_tests], "obligation_bindings": binding if bindings is None else bindings}

    def project(task, mf, oid="TS-1-O1"):
        return next(o for o in CC.coverage_projection(task, report={}, manifest=mf)["obligations"] if o["obligation_id"] == oid)

    root, task = make_story()
    try:
        record = task / "state" / "passed-by-person.jsonl"
        (task / "state").mkdir(exist_ok=True)
        base = project(task, manifest())
        check("R5 (c4) control: no record -> no words, `word_passed` absent, not verified",
              "word_passed" not in base and "passed by the person's word" not in base["gap"] and base["verified"] is False, str(base))
        record.write_text(_word_line(), encoding="utf-8")
        words = "obligation_refs of test_five not established - passed by the person's word (human, 2026-11-13T10:00:00+00:00)"
        for label, refs in (("c1: refs absent", "absent"), ("c2: refs []", []), ("c1: refs not a list", "TS-1-O1"),
                            ("c1: refs unknown to the plan", [{"obligation_id": "TS-9-O9", "obligation_hash": "x"}]),
                            ("c1: refs stale", [{"obligation_id": "TS-1-O1", "obligation_hash": "stale"}])):
            item = project(task, manifest(refs))
            check(f"R5 ({label}) -> not verified, `word_passed`, the gap ends with the person's word after the older gap",
                  item["verified"] is False and item.get("word_passed") is True and item["gap"] == base["gap"] + "; " + words, str(item))
            check_eq(f"R5 ({label}) -> verified, person_debt, execution, sensitivity, validity are untouched",
                     {k: item[k] for k in stable}, {k: base[k] for k in stable})
        good = project(task, manifest([{"obligation_id": "TS-1-O1", "obligation_hash": plan_hash}]))
        check("R5 (c3): refs repaired (valid against the plan) -> no words, no `word_passed`",
              "word_passed" not in good and "passed by the person's word" not in good["gap"], str(good))
        nobinding = project(task, manifest(bindings=[]))
        check("R5 (c6)/F16: no binding -> no `word_passed`, no words", "word_passed" not in nobinding
              and "passed by the person's word" not in nobinding["gap"], str(nobinding))
        two = project(task, manifest(bindings=[{"obligation_id": "TS-1-O1", "instance_ids": ["test_five"], "obligation_hash": plan_hash},
                                               {"obligation_id": "TS-1-O1", "instance_ids": ["test_five"], "obligation_hash": plan_hash}]))
        check("R5 (c6)/F16: two bindings of one obligation -> no words", "word_passed" not in two, str(two))
        other = {"case": "TC-005", "file": "tests/t.py", "instance_id": "test_six", "covers": ["TC-005"], "status": "green"}
        sibling = project(task, manifest(bindings=[
            {"obligation_id": "TS-1-O1", "instance_ids": ["test_five"], "obligation_hash": plan_hash},
            {"obligation_id": "TS-1-O2", "instance_ids": ["test_six"]}], extra_tests=[other]), "TS-1-O2")
        check("R5 (c7): a second obligation bound to another, unnamed instance -> today's item, no words",
              "word_passed" not in sibling and "passed by the person's word" not in sibling["gap"], str(sibling))
        named = project(task, manifest(bindings=[
            {"obligation_id": "TS-1-O1", "instance_ids": ["test_five"], "obligation_hash": plan_hash},
            {"obligation_id": "TS-1-O2", "instance_ids": ["test_six"]}], extra_tests=[other]))
        check("R5 (c7): ... while the named one still carries them", named.get("word_passed") is True, str(named))
        # a record for another field, or one the table does not let a word pass: no words
        record.write_text(_word_line(fields=("assertion_id",)), encoding="utf-8")
        check("R5: a pass naming another field names no `obligation_refs`", "word_passed" not in project(task, manifest()))
        record.write_text(_word_line(fields=("change_disposition",)), encoding="utf-8")
        check("R5/E20: a pass naming only a field the table never passes -> no words", "word_passed" not in project(task, manifest()))
        # c5: the record cannot be read -> today's item
        record.unlink()
        record.mkdir()
        unreadable = project(task, manifest())
        check_eq("R5 (c5): record unreadable -> today's item, byte for byte", unreadable, base)
    finally:
        cleanup(root)


def main() -> None:
    # --- 1. the refusal, and the one word that passes it ------------------------------------
    root, task = make_story()
    try:
        legacy_fragment = {"tests": [{"case": "TC-005", "file": "tests/t.py",
                                      "instance_id": "test_ok", "covers": ["TC-005"]}],
                           "obligation_bindings": [{"obligation_id": "OB-1",
                                                    "instance_ids": ["test_ok"]},
                                                   {"obligation_id": "OB-2",
                                                    "instance_ids": ["test_ok"]}]}
        result = put(root, legacy_fragment)
        check_eq("a fragment spelling OB-n against a schema-2 plan is refused",
                 result.returncode, M.EXIT_BAD_FRAGMENT)
        check_in("the refusal names the ids it refused", "OB-1, OB-2", result.stderr)
        check_in("and the ids the plan does name",
                 "the plan names TS-1-O1, TS-1-O2, TS-2-O1", result.stderr)
        check_in("and where they are written", "work/test-plan.json", result.stderr)
        check_in("and the word that passes it", 'waiver.py --task <TICKET> --stage S5 '
                 '--block "obligation-id"', result.stderr)
        check_not_in("nothing was committed", "revision", result.stdout)

        # A person's recorded decision passes any block in this factory — read here, at the
        # source, the way s5_precheck.passed_by_word reads it.
        (task / "pipeline.json").write_text(json.dumps({"stage_overrides": [
            {"stage": "S5", "match": "obligation-id", "decision": "keep the ids as they are, "
             "this story predates the plan rewrite", "at": "2026-09-23"}]}), encoding="utf-8")
        passed = put(root, legacy_fragment)
        check_eq("a person's word passes the refusal", passed.returncode, 0)
        check_in("and the fragment lands", "automation-manifest.json: revision", passed.stdout)
    finally:
        cleanup(root)

    # --- 2. a legacy plan names no obligation and refuses none -------------------------------
    root, task = make_story(legacy_plan=True)
    try:
        result = put(root, {"obligation_bindings": [{"obligation_id": "OB-1",
                                                     "instance_ids": ["test_ok"]}]})
        check_eq("a plan with no schema-2 obligations refuses nothing", result.returncode, 0)
    finally:
        cleanup(root)

    # --- 3. s5_precheck names the unbound obligation of the scope ----------------------------
    root, task = make_story()
    try:
        manifest = {"tests": [
            {"case": "TC-005", "file": "tests/t.py", "instance_id": "test_five",
             "covers": ["TC-005"], "status": "green"},
            {"case": "TC-006", "file": "tests/t.py", "instance_id": "test_six",
             "covers": ["TC-006"], "status": "green"}],
            "obligation_bindings": [{"obligation_id": "TS-1-O1", "instance_ids": ["test_five"]},
                                    {"obligation_id": "TS-1-O2", "instance_ids": ["test_five"]}]}
        findings: list = []
        P.check_obligations(task, manifest, ["TC-005", "TC-006"], {}, set(), findings)
        check_eq("one bound and one unbound obligation is exactly one finding",
                 len(findings), 1)
        if findings:
            check_in("the finding names the unbound obligation", "TS-2-O1", findings[0]["message"])
            check_in("and the case it belongs to", "TC-006", findings[0]["message"])
            check_eq("and it is a repair, not a question", findings[0]["level"], "repair")
            check_in("its fix names the writer", "manifest_put.py", findings[0]["fix"])
            # one `--block "obligation-id"` covers this check and manifest_put both.
            check_in("and its id carries the block word", "obligation-id", findings[0]["id"])

        # a binding the plan does not know is the same finding, with the allowed ids named.
        stray = dict(manifest, obligation_bindings=[{"obligation_id": "OB-1",
                                                     "instance_ids": ["test_five"]}])
        findings = []
        P.check_obligations(task, stray, ["TC-005", "TC-006"], {}, set(), findings)
        check_eq("an unknown spelling leaves every obligation of the scope unbound",
                 len(findings), 3)
        check_in("and the finding names what the plan does allow",
                 "it names TS-1-O1, TS-1-O2, TS-2-O1", findings[0]["message"])

        # what is not owed: a handed case, and a manual obligation the runner discharges.
        findings = []
        P.check_obligations(task, manifest, ["TC-005", "TC-006"], {}, {"TC-006"}, findings)
        check_eq("a case handed to the person owes no binding", findings, [])
        manual_root, manual_task = make_story(rows=[
            PLAN_ROWS[0],
            {"id": "TS-2", "schema_version": 2, "coverage_obligations": [
                {"obligation_id": "TS-2-O1", "decision": "manual-human",
                 "execution_scope": "current_task"}]}])
        try:
            findings = []
            P.check_obligations(manual_task, manifest, ["TC-005", "TC-006"], {}, set(), findings)
            check_eq("a manual-* obligation is not an automated binding's job", findings, [])
        finally:
            cleanup(manual_root)

        # legacy plan: nothing to join, nothing to ask.
        legacy_root, legacy_task = make_story(legacy_plan=True)
        try:
            findings = []
            P.check_obligations(legacy_task, manifest, ["TC-005"], {}, set(), findings)
            check_eq("a legacy plan produces no finding", findings, [])
        finally:
            cleanup(legacy_root)
    finally:
        cleanup(root)

    # --- 4. the migration renames OB-n by position, and never guesses ------------------------
    root, task = make_story()
    try:
        seed = {"tests": [
            {"case": "TC-005", "file": "tests/t.py", "instance_id": "test_five",
             "covers": ["TC-005"], "status": "green",
             "obligation_refs": [{"obligation_id": "OB-1", "obligation_hash": "h1"}],
             "obligation_ids": ["OB-1"]},
            {"case": "TC-006", "file": "tests/t.py", "instance_id": "test_six",
             "covers": ["TC-006"], "status": "green"}],
            "obligation_bindings": [
                {"obligation_id": "OB-1", "instance_ids": ["test_five"], "sensitivity": "proven",
                 "obligation_hash": "hb"},
                {"obligation_id": "OB-2", "instance_ids": ["test_five"]},
                {"obligation_id": "OB-3", "instance_ids": ["test_six"]},
                {"obligation_id": "OB-4", "instance_ids": ["test_six"]}]}
        # seeded the way 0.7.9 wrote it: straight into the artifact, before the refusal existed.
        (task / "work" / "automation-manifest.json").write_text(json.dumps(seed), encoding="utf-8")
        (task / "state").mkdir(exist_ok=True)

        import migrate_artifacts as MA
        # the real entry point: a story resumed on a newer plugin, exactly as a resume runs it.
        proc = run_script("migrate_artifacts.py", "--task-root", str(task), "--if-older",
                          cwd=root)
        check("--if-older runs to the end", proc.returncode == 0,
              f"exit {proc.returncode}; stderr: {proc.stderr[-800:]}; stdout: {proc.stdout[-400:]}")
        # the journal writes its own OK line first; the report is the last line. A last line that is not
        # JSON is one FAIL line with the stdout tail (B-320), never a traceback that hides the other checks.
        try:
            report = json.loads(proc.stdout.strip().splitlines()[-1])
        except (ValueError, IndexError):
            check("the last stdout line is the JSON report", False,
                  f"stdout tail: {proc.stdout[-400:]!r}; stderr tail: {proc.stderr[-400:]!r}")
            report = None
        if report is not None:
            left = json.dumps(report.get("left"))
            check_in("and says what it renamed",
                     "obligation_bindings[] renamed to the plan's ids", json.dumps(report["changed"]))
            migrated = json.loads((task / "work" / "automation-manifest.json").read_text(encoding="utf-8"))
            bound = sorted(b["obligation_id"] for b in migrated.get("obligation_bindings") or [])
            check("OB-1..OB-3 are renamed to the ids the plan names, OB-4 stays",
                  bound == ["OB-4", "TS-1-O1", "TS-1-O2", "TS-2-O1"], f"got {bound!r}; left: {left}")
            retracted = sorted(migrated.get("retracted_obligations") or [])
            check("the old spellings are retracted, not left beside the new ones",
                  retracted == ["OB-1", "OB-2", "OB-3"], f"got {retracted!r}; left: {left}")
            check("an OB-n past the plan's count is reported, never guessed", "OB-4" in left,
                  f"left: {left}")
            check("with the reason", "no obligation at that position in the plan (3 named)" in left,
                  f"left: {left}")
            check_eq("the renamed binding keeps its own fields",
                     next(b for b in migrated["obligation_bindings"]
                          if b["obligation_id"] == "TS-1-O1").get("sensitivity"), "proven")
            five = next(t for t in migrated["tests"] if t.get("instance_id") == "test_five")
            check_eq("the instance re-cites the same obligation by the plan's id",
                     five.get("obligation_ids"), ["TS-1-O1"])
            # FV1-19 (D4, row o): a hash read from a stored row is never forwarded; the stamp writes the plan's hash of the NEW id.
            plan_hash = content_hash(PLAN_ROWS[0]["coverage_obligations"][0])
            check_eq("and so do its obligation_refs, the hash is the plan's (the stored h1 was not forwarded, nor refused)",
                     five.get("obligation_refs"), [{"obligation_id": "TS-1-O1", "obligation_hash": plan_hash}])
            check_eq("the row's own hash is the hash of the stamped refs",
                     five.get("obligation_hash"), content_hash(five.get("obligation_refs")))
            check_eq("the renamed binding carries the plan's hash of its new id (the seed's `hb` is gone)",
                     next(b for b in migrated["obligation_bindings"] if b["obligation_id"] == "TS-1-O1").get("obligation_hash"), plan_hash)
            again_run = run_script("migrate_artifacts.py", "--task-root", str(task), "--if-older", cwd=root)
            check_eq("--if-older exits 0 again over the stamped manifest", again_run.returncode, 0)

            # the point of the whole package: the projection joins again.
            projection = CC.coverage_projection(task, report={}, manifest=migrated)
            check("coverage_projection now joins instances instead of reporting nine gaps",
                  projection["unique_instances"] > 0,
                  f"unique_instances = {projection['unique_instances']}")
            check_eq("every obligation of the plan is reachable",
                     sorted(o["obligation_id"] for o in projection["obligations"]),
                     ["TS-1-O1", "TS-1-O2", "TS-2-O1"])

            # run twice: the second pass has nothing left to rename and writes nothing.
            again = MA._rename_legacy_obligations(
                task, TICKET, root,
                json.loads((task / "work" / "automation-manifest.json").read_text(encoding="utf-8")))
            check_eq("a second run renames nothing", again["changed"], [])
    finally:
        cleanup(root)

    # --- 4b. FV1-19 (row p, re-pinned by F1): the two retraction sites resend the covering rows by identity only ------------
    import migrate_artifacts as MA
    stale_cover = {"case": "TC-005", "file": "tests/t.py", "instance_id": "test_five", "covers": ["TC-005"], "status": "green",
                   "obligation_refs": [{"obligation_id": "TS-1-O1", "obligation_hash": "stale"}], "obligation_ids": ["TS-1-O1"],
                   "obligation_hash": "stale-row"}
    ghost = {"case": "TC-005", "file": "tests/t.py", "instance_id": "TC-005", "covers": ["TC-005"], "status": "unknown"}
    legacy = {"case": "TC-005", "selector": "test_five", "status": "unknown"}
    for site, run_site, extra, said in (
            ("_retract_case_ghosts", MA._retract_case_ghosts, ghost, "ghost retracted"),
            ("_retract_legacy_selector_rows", MA._retract_legacy_selector_rows, legacy, "legacy selector row retracted")):
        for cites in ("TS-1-O1", "TS-9-O9"):   # an id the plan names, and one it no longer names
            root, task = make_story()
            try:
                cover = dict(stale_cover, obligation_refs=[{"obligation_id": cites, "obligation_hash": "stale"}], obligation_ids=[cites])
                seed = {"tests": [extra, cover]}
                (task / "work" / "automation-manifest.json").write_text(json.dumps(seed), encoding="utf-8")
                (task / "state").mkdir(exist_ok=True)
                result = run_site(task, TICKET, root, json.loads((task / "work" / "automation-manifest.json").read_text(encoding="utf-8")))
                after = json.loads((task / "work" / "automation-manifest.json").read_text(encoding="utf-8"))
                five = next(t for t in after["tests"] if t.get("instance_id") == "test_five")
                # FV1-19 F1 (Lead, t-515): a retraction resends the covering row by identity only - no refs, ids or row hash -
                # so the stored references stay exactly as stored (stale stays stale) and the retraction never depends on the plan.
                check_eq(f"(p) {site}: a covering row citing {cites} (stale stored hash): the retraction commits, nothing left",
                         (len(result["left"]), any(said in c for c in result["changed"]), len(after["tests"])), (0, True, 1))
                check_eq(f"(p) {site}: ... and the covering row's refs, ids and row hash stay exactly as stored (never restamped)",
                         (five["obligation_refs"], five["obligation_ids"], five["obligation_hash"]),
                         ([{"obligation_id": cites, "obligation_hash": "stale"}], [cites], "stale-row"))
            finally:
                cleanup(root)

    # --- one stale test row can leave the manifest (TP1-13797, 27.09) -------------------
    # `tests[]` had no door: a row leaves only when every case it proves goes unresolved, and a
    # partition-scoped unresolved row by design does not compete with `tests[]`. So seven rows
    # written before each partition had an explicit id stood beside the good ones, `run_suite`
    # refused the whole case request over one id it could not find, and TC-002/TC-003 could not
    # be run at all.
    import manifest_put as MP
    held = {"tests": [
        {"instance_id": "test_x[case0]", "test_file": "a.py", "covers": ["TC-002"]},
        {"instance_id": "test_x[regex-operator]", "test_file": "a.py", "covers": ["TC-002"]},
        {"instance_id": "test_y[falsy-match]", "test_file": "a.py", "covers": ["TC-003"]}]}
    summary = {}
    MP._retract_instances(held, {"retracted_instances": ["test_x[case0]"]}, summary)
    check_eq("a retracted instance leaves tests[], the case's good rows stay",
             [e["instance_id"] for e in held["tests"]],
             ["test_x[regex-operator]", "test_y[falsy-match]"])
    check_eq("and the retraction is recorded for the next reader",
             held.get("retracted_instances"), ["test_x[case0]"])
    check_eq("the summary counts it", summary.get("retracted_instances"), 1)
    refused = ""
    try:
        MP._retract_instances(dict(held), {"retracted_instances": ["test_x[regex-operator]"],
            "tests": [{"instance_id": "test_x[regex-operator]", "test_file": "a.py",
                       "covers": ["TC-002"]}]}, {})
    except ValueError as exc:
        refused = str(exc)
    check_in("one fragment cannot both send and retract an instance",
             "cannot both send and retract", refused)
    missing = ""
    try:
        MP._retract_instances(dict(held), {"retracted_instances": ["test_z[nope]"]}, {})
    except ValueError as exc:
        missing = str(exc)
    check_in("and an id no row answers to is refused, not silently ignored",
             "names no row this manifest holds", missing)

    fv1_30b_n2_refs_words()
    finish("obligation join (TP2-2553)")


if __name__ == "__main__":
    main()
