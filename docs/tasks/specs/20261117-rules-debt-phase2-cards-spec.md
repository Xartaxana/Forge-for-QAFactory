# Rules-debt phase 2 — dispatch cards (t-954, F19)

Designer draft for the Lead. Parent spec: `docs/tasks/specs/20261117-rules-debt-fix-spec.md` (accepted, t-924; called
"the spec" below). Owner forks F-O1..F-O6 are decided (the spec's three closing sections, :614-655); Lead forks
F-L1..F-L13 are taken as recommended (brief). S7 and S8 are at builders and are not carded here. Owns are
repo-relative; in a worktree dispatch the Lead substitutes the worktree root. Every load-bearing fact below carries the
path:line read today (17.11.2026) in the root checkout (branch head `ebb0593e`, which carries the phase 1 merge
`b516f786`); where a fact was not established the line says so and gives the command.

## §0. Three facts that change the cards (read before dispatch)

1. **The one predicate the spec names for FR-59 conversions does not exist.** The spec (§2 G-rows, §3 "FR-59 conversion
   nodes") and the debt file say "conversion owed (T2, `gate_template.acceptable`)". `gate_registry.py:837-841` requires
   a converted row's `accept` site to call a function named exactly `acceptable` (`_scan_tree` records any call whose
   name or attribute is `acceptable`, :234-237), else finding F-b. A grep for `def acceptable` over
   `ai-packages/qa-factory/scripts/*.py` finds only `profile_contract.py:895 def acceptable_provenance(` (same call
   shape, so the positive control is that very hit); no `gate_template.py` exists (Glob, 0 hits; the same Glob form finds
   other scripts). No converted row of the registry has an `accept` site today (rows read whole,
   `references/gate-registry.json:1-717`): every conversion so far was done by the note's second clause ("its unknown
   branch is pinned by `test`", :3) with sites in produce/validate/dispatch roles (precedent `finish_exit_gate`, :596
   "Registered as a validate site because the site compares no verdict word and calls no acceptable()"). → fork F-D1.
