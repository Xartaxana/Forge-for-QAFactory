# t-1040 — critic code gate on t-1035 (card S9, a person's word on a `review` gap, FR-57)

Under review: branch `worktree-agent-abb8f45302b3ae471`, `b87cceee` (code, tests, row) + `a8fbb970` (report), base `d41bcdd0`.
Spec: `docs/tasks/specs/20261117-rules-debt-phase2-s9-fl-cards-spec.md` §2 + §4 "Lead decisions after t-1034".

**Verdict: fit_with_fixes (NEEDS WORK).** Two findings to fix in this round: F1 (the B6 invariant breaks at the predicate)
and F2 (the state-exits row says something the code does not do). Three smaller ones (F3-F5) are fixes in the same round.
Nothing blocks the merge once the round lands. The decision to accept belongs to the Lead.

## Findings

**F1 — fix in round (B6, key 2). `word_let_go`'s review rule lets go another instance's gap when one instance id
holds the separator (U4 at the predicate), and the controller then records no pass line for it, so the pass is silent.**
`window_record.py:1355-1361`: `heads` is built from `review_words` alone, and a line is let go when
`line.startswith(h + " — ")`. Take window ids `A` and `A — x`. The reader names only `A`, which is correct (F9-3). But the
bare controller line `review:A — x` (the gap of instance `A — x`, `acceptance.py:1157-1172`) starts with `review:A — `, so it
is let go too. Probe output (scratch `probe.py`, verbatim):
```
P1 review_words: {'A': {'words': 'go', 'at': 't0'}}
P1 word_let_go bare lines: ([], ['review:A', 'review:A — x'])
P2: ([], ['review:A — x — expl'])
```
In `controller.py:7543-7548`, the comprehension skips `review:A — x` because `"A — x" not in review_words`. So the gap is
removed from `other_gaps`, nothing refuses, and no `passed-by-person.jsonl` line is written. That is a pass with no record
(FR-4), for an instance nobody named (the B6 invariant, AR-28). `window_record.run` makes the same mistake: it prints
"passed by the person's word" for the `A — x` line. The card's item 2 spells out the `startswith` rule at the predicate.
F9-3 (exact match first, else the longest id) was applied only in the reader. The reader's own docstring invariant ("never
lifts the review gap of another") is what the predicate breaks. The U4 rows exist only in `s9_review_gap_words`, so no test
catches this.
**Fix:** one helper used by both sites (this also closes F4):
```python
def _review_owner(text, ids):
    """The one id of `ids` whose review head `text` carries: exact equality first, else the longest head followed by ` — `; None."""
    named = [i for i in ids if text == _review_gap_head(i) or text.startswith(_review_gap_head(i) + " — ")]
    exact = [i for i in named if text == _review_gap_head(i)]
    return exact[0] if exact else (max(named, key=len) if named else None)
```
`review_gap_words` calls it with `m`. `word_let_go` lets a line go only when `_review_owner(line, <every non-empty string id
of window["instances"]>) in review_words`. Use all of the window's ids here, not just the named ones: that way the line
belongs to its longest owner first. New row in `fv1_30b_word_let_go_is_the_one_predicate`, with ids `A` and `A — x`,
`review_words={"A": …}`, and lines `review:A`, `review:A — x`, `review:A — x — e`, `review:A — e`. Expected: kept
`review:A — x`, `review:A — x — e`; gone `review:A`, `review:A — e`. Mirror row with `{"A — x": …}`: gone are the two
`A — x` lines only. The expected values come from B6 and F9-3.

