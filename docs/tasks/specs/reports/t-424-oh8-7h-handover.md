# t-424 OH8-7h handover (builder, Sonnet 5.5)

Worktree C:\QAFactory\forge-repo\.claude\worktrees\oh8-7b (wip/oh8-7b, HEAD 5e603e4). Everything is STAGED, nothing committed.
No question is open: the removal was done (items 2-8 below).

## 1. Step 0 (re-measure), verbatim

Command: `python -B <scratchpad>/remeasure.py <wt>/ai-packages/qa-factory <scratchpad>/oh8-7h-list.txt <scratchpad>/oh8-7h-list.txt --last`
(oh8-7h-list.txt = the last 21 lines of oh8-7g-h.txt; both list arguments are the same file, as the spec says for OH8-7h).
The source of remeasure.py is the script of spec 3.2 with the Lead fix of 2026-11-13 (t-369); path C:\Users\i_mas\AppData\Local\Temp\claude\b3e3188b390a00d9\acb1ecf0-04a8-42f3-8bdd-f14a2dae87bf\scratchpad\remeasure.py.

```
pending total: 21 | ceiling on this tree: 21
node files pending: 21 | spec list: 21
missing from the tree: none
extra on the tree: none
pending names in no remaining node: none
listing would also create: none
whole tree, neither unit nor pending: none | pending total == 21: True
in the node's files, owned by a later node: 0
exit=0
```

## 2. §3.5 item 1: the 21 rows, ceiling 0, BEFORE the removal (green)

Edits for this run: ten whole-file entries added to SUBCLASS_UNIT_FILES (hooklib, controller, story_step, event_store, retro_numbers, host_adapter, role_load, release_fingerprint, selftest, config_view), SUBCLASS_PENDING_CEILING 21 -> 0, 21 rows, ratchet raised. Output of `( cd <wt>/ai-packages/qa-factory && python -B scripts/tests/test_judgment_census.py )`, saved in scratchpad item1.txt:

```
PASS test_c1_every_unit_has_a_row_and_every_row_a_unit
PASS test_c2_every_row_is_well_formed
PASS test_c3_the_ratchet_is_dense_and_only_shrinks
PASS test_c4_the_meaning_ceiling_is_the_tests_constant
PASS test_c5_no_refusal_hides_behind_a_wrapper
census: 279 files scanned, 1141 units; shape=832 xref=195 word-list=0 meaning-proxy=8 meaning=24 safety=82; breach=1; blocks_overrides=10; blocking_per_role: conductor=680 qa-automator=173 qa-bug-reporter=139 qa-case-critic=164 qa-case-designer=139 qa-code-critic=139 qa-doc-scribe=139 qa-failure-analyst=140 qa-requirements-tester=157 qa-retro-analyst=139 qa-runner=140 qa-scout=139 qa-test-strategist=171; subclass_family=55 subclass_pending=0 (ceiling 0); SCAN_ROOT='scripts' SCAN_EXCLUDE=('tests',)
census breaches: validate_artifacts.py::check_behaviour_claims
PASS test_c6_totals_line ... (26 PASS lines in all)
=== judgment_census: 26/26 ok ===
exit=0
```

(I did not run the intermediate "rows not yet written" C1 listing: the step-0 output already proves the list is exactly the 21 pending names and that listing creates nothing else.)

## 3. Final witness (after the removal, ONE run after the last edit)

`( cd <wt> && python -m pytest ai-packages/qa-factory/scripts/tests/test_judgment_census.py -q -s )`:

```
census: 279 files scanned, 1141 units; shape=832 xref=195 word-list=0 meaning-proxy=8 meaning=24 safety=82; breach=1; blocks_overrides=10; blocking_per_role: conductor=680 qa-automator=173 ... qa-test-strategist=171; subclass_family=55; SCAN_ROOT='scripts' SCAN_EXCLUDE=('tests',)
census breaches: validate_artifacts.py::check_behaviour_claims
24 passed in 76.42s (0:01:16)
```
Test count: 26 before the removal -> 24 after (the two removed: test_c7_the_subclass_pending_set_is_dense_and_only_shrinks, test_neg_pending_is_dense_and_only_shrinks_c7). 1141 units both before and after: the removal created no unit outside the 21 rows (no "listing would also create" case, C1 green).

