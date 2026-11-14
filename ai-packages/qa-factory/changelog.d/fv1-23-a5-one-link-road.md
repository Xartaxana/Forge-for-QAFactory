- every text the factory reads gets the same link road (`scripts/source_inventory.py`, `scripts/ticket_adapter.py`): a document recorded
  with `record-source` now adds the ticket keys, URLs and merge requests it names to `work/ticket-references.json` (origin
  `mention:document:<ref>`), through `ticket_light.references` and the merge attachments already use; the ticket's own text (S0) and the
  attachment texts add a `linked_document` row for every file they name that lies inside a declared root, each text tried against EACH
  declared root (a file under two roots is two rows); a name that leaves its root, a link that leads outside, a credential-like name or a
  person's exclusion gives no row; the first 500 names of a text are tried and a longer text says so on stderr with its count; a
  credential in a stored reference is masked by ONE helper (`token=`, `secret=`, `password=`, `key=` pairs and the password of a URL's
  `user:password@host`, both as `<hidden>`) in the S0 writer, the paste-only leg of S0 (which now also adds `linked_document` rows) and
  the merge, before a row is stored and before its identity is compared, so the same URL from S0 and from an attachment is one row, and
  a raw row of an older story is masked and joined at the next merge; known limit: a percent-encoded `token%3D` is not masked; no exit code changes, and a story with no references file
  gets no rows and no error
