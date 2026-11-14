# Critic on PLAN (re-review): FV1-23 nodes A-2 / A-3, redraft t-719

Under review: `docs/tasks/specs/20261114-fv1-23-a2-a3-redraft-spec.md` (whole, incl. §8a Lead decisions).
Earlier verdict: `docs/tasks/specs/reviews/20261114-fv1-23-20-plan-critic.md` (t-706). Parent spec: `docs/tasks/specs/20261113-fv1-23-fv1-20-spec.md`.
Package facts read at **origin/main 9c15423** (`git show 9c15423:<path>`), NOT in `.claude/worktrees/read-main`:
that worktree is at 50d9012 (wave 6). Between the two, of the files the cards touch only `driver_stage_plan.py` changed
(+14/-8) and `test-layers.json` (+8/-2); I read both at 9c15423. One pass, no code edited.

## Verdict

**fit_with_fixes**: three findings block the dispatch until the spec takes their amendments (B-1..B-3, each one sentence below).
The rest are text fixes (N-1..N-10). The redraft closes F-1 (both defects), F-2, F-5 a-i, and closes F-6 only in part. The
architecture is right: one predicate in `runtime_paths` on top of `contained`, the listing is data, and the link rows go
through the attachments' merge survivor. Accepting the work, amending the spec and dispatching are the Lead's decisions
(role rule 6).

---

## Blocking until amended

### B-1 (key 3): on POSIX, `declared_place` as written accepts what `_safe_rel` refuses today. It breaks two of the 18 existing rows on CI, and the Windows witness stays green

Spec, A-2 item 1: "`place = normpath(project / ref)` (lexical)". It also lists "a drive" and "rooted (`/`, `\`)" as not_relative,
but never says these are tested in BOTH dialects or that `\` counts as a separator on every OS. Today's rule
(`source_inventory.py:2712-2718`, `_safe_rel`) is "A work-relative path in either spelling ... whichever OS reads it". It
checks `PureWindowsPath` and `PurePosixPath`. The canon runs on `ubuntu-latest` (`.github/workflows/canon.yml:44`).

Probe (a pure calculation, heredoc), posixpath against ntpath for a project `/home/u/proj` / `C:\proj`:
```
'..\\MyRepo/docs\\a.md'  posix: /home/u/proj/..\MyRepo/docs\a.md | relpath ..\MyRepo/docs\a.md | inside: True
                         nt   : C:\MyRepo\docs\a.md | inside: False
'docs\\..\\..\\x.md'     posix: /home/u/proj/docs\..\..\x.md | relpath docs\..\..\x.md | inside: True
                         nt   : C:\x.md | inside: False
```
Failure scenarios on Linux (CI, or any Linux or macOS user of the factory):
- `--ref 'docs\..\..\x.md'` is refused today on every OS. Under the redraft it is ACCEPTED and stored with backslashes, and
  read on Windows that stored ref names a file outside the project. This breaks the stated direction of error (§1: "a path
  outside every declared root is NEVER accepted, listed or stored") and AR-4.
- If "a drive" is read with the native `os.path.splitdrive`, then the existing rows "drive ref" `C:\x\y.md` and "a drive taken
  for a scheme" `C://Users/dev7/x.md` (`test_local_keys.py:471,475`) are accepted on Linux: they are lexically inside the
  project. Both rows go red on CI only, and the builder's Windows witness passes.