Other DoD runs:
```
( cd <wt>/ai-packages/qa-factory && python -B scripts/selftest.py --limits --lang )
  PASS limits: SKILL.md / agents / references within size caps
  PASS limits: every mandatory role rule of design/role-rules.json holds in its carrier
  === qa-factory selftest: 4/4 ok ===
( cd <wt> && python tools/lint_ratchet.py --check )
  lint ratchet: 36 findings, 36 in the baseline, 0 new, 0 stale (pyflakes 3.2.0)
tools/test_sibling_map.py does not exist (checked: ls -> No such file). The tests that name SIBLING_MAP: tools/test_digest_form.py, test_language_sites.py, test_mechanism_gate.py, test_quarantine.py, test_split.py, test_wiring_check.py. The one that reads the map's axes is the gate test:
( cd <wt> && python -m pytest tools/test_mechanism_gate.py -q )  ->  480 passed in 11.93s
grep -c "^## Axis" docs/SIBLING_MAP.md -> 36 (unchanged)
```

Reconcile (`python -B <scratchpad>/reconcile.py <wt>`, source: scratchpad reconcile.py, 22 lines, pure read; exit 0):
```
new rows: 21 | removed rows: 0
existing rows unchanged: True
probe_by_code.py rows sorted ...: True
blocking_per_role.qa-automator: 169 -> 173; new rows naming it: 4 OK
blocking_per_role.qa-bug-reporter: 135 -> 139; new rows naming it: 4 OK
blocking_per_role.qa-case-critic: 160 -> 164; new rows naming it: 4 OK
blocking_per_role.qa-case-designer: 135 -> 139; new rows naming it: 4 OK
blocking_per_role.qa-code-critic: 135 -> 139; new rows naming it: 4 OK
blocking_per_role.qa-doc-scribe: 135 -> 139; new rows naming it: 4 OK
blocking_per_role.qa-failure-analyst: 136 -> 140; new rows naming it: 4 OK
blocking_per_role.qa-requirements-tester: 153 -> 157; new rows naming it: 4 OK
blocking_per_role.qa-retro-analyst: 135 -> 139; new rows naming it: 4 OK
blocking_per_role.qa-runner: 136 -> 140; new rows naming it: 4 OK
blocking_per_role.qa-scout: 135 -> 139; new rows naming it: 4 OK
blocking_per_role.qa-test-strategist: 167 -> 171; new rows naming it: 4 OK
blocking_per_role.conductor: 659 -> 680; new rows naming it: 21 OK
safety: 81 -> 82; new safety rows: 1 OK
other ratchet keys changed: none
about changed: True   (the blind-spot text, item 4: expected)
```

Doc-dispatch witness for docs/SIBLING_MAP.md and docs/tasks/critic-diff-brief.md (keys quoted from the DoD/spec 3.3 item 9, OH8-7h, before the run; script dockeys7h.py, full source below; C:\Users\i_mas\AppData\Local\Temp\claude\b3e3188b390a00d9\acb1ecf0-04a8-42f3-8bdd-f14a2dae87bf\scratchpad\dockeys7h.py):
```
OK   SIBLING_MAP present OH8-7h
OK   SIBLING_MAP absent SUBCLASS_UNIT_FILES
OK   SIBLING_MAP absent SUBCLASS_PENDING_CEILING
OK   brief absent SUBCLASS_PENDING_CEILING
OK   brief absent SUBCLASS_UNIT_FILES
exit=0
negative control (--negative: a key that is absent demanded present):
FAIL NEGATIVE CONTROL SIBLING_MAP present OH8-7z-no-such-key
... exit=1
```
Source of dockeys7h.py:
```python
import sys
from pathlib import Path
wt = Path(sys.argv[1])
neg = len(sys.argv) > 2 and sys.argv[2] == "--negative"
sm = (wt / "docs/SIBLING_MAP.md").read_text(encoding="utf-8")
br = (wt / "docs/tasks/critic-diff-brief.md").read_text(encoding="utf-8")
keys = [("SIBLING_MAP present", "OH8-7h", sm, True),
        ("SIBLING_MAP absent", "SUBCLASS_UNIT_FILES", sm, False),
        ("SIBLING_MAP absent", "SUBCLASS_PENDING_CEILING", sm, False),
        ("brief absent", "SUBCLASS_PENDING_CEILING", br, False),
        ("brief absent", "SUBCLASS_UNIT_FILES", br, False)]
if neg:
    keys[0] = ("NEGATIVE CONTROL SIBLING_MAP present", "OH8-7z-no-such-key", sm, True)
bad = 0
for label, key, text, want in keys:
    ok = (key in text) == want
    print(("OK  " if ok else "FAIL"), label, key)
    bad += not ok
sys.exit(1 if bad else 0)
```
DoD 8 of the spec (one scanner): `refusal_registry.py` not in the diff (stat below); `grep -n "ast.Raise" test_judgment_census.py` -> no hit; positive control on `refusal_registry.py` -> line 1086 `elif isinstance(node, ast.Raise) and isinstance(node.exc, ast.Call)`.

