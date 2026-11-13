# P1-v N4b fix round (after the code critic, fit_with_fixes B1-B3)

Worktree `.claude/worktrees/p1v-n4b`, branch `wip/p1v-n4b`, from tip d8b86a6. Files: `scripts/friction.py`, `scripts/tests/test_friction.py`,
`changelog.d/p1v-n4b-call-time.md`, this report. `hooklib.py`, `run_counters.py`, `test_retro_numbers.py`, `references/` data: not changed.

## B1 - one shell reader (axis 11): fixed at friction.py `_command_words` (:283), `invoked_scripts` (:303)

- `friction._segments` is deleted. `_command_words` = `hooklib.cut_bodies(text, hooklib.scan_bodies(text))` then `hooklib.command_segments(cut, "bash")`.
  Only the program-position rule stays in friction (interpreter -> first non-flag word; `-c`/`-m` run no file; env assignments skipped).
- DEVIATION from the verdict's wording (measured): words are taken as `Word.clean` / the plain str, NOT through `hooklib.cleaned_word`. Probe:
  `python3 "C:\pkg dir\scripts\s5_precheck.py"` gives the word `C:\pkg dir\scripts\s5_precheck.py` raw but `C:pkg dirscriptss5_precheck.py` through
  `cleaned_word` (its strip table deletes backslashes), which would lose every Windows-path call. The reader has already removed the quotes.
- Wrappers (`timeout`, `env`, `sudo`), `bash -c` payloads and `$PY x.py`: NOT read. `launch-causes.json` `wrappers` holds only package runners
  (poetry, uv, npx ...), not timeout/env/sudo, so it is not the data the verdict thought. Named in `CALL_TIME_METHOD` as "not read, so a count is a
  floor"; a test row pins `timeout 120 python scripts/manifest_put.py` -> not read. Question for the Lead, if the floor is not enough: which class
  to read (needs a data list of wrapper programs, a new key).
- Rows added to `INVOCATION_SHAPES` (test_friction.py): heredoc body naming scripts (not counted); apostrophe in a body then a real call
  (counted); real call with `--file ... --fix` after a heredoc; quoted absolute path with spaces after a heredoc; a command that is only a heredoc;
  nested quotes; a 20000-word command; the wrapper (not read). The empty command row was already there.
- Re-measured on all 82 stand transcripts: 170 Bash commands that python-invoke a listed script, the new reader misses 0 (the old one lost 4).

## B2 - the "named by marker" row removed (Lead's decision)

- Deleted: `named_by_marker` row, `named_kind` per call, `refused_total`, `_two_row_total`, `NO_MARKERS`, their fold lines and tests. Refused = the
  host's `is_error` flag only. The call dict has no `named_kind` key; `call_spans` keys are bookkeeping, calls, fragment_writes, method, refused.
- "The markers data key and its reader": the row had NO key of its own; it used `classify` over the existing marker keys, which `friction()` still
  needs. So there was no dead key to delete. Grep of `named_by_marker|refused_total|named_kind|NO_MARKERS|_two_row_total|_empty_rows` over
  `ai-packages/qa-factory`: no hit in friction.py, the tests or the changelog now (positive control: the same grep found them in test_friction.py
  and the changelog before the edit, and `"fragment_patterns"` in the tests).
- Test rows: a voluntary `--help` call (argparse usage text, no flag) and a `tail` result with the role's own "is refused" test title are not
  refusals; only the flagged call is; the `k6` refusal-shaped result with no flag has `kind None`.
- Correction of the round-2 report (`...round2-report.md` :95-98 and the reconciliation row 4): the statements "22 calls ... two MORE" and "the host
  flag alone misses 9 of 22 (41 %)" are WITHDRAWN. Measured: 13 host-flagged refusals against the hand 20 (7 UNDER); the 9 row-2 calls were 9
  non-refusals (7 voluntary `--help`, 2 role-written text); the hand basis of the 7-call difference is unknown. No norm written.

## B3 - unreadable role session is unknown

- `_rows(readable, book, frag)` is the one row constructor (also removes the N3 duplication): bookkeeping, fragment_writes, refused all carry a
  `state`; an unreadable transcript gives `unknown` with `NO_TRANSCRIPT` ("unknown: no session could be read") for all three. `call_spans` marks
  `refused` measured when readable. `story_calls`: a role with no readable session has `calls: None` (the total likewise until one is read).
- "Readable" = at least one line parses as a user or assistant record (`_readable`). Four shapes, one test row each
  (`unreadable_role_sessions_are_unknown_and_a_true_zero_is_zero`): absent, empty file, torn file, open fails (OSError, the open is patched to fail
  because chmod is not reliable on Windows) -> all three rows `unknown`, calls None; the story is `partial`. A readable transcript with a Read
  call only: calls 1, all three rows `measured` 0. `call_spans` straight on an empty and a torn file: all rows unknown, no calls.
