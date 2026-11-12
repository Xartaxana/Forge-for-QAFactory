# t-045 — critic gate: TD-11 T-1 (tools/source_split.py) and P0-A (harness.driver_sources, layer test)

Reviewed against: spec `docs/tasks/specs/td-11a-driver-split.md` §2, §3, §4, §6, overridden by `td-11-lead-brief.md` «Сведение спек» and «Правки после критика на план»; standing brief `docs/tasks/critic-diff-brief.md`. Uncommitted trees: T-1 `.claude/worktrees/agent-a72b9f65526f4b5b4` (HEAD 81e33d7), P0-A `.claude/worktrees/agent-afda5f776328dd89b` (HEAD 81e33d7).

## Verdicts (input to the Lead's acceptance, not the acceptance itself)

- **T-1: NEEDS WORK (ACCEPT WITH FIXES; B1-B4 block the merge).** On the real input the moved code is correct: I ran a cut in a temp repo with every free name resolved (byte check and pyflakes, below). But three of the seven proofs can never pass on `story_run.py`, P7 cannot fail, and I built four inputs where every proof is green and behaviour changes. The tool is not yet the witness the P1-2 cut is meant to rest on.
- **P0-A: ACCEPT WITH FIXES (M8 fix before merge; m6 is a spec defect for the Lead).**

**Can it move code wrongly while every proof stays green? Yes, shown on 4 inputs** (A, B, C, E under M1-M3). None of them occurs in today's `story_run.py` (my own AST scan: no `global`/`nonlocal`, no nameless module statement, no `self.__x`, no import name re-bound by a module definition). Spec B's files do have such forms (55 `global`/`nonlocal` in 40 scripts, spec A §3), so these are defects of the generic class mode, and T-2 would inherit them.

## Empirical layer (my runs; temp trees only, nothing written in the worktrees)

1. Control re-runs reproduced: selftest `selftest: 17 checks, 0 failed`. Real dry-run exit 2: six R4 (5 name-kind plus `KNOWN_PATTERN`), W1 x3, W2 :68, no R10/R11, `git status` afterwards shows only the 3 untracked files. P0-A `=== test_driver_layers: 58/58 ok ===`, with no `L8 informational` line.
2. **Temp cut (E3).** I copied `scripts/*.py`, used a P1-1-like map (the 5 F2 rehomes, 10 mixin rows, name-kind exceptions removed) and iterated R4 to zero. The sixth edge is a chain: `KNOWN_PATTERN`, then `RESUME_CLASSES` (:778), then `KNOWN_REFUSALS`, then `STRUCTURED_RE` (:150). The set that converged: `KNOWN_PATTERN`, `KNOWN_REFUSALS` and `STRUCTURED_RE` all go to driver_dispatch. Rehoming is a home judgment for the Lead (P1-1). Unpatched tool, dry-run: `PASS P1 segments: 963/963 equal` / `FAIL P2 census: 965 before, 961 after` / `FAIL P3 import failed ... manual-capture-steps.json cannot be read` / `FAIL P5 ... L8: ... state_census.py ...` / `result: a proof failed, nothing written, exit 2`.
3. In a scratch copy I applied two patches (P2 keyed by every name; `failed()` set to False) and then ran `--apply` in the temp repo. Results:
   - P2 `965 before, 965 after`.
   - The facade imports with `references/` present: `dir(story_run)` lost nothing (it gained 54 names), `dir(Driver)` is equal. MRO: `Driver, DriverMachine, DriverGates, DriverStages, DriverS0, DriverSources, DriverDispatch, DriverConductor, DriverDialog, DriverRunner, DriverCore, DriverChains, object`.
   - pyflakes over the original against the 11 written files: `before {} after {}`. Positive control on the harness: `['UnusedImport', 'UndefinedName']`.
   - `analyse(cut tree, map, tests_dir=real tests)`: `{}` (L1-L10 empty).
   - Line multiset: 21 045 non-blank original lines, 19 missing from the output. They are the 15 import lines 70-84 (regenerated, see m1), the class header, and the 3 W1 lines. No code line is lost or duplicated, and nothing has a CR.
   - K7 `residue` on the cut tree: `driver_dialog.py [421, 582]`, `driver_gates.py` 8 lines, `driver_machine.py` 12 lines. Before the cut it is `{}`.

