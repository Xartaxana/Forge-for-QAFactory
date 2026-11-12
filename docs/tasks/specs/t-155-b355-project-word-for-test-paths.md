# t-155 — B-355: five more usual test names as a HINT, and every reader reads the project's recorded word first — DRAFT SPEC

Designer (Opus), 12.11.2026. Draft for Lead acceptance; forks are returned in §6, never decided. Owner's new idea (PROJECT.md
"Как разрабатывается новая идея владельца", step 5); critic on plan is mandatory before any builder (step 6).
Sources: finding `plans/piles/onboarding-hooks/findings/B-355-markery-testovykh-putey-references-test-path.md:13-15` (owner's decision
and clarification, 12.11.2026); Lead intent brief t-155 (intent items 1-3, scout t-150 recon). PKG = `C:\QAFactory\forge-repo\ai-packages\qa-factory`.
Every `path:line` below was READ in this drafting turn on `main` (6915cc0) unless marked UNVERIFIED.

## Digest

The one verdict already exists: `test_locations.is_test_path(path, cfg, base, root)` reads the project's word (steps 2/2b) and falls to
the usual names (step 4); `test_files.is_test_for` / `file_kind` already accept `cfg/base/root`. The defect is that (i) ten sites call the
leaf WITHOUT the config, so only the generic list decides there, and (ii) even with the config, step 4 still decides everywhere except
"inside a protected root when `test_locations` is non-empty" (test_locations.py:458-462). This spec: adds the five names to the hint list
(item 1); defines ONE predicate "the project recorded its word" (item 2); runs the generic list in the verdict only when nothing is
recorded (item 3, fork F-2); keeps, per consumer, only the safe-side use of the names (item 4, fork F-3); gives the diff-reading sites
ONE survivor that binds a diff's paths to their checkout (item 5); wires every blind site (items 6-12); moves the onboarding text and the
doctor to "the list is the role's hint, the record is the decision" (items 13-14). No new config key; no new writer.

**Behaviour that changes (everything else byte-for-byte as today):**
1. `dir_names` gains `__test__`, `testing`, `integration`, `fixtures`; `_tests` lands per F-1 (recommended `dir_suffixes`).
2. A project that recorded its word (item 2): the usual names no longer make a path a test in the verdict (step 4 skipped) — for every
   consumer that reads the verdict (production counts, `test_place` advice, the S2 exit gate, ...). Commit shape, write-window claim and
   `test_code` keep the names as an extra trigger toward checking (F-3 (a)).
3. The ten blind sites read the project's word; a diff path is matched to the word only through the checkout it is relative to;
   recorded word + no checkout -> the consumer's declared unknown default (F-5 (a)).
4. Onboarding records a decision even when `--suggest` finds no candidate inside the application code; the doctor names an old project
   whose word is missing or does not cover the suggested places (F-8 (a)).

---

## §0 Facts (read this turn)

- F-1 `references/test-path-markers.json:3` `dir_names` = `test, tests, __tests__, spec, specs, e2e, test-harness`; `:4` `dir_suffixes`
  = `.tests, .test`; `:9` `classic.folders` = `test, tests, __tests__, test-harness`; `_comment` (:2) already says "a SUGGESTION and a
  FALLBACK, never a refusal or a permission".
- F-2 Pins: `scripts/tests/test_protected_test_path.py:307-313` (exact four lists), `:130-132` (loop over six `dir_names`), `:133-135`
  (loop over `dir_suffixes`). keep (`test-layers.json:3985`).
- F-3 The finding names `_tests` a SUFFIX ("суффикс `_tests`", finding :5, :13); the brief puts it into `dir_names` — contradiction, F-1.
- F-4 `test_locations._is_test_path` (:430-482): 1 ADS stream check; 2 `test_locations` match; 2b `_recognition` (`run.levels`,
  `profiles[].roots.test`, `tests_root`; a value at/above the project root or app_root, or covering a protected root whole, is ignored,
  :365-410); 3 inside a protected root AND `ctx.entries()` non-empty -> not a test; 4 markers, relative to the deepest of app_root /
  project root. `ctx.entries()` (:298-312) = live entries (non-empty string, no grammar problem), INCLUDING one covering a whole root.
- F-5 `test_files._decide` (:236-267): `name` never reads the verdict (:239-242: name marker or last segment in `dir_names`); `commit` =
  `v.test or _by_names` (:251-254); `test_body` = config FILE entry or name marker (:247-250); `production` = `v.test` and
  (`source == test_locations` or `_production_names`: classic folder alone, or name + (usual folder or a carrier source)) (:255-260);
  `test_code` = code file and (`_by_names` or `v.test` not from `tests_root`/`roots.test`) (:263-267). `cfg` not a dict -> `{}` (:243).
- F-6 Template: `test_locations: []` (templates/config.json:7), `tests_root: "."` (:9), `protected_app_paths: []` (:5). config-keys.json:19-27:
  `test_locations` absent_means `default` since 0.9.0; `tests_root` `required`, project_fact.
