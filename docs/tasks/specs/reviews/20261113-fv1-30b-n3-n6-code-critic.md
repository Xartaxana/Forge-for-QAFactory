# FV1-30b N3 + N6 — code critic (one pass for the topic's two remaining nodes)

Reviewer: critic (Opus). Date 2026-11-13. Under review: N3 `wip/fv130b-n3` 6a92521 + 2c75173, N6 `wip/fv130b-n6` 3fceeec, both on base a7c6f06
(= `wip/fv130b-topic` HEAD). N0-N2 and their fix round are not re-reviewed.

**Verdict: NEEDS WORK (fit_with_fixes) — 1 blocking finding (B1, N3), 6 fixes (F1-F6), 4 queue lines.**
N6 taken on its own: fit_with_fixes (F3, F4; no blocker). N3: B1 must be closed before acceptance.
This verdict is an input to acceptance; the decision belongs to the Lead.

## Blocking

**B1 (N3) — a recorded pass that let a gate go never reaches the report (AR-27, AR-28, owner item 5).** The surface is the report's
word-pass reader, `_word_passed_gap` (`fv130b-n3 report_facts.py:3265-3313`). It prints a `then_unbound`, `not_run` or
`row_fields_unestablished` pass ONLY when one of three readers annotated it: trace entries, ledger `not_executed` rows, coverage
obligations with `word_passed`. The obligation loop asks just `field="obligation_refs"` (`:3298-3303`). The `all()` loop (`:3304-3310`)
covers only `s5_plan_unread` and `other`. Two classes of recorded passes are therefore silent:
- (a) **Row fields other than `obligation_refs`.** The table passes `assertion_id`, `defect_location` and `profile_id` too
  (`references/word-passed-facts.json` `row_fields`, `pass: true`). N1's tier 4 lets `assertion_identity:<iid>` and
  `defect_location:<iid>` go on such a word, so this path is reachable in production today.
  Probe: a record line `{"finding_id":"manifest:TC-1:row-fields-missing","subjects":[{"instance_id":"A","fields":["assertion_id"]}],
  "word_at":"T1",...}` → `_word_passed_gap(...)` returned `''`. The gate let the gap go, and the delivered report says nothing.
- (b) **Old lines with no `subjects` (E4).** Probe: `{"block":"bindings:TC-1:unbound-2","decision":"go on","word_at":"T1"}` → `''`.
  Spec E4 says such a line gives "report line only", and owner item 5 (`20261113-p1-specs-amendment-owner-words.md:376`) says one line
  "по каждой записи S5". The N3 node text ("one line per pass a reader annotated") is the narrower reading the builder followed, and he
  flagged it (deviation 5). The spec contradicts itself here. The owner's word and AR-28 (an unknown is never a pass) decide the
  direction: show the line.

Expected behaviour (exact):
- (a) For each manifest test (`C.manifest_tests(manifest)` → `C.test_instance_id`) and each field `f` in `index.passed_fields(iid)`
  with `f != "obligation_refs"`: the line is printed while the manifest row's `f` is still empty or absent (E8: once given, no line).
  The line is `_word_gap_line(iid, "row_fields_unestablished", got, pipeline, detail=f" ({f})")`, with `got =
  index.instance("row_fields_unestablished", iid, field=f)`. Its needed text is per field, not the obligation text. Rendered:
  `- **A** — To check: row fields not given (assertion_id) — passed by your word "<word whole>" (human, <ts>). Needed: the assertion_id given in the test manifest`
- (b) For each pass in `index.all()` whose fact is `then_unbound` / `not_run` / `row_fields_unestablished` and that carries NO subjects
  (needs a `subjects` count on the pass: one line in `waiver._entry_of`, see F1): one line per finding id, the same form as `other`.
  `- **bindings:TC-1:unbound-2** — To check: Then not bound to a test — passed by your word "go on" (human, <ts>). Needed: a test bound to it, or your check by hand`
- Rows: (a) assertion_id passed with the field still empty → that line. The field given since → no line. (b) An old line → that line.

## Fixes (this round)

