# t-776 — told-before-work topic code critic: branch wip/tbw-t1r at 60ddb66d vs origin/main

**Verdict: needs_work — 2 merge blockers (B1 is a builder fix; B2 needs a Lead/owner road decision), 4 fixes to make before merge, 7 queue lines.**
Merge base: `ae41e2bc`. Note: `origin/main` (`e4df9c0f`) is now 85 commits past the merge base, so the branch needs another merge from main
before it can land (`role-load.json` rows will conflict, see (b)).

## Findings

**B1 (blocks the merge, builder fix): `K5/real` in `test_stage_joints.py` goes red because of S-1b + S-2.**
S-1b sited `run_suite:phantom_story` at `run_suite.py:971` (`_refuse_phantom_story`). The census row of that unit
(`judgment-census.json`, `run_suite.py::_refuse_phantom_story`) names 4 roles: automator, code-critic, failure-analyst, runner. Its note says
"the four agents files of `run_suite.py`". But the row `run_suite:phantom_story` in `stage-joints.json` names only `qa-automator`.
`k5_problems` (`test_stage_joints.py:765-774`) therefore prints
`run_suite.py::_refuse_phantom_story is met by qa-code-critic, qa-failure-analyst, qa-runner, which no row of it names`.
Before S-1b no ER/RS id was sited, so K5 never joined these units; the T1r-pages fix round's 334/334 predates this.
Proof: I joined `SJ.check_ids()` to the census to the rows, in-process, data only. 14 ER/RS units checked; this is the only one with
missing roles (trail R5). `stage_joints.py --check` cannot see it, because K5 lives only in the slow test file. Nobody ran the file.
- **Fix (S-2 builder, fresh):** edit `references/stage-joints.json`, row `run_suite:phantom_story`:
  - Name the 4 roles. Set `stages` to the stages where each of them calls `run_suite` (`stage_guard.stages_of_role`), not only `S5`.
  - Split the producer entries by the S-2 proof rule: automator and runner get the call marker (the run_suite road is proved F in
    S-1b); code-critic and analyst stay on the page (their red_sandbox / probe_by_code roads are unproved), about +145 B each.
  - Then run `contract_slices.py --write`, add a `T1rs/marked-by-proof` data row, and set the role-load rows to the measure. Do not
    narrow the census: the roles really do meet this refusal.
  - DoD: the K5 join of the in-process probe (trail R5) prints no missing role. `test_stage_joints.py` is judged by the batch canon.

**B2 (blocks the merge, a Lead/owner decision): K10 is red for 3 roles.** I reproduced it, see (b). This is no builder defect: the
spec's STOP path hands it up. The branch cannot merge green until one of the three roads below is decided.

**F1 (fix before merge): code line numbers in door text a role reads.**
- The `door` of `handoff_check:cli` (`stage-joints.json:5743`) ends in "(:3040-3041)". That door is printed on the key page of 7+ roles,
  e.g. `slices/qa-automator/handoff-keys.md:73`.
- The `door` of `execution_request:profile` (`:6359`) carries ":1707-1708, :1728" (automator page 2 line 8, code-critic page line 94).
- A role cannot use a line number of our code, and the number goes stale. T3a itself refused to put a line number on a page (report §4.2).
- **Fix:** drop the parentheticals from both doors and regenerate. Test row: `test_contract_slices` checks that no generated key page
  matches `:\d{3,4}`.

**F2 (fix before merge): a carrier-derived requirement runs into "Door:" with no full stop.**
- `told_line` (`stage_joints.py:603-607`) prints `{expected} Door: {door}.`. `_carrier_expected` (`:558-578`) returns texts with no
  final full stop.
- So `[s5_precheck:row_fields] ... several profiles share Door: add ...` and `[validate_artifacts:check_phase_json.*] ... `triage`
  Door:` read as one run-on sentence. I found 3 distinct lines across the pages.
- **Fix:** in `told_line`, add "." when `expected` does not end in `.`/`!`/`?`. Test row in `renderers()`: a carrier row renders `...x. Door: d.`.
  The fix changes the rendered text and so also the K8 page bytes by a few bytes; regenerate.

**F3 (fix before merge): `catalogue()` lists the key pages as "not in this prompt".**
- `contract_slices.catalogue()` (`:936-941`) puts the key pages under the head "They are not in this prompt".
- Since T3a the key pages are injected inline in every mode (`inline_subject`). The automator's `index.md` names 3 pages, 27.5 KB, as
  files to read. That is a false statement (FR-37 class), and it invites a re-read (AR-12).
