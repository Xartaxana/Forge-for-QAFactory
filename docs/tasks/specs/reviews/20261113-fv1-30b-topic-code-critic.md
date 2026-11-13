# FV1-30b topic code critic — N0 (82c00a0) + N1 (5e7fa3f) + N2 (dc8edef), one pass

Verdict: **fit_with_fixes** (NEEDS WORK). 0 blockers. No unknown becomes a pass anywhere I traced (AR-28 / FR-59 hold). The fixes
are a false refusal the spec's own §4 pseudo-code carries, a cross-match in the coverage words, one duplicated composition at 8
sites, a gate-B text that loses the word, and smaller items. The verdict is an input to acceptance; acceptance and the F6 reading
are the Lead's.

## Findings (numbered; severity; owner = the fresh fix worker of the node named)

**F1. §4 / F6 (a): a refs-passed instance WITH a fingerprint and stale/unknown refs is still refused** — `fv130b-n1 controller.py:7352`
(`refs_bad` = shape only) and `:7363` (`if refs_bad or no_fp:`). Trace: item with a fingerprint, refs a non-empty list with a stale
hash → `ref_kinds={"stale"}`, `refs_bad` False, `no_fp` False → index never asked → `:7386` refuses
"instance obligation_refs ... stale". `row_field_gaps` reports stale/unknown under `obligation_refs` (`window_record.py:279-303`
docstring), so the person was shown that field and passed it, and the finish refuses anyway. The same stale refs on a `not_run`
instance ARE let go (index asked because `no_fp`). Direction: refusing (FR-7 repeat, P13 not honoured), **not** an AR-28 blocker. It is a
spec defect: the §4 block prescribes exactly this condition (builder deviation 5 says so). Fix (N1 fix worker, after the Lead confirms F6 (a)
covers stale/unknown): ask the index when `refs_bad or ref_kinds or no_fp`; row: refs-passed + fingerprint + stale ref → no refusal; same
unnamed → today's stale text. With it, `window_record.build` choice 1 (`:1433-1455`, no `passed_by_word` when the keys are non-empty)
is wrong too: the LIVE index names a field only while its finding stands, so a stale-refs pass gets no `passed_by_word`. Write the entry
for every passed field; keep the keys only for the empty ones.

**F2. Coverage words cross-match another case's test row** — `fv130b-n2 coverage_contract.py:587`
`next(t for t in tests if aliases & set(C.instance_id_aliases(t)))`. Measured (probe, trail): for iid `TC-1::test_x`, with
manifest `[TC-2::test_x, TC-1::test_x]`, it picks **TC-2::test_x**, because both carry the bare alias `test_x`. The index itself
says `_same_instance("TC-1::test_x","TC-2::test_x") == False`. Effect: the words follow the refs of the wrong row. A repaired TC-1 can
show "not established" (E8 broken), or a bad TC-1 shows nothing. This is text only: `verified` is not touched. Fix before merge (N2 fix
worker): match on `waiver._same_instance(iid, C.test_instance_id(t))` (make it public, e.g. `waiver.same_instance`); add a row
with two cases sharing a function name.

**F3. One composition, 8 copies, three sentinels; up to 4 full precheck runs per finish** (Q5; brief item 6) — live
`waiver.word_passed_index(s5_precheck.word_passes(...))`: `controller.py:7395` `_s5_word_index`, `window_record.py:1307` `live_index`,
`branch_accounting.py:1917`. Record `waiver.word_passed_index(waiver.person_passes(x)[0])`: `check_traceability.py:164`,
`check_delivery.py:1609` (returns False), `check_delivery.py:1194` (inline), `coverage_contract.py:560` (False), `traceability.py:1160`
(None). N3 adds one and N6 three, which makes 12. Cost: `word_passes` runs the whole `run(..., judges=False)` precheck whenever a live S5
word stands (`s5_precheck.py:4052-4054`). Tier 2 (`:7098`), tier 3 (`:7363`) and tier 4 (`:7489`) each build it, and so do `build` and
`_record_s5_word_passes`, all on one accepted completion. **Fix NOW in this topic, before N3/N6 write their sites.** Survivors:
`s5_precheck.live_word_index(task_root, scope=None, dispatch_id=None) -> WordPasses|None` beside `word_passes`, and
`waiver.record_word_index(task_root) -> WordPasses|None` beside `person_passes`. Both never raise; None means names nobody. Migrate the 8
sites. `Controller._s5_word_index` memoises per `_s5_completion_problems` call. Owner: ONE fresh fix worker on the merged N0+N1+N2 tree.
Its owns: `s5_precheck.py` (new function), `waiver.py` (new function), the 8 functions above and their keep rows.

