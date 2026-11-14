- every stop of the driver on "the same set of findings again" now leaves one `repeat_stop` row in `driver-runs.jsonl` before the
  person is asked (`Driver.record_repeat`, the one writer): the stage, the road (conductor rounds, the role's own resume, the
  structured-artifact resume, the handoff resume ladder, the gate repair rounds), the series key, the dispatch, the outcome
  (`same_set`, `cap`, `again`) and the finding set as it is compared (dispatch ids masked, at most 20 lines of 300 characters, the true
  count in `set_size`). The row is data for finding the cause of a repeat; it judges none. A record that cannot be written is one
  stderr line and never stops the run. The collector reads the rows through a new row of `references/collect-loops.json` (L8).