`git -C <wt> diff --cached --stat`:
```
 .../scripts/tests/fixtures/judgment-census.json    |  25 +-
 .../scripts/tests/test_judgment_census.py          | 289 ++++++---------------
 docs/SIBLING_MAP.md                                |   4 +-
 docs/tasks/critic-diff-brief.md                    |   4 +-
 4 files changed, 103 insertions(+), 219 deletions(-)
```
The fixture diff holds only: the 21 inserted rows, the `about` line, the `ratchet` line.

## 4. The 21 rows, one line each (form of 4.2 item 6)

- hooklib.py::read_config_file -- shape, [all 12 roles + conductor], data -- config.json readable / non-empty / depth / valid JSON / an object (presence and form); roles follow hooklib.artifact_root (rows 447-448: it calls this function on every hook path)
- hooklib.py::story_of -- shape, [all 12 roles + conductor], data -- which of the two flags was given, same folder for both (samefile); roles follow hooklib.artifacts_dir (story folder resolver family, called by validate_artifacts.py and exit_gate.py hooks)
- hooklib.py::story_root -- shape, [all], data -- a key is one non-empty path component, a project is given and is a project, the folder exists; reads only (writes nothing)
- hooklib.py::story_root_at -- shape, [all], data -- a non-empty path to an existing story folder (isdir / samefile); reads only
- controller.py::refresh_derived -- shape, [conductor], data -- the derived-view refresh after a commit completed or not (a failure becomes DerivedViewStale: "event committed, do not repeat")
- event_store.py::_require_root -- shape, [conductor], data -- the story folder exists before a journal write (presence)
- event_store.py::_run_after_commit -- shape, [conductor], data -- the after-commit step completed or not (the twin of refresh_derived)
- retro_numbers.py::write_retro -- shape, [conductor], data -- the story folder given exists before the retro is written (presence)
- host_adapter.py::launch_id_keys -- shape, [conductor], data -- the data row `launch_id_keys` is readable, a non-empty list of non-empty texts
- role_load.py::_check_kind -- shape, [conductor], data -- the dispatch kind is one of the closed tokens KINDS (rule 3, a closed token)
- role_load.py::_pick_dispatch -- xref, [conductor], data -- a dispatch id resolves in state/controller.json and belongs to the role (a join)
- role_load.py::_require_role -- xref, [conductor], data -- the role name is a key of inject-map.json (a join with a data file)
- role_load.py::_task_root -- shape, [conductor], data -- one path component and the story folder exists; the function only READS (rule 2: read path = shape)
- role_load.py::main -- shape, [conductor], data -- flag combination (--all with --role/--story/--dispatch, --dispatch without --story, --role absent); every RoleLoadError becomes exit 2
- role_load.py::settings -- shape, [conductor], data -- references/role-load.json readable and well-formed
- release_fingerprint.py::_unshipped -- shape, [conductor], data -- the git listing of the clone exited 0 (presence of the evidence, FR-59); not a guard on git state: it reads
- release_fingerprint.py::write_release -- xref, [conductor], data -- plugin.json version of the form N.N.N (shape), recipe files vs the git index (join; the higher reading), no litter-named file (shape)
- selftest.py::slow_tests -- shape, [conductor], data -- the slow-test list file is present, JSON, and of the documented form
- selftest.py::test_layers -- shape, [conductor], data -- test-layers.json is JSON and of the form layers_problems accepts
- config_view.py::parse_path -- shape, [conductor], data -- syntax of a config path (empty part, bad pointer escape, a path Git Bash already rewrote)
- story_step.py::start -- safety, [conductor], data -- BY LEAD RULE 1 (see below): a dispatch id already committed with other fields is refused and the committed dispatch is not replaced

