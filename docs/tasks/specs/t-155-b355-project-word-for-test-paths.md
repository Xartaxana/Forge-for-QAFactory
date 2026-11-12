# t-155 — B-355: five more usual test names as a HINT; where the project recorded its word, only the record decides — DRAFT SPEC (attempt 2)

Designer (Opus), 12.11.2026, fix round after critic on plan t-160 (verdict: 1 blocker, 6 must, 5 minor). Draft for Lead acceptance;
new forks are returned in §6, never decided. Owner's new idea (PROJECT.md "Как разрабатывается новая идея владельца", step 5).
Sources: finding `plans/piles/onboarding-hooks/findings/B-355-markery-testovykh-putey-references-test-path.md:13` (decision), `:15`
(clarification), `:17` (F-3 = (b) "Нет, только запись", 12.11.2026); Lead decisions on the verdict (dispatch of t-155 attempt 2);
critic t-160. PKG = P = `C:\QAFactory\forge-repo\ai-packages\qa-factory`. Every `path:line` was READ in this turn or in attempt 1 on
`main` (631a427 / 6915cc0) unless marked UNVERIFIED; facts taken from t-160 without re-reading are marked "(t-160)".

Lead decisions this draft applies (not re-opened): F-1 (a) `_tests` -> `dir_suffixes`; F-2 (b) the usual names run in the verdict only
where nothing is recorded; F-3 (b) owner's word; F-4 (a); F-5 (a); F-6 (a) with today's condition kept exactly (t-160 minor 9); F-7 (a);
F-8 (a); F-9 (a); F-10 (a). The values of F-1, F-4..F-10 are the attempt-1 recommendations as reviewed by t-160 (the journal line
t-160 says "Lead decided F-1, F-2, F-4..F-10" without the values) — the Lead confirms at acceptance. Blocker decision: "recorded" is
scoped PER AREA (application checkout vs test repo / project root); a carrier counts only for paths inside the area it names.

## Digest

The verdict leaf exists: `test_locations.is_test_path(path, cfg, base, root)` reads the project's word (steps 2/2b) and falls to the usual
names (step 4); `test_files.is_test_for` / `file_kind` answer per consumer. B-355: (1) five names join the hint list; (2) ONE predicate,
`test_locations.recorded`, answers "did the project record where its tests are, FOR THE AREA THIS PATH LIES IN" — the application area
(inside `app_root`) has one carrier, `test_locations`; the project area (inside the project root, outside `app_root`) has `run.levels`,
`profiles[].roots.test`, `tests_root`; (3) where the path's area is recorded, the usual names decide nothing — not in the verdict, not in
the commit guard, the write-window claim or `test_code` (owner F-3 (b)); where it is not, every reader behaves EXACTLY as today; (4) the
ten blind sites pass the project's word plus the checkout a diff path is relative to, through ONE survivor `handoff_check.diff_checkout`,
and keep their today call as the fallback for the nothing-recorded world; (5) onboarding always records a decision and asks for the test
FILE shape where helpers sit beside tests; the doctor names an old project whose word is missing, does not cover the suggested places,
or cannot reach a configured checkout. No new config key; no new writer.

**Behaviour that changes (everything else byte-for-byte as today):**
1. `dir_names` gains `__test__`, `testing`, `integration`, `fixtures`; `dir_suffixes` gains `_tests`.
2. A path whose AREA is recorded: the usual names never make it a test or a commit trigger or a window claim; only the record does
   (verdict, `commit`, `test_body`, `test_code`). `production` keeps the names only as a narrowing inside a recorded place (F-12).
3. The blind sites read the word through the checkout the path is relative to; a diff with no findable checkout under a project that
   recorded a word anywhere -> each consumer's declared unknown (production counted, the S2 refusal names cause and door).
4. The S5/S1 rehearsal pick and the onboarding inventory move off `name`/`test_body` to `test_place` in a recorded area (G3 fixed).
5. Onboarding asks topic 1c always; the doctor gains one advice row.

---

## §0 Facts (read this turn unless marked)

- F-1 `references/test-path-markers.json:3` `dir_names` = `test, tests, __tests__, spec, specs, e2e, test-harness`; `:4` `dir_suffixes` =
  `.tests, .test`; `:9` `classic.folders`; `_comment` (:2) "a SUGGESTION and a FALLBACK" (attempt 1).
- F-2 Pins: `scripts/tests/test_protected_test_path.py:307-313` (exact lists), `:130-135` (loops) (attempt 1). keep (`test-layers.json:3985`).
- F-3 Owner calls `_tests` a suffix (finding :5, :13) — closed: F-1 (a).
- F-4 `test_locations._is_test_path` (:430-482): 1 ADS stream (:442); 2 `test_locations` matched RELATIVE TO app_root
  (`_config_match(ctx, _rel(t, ctx.app_n))`, :445); 2b `_recognition` (:365-410): `run.levels` patterns and `roots.test` / `tests_root`
  joined to the PROJECT ROOT (`ctx.root_p / given`, :360, :405), a value at/above the project root or app_root, or wildcard-only
  covering a protected root whole, ignored (:384, :406); 3 inside a protected root AND `ctx.entries()` non-empty -> False (:459-462);
  4 markers relative to the DEEPEST of app_root / project root holding the path (:464-467), none -> False "outside the project and the
  application" (:465-466). `ctx.entries()` (:298-312) = live entries (non-empty string, no grammar problem), incl. one covering a root.
- F-5 `test_files._decide` (:236-267): `name` (:239-242) never reads the verdict; `test_place` = v.test (:245-246); `test_body` = config
  FILE entry or name marker (:247-250); `commit` = v.test or `_by_names` (:251-254); `production` = v.test and (source `test_locations`
  or `_production_names`) (:255-260); `test_code` (:263-267). Docstring consumer table :7-23.
