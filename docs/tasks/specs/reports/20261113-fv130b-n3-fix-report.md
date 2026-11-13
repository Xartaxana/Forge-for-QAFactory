# FV1-30b N3 - fix round report (after the code critic: B1, F1, F2, F5, F6)

Worktree `.claude/worktrees/fv130b-n3`, branch `wip/fv130b-n3`, from head 2c75173. Files touched: `report_facts.py`, `scripts/tests/test_report_facts.py`,
`changelog.d/fv1-30b-n3-report.md`, this report. `waiver.py` untouched.

## Findings -> what changed

- **B1 (a)** `report_facts.py::_word_passed_gap`: after the obligation loop, for each manifest test and each field in `index.passed_fields(iid)` (the
  table's data, no list in code) other than `OBLIGATION_REFS`, a line while the manifest row's field is empty/absent (`_field_empty`); `(iid, field)` is the
  one-line key; needed text `the <field> given in the test manifest`. A field whose table row says `pass: false` is never in `passed_fields`, so a record
  naming only such fields prints no line (the word passed nothing).
- **B1 (b)** new `_word_bare_lines`: every pass whose record row names no subject (read from `waiver.person_passes` rows, `subjects` with no dict) prints ONE
  line by finding id (fallback tag), the LATER word by `ts` stands; the old `s5_plan_unread` / `other` clause is kept. No `waiver._entry_of` change: the
  subject count is read from the existing public rows, not a new field.
- **F1** `_quoted_word`: an entry with `revoked_at` is quoted and followed by `WORD_TAKEN_BACK` = `(you took this word back since; what it passed still stands)`,
  the verdict's wording; a revoked entry with no text falls to the journal's kept decision plus the same sentence.
- **F2** `left_gap_line(ref, what, needed, requirements=(), whole="")`: `whole` is appended after the cut `what`, behind one space, passes `_words` only
  (newline/whitespace runs collapse, pipe and markdown stand - the same escaping every other part gets minus the cut), empty/blank adds nothing. `_WORD_MARK`
  and the `.replace` splice are gone; `_word_gap_line` passes `whole = word + (by, ts)`. The empty-word case stays `(the word's text is not readable)`.
- **F5** the old row labelled E4 is relabelled E10 (it tests a line with no `word_at`); real E4 rows: old line with no check/case/tag/subjects, one per fact
  (then_unbound, not_run, row fields), plus `subjects: []`.
- **F6** the commit message names AR-13.
- Also (K12 quality note): the obligation loop is plain lines now.

## Rows (all in `fv1_30b_n3_every_recorded_pass_has_a_line`, `test_report_facts.py`)

B1 (a): one case per field of `waiver.row_fields()` read from the data file, id = the field name: recorded+empty -> ONE line (or none for the `pass: false` fields),
given since -> no line, re-given word -> ONE line with the later word; a synthetic field in a table copy (`waiver._fact_table` patched) -> its line with no code edit,
and no line against the real table. B1 (b)/E4: three facts + `subjects: []` + a line with subjects whose fact was repaired (no line) + two words for one old
finding (one line, later). F1: two rows. F2: byte-identical existing caller, 450-char word whole beside cut ref/what, newline/pipe/markdown, U+E000, blank whole,
24 KB word through the report. Existing first-round rows unchanged and green.

## Verification (verbatim)

`python -B scratchpad/run_n3.py` (the three N3 functions of `test_report_facts.py`, after the last edit; the whole file is in `scripts/slow_tests.json`
at 55.6 s, so it was NOT run whole):
`69 checks; 0 failed` (first-round functions plus the new one; the new one alone: 34 checks).

Red-capable (scratch driver, monkeypatching, nothing written to the tree):
```
green (as edited) 34 checks; 0 failed
RED probe 1: bare-line reader removed 34 checks; 8 failed   (B1 (b) / E4 rows)
RED probe 2: the field loop never fires 34 checks; 7 failed (B1 (a) field rows)
RED probe 3: revoked word quoted plain 34 checks; 17 failed
restored 34 checks; 0 failed
```
`scenario_walk.py --witness-for scripts/report_facts.py`: prints 3 scenarios + 16 keeps; non-slow ones run (slow ones per `slow_tests.json` not run):
```
test_exploratory_answers: 107/107 ok     test_exploratory_findings: 253/253 ok   oracle provenance: 296/296 ok
quality demand: 84/84 ok                 test_regression_scope: 93/93 ok         test_then_remainder: 320/320 ok
whole identifier and the revoked word: 166/166 ok                                test_whole_list_sites: 292/292 ok
```
`python -B scripts/selftest.py --lang`: `PASS lang: no Cyrillic anywhere in the package` / `=== qa-factory selftest: 2/2 ok ===`.

## FR walk (touched sections)

A refusals - not changed. B text to a person - the line wording is the verdict's; FR-6/10: one line per subject, a taken-back word is said so (FR-10). C contracts -
FR-14 `left_gap_line` shape kept, one optional parameter; FR-13 field list read from the table. D - FR-18 n/a. E - FR-35: a taken-back word does not read as a live
decision; FR-37 n/a. F - FR-41: an unreadable record still gives the one line and `unknown`. G - FR-30 English/ASCII (selftest --lang green); FR-54 siblings below.

## Deviations / decisions

1. `test_report_facts.py` is in the slow list: not run whole, only its N3 functions (above). CI judges the whole file.
2. A `pass: false` field named alone in a subject prints no line (the word passed nothing); a (finding id, `word_at`) pair shared by two dispatches where one row has subjects
   and one has none would print the bare line for both - not reachable in the record's own writer, not pinned.
3. The subject-less test reads `waiver.person_passes` a second time (the record index is built from the same rows); a public `subjects` count on the pass is Q1's.

## Siblings (the "known-fields filter hides a record" class in `report_facts.py`)

- 156, 1671, 2668, 2701, 4713 `C.live_stage_overrides`: drops revoked words on purpose (words that ACT / are shown as decisions, FR-35) - not this class, no fix.
- 713 `_word_entries` reads only a dict `word_passed` of a trace row; 3319 the obligation loop reads only `word_passed is True`: both are annotations N2/coverage write; a
  pass they do not annotate is now caught by B1 (a)/(b) - no fix.
- No other filter over word/waiver/override records found (grep `stage_overrides|word_passed|waiver\.|passed-by-person|live_stage_overrides|word_at`).
- Queue line (not done, outside owns): public reader in `waiver` - `_entry_of` carries `word`, `word_recorded`, `word_revoked`, `subjects` count; `fact_words()` (the verdict's Q1).
