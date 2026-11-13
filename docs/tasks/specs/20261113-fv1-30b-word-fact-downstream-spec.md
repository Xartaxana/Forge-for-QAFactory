# FV1-30b — a fact the person's word passed is visible downstream (DRAFT, designer, t-542; fix round after critic-on-plan; S1 answered)

Status: DRAFT for Lead acceptance, fix round 1 after `docs/tasks/specs/reviews/20261113-fv1-30b-plan-critic.md` (fit_with_fixes,
B1-B4, M1-M5), **then round 2: the S1 scout's answers written in (§12)**. Lead decisions binding in this round: **F4 = (a)**,
**F8 = (a)**. Forks still open are returned (§8), not decided. Small choices closed by the designer: §9. Reading trail: §10. What
changed in round 1, per finding: §11 "Fix round"; what changed in round 2, per S1 fact and fork: §12 "S1 answered".

Paths: `S\` = `C:\QAFactory\forge-repo\.claude\worktrees\fv130a\ai-packages\qa-factory\scripts\` (branch `wip/fv130a`, FV1-30a);
`N3\` = the same under `C:\QAFactory\forge-repo\.claude\worktrees\fv119-n3\`; **`M\` = the same under
`C:\QAFactory\forge-repo\.claude\worktrees\read-main\` (origin/main) — every fact first relied on in the fix round is cited from `M\`**;
**`W\` = the same under `C:\QAFactory\forge-repo\.claude\worktrees\fv19-30-base\` (commit 4d0ad66: FV1-19 N3 AND FV1-30a merged) —
every fact first relied on in round 2, and every line number in N1/N2 `owns:`, is cited from `W\`**;
`A\` = `C:\QAFactory\forge-repo\docs\tasks\specs\20261113-p1-specs-amendment-owner-words.md`; `F19\` =
`C:\QAFactory\forge-repo\docs\tasks\specs\20261113-fv1-19-obligation-refs-spec.md`; `R30a\` =
`C:\QAFactory\forge-repo\docs\tasks\specs\reviews\20261113-fv130a-code-critic.md`; `CR\` =
`C:\QAFactory\forge-repo\docs\tasks\specs\reviews\20261113-fv1-30b-plan-critic.md`. Package paths in node `owns:` are absolute on the
batch branch (`C:\QAFactory\forge-repo\ai-packages\qa-factory\...`).

**Base note (fix round).** `M\` carries FV1-19 N3 (`M\controller.py:7247` `_s5_v2_collect`, fingerprint line `:7311-7314`) but NOT
FV1-30a: `_s5_no_row_passed`, `word_passes`, `NOT_PASSABLE_TAGS` have no hit in `M\controller.py` (Grep; positive control in the same
call shape: `def _s5_v2_collect` hits `:7247`). So 30a-owned lines are cited from `S\` (`S\controller.py:7353-7366` `_s5_no_row_passed`,
`:7447-7451` the `product:` let-go); every N1 line number is "as on `M\`, shifted by 30a's merge" — the builder locates by FUNCTION
name and the quoted text, never by number.
**Base note (round 2).** `W\` carries both: `W\controller.py` `_s5_completion_problems` `:7025` (shape at `:7079`, door `:7080-7110`),
`_s5_collect` `:7224`, `_s5_v2_collect` `:7275` (loop `:7321-7352`), `_s5_no_row_passed` `:7354-7367`, `_s5_gap_problems` `:7369`
(30a let-go `:7444-7450`, `other_gaps` refusal `:7451-7452`, `passed_green` `:7453-7454`). Line numbers are still a help, never the
locator: the builder finds the FUNCTION and the quoted text.

## §0. What the reading changed against the brief (read before §1)

- **D1. FV1-30a carries only items 1-4 of `A\:330-373`.** (`R30a\:5`.) Item 5 (`person_passes`, `_word_passed_gap`, facts key
  `word_passed`) and item 6 (`awaits_answer`) have no hit under `S\*.py` (Grep -i, controls `word_passed_pairs`, `NOT_PASSABLE_TAGS`;
  confirmed by `CR\:13`). Item 5 is node N3; items 6 (2-3) and 7 are fork F1.
- **D2. A word-passed `row-fields-missing` dies at tier 2 of the finish.** `window_record.build` deletes empty fields
  (`W\window_record.py:1354-1361`); `WINDOW_INSTANCE_FIELDS` requires them (`W\contract.py:5511-5514`); `window_shape_errors` reports
  `"<label>: <f> is missing"` (`W\contract.py:5715-5720`); the shape step stops (`W\controller.py:7079-7110`). (`CR\:14`; S1 confirmed:
  tier 2 refuses BEFORE tier 4 is reached.)
- **D2b (fix round). Tier 4 refuses the same instance again (B2).** For a schema-2 item `validate_window` emits
  `obligation_binding:<iid>` when `obligation_ids` is empty or absent and `obligation_hash:<iid>` when `obligation_hash` is empty
  (`W\acceptance.py:1181-1190`), `assertion_identity:` / `defect_location:` for those empty fields (`:1191-1194`),
  `change_disposition:` / `change_basis:` (`:1195-1198`). All of them are `other_gaps` and refuse as `"unresolved window: ..."` unless
  the completion carries `unresolved` AND `reason` (`W\controller.py:7451-7452`). So: a completion WITH the pair already passes these
  gaps today (the word adds nothing there); a completion WITHOUT it is refused — that is what N1's tier-4 let-go removes.
- **D2c (fix round). Two fields whose EMPTY value switches another check off (CR §3, F2 scout item 2) — measured.**
  (i) `change_disposition`: the probe-missing line needs `== "new_or_changed"` (`W\contract.py:5727-5731`), and
  `proof_level._wanted` reads the row's own flags, `change_disposition == "new_or_changed"` among them, and for a row with no `novelty`
  key nothing else (`W\proof_level.py:452-457`; called through `proof_required(item, {})` from `W\acceptance.py:1153`, `:1207`): an empty
  value drops the probe demand AND the `sensitivity:` gap. (ii) `input_hash`: an empty value makes the item `malformed_instance:<iid>`
  and `continue`s past EVERY later check of that instance (`W\acceptance.py:1115-1117`). Both are excluded from any pass by a data row
  (§2.2 item 4, `row_fields`). (Round 2: S1 confirmed both; rows kept.)
- **D3. A word-passed `no-row-<iid>` dies at tier 2 AND tier 3 (B1).** `window_record._terminal_runs` keys by exact id
  (`window_record.py:471-473`); a no-row instance gets no `outcome` and no `execution_fingerprint` and `evidence_refs: []`
  (`W\window_record.py:1410-1413`). Tier 2 lists `<iid>: outcome is missing`, `<iid>: execution_fingerprint is missing`
  (`W\contract.py:5715-5720`) AND, for a `new_or_changed` item with no outcome and no `probe`, `<iid>: probe is missing for a
  new_or_changed instance` (`W\contract.py:5727-5731`, `PROBE_MISSING_ERROR` `:5525`). Tier 3 then refuses `"coverage v2 instance
  requires execution_fingerprint"` (`W\controller.py:7341-7344`). Tier 4 (round 2, S1 Q3, re-read): `product:<iid>` (`W\acceptance.py:1140-1141`,
  30a lets it go `W\controller.py:7448-7450`); `evidence:<iid>` (`:1251-1252`: `evidence_refs == []`, not handed/stopped); for a
  `new_or_changed` item also `sensitivity:` (`:1207-1218`), `semantic_sensitivity:` (`:1219-1234`), `probe_mutation_kind:` (`:1239-1243`
  with `W\proof_level.py:295-308`: an empty probe reads level `product` with no mutation kind), `probe_evidence:` (`:1244-1245`); and
  whatever review gap its review carries (`:1171-1174`). `stale_run:` is not raised (no `run_identity`: it is written only in the run
  branch, `W\window_record.py:1396-1398`). Which of these a `not_run` word lets go: fork F13 (§8). The precheck/window alias split
  (`s5_precheck.py:1948-1950` vs exact id) is residual node N5 (§6).
- **D4. Two different plans.** (Unchanged; `CR\:16`.) The precheck's `plan-unreadable` is `work/s5-plan.json`; the controller's
  unreadable-plan refusal reads `work/test-plan.json`. `A\:404` vs `A\:887` contradict. Fork F5 (Lead: (b), confirmed by `CR\:83`).
- **D5. `acceptance.blocked_instances` is not a reader of "no run row"** (`acceptance.py:429-433`). (`CR\:17`.)
- **D6. The test-plan read at the finish** (`W\controller.py:7317`) ends tier 3 on an unreadable plan, whatever word stands.
- **D7. The coverage projection joins obligations to instances through `manifest.obligation_bindings`**
  (`W\coverage_contract.py:568-583`), never window refs. (Round 2: S1 Q5 NOT measured on real data; R5 rewritten so that no rule rests on
  it — D13.)
- **D8 (fix round). `check_traceability.walk` is case-level (B3).** It runs `_case_chain` per case (`M\check_traceability.py:211-218`),
  takes the requirement's outcome only when every case reached one (`:219-224`), and `traceability_records` skips a row with an
  outcome (`M\check_delivery.py:1199-1200`). A case with one green Then and one unbound Then reaches a terminal outcome: the unbound
  Then never reaches the verdict. `walk` already loads the manifest (`:171`) and the case index (`:173`); the manifest carries
  `then_bindings` rows `{case, then, ...}` (readers e.g. `M\ledger.py:224`); `traceability.case_thens(path)` (`M\traceability.py:140`)
  gives a case's Thens. The after_checks branch of `traceability_records` attaches `to_check` only for `question_open`
  (`M\check_delivery.py:1223-1230`).
- **D9 (fix round). The coverage verdict is built from strings, not kinds.** `coverage_reasons` (`M\check_delivery.py:1681-1712`)
  exempts only `verified` and `person_debt`, reads no kinds file; `ledger.person_debts` (`M\ledger.py:1801`) lists ledger rows, not
  obligations. So a refs pass switched to `after_checks` later is not one data row (fork F10).
- **D10 (round 2). The probe block copies the item's fields after the deletion loop.** `window_record` builds the window `probe` from
  the item: a prepared `window_probe` gets `obligation_ids`, `obligation_hash`, `defect_location`, `assertion_id` by `setdefault`
  (`W\window_record.py:822-836`), the receipt path copies them outright (`:853-856`); both run after the deletion loop (`:1354-1361`;
  the probe is attached from `:1414` on). `probe_by_code` prepares those keys as `entry.get(...) or None` (`W\probe_by_code.py:2855-2856`).
  So a field N1 keeps as `""` meets `None` in a prepared block and `semantic_sensitivity:` is raised (`W\acceptance.py:1226-1234`); in
  the receipt path the copy equals the item and it is not. Either way the gap kind also covers independent probe defects
  (`receipt_off_target`, `defect_location == expected_location`, mismatched ids/hash) — fork F12.
- **D11 (round 2). Four other readers judge the same window, and none knows the word.** (i) `story_step.finish` derives the
  `unresolved` pair ONLY when EVERY gap is one of `DERIVED_GAP_KINDS` = blocked_by_env, handed_to_person, probe_gap,
  contradicts_requirement (`W\story_step.py:1619`, `:1668-1689`, applied `:2548-2555`); a caller's typed `--unresolved/--reason` is
  kept (`:2556-2571`). (ii) The controller reads the pair as present or not (`W\controller.py:7451`): a typed pair passes EVERY
  `other_gaps` entry (E27 confirmed). (iii) `window_record.run` prints "this window is NOT acceptable yet ... repair the artifact" and
  exits 1 for any gap outside its own `derivable` set (`W\window_record.py:2031-2035`, `:2075-2083`; its `verdict` lists every shape line
  and `validate_window` gap, `:1680-1700`). (iv) `driver_dispatch.Driver.window_gap` derives a pair only when every gap is a handed
  instance or a critic kind `could_not_judge`/`fitted_to_code` (`W\driver_dispatch.py:916-949`) — **the scout's "the same four" is
  corrected: this set is different**. So a window whose only remaining gaps the word let go is accepted by the controller but printed
  "NOT acceptable" by `window_record.run`; and a window that mixes a word-passed gap with a derivable one gets no derived pair while the
  controller's door says "`story_step.py finish` derives that pair" (`W\controller.py:7421`, `:7431`) — a door that cannot be used
  (FR-2). The same holds TODAY for 30a's `product:` let-go. Fork F14.
- **D12 (round 2). `obligation_ref_problems([])` is `[]`** (`W\contract.py:5296-5307`, "`[]` for an empty list (whether refs are DEMANDED
  is the caller's rule)"). R5's first draft read "refs still fail `obligation_ref_problems`" — for absent or empty refs that reads
  "repaired". Corrected in R5.
- **D13 (round 2). R5 needs no measured premise.** (i) A binding is its own array, merged by `obligation_id` with no reference to row
  refs (`W\manifest_put.py:1935-1944`). (ii) `witnessed_binding` runs `validate_window` on the binding's instances and returns False on
  any gap (`W\coverage_contract.py:252-258`); the accepted window carries `obligation_binding:`/`obligation_hash:` for a refs-passed
  instance (D2b), so such a binding is NEVER witnessed and the obligation is NEVER `verified` (`:597`, `:627-629`) — today, without N2.
  (iii) A plan obligation with no binding naming a covering instance is its own S5 finding `obligations:<case>:obligation-id-<oid>`
  (`W\s5_precheck.py:3854-3888`), which a refs word does not pass (its (check, tag) is no `facts` row: fact `other`). So N2's branch keys
  on the binding and only ADDS words; the no-binding obligation reads as today. Fork F16 records that choice.

## §1. Scope, invariants touched, owners of every check

**Goal.** Every LOWER reader of a fact a person's recorded word passed at the S5 exit shows that fact as a named gap "passed by the
person's word (<by>, <when>)": never as proven, never as a second question (FR-7), and the stage does not stop on it (P13, P21,
P22). The word passes the STEP, never the FACT (`A\:413`, A3-E1).

