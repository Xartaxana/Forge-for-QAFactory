- the end of the S7 repair road is "awaiting acceptance", not a closed stage (`acceptance_awaits` marker in `pipeline.json`, read by `awaits_acceptance` in `story_run.py`): the scribe is let in to accept the analyst's work,
  and a bare attempt to close S7 with neither a wait nor an acceptance record is refused with the name of the record it needs.
