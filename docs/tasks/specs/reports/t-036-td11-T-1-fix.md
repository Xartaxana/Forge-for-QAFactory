# t-036 attempt 2 (fix round) - TD-11 T-1, tools/source_split.py class mode

Changed (in place, uncommitted): `tools/source_split.py` (rewritten around the critic's list; no function over 60 lines, checked by an `ast` scan: none), `tools/source-split-carriers.json` (key `ratchets` replaced by `census_test`: file/entry/data of the census test; P7 no longer reads stored baselines). Nothing else touched. AR-1: `grep -c -i "story_run\|driver_"` over the tool prints 0.

## Per finding: fixed / how / selftest case (names as printed)

- B1 fixed. P2 is a multiset of EVERY name of every unit (all targets of a multi-target statement) over all parts plus the facade, against all source names; a name written twice on the parts side fails and is named. Cases: "B1 a same-home tuple assignment through the proofs: P1 and P2 pass", "B1 a name written twice on the parts side fails P2".
- B2 fixed. `_build_trees` copies the whole package root into `before/<pkg>` and `after/<pkg>` (identical layout), writes the generated files and carrier texts only into `after`; OSError/shutil.Error -> `Cannot`. Found while proving on the real tree: on Windows the deep fixture paths pass MAX_PATH, so the copy uses extended-length paths (`_long`) and the temp tree is removed the same way. Cases: "B2 a module that reads a sibling data directory at import passes P3 ...", "B2 an OSError during the tree copy is a Cannot line, not a traceback".
- B3 fixed. P5 calls `analyse(after pkg, map, tests_dir=after pkg/tests_dir)`. Case: "B3 P5 passes tests_dir: a declared source mention in the package tests is found on the result tree".
- B4 fixed. P7 compares values COMPUTED on both trees: pyflakes counts by message class (source before vs parts+facade after), dup groups by `dup_ratchet.analyse_scopes` (every scope that has files in the tree), `test_judgment_census.analyse` totals (`counts`, `blocking_per_role`; census data read from each tree, the after tree carries the carrier-rewritten census json). Any growth fails. pyflakes/dup_ratchet/census function not importable or not runnable -> P7 NOT RUN, `--apply` refuses naming it. A tree without the census data file: the census part is reported "census absent in this tree", the rest still decides. Cases: "B4 P7 fails when a part gains a pyflakes finding (undefined name)", "B4 pyflakes not importable: P7 NOT RUN and --apply refuses naming it".
- M1 fixed (new refusal R14): `global X` in any unit (moved or staying) where X is a census name homed elsewhere than the unit. Cases: "R14 M1 input A ...", "M1 `global` of a name of the same home is not refused".
- M2 fixed: an Assign/AnnAssign with a non-Name target (anywhere in the targets) is a stray at module level (R10 unless `module_statements` places it; the placed statement moves between its names in source order); at class level it is an unattached class-body statement (R10, own text). Cases: "R10 M2 input B ...", "M2 the statement placed by module_statements moves between its names, every proof passes".
- M3 fixed. (a) new R15: a name both import-bound and defined at module level; (b) new R16: any mangled identifier (`__x`, not a dunder: attribute, name, def/class name, argument, keyword) in class code when any class unit moves. Cases: "R15 M3 input E ...", "R16 M3 input C ...".
- M4 fixed. `write_all` writes every file to `<name>.tmp<pid>` beside the target, then `os.replace`s parts (rank order), the facade, then the carriers; any OSError rolls back what was replaced/created and raises `WriteFailed` -> `Cannot` line, exit 2, no traceback. A carrier whose sha256 differs from the one read by the plan is refused. A re-run over part files that still define names the source holds: ONE R8 naming all part files to remove (door "remove ... and re-run"), no R3 per name, and the generic "module is not what the map homes" R8 is skipped for them. Cases: "M4 an OSError on the 2nd replace ... rolled back", "M4 a carrier changed between the plan and the write is refused, nothing written", "M4 a re-run over leftover parts: ONE R8 ...".
- M5 fixed: R13 also matches `alias.<Class>.<m> =` (not `==`), `patch("...<Class>.<m>")`, `patch.multiple(<...Class...>, ..., <m>=`. Cases: "R13 M5 a direct assignment ...", "R13 M5 a patch string target ...", "R13 M5 patch.multiple ...", "M5 a comparison is not a patch: no R13".
- M6 fixed. `_home_of` tries `<Class>.<name>` before the bare name (module-level function so it is testable); the dead loop is gone; P6 second clause `_leftovers`: every present tool carrier is rescanned for the facade file (or `"<facade>:`) with a moved name in the same record (the physical line; for json, the enclosing object only where the file name is the VALUE of a key); a hit fails P6. Cases: "M6 P6 fails when a row the regex skips ...", "M6 home_of tries ...", "carrier pass: unmoved rows stay, P6 passes with every carrier rescanned", "a tree with no carrier files: P6 reports 0 carriers rescanned and passes".
- M7 fixed. New proof P8: K7 residue after the added lines, on every part AND the facade (computed on the final texts, before the first write); non-empty -> P8 FAIL (dry-run reports it as it will fail); K7 not evaluable -> NOT RUN. Cases: "M7 a K7 residue with no setup_import fails P8 and names the part", "M7 with setup_import the added import clears the residue: P8 passes".
- m1 fixed: an import line kept whole is copied verbatim from its first attached comment line to its last line; every other comment line no generated file carries (orphans of imports/preambles/docstrings, attached comments and inline comments of regenerated or dropped imports, trailing comments) is listed by source line number and counted, label corrected ("dropped comment lines (no generated file carries them)"); two statements on one physical line -> R10. Cases: "m1 an import line kept whole stays verbatim with its comment", "m1/m2 a line of which the facade uses only some names is regenerated; its comment is listed as dropped", "m1 every dropped comment line is listed ...", "R10 R10 two statements on one physical line".
- m2 fixed (deviation from spec 2.4, accepted by the Lead): the facade keeps only the import names its own code uses; an existing module is imported/installed by the facade only if the source imports it at module level (or this run writes it). A WARNING lists an import dropped from the facade that no segment uses either (side effects). Cases: "m2 the facade imports only the names its own code uses ...", "m2 a module the source imports lazily is not imported eagerly ...".
- m3 fixed: a `module_statements` key shared by two strays -> R10 naming both lines; dry-run with P3/P7 not run ends `result: would apply (P3 not run) (dry-run writes nothing), exit 0`, `--apply` ends `result: P3 not run, so --apply refuses, nothing written, exit 2` (a failed proof says `a proof failed (P5, ...)`); a property getter/setter pair is one unit. Cases: "R10 m3 a module_statements key shared ...", "m3 P3 not run: ...", "m3 a property getter/setter pair of one name is one unit, not an R3".
- Item 15 fixed: dead code removed (1047-1049, 1314-1315, `glue_rest_users`, `Scan.warnings`); `run_proofs`, `_carrier_pass`, `from_generation`, `_census_and_rows`, `_facade_bound`, `build_facade`, `build_texts`, `report`, `selftest` split (Resolver class, per-form carrier functions, per-proof functions); largest function now under 60 lines.
- Item 16: all cases above plus "W2 ...", "--homes ...", "R9 a source with a BOM", each carrier form (json-file-function, guard, reader, py-tuple, covers-append). Not separately covered: the census-json carrier (same form as gate-registry), the lint/dup/census growth of the P7 census part on a tree that HAS the census data (only the pyflakes branch is exercised by a case).

## Witness 1: `python -B tools/source_split.py --selftest` (exit 0; the clean fixture's own report is printed first, then the cases)
```
PASS R1 a name with no row: reported by name ('extra')
PASS R2 a row whose name is gone: reported by name ('ghost')
PASS R3 a name defined twice: reported by name ('helper')
PASS R4 a free name of a higher home: reported by name ('LABEL')
PASS R5 a free name that resolves to nothing: reported by name ('mystery')
PASS R6 a same-rank import cycle: reported by name ('->')
PASS R7 a class-body use of a name homed elsewhere: reported by name ('SIZE')
PASS R8 a target module half-written: reported by name ('driver_core.py')
PASS R9 mixed newlines: reported by name ('newline')
PASS R9 non-UTF-8 source: reported by name ('UTF-8')
PASS R9 a source with a BOM: reported by name ('byte order mark')
PASS R9 non-ASCII generated text: reported by name ('ASCII')
PASS R10 a module-level statement with no place: reported by name ('print')
PASS R11 targets of one statement in different homes: reported by name ('PA')
PASS R12 a free name of facade code: reported by name ('mystery')
PASS R13 setattr of a rewritten member on the assembled class: reported by name ('SIZE')
PASS R13 M5 a direct assignment of a rewritten member on the assembled class: reported by name ('SIZE')
PASS R13 M5 a patch string target of a rewritten member on the assembled class: reported by name ('SIZE')
PASS R13 M5 patch.multiple of a rewritten member on the assembled class: reported by name ('SIZE')
PASS M5 a comparison is not a patch: no R13
PASS R14 M1 input A: `global` of a name homed in another module: reported by name ('COUNTER')
PASS M1 `global` of a name of the same home is not refused
PASS R10 M2 input B: a module statement with no name target: reported by name ('TABLE["b"] = 2')
PASS M2 the statement placed by module_statements moves between its names, every proof passes
PASS R15 M3 input E: a name both imported and defined at module level: reported by name ('join')
PASS R16 M3 input C: a mangled attribute in cut class code: reported by name ('__x')
PASS R10 R10 two statements on one physical line: reported by name ('two statements on one line')
PASS R10 m3 a module_statements key shared by two statements: reported by name ('places the statements')
PASS M4 a re-run over leftover parts: ONE R8 naming the part files to remove, no R3 per name
PASS clean fixture: dry-run exit 0, proofs P1-P8 pass, nothing written
PASS apply writes the parts; the re-run says nothing to do (exit 0)
PASS B1 a same-home tuple assignment through the proofs: P1 and P2 pass
PASS B1 a name written twice on the parts side fails P2
PASS B2 a module that reads a sibling data directory at import passes P3 (whole package root in both trees)
PASS B2 an OSError during the tree copy is a Cannot line, not a traceback
PASS B3 P5 passes tests_dir: a declared source mention in the package tests is found on the result tree
PASS B4 P7 fails when a part gains a pyflakes finding (undefined name)
PASS B4 pyflakes not importable: P7 NOT RUN and --apply refuses naming it
PASS M7 a K7 residue with no setup_import fails P8 and names the part
PASS M7 with setup_import the added import clears the residue: P8 passes
PASS carrier form of gate-registry.json: the moved row is rewritten ("file": "driver_core.py")
PASS carrier form of null-outcomes.json: the moved row is rewritten ("driver_core.py::helper")
PASS carrier form of block-names.json: the moved row is rewritten ("driver_dialog:DriverDialog.top")
PASS carrier form of audit_factory.py: the moved row is rewritten (("driver_core.py", "DriverCore.low"))
PASS carrier form of test-layers.json: the moved row is rewritten ("driver_core.py")
PASS carrier pass: unmoved rows stay, P6 passes with every carrier rescanned
PASS M6 P6 fails when a row the regex skips still names the facade file with a moved name
PASS M6 home_of tries `<Class>.<name>` before the bare name
PASS a tree with no carrier files: P6 reports 0 carriers rescanned and passes
PASS M4 an OSError on the 2nd replace: exit 2, a Cannot line, the tree is exactly as before (rolled back)
PASS M4 a carrier changed between the plan and the write is refused, nothing written
PASS m3 P3 not run: the dry-run ends `would apply (P3 not run)`, --apply names it and writes nothing
PASS W2 the facade's path preamble is rewritten to the expression of the moved name
PASS --homes: only the selected home is written, the rest stays in the facade, P1-P4 pass (P5 is red by design: the map still homes the unwritten mixin)
PASS m1 an import line kept whole stays verbatim with its comment
PASS m1/m2 a line of which the facade uses only some names is regenerated; its comment is listed as dropped
PASS m1 every dropped comment line is listed by source line number and counted; the label is not `(before imports)`
PASS m2 the facade imports only the names its own code uses (json lives in the part only)
PASS m2 a module the source imports lazily is not imported eagerly by the facade nor installed as a part
PASS m3 a property getter/setter pair of one name is one unit, not an R3
selftest: 60 checks, 0 failed
```

## Witness 2: the real-tree dry-run (the map is the real one at `ai-packages/qa-factory/scripts/tests/fixtures/driver-layers.json`; the bare `driver-layers.json` of the dispatch resolves to no file from any cwd, so I gave its path) - exit 2
Command: `python -B WT/tools/source_split.py --map WT/ai-packages/qa-factory/scripts/tests/fixtures/driver-layers.json --source scripts/story_run.py --class Driver --dry-run --repo WT`
```
dropped comment lines (no generated file carries them): 15
refusals: 6
  R4 scripts/story_run.py:1089: Driver.__init__ ... uses `UNTIL_PAST` (home driver_machine, rank 8) ... (a name-kind row of `exceptions`)
  R4 scripts/story_run.py:2309: Driver.continuation_note ... uses `HANDOFF_FORM` (home driver_dispatch, rank 4) ...
  R4 scripts/story_run.py:2601: Driver.s1_person ... uses `S1_GAP_RE` (home driver_sources, rank 5) ...
  R4 scripts/story_run.py:2601: Driver.s1_person ... uses `S1_REVIEW_RE` (home driver_sources, rank 5) ...
  R4 scripts/story_run.py:3159: Driver.finish ... uses `WINDOW_ROUND_STAGES` (home driver_machine, rank 8) ...
  R4 scripts/story_run.py:772: KNOWN_PATTERN (home driver_dispatch, rank 4) uses `KNOWN_REFUSALS` (home driver_machine, rank 8), a higher layer
  W1 scripts/story_run.py:2935 Driver.role_words -> DriverDialog.role_words (in Driver.stuck_facts)
  W1 scripts/story_run.py:10778 Driver.stage_repair_owed -> DriverStages.stage_repair_owed (in Driver.s4_repair_owed)
  W1 scripts/story_run.py:11549 Driver.CUT -> DriverCore.CUT (in Driver.probe_reason)
  W2 scripts/story_run.py:68 preamble `sys.path.insert(0, str(HERE))` -> `sys.path.insert(0, str(Path(__file__).resolve().parent))` (facade)
result: refused (6 refusals), nothing written, exit 2
```
(no R10/R11/R14/R15/R16 on the real tree.) `git -C WT status --porcelain`: `?? docs/tasks/specs/reports/t-036-td11-T-1.md`, `?? tools/source-split-carriers.json`, `?? tools/source_split.py` (the new report file of this round is the fourth untracked path).

## Extra proof: the proofs run on the real story_run with a P1-1-like map (temp repo copy, nothing written in WT)
Map: the 5 name-kind exceptions removed, the used names rehomed down iteratively (3 rounds: the critic's chain), 10 mixin rows, `setup_import: hooklib`. Dry-run:
```
refusals: 0
PASS P1 segments: 963/963 equal
PASS P2 census (multiset of every name): 965 before, 965 after, each name once: True
NOT RUN P3 not run: the facade module module_facade.py is not in the tree
PASS P4 compile of 11 files: ok
FAIL P5 layer test on the result tree: {'L8': ['the map has a row for test_bug_records.py in `<module>` but that function holds no literal story_run.py: delete the row.']}
PASS P6 carrier pass: 86 carrier lines, 7 carriers rescanned, unresolved or left behind 0
FAIL P7 computed on both trees: pyflakes 0->4, dup groups 9->9, census counts 939=939; GREW: ['pyflakes RedefinedWhileUnused: 0 -> 1', 'pyflakes UnusedImport: 0 -> 3']
PASS P8 K7 residue after the added lines (parts and facade): empty
result: a proof failed (P5, P7), nothing written, exit 2
```
B1 (965=965), B3 (P5 now judges the real tests dir) and B2's tree copy are confirmed on the real tree; P3 stays NOT RUN until `module_facade.py` lands (temporal: absent -> NOT RUN and `--apply` refuses; present -> the real one is used; the stand-in exists only in selftest fixtures and its PASS line says `[stand-in module_facade]`).

## Findings returned (not decided)
1. P5 on the real cut: L8 fails because the carrier pass rewrites the `('story_run.py', ...)` literals of `test_bug_records.py` (row 23, by design) while the map still declares a `source_mentions`/`source_readers` row for that file whose count of the literal `story_run.py` is now lower. P1-1 / the node that edits `driver-layers.json` must lower or delete that row in the same commit; the tool cannot (it never edits the map). Question: should the carrier pass also report which map rows pin a literal in a carrier it rewrites?
2. P7 vs the K7 setup import: pyflakes does not honour `# noqa`, so every `import hooklib  # noqa: F401 (console setup, K7)` line the tool adds is an UnusedImport (3 parts: dialog, gates, machine; gates also gets a RedefinedWhileUnused against a source import of the same module at line 658). With a `setup_import` in the map "any growth fails" can never pass on the real cut. Options for the Lead: (a) P7 exempts the lines the tool itself adds for K7; (b) the setup import is written so pyflakes sees a use; (c) the integrator accepts the growth. Left as fail-closed.
3. Dispatch edge "P3 with the module absent uses the stand-in exactly as now" reads against item 14 ("P3 not run" is a state) and against the code as it was: I kept "absent -> NOT RUN; present -> real one; the stand-in exists only in the selftest fixtures". Say if a stand-in should live in the tool.
4. Class-level strays: spec item 6 says "unless `module_statements` places it"; the key is module-level (first line of a module statement), so a class-level nameless assignment is always R10 here. Say if class-level placement is wanted.
5. m2 drops import lines no segment uses (side-effect imports included); the tool lists such drops as a WARNING per import and in the dropped-comments list, but P3 cannot see a side effect.

## Left undone
Nothing of B1-B4, M1-M7, m1-m4, item 15. Not done by design: M8, m5, m6 (not mine), the census-count cross-check against `test_driver_layers.definitions` (queued to T-2), family/function and test-file modes.

## Analogs noticed
- `test_driver_layers` L8 reads `tests/*.py` top-level only, and its literal is hard-coded (`story_run.py`); same shape as the carrier literal in finding 1.
- Windows MAX_PATH: `shutil.copytree` of the package into any temp tree fails on the deep fixtures (`fixtures/stories/.../CART-1_TC_011/a8/...`); any other tool or test that copies the package tree (e.g. install smoke on this machine) has the same exposure.
- `_walk_tables` still drops assigned names: a `nonlocal` is not refused (it can only name an enclosing function variable inside one unit, so it cannot cross homes).

## Needed beyond the manifest
`tools/dup_ratchet.py`, `tools/lint_ratchet.py` (what P7 computes), `ai-packages/qa-factory/scripts/tests/test_judgment_census.py` (analyse signature, totals), `test_console_encoding.py` (K7 entry), `test_driver_layers.py` L8 (selftest B3 fixture), the real `driver-layers.json` for the temp-repo experiment.