- F-7 Blind sites (scout t-150, each re-read): judge_run.py:208-213 (`is_test_for("name", segment)`, called from `wanted_names` :216, which
  `remedy` calls at :383 holding the project config it read itself at :379-382); gate_preflight.py:887-921 (`_spelled_as_a_test` "name" +
  `is_code_file`; `first_test_file(root)` called at :3656 with the profile's `tests_dir`); exit_gate.py:1531-1539 (`production_files(created,
  {"production"})`, no cfg; called per diff file from `grounding_errors` :1566-1574, which knows `root = artifact_root()/ticket/work`);
  runtime_probe.py:95-99 (`file_kind(name)`; `diff_files` :102-115 parses `+++ b/` with its OWN regex, not `diff_pass`); user_path_failures.py:214
  (`_diff_files`, records of `diff_pass.index` with `diff`/`repo`), :349 (`_bundle_files`, label + resolved absolute path in hand), :427-429
  `_production(path)` called at :462 (`_places`, target resolved), :529 (`_note_files`, key `repo_id/p`), :579 (`address_neighbours`, key
  `repo_id/p`, folder in hand); grounding_table.py:376 (`index_hunks`) and :1253 (`share`, pure, signature `(data, policy, findings,
  policy_why)`; callers grounding_table.py:1379/:1430/:1791, handoff_check.py:878); blast_radius.py:241-245 (`_kind`, `ctx.cfg` loaded :135,
  checkout per diff :185); base_slice.py:421 (`_collect_diff`, `ctx.cfg` :484, checkout per diff :201); project_inventory.py:526-534
  (`names_a_test`); handoff_check.py:274-278 (`cfg` only when `_impl_checkout` :247-257 finds the ONE manifest entry's checkout).
- F-8 Diff -> checkout today: `handoff_check.implementation_checkout(entry, cfg, project, diff_name)` (:230-244, the axis-10 survivor);
  `implementation_entries` (:206-215); `grounding_table.manifest_entry_for(name, entries)` (:258-268: by `diff_path` basename, else
  `impl-diff-<x>.txt` by `repo_id or repo`; "No third guess"); `diff_pass.rich` sets `repo` = suffix after `impl-diff-` ("" for
  `impl-diff.txt`) (:450-453). handoff's `_impl_checkout` uses a DIFFERENT join (exactly one entry, diff name not used) — F-6.
- F-9 Absolute paths must not reach the name rules: `validate_artifacts.is_test_code` comment :2564-2566 ("an absolute path would let a
  checkout that happens to live under `.../test/...` make every file a test"); `file_kind` reads `docs` and classic folders on every segment.
- F-10 Already on the road (pass cfg): stage_guard.py:2254-2261 (commit, `is not False`); guard_pre_tool.py:1598-1599 (test_body, `is not
  True` passes); arch_check.py:124; repo_map.py:243-251; guard_app_under_test.py:142-144 (opens only on `source == test_locations`).
- F-11 Further readers found (siblings, §5): `test_path_grants._is_test_specific` (:98-112) re-implements `dir_marker` / name matching on
  `table` (axis 9 open side, B-431); `probe_by_code._in_test_root` (:2599-) reads `roots.test` / `tests_root` itself, not through
  `test_locations` ("the seam B-415 widens", :2602); judge_run.remedy reads `qa-factory/config.json` with its own `json.loads` (:380,
  OF3-1 N-r4 class).
- F-12 Onboarding: p1-discovery.md:83-87 (`--suggest`, "it decides nothing"); p2-interview.md:119-130 (1c; ":130 With no candidates, 1c
  is not asked"); p4-generate.md:91 (writes `test_locations`), :365-366 (`--check --json` after writing); p3-summary-gate.md:68 (counts);
  skills/qa-story/phases/s5.md:235-242 (the S5 road that records a location on the person's word mid-run). `test_locations._scan` walks
  ONLY the protected roots (:556-597).
- F-13 Ownership (OF3-1 spec t-129 :468-512, doctor spec t-144 §4): OF3-1 node a owns `config-keys.json`, `p2-interview.md`,
  `p4-generate.md`, `test-layers.json` (covers); node b owns `test_locations.py` (`_config_of` only); node f cuts the R2 baseline last.
  Live streams: "handoff" owns `handoff_check.py`; "doctor" owns `readiness.py`, `gate_preflight.py`; "hot" owns `stage_guard.py`;
  "tests" (OH3-25) owns `test_grounding_table.py`.
- F-14 Tests: keep — `test_test_files.py` (table, covers test_files.py, test-layers.json:6220-6228), `test_test_locations.py` (detector,
  :6230), `test_protected_test_path.py` (:3985), `test_grounding_table.py` (:2072), `test_gate_preflight.py` (:1844), `test_stage_guard.py`
  (:5171), `test_arch_check.py` (:76). QUARANTINED (never a witness, no new row): `test_judge_run.py` (:8455), `test_exit_gate_grounding.py`
  (:7988), `test_blast_radius.py` (:7082), `test_base_slice.py` (:7056), `test_project_inventory.py` (:9035), `test_repo_map.py` (:9214).
  No keep row lists `judge_run.py` under `covers` (grep of the covers lines, same call found `exit_gate.py`, `handoff_check.py`).
- F-15 OF3-1's reader: `project_knowledge.value(root, key, ...)` returns ONE key's stored value with `state known/unknown` (t-129 §3); it
  does not compute a verdict over several keys.

## §1 AR-n, principles, owners and census classes

| AR | how this spec touches it | change check in the DoD |
|---|---|---|
| AR-1 | five names are data rows in `test-path-markers.json`; no list in code | item 1 rows; grep `scripts/` for a new literal folder-name tuple: none added |
| AR-2 | where tests live is open variety: the role proposes, the person confirms at onboarding / the doctor; code (`--suggest`) reports candidates and never records | items 13-14: what the role still decides is named in the phase text; `--suggest` on a fixture laid out unlike the default reports, never halts |
| AR-3 | the decision lives in existing config keys; "absent / `[]` / `"."`" = nothing recorded = today's behaviour (the default world) | item 2 rows for both worlds; no template key added (so no `config-keys.json` row) |
| AR-7 | the verdict stays an instrument; the role decides at onboarding what is a test place | item 13 text |
| AR-12 | doctor walk cost (item 14) and S2 friction under F-5 (a) | item 14 caps the walk; F-5 cost named; `code_friction` "not measured" as an open item |
| AR-13 | "is this a test" is read only through `test_files` -> `test_locations.is_test_path`; "recorded?" only through `test_locations.recorded`; the carriers' live-value rule is ONE helper used by both | items 2-4, 6-12; grep for `dir_names`/`name_marker`/`dir_marker` outside the leaf: only `test_path_grants` (item 1b folds it) |
| AR-15 | one survivor `handoff_check.diff_checkout` for "diff path -> checkout" (axis 10), wired at every diff site | item 5; every diff site lists its call |
| AR-19 | S2 exit gate and S1 handoff count read the same rule with the same binding | items 6, 7 rows |
| AR-22 | the recorded word has a producer (onboarding 1c, S5 road) and every reader; a record made "nothing inside the app" still produces a carrier | item 13 |
| AR-23 | the empty outcome of `test_locations` is declared: `[]` = "nothing named" (F-7) | item 2 |
| AR-28 | recorded word + unbindable path -> unknown -> consumer's safe default, never the generic list's pass; unreadable config -> exactly today's reading, never MORE "test" than today | items 4, 6-9 rows |
| AR-29 | every altered check judges data (presence of a carrier, a path join) | census below |

Principles: P2 (no project shape in code), P27 (code owns data, role judgment, person intent), P31 (one road: every site through the
same leaf with the same cfg/base rule; no language branch), FR-13, FR-47, FR-59.

Checks this spec adds or alters — owner served and census class:

| check | where | owner served | census class | note |
|---|---|---|---|---|
| `recorded(cfg, root)` "the project recorded where its tests are" | test_locations.py | intent (the person's recorded word; code checks its PRESENCE) | shape (presence) — a reader, not a refusal site; no census row unless the census lists readers | never raises |
| verdict step 4 gated on `recorded` | test_locations.py | data | existing unit, class unchanged (shape/xref) | |
| consumer rules under a recorded word, `unbound` | test_files.py | data | existing unit, class unchanged | |
| S2 exit `grounding_errors` new-module list (input changes only) | exit_gate.py | data (xref new module <-> `derived` row) | existing unit, class unchanged | refusal text gains a cause clause (item 7) |
| commit shape, write-window claim | stage_guard.py, guard_pre_tool.py | safety | unchanged, no edit | |
| doctor row "test places recorded / cover the suggestions" | readiness.py (F-8 (a)) | intent (presence of the person's word) + data (xref suggestion ⊂ word) | shape + xref; one `judgment-census.json` row if readiness capabilities are census units (builder checks, UNVERIFIED) | advice, never a refusal |

No ratchet raise of `judgment-census.json` is expected; a builder whose change would raise one STOPs (AR-20).

FR walk (sections touched): A — FR-1/FR-2 (item 7's refusal names the cause and the door), FR-4; C — FR-13 (data rows), FR-12 (no
phrase list), FR-17 (one survivor wired everywhere); D — FR-59 (unknown -> declared default), FR-58 n/a; E — FR-41 (doctor counts "at
least" on truncation); G — FR-30, FR-32, FR-47, FR-54. B — the doctor row and the item-7 clause are person/role text through the existing
forms; F not touched.

## §2 Items (each: file / function, behaviour, edges with their invariant, test)

All tests are rows/variants in EXISTING keep files (F-14), never in a quarantined file; no new test file; no source pin. Mutation probes
are one-off runs in the builder report.

**1. Data — `references/test-path-markers.json` `dir_names` (node A).** Append `"__test__", "testing", "integration", "fixtures"`
after `"e2e"` (before `"test-harness"`, order kept for the pin's readability). `_tests` per F-1: recommended into `dir_suffixes` ->
`[".tests", ".test", "_tests"]`. `classic` NOT touched (Lead's decision in the brief). `_comment`: one clause "the list grows only as a
hint; a project's record decides (B-355)". Pins: :307-313 exact lists updated; :130 loop gains the four names; :133 loop gains `_tests`
(F-1 (a)) as `myapp_tests/`.
Edges (each a row in `test_test_files.py` `part_consumers`/`part_classic`, nothing recorded):
- `src/integration/client.py` -> production (no usual name; `integration` is not classic). Invariant: a new product file in an
  `integration/` folder never leaves the S2 exit gate's list on the folder alone.
- `src/integration/client_test.go` -> `test` for `production` (usual name + usual folder, today's F2 rule, test_test_files.py:113-116)
  — a stated change from today (was production). Invariant: only an agreeing name-and-folder pair drops a file; never a folder alone.
- `fixtures/users.json` -> not a test for `test_body`/`name` (no code, no name marker); `commit` -> True (folder hit: checked).
  Invariant: the commit guard errs toward checking.
- `_tests`: `unit_tests/a.py` folder hit; `_tests/a.py` (nothing before the suffix) NOT a hit (dir_marker's `len > len(suffix)`).
- judge_run (nothing recorded): a quoted identifier `fixtures` / `integration` / `testing` is now skipped as a test name. Stated
  consequence; invariant kept: an upper-case env name (`_ENV_NAME`, judge_run.py:221) is never routed through the name test.
- `--suggest` now proposes `fixtures/`, `integration/`, `testing/` folders as candidates (advice to the person, never recorded).
**1b. `test_path_grants._is_test_specific`** (node A) calls `test_locations.dir_marker` and `name_marker` instead of its own copy
(:104-112); behaviour byte-equal except that it follows the shared matcher (camel endings now count as test-specific — a notes-only
change). Test: the :130/:133 loops above are its rows (advice notes `[]` for every name).

**2. `test_locations.recorded(cfg, root=None) -> (bool, list)` (node A, new).** The ONE predicate "the project recorded where its
tests are"; the list names the carriers that hold a live value, in the order `test_locations`, `run.levels`, `roots.test`, `tests_root`.
A carrier is LIVE exactly when the verdict could match through it: `test_locations` -> `_Ctx.entries()` non-empty (an entry covering a
whole protected root counts, as step 3 counts it today); `run.levels` / `roots.test` / `tests_root` -> a value `_recognition` would NOT
ignore. The ignore rules move into one helper `_live_carriers(ctx)` that `_recognition` and `recorded` both call (AR-13; no second
reading of the same keys). `protected_app_paths` is NOT a carrier (it says where application code is, not where tests are; F-7).
Edges (both worlds, rows in `test_test_locations.py`): config absent / `{}` / not a dict -> `(False, [])`; `test_locations` absent, `[]`,
`"src/tests"` (not a list), `["", "/abs", "../x"]` (only dead entries) -> not from this carrier; `tests_root` `"."`, `""`, `".."` above the
project, absolute path equal to the root -> not; `tests_root: "qa"` -> `(True, ["tests_root"])`; `run.levels: {"unit": "**"}` (wildcard
only at the root) -> not; profiles not a list / `roots` not a dict / `roots.test` not a string -> not; any exception -> `(False, [])`
(today's world: the generic list). Invariant: a value the verdict cannot match through never counts as recorded, and a value it can
always does (no carrier that recognises a path while `recorded` says "nothing").

**3. Verdict step 4 only when nothing is recorded (node A; F-2, recommended (b)).** `_is_test_path`: step 3 becomes "the project
recorded its word (item 2) -> `test False, by none`, reason `the project recorded where its tests are (<carriers>) and this path is in
none of them`". Step 4 (markers) runs only when `recorded` is False. POSITIONAL invariant: the new check sits after 2/2b, so a config
match is never hidden; it sits before the "outside the project" check only as today's step 3 did (an outside path is False either way);
an ADS stream path (step 1) with a recorded word is False (a stream of an application file is never a test). Under F-2 (a) instead:
step 3 is left as is and only items 5-12 land.
Edges (rows, `test_test_locations.py`): recorded via `tests_root: "qa"` -> `src/foo.test.ts` is no test (was markers); nothing recorded ->
same path is a markers test (today); markers file unreadable + recorded -> verdicts from config unchanged, unmatched paths False with the
recorded reason (the markers are not needed). Invariant: with a recorded word, no path becomes a test by the generic list in the verdict.

**4. `test_files` consumers (node A; F-3, recommended (a)).** No new consumer. Under a recorded word:
`production`, `test_place` — unchanged code; they lose markers-only tests automatically (item 3). `commit`, `test_code`, `test_body`
keep their past-step use of the names (`_by_names` / name marker), stated as "the names may only move a verdict toward this consumer's
safe side (checked / claimed / detectors run)". `name` per F-4 (recommended (a): with a recorded word, a segment is a test name only
when it equals the LITERAL last folder segment of a live folder carrier (a `test_locations` folder entry, `roots.test`, `tests_root`, a
`run.levels` literal folder) — lower-cased; the generic names are not consulted; nothing recorded -> today's rule).
New keyword `unbound=False` on `is_test_for`, `file_kind`, `production_files`: the caller says "these paths are relative to a checkout I
could not find". `unbound=True` + recorded word -> every consumer returns None (its declared unknown: production stays counted, commit
checked, test_body passes); `unbound=True` + nothing recorded -> cfg not consulted, today's markers (F-5 (a); under F-5 (b) the generic
list always). Invariant: a project word is matched only against a path bound to its base; a guessed base never drops a file.
Error direction of the reused leaf in its new role (it now gates the S2 exit through the project's word): it may call a test
"production" (an extra `derived` row asked), never a production file "test". Adversarial inputs that must stay on the safe side, each
a row: a `test_locations` folder entry matched from the WRONG base (`base=None`, app checkout elsewhere) -> `unbound` path, never a
match; a checkout living under `/home/x/tests/` with an absolute path passed -> callers pass the checkout-relative path + `base` (F-9),
row asserts `file_kind("C:/w/tests/app/src/a.py")` is never used by a site (grep in the report); `run.levels: "**"`; `tests_root: "."`;
a `test_locations` entry covering the whole protected root; a path with `..` climbing out of the checkout.
Test: one parameterised table in `test_test_files.py` (`part_recorded`), ids `<consumer>-<world>-<case>` over worlds
`recorded` / `nothing` / `recorded-unbound` / `nothing-unbound`, real `test_locations.is_test_path` on a temp project (not the stub).

**5. One survivor "diff -> checkout" (node B).** `handoff_check.diff_checkout(task_root, diff_name, cfg, project) -> (Path|None,
reason)`: entries via `implementation_entries` of `work/context-manifest.json`; the entry via `grounding_table.manifest_entry_for`
(lazy import inside the function: grounding_table imports handoff_check at module top); then — F-6 (a) — when that finds none and the
manifest holds exactly one entry and the task holds exactly one `impl-diff*.txt`, that entry (handoff's rule of today, kept so its count
does not regress); then `implementation_checkout`. `_impl_checkout` is deleted; `_production_files` takes the RECORDS (each has `diff`)
and binds each to its diff's checkout. Edges: no manifest, unreadable manifest, two entries naming one diff, an entry with no id, a
configured path that is not a folder -> `(None, reason)` -> the site passes `unbound=True`. Invariant: one join for every diff site; a
diff is never bound to another repository's checkout. Test: rows in the keep test that `--witness-for scripts/handoff_check.py` prints
holding `the_implementation_checkout_has_one_survivor...` (test_handoff.py:1682, keep status UNVERIFIED — builder confirms from the
command; if quarantined, the rows go to `test_test_files.py` with a `covers` line from node A).

**6. s07 `handoff_check._production_files` / `_diff_counts` (node B).** Behaviour: count by `file_kind(path, cfg, base=checkout,
root=project, unbound=checkout is None)`. Edge: multi-repo task (two diffs, two checkouts) -> each file bound to its own (today: none
consulted). Test: row "two diffs, a `test_locations` folder in the second checkout: its files leave the count, the first diff's
same-named path does not".

**7. s08 `exit_gate.new_production_files(diff_text, *, cfg=None, base=None, root=None, unbound=True)` + `grounding_errors` (node C).**
Defaults keep a bare call as today when nothing is recorded. `grounding_errors` reads the config once (`hooklib.load_config()`, as
blast_radius/base_slice/runtime_probe do) and per diff calls `diff_checkout(root.parent, diff.name, cfg, project_root())`. When a module
is listed only because its diff was unbound under a recorded word, the refusal appends one clause: `(counted as production: the checkout
of <diff> is not configured - implementation_repos[].local_path or code_repos[].path; a person's word passes this check)` (FR-1/FR-2;
the existing `S2_DIFF_UNREAD_DOOR` pattern). Edges: config absent -> nothing recorded -> today; config unreadable (`load_config` -> `{}`) ->
today's reading (invariant: never MORE "test" than today); a new file under a recorded `test_locations` folder -> not listed. Test: rows in
the keep test `--witness-for scripts/exit_gate.py` prints that pins grounding (builder names it; `test_exit_gate_grounding.py` is
quarantined and gets nothing).