**F4. Gate B loses the word under F4 (a) (E16)** — `fv130b-n2 check_delivery.py:1222` cuts `row['detail']` at 120 characters. The walk
appends the word mention at the END of the case detail (`check_traceability.py:255-256`), and the `no` record has no ts at all. The
`how` with the ts exists only in the after_checks branch, which F4 (a) makes unreachable. So in the v5 case (a green case detail first)
the person reads a reason cut before "passed by the person's word", which is E16's own text. Fix before merge (N2 fix worker): when a gap
is `word_passed:then_unbound`, add "; Then <n> of <case>: passed by your word at S5 (<ts>)" outside the 120-character cut. Row: v5 text
names the word and the ts.

**F5. A third finding-id splitter whose docstring claims to be the only one** — `fv130b-n1 waiver.py:791-793` ("The ONE place the id is
taken apart"). Others: `s5_precheck.py:4111` `_finding_tag`, `exit_gate.py:1775` `_finding_tag_of`. Fix (topic fix worker of F3,
low): make `_finding_tag` delegate (lazy import, as `s5_precheck.py:3986` already does), or correct the docstring and queue `exit_gate`.

**F6. `build` new block: nesting 5 levels, the table re-read per item, a field literal in code** — `window_record.py:1433-1455`
(`for item` → `if empty_fields` → `if passed` → `for field` → `if`). `_row_fields()` is re-read per item (`:1440`). `k != "input_hash"`
(`:1444`) is a field exclusion in code (spec AR-1 row: "a field's exclusion is a row, never code"; the `input_hash` row already says
`pass: false`). The table's `window_keys` VALUES are never read: the item's own empty value is kept. Fix before merge, low (F3 worker,
same file, `build` only): extract `_word_kept_keys(item, identity, empty_fields, index, table)`, read the table once per `build`, drop
the literal, and make `window_keys` a list or use its values.

