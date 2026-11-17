- a list nested in a map may be left empty, like a top-level list (`scripts/handoff.py`, `scripts/handoff_check.py`): an untouched row of any
  list that crosses no list row (`probes.records` of the code critic's form first of all) reads as the empty list instead of being refused
  field by field, so a critic whose window ran no probe no longer has to invent a record; a row with any real value is still checked in full
  (`handoff.list_paths`, `handoff.only_template`)
- `inputs_read` is a required list on every handoff form that carries it, beside `scope` (`handoff.REQUIRED_LISTS`): an empty or untouched
  `inputs_read` is refused with `handoff_check:required_rows`, whatever the kind of the form; `null-outcomes.json` gives each carrier a home
- the `handoff_check:required_rows` refusal says "`<list>` is a required list and may not be empty" and names the row fields of the list's own
  contract; the joint requirement and the role slices carry the same wording; the code critic's form says in a comment how to leave
  `probes.records` empty
