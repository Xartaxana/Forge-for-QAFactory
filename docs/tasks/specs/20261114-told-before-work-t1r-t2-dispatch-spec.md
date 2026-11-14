# Told before work: T1r and T2 dispatch addendum (draft, designer, t-677)

Status: DRAFT for Lead acceptance. Forks are returned (§8) and decided nowhere in this file. Where a node section depends
on a fork, it says so and gives the recommended option, so a builder can execute it once the Lead accepts the fork.

Parents:
- `docs/tasks/specs/20261113-told-before-work-mechanism-spec.md` ("parent": §2.4 T2 design, §5.1 to §5.6 row lists).
- `docs/tasks/specs/20261113-told-before-work-t1-revision-spec.md` ("revision": §3.4 key table, §3.5a counters, §4 lines 461 to 467, §9 (c)).
- Wave-0 row drafts: `wave0-rows.md`, `wave0-rows-part2.md`, `wave0-rows-part3.md`, with Lead decisions F-W1..F-W8, F-P2-1..7, O-1.

Base: origin/main as read through `C:\QAFactory\forge-repo\.claude\worktrees\read-main` on 2026-11-14 (merge `eb6dd02`
and the T1 topic merge `12317b6` / `6d9ecb4`). `W` below = `C:\QAFactory\forge-repo\ai-packages\qa-factory`. Read
facts were taken from `read-main\ai-packages\qa-factory\...`.

---

## §0 Facts: what is on main, and where the specs disagree with the merged code

### §0.1 Already on main (T1 a/b/c merged)

| fact | carrier (read-main) |
|---|---|
| Rows schema v2 readers exist: `load_rows` / `row_for` (exact id, else `<stem>:*`, two rows → the first plus a why) / `rows_for` / `told_text` / `fill` / `told_line` | `scripts/stage_joints.py` 419-433, 449-460, 522-536, 560-572, 575, 582 |
| `told_ratchet` = {hand_cards 12, legacy_legs 9, unsited 0}; `gaps` ratchet 5 | `references/stage-joints.json` 1142-1144, 1116 |
| Census-side counters `rowless 55` (dense), `untold 253` (ceiling), 220 units, per-unit bare/tagged | `scripts/tests/fixtures/told-ratchet.json`; t1c report step 0 |
| The 55 rowless ids: EG-digest-form, EG-s5-plan-outputs, EG-text-end, adviser; 25 PT-* (24 of parent §5.3 rows 1-24 plus PT-doctor-probe); IC-native-packet-unwritten, IC-oversized-slice; SD-managed-stage, SD-stage-close; 22 SG-* (SG-command, SG-walker-error and 20 G-dispatch ids) | `docs/tasks/specs/reports/20261113-t1c-report.md` lines 12-21 |
| `check_ids` (wide-scan `check` field), `sited_ids` = universe ∪ check_of(REGISTRY) ∪ check_ids, `_is_sited` sub-id rule | `stage_joints.py` 283-310, 313-318, 321-323 |
| `CHECK_PASSTHROUGH = {("exit_gate.py", "own"): 1}`; `_passthrough` resolves only bare-name call sites in the same file; a listed def with zero literal call sites is a walk error | `scripts/refusal_registry.py` 84, 1367-1408 |
| `RECORD_SINKS = ("block","deny","refuse","run_guarded")`, `RECORD_CALLS = {"refusal":0,"with_check":1}`; `_record_kind` binds `refusal` / `with_check` to detector_verdict per file | `refusal_registry.py` 79-83, 1321-1334 |
| `Record(str)` with `check` / `tag`, `check_id`, `with_check` (node N0) | `scripts/detector_verdict.py` 94-113, 116-127, 130-138 |
| `refusal` and `spoken` do NOT exist; T2 is not started | `detector_verdict.py` (whole file; no def of either name, case-insensitive Grep; positive control `def with_check` found) |
| The adviser never blocks: `run_advisers` always returns `[]`; it is wrapped `own(run_advisers(...), "exit_gate:adviser")` | `scripts/exit_gate.py` 676-687, 1893, 1903 |
| `contract_slices.requirement_section` is absent, so T3a is NOT merged; `_page_leg` reds every `{"page": true}` told with "the page renderer is not present" | `stage_joints.py` 676-706; `scripts/contract_slices.py` (no such def) |
| `agents/` holds 12 `qa-*.md` files and no `conductor.md` | Glob `read-main\ai-packages\qa-factory\agents\*.md` |
| `test_stage_joints.py` is about 146 s (slow); `slow_tests.json` still lists 67.6 s | topic-fix report lines 51-53 |

### §0.2 Statements of the two specs that the merged code contradicts