- The new accept row "mixed slashes" stores a different `normal_ref` on Linux than on Windows, so the row cannot be portable.
- The project-None branch says "with no `..` part -> `(posix(ref), "")`". If `posix()` swaps `\` for `/` AFTER a native
  `..` test, then `docs\..\..\x` is stored as `docs/../../x`.

Surface: the syntax reader of `--ref`. Neighbouring classes walked: encoding (a `%2e%2e` in an A-3 link is decoded before
the predicate, fine), nesting (`a/./b/../c`, fine), magnitude (300 characters, see N-8), empty or blank input (not_relative,
fine).

**Amendment B-1:** "`declared_place` first rejects the ref when `PureWindowsPath(ref)` or `PurePosixPath(ref)` has a drive, a
root or is absolute (as `_safe_rel` does), then replaces every `\` with `/` and normalises with `posixpath` semantics before
joining the project. The same steps run in the project-None branch, and every row of `k7_declared_place` and of
`record_source_edges` must give the same result on Windows and Linux."

### B-2 (keys 3, 7): the new refusal texts echo `<ref>` BEFORE the credential check, so a credential-like ref is printed

Spec, A-2 item 2, refusal texts: "`<ref>` resolves outside the project ..." and "`<ref>` is a folder; ... --ref `<ref>/<file name>`".
The POSITIONAL edge: "the predicate runs BEFORE the credential, exclusion and text checks". Today the path refusal does not
echo the ref (`ticket_adapter.py:2202`), and the credential refusal says "the value is not shown"
(`ticket_adapter.py:2207-2208`). `SECRET_QUERY_RE = (?i)(token|secret|password|key)=([^&#]*)` (`config_contract.py:59`)
matches inside a path too.

Input: `--ref ../elsewhere/token=abc123.md`. Today the output is "give the locator relative to the project ..." and the
secret is not printed. Under the redraft the output is "`../elsewhere/token=abc123.md` resolves outside ...", so the secret
reaches stderr and from there the host transcript. The existing guard row ("record-source edge: the secret value is not
printed", `test_local_keys.py:484`) holds only because no current case combines the two. The same leak opens on the folder
text, for a folder whose name is credential-like.

**Amendment B-2:** "In `_record_source` the credential test (`SECRET_QUERY_RE`, it reads no disk) runs before `declared_place`.
No refusal text echoes a ref or a `--file` name that matches `SECRET_QUERY_RE`. Add the row `../elsewhere/token=abc123.md`
(exit 2, `abc123` absent from stderr)."

### B-3 (keys 1, 8, 9): the witness DoD contradicts itself and PROJECT.md p. 2. R-f18 is wrong about `slow_tests.json`

R-f18 says "Neither is in `slow_tests.json` above 30 s (`test_runtime_paths.py` 27.0 s ...)". No 30 s threshold exists. The
file's thresholds are `slow_over_s: 10, fast_under_s: 5`, and every file it lists is a SLOW_TESTS member, the set that
`--fast` skips (`selftest.py:998-1005`, `scripts/slow_tests.json` head). At 9c15423 the listed files include
`test_runtime_paths.py` 27.0, `test_driver_layers.py` 32.5, `test_judgment_census.py` 33.3 and `test_brief_pack.py` 34.6.
`test_local_keys.py` and `test_role_rules.py` are not listed.

The A-2 DoD says to run the printed files "EXCEPT ... the `SLOW_TESTS` members", and then says "the run must include
`test_runtime_paths.py`, `test_driver_layers.py` and `test_judgment_census.py`". A-3 likewise requires `test_brief_pack.py`.
Those are conflicting requirements, and PROJECT.md «Как принимается изменение пакета» p. 2 decides between them: "медленный
файл (`SLOW_TESTS`, ...) локально не запускается и не ждётся". Earlier finding F-6 is therefore closed only in part: the
homes are named, but the witness scope is not lawful.

There is a second gap in the same area. My re-run of `--witness-for ticket_light.py` does not print `test_local_keys.py`,
yet that file is where the `path_candidates` rows go. `--witness-for s1.md` prints only the scenario layer, while the s1.md
template edit sits under the role-rules anchor (N-3), which `test_role_rules.py` (keep, register, not slow) judges.

**Amendment B-3:** "The local witness is `test_local_keys.py` and `test_role_rules.py` plus the printed files that are not in
`slow_tests.json`. `test_runtime_paths.py`, `test_driver_layers.py`, `test_judgment_census.py` and `test_brief_pack.py` are
named in the report as «судит канон пачки» and are not run locally. R-f18 is corrected to 'test_runtime_paths.py is a
SLOW_TESTS member (27.0 s > slow_over_s 10)'."

Consequence for the Lead: the `k7_declared_place` table in `test_runtime_paths.py` is then proven only by the batch canon.
The record-source rows in `test_local_keys.py` exercise `declared_place` end to end, which gives a local signal. This is
acceptable, but it is the Lead's choice.

---

## Text fixes (non-blocking; each one sentence to paste)

- **N-1 (key 5, A-3 item 2 against its own edge):** the edge "`text_ref` ... a ticket key -> nothing" cannot come out of the
  rule as written. `declared_place` accepts `PROJ-9` as a relative path, because TRACKER_RULES[3] records tickets with
  `--ref <KEY>` (`source_inventory.py:2151`), so a recorded ticket's links would be resolved against the project root. Paste:
  "`linked_documents` lists nothing unless `text_ref` resolves to an existing regular file inside a declared root (no key or
  word test); a key, a URL and a task-relative `work/raw/...` ref therefore list nothing."
- **N-2 (key 5, A-3 item 2):** "the declared root holding `text_ref`" for a candidate that starts with `/` is ambiguous when
  roots nest. A `code_repos` path `..` is a legitimate layout: tests inside the app repository, see
  `references/config-keys.json:304`. Paste: "for a rooted candidate, the innermost declared root holding `text_ref`."
- **N-3 (key 9, A-3 item 5):** `s1.md:59` carries the role-rules anchor "text you read there is recorded"
  (`design/role-rules.json:446`). Paste: "the s1.md edit keeps the words `text you read there is recorded` verbatim; only
  `--ref <locator>` on line 60 changes."
- **N-4 (key 9, owns):** the cards make the builder write outside owns. A-2 siblings says "joins the axis row ... in the same
  commit", which is `docs/SIBLING_MAP.md`. The DoD names the fixtures `driver-layers.json` (the row is now `:490`, not `:487`)
  and `judgment-census.json`. A package change also needs a changelog fragment `changelog.d/*.md`. Paste: "owns adds
  `docs/SIBLING_MAP.md` (axis 8 row only), `ai-packages/qa-factory/changelog.d/<new fragment>.md`, and conditionally
  `scripts/tests/fixtures/driver-layers.json` and `scripts/tests/fixtures/judgment-census.json` (rows named by their
  tests)."
- **N-5 (key 2/§1 against census):** §1 classes the `_record_source` check "xref". The census row is
  `{"file": "ticket_adapter.py", "function": "_record_source", "class": "shape"}` (`judgment-census.json:1146`, one row per
  function). The DoD's "census row(s) only if the test asks" leaves §1's class recorded nowhere. Paste: "the builder sets the
  `_record_source` census row to class `xref` (owner data) in the same commit, or §1 says `shape`."
- **N-6 (key 7, outside input `code_repos[].path`):** `_repository_roots` does `Path(project) / item['path']` and
  `.resolve()` (`runtime_paths.py:288-291`). A non-string path (`123`) raises TypeError, and a path holding NUL raises
  ValueError. Both happen in record-source's ref block, which is outside its `try`, so the command crashes with a traceback.
  Paste: "`declared_place` skips a `code_repos` entry whose path is not a non-empty string or cannot be resolved (that root
  holds nothing); battery rows: path `123`, path `\"\"`."
- **N-7 (key 7, A-2 item 4 limits):** two edges are silent. (a) When the total cap of 40 is reached in the MIDDLE of a row, is
  the rest of that row "and k more under <locator>"? (b) Do skipped dot entries count toward the 2000 examined? Paste: "the
  row in which the 40th path is listed counts its remainder in its own `and <k> more` line; dot entries are not counted
  toward DOC_ENTRIES_SCANNED."
- **N-8 (key 7, folder test with no project):** "names an existing FOLDER (resolved against the project)" has no base in the
  project-None branch. Paste: "with no project, the folder test is skipped (today's behaviour)." Also: "empty-named
  dot-free files" (2000-entry row) should read "empty dot-free files".
- **N-9 (key 8, test row label):** "two documents of one folder recorded under their own refs -> two records (F-1 second
  defect, the failing-before row)". With refs inside the project, this row passes before the change too (`docs/A.md` and
  `docs/B.md` are accepted today). The row that fails before the change is "folder ref `docs` with `docs/` on disk ->
  refused". Paste: "the failing-before row of F-1's second defect is the folder-ref refusal; the two-records row uses
  `../sib/docs/A.md` / `B.md` (refused today)."