**In.** The lower readers of four facts (Then not bound; instance with no run row; row fields not established — refs first, F8 (a),
`F19\:588`, and the other fields per §2.2 item 4; S5 plan not read), the report's line for each pass (item 5 of `A\:374-382`), the
delivery verdict for each fact (F4 (a): the fact's own kind, `no`), the recorded pass as the downstream carrier; **(round 2) every
judge of the S5 window that reads its gaps — controller tiers 2-4 (N1), `story_step.finish`, `window_record.run`,
`driver_dispatch.Driver.window_gap` (N6, F14) — through ONE let-go predicate.** **Out.** FV1-30a's detectors and the recording call
(done); new question forms; FV1-19 N4 (`F19\:555`); the text road of `exit_gate.judge_words` and `controller._passed_by_person`
(`R30a\:70`, `:103`); the (b)-world listing of a word-passed obligation in "Left with you" (F10).

**AR-n touched and the change check each demands (written into the DoD of the node that touches it):**

| AR | why touched | change check (DoD line) |
|---|---|---|
| AR-1 | the closed sets "which finding is which fact", "which row field a word may pass" and (round 2) "which gap kinds a `not_run` word lets go" | `references/word-passed-facts.json` with ONE reader module (`waiver`); no `(check, tag)` list, no field list and no gap-kind list at any site (N0, N1); a field's exclusion is a row, never code (N0, N1) |
| AR-13 | "was this fact passed by word" gets one reader; "is this gap let go by a word" gets one predicate | Grep -i `startswith("no-row-")\|in ("no-bindings"\|unbound-\|startswith("product:")` over the package scripts after N1: hits only in the table reader / the survivor; positive control: the same call before the change hits `W\controller.py:7365`, `:7448` and `W\branch_accounting.py:1931` |
| AR-15 | one survivor, wired at every site | the sites list of §3 (each calls the index); the let-go survivor `window_record.word_let_go` called by every window judge (N1: controller tiers 2 and 4; N6: finish, `window_record.run`, `driver_dispatch`); a SIBLING_MAP axis row for the survivor in N0's commit, extended by N1 for `word_let_go` |
| AR-18 | the finding dict and the pass row gain `subjects` | `test_detector_verdict.py` stays green (`finding_line` does not read `subjects`, `s5_precheck.py:3919-3925`) |
| AR-22 | new fields `check`, `case`, `tag`, `subjects` in the journal line; `passed_by_word` on a window item; `word_passed` on a trace row and an obligation; `then` on a walk gap | each names its reader in the node; producer and reader land in the same node or the reader's node merges AFTER the producer's (N3 after N2) |
| AR-23 | empty pass record; empty `row_fields` table; empty `not_run` section | "no record / unreadable / empty list / no row for a field / no section" stated per reader (§5 E1-E3, E26, E30) and pinned by a row |
| AR-24 | the person's words reach the readers whole | the report quotes the word WHOLE from `stage_overrides` by `word_at` (N3) |
| AR-26 | a word-passed Then stays a requirement's gap | the requirement is never `proven` while a Then of it is word-passed (N2 walk row, N3 report row) |
| AR-27 | the verdict's owner for each fact | `trace_gaps["word_passed:then_unbound"] = "chain_broken"` (owner `product`, `M\delivery-verdict-kinds.json:38`); refs stay family `coverage:`/`coverage red:` (owner as today); unknown word = `no` (N2) |
| AR-28 | an unreadable record never becomes a pass; an emptied field never switches a check off; a gap an independent defect could raise is never let go | each reader's unreadable branch keeps today's refusal; `change_disposition`, `input_hash` (and, recommended F15, `change_basis_ref`) are never passed (D2c, N0 table row + N1 rows); `semantic_sensitivity:`, `sensitivity:`, `review:` never let go (F12, F13) |
| AR-29 | every added check is data, not judgment | census rows below; `test_judgment_census.py` green, no count raised (if raised: named, AR-20) |

**Checks the spec adds or alters — owner served and census class (AR-29, CLAUDE.md rule 10):**

| # | check | node | owner it serves | census class |
|---|---|---|---|---|
| K1 | `_judge_words` copies a finding's `subjects` into the pass row | N0 | data | not a check (a field copy) |
| K2 | `word_passed_index` maps a pass row to a fact by the table (`check`, tag exact or prefix) and a field to its `row_fields` row | N0 | data (the word is intent; the join is data) | xref |
| K3 | `_s5_v2_collect`: an instance the index names under `row_fields_unestablished` with `obligation_refs` skips the refs checks; an instance named under `not_run` owes no fingerprint | N1 | intent (the person's word), carried by data | xref |
| K4 | `window_record.build` keeps the `window_keys` of every passable field the pass names (empty) and writes `passed_by_word` | N1 | data | not a check (a writer) |
| K5 | tier-2 shape step drops the shape lines `word_let_go` lets go (the `not_run` section's forms) | N1 | intent, carried by data | xref |
| K6 | tier-4 `_s5_gap_problems` drops the gaps `word_let_go` lets go (30a's `product:` migrated into it; `evidence:`; the `tier4_gaps` of a named instance's passed fields) | N1 | intent, carried by data | xref |
| K7 | `check_traceability.walk`: a Then of a case with no `then_bindings` row that the index names ends the case's outcome with gap `word_passed:then_unbound` | N2 | data | xref |
| K8 | `coverage_projection`: an obligation whose binding names an instance with a refs pass and still-bad refs carries the word-passed gap words (never `verified`, which `witnessed_binding` already ensures, D13) | N2 | data | not a check (a text of an already-unverified item) |
| K9 | `branch_accounting._no_row_passed` reads the index (migration); `controller._s5_no_row_passed` removed (its one caller, tier 4, moves to `word_let_go`; no test calls it: Grep `_s5_no_row_passed` over `W\tests` → none, control `_s5_gap_problems` → 4 files) | N1 | data | xref (unchanged class) |
| K10 | `traceability_records` builds `to_check`/`how` for the `word_passed:then_unbound` gap in the after_checks branch | N2 | data | not a check (text of a record) |
| K11 | (round 2) `window_record.word_let_go(lines, window, index, lets_go)` — THE predicate "is this shape line / gap let go by a recorded word" | N1 | intent, carried by data | xref |
| K12 | (round 2) `story_step.finish`, `window_record.run`, `driver_dispatch.Driver.window_gap` judge the gaps `word_let_go` keeps, and print the ones it let go as "passed by the person's word" | N6 | intent, carried by data | xref |

No check reads a role's or a person's wording (FR-12): every join is by finding id, tag, case id, instance id, field name, gap kind or
Then number.

## §2. The one reader — what it is (N0)

### 2.1 Facts and their carrier
A finding the word passed is recorded at acceptance (30a: `S\controller.py:5907-5909` → `_record_s5_word_passes` `:2426-2440` →
`_record_person_pass` `:2389-2424`, file `state/passed-by-person.jsonl`). A line carries `ts, stage, dispatch, block, decision, by`, plus
`word_at`, `finding_id` when needed (`:2408-2421`). It does not say WHICH Then or instance: `row-fields-missing` is one finding with
case `""` (`W\s5_precheck.py:3832-3834`), and the instance of a `no-row` finding lives only in its tag (`:1960`), parsed by two readers
(`W\controller.py:7363-7366`, `W\branch_accounting.py:1929-1931`).

### 2.2 The change
1. **`subjects` on a finding.** `_finding(check, case, message, fix, tag, level="repair", subjects=None)` (`s5_precheck.py:266-268`) adds
   `"subjects": list(subjects)` only when given. A subject is one of `{"instance_id": iid}`; `{"instance_id": iid, "fields": [names]}`;
   `{"case": case, "then": n}`. Producers:
   - `check_run_mapping` `no-row-<iid>` (`:1952-1960`) and `unmatched-<iid>` (`:1964-1972`): `[{"instance_id": iid}]`.
   - `check_row_fields` (`S\:3840-3842`; `W\:3832-3834`): `[{"instance_id": iid, "fields": [names]} for each gap]` from its `gaps` list.
     N0 touches only the `_finding(...)` call (FV1-19 N2 owns another line, `F19\:341`).
   - `check_bindings`, producers of `no-bindings` and `unbound-<n>`: `no-bindings` → one `{case, then}` per Then of the case with no
     row; `unbound-<n>` → `[{"case": case, "then": n}]`. (Body not read by the designer, line range `A\:303` `:1247-1630`; the builder
     returns a question if a tag's Then set is not computable there — accepted by `CR\:128`.)
   - `check_plan_conformance` `plan-unreadable` (`:4512`): no subjects.
2. **The pass row carries `subjects`.** `_judge_words` (`:4003-4005`) adds `"subjects": finding.get("subjects") or []`.
3. **The journal line carries the parts.** `_record_s5_word_passes` passes `check`, `case`, `tag`, `subjects`; `_record_person_pass`
   writes each only when non-empty; `subjects` cut at 200 with `subjects_cut: <total>` (E9).
4. **The table** `references/word-passed-facts.json` (AR-1). **Round 2: the `row_fields` rows from S1's answer and the `not_run` section
   are written here; N0 lands `facts`, `words` and the three rows `obligation_refs`, `change_disposition`, `input_hash`; N1 adds the rest
   in the same commit as their readers.**
   ```json
   {"schema_version": 1, "note": "...",
    "facts": [
      {"check": "bindings", "tag": "no-bindings", "match": "exact", "fact": "then_unbound"},
      {"check": "bindings", "tag": "unbound-", "match": "prefix", "fact": "then_unbound"},
      {"check": "run_mapping", "tag": "no-row-", "match": "prefix", "fact": "not_run"},
      {"check": "manifest", "tag": "row-fields-missing", "match": "exact", "fact": "row_fields_unestablished"},
      {"check": "plan", "tag": "plan-unreadable", "match": "exact", "fact": "s5_plan_unread"}],
    "not_run": {"shape_missing": ["outcome", "execution_fingerprint"], "shape_probe_missing": true,
                "tier4_gaps": ["product", "evidence"]},
    "row_fields": {
      "obligation_refs": {"pass": true, "window_keys": {"obligation_refs": [], "obligation_ids": [], "obligation_hash": ""},
                          "tier4_gaps": ["obligation_binding", "obligation_hash"]},
      "assertion_id": {"pass": true, "window_keys": {"assertion_id": ""}, "tier4_gaps": ["assertion_identity"]},
      "defect_location": {"pass": true, "window_keys": {"defect_location": ""}, "tier4_gaps": ["defect_location"]},
      "profile_id": {"pass": true, "window_keys": {}, "tier4_gaps": []},
      "change_basis_ref": {"pass": false, "why": "the basis is the evidence of the disposition, and an `unchanged` disposition switches off the probe demand (proof_level._wanted): an empty basis would let an unsupported `unchanged` keep it off"},
      "change_disposition": {"pass": false, "why": "an empty value switches off the probe demand (contract.py probe-missing line; proof_level.proof_required)"},
      "input_hash": {"pass": false, "why": "an empty value makes the item malformed_instance and skips every later check of it (acceptance.validate_window)"}},
    "words": {"then_unbound": "Then not bound to a test", "not_run": "no run row", "row_fields_unestablished": "row fields not given",
              "s5_plan_unread": "the S5 plan not read", "other": "the finding stays as it was"}}
   ```
   `facts`: a pass whose (check, tag) matches no row is fact `other` (report line only, read by no gate). `unmatched-<iid>` is NOT a row
   (`R30a\:72`). `row_fields`: **a field with no row, or a row with `"pass": false`, is never passed by the word** (the safe default: the
   field is deleted when empty and refused at tier 2 as today). `not_run`: section absent, unreadable or not an object → a `not_run`
   word lets go NOTHING at tiers 2 and 4 (E30); tier 3's fingerprint rule for `not_run` is the fact's own meaning (§4 (3)), not a row.

   **The per-field table (S1 answered; every reader re-read on `W\` by the designer).** "Empty" = absent, `None`, `""` or `[]`; `build`
   deletes such a key today (`W\window_record.py:1357-1359`), so tier 2 says "missing" before any reader below runs.

   | field | tier 2 (`window_shape_errors`) | tier 3 (`_s5_v2_collect`) | tier 4 (`validate_window`) and below | does its empty value switch another check OFF? | passable | decided by |
   |---|---|---|---|---|---|---|
   | `assertion_id` | `<iid>: assertion_id is missing` (`W\contract.py:5511-5514`, `:5720`) | not read | `assertion_identity:<iid>` (`W\acceptance.py:1191-1192`); on a probed item `semantic_sensitivity:` (`:1229`, D10); receipt copy `assertion_refs=[]` (`W\window_record.py:1765`) → `witnessed_binding` not witnessed (`W\coverage_contract.py:265-266`) | no: every reader turns the empty value into a gap or a not-witnessed | **true** — `tier4_gaps: [assertion_identity]` | `W\acceptance.py:1191` |
   | `defect_location` | `<iid>: defect_location is missing` | not read | `defect_location:<iid>` (`:1193-1194`); probed: `semantic_sensitivity:` (`:1228`) | no | **true** — `tier4_gaps: [defect_location]` | `W\acceptance.py:1193` |
   | `change_basis_ref` | `<iid>: change_basis_ref is missing` | not read | `change_basis:<iid>` only when the disposition is valid (`:1195-1198`); coverage: item ≠ binding → not witnessed (`W\coverage_contract.py:263`), `unchanged` needs the binding's basis (`:603`) | **indirectly yes**: an `unchanged` disposition switches the probe demand off (`W\proof_level.py:452-457` reads the disposition; `W\contract.py:5727`), and the basis is that claim's only evidence | **false** (recommended, fork F15; S1 said true by the "switches nothing" criterion) | `W\acceptance.py:1197` + `W\proof_level.py:452-454` |
   | `change_disposition` | `<iid>: change_disposition is missing` | not read | `change_disposition:<iid>` (`:1195-1196`); the probe demand, `sensitivity:` and `change_basis:` go OFF (`:1153`, `:1197`, `:1207`; `W\contract.py:5727-5731`; `W\proof_level.py:452-457`) | **yes** (D2c) | **false** (confirmed) | `W\proof_level.py:452-457` |
   | `input_hash` | `<iid>: input_hash is missing` | not read | `malformed_instance:<iid>` and `continue`: every later check of the instance skipped (`W\acceptance.py:1115-1117`) | **yes** (D2c) | **false** (confirmed) | `W\acceptance.py:1115-1117` |
   | `obligation_refs` (window keys `obligation_refs`, `obligation_ids`, `obligation_hash`, written from refs, `W\window_record.py:1321-1323`) | three missing lines | refused `"coverage v2 instance requires unique obligation_refs with exact hashes"` and `continue` (`W\controller.py:7330-7333`): the fingerprint/unknown-stale/ids/hash checks (`:7341-7352`) never run for that instance — a skip INSIDE a refusal, not a switched-off pass; §4 re-asks the fingerprint for a refs-passed instance (invariant (2)) | `obligation_binding:` / `obligation_hash:` (`W\acceptance.py:1185-1190`); probed: `semantic_sensitivity:` (`:1226-1227`); coverage: never witnessed (D13 (ii)) | no | **true** — `tier4_gaps: [obligation_binding, obligation_hash]`; tier-3 refs kinds per F6 | `W\acceptance.py:1185-1190` |
   | `profile_id` | not a window field (`window=False`, `W\window_record.py:190-191`; not in `WINDOW_INSTANCE_FIELDS`) | not read | no window reader (Grep -i `profile_id` over acceptance/contract/controller/window_record/coverage_contract/story_step: hits are run-result and profile readers, none on a window item); at run, a shared test root with no `profile_id` refuses (`W\execution_request.py:1769-1776`) → the instance then has no run row, a DIFFERENT finding with its own word | no (a run refusal is a stop, not a silent pass) | **true** — `window_keys: {}`, `tier4_gaps: []`: the word passes the S5 exit finding and nothing else | `W\execution_request.py:1769` |

   `novelty_of` and `run_freshness_of` read none of these fields (`W\proof_level.py:393-425`, `W\acceptance.py:194-200`). A row with a
   `novelty` key can still be demanded a probe by its measured novelty (`W\proof_level.py:455-457`), which does not make
   `change_disposition` passable: a legacy row (no key) loses the demand.
5. **The reader.** `waiver.word_passed_index(rows, table=None) -> WordPasses` (pure; never raises) with:
   `.then(case, then, cfg=None) -> pass|None` (a `then_unbound` pass whose subjects name `(case, then)`, case by `contract.case_matches`);
   `.instance(fact, iid, field=None) -> pass|None` (a pass of `fact` whose subjects name `iid` by `contract.instance_id_aliases`
   equality; with `field`, only when that subject's `fields` contain it AND `row_fields[field].pass` is true); `.passed_fields(iid) ->
   [field]` (the subject's fields that are passable by the table); `.s5_plan() -> pass|None`; `.all() -> [pass]` (deduplicated, E5);
   `.skipped` (int, malformed rows). `pass` = `{finding_id, check, case, tag, fact, decision, at, by, ts, fields}`.
   `waiver.row_fields() -> (table_rows, why)`: the `row_fields` section; file absent/unreadable/section not an object → `({}, why)` (no
   field passable, E26). **(round 2, N1)** `waiver.not_run_lets_go() -> (section, why)`: the `not_run` section, same failure contract →
   `({}, why)` (nothing let go, E30).
   `waiver.person_passes(task_root) -> (rows | None, why)`: THE reader of `state/passed-by-person.jsonl` (item 5, `A\:374-375`), as in
   the first draft: stage `S5` lines; unparsable line skipped with one reason; unreadable file → `(None, why)`; no file → `([], "")`;
   repeats of `(dispatch, block, word_at)` collapse (A3-E5); old lines parse `block` by `split(":", 2)` once (A3-E4); the word from
   `stage_overrides[]` by `word_at`, else `decision`.
6. **(round 2, N1) The let-go survivor.** `window_record.word_let_go(lines, window, index, lets_go=None) -> (kept, let_go)`, pure, never
   raises (any exception → `(list(lines), [])`). `lines` are shape lines (`"<label>: <text>"`) and gap lines (`"<kind>:<iid>"`) in any
   mix; `lets_go` = `{"not_run": waiver.not_run_lets_go()[0], "row_fields": waiver.row_fields()[0]}` (read when `None`). A line is let go
   only by one of two rules, each needing `index` to name the line's instance:
   - **`not_run`**: `index.instance("not_run", iid)` AND the window item of `iid` has the NO-RUN shape — no `outcome` key, no truthy
     `execution_fingerprint`, `evidence_refs == []` (the writer's branch `W\window_record.py:1410-1413`) — AND the line is
     `"<iid>: <f> is missing"` for `f` in `shape_missing`, or `"<iid>: " + PROBE_MISSING_ERROR` when `shape_probe_missing` is true
     (imported, never retyped), or a gap `"<kind>:<iid>"` with `kind` in `tier4_gaps`.
   - **`row_fields_unestablished`**: a gap `"<kind>:<iid>"` with `kind` in `row_fields[f].tier4_gaps` for some `f` in
     `index.passed_fields(iid)`. (No shape line: the passable fields' keys exist, window record (i).)
   Every other line is kept. `index` `None` → nothing let go.

### 2.3 Two sources, one index (fork F3, Lead provisional (a), `CR\:73`)
- **At the S5 finish and in `window_record.build`/`run`** (nothing is recorded yet): the LIVE rows,
  `waiver.word_passed_index(s5_precheck.word_passes(root, scope, dispatch_id))`.
- **Below S5** (traceability, delivery, coverage, report): the RECORD, `word_passed_index(person_passes(root)[0])`.
- **A pass counts below S5 only while its fact still stands**: each lower reader asks the index only about a fact it already found by
  its own reading. The index never makes a fact appear.

### 2.4 Error direction of the reused `word_passes` in a gate role
`word_passes` was written for recording (30a). In N1 it becomes a GATE input. It may err only toward "no pass"; it must never return
a pass for a finding the word did not name, and **a pass must never let go more than the fields and gap kinds the table maps to what
the person named** — **(round 2) and never a gap kind that a defect independent of the named empty field could also raise on the same
instance (FR-4, AR-28: `semantic_sensitivity:`, `sensitivity:`, `probe_*:`, `review:`, `stale_review:`, `malformed_instance:`).**
Adversarial inputs that stay on the refusing side (rows of N0/N1): a word naming the CASE beside a
`row-fields-missing` finding; a parameter label of an iid (30a B1); a word for `no-row-A` when the instance is `A[neg]`; `*` with an
`open-oracle-asserted-1` finding; a revoked word; `pipeline.json` unreadable (→ `[]`); `word_passes` raising (→ refusing branch);
**(fix round) a `row-fields-missing` pass whose `fields` include `change_disposition` or `input_hash` (→ those keys are deleted as today
and refused at tier 2; the probe demand stands); a pass naming a field with no `row_fields` row (→ not passed)**; **(round 2) a `not_run`
pass for an instance whose window item shows a run (an `outcome`, a fingerprint or evidence) → nothing let go (E29); a refs pass on a
probed item → `semantic_sensitivity:` kept (E28); a `change_basis_ref` pass → deleted and refused (F15)**.
Known wrong-pass road inherited from 30a, not closed here (M2, `CR\:48-53`): `*` and a tag word are stage-wide and undated; the
subjects are those of the finding AT THE FINISH, not as the person saw it. E18 says so.

## §3. Per reader — what it reads today, what it must show, error direction, rows

### R1. Then not bound — the trace table (`traceability`, N2) and the report (`report_facts`, N3)
- **Today.** `Story.then_outcome` returns `{}` for a Then with no binding (`M\traceability.py:1150`); `case_rows` drops a Then with no
  outcome (`:1300-1302`). `report_facts._held_thens` holds pairs from unconfirmed entries and remainders (`M\report_facts.py:686-698`,
  called at `:774`); `_classify` turns `held` into `wait` (`:645-664`); with a `pass` row beside a non-held `not run` row the
  requirement reads `proven` (`:659-662`).
- **Must show (N2, trace table).** `Story.then_outcome` (final `return {}` at `:1150` only): when the RECORD index's `.then(case_key,
  then)` names the pair, return a row with `result` `not run`, `basis` "not bound to a test — passed by the person's word (<by>, <ts>)",
  `then: [n]`, and `word_passed: {"finding_id", "by", "ts", "decision"}`. The `Story` builds the index once (lazily, on the first such
  call).
- **Must show (N3, report).** `_requirements` passes to `_held_thens`, beside `unconfirmed` and `remainders`, the entries
  `{case: key_of(row.case), then: n, word_passed: True, by, ts}` built from the trace rows that carry `word_passed` (one per `then`
  number of such a row). `_partly_words` gets one branch first: `entry.get("word_passed")` → "Then N is not bound to a test, passed by
  your word (<ts>) (<case>)". So the requirement reads `wait`, never `proven`.
- **Error direction.** Silence is today's reading (the defect); never `pass` for the Then; never shown for a Then that has a binding row.
- **Rows — N2** (keep file `--witness-for` names for `traceability.py`): (t1) one Then bound green + one unbound word-passed → trace
  rows include the `not run` row with `word_passed`; (t2) no record → today's rows; (t3) the pass's Then now has a binding → that
  binding's outcome, no `word_passed`; (t4) record unreadable → today's rows. **Rows — N3** (`test_report_facts.py`): (r1) = t1's trace
  → requirement `wait`, `partly` names Then 2 and the time; (r2) = t2 → today's class; (r3) = t3 → no word line; (r4) unreadable record →
  today's class + `unknown["word_passes"]` = "what the person's word passed could not be read".

### R2. Then not bound — the delivery verdict (`check_traceability.walk` → `traceability_records` → kinds), N2 — rewritten (B3)
- **Today.** D8: `walk` is case-level; a case with any terminal outcome hides its unbound Then; `traceability_records` skips rows with
  an outcome (`M\check_delivery.py:1199`).
- **The join (fork F9; written for the recommended (a)).** In `walk` (`M\check_traceability.py:211-218`), after `_case_chain` returns
  for a case and BEFORE its outcome is appended: let `thens` = the case's Then numbers (`traceability.case_thens(Path(meta["path"]))`
  keys, `meta = cases[case]`), `bound` = the `then` values of `manifest["then_bindings"]` rows whose `case` matches the case
  (`C.case_matches(row_case, case, cfg)`), and for each `n in thens - bound` with `index.then(case, n)` → set this case's `outcome` to
  `""` and append `{"case": case, "gap": "word_passed:then_unbound", "then": n}` to `gaps` (one entry per such Then). The index is the
  RECORD index, built once per `walk` and only when the record file exists (E1: no file → no read, no change). A case whose
  `_case_chain` already returned `""` keeps its own gap AND gets the word-passed entries beside it.
- **Positional invariant (what must stay true).** (1) A case with no word-passed unbound Then reads byte for byte as today (no index
  call when the record is absent; no entry otherwise). (2) The gate-waiver loop after the case loop (`:230-239`) runs unchanged: a
  requirement the person waived AT A GATE still takes the waiver's terminal outcome (a different, older word; the gap stays visible
  beside it as today). (3) A Then with a `then_bindings` row is never annotated, whatever that row's status (its own reading decides).
  (4) An index/read failure, a case with no `path`, or `case_thens` raising → no entry for that case (today's reading) and nothing else
  changes; the report's E2 line says the record could not be read.
- **The kind (F4 = (a), Lead).** `references/delivery-verdict-kinds.json` `trace_gaps` gains `"word_passed:then_unbound":
  "chain_broken"` (verdict `no`, owner `product`). **This is a NEW `no`**: today such a Then is silent and the story can read `yes`.
- **The after_checks branch, built now (M3).** In `traceability_records`' after_checks branch (`M\check_delivery.py:1223-1230`), beside
  `question_open`: for `word == "word_passed:then_unbound"` the record gets `to_check` = "Then <n> of <case>: <the Then's text from
  `case_thens`>" and `how` = "passed by your word at S5 (<ts>): no test is bound to it". Under F4 (a) this branch is unreachable in
  production (the kind is `no`); it exists so that switching to (b) is ONE data row (`"unconfirmed_expectation"`).
- **Error direction.** Never `yes` while a word-passed unbound Then stands; never a new question (no question id; `how` names the word).
- **Rows** (keep files `--witness-for` names for `check_traceability.py` / `check_delivery.py`): (v1) only that gap → `delivery_ready:
  no` with kind `chain_broken`; (v2) with a `red` beside → `no`; (v3) kind row absent (temporal world 1, or a deployment without it) →
  `trace_gap:word_passed:then_unbound` → `no` (`M\check_delivery.py:1210-1211`); (v4) **a copy of the kinds file with the row set to
  `"unconfirmed_expectation"`** (`DV.load_kinds(path)` on the copy) → the requirement's record is after_checks and the "Left with you"
  item carries `to_check` "Then 2 of TC-…" and the `how` text; (v5) a case whose only other Then ran green (terminal) + the word-passed
  unbound Then → the row reaches `traceability_records` (the B3 case); (v6) the same requirement waived at gate A → waiver outcome, as
  today; (v7) no record file → `walk` result byte-identical to today's on the same fixture.

### R3. The S5 finish (controller tiers 2, 3, 4) and the window record, N1 — rewritten (B1, B2; round 2: one survivor)
- **Window record (`window_record.build`).** (i) For an instance whose LIVE `row_fields_unestablished` pass names fields, for each
  field `f` in `index.passed_fields(iid)`: the deletion loop (`W\window_record.py:1354-1361`) keeps `row_fields[f].window_keys` with their
  empty values (a field whose `window_keys` is `{}`, `profile_id`, keeps nothing), and the item gets `"passed_by_word": [{"finding_id",
  "fields": [passed fields], "at"}]` (precedent `window_record.py:1094-1095`). A field the pass names that is not passable (no row, or
  `pass: false`) is deleted as today and its `notes` line stays. (ii) A no-row instance named under `not_run`: **decision** — the window
  keeps `outcome` and `execution_fingerprint` ABSENT and `evidence_refs: []` (the no-run branch `W\window_record.py:1410-1413` unchanged;
  no outcome is invented; `WINDOW_OUTCOMES` unchanged, `W\contract.py:5517`) and the item gets `"passed_by_word": [{"finding_id", "fact":
  "not_run", "at"}]`. The index is built ONCE per `build` call, only when some row has an empty field or some instance has no run.
  (round 2) The kept `""` values meet the probe copy (D10): in a `probe_by_code` prepared block they read `None` ≠ `""`, so a probed
  item gets `semantic_sensitivity:` — kept by F12, so the refusing side.
- **Tier 2 — the shape lines a `not_run` pass removes (B1).** In `_s5_completion_problems`, right after `shape =
  window_shape_errors(window)` (`W\controller.py:7079`) and BEFORE `if shape:` (`:7080`): when `shape` is non-empty, `shape, _ =
  window_record.word_let_go(shape, window, self._s5_word_index(d))`. `window_shape_errors` stays pure. The door logic below
  (`:7080-7110`) runs on the filtered list. Row-field passes need no tier-2 branch: their keys exist (window record (i)).
- **Tier 3 — `_s5_v2_collect`.** §4.
- **Tier 4 — `_s5_gap_problems`, one let-go (B2).** Replace 30a's `product:` let-go (`W\controller.py:7444-7450`, the comment and the two
  statements) with ONE call, at the same position (after the handed/blocked/probe_gap/contradicts checks, BEFORE the `other_gaps`
  refusal at `:7451`): `other_gaps, let_go = window_record.word_let_go(other_gaps, window, self._s5_word_index(d))`, made only when
  `other_gaps` is non-empty. `Controller._s5_word_index(d)` (new; replaces `_s5_no_row_passed`, removed — K9) returns the live index or
  `None` on ANY exception (the refusing direction; the import of `s5_precheck`/`waiver` inside the `try`). The `passed_green` refusal
  (`:7453`) still reads the WHOLE `gaps` list (a completion with any gap, passed or not, is never `passed_green`). The handed / blocked /
  probe_gap / contradicts checks before it read `gaps` as today (none of their kinds is ever in a `tier4_gaps` list, so the position
  changes nothing for them).
- **Error direction.** May refuse what the index cannot confirm. Never lets go: an unnamed instance; a field not passable; a gap kind
  not in its field's `tier4_gaps` or the `not_run` section; any shape line outside the `not_run` forms; a `not_run` line of an item that
  shows a run; any tier-3 check of §4 (1); `sensitivity:`, `semantic_sensitivity:`, `probe_level:`, `probe_mutation_kind:`,
  `probe_evidence:`, `review:`, `stale_review:`, `mechanical_green:`, `stale_run:`, `malformed_instance:` of any instance (F12, F13).
- **The other judges of the window** (`story_step.finish`, `window_record.run`, `driver_dispatch.Driver.window_gap`): node N6 (F14),
  after N1. Until N6 lands: a window whose only gaps are let go is accepted by the controller while `window_record.run` prints "NOT
  acceptable" (E33); a mixed window gets no derived pair (E32) — both the refusing side, both inherited from 30a's `product:` let-go.
- **Rows** (`test_controller_state.py`, `test_window_record.py`): listed in §6 N1.

### R4. No run row — the ledger text, N2
- **Today.** No outcome → ledger `not_executed` → kind `not_executed` (`M\delivery-verdict-kinds.json:92`, `:28`, verdict `no`).
- **Must show.** `ledger_records` (`M\check_delivery.py:1648`): the text of a `no` record for a row whose cases include an instance
  the RECORD index names under `not_run` ends with "; passed by the person's word at S5 (<ts>)". Text only; the kind never changes.
- **Rows:** text with and without a record; `no` in both.

### R5. Refs not established — coverage, N2 — rewritten (round 2: S1 Q5 not measured; D12, D13)
- **Today.** `coverage_projection` verifies from `obligation_bindings` (`W\coverage_contract.py:560-655`). An obligation whose binding
  names a refs-passed instance is already never `verified`: `witnessed_binding` runs `validate_window` on the binding's instances and
  the accepted window carries `obligation_binding:`/`obligation_hash:` for it (D13 (ii)). What is missing is only the WORDS: today its
  `gap` reads "current sufficient evidence incomplete" (`:652-655`) with nothing about the person's word.
- **No unmeasured premise (replaces the M5 precondition).** S1 found no real TP1-13797 manifest (not measured). The branch therefore
  keys on the one join the projection already has — the binding's `instance_ids` (`:582`) — and only ADDS words; whether a real
  refs-absent row carries a binding decides only whether the words appear, never a verdict. N2 proves both worlds with CONSTRUCTED
  fixture rows (rows below), not with a real manifest.
- **Must show.** For an obligation with exactly one binding (`binding` non-empty, `:579`) where some `iid` in `instance_ids` has
  `index.instance("row_fields_unestablished", iid, field="obligation_refs")` on the RECORD index AND that instance's manifest row
  (`C.manifest_tests(manifest)`, matched by `C.instance_id_aliases`) has refs that are STILL BAD — `refs` not a list, or empty, or
  `C.obligation_ref_problems(refs, C.obligation_map(rows), strict=True)` non-empty (D12: an empty list returns `[]`, so emptiness is
  tested first, explicitly) — and the item is not `verified`: `word_passed: true` on the item, and the text "obligation_refs of <iid>
  not established — passed by the person's word (<by>, <ts>)" APPENDED to `gap` after "; " (never replacing it: an awaiting, person-debt
  or candidate gap stays first). `verified`, `person_debt`, `execution_state`, `sensitivity`, `code_validity` are never changed by this
  branch. Under F4 (a) it then reads through `coverage_reasons` unchanged (`coverage:` / `coverage red:`, verdict `no`).
- **No binding (`matching == []`, or two bindings).** Not this fact: such an obligation is today's unverified item with today's gap.
  Its S5 road is the separate `obligation-id-<oid>` finding (D13 (iii)), fact `other` in the table, shown by the report's `other` line
  (N3). Fork F16.
- **Error direction.** Never `verified` for such an obligation (already true, D13; the branch must not change it); any other obligation
  byte-identical to today; an index or read failure → no words, today's item.
- **Rows (constructed fixtures, keep file `--witness-for` names for `coverage_contract.py`):** (c1) a manifest row with refs ABSENT, a
  binding naming its instance, a record pass for `obligation_refs` → not verified, `gap` ends with the word text, `word_passed: true`;
  (c2) the same with refs `[]` → the same (D12); (c3) refs repaired (valid against the plan) → today's item, no words; (c4) no record
  file → today's item byte-identical; (c5) record unreadable → today's item; (c6) the same row with NO binding → today's item, no words
  (F16); (c7) a second obligation bound to another, unnamed instance → today's item. **S1 Q5's answer quoted in the N2 report: "not
  measured; constructed fixtures (c1)-(c7) stand in".**

### R6. S5 plan not read
F5 (b): the record is shown by the report line (fact `s5_plan_unread`); no controller refusal changes (D4; `CR\:83`).

## §4. The positional invariant in `_s5_v2_collect` (N1) — rewritten (B1, M1; round 2: `W\` lines)

Base: `W\controller.py:7321-7352` (FV1-19 N3 loop; today's refs refusal + `continue` `:7330-7333`, fingerprint `:7341-7344`,
unknown/stale `:7345-7347`, ids `:7348-7350`, hash `:7351-7352`). **S1 fact (re-read):** today a refs-bad instance is refused at
`:7332` and `continue`s, so its fingerprint was never asked; the branch below ASKS it for a refs-passed instance (invariant (2)) — a
refusal that today could not be reached becomes reachable, the refusing side. Prescribed shape:

```
index = None                                                  # NEW: built lazily, at most once per call
for item in window.get("instances") or []:
    refs = item.get("obligation_refs")
    if item.get("schema_version", 2) != 2:                    # M1: the version test FIRST, unchanged text
        problems.append((ValueError, "coverage v2 instance requires unique obligation_refs with exact hashes"))
        continue
    iid = str(item.get("instance_id") or "")
    refs_bad = <today's refs test, :7330-7331 without the version clause>
    no_fp = not item.get("execution_fingerprint") and item.get("outcome") not in (HANDED_OUTCOME, BLOCKED_OUTCOME)
    if refs_bad or no_fp:                                     # only then is the index consulted (invariant 4)
        index = index or self._s5_word_index(d)               # None on failure -> both flags False (invariant 5)
        not_run = bool(index and index.instance("not_run", iid))
        refs_passed = bool(index and index.instance("row_fields_unestablished", iid, field="obligation_refs"))
    else:
        not_run = refs_passed = False
    owes_fp = no_fp and not not_run
    if refs_passed:                                            # NEW branch
        if owes_fp:
            problems.append((ValueError, "coverage v2 instance requires execution_fingerprint"))   # byte-identical text
        continue                                               # refs, ids and row-hash checks skipped for this instance
    <today's body from :7330 on, with the fingerprint test reading `owes_fp` instead of its own condition>
```

`not_run` here reads the index alone, not the no-run shape of `word_let_go`: at tier 3 the condition `no_fp` already says the item has
no fingerprint; an item that has an outcome but no fingerprint and is named `not_run` is the E29 adversarial case — tier 2 kept its lines
(`word_let_go` checks the shape) and refused before tier 3, so tier 3 never sees it.

**Invariant (what stays refused).** (1) An instance the index names under neither fact goes through today's body byte for byte —
version + refs shape (`:7330-7333`, one text), fingerprint (`:7341-7344`), unknown/stale (`:7345-7347`), ids (`:7348-7350`), row hash
(`:7351-7352`), same order, same texts (FV1-19 N3 rows stay green). (2) **An instance passed ONLY for refs still owes its execution
fingerprint** (a word about refs is not a word about the run). (3) An instance named under `not_run` owes no fingerprint (it never ran,
the same footing as handed/blocked, `:7334-7340`), and — when not refs-passed — still goes through refs, unknown/stale, ids and hash.
(4) The index is built only when an instance has bad refs or no fingerprint (FR-55). (5) A reader that raises or returns nothing names
nobody: today's refusals stand. (6) The author/critic check, the mechanical round and the plan read (`W\controller.py:7290-7320`) run
before the loop as today (D6). (7) The version test precedes every branch: a non-2 instance is refused whatever word stands (M1).

Refs kinds a named instance lets go: fork F6 (Lead provisional (a): all, `CR\:84`; round 2: consistent with the FR-4 direction, because
`row_field_gaps` reports shape, unknown id and stale hash all under the one field `obligation_refs`, `W\window_record.py:279-303` — the
person was told of THAT field's problem, whichever it is).

## §5. Edges (each with the invariant it protects)

| # | Edge | Behaviour | Invariant |
|---|---|---|---|
| E1 | No `passed-by-person.jsonl` | `person_passes` → `([], "")`; readers as today; no report line; `walk` builds no index | an absent record is "no pass" |
| E2 | Record unreadable | `(None, why)`; gate readers refuse as today; lower readers as today; report prints ONE line (`A\:380`); `unknown["word_passes"]` | an unknown never becomes a pass, never a silent drop (AR-28) |
| E3 | Torn line, non-object line, no `block` | skipped, one reason with the line number | one bad line never hides the others |
| E4 | Old line (no `check`/`subjects`) | parts from `block` once; no subjects → matches no lookup (fact `other`/`s5_plan_unread`), report line only | an old record never lets a gate go on a guess |
| E5 | Two passes for one fact | collapsed by `(dispatch, block, word_at)`; lookup returns the latest by `ts` | one fact, one line |
| E6 | A pass for an instance retracted after S5 | no lower reader asks; no report line | a pass never makes a fact appear |
| E7 | A word older than a re-plan | at the next finish the live `word_passes` re-judges current findings (30a time rule, `s5_precheck.py:3998-4000`); below S5, R5 shows the words only while refs still fail the plan | a word about refs never makes a stale ref read verified; F7 |
| E8 | The fact repaired after the pass | readers find no fact → no annotation, no line | the report shows only what still stands |
| E9 | `subjects` with 5000 entries | journal: first 200 + `subjects_cut: 5000`; the index names only the 200 listed; the rest read as not passed; report says "and 4800 more" | a cut never passes an unnamed instance |
| E10 | `decision` 24 KB | journal keeps 1000 + `word_at`; the report quotes the word whole by `word_at` | AR-24 |
| E11 | `word_at` names no word in `stage_overrides` | report quotes `decision` + "(the recorded word is no longer in the story's record)"; gates use live words, where a revoked word is no word | a revoked word passes nothing at a gate |
| E12 | `word_passes` raises at the finish | `_s5_word_index` → `None`; nothing let go at tiers 2-4, today's refusals | refusing direction |
| E13 | Temporal: 30a lines exist before N0 (no `subjects`) | E4 | readable on old data |
| E14 | Temporal: before N2's kind row lands | `trace_gap:word_passed:then_unbound` → `no` | unknown kind never passes |
| E15 | Conflict: "the stage does not stand" vs "never proven" for a no-row instance | the finish lets the step go (tiers 2-3 per R3, tier 4 per F13); the ledger keeps `not_executed` → `no` | the word passes the step, never the fact |
| E16 | Conflict: "no second question" vs a `no` at gate B | gate B shows the reason with "passed by your word (<ts>)"; no new choice | FR-7 |
| E17 | `row-fields-missing` word when only `profile_id` was missing | the pass's `fields` lack `obligation_refs` → refs readers do not apply; `profile_id` is passable (`pass: true`, no window key, no tier-4 kind): the S5 exit finding is passed, nothing at tiers 2-4 changes, the run's own refusal stands | a word is read for the fields it was given for |
| E18 | **(restated, M2)** A stage-wide word (`*`, or the tag `row-fields-missing`) and the case-less finding | live words are `live_stage_overrides(pipeline, ("S5",))` and undated for a finding with no `pair_at`; the word passes the CURRENT case-less finding as it stands at this finish, and its `subjects` (computed now) decide per instance — so an instance added after the person spoke IS passed by an old `*` | stated truthfully, not prevented: inherited from `A\:348`; the bound on harm is the `row_fields` table (no proof-bearing field is passable, E20) and F7 |
| E19 | **(B1)** An instance named under BOTH `not_run` and a refs pass | tier 2: its run lines dropped, its refs keys kept; tier 3: refs branch, `owes_fp` false → no line; tier 4: `product:`, `evidence:` and `obligation_binding:`/`obligation_hash:` let go; `sensitivity:`/probe kinds/`review:` kept (F12, F13) | each fact is let go only by its own pass |
| E20 | **(fix round)** A pass whose `fields` include `change_disposition`, `input_hash` or (F15) `change_basis_ref` | those keys deleted when empty, tier 2 refuses `"<iid>: change_disposition is missing"` (etc.) as today | an emptied field never switches the probe demand or the instance's checks off (AR-28) |
| E21 | A completion with `passed_green` and a word-passed gap | refused `"a completed process with gaps cannot be passed_green"` (reads the whole `gaps`) | a passed gap is still a gap |
| E22 | A case in `walk` with no `path`, or `case_thens` raising | no word-passed entry for it; today's reading | a read failure never invents or drops a gap silently (the report's E2 line covers the record; the case path is the case index's own gap) |
| E23 | A requirement waived at a gate AND holding a word-passed unbound Then | waiver's terminal outcome (today's loop); the gap is visible in `gaps` | a gate word is not overruled by an S5 word |
| E24 | A Then with a `then_bindings` row of any status | never annotated | the binding's own reading decides |
| E25 | **(M1)** A named instance with `schema_version != 2` | today's text, refused | the version test precedes every branch |
| E26 | Temporal: `row_fields` absent (before N0's table lands, or an unreadable table) | no field passable: keys deleted, tier 2 refuses as today; facts still map | an unknown table never passes a field |
| E27 | **(S1 confirmed)** A completion WITH `unresolved` + `reason` | tier-4 other gaps already pass today, whatever the pair names (`W\controller.py:7451`); `finish` derives the pair only for the four `DERIVED_GAP_KINDS` (`W\story_step.py:1619`, `:1682`), a typed pair passes; the let-go changes nothing for such a completion | stated so the let-go is not mistaken for a new pass |
| E28 | **(round 2, F12)** A probed (`proof_required`) item with a passed `obligation_refs` / `assertion_id` / `defect_location` | its `tier4_gaps` let go; `semantic_sensitivity:` kept (raised by the empty field AND by independent probe defects, D10) → refused without the pair; accepted with it (E27) | a gap an independent defect could raise is never let go (FR-4, AR-28) |
| E29 | **(round 2)** A `not_run` pass for an instance whose window item has an `outcome`, a fingerprint or non-empty `evidence_refs` | `word_let_go` lets nothing go for it (the no-run shape fails) → today's lines | a word about "no run" never covers an item that shows a run |
| E30 | **(round 2)** Temporal/unreadable: the `not_run` section absent (N0's table before N1, or an unreadable table) | `not_run_lets_go()` → `({}, why)`: nothing let go for `not_run` at tiers 2 and 4 — **including 30a's `product:`** (a refusal 30a lets go today comes back in that world); N1 lands the section and its reader in ONE commit | an unknown table lets nothing go (refusing direction) |
| E31 | **(round 2, D12)** R5: refs absent / `None` / not a list / `[]` | "still bad" by an explicit emptiness test BEFORE `obligation_ref_problems` | an empty list never reads as repaired refs |
| E32 | **(round 2, D11, F14)** A window whose gaps mix a word-passed gap with a derivable one (`blocked_by_env:`, `probe_gap:` ...) at `story_step.finish` | before N6: no pair derived, the controller refuses with the door "finish derives that pair" (a dead door, inherited from 30a); after N6: `finish` derives over the gaps `word_let_go` keeps | a door a refusal names is one the receiver can use (FR-2) |
| E33 | **(round 2, D11, F14)** `window_record.run` on a window whose only gaps are word-passed | before N6: "NOT acceptable yet" + exit 1 (the critic is sent to repair an acceptable window); after N6: listed as "passed by the person's word", exit 0 when nothing else remains | one judgment of one window (P31, AR-15) |
| E34 | **(round 2, D10)** A kept `""` meets a `probe_by_code` prepared block's `None` | `semantic_sensitivity:` raised; kept (E28) | the refusing side; never a pass |

## §6. Nodes

Order: **(S1 ∥ N0) → (N1 ∥ N2); N3 after N2; N6 after N1; N5 after N1.** N1 also after FV1-19 N3 and FV1-30a (both in `W\`).
`очередь: FV1-30a → FV1-30b`, `очередь: FV1-19 N3 → FV1-30b N1`, `очередь: FV1-19 N2 → FV1-30b N0`. Every builder node's given basket:
`design/factory-rules.md` whole, `plans/builder-rules.md`, this spec, `A\:322-419`, `R30a\`, `CR\`. Tests are ROWS of existing keep files
(TESTING.md; no new test file). Witness: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <the node's
owns>` (builder-rules 7b). If `--witness-for` names no keep file for an owned path, the builder returns a question before writing.

Parallel ownership check: N1 = `controller.py` (`_s5_*` functions), `window_record.py` (`build`, new `word_let_go`),
`branch_accounting.py`, `waiver.py` (new `not_run_lets_go` only), the table (`row_fields` rows + `not_run` section), their test files;
N2 = `traceability.py`, `check_traceability.py`, `check_delivery.py`, `delivery-verdict-kinds.json`, `coverage_contract.py` and the keep
files of those; N3 = `report_facts.py`, `test_report_facts.py` (after N2); N6 = `story_step.py` (`finish`), `window_record.py` (`run`),
`driver_dispatch.py` (`Driver.window_gap`) (after N1). No path is owned by two nodes that run at the same time (N1 ∥ N2 share no file;
N1 owns `waiver.py` and `test_words_doors.py` rows only AFTER N0 merged). If `--witness-for` names one keep file for both an N1 and an N2
path, the Lead serialises N2 after N1 before launch.

### S1 — scout (read-only, parallel with N0): the F2 question list (CR §4 F2, M5) — ANSWERED (round 2)
Question, per field `assertion_id`, `defect_location`, `change_basis_ref`, `profile_id`, and every other field `WR.row_field_gaps`
can return (the scout lists them from `window_record.REQUIRED_ROW_FIELDS`):
- Q1. Every reader of the EMPTY or ABSENT value in `window_shape_errors`, `_s5_collect`/`_s5_v2_collect`, `validate_window`
  (`M\acceptance.py:1113-1230`), `proof_level.proof_required`, novelty/`run_freshness_of`, and the S7/S8 readers of the window, each with
  the gap or behaviour it yields (file:line).
- Q2. Which empty value switches OFF another requirement (as `change_disposition` and `input_hash` do, D2c).
- Q3. For a no-row instance (no `outcome`, no `execution_fingerprint`, no `probe`): every line of tiers 2-4 it hits beyond D3's list
  (e.g. tier-3 (c), (i)).
- Q4. Confirm or refute D2b/E27 (the `unresolved` + `reason` pair already passes tier-4 `other_gaps`) and whether `story_step.py finish`
  derives that pair for these gaps.
- Q5 (M5). On a real TP1-13797 manifest (the scout locates one; the designer's Glob `experiments/**/*13797*/**/automation-manifest.json`
  found none, an unverified absence): does a row whose refs are absent still have an `obligation_bindings` entry naming its instance?
Completeness: a table field → readers → gap → `pass: true|false` + why; Q3-Q5 answered with file:line or "not found" with a trail and
a positive control. Handoff: a digest file named by the Lead. The Lead writes the answer into §2.2 item 4 (rows) and §3 R5 before N1/N2.
**Answers (written in round 2, each re-read on `W\`):** Q1/Q2 → §2.2 item 4 per-field table (one change against the scout:
`change_basis_ref` recommended NOT passable, F15). Q3 → D3 (tier-4 list) and fork F13. Q4 → E27 confirmed; derivation refuted (four
kinds only) → D11, fork F14 (the scout's "driver_dispatch holds the same four" corrected: it holds handed + the critic's two kinds).
Q5 → not measured (whole-repo glob timed out: not a negative) → R5 rewritten on D13; N2 proves both worlds on constructed fixtures.

### N0 — subjects, the table, the one reader (depends: FV1-30a merged)
owns:
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\s5_precheck.py` (`_finding`; the `_finding(...)` calls in `check_run_mapping` `no-row`/`unmatched`, `check_row_fields` at `:3842` only, `check_bindings` producers of `no-bindings`/`unbound-<n>`; `_judge_words` pass dict; `word_passes` docstring)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\waiver.py` (new `person_passes`, `row_fields`, `word_passed_index` + its class)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\controller.py` (`Controller._record_s5_word_passes`, `Controller._record_person_pass` only)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\references\word-passed-facts.json` (new)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_s5_precheck.py` (rows)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_words_doors.py` (rows)
`C:\QAFactory\forge-repo\docs\SIBLING_MAP.md` (one axis row: the survivor `waiver.word_passed_index`)
Rows: (a) every finding dict without `subjects` byte-identical (table over the families of `A\:300-308`); (b) `no-row-A` →
`[{"instance_id": "A"}]`; (c) `row-fields-missing` over two rows → two subjects with fields; (d) `no-bindings` with Thens 1 and 3 unbound
→ two `{case, then}`; (e) pass row copies `subjects`; (f) journal line carries `check, case, tag, subjects`; (g) 5000 subjects → 200 +
`subjects_cut` (E9); (h) `person_passes`: no file / unreadable / torn / old / duplicate (E1-E5); (i) `word_passed_index`: `.then` hits by
`case_matches`, misses a sibling case; `.instance` hits an alias, misses a parameter-label prefix; unknown (check, tag) → `other`;
`unmatched-A` → `other`; (j) §2.4 adversarial inputs stay unpassed; (k) `.instance(..., field="change_disposition")` and `field="input_hash"`
→ None although the subject names them; a field with no row → None; `passed_fields` lists only `obligation_refs` for a subject with
`["obligation_refs", "change_disposition"]`; (l) `row_fields()` with the section absent / not an object / file unreadable → `({}, why)`
and no field passable (E26); (m) Grep -i `word-passed-facts` over the package scripts → only `waiver.py` (positive control: the name in
the table's own `note`).
edges: E1-E5, E9, E10, E13, E18, E20, E26.
DoD: rows green; `test_detector_verdict.py` unchanged (AR-18) if `--witness-for` names it; Grep (m) and the AR-13 Grep pasted;
`architecture:` AR-1, AR-13, AR-15, AR-18, AR-22, AR-23, AR-28, AR-29; census K1, K2; SIBLING_MAP row in the same commit. Witness:
`python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/s5_precheck.py ai-packages/qa-factory/scripts/waiver.py ai-packages/qa-factory/scripts/controller.py ai-packages/qa-factory/references/word-passed-facts.json`.
(Round 2: N0 not touched — a builder is implementing it. Noticed facts that bear on it: §12 "Noticed".)

### N1 — the S5 finish, the window record and the let-go survivor (depends: N0 merged; S1 answered; FV1-19 N3, FV1-30a — both in 4d0ad66)
owns (line numbers for base 4d0ad66; locate by function and quoted text):
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\controller.py` (`Controller._s5_completion_problems` — the one tier-2 call after `shape = window_shape_errors(window)` `:7079` only; `Controller._s5_v2_collect` `:7275` — the loop of §4 `:7321-7352`; `Controller._s5_gap_problems` `:7369` — the one tier-4 call replacing `:7444-7450` only; `Controller._s5_no_row_passed` `:7354-7367` — removed; new `Controller._s5_word_index`; not `_record_*`)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\window_record.py` (`build`: the deletion loop `:1354-1361` and `passed_by_word` on the no-run branch `:1410-1413`; new `word_let_go`)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\branch_accounting.py` (`_no_row_passed` `:1921-1933`, `_word_pass_rows` `:1907-1918`: read the index)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\waiver.py` (new `not_run_lets_go` only)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\references\word-passed-facts.json` (`row_fields` rows `assertion_id`, `defect_location`, `profile_id`, `change_basis_ref` and the `not_run` section, exactly as §2.2 item 4; nothing else)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_controller_state.py` (rows)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_window_record.py` (rows)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_branch_accounting.py` (rows)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_words_doors.py` (rows: 30a's `product:` rows stay green; `not_run_lets_go`)
`C:\QAFactory\forge-repo\docs\SIBLING_MAP.md` (extend N0's axis row with the survivor `window_record.word_let_go` and its four judges)
(`acceptance.py` is NOT owned: S1 named no tier-4 reader that must change — the struck line of round 1.)
non-goals: `story_step.py`, `window_record.run`, `driver_dispatch.py` (N6); `_terminal_runs` (N5); any change to `validate_window` or
`window_shape_errors`; any new question text; N0's functions in `waiver.py`.
Rows: (a) instance with refs absent, `change_disposition: unchanged` + a basis (no probe branch), word `row-fields-missing` naming
`obligation_refs`, completion WITHOUT `unresolved` → window keeps the three keys empty + `passed_by_word`; tier 2 no line for them;
tier 3 lets the instance go (it has a fingerprint); tier 4 drops `obligation_binding:`/`obligation_hash:` of it; **the completion is
accepted end to end through tier 4** (B2); (a2) **(F12)** the same on a `new_or_changed` item with a `probe_by_code` prepared probe block
→ tier 4 refuses `"unresolved window: semantic_sensitivity:<iid>"` (and no `obligation_*` kind); with the pair → accepted (E27, E28);
(b) the same with no word → today's tier-2 lines byte-identical; (c) a second instance NOT named with a stale ref → the `:7346` text
beside the named one; (d) a refs-only named instance with no fingerprint → the fingerprint text (§4 (2)); (e) `_s5_word_index` raising
(monkeypatched `word_passes`) → today's refusals at tiers 2-4; (f) word for `profile_id` only → refs refused as today; nothing at tiers
2-4 changes (E17); (g) **a no-row `new_or_changed` instance named under `not_run`, completion with `unresolved` + `reason`** → tier 2 has
none of its three lines, tier 3 no fingerprint line, tier 4 lets `product:` and `evidence:` go → accepted; **the same without the pair** →
refused `"unresolved window: ..."` naming `sensitivity:<iid>` and the other probe kinds it raises, never `product:`/`evidence:` (F13);
not named → today's tier-2 lines; (g2) **(B1 row) the same instance also refs-passed** → E19, accepted with the pair; (g3) **(E29)** a
`not_run` pass for an instance whose item carries an `outcome` → its shape lines and gaps kept; (h) `branch_accounting._no_row_passed`
returns the same answers on 30a's rows (30a rows in `test_words_doors.py` green, `product:` let-go among them) and the package holds no
`startswith("no-row-")` / tag tuple / `startswith("product:")` let-go outside the table reader and `word_let_go`; (i) a pass naming
`change_disposition` → `"<iid>: change_disposition is missing"` still at tier 2 (E20); (i2) a pass naming `change_basis_ref` →
`"<iid>: change_basis_ref is missing"` still at tier 2 (F15); (j) a named instance with `schema_version: 1` → today's version text (M1,
E25); (k) `passed_green` completion with a let-go gap → refused (E21); (l) per added row: `assertion_id` passed → key kept `""`,
`assertion_identity:` let go, `defect_location:` of the same instance (not passed) kept; `defect_location` symmetrically; (m)
`word_let_go` table over its inputs: unnamed instance; field not passable; kind not listed; shape line of another form; `index` None;
`not_run` section absent → every line kept (E30); (n) `not_run_lets_go()` with the section absent / not an object / file unreadable →
`({}, why)`.
edges: E7 (gate side), E12, E15, E17, E18, E19, E20, E21, E25, E26, E27, E28, E29, E30, E34; positional invariant §4 (1)-(7); R3 tier-2/
tier-4 invariants; §2.2 item 6.
DoD: rows green; FV1-19 N3 rows green unchanged; 30a rows in `test_words_doors.py` green; the AR-13 Grep of §1 pasted with its positive
control; critic on the diff (controller core, rule 3); census K3-K6, K9, K11; `architecture:` AR-1, AR-13, AR-15, AR-22, AR-24, AR-28,
AR-29. Witness: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/controller.py ai-packages/qa-factory/scripts/window_record.py ai-packages/qa-factory/scripts/branch_accounting.py ai-packages/qa-factory/scripts/waiver.py ai-packages/qa-factory/references/word-passed-facts.json`.
**N1 status: READY FOR DISPATCH once N0 is merged** — owns disjoint from N2 by file; every edge decided (written for the recommendations
of F12, F13, F14 (N1 half), F15); each row names its input and expected text. If the Lead flips F15 to "passable", row (i2) becomes "key
kept, `change_basis:` let go" and the table row changes — one row each. If the Lead flips F13 on `evidence`, drop `evidence` from the
`not_run` section and from row (g).

### N2 — trace table, walk join, delivery verdict, ledger text, coverage (depends: N0)
owns:
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\traceability.py` (`Story.then_outcome` final `return {}` branch only; the lazy record index on `Story`)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\check_traceability.py` (`walk`: the per-case Then join of §3 R2 only)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\check_delivery.py` (`traceability_records`: the after_checks `to_check`/`how` for `word_passed:then_unbound`; `ledger_records`: the text suffix; nothing else)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\references\delivery-verdict-kinds.json` (`trace_gaps` row; `note` sentence)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\coverage_contract.py` (`coverage_projection` `:560`: the R5 words branch only, after `item` is built `:644-655`)
rows in the keep files `--witness-for` names for these five paths.
non-goals: any change to `verified`, `person_debt` or `witnessed_binding`; the no-binding obligation (F16); a "Left with you" listing
for refs (F10); the report (N3).
Rows: R1 (t1)-(t4); R2 (v1)-(v7); R4 rows; R5 (c1)-(c7) on constructed fixtures.
edges: E1, E2, E6, E7 (below S5), E8, E14, E15, E16, E22, E23, E24, E31.
DoD: rows green; `architecture:` AR-1, AR-22, AR-26, AR-27, AR-28, AR-29; census K7, K8, K10; S1 Q5's answer quoted in the report ("not
measured; constructed fixtures (c1)-(c7) stand in").
Witness: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/traceability.py ai-packages/qa-factory/scripts/check_traceability.py ai-packages/qa-factory/scripts/check_delivery.py ai-packages/qa-factory/references/delivery-verdict-kinds.json ai-packages/qa-factory/scripts/coverage_contract.py`.
**N2 status: READY FOR DISPATCH once N0 is merged** — R5 no longer rests on S1 Q5 (D13); edges decided (E31 new); owns disjoint from N1
by file; F9 and F16 written for their recommendations (F9 (a) walk; F16 (a) binding only).

### N3 — the report (item 5 of `A\:374-382`, and R1's report half) (depends: N0, N2)
owns:
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\report_facts.py` (new `_word_passed_gap`; one line in `build`; one term in `render`; `_requirements` — the word-passed entries handed to `_held_thens`; `_partly_words` — one branch)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_report_facts.py` (rows)
`_word_passed_gap(art, facts)` builds through `left_gap_line` (`report_facts.py:859-873`) one line per pass a reader annotated — a
trace row with `word_passed`, a ledger record with the suffix, an obligation with `word_passed` — or of fact `other`/`s5_plan_unread`:
ref = case or instance (else finding id), what = "<the fact's words> — passed by your word \"<word whole, by word_at>\" (<by>, <ts>)",
needed = "a test bound to it, or your check by hand" / "a run of it" / "the refs given, or your acceptance of the coverage gap" / "a
readable S5 plan".
Rows: item 5's four (`A\:381-382`); R1 (r1)-(r4); E6/E8 (fact no longer stands → no line); E11.
edges: E1-E4, E6, E8, E10, E11.
DoD: rows green; `architecture:` AR-22, AR-24, AR-26, AR-27, AR-28; census: none new (text). Witness: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/report_facts.py`.

### N5 — residual (M4): the alias / exact-id split of "no run row" (queued; not in this batch's parallel set)
owner: the Lead of pile `fv1` (pile line to be written by the Lead). owns (when cut):
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\window_record.py` (`_terminal_runs`)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_window_record.py` (one row)
Behaviour: `_terminal_runs` finds an instance's terminal run under any `contract.instance_id_aliases` spelling, as the precheck does
(`s5_precheck.py:1948-1950`); row: a run row spelled by an alias → the window item has its outcome and fingerprint. Invariant: a run of
ANOTHER instance (a parameter-label prefix) never counts. Depends: N1 (same file). Status: queued.

### N6 — (round 2, F14) the other three judges of the S5 window read `word_let_go` (depends: N1; written for F14 (b))
owner: the Lead of pile `fv1`. owns (line numbers for base 4d0ad66):
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\story_step.py` (`finish` `:2372`: the derivation block `:2540-2555` only — `gaps` filtered through `word_let_go` before `_derived_pair`)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\window_record.py` (`run` `:1996`: the `problems` filtered through `word_let_go` before `derivable` `:2031-2035`; the let-go lines printed as `note: passed by the person's word: <line>`)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\driver_dispatch.py` (`Driver.window_gap` `:922-964`: the `validate_window` gaps filtered through `word_let_go` before the "any other gap gives ()" test `:947-949`)
rows in the keep files `--witness-for` names for these three paths.
Behaviour: each site builds the LIVE index once (`waiver.word_passed_index(s5_precheck.word_passes(root, cases, dispatch_id))`, cases =
the window's `scope_instances` keys, dispatch = the site's own dispatch id; any exception → `None` → nothing let go) and judges only
the lines `word_let_go` keeps. Rows: (n1) `finish` on gaps `[obligation_binding:A, probe_gap:B]` with A refs-passed → derives the
`probe_gap` pair; without the word → `()` (today); (n2) `window_record.run` on a window whose only gaps are A's word-passed ones → exit 0,
a `passed by the person's word` note per line; with one more unpassed gap → today's "NOT acceptable" listing it; (n3) `window_gap` on
`[handed_to_person:A, product:B]` with B `not_run`-passed → derives the handed pair; (n4) the index raising → each site as today.
Invariant: a site never derives a pair over a gap `word_let_go` kept that is not derivable today (t-204 F1); a let-go line is printed,
never silently dropped. edges: E12, E29, E30, E32, E33. DoD: rows green; census K12; `architecture:` AR-13, AR-15, AR-28, AR-29.
Witness: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/story_step.py ai-packages/qa-factory/scripts/window_record.py ai-packages/qa-factory/scripts/driver_dispatch.py`.
Status: queued after N1 (same file `window_record.py`); not in the N1 ∥ N2 set. Covers 30a's `product:` let-go too (the same class).

### Crossings (function-level)
| other | its owns | overlap |
|---|---|---|
| FV1-30a | `_passable`, `_names`, `_judge_words`, `word_passes`, `_record_person_pass`, `_record_s5_word_passes`, `_s5_gap_problems`, `_s5_no_row_passed`, `_plan_refusal`, `branch_accounting.s5_problems` | N0/N1 edit some: sequential, `очередь: FV1-30a → FV1-30b` (30a is in 4d0ad66) |
| FV1-19 N2 | `check_row_fields` (one call line), `_row_fields_text`, `window_record` carrier | N0 edits the other call line; `очередь: FV1-19 N2 → FV1-30b N0` |
| FV1-19 N3 | `_s5_v2_collect` | N1 rewrites the loop: `очередь: FV1-19 N3 → FV1-30b N1` (N3 is in 4d0ad66) |
| T3b (brief_pack) | `window_record.row_field_lines` | none |
| N0 (this spec) | `waiver.py` (its functions), `test_words_doors.py` | N1 adds one function / rows after N0 merged: sequential |

## §7. Siblings (rule 9) and queue
Axes named for this class: 17, 26, 29, 34 (`R30a\:101-105`; the map is walked by N0's builder, which adds the survivor's axis row; N1
extends it with `word_let_go`).
- `report_facts._changes` re-reads S5 overrides by substring (`report_facts.py:1636-1637`): queued (the pair has its own reader).
- Alias vs exact id (D3): node N5 above (M4).
- `unmatched-<iid>` second question at tier 4 (30a Q4): queued there.
- `controller._passed_by_person`, `exit_gate.judge_words` text road: queued there.
- (round 2) The four judges of one window (D11): N1 (controller) + N6 (finish, `window_record.run`, `driver_dispatch`) — one survivor.

## §8. Forks

Decided by the Lead (binding): **F4 = (a)**, **F8 = (a)**. Open, each with a recommendation; nodes are written for the recommendation.

**F1 — items 6 (2-3) and 7 of `A\:383-392`.** (a) a node N4 in this group (`refusal_cause` → `awaits_answer` for
`open-oracle-asserted-*`, `REFUSAL_CAUSES`, `story_step._gate_refusal` door, C4г `known_red: FV1-30` labels removed); (b) later.
**Recommendation (a)** (critic: holds, `CR\:62`). N4 is written in full once the Lead confirms.

**F2 — the other window fields `row-fields-missing` names.** Direction (a), one road, confirmed by the critic (`CR\:63`): every field
passes through ONE data table (`row_fields`), and a field whose empty value switches another check off is excluded BY A ROW, not by
code. Measured exclusions: `change_disposition`, `input_hash` (D2c, S1 confirmed); round 2 adds the rows `assertion_id`,
`defect_location`, `profile_id` (passable) and `change_basis_ref` (F15). **Recommendation: confirm (a) with the rows of §2.2 item 4.**

**F3 — the source of the index below S5.** (a) the record; (b) live everywhere. **Recommendation (a)** (`CR\:73`).

**F4 — DECIDED (a) by the Lead.** Correction of the premise (`CR\:74`): for the unbound Then, (a) is a **NEW `no`** — today the Then is
silent and the story may read `yes`; for refs, (a) keeps today's `no` (an unverified obligation already blocks). The owner question,
reworded truthfully: «Если вы сказали "иди дальше" при непривязанном к тесту Then или неполных ссылках на обязательства, отчёт сейчас
будет говорить "не готово" с этим пунктом (для непривязанного Then это новое: раньше такой Then молча пропадал). Оставить "не готово"
или сделать "готово после ваших проверок" с пунктом в "Left with you"?» Switching the Then to (b) later is ONE data row (M3 branch built
now). Switching refs to (b) is NOT one row today — fork F10.

**F5 — S5 plan unreadable.** **Recommendation (b)** (`CR\:83`).

**F6 — which refs kinds a named instance lets go.** **Recommendation (a)** all (`CR\:84`); round 2: holds under the FR-4 direction
(§4 last paragraph: shape, unknown and stale are all problems of the ONE named field).

**F7 — a word given before a re-plan, at the next finish.** (a) as 30a (undated); (b) date by plan approval. **Recommendation (a),
conditional (as the critic requires, `CR\:85-87`):** it holds because no proof-bearing field is passable — the `row_fields` table
excludes every field whose empty value disables a check (F2, S1). If the Lead rejects the exclusion rows, or flips F15 to "passable",
F7 flips to (b).

**F9 (new, B3) — where the Then-level join lives.** (a) `check_traceability.walk` (§3 R2 as written): the delivery's own trace input,
the after_checks/`to_check` road already exists there (`M\check_delivery.py:1223-1230`), one record per fact. (b) `ledger.plan_row_state`
(`A\:883` lists it; `M\ledger.py:679`): a new state `not_verified:word_passed_then_unbound` after every failure word and before
`passed_green`, mapped in `ledger_states`. Cost of (b): the ledger has no `to_check` road (the item text is built later by kind,
`M\check_delivery.py:2142-2185`), and the trace table and the ledger would then both need the fact (two readers into the verdict for
one fact unless `walk` is left silent). **Recommendation (a)**; `A\:883`'s ledger row then reads "ledger: not a reader of this fact; the
walk carries it" — the Lead amends `A\:883` or rejects.

**F10 (new, CR F4 note) — refs under a future (b).** (a) Build now: a `coverage_gaps` table in the kinds file + `DV.kind_of_coverage_gap`
read by `coverage_reasons`, plus a "Left with you" listing for a word-passed obligation (none exists: `M\ledger.py:1801` lists ledger
rows; D9). Cost: a new kinds section, a reader, a listing, rows — for a branch F4 (a) never takes. (b) Not now: F4 says "switching refs
to (b) is a code change (one kinds row + one listing branch), a node of its own if the owner picks (b)". **Recommendation (b)**: the
critic's own alternative (`CR\:82`); a half switch would be a dead reader (AR-22).

**F11 — superseded by F13** (round 2): its question (does a `not_run` word let go `sensitivity:`/`review:`) is one row of F13's
enumeration; F11's recommendation (a) is kept there.

**F12 (round 2, S1 fork (a)) — `semantic_sensitivity:` on a probed item whose row field the word passed.** Facts: an empty
`obligation_refs` / `assertion_id` / `defect_location` on a `proof_required` item can yield it (`W\acceptance.py:1219-1234`; D10: in a
`probe_by_code` prepared block always, in a receipt-path block not); the same kind is ALSO raised by independent probe defects — a probe
of another line (`receipt_off_target`, `:1233`), `defect_location == expected_location` (`:1230`), probe ids/hash that differ from
non-empty item ids/hash (`:1226-1227`). Per gap kind, the side (the Lead's FR-4 / AR-28 direction):
- `obligation_binding:`, `obligation_hash:` — **let go** by an `obligation_refs` pass: raised only from the window's ids/hash, which the
  code writes from refs alone (`W\window_record.py:1321-1323`); no other defect produces them on that item.
- `assertion_identity:` — **let go** by an `assertion_id` pass: raised only by the empty field (`:1191-1192`).
- `defect_location:` — **let go** by a `defect_location` pass: raised only by the empty field (`:1193-1194`).
- `semantic_sensitivity:` — **kept (refused)**: an independent defect raises the same line; letting it go would hide a probe of the
  wrong line.
- `sensitivity:`, `probe_level:`, `probe_mutation_kind:`, `probe_evidence:` — **kept**: about the probe, not the field.
- `review:`, `stale_review:`, `mechanical_green:`, `stale_run:`, `evidence:` (of a run that exists), `product:` (of a run that exists),
  `malformed_instance:` — **kept**: other facts.
Options: (a) keep `semantic_sensitivity:` refused (a probed item with a passed field then needs the `unresolved` pair, which passes it
today, E27); (b) split the kind in `acceptance.validate_window` so a comparison that fails ONLY on the passed empty field gets its own
kind `semantic_field_empty:` and list it in `tier4_gaps` — costs an `acceptance.py` change (critic gate, the census, every reader of
`semantic_sensitivity`), for a case the pair already covers. **Recommendation (a)**; N1 row (a2) pins it.

**F13 (round 2, S1 fork (b); supersedes F11) — what a `not_run` word lets go at tiers 2-4.** Per line, the side and the reason (a no-row
instance: no `outcome`, no fingerprint, `evidence_refs: []`, `W\window_record.py:1410-1413`):
- tier 2 `<iid>: outcome is missing`, `<iid>: execution_fingerprint is missing` — **let go**: the direct shape of "no run row"; nothing
  else produces them on an item the writer built in the no-run branch.
- tier 2 `<iid>: probe is missing for a new_or_changed instance` — **let go at tier 2, but MOVED, not dropped**: the same probe fact
  reappears at tier 4 as `sensitivity:<iid>`, which stays refused (below). Without the let-go the window never reaches tier 4 and the
  word could never pass the step; with it, the probe fact still needs the completion's `unresolved` pair.
- tier 3 `coverage v2 instance requires execution_fingerprint` — **let go** (§4 (3)): a run nobody made has no fingerprint, the same
  footing as handed/blocked.
- tier 4 `product:<iid>` — **let go** (30a): `outcome != passed` because there is no outcome; a red run would have a row, and then the
  no-row finding would not stand (live index, E29 shape check).
- tier 4 `evidence:<iid>` — **let go, only on the no-run shape**: raised at `W\acceptance.py:1251-1252` because `evidence_refs == []`,
  which the writer sets for an item with no run; the other `evidence:` roads (`:1254-1261`, a cited file missing or changed) need a
  non-empty list and stay refused (E29).
- tier 4 `sensitivity:`, `semantic_sensitivity:`, `probe_level:`, `probe_mutation_kind:`, `probe_evidence:` — **kept**: a probe is its
  own act (`probe_by_code` runs the test itself), so "no probe" is not a consequence of "no run row"; F11 (a).
- tier 4 `review:`, `stale_review:`, `mechanical_green:` — **kept**: the critic's word is another fact.
- `stale_run:` — not raised for such an item (no `run_identity`); if it ever is, kept. `malformed_instance:` — kept (D2c).
Options: (a) as enumerated (data: the `not_run` section of §2.2 item 4); (b) as 30a only (`product:`), leaving `evidence:` refused, so a
no-row instance ALWAYS needs the pair — the word then passes no step a pair would not pass; (c) also the probe kinds (F11 (b)).
**Recommendation (a)**.

**F14 (round 2, S1 fork (c)) — how the let-go reaches every judge of the window.** Facts: D11. A window with ONLY let-go gaps reaches
tier 4 with no pair (`finish` derives none: `_derived_pair` returns `()` when any gap is not derivable, `W\story_step.py:1682`), the
let-go empties `other_gaps`, the controller accepts — so no derivation is needed for the pure case. Two gaps remain: a MIXED window
(a let-go gap beside a derivable one) gets no derived pair while the refusal's door says `finish` derives it (FR-2), and
`window_record.run` / `driver_dispatch.Driver.window_gap` judge the window without the word (the critic is told "NOT acceptable" for an
acceptable window; the driver derives nothing for a handed instance beside a let-go gap). Both exist TODAY for 30a's `product:`.
Options: (a) N1 wires all four judges — one node, more files for a weaker model; (b) N1: the survivor `word_let_go` + the controller
(tiers 2, 4); N6: `finish`, `window_record.run`, `window_gap` read the same survivor, after N1 (same file `window_record.py`) — the rest
is a named node (rule 6: a slice is no exclusion); (c) leave the three: rejected — a dead door (FR-2) and two roads for one judgment
(P31). **Recommendation (b)**; N1 and N6 are written for it.

**F15 (round 2) — `change_basis_ref` passable?** S1: its empty value yields `change_basis:` only (`W\acceptance.py:1197-1198`) and
switches nothing off directly → pass true. Designer reading: the basis is the evidence of the disposition, and an `unchanged`
disposition switches the probe demand off (`W\proof_level.py:452-457` for a row with no `novelty` key; `W\contract.py:5727`); a passed
empty basis lets an UNSUPPORTED `unchanged` keep the probe off — the class D2c excludes. Coverage stays safe either way (`unchanged`
needs the binding's basis, `W\coverage_contract.py:603`), so the risk is the S5 window only. Options: (a) `pass: false` (the table row of
§2.2 item 4); (b) `pass: true` with `tier4_gaps: ["change_basis"]`; (c) passable only when the disposition is `new_or_changed` — a
condition in code, not a row (AR-1 cost). **Recommendation (a)** (AR-28; F7 stays (a) under it).

**F16 (round 2, Q5 not measured) — R5 for an obligation with no binding.** Facts: D13 (iii) — that state is its own S5 finding
`obligation-id-<oid>` (fact `other`). Options: (a) R5 keys on the binding only; the no-binding obligation reads as today and the report's
`other` line names the `obligation-id` pass (N3); (b) also annotate a no-binding obligation by finding the instance through the plan
row's cases — a second join for a state another word already names. **Recommendation (a)**; N2 row (c6) pins it.

## §9. Small technical choices closed by the designer
1. The reader lives in `waiver.py` (light imports).
2. `subjects` absent (not `[]`) on findings that do not set it.
3. The journal cut of `subjects` at 200; the cut tail reads as not passed.
4. The lookup returns the latest pass by `ts` (E5).
5. (fix round) Node cut: R5 moved N3 → N2 and N3 runs after N2, so every producer of a field N3 reads (`word_passed` on trace rows and
   obligations) merges before its reader (AR-22) and no two parallel nodes write one test file (B4 class).
6. (fix round) `row_fields` lives in the same table file as `facts` (one reader, AR-1/AR-13), not a second file.
7. (fix round) The tier-2 not_run filter matches whole lines by the exact forms built from `window_shape_errors`' own format
   strings and `PROBE_MISSING_ERROR` (imported, never retyped) — round 2: inside `word_let_go`, the field names from the `not_run` section.
8. (round 2) The survivor `word_let_go` lives in `window_record.py`: every judge already imports it (controller, `story_step`, `run`
   itself); `waiver.py` stays the table reader only.
9. (round 2) `controller._s5_no_row_passed` is removed, not kept as a wrapper: its one caller moves to `word_let_go` and no test calls it
   (Grep `_s5_no_row_passed` over `W\tests\` → none; same call shape for `_s5_gap_problems` → 4 files).
10. (round 2) The `not_run` let-go requires the no-run SHAPE of the item (no `outcome`, no fingerprint, `evidence_refs == []`) for every
    line, not per kind: one condition, the same for each line (E29).
11. (round 2) R5 APPENDS its words to `gap` after "; " rather than replacing it, so a more specific gap keeps first place.

## §10. Reading trail
First draft: `A\:300-419`, `:880-909`; `F19\:255-274`, `:338-437`, `:500-599`; `R30a\` whole; `S\controller.py:2251-2280`, `:2380-2470`,
`:4205-4264`, `:5560-5590`, `:5870-5920`, `:6495-6675`, `:7020-7509`; `N3\controller.py:7247-7331`; `N3\contract.py:5230-5359`;
`S\s5_precheck.py:260-279`, `:1905-1979`, `:3790-3849`, `:3900-4100`, `:4487-4536`, `:4540-4689`; `S\report_facts.py:263-352`,
`:640-880`, `:1605-1660`, `:3060-3089`, `:3130-3180`; `S\traceability.py:1081-1200`, `:1291-1450`; `S\check_delivery.py:1183-1242`,
`:1584-1718`, `:1820-2020`, `:2475-2628`; `S\acceptance.py:405-474`, `:1100-1149`; `S\window_record.py:452-482`, `:1040-1099`,
`:1200-1430`; `S\branch_accounting.py:1895-1974`; `S\coverage_contract.py:540-671`; `S\contract.py:5310-5316`, `:5440-5538`;
`references/delivery-verdict-kinds.json`; `design/architecture.md:35-46`, `:145-294`.
Fix round (all on `M\` unless marked): `CR\` whole; `M\controller.py:6997-7094`, `:7240-7409`; `S\controller.py:7340-7369` (30a, absent on
`M\`); `M\contract.py:5495-5539`; `M\acceptance.py:1052-1219`; `M\proof_level.py:467-483`; `M\check_traceability.py:95-239`;
`M\check_delivery.py:1183-1236`, `:1584-1713`; `M\ledger.py:679-723`; `M\traceability.py:1130-1154`; `M\coverage_contract.py:560-594`;
`M\report_facts.py:640-789`; `M\delivery-verdict-kinds.json:19-143`; `M\delivery_verdict.py` (Grep: required sections `:66-72`,
`kind_of_gap` `:202-205`).
Greps (each with a positive control of the same shape): `_s5_no_row_passed|word_passes|NOT_PASSABLE_TAGS|word_at` count over `M\*.py`
(no hit in `controller.py`/`s5_precheck.py`; control `def _s5_v2_collect` hits `M\controller.py:7247`); `probe is missing|new_or_changed`
in `M\contract.py` (`:5324`, `:5526`); `obligation_binding:|obligation_hash:|change_disposition:` in `M\acceptance.py`; `walk\(|
_held_thens|_partly_words` in `M\report_facts.py` (no `walk` call: report reads the trace rows of `traceability`, control
`def _held_thens` `:686`); `person_debt` over `M\*.py`; `then_bindings` producers/readers. Glob `experiments/**/*13797*/**/automation-manifest.json`
→ none (no positive control run; reported as unverified, handed to S1 Q5).
Round 2 (all on `W\`, re-reading the S1 digest's citations): `window_record.py:170-199`, `:279-303`, `:800-864`, `:1320-1420`,
`:1651-1700`, `:1748-1773`, `:1985-2083`; `acceptance.py:185-204`, `:1105-1264`; `proof_level.py:288-312`, `:390-464`;
`controller.py:7070-7114`, `:7224-7275`, `:7310-7459`; `contract.py:5296-5318`, `:5508-5527`, `:5683-5737`; `coverage_contract.py:214-269`,
`:560-659`; `manifest_put.py:1925-1949`; `s5_precheck.py:3815-3894`; `story_step.py:1619-1693`, `:2540-2572`; `driver_dispatch.py:912-964`;
`branch_accounting.py:1905-1939`; `execution_request.py:1762-1779`. Greps: `def (_s5_completion_problems|_s5_v2_collect|...)` in
`controller.py` (7 hits); `PROBE_MISSING_ERROR|def window_shape_errors|...` in `contract.py`; `DERIVED_GAP_KINDS` over `W\*.py` (story_step
+ two tests); `validate_window|derivable|DERIVED|...` in `driver_dispatch.py`; `def verdict|validate_window\(|window_shape_errors\(` in
`window_record.py`; `profile_id` -i over six window modules (no window-item reader); `.get("(defect_location|assertion_id|change_basis_ref)")`
over `W\*.py`; `def obligation_ref_problems`; `_s5_no_row_passed|_no_row_passed\(` (controller `:7354`, `:7449`; branch_accounting
`:1921`, `:1962`); `_s5_no_row_passed` over `W\tests` → none, positive control `_s5_gap_problems` over `W\tests` → 4 files; `^def \w+\(` in
`story_step.py` (`finish` `:2372`).
Not read (named where it matters): `check_bindings` body; `docs/SIBLING_MAP.md`; `test-layers.json` keep rows for the N1-N3, N6 paths
(`--witness-for` decides; a node with no keep row returns a question); the scout's `ledger`/`check_delivery`/`brief_pack`/`probe_debt`/
`case_stamp` readers of `change_disposition` (not needed: the field's row is `pass: false` on the `W\acceptance.py`/`proof_level.py`
readers alone).

## §11. Fix round (critic-on-plan `CR\`, 13.11.2026)

### Blocking
- **B1** — the no-row road. Fixed in: D3 (all three tier-2 lines and the tier-3 fingerprint line named with `M\` lines); §3 R3
  "Tier 2 — every line a not_run pass removes" (exact three line forms) and window record (ii) (the self-answered passage replaced by a
  decision); §4 rewritten — invariant (2) narrowed to "an instance passed ONLY for refs still owes its execution fingerprint", new (3)
  for `not_run`; E19 + N1 row (g2) (an instance named under both); N1 row (g) rewritten: accepted only WITH the `unresolved` pair,
  because tier 4 still yields `sensitivity:` (newly found, D3) — fork F11.
- **B2** — tier 4. Fixed in: D2b; §3 R3 "Tier 4 — one let-go" (`obligation_binding:`/`obligation_hash:` via `row_fields.tier4_gaps`,
  same index as 30a's `product:` let-go, no other kind, no unnamed instance; `passed_green` untouched, E21); N1 owns
  `Controller._s5_gap_problems` (let-go only); N1 row (a) "accepted end to end through tier 4", completion without the pair; E27 states
  that a completion WITH the pair already passes today.
- **B3** — the Then-level join. Fixed in: D8; §3 R2 rewritten (the join in `walk` after `_case_chain`, per-case, emits the gap when the
  case outcome is terminal; positional invariant (1)-(4)); rows (v5)-(v7); K7. The choice walk vs `ledger.plan_row_state` had no critic
  recommendation and carries design weight → returned as **F9** (recommended (a) walk; N2 is written for it). F4 text corrected to "a
  NEW `no`" (§8 F4 and the owner question).
- **B4** — the R1 split. Fixed in: §3 R1 (trace rows t1-t4 → N2; report rows r1-r4 → N3); N3 owns `test_report_facts.py`, N2 does not;
  N3 now runs after N2 (§9 item 5).

### Non-blocking
- **M1** — §4 block: the version test first, unchanged text; invariant (7); E25; N1 row (j). Applied.
- **M2** — E18 restated truthfully (stage-wide, undated words pass the CURRENT case-less finding; an old `*` passes a later instance);
  §2.4 names the road. Applied. F7 made conditional on F2's exclusion rows (§8 F7). Applied.
- **M3** — R2 builds the after_checks `to_check`/`how` now; row (v4) swaps the kind in a copy of the kinds file and asserts the "Left with
  you" item; K10. Applied. The refs half: D9 + fork **F10** (recommended: F4 says the refs switch is code).
- **M4** — the alias/exact-id residual is node N5 with owns, a row and an owner. Applied.
- **M5** — N1 owns `acceptance.py` conditionally (struck unless S1 names a reader); S1 Q5 measures whether a refs-absent row carries a
  binding; §3 R5 has both branches and the Lead records the answer before N2. Applied. (Round 2: the `acceptance.py` line struck — S1
  named no reader; R5 no longer has two branches — D13.)
- **F2 scout list** (CR §4) — node S1, Q1-Q5; the two fields the scout's item 2 targets are already measured (D2c) and excluded by data
  rows (§2.2 item 4); F2 confirmed as (a) with the table. Applied.
- **AR-27 note** (CR §5) — F10 (b) would change the owner of refs gaps; named in F10/F4. Applied.
- **CODE QUALITY** (CR §5) — R3 (iii) self-answered passage rewritten as a decision (§3 R3 window record (ii)). Applied.
- **Lead decisions applied:** F4 (a) — R2 kind `chain_broken`, R5 unchanged `no`, the owner question queued with corrected wording
  (the Lead's phrase "stays `no`" holds for refs and no-row, not for the unbound Then — flagged, not changed: the decision is (a));
  F8 (a) — R3/R5 as written.

### Forks returned to the Lead (each with a recommendation)
F1 (a) · F2 confirm (a) with exclusion rows · F3 (a) · F5 (b) · F6 (a) · F7 (a) conditional · **F9** (a) walk · **F10** (b) refs switch
named as code · **F11** (a) not_run does not let go `sensitivity:`/`review:`.

### Noticed, not in scope
- FV1-30a is not on origin/main (`M\`): N0/N1's base is the merged 30a; every 30a line number in this spec is `S\`'s.
- 30a's `product:` let-go also leaves `passed_green` reading the whole `gaps` list (`S\controller.py:7452`) — consistent with E21, but
  30a's spec may say otherwise; not checked.
- `story_step.py finish` may already derive an `unresolved` pair for these tier-4 gaps (S1 Q4); if so, row (a)'s "without the pair" is
  a path a person seldom takes — the let-go still removes a refusal the word named. (Round 2: refuted — it derives only for four kinds,
  D11; row (a) is the normal path.)

## §12. S1 answered (round 2, 13.11.2026)

Every S1 fact used below was re-read at its `W\` file:line by the designer (trail §10 "Round 2").

### Changes, per S1 fact
- **`REQUIRED_ROW_FIELDS` — six fields** (`W\window_record.py:178-191`); `input_hash` not among them but deleted by the same loop
  (`:1357`). → §2.2 item 4: the per-field table; four rows added to the JSON (`assertion_id`, `defect_location`, `profile_id` passable;
  `change_basis_ref` not, F15); `change_disposition` / `input_hash` rows confirmed (D2c).
- **`build` deletes empty keys, tier 2 refuses first** (`:1354-1361`; `W\controller.py:7079-7110`). → D2 cited on `W\`; R3 window
  record (i) unchanged in substance (keep `window_keys`), now with `profile_id` keeping nothing.
- **Tier-3 `continue` on bad refs** (`W\controller.py:7330-7333`). → §4 base text names it and invariant (2) states that the
  refs-passed branch makes the fingerprint check reachable (refusing side).
- **Q3 no-row tier-4 list** (`W\acceptance.py:1140-1141`, `:1207-1252`; `W\proof_level.py:295-308`). → D3 rewritten; F11 folded into
  F13 with a per-line enumeration; `evidence:` added to the let-go on the no-run shape; N1 row (g) now names `product:` and `evidence:`.
- **Q4: E27 confirmed, derivation refuted** (`W\controller.py:7451`; `W\story_step.py:1619`, `:1682`, `:2548-2571`). → E27 restated;
  D11 (with the scout's `driver_dispatch` claim corrected: `W\driver_dispatch.py:916-949` holds handed + `could_not_judge` /
  `fitted_to_code`, not the four); F14; node N6; E32, E33.
- **Q5 not measured.** → R5 rewritten (D13): keyed on the binding, words only, `verified` already False by `witnessed_binding`; N2 rows
  (c1)-(c7) on constructed fixtures; F16. Plus a defect found while re-reading: `obligation_ref_problems([]) == []` (D12) → E31.
- **The `row-fields-missing` producer is at `W\s5_precheck.py:3834`** (the spec cited `:3842` from `S\`). → §2.1/§2.2 cite both; N0's
  owns line not edited (noticed below).
- **New fact, not in the digest:** the probe block copies the item's row fields after the deletion loop (`W\window_record.py:822-857`,
  D10), so kept `""` values can raise `semantic_sensitivity:` → F12, E28, E34, N1 row (a2).
- **R3 rewritten to one survivor** (`window_record.word_let_go`, §2.2 item 6): tier 2 and tier 4 call it; 30a's `product:` let-go
  migrates into it (data: the `not_run` section); `_s5_no_row_passed` removed (K9, §9 item 9); `Controller._s5_word_index` new.
- **N1 re-checked:** owns updated to 4d0ad66 lines; `acceptance.py` struck; `waiver.py` (`not_run_lets_go`) and `test_words_doors.py`
  rows added (after N0); rows (a2), (g3), (i2), (l)-(n) added; **READY FOR DISPATCH once N0 is merged.**
- **N2 re-checked:** R5 rows replaced by (c1)-(c7); owns `coverage_contract.py` narrowed to the words branch; non-goals added;
  **READY FOR DISPATCH once N0 is merged.**
- **N6 new** (F14 (b)): queued after N1.

### Forks returned (each with a recommendation)
- **F12** (S1 (a)) `semantic_sensitivity:` — keep refused; per-kind sides enumerated in §8. Recommendation (a).
- **F13** (S1 (b); supersedes F11) — a `not_run` word lets go the two shape lines, the probe-missing shape line (moved to tier-4
  `sensitivity:`, which stays), the tier-3 fingerprint line, `product:` and `evidence:` (no-run shape only); keeps every probe and review
  kind. Recommendation (a).
- **F14** (S1 (c)) — one survivor; N1 wires the controller, N6 wires `finish`, `window_record.run`, `driver_dispatch`. Recommendation (b).
- **F15** — `change_basis_ref` not passable (against the scout's "true"). Recommendation (a).
- **F16** — R5 keys on the binding only. Recommendation (a).
- Still open from round 1: F1, F2, F3, F5, F6, F7, F9, F10 (recommendations unchanged; F6 and F7 re-checked against round 2).

### Noticed (not in scope; N0 untouched)
- N0's owns line cites `check_row_fields` "at `:3842`"; at 4d0ad66 the `_finding(...)` call is `W\s5_precheck.py:3834`. The builder
  locates by function, so nothing blocks; the Lead may correct the number at N0's acceptance.
- N0's table lands without the `not_run` section and the four new `row_fields` rows; N1 adds them in the same commit as their readers
  (E30: in the world between, a `not_run` word lets nothing go through the table — but N0 does not yet migrate 30a's `product:` let-go,
  so nothing regresses before N1).
- The mixed-window dead door (D11, E32) and `window_record.run`'s "NOT acceptable" for a word-passed window (E33) exist TODAY for 30a's
  `product:` let-go — N6 closes both for 30a and 30b at once.
- `branch_accounting._no_row_passed` is about the UNBOUND THEN (`no-bindings`/`unbound-<n>`, `W\branch_accounting.py:1921-1933`), not
  about "no run row" as its name suggests; N1 migrates it to `index.then(case, then)`; the name is left as is (renaming is out of scope).
