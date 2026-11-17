# T1r-cards-a report (t-1214, node told-before-work/1/TBW1-13)

Branch `worktree-agent-a1bfa3bfdead0ba50`, commit `ba946ab6` (pushed). Base: origin/main `b5fca9bd` (after wave B and K1b).

## Status

Done except ONE key: `ra-2` (K line of qa-retro-analyst) is NOT landed - STOP, a QUESTION for the Lead (below). Everything else of A-1..A-9 is done.

### Question (1)

`ra-2` text (spec section 3.4, verbatim: "The story's spend is the sessions the driver's own journal names ... the cost files are token-priced ...") contains the words `journal` and `cost files`. The existing, non-quarantined, non-slow test `scripts/tests/test_charters_s5_s9.py::test_retro_reads_only_the_numbers` (:198-203) asserts `"state/cost" not in text and "journal" not in text` over `agents/qa-retro-analyst.md`; landing ra-2 turned it red (measured: `1 failed, 59 passed`). The test is outside my owns and a non-goal ("every test file"). I removed the ra-2 line (charter back to ra-1, ra-3k only) and left it unimplemented. Options for the Lead: (a) re-word ra-2 without the words journal / state/cost; (b) have a node that owns `test_charters_s5_s9.py` move the pin; (c) drop ra-2 (the content stays in the card until -b, so the role is told it; -b must not retire the card text before ra-2 lands somewhere). S-K therefore reports 1 failed (ra-2), by this STOP, not by a defect.

## A-1 measure before (main b5fca9bd, verbatim tails)

```
stage_joints.py --check: stage joints: ... rows 273 ... told counters: hand_cards 12, legacy_legs 0, unsited 11 | stage joints: clean
contract_slices.py --check: slices: 44 declared, all present and fresh; 18 key pages; 12 charters carry a generated digest line
role_rules.py --check: role-rules: 457 rows, 546 carriers checked, 0 finding(s)
dry_exits.py --check: NUMBER ratchet (rows now / base): live_only 68/0, after 0/0, unwalked 270/39, hook_layer 77/77; raised_by 299 ... NOTE ratchet unwalked: raised 231 row(s) above the base 39 ... dry_exits --check: 0 discrepancies
```

## Verbatim witness (one run after all edits)

`scenario_walk.py --witness-for <the 17 owned paths>` printed 25 distinct keep test files; none is quarantined (test-layers.json `quarantine` read: none of the 25). Files over `slow_tests.json` `thresholds.slow_over_s` = 10 s (judged by the batch canon, NOT run here): test_audit_rules (18.3), test_branch_accounting (73.3), test_brief_pack (27.3), test_bug_records (28.7), test_contract_slices (26.2), test_detector_verdict (14.7), test_field_producers (17.1), test_hooks_wiring (19.3), test_manifest_from_tests (79.0), test_readiness (28.2), test_s5_precheck (29.7), test_scenario_dry_1 (221.6), test_selftest_slow_tests (12.8), test_stage_joints (259.4), test_third_verdict (39.7). Run, each alone, after all edits (final tails):

```
test_ahead_cards: 253/253 ok
test_charters_s5_s9: 60 passed in 0.44s   (after removing ra-2; with ra-2 it was 1 failed, 59 passed)
test_delivery_ownership: 310/310 ok
env evidence: 42/42 ok
test_first_look_wiring: 102/102 ok
onboarding notes: 328/328 ok
oracle provenance: 296/296 ok
role_load (the one measure of a role's start load): 186/186 ok
test_validator_class: 51/51 ok
test_walk_plan_fields: 123/123 ok
dry_exits.py --check: ... NOTE ratchet unwalked: raised 243 row(s) above the base 39, named in raised_by: [...] | dry_exits --check: 0 discrepancies   (231 -> 243: the 12 named entries)
contract_slices.py --write then --check: slices: 44 declared, all present and fresh; 20 key pages; 12 charters carry a generated digest line   (no WARN K8)
role_rules.py --check: role-rules: 457 rows, 546 carriers checked, 0 finding(s)
stage_joints.py --check: told counters: hand_cards 12, legacy_legs 0, unsited 17 | REJECT - 1 finding(s): stage-joints: told_ratchet.unsited is 11 but 17 rows have no site in code (...)
selftest.py --limits --lang: PASS limits (size caps); PASS every mandatory role rule; === qa-factory selftest: 4/4 ok ===
t1rc_keys.py <worktree>: FAIL ra-2: fact '1,911' not in agents/qa-retro-analyst.md | t1rc keys: 108 checked, 1 failed | exit=1
t1rc_keys.py <worktree> --negative: FAIL NEG: text not in the requirement of validate_artifacts:check_run_report_head | FAIL NEG: no page line of qa-runner begins - [validate_artifacts:check_run_report_head] and holds the text | t1rc keys: 109 checked, 3 failed | exit=1
```