Class counts from my rows: 17 shape, 3 xref, 1 safety (= 21).
Roles: rule 5 (existing rows of the same file) everywhere; the four hooklib rows follow the hooklib rows that stand on the hook path (artifact_root, artifacts_dir, append_jsonl_line: all roles + conductor). The other nine files' rows are [conductor] as every existing row of the same file.
E3 rows (every raise caught inside its own module and turned into an answer): none. The candidates all leave the function as a refusal: role_load.main and config_view.main print an error and return an exit code (4.2 step 2: a CLI exit is a refusal); selftest, release_fingerprint, hooklib, host_adapter, event_store, controller errors leave the module (tools/test_quarantine.py imports slow_tests and test_layers).
Rows that were already covered by an existing row: none (every one of the 21 had no row).

## 5. BY LEAD RULE

- story_step.py::start -> safety, [conductor], data -- rule 1 (a refusal of a second writer / an overwrite: claim). Raise line: story_step.py:963 `raise IdempotencyKeyReused(f"{exc}. The committed dispatch is not replaced; ...")`; condition: `except IdempotencyKeyReused as exc: ... if exc.key != "dispatch:" + dispatch_id: raise` (bare re-raise for another key), so the sited raise is for the committed `dispatch:<id>` key reused with other fields. Why not plain: see QUESTIONS (flagged, not blocking).
- Rules 2-4 applied without a safety result: role_load._task_root (rule 2, read path -> shape), hooklib.story_root / story_root_at / story_of (rule 2: they only read, "Nothing is created and nothing is written" -> shape; same class as the existing row hooklib.artifacts_dir), role_load._check_kind and _require_role (rule 3: closed tokens), config presence/shape rows (rule 4).

## 6. QUESTIONS (4.3), none blocking; all for the critic / Lead to re-judge, rows are written

1. story_step.py::start (safety by rule 1). Raise: story_step.py:963 (`IdempotencyKeyReused(...)` re-raised with the door text). Proposed class safety / [conductor] / data. Why not plain: the same refusal raised at controller.py:5151-5161 sits in the EXISTING row controller.py::apply, which is `shape` (the condition compares two requests under one idempotency key, which reads as xref/shape). Rule 1 ("refuses an overwrite / claim") makes it safety; I took rule 1, the higher class, which is the safe side of the ratchet. Re-judging it to shape/xref would lower `safety` 82 -> 81. If you prefer P31 consistency with `apply`, both belong to the "one class node after the chain" (6b).
2. hooklib.py story_root / story_root_at / story_of roles: I took all roles + conductor (the hook-path row family, the existing artifacts_dir row is identical). If the class node that re-derives roles finds them conductor-only the 12 role keys fall by 4 each (they are written as ratchet keys now).
3. hooklib.py::story_root / story_root_at (and role_load._task_root, release_fingerprint._unshipped) carry a path-escape or git-listing reading: I judged them shape by rule 2 (read-only path) and by "the condition is the presence of the evidence". If the later written-path-guard class node (6b) wants `hooklib.story_root` together with `artifacts_dir`, it should add them to its list (they are not on the 6b list today).

## 7. §3.5 removal checklist

