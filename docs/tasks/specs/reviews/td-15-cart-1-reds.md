# td-15 story cart-1: judging the five red facets D1..D5

Critic (Opus), 2026-11-11. Read-only work in `D:/ws1/wt-td\15-5-2` (branch td/15-5-2, HEAD 761b1525f). I did not run the
scenario test file and did not run a selftest. I ran narrow probes in-process against the walker's own functions, on throwaway worlds.

## Verdict lines

- **D1: (a)** — G2-12 (commit e6e6fee19, 31.10.2026 18:50 +0100, shipped in 0.10.8) makes a code-sourced `derived` row owe a behaviour claim. The
  recorded register is byte-identical to the one S2 accepted at 01:05 UTC on 31.10, about 17 hours before the rule existed. It is older
  than the rule, but its `created` day equals `UNCONFIRMED_SOURCE_CUTOFF`, so it gets judged under the new rule. Needs an amendment row.
  Separately, a walker artifact (W2) adds an `UNREADABLE` line to the same facet.
- **D2: (a)** — the S3 register fence (GW1-41/G2-15, commit 08bf2fd65, 01.11.2026) and the `## Recommended regression` form check
  (RG1-2, commit 798de744d, 01.11.2026) both came in with 0.10.8, after the run. The 0.10.6 plan's `## Not planned` list is, on purpose,
  no longer accepted in place of a row. There is no process trap. Needs an amendment row. The W2 walker artifact also shows up on this facet.
- **D3: (c)** — the walker world's project `config.json` is the shipped template, where `case_id_form` is `""`. As a result
  `CART-1_TC_001..010` are not case ids at all, and every automated case "appears in no lane". With the recorded project config
  (`{ticket}_TC_{nnn}`) all ten are accounted for and the S6 exit accepts.
- **D4: (c)** — `check_coverage.py` sits on the S8 path unchanged since 0.10.6. With the template config, `cases_root` is `""` and it
  counts the task's own `work/test-cases`. The recorded project had `cases_root: test-cases`, so it read a project-level case store.
  Both that store and `qa-factory/records/coverage-map.md` (written by the scribe's `check_coverage.py --write`) live outside the task
  root.
- **D5: (c)** — the cause is the same template `case_id_form` as D3. `critic_rollcall.parse_rollcall` reads no case ids from the
  roll-call, so the critic's round "does not name" TC_005/006/008/009. With the recorded config (and the case-config memo reset), the
  gate A decision road returns `approve`.

Package bugs found: **0**. The walker/capture changes are below.

---

## D1 — S2 accepted: "R-3 is implementation-only and has no behaviour claim"

**Class (a), a deliberate contract change. The recorded artifact is older than the rule.**

Evidence:
- The refusal comes from `scripts/validate_artifacts.py:682-689`, `check_behaviour_claims`, over `contract.claim_required_requirements`
  (`scripts/contract.py:1428-1435`). For a register whose `created` is on or after `UNCONFIRMED_SOURCE_CUTOFF = "2026-10-31"`
  (`contract.py:1347`), it also lists `code_sourced_requirements` (`contract.py:1393-1412`): a `derived` row with no `ac_ref`, an
  all-silent matrix and an `observable` starting with `current-code:`.
- Which commit introduced it: `git log -S"UNCONFIRMED_SOURCE_CUTOFF = " -- ai-packages/qa-factory/scripts/contract.py` returns only
  `e6e6fee19 2026-10-31 18:50:26 +0100 package: G2-12 code and somebody else's test are no source of a requirement (t-547)`.
  `git merge-base --is-ancestor e6e6fee19 811f31dd5` (811f31dd5 = "release 0.10.6", 2026-10-30) gives NOT an ancestor. The same
  command against 658ceac29 ("release 0.10.8") gives an ancestor.
  - Positive control, same grep form: `git show 811f31dd5:.../contract.py | grep -c UNCONFIRMED_SOURCE_CUTOFF` gives `0`; on `HEAD` it
    gives `5`.
  - CHANGELOG 0.10.8, line 761: "code and somebody else's test are no source of a requirement (`contract.unconfirmed_requirements`,
    G2-12, P20)".
