# t-1428 critic-entry: RH1-9 diff review (one "same test" comparator; the proof_stale/review_stale reader removed)

Diff under review: worktree `.claude/worktrees/agent-aee2405c6cae14809`, commit `8fdf9550` (12 files, +615/-38).
Spec/DoD: `docs/tasks/specs/t-1424-rh1-9-same-test-predicate.md` (§1-§12). Plan review: `docs/tasks/specs/reviews/t-1423-rh1-9-plan-critic.md`.
Builder report: `docs/tasks/handoffs/t-1428-rh1-9-same-test.md` (in the worktree).

**Verdict: fit_with_fixes. 0 blockers, 3 minors (fix before merge: m1, m2; m3 queue/accept).**

## 1. Does every site keep its answer except where the spec changes it on purpose?

I traced each changed site against its OLD body (from `git show 8fdf9550`) and then ran an empirical equivalence check wider than
the builder's (values `""`, `None`, `"a"`, `"b"`, `" "`; scratch script
`C:\Users\DEV1~1\AppData\Local\Temp\claude\D--ws-yml-text-factory\3a3f60aa-3a8b-52a4-814e-0cd29a5e1e07\scratchpad\kr1x.py`,
imports the worktree modules and copies the old bodies verbatim).

| Site | Old vs new | Result |
|---|---|---|
| `proof_level.same_test` rule 1 | `_kept` guarantees a non-empty code sha on both sides, so `compare_identity` always decides by rule 1. content equal + code equal -> `instance` (both); content differs + code equal -> `instance_code` (both); content absent on one side + code equal -> `instance_code` (both); content equal + code differs -> old `instance`, new `""` | only E2 changes (intended, F2); direction: new answer is "not same" = safe |
| `execution_request.same_instance_bytes` | 5^4 = 625 inputs: 4 diffs are exactly E2 (old True, new False); 45 others all involve whitespace-only values (old True, new False). **New True where old False: 0** | intended E2 + M2 strip; no new false "same" |
| `run_history._compare_shas` | `""/"a"/"b"` over 6 fields (729): 0 diffs (builder's K-R1, I re-ran it: 22/22). With `None` added and no whitespace: 0 diffs. All 5125 diffs in the wider space contain a whitespace-only value | equal on every realistic input; see m3 for the whitespace corner |
| `acceptance.green_on_current_bytes_why` | `same_test({"input_hash": X}, {"input_hash": raw}) != "raw"`: rule 1/1b inert (no identity on either side), rule 2 compares `str(...)` non-empty equal; `raw` is non-empty by the `_raw_record` filter; empty/None `input_hash` -> `""` -> not green, as before | identical |
| `acceptance._raw_record` | Windows: `normcase` -> case-sensitive (E12, intended). POSIX: was already case-sensitive. NEW un-named delta: `same_path` is a SYMMETRIC tail (`b.endswith("/"+a)` too), the old rule was one-way (recorded ends with manifest). Traced reachability: the recorded `path` is always `str(Path(given).resolve())` (`execution_fingerprint.py:168`), absolute; the manifest path is project-relative (`proof_level.test_file_of`), so "manifest ends with recorded" needs an absolute manifest path with a foreign prefix - not produced by any writer I know. Not a finding; noted | intended + one unreachable delta |
| `acceptance._instance_test_file` | old: first row with exact id OR alias. New: exact id first; alias only when exactly one row carries it. Direction of the change: an alias shared by 2+ rows of the SAME file now names no file -> `_raw_record(request, "")` -> single-test-file branch or a refusal with a reason: false "different", safe, spec E6 says 2+ -> `""` | intended (E6) |
| `run_history._job_contract` | 0 -> `{}`, 1 -> it, 2+ -> first only with equal non-empty code AND content, else `{}` (was: first) | intended (E5); see m2 for HOW it compares |
| `proof_level._mutated_files_hold`, `node_selects_row` | `_same_path` -> `same_path`, body unchanged | identical |
| `check_delivery.case_version_reasons` | reader removed. AR-22 grep, my own: `grep -rni "proof_stale\|review_stale"` over the worktree package -> 0 lines; same command shape, `sensitivity_proof` in `check_delivery.py` -> 3 (positive control) | intended (F1=A); no writer existed |

Error direction per site: no changed site moves a realistic input from "not same" to "same". The only "toward same" flips are in
m3 (whitespace-only shas, not produced by any writer).

## 2. K-R1's 729-combination check: against the OLD body honestly?

Yes. `before_rh1_9` in `test_run_history_identity.py` is the deleted body verbatim (loop over `("code","raw","file")` ==
old `SHA_FIELDS_ORDER`, same truthiness test, same `_first_sha` tail) - compared line by line with the `-` side of the diff.
The product of `("", "a", "b")` over six fields is 729 and includes code-equal/raw-different, code-different/raw-equal (E2) and
one-sided cases. Its blind spot is whitespace (named by the builder as deviation 4); my wider run closes `None` (0 diffs).

## 3. Deviation 1 (K-C (a) list filled in) - fine

The branch carries N1-N4 in one commit, so E13's temporal edge (N1 merged before N2-N4) does not exist here; an empty list would
leave (a) checking nothing after the merge. The check reads attribute calls (`PL.compare_identity`, `proof_level.same_test`),
and all three sites call through an attribute - verified in the diff. Its error is "red on a bare-name import" (safe).
Lead: drop the M9 integrator step for this node.

## 4. Deviation 2/3 (patching `os.path` directly) - does the test still prove the Linux case?

The "as is" pass proves the Linux case for the CURRENT code: `same_path` is pure string logic, no `os` use, so the four K-P rows
are OS-independent. The ntpath pass is meant as the kill of the `normcase` mutant on Linux (plan-critic B3). It does kill it,
but NOT by the row the report names. Simulation of the mutant on Linux (`mut.py` in the same scratchpad; old rule copied
verbatim, `os.sep` = "/" because the test patches only `os.path`):

```
linux as is                                   row1 ok   row2 ok  row3 ok  row4 (E12 case) ok
linux os.path=ntpath, os.sep='/' (the test)   row1 RED  row2 ok  row3 ok  row4 (E12 case) ok
os.path=ntpath AND os.sep=backslash           row1 ok   row2 ok  row3 ok  row4 (E12 case) RED
```

So on Linux the mutant dies on row 1 ("a recorded Windows absolute path ends in the manifest's POSIX relative one") because
`ntpath.normcase` emits backslashes while `os.sep` stays "/" - an artifact of a half-patched environment, not the case rule.
The E12 row, which the report's killer list names, passes the mutant on Linux. On Windows the "as is" pass kills it on row 4.
-> m1.

## 5. Census sites in owns left untouched?

§2 B1-B4, N-a, N-b, N5, N1 items 1-5, N3 items 1-3, N4 items 1-4: all present in the diff (module header lines, F5 ACCEPTED
RISK docstring, `_bound_to` docstring (vii), `SHA_FIELDS` comment, CHANGELOG fragment). `_same_path` has no caller left
(`grep -rn "_same_path("` -> only `sizing.py:410` and `tests/driver_trace.py` local functions of their own, both queued
in spec §9 / finding F6). Nothing in owns untouched.

## 6. DUPLICATION

- dup ratchet (my re-run, worktree): `scripts: 12 groups, 10 known, 0 new, 0 grown, 2 carried, 3 shrunk/gone`; `tools: 16 known,
  0 new`; exit 0.
- m2: `run_history._job_contract` (`run_history.py:218-220`) decides "these contracts carry the same test identity" with its own
  set-of-`str()` comparison of `instance_code_sha`/`instance_content_sha` - a second implementation of exactly the comparison
  the node makes the one (`proof_level.compare_identity`, `proof_level.py:811`), inside one of the four sites RH1-9 converts.
  The K-C (b) census does not see it (a set comprehension, not `==`/`!=` on a subscript/`.get`) - a further blind spot of the
  detector beyond the "local variables" one the test names. Behaviour is equivalent today (no strip vs strip only).
- Path-rule twins (`execution_request._same_file`, `probe_by_code._same_file`, `sizing._same_path`, `driver_trace._same_path`):
  queued by spec §9 / finding F6 (Lead at integration). Not a finding.
- `_compare_shas` re-derives "did rule 1 decide" with its own strip (`run_history.py`, the `basis = "code" if all(...strip())`
  line) - spec N3 item 1 prescribes this mapping; consistent with `compare_identity`'s normalisation. Not a finding.

## 7. CODE QUALITY

- No new production function over 60 lines or 3 nesting levels (`compare_identity` 30 lines, `_job_contract` 20).
- Test functions `rh1_9_compare_identity` (`test_proof_level.py:1272-1390`, ~118 lines) and
  `rh1_9_the_file_of_an_instance_and_its_bytes` (`test_acceptance_semantics.py:507-584`, ~78 lines) exceed 60 lines; each is a
  sequence of independent key blocks (K-A/K-B/K-N/K-C). Severity: queue (splitting per key would also name the failing key in the
  traceback).
- `acceptance._raw_record` docstring (`acceptance.py:101`) still says "matched on the recorded absolute path's tail"; the rule is
  now `same_path` (either side's tail). Harmless wording; fold into m1's round.
- No dead branches, no unread results found (read: every changed hunk).

## Findings

**m1 (fix before merge) - the ntpath pass kills the mutant on Linux by an artifact, not by the E12 row.**
`ai-packages/qa-factory/scripts/tests/test_acceptance_semantics.py:528-539`. Scenario: Linux CI, mutant "restore
`os.path.normcase`": row 4 (E12, `Tests/test_m.py`) passes the mutant; it is red only on row 1 because `os.sep` stays "/" under
the patched `ntpath`. If row 1 is ever edited the B3 kill silently disappears; the report's killer line (handoff :36) is wrong.
Fix: patch the separators together with the module, and restore all three in `finally`:
`real = (os.path, os.sep, os.altsep)`; in the ntpath mode `os.path, os.sep, os.altsep = ntpath, ntpath.sep, ntpath.altsep`;
`finally: os.path, os.sep, os.altsep = real`. With that, the simulation shows rows 1-3 ok and row 4 RED for the mutant (the
intended killer). Correct the killer line in the report.

**m2 (fix before merge) - a second identity comparison in a converted site.**
`ai-packages/qa-factory/scripts/run_history.py:218-220`. Fix: `if all(PL.compare_identity(found[0], c) == ("same", "content") for c
in found[1:]): return found[0]` (lazy `import proof_level as PL`, as `_compare_shas` does) - `("same", "content")` is exactly "code
non-empty and equal on both, content non-empty and equal on both". K-R2 rows stay as they are (they pin the behaviour).

**m3 (queue / accept) - whitespace-only shas.** `compare_identity`'s strip (spec M2) makes a whitespace-only sha "none". In
`_compare_shas` that can move a pair from `changed` to `same` via the `file` basis (644 of 15625 inputs in my run, every one with a
`" "` value; e.g. red `code=""/raw="a"/file="a"`, green `raw=" "/file="a"`: old `changed/raw`, new `same/file`). No writer produces
a whitespace sha (hex digests or `""`), so it is unreachable; the spec chose strip. Lead may accept as is; if not, drop `.strip()`
from `compare_identity.pick` (no realistic input changes).

## Rules walked

FR-16 n/a (no id stored); FR-18 n/a; FR-41/FR-59/AR-28: `unknown` is never folded to "same" except by
`_same_identity_for_count` (its line 2075, untouched; K-E5 passes); FR-45 n/a (no writer); FR-58: the comparator reads measured
shas only. AR-4: `same_path` OS-independent (string-only). AR-13/AR-15: four sites call the survivor (m2 is the remaining
duplicate inside one). AR-20: K-C exception list by name, an absent exception is red. AR-22: grep with control above.

## Class completeness

Class: "same test" identity comparisons and path-equality rules. Inside the artifact: all four B-sites, N-a, N-b converted;
`_job_contract` converted in behaviour but not in mechanism (m2). Map axes 7 and 25 (SIBLING_MAP): edits belong to Lead at
integration (spec §8) - not in this diff, still owed. Outside owns: B5 `window_record.probe_gap_block`, B6 raw-sha sites in
`probe_by_code`/`red_sandbox`, path twins (`execution_request._same_file`, `probe_by_code._same_file`, `sizing._same_path`,
`driver_trace._same_path`), `_split_node` - queued by spec as finding F6; E8 and F5 findings likewise owed by Lead.

## Trail

Read: the full diff `git show 8fdf9550` (all 12 files); the spec t-1424 (whole); the builder report (whole);
`proof_level.py` `_kept` :780-784, `same_test` tail :878-884, `test_file_of` :513-523; `execution_request.py`
`_same_identity_for_count` :2067-2075; `execution_fingerprint.py` :150-176; `acceptance.py` :95-120; `critic_verdict.schema.json`.
Searches: `_same_path\b|.same_path\b` over the package (callers); `acceptance.os` (no user left); `proof_stale|review_stale` -i
with `sensitivity_proof` control.
Re-runs (worktree): `test_run_history_identity.py` -> `=== test_run_history_identity: 22/22 ok ===`;
`test_acceptance_semantics.py` -> `PASS test_acceptance_semantics`; `tools/dup_ratchet.py --check` -> exit 0, 0 new / 0 grown;
`kr1x.py` (equivalence over None/whitespace, mine); `mut.py` (normcase mutant simulation, mine). Not re-run: test_proof_level,
test_execution_request, test_check_delivery, selftest --limits --lang (builder witness; consistent with the diff - each new key
block is called from its file's `main`).

Decision on acceptance belongs to the Lead.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "m1 test_acceptance_semantics.py:528-539: patch os.sep and os.altsep together with os.path (ntpath.sep, ntpath.altsep) and restore all three in finally, so the normcase mutant dies on the E12 row on Linux, not on row 1 by a separator artifact; correct the killer line in the handoff (:36)",
    "m2 run_history.py:218-220: replace the set-of-str comparison with all(PL.compare_identity(found[0], c) == ('same', 'content') for c in found[1:]) (lazy import), so the one comparator decides E5 too",
    "m3 (queue or accept): whitespace-only shas become 'none' under compare_identity strip and can flip _compare_shas from changed to same via the file basis; unreachable (no writer emits whitespace); Lead accepts or drops .strip() in compare_identity.pick"
  ],
  "class_completeness": "All four B-sites and N-a/N-b converted; _job_contract converted in behaviour, not mechanism (m2). SIBLING_MAP axes 7 and 25 edits and findings E8/F5/F6 (B5 window_record.probe_gap_block, B6 probe_by_code/red_sandbox raw sites, path twins _same_file x2, sizing._same_path, driver_trace._same_path, _split_node) are owed by Lead at integration per spec section 5 DoD; not in this diff.",
  "trail": {
    "read": [
      "git show 8fdf9550 (12 files)",
      "docs/tasks/specs/t-1424-rh1-9-same-test-predicate.md",
      "worktree docs/tasks/handoffs/t-1428-rh1-9-same-test.md",
      "ai-packages/qa-factory/scripts/proof_level.py :513-523, :780-784, :878-884",
      "ai-packages/qa-factory/scripts/execution_request.py :2067-2075",
      "ai-packages/qa-factory/scripts/execution_fingerprint.py :150-176",
      "ai-packages/qa-factory/scripts/acceptance.py :95-120",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "python -B ai-packages/qa-factory/scripts/tests/test_run_history_identity.py", "result": "=== test_run_history_identity: 22/22 ok ==="},
      {"command": "python -B ai-packages/qa-factory/scripts/tests/test_acceptance_semantics.py", "result": "PASS test_acceptance_semantics"},
      {"command": "python tools/dup_ratchet.py --check (worktree)", "result": "exit 0; scripts 0 new 0 grown; tools 0 new 0 grown"},
      {"command": "scratchpad kr1x.py (old bodies vs new over '', None, a, b, whitespace)", "result": "_compare_shas: 0 diffs without whitespace; same_instance_bytes: 4 E2 diffs, 45 whitespace diffs, 0 new-True"},
      {"command": "scratchpad mut.py (normcase mutant on Linux)", "result": "builder patch: row1 RED, E12 row ok; with os.sep patched too: E12 row RED"},
      {"command": "grep -rni proof_stale|review_stale over the package; control sensitivity_proof in check_delivery.py", "result": "0 lines; control 3"}
    ]
  }
}
```