## Findings — T-1

**B1 BLOCKER — P2 fails on the real tree (fails closed).** `source_split.py:1246` keys `gen_units[u.names[0]]`, and `:1264` takes `after_names` from those keys. A multi-target statement therefore loses every target after the first. The real tree has two: `EXIT_DONE, EXIT_ERROR, EXIT_PERSON, EXIT_GAVE_UP` (:86) and `PROBE_JUDGMENT_STATEMENT_LIMIT, PROBE_JUDGMENT_WHY_LIMIT` (:6848). Measured: 965 before, 961 after. Because `gen_units` is a dict and `after_names` a set, a name written into two parts also collapses, so "each name once" is not checked on the parts side. Fix: collect every name of every generated unit into a list and compare multisets. Add a selftest case: a same-home tuple assignment run through the proofs.

**B2 BLOCKER — P3 can never pass on story_run (fails closed).**
- `:1283` copies only `scripts_dir.glob("*.py")` into `tmp/before` and `tmp/after/scripts`.
- `grammar.py:197` reads `Path(__file__).resolve().parents[1] / "references" / "manual-capture-steps.json"` at import, so both imports fail.
- The two trees also have different depths (`before` is one level, `after/scripts` two).
- A directory named `*.py` makes `copyfile` raise an uncaught PermissionError (exit 1 with a traceback, not `Cannot`).

Fix: copy the whole package root (or junction `references/`) into identical `before/<pkg>` and `after/<pkg>` layouts, and catch OSError as a Cannot line.

**B3 BLOCKER — P5 can never pass on the real tree.** `:1308` calls `analyse(root_after, mp)` without `tests_dir`. `root_after` has no `scripts/tests`, so L8 reports the `state_census.py` rows. I reproduced this on the uncut tree too, so the failure comes from the layout, not from the cut. Fix: pass `tests_dir=pkg / cfg["tests_dir"]`. With that argument the cut tree gives `{}` (E3).