- T3a raised this as Q3, and nothing on the branch closes it.
- **Fix:** skip the `keys_targets` pages, the same way `COMMON_LAYER_SUBJECTS` are skipped. Flip test row `X1-7` to "the catalogue does
  not name the key page".

**F4 (fix before merge): census row narrowed past its own note.**
- `judgment-census.json`, `exit_gate.py::required_outputs_errors`: the T1r-pages fix round removed `qa-bug-reporter`, `qa-case-critic`
  and `conductor`. The note justifies only the first two.
- Taking out `conductor` lowered `blocking_per_role.conductor` from 761 to 760. Every sibling `exit_gate.py` row (`scoped_errors`,
  `witness_errors`, `main`, ...) keeps `conductor`.
- Brief item 11: a roles edit that moves a ratchet must be justified.
- **Fix:** put `conductor` back and the ceiling back to 761, or add the conductor's reason to the note. Witness: `test_judgment_census.py`.

## Answers per DoD key

**(a) Fit per part.**
- T2: fits the spec. Its open item 1 is closed on the branch: `stage_joints.py:1240` passes `errors=id_errors`.
- T3a: fits the spec, with the K10-caller deviation described in (e).
- T1r rows, T1r-pages + fix: fit; the A22 raises are named row by row (pages report §4). Lead decision B1 of the pages spec (§435-440)
  allows A22 to go to the measure.
- S-1a / S-1b: fit, but B1 is left behind.
- S-2: fits 6b items 2, 3, 9 and 11. Blocker B1, and its estimate in Question 1 is wrong (see (c)).
- `stage_joints.py --check` is clean (unsited 119). A22 is clean (`_a22_findings`: []).

**(b) K10 numbers.**
- `contract_slices.py --check` on the branch: exit 2. It names exactly strategist 55,724, automator 81,413 and code-critic 74,327.
- Same command on wave13 (`origin/main`): exit 0.
- Main is clean only because K10 does not exist there yet (T3a adds it). By the K10 formula, main's strategist (44,861) is already over
  its H of 42,400.
- `test_contract_slices.py`: 456/461, and the 5 FAIL rows are all these K10 rows (re-run R2).

U per role = charter + common + role injection (bytes), measured with `role_load.py --all --json`. "MB" = the merge base; the per-part
columns are deltas between commit snapshots.

| role | main | MB | T3a | T1r | pages+fix | S-2 | branch | H | gap |
|---|---|---|---|---|---|---|---|---|---|
| qa-automator | 58,426 | 58,426 | +1,429 | +35,362 | -10,977 | -2,827 | 81,413 | 68,400 | +13,013 |
| qa-code-critic | 59,113 | 59,113 | +1,171 | +22,760 | -8,717 | 0 | 74,327 | 68,400 | +5,927 |
| qa-test-strategist | 44,861 | 44,588 | +1,420 | +14,736 | -5,020 | 0 | 55,724 | 42,400 (baseline 46,008) | +9,716 |
| qa-failure-analyst | 52,485 | 52,485 | +1,129 | +32,719 | -19,575 | 0 | 67,058 | 68,400 | green |
| qa-runner | 42,611 | 42,611 | +1,423 | +46,380 | -31,400 | -4,872 | 54,142 | 68,400 | green |

