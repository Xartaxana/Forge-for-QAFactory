# t-2187 — One bug, many manifestations (DRAFT spec, designer)

Status: DRAFT for Lead acceptance; critic-on-plan done (t-2187 review `docs/tasks/specs/reviews/20261110-t-2187-plan-critic.md`,
ACCEPT WITH FIXES); fix round 1 applied (t-2194), per-finding map in §16. Forks are in section 12.
Tree read: `D:/ws2/wt-fbfix` (branch fb-fix = experiment/thinking-roles). `PKG` = `D:/ws2/wt-fbfix/ai-packages/qa-factory`.
Every `file:line` below is from that tree, read on 10.11.2026.

## 1. Goal, AR-n touched, census

**Goal (owner, 10.11.2026).** Bugs with one cause are filed as ONE bug with several manifestations. The analyst looks for the
shared mechanism of all APP_BUG rows and observations before drafting, says how far it got (confirmed by a code line or a
discriminating run / unverified hypothesis / unknown), and understands that a manifestation depends on the start state (field
empty or not, selected or erased, previous value, stock, way of typing). Chosen direction "1+2 with hints" (not reopened):
analyst charter + draft schema (`mechanism`, `manifestations[]`); discriminating probes with per-statement marking (FR-41);
a code-built neighbourhood table as evidence (code never merges, never judges). Merge rule: merge only on a CONFIRMED cause;
an unverified hypothesis keeps separate drafts linked "possibly one cause". Safety: each manifestation keeps its own evidence and
red test; gate B shows one bug with its manifestations and a door "these are different bugs".

**AR-n touched and how each is kept** (the change check of each goes into the DoD of the node named):

| AR | how kept | change check (DoD) |
|---|---|---|
| AR-29 | every new code check is shape / xref / presence of a witness; whether a run DISCRIMINATES, whether two rows share a cause, whether to merge: the analyst's judgment, accepted by the scribe (tier above, `qa-doc-scribe.md:26` already accepts or returns the triage) and by the person at gate B | census row per new unit, class in {shape, xref}, owner `data`; no `meaning*`/`word-list` row added. Each node (N1, N2, N3a, N4, N6) lists its rows in its report; the INTEGRATOR writes them into the census (§11, census rule) |
| AR-13 | ONE reader per new fact: `bug_records.draft_cases`, `draft_requirements` (extended), `manifestation_refs`, `mechanism_problems`, `merged_unconfirmed`; every consumer calls them | grep test: no `draft.get("cases")` / `data.get("case") or data.get("cases")` / `d.get("case")) or ...d.get("cases")` left in ANY `scripts/*.py` outside `bug_records.py` and `scripts/tests/` (N3a; widened from "the readers listed in §5", critic M3) |
| AR-14 | drafts have one writer (the analyst, S7, `artifact-contract-run.md:97`); the neighbourhood table is printed, never a file | `bug_neighbours.py` writes nothing (test asserts no file created, N6) |
| AR-21 / AR-27 | every manifestation travels draft -> gate B packet -> `work/bug-text/<stem>.md` -> `bugs/BUG-n.md` -> report, under its bug | key-presence tests at each hop (N2 bug text, N3a, N3b, N4) |
| AR-22 | `mechanism` and `manifestations[]` each have a producer (analyst) and named readers (§5, incl. 5.17 bug text and 5.18 dashboard); `possibly_same_cause` has a reader (gate B, report) | producer+reader in one commit per node; reader test per field |
| AR-23 | empty outcomes declared: one manifestation; mechanism `unknown` with `why`; no code access; old drafts; the code-reading form | §3.2 table, tests per empty outcome (N1) |
| AR-24 / AR-25 | the person's "these are different bugs" reaches the analyst whole (`--words-file`), a merged draft has a way out (split, written with `distinct_defect` carrying the person's word, so it never re-enters `same_location`), a split draft a way back (merge on the person's word, F-6); the `same_location` refusal names the manifestations door (5.16) | s8.md text + gate B block test (N3b, N8); `same_location_problems` text test (N2) |
| AR-26 | each manifestation names the requirement it breaks (R-n), the bug's `requirements` is the union | `draft_requirements` test (N1) |
| AR-28 | an unverified mechanism never becomes "one bug": a merged draft whose basis does not stand is refused at the S7 claim and the gate B rehearsal (F-2 (a)) | adversarial tests §6 (N2) |
| AR-20 | new refusal sites raise `blocking_per_role` counts in the census ratchet (`judgment-census.json:4`, ONE line): the analyst's (S7 claim) and the conductor's (gate B rehearsal) by N2, the reporter's (bug form) by N4; the integrator writes the summed values. The process ratchet (`role-load.json:24-37`, slack 0) is paid by named cuts or raised only by the owner's word (F-10..F-12) | census counts per node in its report; `role_load.py --all` output in the report of N1, N4, N5 (§11) |
| AR-2 / AR-1 | start states and mechanisms are open variety (role); the closed words (`mechanism.status`, basis kinds) are data in `contract.py` beside `BUG_REPRODUCTION_KINDS` (`contract.py:1828`) | constants test (N1) |
| AR-8 / AR-10 | the analyst is handed the neighbourhood command and the draft key page before the work (FR-15, FR-38); the obligation of F-5 bites only after the charters ask for the field (§3.2 temporal edge) | brief card test (N6); key page lists the new keys (N1); cutoff constant set by N8 (§11) |
| AR-16 | gate B and report text for a merged bug follow `references/human-questions.md` (rule 6 prices) | `human_text.price_problems` on the new block (N3b) |

**Census class and owner of every check the spec adds or alters:**

| check (file::function) | what it checks | class | owner it serves |
|---|---|---|---|
| `bug_records.py::mechanism_problems` (new) | `mechanism` shape; status word in the closed list; each `basis` entry of kind `code_line` stands by `bug_records._fact_problem` (`:547`, its `{path, line, quote}` form, resolver `user_path_failures.resolve_code_path`; no second code-line verifier); each `run` entry names a capture in the recorder index, unchanged, holding the quote (`place_answers.capture_stands`); `confirmed` has >= 1 standing entry; a claim marked confirmed cites a standing entry | xref | data (code); the meaning (does it discriminate) is judgment, accepted by the scribe |
| `bug_records.py::manifestation_problems` (new) | `manifestations[]` shape; each entry's `triage_row` names an APP_BUG row, or its `probe` names a standing capture; each carries `red_test` or `red_test_none` (via `contract.red_test_problems`, `contract.py:1851`) | xref | data |
| `bug_records.py::pair_drafts` (altered, `bug_records.py:354`; stays PURE, signature unchanged) | an APP_BUG row is covered by a draft whose `triage_ref` OR a `manifestations[].triage_row` names it; new keys `manifestation_no_row`, `manifestation_not_app_bug` | xref | data |
| `bug_records.py::merged_unconfirmed` (new, critic M8; Lead, 10.11.2026: a separate reader, not a widened `pair_drafts`) | `(task, drafts) -> [(name, first problem)]`: each draft with 2+ manifestations whose `mechanism_problems(task, draft)` is non-empty or whose status is not `confirmed` | xref | data |
| `bug_records.py::_blocker_cover` (altered, `:457`, critic m3) | reads the blocker draft's cases through `draft_cases` (union) instead of `draft.get("cases")` | xref | data |
| `bug_records.py::same_location_problems` (altered text only, `:1683-1687`, critic M4) | the refusal names the manifestations door (5.16) | xref | data |
| `handoff_check.py::_claim_bug_has_a_draft` (altered, `handoff_check.py:599`) | prints the new `pair_drafts` keys and `BR.merged_unconfirmed(art.root, drafts)` as problems with doors | xref | data |
| `gate_preflight.py::check_bug_drafts` (altered, `gate_preflight.py:5050`) | case label and unreviewed check over the union of cases; manifestation / mechanism findings and `merged_unconfirmed` as `factory_fixable` with waiver; a triage draft dated on/after `BUG_MECHANISM_CUTOFF` without `mechanism` as a `factory_fixable` finding (F-5 (a), presence) | xref / shape | data |
| `validate_artifacts.py::check_bug_form` (altered, `validate_artifacts.py:429`; new optional `draft=None`) | only when the caller passes the resolved source draft: `cases` holds every case of `BR.draft_cases(draft)`; a draft with >= 2 manifestations requires a `## Manifestations` section naming each manifestation's case and red test (presence) | shape | data |
| `artifact_producer.py::validate` (altered, `artifact_producer.py:117-126`, critic M2) | with `task_root`: resolves `BR._draft_of(task_root, source_draft)` and passes it to `check_bug_form`; without: a not-checked line, as for triage (`:93-98`) | xref | data |
| `bug_neighbours.py::neighbours` (new) | groups targets/rows/drafts by equal keys; never refuses | shape (advice, non-blocking) | data -> advice for the analyst's judgment |
| `place_answers.py::settled_answer` (altered, `place_answers.py:485`) | a `bug` answer whose draft was absorbed into a merged draft is settled through the merged draft (`from_draft`) | xref | data |

Error direction of every check above: DOWN (toward separate drafts / "unconfirmed" / a refusal with a door / "not checked"), never
toward a pass.

## 2. What exists today (carriers read)

- Draft schema: `PKG/references/artifact-contract-run.md:95-125`. One `triage_ref`; optional `cases`, `siblings`, `defect_location`,
  `distinct_defect`, `requirements`. Required list `contract.py:1833` (`title, impact, violates, case, triage_ref, manual_steps`).
  Second form `evidence: "code-reading"` (`contract.py:1881-1882`, key page `slices/qa-failure-analyst/artifact-contract-run.md:110`):
  no `triage_ref`/`case`, skips `pair_drafts` (`bug_records.py:381-384`), one draft per requirement (`R_CR_TWICE`, `:477`).
- `siblings` has NO reader in code (grep `siblings` over `PKG/scripts/*.py`: hits only in unrelated functions
  `artifact_supersede.py:106`, `brief_pack.py:3216`/`:3225`, `contract.py:4506`; positive control: the same grep found those).
- Reporter charter `PKG/agents/qa-bug-reporter.md:44`: "Defects that share a mechanism stay separate reports, each naming its siblings." (to be reversed); `:33` and `:36` already name the class. `:36`-`:44` sit under `<!-- kind: craft -->` (`:28`, `:39`).
- Analyst charter `PKG/agents/qa-failure-analyst.md`: no word about a shared mechanism or start states; `:68` the walk commands; `:70` `open-bugs` and "one draft per `defect_location`, or mark `distinct_defect`" (process, Tools `:60`).
- Who can drive the stand in S7 (§7): the analyst already walks through the recorder (t-1991): `PKG/agents/qa-failure-analyst.md:54,68`, `PKG/skills/qa-story/phases/s7.md:94-105`, driver `PKG/scripts/story_run.py:14398-14485` (place lines, settle walk session, actor `guest` at `:14443`).
- Recorder start-state steps: `fill` clears then keys per character, `type` appends, `press Control+A` / `Backspace` (`PKG/references/explore-charter.md:74-81`).
- Process ratchet: `role-load.json:24-37`; `role_load.py --all` (critic rerun) shows process == ratchet exactly for qa-runner 14,388,
  qa-failure-analyst 15,996, qa-bug-reporter 13,901, qa-doc-scribe 16,891 (zero headroom). Static load counts the brief at its
  ceiling (`role_load.py:519`), so brief card lines cost nothing there; injected slices count (`inject-map.json:86-111`): the
  `bug-drafts/*.json` section lands in the analyst's slice (`slices/qa-failure-analyst/artifact-contract-run.md:84`), the
  `bugs/BUG-n.md` section in the scribe's (`slices/qa-doc-scribe/artifact-contract-run.md:79`), neither in the runner's or the
  reporter's (grep `^#+ .*(bug-drafts|BUG-n)` over `references/slices`; the same grep found those two headings).

## 3. Data shape

### 3.1 Draft (triage road) — new keys

```json
{"title": "The quantity field on the book page turns invalid input into a different number",
 "impact": "degraded", "violates": "requirement:R-8", "case": "LOCAL-1_TC_005",
 "triage_ref": {"instance_id": "LOCAL-1_TC_005#obs1", "attempt_id": "a1"},
 "cases": ["LOCAL-1_TC_005", "LOCAL-1_TC_007"], "requirements": ["R-8", "R-9", "R-10"],
 "manual_steps": ["open the book 1984", "select all in Quantity and type -1 one key at a time"],
 "red_test": {"path": "...", "command": "..."},
 "confirmation": "unconfirmed",
 "mechanism": {
   "statement": "the field replaces any value it cannot read as a whole number >= 1 with 1 on every key, and the next key is appended to that 1",
   "status": "confirmed",
   "basis": [
     {"id": "b1", "kind": "code_line", "path": "src/pages/BookDetailPage.tsx", "line": 164, "quote": "setQuantity(Math.max(1, parseInt(e.target.value) || 1))"},
     {"id": "b2", "kind": "run", "case": "settle-new-qty-start", "capture": "work/evidence/manual/settle-new-qty-start/a1/012-fill.txt",
      "quote": "1 11 focus=yes", "start_state": "field erased first"},
     {"id": "b3", "kind": "run", "case": "settle-new-qty-start", "capture": "work/evidence/manual/settle-new-qty-start/a1/015-type.txt",
      "quote": "1 1 focus=yes", "start_state": "typed over a selection"}],
   "claims": [
     {"says": "an invalid intermediate value becomes 1 and the next key is appended", "confirmed_by": ["b1", "b2"]},
     {"says": "1.5 gives 1 over a selection and 11 after erasing", "confirmed_by": ["b2", "b3"]},
     {"says": "pasting -1 behaves like typing it", "confirmed_by": []}],
   "why": ""},
 "manifestations": [
   {"action": "type -1 one key at a time", "start_state": "field shows 1, selected", "seen": "11",
    "requirement": "R-9", "case": "LOCAL-1_TC_005",
    "triage_row": {"instance_id": "LOCAL-1_TC_005#obs1", "attempt_id": "a1"},
    "evidence": "work/evidence/manual/LOCAL-1_TC_005/a1/006-fill.txt",
    "red_test": {"path": "...", "command": "..."}},
   {"action": "type 1.5", "start_state": "field erased first", "seen": "11", "requirement": "R-10", "case": "LOCAL-1_TC_007",
    "probe": {"case": "settle-new-qty-start", "capture": "work/evidence/manual/settle-new-qty-start/a1/012-fill.txt", "quote": "1 11 focus=yes"},
    "evidence": "work/evidence/manual/settle-new-qty-start/a1/012-fill.txt",
    "red_test_none": "manual check only: the case is not in the regression (P28)",
    "from_draft": "qty-invalid-input-coerced.json"}],
 "possibly_same_cause": []}
```

Keys:
- `mechanism` object: `statement` str; `status` one of `confirmed | unverified | unknown` (closed list `contract.MECHANISM_STATUSES`,
  data, AR-1); `basis` [] of entries with `id` and `kind` one of `code_line | run` (`contract.MECHANISM_BASIS_KINDS`):
  `code_line {path, line, quote}`, `run {case, capture, quote, start_state}`; `claims` [] of `{says, confirmed_by: [basis ids]}` —
  an empty `confirmed_by` means the claim is NOT verified and every reader prints it as "not verified" (FR-41); `why` str (required
  when `status` is `unknown` or `unverified`: what is missing — "no access to the application code", "only one start state was run").
  A "not verified" claim is always about THIS mechanism's own behaviour; a behaviour of another code place is another draft (F-9 (a)).
- `manifestations` [] of `{action, start_state, seen, requirement?, case?, triage_row? | probe?, evidence, red_test | red_test_none,
  from_draft?}`: `triage_row` is a triage key (same shapes `draft_triage_key` reads, `bug_records.py:319`); `probe` is a capture the
  analyst made itself (a manifestation no triage row stands for); exactly one of the two, EXCEPT a manifestation absorbed from a
  code-reading draft (§3.2, last row); `from_draft` names the file of a draft this manifestation absorbed (§5.10).
- `possibly_same_cause` [] of `{draft: <file name>, why: <one sentence>}` — separate drafts of THIS run the analyst suspects share a
  cause it could not confirm. Replaces the unread `siblings`: the key page marks `siblings` as legacy (read by nothing; write
  `possibly_same_cause`). It is not named `possible_duplicate`, because that key names an issue in the tracker
  (`gate_brief.py:75` `DUPLICATE_KEYS`), not a draft of this run (critic m5; N1 writes both sentences on the key page).
- Draft-level `triage_ref`, `red_test`, `reproduction` stay; they are the PRIMARY manifestation's (the one the draft was first
  written for). The primary is also `manifestations[0]` when `manifestations` is present (N1 checks equality of the triage key; a
  mismatch is a `manifestation_problems` line "the first manifestation is not the draft's own row").