**B4 BLOCKER — P7 cannot fail, and the cut protocol absorbs whatever P7 should catch.** `:1319-1328` compares a baseline FILE before against the same file after. The tool never writes the lint/dup baselines or the census `ratchet` (the stored ceilings), so all three are equal by construction (the builder's Q2 says the same). In the cut commit the integrator then runs `lint_ratchet --update` and `dup_ratchet --update`, which would absorb any new pyflakes `UndefinedName` from a resolution miss. Answer to Q2, the fix:
- lint: pyflakes counts by class over the source before against the parts plus facade after. This is the cheap independent proof for M1-M3 in function bodies.
- dup: the number of dup groups computed on both trees.
- census: the COUNTS `test_judgment_census.analyse` computes on both trees (class counts and `blocking_per_role`), not the ceilings.

Spec defect for the Lead: fix item 4 («сравнивает весь объект `ratchet`») names the stored object, which is vacuous here.

**M1 MAJOR — `global` across homes: every proof green, NameError at run time (input A).**
- `_walk_tables` (:226) drops names that are assigned, so `global COUNTER; COUNTER += 1` in a part gets no import. Re-binding a module global from another module cannot be expressed anyway.
- Input A: `COUNTER` homed in core, `bump` (with `global COUNTER`) in dialog.
- Tool result: P1-P7 all PASS, `result: applied, exit 0`.
- Behaviour: before `read after bump = 1`, after `NameError: name 'COUNTER' is not defined`.

Fix: a new refusal for a `global`/`nonlocal` in a moved segment that names a module name homed elsewhere (or any `global` in moved code).

**M2 MAJOR — a module statement with no name stays in the facade silently, and import-time order changes (input B). This is an R10 gap.** `_targets` returns `[]` for `X[k] = v` or `obj.a = v`. The statement becomes a nameless `Unit` (:284-286), not a stray, so R10 never sees it and it stays in the facade (`moves False`).
- Input B: `TABLE = {"a": 1}; TABLE["b"] = 2; KEYS = sorted(TABLE)`.
- Tool result: all proofs PASS, applied.
- Behaviour: `KEYS` was `['a', 'b']` and became `['a']`.

The same gap exists at class level (:316). Fix: an Assign/AnnAssign with zero Name targets goes to `sc.strays` (R10 unless `module_statements` places it).

**M3 MAJOR — wrong module of equal name; name mangling (inputs E, C).**
- Input E: `bound` takes precedence over census names (:699, :786), so a module `def join` that re-binds `from os.path import join` makes the dialog part import `os.path.join`. Behaviour: `j = local` became `j = a\b`, with all proofs PASS. Fix: when a name is both import-bound and a census name, the census name wins (source order), or refuse it.
- Input C: `self.__x` written in one mixin and read in another becomes `_DriverCore__x` / `_DriverDialog__x`. With the attribute row L3 asks for, all proofs PASS and the read gives `AttributeError: ... '_DriverDialog__x'`. P3's `dir(Driver)` cannot see instance attributes. Fix: refuse any mangled name (`__x`, not a dunder) inside moved class code.

**M4 MAJOR — a failure midway leaves parts on disk; the re-run gives the wrong refusal and the wrong door.** I injected an OSError on the 2nd write (in-process):
- Run 1: `OSError ... driver_dialog.py` raised as a traceback (`main` catches only `Cannot`). On disk: `driver_core.py`, and `story_run.py` unchanged. Good: the facade is written last.
- Run 2: `R3 ... Driver.a is defined in the source and in the existing module driver_core.py; ... door: keep one row and one definition` (one line per name; on the real tree that is hundreds). The spec (§6) says R8 with "restore it, re-run". The R3 door would send someone to delete definitions.

Fix: write to temp files and `os.replace` them in order with the facade last, or roll back the written files on an exception. When the source still holds the names of a part that exists, refuse R8 and name the part files to remove. Carriers are written after the facade (:1402) without a re-read; a carrier changed since the plan is overwritten. Minor, but the same move.

**M5 MAJOR — R13 misses the patch form the suite uses most.** `:767` matches only `setattr(`/`patch.object(`. The suite assigns directly: `story_run.Driver.run_claude = ...` (`test_s7_investigation_replay.py:218-240`, `test_story_run_s7_live.py:140-142`). It also has string targets (`patch("story_run.Driver.m")`). The three W1 targets of today are patched in no form: my case-insensitive grep over `scripts/tests`, with a positive control of the same pattern in `driver-layers.json` (139, 365, 512), returned no hit. So there is no live miss now; controller has about 27 W1 sites. Fix: add `<alias>.<Class>.<m>\s*=[^=]`, `patch\(["'][\w.]*<Class>\.<m>["']`, `patch.multiple(`.

**M6 MAJOR — P6 cannot see a leftover.** Spec P6 has a second clause, "none left pointing at a name no longer in the old file", and it is not built: `bad6` (:1313) is only rows with no map row, and `:1314-1315` is a dead loop. A row the carrier regexes skip stays at `story_run.py` and P6 passes. Rows that would be skipped: a json object with a nested object (`\{[^{}]*\}`), a py-tuple split over lines, a guard key with spaces. Fix: after the pass, rescan each carrier for `<facade file>` plus a name of `moving` and fail on any hit. Related: `home_of` (:1066) tries the bare name before `<Class>.<name>`, so a module function with a member's name would take the row. There is no collision in today's map (checked); it is latent for controller.

**M7 MAJOR — a K7 residue that is not empty does not stop `--apply`.** The map has no `setup_import`, so three parts are flagged (WARNING lines). The cut would apply and leave `test_console_encoding` red, and the facade text is never K7-checked (it is built after the K7 loop, :1045). Fix: residue after the added lines, facade included, must be empty on `--apply` (a proof). P1-1 adds `setup_import`.

**m1 MINOR — bytes neither moved nor reported.**
- Regenerated import lines lose their prose comments: lines 70-84 carry the AR rationale (`# noqa: E402 (t-329: ...)`).
- Comments attached directly above an import or a preamble, the orphan of a preamble, and the orphan of the class docstring are dropped and not counted. `sc.dropped` counts only orphans of imports, and its label "(before imports)" is wrong.
- Two statements on one line (`A = 1; B = 2`) are copied whole into both homes.

story_run has none of the dropped shapes except lines 70-84.

**m2 MINOR — spec deviation, not named in the report as one.** The facade no longer keeps the import block (spec §2.4 "UNCHANGED"): it keeps only the names facade code uses. `story_run.waiver`, `.time` and `.hooklib` then exist only if `module_facade.install` forwards the names a part imports. P3 covers this once B2 is fixed; confirm the seam with B0. The facade also imports `driver_timing` eagerly. It was lazy (:1935 and others) and is now installed into `story_run`, which gains `render`, `report`, `row`, `console` and `annotations`.

**m3 MINOR.**
- `module_statements` keyed by the first line (Q1) is ambiguous for two `if os.name == "nt":` blocks. Refuse a key two strays share, or key by `{statement, after: <previous census name>}`.
- A property setter pair would hit R3 with a wrong door.
- A dry-run with P3 NOT RUN still ends `would apply ..., exit 0`, and on `--apply` the message says "a proof failed" where it should say "P3 not run" (Q3: the refusal itself works).

**m4 MINOR — tests (`docs/TESTING.md`, F1 (a)).** 17 checks over 1 588 lines. These have no case: `--homes` (code reading only), W2, the carrier pass (every form), P6/P7 failing, K7, R9-BOM, R10 class glue, multi-target units, a fixture that reads data at import (that case would have exposed B2). The selftest's clean fixture is why B1-B3 passed the DoD.

## Findings — P0-A

**M8 MAJOR — the L8 extension is dead by construction (fail-open).** `test_driver_layers.py` (the `enforced` line) counts a non-`story_run.py` name only when its text appears in the JSON of a `source_readers`/`source_mentions` row. Map rows never carry driver file names (the builder says so in "Edge 6"), so after the cut a new test pinning `driver_dispatch.py` text prints "informational" and stays green: the case L8 exists for. Today the rule buys nothing: the builder's run and mine print no informational line. Grep over `scripts/tests/*.py` for `driver_(chains|timing)\.py`: 3 hits, all docstrings or comments. Fix: enforce every driver-set name now and drop `l8_extra`. If the dispatch's edge asked for this temporal rule, that edge is a dispatch defect.

**m5 MINOR.** `driver_sources(root=tmp)` with `exempt=None` reads the REAL map's `not_driver`. A stale `not_driver` row naming a homed part would drop it from `driver_text()`. L1 of the layer test turns that red, so it is guarded indirectly, but `driver_sources` could refuse an exempt stem that is a home in `layers`. The `l8_extra` key and its printer go away with M8.

**m6 MINOR (spec defect, implemented as written).** `Scan` accepts any `^Driver[A-Za-z0-9]*$` name as the assembled class. Probe: `DriverTypo.low` gives L3 `[]`; the control `DriverTypo.nope` is reported, but as "reads `Driver.nope`". `DriverCore.role_words` (role_words is homed in dialog) passes too, and fails at run time. Tighten: `<Mixin>.<m>` resolves only when Mixin is `Driver` or `camel(home of Driver.<m>)`.

## Answers to the dispatch questions (short)

1. **Segments.** P1 is computed on independent slices: the source with W1 applied, against a fresh `scan_text` of the generated file. It can fail. P2 is a list comparison but is broken (B1). Decorators, attached comments, glue :7195/:7197/:21049 (each one consecutive slice), descriptors, multi-line strings and backslashes are handled by `end_lineno`. The last member and the text after the class are covered: the class tail before `main` becomes `main`'s orphan, and there is no trailing text. Bytes lost: m1.
2. **Free names.** On the real tree the resolution is pyflakes-clean in both directions (no UndefinedName, no UnusedImport). Holes: `global` (M1), import vs definition (M3), `from __future__` is not carried into parts (story_run has none), star imports go to R5 and `try/except ImportError` / `TYPE_CHECKING` go to R10 (both loud).
3. **Refusals.** The R10 gap (M2). The R13 forms (M5). R4/R6 rank logic traced correct. R7 covers class-scope defaults and decorators. R10 on story_run: my scan of the module statements finds only the `Expr` at :68 (the preamble) and the `If` at :22170 (`__main__`), so "no R10" is correct. `hooklib.py:19-23` is family mode and was not run. No refusal path writes a package file; `--report FILE` writes the report by design.
4. **Atomicity:** M4. **Line endings:** every carrier file and story_run are `i/lf w/lf attr/text=auto eol=lf`; the output had no CR.
5. **Facade:** checked in the generated text (literal imports, `install` in rank order, from-imports, bases, docstring kept). Notes: m2, m3.
6. **Carriers:** counts match spec §3 (gate-registry 4, null-outcomes 4, block-names 7, NO_MOVE_BASELINE 47, census 20, test-layers 59, plus the new row 23). P6: M6. The builder's finding 1 is confirmed: the layer test does not see a module name reading another module name, and the chain is longer than one edge (E3). Finding 2: rows for the mixin classes are needed, or L1 is red after the cut. That is P1-1's job, and my E3 run agrees once they are added.
7. **AR-1:** the claim holds. Case-insensitive `story_run|driver_` over the tool gives 0 hits; the same pattern over the carriers file gives 2.
8. **P0-A:** M8, m5, m6.
9. **DUPLICATION AND CONSISTENCY:** F6 (a) asked for the cross-check of the tool's census count with `test_driver_layers.definitions`, and it is missing (grep `definitions|cross` in the tool: none). P5 only checks the after-tree indirectly. Queue it, or add the count comparison. `_seg_start`/`_targets`/`_kind_of` mirror `test_driver_layers` (queued by F6). **CODE QUALITY:** NEW functions over 60 lines: `_census_and_rows` 504-611, `from_generation` 653-760, `run_proofs` 1234-1329, `_carrier_pass` 1057-1130, `_facade_bound` 778-841, `build_facade` 925-986. Dead code: 1047-1049, 1314-1315, `glue_rest_users` (set at :332, never read), `Scan.warnings`. An uncaught OSError ends in a traceback. Severity: fix with B1-B4 (same functions), not blocking on its own.
10. **ARCHITECTURE:** AR-13/14/20/22 are named by the spec. AR-20 is defeated by B4 as built.
11. **JUDGMENT:** none; every check is shape/data. Home choice stays a map judgment, and R1's door says so.
12. **ONE ROAD:** none found. The tool reads every name from data. `--homes` is a second road for one commit but F8 is closed; m4 notes it is untested.

## Not checked

- Family/function and test-file modes (T-2, T-3).
- The real `module_facade.install` (absent; I used the selftest's stand-in).
- `hooklib.py` R10 behaviour.
- The carrier pass written onto real carriers and their verification commands (`test_gate_registry`, `waiver.load_block_names`, `test_audit_rules`, `test_bug_records`).
- `--homes` multi-run.
- The dup baseline effect.
- Slow test files and selftest.py (not run, per the dispatch).
- The P0-A dispatch's exact edge 6 wording (I read only the builder's paraphrase).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "T-1 B1 source_split.py:1246,1264 P2 keys generated units by the first name only: real tree 965 before / 961 after (multi-target :86, :6848), a duplicate across parts is invisible",
    "T-1 B2 source_split.py:1283 P3 copies only scripts/*.py with asymmetric depth: grammar.py:197 reads references/ at import, P3 can never pass on story_run",
    "T-1 B3 source_split.py:1308 P5 calls analyse without tests_dir: L8 fails on the layout, P5 can never pass on the real tree",
    "T-1 B4 source_split.py:1319-1328 P7 compares unchanged baseline files (equal by construction) while the cut commit runs lint/dup --update: must compare pyflakes counts, dup groups and census counts computed on both trees"
  ],
  "fixes": [
    "B1-B4 as in blockers (block the merge)",
    "M1 refuse global/nonlocal in moved code naming a module name homed elsewhere (input A: all proofs green, NameError)",
    "M2 nameless Assign (subscript/attribute target) at module or class level goes to strays/R10 (input B: KEYS changed, all proofs green)",
    "M3 census name wins over an import of the same name or refuse; refuse mangled __x in moved class code (inputs E, C)",
    "M4 atomic apply (temp + os.replace, facade last, or rollback); re-run after a partial apply refuses R8 naming the part files, not R3 per name",
    "M5 R13 also matches direct assignment alias.Class.m = and patch string targets and patch.multiple",
    "M6 P6 rescans each carrier for the facade file plus a moved name after the pass; home_of tries Class.name before the bare name",
    "M7 K7 residue after the added lines, facade included, must be empty on --apply",
    "M8 P0-A: enforce L8 on every driver-set file name now, drop the temporal rule and l8_extra",
    "m1-m6, the F6 cross-check, functions over 60 lines and the dead code at 1047-1049, 1314-1315 and glue_rest_users: fix with the same round or queue",
    "Lead/spec: fix item 4 (compare the stored ratchet) is vacuous; Scan acceptance of any Driver* name should resolve the exact mixin; P1-1 must rehome the KNOWN_PATTERN/RESUME_CLASSES/KNOWN_REFUSALS/STRUCTURED_RE chain and add 10 mixin rows and setup_import"
  ],
  "class_completeness": "Surface = the mover's semantic proofs. Neighbour classes walked by experiment: global (A), nameless statements (B), name mangling (C), shadowed import (E), partial write (M4), patch forms (M5), leftover carrier rows (M6). All four fixture classes pass every proof today, so the class fix is a refusal per form plus an independent lint proof (B4). Siblings: spec B family mode (T-2) inherits all of them, so they must be fixed in class mode before T-2. P0-A: the L8 extension and the Scan acceptance are two guards that pass too much.",
  "trail": {
    "read": [
      "tools/source_split.py (whole, T-1 worktree)",
      "tools/source-split-carriers.json",
      "docs/tasks/specs/reports/t-036-td11-T-1.md",
      "docs/tasks/specs/reports/t-037-td11-P0-A.md",
      "P0-A diff harness.py and test_driver_layers.py",
      "docs/tasks/specs/td-11a-driver-split.md",
      "docs/tasks/specs/td-11-lead-brief.md",
      "docs/tasks/critic-diff-brief.md",
      "story_run.py 48-90, 7186-7200, 21044-21056 and an AST scan of all module and class statements",
      "driver-layers.json rows",
      "audit_factory.py 1629-1679",
      "judgment-census.json ratchet; test_judgment_census.py 58-74",
      "grammar.py:197",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "python -B tools/source_split.py --selftest (T-1 worktree)", "result": "selftest: 17 checks, 0 failed"},
      {"command": "python -B tools/source_split.py --map driver-layers.json --source scripts/story_run.py --class Driver --dry-run --repo <T-1 worktree>", "result": "exit 2, 6 R4 (5 name-kind + KNOWN_PATTERN), W1 x3, W2 :68, no R10/R11; git status clean apart from the 3 untracked files"},
      {"command": "same dry-run in a temp repo with a P1-1-like map (iterated R4 to zero)", "result": "P1 963/963 PASS; P2 965/961 FAIL; P3 FAIL manual-capture-steps.json; P5 FAIL L8 state_census.py; exit 2"},
      {"command": "scratch copy (P2 keyed by every name, failed() False) --apply in the temp repo, then import, pyflakes, analyse with tests_dir, line multiset, K7 residue", "result": "import ok, dir(module) lost nothing, dir(Driver) equal; pyflakes before {} after {} (control UndefinedName found); analyse {}; 19 lines missing = imports 70-84, class header, 3 W1; K7 flags 3 parts"},
      {"command": "fixture cut A/B/C/E with the unpatched tool --apply", "result": "all proofs PASS and applied; behaviour changed: NameError COUNTER; KEYS [a,b] became [a]; AttributeError _DriverDialog__x; join local became os.path"},
      {"command": "injected OSError on the 2nd write, then re-run dry-run", "result": "traceback, driver_core.py left on disk, story_run unchanged; re-run R3 per name with door keep one row and one definition"},
      {"command": "python -B scripts/tests/test_driver_layers.py (P0-A worktree)", "result": "=== test_driver_layers: 58/58 ok ===, no L8 informational line"},
      {"command": "problems_of probe in the P0-A layer test: DriverTypo.low vs DriverTypo.nope", "result": "[] vs L3 reported as Driver.nope"},
      {"command": "grep -i story_run|driver_ over tools/source_split.py, control over the carriers json", "result": "0 hits / 2 hits"}
    ]
  }
}
```
