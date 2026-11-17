# t-929 — rules-debt, pass S1a (debt file)

DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/design/factory-rules-debt.md` (plus `test_null_outcomes.py`, `test_s1_s2_contract.py`, `pytest tools/test_piles_close_id.py -q -p no:cacheprovider`)

## Output

Run from the worktree (`( cd <worktree> && ... )`), once, at the end:

```
$ python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/design/factory-rules-debt.md
design/factory-rules-debt.md: not a script of scripts/, matched by keep `covers` and story folders only
design/factory-rules-debt.md: keep test_null_outcomes.py (layer gate_named, covers it)
$ python -B ai-packages/qa-factory/scripts/tests/test_null_outcomes.py   (tail)
PASS K0.16: one verdict reads as one word
=== test_null_outcomes: 327/327 ok ===
$ python -B ai-packages/qa-factory/scripts/tests/test_s1_s2_contract.py   (tail)
PASS G1-10: `none` is a manifest implementation source
=== S1-S2 contract: 67/67 ok ===
$ python -m pytest tools/test_piles_close_id.py -q -p no:cacheprovider   (tail)
.......                                                                  [100%]
7 passed in 2.86s
```

Own check (not a test): the file has no Cyrillic (`re.findall([Ѐ-ӿ])` -> `[]`); open rows counted by section under the edited file: run 5 = 8, FR-47..FR-57 table = 9, FR-59 = 15, FR-42 = 1, FR-7 = 1, plus the 3 "Found by this walk" entries = 37 (header says thirty-seven); "Real limits" = 3 rows.

## row id -> what changed

| row | change |
|---|---|
| header | "Twenty-five rows" -> "Thirty-seven rows", counts per table stated; line 7 points at "Real limits" |
| R1, R2, R4, R7, R9 | unchanged (not S1a) |
| R3 | "is grounding batch 2 (G2-2)" -> "landed in G2-2, release 0.10.8"; `skipped` sentence kept; `**narrowed` + `pending_implementation` wording untouched (E2) |
| R5 | NOT moved — see Question 1 |
| R6 | "53 pending today" -> "52" (measured: `len(null-outcomes.json["pending"])` = 52; the spec said S1 prints it); the four needles kept (E1) |
| R8, R11 | moved to "Fixed" with the §2 evidence |
| R10 | moved to new "Real limits" section whole, plus a why line |
| W2 | heading, "109" -> 221 (read `design/controller-blocks.md:21`); the sentence "walks all 189 refusals" made true: 189 on the day, 353 today (`controller-blocks.md:3`); "most of the 109" -> 221 |
| X2, X3, X11 | narrowed in place, row keeps only the residue with the §2 evidence; X11 gains "texts: words-gates/1 GW1-4" |
| X5, X6, X8 | moved to "Fixed" with the §2 evidence (FR-53, FR-54, FR-57 bullets) |
| X12, X13, X14, X15, X17, X18 | moved to "Fixed", one bullet each, text taken from the row's own "Closed by" part |
| X16 | unchanged (S1b/S6) |
| G1-G13 | "no unknown branch yet" -> the registry's declared branch (read from `gate-registry.json` rows with `status: debt`) + "conversion owed (T2, `gate_template.acceptable`)"; G4 keeps its collect-error residue |
| new row | `environment_property_cover` (debt B-283, `question`, wait at gate A) added; section text "Thirteen" -> "Fourteen" |
| G14 | moved to "Real limits" whole (Lead word F-L5 = real limit) plus a why line |
| G15 | unchanged |
| G16 | moved to "Real limits" whole plus a why line |
| N1 | "105 sites" -> 55 (`audit_factory.py:1716` `NO_MOVE_BASELINE_MAX = 55`); the named converting nodes are closed, no open node converts the 55 |
| P1 | "; node: words-gates/1 GW1-36" appended |
| X1, X4, X7, X9, X10 | unchanged |

Edges: E1 held (one `FR-23`+`FR-5` row, four needles; the FR-23 pilot row R5 stays, see Q1), E2 held (one `| FR-21 |` line, verified green), E3 (B-ids kept inside moved bullets: none of the moved rows names a B-id except through the text copied whole; no B-id invented), E4 n/a (no table emptied), E5 followed (moved, never deleted), E6 followed (no S2-S10 row moved).

## FR walk (sections touched)

- A, B, C, D, E, F (rules text) - not changed; this is a ledger of open rows, no factory-rules text edited.
- G / FR-30 - the file is in the package, English, no Cyrillic (checked above; `selftest.py --lang` judges at the canon).
- FR-26 - each moved row was closed against the carrier line the spec's §2 names; the spec's numbers 221 / 55 were re-read in `controller-blocks.md:21` and `audit_factory.py:1716` before writing; the pending count (52) and the 14 `debt` registry rows were measured, not copied.

## Deviations

- R6 count 53 -> 52 (spec said "S1 prints it from the test"; measured from `references/null-outcomes.json`).
- W2 line 45 also reworded ("189 ... 353 today"), because the spec's number change (109 -> 221) would otherwise leave "221 of 189".
- Moved X12-X18 bullets are long (they carry the row's "Closed by" text whole).

## Questions

1. R5 (FR-23, `story_run.delivery()`, the spec says CLOSE) is NOT moved. Reason: `test_null_outcomes.py:595-596` (K0.15 positive control) requires at least 2 lines starting with `|` that contain `FR-23`; today those are R5 and R6 only; moving R5 leaves 1 and the test goes red. The spec's E1 only protects the FR-23+FR-5 row. Options: (a) Lead lets the test control read a different known sample (a one-line edit of a test I do not own); (b) R5 stays as an open row that says "closed in code (`driver_stage_s8s9.py:370-379`), ledger line kept until the test control moves" (not drafted, a design decision). Left unimplemented; the open count includes R5.

## Needed beyond the manifest

- `ai-packages/qa-factory/scripts/tests/test_null_outcomes.py` (K0.15 control), `ai-packages/qa-factory/scripts/tests/test_s1_s2_contract.py` (`fr21_row_mismatch`), `ai-packages/qa-factory/references/gate-registry.json`, `ai-packages/qa-factory/references/null-outcomes.json`, `ai-packages/qa-factory/design/controller-blocks.md`, `ai-packages/qa-factory/scripts/audit_factory.py` (read only).

## Noticed, not widened

- Header line 10 "Entries are removed when the fix lands" contradicts line 7 (moved, not deleted); E5 settles in favour of line 7, the sentence on line 10 is left as is (not in the edit list).
- Spec §0 says G14/G16 verdicts; a trailing "Fixed" bullet group for X12-X18 duplicates detail kept in git history; fine.
