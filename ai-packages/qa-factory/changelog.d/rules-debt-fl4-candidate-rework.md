- S7 rework for a bug candidate that has no case (`controller.py`, `no_move.py`, `check_delivery.py`, `driver_conductor.py`,
  `driver_machine.py`, `driver_dispatch.py`, `conductor-actions.json`, `conductor.md`): `controller.py --operation rework --stage S7
  --role qa-failure-analyst --candidates K-n,R-n` sends the failure analyst back over the story's bug candidates instead of
  a borrowed case (FR-22); the request carries `bug_candidates` and the conductor's `rework_stage` option takes
  `candidates` (the answer form the conductor fills shows it beside `cases` and `rows`). A ref the story does not name, or one
  asked together with cases or rows, or for another stage or role, is refused with a door. An input that could not be read
  (a grounding table path that is no readable file, a requirements register with no `## Register` table, an unreadable
  candidate-mark vocabulary, empty or non-UTF-8 files) is named as not known, never as absent (FR-41); only a file that does
  not exist is silent. Both judges print one text (`check_delivery.candidate_refusal`). The analyst's packet line and brief
  head carry the candidates and what is asked for each (one text, `check_delivery.BUG_CANDIDATES_LINE`; no standing charter
  line), so a dispatch without candidates pays nothing (`inject_context.py`, `story_step.py`, `brief_pack.py`, `s7.md`,
  `controller-api.md`). `story_step materialize` echoes the candidates beside the plan rows.