- F-6 Template `references/templates/config.json`: `app_root "."` (:3); `test_locations: []` (:7; note :8 "inside the application code ...
  relative to app_root"); `tests_root: "."` (:9; note :10 "Root of the test repository, relative to the project root ... set when tests
  live in a repo separate from the application code"); `code_repos` (:15; note :16 "with several repos, app_root is their common
  parent"); `run.levels {}` (:143). (t-160 minor 8 fixed.)
- F-7 Blind sites (attempt 1, each re-read then): judge_run.py:208-213 (`is_test_for("name", segment)`, re-read now); gate_preflight.py:
  887-921 (`_spelled_as_a_test` / `first_test_file`, re-read now) and caller :3656 (re-read: on nothing found returns code
  `no_test_files` / `nothing_under_profile`, :3666-3668); exit_gate.py:1531-1539 (`production_files(created, {"production"})`, no cfg,
  re-confirmed by grep :1539); runtime_probe.py:95-99 (`file_kind(name)`, grep :99); user_path_failures.py:214, :349, :427-429, :462,
  :529, :579; grounding_table.py:376, :1253 (callers :1379/:1430/:1791, handoff_check.py:878); blast_radius.py:241-245; base_slice.py:421;
  project_inventory.py:526-534 (`_test_area` via `names_a_test`, re-read now); handoff_check.py:274-278 (re-read now).
- F-8 Diff -> checkout (re-read now): `implementation_checkout(entry, cfg, project, diff_name)` (handoff_check.py:230-244, axis-10
  survivor); `implementation_entries` (:206-215); `_impl_checkout` (:247-257) binds when the manifest holds EXACTLY ONE entry, whatever the
  number of diffs; `_production_files` passes `cfg if base is not None else {}` and `base` (:274-278). `grounding_table.manifest_entry_for`
  (:258-268, attempt 1); `diff_pass.rich` hunk `repo` = suffix after `impl-diff-` (:450-453, attempt 1).
- F-9 Absolute paths must not reach the name rules (`validate_artifacts.py:2564-2566`, attempt 1).
- F-10 Readers already passing cfg (grep this turn): stage_guard.py:2260 (`commit`, base = event cwd, `is not False`); guard_pre_tool.py:1599
  (`test_body`, root = project, `is not True` passes); arch_check.py:124 (`test_body`, advice: locator in a test body); repo_map.py:244
  (`test_body`) and :251 (`test_place`, helper in a test place); validate_artifacts.py:2571 (`test_code`; no live caller of
  `is_test_code`, t-160 grep + control).
- F-11 Siblings found in attempt 1: `test_path_grants._is_test_specific` (:98-112); `probe_by_code._in_test_root` (:2599-); judge_run's own
  config read (:380).
- F-12 Onboarding: p1-discovery.md:83-87; p2-interview.md:119-130 (":130 With no candidates, 1c is not asked"); p4-generate.md:91, :365-366;
  s5.md:234-244 (re-read now: the road records a test location IN THE APPLICATION TREE on the person's word, `project_decisions.py` field
  `/test_locations`); `test_locations._scan` walks only protected roots (:556-597).
- F-13 Ownership (re-read t-129:466-512, CORRECTED per t-160 must 6): OF3-1 node a owns `config-keys.json`, `templates/config.json`,
  `p2-interview.md`, `p4-generate.md`, `test-layers.json` (`covers` lines); node b owns `test_locations.py` WHOLE (no function list,
  t-129:491-492); node f owns `test-layers.json` (`fixture_owners` line) and cuts the R2 knowledge-read baseline last. OF3-1 a is
  "accepted (critic t-154)" per commit 631a427's message; its MERGE and node b's state are UNVERIFIED here — the order below is on merges.
  Live streams (t-129:469-479): "handoff" owns `handoff_check.py`, `handoff_init.py` and their two tests; "doctor" owns `readiness.py`,
  `gate_preflight.py`, `skills/qa-doctor/`; "hot" owns `stage_guard.py`; "tests" owns `test_grounding_table.py`, `test_exit_gate_grounding.py`.
- F-14 Test carriers (test-layers.json read this turn): keep — `test_test_files.py` (:6220, table; covers test_files.py, hooklib.py),
  `test_test_locations.py` (:6230, detector; covers test_locations.py, test_path_grants.py, guard_pre_tool.py, the markers file),
  `test_protected_test_path.py` (:3985), `test_handoff.py` (:2216, covers handoff_check.py), `test_grounding_table.py` (:2072),
  `test_runtime_probe_onboarding.py` (:4533, covers runtime_probe.py), `test_flow_requests.py` (:1719, covers user_path_failures.py),
  `test_gate_preflight.py` (:1844), `test_readiness.py` (:4112, covers readiness.py), `test_arch_check.py` (:76, covers arch_check.py),
  `test_probe_by_code.py` (:3572, covers UNVERIFIED), scenarios `test_scenario_cart_1.py` (:4901), `test_scenario_local_1_0108.py`
  (:4921), `test_scenario_local_1_arm_b.py` (:4941) — each covers `scripts/exit_gate.py` and its story folder. Stories walk S1 and S2
  exit gates (cart-1 story.json:9-32; local-1-0108 story.json:10-31). No story has a `variants.json` today (glob
  `fixtures/stories/**/variants*.json` empty; control `fixtures/stories/**/*.json` in the same shape lists 261 files); the walker reads it
  as `[]` when absent (scenario_walk.py:111) and applies `write`/pointer ops to a copy (:225-249). Quarantined (never a witness):
  `test_judge_run.py`, `test_exit_gate_grounding.py`, `test_blast_radius.py` (:7082), `test_base_slice.py` (:7056),
  `test_project_inventory.py`, `test_repo_map.py`.
- F-15 Census (`scripts/tests/fixtures/judgment-census.json`, read this turn): ratchet `safety: 55`, `blocking_per_role.conductor: 472`
  (:4); rows `stage_guard.py rule_pathspec` safety/intent (:782), `rule_manifest` shape/data (:780), `guard_pre_tool.py
  window_file_check` safety/data (:370), `test_files.py is_test_for` shape/data (:841), `exit_gate.py grounding_errors` shape/data (:285);
  readiness capabilities ARE units (`readiness.py check_*`, :651-659). No row names `_is_test_path`, `first_test_file`, `_decide`.
- F-16 The stand's config (t-160 empirics, outside this repo, not re-read): `app_root "../MyBooks"`, `profiles[playwright-tests].roots.test
  "tests"` (the factory's own test repo), `test_locations ["src/**/*.test.ts", "**/test_*.md"]`.
- F-17 Existing pin that changes under F-3 (b) with a real config: `test_test_files.py:276-285` (cfg `app_root "."`, protected `src`,
  `test_locations ["src/legacy/"]`) expects `[True, True, True, True]` for commit `src/legacy/a.py`, commit `src/app/FooTests.cs`,
  commit `lib/FooTests.cs`, production `src/legacy/a.py`; under this spec `[True, False, False, True]`.

## §1 AR-n, principles, owners and census classes

| AR | how this spec touches it | change check in the DoD |
|---|---|---|
| AR-1 | five names are data rows; no list in code | item 1 rows; no new folder-name tuple in `scripts/` (grep in report) |
| AR-2 | where tests live is open variety: the role proposes at onboarding / the doctor, the person confirms; `--suggest` reports, never records | items 13-14: what the role decides is named in the phase text |
| AR-3 | the decision lives in existing keys; a project with nothing recorded IN THE PATH'S AREA reads exactly as today; a carrier about one area never changes another (t-160 AR-3 break closed) | item 2 area rows; §3 row "word about the other area" |
| AR-7 | the verdict stays an instrument; the role decides at onboarding | item 13 |
| AR-12 | S2 friction under F-5 (a); doctor walk cap | item 14 cap; F-5 cost named; first live run measures |
| AR-13 | "is this a test" only through `test_files` -> `test_locations`; "recorded / which area" only through `test_locations.recorded` / `area`; the carriers' live rule is ONE helper `_live_carriers` used by `_recognition` and `recorded`; the area rule is step 4's own "deepest base" | items 2-4; grep for `dir_names`/`name_marker`/`dir_marker` outside the leaf: only `test_path_grants` (folded, item 1b) |
| AR-15 | one survivor `handoff_check.diff_checkout` for "diff path -> checkout"; `_impl_checkout` becomes a one-line use of it | item 5; every diff site lists its call |
| AR-19 | S1 handoff count and S2 exit gate read the same leaf with the same binding | items 6, 7 |
| AR-22 | the word has producers (onboarding 1c, S5 road) and every reader | item 13 |
| AR-23 | empty outcome declared: `test_locations: []` = nothing named for the application area; template `tests_root "."` = nothing for the project area | item 2 |
| AR-28 | recorded word + unbindable diff -> unknown -> consumer's safe default; unreadable config -> today's reading, never MORE "test" than today | items 4-9 |
| AR-29 | every altered check judges data (presence of a carrier in an area, a path join); the commit guard and window claim change INPUT semantics, not class | census table |

Principles: P2, P27 (the record is the person's intent; code checks its presence), P31 (one road: every site through the same leaf with
the same word/checkout rule; no language branch; under F-3 (b) the commit/window/test_code asymmetry of attempt 1 is gone), FR-13, FR-47, FR-59.

Checks this spec adds or alters — owner served and census class:

| check | where | owner served | census class | note |
|---|---|---|---|---|
| `area(path)` / `recorded(cfg, root, path)` | test_locations.py (new) | intent (presence of the person's recorded word for that area) | shape — a reader, not a refusal site; no census row expected (no `test_locations.py` unit is listed, F-15); if `test_judgment_census.py` names one, the builder adds the row it names (shape, data) | never raises |
| verdict step 3b "area recorded -> no markers" | test_locations.py `_is_test_path` | data | not a unit (F-15) | |
| consumer rules under a recorded area; keywords `word`/`checkout` | test_files.py `is_test_for` (unit :841) | data | shape, unchanged | |
| commit shape (`rule_pathspec`, `rule_manifest`) | stage_guard.py — NO EDIT; input semantics ALTERED via `commit` | intent (`rule_pathspec` row :782, unchanged) / data (`rule_manifest` :780) | safety / shape, unchanged | F-3 (b): a recorded area's test commit is checked only when the record names it — G1 (§C rows) |
| write-window claim | guard_pre_tool.py `window_file_check` — NO EDIT; input semantics ALTERED via `test_body` | data (a path joined to the recorded carriers; row :370 unchanged) | safety, unchanged | G2 |
| `test_code` | validate_artifacts.py — NO EDIT; dead consumer (no live caller) | data | n/a | queued for the owner (§7 O-3) |
| S2 `grounding_errors` new-module list | exit_gate.py (unit :285) | data | shape, unchanged | refusal text gains a cause clause (item 7) |
| rehearsal pick, inventory test area | gate_preflight.py, project_inventory.py | data | not units (F-15) | |
| doctor `check_test_places` | readiness.py (new unit) | intent (presence of the word) + data (suggestion ⊂ word; checkout ⊂ an area) | xref, roles `conductor`, never blocks; one census row | if the census test computes `blocks` for it -> STOP (ratchet `blocking_per_role` must not rise, AR-20) |

FR walk: A — FR-1/FR-2 (item 7 clause names cause and door), FR-4, FR-57 (G1/G2 doors, §C); C — FR-12, FR-13, FR-17; D — FR-59 (unknown
-> declared default); E — FR-41 (doctor "at least"); G — FR-30, FR-32, FR-47, FR-54. B — the doctor row and the item-7 clause go through the
existing forms. F not touched.

## §2 Items (each: file / function; World N = nothing recorded in the path's area; World R = recorded; edges with invariant; test)

All rows go into EXISTING keep files or story `variants.json` (layer 1); no new test file; no source pin; no quarantined file.

**1. Data — `references/test-path-markers.json` (node A).** `dir_names` += `"__test__", "testing", "integration", "fixtures"` after `"e2e"`;
`dir_suffixes` -> `[".tests", ".test", "_tests"]`; `classic` untouched; `_comment` += "the list grows only as a hint; a project's record
decides (B-355)". Pins `test_protected_test_path.py:307-313` exact lists; `:130` loop += four names; `:133` loop += `myapp_tests/`.
World N (rows `test_test_files.py` `part_consumers`): `src/integration/client.py` -> production (invariant: a folder alone never drops a
product file from S2); `src/integration/client_test.go` -> `test` for `production` (agreeing name + usual folder; a stated change);
`fixtures/users.json` -> `commit` True, `test_body`/`name` False; `unit_tests/a.py` folder hit, `_tests/a.py` no hit; judge_run skips a
quoted `fixtures`/`integration`/`testing` (invariant: an upper-case env name never meets the name test, judge_run.py:221).
World R (rows `part_recorded`): the same five paths in a recorded area and outside the record -> `commit` False, `test_body` False,
`production` production; invariant: a new hint name never decides anything where the area is recorded.
**1b. `test_path_grants._is_test_specific`** (node A) calls `test_locations.dir_marker` / `name_marker` (byte-equal except the shared camel
rule; advice notes only). Rows: the `:130/:133` loops.

**2. `test_locations.area(path, cfg, *, base=None, root=None) -> "app" | "project" | ""` and `recorded(cfg, *, root=None, path=None,
base=None) -> (bool, carriers list, area)` (node A, new).**
- AREA of a path = the deepest of app_root / project root that holds it — the SAME rule step 4 uses (:464-467), one helper. Tie
  (app_root resolves to the project root): `"app"` (F-11). Neither holds it: `""`.
- CARRIERS per area: `"app"` -> `test_locations` (live when `_Ctx.entries()` is non-empty; an entry covering a whole protected root counts,
  as step 3 counts it today). `"project"` -> `run.levels`, `roots.test`, `tests_root`, each LIVE when `_recognition` would not ignore the
  value AND the place it names (its literal prefix) lies in the project area by the same `area` rule. A project-root carrier whose place
  lies in the application area counts for NO area (it still recognises its paths in step 2b, as today). `""` -> none. `protected_app_paths`
  is never a carrier. The ignore rules move into `_live_carriers(ctx)`, called by `_recognition` and `recorded` (AR-13).
- `path` given -> the answer for that path's area. `path=None` -> "any area": True when either area is recorded (used by `unbound` and
  by `name`); the area field is then `""`.
- World N rows (`test_test_locations.py`, real config on a temp project): config absent / `{}` / not a dict -> `(False, [], <area>)`;
  `test_locations` absent, `[]`, `"src/tests"` (not a list), `["", "/abs", "../x"]` -> app area not recorded; `tests_root` `"."`, `""`,
  `".."`, the root itself as an absolute path -> project area not recorded; `run.levels {"unit": "**"}` -> not; profiles not a list /
  `roots` not a dict / `roots.test` not a string -> not; nested value (`run.levels {"unit": {"x": "tests"}}`) -> not; any exception ->
  `(False, [], "")`.
- World R rows: `app_root "../app"`, `tests_root "qa"` -> path `qa/t.py` -> `(True, ["tests_root"], "project")`, path `../app/src/a.py` ->
  `(False, [], "app")` (THE BLOCKER ROW, t-160 finding 1: a word about the test repo never silences the application area); the stand's
  shape (F-16) -> app area recorded by `test_locations`, project area by `roots.test`; `app_root "."` + `roots.test "tests"` + `test_locations
  []` -> app area NOT recorded (F-11), `src/__tests__/cart.test.ts` stays a markers test (today); `app_root ".."` (common parent of
  `code_repos`) + `roots.test "tests"` -> the test repo's own files are the project area (deeper base), recorded.
- Adversarial battery (outside input, t-160 minor 12; each row compares `recorded()` WITH the verdict on the same spelling, so they can
  never disagree): `tests_root "qa\\tests"` == `"qa/tests"`; `"Tests"` with a folder `tests` (case read as the verdict reads it today);
  trailing `/`; a non-ASCII folder name `pruebas_ñ`; a `test_locations` list of 1000 entries (recorded, no limit introduced); an entry
  of 4096 characters (as the verdict reads it). Invariant: a value the verdict cannot match through never counts as recorded, a value it
  can always does, and a carrier counts only for paths in its own area.

**3. Verdict step 3b (node A; F-2 (b) per area).** `_is_test_path`: steps 1, 2, 2b, 3 stay as they are. New step 3b, before step 4: when
`recorded(cfg, root, path=t)` is True -> `test False, by none`, reason `the project recorded where its tests are for this <application
code | test repository> (<carriers>) and this path is in none of them`. Step 4 runs only when the path's area is not recorded.
POSITIONAL invariant: 3b sits after 2/2b (a config match is never hidden) and after 3 (the protected-root refusal keeps its own reason);
an ADS stream path in a recorded area is False; a path outside both bases has area `""` and reaches step 4's "outside" answer as today.
World N: identical to today for every input (rows: the existing `test_test_locations.py` rows stay green unchanged). World R rows:
`tests_root "qa"` + `app_root "../app"` -> `qa/foo.test.ts` is a config test (2b, unchanged); `helpers/x.test.ts` in the project area
-> no test (was markers); `../app/src/foo.test.ts` -> markers test (app area unrecorded); markers file unreadable + recorded area ->
config verdicts unchanged, unmatched paths False with the 3b reason. Invariant: in a recorded area no path becomes a test by the list.

**4. `test_files` consumers (node A; F-3 (b) owner, F-4 (a), F-5 (a), F-12).** `_decide` asks `test_locations.recorded(cfg, root=root,
path=..., base=base)` once per call (AR-13; never a second reading of the carriers). In a RECORDED area:
- `commit` = `v.test` (no `_by_names`); `test_body` = `_is_config_file(v)` (no name marker); `test_code` = code file AND `v.test` AND source
  not in {tests_root, roots.test} (dead consumer, F-10; follows the same rule mechanically); `test_place` = `v.test` (unchanged code);
  `production` = unchanged code — `v.test` can come only from the record, and inside a `run.levels`/`roots.test`/`tests_root` place the
  usual names only KEEP a helper counted (F-12; error direction: an extra production file, never a lost one).
- `name` (no path, so no area): when every existing area is recorded -> a segment is a test name only when it equals, lower-cased, the
  LITERAL last folder segment of a live folder carrier; when some area is unrecorded -> that set UNION today's rule. ("Existing": the
  project area exists unless app_root resolves to the project root.) Error direction: noise (an identifier grepped), never a skipped
  project folder name.
World N: every consumer exactly as today (rows: the existing `part_consumers`, `part_kinds` rows stay green; F-17 is World R).
New keywords on `is_test_for`, `file_kind`, `production_files`: `word=None, checkout=None` — ONE default for every function and every
caller (t-160 minor 10). `word` is the project config used only to judge through `checkout`; `word is None` -> the call is EXACTLY today's
(`cfg`/`base`/`root` as passed). With `word`:
- `checkout` a folder: area of `checkout/path` recorded under `word` -> judge with `(word, base=checkout, root)`; not recorded -> judge with
  the caller's own `cfg`/`base` (its today call) — so World N is today byte for byte at every site, including a checkout outside
  app_root and the project root (area `""` -> not recorded -> today's call; t-160 must 2 as the Lead decided it).
- `checkout=None` with `word` (unbound): `recorded(word, root=root)` (any area) True -> every consumer returns None (its declared unknown:
  production counted, commit checked, window passes); False -> the today call.
Markers, when they run, read the path exactly as the today call reads it (never the checkout's own folder name: a checkout folder named
`integration` or `x.tests` never makes its files tests; F-9).
Error direction of the reused leaf in its new role (it now gates the S2 exit through the record): it may call a test "production",
never a production file "test". Adversarial rows (each in `part_recorded`): a `test_locations` folder matched from the wrong base
(`checkout=None` -> unbound, never a match); a checkout folder named `integration` / `app.tests` with nothing recorded (no file becomes a
test by the checkout's name); `run.levels "**"`; `tests_root "."`; an entry covering the whole protected root; a path with `..` climbing
out of the checkout (area `""` or the other area, never a match through the word); a word about the project area while the path lies in
the application area (today's call).
Test: ONE parameterised table `part_recorded` in `test_test_files.py`, ids `<consumer>-<world>-<case>` over worlds `R`, `N`, `R-unbound`,
`N-unbound`, `R-other-area`, `outside-both`, real `test_locations.is_test_path` on a temp project; the F-17 pin is updated to
`[True, False, False, True]` (named expected edit).

**5. One survivor "diff -> checkout" (node B).** `handoff_check.diff_checkout(task_root, diff_name, cfg, project) -> (Path|None, reason)`:
entries via `implementation_entries(work/context-manifest.json)`; the entry via `grounding_table.manifest_entry_for` (lazy import:
grounding_table imports handoff_check at module top); else, when the manifest holds EXACTLY ONE entry (whatever the number of diffs —
today's `_impl_checkout` condition, t-160 minor 9), that entry; then `implementation_checkout`. `_impl_checkout(art)` becomes
`diff_checkout(...)` when the manifest holds exactly one entry, else None (one join; it stays as the source of the today call). Edges: no
manifest, unreadable manifest, two entries naming one diff, an entry with no id, a configured path that is not a folder -> `(None,
reason)`. World N/R: the binding is computed in both worlds; whether it is used is item 4's rule. Invariant: one join for every diff
site; a diff is never bound to another repository's checkout. Test: rows in `test_handoff.py` beside
`the_implementation_checkout_has_one_survivor...` (:1682, attempt 1): one entry two diffs -> both bound (today); two entries -> each by
name; none -> unbound.

**6. S1 `handoff_check._production_files` / `_diff_counts` (node B).** Takes the diff RECORDS (each carries `diff`): per record
`file_kind(path, today_cfg, base=today_base, root=project, word=cfg, checkout=diff_checkout(...)[0])` with `(today_cfg, today_base)` =
`(cfg, base)` when `_impl_checkout` binds, else `({}, None)` — exactly today's arguments. World N: the S1 figure equals today's for
every task. World R: a multi-repo task binds each file to its own checkout. Test (layer 1): variant rows in
`P\scripts\tests\fixtures\stories\local-1-0108\variants.json` (NEW file, owned by node B), stage S1: (i) a config writing
`test_locations` + an impl diff whose test file lies under it -> the S1 production figure drops it; (ii) the same diff with nothing
recorded -> today's figure.

**7. S2 `exit_gate.new_production_files(diff_text, *, cfg=None, base=None, root=None, word=None, checkout=None)` + `grounding_errors` (node
C).** A bare call stays today's. `grounding_errors` reads the config once (`hooklib.load_config()`) and per diff calls `diff_checkout(root
.parent, diff.name, cfg, project_root())`, then `new_production_files(text, word=cfg, checkout=<found or None>, root=project)` (the today
arguments are none, as now). When a module is listed only because its diff was unbound under a recorded word, the refusal appends:
`(counted as production: the checkout of <diff> is not configured - implementation_repos[].local_path or code_repos[].path; a person's
word passes this check)`. World N: the S2 list is today's for every task (config absent, unreadable `{}`, or nothing recorded in the
file's area, incl. a checkout outside both bases). World R: a new file under a recorded place is not listed; an unbound diff lists every
code file with the clause. Invariant: never MORE "test" than today when the config cannot be read. Test (layer 1): variant rows in
`P\scripts\tests\fixtures\stories\cart-1\variants.json` (NEW file, owned by node C), stage S2: recorded place -> module not asked;
unbound under a recorded word -> refusal carries the clause; nothing recorded -> today's outcome; config unreadable -> today's outcome.

**8. S9 `runtime_probe._production`, `diff_files`, `diff_new_files` (node C).** Take `cfg` (callers :1453, :1652 hold it;
`execution_request.py:2720`, `gate_preflight.py:4471` call `rp.diff_files(task_root)` and get `hooklib.load_config()` inside — no caller
edit) and bind per diff with `diff_checkout`. The own `+++ b/` regex stays (queued, §5). World N: today. World R: a recorded test place
leaves the stale-stand comparison. Test: rows in `P\scripts\tests\test_runtime_probe_onboarding.py` (keep): R wins / N today / unbound.

**9. `user_path_failures` (node D).** `_production(path, *, cfg, checkout, project)`; `_diff_files` binds each record by
`diff_checkout(task_root, rec["diff"], ...)`; `_bundle_files`, `_places`, `_note_files`, `address_neighbours` pass the checkout-relative
path and the folder they already hold (never the absolute path, F-9); a `repo_id/p` key splits to (checkout of `repo_id`, `p`); a bundle
file under the project root -> checkout = project. cfg from `regression_scope.project_config(project)` (already used :504, :567). Today
call = `file_kind(label)` / `file_kind(path)` as now. World N: today. World R: bound. Test: rows in
`P\scripts\tests\test_flow_requests.py` (keep, covers user_path_failures.py).

**10. `grounding_table.index_hunks`, `share`, `share_of`, `_cmd_share` + `handoff_check._claim_grounding_share` (node B).** `share(...,
*, root=None)`: with `root`, a hunk's file is bound through `diff_checkout(root, <diff name of hunk["repo"]>, ...)` (`""` -> `impl-diff.txt`,
`x` -> `impl-diff-x.txt`); without `root` -> no `word` (the pure call stays today's). `index_hunks(root)` binds by `f["diff"]`. Callers
:1379, :1430, :1791 and handoff_check.py:878 pass `root`. The table's own `kind` is still not believed (grounding_table.py:1221). World N:
today. Test: rows in `P\scripts\tests\test_grounding_table.py` (keep; node B starts after stream "tests" merges).

**11. `blast_radius._kind`, `base_slice._collect_diff` (node D).** Both hold `ctx.cfg` and a per-diff checkout (blast_radius.py:185,
base_slice.py:201): pass `word=ctx.cfg, checkout=<it>`; today call unchanged. Test: rows in `test_test_files.py` `part_sites` (node D,
after A) — `covers` lines added by node A (their own tests are quarantined).

**12. judge_run, project_inventory (node D); gate_preflight (node F) — the readers that PICK a test (t-160 must 7, G3).**
- `judge_run.wanted_names(text, cfg=None, root=None)` -> `_names_a_test(name, cfg, root)` -> `is_test_for("name", segment, cfg, root=root)`;
  `remedy` passes the config it read (:379-382) and the project root. World N: today. World R: item 4's `name` rule. Rows: `part_sites`.
- `gate_preflight.first_test_file(root, cfg=None, project=None)`: per file, by the file's area. World N (no cfg, or the file's area
  unrecorded): today exactly (`_spelled_as_a_test`, the `REPORTER_TEST_GLOBS` floor on None). World R: a candidate = a code file
  (`is_code_file`, the `CODE_EXTENSION_FLOOR` on None) AND `is_test_for("test_place", <path relative to project>, cfg, root=project) is
  True`; among candidates, in the sorted walk order, one whose name `_spelled_as_a_test` is preferred (F-14, an order hint, never a
  verdict). None in a recorded area -> `""`, and the caller's `how` says `none of the files under <cwd> lies in the project's recorded
  test places` with the existing code `no_test_files` — never a fall back to the usual names or `REPORTER_TEST_GLOBS` (Lead decision).
  Caller :3656 passes the gate's config and `ctx.root`. Invariant: the rehearsal never runs a non-code file, and in a recorded area never
  a file the record does not name. Rows: `P\scripts\tests\test_gate_preflight.py` beside :5107-5159: R with a folder carrier (the stand's
  shape: `tests_dir "tests"`, no file entry) -> a code file under `tests/` is picked (G3 regression closed); R with a record naming no
  file under `tests_dir` -> `""` + the how-text; N -> today.
- `project_inventory._test_area(place, cfg=None, project=None)`: World N (phase 1: no config exists yet — TEMPORAL; or the place's area
  unrecorded): today (`names_a_test`). World R (after p4 writes the config): `test_place` AND code file -> its folder; else `""` (a helper
  in a recorded folder now counts as an area: stated). Rows: `part_sites`.

**12b. `arch_check` :124, `repo_map._is_test_file` :244 — the advice readers of `test_body` (node D; F-13; §0 F-10 under F-3 (b)).**
Under (b) `test_body` in a recorded area is "a file the record names one by one". Recommended (F-13 (a)): both ask `test_place`. World N:
`test_place` for a path in an unrecorded area is `v.test` with markers — NOT today's `test_body` (name only) — so the change is gated:
the site asks `test_place` only when `recorded(cfg, root, path)` is True, else `test_body` as today. World R: arch_check flags a locator in
any code file of a recorded place except page objects (noise side); repo_map lists every file of a recorded place as a test (its helper
branch :251 is not reached there). Rows: `P\scripts\tests\test_arch_check.py` (keep) for arch_check; `part_sites` for repo_map.

**13. Onboarding text (node G, after OF3-1 node a merges).** `p1-discovery.md:83-87`: "the candidates are the factory's hint; the team's
answer in 1c is the decision every later stage reads". `p2-interview.md:119-130`: 1c is asked ALWAYS: with no candidate, where this
project's tests live (a test repository / a folder outside the application code / inside it), recorded in the carrier of THAT AREA
(`test_locations` for the application code; `tests_root` or the profile's `roots.test`, or a `run.levels` pattern, for the test
repository); where helpers sit beside tests, the role records the test FILE shape (`tests/**/test_*.py`, `src/**/*.spec.ts`) rather than
the folder, because under the owner's F-3 (b) a folder record makes every file there a test for the commit guard but claims none for a
window (§C). `p4-generate.md:365`: after `--check`, name each `--suggest` candidate no recorded carrier of its area covers, once. Edge:
"we have no tests" -> nothing recorded (declared empty, AR-23); the doctor reads `not_recorded`. No test reads phase prose; FR-33 live run.

**14. Doctor `readiness.check_test_places` (node H, after the doctor stream merges; F-8 (a)).** Per area: `ok` when the area is recorded
and `test_locations.suggest` finds no candidate outside its carriers; `not_recorded`; `uncovered` naming at most 5 candidates (`+N
more`); plus `unreachable` naming each configured checkout (`implementation_repos[].local_path`, `code_repos[].path`) outside both
app_root and the project root while a word is recorded (the word cannot reach its files; t-160 must 2). Walk capped by `DEFAULT_MAX_FILES`,
`truncated` -> "at least" (FR-41); markers unreadable -> `unknown`, never `ok`; remedy owner `user`, step `/qa-factory:qa-onboarding`
(topic 1c); no script handed to a person; no `SKILL.md` byte. The builder's first move reads `readiness.py`; a capability that cannot carry
this shape -> STOP. Rows: `P\scripts\tests\test_readiness.py` (keep): the four states + `unknown`, World N and World R.

**15. `probe_by_code._in_test_root` (node I; F-10 (a)).** Read through `test_locations.is_test_path(...)` (`by == "config"` and source in
`roots.test`/`tests_root`), not its own reading of the keys (its B-415 seam text, :2602). World N/R: the same answers for every config the
two readings agree on; a value `_recognition` ignores (`"."`, at/above the root) is now ignored here too (stated). Rows:
`P\scripts\tests\test_probe_by_code.py` (keep; node A adds the `covers` line if absent).

## §3 Edges consolidated (behaviour + invariant)

| edge | World N | World R | invariant |
|---|---|---|---|
| config absent / unreadable at a site | today | — | an unreadable config never makes a file MORE "test" than today |
| word about the OTHER area only (t-160 blocker) | the path's area is unrecorded -> today | — | a carrier counts only for paths in its own area |
| app_root resolves to the project root | only `test_locations` records (F-11); project carriers recognise in 2b as today | | the tie never silences colocated tests through `roots.test`/`tests_root` |
| app_root a common parent (`..`) | the test repo is the project area (deeper base) | its carriers decide there | area = step 4's deepest-base rule |
| checkout outside app_root and the project root | today's call (area `""`) | today's call; doctor `unreachable` | a word never reaches a place it cannot name; never less than today |
| diff with no findable checkout | today's call | consumer's None (production counted; S2 clause) | a guessed base never drops a file |
| path in a recorded area, not in the record | — | not a test for every consumer; production counted | the list decides nothing where the record speaks |
| test file written outside the record (G1/G2) | — | commit unchecked, window unclaimed — accepted risk with doors (§C, §7) | the record is the person's word (owner F-3 (b)) |
| record names folders only, helpers beside tests | — | commit checks helpers too; window claims nothing there | item 13 asks for file shapes |
| `test_locations: []` / absent / non-list; `tests_root "."` | not recorded | | empty is declared (AR-23) |
| entry covering a whole protected root | | recorded; targets inside stay protected (step 3) | protection wins (F3 of D-0030) |
| ADS stream path | today | False | an application file's stream is never a test location |
| markers file unreadable | each consumer's None default (today) | config verdicts unchanged, others False | an unknown never becomes "test" for production |
| the word changes mid-story (s5.md road) | each read uses the config at read time | | no stored verdict is re-judged |
| TEMPORAL: before node A merges | all sites as today | — | B, C, D, F, H, I start from a `main` holding A |
| TEMPORAL: onboarding phase 1 (no config) vs after p4 | World N | World R where recorded | project_inventory states both |

Conflicting pairs: (i) "only the record decides" (F-3 (b)) vs the commit guard's error direction -> owner chose (b); doors in §C/§7;
(ii) "word first" vs diff paths with no checkout -> F-5 (a); (iii) "role decides once" vs `[]` = "not named" -> F-7 (a) + item 13;
(iv) per-area scope vs `name` (no path) -> item 4 union rule.

### §C Safety rows F-3 (b) opens (from t-160 §C), with the door

| gap | what happens | door | status |
|---|---|---|---|
| G1 commit guard | a test written in an UNRECORDED place of a recorded area (`newdir/test_x.py`, a new `e2e/` beside a recorded `tests/`) is committed without `rule_pathspec` / `rule_manifest` (stage_guard.py:2869-2871, t-160) | doctor `uncovered` (item 14); the S5 road that records a place on the person's word (s5.md:234-244) — today only for the application tree; extending it to the test repository is node J, ONLY on the owner's yes (§7 O-1) | accepted risk per owner's word, stated |
| G2 write window | such a file is not claimed -> two windows may tear it | same doors | accepted risk, stated |
| G3 rehearsal pick / inventory blind | regression | item 12 | fixed |
| G4 G1/G2 over the whole application checkout of a project recorded only through `roots.test` | — | per-area scope (item 2) | fixed |

## §4 Nodes, owns, order (absolute paths; P = `C:\QAFactory\forge-repo\ai-packages\qa-factory`)

Order (every arrow is a MERGE into `main`):
- OF3-1 a -> OF3-1 b -> **A** (A edits `test_locations.py`, b owns it whole; A writes `test-layers.json` `covers`, a writes it too). Lines
  `очередь: OF3-1a → B-355A` and `очередь: OF3-1b → B-355A` in both batch files.
- A + stream "handoff" + stream "tests" -> **B**.
- B -> **C**; A + B -> **D** (D also needs A's `test_test_files.py` merged: serial on that file).
- A + stream "doctor" -> **F**; A + stream "doctor" -> **H**; A -> **I**; OF3-1 a -> **G**.
- B-355 A, B, C, D, F, H, I -> OF3-1 f (f cuts the knowledge-read baseline after the new config readers land; F-15 asks the Lead).
- Node J (s5.md) exists only on the owner's yes to §7 O-1; after G.
Hot files: `gate_preflight.py` alone in F; `stage_guard.py`, `guard_pre_tool.py`, `validate_artifacts.py` not edited.

| node | items | owns |
|---|---|---|
| A | 1, 1b, 2, 3, 4 | `C:\QAFactory\forge-repo\ai-packages\qa-factory\references\test-path-markers.json`; `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\test_locations.py` (`area`, `recorded`, `_live_carriers`, `_recognition`, `_is_test_path`, `is_test_path` docstring); `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\test_files.py`; `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\test_path_grants.py` (`_is_test_specific`); `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_test_files.py` (`part_consumers`, `part_kinds`, new `part_recorded`, the F-17 pin); `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_test_locations.py`; `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_protected_test_path.py`; `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test-layers.json` (`covers` lines only: `test_test_files.py` += `judge_run.py`, `project_inventory.py`, `blast_radius.py`, `base_slice.py`, `repo_map.py`, `test_locations.py`; `test_probe_by_code.py` += `probe_by_code.py` if absent); `C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\b355-a.md` |
| B | 5, 6, 10 | `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\handoff_check.py` (`diff_checkout` new, `_impl_checkout`, `_production_files`, `_diff_counts`, `_claim_grounding_share`); `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\grounding_table.py` (`index_hunks`, `share`, `share_of`, `_cmd_share`, call lines :1379, :1430, :1791); `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_handoff.py`; `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_grounding_table.py`; `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\stories\local-1-0108\variants.json` (new); `C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\b355-b.md` |
| C | 7, 8 | `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\exit_gate.py` (`new_production_files`, `grounding_errors`); `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\runtime_probe.py` (`_production`, `diff_files`, `diff_new_files`); `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_runtime_probe_onboarding.py`; `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\stories\cart-1\variants.json` (new); `C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\b355-c.md` |
| D | 9, 11, 12 (judge_run, project_inventory), 12b | `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\user_path_failures.py`; `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\blast_radius.py` (`_kind`); `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\base_slice.py` (`_collect_diff`); `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\judge_run.py` (`_names_a_test`, `wanted_names`, the `remedy` call line); `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\project_inventory.py` (`_test_area` and its call in `integration_proposals`); `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\arch_check.py` (line :124 block); `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\repo_map.py` (`_is_test_file`); `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_flow_requests.py`; `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_test_files.py` (new `part_sites` only, after A merges); `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_arch_check.py`; `C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\b355-d.md` |
| F | 12 (gate_preflight) | `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\gate_preflight.py` (`_spelled_as_a_test`, `first_test_file`, caller block :3655-3662); `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_gate_preflight.py`; `C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\b355-f.md` |
| G | 13 | `C:\QAFactory\forge-repo\ai-packages\qa-factory\skills\qa-onboarding\phases\p1-discovery.md`; `C:\QAFactory\forge-repo\ai-packages\qa-factory\skills\qa-onboarding\phases\p2-interview.md`; `C:\QAFactory\forge-repo\ai-packages\qa-factory\skills\qa-onboarding\phases\p4-generate.md` |
| H | 14 | `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\readiness.py` (`check_test_places` new and its registration line); `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_readiness.py`; `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json` (one row: `readiness.py check_test_places`, class `xref`, roles `["conductor"]`, owner `intent`); `C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\b355-h.md` |
| I | 15 | `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\probe_by_code.py` (`_in_test_root`); `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_probe_by_code.py`; `C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\b355-i.md` |
| J (owner's yes only) | §7 O-1 | `C:\QAFactory\forge-repo\ai-packages\qa-factory\skills\qa-story\phases\s5.md` (the test-location paragraph :234-244 only) |

Disjointness: `test_test_files.py` A then D (serial, different parts). `test-layers.json` written by A only (OF3-1 a before, OF3-1 f after).
Story `variants.json`: local-1-0108 -> B only; cart-1 -> C only; local-1-arm-b -> nobody (read-only witness for B, C, D). Every story
folder printed by another node's `--witness-for` is a READ-ONLY witness for that node. No other file is shared.

Read-only witnesses (run, never written): B, C, D — `test_scenario_cart_1.py`, `test_scenario_local_1_0108.py`,
`test_scenario_local_1_arm_b.py` and every other keep file `--witness-for <owns>` prints outside `quarantine`.

DoD (every node, written inline at dispatch): the node's rows green; verification run attached verbatim:
`python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <the node's owns>` (and every file it prints outside the
`quarantine` section) and `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang`; package commits carry
`architecture: AR-n -- <how kept>` and `judgment:`. FIRST MOVES: node A greps every keep file that `--witness-for` prints for
`test_files.py`/`test_locations.py` for rows with a real config whose path's area becomes recorded and a markers-only or names-only
expectation, and lists them before coding; a hit in a file A does not own -> return to the Lead (owns amendment) before any edit. Nodes B
and C first confirm the walker can express their variant (a `write` op placing the config and the impl diff in the story's copy, and the
S1/S2 facet reading the figure / the list); if not -> STOP and return; never a new test file, never a quarantined one. STOP and return on:
any test expectation that must change to pass except the named edits (item 1 pins test_protected_test_path.py:130-135, :307-313; the
stated production change in test_test_files.py:113-116 if a row there names `integration`; F-17 test_test_files.py:279-285 ->
`[True, False, False, True]`); an unlisted ratchet raise (H's census row must not raise `blocking_per_role`); a site whose error
direction cannot be kept. Edges per node: §2 item text + §3. Live proof (FR-33): items 13-14 (and J) are "closed by code, not proved" until
a live onboarding + doctor run — rows for the Lead to move to `live-runs`.

## §5 Siblings (axis walk, rule 9; enumerated)

- Same artifact sweep — the `test_files` consumer table (:7-23): commit applied (F-3 (b)), test_code applied (dead, O-3), production applied
  (F-12), test_body applied (F-3 (b)), test_place applied (item 3), name applied (item 4); the docstring table gains a column "in a recorded
  area" (node A).
- Readers of `test_body` / `name` (t-160 class-completeness): guard_pre_tool.py:1599 (owner's (b), no edit), arch_check.py:124 and
  repo_map.py:244 (item 12b, F-13), gate_preflight `_spelled_as_a_test` and project_inventory `_test_area` (item 12), judge_run (item 12).
- New class (t-160): carriers matched against different bases (app_root vs project root vs checkout) — applied by the area rule (item 2),
  the checkout rule (item 4) and the markers-read-as-today rule (item 4). Latent sibling noticed, NOT widened: today handoff binds a
  checkout inside app_root and step 4 reads the path relative to app_root, so the checkout's own folder name enters the markers
  (handoff_check.py:276-278 + test_locations.py:467) — item 4's "markers read as the today call" keeps that exactly; queued as a finding
  for the Lead (§7 O-4).
- Axis 9: `test_path_grants` folded (1b); `judge_code.py:67-76`, `friction.py:58/104` queued under B-431 (not read this turn).
- Axis 10: `_impl_checkout` expressed through `diff_checkout` (item 5); `context_bundle.build`, `judge_diff._diff_files` copies of
  `implementation_entries` queued (handoff_check.py:208-209).
- Axis 16 / OF3-1 N-r4: `judge_run.remedy`'s own `json.loads` (:380) stays (N-r4 owns it).
- Own diff parse `runtime_probe.diff_files` (:109) beside `diff_pass` — queued.
- `probe_by_code._in_test_root` — node I.
- Axis 34 (one road): every site reaches the same leaf with the same `word`/`checkout` rule; no language or project branch; under F-3 (b)
  the consumer asymmetry of attempt 1 is gone; two consumer rows keep the names by error direction only (production narrowing F-12, `name`
  union) and are the same for every language and project.
- Axes 1-8, 11-33, 35, 36: not applicable — no policy, exam, release, measurer, identity, shell walker, journal, dispatch, transcript,
  ratchet (beyond H's census row), role-file, receipt, table-cell, host-form, row-field, ledger or sides code is changed.

## §6 Forks (new in this round; recommendation first). Closed: F-1..F-10 (Lead), F-3 (owner, (b), 12.11.2026).

- **F-11 Tie: app_root resolves to the project root.** (a) the whole project is the application area: only `test_locations` records;
  `roots.test`/`tests_root`/`run.levels` never silence the usual names (they still recognise their own paths) — matches t-160's "with
  app_root '.' the same happens to colocated tests"; (b) the project carriers count for the paths inside the folder they name only.
  Recommend (a): one rule (deepest base) and the safe side; cost: a single-repo project that recorded only `tests_root` keeps the usual
  names everywhere until it records `test_locations` (item 13/14 close it).
- **F-12 `production` inside a `run.levels`/`roots.test`/`tests_root` place.** (a) keep today's narrowing: a file there leaves the count
  only with a classic folder or a usual name of its own (`tests/helpers.py` stays counted); (b) the record alone: every file there leaves
  the count. Recommend (a): the names can only KEEP a file counted (an extra S2 `derived` row), never drop one; (b) drops helpers from
  the S2 grounding list. Owner's F-3 (b) names the commit guard, the window and `test_code`, not `file_kind`; the Lead takes it to the
  owner if (b) is read as "names mean nothing anywhere".
- **F-13 Advice readers of `test_body` (arch_check :124, repo_map :244).** (a) ask `test_place` in a recorded area, `test_body` elsewhere
  (item 12b); (b) keep `test_body`: in a folder-recorded area the locator advice and the repo map's test list go silent until the role
  records file shapes. Recommend (a): the S5 automator reads the repo map to extend existing tests (P17); noise is the cheap side.
- **F-14 Order preference in the rehearsal pick.** (a) in a recorded area, among the record's code files prefer one with a usual test name
  (order only); (b) the first code file in sorted order. Recommend (a): the name never admits or refuses a file, it only orders the
  record's own files; (b) may rehearse a helper first.
- **F-15 OF3-1 f's order.** (a) B-355 A, B, C, D, F, H, I merge before OF3-1 f cuts its knowledge-read baseline (`очередь: B-355 → OF3-1f`);
  (b) f first, and each B-355 node that adds a config read updates the baseline line (each owns `knowledge-read-baseline.json` serially).
  Recommend (a): no shared fixture across seven nodes; cost: f waits.

## §7 For the owner (plain words; recommendations, not decisions)

- **O-1 Tests written where the project has not recorded them (G1, G2).** With "only the record", a test the automator writes in a new
  folder nobody recorded is committed without the factory's commit checks, and two parallel automation windows do not reserve it, so
  they could overwrite each other. Recommendation: accept, with two doors — the doctor names unrecorded places (item 14), and one more
  sentence in the S5 instructions: before writing a test outside the recorded places, the automator stops and the conductor asks you
  whether to record the new place (the road already exists for the application folder; node J extends it to the test repository).
- **O-2 Helpers beside tests.** With "only the record", if the project records a whole folder (`tests/`), the factory can no longer tell a
  test from a helper there by its name: the commit guard checks helpers too (harmless), and windows reserve nothing in that folder.
  Recommendation: at onboarding the role records the test FILE shape (`tests/**/test_*.py`) where helpers sit beside tests (item 13).
- **O-3 "validate_artifacts detectors" are not used.** Your decision names them, but `is_test_code` has no live caller (t-160 checked):
  that part of the factory is dead. Recommendation: a separate finding — delete it or wire it — instead of designing behaviour for it.
- **O-4 (for the Lead, a finding)** the checkout-name latent sibling (§5), to be filed in `onboarding-hooks`.

## §8 Small choices closed by the designer

- Keywords `word` / `checkout` (not `unbound`): `word is None` = today's call; ONE default everywhere (t-160 minor 10).
- `diff_checkout` lives in `handoff_check` beside `implementation_checkout`; `manifest_entry_for` imported lazily, not moved.
- The area rule reuses step 4's deepest-base computation (one helper), not a new notion.
- Nodes D and E of attempt 1 merged into D (both need `test_test_files.py` after A; one serial writer instead of two).
- Story assignment: S1 rows to local-1-0108 (B), S2 rows to cart-1 (C); local-1-arm-b untouched.
- The rehearsal keeps the closed code `no_test_files` and says the record in its `how` text (no new code, FR-12).
- Census row for the doctor: class `xref`, owner `intent` (the person's word), roles `conductor`, like the other `readiness.check_*` rows.
- Config readers: the sibling's existing reader (`hooklib.load_config` in exit_gate; `regression_scope.project_config` in user_path_failures).
- Hunk `repo` -> diff name is the inverse of `diff_pass.rich` (:452-453). New `dir_names` order: after `e2e`.

## §9 Brief contradictions / analogs noticed

- t-160 finding 2 proposed "markers relative to the checkout" for a checkout outside both bases; the Lead's decision ("equals today
  exactly") makes it today's call instead — applied; the critic's unbound variant for the recorded world is replaced by the area rule
  (such a path is in no area, so nothing is recorded for it) plus the doctor's `unreachable` row.
- The owner's list names "детекторы `validate_artifacts`"; the consumer is dead (O-3). Kept the owner's word: `test_code` follows (b).
- No verdict item contradicts an owner's word.

## §10 Reading trail

Read whole: the t-155 draft (attempt 1), t-160 verdict, the B-355 finding, `docs/TESTING.md`, `references/templates/config.json`.
Read in part this turn: t-129 :456-530; `test_locations.py:280-489`; `test_files.py:1-327`; `handoff_check.py:200-304`; `judge_run.py:200-229`;
`gate_preflight.py:880-924, :3640-3669`; `stage_guard.py:2240-2264`; `guard_pre_tool.py:1585-1602`; `arch_check.py:105-154`;
`repo_map.py:232-256`; `project_inventory.py:505-554`; `s5.md:230-244`; `test_test_files.py:1-70, :265-344`; `test-layers.json:1-60,
:1719-1734, :4112-4144, :4533-4556, :4901-4958, :6216-6250`; `judgment-census.json:1-12`; `scenario_walk.py` (grep `variant`);
`test_scenario_cart_1.py`; journal lines t-155/t-160.
Greps (with positive controls in the same shape): `is_test_for\(|test_files\.(file_kind|production_files)\(` over `scripts/*.py`; keep-row
keys and `covers` names in `test-layers.json`; census rows for readiness / stage_guard / guard_pre_tool / test_files / exit_gate (control:
readiness rows found); story `"stage"` lines; `variants*.json` glob empty, control `**/*.json` same path found 261 files.
Not read: `readiness.py` (item 14 first move), `test_probe_by_code.py` covers (UNVERIFIED), `test_handoff.py:1682` this turn (attempt 1),
the stand config (t-160 empirics), `factory-rules.md` full text (index), `probe_by_code.py` this turn (attempt 1).
Needed beyond the manifest: the site files above, `test-layers.json`, `judgment-census.json`, stories, `templates/config.json`, `s5.md`.

## Fix round t-160 — change list

| verdict item | answer |
|---|---|
| 1 BLOCKER per-area scope | fixed: item 2 `area`/`recorded(path=)`; carriers per area; F-11 tie returned; blocker row in item 2; §3 row |
| 2 MUST checkout outside both bases | fixed per Lead: World N = today's call at every site (item 4 `word`/`checkout`, item 6 today arguments); doctor `unreachable` (item 14); §9 says how it differs from the critic's proposal |
| 3 MUST fold F-3 (b) | fixed: Digest, item 1 World R, item 4, item 12, 12b, census table, §3, §5 axis 34, docstring column; §C rows; §7 O-1..O-3 |
| 4 MUST owns | fixed: every test file named inline as an absolute path; story variants to ONE node each (B local-1-0108, C cart-1), others read-only; D owns `test_test_files.py` `part_sites` serial after A (E merged into D); H's census owns unconditional with the row named |
| 5 MUST carriers / layer 1 | fixed: S1 (item 6) and S2 (item 7) outcome rows are story `variants.json` rows; every item names its keep file; walker capability is a first-move STOP, not a fallback table |
| 6 MUST F-13 / order | fixed: F-13 corrected (OF3-1 b owns all of `test_locations.py`); A after OF3-1 a AND b merges, `очередь:` lines; G after OF3-1 a |
| 7 MUST picks under (b) | fixed: item 12 `test_place` + code file, name only as order (F-14); recorded-but-empty -> `""` + how-text, never the generic list (Lead decision) |
| 8 minor template path | fixed (F-6) |
| 9 minor single-entry condition | fixed: today's condition kept exactly (item 5) |
| 10 minor `unbound` defaults | fixed: one default `word=None, checkout=None` everywhere |
| 11 minor dead `test_code` | fixed: stated dead, follows (b) mechanically; O-3 for the owner |
| 12 minor battery | fixed: item 2 encoding / case / trailing / magnitude rows, compared with the verdict |
| §B rows | all applied (Digest, census, item 1 edge, item 4, item 12, §0 F-10 readers -> 12b, §3, F-3 closed, docstring) |
| §C G1-G4 | G1/G2 accepted-risk rows with doors + O-1 (node J on the owner's yes); G3 fixed (item 12); G4 fixed (item 2) |
| Lead "nothing recorded = today" incl. project root | item 4 rule + §3 rows; the tie (F-11) keeps project carriers from silencing anything |
| Lead "first_test_file/_test_area finding nothing" | item 12: both worlds stated |

## Closed 12.11.2026 (Lead acceptance of attempt 2)

- Owner (12.11.2026, in the coordinator's session): O-1 — accept with both doors: the doctor names unrecorded places (item 14) AND node J
  (the S5 conductor asks the person before a test is written outside the recorded places) — node J is IN. O-2 — the role records the
  test FILE shape where helpers sit beside tests (item 13). O-3 — a separate finding (delete or wire `is_test_code`), no behaviour designed
  here. F-12 — (a): usual names only KEEP a file counted in `production`, never drop one.
- Lead: F-11 (a), F-13 (a), F-14 (a), F-15 (a). Assumption 9 confirmed: F-1, F-4..F-10 carry the attempt-1 recommendations.
- Wording slip in item 3 World R fixed by the Lead. O-4 and O-3 go as findings into `onboarding-hooks`.
- Dispatch order unchanged: node A waits for OF3-1 a AND b merged.
