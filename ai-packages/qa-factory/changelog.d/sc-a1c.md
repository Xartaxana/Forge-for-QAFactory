- S3 window 1 is never offered or assumed as the closing dispatch (`controller.py`, `story_step.py`): one predicate
  (`controller.dispatch_can_close_stage`) answers "this dispatch can close its stage" for the halt doors, `decide`, the recorded
  close, the default completion of `finish`, `stage_repairs` and the controller's own "no role to close it" refusal. A window-1
  halt no longer offers `decide --close`, `decide --close` on window 1 is refused with the doors that work (`--open`, or
  `finish --task <T> --dispatch-id <id> --digest "<digest>" --not-complete --unresolved plan_pending --reason "<words>"`), and `--not-complete` without `unresolved` on window 1 is accepted instead of
  refused with text that was false for it. The exit window and every other stage answer as before.
- One public reader of a dispatch record's purpose (`controller.record_purpose`: the binding only, never the top of the record)
  serves `story_step`, the T2 rule of the driver and `s3_window_of`; the stage model is read once where it was rebuilt per call.
- Stale "S2-S4" stage-critic wording corrected to the stages that have an acceptor or a critic now (`acceptance.py`,
  `stage_done.py` `--acceptance` help, `handoffs/vocabulary.yaml`, `handoff.py`, `handoff_init.py`, `story_step.py`,
  `brief_pack.py`, `exit_gate.py`).
