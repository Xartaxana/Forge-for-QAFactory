# Critic t-765 -- FV1-23 A-5 diff (builder t-759, commit b18b0c8 on wip/fv123-a5)

Verdict: **NEEDS WORK (fit_with_fixes)** -- 2 blocking findings (F1, F2), 2 fixes before merge (F3, F4), 4 queue lines.
Acceptance stays with the Lead (critic rule 6).

Scope read: `git diff origin/main...HEAD` (all 5 files), the A-5 node of the topic spec (`20261114-fv1-23-a2-a3-redraft-spec.md:371-383`
and the A-3 card :286-369), the A-2/A-3 topic critic (F5, Q1), the builder report, and the code named below in the worktree.

## Standing questions

1. **Fit to the spec** -- NOT MET on (b) "credentials in a link are masked wherever a row is written" (F1) and on (a) "every text the
   factory reads at S0" for the paste leg (F2). Met: record-source texts get keys/URLs/MRs through `TL.references` + `_merge_reference_rows`
   with origin `mention:document:<ref>`; S0 summary/description/comments and attachment texts get `linked_document` rows through
   `TL.path_candidates` + `_listable`, each declared root a base, one row per root; (c) not built by the Lead's word (no finding).
2. **Builder's own decisions** -- origin = the text's own key (safe, matches `build_references`, Q2 below); a `..` that leaves a root is no
   row even if it lands in another root (safe direction: a missed link is the allowed error); the write only when `TL.references` found
   a row (consistent with A-3). All in the safe direction.