| # | spec statement | what the code says | consequence |
|---|---|---|---|
| C-1 | Brief: "everything waits on T1r and T2" | Parent §5.1: T1r depends on T1 **and T3a merged first**; T3a depends only on T1 (merged). `_page_leg` is red for every page told until `requirement_section` exists | T3a can go now; T1r cannot land its page legs before T3a. Fork F-1 |
| C-2 | Revision §4: "T1r lowers rowless to 0 ... T1r has no census rows" | `rowless` counts ids with no row. T1r can row 30 of the 55: 24 PT, SG-command (through its sub-id rows), SG-walker-error (row 31), 3 EG, adviser. 25 remain: PT-doctor-probe, IC-native-packet-unwritten, IC-oversized-slice, SD-managed-stage, SD-stage-close, and 20 G-dispatch SG ids. They have no drafted sentence, and their roads go through T4 (relabels), T7f (SD, F-W2) and an unowned `collect_blocks` (IC-oversized-slice) | rowless after T1r = 25, not 0. `rowless` is dense, so each later node lowers it by the ids it rows. Fork F-2 |
| C-3 | Revision §4: "aggregator rows stay sentence-less" with parent E16 "legacy_legs → 0" | L3 is the legacy leg of `exit_gate:witness_errors`, an aggregator key (`stage-joints.json` line 172) | Sentence-less and legacy-free agree only when L3 is re-pointed to the key page `references/slices/qa-code-critic/handoff-keys.md` with anchor `## Witness` (its sibling entries already use that anchor). §2 item T1r-6 |
| C-4 | Accepted F-W7 (a), wave0 item 7: the L1-L9 "new leg" points at agents / artifact-contract files | `_legacy_legs` (`stage_joints.py` 1028) counts every leg whose path is not `KEY_PAGE` for its role. A leg on `agents/*.md` or on `artifact-contract-*.md` stays legacy | F-W7 (a) as drafted keeps legacy_legs at 9 and E16 can never close. It misreads "key page" (it cites parent §2.8, which is about roads). Fork F-3, with the uniform translation recommended (§2.3) |
| C-5 | Parent §2.2: `stages: ["*"]` means every stage | `_row_problems` (`stage_joints.py` 898-932) demands every `stages` item be a stage id, so `["*"]` is red | Rows with `roles: *` / `stages: *` (EG-text-end, the adviser) are red until the stage line accepts `"*"`. T1r owns that line (item T1r-2) |
| C-6 | Parent §2.3: a page told needs no demands tokens | `_demands_leg` (`stage_joints.py` 761-784): an entry with page-only told and `demands: []` gives "the demands leg is missing" (red) | Every page row is red. T1r owns the page branch of `_demands_leg` (item T1r-3) |
| C-7 | wave0 item 8: row 28 split as `stage_guard:commit.pathspec` / `stage_guard:commit.manifest` | `_is_sited` counts a row as sited only when its id is a sited id or a dot-extension of one. `commit.pathspec` extends no sited id; the sited id is `SG-command` | The ids become `stage_guard:SG-command.commit.pathspec` / `stage_guard:SG-command.commit.manifest`. Row 31 (pointer to row 22) is kept as its own row `stage_guard:SG-walker-error`: K1 needs a row for that id. Small choice S-3 |
| C-8 | Parent §2.4: `refusal()` call sites are sited "by the scanner" | `_scan_wide` (`refusal_registry.py` 1483-1490) records no id for a bound `refusal(...)` call outside a transport. Only `emit` (1460-1473) sets `rec["check"]`. `r = refusal("x:y", ...)` followed by `block(r)` is never sited | T2 makes the scanner emit a `check_id` record for every bound literal `refusal` / `with_check` call (item T2-8) |
| C-9 | Revision §4: "refusal's pass-through becomes a CHECK_PASSTHROUGH line" | `_passthrough` resolves call sites in the same file only. `refusal` lives in `detector_verdict.py`; its callers live in other files. Listed as-is, it is a walk error (zero same-file literal calls) | T2 writes the cross-file call-site rule (§3.2) |
| C-10 | Parent §2.4: absent row → "(the factory's requirement row <id> could not be read: <why>; ...)" | `row_for` returns `(None, why)` for an absent or broken file, and for an id with no row. `rows_for` returns `[]` silently (t1c L2) | `refusal` must use `row_for`, never `rows_for` (item T2-3) |
| C-11 | Parent §5.1 T1r owns "test_ahead_cards / test_role_rules ... hand_cards → 0" | The 12-card → row mapping is drafted nowhere (`references/ahead-cards.json`: 12 `{sources, text}` paragraphs; no wave-0 file maps them) | A builder cannot execute the cards part from any file. Fork F-4 (split it out) |
| C-12 | wave0 item 4 / F-P2-3, F-P2-6 accepted `profile.none` and `fingerprint` as rows; N4 says sides.pending / sides.provisional are "replaced"; O-1 corrects stage_done:set | none of the five has a requirement sentence in any draft | They are held out of T1r until the Lead writes the sentence. Fork F-5 |
| C-13 | Parent §5.5 / part3 `waiver:carry.*` rows | `waiver:carry.old_key` needs the `move:words_carry` moves row, which T9c adds (F-P1 (a)) | `waiver:carry.call` and `.old_key` land with T9c, not T1r. Small choice S-4 |
| C-14 | Parent conductor rows (wave0 F-W4 (b) `planning_contract:plan.unmarked_revision`; part3 `controller:rework.*` producer "conductor") | `_producer_leg` needs `agents/<role>.md`; there is no `agents/conductor.md` | A row whose producer is the conductor is red today. Fork F-6 |
| C-15 | `test_stage_joints.py` `told_real` asserts `check_in("K1-lit/adviser-counted ...", "exit_gate:adviser", rowless)` (808-825) | It asserts the adviser IS rowless | Once T1r writes the adviser row, this row inverts: T1r rewrites it to assert the adviser is NOT in rowless (item T1r-9) |

---

## §1 Architecture invariants, owners and census class

Both nodes touch `ai-packages/qa-factory/` (CLAUDE.md rule 10, AR-29, P27).

| AR | node | how it is kept | change check written into the DoD |
|---|---|---|---|
| AR-10 a check's requirement reaches the role before the work | T1r (rows carry the sentence), T2 (the refusal speaks it) | T1r writes the rows; T2 reads them at refusal time through `row_for` | T1r: `stage_joints.py --check` green with the counters of §2.5. T2: test rows T2-a..T2-i |
| AR-13 a fact with a reader function is read only through it | T2 | `refusal` reads only through `row_for` / `told_text` / `fill`; no second JSON open | T2 test row "reads only via row_for" (monkeypatched reader seen) |
| AR-14 one artifact, one writer | T1r | `stage-joints.json` rows written by T1r only in this wave; `told-ratchet.json` written by T1r only | owns comparison §4 |
| AR-15 one survivor, wired everywhere | T2 | one constructor `refusal`, one renderer `spoken`; block / deny / refuse print it | T2 rows d, e, f |
| AR-18 one output shape, one reader | T2 | Record is the one shape; sinks accept Record or str | T2 row "Record vs str" |
| AR-20 shrink-only ratchets | T1r | `rowless` 55 → 25 (dense), `legacy_legs` 9 → 0, `hand_cards` unchanged (12) unless F-4 says otherwise, `unsited` 0 → measured (a raise named here, see §2.5), `gaps` 5 → measured | DoD prints the before/after counters |
| AR-22 every field read has a producer | T1r | every row's producer leg names a role file or code that writes the field | `_producer_leg` green |
| AR-28 an unknown never becomes a pass | T2 | absent row / broken file → the I-P text, never a pass, never a crash | T2 row c |
| AR-9 a refusal names a door | T2 | the door comes from the row; an absent row says "factory defect" | T2 row c |

