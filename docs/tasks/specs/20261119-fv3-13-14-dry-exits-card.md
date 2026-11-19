# FV3-14 then FV3-13: one count per live_only subject; "told before work" in the dry story (t-1549, draft)

Node: live-run-fvf/3 (FV3-14, FV3-13), feature F19. Two builder headers, run SERIALLY in this order (both write
`scripts/tests/dry_exits.py`). Designer draft; every decision below marked "fork" is the Lead's.

## §0 Measured state (designer; Grep/Read; a command for each in the trail)
- M1 `_count_reach` (`dry_exits.py:638-646`) counts every census row and every walk row by reach; `_raised` (`:719-739`) builds the
  valid refs from the same two sets. Its only caller is `_ratchets` (`:745`); no other reader in `ai-packages/` (Grep, control = the hit itself).
- M2 Every group's `ratchet.live_only` base is 0 (gates, s0, s1-s4, s5, s6-s9, hooks). All 98 live_only rows (70 census + 28 walk) are
  credited one by one in `raised_by`: gates 37, s0 16, s1-s4 15, s5 30. No `after:` reach exists anywhere (0; control: `"reach": "live_only"` -> 99, the
  extra one is `stories/dry-1/selftest/exits/selftest.json`, which the census never reads).
- M3 Paired walk rows (a live_only walk row whose subject has a live_only census row): gates 15 (`walk/route:<15 routes>/...`), s0 8, s1-s4 4
  (`kind:conductor`, `route:s1_gap`, `route:s1_review`, `route:structured_artifact`) = 27. Walk-only: 1 (`walk/gate_A/words:questions-deferred`, a
  price key, no census row). Census-only: 43 (incl. all 30 of s5). Derived from the `raised_by` entries; `estimate` until the Lead runs `--check`.
- M4 P1-v N0 / W0 IS on main: `driver_core.py:138-149` (`Refusal.checks`, `checks_n`, one `unknown` for none), `driver_runner.py:892`
  and `:996-997` (a resume the CALLER asked for writes `checks` + `checks_n`; the driver's own resume of a cut call and every non-resume row
  write neither). `resume_kind` and the closed lists `resume_kinds` / `rework_kinds` are in `references/run-record.json:5-6`, read only via
  `driver_journal.run_record_names`. FV3-13 is NOT blocked.
- M5 `brief_pack.requirement_rows` does NOT exist (case-insensitive Grep over the package: 0; control `digest_template_lines` -> 12). The reader
  of "rows a receiver is told" that landed is `stage_joints.rows_for(role, stages, dispatch=None, data=None)` (`stage_joints.py:555`), the
  call `contract_slices.py:674` renders the role page with, and `stage_joints.py:835` already uses as "told by the page". Fork F1.
- M6 `dry_world.main_pass` closes its world in `finally` (`dry_world.py:1067-1068`; `World.close` -> `harness.cleanup(self.root)`, `:278-282`):
  after `main_pass` returns, `world.task_root` and its `state/driver-runs.jsonl` are gone. A `_print_told` in `test_scenario_dry_1.py` after
  the pass has nothing to read. Fork F2.
- M7 `test_scenario_dry_1.py` is in `scripts/slow_tests.json` `files` (221.6 s): canon class, never run whole locally (`docs/TESTING.md`).

## §1 Architecture, owners, variety
- AR-20 (ratchets; a raise named row by row). FV3-14 changes what a raise row IS. Change check in DoD A: `--check` = 0 on the tree with the
  rebased `raised_by`; the verdict names the 27 dropped entries and the new count 71 (98 - 27). No base moves (all 0, M2).
- AR-28 (an unknown never becomes a pass). FV3-14: absorption errs toward COUNTING (a walk row is absorbed only by an exact live_only census row of
  the same section and name). FV3-13: `unknown`, a fallback id, no `checks` on a rework resume, an unreadable carrier - each a red result, never PASS.
- AR-13 (one reader). FV3-14: one function yields the counted refs, `_count_reach` and `_raised` both read it. FV3-13: `driver-runs.jsonl` via
  `driver_journal.read_rows_counted`; the closed lists via `driver_journal.run_record_names`; the rows file via `stage_joints.read_rows`; "told"
  via `stage_joints.row_for` + `rows_for` (F1).
