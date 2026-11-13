# t-259 — HF8-4 wave 2 diff review: P2, P3, P6 (one pass per topic, R13-g)

Critic (opus), 13.11.2026. Base `3910f15` (wip/hf84-p1). Under review:
- P2 `9219d02` (wip/hf84-p2): `controller.py`, `tests/test_red_window.py`, `changelog.d/hf8-4-p2.md` (+4/-8 in code).
- P3 `11207f2` (wip/hf84-p3): `s5_precheck.py`, `s7_pretriage.py`, `stage_status.py`, `changelog.d/hf8-4-p3.md`.
- P6 `556eb18` (wip/hf84-p6): `ledger.py`, `manifest_from_tests.py`, `tests/test_ledger.py`, `changelog.d/hf8-4-p6.md`.

DoD: spec `docs/tasks/specs/t-205-hf8-4-parts.md` §4 P2, P3, P6; forks §5 (F9 = (a), decided at t-220 «по рекомендации,
до слова владельца», journal line 585). Not re-reviewed: P1, P7-P11 (t-240).

This verdict is an input to acceptance. The decision to accept belongs to the coordinator of the proper tier.

## Verdict per part

| part | verdict | why |
|---|---|---|
| P2 | ACCEPT | All 4 change items of the DoD done. The load-time invariant holds. My re-run of `test_red_window` gives 195/195. |
| P3 | ACCEPT with one minor fix (finding 2) | All 5 change items done. The split matches the old code on 23,328 inputs (0 differences). My re-runs are green. |
| P6 | ACCEPT | All 4 change items done. The new row is red on the old `ledger.py` (red-first shown) and green on the new one. |
| all | acceptance condition (finding 1) | The builder witnesses for t-242 and t-243 are missing from the journal. |

## Findings

**1. NEEDS WORK, on the acceptance record: no builder witness for P3 (t-242) or P6 (t-243).** The dispatch sent me to
`logs/journal/dev1.jsonl` for these witnesses. That file has only the `delegated` lines (631, 632) and no
witness. I ran each part's named tests once as a cheap control (Trail, re-runs). Those re-runs cover the named files
only. They do not cover the full `scenario_walk.py --witness-for <owns>` set the DoD asks for. Fix: the coordinator puts
each builder's verbatim witness (the `--witness-for` output plus the runs it lists) into the `witness` field of the
`accepted` event for t-242 and t-243. Without a witness that event would be a `rejected` under the witness rule. My
re-runs back the witness up; they do not replace it.

**2. Minor (code quality, P3): `stage_status.py:178-182` is a comment left behind by its constant.** The paragraph
"The manifest's own reason for ... (contract.UNRESOLVED_REASONS) ..." described `RED_ON_PURPOSE`, which is now deleted.
The new sentence was appended to it. The block now stands alone, separated from `reds_on_purpose` by two blank lines, and
documents nothing. Fix: move the paragraph, with its new "ONE home ... imported inside the functions" sentence, into
the docstring of `reds_on_purpose` (`stage_status.py:185`), or put it directly above that `def` with no blank-line gap.
This changes no behaviour. PROJECT.md «Командная работа» p.9 says minor items are fixed in the node's fix round, not
deferred.

**3. Note, no fix: P3's commit subject says `(t-243)`, but its journal task is t-242.** Journal line 631 already
records the mislabel ("prompt said t-243"). History is not rewritten. The integrator should know that `11207f2`'s
"t-243" means t-242.

**4. Note, for the integrator (wave-1 territory): changelog fragment names differ.** P7 uses `hf84-p7.md`. P2, P3 and
P6 use `hf8-4-pN.md`. There is no conflict, because `changelog_assemble.py` takes every fragment. The names are only
inconsistent.

## Questions

### (1) Each part against its §4 DoD and edges

**P2**
- Change 1: `CONTRADICTS_WORD` and its 4-line comment are deleted (`controller.py:234-237` on the base). Done.
- Change 2: `names_contradicts` does `import contract` as the first statement of its body and returns
  `contract.CONTRADICTS_REQUIREMENT in blob` (`controller.py:520-526`). The except branch still returns False, so the
  error direction is unchanged.
- Change 3: `_s5_gap_problems` uses `CONTRADICTS_REQUIREMENT`. I traced the import: it comes from the function-local
  `from acceptance import (CONTRADICTS_REQUIREMENT, ...)` at `:7327`, in the same method. So the name is bound when
  `:7392` and `:7397` run.
