# TD-11 spec B — source maps and module boundaries: `controller.py` and the seven first-wave files

DRAFT by the designer, 11.11.2026, from `docs/tasks/specs/td-11-lead-brief.md`. Decisions belong to the Lead; forks are in §13.
Paths are relative to `ai-packages/qa-factory/` unless they start with `docs/`, `plans/`, `tools/`. Line numbers are as read on
`main` a9bd758 (working tree of this session); every load-bearing fact carries its carrier `file:line` or its counting command.
Commands of the form `grep -c` / `rg` below are the forms the Grep tool ran (ripgrep); the counts are reproducible with them.

Sibling specs: A (`docs/tasks/specs/td-11a-driver-split.md`) owns the MOVE TOOL and the SHARED-REGISTRY PROTOCOL; this spec only
states what its maps REQUIRE of them (§2.9). C (`docs/tasks/specs/td-11c-test-split.md`) owns test-file splitting; this spec
only names which test file mirrors which new module (§x.f).

---

## §1 Goal, and the invariants touched

**Goal.** Cut `controller.py` (9 951 lines) and `gate_preflight.py`, `gate_brief.py`, `report_facts.py`, `story_step.py`,
`probe_by_code.py`, `hooklib.py`, `stage_guard.py` into modules whose boundaries are written as one MAP per file, executable by
the move tool of spec A, so that parallel builders get disjoint `owns` and a builder's local witness stays under a minute. No
behaviour changes: every old import, every module-attribute read or patch, every command line and every door text keeps working
(owner's words 1 and 3 of the brief; Lead decision "names stay entry files and facades").

**AR-n touched, and how each is kept** (host adaptation 9; the change check of each is written into the DoD of §11):

| AR | how it is touched | how it is kept | change check in the DoD |
|---|---|---|---|
| AR-13 one reader per fact | every name now has a home module; readers could start importing a part directly | the facade is the ONE road to a family's names: no file outside the family imports a part (check L11, §2.6) | L11 green; `rg -n "^\s*(import|from) (controller|rehearsal|gate_brief|report_facts|story_step|probe_by_code|hooklib|stage_guard)_\w+" scripts/ --glob "!<family parts>"` empty, positive control: the same command finds the facade's own `import` of a part |
| AR-14 one writer | the map file is a new artifact | one writer: the family's node writes it through the tool of spec A; afterwards only nodes that move names edit rows (as `driver-layers.json`) | the map's `about` names its writer; `test-layers.json` `fixture_owners` row in the same commit |
| AR-15 one survivor | the facade mechanism is needed by 8 (+1 with `story_run.py`) files | ONE module `scripts/module_facade.py` (F-5); no family writes its own `__getattr__`/`__setattr__` forwarding | L11 checks that every facade calls `module_facade.install`; grep for a second `ModuleType` subclass in `scripts/` is empty, positive control finds the one in `module_facade.py` |
| AR-19 twins | no twin logic moves; axis-5 rows name functions by `module.function`, which the facade keeps valid | named in the commit: "axis 5 rows unchanged, read through the facade" | grep axis 5 of `docs/SIBLING_MAP.md` for each moved function: a row with a `file:line` is rewritten (§x.e) |
| AR-20 shrink-only ratchets | new ratchet: the `exceptions` list of each new map; the judgment census, lint and dup baselines change file keys | each new map is born with an EMPTY pinned exceptions list (F-3 rec.), so it can only stay empty; census rows change `file` only, counts unchanged; dup baseline GONE rows are removed by the integrator's `--update` | the verdict lists every row added or raised (key, old -> new); census `ratchet` object byte-identical; new ratchet joins axis 18 of `docs/SIBLING_MAP.md` and critic question 9 in the commit that creates the first family map |
| AR-22 producer and readers in one commit | every carrier keyed to a file name (§x.e tables) is a reader of "where the function lives" | each family's move commit rewrites its carriers by the registry protocol of spec A | the §x.e table is the checklist; `test_gate_registry.py`, `test_refusal_registry.py`, `test_judgment_census.py`, `test_install_paths.py`, `test_controller_blocks.py` in the node's witness when the family has rows there |
| AR-12 friction | `hooklib.py` and `stage_guard.py` are imported by every hook start | parts import only what the original imported (stdlib for `hooklib`); the facade imports parts eagerly with literal imports | `python -X importtime -B -c "import hooklib"` (and `import stage_guard`) before and after, cumulative µs of the top line in the report; over +20 % is a stop for the Lead (§12 E10) |
| AR-29 where judgment lives | the maps and their test add checks | every added check judges DATA only (names, homes, edges, imports): owner **data**, census class **xref** (map rows against definitions, edges against ranks) or **shape** (row well-formedness); the test lives in `scripts/tests/` and is outside the census (`judgment-census.json` `about`: "scripts/*.py outside scripts/tests/"); `module_facade.py` carries no refusal of a role's output | `test_judgment_census.py` green; a census row for `module_facade.py` if the census test demands one (class `shape`, owner `data`, §14 U7) |

AR-1/AR-2 (variety): not touched — the family table is data in each map header (§2.1), the test reads it by key, never a file
name in code. AR-4, AR-5, AR-6, AR-9, AR-10, AR-11, AR-16, AR-17, AR-18, AR-21, AR-23..AR-28: not touched (no refusal text, no
handoff field, no question, no state is added or changed; refusal texts move byte-identical with their bodies).

**FR-n and P-n**: FR-30 (parts are English, `selftest.py --lang` in each witness); FR-31 (no new timing dependence: parts are
imported eagerly in a fixed order); FR-32 (no fix here; a defect found while moving is a finding, not repaired in the move
commit); FR-37 (every path a person or role reads stays the path the code writes: the entry names do not move, §12 E5); FR-44
(maps are read by tests and the generator only, so they live in `scripts/tests/fixtures/`); FR-54 (siblings by the map: §x.e);
P12 (new code checked for similar places: one facade survivor); P27 (code owns data: the map is data, homes are decided by rules
here and accepted by the Lead); P31 (one road: one map shape, one test, one facade mechanism, one naming rule for all nine
files — F-2).

---

## §2 Common rules for all eight maps

### 2.1 The map file: shape and place

- One file per family: `scripts/tests/fixtures/<prefix>-layers.json`, the same naming as the existing
  `scripts/tests/fixtures/driver-layers.json` (`<prefix>` per 2.3). FR-44: read by the layer test and the move tool only.
- Shape = `driver-layers.json` (`driver-layers.json:1-5`, `:1210`): `schema`, `about`, `layers` (list of lists of module stems,
  index = rank), `not_driver` (prefix-carrying modules that are no part; key name kept for one shape), `names`
  (`{name, kind, home}` rows; `kind` in `const|func|class|method|staticmethod|classmethod|classconst` as
  `test_driver_layers.py:84-111` derives them), `exceptions` (`{from, to, kind, reason}`), `source_readers`, `source_mentions`.
  The driver-only tables (`attributes`, `adhoc_attributes`, `state_keys`, `dynamic_state_keys`, `string_dispatch`,
  `stdout_writers`) are OPTIONAL: absent = that check is not run for the family (a data default, AR-1). The driver rows carry a
  `row` field (draft-row provenance, `driver-layers.json:6`); family maps do not.
- NEW header object, also added to `driver-layers.json` by node B0: `"family": {"facade": "<stem>", "prefix": "<prefix>_",
  "class": "<Class>" | null, "cut": "mixins" | "functions"}`. The test discovers maps by the glob `fixtures/*-layers.json` and
  reads everything it needs from this object (no family name in test code).
- Class members are keyed `<Class>.<member>` whatever mixin holds them (the driver's `Driver.<member>` rule,
  `test_driver_layers.py:18-20`). Imports, nested functions, the `if __name__ == "__main__":` block and module dunders
  (`__getattr__`, `__all__`) are not census names.

### 2.2 How homes are assigned (the generator's rule, executable by code)

Per file, in this order; the result is the full `names` array, written by the tool of spec A and checked by the layer test:

1. **Range rule.** Every census name gets the home of the line range (section seam) its definition STARTS in (`ast` `lineno`),
   from the per-file range table in §3-§10. Class members of the split class get the range of the MIXIN table.
2. **Explicit list.** Names listed under "explicit" in the file's section override rule 1.
3. **Facade-bound names** (stay in the facade, home = `<facade stem>`): the split class itself (`Controller`, `Rehearsal`);
   `main`; module dunders; a module-level function or constant whose body names the split class at run time (`Controller(`,
   `Rehearsal(` — not a string annotation); a name rebound by a `global` statement whose holders cannot all share one part
   (§12 E3).
4. **Demotion fixpoint (function homes only).** For a module-level name N (home H) referenced by a function or constant of home
   G with G != H and rank(H) >= rank(G): N moves to the family's rank-0 module (`<prefix>core` or the file's rank-0 row);
   repeat until no such edge remains. Mixin members are never demoted by this rule (calls through `self` need no import).