- The run's own version: `state/controller.json` `"package_version": "0.10.6"`, `pipeline.json` `"plugin_version": "0.10.6"`.
- The register on file is the one S2 accepted. `sha256sum work/requirements-register.md` gives
  `2fb296c4...a725`, which equals the `evidence_refs` sha256 of events seq 11 (`accept:S2-qa-requirements-tester-1`). That event's
  `created_at` is 1793408751.88, i.e. 2026-10-31 01:05:51 UTC, before the rule's commit at 17:50 UTC the same day.
- The register's front matter has `created: 2026-10-31`. Since `_created_since` compares `>=` against the cutoff (`contract.py:1362`),
  this register falls inside the rule.
- The rule's comment states the intent: "a register written before it keeps the narrower reading it was written under (FR-14, a
  story in flight is not turned red)", at `contract.py:1344-1346`. It also states the chosen error direction: "toward the new reading,
  which only costs a question" (`contract.py:1354`). Day granularity cannot separate the morning of the commit day from its evening;
  that is a stated design choice, not a regression. I do not file it as a bug. It is a note only: the cutoff day is the commit day,
  and no released package had the rule before 01.11.
- The refusal is wider than the builder's report says. Re-run of the S2 exit door (below) lists NINE rows: R-3, R-6, R-7, R-9, R-10,
  R-12, R-13, R-14, R-15. Every `derived` + `current-code:` + all-silent row is in that list. R-4 (`ok:` cell), R-5 and R-8
  (`expected-contract:`) and R-16 (`none`) are rightly out.
- The same door also prints `branch_accounting.py: unreadable - branch_accounting could not tell which stage of the story is running`.
  That line is a walker artifact (W2 below), not part of the contract change.

Proposed amendment row (one line, `expected.json` `amendments`):
```
{"stage": "S2", "field": "outcome", "recorded": "accepted (0.10.6, events seq 11)", "expected": "refused: implementation-only requirements without a behaviour claim (R-3, R-6, R-7, R-9, R-10, R-12, R-13, R-14, R-15)", "why": "contract change G2-12 (e6e6fee19, 31.10.2026 18:50 +0100, shipped 0.10.8): a code-sourced derived row owes a behaviour claim; the register was accepted at 01:05 UTC the same day and its created equals UNCONFIRMED_SOURCE_CUTOFF", "ref": "docs/tasks/specs/reviews/td-15-cart-1-reds.md", "accepted_by": "Lead, <date>"}
```
Write it only after W2. Otherwise a bare `refused` outcome would also absorb the walker's `UNREADABLE` line.

## D2 — S3 accepted: "R-9: this requirement of the register has no row in the test plan"

**Class (a), a deliberate contract change. The recorded artifact is older than the rule.**

Evidence:
- The refusal is built in `scripts/planning_contract.py:3825-3833` (`fence_lines`) from `register_fence` (`planning_contract.py:3771-3817`)
  and `requirements_without_row` (`planning_contract.py:509-533`). It runs at the S3 exit only, at `planning_contract.py:4357`. The
  refusal text itself says "A `not_planned` entry does not stand in for a row."
- Which commits introduced it:
  - `git log -S"def register_fence(" -- .../planning_contract.py` gives
    `08bf2fd65 2026-11-01 01:03:59 +0100 qa-factory: GW1-41 + G2-15 partial -- register fence at the S3 exit, candidate defects reach plan and briefs`.
    It is not an ancestor of 811f31dd5 (0.10.6), and it is an ancestor of 658ceac29 (0.10.8).
  - Positive control, same form: `git show 811f31dd5:.../planning_contract.py | grep -c "def register_fence("` gives `0`; on HEAD, `1`.
  - CHANGELOG 0.10.8, line 921: "The S3 exit now fences the register: every id of `## Register` must reach a row of
    `work/test-plan.json` and the `R` column of `test-plan.md`; a `not_planned` entry no longer stands in for a row."