- Change 4: row K1's spelling-equality check is deleted. The behaviour rows of `k1_the_reader_and_its_twin` stay. The
  test's own `RED_WORD = "contradicts_requirement"` (`test_red_window.py:331`) is a test-side pin of the value, which
  is legitimate.
- Load-time edge: `grep -n "^import contract\|^from contract\|^import acceptance" controller.py` returns nothing
  (rc=1). The positive control `^import event_store` finds 1 hit.
- No other reference to `CONTRADICTS_WORD` remains under `ai-packages/` or `tools/`. Hits are only in spec and review
  docs.

**P3**
- Change 1: `s5_precheck.py:110` reads `CONTRADICTS = C.CONTRADICTS_REQUIREMENT`. `C` is imported at load, at `:61`,
  before line 110. The alias stays, as §6-c requires.
- Change 2: the `check_row_fields` docstring now says "no dispatch, an unknown id, or a dispatch with no scope".
- Change 3: the split. See (3).
- Change 4: `s7_pretriage.CONTRADICTS` is deleted, and `:128` uses `C.CONTRADICTS_REQUIREMENT`. `C` is imported at load,
  at `:51`. An outside-reader grep for `RED_ON_PURPOSE|s7_pretriage.CONTRADICTS|PT.CONTRADICTS` over `ai-packages`
  and `tools` (non-md files) found 0 hits. The positive control is the grep in (2), which finds `s5_precheck.CONTRADICTS`.
- Change 5: `RED_ON_PURPOSE` is deleted. `reds_on_purpose` and the selftest block each do a function-local
  `import contract`. The module has no load-time `contract` import (its imports are at `:28-37`).
- Edge: `stage_status.py --selftest` exits 0 ("no violations"). That run goes through `reds_on_purpose` and the local
  import.

**P6**
- Change 1: `_case_picture` reads through `C.then_number` and drops 0 (`manifest_from_tests.py:1593-1596`). I checked
  the claim that this is behaviour-free in `_then_numbers` (`:636-645`): it raises on a bool, on a non-int, and on any
  value below 1. So every value that reaches `_case_picture` is an int >= 1, and `then_number` returns it unchanged. A
  `True` cannot reach it.
- Change 2: `_contradicts_requirement` returns `C.CONTRADICTS_REQUIREMENT`, and its docstring is rewritten. The lazy
  `import acceptance` is removed. That is safe: the old docstring worried that `stage_guard` would load `acceptance`
  through this module, and now nothing is imported here at all. `contract` is already imported at load, at `:75`.
- Change 3: `plan_row_state` uses `n = C.then_number(...)`, the condition `n and n in gaps`, and appends
  `(case, n, gaps[n])`. The order of evaluation changed, but `then_number` is pure, so nothing differs.
- Change 4: there is one parameterised table, and each id names its input. It has the rows the spec asks for
  (`2`, `"2"`, `" 2 "`, `True`), plus the adversarial edges `"02"`, `"²"`, `2.0`, `[2]` and `"x"`. Red-first is shown in
  my re-run: on the base `ledger.py`, `"2"`, `" 2 "` and `"02"` FAIL (`passed_green`), and the bool row also differs
  (the old code flags it). On the new code: 452/452.
- `gaps` keys are ints: `ledger.py:119-120` builds them from `then_oracle_states` with an `isinstance(..., int)` filter,
  which is the spec's non-goal. So `n in gaps` compares int to int.

### (2) One home (AR-13 / AR-15) after the three parts

I merged P2, P3, P6 and P7 in memory (tree `ecab6e0`). On that tree I ran
`git grep -nE "[\"']contradicts_requirement[\"']" -- 'ai-packages/qa-factory/scripts/*.py' ':!.../tests/*'`.
- It finds the definition `contract.py:84`.
- It also finds `check_delivery.py:2003`, `check_traceability.py:67`, `driver_stage_s7.py:44`, `gate_brief.py:4478`,
  `story_step.py:1614` and `traceability.py:931`. All six belong to P4/P5, which are not in this review.
- It finds no hit in any of the 6 product files P2, P3 and P6 touch. The positive control is the same grep: it finds
  the definition and the six P4/P5 sites.

Local then-number parses: on the same tree I grepped
`isinstance\([^)]*then[^)]*\), int\)|int\(b\[.then.\]\)` over the 6 touched product files. The only hit is
`ledger.py:120`, which reads code-produced oracle states and is a non-goal. The positive control is that same hit.

