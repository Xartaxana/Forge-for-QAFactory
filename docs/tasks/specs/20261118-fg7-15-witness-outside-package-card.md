# FG7-15 — `--witness-for` answers for paths outside the package (draft card)

task: t-1411 | node: forge/7/FG7-15 | feature: F19 | designer draft, 18.11.2026 | status: DRAFT, forks F1-F5 open for the Lead
Finding: `plans/piles/forge/findings/20261111-svidetel-dlya-putej-vne-paketa-odin-put.md` (t-013 F5; P31, AR-1, AR-13, FR-41).

## §0 Target on main, measured (file:symbol)

- `ai-packages/qa-factory/scripts/tests/scenario_walk.py::witness_for` (lines 891-947 at read time) is the one witness road.
  `::_relative` strips everything up to `ai-packages/qa-factory/`; a path with no marker is kept whole and then joined
  to the PACKAGE (`absolute = package / rel` when not absolute). `::main` takes `--witness-for PATH...` (argparse
  `nargs="+"`, required), prints the lines, exits 0.
- TODAY for an outside path (read from the code; the probe is the Lead's, I have no shell — `estimate, not verified`:
  `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for tools/wave.py`): relative `tools/wave.py`
  becomes `<package>/tools/wave.py`, which does not exist -> `tools/wave.py: deleted or absent on disk, counted as changed`
  (FALSE: the file exists), then `not a script of scripts/...`, then `no scenario or keep row covers tools/wave.py: the
  whole scenario layer judges it (canon), nothing to run locally` + one canon line per `test_scenario_*.py` (6 files on
  disk, Glob `ai-packages/qa-factory/scripts/tests/test_scenario_*.py`, incl. `test_scenario_walk.py` and
  `test_scenario_world.py`), last line `run locally: 0 file(s); canon judges: 6 file(s)`. An absolute `C:/.../tools/wave.py`
  skips the "absent" line and prints the same false "scenario layer judges it". The real witness `tools/test_wave.py`
  is never named. This is the defect.
- `::witness_for` line 902-903: `layers is None` -> `selftest.test_layers()` with NO path (reads the running package's
  file, ignoring the `package` argument); `selftest.test_layers` raises `TestLayersError` on a malformed file
  (`selftest.py::test_layers`, lines 635-656) and `witness_for` does not catch it -> a traceback, no line at all.
  `selftest.canon_class` already catches and notes (lines 659-680). Absent file: handled (line 917-918).
- Forge test inventory (Grep tool, `pattern "." path tools, type py, glob "!**/test_*"`, files_with_matches -> 86 files;
  same with glob `test_*.py` -> 123 files, 122 top-level + `tools/tests/test_role_carriers_one_owner.py`):
  - four top-level `test_*.py` are TOOLS (`main()`, no `def test_`): `test_quarantine.py`, `test_split.py`,
    `test_redundancy.py`, `test_volume.py` (Grep `argparse|def main|^def test_` over them). Tool modules: 86 + 4 = 90.
  - exact partner `tools/test_<stem>.py`: 80 of 90 (76 of the 86 + the 4 `test_*` tools via `test_test_<x>.py`);
    `controller-blocks-gen.py` pairs only by dash->underscore (`test_controller_blocks_gen.py`): 81 of 90.
  - no partner (9): `conftest`, `piles_testkit`, `under_test`, `no_reaper_wrap` (test kits), `journal_lock`,
    `session_proc`, `coordinator_rules`, `ci_read_common` (libraries), `source_split` (Glob of their partners: none;
    positive control `tools/test_{wave,...}.py` found `test_wave.py`; `source_split` named by no test file: Grep
    `story_capture|source_split|source-split` -i over `tools/test_*.py` found only `test_story_capture.py`).
  - FAMILY files `test_<stem>_<suffix>.py` judging the same tool: 9 tools — `journal_echo` (4), `piles` (10;
    `test_piles_split.py` belongs to `piles_split`), `session_context` (3), `owns_gate` (2), `journal_validator` (2),
    `dispatch_gate`, `mechanism_gate`, `negative_lint`, `claim_control_gate` (1 each). All 11 `test_piles_*.py` name
    `piles.py`/`import piles` (Grep count, 11 files).
  - direct importers among `tools/test_*.py` of the 9 partner-less modules (Grep `^\s*(import|from)\s+(<the 8 names>)\b`):
    `journal_lock` 3, `session_proc` 3, `coordinator_rules` 2, `under_test` 5, `no_reaper_wrap` 3, `piles_testkit` 16;
    `ci_read_common`, `conftest`, `source_split` 0. Many forge tests load their tool by PATH (`load_under_test`), so an
    import scan alone misses them; the name rule does not.
