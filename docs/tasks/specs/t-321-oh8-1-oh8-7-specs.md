# t-321 — two builder specs for batch onboarding-hooks/8: A = OH8-1 (is_one_component copies outside OH6-1), B = OH8-7 (the judgment census counts subclasses of refusal exceptions)

Status: designer draft. Forks are returned at the end and none is decided. Lead acceptance comes before any dispatch.
Every line number below was read on 13.11.2026 in `C:\QAFactory\forge-repo\.claude\worktrees\read-main` (origin/main 303e89e, detached).
The root checkout's `ai-packages/` was not read.
The designer has no shell, so NOTHING in this draft was executed. Every count marked "estimate" comes from reading or grepping.
§B.2 gives the one command that turns the census premise into a measurement. PROJECT.md "package change" item 6(a) requires that measurement BEFORE the builder starts.

---

# A. OH8-1 — the three remaining copies of "a name is one path component" call `hooklib.is_one_component`

## A.0 Dispatch header (R11-f)

given: this spec, section A (marked, one hop: it carries the enumeration); `ai-packages/qa-factory/design/factory-rules.md` (whole; PROJECT.md "package change" p. 1); `plans/builder-rules.md` (whole); `ai-packages/qa-factory/design/architecture.md` AR-4, AR-13, AR-15, AR-20, AR-28, AR-29; `docs/TESTING.md`; `docs/SIBLING_MAP.md` axes 8, 18, 34; `plans/piles/onboarding-hooks/batch-8-ostatki-t-282-t-254-t-287.md` row OH8-1; `plans/piles/onboarding-hooks/findings/20261113-is-one-component-kopii-vne-oh6-1.md`; `docs/tasks/specs/t-282-oh6-1-one-component.md` §2.4, §5 (the table and the sentinel this node extends); the owned files below as they are on origin/main; `scripts/hooklib.py` :269-272 (`is_one_component`, read only); `scripts/tests/harness.py`; `scripts/tests/test_event_store.py` :849-855 (the existing stale-marker test, read only); `references/project-dependencies.json` and `scripts/slow_tests.json` (real data that must still pass)
owns:
C:\QAFactory\forge-repo\.claude\worktrees\oh8-1\ai-packages\qa-factory\scripts\event_store.py
C:\QAFactory\forge-repo\.claude\worktrees\oh8-1\ai-packages\qa-factory\scripts\selftest.py
C:\QAFactory\forge-repo\.claude\worktrees\oh8-1\ai-packages\qa-factory\scripts\dependency_drift.py
C:\QAFactory\forge-repo\.claude\worktrees\oh8-1\ai-packages\qa-factory\scripts\tests\test_resolver.py
C:\QAFactory\forge-repo\.claude\worktrees\oh8-1\ai-packages\qa-factory\scripts\tests\test-layers.json
(The worktree `oh8-1` is NEW: it does not exist at spec time. The dispatch creates it from pushed origin/main, after a push (`tools/dispatch_gate.py`). Every path above refers to that tree.)
non-goals:
- no change to `hooklib.is_one_component` (the batch brief: "do not widen `is_one_component` beyond one component"). No NTFS aliases (OH8-2) and no length ceiling (OH6-2);
- no change to any site's answer except for the inputs of §A.4, and no refusal text changes (byte for byte);
- no edit of `test_event_store.py`, `test_selftest_slow_tests.py` or `test_dependency_drift.py`. The last one is QUARANTINED (`test-layers.json` :7798, under `quarantine` which starts at :7013), so the builder does not run it, fix it or edit it (builder-rules 7b);
- in `test-layers.json`, ONLY the `covers` list of the `test_resolver.py` keep row (:4320-4359) changes;
- no new sentinel pattern (the basename form stays a stated blind spot, §A.5);
- no new test file; no SIBLING_MAP edit.
handoff: a builder report per `.claude/agents/builder.md` rule 7, containing: the commit hash on branch `wip/oh8-1`; the verbatim witness output; the FR walk by section; the §A.2 table with the new line numbers; the mutation witness (hash comparison). If the commit-msg gate asks for `tier:`, the tree stays STAGED and the report says so (builder-rules 18).
edges: §A.3 (the positional invariant per site) and §A.4 (the edge table, per OS).
DoD: §A.6. The verification run is `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <the five owns paths>`, plus every file it prints, under the scope rule of §A.6 item 5.
siblings: axis 8 (the key -> folder rule; survivor `hooklib.is_one_component`); axis 18 (the sentinel allowance is shrink-only; this node shrinks it to `{}`); axis 34 (one road: after this node, no site checks "one component" by another road). Analogs NOT in scope: OH8-2 (NTFS aliases pass the survivor), OH6-2 (no length ceiling), OH8-3 (the quiet skip in `cost_capture`), and `reporters.py` (basename form, not a copy per t-282 §5 Part B; not re-read here).
designer: this draft (t-321 §A), after Lead acceptance.

Order (batch-8 l.10-19): `event_store.py` comes after OH6-3. OH6-3 is in origin/main: `TEMP_NAME_HEX = 8` at `event_store.py:120`, and `_publish` at :180 has a census row (`judgment-census.json` l.267). `selftest.py` has the line `очередь: onboarding-forge/2 → onboarding-hooks/8` (batch-8 l.14), and the D-0048 function list is in §A.7. `onboarding-forge/2` is "в работе", and its nodes SC2-23 and SC2-26 write `selftest.py`. Whichever lands later merges `main` and resolves the conflict.

## A.1 Invariants, owners, census classes

| AR | how the node touches it | change check written into the DoD |
|---|---|---|
| AR-15 (one survivor, wired everywhere) | the last three hand copies become calls of `hooklib.is_one_component` | DoD 1: grep for the problem, not the helper (`Path\(\w+\)\.name`, `basename\(`, `in \(".", "\.\."\)` over the owned scripts); the spy column of the table proves each call |
| AR-13 (a fact with a reader is read only through it) | "is this one path component" has one reader | DoD 2: the sentinel is green with `OH61_ALLOWED = {}` |
| AR-20 (shrink-only ratchets) | the sentinel allowance shrinks `{"event_store.py": 1, "selftest.py": 1}` -> `{}` | DoD 2: the shrink is named in the commit (key, old -> new, reason). No raise |
| AR-4 (no tie to one machine) | `a\b` and `a:b` are refused on POSIX too. Today they pass on POSIX and are refused on Windows at all three sites | DoD 3: the `backslash` and `colon` columns |
| AR-28 (an unknown never becomes a pass) | NUL used to pass all three copies. Now each site refuses it in its own direction | DoD 3: the `nul` column |
| AR-29 (a code check judges data) | every altered check is a SHAPE check of a name | DoD 6: `test_judgment_census.py` is green, with no row added or removed and no count changed |

Owner and census class of every check the node alters (AR-29, P27):

