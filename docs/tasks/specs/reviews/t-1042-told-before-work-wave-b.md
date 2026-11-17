# t-1042 — topic critic, told-before-work wave B (branch `worktree-agent-ad0767bec786dddde`, head a65afe58)

Critic (Opus), one pass for the topic. Spec: `docs/tasks/specs/20261117-told-before-work-finish-spec.md` §6 (common card, T4b, T7a), §3, Lead decisions; mech spec §2.8, §5.3.

## Verdict

**fit_with_fixes**: no finding blocks the merge. One fix round on this branch (F1-F5), plus pile nodes (N1-N3). Accepting is the Lead's call.

| part | verdict line |
|---|---|
| T7a-B (t-1023) | fit with fixes: the sites are correct and byte-identical. The E6 class of the bare `check_phase_json` branches is wrong (F2) |
| T7a-C (t-1024) | fit: 19 functions, 59 sites, byte-identical, each id is its own function's row. The test-loop clone is shared with A/B (F4) |
| T4b (t-1031) | fit with fixes: the decisions are the same and the text is byte-identical. The walker control is tautological (F5), the walker row decision is open (F3), and one EC-2 reason is misstated (note) |
| integrator (t-1030) | fit with fixes: `unsited` 17 is measured, the ceilings only drop, and five spot-checked units are right. The `check_phase_json` census row understates its roles by more than its own deviation says (F1) |

## Findings