**F1 (N3, FR-10 / FR-35) — a revoked word is quoted as if it still passes.** `_quoted_word` (`report_facts.py:3223-3235`) matches any
`stage_overrides` entry by `at`, `revoked_at` included. Probe: entry `{"at":"T2","decision":"revoked word","revoked_at":"T3"}` →
`passed by your word "revoked word" (human, ...)`, with no mention of the revocation. The same report drops revoked words everywhere
else ("a revoked word is not shown as a decision (FR-35)", `report_facts.py:2662`, also `:156`, `:1665`). The fact still stands, so the
line stays (AR-27), but it must say the word was taken back. Change: when the matched entry has `revoked_at`, return
`"<word>" (you took this word back since; what it passed still stands)`. Row: a revoked entry gives that text, and the line is still
printed.

**F2 (N3, K2: the shape of the splice) — make the uncut word a parameter of the ONE form, not a sentinel.** `_word_gap_line`
(`:3238-3245`) puts `chr(0xE000)` into `what`, lets `left_gap_line` cut, then calls `line.replace(mark, word)`. Probe results: the word
is whole on every path I tried. A 1-line, 24 KB word with newlines, `|`, `**` and the sentinel character itself came out whole on one
line (newlines collapse to spaces, as `_words` does everywhere). `str.replace` does not re-scan what it inserts, so a sentinel inside
the word is harmless. A 300-character ref is cut and the word survives. The remaining hole: `.replace` hits EVERY sentinel in the
assembled line, so a ref or requirement that carries U+E000 would get the word twice. The bigger issue is that this is a private second
road around `left_gap_line`'s documented invariant ("`what` passes `_cut`", `:893-897`) that the ONE form does not know about
(AR-15 / AR-19). The better shape: `left_gap_line(ref, what, needed, requirements=(), whole="")`. `whole` is appended after the cut
`what` (`shown + " " + whole`) and documented in its docstring as the one uncut part (AR-24). `_word_gap_line` then passes
`whole=_quoted_word(...)` plus the `(<by>, <ts>)` tail, and `_WORD_MARK` goes. The existing `left_gap_line` callers are unaffected
(the default is `""`).

**F3 (N6, brief item 6/7, axis 34) — three copies of one composition.** `story_step.py:2545-2555`, `window_record.py:2139-2148` and
`driver_dispatch.py:952-966` each repeat the same block: lazy import, `live_word_index(root, list(window.get("scope_instances") or {})
or None, dispatch)`, `word_let_go`, and an `except` that keeps the gaps. That makes three spellings of "the window's scope", which
`window_record.build` already spells differently (`dispatch.scope`, `window_record.py:1315/1332`). Change: one public helper in
`window_record`, `word_kept(lines, window, task_root, dispatch_id) -> (kept, let_go)`: never raises, `(list(lines), [])` on any failure
or None. The three sites call it in one line each. The rows n1-n4 stay as they are; one row on the helper covers the raise and None
cases.

**F4 (N6, K10) — the finish's let-go note is not pinned, and it is lost on a refusal.** `story_step.py:2555` appends to
`decision_notes`, which are printed only after `controller.apply` returns (`:2603-2613`). A refusing `apply` raises past them. Row n1
stops at `prepare` (`Stop`), so no row ever sees the note. Change: one row where `prepare`/`apply` succeed and the output holds
`note: passed by the person's word: obligation_binding:A`. Optionally, also print the let-go lines at once when `apply` refuses.
`window_record.run`'s notes cover the driver path, which is why this is not a blocker.

**F5 (N3, K1/E4) — E4 has no row.** The row labelled "E4" (`test_report_facts.py:2055-2057`) tests a line with no `word_at`, not an old
line with no `check`/`subjects`. B1 (b)'s row closes this.

**F6 (N3 commit, brief item 10) — AR-13 touched and not named.** `_quoted_word` reads `pipeline.json stage_overrides` by `at`, a fact
`waiver.person_passes` already reads (`waiver.py:993-996`, `word`/`word_recorded` per row, `:1026-1027`). `word_passed_index` drops
those fields (`waiver.py:935-937`), so N3 had to re-read. The commit says AR-22/24/26/27/28 but not AR-13. Fix together with Q1, or
name it with "queued (Q1)".