2. **The bug-file home has a writer-side reader the critic did not list.** `external_writes.py:653`
   (`process_bug_proposal`) resolves a proposal's `bug_file` as `state_dir() / bug_file_rel`, and `record_result`
   (:858) does the same at :893-901. `common-rules.md:116` is exactly the frame rule for that field ("`bug_file` …
   the state directory, `<project>/qa-factory/` — `bugs/BUG-1.md` is `<project>/qa-factory/bugs/BUG-1.md`"). The
   reporter writes `<task root>/bugs/BUG-n.md` (`agents/qa-bug-reporter.md:57`). So aligning :116 to the task root without
   touching `external_writes.py` makes every jira-channel proposal REJECT "bug_file not found" (the refusal text is pinned
   whole at `tests/test_external_writes_bug_refusals.py:125`). Whether that already happens on a live story was not
   established by a run (reading only). Also writer-side: `references/stages.json:293` (S8 output `project:bugs/`),
   `:367` (the reporter's witness `project:bugs/`), `references/artifact-writers.json:276`; `exit_gate._output_path`
   resolves `project:` names against `project_root()` (`exit_gate.py:762-763`). → forks D-1, D-2.
3. **Most named tests are SLOW or quarantined.** `scripts/slow_tests.json` lists `test_bug_records.py` (41.5 s, :15),
   `test_check_delivery.py` (:17), `test_execution_request.py` (:36), `test_gate_preflight.py` (:41),
   `test_gate_registry.py` (:42), `test_node_ids.py` (:73), `test_probe_by_code.py` (:78), `test_probe_gap_word.py`
   (:83), `test_proof_level.py` (:86), `test_s5_precheck.py` (:112), `test_stand_identity.py` (:126),
   `test_window_record.py` (:152); `builder-rules.md:53-55` forbids the builder to run them (and `test_controller_*`):
   "judged by the batch canon". Quarantined (section `quarantine` starts `test-layers.json:7174`):
   `test_judge_results.py` (:8655), `test_form_selftest.py` (:8302), `test_s1_s2_contract.py` (:9699, the spec's S1 DoD
   names it as a reader — it is not run), `test_bug_filing.py` (:7364). Every DoD below therefore is
   `scenario_walk.py --witness-for <owns>` + the printed files that are neither slow nor quarantined + the named fast
   CLIs; the slow ones are named "judged by the batch canon".

## §1. Architecture, rules, owners (designer rule 1; package spec)

FR sections by card: C1 B/C/D/E/G; C2 A/G; C3-* A/C/D/E/F; C4 C/D/G; S1b (doc) G (FR-30); S9 A/B/D; S10 A/C/G;
F-L1 D; F-L2 E; F-L4 A/C; F-L9 C/A.

AR-n touched and the change check each DoD carries (text from `design/architecture.md` as quoted by the spec §1, where
the spec already quotes it; a card quotes only what it needs): AR-1, AR-9, AR-13, AR-14, AR-18, AR-20, AR-22, AR-23,
AR-24, AR-25, AR-28, AR-29.

Checks added or altered (AR-29: owner and census class). Census classes are those of
`scripts/tests/fixtures/judgment-census.json`; a row whose class the builder cannot read from the census test returns a
question (spec S6 E1 precedent).

| check | card | owner | census class | blocking |
|---|---|---|---|---|
| `judge_results.run_bugs` duplicate input set (task root + project home [+ other stories, F-D3]) | C1 | data (which files are read); the duplicate verdict stays the judge's, advisory | none (advisory hint, `judge_results.py:18`) | no |
| `external_writes` `bug_file` resolution (task root, then state dir) | C1 on D-1 (ii) | data | shape | refuses a missing file, as today |
| door families executed (test only) | C2 | data | none | no |
| each FR-59 gate's unknown branch (row `status` -> `converted`) | C3-* | data (the record's presence/class); `live_check_demand`'s "probe owed?" is judgment of `role:qa-code-critic`, accepted at window acceptance | shape (unchanged), except C3-b `live_check_demand`: xref -> the critic's answer is read as presence of a typed answer | yes where the registry declares wait/refuse |
| `s5_stand_limits` unmeasured -> card; record cover | C3-j | intent (the person's word, P13) for the answer; data for the cover lookup | xref (a key join, as `environment_property_cover`) | yes (waits at the declared place) |
| no-row probe road reaches acceptance (test only) | C4 | data | none | no |
| window gate reading a person's word for a `review` gap | S9 | intent | xref | lifts a block |
| read heads / reader commands from data | S10 | data | safety | refuses, as today |

Commit lines: every package commit carries `architecture:` and `judgment:` in the form `tools/architecture_gate.py`
accepts (the only carrier of that grammar; not copied here). Each card gives the CONTENT; `judgment: none` always has its
` -- <why>`.

## §2. Cards

Card ids: C1 (item 1), C2 (item 2), C3-0 … C3-k (item 3), C4 (item 4), C5 (item 5), S9, S10, FL1, FL2, FL4, FL9
(item 6), S1b (item 7).

---

### C1 — bug file homes: writer <-> readers (F-O6 (a) follow-up; critic F8 + §0.2)

Dispatchable now on the recommendations of D-1 and D-3 (both returned below); not touching D-2's carriers.

given: `ai-packages/qa-factory/design/factory-rules.md` (whole), `plans/builder-rules.md`, `docs/TESTING.md`; this card;
`docs/tasks/specs/reviews/t-942-rules-debt-phase1.md` (F8); read: `agents/qa-bug-reporter.md:57`,
`scripts/bug_records.py:1-170`, `scripts/judge_results.py:1-30,265-362`, `scripts/external_writes.py:640-660,858-910`,
`scripts/contract_slices.py:1-45`
owns:
- `ai-packages/qa-factory/scripts/bug_records.py` (module docstring :10-18; one new public function next to `_project_home` :130)
- `ai-packages/qa-factory/scripts/judge_results.py` (`_project_bugs_dir` :273-278 removed, `run_bugs` :327-341, docstring :16)
- `ai-packages/qa-factory/scripts/external_writes.py` (`process_bug_proposal` :653, `record_result` :893-901, docstring :46) — only on D-1 (ii)
- `ai-packages/qa-factory/references/common-rules.md` (the :116 table row only)
- `ai-packages/qa-factory/references/slices/*/common-rules.md` (regenerated by `contract_slices.py --write`, never hand-edited; 10 of the 12 slice files carry the line — Grep `<project>/qa-factory/bugs/BUG-1.md` over `references/slices`)
- `ai-packages/qa-factory/references/external-writes.md` (:44, and :49 only if D-1 (i))
- `ai-packages/qa-factory/references/templates/test-report.md` (:35)
- `ai-packages/qa-factory/scripts/form_selftest.py` (`PTR_OK` :245)
- `ai-packages/qa-factory/scripts/tests/test_bug_records.py` (one table row), `ai-packages/qa-factory/scripts/tests/test_external_writes_bug_refusals.py` (one row, D-1 (ii))
non-goals: `stages.json`, `artifact-writers.json`, `collect-sets.json`, `install-paths.json`, `exit_gate._output_path`
(fork D-2); `agents/qa-bug-reporter.md` (already says the task root); `driver_stage_s8s9.py` (S4, merged);
`factory_dashboard.py` (reads both homes, spec §3 S4 siblings); `docs/SIBLING_MAP.md` (Lead's commit, text below);
`test_judge_results.py` / `test_form_selftest.py` (quarantined: not run, not edited)
handoff: report path given by the Lead
edges: E1-E8 below
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <every owns path>`; then run the
printed files that are not in `scripts/slow_tests.json` and not in the quarantine — at least
`python -B ai-packages/qa-factory/scripts/tests/test_external_writes_bug_refusals.py` (keep, table) and
`python -B ai-packages/qa-factory/scripts/contract_slices.py --check` (exit 0 after `--write`);
`test_bug_records.py` (slow) is judged by the batch canon, named in the report
siblings: the class "home of a bug file" — sites listed in §0.2 and owns; D-2 carriers (stages.json :293/:367,
artifact-writers.json :276, collect-sets.json :56-57 E5/E6, install-paths.json :40) are queued by fork D-2, not swept
here; `bug_records.py:1253` and `delivery_summary.py:94` compare `bug_file` by NAME only (`Path(...).name`) — not
applicable (home-independent), builder confirms by reading.

Items (test place / expected from per item):
1. `bug_records`: a public function (name builder's choice, e.g. `filed_bug_paths(task_root)`) returning the BUG files a
   duplicate check compares against, in this order: this story's `<task root>/bugs/` then the project home
   `<project>/qa-factory/bugs/` (through `_project_home`, :130), then — on D-3 (a) — every OTHER story's
   `<artifact root>/<T>/bugs/`; each home listed with `_listing(dir, BUG_GLOB)` (:140, `BUG_GLOB = "*BUG-*.md"` :46);
   a path met twice (resolved) is returned once. test: one row in `test_bug_records.py`'s existing table — a world with
   task-root `BUG-1.md`, home `BUG-1.md` and `BUG-2.md`, another story's `BUG-1.md`, and one empty world. expected from:
   the owner's word F-O6 (a) (spec :616-617: "the reporter writes under the task root, the project home is read for older
   bugs") and critic F8 (t-942 :64-66).
2. `judge_results.run_bugs` takes `existing` from item 1 (AR-13: the reader of the bug folders is `bug_records`); delete
   `_project_bugs_dir`; each duplicate entry keeps `"bug": <stem>` and ADDS `"file": <path relative to the state dir>`
   (two homes can each hold `BUG-1`); the module docstring :16 says "the story's own `bugs/`, the project's
   `qa-factory/bugs/`" [+ other stories]. test: none of its own — `test_judge_results.py` is quarantined; report line "no
   keep row drives run_bugs; the read is covered by the item-1 row". expected from: as item 1.
3. `common-rules.md:116`: split the row. `bug_file` is relative to the story's task root (`<project>/qa-factory/artifacts/<T>/`
   — `bugs/BUG-1.md` is `<task root>/bugs/BUG-1.md`; an older bug that exists only in the project home still resolves
   there); `case_file` and other artifact paths keep the state-directory frame. Then
   `python -B ai-packages/qa-factory/scripts/contract_slices.py --write` (if it needs the package as cwd: a Bash
   `( cd <worktree>/ai-packages/qa-factory && python -B scripts/contract_slices.py --write )` subshell). test: the
   slices' `--check` (generator's own ratchet). expected from: F-O6 (a); D-1 (ii).
4. On D-1 (ii): `external_writes` resolves `bug_file` through one module helper used at :653 and :901: the proposal's
   own task root first (the proposal lies at `<task root>/work/proposals/<file>`, external-writes.md:48), then
   `state_dir()`; absent in both -> the existing REJECT text unchanged. test: one row in
   `test_external_writes_bug_refusals.py` (a proposal `bug_file: bugs/BUG-1.md` with the file only under the task root
   -> no REJECT), red before the change. expected from: F-O6 (a) + the frame rule of item 3 (one frame per field).
5. `external-writes.md:44`: "a bug always gets `bugs/BUG-n.md` in the story's own folder (`<task root>/bugs/`)
   regardless of channel"; `templates/test-report.md:35` and `form_selftest.py:245`: "BUG-n — a bug file in the story's
   `bugs/` folder" — the SAME words in both (the second is a copy of the first). test: none (role/template text; FR-37
   is judged by reading; TESTING.md "пин текста роли" is not written). expected from: F-O6 (a).
6. `bug_records.py:10-18` docstring: the home the reporter writes is the story's `bugs/` (owner, 17.11.2026, F-O6 (a));
   the project's `qa-factory/bugs/` is read for bugs filed before OH5-9, with the `gate_b_decision_id` rule unchanged.
   test: none (docstring). expected from: F-O6 (a).

For the Lead's commit (not the builder's): `docs/SIBLING_MAP.md` new **Axis 38 — bug file homes: writer <-> readers**
(the last axis today is 37, `SIBLING_MAP.md:628`; "Keeping the map up to date" starts :641). Text: "The writer
(`qa-bug-reporter`, `<task root>/bugs/BUG-n.md`, charter `agents/qa-bug-reporter.md:57`) <-> the frame rule
(`references/common-rules.md` 'What a path is relative to' + its slices) <-> the readers that list or resolve a bug
file (`bug_records.story_bugs` and the dedup list of C1, `judge_results.run_bugs`, `external_writes` `bug_file`,
`factory_dashboard` task view, `exit_gate` witness through `stages.json` `project:bugs/`, `collect-sets.json` E5/E6,
`install-paths.json`) <-> the texts a person or role reads (`external-writes.md`, `templates/test-report.md` and its
`form_selftest.py` copy). A change to where the reporter writes changes every reader in one commit (AR-22)."

architecture: `AR-13 -- the bug folders are read only through bug_records`; `AR-22 -- the bug_file frame has one
producer rule and its readers move with it`; `judgment: none -- which files a path read lists; the duplicate decision
stays the judge's advisory answer`.

Edges:
- E1 (empty): no bug folder in any home -> `[]` and `run_bugs` sends no duplicate pairs (today: `existing = []` when the
  dir is absent, :328). INVARIANT: an absent folder is never an error and never a guess.
- E2 (unreadable): a home that cannot be listed (`_listing` returns its error text, :155-156) is NAMED in the judge's
  report (`problems` or the status reason), never read as empty. INVARIANT: FR-59 — an unread home is not "no bugs".
- E3 (limit): `MAX_BUG_PAIRS` (existing cap in `run_bugs`, :337) is unchanged; with more homes the pairs past the cap are
  dropped in the order of item 1 (this story first), and the report's existing counters stay. INVARIANT: the cap bounds
  spend; it never drops the current story's own bugs before others'.
- E4 (conflict: same name in two homes): both are compared; `"file"` tells them apart. INVARIANT: no entry is merged or
  hidden by a name clash (bug_records docstring :6-8 class).
- E5 TEMPORAL: proposals written before C1 carry state-dir-relative `bug_file` values (e.g. `artifacts/<T>/bugs/BUG-1.md`
  or `bugs/BUG-1.md` for a home bug); after C1 they still resolve through the state-dir fallback. INVARIANT: no executed or
  pending proposal becomes unresolvable.
- E6 POSITIONAL: the task root is tried BEFORE the state dir; INVARIANT: a project-home file of another story with the
  same name never shadows this story's own bug (the task root wins), and a file absent from both is still refused with
  the unchanged T6 text.
- E7 (conflict D-1 vs D-2): if the Lead takes D-2 (b) (stages.json to `bugs/`), that node runs AFTER C1 and C1's frame
  stays; C1 never edits stages.json.
- E8: FR-30 — package text English, no Cyrillic; slices are generated, so a hand edit of a slice is refused by `--check`.

---

### C2 — the four command-door families as one table (F-O5 (b))

Dispatchable now.

given: factory-rules.md (whole), builder-rules.md, TESTING.md; read: `scripts/tests/test_controller_doors.py` (whole,
142 lines), `design/controller-blocks.md:1-40` and its `command` rows, `scripts/tests/test_controller_state.py` (the
`BASE` helpers it imports, :33)
owns: `ai-packages/qa-factory/scripts/tests/test_controller_doors.py`
non-goals: `controller.py`, `design/controller-blocks.md`, `tools/controller-blocks-gen.py`; the other 217 `command` rows;
any new test file
handoff: report path given by the Lead
edges: E1-E6 below
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/tests/test_controller_doors.py`;
the file itself is a `test_controller_*` file (builder-rules.md:54): judged by the batch canon, named in the report;
commit carries a `tests-over:` line (test-only diff, TESTING.md «Бюджет / Объём»: reason "F-O5 (b), the owner's word;
a door class that produced two defects")
siblings: `test_controller_blocks.py` (route map, keep detector, `test-layers.json:870-883`) — not applicable (it does not
execute doors); the stale numbers in the docstring (:4 "189 blocks … 109") — applied: the docstring drops the numbers
(the walk states them, `controller-blocks.md:3,21`)

Items:
1. Replace the one-family block (:93-135) by ONE parameterised table `DOOR_FAMILIES`, one row per family, id = the family
   name (P16: the red line names the family): `checkpoint`, `gate-decision`, `semantic_reopen`, `recover`. Each row:
   the world setup, the blocked request, the block's text NEEDLE taken from its `controller-blocks.md` row, the door call,
   and the after-check (the same request goes through, or the state the door leaves). The world is built once per file
   and each row runs on its own copy (TESTING.md «Время»).
2. Rows (the block each family proves; counts of `| \`command\` |` rows naming the family in `controller-blocks.md`:
   checkpoint 9, gate-decision 23, semantic_reopen 7, recover 11 — Grep counts today):
   - `checkpoint`: the existing case, moved unchanged ("checkpoint active work before revising scope", `validate`,
     controller-blocks.md:155).
   - `semantic_reopen`: `validate` "semantic content changed; use semantic_reopen" (:165) — after
     `--operation semantic_reopen` the request the block refused goes through.
   - `recover`: `refresh_derived` `DerivedViewStale` "event committed; derived view not refreshed" (:140) — after
     `--operation recover` the view is fresh AND the committed event count is unchanged (the action is NOT repeated).
   - `gate-decision`: the first row in source order of `controller-blocks.md` whose route names `gate-decision` and
     whose block the world of item 3 can reach (the builder names the row in the report; `rg -n "gate-decision"
     ai-packages/qa-factory/design/controller-blocks.md` lists them).
   test: the table itself. expected from: the owner's word F-O5 (b) (spec :618) and each row's own `the way through`
   cell in `controller-blocks.md` (the route the walk promises), never the controller's output.
3. World: per fork B-2 — recommended: a copy of the recorded story `fixtures/stories/cart-1/` (its
   `state/controller.json` exists) where that family's block is reachable from the recorded state; otherwise the `BASE`
   synthetic world of the existing checkpoint case, and the report says which row uses which.
architecture: `AR-9 -- every refusal names a door its receiver can use; four families now proven by executing the door`;
`judgment: none -- a test of existing doors, no check moves`.

Edges:
- E1: a door that does NOT open (the request is still refused after the door) is a found defect: the builder stops, keeps
  the row out of the commit, and returns the refusal text + row as a question (the Lead opens a fix node). INVARIANT: a
  door is never asserted open by reading, and the canon never carries a red row on purpose.
- E2: the needle is block text, never a line number (`test_controller_blocks.py:16`). INVARIANT: lines move, the needle
  does not.
- E3 (empty): if the walk holds no row for a family (renamed operation), the table row fails naming the family.
  INVARIANT: a family silently missing is never green.
- E4: `recover` must not repeat the committed action — the after-check counts events. INVARIANT: DerivedViewStale's own
  promise ("do not repeat the action") holds.
- E5: environment hygiene as the existing case (`CLAUDE_PROJECT_DIR` and `hooklib._PROJECT_ROOT_CACHE` restored in
  `finally`, :130-135) for every row.
- E6: the first two checks of `main` (every named command exists, :51-91) stay as they are.

---

### C3 — FR-59 conversion cards (F-O1, decided whole; spec :631-643)

Every C3 card needs the PLAN CRITIC before code (spec §7 :570, "each FR-59 conversion"). One designer may refine a card
into its plan; the cards below fix direction and owns.

Shared items of every C3 card (each card adds its own):
- S-a. The gate's unknown branch behaves as the decided branch (table below). Where code already does it, no code moves.
- S-b. One row in the registry row's `test` file pins the unknown branch: an input that yields the unknown class ->
  the declared outcome (the question asked and the stage waits / the rerun / the refusal with its door), never a pass.
  It is the registry's requirement for `converted` (`gate-registry.json:3`, `gate_registry.py:673-674`), so it is a
  gate_named row, not a "как раньше" test.
- S-c. Registry row: `status: converted`, `debt_ref: ""`, the decided `unknown_branch` / `on_no_answer` / `waits_at`,
  `vocabulary: code` with `words` = the literal words the sites compare (read from
  `python -B ai-packages/qa-factory/scripts/gate_registry.py --sites` for the row's files; a converted row must say
  `code`, `gate_registry.py:516-517`); every `accept` site resolved per fork F-D1. If the sites compare no literal word at
  all, the builder returns a question (whether a `code` row with empty `words` passes `_check_row` was not established).
- S-d. The debt file is NOT edited (S1b moves the row after acceptance; spec S1 E6).
- DoD of every C3 card: `scenario_walk.py --witness-for <owns>`, `python -B ai-packages/qa-factory/scripts/gate_registry.py --check`
  (the A26 CLI; exit 0 and the row gone from "gates left as debt"), the printed non-slow files; the row's `test` and
  `test_gate_registry.py` are slow (§0.3) — judged by the batch canon.
- Edges common to C3: E-a TEMPORAL — stories in flight that recorded the old outcome (a note where a question is now
  asked) are not rewritten; the new branch applies from the next gate run. INVARIANT: no recorded verdict changes
  meaning after the fact. E-b — the unknown is never turned into a pass by the conversion (AR-28 change check: "the spec
  states each new gate read's behaviour on missing, unreadable and empty input, and a test pins it"). E-c — a site
  re-roled under F-D1 (b) is re-roled only when the function produces or validates rather than accepts a record; the
  plan critic judges each one. INVARIANT: a re-role never hides a literal acceptance (`gate_registry.py:833-836` class).
  E-d — `gate-registry.json` is shared by all C3 cards and S7 (`witness_backstop` row): each card edits ONLY its own
  rows; later merges resolve (row-disjoint, the D-0048 form applied to rows).
- architecture (every C3): `AR-28 -- the unknown branch is declared and pinned by the row's test`; `AR-29 -- <class>
  unchanged / changed as the §1 table says`; `judgment: none -- <why>` only where the table says owner data and nothing
  moves into judgment.

Decided branches (registry today -> after):

| card | gate (registry line) | unknown_branch now | after (decided) | accept sites (F-D1) |
|---|---|---|---|---|
| C3-h | stand_identity (:8-36) | question / wait / stage_entry | keep | none |
| C3-k | provenance_acceptance (:37-92) | question / wait / stage_entry | keep | 13 accept sites |
| C3-b | test_identity (:123-149) | rerun | keep | same_test, already_probed, _match, green_over_same_bytes |
| C3-a | collected_ids (:150-171) | **debt** | **rerun** (owner «да», :641-642) | none (validate) |
| C3-b | live_check_demand (:187-209) | **debt** | **question / wait / window_acceptance, addressee role:qa-code-critic** | proof_required |
| C3-c | s5_coverage (:210-230) | question / wait / window_acceptance | keep | run |
| C3-d | s5_window (:231-252) | question / wait / window_acceptance | keep | validate_window, verdict |
| C3-e | delivery (:253-275) | **debt** | **refuse_with_door** (a kind not in the kinds file -> `no`, the kind named as a factory defect, FR-19) | decide, assess, ledger_reasons |
| C3-i | case_preconditions (:288-315) | question / wait / gate_a | keep | none |
| C3-f | environment_preparation (:316-337) | question / wait / authorization | keep | none |
| C3-g | baseline_identity (:338-359) | refuse_with_door | keep | deployment_readiness |
| C3-j | s5_stand_limits (:482-502) | **debt** | **question; the person's answer persisted in the environment record** (owner :634-637) | check_s5_stand_limits |
| C3-i | reporter_rehearsal_identity (:503-525) | rerun | keep | _rehearse_reporter, hand_to_conductor |
| C3-i | environment_property_cover (:526-548) | question / wait / gate_a | keep | _rehearse_reporter, check_case_preconditions, gate_b_split |

#### C3-0 — the one predicate (prerequisite of every card with an accept site) — fork F-D1

Not dispatchable until F-D1 is decided. On F-D1 (a): owns `ai-packages/qa-factory/scripts/gate_template.py` (new) with
`acceptable(record, consumer) -> bool` reading the row's `accepts[consumer]` (consumer id `<gate>.<consumer>`, the
registry's own form, :79-85) and `verdict_map`; error direction: toward NOT acceptable (an unknown consumer, an absent
record, a word outside `words`, an unreadable registry -> False). Adversarial inputs that must stay not acceptable:
`person_confirmed` under a `promotable: false` row (F-f, `gate_registry.py:56-57`), `not_applicable` without its reason
code where `accepts` lists only `not_applicable:<reason>`, a word in another case (`Matched`), a list or dict as the word.
test: `test_gate_registry.py` table rows (slow: canon). This card needs designer + plan critic (a new shared mechanism).

#### C3-a — collected_ids -> rerun (B-278)

owns: `ai-packages/qa-factory/references/gate-registry.json` (row `collected_ids` only);
`ai-packages/qa-factory/scripts/tests/test_node_ids.py` (one row); `ai-packages/qa-factory/scripts/run_suite.py`
(`verify_node_ids`, `ids_pytest_did_not_find`) ONLY if S-b's row is red today
non-goals: the collect-error note (S5, merged); `blocked_by_env` code (words-gates GW1-36)
Item: row -> `unknown_branch: rerun`, `on_no_answer: rerun`, the `decides` text's residue clause "(residue, B-278: the
template has no unknown branch)" (:152) removed. S-b row in `test_node_ids.py`: a collect that cannot be verified (timed
out / unreadable) -> the run is not refused, the ids are named "not verified", and pytest's exit 4 is answered
`node_id_mismatch`, never passed or failed. expected from: the owner's word «да» to "collected_ids -> rerun (the run
itself checks the ids: pytest exit 4 -> node_id_mismatch)" (spec :487, :641-642) and the row's own `decides` (:152).
Edges: E1 (empty request ids) -> no collect, no note (unchanged). INVARIANT: no id is "missing" on an unverified collect.
architecture: `AR-28 -- unknown branch rerun, pinned by test_node_ids`; `judgment: none -- registry status and a pin; the
run decides as today`. Axis 4 (`SIBLING_MAP.md:86`): the debt row and backlog row B-278 move together — at S1b, by the
integrator's `piles.py close --id B-278` (backlog frozen, PROJECT.md «Командная работа» п. 4).

