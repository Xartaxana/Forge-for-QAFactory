# t-071 TD-11 T-3: two defects of tools/test_split.py found by the N2 cut (parts run alone)

Worker: builder (fresh), in place in WT = `C:\QAFactory\forge-repo\.claude\worktrees\agent-af3a560c41c1247c7`. Not committed. No edit under any `ai-packages`; no `--apply` on a real tree (temp copies in `C:\Users\i_mas\AppData\Local\Temp\td11_t071\*`). Changed: `tools/test_split.py`, `tools/test_test_split.py`, this report. The scripts that built the temp trees and compared them (`regress.py`, `n2cut.py`) are in the session scratchpad, not committed.

## F1 - a part crashed alone on `import no_move`

Cause (tool): `header_text` (test_split.py, the old loop over `an.header`) kept an import only if one of its names was `used`, so `from story_run_common import driver_for, jsonl, seam_option, seed` vanished from a part that uses none of them; that import was the only thing that put the scripts directory on `sys.path` (story_run_common does `sys.path.insert(0, str(harness.SCRIPTS))`). Nothing in the proof imported a part.

Fix:
- Rule 1(b), `header_text(..., part, keep_path)` (called with `keep_path=True` from `gen_part` only): when the part imports any non-stdlib module (a kept import whose root is not in `sys.stdlib_module_names`, or the common import), every module-level import of the old file that is a LOCAL module of the tests dir (`<root>.py` beside the old test, found by `plan.tests_names`) and that the part uses no name of is kept as
  `import <module>  # noqa: E402` + `del <module>  # split: imported for its sys.path effect`, at its old position among the imports. `analyze` knows the marked `del` (category `keepdel`: header, not a segment), so (b)/(d) are unaffected. A kept line above that already loads the same module makes the extra import needless (it stays listed as dropped). A `test_*` file imported by the old file at module level is never kept; it is printed (`REPORTED:`). The common module and the shim do not get the rule (proof (g) is their net) - see the deviation list.
- pyflakes: no convention exists in the tree for a path-only import (searched `import X  # noqa: F401`: one hit, `clock_sitecustomize/sitecustomize.py`; `story_run_common` is imported bare nowhere at module level). Chosen: `import X` followed by `del X` - a use the tool can state; pyflakes 3.2.0 reports nothing on the generated parts (witness below, `pyflakes rc 0`).
- Dropped imports are never silent: the report prints `DROPPED IMPORT: <file> does not use line N: ...` (one entry per old line, names of a partly dropped `from` line joined), `KEPT FOR ITS sys.path EFFECT: <file> keeps ...`, and `REPORTED: <source>:N: ...` for a test file. Printed in dry-run and apply (function `report`).
- Proof (g), `import_failures` + `prove(..., imports=True)`: every part and the shim is imported in its own child (`python -B -c "import importlib, sys; sys.path[:0] = sys.argv[2:]; importlib.import_module(sys.argv[1])" <stem> <stage> <tests dir>`), cwd a fresh temp directory outside the repo, `PYTHONPATH` removed, `IMPORT_TIMEOUT = 120` s per file, exit 0 required, stderr tail (last 4 lines, 500 chars) quoted on failure, a timeout names the file. Run in `--dry-run` (on the in-memory would-be files, written to a temp stage) and in `--apply` on the re-read temp files, after all static proofs and before any rename; a failure raises the refusal and leaves the target as it was (test row asserts the snapshot).
- Test rows: `F1a import_proof_fails_when_a_part_lacks_the_import_that_makes_its_path` (1(a): the kept import tampered away -> `(g)` FAILED with `test_demo_a.py: exit 1` and `ModuleNotFoundError`; untouched files -> ok; timeout row; apply with a failing `import_failures` -> exit 2, tree unchanged), `F1b path_effect_import_kept_as_import_and_del_and_the_parts_run_alone` (1(b): text, order, both parts run alone `1/1`, pyflakes clean), `F1b dropped_imports_listed_and_a_test_file_import_reported_not_kept` (listing + REPORTED + no part keeps `test_other`), `F1 edge part_with_only_stdlib_imports_keeps_no_helper_import` (stdlib-only usage keeps none; non-part keeps none).