**8. s09 `runtime_probe._production`, `diff_files`, `diff_new_files` (node C).** Take `cfg` (already loaded by callers :1453, :1652;
`execution_request.py:2720`, `gate_preflight.py:4471` call `rp.diff_files(task_root)` — they get the config default `hooklib.load_config()`
inside, no caller edit) and bind each diff file's paths with `diff_checkout(task_root, diff.name, ...)`. The own `+++ b/` regex stays (a
sibling of diff_pass, queued §5, not widened here). Test: row in the keep test of runtime_probe (`--witness-for`), recorded word wins /
nothing recorded.

**9. s10 `user_path_failures` (node D).** `_production(path, *, cfg, base, project, unbound)`; `_diff_files` binds each record by
`diff_checkout(task_root, rec["diff"], ...)`; `_bundle_files`, `_places`, `_note_files`, `address_neighbours` pass the checkout-relative
path and the folder they already hold (`folder` :570, `resolve_code_path` target -> its checkout), never the absolute path (F-9); a
`repo_id/p` key is split back to (checkout of `repo_id`, `p`). cfg from `regression_scope.project_config(project)` (already used :504,
:567). Edge: a bundle file found under the project root (not a checkout) -> base = project. Test: rows in the keep test
`--witness-for scripts/user_path_failures.py` prints (test-layers.json:1732/:6690 cover it).

