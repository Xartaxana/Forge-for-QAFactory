# t-740 — code critic, FV1-23 A-2 (2a4075b) + A-3 (e3defa2), branch wip/fv123-a23 vs origin/main

**Verdict: fit_with_fixes (NEEDS WORK)**. One finding blocks the merge (F1: a test row that will be red on the Linux canon). Seven fixes belong to this round. Queue lines are at the end. This verdict is an input to acceptance. The decision to accept is the Lead's.

The spec and DoD are `docs/tasks/specs/20261114-fv1-23-a2-a3-redraft-spec.md` (cards A-2 and A-3, §8a, and §8b, which binds). The plan verdict is t-726.

## Findings

**F1 (BLOCKS MERGE): `test_local_keys.py:859` fails on the Linux canon.** The row checks `"ln.md" in rec(root, work, "ln.md.txt", "see docs/ln.md NOTES.md").err` and expects `False`. `NOTES.md` is listed at that point: it is never recorded, and the exclusion for it is written only after this row. So stderr carries the heading `Linked from ln.md.txt, ...`, and `ln.md` is a substring of `ln.md.txt`. On Windows the row is skipped because `os.symlink` is refused. My re-run printed `skipped: links to a symlink pointing outside`. The canon runs on `ubuntu-latest` with python 3.12 (`.github/workflows/canon.yml:44,75`), where the symlink gets made and the row runs. Probe with the same text and ref, no symlink needed: `ln.md.txt record -> 0 | 'ln.md' in err: True | err: Linked from ln.md.txt, ... / - NOTES.md (6 B)`. The product itself is right: `declared_place` realpaths the link and refuses it. Only the assertion is wrong. Fix: assert that `"docs/ln.md" not in listed(err)`, and that `NOTES.md` is in it (the positive half).

**F2 (fix): `normal_ref` is not `relpath(place, project)` as card A-2 item 1 prescribes** (`runtime_paths.py:548-553`). The function returns the posix-normalised ref, so a ref that climbs out through the project's own name and back in is kept as spelled. Probe on project `proj`: `../proj/docs/x.md -> 0` and `docs/x.md -> 0`, both stored: `['../proj/docs/x.md', ..., 'docs/x.md']`. That is two records of one document, which breaks the card's invariant "one record per document". A `linked_document` row spelled the other way never settles. The report's claim "equal to `relpath(place, project)` lexically" (§1) is false for this input. It is also missing from the eight decisions. Fix: `normal = os.path.relpath(place, str(project)).replace(os.sep, "/")` after the containment test. Every k7 row keeps its expected value: `../repo/...`, `docs/a.md` and `.` stay the same.

**F3 (fix): the `not_relative` refusal text is now false** (`ticket_adapter.py:2216-2217`). Key 4 and builder question 7 below.

**F4 (fix): duplication.**
- (a) The per-file "listable" chain is written twice, and the two copies already differ. The chain is `declared_place`, then `text_file_problem`, then `SECRET_QUERY_RE`, then `first_ref_match`. Copy one is in `_document_walk` (`source_inventory.py:~2400-2413`), copy two in `linked_documents` (`:~2555-2561`). The length test exists only in the walk. Lift it into one helper, `_listable(project, cfg, ref, live) -> (normal, reason)`, and call it from both. AR-13/AR-15, the spec's "ONE predicate".
- (b) `contained(place, root) and contained(root, place)` (`:2464`) is a second "same place" test. `runtime_paths._same_place` (`runtime_paths.py:603`) already exists for this, and `contract.py:55` reuses it.

**F5 (fix, owns widened by the Lead): B-2 is only partly met on the surface "record-source texts that echo caller values".** I walked every echo site in `_record_source`:
- held: the new `outside` door, the folder door (both its example and `normal`), the exclusion refusal, the link heading, and the "could not be listed" line;
- not held, both lines older than this diff:
  - `{args.file}: nothing to record` and `is not text` (`:2251`, `:2260`). Probe: `--file .../token=abc123.md` (empty) printed `ticket_adapter: C:\...\token=abc123.md: nothing to record`;
  - `_ready_line` (`:2191-2194`) runs before the credential test. Probe with no `--relation`: `ready: ... --ref ../elsewhere/token=abc123.md`.

The text of §8b item 2 reads "No refusal text echoes a ref or a `--file` name". The fix is about three lines: mask each echoed value with `SECRET_QUERY_RE.sub`. These lines sit outside the A-2 owns (the ref check block only), so the Lead either widens owns for this round or opens a node.

**F6 (fix): builder decision 4 leaves a cut unsaid** (`source_inventory.py:2393-2394`). A symlinked folder is neither walked nor counted, which breaks AR-21 ("every cut said with its place"). Count such folders in a line of their own, or in the "not walked" line. A related point, not a defect: on Windows with python 3.12, `os.path.islink` is False for a junction, so a junction IS walked. That stays safe, because each file goes through the realpath predicate.

