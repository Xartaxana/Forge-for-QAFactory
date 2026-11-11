# t-2028 - fix round 2 on the analyst's later nodes (verdict t-2027)

Builder (Sonnet), 06.11.2026. Tree `D:/ws2/wt-fbfix`, branch `fb-fix`. No push. Commits: merge `c3531ff17` (au2b, `--no-ff`, the lines as dispatched) and fix `bc1ab486b`. Temp stories only; no stand, no `tr-walk`, no lease; no browser. Final test tree clean except the commits.

## Per finding

| F | State | What | Test (red before the fix) |
|---|---|---|---|
| F1 | DONE | `story_run.py walk_reopen` answers `([], "")` for a record whose `place` is not `case`; `walk_session.open_walk` writes `place` in its "opening" record | `test_place_session.py::test_settle_record_is_no_case_walk_on_any_road` (REAL `walk_reopen`, the rig's stub deleted per test; resume, continuation, saved result, control record, case record still a case) red: case `open` without `--place`, `walk_after` lanes over place ids; `::test_failed_open_leaves_the_place_in_its_record` red: `place` None |
| F2 | DONE (pin follows the charter) | `test_charters_s5_s9.py:61` key is now `the factory derived itself is no requirement` (the charter's words since `fa688b70d`); role-load margin untouched by this choice | red at head per the verdict (`1 failed, 58 passed`); green now `59 passed` |
| F3 | DONE (SPEC direction taken: the verdict's recommendation) | `place_answers._person_list`: for source `person` an EMPTY `expectation.id` reads the quote against the dispatch's `request_binding.reason`, `person_words` mark still required, an empty reason refused; a GIVEN `id` is still checked as a file under `state/words/` as before; the Commands row says "empty for source person: the quote is read against your dispatch's reason" | `test_place_answers.py::test_person_bug_with_no_words_path_checks_the_dispatch_reason` red: "`expectation.id` '' is no file under state/words/" |
| F4 | DONE | `walk_session.Walk.dispatch`: `StandHeld` on `close` runs `op_close(probe=False)` (note "closed while the stand was held by another job: the end probe was not taken") instead of `stand_busy` | `test_walk_places.py::test_close_under_a_held_lease_still_closes` red: `(3, 'stand_busy', 'ready')` |
| F5 | DONE | `role-commands.json` reopen row: `--items <the items your brief's session line names>`; the `s7_settle_session` docstring too | `test_place_session.py::test_walk_card_rows_for_the_analyst` (byte-copy control: HEAD's json restored -> `assert 'qa-failure-analyst' in ['qa-runner']`; file restored, sha256 equal) |
| F6 | DONE | the session line's reopen door passes `--parent-pid {os.getpid()}` (the driver) | `test_session_line_carries_the_driver_pid_and_the_step_flags` red before the line change |
| F7 | DONE | `qa-failure-analyst` added to `walk_session.py step|look|final|status` rows (`verdict`, `item`, `done` stay out); their `--item` reads `<case id, or your place id>`; the session line names `--line "<one step>"` / `--steps-file` | same two tests |
| F8 | DONE | `Walk.takes_new_item`: a settle or control lane takes any plain id later (`lane_item_ok`, the one test shared with `open`), appended to `items`; a case lane still refuses; the refusal names `manual_capture.py`; a settle lane writes a timing line per item at `close` with ITS place (before: no line at all for settle, `PLACE="case"` constant only for case verdicts) | `test_walk_places.py::test_settle_lane_takes_a_new_id_and_times_its_own_place` red: `(2, 'refused')` |
| F9 | DONE | `s7_settle_session` opens the ids that pass `lane_item_ok`, records the rest as `skipped`; the brief gets a second line naming them with the `manual_capture.py ... --case settle-<place id>` road | `test_odd_place_id_does_not_lose_the_session` red |
| F10 | DONE | `place_answers.close_unsettled`: a settled place's active `place-gap-<id>` line written by `by_close` is withdrawn (a printed line says so) | `test_place_answers.py::test_gap_under_place_gap_is_withdrawn_once_the_place_is_settled` red: the line stays active |
| F11 | DONE | `open` answers a closed `cause` (`stand_busy` from `StandHeld`) in the JSON and the walk record; the driver classes `stand` by `cause`, not by `"stand" in why.lower()`; `why` is the answer's `reason` | `test_session_failure_recorded_for_gap_reason` (a reason "cannot understand the layout of /stand/x" with no cause -> `session`) red; `test_open_under_a_held_stand_says_the_cause` on the walker |
| F12 | DONE | the second copy of the saved-result block in `run_role` deleted | `test_saved_result_retired_once_in_run_role` red: `[1, 1]` |
| F13 | DONE | charter Tools: `publication.` and `- Verdict words` split; trailing newline restored | no test (the file's text only); read |

## U4's cuts (the Lead asked)

- The two-readings line is BACK in "When to ask", shortened to `Two readings both tenable: one question with both quotes, and go on.` (the clause "evidence cannot separate them" is not carried; it dropped 33 B). Paid by two cuts of the same kind (text a role cannot act on or that an injected text repeats): the Tools clause `a withdrawn place unsettled again is gapped as place-gap-<id>` (the verdict's own item) and the Tools lead-in `Any of these (arguments: your brief's Commands card); none is required.` -> `Optional (arguments: your brief's Commands card).`. Process tokens now 15,996 (row was 15,999); the total 17,743 (row 17,751); BOTH ROWS LOWERED in `role-load.json` (process 15,999 -> 15,996, total 17,751 -> 17,743). No raise. NOTE for the Lead: the restored line and Techniques "When both readings are tenable, the product bug is the default" are again the clash the verdict named (it said the cut removed it in favour of `bug`); the brief form (`brief-form.json`, `questions`) carries the same two-readings sentence and reaches the analyst either way. A choice between the two is the Lead's.
- `faq.md` pointer: NOT restored in the charter. It is a pointer the role has: `brief-form.json` `qa-failure-analyst.questions` says "settle it yourself first (faq.md, ...)" and `brief_pack.py:93` / `inject-map.json:93` inject `strategy/faq.md` for the analyst, so the brief carries it. (The verdict's "grep: none" read the charter and slices, not the brief form.)
- The false quarantine claim: confirmed false. `grep -ril quarantine` over `agents/` and `references/` finds it in the bug-reporter, the run contract (full, not the analyst's slice), metrics, null-outcomes - NOT in `references/slices/qa-failure-analyst/` and not in the analyst's charter. The `fix_result: fixed | not_fixed` words stay in the analyst's slice (`artifact-contract-run.md:51`). I did not restore the sentence and did not edit the t-2012 report (not owned); the claim line stays as the critic named it. Lead's call whether the sentence returns.

## Pytest-only files (F2 class), one run each, `timeout 120`, `-p no:cacheprovider`

All 13 passed; none over two minutes (longest `test_exit_limit_halt_answered` 76 s). `test_charters_s5_s9` 59 passed (it was the red one, now fixed).

```
test_charters_s5_s9 59 passed in 0.75s      test_charter_form 17 passed in 2.53s
test_exit_gate_advice 9 passed in 4.87s     test_exit_limit_halt_answered 13 passed in 76.36s
test_handoff_init_author 35 passed in 11.15s  test_open_list_fields 15 passed in 4.66s
test_open_vocabularies 58 passed in 4.45s   test_probe_gap_door 33 passed in 22.46s
test_probe_target_fact 12 passed in 2.96s   test_rework_dispatch_files 3 passed in 16.89s
test_rows_owed 7 passed in 4.63s            test_stage_review_person_pass 29 passed in 12.41s
test_walk_charter 9 passed in 1.18s
```
The class fix (a script entry in each, or `selftest` refusing a file that ran nothing) is NOT done: non-goal, queued for the Lead.

## Witness (final run, after the changes; verbatim)

```
== pytest test_place_session      18 passed in 23.89s
== pytest test_place_driver       10 passed in 38.94s
== pytest test_place_answers      60 passed in 57.75s
== pytest test_walk_places        15 passed in 10.83s
== pytest test_walk_oracle        10 passed in 6.60s
== pytest test_walk_session       22 passed in 15.00s
== pytest test_charters_s5_s9     59 passed in 1.83s
== script test_audit_rules        === audit rules (A1/A9/A11/A13/A14/A17/A20/A21/A22/A27): 328/328 ok ===   exit 0
== script test_judgment_census    === judgment_census: 21/21 ok ===   exit 0
== script test_driver_layers      === test_driver_layers: 52/52 ok ===   exit 0
== script test_role_commands      === test_role_commands: 703/703 ok ===   exit 0
== script test_role_load          === role_load (the one measure of a role's start load): 165/165 ok ===   exit 0
== lint_ratchet                   lint ratchet: 29 findings, 29 in the baseline, 0 new, 0 stale (pyflakes 3.2.0)   exit 0
```
`python -B role_load.py --role qa-failure-analyst --json`: `tokens 17743, process_tokens 15996` (rows 17743 / 15996 after the lowering). Not run (slow, CI's): `test_story_run_s7`, `test_story_run_*`.

## Deviations, decisions made (flag for the Lead)

1. Order of red lines: for F5/F7 (data) the rows were edited before their test was written; the red was shown afterwards with a byte-copy control (HEAD's json, restored, hashes equal). F13 has no test.
2. F3 given-`id` path kept (a path that IS given is still validated); only the empty `id` is new. The door text now says "or leave `id` empty".
3. F8 timing: writing a timing line for settle/control items at `close` is new behaviour (none existed for those lanes); the verdict asked for "the lane's place, not the constant", which has no caller otherwise. Items listed in `item_rec` only.
4. F11 needed a structured field: `ServerDead.cause`, `Walk.cause`, record key `cause`, `open`'s not_started answer key `cause`. The existing test that passed plain text for a stand-held open was changed to the JSON shape.
5. F4 `close` note text lands in the answer's `notes` and the record's `notes`.
6. F2: pin changed, not the charter (role-load margin; the pin said the old words).
7. Spec sync owed (SPEC items left for the Lead, not touched): t-1991 §3.2:287 `impossible`; §3.6 `--items free` and `close` page-touching; Stage 2 timing "grouped by place settle" now has data; the account of a session (guest only); t-2010 F13 (two drafts of one place); U2b merged (done, `c3531ff17`).

## Class siblings noticed (not fixed, reported)

- `s7_gap_reason` still reads the failed record of the LAST triage dispatch only (as before); not touched.
- `walk_after` (case lane) for `walk_retry` is now unreachable from a settle record; nothing else read `state/walks/*.json` as a lane (brief_pack.py:3221 gated on `qa-runner`).
- `s7_settle_session` and `walk_before`/`walk_after` still duplicate the reason-to-text code (the critic queued it).
- The 12 other pytest-only files are green here; the script-entry class stays open.

## Needed beyond the manifest

`walk_session.py` (not in the verdict's fix list as an owned path, but listed in "owns" only via the `scripts/` dir? NOT listed: `walk_session.py` is owned), `brief-form.json`, `inject-map.json`, `brief_pack.py:93` (faq pointer), `test_walk_session.py` (run only), `tools/lint_ratchet.py` (run only). A heredoc `python` edit mangled `\n` twice; fixed by Edit.
