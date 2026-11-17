- the gate measures the stand's start-page load (`gate_preflight.py`, `manual_capture.py`): once per stand definition (one headless,
  signed-out load, at most once in 7 days), kept in the project's answer registry (`project_knowledge.py`); the S5 automator and
  code-critic briefs and the S7 failure-analyst brief carry it (`brief_pack.py`), and the manual capture's page limit becomes
  180 s, or the measured load plus 30 s when that is longer (the measurement only lengthens a limit); a failed measurement is
  told by its owner and keeps no number; `gate_rehearsal.skip_stand_limits: true` now means "do not measure the page load"
