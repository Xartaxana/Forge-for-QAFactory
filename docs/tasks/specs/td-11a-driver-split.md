# TD-11a — the move tool, the shared-registry protocol, phases 0-1 of `story_run.py` (DRAFT, designer)

Status: DRAFT for Lead acceptance. Intent: `docs/tasks/specs/td-11-lead-brief.md` (owner's words 11.11.2026, Lead decisions).
Paths below are relative to `ai-packages/qa-factory/` (PKG) unless they start with `tools/`, `docs/`, `plans/`.
Absolute PKG = `C:\QAFactory\forge-repo\ai-packages\qa-factory`. Measured on `main` a9bd758 (the working tree of 11.11).
Counting carrier for every number: the Grep tool (ripgrep) over the named file, pattern quoted in §9-A.

## 1. Goal, invariants, rules

Goal: `scripts/story_run.py` (22 171 lines, one `class Driver(DriverChains)` at :1081, `main` at :22092) is cut into the
home modules its layer map already names (`scripts/tests/fixtures/driver-layers.json`, 1023 `names` rows, map lines 6-1028),
by a COMMITTED script that is re-runnable on a fresh `main` and is the same tool spec B uses for `controller.py` and the
first-wave files (P31). No behaviour changes; `story_run.py` stays the entry file and a facade.

Already out of `story_run.py`: `driver_chains.py` (33 rows) and `driver_timing.py` (25 rows); `driver_journal.py` is
`not_driver` (map :4). Rows still to move: 1023 - 33 - 25 - 2 (`Driver`, `main`, home `story_run`) = **963**.

| Invariant | How this spec keeps it | Change check written into a DoD |
|---|---|---|
| AR-1 closed variety is data | the tool reads homes, layers and carrier key forms from DATA (the map, `tools/source-split-carriers.json`); no module or file name is written in the tool's code | T-1 DoD: `grep -n "story_run\|driver_" tools/source_split.py` prints only docstring/help lines |
| AR-13 one reader of a fact | ONE reader of "the driver source set" for tests: `harness.driver_sources()`; `test_driver_layers.read_modules` calls it; patch targets go through one helper | P0-A DoD; F6 names the remaining second census reader (the tool) |
| AR-14 one writer | the tool is the only writer of the new modules and of the facade; each carrier row has exactly one rewriter (§3) | §3 column "who" |
| AR-15 one survivor | form scans (one thread site, one appender, words site) keep reading ONE set, now via `harness.driver_text()` | P0-C DoD |
| AR-19 stage twins together | the cut moves twins (S5/S7 repair loops, S6/S7 consumer helpers) without editing them; SIBLING_MAP rows 121-128 rewritten in the cut PR | P1-2 DoD prose sweep |
| AR-20 ratchets only shrink | `exceptions` shrink 14 -> 9 (F2); judgment census, lint and dup baselines are RELOCATED, totals equal before/after (the tool prints both); a raise is a refusal | P1-2 DoD: tool line `ratchets: lint N=N dup N=N census N=N` |
| AR-22 producer and readers in one commit | every carrier keyed by file/function is rewritten IN the cut commit (§3); runtime readers (block-names -> `waiver.load_block_names`) included | P1-2 DoD runs each §3 verification |
| AR-29 code judges data | every check the tool or a test adds judges data only (below) | critic question 11 |
| FR-30 English | everything the tool writes is copied source plus ASCII generated text | tool refuses a non-ASCII byte in generated text (§6) |
| FR-31 no load-only failures | the tool's proof is deterministic (sha256 of segments, AST sets) | - |
| FR-32 root cause, test, green | phase 0 removes the move-fragile forms BEFORE the move | P0 DoDs |
| FR-37 path in text = path in code | prose naming `scripts/story_run.py` as the LOCATION of a moved name is rewritten; `story_run.<name>` prose stays true via the facade | P1-2 prose sweep command |
| FR-54 / P12 siblings by the map | carriers enumerated in §3 incl. ones the brief missed | §3 |
| P27 / P31 | the tool is generic; spec B cites §2/§3 and adds no second mover | §2 "generic" |

Checks added or altered (owner served; judgment-census class — all are DATA checks, class `shape`):

| Check | Owner | Class |
|---|---|---|
| tool refusals R1-R9 (§2.5) | data (code) | shape (keys, joins, presence) |
| tool proofs P1-P7 (§2.6) | data | shape |
| `test_driver_layers` Scan accepts `Driver<Suffix>.X` | data | shape |
| `test_driver_layers` L8 needle = every driver-set file name | data | shape |
| `test_driver_layers` L11 (new): a test assigns/patches an attribute of the `story_run` module | data | shape |
None of them reads a role's or a person's words; none is added to `scripts/` runtime. No judgment-census row is added
(the census covers package `scripts/`; `tests/` and `tools/` checks are outside it — stated, not verified, §9).

## 2. The tool — `tools/source_split.py`

Home: `tools/` (a dev mover, never shipped; precedent `tools/piles_split.py`). Data: `tools/source-split-carriers.json`.

### 2.1 Door
```
python -B tools/source_split.py --map <map.json> --source <PKG-relative .py> [--class <Name>] [--homes a,b] (--dry-run | --apply) [--repo DIR] [--report FILE]
python -B tools/source_split.py --selftest
```
`--class` names the split class (absent: only module-level names move — spec B's function files). `--homes` limits the
move to whole homes (default: every home with rows). Exit: 0 done / nothing to do; 1 cannot run (bad args, unreadable
file, unparsable source); 2 refused (R1-R9) — NOTHING written. `--dry-run` writes nothing and prints the same report.

### 2.2 Input contract (the map)
Reads `names` (`{name, kind, home}`; `row`/`note` ignored), `layers` (rank = index of the group), `exceptions`
(`{from,to,kind}`), `not_driver`. Module of a home = `scripts/<home>.py`; mixin class = `CamelCase(home)` (`driver_s0` ->
`DriverS0`, `driver_stage_s5` -> `DriverStageS5`; `driver_chains` -> `DriverChains`, the existing class). Class members are
rows `<Class>.<member>`; everything else is a module-level row.

### 2.3 Finding a segment (AST + exact slices)
- Census: module-level `def`/`class`/`Assign`/`AnnAssign` targets, and members of `--class` (def, static/class method,
  class-level assignment) — the same rule as `test_driver_layers.definitions` (:84-111). Imports, nested functions and
  `if __name__` are not names.
- Segment of a name = from the first decorator line (or the statement line) to `end_lineno`, sliced from the source TEXT
  (not `ast.unparse`), plus the ATTACHED COMMENT BLOCK: the contiguous comment lines directly above at the same indent with
  no blank line between. A blank-separated comment and a section marker `# --- ... ---` are SECTION TEXT: copied once into
  each home module that receives the first member below it (orientation only; not part of the per-name proof).
- Class-body glue (non-census statements in the class body: `import runtime_paths as _rp` :7195, `del _rp` :7197,
  `from gate_preflight import FINDING_ID_PATTERN as _FINDING_ID_PATTERN` :21049): attached to the census member that uses the
  name the glue binds (import) or that bound the name it deletes (`del`); `import/assign/del` sandwiches travel as one unit.
- Class-level descriptors (`boundary = ThreadSlot(...)` :1086, `last_dispatch = ThreadSlot(...)` :1087) are classconst rows
  (map :936-937) and move as ordinary class attributes; a data descriptor on a base class acts through the MRO, so behaviour
  is unchanged (reasoned, proven by P3/P5).
- Nested functions and lambdas stay inside their parent's segment.
- Bytes are kept as read: the file is read in binary, decoded UTF-8 strict; the newline sequence of the source is detected
  and reused; a file with mixed newlines is refused (R9).

### 2.4 Writing a home module
Module = docstring (generated, ASCII: `"""<file> - <Class> members homed here by <map path> (TD-11 cut by tools/source_split.py);
no behaviour of its own."""`) + imports + section texts + segments in ORIGINAL SOURCE ORDER + (for class members) one
`class <Class>:` with no base and no docstring of its own beyond the generated one-liner.

Imports of a home H — free names of all segments moved to H (loads not bound locally; INCLUDING decorators, default values,
annotations — evaluated at def time, `story_run.py` has no `from __future__ import annotations`):
1. builtin -> nothing;
2. bound by a top-level import of the source (story_run :53-84) -> that import statement copied, reduced to the used aliases,
   in the source's order;
3. a census name with home G: G == H nothing; rank(G) <= rank(H) -> `from G import <name>` (same rank allowed, see R6);
   rank(G) > rank(H) -> R4;
4. `Driver` -> rewrite W1 below, else R4; anything else -> R5 (unresolved free name).
Lazy imports inside bodies (about 520, brief) travel verbatim inside their segment and are not touched. `HERE` lives in
`driver_core` (map :834) with `sys.path.insert(0, str(HERE))` right after it; other homes `from driver_core import HERE`
(defining HERE twice fails L2 — the map note "each module carries its own" is superseded; stated as a small choice §8b).

Rewrites (the ONLY text the tool changes inside copied code; each printed in the report):
- W1 `Driver.<m>` inside a member -> `<HomeClass of m>.<m>` (+ import if another module). Today 3 sites, all in
  staticmethods (no `self`): :2935 `Driver.role_words` (in `stuck_facts`, both dialog), :10778 `Driver.stage_repair_owed`
  (in `s4_repair_owed`, both the same stage module), :11549 `Driver.CUT` (in `probe_reason` (s0) -> `DriverCore.CUT`, downward).
- W2 the facade's path preamble (below).

The facade `story_run.py` after the cut: the original module docstring (`main` uses `__doc__`, :22101); the original import
block :53-84 UNCHANGED except `HERE = ...` replaced by `sys.path.insert(0, str(Path(__file__).resolve().parent))` (W2);
re-exports `from <home> import <every module-level name moved there>  # noqa: E402,F401 (TD-11 facade)` (F5); mixin imports;
`class Driver(<bases>):` with the original class docstring/comments that are not member-attached; `main` and the
`__main__` block unchanged. Bases: homes ordered by rank DESCENDING, within a rank by the `layers` order, `DriverChains`
last — `class Driver(DriverMachine, DriverGates, DriverStagePlan, ..., DriverS0, DriverSources, DriverDispatch,
DriverConductor, DriverDialog, DriverRunner, DriverCore, DriverChains)`. Because every name is defined once (L2), the MRO
order decides nothing but is fixed for determinism; only `DriverCore` defines `__init__`.

### 2.5 Refusals (exit 2, nothing written; each line: what, expected, door)
| # | Condition | Door |
|---|---|---|
| R1 | a census name with no map row | add the row (home is a judgment: the node author / Lead), re-run |
| R2 | a map row whose name the source no longer defines | delete or rename the row |
| R3 | a name with two rows, or defined twice | one row / one definition |
| R4 | a free name resolving to a HIGHER home (incl. a name-kind `exceptions` edge: an import cannot carry it, L6 refuses even lazy upward imports, `test_driver_layers.py:557`) | rehome the name down (F2) or remove the edge |
| R5 | a free name that resolves to nothing | name it in the report; fix the source or the map |
| R6 | a same-rank import cycle between two homes | rehome one name |
| R7 | class-scope split: a class-body expression (assign RHS, decorator, default value, glue) uses a class-body name homed elsewhere (e.g. `PASTE_OPTION` :7313 uses `PASTE_SHAPE` :7295) | give both one home |
| R8 | a target module exists and holds a census name not homed there, or misses one homed there | the module is foreign or half-written: restore it, re-run |
| R9 | mixed newlines, non-UTF-8 source, or a non-ASCII byte in GENERATED text | fix the source / the generator |

### 2.6 Its own proof (printed; the tool's output is the witness)
| # | Proof | Fails -> |
|---|---|---|
| P1 | per name: sha256 of the segment before == after (W1 applied to "before"); line `segments: 963/963 equal` | exit 2 |
| P2 | census set before == union after, each name once | exit 2 |
| P3 | subprocess `python -B -c` import of the facade before (a temp copy of the pre-cut tree) and after: `dir(story_run)` before is a SUBSET of after; `dir(story_run.Driver)` before == after | exit 2 |
| P4 | `compile(text, path, "exec")` of every written file (no bytecode written, builder-rules 6) | exit 2 |
| P5 | `analyse()` of `test_driver_layers` on the result tree: L1-L10 empty | exit 2 |
| P6 | carrier pass: every carrier row rewritten resolves (§3 key forms), none left pointing at a name no longer in the old file | exit 2 |
| P7 | ratchet totals: lint finding count by class, dup group count, judgment-census row count — before == after (relocated, not grown) | exit 2 |
Report head: source sha256, map sha256, per home `N names (funcs/methods/consts) ~L lines, imports k`, refusals, rewrites W1/W2,
carrier rewrites (file, old key -> new key), facade-read count (`story_run.<x>` reads in `scripts/tests`, for F5).

### 2.7 `--selftest`
Builds temp trees (like `test_driver_layers.bad_fixtures`, :795) and asserts each R1-R9 is reported BY NAME and a clean
fixture passes P1-P5. This is the tool's test (F1: no new test file).

## 3. The shared-registry protocol (specs B and C cite this)

ONE RULE: a single-copy registry keyed by a file name, `file:function` or a line number is written ONLY in the CUT COMMIT of
the file being split — by the tool's carrier pass or by the hand list of the same commit — and by nobody in parallel. A
node of B/C that needs a row changed for another reason writes it under "Needed from integration". Cuts are SERIAL on
`main` (one cut commit at a time); each cut re-runs the tool on the fresh `main`. Line-number anchors are abolished: an
anchor is `Driver.<member>` / `<function>` with no line, and no file where the map resolves it.

Lead note at acceptance (11.11.2026), joining this rule with spec C §4.3 (R-A1, R-A2): for a batch of TEST-file splits the
"cut commit" is the integrator's ONE closing commit of the batch — split nodes run in parallel on disjoint test files, commit
no single-copy registry and hand their rows in the report; the closing commit and the node merges reach `main` in one push.
A SOURCE cut (this spec, spec B) is one commit per file, serial on `main`. Either way a registry has one writer at a time.
`global`/`nonlocal` in `story_run.py` = 0 is now verified with a same-pattern positive control (55 hits in 40 other files of `scripts/`).

Carrier key forms in `tools/source-split-carriers.json` (data, AR-1): `json-file-function` (`{file, function}` objects),
`guard` (`<file>.py::<function>`), `reader` (`<module>:<Class>.<method>`), `py-tuple` (`('<file>', '<Class>.<m>', ...)` lines
of a dict literal, re-sorted after rewrite).

| # | Carrier (verified) | Key kind | Who rewrites | When | Verification (from PKG) |
|---|---|---|---|---|---|
| 1 | `references/gate-registry.json` :15,:446,:466,:509 (`build_outcome`, `stand_login_gate`, `stand_check`, `hand_to_conductor`) | json-file-function | tool | cut commit | `python -B scripts/tests/test_gate_registry.py` |
| 2 | `references/null-outcomes.json` :20,:24,:36,:40 (`stage_S5` x2, `stage_S6`, `stage_S7`), resolved by `null_outcomes.unresolved` (:241) | guard | tool | cut | `python -B scripts/tests/test_null_outcomes.py` |
| 3 | `references/block-names.json` :38-73, 7 readers `story_run:Driver.<m>` — RUNTIME reader `waiver._name_row` (:532-553) checks `class <Class>` + `def <m>` in that file | reader | tool (`driver_x:DriverX.<m>`) | cut (a stale row is a runtime BlockNamesError) | `python -B -c "import sys; sys.path.insert(0, 'scripts'); import waiver; print(len(waiver.load_block_names()))"` |
| 4 | `scripts/audit_factory.py` `NO_MOVE_BASELINE` :1628-1675 (47 rows keyed `('story_run.py', 'Driver.<m>', ...)`; keys are `mod.name`, :2277) | py-tuple | tool | cut | `python -B scripts/tests/test_audit_rules.py`; `python -B scripts/tests/test_no_move_seam.py` |
| 5 | `scripts/tests/fixtures/judgment-census.json` 20 rows `"file": "story_run.py"` (+1 unrelated `refuse_untyped_story_run` :701) | json-file-function | tool | cut | `python -B scripts/tests/test_judgment_census.py` |
| 6 | `scripts/tests/test-layers.json` `covers` (59 lines `"story_run.py"`) | append | tool: every keep row whose covers holds `story_run.py` gets every new module (F7); no entry removed (td-15 :267-268) | cut | `python -B scripts/tests/scenario_walk.py --witness-for scripts/driver_s0.py` prints keep rows, not "no scenario or keep row covers" |
| 7 | `scripts/tests/fixtures/driver-layers.json` homes/layers/owners/exceptions | hand | P1-1 (before the cut); `source_readers`/`source_mentions` by P0-C | P1-1 / P0-C commit | `python -B scripts/tests/test_driver_layers.py` |
| 8 | `references/artifact-writers.json` :195 `writer: story_run.py` for `state/driver-timings.jsonl` (writer = module of `Driver.timing_write`) | hand | P1-2 builder | cut | `python -B scripts/tests/test_artifact_writers.py` |
| 9 | `scripts/tests/fixtures/env-facts-baseline.json` :14,:16,:32,:33,:36,:51,:54 (`story_run.py :NNNN` in `site` prose) | line anchor | hand: anchor -> `Driver.<m>`, file dropped | cut | `python -B scripts/tests/test_state_portability.py` |
| 10 | `design/architecture.md` :191 (`:5023`, `:4967`), :249 (`story_run.py:1128`); `design/factory-rules-debt.md` :84, :86 | line anchor | hand | cut | `python -B tools/architecture_index.py --check` (repo root) |
| 11 | `scripts/install_smoke.py` :144 comment `story_run.py:613-616` | line anchor | INTEGRATOR (integrator-only file, builder-rules 1) | cut PR | none (comment) |
| 12 | prose naming `scripts/story_run.py` as the location of a moved name: `references/collect-loops.json` :3, `design/driver.md` :233, `design/state-exits.md` :26, :139, `docs/SIBLING_MAP.md` :121-128 | prose | hand: "the driver set (`scripts/story_run.py`, `scripts/driver_*.py`)" or `Driver.<m>` | cut PR | sweep command §5.4 |
| 13 | prose `story_run.<member>` / `story_run.Driver.<m>` (`field-producers.json` :62, `place-answers.json` :36, `question-vocabulary.json` :92, `human-questions.md` :146, `design/state-exits.md` :53, :57) | prose | none — stays true through the facade | - | - |
| 14 | commands `story_run.py ...` (`INSTALL.md` :27, `docs/RUNBOOK.md` :277, :320, `experiments/measurers/prepare_copy.py` :203, `references/driver-infra.json` :3, `conductor.md` :3) | entry file | none — the entry stays | - | - |
| 15 | `tools/lint-baseline.json` (identity path+class+args, `tools/lint_ratchet.py` :51) | path | integrator: `python tools/lint_ratchet.py --update` in the cut commit; P7 proves equal totals | cut | `python tools/lint_ratchet.py --check` |
| 16 | `tools/dup-baseline.json` (GONE rows green, new-path groups red until update, `tools/dup_ratchet.py` :41-46) | fingerprint+scope | integrator: `python tools/dup_ratchet.py --update` in the cut commit | cut | `python tools/dup_ratchet.py --check` |
| 17 | `tools/crap_report.py` :105 `GOLDEN_FILE`, `scripts/tests/driver_golden.py` :526 `story_run_sha256` | file | none (golden data absent, `test_driver_golden.py` quarantined); debt line: the golden covers `story_run.py` lines only | - | - |
| 18 | `tools/piles.py` owns `path (f1, f2)` (:509-510, :555) | path+functions | F4: P1-4 node | after cut | `python -m pytest tools/test_piles*.py -q -k owns` |
| 19 | `PROJECT.md` «Командная работа» п. 3 hot-file list | prose | Lead | after cut | - |
| 20 | `references/release-fingerprint.json` :372 | sha | release step regenerates | release | - |
| 21 | `experiments/measurers/conductor_families.py` (`story_run.KNOWN_REFUSALS`) | module attr | none — facade (F5) | - | - |
| 22 | `audit_factory.py` :1679 `DRIVER_ENTRY` + `driver_*.py` glob :2342; `test_audit_rules.py` :1043-1099 planted copies | set | none — already set-aware | - | - |
Brief analogs not found as carriers: `slow_tests.json`, `selftest.py` `TEST_TIMEOUTS`/`CONTRACT_TESTS`, `stage-joints.json`,
`forge-check.yml` are keyed by TEST file names, which spec A does not move.

## 4. Phase 0 — move-proof tests, BEFORE the cut

Search command for module-attribute patches (both forms; run from PKG, Grep/rg syntax):
```
rg -n "\b(story_run|SR|sr)\.[A-Za-z_]\w*\s*=[^=]" scripts/tests --glob "*.py"
rg -n "(setattr\(|patch(\.object)?\(|monkeypatch\.setattr\()\s*[\"']?(story_run|SR|sr)\b[.,\"']" scripts/tests --glob "*.py"
rg -n "^\s*\w+\s*=\s*[^=\n]*\bstory_run\s*$|import story_run as \w+|__import__\(\"story_run\"\)\.\w+\s*=[^=]" scripts/tests --glob "*.py"
```
Result on a9bd758 (module attribute, breaks after the cut): KEEP — `test_silent_passes.py` :207,:227,:256,:278,:327
(`_now`), :842,:858 (`json_record`); `test_story_run_words.py` :286 (`open`); `test_driver_stop_record.py` :189-259
(`_append_jsonl`, 8 lines; the brief missed it); `test_walk_lanes_parallel.py` :52 (at import), :1235 (`lane_keys`);
`test_walk_supply.py` :842 (`lane_keys`); `test_walk_account.py` :280 (`lane_keys`), :314 (`WALK_ACCOUNT_TRIGGERS`).
QUARANTINE (not edited): `test_story_run_wait.py` :93,:110 (`time`); `test_refuse_case.py` :158,:166 (`_write_json`).
NOT breaking: `setattr(story_run.Driver, ...)` (`test_s7_investigation_replay.py` :124) and `patch.object(story_run.waiver,
...)` — they patch the assembled class / the shared module object, which the cut keeps.

Kept files that read the driver SOURCE (map `source_readers` :1225-1260, filtered by `test-layers.json` keep): the brief's 12
plus `test_audit_rules.py` (already set-aware: no change), `test_controller_gate_decision.py`, `test_s7_null_outcome.py`,
`test_ticket_adapter.py` = 15 to edit. Rule (F3, docs/TESTING.md :94, builder-rules 7d): a check whose subject is ONE named
member's text is a source pin -> DELETED (report line: file, function, "source pin"); a check over EVERY site of a form in
the driver ("one thread site", "no private appender", "one words site", "no agent-read names", "no U+FEFF", "one source of
MANUAL_BLOCK_MAX") is a form census -> reads `harness.driver_text()`.

| Node | File :: function (map row) | Change |
|---|---|---|
| P0-C | test_knowledge_notice :: test_gate_repair_calls_notice_after_kept_answer_branch | delete (pin of `Driver.gate_repair`) |
| P0-C | test_walk_lanes_parallel :: story_run_makes_no_new_thread_site | thread count over `driver_text()`: expected **2** (driver_chains.py:394 scheduler, story_run.py:1954 timing watcher — measured); `run_chains(items` checks deleted; + patch :52/:1235 via `set_driver_global` |
| P0-C | test_driver_stop_record :: story_run_has_no_private_appender | scan `driver_text()`; + patches :189-259 via `patch_driver_global` |
| P0-C | test_story_run_refusals :: refusal_cc9_every_close..., refusal_every_action_has_a_move | builder classifies by the rule (targets name members -> delete, unless the function iterates every site) |
| P0-C | test_conductor_doors :: c26_... | delete (prompt text of `Driver.conductor`) |
| P0-C | test_gate_brief_and_retro :: test_t409_h3_... | delete (pin of one member) |
| P0-C | test_story_run_s0 :: k5 (form census, architecture.md :86 names it) | `driver_text()`; k6, s0_owners_of_a_failed_read, s0_unread_road_units: delete |
| P0-C | test_story_run_s6 :: d1_texts (every string constant), t329 (one source) | `driver_text()` |
| P0-C | test_story_run_stand_identity :: k37 | delete |
| P0-C | test_story_run_words :: words_no_other_site... (form census) | `driver_text()`; words_the_arrival_road...: delete; + patch :286 via `patch_driver_global("open", ...)` |
| P0-C | test_words_doors :: driver_inline_calls (sole AR-24 detector, architecture.md :249) | `driver_text()` |
| P0-C | test_window_record :: a_word_nothing_reads... (absence over the file) | `driver_text()` |
| P0-C | test_controller_gate_decision :: rn1_20_k_d2 | delete (shape of `Driver.accept_order`) |
| P0-C | test_s7_null_outcome :: one_definition_no_local_set_building | `driver_text()` |
| P0-C | test_ticket_adapter :: part_normalized_input | `driver_text()` |
| P0-B | test_silent_passes, test_walk_supply, test_walk_account | patches via `patch_driver_global` / `set_driver_global` |
P0-C also rewrites the map's `source_readers` rows to the new state (deleted rows go; harness's reader becomes one row).
Quarantined source readers (`test_refuse_case`, `test_collect_stall`, `test_story_run_delivery(_c)`, `test_s1_exit_impl_diff`,
`test_story_run_repair_limit`, `test_version_coherence`, `test_waiver_release`, `test_story_step_finish`,
`test_story_run_codex`) and quarantined patchers are NOT edited; when `quarantine-watch` shows them red after the cut, the
Lead records the verdict "перенос TD-11" through `tools/test_quarantine.py judge` (no `land`: no product defect).

Phase-0 nodes:
- **P0-A** `harness.py`: `driver_sources(root=PLUGIN_ROOT)` -> `[(Path, text)]` of `scripts/story_run.py` + sorted
  `scripts/driver_*.py` minus the map's `not_driver`; `driver_text()` = the texts joined with `"\n"`;
  `patch_driver_global(name, value)` (context manager: sets `name` on `story_run` and on every imported module of the set,
  restores the old value or DELETES where absent — so `open` shadows the builtin only inside the block) and
  `set_driver_global(name, value)` (same, returns the restore callable; for import-time patches). `test_driver_layers.py`:
  `read_modules` calls `harness.driver_sources`; `Scan.visit_Attribute` (:166) accepts any `DRIVER_CLASS` name, not only
  `Driver`; L8 counts literals of EVERY driver-set file name, not only `story_run.py` (:579). Error direction of the patch
  helper: it may over-patch (a module that never reads the name gets it for the block — no effect); it must never
  under-patch a module that binds the name.
- **P0-B** ∥ **P0-C** after P0-A (disjoint files, table above).
- **P0-D** after B and C: `test_driver_layers.py` L11 — a `scripts/tests/*.py` file that assigns to `<story_run alias>.<name>`,
  or calls `setattr(<alias>, ...)` / `mock.patch.object(<alias>, ...)` / `monkeypatch.setattr(<alias>, ...)` on the MODULE
  (aliases: `import story_run as X`, `X = story_run`), is reported `file:line` with the door
  `harness.patch_driver_global`; attributes of `story_run.Driver` and of module objects reached through it are allowed.
  Quarantined files are skipped by L11 (they are not edited). Bad case in `bad_fixtures`.

## 5. Phase 1 — the cut by the map

### 5.1 Final module list (rank = `layers` index after P1-1)
Lines are ESTIMATES = names x 27 (class body :1081-22091 / 769 methods ≈ 27.3); the dry-run's `~L lines` is the measurement.

| Rank | Module (class) | Names | ~Lines (est.) | Content |
|---|---|---|---|---|
| 0 | driver_core (DriverCore) | 57 (+5 via F2) | 1 700 | constants, exceptions, `Person`, `Refusal`, readers, `__init__`, `HERE` |
| 0 | driver_chains | 33 | exists | unchanged |
| 1 | driver_runner (DriverRunner) | 57 | 1 500 | `py`, `launch`, words files, owed rows |
| 1 | driver_timing | 25 | exists | unchanged (not a mixin) |
| 2 | driver_dialog | 50 | 1 400 | questions, `closed_question`, `held_question` |
| 3 | driver_conductor | 56 | 1 500 | the conductor, `no_move` seam |
| 4 | driver_dispatch | 181 | 4 900 | `run_role`, `finish`, `handoff`, `resume_role` |
| 5 | driver_s0, driver_sources | 103, 36 | 2 800, 1 000 | S0 ticket; S1 sources |
| 6 | driver_stage_plan | 48 | 1 300 | map `row` 66, 67, 87: S2-S4, stage acceptor/critic route, `completion_for` |
| 6 | driver_stage_build | 21 | 600 | `row` 72 + `BUILD_*`, `build_*`, `take_build_answer`: stand and build |
| 6 | driver_stage_s5 | 27 | 700 | `row` 73 + `s5_*`, `S5_*`, `run_s5_windows`, `resolve_return_refusal`, `resume_with_filed_words`, `host_window_reason` |
| 6 | driver_stage_s6 | 70 | 1 900 | `row` 74, 75 (incl. `consumer_*`, `accepted_at`, `person_pass`) + `s6_*`, `S6_*`, `manual_lane_plan`, `run_manual_lane`, `run_s6_lanes`, `walk_*`, `file_passed_over` |
| 6 | driver_stage_s7 | 46 | 1 200 | `row` 76 |
| 6 | driver_stage_s8s9 | 18 | 500 | `row` 77, 80 + `S9_QUESTION` (row 7, used only at :17136) + `rebuild_report` (row 43) |
| 7 | driver_gates | 64 | 1 700 | gates, gate-entry repair |
| 8 | driver_machine | 129 | 3 500 | loop, `take_answer`, `KNOWN_REFUSALS`, `describe` |
| 9 | story_run | 2 | ~200 | facade, `Driver`, `main` |
Stage rows: 48+21+27+70+46+18 = 230 (map rows with `"home": "driver_stages"`: 230). Same-rank split keeps L5-L7: every
name keeps rank 6, so no edge changes direction (L5/L7 compare ranks only, `test_driver_layers.py` :524-527); same-rank
`self.` calls are legal. The 22 `attributes`/`state_keys` rows with `owner: driver_stages` get the stage module of their
first accessor in source order (equal rank: no L7 effect). `driver_stages` leaves `layers`; six modules take its place.

### 5.2 Names importable as `story_run.<name>` after the cut (F5)
Every name `dir(story_run)` held before (P3 proves it): all moved module-level names (re-exported) and all names of the import
block :53-84 (kept). The measured reads that make this necessary: `EXIT_*`, `KNOWN_REFUSALS` (also
`conductor_families.py`), `match_known`, `route_known`, `question_body_sha`, `finding_key`, `gate_refusal`,
`last_json_line`, `_answer_note`, `_read_json`, `main`, `Driver`, `Refusal`, `Person`, `Stop` (brief), plus found here:
`Priced`, `RelayCtx`, `CONDUCTOR_CALLS_PER_BOUNDARY`, `waiver`, `lane_keys`, `WALK_ACCOUNT_TRIGGERS`, `_append_jsonl`,
`_now`, `json_record`, `_write_json`. READING through the facade works; ASSIGNING to it does not reach the moved code
(phase 0 / L11).

### 5.3 Phase-1 nodes and commit order
1. **T-1** the tool + carriers file + `--selftest` (parallel with phase 0; disjoint files).
2. **P1-1** map edit (after P0 merged): stage split rows + `layers`; owners; F2 rehoming down: `UNTIL_PAST` -> driver_core,
   `HANDOFF_FORM` -> driver_runner, `WINDOW_ROUND_STAGES` -> driver_dispatch, `S1_GAP_RE`, `S1_REVIEW_RE` -> the home of
   `Driver.s1_person`; delete the 5 name-kind `exceptions` rows (shrink; `PINNED_EXCEPTIONS` untouched — a pinned row the map
   no longer holds is "simply gone", :38-40). Before the cut nothing else changes (rows homed in absent modules stay in
   story_run.py, L2 :355).
3. **P1-2** the cut: on a fresh `main` with T-1, P0-*, P1-1 merged: `--dry-run` (report attached), `--apply`, the hand rows of
   §3 (8-12), `lint_ratchet --update`, `dup_ratchet --update` — ONE commit `architecture: AR-13, AR-14, AR-20, AR-22 -- ...`.
   Rollback: `git revert <cut commit>` (one commit; P1-1 and phase 0 stay, they are valid without the cut).
4. **P1-3** (Lead, docs): `plans/builder-rules.md` 7c note (below), `PROJECT.md` п. 3 hot list (`story_run.py` leaves it;
   `driver_dispatch.py`, `driver_machine.py` enter if the Lead judges them hot).
5. **P1-4** (F4) `tools/piles.py`: an owns token `scripts/story_run.py (f1, f2)` resolves each function to its home module
   through the file maps (data); a bare facade path counts as every home module (over-inclusive = the safe direction).
Integration: the Lead's integrator merges T-1/P0 nodes; P1-2 is one builder in a worktree on a fresh `origin/main`, then the
integrator; no other node writes `scripts/story_run.py` or a `driver_*.py` between P1-1 and the merge of P1-2 (Lead holds
the window; a commit that lands anyway is handled by re-running, §6).

Local witness (builder-rules 7b-7d): the tool's report, `python -B scripts/tests/test_driver_layers.py`,
`python -B scripts/tests/test_story_run_words.py`, the §3 verification commands, and the files
`python -B scripts/tests/scenario_walk.py --witness-for <owns>` prints that run under ~1 min. Left to the CI canon: every
`test_story_run_*`, `SLOW_TESTS`, `selftest.py`, ratchets in `forge-check`, docker.

### 5.4 Prose sweep (P1-2) and the builder-rules note
Sweep: `rg -n "scripts/story_run\.py|story_run\.py[: ]+:?\d+" ai-packages/qa-factory docs/SIBLING_MAP.md` — every hit that
names the LOCATION of a moved name or a line is rewritten (§3 rows 9-12); commands and the entry stay.
Note for `plans/builder-rules.md` 7c (Lead): "After TD-11a a Driver member lives in `scripts/<home>.py`, `<home>` = the
`home` of its row in `scripts/tests/fixtures/driver-layers.json` (`rg -n '\"Driver.<m>\"' <map>`). A node naming
`story_run.py (f)` writes the home module of `f`. Never assign to `story_run.<name>` in a test — use
`harness.patch_driver_global`. A new driver name needs a map row before the commit (L1)."

## 6. Edge behaviours (behaviour + the invariant it protects)

| Edge | Behaviour | Invariant |
|---|---|---|
| name in story_run.py, absent from the map | R1, nothing written | no name lands in a module nobody chose (home is judgment) |
| map row whose name is gone | R2 | the map never claims code that does not exist |
| member defined twice | R3 | one name, one definition (L2), so MRO order can never pick between copies |
| method uses a module-level name of a HIGHER layer | R4; the 5 current cases are rehomed down by P1-1 (F2) | no upward import ever (L6); the exception list never grows |
| the 14 pinned exceptions | 9 call-kind stay (resolve through `self` at run time, no import); 5 name-kind leave via F2 | shrink-only (AR-20) |
| class attributes, descriptors | moved as class attributes; class-scope cross-use split -> R7; glue attached (§2.3) | class creation never meets a NameError; descriptor still found via MRO |
| nested functions, decorators | inside the parent segment; decorators and attached comments travel | per-name segment equality (P1) |
| module-attribute patch in a test — BEFORE the cut | `patch_driver_global` sets `story_run` (the only module) = old behaviour | a patch reaches every module that reads the name |
| — AFTER the cut | it sets every module of the set; a NEW direct assignment is L11 red | a test can never silently patch a dead copy |
| concurrent commit to story_run.py between dry-run and apply | `--apply` recomputes from the CURRENT tree; the report prints both source shas; changed segments move with their new text; a new name without a row -> R1, door: row, re-run; a deleted name -> R2 | the move is a function of the tree it is applied to, never of an old plan |
| re-run after a partial/failed apply | R8 if a target is half-written; a complete earlier cut -> "nothing to do", exit 0 | idempotence; a foreign module is never overwritten |
| Windows CRLF / encoding | source newline reused, mixed -> R9; UTF-8 strict in and out; `open(..., newline="")` | bytes of moved code unchanged (P1 on bytes) |
| empty home (a layer with zero names) | no module written, no base class; listed `0 names` in the report; `layers` keeps it only if the map does | no empty file, no unused import (lint) |
| FR-30 | generated text ASCII (R9 otherwise); copied text is the source's own (already `--lang` clean) | the package stays English |
| W1 rewrite target in a higher home | R4 | same as upward names |
| `__module__`/`__qualname__` change (`DriverX.m`) | accepted; only readers are the golden trace (`tests/driver_trace.py` :1071, quarantined) | no runtime reader depends on them (grep §9-A) |

## 7. Per-node manifests (ready for dispatch)

All nodes: given — this spec, `design/factory-rules.md` whole, `plans/builder-rules.md`, `docs/TESTING.md`, the map,
`scripts/tests/test_driver_layers.py`, `scripts/tests/harness.py`. Commands run from PKG in the worker's worktree unless
`tools/`. Parallel: T-1 ∥ P0-A; then P0-B ∥ P0-C; then P0-D; then P1-1; then P1-2; then P1-3 ∥ P1-4. Writing workers at
once: at most 2.

**T-1** owns: `C:\QAFactory\forge-repo\tools\source_split.py`, `C:\QAFactory\forge-repo\tools\source-split-carriers.json`
non-goals: no edit of the package; no apply on the real tree; no map edit.
DoD: `python -B tools/source_split.py --selftest` (R1-R9 by name, clean fixture P1-P5) and `python -B tools/source_split.py --map ai-packages/qa-factory/scripts/tests/fixtures/driver-layers.json --source scripts/story_run.py --class Driver --dry-run` (report; expected today: R4 on the 5 name-kind edges until P1-1 — that refusal IS the witness).
witness scope: the two commands only.

**P0-A** owns: `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\harness.py`,
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_driver_layers.py`,
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\driver-layers.json`
non-goals: no test file other than these; no driver code.
DoD: `python -B scripts/tests/test_driver_layers.py` green incl. new bad cases (Scan `DriverX.Y`; L8 on a `driver_x.py` literal).
witness scope: `python -B scripts/tests/scenario_walk.py --witness-for scripts/tests/harness.py scripts/tests/test_driver_layers.py` — run only the files under ~1 min; `tests/harness.py` covers many rows: report the list, run `test_driver_layers.py` and `test_story_run_words.py`.

**P0-B** owns: `...\scripts\tests\test_silent_passes.py`, `...\test_walk_supply.py`, `...\test_walk_account.py` (absolute under PKG)
non-goals: no other test; no harness edit. DoD: each owned file green: `python -B scripts/tests/test_silent_passes.py` (and the two others). witness scope: the three files.

**P0-C** owns: the 15 files of §4 table (absolute under `...\scripts\tests\`) + `...\scripts\tests\fixtures\driver-layers.json`
non-goals: quarantined files; no new assertion beyond porting. DoD: each owned file green + `python -B scripts/tests/test_driver_layers.py` (L8 rows match). witness scope: owned files under ~1 min; `test_story_run_s0/s6/refusals/stand_identity` are SLOW_TESTS -> CI (named in the report).

**P0-D** owns: `...\scripts\tests\test_driver_layers.py`. DoD: `python -B scripts/tests/test_driver_layers.py` green, L11 bad case reported by name. witness scope: that file.

**P1-1** owns: `...\scripts\tests\fixtures\driver-layers.json`. non-goals: no code. DoD: `python -B scripts/tests/test_driver_layers.py` green, exceptions rows 9; `python -B tools/source_split.py ... --dry-run` exits 0. witness scope: those two.

**P1-2** owns: `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\story_run.py`, `...\scripts\driver_core.py`, `driver_runner.py`, `driver_dialog.py`, `driver_conductor.py`, `driver_dispatch.py`, `driver_s0.py`, `driver_sources.py`, `driver_stage_plan.py`, `driver_stage_build.py`, `driver_stage_s5.py`, `driver_stage_s6.py`, `driver_stage_s7.py`, `driver_stage_s8s9.py`, `driver_gates.py`, `driver_machine.py` (all under `...\scripts\`), the §3 rows 1-6, 8-10, 12 files (absolute), `C:\QAFactory\forge-repo\tools\lint-baseline.json`, `C:\QAFactory\forge-repo\tools\dup-baseline.json`, `C:\QAFactory\forge-repo\docs\SIBLING_MAP.md`
non-goals: no hand edit of moved code; no behaviour change; no map edit (P1-1 owns it); `install_smoke.py` (integrator).
DoD: the tool report with P1-P7 all equal and exit 0; `python -B scripts/tests/test_driver_layers.py`; `python -B scripts/tests/test_story_run_words.py`; every §3 verification command; `python -B scripts/selftest.py --limits --lang` (integrator may run it instead).
witness scope: the above; everything else CI.

**P1-4** owns: `C:\QAFactory\forge-repo\tools\piles.py` (+ the existing `tools/test_piles*.py` row for owns). DoD: `python -m pytest tools/test_piles.py -q` (narrower `-k owns` if split).

## 8. Forks (Lead/owner) — and what a builder does until answered

| # | Fork | Options | Recommendation (builder follows it until answered) |
|---|---|---|---|
| F1 | proof of the tool | (a) built-in `--selftest` + its run-time proofs, no new test file; (b) a new `tools/test_source_split.py` | (a): the role rule forbids a new test file; the selftest exercises every refusal |
| F2 | the 5 name-kind upward exceptions | (a) rehome the 5 constants down (P1-1), list 14 -> 9; (b) allow a lazy upward import as an L6 exception | (a): shrinks a ratchet, no new door in L6; homes are judgment — Lead confirms the 5 targets |
| F3 | source-pin checks in kept tests | (a) delete member pins, port form censuses to `driver_text()`; (b) port all | (a): docs/TESTING.md :94 deletes pins; form censuses catch NEW sites |
| F4 | `piles.py` owns on a facade path | (a) P1-4 now; (b) the builder-rules note only | (a): two roads to one file otherwise escape the zone check (P31); cheap |
| F5 | facade scope | (a) every old `story_run.<x>` resolves (P3); (b) the measured list only | (a) now (Lead: old imports work); the report counts facade reads; moving readers to home modules is a queued node — the facade is a second road to each name (P31) the owner may want closed |
| F6 | census readers | (a) the tool owns a generic census and cross-checks the layer test's count; (b) the tool imports `test_driver_layers.definitions` | (a): B needs a non-Driver census; a queued node makes `test_driver_layers` call one shared census |
| F7 | `covers` for new modules | (a) append every new module to all 59 rows covering `story_run.py`; (b) narrow per row | (a): witness scope equals today's for `story_run.py`; narrowing is spec C's |
| F8 | phase-1 granularity | (a) one cut commit; (b) one commit per home (`--homes`) | (a): one revert, one registry rewrite |
| F9 | stage split | (a) the six modules of §5.1 by map `row`; (b) fewer/other seams | (a): derived from the map's own row field; `consumer_*` sit with S6 by `row` 74 |

### 8b. Small choices closed by the designer
`tools/` as home; mixin name = CamelCase(home); bases by rank descending, `DriverChains` last; source order inside modules;
section markers copied as orientation; `HERE` only in driver_core (supersedes the map note "each module carries its own",
which contradicts L2); W1 `Driver.X` -> `HomeClass.X`; generated docstrings ASCII; owners of the 22 stage rows = first
accessor's module; phase-0 helper names `driver_sources/driver_text/patch_driver_global/set_driver_global`.

## 9. Not verified by this spec
- A. Counts by Grep (ripgrep): homes `"home": "<h>"` in the map; 59 `^    "story_run.py"` in test-layers; 20 `"file": "story_run.py"` in the census; patch lists by the §4 commands; `global|nonlocal` in story_run.py = 0 WITHOUT a positive control; `__qualname__|__module__|getsource|co_filename` only in `tests/driver_trace.py` (positive control: those hits).
- Line estimates per module (names x 27) — the dry-run measures.
- Whether `test_judgment_census` / `refusal_registry.sites` scan new `driver_*.py` files (`read_package(root, files)` list not read; check `rg -n "files" scripts/tests/test_judgment_census.py`). If they scan a fixed list, the census carrier needs the list too.
- Whether `tools/test_quarantine.py check` treats a `covers` append in a keep row as an edit needing a door (td-15 :514 speaks of rows, not covers).
- Whether `lint_ratchet` flags the facade's re-export imports (F401) beyond `# noqa`; whether dup scope identity contains the path (inferred from `dup_ratchet.py` :41-46).
- Newline style and BOM of `story_run.py` (Read does not show bytes); `.gitattributes`.
- The classification of the 2 `test_story_run_refusals` functions (left to the builder by the rule) and `host_window_reason` as S5 (by name).
- Which callers load `references/block-names.json` at run time (only the validator `waiver._name_row` was read).
- Map rows' `kind` vs census kind for W1 targets (read: `role_words`, `stuck_facts`, `probe_reason`, `s4_repair_owed`, `stage_repair_owed` staticmethod; `CUT` classconst).
