# t-205 — HF8-4 (onboarding-forge/2): the HF2-0 "after release" list, cut into builder parts

Draft by the designer for the Lead. Decisions are the Lead's: forks are in §5, small choices I closed are in §6.
Source finding: `plans/piles/onboarding-forge/findings/20261026-hf2-0-posle-reliza-dolg-kachestva.md` (items 1-9).

**Fix round t-220** (designer, 12.11.2026): the critic verdict `docs/tasks/specs/reviews/t-213-t-205-plan-review.md`
(GO WITH FIXES) is applied. The map "review item -> applied / how" is §8. The forks F1-F7 are written as the
coordinator decided them, «по рекомендации, до слова владельца». Two new forks (F8, F9) are open. P7, P8 and P10 were
dispatched before this round (t-218: P7 + m6; t-219: P8 + P10 + m8). Their text below is unchanged except for that note.

**Freshness note.** I started reading the code in `C:\QAFactory\forge-repo\.claude\worktrees\int-of2\ai-packages\qa-factory\`.
That worktree **disappeared during drafting**: Read and Grep answered "path does not exist", so some other session
removed it. I switched to `C:\QAFactory\forge-repo\ai-packages\qa-factory\` (main, 56e23b1) and re-checked a sample of
line numbers there. All matched: `controller.py:237`, `planning_contract.py:1527`, `question_register.py:85`,
`report_facts.py:4751`, `s5_precheck.py:1974`, `acceptance.py:748`, `artifact-contract-automation.md:70`,
`code-review-rubric.md:72-76`, `role-load.json:16,30`. I did not re-check every other line number on main. **Every
builder re-greps the named symbol before editing** and goes by the symbol, not by the line number. The fix round
re-read on main every line it newly cites (§7, "fix round").

**Paths.** Every `owns:` below is written under `C:\QAFactory\forge-repo\`. A builder working in a worktree maps it to
the same relative path under its worktree root.

---

## §1 Architecture, owners, census (designer rule 1; CLAUDE.md rule 10)

| AR-n | touched by | change check written into the DoD |
|---|---|---|
| AR-13 (a fact with a reader is read only through it) | P1-P10 | after the part, `grep` of the old literal/reader in the owned files finds only the survivor (the DoD quotes the grep) |
| AR-15 (one survivor, wired everywhere) | P1-P5 (one word), P5 + P9 (report headings), P8, P9, P10 (`event_store.replace_file`) | the survivor is named. Each other site imports it and keeps no local spelling, except the aliases listed in §6-c |
| AR-14 (one artifact, one writer) | P9 | `report_facts` writes the appendix (`_refresh_appendix`) and owns its reader. `validate_artifacts` only reads through it |
| AR-10 / AR-11 / AR-20 (a requirement reaches the role before the work; role load; ratchets only shrink) | P11 | the four `role-load.json` rows of qa-automator and qa-code-critic are set to the measured value, each move NAMED row by row in the commit and in the diff critic's verdict (F2, M4) |
| AR-28 (an unknown never becomes a pass) | P6 (ledger), P9 (`is_legacy_report`) | P6: a digit-string `then` now flags a green on an open oracle (toward `NOT_VERIFIED_UNCONFIRMED`); the one removal (a bool `then`) is fork F9. P9: a report is never moved to the lighter legacy contract by the change (the legacy test stays a substring test) |
| AR-29 (a code check judges data) | P2, P6, P9 | no check changes class. See the table below |

**Checks altered, their owner and census class** (`scripts/tests/fixtures/judgment-census.json`; classes: shape, xref, word-list, meaning-proxy, meaning, safety). Census row numbers are as t-213 counted them on main `539361a`; the builder re-greps by function name:

| check (file:function) | change | owner | census class |
|---|---|---|---|
| `controller.py:_s5_gap_problems` / `names_contradicts` | spelling source only | data | xref (row 188, unchanged) |
| `ledger.py:plan_row_state` (green on an open oracle) | reads `then` through `contract.then_number` | data | shape (no row today; add none unless the census test demands one) |
| `validate_artifacts.py:check_report_traceability`, `check_report_forbidden`, the prose-budget cut (`_authored_text`) | read the appendix span through `report_facts` | data | xref (row 918, unchanged) / shape |
| `validate_artifacts.py:is_legacy_report` | spelling source only (substring test kept, M3) | data | unchanged |
| `validate_artifacts.py` readers at `:1314` (`## Left with you`), `:1356` (`## Proven`), `check_report_human_text` (`REPORT_HUMAN_HEADING`), `check_report_gate_b` (`:1461`, `:1464`), the gate-B reader at `:1548-1549` | spelling source only (grammar constant); the READING is unchanged (new finding, F6) | data | unchanged |
| `traceability.py` gate-B insertion (`:1688-1698`) | spelling source only (P5) | data | unchanged |
| `s5_precheck.py:_check_blocked_then` (split only) | none | data | unchanged |
| P11: the automator's role text and contract | a judgment the automator makes (sanctioned masking paths), accepted by the code critic (tier above in the S5 loop) | judgment | not a code check, no census row |

A function split can move a raise into a new helper. If the census test (`test_judgment_census.py`, printed by the
witness command) then asks for a new row, the builder adds it with the parent function's class, roles and owner. It
never raises a ceiling in `ratchet`. A ceiling the change cannot stay under is a question to the Lead, not an edit.
`judgment-census.json` is also edited on `fix/ci-main` and `conv/accepted-nodes` (t-213 M5): a part that adds a row
names that in its report, and the integrator resolves the textual conflict at the merge.

**Every package commit** of a part carries `architecture: AR-n -- <how kept>` and `judgment: ...` (`tools/architecture_gate.py`). It also carries the FR walk by section (PROJECT.md "Как принимается изменение пакета" p.1):
C (FR-13: a closed word in one home) and G (FR-32) for all parts; D (FR-59) for P6 and P9; B for P11 (text the role reads);
A, E and F "not changed".

---

## §2 Verdict per item of the finding (evidence by file:line on main / the worktree before removal)