- The full refusal set is wider than the builder quoted. Re-run of the S3 exit door (below):
  - the fence: R-9, R-13 and R-16 have no plan row, and R-13 (`bug:candidate-defect`) has no planned test;
  - the `## Recommended regression` form: "The section names no test and no `No regression: <reason>` line"
    (`scripts/regression_scope.py:150`). That comes from `798de744d 2026-11-01 01:59:41 +0100 t-609: RG1-2, RG1-1, RG1-3, RG1-4 -- the plan's
    Recommended regression has one checked form`. It is not in 0.10.6 and it is in 0.10.8; CHANGELOG 0.10.8, line 1318, describes it;
  - plus the W2 walker artifact (`branch_accounting.py: unreadable ...`).
- What the run did: `work/test-plan.json` has 12 rows (TS-1..TS-12), none naming R-9, R-13 or R-16. `test-plan.md` `## Not planned`
  lists "R-9 ... Q2", "R-13 ... Q3", "R-16 ... Q4".

**On the builder's process-trap remark: no trap.** Today's S3 exit does not ask for a case at S3. It asks for a ROW, and the refusal
names three forms for that row (`planning_contract.py:3829-3833`):
1. `disposition: unverifiable` with `question_refs: ["Q2"]` and `if_answered["Q2"]` carrying a key per reading letter (or `*`) plus
   `not_needed`;
2. or `disposition: skip` with a reason, which the person sees at gate A.

The person's later "R-9, R-13, R-16 stay without cases" is exactly the `not_needed` / `skip` branch of such a row. The demand at S3 is
therefore "say at S3 what each answer would do", which can be waived later through that same row.

For the candidate defect R-13, `candidates_without_row` (`planning_contract.py:560-595`) wants one reading that sets `automate` or
`manual-agent`. That is still a planned branch, not a written case, and another reading can be `not_needed`.

