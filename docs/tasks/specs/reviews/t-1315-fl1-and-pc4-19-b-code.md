# t-1315 critic: FL1 (RD1-19, t-1254) and PC4-19 stream B (t-1259), code gate

Specs: `docs/tasks/specs/20261117-rd1-19-fl1-pytest-id-card.md`, `docs/tasks/specs/20261117-pc4-19-tests-near-300s-card.md` §3.B/§4/§5.
Heads reviewed: FL1 `4b48d2d5`, PC4-19 B `d11be9de`; both based on `e2ddb6d7`, 37 commits behind origin/main `0598c297`.
I ran checks on detached scratch worktrees of each head, then again after a trial `merge --no-commit origin/main`. All of those worktrees have been removed.

## Verdicts (input to the Lead's acceptance; the decision is the Lead's)

- **(A) FL1 / RD1-19: NEEDS WORK.** 1 blocker, 4 fix-before-merge, 3 notes.
- **(B) PC4-19 stream B: NEEDS WORK.** 1 blocker, 2 fix-before-merge, 3 notes. The split itself is correct: no check lost, none doubled.

---

## (A) FL1: findings

**A1 (blocker): the role-load cut removed the only role-facing statement of a required key.** In `references/artifact-contract-automation.md` the cut dropped `"evidence": "evidence/sanity.json",` from the `self_fixes` example (main :19). That line is also gone from the regenerated qa-automator and qa-code-critic slices. Yet `validate_artifacts.py::check_self_fixes` (:2356) still refuses a `self_fixes` row that has no `evidence`: `for key in ("test", "what", "why_test_defect", "evidence")`.
- Positive control: Grep for `why_test_defect` over agents/, references/, skills/ and handoffs/ finds only the contract and its two slices.
- Positive control: Grep for `self_fixes` near `evidence|keys` finds no other carrier. The joint text (handoff-keys-2 :30) only says "every required key".
- Failure scenario: the automator copies the example. Its manifest is refused at hand-off with "self_fixes[0] has no 'evidence'". That costs a refusal round for a rule the role was told before this change. This is the same class as the attempt-2 reject: a rule the code enforces, lost to a byte cut.
- The builder reported it as a "lost small detail". `role_rules --check` stays green only because the register has no row for this rule.
- Fix: put the line back, and pay for its ~10 tokens with another cut or a named raise of `role-load.json` (AR-20). Which one is the Lead's call. qa-automator has 2 tokens of slack (25,697 of 25,699).

**A2 (fix-before-merge): the FR-40 way out leaves a second row, a ghost that joins nothing.** Location: `manifest_put.py::stamp_node_ids` :954-966 (a stored `not_verified` row is eligible again) plus :1031-1035 (the rename).
- Scenario: `test_x[eu]` is stored `not_verified` (no collect existed yet). Later a collect answers and the row is re-sent with `file`. It is renamed to `test_x[chromium-eu]`. `merge` matches by `_identity`, and the aliases of the stored row do not include the new spelling (contract.py:4075-4105). So the old row stays and the new row is added beside it.
- Probe (`merge` is pure) output: `[('test_x[eu]', 'not_verified'), ('test_x[chromium-eu]', 'verified')]`.
- This breaks E8's invariant ("never creates a second row beside its resolved one"). The ghost is exactly the defect FL1 exists to close.
- The test row `test_manifest_put_assertion_line.py:308` uses `test_plain` (no rename), so this path is never reached.
- Fix: when a re-asked stored row is renamed, retract its old spelling in the same fragment (e.g. `retracted_instances`). Add one table row with a parametrised id.

**A3 (fix-before-merge): the E1 reason is lost when the collect call raises.** Location: `stamp_node_ids` :974-1019. `asks` is assigned before `node_ids.check_request` runs, so the `except` branch's `cannot("<Exc>: msg")` result is overwritten by the `if asks:` block (`checked == {}`). Every row gets "pytest gave no answer".
- Probe: `check_request` patched to raise `RuntimeError("collect exploded")` prints `{'status': 'not_verified', 'note': 'pytest gave no answer'}`.
- The spec (item 2c, E1) says the reason must be `"<ExcType>: <message>"`. The status is still right.
- Fix: enter the reading block only when the call returned, e.g. `if asks and checked`. Add an E1 row for an exception raised by the call.