The remaining `then` reads in `ledger.py` and `manifest_from_tests.py` either already go through `C.then_number` or are
not parses:
- `ledger.py:150`, `:201`, `:904` and `manifest_from_tests.py:1649` only display the value (f-string or `str()`); none
  decides anything.
- `ledger.py:314` reads `then_remainders` rows (a non-goal).
- `ledger.py:670-675` reads code-built placeholder units.

### (3) P3's `_check_blocked_then` split: same behaviour (FR-4)

I traced it by reading:
- The order stays: shape -> seen -> target (no numbers, then Then not in numbers) -> ran -> same-instance conflict ->
  blocker.
- `_finding` (`s5_precheck.py:266-268`) always returns a non-empty dict, so `if target:` and `if finding:` are true
  exactly when the old code appended.
- `blocker_state(blocker)` is still called only after the conflict check, as before.
- In `_blocked_then_blocker`, the old `if/elif` became `if/if` with a `return` in each branch. That is equivalent.

I also ran a differential test. The old function (from `3910f15`) and the new one ran on the same 23,328 inputs:
- rows: then in {1, 2, 5, "2", True, None} x instance in {t1, "", t2} x blocker in {TC-9, "", x} x well-formed/malformed;
- numbers in {[], [1,2], [3]}; covered rows in 3 sets; groups in 2 sets;
- blocker_state in {unknown, not-red, ""}; ran in {none, Then 1 on t1}; seen pre-filled or not.

The result: **0 differences** in the findings or in the final `seen` set. All 7 outcomes occur:
`then-remainder-shape` 19440, `<none>` 2056, `then-remainder-unknown` 1512, `blocked-check-unknown` 112,
`blocked-check-not-red` 112, `then-remainder-conflict` 60, `blocked-check-ran` 36. No silent pass is introduced.

A note on coverage: the keep test `test_s5_precheck.py` (983/983) does not name the blocked-check tags. Those rows live
in the quarantined `test_mixed_then_precheck.py`. So the differential test above is the evidence for the split, not the
keep set.

### (4) P6: `then_number` on each input type; error direction in its new gate role (PROJECT.md package change 6(в))

I measured it on the P6 tree:

| input | then_number | old `isinstance(_, int)` |
|---|---|---|
| `2`, `1`, `10**12` | the same int | True |
| `0`, `-1` | 0 | True (but they never match a key: keys are Then numbers >= 1) |
| `"2"`, `" 2 "`, `"02"`, `"2\n"` | 2 | False |
| `"0"`, `" 0 "`, `"-2"`, `"+2"`, `"1_0"`, `""`, `"x"` | 0 | False |
| `"²"`, `"٢"` (Arabic-Indic 2) | 0 (the `isascii()` guard; `int("٢")` would give 2) | False |
| `None`, `2.0`, `[2]`, `{"2": 1}` | 0 | False |
| `True`, `False` | 0 | True |

In the ledger, 0 means "this binding flags nothing", which is the direction toward `passed_green`. Compared with the old
reader:
- Every input that used to flag still flags, except `True`. (`False` and values <= 0 never matched a key.)
- Every digit string now flags too. That is the AR-28 gain.
- The one input that loses its flag is `True`. That is fork F9, decided (a).

F9(a) relies on one premise. I checked it: `s5_precheck.py:1265-1266` builds `bound` and `recorded` with
`C.then_number`. So a row whose `then` is `True` covers no clause, and the precheck refuses the clause with "Then N of
... has no `then_bindings` row". The direction of the reused function's error is therefore stated in the spec (§4 P6
edges, F9) and backed by a gate upstream.

Residual: a manifest that never passes the S5 precheck, for example a legacy one, loses the accidental flag on
`True`. That is accepted under F9(a) and is not a finding here.

### (5) Merging

- Owned files do not overlap. P2: controller, test_red_window. P3: s5_precheck, s7_pretriage, stage_status. P6:
  ledger, manifest_from_tests, test_ledger. P7: planning_contract. Each part also adds its own changelog fragment.
- `git merge-tree --write-tree`, run one branch at a time: p2+p3 rc=0, then +p6 rc=0, then +p7 rc=0, with no
  conflicts. The merged tree differs from `3910f15` in 13 files, which is exactly the sum of the four parts. P7's base
  `c12c178` is an ancestor of `3910f15`, so the merge brings in nothing extra.
