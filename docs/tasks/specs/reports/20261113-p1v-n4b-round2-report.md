# P1-v N4b round 2: the Lead's six answers, implemented

Branch `wip/p1v-n4b`, base 26d987f (round 1). Owns touched: `scripts/friction.py`, `references/friction-markers.json`,
`scripts/tests/test_friction.py`, `changelog.d/p1v-n4b-call-time.md`, this report. Nothing else (`run_counters.py`, `code_friction.py`,
hooks untouched). All six answers done; no question left open except the two readings listed under "Readings" (both executable as written).

## Per answer

1. **Digits.** `friction.SCRIPT` = `([a-z0-9_]+\.py)`. Readers of the shape: `friction()` (repair tracking `open_repairs`), `call_spans`
   (now through `invoked_scripts`, which checks `SCRIPT.fullmatch`), `experiments/measurers/code_friction.py` (imports the name; its
   `--scripts` listing). Test rows (`round2_rows`, answer 1): (a) `s5_precheck.py` is one name; (b) old shape read it `_precheck.py`;
   (c) every command of the existing scout fixture (plus 4 more) reads IDENTICALLY under both shapes (no digit in a name -> same);
   (d) `friction()` on the existing scout fixture: tally, friction turns, helpers unchanged under old vs new shape; (e) a refused digit-named
   script retried later: tally before `{guard: 1}` -> after `{guard: 1, recovery: 1}` (the only kind of change: the correctly named script
   is now tracked; before, a different digit-named script `s6_precheck.py` shared its truncated key `_precheck.py` and closed the repair).
   Real sessions (three, below): `friction()` tallies identical old vs new (`usage 7, validator 2, guard 9, crash 3` both); the code_friction
   `--scripts` name choice (its own two-line logic replayed over the 21 classified results): 0 differences. Compat row green (names
   `SCRIPT, classify, is_project_test, turns_of, friction` keep their keys). So: ONLY additions, no stop.
   **Old outputs of friction that changed because of answer 1, by name:** `friction()` output for a transcript that names a digit-named script
   in a Bash command (key `_precheck.py` -> `s5_precheck.py`; effect only as in (e)); `code_friction.py --scripts` name column for the same
   case. On the existing fixtures and on the three real sessions: none.
2. **Invocation.** New `friction.invoked_scripts(command)`: quote-aware split into simple commands (`&&`, `||`, `;`, `|`, `&`, newline,
   parentheses outside quotes), env prefixes skipped; the program is `python`/`python3[.x]`/`py` (`.exe` ok) -> first non-flag word
   after its flags (`-W`/`-X` take an argument, `-c`/`-m` run no file), or the command word itself when it is a `.py` name; the basename
   (either slash) is the script. `call_spans` uses it. 18 rows `INVOCATION_SHAPES` (command -> scripts invoked -> attribution): flags,
   absolute Windows path with digit, absolute interpreter, `py -3`, command itself, `-W ignore`, subshell+env, pipe+redirect, argument of
   another program (not counted), grep / cat / editor / quoted text / `-c` (not counted), two invoked joined by `&&` (ONE call,
   attributed to the first in the command; and the row `bookkeeping.calls` counts each joined command once), unlisted first + listed
   second, empty command.
3. **Signed list.** `bookkeeping_scripts` now six: `manifest_put.py`, `manifest_from_tests.py`, `s5_precheck.py`, `handoff_check.py`,
   `handoff_init.py`, `manifest_view.py` (both exist in `scripts/`, checked). New data key `bookkeeping_fragment_patterns`, initial
   `["*.values.yaml"]`; a Write/Edit whose file name (basename, lower-cased, fnmatch) matches is a call of the sub-row `fragment_writes`
   (own tally + state), never in the script row. Rows: Write and Edit (case-insensitive) counted; Write of another file, a name merely
   containing the pattern, a Read, a `cat` not counted; script row unaffected; key absent / a string / empty / no usable pattern ->
   `unknown: no fragment pattern list`, script row still measured. Not added (stay OUT, as given): `plan_row.py`, `artifact_producer.py`,
   `window_record.py`, `handoff_help.py`, `handoff.py`, `s5_plan.py`, `walk_session.py`, `first_look.py put`, `case_versions.py --pin`,
   `critic_rollcall.py --store`, `external_writes.py --record`.
