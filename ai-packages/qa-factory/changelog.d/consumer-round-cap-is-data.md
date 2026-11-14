- consumer acceptance round cap (`references/stages.json`, `scripts/runtime_policy.py`): the S6 and S7 consumer rounds
  are now capped at 1 instead of 2; the cap is the `acceptance_rounds` value of the stage row and
  `runtime_policy.repair_cap` is the one function that reads it for the controller, the cumulative budget and the
  status line; a project's `limits.repair_cycles` no longer lifts it, a person's recorded word still passes the stage
  and lifts the cap; a malformed row is ignored and reads the old limit; S4 and S5 caps are unchanged