- `_Unreadable` (empty/torn) is caught in `_walk_sessions` beside OSError, so such a session is "unreachable" with its reason, as in `story_friction`.
- `_fold` keeps the reason of an unknown part (a missing list says so, not "no session could be read").
- No printer exists yet: nothing prints `n/a` from these rows (N1, below). The reason strings use the package's `unknown: ...` form.

## Non-blocking

- N1: the commit message line `AR-22 -- new keys have a reader` of 26d987f is FALSE: no package code calls `story_calls`, `call_spans` or `seconds_text`
  (run_counters T9/T10 stay `unknown`, :636). This fix commit says AR-13/AR-15/AR-28 and does not repeat it. The wiring node ("run_counters T9/T10
  read `friction.story_calls`") is the Lead's to open after N4b merges (owns run_counters.py, test_retro_numbers.py).
- N2: kept as labelled; `CALL_TIME_METHOD` now says "(Write and Edit only: a fragment written by a Bash redirect is not counted)". The Lead decides
  whether Bash redirect writes join (11 of 39 on stand data).
- N3: fixed. `call_spans` split into `call_spans` + `_classify_call` + `_rows`/`_row`; one constructor for the rows of `call_spans` and `story_calls`.
- N4: fixed. The loader key is `bookkeeping_fragment_patterns` (the file key); the test line follows.
- N5 (the `open_repairs` / `classify` mention-vs-invocation sibling): the verdict's answer 4 says queue, not this node. Left as is, listed:
  `friction()` `open_repairs` (`SCRIPT.findall(arg.lower())`) and `classify` tagging `--help` as `usage` and the role's text as `validator`. Old
  outputs of `friction()` unchanged. Node text is in the verdict N5; the Lead places it.

## Changed expected values (old -> new)

- test rows only: `calls` of an unreachable role 0 -> None; the "second refused row and total line" rows (named 1, total 4) removed -> replaced by
  rows saying the role has bookkeeping, fragment_writes and refused only; `shipped["fragment_patterns"]` -> `["bookkeeping_fragment_patterns"]`.
  No old output of `friction()` or `story_friction` changed (the compat rows are green).

## Row (e), the three automator sessions db9a9038, 8325ed4c, 5a86e7e9 (calls, execution s, turn-attributed s)

| row | before (d8b86a6) | after |
|---|---|---|
| bookkeeping | 42 / 164.4 / 375.7 | 42 / 164.4 / 375.7 |
| fragment writes | 2 / 4.4 / 19.8 | 2 / 4.4 / 19.8 |
| refused (is_error) | 13 / 32.4 / 128.9 | 13 / 32.4 / 128.9 |
| named by marker | 9 / 25.9 / 59.0 | row removed (9 non-refusals) |
| refused total | 22 / 58.3 / 187.9 | removed |

Hand figures: bookkeeping 50 calls, refused 20 calls: refused is 7 under, not 2 over (see B2 correction).

## Siblings (axis 11: private shell readers still in scripts/, listed, not changed)

Grep `def _?(segments|tokenize|split_command|shell_split|_split_segments)|shlex.split` over `scripts/*.py` (positive control: finds
`guard_pre_tool._segments`, the known B-434 one): `guard_pre_tool.py:198 _segments`, `test_locations.py:153 _segments`; `shlex.split` command
readers in `execution_request.py:751`, `gate_preflight.py:457`, `guard_app_under_test.py:391`, `manual_capture.py:1228`, `readiness.py:124`,
`stage_guard.py:2362,2387,2480`, `stand_access.py:185`, `stand_identity.py:673`. Not judged here whether each reads a shell command or a config
string.

## Architecture and judgment (commit lines)

AR-13 (a command's words are read only through hooklib's reader), AR-15 (the heredoc-body scan is the one `scan_bodies`), AR-28 (an unreadable
session and a missing list are unknown, never 0). judgment: none -- code counts structured fields (tool name, invoked program, `is_error`), no
word list over a role's text; the row that applied `classify` to unflagged results is deleted.

FR walk: A, B, E not touched. C: FR-12 now no phrase match over unflagged text; FR-13 lists stay data. F: FR-41 unknown never 0 (B3). G: FR-30
(selftest --lang green), FR-45 readers write nothing, FR-54 siblings above.

## Witness (package dir, one run per round, summary lines)

```
( cd .../p1v-n4b/ai-packages/qa-factory && python -B scripts/tests/test_friction.py | tail -1; ... test_retro_numbers.py | tail -2; ... test_judgment_census.py | tail -1; ... selftest.py --lang | tail -1 )
=== test_friction: 220/220 ok ===
=== test_retro_numbers: 289/289 ok ===
=== judgment_census: 24/24 ok ===
=== qa-factory selftest: 2/2 ok ===
```

Needed beyond the manifest: `scripts/guard_pre_tool.py`, `launch-causes.json` (read for wrappers), SIBLING_MAP axis 11 listing via grep.