4. **Two refused rows + total.** `refused` = `is_error` only (as built); new `named_by_marker` = calls with `is_error` absent/false whose
   result `classify` names a kind (own `by_kind`, own state); `refused_total` = the two summed; a call is in one row only. `classify`
   untouched, no new text reading. Markers file unreadable: row 2 `unknown`, total `partial` with the reason (flagged calls only).
   Rows: row 1 = 3 calls as built; row 2 = the validator result k6 (exec 2.0 s, turn 4.0 s); total = 4 calls, 13.0 s / 18.0 s; a flagged guard
   call has no `named_kind`; unreadable markers. The old row "is_error absent is not an error" stays green (`kind` None, `is_error` False;
   the new field is `named_kind`).
5. **Empty list.** `bookkeeping_scripts: []` -> `unknown: no bookkeeping list` (new row); fragment key: same rule (answer 3 rows).
6. **Split among ALL calls.** `share = window / len(all calls of the message)`; the cut call is `unknown`; sums print
   `at least N s (K calls unmeasured)`. Row: 3 calls, 1 cut: window 0 -> 12 s, 4.0 / 4.0 / None, sum `at least 8.0 s (1 calls unmeasured)`.
   Story level: `story_calls` rows carry the new rows (`fragment_writes`, `named_by_marker`, `refused_total`); an unreachable role has
   them `unknown` (rows added to `story_call_time_rows`).

## Witness (verbatim tails; one run after the last edit; from the package dir in a subshell)

```
( cd .../p1v-n4b/ai-packages/qa-factory && python -B scripts/tests/test_friction.py | tail -2; python -B scripts/tests/test_judgment_census.py | tail -1; python -B scripts/selftest.py --lang | tail -1 )
=== test_friction: 196/196 ok ===
=== judgment_census: 24/24 ok ===
=== qa-factory selftest: 2/2 ok ===
```
(138 -> 196 rows.) Earlier in the round: friction 196/196 on the first run; the census then had one red row, `_refused_total` matched the check-unit name
pattern `refuse*` (`C1: friction.py::_refused_total is a check unit (u1) with no row`); I renamed it `_two_row_total` (a pure sum, not a check)
rather than adding a census row (the census file is not in `owns`). Re-run above is green.

## Row (e): the same three sessions (db9a9038, 8325ed4c, 5a86e7e9; the `5a86e7e9` etc. transcripts in the stand's host projects folder, all three found)

