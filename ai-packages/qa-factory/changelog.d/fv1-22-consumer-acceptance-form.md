- consumer acceptance form (`handoffs/s7-analyst-to-automator.yaml`, `handoffs/s8-scribe-to-gate-b.yaml`, `handoff.py`, `acceptance.py`,
  `handoff_init.py`, `driver_stage_plan.py`, `driver_stage_s6.py`, `driver_stage_s7.py`, `driver_stage_s8s9.py`): the S7 form the analyst
  fills now carries its accept/return word on the runner's handoff (`stage_acceptance.verdict`, the contract's `acceptance_verdict_at`),
  and the S8 form moves its word there from `header.verdict`, so the handoff's own verdict no longer decides the previous stage. ONE reader,
  `handoff.acceptance_verdict_path`, tells every reader (the record, `stage_verdict_known`, the relaxed-section check, the two brief lines)
  where the word is; a missing, malformed or old word is never an accept. A dispatch that awaits nothing gets no acceptance section and no
  reviewed-dispatch row in its skeleton, and the recovery road of `consumer_settled` refuses an unreadable word the way `consumer_completion`
  does. Without this every S6 verdict was unreadable and every analyst form was refused for fields it could not hold (FV1-22).
