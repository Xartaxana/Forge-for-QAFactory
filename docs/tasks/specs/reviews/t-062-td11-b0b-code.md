# t-062 — critic on TD-11 node B0b (builder t-060, report t-059): the layer test of every family

Under review: `ai-packages/qa-factory/scripts/tests/test_driver_layers.py` (worktree `td11-integration`, uncommitted) and the B0b part of `fixtures/driver-layers.json` (header `family`, `allowed_importers`). Not under review: P0-C's `source_readers`/`source_mentions` edits, and P1-1's rows (homes, layers, exceptions), which were being edited while I read.

## Verdict

**NEEDS WORK (fit_with_fixes): 2 blocking findings, 8 fixes for this round, 7 queue lines.** The generalisation is sound. Discovery, the header, per-map skipping and the gizmo re-run all work. M8 and m6 are fixed as the earlier verdict asked. 195/195 reproduced. Both blockers come from the dispatch DoD narrowing the spec (items 4 and 6), not from the builder departing from it. The Lead decides whether to take the fixes in this round. This verdict is an input to that decision, not the acceptance itself.

## Blocking findings

**B1. L12's import clause does not cover `cut: mixins`. Equal-rank imports, cycles included, pass (spec B §2.6 L12 row, §12 E1 invariant, P31).** At `test_driver_layers.py:834` the rule only runs for `fam["cut"] == "functions"`. The fixture at `:1348-1349` ("L12 (mixins cut) an equal-rank import stays a matter of L6 alone") pins this open behaviour. Mutation on a temp copy: a mixins map with `layers [[driver_a, driver_b],[story_run]]`, `driver_a.py: import driver_b`, `driver_b.py: import driver_a`. Result: L6 `[]`, L12 `[]`. A plain-`import` cycle is silent in Python. The spec has one rule: "no part imports another part except lower-ranked function parts and `<prefix>base`", and E1 says "no import between equal-ranked parts". Leaving the mixin cut outside that rule is a case excluded from a shared mechanism, with no data row and no owner's word (question 12, rule 19). After P1-1, the map puts six stage modules at rank 6 (`driver_stage_plan` … `driver_stage_s8s9`, read from the live map). That is exactly where this rule has to hold. **Fix:** one rule for both cuts: a part imports only a strictly lower-ranked part, or `<prefix>base`. Flip the fixture to `expect`. Cost for the driver: none today (`driver_chains` and `driver_timing` import no family module, by my probe). At the cut, a stage-to-stage constant gets rehomed to a lower rank (spec B §2.2 rule 4) instead of becoming a silent edge. **P1-2 should not proceed before this fix**, or else its DoD must assert that no part imports a part of equal rank.

**B2. The per-family pin does not tighten. Removed upward edges can come back unseen (AR-20; SIBLING_MAP axis 18: "a stale row is a refusal … never a silent shrink").** `PINNED_EXCEPTIONS` (`:60-75`) holds 14 rows. The live map holds 8: by my probe, `pin - map` = `Driver.__init__>UNTIL_PAST>name`, `Driver.conductor>Driver.boundary_dispatch>call`, `Driver.continuation_note>HANDOFF_FORM>name`, `Driver.finish>WINDOW_ROUND_STAGES>name`, `Driver.s1_person>S1_GAP_RE>name`, `Driver.s1_person>S1_REVIEW_RE>name`. HEAD already had 13 against the pin's 14. The only checks are subset checks (`:812-816`, `:1393-1396`). Trace: a cut that restores any of those 6 edges and adds its row passes. Line 793 skips it (it is in `exc`) and line 814 skips it (it is in `pinned`). The DoD said "driver rows unchanged", so the builder followed it. That makes this a dispatch defect, but it still defeats the gate at the cut. **Fix:** a pinned row that the map no longer holds is a problem: "drop it from PINNED_EXCEPTIONS". Then set the pin equal to the map (8 rows after P1-1). Whichever of B0b and P1-1 lands second sets the pin. **P1-2 should not proceed before this fix.**

## Fixes for this round (not blocking P1-2)

