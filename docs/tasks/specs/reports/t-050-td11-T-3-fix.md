# T-3 fix round (journal task t-053, attempt 2; the first report is named t-050 — T-F7: the names differ, the task is t-053)

Worker: builder (fresh), in place in WT = `C:\QAFactory\forge-repo\.claude\worktrees\agent-af3a560c41c1247c7`. Not committed. No edit under `ai-packages/`; no `--apply` on a real tree (temp copies in `C:\Users\i_mas\AppData\Local\Temp\tsplit_*`, outside the repo). Files changed: `tools/test_split.py`, `tools/test_test_split.py`, this report.

## Per finding: fixed / how / test row

| Finding | Fixed | How | Test row (in the one parameterised table) |
|---|---|---|---|
| T-B1 a (`if __name__` of direct scenario calls, handoff_values) | yes | `analyze`: a guard-called function is a runner only if it holds finish/run_scenarios, or is "runner-shaped" (`_runner_shaped`: reads a run list by name, or holds only finish / run_scenarios / bare calls / a literal `for`, and no check of its own). Scenarios the guard calls stay scenarios | `T-B1 guard_of_direct_scenario_calls_is_cut` (apply, parts run: 3/3 and 2/2) |
| T-B1 b (`for scenario in (<names>): scenario()` inside `main`, no_move_seam) | yes | `_fill_stmt_block` records a `for` statement (`_literal_for`); `render_runner` restricts the literal per part with `_fmt_list`; entries kind `iter` feed proof (c) | `T-B1 for_over_a_literal_tuple_inside_main_is_cut` |
| T-B1 c (`run_scenarios([], chosen)` in a by-name `main`, freshness) | yes | a by-name block may call `run_scenarios` with an EMPTY literal list; a non-empty literal list is still refused (`_verbatim_problems`) | `T-B1 run_scenarios_empty_first_list_in_a_by_name_main_is_cut` (apply; part alone with argv `a_two` 1/1; argv naming another part's scenario exits nonzero, no tally) |
| T-B1 d (grounding_table: module-level checks, no runner; draft was a false green) | refused, not supported | `analyze`: no scenario in any run list and module-level assign/statement with check sites -> ONE problem "the file is a module-level script ... not supported by this tool". The draft prints it too (rc 2), so draft and map verdicts agree | `T-B1 module_level_script_refused_by_draft_and_map` |
| T-B2.1 module-level check homed in common | refused | `soundness_problems` (new, called in `build_plan` before any generation, so before any proof and write): an assign/statement homed in common with `seg.checks` | `T-B2.1 ...` (assign `SEEN = check(...)` and a bare `check(...)` statement) |
| T-B2.2 scenario call nested in a by-name consumer | refused | `_verbatim_problems` walks EVERY call (`ast.walk`) of a by-name function block and of a by-name module-level `for`: refused: a no-arg call of a top-level function; a call of a check-holding function (transitive, `an.check_funcs`) unless it is handed the loop variable (the block's own once-per-entry wrapper, as `scenario(_fn)` of test_infra_failure) | `T-B2.2 ...` (`extra()`; `checker(1)`; and the allowed wrapper that holds a check) |
| T-B2.3 statement before an import | refused | `statement`-kind segment with a line before the last import / sys.path line | `T-B2.3 ...` (`os.environ[...] = ...` before `import runner_lib`) |
| T-B2.4 conditional rebinding across homes | refused | a name bound by segments of two homes | `T-B2.4 ...` (`FLAG` row in a, `if ...: FLAG = True` in common) |
| T-B2.5 late import shadows a def | refused | `an.import_lines` (all lines per bound name); an import after a def/assign of the same name | `T-B2.5 ...` |
| T-B2.6 `global` rebinding of a common name read by a part | refused | a `global` write of a name homed in common that a segment of another home or a generated runner reads | `T-B2.6 ...` |
| T-B2.7 mutating statement homed apart from its name | refused | a `statement` segment whose free names include a name homed elsewhere | `T-B2.7 ...` |
| Proofs (Lead 3) | done | (a) is labelled "check call sites (AST sites, not executed checks)"; (e) renamed "(compile)"; new (c2): the old run list read again from the PLAIN AST of the old file (`plain_run_sites`: bare calls and literal-list elements of top-level functions in module-level code and in check-free defs) against the same reading of the new files; it uses the classifier only for the runner function NAMES to leave them out. (b), (d) still re-segment with `analyze` (generator-integrity proofs, said so in the verdict) . A line "NOT RUN HERE" says spec 2.5 (e), the executed-check count and the reverse-order run are the node's. A proof (f) "each part imports and lists its scenarios without running them" is NOT offered: importing runs module-level code and listing needs the runner, i.e. scenarios | `dry_run_writes_nothing_and_prints_the_proof` (keys), `proof_c2_reads_the_run_list_without_the_classifier` (c2 fails on a dropped entry) |
| Lead 4 / T-F5 rollback deletes an identical target | fixed | `placed` names that were in `same` are skipped by the rollback | `T-F5 rollback_never_deletes_an_identical_target` (os.replace patched to fail on the second part; tree identical to before) |
| T-F1 | done | see Proofs | |
| T-F2 dead/lying code | done | removed `dropped`, the empty `for part ... pass`, `gen_names`, `entries ... or True`, `src_node`; `validate_map` returns nothing now | |
| T-F4 importer writes through the module alias | refused | `find_importers`: Store/Del ctx on `ALIAS.x`, and `patch.object / setattr / delattr` on the alias, are importer problems | `T-F4 importer_writing_through_the_module_alias_refused` |
| T-F6 `done_state` traceback | fixed at the source | `validate_map` refuses a non-string `parts` item | `T-F6 non_string_part_refused_not_a_traceback` |
| T-F9 argv name of another part | partly | the report prints `ARGV <part>: <its scenarios>` when the source reads argv (so the node/person can find the part); a part whose source has no zero-scenario guard still exits green on a foreign name (only freshness-like sources, which have their own `sys.exit`, exit nonzero: tested) | in the freshness row |
| T-F7 | done | this report's header | |
| T-F3 long functions | NOT DONE (queued) | `analyze`, `build_plan`, `prove`, `render_runner`, `_fill_stmt_block`, `run_map`, `run_draft` are still over 60 lines (build_plan is now a little shorter: the T-B2 phase moved to `soundness_problems`). The split along the commented phases is its own move | |
| T-F8 WORLD_HINTS | queued, as the verdict says | unchanged | |

Edge rows asked for in the dispatch: zero runner blocks and a part with zero scenarios -> refused ("part `...` holds no scenario"), row `edge no_runner_block_and_a_part_without_a_scenario_refused`; a map that homes nothing in common -> handled, no common file, no common import, row `edge map_homing_nothing_in_common_writes_no_common`. Every refusal row also asserts: exit 2, no `PROOF` line, "refused: nothing was written", the tree unchanged (before any proof, before any write).

## New rows counted by name (35 passed = 18 old + 17 new; the T-B1/T-B2/T-F rows are in ONE parameterised test)

T-B1 x4: `guard_of_direct_scenario_calls_is_cut`, `for_over_a_literal_tuple_inside_main_is_cut`, `run_scenarios_empty_first_list_in_a_by_name_main_is_cut`, `module_level_script_refused_by_draft_and_map`. T-B2 x7: `T-B2.1` ... `T-B2.7`. Plus `T-F5 rollback_never_deletes_an_identical_target`, `T-F6 non_string_part_refused_not_a_traceback`, `T-F4 importer_writing_through_the_module_alias_refused`, `edge no_runner_block_and_a_part_without_a_scenario_refused`, `edge map_homing_nothing_in_common_writes_no_common`, `proof_c2_reads_the_run_list_without_the_classifier`. The old row `dry_run_writes_nothing_and_prints_the_proof` has its keys updated for the renamed lines; the old argv/loop and run-list rows are unchanged.

## Draft table of the 15 files (`--draft`, read only, `drafts.py` in the scratchpad; the spec section 3.1 holds 14 rows, I added `test_red_window` (N10) as the 15th: say if another file was meant)

| File | rc | refused constructs |
|---|---|---|
| test_infra_failure | 0 | 0 |
| test_story_run_refusals | 0 | 0 |
| test_story_run_s0 | 0 | 0 |
| test_no_move_seam | 0 | 0 (was 67) |
| test_story_run_stand_identity | 0 | 0 |
| test_story_run_s6 | 0 | 0 |
| test_story_run_freshness | 0 | 0 (was 1) |
| test_words_doors | 0 | 0 |
| test_story_run_loop_b | 0 | 0 |
| test_handoff_values | 0 | 0 (was 215) |
| test_controller_rework | 0 | 0 |
| test_probe_by_code | 2 | 13 |
| test_grounding_table | 2 | 1: "the file is a module-level script ... not supported by this tool" (was a false green) |
| test_probe_by_code_languages | 2 | 5 |
| test_red_window | 0 | 0 |

Refusals explained as correct (wave 2; none of them is a wave-1 file):
- `test_probe_by_code.py:3115-3161` and `test_probe_by_code_languages.py:2241-2260`: `main` is not a list of calls: it builds a shared fixture (`stub_dir = temp_dir(...)`, `stub.write_text(...)`, `root = project()`), runs several scenarios inside one `try/finally` and cleans up after them; the languages `main` also builds a `sections` list of lambdas and filters it by argv. A per-part runner cannot be generated from that without guessing what the fixture is shared by. The map cannot fix it; the node (N7, N9) first hoists the shared setup into scenario functions or asks the Lead. The refusal names each line.
- `test_grounding_table.py:140`: the module-level script shape (decision 1: "not supported" this round, and the draft says the same as the map).

Home-independent T-B2 neighbours over the same 15 files (`sound15.py`, read only): statement before an import 0 in all 15; late-import shadow 0; a name bound by two segments 0 (except grounding_table, a script, already refused); `global` writes 0. So NONE of the seven refusals fires on a wave-1 file.

## DoD output, verbatim

```
$ python -m pytest C:\QAFactory\forge-repo\.claude\worktrees\agent-af3a560c41c1247c7\tools\test_test_split.py -q
...................................                                      [100%]
35 passed in 2.48s
```

Cuts of the three files in a temp copy of the tests dir (only the `*.py` of the dir copied to `C:\Users\i_mas\AppData\Local\Temp\tsplit_<stem>`, a fake repo root above it; the maps are generated by `cut.py` (scratchpad) from the `--draft` rows by the spec 3.1 line ranges; names the ranges alone could not place were moved to common by the tool's own "home it in common" refusals, listed below):

```
== test_handoff_values: map settled after 1 refinement(s); 1 name(s) moved to common beyond the ranges: ['_green_copy']
(a) check call sites (AST sites, not executed checks): source 286, parts 286 + common 0 + shim 0 = 286 -> ok
(c) run list: 53 scenario entries in the source, 53 across the parts, each in its own list, source order kept inside each part -> ok
(c2) run sites read again from the plain AST of the old file (53) against the new files (53), classifier not used -> ok
(compile) 4 written file(s) compile -> ok
PROOF: ok
== test_no_move_seam: map settled after 1 refinement(s); 3 name(s) moved to common beyond the ranges: ['FACTS', 'SITE_Q', '_site_ok']
(a) check call sites (AST sites, not executed checks): source 378, parts 378 + common 0 + shim 0 = 378 -> ok
(c) run list: 65 scenario entries in the source, 65 across the parts, each in its own list, source order kept inside each part -> ok
(c2) run sites read again from the plain AST of the old file (65) against the new files (65), classifier not used -> ok
(compile) 7 written file(s) compile -> ok
PROOF: ok
== test_story_run_freshness: map settled after 1 refinement(s); 1 name(s) moved to common beyond the ranges: ['fixed_adapter']
(a) check call sites (AST sites, not executed checks): source 203, parts 201 + common 2 + shim 0 = 203 -> ok
(c) run list: 30 scenario entries in the source, 30 across the parts, each in its own list, source order kept inside each part -> ok
(c2) run sites read again from the plain AST of the old file (30) against the new files (30), classifier not used -> ok
(compile) 5 written file(s) compile -> ok
PROOF: ok
```
The (b) and (d) lines were also ok in the same runs (handoff_values 91 names / 91 segments; no_move_seam 104 / 104 plus the shim line, 3 names re-exported; freshness 64 / 64). `--apply` on the no_move_seam temp copy printed `APPLIED ... PROOF: ok`, and a second run `nothing to do: test_no_move_seam.py is already a shim over 5 part(s)`. No part was run (slow package files; the tally is the node's own run).

## Not done / questions

1. T-F3 (function lengths) not done; queue it or give it a round (it does not change behaviour).
2. QUESTION (T-B2.3 width). I read class 3 as the verdict words it: a STATEMENT (not a def, not a plain assignment) before an import. My first, wider reading (any executed assign/class too) refused `test_no_move_seam.py`: 15 plain assignments (lines 25, 26, 314, ..., 1943) lie above the stdlib `import copy` at line 2048, and `test_story_run_s6.py` has 1 above line 63. Hoisting `import copy` above them is harmless, so I did not refuse them. The unaddressed neighbour: an assignment whose value is a CALL that an import after it could affect (e.g. an env var set by the late import). Do you want that refused (it would refuse no_move_seam as it stands, so its node would first move `import copy` to the top) or left?
3. QUESTION (T-F9). The generated part of a by-name source with no zero-scenario guard still exits green for a foreign argv name. Only the tool's report names the part (ARGV lines). Making the part exit nonzero needs a generated line in the runner (a design call); left.
4. QUESTION (proof (f)): I judged it impossible without executing module-level code and the runner and did not offer it; confirm that is the answer.
5. The first worker's spec reading of dispatch edge 7 (shim runs parts only with `--all`) is unchanged and was confirmed right by the verdict.

## Beyond the manifest / siblings noticed (class: "a verbatim-copied block")

- Read beyond the manifest: `story_run_common.py` (`run_scenarios` at 715), `test_infra_failure.py:1100-1139` and `:156` (the `scenario(fn)` wrapper that holds a check: it is why a check-carrier rule had to exempt the loop-variable wrapper), `test_probe_by_code.py:3100-3161`, `test_probe_by_code_languages.py:2232-2273`, `test_no_move_seam.py:2040-2053`, `test_story_run_freshness.py:1347-1373`.
- Siblings: (i) a verbatim consumer that holds its own check and whose run list spans two parts is copied twice: proof (a) fails then (safe direction, as the verdict said; no current file has it). (ii) `find_importers` and the spec 2.6 command search `import x` forms only; `importlib.import_module("test_x")` is not seen (the spec's own search found none). (iii) the same line-slicing/decoder/free-names/imports code duplicates `tools/source_split.py` (verdict "T-4 shared reader": the Lead's node, not mine).