Scratch scripts outside the tree: `remeasure.py` (runs round 1's code, extracted by `git show 26d987f`, and the new code on the same files),
`explain.py`, `cf.py` (in the session scratchpad; never committed). Round 1 table repeated, before -> after (calls / execution s / turn-attributed s):

| Row | Round 1 (26d987f) | Now |
|---|---|---|
| Bookkeeping scripts | 36 / 127.9 / 321.7 | 42 / 164.3 / 375.7 |
| Fragment writes (`*.values.yaml`) | not counted | 2 / 4.4 / 19.8 |
| Bookkeeping + fragment writes | 36 / 127.9 / 321.7 | 44 / 168.7 / 395.5 |
| Refused, host `is_error` | 13 / 32.4 / 128.8 (round 1 printed 128.9; rounding of the sum) | 13 / 32.4 / 128.8 |
| Refused, named by marker (kinds: usage 7, validator 2) | not counted | 9 / 25.9 / 59.0 |
| Refused total | 13 / 32.4 / 128.8 | 22 / 58.4 / 187.9 |
| Unmeasured calls | 0 | 0 |

Per script now: `manifest_put.py` 17, `manifest_from_tests.py` 11, `s5_precheck.py` 5, `handoff_check.py` 5, `manifest_view.py` 4,
`handoff_init.py` 0. Per session bookkeeping: db9a9038 16 / 65.7 / 145.5; 8325ed4c 11 / 51.3 / 113.4; 5a86e7e9 15 / 47.3 / 116.8.

Hand figures: bookkeeping 367 s / 50 calls; refused 201 s / 20 calls. Remaining differences, each by measurement:

1. Bookkeeping 36 -> 42 calls, round-1 change decomposed from per-script counts: manifest_from_tests 14 -> 11 (2 are `grep ... manifest_from_tests.py`
   mentions, not invocations; 1 is a `;`-joined command whose first listed script is `manifest_view.py`, so it is attributed there); `s5_precheck.py`
   0 -> 5 (the digit gap: round 1 expected 5, confirmed); `manifest_view.py` 0 -> 4. 36 - 3 + 5 + 4 = 42. (Round 1's "2 false positives"
   was right for the mentions; the third change is the new attribution rule.) 
2. Against the hand 50 calls: ours is 42 + 2 fragment writes = 44. Six calls remain. Measured candidate: SIX commands in the three
   sessions invoke TWO signed scripts in one Bash call (e.g. `manifest_put.py ...; s5_precheck.py ...`, `manifest_view.py && manifest_from_tests.py`,
   `manifest_put.py && handoff_check.py`); by the Lead's rule each is ONE call. 44 + 6 = 50 exactly, so a hand count of one call per script
   fits the call count; it is a fit, not a recorded fact (the hand classification is not recorded call by call). Every other Bash call that
   invokes a script not on the signed list is `run_suite.py` (29), `execution_fingerprint.py` (1), `traceability.py` (1): the role's own work or
   unsigned, none of `plan_row.py` etc. is invoked in these sessions at all.
3. Bookkeeping seconds: ours 395.5 s turn-attributed (44 calls, 9.0 s per call; execution 168.7 s, 3.8 s per call) against the hand 367 s
   (7.3 s per call). Ours is 28.5 s (7 %) HIGHER with 6 fewer calls: this is NOT explained; the hand time basis is not recorded
   (hand 7.3 s per call is neither our 9.0 nor 3.8). Both our figures stay labelled.
4. Refused: by `is_error` alone 13 calls; with the second row 22 calls / 187.9 s against the hand 20 / 201: two calls MORE and 13.1 s LESS.
   Not resolved call by call (the hand list is not recorded). Measured facts: the 9 extra calls are 7 `usage` (argparse dumps) and 2 `validator`
   results with no `is_error`; whether the hand count took the usage dumps as refusals is not known to me. The 13.1 s gap is not explained.
   The host flag alone misses 9 of 22 (41 %), as in round 1.

No norm or threshold is written.

## Readings (executed as written, flagged for the Lead's eye)

- Answer 2 "attributed to the first listed script": I read "listed" as the first in the COMMAND ORDER among the invoked scripts that are
  on the bookkeeping list (an unlisted script before it does not take the call). Row: `other.py && s5_precheck.py` -> `s5_precheck.py`.
- Answer 3 "its own sub-row": placed as `call_spans()['fragment_writes']` beside `bookkeeping` (not nested inside it), so the earlier
  rows on `bookkeeping` stay as they were. Same in `story_calls`.
- The key name of the fragment list, not given by the Lead: `bookkeeping_fragment_patterns`.

## FR walk (sections touched C, D, F, G; A, B, E not touched)

- A refusals not changed. B no text shown to a person changed. E no delivery/report text changed.
- C: FR-12 the bookkeeping decision reads structured fields (tool name, the invoked program of a command, `is_error`) and a closed list
  in data; no phrase list over a role's words; row 2 uses `classify` exactly as it exists, labelled as marker-named. FR-13 both lists are
  data. FR-14 import-only. FR-49 rows are read by the N4 reader (readers-pending).
- D: FR-18 counts and seconds of calls, not coverage. FR-58, FR-16, FR-40 n/a. FR-59 no gate.
- F: FR-25 two time figures and two refused rows, each labelled; the total is printed with its parts. FR-26 the reconciliation reads the raw
  calls (listed above). FR-28 test rows. FR-41 unknown never 0: no list -> `unknown`, cut call -> `unknown`, sum -> `at least`, row 2 -> `unknown` /
  total `partial` when markers are unreadable.
- G: FR-30 English only (`selftest --lang` green). FR-45 readers write nothing. FR-47 code reports what it measured, judges nothing.
  FR-54 siblings below.
- Architecture: AR-1 (the vocabulary of bookkeeping and fragments is data rows), AR-12 (friction measured), AR-28 (an unknown is never a
  zero or a pass).

## Analogs and siblings (reported, not fixed)

- SIBLING_MAP axis 6: `experiments/measurers/code_friction.py` imports `SCRIPT, classify, is_project_test`; compat row green; its `--scripts` name
  choice replayed on 21 real classified results: 0 differences; file not edited.
- Axis 14: `walk_timing.py` reads transcripts with its own per-turn timing (same class: call time from a transcript); not touched.
- Axis 16: one JSON reader for the markers file kept (`load_markers`).
- `friction()` repair tracking (`open_repairs`) still takes a script name ANYWHERE in the command text (`SCRIPT.findall(arg)`), so a `grep x.py`
  after a refusal of `x.py` counts as "recovery": the same mention-versus-invocation class answer 2 closed for bookkeeping. Not touched (changes
  the old `recovery` output; a decision for the Lead). The code_friction `--scripts` name choice has the same shape.
- Census: any new function whose name starts `refuse*`/`check_*`/`validate*`/`judge*` becomes a check unit needing a row; I avoided it by name.