## Queue (pile-ready, owner: the Lead of pile `fv1`)

- **Q1** `fv1 / N7 — the word whole through the record index` | owns `waiver.py` (`_entry_of`, `person_passes`, new `fact_words`),
  `report_facts.py` (`_quoted_word`, `_fact_words`) | behaviour: `_entry_of` carries `word`, `word_recorded`, `word_revoked` and
  `subjects` (count) from the record rows onto the pass. `person_passes` sets `word_revoked` from the matched entry's `revoked_at`. A
  public `waiver.fact_words(path=None)` reads the `words` section, a twin of `row_fields` / `not_run_lets_go`. `_quoted_word` and
  `_fact_words` read only these, which removes the second reader of `stage_overrides` and the private `_fact_table` call (K5). Row: the
  24 KB and revoked cases read through the index give the same text. | why: AR-13; the N3 builder noticed it (analogs 1 and 3).
- **Q2** `fv1 / N8 — needed text as data` | `references/word-passed-facts.json` gains a `needed` section beside `words`.
  `WORD_PASS_NEEDED` (`report_facts.py:3207-3209`) goes, read through Q1's reader. | AR-1 (closed variety in code).
- **Q3** `fv1 / N9 — one "plan row → instance ids" derivation` | `_not_run_instances` (`report_facts.py:3248-3262`) and
  `check_delivery._no_run_word_suffix` (`check_delivery.py:1647-1651`) share the plan_row → manifest tests → instance ids step.
  One public function in `contract`. | brief item 6.
- **Q4** `fv1 / N10 — the live index once per window, not per judge` | `window_record.run` builds the live index in `build`
  (`window_record.py:1324-1335`) and again in `run` (`:2142`). The driver's `window_gap` and `finish` build it again. Each build is
  a full `s5_precheck.run(judges=False)` whenever a live S5 word stands (`s5_precheck.py:4052-4054`), so one critic finish costs
  about 4 precheck runs (estimate, not measured). Memoise it (e.g. `build` hands its index to `run`, as F3 did for the controller).
  | FR-55.
- The Lead's queued "fourth judge" line (`coverage_contract.py:257`, K9) should be CLOSED, not queued. It is not a window judge (see
  K9).

## Keys

**K1 (N3 rows).** Item 5's four: (a) `test_report_facts.py:2030-2033`, (b)/E10 `:2039-2045`, (c)/E1 `:2022-2023` + `:2036-2038`,
(d)/E2 `:2068-2073`. Rows r1 `:2027-2035`, r2 `:2022`, r3/E8 `:2079-2084`, r4 `:2068-2073`. E6/E8 table `:2124` ff. E11 `:2046-2054`.
All are red-capable: r1 depends on the new `_partly_words` branch, because the same story reads `proven` without the record (`:2023`).
The byte-identity pin (`:2038`) compares the new code with no record to the new code before the record existed, not to the base code.
By the diff the no-record path adds only `""` (`render` `+ str("")`, held list `+ []`), so it is identical to today by construction.
Accepted. Gap: E4 (F5) and B1 rows.

**K2.** The word is whole on every path probed (details in F2). The splice is a clean result but a side road around the one form. F2
gives the better shape.

**K3.** The signature `(art, entries, ledger, manifest, pipeline, unknown)` is justified by the data: `facts` holds neither the trace
rows, nor the raw ledger `rows` / `coverage`, nor `pipeline`. N3 builds no reader of the record rows. The record is read only by
`waiver.record_word_index(art)` (`:3279`). `_word_entries` reads N2's annotated trace field. The obligation loop reads the stored
projection. Searched: `word_passed_index|word_passes\(|person_passes|passed-by-person` in the N3 `report_facts.py`, case-insensitive →
none. Positive control: `record_word_index` → found. The one own read is `_quoted_word`'s `stage_overrides` read (F6/Q1). It reads the
word's text, not the pass rows.