Did the run carry a recorded reason that today's gate fails to read? It carried prose under `## Not planned` naming Q2/Q3/Q4. Today's
gate does not read that on purpose (refusal text and CHANGELOG line 921 above), so this is not a reader defect. A plain-text list also
gives gate A no row to change when the answer comes, which is the stated reason for the fence ("a question's answer would have no row to
change", `planning_contract.py:3826-3827`).

Caveat: `test-plan.md` and `work/test-plan.json` on file are NOT the bytes S3 accepted.
- The S3 accept (seq 16) has `test-plan.md` sha256 `1aca670d...`, while the file on disk hashes to `90d7f53f...`.
- The S3 accept has `work/test-plan.json` sha256 `1f36712b...`, while the file on disk hashes to `4a3ed298...`.
- The cause is the case appendix added at S4, the code stamps and the capture's scrub.
- The refusals above depend on rows the S3 author wrote (12 rows, the `## Not planned` list, the regression section), which later
  stages do not add to. I judge the class on that basis, but the S3 facet is walked on post-S3 bytes; see W4.

Proposed amendment row:
```
{"stage": "S3", "field": "outcome", "recorded": "accepted (0.10.6, events seq 16)", "expected": "refused: register fence (R-9, R-13, R-16 have no plan row; candidate defect R-13 has no planned test) and the Recommended regression form (no Command: line)", "why": "contract changes GW1-41/G2-15 (08bf2fd65) and RG1-2 (798de744d), both 01.11.2026, shipped 0.10.8; the 0.10.6 plan's ## Not planned list is deliberately no longer a row", "ref": "docs/tasks/specs/reviews/td-15-cart-1-reds.md", "accepted_by": "Lead, <date>"}
```
As with D1, write it only after W2.

## D3 — S6 accepted: "CART-1_TC_001 is automated at S5 but appears in no lane of this report"

**Class (c), an artifact of the walker's world: the project config is not carried.**

Evidence:
- The refusal is at `scripts/validate_artifacts.py:2051-2061` (`check_run_report_coverage`). It looks lanes up through
  `contract.run_results` (`contract.py:4272-4311`) and `names_case`, and both rest on `case_ids` in the project's `case_id_form`
  (`contract.py:4091-4104`).
- The walker's world: `scenario_walk.build_world` creates the project through `harness.mark_project`
  (`scripts/tests/harness.py:208-227`), which writes the shipped template. In that template,
  `references/templates/config.json:13` reads `"case_id_form": ""`, so only `TC-{nnn}` is recognised.
- The recorded project config: base64-decoding `state/config-at-start.json` gives `case_id_form "{ticket}_TC_{nnn}"` and
  `cases_root 'test-cases'`.
- Probe:
  ```
  python -B -c "... C.run_results(report, cfg=cfg); names_case(...) for CART-1_TC_001..012"
  {'case_id_form': ''} missing: ['CART-1_TC_001', ..., 'CART-1_TC_010']
  {'case_id_form': '{ticket}_TC_{nnn}'} missing: []
  ```
  With the default config, `C.case_ids('CART-1_TC_001')` gives `[]`.
- Through the real door: the S6 `exit_gate` door, on a world carrying the recorded config (cache reset), prints `== S6 accepted`
  (rerun 3 below).
- What the walker must provide: the recorded project `config.json`. See W1.

## D4 — S8 accepted: "records/coverage-map.md is missing"

**Class (c): a project-level record plus the project config and the project case store, all outside the task root.**

Evidence:
- The refusal is at `scripts/check_coverage.py:251-255`. It is wired as the qa-doc-scribe detector at `references/stages.json:285-288`.
- It is not a contract change. At 0.10.6, `git show 811f31dd5:.../references/stages.json | grep -n check_coverage` gives line 274, and
  `git show 811f31dd5:.../check_coverage.py | grep -c "map was never built"` gives `1`. The same detector and the same refusal existed
  when the run was accepted.
- Why today's run refuses where the recorded one passed: `case_paths` / `collect_cases` read `config.cases_root`
  (`check_coverage.py:92-111`).
  - The template has `"cases_root": ""` (`references/templates/config.json:11`), so the walker world counts the task's own
    `work/test-cases/cart/*.md`.
  - The recorded project had `cases_root: test-cases`. The cases lived in the PROJECT store: `state/story-case-links.json`
    `store_provenance.source_path` reads `"test-cases/cart/CART-1_TC_001.md"`, relative to the project.
- Probe on two throwaway copies of the story under a scratch project:
  ```
  python -B .../check_coverage.py --root <scratch>/d4-rec   (recorded config bytes)
  OK: no local cases (<scratch>\d4-rec\test-cases is empty) - counter reconciliation not applicable    exit=0
  python -B .../check_coverage.py --root <scratch>/d4-tpl   (template config)
  REJECT - 1 problem(s): the map is stale: - cases exist (5 total), but ...\qa-factory\records\coverage-map.md is missing    exit=1
  ```
- The green under the recorded config is VACUOUS: the project store `test-cases/` was not captured. The real run's green came from the
  real store plus the map in project `records/`.
- The S8 brief tells the scribe to write that map: `work/briefs/S8-qa-doc-scribe-1.md:23` reads "check_coverage.py --write - regenerates
  the coverage map".
- The builder's claim "the 0.10.6 run never built a map" is NOT established. The brief prescribes `--write`, and the source path is not
  kept, so the slice can neither confirm nor refute it. It is not load-bearing for the class: in both readings the record lives outside
  the task root.
- What the walker/capture must provide: see W1 and W3. Once the recorded config is carried, a bare S8 green is no evidence until the
  store is carried too.

## D5 — gate A decision: "plan row TS-5: independent accepted design review bound to this revision is missing"

**Class (c), the same walker-world artifact as D3. It is not the capture's hash recomputation.**

Evidence:
- The builder truncated the refusal. The full text, from rerun 4: "plan row TS-5: ... gate A cannot read an approving word of the
  case critic for this row (round of dispatch S4-qa-case-critic-2: its roll-call does not name CART-1_TC_005)". The same refusal
  appears for TS-6, TS-8 and TS-9.
- It comes from `scripts/controller.py:3453` (`_dispatch_review_verdict`, the "no_review" basis), via `controller.py:2894-2914` and
  `2966-2968`.
- The roll-call DOES name those cases: `work/test-cases/critic-findings.md`, Round 2, contains rows such as
  `| TS-5 | CART-1_TC_005 | yes | approve |`.
- The receipt is intact: `sha256sum work/test-cases/critic-findings.md` gives `97f54ac5...ab7a`, which equals the evidence ref of events
  seq 32 (`S4-qa-case-critic-2`). The capture did not change that file, and it is not in the README "changed" list.
- `critic_rollcall.parse_rollcall` reads ids through `C.case_ids(..., cfg=C.case_config(artifacts))` (`scripts/critic_rollcall.py:111-125`).
  Probe of `scoped_verdict` on the recorded bytes:
  ```
  tpl cfg form= ''                    -> ('', set()) []
  rec cfg form= '{ticket}_TC_{nnn}'   -> ('accepted', {'CART-1_TC_005', 'CART-1_TC_009'}) []
  ```
- The whole door, `scenario_walk.door_decision` on a cut copy (seq < 34):
  - template config gives `refused` with the four TS rows above;
  - recorded config written into the world before `copy_world`, plus `contract.case_config_reset()`, gives `== recorded+reset approve`.
  - Note: my first try wrote the config only AFTER `copy_world` and did not reset the case-config memo (`contract.py:3164-3234`, a
    per-anchor resolution window). It still refused, because the memo resolved during `_reproject` was reused. W1 must write the
    config before the world is first projected, or reset the memo.
- Not a contract change: the "roll-call does not name" reason dates from CX1-12 (5311ae6c2 / 8ac5f303f / a50ab5153, 20.10.2026), and
  `git show 811f31dd5:.../controller.py | grep -c "roll-call does not name"` gives `2`, so it was already in 0.10.6.
- Not the capture's gate-A binding recomputation: the receipt and pins hold. Only the case-id form is missing.

---

## What to do

### Amendment rows to write (in `fixtures/stories/cart-1/expected.json` `amendments`; owner of the decision: Lead)
1. D1: the S2 row quoted under D1, recorded `accepted`, expected `refused` (G2-12, e6e6fee19).
2. D2: the S3 row quoted under D2, recorded `accepted`, expected `refused` (fence 08bf2fd65 + RG1-2 798de744d).

Both only AFTER W2. Until then each facet carries the walker's own `UNREADABLE` refusal too, and a bare `refused` would hide it.

### Bugs to file (factory class)
- None in the package. All five reds are either contract changes made after 0.10.6 (D1, D2) or the walker's world (D3, D4, D5).
- Not filed, noted: G2-12's day cutoff equals the commit day, so a register created earlier that same day is read under the new rule.
  The rule declares this direction deliberately (`contract.py:1354`).

### Walker / capture changes (scenario layer, TD-15)
- **W1, the project config of the recorded run reaches the world.** `build_world` / `copy_world` write the decoded
  `state/config-at-start.json` bytes as `<tmp>/project/qa-factory/config.json`, falling back to the template when the story has none.
  - Write it BEFORE `_reproject`, or call `contract.case_config_reset()` after writing. The case-config memo otherwise keeps the
    template reading.
  - Fixes D3 and D5 (both proven green above).
  - The class: any story whose project uses a non-default `case_id_form`, `cases_root` or other project key. The builder's
    "Analogs noticed" names the `records/` half of it.
  - The capture should keep this file, or note when the config in force at a stage differed from the one at start: the
    config-at-start `outcome.why` says the revert was skipped because another story (ADD-TO-CART) was in flight.
- **W2, the exit door names the stage and the dispatch it judges, as `story_step finish` does.** `door_exit_gate` calls
  `exit_gate.all_errors` bare (`scripts/tests/scenario_walk.py:220-221`). It should wrap the call in
  `exit_gate.holding_stage(entry["stage"])` and `exit_gate.holding_dispatch(<the stage's accepted dispatch>)` (`exit_gate.py:467-502`).
  - On the final world every stage is `done` (`pipeline.json`), so `branch_accounting._running_stage` (`branch_accounting.py:2000-2015`)
    finds no running stage and prints the `UNREADABLE` line seen on S2 and S3.
  - Alternatively, walk the exit door on a copy cut before the stage's accept seq.
- **W3, D4 / project-level records.** Either:
  - capture the project case store files named by `store_provenance.source_path` of `state/story-case-links.json`, and in the world
    run the scribe's recorded step (`check_coverage.write_map`) before the S8 door, so the map is a real projection of carried
    cases; or
  - declare the coverage part of `cart-1/S8/accepted` not walkable: `not_walked` with "the project case store `test-cases/` and
    `qa-factory/records/coverage-map.md` are project-level, outside the task root; the capture cannot carry them".
  - With W1 alone, S8 turns green VACUOUSLY ("no local cases"). That must not count as coverage.
- **W4, re-walk the eight green facets after W1.** Under the template config every `{ticket}_TC_{nnn}` id is invisible, so case-keyed
  checks on S4, S5 and S9 may have passed with nothing to check.
  - My recorded-config rerun covered only S2, S3, S6 and S8.
  - Also note: the S3 facet is walked on post-S3 bytes of the plan (hashes differ from the seq 16 receipt). Spec A.3 accepts the last
    output of the stage's single writer, but here S4 and code wrote into the same files.
- **W5, story data.** `story.json` says `"package_version": "0.10.9"`, while the recorded run is 0.10.6 (`state/controller.json`,
  `pipeline.json`). Correct the field.
- **The builder's report:** D1 lists one row where the door refuses nine. D2 quotes one refusal where the facet carries five, plus
  the regression form and the W2 line. D5 is truncated before its cause. D4's "never built a map" is not established. These are
  NEEDS-WORK findings on the report, per rule 7: the refusal text has to be quoted whole.

## Trail

Files read:
- `docs/tasks/specs/reports/td-15-5-2-report.md` (lines 21-86)
- `docs/tasks/specs/td-15-scenarios-quarantine.md` (lines 150-239)
- `scripts/validate_artifacts.py` (630-692, 1994-2066)
- `scripts/contract.py` (1225-1449, 2860-2960, 3164-3291, 4040-4359)
- `scripts/planning_contract.py` (495-605, 3760-3850, 4330-4375)
- `scripts/check_coverage.py` (1-130, 195-274)
- `scripts/controller.py` (2850-2973, 3360-3480)
- `scripts/critic_rollcall.py` (89-138, 305-380)
- `scripts/branch_accounting.py` (2000-2099)
- `scripts/exit_gate.py` (462-528)
- `scripts/regression_scope.py` (120-160)
- `scripts/tests/scenario_walk.py` (105-160, 200-280)
- `scripts/tests/harness.py` (208-227)
- `references/templates/config.json` (lines 11, 13)
- `references/stages.json` (285-288)
- CHANGELOG headings and lines 742, 761, 921, 1318
- story `cart-1`: `README.txt`, `story.json`, `expected.json`, `work/requirements-register.md`, `test-plan.md`, `work/test-plan.json`,
  `work/run-report.json`, `work/automation-manifest.json`, `work/test-cases/critic-findings.md`, `state/events.jsonl` (seq 11, 16, 26,
  32, 34), `state/config-at-start.json` (decoded), `state/story-case-links.json`, `pipeline.json`, `work/briefs/S8-qa-doc-scribe-1.md`

Git:
- `git log -S` for `UNCONFIRMED_SOURCE_CUTOFF = `, `def register_fence(`, `roll-call does not name`, `The section names no test and no`,
  and the `## 0.10.6` / `## 0.10.8` headings
- `merge-base --is-ancestor` of e6e6fee19, 08bf2fd65 and 798de744d against 811f31dd5 (0.10.6) and 658ceac29 (0.10.8)
- `git show 811f31dd5:` greps, each with a HEAD positive control of the same form

Process notes:
- I copied the story twice into the session scratchpad for the D4 probe. Nothing in the repo was written apart from this file.
- One early Bash call carried a stray `cd` inside its subshell; it had no lasting effect, and the hook warned about it.

## Reruns (verbatim heads)

1. `python -B -c "...contract.run_results(report, cfg) / names_case..."`:
   - `{'case_id_form': ''} missing: [TC_001..TC_010]`
   - `{'case_id_form': '{ticket}_TC_{nnn}'} missing: []`
2. `check_coverage.py --root` on the scratch copies:
   - recorded config: `OK: no local cases (...\d4-rec\test-cases is empty)`, exit 0
   - template config: `REJECT ... coverage-map.md is missing - the map was never built`, exit 1
3. Walker doors in-process with the recorded config and `case_config_reset()`:
   - `== S2 refused` (9 x "is implementation-only and has no behaviour claim" + `branch_accounting.py: unreadable`)
   - `== S3 refused` (fence R-9/R-13/R-16 + candidate R-13 + regression form + `branch_accounting.py: unreadable`)
   - `== S6 accepted`
   - `== S8 accepted`
4. `scenario_walk.door_decision` gate A, cut before seq 34:
   - template config: `refused` (TS-5/6/8/9 "its roll-call does not name CART-1_TC_00n")
   - recorded config written after `copy_world` without a memo reset: still `refused` (the cache, see D5)
   - recorded config before `copy_world` + reset: `approve`
5. `critic_rollcall.scoped_verdict` on the recorded findings bytes:
   - template config: `('', set())`
   - recorded config: `('accepted', {'CART-1_TC_005','CART-1_TC_009'})`

## Standing questions (critic-diff-brief items 6-7)

- DUPLICATION AND CONSISTENCY: none found in the package for these five. The walker duplicates one road rather than reusing it: the
  `holding_stage`/`holding_dispatch` context that `story_step finish` sets (W2). Grepped: `holding_stage`, `DETECTOR_STAGE`,
  `scenario_walk.py` door functions.
- CODE QUALITY: none found in the package code read. The walker's world builder silently substitutes the template for the project
  config (W1). That is a fidelity defect of the test layer, not of the package.

```json
{"verdict": "fit_with_fixes", "blockers": [], "class_completeness": "D3/D5 class (project config not carried into the walker world) applies to every story with a non-default project key: W1 at build_world, the one survivor; D4 class (project-level records and case store outside the task root) is the builder's own analog, W3; W2 (the exit door does not hold the judged stage) applies to every exit_gate facet of every story; D1/D2 are per-story amendments, no sibling in the package to fix", "trail": {"read": ["docs/tasks/specs/reports/td-15-5-2-report.md", "docs/tasks/specs/td-15-scenarios-quarantine.md", "ai-packages/qa-factory/scripts/validate_artifacts.py", "ai-packages/qa-factory/scripts/contract.py", "ai-packages/qa-factory/scripts/planning_contract.py", "ai-packages/qa-factory/scripts/check_coverage.py", "ai-packages/qa-factory/scripts/controller.py", "ai-packages/qa-factory/scripts/critic_rollcall.py", "ai-packages/qa-factory/scripts/branch_accounting.py", "ai-packages/qa-factory/scripts/exit_gate.py", "ai-packages/qa-factory/scripts/regression_scope.py", "ai-packages/qa-factory/scripts/tests/scenario_walk.py", "ai-packages/qa-factory/scripts/tests/harness.py", "ai-packages/qa-factory/references/templates/config.json", "ai-packages/qa-factory/references/stages.json", "ai-packages/qa-factory/CHANGELOG.md", "ai-packages/qa-factory/scripts/tests/fixtures/stories/cart-1"], "reruns": [{"command": "contract.run_results + names_case with case_id_form '' vs '{ticket}_TC_{nnn}'", "result": "missing TC_001..TC_010 vs missing []"}, {"command": "check_coverage.py --root scratch copies (recorded vs template config)", "result": "OK no local cases exit 0 vs REJECT map missing exit 1"}, {"command": "scenario_walk door_exit_gate S2/S3/S6/S8 with recorded config + case_config_reset", "result": "S2 refused (9 rows G2-12 + branch_accounting unreadable), S3 refused (fence + regression form + unreadable), S6 accepted, S8 accepted"}, {"command": "scenario_walk door_decision gateA cut 34, template vs recorded config + reset", "result": "refused TS-5/6/8/9 roll-call does not name vs approve"}, {"command": "critic_rollcall.scoped_verdict on recorded findings bytes", "result": "('', set()) vs ('accepted', {CART-1_TC_005, CART-1_TC_009})"}]}, "fixes": ["W1: build_world/copy_world write the recorded project config (decoded config-at-start.json) before projecting, or reset the case-config memo", "W2: door_exit_gate holds the judged stage and dispatch (exit_gate.holding_stage/holding_dispatch) or walks a copy cut before the stage's accept", "W3: carry the project case store and regenerate the coverage map, or not_walked for the S8 coverage part", "W4: re-walk the eight green facets after W1", "W5: story.json package_version 0.10.6", "amendment rows for D1 (G2-12, e6e6fee19) and D2 (08bf2fd65 + 798de744d) after W2"]}
```