#### C3-b — test_identity + live_check_demand (share `proof_level.py`)

owns: `ai-packages/qa-factory/references/gate-registry.json` (rows `test_identity`, `live_check_demand`);
`ai-packages/qa-factory/scripts/proof_level.py` (`same_test`, `instance_identity`, `already_probed`, `proof_required`,
`novelty_of`); `ai-packages/qa-factory/scripts/execution_request.py` (`instance_shas`, `_match`,
`green_over_same_bytes`) — only per F-D1; `ai-packages/qa-factory/scripts/tests/test_proof_level.py` (rows); the
window-acceptance reader of the critic's answer (named by the plan — not established here)
Items: (1) test_identity: F-D1 for the 4 accept sites; S-b row: an old result whose identity does not match -> "run
again", never reused. expected from: registry `decides` (:125) "a non-match is an unknown and the answer is to run
again". (2) live_check_demand: today a legacy row with unmeasured novelty "is shown to the person as a debt, never a
block" (:189); after: novelty `unknown` -> a question to `role:qa-code-critic` at window acceptance ("is a live probe owed
for this test?"); the window waits until the critic's typed answer is recorded; `closed_by: [role:qa-code-critic]`,
`addressee: [role:qa-code-critic]`. expected from: the owner's word «да» (spec :488, :641-643). This changes a meaning
(a legacy row can now hold the window): PROJECT.md «Как принимается изменение пакета» п. 6 — (а) measure first how many
rows of a recorded story carry `novelty: unknown` (one command on `fixtures/stories/cart-1`, result in the plan), (б)
plan critic.
Edges: E1 (conflict with C3-k on `execution_request.py`): C3-b before C3-k, `очередь: C3-b → C3-k`. E2 (absent novelty
field) = `unknown` (asked), never `unchanged`. INVARIANT: an unmeasured novelty never passes silently. E3 TEMPORAL: rows
of stories in flight already shown as debt are not re-asked retroactively (E-a).
architecture: `AR-28`, `AR-29 -- the probe-owed decision is the code critic's judgment, accepted at window acceptance;
code checks the presence of the typed answer (xref)`.

