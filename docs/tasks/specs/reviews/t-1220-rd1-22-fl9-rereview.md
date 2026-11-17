# t-1220 — re-review of the FL9 fix round, RD1-22 (commits 5d0de450, c1d2b296, t-1188)

Scope: `git diff 6d05f3fd..c1d2b296` on branch `worktree-agent-ad30c6b4429bfe57a`, checked against findings F1-F8 and the
siblings of the t-1181 verdict (`docs/tasks/specs/reviews/t-1181-rd1-22-fl9-code.md`). I did not re-judge anything that
verdict says holds. The branch canon is read by the Lead.

## Verdict

**FIT WITH FIXES.** No finding blocks. F1-F6 and F8 are fixed, and so are the three sibling lines. F7 is answered with a
stated reason; the Lead judges whether it holds. Three small fixes are left for this round (N1-N3). N1 is the only one
of substance: no test drives the three sibling lines, so a revert of any of them would pass every test.

## Per finding

- **F1: fixed** (the Lead's option (c), a new manifest_put door). `manifest_put.py::open_oracle_fragment` builds
  `{"claim_then_pairs": [{case, then}], "then_bindings": [<the open row>]}`. `_claim_then_pairs` runs inside `_merge`
  before the `then_bindings` merge. It drops every row of the pair (case, Then) whatever the instance, so a unit's only row
  goes too: this was the case that failed in my probe 2 of t-1181. The removed rows go into `trail["then_claimed"]`, and
  `removed_then_lines` prints them. The claim key sits in `SCALAR_EXEMPT`, so it is not stored (a test checks this).
  `claim_pair_problems` refuses an unknown case or a bad Then number in `run`, before the commit, and names the door.
  `merge` stays pure and tolerant, so replaying an old journal still works.
  - Driven by `fl9_open_oracle_door_claims_the_pair`: unit-only, two-instance and no-row stories, the refusals, and a
    `Stand` run through `run` that ends with only the open row in the projection.
  - Driven by `open_oracle_door_for_a_non_python_story_closes_the_gate`: through `P.run`, the gate goes silent with no
    covered Then-2 row left.
- **F2: fixed.** `_open_oracle_door` puts `qa(then=[n])`, `# oracle_unknown` and "re-run manifest_from_tests.py" inside
  the marker branch only. The manifest_put branch names a `then_bindings` row for the established part. The table checks
  all three Python tokens per row, and they appear exactly when the marker form does.
- **F3: fixed at the door** (`_road(task_name)`, and `--task {task_name}` on `--open-oracle`). The builder also moved the
  ghost-row, pending-leftover and C2 lines to `_road(task)`. The class is not complete: see N2.
- **F4: fixed.** There is a public `assertion_detectors.binding_form(test_file, path) -> (form, note)`. `_document` is now
  called only inside `assertion_detectors.py`. A key it cannot use gives `''` plus a note naming the key. `_marker_form`
  appends that note to `notes` once (`binding forms: ...`), the way `_baseline_tokens` does. `run` passes `notes` into
  `check_manifest`, which feeds the partial-green line. The reader test has 12 rows, covering absent, empty, no-form,
  non-object and unreadable keys, each with a note.
- **F5: fixed.** No `observed` key unless `--observed` is given (a test checks this). The door text says "add
  `--observed` with that value, never a guess".
- **F6: fixed.** One story goes through `P.run` with `tests[].file = tests/XTests.cs`. It asserts the `--open-oracle`
  door with the task filled in, no `qa(then=`, and the gate silent after the door's fragment is merged.
- **F7: answered, for the Lead.** The table stays separate, and its note says why: "the door knows the TEST FILE while a
  runner entry is keyed by runner". The reason holds only in part. The `assertion_probes` rows carry `suffixes` too
  (`detectors.json` `assertion_probes.csharp.suffixes: [".cs"]`), so the drift risk named in t-1181 (two rows in two
  tables) is still there. It is non-blocking, as before. Whether this reason is enough is the Lead's call.
- **F8: fixed.** `_binding_files` matches through `C.instance_id_aliases(e, cfg)` and now returns the files of EVERY
  asserting instance. A test checks that a row bound as `TC-500::<iid>` finds `tests/XTests.cs`. The t-1181 note on
  "multi-instance takes the first file" is fixed too: `_marker_form` gives the marker only when every file shares one
  form, and a mixed `.py`+`.cs` row in the table gets the manifest_put road.
- **Siblings :1189 / :1607 / :4562: fixed in code.** Each line now picks its text through `_marker_form(_files_of(...))`:
  partial-green, the malformed handed_to_person remainder, and the C5 shape. The manifest_put branch names the row's
  fields and `_road`. **Not tested at any site:** N1.

## New findings (fix this round, none blocking)

**N1 (rule 20 / Q5(c)): no test drives the branch choice of the three sibling lines.**
- Surface: the repair text of `check_manifest` partial-green, `check_then_remainders` shape-malformed and `_Window.c5`.
- The only sibling check is `P._marker_form(["a.py"])` / `(["A.cs"])`, a call to the helper alone.
- Searched every file under `scripts/tests/` (case-insensitive): no match for `rewrite the row`, `with the planned`,
  `handed_to_person, .owner. and`, `rewrite the marker` or `tag the test with the planned`.
- Positive control: the same search finds `goes back to S4` in `test_s5_precheck.py:2035, 2056`.
- So putting back today's fixed marker text at any of :1190, :1611 or :4569, or swapping a branch, passes every test.
- Fix: one table row per site with a `.py` and a `.cs` file, each asserting that the marker text or the manifest_put row
  wording appears exactly where expected. That means at most 6 rows in one parameterised check.

**N2 (Q6, the F3 class): the sweep matched `FRAGMENT_ROAD`, not `<T>`, so three hand-typed copies of the road remain.**
- `s5_precheck.py:1948`, in `check_case_is_oracle` (no task parameter): `manifest_put.py --task <T> --fragment '...'`.
- `:3179`, in `helper_twin_hint`, which has `task_root`.
- `:3185-3186`, `COPY_KEEP`.
- Also, the new partial-green line at :1193 uses `_road()` (`<TICKET>`), although `check_manifest` gets `store_root`
  from `run`. The other `_road()` calls in that function do the same, so it is consistent with its neighbours but leaves
  the slot open where the task is known.
- These copies were there before this branch, but they belong to the class this round named (F3: a door that leaves the
  task slot open, and copies of the road outside the one helper).
- Fix: route all of them through `_road(...)`. Pass the task where it is in scope, and keep the `<TICKET>` slot where it
  is not. One helper, one spelling (AR-15).

**N3 (error direction of the door's wording): the manifest_put door does not say the order of its two steps.**
- The text: "bind it with `manifest_put.py ... --open-oracle ...` (one call: it takes every proof row of Then n out ...),
  keep an assert only for the part a source establishes and bind that part with a `then_bindings` row of its own ... sent
  through `<road>`".
- Concrete trace: an author sends the part row `(TC-500, 2, X, covered, assertion_ref)` first and runs `--open-oracle`
  second. `_claim_then_pairs` then drops the part row too, since it drops every row of the pair. The manifest ends with
  only the open row, and the gate skips declared Thens (`number in declared`), so nothing refuses it.
- `run` prints the removed line, so this is not silent, but the established part loses its binding.
- The marker road has no such order issue: the writer writes both rows from the file on every run.
- Fix: say it in the text, e.g. "first ... --open-oracle ...; after that call, bind the part a source establishes ...".
  A re-run of `--open-oracle` also drops the part row, so "after" is the rule.

## Standing questions (critic rules 18-20)

- **DUPLICATION AND CONSISTENCY:** N2. Otherwise none found. Searched for `_document(` (only in `assertion_detectors.py`
  now), `FRAGMENT_ROAD`/`_road(`/`<T>` over `s5_precheck.py`, `instance_id_aliases` in the new reader, and
  `claim_then_pairs` / `retracted_provisional` over the package (claim lives in `manifest_put.py`, its test and the
  changelog fragment). F7's second suffix map is left to the Lead.
- **CODE QUALITY:** none blocking. New functions are under 30 lines with nesting of 3 or less. The `a and b or c` at
  :1190 is safe, because `b` is a non-empty literal.
- **ONE ROAD (P31):** the door, the three siblings and the fallback all choose by one reader and one data row. No
  language name appears in code; the code reads only `Path.suffix` and the row. A mixed-kind Then gets the road every
  kind can use. No exclusion without a data row.
- **TESTS (rule 20):** the diff adds 135 test lines (19 removed) against about 202 product and doc lines, so no
  `tests-over:` is owed. Coverage gap: N1.
- Hygiene: 337 added lines, 0 CRLF. The 2 non-ASCII lines are em dashes in the generated slice `index.md` lines, the
  same style as the generator's existing lines. There is no Cyrillic.
- Architecture: the commits name AR-1, AR-9, AR-13, AR-15, AR-22 and AR-28. That covers the t-1181 Q10 request (name
  AR-13 and AR-28).
- Doc trim: the contract line lost "and the fragment to send" to stay under the role-load headroom. The refusal still
  names its fragment in code, so nothing load-bearing is lost. The slices were regenerated, and the control re-run below
  confirms they are fresh.

## Trail

- Read: `git diff 6d05f3fd..c1d2b296` for `s5_precheck.py`, `assertion_detectors.py`, `manifest_put.py`,
  `detectors.json`, `artifact-contract-automation.md`, the census, all three test files and the changelog fragment;
  `git log -2` (both commit messages).
- Read in the worktree: `s5_precheck.py` 664-666, 900-915, 1030-1060, 1160-1180, 1560-1575, 1935-1952, 3153-3188, plus
  the grep for the `matched`/`self.notes` sites; `manifest_put.py` 1714-1736 and the `SCALAR_EXEMPT` use at :2091;
  `contract.py::instance_id_aliases` 4075-4090; `design/state-exits.md` rows mentioning `then_bindings`.
- Re-runs, verbatim tails:
  - `python -B <wt>/ai-packages/qa-factory/scripts/tests/test_contract_slices.py` printed
    `=== contract slices (markup, generation, freshness, shipped map): 531/531 ok ===`. This is the control the
    dispatch asked for, after the slice regeneration.
  - `python -B -c` importing `test_manifest_put_merge.fl9_open_oracle_door_claims_the_pair`,
    `test_s5_precheck.open_oracle_door_is_chosen_by_the_binding_file` and
    `test_s5_precheck.open_oracle_door_for_a_non_python_story_closes_the_gate` (the worktree's scripts and tests on
    `sys.path`): 100 `PASS` lines, and no line other than `PASS`.
  - The hygiene count was a python pass over the diff: `added 337 crlf 0 nonascii 2`. The two non-ASCII lines are the
    slice `index.md` em dashes.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "N1 test_s5_precheck.py - the three sibling lines (check_manifest partial-green s5_precheck.py:1190, check_then_remainders shape-malformed :1611, _Window.c5 :4569) choose marker vs manifest_put text through _marker_form, but no test drives any site (only _marker_form alone); add one parameterised check, a .py and a .cs row per site, asserting the text of each branch",
    "N2 s5_precheck.py:1948, :3179, :3185-3186 - hand-typed copies of manifest_put.py --task <T> --fragment remain outside _road (the F3 class; the sweep matched FRAGMENT_ROAD, not the literal); the new partial-green line :1193 uses _road() though check_manifest has store_root; route all through _road with the task where in scope",
    "N3 s5_precheck.py _open_oracle_door manifest_put branch - say the order: the --open-oracle call first, the established-part then_bindings row after it (the claim drops every row of the pair, so a part row sent before, or a re-run of --open-oracle, removes the part's binding while the gate skips declared Thens)",
    "F7 (Lead decision, non-blocking) - the separate oracle_binding_forms table is kept with a reason (door keyed by test file, probes keyed by runner) that holds only in part: assertion_probes rows carry suffixes too, so the two-tables drift risk stays; the Lead accepts the reason or asks for the capability field"
  ],
  "class_completeness": "F1-F6, F8 and the t-1181 siblings s5_precheck :1189/:1607/:4562 are fixed; the F3 class (task slot left open / road copies outside _road) has three hand-typed residues at s5_precheck :1948, :3179, :3185-3186 in this pile's file (N2, fix this round); axis 34 (one road): one reader and one data row decide every site, no language name in code; axis 5 assertion-probe overlap stays as F7 for the Lead.",
  "trail": {
    "read": [
      "docs/tasks/specs/reviews/t-1181-rd1-22-fl9-code.md",
      "git diff 6d05f3fd..c1d2b296 (worktree agent-ad30c6b4429bfe57a), all 14 files",
      "git log -2 --format=%B (commits 5d0de450, c1d2b296)",
      "ai-packages/qa-factory/scripts/s5_precheck.py:664-666,900-915,1030-1060,1160-1180,1560-1575,1935-1952,3153-3188",
      "ai-packages/qa-factory/scripts/manifest_put.py:1714-1736 and SCALAR_EXEMPT use :2091",
      "ai-packages/qa-factory/scripts/contract.py:4075-4090 instance_id_aliases",
      "ai-packages/qa-factory/design/state-exits.md then_bindings rows"
    ],
    "reruns": [
      {"command": "python -B <wt>/ai-packages/qa-factory/scripts/tests/test_contract_slices.py", "result": "=== contract slices (markup, generation, freshness, shipped map): 531/531 ok ==="},
      {"command": "python -B -c importing fl9_open_oracle_door_claims_the_pair, open_oracle_door_is_chosen_by_the_binding_file, open_oracle_door_for_a_non_python_story_closes_the_gate (worktree scripts on sys.path)", "result": "100 PASS lines, no other output"},
      {"command": "grep -rniE over scripts/tests for the three sibling-line texts, positive control goes back to S4", "result": "no match for the sibling texts; control found test_s5_precheck.py:2035, 2056"},
      {"command": "python over git diff 6d05f3fd..c1d2b296 (CRLF / non-ASCII in added lines)", "result": "added 337 crlf 0 nonascii 2 (generated slice index em dashes)"}
    ]
  }
}
```
