# t-1130 — code gate, K1b (builder t-1120, node FV2-79 / TBW1-9)

Tree `C:/QAFactory/forge-repo/.claude/worktrees/agent-a9f89661be4c45267`, branch `worktree-agent-a9f89661be4c45267`,
commit 82003646, merge-base 43eb3811 (origin/main has moved only by journal commits since; no package path changed:
`git diff --stat 43eb3811 origin/main -- ai-packages/qa-factory/...` empty).
Spec: card r3 `docs/tasks/specs/20261117-tbw-k1b-card-r3.md` with "Lead decisions and the canon input" (F1-F5 = (a)).
Report: `docs/tasks/specs/reports/20261114-k10-paydown-k1b-report.md` (in the tree).

**Verdict: fit_with_fixes — 2 findings to fix in this round (F-1 edge E6 not applied; F-2 a test row that cannot fail).**

## Findings

### F-1 (fix before merge) — edge E6 not applied: a listed key page of the automator is left with no row

Surface: the key-page pagination (`inject-map.json` list <-> `contract_slices.py` page generator).

- `ai-packages/qa-factory/references/slices/qa-automator/handoff-keys-3.md` (in the tree, 310 bytes) now holds only
  the heading and `- none: every row of this role stands on the pages before this one` — the generator's
  `NONE_CONTINUED` (`scripts/contract_slices.py:585`, emitted at :703). At the base (43eb3811) the page held the
  `s5_precheck:sides.*` rows and the "Not yet in rows" card; the diff moved those to page 2 (slice diff, page 2 now
  ends with `### Not yet in rows`).
- The page is still listed: `references/inject-map.json:66` (`roles.qa-automator`).
- Card edge E6: "a listed key page left with no row (`NONE_CONTINUED`): remove that page's line from
  `inject-map.json` `roles.<role>` and `--write` again"; owns name `inject-map.json` exactly for this. The report has
  no E6 line. Neighbouring pages: Grep for the NONE_CONTINUED sentence over all slices finds only this file (base:
  none), so this is the one instance.
- Consequence: 310 bytes of empty page stay injected into every automator dispatch, and
  `native_headroom.qa-automator` 76,472 / `process_ratchet_tokens.qa-automator` 23,257 are set to a measure that still
  counts them. The ratchets are honest for the tree as committed, but the card's end state is not reached.
- `contract_slices.write` deletes a page file that is no longer declared (`contract_slices.py:891-895`), and the only
  other `handoff-keys-3` mentions in the package are fixtures of `test_contract_slices.py` (:751, :754, :767), so the fix
  is a one-line data edit.

### F-2 (fix before merge) — `T1rs/road-carries/<road>` can never be red

Surface: the proof constants of `test_t1rs` (`scripts/tests/test_contract_slices.py`, the new block after
`T1rs/roads-of-role`).

- `CARRIED` and `L_SITE` are DERIVED from `ids` (the rows themselves): `CARRIED["probe_by_code"] = {c for c in ids if
  c.startswith(er)}`, `CARRIED["red_sandbox.*"] = ids - not_by_red_sandbox`, `L_SITE` = copies of these. The row
  checks `sorted(stale - ids) == []` with `stale` drawn from those sets, so `stale` is a subset of `ids` by
  construction: the row passes for every input (traced: no assignment makes `CARRIED[...] - ids` non-empty).
- Card item 4: "every id in `CARRIED[road]` and `L_SITE[road]` names one of the 31 rows (a stale constant is red,
  naming the ids)". Deriving CARRIED from the rows is a good move (it can't go stale), but the TYPED constants that
  CAN go stale are the exclusion set `not_by_red_sandbox` (`run_suite:phantom_story`, `:recover`, `:reparse`), `request`
  (11 typed ids, the `import_test_receipt` carry/proof) and `unproved_site`; none of them is checked against the rows.
  Concrete scenario: rename the row `run_suite:recover` in `stage-joints.json` -> the stale name in
  `not_by_red_sandbox` silently stops excluding anything, the renamed row becomes "carried" by red_sandbox, and no row
  names the stale constant (`docs/TESTING.md` «Откуда берётся ожидаемое значение»: a test that can only pass;
  brief question 5 (a)). The error direction is safe (more page), which is why this is a fix, not a block on the
  markers.