- Other outside places: `.githooks/` holds 5 hook files, no test beside them; root `scripts/`, `.claude/hooks/` and
  `ai-packages/qa-factory/tools/` hold nothing (Glob `{scripts/*,ai-packages/qa-factory/tools/*,.githooks/*,.claude/hooks/*}`,
  only `.githooks` hits). So no relative path is physically in both the package and `tools/` today.
- Rules that state the reservation this node removes: `COORDINATOR.md` rule 4 line 153 ("an owned path outside the
  package, where that command has no row: the test file that judges the path, named in the DoD"); `docs/TESTING.md`
  lines 108 and 255-256; `tools/owns_readers.py` docstring KNOWN MISSES 1 ("for a package path").
- Analog: spec `docs/tasks/specs/20261116-spec-facts-by-code-spec.md` §1 C6 / §2.7 / F-11: node C6 converges
  `owns_readers` and `--witness-for`; F-11 recommended that a package file never names a forge tool (the release copies
  `ai-packages/qa-factory/` only). This card stays inside both: it answers WHAT TO RUN, and names no forge path in the package.

## §1 Architecture

Touches `ai-packages/qa-factory/` (a `scripts/tests/` helper; it ships with the package).

- AR-1 (closed variety is data): KEPT — no list of tool names, folders or exceptions enters the code; the pairing is the
  dev-test naming convention `test_<stem>.py` the package already uses (`test_scenario_*.py`, selftest's `test_*.py`).
  Change check (DoD key K4): `scenario_walk.py` contains no literal `tools/` or `.githooks` (Grep; positive control:
  the same Grep finds `scripts/`).
- AR-4 (no machine or layout tie): KEPT under F3 (a) — a relative outside path is resolved against the caller's working
  directory (a parameter in the API), never by assuming the package sits two levels under a repository root; printed
  paths are shown relative to that root or as given. Change check: a test row with paths under a temp dir, no drive letter.
- AR-13 (one reader): KEPT and tightened — `test-layers.json` is read only through `selftest.test_layers(<path>)`, now
  given `package/scripts/tests/test-layers.json`; the canon class only through `selftest.canon_class`. Change check:
  Grep `scenario_walk.py` for `json.loads` near `test-layers` -> none new.
- AR-15 (one survivor): KEPT — `witness_for` stays the one answer to "which tests judge this path"; the outside branch is
  inside it, `_imports_of` is reused for importers. No second command, no wrapper tool. Change check: no new
  `def` answering a run list outside `witness_for`'s module.
- AR-29: the change alters ONE check-like unit, `witness_for`'s outside branch: owner **data (code)** — it reports which
  files exist and import a stem; class **shape/presence**; it is ADVICE for the dispatcher (the dispatch gate refuses
  `--witness-for` inside a DoD, `tools/dispatch_manifest.py` R1), never a refusal. Census: n/a — the census covers
  `scripts/*.py` outside `scripts/tests/` (AR-29 Detector text).
- Error direction (advice reused in a more visible role): `witness_for` may err only toward NAMING TOO MANY files (a
  family or importer over-match costs a builder seconds) and toward "no witness" (the batch canon judges); it must never
  name a file that does not exist, never print the false "whole scenario layer judges it" for an outside path, and never
  move a forge test under the package canon header. Adversarial inputs that must stay on the safe side: a stem that is a
  prefix of another (`piles` / `piles_split`), a tool named `test_*`, a dash stem, a folder path, a data file, a path in
  a worktree copy, a deleted path, a relative path whose first segment is a package folder.
- `variety: none -- a developer witness helper under scripts/tests/ that no stage of a user project runs; its paths are the repository's own, not a project's`
- Commit lines: the builder writes `architecture:` (AR-1, AR-4, AR-13, AR-15, each with how it is kept) and `judgment:`
  in the forms `tools/architecture_gate.py` owns (its docstring, items 1 and 6); the judgment line is the `none` form
  with its reason: the helper prints a run list for a dispatcher and judges or refuses no role output.

## §2 Design (as recommended in F1 (a), F2 (c), F3 (a))

One function, one road: `witness_for(paths, package=None, layers=None, door_modules=None, canon=None, root=None)`.
`root` = where a relative OUTSIDE path is resolved; `None` = `Path.cwd()` (CLI). Per given path:

1. CLASSIFY (before every existing step). A path is a PACKAGE path when (i) its `/`-normalised text contains
   `ai-packages/qa-factory/`, or (ii) it is absolute and lies under `package`, or (iii) it is relative and its first
   segment is an existing top-level entry of `package` (read from disk, no list). Everything else is OUTSIDE.
   A package path takes today's steps unchanged, byte for byte.
2. OUTSIDE path: `absolute` = the path if absolute, else `root / path`; `shown` = relative to `root` when under it, else
   the given text with `/`. Missing on disk -> today's line `<shown>: deleted or absent on disk, counted as changed`
   (the steps below still run on its folder). Stem = file stem with `-` read as `_`. In the path's OWN folder:
   a. NAME: `test_<stem>.py` exists -> hit `<shown>: <test shown> (test_<stem>.py beside it)`.
   b. FAMILY: every `test_<stem>_*.py` in that folder whose longest owning stem is `<stem>` (owning stem of `test_X.py`
      = the longest stem S of a `*.py` in the folder with X == S or X starting `S_`) -> hit `(... family of <stem>)`.
   c. SELF: the path itself is named `test_*.py` and a+b found nothing -> it is its own witness, hit `(the test itself)`.
   d. IMPORTERS (only for a `.py`, only when a-c found nothing): every `test_*.py` in that folder whose `_imports_of`
      names `<stem>` -> hit `(imports <stem>)`.
   e. NOTHING: one line `no witness for <shown>: no test_<stem>*.py beside it and no test beside it imports it; the batch
      canon judges it` (FR-41: unknown is said, never a fact). A folder path: `no witness for <shown>: a folder`.
   Outside hits go to the RUN block and its count, keyed by their shown path (never by bare name), and never through
   `is_canon` (the package canon data classifies only package tests). The outside branch never consults keep rows or
   stories and never prints `not a script of scripts/` or the "whole scenario layer" line.
3. `layers is None` -> `selftest.test_layers(package / "scripts" / "tests" / "test-layers.json")`; `TestLayersError` ->
   one line `test-layers.json could not be read (<reason, 120 chars>): no keep row is consulted`, keep = {}; the walk goes on.
4. Docstring (line 14) gains one sentence: a path outside the package is answered by the test files beside it. No
   forge path is named (F-11 spirit). Exit code stays 0 in every case.

## §3 Edges, each with its invariant

| # | input / limit | behaviour | invariant it protects |
|---|---|---|---|
| E1 | outside path with no test (any rule) | the `no witness for` line; nothing else for it | a path is never silent and never gets a false witness (FR-41) |
| E2 | path in both worlds (relative `scripts/x.py` while a root `scripts/x.py` exists; a marker path naming a non-existent `ai-packages/qa-factory/tools/x.py`) | package classification wins (marker, then first package segment) | every package path keeps today's answer byte-identical; a forge path that collides is given absolute (R11-f owns are absolute) |
| E3 | `test-layers.json` absent | today's line `test-layers.json is absent...`; outside answers in full | the absent world is said; outside answers never depend on the package registry |
| E4 | `test-layers.json` malformed/unreadable | the new `could not be read` line, keep = {}, exit 0, no traceback | an unreadable registry is said, never silent, never stops the walk |
| E5 | empty path list | CLI: argparse refuses (exit 2), unchanged; API `witness_for([])` returns only the count line (0/0) plus today's header notes | an empty request never yields a witness |
| E6 | stem prefix of another (`piles` vs `piles_split`) | a test goes to the LONGEST owning stem only | a family hit never names a test of a different module |
| E7 | tool named `test_*` with a `test_test_<x>.py` partner | the partner (rule a); the tool is not its own witness | a tool with no tests in it is never handed to a builder as a test run |
| E8 | plain forge test file changed (`tools/test_wave.py`) | itself (rule c) | a changed test is run, never reported "no witness" |
| E9 | dash stem (`controller-blocks-gen.py`, `.githooks/pre-commit`) | `-` read as `_` for the pairing only; shown as given | a pairing is never lost to spelling; the shown path is the given one |
| E10 | data or non-`.py` outside file (`tools/owns_readers.json`) | rules a-b by stem; no importer scan; else `no witness` | data readers are never guessed from imports |
| E11 | outside path in a worktree copy (absolute under `.claude/worktrees/...`) | its own folder is searched | the witness is read from the bytes the builder changed, not from the main checkout |
| E12 | deleted outside path | today's "deleted" line + rules a-b on its folder | a deletion is counted as changed and its test still runs |
| E13 | forge test whose bare name equals a package slow key or `canon_only` glob | stays in the run block | package canon data never classifies a forge test |
| E14 | `piles_testkit`-like helper with many importers (16) | all are printed, uncapped (no new limit) | over-naming is the allowed error direction; no silent truncation |
| E15 | relative outside path, CLI started outside the repo root | resolved against the cwd -> absent -> "deleted" + `no witness` | a wrong root says so, never invents a witness |

## §4 Builder card (one card; owns as under F1 (a), F2 (c), F3 (a))

given: C:/QAFactory/forge-repo/docs/tasks/specs/20261118-fg7-15-witness-outside-package-card.md (this spec §0-§3), C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/scenario_walk.py::witness_for, ::_relative, ::_imports_of, ::main, C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/selftest.py::test_layers, ::canon_class, ::TestLayersError, C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_scenario_walk.py::witness, ::package_tree, C:/QAFactory/forge-repo/docs/TESTING.md
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/scenario_walk.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_scenario_walk.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/changelog.d/forge-fg7-15-witness-outside-package.md
non-goals: no edit of test-layers.json (F1 (a)); no rule text (COORDINATOR.md, docs/TESTING.md, agents, owns_readers.py docstring: F4); no forge canon class (F5); no change to package-path answers; no new test file; no cap on printed hits
handoff: a commit on the node branch with the `architecture:` and `judgment:` lines (§1), and the builder report (rule 7 of .claude/agents/builder.md) carrying the witness tail, the red-before line and the K1-K5 results
edges: E1-E15 of §3, inline: no-test outside path -> `no witness for` line; both-worlds path -> package wins; test-layers absent -> today's line; unreadable -> `could not be read` line, keep {}, no traceback; empty list -> argparse exit 2 / API count line only; longest stem owns a family test; `test_*` tool -> its partner; changed test -> itself; dash read as underscore for pairing; data file -> name rules only; worktree path -> its own folder; deleted -> counted and paired; forge test never through is_canon; importers uncapped; wrong cwd -> absent + no witness
DoD: `python -B ai-packages/qa-factory/scripts/tests/test_scenario_walk.py` and `python -B ai-packages/qa-factory/scripts/selftest.py --lang`
siblings: scenario_walk --witness-for is the one witness road (extended in place, no second command); tools/owns_readers.py answers what must not break (unchanged; convergence is node C6); tools/dispatch_manifest.py R1 keeps refusing --witness-for inside a DoD (unchanged)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261118-fg7-15-witness-outside-package-card.md

Acceptance keys (verbatim, checked by the critic against the diff):
- K1 every existing `witness_rows` row of `test_scenario_walk.py` passes unchanged (package answers byte-identical).
- K2 an outside path is never resolved against the package and never gets the "whole scenario layer" line.
- K3 the `test:` rows below exist as rows of the existing `witness_rows` table (one fixture tree, built once).
- K4 `scenario_walk.py` holds no literal `tools/` or `.githooks` (Grep with a positive control on `scripts/`).
- K5 `red-before:` the row T1 run before the code change, red on its assertion (docs/TESTING.md «Тест может упасть»).

test: (rows of `witness_rows`, strongest first; a fixture `forge_tree()` beside `package_tree()` with `tools/a.py`,
`tools/test_a.py`, `tools/test_a_md.py`, `tools/a_b.py`, `tools/test_a_b.py`, `tools/lib.py`, `tools/test_user.py`
(`import lib`), `tools/lone.py`, `tools/test_q.py` + `tools/test_test_q.py`; `root=` the temp dir)
- T1 outside path with its named test -> `tools/test_a.py` in the run block, counted `run locally: 1`, no "whole scenario layer" line (the defect; red before)
- T2 outside path with no test and no importer -> `no witness for tools/lone.py` and `run locally: 0`
- T3 family by longest stem: `tools/a.py` names `test_a_md.py`, not `test_a_b.py`; `tools/a_b.py` names `test_a_b.py`
- T4 importer fallback: `tools/lib.py` -> `test_user.py (imports lib)`
- T5 `test_*` tool and plain test: `tools/test_q.py` -> `test_test_q.py`; `tools/test_a.py` -> itself
- T6 both worlds: relative `scripts/c.py` with a `scripts/c.py` + `scripts/test_c.py` under `root` -> still `test_scenario_demo.py`, no outside line
- T7 unreadable test-layers.json (a broken file in the temp package, `layers=None`) -> the `could not be read` line and the outside answer, no exception
(The builder writes them top-down until its test lines reach its code lines and reports the rest as not written.)

## §5 Readers of every touched file

The `owns_readers` block was NOT attached (`facts: none`); I have no shell. The plan critic runs
`python -B tools/owns_readers.py --paths ai-packages/qa-factory/scripts/tests/scenario_walk.py ai-packages/qa-factory/scripts/tests/test_scenario_walk.py "ai-packages/qa-factory/changelog.d/forge-fg7-15-witness-outside-package.md (new)" --names witness_for _relative main --readers`
(Q13 (d)). Hand grep meanwhile (Grep tool, case-sensitive, positive control = the owned file itself hits):
`scenario_walk|witness_for|witness-for` over `tools/` -> 20 hits in 9 files; `scenario_walk` over the package -> 78 in
20 files; `witness_for|--witness-for` over package `scripts/` -> 34 in 8 files; `scenario_walk` over `.githooks/**`,
`.claude/hooks/**`, `.claude/agents/**`, `.github/**`, `CLAUDE.md`, `PROJECT.md`, `COORDINATOR.md` -> 3 files.

| touched file / name | reader | status |
|---|---|---|
| `scenario_walk.py::witness_for` | `test_scenario_walk.py` (16 hits) | changes in this card |
| same | `tools/dispatch_manifest.py` R1 + `tools/test_dispatch_manifest.py:1342` (the string `--witness-for` in a DoD) | unchanged |
| same | `tools/source-split-carriers.json` row 6 (expects `no scenario or keep row covers` absent for package path `scripts/driver_s0.py`) | unchanged (package answers byte-identical, K1) |
| same | `tools/owns_readers.py` docstring KNOWN MISSES 1 and §2.7 split | unchanged by this card; text stale-ish -> F4 |
| same | `COORDINATOR.md` rule 4 (153), `docs/TESTING.md` (95-108, 146, 255-256), `.claude/agents/builder.md:50`, `.claude/agents/critic.md:309` | unchanged by this card; reservation removal -> F4 |
| same | `tools/install_parity_anchors.json:63` (anchor `scenario_walk.py --witness-for <owns>` in COORDINATOR.md) | unchanged; F4's text node must keep the anchor phrase |
| `scenario_walk.py` (module) | `tools/story_capture.py` + `tools/test_story_capture.py` (import by path: `GATE_ACTIONS`, `QUESTION_KINDS`) | unchanged (names untouched) |
| same | `tools/test_quarantine.py:951-955` (`results_for`) | unchanged |
| same | package: `test_scenario_{cart_1,dry_1,local_1_0108,local_1_arm_b}.py` (`run`), `dry_world.py`, `dry_stub.py`, `dry_exits.py`, `test_controller_doors.py`, `test_acceptance_semantics.py`, `test_stage_acceptance_consumer.py`, `stage_done.py`, `acceptance.py`, `test_field_producers.py` (walk machinery or name mentions; none calls `witness_for`: the `witness_for` Grep found only `scenario_walk.py`, `test_scenario_walk.py`, `test-layers.json` and `witness_form` substrings) | unchanged |
| same | `test-layers.json` keep row `test_scenario_walk.py` (covers `tests/harness.py`, `tests/scenario_walk.py`) | unchanged |
| `test_scenario_walk.py` | `test-layers.json` keep row (listing); selftest collection | unchanged (no rename) |
| `changelog.d/<new>.md` | the release assembly of `CHANGELOG.md` from `changelog.d/` (PROJECT.md:194) | new fragment, English only (`--lang`) |
| `selftest.test_layers` (called with a path now) | its other callers | unchanged (signature already takes `path`) |

## §6 Test cost (docs/TESTING.md «Бюджет», «Строка теста в DoD»)

- No new file: T1-T7 are rows of the existing `witness_rows` table in `test_scenario_walk.py` (keep row, layer
  `scenario`; not in `slow_tests.json` (Grep: no `test_scenario_walk` key) and not a `canon_only` glob) + one fixture
  builder of ~12 lines. Code estimate ~45 lines; seven rows fit under it.
- Witness: the one file above + `selftest.py --lang` (the package text grows); no forge test runs (no forge file changes).
- Internal boundary, no adversarial battery: the input is a dispatcher's own owns list (a CLI used by the Lead), not
  outside input in the TESTING.md sense; the adversarial set of §1 is covered by T3, T5, T6, T7 and E-rows. If the Lead
  reads the CLI as outside input, the battery (magnitude, nesting, encoding, empty) is a fork, not a silent omission.
- Platform: rows use temp-dir paths (no drive letters, `/` and `\` both via `Path`); the POSIX run is CI's.

## §7 Forks (returned, not decided)

- **F1 Where the outside rule lives.** (a) a computed rule inside `witness_for`: the tests beside the path; no data row,
  no forge path in the package [RECOMMENDED: 81 of 90 tool modules pair by name, the family and importer rules cover
  the rest but 3; the finding's "exceptions are data rows" then needs no row today; F-11 spirit kept]; (b) an `outside`
  mapping key in `test-layers.json` — ships forge paths in the package, needs `selftest.layers_problems` and
  `test_layers` to carry the key (AR-13: one reader) and `tools/test_quarantine.py`'s writer to leave it alone: ~3 more
  files; (c) a forge map `tools/<x>.json` read by the package by path — the package reads a forge file (against F-11).
  A wrapper forge tool calling `witness_for` is not offered: a second road (P31, the siblings line).
- **F2 The pairing rule.** (a) exact `test_<stem>.py` only: 81/90, the family files of 9 tools missed (e.g. 10 of 11
  `test_piles_*`); (b) exact + family by longest stem; (c) (b) + direct importers when (b) finds nothing [RECOMMENDED:
  "no witness" falls from 9 to 3 (`conftest`, `ci_read_common`, `source_split`); cost: over-naming for `piles_testkit`
  (16), and importers overlap `owns_readers`' reader list — answered as "what to run", §2.7 split kept].
- **F3 Relative outside paths.** (a) resolved against the cwd (CLI convention; `root=` in the API) [RECOMMENDED: AR-4,
  works in a worktree]; (b) against `package.parents[1]` — a layout assumption in a shipped file, wrong in an installed
  copy.
- **F4 The rule texts after the node** (finding item 4): `COORDINATOR.md` rule 4 line 153, `docs/TESTING.md` 108/255-256,
  `tools/owns_readers.py` KNOWN MISSES 1, `.claude/agents/critic.md:309`. (a) a separate text node with its own owns in
  the same batch, after this card merges, keeping the `install_parity_anchors.json` anchor phrase [RECOMMENDED: Lead and
  coordinator files, another owner tier]; (b) widen this card's owns — mixes a package commit with coordinator rules.
- **F5 A forge canon class.** Forge tests have no slow/canon data, so every forge hit lands in the run block, even a
  slow or platform-bound one (TESTING.md line 134). (a) not now; a node when a forge slow file is measured [RECOMMENDED];
  (b) a forge data row read by `witness_for` — a package reading forge data (against F-11).
- Observation for the Lead (not widened): `_scenarios` globs `test_scenario_*.py` and so counts `test_scenario_walk.py`
  and `test_scenario_world.py` as "scenarios" with no story (the no-hit canon list names them). Package-path behaviour;
  outside this node's reach by its non-goal "no change to package-path answers" — a finding if the Lead wants it.
- Observation: `tools/owns_readers.py` docstring names 2 tools called `test_*`; measured 4 (`test_redundancy.py`,
  `test_volume.py` too). Another pile's file — a one-line finding if wanted.

## §8 Small choices closed by the designer

- `-` read as `_` in the pairing (precedent: `_scenarios` matches story folders by `name.replace("-", "_")`).
- `test_layers` gets the package's own path (the `package` argument was ignored for this read; `canon_class` already
  honours it) — same default world, testable with a temp package.
- An unreadable `test-layers.json` becomes a line, not a traceback (mirrors `canon_class`, which notes and never refuses).
- Outside hits keyed by shown path in the count set (no collision with package bare names).
- Hit lines name the rule that found them (`beside it` / `family of` / `the test itself` / `imports`) so the reader can
  judge an over-match; the order within a path: a, b, c, d.
- Changelog fragment name `forge-fg7-15-witness-outside-package.md` (form of the FG7-63 fragment).

## §9 Reading trail

- Read: batch file row FG7-15 and queue line 13 (Grep); the finding (whole); `scenario_walk.py` 1-86, 830-959;
  `selftest.py` 635-689 (+ Grep 87-89, 577); `test_scenario_walk.py` 40-69, 460-492; `test-layers.json` 1-40, 5308-5321;
  `docs/TESTING.md` 88-157, 225-269; `design/architecture.md` 1-125, 173-222; `tools/owns_readers.py` 1-75;
  `tools/owns_readers.json`; `tools/source-split-carriers.json` 18-25; `COORDINATOR.md` 148-157; `builder.md` 46-53;
  spec 20261116-spec-facts-by-code-spec.md 322-331, 712-719 (+ Grep C6/L9/F-11); `test_files.py` 1-64 (AR-15 check:
  it answers "is this a project's test file", per consumer — not the pairing asked here; no reuse owed);
  `architecture_gate.py` (Grep of its forms); changelog.d FG7-63 fragment.
- Counts and their carriers: §0 (Grep/Glob calls named inline). Negative claims carry a same-shape positive control
  (`tools/test_wave.py` for the partner Glob; `test_story_capture.py` for the `source_split` Grep; `.githooks` for the
  outside-places Glob).
- Not measured (no shell): the live `--witness-for tools/wave.py` output (§0, labelled estimate, command given); the
  owns_readers block (§5, command given).
- needed beyond the manifest: `selftest.py`, `test_scenario_walk.py`, `design/architecture.md`, `tools/owns_readers.py`,
  `tools/owns_readers.json`, `COORDINATOR.md`, the 20261116 spec (read-only).

## §10 Lead decisions (18.11, Lead 501cb4e0, accepted)

- F1: (a) a computed rule inside `witness_for`; no data row, no forge path in the package.
- F2: (c) exact name + family by longest stem + direct importers when nothing else is found; over-naming is the allowed
  error direction (E14).
- F3: (a) relative outside paths resolve against the cwd (`root=` in the API).
- F4: (a) the rule texts (COORDINATOR.md rule 4, docs/TESTING.md, owns_readers.py KNOWN MISSES, critic.md) are a separate
  Lead text node after this card merges.
- F5: (a) no forge canon class now.
- The two observations (scenario glob counting test_scenario_walk/world; owns_readers docstring count) are not widened.
The builder card of §4 stands as written.
- Round 2 (critic t-1417 W2, option b): a relative path whose top folder exists neither in the package nor under root stays a package path. E15 changes with it: a wrong cwd now gets the package answer (deleted + the whole scenario layer), not `no witness`. Accepted: the invariant "never invents a witness" holds, since the whole layer is the over-naming direction E14 allows, never a narrower list.