1. First the 21 rows with the ceiling at 0, green: done (section 2 above).
2. Removal in the same change: done in `test_judgment_census.py`: constants `SUBCLASS_UNIT_FILES`, `SUBCLASS_PENDING_CEILING`, function `_c7`, keywords `unit_files` / `pending_ceiling` of `units_of` (`unit_files`) and `analyse` (`unit_files`, `pending_ceiling`), totals `pending` / `pending_names`, units_of keys `pending` and `list_problems`, the problem key `C7` (the `probs` dict now holds C1..C5), the list-form checks, the two tests `test_c7_the_subclass_pending_set_is_dense_and_only_shrinks` and `test_neg_pending_is_dense_and_only_shrinks_c7` with their TESTS entries and the table C7_LISTS / C7_NEUTRAL, the pending branch of the flip loop, both `setdefault` lines of `_run`. Every scanned file creates units from the widened sites (`for s in wide_by_file.get(file, []): add(file, s["function"], "u3")`); `seen` / `sites_by_file` (the literal-only scan) are gone, `totals["sites"]` = len(widened sites) (spec 7 C-3). `totals_line` keeps `subclass_family=` and drops `subclass_pending=`.
3. `SUBCLASS_ROWS`: columns `pending` and `unit_files` and the seven `listed_*` rows gone; each row is (id, files, blocking) with ids; body as specified (neutral_only: no row -> C1 names `helpers_x.py::f is a check unit (u3)` and blocking_units 0; with `_row("helpers_x.py", "f")` -> C1 silent and blocking_units 1; every other case: row check_f, blocking_units == blocking, C1 does not name `helpers_x.py::f`). The test function is renamed `test_neg_subclass_raises_flip_blocks_or_are_pending` -> `test_neg_subclass_raises_flip_blocks_and_create_units` (its old name said "pending"; grep of the old name: only the test file itself and a .pytest_cache nodeids file; this rename is a deviation from the spec text, which only names the body).
4. Texts: u3 docstring line, the blind-spot paragraph, `BLIND_SPOT` and the fixture `about`: done. They say that a raise through a package subclass (resolved per file) or the attribute form is a refusal site like a literal raise (OH8-7h) and that "every WIDENED raise site creates a unit"; the "still unseen" list stays and gains the clause "a raise of a call to a module factory function that returns the family exception (`raise _held_by(...)`): the scanner does not see that form; 52 rowless functions carry such a raise on 097f58d (an upper bound; `exploration.py::acquire` is one)". No sentence says or implies that every refusal site creates a unit. `test_blind_spot_states_the_subclass_clause` asserts present: `subclass`, `stdlib`, `` `raise a()` ``, `factory function` (the chosen token: the two-word `factory function`, which the other texts never use alone); absent: `pending`, `oh8-7b`, `subclass_unit_files`; and `subclass_family=` present / `pending` absent in `totals_line`. (The old needle "flips `blocks`" was dropped: the sentence it needed is gone.)
5. docs/SIBLING_MAP.md: axis 18's member text: the two clauses "since OH8-7" and "since OH8-7b" are replaced by one "since OH8-7h ... the census creates units from every widened raise site ...; the temporary constants of the chain are gone" (no constant names); axis 34's "known roads off it": the line added by OH8-7b is removed (done).
6. The AR-22 grep, zero hits: `grep -rnE "subclass_pending|SUBCLASS_PENDING|pending_names|SUBCLASS_UNIT_FILES" <wt>/ai-packages <wt>/tools <wt>/PROCESS <wt>/.github <wt>/docs/SIBLING_MAP.md <wt>/docs/tasks/critic-diff-brief.md <wt>/CLAUDE.md <wt>/PROJECT.md` -> (no output), `hits-exit=1`. Positive control, same dirs, same flags, pattern `subclass_family`: `ai-packages/qa-factory/scripts/tests/test_judgment_census.py:463:  f"subclass_family={t['family']}; "` and `:834: assert "subclass_family=" in line and "pending" not in line, line`. (To make the grep zero the test asserts `"pending" not in line`, not the `subclass_pending=` token.)
7. Readers of `C7` / `pending` / `SUBCLASS_PENDING_CEILING`: `grep -rnE "SUBCLASS_PENDING_CEILING|SUBCLASS_UNIT_FILES|subclass_pending|pending_names|\bC7\b" <wt>/tools <wt>/PROCESS <wt>/.github <wt>/docs` minus docs/tasks and docs/specs: hits only tools/language_sites.py (its own check "C7 a script that does not parse"), tools/source-split-carriers.json l.41 (an unrelated id "C7"), and docs/SIBLING_MAP.md l.390 and l.588 (the two clauses I rewrote). Readers of the census module: tools/architecture_gate.py (the `ratchet` object only), tools/source_split.py (calls `analyse(root, census)` and reads `totals["counts"]` and `totals["blocking_per_role"]` only -- checked at source_split.py:2196-2199; the `analyse` signature keeps its first two positional parameters), tools/source-split-carriers.json (`entry: analyse`), PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md l.1087 (check 41 text; no constant name hit by the pattern). Positive control: the same grep finds the SIBLING_MAP l.390 / l.588 clauses before the edit and the tools hits listed. No reader outside the two test files: no stop.
8. docs/tasks/critic-diff-brief.md: question 9's list lost `SUBCLASS_PENDING_CEILING`; question 11's list lost both names (done; grep shown in section 3: both keys absent).

Edge checks: step 0 equals the 21 of the list file (no stop). After the removal the census reports 1141 units, the same as before it: no unit outside the 21 rows (C1 green), so no node-list orphan.

