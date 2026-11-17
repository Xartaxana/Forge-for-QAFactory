# Rules-debt phase 2 — dispatch cards (t-954, F19; fix rounds t-994, t-1033)

Designer draft for the Lead. Parent spec: `docs/tasks/specs/20261117-rules-debt-fix-spec.md` (accepted; called "the
spec" below). Owner forks F-O1..F-O6 are decided (the spec's three closing sections, :614-655); Lead forks F-L1..F-L13
are taken as recommended (brief). S7 and S8 are at builders and are not carded here. Owns are repo-relative; in a
worktree dispatch the Lead substitutes the worktree root. Every load-bearing fact below carries the path:line read today
(17.11.2026) in the root checkout, branch `main` (head at session start `58bcfc07` per the git status snapshot; the
phase 1 merge commit was not re-identified by hash); where a fact was not established the line says so and gives the
command.

**Fix round t-994 (17.11.2026).** The C3 section, §3, §4, §5 and the S9/FL2/FL4 cards were rewritten after the plan
critic t-989 (`docs/tasks/specs/reviews/t-989-rules-debt-phase2-wave2-plan.md`) under the Lead's eight decisions of the
t-994 brief. Facts added in this round were read in the root checkout, which IS `origin/main` today: both
`.git/refs/heads/main` and `.git/refs/remotes/origin/main` hold `a6df7fd1a7aa9a203be7ca844db8ab97332e736a` (read
directly), and the git status snapshot shows only `logs/journal/dev1.jsonl` modified. This dispatch had no shell: no
command was RUN here; where a fact rests on a run, the run is the critic's (quoted with its trail) and is marked "not
re-run". The round's ledger is the table «Fix round t-994» at the end; the forks it opens are «Forks returned (t-994)».

**Fix round t-1033 (17.11.2026).** Cards C3-0, C3-b1, C3-b2, C3-d, the new card C3-rr, the B1 lines of C3-g, C3-h, C3-j
and C3-k, the A2 line of C3-k, the C3 shared items (new S-f), the E-c tables, §1, §3, §5, §7, §8 and F-T5 were edited
under the plan critic t-1026 (`docs/tasks/specs/reviews/t-1026-rules-debt-wave2-code-and-cards.md`, findings A1, A2, B1,
B2, B3, B4, B5, B9, B10, "C3-b1 other keys") and the Lead's decision on A1 (option (a)). Facts of this round were read in
the root checkout at `2151eeef9162a16abf5af2e58d6d95e4fc46b569`: `.git/refs/heads/main` and
`.git/refs/remotes/origin/main` both hold it (read directly). No shell in this dispatch either: nothing was RUN; every
run named below is a command for the Lead or the builder, or the critic's run marked "not re-run". In the cards this
round changed, `owns:` and `given:` carry absolute paths under `C:/QAFactory/forge-repo/` (a worktree dispatch
substitutes the worktree root). The round's ledger is «Fix round t-1033» at the end; its forks are «Forks returned
(t-1033)».

## §0. Three facts that change the cards (read before dispatch)

1. **The one predicate the spec names for FR-59 conversions does not exist.** The spec (§2 G-rows, §3 "FR-59 conversion
   nodes") and the debt file say "conversion owed (T2, `gate_template.acceptable`)". `gate_registry.py:837-841` requires
   a converted row's `accept` site to call a function named exactly `acceptable` (`_walk` records any call whose
   name or attribute is `acceptable`, `gate_registry.py:205-237`, the check at :235-237), else finding F-b. A grep for `def acceptable` over
   `ai-packages/qa-factory/scripts/*.py` finds only `profile_contract.py:895 def acceptable_provenance(` (same call
   shape, so the positive control is that very hit); no `gate_template.py` exists (Glob, 0 hits; the same Glob form finds
   other scripts). No converted row of the registry has an `accept` site today (rows read whole,
   `references/gate-registry.json:1-717`): every conversion so far was done by the note's second clause ("its unknown
   branch is pinned by `test`", :3) with sites in produce/validate/dispatch roles (precedent `finish_exit_gate`, :596
   "Registered as a validate site because the site compares no verdict word and calls no acceptable()"). → fork F-D1
   (decided (b), Lead 17.11; the predicate is card C3-0). (t-1033: still true on 2151eeef — Glob
   `ai-packages/qa-factory/scripts/gate_*.py` lists `gate_registry.py`, `gate_shown.py`, `gate_preflight.py`,
   `gate_brief.py`, no `gate_template.py`.)
