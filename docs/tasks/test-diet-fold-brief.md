# Test-diet fold brief — the standing spec of a fold node (TD-14)

The owner's word 10.11.2026 (evening), on the redundancy report `docs/tasks/specs/reports/td-12-redundancy-8069240.md`:
every test file that adds under 100 product lines to the coverage of the others is read; what matters in it moves into the
tests that cover behaviour; the rest goes. The rule is `docs/TESTING.md`; the kinds of checks are the table of
`docs/tasks/test-diet-brief.md` (read both first). A fold dispatch names its files in `owns:` and points here.

## Words

- **candidate** — an owned test file. The dispatch gives, per candidate, `adds` (product lines only this file covers after
  the bigger files; 0 = nothing) and its lines.
- **home** — the test file that already exercises the same script through the same door. Find it by what the candidate
  calls: the script it runs or imports (`role_commands.py` -> `test_role_commands.py`), then the family
  (`test_gate_*`, `test_controller_*`, `test_cost_capture*`). A home is NOT a candidate of another group of the same wave
  unless it is in your own `owns:`.

## What you do with each candidate, in this order

1. Read it whole. Sort every check by the table of `docs/tasks/test-diet-brief.md`. Checks of a kind that table deletes
   (source pin, measured constant, wall clock, "as before", negative control of a predicate defined in the test, workflow
   document) are deleted. Role-text pins stay untouched where they are (the owner's word: a role's rule is not lost).
2. For every BEHAVIOUR check left, open the home and answer one question: **does the home already assert this behaviour —
   the same door, the same class of input, the same outcome (artifact, exit code, refusal, field)?**
   - yes -> the check is a duplicate: delete it.
   - no -> it is unique: MOVE it into the home as a case — a row in an existing table of cases when the call is the same
     and only the input and the expected value differ; otherwise one new function in the home, using the home's own world
     builder and helpers. The moved check keeps its assertion at full strength and its id in the message, so a red line
     names the case.
3. Decide the candidate's fate, one of three, and write it in the report:
   - **folded** — nothing unique is left in it: `git rm` the file and remove its name from every registry that lists it
     (below);
   - **kept as the home** — the candidate IS the only test file of its script or of its door (a small script has few
     lines; that is why it adds little). It stays, pruned by step 1. Name the script.
   - **kept, doubt** — you cannot tell whether a check is covered, or moving it needs a world the home does not build and
     building it costs more than about 40 lines: leave the file as it is and say why in one line per check.

Budget of a fold: the lines added to homes are under a third of the lines deleted; a group that cannot hold this says so
in the report with the reason (the owner's door: the builder explains, the critic judges).

## Registries that name a test file — clean them in the same commit as the `git rm`

`plans/features.json`; `ai-packages/qa-factory/scripts/tests/fixtures/driver-layers.json` (`source_readers`,
`source_mentions` — rows keyed `file::function`); `ai-packages/qa-factory/references/gate-registry.json` (`test`);
`ai-packages/qa-factory/references/stage-joints.json`; `CONTRACT_TESTS` and `TEST_TIMEOUTS` in
`ai-packages/qa-factory/scripts/selftest.py`; `ai-packages/qa-factory/scripts/slow_tests.json`; `.gitlab-ci.yml`;
`ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json`. Grep each for the file's name; a row that names a
MOVED check is re-pointed to the home (`home_file::function`), a row of a deleted check is removed. These files are in
your owns for these rows only. A file listed in `CONTRACT_TESTS` or in `gate-registry.json` is never folded: it is
**kept as the home** (prune only), because a gate names it.

## What you never do

- No edit to production code, role texts, references (except the registry rows above), `harness.py`,
  `story_run_common.py`, `story_step_common.py`, CI jobs.
- No new test FILE, no rename, no new helper module.
- No deletion of a behaviour check you did not find in the home: unique means MOVE, doubt means KEEP.
- No weakening of an assertion. No change to a home's existing checks beyond adding rows and functions.
- No edit to a `test_story_run_*.py` file or to any test file outside your owns except as a home; a home that belongs to
  another group of this wave (the dispatch lists the other groups' ranges) is not edited — the check stays where it is
  and goes under `doubt:` with the home's name.
- No git state change except `git add` / `git rm` / `git commit` in your own worktree; no change of the shell's working
  directory (absolute paths, `git -C`); no trailing `2>&1`.

## Edges

- A candidate with fixtures of its own (`fixtures/<name>/`): when the file is folded and no other test reads the
  fixtures (grep the directory name over `scripts/tests/`), `git rm` them too; when a moved check needs them, they stay.
- A candidate the dispatch marks `slow`: do NOT run it locally; read, decide, and say "not run" in the report. A HOME
  marked slow or listed in `slow_tests.json` above 60 s is not run either — the wave's CI pipeline judges it.
- A candidate red BEFORE your edit: do not repair; report the red lines; a red file is never a source of moved checks —
  **kept, doubt**.
- An empty home choice (no file exercises that script): the candidate is **kept as the home**.
- Two candidates of your group that test the same script and neither is the bigger: the one with more behaviour checks
  becomes the home, the other folds into it.
- A check that only asserts "the script exits 0 and prints something": it is behaviour only if no other check runs that
  door; otherwise a duplicate.
- A helper, import or fixture left unused: remove it. A pytest-style file keeps its `if __name__ == "__main__"` entry; a
  harness file keeps `finish(...)`.

## Witness (DoD)

For every home you edited and every candidate that stays (not slow): `python -B <absolute path>` once BEFORE and once
AFTER, exit 0 after, both summary lines verbatim in the report. `ast.parse` passes for every edited file.
`python -B <tree>/ai-packages/qa-factory/scripts/tests/test_driver_layers.py` exits 0 after. No other run; the full sets
are the wave's CI pipeline, and the wave is re-measured by the `test-redundancy` job (the covered product lines must not
drop).

## Report (the handoff file named in the dispatch), written BEFORE the final message

One table, a row per candidate: fate (folded / kept as the home of `<script>` / kept, doubt) | lines before -> after |
checks deleted as duplicates | checks moved (count -> home) | checks deleted by kind. Then per home: lines before ->
after and the two summary lines. Then `moved:` — one line per moved check: `candidate::check -> home::case`.
`doubt:`, `red before:`, `registry rows:` (each may be `none`). Totals: lines deleted, lines added, the ratio. The commit
hash. Nothing else.

Commit message: subject `tests: fold <first file> .. <last file> into their homes (test-diet <node id>)`, then the lines
`architecture: none -- test files only`, `judgment: none -- no package check changed`,
`axes: not a mechanism (test folding under docs/TESTING.md)`,
`piles-skip: <node id> -- the owner's word 10.11.2026, docs/tasks/test-diet.md`, `[F15]`.
