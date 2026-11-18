- the gate measures the stand's start-page load (`gate_preflight.py`, `manual_capture.py`): once per stand definition (one headless,
  signed-out load, at most once in 7 days), kept in the project's answer registry (`project_knowledge.py`); the S5 automator and
  code-critic briefs and the S7 failure-analyst brief carry it (`brief_pack.py`), and the manual capture's page limit becomes
  180 s, or the measured load plus 30 s when that is longer (the measurement only lengthens a limit); a failed measurement is
  told by its owner and keeps no number but its reason (cause, why, time, attempts; never "this machine has no browser", a machine fact, which is told per run only) in the same registry row: the second start
  tries once more, a second failure of the same cause stops the tries and the reason is carried in the gate note until the stand's definition or address changes or a person revokes the row; `gate_rehearsal.skip_stand_limits: true` now means "do not measure the page load"
