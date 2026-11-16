# t-917 (F19) -- stream S1: tools/owns_readers.py and its door in dispatch_new.py

DoD: `python -m pytest tools/test_owns_readers.py tools/test_dispatch_new.py -q`  (run from the worktree root, `-p no:cacheprovider`)

## Output

```
........................................................................ [ 79%]
...................                                                      [100%]
91 passed in 19.69s
```

(test_owns_readers.py: 44 passed, test_dispatch_new.py: 47 passed.)

## Measured runs (worktree root; base origin/main 2b6b1577 at run time)

1. `python -B tools/owns_readers.py --paths tools/dispatch_manifest.py tools/test_dispatch_manifest.py --readers` -- real 0.724 s

```
readers: 20 outside owns, 11 lines below -- base origin/main 2b6b1577 (literal mention; known misses: tools/owns_readers.py docstring)
- outside: tools/test_agent_budget.py (test) names tools/dispatch_manifest.py
- outside: tools/test_dispatch_gate.py (test) names tools/dispatch_manifest.py
- outside: tools/test_dispatch_new.py (test) names tools/dispatch_manifest.py
- outside: tools/test_handoff_gate.py (test) names tools/dispatch_manifest.py
- outside: tools/test_dispatch_cut.py (test) names tools/dispatch_manifest.py
- outside: tools/test_dispatch_gate_md.py (test) names tools/dispatch_manifest.py
- outside: tools/test_hop_metrics.py (test) names tools/dispatch_manifest.py
- outside: tools/test_journal_hooks.py (test) names tools/dispatch_manifest.py
- outside: tools/test_owns_gate_md.py (test) names tools/dispatch_manifest.py
- data: tools/warn_layers.json names tools/dispatch_manifest.py
- more: tools/dispatch_manifest.py -- 10 code readers not listed (--readers / --all lists them)
```
Shape = §2.4 row 1 (20 outside: 9 test, 10 code, 1 data; 12 lines).

2. `python -B tools/owns_readers.py --paths ai-packages/qa-factory/scripts/story_run.py --names s0_criteria` -- real 0.853 s

```
readers: 253 outside owns, 6 lines below -- base origin/main 2b6b1577 (literal mention; known misses: tools/owns_readers.py docstring)
- names: ai-packages/qa-factory/scripts/tests/test_conductor_doors.py (test, slow) names s0_criteria
- names: ai-packages/qa-factory/scripts/tests/test_silent_passes.py (test, slow) names s0_criteria
- names: ai-packages/qa-factory/scripts/tests/test_story_run_s0.py (test, slow) names s0_criteria
- names: ai-packages/qa-factory/scripts/tests/fixtures/driver-layers.json (data) names s0_criteria
- more: ai-packages/qa-factory/scripts/story_run.py -- 92 test, 81 quarantined, 67 code, 13 data readers not listed (--readers / --all lists them)
- more: name s0_criteria -- 1 code readers not listed (--readers / --all lists them)
```
Shape = §2.4 row 2 / Example B (253 outside, 92 test, 81 quarantined). Counts 67 code / 13 data against the spec's 68 / 12 differ
by one: the spec's numbers are the critic's at 0d6f61b1, this is a later base. Without `--names` the same path prints `hot` + `more` (checked).

## Edge E-n -> behaviour -> test row (tools/test_owns_readers.py, test_owns_readers_table unless noted)

| Edge | Behaviour | Row |
|---|---|---|
| E-1 | exit 2, `OWNS_READERS REFUSED: no path given -- pass --paths <owned path>...` | test_cli_door |
| E-2 | Example C only, nothing else run | base-missing |
| E-3 | `quarantine: unknown (... absent ...)` | quarantine-layers-absent |
| E-3b | `quarantine: unknown (... read empty)`, rest kept | quarantine-show-fails |
| E-3c | `quarantine: unknown (... not JSON)`, rest kept | quarantine-malformed |
| E-3d | no line, no unknown | quarantine-section-gone |
| E-4 | `- unsearched: x.py (outside the repo; ...)`, no absolute path | outside-repo |
| E-5 | `(new)` path/name: present -> exists; absent -> no line | new-exists, new-absent, names-new-exists, names-new-absent |
| E-6 | dir over 40 files -> one unsearched; small dir expanded | dir-wide, dir-small |
| E-7 | `readers: 0 outside owns, 0 lines below ...` | quiet, untracked-copy, short-stem-not-a-reader |
| E-8 | space / Cyrillic path searched and counted | space-cyrillic |
| E-9 | `-x.py` searched; `--part` name found; every pattern after `-e`, paths after `--`; base starting with `-` not read as a ref (code, no row beyond these) | dash-name, names-nonword |
| E-10 | short stem (<4) file name only; common stem sorts last | short-stem-not-a-reader / short-stem-named, order-tiers |
| E-11 | binary file skipped (`-I`) | binary-skipped |
| E-12 | one line per reader, names joined, counted once | two-owned-one-line |
| E-13 | any ref/sha, header names ref and sha; the world is a detached HEAD | base-sha, quiet (regex on sha8) |
| E-14 | `slow: unknown (...)` | slow-malformed |
| E-15 | `readers: unknown -- git grep exited <rc> (...)`, absent line kept; rc 128 and -1 | grep-rc-128, grep-timeout |
| E-16 | `presence: unknown`, no absent/exists, quarantine and slow unknown | lstree-fails |
| E-17 | 21 names -> 20 searched + unsearched line; non-word name matched without `-w` | names-cap, names-nonword |

