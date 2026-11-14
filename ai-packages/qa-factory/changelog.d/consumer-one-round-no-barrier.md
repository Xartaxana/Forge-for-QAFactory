- the acceptance of S6 (by the failure analyst) and of S7 (by the doc scribe) is never a barrier: when the one repair round of the author is
  spent, or the consumer's verdict word cannot be read, or its acceptance form is refused, or the rounds cannot be counted, or the controller
  registers no round, the driver accepts the stage itself with a named gap (`consumer_gap`: a driver acceptance whose quote starts `gap:`,
  then the warning `<stage> was accepted with a gap: <why>`), the consumer goes on with what it has, and no question reaches the conductor or
  the person; the gap reaches the report under "Factory defects" (S6) or gate B's packet, which now carries the "Warnings the factory is
  carrying" block (S7); a person's pass, given before the verdict or after it, always wins over a gap, and a consumer's questions to the
  person are never folded into one (`scripts/driver_stage_s6.py`, `scripts/gate_brief.py`, `scripts/driver_core.py` `GAP_PREFIX`)
- the consumer's brief carries a round line before its work: one return left ("the one chance"), or none left / not countable ("do your own
  work with what it gives, name the gap in `unresolved`") (`scripts/driver_stage_s7.py`, `scripts/driver_stage_s8s9.py`); a story in flight
  with a second consumer round already registered runs it and meets the gap road at the next verdict; one with none registered gets none
