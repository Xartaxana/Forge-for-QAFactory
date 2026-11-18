# t-1433 code critic: FG7-7 A, FG7-27 A, FG7-27 B, FG7-82

Verdict: NEEDS WORK, 0 blocking findings, 10 fix-before-merge findings. Per node: FG7-7 A NEEDS WORK (F1-F4); FG7-27 A NEEDS WORK (F5-F6); FG7-27 B NEEDS WORK (F7); FG7-82 NEEDS WORK (F8-F10). Accepting the work, and every node or Остатки line proposed below, is the Lead's call.

Diffs read: `git -C <worktree> diff origin/main...HEAD` for 8faa6538, 9cfbb064 (plus the wire patch), a432a195/fdd80f8a and ca43b24d. Cards read: FG7-7 card §3, §4.A, §5, §6 A, §8-§10, §13; FG7-27 card §2, §3, §4 A/B, §10. FG7-82 has no card: its spec is the dispatch `edges:` line plus the pile row (60ed96c0).

## Findings

**F1 (FG7-7, fix before merge). Surface: the moves print. A window with no rows prints none of its no-node moves.** `tools/forge_metrics.py:1411-1414`: `render_node_costs` returns the two empty-journal lines whenever `not d["rows"] and not d["shared"]`. That fires on a journal that is not empty but whose only in-window lines are task_id-less `delegated` ones. Scratch proof (`p1.py`, journal = one `delegated` line with no task_id, through `test_forge_metrics.nc_world`): `rows 0 no_node {'sends': 0, 'delegated': 1}`, and the print is the two-line empty form with no `coordinator moves:` line. That breaks EA3's INV ("none vanishes silently if it is a move"). EA4 promises the two-line form only for an EMPTY journal, so the code's condition is wider than the card's. Fix: take the early return only when `totals.no_node` is also zero, or print the moves line before returning. Then `empty_journal` stays unedited. Neighbours on the same surface: the row cell and the top line do print `>=` (`_moves_cell`). The shared line (`:1471-1473`) prints nothing when `moves == 0` and `resumes_unscanned > 0`, so a reader cannot tell an unknown from a measured 0. A8 literally says "when N > 0", so this neighbour is a spec gap for the Lead to settle in the same fix (print `, moves >= 0` when unscanned).

**F2 (FG7-7, Q4 sibling outside owns).** Card §3 orders a change check: "grep for SendMessage / isSidechain / uuids readers in tools/ with a positive control". The builder's report says it was "not run". My grep (case-insensitive `sendmessage` over `tools/*.py`; positive control: it hits `hop_metrics.py` and `transcripts.py`) finds `tools/session_retro.py:78-133`. That file runs its own pass over the main transcript (`open` + `json.loads`, not `transcripts.iter_lines/parse_line`), with no uuid first-copy and no tool_use-id guard. Scratch proof: one SendMessage record re-written under the same uuid (E32) gives `session_retro tools: [('SendMessage', 2)]`. So the commit line "axis 34 covered -- the dedupe lives only in transcripts.py" holds for where the dedupe lives, but one main-transcript reader does not use it. Proposed line: `session_retro.analyze counts E32 re-writes twice and reads the main transcript without transcripts.first_copy/new_tool_uses | узел: <Lead opens>`.

**F3 (FG7-7, Q5(a)).** Row `resumes_from_parent_session` never reaches the tool_use-id guard of `send_targets`. Its `api-request-blob` copy is dropped by `type != "assistant"` before `new_tool_uses` runs, and its re-write shares uuid `u1`. If `new_tool_uses(obj, ids)` in `transcripts.py:send_targets` were replaced by the bare `content_blocks` filter, the row would stay green (traced by reading). EA6 names "one tool_use id twice". Fix: one record with a fresh uuid that repeats `x1` in the same row.

**F4 (FG7-7, Q7).** `node_costs` (`tools/forge_metrics.py:1303-~1385`) is about 82 lines after the diff, past the 60-line bar, and now holds a nested `moves_of`. `_nc_unscanned` re-derives `_agent_id` for every delegated line on every call. Not a defect. Fix: move the row/shared assembly into a helper.

