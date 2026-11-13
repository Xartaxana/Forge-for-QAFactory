- every exit-gate refusal record now names the check that produced it (`scripts/detector_verdict.py`, `scripts/exit_gate.py`): `Record.check`
  (`<producer>:<family>`, e.g. `s5_precheck:manifest`) and `Record.tag` are fields beside the text, `parse` returns `labels` parallel to
  `findings`, and `check_id` / `with_check` are the one reader and the one writer; the text of a record is unchanged
- `story_step finish` prints a last machine line `checks: [...]` on an exit-gate refusal, and the driver takes it out of the text before a
  role, the conductor or the finding key reads it (`scripts/story_step.py`, `scripts/driver_dispatch.py`); `Refusal.checks` carries the ids
  (a refusal with no id counts as ONE `unknown`), and the resumed rows of `driver-runs.jsonl` carry `checks` and `checks_n`
  (`scripts/driver_core.py`, `scripts/driver_runner.py`, `scripts/driver_machine.py`); rows written before this change read as `unknown`
