- S7 rework for a bug candidate that has no case (`controller.py`, `no_move.py`, `check_delivery.py`, `driver_conductor.py`,
  `driver_machine.py`, `driver_dispatch.py`, `conductor-actions.json`): `controller.py --operation rework --stage S7
  --role qa-failure-analyst --candidates K-n,R-n` sends the failure analyst back over the story's bug candidates instead of
  a borrowed case (FR-22); the request carries `bug_candidates` and the conductor's `rework_stage` option takes
  `candidates`. A ref the story does not name, or one asked together with cases or rows, or for another stage or role, is
  refused with a door; an input that could not be read is named as not known, never as absent (FR-41). Both judges print
  one text (`check_delivery.candidate_refusal`). The analyst's packet, prompt and brief name the candidates
  (`inject_context.py`, `story_step.py`, `brief_pack.py`, `qa-failure-analyst.md`, `s7.md`, `controller-api.md`)