5. **Class-level names of the split class** (`classconst`, and a `staticmethod` named through the class `<Class>.<m>`): a
   classconst read by two or more mixin homes, or read as `<Class>.<k>` from another home, and a static named as `<Class>.<m>`
   from another home, home in the base mixin `<Class>Base` (2.5).
6. The generator prints, per home: names before/after demotion, lines, and every demoted name with the referencing site.
   **Seam check** (F-4): the cut of a file is accepted for the move only when, after rule 4, the rank-0 module holds at most 35 %
   of the file's lines and every other part keeps at least 60 % of the names its range gave it; otherwise the node STOPS with
   the generator output as its report ("seam does not hold: <part>, <numbers>") — it does not force the cut.

### 2.3 Naming (one convention for all nine files, P31; F-2)

- Part prefix: the lowercase name of the split class when the file is cut into mixins of ONE class, otherwise the file stem:
  `story_run.py` -> `driver_` (already fixed, class `Driver`), `controller.py` -> `controller_`, `gate_preflight.py` ->
  `rehearsal_`, the six function files -> `<stem>_`.
- Part module: `<prefix><area>.py` in `scripts/`; mixin class `<Class><Area>` (CamelCase of the area); the lowest mixin is
  always `<Class>Base` in `<prefix>base.py`; the lowest function module is `<prefix>core.py`.
- Collision check, done: no `scripts/{controller,gate_preflight,gate_brief,report_facts,story_step,probe_by_code,hooklib,stage_guard}_*.py`
  and no `scripts/rehearsal*.py` exists (Glob, empty; positive control `scripts/driver*.py` finds `driver_chains.py`,
  `driver_journal.py`, `driver_timing.py`).

### 2.4 The facade rule (F-1, recommendation)

The original file stays the entry point and the import facade. It contains only: its docstring, the original stdlib imports it
still uses, the `sys.path.insert` line, one literal `import <part>` per part (literal, so `scenario_walk._closure` follows it,
`scenario_walk.py:835-859`), the assembled class (mixin files), the facade-bound names of 2.2 rule 3, `main`, the
`__main__` block, and one call `module_facade.install(__name__, [<parts, low rank first>])`.

`scripts/module_facade.py` (new, one survivor for all families, F-5):
- reads: the module's `__getattr__` (PEP 562) returns a name from the first part (low rank first) that binds it — LIVE, so a
  cache a part rebinds (`hooklib._PROJECT_ROOT_CACHE`) reads current; an existing module `__getattr__` of the facade
  (`stage_guard.py:127-131`) is chained after the parts;
- writes: the module class is swapped (`sys.modules[name].__class__ = <ModuleType subclass>`) so `setattr(facade, n, v)` /
  `mock.patch.object(facade, n, v)` / `facade.n = v` writes `n` into EVERY part that binds `n` (definition or import) and into
  the facade if it binds it; `delattr` likewise. This keeps today's meaning of a patch: before the cut one binding was seen by
  all the file's code and by every reader through the module; after it every binding is written;
- `dir(facade)` = facade names plus part names.
- Works when the facade runs as `__main__` (directly or through `run_py_entry.py`, which execs a fresh module as `__main__`,
  `run_py_entry.py:87-97`): `install` uses `sys.modules[__name__]`.

Invariant the facade protects: **every read or write of `<stem>.<name>` that worked before the cut means the same after it**;
what stays unreachable: a part bypassing the facade for outside callers (AR-13) and a patch that reaches only some bindings.
Error direction: the forwarding may only err toward refusing — an unknown name raises `AttributeError` exactly as today; it never
invents a value. Adversarial inputs that must stay on the safe side: a name bound in two parts by import (`json`, `Path`,
`atomic_json`) — the write goes to both; a name a part rebinds through `global` — the read is live; `mock.patch(..., create=True)`
of an absent name — set then delete leaves no trace in any part; `from <stem> import X` taken at import time — a copy, exactly
as today (not reached by a later patch, as today).

### 2.5 The mixin rule (`controller.py`, `gate_preflight.py`)

- One mixin class per mixin home, `class <Class><Area>:` (no base), in its part; `class <Class>(<mixins by rank descending,
  then name>, <Class>Base)` in the facade. No member is defined twice (L2), so the MRO order cannot change a lookup.
- Mixins never import each other, with ONE exception: a part may import `<Class>Base` from `<prefix>base` at module top, solely
  to name `<Class>Base.<m>` (2.2 rule 5). Inside a moved body: `<Class>.<m>` with `m` in the same home becomes
  `<Class><Area>.<m>`; with `m` in Base becomes `<Class>Base.<m>`; any other target is impossible by rule 5. `self.` and
  `type(self).` forms are left as written.
- Instance state (`self.store`, `self._items_memo` for the controller — brief; `Rehearsal.__init__` attributes at
  `gate_preflight.py:1268-1302`) is set in `__init__`, which homes in Base.
- Mixin homes of one class share ONE rank (F-3 recommendation): calls through `self` cross homes freely, so no upward edge and
  no exception exists by construction; module-level function homes are ranked below the mixin rank, entry-level function homes
  above it.
- Calls by class name from OUTSIDE the family (`Controller.X` in another file, instance calls such as
  `Controller(root)._dispatch_starts()` at `story_run.py:11174`, `_pinned_links()` at `:11330`) resolve through the assembled
  class and its MRO: unchanged.

### 2.6 The layer test: reuse and generalise `test_driver_layers.py` (not a new file)

`scripts/tests/test_driver_layers.py` (keep row `test-layers.json:1141`) becomes the test of every map: it globs
`fixtures/*-layers.json` and runs per family, reading the `family` header. Checks:

| id | what | owner / census class |
|---|---|---|
| L1 | census both directions: every name defined in the family (facade + parts) has a row; every row names a definition | data / xref |
| L2 | one definition per name, in its home (or in the facade while the home part does not exist yet) | data / xref |
| L3, L4, L7, L9 | driver-only tables — run only when the map holds the table | data / xref (unchanged) |
| L5 | no call/name edge to a higher rank unless in `exceptions`; `exceptions` pinned per family, shrink-only (family maps: pinned empty) | data / xref |
| L6 | no import of a higher-ranked part | data / shape |
| L8 | literal `<facade>.py` mentions in `scripts/tests/*.py` declared as `source_readers` / `source_mentions` | data / xref |
| L10 | well-formed rows (home in `layers`, one row per name, reasons present) | data / shape |
| L11 NEW | the facade: imports each part by a literal `import`, calls `module_facade.install` with the parts in rank order, defines no name whose home is a part; no file outside the family (all of `scripts/`, `tools/` excluded) imports a part | data / shape |
| L12 NEW | no `<Class>.<m>` attribute in a part except `<Class>Base.<m>` / `<Class><Area>.<m>` of its own home; no part imports another part except lower-ranked function parts and `<prefix>base` | data / xref |

`DRIVER_CLASS` (`test_driver_layers.py:33`) and `read_modules` (`:62-72`) become family-parameterised (class regex
`^<Class>[A-Za-z0-9]*$`, files `<facade>.py` + `<prefix>*.py` minus `not_driver`). `PINNED_EXCEPTIONS` (`:43-58`) becomes a
per-family pin: the driver's 14 rows unchanged, every other family empty. The bad fixtures (`:795-888`) gain one fixture per new
check (L11, L12) and one family-agnostic run of the existing fixtures with a non-driver family header.

### 2.7 What stays importable

Everything. Under F-1 (rec.) the importer lists of §x.b are informational: any `<stem>.<name>` read through the facade resolves.
Search command for importers and patches (run per family, results go in the node report, not in this spec):
`rg -n "^\s*(import <stem>( as \w+)?|from <stem> import)" ai-packages/qa-factory/ experiments/ tools/` and, for each alias
`A` found, `rg -n "\b(<stem>|A)\.[A-Za-z_]\w* = |patch(\.object)?\(\s*(<stem>|A)\b|patch\(\"<stem>\." ai-packages/qa-factory/`.

### 2.8 Witness (per family node)