## 8. Judgment line form (read tools/architecture_gate.py)

The gate (docstring item 6/7 (v), ADDS_RE `adds data check <unit> -- <why>`) takes a raise of only `blocking_per_role.*` and/or `safety` with `judgment: adds data check <unit> -- <why>`. This commit raises only those keys, so the form used is `judgment: adds data check test_judgment_census.units_of -- ...` (SUBCLASS_UNIT_FILES no longer exists after this commit, so it cannot be the unit token; `units_of` is the unit road that now makes every widened site a unit). The removal of the two constants lowers no ceiling and the gate has no form for "removes a scan constant"; the message says in one sentence that the two constants die as specified in OH8-7b's four-questions block (critic question 11 counts an edited scan constant).

## 9. Draft commit message

=== MESSAGE BEGIN ===
OH8-7h (t-424): the judgment census classifies the 21 subclass-only refusers of hooklib.py, controller.py, story_step.py, event_store.py, retro_numbers.py, host_adapter.py, role_load.py, release_fingerprint.py, selftest.py and config_view.py, and the temporary mechanism (SUBCLASS_UNIT_FILES, SUBCLASS_PENDING_CEILING, C7) is removed

Ten whole-file entries joined SUBCLASS_UNIT_FILES and SUBCLASS_PENDING_CEILING went 21 -> 0 with 21 rows (green); the same commit then removes SUBCLASS_UNIT_FILES, SUBCLASS_PENDING_CEILING, _c7, the unit_files / pending_ceiling keywords, the pending / pending_names totals and the C7 problem key, the two tests test_c7_the_subclass_pending_set_is_dense_and_only_shrinks and test_neg_pending_is_dense_and_only_shrinks_c7 (26 tests -> 24) and the pending branch of the flip loop. Every scanned file now creates units from its widened raise sites (a raise through a package subclass of ValueError / StateConflict, resolved per file, or the attribute form); totals["sites"] counts the widened sites; the totals line keeps subclass_family. The two constants die as specified in OH8-7b's four-questions block (spec t-346 1.3, 3.5); critic question 11 counted them as scan constants and its list is shortened in this commit.

21 rows: 17 shape, 3 xref, 1 safety. Safety by Lead rule 1: story_step.py::start (a dispatch id already committed with other fields is refused and the committed dispatch is not replaced; the same refusal in the existing row controller.py::apply is shape; critic to read the two together). Xref: role_load.py::_pick_dispatch, ::_require_role (joins with controller.json and inject-map.json), release_fingerprint.py::write_release (recipe files against the git index). Roles follow the existing rows of each file (rule 5): the four hooklib rows (read_config_file, story_of, story_root, story_root_at) take every role and the conductor like hooklib.artifact_root and artifacts_dir (the hook path), all other rows [conductor]. No E3 row: every refusal of the 21 leaves its module or becomes a CLI exit.
by Lead rule: story_step.py::start -> safety, [conductor], data (rule 1); role_load.py::_check_kind -> shape (rule 3, closed tokens); role_load.py::_task_root, hooklib.py::story_root, ::story_root_at, ::story_of -> shape (rule 2, read-only paths); config/presence rows (config_view.py::parse_path, hooklib.py::read_config_file, host_adapter.py::launch_id_keys, selftest.py::slow_tests, ::test_layers, role_load.py::settings) -> shape (rule 4).

The scanner blind spot (Lead decision 6b): a raise through a factory function that returns the family exception (raise _held_by(...)) is not seen; measured on 097f58d, 52 rowless functions carry such a raise (an upper bound), exploration.py::acquire among them. The u3 docstring line, the blind-spot paragraph, BLIND_SPOT and the fixture about say so in one clause and say that every WIDENED raise site creates a unit; no text claims that every refusal site does. test_blind_spot_states_the_subclass_clause asserts the token "factory function".

