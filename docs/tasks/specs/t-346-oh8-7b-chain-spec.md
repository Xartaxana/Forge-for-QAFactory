# t-346 — OH8-7b..h: the census classifies the 190 pending subclass refusers (designer draft; waits for Lead acceptance)

Source of the decisions: the Lead (Fable, 2026-11-13): F1 = (a) `SUBCLASS_UNIT_FILES`; F3 = 20-40 functions per node, files
never split except `probe_by_code.py`; F4 = strict sequence, one critic pass per PAIR of consecutive nodes, the last node alone;
the first node carries the mechanism (a mechanism commit, committed by the Lead). They are not reopened here. Where they
collide with each other or with the code, the collision is a fork (section 6), with a recommendation the nodes can run on.

Base of every fact below: worktree `C:\QAFactory\forge-repo\.claude\worktrees\oh8-7` (branch `wip/oh8-7`, commit 0bc7b1d),
and the measured list `...\scratchpad\oh8-7-pending.txt` (190 lines, authoritative). Line numbers are of that tree.

---

## 1. Invariants, owners, census classes, the four questions

### 1.1 AR-n touched (the change check of each is a DoD line, section 3.3)

| AR | how the chain touches it | how it is kept / the change check in the DoD |
|---|---|---|
| AR-29 | 190 functions that refuse only through a package subclass of `ValueError` / `StateConflict` become census units with a judged `class`, `roles`, `owner` | every row is judged per unit (section 4), never defaulted; a reading other than `shape`/`xref` goes up as a question (4.3); a `word-list`/`meaning-proxy`/`meaning` reading stops the node (edge E9). DoD 7: `test_judgment_census.py` green; the critic of the pair reads every new row (question 11) |
| AR-20 | each node's rows raise `blocking_per_role.*` (and `safety`, if a guard is confirmed) | DoD 6: every raised key listed in the commit message and the report, row by row: key, old -> new, reason `census classifies subclass refusers of <files> (OH8-7x)`, with the reconciliation witness (delta per key == the node's new rows naming it); the critic verdict repeats the list (question 9) |
| AR-13 / axis 32 (one scanner, no second AST walk over refusals) | the new unit road reads the widened sites `units_of` ALREADY gets from `refusal_registry.sites(..., raises=raise_family(...))` (`test_judgment_census.py:276-277`) | DoD 8: `refusal_registry.py` is not in any node's owns; a grep of `ast.Raise` in `test_judgment_census.py` has no hit (positive control: the same grep hits `refusal_registry.py:1086`) |
| AR-22 (producer and reader in one commit) | `SUBCLASS_UNIT_FILES` (producer) and `units_of` (its one reader) are born in OH8-7b and die in OH8-7h, each time in one commit; the totals keys `pending` / `pending_names` and the problem key `C7` die with their one reader (the test itself) | a grep for `subclass_pending|SUBCLASS_PENDING|pending_names` over the tree on 0bc7b1d hits only the test, the fixture `about` and `docs/SIBLING_MAP.md` (the hit list is non-empty and holds the constant's own definition at `test_judgment_census.py:99`, which shows the grep runs; that is a hit of the searched pattern itself, not a control on a different known sample); OH8-7h's DoD repeats the grep, scoped as in 3.5 item 6, with zero hits |
| AR-28 | the pending set is an "unknown" (a refusal not classified); it shrinks by an exact count per node and is gone at OH8-7h | C7 dense at every node; at OH8-7h the second road ends (no pending branch remains) and the `about` / `BLIND_SPOT` / docstring texts say so |

Not touched: AR-1 (`SUBCLASS_UNIT_FILES` is a TEST constant on purpose — "THE SCAN IS NOT DATA", `test_judgment_census.py:12-14`:
census data must never widen or narrow what is a unit; same status as `BLOCKING_ENTRY_FILES` :77); AR-2..AR-12, AR-14..AR-19,
AR-21, AR-23..AR-27 (no script of the package changes; only the census test and its fixture).

FR walk (PROJECT.md "package change" 1): C — FR-14 (`units_of`'s return shape keeps every key until OH8-7h; OH8-7h removes
`pending` together with its only reader). F — FR-28 (the measurer keeps its test: the synthetic tables), FR-41 (the pending
count stays printed until it is 0). G — FR-32 (each node green). A, B, D, E — not touched (no refusal text, no person text, no
identity, no delivery changes).

### 1.2 Owner and census class of every check the chain adds or alters (AR-29, P27)

| check | owner it serves | census class | census row |
|---|---|---|---|
| `SUBCLASS_UNIT_FILES` and the unit road in `units_of` | data (code: a name join over files) | none: a test constant and a test function are not census units (the scan excludes `scripts/tests/`, `SCAN_EXCLUDE` :66) | none |
| the list-form checks on `SUBCLASS_UNIT_FILES` (duplicate, stale; reported under C7) | data | shape (presence / uniqueness of names) | none (test) |
| C1/C2/C3/C7 over the widened unit set | data (code detector) | shape / xref, as today | none (test) |
| each NEW row's `class`, `roles`, `owner` | judgment: the builder judges, the critic of the pair accepts as the tier above (question 11) | the class judged per unit | the 190 rows |
| each raised ceiling | intent of the Lead (a named raise, AR-20), read by the critic (question 9) | — | `ratchet` |

### 1.3 The four questions for `SUBCLASS_UNIT_FILES` (rule 10; this block goes into OH8-7b's commit message, and OH8-7h's commit carries its own block for the removal)

(a) Cost and who pays. A node edits one tuple line and adds 21-38 rows; the census run gets no new walk (the widened site list is
already computed; OH8-7b only moves its computation earlier inside `units_of`). The builder pays the classification (about 190
judgments over the chain); the critic pays one reading of every new row per pair (4 passes); the Lead pays OH8-7b's mechanism
commit and the answers to the questions of section 4.3.

(b) Axes, by enumeration against the current map (36 axes; `docs/SIBLING_MAP.md` on 0bc7b1d and on read-main both hold 36 `## Axis` headings):
- axis 1 (policy <-> role files <-> journal): covered — critic brief q9/q11 lists edited (OH8-7b adds the constants, OH8-7h removes them; 3.4 item 7, 3.5 item 8); CLAUDE.md rule 10 paragraph and designer rule 1 name no constant (checked).
- axis 2 (per-tier exam instruments): n/a — no exam.
- axis 3 (package <-> release copy <-> installed plugin): n/a — test files ship as usual; no release-side step changes.
- axis 4 (rules <-> debt <-> backlog <-> principles): n/a — no FR changes; the temporary second road is bounded by `SUBCLASS_PENDING_CEILING` and these nodes, not by a debt row (same as OH8-7).
- axis 5 (stage twins): n/a — the census is not a stage.
- axis 6 (measurement tools <-> package): n/a — no measurer reads the census.
- axis 7 (per-test identity): n/a.
- axis 8 (story on disk): n/a.
- axis 9 ("is this a test file"): n/a — `SCAN_EXCLUDE` unchanged.
- axis 10 (git-top readers): n/a.
- axis 11 (shell-command recognizers): n/a.
- axis 12 (carriers of the work plan): covered — the nodes are rows of a new untaken batch `onboarding-hooks/9` (section 5); the card rows are the coordinator's move (D-0044).
- axis 13 (dispatch text): n/a.
- axis 14 (transcript readers): n/a.
- axis 15 (console stream setup): n/a — the test prints as before.
- axis 16 (one JSON reader): n/a — the test reads its fixture as before.
- axis 17 (detector verdict shape): n/a — the census is a test, not a detector producer.
- axis 18 (in-tree shrink-only ratchets): covered — `SUBCLASS_UNIT_FILES` joins the axis-18 member text in OH8-7b (grow-only like `BLOCKING_ENTRY_FILES`, which the axis already lists); every raise named row by row; OH8-7h rewrites the clause.
- axes 19-31 (role `tools:` line; host receipt names; markdown tables; host return form; `tests[]` row fields; execution record; freshness; `stand not confirmed`; test-row profile; row-form render site; jsonl appenders; profile commands; role carriers): n/a each — none of these carriers is edited; the chain only reads the scripts.
- axis 32 (where judgment lives): covered — census rows in the same commit as the units (C1); one scanner (`sites()`); rows read by question 11.
- axis 33 (which dispatch am I): n/a.
- axis 34 (one road for one action): covered — the chain shrinks the temporary second road file by file and removes it at OH8-7h; OH8-7b records the road on the axis's "known roads off it" row, OH8-7h removes that line.
- axis 35 (sides of a story): n/a.
- axis 36 (row against a substitute): n/a.

(c) Detector, registered: `test_judgment_census.py` — C1 (a created unit with no row, a row whose unit vanished), C7 (pending count dense; the list-form checks on `SUBCLASS_UNIT_FILES`), C3 (raises); calibration checks 41 (judgment census) and 35 (b) (every raise named), in `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`.

(d) What stops a skip: code on the path. The census test is a `keep` row (layer `register`) printed by `scenario_walk.py --witness-for` for both owned files, and runs in the CI canon. A node that writes rows without listing the file gets C1 "stale row ... no such check unit"; a node that lists without rows gets C1 "... is a check unit (u3) with no row"; a node that does not lower the ceiling gets C7 "below SUBCLASS_PENDING_CEILING"; a node that lowers it too far gets C7 "above". The MEANING of each class is judged by a tier above (critic question 11), not by code.

---

## 2. The mechanism

### 2.1 Behaviour of `units_of` with `SUBCLASS_UNIT_FILES` (OH8-7b introduces it; nodes c..g only add entries; OH8-7h removes it)

New test constant, next to `SUBCLASS_PENDING_CEILING` (:99), with a comment in the file's style:

```python
# OH8-7b..h (F1 (a)): files (names relative to scripts/) in which a widened raise site (a package subclass of
# ValueError/StateConflict resolved per file, or the attribute form) CREATES a unit exactly like a literal raise.
# Grow-only: each node of the chain adds its files with their rows and lowers SUBCLASS_PENDING_CEILING by its count;
# OH8-7h removes this tuple and the pending machinery (every scanned file then creates units from widened sites).
SUBCLASS_UNIT_FILES = (...)
```

`units_of(root, files, registry=(), entry_files=BLOCKING_ENTRY_FILES, unit_files=SUBCLASS_UNIT_FILES)` — a new keyword with the
constant as default (so the synthetic tests pass their own list, like `entry_files`); `analyse(..., unit_files=None)` passes
`SUBCLASS_UNIT_FILES` when None, as it does for `pending_ceiling`.

Exact behaviour:

1. The family and the widened sites (`family = raise_family(...)`, `wide = sites(..., raises=family)`, today :276-277) are computed
   BEFORE the per-file loop (:236), and grouped by file (`wide_by_file`). Nothing else about them changes.
2. In the per-file loop, the u3 line (:246-247) becomes: for a file listed in `unit_files`, units are created from
   `wide_by_file[file]`; for any other file, from `sites_by_file[file]` exactly as today. Both use `add(file, s["function"], "u3")`.
   (The literal sites are a subset of the widened sites — asserted by `test_neg_the_attribute_form_...` :847 — so a listed file
   keeps every unit it had and gains the ones its subclass raises name.)
3. The stage-row pass, the registry pass and the `blocking_files` pass run after, unchanged — so a created unit receives its
   stage `ref`s and suppresses a `<script>` unit exactly like a literal-site unit.
4. The flip loop (:278-289) is unchanged: every widened site flips `blocks` on the unit(s) it hits; an unhit site goes to
   `pending`. A site in a listed file is always hit (its own unit was created in step 2), so it never reaches `pending`.

POSITIONAL invariant (step 2's place): unit creation from widened sites happens in the per-file loop, before the stage-row and
registry passes. What stays unreachable: a pending name whose file is listed (pending ∩ listed = ∅ on every run); a created
unit without the stage `ref` its script's stage row demands; a `<script>` unit beside a function unit of the same script.
What must still be refused: a created unit with no row (C1), a row whose unit vanished (C1 stale), a pending count off its
ceiling (C7).

Both worlds (TEMPORAL, rule 11 (i)):
- before OH8-7b: no `SUBCLASS_UNIT_FILES`; all 190 are pending; C7 holds the count at 190 (or at whatever the tree's constant
  is when the node starts — see 3.2).
- OH8-7b..g: a listed file creates units from widened sites; an unlisted file keeps the (c1) behaviour (flip or pending).
- after OH8-7h: no constant, no pending set, no C7: every scanned file creates units from widened sites (step 2 without the
  branch); `totals["sites"]` counts the widened sites (closed choice C-3); a function refusing only through a subclass is a
  unit like any other and C1 demands its row.

Per-function entries (fork F-P, recommendation (a), which the node table below runs on): an entry is either `file.py` (the
whole file) or `file.py::function`. A widened site creates a unit when its file is listed OR its `file::function` is listed
(the function name as `sites()` reports it: the outermost enclosing function, or a method name; `probe_by_code.py::__init__`
covers every `__init__` of that file, matching the census's (file, function) key). Only `probe_by_code.py` uses this form:
OH8-7b lists its 23 functions; OH8-7c replaces those 23 entries with the single entry `probe_by_code.py`.

### 2.2 Edges (every edge names the invariant it protects)

| # | edge | behaviour | invariant protected | where it is red (test line) |
|---|---|---|---|---|
| E1 | a listed file with a pending function the node leaves without a row | the function is now a unit with no row | no refusal through a subclass in a listed file is unclassified | `test_c1_every_unit_has_a_row_and_every_row_a_unit`: "`<file>::<f>` is a check unit (u3) with no row in judgment-census.json: add a row ..." |
| E2 | the node lists a file but does not lower the ceiling (or lowers it by the wrong count) | pending dropped by N; the constant is off by N (or by the error) | the count only moves by exactly the node's measured number | `test_c7_the_subclass_pending_set_is_dense_and_only_shrinks`: "below SUBCLASS_PENDING_CEILING ...: lower the constant to M" (or "above ...") |
| E3 | a function that, on reading, does NOT refuse to a role (its family exception is raised and caught inside the module, or guards a programming error) | DECIDED (6a F-A = (b)): the row is written WITHOUT `blocks_override`, class by the raising condition as for any unit (4.2 steps 3-5), with `note: "E3: refuses nothing -- <why>; override queued (plans/piles/onboarding-hooks/findings/20261113-gate-form-for-blocks-override-on-non-refusing-units.md)"`; listed in the report. No question is returned for it (a class reading other than `shape`/`xref` still goes up by 4.3, as for any unit). A "no row" answer does not exist under F1 (a): C1 refuses a unit without one | a computed refusal is never relabelled non-blocking inside this chain (the count errs toward extra blocking); a unit that refuses nothing stays findable for the queued override by a grep of `"note": "E3:` in the fixture | C1 if the row is missing; C3 `blocking_per_role.*` above its ceiling until raised (E10) |
| E4 | a file listed twice (or `file.py` and `file.py::f` both listed) | red | one entry per file: the list stays reviewable and a removal is never masked by a duplicate | C7 via `test_c7_...`: "SUBCLASS_UNIT_FILES lists `<entry>` twice (or a function of a listed file): remove the duplicate" |
| E5 | a listed file that no longer exists in the scan (renamed or deleted by another merge), or a `file::function` entry whose function has no widened site any more | red, with the door | a stale entry never stands for coverage that is not there | C7 via `test_c7_...`: "SUBCLASS_UNIT_FILES lists `<entry>`, which the scan does not hold (renamed or deleted?): rename the entry in the commit that renames the file, or remove it; its rows go stale under C1 the same way". A whole-file entry whose file still exists but has no widened-only function is NOT red (it creates nothing; OH8-7h removes the tuple anyway) — closed choice C-4 |
| E6 | an EXISTING listed file loses its entry (a removal) | its created units vanish: their rows turn stale and the pending count jumps back | grow-only, held by code: a removal can never be green | C1 stale rows AND C7 "above SUBCLASS_PENDING_CEILING" |
| E7 | another merge adds a new subclass-only refuser to a LISTED file | a new unit with no row | a new refusal is classified by its author | `test_c1_...` "... is a check unit (u3) with no row" — red for whoever merges second |
| E8 | another merge adds one to an UNLISTED file | pending +1 | the same | `test_c7_...` "above SUBCLASS_PENDING_CEILING" (unchanged OH8-7 behaviour); OH8-7b adds the door "or list its file in SUBCLASS_UNIT_FILES with its rows" to that refusal text |
| E9 | a builder judges a new unit `word-list`, `meaning-proxy` or `meaning` | the node STOPS that row and returns it (4.3); never committed under this chain: the raise of a class ceiling or of `breach` makes `tools/architecture_gate.py` demand `moves <what> to code` (docstring item 7 (v), :51-53), a false statement for a classification; `MEANING_CEILING` is never edited | a classification never smuggles in a breach raise | — (stop, by procedure) |
| E10 | the ratchet: every new blocking row adds 1 to `blocking_per_role.<r>` for each role it names; a `safety` row adds 1 to `safety`. All created units block by construction (their own widened site flips them), so each new row raises every role it names by 1 | the node raises exactly those ceilings to the measured counts (dense) and names each, row by row, in the commit message (AR-20), with the reconciliation of DoD 6; `judgment: adds data check ...` is the gate form for a raise of only `blocking_per_role.*` / `safety` (item 7 (v)) | no silent raise | C3 "above its ceiling" until raised; C3 "below ... lower the ceiling" if raised too far |
| E11 | the reused scanner in a more consequential role: `raise_family` + `sites(raises=)` move from "flip `blocks`" (advice to the count) to "create a unit" (a gate: C1 demands a row) | allowed error direction: EXTRA units only (over-inclusion: a family name resolved where the raise is in fact caught -> a unit that E3 marks). It must never hide a raise it can resolve. Adversarial inputs that must stay on the safe side even in a listed file: `unrelated` (`class A(Exception)`) — no unit; `shadowed_local` / `shadowed_import` — no unit; `tests_only` — no unit; `no_binding` — no unit; `no_arg` (`raise A()`) — no unit (named miss); `cycle` — terminates, no unit. The known collisions `Refusal` x5 / `Refused` x1 (critic t-326 M1) resolve per file | a unit is created only where `raise_family` resolves the name in that file | the synthetic table, 3.3 |
| E12 | a pending function nested inside another function, or a method | the unit is the name `sites()` reports (the outermost function / the method); several `__init__` of one file are ONE unit | one row per (file, function) | C1 two rows, if written twice |
| E13 | a created unit whose script is a `stages.json` detector | it gets the stage `ref` (step 3 runs after creation); C1 demands it on the row. Today none of the 38 files is in `stages.json` (a grep of the 38 names over `references/stages.json` finds none; positive control: `\w+\.py` finds 11 names there) | a registered unit is not counted twice | C1 "`ref` lacks ..." |
| E14 | a listed file with a `<script>` row | the `<script>` row turns stale once a function unit exists. Today the only `<script>` row is `check_coverage.py` (fixture l.78), not in the chain | a stage row counts once | C1 stale row |
| E15 | the pair critic finds a defect in OH8-7b's mechanism after OH8-7c was built on it | the fix round runs on the pair's tip (b+c), one fresh builder with the diff and the verdict (cost gates) | a mechanism defect is fixed once, on top, never by rewriting a committed node | — (process; fork F-D) |

---

## 3. The nodes

### 3.1 Node table (the function lists are copied from the measured file; per-node counts sum to 190)

Ceiling column: the expected `SUBCLASS_PENDING_CEILING` before -> after, if main has not moved; the binding rule is "lowered by exactly the node's count" (3.2).

| node | files (count) | count | ceiling | critic pass |
|---|---|---|---|---|
| OH8-7b | `probe_by_code.py`, first 23 in source order (lines 217-2902), as function entries (F-P) + the mechanism | 23 | 190 -> 167 | pair 1 (b+c) |
| OH8-7c | `probe_by_code.py`, last 23 (lines 3738-8309); entries replaced by `probe_by_code.py` | 23 | 167 -> 144 | pair 1 |
| OH8-7d | execution_request (14), environment_preparation (10), execution_scheduler (4), managed_dependency (1), run_suite (3), red_sandbox (6) | 38 | 144 -> 106 | pair 2 (d+e) |
| OH8-7e | exploration (11), explore_step (1), manual_evidence (3), manual_capture (2), import_test_receipt (7), s7_reorder (8) | 32 | 106 -> 74 | pair 2 |
| OH8-7f | ticket_light (7), ticket_adapter (1), source_inventory (2), source_exclusions (2), vcs_evidence (4), local_keys (2), onboard_apply (6) | 24 | 74 -> 50 | pair 3 (f+g) |
| OH8-7g | s5_plan (6), question_register (6), question_stop (3), person_words (2), grammar (3), assertion_detectors (5), machine_facts (3), driver_dispatch (1) | 29 | 50 -> 21 | pair 3 |
| OH8-7h | hooklib (4), controller (1), story_step (1), event_store (2), retro_numbers (1), host_adapter (1), role_load (6), release_fingerprint (2), selftest (2), config_view (1) + removal of the mechanism | 21 | 21 -> 0, then both constants removed | alone |

Sum: 23 + 23 + 38 + 32 + 24 + 29 + 21 = 190. Every node is within 20-40 (F3). No file is split except `probe_by_code.py` (b/c, function-disjoint). 38 files in all.

Left out on purpose (dispatch edge): `manifest_from_tests.py`, `project_decisions.py`, `baseline_contract.py` — marked "(?)" in the t-337 draft, NOT in the measured list (checked: none of the three names occurs in `oh8-7-pending.txt`). The measured per-file counts agree with t-337 §1 for every file; the old grouping (§2 of t-337) is replaced: `role_load`, `release_fingerprint`, `selftest`, `config_view` moved from the old OH8-7f to OH8-7h so that the hot-file group reaches 20.

The exact function lists (`file.py::function`; the builder saves two re-measure inputs to the scratchpad, one name per line: its node's block, and the union of its node's block and every later node's block to OH8-7h — for OH8-7h the two files are the same):

**OH8-7b (23)** — probe_by_code.py: `__init__`, `parse_node`, `locate`, `_python_entry`, `find_oracle`, `plan_mutation`, `parse_detector_node`, `body_span`, `locate_target`, `_statement_span`, `_matcher_position`, `_inverted`, `plan_detector_mutation`, `checks_of`, `_parse_at`, `_parse_at_row`, `_target_file`, `_profile_of`, `_longer_title`, `run_shape_checks`, `manifest_entry`, `_profile_cwd`, `build_request`.

**OH8-7c (23)** — probe_by_code.py: `claim_key`, `begin_copy`, `release_copy`, `_test_path`, `_dispatch_context`, `_require_cover`, `_probe`, `parse_alternative_token`, `_located`, `_body_of`, `_region_of`, `_model_region`, `_model_edit`, `plan_model`, `_invert_edit`, `_probe_alternative`, `_check_record`, `_row_selection`, `_selected_keys`, `_probe_plan`, `_judge_cli`, `_plan_cli`, `main`.

**OH8-7d (38)**
- execution_request.py (14): `_command_from_profile`, `_entries_of_case`, `_observe_precedent`, `_observe_stand`, `_place_rows`, `_profile_for`, `begin`, `build_mine_request`, `find_active_dispatch`, `probe_record`, `read`, `recover`, `rehearsal_probe`, `s6_close_from_state`
- environment_preparation.py (10): `_claim_locked`, `_facts`, `_observation`, `_runtime_identity`, `_verified_absence`, `observe`, `plan_environment`, `read`, `reconcile_environment`, `transition`
- execution_scheduler.py (4): `_resources`, `_with_native_workers`, `_workers`, `prepare_schedule`
- managed_dependency.py (1): `install`
- run_suite.py (3): `main`, `probe_runtime`, `reparse_run_block`
- red_sandbox.py (6): `_check_row_in_clone`, `_clone_guard`, `_plan_row`, `_run_install`, `install_budget_s`, `plan_setup`

**OH8-7e (32)**
- exploration.py (11): `_clean_stories`, `_config`, `_hit_repos`, `_need_session`, `brief`, `frame`, `narrow`, `place`, `record_answer`, `release_lock`, `set_step`
- explore_step.py (1): `_session`
- manual_evidence.py (3): `_case_thens`, `_request_tail`, `prepare_request`
- manual_capture.py (2): `_read_pair`, `read_login`
- import_test_receipt.py (7): `_copy_evidence`, `_reject_destination_symlinks`, `_safe_local`, `_time`, `_trusted_producer`, `_write_exclusive`, `import_receipt`
- s7_reorder.py (8): `_entry`, `_read_test`, `_triage`, `find_row`, `finish`, `locate`, `main`, `repo_of`

**OH8-7f (24)**
- ticket_light.py (7): `_id_list`, `_load_table`, `_need_list`, `_norm_names`, `project`, `references`, `ticket_url_regex`
- ticket_adapter.py (1): `write_paste_references`
- source_inventory.py (2): `_extra_headings`, `attachment_policy_for`
- source_exclusions.py (2): `read_record`, `write_record`
- vcs_evidence.py (4): `api`, `collect`, `pages`, `readiness`
- local_keys.py (2): `_local_row`, `mint`
- onboard_apply.py (6): `_load_json`, `_proposal_for`, `apply`, `main`, `plan`, `set_login_ui`

**OH8-7g (29)**
- s5_plan.py (6): `_dispatches`, `_scope`, `_words`, `load`, `refresh`, `remarks_of`
- question_register.py (6): `_raise`, `answers_lock`, `raise_question`, `raise_role_question`, `record`, `record_case`
- question_stop.py (3): `_as_count`, `_as_share`, `defaults`
- person_words.py (2): `_from_file`, `read`
- grammar.py (3): `find_blocks`, `render_block`, `replace_block`
- assertion_detectors.py (5): `_claims_once`, `_document`, `_keyed_table`, `assertion_detectors`, `shape_patterns`
- machine_facts.py (3): `_check_scalar`, `_json_line`, `_parse`
- driver_dispatch.py (1): `s5_open_windows`

**OH8-7h (21)**
- hooklib.py (4): `read_config_file`, `story_of`, `story_root`, `story_root_at`
- controller.py (1): `refresh_derived`
- story_step.py (1): `start`
- event_store.py (2): `_require_root`, `_run_after_commit`
- retro_numbers.py (1): `write_retro`
- host_adapter.py (1): `launch_id_keys`
- role_load.py (6): `_check_kind`, `_pick_dispatch`, `_require_role`, `_task_root`, `main`, `settings`
- release_fingerprint.py (2): `_unshipped`, `write_release`
- selftest.py (2): `slow_tests`, `test_layers`
- config_view.py (1): `parse_path`

### 3.2 Step 0 of every node: RE-MEASURE, then stop on a difference

Main moves (waves 11 and 12 land before this chain; every earlier node of the chain lands before the next). The builder runs,
on ITS OWN tree, before any edit, this pure read (command hygiene pt. 4b; saved under the builder's scratchpad, never committed;
its full source goes into the builder's report beside its output;
`python -B <abs path to remeasure.py> <worktree>\ai-packages\qa-factory <node list file> <remaining list file> [--last]`, where
the two list files are the ones saved from 3.1 and `--last` is given by OH8-7h only):

```python
import sys
from pathlib import Path
root = Path(sys.argv[1])
def names(p):
    return {l.strip() for l in Path(p).read_text(encoding="utf-8").splitlines() if l.strip()}
want = names(sys.argv[2])                      # this node's block of 3.1
rest = names(sys.argv[3])                      # this node's block and every later node's block, to OH8-7h
last = sys.argv[4:] == ["--last"]              # OH8-7h only
sys.path[:0] = [str(root / "scripts" / "tests"), str(root / "scripts")]
import test_judgment_census as T
R = T.refusal_registry
found = T.units_of(root, T.scan_files(root), R.REGISTRY)
pending = set(found["pending"])
files = {w.split("::")[0] for w in want}
have = {p for p in pending if p.split("::")[0] in files}
fam = R.raise_family(plugin_root=root, files=found["files"])
wide = {f"{s['file']}::{s['function']}" for s in R.sites(plugin_root=root, files=found["files"], raises=fam)}
units = {f"{f}::{fn}" for f, fn in found["units"]}
extra = sorted(wide - units - pending)         # hit only by a span today: listing its file would CREATE it as a unit
orphans = sorted(pending - rest)               # pending, but in no node from this one to OH8-7h
also = [n for n in extra if n.split("::")[0] in files]
print("pending total:", len(pending), "| ceiling on this tree:", T.SUBCLASS_PENDING_CEILING)
print("node files pending:", len(have), "| spec list:", len(want))
print("missing from the tree:", sorted(want - have) or "none")
print("extra on the tree:", sorted(have - want) or "none")
print("pending names in no remaining node:", orphans or "none")
print("listing would also create:", also or "none")
if last:
    print("whole tree, neither unit nor pending:", extra or "none", "| pending total == 21:", len(pending) == 21)
later = (have - want) & rest                   # the node's files also hold names of a LATER node (probe_by_code.py: b and c)
print("in the node's files, owned by a later node:", len(later))
stop = (want - have) or ((have - want) - rest) or orphans or also or (last and (extra or len(pending) != 21))
# Lead fix 2026-11-13 (t-369 step 0): `have != want` stopped OH8-7b, whose file is split with OH8-7c; a name of a later node is not drift.
sys.exit(2 if stop else 0)
```

What it prints: the pending total and the tree's ceiling; the node's pending count against the spec list; the names missing
from the tree and the extra ones in the node's own files; then the three drift outputs. Its stops (exit 2), besides a
missing/extra name in the node's own files:
- (a) `pending names in no remaining node:` is not `none` — a pending function a wave added in a file of no remaining node
  (otherwise OH8-7h would reach 21 -> 1 and the removal would turn it into a rowless unit);
- (b) `listing would also create:` is not `none` — a widened site in the node's files whose function is neither a unit nor
  pending (hit today only by a nested unit's span), which listing the file would turn into a unit outside the node's list
  (DoD 3's "exactly N" would fail);
- (c) OH8-7h only: `whole tree, neither unit nor pending:` is not `none`, or `pending total == 21:` is `False` — the removal
  would create a unit outside its list.

- Exit 0: proceed. The ceiling is lowered from THE TREE'S value by exactly the spec count (if the tree's value differs from the
  table's "before", that is another node's or merge's move; it is a report line, not a stop).
- Exit 2: STOP before any edit and return a question with the verbatim output. The Lead re-cuts the node (or assigns the
  orphan / extra names to a node); the builder does not adjust the list itself (a node's list is the spec's word).
- Any other exit code (a traceback, e.g. after a wave changed `units_of`'s shape, exits 1): the same stop, with the output.
- The output is pasted in the report as the first witness block.

### 3.3 Per-node DoD (inline; each dispatch copies it with its own N, files and worktree)

`<wt>` = the node's worktree root, e.g. `C:\QAFactory\forge-repo\.claude\worktrees\oh8-7b` (TEMPORAL: it does not exist at spec
time; the dispatch creates it after a push, from the tip that holds the previous node of the chain).

owns (every node):
- `<wt>\ai-packages\qa-factory\scripts\tests\test_judgment_census.py`
- `<wt>\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json`
- OH8-7b and OH8-7h also: `<wt>\docs\SIBLING_MAP.md` (axes 18 and 34 rows only) and `<wt>\docs\tasks\critic-diff-brief.md` (questions 9 and 11 lists only)

non-goals (every node): no edit of any `scripts/*.py` outside `scripts/tests/` (the 38 files are READ); no edit of
`refusal_registry.py`; no class lowered or override added on an EXISTING row; no edit of `MEANING_CEILING`, `BLOCKING_ENTRY_FILES`,
`UNIT_NAME_RE`, `JUDGE_CALLS`, `SCAN_ROOT`, `SCAN_EXCLUDE`; no edit of `tools/architecture_gate.py`; no new test file (new cases
are rows of `SUBCLASS_ROWS` or of the C7 table); no mutation runs (`plans/builder-rules.md` 7b, the owner's word 28.10 / 10.11).

DoD (acceptance criteria and the verification runs):
1. Step 0 output (3.2) pasted, exit 0.
2. The node's entries are added to `SUBCLASS_UNIT_FILES` (OH8-7b: created with the mechanism, 3.4; OH8-7c: the 23 function
   entries replaced by `probe_by_code.py`).
3. An intermediate run of `python -B <wt>\ai-packages\qa-factory\scripts\tests\test_judgment_census.py` BEFORE any row is
   written is pasted: C1's "with no row" lines name EXACTLY the node's N functions (this proves the list and the mechanism),
   and C7 says "below SUBCLASS_PENDING_CEILING <before>: lower the constant to <before - N>".
4. N rows are added, sorted into place by (file, function) like the existing rows, each with `class`, `roles`, `owner`
   (and `ref` where C1 demands it); the report lists every row with a one-clause reason (section 4), and every E3 row with
   its `E3:` note. Questions (4.3) are returned, not guessed; while one is open the node is handed back with C1 red naming
   exactly the question units, is NOT committed and does not release the next node; the Lead's answers are written in a fix
   round of the same task_id, then the node commits (4.3).
5. `SUBCLASS_PENDING_CEILING` is lowered by exactly N (C7 silent = dense).
6. An intermediate C3 output (rows in, ceilings still old) is pasted; then each raised ceiling is set to its exact count;
   the commit message and the report carry the raise list: `<key>: <old> -> <new> -- census classifies subclass refusers of <files> (OH8-7x)`.
   The witness also carries the output of a reconciliation (scratchpad script, pure read, full source in the report): for
   each `blocking_per_role.<r>` and `safety`, old -> new, and the number of the node's NEW rows that name `<r>` (resp. class
   `safety`); they must be equal; every other `ratchet` key and every EXISTING row unchanged (`git diff` of the fixture shows
   only inserted rows and the ratchet lines).
7. `python -B <wt>\ai-packages\qa-factory\scripts\tests\test_judgment_census.py` is green; the totals line (with
   `subclass_pending=<after>`) is pasted.
8. `refusal_registry.py` is not in the diff (`git -C <wt> diff --stat` pasted); a grep of `ast.Raise` in `test_judgment_census.py`: no hit (positive control on `refusal_registry.py`).
9. Witness: `python -B <wt>\ai-packages\qa-factory\scripts\tests\scenario_walk.py --witness-for <the owns paths>`; every
   printed non-slow, non-quarantined file is run; slow files are named, not run. For `docs/SIBLING_MAP.md` and
   `docs/tasks/critic-diff-brief.md` (no test of their own) the doc-dispatch witness of rule 11: a key-presence script
   attached in full source, keys quoted verbatim from this DoD before the run, with one negative control (OH8-7b keys:
   `SUBCLASS_UNIT_FILES` in the axis-18 row and `OH8-7b` in the axis-34 row of `docs/SIBLING_MAP.md`; `SUBCLASS_PENDING_CEILING`
   and `SUBCLASS_UNIT_FILES` both present in `docs/tasks/critic-diff-brief.md`. OH8-7h keys: `OH8-7h` present,
   `SUBCLASS_UNIT_FILES` and `SUBCLASS_PENDING_CEILING` absent in `docs/SIBLING_MAP.md`; `SUBCLASS_PENDING_CEILING` and
   `SUBCLASS_UNIT_FILES` both absent in `docs/tasks/critic-diff-brief.md`).
10. `python -B <wt>\ai-packages\qa-factory\scripts\selftest.py --lang` passes (the fixture's `about` and the test are package text).
11. Commit message lines: `architecture: AR-29, AR-20, AR-13, AR-22, AR-28 -- <how kept, one clause each>`; `judgment: adds data check test_judgment_census.SUBCLASS_UNIT_FILES -- census rows for refusals through package subclasses in <files>, each a data check or a guard classified per unit`; the raise list (DoD 6). OH8-7b and OH8-7h add the four-question block with the full axis enumeration (1.3) and a `tier:` line; the gate refuses a tier below the Lead binding, so the builder leaves the tree STAGED and the Lead commits (rule 10).

edges (every node): section 2.2.

The per-node tests in one line: C7 dense at the lowered constant (exactly N); C1 green with the N new rows; C3 dense after the named raise.

### 3.4 OH8-7b additionally: the mechanism

1. `SUBCLASS_UNIT_FILES`, the `unit_files` keyword of `units_of` and `analyse`, and the reordering of 2.1 steps 1-2.
2. The list-form checks, reported as C7 problems inside `analyse` (E4, E5): a duplicate entry (or a function entry of a listed
   file); an entry the scan does not hold (file absent from `scan_files`, or a `file::function` with no widened site in that file).
   Texts name the entry, what was expected and the door (FR-1).
3. The C7 "above" refusal text gains the door "or list its file in SUBCLASS_UNIT_FILES with its rows (the OH8-7 chain)".
4. Tests (variant rows, no new file; `test_judgment_census.py` is a `keep` row, layer `register`):
   - `_run` gains `kw.setdefault("unit_files", ())` next to `pending_ceiling` (:602): a synthetic package lists nothing unless
     the case says so; otherwise E5 fires on every synthetic run (the real tuple names files the temp package lacks).
   - `SUBCLASS_ROWS` gains a column `unit_files` (default `()`), and `test_neg_subclass_raises_flip_blocks_or_are_pending` asserts
     "`helpers_x.py::f` is a check unit (u3)" iff `helpers_x.py` (or `helpers_x.py::f`) is in that column. New rows:
     `listed_neutral` (the `neutral_only` source, listed: unit created, pending 0); `listed_function` (same, listed as
     `helpers_x.py::f`); `listed_unrelated`, `listed_shadowed_local`, `listed_tests_only`, `listed_no_arg` (listed, still no
     unit — the E11 safe side); `listed_other_function` (listed as `helpers_x.py::g`: `f` stays pending).
   - `test_neg_pending_is_dense_and_only_shrinks_c7` gains a table (id, unit_files, expected C7 text): `twice`
     (`("helpers_x.py", "helpers_x.py")`), `file_and_function`, `stale_file` (`("gone_x.py",)`), `stale_function`
     (`("helpers_x.py::nope",)`), and `ok` (no C7 text).
5. The texts: the u3 docstring line (:22-24), the docstring blind-spot paragraph, `BLIND_SPOT` and the fixture `about` each add
   that a file listed in `SUBCLASS_UNIT_FILES` creates units from widened sites; `test_blind_spot_states_the_subclass_clause`
   adds the needle `subclass_unit_files` (its other needles stay).
6. `docs/SIBLING_MAP.md`: axis 18's member text adds `SUBCLASS_UNIT_FILES` (grow-only, its growth lowers
   `SUBCLASS_PENDING_CEILING`, removed with it by OH8-7h); axis 34's "known roads off it" row adds one line: the census's
   temporary second road (a subclass-only refuser is pending in an unlisted file), bounded by the two constants, closed by
   OH8-7b..h (spec t-346).
7. `docs/tasks/critic-diff-brief.md`: question 9's ratchet list adds `SUBCLASS_PENDING_CEILING`; question 11's list of census
   scan constants adds `SUBCLASS_PENDING_CEILING` and `SUBCLASS_UNIT_FILES` (6a F-B = (a)); nothing else in the brief changes.

### 3.5 OH8-7h additionally: the removal (one commit)

1. First the node's 21 rows with the constant lowered to 0: green (pasted).
2. Then, in the same commit: remove `SUBCLASS_UNIT_FILES`, `SUBCLASS_PENDING_CEILING`, `_c7`, the `unit_files` and
   `pending_ceiling` keywords, the `pending` / `pending_names` totals and units_of keys, the "C7" problem key,
   `test_c7_the_subclass_pending_set_is_dense_and_only_shrinks`, `test_neg_pending_is_dense_and_only_shrinks_c7` (and their
   `TESTS` entries), and the pending branch of the flip loop; both `setdefault` lines of `_run` (`pending_ceiling`,
   `unit_files`) go. Every scanned file creates units from widened sites. The `totals_line` keeps `subclass_family=` and
   drops `subclass_pending=...`.
3. `SUBCLASS_ROWS`: the `pending` and `unit_files` columns go (and the `listed_*` rows of 3.4 item 4, whose distinction no
   longer exists); each row is (id, files, blocking). The body of `test_neg_subclass_raises_flip_blocks_or_are_pending`
   becomes: for every case except `neutral_only`, the census holds `_row("helpers_x.py", "check_f")` and
   `blocking_units == blocking` (1 for the ten positive rows, 0 for the seven misses `unrelated`, `tests_only`,
   `shadowed_local`, `shadowed_import`, `no_binding`, `no_arg`, `cycle`), and C1 does not name `helpers_x.py::f`; for
   `neutral_only`, (i) with no row: C1 names "`helpers_x.py::f` is a check unit (u3)" and `blocking_units` is 0, (ii) with
   `_row("helpers_x.py", "f")`: C1 silent and `blocking_units` is 1. The `t["pending"]` / `pending_names` assertions go.
4. Texts: the u3 docstring line, the blind-spot paragraph, `BLIND_SPOT` and `about` say that a raise through a package subclass
   (resolved per file) or the attribute form is a refusal site like a literal raise; the "pending ... OH8-7b" clause goes; the
   "still unseen" list stays. `test_blind_spot_states_the_subclass_clause` asserts `subclass`, `stdlib`, `` `raise a()` `` present
   and `pending`, `oh8-7b`, `subclass_unit_files` absent.
5. `docs/SIBLING_MAP.md`: axis 18's OH8-7 clause is rewritten ("since OH8-7h the census creates units from every widened
   raise site; the temporary constants are gone", no constant names); axis 34's line added by OH8-7b is removed.
6. The grep of AR-22 (1.1): zero hits for `subclass_pending|SUBCLASS_PENDING|pending_names|SUBCLASS_UNIT_FILES` in
   `ai-packages/`, `tools/`, `PROCESS/`, `.github/`, `docs/SIBLING_MAP.md`, `docs/tasks/critic-diff-brief.md`, `CLAUDE.md`,
   `PROJECT.md`; the history carriers `docs/tasks/`, `plans/piles/` and `logs/` are excluded by name (the batch-9 file,
   journal notes, compact snapshots and pile findings hold the names); positive control: the same grep finds
   `subclass_family` in the test.
7. Before step 2 is committed, `C7`, `pending` and `SUBCLASS_PENDING_CEILING` are grepped across `tools/`, `PROCESS/`, `docs/`
   (outside specs) and `.github/` with a positive control: a reader found there is a stop and a question (none known on 0bc7b1d).
8. `docs/tasks/critic-diff-brief.md`: the names added by 3.4 item 7 are removed from the lists of questions 9 and 11.

---

## 4. How a builder classifies a function

### 4.1 The census's own definitions (quoted)

- The row (test docstring, `test_judgment_census.py:5-7`): "A row names the unit's CLASS (shape / xref / word-list /
  meaning-proxy / meaning / safety), the roles on whose path it stands, and the owner it serves (data / judgment / intent).
  Whether a unit BLOCKS is COMPUTED, never labelled".
- The class order (:29-32): "meaning > meaning-proxy > word-list > safety > xref > shape (CLASS_ORDER); the HIGHER wins.
  `safety` is a guard on the application, secrets, outside writes, a person's words or git state."
- C1's text (:318-320): "the class is a judgment about what the unit decides, never defaulted".
- The fixture `about`: "`blocks` is computed by the test, never written here; `blocks_override: false` (with a `note`) is the
  only hand mark."
- The classes (spec t-1765 §"Классы", the census's source table): `shape` — keys, types, form, presence; `xref` — cross
  references, equal counts, joins; `word-list` — a role's or person's words against a list, a closed list of closing reasons;
  `meaning-proxy` — quality by pattern (AST, a regex on meaning); `meaning` — is the case good, is the red a bug; `safety` —
  protection of the application, secrets, outside writes, a person's words, git state.
- AR-29: "a check in code judges the SHAPE of an artifact (keys, types, a form), its JOINS ... or the PRESENCE of an input, a
  witness or a person's word."

### 4.2 The procedure (per function, in this order)

1. Read the function whole, and the widened raise site(s) the intermediate run names (DoD 3).
2. Does the raise reach a role or the conductor as a refusal (the exception leaves the module, or the CLI turns it into an
   exit/refusal)? If it is caught inside the module and never refuses anyone, or guards a programming error only -> it is
   the E3 case (6a F-A = (b)), no question: the row is written WITHOUT `blocks_override`, class by the raising condition
   (steps 3-5) as for any unit, with `note: "E3: refuses nothing -- <why>; override queued
   (plans/piles/onboarding-hooks/findings/20261113-gate-form-for-blocks-override-on-non-refusing-units.md)"`; listed in the report.
3. What does the condition that raises test? In this order:
   - FIRST: does the raise protect the application, secrets, an outside write, a person's words or git state (a symlink or
     path escape, a lock or claim, a root or clone guard, trust of a producer or signature, an exclusive write)? -> question
     (4.3) with a `safety` proposal. A condition that is both a presence test and a guard is the guard (CLASS_ORDER: safety >
     shape);
   - keys, types, a form, presence of a file/field/input, a parse failure -> `shape`;
   - one record against another (an id resolves, counts match, a reference joins, a hash equals) -> `xref`;
   - anything else -> question (4.3), including any reading that touches the words or content of a role or a person.
   Two readings on one function: the higher in CLASS_ORDER wins (and if it is not shape/xref, it is a question).
4. `roles`: the roles on whose path the function stands. In order: (i) a `ref` row of `stages.json` names its stage roles
   (none of the 38 files today, E13); (ii) a function every role passes through on a hook path (as `hooklib.artifact_root`,
   fixture l.400) takes every role and `conductor`; (iii) otherwise follow the existing rows of the SAME file that sit on the
   same command (quote the row you followed in the report: e.g. `probe_by_code.py` rows are `["conductor"]` except
   `judge_record` `["qa-code-critic"]`, fixture l.618-627); (iv) otherwise `["conductor"]`. A doubt between (ii) and (iii) is a
   question: roles drive `blocking_per_role`.
5. `owner`: `data` for `shape` / `xref` (and for `safety`, as every existing safety row, e.g. fixture l.279); `judgment` only
   where the unit stands in front of a role's verdict (precedent `probe_by_code.py::judge_record`); `intent` only for a
   person's word — both of these are questions, not builder decisions.
6. The report line per row: `<file>::<function> -- <class>, <roles>, <owner> -- <one clause: what the raising condition tests>`.

### 4.3 What goes up instead of being guessed

Returned as a question, with the function's full text, the raise line(s), the builder's proposed class/roles/owner and one
clause of why it is not plain:
- any class reading other than `shape` / `xref` (a `safety` proposal included);
- a `word-list` / `meaning-proxy` / `meaning` reading (E9: stop, never committed in this chain);
- a roles doubt (4.2 step 4) or an owner other than `data`.

The questions of a node are answered by the Lead (Fable, the tier above the builder) in ONE batch per node — not by the pair
critic. A node with open questions is handed back with C1 red naming exactly the question units (DoD 4; the rest of its rows
stand), is NOT committed and does NOT release the next node; the answers are written as the rows in a fix round of the same
task_id (a continuation), then the node commits. Forecast: OH8-7e and OH8-7g are expected to carry the most questions (guards
in `import_test_receipt`, `exploration`; a person's words in `person_words`, `question_register`; assertion patterns in
`assertion_detectors`).

---

## 5. Ready-to-paste batch file (new, untaken): `plans/piles/onboarding-hooks/batch-9-perepis-podklassov-oh8-7b-h.md`

No `batch-9-*` file exists in any worktree (glob `**/onboarding-hooks/batch-9*.md` over `.claude/worktrees`: none; positive
control `batch-8*.md`: 20 hits). The «Пишет в» cells follow 6a F-Z = (b): only the two test files, plus `docs/SIBLING_MAP.md`
and `docs/tasks/critic-diff-brief.md` for b and h; the script files are named in «Что» without backticks. The card rows
(table «Пачки» and «Содержание» of `README.md`) are the coordinator's move in the same commit (D-0044); the chain's carrier is
this spec (the gate-form finding of 6a F-A is a separate finding with its own batch row).

```markdown
# Онбординг, установка, хуки и гард — пачка 9: перепись суждений классифицирует 190 функций, отказывающих только через подкласс (OH8-7b…h)

кучка: `onboarding-hooks` | статус: ожидает | взял: — | ветка: `pile/onboarding-hooks/batch-9` | MR: — | стенд: не нужен (CI) | приоритет: П3

Открыта 13.11.2026 (спека `docs/tasks/specs/t-346-oh8-7b-chain-spec.md`; решения Lead F1 (a), F3, F4 от 13.11.2026): хвост узла OH8-7 (t-321 часть B, вариант (d)+(c1)) — 190 функций в «pending» под `SUBCLASS_PENDING_CEILING`.

Правило готовности: пачка закрыта, когда каждый узел «принято», свидетели узлов — в журнале взявшего.

Решения владельца: нет (решения Lead 13.11.2026; развилки спеки t-346 §6 — у Lead).
Порядок: узлы строго один за другим (каждый переписывает `judgment-census.json`); критик — один проход на пару (b+c, d+e, f+g), OH8-7h — свой проход. Узел начинает с перезамера (спека §3.2) и останавливается вопросом при расхождении. OH8-7b и OH8-7h — коммиты механизма: коммитит Lead (строка `tier:`).
очередь: onboarding-hooks/8 → onboarding-hooks/9
Скоуп свидетеля: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <пути узла>`; BATCH CANON — CI интегратора.

## Бриф

Что сделать: семь узлов по спеке t-346 — каждый добавляет свои файлы в `SUBCLASS_UNIT_FILES`, пишет строки переписи по каждой функции (класс, роли, владелец), опускает `SUBCLASS_PENDING_CEILING` ровно на своё число и называет каждый подъём храповика построчно; OH8-7h убирает обе константы. НЕ делать: править скрипты пакета (они только читаются), `refusal_registry.py`, `tools/architecture_gate.py`, `MEANING_CEILING`; понижать класс или добавлять `blocks_override` существующим строкам; угадывать класс вне `shape`/`xref` — это вопрос (спека §4.3).

## Узлы

Исполнитель «builder → critic» — кодовый узел по готовой спеке. Статусы: `ожидает` → `в работе` → `сдано` → `принято` / `отклонено`.

| Узел | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Статус |
|---|---|---|---|---|---|---|
| OH8-7b | П3 | Механизм `SUBCLASS_UNIT_FILES` (спека t-346 §2, §3.4) + первые 23 функции scripts/probe_by_code.py (строки 217–2902, записями `файл::функция`; скрипт только читается). Потолок 190 → 167. Тест: строки `SUBCLASS_ROWS` со столбцом `unit_files`, таблица C7 (дубль, устаревшая запись); C1/C7/C3 зелёные. Списки вопросов 9 и 11 брифа критика получают обе константы. Коммит механизма — Lead | builder → critic (пара 1) | `scripts/tests/test_judgment_census.py`, `scripts/tests/fixtures/judgment-census.json`, `docs/SIBLING_MAP.md` (оси 18, 34), `docs/tasks/critic-diff-brief.md` (вопросы 9, 11) | OH8-7 | ожидает |
| OH8-7c | П3 | Остальные 23 функции scripts/probe_by_code.py (строки 3738–8309; скрипт только читается); 23 записи заменяются записью файла. Потолок 167 → 144. Тест: C1/C7/C3 | builder → critic (пара 1) | `scripts/tests/test_judgment_census.py`, `scripts/tests/fixtures/judgment-census.json` | OH8-7b | ожидает |
| OH8-7d | П3 | 38 функций (скрипты только читаются): execution_request (14), environment_preparation (10), execution_scheduler (4), managed_dependency (1), run_suite (3), red_sandbox (6). Потолок 144 → 106. Тест: C1/C7/C3 | builder → critic (пара 2) | `scripts/tests/test_judgment_census.py`, `scripts/tests/fixtures/judgment-census.json` | OH8-7c | ожидает |
| OH8-7e | П3 | 32 функции (скрипты только читаются): exploration (11), explore_step (1), manual_evidence (3), manual_capture (2), import_test_receipt (7), s7_reorder (8). Потолок 106 → 74. Тест: C1/C7/C3 | builder → critic (пара 2) | `scripts/tests/test_judgment_census.py`, `scripts/tests/fixtures/judgment-census.json` | OH8-7d | ожидает |
| OH8-7f | П3 | 24 функции (скрипты только читаются): ticket_light (7), ticket_adapter (1), source_inventory (2), source_exclusions (2), vcs_evidence (4), local_keys (2), onboard_apply (6). Потолок 74 → 50. Тест: C1/C7/C3 | builder → critic (пара 3) | `scripts/tests/test_judgment_census.py`, `scripts/tests/fixtures/judgment-census.json` | OH8-7e | ожидает |
| OH8-7g | П3 | 29 функций (скрипты только читаются): s5_plan (6), question_register (6), question_stop (3), person_words (2), grammar (3), assertion_detectors (5), machine_facts (3), driver_dispatch (1). Потолок 50 → 21. Тест: C1/C7/C3 | builder → critic (пара 3) | `scripts/tests/test_judgment_census.py`, `scripts/tests/fixtures/judgment-census.json` | OH8-7f | ожидает |
| OH8-7h | П3 | 21 функция (скрипты только читаются): hooklib (4), controller (1), story_step (1), event_store (2), retro_numbers (1), host_adapter (1), role_load (6), release_fingerprint (2), selftest (2), config_view (1); потолок 21 → 0, затем тем же коммитом удаляются `SUBCLASS_UNIT_FILES`, `SUBCLASS_PENDING_CEILING`, C7 и ветка pending; тексты слепого пятна, `about`, оси 18/34 и списки вопросов 9/11 брифа критика переписаны (спека §3.5). Коммит механизма — Lead. Тест: C1/C3 зелёные, `neutral_only` создаёт единицу | builder → critic (свой проход) | `scripts/tests/test_judgment_census.py`, `scripts/tests/fixtures/judgment-census.json`, `docs/SIBLING_MAP.md` (оси 18, 34), `docs/tasks/critic-diff-brief.md` (вопросы 9, 11) | OH8-7g | ожидает |

## Ход

Журнал передачи Lead пачки, новые записи в конец: `<дата время> — <что сделано, диспатчи t-nnn, хэши>`.

- 13.11 — пачка открыта по спеке t-346 (D-0044); не взята

## Живые доказательства

| Что | Стенд / проект | Кто | Статус |
|---|---|---|---|

## Остатки

<!--
Пачка закрывается доделкой, не переносом (слово владельца 08.10.2026): `close` отказывает, пока в этом разделе есть
пункт, у которого нет одной из двух форм (ключи в нижнем регистре, пары `ключ: значение` через ` | `, текст впереди):
  - <что осталось> | сделано: <хэш 7-40 hex | t-nnn>
  - <что осталось> | перенос: <findings/<файл> | пачка N | <кучка>/findings/<файл>> | обоснование: <почему> | подтвердил: <кто, дата>
Пустой раздел — можно закрывать.
-->
```

Notes for the coordinator (not part of the paste): «Живые доказательства» is empty on purpose — no role behaviour changes
(FR-33 does not apply to a test-only change). The `docs/SIBLING_MAP.md` and `docs/tasks/critic-diff-brief.md` cells of b and h
put shared docs into the zone; the `(оси 18, 34)` / `(вопросы 9, 11)` texts are prose, the backticked path is a whole-file claim
(6a F-Z = (b) accepted this).

---

## 6. Forks (returned; none decided)

**F-P (blocking for OH8-7b/c). Per-file listing vs. the split of `probe_by_code.py`.** F1 lists FILES, and F3 lets
`probe_by_code.py` take two function-disjoint nodes. Listing `probe_by_code.py` in OH8-7b would create units for all 46
functions at once, so OH8-7b would owe 46 rows (outside 20-40), and OH8-7c would have nothing.
- (a) Entries may also be `file.py::function` (2.1); used only for `probe_by_code.py` in OH8-7b; OH8-7c replaces the 23
  entries with the file entry. Cost: one more match form, two more C7 list-form rows (`file_and_function`, `stale_function`),
  gone at OH8-7h.
- (b) One node of 46 for `probe_by_code.py` (outside F3's 20-40); the chain becomes six nodes (b..g), pairs re-cut.
- (c) OH8-7b lists `probe_by_code.py` and writes 46 rows; OH8-7c takes another group (re-cut of the table).
- Recommendation: (a). The node table and section 5 are written on it.

**F-A (blocking only when an E3 function appears). The commit gate cannot take a `blocks_override` truthfully.** The census
convention (decided, E3) writes a non-refusing unit with `blocks_override: false` + `note`. Each such row raises
`ratchet.blocks_overrides` (10 today), and `tools/architecture_gate.py` item 7 (v) accepts a raise of `blocks_overrides` only
with `judgment: moves <what> to code` (docstring :51-53, `WEAK_KEYS` :102-103) — a false line for a classification.
- (a) A new gate form for an override raise (e.g. `judgment: overrides <unit> -- <why>`): a `tools/` mechanism change (rule
  10) as its own node before the first node that needs it.
- (b) The row is written WITHOUT the override (counted as blocking: the error falls on the safe side, `blocking_per_role` is
  over-counted, which the gate accepts with `adds data check`); the reason goes into the report and a finding queues the
  override for after (a).
- (c) The node stops on every such function (as E9) and the Lead decides each.
- Recommendation: (b) for this chain plus a finding for (a): no gate edit inside the chain, the count errs toward extra
  blocking, and the override decision is made once for the class. Until answered, the builder returns E3 functions as
  questions (4.3).

**F-Z. The zones of section 5.** The Lead's instruction puts each node's script files in «Пишет в». The nodes only READ them;
`piles.py check (б)` reads every backticked path of that cell as a write claim, so batch-9 «в работе» would lock 38 files,
among them the hot `hooklib.py`, `controller.py`, `story_step.py`, `selftest.py`, `event_store.py`, `driver_dispatch.py`,
against every other batch (and `take` is already blocked by the broad zones of `onboarding-forge/1,2`, t-337 §3).
- (a) As instructed (section 5 as pasted).
- (b) «Пишет в» holds only the two test files (and `docs/SIBLING_MAP.md` for b/h); the script files are named in «Что»
  without backticks. Drift in a script is caught by the re-measure step (3.2) and by C1/C7 for whoever merges second (E7, E8).
- Recommendation: (b). Cost of (b): a concurrent edit of a listed script by another batch is not prevented, only detected
  (step 0 stop or a red C1 for the later merge).

**F-B. Critic question 11 does not list the chain's constants.** `docs/tasks/critic-diff-brief.md` question 11 lists the census
test's scan constants a critic must read (`SCAN_ROOT`, `SCAN_EXCLUDE`, `BLOCKING_ENTRY_FILES`, `UNIT_NAME_RE`, `JUDGE_CALLS`,
`MEANING_CEILING`), but neither `SUBCLASS_PENDING_CEILING` (OH8-7) nor `SUBCLASS_UNIT_FILES` (this chain). An edit of either
changes what is counted.
- (a) OH8-7b adds both names to that list (owns + `docs/tasks/critic-diff-brief.md`); OH8-7h removes them.
- (b) No edit: the pair critics read every edit of the constants anyway; the residual is named in the four-question block.
- Recommendation: (a) (the brief is the carrier of the review duty, axis 32; a one-line edit). Note: CLAUDE.md rule 10 says
  that paragraph, question 11 and designer rule 1 change together (axis 1); the paragraph names no constant, so (a) changes
  only question 11.

**F-D. Acceptance timing inside a pair.** Under F4 the critic reads b and c together, so OH8-7c is built on OH8-7b's committed
but not yet accepted tip.
- (a) Dispatch c on b's committed tip right after b's builder self-run (DoD green) and the Lead's mechanism commit; accept both
  at the pair verdict; a defect in b is fixed on top (E15).
- (b) Hold c until a critic reads b alone (contradicts F4's pairs for pair 1).
- Recommendation: (a), with the pair critic's dispatch asking for the mechanism (b's §3.4) FIRST in its verdict.

### 6a. Lead decisions on the forks (Fable, 2026-11-13; technical, "решила сама", on the owner's morning list)

- **F-P = (a).** `file.py::function` entries, used only for `probe_by_code.py` in OH8-7b; OH8-7c replaces them with the file entry.
- **F-A = (b).** A non-refusing unit gets its row WITHOUT `blocks_override` in this chain (the count errs toward extra
  blocking); the builder lists every such function in its report, and one finding queues the gate form for an override
  raise. No gate edit inside the chain. The builder does not return these as questions: (b) is the answer. The finding's
  carrier is `plans/piles/onboarding-hooks/findings/20261113-gate-form-for-blocks-override-on-non-refusing-units.md`; the
  Lead creates that file and its batch row (D-0044) before the first dispatch of the chain. The E3 `note`s point to this path (E3).
- **F-Z = (b).** «Пишет в» holds only the two test files (plus `docs/SIBLING_MAP.md` and `docs/tasks/critic-diff-brief.md`
  for b and h); scripts are named in «Что» without backticks. Section 5 is re-cut to this before it is pasted.
- **F-B = (a).** OH8-7b adds both constants to critic question 11; OH8-7h removes them. Question 9's list gets
  `SUBCLASS_PENDING_CEILING` in the same edit (the analog of section 8).
- **F-D = (a).** c is dispatched on b's committed tip; the pair critic answers the mechanism first. The questions of a node are
  answered by the Lead in one batch per node (4.3); a node with open questions is not committed and does not release the next
  node; the answers land in a fix round of the same task_id. Forecast: OH8-7e and OH8-7g carry the most questions.
- C-1..C-8 stand.

A critic reads this plan before any builder (rule 3: a spec with forks and a census mechanism): t-353.

---

## 7. Small technical choices closed by the designer

- C-1: a created unit's `via` label is `u3`, the same as a literal-site unit (one road; the end state has no other label).
- C-2: the list-form checks report under C7 (the subclass machinery's problem key), not under a new key, so OH8-7h removes
  them with C7.
- C-3: after OH8-7h, `totals["sites"]` counts the widened sites (the census's sites); the totals line keeps the name.
- C-4: a whole-file entry whose file has no widened-only function is not red (it creates nothing; the tuple is temporary).
- C-5: the split of `probe_by_code.py` is by source order (lines 217-2902 / 3738-8309), so each half is a contiguous reading
  for the builder and the critic; all `__init__` methods fall in the first half.
- C-6: the `judgment:` unit token for c..g is `test_judgment_census.SUBCLASS_UNIT_FILES` (the gate's `ADDS_RE` needs one
  non-empty unit; one token for the node's 21-38 rows).
- C-7: OH8-7b records the temporary road on axis 34 ("known roads off it"), because the Lead's decision has OH8-7h update the
  axis-34 row and the row holds no OH8-7 text today (grep `OH8-7` in `docs/SIBLING_MAP.md` on 0bc7b1d: only the axis-18 line 390).
- C-8: rows are inserted sorted by (file, function), as the fixture is.

## 8. Contradictions and analogs noticed (reported, not widened)

- OH8-7 itself did not record its second road on axis 34 (only axis 18 mentions "axis 34" in parentheses); C-7 closes it
  inside this chain.
- `docs/tasks/critic-diff-brief.md` question 9's ratchet list does not name `SUBCLASS_PENDING_CEILING` either (its header names
  the census `ratchet`); same class as F-B — closed by 6a F-B and carried into 3.4 item 7.
- t-321 §B.6 DoD 7 asked the builder for a mutation run; `plans/builder-rules.md` 7b now says builders do not run mutations.
  The DoDs here follow 7b.
- The t-337 draft's edge "a function that turns out not to refuse gets no row" is impossible under F1 (a): a listed file's
  widened site IS a unit, and C1 demands its row; E3 replaces it.
- `tools/architecture_gate.py`'s `blocks_overrides` rule (F-A) will meet any future node that adds an honest override, not only
  this chain.
- The expected raise has a measured lower bound: every created unit blocks by construction (critic t-353 key 3: its own
  widened site flips it, :285-286), so the sum of per-role raises over the chain is >= 190; `blocking_per_role.conductor`
  rises from 491 by up to ~190 if most rows name only `conductor` (that split is an estimate, not measured); other roles rise
  where rows name them.

## 9. Reading trail

All under `C:\QAFactory\forge-repo\.claude\worktrees\oh8-7\` unless absolute.
- `C:\QAFactory\forge-repo\docs\tasks\specs\t-337-oh8-7b-nodes-draft.md` (whole).
- `C:\QAFactory\forge-repo\docs\tasks\specs\t-321-oh8-1-oh8-7-specs.md` :157-486 (part B, Lead decisions, critic t-326 fixes, forks, choices, analogs).
- `...\scratchpad\oh8-7-pending.txt` (whole, 190 lines; per-file counts recounted against t-337 §1: all equal).
- `ai-packages/qa-factory/scripts/tests/test_judgment_census.py` :1-898 (whole).
- `ai-packages/qa-factory/scripts/refusal_registry.py` :1040-1225 (`_key_text`, `_raised_here`, `_refusal_calls`, `_module_file`, `_file_bindings`, `raise_family`, `sites`).
- `ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json` :1-40; greps `blocks_override` (l.28, 95, 386-388, 730), `<script>` (l.78), rows of `probe_by_code` / `execution_request` / `hooklib` / `question_register`.
- `ai-packages/qa-factory/scripts/probe_by_code.py`: grep of every `def` / `class` (line numbers of the 46 names).
- `ai-packages/qa-factory/references/stages.json`: grep of the 38 file names (none) with positive control `\w+\.py` (11).
- `ai-packages/qa-factory/design/architecture.md` :134-157 (AR-29), :159-166 (AR-13), :210-222 (AR-20), :233-238 (AR-22), :275-280 (AR-28).
- `docs/SIBLING_MAP.md`: all `## Axis` headings (36; read-main also 36), axis 18 :386-396, axes 32-34 :557-593; grep `OH8-7`.
- `docs/tasks/critic-diff-brief.md` :59-72 (questions 9-11).
- `docs/tasks/specs/t-1765-thinking-roles.md` :156-169 (the class table).
- `tools/architecture_gate.py` :20-104 (item 7 (v), `WEAK_KEYS`); grep `blocks_overrides|moves|adds data check`.
- `plans/builder-rules.md` :10-34 (7, 7b).
- `C:\QAFactory\forge-repo\.claude\worktrees\read-main\plans\piles\onboarding-hooks\batch-8-ostatki-t-282-t-254-t-287.md` (whole, the form); glob of batch files; glob `batch-9*` over all worktrees (none; control `batch-8*`: 20).
- `C:\QAFactory\forge-repo\.claude\worktrees\read-main\tools\piles.py` :36-75 (zones, «Пишет в», D-0048 lists).
- Grep `subclass_pending|SUBCLASS_PENDING|pending_names` over the oh8-7 tree: 3 files (test, fixture, SIBLING_MAP).
- t-360 fix round: `C:\QAFactory\forge-repo\docs\tasks\specs\reviews\t-353-oh8-7b-chain-plan-review.md` (whole); `test_judgment_census.py` :215-299 (`units_of`, return keys `units`/`pending`/`files`), :590-650 (`_run` :600-606), :760-840 (`SUBCLASS_ROWS`, the two subclass tests).

Needed beyond the manifest: `tools/architecture_gate.py`, `docs/tasks/specs/t-1765-thinking-roles.md`, `plans/builder-rules.md`, `tools/piles.py`, `references/stages.json`, `scripts/probe_by_code.py` (reads only).

## 10. Fix round t-360

Folds critic t-353 (fit_with_fixes) into the body; no 6a decision reopened; node lists of 3.1 untouched (23/23/38/32/24/29/21 = 190).
- B1: E3 cell and 4.2 step 2 rewritten to F-A (b) with the `E3:` note; 4.3 bullet "E3 until F-A" deleted; section 5 re-cut to F-Z (b) (brief added to b/h cells); 3.3 owns brief unconditional; 3.4 item 7, 3.5 item 8; DoD 9 brief keys; 1.3 axis 1 covered.
- B2: 4.3 closing paragraph and 6a F-D: the Lead answers a node's questions in one batch; an open-question node is not committed and does not release the next; fix round of the same task_id; forecast e/g. DoD 4 aligned.
- B3: DoD 6 reconciliation witness; E10 "all created units block by construction"; 1.1 AR-20 row names it.
- B4: 3.4 item 4 `_run` setdefault `unit_files`; 3.5 item 2 both setdefault lines go.
- B5: 3.2 script takes the remaining-nodes list and `--last`; three stops (a)/(b)/(c); non-0/2 exit is a stop; 3.1 list-saving line updated.
- B6: 4.2 step 3 tests the guard (safety) first. B7: 3.5 item 6 grep scoped by named carriers.
- N1: 3.5 item 3 post-removal test body. N2: 1.1 AR-22 control wording. N3: §8 measured lower bound. N4: 6a F-A carrier path.
Deviations:
- B2: the critic's alternative "or ONE critic question-pass per node" is not carried — the Lead's B2 decision names the Lead only.
- B5: the review cites scratchpad `t353_sim.py`, which was not in the manifest; the 3.2 script is rebuilt from review keys 3 and 7 against `units_of` :276-292 (not run by the designer).
- N4: the batch number of the finding's row is not named — the Lead creates file and row (D-0044); section 6 forks are left as the historical record.
