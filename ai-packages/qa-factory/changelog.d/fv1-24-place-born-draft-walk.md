- A bug draft of a place the analyst walked, for a case the runner never ran, is lifted by its `walk` record (`bug_records.py`:
  `reproduction_problems`, new public `no_run_target`): the draft's own triage row of such a case is archived by the
  `finalize_task` binding ("not bound to current failure"), so the two draft-wide facts (an APP_BUG triage row, a red current
  result) could never hold and the draft read `unconfirmed` whatever the walk showed. When the draft's triage instance matches no
  id the run report holds (any attempt, any spelling) a `walk` entry no longer needs them: the walk record is the step, and
  `place_answers.settled_answer` and the investigation's unresolved-target reader gain the lift through `confirmation_of`. A draft
  whose instance the report holds, a non-walk entry, a draft with no `triage_ref` and an unreadable or empty report keep both facts
  (an unknown never lifts). A place-born draft that also names a requirement in `unconfirmed_requirements` will read `unconfirmed`
  again once the later expectation check lands, until the analyst splits that part off; the gate B bug-draft check still reads
  the triage verdicts directly and still blocks a place-born draft until it reads `no_run_target` (a separate node).