**F7. `passed_by_word` on a window INSTANCE: no reader, and the name collides** (AR-22, Q8) — producer `window_record.py:1452`, `:1518`.
Readers: none in N1/N2. The N3 spec reads trace rows, ledger text and obligations; the N6 spec reads `word_let_go`, not this key. The
same key already exists with another shape and meaning on `expectation_changes[]` (bool: `window_record.py:1105`, readers
`acceptance.py:283`, `window_record.py:1780`, `report_facts.py:1647`). N2 names the same idea `word_passed` (trace row, obligation).
Today no reader is misled: all three bool readers iterate `expectation_changes`. Fix before N6 (N1 fix worker): rename it to
`word_passed` (list) so one name means one thing per carrier. The Lead names its reader (recommend N6 `window_record.run`: print the
item's entries as the "passed by the person's word" note) or drops it.

**F8. Left-with-you under (b) is not one data row** (N2 deviation 2; spec R2 v4 / M3) — `build_left_items` rewrites `to_check` of
an `unconfirmed_expectation` item. Under F4 (a) this cannot be reached. Lead node: amend F4's sentence ("one row + one
`build_left_items` branch") or open a node.

**F9. `references/word-passed-facts.json` is in no keep row's `covers`** (Q8; N0 report line 111). `--witness-for` names only the
scenario layer. Not a blocker: `test_words_doors.py` (keep, detector) runs in the canon. Lead node: add it to the `covers` of
`test_words_doors.py` and `test_window_record.py` in `scripts/tests/test-layers.json`.

**F10. Tests: budget and one data pin** (Q9). N1 adds about 435 test lines against about 259 product lines, and N2 about 245 against
about 205 (`git show --stat`). Neither report names a reason (TESTING.md «Бюджет»). `test_words_doors.py`
`row_fv130b_n1_the_not_run_section_and_the_field_rows` also pins the SHIPPED table's values ("the shipped `not_run` section is the spec's").
That is a data pin, and rows (g)/(l) already prove the behaviour. Queue (low): drop the two shipped-value checks; add a reason line to
each report.

## Topic questions

1. **AR-13/AR-15.** On N1 the case-insensitive grep finds no non-test reader of a tag. What remains: the producers' own tags
(`s5_precheck.py:1282`, `:1966`), the writer (`controller.py:2402`), docstrings (`branch_accounting.py:1924`, `s5_precheck.py:4046`) and
refusal text (`refusal_registry.py:858`). The two benign hits are verified. Positive control at 4d0ad66, same pattern:
`branch_accounting.py:1931`, `controller.py:7365`, `:7448`, `:7450`. `word_let_go` is the one let-go predicate for tiers 2/4.
`_s5_v2_collect` asks the index directly, which the spec sanctions (§4). The readers are one class, but the composition is
duplicated: F3.
2. **§4.** Invariants (1)-(7) are preserved: the version test comes first (`:7347`); unnamed instances get the same order and texts;
refs-only still owes the fingerprint; `not_run` owes none and still goes through refs/ids/hash; the lazy single build; None names
nobody. Deviation 5 is a spec defect against F6 (a). It errs toward REFUSAL, so it is not an AR-28/FR-59 blocker: F1.
3. **Stub.** `test_probe_gap_door.py:122` delegates to the real `_s5_word_index` with the stub's `store.root`. There is no live S5 word
under that root, so the index is empty and nothing changes. The edit is correct and minimal, and it uses the file's own `_noted`
pattern. The unbound-method coupling predates this topic and is not hidden by the stub. The file is keep `data_join`, not quarantined.
The Lead adds it retroactively to N1's owns.
4. **Fixtures.** Row 30a still proves "the other instance is still refused", "another finding lets nothing go" and "a raising reader lets
nothing go", and it gains E4. Row (k) still proves "a field with no row misses". The `build` choices: no notes line for a kept key —
right (the key exists, so tier 2 has nothing to explain). `profile_id` beside a standing field — acceptable but asymmetric (only when
some field is empty). Choice "keys no longer empty → no entry" — wrong: F1.
5. Fix now, not N6's: F3 (survivor homes named there).
6. **AR-29.** No judgment moved. All of these are xref by id/kind/Then number: K2 `word_passed_index`, K3 `_s5_v2_collect` branch, K5/K6/K11
`word_let_go`, K9 `_no_row_passed` → `index.then`, K7 walk join. `_no_run_shape` is shape; `not_run_lets_go` / `row_fields` are data
readers, not checks; K1, K4, K8, K10 are copies/texts. The census reads 24/24 in every report, and no row was raised.
7. **FR-10/FR-35.** The trace row says `not run` with "passed by the person's word". The kind stays `chain_broken`/`not_executed` (`no`).
`verified`/`person_debt` are untouched. Nothing reads as verified. One temporal FR-10 gap: between the N2 merge and N3, `report_facts`
still reads the requirement `proven` beside a `not run` row (`report_facts.py:659-662`) while delivery now says `no`. N3 must land before
any release that carries N2 (Lead sequencing note). E16 text: F4.
8. **AR-22.** `subjects`: producer → copy → line → `person_passes` → index, all in N0. `passed_by_word` (instance): F7.
`word_passed`/`then`: read by N3 (named). The missing keep row is a Lead node (F9), not a blocker.
9. **Tests.** Every N1 row (a)-(n) and N2 row (t1-t4, v1-v7, R4, c1-c7) has a named check with a case-naming red id. §4 (4) is not
pinned: that is not a finding. No source pins: the grep of the added test lines for `read_text(`/`getsource`/glob finds only JSON
fixtures. Budget and data pin: F10.
10. **Axis 37.** The row is right in substance, but not complete, and N0 never committed it (the spec wanted it in N0's commit). The Lead
places it with these additions: the two survivors of F3; known roads `controller._passed_by_person`/`exit_gate.judge_words` text road
(spec §7), N5 alias split, `build_left_items` (F8), the three splitters (F5); N2's detectors (`test_then_remainder`
`fv1_30b_n2_trace_and_verdict`, `test_obligation_join` `fv1_30b_n2_refs_words`, `test_check_delivery` `fv1_30b_n2_no_run_row_names_the_word`).
Map siblings outside the diff: Axis 29 — `controller._record_person_pass` (`controller.py:2402-2433`, a plain `open("a")` jsonl appender,
extended by N0) is in neither the adopters nor the queued list → `<adopt hooklib.append_jsonl_line in _record_person_pass> | перенос:
pile fv1 untaken batch | обоснование: pre-existing 30a writer, outside these owns | подтвердил: —`. Axis 23 — the `row_fields` table is
now a per-field list over `REQUIRED_ROW_FIELDS` (all 6 have rows today, measured) → a new required field needs a row decision: add a
cross-reference line to Axis 23.

## Standing questions

- Fit to spec: met except F1 (spec defect), F4 (E16), F8 (v4). Builder decisions: F1/F7 against, the rest safe.
- Seams: N1 ∥ N2 merge clean (`git merge-tree` exit 0, no shared file). Same reader used two ways: live (no `ts`) vs record, which is
F3 as designed; no semantic clash.
- DUPLICATION AND CONSISTENCY: F3, F5, F7, F2 (a second instance matcher). Searched for: compositions (`word_passed_index(`,
`person_passes(`), finding-id splitters (`split(":", 2)`), instance matchers (`def same_instance|_same_instance`), key `passed_by_word`.
- CODE QUALITY: F6 (blocks nothing; fix before merge); `word_let_go` 48 lines, fine; `person_passes` about 60 lines, at the edge.
- Hygiene: `selftest --lang` green in all three reports; no Cyrillic in the diffs' package files.
- Ratchets (item 9): no in-tree ratchet row added or raised (census 24/24).
- Architecture: AR-1, 13, 15, 22, 28, 29 named. AR-22 has a gap (F7). AR-1 is broken in letter at `window_record.py:1444` (F6).
- Judgment: none moved (Q6).
- ONE ROAD (P31): none found. Searched for language/project/runner names in the three diffs' product lines: no branch on any. Every fact
takes one road through the table.
- Process note: N1 ran slow files locally (`test_controller_state`, `test_window_record`, `test_branch_accounting`), which PROJECT.md p. 2
forbids. That is a calibration item, not a code finding.

## May N3 and N6 start before the fixes?

N3 and N6 may start on merged N0+N1+N2 **once F3's two survivors exist** (one small commit, first in the fix worker's order). Their
dispatches must name `waiver.record_word_index` / `s5_precheck.live_word_index`, and N6's must name the F7 rename. Otherwise each adds
copies and the fix has to chase them. F1, F2, F4, F5 and F6 touch other functions, so they may run in parallel with N3/N6. Function
lists: `window_record.build` for the fix vs `run` for N6 (D-0048).