**K4.** Yes, a recorded pass can be silently invisible. This is B1 (blocker), with the exact lines given there.

**K5.** Yes, a revoked word is shown as if it passes. This is F1 (fix now, inside N3's file). The public reader (`fact_words`, word
fields on the index) is Q1 (queue: `waiver.py` is outside N3's owns).

**K6.** Traced. A word-passed Then is a `not run` trace row (N2). `_word_entries` makes one held entry per (key_of(case), then)
(`:705-726`). `_held_thens` matches on the same `key_of` and the same `then` element (`:690-702`). `_classify(results, held=True)` with
a `pass` gives `wait` (`:661-663`). With no pass, `not run` gives `unproven` (`:665-666`). `proven` is unreachable on both branches.
`partly` is said only when a pass exists (`:809`). A requirement shared by two cases: held is computed per requirement over ALL its
rows, so a pass row from TC-1 beside the word-passed row from TC-2 gives `wait`. One Then under two requirements is tested
(`:2088-2099`). The two-cases-one-requirement shape has no row. It holds by construction (low; it could join B1's fix round).

**K7.** Positional invariant at the three sites:
- finish: the filter is at `story_step.py:2545-2555`, before `_blocked_ids`, `no_instance` and `_derived_pair` (`:2556-2566`). The
  rows: n1 (`test_window_record.py`, "n1 (E32 invariant)"), a kept `product:C` → no pair, n4 raising/None → today.
- run: the filter is at `window_record.py:2139-2148`, before `derivable`, `sent_back` and the NOT-acceptable listing (`:2165-2222`).
  The rows: n2 (one more `review:A` → exit 1, listing only the kept gap), n4.
- window_gap: the filter is at `driver_dispatch.py:952-966`, before the "other gap → ()" loop (`:967-969`).

I probed this site myself, with a constructed record, patched `validate_window` and a real `word_passed_index`:
- `[handed:A, product:B]` with B not_run-passed → `('handed_to_person', 'handed_to_person: handed_to_person:A')`, index asked
  `(['TC-1'], 'd-7')`
- no word → `()`; raising → `()`; None → `()`
- `+ review:B` → `()`
- E29 (B carries an outcome) → `()`

An empty list after filtering falls through exactly like an originally empty list at all three sites (the builder's edge note,
confirmed by reading). One consequence at finish: all gaps let go plus `no_instance` handed cases → the handed pair is now derived.
That is correct (the remaining gaps are derivable).

**K8.** The stem default is never used in production. The one caller passes `dispatch` (`driver_dispatch.py:799`). The stem serves only
test calls (`test_story_run_loop_b_loop.py:239-375`, `test_window_record.py:2467`). Where the stem could differ: `window_record.run`
writes `_safe_name(dispatch_id)` (`window_record.py:2124`, `:433-434`), while the driver reads `work/windows/{dispatch}.json` unsanitised
(`:786`, a pre-existing mismatch: a missing file gives `()`, the safe side). If a wrong id ever reached `live_word_index`, the scope is
still passed explicitly. Only the dispatch-keyed checks (`is_s7_fix_round`, plan conformance) would differ, so the passes could differ
in either direction. Even then, `word_let_go` lets go only lines of instances the window holds and a live word names. The controller's
tier 4 judges again with the real dispatch, so the worst case is a proposed pair the controller refuses (the refusing side), never a
wrong accept. Keeping it is safe. Making `dispatch` required would remove a default nobody needs (optional).

**K9.** No contradiction. `witnessed_binding` (`coverage_contract.py:252-258`) is a FACT reader: is this obligation's evidence current?
It is not a window-acceptance judge. Spec R5 / D13 (ii) says an obligation whose binding names a refs-passed instance is "already never
`verified`". The word passes the STEP, never the FACT. The person sees a window that is accepted and an obligation that is "not
verified; passed by the person's word" (N2's words), which is consistent. Wiring `word_let_go` there would make a word verify a fact,
which breaks the topic's core rule. Recommendation: close the Lead's queue line as "not applicable — intended (D13 (ii))".

**K10.** Let-go visibility:
- `window_record.run` prints every let-go line (`:2147-2148`, row n2).
- finish prints them via `decision_notes`. This is unpinned and lost on a refusal (F4).
- `window_gap` prints nothing by design; the same lines are printed by `window_record.run`, which the driver runs first (`:789`).
- In the report, the facts behind window let-gos reach the report through N3, except B1 (a): `assertion_identity` and
  `defect_location` let-gos have no report line. That is the B1 gap.

Names: N3 reads the trace `word_passed` (a dict, `traceability.py:1156`) and the coverage `word_passed` (`True`,
`coverage_contract.py:710`). N6 reads none of them. The window item's `word_passed` (a list, `window_record.py:1466/1532`) is read by
neither node. All three carriers share one name with three shapes. N3 checks the type of each one it reads (`isinstance(word, dict)`,
`is True`), so nothing is misread. Noted for axis 37, not a finding of these nodes.

**K11.** K12 landed as specified: `window_record.py::run` is `xref` / `intent` (census diff line 1146). `finish` and `window_gap` are
not census units (builder). The `ratchet` block (census line 4) is unchanged. `shape → xref` is not a ratcheted class. No other
shrink-only ratchet file is in either diff (`git diff --stat` on `*ratchet*`, `*baseline*`, `*role-load*` → empty). Census test re-run:
24/24 (see trail and the deviation note).

**K12. DUPLICATION AND CONSISTENCY:**
- N6: three copies of one block (F3).
- N3: `_quoted_word` re-reads what `person_passes` reads (F6/Q1). `_not_run_instances` is a clone of `_no_run_word_suffix`'s
  derivation (Q3). `WORD_PASS_NEEDED` is closed variety in code (Q2).
- No clone of the existing gap-line builders: N3 goes through `left_gap_line` (with the F2 reservation). Grepped:
  `left_gap_line\(|gap_needed_line\(` in N3's `report_facts.py`. The only new caller is `_word_gap_line` plus the E2 line.

**CODE QUALITY:**
- No new function over 60 lines: `_word_passed_gap` is 49 lines (`:3265-3313`), `_word_entries` 22, each N6 block about 10.
- Nesting: `_word_passed_gap`'s obligation loop packs two conditionals into the `for` expressions (`:3298-3299`), which is hard to read
  (fold into F2's round: a plain `obligations = ...` line).
- The `pipeline` type is guarded twice (`:3285` and in `_quoted_word`); this is harmless.
- `window_record.run` prints "the window is acceptable: no structural error, no semantic gap." after it has let gaps go, which
  undersells what happened; the notes above it say so (low).
- No dead branches found.

**K13 (class-wide).**
- Axis 34, one road: F3 (three spellings of one composition) and the `stage_overrides` second read (Q1). Both are named, as a fix and
  a queued node with an owner.
- Axis 37: still absent from `docs/SIBLING_MAP.md`. Checked the root and both worktrees: the last axis is 36. The earlier verdict's
  Lead item (commit the axis-37 row) is still open. When it lands, the row must list the three N6 sites (or F3's helper),
  `report_facts._word_passed_gap` / `_quoted_word`, and the K10 note on the three `word_passed` shapes.
- Axis 17 (one tool wired everywhere the problem occurs): the window judges are covered (controller tiers 2-4 by N1, the three by N6).
  `coverage_contract:257` is out of class (K9). Asymmetry left: the report covers only one of four passable row fields (B1).

**K14 (merge).** File sets are disjoint. N3 owns `report_facts.py`, `test_report_facts.py`, its changelog fragment and its report. N6
owns `driver_dispatch.py`, `story_step.py`, `window_record.py`, `test_window_record.py`, `judgment-census.json`, its changelog fragment
and its report. `git merge-tree --write-tree wip/fv130b-n3 wip/fv130b-n6` → rc 0, tree 44de67a. topic+n3 → rc 0. topic+n6 → rc 0
(topic = a7c6f06 = both bases).

**ONE ROAD (brief item 12):** no exclusion of a language, project or case. The residuals of the class are F3 (fix) and Q1 (node,
owner: the Lead of pile `fv1`).

**JUDGMENT (item 11):** no judgment moved into code. N6 filters only by the person's recorded word (owner `intent`), and N3 renders
text. N6's `judgment: none` is defensible. The census reclassification is the spec's K12.

## Deviation of my own

`test_judgment_census.py` is listed in `scripts/slow_tests.json`. I ran it as the cheap control before checking the list, against the
dispatch's "do NOT run files listed in slow_tests.json". It finished well under the timeout (24/24 ok). It ran in the N6 worktree and
nothing ran in parallel. Recorded here so the Lead can count it.

## Trail

Read:
- the spec: §3 R1, R3, R4, R5 head, §5 E1-E4/E6/E8/E10-E12/E29/E30/E32/E33, §6 N3/N6, §7, the K12 row
- owner item 5: `20261113-p1-specs-amendment-owner-words.md:370-384`
- both builder reports; both diffs in full (code, tests, census, changelog); both commit messages
- `waiver.py:740-1048`
- `report_facts.py`: 88-110, 640-726, 783-817, 855-903, 2650-2667, 3199-3313
- `window_record.py`: 1218-1339, 2085-2228
- `story_step.py:2515-2627`
- `driver_dispatch.py`: 760-810, 920-985
- `s5_precheck.py`: 3990-4070, grep of `dispatch_id`
- `coverage_contract.py`: 225-274, 690-717
- `check_delivery.py:1640-1658`
- `ledger.py` coverage storage (grep)
- `references/word-passed-facts.json`
- `critic-diff-brief.md` items 6-12
- `SIBLING_MAP.md` axis list
- the earlier topic verdict (F3/F4/F5/F8/axis 37)

Re-runs and probes: see the JSON block.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1 (N3) report_facts.py:3265-3313 _word_passed_gap prints no line for (a) a row_fields_unestablished pass of assertion_id/defect_location/profile_id (tier 4 lets assertion_identity/defect_location go on it: reachable) and (b) an old record line with no subjects (spec E4, owner item 5 'one line per S5 record'); probe: both return ''. Expected: (a) per manifest test iid and passed field f != obligation_refs whose manifest value is still empty: '- **A** -- To check: row fields not given (assertion_id) -- passed by your word \"<word>\" (human, <ts>). Needed: the assertion_id given in the test manifest'; (b) per subject-less pass of then_unbound/not_run/row_fields_unestablished: one line by finding id in the 'other' form; rows for both and for 'field given since -> no line'"
  ],
  "fixes": [
    "F1 (N3) report_facts.py:3223-3235 _quoted_word: a stage_overrides entry with revoked_at -> '\"<word>\" (you took this word back since; what it passed still stands)', line kept; one row",
    "F2 (N3) report_facts.py:3238-3245: replace the chr(0xE000) sentinel + str.replace splice with left_gap_line(..., whole='') appended uncut after the cut what and documented in left_gap_line's docstring (:888-902); drop _WORD_MARK",
    "F3 (N6) story_step.py:2545-2555, window_record.py:2139-2148, driver_dispatch.py:952-966: one helper window_record.word_kept(lines, window, task_root, dispatch_id) -> (kept, let_go), never raising; three one-line calls; one row on the helper",
    "F4 (N6) story_step.py:2555: a row where prepare/apply succeed and the output carries 'note: passed by the person's word: obligation_binding:A' (today unpinned; notes are lost when apply refuses)",
    "F5 (N3) test_report_facts.py:2055-2057: the 'E4' row tests no word_at, not an old line without check/subjects; B1(b) row closes it",
    "F6 (N3 commit) name AR-13 (the stage_overrides re-read in _quoted_word) as 'queued (Q1)' or fix with Q1"
  ],
  "class_completeness": "Surface: the report's word-pass reader and the window judges' let-go composition. Axis 17: window judges complete (N1 tiers 2-4, N6 the other three); coverage_contract.py:257 is a fact reader, out of class by D13(ii), Lead's queue line should close. Asymmetry: report covers 1 of 4 passable row fields (B1). Axis 34: three copies of the live-index+let-go composition (F3) and a second reader of stage_overrides-by-at (F6/Q1, owner Lead of pile fv1). Axis 37 row still absent from SIBLING_MAP (root and both worktrees end at axis 36) - earlier verdict's Lead item open; must list the N6 sites/F3 helper, _word_passed_gap/_quoted_word, and the three shapes of the name word_passed. Queue: Q1 word fields + fact_words through the record index, Q2 needed section as data, Q3 one plan_row->instance ids derivation, Q4 live index memoised per window (FR-55).",
  "trail": {
    "read": [
      "docs/tasks/specs/20261113-fv1-30b-word-fact-downstream-spec.md (R1, R3, R4, R5, section 5 edges, N3, N6, section 7)",
      "docs/tasks/specs/20261113-p1-specs-amendment-owner-words.md:370-384",
      ".claude/worktrees/fv130b-n3/docs/tasks/specs/reports/20261113-fv130b-n3-report.md",
      ".claude/worktrees/fv130b-n6/docs/tasks/specs/reports/20261113-fv130b-n6-report.md",
      "git diff a7c6f06..HEAD in both worktrees (code, tests, census, changelog) and both commit messages",
      "ai-packages/qa-factory/scripts/waiver.py:740-1048",
      "ai-packages/qa-factory/scripts/report_facts.py:88-110,640-726,783-817,855-903,2650-2667,3199-3313 (n3)",
      "ai-packages/qa-factory/scripts/window_record.py:1218-1339,2085-2228 (n6)",
      "ai-packages/qa-factory/scripts/story_step.py:2515-2627 (n6)",
      "ai-packages/qa-factory/scripts/driver_dispatch.py:760-810,920-985 (n6)",
      "ai-packages/qa-factory/scripts/s5_precheck.py:3990-4070",
      "ai-packages/qa-factory/scripts/coverage_contract.py:225-274,690-717",
      "ai-packages/qa-factory/scripts/check_delivery.py:1640-1658",
      "ai-packages/qa-factory/references/word-passed-facts.json",
      "ai-packages/qa-factory/scripts/tests/test_report_facts.py:2010-2125 (n3)",
      "docs/tasks/critic-diff-brief.md items 6-12",
      "docs/SIBLING_MAP.md axis headings",
      "docs/tasks/specs/reviews/20261113-fv1-30b-topic-code-critic.md (grep F3-F8, axis 37)"
    ],
    "reruns": [
      {"command": "probe (python -B heredoc, n6 scripts): Driver.window_gap on a constructed record with patched validate_window/live_word_index and a real waiver.word_passed_index", "result": "[handed:A, product:B] + B not_run word -> ('handed_to_person','handed_to_person: handed_to_person:A'), index asked (['TC-1'],'d-7'); no word -> (); raising -> (); None -> (); + review:B -> (); E29 B shows a run -> (); default dispatch -> stem 'd-7'"},
      {"command": "probe (python -B heredoc, n3 scripts): report_facts._word_passed_gap on constructed passed-by-person.jsonl + pipeline", "result": "assertion_id pass -> '' (B1a); old then_unbound line without subjects -> '' (B1b); plan-unread with 450-char word + newline + pipe + ** + U+E000 -> 1 line, word whole; revoked entry -> 'passed by your word \"revoked word\"' with no mention (F1); 300-char finding id -> cut ref, word whole"},
      {"command": "(cd fv130b-n6/ai-packages/qa-factory && python -B scripts/tests/test_judgment_census.py) -- NOTE: listed in slow_tests.json, run in deviation", "result": "=== judgment_census: 24/24 ok ==="},
      {"command": "git merge-tree --write-tree wip/fv130b-n3 wip/fv130b-n6; topic+n3; topic+n6", "result": "rc 0 (44de67a), rc 0 (f725afa), rc 0 (6872142); topic HEAD = a7c6f06 = both bases"}
    ]
  }
}
```
