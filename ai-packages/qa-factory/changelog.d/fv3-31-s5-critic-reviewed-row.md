- S5 code critic form (`handoffs/s5-critic-to-automator.yaml`, `handoffs/s5-critic-plan-to-automator.yaml`, `references/stages.json`,
  `scripts/brief_pack.py`, `scripts/story_step.py`): the critic's form now arrives with the automator dispatch it reviews filled
  into `inputs[0]` and `inputs_read[0]`, and its brief carries the `Reviewed dispatch:` line. The new S5 stage key `reviewed_by`
  names the reviewing role; `brief_pack.reviewed_dispatch` is its one reader and picks the author bound to the critic's own
  window or plan (parallel windows never name a neighbour's automator, nothing is named when no match exists). Absent or
  invalid key: no line and no prefill, as before (a missing author is never guessed).