Local, each under a minute: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>` — run the keep
files it prints EXCEPT those weighing over 60 s in `scripts/slow_tests.json` (those go to CI); plus
`python -B ai-packages/qa-factory/scripts/tests/test_driver_layers.py` and `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang`;
plus the move tool's own output (spec A). CI canon: everything else (the batch canon, D-0059).

### 2.9 What the maps REQUIRE of spec A (stated only as requirements)

R-A1 the move tool executes any `*-layers.json` with a `family` header (not only the driver map), including 2.2 rules 3-5 and the
2.5 rewrite of `<Class>.<m>`; R-A2 each part's import block = exactly the names its bodies use (no unused import: the lint
baseline must not grow), each part carries the original's `sys.path.insert` line; R-A3 lazy (in-body) imports travel with
their bodies unchanged; R-A4 `--draft` mode prints 2.2 rule 6 without writing; R-A5 the registry protocol rewrites, in the
move commit, every carrier row of the §x.e tables marked "must change", one line per row, so parallel families touch disjoint
lines; R-A6 every keep row of `test-layers.json` whose `covers` names `<stem>.py` gains every part in the same commit (otherwise
`--witness-for <part>` prints "no scenario or keep row covers", `scenario_walk.py:920`); R-A7 the tool refuses (no write) when a
test patches a class attribute of the split class by name (`setattr(<Class>, ...)`, `patch.object(<Class>, ...)`) on a target
whose home is not Base (§12 E4).

---

## §3 `controller.py` (9 951 lines; prefix `controller_`, class `Controller`, cut `mixins`)

Verified structure: module-level 52-1591 (seams: `controller.py:1143` gate B orders, `:1500` held for code); `projection`
`:1592`; `_TierEnds` `:1994`; `class Controller` `:2018`-`:9093`; after it op tuples, `stop_after` `:9130`, the gate-decision
executor `:9236`, `--brief` `:9661`, `main` `:9730`. Method count 227 (`rg -c "^    def " controller.py` gives 229 incl. two
nested at `:358`, `:897`; the class range holds 227 — sum of the table below).

### (a) Module table

Ranks: `layers = [["controller_core"], ["controller_orders"], ["controller_projection"], [<the 11 mixin parts>], ["controller_gate"], ["controller"]]`.

| home | holds (range by definition line) | names | ~lines | rank |
|---|---|---|---|---|
| `controller_core` | 52-1142: stage vocabulary, statuses, repair ledger, windows, manual blocks and lanes, code close facts, set/reopen stage, `now_iso` | 56 functions + constants | 1 090 | 0 |
| `controller_orders` | 1143-1591: gate B orders, closure, held dispatches, held for code | 27 functions + constants | 450 | 1 |
| `controller_projection` | 1592-2017: `projection`, `_TierEnds`, the constant at `:1999` | 2 + constants | 425 | 2 |
| `controller_base` / `ControllerBase` | methods 2019-2433: `__init__`, `state`, refs, `prepare`, inputs, plan baseline, gate A marks, `_after_commit`, person pass + rule-5 names | 17 + rule 5 | 415 | 3 |
| `controller_scope` / `ControllerScope` | 2434-2960: case rows, ticket, liveness, verdicts, holding, `_pinned_links`, scope membership, revise scope, cover basis | 31 | 527 | 3 |
| `controller_gates` / `ControllerGates` | 2961-3654: accept order, design reviews, decision problems, gate items, `build_gate_decision`, review verdicts | 18 | 694 | 3 |
| `controller_rework` / `ControllerRework` | 3655-4733: `build_rework_request`, rework kind, `stage_scope`, S5 windows, `scope_instances`, plan hashes, gate A content | 36 | 1 079 | 3 |
| `controller_engine` / `ControllerEngine` | 4734-5310: inputs, pipeline, `project`, `refresh_derived`, `apply`, replay, legacy import | 14 | 577 | 3 |
| `controller_validate` / `ControllerValidate` | 5311-6165: `validate` and its static helpers (`_raise_all` etc., rule 5 may move some to Base) | 11 | 855 | 3 |
| `controller_resume` / `ControllerResume` | 6166-6439: FB-4 resume, caps, `_window_beside_running`, `_lane_beside_running`, `build_resume_request` | 16 | 274 | 3 |
| `controller_completion` / `ControllerCompletion` | 6440-7612: S5 plan and windows, completion problems, collect, gaps, S3 gate, `_closes_stage`, code review | 33 | 1 173 | 3 |
| `controller_liveness` / `ControllerLiveness` | 7613-8093: `stage_guard_errors`, `_dispatch_starts`, denial, liveness fixes, `record_return`, checkpoint, closure repairs, release | 15 | 481 | 3 |
| `controller_holds` / `ControllerHolds` | 8094-8446: held work, reopen, leave unlaunched, hold ops, `settle_order` | 17 | 353 | 3 |
| `controller_next` / `ControllerNext` | 8447-9093: `stage_repairs`, `recover`, retry packets, `next_action`, `launch_answer`, packets, `_next_action_for_state` | 19 | 647 | 3 |
| `controller_gate` | 9094-9729: operation tuples, `stop_after`, `with_stop_after`, risk line, gate-decision executor, `apply_door`, `_cli_story_root`, brief output | 28 functions + tuples | 636 | 4 |
| `controller` (facade) | `Controller` (assembled), `main` (9730-9951), `__main__` | 2 | ~260 | 5 |

Method counts per range are from `rg -n "^    def " controller.py` (lines listed in the reading trail); 17+31+18+36+14+11+16+33+15+17+19 = 227.
Explicit list: none needed beyond rules 3 and 5. Rule-5 candidates (named as `Controller.<m>` across homes, `rg -n "Controller\.[A-Za-z_]+" controller.py`):
`_raise_all` and `_noted` (named from `_validate_rerun_after` `:4086-4113` in rework and `_hold_op_refusal` `:8317-8318` in holds,
defined in validate `:6093`, `:6136`), `_covers` (named from `_last_covering` `:3652` in gates, defined in scope `:2957`),
`_stamped_paths` (named from `build_rework_request` `:3845`, defined in next `:8740`) -> Base. Same-home class-name calls
(`:2946`, `:2959`, `:4045-4105`, `:6152`, `:8749-8863`, `:8987-9007`) become `Controller<Area>.<m>`. `main` `:9827` stays
`Controller._raise_all` (facade, the class is there).

### (b) The facade keeps

- Importers (verify with 2.7): 187 files, 37 non-test (brief); seen in this reading: eager `from controller import ...` in
  `story_run.py:72`, `story_step.py:104`, `no_move.py:27`, `migrate_coverage.py:13`, `investigation_probe.py:39`,
  `collect_stall.py:90`; lazy everywhere else (`acceptance.py:1390,1455`, `brief_pack.py:1801..4081`, `s5_plan.py:398..1483`,
  `window_record.py:438,1203,1887`, `stage_guard.py:811,1435,1720`, `gate_preflight.py:1457,1539`, `report_facts.py:551..2312`, ...).
  Many read `CT.<name>` / `C.<name>` after `import controller as CT` — any module-level name must stay readable: F-1 gives it.
- Module-attribute patches (2.7 search), verified: `mock.patch.object(controller, "atomic_json", ...)` `test_controller_brief.py:195`
  (reader `_print_result` `controller.py:9722`, home `controller_gate`; `atomic_json` is also imported by base and engine —
  F-1 writes all three); `controller_module.validate_record` `test_controller_state.py:1304,1308` (readers `:3119` gates,
  `:5441` validate — both bindings written); `controller_module_.Controller = factory` `test_controller_state.py:1934,1953`
  (facade-bound, read by `execution_request` through the module); `controller_module.code_close_conflicts` /
  `code_close_facts` `test_execution_request.py:1033..1098` (home core; read through the module by `execution_request`);
  `controller.SETTLED` / `DISCOUNTED` `test_collect_stall.py:275-286`; `mock.patch("controller.Controller", ...)`
  `tests/fixtures/manual-evidence/scaffold.py:345`. Instance patches (`controller._window_stand_signal = ...`
  `test_controller_rework.py:554`, `controller._revision_past_own_return` `test_controller_release.py:263`, where `controller` is
  a `Controller` instance, `:39`) are unaffected by any cut.

### (c) Class
Mixins as in (a), one rank (F-3). Private members reached from other files (`_dispatch_starts`, `_pinned_links`,
`_lane_beside_running` — `story_run.py:11174`, `:11330`, `:15122` comment) are instance calls: MRO keeps them.
`PLAN_BASELINE` (read `self.PLAN_BASELINE` `:2287`) and any other classconst follow rule 5.

### (d) Import cycles
Lazy imports from controller bodies into `stage_guard` (`:82`, `:7626`), `planning_contract` (`:3181`, `:5427`, `:7464`, `:9323..9451`),
`acceptance` (`:3906`, `:5514`, `:5871`, `:7302`, `:7398`, `:7459`, `:7588`, `:9079`), `gate_preflight` (`:4248`, `:9925`),
`s5_plan` (`:4413`..`:6956`), `window_record` (`:7040`..`:7304`) travel with their bodies (R-A3); they run at call time, when
`controller` is fully loaded. Eager imports of each part = a subset of the original's (`event_store`, `hooklib`, `person_words`,
`record_schema`, `runtime_policy`, stdlib; `controller.py:30-49`) plus lower parts — none of the six partners, never the facade.
The partners' imports of `controller` are lazy except the six eager ones in (b), none of which `controller` imports back. Hence
no new cycle: proof obligation in the DoD = `python -B -c "import controller_core, controller_base, ..., controller"` in a fresh
process (each part importable alone, in rank order) plus L6/L12.

### (e) Carriers keyed to `controller.py`

| carrier | key kind | facade keeps it? |
|---|---|---|
| `refusal_registry.py` 8 rows `"kind": "operation", "file": "controller.py"` (`:574`, `:594`, `:609`, `:622`, `:695`, `:702`, `:711`, `:720`) | `guarantor` text must be in the file's text (`refusal_registry.py:918-926`) | NO — `file` becomes the part holding the guarantor (`_passed_by_person` base, `_s5_plan_problems` / `_s5_plan_accept_problems` / `_grown_close_problems` completion, `check_decision` gates, `_executing_refusal` orders, `_settle_order_refusal` / `_hold_op_refusal` holds) |
| `scripts/tests/fixtures/judgment-census.json` 59 rows `"file": "controller.py"` (`:159-217`) | `{file, function}` | NO — `file` = home part; ratchet counts unchanged |
| `tools/controller-blocks-gen.py:22` `SRC` (one file) and `collect_rows` keyed fn+message | file text | NO — reads the facade + all parts (by the map's `layers`); rows ordered by (rank, file, line) — closed choice S-3 |
| `scripts/tests/test_controller_blocks.py:56` reads `controller.py` text | file text | NO — reads the same set as the generator |
| `design/controller-blocks.md` | generated | regenerated in the move commit (row order may change, counts must not) |
| `runtime_paths.py:225` `ENTRYPOINT_NAMES` | script name | YES |
| `scripts/tests/scenario_walk.py:45` door modules | module closure | YES (literal part imports) |
| door texts printing `controller.py --operation ...` (~116 lines in 26 scripts, brief) | command | YES (FR-37) |
| `design/architecture.md:256` `controller.py:539` | file:line | NO — rewritten to the home part and its new line |
| `references/null-outcomes.json:105,108,131`, `field-producers.json:13,23`, `artifact-writers.json:15` | file name / `file::function` (form not read, §14 U3) | YES if the key is the command or the module; NO if `file::function` -> home part |
| `scripts/tests/test-layers.json` `covers` naming `controller.py` (e.g. `test_controller_state.py` row `:880-906`) | path | NO — parts appended (R-A6) |
| tests reading the text of `controller.py`: `test_controller_blocks.py:56`, `test_first_look_wiring.py:105`, `test_needs_author.py:375`, `test_refuse_case.py:203`, `test_s5_plan_controller.py:447`, `test_story_run_refusals.py:453`, `test_story_root_class.py:1005`, `test_task_root_parsers.py:241` (as seen; L8 census is authoritative) | file text | NO — L8 rows in the map; the move node owns these tests for the names it moves (t-301 §0b F3 precedent); a quarantined one is marked "перенос TD-11" by the Lead |
| `tools/lint-baseline.json`, `tools/dup-baseline.json` | path / fingerprint | NO — integrator per protocol (`--update`, GONE rows) |
| `references/release-fingerprint.json` | hash | rebuilt at release |

### (f) Test files mirroring the parts (names only; splitting is spec C)
core/orders/projection: `test_controller_state.py` (keep, fixture of ~50 tests); scope/gates: `test_controller_gate_decision.py`,
`test_controller_lifecycle_gate.py`, `test_controller_rework_scope.py` (keep); rework: `test_controller_rework.py` (keep, 107 s —
CI); resume/liveness: `test_controller_resume.py`, `test_controller_release.py` (keep); completion: `test_s5_plan_controller.py`;
gate/facade: `test_controller_doors.py`, `test_controller_task_flag.py`, `test_controller_blocks.py` (keep),
`test_controller_brief.py` (pin_holds `:5327`). Quarantine (not run): `test_controller_paths.py`, `_scope_expansion.py`,
`_stage_acceptance.py`.

---

## §4 `gate_preflight.py` (6 097 lines; prefix `rehearsal_`, class `Rehearsal`, cut `mixins`)

Verified: module-level 1-1257 (seams `:325`, `:376`, `:657`, `:772`); `class Rehearsal` `:1258`-`:5753` (163 methods: `rg -n "^    def "`
gives 167, of which `:953`, `:971`, `:5971`, `:5997` lie outside the class); `run` `:5754`, `render` `:5787`, `brief_lines` `:5917`,
`selftest` `:5994`, `main` `:6081`.

### (a) Module table — ranks `[["rehearsal_core"], [<9 mixin parts>], ["rehearsal_selftest"], ["gate_preflight"]]`

| home | range | names | ~lines | rank |
|---|---|---|---|---|
| `rehearsal_core` | 1-1257: helpers, executor/profile questions, reporter context, precondition shape, ids | 53 functions + `ReporterCtx` + constants | 1 180 | 0 |
| `rehearsal_base` / `RehearsalBase` | 1258-1444: `__init__`, profiles memo, recording (`add`, `unavailable`, `waiver_command`, ...) + rule 5 | 12 | 187 | 1 |
| `rehearsal_start` / `RehearsalStart` | 1445-1914: gate A 1-2 (decision, stage guard, prepare, permissions, cases, planning contract, questions) | 11 | 470 | 1 |
| `rehearsal_stand` / `RehearsalStand` | 1915-2523: gate A 3, 3b (vcs, stand, env gaps, role accounts, sign-in) | 20 | 609 | 1 |
| `rehearsal_s5` / `RehearsalS5` | 2524-2962: gate A 4, 4b (executor, dependencies, toolchain, stand limits) | 13 | 439 | 1 |
| `rehearsal_reporter` / `RehearsalReporter` | 2963-3936: `check_s5_reporter` and its rehearsal | 40 | 974 | 1 |
| `rehearsal_probe` / `RehearsalProbe` | 3937-4287: gate A 4d runtime probe | 20 | 351 | 1 |
| `rehearsal_credentials` / `RehearsalCredentials` | 4288-4832: `check_s5_credentials` and helpers | 19 | 545 | 1 |
| `rehearsal_cases` / `RehearsalCases` | 4833-5447: gate A 5 case preconditions | 23 | 615 | 1 |
| `rehearsal_gate_b` / `RehearsalGateB` | 5448-5753: gate B checks | 5 | 306 | 1 |
| `rehearsal_selftest` | 5994-6080: `selftest` (F-6) | 1 | 87 | 2 |
| `gate_preflight` (facade) | `Rehearsal`, `run` (names `Rehearsal(` `:5760`), and 5787-5993 `render`, `unmatched_integrations`, `integration_ids_of_case`, `_group_by_integration`, `brief_lines` (explicit: entry-level, kept beside `run`), `main` | 8 | ~260 | 3 |

12+11+20+13+40+20+19+23+5 = 163. Seams `:2963` and `:4288` have no marker: explicit range starts. Rule 5: `Rehearsal._rel_inside`
named at `:3074` (reporter) — Base if defined in another home. Classconst `_declarations_read = False` `:1266` (read through
`self`; "set by `_integration_keys`") -> §12 E2.

### (b) Facade keeps
70 importers (brief); verified 50+ sites by `rg "import gate_preflight( as (\w+))?|from gate_preflight import"` (e.g.
`brief_pack.py:2536`, `gate_brief.py:417..3034`, `story_run.py:3698..21049`, `stand_gaps.py:170..594`). Module-attribute patches:
55 sites in 16 test files (`rg -c "\b(gate_preflight|GP)\.[A-Za-z_]\w* = |patch\.object\((gate_preflight|GP)\b|patch\(\"gate_preflight\." scripts/tests`;
`test_gate_preflight.py` 17) — F-1 covers them without a per-site list.

### (c) Class: as §2.5; the step tuple of `run` (`:5762-5773`) names bound methods (`r.check_*`), unaffected.

### (d) Cycles: `controller` imports `gate_preflight` lazily (`controller.py:4248`, `:9925`) and `gate_preflight` imports `controller`
lazily (`gate_preflight.py:1457`, `:1539`): both stay lazy in their bodies. Parts import only the original's eager imports.

### (e) Carriers

| carrier | key | facade keeps? |
|---|---|---|
| `references/gate-registry.json` 17 rows `{file: "gate_preflight.py", function}` (`:13`, `:14`, `:53`, `:177`, `:292-296`, `:313`, `:486`, `:500`, `:507`, `:508`, `:523`, `:530`, `:531`) | file+function | NO -> home part |
| `references/null-outcomes.json:45,48,61,64,104` | `file::function` (§14 U3) | NO if function-keyed |
| `references/install-paths.json:34,112` `"reader": "gate_preflight.py"` | reader text must contain the key (`install_paths.py:757-768`) | NO unless the key text stays in the facade -> the part holding it |
| `judgment-census.json` 28 rows (`:314-341`) | file+function | NO |
| tests reading the text: `test_gate_preflight.py:3127,4178,4580`, `test_story_run_gate_repair.py:868` | text | NO (L8) |
| `docs/SIBLING_MAP.md:447` `gate_preflight.py:1946` | file:line | NO |
| door/CLI `gate_preflight.py --task-root ...` (`test_reporter_choice.py:213`) | command | YES |
| branch `origin/held/tr2-9` (19 lines in this file, brief) | — | sequencing only (§11) |

### (f) Mirrors: core/start/stand/s5/reporter/probe/credentials/cases/gate_b: `test_gate_preflight.py` (keep, 5 460 lines);
reporter: `test_reporter_rehearsal.py`, `test_reporter_choice.py`; stand: `test_gate_role_accounts.py`; quarantine:
`test_gate_preflight_extra_accounts.py`, `test_gate_preflight_integrations.py`.

---

## §5 `gate_brief.py` (5 117 lines; prefix `gate_brief_`, cut `functions`)

Verified: 202 top-level functions (`rg -c "^def " gate_brief.py`); markers `:642`, `:1033`, `:1285`, `:3231`, `:3614`, `:3968`;
`CardCtx` `:1567`; `selftest` `:4948`; `main` `:5061`.

### (a) Ranks `[["gate_brief_core"], ["gate_brief_words", "gate_brief_exploratory", "gate_brief_cards"], ["gate_brief_packet_a", "gate_brief_attachments", "gate_brief_reference"], ["gate_brief_packet_b", "gate_brief_gate_b"], ["gate_brief_render"], ["gate_brief_selftest"], ["gate_brief"]]`

| home | range | functions | ~lines | rank |
|---|---|---|---|---|
| `gate_brief_core` | 1-641: judge facts, plan rows, roll call, sources, rehearsal items, stand gap gaps | 25 | 640 | 0 |
| `gate_brief_words` | 642-1032: gate B stand gap words | 24 | 390 | 1 |
| `gate_brief_exploratory` | 1033-1284: exploratory questions answered in words | 12 | 252 | 1 |
| `gate_brief_cards` | 1285-1806: reporter command legs, card building, `CardCtx` | 19 + 1 class | 522 | 1 |
| `gate_brief_packet_a` | 1807-2282: case files, documents, register view, answered/contradiction questions, warnings (no marker: explicit start `case_files` `:1807`) | 19 | 476 | 2 |
| `gate_brief_attachments` | 3231-3613 | 20 | 383 | 2 |
| `gate_brief_reference` | 3614-3829 | 9 | 216 | 2 |
| `gate_brief_packet_b` | 2283-3230: `collect`, question effects, question card, answer forms, head/tail sections (explicit start `collect` `:2283`) | 37 | 948 | 3 |
| `gate_brief_gate_b` | 3968-4947: open before MR, bug rows, `render_gate_b` | 31 | 980 | 3 |
| `gate_brief_render` | 3830-3967: `render`, `project_config`, `_first`, `sizing_line` (explicit) | 4 | 138 | 4 |
| `gate_brief_selftest` | 4948-5060 | 1 | 113 | 5 |
| `gate_brief` (facade) | `main`, `__main__` | 1 | ~70 | 6 |

25+24+12+19+19+20+9+37+31+4+1+1 = 202. The section titled "reporter card command" (`:1285`) also holds generic card
builders (`_card` `:1644`, `stand_gap_card_lines` `:1749`): demotion (rule 4) moves those used by words/exploratory to core.

(b) Importers: lazy `import gate_brief` sites (2.7); census rows 3. (c) none (functions). (d) `gate_brief` imports `controller`
lazily (`:2160`, `:2182`) and `gate_preflight` lazily (`:417`..`:3034`): unchanged in bodies.

(e) Carriers: `judgment-census.json:311-313` (NO); `references/null-outcomes.json:92` (§14 U3); `references/artifact-writers.json:90`
(form not read, §14 U3); `test_gate_brief_and_retro.py` text reads (L8 census); CLI `gate_brief.py --selftest` (YES).
(f) Mirrors: `test_gate_brief_and_retro.py` (keep, 3 545 lines) for all parts; `test_gate_question_form.py`; quarantine
`test_gate_brief_attachments.py`.

---

## §6 `report_facts.py` (4 894 lines; prefix `report_facts_`, cut `functions`)

Verified: 239 top-level functions (`rg -c "^def "`); 12 markers `:90`, `:262`, `:911`, `:1751`, `:1925`, `:2925`, `:3035`, `:4305`,
`:4401`, `:4434`, `:4534`, `:4851`; `main` `:4853`.

| home | range | ~lines | rank |
|---|---|---|---|
| `report_facts_core` | 1-261 small helpers, constants (`RISK_WORDS_PATH` `:60`) | 260 | 0 |
| `report_facts_facts` | 262-910 the facts | 650 | 1 |
| `report_facts_manual` | 911-1750 checked by hand | 840 | 1 |
| `report_facts_measures` | 1751-2924 sides measures + price and use of first look/registry | 1 174 | 1 |
| `report_facts_blocks` | 2925-4304 verdict + blocks (verdict 110 lines joined: closed choice S-4) | 1 380 | 2 |
| `report_facts_file` | 4305-4850 positions, conversion, "Left with you", write/check | 546 | 3 |
| `report_facts` (facade) | `main`, `__main__` | ~45 | 4 |

Per-home function counts: printed by the generator (2.2 rule 6); not counted here (§14 U5). Total 239 must be preserved.
(b) importers through the facade (`import report_facts` sites; AR-13 text names `report_facts.knowledge_use` — valid via facade).
(d) lazy imports of `controller` (`:551`, `:1833`, `:2277`, `:2312`) and `gate_preflight` (`:2105`, `:3096`) stay in bodies.
(e) `judgment-census.json:685-688` (NO); `references/gate-registry.json:657` (NO); text readers (L8). (f) `test_report_facts.py`
(keep, 4 970 lines) for every part; `test_report_manual_counted.py`, `test_report_env.py`.

---

## §7 `story_step.py` (3 388 lines; prefix `story_step_`, cut `functions`)

Verified: 126 top-level functions (list in the trail); markers `:480`, `:691`, `:760`, `:1230`, `:1947`, `:2650`, `:3144`; eager
`from controller import (Controller, MANUAL_BLOCK_CASES, ...)` `:104`; `main` `:3279`.

| home | range | functions | ~lines | rank |
|---|---|---|---|---|
| `story_step_core` | 1-887: helpers, prompt, handoff form, probe debt, run mode, config detector, `config_snapshot`/`config_restore` | 44 | 887 | 0 |
| `story_step_start` | 888-1330: `start`, manual block, dispatch files, committed packet | 12 | 443 | 1 |
| `story_step_bind` | 1331-1514: `materialize`, `bind` | 5 | 184 | 1 |
| `story_step_finish` | 1515-2649: evidence, gaps, halts, exit gate, plan next, `_needs_author`, `finish` | 34 | 1 135 | 1 |
| `story_step_decide` | 2650-3143: `decide`, `pause`, `resume`, card rebuild, launch from where | 22 | 494 | 1 |
| `story_step_card` | 3144-3278: stage card, `card`, `where` | 8 | 135 | 1 |
| `story_step` (facade) | `main`, `__main__` | 1 | ~110 | 2 |

44+12+5+34+22+8+1 = 126. Subcommand dispatch lives in `main` (facade) and names the subcommand functions: the facade imports
them explicitly (2.4). `tests/story_step_common.py` is a test helper, no name clash with `story_step_core`.
(d) each part that names `Controller`/constants imports them from `controller` exactly as `:104` does; `controller` never
imports `story_step` (verified: not in the `from controller`/`import controller` list's reverse — §14 U8 for a full proof).
(e) `refusal_registry.py:581` `SS-needs-author` (operation, guarantor `_needs_author`) -> `story_step_finish` (NO);
`judgment-census.json:822-833` 12 rows (NO); `references/gate-registry.json:598` (NO); text readers `test_words_doors.py:295`,
`test_story_run_refusals.py:464`, `test_probe_not_proved.py:435`, `test_story_step_gate.py:366` (L8); command `story_step.py ...`
in doors, `agent_autobind.py:109`, `test_needs_author.py:187` (YES).
(f) `test_story_step.py` (keep, 60-line stub), `test_story_step_start.py`, `test_story_step_manual_block.py` (keep); quarantine:
`_card`, `_config`, `_decide`, `_finish`, `_gate`, `_materialize`, `_pause`, `_prompt`, `_s5_plan`.

---

## §8 `probe_by_code.py` (8 347 lines; prefix `probe_by_code_`, cut `functions`)

Verified: 318 top-level functions (`rg -c "^def "`); 23 markers (`:228` ... `:6920`); the marker `--- main` sits at `:3976` but
`main` is defined at `:8268`.

| home | range | ~lines | rank |
|---|---|---|---|
| `probe_by_code_core` | 1-466: refusals (`Refusal` `:201`, `ToolRefusal` `:205`), the test | 466 | 0 |
| `probe_by_code_oracle` | 467-889 | 423 | 1 |
| `probe_by_code_mutation` | 890-1218 | 329 | 1 |
| `probe_by_code_languages` | 1219-1506 | 288 | 1 |
| `probe_by_code_locate` | 1507-2023 body, first assertion, factory marker | 517 | 1 |
| `probe_by_code_target` | 2024-2593 | 570 | 2 |
| `probe_by_code_run` | 2594-3544 checks before write, run, reading, row judge, restore | 951 | 2 |
| `probe_by_code_durable` | 3545-3995 durable copy, lock, recovery, binding, the `main` marker block | 451 | 2 |
| `probe_by_code_receipt` | 3996-4806 live receipt, `ProbeCtx` | 811 | 3 |
| `probe_by_code_models` | 4807-5578 alternative reading, model on any reader | 772 | 3 |
| `probe_by_code_report` | 5579-6088 identity, report | 510 | 3 |
| `probe_by_code_walk` | 6089-6552 walk over the plan | 464 | 4 |
| `probe_by_code_aggregate` | 6553-6919 | 367 | 4 |
| `probe_by_code_flip` | 6920-8267 | 1 348 | 5 |
| `probe_by_code` (facade) | `main` 8268-8346 | ~80 | 6 |

Per-home counts: generator (§14 U5); 318 preserved. (e) `judgment-census.json:609-618` 10 rows (NO); `references/gate-registry.json:50,574,575`
(NO); `field-producers.json:73-74`, `detectors.json:370`, `artifact-writers.json:165,169` (§14 U3); `install-paths.json:100` reader text
(NO unless the key stays in the facade); `docs/SIBLING_MAP.md:191,431,447` file:line (NO); text readers
`test_probe_by_code.py:2761`, `test_probe_marker_judgment.py:528` (L8; the latter counts `def judge_record` in the file text — it
must read the family). (f) `test_probe_by_code.py` (keep, 105.8 s — CI), `_alternative` (337 s — CI), `_copy`, `_languages` (103.7 s — CI);
locally only the moved names' scenario rows.

---

## §9 `hooklib.py` (2 789 lines; prefix `hooklib_`, cut `functions`)

Verified: stdlib-only eager imports (`hooklib.py:2-13`); `global` holders `_PROJECT_ROOT_CACHE` (`:71`, `:144`, `:156`) and
`_RUN_FORMS_CACHE` (`:1096`) — the same `rg "^\s+global "` over the other seven files finds none (positive control: the hits in
`hooklib.py`). `_PROJECT_ROOT_CACHE`: 240 occurrences in 76 files (`rg -c`), READ from outside, e.g. `test_bare_calls_live.py:59`,
`guard_pre_tool.py:2648`, `stage_done.py:1466`, `turn_budget.py:385`.

| home | range | ~names | ~lines | rank |
|---|---|---|---|---|
| `hooklib_roots` | 1-500: `PLUGIN_ROOT`, `_PROJECT_ROOT_CACHE` and every `global` holder of it (`project_root`, `pin_project_root`, `selftest_root_restored`), story root, `story_cli`, `append_jsonl_line` | 24 | 500 | 0 |
| `hooklib_read` | 501-858: closure fields, `story_closure`, read helpers, config, `block`, frontmatter | 23 | 358 | 1 |
| `hooklib_runforms` | 859-1110: write markers, run forms, `_RUN_FORMS_CACHE` + `run_forms` | 12 | 252 | 2 |
| `hooklib_shell` | 1111-1694: the shell scanner (`Word`, `Unit`, `_Frame`, `_Reader`, `walk`) | 20 | 584 | 3 |
| `hooklib_bodies` | 1695-2152: heredoc bodies, opaque shell, launch forms | 19 | 458 | 4 |
| `hooklib_guard` | 2153-2394: `needs_guard`, subagent meta, telemetry rotation | 7 | 242 | 5 |
| `hooklib_notices` | 2395-2562: notices and signals | 8 | 168 | 5 |
| `hooklib_version` | 2563-2789: version coherence, `run_stop_hook` | 10 | 227 | 5 |
| `hooklib` (facade) | parts, `install` | 0 | ~30 | 6 |

The roots group shares one part with every holder of its `global`, so the live read of F-1 covers its outside readers. Under
F-1 option (b) this file is NOT cut (75 files would change) — see F-1 and F-7. (b) 327 importing files (brief); many take names
eagerly (`from hooklib import ...`, e.g. `stage_guard.py:78,84`, `refusal_registry.py:54`). Facade import cost: eager parts =
the same bytecode in 8 files; measured before/after in the DoD (AR-12). (d) parts import stdlib and lower parts only; `hooklib`
imports nothing of the package today (`:2-13`), so no cycle is possible. (e) `judgment-census.json:393-398` 6 rows (NO);
`docs/SIBLING_MAP.md:255` `hooklib.py:114` (NO); text/AST readers `test_runtime_paths.py:425` (`_config_names` of the AST of
`hooklib.py`), `test_run_forms.py:868` (`HOOKLIB_PATH`) (NO: read the family); axis 11/16/19/29 survivors named `hooklib.<fn>`
(YES). (f) `test_hooklib_append_jsonl.py`, `test_hooklib_scan.py` (keep), `test_run_forms.py`, `test_project_root.py`; quarantine
`test_hooklib_sorted_paths.py`, `test_hooklib_subagent_meta.py`.

---

## §10 `stage_guard.py` (3 523 lines; prefix `stage_guard_`, cut `functions`)

Verified: module `__getattr__` `:127-131` (lazy `UNRESOLVED_REASONS`); markers `:134`, `:195`, `:281`, `:759`, `:1222`, `:1860`,
`:1938`, `:2896`; `selftest` `:3043-3503`; `main` `:3504`; 140 top-level functions (list in the trail).

| home | range | functions | ~lines | rank |
|---|---|---|---|---|
| `stage_guard_model` | 66-280 constants, `closed_unresolved_reasons`, stage model, optional dispatches (`__getattr__` stays in the facade) | 14 | 215 | 0 |
| `stage_guard_event` | 281-758 reading the event, resolve ticket, resume targets, journal | 23 | 478 | 1 |
| `stage_guard_rules` | 759-1221 the rules, `deny`, `dispatch_errors`, manifest, delivery | 23 | 463 | 2 |
| `stage_guard_shapes` | 1860-2895 command shapes, carried bodies, typed runner, `check_command`, `needs_stage_guard`, `_Slice` | 52 + 1 class | 1 036 | 3 |
| `stage_guard_entry` | 1222-1859 `check`, `check_resume`, `check_dispatch` | 22 | 638 | 3 |
| `stage_guard_cli` | 2896-3042 `explain`, `stories` | 3 | 147 | 4 |
| `stage_guard_selftest` | 3043-3503 | 1 | 461 | 5 |
| `stage_guard` (facade) | `__getattr__`, `main` | 2 | ~40 | 6 |

14+23+23+52+22+3+1+2 = 140. Hook entries `inject_context.py` and `guard_pre_tool.py` call `stage_guard.check` / `check_command`
through the facade (`refusal_registry.py:33-35` docstring) — YES.
(e) `refusal_registry.py:56` `SCANNED = ("stage_guard.py", ...)` and 22 rows `"file": "stage_guard.py"` keyed file+function
(`rg -c`): `sites()` (`:840-852`) reports the file a refusal is in, so SCANNED gains the parts (a production script: the list is
a literal there, FR-44 forbids reading the fixture map at run time) and each row's `file` becomes its home — producer and reader
in one commit (AR-22) (NO); `judgment-census.json:766-783` 18 rows (NO); `test_stage_guard.py` runs `stage_guard.py --selftest`
(YES). (f) `test_stage_guard.py` (keep, 2 236 lines), `test_guard_command_text.py`, `test_resume_story_isolation.py`.

---

## §11 Order, parallelism, nodes

Hot files (PROJECT.md «Командная работа» item 3) among the eight: `hooklib.py`, `stage_guard.py`, `gate_preflight.py`,
`controller.py`. Writing builders at most 6 at once (host adaptation 6).

| order | node | depends on | parallel with |
|---|---|---|---|
| 0 | **B0** facade survivor + generalised layer test + `family` header in `driver-layers.json` | the move tool of spec A exists (R-A1); coordination with spec A on `module_facade.py` (F-5) and on `test_driver_layers.py` (spec A nodes also edit it: `очередь:` line in both) | — |
| 1 | **B-RF** report_facts, **B-SS** story_step, **B-PBC** probe_by_code, **B-GB** gate_brief, **B-SG** stage_guard | B0 | each other (disjoint sources; shared registries by the protocol of spec A, disjoint rows) |
| 2 | **B-HL** hooklib | B0; after wave 1 lands (one importer change at a time is easier to read in CI) | B-GP if ready |
| 2 | **B-GP** gate_preflight | B0; `origin/held/tr2-9` merged into `main` or rebased onto the cut (F-8) | B-HL |
| 3 | **B-CT** controller | B0; `story_run.py` phases of spec A merged (brief) | — |
| 4 | C3-24 (`Controller.validate` by operation, `conductor/batch-3`) | B-CT | — |

Each node, written for a weaker model (PROJECT.md item 11): the file, the ranges, the explicit list and the rule are here; the
direction is chosen; a stop condition is named. Template (filled per node below):

```
node: B-<ID> — cut <file> by its map
given: this spec §2 and §<n>; plans/builder-rules.md; ai-packages/qa-factory/design/factory-rules.md (whole); the move tool of spec A and its protocol
owns:
<absolute paths — below>
non-goals: no behaviour change; no edit of another family; no test-file split (spec C); no repair of a quarantined test; no fix of a defect found (finding instead)
handoff: docs/tasks/handoffs/<task-id>-<ID>.md (report per plans/builder-rules.md item 11 + generator output + importtime lines where named)
edges: §12 E1-E10 as they apply to this file; stop and report if the seam check (§2.2 rule 6) fails or R-A7 refuses
DoD: (1) `python -B ai-packages/qa-factory/scripts/tests/test_driver_layers.py` green incl. the family; (2) the generator's `--draft` output pasted, seam check passed; (3) `python -B -c "import <parts in rank order>, <facade>"` from ai-packages/qa-factory/scripts prints nothing and exits 0; (4) `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>` and the keep files it prints except slow_tests.json > 60 s, green; (5) every row of §<n>(e) marked NO rewritten (grep of the old key returns only rows marked YES; positive control: the same grep on main returns them); (6) `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang`; (7) architecture: line `AR-13, AR-14, AR-15, AR-20, AR-22, AR-29 -- <how kept>` in the commit
```

Per-node `owns` (sources and the family map; shared-registry rows per the protocol of spec A are listed by file, rows of this family only):

- **B0** — `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\module_facade.py` (new);
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_driver_layers.py`;
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\driver-layers.json` (the `family` header only);
  `C:\QAFactory\forge-repo\docs\SIBLING_MAP.md` (axis 18 row: the family maps' exceptions);
  `C:\QAFactory\forge-repo\docs\tasks\critic-diff-brief.md` (question 9 names the new ratchet).
  Witness: `python -B ai-packages/qa-factory/scripts/tests/test_driver_layers.py` (driver family unchanged: 54/54 class result, plus the new
  bad fixtures for L11, L12 and a non-driver family header reported by name); `--witness-for` on the owns.
- **B-RF** — `...\scripts\report_facts.py`; `...\scripts\report_facts_*.py` (new, per §6);
  `...\scripts\tests\fixtures\report_facts-layers.json` (new); rows in `judgment-census.json`, `references\gate-registry.json`,
  `scripts\tests\test-layers.json` (`covers`, `fixture_owners`).
- **B-SS** — `...\scripts\story_step.py`; `...\scripts\story_step_*.py` (new); `...\scripts\tests\fixtures\story_step-layers.json`;
  rows in `refusal_registry.py` (`SS-needs-author`), `judgment-census.json`, `gate-registry.json`, `test-layers.json`.
- **B-PBC** — `...\scripts\probe_by_code.py`; `...\scripts\probe_by_code_*.py`; `...\scripts\tests\fixtures\probe_by_code-layers.json`;
  rows in `judgment-census.json`, `gate-registry.json`, `install-paths.json`, `test-layers.json`; `C:\QAFactory\forge-repo\docs\SIBLING_MAP.md` lines 191, 431, 447 (probe part).
- **B-GB** — `...\scripts\gate_brief.py`; `...\scripts\gate_brief_*.py`; `...\scripts\tests\fixtures\gate_brief-layers.json`; rows in
  `judgment-census.json`, `test-layers.json` (+ `null-outcomes.json`/`artifact-writers.json` if U3 says function-keyed).
- **B-SG** — `...\scripts\stage_guard.py`; `...\scripts\stage_guard_*.py`; `...\scripts\tests\fixtures\stage_guard-layers.json`;
  `...\scripts\refusal_registry.py` (`SCANNED` + 22 SG rows); rows in `judgment-census.json`, `test-layers.json`.
- **B-HL** — `...\scripts\hooklib.py`; `...\scripts\hooklib_*.py`; `...\scripts\tests\fixtures\hooklib-layers.json`; rows in
  `judgment-census.json`, `test-layers.json`; `docs\SIBLING_MAP.md:255`; `...\scripts\tests\test_runtime_paths.py` and
  `...\scripts\tests\test_run_forms.py` (only the file-text reads, if keep). Extra DoD: importtime before/after (AR-12, §12 E10).
- **B-GP** — `...\scripts\gate_preflight.py`; `...\scripts\rehearsal_*.py`; `...\scripts\tests\fixtures\rehearsal-layers.json`; rows
  in `gate-registry.json`, `null-outcomes.json`, `install-paths.json`, `judgment-census.json`, `test-layers.json`;
  `docs\SIBLING_MAP.md:447` (gate_preflight part).
- **B-CT** — `...\scripts\controller.py`; `...\scripts\controller_*.py`; `...\scripts\tests\fixtures\controller-layers.json`;
  `...\scripts\refusal_registry.py` (8 operation rows); `C:\QAFactory\forge-repo\tools\controller-blocks-gen.py`;
  `...\scripts\tests\test_controller_blocks.py`; `...\design\controller-blocks.md`; `...\design\architecture.md` (line 256 only);
  rows in `judgment-census.json`, `test-layers.json`.

(`...` = `C:\QAFactory\forge-repo\ai-packages\qa-factory`; the dispatch writes the full absolute path, R11-f.)

After all nodes: the Lead updates the hot-file list (PROJECT.md item 3) and the `plans/builder-rules.md` line "where a function
lives: read the family map" (brief, Lead's decisions) — not a node of this spec.

---

## §12 Edge behaviours (each with the invariant it protects)

| # | edge | behaviour | invariant |
|---|---|---|---|
| E1 | a name used by two homes of equal rank | mixin homes: legal (through `self`, no import). Function homes: the name is demoted to the rank-0 module (2.2 rule 4); if that breaks the seam check, stop | no import between equal-ranked parts: an import cycle stays unreachable |
| E2 | a class-level constant read through `self` and through the class name | home in `<Class>Base` when read by 2+ homes or by `<Class>.k` from another home; `<Class>.k` becomes `<Class>Base.k`; a class attribute ASSIGNED through the class name (`<Class>.k = v`, `type(self).k = v`) keeps `k` in the facade class body (rule 3); `self.k = v` (instance) is unaffected (`_declarations_read`, `gate_preflight.py:1266`: if set through `self`, Base) | one binding of the class attribute: a reader never sees a stale copy on a mixin |
| E3 | a module-level table mutated at import time, or a global rebound by `global` | mutation at import (e.g. a dict filled by a loop at module level): the table and its filling statements share one home (the statement order inside the part is the original order); a `global` name and every function holding the `global` statement share one part; if they cannot (holders in two ranges), the name and holders are facade-bound | the value every reader sees is the one the original computed, read live through the facade |
| E4 | a function imported by other files AND patched by tests | F-1: the patch writes every binding; nothing to rewrite. Under F-1 (b): the patch target and all bare-global readers must share one module, else the node stops. A class-attribute patch on the split class (`setattr(Controller, m, ...)`) on a member outside Base: the tool refuses (R-A7) and the node reports | a patch keeps today's reach: it can never reach fewer call sites than before |
| E5 | a script also run as `__main__` by hooks or by door text | the entry file name does not move; `main` and the `__main__` block stay in the facade; parts carry no `__main__` block; `module_facade.install` works on the `__main__` module (`run_py_entry.py:87-97`) | FR-37: every path a person or role reads (`controller.py --operation`, `story_step.py finish`, `gate_preflight.py --task-root`, `stage_guard.py --selftest`) is the path the code runs |
| E6 | an embedded `selftest` block (`stage_guard.py:3043-3503`, `gate_brief.py:4948`, `gate_preflight.py:5994`) | goes to `<prefix>selftest.py`, the top function rank; the CLI flag `--selftest` stays in the facade's `main`, which imports it (F-6) | `<file>.py --selftest` and `test_stage_guard.py` keep running the same checks |
| E7 | a name starting with underscore imported across a part boundary | allowed (the tool writes explicit `from <part> import _name`); the facade never imports underscore names it does not use; outside files reaching `<stem>._name` resolve through F-1 | a private name keeps one definition; no outside file imports a part (L11) |
| E8 | the temporal edge: the map file does not exist before the node | before: the family header is absent, the generalised test finds no `<prefix>-layers.json` for the family and asserts that no `<prefix>*.py` part exists (L1 "part without map"); the family node creates the map and the parts in ONE commit with the `fixture_owners` row; after: all checks run. B0 creates the test's family loop, not any family map | a part never exists without its map, and a map never names a part that the facade does not import |
| E9 | a file whose seam does not hold on inspection | the node stops with "do not cut, <reason>" (generator output) — seam check fails, R-A7 refuses, or the importtime rise exceeds +20 %; the Lead decides re-ranking or not cutting | no forced cut: a cut that adds cross-module traffic is worse than none (P11) |
| E10 | hook start cost (`hooklib`, `stage_guard`) | parts imported eagerly, stdlib-only for hooklib; cumulative import time measured before/after in the node; over +20 % is E9 | a hook is never slower to start because of the cut (AR-12) |
| E11 | a name defined twice in the original file (re-definition later in the file) | the census finds it (L2 on the original): the node stops before cutting and reports; the later definition is what runs today, the tool must keep that one | the definition that wins today still wins |
| E12 | `from <stem> import *` | none found is not claimed (not searched); the facade defines no `__all__`, so a star import gives the facade's bound names only — the tool refuses to cut a family with a star importer until the Lead decides | no importer silently loses names |

Error direction of the reused `test_driver_layers.py` in its wider role (it now gates eight more files): it errs toward refusing
(`test_driver_layers.py:10-11`: "an access it cannot resolve fails; it never passes one"); adversarial inputs that must stay on the
safe side: a part with no map row (L1), a facade that defines a moved name (L11), a part imported from outside (L11), an equal-rank
import between function parts (L6 extended to `>=` for function homes), `<Class>.<m>` left in a part (L12).

---

## §13 Forks (recommendation first; a builder follows the recommendation until the Lead answers)

| id | question | options | recommendation, and what the builder does meanwhile |
|---|---|---|---|
| F-1 | facade form | (a) forwarding facade `module_facade.install` (live reads, writes to every binding); (b) binding facade: explicit re-export of every name, test patches retargeted per site, `global`-state groups kept in the facade | (a): no test edits, one survivor, keeps the meaning of every patch; (b) costs ~75 files for `_PROJECT_ROOT_CACHE` alone (§9) and per-site work on 55 `gate_preflight` patches. Builder: (a) |
| F-2 | naming prefix | (a) class name for one-class files, stem otherwise (`driver_`, `controller_`, `rehearsal_`, `<stem>_`) — one rule for nine files; (b) stem for all eight, `driver_` kept as the one exception | (a): (b) is a road-for-one-case under P31 unless the owner words it. Builder: (a) |
| F-3 | ranks of mixin homes | (a) all mixins of a class share one rank; exceptions empty; (b) ranked like the driver with exceptions seeded at map creation and pinned | (a): mechanical, no call-graph judgment needed now; the cost is no layering inside `Controller`/`Rehearsal` until a later node wants it. Builder: (a) |
| F-4 | seam check thresholds | (a) rank-0 <= 35 % of lines and each part keeps >= 60 % of its range's names, as a STOP signal for the Lead; (b) no threshold, the Lead reads the `--draft` output | (a) as a stop, never as an auto-pass. Builder: (a) |
| F-5 | one facade survivor across specs A and B | (a) `module_facade.py` is also the facade of `story_run.py`; created by whichever of B0 / spec A phase 0 lands first; (b) spec A keeps its own form | (a) (P31, AR-15). Needs the Lead to align spec A. Builder of B0: create it unless spec A's already exists, then use that one |
| F-6 | where an embedded selftest lives | (a) `<prefix>selftest.py` at the top function rank; (b) stays in the facade | (a): one rule for three files, and the facade stays thin. Builder: (a) |
| F-7 | cut `hooklib.py` at all | (a) cut, in wave 2, with the importtime gate; (b) do not cut (only 15 open nodes, brief) | (a) only if F-1 = (a); under F-1 (b) recommend (b) not cutting. Builder: (a) |
| F-8 | `gate_preflight.py` and `origin/held/tr2-9` | (a) wait until the branch is merged; (b) cut, then the branch rebases onto the map (its 19 lines land in the home part) | Lead's call (branch state not read here). Builder: does not start B-GP until the Lead names (a) or (b). **ANSWERED — the owner, 11.11.2026: (b) — the branch is one of ours; it is left as it is and rewritten later onto the new modules. B-GP does not wait for it** |
| F-9 | parts private to the family (L11) | (a) no file outside the family imports a part; (b) allow direct part imports (e.g. a hook taking `hooklib_roots` only) | (a) now (AR-13); (b) can be opened later by a data row. Builder: (a) |

## Small choices closed by the designer
- S-1 map file name `<prefix>-layers.json` beside `driver-layers.json` (not a subfolder).
- S-2 mixin base order in the facade class: rank descending, then name, Base last (no lookup depends on it, L2).
- S-3 `controller-blocks-gen.py` rows ordered by (rank, file, line); the rendered text "Rows are in source order" becomes "in
  source order of the family, by the map's ranks".
- S-4 `report_facts`: the 110-line verdict section joins the blocks part.
- S-5 entry-level functions that build the split class stay beside `run`/`main` in the facade (`gate_preflight.py:5754-5993`).
- S-6 counts of names per home are printed by the generator; the spec gives ranges and totals where the definitions were listed.

---

## §14 What this spec did NOT verify

- U1 the call graph between controller mixin homes and between function sections: ranks of function parts are a starting point;
  the generator's demotions decide, the seam check stops a bad cut.
- U2 that `module_facade`'s class swap behaves under every runner in use (pytest is not used here; `harness`, `run_py_entry`,
  `golden_sitecustomize/sitecustomize.py:20` registers modules) — B0's witness must include one run through `run_py_entry`.
- U3 the key form of `references/null-outcomes.json`, `field-producers.json`, `artifact-writers.json`, `detectors.json` rows for
  these files (lines counted, form not read): NO if `file::function`, YES if command/module.
- U4 the state of `origin/held/tr2-9` (git not run in this session).
- U5 per-home function counts for `report_facts.py`, `probe_by_code.py` (totals 239 and 318 verified; per-range lines not listed).
- U6 timings of the keep files per family beyond those quoted from the brief (`slow_tests.json` is the authority in the node).
- U7 whether `test_judgment_census.py` demands a row for `module_facade.py`.
- U8 a full proof that no partner imports `story_step` back into `controller` at import time (only the lists seen above).
- U9 star imports of the eight modules and class-attribute patches on `Controller`/`Rehearsal` (R-A7, E12 make the tool check).
- U10 `env-facts-baseline.json`, `lint-baseline.json`, `dup-baseline.json` rows of these files (integrator's update per spec A).
- U11 the content of spec A (drafted in parallel): R-A1..R-A7 are requirements, not facts about it.
- U12 the door-text count (~116 lines in 26 scripts) and importer counts (187/70/327) are the brief's, not recounted.

## Reading trail
Read whole: `docs/tasks/specs/td-11-lead-brief.md`; `scripts/tests/test_driver_layers.py`; `tools/controller-blocks-gen.py`.
Read in part: `driver-layers.json:1-12,1205-1234`; `stage_guard.py:1-134`; `gate_preflight.py:1258-1317,5754-5788`;
`driver_chains.py:1-30`; `refusal_registry.py:30-69,895-934`; `install_paths.py:745-779`; `scenario_walk.py:833-927`;
`test-layers.json:1-32,880-909`; `test_controller_state.py:1922-1956`; `judgment-census.json:3-4`; `architecture.md:140-229`;
`SIBLING_MAP.md:383-394,579-590`; `plans/builder-rules.md:14-83`; `gate-registry.json:8-17,288-297`;
`plans/piles/driver-hosts/findings/20261017-controller-ostatki-c4-10.md` (headings). Greps (ripgrep): section markers, `^def`,
`^    def`, `^class` of all eight files; importers `from controller import|import controller`, `import gate_preflight`; module patches;
`global`; `__file__`; `_PROJECT_ROOT_CACHE`/`_RUN_FORMS_CACHE`; `"file": "<eight>.py"` in `refusal_registry.py` and
`judgment-census.json`; references/*.json mentions; `file:line` carriers in `design/` and `docs/SIBLING_MAP.md`; keep/quarantine rows in
`test-layers.json`; Glob of `<stem>_*.py`, `rehearsal*.py` (controls: `driver*.py`).
Needed beyond the manifest: `refusal_registry.py` scan logic, `install_paths.py`, `scenario_walk.py`, `run_py_entry.py`,
`runtime_paths.py`, `test-layers.json`, `judgment-census.json`, `gate-registry.json`, `driver_chains.py`, `hooks/hooks.json`.
