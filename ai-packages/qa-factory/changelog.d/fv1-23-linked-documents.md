- `record-source` (`ticket_adapter.py`, `source_inventory.linked_documents`, `ticket_light.path_candidates`): after a text is
  recorded from a file inside the project or a declared `code_repos` checkout, the documents that text links by a relative path
  (a markdown link, a bare file name) and that exist there as non-empty text files are listed on stderr (at most 25, with their size,
  then `and <k> more`), so the scout takes a first look at each; stdout keeps its three shapes and the exit code never depends on the
  listing; each listed document is also kept as a `linked_document` row of `ticket-references.json` (not read until its path is
  recorded, which settles the row), through the one merge that attachments' rows use too (FV1-23)
