# Critic on the plan — FV1-30b (word fact downstream), draft t-542

Plan: `docs/tasks/specs/20261113-fv1-30b-word-fact-downstream-spec.md`. Judged together with the Lead's provisional fork decisions
(F1 a, F2 a + scout, F3 a, F4 a-now, F5 b, F6 a, F7 a). Trees: `S\` = fv130a worktree, `N3\` = fv119-n3 worktree (read-only).

**Verdict: fit_with_fixes. 4 blocking spec edits (B1-B4), 5 non-blocking (M1-M5).** Each fix is a spec text edit; none needs a new fork
from the owner except the one F4 already sends her.

## (1) Reading facts D1-D7 — checked by trail

| D | result | my trail |
|---|---|---|
| D1 | holds | Grep -i `person_passes\|_word_passed_gap\|word_passed\|word_at` over `S\scripts\*.py`: only `word_passed_pairs`, local `word_passed` (`branch_accounting.py:1950-1962`, `controller.py:7448`), `word_at` (`controller.py:2415-2419`); the same call found `word_passed_pairs` (control). `awaits_answer` absent; control `NOT_PASSABLE_TAGS` hits `s5_precheck.py:3931` |
| D2 | holds | `window_record.py:1346-1350` deletes empty refs/ids/hash/text fields; `contract.py:5310-5313` requires them; `:5514-5519` "is missing"; `controller.py:7079-7110` reads no word |
| D3 | holds, and is worse than stated (B1) | `window_record.py:471-473` exact id; `:1399-1402` no outcome/fingerprint; `s5_precheck.py:1948-1950` aliases |
| D4 | holds | `s5_precheck.py:4487-4512` (S5 plan); `controller.py:4212-4225` → `_case_rows` `:2456-2466` → `_plan_document` `:2251-2258` (test-plan.json); `A\:404` vs `A\:887` contradict |
| D5 | holds | `acceptance.py:429-433` reads only `blocked_by_env` rows |
| D6 | holds | `N3\controller.py:7289` `_tier3_call(self._plan_document)` before the loop |
| D7 | holds | `coverage_contract.py:568-583` joins via `obligation_bindings` |

## (2) The positional invariant of §4

The invariant is stated (§4 (1)-(5)) and the position keeps (1), (3), (4), (5) for the refs case. Two defects:

- **B1 (blocking) — the no-row road stays unreachable, and §4 (2) contradicts N1 row (g).** F2's recommended tier-2 branch drops
  only the `outcome` and `execution_fingerprint` lines. But (i) the same shape step also emits `"<iid>: probe is missing ..."` for any
  item with `change_disposition == "new_or_changed"`, an outcome that is not handed, blocked or pending, and no `probe`
  (`contract.py:5526-5528`). A no-row new test has no outcome and no probe, so tier 2 still stops. (ii) Tier 3 then refuses
  `"coverage v2 instance requires execution_fingerprint"` (`N3\controller.py:7313-7316`), and §4 (2) keeps that refusal on purpose.
  N1 row (g) ("accepted") cannot pass. Fix: in §3 R3 (iii), §4 and F2, list every line the not_run pass removes for a named
  instance (tier 2: outcome, fingerprint, probe-missing; tier 3: fingerprint). Narrow §4 (2) to "an instance passed only for refs
  still owes its fingerprint". Add a row: a named not_run instance that is also a refs-passed instance.
- **B2 (blocking) — N1 row (a) "the completion is accepted" is false through tier 4.** `validate_window` emits
  `obligation_binding:<iid>` and `obligation_hash:<iid>` for a schema-2 item with empty `obligation_ids`/`obligation_hash`
  (`acceptance.py:1181-1190`). They fall into `other_gaps` and refuse as `"unresolved window: ..."` (`S\controller.py:7450-7451`)
  unless the completion carries `unresolved` + `reason`. N1's owns exclude `_s5_gap_problems`. Fix: N1 owns one more let-go in
  `_s5_gap_problems`, beside 30a's `product:` let-go and through the same index: the `obligation_binding:`/`obligation_hash:` gaps
  of an instance named under `row_fields_unestablished` with `obligation_refs` in `fields`. Row (a) runs end to end through tier
  4. Invariant: no other gap kind and no unnamed instance is let go.
- M1: the `continue` branch also skips the `schema_version != 2` part of the `:7302` test for a named instance. State that it stays:
  check the version first, then branch.

## (3) Error direction of `word_passes` in a gate role (§2.4)

The adversarial list is good, and every input on it stays on the refusing side: `_names` matches by equality only
(`s5_precheck.py:3940-3955`), and a revoked or blank word is no word (`:3990-3991`). Two wrong-pass roads are missing:

- **Stage-wide words, current subjects.** `*` and a tag word are not tied to a window or a time. The live words are
  `live_stage_overrides(pipeline, ("S5",))`, and a finding with no `pair_at` has no time rule (`:3998-4000`). The `subjects` are
  those of the finding as it stands at the finish, not as the person saw it. So E18's invariant ("a word about window A's instance
  never passes window B's instance") is false for `*` and for the tag `row-fields-missing`. This is inherited from A's decided
  semantics (`A\:348`), so it is M2, not blocking: restate E18 truthfully ("the word passes the CURRENT case-less finding; its
  subjects decide per instance").
- **F2 (a) widens a refs word into a probe waiver.** If `change_disposition` is kept empty, the probe-missing line needs
  `== "new_or_changed"` and goes silent (`contract.py:5526`). `validate_window` gives `change_disposition:<iid>`
  (`acceptance.py:1195-1196`) instead of a probe gap. That gap passes whenever the completion carries `unresolved` + `reason`
  (`controller.py:7450`). A word about "row fields not given" then drops a sensitivity proof nobody named. This is exactly the
  "passes more than the person named" class. It goes on the scout list under F2 below and makes F7 (a) conditional.

## (4) Forks — the Lead's decisions

- **F1 (a): holds.** The `known_red: FV1-30` labels need a closing node.
- **F2 (a): holds as the direction (P31: one finding, one pass).** N1 cannot be cut before a scout answers: (1) for each of
  `assertion_id`, `defect_location`, `change_disposition`, `change_basis_ref`, `obligation_ids`, `obligation_hash`, `input_hash`:
  every reader of the EMPTY value in `window_shape_errors`, `_s5_collect` / `_s5_v2_collect`, `validate_window` (`:1180-1198` and
  the probe chain `:1199-1215`), `proof_level.proof_required`, novelty / `run_freshness_of`, and S7/S8 readers of the window, each
  with the gap it emits; (2) which of these empty values switches OFF a different requirement (the probe through
  `change_disposition`, as above); the plan must forbid that: such a field is never passed by this word, or passing it still owes
  the probe; (3) for a no-row instance, every line of tiers 2-4 it hits (B1); (4) whether the tier-4 `unresolved` + `reason` pair
  already lets these gaps through today: if it does, the word adds nothing at tier 4 and the plan should say so. If the scout finds
  a field whose empty value disables another check, F2 (a) must exclude that field by a data row of `word-passed-facts.json`, not
  by code.
- **F3 (a): holds.** The record is what was accepted; a live re-run at S8 costs a whole precheck and can show passes nobody gave.
- **F4 (a) now: holds as an owner question.** One correction: the premise "the verdict STAYS `no`" is wrong for the unbound Then
  (B3). Today such a Then is silent, so (a) is a NEW `no`; say so in F4 and in the owner question. **Is the switch one data row?**
  For the Then, yes: `trace_gaps["word_passed:then_unbound"]` goes from `"chain_broken"` to `"unconfirmed_expectation"`. That holds
  only if N2 also builds the `after_checks` branch now, because `traceability_records` attaches `to_check` only for `question_open`
  (`check_delivery.py:1223-1230`) and puts a `no` kind in the text branch (`:1231-1234`). Add an N2 row that swaps the kind in a
  copy of the kinds file and asserts the "Left with you" item (M3). For refs, NO: the coverage verdict is built from strings
  (`coverage:` / `coverage red:`, `check_delivery.py:1692-1711`); only `verified` and `person_debt` exempt an obligation, and the
  kinds file is not read there. Fix (part of B3's edit to §3 R5 / N3): R5 emits a typed field that a kinds-file row decides (for
  example `word_passed: true` read through a `coverage_gaps` row). Otherwise F4 must say that switching refs to (b) is a code change.
- **F5 (b): holds.** The finish does not read `work/s5-plan.json` (the plan's §3 R6 trail is consistent with D4).
- **F6 (a): holds.** No reader below S5 reads window refs (D7). `validate_window` reads only ids and hash, which B2 covers.
- **F7 (a): holds only with F2 limited to refs.** If F2 (a) widens to `change_disposition` or other proof-bearing fields, an old
  `*` passes those fields on instances added after the word. Then (b), dating by plan approval, or excluding those fields (see F2)
  is needed. State the condition in F7.

## (5) AR / P / FR

- AR-13: kept. One reader (`word_passed_index`); the two tag parses (`controller.py:7362-7365`, `branch_accounting.py:1929-1931`,
  read) migrate.
- AR-24: kept (whole word by `word_at`, E10).
- AR-28: at risk through F2's `change_disposition` road (§3). Otherwise kept: every reader has an unreadable branch toward refusal.
- AR-29 / JUDGMENT: no judgment moves. Every join is by id, tag, case or Then, and K1-K8 are data and xref. "None found" on
  role-wording reads.
- AR-27: refs gaps are owned by `coverage:` = factory today; F4 (b) would change the owner, so name it there.
- AR-1: the table is data, kept.
- P13/P21/P22: kept by A3-E1 "step not fact".
- FR-7: E16, kept.
- **P31 / ONE ROAD:** F2 (a) is the one-road choice, and `unmatched-` stays out of the table (a data row, with the 30a critic's
  reason). I found no road that a language or project takes differently (`check_bindings`, `check_run_mapping` and `_names` read no
  language). Residual of the class: the alias/exact-id split (D3), queued in §7 without a node id (M4: give it a node or a pile
  line with an owner).
- DUPLICATION: none found. Grep -i `passed-by-person` over `S\scripts\*.py` hits 10 files: the writer (`controller.py`), tests, and
  two text mentions (`s5_precheck.py:4043`, `refusal_registry.py:858`). No package reader exists, so `person_passes` will be the only
  one (agrees with `A\:889`).
- CODE QUALITY: §3 R3 (iii) contains a self-answered "recommended `not_run`? No:" passage. Rewrite it as a decision.

## (6) Node cut

- N0 → (N1 ∥ N2 ∥ N3): the source files are disjoint (controller functions split N0 `_record_*` / N1 `_s5_*`, D-0048 form).
- **B3 (blocking) — N2 R2 has no carrier.** `check_traceability.walk` is case-level: `_case_chain` runs per case (`:211-218`), and
  the file holds no `then_bindings`, `then_outcome` or traceability import (Grep -i, zero hits; control `def walk` hits `:161`). A
  `gap_word` on a `traceability.py` row has no reader there. A case whose other Then ran green reaches a terminal outcome, so
  `traceability_records` skips the requirement (`check_delivery.py:1199`). Fix: N2 names the Then-level join (in `walk`: the
  case's `then_bindings` plus `.then(case, n)` from the record index, which emits the gap even when the case outcome is
  terminal), or names `ledger.plan_row_state`. `A\:883` lists that reader, and the draft drops it. A weaker model cannot pick
  between the two.
- **B4 (blocking) — the R1 split crosses nodes.** R1's report half (`_held_thens`, `_partly_words`, `report_facts.py`) is N3's file,
  but its rows sit under N2. Both nodes would write `test_report_facts.py` in parallel. Fix: R1 (a)-(d) report rows go to N3; N2
  keeps the trace-table and delivery rows only.
- M5: N1's owns lack `acceptance.py` if the F2 scout returns a tier-4 field reader to change. R5 rests on an obligation whose refs
  are absent still having a binding (`coverage_contract.py:578-582`). That holds only if the binding is written apart from the refs
  (rule 13: measure it on a real manifest). Add to N3: "establish on a TP1-13797 manifest whether a refs-absent row carries a
  binding; if not, R5's annotation goes on the binding-less obligation".
- Weaker-model test (п. 11): N0 and N3 are executable. N1 and N2 are not, until B1-B3 are edited. `check_bindings` and `walk` are
  still unread by the designer, and the builder is told to "return a question": acceptable for `check_bindings`, not for `walk`,
  which carries a design choice (B3).

## Trail

Read: plan whole; `A\:296-420`, `:880-900`; `F19\:505-592`; `S\controller.py:2248-2261`, `:2389-2440`, `:4205-4229`,
`:7025-7123`, `:7224-7275`, `:7340-7462`; `N3\controller.py:7240-7334`; `S\window_record.py:452-483`, `:1330-1409`;
`S\contract.py:5300-5324`, `:5490-5529`; `S\s5_precheck.py:1930-1977`, `:3820-3843`, `:3938-4056`, `:4484-4515`;
`S\acceptance.py:410-439`, `:1052-1215`; `S\coverage_contract.py:560-589`; `S\check_delivery.py:1183-1236`, `:1685-1712`;
`S\check_traceability.py:100-234`; `S\traceability.py:1136-1151`, `:1290-1305`; `S\branch_accounting.py:1918-1965`;
`S\ledger.py:679-709`; `S\delivery_verdict.py:202-222`; `S\references\delivery-verdict-kinds.json` whole; critic-diff-brief
q11-12. Greps (each with a control of the same shape): D1 pair; `then_bindings|then_outcome|import traceability` in
check_traceability (0; control `def walk|def _case_chain` 2); `_case_rows|_plan_document()` call sites; `dispositions|change_disposition`
in acceptance; `passed-by-person` over scripts (10 files, read the two non-test, non-writer hits). No reruns (plan gate: no code).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1 no-row road unreachable: tier-2 probe-missing line (contract.py:5526-5528) and tier-3 fingerprint (N3 controller.py:7313-7316) still refuse; section 4 invariant (2) contradicts N1 row (g)",
    "B2 tier 4 validate_window emits obligation_binding/obligation_hash gaps for empty ids/hash (acceptance.py:1181-1190), refused at controller.py:7450; N1 excludes _s5_gap_problems so N1 row (a) cannot be accepted",
    "B3 N2 R2 has no carrier: check_traceability.walk is case-level (_case_chain, :211-218), reads no then_bindings; the Then-level join (walk or ledger.plan_row_state, A:883) must be named",
    "B4 R1 report rows (report_facts _held_thens/_partly_words) listed under N2 while report_facts.py is N3's; parallel writes to test_report_facts.py"
  ],
  "fixes": [
    "Section 3 R3(iii), section 4, F2: list every tier 2-3 line a not_run pass removes (outcome, fingerprint, probe-missing; tier-3 fingerprint); narrow invariant (2) to refs-only passes; add a row (blocking)",
    "Section 6 N1 owns + row (a): one let-go in _s5_gap_problems for obligation_binding:/obligation_hash: of an index-named refs instance, same index, no other kind; row (a) end to end through tier 4 (blocking)",
    "Section 3 R2 / N2: name the Then-level join in check_traceability.walk or ledger.plan_row_state; F4 text: (a) is a NEW no, not 'stays no' (blocking)",
    "Section 6: move R1 report rows to N3; N2 keeps trace/delivery rows (blocking)",
    "F2: scout questions (empty-value readers per field; fields whose emptiness disables another check such as the probe via change_disposition; no-row lines tiers 2-4; whether the unresolved pair already passes tier 4) answered before N1; a field that disables a check is excluded by a data row",
    "F4 / N2: build the after_checks branch with to_check/how now, plus a row swapping the kind in a copy of the kinds file; R5 refs gap gets a typed field decided by a kinds-file row, or F4 says the refs switch is code",
    "E18 restated: stage-wide words pass the current case-less finding; F7 (a) conditional on F2 staying refs-only",
    "Section 4: keep the schema_version check before the named-instance branch; N3: measure whether a refs-absent row carries an obligation binding (rule 13); section 7 alias/exact-id residual gets a node id and owner; R3(iii) self-answered passage rewritten"
  ],
  "class_completeness": "Readers of the four facts walked against A:394-404 and A:880-889: ledger.plan_row_state (A:883) is omitted from the draft (B3); the tier-4 validate_window gap kinds for empty window fields are an unwalked sibling of D2 (B2); alias vs exact-id split queued without a node (section 7). SIBLING_MAP axis row for word_passed_index is in N0 owns; axes 17/26/29/34 not re-walked by me (map not opened: plan gate scope).",
  "trail": {
    "read": [
      "docs/tasks/specs/20261113-fv1-30b-word-fact-downstream-spec.md",
      "docs/tasks/specs/20261113-p1-specs-amendment-owner-words.md:296-420,880-900",
      "docs/tasks/specs/20261113-fv1-19-obligation-refs-spec.md:505-592",
      "fv130a controller.py:2248-2261,2389-2440,4205-4229,7025-7123,7224-7275,7340-7462",
      "fv119-n3 controller.py:7240-7334",
      "fv130a window_record.py:452-483,1330-1409",
      "fv130a contract.py:5300-5324,5490-5529",
      "fv130a s5_precheck.py:1930-1977,3820-3843,3938-4056,4484-4515",
      "fv130a acceptance.py:410-439,1052-1215",
      "fv130a coverage_contract.py:560-589",
      "fv130a check_delivery.py:1183-1236,1685-1712",
      "fv130a check_traceability.py:100-234",
      "fv130a traceability.py:1136-1151,1290-1305",
      "fv130a branch_accounting.py:1918-1965",
      "fv130a ledger.py:679-709",
      "fv130a delivery_verdict.py:202-222",
      "fv130a references/delivery-verdict-kinds.json",
      "docs/tasks/critic-diff-brief.md:67-90"
    ],
    "reruns": []
  }
}
```