- **F1. L11 (c) fails open through any alias** (`:420-433`, `:466-471`). With `installed: false`, three facades pass L11 with `[]`: `import module_facade as mf; mf.install(...)`, `from module_facade import install as inst; inst(...)`, and `getattr(module_facade, 'install')(...)`. When the flag is wrong, all of (b) is skipped silently. Fix: with `installed: false`, refuse any import of `module_facade` in the facade, in any form (reuse `_imports_of`). In (b), also check that the first argument is `__name__` (a literal `'story_run'` passes today, and E5 needs `__main__`) and that the call sits at module top level (`if False: module_facade.install(...)` passes today). P1-2 is not blocked: the tool writes the literal form (`tools/source_split.py:1254`, config `source-split-carriers.json:8`), and P1-2 sets `installed: true`.
- **F2. Two import walkers in one file disagree.** `_imports_of` (`:403-417`) sees literal `import_module`/`__import__` calls. The L6/L12 loop (`:824-829`) does not. Mutation: `driver_core.py: importlib.import_module('driver_dialog')` (an upward import) gives L6 `[]`, and the same form at equal rank in a functions family gives L12 `[]`. Fix: the loop uses `_imports_of`.
- **F3. Q1, AR-1 and DoD item 1.** `L8_SKIP_BY_FACADE = {"story_run": {...}}` (`:52`) is a family-named table in check code. Move it into the map as an optional header key (e.g. `instrument_files: [{file, reason}]`), shape-checked in L10. The cost is a few lines.
- **F4. L11 (a) silently skips any script it cannot parse** (`:448-451`). Mutations: a script starting with a UTF-8 BOM, `\ufeffimport driver_core`, gives L11 `[]` (Python runs that file fine). A script with a syntax error after the import also gives `[]`. Fix: read with `utf-8-sig`, and report an unparsable script as a problem. Today there is no BOM script and no unparsable script in `scripts/` (my probe), so this is not live.
- **F5. L10 header gaps.** (i) A stem listed twice in `layers` is accepted and the later rank silently wins (mutation: L10 `[]`). (ii) `facade: "tests/harness"` passes the header and then crashes `analyse` with `KeyError` (loud, but not reported). Require `facade.isidentifier()`. (iii) `class: null` with class tables present: the info line says "class clauses … not run", yet L3/L4 report every row as untouched. Refuse class tables on `class: null`. (iv) Spec §2.1 names the file `<prefix>-layers.json`, but nothing checks that the file name matches `family.prefix`, or that one facade has only one map. A second map naming `story_run` inherits the driver's pin.
- **F6. Q3/E8, built without new data.** In `real_maps`, check that every `scripts/*.py` that imports `module_facade` is the `family.facade` of a discovered map. My probe showed that `controller_layers.json` (underscore) is silently not discovered. This check catches a misnamed map and an installed family that has no map.
- **F7. L12 scope.** (i) The spec says that inside a part only `<Class>Base.<m>` or the mixin of the body's own home are allowed. `l12_class_use` (`:508-510`) accepts the assembled class `<Class>.<m>` anywhere, and in a part that is a NameError at run time. Refuse it when the access is in a part (`stem != facade`). (ii) Module-level code and class bodies are not scanned. Mutations: `TABLE = {'t': DriverCore.top}` and `T2 = DriverCore.top` in the class body both give L12 `[]`. Both fail loudly at import time, so this is low severity.
- **F8. Dead code.** `per_file` (`:865-868`) is computed and never read. It was already there, but it sits inside the L8 block this diff rewrote. The `case` parameter of `problems_of` (`:1091`) is unused.

## Queue (outside B0b's owns; the Lead writes each into «Остатки» with an owner)

1. `harness.driver_sources` (`harness.py:54-73`) is a second reader of the file set that `family_paths`/`read_modules` (`:102-120`) now read generically (AR-13). Converge them on one `family_sources(fam, exempt)` | узел: harness owner (P0-C successor).
2. L8 does not count a test that reads the family through its own glob (`test_audit_rules.py:1049`, `fnmatch(..., "driver_*.py")`) or a name built at run time (`'driver_' + 'core.py'`, `f'driver_{a}.py'`, `b'driver_core.py'`; each gave L8 `[]`). Count the literal `<prefix>*.py` as a family read | узел: L8 follow-up.
3. `Person` is still hard-coded in L4 (`:748`, `:299-311`, `:195`). Read the class from the `on` of `adhoc_attributes` rows.
4. A third import walker, `scenario_walk._imports_of` (`scenario_walk.py:835-846`) | узел: one-walker convergence.
5. Code quality: `analyse()` (`:524-914`, 390 lines; it grew), `l11_problems` (`:436-502`, 67 lines, new), `bad_fixtures` (`:1135-1352`, 218 lines). Split `analyse` by check.
6. The `not_driver` reason for `driver_journal` ("the driver never imports it") is false: `story_run.py:1890` has `import driver_journal`. A map-text fix for the map's owner. A check that "no family file imports a `not_driver` module" would make the reason checkable.
7. SIBLING_MAP axis 18 lists only `fixtures/driver-layers.json`. Make it `fixtures/*-layers.json`, and decide whether `allowed_importers` (an AR-13 exemption list with no pin) is a member | Lead.