- **N-10 (key 9, cut):** inside A-2's own commit, the grep line still prints `--ref {whole}` (a folder for folder rows) while
  A-2 starts refusing folder refs. A-3 item 5 removes the contradiction one commit later. The release carries both, but
  under F-R2's alternative branch item 5 is still built. Paste: "A-3 item 5 (the grep-line string and s1.md:59-60) moves into
  A-2, so each commit's brief names only refs its record-source accepts."

## Rule-19 residual (one action, one road), a proposed node with an owner

- **R-1 (keys 6, 11; axes 5 and 34):** A-2's folder listing reaches only the DRIVER road. `requirement_source_lines` and the
  new `document_place_lines` are called only from `driver_stage_plan.role_lines`. A git grep at 9c15423 finds no other
  caller; the positive control, the same grep on `source_inventory.py`, finds 7 hits. On the skill road the conductor fills
  "Requirement sources: <the lines of config.requirements_sources>" by hand (`s1.md:59`), and no listing reaches that
  scout. The A-2 axis-34 line ("both roads meet it inside record-source") is true of the predicate, not of the listing. A-3
  is two-road through record-source output, which is fine. This is a second road for one action ("tell the scout what
  documents a place holds") with no data row and no word from the owner. It must be either a fix of this round (put the call
  where both roads read, for example the scout brief, if brief_pack builds it on both roads; NOT verified by me) or a node.
  **Proposed node A-6, owner: Lead of pile `live-run-fvf`; the Lead opens it.**

---

## Answers per key

**1. Earlier findings.**
- F-1 first defect: closed by A-2 items 1-2 (a `..` ref inside a `code_repos` root is accepted; join row). It holds apart from
  B-1's dialect hole.
- F-1 second defect: closed (the folder refusal at A-2 item 2, the per-document listing, the grep line at A-3 item 5). The
  failing-before label is wrong (N-9).
- F-2: closed. TRACKER_RULES and s1.md:126 are untouched (verified: `source_inventory.py:2153-2154` equals `s1.md:126`).
  The headings point at the charter section name. One remaining wording note: the A-3 heading's "record what can carry a
  requirement" is a mini-paraphrase of charter :53; it is harmless but not a pure pointer.