**F2 — fix in round (key 7, AR-25/FR-37). The new state-exits row claims "the pass line leaves the report with it" when a
critic verdict is recorded later. It does not.** The pass line is `check: "review"`. That maps to fact `other`
(`waiver._fact_of`, `references/word-passed-facts.json` has no `review` row). Probe:
`[('other', 'review:A')]`, control `run_mapping/no-row-A` → `['not_run']`. `report_facts._word_bare_lines`
(`report_facts.py:3345-3365`) prints every `other` pass whether or not the fact still stands. `passed-by-person.jsonl` is
append-only. So once the critic approves later, the report still shows "passed by your word" for that test.
**Fix:** correct the row's exit cell. Say that a later critic verdict removes the GAP (the next window has none), and that
the recorded pass stays as a past line under "passes recorded by your word". Do not change the reader: that is reading (i)
plus fact `other`, as §4 decided. The report keeps showing a pass for a fact that was repaired, which is an AR-27 nuance.
It goes into the F9-1 follow-up node as an input (it will give the review word its own fact). Add a line to §4's
"follow-up node of (ii)" | node: F9-1 follow-up (Lead opens it on the owner's answer).

**F3 — fix in round (key 7, a comment that is now false).** The `WORD_READ_KINDS` comment at `window_record.py:1817-1818`
still says "the controller reads a word for the critic's receipts and for a missing window record, never for a gap of the
window". It sits right after the new S9 sentence. It is false for `review:` now, and it was already false for the
not_run/row_fields lines. The comment is in owns. **Fix:** cut that clause, or write "...and, through `word_let_go`, for the
gaps it names".

**F4 — fix in round (key 7, duplication).** The head test `x == h or x.startswith(h + " — ")` is written twice in new code
(`window_record.py:1289`, `:1361`). It also exists twice already in the same form (`:2164`, `:2193`, the P-i precedent).
The `_review_gap_head` docstring claims "one definition for the matcher and the predicate", but the separator literal is
repeated. The F1 helper removes the two new copies. The two older ones match a different direction (a problem line against
a head) and can stay as they are: note only.

**F5 — fix in round (key 7, code quality).** `word_let_go` (`window_record.py:1300-1368`, about 69 lines) now nests 6
levels deep: try / if index / try / for / if section / update, with max indent 28. The new outer `try` wraps the old body
verbatim. **Fix:** move the old index body out into `_index_let_go(window, index, lets_go) -> set` (it returns `set()` on any
exception), and make `word_let_go` the union of that and the review rule. Behaviour stays the same. In the same pass,
`controller.py:7543-7548` computes `g[len("review:"):]` five times. Bind `iid = g.partition(":")[2]` once (note).

**F6 — note (report accuracy).** The report says the non-ASCII test ids were written "as `\u` escapes". They are literal in
the file: added lines carry U+00DC, U+00EF, U+00FC, U+2713 and U+2013. The scan found no Cyrillic and no control bytes, so
FR-29/FR-30 hold (`selftest.py:298` checks Cyrillic only). Earlier test files carry literals too. Only the report's claim is
wrong.

**F7 — note.** An instance id with trailing whitespace (`"A "`) cannot be named by the bare word, because `m` is stripped:
`rgw(["A "], ["review:A "])` → `{}`. The reason-tail form does name it (`{'A ': …}`). The error points the safe way (nothing
passes), and the door text shows the tail form through `verdict`'s printed line. No change.

## Keys

1. **Fit to the card.** Items 1-7 are implemented as written. Item 8 is void by N-1, and `judgment-census.json` is untouched
   (diff stat: 6 files, all within owns). In `controller.py` only `_s5_gap_problems` changed (the diff hunk at 7517-7548).
   `controller-blocks.md` was left alone. The builder reports a generator run to scratch that came out byte-equal; I accept
   that as stated (not re-run). The deviations the builder chose are all safe: the door is built with `person_words.door`,
   the same road as `PROBE_GAP_RECORD`, and the substring `--block "review:` is present; a raising table read no longer
   hides the review rule. The only gap against the card's invariant is F1.
2. **B6.** Reader: exact head, case-exact, one record names one instance, F9-3 (a). I re-ran 60 rows and probed further:
   prefix id, separator id, case, `review: A`, en dash and hyphen, empty id, missing/empty/non-string `match`, `*`,
   `review:*`, list forms, and two words for one gap (the later one wins: `P4 {'A': {..., 'at': 't1'}}`). All behave as the
   card says. Predicate: broken for U4 (F1).
3. **B7.** Row (d) is pinned. With no word and the typed pair, the window is accepted and no pass line is written. When the
   pair is absent, the kept gaps are refused by `unresolved window: …` (`controller.py:7529-7530`, unchanged). The `*` word
   is refused and writes no line, row (b). Every row uses `p` without the pair, except (d) and `passed_green`.
4. **Error direction.** Unreadable or malformed pipeline, a non-dict window, entries that are not objects → `{}`
   (`s9_review_gap_words` E5 rows, re-run). An unknown instance or a kind other than review → `{}` (probe P5: `review:B`,
   `stale_review:A`, `probe_gap:A`). Stage `s5` (case) is not read (P7). The other rules: I compared the old and new
   `word_let_go` line by line. `index is None` → old early return, new `let = set()`; any exception → `(lines, [])` in both;
   a partial index walk is dropped (`let = found` only after the loop). I then re-ran
   `fv1_30b_word_let_go_is_the_one_predicate` with all its old pins ("an index that raises: every line kept", "a window that
   is no object", the not_run/row_fields union rows), and they pass. I did not replay recorded stories: that is the CI
   canon's job (scenario tests named by the walker).
5. **AR-13 / AR-15 / AR-24 / axis 5.** `live_stage_overrides(` has 30 callers in the package. The only `review:` reader is
   `window_record.py:1282`. Grep shows `"review:" +` builders only in `acceptance.py` (the gap producer) and the
   controller's pass list. The other S5 override readers are `s5_precheck.py:4049` (exit findings, `_names`) and
   `report_facts.py:1677` (`*` / changed-after-red), and neither reads a review word. Judge sites: `controller.py:7528`
   directly; `story_step.py:2563`, `driver_dispatch.py:1018` and `window_record.py:2266` through `word_kept`.
   `controller.py:7122` (shape call) is unchanged, as the spec requires. `verdict`'s `read` join (`:1972`) uses the same
   reader with the exact identity, so it agrees. AR-24: `decision` is the whitespace-folded words and `word_at` points to
   the whole record (the test checks both). Axis 5: Grep `word_let_go|review_gap_words` over `driver_stage_s6.py` found
   nothing; the positive control on `driver_dispatch.py` hit (999, 1014).
6. **Tests.** The expected values trace to the card's rules (U1-U4, E1-E12, rows a-d). The tables are parameterised. No
   new file. No internal-boundary test, since every row goes through a door the package uses (reader, predicate,
   `word_kept`, `verdict` info, controller). Killing power: the rows would catch a `names_whole` reader, a missing `*`
   filter, an early return on a None index, and a pass line on a typed pair. They would not catch F1. `tests-over:` is
   present in the commit with a reason that holds (the card names the rows). The two files keep their layer rows
   (`gate_named`, `detector`); neither is quarantined.
7. **Duplication / quality / hygiene / row.** F3, F4, F5 and F6 above. Hygiene: no Cyrillic, no control bytes. The row is
   true except its exit cell (F2).
8. **Class.** Axis 26: n/a holds, since the review word is not the stand word and its docstring says why. Axis 32: no census
   row by N-1. The commit's `judgment: adds data check … no census row` is honest: the reader joins identifiers and reads no
   wording. Axis 34: one road, `word_let_go`, with no third road. The remaining split by gap kind (a probe word goes to
   `after_checks`, a review word to `no`) is F9-1, a question with the owner, carried in spec §4. The builder's analogs:
   the `NO_DOOR` / `stale_run` comments are still true for their kinds, so no fix. `acceptance`/`ledger` reading the review
   state is the F9-1 follow-up. The `controller-blocks-gen.py --help` writing a file → `tools/controller-blocks-gen.py`
   treats `--help` as an output path | carry-over: findings/ of the forge pile | reason: tools hazard outside the
   package, not S9 | confirmed: —. The `OWNER_PRINCIPLES_INDEX.md` regeneration was not committed, which is correct (it is
   not in owns).
9. **Step 0.** Still a valid measurement. The three setups (folder name = task id, a project config copied from the
   fixture's own `config-at-start.json`, stub files at the manifest's paths) are infrastructure. They get the CLI to the
   point where `verdict` lists a `review:` gap. None of them touches the code under question (`verdict`, `_unread_words`,
   `word_let_go`), and the critic_verdict deletion is the one the card allows. What the run proves holds: today's code
   printed the gap and "recorded, not read" for a whole-line word. The builder's side observation is a real fact: the
   unread note fires only when the word is whole words of the printed line (`_unread_words` uses `names_whole`). The run
   was not repeated after the change, so the absence of the note on the new code is shown only by the
   `a_word_nothing_reads…` rows. The card's recipe should name the three setups; the Lead can add that to the spec as a
   one-line note.

## Not checked

Slow files and scenario tests as whole files (the CI canon's job). `waiver.py` CLI acceptance of `--block "review:<iid>"`
against the standing refusal: the spec marks it NOT ESTABLISHED, and the live-runs row covers it. The `controller-blocks.md`
byte-equality (taken from the report). The §2.4 reader grep over `tools/`/`.githooks/`/`.claude/`. The ratchet pipeline
(`forge-check`): no ratchet file is in the diff.

## Trail

- Read: spec §2 (lines 82-347) and §4 (837-893); the builder report; diff `d41bcdd0..b87cceee` in full; `controller.py`
  7440-7550 and 2403-2448; `window_record.py` 1806-1825, 1936-1975, 2255-2285; `waiver.py` 742, 801-816, 918-1048;
  `report_facts.py` 3290-3365, 1670-1690; `s5_precheck.py` 4040-4060; `references/word-passed-facts.json`;
  `docs/SIBLING_MAP.md` axes 26, 32, 34; `docs/tasks/critic-diff-brief.md`; `test-layers.json` rows of the two files.
- Re-ran `fv1_30b_word_let_go_is_the_one_predicate` + `s9_review_gap_words`, called directly (scratch `smoke.py`):
  exit 0, 88 `PASS`, no other lines but "ran …".
- Probe `probe.py` (F1, P3-P7) and `fact.py` (F2): outputs quoted above.
- Hygiene scan `scan.py` of the added lines: non-ASCII `0x2013 0x2014 0x2713 0xdc 0xef 0xfc`, Cyrillic False, control
  False.
- Greps: `live_stage_overrides(` across the package; `"review:"` builders; axis-5 grep with its control.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "Axis 26 n/a (not the stand word, reason in the reader docstring); axis 32 no census row by Lead decision N-1, judgment line honest; axis 34 one road word_let_go, the probe-vs-review delivery split is F9-1 with the owner (spec 4); axis 5 no S6 twin (grep driver_stage_s6.py empty, control driver_dispatch.py hits). Within the artifact: F1 is the U4 class left unapplied at the predicate (applied only in the reader); F4 the duplicated head test.",
  "fixes": [
    "F1 window_record.py:1355-1361 word_let_go review rule: attribute each line to its owner among ALL window ids (exact first, else longest, one helper _review_owner shared with review_gap_words) and let it go only if that owner is in review_words; add the U4 predicate rows (ids A and 'A — x') to fv1_30b_word_let_go_is_the_one_predicate",
    "F2 design/state-exits.md new row exit cell: drop 'the pass line leaves the report with it' - the pass is fact other and report_facts._word_bare_lines keeps printing it; say the gap leaves, the recorded pass stays; note the nuance for the F9-1 follow-up node",
    "F3 window_record.py:1817-1818 WORD_READ_KINDS comment: remove or correct 'never for a gap of the window'",
    "F4 window_record.py:1289 and :1361 duplicated head test: one helper (comes with F1)",
    "F5 window_record.py:1300-1368 word_let_go: extract the index body into _index_let_go to undo 6-level nesting; controller.py:7543-7548 bind the iid once"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-rules-debt-phase2-s9-fl-cards-spec.md (2, 4)",
      ".claude/worktrees/agent-abb8f45302b3ae471/docs/tasks/specs/reports/20261117-rules-debt-s9-report.md",
      "git diff d41bcdd0 b87cceee (all six files)",
      "ai-packages/qa-factory/scripts/controller.py 7440-7550, 2403-2448",
      "ai-packages/qa-factory/scripts/window_record.py 1245-1390, 1806-1825, 1936-1975, 2255-2285",
      "ai-packages/qa-factory/scripts/waiver.py 742, 801-816, 918-1048",
      "ai-packages/qa-factory/scripts/report_facts.py 3290-3365, 1670-1690",
      "ai-packages/qa-factory/scripts/s5_precheck.py 4040-4060",
      "ai-packages/qa-factory/references/word-passed-facts.json",
      "docs/SIBLING_MAP.md axes 26, 32, 34",
      "docs/tasks/critic-diff-brief.md"
    ],
    "reruns": [
      {"command": "python -B scratch/t1040/smoke.py (fv1_30b_word_let_go_is_the_one_predicate + s9_review_gap_words called directly)", "result": "exit 0, 88 PASS, no FAIL"},
      {"command": "python -B scratch/t1040/probe.py", "result": "P1 word for A lets go review:A and review:A — x (F1); P3 trailing-space id bare word {}; P4 later word wins; P5 unknown instance / other kinds {}; P6 missing or empty match {}; P7 stage s5 {}"},
      {"command": "python -B scratch/t1040/fact.py", "result": "review pass row -> fact other; control run_mapping -> not_run (F2)"},
      {"command": "python -B scratch/t1040/scan.py over added diff lines", "result": "non-ASCII 0x2013 0x2014 0x2713 0xdc 0xef 0xfc; Cyrillic False; control bytes False"}
    ]
  }
}
```