## Answers a-f

**a. Fail-open hunt.** Caught: a part file with no row or no layer (L1); a row homed in a part while an installed facade defines the name (L11 b, plus L2); an upward `import` (L6); an equal-rank import in a functions family (L12); outside importers written as `from x import y`, `import x as z`, `importlib.import_module("x")`, `__import__("x")`, including a planned part with no file yet; install called out of order, twice, or with string names (all three L11 b); a broken map beside a good one (FAIL for that map, the others still run; invalid JSON also FAILs); a new family's exception (L5 "is new"). Open: equal-rank import in a mixins family (B1); `installed: false` with install through an alias (F1); an upward or equal-rank import through `importlib` (F2); an outside importer in a BOM file or an unparsable file (F4); outside imports with a non-literal `import_module` name or `spec_from_file_location` (dynamic forms, not in the spec: accepted gap); module-level and class-body class-name access (F7). Prefix overlap (`gate_` vs `gate_brief_`) fails closed: L1 lists every `gate_brief*` file as unlayered. The spec's nine prefixes do not overlap, though no cross-map check exists (F5 iv). `class: null` with class tables fails closed but with a misleading line (F5 iii).

**b. Did each check run on the real map?** L1 ran (1023 names against 1023 rows). L2 ran. L3 ran (every optional table is present, so no "table(s)" line; class `Driver`). L4 ran. L5 ran (8 upward edges against 8 rows). L6 ran but was vacuous: neither part imports a family module. L7 ran. L8 ran (72 sites). L9 ran. L10 ran (header plus rows). L11: (a) ran and matched the one `allowed_importers` row; (c) ran; (b) did not run, and an informational line says so. L12: the class-name clause ran but was vacuous (no `Driver<Area>.x` access exists today); the import clause did **not** run for the mixin cut, and **no line says so** (B1). Checks that switch on at the cut: L11 (b) when `installed` turns true; L12's class clause once T-1 writes mixin names; L2's placement and L6 with real parts; L8 for each new part's file name.

**c. M8 and m6.** M8 is fixed. `l8_extra` and the temporal rule are gone, and every family file name counts. The `SCRIPTS / 'driver_core.py'` mutation is reported by L8. The docstring exclusion is the same rule for every name: one `_literal_mentions` call per file name, and comments are not AST nodes. It is sound, because a docstring cannot read a file. Today I find two hits for `driver_(chains|timing)\.py` in `scripts/tests/*.py`, both in docstrings (`test_driver_chain.py:1069`, `test_driver_timing.py:2`), not three. Built names are not counted (queue 2). m6 is fixed: `DriverTypo.low` is reported, and a wrong mixin is reported with the expected class named. F7 (i) is a spec-level tightening beyond what m6 asked for.

**d. The builder's questions.** Q1: an AR-1 breach. Move it into the map now (F3). Q2: correct. A mixins family with `class: null` would census no members, which is the open direction. A functions family with a class only censuses more. Q3: build F6, which needs no data. Q4: yes, refuse it (B1). A plain-import cycle is silent. The cost for the driver is zero today, and at the cut it means rehoming constants by spec B §2.2 rule 4.

**e. The pin.** A new family cannot smuggle in an exception: a facade with no pin is pinned empty and L5 says "is new" (probed). A second map that names an existing facade inherits that facade's pin (F5 iv). The driver's pin can only grow through a test-code edit, which axis 18 makes visible in review. But it currently has 6 rows of slack, so the map can grow back without any edit to the pin (B2).

