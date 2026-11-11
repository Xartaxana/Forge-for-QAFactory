# Test-diet brief — the standing spec of a pruning node

The rule is `docs/TESTING.md`; the plan is `docs/tasks/test-diet.md`. A pruning dispatch names its files in `owns:` and
points here; everything below applies to each owned test file. The package is English (FR-30).

## What you do in each owned test file

Read the file. For every check (a `check*(...)` call, an `assert`, a `test_*` function, a unittest method) decide its
kind and act:

| Kind | How to recognise it | Action |
|---|---|---|
| behaviour | calls package code (a function, a CLI through `run_script` / `subprocess`) and asserts on the result: an artifact, a return value, an exit code, a refusal | KEEP |
| source pin | reads the text of a package `.py` (`read_text()`, `inspect.getsource`, `ast.parse` of a script) and asserts a string, a regex count, a call site, an order of lines | DELETE — unless the asserted string is a NAME FROM A DATA FILE, or a field one stage writes and another reads, and the scan is the only proof the reader exists: that is a data join — KEEP it, or rewrite it as a call of the reader with that field. If it holds a layering or one-writer invariant that no behaviour test would catch, do not move it — list it in the report under `structural:` with one line why |
| measured constant | asserts an exact byte size, line count, duration, number of rows that is only "what it is today" | DELETE; a documented CAP with headroom (`<= LIMIT` where LIMIT is a named limit of the product) is behaviour — keep; a hash or id literal that is a key of records already on a project's disk (attempt identity, receipt keys) is a compatibility contract — KEEP, with a comment saying so |
| wall clock | asserts on elapsed time or sleeps to make an order | DELETE or rewrite on a step clock when the behaviour matters (FR-31) |
| "as before" | asserts that a helper reproduces the code it replaced, an incidental detail no reader depends on | DELETE |
| negative control | feeds a corrupted or synthetic input to a predicate DEFINED IN THE TEST FILE, or a corrupted copy of a real file, to show the test can fail | DELETE; the same input fed to PACKAGE code is behaviour — KEEP |
| receipt duplicate | several checks assert the same behaviour once per DoD key, edge id or mutation, with the same call and a different label | MERGE into one table of cases, one assertion loop; the case id stays in the message so a red line names the case |
| workflow document | asserts lines of CHANGELOG, a batch file, a report, a debt table | DELETE |
| role-text pin | asserts that a phrase stands in `agents/*.md`, `skills/**`, `references/*.md`, `phases/*.md` | KEEP UNTOUCHED (the owner's word 10.11.2026: a role's rule must not be lost; it moves to a register in node TD-5, not here) |
| data join | asserts that every name in one data file exists in another, that a registry row has its reader | KEEP |

When a whole file ends up empty of checks, delete the file (`git rm`) and remove its name from `plans/features.json`
(one line; mind the trailing comma of the list).

Speed, only where it is cheap and safe: when a file starts the driver, the controller or a script once per check with
the same inputs, build the world once and read every check from it. Do not restructure a file you cannot run.

## What you never do

- No edit to production code, role texts, references, fixtures used by another test file, `harness.py`,
  `story_run_common.py`, `story_step_common.py`, `selftest.py`, `slow_tests.json`, CI files.
- No new test, no new file, no rename of a test file.
- No deletion of a behaviour check because it is slow, long or ugly. In doubt — KEEP and list it under `doubt:`.
- No weakening of an assertion that stays.
- No git state change except `git add` / `git rm` / `git commit` of your owns in your own worktree.
- No change of the shell's working directory: absolute paths only (`python -B <absolute path>`, `git -C <worktree>`).

## Edges

- A check that mixes behaviour and a source pin in one function: remove only the pin lines, keep the behaviour.
- A helper, import or fixture left unused by your deletions: remove it (the lint ratchet counts unused imports).
- A file listed in `ai-packages/qa-factory/scripts/slow_tests.json` above 60 s: do NOT run it locally; edit by
  reading, say so in the report — the CI of the wave judges it.
- A file that is red BEFORE your edit (run it first): do not repair behaviour; report the red lines and prune only.
- A pytest-style file must keep its `if __name__ == "__main__"` entry; a harness file keeps `finish(...)`.
- A check you cannot classify: KEEP, list under `doubt:`.
- A deleted function that read the text of `story_run.py`: list `file::function` under `map rows:` in the report AND
  remove its row from `source_readers` (or `source_mentions`) of `scripts/tests/fixtures/driver-layers.json` — that
  file is in your owns for this purpose only; `test_driver_layers.py` (L8) is then part of your witness. Wave 1 left
  five such rows and turned the branch red.
- A scan whose corpus mixes package `.py` and role texts: drop the `.py` part, keep the role-text part.
- Removing a source pin leaves a function that no longer checks what its name says: assert the same words on the
  OUTPUT the function already produces (stderr, message, artifact) if that is a few lines; otherwise `doubt:`.

## Witness (DoD)

For each owned file that still exists: `python -B <absolute path to the file>` run once BEFORE and once AFTER, exit 0
after; the summary line of both runs (`=== label: N/M ok ===` or the pytest line) goes into the report verbatim.
`python -B -c "import ast,sys; ast.parse(open(sys.argv[1],encoding='utf-8').read())" <file>` passes for every file.

## Report (the handoff file named in the dispatch)

A table, one row per file: lines before / after, checks before / after (from the summary lines), seconds before /
after, then per file the removed checks as `kind: count` and, for every removed check that is not plainly a pin, one
line naming it. Sections `structural:`, `doubt:`, `red before:` (each may be `none`). The commit hash. Nothing else.

Commit message: subject `tests: prune <first file> .. <last file> (test-diet <node id>)`, then the lines
`architecture: none -- test files only`, `judgment: none -- no package check changed`,
`axes: not a mechanism (test pruning under docs/TESTING.md)`,
`piles-skip: <node id> -- the owner's word 10.11.2026, docs/tasks/test-diet.md`, `[F15]`.