#### C3-c — s5_coverage (B-221)

owns: gate-registry.json (row `s5_coverage`); `ai-packages/qa-factory/scripts/s5_precheck.py` (`run`) per F-D1;
`ai-packages/qa-factory/scripts/tests/test_s5_precheck.py` (one row)
Item: S-b: a Then whose binding cannot be established -> a question to the code critic at window acceptance, the
window waits. expected from: registry (:212, :225-226). Edge: FL9 owns `s5_precheck._open_oracle_door` — function
disjoint; `очередь: FL9 → C3-c` if both run the same week.

#### C3-d — s5_window (B-179) — after S9

owns: gate-registry.json (row `s5_window`); `ai-packages/qa-factory/scripts/acceptance.py` (`validate_window`);
`ai-packages/qa-factory/scripts/window_record.py` (`verdict`); `ai-packages/qa-factory/scripts/tests/test_window_record.py` (one row)
Item: S-b: an unmeasured detector in the window -> a gap closed by the critic, never a pass (:233). Edge: S9 owns
`window_record.verdict` too — `очередь: S9 → C3-d` (spec §3 :432-433).

#### C3-e — delivery -> refuse_with_door (B-061)

owns: gate-registry.json (row `delivery`); `ai-packages/qa-factory/scripts/delivery_verdict.py` (`decide`);
`ai-packages/qa-factory/scripts/check_delivery.py` (`assess`, `ledger_reasons`) — only if S-b is red;
`ai-packages/qa-factory/scripts/tests/test_check_delivery.py` (one row)
Item: row -> `unknown_branch: refuse_with_door`, `on_no_answer: refuse_with_door`. S-b row: a record whose kind is not a
key of `references/delivery-verdict-kinds.json` -> the verdict is `no`, and the reason names the unrecognised kind with
owner `factory` (FR-19: "an unrecognised reason is a defect of the classifier"). expected from: the owner's word «да»
(spec :491, :641-643) and the row's own `decides` (:255 "a kind the file does not hold is no (it never asks)").
Edges: E1 (empty kinds file / unreadable) -> `no` with the factory defect named, never `yes`. INVARIANT: an unknown kind
never yields `yes` or `after_checks`. E2: F-D1 — `decide` produces the word (re-role `produce` is the honest one,
recommended; the plan critic confirms).

#### C3-f — environment_preparation (B-255), C3-g — baseline_identity (B-281)

