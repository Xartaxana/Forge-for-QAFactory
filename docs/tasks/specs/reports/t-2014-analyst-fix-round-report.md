# t-2014 report - fix round on analyst nodes U1, U2, U3a (critic verdict t-2010)

Branch `afix` in `D:/ws2/wt-fb4`, one commit `ed0045010` on top of `ec7e3c536`, not pushed. Trailer and the `architecture:` / `judgment:` / `piles-skip:` lines are in the message.

## Per finding

| Finding | State | What changed | Red line before the fix (test, reason) |
|---|---|---|---|
| F1 | DONE | `place_answers.write`: a `bug` answer withdraws the active line only when `settled_answer` says `settled` now; `close_unsettled` withdraws the active line of a place already settled as `bug` (owner check, `printed` names it); a chain already withdrawn and unsettled again takes its gap under `place-gap-<id>` (data row `gap_target_prefix`) | `test_replace_to_bug_with_void_receipt_keeps_the_question_until_the_gap`: `assert ('EX-2' is None)`; `test_withdrawn_chain_unsettled_again_still_gets_a_gap_line`: printed only, `gap` None; `test_close_withdraws_the_line_of_a_bug_settled_after_the_write`; `test_walk_receipt::test_replace_to_bug_with_a_void_receipt_leaves_a_register_line` |
| F2 | DONE | `and old` dropped (same change as F1a) | `test_first_bug_answer_corrects_a_stale_gap`, `test_walk_receipt::test_first_bug_answer_after_a_gap_leaves_no_stale_gap`: stale `coverage_gap` still active |
| F3 | DONE (U1 owns widened by one clause, as the verdict says) | `investigation.project` skips a target whose `settled_answer` is `settled` (helper `_settled_by_analyst`; a reader that raises asks as before) | `test_investigation.py key_project_skips_settled_bug`: `FAIL F3 the settled target has no register line and is skipped` (run in a clean worktree at `ec7e3c536` with the new test file, 259/260); `test_place_answers::test_project_skips_a_place_settled_bug` |
| F4 | NOT DONE, non-goal (U4 holds `gate_brief.py`) | see "For F4" below | - |
| F5 | DONE | (1) state `open`/`invalid` with source `open` is skipped; (2) a line of another owner (not the close, not `code:`, not the answering dispatch) is named in `printed`, never corrected; (3) a `correct` keeps `question`, `owner_role`, `oracle_status`; (4) `settled_answer` checks `conflict` before the line check (also before the writer check) | `test_open_place_with_a_draft_keeps_the_investigation_question`, `test_close_never_corrects_a_line_of_another_owner`, `test_conflict_twice_writes_one_line_and_keeps_the_question` (second close wrote a line / state flipped to `carrier missing`) |
| F6 | DONE (code part) | `_confirmation` in `place_answers`: a draft with no `confirmation` word is `unconfirmed` for the list and the conflict join; a `bug` answer on it reads `carrier missing` with the door "write `confirmation: unconfirmed`" (data row `line_texts.no_confirmation`). Contract default (`contract.bug_confirmation`) untouched: queued for the Lead | `test_draft_without_confirmation_is_a_place_with_a_door` |
| F7 | DONE in code; SPEC text open | door is "answer `bug`, or record the question under a new place `new-<slug>`" | `test_withdrawn_chain_replace_refused_with_door`: `'impossible' is contained here` |
| F8 | DONE | `_records` returns `(records, unreadable)`; `places` adds unreadable record files (unparseable or naming no place) to `unreadable` | `test_corrupt_record_of_a_new_place_is_unreadable_not_none` |
| F9 | DONE | `bug_records.reproduction_problems`: a walk entry on a non-code-reading draft with no readable run report reads `R_NO_REPORT` | `test_walk_receipt::test_walk_without_a_readable_report_void_except_code_reading` (stayed `reproduced_by_factory`); the code-reading draft still lifts with no report |
| F10 | DONE | `story_run.s7_place_lines`: one line with the keys of the answer file (`expectation`, `seen`, `question`/`why`/`draft`, the walk entry form) and the capture command carries `--task-root`, `--steps-file` (ui), `--method`/`--url` (http) | `test_place_driver::test_brief_names_places_and_answer_keys` (clean worktree: `AssertionError: \`expectation\` {...}`) |
| F11 | DONE | `_answer_lines`: when the controller state reads and holds dispatches, an unknown `--dispatch` is refused with a door; an unreadable state locks nobody | `test_unknown_dispatch_refused_when_the_story_state_reads` |
| F12 | DONE | `scribe_line_max` data row (Q5), `.get(...,1500)` gone; removed dead `capture_optional`, `new_slug_pattern`, `STATES`; `s7_gap_reason` picks by name (`gap_reason_names`, pinned equal to `gap_reasons`); `write` computes `places` once | `test_data_rows_and_no_dead_names` |
| Q4 | DONE | `test_story_run_s7.py`: five exact-list pins gain `Places to settle: none in this run` (constant `NO_PLACES`). Not run (slow file), edited by reading | - |
| F13-F15, F16-F17 | not touched (SPEC / queue) | - | - |