**F1 — fix in round (+ node N1). `check_phase_json` census row: more roles meet it than the integrator found.**
Evidence: `validate_artifacts.py:1726`: `errors.append(told(f"{path.name}: broken JSON ({e})"))` runs for EVERY `.json` file. `collect_errors` calls it for every in-artifacts JSON (`:2680-2681`). `exit_gate.collect_errors` calls it for every JSON under the story (`exit_gate.py:1324-1325`). `scoped_errors.mine()` then hands each error to the stage whose `outputs` list that file name (`exit_gate.py:1429-1480`; stages.json: S2 `requirements-readiness.json`, S3 `test-plan.json`, S5 `automation-manifest.json` + `s5-plan.json`, S6 `run-report.json`). Probe (scratch, verbatim):
```
'test-plan.json: broken JSON (Expecting property name ...' | check= None
'requirements-readiness.json: broken JSON (Expecting property name ...' | check= None
"context-manifest.json: required key 'acceptance_criteria' is missing" | check= validate_artifacts:check_phase_json.context-manifest.json
```
So qa-requirements-tester, qa-test-strategist, qa-automator and qa-runner all meet `check_phase_json` (bare). The census says only `["qa-failure-analyst", "qa-scout", "conductor"]`, and the hand-back lists only automator and runner. This goes against the Lead's rule (narrow to the roles that REALLY meet the check). It also stores a debt: correcting it later raises 4 per-role ceilings by 1 each (an AR-20 raise that must be named).
Fix this round: put a `note` on that census row naming the 4 roles that meet it with no row, and the node id (FR-41: the known gap is said, not hidden). Correct the hand-back table to match.
Node N1 (file `references/stage-joints.json` + `validate_artifacts.py::check_phase_json.told` + the census row): add rows `validate_artifacts:check_phase_json.automation-manifest.json` (qa-automator, S5) and `.run-report.json` (qa-runner, S6), `requirement_from: validate_artifacts.PHASE_JSON_KEYS`, `carrier_key` as the existing two. Add one row for the broken-JSON branch ("a JSON artifact parses"), producers = every role that writes a JSON artifact (artifact-writers.json: scout, requirements-tester, strategist, automator, failure-analyst). Site them in `told()`. Restore the census roles to the true set, with a named raise of the 4 ceilings. Expected: K5/real green with the true roles. Owner: T1r-cards-R / the told-before-work pile (stage-joints rows are T1r-cards' file).

**F2 — fix in round (report text). T7a-B's E6 says "(code) code writer, no row" and "(role): none".** The bare branches of `check_phase_json` are met by roles (F1 evidence). Fix: reclass them as `(role)` in `20261117-tbw-t7a-b-report.md` and point to N1. The test row `t7a-b check_phase_json (no row for the file)` (`test_validators.py`, tbw_t7a_b_sites last check) pins the untold state as expected. That is acceptable as a change detector, but N1 must flip it.

**F3 — fix in round, Lead decides T4b Q1. `stage_guard:SG-walker-error` is a real row, not a pointer.** stage-joints has a row with requirement "A shell command is one the stage guard's command reader can walk." and 12 producer roles. Yet `stage_guard.py:1238` `deny(hooklib.WALKER_DOOR.format(reason=e))` prints no expected/door. The spec's "row 31 a pointer" (wave0 8b) is stale against the file. My recommendation: site it (one `DV.refusal("stage_guard:SG-walker-error", ...)` line + one row in `tbw_t4b_sites`). Before that, confirm with `test_refusal_registry` that the A24 key for `hooklib.WALKER_DOOR.format(` (refusal_registry.py:818) still matches.

**F4 — fix in round (minor, brief item 6). Clone of the assertion loop.** `test_validators.py` tbw_t7a_a_sites / tbw_t7a_b_sites / tbw_t7a_c_sites each carry the same ~12-line loop: refuses, old text, id, row sentence, Record sentence. Fix: one helper `_sites_table(label, rows, allowed=())` called by the three functions. This keeps F-2(b)'s one-function-per-node, with one parameterised behaviour.

**F5 — fix in round (minor, brief 5a). The T4b walker control is tautological.** `tbw_t4b_sites` calls `sg.deny(hooklib.WALKER_DOOR.format(reason="boom"))` with a plain `str`. `deny` of a plain str can never print `check:`, so the row cannot fail. Fix: drive `sg.check(event)` with the walker made to raise (mock), or replace the row with the F3 site row.

**Notes (no action this round unless the Lead says so):**
- N-a (node N2): the K12 counter is blind to A24-parented sub-ids. `stage_joints.sited_ids` counts `stage_guard:SG-command.*` and `SG-walker-error` as sited through their A24 parent (T4b report: "unsited 46 before and after"; my run: `walker sited? True`). A bare SG site therefore never raises `unsited`. Only the `tbw_t4b_sites` rows guard them. Node: `stage_joints.sited_ids` counts a row as sited only by a literal `refusal("<id>"`; expected: turning a T4b site bare raises `unsited` by 1.
- N-b: `stage_guard.py::explain` keeps 13 roles in the census. It is reached only by `stage_guard.py --ticket --stage` (qa-doctor/conductor). Grep of agents/references/skills for `--explain`/`stage_guard.py` found nothing; positive control: the same grep found `waiver.py` in 3 slices. The census overstates in the conservative direction. Cheap relabel (T4b Q2 named it, the integrator left it).
- N-c: T4b's EC-2 reason for `rule_delivery` ("other callers dispatch_errors…") is wrong: its only non-test caller is `check_command:2928` (grep). The outcome (id at the caller) is still legal.
- N-d: `check_command`'s last `return deny(f"{ticket}: {message}")` (runner branch) is now unreachable: every truthy return of `rule_typed_runner`/`_judge_slice` is a Record with one of the three ids. It is a harmless defensive fallback.
- N-e: EC-8 inputs for T1r-cards-R. Verified: `check_plan_v0` "names a register requirement", while the body checks only non-empty (`validate_artifacts.py:1872`). T7a-B also reports a `check_plan` count over-claim. NEW: `SG-command.delivery` "Before gate B, …" scopes wrongly, because `rule_delivery` (`stage_guard.py:1143-1172`) demands the ledger word at any time, not only before gate B. The role is told a narrower rule than the one enforced. Also the T4b-reported `stash` and `opaque` under-claims. None blocks: EC-8 forbids builders editing rows, and these rows were already page-told before the siting.
- N-f: the scanner counts `notes.append` / `ORACLE_NOTES.append` as bare. told-ratchet keeps bare 1 on `check_test_report:1147`, `check_report_blocks:1508`, `check_run_report_coverage:2160` although T7a-C has "E6: none". This is a counter false positive in the conservative direction.
- N-g: validate_artifacts sinks (`main` `"\n- ".join(found)`, hook `block(... join(errors))`) print the problem only. This matches the Lead's K3 decision (the validator family is told by the page) and is not a finding.
- N-h: axis 39 is not yet in `docs/SIBLING_MAP.md` (T10, owed by the Lead).

## Answers to the keys

1. **Byte identity — holds.** I parsed old and new with the AST and replaced each `refusal("<lit>", X)` by X. 27/28 owned validator functions are AST-identical to origin/main. The one difference, `check_phase_json`, differs only by the nested `told()`, which returns either the text or `refusal(<lit>, text)`; its decisions are unchanged (read :1712-1745). stage_guard: `rule_typed_runner`, `_judge_slice`, `check`, `check_dispatch` and the four rule helpers are identical. `check_command` I traced by hand. Old: `message = rule_pathspec(...) or rule_manifest(...)`, then `if message: return deny(...)` inside the loop. New: pathspec first, return if truthy, then manifest, return if truthy. Same order, same short-circuit, same continue. Stash and delivery each moved their own `if` into their branch, so the behaviour is the same. The text through `f"{ticket}: {message}"` is `str.__format__` of a str subclass, so it is identical. `deny` keeps `LAST_DENIAL` = problem only (`stage_guard.py:766-771`).
2. **Siting.** Every validator id equals `validate_artifacts:<its own function>` or the two `check_phase_json.<file>` rows (AST id census, Trail). All ids exist (tests assert `row_for`). T4b's 7 ids exist (stage-joints :2131-2374), each at the branch whose body its sentence describes. Under- and over-claims: N-e. They do not block: the AR-29 risk existed before the siting through the page, and the fix belongs to T1r-cards-R. `check_remedy_rows`: one id = one requirement. Its row IS the helper's ("a row blocked on the environment carries a remedy…"), and both callers (`check_phase_json:1745` run-report env_blocked, `check_manifest_invariants:2261` unresolved) impose that same requirement. So this is not an EC-2 breach. EC-2 guards helpers whose refusal means different requirements per caller. The same reading as the accepted `check_cell_counts`.
3. **Census narrowing.** Reach roads: the validate_artifacts PostToolUse hook (writer role, the guard owns writes); `exit_gate.scoped_errors` by stage outputs; `artifact_producer.validate` (`--kind triage` → `check_triage_v0`, failure analyst); `traceability --close-gate-b` → `check_test_report` (scribe/conductor). Spot-checks:
   - `check_remedy_rows` → automator + runner: correct.
   - `check_triage_v0` → failure-analyst: correct.
   - `check_plan_v0` → strategist (test-plan.md, S3): correct.
   - `check_context_manifest_v0` → scout: correct.
   - `check_test_report` → doc-scribe: correct.
   - `check_marker_in_file` → automator (via `check_manifest_v0:2193`): correct.
   - `check_phase_json`: WRONG, see F1. The roles are wider than the named deviation.

   The right fix for `check_phase_json` is N1 (rows + sites + true census, named raise). Until then, declare it with a census `note` (F1). It does not block the merge.
4. **Ratchets.** `blocking_per_role`: all 12 role ceilings lower, conductor 748 unchanged. No class, owner or `blocks_override` changed (my old/new census diff: 46 rows changed, roles/note only). The arithmetic matches the narrowing: bug-reporter −34 = all 34 narrowed units, scout/FA/strategist −32, automator −29, runner −28, scribe −21, each consistent with the kept lists. told-ratchet: every unit change is a drop. The dropped units are the 6 stage_guard helpers (callers: `check_dispatch:1874/1878/1887`, `explain:2963`, `waiver._guard_lines:642`, all dispatch- or person-word-time; roles are not told to run `waiver.py`) and the 3 inject_context units (T4b relabel, mech §2.8 IC-*). The `check_phase_json` unit stays in the baseline with bare 2, so `untold` hides nothing there; the understatement lives in the census/K5 (F1). Wave A's sited units (guard_pre_tool, planning_contract, validate_artifacts A) also drop here: lowering to the measure, legal. `unsited` 46→17: my re-run measures 17, and the 17 are T9a controller (6) + T3b first_look (11), as §3 plans. The K12 pin is 17/17/17.
5. **hooklib / walker.** No hooklib change (empty diff stat). `shell_opaque_found` has two callers with different rows (`stage_guard.py:2776` row 25, `host_adapter.py:541` row 35), so the id goes at the callers: correct. The walker deny staying bare follows the spec's text, but the row file contradicts the spec (F3).
6. **Tests.** Killing power: each row asserts `check == id` and the row's lines after the problem. T4b's and T7a-B's negative controls show the row FAILing when the site is made bare. Expected values: the old texts are literals from the pre-edit byte copy (T4b: sha256 digests), and the ids/sentences come from `SJ.row_for`/`told_text`, not from the implementation. One behaviour per node table, but the loop is cloned (F4). F5 is a dead control. Volume: T7a-B 74 test vs ~105 product lines, within budget. T7a-C `tests-over:` "nineteen functions need one provoking fixture row each": holds (DoD row per id). T4b `tests-over:` "a row per id": partly. There are 13 rows for 7 ids, with 6 extra `request` variants that serve the per-site EC-1 claim. That is acceptable, but the stated reason is imprecise (note). No new test file.
7. **Duplication / quality / hygiene.** Duplication: F4. Otherwise none found. I grepped added package lines for `Record(` / `with_check(`: none, so `refusal()` is the one road (axis 34). The three `getattr(message,"check")` branches in `check_command` are forced by refusal_registry keying on the literal (T4b report, 533/533). Quality: N-d dead fallback; the `capture` mode inside `tbw_t4b_sites` is acceptable (it documents how the oracle was derived). Hygiene: added package lines have 0 Cyrillic and 0 control bytes. The non-ASCII is em-dashes moved with the old texts plus `§` in the spec-mandated census note. Changelog: three one-bullet English fragments. AR-n named in the reports (AR-9/13/18/20/29). JUDGMENT: no judgment moved: wrappers only, and census reclassification touches roles only.
8. **Class completeness.**
   - Axis 17: Record shape unchanged.
   - Axis 34: one road kept. A residual exclusion remains: `check_phase_json` bare for files with no row, with no data row → N1. Proposed as a node with an owner, per rule 19.
   - Axis 39: absent from the map (N-h).
   - Bare remainder a role can still meet with no id: the `check_phase_json` non-row files (F1/N1), the stage_guard walker deny (F3), `_oracle_dated` (EC-2, T7a-B listed it), and the multi-caller rule-helper bodies (sited at the caller, fine).
   - Analogs from the reports: `repo_words.py:187` third caller of `rule_pathspec`/`rule_stash` is a person text, bare: fine.
9. **What to do.**
   - Before the merge: nothing blocks.
   - Fix round on this branch: F1 (census note + hand-back correction), F2 (report reclass), F3 (site SG-walker-error if the Lead agrees), F4, F5. Optional: the N-b `explain` relabel.
   - Pile nodes: N1 (check_phase_json rows/sites/true census; `stage-joints.json`, `validate_artifacts.py::check_phase_json.told`, census row). N2 (`stage_joints.sited_ids` literal-only siting; expected: a bare T4b site raises `unsited` by 1). N-e lines to T1r-cards-R (`check_plan_v0`, `check_plan`, `SG-command.delivery`/`stash`/`opaque` sentences).

## Not checked
- `test_judgment_census.py`, `test_stage_joints.py` and the other slow files: not run, judged by the batch canon. The census ceilings were checked by arithmetic, not by `analyse`.
- `nfr-*.json` → `check_nfr_report` roles: not traced.
- The full `untold` 175 recount.
- Whether stage_guard and guard_pre_tool both fire on a walker crash (relevant to F3's value).

## Trail
Read: finish spec §6/§3/Lead decisions (:223-390, :664-697); mech spec §5.3 (:500-512); the integrator's hand-back part 2; the T4b, T7a-B and T7a-C reports; `detector_verdict.py:95-192`; `stage_guard.py:766-771, 905-930, 1135-1175, 1225-1238, 2760-2932, 2952-2970, 3558-3572`; `validate_artifacts.py:1712-1745, 1866-1876, 2645-2712, 2738-2790`; `exit_gate.py:1295-1335, 1429-1480`; `artifact_producer.py:1-30, 70-100`; `traceability.py:1905-1935`; `waiver.py:630-650`; stages.json outputs; artifact-writers.json role JSON writers; stage-joints rows for SG-command.*, SG-walker-error, check_remedy_rows, check_phase_json.*, check_plan*; `test_stage_joints.py:774-811, 865-873`; the test diffs; critic-diff-brief.md.

Re-runs (verbatim tails):
- `python -B …/scripts/stage_joints.py --check` → `told counters: hand_cards 12, legacy_legs 0, unsited 17` / `stage joints: clean`
- `python -B …/scripts/contract_slices.py --check` → `slices: 44 declared, all present and fresh; 19 key pages; 12 charters carry a generated digest line`
- `python -B …/scripts/tests/test_detector_verdict.py` → `=== test_detector_verdict: 802/802 ok ===`
- `python -B …/scripts/tests/test_validators.py` → `=== test_validators: 579/579 ok ===`
- AST strip-compare (scratch `astcmp.py`, origin/main vs head): 27 SAME + `check_phase_json` DIFF (told helper) for validate_artifacts; stage_guard 8 SAME + `check_command` DIFF (traced). Id census: each id = own function.
- unsited list via `SJ._direction_a`: 17 = controller ×6 + first_look ×11; `walker sited? True ['guard_pre_tool:PT-walker-error', 'stage_guard:SG-walker-error']`
- check_phase_json probe on broken `test-plan.json` / `requirements-readiness.json`: bare `check= None` (F1 output above).
- census old/new diff: `added set() removed set()`, 46 rows changed (roles/note only), `blocking_per_role` all lower.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "Axis 17 kept (Record shape unchanged); axis 34 kept (refusal() the one road, no Record/with_check in added package code), residual exclusion: check_phase_json bare for files without a row and the broken-JSON branch met by requirements-tester, strategist, automator, runner -> node N1; axis 39 not yet in SIBLING_MAP (T10, Lead). Bare remainder a role can meet: check_phase_json non-row files (F1/N1), stage_guard walker deny (F3), _oracle_dated (EC-2). Counter blind spot: sited_ids counts A24-parented sub-ids as sited (N2).",
  "fixes": [
    "F1 judgment-census.json check_phase_json row: add a note naming the four roles that meet it with no row (qa-requirements-tester, qa-test-strategist, qa-automator, qa-runner) and the node N1 id; correct the integrator hand-back table",
    "F2 docs/tasks/specs/reports/20261117-tbw-t7a-b-report.md E6: reclass the bare check_phase_json branches from (code) to (role), pointing to N1",
    "F3 stage_guard.py:1238 walker deny: site stage_guard:SG-walker-error through DV.refusal plus one tbw_t4b_sites row, if the Lead answers T4b Q1 that way (row exists with its own sentence)",
    "F4 test_validators.py: extract the cloned assertion loop of tbw_t7a_a/b/c_sites into one helper",
    "F5 test_detector_verdict.py tbw_t4b_sites walker control: drive sg.check with a raising walker instead of deny(plain str), or replace it by the F3 site row"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-told-before-work-finish-spec.md",
      "docs/tasks/specs/20261113-told-before-work-mechanism-spec.md",
      "docs/tasks/handoffs/t-1030-wave-b-integrator-part2.md",
      "docs/tasks/specs/reports/20261117-tbw-t4b-report.md",
      "docs/tasks/specs/reports/20261117-tbw-t7a-b-report.md",
      "docs/tasks/specs/reports/20261117-tbw-t7a-c-report.md",
      "ai-packages/qa-factory/scripts/detector_verdict.py",
      "ai-packages/qa-factory/scripts/stage_guard.py",
      "ai-packages/qa-factory/scripts/validate_artifacts.py",
      "ai-packages/qa-factory/scripts/exit_gate.py",
      "ai-packages/qa-factory/scripts/artifact_producer.py",
      "ai-packages/qa-factory/scripts/traceability.py",
      "ai-packages/qa-factory/scripts/waiver.py",
      "ai-packages/qa-factory/references/stage-joints.json",
      "ai-packages/qa-factory/references/stages.json",
      "ai-packages/qa-factory/references/artifact-writers.json",
      "ai-packages/qa-factory/scripts/tests/test_stage_joints.py",
      "ai-packages/qa-factory/scripts/tests/test_validators.py",
      "ai-packages/qa-factory/scripts/tests/test_detector_verdict.py",
      "ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json",
      "ai-packages/qa-factory/scripts/tests/fixtures/told-ratchet.json",
      "docs/tasks/critic-diff-brief.md"
    ],
    "reruns": [
      {"command": "python -B ai-packages/qa-factory/scripts/stage_joints.py --check", "result": "told counters: hand_cards 12, legacy_legs 0, unsited 17 / stage joints: clean"},
      {"command": "python -B ai-packages/qa-factory/scripts/contract_slices.py --check", "result": "slices: 44 declared, all present and fresh; 19 key pages; 12 charters carry a generated digest line"},
      {"command": "python -B ai-packages/qa-factory/scripts/tests/test_detector_verdict.py", "result": "=== test_detector_verdict: 802/802 ok ==="},
      {"command": "python -B ai-packages/qa-factory/scripts/tests/test_validators.py", "result": "=== test_validators: 579/579 ok ==="},
      {"command": "scratch astcmp.py origin/main vs a65afe58 (refusal wrapper stripped)", "result": "validate_artifacts 27 SAME, check_phase_json DIFF (told helper only); stage_guard 8 SAME, check_command DIFF (traced: same order and result)"},
      {"command": "scratch probe V.check_phase_json on broken test-plan.json / requirements-readiness.json", "result": "bare refusals, check=None: roles outside the census meet the unit (F1)"}
    ]
  }
}
```