| check | owner | class | census row |
|---|---|---|---|
| `event_store.EventStore.__init__` (`stale_marker`) | data (code) | shape | `event_store.py::__init__` shape / conductor / data (`judgment-census.json` l.265). Unchanged: the `raise ValueError` stays in `__init__` |
| `selftest._slow_tests_problem` (`files` keys) | data (code) | shape | none. It is not a unit: `UNIT_NAME_RE` (`test_judgment_census.py:61`) needs `_problems$`, and the name ends in `_problem`. It returns a string and has no raise site |
| `dependency_drift.load_table` (`locks[].file`) | data (code) | shape | none. No unit name and no raise site (rows l.238-239 are `check` and `check_profiles`) |
| the OH6-1 sentinel allowance (`test_resolver.py`) | data (code detector) | shape. It is a test, outside the census (`scripts/tests/` is not scanned) | — |

FR sections: A: no refusal text changes. B: no text shown to a person. C: FR-14, no output shape changes. D: FR-17 (the tool is wired wherever the problem occurs). E and F: not touched. G: FR-32, FR-54. Principles: P31, P12.

## A.2 The sites (current line, current behaviour, new behaviour, error direction)

| # | site | current line (verified) | current behaviour | new line | error direction (unchanged) |
|---|---|---|---|---|---|
| 1 | `event_store.EventStore.__init__` | :494 (the finding says :482; the lines drifted) `if not isinstance(marker, str) or not marker or marker != Path(marker).name or marker in (".", ".."):` then `raise ValueError("stale_marker must be a plain file name under state/ (default %r), got %r" % (STALE_MARKER, marker))` :495-496 | refuses non-str, `""`, `.`, `..` and `a/b` everywhere. Refuses `a\b` and `a:b` on Windows only (`PureWindowsPath('a:b').name == 'b'`). Accepts NUL, which then fails later at the `unlink` / `atomic_json` of the marker (`ValueError: embedded null byte`, at commit time, by reading) | `if not hooklib.is_one_component(marker):` with the same raise, text byte for byte. The import follows F-A1 (recommended: `import hooklib` as a local import at the top of `__init__`, like `_require_root` :521) | `ValueError` |
| 2 | `selftest._slow_tests_problem` | def :964; the check :982 `if not name or name != Path(name).name:` returns `f'"files" key {name!r} is not a test file name'` :983 | `..` passes; `.` is refused (`Path('.').name == ''`); `a/b` is refused; `a\b` and `a:b` are refused on Windows and pass on POSIX; NUL passes | `if not hooklib.is_one_component(name):` with the same return string. Local `import hooklib` at the top of the function (C-A2) | an error string (the caller `slow_tests` :1018 turns it into `SlowTestsError`) |
| 3 | `dependency_drift.load_table` | def :78; the check :92 `if not ok or os.path.basename(row["file"]) != row["file"]:` returns `(None, f"{target.name} locks[{index}] needs a plain file name, a `format` and a `manager`")` :93 | `..` AND `.` pass (`basename('.') == '.'`); `a/b` is refused; `a\b` and `a:b` are refused on Windows (ntpath) and pass on POSIX; NUL passes | `if not ok or not hooklib.is_one_component(row["file"]):` with the same return. `import hooklib` already exists at :60. `os` stays imported (16 other `os.` uses) | `(None, problem)`. Callers say `unknown` / `none` |
| S | the OH6-1 sentinel (`test_resolver.py`) | :1680-1682 `OH61_ALLOWED = {"event_store.py": 1, "selftest.py": 1}` with comments; :1704 checks that literal; docstring :1690-1693 | allows the two PATH_NAME hits | `OH61_ALLOWED = {}`, comment "shrink-only (AR-20); emptied by OH8-1". :1704 becomes `check("OH6-1 sentinel: the allowance is empty", OH61_ALLOWED == {})`. The docstring keeps the basename blind spot, and now names the Part A spy rows `dependency_drift` (and the other two) as its detector instead of "the named node" | — |

`dependency_drift.py` is outside the sentinel patterns: the basename form is a stated blind spot. After this node its only detector is the spy cell `OH6-1 dependency_drift-<label> asked the survivor`.

## A.3 The POSITIONAL invariant at each site

| site | where the call stands | what must stay refused or unreachable |
|---|---|---|
| `EventStore.__init__` | the first statement, before ANY attribute is set (`self.stale_marker`, `self.root`, ...) and before any file-system call | a refused marker leaves no half-built store and touches no file. `None` and `5` stay `ValueError` (the survivor answers False for a non-str), so `test_event_store.py:849-855` stays green unedited |
| `_slow_tests_problem` | the same place in the `files` loop, BEFORE the seconds check of the same key | the first bad key still returns first, and the order of the earlier checks (`thresholds`, `max_drift`, `measured_on`/`source`, `files` type) does not change |
| `load_table` | `not ok or ...` keeps `ok` FIRST, so the survivor is only reached with a non-empty str (it would answer False anyway) | a row the reader cannot trust still makes the WHOLE file unusable (`(None, why)`, never a partial table). A lock name is never joined to the project folder unless it is one component |

## A.4 Edge table (after; "before" given where it differs; "W" = Windows, "P" = POSIX; by reading, not run)

| input | 1 `__init__` | 2 `_slow_tests_problem` | 3 `load_table` | invariant protected |
|---|---|---|---|---|
| `..` | ValueError (unchanged) | error string (NEW; before: passed) | `(None, problem)` (NEW; before: passed) | no name climbs to the parent of `state/`, of `scripts/tests/` or of the lock folder |
| `.` | ValueError (unchanged) | error string (unchanged) | `(None, problem)` (NEW; before: passed) | a name never names the folder itself |
| `a/b` | ValueError (unchanged) | error string (unchanged) | `(None, problem)` (unchanged) | one component |
| `a\b` | ValueError (NEW on P) | error string (NEW on P) | `(None, problem)` (NEW on P) | one component on every OS (AR-4) |
| `a:b` | ValueError (NEW on P) | error string (NEW on P) | `(None, problem)` (NEW on P) | the same; on W, `C:x` is drive-relative and escapes the folder |
| NUL `a\0b` | ValueError at construction (NEW; before: accepted, then failed at the first marker write or unlink) | error string (NEW) | `(None, problem)` (NEW) | a name with NUL never reaches an OS call |
| `""` | ValueError (unchanged) | error string (unchanged) | `(None, problem)` via `ok` (unchanged) | an empty name never names the parent folder |
| non-str | ValueError (unchanged) | unreachable: the only caller passes `json.loads` output, whose keys are always str | `(None, problem)` via `ok` (unchanged) | refused in the site's direction, never a TypeError |
| `T.`, `T ` (NTFS aliases), very long | accepted (unchanged) | accepted (unchanged) | accepted (unchanged) | out of scope: OH8-2, OH6-2 |
| good `T` | accepted; `store.stale_marker == "T"` | `None` (no problem) | the table, with `locks[0]["file"] == "T"` and problem `""` | real data still passes: `projection-stale.json`, `manifest-projection-stale.json` (`manifest_put.py:133`), `poetry.lock` / `uv.lock` / `pdm.lock` (`project-dependencies.json` l.4-6) |