Checks each node adds or alters (owner / census class, AR-29):

| check | node | owner it serves | census class |
|---|---|---|---|
| `_row_problems` stage line accepts `"*"` | T1r | data (code: shape of a row) | shape; not a census unit change (existing unit `stage_joints.py::_row_problems`) |
| `_demands_leg` page branch | T1r | data (join between a row and its key page) | xref; existing unit |
| `told_ratchet` and `rowless` numbers | T1r | data (counts) | ratchet; no new unit |
| `refusal()` constructor | T2 | data: it carries the row's words; it judges nothing | not a census unit (`refusal` does not match `UNIT_NAME_RE`, `test_judgment_census.py` 77); no census row |
| `spoken()` renderer | T2 | data | not a unit (same reason) |
| `_passthrough` cross-file rule, check_id records for bare refusal calls | T2 | data (siting) | xref; existing unit `refusal_registry.py::_passthrough` (no new unit) |
| `refuse(..., check=)` extra line | T2 | data | existing unit `role_cli.py::refuse` (name matches `_?refuse`); its blocking class is unchanged |

The judgment itself (is the role's output right) stays with the role and the tier above (P27). Neither node adds a code verdict on meaning.

P31 / one road: T2 gives every refusal one road (`refusal` → Record → a sink that prints `spoken`). A plain `str` passed to a sink stays legal and unchanged during the migration; that is a migration state, not a second road, and it is measured by `untold` (ceiling, shrinks per T4/T5/T7 node). No language, project or case is exempted.

---

## §2 Node T1r: rows under v2 keys

given: this file; `references/stage-joints.json`; `scripts/stage_joints.py`; `scripts/tests/test_stage_joints.py`; `scripts/tests/fixtures/told-ratchet.json`; `scripts/refusal_registry.py` (A24 entries, read only); `scripts/exit_gate.py` 676-687, 1893, 1903 (read only); revision spec §3.4 and §3.5a; parent spec §5.1 to §5.5; `wave0-rows.md`, `wave0-rows-part2.md`, `wave0-rows-part3.md` with their Lead decision blocks; `design/factory-rules.md` whole; `plans/builder-rules.md`
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\stage-joints.json
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\stage_joints.py (_row_problems, _demands_leg)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_stage_joints.py (told_real, the T1r variant rows of §2.4)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\told-ratchet.json
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\tbw-t1r-rows.md
non-goals: the 12 ahead cards, `role-rules.json` re-points, generated pages, `inject-map.json`, `role-load.json` (fork F-4: T1r-cards); any code outside the two named functions; refusal text; rows whose sentence is not drafted (F-5); conductor-producer rows (F-6); `waiver:carry.*` (T9c); census rows; relabelling any refusal site (T4/T5/T7)
handoff: the branch commit plus a report `docs/tasks/specs/reports/20261114-t1r-report.md` with the counters before/after (verbatim), the row count per group, the FR walk, and the witness
edges: §2.6
siblings: SIBLING_MAP axis 34 (one road: every row uses the same leg form, §2.3); stage twins (AR-19) n/a: no stage behaviour changes; T3a renderer (reads these rows: page legs go live when it lands)
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for scripts/stage_joints.py references/stage-joints.json scripts/tests/fixtures/told-ratchet.json` (run the non-slow files it lists), then `python -B ai-packages/qa-factory/scripts/stage_joints.py --check` (the summary line prints hand_cards, legacy_legs, unsited). `test_stage_joints.py` is slow (about 146 s): it runs per F-9 (recommended: once, as the only carrier of `rowless`); otherwise CI
designer: this file (accepted draft path, once the Lead accepts it)

Gate: T1r starts only after T3a is merged into main (C-1), unless the Lead takes F-1 (b).

### §2.1 Items

| item | what | expected behaviour | test |
|---|---|---|---|
| T1r-1 | Rename the existing rows per revision §3.4 | 5 exit families → `exit_gate:scoped|grounding|case_identity|digest|required_outputs`; `exit_gate:detector_errors`, `exit_gate:witness_errors` kept as aggregator keys; `exit_gate:text_end_after_handback` kept; 8 detector rows → 5 `<stem>:*` rows (`branch_accounting:*` takes 4; `planning_contract:*`, `critic_rollcall:*`, `s5_precheck:*`, `check_coverage:*`); 27 `window:` rows → `acceptance:<kind>`. PINS stay walked exit 8, detector 5, window 27 | audit line prints `walked exit 8, detector 5, window 27` |
| T1r-2 | `_row_problems`: the stage line accepts the single item `"*"` | `stages: ["*"]` is legal; `"*"` together with a stage id is red ("`*` stands alone"); an empty list stays red as today; an unknown id stays red | variant rows `stages-star/ok`, `stages-star/mixed-red`, `stages-empty/red` in `test_stage_joints.py` |
| T1r-3 | `_demands_leg` page branch | a producer entry whose `told` is `[{"page": true}]` and whose `demands` is `[]` is no finding: the page carries the sentence. A page entry WITH demands tokens: each token is looked up on the key page `references/slices/<role>/handoff-keys.md` (as for path entries); a missing token is red. A path entry with `demands: []` stays red (unchanged) | variant rows `demands-page/empty-ok`, `demands-page/token-missing-red`, `demands-path/empty-red` |
| T1r-4 | Write rows R1 to R11 (§2.2) | each row has `requirement` (or `requirement_from`), `door`, `when`, `roles`, `stages`, `producers` with a leg per §2.3 | `stage_joints.py --check` green; K1 / K3 / K7 green in `told_real` |
| T1r-5 | The adviser row | §2.2 R1 row 4: a code row | `told_real`: adviser not rowless |
| T1r-6 | Translate L1 to L9 | §2.3 table | `legacy_legs` 0 on `--check` |
| T1r-7 | Remove the gaps F6-51/1 and F6-51/4 (they were the legacy L2 and L8 placeholders) | `gaps` ratchet lowered to the measured count (5 → 3 expected; write what `--check` measures, never raise) | `--check` green |
| T1r-8 | Counters | `told-ratchet.json` `rowless` 55 → measured (expected 25: the C-2 list); `stage-joints.json` `told_ratchet.legacy_legs` 9 → 0, `unsited` 0 → measured (§2.5), `hand_cards` stays 12 | the counters before/after are pasted in the report |
| T1r-9 | Rewrite `told_real` K1-lit adviser row | assert `exit_gate:adviser` is NOT in `rowless`; keep the K5 real-tree row as is (it goes live by itself) | `told_real` green |
| T1r-10 | Changelog fragment | `changelog.d/tbw-t1r-rows.md`: one English ASCII bullet | `selftest.py --lang` in CI |

### §2.2 The row list (by group; source file and section per group, with counts)

Every row below is copied from its source with the Lead decisions applied. When a source row and a Lead decision differ, the decision wins. Ids are written exactly as listed; the sub-id rule (C-7) is applied.

| group | source | rows | notes |
|---|---|---|---|
| R1 exit_gate (ids with no row today) | this file, below | 4 | EG rows keyed by the A24 id (F-7 (a)) |
| R2 guard_pre_tool / stage_guard | parent §5.3 rows 1-24 (24 PT) and rows 25-39 with wave0 item 8 corrections (rows 28 split per C-7, row 30 corrected, row 31 its own row, rows 33-37 host_adapter "On Codex" sentences, `when: always` for 36/37) | 40 | PT-doctor-probe and the 20 G-dispatch SG ids are NOT here (no sentence; F-2) |
| R3 inject_context / stage_done | parent §5.3a (T9a rows) filtered by spike report M7 (road b: the 3 controller units) | up to 6 | IC-*, SD-* stay out (F-2) |
| R4 controller and phase readers | parent §5.4 (37) + wave0 item 9 (`controller:code_review_receipts`, `controller:s5_plan_gaps.rework_rows`) | 39 | |
| R5 command rows | parent §5.5 (4) + part3 (controller:rework.call/.args/.runner_half/.cap; controller:release.call; waiver:block.call/.placeholder/.stand_gap_id/.grant_pattern/.standing; waiver:remark.call; source_exclusions:revoke.call/.target) | 17 | `waiver:carry.call`, `.old_key` go to T9c (C-13); conductor-producer rows per F-6 |
| R6 S0/S1 producers and phase JSON | parent §5.2 (T7a, 40) + one `phase_json` row per qa-writer artifact named in §5.2 | 40 + N | N = the count of writer artifacts §5.2 names; the builder writes the count in the report |
| R7 handoff_check | parent §5.1 handoff block + part2 item 1 (`handoff_check:binding`, `handoff_check:investigation`) | 22 | |
| R8 planning / coverage | parent §5.1 + wave0 item 10 (sides.declared, manifest_put:provisional, expectation_changes) + part2 item 10 (sides.settled, sides.placeholders) + part2 item 3 (`coverage_contract:obligations.observation`) | 15 | S3 rows `when: always`, `stages: ["S3"]` (F-P2-7 (a)); sides.pending / sides.provisional held out (F-5) |
| R9 execution_request | parent §5.1 + part2 item 4 (active_dispatch, case_entries, profile, profile_command, stand, stand.probe, stand.reference, mine_call, scope, no_test, selector_args, window_first; corrected sandbox and place_rows) | 14 | profile.none, fingerprint held out (F-5) |
| R10 run_suite | part2 item 5 (run_suite:recover, run_suite:begin) + parent | 3 | |
| R11 first_look | parent §5.1 first_look block | 11 | `first_look:put.walked` is advice, no row (F-W6 (a)) |
| role_cli | 31 rows from `references/role-commands.json` | 0 or 31 | per F-8; recommended (a): 31 rows here |

Total: about 211 + N rows (242 + N with F-8 (a)). `null_outcome.failures` is narrowed to "every shown failure has a row" (F-P2-1 (a)). `exit_gate:digest` takes the part2 item 7 RD.check sentence.

R1 rows written in full (the A24 `refuses` of each id is the source of the sentence):

1. `exit_gate:EG-digest-form`: requirement = the part2 item 7 RD.check digest sentence; roles = the producers of `exit_gate:digest`; stages = those of `exit_gate:digest`; when `always`; door "fix the digest line the refusal names, then end the dispatch again"; producers: as `exit_gate:digest`, told `[{"page": true}]`.
2. `exit_gate:EG-s5-plan-outputs`: requirement "Before you end an S5 dispatch, every output the S5 plan names for your role is written."; roles qa-automator, qa-code-critic; stages ["S5"]; when `plan`; door "write the output the refusal names before you end the dispatch"; producers: qa-automator and qa-code-critic, field = the plan outputs, told `[{"page": true}]`, demands [].
3. `exit_gate:EG-text-end`: requirement "Your dispatch ends with the host's handback tool carrying your digest line, never with free text after it."; roles ["*"]; stages ["*"]; when `always`; door "call the host's handback tool with your digest line"; producers: every role (`roles: *`), told `[{"page": true}]`.
4. `exit_gate:adviser`: no requirement (sentence-less: the adviser never refuses, `exit_gate.py` 676-687); roles ["*"]; stages ["*"]; when `always`; producers `[{"code": "exit_gate.py::run_advisers", "field": "advice", "told": [{"path": "scripts/exit_gate.py", "anchor": "def run_advisers"}], "demands": []}]`. A code producer's leg is not a legacy leg (no role).

The v1 literal rows (`exit_gate:digest`, `exit_gate:required_outputs`, `exit_gate:text_end_after_handback`) stay as they are and stay sentence-less where §3.4 says so. Rows 1 to 3 carry the sentence (F-7).

### §2.3 L1 to L9 translation (by revision §3.4, uniform rule)

Rule (F-3 (b), recommended): a row that states a requirement gets `told: [{"page": true}]`. A sentence-less row (aggregator) gets `told: [{"path": "references/slices/<role>/handoff-keys.md", "anchor": "<the anchor its sibling entries use>"}]`. No leg points at `agents/*.md` or `artifact-contract-*.md`.

| leg | row (v1 → §3.4 key) | stage-joints.json line (today) | today's leg | new leg |
|---|---|---|---|---|
| L1 | scoped → `exit_gate:scoped` | 58 | `artifact-contract-run` | `{"page": true}` |
| L2 | scoped → `exit_gate:scoped` (gap F6-51/1) | 75 | agents file | `{"page": true}`; gap removed |
| L3 | witness_errors → `exit_gate:witness_errors` (aggregator) | 172 | `artifact-contract-automation` anchor `automation-manifest.json` | key page of qa-code-critic, anchor `## Witness` |
| L4 | digest → `exit_gate:digest` | 262 | agents file | `{"page": true}` |
| L5 | digest → `exit_gate:digest` | 266 | common-rules | dropped (F-W7 (a), accepted) |
| L6 | required_outputs → `exit_gate:required_outputs` | 336 | agents/contract | `{"page": true}` |
| L7 | branch_accounting (plan contract) → `branch_accounting:*` | 431 | plan contract file | `{"page": true}` |
| L8 | branch_accounting (gap F6-51/4) → `branch_accounting:*` | 445 | agents file | `{"page": true}`; gap removed |
| L9 | critic_rollcall → `critic_rollcall:*` | 513 | agents file | `{"page": true}` |

Note: revision §4 assigns L7 and L9 to `branch_accounting:*` and L8 to `critic_rollcall:*`. The file lines (431, 445 under branch_accounting; 513 under critic_rollcall) say L7 and L8 are branch_accounting and L9 is critic_rollcall. The table above follows the file; the builder reads the row each line belongs to before editing and reports any difference. If a row in this table is sentence-less after §3.4, its leg takes the key-page path form instead of `page: true`.

`exit_gate:digest` and `exit_gate:required_outputs` get `page: true` only if they carry a sentence after the rename (part2 item 7 completes `digest`). If `required_outputs` stays sentence-less, L6 takes the key-page path form (anchor of its sibling entry).

### §2.4 Test rows T1r adds (variant rows in the existing file, no new file)

`stages-star/ok`, `stages-star/mixed-red`, `stages-empty/red`, `demands-page/empty-ok`, `demands-page/token-missing-red`, `demands-path/empty-red`, and the rewritten K1-lit adviser row. They go into the existing parameter tables of `test_stage_joints.py` (keep row of `test-layers.json`).

### §2.5 Counters before and after, and the commands

| counter | carrier | before | after | command |
|---|---|---|---|---|
| rowless (dense) | `scripts/tests/fixtures/told-ratchet.json` | 55 | 25 expected (the C-2 list), the measured value is written | `python -B ai-packages/qa-factory/scripts/tests/test_stage_joints.py` (the told line prints rowless and its list; slow) |
| untold (ceiling) | same fixture | 253 | 253 (T1r relabels no site) | same |
| legacy_legs (ceiling) | `stage-joints.json` `told_ratchet` | 9 | 0 | `python -B ai-packages/qa-factory/scripts/stage_joints.py --check` |
| hand_cards (dense) | same | 12 | 12 (F-4 (a)) | same |
| unsited (ceiling) | same | 0 | measured: the count of rows whose id is not sited | same (audit prints it; each unsited row is named) |
| gaps | `stage-joints.json` 1116 | 5 | measured (expected 3) | same |

`unsited` is a named raise (AR-20): rows written ahead of their refusal site (the role_cli rows before T2 sites `role_cli:<key>`, and any §5.4 row whose site is relabelled later) are unsited by design until the relabelling node lands. Every unsited row is listed in the T1r report with the node that sites it. A row unsited with no named siting node is a defect: the builder stops and asks.

### §2.6 Edges

- TEMPORAL, page legs: before T3a, `_page_leg` is red for every page told. Before T3a merges, T1r does not land (gate). After T3a, the same rows are green with no edit. Invariant: a row is never green on a leg that nothing renders.
- TEMPORAL, unsited: before T1r, unsited = 0. After it, unsited = the measured count. The ceiling written equals the measured count, never more. Invariant: a row ahead of its site is counted and named, never silently sited.
- TEMPORAL, rowless: dense. After T1r every later node that rows an id lowers it in its own commit. Invariant: an id with no row is always counted.
- POSITIONAL, `_demands_leg` page branch: it comes before the "demands leg missing" verdict and applies only when every `told` item is `{"page": true}`. Invariant: a path entry with no demands stays red, and a page entry's tokens are still checked.
- POSITIONAL, the `"*"` stage branch: it comes before the stage-id lookup. Invariant: an unknown stage id or a mixed `["*","S3"]` is still refused.
- Empty or absent: a row with `requirement_from` naming a missing file is red (as today). A producer with `roles: ["*"]` names every mapped role for K5.
- Conflict, R1 vs §3.4: the v1 literal rows stay sentence-less, the A24-id rows carry the sentence (F-7). Both exist, and `row_for` picks the exact id first, so there is no "two rows" case.
- Conflict, C-2 vs revision §4: rowless is written as measured, not forced to 0. Forcing it to 0 would need rows with no sentence, which K3 refuses.
- Error direction of the reused `_is_sited`: it may err toward "unsited" (a correct row counted unsited is visible and named) and never toward "sited". Adversarial inputs that must stay unsited: an id that only shares a prefix without a dot (`SG-commandx`), a sub-id of an unsited parent, an id in a comment.

---

## §3 Node T2: the refusal constructor and its sinks

given: this file; parent spec §2.4 (design, I-P, I-R); `scripts/detector_verdict.py`; `scripts/stage_joints.py` (`row_for`, `told_text`, `fill`, `sited_ids`); `scripts/hooklib.py` 984-992; `scripts/stage_guard.py` 766-769 and its `LAST_DENIAL` / `BLOCK_MATCHES` readers; `scripts/role_cli.py` 52-172; `scripts/refusal_registry.py` 79-84, 1321-1490; `references/role-commands.json`; `scripts/tests/test_detector_verdict.py`; `scripts/tests/test_role_commands.py`; `scripts/tests/test_refusal_registry.py`; `design/factory-rules.md` whole; `plans/builder-rules.md`
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\detector_verdict.py (Record, refusal, spoken)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\hooklib.py (block)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\stage_guard.py (deny)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\role_cli.py (refuse, run_guarded, RefusingParser.error)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\refusal_registry.py (CHECK_PASSTHROUGH, _passthrough, _scan_wide, RECORD_SINKS)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\stage_joints.py (sited_ids)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_detector_verdict.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_role_commands.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_refusal_registry.py (the pass-through variant rows)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\tbw-t2-refusal.md
non-goals: relabelling any refusal site to call `refusal()` (T4/T5/T7); rows (T1r); the census and `told-ratchet.json` (if K4 or C1 goes red on T2's tree: STOP and report); the text of any existing refusal; REPAIR_MARKER / PERSON_MARKER
handoff: the branch commit plus `docs/tasks/specs/reports/20261114-t2-report.md` with the FR walk, the byte-identity witness for block(str) / deny(str), and the witness
edges: §3.4
siblings: axis 34 (one road: block / deny / refuse all print `spoken`); AR-18 one shape; `role_cli` and `hooklib` sinks change together
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for scripts/detector_verdict.py scripts/hooklib.py scripts/stage_guard.py scripts/role_cli.py scripts/refusal_registry.py` (run the non-slow files it lists, including `test_detector_verdict`, `test_role_commands`, `test_refusal_registry`), then `python -B ai-packages/qa-factory/scripts/refusal_registry.py --check` (exit 0, no violations); `test_stage_joints.py` and `test_judgment_census.py` run in CI
designer: this file (accepted draft path, once the Lead accepts it)

### §3.1 Items

| item | what | expected behaviour | test |
|---|---|---|---|
| T2-1 | `Record` gains `expected` and `door` (str, default "") | old constructors unchanged; `str(record)` is the problem only | test_detector_verdict row a |
| T2-2 | `refusal(check, problem, *, fill=None) -> Record` | never raises; builds `with_check(Record(problem), check)`; `expected` = `told_text(row)` with `fill` applied; `door` = `fill(row["door"])` | row b |
| T2-3 | Lookup through `row_for(check)` only (exact v2 id, else `<stem>:*`) | AR-13; never `rows_for` (C-10) | row "reads only via row_for" (monkeypatched reader seen) |
| T2-4 | `spoken(record)` | problem + `\n  expected: <expected>` (if non-empty) + `\n  door: <door>` (if non-empty) + `\n  check: <id>`; a plain `str` is returned unchanged | row d |
| T2-5 | `hooklib.block(message)` | prints `spoken(message).rstrip() + "\n" + TRAPPED` to stderr; TRAPPED stays the last line; `block(str)` byte-identical to today | row e (byte compare of stderr for a str) |
| T2-6 | `stage_guard.deny(message)` | prints `"STAGE GUARD: " + spoken(message)`; `LAST_DENIAL["message"] = str(message)` (the problem only, so `BLOCK_MATCHES` / `block_match` still match); `deny(str)` byte-identical | row f |
| T2-7 | `role_cli.refuse(command, problem, stream=None, *, check=None)`; `run_guarded` passes a Record whole; `RefusingParser.error` passes `check=f"role_cli:{command}"` | str problem: today's lines unchanged, then one last line `  check: role_cli:<command>`; no lookup. Record: today's lines with `str(record)`, plus `expected` / `door` lines from the Record, then `  check: <record.check>`. If the Record's check is the command's own `role_cli:<command>` row, the expected / door lines are skipped (the command's own lines already say it) | test_role_commands rows g, h |
| T2-8 | Scanner: every bound literal `refusal(...)` / `with_check(...)` call is sited | `_scan_wide` emits a `check_id` record (state `walk_error`, out of units and totals, as the pass-through records) for each such call, inside a transport or not (C-8) | test_refusal_registry row `assigned-first-refusal/sited` |
| T2-9 | The cross-file call-site rule (§3.2) and the `CHECK_PASSTHROUGH` line | §3.2 | rows `refusal-crossfile/ok`, `refusal-nonliteral/walk-error`, `refusal-zero-sites/no-error` |
| T2-10 | `sited_ids` takes the `role_cli:<key>` ids | `sited_ids` ∪ {`role_cli:` + key for each key of `references/role-commands.json`}; a missing / broken role-commands file adds nothing and the audit names it (no crash) | row in test_stage_joints (CI) or in test_refusal_registry, whichever holds the sited-id table; builder picks the existing table |
| T2-11 | `RECORD_SINKS` content | unchanged tuple ("block","deny","refuse","run_guarded"): all four now accept a Record | row i |
| T2-12 | Changelog fragment | one English ASCII bullet | CI `--lang` |

### §3.2 The cross-file call-site rule for `refusal` (written out)

1. `CHECK_PASSTHROUGH` gets one line: `("detector_verdict.py", "refusal"): 0` (argument index 0 is the check id).
2. `_passthrough` treats a listed def whose name is a key of `RECORD_CALLS` as a constructor. Its call sites are every call, in every scanned file, that `_record_kind` binds to detector_verdict in that file (import alias, `from detector_verdict import refusal`, or a call inside detector_verdict itself), not the bare-name calls of the def's own file.
3. At each such call site, the argument at the listed index is read by `_record_id`: a string literal or a module-level str constant counts (as today). Any other expression is a `check_arg` walk error naming the file, the line and "the check of refusal() must be a literal".
4. For a constructor line, zero call sites is NOT a walk error (no site has been relabelled yet). For every other listed def, the existing rule stays: zero literal call sites is a walk error.
5. A call in a file where `refusal` is not bound to detector_verdict (a local function of the same name) is not a call site. Invariant: a same-name function elsewhere never sites an id.
6. `exit_gate.own` keeps its line and its same-file rule unchanged.

Error direction: the rule may err toward "not sited" (a call reached through an unusual alias is missed, and its row shows as unsited, visible). It must never err toward "sited". Adversarial inputs that must stay unsited: `refusal(name_var, ...)` (non-literal: walk error), a local `def refusal` in another file, `refusal` called in a comment or a string, `getattr(dv, "refusal")("x:y", ...)`.

### §3.3 Behaviour table for the four cases the brief names

| case | `refusal()` result | what a sink prints |
|---|---|---|
| absent row (the file is readable, no exact row, no `<stem>:*` row) | Record(problem), check set, `expected` = "(the factory's requirement row <id> could not be read: <why from row_for>; this is a factory defect)", door "" | problem, the expected line, the check line; no door line |
| broken rows file (absent or unparsable `stage-joints.json`) | same as absent, with `row_for`'s why (file unreadable) | same; never a crash, never a pass (I-P) |
| two rows | `row_for` returns the first plus a why; `refusal` uses the first row and appends nothing to the person's text; the why is not shown to the role (the audit catches duplicates, E7) | the first row's expected / door |
| Record vs str | a sink given a Record prints `spoken(record)`; a sink given a str prints exactly today's bytes (block, deny) or today's lines plus the check line (refuse, T2-7) | as left |

A row that exists but is sentence-less (an aggregator key): `expected` = "" and the expected line is omitted; door from the row if present. This is not the absent case. I-R: `match_known` equality holds; no REPAIR_MARKER / PERSON_MARKER is added by `refusal` or `spoken`.

Tests inject the rows (the reader is monkeypatched, or a data argument is passed in a test seam). No test reads the real `stage-joints.json` for these cases.

### §3.4 Edges

- TEMPORAL, rows: before T1r, most v2 ids have no row, so a `refusal()` called today shows the absent-row text. No site calls `refusal()` until T4/T5/T7, so no role sees it in this wave. After T1r, the same call shows the row. Invariant: a missing row is never a pass or a crash.
- TEMPORAL, siting: before T2, `role_cli:<key>` rows (if F-8 (a) lands first in T1r) count as unsited. T2's `sited_ids` change lowers `unsited`. T2 does not own the counter, so it reports the new measured `unsited` and T1r's ceiling stays valid (ceilings only shrink: a lower value passes).
- POSITIONAL, `deny`: `LAST_DENIAL` is set from `str(message)` before printing. Invariant: `block_match` reads the problem only, never the expected / door text.
- POSITIONAL, `block`: TRAPPED is printed after `spoken`. Invariant: TRAPPED stays the last line.
- POSITIONAL, `refuse`: the check line is the last line, after "if you cannot". Invariant: today's lines keep their order and bytes.
- Limit: `spoken` does not truncate. A row's sentence is bounded by the rows audit, not by `spoken`.
- Empty: `fill=None` leaves placeholders as written. A placeholder with no value in `fill` stays literal (no KeyError).

---

## §4 Can T1r and T2 run in parallel

| file | T1r | T2 | overlap |
|---|---|---|---|
| `references/stage-joints.json` | owns | reads only (tests inject rows) | none |
| `scripts/stage_joints.py` | `_row_problems`, `_demands_leg` | `sited_ids` | different functions (D-0048 function lists) |
| `scripts/tests/test_stage_joints.py` | `told_real`, its variant rows | at most one sited-id row (T2-10) | different rows; the later branch merges main and keeps both |
| `scripts/tests/fixtures/told-ratchet.json` | owns | not touched | none |
| detector_verdict / hooklib / stage_guard / role_cli / refusal_registry and their tests | not touched | owns | none |
| `changelog.d/` | own fragment | own fragment | none |

Verdict: parallel by function lists. Two constraints: T1r waits for T3a merged (C-1, F-1). `stage_joints.py` is not a hot file of PROJECT.md «Командная работа» п. 3, but the two dispatches still carry their function lists. Whichever merges second merges main into its tree first.

---

## §5 What T1r and T2 change for later nodes (one line each)

- T3a: unchanged; its renderer makes T1r's page legs green. It must land before T1r.
- T4: relabels PT / SG sites to `refusal("<id>", ...)`; each relabel lowers `untold` and needs its row already present (T1r R2). G-dispatch SG ids need sentences first (F-2).
- T5: §5.4 sites; rows from T1r R4.
- T7a / T7f: §5.2 rows from T1r R6; SD ids get rows in T7f (F-W2).
- T9a: IC rows; `collect_blocks` (IC-oversized-slice) has no owner (F-2).
- T9c: `waiver:carry.*` rows and the `move:words_carry` moves row; conductor rows per F-6.
- T1r-cards (F-4): ahead cards → rows, role-rules re-points, hand_cards 12 → 0, role-load.

---

## §8 Forks (returned, not decided)

- F-1 T1r gate on T3a. (a) T3a goes first, T1r after it merges (the parent's order). (b) T1r lands now with `_page_leg` relaxed. Recommend (a): no row ever goes green on a leg nothing renders; T3a has no dependency left.
- F-2 rowless after T1r. (a) Write 25 as measured; every node that rows an id lowers it (dense). (b) Draft sentences now for PT-doctor-probe, IC×2, SD×2 and the 20 G-dispatch ids and land them in T1r. (c) Keep revision §4's "0" (impossible without sentence-less rows, which K3 refuses). Recommend (a), plus a named owner per remaining id: T4 (PT-doctor-probe, 20 G-dispatch), T7f (SD×2), T9a (IC-native-packet-unwritten). IC-oversized-slice (`collect_blocks`) needs an owner node: the Lead names one. Cost of (b): about 25 sentences from the A24 `refuses`, one designer pass.
- F-3 Leg form for L1-L9. (a) F-W7 (a) as accepted: legs on agents / artifact files (legacy_legs stays 9, E16 never closes). (b) Uniform: page leg for a row with a sentence, key-page path for a sentence-less row. Recommend (b): one road (P31), closes E16. It reverses an accepted decision, so the Lead takes it back.
- F-4 The 12 ahead cards. (a) Split: T1r without cards; a new node T1r-cards after a designer mapping (cards → rows, pages, role-rules re-points, hand_cards 12 → 0, role-load). (b) T1r maps them itself. Recommend (a): no draft maps them, and a builder would have to invent the mapping (PROJECT.md «Командная работа» п. 11).
- F-5 Rows with no sentence (`sides.provisional`, `sides.pending`, `profile.none`, `fingerprint`, `stage_done:set`, `planning_contract:plan.unmarked_revision`). (a) Held out of T1r; the Lead (or a designer pass) writes the sentences into a later node. (b) Land them sentence-less. Recommend (a): a sentence-less row with a producer is red under K3, and inventing a sentence is the builder's guess.
- F-6 Conductor-producer rows. (a) T9c lands them with its conductor work. (b) `_producer_leg` accepts "conductor" with a code-side leg (a T1r change to one more function). Recommend (a): no conductor role file exists; one owner for the conductor's surface.
- F-7 EG ids: two namespaces. (a) Rows keyed by the A24 id carry the sentence and page leg; the v1 literal rows stay sentence-less. (b) Merge: the v1 row takes the sentence and the A24 id becomes a sub-id. Recommend (a): no key redesign (non-goal), K1 is satisfied by exact ids.
- F-8 role_cli rows (31). (a) T1r lands them with `requirement_from` = `references/role-commands.json`, one uniform door, roles from data; T2 sites them (`sited_ids`). (b) A later node. Recommend (a): the data already exists, and the unsited raise is named and closed by T2 in the same wave.
- F-9 Running `test_stage_joints.py` (about 146 s) in T1r's witness. (a) Once, as the only carrier of `rowless` (precedent: T1c and the topic fix ran it). (b) CI only. Recommend (a) for T1r (the counter it writes needs the measurement); (b) for T2.

### Lead decisions on the forks (14.11.2026, acceptance of draft t-677)

- F-1 = (a): T3a goes first; T1r after T3a merges. T2 runs now, in parallel with T3a.
- F-2 = (a): `rowless` after T1r is the measured 25; owners per remaining id as recommended (T4, T7f, T9a). `IC-oversized-slice`
  (`collect_blocks`) is owned by T9a together with the other IC rows.
- F-3 = (b): one road for L1-L9 (a page leg for a row with a sentence, the key-page path for a sentence-less row). The Lead takes back
  its earlier acceptance of F-W7 (a) (P31; closes E16).
- F-4 = (a): T1r without the ahead cards; a new node T1r-cards after a designer mapping.
- F-5 = (a): the six sentence-less rows are held out of T1r; their sentences are written in a designer pass with T1r-cards.
- F-6 = (a): conductor-producer rows land with T9c.
- F-7 = (a), F-8 = (a), F-9 = (a for T1r, b for T2).
- The draft is ACCEPTED as the dispatch carrier for T2 (§3) and T1r (§2). No second plan-critic pass: no key or architecture redesign.

## §9 Small choices closed by the designer

- S-1 Report file names `20261114-t1r-report.md`, `20261114-t2-report.md`; changelog fragments `tbw-t1r-rows.md`, `tbw-t2-refusal.md`.
- S-2 `"*"` stands alone in `stages`; mixing it with a stage id is red.
- S-3 Sub-id form `stage_guard:SG-command.commit.pathspec` / `.manifest`; row 31 is its own row `stage_guard:SG-walker-error` (K1 needs it).
- S-4 `waiver:carry.*` moves to T9c with its moves row.
- S-5 The adviser row is a code producer row with no requirement (it never refuses).
- S-6 `spoken` omits empty expected / door lines instead of printing them blank.
- S-7 T2's check line in `refuse` goes last, so today's lines keep their order.

## §10 Reading trail (read-main unless noted)

- `docs/tasks/specs/20261113-told-before-work-t1-revision-spec.md` §3.4, §3.5a, §4 461-467, §9.
- `docs/tasks/specs/20261113-told-before-work-mechanism-spec.md` §2.2-§2.4, §5.1-§5.6, T0 gate note.
- `wave0-rows.md` items 7-11 and Lead decisions; `wave0-rows-part2.md` items 1, 3, 4, 5, 7, 10 and F-P2-*; `wave0-rows-part3.md` and O-1.
- Reports: `docs/tasks/specs/reports/20261113-t1c-report.md`, `20261113-tbw-t1-topic-fix-report.md`, `20261113-t1b-report.md`; spike `.claude/worktrees/tbw-t0/docs/tasks/specs/reports/20261113-told-before-work-spike.md` M7.
- `ai-packages/qa-factory/scripts/stage_joints.py` 44-94, 105-163, 276-323, 419-582, 676-706, 761-784, 898-932, 955, 991-1130.
- `scripts/tests/test_stage_joints.py` 680-698, 808-847; `scripts/tests/fixtures/told-ratchet.json`.
- `scripts/refusal_registry.py` 79-84, 330, 781, 813, 894, 928, 1041, 1048, 1321-1490, 1692.
- `scripts/detector_verdict.py` 59, 94-138; `scripts/hooklib.py` 984-992; `scripts/stage_guard.py` 766-769; `scripts/role_cli.py` 52-172; `scripts/exit_gate.py` 676-687, 1893, 1903.
- `references/stage-joints.json` 58, 75, 172, 262, 266, 336, 431, 445, 513, 1116, 1142-1144; `references/ahead-cards.json`.
- `scripts/tests/test_judgment_census.py` 77; Glob `agents/*.md` (12 files, no conductor.md).
- Negative claims and their controls: "no `refusal`/`spoken` in detector_verdict" (control: `def with_check` found in the same file by the same search); "no `requirement_section`" (control: other defs of contract_slices.py found); "no conductor.md" (control: the 12 qa- files found by the same Glob). Globs at the worktree root returned nothing (a miscall); no claim rests on them.

Needed beyond the manifest: `scripts/exit_gate.py`, `scripts/tests/test_stage_joints.py`, `scripts/tests/test_judgment_census.py`, `references/ahead-cards.json`, `agents/`, the t1b / t1c / topic-fix reports, the T0 spike report.