### 3.2 Empty / absent outcomes (AR-23) and their invariants

| case | behaviour | invariant protected |
|---|---|---|
| a bug with one manifestation | `manifestations` absent or one entry; every reader shows it as today (no "1 manifestation" line) | an ordinary bug's packet/report/bug-text changes no byte (test: golden render of a single-manifestation draft equals today's) |
| mechanism unknown | `mechanism: {status: "unknown", why: "..."}`, `basis: []`; a draft with ONE manifestation is valid | "unknown" is never printed as a cause; the packet line says "cause not established: <why>" |
| no code access | `basis` has no `code_line`; `confirmed` only through `run` entries; else `unverified` with `why: no access to the application code` | code is never the oracle (FR-58): a code line is evidence of the CAUSE, never of the EXPECTATION, which still comes from `violates` |
| mechanism unverified, 2+ rows suspected | separate drafts, each `possibly_same_cause` naming the others with `why` | an unconfirmed cause never removes a bug from the person's list |
| `mechanism.status: confirmed` with 2+ manifestations, basis does not stand (quote not in file, capture not in index / changed) | refused as `merged_unconfirmed` (F-2 (a)); the door: fix the basis, or split into separate drafts with `possibly_same_cause` | a merge whose evidence cannot be re-read never stands (error goes DOWN) |
| old draft (no `mechanism`, no `manifestations`) | read exactly as today: one manifestation = the draft itself; mechanism "not stated"; no refusal | a draft or bug filed before the change is never re-litigated |
| EVERY triage draft (any number of manifestations) created on/after `BUG_MECHANISM_CUTOFF` without `mechanism` (Lead, 10.11.2026, M5: F-5 (a) for every new draft) | a gate B rehearsal finding `factory_fixable` (`gate_preflight.check_bug_drafts`, door: the person's word via `waiver.py`), the same form as the other draft findings of the key page (`artifact-contract-run.md` "Checked" paragraph); NOT a refusal at the S7 claim (F-5 (a) names a finding with the person's door). The empty outcome is `{status: "unknown", why}` | the cause analysis is never skipped silently; a draft is never refused for a field no charter asked for (FR-38, FR-5: see temporal edge) |
| a code-reading draft (`evidence: "code-reading"`, `contract.py:1881-1882`) (critic M6) | F-5's obligation is NOT asked of it (it has no run and no triage row; its own checker is `code_reading_problems`). A triage draft may ABSORB it as a manifestation with `from_draft: <its file>`, no `triage_row` and no `probe` (the one exception to "exactly one of the two"), `evidence` = the absorbed draft's `fact` as `path:line`; the absorbed file is removed by the analyst. `R_CR_TWICE` then counts one draft fewer for that requirement, never more | a code-reading candidate is never lost by a merge (it stays a manifestation with its fact) and never counted twice (one requirement, one draft still holds) |

**Temporal edge (before / after the fields exist and are asked for)** (Lead, 10.11.2026, M5). Three worlds:
1. Before N1 merges: no reader knows the keys; a draft carrying them is read by its old keys (extra keys are ignored today —
   `pair_drafts` reads only `triage_ref`, `defect_location`, `distinct_defect`, `cases`; `bug_records.py:383-427`).
2. After N1, before the charters ask for the field: the keys are read by the new readers; `contract.BUG_MECHANISM_CUTOFF` holds the
   placeholder `None`, and `check_bug_drafts` asks the obligation only when the constant is a date — so NOTHING is refused or found
   for a missing `mechanism`. N1 never sets a date.
3. After the LAST of the charter/key-page nodes lands: N8 (ordered after N1 and N5, §11) sets `BUG_MECHANISM_CUTOFF` to the day of its
   own merge, in the same commit as its phase text. From then on every triage draft whose `created` (else file day, the same rule as
   `contract.red_test_owed`, `contract.py:1842-1848`) is on/after that day is asked for `mechanism` (row above).
The move that creates the fields is N1 (contract + reader functions); the analyst is told about them by N5 (charter) and N1 (key
page); the move that makes them owed is N8's one-line constant.

## 4. The merge rule in data terms

- One draft = one mechanism. A draft MAY carry 2+ manifestations only when `mechanism.status` is `confirmed` and its basis stands
  (`mechanism_problems` empty). This is a PRESENCE-of-witness check (AR-29 allows it, `architecture.md:134-140`); whether the
  witness truly discriminates is the scribe's acceptance and the person's door.
- Adversarial inputs that must stay on the safe side (refused, door named): status `confirmed` with `basis: []`; a `code_line` whose
  quote is not on that line or the file is outside the repo root / missing / line beyond the end (all through `_fact_problem`); a
  `run` whose capture is not in the recorder index of the case it names, or changed after hashing, or the quote is not in it, or it is
  a picture; `basis` not a list; an entry with an unknown `kind`; a claim citing an id not in `basis`; status `Confirmed` (case) — a
  typo is not the word.
