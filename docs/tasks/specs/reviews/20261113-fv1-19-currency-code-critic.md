# FV1-19e binding currency: code critic (one pass for the topic, nodes C1 + C2)

Critic (opus), 13.11.2026. Diff: worktree `C:\QAFactory\forge-repo\.claude\worktrees\fv19-c2`, `git diff b3df35d..ec9c944`
(928cac6 C1, ec9c944 C2). Spec: `docs/tasks/specs/20261113-fv1-19-binding-currency-spec.md` (§1-§6, T1/T2/T3).
Paths below with prefix `S\` mean `<WT>\ai-packages\qa-factory\scripts\`.

## Verdict: NEEDS WORK (fit_with_fixes). 0 blocking findings, 5 fixes to make before merge (F1-F5)

The mechanism is correct. I traced it and re-ran it: one stamp writes the stamps, `merge` folds them key by key, and
`binding_currency` is the one reader for the projection, the precheck and the rename report. Every adversarial input reads as
"not current". No C2 edge depends on the dropped hash. The fixes are one wrong ratchet attribution (AR-20 record) plus four
small text and quality items.

## Answers by question

**1. DoD keys and edges.**
- C1: T1 r1-r17 are all present, in `test_manifest_put_merge.py`, `fv1_19e_binding_currency` (diff 928cac6 +1035..+1213).
  r2 is the defect row and r9 the F8 row. r8 uses the real `Stand.put` door and checks journal and tree unchanged (B22). T3
  rows t3-a..t3-e are in `test_obligation_join.py` §4/§4a; t3-a asserts the 80-character cut (B27). The `renamed_from` grep
  holds: only `contract.py`, `migrate_artifacts.py` and tests (report witness; my `judged_on` grep below shares the same
  shape). Census unchanged; my re-run gives 24/24. Edges B4-B12 and B20-B29 are each pinned by a row, or sit in code I traced:
  `S\contract.py:5491-5517` (step order 1→2→3→4a/4b→5 as the spec states) and `S\manifest_put.py:1943-1956` (materialization
  reads `old` before `dict(old, **binding)`, B23).
- C2: met, apart from F2-F4. T2 p1-p12 and p-proj are present (Q8). `design_assessment` in `window_record.py`: 0 hits
  (control: 3 in `coverage_contract.py`, same call). `obligation_hash` in `coverage_contract.py`/`s5_precheck.py`: Q3.
  `contract_slices --check`, `selftest --lang`, `test_role_load` and `test_judgment_census` are green on my re-run. One caveat:
  `test_role_load` is green only because of the ratchet rows (Q6). The changelog fragment names C1's refusals and the rename
  rows (N-7): yes, bullets 2 and 4.
- What the CI-only files could break (not run, per dispatch): (a) `test_scenario_local_1_*` replay fixtures whose bindings
  carry role-typed hashes and `design_assessment: sufficient` (`S\tests\fixtures\local1-manifest\manifest-run3.json`,
  `frag-4-b.json`). A replay that runs the S5 precheck on such a stored binding whose hash differs from the plan's now gets a
  `binding-stale-<oid>` finding in the `obligations` family. That family is PASSABLE, so a recorded word passes it, but a
  scenario that counts findings would change. (b) `test_controller_state`: it does not call `manifest_put` (grep `manifest_put|MP\.|\.put(`:
  0 hits). Its 24 `obligation_hash` uses are window-item hashes, so the stamp change cannot reach it. (c) `test_story_run_*`:
  no `obligation_bindings` in any of them (grep, positive control `test_controller_release.py` hit), so only the projection
  change could reach them, and a world-1 binding reads exactly as before.

**2. C1's dropped hash.** True: it changed no C2 edge, and no reader expects the dropped value. What changed: a sent binding
hash on an id the plan map lacks, or under an empty map, is now popped (`S\contract.py:5507`); before, it was stored as sent.
Readers of a binding's `obligation_hash` (grep -i over the scripts, every non-test hit read):
- `coverage_contract.py:281` and `:580` (through `binding_currency`) read only plan obligations' bindings.
- `s5_precheck.py:3885` reads only ids in `plan_map`.
- `migrate_artifacts.py:450` reads only the plan's ids.
- `acceptance.py:1189/1227` and `controller.py:7323` read WINDOW-ITEM hashes, not bindings.
- `probe_by_code.py:2854/4031` are row/record hashes.

So no reader ever reads the hash of a binding whose id the plan does not name. Code writers never send the hash
(`_forwardable` drops it; `red_sandbox.py:1863`, `probe_by_code.py:7545`, `window_record.py:1867` build fresh items).
`manifest_from_tests.py:1543` stamps a fragment that carries no `obligation_bindings`. Row (k)'s rewrite follows spec step 3.

**3. AR-13 / AR-15, one currency reader.** Confirmed for the readers. My search: Grep -i `obligation_hash` over the scripts
(positive control: the same call found 26 hits in `contract.py`), then `content_hash\(` over
`{coverage_contract,s5_precheck,migrate_artifacts}.py`. Every plan-hash comparison of a binding goes through
`C.binding_currency` (`coverage_contract.py:580`, `s5_precheck.py:3885`, `migrate_artifacts.py:450`). The leftovers are legitimate:
- `coverage_contract.py:281` compares the WINDOW ITEM's ref hash with the binding's hash, inside `witnessed_binding`. It joins
  the window to the binding; it does not read currency against the plan.
- `:734-756` is a manual record's own `obligation_hashes` map, a separate judgment carrier with its own currency (spec §0 item 5).

One more comparison the builder did not list: the writer's own `stored.get("obligation_hash") == want` in
`_binding_stamp_allowed` (`S\contract.py:5381`). It is a writer gate that the spec keeps ("today's rule", M1). It is not a reader.

**4. The `binding-stale-<oid>` finding.**
- FR-1 and AR-9: it says what is wrong (the fields, written against another text), what is expected (judge again and re-send)
  and gives a worked fragment.
- FR-2: the door is a usable command, but it prints a literal `<T>` although the task is known (F2).
- FR-46: it is the author's repair in the existing `obligations` family. The text names both causes.
- AR-18: it uses the same `_finding(...)` shape and the same family as the sibling unbound finding.

False refusal: not possible on a current binding. The stamp (`manifest_put.py:2445` → `C.plan_obligation_map`) and the
precheck (`s5_precheck.py:3857`) hash the same obligation from the same reader (`contract.py:5251` → `_plan_rows_of`), so a
binding stamped just now always equals the hash the precheck computes. The projection's own plan reader differs (B18, queued
Q-c), and the error there goes in the harmless direction.

Silence on a stale binding (AR-28): the finding is scoped to the dispatch's cases and to bindings whose instances overlap the
case aliases. A stale binding outside that scope still gets the existing unbound finding, and the projection counts it as
nothing. Dedup: my probe `probe_p9.py` gives `['TC-004'] -> 1 finding` alone and `['feedback-api/TC-003','TC-004'] -> 1
finding (first case)`, so p9 is a real dedup test.

The removed clause in `window_record._obligation_refs_problem` fired only together with a stale ROW ref and told the role to
re-send `design_assessment`. Everything it covered is now covered by the precheck finding, with one exception: a stale binding
with NO counting judgment, for example `sensitivity: proven` only. Nothing needs to name that one: with no counting design the
projection already shows design `unknown`, and the first `design_assessment` the role sends re-stamps the hash
(`_binding_stamp_allowed`). Nothing that could count is lost unnamed. There are no duplicates: grep
`design_assessment` in `window_record.py` gives 0.

**5. JUDGMENT (q. 11, AR-29, P27).** It judges data only. It compares a stamp with a hash and checks membership in the
projection's own "counts for nothing" words (`JUDGED_UNKNOWN`). Census: right as it is. The site is inside
`check_obligations`, which already has a row (`judgment-census.json:900`, `xref`, owner `data`). No new unit matches
`UNIT_NAME_RE` (`binding_currency`, `counting_value`, `_renamed_stamps`, `_renamed_from_valid`). No scan constant, class or
`blocks_override` was touched. 24/24 is correct.

**6. AR-20 RATCHET RAISES, named row by row.**

| key | old → new | measured cause | verdict |
|---|---|---|---|
| `process_ratchet_tokens.qa-automator` | 18687 → 18746 | slice +236 B (11,093 → 11,329; `injection_role` 41,171 → 41,407 B) = +59 tok at 4 B/tok | exact delta; justified |
| `process_ratchet_tokens.qa-code-critic` | 17596 → 17655 | slice +236 B (40,446 → 40,682 B) = +59 | exact; justified |
| `ratchet_tokens.qa-automator` | 20257 → 20313 | measured 20254 → 20313 (+59; the old row had 3 tokens of slack) | tight to the measure; outside the owns line; K10-c forces it |
| `ratchet_tokens.qa-code-critic` | 19420 → 19478 | measured 19419 → 19478 | the same |
| `ratchet_tokens.qa-failure-analyst` | 18361 → 18426 | NOT moved by this diff | misattributed (F1) |
| `process_ratchet_tokens.qa-failure-analyst` | 16322 → 16401 | NOT moved by this diff | misattributed (F1) |

Why qa-failure-analyst "moved": it did not. I measured with `role_load.py --role ... --json` on `git archive` copies of both
trees. At b3df35d: 18426 / 16401. At ec9c944: 18426 / 16401, all four layers byte-identical. `test_role_load.py` on the BASE
copy gives `169/171`, and both failures are qa-failure-analyst ("over its shrink-only ratchet 18,361" / "process ratchet
16,322"). The base was already red. The cause was TR4-15 (the `observation` field in the analyst's slice), and `origin/main`
raised those exact rows itself in c9f6e02 ("role-load qa-failure-analyst: ratchet 18361 -> 18426, process 16322 -> 16401 --
TR4-15 observation field"). The builder's line "169/171 before the ratchet rows moved" hid that base-red state, and its
explanation ("carries the contract text from another path") is wrong. The values match main's, so the merge produces no
conflict. But the raise is not this diff's, and the commit message ec9c944 names it as this diff's growth (F1).

Is the raise of the two real roles justified? Yes. FR-38 requires the automator to be told before its work that
`obligation_hash` and `judged_on` are the code's, and the precheck refuses on that. Could the text be shorter? Somewhat. For
example, "`obligation_hash` and `judged_on` (per-field stamps) are the code's: never send them; re-send what you re-judged",
with line 161 kept nearer its old length, would save roughly 25-30 tokens per role. That is optional and does not block. The
first-load rows outside `owns` are a Lead decision on an owns deviation; I recommend accepting it, because K10-c makes it
mechanical. After merging main (8207150 changed `allowances.brief` in `role-load.json`), the integrator must re-measure the
first-load rows.

**7. FR-11 / FR-38 / AR-10 / FR-37.**
- The reworded contract text (`references/artifact-contract-automation.md:160-168`) and both regenerated slices
  (`slices/qa-automator/...:144-152`, `slices/qa-code-critic/...:132-140`) tell the automator, before its work and among its
  own fields, that both hashes are the code's and that it re-sends the fields it re-judged.
- `contract_slices --check` is green: 44 slices fresh.
- The finding's vocabulary example matches the contract words (`sufficient|partial|unknown`, `valid|unverified`).
- FR-37: `manifest_put.py` exists, and `--task`/`--fragment` are its arguments (`manifest_put.py:2827-2843`).
- The finding prints `<T>` where the sibling at `s5_precheck.py:1536` fills the task in (F2).
- The rename `left` row names `manifest_put.py --fragment` without the REQUIRED `--task` (`manifest_put.py:2842`
  "--task and --fragment are both required") (F3).
- The message says the coverage map "counts it as unknown", but for `code_validity` the projection prints `unverified`
  (`coverage_contract.py:595-596`) (F4).

**8. Tests.** T2 p1-p9, p11 and p12 are in `test_s5_precheck.py::a_stale_binding_is_named_before_the_finish`, with ids that
name the case ("p1: ...", "p11: r2-state: ..."). p10 is the rewritten QB row (`check_not_in`). p-proj is in
`test_manifest_put_merge.py::fv1_19e_projection_reads_the_currency`; it goes through the real `Stand.put` door and would fail
before C1 (`code_validity` read `valid`). All three files are keep, not quarantine (`test-layers.json` `quarantine` section:
False for all three; True for `test_coverage_contract.py`, which was not edited). "B24 holds through the existing PASSABLE"
is acceptable. The word road is the family-generic `PASSABLE` (`s5_precheck.py:82`, untouched), and the half that matters
(the projection still counts nothing stale) is pinned by p-proj. TESTING.md asks for no test per edge.

**9. DUPLICATION / CONSISTENCY, CODE QUALITY, class completeness.**
- DUPLICATION AND CONSISTENCY: two findings, both small.
  - (a) `_BINDING_VOCAB` (`s5_precheck.py:3859`) is a second code copy of the contract's closed words. No code source of them
    exists: grep `"partial"` / `"sufficient"` gives no binding vocabulary in the scripts, and `record-schemas.json:541` is a
    different (parts) enum. It belongs beside `JUDGED_UNKNOWN` in `contract.py` (F5).
  - (b) Raw `FRAGMENT_ROAD` with `<T>` where `_road(task_root.name)` exists (`s5_precheck.py:640`, used at `:1536`) (F2).
  - No other second implementation: the projection, the precheck and the rename all call `binding_currency`/`counting_value`
    (grep above).
- CODE QUALITY: the new block in `check_obligations` (`s5_precheck.py:3878-3904`) nests 5 levels (case → obligation →
  owners → plan_map/reported → stale) and builds the message inline over 15 lines. Extract a helper (a name outside
  `UNIT_NAME_RE`, e.g. `_stale_binding_text`). Severity: fix before merge, small (F5). No dead branches, and no names that lie.
- Class completeness by the map:
  - Axis 18: the raises are named above.
  - Axis 28: one door text survives; `s5.md` is queued per spec §7.
  - Axis 32: census unchanged and correct.
  - Axis 34: none found (grep of the added lines for `typescript|\.spec\.ts|java|csharp|python|playwright|pytest` gives 0;
    positive control in the same call shape: `content_hash` gives 12).
  - Other readers of binding freshness: `metrics_projection.py:152` and `ledger.py:1740` read the projection's output.
    `check_delivery` reads `verified`. `case_stamp.py:485` and `proof_level.py:432` read `sensitivity`/`change_disposition`
    with no currency; these bind receipt FILES, are queued as spec Q-d, and are consistent with F3 (b).
  - No binding writer was left unmoved: every `"obligation_bindings":` producer was read (`red_sandbox.py:1880`,
    `probe_by_code.py:7621`, `window_record.py:1867`, `migrate_artifacts.py:427`) and none forwards `judged_on`.

**10. Rename edge.** On the migration road, no. `_renamed_stamps` (`S\contract.py:5410-5428`) gives a counting field only the
OLD stamp, or none. It is current only when the old stamp equals the new id's plan hash, which means the same text. The
migration skips a target id that already holds a binding (`migrate_artifacts.py:413`), so `merge` folds onto `{}` and inherits
nothing. One residual on a road the spec allows, and harmless: a ROLE that sends a valid `renamed_from` onto an id that already
has a stored binding gets that id's stored stamps through the per-key fold for any field the old binding held no stamp for. The
outcome equals the role sending the value fresh, which the normal path stamps with the current hash anyway. B26's wording
("yields only old stamps") is true at the stamp but not after the merge. This needs a spec note only; it is not a fix.

## Fixes (before merge; none blocks the design)

- **F1** (AR-20 record): the qa-failure-analyst rows are not this diff's raise. They were pre-existing red at b3df35d and are
  owned by main's c9f6e02. Either drop the two lines from the branch (merging main brings identical values), or correct the
  attribution in the report and the integration commit, naming c9f6e02. Name the first-load rows old → new.
- **F2** `s5_precheck.py:3899`: use `_road(task_root.name)` instead of raw `FRAGMENT_ROAD`, as the sibling at `:1536` does,
  and adjust p1 accordingly.
- **F3** `migrate_artifacts.py:457`: the `left` reason names `manifest_put.py --fragment` without the required `--task`. Use
  `manifest_put.py --task {task_id} --fragment <file>`; the field list stays first, so the 80-character cut is unaffected.
- **F4** `s5_precheck.py:3896`: "counts it as unknown" is wrong for `code_validity` (the projection prints `unverified`). Say
  "counts it for nothing", or name each field's `C.JUDGED_UNKNOWN` word.
- **F5** `s5_precheck.py:3859, 3878-3904`: move the vocabulary next to `JUDGED_UNKNOWN` in `contract.py`, and extract the
  finding text into a helper whose name is outside `UNIT_NAME_RE` (5 nesting levels in new code).

The verdict is an input; acceptance and the owns deviation (first-load rows) belong to the Lead.

## Trail

Read:
- the spec (whole, §0-§8);
- both builder reports;
- the full diff b3df35d..ec9c944 (production and tests);
- `S\contract.py:5178-5267`;
- `S\s5_precheck.py:78-90, 120-126, 636-643, 3835-3915`;
- `S\migrate_artifacts.py:380-459`;
- `S\manifest_put.py:860-900, 2420-2450, 2820-2843`;
- `S\coverage_contract.py:262-290`;
- `S\red_sandbox.py:1850-1885`, `S\probe_by_code.py:7526-7560`, `S\case_stamp.py:478-492`, `S\proof_level.py:428-440`;
- `S\acceptance.py:1178-1192`, `S\controller.py:7312-7325`, `S\manifest_from_tests.py:1515-1548`;
- `judgment-census.json:892-908`;
- `docs/SIBLING_MAP.md` axis 18, `docs/tasks/critic-diff-brief.md`;
- commit messages 928cac6 and ec9c944, and c9f6e02 on main.

Searches (Grep tool, -i, each with a positive control in the same call):
- `obligation_hash` over the scripts;
- `design_assessment|code_validity|obligation_bindings`;
- binding fragment producers;
- `stamp_obligation_refs|binding_currency|counting_value|JUDGED_`;
- `judged_on` over the package (one extra hit, `test_metric_signals.py:409`, is the unrelated word "judged_on_its_own");
- `content_hash\(`;
- `FRAGMENT_ROAD` / `_road(`.

Re-runs:
- in the worktree package (subshell): `python -B scripts/tests/test_manifest_put_merge.py` → `378/378 ok`;
  `test_s5_precheck.py` → `1076/1076 ok`; `test_role_load.py` → `171/171 ok`; `test_judgment_census.py` → `24/24 ok`;
  `test_obligation_join.py` → `63/63 ok`; `scripts/contract_slices.py --check` → `slices: 44 declared, all present and
  fresh`; `scripts/selftest.py --lang` → `2/2 ok`.
- on a base copy (`git archive b3df35d`): `test_role_load.py` → `169/171 ok`, both FAIL lines qa-failure-analyst;
  `role_load.py --role <r> --json` base/head → failure-analyst 18426/16401 at both, automator 20254/18687 → 20313/18746,
  code-critic 19419/17596 → 19478/17655.
- scratch probe `probe_p9.py` (p9 dedup, positive control: the second case alone gives one finding).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "Covered by the map: axis 18 raises named row by row (qa-failure-analyst rows misattributed, F1); axis 28 one door text survives, s5.md queued per spec section 7; axis 32 census unchanged and correct (check_obligations row 900 xref/data); axis 34 none found (grep of added lines, positive control content_hash). All three readers (projection, precheck, rename report) go through contract.binding_currency; every binding fragment producer read (red_sandbox, probe_by_code, window_record, migrate_artifacts) and none forwards judged_on; case_stamp/proof_level sensitivity readers are queued Q-d.",
  "fixes": [
    "F1 role-load.json: qa-failure-analyst ratchet_tokens 18361->18426 and process 16322->16401 are NOT this diff's (base b3df35d already red 169/171, owned by main c9f6e02 TR4-15): drop from branch or correct attribution in report and integration commit; name first-load rows old->new",
    "F2 s5_precheck.py:3899 use _road(task_root.name) instead of raw FRAGMENT_ROAD with literal <T> (sibling s5_precheck.py:1536)",
    "F3 migrate_artifacts.py:457 left-row door names manifest_put.py --fragment without the required --task (manifest_put.py:2842); print --task {task_id}",
    "F4 s5_precheck.py:3896 message says the map counts it as unknown; for code_validity the projection prints unverified (coverage_contract.py:595-596)",
    "F5 s5_precheck.py:3859 and 3878-3904 move _BINDING_VOCAB beside JUDGED_UNKNOWN in contract.py and extract the finding text into a helper outside UNIT_NAME_RE (5 nesting levels in new code)"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/20261113-fv1-19-binding-currency-spec.md",
      "docs/tasks/specs/reports/20261113-fv1-19-c1-report.md",
      "docs/tasks/specs/reports/20261113-fv1-19-c2-report.md",
      "git diff b3df35d..ec9c944 (worktree fv19-c2)",
      "scripts/contract.py:5178-5267, 5356-5520",
      "scripts/s5_precheck.py:78-126, 636-643, 3835-3915",
      "scripts/migrate_artifacts.py:166-184, 380-459",
      "scripts/manifest_put.py:860-900, 1936-1957, 2420-2450, 2820-2843",
      "scripts/coverage_contract.py:262-290, 575-600",
      "scripts/red_sandbox.py:1850-1885; probe_by_code.py:7526-7560; case_stamp.py:478-492; proof_level.py:428-440; acceptance.py:1178-1192; controller.py:7312-7325; manifest_from_tests.py:1515-1548",
      "scripts/tests/fixtures/judgment-census.json:892-908",
      "docs/SIBLING_MAP.md axis 18; docs/tasks/critic-diff-brief.md",
      "git log c9f6e02 (origin/main) and commit messages 928cac6, ec9c944"
    ],
    "reruns": [
      {"command": "python -B scripts/tests/test_manifest_put_merge.py (worktree)", "result": "=== test_manifest_put_merge: 378/378 ok ==="},
      {"command": "python -B scripts/tests/test_s5_precheck.py (worktree)", "result": "=== test_s5_precheck: 1076/1076 ok ==="},
      {"command": "python -B scripts/tests/test_role_load.py (worktree)", "result": "=== role_load: 171/171 ok ==="},
      {"command": "python -B scripts/tests/test_judgment_census.py (worktree)", "result": "=== judgment_census: 24/24 ok ==="},
      {"command": "python -B scripts/tests/test_obligation_join.py (worktree)", "result": "=== obligation join (TP2-2553): 63/63 ok ==="},
      {"command": "python -B scripts/contract_slices.py --check (worktree)", "result": "slices: 44 declared, all present and fresh"},
      {"command": "python -B scripts/selftest.py --lang (worktree)", "result": "=== qa-factory selftest: 2/2 ok ==="},
      {"command": "python -B scripts/tests/test_role_load.py (git archive b3df35d copy)", "result": "169/171 ok; both FAIL lines are qa-failure-analyst over 18,361 / 16,322"},
      {"command": "role_load.py --role <r> --json on base and head copies", "result": "failure-analyst 18426/16401 at both; automator 20254/18687 -> 20313/18746; code-critic 19419/17596 -> 19478/17655"},
      {"command": "scratch probe_p9.py (check_obligations, head copy)", "result": "TC-004 alone: 1 binding-stale finding; both cases: 1 finding on the first case"}
    ]
  }
}
```
