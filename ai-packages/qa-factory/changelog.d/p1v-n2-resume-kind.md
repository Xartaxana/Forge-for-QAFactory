- every resumed role row of `driver-runs.jsonl` carries `resume_kind`, a closed token naming the ROAD of the resume (`handoff_findings`,
  `handoff_findings_mechanical`, `person_answer`, `refusal_resume`, `stand_answers`, `paid_round`, `structured_refusal`, `service_cut`,
  `unclassified`); the table is `references/run-record.json` key `resume_kinds`, read only through `driver_journal.run_record_names`
  (the one validator of the lists of that file, shared with the run class: an empty list or an empty name is refused); the driver's own
  retry of a call the service broke after it worked is `service_cut`, like the resume of an interrupted record
- a caller that names no kind, a kind outside the table, or an unreadable table gives `unclassified` and one note, never a stop; a row that is
  not a resume has no `resume_kind` key; rows written before this change have no key and nothing here reads them (the scoreboard reader must
  read an absent key as unknown) (`scripts/driver_runner.py`, `driver_dispatch.py`, `driver_machine.py`)