**F5 (FG7-27 A, Q7, a docstring that is wrong).** `tools/language_sites.py:5` (commit 687cc734) reads: "Wired (FG7-27): .githooks/pre-commit runs `--check --staged`; forge-check runs ...". After F5 (a) the pre-commit hunk was dropped. The same branch's SIBLING_MAP row ("pre-commit: not placed") and the patch's `mechanism_gate.py` comment ("CI-only") both contradict this line. Fix: "Wired (FG7-27): forge-check runs `--check --base $BASE`; pre-commit not placed (scan over 10 s, F5)". The SIBLING_MAP "The detector" row still says "until the code layer is wired, the spec grep there"; reword it in the same fix.

**F6 (FG7-27 A, the patch, fix before placement).** The `tools/test_streams.py` hunk of `t-1430-fg7-27-wire.patch` keeps the comment "the census still tells a link from a tool OUTSIDE the chain that carries a call (language_sites.py, exempt only through KEPT)". The line under it now asserts `in_chain("tools/language_sites.py")` and KEPT is `{}`. The builder noticed this and left it. Fix: regenerate the patch with the comment saying language_sites.py is a chain link (MECHANISM_PREFIXES) and the negative control is `test_s3_negative_control...`.

**F7 (FG7-27 B, Q5(a), CLAUDE.md rule 11 AT-and-BEYOND).** The window bounds are user input (`--window-start/--window-end`) and `ONE_ROAD_SINCE` is a limit, yet the table has no row AT any bound. Three mutants of `tools/calibration_counts.py:771` / `:712` survive on a scratch copy (all with `pytest -k fg7_27`):
- `when < hi` changed to `when <= hi`: 11 passed;
- `lo <= when` changed to `lo < when`: 11 passed;
- `ONE_ROAD_SINCE = "2026-11-11T00:00:00"`: 11 passed (the only pre-floor row is 11-10).

So neither the Lead's F1 floor nor E13's half-open window is pinned. Fix: three rows in `test_fg7_27_one_road_cases`:
- added at `2026-11-17T13:51:09+0100`: listed;
- added at exactly `--window-end`: not listed;
- added at `2026-11-15`: not listed.

Smaller, same file (Q6): the default root expression is now written twice (`:1043` in `_default_reports`, `:1117` in `main`); pass one root.

