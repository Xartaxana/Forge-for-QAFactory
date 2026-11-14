# t-719 — REDRAFT of FV1-23 nodes A-2 and A-3 (after plan critic t-706)

DRAFT by designer, 14.11.2026, for Lead acceptance. Forks are returned with a recommendation and are not decided. This
file replaces A-2 and A-3 of `docs/tasks/specs/20261113-fv1-23-fv1-20-spec.md` §A.4. A-1 and A-4 (built, branch
`wip/fv123-a14` b2c082a), F-A1 (a), F-A2 (a), F-A3 (a) stand as the Lead amended them. Prefixes: `P\` =
`C:\QAFactory\forge-repo\.claude\worktrees\read-main\ai-packages\qa-factory\` (origin/main, where every package fact
below was read); `S\` = `C:\QAFactory\mybooks-stand\arm-factory\`; `T\` = the S1 scout transcript
`C:\Users\i_mas\.claude\projects\C--QAFactory-mybooks-stand-arm-factory-test-automation-framework\634b0a20-f8e1-408c-a85d-5a78f5c56ef8.jsonl`.

---

## 1. Scope, owners, AR-n (designer rule 1)

The package is touched. AR-n touched, each with the change check written into the DoD of the card that touches it:

| AR | How the redraft touches it | Change check (in the DoD) |
|---|---|---|
| AR-4 | a ref into a sibling checkout is resolved through `runtime_paths` (`contained`, `_repository_roots`) and stored project-relative, posix | no new project walk outside `nearest_project`; the stored ref has no drive and no absolute part (table rows) |
| AR-13 / AR-15 | ONE predicate "inside a declared root" read by the listing (A-2), by `record-source` (A-2) and by the link listing (A-3); ONE merge of reference rows for attachments and documents (A-3) | grep the diff: no second containment test for these refs; `append_attachment_references` calls the shared merge |
| AR-1 | which config row is a place on disk is read by the kinds table's capability key `route == "grep"`, never by kind name | grep the new functions for `"repository"` / `"file"` literals: none |
| AR-3 / P2 | no file or folder name (`README`, `docs`, `AUTH`) and no project name in code or role text | grep the diff for those literals (case-insensitive) with a positive control on a test fixture |
| AR-9 / FR-1 / FR-2 | every new refusal of `record-source` names what was expected and a door the scout can use | each refusal is a table row asserting its door text |
| AR-21 / AR-23 | every cut (count, depth, length, candidates) is said with its place; every empty outcome is declared | AT/BEYOND rows per limit |
| AR-22 | the new `linked_document` rows of `ticket-references.json` have a reader (`brief_pack.reference_gap_lines`, unchanged) and a settler (`_settle_references`) | one join row: a row written by A-3 is read back by `reference_gap_lines` and settled by a later record |
| AR-29 / P27 | code lists data (files at a place, paths a text links); the scout judges relevance; no verdict word in any line | grep the new lines for `relevant`; the census rows below |
| AR-12 | the record road gets cheaper for a sibling checkout (no copy to `work/raw/`) | report: friction of the S1 road "not measured" as an open item, measured at A-L |

Checks the redraft adds or alters — owner (P27) and census class (AR-29):

| Check | Where | Owner | Class | Blocks |
|---|---|---|---|---|
| `--ref` resolves inside the project or a declared `code_repos` root | `ticket_adapter._record_source` (through `runtime_paths.declared_place`) | data (code) | xref (a ref joined with config `code_repos`) | refuses the command, door named |
| `--ref` names an existing folder | same | data | shape | refuses, door names the document's own path |
| `..` ref with no project config above `--output` | same | data | shape (presence of the config) | refuses (FR-59 safe default), door named |
| a listed path / a linked path must pass the same predicate, be a regular non-empty text file | `source_inventory.document_place_lines`, `linked_documents` | data | shape | never (advice lines) |
| a `linked_document` row is settled when its path is recorded | `source_inventory._settle_references` | data | xref | never |
| relevance of a listed or linked document | the scout (charter `qa-scout.md:72`, `:53`) | judgment, accepted by the S1 acceptor (driver, `tried`) and the S2 tester | — (role) | — |

Direction of the allowed error (designer rule 1, reused functions in a gate role): `runtime_paths.contained` moves from an
advisory resolver into a refusal of `record-source`. Its own docstring already fixes the direction
(`runtime_paths.py:479-486`): "the allowed error is not recognising a path as ours ... calling a foreign path ours is the
forbidden one". The redraft keeps it: a legal document may be refused (the door then names the document path or the old
road "copy it under work/raw/ and record that path"), a path outside every declared root is NEVER accepted, listed or
stored. Adversarial inputs that must stay on the safe side: `../../..` escapes, `docs/../../x`, a symlink or junction
inside a repository pointing outside, an absolute path (`C:\`, `/etc`, `\\server\share`), a `file:` URL, a drive taken for
a scheme (`C://x`), mixed slashes (`..\MyRepo/docs\a.md`), a repository root on another drive, a 300-character ref, a
credential-like ref.

---

## 2. Facts (each read at its carrier on origin/main)