- F-5 a: closed (`SE.live(task_root)`, `source_exclusions.py:330-331`).
- F-5 b: closed (an unreadable record gives `[]`, then `left_out_lines` raises the Refusal, `driver_sources.py:780-784`).
- F-5 c: closed (depth defined, 2000-entry cap).
- F-5 d: closed (length 200 counted).
- F-5 e: closed (empty or whitespace = not text).
- F-5 f: closed (withheld).
- F-5 g: closed (`<n> B`).
- F-5 h/i: closed.
- F-6: closed in part, see B-3.

**2. Facts.** Each was checked at its carrier at 9c15423:
- Hold: R-f1 (`ticket_adapter.py:2200-2204`, `source_inventory.py:2712-2718`), R-f2, R-f3 (`:1896-1913`), R-f4 (`:2301-2306`),
  R-f5 (`runtime_paths.py:193, 285-292, 479-517, 920-925`), R-f6, R-f8, R-f10 (`:2006` `kind == "ticket"`), R-f12
  (`driver_stage_plan.py:11-48`, the numbers moved and the code is the same; `driver_core.py:457-462`), R-f13, R-f14, R-f15,
  R-f16, R-f17 (the test parses `got.out` with `json.loads`, `test_local_keys.py:428`), R-f19 (`:468-472, 423, 491`).
- **R-f18 is wrong** (B-3).
- Negative claims, each with a positive control:
  - R-f7 "adds no reference rows": the writers of `ticket-references.json` at 9c15423 are `source_inventory.py:1133` (S0),
    `ticket_adapter.py:1662` (paste references), `append_attachment_references` (:2053) and `_settle_references` (status
    only). `record_text_source` -> `update_inventory` adds no row. The same git grep found all four writers. **Holds.**
  - R-f9 "does not extract a relative path": I read `_LOCAL_PATH_RE` (`ticket_light.py:942`), which matches only `~/...` or a
    drive with a backslash. URLs are http(s) only. The only `local_path` rows come from that regex (`:1160-1162`).
    **Holds.**
  - R-f11 "no S1 exit reads ticket-references.json": a case-insensitive git grep of `ticket-references|ticket_references` at
    9c15423 over the package, outside tests, finds only `brief_pack.py`, `driver_s0.py`, `ticket_adapter.py` and
    `source_inventory.py` among scripts (plus docs and the kinds JSON). `controller.py` has 0 hits, and the same call
    counted 5 hits of `source-inventory` there. A second grep for the alternative spelling `references.json|REFERENCES_FILE`
    finds only brief_pack. **Holds.**
  - R-f20: `scenario_walk.py:40,46-47`. The doors are exit_gate/joint/start/gate/delivery and no record-source hit appears;
    the control, `exit_gate`, has 13 hits. **Holds.**
- E1: holds (transcript line 5 carries `app-readme: search ../MyBooks/README.md ...` and "A key or link in what you read").
- E3: holds (line 63 `grep -n -i "cart" ../MyBooks/TEST_IDS_REFERENCE.md`).
- E4: holds (`AUTH.md` occurs on line 57 only).
- E5: holds (`MyBooks/docs/AUTH.md:8` read verbatim).
- E6: holds for the stored `canonical_ref: qa-factory/artifacts/LOCAL-1/work/raw/MyBooks-README.md` and for the refusal
  string at line 82. Lines 80 and 87 were not re-traced.
- E2: not checked beyond line 57 holding the README text.

**3. Meaning change at the gate.** For each branch of A-2.1:
- Lexical pass when project is None: acceptable and declared. It is today's lexical rule and only tests or tools meet it,
  since a real task folder always sits under a marker. It needs B-1's dialect rule and N-8.
- A `code_repos` path that does not exist: `contained` compares as spelled (`runtime_paths.py:484-486`). Lexically inside is
  accepted and a realpath elsewhere is not. Safe.
- Symlink or junction: `_rest_under` takes realpath of both sides, so a link inside a repository that points outside is
  refused. Safe.
- Another drive: `_drive` differs, so the answer is None before realpath (`:490-491`). Safe. Such a repository can then never
  be reached by a relative ref; the door "save the text under work/raw/" covers it.
- `normpath` before `contained`: `link/../x` normalises lexically to `x`, which differs from what the OS resolves. This is a
  provenance question, not a containment leak: the stored lexical ref is inside and later readers open the lexical path.
  Acceptable.
- Direction of error: right, once B-1 and B-2 are applied.
- Regressions for accepted refs:
  - The 18 rows stay green on Windows logic (their needle is kept); 2 of them break on Linux without B-1.
  - `work/raw/` refs (project-relative or task-relative) are inside and accepted.
  - URLs keep today's road.
  - Ticket keys (`PROJ-9`) are accepted, normal form unchanged. They would be refused only if a folder of that exact name
    exists at the project root (negligible).
  - Newly refused: a ref through a project symlink or junction pointing outside every root, and `.` (a folder). Both fall
    under the declared allowed error, and the door is named.
- Folder refusal when `docs` is absent (R-f19): `is_dir` is False, so the ref is accepted. Safe.

**4. Stored-ref normalisation.**
- `update_inventory`: identity is exact `canonical_ref`. An old `./x` spelling and a new `x` become two records, as declared
  in TEMPORAL.