**F8 (FG7-82, Q6 duplication; refutes the report's "Analogs: none seen").** `tools/journal_write.py:255-266` `_replace_text` already retries `os.replace` on PermissionError only (deadline `SAVE_RETRY_SECONDS = 1.0` at `:90`, pause 0.02 s). The diff adds a second loop of the same rule with other constants (`tools/wave.py:68-69`, `:123-131`). Both modules import `journal_lock`. Fix: one helper (for example `journal_lock.replace_retrying(tmp, path)`) used by both, or a node the Lead opens for the convergence. Neighbours on the same surface (temp-then-replace on Windows), none retried: `piles.write_bytes_atomic` (`piles.py:1007-1018`), `compact_snapshot.py:200`, `dod_track.py:445`, `worktree_sweep.py:1222`. Name them in that node.

**F9 (FG7-82, Q5(a)/(c)).** The new behaviour at the door is the clause on the step-9 `JOURNAL RESTORE FAILED` line. No row reaches it. `test_restore_failed_clause_only_when_copy_equals_main_FG7_82` calls the internal `_recovery_clause` directly. The only door row, `test_wave.py:438` (`test_oserror_in_the_window_names_the_copy_Q5c`), does not check the clause. If `tools/wave.py:533` (`self.mismatch += self._recovery_clause(rel, copy)`) were deleted, every test would stay green (grep of `test_wave.py` for `_recovery_clause|by hand|RESTORE FAILED`: only `:438` and `:472`). The builder lists this under "Not tested". Fix: extend the `:438` world so origin/main's journal equals the copy, assert the clause there, and drop the direct helper row (Q5(e): the internal boundary gets no row).

**F10 (FG7-82, Q4 residual, and the dispatch's witness).** The pile row (60ed96c0) asks for more than the code does. It says "если копия равна версии main -- сразу обновить корень и сказать это одной строкой". The code only names the manual recovery. The dispatch `edges:` narrows the node to the clause, but that narrowing is recorded nowhere in the pile. Proposed: the Lead writes `FG7-82 auto fast-forward of the root when the kept copy equals origin/main | узел: <id>`, or records the narrowing in the row. Separately, the DoD witness `pytest tools/test_wave.py -q -k replace` selects nothing: `128 deselected in 1.82s`, because neither new row has "replace" in its name. I ran the two new names instead (below).

## Standing questions

- Q1 FIT. FG7-7: A1-A9 are implemented as written. EA1, EA2, EA5-EA11, EA13-EA15 were traced by reading. EA3 falls short through F1. EA12: an unreadable session drops all its sends (`send_targets` returns `[]` on OSError or ValueError) and its agents are unscanned. Round 2 (a non-str ts counts HIGH) is at `:1376` and in row `no_task_id_delegated_without_ts_counts_high`. FG7-27 A: 322 rows; `ONE_ROAD_SINCE` matches §10; CI-only. FG7-27 B: D6 and E10-E14 hold. FG7-82: 5 tries x 0.2 s, PermissionError only, any other OSError raised at once after the tmp is removed, clause only when the copy equals origin/main.
- Q2 BUILDER DECISIONS. Each is in the safe direction: shared entries carry `resumes_unscanned`; a None session path means unscanned; `send_targets` also catches ValueError; card B lists `uncommitted`, uses `core.quotepath=false`, and dates by commit wall clock. One accepted gap: under the wall-clock rule, a UTC-zoned commit in the hour after the floor on 11-17 compares below the floor. D6 prescribes this, it is past, and it matters only on that day.
- Q3 SEAMS. Additive. `_nc_tasks` and `_nc_price_all` gain a return value, and both have only `node_costs` as caller (grep). `hop_metrics` stays byte-identical (traced: `not first_copy` equals the old `_seen_before`; `new_tool_uses` equals the old id guard). The patch applies to origin/main 0e6b7ff8 (`git apply --cached --check` on a scratch index: exit 0).
- Q4 CLASS. F2, F8 neighbours, F10. FG7-27 has no gitlab mirror (`git grep dup_ratchet origin/main -- *.yml`: forge-check.yml and nightly.yml only).
- Q5 TESTS. F3, F7, F9. The FG7-7 expected values trace to card §6 rows. Volume: FG7-7 has 46 test lines against about 171 code lines, and FG7-27 B 78 against 107. No pins on text beyond CLI output at the door.
- Q6 DUPLICATION. F8, plus the F7 root expression. FG7-7: no second dedupe (grep `"uuids"|get("uuid")` in tools/: `transcripts.py:505`, plus `warn_density.py:721`, which is a unit key, not a dedupe pass). FG7-27: the baseline is written by `--init` only (one site counter).
- Q7 CODE QUALITY. F4, F5, F6.
- Q8 HYGIENE. Not a package diff: no file under `ai-packages/`.
- Q9 RATCHETS. FG7-27 A adds a NEW member of axis 18, `tools/language-sites-baseline.json`: 322 rows, "grandfathered, not approved", written by `--init`. It raises no existing ratchet. Freshness risk: 10 package-script commits landed on origin/main after merge base b3c1a28c (`git log b3c1a28c..origin/main -- ai-packages/qa-factory/scripts`). Per F2 (a), the integrator re-runs `--init` on a red C1/C2 at merge. The other three branches touch no ratchet.
- Q10 ARCHITECTURE. The FG7-7 commit names AR-13 and AR-15, and the producer-reader walk holds. EA14: forge_metrics never imports hop_metrics (grep: comments only, at `:1016`). VARIETY: none. These are forge tools: an unknown value is printed `>=`, `n/d` or `cannot judge`; nothing blocks.
- Q11 JUDGMENT. None. The FG7-27 B list is advice only, and the exit code is unchanged.
- Q12 ONE ROAD. None found. Grep over the four diffs for language, runner or project names: only the baseline data rows and the uds-pipe sample, which is data.

## Spot-checks

- FG7-7 report says "imports unchanged / closure": confirmed by grep (above).
- FG7-27 A report says "patch applies": re-run on today's origin/main with exit 0.
- FG7-27 B report says "Noticed analogs: none": no counter-example found.
- FG7-82 report says "Analogs: none seen": REFUTED by F8.
- Every negative above carries its positive control.

## Trail

- `pytest tools/test_forge_metrics.py -q` (FG7-7 worktree): `129 passed, 3 skipped in 98.45s`.
- `pytest tools/test_wave.py -q -k replace` (FG7-82): `128 deselected in 1.82s`. Then `-k "retries_permission_error_only or clause_only_when_copy"`: `6 passed, 122 deselected in 10.85s`.
- `pytest tools/test_calibration_counts.py -q -k fg7_27` (FG7-27 B): `11 passed, 105 deselected in 5.45s`.
- Scratch: `scratchpad/p1.py` (F1, F2 proofs, output quoted above). `scratchpad/fg727b/tools` is a byte copy of the worktree tools (calibration_counts sha256 faaedeffe0a1c75d before the mutants); the three mutant runs are quoted in F7. Live trees untouched.
- `GIT_INDEX_FILE=<scratch>/idx-main git read-tree origin/main && git apply --cached --check <patch>`: exit 0.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "FG7-7: session_retro.py:78-133 reads main transcripts without first_copy/new_tool_uses (E32 counted twice, scratch proof) - node for the Lead; FG7-82: journal_write._replace_text :255-266 is a second PermissionError replace-retry, plus unretried temp-replace writers piles.py:1007, compact_snapshot.py:200, dod_track.py:445, worktree_sweep.py:1222 - one helper or a node; FG7-82 pile row's auto fast-forward not implemented - node or narrowing recorded; FG7-27: no gitlab mirror exists",
  "fixes": [
    "F1 forge_metrics.py:1411-1414 early return hides no_node moves when rows==0 but nokey delegated lines exist; shared line :1471-1473 silent on unscanned with moves 0",
    "F2 session_retro.py:78-133 sibling: Lead opens a node (card section 3 change check was not run by the builder)",
    "F3 test_forge_metrics.py resumes_from_parent_session: add a fresh-uuid record repeating tool_use id x1",
    "F4 forge_metrics.py:1303-1385 node_costs about 82 lines: split the row/shared assembly",
    "F5 language_sites.py:5 docstring claims pre-commit runs --check --staged; CI-only after F5 (a); also SIBLING_MAP detector row wording",
    "F6 wire patch test_streams.py hunk keeps the comment 'exempt only through KEPT' above in_chain(language_sites.py)",
    "F7 test_calibration_counts.py test_fg7_27_one_road_cases: add rows at the floor instant, at window-end, and between 2026-11-11 and the floor (three mutants survive); dedupe root expression :1043/:1117",
    "F8 wave.py:123-131 duplicates journal_write.py:255-266 PermissionError retry: one helper or a Lead node",
    "F9 test_wave.py: the FAILED-line clause (wave.py:533) has no door row; extend the :438 world, drop the direct helper row",
    "F10 FG7-82 pile row auto fast-forward residual needs a node or recorded narrowing; dispatch witness -k replace selects 0 tests"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/20261118-fg7-6-fg7-7-coordinator-moves-card.md sections 3,4.A,5,6A,8-10,13",
      "docs/tasks/specs/20261118-fg7-27-language-sites-one-road-card.md sections 2,3,4,10",
      "handoffs t-1429-fg7-7.md, t-1430-fg7-27-a.md, t-1430-fg7-27-wire.patch, t-1431-fg7-27-b.md, t-1425-fg7-82.md",
      "diffs origin/main...HEAD of 8faa6538, 9cfbb064, a432a195, ca43b24d",
      "tools/transcripts.py parse_line/iter_lines/content_blocks; tools/forge_metrics.py 1027-1032, 1205-1232, 1405-1414",
      "tools/session_retro.py 70-150; tools/journal_write.py 86-92, 245-266; tools/piles.py 1005-1018; tools/wave.py 400-545",
      "tools/calibration_counts.py 202-211, 1043, 1117; commit messages of the four branches"
    ],
    "reruns": [
      {"command": "python -m pytest tools/test_forge_metrics.py -q (FG7-7 worktree)", "result": "129 passed, 3 skipped in 98.45s"},
      {"command": "python -m pytest tools/test_wave.py -q -k replace (FG7-82 worktree)", "result": "128 deselected in 1.82s (selects nothing)"},
      {"command": "python -m pytest tools/test_wave.py -q -k 'retries_permission_error_only or clause_only_when_copy'", "result": "6 passed, 122 deselected in 10.85s"},
      {"command": "python -m pytest tools/test_calibration_counts.py -q -k fg7_27 (FG7-27 B worktree)", "result": "11 passed, 105 deselected in 5.45s"},
      {"command": "scratch mutants of calibration_counts.py (end <=, floor <, ONE_ROAD_SINCE 2026-11-11)", "result": "11 passed each: all three survive"},
      {"command": "scratch p1.py: rows-empty window with one task_id-less delegated line; session_retro duplicate record", "result": "no_node delegated 1 with no moves line in print; SendMessage counted 2"},
      {"command": "git apply --cached --check wire patch on scratch index of origin/main 0e6b7ff8", "result": "exit 0"}
    ]
  }
}
```
