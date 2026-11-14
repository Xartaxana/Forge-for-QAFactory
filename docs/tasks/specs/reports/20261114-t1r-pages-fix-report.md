# T1r-pages fix round report (task t-722, attempt 2, branch wip/tbw-t1r)

Status: DONE for Q1 (K5/real green) and Q3 (wording is data, pages byte-equal), A22 baseline table present. K10 stays red for
exactly the three STOP roles (expected, non-goal). One thing to read: the census narrowing needed three dense-ratchet ceilings
lowered by 1 (section 2) - it was not a refusal, but the spec said STOP on a refusal, so it is stated here.

## 1. What was done

- Q3 (data): `references/stage-joints.json` has a second top key `call_index_wording` (one wording per listed family, `{n}` = row
  count, `{scripts}` = the `<script> --help` list). `scripts/stage_joints.py`: `WORDING_KEY`, in `TOP_KEYS`; `call_wording(data)` is
  the one loader; `call_families` returns only listed families that have a usable wording (a family with none stays on the page: its
  rows are never in neither carrier); `_shape_problems` rows: a listed family with no wording, a wording for an unlisted family, an
  empty or non-string wording, a non-object key (each names the family). `scripts/contract_slices.py`: the code table `CALL_*`
  is gone; only the frame `CALL_LINE = "- [{family}:*] {words}"` stays; `_call_index_lines(wording, families, rows)` reads
  `stage_joints.call_wording(data)`.