- `_settle_references`: keys by `_key(item)` = canonical_ref split at `/browse/` (`source_inventory.py:2673-2674`). A row
  ref written by the same `declared_place` joins. Edge: a document path containing `/browse/` never settles. This is cosmetic
  (a row stays `not_fetched`); note it in A-3 edges.
- Exclusions: `first_ref_match` matches tickets, MRs, URLs and git refs by `as_written` or the parsed target
  (`source_exclusions.py:401-414, 790-820`). `_parse_target` gives "unreadable" for a bare path (`:138-185`), and
  `read_record` refuses a non-KINDS target (`:316`). So no exclusion can name a file path today, and normalisation cannot
  break a match. Consequences: the spec's claim "`docs\a.md` and `docs/a.md` are one exclusion match" is vacuous, and the
  listing's "left out by the person's word" count is always 0 for paths. The test row "a left-out path" can only be built
  from a hand-made `as_written` entry, which the builder should label as such.
- `text_snapshot`: the title is the last part after `[\\/]`, unchanged.
- `stable_source_id("text", ref)`: a new id for a new spelling, as declared.
- `_safe_rel` callers (`branch_accounting.py:355,873`, `source_inventory.py:1180,2798,3141,3191,3600,3783`) judge
  snapshot/local/evidence refs, never `canonical_ref`. `validate_inventory` does not shape-check `canonical_ref`, and
  `context_bundle.py:197,229` takes `ref` as a string. No reader refuses a stored `..` ref. AR-13 and AR-22 hold.

**5. A-3 readers, path_candidates, stderr, refactor.**
- `brief_pack.reference_gap_lines` (`:1358-1391`) renders any non-`fetched` row generically and never blocks; it runs only for
  briefs naming `work/ticket-snapshot.json`, which is the scout's alone (`brief_pack.py:92`).
- `driver_s0.s0_references_allow_no_change` (`:920-931`) reads only `is_change` kinds, so `linked_document` is inert there.
  No reader treats the new kind as a question or a count.
- `references/reference-kinds.json` classifies links found in ticket text. `local_path` is already a code-produced kind
  outside it (`ticket_light.py:1162,1261`), so `LINKED_DOCUMENT_KIND` as a code constant is consistent.
- Risk, accepted by the spec: README-style texts name `package.json`, config files and so on. These pass the text filter and
  become up to 25 `not_fetched` rows per text. They can crowd `REFERENCES_SHOWN = 20` in a later brief, though the original
  rows come first since rows are appended.
- `path_candidates`: character grammar only, no project names. FR-12 and P2 hold. The adversarial list should add `%00`
  (NUL after decoding). It is safe today because `_rest_under` catches ValueError, but name the row.
- stderr (F-R3): no package script runs `record-source` as a subprocess. A git grep of `record-source` at 9c15423 outside
  tests finds only text doors. Friction classifies by the host's `is_error` flag alone (`friction.py:270,415`), so stderr
  with exit 0 is not friction. **Safe.**
- `_merge_reference_rows`: the lifted identity merge adds origins and never changes the status of an existing row. Attachment
  behaviour is kept, and the refactor-guard row is in the test list.

**6. P27 / AR-29, P5 / FR-50.** No line judges relevance and none blocks on it. Listing failures never change the exit code
(A-3 item 6). Census classes: see N-5. P5: the listing names only existing, contained, non-empty text files and says
"not on disk here: a gap" for a missing locator. It never sends the role to something unreachable, apart from the declared
sniff-window divergence.

**7. Edges.** Edges the cards create and leave silent:
- N-6: a malformed `code_repos` entry.
- N-7: the total cap reached in the middle of a row; dot entries against the scan count.
- N-8: the folder test with no project.
- N-1: a key as `text_ref`.
- N-2: a rooted candidate under nested roots.
- B-2: refusal texts echoing secrets.
- A path containing `/browse/` never settles (key 4).
- The listing's project (`self.project` = `hooklib.project_root()`, env first, `driver_core.py:457`) against record-source's
  project (`nearest_project(output)`). These could differ, and the join would then break. Paste: "`document_place_lines`
  derives the project with `runtime_paths.nearest_project(task_root)`, as record-source does."

TEMPORAL and POSITIONAL invariants are stated and right, except that B-2 changes the order.

**8. Tests.**
- Homes: `test_local_keys.py` (keep, table, covers `source_inventory.py` and `ticket_adapter.py`) and `test_runtime_paths.py`
  (keep, table).
- The battery covers `--ref` and the recorded text; it lacks non-string or empty `code_repos` paths (N-6) and NUL after
  decoding.
- The witness: see B-3.
- No quarantined file is edited. The list of expected quarantine reds is right (`test_tracker_route.py`,
  `test_requirement_sources.py`: quarantine cohort 8073673).
- The 2000-entry row is feasible. Empty files are cheap on Linux and Windows; the fallback (a private-helper cap
  parameter) is acceptable.