- No semantic coupling: none of the four parts reads a name another part removes. (`CONTRADICTS_WORD`,
  `s7_pretriage.CONTRADICTS` and `RED_ON_PURPOSE` have no outside readers, per the grep in (1).)
- To build the merge tree I made 2 unreferenced probe commit objects with `commit-tree`. No ref was moved, and gc will
  collect them.

### (6) Duplication, code quality, class completeness

- **DUPLICATION AND CONSISTENCY: none found.** I grepped the word literal and the alias names over `scripts/*.py`, and
  the then-parse forms over the touched files (see (2)). The new helpers `_blocked_then_target` and
  `_blocked_then_blocker` duplicate nothing: the old bodies were moved, not copied. `_contradicts_requirement` is now a
  one-line wrapper. The spec keeps it (§4 P6 change 2) because it has callers. That is consistent with the
  `PENDING_OUTCOME` alias precedent.
- **CODE QUALITY:** one minor item, finding 2 (the leftover comment). `_check_blocked_then` went from 77 lines to about
  55. The new helpers are short and each docstring names its error direction.
- **ARCHITECTURE:** the commits name AR-13 and AR-15 (P2, P3) and AR-13 and AR-28 (P6), which is the full set the
  diffs touch. I walked AR-13 from both ends: producer `contract.CONTRADICTS_REQUIREMENT` and `contract.then_number`, and
  their readers in the touched files, with the positive controls above. No second reader or writer was added.
- **JUDGMENT (AR-29):** no check changes class. `test_judgment_census.py` gives 22/22 on P3 and on P6. No census row
  was needed.
- **ONE ROAD (P31, axis 34):** the diffs add no exclusion of a language, project or case. They remove three ways of
  reading the word and one way of reading the Then number.
- **Class completeness (SIBLING_MAP):**
  - The word class is covered by P1-P5. P4 and P5 are still open (wave 2).
  - The sibling words (`blocked_by_env`, `handed_to_person`, `probe_gap`) and the reader twin (`json.dumps` substring
    in `s7_pretriage.py:128` and `driver_stage_s7.py:44`) are queued as F7.
  - The other `isinstance(then, int)` sites are queued as F5.
  - The six grown long functions, `ledger.plan_row_state` among them, are queued under F4.
  - Axis 5 (stage twins): n/a, no stage twin is changed.
  - Axis 18 (ratchets): no raise.
  - Axis 32 (census): unchanged, see JUDGMENT above.
  - Axis 34: see ONE ROAD above.
  - Axis 3 (release copy): n/a until release.
  - No other axis applies to these files.

## Trail

Read:
- the spec `docs/tasks/specs/t-205-hf8-4-parts.md`: §1-§4 (P1-P6), §5, §6, §8;
- the three diffs `3910f15..HEAD` and their commit messages;
- `controller.py` (`:225-237`, `:510-527`, `:7322-7400`, imports);
- `s5_precheck.py` (`:61`, `:110`, `:266-268`, `:1255-1275`, `:1392-1510`, and every `CONTRADICTS` use);
- `s7_pretriage.py` (`:51-60`, `:120-135`);
- `stage_status.py` (`:28-37`, `:170-200`, the selftest block);
- `ledger.py` (`:100-125`, `:679-700`, `:860-906`, every `then` read);
- `manifest_from_tests.py` (`:75`, `:636-645`, `:947-952`, `:1590-1600`, `:1640-1652`);
- `contract.py:228-246` (`then_number`);
- `test_red_window.py:331`, `:378-395`; the new `test_ledger.py` row;
- `logs/journal/dev1.jsonl` (t-241..t-244, t-220, F9);
- `docs/SIBLING_MAP.md` (the axis headings); `docs/tasks/critic-diff-brief.md` (items 6, 7, 10-12);
- `tools/critic_verdict.schema.json`.