- T2 and S-1a/S-1b add 0 bytes.
- All other roles grow by +6.5K to +11K and stay under H.
- All of the growth is the key pages: automator 4,585 -> 27,572 B, strategist 6,626 -> 17,762 B.
- After the merge from main, strategist rises by another +273 (main's charter). That is about 55,997, an estimate, not measured.

The three roads:
- **(2) Pay down first**, bytes measured from the page lines:
  - (2a) `import_test_receipt` prints one `expected:`/`door:` pair per check. That returns 3,056 B, automator only (10 request rows +
    `stand.reference`). Automator then sits at about 78,357, still +9,957 over H.
  - (2b) Carry lists plus a provoked `told` for red_sandbox / probe_by_code. For code-critic that returns 5,380 B minus about 412 B for
    the two new index lines, i.e. about 4,968 B. Code-critic would still be over by about 959. It closes, by about 451 (about 306 after
    B1's +145), only if the four W/N rows (`selector_args`, `window_first`, `stand`, `run_suite:begin`, 1,410 B) are also proved on the
    run_suite road.
  - Strategist gains 0 from any of road (2): it holds no ER/RS row.
  - Even with every ER/RS row told at the call, automator saves at most about 6.3K.
- **(3) Cut the pages.** For the strategist, T1r's net is exactly its gap (+9,716). Cutting it means taking output-check rows
  (handoff_check 3,326, planning_contract 1,659, coverage_contract 1,560, ...) off the page with no call road. That breaks FR-38 (pages
  spec F-1 (c), refused). The cuts that keep FR-38 are the queued N-door (about 2-3K per role) and the prose pass F-2 (c) (about 5-7K
  per STOP role). Both are the spec's estimates; I did not measure them.
- **(1) Raise the baselines at the measure**, named rows: strategist 46,008 -> 55,724 (about 55,997 after the merge), new rows
  automator 81,413 and code-critic 74,327. FR-38 stays whole. The risk taken is the Codex native ceiling, and only when the project
  files are near the 26,000-per-entry worst case (N-10, real sizes unknown). Under the pages spec the no-raise of `native_headroom` is
  a Lead decision with the owner's F-2 (a) behind it.

The cheapest road that keeps FR-38 and AR-12:
- **Code-critic:** (2b) plus the W/N proofs closes it with no raise.
- **Automator and strategist:** no FR-38-keeping road closes them within this topic. (1) plus queued pay-down nodes, each with a DoD
  that lowers its row, is the only green merge. A measurement of real `framework-rules.md` / strategy file sizes (N-10) should
  accompany the raise.
- The AR-12 price is already paid in A22: +1.6K to +5.7K tokens per start against main, for all 12 roles. It is named.
- The decision belongs to the Lead and the owner.

**(c) The S-2 proof rule.**
- "Proved on every road the role uses that can carry the row" is the right reading of 6b items 2-3. The added "that can carry" is
  needed: `import_test_receipt` carries only `validate_request` ids.
- Dropping `schedule` as a road is harmless: it is `run_suite.py --schedule`, and S-1b proves `_child_row`'s pass-through of the
  child's list on a representative id. The scheduler's own refusals (`_apply_budget`, `main`'s `invalid_schedule`) are queued by S-1b.
- Toward under-telling the rule is safe: a row is never in neither carrier (`T1rp/no-row-lost`). Toward over-telling it costs only
  bytes, and that is exactly why code-critic did not close.
- One soft spot: the binding index wording (6b item 11) names `red_sandbox.py`/`probe_by_code.py` to automator and runner. Those roads
  are not theirs and not proved, so the line claims a told refusal on roads nobody proved (Q-5).
- Q1: keep the rows on the page until a per-check printer lands. The saving is 3,056 B, not the "about 5.8K" the report estimates.
  The fix belongs in `role_cli.run_guarded`/`refuse`: one `expected`/`door` pair per distinct record of `exc.records` (first-seen), so
  the text road equals the JSON road (`told_fields`). Test row: a request failing on 2 checks prints both.
- Q2: red_sandbox passes `run_suite`'s `told` list through unchanged (`_carry_told(told, summary)`). Its carry list is therefore every
  id run_suite prints, plus the in-process `fresh_evidence` / newest-result exceptions. One provoked pass-through row per road proves
  it, the same reading S-1b used for `schedule`. It can be done in-process by monkeypatching `_run_mine`/subprocess, with no sandbox.
  A reachability reading alone is not "proved" under 6b item 2.
- Q3: yes. `stand.reference` is raised by `validate_request` (`execution_request.py:185`) and by `build_mine_request` (`:2912`).

**(d) T2.**
- `block` prints `spoken` + TRAPPED; `deny` prints "STAGE GUARD: " + `spoken`; `refuse` uses the same labels with the card lines
  between `door` and `check`. In all three, `check` comes last before the trailer. Byte identity for `str` is witnessed (T2 report).
- No code parses the old text: `LAST_DENIAL` keeps the problem only. The `splitlines()[-1]` readers (`story_step.py:459`,
  `driver_stage_s6/s7`) read `finalize_task`/`brief_pack` output, which does not go through `role_cli.refuse`. I grepped for both.
- `sited_ids(errors=)` is wired (`:1240`).
- `role_cli:<command>` for a command with no card: queue Q-1.
- Queue line Q-c of the last verdict is still open: `refusal_registry.py:1416,1508` (Q-2).

**(e) T3a.**
- K8 is one constant (`SLICE_MAX_BYTES` 12,000) and the largest page is 11,970.
- The K10 caller is `contract_slices.keys_findings` instead of the A22 caller. Today that is the only CI road, so it is acceptable,
  but a size finding turns 3 freshness rows red ("fresh", "present", "CLI") and `--check` reports it as a slice problem (Q-3).
- The census row outside owns (`role_load.py::native_headroom_problems`, shape/conductor/data) is correct and required by C1. The Lead
  should note the owns breach.
- `catalogue()`: F3.

**(f) Class / duplication / quality.**
- Axis 18: every raise is named (A22, `native_headroom` new, `told_ratchet.unsited` 0 -> 150 -> 119, `rowless` 55 -> 25 down, census
  ceilings down). F4 is the one edit with no reason.
- Axis 17: one Record, `spoken` for the text road, `told_fields` for JSON.
- Axis 34: the automator's manifest-row exclusion stays. It is a data marker per producer entry, with its reason in the test constant
  `manifest` and in sites spec F-3 "по рекомендации, до слова владельца". Named here as a remaining exclusion (12 (c)); the owner's word
  is still owed.
- DUPLICATION: `role_cli.refuse` renders the `expected`/`door`/`check` labels a second time beside `spoken` (`detector_verdict.py`
  `spoken`), forced by an import cycle (Q-4). `red_sandbox._carry_told` repeats `told_fields`' dedupe by check (low).
  Grepped `expected: |door: ` over `scripts/*.py`.
- CODE QUALITY: no new function over 60 lines. The long functions touched are the existing `validate_request` (273 lines),
  `build_mine_request` (701) and `run_suite.main` (289), where only sites were relabelled. `red_sandbox.probe` can attach a `told` met
  on a note path to a later refusal of another check (low, Q-6).
- `hooklib.block` falls back on `ImportError` only. Any other import or `spoken` failure would exit 1 (a non-blocking hook error), not
  2 (Q-7).

**(g) Slow files.**
- `test_stage_joints.py`: **red on K5/real (B1)**. The other pins hold, measured in-process: K1 267 rows, `rows-for/real` 114, legacy
  0, the six families, unsited 119.
- `test_audit_rules.py` (A22 / A-K1): `_a22_findings` is [], so green by measure.
- `test_hooks_wiring.py` part 5: the injected headers did not change for the expected refs, and there is no total injection cap
  (per-file 26,000 only). Low risk.
- `test_brief_pack.py` and `test_story_run_refusals.py`: no reference to the changed sinks, pages or ER/RS JSON. Low risk.
- `test_selftest_slow_tests`: no new test file. Low risk.

## Queue lines (pile form)
- Q-1 `RefusingParser.error` prints `check: role_cli:<command>` for a command with no registry card: an id with no row | перенос: tbw T1r-cards | обоснование: AR-22, an id produced with no reader | подтвердил: —
- Q-2 `refusal_registry.py:1416,1508` `check_id` records typed `state: walk_error` (earlier Q-c; T2 added a second) | перенос: tbw T10 | обоснование: the name misleads; readers filter consistently | подтвердил: —
- Q-3 K10 reported through `keys_findings`: a size finding turns the freshness/SHIPPED rows red; give it its own label or also run it from `audit_factory._a22_start_load` | перенос: tbw T3b | обоснование: AR-18, the message names the wrong problem | подтвердил: —
- Q-4 `role_cli.refuse` is a second renderer of the `spoken` labels (import cycle) | перенос: tbw T10 | обоснование: AR-18 / brief item 6 | подтвердил: —
- Q-5 ER index wording names `red_sandbox.py`/`probe_by_code.py` to roles that do not use those roads | перенос: tbw T1r-sites next node | обоснование: FR-56, an unproved claim | подтвердил: —
- Q-6 `red_sandbox._author_baseline`/`_diagnostic_red` note-path `told` rides a later refusal of another check | перенос: tbw T1r-sites next node | обоснование: AR-18 | подтвердил: —
- Q-7 `hooklib.block` catches only `ImportError` around `spoken` | перенос: tbw T10 | обоснование: FR-59, a block must exit 2 | подтвердил: —
- K5 lives only in the slow `test_stage_joints.py`, so the CLI audit missed B1: move the K5 join into `stage_joints.check` or a fast keep file | перенос: tbw T10 | обоснование: a detector placed where nobody runs it | подтвердил: —

## Trail
- **Read:** the brief; S-2, T2, T3a, T1r-pages and pages-fix reports; sites spec §6/§6a/§6b/§7; pages spec grep of A22/AR-20;
  `detector_verdict.py`, `hooklib.block`, `stage_guard.deny`, `role_cli.refuse` diffs; `import_test_receipt.py` and `red_sandbox.py`
  diffs; `execution_request.py:25-54,119-208,366-381`; `stage_joints.py:321-342,468-488,541-607`; `test_stage_joints.py:500-515,745-865,
  914-923,1107-1189`; `test_contract_slices.py:930-1000`; `test_hooks_wiring.py:274-313`; automator `handoff-keys-2.md`, `index.md`;
  `inject-map.json` diff; `role-load.json` diffs; census and told-ratchet diffs.
- **Re-runs:**
  - R1 `contract_slices.py --check`: branch exit 2 (3 K10), wave13 exit 0.
  - R2 `test_contract_slices.py`: 456/461, 5 K10 FAILs.
  - R3 `stage_joints.py --check`: clean, unsited 119.
  - R4 `role_load.py --all --json` on main, the MB and 9 commit snapshots (`git archive` into the scratchpad).
  - R5 in-process K5 join of ER/RS ids: only `_refuse_phantom_story` is missing 3 roles.
  - R6 `_a22_findings`: [].
  - R7 in-process pins: 267 / 114 / 0 / six families.

```json
{
  "verdict": "blocker",
  "blockers": [
    "B1 K5/real red: run_suite:phantom_story (sited by S-1b, run_suite.py:971) names only qa-automator while census unit run_suite.py::_refuse_phantom_story names automator, code-critic, failure-analyst, runner; fix the row's producers/stages and markers per the S-2 proof rule",
    "B2 K10 red for qa-test-strategist 55,724, qa-automator 81,413, qa-code-critic 74,327: the merge needs a Lead/owner road decision (named native_headroom raise with queued pay-down, or pay-down nodes first)"
  ],
  "fixes": [
    "F1 drop code line numbers from the doors of handoff_check:cli and execution_request:profile in stage-joints.json, regenerate, add a no-line-number page row",
    "F2 told_line adds a full stop when the expected text has none (carrier-derived rows), test row in renderers()",
    "F3 contract_slices.catalogue skips key pages (inline since T3a), flip test X1-7",
    "F4 census required_outputs_errors: restore conductor (ceiling 761) or state its reason in the note"
  ],
  "class_completeness": "Axis 18: all ratchet moves named except the conductor narrowing (F4). Axis 17: one Record, spoken plus told_fields. Axis 34: the automator manifest-row exclusion stays as a data marker, owner word owed. Siblings of B1 checked over all 14 ER/RS units: only phantom_story. Analogs queued as Q-1..Q-7 plus the K5 placement line.",
  "trail": {
    "read": [
      "docs/tasks/critic-diff-brief.md",
      "docs/tasks/specs/20261114-told-before-work-t1r-sites-spec.md",
      "docs/tasks/specs/20261114-told-before-work-t1r-pages-spec.md",
      "worktree reports: t2, t3a, t1r-pages, t1r-pages-fix, t1r-sites-s2",
      "scripts: detector_verdict.py, hooklib.py block, stage_guard.py deny, role_cli.py refuse, import_test_receipt.py, red_sandbox.py, execution_request.py, stage_joints.py, contract_slices.py catalogue",
      "tests: test_stage_joints.py K5/K12/t1rp, test_contract_slices.py test_t1rs, test_hooks_wiring.py part5",
      "references: stage-joints.json rows, role-load.json, inject-map.json, judgment-census.json, slices/qa-automator"
    ],
    "reruns": [
      {"command": "python -B scripts/contract_slices.py --check (branch / wave13)", "result": "exit 2 with K10 strategist 55,724, automator 81,413, code-critic 74,327 / exit 0"},
      {"command": "python -B scripts/tests/test_contract_slices.py", "result": "456/461 ok, 5 FAIL all K10"},
      {"command": "python -B scripts/stage_joints.py --check", "result": "clean, unsited 119"},
      {"command": "role_load.py --all --json on main, merge base and 9 branch commits", "result": "per-part deltas in table (b)"},
      {"command": "in-process K5 join of ER/RS check_ids to census and rows", "result": "run_suite.py::_refuse_phantom_story missing qa-code-critic, qa-failure-analyst, qa-runner"},
      {"command": "audit_factory._a22_findings(PLUGIN_ROOT, require_settings=True)", "result": "[]"}
    ]
  }
}
```