**f. Standing items.** DUPLICATION AND CONSISTENCY: two import walkers in the file (F2); a third in `scenario_walk` (queue 4); the file-set reader in `harness.driver_sources` (queue 1); `module_facade`/`install` written in the test while the tool reads them from `source-split-carriers.json:8` (accepted: the package test does not read `tools/`); the tool's own census, `rank`, `camel` (`source_split.py:121`, `:743-771`) and its `--class` CLI next to the header's `class` (T-2 reads the header, brief item 10, queued there). CODE QUALITY: queue 5, F8. ARCHITECTURE: AR-1 (F3, queue 3); AR-13 (queue 1; L11 enforces AR-13 for scripts); AR-15 (F2); AR-20 (B2); AR-22: the new keys `family` and `allowed_importers` have producer and reader in one commit, and `driver_golden.layer_map` (`driver_golden.py:101-114`) reads only `layers`, which is unchanged. JUDGMENT: none. Every check is data, shape or xref. ONE ROAD: B1 is the one case found (grepped `cut ==` and `installed` branches in the test). The `installed` branch serves the task's own temporal condition and the mechanism is reached afterwards, so it is not a P31 exclusion. TESTING.md: the test is the `gate_named` ratchet (`test-layers.json:1141`). The header cases are one parameterised table. The fixtures test the checker, so they are not negative controls inside a test. Hygiene: ASCII-only, LF kept (0 CRLF at HEAD and now), no control bytes.

## Lines L1-L12

L1: holds; part with no layer and def with no row are probed and caught. L2: holds, unchanged. L3: holds; table-optional as specified. L4: holds; `Person` hard-coded (queue 3). L5: holds per family; the pin is slack (B2). L6: holds for `import`/`from`; misses `importlib` (F2). L7: holds, unchanged. L8: M8 fixed; built names not counted (queue 2). L9: holds; table-optional. L10: header and optional keys checked; duplicate layer stem, facade path and class tables open (F5). L11: (a) holds for literal forms, unparsable files skipped (F4); (b) holds for literal forms; (c) fails open on aliases (F1). L12: m6 fixed; mixin import clause missing (B1); scope (F7).

## What I did not check