## Keys

1. **Items 1-8 built as written; nothing beyond — holds except E6 (F-1).**
   - Item 1: `unproved_site = {er+"stand", rs+"begin"}` with the comment naming canon run 44068480897 (test file, the
     `unproved_site` line of `test_t1rs`).
   - Item 2: `road_token` (one dict, read by `T1rs/roads-of-role`), `roads_of` with the F4 mode split, `PROVED_ROAD`
     (`import_test_receipt: request`, `red_sandbox.diagnostic: "pass-through"`, the two probe roads empty), the S1 = A
     sentence verbatim (compared with card item 2 word for word), `CARRIED` with the file:line reasons, `L_SITE`,
     `carries`, `proved`. `proved(check, "import_test_receipt")` = `check in request and proved(check,"run_suite")` —
     equal to the card's `check in request and check not in unproved_site`. Docstring rewritten.
   - Item 3: my own data diff (scratch script comparing base/head JSON, per (row, role): field, demands, other `told`
     keys, extra keys) — exactly the 30 flips the report lists, all page -> call; no field/demand change; no row outside
     the 31 and no top-level key changed (`other rows equal True`). Entry order for `window_first` / `stand.probe`
     (the code-critic's page-only entry placed first, the old entry flipped) differs from the C4 literal procedure but
     is semantically identical; no fix.
   - Item 4: `l-site-keeps-page`, `unproved-road-keeps-page`, `road-carries` (F-2), `partial-split` expected
     `[False, key not in unproved_site, False, key not in unproved_site]` with the card's label, `counted` / `n_er` /
     `n_rs` / `(31, 31)` removed, `T1rs/rows` = uniqueness, door-words row conditioned on `own_er`.
   - Items 5, 6, 7, 8: done (see keys 4, 9; the pin below). Item 5's E6 clause: not done (F-1).
   - Nothing beyond: `--numstat` lists only owned paths; no product `.py`, no row sentence, no `call_index_wording`.
2. **Proof constants from the requirement, not from the implementation (FR-58, P20) — holds (with F-2 on the
   stale-check row).** `unproved_site`, `PROVED_ROAD`, the carry exclusions and their file:line reasons come from
   the card / K1a table and canon run 44068480897. I checked that the canon proves THIS tree: bc689891 (the canon's
   main) contains the three §0 fixes (`probe_by_code.py:225-226`, `test_red_sandbox_probe.py:994-995`,
   `test_execution_request.py:2189-2190`, read by `git show`), and `git diff --stat bc689891 82003646` over
   `probe_by_code.py`, `red_sandbox.py`, `run_suite.py`, `execution_request.py`, `import_test_receipt.py`, `role_cli.py`
   and the three proving test files is empty. Note: bc689891 is an ancestor of 89d4b3c3, not a descendant, so the
   card's "89d4b3c3 or later" wording is not met literally; its E-canon invariant (the fixes present) is met, and the
   Lead accepted that run by name. `expected()` never reads `call_told`; `marked-by-proof` compares the data to the
   constants. Killing power: the builder's negative control (diagnostic proof removed -> 3 FAIL, hash restored
   ab133f5c…) is consistent with the code: `unproved-road-keeps-page` iterates roads whose proof is falsy, so
   `set()` adds the diagnostic row; `marked-by-proof` and `entry-uniform` turn red for the analyst's flipped rows.
   The T3a (j) pin: a join — `RL.settings` is a module global read by `native_headroom_problems`
   (`role_load.py:313`), so the patch reaches it; the role name parse `line.split(":")[0].split(" ")[1]` matches the
   message form `f"K10 {role}: the plugin share is ..."` (`role_load.py:336-337`); an unmeasured role is caught by the
   second check. Both worlds of E-T judged by one row.