- Q1 (a): `test_stage_joints.py::told_world` maps the literal `exit_gate:required_outputs` to the unit
  `exit_gate.py::required_outputs_errors` (the walk's mapping of every other literal to `all_errors` is unchanged);
  `judgment-census.json` row of `required_outputs_errors`: `roles` narrowed to the 10 the row names (qa-automator, qa-case-designer,
  qa-code-critic, qa-doc-scribe, qa-failure-analyst, qa-requirements-tester, qa-retro-analyst, qa-runner, qa-scout,
  qa-test-strategist) with a `note` (qa-bug-reporter is in no stage's required outputs; qa-case-critic is the row's declared
  producer-attribution gap). `conductor` is also gone from that row's roles (the spec lists 10 qa- roles; conductor is not one).
- Tests (existing files only): `test_stage_joints.py` rows `T1rp/call-wording/{real,unusable-sleeps,missing,unlisted,empty,not-text,
  not-object,absent}`; the `empty-green` row now empties the wording too (an empty family list with a leftover wording is a
  shape problem by design); `test_contract_slices.py` fixture `joints()` carries the wording of the families it lists.

## 2. The census ratchet (verbatim) - fork for the Lead to read

After the narrowing `test_judgment_census.py` printed (dense ratchet, a SHRINK demand, not a raise):

```
FAIL test_c3_the_ratchet_is_dense_and_only_shrinks
  `blocking_per_role.qa-bug-reporter` is 152, below its ceiling 153: lower the ceiling to 152 (the ratchet is dense and only shrinks)
  `blocking_per_role.qa-case-critic` is 172, below its ceiling 173: lower the ceiling to 172 (the ratchet is dense and only shrinks)
  `blocking_per_role.conductor` is 760, below its ceiling 761: lower the ceiling to 760 (the ratchet is dense and only shrinks)
```

I read this as the ratchet accepting the narrowing and asking for the ceilings to follow (a shrink is its own move, AR-20 names
only raises) and lowered the three ceilings (`ratchet.blocking_per_role` in `judgment-census.json`: bug-reporter 153 -> 152,
case-critic 173 -> 172, conductor 761 -> 760). If the Lead reads it as the STOP the spec names, revert those three numbers and the
roles of the row (one hunk) - nothing else depends on them. The conductor line is the one side effect to look at: keeping
`conductor` in the row's roles would leave that ceiling at 761.

## 3. Pages byte-equal

`python -B scripts/contract_slices.py --write` -> `slices: 44 declared, 0 rewritten`; `git status --short references/slices | wc -l` -> `0`.
No page changed.

## 4. A22 baseline: first-start tokens per role

Measured by `python -B scripts/role_load.py --all --json` (field `tokens`; `process_tokens` differs by a constant per role and moves
identically). (a) = detached scratch worktree at `e8a5cf7` = the PARENT of the first T1r-pages commit `7ed7f10` (the merge of
origin/main into the branch, key pages as T1 left them; `git merge-base 7ed7f10 origin/main` is not it, main lacks the T1 key
pages); (b) = detached scratch worktree at current `origin/main` `fdc94d9`; (c) = this worktree now. Worktrees removed after.

| role | (a) pre-T1r-pages e8a5cf7 | (b) origin/main fdc94d9 | (c) now | now - (a) | now - (b) |
|---|---|---|---|---|---|
| qa-scout | 19682 | 15433 | 17184 | -2498 | +1751 |
| qa-requirements-tester | 17172 | 12670 | 14838 | -2334 | +2168 |
| qa-test-strategist | 20960 | 16921 | 19705 | -1255 | +2784 |
| qa-case-designer | 16438 | 13353 | 15170 | -1268 | +1817 |
| qa-case-critic | 22312 | 18296 | 21044 | -1268 | +2748 |
| qa-automator | 29511 | 20313 | 26767 | -2744 | +6454 |
| qa-code-critic | 25551 | 19568 | 23372 | -2179 | +3804 |
| qa-runner | 27977 | 16026 | 20127 | -7850 | +4101 |
| qa-failure-analyst | 27306 | 18769 | 22413 | -4893 | +3644 |
| qa-bug-reporter | 19282 | 14794 | 16654 | -2628 | +1860 |
| qa-doc-scribe | 22385 | 17971 | 20423 | -1962 | +2452 |
| qa-retro-analyst | 18091 | 14213 | 15828 | -2263 | +1615 |

Answer: T1r-pages did NOT make any role's start dearer than the branch state before it: every role is cheaper than (a), by 1,255
(strategist) to 7,850 (runner) tokens. Against origin/main (b) every role is dearer, by 1,615 (retro-analyst) to 6,454
(automator) tokens: the key pages T1 put on the branch cost more than main's state, and T1r-pages recovers part of that, not all.
Note: (b) is the main of now; the rows main had at the merge differ slightly (the report of round 1 quotes those).

## 5. Verification run (verbatim, from `ai-packages/qa-factory/` of the worktree)

```
### python -B scripts/stage_joints.py --check
stage joints: clean
### python -B scripts/tests/test_stage_joints.py
=== test_stage_joints: 334/334 ok ===
### python -B scripts/tests/test_contract_slices.py
FAIL T3a (h): ... K10 qa-test-strategist / qa-automator / qa-code-critic (plugin share over native-context headroom)
FAIL T3a (j): ... the same three K10 findings
FAIL keys/findings-clean: ... the same three K10 findings
FAIL SHIPPED: ... the same three K10 findings
FAIL CLI: --check exits 0 on the shipped package - ... K10
=== contract slices (markup, generation, freshness, shipped map): 421/426 ok ===
### python -B scripts/tests/test_judgment_census.py
=== judgment_census: 25/25 ok ===
### python -B scripts/tests/test_role_load.py
=== role_load (the one measure of a role's start load): 186/186 ok ===
### python -B scripts/selftest.py --limits --lang
PASS limits: SKILL.md / agents / references within size caps
PASS limits: every mandatory role rule of design/role-rules.json holds in its carrier
=== qa-factory selftest: 4/4 ok ===
```

The 5 failing rows of test_contract_slices are exactly the K10 rows of the three STOP roles (T3a (h), T3a (j), keys/findings-clean,
SHIPPED, CLI), as expected. K5/real is no longer in the failing list of test_stage_joints (334/334).

NEGATIVE control (the wording of `role_cli` removed from the data - its key renamed to a probe key; byte copy first):

```
sha256 before: 197084a8ad6febf9e4a3... (original == copy)
python -B scripts/stage_joints.py --check
REJECT - 2 finding(s):
- stage-joints.json `call_index_wording` has no wording for the listed family `role_cli`
- stage-joints.json `call_index_wording` has a wording for `role_cli_REMOVED_PROBE`, which `call_told_families` does not list
exit 1
sha256 after restore from the byte copy: 197084a8ad6febf9e4a3... (equal)
```

(A first attempt of the probe broke the JSON by a trailing comma - `UNREADABLE: stage-joints.json is not valid JSON` - and was restored
from the same copy before the run above.)

## 6. Siblings, deviations, beyond the manifest

- siblings: axis 32 (census): the one row of `required_outputs_errors` changed, no other row; AR-1: the family list and the index
  wording are both data now. Seen, not touched: other literals the walk maps to `all_errors` while another function produces them
  (`own(f(), "exit_gate:x")` pattern) are joined to `all_errors` in K5 the same way - only this one literal was found wrong.
- Deviations: conductor removed from the narrowed roles (section 2); `call_families` also filters on wording (not in the spec,
  needed so a family with no wording cannot move rows off the page with no index line).
- Needed beyond the manifest: `scripts/tests/test_judgment_census.py` (the ratchet text), `scripts/role_load.py` (baseline
  measure), `exit_gate.py` (the `own(..., "exit_gate:required_outputs")` site).
- FR walk: A - FR-1 shape rows name the family and what is expected; G - FR-30 package English (`selftest --lang` PASS), FR-32
  tests added; AR-1 (wording is data), AR-13 (one loader `call_wording`), AR-20 (three ceilings lowered, no raise), AR-22 (key
  written and read in one commit), AR-23 (empty list + empty wording is green).
- Not run: CI, pipeline, mutations, slow files.