- AR-10 (a check's requirement reaches the role before the work). FV3-13 is its detector in the dry story (A2 §1). Change check in DoD B: the
  negative controls (row absent for the role; row named for another role) are red.
- AR-29 census: both changes live in `scripts/tests/`, outside `test_judgment_census.py`'s scope. FV3-14 ratchet sum = class `xref`, owner
  data (code). FV3-13 C11 = class `xref`, owner data (code) (A2 §1 row C11). Commit line: the `judgment:` line in the form
  `tools/architecture_gate.py` checks, value `none -- <why>`, why = "scripts/tests only: a count join (A) / a presence join of check id to
  requirement row (B); no role output judged".
- `variety: none -- both nodes change the forge's dry-story census and walker; no project axis of design/architecture.md § A is read or branched on.`

## Card A - FV3-14: one live_only count per subject

given: this card §0-§1; `docs/tasks/specs/20261117-p1b-finish-spec.md` :576-579 (F-P8) and :811 (Lead: reading 2); `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\dry_exits.py::_count_reach`, `::_raised`, `::_ratchets`, `::_subject_of`, `::_selftest_cases` (ratchet rows near "the ratchet at and beyond its base"); the fixture files under owns
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\dry_exits.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\driver-exits\gates.json
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\driver-exits\s0.json
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\driver-exits\s1-s4.json
non-goals: no change to `after`/`unwalked`/`hook_layer` counting (F3); no walk file or census row edit (only `ratchet.raised_by`); no base change; s5/s6-s9/hooks files untouched (no paired rows, M2-M3)
handoff: report `C:\QAFactory\forge-repo\docs\tasks\specs\reports\20261119-fv3-14-report.md` (before/after `--check` tails, the 27 dropped entries listed) + commit hash
edges: the table "Edges A" of this card (E-A1..E-A9), every row with its invariant
DoD: `python -B ai-packages/qa-factory/scripts/tests/dry_exits.py --selftest` all cases pass; `python -B ai-packages/qa-factory/scripts/tests/dry_exits.py --check` prints `0 discrepancies` and the NOTE `ratchet live_only: raised 71 row(s) above the base 0`
siblings: axis 18 / AR-20 (other ratchets: none changes); FV3-25 (pending, writes s5 walk rows that will turn live_only: a price-key walk row counts on its own, E-A3 - whichever lands second rebases on the merged tree); in-flight worktree `.claude/worktrees/fv3-22-2` holds a `dry_exits.py` copy - the Lead checks the merge order
designer: C:\QAFactory\forge-repo\docs\tasks\specs\20261119-fv3-13-14-dry-exits-card.md
test: dry_exits.py::_selftest_cases ratchet rows - a subject with a live_only census row and live_only walk row(s) counts once; a leftover `walk/` raise for it is red naming the census row | expected from: F-P8 reading 2 (finish spec :576-579, :811); E-A1, E-A2
test: dry_exits.py::_selftest_cases ratchet rows - a walk-only subject counts its walk row; `route:x` walk row beside a `kinds_without_key/x` census row is NOT absorbed | expected from: this card E-A3, E-A6
test: dry_exits.py::_selftest_cases ratchet rows - census row `seed` + walk row live_only counts the walk row | expected from: this card E-A5

What to build:
1. One function `_counted_refs(census, walk) -> {count name: set of refs}` (refs in the `raised_by` row form: `<section>/<name>`,
   `walk/<rid>`). A walk row whose reach is `live_only` is LEFT OUT when `_subject_of(rid)[:2]` = `(section, name)` with `section` in
   `SECTIONS` and `census[section][name]["reach"] == "live_only"`. Everything else is as today.
2. `_count_reach` = the sizes of those sets (keys `live_only`, `after`, `unwalked`); `_raised` takes its live_only/after/unwalked refs from
   the same function (the hook_layer refs unchanged). Invariant: `counts[k] == len(refs[k])` for every k, by construction.
3. A `raised_by` entry naming a left-out walk row is stale; its problem line names the counting row: `... its row 'walk/<rid>' is counted on
   its census row '<section>/<name>' (one count per subject, FV3-14); drop the entry`.
4. Rebase in the SAME commit: drop the 27 `live_only | walk/...` entries of M3 (gates 15, s0 8, s1-s4 4); keep `walk/gate_A/words:questions-deferred`.
   Bases stay 0. If `--check` disagrees with M3, the measured `--check` list wins and the report says so.

Edges A
| # | Edge | Behaviour | Invariant |
|---|---|---|---|
| E-A1 | census live_only + one walk live_only, same subject | 1 count, on the census row; the walk entry is stale (item 3) | one subject, one entry: AR-20 reads no doubles |
| E-A2 | census live_only + two walk live_only variants | 1 count | a variant never adds a count to a counted subject |
| E-A3 | walk row only (a price key, or a route/kind whose census row is not live_only) | each such walk row counts, its own entry | a live_only row with no counting census row is never uncounted |
| E-A4 | census row only | 1 count, unchanged | unchanged rows keep their entries byte-identical |
| E-A5 | census `seed`/`story`/`unwalked` + walk live_only | the walk row counts | absorption needs a LIVE_ONLY census row, never any census row |
| E-A6 | same name, other section (`routes/s1_gap` vs `kinds_without_key/s1_gap`, real) | no cross-absorption | the subject is (section, name), never the name |
| E-A7 | census row in group G1, walk row in walk file G2 | absorbed (the census is glued); the stale entry is dropped from whichever file holds it | group boundaries never create a second count |
| E-A8 | TEMPORAL: a census row moves live_only -> seed later | its walk rows count again; `--check` red "above the base" until an entry names each | the ratchet never loses a row silently |
| E-A9 | walk row with an unknown subject (red in `_walk_problems`) or `route:/v` (empty rest -> section `key`) | not absorbed, counted | a malformed id errs toward counting |

## Card B - FV3-13: "told before work" in the dry main pass (A2 / N3a)

given: this card §0-§1; `docs/tasks/specs/20261113-p1-specs-amendment-owner-words.md` :198-259 (A2: mechanism, N3a, A2-E1..E6); `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\driver_runner.py::run_claude` (the `checks` row keys), `...\scripts\driver_core.py::Refusal.id_set`, `...\scripts\driver_journal.py::read_rows_counted`, `::run_record_names`, `...\scripts\stage_joints.py::read_rows`, `::row_for`, `::rows_for`, `::is_fallback`, `...\scripts\tests\dry_world.py::main_pass`, `::_ledger_lines`, `...\scripts\tests\known_red.py::reconcile`
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\dry_exits.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\dry_world.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\driver-exits\known_red.json
non-goals: no product code; no edit of `stage-joints.json` rows (a not-told id is labelled, its fix belongs to the mechanism's owner); no brief read (F-A2-1 (a)); exits-group worlds not walked (F4); `test_scenario_dry_1.py` unchanged under F2 (a)
handoff: report `C:\QAFactory\forge-repo\docs\tasks\specs\reports\20261119-fv3-13-report.md` (selftest tail, the told results and labels added) + commit hash
edges: the table "Edges B" of this card (E-B1..E-B11), every row with its invariant
DoD: `python -B ai-packages/qa-factory/scripts/tests/dry_exits.py --selftest` all cases pass, `--check` 0 discrepancies; `not run locally: test_scenario_dry_1.py, canon judges` - its CI run on the branch prints `NOTE dry-1/main/told-before-work: <n> refusals, <m> said, <k> not said (known_red)` with no `new red`/`unknown row` (F5)
siblings: axis 17 (one output form: told results are main-pass Results through `_ledger_lines`, no second printer); axis 34 / P31 (one road for every role and stage, F4); FV3-23/FV3-20 (other `main/*` labels in the same ledger)
designer: C:\QAFactory\forge-repo\docs\tasks\specs\20261119-fv3-13-14-dry-exits-card.md
test: dry_exits.py::_selftest_cases told rows over a tmp task root + a COPY of a rows file - id told for (role, stage) -> green; row absent for (role, stage) -> red; row named for another role -> red | expected from: A2 N3a (1)-(2), F-A2-3
test: dry_exits.py::_selftest_cases told rows - `checks: ["unknown"]` / `<stem>:unlabelled` -> red `.../unknown`; rework resume with no `checks` -> red `.../ids-not-recorded`; a non-rework resume with no `checks` -> no result, counted in the NOTE | expected from: A2-E2, A2-E4, this card E-B3..E-B5
test: dry_exits.py::_selftest_cases told rows - unreadable rows file / run record / a broken journal line -> red `main/told/carrier` naming the path | expected from: A2-E3, this card E-B8
test: test_scenario_dry_1.py --part main (canon judges, not run locally) - told results reconciled with `known_red.json` | expected from: A2 N3a DoD

What to build (under F1 (a), F2 (a)):
1. `dry_exits.told_before_work(task_root, *, rows_data=None, run_record=None) -> (results: {name: bool}, details: {name: str}, summary: str)`.
   Source: `driver_journal.read_rows_counted(<task_root>/state/driver-runs.jsonl)`. A REFUSAL row = `resumed is True` AND (`"checks" in row`
   OR `resume_kind` in `run_record_names("rework_kinds")`). Ids: list -> `Refusal.id_set(list)`; str -> `id_set([str])`; else `("unknown",)`.
2. Per (role, stage, id): fallback id (`stage_joints.is_fallback`) -> red `main/told/<role>@<stage>/unknown`; else
   `row, _ = row_for(id, data)`; green iff `row is not None and row in rows_for(role, [stage], None, data=data)` (the page's own call).
   Result name `main/told/<role>@<stage>/<id>`; detail names every dispatch that drew it, the role, the stage, the id.
3. `dry_world.main_pass`: after `results.update(gates)` and BEFORE `_ledger_lines`, `results.update(told results)` and append the details/summary
   through `line(...)` - the told results ride the one reconcile road with `main/S<n>` rows; nothing is printed elsewhere.
4. Labels: each red told result the branch's CI run shows gets a `known_red.json` row `main/told/...` with node = the mechanism finding the Lead
   names (F5) and `pins.known_red` raised in the same commit (AR-20, named in the report).

Edges B
| # | Edge | Behaviour | Invariant |
|---|---|---|---|
| E-B1 | id told for (role, stage): exact row or `<stem>:*` row, and `rows_for(role,[stage],None)` returns it | green | "said" = on the role's page exactly as `contract_slices` renders it, no wider claim |
| E-B2 | row exists but not for this role / stage / capability (`when: shell` on a no-shell role) | red | a row told to someone else is not told to this role (F-A2-3) |
| E-B3 | `checks: ["unknown"]`, `<stem>:unlabelled`, `checks: []`, non-list `checks` | red `.../unknown` | an unknown id never passes (A2-E2, AR-28) |
| E-B4 | rework resume (`resume_kind` in `rework_kinds`) with no `checks` key | red `main/told/<role>@<stage>/ids-not-recorded` (W0 landed: an absent key now means a caller lost the ids) | no refusal escapes by carrying no ids (A2-E4 post-N0) |
| E-B5 | resume not in `rework_kinds` (`person_answer`, `service_cut`, `stand_answers`, `unclassified`) with no `checks` | no result; counted `<s> resumes not refusals` in the summary | a non-refusal is never judged; the count keeps it visible |
| E-B6 | one refusal, several ids | one result per id | no id is lost (A2-E5) |
| E-B7 | row with empty/absent `role` or `stage` | red `main/told/?@?/<id>` "role or stage unknown for <dispatch>"; `rows_for` not called | the reader is never called with an invented value (A2-E6 analogue, F1) |
| E-B8 | rows file unreadable (`read_rows` -> None), `rework_kinds` unreadable (`()` + note), journal bad lines > 0, journal absent | red `main/told/carrier` with path and reason; no other told result | an unreadable source is red, never "nothing to check" (A2-E3) |
| E-B9 | 0 refusal rows in a readable journal | no told result; summary `0 refusals` | a zero is a count line, never a green "said" line |
| E-B10 | `row_for` -> "two rows" | judged on the first; detail says "two rows" (K5 is `stage_joints --check`'s red) | one judge per fact; the duplicate stays its owner's red |
| E-B11 | TEMPORAL: a labelled told result stops occurring / turns green | `reconcile` red `unknown row` / `stale`; the label is removed in that commit | a label never outlives its red |

Direction of error (rule 1, reused function in a gate role): `rows_for(..., dispatch=None)` lets every dispatch-group `when` token hold
(`stage_joints.py:536-538`, "toward more text") - it errs toward "said". Kept on purpose: the page is rendered with the same `None`, so "said" is
literal for the page. Adversarial inputs that must stay red: a capability-gated row on the wrong capability (E-B2), a `*` producer row for
`conductor` (`rows_for` excludes it), a row of another stage, an id with no row at all, a fallback id.

## Readers of touched files (rule 7)
The Lead did not attach a `tools/owns_readers.py` block: run `python -B tools/owns_readers.py --paths <owns of A and B> --names
_count_reach,_raised,told_before_work,main_pass --readers` before dispatch. Designer hand grep (`Grep "driver-exits"` *.py over the repo:
3 main-tree files `dry_exits.py`, `dry_world.py`, `test_scenario_dry_1.py`; worktree copies ignored; `Grep "_count_reach|told_before_work|_print_told"` in `tools/`: 0, control = same pattern in `ai-packages/` -> 2):
- `dry_exits.py::_ratchets` (calls both) - changes in A. `check()` NOTE text count 98 -> 71 - changes in A.
- `test_scenario_dry_1.py::census` prints `report.notes` - unchanged (text only differs in the number).
- `driver-exits/*.json` read by `dry_exits.load` (census, `test_scenario_dry_1.exits_part`, `group_unwalked`) - only `raised_by` changes in A; `group_unwalked` does not read `raised_by` (`dry_exits.py:1697`, not re-read in full: `estimate`).
- `dry_world.main_pass` read by `test_scenario_dry_1.main` - result list grows in B; the loop prints every Result already - unchanged.
- `known_red.json` read by `dry_world._ledger_lines`, `dry_exits._ledgers`/`_ledger_orphans(shared=True)` (accepts `main/` ids) - changes in B.

## Forks (Lead decides)
- F1 Which reader is "told". (a) `stage_joints.row_for` + `rows_for(role,[stage],None)` - the reader that landed, the page's own call; A2's
  `brief_pack.requirement_rows(role, stage, dispatch_kind)` does not exist (M5), so A2-E6 becomes E-B7. (b) write `requirement_rows` first as a
  new node. Recommend (a): one road with the page (P31, AR-13); (b) builds a second reader of the same file.
- F2 Where the told walk runs. (a) inside `dry_world.main_pass` before `_ledger_lines` (owns += `dry_world.py`; no `_print_told`; the batch row's
  `test_scenario_dry_1.py` owns dropped). (b) a callback parameter of `main_pass` carrying `_print_told`. Recommend (a): the task root is deleted
  when `main_pass` returns (M6); (a) uses the existing Result + ledger road, (b) adds a second printer and a hook.
- F3 Should `after:` get the same one-per-subject rule? (a) live_only only (the Lead's 17.11 decision names live_only; 0 `after:` rows today, M2).
  (b) every walk-carried count. Recommend (a), with a note: the first paired `after:` rows reopen it.
- F4 Exits-group worlds (the walker's per-row runs) also produce refusals and are not walked (P31 residual). (a) a named node FV3-13b:
  owns `dry_world.walk_exits` + `known_red/<group>.json`, test = the same selftest rows + the group run. (b) cover them in this card.
  Recommend (a): group labels follow `judge_group`, a different reconcile road that needs its own design; cost of (b) = +1 owns file and per-group labels.
- F5 Labels before merge. The told reds are unknown until the main pass runs (canon class, M7). (a) push the branch, read CI's main-pass
  output, add the `known_red.json` rows, re-push - merge only on a CI run with no `new red`; label node = a finding the Lead files for the
  mechanism's owner. (b) `manifest-skip: dod-run` and one local main pass (221.6 s). Recommend (a). Whether a branch push runs the dry story on CI: `estimate`, the Lead checks the workflow.
- F6 E-B4 severity. (a) red (W0 landed, M4). (b) NOTE as A2 wrote it for the pre-N0 world. Recommend (a); A2's invariant "not PASS" holds both ways.

## Small choices closed by the designer
- Result key `<role>@<stage>/<id>`, not per dispatch: the reader's answer depends on exactly (role, stage, id); dispatch ids go into the detail.
- Ids normalised by `Refusal.id_set` (the runner's own normal form); a bare string is wrapped first (`id_set("ab")` would split it).
- Card A keeps counting in one helper used by both `_count_reach` and `_raised` (no second definition of "counted").
- Builder report paths under `docs/tasks/specs/reports/`.

## Reading trail
Read: batch rows FV3-3..FV3-26 (`batch-3-live-run-fvf.md:20-55`); finish spec :560-589, :800-819; amendment :190-270; n4g-s0 report :1-30;
`dry_exits.py` :159-330, :630-870, :1027-1040, :2026-2160, CLI :12-13/:3166-3184; `driver_core.py` :120-164; `driver_runner.py` :840-899,
:985-1000; `driver_journal.py` :360-489; `stage_joints.py` :284-290, :438-622; `known_red.py` :53-153; `dry_world.py` :961-991, :1029-1069,
close :278-282; `test_scenario_dry_1.py` :1-156; `architecture.md` :33-60, :150-197, :249-262; `docs/TESTING.md` :75-114; `slow_tests.json`.
Grep: `"live_only \| "` over `driver-exits` (98 entries listed); `"reach": "live_only"` (99) / `"reach": "after:` (0) over `fixtures`;
`"ratchet"` -A8 (bases); `requirement_rows` -i (0, control `digest_template_lines` -i -> 12); `rows_for\(` (readers); `resume_kinds` in run-record.json.
Not read: `.claude/agents/designer.md` beyond the dispatch text; `references/stage-joints.json` rows (no row-level claim is made).