Raise list (AR-20), reconciled by script (delta per key == new rows naming it):
blocking_per_role.conductor: 659 -> 680 -- census classifies subclass refusers of hooklib.py, controller.py, story_step.py, event_store.py, retro_numbers.py, host_adapter.py, role_load.py, release_fingerprint.py, selftest.py, config_view.py (OH8-7h)
blocking_per_role.qa-automator: 169 -> 173; qa-bug-reporter: 135 -> 139; qa-case-critic: 160 -> 164; qa-case-designer: 135 -> 139; qa-code-critic: 135 -> 139; qa-doc-scribe: 135 -> 139; qa-failure-analyst: 136 -> 140; qa-requirements-tester: 153 -> 157; qa-retro-analyst: 135 -> 139; qa-runner: 136 -> 140; qa-scout: 135 -> 139; qa-test-strategist: 167 -> 171 -- census classifies the four hooklib refusers (read_config_file, story_of, story_root, story_root_at) on the hook path (OH8-7h)
safety: 81 -> 82 -- census classifies subclass refusers of story_step.py (OH8-7h): start
no other ratchet key and no existing row changed. No ceiling is lowered by the removal.

architecture: AR-29 -- every row is a judged class per unit (21 rows: 17 shape, 3 xref, 1 safety by Lead rule 1; no word-list / meaning-proxy / meaning reading); AR-20 -- the raised keys are named above with their reconciliation; AR-13 -- no second AST walk over refusals: units_of reads the widened sites refusal_registry.sites(raises=raise_family(...)) returns, refusal_registry.py untouched; AR-22 -- the producer (SUBCLASS_UNIT_FILES) and its one reader (units_of) die in one commit, together with the totals keys pending / pending_names and the C7 key (a grep of the names over ai-packages, tools, PROCESS, .github, SIBLING_MAP, the critic brief, CLAUDE.md and PROJECT.md: zero hits; positive control subclass_family); AR-28 -- the pending set (an unknown) is gone: every refusal site of the scan is a unit with a row, and the one form still unseen (the factory function) is named in the texts
judgment: adds data check test_judgment_census.units_of -- census rows for refusals through package subclasses in hooklib.py, controller.py, story_step.py, event_store.py, retro_numbers.py, host_adapter.py, role_load.py, release_fingerprint.py, selftest.py, config_view.py, each a data check or a guard classified per unit; units_of now creates a unit from every widened raise site
tier: <model>