2. **The bug-file home has a writer-side reader the critic did not list.** `external_writes.py:653`
   (`process_bug_proposal`) resolves a proposal's `bug_file` as `state_dir() / bug_file_rel`, and `record_result`
   (:858) does the same at :893-901. `common-rules.md:116` is exactly the frame rule for that field ("`bug_file` …
   the state directory, `<project>/qa-factory/` — `bugs/BUG-1.md` is `<project>/qa-factory/bugs/BUG-1.md`"). The
   reporter writes `<task root>/bugs/BUG-n.md` (`agents/qa-bug-reporter.md:57`). So aligning :116 to the task root without
   touching `external_writes.py` makes every jira-channel proposal REJECT "bug_file not found" (the refusal text is pinned
   whole at `tests/test_external_writes_bug_refusals.py:122-125`). Whether that already happens on a live story was not
   established by a run (reading only). Also writer-side: `references/stages.json:293` (S8 output `project:bugs/`),
   `:367` (the reporter's witness `project:bugs/`), `references/artifact-writers.json:276`; `exit_gate._output_path`
   resolves `project:` names against `project_root()` (`exit_gate.py:762-763`). → forks D-1, D-2.
3. **Most named tests are SLOW or quarantined.** `scripts/slow_tests.json` lists `test_bug_records.py` (41.5 s),
   `test_check_delivery.py`, `test_execution_request.py`, `test_gate_preflight.py`, `test_gate_registry.py`,
   `test_node_ids.py`, `test_probe_by_code.py`, `test_probe_gap_word.py`, `test_proof_level.py`, `test_s5_precheck.py`,
   `test_stand_identity.py`, `test_window_record.py` (all over the file's `slow_over_s` 10); `builder-rules.md:53-55`
   forbids the builder to run them (and `test_controller_*`): "judged by the batch canon". Quarantined (section
   `quarantine` starts `test-layers.json:7182` on a6df7fd1; `:7207` on 2151eeef, t-1033): `test_judge_results.py`, `test_form_selftest.py`,
   `test_s1_s2_contract.py` (the spec's S1 DoD names it as a reader — it is not run), `test_run_suite_mine.py` (:9674).
   Every DoD below therefore is `scenario_walk.py --witness-for <owns>` + the printed files that are neither slow nor
   quarantined + the named fast CLIs; the slow ones are named "judged by the batch canon". Also slow (read
   `slow_tests.json` t-994): `test_third_verdict.py` (44.5 s, :151), `test_judgment_census.py` (33.3 s, :63). Keep and
   fast (in `keep`, not in `slow_tests.json`): `test_environment_preparation.py`, `test_environment_record.py`,
   `test_baseline_contract.py`.

## §1. Architecture, rules, owners (designer rule 1; package spec)

FR sections by card: C1 B/C/D/E/G; C2 A/G; C3-* A/C/D/E/F; C4 C/D/G; S1b (doc) G (FR-30); S9 A/B/D; S10 A/C/G;
F-L1 D; F-L2 E; F-L4 A/C; F-L9 C/A.

AR-n touched (each card's DoD carries the change check of the AR it names, from `design/architecture.md`): AR-1, AR-9,
AR-13, AR-14, AR-15, AR-18, AR-20, AR-22, AR-23, AR-24, AR-25, AR-28, AR-29. Change checks used by the C3 cards
(`design/architecture.md`): AR-28 :282 "the spec states each new gate read's behaviour on missing, unreadable and empty
input, and a test pins it. A new gate is a registry row with its unknown branch"; AR-29 :155-157 "for every check the
change adds or alters, name its class … and the owner it serves … Run `test_judgment_census.py`; a raised count is named
in the verdict (AR-20)"; AR-13 :166 "grep SIBLING_MAP for the file or fact. If an axis names a survivor, call it"; AR-15
:180 "grep for the problem, not the helper (FR-17), and list every site … A new survivor gets an axis in the same commit".
AR-20 (t-1033, S-f): every pin of `test_gate_registry.py` a card moves (debt / converted / split / D13 count) is named in
the diff with its reason, in the comment form of `test_gate_registry.py:969-986`.

Checks added or altered (AR-29: owner and census class). Census classes are those of
`scripts/tests/fixtures/judgment-census.json` (header :3: shape, xref, word-list, meaning-proxy, meaning, safety; a unit
exists only where the wide scan finds a refusal site — a `.append` to a list never creates one); a row whose class the
builder cannot read from the census test returns a question (spec S6 E1 precedent).

| check | card | owner | census class | blocking |
|---|---|---|---|---|
| `judge_results.run_bugs` duplicate input set (task root + project home [+ other stories, D-3]) | C1 | data (which files are read); the duplicate verdict stays the judge's, advisory | none (advisory hint) | no |
| `external_writes` `bug_file` resolution (task root, then state dir) | C1 on D-1 (ii) | data | shape | refuses a missing file, as today |
| door families executed (test only) | C2 | data | none | no |
| the seven registry rows of C3-R: status, words, roles, branch (no code) | C3-R | data | none (no check unit moves; registry rows are not census units) | unchanged |
| `gate_template.acceptable(value, consumer)` — is this word/record one the consumer may take; `registry_problem()` (on F-T11 (a)) | C3-0 | data (a join between a word and the registry row) | xref, only if a unit exists: the card forbids a refusal site, so no unit is expected | no (a boolean the caller acts on) |
| `reporter_rehearsal_identity` reuse through the predicate (`_reporter_outcome`) | C3-rr (t-1033) | data | none: `_reporter_outcome` has no census row (grep of `judgment-census.json`, control `validate_window` found at :7) and the change adds no refusal site | no (a reuse is refused: the command is rehearsed) |
| `live_check_demand`: a keyless, flagless, unhanded row asks the code critic "is a live probe owed?" at window acceptance | C3-b1 | judgment of `role:qa-code-critic`, accepted at window acceptance (the tier above reads it); code checks only the presence and the closed value of the typed answer | xref (presence of a typed answer); the gap is list transport, no unit; `manifest_put`'s refusal of a value outside {yes, no} sits in an existing rowed function (class unchanged) | yes (waits at window acceptance) |
| `test_identity` accept sites through the predicate (`already_probed`, `_product_receipt_repeat`, `_run_freshness`, `_match`; `_evaluate` on F-T10 (a)) | C3-b2 | data | unchanged (no new unit; none of these functions has a census row — grep, control `validate_window`) | unchanged |
| `s5_window`: the critic's review word accepted through the predicate (`validate_window`, three consumers) | C3-d (t-1033, rec (i) + F-T9 (a)) | data (a join of the critic's word to the row; the review itself stays the critic's judgment, accepted at window acceptance) | unchanged: `validate_window`'s census row is `shape`, owner data (`judgment-census.json:7`); its unit is the `ValueError` at `acceptance.py:1073`; the gaps are list transport | unchanged (a review gap holds, as today) |
| `s5_window` unmeasured detector | C3-d | rec (i): none moves (INFO stays); (ii): judgment of the critic | (i) none; (ii) xref | (i) no; (ii) yes |
| `s5_stand_limits` unmeasured -> card; record cover | C3-j | intent (the person's word, P13) for the answer; data for the cover lookup | xref (a key join, as `environment_property_cover`) | yes (waits at the declared place) |
| no-row probe road reaches acceptance (test only) | C4 | data | none | no |
| window gate reading a person's word for a `review` gap | S9 | intent | xref | lifts a block |
| read heads / reader commands from data | S10 | data | safety | refuses, as today |

Commit lines: every package commit carries `architecture:` and `judgment:` in the form `tools/architecture_gate.py`
accepts (the only carrier of that grammar; not copied here). Each card gives the CONTENT; `judgment: none` always has its
` -- <why>`.

## §2. Cards

Card ids: C1 (item 1), C2 (item 2), C3-R, C3-0, C3-rr (t-1033), C3-b1, C3-b2, C3-d, C3-g, C3-h, C3-j, C3-k (item 3; C3-a, C3-c, C3-e,
C3-f and C3-i are folded into C3-R), C4 (item 4), C5 (item 5), S9, S10, FL1, FL2, FL4, FL9 (item 6), S1b (item 7).

---

### C1 — bug file homes: writer <-> readers (F-O6 (a) follow-up; critic F8 + §0.2)

Dispatchable now on the recommendations of D-1 and D-3 (both returned below); not touching D-2's carriers.

given: `ai-packages/qa-factory/design/factory-rules.md` (whole), `plans/builder-rules.md`, `docs/TESTING.md`; this card;
`docs/tasks/specs/reviews/t-942-rules-debt-phase1.md` (F8); read: `agents/qa-bug-reporter.md:57`,
`scripts/bug_records.py:1-170`, `scripts/judge_results.py:1-30,265-362`, `scripts/external_writes.py:640-660,858-910`,
`scripts/contract_slices.py` (docstring)
owns:
- `ai-packages/qa-factory/scripts/bug_records.py` (module docstring :10-18; one new public function next to `_project_home` :130)
- `ai-packages/qa-factory/scripts/judge_results.py` (`_project_bugs_dir` :273-278 removed, `run_bugs` :315-362, docstring :16)
- `ai-packages/qa-factory/scripts/external_writes.py` (`process_bug_proposal` :653, `record_result` :893-901, docstring :46) — only on D-1 (ii)
- `ai-packages/qa-factory/references/common-rules.md` (the :116 table row only)
- `ai-packages/qa-factory/references/slices/*/common-rules.md` (regenerated by `contract_slices.py --write`, never hand-edited; 10 of the 12 slice files carry the line)
- `ai-packages/qa-factory/references/external-writes.md` (:44, and :49 only if D-1 (i))
- `ai-packages/qa-factory/references/templates/test-report.md` (:35)
- `ai-packages/qa-factory/scripts/form_selftest.py` (:245)
- `ai-packages/qa-factory/scripts/tests/test_bug_records.py` (one table row), `ai-packages/qa-factory/scripts/tests/test_external_writes_bug_refusals.py` (one row, D-1 (ii))
non-goals: `stages.json`, `artifact-writers.json`, `collect-sets.json`, `install-paths.json`, `exit_gate._output_path`
(fork D-2); `agents/qa-bug-reporter.md` (already says the task root); `driver_stage_s8s9.py` (merged phase 1);
`factory_dashboard.py` (S8's owns); `docs/SIBLING_MAP.md` (Lead's commit, text below); `test_judge_results.py` /
`test_form_selftest.py` (quarantined: not run, not edited)
handoff: report path given by the Lead
edges: E1-E8 below
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <every owns path>`; then run the
printed files that are not in `scripts/slow_tests.json` and not in the quarantine — at least
`python -B ai-packages/qa-factory/scripts/tests/test_external_writes_bug_refusals.py` (keep, table) and
`python -B ai-packages/qa-factory/scripts/contract_slices.py --check` (exit 0 after `--write`);
`test_bug_records.py` (slow) is judged by the batch canon, named in the report
siblings: the class "home of a bug file" — sites listed in §0.2 and owns; D-2 carriers (stages.json :293/:367,
artifact-writers.json :276, collect-sets.json :56-57 E5/E6, install-paths.json :40) are queued by fork D-2, not swept
here; `guard_pre_tool.py:1049-1052` matches `/bugs/` in any path — not applicable (home-independent).

Items (test place / expected from per item):
1. `bug_records`: a public function (name builder's choice, e.g. `filed_bug_paths(task_root)`) returning the BUG files a
   duplicate check compares against, in this order: this story's `<task root>/bugs/`, then the project home
   `<project>/qa-factory/bugs/` (through `_project_home`, :130), then — on D-3 (a) — every OTHER story's
   `<artifact root>/<T>/bugs/` (through `hooklib.artifacts_dir`); each home listed with `_listing(dir, BUG_GLOB)` (:140,
   `BUG_GLOB = "*BUG-*.md"` :46); a path met twice (resolved) is returned once. test: one row in `test_bug_records.py`'s
   existing table — a world with task-root `BUG-1.md`, home `BUG-1.md` and `BUG-2.md`, another story's `BUG-1.md`, and
   one empty world. expected from: the owner's word F-O6 (a) (spec closing sections: the reporter writes under the task
   root, the project home is read for older bugs) and critic F8.
2. `judge_results.run_bugs` takes `existing` from item 1 (AR-13: the reader of the bug folders is `bug_records`); delete
   `_project_bugs_dir`; each duplicate entry keeps `"bug": <stem>` and ADDS `"file": <path relative to the state dir>`
   (two homes can each hold `BUG-1`; today meta keys bugs by `bug_path.stem`); the module docstring :16 names the homes.
   test: none of its own — `test_judge_results.py` is quarantined; report line "no keep row drives run_bugs; the read is
   covered by the item-1 row". expected from: as item 1.
3. `common-rules.md:116`: split the row. `bug_file` is relative to the story's task root (`<project>/qa-factory/artifacts/<T>/`
   — `bugs/BUG-1.md` is `<task root>/bugs/BUG-1.md`; an older bug that exists only in the state directory still resolves
   there); `case_file` and other artifact paths keep the state-directory frame. Then
   `python -B ai-packages/qa-factory/scripts/contract_slices.py --write` (if it needs the package as cwd: a Bash
   `( cd <worktree>/ai-packages/qa-factory && python -B scripts/contract_slices.py --write )` subshell). test: the
   slices' `--check` (generator's own ratchet; `test_contract_slices.py` keep table). expected from: F-O6 (a); D-1 (ii).
4. On D-1 (ii): `external_writes` resolves `bug_file` through one module helper used at :653 and :901: the proposal's
   own task root first (a proposal lies at `<task root>/work/proposals/<file>`), then `state_dir()`; absent in both -> the
   existing REJECT text unchanged. test: one row in `test_external_writes_bug_refusals.py` (a proposal
   `bug_file: bugs/BUG-1.md` with the file only under the task root -> no REJECT), red before the change. expected from:
   F-O6 (a) + the frame rule of item 3 (one frame per field).
5. `external-writes.md:44`: "a bug always gets `bugs/BUG-n.md` in the story's own folder (`<task root>/bugs/`)
   regardless of channel"; `templates/test-report.md:35` and `form_selftest.py:245`: "BUG-n — a bug file in the story's
   `bugs/` folder" — the SAME words in both (the second is a copy of the first). test: none (role/template text; FR-37
   judged by reading). expected from: F-O6 (a).
6. `bug_records.py:10-18` docstring: the home the reporter writes is the story's `bugs/` (owner, 17.11.2026, F-O6 (a));
   the project's `qa-factory/bugs/` is read for bugs filed before, the `gate_b_decision_id` rule unchanged. test: none
   (docstring). expected from: F-O6 (a).

For the Lead's commit (not the builder's): `docs/SIBLING_MAP.md` new **Axis 38 — bug file homes: writer <-> readers**
(the last axis today is 37, `SIBLING_MAP.md:628`). Text: "The writer (`qa-bug-reporter`, `<task root>/bugs/BUG-n.md`,
charter `agents/qa-bug-reporter.md:57`) <-> the frame rule (`references/common-rules.md` 'What a path is relative to' +
its slices) <-> the readers that list or resolve a bug file (`bug_records.story_bugs` and the dedup list of C1,
`judge_results.run_bugs`, `external_writes` `bug_file`, `factory_dashboard` task view, `exit_gate` witness through
`stages.json` `project:bugs/`, `collect-sets.json` E5/E6, `install-paths.json`) <-> the texts a person or role reads
(`external-writes.md`, `templates/test-report.md` and its `form_selftest.py` copy). A change to where the reporter writes
changes every reader in one commit (AR-22)."

architecture content: `AR-13 -- the bug folders are read only through bug_records`; `AR-22 -- the bug_file frame has one
producer rule and its readers move with it`; judgment content: `none -- which files a path read lists; the duplicate
decision stays the judge's advisory answer`.

Edges:
- E1 (empty): no bug folder in any home -> `[]` and `run_bugs` sends no duplicate pairs (today `existing = []` when the
  dir is absent). INVARIANT: an absent folder is never an error and never a guess.
- E2 (unreadable): a home that cannot be listed (`_listing` returns its error) is NAMED in the judge's report, never read
  as empty. INVARIANT: FR-59 — an unread home is not "no bugs".
- E3 (limit): `MAX_BUG_PAIRS` is unchanged; with more homes the pairs past the cap are dropped in the order of item 1
  (this story first). INVARIANT: the cap bounds spend; it never drops the current story's own bugs before others'.
- E4 (conflict: same name in two homes): both are compared; `"file"` tells them apart. INVARIANT: no entry is merged or
  hidden by a name clash.
- E5 TEMPORAL: proposals written before C1 carry state-dir-relative `bug_file` values; after C1 they still resolve through
  the state-dir fallback. INVARIANT: no executed or pending proposal becomes unresolvable.
- E6 POSITIONAL: the task root is tried BEFORE the state dir; INVARIANT: a state-dir file of the same name never shadows
  this story's own bug, and a file absent from both is still refused with the unchanged T6 text.
- E7 (conflict D-1 vs D-2): if the Lead takes D-2 (b), that node runs AFTER C1 and C1's frame stays; C1 never edits
  stages.json.
- E8: FR-30 — package text English; slices are generated, so a hand edit of a slice is refused by `--check`.

---

### C2 — the four command-door families as one table (F-O5 (b))

Dispatchable now.

given: factory-rules.md (whole), builder-rules.md, TESTING.md; read: `scripts/tests/test_controller_doors.py` (whole),
`design/controller-blocks.md:1-40` and its `command` rows, the `BASE` helpers the doors test imports
owns: `ai-packages/qa-factory/scripts/tests/test_controller_doors.py`
non-goals: `controller.py`, `design/controller-blocks.md`, `tools/controller-blocks-gen.py`; the other `command` rows;
any new test file
handoff: report path given by the Lead
edges: E1-E6 below
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/tests/test_controller_doors.py`;
the file itself is a `test_controller_*` file (builder-rules.md:54): judged by the batch canon, named in the report;
commit carries a `tests-over:` line if the volume gate asks (test-only diff; reason "F-O5 (b), the owner's word")
siblings: `test_controller_blocks.py` (route map) — not applicable (it does not execute doors); the stale numbers in the
docstring (:4 "189 … 109"; the walk says 353 blocks, `command` 221, `controller-blocks.md:3,21`) — applied: the
docstring drops the numbers

Items:
1. Replace the one-family block (:93-135) by ONE parameterised table `DOOR_FAMILIES`, one row per family, id = the family
   name (P16: the red line names the family): `checkpoint`, `gate-decision`, `semantic_reopen`, `recover`. Each row:
   the world setup, the blocked request, the block's text NEEDLE taken from its `controller-blocks.md` row, the door call,
   and the after-check (the same request goes through, or the state the door leaves). Each row runs on its own copy of
   the world.
2. Rows (counts of `command` rows naming the family in `controller-blocks.md`, Grep today: checkpoint 9, gate-decision 23,
   semantic_reopen 7, recover 11):
   - `checkpoint`: the existing case, moved unchanged ("checkpoint active work before revising scope", :155).
   - `semantic_reopen`: "semantic content changed; use semantic_reopen" (:165) — after `--operation semantic_reopen` the
     refused request goes through.
   - `recover`: `refresh_derived` `DerivedViewStale` (:140) — after `--operation recover` the view is fresh AND the
     committed event count is unchanged (the action is NOT repeated).
   - `gate-decision`: the first row in source order of `controller-blocks.md` whose route names `gate-decision` and whose
     block the world of item 3 can reach (the builder names the row; `rg -n "gate-decision"
     ai-packages/qa-factory/design/controller-blocks.md` lists them).
   test: the table itself. expected from: the owner's word F-O5 (b) and each row's own "way through" cell in
   `controller-blocks.md`, never the controller's output.
3. World: per fork B-2 — recommended: a copy of the recorded story `fixtures/stories/cart-1/` (its
   `state/controller.json` exists) where that family's block is reachable from the recorded state; otherwise the `BASE`
   synthetic world of the existing checkpoint case, and the report says which row uses which.
architecture content: `AR-9 -- every refusal names a door its receiver can use; four families now proven by executing the
door`; judgment content: `none -- a test of existing doors, no check moves`.

Edges:
- E1: a door that does NOT open is a found defect: the builder keeps the row out of the commit and returns the refusal
  text + row as a question (the Lead opens a fix node). INVARIANT: a door is never asserted open by reading, and the canon
  never carries a red row on purpose.
- E2: the needle is block text, never a line number. INVARIANT: lines move, the needle does not.
- E3 (empty): if the walk holds no row for a family, the table row fails naming the family. INVARIANT: a family silently
  missing is never green.
- E4: `recover` must not repeat the committed action — the after-check counts events.
- E5: environment hygiene as the existing case (`CLAUDE_PROJECT_DIR` and `hooklib._PROJECT_ROOT_CACHE` restored in
  `finally`) for every row.
- E6: the existing checks of `main` before :93 stay as they are.

---

### C3 — FR-59 conversion cards (F-O1, decided whole; fix rounds t-994, t-1033)

Every C3 card needs the PLAN CRITIC before code (spec §7, "each FR-59 conversion"); the plan critic of the topic is
t-989 (R13-g: one pass per topic). C3-R is dispatchable after the Lead accepts this round; C3-0, C3-b1 and C3-d carry
open forks of «Forks returned (t-994)»; C3-b2, C3-g, C3-h, C3-j and C3-k are wave 3. (t-1033: C3-R merged as `5751426c`;
its row `reporter_rehearsal_identity` goes back to debt in the fix round t-1032 (critic t-1026 A1, Lead option (a)), and
its conversion is the new card C3-rr, wave 3. The second plan critic of the topic is t-1026.)

Shared items of every C3 card (each card adds its own):
- S-a. The gate's unknown branch behaves as the decided branch (table below). Where code already does it, no code moves.
- S-b. One row in the registry row's `test` file pins the unknown branch: an input that yields the unknown class -> the
  declared outcome (the question asked and the stage waits / the rerun / the refusal with its door), never a pass. It is
  the registry's requirement for `converted` (`gate-registry.json:3`). Where such a pin already exists, it is NAMED in the
  report and no new row is written (the card says which).
- S-c. Registry row: `status: converted`, `debt_ref: ""`, the decided `unknown_branch` / `on_no_answer` / `waits_at`,
  `vocabulary: code`; every `accept` site resolved per F-D1 (b) and the E-c table. `words` = the outcome words the row's
  code writes for each class, as they appear in the code: the literal verdict words the sites compare
  (`python -B ai-packages/qa-factory/scripts/gate_registry.py --sites`, the row's files), and when the sites compare
  none, the words the row's own functions return or write for matched / mismatched / unknown (precedents:
  `inputs_unchanged` `["inconclusive"]`, `finish_exit_gate`). Each word gets a `verdict_map` entry, and the unknown-class
  word carries its `owner`. `words` is never empty: `_check_row` refuses an empty list on any non-exempt row
  (`gate_registry.py:524-526`). The per-card words are given in the card. (t-994: three rows' as-written words are not all
  written by the code — fork F-T6.)
- S-d. The debt file is NOT edited (S1b moves the row after acceptance).
- S-e. A card that adds or changes a check unit in `scripts/*.py` owns
  `ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json` (its own rows only, class per the §1 table) and is
  based on `main` after `wave-a/integrate` lands (that branch edits the same file). A card that moves no code does not
  touch the census. (t-1033: `wave-a/integrate` is merged — `71d36190 wave: merge wave-a/integrate (t-993)`, the critic's
  `git log origin/main --grep=wave-a` run in t-1026, not re-run here — so the order is satisfied for every card based on
  today's main.)
- S-f (t-1033, critic t-1026 B1). **The pins of `ai-packages/qa-factory/scripts/tests/test_gate_registry.py` move with
  every conversion.** Every converting card owns that file for ITS OWN ROW'S pins only (line numbers read on 2151eeef):
  `EXPECTED_DEBT` (:57-60: the row's id leaves), `EXPECTED_CONVERTED` (:63-68: the id joins), the K-T1.2 text
  `"N gate(s) left as debt:"` (:246: N-1), the K-T1.14 debt list (:322: it reads `EXPECTED_DEBT`, no edit of its own) and
  the split pin (:331-334: converted +1, debt -1, with its AR-20 comment line naming the card and task), the F4 `code`
  list (:729-738: the id joins only when the row's `vocabulary` turns `target` -> `code`), and `D13_TRIPLES` /
  `D13_ITEM_COUNT` (:907-987). Item of every converting card: **"re-measure D13 with `GR.analyse(PLUGIN_ROOT)` before
  and after the change (the set of `(file, function, row)` triples and `len(items)`), and name every added or removed
  triple and the count's move in a comment line in the form of :969-986 (`N -> M (<card>, <task>): <which comparisons
  in which site>`)"**. Expected values come from the status rule (one row moves from debt to converted) and from the list
  of comparisons the card adds to or removes from its sites; the D13 count is the one pin whose new value is a
  measurement, and its reason is that list, never the scanner's number alone. The consumer pins F1 (:627-647) and
  K-N2.12 NEG (:285-292) move only in C3-g (`provenance.baseline`) and C3-k (`provenance.environment_preparation`).
  The F4 flip control (:751-754) flips the live debt row `s5_window`; C3-0 moves it onto an in-memory copy row (C3-0
  item 7), so it survives the conversion of the last `target` debt row.
  TEMPORAL, both worlds. The numbers a card applies are DELTAS from the main it is based on, never absolute.

  Main at t-1043:
  - t-1032 is merged (critic t-1039: `7f2f6f78`). Its pins are on main: `test_gate_registry.py:55-61`, :247 "8", :334-336 (19 converted / 8 debt / 6 exempt), :930-932 (the triples `_record_unreadable` and `_reporter_outcome`), :991-994 (`D13_ITEM_COUNT = 140`).
  - C3-0 (t-1038) is not on main yet (Glob: no `gate_template.py` on the root). On its branch `worktree-agent-aa11322709a274e56` (a4aca646) it moves only D13:
    - `D13_TRIPLES` gains `("gate_template.py", "acceptable", "provenance_acceptance")`;
    - `D13_ITEM_COUNT` goes 140 -> 146: six comparisons of `acceptable`, the two `not_applicable` ones included (`test_gate_registry.py:1003-1006` there).

  So every converting card is based on main AFTER C3-0 merges, and its D13 base is 146 plus whatever merged in between.

  Main line numbers (t-1043): EXPECTED_DEBT :58-61, EXPECTED_CONVERTED :64-69, K-T1.2 :247, split :334-336, F4 flip :753-756 (C3-0 rewrites it; :760 on its branch), D13 :913-994. The F4 `code` list (:729-738) and K-T1.14 (:322) were not re-read. A card whose
  base predates a sibling's merge merges main into its tree (D-0048), re-derives every pin of its own row from the
  merged state, re-measures D13 on the merged tree, and never resolves a conflict by keeping either side's number.
  INVARIANT: the pins always equal the live registry (K-T1.14 compares them to the file, :329-336) — no merge lands with
  another card's row reverted in a pin, and no card's diff edits another row's pin.
  Expected merge order on the file (from the dependencies; the binding rule is D-0048's, above): t-1032 -> C3-0 -> C3-rr
  -> C3-b1 -> C3-b2 -> C3-g -> C3-d -> C3-j -> C3-k -> C3-h.
- DoD of every C3 card: `scenario_walk.py --witness-for <owns>`, `python -B ai-packages/qa-factory/scripts/gate_registry.py --check`
  (exit 0, and the row's id is absent from the `N gate(s) left as debt:` block that `--check` prints — the block is
  printed by `gate_registry.py:968-971`), the printed non-slow files; the row's `test` and `test_gate_registry.py` are
  slow (§0.3) — judged by the batch canon.
- Edges common to C3: E-a TEMPORAL — stories in flight that recorded the old outcome are not rewritten; the new branch
  applies from the next gate run. INVARIANT: no recorded verdict changes meaning after the fact. E-b — the unknown is
  never turned into a pass (AR-28: each new gate read's behaviour on missing, unreadable and empty input is stated and
  pinned). E-c — a site re-roled under F-D1 (b) is re-roled only when the function produces or validates rather than
  accepts a record; the plan critic judged each one (table "Re-roles judged by the plan critic (E-c)" below).
  INVARIANT: a re-role never hides a literal acceptance. E-d — `gate-registry.json` is shared by all C3 cards and S7
  (`witness_backstop` row): each card edits ONLY its own rows; later merges resolve (row-disjoint, the D-0048 form
  applied to rows). E-e (t-1033) — `test_gate_registry.py` is shared by every converting card: S-f.
- architecture content (every C3): `AR-28 -- the unknown branch is declared and pinned by the row's test`; `AR-29 --
  <class> unchanged / changed as the §1 table says`; `AR-20 -- the registry pins move by the named delta, D13 re-measured`
  (t-1033, S-f); judgment `none -- <why>` only where the table says owner data and nothing moves into judgment.

Decided branches (registry today -> after):

| card | gate (registry line) | unknown_branch now | after (decided) | true accept sites after E-c |
|---|---|---|---|---|
| C3-h | stand_identity (:35) | question / wait / stage_entry | keep | none |
| C3-k | provenance_acceptance (:91) | question / wait / stage_entry | keep | designer (C3-k) |
| C3-b2 | test_identity (:148) | rerun | keep | `already_probed`, `_match`, `green_over_same_bytes` (t-994: fork F-T1 on the last two); t-1033 (B4): + `_product_receipt_repeat`, `_run_freshness`; `_evaluate` on F-T10 |
| C3-R (was C3-a) | collected_ids (:170) | **debt** | **rerun** (owner) | none (validate) |
| C3-b1 | live_check_demand (:208) | **debt** | **question / wait / window_acceptance, addressee role:qa-code-critic** | none |
| C3-R (was C3-c) | s5_coverage (:229) | question / wait / window_acceptance | keep | none |
| C3-d | s5_window (:251) | question / wait / window_acceptance | keep (t-994: fork F-T7) | t-1033 (B3): `acceptance.validate_window` (the critic's review word) |
| C3-R (was C3-e) | delivery (:274) | **debt** | **refuse_with_door** (a kind not in the kinds file -> `no`, the kind named as a factory defect, FR-19) | none |
| C3-R (was C3-i) | case_preconditions (:314) | question / wait / gate_a | keep | none |
| C3-R (was C3-f) | environment_preparation (:336) | question / wait / authorization | **refuse_with_door** (Lead, 17.11.2026, по рекомендации критика, до слова владельца) | none |
| C3-g | baseline_identity (:358) | refuse_with_door | keep | `deployment_readiness` (t-994: fork F-T3) |
| C3-j | s5_stand_limits (:501) | **debt** | **question; the person's answer persisted in the environment record** (owner) | none |
| C3-R (was C3-i) -> t-1032 debt -> C3-rr | reporter_rehearsal_identity (:524) | rerun | keep | t-1033 (A1): `gate_preflight._reporter_outcome` |
| C3-R (was C3-i) | environment_property_cover (:547) | question / wait / gate_a | keep | none |

(Line numbers = the 14 rows' `status: debt` lines in `gate-registry.json`; re-read on a6df7fd1 for the rows of C3-R,
C3-0, C3-b and C3-g: :148, :170, :208, :229, :251, :274, :314, :336, :358, :524, :547 hold. On 2151eeef, after C3-R,
the rows' `status` lines are test_identity :148, live_check_demand :206, s5_window :247, baseline_identity :353,
s5_stand_limits :496, reporter_rehearsal_identity :520 — read t-1033.)

Re-roles judged by the plan critic (E-c) — t-989 F-S5, applied as written (Lead decision 1). The column "t-994 read" is
this round's check of the critic's reading on a6df7fd1; where it disagrees, the disagreement is a returned fork, not an
edit of the critic's judgment. The rows marked t-1033 are the plan critic t-1026's corrections (A1, B3, B4) and their
class sweep, read on 2151eeef.

| row | site | today | judgment | why (critic) | t-994 read |
|---|---|---|---|---|---|
| test_identity | `proof_level.same_test` (:850) | accept | **produce** | it RETURNS the row's words (`raw`/`instance`/`instance_code`/`file_code`/`""`); it consumes none | holds (`proof_level.py:850-892`) |
| test_identity | `proof_level.already_probed` (:1404) | accept | **true accept** | compares `hit['holds'] in ('instance_code','file_code')` (:1520): it consumes the word to reuse a probe | holds, with a nuance: the reuse ACCEPTANCE is the truthiness of `same_test(...)` at :1492 and :1507 (any non-empty word); the comparison at :1520 only picks the words shown (`held_words`). C3-b2 allow-lists :1520 and routes :1492/:1507 through the predicate |
| test_identity | `execution_request._match` (:2078), `green_over_same_bytes` (:2169) | accept | **true accept** | they decide whether an old job or green is reused for this request | the decision holds, but neither consumes a word of this row: `_match` calls `same_instance_bytes` (:2099-2101), which compares `proof_level.compare_identity(...)[0] == "same"` (:2065-2075, vocabulary same/different/unknown); `green_over_same_bytes` reads identity only through `covered` -> `_match` (:2182-2183) and compares `execution_status == "passed"` → fork F-T1 |
| test_identity (t-1033, B4) | `proof_level._product_receipt_repeat` (:1365; the test :1378-1379) | not registered | **true accept** | the reuse of a product receipt by the truthiness of `same_test(now, proof_identity(record))`, the shape of :1492/:1507; called from `already_probed` :1514 | t-1033: holds (`proof_level.py:1365-1401`) |
| test_identity (t-1033, B4) | `proof_level._run_freshness` (:924; the test :939) | not registered | **true accept** (designer's choice on the critic's recommendation, §7) | `same_test(...) in ("instance", "instance_code")` decides whether a run row still speaks for the test (`fresh`) | t-1033: at :939 both sides carry a kept per-test identity (`now` checked at :932; `bound` holds only `instance_identity` built from `run_identity`, which requires both shas, :911-921), so `same_test` decides by its rule 1 and returns only `instance`, `instance_code` or `""` (:878-883): routing through a `["matched"]` consumer accepts exactly what the literal accepts |
| test_identity (t-1033, class sweep, F-T10) | `proof_level._evaluate` (:1580; :1604-1605), `holds_over_comments` (:1552; :1562), `_stale_receipt` (:1886; :1898) | not registered | `_evaluate`: true accept (a receipt counts by the truthiness of `same_test`); `_stale_receipt`: produce (a why); `holds_over_comments`: no production caller (grep `holds_over_comments\(` over `scripts/`: the def and `tests/test_proof_level.py:1499-1500` only) | not judged by a critic → fork F-T10 | t-1033 read only |
| live_check_demand | `proof_level.proof_required` (:467) | accept | **produce** | it produces the demand (flags, `_NOVELTY_DEMANDS` membership, handed) and accepts no record | holds (`proof_level.py:467-483`) |
| s5_coverage | `s5_precheck.run` (:4598) | accept | **validate** | it produces findings and `unchecked[]` over the author's artifacts; no verdict word is compared | holds (`s5_precheck.py:4598`, return :4736-4739: `ok`, findings, `unchecked`) |
| delivery | `delivery_verdict.decide` (:119) | accept | **produce** | it computes the word | not re-read |
| delivery | `check_delivery.assess` (:2558) | accept | **produce** | it FINALISES the word and writes `delivery_verdict`; its `in ('no', None)` reads go through `DV.verdict_of_kind` and err toward `no` | not re-read |
| delivery | `check_delivery.ledger_reasons` (:1740) | accept | **produce** | it returns the texts of the blocking ledger records | not re-read |
| baseline_identity | `baseline_contract.deployment_readiness` (:175) | accept | **true accept** | it accepts `provenance.baseline` receipts (registry `accepts`) | it accepts BASELINE RECEIPTS by `status == "captured"` + revision, gate ref and file-hash equalities (`baseline_contract.py:185-214`); it reads no provenance word and no registry entry; the consumer id `provenance.baseline` is read by no `scripts/*.py` (grep `provenance\.baseline` over `scripts/`: hits only in `tests/test_gate_registry.py:284-288,626,635`; positive control: the same grep found `"captured"` at `baseline_contract.py:134,199`) → fork F-T3 |
| reporter_rehearsal_identity + environment_property_cover | `gate_preflight._rehearse_reporter` (:3577) | accept (two rows) | **validate**, under `reporter_rehearsal_identity` only | the reuse decision is a key join; no verdict word is compared | not re-read. t-1033: the critic withdrew the reasoning (t-1026 A1): the reuse decision is in the extracted `_reporter_outcome`; `_rehearse_reporter` stays `validate` (its `countable['state'] == 'none'` is `report_adapt.countable`'s vocabulary, `gate_preflight.py:3876-3880`, a coincidence of the word) |
| reporter_rehearsal_identity (t-1033, A1) | `gate_preflight._reporter_outcome` (:3824; the test :3843) | not registered (t-1032 registers it `accept`) | **true accept** | `earlier["state"] == "same_command"` consumes the row's word to reuse a proof | t-1033: holds (`gate_preflight.py:3836-3851`); C3-rr routes it through the predicate |
| reporter_rehearsal_identity (t-1033, A1) | `gate_preflight._record_unreadable` (:3966; :3969) | not registered (t-1032 registers it `produce`) | **produce** | it returns the tail of a sentence for the `unreadable` state | t-1033: holds (`gate_preflight.py:3965-3971`) |
| reporter_rehearsal_identity | `driver_gates.hand_to_conductor` (:1024) | accept | **dispatch** | it hands the state to the conductor | not re-read |
| environment_property_cover | `gate_preflight.check_case_preconditions` (:5460) | accept (+ dispatch under case_preconditions) | **drop from this row** | it stays only under `case_preconditions` (dispatch) | registry :293 (dispatch under case_preconditions) and :531 (accept here) hold |
| environment_property_cover | `gate_preflight._environment_cover` (:4214) | not registered | **validate** (new registration) | it holds the whole gate A cover decision | `_environment_cover` is a method of `Rehearsal` (a26 keys a method by its bare name, `gate_registry.py:206-207`); uniqueness of the name in the file is checked by `--check` (F-e) |
| environment_property_cover | `stand_gaps.gate_b_split` (:962) | accept | **validate** | the gate B cover is a key join | not re-read |
| s5_stand_limits | `gate_preflight.check_s5_stand_limits` (:3165) | accept | **produce** | it measures and cards; it accepts no record | not re-read |
| s5_window | `acceptance.validate_window`, `window_record.verdict` | accept | not judged here | C3-d is unfit (F-d1) | C3-d below |
| s5_window (t-1033, B3) | `acceptance.validate_window` (:1052; :1156, :1161, :1167, :1171) | accept | **true accept — stays `accept`** | it accepts the critic's review word to close a review (`!= "approved"` :1171, `not in HANDED_REVIEW_VERDICTS` :1161, `!= BLOCKED_REVIEW_VERDICT` :1156/:1167); a `validate` role would allow these silently (`gate_registry.py:37-41`) | t-1033: holds (`acceptance.py:1154-1174`, :33-34, :42-44) |
| s5_window (t-1033, B3) | `window_record.verdict` (:1816) | accept | **produce** | it builds the problem lines and `info` | t-1033: holds (`window_record.py:1816-1913`) |
| s5_window (t-1033, class sweep) | `window_record.build` (:1332; :1532 `item["review"]["verdict"] != "approved"`) | not registered | **produce** (new registration in C3-d) | it writes the review NOTE (the door text), not an acceptance | t-1033 read; the comparison at :1524/:1625 uses the imported `BLOCKED_REVIEW_VERDICT` (invisible to A26, docstring :63-66) |

Result (critic): under (b) the predicate is needed for exactly **test_identity** (three sites), **baseline_identity**
(one) and **provenance_acceptance** (C3-k). Every other row converts with no `acceptable()` call. (t-994: forks F-T1 and
F-T3 ask the Lead whether two of those four sites need the predicate in the form decided.) (t-1033, critic t-1026: the
list grows by **reporter_rehearsal_identity** (`_reporter_outcome`, C3-rr), **s5_window** (`validate_window`, C3-d) and
two more test_identity sites (`_product_receipt_repeat`, `_run_freshness`, C3-b2; `_evaluate` on F-T10).)

#### C3-R — registry conversions with no code (C3-a + C3-c + C3-e + C3-f + C3-i; F-K7, Lead decision 2) — wave 2, one builder node

given: `ai-packages/qa-factory/design/factory-rules.md` (whole), `plans/builder-rules.md`, `docs/TESTING.md`; this card
and the C3 shared items above; `docs/tasks/specs/reviews/t-989-rules-debt-phase2-wave2-plan.md` (F-a1, F-a2, F-c1, F-e1,
F-e2, F-f1, F-f2, F-i1, F-i2); read: `references/gate-registry.json` (the seven rows: :150-171, :210-230, :253-275,
:288-315, :316-337, :503-525, :526-548), `scripts/gate_registry.py` (:485-681 `_check_row`, :786-912 `analyse`),
`scripts/run_suite.py:30-45,1673-1674,1736-1753`, `scripts/delivery_verdict.py:40-150`,
`scripts/environment_preparation.py:40-135,440-470`, `scripts/onboarding_probe.py:375-395`,
`scripts/environment_record.py:133-199,275-310`, `scripts/gate_preflight.py:4195-4250`,
`scripts/tests/test_run_suite_mine.py:1700-1746` (quarantined: read for its world only)
owns:
- `ai-packages/qa-factory/references/gate-registry.json` (rows `collected_ids`, `s5_coverage`, `delivery`, `case_preconditions`, `environment_preparation`, `reporter_rehearsal_identity`, `environment_property_cover` only)
- `ai-packages/qa-factory/scripts/tests/test_node_ids.py` (one row)
- `ai-packages/qa-factory/scripts/tests/test_third_verdict.py` (one row)
- `ai-packages/qa-factory/scripts/tests/test_gate_preflight.py` (one row, only if the builder's grep finds no pin of the rehearsal unknown, item 7)
non-goals: any `scripts/*.py` outside `scripts/tests/` (a code edit of any site is OUT of C3-R); `judgment-census.json`
(no code moves, S-e); `test-layers.json` (no new test file); the debt file (S-d); `plans/BACKLOG.md` (frozen; B-ids go to
the integrator); the other seven debt rows; `test_gate_registry.py` (item 9 says what to do if it pins a converted row);
`test_run_suite_mine.py` (quarantined: not run, not edited)
handoff: report path given by the Lead
edges: E1-E9 below
DoD: `python -B ai-packages/qa-factory/scripts/gate_registry.py --check` exits 0 and none of the seven ids appears in the
`N gate(s) left as debt:` block (14 before, 7 after); then
`python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/references/gate-registry.json ai-packages/qa-factory/scripts/tests/test_node_ids.py ai-packages/qa-factory/scripts/tests/test_third_verdict.py ai-packages/qa-factory/scripts/tests/test_gate_preflight.py`
and the printed files that are neither slow nor quarantined — at least
`python -B ai-packages/qa-factory/scripts/tests/test_environment_preparation.py` and
`python -B ai-packages/qa-factory/scripts/tests/test_environment_record.py` (keep, fast); `test_node_ids.py`,
`test_third_verdict.py`, `test_s5_precheck.py`, `test_gate_preflight.py` and `test_gate_registry.py` are slow — judged
by the batch canon, named in the report
siblings: axis 4 (rules <-> debt <-> backlog): the report lists the B-ids for S1b and the integrator — B-278
(collected_ids), B-221 (s5_coverage), B-061 (delivery), B-280 (case_preconditions), B-283 (reporter_rehearsal_identity
and environment_property_cover, one id for two rows), and B-255 for environment_preparation **with the line "B-255 stays
open: provenance_acceptance still carries it"**; axis 32 (census): n/a — no code moves; the five folded cards' siblings
are their rows only
designer: `C:\QAFactory\forge-repo\docs\tasks\specs\20261117-rules-debt-phase2-cards-spec.md` (this file, C3-R, after the Lead accepts t-994)

Items (one per row; test place / expected from per item):
1. **collected_ids** (was C3-a; B-278). Row edit: `vocabulary: code`, `words: ["node_id_mismatch"]`,
   `verdict_map: {"node_id_mismatch": {"class": "mismatched"}}`, `unknown_branch: rerun`, `on_no_answer: rerun`,
   `waits_at: null`, `closed_by: []`, sites keep `validate`, `status: converted`, `debt_ref: ""`, and the `decides` text
   loses its closing "(residue, B-278: the template has no unknown branch)". Why one word (closed t-994 by the critic's
   own fallback, F-a2): the code writes no `not_verified` token — `run_suite.py:1673-1674` defines `_not_verified(reason)`
   and writes the prose note "node ids were not verified: …" (also :1743, :1753, :1791); `NODE_ID_BLOCK =
   "node_id_mismatch"` is the token (:1539). S-b row in `test_node_ids.py`: the world of `test_run_suite_mine.py` M-B3
   (:1744, a quarantined file, read for its world only, not edited): an unreadable collect, then pytest's exit 4 -> the
   summary says `node_id_mismatch`, `execution_status: not_executed`, never passed or failed, and the ids are named "not
   verified", never "missing". expected from: the row's `decides` (registry :152) and the owner's «да» (F-O1).
   `run_suite.py` is not in owns: if the row is red on real code, the node stops with the red output.
2. **s5_coverage** (was C3-c; B-221). No code moves and no new test row: S-b is `test_s5_precheck.py` K-C4 (:843). Row
   edit (as written, F-c1; fork F-T6 asks to change the words): `vocabulary: code`,
   `words: ["matched", "mismatched", "unchecked"]`, with `unchecked` -> `{"class": "unknown", "owner": "role"}`;
   `s5_precheck.run` re-roled `validate`. The branch stays question / wait / window_acceptance; the window's wait is the
   instance's `review` gap, which stays until the critic records `critic_verdict`. expected from: the registry row and
   K-C4's own expected values.
3. **delivery** (was C3-e; B-061). No code moves: `delivery_verdict.decide` (:119-145) already answers an unknown kind and
   an unreadable file with `no` and a `factory`-owned finding. Row edit: `vocabulary: code` (the words `yes`,
   `after_checks`, `no` are the code's), `unknown_branch: refuse_with_door`, `on_no_answer: refuse_with_door`,
   `test: scripts/tests/test_third_verdict.py` (it pins the unknown kind, :190), the three sites re-roled `produce` (E-c
   table), `addressee: []` stays: the door is the factory's own (the finding text names the kinds file); no person is
   asked (FR-3). S-b row added to `test_third_verdict.py`: an unreadable / empty kinds file ->
   `("no", [VERDICT_KINDS_UNREADABLE])`, never `yes` or `after_checks`. expected from: the row's `decides` (registry :255)
   and FR-19 ("an unrecognised reason is a defect of the classifier").
4. **environment_preparation** (was C3-f; B-255 shared). No code moves. The unknown is an unknown compatibility fact or an
   unidentified existing runtime; the code refuses it as `blocked` with the missing facts named (exit 2): `_facts` raises
   `PreparationError("unknown compatibility facts: …")` (`environment_preparation.py:51,60`), the plan returns
   `{"status": "blocked", …}` (:102-171), `execute_environment` turns refusals into `blocked` (:444-469). Row edit (Lead
   decision 3: the registry is brought to what the code does; FR-59's "declared safe default, never a pass" is kept by the
   refusal — Lead, 17.11.2026, по рекомендации критика, до слова владельца): `vocabulary: code`,
   `words: ["blocked", "unknown"]`, `verdict_map: {"blocked": {"class": "unknown", "owner": "environment"}, "unknown":
   {"class": "unknown", "owner": "environment"}}`, `unknown_branch: refuse_with_door`, `on_no_answer: refuse_with_door`,
   `waits_at: null`, `closed_by: []`; `addressee` and `person_subject` unchanged (small choice: the person still supplies the
   missing facts through the door the refusal names); `accepts` unchanged. S-b = the existing
   `test_environment_preparation.py::test_unknown_compatibility_never_selects_rebuild` (:81; also
   `test_unknown_outcome_blocks_instead_of_relaunch` :133) — named, no new row. `test_environment_preparation.py` and
   `test_baseline_contract.py` are keep and fast: run them in the DoD. expected from: the code's own refusal and FR-59.
5. **case_preconditions** (was C3-i; B-280). Row edit: `status: converted`, `debt_ref: ""`; words unchanged (already
   `code`: `met/unmet/uncheckable/error/seeded`, registry :300); sites unchanged (`check_case_preconditions` stays
   `dispatch` here, :293). S-b: the existing `uncheckable` rows of `test_gate_preflight.py` (5 hits, critic grep; not
   re-run) — named.
6. **environment_property_cover** (was C3-i; B-283). Registrations after the change: `gate_preflight._environment_cover`
   (validate, new) and `stand_gaps.gate_b_split` (validate); `_rehearse_reporter` and `check_case_preconditions` are
   removed from this row. Words (as written, F-i1; fork F-T6 asks to change them): `["covered", "changed_since",
   "not_covered", "unreadable"]`, `covered` -> matched, `changed_since` -> mismatched, `not_covered` and `unreadable` ->
   unknown (owner environment). Status converted, `test` stays `scripts/tests/test_environment_record.py`. S-b: the existing
   pins E9 and E14 of `test_environment_record.py` (:3-5, :113; unreadable / revoked record) — named.
7. **reporter_rehearsal_identity** (was C3-i; B-283). Registrations: `_rehearse_reporter` (validate), `_read_probe_report`
   (measure), `driver_gates.hand_to_conductor` (dispatch). Words (as written, F-i1; fork F-T6): `["reused", "rehearsed",
   "none", "command_changed", "unreadable"]`, `reused` -> matched, `rehearsed` -> mismatched, `none`, `command_changed`,
   `unreadable` -> unknown (owner environment). S-b: write ONE new row in `test_gate_preflight.py` for this row's unknown
   (a record with no row of this command -> the command is rehearsed again, nothing reused), expected from the row's
   `decides` (registry :505, "`unknown`: no row of this command … nothing is reused: the command is rehearsed again"),
   unless the builder's grep finds it pinned (the critic's grep of `command_changed` in `test_gate_preflight.py` found 0,
   control `uncheckable` 5 — not re-run).
8. After items 5-7 no function is registered by two rows (the "registered more than once" finding,
   `gate_registry.py:833-836`); `--check` proves it.
9. Before the commit the builder greps `scripts/tests/test_gate_registry.py` for the seven ids and for a pinned debt count
   (`14`); a hit that pins a converted row as `debt` or the count is OUT of owns: the node stops and returns the hit as a
   question (the Lead adds the row or queues it); no hit -> one report line with the grep and its positive control.

architecture content: `AR-28 -- the seven unknown branches are declared and pinned by each row's test`; `AR-29 -- no
check unit moves; registry rows only`; judgment `none -- registry status, words and roles; every gate decides as today`.

Edges:
- E1 TEMPORAL: the registry is read by the audit (`gate_registry.py`) and by forge tools (§8), not by any gate at run time
  today (no `acceptable()` exists, §0.1); stories in flight see no behaviour change. INVARIANT: no recorded verdict changes
  meaning (E-a).
- E2 (stop rule): a pin red on real code stops the node with the red output; no site is edited to make it green (the C4
  precedent). INVARIANT: a converted row never claims a branch the code does not take.
- E3 (empty): a row's `words` is never empty (`_check_row` :524-526); `--check` exit 1 on a schema finding stops the node
  with the finding text. INVARIANT: no row is committed red.
- E4 (conflict, E-d): S7 may edit `witness_backstop`; C3-0 adds one site line to `provenance_acceptance`; both are other
  rows. INVARIANT: C3-R's diff touches only its seven rows.
- E5 (words, F-T6): the as-written words of items 2, 6, 7 pass `_check_row` (it does not read the code) but are partly not
  written by the code; until the Lead answers F-T6 the card executes as written. INVARIANT: whatever the answer, every
  word has a `verdict_map` entry and every unknown-class word an owner.
- E6 (FR-3): no row of C3-R gains `person` as an addressee where its only unknown owner is `factory` (`_check_row`
  :628-633). INVARIANT: our own defects are reported, never asked.
- E7 (B-255): converting `environment_preparation` never closes B-255. INVARIANT: an open backlog row stays open while a
  row still names it (provenance_acceptance :91).
- E8 POSITIONAL: none — no code position is prescribed.
- E9 (quarantined world): the M-B3 world is copied into `test_node_ids.py`, the quarantined file is not edited or run.
  INVARIANT: canon never depends on a quarantined file.

#### C3-0 — the one predicate for true accept sites (F-D1 (b), Lead 17.11) — designer draft (this), then plan critic

Needed by C3-b2 (test_identity: `already_probed`, `_match`, `green_over_same_bytes` — fork F-T1; t-1033:
`_product_receipt_repeat`, `_run_freshness`), C3-rr (t-1033, `_reporter_outcome`), C3-d (t-1033, `validate_window`), C3-g
(`deployment_readiness` — fork F-T3) and C3-k. Not a wave 2 builder dispatch until the plan critic passes this card
(PROJECT.md п. 6 (в): a reused shape in a gate role) and the Lead answers F-T1/F-T2. (t-1033: the plan critic t-1026
passed it "dispatchable after listed edits (B1, B2, B10)"; the edits are in; K3 (error direction) and F-T1 (a) / F-T2 (a)
agreed by the critic; the Lead's answers are still owed. Based on main AFTER t-1032 merges, S-f.)

given: `C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md` (whole),
`C:/QAFactory/forge-repo/plans/builder-rules.md`, `C:/QAFactory/forge-repo/docs/TESTING.md`; this card and the C3
shared items (S-a..S-f); read, under `C:/QAFactory/forge-repo/ai-packages/qa-factory/`:
`scripts/gate_registry.py:1-80,110-146,205-264,427-457,467-483,485-681,684-743,786-842`,
`references/gate-registry.json` (rows test_identity :123-149, baseline_identity :333-354, provenance_acceptance :37-92,
exploratory_oracle :417-436 — lines on 2151eeef), `scripts/profile_contract.py:877-923` (`acceptable_provenance`, the
precedent and the error-direction model), `scripts/proof_level.py:850-892`, `scripts/tests/test_gate_registry.py` (its
table helpers; the S-f lines :55-68, :240-250, :316-339, :728-755, :907-1012)
owns:
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_template.py` (new: `acceptable`, `registry_problem` on F-T11 (a), a module docstring, no CLI)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json` (ONE site line in row `provenance_acceptance`: `{"file": "gate_template.py", "function": "acceptable", "role": "library"}`, beside the `gate_registry.py` library sites :65-68)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py` (one table of rows, item 4; the F4 flip control, item 7; the D13 triple and count of the new library site, item 8)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test-layers.json` (one string `"gate_template.py"` in the `covers` list :2035-2076 of the keep row `test_gate_registry.py`, :2032-2033)
non-goals: any consumer site (`proof_level`, `execution_request`, `baseline_contract`, `profile_contract`, `gate_preflight`,
`acceptance` and the provenance sites are wired by C3-b2 / C3-rr / C3-d / C3-g / C3-k); any `accepts` entry in the
registry (the consumers add theirs in the commit that wires them, AR-22); `profile_contract.acceptable_provenance` (F-T2);
`gate_registry.py` (its finding texts already name `gate_template.acceptable`, :840, :878); the census (no unit, item 3);
the debt/converted/split pins (C3-0 converts no row, S-f)
handoff: report path given by the Lead
edges: E1-E10 below
DoD: `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_registry.py --check` exits 0 (the new
module's comparisons sit in a registered `library` site; the debt block is unchanged at its count before the node — 8
after t-1032); then
`python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_template.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test-layers.json C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json`
and the printed non-slow files; `python -B ai-packages/qa-factory/scripts/tests/test_console_encoding.py` is not owed (no
console output). `test_gate_registry.py` and `test_judgment_census.py` are slow — judged by the batch canon, named in the
report
siblings: axis 26-class "one reader of a verdict word" — `profile_contract.acceptable_provenance` is the existing
provenance predicate (F-T2; named, not swept); `compare_identity` / `same_test` (axis 7, per-test identity) are the
producers of the words C3-b2 feeds in, unchanged here; the A26 audit's own reader `load_registry` is reused, not copied
(AR-13)

Items:
1. **Signature and lookup.** `acceptable(value, consumer, *, registry=None) -> bool` in `scripts/gate_template.py`.
   `consumer` is `<gate>.<consumer>` (`CONSUMER_RE`, `gate_registry.py:138`). The registry is the file read through
   `gate_registry.load_registry(<plugin root>)` (:427-447, the one reader, AR-13), read once per process and kept;
   `registry=<dict>` replaces it (the test seam `analyse(registry=…)` already uses, :786-795). The consumer resolves to the
   ONE row whose `accepts` holds it (consumer ids are unique across rows, `_check_registry` :722-727); its tokens are
   `accepts[consumer]`.
2. **The word.** `value` is a word or a record. A `str` is the word. A `dict` is a record: the word is
   `value[row["field"]]` when the row's `field` is a non-empty string (`baseline_identity` would name its field, F-T3);
   a dict under a row whose `field` is null is not acceptable. The word must be a `str` and an EXACT member of the row's
   `words` (no case fold, no strip); its class is `verdict_map[word]["class"]` and its reason is
   `verdict_map[word].get("reason_code")`. Acceptance, in class space (the `accepts` grammar is class tokens only,
   `_token_problem` :467-482):
   - class `matched`: acceptable iff `"matched"` is a token;
   - class `person_confirmed`: iff `"person_confirmed"` is a token AND the row's `promotable` is `true`;
   - class `not_applicable`: iff `"not_applicable"` is a token, or the reason is non-empty and `"not_applicable:<reason>"`
     is a token;
   - class `unknown` or `mismatched`: never (FR-59; `_token_problem` refuses those tokens, this is the second wall).
3. **Error direction: only toward NOT acceptable, and never raises.** Every doubt returns `False`: an unknown consumer, a
   consumer id that is not a string, a registry that cannot be read (`load_registry` returns a reason) or has no `rows`,
   a row with no `words` / `verdict_map` / `accepts`, a word outside `words`, a non-str word, a dict under a field-less
   row, a record missing its field, a class outside the five. Contrast with `acceptable_provenance`, which raises
   `ValueError` on an unknown token (`profile_contract.py:908-910`): here an unknown token cannot reach a caller because A26
   refuses it in the data, and if one ever did it simply matches nothing. No refusal site means no census unit (the
   census's units are refusal sites, `judgment-census.json:3`); if the builder needs a raise anywhere, the node stops and
   returns a question (the row would be `{"file": "gate_template.py", "function": "acceptable", "class": "xref",
   "owner": "data"}`, S-e).
4. **Test — one table in `test_gate_registry.py`** (keep, layer `gate_named`, `test-layers.json:2032-2033`; slow: canon),
   on an in-memory registry built from copies of the real rows (expected values from FR-59 "never a pass" and the rows'
   own `words` / `verdict_map` / `promotable`, never from the predicate's output). Rows, id = the case:
   - `word-matched`: test_identity words with a consumer `test_identity.probe_repeat: ["matched"]`; `"instance"` -> True
     (verdict_map `instance` -> matched, registry :136-141);
   - `empty-word`: `""` (what `same_test` returns for "not the same", `proof_level.py:874,892`) -> False;
   - `other-case`: `"Instance"` -> False; `other-shape`: `["instance"]`, `{"x": 1}`, `None`, `5` -> False each;
   - `unknown-consumer`: `test_identity.nope` -> False; `wrong-row`: a word of another row under this consumer -> False;
   - `record`: a row with `field: "status"`, words `captured`/`inconclusive` -> matched/unknown, consumer
     `[matched]`: `{"status": "captured"}` -> True, `{"status": "inconclusive"}` -> False, `{}` -> False,
     `{"status": None}` -> False, the dict under a field-null row -> False;
   - `never-unknown`: a hand-broken in-memory row whose consumer lists `"unknown"` and `"mismatched"`: their words -> False;
   - `person`: `person_confirmed`-class word with token `person_confirmed`: row `promotable: false` -> False, `true` ->
     True (exploratory_oracle :435 is the promotable precedent);
   - `not-applicable`: reason `no_changed_file` with token `not_applicable:no_changed_file` -> True, reason `local_source`
     -> False, bare token `not_applicable` -> True for any reason;
   - `registry-unreadable`: `registry={"rows": "x"}` and a plugin root with no registry -> False for every consumer.
   - (t-1033, on F-T11 (a)) `registry-problem`: `registry_problem(registry={"rows": "x"})` and a plugin root with no
     registry -> a non-empty reason (the `load_registry` / `structural_error` text); the live registry -> `""`.
5. **Covers line.** `"gate_template.py"` joins the `covers` of keep row `test_gate_registry.py`, so `--witness-for
   scripts/gate_template.py` names that file instead of "run the whole scenario layer" (`scenario_walk.py:913-921`).
6. **Registration.** `gate_template.py:acceptable` registered as a `library` site in `provenance_acceptance` (precedent:
   `gate_registry.py:_token_problem` / `_check_row` / `_check_registry` are `library` sites there, registry :65-67). Why a
   site at all: the body compares the anchor words `matched` / `person_confirmed` (`ANCHOR_FLOOR`, :119), and A26 flags an
   anchor comparison in any unregistered function (docstring :28-29).
7. **(t-1033, B1 (3)) The F4 flip control moves onto an in-memory copy row.** Today it flips the live debt row
   `s5_window` (`test_gate_registry.py:751-754`), which C3-d converts with `vocabulary: code`; after that (and after the
   last `target` debt row converts) the control would flip nothing. Rewrite: deep-copy the live registry, add to the copy
   one row copied from a live row with `vocabulary: "target"`, `status: "converted"`, `test` set to an existing test file
   and `debt_ref: ""` (a fresh id), run `GR.analyse(PLUGIN_ROOT, copy)`, and assert a finding starting `<that id>.vocabulary:`.
   expected from: `_check_row` rule "a converted row must say `code`" (`gate_registry.py:516-519`). The check id and
   message stay as at :753 ("F4 flipping a live `target` row …" becomes "… a `target` row …").
8. **(t-1033, S-f) D13.** The new library site's anchor comparisons are counted: `D13_TRIPLES` gains
   `("gate_template.py", "acceptable", "provenance_acceptance")`; `D13_ITEM_COUNT` rises by the number of comparisons the
   scan attributes to it, measured with `GR.analyse` before and after and named in a comment line (S-f form). No other
   pin of S-f moves (C3-0 converts no row).
9. **(t-1033, on F-T11 (a)) `registry_problem(*, registry=None) -> str`.** `""` when the registry reads and has `rows`,
   else the reason `load_registry` / `structural_error` gives (the same read, the same once-per-process cache as item 1).
   Pure, never raises. It is the one source a converted site uses to say WHY a reuse or a review was not accepted when
   the cause is the registry, not the word (C3-b2 E8, C3-d E3). No comparison of a row word in its body.

architecture content: `AR-13 -- the registry is read only through gate_registry.load_registry`; `AR-15 -- one predicate
for a true accept site; acceptable_provenance is named as the provenance survivor (F-T2)`; `AR-28 -- every unknown,
absent or malformed input is not acceptable, pinned by the table`; `AR-29 -- xref (a word joined to its registry row),
owner data, no census unit`; `AR-20 -- D13 +1 triple, count re-measured and named`. judgment content: `none -- a
membership join; what the word means stays with the producer (same_test, compare_identity) and the consumer`.

Edges:
- E1 (empty / absent): `value` `""`, `None`, `{}` or a record without its field -> False. INVARIANT: an absent word is
  never a pass (AR-28).
- E2 (unreadable registry): False for all, every call. INVARIANT: a broken registry makes every converted site refuse
  reuse (run again / not accepted), never accept.
- E3 (word outside the vocabulary): False, case-exact. INVARIANT: a word the row does not declare never counts
  (`Matched` is not `matched`).
- E4 (stale record): the predicate cannot see freshness; the caller computes the word NOW (`same_test(now, bound)`,
  `compare_identity(now, before)`) and passes it. INVARIANT: "a receipt measured on other bytes never counts" is kept by
  the producer returning `""` / `different` / `unknown`, all of which are not acceptable here.
- E5 (limit): none introduced (no size or count limit).
- E6 TEMPORAL (corrected t-1033, B2): seven consumer ids exist in the registry today — five under `provenance_acceptance`
  (`provenance.automation`, `.fingerprint`, `.manual`, `.manual_capture`, `.rehearsal`, registry :80-84),
  `provenance.environment_preparation` (:325) and `provenance.baseline` (:347) — and no `scripts/*.py` outside
  `scripts/tests/` reads any of them (Grep `provenance\.(automation|fingerprint|manual|manual_capture|rehearsal|environment_preparation|baseline)\b`
  over `scripts/*.py`: hits only `tests/test_gate_registry.py:287-291, 630-640`; those hits are the positive control of the
  same call). The two outside `provenance_acceptance` are dead consumers: C3-k removes `provenance.environment_preparation`
  (A2), C3-g removes or moves `provenance.baseline` (F-T3); the five are C3-k's. No real call of `acceptable` exists
  before C3-b2 / C3-rr / C3-d; the table runs on an in-memory registry. The file `gate_template.py` and its covers line
  are created by this node; before it, `gate_registry.py`'s texts name a function that does not exist (:840, :878), after
  it they name this one. INVARIANT: no consumer is wired before its `accepts` entry lands in the same commit, and no
  `accepts` entry is added without its reader in that commit (AR-22).
- E7 POSITIONAL: none in C3-0 (consumer positions are the consumer cards' E-rows).
- E8 (conflict with C3-k on `provenance_acceptance`): C3-0 adds one site line; C3-k runs after C3-0. INVARIANT: the line
  is additive and row-local.
- E9 (one road, P31): every true accept site of every converted row calls this one function; no row gets its own
  predicate. INVARIANT: a second acceptance reader is a finding (F-b), not a variant.
- E10 TEMPORAL (t-1033, S-f): C3-0 is based on main after t-1032; it edits `test_gate_registry.py` in three places of its
  own (item 4 table, item 7 control, item 8 D13 line) and no debt/converted/split pin. INVARIANT: the flip control never
  depends on a live row's status, so no later conversion kills it.

#### C3-rr — reporter_rehearsal_identity: the reuse through the predicate (t-1026 A1, Lead option (a); B-283) — wave 3, after C3-0 (t-1032 merged); gate_preflight queue position 1

The fix round t-1032 is merged (critic t-1039: `7f2f6f78`; pins on main, S-f). It put the row back to `status: debt`, `debt_ref: B-283`,
registers `gate_preflight._reporter_outcome` as `accept` and `_record_unreadable` as `produce`, and keeps the t-1009 test
row as the pin. Row on main: `gate-registry.json:498-523` (status :522; `_reporter_outcome` accept :503, `_record_unreadable` produce :504); +1 line after C3-0. The reuse decision is still `gate_preflight.py:3843` (`_reporter_outcome` :3824-3869), re-read in t-1043. This card converts the row again by routing the reuse decision through the predicate. Fact read t-1033:
the reuse decision is `gate_preflight.py:3843`, `if isinstance(hit, dict) and isinstance(hit.get("at"), str) and
earlier["state"] == "same_command":` inside `_reporter_outcome` (:3824-3869); `earlier` comes from `_earlier_proof`
(:3954-3963), always a dict with `state` (`onboarding_probe.earlier_proof`, or `{"state": "unreadable", …}` when the reader
cannot be imported).

given: `C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md` (whole),
`C:/QAFactory/forge-repo/plans/builder-rules.md`, `C:/QAFactory/forge-repo/docs/TESTING.md`; this card and the C3 shared
items (S-a..S-f); `C:/QAFactory/forge-repo/docs/tasks/specs/reviews/t-1026-rules-debt-wave2-code-and-cards.md` (A1); the
accepted C3-0 card and its diff; read, under `C:/QAFactory/forge-repo/ai-packages/qa-factory/`:
`scripts/gate_preflight.py:3824-3869,3954-3971`, `references/gate-registry.json` (row `reporter_rehearsal_identity`, :498-523 on main (t-1043)), `scripts/tests/test_gate_preflight.py:5199-5224`, `scripts/tests/test_gate_registry.py`
(the S-f lines), `gate_template.py` on C3-0's tree (:29-57)
owns:
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_preflight.py` (`_reporter_outcome` only: the reuse condition at :3843 and the import it needs) — HOT
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json` (row `reporter_rehearsal_identity` only: `accepts`, `status`, `debt_ref`)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_preflight.py` (rows of the table of `test_c3r_reporter_rehearsal_identity_an_unknown_is_rehearsed_again_never_reused`, :5210, only)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py` (S-f pins of this row only)
non-goals: `_rehearse_reporter`, `_record_unreadable`, `_earlier_proof`, `_rehearsal_key`, `_record_rehearsal`,
`onboarding_probe.earlier_proof` (the producer of the state words); `driver_gates.hand_to_conductor`; the row's words,
`verdict_map`, sites and roles (t-1032's); `gate_template.py` (C3-0's); `judgment-census.json` (no unit: `_reporter_outcome`
has no census row and no refusal site is added); any new test function or file
handoff: report path given by the Lead
edges: E1-E7 below
DoD: `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_registry.py --check` exits 0,
`reporter_rehearsal_identity` is absent from the `N gate(s) left as debt:` block, and no F-b line names
`_reporter_outcome`; then
`python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_preflight.py C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_preflight.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py`
and the printed non-slow files; `test_gate_preflight.py` and `test_gate_registry.py` are slow — judged by the batch
canon, named in the report
siblings: A1's class "a converted row's word compared in an unregistered function" — `_record_unreadable` (produce,
t-1032), `_rehearse_reporter`'s coincident `countable['state'] == 'none'` (stays a `validate` site: report_adapt's word);
the other sweep items of t-1026 q4 (`red_sandbox.py:2292`, `execution_request.py:3187`, `environment_preparation.py:444,616`,
`stand_gaps._c4`) are the critic's queue lines, not this card; axis 5 (`docs/SIBLING_MAP.md:143`, gate rows <-> sites <-> prose twins): the row's words do not change, so no prose twin is walked. Waiting finding (R12 (b)): `profile_contract.selector_contract:417` (`if state == "same_command": return result(True, …)`) is a second reader of `onboarding_probe.earlier_proof`'s word, registered in no row. It decides 'selector verified', not reuse, and its docstring bounds the error (:361-363, 'a wrong True never gives a pass … Error direction: False when in doubt'). One finding in the rules-debt pile, not carded.
designer: `C:\QAFactory\forge-repo\docs\tasks\specs\20261117-rules-debt-phase2-cards-spec.md` (C3-rr, t-1033)

Items:
1. **Registry.** Row `reporter_rehearsal_identity`: `accepts: {"reporter_rehearsal_identity.reuse": ["matched"]}`,
   `status: converted`, `debt_ref: ""`; `_reporter_outcome` stays `accept`; words and `verdict_map` unchanged
   (`same_command` -> matched; `command_changed`, `none`, `unreadable` -> unknown, owner environment, registry :507-513).
   expected from: A1 (a) and the row's `decides` ("`matched`: the same command, and the key hits", :500).
2. **The reuse condition.** `gate_preflight.py:3843` becomes
   `if isinstance(hit, dict) and isinstance(hit.get("at"), str) and acceptable(earlier.get("state"), "reporter_rehearsal_identity.reuse"):`
   — the two hit checks stay first; the literal `earlier["state"] == "same_command"` is gone. Import: `from gate_template
   import acceptable` at the module's top, or at the point of use when the import would cycle (the builder reads the
   import chain; `gate_template` imports `gate_registry`, which imports `hooklib`). (Small choice: `.get("state")`, not
   `["state"]` — an absent state is False, never a `KeyError`; §7.) Module-top `from gate_template import acceptable` is cycle-free: `gate_registry.py` imports only stdlib and `hooklib` (:97-104), and `hooklib` only stdlib (`hooklib.py:2-13`). The builder re-checks against the merged C3-0.
3. **Tests.** Rows added to the table at `test_gate_preflight.py:5210` (tuples of `(state, reused)`, no new function):
   `("Same_command", False)`; a non-str state `(None, False)`; an absent state (the call gets `{"at": ""}` with no `state`;
   the builder adds one optional field to the tuple for it) -> not reused; and, only if no case of the file pins it (the
   builder greps first), `same_command` with the `_rehearsals` map holding ANOTHER key -> rehearsed (A1: "a `same_command`
   whose key misses is rehearsed again"). One row for the unreadable registry : `same_command` with a hit -> rehearsed, nothing reused. The unreadable-registry row patches the registry cache of `gate_template` named in C3-0's accepted diff. At a4aca646 that is `_READ`, a module list holding one `(registry, reason)` pair (`gate_template.py:31-37` there). Save `list(GT._READ)`, set `GT._READ[:] = [({"rows": "x"}, GR.structural_error({"rows": "x"}))]`, and restore it in `finally` (precedent: `test_gate_registry.py:1108-1119` on that branch). If the merged C3-0 names the cache otherwise, use that name; if it exposes no cache, the node stops with a question.
   expected from: the row's `decides` ("An unknown never keys a proof as the same", :500), FR-59 and C3-0 E2 — never from
   `_reporter_outcome`'s output before the change.
4. **S-f pins.** `EXPECTED_DEBT` loses `reporter_rehearsal_identity`; `EXPECTED_CONVERTED` gains it; K-T1.2 N-1; split
   converted +1 / debt -1; F4 unchanged (the row already says `code`); D13: the triple
   `("gate_preflight.py", "_reporter_outcome", "reporter_rehearsal_identity")` leaves the set when no comparison of a row
   word is left in the function — expected to leave: the only one is :3843 (`_reporter_outcome` read whole, :3824-3869;
   `hit.get("source") == "onboarding"` holds no row word) — and the count falls by one from the base (140 after t-1032, 146 after C3-0's library-site comparisons, a4aca646, S-f; plus whatever merged between C3-0 and this node); measured with
   `GR.analyse` before and after and named (S-f).
5. **No text moves.** On "not acceptable" the function rehearses exactly as before; the person-facing sentence keyed by
   the state word (`_EARLIER_SAYS`, :4075, read at :4180) is unchanged. On F-T11 (a) nothing is added here: this branch
   prints no reason for the non-reuse. (R5/R15) An unreadable registry is stopped earlier, at the next dispatch, by C3-reg-precondition. Inside a stage that began before, this branch rehearses with no word about the registry: cost only, not a dead end (critic t-1039 R5). `registry_problem()` does not cover a registry that parses but lacks the consumer; there `acceptable` is False and the command is rehearsed (C3-0 R15 note, F-T11).

architecture content: `AR-13 -- the reuse word is read only through gate_template.acceptable`; `AR-22 -- the consumer
reporter_rehearsal_identity.reuse and its reader land in one commit`; `AR-28 -- an absent, malformed or unaccepted state
rehearses, pinned by the table`; `AR-29 -- xref (a state word joined to its registry row), owner data, no census unit`;
`AR-20 -- debt -1, converted +1, D13 -1 triple, named`. judgment content: `none -- a membership join of the producer's
state word; the durable key hit stays code's data check`.

Edges:
- E1 (absent / empty / other case / non-str state): not acceptable -> the command is rehearsed. INVARIANT: an unknown never
  keys a proof as the same (the row's `decides`).
- E2 (unreadable registry): every call rehearses; cost: one rehearsal per command per process (the per-process map
  `_REPORTER_PROBES` still keeps the outcome). INVARIANT: a broken registry never reuses a proof.
- E3 POSITIONAL: the two hit checks stay BEFORE the predicate. INVARIANT: a missing or malformed hit is never reused,
  whatever the state says; the predicate is never the only guard (the key still has to hit: same words, test, report
  format, dependency files, :3836-3840).
- E4 TEMPORAL: before C3-rr (main since t-1032 merged) the row is debt and the literal at :3843 is allowed (a debt accept site);
  after, the row is converted and F-b is satisfied by the `acceptable` call. C3-rr cannot be built before C3-0 merges (`gate_template.py` is absent on main at t-1043: Glob, with the worktree hit as the control). Durable records written before (onboarding, earlier gates) are read the same
  way: the state words are the producer's, unchanged. INVARIANT: for every state word that exists today the behaviour is
  identical (`same_command` reused iff the key hits; every other word rehearsed); no recorded proof changes meaning.
- E5 TEMPORAL (S-f): the pins are deltas from the main the card is based on (after t-1032 and C3-0). INVARIANT: S-f.
- E6 (limit): none introduced.
- E7 (conflict on `gate_preflight.py`, HOT): function-disjoint with C3-j (`_e2e_limit`, `check_s5_stand_limits`,
  `_stand_limit_card`), C3-k (`_observed_identity`) and C3-h (code only if its S-b is red); the file is still one stream at a
  time: `очередь: C3-rr → C3-j → C3-k → C3-h` (gate_preflight.py). INVARIANT: no two open nodes edit the HOT file at once.

Measurement (п. 6 (а)): not a meaning change (the same words accepted, the same refused). Not measured here (no shell);
the control for the Lead or the builder: `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_registry.py --sites`
before and after, filtered for `_reporter_outcome` — one line (`earlier['state'] == 'same_command'`) before, none after.

#### C3-a — folded into C3-R (item 1)

#### C3-b1 — live_check_demand -> question to the code critic (B-279) — designer draft (this), then plan critic; wave 2½, after S9

Split out of C3-b (F-b5, Lead decision 5). No predicate: `proof_required` and `novelty_of` are `produce` (E-c table).
(t-1033: the plan critic t-1026 found K1, K2, K4 holding and agreed F-T4 (a), F-T8 (a); its edits B1 and B5 are in: the S-f
pins, and F-T5 (a+) with the writer's manifest-level marker.)

**What changes, and what does not (F-b1, Lead decision 5: NO existing block is relaxed).** A stored `unknown` novelty
already DEMANDS a live probe: `_NOVELTY_DEMANDS = ("new", "changed", "unknown")` (`proof_level.py:327`) and
`proof_required` (c) (:475-478). An absent key gives `(None, "")` (:413-414) and then only the row's flags count (:452-456,
`_wanted`). The debt the row names ("a legacy row whose novelty nobody measured is shown to the person as a debt",
registry :189) is `not_required_why == "unmeasured"` (:501): no `novelty` key, no flag, not handed. ONLY such a row is
asked; every row that is required today stays required, and a stored `unknown` keeps its demanded probe (it is never
replaced by a question).

**Measured premise (п. 6 (а)).** On the recorded stories the question fires on **0** rows: no `tests[]` row carries a
`novelty` key (Grep `"novelty"` count over `fixtures/stories/cart-1/work/automation-manifest.json` and
`fixtures/stories/local-1-0108/work/automation-manifest.json`: 0 and 0; positive control, same tool and file:
`"change_disposition": "new_or_changed"` counts 24 and 45), and the critic's per-row probe (t-989 trail: `novelty_of` /
`proof_required` / `not_required_why` over every `tests[]` row — cart-1 18 rows all `(None, required=True, why='')`,
local-1-0108 34 rows the same: 0 of 52 asked; not re-run here, no shell). The change bites only on a keyless, flagless,
unhanded row; the test row must BUILD that world. (t-1033: the marker of F-T5 (a+) is a new field, absent from every
recorded manifest by construction; its premise is not measurable on fixtures — the command for a live story after the
node: `python -B -c "import json,sys; m=json.load(open(sys.argv[1],encoding='utf-8')); print(repr(m.get('novelty_unmeasured')), sum('novelty' in r for r in m.get('tests',[])))" <task root>/work/automation-manifest.json`.)

given: `C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md` (whole),
`C:/QAFactory/forge-repo/plans/builder-rules.md`, `C:/QAFactory/forge-repo/docs/TESTING.md`; this card and the C3 shared
items (S-a..S-f); t-989 F-b1..F-b5; t-1026 B5; read, under `C:/QAFactory/forge-repo/ai-packages/qa-factory/`:
`scripts/proof_level.py:320-501`, `scripts/acceptance.py:1052-1230` (`validate_window`: the review and `sensitivity:`
gaps), `scripts/window_record.py:1460-1500` (the item build: `review`, `novelty`), `scripts/manifest_put.py:75-95,
158-172, 1085, 1285-1330` (`SCALAR_EXEMPT` and the "a scalar the fragment carries wins" loop, `CRITIC_FIELDS`, the critic's
write road), `scripts/manifest_from_tests.py:825-940` (V2, `_novelty_block`, `_keep_stored_novelty`, `_attach_novelty`),
the S9 card's accepted draft (the word road for a window gap), `scripts/tests/test_gate_registry.py` (the S-f lines)
owns:
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/proof_level.py` (`_wanted`: a `probe_owed: "yes"` adds the requirement on a keyless row; new `novelty_question_owed(entry, manifest) -> bool`)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/acceptance.py` (`validate_window`: one gap `novelty_question:<instance>`)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/window_record.py` (the item copies `probe_owed` from its row beside `review`; `WORD_READ_KINDS` gains `novelty_question` — after S9)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/manifest_put.py` (`CRITIC_FIELDS` gains `probe_owed`; a value outside `yes`/`no` refused with its field name)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/manifest_from_tests.py` (`_attach_novelty` only: the `novelty_unmeasured` marker, item 8 — on F-T5 (a+))
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/agents/qa-code-critic.md` (one paragraph: the question, the two answers, where they are written — AR-10/FR-38: the requirement reaches the role before the work)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json` (row `live_check_demand` only)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_proof_level.py` (rows), `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_window_record.py` (one row)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py` (S-f pins of `live_check_demand` only)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json` (S-e: own rows only, if the wide scan finds a new unit)
non-goals: any change to `proof_required` for a row that carries `novelty` or a flag; `novelty_of`; `manifest_from_tests`
beyond `_attach_novelty`'s marker (the one novelty writer: V2, `_novelty_block` and `_keep_stored_novelty` unchanged);
`probe_debt.py`; the ledger words (`words_for`); `s5_precheck.py`
handoff: report path given by the Lead
edges: E1-E11 below
DoD: `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_registry.py --check` (exit 0; `live_check_demand` absent from the debt
block); `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <every owns path>` and the printed
non-slow files; `test_proof_level.py`, `test_window_record.py`, `test_judgment_census.py`, `test_gate_registry.py` are
slow — judged by the batch canon
siblings: axis 34 (one road: a person's word passes the new gap through the window's word road, `WORD_READ_KINDS`, as S9
makes it pass a `review` gap — not a third road); axis 32 (census, S-e); axis 7 n/a (no identity rule moves); the
`handed` exemption (`_handed`, :460-464) is kept as it is, decided first
designer: `C:\QAFactory\forge-repo\docs\tasks\specs\20261117-rules-debt-phase2-cards-spec.md` (C3-b1, after the plan critic and F-T4/F-T5/F-T8)

Items (on the recommendations of F-T4, F-T5 (a+), F-T8):
1. `proof_level.novelty_question_owed(entry, manifest) -> bool`: True iff `entry` is a dict, has NO `novelty` key, no
   flag (`sensitivity_proof_required`, `new_or_changed`, `change_disposition == "new_or_changed"`), is not handed
   (`_handed`), carries no `probe_owed` in {`yes`, `no`}, AND the manifest holds at least one `tests[]` row that carries a
   `novelty` key (F-T5 observable: the writer of this version ran) OR — on F-T5 (a+) — the manifest's top-level
   `novelty_unmeasured` is a non-empty string (the writer ran and its measurement failed, item 8). test: rows in
   `test_proof_level.py` — the keyless, flagless row in a manifest with one measured row -> True; the same row in an
   all-keyless manifest (the recorded stories' shape) -> False; the same all-keyless manifest with
   `novelty_unmeasured: "novelty could not be measured (OSError)"` -> True; with `novelty_unmeasured: ""` -> False; with
   `novelty_unmeasured: 5` or `[]` -> False (E10); flagged -> False; handed -> False; `probe_owed: "no"` -> False; stored
   `novelty: unknown` -> False (it is already required). expected from: registry `decides` (:187), F-b1, t-1026 B5, the
   owner's «да» (F-O1).
2. `_wanted`: a keyless row with `probe_owed: "yes"` is wanted (the answer only ADDS a requirement); `"no"` adds nothing.
   test: `proof_required` row: keyless + `probe_owed: "yes"` -> True; keyless + `"no"` -> False (as today); flagged +
   `"no"` -> True (a flag is never overruled). expected from: `proof_required` (c) "a layer can only add a requirement"
   (:476-478).
3. `validate_window`: an item for which the question is owed (the window item carries the row's `probe_owed` copy and
   the window builder records the owed state; the reader is item 1's predicate over the item and the window's manifest
   view) gets ONE gap `novelty_question:<instance>`, after the review checks and before the `sensitivity:` check.
   test: one row in `test_window_record.py` (a window with such an item -> the gap and its door; the same item with
   `probe_owed: "no"` -> no gap). expected from: the registry branch (question / wait / window_acceptance).
4. `manifest_put`: `probe_owed` joins `CRITIC_FIELDS` (:1085); a value other than `yes` / `no` is refused naming the
   field and the two values (FR-1). test: covered by the item-2 row through the fragment (the field must survive the
   write road); a refusal row only if the existing critic-field table holds one per field (builder reads).
5. Charter (`agents/qa-code-critic.md`): "When the window asks `novelty_question` for a test, answer in the manifest
   fragment `probe_owed: yes` (a live probe is owed: the test is new or changed) or `probe_owed: no` with `critic_note`
   (why not)". English, FR-30.
6. Registry row (F-b3): `unknown_branch: question`, `on_no_answer: wait`, `waits_at: window_acceptance`,
   `closed_by: ["role:qa-code-critic", "person"]`, `addressee: ["role:qa-code-critic"]`, `vocabulary: code` (the words
   `new/changed/unchanged/unknown` are the code's, `proof_level.py:326`), `verdict_map.unknown.owner: "role"` (small choice:
   the critic answers it now; `factory` would claim our defect), `decides` rewritten to the new behaviour, `status:
   converted`, `debt_ref: ""`.
7. (t-1033, S-f) The pins of `live_check_demand`: `EXPECTED_DEBT` loses it, `EXPECTED_CONVERTED` gains it, K-T1.2 N-1,
   split +1/-1; F4 unchanged (the row already says `code`, registry :186); re-measure D13 with `GR.analyse` before and
   after and name the move (the row's sites `proof_required` / `novelty_of` and the new `novelty_question_owed` if the
   builder registers it — `("proof_level.py", "novelty_of", "live_check_demand")` is in the set today, :957).
8. (t-1033, on F-T5 (a+)) `manifest_from_tests._attach_novelty` writes the top-level fragment key `novelty_unmeasured`
   on EVERY call that measures: the failure note (`"novelty could not be measured (<ExcName>)"`, the text it already
   appends at :924) when the call fails, `""` when it succeeds. The key reaches the manifest through `manifest_put`'s
   scalar loop ("a scalar the fragment carries wins", `manifest_put.py:161-166`); the builder confirms by reading the merge
   and the manifest schema that a top-level string is taken — if `manifest_put` refuses or drops it, the node stops and
   returns the refusal as a question (owns stay as they are). test: one row in `test_proof_level.py` is item 1's; the
   writer's half rides on an existing `manifest_from_tests` keep test only if `--witness-for` names one, else a report line
   "no keep row drives `_attach_novelty`'s failure branch". expected from: t-1026 B5 ("the writer's failure note becomes a
   manifest-level marker").

architecture content: `AR-28 -- an unmeasured novelty is asked, never passed silently`; `AR-29 -- the probe-owed decision
is the code critic's judgment, accepted at window acceptance; code checks the presence of a closed typed answer (xref)`;
`AR-22 -- probe_owed has one writer (manifest_put, the critic's fragment) and its readers (proof_level, window) in the
same commit; novelty_unmeasured has one writer (manifest_from_tests) and its reader (novelty_question_owed) in the same
commit`; `AR-10 -- the charter states the answer before the window asks`; `AR-20 -- debt -1, converted +1, D13
re-measured`.

Edges:
- E1 (absent key, the real change): keyless + flagless + unhanded + measured manifest -> asked. INVARIANT: an
  unmeasured novelty never passes silently in a story whose writer measures.
- E2 (stored unknown): unchanged — demanded probe, never a question. INVARIANT: no existing block is relaxed (Lead
  decision 5).
- E3 TEMPORAL (in-flight stories, F-b4; consequence corrected t-1033): a manifest with no `novelty` row and no
  `novelty_unmeasured` marker (written before the writer of this version, or by hand) is never asked (F-T5). The field
  `probe_owed`, the marker and the gap kind exist only after this node; before it, no window carries them and nothing
  reads them; after it, the marker is written by the next `manifest_from_tests` run of a story, so a story in flight is
  asked only from its next writer run on. Not every in-flight story stays un-asked: a row V2 left keyless
  (`manifest_from_tests.py:835-840`) in a manifest where another row measured `new`/`changed` IS asked (F-T5, case 2).
  INVARIANT: builder-rules 9 — a story in flight is never held over a field its artifacts do not have (cases 3 and 4 of
  F-T5); the one exception (case 2) is named in F-T5 for the Lead.
- E4 POSITIONAL: the gap is added after the review checks and before `sensitivity:`; INVARIANT: it never replaces a review
  gap or a sensitivity gap, and it never fires on a handed, stopped or pending item (they are decided first, as at
  `acceptance.py:1154-1207`).
- E5 (conflict: `probe_owed: "no"` on a flagged row): the flag wins (required). INVARIANT: the critic's answer can only
  add a requirement.
- E6 (empty / broken answer): `probe_owed: ""`, `"Yes"`, `true`, a list -> refused by `manifest_put` with the field name;
  on a hand-edited manifest, the reader treats anything outside {yes, no} as "not answered" (the gap stays). INVARIANT: a
  malformed answer never closes the question.
- E7 (person, FR-4/P13): a person's recorded word passes the gap through the window's word road (axis 34, after S9).
  INVARIANT: the person passes every block, by the one road.
- E8 (limit): none introduced (the marker carries the writer's note, already bounded by `type(exc).__name__`).
- E9 (outside input): the critic's fragment is a role's output (internal): no battery beyond E6.
- E10 (t-1033, the marker's own edges): absent, `""`, or a non-string (`5`, `[]`, `null`, a hand edit) -> "not marked"
  (the in-flight-safe side: the marker is the writer's own output, and only the writer's non-empty note means "the writer
  ran and failed"); a stale marker from an earlier failed run is overwritten by the next successful call's `""`.
  INVARIANT: a manifest is asked on the marker only when its last writer run failed.
- E11 (t-1033, S-f TEMPORAL): the pins are deltas from the main C3-b1 is based on (after t-1032, C3-0 and C3-rr in the
  expected order); D-0048 re-derivation when a sibling merged first. INVARIANT: S-f.

#### C3-b2 — test_identity through the predicate (B-217) — wave 3, after C3-0 (and F-T1)

(t-1033: redrafted under t-1026 B1 and B4 — two reuse decisions added, `_product_receipt_repeat` and `_run_freshness` —
and the class sweep returned as fork F-T10.)

given: `C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md` (whole),
`C:/QAFactory/forge-repo/plans/builder-rules.md`, `C:/QAFactory/forge-repo/docs/TESTING.md`; this card and the C3 shared
items (S-a..S-f); the accepted C3-0 card and its diff; t-1026 B4; read, under
`C:/QAFactory/forge-repo/ai-packages/qa-factory/`: `scripts/proof_level.py:815-974,1365-1532` (and `:1580-1620`,
`:1886-1905` on F-T10 (a)), `scripts/execution_request.py:2065-2183`, `references/gate-registry.json` row test_identity
:123-149, `scripts/tests/test_gate_registry.py` (the S-f lines)
owns:
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json` (row `test_identity` only, :123-149 on main, +1 after C3-0: `accepts`, words (F-T1 (a)), sites, status)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/proof_level.py` (`already_probed`, `_product_receipt_repeat`, `_run_freshness`, `_evaluate` (F-T10 (a), decided), and the import line it needs)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/execution_request.py` (`_match` and the import it needs; ONE docstring sentence of `same_instance_bytes`, :2069-2072, R14; `green_over_same_bytes` only as re-roled in the registry, F-T1 (a))
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_proof_level.py` (rows: item 2 one, item 3 one, item 6 two)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_execution_request.py` (two rows, item 5)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_run_freshness.py` (one row, item 4)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py` (S-f pins of `test_identity` only)
non-goals: `same_test`, `compare_identity`, the code of `same_instance_bytes` (it keeps serving `_same_identity_for_count`, the budget side; only its docstring sentence that names `_match` as a caller changes, R14); the receipt path of `already_probed` (it relies on `reached`); the public
`run_freshness` wrapper (:945-974) and `acceptance.run_freshness_of`; `holds_over_comments` (finding, F-T10 (a)); the code of `_stale_receipt` (registered `produce` only) and `probe_freshness` (R2 residue, E8);
`judgment-census.json` (none of the owned functions has a census row — grep, control `validate_window` found at :7 — and
no refusal site is added)
handoff: report path given by the Lead
edges: E1-E11 below
DoD: `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_registry.py --check` (exit 0; `test_identity` absent from the debt
block; no F-b for its accept sites); `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <every owns path>`
and the printed non-slow files; `test_proof_level.py`, `test_execution_request.py`, `test_gate_registry.py` slow — canon
siblings: axis 7 (per-test identity: one predicate `compare_identity`, its readers fold `unknown` themselves —
`proof_level.py:824-827`); axis 25 (freshness predicates: `_run_freshness` is the run side of `same_test`, `proof_level.py:895-900`)
- axis 5 (`docs/SIBLING_MAP.md:143`): F-T1 (a) changes `test_identity`'s words. The axis's prose twins (`references/execution-lifecycle.md` + slice, `manual-evidence.md`, `environment-preparation.md`, `phases/s5.md`/`s6.md`) are walked by the builder by grep for `instance_code|file_code|same_test|compare_identity`. Each hit gets a report line 'checked, no edit (meaning unchanged)' or an edit named as a finding. Not walked by the designer.
- Waiting findings (R12): (a) `probe_verdict`'s words are accepted in functions no probe_verdict site names: `proof_level.already_probed:1463` (`== "intended_failure"`) and :1491 (`in ("no_failure", "wrong_location")`), `_product_receipt_repeat:1378`, and `acceptance.validate_window:1211`. After C3-b2/C3-d those functions are converted accept sites of other rows, and A26 refuses a second registration of a converted accept site (`gate_registry.py:831-836`, 'give each row its own function'). Any later fix therefore needs a function split. One finding. (d) 'delete or wire `holds_over_comments`' (no production caller; F-T10 (a)). One finding.
designer: `C:\QAFactory\forge-repo\docs\tasks\specs\20261117-rules-debt-phase2-cards-spec.md` (C3-b2, after C3-0)

Items:
1. **Registry.** `same_test` re-roled `produce`; new sites `{"file": "proof_level.py", "function":
   "_product_receipt_repeat", "role": "accept"}` and `{"file": "proof_level.py", "function": "_run_freshness", "role":
   "accept"}` (on F-T10 (a) also `_evaluate` accept and `_stale_receipt` produce); consumers
   `test_identity.probe_repeat: ["matched"]` (already_probed, _product_receipt_repeat), `test_identity.run_reuse:
   ["matched"]` (_match), `test_identity.run_fresh: ["matched"]` (_run_freshness) (on F-T10 (a) also
   `test_identity.receipt_holds: ["matched"]`); on F-T1 (a) the row's words gain `same` -> matched, `different` ->
   mismatched, `unknown` -> unknown (owner environment) and `green_over_same_bytes` is re-roled `validate`; status
   converted.
2. **`already_probed`.** The two reuse tests at :1491-1492 and :1506-1507 call `acceptable(same_test(now,
   proof_identity(record)), "test_identity.probe_repeat")` in place of the bare truthiness; the display comparison at
   :1520 gets an `allow` entry in the `ast.unparse` form `hit['holds'] in ('instance_code', 'file_code')` with why "picks
   the words shown, not an acceptance". S-b row (moved from item 5, R3) in `test_proof_level.py`: an old probe record (`no_failure`) whose identity does not match the test now -> `already_probed` answers `{"probed": False}` (the probe runs). Expected from: the row's `decides` (`gate-registry.json:125`).
3. **(t-1033, B4) `_product_receipt_repeat`.** The test at :1378-1379 calls `acceptable(same_test(now,
   proof_identity(record)), "test_identity.probe_repeat")` in place of the bare `same_test(...)` truthiness; `"holds":
   same_test(...)` at :1400 is display and stays. S-b row in `test_proof_level.py`: a product record `intended_failure`
   over OTHER test bytes (its identity does not match) with a holding receipt -> `_product_receipt_repeat` returns None,
   `already_probed(kind="product")` answers `{"probed": False}` (the probe runs). expected from: the row's `decides`
   (:125) "a non-match is an unknown and the answer is to run again", and the function's own contract that the record must
   be "on the same test bytes (`same_test`)" (docstring :1371) — never from its output before the change.
4. **`_run_freshness`.** The test at :939 becomes `if acceptable(same_test(now, {"instance_identity": dict(shas, job_id="")}), "test_identity.run_fresh"): return "fresh", ""`. On False the `stale` return stays, with its why `WHY_RUN_CHANGED` (:903, :941-942). On F-T11 (a), when `gate_template.registry_problem()` is non-empty, the why names the registry instead: 'the gate registry cannot be read (<reason>): a factory defect, not a change of the test'. The why names the registry; the `stale_run` gap's owner and door stay as they are (`_run_freshness` returns `(state, why)` only; the gap's owner and door come from the window's origin table). The re-run loop is the node C3-reg-precondition's.
   Pins (R1): `test_proof_level.py` has no run_freshness table (critic grep: only :1554-1556, an import; not re-read here). The table is `scripts/tests/test_run_freshness.py` (keep, layer `gate_named`, `test-layers.json:4702`), function `the_run_is_fresh_or_stale_by_the_code_it_ran` (:73). It already pins both rows: K1 (b) :80-86 (a comment, docstring or blank lines in the test -> fresh, the `instance_code` case) and K1 (f) :104-106 (a variable renamed -> stale). K1 (d) :92-98 pins the `WHY_RUN_CHANGED` sentence. These are NAMED in the report and get no new row (S-b). ONE new row beside them: the unreadable registry (the `gate_template` cache patched as in C3-rr item 3, restored in `finally`) -> `stale`, with a why that names the registry and does not say 'changed since'. Expected from: the docstring rule list of `run_freshness` (`proof_level.py:952-960`, rule 4) and FR-59.
5. **`_match`.** Inside the same `author_run_reading != "per_story"` condition (`execution_request.py:2099-2103`), `not same_instance_bytes(a, b)` becomes `not acceptable(proof_level.compare_identity(a, b)[0], "test_identity.run_reuse")` (`import proof_level` in the function, as `same_instance_bytes` does at :2074; `from gate_template import acceptable`). The return stays `("", <why>, _WHY_RANK["bytes"])`. The why is 'instance bytes differ: …' (:2102-2103) or, when `registry_problem()` is non-empty, 'the gate registry cannot be read (<reason>): a factory defect, the earlier run was not judged'. The rank stays `bytes` in both cases, so the order of the first difference is unchanged (docstring :2080-2082). Two rows in `test_execution_request.py`: (i) an earlier job whose instance bytes differ -> `("", "instance bytes differ: …", _WHY_RANK["bytes"])`; (ii) the unreadable registry (cache patched, restored in `finally`) -> `("", <a why that names the registry>, _WHY_RANK["bytes"])`. Expected from: the row's `decides` (:125) and the docstring's order, never from `_match`'s output before the change. The R14 docstring sentence: `same_instance_bytes`'s 'the two callers fold it … `_match` …' (:2070-2072) is rewritten to name its one caller, `_same_identity_for_count`, and to say that `_match` reads `compare_identity` through the predicate.
6. **(F-T10 (a), decided) `_evaluate`.** `if not how:` at :1605 becomes `if not acceptable(how,
   "test_identity.receipt_holds"):` (the same words are matched-class, so the same receipts count); `over_comments = how in
   ("instance_code", "file_code")` (:1613) gets an `allow` entry (display flag, as :1520); `_stale_receipt` registered
   `produce` (it builds a why). On F-T11 (a) (R2): when `gate_template.registry_problem()` is non-empty, the issue reads 'the gate registry cannot be read (<reason>): a factory defect, the receipt was not judged' instead of the bytes sentence (:1606-1612). Two rows in `test_proof_level.py`: a receipt for other code -> not valid; the unreadable registry (cache patched) -> not valid, and the issue names the registry, not 'other bytes'. `holds_over_comments`
   is not touched (no production caller): its delete-or-wire question goes to a finding of the rules-debt pile (F-T10).
7. **(t-1033, S-f) Pins.** `EXPECTED_DEBT` loses `test_identity`, `EXPECTED_CONVERTED` gains it, K-T1.2 N-1, split
   +1/-1; F4 unchanged (the row already says `code`, registry :124); D13 re-measured with `GR.analyse` before and after. Expected: +2 triples:
   - `("proof_level.py", "same_test", "test_identity")`: `:881 verdict == 'same'` is counted once F-T1 (a)'s words land; allowed, because `same_test` becomes `produce`;
   - `("proof_level.py", "_evaluate", "test_identity")`: `:1613 how in ('instance_code', 'file_code')`, covered by item 6's `allow`.

   `D13_ITEM_COUNT` +2 from the base (146 after C3-0, plus what merged since; S-f). `_run_freshness:939` is not counted after the change (its literal is gone). `already_probed:1520` stays counted, with its allow. `_product_receipt_repeat` and `_stale_receipt` hold no row word (critic t-1039 R4, `GR.analyse` on in-memory copies; not re-run here). A different measurement is a stop and a question.

architecture content: `AR-13 -- every test_identity reuse word is read through gate_template.acceptable`; `AR-28 -- a
non-match, an absent identity or an unreadable registry runs again, pinned`; `AR-29 -- xref, owner data, no census unit`;
`AR-20 -- debt -1, converted +1, D13 re-measured`; judgment `none -- the reuse decision is a join of a computed identity
word to the registry`.

Edges:
- E1 POSITIONAL (`_match`): the predicate is reached only when the whole-file fingerprints differ (the `identical`
  short-circuit at :2091-2093 stays first) and only off `per_story`; INVARIANT: no request that reuses today on equal
  fingerprints is refused, and no result over other bytes is reused.
- E2 POSITIONAL (`already_probed`, `_product_receipt_repeat`): the predicate sits where the truthiness was, after the
  record's verdict check and before `_mutated_files_hold`; INVARIANT: a record over other bytes never answers the repeat
  (`same_test` -> `""`), and a record that does not say `no_failure`/`wrong_location`/`survived`/`intended_failure` is
  never asked about identity at all.
- E3 (empty identity): `compare_identity` -> `unknown` -> not acceptable -> run again.
- E4 TEMPORAL: jobs recorded before `instance_code_sha` compare by content (unchanged rule); run rows without both shas
  stay `unknown` (`_run_freshness` :929-931, before the predicate).
- E5 (unreadable registry): every reuse is refused, so the probe or run happens (cost, never a false pass). Every run reads `stale`, so each instance that ran gets a `stale_run:` gap. The why names the registry (F-T11 (a)); the `stale_run` gap's owner and door stay as they are; the re-run loop is the node C3-reg-precondition's. INVARIANT: a broken registry never lets an old result or probe speak for a test.
- E6: `очередь: C3-b2 → C3-k` (execution_request.py).
- E7 POSITIONAL (`_run_freshness`, t-1033): the predicate replaces only the comparison at :939, after the file check
  (:927-928), the run-identity check (:929-931) and the measurement check (:932-938). INVARIANT: a missing file is still
  `stale`, a run with no identity is still `unknown`, an unmeasurable helper is still `stale`; `fresh` is reachable only
  through `instance` / `instance_code` (at :939 `same_test` decides by its rule 1 — both identities are kept — so `raw` and
  `file_code` cannot reach the call; error direction: toward `stale`).
- E8 (t-1033, F-T11) TEXT: a refusal caused by the registry never claims the test or its bytes changed. INVARIANT: FR-41
  — an unknown is never reported as a fact. `_evaluate`'s issue and `_match`'s why name the registry (items 5, 6). Known residue (R2): `_stale_receipt` keeps the bare truthiness (a produce site, :1898). On a broken registry `probe_freshness` therefore returns `missing` with `WHY_PROBE_MISSING` (:1814, :1972), a second false cause. Its code is not in owns. C3-reg-precondition closes it in practice (no dispatch on a broken registry); inside a stage that began before, it stays a residue named in that node.
- E9 (conflict on `proof_level.py`): C3-b1 owns `_wanted` and the new `novelty_question_owed`; C3-b2 owns `already_probed`,
  `_product_receipt_repeat`, `_run_freshness` (and `_evaluate` on F-T10 (a)) — function-disjoint (D-0048 form).
- E10 (S-f TEMPORAL): the pins are deltas from the main C3-b2 is based on. INVARIANT: S-f.
- E11 (one row, two producers' vocabularies, F-T1 (a)): after F-T1 the row's `words` hold both `same_test`'s words and `compare_identity`'s, so `acceptable("same", "test_identity.probe_repeat")` is True. That cannot happen today: `same_test` never returns `same` (:876-892), and `compare_identity` never returns `instance` (:834-847). INVARIANT: each consumer is fed by exactly one producer (`probe_repeat`, `run_fresh`, `receipt_holds` <- `same_test`; `run_reuse` <- `compare_identity`). A call that feeds a consumer another producer's word is a review finding.

Measurement (п. 6 (а)). The command below, run by critic t-1039 (verbatim in its trail), gives all 18 recorded instances `('unknown', 'the run recorded no per-test identity')`. With a spy on `same_test`, `reached()` over both recorded manifests (cart-1, 18 rows; local-1-0108, 34 rows) calls it 0 times. So no recorded story reaches `:939`, `:1379`, `:1492`, `:1507` or `:1605`, and 'the six lists equal' is vacuous. The run stays as a smoke check, not as evidence.
   The premise 'not a meaning change' rests on a code trace, re-read in t-1043:
   - `same_test` returns only `raw`, `instance`, `instance_code`, `file_code` or `""` (`proof_level.py:876-892`);
   - the four words are all class `matched` (`gate-registry.json:136-141`);
   - every new consumer lists only `["matched"]`, so the predicate is True exactly when the old truthiness was.

   At `:939` both sides keep their identity (:929-938), so only `instance`, `instance_code` or `""` reach it (E7). The command:
`python -B -c "import json,sys,glob; sys.path.insert(0,'C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts'); import acceptance as A; [print(p, [A.run_freshness_of(i)[0] for i in json.load(open(p,encoding='utf-8')).get('instances',[]) if isinstance(i,dict)]) for p in glob.glob('C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/stories/*/work/windows/*.json')]"`
before and after: the six lists equal.

#### C3-c — folded into C3-R (item 2)

#### C3-d — s5_window (B-179) — designer draft; fork F-T7 to the Lead; queue after S9, C3-b1 and C3-0 (redrafted t-1033)

**Fact (F-d1, re-read t-994 on a6df7fd1).** Today an unmeasured detector of the window is an INFO line, never a gap:
`window_record.verdict` (:1816) fills `info` with `_comment_only`, `_run_freshness_unknown` (:1790-1802, "not a gap - the
story goes on"), `_reason_detail_notes`, `_unknown_target_notes` (:659-667), `_probe_scope_notes` (:633-657) and, when
the window carries `expectation_changes_unmeasured`, the line "expectation changes not measured: <why>" (:1831-1836,
"Not a problem and not a gap"). `acceptance.py:1146-1147` says the same of an unknown run freshness. The row's `decides`
("an unmeasured detector is a gap closed by the critic, never a pass", registry :233) does not describe the code.

**Fact (t-1026 B3, re-read t-1033 on 2151eeef).** `acceptance.validate_window` ACCEPTS the critic's review word to close
an instance's review: for an instance that ran, `item.get("review", {}).get("verdict") != "approved"` -> `review:<iid>`
(:1171); for a handed instance, `not in HANDED_REVIEW_VERDICTS` (`("approved", "unverified")`, :34) (:1161); for a stopped
or probe-gapped instance, `!= BLOCKED_REVIEW_VERDICT` (`"unverified"`, :44) (:1156, :1167). Re-roled `validate`, these
acceptances would be allowed silently once the row's words are `code` (the role-allow rule, `gate_registry.py:37-41`) —
what E-c forbids. So `validate_window` stays `accept`, and C3-d needs C3-0. The window item's review word is the
manifest row's `critic_verdict` or `""` (`window_record.py:1474`); the critic's four words are `approved`,
`approved_with_fixes`, `rejected`, `unverified` (`contract.py:2212-2215`, charter `agents/qa-code-critic.md:84`).

**Measured premise (п. 6 (а)).** `expectation_changes_unmeasured` is present in 4 of the 6 recorded S5 windows of cart-1
(`S5-qa-code-critic-4..7.json`; Grep over `fixtures/stories/cart-1/work/windows`, 4 files; the 6 files listed by Glob
`fixtures/stories/*/work/windows/*.json`); local-1-0108 has no recorded window file (the same Glob lists none). Each says
"a red run has no later pass for … CART-1_TC_009 … and the test file that would say whether the test still exists cannot
…". Under the stricter reading (ii) every one of those four windows, including the story's last (`-7`), would have
carried a blocking gap waiting on the critic. The other INFO classes (run freshness unknown, unknown target, probe scope)
were not measured: it needs `window_record.verdict(..., info=[])` over each recorded window (no shell here; the command
for the Lead or the plan critic: a three-line script calling `window_record.verdict(task_root, json.load(window), [],
info)` per file and counting `info` lines by their prefix). (t-1033: the review acceptance is meant to be
behaviour-preserving; not measured — the control: `acceptance.validate_window(window, task_root)` over the six recorded
windows before and after, the six gap lists equal.) (t-1043, critic t-1039 R10) The review acceptance was emulated on a copy of `acceptance.py` with a C3-0-shaped predicate over item 3's row: all six windows give equal gap lists. A broken consumer (`static_review: ["matched"]`) gives DIFFER on 3 of 6, so the harness can fail. Limit: the recorded windows exercise only the probe-gapped branch (17 `unverified`) and one ran instance (`approved`, failed). The stopped and handed branches rest on item 5's table alone. For F-T7 (ii) (owner question, no edit): `window_record.verdict(..., info)` gives 'run freshness not measured' in windows -2, -3, -6, -7 (18 lines) and 'expectation changes not measured' in -4..-7.

**Recommended direction (i) with F-T9 (a), executable until the Lead answers F-T7 and F-T9:**
given: `C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md` (whole),
`C:/QAFactory/forge-repo/plans/builder-rules.md`, `C:/QAFactory/forge-repo/docs/TESTING.md`; this card and the C3 shared
items (S-a..S-f); the accepted C3-0 card and its diff; t-1026 B3, B9; read, under
`C:/QAFactory/forge-repo/ai-packages/qa-factory/`: `scripts/acceptance.py:25-50,240-252,1052-1180`,
`scripts/window_record.py:633-667,1460-1540,1600-1640,1785-1913`, `handoffs/vocabulary.yaml:293-303`
(`expectation_change_words`), `scripts/contract.py:2209-2215`, `agents/qa-code-critic.md:68-84`,
`references/gate-registry.json` row s5_window :227-248, `scripts/tests/test_gate_registry.py` (the S-f lines)
owns:
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json` (row `s5_window` only)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/acceptance.py` (`validate_window`: the review branch :1154-1174; the constant `HANDED_REVIEW_VERDICTS` :33-34, and the import line it needs)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_window_record.py` (one table of rows, item 5; item 6: no row, the pin exists, R7)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py` (S-f pins of `s5_window` only)
non-goals: `window_record.py` code (S9 owns `verdict`; `build` is only registered, item 2); the run-freshness rule (axis 25:
`run_freshness_of(item)[0] == "stale"` at `acceptance.py:1148` and `_run_freshness` are C3-b2's); C3-b1's gap; the probe
comparisons of `validate_window` (`probe.get("verdict") != "intended_failure"` :1211 and the rest of :1210-1218 — words of
other rows, not this card's; noticed analog, «Not done (t-1033)»); `BLOCKED_REVIEW_VERDICT` (:44, imported by
`window_record.py:75` for its note text); the census (item 8)
handoff: report path given by the Lead
edges: E1-E10 below
DoD: `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_registry.py --check` (exit 0; `s5_window`
absent from the debt block; no F-b for `validate_window`); `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <every owns path>`
and the printed non-slow files; `test_window_record.py` and `test_gate_registry.py` slow — canon
siblings: axis 25 (freshness predicates): `run_freshness_of` is named, unchanged; axis 32 (census): unchanged, item 8;
axis 34 (one road for a person's word on a `review` gap): S9's road, untouched; A1's class: `window_record.build` registered
`produce` (item 2)
- axis 5 (`docs/SIBLING_MAP.md:143`, gate rows <-> sites <-> prose twins), not 'axis 26' (`docs/SIBLING_MAP.md:453` is the word `stand not confirmed`). C3-d changes `s5_window`'s words. Prose twins walked: `skills/qa-story/phases/s5.md:162` ('records the verdict `unverified`' for a probe that cannot run here) and :184 ('the critic's `approved` stands'); `references/code-review-rubric.md:92-93` ('`unverified` is not a pass … only for a window where the test could not run'): checked, no edit (meaning unchanged).
- Waiting findings (R12): (a) `probe_verdict`'s words accepted in `validate_window:1211` and in `proof_level` (see C3-b2 siblings); a later fix needs a function split (`gate_registry.py:831-836`). (c) The critic's review word is read outside the registry: `check_delivery.py:860` and `case_stamp.APPROVING` :317 (twin `report_facts.APPROVING`) accept `{approved, approved_with_fixes}`. Inside the window, `window_record.build` (:1524, :1532, :1625) and `GAP_ORIGIN["review"]` (:318-319) carry the per-kind rule as door text: three copies beside the registry (P31 drift; `build`'s code is outside owns). One finding each, not carded. (Not re-read in t-1043: check_delivery:860, case_stamp:317, window_record:318-319.)
designer: `C:\QAFactory\forge-repo\docs\tasks\specs\20261117-rules-debt-phase2-cards-spec.md` (C3-d, after S9, C3-b1, C3-0, F-T7 and F-T9)
Items:
1. `decides` corrected to the code: "the S5 window is acceptable: run blocks, receipts, reviews and expectation changes
   agree; the critic's review word closes an instance's review only as the instance allows — `approved` for a test that
   ran with its proof, `unverified` (a static review) for one the stand blocked or whose probe could not run here, either
   for one handed to the person; `unverified` closes the review only: the instance stays unresolved (`story_step.py finish` derives the pair, and the report lists it as left with the person, D-0013), so it is never a pass — and any other word or none is a review gap the critic closes; a detector that could not
   measure is said as an INFO line with its reason (owner role: the critic reads it in the window), never a pass and never
   silence". The charter fact behind it: `agents/qa-code-critic.md:76` says `unverified` is 'could not verify'. `window_record.py:36-41` and :344-351 (PROBE_GAP_KIND, 'S8 reads it as the critic's `unverified`') were re-read. The verdict_map entry is unchanged.
2. Sites: `acceptance.validate_window` stays `accept` (B3); `window_record.verdict` re-roled `produce` (B3: it builds
   problems and `info`); `window_record.build` registered `produce` (new: its `item["review"]["verdict"] != "approved"` at
   :1532 writes the review note, the door text, not an acceptance; `build` is defined once in the file, :1332).
3. Row: `vocabulary: code`; `field: null` (the word is passed as a string); `words: ["approved", "unverified"]` — the
   literal words the sites compare (S-c; `approved_with_fixes` and `rejected` are compared nowhere and are refused by
   being outside `words`); `verdict_map: {"approved": {"class": "matched"}, "unverified": {"class": "not_applicable",
   "reason_code": "static_review"}}`; `accepts` (on F-T9 (a)): `"s5_window.review": ["matched"]`,
   `"s5_window.static_review": ["not_applicable:static_review"]`, `"s5_window.handed_review": ["matched",
   "not_applicable:static_review"]`; `promotable: false` unchanged; `unknown_branch` / `on_no_answer` / `waits_at` stay
   `question / wait / window_acceptance` (the window's unknowns that DO block — a missing review, a missing probe — are
   gaps the critic closes); status converted, `debt_ref: ""`. expected from: the charter `qa-code-critic.md:76`
   (`unverified` = "could not verify", a static review, not a rejection) and `:84` (the four words), `_token_problem`'s
   grammar (`gate_registry.py:467-482`), C3-0 item 2.
4. `validate_window`: the four review comparisons become calls of the predicate on `item.get("review", {}).get("verdict")`
   — stopped (:1156) and gapped (:1167): `not acceptable(<word>, "s5_window.static_review")`; handed (:1161): `not
   acceptable(<word>, "s5_window.handed_review")`; ran (:1171): `not acceptable(<word>, "s5_window.review")`. The branch
   order and the `_bound_to` / `stale_review:` / `mechanical_green:` follow-ups are unchanged. `HANDED_REVIEW_VERDICTS`
   (:34) is deleted (no reader left: grep over the package finds it only at `acceptance.py:34,1161`).
5. S-b and the review table: ONE table in `test_window_record.py` (rows of (kind, word) -> review gap or none): ran:
   `approved` -> none; `unverified`, `approved_with_fixes`, `rejected`, `""`, `"Approved"`, no `review` key ->
   `review:<iid>`; stopped: `unverified` -> none, `approved` -> `review:<iid>`; probe-gapped: `unverified` -> none,
   `approved` -> `review:<iid>`; handed: `approved` and `unverified` -> none, `rejected` -> `review:<iid>`; the unreadable registry (the `gate_template` cache patched as in C3-rr item 3, restored in `finally`; if the merged C3-0 exposes no cache, the node stops with a question) -> `review:<iid>` for every kind and word. The absent word is the row's unknown (S-b). expected
   from: the corrected `decides` (item 1), the charter lines of item 3 and FR-59 — never from `validate_window`'s output
   before the change. The builder greps `review:` in `test_window_record.py` first and adds rows to an existing table if
   one pins these; pins found in other files are named in the report, not edited.
6. INFO line (B9): a window carrying `expectation_changes_unmeasured` -> `info` holds `"expectation changes " +` the
   `not_measured` row of `expectation_change_words` in `handoffs/vocabulary.yaml` (:300, `"not measured: {why}"`) with
   `why` substituted, the problem list unchanged; the test reads that row from the vocabulary file (the data), never the
   literal "expectation changes not measured: <why>". Already pinned: named, no new row. `test_window_record.py:2110-2111` (`line.startswith("expectation changes not measured: ")`) and :2117 (the CLI prints the note) pin the line. The literal in that pin equals the data row (`handoffs/vocabulary.yaml:300`, `not_measured: "not measured: {why}"`). Re-sourcing it is optional; recommended: leave it. expected from: the data row and FR-41 ("the reader is told what was
   NOT looked at").
7. (S-f) Pins: `EXPECTED_DEBT` loses `s5_window`, `EXPECTED_CONVERTED` gains it, K-T1.2 N-1, split +1/-1; the F4 `code`
   list gains `s5_window` (`target` -> `code`); the F4 flip control already runs on an in-memory row (C3-0 item 7 — C3-d is
   not dispatchable before C3-0 merges); D13 re-measured. Expected: +1 triple `("window_record.py", "build", "s5_window")`, `D13_ITEM_COUNT` +1 from the base (exactly `:1532 item["review"]["verdict"] != "approved"`).
   - The four comparisons of `validate_window` (`acceptance.py:1156, 1161, 1167, 1171`) are removed by item 4.
   - :1524 and :1625 use the imported `BLOCKED_REVIEW_VERDICT` (`window_record.py:75`), which A26 cannot see (docstring `gate_registry.py:63-66`).

   Critic t-1039 measured this on an in-memory copy; not re-run here. A different measurement is a stop and a question.
8. Census: unchanged. `validate_window`'s row is `{"class": "shape", "owner": "data"}` (`judgment-census.json:7`); its unit
   is the `ValueError` at :1073; the review gaps are list transport (`gaps.append`, census header :3) — no unit, no class
   change. If `test_judgment_census.py` reads otherwise, the node stops with a question.
architecture content: `AR-13 -- the critic's review word is read through gate_template.acceptable`; `AR-22 -- the three
s5_window consumers land with their reader`; `AR-28 -- an absent or unaccepted review word is a review gap; an unmeasured
detector is said, never read as measured`; `AR-29 -- shape unchanged (validate_window's unit); the review acceptance is a
join, owner data`; `AR-20 -- debt -1, converted +1, F4 +1, D13 re-measured`; judgment `none -- the critic's review stays
the critic's judgment, accepted at window acceptance as today; the registry carries which word closes which kind`.
Edges:
- E1 TEMPORAL: behaviour identical for every word the critic writes, per kind (the predicate reproduces the four
  comparisons); after C3-d `validate_window` reads the registry at run time through `gate_template` (once per process).
  Windows recorded before are judged at their next validation exactly as today. INVARIANT: no window that closes today
  is held, and none held today closes.
- E2 (absent / empty review): `""` or no `review` key -> not acceptable -> `review:<iid>`. INVARIANT: no word, no closed
  review.
- E3 (unreadable registry): every review is a gap; the window holds (never a pass). The gap's door ("the critic records
  the verdict") cannot close it while the file is broken — a dead end (FR-57) for that case: F-T11 (a) + R5 (b), decided: the dead end is closed by C3-reg-precondition (no dispatch starts while the file cannot be read). Inside a stage that began before, the gap stays, and the per-site why branches are belt-and-braces. INVARIANT: a broken registry never closes a review.
- E4 POSITIONAL: the order stopped -> handed -> gapped -> ran is unchanged and each branch calls its own consumer.
  INVARIANT: `approved` never closes a test that never ran (stopped) or whose probe never ran (gapped), and `unverified`
  never closes a test that ran with its proof.
- E5 (case and shape): `"Approved"`, `" approved"`, `["approved"]`, `None` -> not acceptable -> gap (C3-0 E3).
- E6 (conflict with C3-b1, same function): C3-b1 adds `novelty_question:` after the review checks; C3-d is based after
  C3-b1 merges. INVARIANT: neither replaces the other's gap.
- E7 (limit): none introduced.
- E8 queue: `очередь: S9 → C3-b1 → C3-d` (window_record / acceptance), `C3-0 → C3-d` (gate_template), S-f order on the pins.
- E9 (INFO lines): absent key -> no line (AR-23: absent says nothing); empty reason -> "no reason was recorded" (:1834).
- E10 (conflict with C3-b1's gap kind): C3-b1's gap is a real gap, not an INFO line. INVARIANT: (i) never downgrades a gap to
  INFO.
Under (ii) instead: the listed detectors become gaps closed by the critic; owns add `window_record.verdict`, the census
rows (S-e) and one row per detector; a plan critic on the meaning change; cost: the four cart-1 windows above would have
held. Items 2-8 above hold under (ii) too.

#### C3-reg-precondition — one stop when the gate registry cannot be read (F-T11 residue, critic t-1039 R5 (b), Lead 17.11) — after C3-0; controller.py queue after FL4

Why: with an unreadable registry, every converted site refuses, and three of them loop: `_run_freshness` gives a stale_run gap whose re-run reads stale again; `_evaluate` refuses every receipt, so the probe runs again; `validate_window` gives a review gap no verdict closes. They also answer the same cause five ways (P31). This card puts one survivor in front of all of them (AR-15). The per-site why branches of C3-b2/C3-d stay as belt-and-braces (Lead decision).

given: `C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md` (whole), `C:/QAFactory/forge-repo/plans/builder-rules.md`, `C:/QAFactory/forge-repo/docs/TESTING.md`; this card; the accepted C3-0 card and its diff (`gate_template.py`: `registry_problem(*, registry=None) -> str`, cache `_READ`). Read, under `C:/QAFactory/forge-repo/ai-packages/qa-factory/`:
- `scripts/controller.py:5364-5377` (validate head), `:5493-5529` (dispatch branch head), `:5185-5189` (`apply` runs `validate` in the commit), `:2470-2482` (`_passed_by_person`), `:5612` (a dispatch-branch use of it), `:2109-2147` (`prepare`, read-only), `:9206-9236` (the stage loop's `prepare_stage`);
- `scripts/gate_registry.py:16-19, 97-106, 427-456`;
- `design/controller-blocks.md:1-38` and rows :50-53 (the row form);
- `design/state-exits.md:1-20, 138-143`;
- `scripts/tests/test_state_exits.py:43-54, 124-128`;
- `scripts/refusal_registry.py:41-44` (controller.py is one `operation` entry);
- `scripts/driver_dispatch.py:38-107` (KNOWN_REFUSALS, unchanged);
- `UPGRADE.md:71-90` (the reinstall steps);
- seam precedent: `scripts/tests/test_gate_registry.py:1108-1119` on C3-0's branch.

owns:
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/controller.py` (`Controller.validate`, the `dispatch` branch only: one block and the import it needs) — HOT
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/design/controller-blocks.md` (one row in source order; the header counts it moves)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/design/state-exits.md` (one row in "What an infrastructure failure leaves", :138)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_controller_state.py` (one table, item 4)

non-goals:
- `gate_template.py`, `gate_registry.py`;
- any call of `gate_registry.analyse` / `--check` / `main` from the controller (`gate_registry.py:16-19`), and `audit_factory.py` (the doctor);
- `gate-registry.json`, `test_gate_registry.py` (no row-word comparison is added; D13 unchanged), `judgment-census.json` (no new unit);
- `driver_dispatch.KNOWN_REFUSALS` (F-T13 (a)); `prepare`, `next_action`, `_next_action_for_state` (F-T14 (a));
- the `accept` / `checkpoint` / `resume` / `initialize` branches;
- the per-site texts of C3-b2/C3-d;
- `docs/SIBLING_MAP.md` (its axis-5 line is the Lead's at acceptance, item 5).

handoff: report path given by the Lead
edges: E1-E11 below
DoD: `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_registry.py --check` exits 0 (no registry edit; the debt block unchanged). Then `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/controller.py C:/QAFactory/forge-repo/ai-packages/qa-factory/design/controller-blocks.md C:/QAFactory/forge-repo/ai-packages/qa-factory/design/state-exits.md C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_controller_state.py`, and the printed non-slow files. `test_controller_state.py` and `test_controller_blocks.py` are `test_controller_*` (builder-rules 7b): judged by the batch canon and named in the report. `test_state_exits.py` is run if printed and not slow.
siblings: axis 5 (`docs/SIBLING_MAP.md:143`): this is the one stop for "the registry cannot be read" (AR-15: a new survivor is named on its axis, item 5). The per-site texts (C3-b2 items 4-6, C3-d E3) are belt-and-braces. `_stale_receipt` / `probe_freshness` `missing` is the residue named in C3-b2 E8. Open C3-0 finding (its report :54): audit A1 says `gate_template.py` is reachable from nothing; whether this import from `controller.py` (a CLI script) clears it is not established.
designer: `C:\QAFactory\forge-repo\docs\tasks\specs\20261117-rules-debt-phase2-cards-spec.md` (C3-reg-precondition, t-1043)

Items:
1. **The block.** In `validate`'s `dispatch` branch, right after the contract check `required` (:5515-5517: `raise ValueError("dispatch contract incomplete")`) and before the closure test (:5518-5523):
   - read `problem = registry_problem()` (`from gate_template import registry_problem` at the point of use, the file's "late" import style);
   - when it is non-empty, build one text with the stable prefix `gate registry unreadable:`, e.g. "gate registry unreadable: the plugin's references/gate-registry.json cannot be read (<problem>). Owner: factory - a defect of the install, not of the story; nothing is wanted from you. Reinstall or update the qa-factory plugin (UPGRADE.md, step 3), then start the stage again. No stage starts until the file reads, because every reuse and review acceptance reads it.";
   - pass it through `blocking, _ = self._passed_by_person(p["stage"], [text])`, as the branch's other blocks do (:5612), and `raise StateConflict(blocking[0])` when it is still blocking (F-T12 (a)).

   The text reports and does not ask (FR-3: a factory reason is never put as a choice); the person's word is the standing FR-4 road. The builder reads `waiver.split_overridden` for whether a pass over a factory-owned block is filed as a factory finding (FR-4); this was not read here. Expected from: AR-28 / FR-59 (an unknown never becomes a pass at a stage boundary), FR-4, AR-9's change check (`architecture.md:111`: the door and the person's-word route), the Lead decision R5 (b).
2. **controller-blocks.md row** (source order, beside the other `validate` rows): `| \`validate\` | \`StateConflict\` | gate registry unreadable: the plugin's references/gate-registry.json cannot be read | \`person\` | a factory defect (FR-3): reinstall or update the plugin, then start the stage again; a person's recorded words pass it (\`waiver.py --stage <S> --block "gate registry unreadable" --words-file <file>\`), and the stage then runs with every converted site refusing reuse (C3-0 E2) |`. The header counts (352 blocks, route `person` 17, `controller-blocks.md:3,20`) move by one. If `tools/controller-blocks-gen.py` places the row, its output is used. If `test_controller_blocks.py` does not pin the header counts, they still move (the file is the walk).
3. **state-exits.md row** in "What an infrastructure failure leaves" (:138-143): `| a story whose next dispatch is refused because the plugin's \`references/gate-registry.json\` cannot be read (absent, 0 bytes, not UTF-8, not JSON, duplicate keys, not an object, no \`rows\` list) | a broken or partial install or update of the plugin | reinstall or update the plugin (UPGRADE.md step 3); the next \`dispatch\`, in a new process, reads the file again and goes through; a person's recorded word passes it (\`waiver.py\`) | \`test_controller_state.py\` |`. `test_state_exits.py` reads the first backticked token of column 1 (:43-54); extra names are harmless. The doors it checks (`dispatch`, a test file on disk, :124-128) exist.
4. **Test: one table in `test_controller_state.py`** (keep, layer `detector`, covers `controller.py`, `test-layers.json:1082`). The builder greps for an existing dispatch-refusal table first. If there is none, it adds one parameterised function (no new file). Rows (id -> expected):
   - `absent`: `gate_registry.PLUGIN_ROOT` swapped to an empty temp dir and `gate_template._READ.clear()` (restored in `finally`, the precedent seam) -> the dispatch is refused with `StateConflict`, the text starts with `gate registry unreadable:`, names "the file is absent", and the journal records no dispatch;
   - `zero-bytes`, `not-json`, `not-utf8`, `no-rows`: `_READ[:] = [(None, <the load_registry reason>)]` or `[({"rows": "x"}, "it carries no `rows` list")]` -> refused, each naming its reason;
   - `passed-by-word`: `no-rows` plus a recorded waiver for the block `gate registry unreadable` -> the dispatch is recorded;
   - `live`: the live registry -> the dispatch is recorded (control);
   - `malformed-first` (POSITIONAL): `no-rows` and a request missing `input_hash` -> `ValueError("dispatch contract incomplete")`, not the registry text;
   - `after-reinstall` (TEMPORAL): refused; then the root restored and `_READ` cleared -> the next dispatch is recorded.

   Expected from: AR-28, FR-4 and the decided text above; never from the code's output.
5. **SIBLING_MAP axis-5 line (the Lead's, at acceptance):** "one stop for an unreadable registry: `controller.validate` dispatch branch via `gate_template.registry_problem()` (C3-reg-precondition); per-site why texts are belt-and-braces". It is a mechanism path (`tools/mechanism_gate.py`, 7 `SIBLING_MAP` hits; prefix not read), so the builder reports it under "Needed from integration".

architecture content: `architecture: AR-9, AR-13, AR-15, AR-25, AR-28 -- <how kept>`, in the gate's own form (`tools/architecture_gate.py`; the grammar is not copied here). Points:
- AR-9: the refusal names what it expected and two doors (reinstall; the person's word). Change check `architecture.md:111`: controller-blocks row, `test_controller_blocks.py`, `refusal_registry.py --check` (controller is one `operation` entry, `refusal_registry.py:41-44`).
- AR-13: read only through `load_registry`, via `registry_problem()` (:166).
- AR-15: one survivor, named on axis 5 (:180).
- AR-25: a `state-exits.md` row with its reversing command (:261).
- AR-28: an unreadable registry never becomes a pass at a stage boundary, pinned by item 4 (:282).
- AR-29 (:155): the check is class `shape` (a package file reads and has `rows`), owner data; it sits in the existing unit `controller.py::validate` (`judgment-census.json:245`, shape/data), so there is no new census row. If the builder places the raise in a helper (a new unit), the node stops with a question.
- judgment: `judgment: none -- a readability check of a package data file inside the existing shape unit controller.validate; the person's pass is the existing waiver road`. Per check: the readability check serves DATA (code), census class shape; the pass serves INTENT (the person, FR-4).

Edges:
- E1 (empty / absent): an absent file, 0 bytes or no `rows` gives a reason, so the dispatch is refused. INVARIANT: no stage starts on a registry that cannot be read (AR-28).
- E2 (present but incomplete, R15): `registry_problem()` covers a registry that cannot be read, not a missing consumer. A file that parses, with `rows`, but lacks a consumer, `words` or `verdict_map` gives "", so the precondition passes; the site's `acceptable` is False and the site prints its usual cause. INVARIANT: the precondition never stops a registry that reads (no false stop). That blind spot is held by CI (A26 `--check`; the positive rows of every consumer table turn red on a consumer-id typo).
- E3 TEMPORAL:
  - (i) the registry appears after a reinstall. `gate_template` caches per process, and a failure is cached as such (`_READ`, :31-37 at a4aca646). A CLI call is a new process, so the next call reads the file again. The driver imports `controller` in-process (`driver_dispatch.py:2141` and others), so a driver running across a reinstall keeps the cached failure until it restarts. UPGRADE.md:71 asks to stop active factory work before a reinstall; the door says "then start the stage again".
  - (ii) Before C3-0 merges, `gate_template.py` is absent, so this node cannot be built (order).
  - (iii) Before this node, a broken registry loops at the sites (R5); after it, the first dispatch stops.
  - INVARIANT: a fixed registry is read by the next process, and a cached failure only ever stops, never passes.
- E4 POSITIONAL: after `validate_record("Dispatch", p)`, the running-dispatch refusal (:5501-5514) and `required` (:5515-5517); before the closure test (:5518-5523) and every later check. INVARIANTS:
  - (i) a malformed request is still refused as `ValueError` first (the call's fault before the install's, FR-46);
  - (ii) the running-dispatch refusal keeps its text byte for byte (finishing a running dispatch is an `accept`, which is not blocked);
  - (iii) no dispatch is committed while the file cannot be read, on any road that commits one: `story_step.py start`, `rework`, relaunch and retry packets, the driver. All of them go through `apply` -> `store.commit` -> `validate` (:5188);
  - (iv) the closure test and every later check still run on an admitted dispatch;
  - (v) the block reads only `p["stage"]`, which `required` guarantees.
- E5 one road (P31, AR-15): one precondition for every stage and role alike, keyed on no stage, language or project; no per-site variant.
- E6 (not covered, by design): `accept`, `checkpoint` and `resume` of an admitted dispatch (the stage is already entered; its sites refuse with the registry why), and `initialize` (it runs no converted site). INVARIANT: a broken registry is a pass nowhere (the sites err toward not-acceptable, C3-0 E2); the precondition only stops it early.
- E7 doctor separation: this is a read through `registry_problem()` (`load_registry` + `structural_error`, `gate_registry.py:427-456`), never `analyse`, `--check` or `main`. `gate_registry.py:16-19` forbids the A26 AUDIT in the project doctor; a read is not the audit. INVARIANT: no A26 audit runs in a project.
- E8 (limit): none introduced. The reason is passed whole; `load_registry`'s sentences are short, and a JSON error carries its position.
- E9 (cost): one file read and parse per process at its first dispatch (cached); nothing on other operations.
- E10 (conflicts):
  - `controller.py` is HOT: S9 owns `_s5_gap_problems`; FL4 owns `BINDING_KEYS`, `build_rework_request` and `main`'s rework parsing (S9/FL spec :334-336). This node owns `validate`'s dispatch branch: function-disjoint.
  - `controller-blocks.md` is row-disjoint, but the header counts are shared if S9/FL4 add blocks: the later merger re-derives them (D-0048).
  - `очередь: S9 → FL4 → C3-reg-precondition` (controller.py, controller-blocks.md); `C3-0 → C3-reg-precondition` (gate_template).
- E11 (driver): the refusal matches no `KNOWN_REFUSALS` row (`driver_dispatch.py:38-107`), so it goes to the conductor (FR-48, F-T13 (a)). The conductor cannot reinstall; it reports the defect (FR-3). INVARIANT: no silent pass and no question about our own defect; the same refusal repeats until the reinstall.

Measurement (п. 6 (а)): not a meaning change for any story on a sound install (`registry_problem()` is "" on the live registry: the C3-0 row "registry-problem: the live registry", `test_gate_registry.py:1124` on its branch). Not measured here (no shell).

#### C3-e — folded into C3-R (item 3)

#### C3-f — folded into C3-R (item 4); C3-g — baseline_identity (B-281) — wave 3, after C3-0

C3-g owns: gate-registry.json (row `baseline_identity`), `ai-packages/qa-factory/scripts/baseline_contract.py`
(`deployment_readiness`) per F-D1, its registry `test` file `scripts/tests/test_baseline_contract.py` (keep, fast; one
row). Dispatch after C3-0. S-b names the refusing function (`baseline_contract.validate_baseline_request` is the
candidate; t-994 read: it returns an error list, and the raises are in `build_baseline_fields` (:50-52) and
`baseline_receipt` (:112-116) — the designer of C3-g confirms which one refuses an unknown old-build identity);
`deployment_readiness` never refuses (docstring :175-182: `ready` "is always true", gaps carry `blocks_execution: False`,
:216-221) and goes through `acceptable(…)` — under fork F-T3 with a consumer of its own and the receipt's `status` as the
row's field, not `provenance.baseline` (read by no script).
(t-1033, B1) Also owns `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py` (S-f pins of
`baseline_identity` only, plus — under F-T3 (a) — the `provenance.baseline` consumer pins F1 :630, :639-647 and K-N2.12 NEG
:285-292); item: re-measure D13 with `GR.analyse` before and after and name the move (S-f); F4 `code` list gains
`baseline_identity` (`target` -> `code`). TEMPORAL: S-f.

#### C3-h — stand_identity (B-257) — wave 3, gate_preflight queue position 4

owns: gate-registry.json (row `stand_identity`); `ai-packages/qa-factory/scripts/tests/test_stand_identity.py` (one row);
code sites only if S-b is red (the row's produce/validate sites in `runtime_probe.py`, `gate_preflight.py`,
`driver_stage_build.py`); (t-1033, B1) `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py`
(S-f pins of `stand_identity` only: debt/converted/split, F4 `code` list `target` -> `code`, D13 re-measured and named)
Item: no accept site — converts by S-b/S-c alone (F-D1 does not apply). Row edit: `vocabulary: code`, words unchanged
(`_derive_probe` compares all five, critic's read); sites keep their roles (produce/dispatch: none is accept). S-b: a
stand whose build cannot be identified -> the `stand_identity` question before the stage, the stage waits; the person's
word recorded in the row's policy file covers the same scope keys next time. expected from: the registry row. TEMPORAL
(t-1033): S-f — C3-h is last in the expected order.

#### C3-i — folded into C3-R (items 5-8); it leaves the gate_preflight queue (no code)

#### C3-j — s5_stand_limits -> question, answer persisted (B-282) — wave 3, gate_preflight queue position 2

The registry: "the environment registry" of the owner's word is **the environment record**,
`qa-factory/records/environment-properties.json` (`environment_record.py:33 RECORD_REL`; its docstring: what a person
accepted ONCE as a property of this environment, read by the gates before they build a card). Its ONE writer is
`environment_record.record` (:326); the gate's reader is `environment_record.covering` (:300) through
`Rehearsal._environment_cover` (`gate_preflight.py:4214`); the key of a gap row is derived by `environment_record.lasting`
(:133) through `Rehearsal._lasting_of` (`gate_preflight.py:4200`); the driver writes the person's `accept always` through
`stand_gaps.record_lasting` (`stand_gaps.py:1243-1249`). Alternative carrier: the project answer registry
`project_knowledge.py` (`records/project-knowledge.json`) — fork F-C2 (decided (a)).
owns:
- `ai-packages/qa-factory/scripts/environment_record.py` (a third scope beside `LEVEL`/`CASE` :35: `stand_limit`, its key fields, its branch in `lasting`, `current_key` :165, `near_miss` :188, and `record`'s CLI form)
- `ai-packages/qa-factory/scripts/gate_preflight.py` (`_e2e_limit` :3088, `check_s5_stand_limits` :3165, `_stand_limit_card` :3242) — HOT
- `ai-packages/qa-factory/references/gate-registry.json` (row `s5_stand_limits`)
- `ai-packages/qa-factory/scripts/tests/test_environment_record.py`, `ai-packages/qa-factory/scripts/tests/test_gate_preflight.py` (rows)
- `ai-packages/qa-factory/scripts/stand_gaps.py` (`collect` and the function that calls `record_lasting`, so a `stand_limit` gap row is collected and its `accept always` recorded) and the answer-vocabulary row that offers `accept always` on a stand-gap card (`references/question-vocabulary.json` `stand_gap_words`); the new card is a GAP ROW of the stand-gap flow (`scope: "stand_limit"`, `property_key` from `lasting`), not a `PERSON_DECIDES` finding; test: one row in `test_environment_record.py` or the stand-gap test that drives answer -> `record_lasting` -> a record row under the stand_limit key -> the next rehearsal covers it (the AR-22 round trip)
- `ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json` (S-e; based after `wave-a/integrate`)
- (t-1033, B1) `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py` (S-f pins of `s5_stand_limits` only: debt/converted/split, F4 `code` list `target` -> `code`, D13 re-measured and named — `check_s5_stand_limits` re-roled `produce` moves its comparisons' attribution)
non-goals: writing `config.json` `environments[].measured`; `manual_capture` readers of the config measurement
Items:
1. Today `unmeasured` is a note, never a card (`check_s5_stand_limits` :3191-3194). After: `unmeasured` builds ONE gap
   card per profile at the gate where the check runs (gate A rehearsal, :6084-6093 — fork F-C1, decided (a)), saying: the
   stand's page load is not measured and the page objects wait at most N s, so whether the e2e rows of `<profile>` fit
   this stand is unknown. Options: (a) `accept always` for this stand (recorded in the environment record); (b) the
   existing handed door `executor unavailable: <profile>`; (c) `<case id>: manual` (existing). expected from: the owner's
   word (spec closing sections, F-O1 s5_stand_limits).
2. The gap row carries `property_key` from `lasting`: key `{scope: "stand_limit", environment: <stand name>,
   definition_sha: <stand definition sha, as CASE keys use>, contour: <profile_id>, wait_s: <page_object_max_wait_s>}`;
   `_environment_cover` is asked BEFORE the card: a live row under exactly this key -> no card, one note "not asked —
   <their words>, as you recorded on <date>". test: rows in `test_environment_record.py` (key built / refused when stand
   or wait absent) and `test_gate_preflight.py` (unmeasured -> card; same stand + same wait with a recorded row -> note,
   no card; wait changed -> card says the earlier answer no longer applies). expected from: FR-7 ("a boundary a person
   has answered is never re-asked with the same text") and the owner's word.
3. The writer and its reader land in ONE commit (AR-22).
4. Registry row: `unknown_branch: question`, `on_no_answer: wait`, `waits_at: gate_a` (F-C1 (a)), closed by and
   addressed to the person; `check_s5_stand_limits` re-roled `produce` (E-c table; no accept site after C3-j: the record
   read is `_environment_cover`'s).
5. (t-1033, S-f) Re-measure D13 with `GR.analyse` before and after and name the move; debt/converted/split and F4 by the
   S-f deltas.
Edges:
- E1 (absent stand name / placeholder): no key, the card is shown without `accept always`. INVARIANT: nothing is
  recorded under a placeholder key.
- E2 (absent `page_object_max_wait_s`): `unmeasured` names the missing wait; no key (the wait is part of the key) — the
  card offers (b)/(c) only. INVARIANT: a cover never holds for an unknown wait.
- E3 (unreadable record): said once, covers nothing, card shown (FR-59).
- E4 (the existing off switch of the stand-limit check): unchanged — no card, no record read.
- E5 (conflict with the reporter rehearsal, which is skipped only when the state is `over`): unchanged — an
  `unmeasured` profile is still rehearsed. INVARIANT: the reporter proof is not lost to the new card.
- E6 TEMPORAL: the record file may not exist before any `record`; readers treat absence as "no rows". The new scope
  exists only after this card; older records with two scopes stay valid (an extra scope is additive; if the loader
  refuses an unknown scope the builder returns a question).
- E7 POSITIONAL: the cover is read only on the card branch, never before the measurement check. INVARIANT: a recorded
  measurement in the config always wins; the record never hides `over`.
- E8 (outside input): the person's words are outside input; `record` already cuts and validates them — rows AT and
  BEYOND its existing limit if the test table does not hold them.
- E9 (temporal, FR-4): a waiver already recorded for `e2e stand limit: <profile>` still passes the new card. INVARIANT: an
  informed word recorded before the change is never re-asked.
- E10 (t-1033, S-f TEMPORAL): pins are deltas from the main C3-j is based on; C3-j follows C3-rr on `gate_preflight.py`.
  INVARIANT: S-f.
architecture content: `AR-22 -- the answer's writer and its gate reader in one commit`; `AR-24 -- the person's words
reach the record whole`; `AR-28 -- an unmeasured limit is asked, never run on a guess`; `AR-29 -- owner intent for the
answer, the cover is a key join (xref)`.

#### C3-k — provenance_acceptance (B-255) — designer first; wave 3, gate_preflight queue position 3

Many accept sites across many files; the row's `decides` lists its own residue. Not dispatchable from this text: designer
refines (after C3-0 under F-D1 (b)) into per-file steps, settling F-T2's second half (whether `acceptable` delegates the
record check to `profile_contract.acceptable_provenance`, and the bare `not_applicable` residue of `provenance.fingerprint`
/ `provenance.manual_capture`, registry :81,83, which `acceptable_provenance`'s `ACCEPTS` does not hold,
`profile_contract.py:877`); `очередь: C3-b2 → C3-k` (execution_request.py), `C3-R → C3-k` (run_suite.py is not touched by
C3-R; the queue is kept only for the registry file).

(t-1033, A2) **The dead consumer `provenance.environment_preparation` is removed.** It sits in the row
`environment_preparation` (`gate-registry.json:325`, `accepts: {"provenance.environment_preparation": ["matched"]}`); after
C3-R no word of that row maps to `matched` (words `blocked`/`unknown`, both unknown, :320-324), so under C3-0 it can accept
nothing, and no `scripts/*.py` reads it (Grep over `scripts/*.py`: only `tests/test_gate_registry.py:631-632, 640`, which are
the positive control). Direction chosen: C3-k's registry commit REMOVES it from the row `environment_preparation`; when
C3-k wires `environment_preparation._run_step` (a `provenance_acceptance` accept site, registry :49; the deploy's proof
step, as the row's own `decides` says at :314) through `acceptable`, the consumer that reader calls is added in THAT
commit, under a row whose `promotable` is false (the guard F1 pins, `test_gate_registry.py:637-647`: a person's word never
stands in for the deploy's proof) — never moved ahead of its reader (AR-22; the same class as F-T3's `provenance.baseline`).
The F1 lines `:631-632` and the `environment_preparation` pair of the loop `:639-647` move in the same commit.

(t-1033, B1) Also owns `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py` (S-f pins of
`provenance_acceptance` only, plus the A2 consumer pins above); item: re-measure D13 with `GR.analyse` before and after
and name the move (S-f: `provenance_acceptance` holds the most triples of the set, :915-955); F4 `code` list gains
`provenance_acceptance` (`target` -> `code`). TEMPORAL: S-f; C3-k is based after C3-g (the F1 block is shared with C3-g's
`provenance.baseline` lines).

gate_preflight queue (HOT, one stream at a time): **C3-rr → C3-j → C3-k → C3-h** (C3-i left it: no code, F-i2; C3-rr joined
it in t-1033), each after any open node of a TAKEN batch that owns `gate_preflight.py` (§4).

---

### C4 — F-O2's condition: a language with no probe row takes the role's probe road

Dispatchable now on fork B-1's recommendation.

given: factory-rules.md (whole), builder-rules.md, TESTING.md; read: the `probe_verdict` row of
`references/gate-registry.json`, `scripts/probe_by_code.py` (docstring), `scripts/red_sandbox.py` (`--probe`),
`scripts/tests/test_probe_by_code.py` (its world builder), `references/detectors.json` (`assertion_probes`)
owns: `ai-packages/qa-factory/scripts/tests/test_probe_by_code.py` (one table row) — on B-1 (a)
non-goals: any probe row in `detectors.json` (F-O2 (a): none now); `probe_by_code.py`, `red_sandbox.py`, the window code
(a red row is a found defect, E1)
handoff: report path given by the Lead
edges: E1-E4
DoD: `scenario_walk.py --witness-for ai-packages/qa-factory/scripts/tests/test_probe_by_code.py`; the file is slow
(221.4 s, `slow_tests.json`): judged by the batch canon
siblings: `test_red_sandbox_probe.py` (keep, `test-layers.json:4321`) — the builder takes the row there instead if the
receipt reader lives there and says so; live proof B-373 stays queued in live-runs
Item: one row: a test file whose suffix has NO `assertion_probes` row (the builder picks one and shows from
`detectors.json` that it has no row) -> `probe_by_code` writes a record that names what was not read and names the door
`red_sandbox.py --probe`; THEN the role's road: the same test probed through `red_sandbox.py --probe` (stub run, as the
file's world does) leaves a receipt, and the reader that decides whether the window may close (the builder names it)
counts that receipt — the stage does not stop. expected from: the owner's word F-O2 (spec closing sections: on a language
with no row the role's own probe must be a working road end to end, the stage does not stop), P30, and the registry
`probe_verdict` row's door.
Edges:
- E1: if the road is broken (the receipt is not counted, or `--probe` refuses the suffix), the builder stops and returns
  the evidence as a question; the Lead opens a fix node (P22). INVARIANT: no red row is committed; the defect is never
  left implied.
- E2: an incomplete record never replaces a judged one. INVARIANT unchanged.
- E3 (one road, P31): the row must not branch on the language NAME; the suffix reaches the shared mechanism through the
  data lookup like every other language.
- E4: `--probe` output is the factory's own (not outside input): no battery.
architecture content: `AR-1 -- the suffix is read through the data row lookup; no language name in code`; `AR-28 -- no
row is a named unknown with a door, never a stop`; judgment `none -- a test of an existing road`.

---

### C5 — F-O4: the conductor prompt, replace vs append — ONE measured experiment (procedure for the Lead)

Not a builder card. The owner: «ок и учти что мы планируем оркестратора полностью заменить дирежёром. Надо что бы он
справлялся» (spec closing sections).

Facts: the conductor is called with `system_file=references/conductor.md` at `driver_conductor.py:337` and
`driver_stage_s8s9.py:451`; `driver_runner.claude_cmd` (:593) turns it into `--append-system-prompt-file`
(`driver_runner.py:606-607`). A run's conductor sessions are recorded in `state/conductor.jsonl`
(`experiments/measurers/conductor_families.py`). No earlier experiment found (Grep "system-prompt" over `experiments/`:
0; not controlled by a positive hit of the same form — treat as "not found", not "absent").

Procedure:
1. Measure the premise (CLAUDE.md pt. 6a): `claude --help` on this machine — does a REPLACING flag exist? Record the
   verbatim help line. If none exists, the experiment ends: the prompt half of X3 becomes a real limit (debt file "Real
   limits") with that line as its reason.
2. Pick recorded conductor questions from the latest stand run's `state/conductor.jsonl` (fork F-E1 on how many): at
   least one that needs tool use and one `ask_person`.
3. In a project copy (`experiments/measurers/prepare_copy.py` if present; P8: no trace in the project), run each question
   twice with the same model and allowed tools: (A) as today, (B) with the replacing flag; nothing else differs.
4. Judge per run, in `experiments/conductor-system-prompt/notes.md` (PROJECT.md п. 5 notebook): (a) turns; (b) input and
   cache tokens; (c) the answer obeys `references/conductor.md` "Your answer" (shape valid); (d) the decision: same as
   (A), or different with a reason the Lead accepts; (e) **copes without the host's default tool guidance**: every tool
   call well-formed, no refused or malformed call, no command the guard refuses, no lost turn re-explaining tools. (e) is
   the owner's added measure; a (B) run that fails (e) is "does not cope" whatever (a)/(b) say.
5. Verdict to the owner in plain words: switch / keep (real limit) / switch with an added short tool section in
   `conductor.md` (then one more (B) run). No money figures in the notebook (P18).
FR: F (FR-26: read the raw transcripts before any number is a finding). A switch, if chosen, is its own builder node
(`driver_runner.claude_cmd` + the two callers), with an FR-33 live-proof row in `live-runs`.

---

### S9 — X10, a person's word on a `review` gap (FR-57)

card: `docs/tasks/specs/20261117-rules-debt-phase2-s9-fl-cards-spec.md`

### S10 — G15, read heads as data (F-L6 (a)) — HOT `stage_guard.py`

The spec's S10 stands; facts re-read: `host_adapter.py:452 _READ_HEAD`, `:525 _read_refusal`;
`stage_guard.py:2509-2512 READER_COMMANDS`, `:2589-2590 _is_reader`; `tests/role_replay.py:30-36` derives `_READ_ALTS`
from `_READ_HEAD` (must follow).
**Found today, in S10's own function**: `stage_guard._is_reader` does `name.rstrip(".exe")` (:2590) — `rstrip` strips the
CHARACTERS `.`, `e`, `x`, not the suffix, so `catx` -> `cat` is treated as a reader (errs toward the reader exemption,
i.e. permissive). Added to S10's adversarial list and items: use `removesuffix(".exe")` (after lowercasing, if the
existing code lowercases).
Adversarial heads that must stay refused / non-reader: `python`, `bash`, `pwsh`, `node`; a head with a path
(`/usr/bin/rg`); `.exe` and case variants; `catx`, `lsx` (the rstrip class); an empty or unreadable table (falls back to
the in-code floor = today's lists, never "any head"); a table row adding a writer to the read heads. The two lists stay
separate (READER_COMMANDS: runner-guard "mention" heads; `_READ_HEAD`: a no-Bash role's one plain read).
owns: `ai-packages/qa-factory/references/launch-causes.json` (new tables for the two lists, per the spec's F-L6 (a));
`ai-packages/qa-factory/scripts/host_adapter.py` (`_READ_HEAD`, `_read_refusal`); `ai-packages/qa-factory/scripts/stage_guard.py`
(`READER_COMMANDS`, `_is_reader`) — HOT; `ai-packages/qa-factory/scripts/tests/role_replay.py` (`_READ_ALTS`)
DoD: witness-for over owns; slow guard tests named by the walk: canon.
Queue: taken batches name `stage_guard` (onboarding-hooks/6, onboarding-forge/2) and `host_adapter` (onboarding-hooks/7)
— the Lead reads those node rows' status before launch (§4); if open, `очередь:` lines.
architecture content: `AR-1 -- the head lists are data rows with an in-code floor`; census safety (§1).

### FL1 — R2: resolve a hand-typed pytest id at store time (F-L1 (a))

owns: `ai-packages/qa-factory/scripts/manifest_put.py` (the store path of a test id — the plan names the function; no
id resolver among its functions today, Grep `node_ids` over the file: 0 hits, control: the same Grep finds `node_ids` in
`run_suite.py`… not run — treat as "not found"); a table row in the keep test that judges `manifest_put` (witness-for
names it)
Item: a hand-typed pytest node id is resolved through `node_ids` (the one collect reader) when the fragment is stored; a
store where no collect is possible keeps the id and marks it "not verified" (FR-16 "at the moment it is stored"; FR-59).
expected from: FR-16 text and the spec's F-L1 (a).
Edges: E1 (no collect possible) -> "not verified", never refused and never "missing". E2 (limit) — a collect call is
bounded by the existing collect timeout; at timeout -> E1. E3 — the id string is a role's output (internal): no battery.
Queue: `manifest_put.py` is in thinking-roles/6 TR4-17 (spec F-L1 note; batch not taken) and is named in TAKEN
onboarding-forge/1 and /2 rows — status not read today (§4). Needs a designer pass for the function name. (t-994: C3-b1
also owns `manifest_put.CRITIC_FIELDS` — function-disjoint with FL1's store path; `очередь:` only if the Lead's read of
the taken rows says one stream at a time.)

### FL2 — R3: "skipped because the product has no such surface" (F-L2 (a))

card: `docs/tasks/specs/20261117-rules-debt-phase2-s9-fl-cards-spec.md`

### FL4 — R4: the S7 rework door for a case-less `bug_candidate` (F-L4)

card: `docs/tasks/specs/20261117-rules-debt-phase2-s9-fl-cards-spec.md`

### FL9 — X2 residue: the oracle door by capability, not by pytest (F-L9)

owns: `ai-packages/qa-factory/scripts/s5_precheck.py` (`_open_oracle_door` :1654 only); one row in `test_s5_precheck.py`
(slow: canon)
Item: `_open_oracle_door` names the binding road by a capability key of the test file's language row in
`references/detectors.json` (marker form vs the `manifest_put` fragment), never by the language name; today it names the
pytest marker for any file (:1661). expected from: P31, AR-1, the spec's F-L9.
Edges: E1 — the capability key itself is NOT established today (the spec says it needs confirming in `detectors.json`);
if no such key exists, the builder stops and returns a question (adding a data key is a new row with a default, AR-1
form — the Lead decides). INVARIANT: no language name enters the branch. E2: a language with no row -> the door says how
to bind through the `manifest_put` fragment (the road every language has). (t-994: FL9 t-962 stopped at its E1 with no
diff, `a18336d2`, per t-989 F-c2; its line :1654 drifts by about +19 after `wave-a/integrate`. C3-c no longer queues
behind it: C3-R moves no code in `s5_precheck.py`.)

---

### S1b — the debt file's second pass (LAST)

Runs after every phase-2 node it moves is accepted (spec S1 E6). One writer of the debt file at a time.
given: the spec §0, §2, S1 (edges); this card; the accepted handoffs of the nodes it moves
owns: `ai-packages/qa-factory/design/factory-rules-debt.md`; `ai-packages/qa-factory/design/factory-rules.md` (the *Check*
lines of FR-5 and FR-23 only, F-L12); `ai-packages/qa-factory/scripts/tests/test_null_outcomes.py` (the K0.15 block,
:588-597, only)
non-goals: any code; any row not listed; `plans/BACKLOG.md` (frozen; B-ids closed by the integrator's `piles.py close --id`)
DoD: `scenario_walk.py --witness-for <the three owns>`; `python -B ai-packages/qa-factory/scripts/tests/test_null_outcomes.py`
(keep; not in the slow list); `python -m pytest tools/test_piles_close_id.py -q` (reads the debt file);
`python -B tools/factory_rules_index.py --check`
Items:
1. Move to "Fixed since this walk" (one bullet each, B-id kept inside the bullet): R5 (closed in code; critic F4), R7 (on
   the batch canon), R9 (after C1: "closed by code; proven by a live run (FR-33)" + live-runs row), X16, G4 (after C3-R
   item 1), W3 (S7), X9 (S8), X10 (S9), G15 (S10), each FR-59 G-row after its C3 card, R2/R3/R4/X2-residue after
   FL1/FL2/FL4/FL9. B-255 stays open after C3-R (provenance_acceptance still carries it).
2. **W1 is NARROWED, not closed** (critic F7): the row keeps "residue: the Level vocabulary is a code tuple
   (`contract.PLAN_LEVELS`; `contract.py:594` `TRACE_LEVELS` re-spells it)". Closing it whole needs a data row or a
   written Lead decision (fork F-L14).
3. K0.15 (`test_null_outcomes.py:596-597`): its positive control counts `|` lines holding `FR-23` `>= 2`; moving R5 (the
   FR-23-alone row) to a bullet leaves one. Re-point the control to a row that stays: the same filter shape must find the
   `| FR-21 |` row (`>= 1`), which the spec keeps. The main check (exactly one FR-23+FR-5 row with the four needles,
   :591-595) is unchanged. expected from: the spec S1 E1 and critic F4.
4. F-L12: FR-5 and FR-23 *Check* lines name `references/null-outcomes.json` and `scripts/tests/test_null_outcomes.py`
   (the spec's F-L12: it names an existing check's carrier, no meaning change).
5. Header counts recomputed from the tables after the edit; a table left empty keeps its heading with "Nothing open."
Edges: E1 — the FR-23+FR-5 row stays (it is open). INVARIANT: K0.15's single debt carrier stays. E2 — the `| FR-21 |`
line count stays exactly one (G1-10 of the quarantined `test_s1_s2_contract.py`: judged by reading). E3 — moved, never
deleted. E4 — FR-30 English. E5 TEMPORAL — a row whose node is not accepted when S1b runs stays open; S1b may run in two
sub-passes (after wave 2, after wave 3). E6 — axis 4: each moved FR-59 row's B-id is handed to the integrator for
`piles.py close --id` in the same move.
architecture content: `none -- <reason>` in the form `tools/architecture_gate.py` accepts (design doc rows, two Check
lines and one test control); judgment `none -- the debt file and Check lines name carriers, no check moves`.

## §3. Waves (rewritten t-994; updated t-1033)

**Wave 1 — launched (Lead, 17.11):** C1, C2, C4, FL9; C5 (Lead procedure, any time). FL9 stopped at its E1 with no diff
(t-962, `a18336d2`); C4's row was red on real code (t-961, «C4 result» below).

**Wave 2 — done / in flight (t-1033):** **C3-R** merged (`5751426c`, t-1009; plan-and-code critic t-1026: "needs work,
one fix round"); its fix round **t-1032** is merged (critic t-1039: `7f2f6f78`) (registry and tests only: A1 — `reporter_rehearsal_identity`
back to debt B-283 with `_reporter_outcome` accept and `_record_unreadable` produce —, A3, A4, A5). The second designer's
S9, FL2, FL4 (`docs/tasks/specs/20261117-rules-debt-phase2-s9-fl-cards-spec.md`) passed their plan critic in t-1026 with
edits (B6-B8, B11-B13) owned by that file. Before dispatch the Lead answers F-T6 (C3-R's words; still open in the forks).

**Wave 2½ — after t-1032 merges:** **C3-0** (builder) — first writer of `test_gate_registry.py` after t-1032 (S-f); no
other overlap except the registry (row-disjoint: one site line in `provenance_acceptance`) and `test-layers.json` (queue
line below). C3-b1 after S9 lands (window_record `WORD_READ_KINDS`); `wave-a/integrate` is merged (`71d36190`, the critic's
run), so S-e holds for every card based on today's main. C3-0 built at a4aca646 (branch `worktree-agent-aa11322709a274e56`), not on main at t-1043.

**Wave 3 — serial on hot files, after C3-0:**
- **C3-rr** (gate_preflight `_reporter_outcome`, registry row, its test rows) — first on the gate_preflight queue: **C3-rr →
  C3-j → C3-k → C3-h**.
- **C3-b2** (proof_level `already_probed` / `_product_receipt_repeat` / `_run_freshness` [/ `_evaluate`], execution_request
  `_match`) and **C3-g** (baseline_contract) after C3-0; C3-k after C3-0, C3-b2 and C3-g.
- window_record / acceptance: **S9 → C3-b1 → C3-d** (C3-d also after C3-0, F-T7 and F-T9; under rec (i) C3-d now moves
  code in `acceptance.validate_window`).
- controller.py: FL4 after S9 (second designer's file); FL2 after C3-R (its unknown-kind branch is pinned by C3-R item 3);
  S10 after the taken stage_guard/host_adapter rows are read; FL1 after TR4-17 and the taken manifest_put rows.
- **C3-reg-precondition** (controller `validate` dispatch branch, controller-blocks.md, state-exits.md, test_controller_state.py) after C3-0; on controller.py after S9 and FL4.
- `test_gate_registry.py` (every converting card, S-f): expected merge order **t-1032 → C3-0 → C3-rr → C3-b1 → C3-b2 →
  C3-g → C3-d → C3-j → C3-k → C3-h**; a card ready before its turn may merge first only by D-0048's rule (it merges main
  into its tree, re-derives its own row's pins and re-measures D13 on the merged tree; both sides' pins green).

**Wave 4:** S1b (two sub-passes allowed), then the BATCH CANON on CI (builder-rules 7b; coordinator).

**Collisions and order (t-989 K6, folded; t-1033 updated):**
- `references/gate-registry.json`: every C3 card; t-1032 edits rows `reporter_rehearsal_identity`, `environment_preparation`
  (A3, optional), `delivery` (A4 text); C3-0 adds one site line in another row; C3-rr edits `reporter_rehearsal_identity`
  after t-1032; S7 may edit `witness_backstop`. Row-disjoint, the later merge resolves (E-d).
- `scripts/tests/test_gate_registry.py` (t-1033, B1): owned by t-1032 (A1 pins), C3-0 (table, flip control, its D13 line)
  and every converting card (its own row's pins, S-f). Shared pins (the split counts, `D13_ITEM_COUNT`) are touched by
  every one of them: the expected order and D-0048 re-derivation of S-f; C3-g before C3-k on the F1 consumer block.
- `scripts/tests/fixtures/judgment-census.json`: `wave-a/integrate` is merged (`71d36190`, critic's run) — C3-j, C3-b1, S9 and
  any code-moving card start from today's main (S-e). C3-R, C3-0, C3-rr, C3-b2 and C3-d do not touch it (no unit moves).
- `s5_precheck.py`: `wave-a/integrate` changed it (not `run`); C3-R moves no code there, so no queue against FL9.
- `gate_preflight.py` (HOT): **C3-rr → C3-j → C3-k → C3-h**; C3-i left the queue (no code). C3-rr owns `_reporter_outcome`
  only.
- `window_record.py` / `acceptance.py`: S9 → C3-b1 → C3-d; C3-b1 and C3-d both edit `acceptance.validate_window` (C3-b1 a
  gap after the review checks, C3-d the review branch): serial. C3-d edits no `window_record.py` code (it only registers
  `build` and re-roles `verdict` in the registry). `controller.py` (HOT): S9 → FL4 → C3-reg-precondition (also `design/controller-blocks.md` header counts).
- `delivery-verdict-kinds.json`: FL2 only (C3-R moves no code).
- `proof_level.py`: C3-b1 (`_wanted`, new function) and C3-b2 (`already_probed`, `_product_receipt_repeat`,
  `_run_freshness`, and `_evaluate` on F-T10 (a)) — function-disjoint (D-0048 form); `execution_request.py`: C3-b2 → C3-k.
- `manifest_put.py`: C3-b1 (`CRITIC_FIELDS`) and FL1 (store path) — function-disjoint.
- `manifest_from_tests.py` (t-1033): C3-b1 only, `_attach_novelty` (F-T5 (a+)); no other card owns it.
- `scripts/tests/test-layers.json`: C3-0 adds one string to a `covers` list; `pile/live-run-fvf/batch-3` (dry story:
  `dry_*.py`, fixtures, `slow_tests.json`, `test-layers.json`, `selftest.py`, `scenario_walk.py`,
  `test_form_selftest.py`) also edits the file → `очередь: live-run-fvf/batch-3 → C3-0` for that one file, or the later
  merge resolves a one-line conflict (rec: the queue line). C3-R adds rows to existing keep files only: `test-layers.json`
  untouched. (Whether batch-3 has merged was not read in t-1033.)
- Taken batches (§4): the Lead decision (dev1's batches do not hold each other) stands; no new hit beyond §4's list.
- Afterwards: t-1032 → C3-0 → {C3-rr, C3-b2, C3-g, C3-d, C3-k}; C3-b1 after S9; C3-d after C3-b1.

**Plan critic needed:** C3-0, C3-b1, C3-b2 (one pass with C3-0: the same predicate, R13-g), C3-d (its two re-roles),
C3-g, C3-k, and the S9/FL2/FL4 file. Not needed: C3-R (judged in t-989; F-T6 is the Lead's answer), C2, C4, FL9, S1b.
(t-1033: t-1026 was that pass for C3-0, C3-b1, C3-b2, C3-d and the S9/FL file. The t-1033 redrafts of C3-b2 and C3-d and
the new C3-rr are fix-round text; whether they need a re-review is the Lead's call under PROJECT.md «new idea» step 6 —
"only if the fixes change the architecture": C3-d's three consumers (F-T9) and F-T11 are new shapes, rec: the Lead
reviews them himself unless F-T9 is answered other than (a).)

## §4. Taken pile batches (collisions)

Taken today (header status "в работе"): github-move/3; onboarding-forge/1, /2, /3, /4; onboarding-hooks/4, /5, /6, /7, /8
(10 batches; onboarding-forge/5 status not checked). A Grep of their files for this draft's owned file names (positive
control: the same call form found `check_witness` at onboarding-forge/2 :60) hits:
- onboarding-forge/2: `external_writes`, `common-rules` (:50-51), `judge_results`, `bug_records` (:65-66), plus
  `stage_guard`, `run_suite`, `execution_request`, `window_record`, `manifest_put`, `gate_preflight`, `controller`,
  `acceptance`, `s5_precheck` rows — touches C1, S10, C3-b1/b2/d/h/j/k, FL1, FL4, FL9.
- onboarding-forge/4: `common-rules`, `external-writes`, `test-report.md` (:45), `bug_records` (:57), `gate_preflight`
  (:42), `baseline_contract` (:44), `probe_by_code` (:36) — touches C1, C3-g, C3-j, C4.
- onboarding-forge/1: `gate_preflight` (:32, :74), `environment_record` (:40), `run_suite`/`launch-causes` (:48),
  `manifest_put`/`controller.py` (:50) — touches C3-j, S10, FL1, FL4, C3-b1 (manifest_put).
- onboarding-hooks/5: `gate_preflight` (:35, :38); /6: `stage_guard` (:16, :31); /7: `host_adapter` (:30); /8:
  `common-rules` (:36).
- C3-R touches only the registry and three test files, none named by these hits (the grep list above holds no
  `gate-registry`, `test_node_ids`, `test_third_verdict` or `test_gate_preflight` hit; not re-grepped in t-994).
- Unmerged branches the C3 cards meet (t-989 K6): `wave-a/integrate` (census, `s5_precheck.py`) and
  `pile/live-run-fvf/batch-3` (dry story, `test-layers.json`) — orders in §3.
NOT ESTABLISHED: whether those rows are open nodes owning the files or closed history (their status cells were not read).
Before launching C1 the Lead reads onboarding-forge/2 :50-51, :65-66 and onboarding-forge/4 :45, :57 (the status cell at
the row's end); before C4, onboarding-forge/4 :36; an open row -> an `очередь:` line in both batches (PROJECT.md «Командная
работа» п. 3) or a function-disjoint owns split. Same for the other cards' hits. (Lead decisions below: rows read, dev1's
batches do not hold each other.)

## §5. Pile rows to register (П1)

Into an UNTAKEN batch of the pile that holds the rules-debt topic (the Lead names it; each row with a findings file by
D-0044 — the findings are this draft's cards):
- `RD2-C1 | П1 | bug file homes: writer <-> readers (F-O6 (a), critic F8, external_writes bug_file) | builder | owns of C1 | D-1, D-3 | ожидает`
- `RD2-C2 | П1 | four command-door families as one table (F-O5 (b)) | builder | test_controller_doors.py | B-2 | ожидает`
- `RD2-C3-R | П1 | FR-59 registry conversions with no code: collected_ids, s5_coverage, delivery, case_preconditions, environment_preparation, reporter_rehearsal_identity, environment_property_cover (F-O1, t-989 F-K7) | builder | gate-registry.json (7 rows), test_node_ids.py, test_third_verdict.py, test_gate_preflight.py (1 row each) | F-T6 | ожидает`
- `RD2-C3-0 | П1 | the one predicate gate_template.acceptable for true accept sites (F-D1 (b)) | designer -> plan critic -> builder | gate_template.py, gate-registry.json (1 site), test_gate_registry.py, test-layers.json (covers) | F-T1, F-T2, F-T11; t-1032 → C3-0; очередь live-run-fvf/batch-3 → C3-0 | ожидает`
- `RD2-C3-rr | П1 | reporter_rehearsal_identity reuse through the predicate (t-1026 A1 (a), B-283) | builder (after t-1032 and C3-0) | gate_preflight._reporter_outcome, gate-registry.json (1 row), test_gate_preflight.py (table rows), test_gate_registry.py (pins) | C3-0 → C3-rr → C3-j | ожидает` (t-1033)
- `RD2-C3-b1 | П1 | live_check_demand: question to the code critic on a keyless, flagless row (F-O1) | designer -> plan critic -> builder | proof_level, acceptance, window_record, manifest_put, manifest_from_tests (_attach_novelty), qa-code-critic.md, gate-registry.json, tests, census | F-T4, F-T5, F-T8; S9 → C3-b1 | ожидает`
- `RD2-C3-b2 | П1 | test_identity through the predicate (F-O1) | builder (after C3-0) | gate-registry.json, proof_level (already_probed, _product_receipt_repeat, _run_freshness), execution_request._match, tests | F-T1, F-T10, F-T11; C3-0 → C3-b2 → C3-k | ожидает`
- `RD2-C3-<x> | П1 | FR-59 conversion: <gate> (F-O1) | designer -> plan critic -> builder | owns of the card | per card | ожидает` (one row each for d, g, h, j, k)
- `RD2-C4 | П1 | the no-probe-row road reaches acceptance (F-O2 condition) | builder | test_probe_by_code.py | B-1 | ожидает`
- `RD2-C5 | П1 | conductor prompt replace vs append: one experiment (F-O4) | Lead | experiments/conductor-system-prompt/ | F-E1 | ожидает`
- `RD2-S9 | П1 | person's word on a review gap (X10) | designer -> plan critic -> builder | window_record, controller | — | ожидает`
- `RD2-S10 | П1 | read heads as data + _is_reader rstrip fix (G15) | builder | launch-causes, host_adapter, stage_guard, role_replay | taken-batch rows | ожидает`
- `RD2-FL1 / FL2 / FL4 / FL9 | П1 | R2 / R3 / R4 / X2 residue | per card | per card | per card | ожидает`
- `RD2-S1b | П1 | debt file second pass + K0.15 control + FR-5/FR-23 Check lines | builder | three owns | all above | ожидает`
- live-runs rows (FR-33): R9/C1 (reporter + external write on the jira channel), C3-j (the card and the recorded
  answer), C3-b1 (critic asked at window acceptance), S9, and B-373 (F-O2's live proof, already owed).
- NOTE (t-1043): `plans/piles/rules-debt/` holds only `batch-1-phase-2.md` (Glob), and a grep there for `C3-rr|residue|holds_over|reg-precondition|RD1-7` finds only `RD1-7` (:18, :35, :45, the control). So C3-rr, the residue node and the findings have no carrier yet: the Lead/integrator opens one.
- `RD2-C3-reg-precondition | П1 | one stop when the gate registry cannot be read (F-T11 residue, R5 (b)) | builder (after C3-0) | controller.validate, controller-blocks.md, state-exits.md, test_controller_state.py | F-T12..F-T15; C3-0 → it; S9 → FL4 → it | ожидает`
- findings, one file each, `id: —`: `holds_over_comments` delete-or-wire (F-T10); probe_verdict accepted in unregistered functions, split needed (R12 a); `selector_contract:417` second reader of `same_command` (R12 b); the critic's review word read outside the registry and three door-text copies (R12 c).
- Batch row RD1-7 still describes C3-d by the (ii) direction (critic R11): the Lead updates it under TEAMWORK §2 (frozen batch).

## §6. Forks (returned, not decided)

Lead (technical):
- **F-D1 — conversion of accept sites** (§0.1). (a) build `gate_template.acceptable` (C3-0) and route every accept site
  of a converted row through it; (b) re-role a site to produce/validate where it honestly produces or validates
  (precedent `finish_exit_gate`, registry :596), and build the predicate only for sites that truly accept a record
  (test_identity, live_check_demand, provenance consumers, baseline_identity); (c) keep accept-site rows on `debt` with
  only the unknown branch declared. **Rec (b)**: smallest honest change, uses the registry's own second clause; the plan
  critic judges each re-role (E-c). Cost of (a) everywhere: a new shared mechanism plus edits at every accept site.
- **D-1 — the frame of `bug_file`** (§0.2). (i) keep the state-dir frame and have the reporter write
  `artifacts/<T>/bugs/BUG-n.md` in proposals (breaks if the artifact root lies outside the state dir, which
  `judge_results.py:274-275` says can happen); (ii) `bug_file` is task-root relative, `external_writes` resolves task
  root first then state dir. **Rec (ii)**: one frame for the field the reporter already writes, every older proposal still
  resolves (E5).
- **D-3 — does the duplicate check also read OTHER stories' task-root bugs?** (a) yes — keeps the meaning "every filed bug
  of the project" (before, every filed bug lived in one folder); (b) no — this story + the project home only (critic F8's
  minimum). **Rec (a)**; cost: more pairs, bounded by `MAX_BUG_PAIRS` (E3).
- **D-2 — `stages.json`/`artifact-writers.json` `project:bugs/`** (§0.2): (a) leave (the guard matches `/bugs/` in any
  path; the witness may look at the old home); (b) a follow-up node moving the S8 output and the reporter's witness to the
  task-root `bugs/` with every reader of the key, after a scout question "what does each reader of `project:bugs/` do with
  a task-root bug?". **Rec (b)** as a separate node after C1 (one road, P31); outside C1 because the reader set is wide
  and not read today.
- **B-1 — where the F-O2 "scenario row" lives.** (a) a row in `test_probe_by_code.py` (keep, `test-layers.json:3676`);
  (b) a `variants.json` row of a recorded story — but the walker has no door that runs a probe (`DOORS = ("exit_gate",
  "joint", "start", "gate", "delivery")`, `scenario_walk.py:40`), so (b) needs a new walker door (a mechanism). **Rec
  (a)**; the owner's word said "scenario row" — the Lead confirms the reading (or takes it to the owner).
- **B-2 — C2's world.** (a) the recorded story `cart-1` where the block is reachable, the `BASE` synthetic otherwise,
  named per row; (b) `BASE` everywhere (the existing precedent). **Rec (a)** — closer to the owner's "real story" intent.
- **F-C1 — where C3-j asks.** (a) on the gate A card where `check_s5_stand_limits` already runs (`gate_preflight.py:6084-6093`)
  and where `over` already cards — gate A is the gate before S5, so nothing runs on a guess; `waits_at: gate_a`; (b) a new
  S5-entry question (the owner's literal "stage entry"), a second place for the same fact (P31 risk). **Rec (a)**; the
  Lead says whether the owner must confirm that gate A satisfies "stage entry".
- **F-C2 — which registry holds the answer.** (a) the environment record (`environment_record.py`, "accept always",
  keyed, FR-7's existing road for stand-gap cards); (b) the project answer registry (`project_knowledge.py`). **Rec
  (a)**: the existing card -> record -> cover road (P31: one road for "do not ask this stand again"); (b) fits only if the
  person is asked for a NUMBER, which the owner did not say.
- **F-E1 — C5 sample size.** (a) one question each way; (b) 2-3 questions of different classes each way, still one
  experiment. **Rec (b)**: one call cannot judge "copes" (the owner's added measure).
- **F-L14 — W1 whole** (critic F7): a written Lead decision that one code owner satisfies FR-13 for the Level set, or a
  data row (a node). **Rec**: a node later (FR-13's letter); S1b narrows now.

Owner: none new — F-C1 and B-1 may need her confirmation (Lead's call).

## §7. Small technical choices closed

- C3 grouped by shared functions (forced by the registry's "registered more than once" finding), not one node per gate.
- C2 drops the stale numbers from its docstring rather than updating them.
- C1 adds `"file"` to duplicate entries instead of changing `"bug"` (additive; FR-14).
- S1b re-points K0.15's positive control to the FR-21 row (same filter shape) instead of deleting it.
- DoDs never run slow or quarantined files (builder-rules.md:53-55); they name them "judged by the batch canon".
- Axis number 38 for the new SIBLING_MAP axis (the next free number).
- t-994: `collected_ids` words = `["node_id_mismatch"]` alone — the critic's own fallback (F-a2) applies, because the code
  writes no `not_verified` token (`run_suite.py:1673-1674`, the prose note only).
- t-994: `environment_preparation` keeps `addressee` / `person_subject` / `accepts` unchanged (the decision changes the
  branch, not who supplies the facts); `verdict_map` maps both `blocked` and `unknown` to class unknown, owner
  environment (both are "a fact could not be established", not a mismatch).
- t-994: `live_check_demand` unknown owner becomes `role` (the critic answers it); `factory` would claim our own defect
  (FR-3) for a judgment.
- t-994: C3-0 registers `gate_template.py:acceptable` as a `library` site in `provenance_acceptance` (the row that already
  hosts the A26 library sites) rather than a new row (a new row would need its own branch and test for a library).
- t-994: C3-0's test rows go into the existing keep file `test_gate_registry.py` (no new test file, builder-rules 7d) and
  its `covers` gains `gate_template.py`.
- t-994: C3-b1's gap sits after the review checks and before `sensitivity:` (it never shadows either).
- t-1033: the A1 conversion is a NEW small card C3-rr, not an item of C3-0 (C3-0 wires no consumer, its non-goals) nor of
  C3-k (designer-first, many files): C3-rr's owns are one function, one row, one test table and its pins.
- t-1033: C3-rr reads `earlier.get("state")`, not the brief's `earlier["state"]`: an absent state is "not acceptable"
  (rehearse), never a `KeyError`; the hit checks stay before the predicate (E3).
- t-1033: the binding rule on `test_gate_registry.py` is D-0048's (the later merger re-derives its own row's pins and
  re-measures D13 on the merged tree); the order list in S-f is the expected order from the dependencies, not a lock.
- t-1033: `_run_freshness` takes the predicate (true accept), not a named residue: at :939 the predicate accepts exactly
  the words the literal accepts (E-c table, t-1033 row), so the conversion is behaviour-preserving and keeps one road.
- t-1033: C3-d's `words` are only the words its sites compare (`approved`, `unverified`), per S-c; `approved_with_fixes`
  and `rejected` are refused by being outside `words`.
- t-1033: `HANDED_REVIEW_VERDICTS` is deleted after C3-d (no reader left); `BLOCKED_REVIEW_VERDICT` stays (its only other
  readers are `window_record`'s note texts).
- t-1033: `window_record.build` is registered `produce` under `s5_window` (A1's class: the row's word compared in an
  unregistered function, here for a note).
- t-1033: A2's direction — remove `provenance.environment_preparation` in C3-k and add the consumer `_run_step` calls only
  in the commit that wires `_run_step`, under a promotable-false row (F1's guard kept, AR-22).
- t-1033: the F-T5 (a+) marker counts only as a non-empty string; every other value reads "not marked" (E10).
- t-1033: cards edited in this round carry absolute `owns:` / `given:` paths; the untouched cards keep repo-relative ones.

## §8. Readers of every touched file (rule 7)

Command (pre-t-994): Grep over `tools/*.py` for the touched names (`judge_results|bug_records|external_writes|common-rules|external-writes|test-report|form_selftest|test_controller_doors|gate-registry|environment_record|launch-causes|host_adapter|stage_guard|factory-rules-debt|delivery-verdict-kinds|manifest_put`)
-> hits in 6 files (listed below); the same names over `.githooks/` -> 0 (positive control: `architecture_gate` found in
`.githooks/commit-msg`, 1 hit); over `.claude/` settings/hooks/agents -> 0 (positive control in that shape not run: not
established).

t-994 command: Grep (count) over `tools/` for
`gate_template|gate-registry|proof_level|window_record|manifest_put|test-layers|judgment-census|baseline_contract|execution_request`
-> 84 hits in 18 files: `architecture_gate.py` 1, `controller-blocks-gen.py` 10, `fixtures/dispatch_manifest/K8.txt` 2,
`lint-baseline.json` 3, `lint_ratchet.py` 3, `owns_readers.py` 6, `owns_readers.json` 1, `source-split-carriers.json` 5,
`source_split.py` 12, `test_lint_ratchet.py` 4, `test_owns_readers.py` 4, `test_test_redundancy.py` 1, `test_split.py` 3,
`test_test_quarantine.py` 2, `test_quarantine.py` 11, `test_redundancy.py` 4, `test_warn_density.py` 4,
`warn_density.py` 8. The same pattern plus `architecture_gate` (the positive control) over `.githooks/` -> 2 hits, both in
`commit-msg`. NOT split per name (one combined count; the split is owed before C3-0/C3-b1 dispatch — one Grep per name,
`output_mode: content`); `.claude/` not grepped in t-994.

t-1033 command (the names this round adds to owns): Grep (count) over `tools/` for
`test_gate_registry|manifest_from_tests|gate_template|acceptance\.py|gate_preflight` -> 7 hits in 4 files:
`dup-baseline.json` 1 (:92, `manifest_from_tests.py` `build` in a clone group), `fixtures/dispatch_manifest/K8.txt` 1,
`source-split-carriers.json` 2 (:15 the registry carrier verified by `test_gate_registry.py`; :25 `test_gate_registry.py`
as a `py-triple` carrier: "set literal of ('<file>', '<function>', '<gate>') rows (check D13): only the file changes"),
`source_split.py` 3 (:2812-2826, selftest strings of a `test_gate_registry.py` SITES literal). Over `.githooks/` with the
control `architecture_gate`: 1 hit (`commit-msg:37`, the control) -> 0 for the names. Over `.claude/settings.json` with the
control `hygiene_gate`: 1 hit (:38, the control) -> 0. Over `.claude/agents/` with the control `designer`: 3 hits, all
`designer.md` (the control) -> 0. (A grep over the whole `.claude/` tree ran into `.claude/worktrees/` copies and stopped
at its time limit: not used.)

Commands (t-1043):
- Grep (count) over `tools/` for `state-exits|controller-blocks\.md|gate_template`: 3 hits — `controller-blocks-gen.py:1`, `test_controller_blocks_gen.py:1`, `test_test_quarantine.py:863` (a fixture string `design/state-exits.md:34`).
- `controller\.py` over `tools/`: 12 hits in 5 files (`controller-blocks-gen.py` 4, `test_forge_metrics.py` 5, `test_collect_intake.py` 1, `test_controller_blocks_gen.py` 1, `test_dispatch_gate.py` 1).
- Over `.githooks/` with the control `architecture_gate`: 1 hit (the control), so 0 for the names.
- Over `.claude/settings.json` with the control `hygiene_gate`: 1 (the control), so 0.
- Over `.claude/agents/` with the control `designer`: 3, all `designer.md`, so 0.
- `SIBLING_MAP` over `tools/`: 44 hits in 25 files (mechanism_gate.py 7); over `.githooks/`: 0. No positive control was run in that dir for this exact pattern; the earlier combined grep there found `architecture_gate`.

| touched | reader | verdict |
|---|---|---|
| bug_records.py (C1) | `tools/source_split.py:2810-2821,3028-3033` | unchanged — a new function is additive; if source_split lists functions, a report line |
| gate-registry.json (C3-R, C3-0, C3-rr, C3-b1, C3-b2, C3-d, C3-g, C3-j, C3-k) | `tools/source_split.py:2753-2891`, `tools/test_quarantine.py:2199`, `tools/source-split-carriers.json:15`; package: `gate_registry.py` (A26), `test_gate_registry.py`, `test_branch_accounting.py` (greps the name); at run time after C3-0's consumers: `gate_template.py` (new) | unchanged by row edits (file name unchanged); builder confirms they read the path, not row ids; `test_gate_registry.py` pins: S-f |
| gate_template.py (C3-0, new) | `gate_registry.py` finding texts (:840, :878) name it; consumers after wiring: `gate_preflight.py` (C3-rr), `proof_level.py` / `execution_request.py` (C3-b2), `acceptance.py` (C3-d), `baseline_contract.py` (C3-g), provenance sites (C3-k); tools: 0 hits (t-1033 grep) | unchanged (texts already name it); each consumer changes in its own card |
| test_gate_registry.py (t-1032, C3-0 and every converting card, S-f) | `tools/source-split-carriers.json:15,25` (D13 py-triple carrier), `tools/source_split.py:2812-2826` (selftest strings only); `test-layers.json:2032` keep row | unchanged — every S-f edit keeps the `(file, function, row)` tuple form the carrier reads; the shared pins change in every converting stream (S-f order, D-0048) |
| test-layers.json (C3-0 covers line) | `scripts/selftest.py` (`test_layers()`), `scenario_walk.py --witness-for` (:913-916), `tools/test_quarantine.py` (writes quarantine/cohorts) | unchanged — a `covers` string is read by witness-for only; `test_quarantine.py` does not write `covers` (file note :3); changes in stream `live-run-fvf/batch-3` (queue line, §3) |
| judgment-census.json (C3-b1, C3-j: own rows only if a unit appears) | `tools/architecture_gate.py` (the `ratchet` object, census header :3), `test_judgment_census.py` | unchanged unless a counted class grows (then AR-20: named in the verdict); `wave-a/integrate` merged (S-e) |
| proof_level.py (C3-b1, C3-b2) | tools: in the combined count (not split); package readers of `proof_required` / `not_required_why`: `ledger.py:1081,1610`, `case_stamp.py:557`, `probe_debt.py:303-304`, `report_facts.py:1534,1644`, `acceptance.py:1153,1207`, `window_record.py:1782`; of `run_freshness`: `acceptance.run_freshness_of` (`acceptance.py:1148`), `window_record._run_freshness_unknown` (:1798) | unchanged for every row that carries `novelty` or a flag; a keyless row with `probe_owed: "yes"` becomes required (adds only) — readers show it as required, which is the intent; `run_freshness` answers the same words (C3-b2 E7), and on an unreadable registry `stale` with the registry why (F-T11) |
| acceptance.py (C3-b1; C3-d) | `tools/controller-blocks-gen.py` (block routes, if a gap route changes); tools: 0 hits for `acceptance\.py` (t-1033 grep); package callers of `validate_window`: `driver_dispatch.py:1011`, `coverage_contract.py:258`, `controller.py:7445`, `story_step.py:1629`, `window_record.py:1849` | C3-b1: changes only if a new gap route enters `controller-blocks.md` (builder runs the generator's check); C3-d: unchanged for every caller (the same gaps for the same words, E1); `HANDED_REVIEW_VERDICTS` has no reader outside `acceptance.py` (grep) |
| window_record.py (C3-b1; C3-d registry only) | `tools/controller-blocks-gen.py` | changes in C3-b1 only if a new gap route enters `controller-blocks.md`; C3-d moves no code |
| manifest_put.py (C3-b1, FL1) | `tools/controller-blocks-gen.py:138,190-193` | changes in C3-b1/FL1 only if a block route text changes |
| manifest_from_tests.py (C3-b1 on F-T5 (a+), t-1033) | `tools/dup-baseline.json:92` (clone group of `build`) | unchanged — C3-b1 edits `_attach_novelty`, not `build`; the clone ratchet re-reads it in CI |
| gate_preflight.py (C3-rr, C3-j, C3-k, C3-h) | tools: 0 hits for `gate_preflight` (t-1033 grep) | unchanged |
| baseline_contract.py, execution_request.py (C3-g, C3-b2) | tools: combined count (not split) | owed split before wave 3 |
| stage_guard.py / host_adapter.py (S10) | `tools/controller-blocks-gen.py:342`, `tools/test_collect_intake.py:543` | unchanged (they use names S10 does not change) |
| factory-rules-debt.md (S1b) | `tools/piles.py:2381`, `tools/test_piles_close_id.py:87-89` | unchanged — rows move, the file and its bullet form stay |
| factory-rules.md (S1b) | `tools/factory_rules_index.py` | unchanged — a Check line is not a title |
| controller.py (S9, FL4) | `tools/controller-blocks-gen.py` | changes in S9/FL4 if a block route changes |
| judge_results, external_writes, common-rules, external-writes.md, test-report.md, form_selftest, test_controller_doors, environment_record, launch-causes, delivery-verdict-kinds | no hit in tools/ or .githooks/ (pre-t-994 grep) | — |
| controller.py (C3-reg-precondition) | `tools/controller-blocks-gen.py` (reads raises); `test_forge_metrics.py`, `test_collect_intake.py`, `test_dispatch_gate.py` (name strings) | the generator must place the new `person`-route block (or the row is hand-written, `controller-blocks.md:25-29`); the others unchanged |
| design/controller-blocks.md | `tools/controller-blocks-gen.py`, `tools/test_controller_blocks_gen.py`, package `test_controller_blocks.py` | one row in source order; header counts also move in S9/FL4 if they add blocks (D-0048) |
| design/state-exits.md | package `test_state_exits.py`; `tools/test_test_quarantine.py:863` (fixture string only) | unchanged by an added row |
| test_controller_state.py | `test-layers.json:1082` keep row | unchanged |
| test_run_freshness.py (C3-b2, one row) | `test-layers.json:4702` keep row; imported by test_proof_level.py (its `why`) | unchanged |
| docs/SIBLING_MAP.md (Lead's line) | `tools/mechanism_gate.py` and 24 more tools files | a mechanism path: the Lead commits it with the axis block |

`tools/owns_readers.py` / `owns_readers.json` (6 + 1 hits of the combined pattern) is a tool that maps owned paths to
their readers: the Lead runs it on each card's owns before dispatch (its CLI not read in t-994).

Package readers (outside rule 7's scope, load-bearing): `external_writes.py` reads `bug_file` (C1 item 4);
`stages.json`/`exit_gate` read `project:bugs/` (D-2); `contract_slices.py --check` reads `common-rules.md` (C1 item 3).

## §9. Reading trail

Read whole: the spec; `reviews/t-942-rules-debt-phase1.md`; `references/gate-registry.json`; `test_controller_doors.py`.
Read parts: `judge_results.py` (:16, :265-362); `bug_records.py` (:1-60, :128-170, :1502); `external_writes.py` (:46,
:117, :640-660, :858-910); `exit_gate.py:750-779`; `guard_pre_tool.py:1040-1061`; `common-rules.md:108-121`;
`external-writes.md:38-51`; `templates/test-report.md:28-39`; `form_selftest.py:225-259`; `agents/qa-bug-reporter.md:50-61`;
`controller-blocks.md:1-40` (+ Grep counts); `gate_registry.py` (:1-110, :225-240, :760-884); `environment_record.py`
(:1-199, :290-340); `project_knowledge.py:1-80`; `gate_preflight.py` (:3080-3330, :4195-4255, :6070-6099);
`stand_gaps.py:1225-1264`; `driver_runner.py:575-634`; `conductor_families.py:1-25`; `scenario_walk.py:40`;
`stage_guard.py:2500-2594`; `host_adapter.py:440-549`; `role_replay.py:30-36`; `window_record.py:1735-1770, 1885-1895`;
`controller.py` (:7420-7450, :9391, :9908); `s5_precheck.py:1650-1665`; `delivery-verdict-kinds.json`;
`test_null_outcomes.py:584-599`; `TESTING.md`; `builder-rules.md`; `slow_tests.json`; `test-layers.json` (Grep);
`SIBLING_MAP.md` headings; debt file headings; taken batch files (Grep).
Greps with positive controls of the same shape: `def acceptable` (control: `acceptable_provenance` hit); `gate_template.py`
Glob (control: same Glob form on scripts); `variants*.json` Glob (control: `story.json` found by the same form); taken
batch names (control: `check_witness`); `.githooks` names (control: `architecture_gate`).

t-994 (on a6df7fd1, root checkout = origin/main by the two refs files): the verdict
`reviews/t-989-rules-debt-phase2-wave2-plan.md` (whole); `gate_registry.py` (:1-80, :110-146, :205-264, :405-483,
:485-681, :684-785, :786-975); `gate-registry.json` (:1-280, :280-296, :296-570, :595-614); `proof_level.py` (:320-504,
:815-914, :1404-1538, def list); `execution_request.py` (:2065-2237, def lines); `profile_contract.py:850-959`;
`baseline_contract.py` (whole, 222 lines); `acceptance.py` (def list, :1140-1230); `window_record.py` (:633-667 by grep,
:1470-1510, :1778-1847); `probe_debt.py` (:1-60, :270-330); `ledger.py:1060-1083`; `s5_precheck.py` (:4598-4612,
:4726-4740, greps `unchecked`); `run_suite.py` (greps `node_id_mismatch|not_verified|not verified`);
`environment_preparation.py` (greps `blocked|unknown`); `onboarding_probe.py` (greps of the rehearsal words);
`environment_record.py` (def heads :133, :165, :188, :275, :300); `gate_preflight.py` (greps of the cover/rehearsal words);
`manifest_put.py` (greps `sensitivity_proof_required|critic_verdict`); `scenario_walk.py:833-922`; `selftest.py:736-756`;
`test-layers.json` (:1-30, :2020-2059, greps of the keep/quarantine rows); `slow_tests.json` (grep);
`judgment-census.json` (:1-40, greps); `design/architecture.md` (:146-183, :276-283, change-check grep);
`factory-rules.md` FR-59 (:289-301); `plans/builder-rules.md:40-109`; fixture greps:
`fixtures/stories/*/work/automation-manifest.json` (`"novelty"` 0 and 0; control `change_disposition` 24 and 45),
`fixtures/stories/cart-1/work/windows` (`expectation_changes_unmeasured` 4 files), Glob of recorded windows (6, all
cart-1). Negative claims with controls: `provenance\.baseline` in `scripts/*.py` only in tests (control `"captured"`
found in `baseline_contract.py`); `"novelty"` in the two manifests 0 (control above); `"(matched|mismatched|unchecked)"`
literals in `s5_precheck.py` only the `unchecked` key (the hits are the control); `"(covered|changed_since|not_covered|
unreadable|near_miss)"` literals in `environment_record.py` 0 — NO same-file positive control was run (treat as "not
found"; the def heads read at :188-191, :300-305 support it); rehearsal words in `gate_preflight.py` / `onboarding_probe.py`
(the hits themselves). Not available: a shell — no `gate_registry.py --check`, no `--sites`, no novelty probe run here.

## Not done / not established

- The status cells of the taken-batch rows in §4 (whether they own the files now) — not read; lines given.
- Whether a jira-channel proposal already fails "bug_file not found" on a live story (D-1) — by reading only.
- The window reader that counts a `red_sandbox.py --probe` receipt (C4) — the builder names it.
- The capability key in `detectors.json` for FL9 — not established (the spec says the same).
- FL1's function in `manifest_put.py` — not named; a designer pass is owed.
- The `gate-decision` row for C2 — chosen by rule, not named here.
- C3-k (provenance) is not drafted to builder level (designer first).
- The `.claude/` positive control for §8 was not run in the same shape; the "system-prompt" grep over `experiments/` had
  no same-form positive control.
- Spec line references were taken from the pre-compaction read of the spec; the Lead spot-checks one at acceptance.
- t-994: no command was run (no shell): `gate_registry.py --check` / `--sites`, the novelty probe and the C3-d INFO-line
  count rest on the critic's runs or on reading; §8's tools grep is one combined count, not split per name; whether
  `manifest_put` accepts `sensitivity_proof_required` or an unknown key on a `tests[]` row from the critic's fragment was not
  read (C3-b1 uses a new `CRITIC_FIELDS` member instead); C3-b1's exact place where the window records the owed state (item
  3) is the builder's reading of `window_record`'s item build, bounded by E4.
- Resolved in t-994 (were open above): the empty-`words` question (F-S1: refused, `gate_registry.py:524-526`); the
  `--check` debt block (`gate_registry.py:968-971`); keep/quarantine status of C3-f/C3-g tests (keep, fast).

## Lead decisions on the forks (17.11.2026, draft accepted t-954)

- F-D1 -> (b) re-role a site where it honestly produces or validates; the predicate only for true accept sites; the plan
  critic judges each re-role.
- D-1 -> (ii) `bug_file` is task-root relative; `external_writes` resolves task root first, then the state dir.
- D-3 -> (a) the duplicate check reads other stories' task-root bugs, bounded by `MAX_BUG_PAIRS`.
- D-2 -> (b) a separate node after C1, scout question first.
- B-1 -> (a) the row lives in `test_probe_by_code.py`; "scenario row" in the owner's word is read as "a row of the test
  that walks the road", not a new walker door (told to the owner).
- B-2 -> (a) the recorded story where the block is reachable, `BASE` otherwise, named per row.
- F-C1 -> (a) the question sits on the gate A card, before S5 runs: this IS the owner's "at stage entry" (nothing in S5
  runs on a guess; a second place would break P31) (told to the owner).
- F-C2 -> (a) the environment record — the owner's word "записать в реестр энвайроментов".
- F-E1 -> (b) 2-3 questions of different classes each way, one experiment.
- F-L14 -> a node later; S1b narrows now.
- C1 and PROJECT.md «package change» item 6: the old frame still resolves (E5), so the topic code critic is enough; no
  separate plan critic for C1.
- Taken batches (§4): onboarding-forge/1-4 and onboarding-hooks/4-8 are taken by dev1; batches of one developer do not
  hold each other (owner, 13.11.2026). Rows read: OH3-25, OF4-6, OF4-27, RC1-10 accepted; RC1-15, TQ1-29, OF4-15 waiting
  (П3, no worker in flight). Wave 1 launches.
- Wave 1 now: C1, C2, C4, FL9. Pile rows of §5 are registered as one small-work batch at the stage boundary.

## C4 result (t-961, 17.11.2026): the condition of F-O2 does not hold today

The builder wrote the row and it was RED on real code (edge E1), so no row is committed; the report is
`docs/tasks/handoffs/t-961-rules-debt-c4.md` on branch `worktree-agent-a72a37ff6d6ddc10a` (commit dd27d27e).
Measured: for a suffix with no probe row (`.kt`), a non-pytest command and a junit-xml reporter,
`red_sandbox.py --probe` answers `incomplete` ("assertion site of a junit-xml/python report is not read yet (B-337)")
and publishes no receipt, so `proof_level.reached` has nothing to count; a pytest-named command cannot select a non-.py
test (`node_ids` keeps .py ids only). Cause by the builder's reading (not re-verified by the Lead):
`red_sandbox._frame_grammar` returns {} for a suffix with no row and `reporters.assertion_site` then gives `site_unread`.
Also: the card said `probe_by_code` "writes a record" for a no-row suffix — it refuses (exit 2), pinned by
`non_python_test_refused`; the card's sentence was wrong.
Consequence: F-O2 (a) "no probe rows for other languages now" was taken on the condition that the role's probe road
reaches acceptance. It does not. A fix node (designer first: where the site of a junit-xml report is read, B-337) is owed;
the red row lands with that fix (red-before). The owner is told.

Владелец, 17.11.2026, о починке B-337 (расписка «проверка живая» для не-Python тестов, результат C4): «Отдельный П1 на
потом». Сегодня не берётся; узел П1 заводится в невзятой пачке вместе со строками §5 (один малый пакет билдеру),
красная строка C4 входит вместе с починкой.

## Forks returned (t-994)

Each is the Lead's (technical) unless marked; none is decided here. The cards execute on the recommendation only where
the card says so.

- **F-T1 — test_identity's two `execution_request` sites consume no word of the row** (C3-0, C3-b2). Fact:
  `_match` decides byte identity through `same_instance_bytes` -> `compare_identity(...)[0] == "same"`
  (`execution_request.py:2065-2075, 2099-2101`), vocabulary `same/different/unknown`, not `raw/instance/instance_code/
  file_code`; `green_over_same_bytes` reads identity only through `covered` -> `_match` (:2182-2183). Options: (a) the row's
  words gain `same`/`different`/`unknown` (verdict_map matched/mismatched/unknown, owner environment); `_match` calls
  `acceptable(compare_identity(a, b)[0], "test_identity.run_reuse")`; `green_over_same_bytes` is re-roled `validate` (its
  only identity read is `_match`'s answer — a second `acceptable()` call over the same answer would be a second road, P31);
  (b) as decided (three accept sites): `green_over_same_bytes` also calls `acceptable` (on what word? it has none of its
  own — it would have to recompute identity per instance); (c) `_match` and `green_over_same_bytes` both re-roled
  (`validate`) and only `already_probed` converts — contradicts the critic's "true accept". **Rec (a)**: honest to the code,
  one call per decision; cost: one re-role the critic did not judge (C3-b2's plan critic judges it).
- **F-T2 — where the predicate lives and how it relates to `acceptable_provenance`** (C3-0, C3-k). (a) new
  `scripts/gate_template.py` (the name the A26 texts already print, `gate_registry.py:840,878`), generic over word and
  record; `profile_contract.acceptable_provenance` stays the provenance record validator and C3-k decides whether
  `acceptable` delegates to it for `provenance.*` consumers (one survivor, AR-15, named on an axis then); (b) put
  `acceptable` inside `gate_registry.py` (no new file, no covers line, but every consumer then imports the audit module);
  (c) extend `acceptable_provenance` into the general predicate (renames a working provenance road; the name stays wrong
  for test_identity). **Rec (a)**.
- **F-T3 — baseline_identity's "true accept" is not a provenance acceptance** (C3-0, C3-g). Fact: `deployment_readiness`
  accepts baseline receipts by `status == "captured"` plus revision, gate-ref and hash equalities
  (`baseline_contract.py:185-214`), reports gaps with `blocks_execution: False` and `ready: True` always (:216-221); the
  consumer `provenance.baseline` (registry :352) is read by no script. Options: (a) C3-g converts on the receipt's own
  vocabulary: `field: "status"`, words `captured`/`inconclusive` (written at :134), a consumer
  `baseline_identity.readiness: ["matched"]`, and `deployment_readiness` calls `acceptable(receipt,
  "baseline_identity.readiness")` in place of the literal at :199; the unused `provenance.baseline` is removed or moved to
  the reader that really reads a baseline provenance (`manual_evidence.validate_baseline_record`, a provenance accept site,
  registry :47 — C3-k); (b) re-role `deployment_readiness` `measure` (it never blocks; the refusal is elsewhere) and
  convert with no predicate; (c) as decided, against `provenance.baseline` (fits no code). **Rec (a)** (keeps the Lead's
  "one true accept site" and fits the code); C3-g's designer confirms.
- **F-T4 — the carrier of the code critic's answer** (C3-b1, F-b2). (a) one closed field `probe_owed: yes | no` on the
  `tests[]` row, written through the critic's existing road (`manifest_put.CRITIC_FIELDS`, :1085) with `critic_note` for
  "no"; `yes` adds the requirement in `_wanted`, `no` closes the question; (b) the critic's recommendation in t-989: "owed"
  = set `sensitivity_proof_required: true` through the fragment (no new reader), "not owed" = a typed answer the window
  reads (still a new field; and whether `manifest_put` lets the critic write the flag was not read); (c) a window-only
  answer (an item field), not on the row (the next window asks again: FR-7 risk). **Rec (a)**: one field for both answers,
  one writer, readers in the same commit (AR-22).
- **F-T5 — the observable that keeps in-flight stories un-asked** (C3-b1, F-b4, builder-rules 9; the consequence
  corrected in t-1033 under t-1026 B5, before anyone answers). Options: (a) the question applies only when the manifest
  holds at least one `tests[]` row with a `novelty` key (the writer of this version ran); on the recorded stories that is
  never (0 novelty keys); (a+) (a), plus the writer marks a manifest whose measurement failed: `_attach_novelty` writes a
  top-level `novelty_unmeasured` (its failure note) on a failed call and `""` on a successful one, and the question also
  applies when that marker is a non-empty string (a new field; both worlds in C3-b1 E3/E10, item 8); (b) every window
  built after the change asks (in-flight stories are held at their next window — against builder-rules 9); (c) the owner
  accepts that in-flight stories are asked. **Consequence of (a), from the writer's facts** (`manifest_from_tests.py`):
  the question FIRES on (1) a row added by hand into a measured manifest, and (2) a row the writer itself left keyless by
  policy V2 — against a base that is not a recorded S0 base, a value outside `NOVELTY_KEPT_WITHOUT_S0` (`new`, `changed`)
  gets no key (`_novelty_block` returns None, :835-840; V2 note :826-831) — whenever another row of the same manifest
  measured `new` or `changed`; such a manifest is typically a story in flight against a non-S0 base, so (a) DOES ask in
  some in-flight stories (a wait at window acceptance; the answer can only add a requirement) — the one place (a) meets
  builder-rules 9. The question NEVER fires on (3) a manifest written before the novelty writer, and (4) a manifest whose
  whole measuring call failed: the `except` at :923-926 notes "novelty could not be measured", copies back only blocks the
  manifest already held (`_keep_stored_novelty`, :855-887) and leaves every other row keyless — with no stored block
  anywhere it reads exactly like a legacy manifest, so the case where nobody measured anything is the one that escapes.
  (a+) closes (4) for manifests this writer writes from now on; (2) stays under (a) and (a+), and (b)/(c) widen it to
  every in-flight row. **Rec (a+)** (critic t-1026 B5): in-flight safety of (a) plus the whole-failure case; cost: one
  marker field with one writer and one reader in C3-b1's commit. If the Lead declines (a+), the owner is told in plain
  words: «если замер новизны тестов целиком не удался, фабрика не спросит критика, нужна ли живая проба этим тестам». In
  either case the owner is told case (2): «в историях, начатых до замера, критика иногда спросят про тесты, которые замер
  счёл неизменными». If the owner meant every legacy row, it is (c) and the Lead takes it to her.
- **F-T6 — three C3-R rows' as-written words are not all written by the code** (C3-R items 2, 6, 7; Lead decision 1 applied
  them as written). Facts: `s5_precheck.run` writes no `"matched"`/`"mismatched"` literal; `unchecked` is a result KEY
  (:4366, :4737); `reporter_rehearsal_identity`: `onboarding_probe.earlier_proof` returns the states `none`,
  `unreadable`, `same_command`, `command_changed` (`onboarding_probe.py:381-394`), `reused` is a dict key
  (`gate_preflight.py:3623, 3846`) and `rehearsed` was found in neither file; `environment_property_cover`:
  `environment_record.covering` returns a row or `None` (:300-305), `near_miss` returns a why in `command`/`reason`/
  `address` (:188-191), `changed_since` is a key the card writes (`gate_preflight.py:4241`), and `covered`/`not_covered`
  were not found. Options: (a) keep as written (the rows pass `_check_row`, which does not read the code, but say `code`
  for words the code does not write — the claim `vocabulary` exists to keep honest, `gate_registry.py:129-131,516-519`);
  (b) only tokens the code writes: s5_coverage `["unchecked"]`; reporter_rehearsal_identity `["same_command",
  "command_changed", "none", "unreadable"]` (same_command -> matched, the rest -> unknown, owner environment);
  environment_property_cover `["command", "reason", "address"]` (the near-miss whys, mismatched) — matched and unknown
  carry no word because the code writes none (the test_identity precedent: words of one class); (c) leave those three rows
  `debt` until a word exists. **Rec (b)**; cost: none in code, three row texts. (t-1033 note: the merged registry on
  2151eeef already carries (b)'s words for all three rows, :215-217, :507-513, :530-535.)
- **F-T7 — C3-d: correct the row, or make unmeasured detectors gaps** (C3-d, F-d1; a MEANING change, AR-28). (i) the
  row's `decides` is corrected to the code (INFO line, owner role) and converted as is; (ii) the listed unmeasured
  detectors become gaps closed by the critic. Premise measured above: 4 of 6 recorded cart-1 windows carry
  `expectation_changes_unmeasured`; under (ii) all four, including the last, would have held. **Rec (i)** unless the Lead
  or the owner wants the stricter window; (ii) is an owner question (it changes what holds a story).
- **F-T8 — the person's door on C3-b1's gap** (C3-b1, FR-4/P13, axis 34). (a) the gap kind joins the window's word road
  (`WORD_READ_KINDS`, `window_record.py:1741`) as S9 makes it carry a `review` gap — C3-b1 queues after S9; (b) C3-b1 builds
  its own person door now (a third road — P31 defect). **Rec (a)**.

## Fix round t-994 — where each t-989 finding went

| finding | where applied / status |
|---|---|
| F-S1 (S-c words rule) | C3 shared item S-c (replacement text applied); three rows' words then checked against the code → fork F-T6 |
| F-S2 (DoD flag) | C3 shared item "DoD of every C3 card" (with `gate_registry.py:968-971`) |
| F-S3 (`_scan_tree` -> `_walk`) | §0.1 |
| F-S4 (census, S-e) | C3 shared item S-e; used by C3-b1, C3-j owns; §3 collisions |
| F-S5 (E-c re-role table; "true accept sites after E-c" column) | C3 "Decided branches" (column replaced) and "Re-roles judged by the plan critic (E-c)" (with the t-994 read column) → forks F-T1, F-T3 |
| F-K7 (one registry node) | C3-R card; §3 wave 2; §5 row RD2-C3-R |
| F-0-1 (C3-0 written for (a)) | C3-0 card rewritten for F-D1 (b); §3 waves 2½/3 |
| F-0-2 (signature does not fit) | C3-0 items 1-2 (`acceptable(value, consumer)`, word or record; class-space accepts) → F-T1 for the `_match` word |
| F-a1 (C3-a pin in a quarantined file) | C3-R item 1 (M-B3 world into `test_node_ids.py`; stop rule) |
| F-a2 (C3-a words) | C3-R item 1; `not_verified` not written → `["node_id_mismatch"]` (critic's fallback; §7) |
| F-b1 (unknown vs absent; relaxes a block) | C3-b1 "What changes, and what does not" + measured premise (Lead decision 5) |
| F-b2 (answer carrier) | C3-b1 items 2-5 on rec → fork F-T4 |
| F-b3 (registry edit incomplete) | C3-b1 item 6 |
| F-b4 (E3 not decidable) | C3-b1 item 1 / E3 on rec → fork F-T5 |
| F-b5 (split) | C3-b1 and C3-b2 cards; §3, §5 |
| F-c1 (C3-c: no code, no new row) | C3-R item 2 (as written) → fork F-T6 on its words |
| F-c2 (FL9 queue moot) | C3-R item 2 / §3 collisions; FL9 card note |
| F-d1 (C3-d red by design) | C3-d card (fact re-read, premise measured, rec (i) drafted) → fork F-T7 |
| F-e1 (C3-e owns/test/new row) | C3-R item 3 |
| F-e2 (FR-3 door) | C3-R item 3 and E6 |
| F-f1 (test status) | §0.3 and C3-R item 4 (keep, fast; in the DoD) |
| F-f2 (wrong unknown; refuse_with_door) | C3-R item 4; Decided-branches row (Lead decision 3, «Lead, 17.11.2026, по рекомендации критика, до слова владельца») |
| F-g1 (C3-g after C3-0; refusing function) | C3-g card (wave 3) → fork F-T3 |
| C3-h fix (vocabulary code, words unchanged) | C3-h card; queue position 3 |
| F-i1 (registrations decided) | C3-R items 6-8 (as written) → fork F-T6 on words |
| F-i2 (existing pins; one new row; leaves the queue) | C3-R items 5-7; gate_preflight queue C3-j → C3-k → C3-h |
| F-j1 (writer road; stand_gaps; census) | C3-j owns (replacement applied) |
| F-j2 (old waiver passes) | C3-j E9 |
| C3-k fix (queue text) | C3-k card ("after C3-0 under F-D1 (b)") and gate_preflight queue |
| F-9-1 … F-9-6 (S9) | designer: S9/FL file (`20261117-rules-debt-phase2-s9-fl-cards-spec.md`); S9 card here is a pointer |
| F-L2-1 … F-L2-3 (FL2) | designer: S9/FL file; FL2 card is a pointer; §3 "FL2 after C3-R" |
| F-L4-1, F-L4-2 (FL4) | designer: S9/FL file; FL4 card is a pointer; §3 "FL4 after S9" |
| K6 — gate-registry.json | §3 collisions (C3-R one writer; C3-0 one site line; S7 row) |
| K6 — judgment-census.json / wave-a/integrate | S-e; §3 collisions and wave 2½/3 orders |
| K6 — s5_precheck.py | §3 collisions; FL9 note (+19 drift) |
| K6 — gate_preflight.py | §3 wave 3 and collisions (C3-j → C3-k → C3-h) |
| K6 — window_record.py / controller.py | §3 (S9 → C3-b1 → C3-d; S9 → FL4) |
| K6 — delivery-verdict-kinds.json | §3 collisions (FL2 only) |
| K6 — pile/live-run-fvf/batch-3 (dry story) | §3 collisions (C3-R untouched; C3-0's covers line → queue line) |
| K6 — taken batches | §4 (unchanged decision; C3-R line added) |
| K6 — parallel now / afterwards | §3 waves 2, 2½, 3 |
| K8 — axis 4 (B-ids; B-255 not closed) | C3-R siblings and E7; S1b item 1 |
| K8 — axis 7 | C3-b2 siblings |
| K8 — axis 25 | C3-d siblings |
| K8 — axes 26 / 32 / 34 / 5 | 26, 34: S9/FL file and C3-b1 (F-T8); 32: S-e; 5: S9/FL file (FL4) |
| K8 — B-255 shared | C3-R E7, siblings; S1b item 1 |
| Standing q6 (duplication: new rows for C3-c/C3-e) | C3-R items 2-3 (no duplicate rows; the unreadable-kinds row is new because unpinned) |
| Standing q12 (one road) | C3-0 E9; C3-b1 F-T8; FL2 in the S9/FL file |
| Standing q5 (tests) | C3-R E9 (M-B3 world into keep); no new test file in any card |

## Forks returned (t-1033)

Each is the Lead's (technical); none is decided here; every card named executes on the recommendation.

- **F-T9 — the shape of C3-d's review acceptance** (C3-d; t-1026 B3 offered two forms). The critic's word closes a review
  differently by the instance's kind: `approved` only (ran), `unverified` only (stopped, probe-gapped), either (handed).
  One word has one class in `verdict_map`, so one consumer cannot say all three. (a) three consumers on the `s5_window`
  row — `s5_window.review: ["matched"]`, `s5_window.static_review: ["not_applicable:static_review"]`,
  `s5_window.handed_review: ["matched", "not_applicable:static_review"]` — with `approved` -> matched and `unverified` ->
  not_applicable (reason `static_review`: the live check did not apply, the critic read the test); one call per decision,
  `validate_window` stays the row's accept site; (b) the review acceptance as a row of its own (`window_review`) with the
  same words and consumers — but `validate_window` would then be registered by two rows with a converted accept site,
  which A26 refuses ("registered more than once", `gate_registry.py:832-836`), so (b) needs the review branch moved into a
  function of its own (a code split); (c) keep `s5_window` debt and only correct `decides` (no conversion). **Rec (a)**:
  no code split, the grammar already holds `not_applicable:<reason>` (`gate_registry.py:477-480`), the predicate already
  accepts it (C3-0 item 2); cost: a class word (`not_applicable`) given a meaning ("static review") the Lead approves.
- **F-T10 — test_identity's other `same_test` readers** (C3-b2; found by the t-1033 class sweep of B4, not judged by a
  critic). `_evaluate` (:1580; `how = same_test(...)`, `if not how:` -> the receipt is not valid, :1604-1605) is a receipt
  acceptance by truthiness — a true accept, unregistered; `_stale_receipt` (:1886; :1898) builds a why (produce);
  `holds_over_comments` (:1552; :1562 `in ("instance_code", "file_code")`) has no production caller (grep
  `holds_over_comments\(` over `scripts/`: its def and `tests/test_proof_level.py:1499-1500` only; control: the same grep
  finds the def). (a) C3-b2 also routes `_evaluate` through `acceptable(how, "test_identity.receipt_holds")` (matched-class
  words = the truthy words: the same receipts count), allow-lists the display flag at :1613, registers `_stale_receipt`
  `produce`, and files a finding "delete or wire `holds_over_comments`" in the rules-debt pile; (b) queue all three to a
  follow-up node after C3-b2 (the row converts while a truthiness acceptance stays outside the predicate — invisible to
  A26, docstring :63-66). **Rec (a)**: one card for one row's accept sites (E-c: "a re-role never hides a literal
  acceptance" — here an unregistered one); cost: one function and one test row more in C3-b2.
- **F-T11 — what a converted site says when the registry itself cannot be read** (C3-0, C3-b2, C3-d; an edge the C3-0
  E2 invariant creates). `acceptable` returns only a boolean, so a site that refuses on a broken registry would print its
  usual reason: `_run_freshness` "the test … changed since its run", `_match` the bytes reason (both false, FR-41), and
  `validate_window` a `review:<iid>` gap whose door (the critic records a verdict) cannot close it (a dead end, FR-57).
  (a) C3-0 adds `registry_problem()` (C3-0 item 9); a site that prints a WHY (`_run_freshness`, `_match`) names the
  registry when it is non-empty (owner factory); `validate_window`'s gaps stay as they are and the dead end is a residue
  node: a window-level gap kind (e.g. `gate_registry:`) with a controller route and the door "the plugin's
  `references/gate-registry.json` cannot be read: reinstall or update the plugin" — a mechanism (controller-blocks) the
  Lead opens as its own node; (b) no helper: accept the false reasons, because the registry is a package file checked by
  CI (`test_gate_registry.py`) and never changed by a project (`gate_registry.py:16-19`), so a broken one is a broken
  install; (c) an in-code floor of accepted words when the registry cannot be read (a second road, P31 — not
  recommended). **Rec (a)** with the residue node; cost: one pure function in C3-0, a branch of text in two sites, one node.
  Until the Lead answers, C3-b2 and C3-d execute on (a) without the residue node.

## Fix round t-1033 — where each t-1026 finding went

| finding | what changed | section |
|---|---|---|
| B1 (pins of `test_gate_registry.py` move with every conversion; same-file collision with no order) | new shared item S-f: the pins by line (2151eeef), the D13 re-measure item, TEMPORAL both worlds (today / after t-1032 / after each sibling, D-0048 re-derivation), expected merge order; `owns:` line + item in C3-b1 (item 7, E11), C3-b2 (item 7, E10), C3-d (item 7), C3-g, C3-h, C3-j (item 5, E10), C3-k, C3-rr (item 4, E5); C3-0 item 7 moves the F4 flip control onto an in-memory row, item 8 its own D13 triple, E10 | C3 shared items S-f, E-e; C3-0; C3-rr; C3-b1; C3-b2; C3-d; C3-g; C3-h; C3-j; C3-k; §3 |
| B2 (C3-0 E6 false negative) | E6 rewritten: seven consumer ids exist, none read by a script (grep with its positive control), the two dead ones go in C3-k (A2) / C3-g (F-T3); no real `acceptable` call before C3-b2 / C3-rr / C3-d; invariant widened (no `accepts` without its reader) | C3-0 E6 |
| B3 (`validate_window` is a true acceptance of the critic's review word) | C3-d redrafted: `validate_window` stays `accept`, words `approved`/`unverified`, three consumers (fork F-T9, rec (a)), the four comparisons through the predicate, `HANDED_REVIEW_VERDICTS` deleted, `window_record.verdict` produce, `window_record.build` produce (new), review table, census unchanged (shape), queue C3-0 → C3-d; E-c table rows | C3-d; E-c table; Decided branches; §1; §3 |
| B4 (two test_identity reuse decisions missing) | C3-b2 redrafted: `_product_receipt_repeat` (item 3, S-b row) and `_run_freshness` (item 4, rows, E7 with the error direction) through the predicate, owns +2 functions, consumer `test_identity.run_fresh`, siblings axis 25; the class sweep's three more readers → fork F-T10 | C3-b2; E-c table; fork F-T10 |
| B5 (F-T5's consequence incomplete) | F-T5 rewritten with the writer's carriers (V2 :826-840, the whole-failure `except` :923-926, `_keep_stored_novelty` :855-887): cases (1)-(4); new option (a+) (the marker) recommended; plain-words lines for the owner; C3-b1 item 1, item 8, owns `_attach_novelty`, E3, E10 follow | Forks returned (t-994) F-T5; C3-b1 |
| B9 (C3-d S-b expected value) | expected = `"expectation changes " +` the `not_measured` row of `expectation_change_words` (`handoffs/vocabulary.yaml:300`) with `why` substituted, read from the data file | C3-d item 6 |
| B10 (C3-0 other keys; keep row line drift) | `test-layers.json:2028-2030` → `:2032-2033` (keep row), covers list `:2035-2076`; quarantine start `:7207`; registry row lines in `given` refreshed for 2151eeef; K3 / F-T1 (a) / F-T2 (a) agreement noted | C3-0 header and item 4; §0.3 |
| C3-b1 other keys (K1, K2, K4, K9 hold) | no edit owed; noted in the card head; F-T4 (a) and F-T8 (a) stand as recommended | C3-b1 head |
| A1 (`reporter_rehearsal_identity`'s true accept site unregistered; Lead option (a)) | new card C3-rr (header-ready): `accepts` consumer `reporter_rehearsal_identity.reuse`, `acceptable(earlier.get("state"), …)` after the hit checks at `gate_preflight.py:3843`, table rows, S-f pins (D13 -1 triple); E-c rows for `_reporter_outcome` (true accept) and `_record_unreadable` (produce); Decided-branches row; gate_preflight queue C3-rr → C3-j → C3-k → C3-h; §5 row | C3-rr; E-c table; Decided branches; C3-k queue line; §3; §5 |
| A2 (`provenance.environment_preparation` a dead consumer) | C3-k line: removed in C3-k's registry commit; the consumer `_run_step` calls is added only with that reader, under a promotable-false row; the F1 pins move with it (S-f) | C3-k |
| (beyond the list, found while reading) | F4/F1/K-N2.12 consumer pins (:285-292, :627-647) named in S-f for C3-g/C3-k; the registry-doubt reason edge → fork F-T11 with `registry_problem()` (C3-0 item 9); F-T6 note: the merged registry already carries (b)'s words | S-f; C3-0; forks |

## Not done / not established (t-1033)

- Nothing was RUN (no shell): `gate_registry.py --check` / `--sites`, `GR.analyse` before/after, the
  `validate_window` / `run_freshness_of` controls over the recorded windows — each is named as a command in its card.
- t-1032's exact diff is not read (in flight): the S-f "after t-1032" numbers (debt 8 / converted 19, the two D13 triples,
  count ≈ 140) follow the verdict's A1 (a) text and the journal line `dev1.jsonl:2642`; C3-0 and every converting card
  re-derive from main after it merges. (t-1043: superseded — t-1032 is merged and its pins are on main, S-f; D13 is 140 after it and 146 after C3-0, a4aca646.)
- Whether `manifest_put` takes a top-level string key from a fragment through its scalar loop was read only at
  `manifest_put.py:158-172` (the loop's exemption list), not the loop body or the manifest schema: C3-b1 item 8 carries a
  stop rule.
- Whether `gate_preflight` importing `gate_template` cycles was not read (C3-rr item 2 leaves the import place to the
  builder's read). (t-1043: closed — `gate_registry.py:97-104` stdlib + `hooklib`, `hooklib.py:2-13` stdlib only; the builder re-checks against the merged C3-0.)
- Noticed analogs of A1's class, not carded (reported, scope not widened): `validate_window`'s probe comparisons
  (`probe.get("verdict") != "intended_failure"` and the rest of `acceptance.py:1210-1218`) compare words of rows that do not
  register `validate_window`; `window_record.build`'s `BLOCKED_REVIEW_VERDICT` comparisons (:1524, :1625) use an imported
  name invisible to A26.
- C3-g, C3-h, C3-j and C3-k gained only their B1 lines (and C3-k the A2 line); they stay designer-first sketches, not
  header-ready, as before this round.
- Whether `pile/live-run-fvf/batch-3` merged (the C3-0 `test-layers.json` queue line) was not read.
- The S9/FL findings of t-1026 (B6, B7, B8, B11, B12, B13) belong to `20261117-rules-debt-phase2-s9-fl-cards-spec.md` and
  were not touched; A3-A6 are t-1032's.

## Reading trail (t-1033)

On 2151eeef (root checkout; `.git/refs/heads/main` = `.git/refs/remotes/origin/main` = 2151eeef…, read directly):
- the verdict `docs/tasks/specs/reviews/t-1026-rules-debt-wave2-code-and-cards.md` (whole, :1-383);
- this spec (whole, :1-1465 of the t-994 text);
- `scripts/tests/test_gate_registry.py` :36-71, :278-292, :310-339, :620-647, :720-759, :900-1013 (+ grep of the pin names);
- `references/gate-registry.json` :38-92, :120-354, :496-543 (+ greps of `id`/`vocabulary`/`status`/`debt_ref`; of
  `run_freshness|_product_receipt_repeat|validate_window|"build"|_reporter_outcome|_record_unreadable|held_words|holds_over_comments`:
  `validate_window` :231 and `execution_fingerprint` `build` :44 only — the hits are the control);
- `scripts/gate_registry.py` :1-150, :425-484, :485-681, :780-979;
- `scripts/gate_preflight.py` :3820-3888, :3950-3974 (+ grep of `_reporter_outcome|_record_unreadable|same_command|earlier`);
- `scripts/tests/test_gate_preflight.py` :5199-5238 (+ grep `c3r|command_changed|same_command`, case-insensitive);
- `scripts/acceptance.py` :25-50, :240-259, :1052-1231 (+ grep of the review constants);
- `scripts/window_record.py` def list, :1505-1540, :1600-1640, :1771-1914 (+ grep of the review build at :1474);
- `scripts/contract.py` :2205-2219; `agents/qa-code-critic.md` :68-84 (+ grep `unverified`); `handoffs/vocabulary.yaml` :290-303;
- `scripts/proof_level.py` :815-974, :1360-1564, :1585-1614, :1880-1905 (+ greps of `same_test(`, `holds_over_comments(`);
- `scripts/manifest_from_tests.py` :800-949 (+ grep of `notes`/`fragment[`); `scripts/manifest_put.py` :158-172 (+ grep);
- `scripts/tests/test-layers.json` :2030-2076 (+ grep of the keep row and `"quarantine"` :7207);
- `scripts/tests/fixtures/judgment-census.json` :1-6 (+ grep of the owned functions: `validate_window` :7 only);
- Glob `scripts/gate_*.py` (4 files, no `gate_template.py`); grep `provenance\.(…)\b` over `scripts/*.py` (test hits only);
  grep `HANDED_REVIEW_VERDICTS|BLOCKED_REVIEW_VERDICT` over the package; grep `validate_window\(` over `scripts/*.py`
  (production callers listed in §8); grep `acceptable_provenance\(|def _run_step|ACCEPTS` over `scripts/*.py`;
- `logs/journal/dev1.jsonl` grep `t-1032` (:2642-2643);
- rule 7 greps of §8 over `tools/`, `.githooks/commit-msg`, `.claude/settings.json`, `.claude/agents/` with their controls;
  `tools/dup-baseline.json` :82-96; `tools/source_split.py` / `tools/source-split-carriers.json` (grep).

## Lead decisions after t-1033 (17.11.2026, Fable; по рекомендации, до слова владельца — the owner is away)

- F-T1 (a), F-T2 (a) (agreed by critic t-1026). F-T6: the merged registry's words (b) stand.
- F-T5 (a+): the `novelty_unmeasured` marker. The plain-words lines for the owner go into the morning report.
- F-T7 (i): the row's `decides` is corrected to the code and converted as is; (ii) stays an owner question.
- F-T9 (a): three consumers on the `s5_window` row; `not_applicable:static_review` approved as the class word.
- F-T10 (a): C3-b2 also routes `_evaluate` through the predicate; finding "delete or wire `holds_over_comments`".
- F-T11 (a): `registry_problem()` in C3-0; the window-level gap kind for an unreadable registry is a residue node.
- Re-review of the t-1033 redrafts (C3-b2, C3-d, C3-rr): one plan-critic pass before their dispatch (new shapes F-T9,
  F-T11); C3-0 and C3-b1 were passed by t-1026 and are dispatched without it.
- C3-0 report: `docs/tasks/specs/reports/20261117-rules-debt-c3-0-report.md`.

## Lead decisions after t-1039 (17.11.2026, Fable; по рекомендации, до слова владельца — the owner is away)

Review: `docs/tasks/specs/reviews/t-1039-rules-debt-c3-redrafts-plan.md` (needs work, 0 blocking). All of R1-R15 are
taken into the cards in one designer fix round (t-1043), the optional ones (R7, R13, R14, R15) included.

- R5 (b): the F-T11 residue is ONE story-level precondition, not a window gap kind: a read of
  `gate_template.registry_problem()` at stage entry stops the story with the reinstall door, owner factory, reported
  and not asked (FR-3); one controller block and one `state-exits.md` row. The per-site text branches of F-T11 (a)
  stay as belt-and-braces. The node is "C3-reg-precondition" (pile `rules-debt`), after C3-0; its card is drafted in
  the same fix round. C3-b2 item 4 / E5 drop "owner factory" (the critic's text edit).
- R12: the analogs wait as findings named in the cards' `siblings:` lines; none is carded first.

## Forks returned (t-1043)

None of them reopens F-T1..F-T11. Each card executes on the recommendation.
- **F-T12 — the precondition's route.** (a) person-passable: `_passed_by_person` and the controller-blocks route `person`. The text reports a factory defect and does not ask (FR-3); the waiver is the standing FR-4 road. A pass runs the stage with every converted site refusing reuse, so it is cost, not a false pass. (b) route `command`, no word passes (strict reading of "reported and not asked"). **Rec (a)**: FR-4 ("a person's word passes any block"), P13, builder-rules 8 and AR-9's change check (`architecture.md:111`, "its person's-word route") all demand it. The Lead's "not asked" holds because the text asks nothing. Cost: one line.
- **F-T13 — the driver's routing of the new refusal.** (a) no `KNOWN_REFUSALS` row: it is unmatched and goes to the conductor (FR-48), who reports it. (b) a row `("gate_registry", r"gate registry unreadable", "error")` beside `no_project` (`driver_dispatch.py:106`): it stops with no paid call, but costs a driver_dispatch.py edit, the dry_exits recount (21 -> 22, `tests/dry_exits.py:491,860`) and a driver-layers.json note. **Rec (a)**: a broken install is rare, and a phrase row adds to a table FR-12 is moving out of code (N5).
- **F-T14 — what "stage entry" means.** (a) every `dispatch`, in `validate`'s dispatch branch: the one road all stage starts take (start, rework, relaunch, retry, driver). (b) `prepare` / `_next_action_for_state` (`prepare_stage`): `prepare` is read-only and rework and relaunch bypass it, which would be a second road (P31). (c) also `accept` and `resume`. **Rec (a)**; (c) is not needed, because the sites already err toward not-acceptable (E6).
- **F-T15 — the test layer.** (a) one table in `test_controller_state.py` (keep detector; judged by canon). (b) a `variants.json` row of a recorded story at the walker's `start` door: a better layer, but whether a variant can break a PACKAGE file (not a story file) was not read. **Rec (a)**, executable now; (b) is a scout question if the Lead wants layer 1.

## Fix round t-1043 — where each t-1039 finding went

| finding | where edited (section, item) | what changed |
|---|---|---|
| R1 | C3-b2 item 4; owns | the existing pins named (test_run_freshness.py:73, K1 (b) :80-86, K1 (f) :104-106, K1 (d) :92-98); one registry row there; owns gains test_run_freshness.py |
| R2 | C3-b2 item 6; E8 | `_evaluate` names the registry; a second row; the `_stale_receipt`/`probe_freshness` `missing` residue named |
| R3 | C3-b2 items 2, 5; owns | probe-record row moved to item 2; `_match` rows return `("", why, _WHY_RANK["bytes"])` for bytes and for the registry; test_execution_request.py gets two rows |
| R4 | C3-b2 item 7 | D13 expected +2 triples (same_test:881, _evaluate:1613), count +2 from base 146; a different measurement stops |
| R5 | C3-b2 item 4, E5; new card C3-reg-precondition; C3-d E3; C3-rr item 5 | "owner factory" dropped; the gap's owner and door stay; the loop is the new node's; node drafted (R5 (b)) |
| R6 | C3-d item 1 | `decides`: `unverified` closes the review only, the instance stays unresolved (D-0013) |
| R7 | C3-d item 6; owns | the pin exists (test_window_record.py:2110-2111, :2117): named, no row |
| R8 | C3-d item 7 | D13 exactly +1 triple build:1532, count +1 |
| R9 | C3-rr item 3; C3-b2 items 4-6; C3-d item 5; owns | the seam is C3-0's `_READ` cache (a4aca646 :31-37), patched and restored in `finally`, or stop; owns name the import lines; the cycle question closed |
| R10 | C3-b2 Measurement; C3-d Measured premise | C3-b2: the run is vacuous, the premise rests on a code trace; C3-d: emulation 6/6 equal, negative control, branch limit |
| R11 | S-f TEMPORAL; C3-rr head, given, item 4, E4; §3; «Not done»; §5 | t-1032 merged; D13 140 -> 146 (C3-0) as base; main line numbers refreshed; batch carriers missing (grep) -> §5 |
| R12 | C3-b2 siblings (a, d); C3-d siblings (a, c, e); C3-rr siblings (b, e) | analogs as waiting findings; axis 26 -> axis 5 :143 with the prose-twin line |
| R13 | C3-b2 E11 | one producer per consumer invariant |
| R14 | C3-b2 owns, non-goals, item 5 | the `same_instance_bytes` docstring sentence (:2069-2072) owned and rewritten |
| R15 | C3-rr item 5; new card E2 | what `registry_problem()` covers (unreadable file) and not (missing consumer/words); the CI backstop |

## Facts of the fix round t-1043

(read in t-1043, root checkout; main HEAD 60c41e39 per the session git snapshot, not re-run)

- C3-0 is NOT on main. Glob `ai-packages/qa-factory/scripts/gate_template.py` on the root found nothing; the same Glob over `.claude/worktrees/*/…` found it in `agent-aa11322709a274e56` (positive control).
- That worktree's branch is `worktree-agent-aa11322709a274e56`, ref `a4aca64694799c8c649449d9ce0dd8f054240487` (read from `.git/refs/heads/…`). I read the worktree's checkout, not `git show a4aca646:`, so I could not confirm the tree has no uncommitted edits.
- `gate_template.py` on that tree:
  - :29 `import gate_registry`;
  - :31-37 `_READ = []`, which holds one `(registry, reason)` from `gate_registry.load_registry(gate_registry.PLUGIN_ROOT)`, read once per process; a failure is cached as such;
  - :40-43 `_registry_and_reason`: with `registry=` given, it returns `(registry, structural_error(registry))`;
  - :46 `def registry_problem(*, registry=None) -> str`, which returns "" or the reason, `"it is not available"` when there is no data, or `"it cannot be read (<Exc>)"`, and never raises;
  - :60 `def acceptable(value, consumer, *, registry=None) -> bool`, False on every doubt, never raises;
  - :87-94: the six counted comparisons.
- `test_gate_registry.py` on that tree:
  - :951 has the new triple;
  - :1003-1006 reads `140 -> 146 (C3-0, t-1038)`, `D13_ITEM_COUNT = 146`;
  - :1108-1119 is the cache seam precedent: save `list(GT._READ)`, swap `GR.PLUGIN_ROOT` to an empty dir, `GT._READ.clear()`, restore in `finally`.
- The C3-0 report (on that tree, `docs/tasks/specs/reports/20261117-rules-debt-c3-0-report.md`):
  - :11 has 140 -> 146 with six comparisons, the two `not_applicable` ones included;
  - :54 has an OPEN audit A1 finding, "gate_template.py is reachable from nothing".
- t-1032 is merged on main:
  - `test_gate_registry.py:55-61` EXPECTED_DEBT with `reporter_rehearsal_identity: B-283`;
  - :334-336 split 19/8/6; :247 K-T1.2 "8";
  - :930-932 the `_record_unreadable` / `_reporter_outcome` triples; :991-994 `138 -> 140`, `D13_ITEM_COUNT = 140`;
  - journal `dev1.jsonl:2649` `accepted` t-1032.
  - The merge sha 7f2f6f78 is the critic's run (t-1039), not re-run here.
- Main line numbers in `test_gate_registry.py`: EXPECTED_DEBT :58-61, EXPECTED_CONVERTED :64-69, K-T1.2 :247, split :334-336, F4 flip :753-756 (:760 on C3-0's tree), D13 :913-994.
- `gate-registry.json` on main:
  - test_identity :123-149 (words :135, verdict_map :136-141, status :148);
  - s5_window :227-248;
  - reporter_rehearsal_identity :498-523 (sites :502-506, words :509, status :522).
  - C3-0 adds one line in `provenance_acceptance`, so every later row is +1 on its tree.

- Conflicts between findings or Lead decisions: None found. R9's "if C3-0 exposes no reset" is settled by `_READ`. R2's residue is now a residue of the R5 (b) node.

## Small choices closed (t-1043)

- Test seam = `gate_template._READ` (a private module list): C3-0's own test uses it (:1108-1119 on its branch).
- The new card's raise sits in `validate` (the existing census unit), not in a helper (a new unit).
- The import of `gate_template` in controller.py is at the point of use (the file's late-import style).
- The registry-why wording is one family across sites: "the gate registry cannot be read (<reason>): a factory defect, …".

## Not read (t-1043)

(never written as checked)

- `git show a4aca646 --stat` and `git show a4aca646:…` (no shell). The worktree checkout was read instead (branch ref = a4aca646); whether that tree has no uncommitted edits is not established.
- The merge sha 7f2f6f78 (critic's run).
- `test_proof_level.py:1554-1556` (no run_freshness table: the critic's grep).
- The F4 `code` list :729-738.
- `check_delivery.py:860`, `case_stamp.py:317`, `window_record.py:318-319`, `test_window_record.py` helpers.
- `waiver.split_overridden` (whether a pass over a factory block is filed as a finding).
- Whether `test_controller_blocks.py` pins the header counts.
- `controller-blocks-gen.py`'s classifier for a `person` row.
- Whether `test_state_exits.py` is in SLOW_TESTS.
- Whether a controller.py import clears audit A1 for gate_template.
- `tools/mechanism_gate.py`'s prefix list.
- The axis-5 prose twins for test_identity's words (left to the builder).
- `scenario_walk.py --witness-for` output for the new owns.
- No run of `GR.analyse` / `--check` / `--sites` (D13 deltas are the critic's measurement plus C3-0's report).

## Reading trail (t-1043)

- review `docs/tasks/specs/reviews/t-1039-rules-debt-c3-redrafts-plan.md` (whole);
- spec :270-409, :529-773, :910-1170, :1458-1707, :1940-2076;
- C3-0 tree: `gate_template.py` (whole), `test_gate_registry.py` (grep of pins; :995-1009, :1095-1143), the C3-0 report (whole), `.git/worktrees/…/HEAD`, `.git/refs/heads/worktree-agent-aa11322709a274e56`;
- main `test_gate_registry.py` :55-70, :328-339, :745-758, :910-997; `gate-registry.json` ids (grep), :122-151, :226-249, :497-524;
- `gate_registry.py` :1-110, :425-469, :829-837; `hooklib.py` imports;
- `gate_preflight.py` imports and :3824-3871 (+ grep); `profile_contract.py` :345-363, :417-418 (grep);
- `proof_level.py` :815-974, :1365-1401, :1462-1463, :1485-1524, :1578-1617 (+ grep :1814, :1886, :1898, :1947, :1972); `execution_request.py` :2062-2113;
- `test_run_freshness.py` :1-125; `test-layers.json` :871-882, :1082-1093, :4702-4710, :5528-5539 (+ grep :7207);
- `acceptance.py` :30-45, :1140-1179 (+ grep :1211); `window_record.py` imports/defs (grep), :28-47, :340-353;
- `agents/qa-code-critic.md` :74-84; `handoffs/vocabulary.yaml` :293-302; `test_window_record.py` :2100-2119;
- `docs/SIBLING_MAP.md` :136-147, :448-456; `phases/s5.md` (grep), :158-187; `code-review-rubric.md` (grep), :90-94;
- `controller.py` defs (grep), :2030-2244, :2470-2483, :5170-5194, :5364-5383, :5488-5547, :8704-8751, :9012-9273, :10050-10083 (+ greps of `self.validate(`, `_passed_by_person(`);
- `design/controller-blocks.md` :1-60 (+ greps); `design/state-exits.md` :1-20, :136-145 (+ heading grep); `test_state_exits.py` :1-131; `test_controller_blocks.py` (grep);
- `judgment-census.json` :1-8 (+ grep :238, :245); `refusal_registry.py` :38-47; `driver_dispatch.py` :30-144; `architecture.md` change-check grep (:111, :155, :166, :180, :261, :282);
- `factory-rules.md` :47-64; `plans/builder-rules.md` (whole); the S9/FL spec :334-337 (+ grep);
- `plans/piles/rules-debt` (Glob + grep with control); `logs/journal/dev1.jsonl` :2642-2649 (grep);
- rule-7 greps as in B8.

## Lead decisions on forks F-T12..F-T15 (17.11.2026, Fable; по рекомендации, до слова владельца — the owner is away)

- F-T12 (a): the precondition's refusal is person-passable (FR-4, P13); its text reports and asks nothing (FR-3).
- F-T13 (a): no `KNOWN_REFUSALS` row; the refusal goes to the conductor.
- F-T14 (a): "stage entry" is every `dispatch`, in `validate`'s dispatch branch.
- F-T15 (a): one table in `test_controller_state.py`.
