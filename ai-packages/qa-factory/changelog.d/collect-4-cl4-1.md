- Driver (`driver_machine.py`): every rework round of an S5 window that goes to the conductor, and the stop at the cap or at a
  repeated finding set, also writes a `window_round` row to `driver-runs.jsonl` (`stage`, `key`, `dispatch`, `round`, `cause`,
  `outcome`, `findings`). The collector reads it (`references/collect-loops.json`, L2), so a window that hit its cap and was
  accepted later still counts as a loop, and that story's transcripts are now sent with the archive, like a stalled story's.
  Stories run by an earlier version keep no such row: a capped window of theirs accepted before the collect is not seen as a loop.
- Task price (`references/driver-journal-kinds.json`): `window_round` rows and the driver's own `process` rows are bookkeeping
  with no session and no money, so they no longer make a story's price `incomplete`.
- Collector (`collect_stall.py`, `collect_pack.py`): each story of the manifest carries `ignored` and `loop_ignored`, the records
  the stall and loop rules could not use because they hold no time, and the intake lists them; whether a story stalled and
  whether it looped is read in one place (`collect_stall.loop_state`). qa-collect and its page say "stalled or looped".