All red lines were taken from one run of the new tests on the unfixed source (16 failed of 79 in the two files) plus a clean worktree at `ec7e3c536` (removed afterwards) for the two files written after that run. No byte-copy rollback was needed: nothing was corrupted, the fix was written after the red run.

## Witness (verbatim)

```
python -m pytest -p no:cacheprovider .../test_place_answers.py .../test_walk_receipt.py .../test_place_driver.py -q --no-header --maxfail=40
........................................................................ [ 80%]
.................                                                        [100%]
89 passed in 114.90s (0:01:54)

python -B .../test_investigation.py
PASS F3 the settled target has no register line and is skipped
PASS F3 the other targets are projected as ever
PASS F3 a reader that raises asks the question as before
PASS the fixture tree is byte-identical after the run (no test wrote it)
=== test_investigation: 260/260 ok ===

python -B .../test_judgment_census.py
=== judgment_census: 21/21 ok ===

python -B .../test_driver_layers.py
=== test_driver_layers: 52/52 ok ===
```

Red controls (before the fix): `FAIL F3 the settled target has no register line and is skipped` / `=== test_investigation: 259/260 ok ===`; `FAIL test_brief_names_places_and_answer_keys` / `test_place_driver: 9 passed, 1 failed`; first red run `16 failed, 63 passed in 103.02s`.

The pre-commit hooks passed (factory rules index, architecture index, AGENTS.md). The first commit attempt was refused for a `judgment:` line without ` -- <why>`; the message was fixed, nothing else.

## For the Lead

For F4 (gate_brief.py, U4's file): at `gate_brief.py:4336` the branch must be `if row.get("code_reading") and row.get("confirmation") != "reproduced_by_factory":` so a lifted code-reading draft falls to the `elif` and prints `BR.reproduction_words(row)`; keep the oracle and code lines at `:4344`. Test beside the one that pins t-1676's text.

SPEC items done by the verdict's direction, listed for you: F3 (extends U1 owns by the `project` clause), F6 (code part: absent word is a place; the contract default queued), F7 (code; §3.2 of spec t-1991 must drop `impossible` from the withdrawn-chain door), Q4 (pins follow; U3b's owns must list `test_story_run_s7.py`), Q5 (data row). No SPEC item needed a choice between directions.

Choices I made inside the verdict's directions, so you can overrule them:
- The "line of another owner" rule: foreign = not `code:place_answers.close_unsettled`, not a `code:` line, not the dispatch of the place's record. A person's own line (`person`, `person:...`) is therefore foreign and is named, not rewritten, in every state.
- Withdrawals the close makes are reported in `printed`, not in the returned ids (the driver prints "N place(s) ... recorded as coverage gaps" from `len(written)`).
- `gap_reason_names` duplicates the five texts of `gap_reasons` as a name map; a test pins the equality. `gap_reasons` stays a list because `why` is validated against it and tests index it.
- A record file that names no place is listed as unreadable too (not only unparseable ones).

Not touched, noticed: `tests/fixtures/driver-layers.json:641` note still says "texts 4/5 by kind, 2/3 from state" (text only; the row is valid). `s7.md` / the charter still owe the new `place-gap-<id>` target and the brief line (U4).

Needed beyond the manifest: `investigation.py` (the `project` site, the verdict allowed it), `story_run.py` `s7_place_lines`, `exploratory_findings.py` (`append`, `target_of`) and `tests/fixtures/` listing for the red-control worktree.