| # | Fact | Carrier |
|---|---|---|
| R-f1 | `record-source` refuses any ref that is not a URL and fails `SI._safe_rel` (no drive, not rooted, no `..`) with "give the locator relative to the project (a path with no drive and no `..`), or a URL"; no disk resolution of the ref happens anywhere in the command | `P\scripts\ticket_adapter.py:2200-2204`; `P\scripts\source_inventory.py:2712-2718` |
| R-f2 | Then: credential refusal (:2205-2209), the person's exclusions by `first_ref_match(live_in(<output parent>), ref)` (:2210-2215), the text test (empty/blank -> "nothing to record", not UTF-8 or NUL -> exit 3 "is not text"), then `record_text_source` | `ticket_adapter.py:2205-2236` |
| R-f3 | `update_inventory` replaces a record with the same `canonical_ref` and keeps the old one only in `prior_revisions`: two documents recorded under one folder ref leave ONE source | `source_inventory.py:1896-1913` |
| R-f4 | The grep line of `requirement_source_lines` tells `record-source --ref {whole}` = the row's locator (a PLACE) | `source_inventory.py:2301-2306` |
| R-f5 | One containment predicate exists: `runtime_paths.contained(path, root)` (realpath both sides, by components, allowed error = not ours); `_repository_roots(project, cfg)` resolves `code_repos[].path` against the project; `nearest_project(start)` is the one marker walk; `_config_of(project)` reads the config | `P\scripts\runtime_paths.py:479-517`, `:285-292`, `:193-207`, `:920-925`; axis 8 row "The resolver (READ)" (`docs/SIBLING_MAP.md:209`) |
| R-f6 | `source_inventory._task_config(task_root)` and `size_limit_of(task_root)` (the guard's big-read cap, `guard_pre_tool.big_read_cap`; 0 = unknown) exist | `source_inventory.py:2730-2756` |
| R-f7 | `record_text_source` adds NO reference rows; its docstring says "the links of the text are read from `ticket-references.json`" — which nothing fills for a recorded text | `source_inventory.py:2078-2085`, `:2115-2124` |
| R-f8 | `append_attachment_references` fills `ticket-references.json` from text attachments through `TL.references` and merges by identity `(kind, ref, repo)` (origin added, no twin), marks `scanned`/`written_by`; returns silently when the file is absent or unreadable | `source_inventory.py:2014-2053` |
| R-f9 | `TL.references` extracts URLs, `~/` and `C:\` local paths, merge requests and keys; it does NOT extract a relative path like `docs/AUTH.md` or a bare `TEST_IDS_REFERENCE.md` | `P\scripts\ticket_light.py:942` (`_LOCAL_PATH_RE`), `:1050-1165`, `:1255-1269` |
| R-f10 | `_settle_references` moves only rows of kind `ticket` | `source_inventory.py:1985-2011` |
| R-f11 | Readers of `ticket-references.json`: `brief_pack.reference_gap_lines` (renders every non-`fetched` row generically, any kind, at brief time, scout brief only when `work/ticket-snapshot.json` is named) and `driver_s0` (no-change question: change kinds only). No S1 exit reads it (Grep `ticket-references` over `scripts/*.py`: 11 files, `controller.py` not among them; the same call found `brief_pack.py`) | `P\scripts\brief_pack.py:1353-1391`, `:4421-4424`; `P\scripts\driver_s0.py:920-968` |
| R-f12 | The driver-run scout's prompt = `role_lines`: launch flags, environment, ticket source, `tracker_route_lines` (TRACKER_RULES when the role reads the tracker), `Repositories:`, `requirement_source_lines`, `left_out_lines`; the driver has `self.project` and `self.task_root` | `P\scripts\driver_stage_plan.py:19-48`; `P\scripts\driver_core.py:457-460` |
| R-f13 | `left_out_lines` reads `SE.live(self.task_root)` and turns an unreadable record into a `Refusal` | `P\scripts\driver_sources.py:776-784` |
| R-f14 | `TRACKER_RULES[3]` = `s1.md:126` word for word, pinned by `test_tracker_route.py:581-583` (quarantined, cohort 8073673) | `source_inventory.py:2153-2154`; `P\skills\qa-story\phases\s1.md:126`; `test-layers.json:10463-10466` |
| R-f15 | The skill road's prompt template tells `record-source --output INV --ref <locator> --file <file> --relation normative --summary` | `s1.md:59-60` |
| R-f16 | The charter carries the link rule for every text: `qa-scout.md:72` "The walk of references: take a first look at every key, link or file name, read whole only what you judged relevant, keep a visited set", and `:53` "Judge a link by what you read in it, never by its title or type" | `P\agents\qa-scout.md:53,72` |
| R-f17 | `--summary` prints ONE line of compact JSON (a test parses it with `json.loads`); `--json` prints the inventory or record as JSON | `ticket_adapter.py:2027-2046`, `:1753-1756`; `test_local_keys.py:426-429` |
| R-f18 | Keep test homes exist: `test_local_keys.py` (keep, layer `table`, covers `source_inventory.py` and `ticket_adapter.py`; its `record_source_edges` holds a `cases` table of record-source refusals, :461-486) and `test_runtime_paths.py` (keep, layer `table`, covers `runtime_paths.py`). Neither is in `slow_tests.json` above 30 s (`test_runtime_paths.py` 27.0 s; `test_local_keys.py` not listed) | `P\scripts\tests\test-layers.json:2893-2909`, `:4690-4707`; `P\scripts\slow_tests.json:103` |
| R-f19 | The existing row "dotdot ref" `docs/../../x.md` -> exit 2 with the needle "give the locator relative to the project"; refs `docs/price-rules.md`, `docs/ok.md` are accepted although `docs/` does not exist in the temp project | `test_local_keys.py:468-472`, `:423-424`, `:490-491` |
| R-f20 | The scenario walker's doors are `exit_gate, joint, start, gate, delivery`: no door runs `ticket_adapter record-source`, so record-source cases cannot be scenario rows | `P\scripts\tests\scenario_walk.py:40-47` |

### 2.1 Why a rule that exists did not work (A-3's question), from the evidence

| # | Evidence | Carrier |
|---|---|---|
| E1 | The driver's prompt to the scout carried TRACKER_RULES rule 4 ("A key or link in what you read: read it, keep only what can carry a requirement ...") and the line `app-readme: search ../MyBooks/README.md for the story's words with Grep; ... record-source --ref ../MyBooks/README.md ...`. With charter :72 the link rule reached the scout TWICE | `T` line 5 (and 17) |
| E2 | The scout read the README, whose "More" section says `[docs/AUTH.md](docs/AUTH.md): accounts, roles, sessions, limits`, and listed `docs/` (AUTH.md, DEPLOYMENT.md, openapi.json) | `T` line 57 |
| E3 | Its only look at a linked document was `grep -n -i "cart" ../MyBooks/TEST_IDS_REFERENCE.md` — a story-word grep, the method its prompt line names for a source | `T` line 63 |
| E4 | No tool call names `AUTH.md` (critic's per-line count; my Grep `-o` over `T` finds AUTH.md only inside the tool RESULT of line 57) | `T`; critic verdict F-2 |
| E5 | `AUTH.md:8` holds the merge rule and the story's own word: "Guest cart: ... After sign-in the login page calls `POST /api/cart/merge`; the higher quantity wins ..., capped at stock." A grep of "cart" over AUTH.md would have found it | `S\MyBooks\docs\AUTH.md:8` |
| E6 | The brief's own record command was refused (`..`) and the scout copied the README to `work/raw/` and recorded the copy: provenance became `qa-factory/artifacts/LOCAL-1/work/raw/MyBooks-README.md` | `T` lines 80, 82, 87; stand `work/source-inventory.json:53` (critic's read) |

Reading: the miss was not "no rule". The scout never took a first look at AUTH.md at all; whatever it did with
TEST_IDS it did not do with AUTH.md, whose link TITLE lacks the story's word — a title judgment against charter :53.
INFERRED, not established: the motive (thinking blocks are empty), and whether the friction of E6 cut the walk short.
Established: a rule text was present twice and did not produce the look. A third rule text (fork F-R2 (a)) has a low
expected yield. What the role lacked at the moment it recorded the README was the LIST of what that text links on disk —
data code can produce. That is the remedy recommended in F-R2 (b): it reaches the driver-run scout through the tool
output of `record-source`, the command both roads use (s1.md is never read under the driver), and it does not touch
TRACKER_RULES or s1.md:126, so the pin of R-f14 stays green.

---

## 3. Critic findings -> where the redraft closes them

| Finding | Closed where |
|---|---|
| F-1 (ref of a sibling checkout refused) | A-2 items 1-2: `runtime_paths.declared_place` + `record-source` accepts a ref resolving inside a declared root; rows "`..` inside code_repos accepted", "listed path accepted by record-source" (join) |
| F-1 second defect (several documents under one folder ref keep the last) | A-2 item 2: a ref naming an existing folder is refused with the door "the document's own path"; A-2 item 3 lists per-document refs; A-3 item 4: the grep line says `--ref <that document's path>`; row "two documents of one folder -> two records" |
| F-2 (A-f8 false; s1.md not read by the driver scout; TRACKER_RULES pin; two wordings) | §2.1 restates the cause from the evidence; A-3 does not move or reword the link rule: TRACKER_RULES and s1.md:126 are untouched (pin green); the new lines POINT to the charter rule (axis 31) instead of paraphrasing it; the remedy rides `record-source` output, read on both roads |
| F-5 a (wrong `live_in` call) | A-2 item 3: `SE.live(task_root)`; `task_root` is a parameter |
| F-5 b (unreadable exclusion record) | A-2 edge: `ExclusionRecordError` -> the listing returns `[]`; `left_out_lines` refuses next, naming the file |
| F-5 c (depth vs "counted in more") | A-2 item 3: depth defined (a file directly in the folder = depth 1); the walk does not enter folders below depth 3 and counts them as "not walked"; an entries cap bounds a wide tree |
| F-5 d (bytes / long path) | A-2 item 3: a path over REQUIREMENT_SOURCE_LOCATOR_LIMIT is not listed and counted "name too long"; listing bounded by counts per row and total |
| F-5 e (empty file) | shared text test: empty or whitespace-only = not text |
| F-5 f (credential-like file name) | not listed, counted "withheld" |
| F-5 g (size unit) | `<n> B` |
| F-5 h / i | TEMPORAL and POSITIONAL kept, restated in A-2 edges |
| F-6 (no keep test home; slow files in the witness) | homes: `test_local_keys.py` (keep table, covers both scripts) and `test_runtime_paths.py` (keep table); no `test-layers.json` edit needed; every DoD runs the printed witness minus the slow files, named "судит канон пачки"; `test_driver_layers.py` named for the `role_lines` import |

---

## 4. Cards

### A-2 — one rule "inside a declared root" for the listing and for `record-source`; the document places listed per document

given: `P\scripts\runtime_paths.py` (:193-207, :285-292, :479-517, :920-925), `P\scripts\ticket_adapter.py` (:2184-2246),
`P\scripts\source_inventory.py` (:1896-1970, :2128-2140, :2248-2312, :2712-2756), `P\scripts\source_exclusions.py`
(`live`, `live_in`, `first_ref_match`, `ExclusionRecordError`), `P\scripts\driver_stage_plan.py` (:11-48),
`P\scripts\driver_sources.py` (:776-790), `P\scripts\config_contract.py` (`requirement_source_kinds`, `SECRET_QUERY_RE`),
`P\references\requirement-source-kinds.json`, `P\scripts\tests\test_local_keys.py` (:415-516),
`P\scripts\tests\test_runtime_paths.py` (`k1_*`), `P\design\factory-rules.md` (whole), `P\design\architecture.md` (AR-4,
AR-9, AR-13, AR-15, AR-29), `plans\builder-rules.md`, this spec §1-§3.
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\runtime_paths.py (new function `declared_place` only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\ticket_adapter.py (function `_record_source`: the ref check block :2200-2215 only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\source_inventory.py (new `document_place_lines`, new `text_file_problem`, their constants)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\driver_stage_plan.py (function `role_lines`, the `qa-scout` return expression only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_local_keys.py (rows in `record_source_edges`; one new table function `document_places`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_runtime_paths.py (one new table function for `declared_place`)
non-goals: no inventory record written by code; no change to `record_text_source`, `update_inventory`, `requirement_source_lines`
(A-3 owns its string), TRACKER_RULES, s1.md, `brief_pack.py`, any role text; no migration of configs; no new test file; no
edit of a quarantined test file (TESTING.md "Кто что делает"); no change to `_safe_rel` (other callers).
handoff: the builder report per `.claude/agents/builder.md` rule 7 with the FR pass (sections A, C, D, G) and the witness verbatim.
designer: this draft (path on the handoff line of t-719), after Lead acceptance.

What changes:
1. `runtime_paths.declared_place(project, cfg, ref) -> tuple[str | None, str]`. Pure of writes; reads the disk only through
   `contained`. Returns `(normal_ref, "")` or `(None, why)` with `why` one of `not_relative`, `outside`, `no_project`.
   - `ref` not a str, blank, a URL (`scheme://`), `file:` in any case, a drive, rooted (`/`, `\`), a UNC -> `not_relative`.
   - `project` None -> `no_project` when the ref has a `..` part; with no `..` part -> `(posix(ref), "")` (today's lexical rule
     `_safe_rel`, nothing to resolve against: the old behaviour kept for a test or tool with no marker above `--output`).
   - Otherwise `place = normpath(project / ref)` (lexical); roots = `[project] + list(_repository_roots(project, cfg).values())`;
     accepted iff `any(contained(place, root) for root in roots)`; `normal_ref = relpath(place, project)` with `/` (no drive
     can appear: `contained` refuses another drive first). A `ValueError` from `relpath` -> `outside`.
   - `cfg` not a dict / no `code_repos` -> roots = `[project]`.
2. `_record_source` ref block: replace the `_safe_rel` test with `declared_place(nearest_project(Path(args.output).resolve().parent.parent),
   _config_of(that project), ref)` (URLs keep today's road; the credential and exclusion checks follow unchanged and take
   `normal_ref`). Refusals, each exit 2 (EXIT_USAGE), inventory untouched, each text keeping the existing needle
   "give the locator relative to the project" so the existing rows stay green:
   - `not_relative` -> today's text, plus "; a document of a declared repository is named from the project, for example
     `<code_repos path>/<path inside it>`".
   - `outside` -> "give the locator relative to the project: `<ref>` resolves outside the project and every declared
     repository (code_repos); name a file inside one of them, or save the text under work/raw/ and record that path".
   - `no_project` -> "give the locator relative to the project: no qa-factory/config.json above --output, so a `..` path cannot
     be checked against the declared repositories; record the text under work/raw/ with that path".
   - NEW after the predicate: `normal_ref` names an existing FOLDER (resolved against the project) -> "give the locator
     relative to the project: `<ref>` is a folder; one record per document: --ref `<ref>/<file name>`" (when `--file` resolves
     inside that folder, the example is that file's own normal ref).
   - The stored ref, the exclusion match and `text_snapshot` use `normal_ref`.
3. `source_inventory.text_file_problem(path) -> str` ("" = text): reads at most DOC_SNIFF_BYTES = 4096 bytes; `""` unless:
   unreadable (`OSError` -> `unreadable`), size 0 or (size <= 4096 and the slice is whitespace only) -> `empty`, a NUL in the
   slice -> `not_text`, the slice does not decode as UTF-8 (BOM allowed; a multibyte character cut at the slice end tolerated
   by retrying with up to 3 trailing bytes dropped) -> `not_text`. The SAME criteria as record-source's whole-file test on
   the slice.
4. `source_inventory.document_place_lines(cfg, project, task_root) -> list[str]` (reads disk, writes nothing). For each
   `requirements_sources` row in order, the first REQUIREMENT_SOURCE_LINE_LIMIT rows, that is a dict, `status == "verified"`,
   whose kind the table routes `route == "grep"` (through `requirement_source_kinds()`), and whose locator holds no
   credential (`SECRET_QUERY_RE`):
   - `declared_place(project, cfg, locator)`: `None` -> one line `<name>: <locator> is outside the project's repositories:
     not listed` (any `why`); the place is a root itself (the project or a code_repos root) -> nothing (today's grep line
     stands for a whole repository); a file -> nothing (the grep line covers it); missing -> `<name>: <locator> is not on disk
     here: a gap with that reason, not a question`.
   - A folder: walk it in sorted order, `followlinks=False`, skipping names starting with `.`. Depth: a file directly in the
     folder is depth 1; folders at depth DOC_DEPTH = 3 are not entered. At most DOC_ENTRIES_SCANNED = 2000 directory entries
     are examined per row. Each file: its own `declared_place` (a symlink resolving outside fails here), `text_file_problem`,
     the credential test on its normal ref, the length test (`len(normal_ref) > REQUIREMENT_SOURCE_LOCATOR_LIMIT`), and the
     exclusion filter `SE.first_ref_match(SE.live(task_root), normal_ref)`.
   - Lines: heading `Documents under <locator> (record each one you read on its own: record-source --ref <the path as listed>
     --relation normative; a first look at each, charter: the walk of references):`, then up to DOC_FILES_LIMIT = 25 lines
     `- <normal_ref> (<n> B)`, suffix ` over the read cap: read it with offset/limit` when `size_limit_of(task_root)` > 0 and the
     size exceeds it. Then, each only when its count > 0, ONE line each: `- and <k> more under <locator>: list them yourself`;
     `- <j> file(s) not listed: not text or empty`; `- <w> file(s) withheld: a credential-like name`; `- <l> file(s) not listed:
     name too long`; `- <x> file(s) not listed: outside the declared repositories`; `- <e> file(s) left out by the person's word`;
     `- <d> folder(s) deeper than 3 levels not walked under <locator>: list them yourself`; `- the walk stopped after 2000
     entries under <locator>: list the rest yourself`. A folder with no listable file and all counts 0 -> ONE line `<name>: no
     text file under <locator>`.
   - Total cap DOC_FILES_TOTAL = 40 listed paths over all rows; once reached, each later folder row gets ONE line `<name>:
     <locator>: not listed (the list is full); search it yourself`.
   - `OSError` on a folder -> `<name>: <locator> could not be read here (<ErrorName>): a gap with that reason`.
   - No such row, `requirements_sources` absent / [] / not a list, the kinds table unreadable (`ValueError`) -> `[]`.
   - `SE.ExclusionRecordError` -> `[]` (the whole listing).
5. `role_lines` (`qa-scout`): insert `document_place_lines(self.config, self.project, self.task_root)` right AFTER
   `requirement_source_lines(...)` and BEFORE `self.left_out_lines()`.

edges (each with the invariant it protects):
- POSITIONAL: the listing follows the row lines it details and precedes `left_out_lines`. Invariant: a source line is read
  before its detail; the person's exclusions stay the last word, and an unreadable exclusion record is still a `Refusal`
  (from `left_out_lines`), never swallowed by the listing.
- POSITIONAL in `_record_source`: the predicate runs BEFORE the credential, exclusion and text checks, the folder test right
  after the predicate. Invariant: no disk read of `--file` and no write happens for a ref that is refused; a left-out source
  stays refused under its normal spelling (`docs\a.md` and `docs/a.md` are one exclusion match).
- TEMPORAL: configs written before A-1 hold file rows only (the stand: README) -> no listing; folder rows written after A-1
  get it. Inventories written before this node keep their records; a document recorded before under a backslash or `./`
  spelling and re-recorded now under the normal ref is a second record (accepted: one-off, the old spelling was never
  produced by the brief).
- Limits AT and BEYOND (one row each): 25 listed / 26 -> 25 + "and 1 more"; total 40 / 41 -> next row "the list is full";
  depth 3 file listed / a folder at depth 3 counted "not walked"; 2000 / 2001 entries; locator length 200 / 201 chars
  (listed / "name too long"); sniff 4096: a valid file whose first non-UTF-8 byte is at offset 4097 is listed and then
  refused by record-source (the allowed error, stated in the docstring: the listing is advice, the refusal names its door).
- Empty/absent: no `code_repos` -> roots = project only; a `code_repos` path that does not exist -> its root contains
  nothing it can prove (`contained` compares as spelled; `normpath` keeps it lexical): a ref into it is accepted only if
  lexically inside, never if a realpath elsewhere; a missing locator -> the "not on disk" line; empty folder, images only
  -> "no text file"; a UTF-16 file -> not text; an empty file -> not text.
- Conflicting pair: "list every document" vs "never send the role to a ref record-source refuses" -> the listing applies the
  same predicate, text, credential and exclusion tests as record-source; the only remaining divergence is the sniff window
  (allowed error above).
- Conflicting pair: "folder refs refused" vs A-1's folder ROWS in config -> rows stay folders (a place to search); only a
  RECORD names a document. Invariant: one record per document.
- Outside input (config `locator`, `code_repos[].path`, the role's `--ref`): adversarial rows below.
- Direction of error: §1.

tests (one parameterised table per function; each row id names the case):
- `test_runtime_paths.py` new table `k7_declared_place` (layer table, covers runtime_paths.py): `..` into a code_repos root
  (accepted, normal ref `../repo/docs/a.md`); mixed slashes; `docs/../../x` (outside); `../../..`; absolute `C:\x`, `/etc/x`,
  `\\server\share\x`, `file:///x`, `C://x`, URL (not_relative); a symlink/junction inside the repo pointing outside
  (outside; skipped with a row-level `skipped()` where the OS cannot make a link, as the file already does); repo root on
  another drive (outside; skipped when no second drive); no project with and without `..`; ref = the project itself; a
  300-character ref; non-ASCII and space in a name (accepted).
- `test_local_keys.py` `record_source_edges` `cases` rows (refusals) and accept rows: a project with `code_repos: [{"path":
  "../sib"}]` and `../sib/docs/a.md` (exit 0, stored `canonical_ref` `../sib/docs/a.md`); `../elsewhere/a.md` (refused,
  "resolves outside"); a folder ref `docs` with `docs/` on disk (refused, "is a folder", example names the file); two
  documents of one folder recorded under their own refs -> two records (F-1 second defect, the failing-before row); the
  existing 18 rows unchanged and green.
- `test_local_keys.py` new table `document_places`: folder with 3 text files; 25 / 26; total 40 / 41; depth 3 / folder at
  depth 3; 2000 / 2001 entries (built cheaply as empty-named dot-free files only if the 10 s budget holds, else the cap is
  passed as a parameter of a private helper — the builder says which); NUL, UTF-16, empty, whitespace-only file; images only;
  empty folder; missing path; `../../..` locator; absolute locator; locator == a code_repos root; a file locator; status
  `unknown`; a route-`role` kind; a credential locator; a credential-like file name; a 201-char path; a left-out path; an
  unreadable exclusion record -> `[]`; JOIN row: every listed path fed to `record-source --ref` is accepted (exit 0).

DoD:
- `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/runtime_paths.py ai-packages/qa-factory/scripts/ticket_adapter.py ai-packages/qa-factory/scripts/source_inventory.py ai-packages/qa-factory/scripts/driver_stage_plan.py`
  — output verbatim; then run every printed file EXCEPT `test_story_run_*`, `test_controller_*` and the `SLOW_TESTS`
  members, each named in the report "судит канон пачки"; the run must include `test_local_keys.py`,
  `test_runtime_paths.py`, `test_driver_layers.py` and `test_judgment_census.py` (if `--witness-for` does not print one of
  them, the builder runs it anyway and says so). All green.
- `python -B ai-packages/qa-factory/scripts/selftest.py --lang` green.
- AR change checks in the report: grep of the diff for `"repository"`, `"file"` in the new functions (none); for `README`,
  `AUTH`, `docs` literals in code (none; positive control on a test fixture); no second containment test (the new code calls
  `contained`); `judgment:` line `adds data check ticket_adapter._record_source (declared root: xref; folder ref: shape)`;
  the census row(s) only if `test_judgment_census.py` asks (class/owner from §1).
- `architecture: AR-4, AR-9, AR-13, AR-15, AR-1, AR-3, AR-21, AR-23, AR-29 -- <how kept, one clause each>`.
- If `fixtures/driver-layers.json:487` (row `Driver.role_lines`) changes with the import, the builder updates it through
  the tool that owns it and names it.

siblings:
- axis 8 (one resolver): `declared_place` builds on `contained` / `_repository_roots` / `nearest_project`; it joins the axis
  row "The resolver (READ)" in the same commit (one clause).
- axis 34 (one road): the same predicate serves the listing, `record-source` and A-3's link listing; the skill road and the
  driver road both meet it inside `record-source`.
- axis 5 "Skill phase <-> driver": the skill road's template `s1.md:59-60` names `--ref <locator>`; changed in A-3 with the
  grep line (same wording), not here.
- sweep of `_record_source` (the enclosing block): ref check (changed), credential (n/a — unchanged, takes `normal_ref`),
  exclusion (changed: takes `normal_ref`), text test (n/a), record (takes `normal_ref`). `_safe_rel` other callers: not
  touched (they judge work-relative refs, a different fact).

### A-3 — the documents a recorded text links on disk are listed to the role and kept as reference rows (F-R2 (b))

Starts from A-2 merged (it calls `declared_place` and `text_file_problem`). If the Lead takes F-R2 (a) instead, only
item 4 and item 5 of this card are built.

given: everything A-2 names, plus `P\scripts\ticket_light.py` (:942, :1050-1269), `P\scripts\brief_pack.py` (:1353-1391,
read only), `P\skills\qa-story\phases\s1.md` (:45-76, :117-135), `P\agents\qa-scout.md` (:53, :72), §2.1 of this spec.
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\ticket_light.py (new pure function `path_candidates` only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\source_inventory.py (new `linked_documents`, new `_merge_reference_rows`, `append_attachment_references` (calls the merge), `_settle_references` (one kind added), `requirement_source_lines` (the grep branch string only), constant `LINKED_DOCUMENT_KIND`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\ticket_adapter.py (function `_record_source`: the lines after a successful record only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\skills\qa-story\phases\s1.md (the prompt template lines :59-60 only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_local_keys.py (rows in a new table `linked_documents_rows`)
non-goals: TRACKER_RULES and `s1.md:117-133` untouched (the pin of `test_tracker_route.py:581-583` stays green); no role text
other than the template line; `brief_pack.py` untouched (its generic renderer already shows the new rows); keys and URLs of a
recorded text and links in ticket/attachment texts are A-5, not here; no S1 exit check.
handoff: the builder report per builder.md rule 7, FR pass (A, C, D, E, G), witness verbatim.
designer: this draft, after Lead acceptance.

What changes:
1. `ticket_light.path_candidates(text) -> list[str]`, pure: split on whitespace and on ``()[]<>"'`|,;``; strip trailing
   `.:!?`; drop a `#...` or `?...` suffix; percent-decode once; drop empty pieces, pieces with `://` or starting `mailto:`,
   absolute machine paths (the `_LOCAL_PATH_RE` shapes and a drive / `\\`), pieces with neither `/` nor `.`, pieces longer than
   200 characters; first occurrence order, distinct. No word list (FR-12): the grammar is characters only.
2. `source_inventory.linked_documents(project, cfg, text_ref, text, task_root) -> dict` `{"paths": [normal refs], "more": k,
   "recorded": r, "checked_all": bool}`. Nothing when `text_ref` is a URL or not a path accepted by `declared_place`. Each of
   the first LINK_CANDIDATES_LIMIT = 500 candidates is resolved against the folder of `text_ref`; a candidate starting with
   `/` against the declared root holding `text_ref`. Kept iff: `declared_place` accepts it, it is an existing regular file,
   not `text_ref` itself, `text_file_problem` is "", no credential-like name, not left out (`SE.live(task_root)`;
   `ExclusionRecordError` -> nothing listed). At most DOC_FILES_LIMIT = 25 paths; `more` = kept beyond it; `recorded` = kept
   paths already a `read` source of the inventory (they are not listed, only counted).
3. `_merge_reference_rows(path, fresh, scanned_word)`: the identity merge, `scanned` and `written_by: S1` marks and atomic
   write lifted from `append_attachment_references`, which now calls it (behaviour unchanged). Rows for documents: `{"ref":
   <normal ref>, "kind": LINKED_DOCUMENT_KIND = "linked_document", "origins": ["mention:document:<text_ref>"], "status":
   "not_fetched:linked document - a first look by the walk of references"}`; a path already a `read` source is written with
   status `fetched`; scanned word `documents`. No file or an unreadable one -> nothing written (as attachments).
4. `_settle_references`: rows of kind `ticket` OR `linked_document` whose `ref` equals a recorded source's key are settled.
5. `requirement_source_lines` grep branch: `{name}: search {locator} for the story's words with Grep; record each document you
   read on its own with ticket_adapter.py record-source --ref <that document's path, relative to the project> --file <file>
   --relation normative; it reaches the manifest from the inventory` (F-R5 (a); the `whole` variable goes). `s1.md:59-60`
   changes the same way: `--ref <that document's path>`.
6. `_record_source`, after a successful record (any output form): `linked_documents(...)`; rows merged (item 3); the lines
   go to STDERR (F-R3 (a)), stdout keeps its three shapes byte for byte: `Linked from <text_ref>, inside the declared
   repositories (a first look at each, charter: the walk of references; record what can carry a requirement, or name it in
   your trail):` then `- <path> (<n> B)` per path, then when > 0: `- and <k> more linked from <text_ref>: look for them
   yourself`, `- <r> linked document(s) already recorded`, `- more than 500 names in the text: only the first 500 were
   checked`. Nothing kept -> no line. Any exception inside items 2-3 -> ONE stderr line `links of <text_ref> could not be
   listed (<ErrorName>)`, exit stays 0.

edges:
- Invariant (direction of error): a listed or row-written path is inside a declared root, an existing regular non-empty
  text file and not left out; a link the code fails to see is the allowed error (the charter rule still applies); never a
  path outside the roots. Adversarial texts (rows): `[x](../../../etc/passwd)`, a link to a symlink pointing outside, `C:\x`,
  `~/x`, `file:///x`, `https://host/docs/a.md` (URL: TL's road, not here), `docs/a.md#part`, `docs/My%20Doc.md`,
  `docs/a.md?x=1`, a 201-char link, a link to a folder, a link to the text itself, a link to an image, a credential-like
  file name, 500 / 501 distinct candidates, 25 / 26 kept links.
- TEMPORAL: `ticket-references.json` absent (a story older than S0's file) -> the stderr lines still print, no rows. Order:
  a document recorded BEFORE the text that links it -> its row is born `fetched` and it is counted "already recorded", never
  listed as unread. Invariant: a recorded document never shows as not read.
- POSITIONAL: the listing runs only AFTER `record_text_source` returned; it never changes the exit code or the record.
  Invariant: record-source's verdict does not depend on link listing.
- Empty/absent: text with no candidate -> nothing; `text_ref` a URL or a ticket key -> nothing; `text_ref` a `work/raw/`
  copy -> links resolve against `work/raw/` and usually find nothing (the allowed miss; A-2 makes the copy unnecessary).
- Conflicting pair: FR-14 (stdout shape is a contract) vs "the role must see the list" -> stderr (F-R3).
- Conflicting pair: rows of judged-not-relevant documents stay `not_fetched` (no door settles them as not relevant) and
  show again in a later S1 brief through `reference_gap_lines` -> accepted: that renderer is a scout-brief line about what
  was not read (FR-41); S2 and the S1 exit do not read the rows (R-f11). Queued as part of A-5's question.

tests: `test_local_keys.py` new table `linked_documents_rows` (one row per adversarial text above, plus: README-like text
with a relative link and a bare file name in backticks, both kept; a text recorded twice -> one row per path, origins not
doubled; a document recorded before the text -> row `fetched`; a later record of a listed path settles its row (join with
`_settle_references`); JOIN with the reader: `brief_pack.reference_gap_lines` renders an unsettled row and not a settled one;
`--summary` stdout still parses as one JSON line with a listing present; an attachment row merged by
`append_attachment_references` unchanged (refactor guard: the failing-if-broken row).

DoD:
- `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/ticket_light.py ai-packages/qa-factory/scripts/source_inventory.py ai-packages/qa-factory/scripts/ticket_adapter.py ai-packages/qa-factory/skills/qa-story/phases/s1.md`
  — verbatim; run the printed files minus `test_story_run_*`, `test_controller_*`, `SLOW_TESTS` ("судит канон пачки");
  `test_local_keys.py`, `test_brief_pack.py`, `test_judgment_census.py` included. All green.
- `python -B ai-packages/qa-factory/scripts/selftest.py --lang` green.
- The report lists the quarantined files whose assertions name the old grep string (`test_tracker_route.py` `grep_rows`,
  `test_requirement_sources.py`) as "red expected in quarantine-watch, not edited" (TESTING.md: a builder neither runs nor
  edits a quarantined file).
- AR checks: no `README`/`AUTH`/`docs` literal in code; `append_attachment_references` calls `_merge_reference_rows`;
  `judgment: none -- lines and rows only, the scout judges` (unless the census asks for a row: class shape/xref, owner data).
- `architecture: AR-15, AR-22, AR-13, AR-21, AR-29, AR-4 -- <one clause each>`.

siblings:
- axis 31 (one owner per aspect): the link rule's owner is `qa-scout.md:72`; the new stderr heading and A-2's heading are
  POINTERS ("charter: the walk of references"), not paraphrases. Sweep of the copies (critic F-2's nine sites): charter
  :23/:53/:72 (owner, unchanged); TRACKER_RULES[3] and s1.md:126 (pinned pair, unchanged — consistent with the owner);
  s1.md:59-60 (changed: the ref form only); grep branch (changed: ref form, no link paraphrase); local-adapter branch
  `source_inventory.py:2297-2298` (n/a: a route fact, its words are pinned by quarantined rows; queued to A-5's sweep);
  role-route branch :2308-2309 (n/a: no `--ref` is printed there); A-2 heading (pointer); `append_attachment_references`
  vs `record_text_source` (closed for document paths here; keys/URLs -> A-5).
- axis 5 "Skill phase <-> driver": s1.md template and the grep line change together (item 5).
- axis 34: one road for "the documents a text links" on both roads via `record-source`; the ticket and attachment texts
  are A-5 (a named node of this spec, so no exclusion).

### A-5 — the same link road for every text the factory reads (residual of the one-road class, node with owns and test)

Dispatched after A-3 is accepted (F-R6). Owner: Lead of pile `live-run-fvf`.
- (a) `record-source` texts get `TL.references` (keys, URLs, MRs) through `_merge_reference_rows`, as attachments do.
- (b) the S0 ticket text (`source_inventory.py:1133` writer) and attachment texts (`append_attachment_references`) get
  `linked_documents` with the declared roots as bases (a ref-less text: each root; a path found under two roots is one row
  per root, never a guess).
- (c) the question of a door that settles a `linked_document` row as "looked, not relevant" (the scout's `assess`-like
  word) — or the Lead's word that the trail is enough.
owns (to confirm at dispatch): `source_inventory.py` (`record_text_source` caller side in `_record_source`, the S0 writer
at :1133 function, `append_attachment_references`), `ticket_adapter.py` (`_record_source` tail); tests: rows in
`test_local_keys.py`. DoD: the same witness command over the owned paths; rows: a ticket text naming `docs/a.md` gives one
row; a recorded document naming `PROJ-9` gives a ticket row with origin `mention:document:<ref>`.

### Build order and the live proof

1. A-1 and A-4: built (`wip/fv123-a14` b2c082a); independent of A-2/A-3 (markdown only); merge when accepted.
2. A-2, then A-3 on A-2's branch — ONE builder, two commits (shared `source_inventory.py`, `ticket_adapter._record_source`
   and the predicate). A-3 must not start before A-2's witness is green.
3. Critic: ONE pass for the topic A-2+A-3 (R13-g), diff over 100 lines and a gate change (`record-source` refusals).
4. A-5 after A-3 is accepted.
5. A-L (live proof, moved to pile `live-runs` per PROJECT.md «Командная работа» п. 9). With A-3 the README-only stand config
   is enough; with a re-onboarded folder row A-2 is proven too. The row: "MyBooks LOCAL-1: the README is recorded under its
   own ref `../MyBooks/README.md` (no `work/raw/` copy); AUTH.md is in `work/source-inventory.json`; the register's source
   table carries it; no question about the cart-merge rule reaches the person."
   **Detector of F-A1 (a)** — where it is measured: at the A-L review by the Lead, from two persisted carriers and one
   recomputation: (i) every `linked_document` row of `work/ticket-references.json` is `fetched` or named in
   `work/handoffs/S1-qa-scout-<n>.yaml` `tried` / `unresolved` or in the manifest's `unresolved_facts`; (ii) the A-2 listing
   is NOT persisted (the prompt lives only in the host transcript; Grep for `Requirement sources` over the task folder found
   nothing, positive control `MyBooks README` found 46 files), so it is recomputed by calling `document_place_lines` on
   `state/config-at-start.json` with the story's project and task root, and each listed path is checked the same way. The
   four-questions block of the commit names this as detector (c) and "on discipline" as (d) until a second miss promotes a
   code join.

---

## 5. Forks (returned, not decided)

- **F-R2 — the remedy for "links of a read document not followed" (A-3).**
  (a) Role text only: the grep line and s1.md:59-60 point at the charter rule; no code. Cost: ~2 lines. Against: the rule
  reached the scout twice on the live run and did not produce the look (§2.1 E1-E4); a third text is a guess.
  (b) RECOMMENDED: code lists the on-disk documents a recorded text links (A-3), in `record-source`'s output at the moment of
  recording, and keeps them as `linked_document` rows through the attachments' merge survivor (critic's option (c), adapted:
  `TL.references` cannot see relative paths, R-f9, so a pure `path_candidates` joins `ticket_light` and the disk resolution
  sits in `source_inventory`). Data, not judgment (P27); one road on both conductor roads. Cost: ~150 lines of code, one
  table of rows, a settle-kind line, and rows of not-relevant documents stay "not fetched" until A-5 (c).
  (c) Echo only (stderr list, no rows). Cost: ~70 lines. Against: nothing persists, so the F-A1 detector has no carrier for
  linked documents and the `record_text_source` docstring stays false (R-f7).
- **F-R3 — the channel of the listing.** (a) RECOMMENDED: stderr lines after exit 0; the three stdout shapes stay byte for
  byte (FR-14). Risk: a caller that treats non-empty stderr as failure (none found in the package's callers of
  `record-source`; not exhaustively verified). (b) a `linked` key in the `--summary` JSON and lines after the plain output,
  stderr only for `--json`. Against: three placements for one fact.
- **F-R4 — must `--file` hold the bytes of the on-disk `--ref`?** (a) RECOMMENDED: no check now (today's contract: the role
  records what it read). (b) refuse when `--ref` is an existing file and the bytes differ ("a receipt measured on other
  bytes never counts"). Cost of (b): a read and a compare, CRLF/BOM edge cases, a refusal on a legitimate excerpt.
- **F-R5 — the ready ref in the grep line.** (a) RECOMMENDED: always the placeholder `<that document's path>` (correct for a
  folder and a file; the pure function cannot tell them apart). (b) keep `--ref {whole}`: a ready command for a file row,
  a refused one (with door) for a folder row.
- **F-R6 — A-5 timing.** (a) RECOMMENDED: a node after A-3 is accepted (the one-road residual is a named node with owns and
  test, rule 6). (b) inside the A-2+A-3 builder now: wider diff, S0 writer touched.
- **F-R7 — test home of the listing.** (a) RECOMMENDED: `test_local_keys.py` (keep table already covering
  `source_inventory.py` and holding record-source's table). (b) `test_runtime_paths.py` (keep table; its theme is paths,
  not S1 sources).

## 6. Small choices closed by the designer

- The predicate lives in `runtime_paths` beside `contained` / `_repository_roots` (axis 8's resolver), not in
  `source_inventory`: one home for "is this path ours".
- Every path ref (not a URL) is stored in its normal form (posix, lexical `..` collapsed, `./` dropped).
- A project with no marker above `--output` keeps today's lexical rule for `..`-free refs and refuses `..` refs (FR-59).
- Limits: DOC_FILES_LIMIT 25, DOC_FILES_TOTAL 40, DOC_DEPTH 3, DOC_ENTRIES_SCANNED 2000, DOC_SNIFF_BYTES 4096,
  LINK_CANDIDATES_LIMIT 500; "large" = the guard's own read cap (`size_limit_of`), not a new number.
- Size printed as `<n> B`. Dot entries skipped; symlinks not followed by the walk and resolved by the predicate.
- Refusal texts keep the existing needle so the 18 existing rows stay green.

## 7. Four questions (rule 10), per mechanism

- `declared_place` + record-source refusals: (a) cost: one realpath per root per call, paid by the role's command; (b) axes:
  the builder enumerates every axis in the commit (here: 5, 8, 31, 34 apply; the others n/a); (c) detector: the
  `test_runtime_paths.py` and `test_local_keys.py` rows; A24 for the refusal sites if `refusal_registry` lists them; (d) on the
  execution path of every `record-source`.
- `document_place_lines`: (a) one bounded walk per S1 dispatch (40 paths, 2000 entries per row); (c) the table rows and A-L;
  (d) built into every S1 scout prompt by `role_lines`.
- `linked_documents` + rows: (a) one bounded scan per recorded text (500 candidates); (c) the rows, A-L detector (i); (d) every
  `record-source`.

## 8. Not established (stated, not guessed)

- The `--witness-for` output for the owned paths: this designer has no shell (tools: Read/Glob/Grep/Write); the DoD names the
  files that must be in the run whatever it prints.
- Whether another in-flight batch owns `runtime_paths.py` or `test_local_keys.py` (the Lead checks the owns registry).
- Whether `config_contract` allows an absolute `code_repos[].path` (not read); the predicate handles both.
- Whether adding the import changes `fixtures/driver-layers.json:487` (DoD item covers it).
- Whether `test_local_keys.py` stays under 10 s with the new tables (not in `slow_tests.json`; the 2000-entry row may need the
  parameterised cap, said in the card).
- `state/config-at-start.json` of the run equals today's stand config (52K tokens, not read; the S1 prompt in `T` line 5 shows
  the same three rows).

## 8a. Lead decisions (14.11.2026, owner away: by recommendation, reversible, in the morning report)

- F-R2 (b): code lists the on-disk documents a recorded text links and keeps them as `linked_document` rows (data, P27);
  the link rule text is not multiplied. F-R3 (a) stderr. F-R4 (a) no bytes check. F-R5 (a) placeholder ref. F-R6 (a) A-5
  is a node after A-3. F-R7 (a) `test_local_keys.py`.
- Build: ONE builder, A-2 then A-3 as two commits; dispatched only after the plan critic's pass over this redraft
  (PROJECT.md package change item 6: a refusal of `record-source` changes meaning; `contained` moves advisor -> gate).
- The owns paths of the cards are rewritten at dispatch to the builder's worktree.

## 8b. BINDING amendments after the plan critic (t-726, `docs/tasks/specs/reviews/20261114-fv1-23-a2-a3-redraft-plan-critic.md`)

They override the cards where they differ. Anchor by FUNCTION NAME and quoted text on origin/main, not by line number.

Blocking (A-2):
1. B-1: `declared_place` first REJECTS the ref when `PureWindowsPath(ref)` or `PurePosixPath(ref)` has a drive, a root or is
   absolute (as `_safe_rel` does today), then replaces every `\` with `/` and normalises with `posixpath` semantics BEFORE joining
   the project. The same steps run in the project-None branch. Every row of `k7_declared_place` and of `record_source_edges` gives
   the same result on Windows and Linux (rows: `docs\..\..\x.md` refused; `C:\x\y.md` and `C://Users/dev7/x.md` refused; the
   mixed-slash accept row stores one `normal_ref` on both).
2. B-2: in `_record_source` the credential test (`SECRET_QUERY_RE`, reads no disk) runs BEFORE `declared_place`. No refusal text
   echoes a ref or a `--file` name that matches `SECRET_QUERY_RE`. Row: `--ref ../elsewhere/token=abc123.md` -> exit 2, `abc123`
   absent from stderr; the same for a credential-like folder name on the folder refusal.
3. B-3 (witness scope): the local witness is `test_local_keys.py` and `test_role_rules.py` plus the printed files that are NOT in
   `scripts/slow_tests.json`. `test_runtime_paths.py`, `test_driver_layers.py`, `test_judgment_census.py`, `test_brief_pack.py` and
   every `test_story_run_*` are named in the report "judged by the batch canon" and are not run locally. R-f18 reads:
   "`test_runtime_paths.py` is a SLOW_TESTS member (27.0 s > slow_over_s 10)". The `k7_declared_place` table is therefore proven by
   the canon; the record-source rows in `test_local_keys.py` drive `declared_place` end to end and are the local signal (Lead's choice).

Text fixes:
4. N-1: `linked_documents` lists nothing unless `text_ref` resolves to an existing regular file inside a declared root (no key or
   word test); a ticket key, a URL and a task-relative `work/raw/...` ref therefore list nothing.
5. N-2: a rooted candidate (`/docs/x.md`) resolves against the INNERMOST declared root holding `text_ref`.
6. N-3: the s1.md edit keeps the words `text you read there is recorded` verbatim (role-rules anchor); only `--ref <locator>` changes.
7. N-4: owns add `docs/SIBLING_MAP.md` (the axis 8 row only), `ai-packages/qa-factory/changelog.d/<fragment>.md` (one per commit),
   and conditionally `scripts/tests/fixtures/driver-layers.json` and `scripts/tests/fixtures/judgment-census.json` (only the rows
   their tests name; any ratchet raise is named in the report, AR-20).
8. N-5: the builder sets the `_record_source` census row to class `xref` in the same commit (it now joins the ref to declared roots).
9. N-6: `declared_place` skips a `code_repos` entry whose path is not a non-empty string or cannot be resolved (that root holds
   nothing, no traceback). Rows: path `123`, path `""`.
10. N-7: the row in which the 40th path is listed counts its remainder in its own `and <k> more` line; dot entries are not counted
    toward DOC_ENTRIES_SCANNED.
11. N-8: with no project, the folder test is skipped (today's behaviour). "empty-named dot-free files" reads "empty dot-free files".
12. N-9: the failing-before row of F-1's second defect is the folder-ref refusal (`docs` with `docs/` on disk -> refused); the
    two-records row uses `../sib/docs/A.md` and `../sib/docs/B.md` (refused today).
13. N-10: A-3 item 5 (the grep-line string and the s1.md lines) MOVES INTO A-2, so each commit's brief names only refs its own
    `record-source` accepts.
14. Edges: `document_place_lines` derives the project with `runtime_paths.nearest_project(task_root)`, as record-source does (not
    `self.project`); a document path containing `/browse/` never settles (`_key`): stated, cosmetic, no fix; A-3 adversarial rows add
    `%00` (NUL after decoding -> not listed, no traceback); the "left-out path" row is built from a hand-made `as_written` entry and
    labelled so (no exclusion kind names a path today).
15. Volume: the builder names in one line why the four tables are as long as they are (TESTING budget).

Queue (Lead, not this builder): node A-6 — the folder listing reaches only the driver road (`role_lines`); the skill road's scout
gets no listing (R-1, axes 5 and 34), owner Lead of `live-run-fvf`; `covers` of `test_local_keys.py` in `test-layers.json` gains
`ticket_light.py` and `runtime_paths.py` (busy file).

Collision answer (critic's question): `driver_stage_plan.py` is edited by topic "stage critics removed" (A1c, awaiting merge) and
by FV1-9 card A. This builder touches ONLY `role_lines` there, starts from origin/main after A1c is merged, and FV1-9 card A is
dispatched after this node's A-2 commit is merged (one writer of the file at a time).

## 9. Reading trail

Read: the t-706 verdict whole; the FV1-23/20 spec whole (Part A, amendments); `ticket_adapter.py:2180-2249`, `:2027-2046`,
`:1753-1767` (+Grep defs); `source_inventory.py:1890-2329`, `:2673-2768` (+Grep defs, `ticket-references`); `ticket_light.py:173-212`,
`:1050-1269` (+Grep); `runtime_paths.py:193-213`, `:275-292`, `:335-357`, `:479-517`, `:920-925`, `:960-989`; `driver_stage_plan.py:1-80`;
`driver_sources.py:776-790` (Grep); `driver_core.py` (Grep project/task_root); `brief_pack.py:1339-1391`, `:4421-4424` (Grep);
`qa-scout.md` whole; `s1.md:40-139`; `test_tracker_route.py:560-600`; `test_local_keys.py:30-69`, `:413-522` (+Grep defs);
`test_runtime_paths.py` (Grep defs); `test_ticket_adapter.py` (Grep defs); `test-layers.json:1-40`, `:2893-2917`, `:4686-4710`,
`:6490-6500` (+Grep); `slow_tests.json` (Grep); `scenario_walk.py:1-120` (+Grep); `docs/TESTING.md` whole; `docs/SIBLING_MAP.md`
axes 5, 8, 31, 34 (+headings); `design/architecture.md:68-167`, change-check lines (Grep). Stand: `S\MyBooks\docs\AUTH.md` (Grep
cart/merge/guest); LOCAL-1 `work/handoffs/S1-qa-scout-1.yaml:160-184`, `work/briefs/S1-qa-scout-1.launch.md` (Grep); transcript `T`
(Grep `-o` for TEST_IDS/AUTH.md/record-source/the refusal).
Negative claims with positive controls: "no S1 exit reads ticket-references.json" (Grep over scripts/*.py found brief_pack.py —
the same call); "TL.references sees no relative path" (read `_LOCAL_PATH_RE` and the extraction order directly); "the A-2 listing is
not persisted" (Grep `Requirement sources|app-readme` over the task folder: none; control `MyBooks README`: 46 files); "no
record-source test in test_ticket_adapter.py" (Grep defs + `record.source` found none there; the same Grep found 31 hits in
test_local_keys.py).
Needed beyond the manifest: the stand copy `C:\QAFactory\mybooks-stand\...` and the transcript under `C:\Users\i_mas\.claude\projects\...`.
