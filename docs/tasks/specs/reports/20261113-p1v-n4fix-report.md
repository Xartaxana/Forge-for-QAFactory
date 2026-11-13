# P1-v N4 fix round (verdict 20261113-p1v-n4-topic-code-critic.md), worktree p1v-n4fix

Per finding (all fixed in the one commit of this round, see `git log`):

- F1 (blocking): fixed. `_outside_hops` now takes `cut` (open `launched` rows): a window holding one is `unknown` with the reason
  naming the open call; a call or open call that cannot be placed in any window (unreadable time, or a time between windows) is
  counted in `calls_unplaced` and makes the ROW total `unknown` (per-window values stay listed). Rows: F1 open call -> unknown (not 540),
  open call with unreadable start, call between windows, unreadable-ts row re-pinned from `measured 60.0` to `unknown`.
- F2: fixed. `n/a` only with no journal file or an empty file; `runs_bad > 0` with no rows -> F1 G1 T5 T6 T7 `unknown`; render prints an
  `unknown` rework line. Row added.
- F3: fixed. Rows but no process rows -> `T5.outside_hops` `unknown` ("the record predates the process rows"); the two pins re-pinned.
- F4: fixed. `F1.rework` carries `role_s` and `wall_unknown` per class {rework, non_rework, unclassified}. Two rows (real table; a call with no wall).
- F5 (Lead decision): fixed. `outside_hops_s` = window - calls - hops (hops from `driver_timing.report` hops, clipped to the window; a hop
  crossing two windows is clipped to each); description "wall time of the window outside the calls and outside the hops"; name unchanged;
  negative never clamped. No driver timings -> hop term unknown -> window and row `unknown`.
- F6: fixed. `F1.controller_rounds` attached also in the n/a / unknown no-rows branch. Row added for all three journal worlds.
- F7: fixed. `_merge`/`_length` removed; `_union_s` calls `cost_capture.merge_spans` (T2 and T3 values unchanged, rows green).
- Changelog fragment `p1v-n3-brief-sizes.md`: wording changed as decided.
- Notes N-a..N-d: N-a partly (the T5 function split into `_hop_s_in`, `_window_entry`, `_outside_hops`; `_time_rows`, `_resume_rows`, `counters` not split: queue),
  N-b queue, N-c outside owns (`driver_runner.py:777`), N-d Lead decision (unchanged).
- `references/run-record.json`: no finding pointed at it, unchanged.

Hand arithmetic of the control values:
- F5 probe: window 0-100 = 100 s; calls 10-50 (40 s) and 70-90 (20 s) = 60 s; one hop (result at 50 -> next launch at 70) = 20 s;
  100 - 60 - 20 = 20.0 (printed 20.0; before: 100 - 60 = 40). Row green.
- cross-window hop: windows 0-100 and 200-300; call 10-50 and 250-290 (40 s each); hop 50 -> 250 = 200 s, clipped 50-100 = 50 s and 200-250 = 50 s;
  100 - 40 - 50 = 10 and 100 - 40 - 50 = 10, total 20.0. Row green.
- F1 open call: window 0-600, `launched` at 60 with no outcome -> window unknown, row `outside_hops_s` None (before: 600 - 0 = measured, probe A 540).

Spec fork observed (not decided): `driver_timing.report` returns no hops without `driver-timings.jsonl`, so a run with no timings now gives
T5 `unknown` (literal reading of "any term unknown -> unknown"). The hops are derivable from `driver-runs.jsonl` alone (`driver_timing._hops`,
private, outside owns). Question for the Lead: keep, or expose a public hops reader in driver_timing (outside owns)?

Siblings (report only): axis 6 `retro_numbers.resume_metrics` second rework definition (already queued per spec C-11); no widening.

Witness (from the package dir of the worktree, subshell):

```
$ python -B scripts/tests/test_retro_numbers.py | tail -1
=== test_retro_numbers: 289/289 ok ===
$ python -B scripts/tests/test_driver_stop_record.py | tail -2
=== test_driver_stop_record: 255/255 ok ===
$ python -B scripts/tests/test_judgment_census.py | tail -2
=== judgment_census: 24/24 ok ===
$ python -B scripts/selftest.py --lang | tail -2
PASS lang: no control byte left by an eaten escape sequence (FR-29)

=== qa-factory selftest: 2/2 ok ===
```
