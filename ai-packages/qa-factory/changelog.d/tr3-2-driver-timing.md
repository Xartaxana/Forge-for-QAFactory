- The driver times the steps between one role's result and the next launch (`story_run.py` `Driver.timed`, `story_step.py` `start`): one line per step in
  `state/driver-timings.jsonl`, and `python driver_timing.py --task <KEY> [--json] [--check-hop-s N]` prints each hop's wall, its steps, the
  unattributed remainder and the per-step totals (a story with no such file prints "no timings recorded", never 0 s). The console says
  `note: <step> took N s` only over 20 s. The journal row of a role or conductor call now carries `wall_ms` next to `duration_ms`, with one
  note when the CLI's own count trails the wall clock by more than 120 s. While a role's process is waited for, one line
  `[progress] <dispatch> has written nothing for N min (last at HH:MM)` appears once per silence episode; the driver never stops a role for it.