**A4 (fix-before-merge): a judge-resolved id is marked `verified` while the stored spelling joins nothing.** `match` passes `missing` through `judge_form.resolve_missing` (node_ids.py `_judged`). The judge reads the project from the cwd. With `judge.provider: typesafe` and `mode: on`, the judge can move a typo `test_logn` to `tests/a.py::test_login`. The verified branch (:1021-1040) replaces only the parameter part. So it keeps `test_logn` and stamps it `verified`.
- Probe: `test_logn {'status': 'verified', 'note': 'pytest collects test_logn as test_login'}`.
- This violates the card's error direction ("never verified without a collected match", for the stored spelling). The default config (judge off) does not reach it.
- Fix: when the resolved base's last segment differs from the typed base, rewrite the function part too, or treat it as `missing`. The spec was silent here. The safe side is: never `verified` for a spelling that does not join.

**A5 (fix-before-merge, Q7): one function is too long.** `stamp_node_ids` is about 140 lines (:919-1058) and nests 4 levels in the ask block. `import node_ids` is repeated inside loop branches (:1024, :1048). `file.strip().replace("\\","/")` is computed three times. Fix: split it into map / eligible / ask / read helpers.

**Notes.**
- (n1) The report's `owns-skip` lists `slices/qa-failure-analyst/index.md`, but the final diff no longer touches that file. The slice files outside owns (`handoff-keys-2.md`, `index.md` ×2) come from `contract_slices.py --write`. The card said to stop if this happened. Accepting it is the Lead's call.
- (n2) The `### Typed ids` sentence leaves out "the field is the code's" (item 5). E10 drops a role-sent mark anyway, so this is not blocking.
- (n3) Q6: the third reader of `execution.node_id_collect_timeout_s` coerces values differently from `run_suite._setting` (:1456, :1731 `int(...)`, which crashes on a non-number). The card's C4 allowed "read like". Converging them belongs to RD1-35 or the Lead.

