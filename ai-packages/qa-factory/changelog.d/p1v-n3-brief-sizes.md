- brief size record (`scripts/brief_pack.py`, `references/artifact-writers.json`): `brief_pack.build` appends one line
  `{ts, stage, role, dispatch, bytes, budget_bytes, ceiling, over}` to `state/brief-sizes.jsonl` for every brief it writes as
  the dispatched brief (not on a dry run, not with `--output`); a record for the forge's run scoreboard only, so nothing in a run
  reads it or compares it with the ceiling, and the text of the brief and of its stdout line are unchanged; a record that cannot
  be written is one note on stderr and the brief is still written