Re-runs (verbatim tails):
- `python -B .../hf84-p2/.../tests/test_red_window.py` -> `=== red window: 195/195 ok ===` rc=0
- `grep -n "^import contract\|^from contract\|^import acceptance" .../hf84-p2/.../controller.py` -> empty, rc=1; control `^import event_store` -> 1
- `python -B .../hf84-p3/.../stage_status.py --selftest` -> `STAGE_STATUS SELFTEST: no violations (one line, counted not quoted, cap, need)` rc=0
- `python -B .../hf84-p3/.../tests/test_s5_precheck.py` -> `=== test_s5_precheck: 983/983 ok ===` rc=0
- `python -B .../hf84-p3/.../tests/test_s7_pretriage.py` -> `=== s7 pretriage: 441/441 ok ===` rc=0
- differential old/new `_check_blocked_then` (stdin python, loads both module copies) -> `cases=23328 diffs=0`
- `python -B .../hf84-p6/.../tests/test_ledger.py` -> `=== test_ledger: 452/452 ok ===` rc=0
- the new P6 row against the base `ledger.py` (stdin python) -> FAIL for `'2'`, `' 2 '`, `'02'` (`passed_green`) and for the bool row; ok for the controls
- `python -B .../hf84-p6/.../tests/test_manifest_from_tests.py` -> `=== test_manifest_from_tests: 521/521 ok ===` rc=0
- `python -B .../hf84-p3|p6/.../tests/test_judgment_census.py` -> `=== judgment_census: 22/22 ok ===` (each)
- `then_number` probe on 24 control values -> the table in (4)
- `git merge-tree --write-tree` p2+p3 -> +p6 -> +p7: rc=0 each, final tree `ecab6e0`, 13 files

Not re-run: `test_story_run_*` and `test_controller_*`, which CI judges. The full `--witness-for` sets of P3 and P6 are
the builders' (finding 1).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "Acceptance record: attach the builders' verbatim witnesses (scenario_walk --witness-for <owns> output plus the runs it lists) for t-242 (P3) and t-243 (P6) in their accepted events; the journal holds only their delegated lines, and the critic's re-runs cover the named tests only",
    "P3 stage_status.py:178-182: the comment left behind by the deleted RED_ON_PURPOSE floats over two blank lines; fold it, with its new ONE-home sentence, into the reds_on_purpose docstring (or directly above the def); no behaviour change"
  ],
  "class_completeness": "Word class: P2/P3/P6 leave no literal in their 6 product files (git grep on the merged tree, positive control = contract.py:84 plus the six P4/P5 sites still open in wave 2). Sibling words and the json.dumps reader twin are queued as F7; the other isinstance(then, int) readers as F5; grown long functions as F4. Axis 5 n/a, axis 18 no raise, axis 32 census 22/22 with no row needed, axis 34 no exclusion, axis 3 n/a until release.",
  "trail": {
    "read": [
      "docs/tasks/specs/t-205-hf8-4-parts.md sections 1-6 and 8",
      "git diff 3910f15..HEAD in hf84-p2, hf84-p3, hf84-p6 plus commit messages",
      "controller.py 225-237, 510-527, 7322-7400",
      "s5_precheck.py 61, 110, 266-268, 1255-1275, 1392-1510",
      "s7_pretriage.py 51-60, 120-135",
      "stage_status.py 28-37, 170-200, selftest block",
      "ledger.py 100-125, 679-700, 860-906",
      "manifest_from_tests.py 75, 636-645, 947-952, 1590-1652",
      "contract.py 228-246 then_number",
      "logs/journal/dev1.jsonl t-220, t-241..t-244",
      "docs/SIBLING_MAP.md axis headings",
      "docs/tasks/critic-diff-brief.md items 6, 7, 10-12"
    ],
    "reruns": [
      {"command": "python -B hf84-p2/.../tests/test_red_window.py", "result": "195/195 ok rc=0"},
      {"command": "grep ^import contract|^from contract|^import acceptance controller.py (control ^import event_store)", "result": "empty rc=1; control 1 hit"},
      {"command": "python -B hf84-p3/.../stage_status.py --selftest", "result": "no violations rc=0"},
      {"command": "python -B hf84-p3/.../tests/test_s5_precheck.py", "result": "983/983 ok rc=0"},
      {"command": "python -B hf84-p3/.../tests/test_s7_pretriage.py", "result": "441/441 ok rc=0"},
      {"command": "differential old vs new _check_blocked_then, 23328 inputs", "result": "diffs=0, all 7 outcome tags hit"},
      {"command": "python -B hf84-p6/.../tests/test_ledger.py", "result": "452/452 ok rc=0"},
      {"command": "new P6 row against base ledger.py", "result": "FAIL on '2', ' 2 ', '02' and the bool row; controls ok (red-first shown)"},
      {"command": "python -B hf84-p6/.../tests/test_manifest_from_tests.py", "result": "521/521 ok rc=0"},
      {"command": "python -B test_judgment_census.py on p3 and p6", "result": "22/22 ok each"},
      {"command": "git merge-tree --write-tree p2+p3, +p6, +p7", "result": "rc=0 each, 13 files, no conflicts"}
    ]
  }
}
```
