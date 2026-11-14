- `record-source` (`ticket_adapter.py`, `runtime_paths.declared_place`): `--ref` may now name a document inside the project or inside a
  repository the config declares in `code_repos` (for example `../sibling/docs/a.md`), so a document of a sibling checkout is recorded
  under its own path and no copy under `work/raw/` is needed; the ref is stored in one normal posix form, a ref that resolves
  outside every declared root, a drive, a rooted path, a `file:` URL or a NUL is refused with the door named, a ref naming a folder is
  refused (one record per document: the refusal names the document's own path), and a credential-like ref is refused before any
  other check and never printed (FV1-23)
- S1 scout prompt (`source_inventory.document_place_lines`, `driver_stage_plan.role_lines`): under each verified folder row of
  `requirements_sources` the scout is told the text documents the folder holds, one path per line with its size (at most 25 per row,
  40 in all, 3 levels, 2000 entries; every cut says where), so each document can be recorded on its own; the grep line and the
  `s1.md` prompt template now say `--ref <that document's path>` instead of the locator (FV1-23)