The P1-1 rows of the map (they were being edited while I read); P0-C's L8 rows; `module_facade.py` itself; T-1's behaviour beyond the facade line it writes; the full `test_story_run_words` (the builder reported 115/115; I did not re-run it, it is canon's).

## Trail

Read: the B0b report (`docs/tasks/specs/reports/t-059-td11-B0b.md`); `test_driver_layers.py` 1-1429 (whole file) and HEAD for comparison; the json diff and the live header lines 1-6; spec B §2.1-2.6 (lines 40-174) and E1-E12; lead brief items 1-12; t-045 M8/m5/m6; `critic-diff-brief.md`; `TESTING.md` 86-110; `test-layers.json:1141`; `harness.py:47-73`; `scenario_walk.py:835-859`; `driver_golden.py:95-114`; `source_split.py:118-125`, `:743-771`, `:1244-1259`; `module_facade.install` docstring; SIBLING_MAP axes 6 and 18.

Re-runs and probes (temp roots from `tempfile.mkdtemp`, outside the repo; nothing written in the worktree):
- `python -B <wt>/ai-packages/qa-factory/scripts/tests/test_driver_layers.py` gave `=== test_driver_layers: 195/195 ok ===`, 195 PASS, 0 FAIL, exit 0. Notes printed: only `L11 (b): not run`.
- Probe battery against `analyse()` (stdin script): the outcomes quoted above, including `outside: importlib.import_module('driver_' + 'core')` giving no L11, BOM and syntax-error files giving no L11, three alias forms with `installed: false` giving L11 PASSES, the equal-rank cycle in mixins giving L6/L12 PASSES, `importlib` upward giving L6 PASSES, duplicate layer stem giving L10 PASSES, `facade=tests/harness` crashing with `KeyError`.
- `real_maps()` with `harness.FIXTURES` pointed at a temp dir holding a copy of the driver map, a broken-header map, invalid JSON and `controller_layers.json`: FAIL for the invalid JSON, FAIL L10 for the broken prefix, the driver map 12 PASS, `controller_layers.json` not discovered.
- Pin against map: pin 14, map 8, the 6 slack rows listed in B2. At HEAD the map had 13.
- Independent search for outside importers (case-insensitive `^\s*(import|from)\s+driver_(chains|timing)|import_module\(.driver_` over `scripts/*.py`): only `story_step.py:889` is outside the family. Positive control: the `story_run.py` hits at :71 and :1935 were found by the same search.
- Hygiene byte count: nonascii 0, CRLF 0, control bytes 0.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1 test_driver_layers.py:834 and fixture :1348-1349 - the L12 part-import rule runs only for cut functions; in a mixins family an equal-rank import, even a two-way cycle, passes L6 and L12 (probed). Spec B 2.6 L12 and E1 forbid it; P31. Fix: one rule for both cuts (strictly lower-ranked part or prefix base) and flip the fixture. P1-2 must not proceed before the fix, or its DoD must assert no equal-rank part import",
    "B2 test_driver_layers.py:60-75, :812-816, :1393-1396 - the per-family pin is checked as a superset only; pin 14 rows against map 8, so 6 removed upward edges can come back at the cut unseen (AR-20, axis 18 stale-row semantics). Fix: a pinned row the map no longer holds is a problem; set the pin equal to the map. P1-2 must not proceed before the fix"
  ],
  "fixes": [
    "F1 L11 (c) :420-433/:466-471 - with installed false, refuse any import of module_facade in the facade (alias, from-import alias and getattr all pass today); in (b) also check that the first argument is __name__ and that the call is at module top level",
    "F2 :824-829 - the L6/L12 import loop must use _imports_of; a literal importlib.import_module upward or equal-rank import passes today",
    "F3 :52 - move L8_SKIP_BY_FACADE into the map as an optional header key, shape-checked in L10 (AR-1, DoD item 1)",
    "F4 :448-451 - L11 (a) silently skips an unparsable script (a BOM or a syntax error hides its imports); read with utf-8-sig and report unparsable files",
    "F5 header_problems - refuse a duplicate stem in layers, a non-identifier facade (tests/harness crashes analyse), class tables on class null; check that the map file name matches the prefix and that one facade has one map",
    "F6 real_maps - every scripts/*.py importing module_facade must be the facade of a discovered map (E8 part-without-map with no new data; a misnamed map is invisible today)",
    "F7 l12_class_use :508-510 - refuse the assembled-class access inside a part (spec L12); module-level and class-body class-name accesses are not scanned",
    "F8 dead code: per_file :865-868, the unused case parameter of problems_of :1091"
  ],
  "class_completeness": "The fail-open class (a gate passing a wrong tree) was walked over L1-L12 by mutation: open instances are B1, F1, F2, F4, F7. The import-walker surface was walked across three walkers (two in this file, F2; scenario_walk queued). Axis 18: B2 found, and the member row widening is queued to the Lead. Axis 34: B1 is the only one-road case found. Queue lines 1-7 carry the analogs outside the owns.",
  "trail": {
    "read": [
      "C:/QAFactory/forge-repo/.claude/worktrees/td11-integration/docs/tasks/specs/reports/t-059-td11-B0b.md",
      "C:/QAFactory/forge-repo/.claude/worktrees/td11-integration/ai-packages/qa-factory/scripts/tests/test_driver_layers.py (1-1429 and HEAD)",
      "C:/QAFactory/forge-repo/.claude/worktrees/td11-integration/ai-packages/qa-factory/scripts/tests/fixtures/driver-layers.json (diff and lines 1-6)",
      "C:/QAFactory/forge-repo/docs/tasks/specs/td-11b-source-maps.md 40-174 and E1-E12",
      "C:/QAFactory/forge-repo/docs/tasks/specs/td-11-lead-brief.md 195-255",
      "C:/QAFactory/forge-repo/docs/tasks/specs/reviews/t-045-td11-t1-p0a-code.md (M8, m5, m6)",
      "C:/QAFactory/forge-repo/docs/tasks/critic-diff-brief.md",
      "C:/QAFactory/forge-repo/docs/TESTING.md 86-110",
      "harness.py 47-73, scenario_walk.py 835-859, driver_golden.py 95-114, source_split.py 118-125/743-771/1244-1259, module_facade.install docstring, SIBLING_MAP axes 6 and 18"
    ],
    "reruns": [
      {"command": "python -B <wt>/ai-packages/qa-factory/scripts/tests/test_driver_layers.py", "result": "=== test_driver_layers: 195/195 ok ===, 195 PASS, 0 FAIL, exit 0"},
      {"command": "stdin probe battery against analyse() on temp roots", "result": "mixins equal-rank cycle passes L6/L12; three install aliases with installed false pass L11; importlib upward passes L6; BOM and syntax-error importer files pass L11; duplicate layer stem passes L10; facade tests/harness raises KeyError; literal outside importers, wrong install order, double install, string names and a facade-defined moved name are caught"},
      {"command": "real_maps() with FIXTURES redirected to a temp copy plus broken maps", "result": "invalid JSON FAIL, broken prefix FAIL L10, driver map 12 PASS, controller_layers.json not discovered"},
      {"command": "pin against live map comparison", "result": "pin 14, map 8 (HEAD 13); 6 slack rows"},
      {"command": "case-insensitive search for outside driver part importers in scripts/*.py", "result": "only story_step.py:889 outside the family; positive control story_run.py:71,1935 found"}
    ]
  }
}
```