## F2 - two parts had no closing `harness.finish(...)`

Cause (tool): `render_runner` emits only the statements of `main` that belong to the part, and includes `main` only when the part holds a scenario `main` runs. A part whose scenarios come only from the `if __name__` block (k4s, c26_g27_f2) got the guard without the `main()` call and nothing carried the `finish` at the end of `main`.

Fix: `_has_finish` (does the part's runner already hold a closing?), `_closing_candidates` (own `finish` of a block, else those of the runner functions it calls), `pick_closing` and `_closing_text` (new, before `render_runner`; `render_runner` appends the closing at the end of the last emitted `if __name__` block, else runner function, label + part suffix, re-indented). When there is none to find, two different ones (compared by source text), or no guard/function to carry it: REFUSED with `<source>:<line>` (first included block) and the door = the new map key `closing` (an int: the line of a `finish("<label>")` statement of the source; documented in the module docstring and the map comment; validated in `build_plan`: a line that holds no such statement is refused, the lines that do are listed). Existing maps need no key (found automatically). Report line `CLOSING: <part>.py got the old runner's closing (line N: ...)`.
- Proof (f): each part's runner (classifier over the re-read part file) holds exactly one closing call - `(f) closing: each of N part runner(s) holds exactly one closing call (finish) -> ok`; FAILED names `<file> holds 0|2`.
- Test rows: `F2 closing_copied_into_every_part_and_each_part_runs_alone`, `F2 runner_without_any_closing_refused_with_file_line_and_door`, `F2 different_closings_refused_and_the_map_key_closing_decides` (also a bad `closing` line refused), `proof_f_each_runner_holds_exactly_one_closing_call` (0 and 2 closings fail the proof). The old row `dry_run_writes_nothing_and_prints_the_proof` has the keys of (f) and (g).

## Witness (verbatim)

```
$ python -m pytest C:\QAFactory\forge-repo\.claude\worktrees\agent-af3a560c41c1247c7\tools\test_test_split.py -q
...........................................                              [100%]
43 passed in 6.87s
```
(35 old + 8 new rows, all in the one parameterised table.)

N2 cut on a temp copy (`...\Temp\td11_t071\n2final`: N2WT's package, generated parts left out, old file = `git show HEAD:`; script `n2cut.py`), `--apply` with the N2 map:
```
CLOSING: test_no_move_seam_k4s.py got the old runner's closing (line 1402: harness.finish("no_move seam")), label with the part suffix; its own blocks hold none
CLOSING: test_no_move_seam_c26_g27_f2.py got the old runner's closing (line 1402: harness.finish("no_move seam")), label with the part suffix; its own blocks hold none
KEPT FOR ITS sys.path EFFECT: test_no_move_seam_k4s.py keeps (as `import <module>` + `del <module>`) line 19: `from story_run_common import driver_for, jsonl, seam_option, seed # noqa: E402`
(a) check call sites ...: source 378, parts 378 + common 0 + shim 0 = 378 -> ok
(b) top-level names: source 104, parts + common 104, each exactly once; ... -> ok
(c) run list: 65 scenario entries in the source, 65 across the parts ... -> ok
(c2) run sites read again from the plain AST ... (65) against the new files (65) ... -> ok
(d) byte identity: sha256 of 104 moved segments before == after -> ok
(compile) 7 written file(s) compile -> ok
(f) closing: each of 5 part runner(s) holds exactly one closing call (finish) -> ok
(g) import: 6 written file(s) (test_no_move_seam_n1_n9.py, ... test_no_move_seam.py) each imported alone in a child process, cwd outside the repo, the written files and the tests dir of the target tree as the only extra path entries, exit 0 required -> ok
PROOF: ok
apply rc 0
k4s exit 0 ['=== no_move seam_k4s: 73/73 ok ===']
c26_g27_f2 exit 0 ['=== no_move seam_c26_g27_f2: 87/87 ok ===']
pyflakes rc 0 ''        (pyflakes over the 5 parts, the common module and the shim)
```
Both tallies are the expected 73/73 and 87/87.

Regression, loop_b (N4 map) and controller_rework (N6 map) re-cut on temp copies of the old files (`regress.py`), sha256 against the generated files in the two worktrees:
```
SAME test_story_run_loop_b_loop.py            61944de94f8cefb022f657ce25054ee5b8509141ed2c6b727fa46b98db41be7a
SAME test_story_run_loop_b_threshold.py       77c5f73588c0d3a6e5bee9139f441867a1e365f6edd1224962fd348d45ba1b2d
SAME test_story_run_loop_b_answers.py         77045f339630a77fbd8bc2da43732ba6a9c10937482958ab95f8d2833773dbdf
SAME story_run_loop_b_common.py               94d04756dbf21e22010af9ad987995de5f2d80f83143498dd7b1ea79c5fe9b11
SAME test_controller_rework_jobs_guard.py     5e5729d20793eceaf1a1228b88f58c1a3bcbfccb02cf82d9726724bd30560790
SAME test_controller_rework_repair_binding.py 0f0de67da24bc3f7d174ac179c4fe5847dd898ebd58b025e48f6e983575b041a
SAME test_controller_rework_window_words.py   9b0afd2a1d1ff30283f240e7606c5b5b79ec3f90a3cb769e46009f18201da7f1
SAME controller_rework_common.py              a7763ce5eb2ac294f5d67e0a05e303e547c7e23fcaa3f3c0b1de58bf5310fa49
```
Both cuts: PROOF ok including (f) and (g); no CLOSING and no KEPT line (their parts already closed and imported fine). The infra_failure, handoff_values and freshness maps were NOT re-run (not asked); no key was added, so their maps stay valid, but their byte-identity is unproven.

## Deviations / findings

1. Spec said the import child has "the tests dir of the target tree as the only extra path entry". The would-be files are not in that dir before the proof passes (a failed proof must leave the target unchanged), so the child gets TWO entries: a temp stage dir holding the would-be files first, then the tests dir of the target tree. Said in the proof line.
2. The rule 1(b) applies to PARTS only. First version applied it to the common module and the shim too: it changed `story_run_loop_b_common.py` (an added `import harness` + `del harness`, sha differed) and broke the "byte-identical" regression; common and shim are covered by proof (g) (the shim is imported; common is imported by every part). If the Lead wants the rule in common too, the loop_b common would differ by those two lines.
3. A local-module import that a kept line ABOVE already loads (e.g. `import harness` dropped while `from harness import check` is kept) is listed as dropped, not re-added: its effect is preserved, and adding it would have changed the existing parts.
4. Fork not decided: "local module" = a `<root>.py` file in the tests dir whose name does not start with `test_` (harness, story_run_common, state_census, ...). Package modules (`human_text`, `no_move`, `story_run` live in scripts/) are not beside the old test and are not kept by this rule - read from the Lead's text "(a file beside the old test)" and the edge about 2.8.
5. Analogs noticed (not fixed): (i) `(g)` doubles module-import time per apply (first static pass skips it in --apply, so it runs once in apply and once in dry-run: no duplicate); (ii) the old dropped-import behaviour also hits `import copy` at old line 2048 (a late import in the middle of the file) - listed as dropped, harmless; (iii) the proof still does not run a part's scenarios (spec 2.5 (e) stays the node's own run); (iv) `test_split.py` long functions (T-F3) are still queued, `header_text`/`render_runner` grew a little.

## Needed beyond the manifest
Read: `ai-packages/qa-factory/scripts/tests/harness.py` (`finish`, `SCRIPTS`), the generated N2 parts, `git show HEAD:` old N2 file, maps of N4/N6 (needed to pick the regression files), `test_no_move_seam_*` in N2WT. `sys.stdlib_module_names` needs Python 3.10+ (the repo runs 3.12; before 3.10 every module counts as non-stdlib, a safe direction).

## Questions
- Is the `import X` + `del X` form acceptable as the path-effect binding in generated test files (pyflakes clean), or does the Lead prefer a named helper in `harness` (a `harness.use_scripts_path()`-style call) - that would be a package change, not decided here.
- Should the rule also cover common/shim (deviation 2)?