**F7 (Lead's question, recommendation given): builder decision 3.** Rows are written only for the ≤25 listed paths. The builder's reason ("a row per remainder path would need the unbounded list") is factually wrong: `unread` already holds every kept path and is bounded by LINK_CANDIDATES_LIMIT = 500 (`:2563-2567`). Without rows, the remainder never reaches the persisted carrier that the A-L detector (i) reads. Recommendation: build the `rows` comprehension from `unread` instead of `paths`. The stderr listing stays capped at 25, and the brief renderer already caps at 20 with `+K more`.

**F8 (Lead, before the merge to main): commit message, key 12.** Spec §7 is titled "Four questions (rule 10), per mechanism" and says "(b) axes: the builder enumerates every axis in the commit". It names three mechanisms: the `declared_place` refusals, `document_place_lines` and `linked_documents`. CLAUDE.md rule 10 counts a new refusal of a command as a mechanism. So `axes: not a mechanism (...)` on 2a4075b is the wrong waiver, and A-3 carries no axis block at all. A mechanism block is owed. `tools/mechanism_gate.py` refuses a `tier:` below the lead binding, so the block must come from the Lead at integration: the four questions from §7, one line per axis of the map, and `tier:`. No code changes.

## Keys

1. **§8b items 1-15.**
   - B-1 held:
     - `PureWindowsPath`/`PurePosixPath` drive, root and absolute checks, plus `/`, `\`, scheme, `file:` and NUL, all before the `\`→`/` replacement and `posixpath.normpath`; the same steps run in the project-None branch;
     - the k7 rows read row by row for Linux, all plausible: `C:\x\y.md` → drive; `docs\..\..\x.md` → `../x.md` → outside; with a NUL in the `code_repos` path, Linux `realpath` raises ValueError, which `declared_roots` catches;
     - the record_source rows are plausible too (`cli` runs in-process, so a NUL in argv is safe).
   - B-2: held for every new text, not for two older ones (F5).
   - B-3: the witness scope is right.
   - N-1, N-2 (innermost root by realpath length), N-3 (anchor kept verbatim, `s1.md:59`), N-5, N-6, N-7, N-8, N-10 and item 14: held.
   - N-4: owns kept. N-9: rows present.
   - Item 15: report §5.
2. **Direction of error.** Nothing outside every declared root was accepted, listed or stored in any of these:
   - symlink: `contained` realpaths both sides; a file link is checked by the predicate; folder links are not walked;
   - `..` after normalisation: the containment test runs on the normalised path;
   - percent-decoding: it happens before `declared_place` in `path_candidates`; record-source keeps `%2e%2e` literal, and the probe stored it as a literal folder name inside the project, not as an escape;
   - NUL: refused in both functions;
   - rooted candidate: joined, then put through the predicate.

   `code_repos` spelled `..` does declare the parent folder. Probe: `../other/secret.md -> 0`. That follows the declaration, so it is not a hole in the predicate, but a root that is an ancestor of the project, or a drive root, declares everything. Queue Q2.
3. **The eight decisions.**
   1. No project gives []: right (the safe direction; the grep line still stands).
   2. Counts after "no text file": right (AR-21).
   3. Rows only for listed paths: question to the Lead, F7.
   4. A symlinked folder is silent: fix, F6.
   5. A NUL is `not_relative`: right.
   6. A second `rstrip` after decoding: right.
   7. The refusal text: false, F3.
   8. The 2000 cap patched to 20: allowed by the card. But the row `test_local_keys.py:674`, `DOC_ENTRIES_SCANNED == 2000`, pins a constant, which is TESTING «не пишется»: drop it (minor, in this round).
4. **The text is false.** The `not_relative` branch fires only for a drive, a root, a scheme, a NUL or a blank ref, and a `..` path into a declared root is now accepted. Saying "no `..`" sends the scout off a legal road (FR-1, FR-2). Corrected sentence, which keeps the needle (no test pins the old parenthesis: a Grep for `no drive and no` finds only `ticket_adapter.py:2216`): `give the locator relative to the project (no drive, no leading / or \, no file: or other scheme), or a URL; a document of a declared repository is named from the project, for example <code_repos path>/<path inside it>, which may start with ..`
5. **Held.** The listing sits in `try/except Exception` after the record and the stdout output, and `return 0` always follows (`ticket_adapter.py:2272-2290`). The friction classifier was run over the listing text and the failure line: `None`, `None`. Positive control: `the gate is refused` → `validator`.
6. **P27/AR-29.**
   - No line judges relevance.
   - `_record_source` → `xref` is right by CLASS_ORDER over `shape`.
   - No new census unit: `UNIT_NAME_RE` (`_problems$`) does not match `text_file_problem`, and no new function has a refusal site.
   - No ratchet raised. AR-20 holds: the census `ratchet` has no `xref` key.
   - A question for the Lead, not this node: the credential refusal in the same unit reads as `safety`, which ranks above `xref` (Q4).
7. **Readers.** None blocks, asks or counts on the new kind.
   - `brief_pack.reference_gap_lines` renders it generically, as advice.
   - `driver_s0.s0_references_allow_no_change` counts only `change_kinds`, i.e. `is_change` rows of `reference-kinds.json`: `merge_request` and `pull_request`.
   - `_settle_references` settles the kind (the test JOIN row passes).
   - A case-insensitive Grep for `ticket-references|REFERENCES_FILE` over the package (tests excluded) found only these readers and the S0 writers (positive control: it found `brief_pack.py:1363`).
8. **Tests.**
   - Tables carry ids that name the case.
   - Every adversarial row of §8b is present: `../elsewhere/token=abc123.md`, `123` and `""` (both files), `%00`, `docs\..\..\x.md`, `C:\x\y.md` (`:476`, k7).
   - The k7 rows are plausible on Linux.
   - test_local_keys has one row that fails on Linux: F1.
9. **Duplication: F4.**
   - `text_file_problem` duplicates on purpose the whole-file criteria of record-source on a slice: allowed by the card, with the allowed error stated.
   - `_merge_reference_rows` is a faithful lift of the attachments' merge; the refactor-guard row passes.
   - `declared_place`'s syntax half repeats `_safe_rel` (`source_inventory.py:2971`, builder analog (a)): queue Q3.

   **Code quality** (severity: queue):
   - `_record_source` 112 lines (`ticket_adapter.py:2184-2296`);
   - `document_place_lines` 86 lines (`source_inventory.py:2421-2506`);
   - nesting 4 in `_document_walk.walk` (`:2381-2416`).

   F4a removes part of this. Extracting the ref block of `_record_source` is a later step.
10. **Held.** Only the `role_lines` qa-scout return changed: the diff shows one hunk in `driver_stage_plan.py`.
11. **Axes.**
    - 5 (skill↔driver): the s1.md template and the grep line changed together. Covered.
    - 8: the row was extended in the same commit and reads correctly. Covered.
    - 18: no raise. Covered.
    - 31: the new headings point at the charter ("charter: the walk of references"). Covered.
    - 32: one class change, correct. Covered.
    - 34: the folder listing reaches only the driver road. A-6 is named in spec §8b, but it has no row in any pile carrier: a case-insensitive Grep for `A-6` over `plans/piles` found only unrelated hits (`potolka-6`). Positive control: `FV1-23` is found in `batch-1-live-run-fvf.md:52`. Q1.
12. **F8.**

## Queue lines (for the Lead; form `<what> | узел: <id>` once a node is opened)

- Q1: FV1-23 A-6 (the folder listing on the skill road, axes 5 and 34) and A-5 need rows in an untaken `live-run-fvf` batch. `| узел: FV1-23 A-6` and `| узел: FV1-23 A-5`. Owner: Lead of live-run-fvf.
- Q2: `config_contract` should refuse, or flag, a `code_repos` root that holds the project (`..`, a drive root). Owner: Lead of live-run-fvf.
- Q3: `_safe_rel` should call `declared_place`'s syntax half (axis 8: one syntax test). Owner: the same.
- Q4: should the `_record_source` census class be `safety`? A named raise of the `safety` ceiling 86 would follow. Owner: the census owner.
- Q5: on Windows, a case alias of a `code_repos` root (`../SIB/docs/A.md` next to `../sib/...`) is a second spelling of the same file. Probe: both stored. Canonical spelling would take the root prefix from `declared_roots`. Owner: Lead of live-run-fvf.
- Q6: `linked_documents` derives the inventory and the exclusions from `task_root/work`, while record-source uses `--output`'s parent (builder analog d). They should be one derivation.

## Trail

Read:
- the spec: whole;
- the t-726 verdict (Grep: B-1, B-2);
- the builder report: whole;
- critic-diff-brief: whole;
- SIBLING_MAP: axes 5, 8, 34 and the headings;
- the full diff of both commits: all 12 files;
- worktree code:
  - `runtime_paths.py` 190-293, 470-519;
  - `ticket_adapter.py` 2180-2299, `_ready_line`;
  - `source_exclusions.py` 320-439;
  - `source_inventory.py` 1955-1984 and `_key`, `_safe_rel`;
  - `brief_pack.reference_gap_lines`, `driver_s0.s0_references_allow_no_change`;
  - `friction.py` 1-130 and `friction-markers.json`;
  - `reference-kinds.json`;
  - the census test header and `UNIT_NAME_RE`;
  - the `ratchet` keys of `judgment-census.json`;
  - the `role_lines` row of `driver-layers.json`;
  - `canon.yml` (runs-on, python);
  - `mechanism_gate.py` (Grep).

Re-runs (verbatim tails):
- `( cd <wt>/ai-packages/qa-factory && python -B scripts/tests/test_local_keys.py )` → `skipped: links to a symlink pointing outside - the OS refused to make a file link` / `=== test_local_keys: 294/294 ok ===`.
- Temp-project probe (heredoc, temp directory only):
  - `self-alias ../proj/docs/x.md -> 0`; `plain docs/x.md -> 0`; `case alias ../SIB/docs/A.md -> 0`;
  - `stored refs: ['../SIB/docs/A.md', '../proj/docs/x.md', '../sib/docs/A.md', 'docs/%2e%2e/%2e%2e/x.md', 'docs/x.md']`;
  - `--file credential-like, empty -> (2, '', 'ticket_adapter: C:\\...\\token=abc123.md: nothing to record ...')`;
  - `--ref credential-like, no --relation -> (2, '', 'usage: ... ready: ... --ref ../elsewhere/token=abc123.md ...')`;
  - `ln.md.txt record -> 0 | 'ln.md' in err: True`;
  - `code_repos '..' then ../other/secret.md -> 0`.
- `friction.classify`: listing → None, failure → None, control → validator.

```json
{"verdict": "fit_with_fixes", "blockers": ["F1: ai-packages/qa-factory/scripts/tests/test_local_keys.py:859 asserts 'ln.md' not in stderr, but the heading 'Linked from ln.md.txt' contains it whenever NOTES.md is listed, so the symlink row (skipped on Windows) fails on the ubuntu canon"], "fixes": ["F1 test_local_keys.py:859: assert docs/ln.md not in listed(err) and NOTES.md in it", "F2 runtime_paths.py:548-553: normal_ref = relpath(place, project) posix as the card says (self-alias ../proj/docs/x.md stored as a second record)", "F3 ticket_adapter.py:2216-2217: reword the not_relative door (no drive, no leading slash or backslash, no scheme; code_repos example may start with ..)", "F4 source_inventory.py:~2400-2413 and ~2555-2561: one _listable helper for the walk and the link filter (length test diverges); :2464 reuse runtime_paths._same_place", "F5 ticket_adapter.py:2191-2194, 2251, 2260: mask SECRET_QUERY_RE in the --file echo and the ready line (B-2 text), owns widened by the Lead or a node", "F6 source_inventory.py:2393-2394: count symlinked folders instead of skipping them silently (AR-21)", "F7 source_inventory.py:2567: Lead decision, recommended rows for every kept unread path (bounded by 500), not only the 25 listed", "F8 Lead at integration: mechanism axis block per spec section 7 plus tier line instead of axes: not a mechanism on 2a4075b", "minor: drop the constant pin test_local_keys.py:674"], "class_completeness": "Axes 5, 8, 18, 31, 32 covered; axis 34 residual A-6 (and A-5) named in spec 8b but absent from any pile carrier (queue Q1); B-2 surface walk found two older echo sites (F5); predicate surface neighbours: self-alias (F2), Windows case alias (Q5), code_repos ancestor root (Q2), _safe_rel syntax twin (Q3).", "trail": {"read": ["docs/tasks/specs/20261114-fv1-23-a2-a3-redraft-spec.md", "docs/tasks/specs/reviews/20261114-fv1-23-a2-a3-redraft-plan-critic.md (Grep B-1/B-2)", ".claude/worktrees/fv123-a23/docs/tasks/specs/reports/20261114-fv123-a23-report.md", "docs/tasks/critic-diff-brief.md", "docs/SIBLING_MAP.md axes 5, 8, 34", "git diff origin/main...HEAD all 12 files", "runtime_paths.py 190-293, 470-519", "ticket_adapter.py 2180-2299, _ready_line", "source_exclusions.py 320-439", "source_inventory.py 1955-1984, _key, _safe_rel", "brief_pack.reference_gap_lines", "driver_s0.s0_references_allow_no_change", "friction.py 1-130, friction-markers.json", "reference-kinds.json", "test_judgment_census.py header, judgment-census.json ratchet", ".github/workflows/canon.yml"], "reruns": [{"command": "python -B scripts/tests/test_local_keys.py (worktree package dir)", "result": "skipped: links to a symlink pointing outside; 294/294 ok"}, {"command": "temp-project record-source probe (heredoc)", "result": "self-alias and case alias stored as extra records; --file and ready-line echo abc123; 'ln.md' in err True; code_repos '..' accepts ../other/secret.md"}, {"command": "friction.classify on listing/failure/control texts", "result": "None, None, validator"}]}}
```