- `test_local_keys.py`'s `covers` lacks `ticket_light.py` and `runtime_paths.py`, so future edits of `path_candidates` will
  not print it. Queue one `covers` edit of `test-layers.json` (busy file: an `очередь:` line) or accept the gap explicitly.
- Volume: the four tables risk more test lines than code (TESTING «Бюджет»). The builder names the reason in one line.

**9. Feasibility and cut.** ONE builder for A-2 then A-3 is right: shared `source_inventory.py`, `_record_source` and the
predicate. Each item names a file, a function, a behaviour and a test, so a weaker model can execute them, given the
amendments. Owns are insufficient (N-4). Collisions with in-flight work: I cannot establish batch status from the files. A
grep found mentions of these files in four batch files (collect/1, grounding/1, onboarding-forge/2, onboarding-hooks/8),
whose status I did not resolve. **Question to the Lead:** does any batch in progress own `source_inventory.py`,
`ticket_adapter.py`, `runtime_paths.py`, `test_local_keys.py` or `driver_stage_plan.py`?

**10. §8a.**
- F-R2 (b): holds against P1 and P27. Code reads documents and lists data; the scout judges; failures report and do not
  stop. The `not_fetched` rows are FR-41 data, not a verdict.
- F-R3 (a): holds; callers verified (key 5).
- F-R4 (a): holds. It is today's contract and refs could never be verified before either.
- F-R5 (a): holds.
- F-R6 (a): holds. A-5 is a named node with an owner and a DoD (rule 19).
- F-R7 (a): holds.

None is wrong against the rules.

**11. Class completeness (SIBLING_MAP).**
- Axis 8: applies. `declared_place` builds on `contained`, `_repository_roots` and `nearest_project` (the row at
  `SIBLING_MAP.md:209`). Its row edit needs owns (N-4).
- Axis 5: applies. The s1.md template and the grep line change together, but the A-2 listing has no skill-road twin (R-1).
- Axis 31: applies. The headings are pointers; one mini-paraphrase remains (key 1).
- Axis 34: applies. The predicate is one road; the listing is not (R-1).
- Not named by the spec:
  - **Axis 32** (judgment census): the `_record_source` row class must be stated (N-5).
  - **Axis 18** (shrink-only ratchets): touched if `driver-layers.json` or the census move. Any raise is named in the diff
    critic's verdict, and the cards should say so.

## Standing questions

- ONE ACTION, ONE ROAD (item 12, P31): NEEDS WORK on R-1 (the listing is driver-only). Proposed node A-6, owner Lead
  `live-run-fvf`. Otherwise the plan closes the earlier one-road findings.