## Trail

Read: `docs/tasks/critic-diff-brief.md`; spec lines 1-739 (§0-§8, N0/N1/N2/N3/N5/N6 blocks, E1-E34); the three reports;
`git show` 82c00a0 / 5e7fa3f / dc8edef (product and test diffs); `contract.py:3563-3570, 4064-4095, 5683-5739`;
`acceptance.py:262-289`; `window_record.py:279-303, 1770-1787`; `coverage_contract.py:598-712`; `check_delivery.py:1204-1260, 1418-1437,
1746-1777`; `check_traceability.py:236-285`; `traceability.py:1095-1160`; `ledger.py:1585-1614`; `s5_precheck.py:4041-4058, 4111`;
`branch_accounting.py:1829-1831, 1907-1968`; `controller.py:2389-2452` (at 5e7fa3f); `test-layers.json` keep rows; SIBLING_MAP axes
23, 25-30 (read-main) and axis headings (root, read-main, origin/main: 37 free); TESTING.md 60-139.

Reruns and probes:
- `( cd fv130b-n2/ai-packages/qa-factory && python -B scripts/tests/test_then_remainder.py )` → `=== test_then_remainder: 315/315 ok ===` (= N2 report).
- Lead's control run at 5e7fa3f `test_words_doors 702/702` taken as given (= N1 report).
- `git merge-tree --write-tree 5e7fa3f dc8edef` → exit 0; `comm` of changed paths → empty.
- AR-13 grep (`grep -rniE` over each worktree's scripts, tests excluded) with positive control `git grep` at 4d0ad66: output in Q1.
- F2 probe (python heredoc, read-only): `coverage_contract picks: TC-2::test_x`; `waiver._same_instance(TC-1::test_x, TC-2::test_x): False`.
- `REQUIRED_ROW_FIELDS` vs `waiver.row_fields()` keys (probe): 6 fields, all with rows (+ `input_hash`).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "Axis 37 row (builders' text) is right in substance but incomplete and was never committed: Lead adds the F3 survivors, known roads (_passed_by_person / exit_gate.judge_words, N5, build_left_items, the three finding-id splitters) and N2 detectors. Axis 29: controller._record_person_pass is an unadopted, unqueued jsonl appender -> queue line given. Axis 23: row_fields table is a new per-field list over REQUIRED_ROW_FIELDS -> cross-reference line. In-artifact sweep: 8 index compositions (F3), 3 splitters (F5), 2 instance matchers (F2).",
  "fixes": [
    "F1 N1 fix worker: controller.py:7363 ask the index when refs_bad or ref_kinds or no_fp (F6 (a) covers stale/unknown, Lead confirms); window_record.py:1433-1455 write passed_by_word for every live-passed field, keep keys only for empty ones; row: refs-passed + fingerprint + stale ref -> accepted, unnamed -> stale text",
    "F2 N2 fix worker: coverage_contract.py:587 match the manifest row by waiver same-instance on the canonical id, not by alias-set intersection; row with TC-1::test_x and TC-2::test_x",
    "F3 topic fix worker on merged tree, FIRST: s5_precheck.live_word_index and waiver.record_word_index survivors; migrate controller.py:7395, window_record.py:1307, branch_accounting.py:1917, check_traceability.py:164, check_delivery.py:1194 and :1609, coverage_contract.py:560, traceability.py:1160; memoise _s5_word_index per completion check",
    "F4 N2 fix worker: check_delivery.py:1222 put the word-passed Then and its ts outside the 120-char cut of the no-record text (E16); row on v5",
    "F5 topic fix worker: waiver.py:791-793 docstring false; s5_precheck._finding_tag delegates to the splitter or queue exit_gate._finding_tag_of",
    "F6 topic fix worker: window_record.py:1433-1455 extract a helper (nesting 5), read the table once per build, drop the input_hash literal at :1444, use or drop window_keys values",
    "F7 N1 fix worker before N6: rename instance key passed_by_word to word_passed (collides with expectation_changes[].passed_by_word bool); Lead names its reader (N6 window_record.run) or drops it",
    "F8 Lead: amend F4 statement (b switch = one kinds row + one build_left_items branch) or open a node",
    "F9 Lead: add references/word-passed-facts.json to covers of test_words_doors.py and test_window_record.py in test-layers.json",
    "F10 queue: drop shipped-table value checks in row_fv130b_n1_the_not_run_section_and_the_field_rows; add test-budget reason lines to N1/N2 reports"
  ],
  "trail": {
    "read": [
      "docs/tasks/critic-diff-brief.md",
      "docs/tasks/specs/20261113-fv1-30b-word-fact-downstream-spec.md (lines 1-739)",
      ".claude/worktrees/fv130b-n0/docs/tasks/specs/reports/20261113-fv130b-n0-report.md",
      ".claude/worktrees/fv130b-n1/docs/tasks/specs/reports/20261113-fv130b-n1-report.md",
      ".claude/worktrees/fv130b-n2/docs/tasks/specs/reports/20261113-fv130b-n2-report.md",
      "git show 82c00a0, 5e7fa3f, dc8edef",
      "contract.py instance_id_aliases, case_matches, window_shape_errors",
      "acceptance.py:262-289; window_record.py:279-303, 1770-1787; coverage_contract.py:598-712",
      "check_delivery.py:1204-1260, 1418-1437, 1746-1777; check_traceability.py:236-285; traceability.py:1095-1160",
      "ledger.py:1585-1614; s5_precheck.py:4041-4058; branch_accounting.py:1829-1968; controller.py:2389-2452",
      "scripts/tests/test-layers.json keep rows; docs/SIBLING_MAP.md axes 23, 25-30, headings; docs/TESTING.md 60-139"
    ],
    "reruns": [
      {"command": "python -B scripts/tests/test_then_remainder.py (fv130b-n2 package dir)", "result": "=== test_then_remainder: 315/315 ok ==="},
      {"command": "git merge-tree --write-tree 5e7fa3f dc8edef", "result": "exit 0, no shared changed path"},
      {"command": "grep -rniE AR-13 pattern over n1/n2 scripts (tests excluded) + git grep at 4d0ad66 as positive control", "result": "n1: producers, writer, docstrings only; control hits branch_accounting.py:1931, controller.py:7365, 7448, 7450"},
      {"command": "python heredoc probe of coverage_contract alias match", "result": "picks TC-2::test_x for TC-1::test_x; waiver._same_instance False"}
    ]
  }
}
```