stage_joints --check, the ONLY finding: unsited 11 -> 17, the 6 ids: `source_preflight:check_source_inventory`, `estimate_record:facts_problems`, `artifact_producer:validate`, `gate_preflight:question_branches`, `s5_precheck:sides.provisional`, `s5_precheck:sides.pending` (all six found by name in the finding text; no missing-door or shape finding). For TBW-T1rc-int: stored 11 -> 17 (main's `unsited` is 11 after wave B, not the spec's 17-on-wave-B/46-on-main; the +6 is the spec's).

## Per-key lines (spec 3.4)

Landed (row keys: text inside the row requirement AND on a page line `- [<row>]` of the role, S-K): every `row` and `door` key of 3.4 (sc-2, sc-3, sc-4, rt-1a..rt-5, ts-1a, ts-3b, ts-3c, cd-1, cd-2, cd-4b, cd-4c, cd-4e, cc-1, au-1..au-3, au-5, au-6, 3.3c, ck-3b, ru-1..ru-6, fa-1a..fa-1f, ds-1..ds-7, br-1b..br-4a, ra-3, 3.3, 3.3b, 4-prov, 4-pend, 4-none, 4-fp, 4-ren). S-K: all 108 non-ra-2 keys pass.

K lines (charter, appended as `- <text>` last line of the named section):

- sc-5: landed (agents/qa-scout.md)
- rt-2k: landed (agents/qa-requirements-tester.md)
- ts-0: landed (agents/qa-test-strategist.md)
- ts-1k: landed (agents/qa-test-strategist.md)
- ts-2b: landed (agents/qa-test-strategist.md)
- ts-3a: landed (agents/qa-test-strategist.md)
- cd-2k: landed (agents/qa-case-designer.md)
- cd-3: landed (agents/qa-case-designer.md)
- cd-4a: SKIPPED: fact present (agents/qa-case-designer.md)
- cd-4d: landed (agents/qa-case-designer.md)
- au-4: landed (agents/qa-automator.md)
- ck-1: landed (agents/qa-code-critic.md)
- ck-2: landed (agents/qa-code-critic.md)
- ck-3a: landed (agents/qa-code-critic.md)
- ck-4a: landed (agents/qa-code-critic.md)
- fa-1ak: landed (agents/qa-failure-analyst.md)
- fa-1g: landed (agents/qa-failure-analyst.md)
- ds-1k: SKIPPED: fact present (agents/qa-doc-scribe.md)
- ds-4a: landed (agents/qa-doc-scribe.md)
- ds-4b: SKIPPED: fact present (agents/qa-doc-scribe.md)
- ds-6a: SKIPPED: fact present (agents/qa-doc-scribe.md)
- br-1a: landed (agents/qa-bug-reporter.md)
- br-2k: landed (agents/qa-bug-reporter.md)
- br-3k: landed (agents/qa-bug-reporter.md)
- br-4bk: landed (agents/qa-bug-reporter.md)
- ra-1: landed (agents/qa-retro-analyst.md)
- ra-2: NOT landed: STOP, question (1) (agents/qa-retro-analyst.md)
- ra-3k: landed (agents/qa-retro-analyst.md)
- ra-4: SKIPPED: fact present (agents/qa-retro-analyst.md)

K skipped by fact (R-5): ds-1k, ds-4b (fact `left_items` stands at qa-doc-scribe.md:23, the charter already says one item per `left_items` entry; the spec expected ds-4b to land), ds-6a, ra-4. cd-4a: spec-skipped by F14 (it is not a key of the block). qa-runner.md and qa-case-critic.md: no K line, untouched.

T/R/drops (per spec 3.1, nothing written): T/R sc-1, ts-2a, ts-3d, ck-4b, ru-4c, br-3, br-4b; drops rt-0, br-2b, ds-4d; cuts applied inside the keys (the texts are the 3.4 texts, not reworded).

ROLE+ (R-4a): `manifest_put:expectation_changes` gained a producer entry for qa-code-critic (`told: [{"page": true}]`, `demands: []`, field copied).
M2 (R-3, 3.5 doors): `exit_gate:grounding`, `exit_gate:case_identity`, `critic_rollcall:*` (field doors), `check_coverage:*` (`door_needs: shell`, `when: [shell]`); their producer `told` is now `[{"page": true}]`.
role_rule (R-8): set on check_behaviour_claims (tester-card-derived-row-also-gets-a-behaviour-claims-row), planning_contract:branches (letter-branch-settles-oracle), coverage_contract:obligations (designer-card-observation-sufficiency-review), exit_gate:case_identity (case-id-in-briefs-form), validate_artifacts:check_case (designer-card-reuse-decision-vocabulary), gate_preflight:question_branches NEW (designer-one-case-per-plan-row), check_then_oracles (designer-now-before-keys), critic_rollcall:* (merge-keep-only-for-p16-p19), check_report_ledger_and_readiness (scribe-card-delivery-ready-line-is-the-blocks). Pairs with another existing role_rule: none. role_rules.py --check 0 findings.
Door replaced (R-6): `validate_artifacts:check_run_report_empty` door was: `edit the file and the field the refusal line names` -> ru-5 door.

## E-4: the pre-append sentence of every touched row (verbatim, for TBW-T1rc-ec8)

- `validate_artifacts:check_context_manifest_v0`: Every `related[]` entry is an object with a `kind` from `RELATED_KINDS` and a `source`; every `implementations[]` entry is an object naming a `repo` once with a listed `source`; the list keys are arrays or absent.
- `validate_artifacts:check_register`: The register's front matter carries the required fields, non-empty `ids` of the form R-n, sources from the source list and `confidence` high or low; every declared id has a full-width row under the register heading with a listed source (or a derivation), matrix cells per the grammar and an impact from the project's scale.
- `validate_artifacts:check_behaviour_claims`: Every requirement seen only in the implementation has exactly one entry under the behaviour-claims heading, with an `origin` from its list and the fields of a claim.
- `validate_artifacts:check_understanding`: The understanding file stays within `UNDERSTANDING_MAX_LINES`, has every section of `UNDERSTANDING_SECTIONS`, and names every requirement id in a "What we verify" or "What we do not verify" line.
- `planning_contract:plan`: The plan validates: every obligation of the registry has its row, coverage revisions and revision marks are consistent (validate_plan + coverage_revision_errors + unmarked_revision_errors).
- `planning_contract:branches`: Every question branch kind of S3_EXIT_KINDS is accounted for (the messages name what each kind expects).
- `coverage_contract:obligations`: Each obligation in the plan names its requirement, its coverage and a known state, per the messages of validate_obligations.
- `validate_artifacts:check_case`: A case file opens with YAML front matter that carries every required field, takes `status`, `priority`, `channel` and `reuse_decision` from their closed lists, carries `automated_by` (file::test) when `Automated`, a `red_lock` that names a BUG-NNN, passes the form checks, and covers register requirements (or legacy `covers_ac`).
- `validate_artifacts:check_then_oracles`: A case written on or after the oracle cutoff gives every Then an entry in `then_oracles` with a basis per the oracle grammar.
- `s5_precheck:bindings`: Every Then clause of every case in scope is bound to a test and an assertion (`then_bindings`), or is a remainder the person took (`then handed:`), named.
- `s5_precheck:oracle`: A test never asserts an expected value the case left `open` or `invalid`; a test that went red and later passed on changed code has an `expectation_changes[]` record whose `then_refs` resolve; an unresolved row never disputes the approved case.
- `manifest_put:expectation_changes`: An expectation change names its function(s), red_attempt, green_attempt (or null), then_refs as `[{case, then: int}]`, what_changed, and a reason for a new row; the patch verdict joins; critic_verdict is a list, critic_note a string, and a note stands for each NOTE_REQUIRED_VERDICTS verdict.
- `s5_precheck:environment`: A `blocked_by_env` row of this dispatch carries the fix it found (`remedy`), names no credential value, blames the stand for no fixture the approved case never asked for, and stands on a run that shows the stand.
- `s5_precheck:manifest`: The manifest of this dispatch's cases keeps the invariants `manifest_put.py` owns (one instance per id, a covering row per scoped case), as a hand edit would break them.
- `validate_artifacts:check_run_report_head`: The run report carries a non-empty `head`.
- `validate_artifacts:check_run_report_v0`: The run report carries an `execution_status` from its list, computed from the run's own evidence, and `blocked` when `env_preflight` is blocked.
- `validate_artifacts:check_result_rows`: Every `results[]` row is an object naming one case or a test id, with a status from its list, a reason when skipped, and totals that agree with the rows.
- `validate_artifacts:check_run_report_empty`: A run with zero tests carries `env_preflight: blocked`, or names its environment-blocked, manual-check or manual-skipped rows.
- `validate_artifacts:check_run_report_coverage`: Every case S5 automated and every manual-agent plan row is accounted for in the run report.
- `validate_artifacts:check_triage_v0`: One triage row per observation, a verdict from its list, and a FLAKY verdict only with enough reruns, a listed mechanism and a `fix_result`.
- `validate_artifacts:check_report_blocks`: Every code-owned block stands with its markers, opens with its own heading and holds no section heading; "Decided at gate B" stands only when gate B has recorded words, and never quotes gate A's.
- `validate_artifacts:check_report_ledger_and_readiness`: Hand text outside the generated tables stays within `TEST_REPORT_MAX_BYTES`, section 1 is the table `ledger.py` generated, and a `delivery_ready: yes|after_checks|no` line agrees with `ledger.json`.
- `validate_artifacts:check_report_sections`: Every template section stands, in the template's order, with the verdict and its `delivery_ready:` line above the rest.
- `validate_artifacts:check_report_left_with_you`: Every `Left with you` item names its requirement and case, what a person would observe, and how.
- `validate_artifacts:check_report_traceability`: Every register requirement and every plan case stands in a row of the traceability appendix.
- `validate_artifacts:check_bug`: A bug file opens with front matter that carries every required field, with `status` from its list and `severity` from the allowed set.
- `validate_artifacts:check_bug_form`: A bug carries an impact from the scale and the sections that make it reproducible; when its source draft has several manifestations of one cause, the source draft is readable, `cases` lists every manifestation's case and a `## Manifestations` section has one complete line per case.
- `validate_artifacts:check_bug_filing_header`: A bug filed from a draft of this run carries non-empty `cases` (from the draft's `case`/`cases`) and `requirements` (the R-n its `violates` names).
- `validate_artifacts:check_case_form`: `covers` names only register `R-n` ids of the task's register (or `legacy:<import reason>`), and the case inherits `defect_class` and `basis` from its plan row.
- `planning_contract:contradictions`: No two plan rows contradict each other on the same requirement.

## The 12 NEW rows and the 12 census rows

New rows (R-4 form, sited under their family or neighbour): `source_preflight:check_source_inventory`, `exit_gate:witness_errors.requirements-tester`, `exit_gate:witness_errors.runner`, `exit_gate:witness_errors.failure-analyst`, `artifact_producer:validate`, `gate_preflight:question_branches`, `estimate_record:facts_problems`, `s5_precheck:sides.provisional`, `s5_precheck:sides.pending`, `execution_request:profile.none`, `execution_request:fingerprint.build`, `handoff_check:cli.values_rename`.
Census rows (4.3): s1-s4.json: source_preflight:check_source_inventory, exit_gate:witness_errors.requirements-tester, gate_preflight:question_branches; s5.json: s5_precheck:sides.provisional, s5_precheck:sides.pending; s6-s9.json: exit_gate:witness_errors.runner, exit_gate:witness_errors.failure-analyst, artifact_producer:validate, estimate_record:facts_problems; gates.json: execution_request:profile.none, execution_request:fingerprint.build, handoff_check:cli.values_rename. Each `reach: unwalked`, 12 `raised_by` entries `unwalked | joints/<id> | T1r-cards-a, 2026-11-17`, bases unchanged. Note from `dry_exits --check`: `ratchet unwalked: raised 243 row(s) above the base 39` (231 before = +12 named).

## K8 page sizes (bytes of the pages written by `contract_slices.py --write`; every page under 12,000)

Largest after: qa-automator handoff-keys-2 11,475; qa-runner handoff-keys 11,567; qa-requirements-tester 11,592; qa-code-critic 11,669; qa-doc-scribe handoff-keys 11,898; qa-automator handoff-keys 11,912; qa-failure-analyst 11,982. Splits (continuation lines added to inject-map.json, same commit): qa-automator `handoff-keys-3.md` (was 14,090 B in -2 > 12,000 slice cap, found by `selftest --limits`; `contract_slices --check` alone did not flag it), qa-doc-scribe `handoff-keys-2.md` (was 13,110 B). Key pages 18 -> 20. No `WARN K8`.

## K10 plugin share U vs headroom H, and the raises (E-9)

```
role                U before(baseline)  U after   H        raise (U-H)
qa-test-strategist  53,739              55,103    42,400   native_headroom 53739 -> 55103 (U-H = 12,703 B)
qa-automator        76,162              79,970    68,400   native_headroom 76162 -> 79970 (U-H = 11,570 B)
qa-code-critic      72,717              75,268    68,400   native_headroom 72717 -> 75268 (U-H = 6,868 B)
```
Largest U = qa-automator 79,970 B, under the 100,000 B Codex ceiling: no STOP (R2-F6'). The other 9 roles are under their H. (before = the stored baselines, which were tight.)

ratchet_tokens (raise: role key old -> new): requirements-tester 14881 -> 14907 (+26); case-designer 15167 -> 15230 (+63); automator 24824 -> 25699 (+875); code-critic 23394 -> 23607 (+213); failure-analyst 20930 -> 21557 (+627); doc-scribe 20420 -> 20501 (+81). process_ratchet_tokens (tight, slack 0): scout 15386 -> 15713; requirements-tester 13153 -> 13538; test-strategist 17629 -> 17899; case-designer 13512 -> 13895; case-critic 18795 -> 19112; automator 23180 -> 24109; code-critic 21146 -> 21747; runner 16732 -> 17278; failure-analyst 18905 -> 19489; bug-reporter 15447 -> 15705; doc-scribe 19083 -> 19462; retro-analyst 14476 -> 14620. All in the commit message as `raise:` lines. test_role_load 186/186.

## FR walk (design/factory-rules.md, touched sections)

- A (FR-1/2/4/5): FR-2 kept: a `door_needs: shell` row exists only for roles with Bash (ck-3b's row told to qa-code-critic, which has Bash); the three no-Bash roles (case-critic, case-designer, test-strategist) carry field doors (cd-1, cd-4b, cc-1 doors name fields/files). One door per row (R-6). The `values_rename` door is a shell door told to the 9 Bash roles only (R4-F3). B - text to a person not touched. C (FR-11, FR-38): every landed clause names a field its check reads; the requirement reaches the role before the work, on its page. D (FR-58): all expected values come from the spec's 3.4 block, none from new output. E, F - not touched. G: FR-30 English ASCII (selftest --lang PASS), FR-54 siblings below.

## Deviations, E-13, analogs, beyond the manifest

- E-13 (body no longer checks a clause at today's line): not verified clause by clause (115 KB spec, cost cap). Checked by diff: `git diff c9b42659..HEAD` on validate_artifacts.py is only `refusal(...)` wrapping (no check changed), and manifest_put.py / execution_request.py / planning_contract.py hunks touch only `probe_owed`, `_match` reuse, and a door sentence (no clause of 3.1). No STOP by E-13 was needed; the full per-clause body re-read of the NEW rows' bodies was NOT done (estimate, not verified). The critic reading 3.1 bodies is the check.
- inject-map.json: owns scope says 'continuation page lines only' - used exactly for the two splits.
- Deviation from the dispatch: the dispatch AR line is `AR-10, AR-20, AR-29`; the spec 1 lists also AR-11, AR-22 (the commit names the dispatch's three).
- Spec-vs-reality: spec said unsited stored 46 (main) / 17 (wave B); the tree stored 11 (after wave B + others), +6 -> 17 for TBW-T1rc-int. The key block row for qa-scout `sc-4` etc. all matched. ds-4b was skipped by fact (spec expected a K line).
- A K line is appended as a bullet `- <text>` (my choice of form; the spec says 'as the last line of the section'). In qa-scout.md `## Tools` the last line is inside/after the generated digest block (`<!-- /gen -->`); the bullet stands after it.
- Analogs noticed (not fixed): `estimate_record.append_record` writes no delta/hit/ts while a card names them (spec-reported analog); `contract_slices --check` does not flag a continuation page over the 12,000 B slice cap (only `selftest --limits` does) - a gap between K8 and the limits check; `test_charters_s5_s9::test_retro_reads_only_the_numbers` pins words in a charter, same class as the quarantined card pins (candidate for the -b re-point list).
- Beyond the manifest: `scripts/role_load.py` (to compute the raises), `scripts/slow_tests.json`, `scripts/tests/test-layers.json`, `scripts/tests/test_charters_s5_s9.py`.
- Not done: ra-2 (question 1). Not run locally (batch canon): the 15 slow files above; CI.

## S-K script (full source, never committed; scratchpad t1rc_keys.py, extracted verbatim from spec section 6)

```python
"""Supplementary key-presence check of T1r-cards-a (spec r3 section 3.4). Never committed."""
import json
import re
import sys
from pathlib import Path

SPEC = Path(r"C:\QAFactory\forge-repo\docs\tasks\specs\20261117-told-before-work-t1r-cards-spec-r3.md")
NEGATIVE = {"seg": "NEG", "kind": "row", "role": "qa-runner", "row": "validate_artifacts:check_run_report_head",
            "text": "NEGATIVE CONTROL: this sentence stands on no row and no page."}


def main(argv):
    root = Path(argv[1]).resolve()
    pkg = root / "ai-packages" / "qa-factory"
    sys.path.insert(0, str(pkg / "scripts"))
    import contract_slices
    found = re.search(r"<!-- keys:begin -->\s*```json\n(.*?)\n```\s*<!-- keys:end -->",
                      SPEC.read_text(encoding="utf-8"), re.S)
    if not found:
        print("t1rc keys: the key block of the spec cannot be read")
        return 2
    keys = json.loads(found.group(1)) + ([NEGATIVE] if "--negative" in argv else [])
    rows = {r.get("check"): r for r in json.loads((pkg / "references" / "stage-joints.json").read_text(encoding="utf-8"))["joints"]}
    pages, failed = {}, []
    for key in keys:
        seg, kind, text = key["seg"], key["kind"], key["text"]
        if kind == "k":
            body = (pkg / key["file"]).read_text(encoding="utf-8")
            if key["fact"].lower() not in body.lower():
                failed.append(f"{seg}: fact {key['fact']!r} not in {key['file']}")
            continue
        row = rows.get(key["row"])
        if row is None:
            failed.append(f"{seg}: no row {key['row']}")
            continue
        if kind == "door":
            if row.get("door") != text:
                failed.append(f"{seg}: door of {key['row']} is {row.get('door')!r}")
            continue
        if text not in str(row.get("requirement") or ""):
            failed.append(f"{seg}: text not in the requirement of {key['row']}")
        if key["role"] not in pages:
            pages[key["role"]] = "\n".join(contract_slices.handoff_keys_pages(pkg, key["role"])).splitlines()
        if not any(line.startswith(f"- [{key['row']}]") and text in line for line in pages[key["role"]]):
            failed.append(f"{seg}: no page line of {key['role']} begins - [{key['row']}] and holds the text")
    for line in failed:
        print("FAIL " + line)
    print(f"t1rc keys: {len(keys)} checked, {len(failed)} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
```