3. **Seams** -- additive: one call appended in `_write_s0_files`, one in `append_attachment_references`, one try-block at the tail of
   `_record_source`; the masking loop inside `_merge_reference_rows` changes behaviour for every caller (A-3's rows, attachments) -- that
   is the point of F1(iv).
4. **Class-wide completeness** -- see the Class section: axis 5 (S0 twins REST/paste) and axis 34 open (F1, F2); axes 8, 18, 31, 32 n/a or held.
5. **Tests** -- `test_local_keys.py` is the right home: keep row `layer: table` (`test-layers.json:2892`), not in `slow_tests.json`
   (positive control: `test_story_run_s6.py` found at :142), not quarantined; the rows are behaviour rows in the existing table
   `linked_documents_rows`, the S0 and attachment rows go through the factory's own writers (`_write_s0_files`,
   `append_attachment_references`). Killing power: the rows would catch a removed call (builder's negative control proves it). They do
   NOT catch F1: no row stores a credential URL at S0 and then merges the same URL from an attachment. F8 (minor).
6. **DUPLICATION AND CONSISTENCY** -- F3 (fix before merge), F4 (fix before merge), F5 (queue). No new URL/link parser added: the diff
   has no `re.compile`; it calls `TL.path_candidates` and `TL.references`. Pre-existing separate URL regexes outside the diff:
   `source_exclusions.py:805`, `:890`, `source_inventory.py:214`, `device_stand.py:51` beside `ticket_light.py:941` (queue line Q-c).
7. **CODE QUALITY** -- `linked_documents_of_texts` (`source_inventory.py:2606-2648`, ~43 lines) has four nesting levels (for origin -> for
   name -> for root -> try/if) -- queue, folded into F5. No dead branches; names honest except the report's "origin = the attachment name"
   (the real origin is `mention:attachment:<name>`, `source_inventory.py:1562`; F8).
8. **Hygiene** -- added lines ASCII only (grep -P non-ASCII over `+` lines: none); the three .py files are LF at base and HEAD
   (CR-terminated lines 0/0 each), consistent; changelog fragment ASCII.
9. **In-tree ratchets** -- the diff touches no ratchet file (no census, `role-load.json`, baselines, `known_red`): none raised.
10. **ARCHITECTURE** -- named AR-13, AR-15, AR-21, AR-28. Touched and not named: AR-22 (a new producer of `linked_document` rows at S0).
    My reader walk: `brief_pack.reference_gap_lines` renders them (A-3 join), `_settle_references` settles them by ref
    (`source_inventory.py:2060`), `driver_s0.s0_references_allow_no_change` (`driver_s0.py:920-932`) reads only `is_change` kinds and
    `linked_document` is not a row of `reference-kinds.json` -> the no-change question is unaffected. No reader starved; F7 (minor).
11. **JUDGMENT** -- `judgment: none` holds: code lists names that exist inside a declared root and writes rows; relevance stays the
    scout's (P27/AR-29). No census row, no `blocks_override`, no craft marker, no scan-constant edit.
12. **ONE ROAD** -- residual found: the S0 paste leg (F2) takes the ticket's own text by a road with no link reader, and the REST leg
    and the paste leg disagree on whether acceptance criteria are scanned (Q3 below). `linked_documents` vs `linked_documents_of_texts`
    is NOT a second road: same tokenizer (`TL.path_candidates`), same predicate (`_listable`), same row form, same merge -- the base
    resolution differs by the task's own condition (a text with a place vs a text without one); the duplicated loop is F5.

## Findings

**F1 (BLOCKS) -- credentials reach disk; the masking is at one writer of three and breaks the identity merge.** Surface: "a credential
inside a stored reference ref". Masking lives only in `_merge_reference_rows` (`source_inventory.py:2018-2020`). Walked:
(i) the S0 writer `_write_s0_files` (`:1127`, `:1136-1139`) writes `build_references` rows raw -- `TL.references` keeps the URL as the
ref (`ticket_light.py:1154`); (ii) the paste leg `write_paste_references` (`ticket_adapter.py:1654-1663`) writes raw; (iii) userinfo:
`SECRET_QUERY_RE` (`config_contract.py:59`) sees only `name=value`, so `https://u:p4ss@host/q` is stored raw by every writer, though
`_record_source` already treats `urlsplit(ref).password` as a credential (`ticket_adapter.py:2205`); (iv) regression: an S0 raw URL and
the same URL from an attachment no longer merge -- the fresh row is masked, its identity differs, a twin is appended. Probe (scratchpad
`probe.py`, S0 rows written as `_write_s0_files` does, then `_merge_reference_rows` with an attachment naming the same two URLs):
```
after merge: url https://wiki.example/p?token=abc123 ['mention:description']
after merge: url https://u:p4ss@wiki.example/q ['mention:description', 'notes.txt']
after merge: url https://wiki.example/p?token=<hidden> ['notes.txt']
abc123 on disk: True | p4ss on disk: True
```
Neighbouring classes walked: fragment `#token=` (masked: the regex is position-free), case (`(?i)`), over-match `monkey=` -> masked
(safe direction), percent-encoded `token%3D` (not masked; low, rides on the same helper), origins carrying an attachment file name
(pre-existing, not a link: note only). Answer to builder question 4: YES, an unmasked credential is written to disk after this diff.
Fix: one masking helper (query `name=value` AND the userinfo password) applied to every row before it is stored and before identity is
computed -- in the S0 writer, the paste leg and the merge (cleanest: where `TL.references` builds the ref, if the Lead widens owns to
`ticket_light.py`) -- plus one row: an S0 URL with `token=` then the same URL from an attachment -> one row, masked, no raw value in the file.

**F2 (BLOCKS, or a node with id and owner before acceptance) -- the pasted ticket text has no link road.** `write_paste_references`
(`ticket_adapter.py:1623-1663`) is S0's other writer of the same file from the same kind of text (the person's ticket description,
`paste_texts` :1607-1620) and gets no `linked_document` rows; the dispatch's (a) names "every text the factory reads at S0". The builder
queued it as outside owns; brief question 12(d) does not allow a bare queue line. Fix (recommended in this round, F1 touches the same
function): append `SI.text_link_rows(work.parent, <the paste texts>)` to its rows, with one row in the existing table.

**F3 (fix before merge) -- the S0 text set is copied.** `_write_s0_files` `source_inventory.py:1132-1134` repeats `build_references`
`:1111-1113` line for line. Fix: one `_ticket_texts(snapshot)` used by both, so the key road and the link road read the same texts (and
Q3 becomes a one-place change).

**F4 (fix before merge, non-blocking) -- a second known-prefix builder.** `append_document_references` (`:2681-2683`) hand-builds the
known prefixes; `_known_prefixes` (`:1667-1694`) already does it and works with `client=None` (probe2: returns `{'PROJ','ABC'}` for a
text with a `/browse/ABC-5` link); the hand set misses the `/browse/KEY`-in-text rule. My probe showed no row difference for that text,
so not blocking. Fix: call `_known_prefixes(None, output, own, {}, (text,))` and add `project_keys`.

**F5 (queue) -- builder question 1.** `linked_documents_of_texts` (`:2606-2648`) and `_recorded_read_refs` (`:2597-2603`) repeat the
candidate loop and the recorded-set block of `linked_documents` (`:2567-2585`). Not a one-road breach (see 12) and not fixable here
(`linked_documents` was a dispatch non-goal). Recommendation: a later node puts both on one core `_kept_links(...)` whose caller
supplies the base resolution, `linked_documents` reads `_recorded_read_refs`, and the nesting drops to three.