- DUPLICATION AND CONSISTENCY: no second containment test. `declared_place` calls `contained`, and the text test is shared
  (`text_file_problem` against record-source's whole-file test; the spec states the one divergence). One inconsistency:
  `_safe_rel` (both dialects) against the planned `declared_place` (native), which is B-1. Grepped: `_safe_rel` callers,
  `".." in` checks across scripts, `ticket-references` readers, `record-source` callers.
- CODE QUALITY (planned code): the signatures carry what their filters need (`task_root`). The bounded walk is fine. A
  malformed `code_repos` entry can crash the ref block (N-6).

## Trail

Read at 9c15423 (via `git show` into the scratchpad):
- `scripts/ticket_adapter.py:2180-2250, 2062`
- `scripts/source_inventory.py:1896-2128, 2129-2160, 2248-2312, 2338-2366, 2673-2760`
- `scripts/runtime_paths.py:185-215, 270-300, 470-520, 915-930`
- `scripts/source_exclusions.py:125-185, 286-414, 790-820`
- `scripts/driver_stage_plan.py:1-70`, `scripts/driver_sources.py:776-788`, `scripts/driver_core.py` (grep)
- `scripts/brief_pack.py:1350-1395, 4405-4440, 92`, `scripts/driver_s0.py:918-970`
- `scripts/ticket_light.py:935-950, 1150-1170, 1250-1275`
- `scripts/config_contract.py:59-100`, `references/requirement-source-kinds.json`, `references/reference-kinds.json`,
  `references/templates/config.json` (code_repos, requirements_sources)
- `scripts/tests/test_local_keys.py:1-85, 400-530`, `scripts/tests/harness.py` (temp_project, mark_project)
- `scripts/tests/scenario_walk.py:36-50`, `scripts/tests/test-layers.json` (keep/quarantine rows via json),
  `scripts/slow_tests.json`, `scripts/selftest.py:998-1135`
- `scripts/tests/fixtures/driver-layers.json` (role_lines rows), `scripts/tests/fixtures/judgment-census.json`
  (ticket_adapter, runtime_paths rows, ratchet)
- `scripts/friction.py:95-130, 270, 415`, `scripts/handoff_check.py:505-535`, `scripts/acceptance.py:1310-1332`,
  `scripts/branch_accounting.py:330-365, 860-880`
- `skills/qa-story/phases/s1.md:52-64, 120-128`, `agents/qa-scout.md:23, 53, 72`, `design/role-rules.json:446`,
  `references/artifact-writers.json`, `references/role-load.json` (grep)
- `.github/workflows/*.yml` (runs-on)
- `docs/TESTING.md` (whole), `docs/SIBLING_MAP.md` axes 8, 18, 32, 33, 34 and the headings, `plans/builder-rules.md:28-50`
- Stand `MyBooks/docs/AUTH.md:8`, LOCAL-1 `work/source-inventory.json` (grep), transcript 634b0a20 lines 5, 57, 63, 82
  (awk/grep)

Negative claims of mine, each with its control:
- "No package script outside tests runs record-source as a subprocess": git grep `record-source|_record_source|record_source`
  outside tests lists only text doors and the CLI dispatch. The same call found `ticket_adapter.py:2657`.
- "No exclusion can name a path": read `_parse_target` and `read_record` directly.
- "role-load.json has no s1.md ratchet": an E-regex grep finds the `qa-scout` rows, which is the control; there is no `s1`
  row.
- "Only driver_stage_plan calls requirement_source_lines": git grep; the control is source_inventory with 7 hits.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B-1: declared_place as written (native normpath; drive/rooted not stated as both dialects) accepts on POSIX what _safe_rel refuses on every OS today: 'docs\\..\\..\\x.md' is lexically inside on Linux and stored with backslashes, an escape when read on Windows; the existing rows 'drive ref' and 'a drive taken for a scheme' (test_local_keys.py:471,475) go red on the Linux canon while the Windows witness stays green (probe output in the report). Amendment: test drive/root/absolute in both PureWindowsPath and PurePosixPath, replace backslash with slash and normalise with posixpath before joining; rows equal on both OS.",
    "B-2: new refusal texts ('<ref> resolves outside', '<ref> is a folder') run before the credential check and echo the ref: --ref ../elsewhere/token=abc123.md prints the secret (SECRET_QUERY_RE config_contract.py:59 matches inside paths; today the path refusal echoes nothing). Amendment: the credential test first; no refusal echoes a ref or --file name matching SECRET_QUERY_RE; add that row.",
    "B-3: the DoD excludes SLOW_TESTS yet requires test_runtime_paths (27.0 s), test_driver_layers (32.5), test_judgment_census (33.3), test_brief_pack (34.6), all listed in slow_tests.json (slow_over_s 10); PROJECT.md package change p.2 forbids running them locally; R-f18's '30 s' threshold does not exist. Amendment: local witness = test_local_keys.py + test_role_rules.py + non-slow printed files; the four named 'sudit kanon pachki'; correct R-f18."
  ],
  "fixes": [
    "B-1 amendment (dialect-independent syntax and posix normalisation in declared_place, both branches).",
    "B-2 amendment (credential test before the predicate; no echo of a credential-like ref; row ../elsewhere/token=abc123.md).",
    "B-3 amendment (witness scope; R-f18 corrected).",
    "N-1: linked_documents lists nothing unless text_ref resolves to an existing regular file inside a declared root (keys, URLs, task-relative work/raw refs list nothing).",
    "N-2: a rooted candidate resolves against the innermost declared root holding text_ref.",
    "N-3: the s1.md edit keeps 'text you read there is recorded' (role-rules.json:446) verbatim; only --ref on line 60 changes.",
    "N-4: owns add docs/SIBLING_MAP.md (axis 8 row), a changelog.d fragment, and conditionally fixtures/driver-layers.json (row now :490) and fixtures/judgment-census.json.",
    "N-5: set the _record_source census row to class xref (owner data) in the same commit, or make section 1 say shape.",
    "N-6: declared_place skips a code_repos entry whose path is not a non-empty string or cannot be resolved; rows path 123 and empty path.",
    "N-7: the row where the 40th path is listed counts its remainder in its own 'and <k> more' line; dot entries do not count toward DOC_ENTRIES_SCANNED.",
    "N-8: with no project the folder test is skipped; 'empty-named dot-free files' reads 'empty dot-free files'.",
    "N-9: the failing-before row of F-1's second defect is the folder-ref refusal; the two-records row uses ../sib/docs/A.md and B.md.",
    "N-10: move A-3 item 5 (grep line string, s1.md:59-60) into A-2 so each commit's brief names only refs record-source accepts.",
    "Edge: document_place_lines derives the project with runtime_paths.nearest_project(task_root), as record-source does; note that a path containing /browse/ never settles (_key); add %00 to the A-3 adversarial rows; label the left-out-path row as a hand-built as_written entry (no exclusion kind names a path).",
    "R-1 (rule 19): A-2's listing reaches only the driver road (requirement_source_lines/document_place_lines are called only from role_lines); fix this round where both roads read, or open node A-6, owner Lead live-run-fvf.",
    "Queue a covers edit of test_local_keys.py in test-layers.json (add ticket_light.py, runtime_paths.py) or accept the witness gap explicitly."
  ],
  "class_completeness": "Surface 'the syntax reader of --ref' walked: encoding (backslash dialect B-1; percent-decoded links; NUL after decoding), nesting (lexical normpath vs OS resolution: provenance only), magnitude (200/201, 300-char ref), empty or broken (blank, malformed code_repos entry N-6). Surface 'refusal text' walked for secret echo (B-2). Axes: 8 applies (declared_place on contained/_repository_roots/nearest_project; its row edit needs owns); 5 applies (s1.md template and grep line change together; the A-2 listing has no skill-road twin, R-1); 31 applies (pointers, one mini-paraphrase); 34 applies (one predicate; the listing is driver-only, proposed node A-6 owner Lead live-run-fvf); 32 not named by the spec (census class of _record_source, N-5); 18 touched if driver-layers or the census move (name any raise). Readers of ticket-references.json enumerated: brief_pack.reference_gap_lines, driver_s0.s0_references_allow_no_change, source_inventory writers and settler; none blocks or asks on an unknown kind.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261114-fv1-23-a2-a3-redraft-spec.md",
      "docs/tasks/specs/reviews/20261114-fv1-23-20-plan-critic.md",
      "9c15423 ai-packages/qa-factory/scripts/ticket_adapter.py",
      "9c15423 ai-packages/qa-factory/scripts/source_inventory.py",
      "9c15423 ai-packages/qa-factory/scripts/runtime_paths.py",
      "9c15423 ai-packages/qa-factory/scripts/source_exclusions.py",
      "9c15423 ai-packages/qa-factory/scripts/driver_stage_plan.py",
      "9c15423 ai-packages/qa-factory/scripts/driver_sources.py",
      "9c15423 ai-packages/qa-factory/scripts/brief_pack.py",
      "9c15423 ai-packages/qa-factory/scripts/driver_s0.py",
      "9c15423 ai-packages/qa-factory/scripts/ticket_light.py",
      "9c15423 ai-packages/qa-factory/scripts/config_contract.py",
      "9c15423 ai-packages/qa-factory/scripts/friction.py",
      "9c15423 ai-packages/qa-factory/scripts/selftest.py",
      "9c15423 ai-packages/qa-factory/scripts/slow_tests.json",
      "9c15423 ai-packages/qa-factory/scripts/tests/test_local_keys.py",
      "9c15423 ai-packages/qa-factory/scripts/tests/harness.py",
      "9c15423 ai-packages/qa-factory/scripts/tests/scenario_walk.py",
      "9c15423 ai-packages/qa-factory/scripts/tests/test-layers.json",
      "9c15423 ai-packages/qa-factory/scripts/tests/fixtures/driver-layers.json",
      "9c15423 ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json",
      "9c15423 ai-packages/qa-factory/skills/qa-story/phases/s1.md",
      "9c15423 ai-packages/qa-factory/agents/qa-scout.md",
      "9c15423 ai-packages/qa-factory/references/reference-kinds.json",
      "9c15423 ai-packages/qa-factory/references/requirement-source-kinds.json",
      "9c15423 ai-packages/qa-factory/references/templates/config.json",
      "9c15423 ai-packages/qa-factory/references/artifact-writers.json",
      "9c15423 .github/workflows (runs-on)",
      "docs/TESTING.md",
      "docs/SIBLING_MAP.md (axes 8, 18, 32, 33, 34, headings)",
      "plans/builder-rules.md (7b)",
      "stand MyBooks/docs/AUTH.md:8; LOCAL-1 work/source-inventory.json; transcript 634b0a20 lines 5, 57, 63, 82"
    ],
    "reruns": [
      {
        "command": "python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for runtime_paths.py ticket_adapter.py source_inventory.py driver_stage_plan.py ticket_light.py s1.md (read-main worktree; test-layers differs from 9c15423 by +8/-2)",
        "result": "runtime_paths: 3 scenarios + ~19 keep incl. test_runtime_paths; ticket_adapter/source_inventory: test_local_keys among keep, plus test_story_run_* files; ticket_light: no test_local_keys; s1.md: no keep row, whole scenario layer (no test_role_rules); driver_stage_plan: test_driver_layers among keep"
      },
      {
        "command": "python heredoc: posixpath vs ntpath normpath/relpath for backslash refs",
        "result": "on POSIX '..\\\\MyRepo/docs\\\\a.md' and 'docs\\\\..\\\\..\\\\x.md' stay lexically inside the project (relpath keeps the backslashes); on Windows both resolve outside"
      },
      {
        "command": "git grep at 9c15423: readers of ticket-references.json; callers of record-source; _safe_rel callers; requirement_source_lines callers",
        "result": "readers: brief_pack, driver_s0, source_inventory, ticket_adapter only (controller 0; control source-inventory 5); no subprocess caller of record-source; _safe_rel judges snapshot/local/evidence refs only; requirement_source_lines called only from driver_stage_plan.role_lines"
      }
    ]
  }
}
```