Witness gap: the builder did not re-run test_stage_joints or test_judgment_census after the final edits, and left several walk files unrun. The Lead-measured canon 44204086316 covers them (its reds are main's only: shard 1 `test_probe_by_code.py` timeout). That gap is not a finding.

### (A) standing questions
- Q1 fit: items 1-5 are implemented. Deviations: A2, A3, A4. The census row was dropped because C1 refused it ("no such check unit"). The joint's roles were widened to qa-code-critic because K5 required it. Both are justified.
- Q2: the `words` callable (E12 decided in `run`) points the safe way.
- Q3 seams: additive.
- Q4 class: the class step lives in the survivor, so `run_suite` and `red_sandbox` inherit it. The writer road is RD1-35 (exists, batch-1-phase-2.md:63). F6's universality node does not exist yet: Grep `-i -E "node.?id"` over `plans/piles/universality` returns 0 hits, though the pile itself is present. Q12(d) residual: the Lead must open it before accepting. SIBLING_MAP axis 39 (F8) is not on main yet; it is the Lead's, with the acceptance commit.
- Q5 tests: (a) the class rows i-vii would catch the defect. (c) A2 and A3 have no row. Budget: 184 test lines against 239 product lines, within the rule. The builder's `tests-over:` line is unneeded (rule 20 note).
- Q6: see n3.
- Q7: A5.
- Q8: the package text is English.
- Q9 ratchets: s5.json gets a `raised_by` line `unwalked | joints/manifest_put:node_id | RD1-19, 2026-11-17` (named). `role-load.json` is untouched. The K1 pin goes 285 -> 286, named.
- Q10: AR-13/15/22/28/29 are named. VARIETY: a runner with no checker gets `not_verified` plus a printed line. No block, no silent default.
- Q11 judgment: none moved. The refusal is a sourced id-to-collect join.
- Q12: one road (`node_ids`). The residual is F6 (see Q4).

### (A) merge conflicts expected
- With current main the trial merge is clean. On the merged tree: A22 qa-automator 25,697 tokens (2 tokens of slack), failure-analyst 21,659 = its ratchet, `role_rules` 0 findings, slices fresh, `test_role_load` 186/186, `dry_exits` 0 discrepancies.
- PC4-19 stream A, if it lands first, splits `test_stage_joints.py`. That gives a modify/delete conflict on the K1 pin line, which moves to `test_stage_joints_k1_k8.py`.
- RD1-34 touches the same `stage-joints.json`, K1 pin and `s5.json` ratchet. The later node sets the sum.
- Any main change that adds to qa-automator's load before FL1 lands turns A22 red.

---

## (B) PC4-19 stream B: findings

**Split check, done by script, not by reading** (`pcv_check.py` over origin/main's old file against the 8 new files):
- 119 old top-level names. LOST: none. DOUBLED: only `main` (one per part plus the shim).
- Source changed: only `main`. Every other name sits in exactly one file, byte-identical.
- New names: `mutations_flow`, `records_flow`, `two_profiles_flow` (each AST-identical to the old inline block of `main`), plus the shim's `PARTS`/`__all__`.
- Check calls: old 524 (523 plus 1 `finish`), new 529 (523 plus 6 `finish`).
- Run list: 14 entries in the old order (6 bindings, mutations, receipt, records, two_profiles, 4 exit_order).
- pyflakes: 0 undefined names in all 8 files (positive control: a planted `nope` is reported).
- Importers: all names of the 5 importers resolve through the shim (9/13/10/8/3 names, none missing). Only from-imports are used, so no module-attribute patching.

**B1 (blocker): a branch-only red, the `test_stage_joints.py` timeout. The evidence says it is not environmental.** Same-day canons, per-file seconds via `tools/ci_read.py artifact`:
- FL1 canon 44204086316 (main's sharding). Shard 1 holds `test_probe_by_code.py` and is the slow shard: story_sides 462.1, story_run_refusals 334.1, s0 314.7, probe_by_code timeout. Shard 2: stage_joints **187.3**, story_run_s6 197.8, dry_1 196.6, stand_identity 146.7.
- PC4-19 B canon 44202707023. The heavy parts mutations (71.8 s) and records (115.2 s) land in **shard 2**, and shard 2 becomes the slow one: stage_joints **300.2 timeout**, story_run_s6 332.2, dry_1 330.6, stand_identity 253.0. Shard 1 gets faster: story_sides 287.0, refusals 217.1, s0 198.2.
- So the slowdown follows the heavy probe-by-code work, not the runner. This branch moved it into stage_joints' shard.
- Cause: the shard balancer (`selftest.shard_files`, weights from `slow_tests.json`, default `fast_under_s/2` = 2.5 s) still weights the 0.7 s shim at 206.8 s and weights each part at 2.5 s. Real seconds: bindings 2.0, mutations 71.8, receipts 16.4, records 115.2, two_profiles 5.0, exit_order 7.2. That leaves about 190 s of real work unweighted in shard 2 and about 206 s of phantom weight in shard 1.
- The card puts the `slow_tests.json` rows in NC-19, "one push with the stream merges" (§4, E-6). B therefore cannot merge alone.
- Fix: in the same push, remove the old row and add the six parts (the measured canon seconds above are better than the line-share estimate). Re-run the canon on that combined head. If stage_joints is still near the cap, that is stream A's case.
- E-2 lines owed: records 115.2 s and mutations 71.8 s are over the 60 s target.

**B2 (fix-before-merge): the witness for the common module is narrower than the card allows.** Card §1/§4 say the 5 importer keep rows get `covers += tests/probe_by_code_common.py`. On this head they lack it (they still cover `tests/test_probe_by_code.py`).
- `scenario_walk.py --witness-for .../probe_by_code_common.py` prints the 6 parts and the shim only, not alternative/copy/languages_cli/languages_plan/languages_ts_playwright.
- Scenario: an edit to `env_for` in common breaks `test_probe_by_code_copy.py`, and the builder's witness never runs it.
- Fix: add the five covers. The builder now writes test-layers.json, so this belongs in the same commit or push.

**B3 (fix-before-merge): keep rows were written by hand, not by `split-keep` (AR-14, E-14).**
- The shim row keeps `layer data_join` and the old `why` ("AR-22/AR-28 join: the critic's red probe ... repinned here"). That describes a file that now holds no check (a label that lies, Q7).
- The six part rows copy the old covers (wider, which is safe) and carry no `keep-split:` commit line (62f1f823, d11be9de).
- Fix: regenerate the rows with `tools/test_quarantine.py split-keep test_probe_by_code.py --into <6> --shim`. If the Lead keeps the hand rows, at least set the shim's `why` to `split shim: ...`.

**Notes.**
- (n1) E-4: the builder did not audit exit_order. My AST scan: `main_exit_order_is_pinned` and `raw_bytes_through_manifest_from_tests` each call `use_project` themselves; `missing_facts...` works only through `run` (a child with explicit env); `through_real_run_suite` makes no in-process call. No entry breaks the rule.
- (n2) No CHANGELOG fragment (not in owns). The Lead adds it at integration.
- (n3) The builder wrote a `tests-over:` line (rule 20). This is a byte move, so the reason is the Lead's to give at merge.

### (B) standing questions
- Q1: §3.B keys hold: proof, 14 entries / 6 parts, shim with no check, importers resolve. B1 and B2 come from §4 rows the builder only partly took on.
- Q3: additive.
- Q4: streams A and D are their own nodes.
- Q5: `test: none -- byte move` is correct.
- Q6: none found. pyflakes is clean, and the 36 common names are not redefined in parts (DOUBLED = main only).
- Q7: B3 (shim `why`).
- Q8: OK.
- Q9: no `TEST_TIMEOUTS` row. `slow_tests.json` is unchanged, which is B1.
- Q10: AR-14 bypassed (B3). AR-20 kept. AR-22 shim. VARIETY n/a (package tests).
- Q11: none.
- Q12: one road, `test_split.py`.

### (B) merge conflicts expected
- With current main the trial merge is clean (test-layers.json and features.json auto-merged; the merged JSON parses).
- No file overlap with FL1 (`comm` of the two name lists is empty).
- Later conflicts: NC-19 (`slow_tests.json`, the importer covers), PC4-14/PC4-13, which are re-pointed to the parts, and stream A on `slow_tests.json`.

---

## Trail
- Read: both cards (FL1 whole; PC4 :1-395), both builder reports, both diffs (`--stat` first). FL1 `manifest_put.py` :10-37, :220-237, :335-357, :660-682, :869-1072, :2082-2240, :2820-2840. `node_ids.py` :540-720. `judge.py` :100-140. `judge_form.py` :101-130. `contract.py` :4075-4105. `validate_artifacts.py` :2345-2362. `role_rules.py` header. `role-rules.json` (grep). `run_suite.py` :1456-1464. FL1 tests :290-335. The PC4 shim (whole) and the part runners (AST). `test-layers.json` probe rows (script). `selftest.py` :868-935.
- Reruns (FL1 head): `role_rules.py --check` → `457 rows, 546 carriers checked, 0 finding(s)`. `contract_slices.py --check` → `44 declared, all present and fresh`. `test_role_load.py` → `186/186 ok`. `audit_factory.py` → `A22 role start load: no violations ... Result: clean` (qa-automator ~25,697).
- Reruns (FL1 head + main): the same four, all green. `dry_exits.py --check` → `0 discrepancies`.
- Probes: `merge` two rows (A2); E1 raise (A3); judge shape (A4). Outputs are quoted above.
- PC4: `pcv_check.py` (split), the lifted-flow AST compare, importer names, pyflakes plus a negative control. `scenario_walk --witness-for common` → 6 parts + shim. Shard simulation. `ci_read.py artifact` on 44202707023 and 44204086316, both shards.

```json
{
  "verdict": "blocker",
  "blockers": [
    "FL1 A1: references/artifact-contract-automation.md cut removed the self_fixes example key evidence (main :19), the only role-read carrier of a key validate_artifacts.py:2356 check_self_fixes refuses without",
    "PC4-19 B B1: branch-only red test_stage_joints.py timeout 300.2 s; canon evidence ties it to the heavy probe parts (mutations 71.8 s, records 115.2 s) landing in stage_joints' shard because slow_tests.json still weights the shim 206.8 s and the parts at the 2.5 s default; slow_tests rows must land in the same push (card par.4 NC-19) and the canon re-run"
  ],
  "fixes": [
    "FL1 A2 manifest_put.py:954-966,1031-1035 - FR-40 re-ask with a param rewrite leaves the stored not_verified row beside the new one; retract the old spelling, add a table row",
    "FL1 A3 manifest_put.py:974-1019 - an exception from check_request/runner_form is overwritten by 'pytest gave no answer'; keep the ExcType: message reason",
    "FL1 A4 manifest_put.py:1021-1040 - a judge-resolved other function is stamped verified under the typed spelling; rewrite the function part or treat as missing",
    "FL1 A5 manifest_put.py:919-1058 - stamp_node_ids ~140 lines, 4 nesting levels; split",
    "PC4-19 B B2 test-layers.json - the 5 importer keep rows lack covers tests/probe_by_code_common.py; witness-for common misses them",
    "PC4-19 B B3 test-layers.json - rows hand-written, not by split-keep; shim row keeps the old data_join why of a file with no check"
  ],
  "class_completeness": "FL1: class step fixed in the survivor node_ids.match, inherited by run_suite and red_sandbox; writer road is RD1-35 (exists); F6 universality node for non-pytest checkers not yet opened (Lead, Q12 d); SIBLING_MAP axis 39 pending with the Lead's acceptance commit. PC4-19 B: every old top-level name in exactly one file, byte-identical; sibling streams A and D are their own nodes; NC-19 registry rows (slow_tests, importer covers) are the open class remainder.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-rd1-19-fl1-pytest-id-card.md",
      "docs/tasks/specs/20261117-pc4-19-tests-near-300s-card.md",
      "docs/tasks/specs/reports/20261117-rd1-19-fl1-report.md",
      "docs/tasks/specs/reports/t-1259-pc4-19-b.md",
      "ai-packages/qa-factory/scripts/manifest_put.py",
      "ai-packages/qa-factory/scripts/node_ids.py",
      "ai-packages/qa-factory/scripts/judge.py",
      "ai-packages/qa-factory/scripts/judge_form.py",
      "ai-packages/qa-factory/scripts/validate_artifacts.py",
      "ai-packages/qa-factory/scripts/selftest.py",
      "ai-packages/qa-factory/references/artifact-contract-automation.md",
      "ai-packages/qa-factory/scripts/tests/test_manifest_put_assertion_line.py",
      "ai-packages/qa-factory/scripts/tests/test_probe_by_code.py",
      "ai-packages/qa-factory/scripts/tests/test-layers.json"
    ],
    "reruns": [
      {"command": "python -B scripts/role_rules.py --check (FL1 head and FL1+main)", "result": "457 rows, 546 carriers checked, 0 finding(s)"},
      {"command": "python -B scripts/contract_slices.py --check (FL1 head and FL1+main)", "result": "slices: 44 declared, all present and fresh"},
      {"command": "python -B scripts/tests/test_role_load.py (FL1 head and FL1+main)", "result": "186/186 ok"},
      {"command": "python -B scripts/audit_factory.py (FL1 head and FL1+main)", "result": "A22 role start load: no violations; Result: clean; qa-automator ~25,697 tokens"},
      {"command": "python -B scripts/tests/dry_exits.py --check (FL1+main)", "result": "0 discrepancies"},
      {"command": "probe merge(): stored test_x[eu] not_verified + fragment test_x[chromium-eu]", "result": "two rows: test_x[eu] not_verified, test_x[chromium-eu] verified"},
      {"command": "probe stamp_node_ids with check_request raising RuntimeError", "result": "note 'pytest gave no answer' (reason lost)"},
      {"command": "probe stamp_node_ids with a judge-shaped resolved answer test_logn -> test_login", "result": "test_logn stamped verified"},
      {"command": "pcv_check.py old test_probe_by_code.py vs 8 split files", "result": "LOST none; DOUBLED main only; checks 523+1 finish vs 523+6 finish; 14 run-list entries in order"},
      {"command": "python -m pyflakes on the 8 split files (+ negative control)", "result": "0 undefined names; control reported"},
      {"command": "scenario_walk.py --witness-for scripts/tests/probe_by_code_common.py (PC4 head)", "result": "6 parts + shim; no importer row"},
      {"command": "tools/ci_read.py artifact 44202707023 and 44204086316, both shards", "result": "B: shard 2 stage_joints 300.2 timeout, s6 332.2, mutations 71.8, records 115.2; FL1: shard 2 stage_joints 187.3, s6 197.8; probe_by_code shard 1"}
    ]
  }
}
```
