- every text the factory reads gets the same link road (`scripts/source_inventory.py`, `scripts/ticket_adapter.py`): a document recorded
  with `record-source` now adds the ticket keys, URLs and merge requests it names to `work/ticket-references.json` (origin
  `mention:document:<ref>`), through `ticket_light.references` and the merge attachments already use; the ticket's own text (S0) and the
  attachment texts add a `linked_document` row for every file they name that lies inside a declared root, each text tried against EACH
  declared root (a file under two roots is two rows); a name that leaves its root, a link that leads outside, a credential-like name or a
  person's exclusion gives no row; the first 500 names of a text are tried and a longer text says so on stderr with its count; a
  credential in the query of a stored reference is masked (`token=<hidden>`); no exit code changes, and a story with no references file
  gets no rows and no error