| # | item | verdict | evidence |
|---|---|---|---|
| 1 | four spellings of `contradicts_requirement` | **live, and grown to 14 spellings in 12 files** | literals: `acceptance.py:748` (`CONTRADICTS_REQUIREMENT`, today's de-facto home; `manifest_from_tests.py:950` says "`contract` holds no such constant"), `contract.py:83` (inside `UNRESOLVED_REASONS`), `contract.py:2576` (`_red_thens_of`), `contract.py:5335` (`PROBE_NOT_APPLICABLE_REASON`), `controller.py:237` (`CONTRADICTS_WORD`; test K1 `test_red_window.py:381-382` holds it equal), `s5_precheck.py:110` (`CONTRADICTS`), `s7_pretriage.py:58` (`CONTRADICTS`), `stage_status.py:181` (`RED_ON_PURPOSE`), `story_step.py:1614` (inside `DERIVED_GAP_KINDS`), `check_traceability.py:67`, `check_delivery.py:2003`, `driver_stage_s7.py:44`, `gate_brief.py:4478`, `traceability.py:931`. Search: `["']contradicts_requirement["']` over `scripts/*.py`. Positive control: the same search found the test literals. The finding's `story_step.py:1146` and `controller.py:122` moved (now 1614 and 237). t-213 re-ran the grep: 14 hits in 12 files, the same list |
| 2 | the automator has no `code-review-rubric.md` | **live** | `references/inject-map.json:59-67`: the automator's list has no rubric. The critic's list (`:72`) has it. `brief_pack.py:1912-1913` names the rubric only to the plan critic (`if not author`). The automator still has pointers it cannot follow: `agents/qa-automator.md:72` "(commented out: rubric dimension 8)" and `references/artifact-contract-automation.md:70` "A commented-out Then: rubric dimension 8." (both also in `references/slices/qa-automator/artifact-contract-automation.md:68`). Dimension 8 now has FOUR sanctioned paths (`code-review-rubric.md:72-76`), not three. Case-insensitive search for `known defect\|red_lock\|sanctioned\|code-review-rubric` in `agents/qa-automator.md` gave 0 hits. Positive control: the same search in `references/` found the rubric |
| 3 | readers of the Then number outside `contract.then_number` | **live at ONE site (the ledger); the manifest site is not a defect** (corrected after t-213 B1) | `ledger.py:866-868` `plan_row_state`: `isinstance(binding.get("then"), int)`. A hand-sent `"2"` on an open-oracle Then is skipped, so the green is not flagged (error toward a pass). A hand row reaches the ledger: `manifest_put` accepts hand rows and reads them through `then_number` (`manifest_put.py:1459-1473`). The finding's `ledger.py:412` moved here. NOT live: `manifest_from_tests.py:1596-1597` `_case_picture` does `int(b["then"])`, but it receives `bindings` (the rows the markers wrote, `:1536`, `:1549`), never the list `_merge_bindings` returns (that list only goes into `fragment["then_bindings"]`, `:1531`). Every marker row takes its `then` from `_then_numbers` (`:636-645`), which refuses anything that is not an int >= 1. So no hand-sent row reaches `int(...)`. Wider analogs are in fork F5 |
| 4 | `SETTLED_STATUSES` twice | **live** | `question_register.py:85` and `planning_contract.py:1527`. The latter is used at `:2711`, `:2771` (`_apply_gate_answers`, where `QR` is imported at `:2663`) and `:3499` (`_apply_recorded`, `QR` imported at `:3497`). Not applicable: `s5_precheck.py:1974` `SETTLED_STATUSES = C.PROVISIONAL_SETTLED` is another fact under the same name (provisional sides) |
| 5 | the "stand not confirmed" block text built twice (story_run) | **live, moved out of story_run.py** | `driver_stage_build.py:102-103` (`stand_check`) and `driver_stage_s6.py:603-604` (`s6_no_stand`) build the same f-string. `story_run.py` no longer holds it: Grep for `STAND_NOT_CONFIRMED\|stand_not_confirmed\|--block` in `story_run.py` gave 0 hits. Positive control: `waiver.py:373` was found by `stand not confirmed` |
| 6 | readers of the appendix twice; `APPENDIX_HEADING` beside a literal | **live, and wider** (t-213 B2) | own readings in `validate_artifacts.py`: `:1170` (`"## Appendix" not in text`), `:1255` (`partition`), `:1408` (`find`), `:1972` (`find`, on `authored`). The reader `report_facts._appendix_body` / `_section_span` is at `:4754` / `:4324`. The constant `report_facts.py:4751` is defined AFTER the literal `report_facts.py:81` (in `SLOTS`). A third spelling: `grammar.py:105` (`REPORT_SECTIONS`). The same class covers every report heading the three files spell: the full enumeration is in P9 (and `traceability.py`'s in P5). A second section READER exists beside `_section_span`: `validate_artifacts._report_section_body` (`:1200`, no fences, no block markers), plus own section readings in `report_facts.left_with_you_text` (`:4339-4353`), `validate_artifacts.check_report_gate_b` (`:1461-1464`), `traceability.py:1688-1698`, and `human_text.section_problems` (`:420`). These go to a new finding (F6) |
| 7 | long functions | **live, all grown** | new ones: `acceptance.red_by_requirement` 851-967 (117 lines, ~32 of docstring); `planning_contract._apply_recorded` 3496-3591 (96); `execution_request._observe_stand` 2786-2865 (80); `s5_precheck._check_blocked_then` 1419-1495 (77). Grown: `execution_request.build_mine_request` 3165-3855 (~690); `manifest_from_tests.build` 1125-1551 (427); `window_record.build` 1200-1521 (322); `acceptance.validate_window` 1034-1258 (225); `ledger.plan_row_state` 679-917 (239); `stage_S6` now `driver_stage_s6.py:403-513` (111, moved from story_run). Counted from the `def` line to the next top-level `def` (or the next method for `stage_S6`) |
| 8 | lying comments | **half fixed** | live: `s5_precheck.py:3793`, in the docstring of `check_row_fields` (`:3782`): "(`dispatch_scope` is None - no dispatch, an unknown id, or two running)". `dispatch_scope` (`:450-466`) has no running-count logic. It returns None for no id, an unknown id, or a dispatch with an empty scope. Fixed: `<!-- wave 2: plan critic -->` is gone from `agents/qa-code-critic.md`. Its only HTML comments are `kind:`/`gen:` markers (`:12,17,27,42,64,81,83,86`). Positive control: the search `wave 2` found `CHANGELOG.md:386` |
| 9 | FR-31 observation, `PermissionError` on `os.replace` | **live** | `execution_request.py:411` (`JobStore.write`) and `:3869` (`write_mine_request`) use a bare `os.replace`. The survivor exists: `event_store.replace_file` (`event_store.py:177-190`, WinError 5/32 on Windows, 8 tries; stdlib-only imports, so no cycle). The class is wide: t-213 recount, 45 occurrences of `os.replace(` in 35 non-test package `.py` files, counting the survivor and its docstring. After P10, 41 bare sites in 33 files remain (F3 finding) |

Live: items 1, 2, 3 (ledger only), 4, 5, 6, 7, 8 (half) and 9. Fixed: the `qa-code-critic.md` half of 8. Not
applicable: the `_case_picture` half of 3 (no input reaches it); `s5_precheck.SETTLED_STATUSES` (item 4, another fact).

---

## §3 Parts, waves, parallelism

Ownership is disjoint by file. `controller.py` stands alone (P2). The `story_run.py` concern of item 5 now lives in the
driver mixins (P8), and no part touches `story_run.py`.

| part | owns (product files) | items | depends on | status |
|---|---|---|---|---|
| P1 | `contract.py`, `acceptance.py` | 1 (survivor), 7 (`red_by_requirement`) | the `очередь:` line for `contract.py` (M5, F8) | ready after the gate |
| P2 | `controller.py` (+ `tests/test_red_window.py`) | 1 | P1 | wave 2 |
| P3 | `s5_precheck.py`, `s7_pretriage.py`, `stage_status.py` | 1, 7 (`_check_blocked_then`), 8 | P1 | wave 2 |
| P4 | `story_step.py`, `driver_stage_s7.py`, `gate_brief.py` | 1 | P1; onboarding-hooks/4 (existing queue line) | wave 2 |
| P5 | `check_traceability.py`, `check_delivery.py`, `traceability.py` | 1, 6 (traceability headings) | P1, P9; OF4-27 merged (`traceability.py`) | wave 2 |
| P6 | `ledger.py`, `manifest_from_tests.py` (+ 1 test row in `test_ledger.py`) | 3 (+1: the docstring that says contract has no constant) | P1 | wave 2 |
| P7 | `planning_contract.py` | 4, 7 (`_apply_recorded`) | — | dispatched t-218 |
| P8 | `waiver.py`, `driver_stage_build.py`, `driver_stage_s6.py` | 5 | — | dispatched t-219 (with m8) |
| P9 | `grammar.py`, `report_facts.py`, `validate_artifacts.py` (+ 1 test row in `test_report_facts.py`) | 6 (+F6 a') | — | ready |
| P10 | `execution_request.py` | 9, 7 (`_observe_stand`) | — | dispatched t-219 |
| P11 | docs, see the part | 2 | — | ready |

**Wave 1 (parallel, at most 6 writers):** P1 (after its gate), P7, P8, P9, P10, P11. P7, P8 and P10 are running
(t-218, t-219: two writers for three parts).
**Wave 2 (parallel, after P1 is merged to the batch branch):** P2, P3, P4, P5 (also after P9 and OF4-27), P6.
Wave 2 needs `contract.CONTRADICTS_REQUIREMENT` to exist. A wave-2 part started before P1 lands would have to invent it.
P5 also needs the grammar heading constants of P9.

**Zone records, before P1 starts (Lead actions, t-213 M5; no builder writes these):**
1. The frozen HF8-4 cell (`batch-2-onboarding-roles-forge-p3.md:60`, «Пишет в») does not name 16 of the written files.
   Positive control of that claim: the cell names `contract.py` and `execution_request`, and does not name
   `s7_pretriage`, `stage_status`, `waiver`, `grammar`, `role-load`, `code-review-rubric`. The Lead writes the full
   list of owned files of P1-P11 into the batch's «Ход» section (writable in a taken batch).
2. `contract.py` is also in OF4-25 (onboarding-forge/4, file on `wip/of-batch4`). P1 changes module constants, which
   the D-0048 `функции:` door cannot name. The Lead records one `очередь:` line for the pair in BOTH preambles (the
   direction is fork F8). **P1 is not dispatched until both lines exist.**
3. The integrator is told about the `judgment-census.json` conflict (§1).

Long functions: the four new ones are split inside P1/P3/P7/P10 (F4 decided). The six grown ones go to «Остатки» as
`перенос:` lines with a human's confirmation (F4).

**Witness, every part** (`plans/builder-rules.md` 7b; CLAUDE.md rule 4):
`python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <every owned path>`. Then run every
test file it prints, except a quarantined file (`test-layers.json` "quarantine") and except `SLOW_TESTS`
(builder-rules 7b; CI judges those). The witness in the report is both outputs verbatim. Keep files these parts are
known to touch: `test_red_window.py`, `test_manifest_from_tests.py`, `test_ledger.py`, `test_s5_precheck.py`,
`test_question_register.py`, `test_execution_request.py`, `test_report_facts.py`, `test_validators.py`,
`test_story_run_stand_identity.py`, `test_window_record.py`, `test_check_delivery.py`, `test_s7_pretriage.py`,
`test_story_step.py`, `test_then_remainder.py`, `test_probe_gap_word.py`, `test_role_rules.py`,
`test_contract_slices.py`, `test_judgment_census.py`. Quarantined, never run or edited: `test_contract.py`,
`test_acceptance_semantics.py`, `test_mixed_then_precheck.py`, `test_question_stop.py`, `test_bug_link_s9.py`,
`test_planning_contract_not_planned.py`, `test_story_run_stand.py`, `test_traceability.py`,
`test_traceability_report.py`, `test_validate_artifacts_report.py`, `test_waiver_release.py`.

**Tests asked for** (docs/TESTING.md): no new test file anywhere. Parts P1-P5, P7, P8 and P10 are
behaviour-preserving: no new rows; the keep rows the witness prints must stay green. A row is rewritten only where it
pinned a removed name (P2). New rows only where behaviour changes on a defect: P6 (one variant row in
`test_ledger.py`) and P9 (one parameterised row in `test_report_facts.py`, t-213 M3).

---

## §4 The parts

### P1 — the one home of `contradicts_requirement`; `red_by_requirement` split

given: this spec §1-§4; `ai-packages/qa-factory/design/factory-rules.md` (whole); `plans/builder-rules.md`; `docs/TESTING.md`; `ai-packages/qa-factory/scripts/tests/test-layers.json`
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\contract.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\acceptance.py
non-goals: any other module's literal (P2-P6); any behaviour of `red_by_requirement`; `validate_window` (F4, queued); the OF4-25 region of `contract.py` (`registry_sides`) and the FV1-1 regions (`case_levels`, `CASE_REQ_LINE_RE`)
handoff: report per `.claude/agents/builder.md` rule 7 with the witness and the grep below
edges: see "Edge behaviour"
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/contract.py ai-packages/qa-factory/scripts/acceptance.py` plus every keep test it prints, all green
siblings: P2-P6 (same word, wave 2); `acceptance.PENDING_OUTCOME = C.PENDING_IMPLEMENTATION` (`acceptance.py:554`) is the alias precedent
designer: this file

**Start gate (t-213 M5):** the Lead dispatches P1 only after the `очередь:` line for `contract.py` between
onboarding-forge/4 and onboarding-forge/2 stands in both batch preambles (§3 "Zone records" 2; direction F8). The
builder merges `main` into its tree before committing if the other batch landed first; the regions are disjoint by line.

Change:
1. `contract.py`: add `CONTRADICTS_REQUIREMENT = "contradicts_requirement"` right after `PENDING_IMPLEMENTATION`
   (`:82`), BEFORE `UNRESOLVED_REASONS` (`:83`, a module-level tuple that uses it). Add a one-line comment: "ONE home
   (FR-13, AR-13); `acceptance.CONTRADICTS_REQUIREMENT` and `PROBE_NOT_APPLICABLE_REASON` alias it". In
   `UNRESOLVED_REASONS` replace the literal by the name. In `_red_thens_of` (`:2576`) compare with
   `CONTRADICTS_REQUIREMENT`. `PROBE_NOT_APPLICABLE_REASON = CONTRADICTS_REQUIREMENT` (`:5335`); the name stays,
   because its role is a different reading of the same word.
2. `acceptance.py:748`: `CONTRADICTS_REQUIREMENT = C.CONTRADICTS_REQUIREMENT` (the alias stays, because
   `controller.py:7330`, `window_record.py:75`, `manifest_put.py:410`, `ledger.py:751` and `manifest_from_tests.py:954`
   import it).
3. Split `red_by_requirement` (`:851`) with no behaviour change. Extract:
   - `_red_source(report, strict, runs, root)`. It returns the closure `failed(names) -> bool` of today's
     `:896-925`, or `None` when today's code returns `{}` at `:908` (runs unreadable). The caller does
     `failed = _red_source(...)`, `if failed is None: return {}`.
   - `_rows_for_instance(rows, entry, iid, names, covered, bindings, cfg) -> (matched, turned_down)`: today's loop
     body `:939-959`, rows in manifest order.
   - The docstring stays whole on `red_by_requirement`. Each helper gets a 2-3 line docstring that names the error
     direction "not red".

Edge behaviour, with the invariant each protects:
- An unreadable report or run map still gives "not red". **Invariant:** a red that nobody explained never passes as
  explained, and a green one is never called red (FR-59).
- `refused` receives a sentence only in source (v-b), only for a failed instance that no row matched, and only the
  first turned-down row. **Invariant:** a green or unrun sibling of a red instance gets no refusal.
- Row order and the "every matching row, not the first" result (N1) are unchanged.
- The value of the word is unchanged, so no artifact on disk changes meaning.

AR: AR-13, AR-15. Grep the DoD quotes: `"contradicts_requirement"` in `contract.py` appears exactly once (the
definition), and in `acceptance.py` zero times as a code literal (docstrings may name the word in backticks).

### P2 — controller.py (hot, alone)

given: as P1, plus P1 merged
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\controller.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_red_window.py
non-goals: `HANDED_OUTCOME`, `BLOCKED_OUTCOME` and `PROBE_GAP_WORD` (`:226-233`), which are the same class (F7 finding); any import of `contract` or `acceptance` at module load
handoff: as P1
edges: see below
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/controller.py ai-packages/qa-factory/scripts/tests/test_red_window.py` plus every keep test it prints (non-SLOW), green
siblings: the sweep of `controller.py:225-237`, enumerated: `HANDED_OUTCOME` (queued, F7 finding, `contract.HANDED_TO_PERSON` exists); `BLOCKED_OUTCOME` (queued, F7 finding, no contract home); `PROBE_GAP_WORD` (queued, F7 finding, no contract home); `CONTRADICTS_WORD` (applied here)
designer: this file

Change:
1. Delete `CONTRADICTS_WORD` and its comment (`:234-237`).
2. `names_contradicts` (`:515`): add `import contract` as the first statement of the function body (controller
   imports `contract` lazily elsewhere: `:1543`, `:9195`, `:9350`). Return `contract.CONTRADICTS_REQUIREMENT in blob`.
3. `_s5_gap_problems` (`:7400`): replace `CONTRADICTS_WORD` by `CONTRADICTS_REQUIREMENT` (already imported at
   `:7330`).
4. `test_red_window.py:381-382`: delete row K1 ("the word the controller spells is the one the window gap
   carries"). It held two spellings equal, and there is now one. The behaviour rows `:384-395` stay and keep checking
   `names_contradicts`.

Edge behaviour:
- A payload that cannot be dumped still returns False. **Invariant:** error direction toward False (the docstring at
  `:523`). A pair that does not name the word is still refused (FR-10).
- **Load-time invariant:** `controller.py` still imports neither `contract` nor `acceptance` at module load. The DoD
  quotes `grep -n "^import contract\|^from contract\|^import acceptance" controller.py` with an empty result. Positive
  control: the same grep finds `^import event_store`.

AR: AR-13, AR-15. Census row 188 (`_s5_gap_problems`, xref, data) is unchanged.

### P3 — s5_precheck.py, s7_pretriage.py, stage_status.py

given: as P1, plus P1 merged
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\s5_precheck.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\s7_pretriage.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\stage_status.py
non-goals: the substring readers `s7_pretriage.py:129` and `driver_stage_s7.py:44`, which read the word inside `json.dumps` (spelling only here; the reading is queued in the F7 finding); `s5_precheck.SETTLED_STATUSES` (another fact); `s5_precheck.UNCHECKED_CHECKS` (`:76-79`, FV1-1's region); any finding text
handoff: as P1
edges: see below
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/s5_precheck.py ai-packages/qa-factory/scripts/s7_pretriage.py ai-packages/qa-factory/scripts/stage_status.py` plus every keep test it prints, green; plus `python -B ai-packages/qa-factory/scripts/stage_status.py --selftest` exits 0 (the flag exists, `stage_status.py:403`; its output goes verbatim into the witness)
siblings: P1, P2, P4, P5
designer: this file

Change:
1. `s5_precheck.py:110`: `CONTRADICTS = C.CONTRADICTS_REQUIREMENT`. The alias stays: `test_ahead_cards.py:63,247`
   and `test_s5_precheck.py` read `P.CONTRADICTS`.
2. `s5_precheck.py:3793` (docstring of `check_row_fields`): replace "no dispatch, an unknown id, or two running" by
   "no dispatch, an unknown id, or a dispatch with no scope". That is what `dispatch_scope` (`:450-466`) returns None
   for. Sweep of the same docstring block: no other claim about `dispatch_scope` in it.
3. Split `_check_blocked_then` (`:1419`) with no behaviour change. Extract:
   - `_blocked_then_target(case, then, tag, numbers, door_) -> dict | None`: the two `numbers` checks `:1442-1456`
     (unknown case file, Then not of the case), the finding or None.
   - `_blocked_then_blocker(case, then, tag, blocker, state, door_) -> dict | None`: the final branch `:1481-1493`.
   The order inside `_check_blocked_then` stays: shape -> seen -> target -> ran -> same-instance conflict -> blocker.
4. `s7_pretriage.py:58`: delete `CONTRADICTS` and use `C.CONTRADICTS_REQUIREMENT` at `:129` (no reader outside the
   module: Grep `s7_pretriage.CONTRADICTS` gives 0 hits; t-213 re-checked with a positive control).
5. `stage_status.py:181`: delete `RED_ON_PURPOSE`. In `reds_on_purpose` (`:184`) and in the selftest block that uses
   it (`:308-309`), add a function-local `import contract` and use `contract.CONTRADICTS_REQUIREMENT`. The module keeps
   no load-time `contract` import (it is a light status script).

Edge behaviour:
- `_check_blocked_then` gives at most one finding per row, with the same text and tag byte for byte. **Invariant:**
  a shape error still answers before everything. A Then that ran red still answers before the same-instance conflict
  (the comment at `:1458-1461` moves with its branch, unchanged).
- `stage_status` on a story with no manifest still gives `0`. The `--selftest` run exercises `reds_on_purpose` through
  the function-local import, so a missing import fails the DoD, not a later run.

AR: AR-13, AR-15.

### P4 — story_step.py, driver_stage_s7.py, gate_brief.py

given: as P1, plus P1 merged
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\story_step.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\driver_stage_s7.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\gate_brief.py
non-goals: the other words of `DERIVED_GAP_KINDS` (`blocked_by_env`, `handed_to_person`, `probe_gap`), which are the F7 finding's class; `"impossible"` at `gate_brief.py:4478`; the substring reading at `driver_stage_s7.py:44` (queued in the F7 finding)
handoff: as P1
edges: the values are unchanged; `DERIVED_GAP_KINDS` keeps its order (`test_probe_gap_word.py:680` compares the tuple)
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/story_step.py ai-packages/qa-factory/scripts/driver_stage_s7.py ai-packages/qa-factory/scripts/gate_brief.py` plus every keep test it prints, green
siblings: P1-P3, P5
designer: this file

Start: after P1 merged and after onboarding-hooks/4 (the existing line `очередь: onboarding-hooks/4 → onboarding-forge/2`;
`gate_brief.py` carries its unmerged commit `ca9cdf2`, `carried_concern_cases`, a disjoint region).

Change: `story_step.py:1614` uses `C.CONTRADICTS_REQUIREMENT` in place of the 4th literal. `driver_stage_s7.py:44`:
`contract.CONTRADICTS_REQUIREMENT` (`contract` is already imported at `:27` in the same function). The reason text at
`:45` becomes `contract.CONTRADICTS_REQUIREMENT + " rows"`. `gate_brief.py:4478`: `(C.CONTRADICTS_REQUIREMENT, "impossible")`.
AR: AR-13, AR-15.

### P5 — check_traceability.py, check_delivery.py, traceability.py

given: as P1, plus P1 and P9 merged (P9 brings the grammar heading constants)
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\check_traceability.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\check_delivery.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\traceability.py
non-goals: any change to a comparison other than its right-hand side; the READING of report sections at `traceability.py:1688-1698` (the F6 reader finding); OF4-27's region (`resolve`, `:1831-1840`)
handoff: as P1
edges: values unchanged
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/check_traceability.py ai-packages/qa-factory/scripts/check_delivery.py ai-packages/qa-factory/scripts/traceability.py` plus every keep test it prints, green; the grep `grep -nE "[\"']## (Decided at gate B|Left with you|Factory defects)" traceability.py` finds no code literal (positive control: the same grep in `grammar.py` finds the definitions)
siblings: P1-P4 (the word); P9 (the headings)
designer: this file

Start: after P1 and P9 are merged to the batch branch, and after OF4-27 (an uncommitted edit in `traceability.py`
`resolve`) is merged to `main`. The builder merges `main` into its tree first.

Change:
1. `check_traceability.py:67`, `check_delivery.py:2003` and `traceability.py:931` compare with
   `C.CONTRADICTS_REQUIREMENT` (all three import `contract as C` at load).
2. Report headings in `traceability.py` (t-213 B2, F6 a'; `grammar` is imported at load as `G`, `:37`):
   - delete `GATE_B_HEADING` (`:1624`), `LEFT_HEADING` (`:1625`) and `GATE_B_BEFORE` (`:1627`); no reader outside the
     module (Grep over `scripts/`: only `:1688`, `:1690`, `:1698`). Those three lines use `G.GATE_B_HEADING`,
     `G.LEFT_WITH_YOU_HEADING` and `G.FACTORY_DEFECTS_HEADING`. Keep the comment that explains why gate B goes before
     "Factory defects".
   - `:1612` `lines = ["## Decided at gate B", ""]` renders the gate-B block's heading: `[G.REPORT_BLOCK_HEADINGS["gate-b"], ""]`.

Edge behaviour: every string is byte-identical to today. **Invariant:** the gate-B section is inserted in the same
place (before "Factory defects", after "Left with you") and is never inserted twice.

AR: AR-13, AR-15.

### P6 — the Then-number reader in the ledger (ledger.py; manifest_from_tests.py alignment)

given: as P1, plus P1 merged; `contract.then_number` (`contract.py:226-244`, the reading rule)
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\manifest_from_tests.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\ledger.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_ledger.py
non-goals: any test row in `test_manifest_from_tests.py` (t-213 B1: no input reaches `_case_picture` with a non-int `then`); `manifest_from_tests.build` length (F4, queued); `ledger.py:120` (reads code-produced `then_oracle_states`, not a manifest row); `ledger.py:314` (`blocked` rows come from `contract.then_remainders`); the wider class (F5 finding)
handoff: as P1
edges: see below
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/manifest_from_tests.py ai-packages/qa-factory/scripts/ledger.py ai-packages/qa-factory/scripts/tests/test_ledger.py` plus every keep test it prints, green; the new `test_ledger.py` row fails on the pre-change `ledger.py` (the report shows the red run first, then the green run)
siblings: F5 finding (the other `isinstance(then, int)` readers)
designer: this file

Change:
1. `manifest_from_tests._case_picture` (`:1596-1597`): read each row's `then` through `C.then_number` and drop a 0
   (`covered = sorted({n for b in bindings if ... for n in [C.then_number(b["then"])] if n})`, the same for
   `unresolved`). **This is a behaviour-free AR-13 alignment, stated as such:** every row in `bindings` comes from
   `_then_numbers` (`:636-645`), an int >= 1, for which `then_number` returns the same int. No test row judges it; the
   keep rows of `test_manifest_from_tests.py` stay green.
2. `manifest_from_tests._contradicts_requirement` (`:949-955`): return `C.CONTRADICTS_REQUIREMENT`. Rewrite the
   docstring to "ONE home, `contract.CONTRADICTS_REQUIREMENT`". The old docstring becomes false after P1. Keep the
   function: its callers stay.
3. `ledger.plan_row_state` (`:866-868`): `n = C.then_number(binding.get("then"))`. The condition becomes
   `... and n and n in gaps ...` and the appended tuple uses `n` and `gaps[n]`.
4. Test row (a variant, no new file): `test_ledger.py`, beside the open-oracle rows (`:1007`, `:1090`), one
   parameterised table of a covered binding on a Then whose oracle is open, on a passed case:
   - `"then": "2"` (Then 2 open) -> `NOT_VERIFIED_UNCONFIRMED`, the words name Then 2. Before the change: not flagged
     (`isinstance("2", int)` is False) -> this row is the red-first row.
   - `"then": " 2 "` -> the same as `"2"`.
   - `"then": 2` -> `NOT_VERIFIED_UNCONFIRMED` (control: same before and after).
   - `"then": True` with Then 1 open -> per fork F9 (recommended: not flagged here; see the edge below).
   Each parameter id names the input.

Edge behaviour:
- ledger. **Invariant (AR-28):** a digit string now counts, so the change ADDS `green_open` hits for `"2"`, `" 2 "`,
  `"02"`. The ONE input that loses a hit is a bool: today `True` passes `isinstance(..., int)` and equals key 1, so it
  flags Then 1 by accident; `then_number(True)` is 0. Which way that goes is fork F9. Under the recommendation, the
  safety does not rest on the ledger: the S5 precheck reads every row through `then_number`
  (`s5_precheck.py:1265-1269`), so a covered row whose `then` is `True` covers no Then, and its clause is refused as
  unbound before the story reaches the ledger.
- Adversarial inputs that must stay on the safe side (never a new `passed_green` that a correct reading would flag):
  `"02"` (2), `" 2 "` (2), `"²"` (not ASCII -> 0), `2.0` (0, the same as today: a float is not an int), `[2]` (0, same
  as today), `"x"` (0, same as today), `True` (F9).
- `_case_picture`: no input changes; a crash today is impossible and stays impossible.

AR: AR-13, AR-28. Census: `plan_row_state` has no row today. Add none unless the census test asks.

### P7 — planning_contract.py: one `SETTLED_STATUSES`; `_apply_recorded` split

**dispatched t-218** (with fix m6: the DoD's "expect" list was dropped in the dispatch). Text below as dispatched.

given: as P1
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\planning_contract.py
non-goals: `question_register.py` (the survivor, unchanged); replacing the status test by `QR.settled(q)` (different meaning: `settled` also requires `_holds`, `question_register.py:376`)
handoff: as P1
edges: see below
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/planning_contract.py` plus every keep test it prints (expect `test_question_register.py`, `test_gate_preflight_question_status.py`, `test_question_branches.py`), green; the grep `SETTLED_STATUSES =` in `planning_contract.py` gives 0 hits (positive control: the same grep in `question_register.py` gives 1)
siblings: `test_gate_brief_and_retro.py:2937-2939` is a source pin on `gate_brief`, not touched
designer: this file

Change:
1. Delete `planning_contract.py:1527`. At `:2711` and `:2771` use `QR.SETTLED_STATUSES` (`QR` is imported at
   `:2663` in `_apply_gate_answers`). At `:3499` use `QR.SETTLED_STATUSES` (`QR` imported at `:3497`).
2. Split `_apply_recorded` (`:3496`) with no behaviour change. Extract:
   - `_reopened(q, intents, cases, key, answer, at, lines) -> (rework_items, record)`: the branch `:3548-3563`. It
     appends its line to `lines`, as today.
   - `_publish_plan(root, path, document, rows, md_changes)`: `:3572-3579`.
   - `_note_applied(root, records, where, by, out, lines)`: `:3580-3587`.
   `out["lines"]` and `out["rework"]` are still extended only at the end of `_apply_recorded`.

Edge behaviour:
- **Invariant:** a failed write reports nothing it did not do (comment `:3502`). The lines and rework go to `out` only
  after the pass got through. The plan is written once, before the records.
- **Invariant:** with no settled question nothing is read or written (early return).
- `planning_contract` still imports `question_register` lazily, never at load (comment `:1395`).

AR: AR-13.

### P8 — the stand block text: one builder

**dispatched t-219** (with fix m8: `docs/SIBLING_MAP.md` axis 26 updated in the same move). Text below as dispatched.

given: as P1
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\waiver.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\driver_stage_build.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\driver_stage_s6.py
non-goals: `stage_S6` length (F4); the duplicated "confirmed and passed by word" loop of `s6_no_stand` and `stand_check`; any driver member move (`fixtures/driver-layers.json` stays untouched)
handoff: as P1
edges: see below
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/waiver.py ai-packages/qa-factory/scripts/driver_stage_build.py ai-packages/qa-factory/scripts/driver_stage_s6.py` plus every keep test it prints (non-SLOW; expect `test_story_run_stand_identity.py`), green
siblings: none -- the text has exactly these two builders (Grep `is not confirmed as usable` over `scripts/*.py`: 2 hits)
designer: this file

Change: in `waiver.py`, right after `OWN_FORM_BLOCKS` (`:375`), add:
`def stand_block(environment: str) -> str:` returning
`f"{STAND_NOT_CONFIRMED_BLOCK}: " + (f"stand `{environment}` is not confirmed as usable" if environment else "no stand is confirmed for this story")`.
Give it a one-line docstring naming both callers. `driver_stage_build.py:102-103` and `driver_stage_s6.py:603-604`
call `waiver.stand_block(environment)`.

Edge behaviour:
- An empty environment gives the "no stand" text. The bytes are the same as today in both worlds. **Invariant:** a
  recorded word that passed the block before still passes it (`waiver.split_overridden` matches the same string), and
  a confirmed stand is never "no stand" (both callers return before building the block).

AR: AR-13, AR-15. Census row 824 (`stand_check`) is unchanged.

### P9 — report headings: one home each; the appendix: one reader

given: as P1; `grammar.py:94-180` (the section and block heading lists, the marker grammar)
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\grammar.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\report_facts.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\validate_artifacts.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_report_facts.py
non-goals: the READING of any section other than the appendix: `validate_artifacts._report_section_body` (`:1200`), `report_facts.left_with_you_text` (`:4339-4353`), `check_report_gate_b`'s `partition`/`split` (`:1464`), `traceability.py:1688-1698`, `human_text.section_problems` (all in the F6 reader finding: moving them changes fence and marker behaviour); `traceability.py` headings (P5); headings of OTHER artifacts in `validate_artifacts.py` (register, plan, charter, bug form, understanding: `:62-74`, `:130` are their homes; the re-spellings at `:530-534` and `:1948` go to the F6 finding); `tests/harness.py` and quarantined tests that call `RF._section_span(text, "## Appendix")` (they keep working); `form_selftest.py:285` (a sample report text, not a reader); any heading text change
handoff: as P1
edges: see below
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/grammar.py ai-packages/qa-factory/scripts/report_facts.py ai-packages/qa-factory/scripts/validate_artifacts.py ai-packages/qa-factory/scripts/tests/test_report_facts.py` plus every keep test it prints, green; the new `test_report_facts.py` row fails on the pre-change `validate_artifacts.py` (red run first, then green); and `grep -nE "[\"']#{2,3} [A-Z]" ai-packages/qa-factory/scripts/report_facts.py ai-packages/qa-factory/scripts/validate_artifacts.py` prints ONLY the lines this part lists as not applicable (below) plus the one definition of `SHOTS_HEADING` (positive control: the same grep over `grammar.py` prints the heading definitions)
siblings: P5 (traceability headings); the F6 reader finding
designer: this file

Change:
1. `grammar.py`, directly above `REPORT_SECTIONS` (`:103`), one named constant per report section heading:
   `PROVEN_HEADING = "## Proven"`, `BUGS_HEADING = "## Product bugs"`, `LEFT_WITH_YOU_HEADING = "## Left with you"`,
   `OPEN_QUESTIONS_HEADING = "## Open questions"`, `NOT_PROVEN_HEADING = "## Not proven"`,
   `GATE_A_HEADING = "## Decided at gate A"`, `GATE_B_HEADING = "## Decided at gate B"`,
   `FACTORY_DEFECTS_HEADING = "## Factory defects"`, `SIZE_HEADING = "## Size"`, `WHERE_TO_LOOK_HEADING = "## Where to look"`,
   `APPENDIX_HEADING = "## Appendix"`. Then `REPORT_SECTIONS` (`:103-105`), `REPORT_SECTIONS_AFTER_GATE_B` (`:107`),
   `REPORT_SECTIONS_WITH_BLOCKS` (`:112`) and the eight matching values of `REPORT_BLOCK_HEADINGS` (`:161`, `:163`,
   `:169`, `:171`, `:173-176`) use the names. Tuple order and every value stay as they are.
2. `report_facts.py` (one rule for every site: a line that RENDERS a block's heading uses
   `G.REPORT_BLOCK_HEADINGS[<block>]`, the precedent is `:3695`; a line that FINDS a section by its heading uses the
   `G.*_HEADING` constant):
   - `SLOTS` (`:77`, `:80`, `:81`): `G.LEFT_WITH_YOU_HEADING`, `G.FACTORY_DEFECTS_HEADING`, `G.APPENDIX_HEADING`.
   - `LEGACY_SECTIONS` (`:83-85`): `tuple((G.REPORT_BLOCK_HEADINGS[name], name) for name in ("proven", "bugs",
     "open-questions", "not-proven", "gate-a", "gate-b", "size", "where-to-look"))`, the same order and pairs as today.
   - Block renderers, the heading part only, suffixes kept byte for byte: `:1413`, `:1414`, `:1438` (`manual-checks`);
     `:3211` (`left-gate-b` + `" (from your answers)"`); `:3268` (`left-branches`); `:3279` (`branches-not-proven`);
     `:3300` (`regression` + `" (from the plan approved at gate A)"`); `:3471`, `:3473` (`proven`); `:3562`, `:3563`
     (`bugs`); `:3934`, `:3940` (`review-gaps`); `:3958`, `:3962` (`open-questions`); `:4002` (`not-proven` +
     `", and what it costs"`); `:4011` (`skipped-by-plan`); `:4017` (`gate-a`); `:4055` (`gate-b`); `:4140` (`size`);
     `:4271` (`where-to-look`).
   - Section finders: `:4350` (`left_with_you_text`), `:4485`, `:4720` -> `G.LEFT_WITH_YOU_HEADING`; `:4604` ->
     `G.GATE_B_HEADING`.
   - `:1321` and `:1324` spell `"## Screenshots of the manual checks"` twice in one function and nowhere in `grammar`:
     one module constant `SHOTS_HEADING` beside `SHOTS_HEAD`, used by both.
   - Delete `APPENDIX_HEADING` (`:4751`). Add the public reader `def appendix_span(text: str)`:
     `_section_span(text, G.APPENDIX_HEADING)`, `(start, end)` or None. Rename `_appendix_body` to `appendix_body`
     (two callers, `:4775` and `:4803`) and build it on `appendix_span`.
   - Not applicable (one spelling, no other home): `:473` (`### Test files the run could not collect`), `:3609-3610`
     (`EXPLORATORY_SECTIONS`, its home), `:3932` (`### Windows over the cap`), `:3943` (`### Runs left failing`).
3. `validate_artifacts.py` (it imports `grammar as G` at load, `:50`; for the appendix readers add a function-local
   `import report_facts as RF`: `report_facts` imports `validate_artifacts` only lazily, `:180`, `:191`, `:2658`,
   `:4549`, so there is no load cycle):
   - `LEGACY_REPORT_SECTIONS` (`:1158-1160`): `"## Check coverage"` -> `PTR_COVERAGE_HEADING` (`:130`),
     `"## Readiness within what was verified"` -> `PTR_READINESS_HEADING` (`:70`). Both defined above it.
   - `is_legacy_report` (`:1170`): `PTR_COVERAGE_HEADING in text and G.APPENDIX_HEADING not in text`. **Still a
     substring test** (t-213 M3, see the edge).
   - `check_report_traceability` (`:1255`): `_span, appendix = RF.appendix_body(text)`; the early `return` at `:1257`
     stays (`if not appendix.strip()`).
   - `check_report_forbidden` (`:1408`): `span = RF.appendix_span(text)`, `body = text[:span[0]] if span else text`.
   - `_authored_text`, the prose-budget cut (`:1972-1973`): the offsets are taken on `authored`, not on `text`:
     `span = RF.appendix_span(authored)`, `return authored[:span[0]] if span else authored` (t-213 M3).
   - `:1314` -> `G.LEFT_WITH_YOU_HEADING`; `:1356` -> `G.PROVEN_HEADING`; `:1461`, `:1464`, `:1548`, `:1549` ->
     `G.GATE_B_HEADING` (spelling only; the `partition`/`split` reading at `:1464` stays, F6 finding).
   - Delete `REPORT_HUMAN_HEADING` (`:1420`; no reader outside the module, Grep over `scripts/`: only `:1448`) and use
     `G.FACTORY_DEFECTS_HEADING` at `:1448`.
   - Not applicable: `:62-74`, `:130` (homes of other artifacts' headings); `:530`, `:534`, `:546`, `:555` (bug-form
     `## Cause` / `## Manifestations`, F6 finding); `:1754-1755` (`UNDERSTANDING_SECTIONS`, its home); `:1844`
     (message text); `:1948` (re-spells two `UNDERSTANDING_SECTIONS` entries, F6 finding); docstrings `:11`, `:132`.
4. Test row (one parameterised table, no new file; `test_report_facts.py` is a keep file and already calls
   `check_report_forbidden`): a marked report with a real `## Appendix` section at its end and a forbidden id (one of
   `REPORT_ID_SHAPES`) in the body ABOVE an earlier mention of `## Appendix`. Variants:
   - the mention is inside a fenced code block -> `check_report_forbidden` names the id (before the change: hidden,
     because `text.find` cut the body at the fence) -> red-first row;
   - the mention is mid-line (`see ## Appendix below`) -> names the id (red-first row);
   - control: the forbidden id stands only inside the real appendix -> no error, before and after.

Edge behaviour (behaviour changes, stated):
- The appendix is now the SECTION from its heading line to the next `## ` heading or block marker, outside code
  fences. Before, it was everything after the first substring match.
  - A section after the appendix (e.g. "## Retro proposals", seen in `test_report_facts.py:2735`) no longer counts as
    appendix rows in `check_report_traceability`. **Invariant:** a requirement or case named only outside the appendix
    is reported missing (refusal side, FR-59), never counted as present.
  - A mid-line or fenced mention of "## Appendix" no longer cuts the body in `check_report_forbidden` and in
    `_authored_text`. **Invariant:** the forbidden-id check and the prose budget can only see MORE text, so they can
    only refuse more, never pass a report that used to be refused.
- `is_legacy_report` stays a substring test. **Invariant (AR-28):** the legacy contract skips checks (e.g.
  `check_report_human_text` returns early). A section reading would move a report whose only `## Appendix` is fenced
  or mid-line onto the lighter contract, toward a pass. The substring test keeps every such report on the current,
  stricter contract, as today.
- No appendix: the same outcomes as today (legacy test, `return` at `:1257`, the whole body counted).
- Every heading constant has the value of the literal it replaces, so every rendered report is byte-identical.
  **Invariant:** `--check` of a report written before this part finds no stale block it did not find before.

AR: AR-13, AR-14, AR-15, AR-28. Census rows of the checks are unchanged (data; row 918 on main).

### P10 — execution_request.py: the retrying replace; `_observe_stand` split

**dispatched t-219** (with P8). Text below as dispatched. The count "42" in its non-goals is stale; the recount is in
§2 item 9 and F3 (41 sites in 33 files after P10).

given: as P1; `event_store.replace_file` (`event_store.py:177-190`)
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\execution_request.py
non-goals: the other 42 bare `os.replace` sites (F3); `build_mine_request` (F4); the serialization format of either file
handoff: as P1
edges: see below
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/execution_request.py` plus every keep test it prints (non-SLOW; expect `test_execution_request.py`), green; the grep `os.replace(` in `execution_request.py` gives 0 hits (positive control: the same grep gives 2 hits before the change)
siblings: F3
designer: this file (pending F3)

Change:
1. `from event_store import replace_file` at load (`event_store` imports only the stdlib). `JobStore.write` (`:411`)
   and `write_mine_request` (`:3869`): `replace_file(tmp, path)`. Keep `json.dumps(...)` and the `.tmp` naming
   exactly as they are.
2. Split `_observe_stand` (`:2786`) with no behaviour change:
   - `_probe_cwd(spec_or_probe, project_root) -> str`: today's two copies (`:2813-2816`, `:2839-2842`).
   - `_observe_precedent(runtime_precedent, policy, purpose, probe, probe_extra, project_root, evidence_only, notes, now) -> dict`:
     the branch `:2797-2835`.
   `now` is computed once in `_observe_stand`, as today.

Edge behaviour:
- `replace_file` retries only WinError 5/32 on Windows, up to 8 tries. Any other error is raised on the first try.
  After the last try it raises exactly as before. The `.tmp` file is left behind in that case, as today.
  **Invariant:** a write either lands whole or raises. It never silently drops a job record.
- `_observe_stand`. **Invariant** (its docstring `:2793`): every input refused here before is refused now, with the
  same class and opening words. A `ProvenanceRefused` under `evidence_only` still re-raises.

AR: AR-15 (the one retrying replace), AR-13. FR-31: the fix is in the code, not a retry in the test.

### P11 — the automator sees the sanctioned masking paths (F2 decided: option d, with the M4 correction)

given: as P1; `references/inject-map.json`; `references/role-load.json`; `scripts/role_load.py` (`process_ratchet_problems`, `:259-282`: slack 0 both ways); `design/role-rules.json` row `commented-out-then-path` (`:74`)
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\artifact-contract-automation.md
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\code-review-rubric.md
C:\QAFactory\forge-repo\ai-packages\qa-factory\agents\qa-automator.md
C:\QAFactory\forge-repo\ai-packages\qa-factory\design\role-rules.json
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\role-load.json
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\slices\
(only the slices `scripts/contract_slices.py --write` regenerates)
non-goals: `inject-map.json` (option d adds no entry); the critic's charter; any other dimension of the rubric; other rows of `role-rules.json` (oh3-9 edits other rows)
handoff: as P1, plus the before/after numbers of `python -B ai-packages/qa-factory/scripts/role_load.py --all` for qa-automator and qa-code-critic (total and process), verbatim
edges: see below
DoD: `python -B ai-packages/qa-factory/scripts/contract_slices.py --write`, then `python -B ai-packages/qa-factory/scripts/contract_slices.py --check` (exit 0), then `python -B ai-packages/qa-factory/scripts/role_load.py --all` (the four rows equal the measured values), then `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for` with every owned path (the slices included) plus every keep test it prints (expect `test_role_rules.py`, `test_contract_slices.py`, `test_role_load.py`, `test_manifest_from_tests.py`), green
siblings: `references/slices/qa-code-critic/artifact-contract-automation.md:68` and `references/slices/qa-automator/artifact-contract-automation.md:68` (regenerated); `judgments.json:275` "rubric dimension 8" is the CASE critic's rubric, not applicable
designer: this file

Change (option d):
1. `artifact-contract-automation.md:70`: replace "A commented-out Then: rubric dimension 8." with the closed list
   moved from `code-review-rubric.md:74-76`, word for word: "A check that does not pass is legitimate only on a
   sanctioned path: `Known defect: BUG-n` + `red_lock`; an honest failure; a `legitimate_correction` (an
   `expectation_changes[]` row); or a commented-out Then with its reason, its `then_bindings` row with reason
   `handed_to_person` or `blocked_by_check`, and its Left with you line."
2. `code-review-rubric.md` dimension 8 (`:74-76`): "Without a sanctioned path (`artifact-contract-automation.md`, the
   list beside `retracted_unresolved`) -> fail." Dimension 6's "dimension-8 sanctioned path" (`:65`) stays: it is the
   anchor of `no-commented-out-checks`.
3. `agents/qa-automator.md:72`: "(commented out: rubric dimension 8)" becomes "(commented out: the contract's
   sanctioned paths)".
4. `design/role-rules.json:74` (`commented-out-then-path`): carrier anchors become "a commented-out Then with its
   reason" with file `references/artifact-contract-automation.md`, "the contract's sanctioned paths" in
   `agents/qa-automator.md`, and the rubric anchor "Without a sanctioned path". Edit the `rule` text to "(the
   contract's sanctioned paths)".
5. `role-load.json` (t-213 M4): set EACH of the four rows — `ratchet_tokens.qa-automator`,
   `process_ratchet_tokens.qa-automator`, `ratchet_tokens.qa-code-critic`, `process_ratchet_tokens.qa-code-critic` —
   to the value `role_load.py --all` measures AFTER the edit, in either direction (the process rows have slack 0: a row
   above or below the measured load is red). Before the edit, t-213 measured 20,181 / 18,614 (automator) and
   19,389 / 17,566 (critic), each equal to its row. The commit message and the report name every moved row as
   `<key>.<role>: <old> -> <new> (<reason>)`; the diff critic's verdict repeats them (AR-20, SIBLING_MAP axis 18,
   critic brief q.9). The raise is decided by the Lead (F2, «по рекомендации, до слова владельца»).

Edge behaviour:
- **Invariant:** no rule leaves the registry. Every anchor of row `commented-out-then-path` stands in its carrier after
  the edit (`test_role_rules.py`).
- The critic still reads the full list, through its own slice of the same contract section. If
  `contract_slices.py --check` shows the section is NOT in the critic's slice, stop and return the question. Do not add
  markers by guess.
- The critic's net can be POSITIVE: its slice grows by the moved list while its rubric shrinks by a shorter pointer.
  A growth is set like any other move (step 5). **Invariant (AR-20):** no row moves without its line in the commit and
  the verdict.
- If EITHER role's measured total or process load grows by more than 200 tokens, stop before editing `role-load.json`
  and return the four numbers. The Lead decides.
- A row lower than before (a shrink) is set too: leaving it higher is red (slack 0), and lowering is never a raise.
- FR-33: a role-text change is "closed by code, not proven" until a `live-runs` row is cleared (PROJECT.md «Командная
  работа» p.9). The part adds that row to its batch's "Живые доказательства".

AR: AR-10, AR-11, AR-20, AR-15 (one home of the list: the contract). Owner: judgment (the automator), accepted by the
code critic. Census: not a code check.

---

## §5 Forks

Decided by the coordinator in t-220, «по рекомендации, до слова владельца» (the owner can still overturn each):

- **F1 — width of item 1: (a), all 14 spellings in the 12 files**, in P1-P5 (one road, P31, AR-15). The data-file
  spellings (`handoffs/vocabulary.yaml:65,107`, `references/*.json`) are AR-1 data pinned by `test_handoff.py:90` and
  stay out (t-213). «по рекомендации, до слова владельца».
- **F2 — the automator gets the sanctioned paths: (d), with the M4 correction.** The home is
  `artifact-contract-automation.md`, which both roles get as a slice; the rubric points there. All four `role-load.json`
  rows of the two roles are set to the measured value, each named row by row (P11 step 5). The raise is the Lead's word
  as a verdict-named act (AR-20); the owner's word is not needed (t-213: `threshold_confirmed_by` concerns the threshold,
  not the ratchet). P11 is one node (a split leaves `test_role_rules.py` red between halves). «по рекомендации, до слова
  владельца».
- **F3 — item 9: (a).** P10 uses `event_store.replace_file` (dispatched t-219). A NEW finding covers the remaining 41
  bare `os.replace` sites in 33 files (t-213 recount; an AR-15 class that needs its own decomposition). **Pile:
  `package-ci`** (the race surfaced as an FR-31 flake under load on Windows hosts). «по рекомендации, до слова владельца».
- **F4 — long functions: (a).** The four new ones are split now (P1, P3, P7, P10). The six grown ones
  (`build_mine_request`, `manifest_from_tests.build`, `window_record.build`, `ledger.plan_row_state`,
  `acceptance.validate_window`, `driver_stage_s6.stage_S6`) go to batch-2 «Остатки» as `перенос:` lines with a human's
  confirmation (PROJECT.md «Командная работа» p.9); each needs its own design read and critic. «по рекомендации, до
  слова владельца».
- **F5 — the wider Then-number class: as the critic agreed.** One scout dispatch classifies the ten
  `isinstance(then, int)` sites (`contract.py:338,393,1140,1632,1650,1761`, `planning_contract.py:2080`,
  `question_register.py:1267`, `s5_precheck.py:1735`, `manifest_put.py:1285`) as shape VALIDATORS (rightly refuse a
  string) or READERS (should use `then_number`). A finding carries the question; its result opens a node. Not in
  HF8-4. **Pile: `onboarding-forge`** (item 3 of its HF2-0 finding). «по рекомендации, до слова владельца».
- **F6 — the sweep of the same artifact for P9: (a') as the critic proposes**, replacing the original wording. P9 takes
  a grammar constant for every report heading its three files spell (the full enumeration is in P9, wider than the
  t-213 list: the fix round also found `validate_artifacts.py:1461/1464`, `report_facts.py:4604`, the block renderers
  and `traceability.py:1612/1624`). `traceability.py`'s headings go to P5 (after OF4-27). A NEW finding covers what is
  not behaviour-free: (i) the section READERS — `validate_artifacts._report_section_body` vs `report_facts._section_span`
  (an AR-13 twin; fences and block markers differ), plus `report_facts.left_with_you_text`, `check_report_gate_b`'s
  `partition`/`split`, `traceability.py:1688-1698` and `human_text.section_problems`; moving them changes behaviour on
  at least 4 checks; (ii) the heading re-spellings of other artifacts in `validate_artifacts.py` (`:530-534` bug form,
  `:1948` vs `UNDERSTANDING_SECTIONS`); (iii) report headings spelled in modules outside P5/P9 (not swept here; the
  finding's first step is a grep with a positive control). **Pile: `report-delivery`**. «по рекомендации, до слова
  владельца».
- **F7 — controller siblings: as the critic agreed.** A NEW finding and node: "one home in `contract` for every closed
  gap/outcome word (`blocked_by_env`, `handed_to_person`, `probe_gap`)" — `controller.py:225-233`,
  `acceptance.py:27,41,53`, `contract.py:112`, `s5_precheck.py:199`, `story_step.DERIVED_GAP_KINDS`. It also carries
  the READER twin (t-213 m9): `driver_stage_s7.py:44` and `s7_pretriage.py:129` both read "the word anywhere in
  `json.dumps(entry)`" (s7_pretriage's docstring says "as the driver finds it") -> one reader for "a manifest row
  carries the red word". Not in HF8-4, so P2 stays a one-word diff in a hot file. **Pile: `onboarding-forge`**
  (continuation of item 1's class). «по рекомендации, до слова владельца».

Each new finding lands, in the same move as its file in `findings/`, as a node line in an UNtaken batch of its pile
(D-0044), and as a row in the pile card's «Содержание». This is the Lead's move at acceptance, not a builder's.

Open — returned to the Lead (new in t-220):

- **F8 — direction of the `contract.py` queue line (M5).** The line must stand in both preambles before P1 starts.
  (a) `очередь: onboarding-forge/4 → onboarding-forge/2`: OF4-25 lands first; P1's builder merges `main` before
  committing. (b) `onboarding-forge/2 → onboarding-forge/4`: batch-4 waits for HF8-4's PR. The edits are disjoint by
  line, so either works textually. **Recommend (a):** batch-4's file and OF4-25 are already in flight, and batch-2's
  PR lands only after all eleven parts and wave 2, so /2 is the later one in fact. Writing the line into batch-4's
  preamble means touching `wip/of-batch4`; that is the Lead's or that batch's owner's move.
- **F9 — a bool `then` in the ledger (P6), an edge the fix round found in my own P6.** Today
  `isinstance(True, int)` is True and `True in gaps` matches key 1, so a covered binding with `"then": true` flags Then
  1 as green-on-open by accident. `then_number(True)` is 0, so after P6 that hit is gone. (a) Follow the one reader
  (AR-13): not flagged in the ledger. Safety rests on the S5 precheck, which reads every row through `then_number`
  (`s5_precheck.py:1265-1269`) and refuses the clause as unbound, so such a row does not reach the ledger as coverage.
  The P6 table row for `True` expects "not flagged". (b) The ledger flags any covered binding whose `then` reads 0 on a
  passed case with an open oracle as `NOT_VERIFIED_UNCONFIRMED` ("a test bound to no readable Then"). That is stricter,
  but it also starts flagging `"x"` and `[2]`, which are not flagged today, and the words need a new sentence. (c)
  Special-case bool in the ledger: a second reading, refused by AR-13. **Recommend (a).** P6 is executable by the
  recommendation until the Lead answers; under (b) the `True` row and a new `"x"` row expect `NOT_VERIFIED_UNCONFIRMED`.

## §6 Small choices I closed (no design weight; listed so the Lead can stop them)

- a. Survivor homes: `contract.CONTRADICTS_REQUIREMENT` (the lowest module that the vocabulary `UNRESOLVED_REASONS`
  already lives in). `question_register.SETTLED_STATUSES` (the register owns question statuses). `waiver.stand_block`
  (beside `STAND_NOT_CONFIRMED_BLOCK`, a pure function. A driver-mixin method would need a `driver-layers.json` home).
  `grammar.*_HEADING` and `grammar.REPORT_BLOCK_HEADINGS` (every reader imports `grammar` at load) with the reader
  `report_facts.appendix_span` (the writer of the section). `event_store.replace_file` (the existing one retrying replace).
- b. Lazy imports where a module avoids a load-time import today: `controller.names_contradicts`, `stage_status`, and
  `validate_artifacts` -> `report_facts`.
- c. Aliases are kept ONLY where a reader outside the module exists: `acceptance.CONTRADICTS_REQUIREMENT`,
  `contract.PROBE_NOT_APPLICABLE_REASON`, `s5_precheck.CONTRADICTS`. Names with no outside reader are deleted:
  `controller.CONTRADICTS_WORD`, `s7_pretriage.CONTRADICTS`, `stage_status.RED_ON_PURPOSE`,
  `validate_artifacts.REPORT_HUMAN_HEADING`, `traceability.GATE_B_HEADING` / `LEFT_HEADING` / `GATE_B_BEFORE`.
- d. `_case_picture` change 1 is KEPT as a behaviour-free AR-13 alignment (t-213 allowed keep or drop): the module
  then reads `then` through one reader everywhere. It drops a 0, which cannot occur.
- e. `_appendix_body` is renamed public `appendix_body`, because `validate_artifacts` now calls it.
- f. P11 has 5 authored files, over the 1-3 guide, because the anchors and texts must move in one commit.
- g. P9: one rule decides between the two survivors of a heading: a block renderer uses `G.REPORT_BLOCK_HEADINGS[name]`
  (precedent `report_facts.py:3695`); a section finder uses the `G.*_HEADING` constant. Both resolve to the one constant.
- h. P9: `is_legacy_report` keeps the substring test (t-213 M3 recommendation): it is the safe direction (the stricter
  contract), and it keeps the site behaviour-free.
- i. P9: `LEGACY_SECTIONS` is built from `REPORT_BLOCK_HEADINGS`; the pairs are exactly that mapping.
- j. P9's test row goes into `test_report_facts.py` (a keep file that already calls `check_report_forbidden`), not
  `test_validators.py`.
- k. Piles of the new findings (t-213 m10): F3 `package-ci`, F5 `onboarding-forge`, F6 `report-delivery`, F7
  `onboarding-forge`.
- l. Census row numbers updated to t-213's count on main (188, 826, 918); P8's "824" stays (dispatched text).

## §7 Reading trail

Read (draft): the finding (whole); `contract.py:60-104, 215-274, 2565-2584, 5325-5344`; `controller.py:225-240, 500-531,
7325-7404`, imports; `acceptance.py:740-967` and the def/const list; `s5_precheck.py:450-482, 1397-1495, 3786-3797`,
the def list; `planning_contract.py:1518-1529, 2695-2774, 3454-3591`, imports and the def list;
`question_register.py:78-87`, imports; `manifest_from_tests.py:1560-1603`, the def list; `ledger.py:181-203,
300-325, 845-873`, the def list; `execution_request.py:1-27, 382-421, 2786-2858, 3856-3870`, the def list;
`event_store.py:80-190`, imports; `driver_stage_s6.py:585-623`, imports, the method list; `driver_stage_build.py:68-117`,
imports; `driver_stage_s7.py:1-47`; `stage_status.py:170-194`, imports; `waiver.py:362-381`; `validate_artifacts.py:1160-1174,
1240-1274, 1398-1417, 1962-1979`; `report_facts.py:39-87, 4307-4357, 4745-4770`; `grammar.py:96-107`;
`code-review-rubric.md:1-90`; `inject-map.json` (whole); `test-code-patterns.md` (marker list, `:140-159`);
`role-load.json` (whole); `role-rules.json:72-74`; `contract_slices.py:180-202`, flags; `brief_pack.py:1813-1815,
1890-1914`; `scenario_walk.py:11-47, 860-930`; `test-layers.json` (keep and quarantine name lists, rows of
test_one_source_per_fact, test_red_window, test_report_facts, test_ledger, test_manifest_from_tests);
`judgment-census.json:1-15`, rows grep; `docs/TESTING.md` (whole); `test_gate_brief_and_retro.py:2930-2941`.

Read (fix round t-220, main): the review `t-213-t-205-plan-review.md` (whole); `manifest_from_tests.py:632-647,
1525-1604` (B1 confirmed: `_case_picture` gets marker `bindings`, `_then_numbers` refuses non-int); `contract.py:224-245`
(`then_number`); `ledger.py:858-871` (bool edge, F9); `manifest_put.py:1455-1475`; `s5_precheck.py` `then_number` uses
(`:666-668, 900-908, 1263-1269, 1332-1337, 1471-1475, 1535-1541, 1623-1627, 1676-1683`); `grammar.py:94-183`;
`report_facts.py:68-89, 4320-4355, 4748-4807`; `validate_artifacts.py:60-135, 1145-1219, 1248-1261, 1400-1469,
1959-1974`; `role_load.py:255-283` (M4 confirmed: slack 0 both ways); `stage_status.py:396-415` (m7 confirmed);
`batch-2-onboarding-roles-forge-p3.md:1-20` and the HF8-4 row (M5 confirmed); journal `logs/journal/dev1.jsonl:581-582`
(t-218 = P7 + m6, t-219 = P8 + P10 + m8).

Greps (fix round, each negative with a positive control): `"## (Left with you|Proven|Factory defects|Decided at gate B|Appendix)`
over the four report files; `["']#{2,3} [A-Z]` over `report_facts.py`, `validate_artifacts.py` and `grammar.py` (the
P9 enumeration); `REPORT_HUMAN_HEADING|LEFT_HEADING|GATE_B_BEFORE|GATE_B_HEADING|LEGACY_REPORT_SECTIONS` and the
`grammar` importers over `scripts/` (no outside reader of the deleted names; control: the definitions hit);
`REPORT_BLOCK_HEADINGS[` (precedent `report_facts.py:3695`); `check_report_forbidden|is_legacy_report` over `tests/`
(10 in `test_report_facts.py`); `test_validators|test_report_facts|"quarantine"` in `test-layers.json` (both keep);
`def section_problems` in `human_text.py`; the HF8-4 cell for six file names (control: `contract.py` hits); the pile
batch list (piles `package-ci`, `report-delivery`, `onboarding-forge` exist).

Not read, so not claimed: `design/architecture.md` and `design/factory-rules.md` in full. I worked from the generated
indexes loaded with CLAUDE.md. The AR-n "change check" columns above are mine. A builder of a package part still gets
`factory-rules.md` whole (PROJECT.md p.1). `docs/SIBLING_MAP.md` was not read by me (t-213 walked axes 5, 18, 26, 32,
34). The axis enumeration (rule 10(b)) is the committing builder's or the Lead's duty, per commit. I did not re-verify
t-213's worktree overlap scan (M5 bullets on FV1-1, oh3-9, agent-a365d2) or its census row numbers; they are carried as
t-213's facts.

## §8 Fix round t-220: review item -> applied / how

| item | applied? | how |
|---|---|---|
| B1 (P6) | applied, re-verified | §2 item 3 restated (ledger only live). P6: the `test_manifest_from_tests.py` row, its owns line and its DoD clause removed; change 1 kept as a stated behaviour-free alignment (§6-d). The red-first row is the `test_ledger.py` `"2"` row, whose input reaches `plan_row_state`. New edge found: a bool `then` -> F9 |
| B2 (P9) | applied as F6 (a'), wider than t-213's list | P9 enumerates every heading literal of its three files (sites t-213 missed: `validate_artifacts.py:1461/1464`, `report_facts.py:4604`, the block renderers, `:1321/1324`, `LEGACY_REPORT_SECTIONS`). Not-applicable lines are named, and the DoD grep allows only them. `traceability.py:1612/1624/1625/1627` -> P5. The second reader `_report_section_body` and four other section readings -> the F6 finding |
| M3 (P9) | applied | `is_legacy_report` stays a substring test, with an AR-28 invariant; the budget cut uses `authored`; one parameterised row in `test_report_facts.py`; §3 "tests asked for" updated |
| M4 (P11) | applied, re-verified | step 5 sets all four rows to the measured value either way, each named row by row; the 200-token stop covers either role; the critic-growth edge is stated |
| M5 (zones) | applied | §3 "Zone records" (cell list into «Ход», the queue line, the census conflict); P1 start gate; direction -> F8 |
| m6 (P7) | applied in the t-218 dispatch | P7 text unchanged, noted |
| m7 (P3) | applied, re-verified | `stage_status.py --selftest` is a definite DoD line (exit 0) |
| m8 (P8) | applied in the t-219 dispatch | P8 text unchanged, noted |
| m9 | applied | the reader twin is in the F7 finding; P3/P4 non-goals point there |
| m10 | applied | one pile for each of F3, F5, F6, F7 (§5, §6-k) |
| small stale facts | applied | census rows 188/918 (P8's 824 left: dispatched); `os.replace` recount in §2 item 9 and F3 |
| forks F1-F7 | written as decided | «по рекомендации, до слова владельца» |