- Adversarial inputs that must NOT be refused (judgment stays with the role): a run whose capture is also a manifestation's evidence
  (the two-point discrimination of the owner's example is exactly that); a single `code_line` basis with no run; a `confirmed`
  status with some claims unverified (the packet prints those claims as "not verified").

## 5. Every join that assumes one draft = one row / one bug = one draft / one bug per case

Producer and readers change together (AR-22). Test per item; test file in brackets.

| # | file:function (line) | assumption today | new behaviour | test |
|---|---|---|---|---|
| 5.1 | `bug_records.py::pair_drafts` (`:354-430`), `_blocker_cover` (`:457`), new `merged_unconfirmed` | `keys` = the drafts' `triage_ref` only (`:392`); an APP_BUG row named only in a merged draft's manifestation lands in `app_bug_without_draft` (`:417-420`); `_blocker_cover` reads `draft.get("cases")` | `pair_drafts` keeps its signature `pair_drafts(drafts, rows, filed=())` and stays PURE (reads no file); `keys` also holds every `manifestations[].triage_row` (via `manifestation_refs`); new outputs `manifestation_no_row` `[(name, label)]`, `manifestation_not_app_bug` `[(name, label, verdicts)]`; a manifestation naming a row with `blocking_check` is NOT coverage (the blocker rule `:404-416` stands). `_blocker_cover` reads `draft_cases(draft)`. New `merged_unconfirmed(task, drafts) -> [(name, first problem)]` in `bug_records.py` (Lead, 10.11.2026, M8), called by the callers that already hold the task root: `handoff_check._claim_bug_has_a_draft` (`art.root`) and `gate_preflight.check_bug_drafts` | three APP_BUG rows, one draft listing all three as manifestations -> `app_bug_without_draft == []`; a manifestation naming a NO_DEFECT row -> `manifestation_not_app_bug`; naming no row -> `manifestation_no_row`; a blocked row whose case sits only in `manifestations[].case` of the blocker's draft -> no `blocker_draft_misses_case`; `merged_unconfirmed` over a merged draft with a broken basis -> one entry, over a draft with one manifestation -> `[]`; `pair_drafts` is pure: called with `Path.read_text`/`open` patched to raise, it returns the same dict as unpatched [`test_bug_records.py`] |
| 5.2 | `handoff_check.py::_claim_bug_has_a_draft` (`:599-645`) | prints only the old keys | one problem line per new key and per `BR.merged_unconfirmed(art.root, drafts)` entry, each with its door ("add the row the manifestation names, or remove the manifestation", "fix the basis (a shared `defect_location` line can be cited as a `code_line`), or split the draft and link the parts with `possibly_same_cause`") | the claim over the 5.1 fixtures returns those lines [`test_handoff.py`] |
| 5.3 | `gate_preflight.py::check_bug_drafts` (`:5084-5177`) | `case = draft.case or draft.cases` (`:1086` in the method, file line 5086) — `cases` ignored when `case` is set; unreviewed check over that string only (`:5118`); verdict check on the primary row only (`:5096`) | label = primary case; the unreviewed/unstated check runs over `BR.draft_cases(draft)` (union of `case`, `cases`, `manifestations[].case`); `manifestation_problems`, `mechanism_problems` and `BR.merged_unconfirmed(task, drafts)` lines become `factory_fixable` findings with `self.waiver_command(block)`; when `C.BUG_MECHANISM_CUTOFF` is a date, a triage draft dated on/after it without `mechanism` is one more such finding (F-5 (a), §3.2); a code-reading draft is never asked | a merged draft whose second case is in the roll-call's unreviewed list -> finding; a broken manifestation -> finding; cutoff `None` + draft without `mechanism` -> no finding; cutoff a date + new draft without `mechanism` -> finding; same with a draft dated before it -> none; code-reading draft without `mechanism` -> none [`test_gate_preflight.py`] |
| 5.4 | `bug_records.py::reproduction_problems` / `_current_red_problem` (`:843-974`) | one instance (`draft_triage_key`) | UNCHANGED: the draft-level `reproduction` and the red-now fact stay the primary manifestation's; manifestations carry their own `evidence`, not receipts. State it in the docstring | a merged draft whose primary is red and a second manifestation's test is green now: `confirmation_of` unchanged (`reproduced_by_factory` only through the primary's receipts) [`test_bug_reproduction.py`] |
| 5.5 | `traceability.py::story_bug_records` (`:192-252`) | `data.get("case") or data.get("cases")` (`:236`, `:244`) — a draft with both reads only `case`; requirements from `DRAFT_REQUIREMENT_FIELDS` (`:83`: `requirement, requirements, violates, triage_ref`) | cases = `BR.draft_cases(data)`; requirements = union of today's reading and `BR.draft_requirements(data)` (extended to `manifestations[].requirement`); record gains `manifestations` (count + one-line each, from `BR.manifestation_summary`) and `mechanism` (status, statement, unverified claims) for the report | merged draft with `case: A`, `cases: [A, B]`, manifestation of C -> record `cases == [A, B, C]`; `bug_for(B, ...)` returns the merged bug [`test_bug_link_s9.py`, `test_bug_reproduction.py` — the two files `grep -l story_bug_records scripts/tests/*.py` gives, critic m6] |
| 5.6 | `traceability.py::Story.bug_for` (`:531-542`) | one bug per case | UNCHANGED: with merging there are FEWER bugs per case; a case covered by two mechanisms still returns the first (filed first, then by requirement) as today. Edge stated, no change | covered by 5.5's test |
| 5.7 | `gate_brief.py::packet_items` (`:4026-4030`) and `undrafted_discrepancies` (`:4074-4079`) | read `id`, `case`, `cases` (`case_id`) of a draft; a case present only in a manifestation is "no draft speaks for it" -> the packet contradicts itself (FR-10) | both read `BR.draft_cases(draft)` | a `contradicts_requirement` manifest row for case C covered by a merged draft's manifestation -> not in `undrafted_discrepancies`; C in `packet_items("B")` [`test_gate_brief_and_retro.py`] |
| 5.8 | `gate_brief.py::bug_rows` / `render_gate_b` (`:4093-4161`, `:4320-4361`) | one line of evidence per draft (`_bug_evidence`, `:4193-4211`) | a row gains `manifestations` (list of one-liners) and `mechanism` (status, statement, unverified claims) and `possibly_same_cause` (numbers of the linked rows); render per §8; new `merged_bug_block(rows)` after `code_reading_block` (`:4354`) | §8 golden text; single-manifestation golden unchanged [`test_gate_brief_and_retro.py`, `test_human_reading.py`] |
| 5.9 | `report_facts.py::_bugs` / `_r_bugs` (`:579-632`, `:2709-2745`) | one line per record | record carries `manifestations`/`mechanism` from 5.5; `_r_bugs` prints under a merged bug's line one indented line per manifestation and one cause line (§8.3) | report golden for a merged bug; counts (`confirmed`/`unconfirmed`) count BUGS, not manifestations [`test_report_facts.py`] |
| 5.10 | `place_answers.py::settled_answer` (`:485-528`) and `places` (`:249-268`) | a `bug` answer names a draft file; an absorbed draft is gone -> "carrier missing" -> the place becomes a gap at the close | a `bug` answer whose `draft` names a file that is the `from_draft` of a manifestation of a live draft is settled when that live draft's step holds (`confirmation_of` -> `reproduced_by_factory` with `walk`) OR the manifestation's `evidence` is the answer's own `seen.capture`; otherwise as today | absorbed draft with a walk answer, merged draft carrying `from_draft` -> `settled`; `from_draft` naming a draft no answer names -> no change [`test_place_answers.py`] |
| 5.11 | `delivery_summary.py` (`:286-338`) | one `source_draft` per proposal | UNCHANGED: one draft per bug still holds (one mechanism = one draft = one bug). Verified: `source_draft` is compared whole (`:297-312`) | none needed; N4 adds one assertion that a merged draft's proposal pairs as before [`test_story_run_delivery*` not run locally — CI] |
| 5.12 | `bug_records.py::story_bugs` (`:1360-1555`) | pairs a filed bug with the draft its `source_draft` names | UNCHANGED join; `_draft_of` (`:998`) is the one reader N3a and N4 use for the source draft of a filed bug | covered by 5.5 |
| 5.13 | `validate_artifacts.py::check_bug_form` (`:429`) + its caller `artifact_producer.py::validate` (`:117-126`); `check_bug_filing_header` (`:411-426`) UNCHANGED | neither function has a task root, so neither can open the source draft (`_draft_of(task, ref)` needs `task`); `artifact_producer.py:126` calls `check_bug_form(Path('BUG-draft.md'), ...)` | (critic M2) `check_bug_form(path, fm, text, errors, draft=None)`: when `draft` is a dict (the RESOLVED source draft), `cases` must hold every case of `BR.draft_cases(draft)` (presence) and, with 2+ manifestations, a `## Manifestations` section must name each manifestation's case and its red test or `red_test_none` reason (presence, not wording); `draft=None` -> no new check. `artifact_producer.validate(kind, data, task_root, not_checked)`: in the `bug` branch, with `task_root` it resolves `BR._draft_of(Path(task_root), source_draft)` and passes it (an unresolvable draft -> `{}` -> one FORM line "the source draft cannot be read, so its manifestations cannot be checked", never a pass); without `task_root` and with `not_checked` it appends "the manifestations of the source draft were not checked (no task root)", the pattern of `:93-98`. `validate_artifacts.check_bug` (write-time, `:394`, path only) passes no draft: it cannot see the task, and says nothing new (the producer's check is the gate) | bug data whose source draft has 2 manifestations, no `## Manifestations` -> FORM error via `artifact_producer.validate(..., task_root=T)`; with it -> clean; missing a manifestation's case in `cases` -> FORM error; no task root + `not_checked=[]` -> one not-checked line, no error; `check_bug_form` without `draft` on today's fixtures -> unchanged errors; old bug (source draft without manifestations) -> no new error [`test_bug_filing.py`, `test_validate_artifacts_report.py`] |
| 5.14 | `ledger.py`, `check_delivery.py` | — | UNCHANGED: neither reads drafts or bug files. `grep -i bug` over `ledger.py` hits one comment (`:219`); `grep draft|bug_records|story_bug|BR\.` over `check_delivery.py` hits one comment (`:120`); positive control: the same greps hit those lines. Delivery reads triage verdicts per row (`check_delivery.py:104`), which the merge leaves untouched (every manifestation keeps its own APP_BUG row) | none |
| 5.15 | `judge_results.py` (`:294-308`) | reads `case`, `title`, `expected`, `actual` of a draft for duplicate advice | UNCHANGED (advice only; reads the primary) | none |
| 5.16 | `bug_records.py::same_location_problems` / `draft_location` (`:1651-1687`) | refuses 2+ drafts naming one `defect_location` unless merged or `distinct_defect`; the door says "every case in `cases`", which leaves the absorbed rows in `app_bug_without_draft` (`pair_drafts` keys on `triage_ref` only) | (Lead, 10.11.2026, M4) grouping unchanged; the refusal text becomes: "the drafts <names> name one defect place <place>; merge them into one draft whose `manifestations` hold every row, or write `distinct_defect: <why>` on each draft that is another defect". A `split` at gate B by the person's word (§8.2) writes on each resulting draft `distinct_defect: the person said these are different bugs at gate B: "<their words>"`, so the split never re-enters this refusal. Invariant: no APP_BUG row is left without a draft by either door — the merge door covers every row through `manifestations[].triage_row` (5.1), the `distinct_defect` door keeps one draft per row | the refusal text names `manifestations`; two drafts at one place, merged with both rows as manifestations -> no `same_location`, no `app_bug_without_draft`; two drafts at one place with `distinct_defect` carrying the person's words -> no `same_location` [`test_bug_records.py`] |
| 5.17 | `bug_records.py::bug_text` (`:255-275`) / `write_draft_texts` (`:277-312`) (critic M1) | renders `work/bug-text/<stem>.md` from `manual_steps`, `expected`, `actual`/`observed` only; §8.1 prints that path and caps manifestations with "(+k more, in the bug text)" | with 2+ manifestations `bug_text` adds `## Cause` (statement, how confirmed in words, "Not verified:" claims) and `## Manifestations` (one line each: action, start state, seen, expected with the requirement, red test command or "no test: <reason>"), ALL manifestations (no cap); with one manifestation or none the text is byte-equal to today | golden: single-manifestation draft -> today's bytes; merged draft with 7 manifestations -> both sections, 7 lines [`test_bug_records.py`] |
| 5.18 | `factory_dashboard.py::story_bug_rows` (`:1309`; drafts from `:1602` `BR.draft_paths`) (critic M3) | `cases = C.case_ids(d.get("case")) or C.case_ids(d.get("cases"))` — a merged draft hides `cases` and `manifestations[].case` | `cases = BR.draft_cases(d)` | a merged draft with `case: A`, `cases: [A, B]`, manifestation of C -> the row lists A, B, C [`test_factory_dashboard_joins.py`] |

## 6. Gate on old functions in a new role — error direction and adversarial inputs

- `place_answers._capture_list` (`:280-317`) is lifted into a public `capture_stands(task, case, capture, quote) -> [problems]`
  (one reader, AR-13; `_capture_list` calls it with `settle-<place>`). New role: it decides whether a `mechanism.basis` run and a
  `manifestations[].probe` stand, which decides whether a MERGE stands. May err only toward "does not stand". Adversarial inputs
  (each a test, N1): capture of another case named under this case; capture edited after hashing; quote absent; quote whitespace;
  path with `..` or absolute; a picture (no quote possible); case id that cannot name a capture root; an index file that is not JSONL.
- `bug_records.pair_drafts` in a new role (coverage through manifestations). May err only toward `app_bug_without_draft` (a draft is
  owed). It stays pure: everything that reads files (`merged_unconfirmed`) is a separate function (M8). Adversarial: manifestations
  not a list; an entry not an object; `triage_row` a bare instance (covers every attempt, the same rule as `triage_ref`,
  `bug_records.py:361-363`); a row with `blocking_check` (not coverage); one row listed twice in one draft (one coverage, no error);
  one row in two drafts' manifestations (F-3).
- The code-line check IS `bug_records._fact_problem(task, entry, None, "")` (`:547-582`), called with the basis entry's
  `{path, line, quote}` (no `id`, so the code-place branch runs: resolver `user_path_failures.resolve_code_path`, whole-line compare
  after whitespace normalisation). No second code-line verifier (critic m4). Error direction: refusal; a verification that could not
  run is "could not be verified", never a pass (`:576-577`).

## 7. Who executes a discriminating probe — established

**Fact: the analyst can drive the stand through the recorder today.** Carriers:
- `PKG/agents/qa-failure-analyst.md:54` ("Find out the truth on the page ... do what a person would do, a step or a short run at a
  time") and `:68` (`walk_session.py step|look|final`, or `manual_capture.py ui|http --case settle-<place>`).
- `PKG/skills/qa-story/phases/s7.md:94-105`: walks a place with `manual_capture.py ui|http --case settle-<place id>`; a place may be
  the analyst's own `new-<slug>` (`PKG/scripts/place_answers.py:8`, `:419`).
- Driver: every S7 triage dispatch gets a settle walk session (`PKG/scripts/story_run.py:14398-14485`, `s7_session_line`;
  changelog `PKG/changelog.d/t-1991-u3b.md:1`); the session can be reopened by the analyst.
- The recorder has the start-state steps the owner's example needs (`explore-charter.md:74-81`: `fill` clears and keys per character
  with value/focus per key, `type` appends, `press Control+A`, `Backspace`).

So no new route is needed: a discriminating probe is a walk under a place (`new-<slug>` or the draft's own place), and its capture is
cited in `mechanism.basis` (`kind: run`) and/or `manifestations[].probe`. Residual limits (stated, not forked unless noted):
1. The investigation dispatch is read-only (`s7.md:272-274`; `story_run.py:14445-14458` gives it no session): no probes there.
2. The settle walk session opens as actor `guest` (`story_run.py:14443` `S7_SETTLE_ACTOR`), and its `open` stays the driver's
   (changelog `t-2003-role-commands.md`). A probe needing a signed-in state (an account's cart) goes through
   `manual_capture.py ui --as <account>`: `references/role-commands.json:40-45` gives `manual_capture.py ui` to `qa-failure-analyst`
   with `[--as <account>] [--session <actor>]` and the rule "An S7 analyst captures only with `--case settle-<place id>`"; no hook
   restricts a `settle-*` case (grep `settle` over `PKG/hooks`: none; the same grep finds the term in `PKG/scripts`). Established
   (critic m1).
3. Cost: every probe is analyst time on Sonnet/Terra inside the S7 dispatch; measured by N9 (ii) against the previous LOCAL-1 run.
   See F-7.

The route "analyst orders a probe from the runner through the controller" is therefore not needed; it is listed in F-1 only as the
alternative should the Lead want probes out of the analyst's context.

## 8. Gate B packet and report text for a merged bug (human-questions.md form)

### 8.1 Bug row (in `render_gate_b`, after the head line `:4327-4342`)

```
2. **The quantity field on the book page turns invalid input into a different number** — impact `degraded` → P2 · one cause, 3 ways it shows · not reproduced outside this run.
   Cause, confirmed by trying it from two starting states: the field replaces a value it cannot read as a whole number with 1 after every key, and the next key is added to that 1.
   Not verified: whether pasting -1 behaves like typing it.
   a) Typing -1 one key at a time over a selected 1 — the field shows 11 (expected: rejected, the requirement on quantity 0 and below).
   b) Typing 1.5 after erasing the field — 11; over a selection — 1 (expected: rejected).
   c) Erasing the field — it shows 1 at once (expected: empty until typed; your answer at gate A).
   work/bug-text/qty-invalid-input-coerced.md
3. **Typing 12 in the cart quantity keeps only one digit when the field started at 2** — impact `degraded` → P2 · not reproduced outside this run.
   Cause not established: only one starting state was run.
   Possibly the same cause as 2 (not verified: both fields turn input into a different number).
   work/bug-text/cart-qty-loses-digit.md
```

Row 3 is the cart field (`CartPage.tsx:183`, a different code line, a separate draft under F-9 (a)); its "Possibly the same cause"
line appears only when the analyst wrote `possibly_same_cause` (critic M9).

Rules: "one cause, N ways it shows" only when N >= 2; the cause line says how it was confirmed in words (`code_line` -> "by the
line of the application code that does it"; `run` -> "by trying it from <n> starting states"; both -> both); a `status: unknown`
one-manifestation bug prints nothing new except "Cause not established: <why>" when F-5 made `mechanism` present; claims with empty
`confirmed_by` print under "Not verified:"; letters a), b) ... cap at `MAX_MANIFESTATIONS_SHOWN` (new constant, 6) with "(+k more, in
the bug text)" — the bug text holds them all (5.17). A row with `possibly_same_cause` adds:
`   Possibly the same cause as 4 (not verified: <why>).` — numbers, never file names.

### 8.2 The door block (`merged_bug_block(rows)`, after `code_reading_block`), only when a shown row has 2+ manifestations

```
## One bug or several
The factory found that 2 has one cause behind 3 different-looking problems and drafted it as one bug, so a fix is checked against all of them. It cannot know whether you want them tracked apart. For each such bug:
(a) `file` 2 — file it as one bug listing every way it shows.
the factory: one working session of the bug writer.
you: nothing more.
the story: each way it shows keeps its own test or check; after the fix every one is re-checked, and one still failing becomes its own bug; delivery unchanged.
(b) `split` 2 — these are different bugs; draft them apart.
the factory: one more working session of the failure analyst, then the report is rebuilt and this gate is shown again.
you: this answer, and one more look at this gate.
the story: nothing stays unverified by this choice; delivery waits until the gate is shown again.
(c) `not a bug` 2 — do not file it.
the factory: a record only.
you: nothing more.
the story: the problems stay in the report as found and not filed; delivery unchanged.
```

When a shown row has `possibly_same_cause`, one more option in the same block (F-6): `(d) `merge` 2 4 — they are one bug; draft them
together` with prices like (b).

Executors (FR-9): `file` -> the ref in `--drafts` (existing, `s8.md:318-322`); `not a bug` -> left out (existing); `split` and
`merge` -> words that ask a change are not recorded (`s8.md:267-268`); the conductor runs
`controller.py --task-root <T> --operation rework --stage S7 --role qa-failure-analyst --cases <the cases of the draft> --cause
question_answer --words-file <the answer file>` (the existing S7 rework road, `s7.md:249-252`), then gate B is asked again. Code does
not parse the answer (FR-12): the conductor reads it, as for `code_reading_block` (`gate_brief.py:4164-4190`). On the driver road the
same holds: `story_run.py:18383-18386` `record_by_code` returns False for any gate words that are not an approval, so `split` and
`merge` reach the conductor exactly as `prove by a run` does (established, critic m2). s8.md gains one line beside `:28` / `:324`
naming this (N8).

The analyst on a `split` rework: writes one draft per manifestation group the person named (or one per manifestation when the words
name none), each with `possibly_same_cause` back to the others and `why: the person said these are different bugs`, and — when the
drafts share a `defect_location` — `distinct_defect` carrying the person's words (5.16, Lead, 10.11.2026); the merged draft
file is removed (it was never filed: a filed draft is never rewritten, `bug_records.py:375-378`). On `merge` (F-6): one draft, basis
entry `kind: person` (F-6) or the analyst's own run.

### 8.3 Report (`_r_bugs`)

```
2. **minor · R-8, R-9, R-10 · LOCAL-1_TC_005, LOCAL-1_TC_007** — The quantity field on the book page turns invalid input into a different number (qty-invalid-input-coerced) (not reproduced outside this run) — chosen at gate B, not filed yet
   One cause (confirmed by trying it from two starting states): the field replaces a value it cannot read as a whole number with 1 after every key.
   Shows as: typing -1 over a selection gives 11; typing 1.5 after erasing gives 11, over a selection 1; erasing gives 1.
   Not verified: whether pasting -1 behaves like typing it.
3. **minor · R-11 · LOCAL-1_TC_009** — Typing 12 in the cart quantity keeps only one digit when the field started at 2 (cart-qty-loses-digit) (not reproduced outside this run) — chosen at gate B, not filed yet
   Possibly the same cause as 2 (not verified).
```

### 8.4 Bug file (`bugs/BUG-n.md`, reporter, N4)

Frontmatter `cases`, `requirements` = the unions; `red_test` = the primary's (flat, as today, `artifact-contract-run.md:58`).
Body sections `## Cause` (statement, how confirmed, "Not verified:" claims) and `## Manifestations` (one line per manifestation:
action, start state, seen, expected with the requirement, its red test command or "no test: <reason>"), and the sentence
"After the fix, re-check every manifestation; one that still fails is a separate bug." — the executor of that re-check is the
person/developer after this run (nothing in this run fixes the product); in a later story it is the regression list (P24).

## 9. The neighbourhood table (hint, code never merges)

- **Producer:** new `PKG/scripts/bug_neighbours.py` (pure `neighbours(task) -> dict`, CLI `bug_neighbours.py --task-root <T>` printing
  ONE JSON line; reads only, writes nothing — FR-45, AR-14).
- **Inputs:** `contract.triage_failures(run-report)` (the S7 targets incl. `#obs`/`#sur`, `contract.py:4498-4515`); the observations of
  manual records (`{step, expected, seen, evidence, quote}`, `explore-charter.md:26`); the manifest tests (case, test file); plan rows
  (requirement per case); when present, `triage.json` rows and drafts (`BR.draft_cases`, `BR.draft_requirements`, `draft_location`,
  `mechanism.basis` code lines). The `code_line` group key is `bug_records.normalize_location` of `draft_location` / of a basis
  entry's `path:line` — the same normaliser `same_location` uses, never a second one.
- **Shape:** `{"groups": [{"key": "requirement" | "case" | "test_file" | "code_line" | "seen", "value": "...", "members": [{"kind":
  "failure" | "observation" | "surprise" | "row" | "draft", "id": "...", "case": "..."}]}], "notes": [...], "unreadable": [...]}`;
  a group exists only with 2+ members; `seen` is EQUAL text after whitespace squash and casefold (equality, no meaning, FR-12);
  "element" is NOT a key in v1 (no structured element field exists in observations; §13, F-8).
- **Readers:** the analyst (S7) and the scribe (its acceptance of the analyst's merges). Never a gate, never a refusal; census class
  `shape`, non-blocking.
- **Handed (FR-15):** driver: a new `Driver.s7_neighbour_lines(dispatch)` called at the ONE site beside `s7_place_lines`
  (`story_run.py:3203`), printing at most `brief_neighbours_max` groups (data row) and the command for the rest; skill road:
  `s7.md` Dispatch section names the command; role cards in `brief_pack.py` `ROLE_COMMANDS["qa-failure-analyst"]` (`:259-273`) and
  `["qa-doc-scribe"]` (`:274`): `bug_neighbours.py --task-root <task root> - the failures, observations, rows and drafts that share a
  requirement, case, test file, code line or seen value; a hint, never a verdict`. (Card lines cost nothing on the static process
  ratchet: the brief counts at its ceiling, `role_load.py:519`.)
- Empty outcome: "No two failures share a requirement, case, test file, code line or seen value." A table that cannot be computed
  whole says so (AR-28), never "none".

## 10. Charter text (tester's experience, P27) — the gist each node writes

All experience text goes under `<!-- kind: craft -->` (it costs no process tokens); only keys and commands go under
`<!-- kind: process -->`, and every process addition is paid by a named cut or by an owner-authorised raise (§11, F-10..F-12).

- `qa-failure-analyst.md`, "Where bugs hide" (craft, `:30`): **"Several reds, one cause.** Three APP_BUG rows on one field look like
  three bugs until you lay them side by side: the same element, the same requirement, the same odd value. Filed apart, the cause is
  fixed once and two stay, or fixed three times." **"A behaviour that depends on where it started.** The same keys give 11 after
  erasing and 1 over a selection; a result seen from one start is half a fact."
- "Techniques" (craft, `:46`): **"Lay them side by side before you draft."** Read every APP_BUG row and observation together (the
  neighbourhood command is a hint), name the mechanism you suspect. **"Discriminate the cause."** Change one thing in the start state
  (empty or filled, selected or erased, the previous value, stock) and run it again on the stand; the result that differs is the
  evidence. **"Say how far you got."** Each statement of the cause is confirmed by a named run or code line, or marked not verified.
  **"One cause, one draft."** Merge only on a confirmed cause; a suspicion keeps separate drafts that name each other. Each
  manifestation keeps its own evidence and its own red test.
- "Tools" (process, `:60`): the command `bug_neighbours.py` replaces `:70`'s clause "one draft per `defect_location`, or mark
  `distinct_defect`" (the `same_location` refusal names its own doors, 5.16; the rule lives in the craft line "One cause, one
  draft"). The keys are NOT listed in Tools: `:69` already points to the key page, which N1 extends.
- `qa-bug-reporter.md:44` (craft, Techniques `:39`) rewritten: **"One cause, one report.** Defects with one confirmed cause are one
  report listing every manifestation, each with its steps from its own start and its own failing test; a suspected shared cause is a
  link between separate reports, never a merge." `:36` kept; `:33` kept. Process Tools `:58` gains the section names only per F-11.
- `explore-charter.md` (Techniques, craft `:43`) and `qa-runner.md` "Where bugs hide" (craft `:27`): **"Vary the start on odd
  input.** When a field behaves oddly, try the same keys from another start: empty and filled, selected and erased, a previous value,
  a different stock; write the start in the row."
- `qa-doc-scribe.md`: the acceptance of the analyst's merges goes as one bullet in "Where bugs hide" (craft, `:28`), NOT into item 5
  (`:26`, process): **"A merge the cause does not explain.** A merged draft whose manifestations the cause does not explain, or two
  drafts the neighbourhood table groups with no word on why they are apart, go back to the analyst with the quote." Item 5 already
  covers returning the triage.

## 11. Nodes (written for a weaker model)

All paths absolute. Parallel nodes have disjoint `owns`. Witness per node = the test FILE that judges each owned path
(`plans/builder-rules.md` 7b, host adaptation 11); slow files (`test_story_run_*`, `test_controller_*`) are CI's. Every package node:
`architecture:` and `judgment:` lines in the commit, a `changelog.d/t-2187-<node>.md` fragment, FR pass by sections C, D, E, G.

**Census rule (Lead, 10.11.2026, critic m7).** No node edits `PKG/scripts/tests/fixtures/judgment-census.json`: its `ratchet`
object, `blocking_per_role` included, is ONE line (`:4`), so parallel edits conflict and the counts must be ADDED. Each node lists in
its report (i) the census rows of its new or altered units (unit, class, roles, owner) and (ii) the `blocking_per_role` counts it
raises and by how much: N1 none (readers, no refusal); N2 `qa-failure-analyst` (S7 claim `_claim_bug_has_a_draft`: manifestation
keys, `merged_unconfirmed`) and `conductor` (gate B rehearsal `check_bug_drafts`); N4 `qa-bug-reporter` (`check_bug_form`,
`artifact_producer.validate`); N3a, N3b, N6, N7 none unless their report shows one. The INTEGRATOR writes all rows and the summed
counts in one commit at convergence and names the raise in the verdict (AR-20). Edge: on a node's branch `test_judgment_census.py`
may be red for exactly the units the node listed; it is therefore not in any node's witness and runs in the BATCH CANON after the
integrator's commit (CI).

**Process ratchet rule (Lead, 10.11.2026, critic M7).** `role-load.json` `process_ratchet_tokens` has zero headroom for the four
roles touched. Each node that adds process text names the cut that pays for it; where no honest cut exists, the raise is the owner's
fork (F-10..F-12) and the node, after the owner's word, sets the row to its MEASURED value (slack 0), never above the authorised cap.
Before the word the node runs by the fork's recommendation and reports the measured overrun. Every such node attaches
`python -B ai-packages/qa-factory/scripts/role_load.py --all` output (before and after) to its report.

Order: **N1** first (schema + readers). Then in parallel: **N2**, **N3a**, **N3b**, **N4**, **N6**, **N7**. **N5** (markdown) may
run in parallel with N1. **N8** after N1 and N5 are merged (it sets the cutoff, §3.2). **N9** last.

**N1 — schema, constants, readers.**
owns: `D:/ws2/wt-fbfix/ai-packages/qa-factory/references/artifact-contract-run.md` (section `bug-drafts/*.json` only),
`D:/ws2/wt-fbfix/ai-packages/qa-factory/references/slices/qa-failure-analyst/artifact-contract-run.md` (regenerated by
`python -B scripts/contract_slices.py --write`; only this slice may change — any other file the write touches is a stop),
`D:/ws2/wt-fbfix/ai-packages/qa-factory/scripts/contract.py` (new constants only, beside `:1828-1839`),
`D:/ws2/wt-fbfix/ai-packages/qa-factory/scripts/bug_records.py` (NEW functions only, a new section after `same_location_problems`),
`D:/ws2/wt-fbfix/ai-packages/qa-factory/scripts/place_answers.py` (`capture_stands` lift only),
`D:/ws2/wt-fbfix/ai-packages/qa-factory/scripts/tests/test_bug_manifestations.py` (new).
- `contract.py`: `MECHANISM_STATUSES = ("confirmed", "unverified", "unknown")`, `MECHANISM_BASIS_KINDS = ("code_line", "run")`
  (+ `"person"` only if F-6 (a)), `BUG_MECHANISM_CUTOFF = None` (placeholder: no obligation; N8 sets the date, §3.2).
- `bug_records.py`: `draft_cases(draft) -> list` (union of `case`, `cases`, `manifestations[].case`, order kept, unique);
  extend `draft_requirements` (`:1659`) with `manifestations[].requirement`; `manifestation_refs(draft) -> [(instance, attempt)]`;
  `manifestation_summary(draft) -> [str]` (one line each: action, start, seen); `mechanism_problems(task, draft) -> [(code, detail)]`
  (code lines through `_fact_problem(task, entry, None, "")`, runs through `place_answers.capture_stands`);
  `manifestation_problems(task, draft, rows) -> [(code, detail)]` (a code-reading-absorbed manifestation: `from_draft` + `evidence`,
  no `triage_row`/`probe`, is valid). Closed reason codes as module constants (`R_MECH_*`, `R_MAN_*`).
- `place_answers.py`: public `capture_stands(task, case, capture, quote) -> list`; `_capture_list` calls it.
- Key page (`bug-drafts/*.json` section): the three keys of §3.1 with their empty outcomes; `siblings` marked legacy with the pointer
  to `possibly_same_cause` and why that key is not `possible_duplicate` (`gate_brief.py:75`); the code-reading absorption sentence.
- Process cost (analyst slice): cut `siblings, ` from the Optional list's live keys (it moves to the legacy sentence); the rest of the
  addition (~380 tokens with N5's Tools line, estimate, not measured) is F-10.
- Tests: every row of §3.2, every adversarial input of §4 and §6 (capture, code line); `draft_cases` with `case` + `cases` +
  manifestation; old draft -> `[]` problems, `draft_cases == [case]`; `BUG_MECHANISM_CUTOFF is None`.
- DoD: `python -m pytest ai-packages/qa-factory/scripts/tests/test_bug_manifestations.py ai-packages/qa-factory/scripts/tests/test_place_answers.py -q` green (from the worktree root); `python -B ai-packages/qa-factory/scripts/contract_slices.py --check` clean; `role_load.py --all` before/after attached; census rows listed in the report (census rule).

**N2 — pairing, S7 claim, gate B rehearsal, bug text.**
owns: `D:/ws2/wt-fbfix/ai-packages/qa-factory/scripts/bug_records.py` (`pair_drafts`, `_blocker_cover`,
`same_location_problems`, new `merged_unconfirmed`, `bug_text`, `write_draft_texts`),
`D:/ws2/wt-fbfix/ai-packages/qa-factory/scripts/handoff_check.py` (`_claim_bug_has_a_draft`),
`D:/ws2/wt-fbfix/ai-packages/qa-factory/scripts/gate_preflight.py` (`check_bug_drafts`), tests `test_bug_records.py`,
`test_handoff.py`, `test_gate_preflight.py`.
- Behaviour: rows 5.1, 5.2, 5.3, 5.16, 5.17 of §5; door texts as in 5.2 and 5.16; F-2 (a): `merged_unconfirmed` refuses at the S7
  claim and is a `factory_fixable` finding at the rehearsal.
- `merged_unconfirmed(task, drafts)`: file `bug_records.py`; callers `handoff_check._claim_bug_has_a_draft` (passes `art.root`) and
  `gate_preflight.check_bug_drafts` (passes its task root); `pair_drafts` signature and purity unchanged; tests in 5.1.
- F-5 finding in `check_bug_drafts` guarded by `C.BUG_MECHANISM_CUTOFF` (`None` -> skipped), tests in 5.3.
- DoD: `python -m pytest ai-packages/qa-factory/scripts/tests/test_bug_records.py ai-packages/qa-factory/scripts/tests/test_handoff.py ai-packages/qa-factory/scripts/tests/test_gate_preflight.py -q` green; census rows and the `blocking_per_role` counts for `qa-failure-analyst` and `conductor` listed in the report (census rule).

**N3a — traceability, report, dashboard.**
owns: `D:/ws2/wt-fbfix/ai-packages/qa-factory/scripts/traceability.py` (`story_bug_records`),
`D:/ws2/wt-fbfix/ai-packages/qa-factory/scripts/report_facts.py` (`_bugs`, `_r_bugs`),
`D:/ws2/wt-fbfix/ai-packages/qa-factory/scripts/factory_dashboard.py` (`story_bug_rows` only),
tests `test_bug_link_s9.py`, `test_bug_reproduction.py`, `test_report_facts.py`, `test_factory_dashboard_joins.py`, and the new AR-13
grep test `test_draft_readers.py` (new).
- Behaviour: rows 5.5, 5.6, 5.9, 5.18; §8.3 text; single-manifestation output byte-equal to today; the grep test of §1 AR-13 over
  every `scripts/*.py` outside `bug_records.py` and `scripts/tests/` (positive control inside the test: the same pattern finds a
  planted line in a temp file).
- DoD: `python -m pytest ai-packages/qa-factory/scripts/tests/test_bug_link_s9.py ai-packages/qa-factory/scripts/tests/test_bug_reproduction.py ai-packages/qa-factory/scripts/tests/test_report_facts.py ai-packages/qa-factory/scripts/tests/test_factory_dashboard_joins.py ai-packages/qa-factory/scripts/tests/test_draft_readers.py -q` green; `python -B ai-packages/qa-factory/scripts/selftest.py --lang` clean.
- Edge: the grep test lands with N3a while N2/N3b/N4 change other readers in parallel; it is written against the post-batch tree and
  may be red on N3a's branch only for `gate_brief.py` / `gate_preflight.py` lines the parallel nodes remove; N3a lists those lines in
  its report and the integrator's BATCH CANON is where it must be green.

**N3b — gate B packet.**
owns: `D:/ws2/wt-fbfix/ai-packages/qa-factory/scripts/gate_brief.py` (`packet_items`, `undrafted_discrepancies`, `bug_rows`,
`render_gate_b`, new `merged_bug_block`), `test_gate_brief_and_retro.py`, `test_human_reading.py`.
- Behaviour: rows 5.7, 5.8; §8.1, §8.2; `human_text.price_problems` empty on the new block; no file name, no field name in the body.
- DoD: those test files green.

**N4 — reporter and bug file validation.**
owns: `D:/ws2/wt-fbfix/ai-packages/qa-factory/agents/qa-bug-reporter.md`,
`D:/ws2/wt-fbfix/ai-packages/qa-factory/scripts/validate_artifacts.py` (`check_bug_form` only),
`D:/ws2/wt-fbfix/ai-packages/qa-factory/scripts/artifact_producer.py` (`validate`, the `bug` branch `:117-126` only),
`D:/ws2/wt-fbfix/ai-packages/qa-factory/references/artifact-contract-run.md` (section `bugs/BUG-n.md` only — after N1 merged),
`D:/ws2/wt-fbfix/ai-packages/qa-factory/references/slices/qa-doc-scribe/artifact-contract-run.md` (regenerated by
`contract_slices.py --write`; only this slice may change),
`test_validate_artifacts_report.py`, `test_bug_filing.py`.
- Behaviour: §10 reporter text (craft `:44`); row 5.13 (`check_bug_form(..., draft=None)`, `artifact_producer.validate` resolves the
  draft through `BR._draft_of` when `task_root` is given, else a not-checked line); §8.4; `check_bug_filing_header` unchanged.
- Process cost: reporter `:58` (Tools) gains the section names only per F-11; the `bugs/BUG-n.md` section addition lands in the
  scribe's slice (~65 tokens, estimate), F-12. No honest process cut found in either: `:44` is craft and pays nothing.
- DoD: `python -m pytest ai-packages/qa-factory/scripts/tests/test_bug_filing.py ai-packages/qa-factory/scripts/tests/test_validate_artifacts_report.py -q` green; `selftest.py --lang` clean; `contract_slices.py --check` clean; `role_load.py --all` before/after attached; census rows and the `qa-bug-reporter` count listed in the report.

**N5 — analyst, explore, runner, scribe charters.**
owns: `D:/ws2/wt-fbfix/ai-packages/qa-factory/agents/qa-failure-analyst.md`,
`D:/ws2/wt-fbfix/ai-packages/qa-factory/references/explore-charter.md`,
`D:/ws2/wt-fbfix/ai-packages/qa-factory/agents/qa-runner.md`,
`D:/ws2/wt-fbfix/ai-packages/qa-factory/agents/qa-doc-scribe.md`.
- Behaviour: §10 text; experience under `<!-- kind: craft -->` sections (existing ones: analyst `:30`, `:46`; runner `:27`;
  explore-charter `:43`; scribe `:28`), keys/tools under `<!-- kind: process -->`.
- Cuts per role (Lead, 10.11.2026, M7):
  - analyst: Tools `:70` — the clause "one draft per `defect_location`, or mark `distinct_defect`" is CUT and the
    `bug_neighbours.py` line takes its place; keys are not repeated in Tools (`:69` points to the key page). Remaining overrun with
    N1's key page: F-10.
  - runner: every addition is craft (`qa-runner.md:27`, `explore-charter.md:43`); process unchanged — DoD shows runner process
    14,388 before and after.
  - scribe: the merges acceptance is a craft bullet (`:28`), item 5 (`:26`) untouched; scribe process unchanged by N5 (N4's slice
    change is F-12).
  - reporter: not N5's file.
- DoD: `role_load.py --all` before/after attached: runner and scribe process unchanged by this node, analyst process overrun printed
  and within F-10's cap (or the recommendation of F-10 before the owner's word); doc witness per CLAUDE.md rule 11 (keys quoted
  verbatim from §10, committed or attached script, a negative control); `selftest.py --lang` clean.

**N6 — neighbourhood table.**
owns: `D:/ws2/wt-fbfix/ai-packages/qa-factory/scripts/bug_neighbours.py` (new),
`D:/ws2/wt-fbfix/ai-packages/qa-factory/scripts/brief_pack.py` (`ROLE_COMMANDS` two cards),
`D:/ws2/wt-fbfix/ai-packages/qa-factory/scripts/story_run.py` (new `Driver.s7_neighbour_lines` + one call at `:3203`),
`D:/ws2/wt-fbfix/ai-packages/qa-factory/references/place-answers.json` (`brief_neighbours_max` row) — or a new data file if F-8
says so, `D:/ws2/wt-fbfix/ai-packages/qa-factory/scripts/tests/test_bug_neighbours.py` (new).
- Behaviour: §9 (the `code_line` key through `normalize_location`). Tests: two failures of one case -> one `case` group; equal `seen`
  after squash/casefold -> one group; different -> none; no file written; unreadable triage -> `unreadable`, not empty; two drafts at
  one `defect_location` -> one `code_line` group with the value `normalize_location` gives; the one call site (mirror
  `test_place_session.py:380-384`).
- DoD: `test_bug_neighbours.py`, `test_brief_pack_roles*` (the card test), `test_place_session.py` green; `story_run.py` slow files
  are CI's.

**N7 — absorbed drafts' places.**
owns: `D:/ws2/wt-fbfix/ai-packages/qa-factory/scripts/place_answers.py` (`settled_answer`, `places` — after N1 merged),
`test_place_answers.py`. Behaviour: row 5.10. DoD: `test_place_answers.py`, `test_walk_receipt.py` green.

**N8 — phase text and the cutoff.**
owns: `D:/ws2/wt-fbfix/ai-packages/qa-factory/skills/qa-story/phases/s7.md`,
`D:/ws2/wt-fbfix/ai-packages/qa-factory/skills/qa-story/phases/s8.md`,
`D:/ws2/wt-fbfix/ai-packages/qa-factory/scripts/contract.py` (the `BUG_MECHANISM_CUTOFF` line only; N1 is merged before N8
starts, so the owns do not overlap in time).
- s7.md "No repair — APP_BUG" (`:208-219`): one draft per mechanism, `manifestations`, the neighbourhood command; Dispatch section
  names the command on the skill road. s8.md beside `:28` and `:324`: `split` / `merge` -> `rework --stage S7` with the words file;
  a `split` of drafts sharing a `defect_location` writes `distinct_defect` with the person's words (5.16).
- Cutoff (Lead, 10.11.2026, M5): N8 lands LAST of the charter/key-page nodes (after N1 and N5); in its own commit it sets
  `BUG_MECHANISM_CUTOFF = "<the day of that merge, YYYY-MM-DD>"`. Before: `None`, nothing asked; after: §3.2.
- DoD: doc witness (as N5); `selftest.py --lang` clean; `python -m pytest ai-packages/qa-factory/scripts/tests/test_gate_preflight.py -q`
  green with the date set (N2's tests in 5.3 cover both worlds); `role_load.py --all` shows no role's process changed by s7/s8 (phase
  files are not in `inject-map.json`; if it shows a change, the node stops and reports).

**N9 — live proof (FR-33).** LOCAL-1 rerun on MyBooks (stand per `docs/RUNBOOK.md` §11). Expectation (subject to F-9): the
book-page quantity field is ONE draft with >= 3 manifestations (0/-1/1.5/abc/erase), `mechanism.status: confirmed` with a code line
(`BookDetailPage.tsx:164` per `experiments/mybooks/add-to-cart-disputed-places.md` card 1) and/or two runs from different starts; the
cart "12" behaviour (`CartPage.tsx:183`, card 3, a different code line) is a SEPARATE draft; gate B shows the merged row with the
`split` door; the report lists the manifestations. Evidence: the run's `work/bug-drafts/*.json`, `gate-b` text, `test-report.md`,
under `experiments/<exp>/`.
DoD (Lead, 10.11.2026, M10), both required:
(i) at least one merged bug whose `mechanism.basis` holds `run` entries from two DIFFERENT `start_state` values, captured by the
analyst in THIS run (captures under this run's `work/evidence/manual/settle-*`, standing by `capture_stands`); the cart's two starts
(start 2 against start 1) are the natural candidate — a `code_line`-only basis does not satisfy (i);
(ii) the analyst's S7 stage spend of this run printed next to the previous LOCAL-1 run's S7 spend from its carrier
`D:/ws2/wt-fbfix/experiments/mybooks/thinking-roles/thinking-roles.md:115` (arm-B line, "S7 $1.37"; the triage-only figure
`:140`, "триаж S7 $0,85", stated beside it), same metric (the stage's dollar spend from the story's own journal, FR-24) and the
counting carrier named (FR-26, pt.6b). This is the probe-cost detector of F-7 and §13 fact 6.

## 12. Forks for the owner (plain words, recommendation each)

**Lead, 10.11.2026.** Технические развилки решены по рекомендации (владелец может отменить): F-1 (а), F-2 (а), F-3 (а), F-4 (а),
F-5 (а), F-8 (а). Владельцу вынесены F-6, F-7, F-9; до её слова узлы исполняются по рекомендации (а). F-10..F-12 (бюджет текста
ролей) — владельцу, добавлены раундом правки t-2194.
**Владелец, 10.11.2026 («Да, запускай»):** приняты рекомендации (а) по F-6, F-7, F-9, F-10, F-11, F-12. Подъёмы храповика —
не выше названных потолков, узел ставит измеренное значение.

- **F-1. Кто делает «различающую» пробу.** Сегодня аналитик уже умеет ходить по стенду через рекордер (места S7, t-1991).
  (а) Аналитик сам, своим сеансом прогулки — ничего нового не строим; цена — время аналитика в его же диспатче. (б) Аналитик заказывает
  пробу раннеру через контроллер — дороже (ещё одна роль, ещё один бриф, ожидание), ломает «одно место — один ответ» мест S7.
  **Рекомендация: (а).**
- **F-2. Проверяет ли код, что у склейки есть доказательство.** (а) Да: черновик с двумя и более проявлениями без строки кода или
  прогона, которые код может перечитать, возвращается аналитику (с дверью: починить основание или разделить); код не судит, «различает»
  ли прогон — это решает писарь и вы на гейте. (б) Нет: только текст хартии и приёмка писаря. **Рекомендация: (а)** — ошибочная склейка
  теряет баг, а проверка ошибается только в сторону «разделить».
- **F-3. Одна красная строка в двух багах.** (а) Разрешить (как сегодня можно двум черновикам стоять на одной строке), таблица соседства
  покажет. (б) Отказывать: строка — в одном баге, второй ссылается «возможно, та же причина». **Рекомендация: (а).**
- **F-4. Старое правило «одно место в коде — один черновик» (`same_location`).** (а) Оставить как есть (оно уже требует склеить или
  написать `distinct_defect`) и не распространять на строки кода из `mechanism`. (б) Распространить: два черновика с одной строкой кода в
  причине — отказ. (в) Превратить в подсказку таблицы соседства, без отказа. **Рекомендация: (а)**; (б) — код начал бы склеивать за роль.
  **Lead, 10.11.2026 (M4):** при (а) текст отказа называет новую дверь — «склеить в один черновик, чьи `manifestations` держат каждую
  строку, или написать `distinct_defect: <почему>`»; разделение на гейте B по слову человека пишет `distinct_defect` с этим словом и в
  отказ не возвращается. Инвариант: ни одна строка APP_BUG не остаётся без черновика ни через одну дверь (5.16).
- **F-5. Обязательна ли причина в новых черновиках.** (а) Обязательна с даты внедрения, пустой исход — `unknown` с объяснением;
  без поля — находка «исправимо фабрикой» с дверью слова человека. (б) Необязательна; отсутствие читается как «причина не указана».
  **Рекомендация: (а)** — иначе анализ причины будет пропускаться молча. **Lead, 10.11.2026 (M5):** (а) действует для КАЖДОГО нового
  черновика триажа (не только склеенного; черновик чтения кода не спрашивается); дату ставит узел, который приземляется последним
  из узлов хартий и страницы ключей (N8), не N1; до неё не отказывается ничего (§3.2).
- **F-6. Обратная дверь «это один баг».** Для черновиков, связанных «возможно, та же причина», показывать на гейте B вариант `merge`.
  И считается ли ваше слово подтверждением причины (основание `person`). (а) Да, дверь есть, слово — основание. (б) Дверь есть, но
  аналитик должен ещё подтвердить прогоном. (в) Двери нет. **Рекомендация: (а)** — FR-9: у каждого решения на гейте есть исполнитель.
- **F-7. Ограничение числа проб.** (а) Без нового лимита — проба идёт в общий бюджет S7. (б) Лимит, например 3 пробы на одну причину.
  **Рекомендация: (а)** до первого измерения; лимит — по данным прогона N9. Детектор этой цены (и цены обязательного поля F-5 в каждом
  черновике — единственных неограниченных затрат спеки) — замер N9 (ii): расход S7 аналитика рядом с расходом S7 прошлого прогона
  LOCAL-1 (`experiments/mybooks/thinking-roles/thinking-roles.md:115`).
- **F-8. Ключ «тот же элемент» в таблице соседства.** В наблюдениях нет поля «элемент» (только текст шага). (а) В первой версии без
  этого ключа. (б) Добавить раннеру необязательное поле `element` (селектор) в наблюдение — ещё одна правка хартии раннера и формы.
  **Рекомендация: (а)**, (б) — отдельным узлом, если N9 покажет нужду.
- **F-9. Что значит «один баг количества» в живой проверке.** По коду это две разные строки: поле на странице книги (0, −1, 1.5, стирание)
  и поле в корзине («12»). (а) Ждём один баг страницы книги с проявлениями и отдельный баг корзины. (б) Ждём один баг на оба поля.
  **Рекомендация: (а)**; (б) противоречит правилу «склейка только при подтверждённой общей причине».
- **F-10. Бюджет текста аналитика (храповик процесса, AR-20).** Новые ключи черновика на странице ключей (`bug-drafts/*.json`, срез
  аналитика) и строка команды `bug_neighbours.py` — это текст процесса; запаса у аналитика ноль (15 996 = храповику). Сокращения,
  которые честно перекрывает новое правило: фраза «one draft per `defect_location`…» (`qa-failure-analyst.md:70`) и `siblings` в
  списке живых ключей — ≈ 20 токенов против ≈ 400 добавленных (оценка, не замер). (а) Поднять храповик аналитика не больше чем на
  380 токенов (15 996 → ≤ 16 376), узел ставит измеренное значение. (б) Не поднимать: описывать новые ключи только в полной
  `artifact-contract-run.md`, а в срез аналитика не пускать — роль не узнает ключи до работы (против FR-38/AR-10). **Рекомендация: (а).**
- **F-11. Бюджет текста репортёра.** В Tools (`qa-bug-reporter.md:58`) нужна одна фраза: «`red_test` — основного проявления; при двух и
  более проявлениях — разделы `## Cause` и `## Manifestations`» (≈ 40 токенов, оценка). Строка `:44`, которую правило заменяет, лежит
  под `<!-- kind: craft -->` и храповик процесса не освобождает. (а) Поднять храповик репортёра не больше чем на 40 (13 901 → ≤ 13 941).
  (б) Не поднимать: назвать разделы внутри строки опыта `:44` (craft) — 0 токенов, но имена полей окажутся в опыте, вопреки делению
  «ключи — в процессе». **Рекомендация: (а).**
- **F-12. Бюджет текста писаря.** Раздел `bugs/BUG-n.md` страницы ключей попадает в срез писаря
  (`slices/qa-doc-scribe/artifact-contract-run.md:79`), не репортёра; два новых раздела файла бага — ≈ 65 токенов (оценка). Честного
  сокращения не найдено. (а) Поднять храповик писаря не больше чем на 65 (16 891 → ≤ 16 956). (б) Не поднимать: требование разделов
  живёт только в отказе `check_bug_form` и в Tools репортёра (F-11), страница ключей его не называет. **Рекомендация: (а)** — один
  носитель формы файла бага.

## 13. Facts I could not establish

1. CLOSED (critic m1): `manual_capture.py ui --as <account>` is given to the analyst (`references/role-commands.json:40-45`); no hook
   restricts `settle-*` (§7 limit 2).
2. CLOSED (critic m2): on the driver road `story_run.py:18383-18386` `record_by_code` returns False for non-approval gate words, so
   the conductor reads `split` / `merge` (§8.2).
3. MyBooks code lines (`BookDetailPage.tsx:164`, `CartPage.tsx:183`) are quoted from `experiments/mybooks/add-to-cart-disputed-places.md`;
   the stand's code was not read.
4. CLOSED (critic M3): `factory_dashboard.py:1309` reads `case or cases`; row 5.18.
5. CLOSED (critic m6): `test_bug_link_s9.py`, `test_bug_reproduction.py` (N3a).
6. Probe cost (analyst tokens per discriminating run) — not measured; N9 (ii) measures the S7 spend.
7. `docs/tasks/specs/reviews/t-1672-local-1-whole-run.md` was not read; its findings are cited only through the RN1-18 finding.
8. CLOSED (critic M2): `artifact_producer.py:126` calls `check_bug_form`; it gets the resolved draft (5.13, N4).

## 14. Small technical choices closed by the designer

- Draft-level `triage_ref` / `red_test` / `reproduction` remain the primary manifestation's; `manifestations[0]` is the primary.
- `possibly_same_cause` replaces the unread `siblings` (kept readable, unread, marked legacy on the key page).
- The neighbourhood table is printed (CLI + brief lines), never a file — no new artifact, no new writer.
- Packet shows at most 6 manifestation lines per bug (`MAX_MANIFESTATIONS_SHOWN`); the bug text shows all.
- `seen` equality = whitespace squash + casefold, nothing more.
- Bug file frontmatter keeps one flat `red_test`; the others go to the `## Manifestations` body section.
- The merged draft keeps the primary draft's file name (its walk receipt stays valid, `bug_records.py:806-833`).
- Fix round: F-5's obligation is a gate B rehearsal finding, not an S7 claim refusal (read from F-5 (a)'s own words "finding ...
  with the person's door"); `check_bug_filing_header` stays unchanged (the union-of-cases check moves to `check_bug_form` with the
  resolved draft); N8 is ordered after N5 so that "the node that lands last" is one named node with disjoint owns.

## 15. Reading trail

Read: `PKG/agents/qa-bug-reporter.md` (whole), `qa-failure-analyst.md` (whole), `qa-runner.md` (whole), `qa-doc-scribe.md` (grep
bug|draft); `PKG/references/artifact-contract-run.md:1-135`, `explore-charter.md` (whole), `human-questions.md` (whole),
`manual-evidence.md` (grep); `PKG/scripts/bug_records.py:245-479, 785-1055, 1226-1720` + function index; `traceability.py:185-264,
440-590` + grep; `delivery_summary.py:270-340`; `gate_brief.py:3984-4385`; `validate_artifacts.py:395-470`; `gate_preflight.py:5050-5200`;
`handoff_check.py:595-645`; `ledger.py:740-790` + grep `bug` (-i); `check_delivery.py` grep + `:1640-1670`, `:2040-2075`;
`report_facts.py:579-632, 2709-2745` + grep; `contract.py:1825-1894`, `:4498-4528`; `place_answers.py:1-60, 153-330, 455-534` + grep;
`story_run.py:14398-14487`; `brief_pack.py:85-114, 250-280`; `judge_results.py` grep; `design/architecture.md:134-153` + AR index;
`scripts/tests/fixtures/judgment-census.json` (head, bug_records rows); `test_judgment_census.py` (class list `:74`);
`PKG/skills/qa-story/phases/s7.md`, `s8.md` (whole); `PKG/changelog.d/t-1991-u1.md`, `t-1991-u3b.md`, `t-2003-role-commands.md`;
`wt-fbfix/plans/piles/release-next/findings/20261102-bag-dublikat-...md`; `wt-fbfix/experiments/mybooks/add-to-cart-disputed-places.md`;
`wt-fbfix/experiments/mybooks/thinking-roles/walker-vs-plain-agent.md` (grep). Negative claims carry their positive controls inline
(§2 `siblings`, §5.14). Not read: `PROJECT.md` principles beyond the auto-loaded copy, `plans/builder-rules.md` (cited by number only).

Fix round 1 (t-2194) read in `wt-fbfix`: the critic verdict whole; `handoff_check.py:595-650`; `qa-failure-analyst.md` whole;
`qa-bug-reporter.md` whole; `qa-doc-scribe.md:1-45`; kind markers of `qa-runner.md` and `explore-charter.md` (grep `kind:|^#`);
`role_load.py` (grep: craft/process split `:26-30`, `:147-226`; brief at ceiling `:519`); `role-load.json` whole; `inject-map.json:76-115`;
`references/slices` (grep `^#+ .*(bug-drafts|BUG-n)`: analyst `:84`, scribe `:79`); `slices/qa-failure-analyst/artifact-contract-run.md:84-115`;
`contract_slices.py` (grep `--write|--check`); `validate_artifacts.py:405-470`, `:2470-2504`; `artifact_producer.py:105-132` + grep
`task_root` (`:73-98`, `:284-285`); `bug_records.py:440-479`, `:545-584`, `:995-1011`, `:1651-1687`; `judgment-census.json:1-5`;
glob `test_*dashboard*.py`; grep `story_bug_rows|write_draft_texts|bug_text\(` and `import artifact_producer` over `scripts/tests`;
grep `S7.{0,120}` over `experiments/mybooks/thinking-roles/thinking-roles.md` (`:115`, `:140`). Negative: handoff_check has no S8
bug-file claim (grep `BUG-|bugs/|qa-bug-reporter` empty; positive control `bug-drafts|qa-failure-analyst|S8` found `:601`, `:620`).

## 16. Fix round 1 (critic t-2187)

- M1: §5 row 5.17 (`bug_text`/`write_draft_texts`, Cause + Manifestations, single-manifestation golden); N2 owns it; §1 AR-21 row; §8.1 rules.
- M2: §5 row 5.13 rewritten (`check_bug_form(..., draft=None)`, resolved by `artifact_producer.validate` via `_draft_of` with `task_root`, not-checked line without); §1 census table (two rows); N4 owns `artifact_producer.py`; §13 fact 8 closed.
- M3: §5 row 5.18 (`factory_dashboard.story_bug_rows` via `BR.draft_cases`); §1 AR-13 grep test widened to every `scripts/*.py`; N3a owns both + `test_draft_readers.py`; §13 fact 4 closed.
- M4: §5 row 5.16 (new refusal text, `distinct_defect` with the person's words on a split, invariant); §8.2 analyst-on-split paragraph; F-4 Lead note; N2, N8 behaviour; §1 AR-24/25 row. Critic's alternative (exempting `possibly_same_cause` drafts from grouping) not taken, per the Lead decision.
- M5: §3.2 F-5 row (every new triage draft) and temporal edge (three worlds); `BUG_MECHANISM_CUTOFF = None` in N1; N8 sets it and is ordered after N1/N5; F-5 Lead note; 5.3 tests both worlds; §14.
- M6: §3.2 last row (code-reading form: not asked; absorbed as manifestation with `from_draft` + fact evidence; `R_CR_TWICE`); §2; §3.1 keys; N1 `manifestation_problems`.
- M7: §11 process ratchet rule; N1/N4/N5 cost lines (cuts: analyst `:70` clause, `siblings`; runner and scribe moved to craft = 0); §10 head; §2 facts; forks F-10 (analyst ≤ +380), F-11 (reporter ≤ +40), F-12 (scribe ≤ +65).
- M8: §1 census table (`merged_unconfirmed` new, `pair_drafts` pure); §5 row 5.1 (function, callers, purity test); 5.2, 5.3; §6; N2 bullet.
- M9: §8.1 (row 2 claim replaced, cart as row 3), §8.3 (same), §3.1 example claim, §3.1 keys sentence.
- M10: N9 DoD (i) two start states in this run, (ii) S7 spend vs `thinking-roles.md:115`; §7 limit 3; F-7.
- m1: §7 limit 2; §13 fact 1 closed.
- m2: §8.2 executors paragraph; §13 fact 2 closed.
- m3: §5 row 5.1 (`_blocker_cover` via `draft_cases`, test); §1 census table; N2 owns `_blocker_cover`.
- m4: §6 third bullet (`_fact_problem` itself); §1 census row `mechanism_problems`; §4; N1.
- m5: §3.1 `possibly_same_cause` key (legacy `siblings`, why not `possible_duplicate`, `gate_brief.py:75`); N1 key page bullet.
- m6: §5 row 5.5 test cell; N3a owns/DoD; §13 fact 5 closed.
- m7: §11 census rule (integrator writes; counts per node); §1 AR-29 and AR-20 rows; N1/N2/N4 DoD.
- m8: §2 `brief_pack.py:3216`/`:3225`; §5 row 5.3 `:5118`.
- m9: F-7 names N9 (ii) as the detector of probe cost and of F-5's per-draft field.

Fix round: returned — none.

**Владелец, 10.11.2026 (о N9):** «живой перепрогон отложи. Сделаем после завершения изменений в параллельных сессиях». N9 не
запускается до её слова; до тех пор пачка закрыта кодом, но не доказана живым прогоном (FR-33).

## 17. Lead answers after N1 and N5 (10.11.2026; merged as `e1b0cbb12` on `bm/integration`)

N1's questions and deviations, decided by the Lead; each names the node that carries it.

- A1 (`kind: person` basis, F-6 (a)). Shape: `{"id", "kind": "person", "quote": "<the person's own words at gate B>"}`. It STANDS when
  `quote` is non-empty text and is found (whitespace-squashed, casefolded) in the person's recorded gate B words of this task, read
  through the reader the package already has for those words; no such record or no match -> it does not stand (today's N1 behaviour:
  `R_MECH_NO_BASIS`). Invariant: a merge on the person's word is never accepted on words the factory did not record. Carrier: **N2**
  (extends `mechanism_problems`; if no reader of the gate B words exists, N2 returns that as a question and leaves N1's behaviour).
- A2. `mechanism.statement` is required non-empty text when `status` is `confirmed` or `unverified`; optional for `unknown`
  (`why` is the required text there). New reason `R_MECH_STATEMENT`. Carrier: **N2**.
- A3. An absent `basis` or `claims` key reads as an empty list — accepted as N1 built it.
- A4. Total `ratchet_tokens` rows are raised by the integrator to the measured values and named in the merge message (AR-20):
  analyst 17743 -> 18307, runner 15555 -> 15596, scribe 17827 -> 17883; analyst process 15996 -> 16282 (F-10). A later node that
  adds charter or slice text reports its measured before/after and does NOT edit `role-load.json` total rows; the integrator sets them.
- A5. A manifestation requires non-empty `action`, `start_state`, `seen`, `evidence`; `requirement` and `case` stay optional — accepted.
- D1. `contract_slices.py --write` also regenerates the slice's `index.md` size line — accepted for every node that regenerates a slice.
- D2. `capture_stands(task, case, capture, quote, field="seen")` — accepted.
- D3. `draft_cases` returns the cells as written; a reader that holds the artifacts config passes the result through `C.case_ids`
  exactly as it does today for `case or cases`. Carriers: **N2**, **N3a**, **N3b**, **N4**.
- First-manifestation check: a bare-instance `triage_ref` and a full-key `manifestations[0].triage_row` naming the same instance are
  the SAME row (compare by instance when either side has no attempt). Carrier: **N2** (fix in `manifestation_problems`, with a test).
