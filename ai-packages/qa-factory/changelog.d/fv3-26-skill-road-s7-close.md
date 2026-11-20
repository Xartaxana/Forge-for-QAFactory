- the skill road closes S7 by code when nothing is left to triage (FV3-26): `story_step.py start --stage S7 --role qa-failure-analyst` runs the
  driver's own `s7.no_failures` body (`stage_close.s7_code_close`: places nobody settled become gaps, the investigation gate, the `code_only`
  receipt, the stage record, the `dispatch_skipped` row) instead of dispatching an analyst, then prints the S8 card; the hand-written
  `S7.status: done` record, which the controller refused, is gone from `phases/s7.md` and SKILL.md. A running or owed investigation pass,
  a failure in the run report, a counting need row and a halted or missing run report close nothing (the last two refuse with a door);
  a completed S7 is never closed again