**F6 (queue / question to the Lead) -- no bound per ticket.** `LINK_CANDIDATES_LIMIT` is per text; S0 now scans every comment against
every root: 200 comments x 500 names x 3 roots = 300k `_listable` calls at S0 (estimate, not measured). The dispatch fixed "limits
unchanged", so the builder complied; a per-ticket bound (with its cut said) is the Lead's fork.

**F7 (minor)** -- the `architecture:` line should name AR-22 (walk above) at the fix round.

**F8 (minor)** -- the attachment rows in the test pass `notes.txt` as the origin; the factory passes `mention:attachment:notes.txt`
(`source_inventory.py:1562`). Use the real form so the row tests the door the factory uses.

## Builder's questions -- recommendations

1. One core: yes, but as a later node (F5), not in this diff -- the duplication is real, the road is one.
2. Origin = the text's own key: yes -- the same origins `build_references` already writes, so the S0 merge joins them; attachments get
   `mention:attachment:<name>` from their caller.
3. AC: yes -- the paste leg already scans criteria (`ticket_adapter.py:1616-1617`), the REST leg does not (`build_references`
   `:1111-1117`), while `_known_prefixes` does read AC (`:1686`): a P31 divergence that predates the diff. Add AC to the shared
   `_ticket_texts` (F3) for keys and links together, as a node (it changes S0's key rows).
4. Masking: yes, and it is blocking (F1).

## Class (SIBLING_MAP, origin/main copy)

- axis 5 (stage twins): S0 REST writer <-> S0 paste writer -- link road (F2) and masking (F1) open; AC scan divergence (Q3).
- axis 8 (where the story is on disk): `work.parent` and `Path(output).resolve().parent.parent` both reach the task root; project via
  `runtime_paths.nearest_project`, containment via `contained`/`_listable` -- held.
- axis 18: nothing raised.  axis 31: no role text -- n/a.  axis 32: judgment none holds.
- axis 34: F2 and Q3; pre-existing URL regex twins (Q-c).

## Queue lines (for the Lead to write into the batch «Остатки»)

- Q-a: one link core for `linked_documents` and `linked_documents_of_texts`, nesting to three (F5) | узел: FV1-23 A-7 (proposed; owner: Lead of live-run-fvf)
- Q-b: acceptance criteria scanned by the REST S0 leg for keys and links through the shared `_ticket_texts` (Q3); a per-ticket bound on link candidates (F6) | узел: FV1-23 A-8 (proposed; owner: Lead of live-run-fvf)
- Q-c: four URL regexes outside `ticket_light._URL_RE` (`source_exclusions.py:805`, `:890`, `source_inventory.py:214`, `device_stand.py:51`) -- one URL tokenizer (AR-15) | перенос: findings/<new file in pile live-run-fvf> | обоснование: pre-existing, outside the A-5 owns | подтвердил: —
- F2, if the Lead does not take it this round: | узел: FV1-23 A-9 (proposed; owner: Lead of live-run-fvf)

## Edges (the dispatch's list, against the code)

| edge | verdict |
|---|---|
| empty text | holds: `path_candidates("")` empty, row `A-5 (b): empty...` |
| a text with no link | holds |
| the same link in two texts | one row, origins joined (within a scan by the `rows` dict; across S0 -> S1 by merge identity); BROKEN for a credential URL (F1 iv) |
| a link with credentials | FAILS (F1) |
| an unreadable attachment | holds: never enters `attachment_named` (`source_inventory.py:1552-1564`, receipt marked unavailable) -> no rows; no new test row, existing path |
| limits of the existing reader unchanged | holds (500 per text, cut said on stderr with its count); no per-ticket bound (F6) |

## Trail

- Read: diff (5 files); `source_inventory.py` 1100-1149, 1548-1565, 1667-1711, 1990-2084, 2378-2404, 2537-2690;
  `ticket_adapter.py` 1600-1663, 2203-2305 (diff hunk), `ticket_light.py` 179-183, 941-942, 1120-1179; `driver_s0.py` 919-940;
  `config_contract.py:59`; `reference-kinds.json` note; `test-layers.json` 2888-2895; `slow_tests.json` (grep); spec 286-395; A-2/A-3
  critic (grep); builder report; SIBLING_MAP axes list, 5, 34 (read-main).
- Re-run: `( cd <worktree>/ai-packages/qa-factory && python -B scripts/tests/test_local_keys.py )` -> `=== test_local_keys: 327/327 ok ===`
  (skips printed: places F6, links symlink, A-5 symlink -- the OS refused links), matches the witness.
- Probes (scratchpad, read-only on the repo): `probe.py` output quoted in F1; `probe2.py` -> both prefix sets give
  `[('ticket', 'https://other.example/browse/ABC-5', 'person'), ('ticket', 'ABC-7', 'not_fetched:not read yet')]`; `_known_prefixes(None,...)` -> `{'PROJ', 'ABC'}`.
- Greps: URL regexes `https\?:` + compile/findall/finditer over `scripts/*.py` (positive control `ticket_light.py:941` hit);
  `path_candidates(` callers (2, both in the diff's file); writers of `ticket-references.json` (S0 writer, paste leg, merge, settle).
- A first CR count with `grep -c $'\r'` was a miscall (counted every line); redone with `grep -c -P '\r$'`: 0 at base and HEAD.

```json
{"verdict": "fit_with_fixes", "blockers": ["F1: credentials reach disk: masking only in _merge_reference_rows (source_inventory.py:2018-2020); S0 writer (_write_s0_files :1127/:1136) and paste leg (ticket_adapter.py:1654-1663) store token= URLs raw, userinfo passwords are masked nowhere, and an S0 raw URL plus the same URL from an attachment now gives a twin row (probe: abc123 and p4ss on disk)", "F2: the S0 paste leg write_paste_references (ticket_adapter.py:1623-1663) reads the ticket's own text with no link road (P31, dispatch item a); fix this round or a node with id and owner before acceptance"], "fixes": ["F1: one masking helper (query name=value and userinfo password) applied to every row before storage and before identity at the S0 writer, the paste leg and the merge, plus a row: S0 token URL then the same URL from an attachment gives one masked row", "F2: append SI.text_link_rows(work.parent, paste texts) to write_paste_references rows, with one table row", "F3: one _ticket_texts(snapshot) helper for build_references (source_inventory.py:1111-1113) and _write_s0_files (:1132-1134)", "F4: append_document_references (:2681-2683) uses _known_prefixes(None, output, own, {}, (text,)) plus project_keys instead of a hand-built set", "F7: name AR-22 in the architecture line", "F8: test attachment origin uses mention:attachment:notes.txt as the factory does"], "class_completeness": "Axis 5 S0 twins REST/paste: link road and masking open (F1, F2), AC divergence queued (Q-b); axis 34: F2 plus pre-existing URL regex twins queued (Q-c); axis 8 held; axes 18, 31 n/a; axis 32 judgment none holds; duplicate link loop queued as a node (Q-a, F5).", "trail": {"read": ["git diff origin/main...HEAD (5 files) in .claude/worktrees/fv123-a5", "source_inventory.py 1100-1149, 1548-1565, 1667-1711, 1990-2084, 2378-2404, 2537-2690", "ticket_adapter.py 1600-1663, _record_source tail", "ticket_light.py 179-183, 941-942, 1120-1179", "driver_s0.py 919-940", "config_contract.py:59", "references/reference-kinds.json note", "scripts/tests/test-layers.json 2888-2895", "scripts/slow_tests.json grep", "docs/tasks/specs/20261114-fv1-23-a2-a3-redraft-spec.md 286-395", "docs/tasks/specs/reviews/20261114-fv1-23-a2-a3-diff-critic.md grep", "docs/tasks/specs/reports/20261114-fv1-23-a5-report.md", "docs/tasks/critic-diff-brief.md", ".claude/worktrees/read-main/docs/SIBLING_MAP.md axes 5, 34"], "reruns": [{"command": "( cd .claude/worktrees/fv123-a5/ai-packages/qa-factory && python -B scripts/tests/test_local_keys.py )", "result": "=== test_local_keys: 327/327 ok === (three symlink rows skipped by the OS)"}, {"command": "python -B scratchpad/probe.py (S0 rows then _merge_reference_rows with the same URLs from an attachment)", "result": "twin row token=abc123 raw plus token=<hidden>; abc123 on disk True; p4ss on disk True"}, {"command": "python -B scratchpad/probe2.py (TL.references with and without the /browse/ prefix; _known_prefixes(None,...))", "result": "same rows for both prefix sets; _known_prefixes returns PROJ and ABC"}]}}
```
