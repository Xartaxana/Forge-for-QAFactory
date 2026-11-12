# t-194 — B-355 nodes B, C, D, F, H, I, J: critic of code (one pass on one topic, R13-g)

Critic (Opus), 12.11.2026. Topic: the project's word decides what a test path is, read through each diff's own checkout.
Spec: `docs/tasks/specs/t-155-b355-project-word-for-test-paths.md` (§2 items 5-15, §3, §4, §5, "Closed", "Decided during the code").
Standing context: `docs/tasks/specs/reviews/t-180-b355-ag-critic.md` (A and G are not re-reviewed here).
Diffs: B `baf572d..bb7756b`, C `bb7756b..3c6620e`, D `890a42f..8866d93`, F `40855ad..0452e89`, H `bae3fe8..9c86d98`,
I `224bca9..33842e9`, J `74a5ca3..704b5e9`. I read every diff in full: code, tests and changelog fragments.

These verdicts are input to acceptance, not acceptance itself. The decision belongs to the coordinator of the proper tier.

## Verdicts

| node | verdict | why, in one line |
|---|---|---|
| B | **fit** | `diff_checkout` is one survivor. The (diff, path) cache and the both-forms `_production_files` follow the Lead's decisions. Rows re-ran green. |
| C | **fit_with_fixes** | The code is right. The item 7 table has three redundant row pairs, and the spec's "config unreadable" row is missing (artifact_root raises). |
| D | **fit_with_fixes** | The code is right on every site I traced. The sibling join is inconsistent: base_slice re-joins through `diff_checkout`, while blast_radius uses its held checkout and leaves it None on `no_record`. The mechanical layer is MISSING. |
| F | **fit_with_fixes (must, regression)** | A config whose application area lies outside the project root (the stand's shape) makes the rehearsal pick nothing in a recorded area and print a false "none of the files lies in the recorded test places". Probe below. The mechanical layer is MISSING. |
| H | **fit_with_fixes** | `published_test_places` drops `not_recorded`, against spec Digest (5) and item 13. The published `note` still names the dropped areas. `test_doctor_context` red is unresolved and owed. |
| I | **fit** | Reads through the one reader. Spelling variants probed and agree. The private helpers it calls kept their signatures through A's fix round. |
| J | **fit_with_fixes (must)** | `/roots/test` is not a pointer any reader reads. Recording a new place into the single-string `tests_root` / `roots.test` OVERWRITES the existing record. `--check --candidate` cannot tell whether a test-repository place is covered. |

Overall (JSON block): `fit_with_fixes`. Nothing is unfixable; every must-fix has its exact fix below.

## Findings

### Node B — fit

There are no findings. What I traced:
- `diff_checkout` (handoff_check.py, after `implementation_checkout`). The order is `manifest_entry_for` by name, then the single-entry
  fallback, then `implementation_checkout`. That equals spec item 5.
- `_impl_checkout` is now `diff_checkout(art.root, "", ...)[0]` under the same `len(entries) == 1` guard. I traced it:
  `manifest_entry_for("")` matches nothing, unless an entry's `diff_path` has an empty basename, and then the single-entry fallback
  takes the same entry as before. The behaviour equals the old `_checkout_path` + `is_dir` code.
- `_production_files`: a str item is exactly today's call. A record item passes `word=cfg, checkout=bound[diff]`, and `bound` is
  cached per diff. "First wins, judged again per diff" is correct: a path excluded by diff 1 can still be counted from diff 2. The
  removed `seen` set is the reason.
- `grounding_table._kind_reader`. The cache key is `(diff, path)`; with no root it is `("", path)`. `index_hunks` passes
  `f["diff"]`, which is the basename (`diff_pass.py:453` `record.update({"diff": name, ...})`). `share` maps `repo` through
  `diff_name_of`, the inverse of `diff_pass.rich`. An unreadable config or an empty `{}` gives the bare call (AR-28).
- All four callers pass `root`: `share_of`, `r6_findings`, `_cmd_share` and `_claim_grounding_share`.

### Node C — fit_with_fixes

**F-C-1 (minor, test quality; known): three redundant row pairs in the item 7 table.** File:
`scripts/tests/test_exit_gate_scope.py`, the `for case, config, bound, want_names, want_clause in (...)` tuple (lines ~661-668 of
the added block). Every row already checks both the list and the clause, so `R`/`R-bound-no-clause`, `N`/`N-no-clause` and
`R-unbound-list`/`R-unbound-clause` are three identical pairs. The dispatch named only the first pair.

Fix: keep one row per case, as `R`, `N`, `R-unbound`, `N-unbound` and `absent-config`. Each keeps its two checks
(`item 7 <case>: list` / `: clause present|absent`).

**F-C-2 (minor, spec row missing): no "config unreadable" row.** Spec item 7 lists "config unreadable -> today's outcome" as a
test row. The builder found that `hooklib.artifact_root()` raises on invalid-JSON or non-object config before `grounding_errors`
reads anything, so the row cannot be expressed end to end. The gate's own fallback (`load_config() or {}` inside try) is right.

Fix: add one row that calls `new_production_files(diff_text, word={}, checkout=None, root=proj7)` and the gate with
`hooklib.load_config` patched to return `{}`. Expected: today's list, no clause. The `artifact_root` hardening is a sibling outside
C's owns: see Queue Q3.

What I traced:
- The clause is appended only for modules that are listed because their diff is unbound under a recorded word, and only when the
  module is in no diff's today list (`all_today`). A bound diff never gets the clause.
- `cfg` empty gives the today list without binding (`listed = ... if cfg else today`).
- A word that records nothing plus an unbound diff gives the today call (A's `_bind`: `recorded(word)` False). The N-unbound row
  pins this.
- runtime_probe: `diff_files(task_root, cfg=None)` reads `load_config()` itself. An explicit `{}` stays `{}`, which is today's
  answer. The callers `execution_request.py:2720` and `gate_preflight.py:4471` are unchanged, and the spec says so.
- `main` reuses the one config it reads.

### Node D — fit_with_fixes

**F-D-1 (should, one road / AR-15): base_slice and blast_radius bind the same diff by two different joins.**
- `base_slice._collect_diff` (base_slice.py:421-425) calls `HC.diff_checkout(ctx.root, name, word, ctx.project)`. The same
  function then computes `state = _repo_state(...)` at :430, which holds `state.checkout` from `HC.implementation_checkout(entry,
  ...)` (:201).
- `blast_radius._new_area` / `_file_sites` pass `rec.checkout` instead. That value is set only at blast_radius.py:195, after the
  `no_record` and `unknown_repo` returns. A diff whose checkout IS found but whose commit is unrecorded gets `checkout=None`, so
  every path of it is "unbound". Under a recorded word every test file of it becomes `production` (noise side, not a lost file).
- Spec item 11 says "both hold ... a per-diff checkout: pass `checkout=<it>`".

Failure scenario: a single-entry manifest whose entry has no `diff_path`, plus a diff `impl-diff.txt`. In base_slice,
`diff_checkout` binds it through the single-entry fallback. In blast_radius, `manifest_entry_for` finds no entry, so `rec.entry`
is None, so `unknown_repo`, so no checkout. The two S3 tools then classify the same file differently under one recorded word.

Fix (one of two, the Lead chooses one road):
- (a) In base_slice, compute `state` before `chosen` and pass `checkout=state.checkout`. In blast_radius, store `found` on `rec`
  before the `no_record` return (`rec.found = found`) and pass that. This is what the spec prescribes.
- (b) Both call `HC.diff_checkout`.

I recommend (a). It is the spec's text, costs no second manifest read per diff, and both tools' own join already decides what
they report.

**F-D-2 (minor, code quality): `import test_locations` inside the per-line loop in arch_check.py:126.** It is cheap after the first
import, but it sits inside `for n, line in ...`. Fix: move it to the module imports (repo_map already imports it at module level,
repo_map.py:50).

**F-D-3 (owed, witness rule): node D has no mechanical layer in the attached file.** The section "Node D t-188" of
`b355-witness-reports.md` is empty. There is no `--witness-for` run, no negative control and no FR walk. My own control re-runs of
D's three row files are green (Trail). The scenario files and the other keep files `--witness-for` prints are owed before
acceptance.

What I traced:
- judge_run passes the parsed config as `cfg`. After A-2, `name` judges by cfg over any area, so this is consistent with A's
  decision.
- An unreadable config gives `{}`, which gives `recorded` False, which gives today's rule.
- project_inventory: phase 1 (`config=None`) is today's rule.
- user_path_failures:
  - `_production` asks the record about `rel` inside the checkout when the label carries a repo id.
  - Every branch falls back to `file_kind(path)`.
  - `_places` resolves without `repo_ids`, and `_bound` is called without them too, so both use the same candidate list.
  - `cfg` is in scope in `_note_files` (:571) and `address_neighbours` (:634).

### Node F — fit_with_fixes (must)

**F-F-1 (must, regression of the G3 class): the record can never name a file outside the project root, so the rehearsal picks
nothing.** File: `gate_preflight.py` `_recorded_test_place`:
`rel = Path(path).resolve().relative_to(Path(project).resolve()).as_posix()`.

For a file under an `app_root` outside the project root, `relative_to` raises and the function returns False. Meanwhile
`_area_recorded` says the area IS recorded (area `app`). Under `app_root "../MyBooks"` and `test_locations ["src/**/*.test.ts"]`
(the stand's shape, spec F-16), a rehearsal whose cwd is in the application tree therefore finds nothing. The caller then prints
the false how-text "none of the files under ... lies in the project's recorded test places". Today it picks `cart.test.ts`.

Probe (`scratchpad/t194/probe_f.py`, run against the b355-f worktree):
```
recorded app/src: (True, ['test_locations'], 'app')
first_test_file(app, cfg, proj) = ''
first_test_file(app) today      = '...\\app\\src\\cart.test.ts'
verdict ../app/src/cart.test.ts: {'test': True, 'by': 'config', 'source': 'test_locations', ...}
```

The verdict itself recognises the file through the `../app/...` spelling. Only the relative-path computation loses it.

Fix: in `_recorded_test_place`, compute
`rel = os.path.relpath(Path(path).resolve(), Path(project).resolve()).replace("\\", "/")`. Keep a `ValueError` (different drives)
as False. Add a row to `test_b355_f_...`: `app_root "../app"`, `test_locations ["src/**/*.test.ts"]`, a scan of `app` gives
`src/cart.test.ts`. Item 12's invariant is "in a recorded area never a file the record does not name". It is not "never a file
the record does name".

**F-F-2 (minor, spec edge unstated): in a mixed-area walk, a World N hit beats an earlier recorded candidate.** `first_test_file`
returns the first World N usual-name hit immediately. A recorded candidate without a usual name is held only as `fallback`. With a
scan root above both areas (`app_root "app"`, `tests_root "tests"`, scan = project root), `app/test_x.py` beats an earlier
`tests/checkout.py`. The spec is silent on a walk that crosses areas. Fix: write the rule in the docstring. Recommended rule: a
recorded candidate in walk order counts the same as a World N hit, and the usual-name preference applies inside a recorded area
only. Alternatively, return the question to the Lead.

**F-F-3 (owed, witness rule): node F has no mechanical layer in the attached file.** The section "Node F t-178" is empty. The
`test_gate_preflight.py` run (over 150 s), the other `--witness-for` files and a negative control are owed. I did not re-run the
slow file: it is outside the control re-run budget.

### Node H — fit_with_fixes

**F-H-1 (must, spec fit / AR-22): `not_recorded` is never published, so the doctor never names a project whose word is missing.**
File: `readiness.py` `published_test_places`:
`areas = {k: v for ... if v.get("status") in ("uncovered", UNKNOWN)}`.

Spec Digest (5) says "the doctor names an old project whose word is missing", and item 13 says "the doctor reads `not_recorded`".
The Lead's decision says "published top-level only when non-ok", and `not_recorded` is non-ok (`check_test_places` ranks it in
`worst`). The builder's t-192 note ("not_recorded, which the spec excludes") misreads the spec. If the t-192 dispatch itself
excluded `not_recorded`, the Lead confirms that here and this finding falls away.

Fix: keep `not_recorded` areas in the filter (`("uncovered", UNKNOWN, "not_recorded")`). Update the K-14 row "nothing recorded ->
key absent" to "nothing recorded -> the area is published with its not_recorded note". This is the named expected edit.

**F-H-2 (minor, consistency): the published row keeps the full `note`, which names the areas the filter dropped.**
`dict(row, areas=areas)` keeps `row["note"]`, which is built from ALL areas, `ok` ones included. SKILL.md says to print each
`note`. Fix: rebuild `note` from the kept areas plus the unreachable sentence, or publish the area notes only.

**F-H-3 (owed, witness rule): `test_doctor_context.py` red is unresolved.** The builder's addendum: the first run ended
`FAILED (failures=1)` with the failing test not captured, and a rerun alone showed no FAIL. The scenario files and 10 other keep
files that `--witness-for` prints were not run (the addendum names them). Owed: a run against 59937ac and 9c86d98 that names the
failing test and says whether it is flaky or caused by H. Until then, the H mechanical layer is incomplete.

**Note (AR-12, not a defect of H):** `compute` now walks up to `DEFAULT_MAX_FILES` (20000) on every `readiness.py` run, including
S0's `--write` and `--require` (driver_s0.py:2343, :2363). The spec accepted the capped walk. The first live run should measure
it (Queue Q4).

### Node I — fit

There are no findings. What I traced:
- `_in_test_root` keeps its refusal guards. It asks `is_test_path(key, cfg, root=_STAND_IN_ROOT)` and passes only when
  `by == "config"`, either from `roots.test`/`tests_root` or from `test_locations` with a live `roots.test`/`tests_root` carrier
  over the same target. That is the Lead's decision. Protected paths still win.
- Spelling probes (`scratchpad/t194/probe_i.py`): `./tests`, `tests/`, `tests\`, `qa/./tests`, `Tests`, the stand's shape with
  `app_root ../MyBooks`, and `tests/a/../x.py` all give True. `roots.test "tests/a/.."` gives False.
- The private `TL._Ctx` / `_target` / `_inside` / `_live_carriers` keep the same signatures on A 224bca9, A 22fe2f2 and I 33842e9
  (grep of `def` lines on all three). The merge is safe.
- Code quality, not blocking: calling four private helpers of another module is a seam. A public
  `test_locations.carriers_over(cfg, root, path, sources)` would remove it. That is A's file: see Queue Q5.

### Node J — fit_with_fixes (must)

**F-J-1 (must, AR-22 / AR-24 / FR-8): `/roots/test` writes a key no reader reads.** File:
`skills/qa-story/phases/s5.md`, the "Record this place for the project" bullet (around lines 250-252 on wip/b355-j):
"`/tests_root`, `/roots/test`, or the pointer of the `run.levels` pattern list".

`roots.test` lives in `profiles[i].roots.test`. `project_decisions._set_pointer` creates missing objects
(`node.setdefault(key, {})`), so `/roots/test` silently writes a top-level `roots` object. The person's word is recorded and read
by nobody.

Fix: write `/profiles/<i>/roots/test` (the index of the profile whose tests live there) and `/run/levels/<level>`. Name these
exact forms in the text.

**F-J-2 (must, the person's word overwrites an earlier one): `tests_root` and `roots.test` hold ONE folder.** "Record this place"
with `--field-values '{"/tests_root": ...}'` REPLACES the existing value. The previously recorded test place silently becomes
unrecorded, and then its tests leave the commit guard and the window claim (G1/G2 widen). The text also names no value to write:
`--check`'s `proposed_value` is the `test_locations` list only (test_locations.py, the `check()` docstring: "the current
`test_locations` list with the candidates appended").

This is a design fork the Lead decides; I recommend the first option:
- **(a, recommended)** For the test repository, "record this place" adds a `run.levels` pattern (an additive carrier) and never
  rewrites `tests_root` / `roots.test`. The value is written as `<p>` with a trailing `/**`, or the file shape where helpers sit
  beside tests.
- **(b)** Write `tests_root` / `roots.test` only when it is the template default (`"."`) or absent, and otherwise ask the person
  which place to keep.

One more point needs the Lead before J is fixed: whether `run.levels` entries are read only as test PLACES, or are also run by
the runners. A new level could change what a run executes. That needs a scout check of the `run.levels` readers.

**F-J-3 (must, FR-11 / FR-15 / AR-8): the command J names cannot answer "is `<p>` covered" for the test repository.**
`test_locations.py --check --candidate` counts `test_locations` entries over a walk of the protected application roots only
(`_scan`, spec §0 F-12). It reports neither coverage by `tests_root` / `roots.test` / `run.levels` nor the counts `<N>/<M>` for a
test-repository place. A conductor following s5.md gets `files: 0`. For a `../`-relative candidate it gets a grammar `problem`.

Fix: either name a reader that answers per area (today no CLI does: the flags are `--suggest` and `--check` only), or, for the
test repository, drop the counts and the "first runs --check" step and say "ask when `<p>` is outside the recorded test-repository
place". The CLI reader is a node-A-class change: see Queue Q5. The same gap sits in G-3's fix (p4 points at
`--check --candidate` for "covered"): see the class note below.

**F-J-4 (minor, cosmetic):** three lines of the record and waiver bullets run past 120 columns (the builder noted it). Fix: rewrap
them.

## Known small fixes the dispatch asked to include

- **F-G-dup** — `ai-packages/qa-factory/skills/qa-onboarding/phases/p4-generate.md:92` on wip/b355-g. The line lists `tests_root`
  twice: "... in `tests_root` / the profile's `roots.test` / `run.levels`, `tests_root`," (read via `git show wip/b355-g:...`).
  Fix: drop the second `` `tests_root`, ``. Path corrected per the coordinator: `phases/`, not `references/`.
- **F-C-1** — above.

## Merge-only behaviour (for the integrator; I merged nothing)

- **No textual overlap.** The owned files are disjoint across B, C, D, F, H, I and J. `test_test_files.py` is serial (A
  22fe2f2, then D). `judgment-census.json` is H only.
- **The A fix round (22fe2f2) and the nodes built on 224bca9 (C via B, F, I, H's base).** A's fix round changed `recorded_names`,
  the `name` binding and `_folder_kind`. Of these nodes, only judge_run (D, already on 22fe2f2) calls `name` with a config;
  gate_preflight `_spelled_as_a_test` calls it bare. I's private helpers keep their signatures. I see no behaviour that appears
  only after the merge. **The integrator must run** `test_test_files`, `test_test_locations`, `test_probe_by_code`,
  `test_gate_preflight` and `test_exit_gate_scope` on the converged branch, because C, F and I were never run against 22fe2f2.
- **After merge, runtime_probe.diff_files reads the project config by default.** `gate_preflight.py:4471` (F's file, not edited
  there) and `execution_request.py:2720` therefore change behaviour under a recorded word. This is intended (spec item 8), but the
  gate_preflight rows for :4471 were never run with a recorded config. The integrator's canon covers it.

## Standing questions

**DUPLICATION AND CONSISTENCY** (brief item 6): found, and named in F-D-1 and Q5.
- F-D-1: two joins for one diff inside S3.
- Q5: node I reads four privates of test_locations instead of a public reader.
- Positive: every diff site goes through `test_files` with `word`/`checkout` and through `handoff_check.diff_checkout`. The grep
  over `scripts/*.py` (Trail) shows no site calling `file_kind` / `production_files` bare where the spec asks for the word, except
  the stated fallbacks, gate_preflight `_spelled_as_a_test` (an order hint, F-14) and the out-of-scope readers (stage_guard,
  guard_pre_tool, validate_artifacts: no edit by spec).
- No new folder-name tuple: the grep for `dir_names|dir_suffixes|name_marker|dir_marker` in the seven diffs found none.

**CODE QUALITY** (brief item 7):
- F-D-2 (import in a loop).
- F-C-1 (redundant rows).
- F-H-2 (stale note).
- `check_test_places` is about 95 lines with several branches. It is acceptable as one capability, but it is the next candidate
  for a split into `_area_rows` / `_unreachable`. Not blocking.
- B's `_kind_reader` and C's `_diff_checkouts` both wrap `diff_checkout` with a per-diff cache. They are small and per-module
  (different keys), so I accept them.

**JUDGMENT (q10/q11, AR-29, P27):**
- Every altered check judges data: presence of a carrier for an area, and a path join.
- `check_test_places` reports and blocks nothing. Its census row is `xref` / `intent` / conductor, and `test_judgment_census` is
  green per H's witness.
- J keeps the question with the person and the decision with the conductor's reading of their words.

**ONE ROAD (item 12, P31):**
- There is no language or project branch.
- One residual: F-D-1, two roads to "diff to checkout" inside S3. Proposed as a fix of this round (D), not as a line to pass on.
- J's area-dependent question (four options in the application tree, three in the test repository) follows the Lead's decision
  and the existing protected-path consent. It is not an exclusion.

## Class-wide completeness (spec §5 and SIBLING_MAP axes 9, 10, 34)

| sibling | status |
|---|---|
| Blind sites F-7: judge_run, gate_preflight, exit_gate, runtime_probe, user_path_failures (6 sites), grounding_table, blast_radius, base_slice, project_inventory, handoff_check | applied by B/C/D/F. Verified by the grep of `file_kind(` / `is_test_for(` / `production_files(` in the D worktree; the positive control is the known `stage_guard.py:2260` hit |
| `test_body` advice readers: arch_check :124, repo_map :244 | applied (D) |
| `probe_by_code._in_test_root` | applied (I) |
| Axis 10: `_impl_checkout` through `diff_checkout` | applied (B); `context_bundle.build`, `judge_diff._diff_files`, `grounding_table.diff_records` copies are queued (spec §5; B's report) |
| Own diff parse `runtime_probe.diff_files` regex | queued (spec §5), unchanged |
| Onboarding / S5 producers of the word (G, J) | J must-fixes F-J-1..3. The same "covered" gap exists in G-3's fix (p4 points at `--check --candidate`): class note, queued Q5 |
| `execution_request.profiles_owning` still reads `roots.test` itself (diverges from `_in_test_root` for `.` / above-root) | not covered; queued Q2 (I's report) |
| `hooklib.artifact_root` raises on corrupt config before readers fall back | queued Q3 |

## Queue (outside the nodes' owns; not part of the verdict)

- **Q1.** `execution_request.py:1618` docstring still describes the older `_path_key` reading (I's report).
- **Q2.** `execution_request.profiles_owning` reads `roots.test` on its own. Fold it through the same reader as `_in_test_root`
  (axis 9/10 class: two readers of one key).
- **Q3.** `hooklib.artifact_root()` raises on invalid-JSON or non-object config, while `load_config` falls back to `{}` (C's
  report). That is two readers of one file with two error directions.
- **Q4.** AR-12: measure the `check_test_places` walk cost at S0 (`readiness.py --write` / `--require`) in the first live run.
- **Q5.** Node A's file (`test_locations.py`) lacks two public readers:
  - `carriers_over(cfg, root, path, sources)`, which would remove I's private calls;
  - a CLI `--covered <p>` (per area), which J (F-J-3) and G-3's p4 sentence both need.
  This is one mechanism instead of two prose workarounds. Proposed node in onboarding-hooks, owner: the Lead.
- **Q6.** FR-33: H's doctor row and J's s5.md prose are "closed by code, not proved". Their rows go to `live-runs`.

## Trail

**Read:**
- the spec t-155 in full (544 lines);
- the review t-180 in full;
- the witness file `b355-witness-reports.md` in full (D and F sections are EMPTY) plus the coordinator's H addendum;
- all seven diffs in full;
- handoff_check.py :200-265 (b355-b);
- grounding_table.py :258-292, :385-412 (b355-b);
- hooklib.py `load_config` (b355-b);
- test_files.py `_bind`, `is_test_for`, `file_kind`, `production_files` (b355-a 22fe2f2);
- test_locations.py `check()` :815-870 and the CLI :880-930 (b355-a);
- blast_radius.py :128-200 (b355-d);
- base_slice.py :180-215, :416-430 (b355-d);
- user_path_failures.py :500-575, cfg scope :571/:634 (b355-d);
- project_decisions.py :225-280, :355-386, :440-480 (b355-j);
- `git show wip/b355-g:.../p4-generate.md` :89-94;
- `tools/critic_verdict.schema.json`;
- `docs/tasks/critic-diff-brief.md` headings.

**Greps (positive controls in the same shape):**
- `file_kind(|is_test_for(|production_files(` over b355-d `scripts/*.py` (-i): every expected site hit. The positive control is
  the known untouched `stage_guard.py:2260` and `guard_pre_tool.py:1599` lines, found by the same call. This is the basis for the
  "no bare site left" claim.
- `first_test_file(|_test_area(|wanted_names(|_names_a_test(` (-i): one caller each. In the b355-d tree `gate_preflight.py:3656`
  shows the OLD bare call (F not merged there), which is the merge note above.
- `def _live_carriers|def _target|def _inside|class _Ctx` on three commits: all present, same signatures.
- `field.ref|field_ref|allowed` in project_decisions.py: no allowlist. Any pointer is accepted and created, which is the basis of
  F-J-1.
- `readiness\.compute|readiness.py` callers: S0 driver lines (Q4).

**Probes (scratchpad `C:\Users\i_mas\AppData\Local\Temp\claude\b3e3188b390a00d9\acb1ecf0-04a8-42f3-8bdd-f14a2dae87bf\scratchpad\t194\`):**
- `probe_f.py` gives F-F-1 (output above).
- `probe_i.py` gives 9 spelling rows for I (output above).

**Control re-runs (worktrees, `python -B scripts/tests/<file>.py` from the package dir in a subshell):** see the JSON block.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "verdicts": {"B": "fit", "C": "fit_with_fixes", "D": "fit_with_fixes", "F": "fit_with_fixes", "H": "fit_with_fixes", "I": "fit", "J": "fit_with_fixes"},
  "class_completeness": "Spec 5 blind sites F-7 all wired (B grounding_table/handoff_check; C exit_gate/runtime_probe; D user_path_failures, blast_radius, base_slice, judge_run, project_inventory, arch_check, repo_map; F gate_preflight; I probe_by_code), grep-verified with positive control. Gaps: F-D-1 two joins for one diff in S3 (base_slice diff_checkout vs blast_radius held rec.checkout, None on no_record); F-J-3 and G-3 share the missing per-area covered reader (Q5); queued Q1-Q3 (execution_request docstring and profiles_owning, artifact_root error direction) and spec-5 axis-10 copies.",
  "fixes": [
    "F-C-1 test_exit_gate_scope.py item 7 table: collapse the three identical pairs (R/R-bound-no-clause, N/N-no-clause, R-unbound-list/R-unbound-clause) to one row per case",
    "F-C-2 test_exit_gate_scope.py: add the config-unreadable row (load_config patched to an empty dict, today's list, no clause)",
    "F-D-1 base_slice._collect_diff: compute state before chosen and pass checkout=state.checkout; blast_radius._classify: keep the found checkout on rec before the no_record return and pass it to _kind (or both call HC.diff_checkout - Lead picks one road)",
    "F-D-2 arch_check.py:126: move import test_locations to the module imports",
    "F-D-3 attach node D's mechanical layer: scenario_walk --witness-for runs and a negative control",
    "F-F-1 gate_preflight._recorded_test_place: rel = os.path.relpath(resolved path, resolved project) with forward slashes, ValueError means False; add the row app_root ../app with test_locations src/**/*.test.ts picks src/cart.test.ts",
    "F-F-2 gate_preflight.first_test_file: state the mixed-area walk rule in the docstring (recorded candidate in walk order equals a World N hit) or return the question",
    "F-F-3 attach node F's mechanical layer: test_gate_preflight run, the other witness-for files, a negative control",
    "F-H-1 readiness.published_test_places: keep not_recorded areas; update the K-14 key-absent row (named expected edit), unless the Lead confirms t-192 excluded not_recorded",
    "F-H-2 readiness.published_test_places: rebuild note from the kept areas plus the unreachable sentence",
    "F-H-3 run test_doctor_context.py against 59937ac and 9c86d98, name the failing test, and run the 3 scenario files and remaining keep files",
    "F-J-1 s5.md record bullet: pointers /profiles/<i>/roots/test and /run/levels/<level>, never /roots/test",
    "F-J-2 s5.md record bullet: never overwrite the single-string tests_root or roots.test; recommended: add a run.levels pattern (Lead fork; scout the run.levels readers first)",
    "F-J-3 s5.md: drop the --check coverage and counts step for the test repository, or name a per-area reader (Q5)",
    "F-J-4 s5.md: rewrap the three lines over 120 columns",
    "F-G-dup skills/qa-onboarding/phases/p4-generate.md:92 on wip/b355-g: drop the second tests_root"
  ],
  "queue": [
    "Q1 execution_request.py:1618 docstring describes the old _path_key reading",
    "Q2 execution_request.profiles_owning reads roots.test on its own; fold through the one reader",
    "Q3 hooklib.artifact_root raises on a corrupt config while load_config falls back to an empty dict",
    "Q4 AR-12: measure the check_test_places walk at S0 in the first live run",
    "Q5 test_locations public readers: carriers_over for node I, a per-area covered CLI for J and G-3 (one mechanism, owner Lead)",
    "Q6 FR-33: H doctor row and J s5.md prose rows go to live-runs"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/t-155-b355-project-word-for-test-paths.md",
      "docs/tasks/specs/reviews/t-180-b355-ag-critic.md",
      "scratchpad/b355-witness-reports.md",
      "git diff baf572d..bb7756b",
      "git diff bb7756b..3c6620e",
      "git diff 890a42f..8866d93",
      "git diff 40855ad..0452e89",
      "git diff bae3fe8..9c86d98",
      "git diff 224bca9..33842e9",
      "git diff 74a5ca3..704b5e9",
      "b355-b handoff_check.py:200-265, grounding_table.py:258-292,385-412, hooklib.load_config",
      "b355-a test_files.py _bind/is_test_for/file_kind/production_files, test_locations.py check() and CLI",
      "b355-d blast_radius.py:128-200, base_slice.py:180-215,416-430, user_path_failures.py:500-575",
      "b355-j project_decisions.py _refs/_set_pointer/resolve",
      "wip/b355-g p4-generate.md:89-94",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "python -B .claude/worktrees/b355-b/.../tests/test_handoff.py", "result": "=== test_handoff: 602/602 ok ==="},
      {"command": "python -B .claude/worktrees/b355-b/.../tests/test_grounding_table.py", "result": "=== test_grounding_table: 222/222 ok ==="},
      {"command": "python -B .claude/worktrees/b355-c/.../tests/test_exit_gate_scope.py", "result": "=== test_exit_gate_scope: 108/108 ok ==="},
      {"command": "python -B .claude/worktrees/b355-c/.../tests/test_runtime_probe_onboarding.py", "result": "=== test_runtime_probe_onboarding: 702/702 ok ==="},
      {"command": "python -B .claude/worktrees/b355-d/.../tests/test_flow_requests.py", "result": "=== flow requests: 94/94 ok ==="},
      {"command": "python -B .claude/worktrees/b355-d/.../tests/test_test_files.py", "result": "=== test_test_files: 186/186 ok ==="},
      {"command": "python -B .claude/worktrees/b355-d/.../tests/test_arch_check.py", "result": "=== test_arch_check: 42/42 ok ==="},
      {"command": "python -B .claude/worktrees/b355-i/.../tests/test_probe_by_code.py", "result": "=== test_probe_by_code: 776/776 ok ==="},
      {"command": "python -B .claude/worktrees/b355-h/.../tests/test_readiness.py", "result": "=== test_readiness: 265/265 ok ==="},
      {"command": "python -B scratchpad/t194/probe_f.py <b355-f package>", "result": "recorded app/src True app; first_test_file(app, cfg, proj) empty; today picks src/cart.test.ts; verdict of ../app/src/cart.test.ts test True by config"},
      {"command": "python -B scratchpad/t194/probe_i.py <b355-i package>", "result": "./tests, tests/, tests backslash, qa/./tests, Tests, stand shape, tests/a/../x.py all True; roots.test tests/a/.. False"}
    ]
  }
}
```