3. **`told` markers really told before the work (FR-38, AR-10) — holds, sample of 10 (row, role) across 4 roles.**
   The "text behind" a call marker is (a) the role's road named in its agent file and (b) the refusal of that road
   printing the row's sentence before any launch, plus (c) the index line on the page naming the door.
   - qa-automator `purpose`, `selector`, `stand.reference`: roads `run_suite.py --mine` and `import_test_receipt.py`
     (`agents/qa-automator.md:68`); `import_test_receipt` prints every refused check (`K10p/import-prints-every-check/*`,
     `test_import_test_receipt_refusal.py:95`, builder ran 7 passed); index line "17 checks ... `run_suite.py
     --template request`" on `slices/qa-automator/handoff-keys-2.md:28` (17 = 5 before + 12 flipped: consistent).
   - qa-automator / qa-runner `window_first`, qa-runner `selector_args`: road `run_suite.py` (`agents/qa-runner.md:62`);
     sites proved by `t1rs_sites_after_the_probe` (`test_execution_request.py:2135-2210`, rows "T1rs window_first (road
     run_suite): the told entry of the printed line"), file green in the canon; runner index line "12 checks"
     (`slices/qa-runner/handoff-keys.md:105`).
   - qa-failure-analyst `active_dispatch`, `profile`, `sandbox`, `no_test`: road `red_sandbox.py --diagnostic` and
     `run_suite.py --request` only (`agents/qa-failure-analyst.md:73`; no `--probe` / `probe_by_code.py` token: Grep of
     the four agent files). The diagnostic flow refuses before its one launch and carries `told`
     (`red_sandbox.py:2185-2197`: `prepare` (clone, no test), `_run_mine`, `summary.error and not execution_status` ->
     `_carry_told`), proved by `K10p/rs-told-passes-through/diagnostic/*` (`test_red_sandbox_probe.py:996`); index line
     "13 checks" (`slices/qa-failure-analyst/handoff-keys.md:96`).
   - qa-code-critic `run_suite:phantom_story`, `run_suite:recover`: road `run_suite.py --request`
     (`agents/qa-code-critic.md:69`); `_refuse_phantom_story` prints `told_fields(refusal("run_suite:phantom_story", ...))`
     and exits 2 before any evidence write (`run_suite.py:965-974`); neither id is carried by its probe roads (reasons
     in the constants). Index line "2 checks" (`slices/qa-code-critic/handoff-keys-2.md`). Every code-critic ER row stays
     page (S1 = A): no ER index line on its page.
   No marker without text behind it found.
4. **`role-load.json` shrink-only (AR-20) — holds.** Moved keys, all DOWN: `ratchet_tokens.qa-automator` 26,053 -> 24,824,
   `.qa-failure-analyst` 22,442 -> 20,930; `process_ratchet_tokens.qa-automator` 24,116 -> 23,257, `.qa-code-critic`
   21,250 -> 21,146, `.qa-runner` 16,919 -> 16,732, `.qa-failure-analyst` 20,261 -> 18,905; `native_headroom.qa-automator`
   79,909 -> 76,472, `.qa-code-critic` 73,134 -> 72,717; `.qa-test-strategist` 53,739 unchanged (U = 53,739). No raise.
   My U-CMD re-run matches the report for all 12 roles (code-critic 72,717, automator 76,472, analyst 61,126, runner
   51,871); `native_headroom_problems()` = `[]`; `test_role_load.py` 186/186 (process slack 0). The code-critic and
   runner `ratchet_tokens` are within the 1,000 slack (425, 565) and correctly not moved (card item 7). The code-critic
   residual 72,717 - 68,400 = 4,317 B is stated in the report (line "lowered to 72717 (E7) ... residual 4,317 bytes for
   the owner") and in the changelog fragment; the row equals U exactly, so nothing is hidden by headroom in the row.
   STOP justified: E7 + F2 (a) + row-106 "lowered to U with the E7 stop" as a legal close; F5 (b) is an owner
   question, not K1b. After F-1 the automator rows move down again (re-measure).
5. **Role text edits (`agents/qa-*.md`) — not applicable: the diff touches no agent file** (`git diff --numstat`). The
   only removed role-facing text is generated page lines of rows that moved to the call; each such row's sentence is
   printed by the refusal (key 3). English: 0 Cyrillic lines in the added package lines (grep -P U+0400-04FF; positive
   control on PROJECT.md: 240), builder's `--lang` PASS.
6. **Duplication and code quality; class completeness.**
   - DUPLICATION AND CONSISTENCY: none found beyond F-2: the roads are read from one dict `road_token`; the over-H list
     goes through `RL.native_headroom_problems` (no copied formula; grep `NATIVE_CONTEXT_LIMIT|MAX_BLOCK_CHARS` is not
     in the diff); `held_by` replaces the repeated inline `any(role in e["roles"] ...)`; `texts` reused by two tables.
   - CODE QUALITY: `test_t1rs` is now ~130 lines (> 60) — the card mandates "rows of the existing function; no new
     file", nesting <= 3; not a finding. Dead/no-reader: `road_token["execution_scheduler"]` is matched by no role but
     is read (a role naming it would turn `roads-of-role` red) — intentional. F-2 is the one "work whose result nobody
     can read" item.
   - Class completeness (SIBLING_MAP axis 18 ratchets: every moved row named above, no raise, judgment census untouched
     since no `.py` product unit changed; axis 34 one printer/one road: one proof rule for all four roles, roles differ
     only by data `roads_of` checked against agent files; no role exempted by name). The E6 class (empty listed page)
     has one instance (F-1).
7. **Commit lines — hold.** `architecture: AR-10 / AR-12 / AR-20` true to the diff; `judgment: none` true (data and a
   test only). `tests-over:` — by `tools/test_volume.py` classes the commit adds 97 test lines vs 136 product lines
   (role-load 8 + slices 30 + stage-joints 98; changelog and docs excluded), so the commit is NOT over; the line is
   superfluous but its reason is true; not a finding. `axes: not a mechanism` fits (data flips under an accepted card).
8. **Tests fit `docs/TESTING.md` — holds except F-2.** No source pins: the measured `counted` / `(31, 31)` pins are
   removed; the pin T3a (j) is now a join; new rows are table rows of the existing function; no new file.
9. **`unsited 17` — holds: the card's expected remainder.** Card item 5 / DoD 3 "`unsited` stays 17 or goes down,
   never up: K1b sites nothing"; §3 / §5 name siting stream B as owner of the 17 conductor rows. My re-run:
   `told counters: hand_cards 12, legacy_legs 0, unsited 17 / stage joints: clean`.

## Observations (non-blocking, proposed for the Lead; not in K1b's owns)

- O-1: the analyst page now prints `- [run_suite:*] 1 checks of your commands ...` (`slices/qa-failure-analyst/handoff-keys.md`):
  the family wording (`stage-joints.json` `call_index_wording`, a K1b non-goal) has no singular form; first time a
  count of 1 appears. Role-facing, not person-facing. Proposed node: the owner of `call_index_wording`.
- O-2: the dropped comment "the other eight roles hold none" (E-empty) was never checked by a row; a fifth role holding
  an ER/RS row would escape `marked-by-proof` (pre-existing, not a regression). Proposed: a one-row join "every role
  holding a row of the two families is a key of `roads_of`" in a later node touching `test_t1rs` (FV2-91 or FV2-86).

## Fixes (all in this round, the same builder tree)

1. F-1: delete the line `"plugin:references/slices/qa-automator/handoff-keys-3.md",` (`references/inject-map.json:66`);
   run `python -B ai-packages/qa-factory/scripts/contract_slices.py --write` (it deletes the undeclared page,
   `contract_slices.py:891-895`) and `--check` (exit 0); re-run U-CMD and `role_load.py --all --json`; set
   `native_headroom.qa-automator` and `process_ratchet_tokens.qa-automator` to the new measure (down only), and
   `ratchet_tokens.qa-automator` only if the new tokens are more than 1,000 below 24,824; update the changelog
   fragment numbers and the report (an E6 line + new before/after). If `T1rp/pages-listed/qa-automator` turns red
   (page 2 over its cap with two pages), restore the line and write in the report why E6 does not apply.
2. F-2: replace the `road-carries` loop with rows over the TYPED sets:
   `for road, typed in (("run_suite", unproved_site), ("import_test_receipt", request), ("red_sandbox.probe", not_by_red_sandbox), ("red_sandbox.diagnostic", not_by_red_sandbox)):`
   `check_eq(f"T1rs/road-carries/{road}: every id the constants type for the road names one of the rows", sorted(typed - ids), [])`
   and one comment line that `CARRIED` / `L_SITE` are derived from the rows and cannot go stale. One probe (TESTING
   «одна проба»): on a byte copy rename `"reparse"` in `not_by_red_sandbox` -> the two red_sandbox rows FAIL naming
   `run_suite:reparsed`; restore, hash equal.
3. Witness: `python -B ai-packages/qa-factory/scripts/tests/test_contract_slices.py` (alone, all ok),
   `python -B ai-packages/qa-factory/scripts/tests/test_role_load.py`, `contract_slices.py --check`,
   `stage_joints.py --check`, U-CMD after.

## Owner paragraph — the code-critic residual (plain words)

The code critic's start packet is still about 4,300 bytes (72,717 against a ceiling of 68,400) larger than what the
Codex host can carry with room to spare. It remains because almost all of the critic's "what code will check of you"
lines about test-run requests have to stay written in its packet: the critic's probing tool can raise those errors
after a test has already started, and by your rule of 14.11 (variant A) something told only after work has begun does
not count as told before the work. So this step lowered the limit row to exactly the measured size and stopped there,
as agreed — nothing is hidden. Paying the rest down would take one of two things: either a separate design step that
re-examines whether those two places in the probing tool (`probe_by_code.py` around lines 4695 and 6266) really come
after a launch — the card's F5 (b): if they do not, most of those lines could leave the packet, but that reopens your
14.11 decision and needs your word — or cutting other text from the critic's charter and pages, which costs the critic
guidance it uses. Until then the practical risk is that Codex may refuse the critic when a project's own files add more
than about 21,700 characters to its packet.

## Trail

Read: card r3 whole (incl. Lead decisions); builder report whole; `git log -1 --format=%B 82003646`; full diff of
`test_contract_slices.py`, `role-load.json`, the changelog fragment; the slices diff (index-line hunks); the
stage-joints diff plus my scratch base/head comparison of all 31 rows; `role_load.py:296-346`; `contract_slices.py:690-720,
880-895`; `red_sandbox.py:2180-2200`; `run_suite.py:960-976`; `agents/qa-failure-analyst.md:73`, `qa-automator.md:68`,
`qa-runner.md:62`, Grep of road tokens in the four agent files; `inject-map.json:58-70`; the three automator/analyst/runner
pages' row counts and `qa-automator/handoff-keys-3.md`; `test_red_sandbox_probe.py` / `test_import_test_receipt_refusal.py` /
`test_execution_request.py` row-label greps; `docs/TESTING.md` «Бюджет», «Откуда берётся ожидаемое значение»;
`docs/tasks/critic-diff-brief.md` items 5-7, 12; `docs/SIBLING_MAP.md` axis 18; `tools/test_volume.py` head;
`tools/critic_verdict.schema.json`.
Re-runs (in the tree): `contract_slices.py --check` -> "44 declared, all present and fresh ... exit 0";
`stage_joints.py --check` -> "legacy_legs 0, unsited 17 / stage joints: clean"; `test_role_load.py` -> 186/186 ok; U-CMD
-> identical to the report's "after" column; `native_headroom_problems()` -> `[]`. Not re-run: `test_contract_slices.py`
(slow, per dispatch). Ancestry: bc689891 is an ancestor of 43eb3811; the proving files are unchanged bc689891..82003646.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "F-1: edge E6 not applied: slices/qa-automator/handoff-keys-3.md holds only NONE_CONTINUED (contract_slices.py:585) but stays listed at inject-map.json:66; 310 B injected into every automator dispatch; report has no E6 line",
    "F-2: T1rs/road-carries/<road> is a tautology: CARRIED and L_SITE are derived from ids, so stale - ids is always empty; the typed sets not_by_red_sandbox, request, unproved_site are never checked against the rows"
  ],
  "fixes": [
    "F-1: delete inject-map.json:66 (qa-automator handoff-keys-3.md); contract_slices.py --write then --check; re-measure U-CMD and role_load.py --all --json; lower native_headroom.qa-automator and process_ratchet_tokens.qa-automator to the measure (ratchet_tokens only if more than 1000 below); update changelog fragment and report with an E6 line; if T1rp/pages-listed/qa-automator turns red, restore the line and state why E6 does not apply",
    "F-2: replace the road-carries loop by rows over typed sets: (run_suite, unproved_site), (import_test_receipt, request), (red_sandbox.probe, not_by_red_sandbox), (red_sandbox.diagnostic, not_by_red_sandbox), each check_eq(sorted(typed - ids), []); comment that CARRIED/L_SITE are derived and cannot go stale; one probe on a byte copy renaming reparse shows the red_sandbox rows FAIL, hash restored",
    "Witness after fixes: test_contract_slices.py alone, test_role_load.py, contract_slices.py --check, stage_joints.py --check, U-CMD after"
  ],
  "class_completeness": "Axis 18: every moved ratchet row named, all down, census untouched (no .py product unit). Axis 34: one proof rule for four roles, roads read as data from agent files, no role exempted by name. E6 class: one instance (Grep of NONE_CONTINUED over all slices: only qa-automator/handoff-keys-3.md; base none) -> F-1. Stale-constant class inside test_t1rs: typed sets not_by_red_sandbox, request, unproved_site -> F-2; manifest already fails loudly via next().",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-tbw-k1b-card-r3.md",
      ".claude/worktrees/agent-a9f89661be4c45267/docs/tasks/specs/reports/20261114-k10-paydown-k1b-report.md",
      "ai-packages/qa-factory/scripts/tests/test_contract_slices.py (diff)",
      "ai-packages/qa-factory/references/role-load.json (diff)",
      "ai-packages/qa-factory/references/stage-joints.json (diff + scratch base/head comparison of 31 rows)",
      "ai-packages/qa-factory/references/slices/* (diff, qa-automator/handoff-keys-3.md)",
      "ai-packages/qa-factory/references/inject-map.json:58-70",
      "ai-packages/qa-factory/scripts/role_load.py:296-346",
      "ai-packages/qa-factory/scripts/contract_slices.py:585,690-720,880-895",
      "ai-packages/qa-factory/scripts/red_sandbox.py:2180-2200",
      "ai-packages/qa-factory/scripts/run_suite.py:960-976",
      "ai-packages/qa-factory/agents/qa-failure-analyst.md:73, qa-automator.md:68, qa-runner.md:62, qa-code-critic.md:68-70",
      "docs/TESTING.md, docs/tasks/critic-diff-brief.md, docs/SIBLING_MAP.md axis 18, tools/test_volume.py"
    ],
    "reruns": [
      {"command": "python -B ai-packages/qa-factory/scripts/contract_slices.py --check (in tree)", "result": "44 declared, all present and fresh; 19 key pages; exit 0"},
      {"command": "python -B ai-packages/qa-factory/scripts/stage_joints.py --check (in tree)", "result": "hand_cards 12, legacy_legs 0, unsited 17 / stage joints: clean"},
      {"command": "python -B ai-packages/qa-factory/scripts/tests/test_role_load.py (in tree)", "result": "186/186 ok"},
      {"command": "U-CMD of the card + role_load.native_headroom_problems() (in tree)", "result": "12 roles identical to the report after column (code-critic 72717, automator 76472); problems []"},
      {"command": "git diff --stat bc689891 82003646 -- proving scripts and tests", "result": "empty: the canon run proves this tree"}
    ]
  }
}
```