Four questions (rule 10) for the REMOVAL of SUBCLASS_UNIT_FILES, SUBCLASS_PENDING_CEILING and C7:
(a) Cost and who pays: the census run gets no new walk (the widened site list was already computed; the literal-only scan is dropped, so one less call of refusal_registry.sites); a future author of a refusal through a package subclass now owes a census row (C1), like for a literal raise; the builder paid the 21 judgments, the critic pays one reading of the rows and of the removal, the Lead pays this commit and the answers to the three flagged readings.
(b) Axes (36 on docs/SIBLING_MAP.md):
axis 1 (policy <-> role): covered critic brief questions 9 and 11 lose both names; CLAUDE.md rule 10 and designer rule 1 name no constant.
axis 2 (per-tier exam instruments): n/a no exam.
axis 3 (factory package <->): n/a test files ship as usual; no release-side step changes.
axis 4 (factory rules <->): n/a no FR change; the temporary second road ends with this commit.
axis 5 (stage twins inside): n/a the census is not a stage.
axis 6 (measurement tools <->): n/a no measurer reads the census except source_split, which reads totals counts and blocking_per_role only (checked).
axis 7 (per-test identity <->): n/a no per-test identity changed
axis 8 (where the story): n/a no story path resolver touched
axis 9 (is this a): n/a SCAN_EXCLUDE unchanged.
axis 10 (git-top readers): n/a no git-top reader touched
axis 11 (shell-command recognizers): n/a no shell-command recognizer touched
axis 12 (carriers of the): covered the node is a row of batch onboarding-hooks/9 (the coordinator's move, D-0044); with it the batch holds no open node of the chain.
axis 13 (the dispatch text): n/a no dispatch text touched
axis 14 (readers of agent): n/a no transcript reader touched
axis 15 (console stream setup): n/a the test prints as before.
axis 16 (one json reader): n/a the test reads its fixture as before.
axis 17 (detector verdict shape): n/a the census is a test, not a detector producer.
axis 18 (in-tree shrink-only ratchets): covered the member text drops the two constants and names OH8-7h; every raise named row by row; no ceiling lowered or removed other than the two constants of this chain.
axis 19 (one reader of): n/a no role tools line reader touched
axis 20 (host receipt names): n/a no host receipt name touched
axis 21 (readers of the): n/a no markdown table reader touched
axis 22 (a host's return): n/a no host report form touched
axis 23 (fields of a): n/a no tests[] row field touched
axis 24 (the record of): n/a no execution record join touched
axis 25 (freshness of a): n/a no freshness predicate touched
axis 26 (the word stand): n/a no stand-not-confirmed word touched
axis 27 (the profile of): n/a no profile of a test row touched
axis 28 (the render site): n/a no row form render site touched
axis 29 (append-only jsonl writers): n/a no jsonl appender touched
axis 30 (the commands of): n/a no profile commands reader touched
axis 31 (role carriers): n/a no role carrier touched
axis 32 (where judgment lives): covered census rows in the same commit as the units (C1); one scanner (sites()); rows read by critic question 11.
axis 33 (which dispatch am): n/a no dispatch identity reader touched
axis 34 (one road for): covered the temporary second road is closed by this commit and its line is removed from the row; the factory-function form remains an unseen road, named in the texts, with its own node after the chain.
axis 35 (sides of a): n/a no story sides reader touched
axis 36 (the row written): n/a no placeholder row predicate touched
(c) Detector: test_judgment_census.py -- C1 (a created unit with no row, a row whose unit vanished: now for every widened site), C3 (raises); calibration checks 41 (judgment census) and 35 (b) (every raise named) in PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md; the removed C7 had no other reader (grep above).
(d) What stops a skip: code on the path. The census test is a `keep` row (layer register) printed by scenario_walk.py --witness-for for the fixture and runs in the CI canon. A new refusal through a package subclass in ANY scanned file without a row now gets C1 "... is a check unit (u3) with no row"; no list to forget to extend. The MEANING of each class is judged by a tier above (critic question 11), not by code.

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
=== MESSAGE END ===

(The Lead replaces `tier: <model>` and the Co-Authored-By line as the commit requires; the message is written for a Lead commit, not a builder commit.)

## 10. Analogs noticed, not fixed

- controller.py::apply (existing row, shape) and story_step.py::start (new row, safety) refuse the same IdempotencyKeyReused case: P31 one road; belongs to the 6b "class node after the chain" for written-path guards and trust.
- event_store.py::_run_after_commit and controller.py::refresh_derived are twins (both wrap a failed after-commit step into DerivedViewStale with a "do not repeat" text); the two bodies also each carry a different text for the same fact.
- role_load.py::_task_root swallows (OSError, ValueError, AttributeError) from artifact_root and falls back to `<project>/qa-factory/artifacts` ("a broken config: today's folder"), while hooklib.artifact_root states that a broken config raises and never becomes {} (FR-59 class: an unknown read as a default).
- hooklib.py::story_root and ::story_root_at raise through a factory (`raise _no_story(...)`, hooklib.py:~434, 487): the very form the scanner does not see; story_root's other raises were enough to make the function a unit, so its row exists, but the `_no_story` sites are an example of the 52-function upper bound.
- selftest.py::slow_tests and ::test_layers read their data file with the same three-step pattern (FileNotFound / OSError+ValueError / form problem) in two copies.
- hooklib.py::story_of and ::story_root_at carry long door texts built three ways (tail / door / `_example_folder`); a text duplication, not touched.

## 11. FR walk by section (package change: only the census test and fixture, no script)

A refusals and doors -- no refusal text changed. B text shown to a person -- not touched. C contracts -- FR-14: `units_of`'s return shape lost `pending` and `list_problems` together with their only reader (`analyse`); `analyse` keeps its two positional parameters (source_split.py reads it). D identity -- n/a. E delivery -- n/a. F measurement -- FR-28 (the measurer keeps its test: SUBCLASS_ROWS and the synthetic tables), FR-41 (the unknown "pending" is gone, the one still unseen form is named in the texts). G code -- FR-30: `selftest.py --lang` passed (the fixture `about` and the test are package text, no Cyrillic: `--limits --lang` 4/4); FR-32 green; FR-54 siblings by the map (axes in the message).

## 12. Needed beyond the manifest (telemetry)

tools/architecture_gate.py (the judgment form), tools/source_split.py and tools/source-split-carriers.json (reader check), tools/test_mechanism_gate.py (the map test), hooks/hooks.json and scripts/validate_artifacts.py, exit_gate.py (hook path roles of the hooklib rows), the 21 script files, scripts/event_store.py / controller.py (the IdempotencyKeyReused twin), docs/CLAUDE.md-level texts only as quoted in the dispatch.