T2 (tools/test_dispatch_new.py): rows `readers-block` (real tool, round trip `test_printed_text_passes_check_and_ids_read_back` runs on it),
`readers-no-note` (+ universal `READERS NOTE not in err`), `names-backtick`, `names-accepted`; tests `test_block_leaves_the_manifest_reads_unchanged`
(position invariant with the worst-case Example B block), `test_readers_tool_raises`, `test_block_refused_is_replaced` (vector `manifest-skip: bogus -- x`
does refuse), `test_names_reach_the_report`. An autouse fixture stubs `owns_readers.report` (unresolved-base report) on every row but `readers-block`.

## Deviations and choices (none changes a spec requirement; each is a point to accept or reverse)

1. dispatch_new decides on the HEADERS first and refuses there (before the tool runs), then decides on headers + block (§3.1 step 3), then the step-4 fallback. Same refusals and messages; a refused dispatch never pays for a git search (tests: ~25 refusal rows).
2. grep is run as several `git grep` calls, not one (§2.3 (i) says one call): whole-word patterns apart from plain ones (S-8, a single call has one `-w` setting), and no pattern a substring of another inside one call (`git grep -o` prints only the longest match at a position, so `foo.py` would hide `foo`). `--names` shares those calls. Typical block: 2-4 grep calls.
3. Name presence uses `-o -z` WITH file names (spec: `-h`), because `exists: name ... already named by <K> files` needs K.
4. Unknown quarantine registry: test readers under scripts/tests/ are still listed/counted as tests, and the `more` line gains the part `? quarantined` (spec: "no reader is counted as non-quarantined" -- listing them as tests keeps the over-report direction; counting them only under `?` would hide them).
5. `--all` also suppresses the `hot` line (the list is complete). Quarantined readers under `--all` print as `- outside: <f> (test) (quarantined: the canon does not run it; do not edit) names <x>`.
6. An item with a control character (a newline in a path or name would split a git pattern) is not searched and named in `- unsearched: N paths|names with a control character (not searched)`. Not in the spec.
7. `--paths -x.py` on the CLI is read by argparse as an option; the API (what dispatch_new uses) takes it as a path (row dash-name). A CLI user passes `--paths=./-x.py` or the API.
8. `report()` with an empty path list is not refused (only the CLI refuses, E-1); it prints the 0-readers header.
9. Wall time: test_owns_readers.py takes ~19 s (44 rows x ~8 git calls on Windows; ~0.45 s a row). The spec says "well under 10 s"; not asserted, not reduced.
10. Windows-style absolute paths: a `C:\...` path on a POSIX machine is classed as outside the repo.

## Questions

None blocking. Choices 4 and 5 are small design points the Lead may want to confirm.

## Needed beyond the manifest

`tools/streams.py` (utf8_stdio), `docs/tasks/handoffs/` existing handoffs (form only), `ai-packages/qa-factory/scripts/tests/test-layers.json` and `scripts/slow_tests.json` (real shape of the two registries, read only), `tools/test_dispatch_manifest.py` not needed. No package file touched.

## Analogs noticed (report, not fixed)

- `tools/test_quarantine.py::_blob_sections` returns empty sections on any git failure (the unsafe direction for a reader role); owns_readers guards it, other callers (if any) are not checked here.
- `tools/dispatch_new.py::_empty_item` checks `given`/`owns` only; an empty `--names` item is silently ignored by the tool (a blank name is nothing), not refused.
- `dispatch_gate.given_path_warn` will WARN on a block path present on the base but absent from the launching checkout (spec §3.1, accepted; seen as expected, not exercised in a test).
- Axes (Lead's map edits, spec 6 L8): axis 9 (new forge "is this a test" reader: `owns_readers._classify` by scope glob), axis 10 (new gitcmd caller `owns_readers`; `test_quarantine._git` runs the one `git show`), axis 34 (the `--witness-for` vs `owns_readers` split is in the docstring).