Conflicting requirements: "keep each site's direction" and "`..`, NUL, `a\b`, `a:b` are refused" do not conflict. Each new refusal joins the site's existing refusal set, in its existing form.

Limits or truncation introduced: none.

TEMPORAL: nothing comes into existence.

The reused function in a more consequential role: `is_one_component` takes over the gate role at three more sites. It may err only toward REFUSING; it must never accept a name with `/`, `\`, `:`, NUL, or one that is `.`, `..` or empty. Adversarial inputs that must stay refused are the six bad names of the table. The over-refusal it may commit is that NTFS aliases still pass (OH8-2), which is not over-refusal but a known accept.

## A.5 Test (`test_resolver.py`: a keep row, layer `table`, l.4320; not quarantined)

Extend the existing OH6-1 table. Do NOT add a new table: the three sites become three variant rows of `OH61_ROWS` (:1620-1650). Names come from `OH61_NAMES` (:1435-1436): `dotdot`, `dot`, `slash`, `backslash`, `colon`, `nul`, `good`. Ids follow `OH6-1 <id>-<label>`.

| id | how the name reaches the check | refused (6 bad names) | good name `T` | spied |
|---|---|---|---|---|
| `event_store` | `event_store.EventStore(where, stale_marker=name)` | `o[:2] == ("raised", "ValueError")` and `o[2].startswith("stale_marker must be a plain file name")` | `o[0] == "value"` and `o[1].stale_marker == "T"` | True |
| `selftest_slow_tests` | `selftest._slow_tests_problem({"thresholds": {"slow_over_s": 1, "fast_under_s": 0}, "files": {name: None}})` | `o == ("value", f'"files" key {name!r} is not a test file name')` | `o == ("value", None)` | True |
| `dependency_drift` | write `where/t.json` = `{"locks": [{"file": name, "format": "toml_packages", "manager": "poetry"}], "install_commands": {"poetry": ["poetry", "install"]}}` (via `json.dumps`, so NUL is written as an escape), then call `dependency_drift.load_table(where / "t.json")` | `o == ("value", (None, "t.json locks[0] needs a plain file name, a `format` and a `manager`"))` | `o[0] == "value"` and `o[1][0]["locks"][0]["file"] == "T"` and `o[1][1] == ""` | True |

The spy column holds for all three rows. Each site must call `hooklib.is_one_component` through the MODULE ATTRIBUTE: `import hooklib` and then `hooklib.is_one_component(...)`, never `from hooklib import is_one_component`. A bound name would escape the spy that `oh6_1_one_component_table` installs on `hooklib` (:1659-1666). That cell is what proves the copy is gone.

Reachability: all three checks run before any file-system effect of the name, so the spy carries the proof. `_oh61_plant` is not needed.

Counts after the node: 18 rows × 7 names = 126 cells, plus 17 spied rows × 7 = 119 spy cells. Update the docstring of `oh6_1_one_component_table` (:1654, "15 callers x 7 names") to match.

Sentinel (Part B): `OH61_ALLOWED = {}` and the :1704 check as in §A.2 row S. The positive, negative and differential controls (:1711-1721) stay unchanged.

The stated mutation (DoD 4): put `os.path.basename(row["file"]) != row["file"]` back into `dependency_drift.load_table`. Then `OH6-1 dependency_drift-dotdot` and `OH6-1 dependency_drift-dotdot asked the survivor` must turn red. A second mutation is optional: put back `name != Path(name).name` in selftest. That turns `selftest_slow_tests-dotdot` red, and the sentinel's "no script outside the allowance" check too.

`test-layers.json`: add `event_store.py`, `selftest.py` and `dependency_drift.py` to the `covers` of the `test_resolver.py` row (the t-282 F-2 (a) precedent; C-A3). Nothing else changes.

## A.6 DoD (inline)

1. All three sites of §A.2 call `hooklib.is_one_component` through the module attribute. Each keeps its direction and its text byte for byte. A grep of `Path\(\w+\)\.name|basename\(row` over the three owned scripts finds nothing. Positive control: the same grep finds `reporters.py` or the sentinel fixture string.
2. The sentinel is green with `OH61_ALLOWED = {}`, and all its controls pass.
3. The table is green: 126 cells plus 119 spy cells, ids as in §A.5.
4. The mutation of §A.5 is run once by hand. Take a byte copy before, restore from it, and use a hash comparison as the witness (command hygiene pt. 7). Quote the red ids.
5. Witness (builder-rules 7b): `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for C:\QAFactory\forge-repo\.claude\worktrees\oh8-1\ai-packages\qa-factory\scripts\event_store.py C:\QAFactory\forge-repo\.claude\worktrees\oh8-1\ai-packages\qa-factory\scripts\selftest.py C:\QAFactory\forge-repo\.claude\worktrees\oh8-1\ai-packages\qa-factory\scripts\dependency_drift.py C:\QAFactory\forge-repo\.claude\worktrees\oh8-1\ai-packages\qa-factory\scripts\tests\test_resolver.py C:\QAFactory\forge-repo\.claude\worktrees\oh8-1\ai-packages\qa-factory\scripts\tests\test-layers.json`
   - Run every file it prints with `python -B scripts/tests/<file>.py` and paste the output verbatim.
   - `event_store.py` is in the `covers` of about 50 keep rows (estimate by grep of `test-layers.json`), so the printed set is large. The slow files of PROJECT.md "package change" p. 2 (`SLOW_TESTS`, `test_story_run_*`, `test_controller_*`, `test_fixes_13797`) are NOT run locally: they are named in the report and CI judges them (the t-282 F-5 (a) precedent).
   - A quarantined file is never run, `test_dependency_drift.py` included.
   - A line "no scenario or keep row covers" is a report line.
   - This spec did not run the command, so the predicted set is an estimate.
6. The AR-29 change check: `python -B ai-packages/qa-factory/scripts/tests/test_judgment_census.py` is green, with no row added or removed and no count changed. Its totals line is pasted.
7. `python -B ai-packages/qa-factory/scripts/selftest.py --lang` (FR-30) passes on the owned files.
8. The commit message carries:
   - `architecture: AR-15, AR-13, AR-20, AR-4, AR-28, AR-29 -- <how kept>`;
   - `judgment: none -- three shape checks of a name now call the survivor; no unit, row or count changes`;
   - the sentinel allowance shrink, named (`OH61_ALLOWED event_store.py 1 -> 0, selftest.py 1 -> 0`, AR-20);
   - the four questions and the axis block (the sentinel is a machine check, rule 10);
   - the function lists of §A.7.

## A.7 Hot files and the D-0048 function lists

| file | hot | functions touched | outside a function |
|---|---|---|---|
| `event_store.py` | yes (core; batch-8 l.10) | `EventStore.__init__`; under F-A1 (a) also the docstring of `EventStore._require_root` (:510-515: "the store stays a leaf of the standard library while nothing is refused" stops being true) | none (local import) |
| `selftest.py` | yes (zone of `onboarding-forge/2`, queue line batch-8 l.14) | `_slow_tests_problem` only | none (local import) |
| `dependency_drift.py` | no | `load_table` | none (`import hooklib` exists at :60) |
| `tests/test_resolver.py` | no | three new row functions `_oh61_row_event_store`, `_oh61_row_selftest_slow_tests`, `_oh61_row_dependency_drift`; `oh6_1_one_component_table` (docstring count); `oh6_1_sentinel` (:1704 check, docstring) | `OH61_ROWS` (+3 rows), `OH61_ALLOWED` and its comment |
| `tests/test-layers.json` | no | — | the `covers` of the `test_resolver.py` row |

---

# B. OH8-7 — the judgment census counts subclasses of refusal exceptions, with one named ratchet raise

## B.0 Dispatch header (R11-f)

given: this spec, section B (marked, one hop); `ai-packages/qa-factory/design/factory-rules.md` (whole); `plans/builder-rules.md` (whole); `ai-packages/qa-factory/design/architecture.md` AR-13, AR-20, AR-22, AR-28, AR-29; `docs/TESTING.md`; `docs/SIBLING_MAP.md` axes 18, 32, 34; `docs/tasks/critic-diff-brief.md` questions 9 and 11; batch-8 row OH8-7; `plans/piles/onboarding-hooks/findings/20261113-oh7-2-f2-2-rasshirenie-perepisi-na-podklassy-isklyuchenij-otkaza.md`; `scripts/tests/test_judgment_census.py`; `scripts/tests/fixtures/judgment-census.json`; `scripts/refusal_registry.py` :56-59 and :1046-1101 (`REFUSAL_RAISES`, `_refusal_calls`, `sites`); `tools/architecture_gate.py` docstring item 7 and `census_state` (:268-284) (read only: which `judgment:` form a raise needs); the Lead's §B.2 measurement output (pasted into this spec before the dispatch)
owns (under the recommended F-B2 (a); the Lead's F-B2 choice may remove the third line):
C:\QAFactory\forge-repo\.claude\worktrees\oh8-7\ai-packages\qa-factory\scripts\tests\test_judgment_census.py
C:\QAFactory\forge-repo\.claude\worktrees\oh8-7\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json
C:\QAFactory\forge-repo\.claude\worktrees\oh8-7\ai-packages\qa-factory\scripts\refusal_registry.py
(The worktree `oh8-7` is NEW: it does not exist at spec time. The dispatch creates it after a push.)
non-goals:
- the A24 audit (`refusal_registry.findings`, `--check`) does NOT widen: `sites()` without the new argument scans exactly as today;
- no change of any refusal in any script; no class lowered or raised on an EXISTING row;
- no edit of `tools/architecture_gate.py` (F-B4);
- no change to `MEANING_CEILING` (`test_judgment_census.py:88`): a new `meaning` row stops the node (§B.4 edge E7);
- no new test file.
handoff: a builder report (rule 7), containing: the commit hash on `wip/oh8-7`; the verbatim witness; the FR walk; the before/after totals lines; the list of every raised ceiling (key, old -> new, reason); the list of new rows with their class and a one-clause reason each (under F-B1 (a)); the mutation witness. If the gate asks for `tier:`, the tree stays STAGED.
edges: §B.4.
DoD: §B.6. The verification run is `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <the owns paths>`, plus every file it prints.
siblings: axis 32 (the census, the one scanner `sites()`, the gate, question 11); axis 18 (the census `ratchet` is a member; the raise is named row by row); axis 34 (one road: today a literal `raise ValueError(...)` makes a unit and a subclass raise does not, so the same action takes two roads). Analog: OH8-6 writes the `refusal_registry.py` module docstring (`SCOPE`). Under F-B2 (a) the D-0048 lists are disjoint (§B.7), or a queue line is used.
designer: this draft (t-321 §B), after Lead acceptance AND after the §B.2 measurement is pasted.

Order: batch-8 l.38 says OH8-7 depends on OH7-2. OH7-2 is in origin/main: `SCANNED` holds `codex_roles.py` and `host_adapter.py` (`refusal_registry.py:56-57`).

## B.1 Invariants, owners, census classes

| AR | how the node touches it | change check written into the DoD |
|---|---|---|
| AR-29 | the census, the AR-29 detector, sees refusals raised through package subclasses of `ValueError` / `StateConflict` | DoD 5: run `test_judgment_census.py`. Every raised count is named |
| AR-20 | one named raise of the ceilings the widening moves (at least `blocking_per_role.*`) | DoD 6: list every raised key (key, old -> new, reason) in the commit and in the critic verdict |
| AR-13 / axis 32 ("no second AST walk over refusals") | the widening goes THROUGH `refusal_registry.sites()` (F-B2 (a)); the census never matches raises itself | DoD 3: `test_c6_totals_line`'s assert on `refusal_registry` stays; grep the census for `ast.Raise`: no hit |
| AR-22 (producer and reader in one commit) | the new `sites()` argument (producer) and the census call (reader) change in one commit | DoD 3 |
| AR-28 | a refusal through a subclass was an unknown that counted as "no unit". After the node it is counted. The misses that remain are NAMED in `BLIND_SPOT` | DoD 4 |

Owner and census class of every check the node adds or alters:

| check | owner | class | census row |
|---|---|---|---|
| the family closure, and `sites(..., raises=...)` in `refusal_registry.py` | data (code) | shape (a name join over class definitions) | none: neither `sites` nor the new helper is a unit (no unit name, no raise site, no judge call). The helper must not be named `check_*`, `*_problems` and so on, or it becomes a unit (C-B4) |
| C1-C5 of the census, now over the widened unit set | data (code detector) | shape. It is a test, outside the census | — |
| each NEW census row's `class`, `roles` and `owner` | judgment (the builder judges; the critic accepts as the tier above, question 11) | the class the builder judges per unit, never defaulted (`test_judgment_census.py:293-294`) | the new rows themselves (F-B1) |
| the ratchet raise | intent of the Lead (named raise, AR-20), read by the critic (question 9) | — | `ratchet` object |

FR sections: C: FR-14 (`sites()` return shape unchanged). F: FR-28 (a measurer gets a test), FR-41 (an unknown is not a fact). G: FR-32. A, B, D and E: not touched.

## B.2 MEASURE FIRST (PROJECT.md "package change" item 6 (a))

### How units are found today (read, `test_judgment_census.py`)

- `scan_files` (:97-106) takes every `scripts/**/*.py` except `scripts/tests/`.
- `units_of` (:202-266) finds:
  - u1: a name matching `UNIT_NAME_RE` (:61);
  - u2: a call of `judge.*` / `judge_form.*` (:139-148);
  - u3: a refusal site from `refusal_registry.sites(plugin_root, files=...)` (:212, :234-235);
  - a `stages.json` detector script with no function unit (`<script>`);
  - a `refusal_registry.REGISTRY` entry.
- Units are keyed by (file, function).
- `blocks` is True when the file is on the blocking path, or when a site lies in the unit's span (:259-264).
- `sites()` -> `_refusal_calls` (`refusal_registry.py:1065-1074`) matches only `deny(...)` / `block(...)` calls and `raise X(...)` where `X` is a bare NAME in `REFUSAL_RAISES = ("StateConflict", "ValueError")` (:59). A subclass raised by its own name is invisible. So is `raise mod.StateConflict(...)` (an attribute, not a Name).

### What the finding's numbers mean (read, and a correction)

- `_c3` (:337-354) counts `blocking_per_role` ONLY over census ROWS that exist (`for key, row in rows.items()`). A new unit with no row adds a C1 problem and NOTHING to the counts.
- So the finding's "conductor 474 -> 496" (+22) is existing rows flipping to blocking. It is NOT the count after the ~157 new units get rows.
- Once those rows exist, every new u3 unit blocks (its site is in its own span). Each row then adds 1 to every role it names.
- Expected (estimate): conductor rises by +22 plus the number of new rows that name `conductor`, and the other roles rise as well. The batch row's "raises from 489 to ~496" understates the raise.
- Also, origin/main's ceiling is `"conductor": 476` (`judgment-census.json` l.4), not 489 and not 474. The batch row and the finding are stale. The rows today: 951 lines with `"file":` (finding: 949 units).

### New units on main today: NOT measured by the designer (no shell)

Estimate:
- about 157 new units (1106 - 949 on the older tree), unverified. Main has 951 rows, close to 949;
- about 47 direct package subclasses of `ValueError` / `StateConflict` outside `scripts/tests/` (a grep of `class \w+\((ValueError|StateConflict|...)\)`: 51 hits in 41 files, 4 of them under `tests/`), plus transitive ones (for example `DetectorsUnreadable(DetectorsError)`, `ProjectionStale(EventCommitted)`).

The measurement (a pure read, command hygiene pt. 4b). The LEAD runs it before the dispatch and pastes the output into this section. It is never committed. Save it under the scratchpad and run it with `python -B <abs path> <plugin root>`:

```python
import ast, sys
from pathlib import Path
root = Path(sys.argv[1])                       # ...\ai-packages\qa-factory of a clean origin/main tree
sys.path[:0] = [str(root / "scripts" / "tests"), str(root / "scripts")]
import test_judgment_census as T, refusal_registry as R
files = T.scan_files(root)
bases, defined = {}, {}
for f in files:
    tree = ast.parse((root / "scripts" / f).read_text(encoding="utf-8", errors="replace"))
    for n in ast.walk(tree):
        if isinstance(n, ast.ClassDef):
            names = {b.id if isinstance(b, ast.Name) else b.attr for b in n.bases if isinstance(b, (ast.Name, ast.Attribute))}
            bases.setdefault(n.name, set()).update(names); defined.setdefault(n.name, set()).add(f)
family, grew = set(R.REFUSAL_RAISES), True
while grew:
    grew = False
    for c, bs in bases.items():
        if c not in family and bs & family:
            family.add(c); grew = True
before = T.analyse(root, T.load_census())
R.REFUSAL_RAISES = tuple(sorted(family))       # _refusal_calls reads the module global at call time
after = T.analyse(root, T.load_census())
norow = [p for p in after["problems"]["C1"] if "with no row" in p]
print("family size (beyond the 2 literals):", len(family) - 2)
print("units before/after:", before["totals"]["units"], after["totals"]["units"])
print("new units needing a row:", len(norow))
print("blocking_per_role before:", before["totals"]["blocking_per_role"])
print("blocking_per_role after (existing rows only):", after["totals"]["blocking_per_role"])
print("C3 after:", *after["problems"]["C3"], sep="\n  ")
print("name collisions (a family name also defined with no family base):",
      sorted(c for c in family - set(R.REFUSAL_RAISES) if len(defined.get(c, ())) > 1))
print("new units by file:", sorted({p.split("::")[0] for p in norow}))
```

It also measures the F-B3 count: rerun with `_refusal_calls` accepting `ast.Attribute` whose `.attr` is in the family, and print the difference. Without that rerun, F-B3's cost stays an estimate: 8 attribute-form raises of `X.<Name>Error` / `X.StateConflict` in non-test scripts (grep), not all of them in the family.

### Does every new unit need its own row with a class? YES, on today's rules

- C1 (`_c1`, :290-294) refuses a unit with no row, with the text "the class is a judgment about what the unit decides, never defaulted".
- C2 (:316-326) refuses a class outside `CLASSES`, an owner outside `OWNERS` and an empty `roles`.
- So on today's rules about 157 rows each need a judged `class`, a judged `roles` list and an `owner`. That is the load-bearing fork F-B1.

### Where the "blind spot" text is (verified)

- `test_judgment_census.py` module docstring :32-37 (the sentence from "A subclass of `ValueError`" on) and the u3 line :22 (`raise StateConflict|ValueError`);
- `BLIND_SPOT` constant :449-453 (the clause "a subclass of `ValueError` or `StateConflict` raised by its own name is invisible ...");
- `judgment-census.json` `about` l.3 (the sentence "Blind spot: a subclass ...");
- the check `blind_spot_names_subclass_gap` :721-723, which ASSERTS that "subclass" is in both `BLIND_SPOT` and `about`. It must be rewritten in the same commit, or it turns red. It has no `test_` prefix, so pytest does not collect it; only script mode runs it (the `TESTS` list :726-738). An analog is reported in §Analogs.

A grep of `subclass of .?ValueError|invisible to .?refusal_registry` (case-insensitive) over the tree finds only these two package files. The other hits are historical specs (`t-263`, `t-2222`, the `t-300` review), which are not edited.

## B.3 The change (under the recommended F-B2 (a); the shape of the rows follows F-B1)

1. `refusal_registry.py`:
   - a helper (C-B4: the name must not match `UNIT_NAME_RE`, for example `raise_family(plugin_root, files)`) returns `REFUSAL_RAISES` plus every class name defined in `files` whose base, read as `Name.id` or `Attribute.attr`, is in the family, closed transitively;
   - `sites(plugin_root=None, files=None, raises=None)`: with `raises=None` it behaves exactly as today. `_refusal_calls(tree, raises=REFUSAL_RAISES)` takes the set as an argument;
   - the A24 path (`findings`, `--check`, `--sites`) never passes `raises`.
2. `test_judgment_census.py`:
   - `units_of` calls `refusal_registry.sites(plugin_root=root, files=..., raises=refusal_registry.raise_family(root, files))`. The family is computed over the SAME scanned file set: tests are excluded, so a test-only subclass is not in it;
   - the u3 docstring line and the BLIND_SPOT texts are rewritten (§B.2): "subclasses are counted";
   - the misses that remain are named: alias imports (`from x import A as B`), `raise A` with no call, stdlib subclasses (`json.JSONDecodeError`, ...), bases that are not a plain name (`class X(make())`), and the attribute form if F-B3 leaves it out. Name collisions are counted (over-inclusion, the safe side);
   - `blind_spot_names_subclass_gap` is rewritten, for example to `test_blind_spot_states_subclasses_counted`: the old gap clause is absent from `BLIND_SPOT` and `about`, and the remaining misses are named;
   - the totals line prints the family size.
3. `judgment-census.json`: the new rows (F-B1); `about` rewritten; the `ratchet` ceilings raised to the measured counts, in ONE commit (dense: ceiling == count).

## B.4 Edges

| # | edge | behaviour | invariant protected |
|---|---|---|---|
| E1 | the error direction of the reused scanner, now in a more consequential role (advice -> a gate on the census) | `sites(raises=family)` may err only toward EXTRA units (over-inclusion). It never hides a raise of a family name it can resolve | a refusal through a package subclass is never invisible to the census |
| E2 | adversarial inputs that must stay COUNTED: a direct subclass; a subclass of a subclass; a base written `mod.StateConflict`; a class defined inside a function; multiple inheritance `class C(Mixin, ValueError)`; a subclass defined in module X and raised in Y through `from X import A` | counted (table rows in §B.5) | the same |
| E3 | a name collision: `class Unreadable(Exception)` in one module and `class Unreadable(ValueError)` in another (`branch_accounting.py:78` defines `Unreadable(Exception)`; a ValueError twin is not verified) | counted wherever `raise Unreadable(...)` appears (over-inclusion). The measurement prints the collisions; the builder's report names each counted false positive with a row (class `shape`, owner `data`), or with `blocks_override: false` plus a `note` if it does not refuse | the safe side is extra, never hidden |
| E4 | `raises=None` (the A24 audit) | byte-identical answer to today. The test proves it: `sites()` on the real package without `raises` equals the list from before the change (compare lengths and the first and last keys) | A24 does not widen silently (non-goal) |
| E5 | an empty family (no subclass anywhere: a synthetic package) | `raise_family` returns exactly `REFUSAL_RAISES` | the literals are always matched |
| E6 | a class that inherits from itself or from a cycle | the closure ends: a fixpoint over a finite set | the scan terminates |
| E7 | a new unit the builder judges `meaning`, `meaning-proxy` or `word-list` | the node STOPS that row and reports it as a finding of an AR-29 breach. It is never committed as a widening raise. A blocking breach-class row raises `breach`, and `tools/architecture_gate.py` then demands `moves <what> to code`, which would be a false statement (F-B4). `MEANING_CEILING` is never edited | a widening never smuggles in a breach raise |
| E8 | the raise itself | ONLY the ceilings the measurement moves are raised, each to its exact new count (dense). The commit message and the critic verdict list each key, old -> new, with the reason "census widened to subclass raises (OH8-7)" | AR-20: no silent raise |
| E9 | `judgment:` form (gate item 7 (v)) | a raise of only `blocking_per_role.*` and/or `safety`: `judgment: adds data check <unit> -- census sees refusals through package subclasses`. Any other key raised -> stop (E7, F-B4) | the gate's form is never answered falsely |
| E10 | TEMPORAL: the family is computed on every run, and no stored artifact is created | before the node, `sites()` has no `raises`; after it, the census passes it. Both worlds give A24 the same answer | — |
| E11 | the cost of the run: the census already measured 138 s with several walks (:110) | the family helper parses each scanned file once more. Accepted (a test-only cost). C-B3 proposes reusing the census's parsed trees if the Lead prefers | — |
| E12 | a unit found only through a stage row or the registry that now also has a subclass site | still one unit, keyed (file, function) | one row per unit |

## B.5 Tests (`test_judgment_census.py`: a keep row, layer `register`, `test-layers.json` l.2708; not quarantined)

One parameterised test, built with the synthetic-package helpers already in the file (`_package`, `_census`, `_row`, `_run`, :516-551): `test_neg_subclass_raises_are_units`. Each row is a small source text. Its id names the case. The expectation is "C1 names `helpers_x.py::f` as a unit (u3)", or not.

| id | source | counted |
|---|---|---|
| `literal` | `def f(x):\n    raise ValueError('no')` | yes (unchanged control) |
| `direct` | `class A(ValueError): pass` + `def f(x): raise A('no')` | yes |
| `grandchild` | `class A(ValueError)`, `class B(A)`, `raise B(...)` | yes |
| `attr_base` | `import event_store as ES` + `class A(ES.StateConflict)`, `raise A(...)` | yes |
| `nested_class` | the class defined inside another function, raised in `f` | yes |
| `multiple` | `class A(Mixin, ValueError)` | yes |
| `cross_module` | `class A(ValueError)` in `mod_a.py`; `from mod_a import A` and `raise A(...)` in `helpers_x.py` | yes |
| `unrelated` | `class A(Exception)`, `raise A(...)` | no |
| `tests_only` | `class A(ValueError)` defined only under `scripts/tests/`, raised in `helpers_x.py` | no (the family is computed over scanned files only; stated as a miss) |
| `attr_raise` | `raise ES.StateConflict('no')` | per F-B3: yes (F-B3 (a)), or no plus a named miss |
| `alias` | `from mod_a import A as B`, `raise B(...)` | no (named miss) |

Plus E4's check: real-package `sites()` without `raises` keeps today's length.

Mutation (DoD 7): make `raise_family` return only `REFUSAL_RAISES` (no closure). Then the rows `direct`, `grandchild`, `attr_base`, `nested_class`, `multiple` and `cross_module` must turn red, and so must C1 on the real census (the new rows become stale).

The ratchet proof: the builder pastes the C3 output of an intermediate state (new rows in, ceilings still old), which shows "`blocking_per_role.conductor` is N, above its ceiling 476". Then the green run with the raised ceilings.

## B.6 DoD (inline)

1. The §B.2 measurement output is in the spec before the dispatch (the Lead's move). The builder re-runs it on the node tree and pastes it.
2. §B.3 is applied as decided in F-B1, F-B2 and F-B3.
3. Grep `ast.Raise` in `test_judgment_census.py`: no hit (positive control: `refusal_registry.py:1071` is hit). `test_c6_totals_line` stays green.
4. No "invisible" subclass clause remains in `BLIND_SPOT`, in `about` or in the docstring. The remaining misses are named. The rewritten blind-spot check passes.
5. `python -B ai-packages/qa-factory/scripts/tests/test_judgment_census.py` is green. The before and after totals lines are pasted.
6. Every raised ceiling is listed (key, old -> new, reason) in the commit message and the report. No key outside `blocking_per_role.*` / `safety` is raised (E7, E9).
7. The mutation of §B.5 is run once, with a byte copy and a hash witness. The red ids are quoted.
8. Witness: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for C:\QAFactory\forge-repo\.claude\worktrees\oh8-7\ai-packages\qa-factory\scripts\tests\test_judgment_census.py C:\QAFactory\forge-repo\.claude\worktrees\oh8-7\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json C:\QAFactory\forge-repo\.claude\worktrees\oh8-7\ai-packages\qa-factory\scripts\refusal_registry.py`. Run every printed non-slow, non-quarantined file. Slow files are named, not run.
9. `python -B ai-packages/qa-factory/scripts/selftest.py --lang` passes.
10. The commit message carries:
    - `architecture: AR-29, AR-20, AR-13, AR-22, AR-28 -- <how kept>`;
    - the `judgment:` line of E9;
    - the raise list;
    - the four questions and the full axis block (a machine check changes, rule 10).

## B.7 Hot files and D-0048

| file | hot | functions touched | outside a function |
|---|---|---|---|
| `refusal_registry.py` | yes in batch 8 (l.10: "after OH7-2"; OH8-6 also writes it) | `_refusal_calls`, `sites`; the new `raise_family` | none. The module docstring is NOT touched: OH8-6 owns the `SCOPE` paragraph. With that, the two lists are disjoint |
| `tests/test_judgment_census.py` | no | `units_of`, `totals_line`, `blind_spot_names_subclass_gap` (renamed), the new `test_neg_subclass_raises_are_units`, `TESTS` | the module docstring, `BLIND_SPOT` |
| `tests/fixtures/judgment-census.json` | no | — | `about`, `ratchet`, new rows |

---

# Lead decisions (coordinator Opus, 2026-11-13; "решила сама", by recommendation until the owner's word)

The §B.2 measurement was run by the coordinator on origin/main 2f1cec8, with the script above saved to the scratchpad and not committed:
```
family size (beyond the 2 literals): 56
units before/after: 951 1223
new units needing a row: 272
blocking_per_role after (existing rows only): conductor 476 -> 496; every other role unchanged
C3 after: `blocking_per_role.conductor` is 496, above its ceiling 476
name collisions: []
new units in 59 files (assertion_detectors.py ... vcs_evidence.py)
```
- **F-A1: (a).** A local import in `__init__`, and the leaf docstring is rewritten.
- **F-B1: (d).** This node lands the mechanism under (c1): subclass raises flip `blocks` on EXISTING units only, and the raise is conductor 476 -> 496, named row by row. The 272 u3 units become follow-up nodes, OH8-7b and onward, each classifying one file group of at most ~60 units with a named raise. They run one after another, because they share `judgment-census.json`. `BLIND_SPOT` names the temporary second road and points to the follow-up nodes. The end state equals (a).
- **F-B2: (a).**
- **F-B3: (a).** The builder reports the attribute-form count it added.
- **F-B4: (a).**
- Part B gets a critic-on-plan before any builder (PROJECT.md "package change" item 6 (b): the census changes meaning). Part A goes straight to its builder: no fork is left, and it changes no meaning.

# Forks (returned; none decided)

**F-A1. How `event_store.py` reaches `hooklib`.** `event_store.py` is deliberately "a leaf of the standard library while nothing is refused" (`_require_root` docstring :514-515; its one hooklib import is local, at :521).
- (a) A local `import hooklib` at the top of `__init__`. After this, every store construction imports hooklib, so the leaf statement must be rewritten. Cost: a docstring edit, plus a hooklib import on the first construction (cached afterwards). hooklib imports only the standard library at module level (`hooklib.py:2-13`), so there is no cycle.
- (b) A fast path: the default `STALE_MARKER` skips the survivor, and only a custom marker reaches it. The leaf stays a leaf for the default. But the default constant takes a second road around the shared check: a P31 / designer rule 6 case, so it would need the owner's word.
- (c) A module-level import. Same as (a), and less local.
- Recommendation: (a).

**F-B1 (LOAD-BEARING). About 157 new units (estimate; §B.2 measures it), and each needs its own row with a judged class, roles and owner.** As the Lead asked, the options are given with their costs and none is picked.
- (a) Classify all of them in this node. The builder reads each function and writes `class`, `roles` and `owner`, with a one-clause reason per row. The critic, as the tier above, samples and checks under question 11.
  - Cost: about 157 judgments (several hours of builder work), a heavier critic pass, and a large raise of `blocking_per_role.*` for EVERY role named.
  - Possibly `safety` rises too. A breach-class row stops the node (E7).
  - The end state is fully counted, with no blind spot.
- (b) A separate data-only row source: for example, a row with `"pending": "OH8-7"` and no class, plus a new shrink-only ceiling `pending` that the census counts. Later nodes classify the rows in chunks.
  - Cost: a schema change and a new axis-18 member (rule 10: the four questions, critic question 9).
  - `tools/architecture_gate.py` treats an unknown new key above 0 as a raise that needs `moves ... to code`, so the gate needs an edit too (outside the package).
  - It also bends "the class is never defaulted" (C1's text, :293-294).
- (c) Narrow the widening.
  - (c1) Subclasses only flip `blocks` on EXISTING units (b1) and create no new u3 units. That means zero new rows, and only the measured flips (+22 for conductor on the older tree) are raised. Cost: a function that refuses only through a subclass, under a neutral name, stays invisible. That is a different road for the same action as a literal raise (P31 / rule 6: this goes to the owner). The blind-spot text then shrinks rather than disappears.
  - (c2) Only the five named classes (`ConfigUnreadable`, `PathSyntax`, `WindowsUnreadable`, `PreparationError`, `LaunchIdRowRefused`). This is an arbitrary exclusion of the other ~40 classes, a P31 case.
- (d) Two nodes: land the mechanism now under (c1), then a follow-up node (or nodes, per file group) adds the u3 units with judged rows. Each chunk is a named raise, and the end state equals (a). Cost: two or more critic passes, and a temporary second road that is named in `BLIND_SPOT` until the follow-up lands.

**F-B2. Where the widening lives.**
- (a) A `raises=` argument on `refusal_registry.sites()`, plus a family helper in `refusal_registry.py`. The default stays unchanged, so A24 does not widen. `refusal_registry.py` joins owns (a hot file, with the OH8-6 overlap handled by §B.7).
- (b) Widen `REFUSAL_RAISES` globally. A24's audit over `SCANNED` then widens too: new A24 findings for subclass refusals in `stage_guard.py`, `inject_context.py` and others, each needing a REGISTRY entry and a test. That widens the scope a lot.
- (c) The census computes the family from its own parsed trees and passes it in as `raises=`. That is (a) with the class walk living in the test (C-B3).
- (d) The census matches raises itself. This breaks axis 32's "no second AST walk over refusals" and AR-13. Not recommended.
- Recommendation: (a). The batch row's owns (test plus fixture only) were written before this was visible.

**F-B3. Attribute-form raises (`raise ES.StateConflict(...)`, `raise mod.SubError(...)`).** Today they are invisible even for the literal names: 8 attribute-form raise sites in non-test scripts (grep; how many are in the family is not measured). Options:
- (a) include them now, in the same `_refusal_calls` change: same walk, a small extra count measured by the §B.2 rerun;
- (b) name them as a remaining miss in `BLIND_SPOT`, plus a finding.
- Recommendation: (a). It is the same class (a refusal raise the scanner cannot see), and rule 9 says fix the class now.

**F-B4. A raise the gate can only accept with a false line.** `tools/architecture_gate.py` item 7 (v) accepts a raise of `blocking_per_role.*` / `safety` with `adds data check <unit>`. Any other key raised needs `moves <what> to code`, which is false for a widening. Options:
- (a) the node stops on any such row and files a breach finding (E7, E9);
- (b) a new gate form, for example `judgment: widens census -- <why>`, which is a `tools/` mechanism change (rule 10) outside this batch.
- Recommendation: (a).

# Small technical choices closed by the designer

- C-A1: the three new calls are written `hooklib.is_one_component(...)` so the existing spy covers them (the t-282 C-1 precedent).
- C-A2: `selftest._slow_tests_problem` imports hooklib locally, following that file's existing pattern of local imports (`selftest.py:380`, :402, :537, :761). The redundant `not name` goes away, because the survivor refuses `""`.
- C-A3: `event_store.py`, `selftest.py` and `dependency_drift.py` join the `covers` of the `test_resolver.py` keep row (the t-282 F-2 (a) precedent), so the witness prints the table that judges them.
- C-A4: the table extends `OH61_ROWS` (variant rows), with no new function table. Check ids keep the `OH6-1 ` prefix.
- C-B1: the rewritten blind-spot check gets a `test_` prefix, so pytest collects it as well as script mode.
- C-B2: the family is computed over `scan_files` (the same set the census reads). `scripts/tests/` classes are excluded.
- C-B3: the default is a second parse in `refusal_registry` (simpler, and keeps the class logic beside the scanner). Reusing the census's trees is the alternative named in F-B2 (c).
- C-B4: the new helper's name must not match `UNIT_NAME_RE`, or it becomes a census unit itself.

# Contradictions and analogs noticed (reported, not widened)

- Batch-8 row OH8-1 and the finding give `event_store.py:482`. On origin/main it is :494.
- Batch-8 row OH8-7 says the ratchet is raised "from 489". The census on origin/main holds `conductor: 476` (`judgment-census.json` l.4). The finding's 474 -> 496 counts only existing rows (§B.2). The real raise will be larger.
- Batch-6 still shows OH6-1 and OH6-3 as "ожидает", but both are in origin/main (the sentinel at `test_resolver.py:1676-1721`; `TEMP_NAME_HEX = 8`). The batch status lags.
- `blind_spot_names_subclass_gap` is not collected by pytest (no `test_` prefix). Other script-only checks in keep files may share this. That analog is not walked here.
- `refusal_registry._refusal_calls` misses `raise mod.Name(...)` for the literal names too (F-B3). This also affects A24 over `SCANNED`, which is not in this node.

# Reading trail

All paths are under `C:\QAFactory\forge-repo\.claude\worktrees\read-main\` unless absolute.
- `plans/piles/onboarding-hooks/batch-8-ostatki-t-282-t-254-t-287.md` (whole); `batch-6-ostatki-t-203-i-t-227.md` :1-12, :29-34; `batch-7-ostatki-t-263.md` (grep: the OH7-2 row); `plans/piles/onboarding-forge/batch-2-onboarding-roles-forge-p3.md` (grep: SC2-23, SC2-26, status).
- Findings (whole): `20261113-is-one-component-kopii-vne-oh6-1.md`, `20261113-kopii-proverki-odnoj-komponenty-puti.md`, `20261113-komponenty-puti-bez-potolka-dliny.md`, `20261113-oh7-2-f2-2-rasshirenie-perepisi-na-podklassy-isklyuchenij-otkaza.md`.
- `docs/tasks/specs/t-282-oh6-1-one-component.md` :1-100, :165-367. The review t-286 was not opened: its fixes are folded into t-282 §10, which was read.
- `ai-packages/qa-factory/scripts/event_store.py`: :1-60, :468-531; greps for `import`, `stale_marker`, `_publish`/`TEMP`, `Path(`.
- `scripts/selftest.py`: :955-1004; greps for imports, local imports, `sys.path`, `_slow_tests_problem`.
- `scripts/dependency_drift.py`: :1-130; a grep of `os.`.
- `scripts/hooklib.py`: :269-299; a grep of imports and `event_store` (no hit; same-tool positive control: `import` lines found).
- `scripts/tests/test_resolver.py`: :1420-1510, :1560-1760.
- `scripts/tests/test_event_store.py`: :846-860.
- `scripts/manifest_put.py`: grep of `MANIFEST_STALE_MARKER` (:133).
- `references/project-dependencies.json`: grep of `"file"`.
- `scripts/tests/test-layers.json`: :2706-2719, :4318-4371, :5039-5048, :7796-7803; greps for the section heads (`keep` :35, `pin_holds` :6959, `quarantine` :7013) and the file names.
- `scripts/tests/test_judgment_census.py` (whole).
- `scripts/tests/fixtures/judgment-census.json`: :1-4; a count of `"file":` (951); grep of the event_store / selftest / dependency_drift rows; grep of `refusal_registry.py` rows (no hit; positive control: the same pattern shape found the event_store rows).
- `scripts/refusal_registry.py`: :1-70, :1030-1189; grep of `REFUSAL_RAISES` / `sites` usage across the tree.
- Greps over `scripts/`: class definitions (persisted output; count of direct ValueError / StateConflict subclasses: 51 in 41 files); attribute-form raises (8 non-test hits); helper names (`subclass|famil|...`: no hierarchy helper).
- `tools/architecture_gate.py`: :25-104, :268-307.
- `design/architecture.md`: :134-223 (AR-29, AR-13 ... AR-20).
- `docs/SIBLING_MAP.md`: axes 18, 32, 34 (:386-396, :557-593).
- `plans/builder-rules.md`: grep 7b (:14-27, :66-73).
- `scripts/tests/scenario_walk.py`: grep `--witness-for` (:14, :833).
- A grep for the blind-spot clause over the whole tree (5 files: 2 in the package, 3 historical specs).

Needed beyond the manifest: `tools/architecture_gate.py`, `scripts/refusal_registry.py`, `scripts/hooklib.py`, `scripts/manifest_put.py` (one grep), `references/project-dependencies.json`, `scripts/tests/test_event_store.py` and the onboarding-forge batch 2 file. `docs/TESTING.md` was not opened; the keep / quarantine facts were read from `test-layers.json` directly.