C3-f owns: gate-registry.json (row `environment_preparation`), `ai-packages/qa-factory/scripts/environment_preparation.py`
(`plan_environment`, `_facts`) only if S-b is red, `ai-packages/qa-factory/scripts/tests/test_environment_preparation.py`
(one row: unknown deploy proof -> question at authorization, waits; registry :318, :332-334).
C3-g owns: gate-registry.json (row `baseline_identity`), `ai-packages/qa-factory/scripts/baseline_contract.py`
(`deployment_readiness`) per F-D1, `ai-packages/qa-factory/scripts/tests/test_baseline_contract.py` (one row: unknown
old-build identity -> refused with its door; a person's word never stands in, :340). Keep-status of those two test files
in `test-layers.json` not read today (command: `rg -n "test_environment_preparation|test_baseline_contract"
ai-packages/qa-factory/scripts/tests/test-layers.json`); if quarantined, the card returns a question (the registry's
`test` must be a canon file).

#### C3-h — stand_identity (B-257) — gate_preflight queue position 4

owns: gate-registry.json (row `stand_identity`); `ai-packages/qa-factory/scripts/tests/test_stand_identity.py` (one row);
code sites only if S-b is red: `runtime_probe.py` (`conclude`, `finish`), `gate_preflight.py` (`_derive_probe`,
`named_container_said`), `driver_stage_build.py` (`build_outcome`)
Item: no accept site — converts by S-b/S-c alone (F-D1 does not apply). S-b: a stand whose build cannot be identified ->
the `stand_identity` question before the stage, the stage waits; the person's word recorded in
`records/stand-identity.json` (policy_file :30) covers the same `scope_keys` next time. expected from: registry (:9,
:28-33). Edge: `vocabulary: target` -> `code`: the words are the code's own `result` words (`runtime_probe`); builder
confirms from `--sites`.

#### C3-i — case_preconditions + reporter_rehearsal_identity + environment_property_cover (one card: shared functions)

Why one card: `_rehearse_reporter` is registered by both `reporter_rehearsal_identity` (:507) and
`environment_property_cover` (:530); `check_case_preconditions` by both `case_preconditions` (:293, dispatch) and
`environment_property_cover` (:531, accept). Converting one row while the other still registers the same function is
finding "registered more than once … give each row its own function" (`gate_registry.py:833-836`).
owns: gate-registry.json (the three rows); `ai-packages/qa-factory/scripts/gate_preflight.py` (`_check_one_precondition`,
`check_case_preconditions`, `_sort_items`, `_case_question`, `_none_card`, `_rehearse_reporter`, `_read_probe_report`) —
HOT; `ai-packages/qa-factory/scripts/planning_contract.py` (`_unmet_preconditions`);
`ai-packages/qa-factory/scripts/driver_gates.py` (`hand_to_conductor`); `ai-packages/qa-factory/scripts/stand_gaps.py`
(`gate_b_split`); `ai-packages/qa-factory/scripts/tests/test_gate_preflight.py` and `test_environment_record.py` (rows)
Items: (1) give each row its own function where a function serves two rows (split the `environment_property_cover`
lookup out of `_rehearse_reporter` and `check_case_preconditions` into its own helper — e.g. the existing
`_environment_cover` (:4214) — and register THAT helper under `environment_property_cover`); (2) S-b rows: a precondition
`uncheckable` -> gate A question, waits (:300-311); a rehearsal with no row of this command -> rehearsed again, nothing
reused (:505); no record row / unreadable record / revoked row -> the person is asked (:528). expected from: the three
rows' `decides` texts.
Edges: E1 POSITIONAL: the cover lookup stays AFTER the probe and only on the card branch (`_environment_cover` docstring
:4218-4221). INVARIANT: the record never hides a report the probe reads and never skips a probe. E2 (unreadable record) ->
said once, covers nothing (:4228-4231). This card is the gate_preflight queue's FIRST.

#### C3-j — s5_stand_limits -> question, answer persisted (B-282) — gate_preflight queue position 2

The registry: "the environment registry" of the owner's word is **the environment record**,
`qa-factory/records/environment-properties.json` (`environment_record.py:33 RECORD_REL`; docstring :1-17: "what a person
accepted ONCE as a property of this environment … the gates read it before they build a card"). Its ONE writer is
`environment_record.record(root, key, option, words, story, about)` (:326); the gate's reader is `environment_record.covering`
(:300) through `Rehearsal._environment_cover` (`gate_preflight.py:4214-4249`); the key of a gap row is derived by
`environment_record.lasting` (:133) through `Rehearsal._lasting_of` (`gate_preflight.py:4200-4212`); the driver writes the
person's `accept always` through `stand_gaps.record_lasting` (`stand_gaps.py:1243-1254`, `ER.record(project,
gap["property_key"], "accept", …)`). Alternative carrier: the project answer registry `project_knowledge.py`
(`records/project-knowledge.json`, :1-16) — fork F-C2.
owns:
- `ai-packages/qa-factory/scripts/environment_record.py` (a third scope beside `LEVEL`/`CASE` :35: `STAND_LIMIT = "stand_limit"`, its fields, its branch in `lasting`, `about_of`, `current_key`, `near_miss`, `_valid_key`, and `record`'s CLI form)
- `ai-packages/qa-factory/scripts/gate_preflight.py` (`_e2e_limit` :3088, `check_s5_stand_limits` :3165, `_stand_limit_card` :3242) — HOT
- `ai-packages/qa-factory/references/gate-registry.json` (row `s5_stand_limits`)
- `ai-packages/qa-factory/scripts/tests/test_environment_record.py`, `ai-packages/qa-factory/scripts/tests/test_gate_preflight.py` (rows)
- the question vocabulary / card text carrier if the new card needs a new kind (`references/question-vocabulary.json`; the builder reports, a new kind is a question first)
non-goals: `config.json` writing (no package writer of `environments[].measured` exists: Grep `def (write_config|save_config|…)` over `scripts/*.py` finds only test helpers); `manual_capture.timeout_for` (reads the config measurement, unchanged)
Items:
1. Today `unmeasured` is an INFO note, never a card (`check_s5_stand_limits` :3191-3194; docstring :3176-3177). After:
   `unmeasured` builds ONE gap card per profile at the gate where the check runs (gate A rehearsal, `run` :6088 — fork
   F-C1 on the place), saying: the stand's page load is not measured and the page objects wait at most N s, so whether
   the e2e rows of `<profile>` fit this stand is unknown. Options: (a) `accept always` for this stand: the e2e rows run
   here (recorded in the environment record); (b) the existing handed door `executor unavailable: <profile>`; (c)
   `<case id>: manual` (existing). expected from: the owner's word (spec :634-637) and the spec's F-O1 row (:495).
2. The gap row carries `property_key` from `lasting`: key `{scope: "stand_limit", environment: <stand name>,
   definition_sha: <stand definition sha, as CASE keys use, `stand_identity.definition_sha_for`>, contour: <profile_id>,
   wait_s: <page_object_max_wait_s>}`; `_environment_cover` is asked BEFORE the card: a live row under exactly this key ->
   no card, one note "not asked — <their words>, as you recorded on <date> (EP-n)". test: rows in
   `test_environment_record.py` (key built / refused when stand or wait absent) and `test_gate_preflight.py` (unmeasured
   -> card; same stand + same wait with a recorded row -> note, no card; wait changed -> card says the earlier answer no
   longer applies). expected from: FR-7 ("a boundary a person has answered is never re-asked with the same text") and the
   owner's word "so the same stand is not asked again".
3. The writer and its reader land in ONE commit (AR-22): the new scope in `environment_record` and the gate's read of it.
4. Registry row: `unknown_branch: question`, `on_no_answer: wait`, `waits_at` per F-C1, `closed_by: ["person"]`,
   `addressee: ["person"]`, `person_subject: "world"`; F-D1 for the accept site.
Edges:
- E1 (absent stand name / placeholder `this stand`, `environment_record.py:49`): no key (`why: no_key`), the card is
  shown without `accept always`. INVARIANT: nothing is recorded under a placeholder key (docstring :17).
- E2 (absent `page_object_max_wait_s`): today's `unmeasured` with `fields` names the missing wait; no key (the wait is part
  of the key) — the card offers (b)/(c) only. INVARIANT: a cover never holds for an unknown wait.
- E3 (unreadable record): said once, covers nothing, card shown (FR-59).
- E4 (`skip_stand_limits: true`, :3180): unchanged — the check is off, no card, no record read.
- E5 (conflict with `check_s5_reporter`, which skips a rehearsal only when the state is `over`, :3322): unchanged — an
  `unmeasured` profile is still rehearsed. INVARIANT: the reporter proof is not lost to the new card.
- E6 TEMPORAL: the environment record file may not exist (before any `record`); readers treat absence as "no rows". The
  new scope exists only after this card; older records with two scopes stay valid (`schema_version` unchanged, an extra
  scope is additive; if `load_rows` refuses an unknown scope the builder returns a question).
- E7 POSITIONAL: the cover is read only on the card branch (as `_environment_cover`, :4218), never before the measurement
  check. INVARIANT: a recorded measurement in the config always wins; the record never hides `over`.
- E8 (outside input): the person's words file (`--words-file`) is outside input; `record` already cuts and validates it —
  rows AT and BEYOND its existing limit if `test_environment_record.py` lacks them.
architecture: `AR-22 -- the answer's writer and its gate reader in one commit`; `AR-24 -- the person's words reach the
record whole`; `AR-28 -- an unmeasured limit is asked, never run on a guess`; `AR-29 -- owner intent for the answer, the
cover is a key join (xref)`.

#### C3-k — provenance_acceptance (B-255) — designer first; gate_preflight queue position 3

13 accept sites in 9 files (:41-54); the `decides` text lists its own residue ("the local_source and fingerprint bare
not_applicable, the baseline, gate A - T2", :39). Not dispatchable from this text: designer refines (after C3-0) into
per-file steps; `очередь: C3-b → C3-k` (execution_request.py), `C3-a → C3-k` (run_suite.py `probe_runtime`).

gate_preflight queue (HOT, one stream at a time): **C3-i → C3-j → C3-k → C3-h**, each after any open node of a TAKEN batch
that owns `gate_preflight.py` (§4).

---

### C4 — F-O2's condition: a language with no probe row takes the role's probe road

Dispatchable now on fork B-1's recommendation.

given: factory-rules.md (whole), builder-rules.md, TESTING.md; read: `references/gate-registry.json:571-593`
(`probe_verdict`), `scripts/probe_by_code.py` (docstring), `scripts/red_sandbox.py` (`--probe` docstring),
`scripts/tests/test_probe_by_code.py` (its world builder), `references/detectors.json` (`assertion_probes`)
owns: `ai-packages/qa-factory/scripts/tests/test_probe_by_code.py` (one table row) — on B-1 (a)
non-goals: any probe row in `detectors.json` (F-O2 (a): none now); `probe_by_code.py`, `red_sandbox.py`, the window code
(a red row is a found defect, E1)
handoff: report path given by the Lead
edges: E1-E4
DoD: `scenario_walk.py --witness-for ai-packages/qa-factory/scripts/tests/test_probe_by_code.py`; the file is slow
(221.4 s, `slow_tests.json:78`): judged by the batch canon
siblings: `test_red_sandbox_probe.py` (keep, `test-layers.json:4321`) — not applicable unless the receipt reader lives
there (builder names it); live proof B-373 (`plans/piles/live-runs/findings/B-373-…`) stays queued
Item: one row: a test file whose suffix has NO `assertion_probes` row (the builder picks one and shows the data has no row
for it, e.g. `.kt`; the pick is confirmed by reading `detectors.json`) -> `probe_by_code` writes a record that names what
was not read, exits non-zero and names the door `red_sandbox.py --probe` (registry :572); THEN the role's road: the same
test probed through `red_sandbox.py --probe` (stub run, as the file's world does) leaves a receipt, and the reader that
decides whether the window may close (the builder names it: `proof_level.proof_required` or `acceptance.validate_window`)
counts that receipt — the stage does not stop. expected from: the owner's word F-O2 (spec :622-627: "on a language with
no row the role's own probe … must be a working road end to end … the stage does not stop"), P30, registry `probe_verdict`
(:572: "a language with no `assertion_probes` entry … the door `red_sandbox.py --probe`").
Edges:
- E1: if the road is broken (the receipt is not counted, or `--probe` refuses the suffix), the builder stops and returns
  the evidence as a question; the Lead opens a fix node (P22: a language with no row that stops the factory is a defect).
  INVARIANT: no red row is committed; the defect is never left implied.
- E2: an `incomplete` record never replaces a judged one (`keep_standing_record`, :572). INVARIANT unchanged.
- E3 (one road, P31): the row must not branch on the language NAME; the suffix reaches the shared mechanism through the
  data lookup like every other language.
- E4: `--probe` output is the factory's own (not outside input): no battery.
architecture: `AR-1 -- the suffix is read through the data row lookup; no language name in code`; `AR-28 -- no row is a
named unknown with a door, never a stop`; `judgment: none -- a test of an existing road`. Commit carries a `tests-over:`
line (test-only).

---

### C5 — F-O4: the conductor prompt, replace vs append — ONE measured experiment (procedure for the Lead)

Not a builder card. The owner: «ок и учти что мы планируем оркестратора полностью заменить дирежёром. Надо что бы он
справлялся» (spec :619-621).

Facts: the conductor is called with `system_file=references/conductor.md` at `driver_conductor.py:337` and
`driver_stage_s8s9.py:451`; `driver_runner.claude_cmd` turns it into `--append-system-prompt-file` (`driver_runner.py:606-607`).
A run's conductor sessions are recorded in `state/conductor.jsonl` (`experiments/measurers/conductor_families.py:3`).

Procedure:
1. Measure the premise (CLAUDE.md pt. 6a): `claude --help` on this machine — does a REPLACING flag exist
   (`--system-prompt-file` or the current spelling)? Record the verbatim help line. If none exists, the experiment ends:
   X3's prompt half becomes a real limit (debt file "Real limits") with that line as its reason.
2. Pick recorded conductor questions from the latest stand run's `state/conductor.jsonl` (fork F-E1 on how many): at least
   one that needs tool use (the conductor runs a factory command) and one `ask_person`.
3. In a project copy (`experiments/measurers/prepare_copy.py`; P8: no trace in the project), run each question twice with
   the same model and allowed tools: (A) as today, (B) with the replacing flag; nothing else differs.
4. Judge per run, in `experiments/conductor-system-prompt/notes.md` (PROJECT.md п. 5 notebook): (a) turns; (b) input and
   cache tokens; (c) the answer obeys `references/conductor.md` "Your answer" (shape valid, `options` only with
   `ask_person`/`stop`); (d) the decision: same as (A), or different with a reason the Lead accepts; (e) **copes without
   the host's default tool guidance**: every tool call well-formed, no refused or malformed call, no command the guard
   refuses, no lost turn re-explaining tools. (e) is the owner's added measure; a (B) run that fails (e) is "does not
   cope" whatever (a)/(b) say.
5. Verdict to the owner in plain words: switch / keep (real limit) / switch with an added short tool section in
   `conductor.md` (then one more (B) run). No money figures in the notebook (P18: money is not written to repo files).
FR: F (FR-26: read the raw transcripts before any number is a finding). A switch, if chosen, is its own builder node
(`driver_runner.claude_cmd` + the two callers), FR-33 live proof row in `live-runs`.

---

### S9 — X10, a person's word on a `review` gap (FR-57) — PLAN CRITIC FIRST

The spec's S9 (:379-394) stands as written; this card adds dispatch facts. Re-read today: `window_record.py:1741`
`WORD_READ_KINDS = ("quality", PROBE_GAP_KIND)`, `:1745 _unread_words`, `:1766` "recorded, not read by this window",
`:1891` the read; `controller.py:7425 _s5_word_index`, `:7444 _s5_gap_problems`.
Order: (а) the premise measured on a fixture story (one `window_record.py` run with a `review` gap and a recorded word —
the "recorded, not read" line must appear; result in the plan); (б) plan critic; (в) the reused
`waiver.split_overridden` (:1756-1760) in its gate role errs toward "does not match" — adversarial words that must stay
unread: a word naming a different gap, a revoked word, a word for another stage, `*` where the block names the review gap
of a different instance.
owns (for the plan): `ai-packages/qa-factory/scripts/window_record.py` (`WORD_READ_KINDS`, `verdict`, `_unread_words`);
`ai-packages/qa-factory/scripts/controller.py` (`_s5_word_index`, `_s5_gap_problems`) — HOT; tests
`test_probe_gap_word.py`, `test_window_record.py` (both slow: canon); `design/state-exits.md` row (AR-25);
`design/controller-blocks.md` + `tools/controller-blocks-gen.py` regeneration if a block route changes (spec §5 :471).
Queue: `S9 → C3-d` (`window_record.verdict`); controller.py also in FL4 — `S9 → FL4` or function-disjoint (D-0048).
architecture: `AR-9`, `AR-24`, `AR-25`, `AR-28`; census: intent / xref (§1).

### S10 — G15, read heads as data (F-L6 (a)) — HOT `stage_guard.py`

The spec's S10 (:396-408) stands; facts re-read: `host_adapter.py:452 _READ_HEAD`, `:525 _read_refusal` (:539 uses it);
`stage_guard.py:2509-2512 READER_COMMANDS`, `:2589-2590 _is_reader`; `tests/role_replay.py:30-36` derives `_READ_ALTS`
from `_READ_HEAD.pattern` (must follow; `:34` asserts the pattern's shape).
**Found today, in S10's own function**: `stage_guard._is_reader` does `name.rstrip(".exe")` (:2590) — `rstrip` strips the
CHARACTERS `.`, `e`, `x`, not the suffix, so `catx` -> `cat`, `lsx` -> `ls`, `type`... -> head treated as a reader (errs
toward the reader exemption, i.e. permissive). Added to S10's adversarial list and item: use `removesuffix(".exe")`.
Adversarial heads that must stay refused / non-reader: `python`, `bash`, `pwsh`, `node` named in the table; a head with a
path (`/usr/bin/rg`); `.exe` and case variants; `catx`/`lsx`/`grepe` (the rstrip class); an empty or unreadable table
(falls back to the in-code floor = today's lists, never "any head"); a table row adding a writer to the read heads. The
two lists stay separate (READER_COMMANDS: runner-guard "mention" heads incl. `cp`/`mv`; `_READ_HEAD`: a no-Bash role's
one plain read).
owns: `ai-packages/qa-factory/references/launch-causes.json` (new tables `read_heads`, `reader_commands`);
`ai-packages/qa-factory/scripts/host_adapter.py` (`_READ_HEAD`, `_read_refusal` text); `ai-packages/qa-factory/scripts/stage_guard.py`
(`READER_COMMANDS`, `_is_reader`) — HOT; `ai-packages/qa-factory/scripts/tests/role_replay.py` (`_READ_ALTS`)
DoD: witness-for over owns; `test_hooks_wiring.py` if printed (hooks, builder-rules.md:50); slow guard tests: canon.
Queue: taken batches name `stage_guard` (onboarding-hooks/6 :16,:31; onboarding-forge/2 :53,:82) and `host_adapter`
(onboarding-hooks/7 :30) — the Lead reads those node rows' status before launch (§4); if open, `очередь:` lines.
architecture: `AR-1 -- the head lists are data rows with an in-code floor`; census safety (§1).

### FL1 — R2: resolve a hand-typed pytest id at store time (F-L1 (a))

owns: `ai-packages/qa-factory/scripts/manifest_put.py` (the store path of a test id — the plan names the function; the
module's `def` list read today :174-1021 holds no id resolver); a table row in the keep test that judges `manifest_put`
(witness-for names it)
Item: a hand-typed pytest node id is resolved through `node_ids` (the one collect reader) when the fragment is stored; a
store where no collect is possible keeps the id and marks it "not verified" (FR-16 "at the moment it is stored"; FR-59).
expected from: FR-16 text and the spec's F-L1 (a) (:535-537).
Edges: E1 (no collect possible) -> "not verified", never refused and never "missing". E2 (limit) — a collect call is
bounded by the existing collect timeout of `node_ids`; at timeout -> E1. E3 (outside input: the id string from a role) —
internal (a role's output): no battery.
Queue: `manifest_put.py` is in thinking-roles/6 TR4-17 (spec :537, batch not taken) and is named in TAKEN
onboarding-forge/1 (:50) and /2 (:103) rows — status not read today (§4). Needs a designer pass for the function name
(not drafted further here).

### FL2 — R3: "skipped because the product has no such surface" (F-L2 (a)) — PLAN CRITIC FIRST

owns (for the plan): `ai-packages/qa-factory/references/delivery-verdict-kinds.json` (one skip-reason word mapped to
`pending_implementation`; today `"skipped": "planned_skip"` :95 and `"pending_implementation": {"verdict": "no", …}` :44);
the run-row writer that carries the closed skip-reason word (named by the plan); `test_check_delivery.py` row (slow).
The role chooses the word (P27); code maps it. Meaning of a delivery word changes -> PROJECT.md п. 6 (а)(б).
Reader that must stay consistent: `test_s1_s2_contract.py:319-325` G1-10 (`fr21_row_mismatch`, quarantined — not run;
its debt-row statement is S1b's edge E2).

### FL4 — R4: the S7 rework door for a case-less `bug_candidate` (F-L4) — PLAN CRITIC FIRST, HOT `controller.py`

owns (for the plan): `ai-packages/qa-factory/scripts/controller.py` (the rework route; `ANSWER_REWORK_OWNERS` :9391, the
`--cases` argument :9908) — a typed `--candidate <K-n>` in place of `--cases` for that route; `design/controller-blocks.md`
regeneration (`tools/controller-blocks-gen.py`); `test_controller_*` rows (canon). Designer + plan critic (spec :543-544).
Queue: one stream on `controller.py` at a time: S9 and FL4 function-disjoint or `S9 → FL4`.

### FL9 — X2 residue: the oracle door by capability, not by pytest (F-L9)

owns: `ai-packages/qa-factory/scripts/s5_precheck.py` (`_open_oracle_door` :1654 only); one row in `test_s5_precheck.py`
(slow: canon)
Item: `_open_oracle_door` names the binding road by a capability key of the test file's language row in
`references/detectors.json` (marker form vs the `manifest_put` fragment), never by the language name; today it names
`@pytest.mark.qa_unresolved(...)` for any file (:1661). expected from: P31, AR-1, spec F-L9 (:553-555).
Edge: E1 — the capability key itself is NOT established today (spec: "it needs the capability key confirmed in
`detectors.json`"); if no such key exists, the builder stops and returns a question (adding a data key is a new row with a
default, AR-1 form — the Lead decides). INVARIANT: no language name enters the branch. E2: a language with no row -> the
door says how to bind through the `manifest_put` fragment (the road every language has). `очередь: FL9 → C3-c`.

---

### S1b — the debt file's second pass (LAST)

Runs after every phase-2 node it moves is accepted (spec S1 E6). One writer of the debt file at a time.
given: the spec §0, §2, S1 (edges E1-E5); this card; the accepted handoffs of the nodes it moves
owns: `ai-packages/qa-factory/design/factory-rules-debt.md`; `ai-packages/qa-factory/design/factory-rules.md` (the *Check*
lines of FR-5 and FR-23 only, F-L12); `ai-packages/qa-factory/scripts/tests/test_null_outcomes.py` (`the_debt_row`,
:588-597, K0.15 only)
non-goals: any code; any row not listed; `plans/BACKLOG.md` (frozen; B-ids closed by the integrator's `piles.py close --id`)
DoD: `scenario_walk.py --witness-for <the three owns>`; `python -B ai-packages/qa-factory/scripts/tests/test_null_outcomes.py`
(keep, gate_named; not in slow list); `python -m pytest tools/test_piles_close_id.py -q`;
`python -B tools/factory_rules_index.py --check` (the index is built from titles; a Check line is not a title)
Items:
1. Move to "Fixed since this walk" (one bullet each, B-id kept inside the bullet — spec S1 E3): R5 (closed in code,
   `driver_stage_s8s9.py:370-379` per the spec; critic F4), R7 (on the batch canon, critic key 2), R9 (after C1: "closed by
   code; proven by a live run (FR-33)" + live-runs row), X16, G4 (after C3-a), W3 (S7), X9 (S8), X10 (S9), G15 (S10), each
   FR-59 G-row after its C3 card, R2/R3/R4/X2-residue after FL1/FL2/FL4/FL9.
2. **W1 is NARROWED, not closed** (critic F7, t-942 :54-59): the row keeps "residue: the Level vocabulary is a code tuple
   (`contract.PLAN_LEVELS`; `contract.py:594` `TRACE_LEVELS` re-spells it)". Closing it whole needs a data row or a written
   Lead decision (fork F-L14).
3. K0.15 (`test_null_outcomes.py:596-597`): its positive control counts `|` lines holding `FR-23` `>= 2`; moving R5 (the
   FR-23-alone row) to a bullet leaves one. Re-point the control to a row that stays: the same filter shape
   (`ln.startswith("|") and "<rule>" in ln`) must find the `| FR-21 |` row (`>= 1`), which E2 of the spec keeps. The main
   check (exactly one FR-23+FR-5 row with the four needles, :591-595) is unchanged. expected from: spec S1 E1 (:176-179).
4. F-L12: FR-5 and FR-23 *Check* lines name `references/null-outcomes.json` and `scripts/tests/test_null_outcomes.py`
   (spec :560-561: "it names an existing check's carrier, no meaning change").
5. Header counts recomputed from the tables after the edit; a table left empty keeps its heading with "Nothing open."
   (spec S1 E4).
Edges: E1 — the FR-23+FR-5 row (R6) stays (it is open). INVARIANT: K0.15's single debt carrier stays. E2 — the
`| FR-21 |` line count stays exactly one (G1-10, `test_s1_s2_contract.py:319-325`, quarantined: judged by reading). E3 —
moved, never deleted (spec S1 E5). E4 — FR-30 English. E5 TEMPORAL — a row whose node is not accepted when S1b runs stays
open; S1b may run in two sub-passes (after wave 1, after wave 3). E6 — axis 4: each moved FR-59 row's B-id is handed to
the integrator for `piles.py close --id` in the same move (spec critic key 4).
architecture: `none -- design doc and one control of a test` is not available for a package commit touching
`factory-rules.md`'s Check lines only if the gate refuses it; builder writes `architecture: none -- <reason>` per
`tools/architecture_gate.py`; `judgment: none -- the debt file and Check lines name carriers, no check moves`.

## §3. Waves

**Wave 1 — now, in parallel (disjoint owns):** C1, C2, C4, FL9 (stops at E1 if the key is absent), plus C5 (Lead
procedure, any time) and C3-a (registry row `collected_ids` + `test_node_ids.py`; row-disjoint with S7 on
`gate-registry.json`) once its plan critic passes. Owns check: C1 {bug_records, judge_results, external_writes,
common-rules + slices, external-writes.md, templates/test-report.md, form_selftest, test_bug_records,
test_external_writes_bug_refusals}; C2 {test_controller_doors}; C4 {test_probe_by_code}; FL9 {s5_precheck
`_open_oracle_door`, test_s5_precheck}; C3-a {gate-registry row, test_node_ids, run_suite two fns}. Pairwise disjoint;
none touches S7 (`check_witness.main`, `exit_gate.witness_errors`, registry row `witness_backstop`) or S8
(`project_decisions`, `factory_dashboard`, `finding-scopes.json`, `factory-backlog.md`) except `gate-registry.json` by row.
Four dispatchable from the text alone: C1, C2, C4, FL9 (each on the recommended fork, named in its header).

**Wave 2 — after plan critics (one critic pass per topic, R13-g: topic "rules debt, phase 2 plans"):** C3-0 (if F-D1
(a)), C3-b, C3-c (after FL9), C3-e, C3-f, C3-g, C3-i (gate_preflight 1st), S9, FL2. Disjoint pairs: C3-b {proof_level,
execution_request three fns}, C3-c {s5_precheck.run}, C3-e {delivery_verdict, check_delivery}, C3-f
{environment_preparation}, C3-g {baseline_contract}, C3-i {gate_preflight 7 fns, planning_contract, driver_gates,
stand_gaps}, S9 {window_record, controller two fns}, FL2 {delivery-verdict-kinds.json + run-row writer} — FL2 and C3-e
both read delivery kinds: `очередь: C3-e → FL2` (C3-e pins the unknown-kind branch FL2's new word must pass).

**Wave 3 — serial on hot files:** gate_preflight: C3-j → C3-k → C3-h (after C3-i); window_record: C3-d after S9;
controller.py: FL4 after S9 (or function-disjoint); S10 after the taken stage_guard/host_adapter rows are read; FL1 after
TR4-17 and the taken manifest_put rows.

**Wave 4:** S1b (two sub-passes allowed, E5), then the BATCH CANON on CI (builder-rules 7b; coordinator).

**Collisions with S7/S8 in flight:** `references/gate-registry.json` — S7 may edit row `witness_backstop`
(`exempt_reason`, spec S7 siblings); every C3 card edits other rows: row-disjoint, the later merge resolves. No other
overlap (S7: check_witness/exit_gate; S8: project_decisions/factory_dashboard/factory-backlog/finding-scopes). Note for
the Lead: onboarding-forge/2 is now TAKEN (`plans/piles/onboarding-forge/batch-2-onboarding-roles-forge-p3.md:3`,
"статус: в работе"), and its row SC2-26 (:60) owns `check_witness.py` and `factory_dashboard.py` (status `ожидает`) —
the spec's "not taken" (:136) is stale for S7/S8.

**Plan critic needed:** C3-0, every C3 card (spec §7), S9, FL2, FL4. Not needed: C1 (no meaning change — the owner
decided the home; but D-1 (ii) changes how `bug_file` resolves: the Lead may route it to the plan critic under п. 6;
recommendation: critic on the C1 diff is enough because the old frame still resolves, E5), C2, C4, FL9, S1b.

## §4. Taken pile batches (collisions)

Taken today (header "статус: в работе", Grep `^кучка: .*статус: (в работе|взята)` over `plans/piles/**/batch-*.md`, 10
hits): github-move/3; onboarding-forge/1, /2, /3, /4; onboarding-hooks/4, /5, /6, /7, /8. A Grep of their files for this
draft's owned file names (positive control: the same call found `check_witness` at onboarding-forge/2 :60) hits:
- onboarding-forge/2: `external_writes` and `common-rules` (:50-51), `judge_results` (:65), `bug_records` (:66, :82),
  `stage_guard` (:53, :82), `run_suite`/`execution_request` (:49, :81, :84), `window_record` (:64, :106), `manifest_put` (:103),
  `gate_preflight` (:32, :39) — touches C1, S10, C3-a/b/d/k, FL1, C3-h/i/j.
- onboarding-forge/4: `common-rules`, `external-writes`, `test-report.md` (:45), `bug_records` (:57), `gate_preflight`
  (:42), `baseline_contract` (:44), `stand_gaps` (:53) — touches C1, C3-g, C3-i/j.
- onboarding-forge/1: `gate_preflight` (:32, :74), `environment_record` (:40), `manifest_put`/`controller.py` (:50) —
  touches C3-j, FL1, FL4.
- onboarding-hooks/8: `common-rules` (:36), `execution_request` (:35); onboarding-hooks/7: `host_adapter` (:30);
  onboarding-hooks/6: `stage_guard` (:16, :31); onboarding-hooks/5: `gate_preflight` (:35, :38).
NOT ESTABLISHED: whether those rows are open nodes owning the files or closed history (the lines are long; their status
cells were not read). Before launching C1 the Lead reads onboarding-forge/2 :50-51, :65-66 and onboarding-forge/4 :45, :57
(`rg -n "" <file>` with those lines, the status cell at the row's end); an open row -> an `очередь:` line in both batches
(PROJECT.md «Командная работа» п. 3) or a function-disjoint owns split. Same for the other cards' hits.

## §5. Pile rows to register (П1)

Into an UNTAKEN batch of the pile that holds the rules-debt topic (the Lead names it; each row with a findings file by
D-0044 — the findings are this draft's cards):
- `RD2-C1 | П1 | bug file homes: writer <-> readers (F-O6 (a), critic F8, external_writes bug_file) | builder | owns of C1 | D-1, D-3 | ожидает`
- `RD2-C2 | П1 | four command-door families as one table (F-O5 (b)) | builder | test_controller_doors.py | B-2 | ожидает`
- `RD2-C3-<x> | П1 | FR-59 conversion: <gate> (F-O1) | designer -> plan critic -> builder | owns of the card | F-D1; gate_preflight queue | ожидает` (one row per C3 card: 0, a, b, c, d, e, f, g, h, i, j, k)
- `RD2-C4 | П1 | the no-probe-row road reaches acceptance (F-O2 condition) | builder | test_probe_by_code.py | B-1 | ожидает`
- `RD2-C5 | П1 | conductor prompt replace vs append: one experiment (F-O4) | Lead | experiments/conductor-system-prompt/ | F-E1 | ожидает`
- `RD2-S9 | П1 | person's word on a review gap (X10) | designer -> plan critic -> builder | window_record, controller | — | ожидает`
- `RD2-S10 | П1 | read heads as data + _is_reader rstrip fix (G15) | builder | launch-causes, host_adapter, stage_guard, role_replay | taken-batch rows | ожидает`
- `RD2-FL1 / FL2 / FL4 / FL9 | П1 | R2 / R3 / R4 / X2 residue | per card | per card | per card | ожидает`
- `RD2-S1b | П1 | debt file second pass + K0.15 control + FR-5/FR-23 Check lines | builder | three owns | all above | ожидает`
- live-runs rows (FR-33), by the spec §7 (:573-575): R9/C1 (reporter + external write on the jira channel), C3-j (the
  card and the recorded answer), C3-b (critic asked at window acceptance), S9.

## §6. Forks (returned, not decided)

Lead (technical):
- **F-D1 — conversion of accept sites** (§0.1). (a) build `gate_template.acceptable` (C3-0) and route every accept site
  of a converted row through it; (b) re-role a site to produce/validate where it honestly produces or validates
  (precedent `finish_exit_gate`, registry :596), and build the predicate only for sites that truly accept a record
  (test_identity, live_check_demand, provenance consumers, baseline_identity); (c) keep accept-site rows on `debt` with
  only the unknown branch declared. **Rec (b)**: smallest honest change, uses the registry's own second clause; the plan
  critic judges each re-role (E-c). Cost of (a) everywhere: a new shared mechanism + 20+ site edits.
- **D-1 — the frame of `bug_file`** (§0.2). (i) keep the state-dir frame and have the reporter write
  `artifacts/<T>/bugs/BUG-n.md` in proposals (text only; breaks with an `artifact_root` outside the state dir, which
  `judge_results.py:274-275` says exists); (ii) `bug_file` is task-root relative, `external_writes` resolves task root
  first then state dir. **Rec (ii)**: one frame for the field the reporter already writes (`bugs/BUG-n.md`), every older
  proposal still resolves (E5).
- **D-3 — does the duplicate check also read OTHER stories' task-root bugs?** (a) yes — keeps the meaning of
  "the project's own bugs" (before OH5-9 every filed bug lived in one folder); (b) no — this story + the project home
  only (critic F8's minimum). **Rec (a)**; cost: more pairs, bounded by the existing `MAX_BUG_PAIRS` (E3).
- **B-1 — where the F-O2 "scenario row" lives.** (a) a row in `test_probe_by_code.py` (keep data_join, "the readers
  take" the records, `test-layers.json:3678`); (b) a `variants.json` row of a recorded story — but the walker has no door
  that runs a probe (`DOORS`, `scenario_walk.py:40`), so (b) needs a new walker door (a mechanism). **Rec (a)**; the
  owner's word said "scenario row" — the Lead confirms the reading.
- **B-2 — C2's world.** (a) the recorded story `cart-1` where the block is reachable, the `BASE` synthetic otherwise,
  named per row; (b) `BASE` everywhere (the existing precedent). **Rec (a)** — the owner accepted "on a real story
  fixture" (spec :520-521).
- **F-C1 — where C3-j asks.** (a) on the gate A card where `check_s5_stand_limits` already runs (`gate_preflight.py:6088`)
  and where `over` already cards — gate A is the gate before S5, so nothing runs on a guess; registry `waits_at: gate_a`;
  (b) a new S5-entry question (the owner's literal "stage entry"), a second place for the same fact (P31 risk).
  **Rec (a)**; the Lead says whether the owner must confirm that gate A satisfies "stage entry".
- **F-C2 — which registry holds the answer.** (a) the environment record (`environment_record.py`, "accept always",
  keyed, FR-7's existing road for stand-gap cards); (b) the project answer registry (`project_knowledge.py`) with a
  stand-scope key holding a measured page load. **Rec (a)**: the existing card -> record -> cover road (P31: one road for
  "do not ask this stand again"); (b) fits only if the person is asked for a NUMBER, which the owner did not say.
- **F-E1 — C5 sample size.** (a) one question each way (the spec's "one conductor call each way"); (b) 2-3 questions of
  different classes each way, still one experiment. **Rec (b)**: one call cannot judge "copes" (the owner's added
  measure).
- **F-L14 — W1 whole** (critic F7 option): a written Lead decision that one code owner satisfies FR-13 for the Level set,
  or a data row (a node). Rec: a node later (FR-13's letter); S1b narrows now.
- **D-2 — `stages.json`/`artifact-writers.json` `project:bugs/`** (§0.2): (a) leave (the guard matches `/bugs/` in any
  path, `guard_pre_tool.py:1049-1052`; the witness may look at the old home); (b) a follow-up node moving the S8 output
  and the reporter's witness to the task-root `bugs/` with every reader of the key (exit_gate `_output_path` :762,
  `brief_pack`, `story_step`, `selftest.py:539`, `test_stages.py`, `dry_exits.py`), after a scout question "what does
  each reader of `project:bugs/` do with a task-root bug?". **Rec (b)** as a separate node after C1 (one road, P31); it is
  outside C1 because the reader set is wide and not read today.

Owner: none new — F-C1 may need her confirmation (Lead's call).

## §7. Small technical choices closed

- C3 grouped by shared functions (forced by `gate_registry.py:833-836`), not one node per gate.
- C2 drops the stale numbers from its docstring rather than updating them.
- C1 adds `"file"` to duplicate entries instead of changing `"bug"` (additive; FR-14).
- S1b re-points K0.15's positive control to the FR-21 row (same filter shape) instead of deleting it.
- DoDs never run slow or quarantined files (builder-rules.md:53-55); they name them "judged by the batch canon".

## §8. Readers of every touched file (rule 7)

Command: Grep over `tools/*.py` for `judge_results|bug_records|external_writes|common-rules|external-writes\.md|templates/test-report|form_selftest|test_controller_doors|gate-registry|environment_record|launch-causes|host_adapter|stage_guard|factory-rules-debt|delivery-verdict-kinds|manifest_put`
-> 28 hits in 6 files; the same names over `.githooks/` -> 0 (positive control: `architecture_gate` found in
`.githooks/commit-msg`, 1 hit); over `.claude/{settings*.json,hooks/**,agents/**}` -> 0 (positive control not run in that
shape: not established).

| touched | reader | verdict |
|---|---|---|
| bug_records.py (C1) | `tools/source_split.py:2810-2821,3028-3033` (splitter knowledge of the module) | unchanged — a new function is additive; if source_split lists functions it is a report line |
| gate-registry.json (C3-*) | `tools/source_split.py:2753-2891`, `tools/test_quarantine.py:2199` | unchanged by row edits (file name unchanged); builder confirms they read the path, not row ids |
| stage_guard.py (S10) | `tools/controller-blocks-gen.py:342` (`stage_guard.dispatch_errors`), `tools/test_collect_intake.py:543` (path pattern of host_adapter) | unchanged (names, not the changed functions) |
| manifest_put.py (FL1) | `tools/controller-blocks-gen.py:138,190-193` (route texts) | changes in FL1 only if a block route text changes |
| factory-rules-debt.md (S1b) | `tools/piles.py:2381` `DEBT_REL`, `tools/test_piles_close_id.py:87-89` | unchanged — spec S1 E3 |
| factory-rules.md (S1b) | `tools/factory_rules_index.py` (spec §5 :460) | unchanged — Check line is not a title |
| controller.py (S9, FL4) | `tools/controller-blocks-gen.py` (spec §5 :471) | changes in S9/FL4 if a block route changes |
| judge_results, external_writes, common-rules, external-writes.md, test-report.md, form_selftest, test_controller_doors, environment_record, launch-causes, host_adapter, delivery-verdict-kinds | none in tools/.githooks/.claude | — |
Package readers (not in rule 7's scope but load-bearing): `external_writes.py` reads `bug_file` (C1 item 4);
`stages.json`/`exit_gate` read `project:bugs/` (D-2); `contract_slices.py --check` reads `common-rules.md` (C1 item 3).

## §9. Reading trail

Read whole: the spec (655 lines); `reviews/t-942-rules-debt-phase1.md`; `references/gate-registry.json` (717 lines).
Read parts: `judge_results.py:1-30,265-362`; `bug_records.py:1-60,128-170` (+ def list); `external_writes.py:640-660`
(+ def list, `state_dir` uses); `exit_gate.py:750-779`; `guard_pre_tool.py:1040-1061`; `common-rules.md:108-121`;
`external-writes.md:38-51`; `templates/test-report.md:28-39`; `form_selftest.py:225-259`; `agents/qa-bug-reporter.md:50-61`;
`test_controller_blocks.py:1-60`; `test_controller_doors.py` (whole); `controller-blocks.md:1-40` (+ Grep counts);
`gate_registry.py:1-110,760-884` (+ `acceptable_in` Grep); `environment_record.py:1-120,130-199` (+ def list);
`project_knowledge.py:1-80`; `gate_preflight.py:795-814,3100-3330,4150-4255,6070-6099`; `stand_gaps.py:1225-1264`;
`driver_runner.py:575-634`; `run_headless.py:1-30`; `conductor_families.py:1-25`; `scenario_walk.py:1-70`;
`stage_guard.py:2500-2594`; `host_adapter.py:440-549`; `test_null_outcomes.py:584-599`; `TESTING.md:36-180`;
`builder-rules.md:36-75`; `slow_tests.json:1-14` (+ Grep); `test-layers.json` (Grep + :1-40, :370-409, :865-903,
:3670-3694, :8295-8314, :8650-8662); `SIBLING_MAP.md` headings; debt file headings.
Greps (negatives with positive controls of the same shape): `def acceptable` (control: `acceptable_provenance` hit);
`gate_template.py` Glob (control: same Glob form on scripts); `variants*.json` Glob (control: `story.json` found by the
same form); `environment registry` (control: "the environment record" found); taken-batch file names (control:
`check_witness`); `.githooks` names (control: `architecture_gate`).

## Not done / not established

- The status cells of the taken-batch rows in §4 (whether they own the files now) — not read; command given.
- Whether a jira-channel proposal already fails "bug_file not found" on a live story (D-1) — by reading only.
- Keep/quarantine status of `test_environment_preparation.py`, `test_baseline_contract.py`, `test_stand_identity.py`
  (slow-listed, keep status not read), `test_contract_slices.py` slowness — commands in C3-f/C3-g.
- Whether `_check_row` accepts a `code` row with empty `words` (C3 S-c) — not read.
- The window reader that counts a `red_sandbox.py --probe` receipt (C4) — the builder names it.
- The capability key in `detectors.json` for FL9 — not established (the spec said the same).
- FL1's function in `manifest_put.py` — not named; designer pass owed.
- `gate-decision` row for C2 — chosen by rule, not named here.
- C3-k (provenance) is not drafted to builder level (designer first).
- The `.claude/` positive control for §8 was not run in the same shape.