**10. s11 `grounding_table.index_hunks`, `share`, `share_of`, `_cmd_share` + caller `handoff_check._claim_grounding_share` (node B).**
`share(..., *, root=None)`: with `root`, a hunk's file is bound through `diff_checkout(root, <diff name of hunk["repo"]>, ...)` (`""` ->
`impl-diff.txt`, `x` -> `impl-diff-x.txt`); without `root` -> `unbound=True` (a pure call stays deterministic). `index_hunks(root)`
binds by `f["diff"]`. Callers :1379, :1430, :1791 and handoff_check.py:878 pass `root`. Invariant: the table's own `kind` is still not
believed (grounding_table.py:1221). Test: `test_grounding_table.py` (keep; written by stream "tests" first — node B waits, §4).

**11. s12 `blast_radius._kind`, s13 `base_slice._collect_diff` (node D).** Both already hold `ctx.cfg` and a per-diff checkout
(blast_radius.py:185, base_slice.py:201): pass them (`unbound` when the checkout is None). Tests: their test files are quarantined (F-14);
rows go to `test_test_files.py` via `covers` lines added by node A (`blast_radius.py`, `base_slice.py` are already covered by a keep row
at test-layers.json:5912-5913 — builder uses that file if `--witness-for` prints it).

**12. s05 judge_run, s06 gate_preflight, s14 project_inventory (node E for judge_run + project_inventory; node F for gate_preflight).**
- `judge_run.wanted_names(text, cfg=None)` -> `_names_a_test(name, cfg)` -> `is_test_for("name", segment, cfg, root=...)`; `remedy` passes
  the config it read (:379-382). Behaviour per F-4. Test: `test_test_files.py` rows (judge_run has no keep coverage; node A adds
  `judge_run.py` to that file's `covers`).
- `gate_preflight.first_test_file(root, cfg=None, project=None)`: a candidate = a code file (`is_code_file`, floor kept) AND
  `is_test_for("test_body", <path relative to project>, cfg, root=project) is True` (a file the project names one by one counts; a helper
  under a named folder does not); None -> `REPORTER_TEST_GLOBS` (today's floor). Caller :3656 passes the gate's config and `ctx.root`.
  Invariant: the rehearsal never runs a non-code file or a helper as "the one test". Test: rows in `test_gate_preflight.py` beside :5107-5159.
- `project_inventory._test_area(place, cfg=None, project=None)`: `is_test_for("test_body", path, cfg, root=project) is True`. TEMPORAL:
  at onboarding phase 1 no config exists -> nothing recorded -> the usual names (the role's hint); after p4 writes the config -> the
  project's word. Test: row in a keep test covering project_inventory (test-layers.json:1570/:1591/:4252/:4283; builder names it).

**13. Onboarding text — the list is the hint, the record is the decision (node G, after OF3-1 node a).** `p1-discovery.md:83-87`: one
sentence "the candidates are the factory's hint; the team's answer in 1c is the decision every later stage reads". `p2-interview.md:119-130`:
1c is asked ALWAYS (not only with candidates): with none, the question is where the tests of this project live (a test repository / a
folder outside the application code / inside it), and the answer is recorded in the carrier it names (`test_locations`, `tests_root`, or the
profile's `roots.test`). `p4-generate.md:365`: after `--check`, name each `--suggest` candidate that no recorded carrier covers to the person
once. Edge: the team says "we have no tests" -> nothing recorded (declared empty outcome, AR-23; the generic list stays the fallback and the
doctor row reads `not_recorded`). No test reads phase prose; FR-33 live run is the proof (live-runs row).

**14. Doctor for projects onboarded earlier (node H, after the doctor stream merges; F-8, recommended (a)).** A `readiness.py`
capability `test_places` (name a small choice): `ok` when `recorded` is True and `test_locations.suggest` finds no candidate outside every
recorded carrier; `not_recorded` when nothing is recorded; `uncovered` naming at most 5 candidates (`+N more`) otherwise; walk capped by
`DEFAULT_MAX_FILES`, `truncated` -> "at least" (FR-41); remedy owner `user`, step `/qa-factory:qa-onboarding` (topic 1c) — no factory
script handed to a person (doctor spec t-144 item 3); no `SKILL.md` byte added (t-144 item 7 budget). Readiness internals are UNVERIFIED
in this draft: the builder's first move reads `readiness.py` and the census, and STOPs if a capability cannot carry this shape.
Test: rows in the keep test `--witness-for scripts/readiness.py` prints: three worlds above + markers unreadable -> `unknown`, never `ok`.

## §3 Edges consolidated (behaviour + invariant)

| edge | behaviour | invariant |
|---|---|---|
| config absent | nothing recorded; every site reads as today | the default world is today's, byte for byte |
| config unreadable at a site | the site's existing reader default (`{}`) -> nothing recorded -> today | an unreadable config never makes a file MORE "test" than today |
| `test_locations: []` / absent / non-list | not recorded by this carrier | empty is declared, never a guess (AR-23) |
| `tests_root: "."` (template default) | not recorded | the template default is not a decision |
| only `protected_app_paths` set | not recorded | the application boundary never names tests |
| recorded word, path not under it | not a test (step 4 skipped); commit/test_body/test_code still triggered by usual names (F-3 (a)) | the generic list decides nothing on a recorded project; it only adds checking |
| recorded word, diff with no checkout | `unbound` -> None -> production counted; S2 refusal names the cause and the door | a guessed base never drops a file (AR-28) |
| nothing recorded, no checkout | today's generic list | no regression |
| ADS stream path | False with a recorded word; today's rule otherwise | an application file's stream is never a test location |
| entry covering a whole protected root | counts as recorded; targets inside stay protected | protection wins (F3 of D-0030) |
| the word changes mid-story (s5.md:235 road) | each read uses the config at read time; no stored verdict is re-judged | no flip of an already-written artifact |
| markers file unreadable | recorded: config verdicts unchanged; nothing recorded: each consumer's None default (today) | an unknown never becomes "test" for production |
| absolute path at a site | never passed; checkout-relative path + base | a machine folder named `tests` never makes files tests |
| temporal: before node A merges | sites still blind; after: all on the word | nodes B-F start from a `main` holding A |

Conflicting pairs: (i) intent 3 "generic list only when nothing recorded" vs a guard's error direction (commit) -> F-3; (ii) "project
word first" vs diff paths with no known checkout -> F-5; (iii) "role decides once" vs `[]` meaning "not named" -> F-7 + item 13.

## §4 Nodes, owns, order (absolute paths; P = `C:\QAFactory\forge-repo\ai-packages\qa-factory`)

Order: A first (after OF3-1 node b merges, or D-0048 form: A owns `recorded`, `_live_carriers`, `_recognition`, `_is_test_path`; b owns
`_config_of`). Then B (after stream "handoff" AND stream "tests" merge), C, D, E in parallel (C, D need B's `diff_checkout`: they start
after B merges); F after stream "doctor" merges; G after OF3-1 node a merges; H after stream "doctor" merges. OF3-1 node f cuts its R2
baseline after A-H (announcement line `очередь: B-355 → OF3-1f`). Hot files: `gate_preflight.py` alone in F; `stage_guard.py` not edited.

| node | items | owns |
|---|---|---|
| A | 1, 1b, 2, 3, 4 | P\references\test-path-markers.json; P\scripts\test_locations.py (`recorded`, `_live_carriers`, `_recognition`, `_is_test_path` only); P\scripts\test_files.py; P\scripts\test_path_grants.py (`_is_test_specific` only); P\scripts\tests\test_test_files.py; P\scripts\tests\test_test_locations.py; P\scripts\tests\test_protected_test_path.py; P\scripts\tests\test-layers.json (`covers` lines only: `test_test_files.py` += judge_run.py, blast_radius.py, base_slice.py, project_inventory.py, test_path_grants.py if absent); P\changelog.d\b355-a.md |
| B | 5, 6, 10 | P\scripts\handoff_check.py (`diff_checkout`, `_production_files`, `_diff_counts`, `_claim_grounding_share` only); P\scripts\grounding_table.py (`index_hunks`, `share`, `share_of`, `_cmd_share` only); the keep test of handoff_check named by `--witness-for`; P\scripts\tests\test_grounding_table.py; P\changelog.d\b355-b.md |
| C | 7, 8 | P\scripts\exit_gate.py (`new_production_files`, `grounding_errors` only); P\scripts\runtime_probe.py (`_production`, `diff_files`, `diff_new_files` only); their keep tests named by `--witness-for`; P\changelog.d\b355-c.md |
| D | 9, 11 | P\scripts\user_path_failures.py; P\scripts\blast_radius.py (`_kind` only); P\scripts\base_slice.py (`_collect_diff` only); their keep tests named by `--witness-for` (never a quarantined one); P\changelog.d\b355-d.md |
| E | 12 (judge_run, project_inventory) | P\scripts\judge_run.py (`_names_a_test`, `wanted_names`, `remedy` call line); P\scripts\project_inventory.py (`_test_area` and its caller); P\changelog.d\b355-e.md (rows live in A's `test_test_files.py` — E adds its rows there AFTER A merges; serial on that file) |
| F | 12 (gate_preflight) | P\scripts\gate_preflight.py (`_spelled_as_a_test`, `first_test_file`, caller :3656 only); P\scripts\tests\test_gate_preflight.py; P\changelog.d\b355-f.md |
| G | 13 | P\skills\qa-onboarding\phases\p1-discovery.md; P\skills\qa-onboarding\phases\p2-interview.md; P\skills\qa-onboarding\phases\p4-generate.md |
| H | 14 | P\scripts\readiness.py (new capability only); its keep test named by `--witness-for`; P\scripts\tests\fixtures\judgment-census.json (one row, if a unit); P\changelog.d\b355-h.md |

Disjointness: A/E share `test_test_files.py` serially (E after A). B/C/D share no file. `test-layers.json` written by A only.
DoD (every node, written inline at dispatch): the node's rows green; verification run attached verbatim:
`python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <the node's owns>` (and every file it prints outside the
`quarantine` section) and `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang`; package commits carry
`architecture: AR-n -- <how kept>` and `judgment:`; STOP and return on any test expectation that must change to pass except the named
pins (item 1: test_protected_test_path.py:130-135, :307-313; item 1's stated production change in test_test_files.py:113-116 if a row
there names `integration`), an unlisted ratchet raise, or a site whose error direction cannot be kept. Live proof (FR-33): items 13-14
are "closed by code, not proved" until a live onboarding + doctor run — a row for the Lead to move to `live-runs`.

## §5 Siblings (axis walk, rule 9; enumerated)

- Same artifact sweep — `test_files` consumer table (module docstring :7-23): commit applied (F-3), test_code applied, production
  applied (via item 3), test_body applied, test_place applied (via item 3), name applied (F-4); the docstring table gains a column
  "with a recorded word" (node A).
- Axis 9: done sides above; open sides — `test_path_grants._is_test_specific` folded (1b); `judge_code.py:67-76`, `friction.py:58/104`
  (friction-markers `project_test_regex`) — NOT read this turn, queued under B-431 (the axis's own queue line), not widened.
- Axis 10: `_impl_checkout` folded into `diff_checkout` (item 5); `context_bundle.build` and `judge_diff._diff_files` carry their own copy
  of `implementation_entries` (handoff_check.py:208-209 says so) — queued there, not widened.
- Axis 16 / OF3-1 N-r4: `judge_run.remedy`'s own `json.loads` of the config (:380) stays (N-r4 owns it); item 12 only passes its result.
- Further reader, not a blind site: `probe_by_code._in_test_root` (:2599-) reads `roots.test` / `tests_root` itself — fork F-10.
- Own diff parse: `runtime_probe.diff_files` `+++ b/` regex (:109) beside `diff_pass` — AR-13 twin, queued as a finding (not this class).
- `validate_artifacts.is_test_code` (:2545, scout: no live caller — not re-verified here): unchanged; leaf behaviour covers it.
- Axis 34 (one road): no language or project branch; every site reaches the same leaf with the same cfg/base rule. The only asymmetry
  (commit/test_body/test_code keep the names) is a consumer-table row with its safe direction (F-3), not an exclusion.
- Axes 1-8, 11-33, 35, 36: not applicable — no policy, exam, release, measurer, identity, shell walker, journal, dispatch, transcript,
  ratchet (beyond the census row of H), role-file, receipt, table-cell, host-form, row-field, ledger or sides code is changed.

## §6 Forks (returned; recommendation first)

- **F-1 `_tests`.** (a) into `dir_suffixes` (`unit_tests/`, `api_tests/`) — the owner's words call it a SUFFIX (finding :5, :13);
  (b) into `dir_names` as the literal folder `_tests` (the brief's wording). Recommend (a). Cost of (b): matches almost nothing.
- **F-2 Where the generic list stops in the verdict.** (a) today's scope (step 3: inside a protected root, only when `test_locations` is
  non-empty) — B-355 then only wires the blind sites; (b) step 4 runs only when nothing is recorded (intent 3 literal, owner's "the list
  never decides by itself"). Recommend (b). Cost: a project that recorded only `tests_root`/`roots.test` loses markers-only recognition of
  colocated tests (production: extra rows; `test_place` advice: fewer) until it records `test_locations` — item 13/14 close the gap.
- **F-3 Commit guard, write-window claim, `test_code` under a recorded word.** (a) keep the usual names as an extra trigger toward
  checking (safe side of each consumer: a test commit is checked, two windows do not tear a file); (b) strict: project word only.
  Recommend (a) — but the owner's decision lists the commit guard and the window by name ("страж коммита", "окно записи гарда"), so (a)
  needs the owner's word; the Lead takes it. Cost of (b): a test written in an unrecorded place is committed unchecked and may be torn by
  two windows; adversarial input `newdir/test_x.py` must then be named as an accepted risk.
- **F-4 The `name` consumer (judge_run identifiers).** (a) recorded word -> literal folder names of the live carriers only; nothing
  recorded -> today; (b) always the generic list (one consumer left off the project word — a rule-6 exclusion, needs the owner's word);
  (c) union. Recommend (a): more identifiers grepped (noise, the cheap side), never fewer than the project's own folders.
- **F-5 Recorded word, diff path with no checkout.** (a) unknown -> consumer default (production counted; S2 asks a `derived` row or a
  person's word; the refusal names the cause and the door); (b) the generic list, as handoff does today. Recommend (a) (AR-28, FR-59).
  Cost: friction on projects without `implementation_repos`/`code_repos` until configured (AR-12, measure on the first live run).
- **F-6 Diff -> entry join.** (a) `manifest_entry_for`, then handoff's single-entry rule when the task has one diff and one entry; (b)
  `manifest_entry_for` only ("no third guess"). Recommend (a): (b) unbinds today's bound single-repo handoff count.
- **F-7 What counts as recorded.** (a) a live value in `test_locations`, `run.levels`, `profiles[].roots.test`, `tests_root`;
  `protected_app_paths` never; `[]`/absent/`"."` = nothing; (b) also a `project-decisions.json` answer on `/test_locations` even when the
  value is `[]` ("decided: none inside the app"); (c) a new sentinel key. Recommend (a) (no new key, no new reader; item 13 makes the role
  record a real carrier). Cost: "decided: no tests anywhere" stays indistinguishable from "never asked" (doctor reads `not_recorded`).
- **F-8 Doctor form.** (a) a `readiness.py` capability (no SKILL.md bytes; remedy = onboarding 1c); (b) a doctor step with a closed
  question that records through `project_decisions.py` (SKILL.md bytes over t-144's budget, a new write road for the doctor). Recommend (a).
- **F-9 Reader road for the config.** (a) the verdict through `test_files` -> `test_locations` (axis 9); each site passes the config its
  existing reader gives; OF3-1's catalogue rows for `test_locations`/`tests_root`/`run`/`profiles` get `needed_by` += the new readers in
  node f's R3 reconciliation; (b) sites call `project_knowledge.value()` per key and rebuild a cfg. Recommend (a): `value()` reads one key's
  raw value (F-15); the verdict needs the whole set and has its own reader (AR-13).
- **F-10 `probe_by_code._in_test_root`.** (a) a queued node in the same batch after A: read through `test_locations.is_test_path(...).by ==
  "config"` (its own B-415 seam text) with a row in its keep test; (b) leave for B-415. Recommend (a) (rule 6: a residual is a node).

## §7 Small choices closed by the designer

- Keyword name `unbound` (not a sentinel base); default False keeps every existing call unchanged.
- `diff_checkout` lives in `handoff_check` beside `implementation_checkout`; `manifest_entry_for` is imported lazily, not moved.
- New config reads use the reader the sibling already uses (`hooklib.load_config` in exit_gate; `regression_scope.project_config` in
  user_path_failures); no new road (OF3-1 N-r2 unifies later).
- Hunk `repo` -> diff name mapping (`""` -> `impl-diff.txt`) is the inverse of `diff_pass.rich` (:452-453).
- Order of the new `dir_names` entries: after `e2e`, before `test-harness`.
- `_live_carriers` shared by `_recognition` and `recorded` (one reading of the carriers).

## §8 Brief contradictions / analogs noticed

- `_tests` is a suffix in the owner's words, a folder name in the brief (F-1).
- Onboarding 1c is skipped with no candidates (p2-interview.md:130), and `--suggest` walks only the protected roots (:556): a project with
  tests outside the application folders is never asked — the owner's "the role decides once" is unreachable there (item 13).
- `test_grounding_table.py` is written by stream "tests" (OH3-25): node B waits for it.
- t-144 doctor stream owns `readiness.py` and `gate_preflight.py` and caps SKILL.md bytes: nodes F and H follow it.

## §9 Reading trail

Read whole: the B-355 finding; `references/test-path-markers.json`; `scripts/test_files.py`; `scripts/test_locations.py`; t-144 doctor spec.
Read in part: t-129 OF3-1 spec (:1-412, :456-525, grep for test_locations/node); `config-keys.json:1-30`; `templates/config.json:1-20`;
`judge_run.py:180-249, :360-390`; `gate_preflight.py:838-937, :3630-3674`; `exit_gate.py:1520-1593`; `handoff_check.py:200-304`;
`runtime_probe.py:80-119`; `user_path_failures.py:195-224, :300-359, :384-434, :440-589`; `grounding_table.py:232-286, :355-384,
:1215-1264`; `blast_radius.py:225-254`; `base_slice.py:395-429`; `project_inventory.py:515-544`; `stage_guard.py:88-107, :2225-2269`;
`guard_pre_tool.py:1560-1604`; `validate_artifacts.py:2540-2580`; `probe_by_code.py:2590-2619`; `test_path_grants.py:90-119`;
`diff_pass.py:425-484`; `test_protected_test_path.py:120-143, :300-319`; `test_test_files.py:1-140`; `test-layers.json:1-35, :1874-1895,
:6215-6244, :6966-7005`; `design/architecture.md:30-189, :226-285`; `docs/SIBLING_MAP.md` headings, axis 9 (:228-246), axis 34 (:582-593);
`p1-discovery.md:80-89`; `p2-interview.md:116-131`.
Greps (each with a positive control in the same shape): `test_files|is_test_for|file_kind|production_files|names_a_test|in_test_folder|
test_locations` over `scripts/*.py`; `\.markers\(\)|dir_names|name_marker|dir_marker|...` over the package minus tests; covers lines of
the site files in `test-layers.json` (no `judge_run.py` hit; control `exit_gate.py` hit); `test_locations` in `skills/` (hits p1, p2, p3,
p4, s5); call sites of the blind functions; `load_config\(|...` over six site files; `implementation_checkout|_impl_checkout|
implementation_entries`. Two first-try greps with brace globs over nested paths returned nothing and were re-run without the glob (hits
found) — no negative claim rests on them.
Not read: `docs/TESTING.md` and `plans/builder-rules.md` 7b (their rules taken from CLAUDE.md rule 11 / R11 text auto-loaded and the brief);
`factory-rules.md` full text (FR one-liners from the auto-loaded index); `readiness.py` (item 14 marked UNVERIFIED); spec t-468 consumer
table; `judge_code.py`, `friction.py` (axis 9 open sides, queued).
Needed beyond the manifest: the site files listed above, `diff_pass.py`, `probe_by_code.py`, `test_path_grants.py`, `validate_artifacts.py`,
`test_test_files.py`, `test-layers.json`, onboarding phase files, `config-keys.json`, `templates/config.json`.
