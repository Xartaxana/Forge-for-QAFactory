# t-247: diagnosis of the two reds on conv/wave-2 (critic, opus)

Subject: worktree `.claude/worktrees/conv-wave2`, branch conv/wave-2, head ddb7c6c. I changed no code. I ran the tests in my own scratch worktrees, which I have since removed (`git worktree prune`: 0 t247 entries left). conv-wave2 `git status --short` is empty.

Verdict line: **NEEDS WORK, 1 blocking finding (Red 1). Red 2 cannot be reproduced and has no culprit merge.** Acceptance of the branch is the coordinator's decision (rule 6).

---

## Red 1: `test_reinstall_equals_fresh.py` fails 110/112 after merging origin/main

### Witness (my runs)

```
python -B <scratch>/n/ai-packages/qa-factory/scripts/tests/test_reinstall_equals_fresh.py    # n = 9b66189
n rc=0
=== test_reinstall_equals_fresh: 112/112 ok ===

python -B <scratch>/d/ai-packages/qa-factory/scripts/tests/test_reinstall_equals_fresh.py    # d = ddb7c6c
d rc=1
FAIL stale-receipt reinstall: the apply ran the coverage check ONCE, with --ignore-receipt, and it passed (rc 0) — expected [('--ignore-receipt', 0)], got [('C:\\Users\\i_mas\\AppData\\Local\\Temp\\qa-reinstall-equals-fresh-7dzdfoc1\\k-stale', 0)]
FAIL stale-receipt reinstall: after the apply the receipt is gone from state/ and the retire record has it as deleted (what _retire does today) — expected (False, ['deleted']), got (True, [])
=== test_reinstall_equals_fresh: 110/112 ok ===
```
The ddb7c6c CI canon (run 43343938014, shard 1 artifact) shows the same two FAIL lines: `ci_read.py artifact 43343938014 package-full-shard-1/selftest-shard-1-of-2.txt`.

### Mechanism (traced)

- OH3-9 (on main, PR #5): `references/install-paths.json:89` makes `qa-factory/state/coverage-map.receipt.json` `"class": "carried"`, with the note "kept in place, never retired (owner, 22.10.2026)". The spec is t-167 §3.4. The `install_paths.py:59-61` invariant ("a carried path never appears in a retire listing", t-232) and `:260-264` (`"carried": "none"`, "whatever a data edit says") mean the receipt can never be in `listing["retire"]`.
- OH5-7 (8f40b43, merged 316baf8): `onboard_apply.py:1550-1554` passes `--ignore-receipt` only when `receipt_rel.casefold() in {listing["retire"]...}`. With the receipt carried, that condition can never be true. **The branch is dead code on this head**, and the new `check_coverage.py --ignore-receipt` flag (:230-231, :262-265) has no caller left.
- OH5-7 was built and accepted (journal t-202, `accepted` 23:33:10) on batch-5's base, which did not have OH3-9 yet. Its test `k_stale_receipt` (test_reinstall_equals_fresh.py:843-893) pins the pre-OH3-9 world: receipt retired and deleted. It contradicts the same file's `MACHINE_LOCAL_KEPT` (:109-111), which PR #5 moved the receipt into ("kept byte for byte"). The integrator's reading is correct.
- Why the first row reports rc 0 with no flag: the fixture receipt really does bind the fixture map. The reinstall moves `state/coverage-map.md` to `records/coverage-map.md` byte for byte (`_move_records`, lossless), so `map_sha256` still matches. The "stale" receipt in the apply part of the test is not stale; only the later `probe` copy zeroes `map_sha256`.

### (a) Carried or retired: **carried is right**

1. **Owner's word.** The OH3-9 spec §3.4 and the row's note quote the owner's 22.10.2026 decision. OH5-7's node (batch-5:37) never chose "retire". Its coordinator direction was "the check does not read a receipt of another package generation". Attempt 2 swapped that for "option c" (journal :551) because the receipt has no signature. Option c leaned on a retirement that OH3-9 had already removed.
2. **AR-25 / AR-21.** The install runs `check_coverage` without `--write` (onboard_apply.py:1548), so nothing in the install rebuilds the receipt. Retiring it throws away the map-to-cases binding with no producer to restore it. Keeping it hands the whole state on. The receipt's way out stays real: `check_coverage.py --write` rewrites map and receipt together (check_coverage.py:209-221).
3. **What a stale receipt must cause.** Evidence from history: the receipt's format and location have not changed since the initial import. `git log -S"map_sha256"`, `-S'max_updated"}'` and `-S"coverage-map.receipt.json"` on check_coverage.py each return only 9ac00f0. The reinstall also preserves the map's bytes. So **a reinstall never makes a receipt stale.** A receipt that disagrees after a reinstall already disagreed before it: the map or the cases changed without `--write`. That is a true fact about the project, and it is exactly what `check_coverage` exists to catch. So it must cause what it causes everywhere else: `check_coverage` reports REJECT. Inside the apply this is non-fatal. `_run_script` (:1355-1363) only records `{"ok": False, "rc": 1, "note": ...}` in the `regenerate` step, nothing reads `ok` to abort, and `out["applied"] = True` still lands. The receipt stays on disk byte for byte. Hiding the mismatch (passing `--ignore-receipt` on every reinstall) would let a known disagreement pass silently (AR-28, FR-4). The flag's own warning would also become false: it says "this reinstall retires it", and nothing retires it. B-248's original premise ("a stale receipt of an older generation") has no mechanism under the unchanged format. That fits B-248's own tag "needs a read: one live reinstall decides it".
4. **Not the owner's call.** The meaning (carried) is already the owner's word. What follows from it in the apply is technical, and AR-28 settles it.

### (b) The one fix: retire OH5-7's code path and rewrite its test to the carried world (OH5-7 fix round, same task t-202 or a new id per the coordinator)

- `ai-packages/qa-factory/scripts/onboard_apply.py`, `apply`, final phase: delete the B-248 block at :1549-1554 (the comment, `receipt_rel = ...`, the `if ... listing["retire"]` and `args = args + ["--ignore-receipt"]`). `check_coverage.py` then runs with `["--root", str(root)]` like the other scripts. Expected behaviour: the coverage check compares whatever receipt is there. rc 0 when it binds, rc 1 REJECT recorded in the `regenerate` step when it does not. The apply still completes and the receipt is kept.
- `ai-packages/qa-factory/scripts/check_coverage.py`, `main`: remove the `--ignore-receipt` argument (:230-231) and the `if args.ignore_receipt ...` branch (:262-265), restoring `if receipt_path.exists():`. A flag with no caller is a producer with no reader (AR-22).
- `ai-packages/qa-factory/changelog.d/oh5-7-stale-receipt.md`: delete it. It was never released, and its text describes behaviour that no longer exists.
- `scripts/tests/test_reinstall_equals_fresh.py`, `k_stale_receipt` (:843-893). Rows:
  - "apply ran the coverage check ONCE, with --ignore-receipt": **changes** to "the apply ran the coverage check ONCE, without --ignore-receipt, rc 0 (the carried receipt binds the moved map)". Expected `[(False, 0)]` from `[("--ignore-receipt" in c[1], c[2]["rc"]) for c in cov]`.
  - "after the apply the receipt is gone ... deleted": **changes** to "the receipt stays in state/ and is not in the retire record (carried)". Expected `(True, [])`. Byte equality is already proven by the `MACHINE_LOCAL_KEPT` check.
  - **new row**: copy the fixture, zero `map_sha256` in its receipt BEFORE `plan`/`approve_and_apply`, then apply. Expected: `done["applied"] is True`, the `regenerate` step's `check_coverage.py` run has `rc == 1` and a note naming REJECT, and the receipt file is byte-identical to what was put there. This is the stale-receipt reinstall: reported, not hidden, not deleted.
  - "WITHOUT the flag the stale receipt is still a REJECT": **kept**, relabelled "a stale receipt is a REJECT".
  - "WITH the flag: rc 0, one warning ...": **deleted** (the flag is gone).
  - "fresh-receipt precondition" and "fresh-receipt ... REJECT": **kept**.
  - "flag-no-receipt": **deleted**. A missing receipt is OF4-3's row (onboarding-forge/4), not this one.
  - Expected count: 111/111 (112 - 2 deleted + 1 new; the 2 changed rows stay).
- Witness scope: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <the three owns>`; at least the run above must reach 111/111.
- Pile carriers (Lead's action, not the builder's). The OH5-7 row in batch-5 Живые доказательства ("REJECT нет, retire выполнен", :58) and its live-runs copy now state the wrong expectation. Rewrite them as: "live reinstall over a receipt that disagrees with the map: apply completes, the regenerate step reports the coverage REJECT, the receipt is kept". The OF4-3 finding's §2 ("единственное лекарство — OH5-7") is also overtaken. Its dependency line `очередь: onboarding-hooks/5 → onboarding-forge/4` stays valid, since both still write `check_coverage.py`. B-248's closure note should say "closed by OH3-9 (carried) + this fix; premise unreproduced".
- Architecture to name in the fix commit: AR-25 (way out = `--write`), AR-28 (no silent pass), AR-22 (flag removed with its only caller).

---

## Red 2: `test_controller_rework_repair_binding.py` failed 234/235 on CI at 9b66189

### Witness

The canon run checked out 9b66189 (job 131612689049 log: `git checkout ... refs/remotes/origin/conv/wave-2` then `9b661899535cf0e09a7ded4687b2a615fd4e699f`). The artifact:
```
python -B tools/ci_read.py artifact 43342086225 package-full-shard-1/selftest-shard-1-of-2.txt --grep "rework_repair_binding|resume existing|FAIL"
FAIL tests: scripts/tests/test_controller_rework_repair_binding.py  10.8s ? exit 1 ? === test_controller_rework_repair_binding: 234/235 ok ===
      FAIL a recorded id under a fresh key is refused: resume, do not replace ? 'resume existing dispatch' not found in:
```
My local runs, each in a fresh detached scratch worktree:
```
python -B <scratch>/d/.../tests/test_controller_rework_repair_binding.py    # ddb7c6c
real 0m35.961s   rc=0
=== test_controller_rework_repair_binding: 235/235 ok ===

python -B <scratch>/n/.../tests/test_controller_rework_repair_binding.py    # 9b66189 (the red commit itself)
rc=0
=== test_controller_rework_repair_binding: 235/235 ok ===
```
The ddb7c6c CI canon (run 43343938014): shard 1 lists only `test_reinstall_equals_fresh.py` as FAIL, so `test_controller_rework_repair_binding.py` passed on CI there. Shard 2 FAILs only `test_selftest_slow_tests.py` (Red 3, not mine).

### (c) Culprit merge: **none. It does not reproduce, and the code under test is identical between the red and a green CI run**

- `git diff --stat 9b66189 ddb7c6c -- scripts/controller.py scripts/event_store.py tests/test_dispatch_liveness.py tests/controller_rework_common.py tests/test_controller_state.py tests/test_controller_rework_scope.py tests/harness.py` is **empty**. The test file and every module it imports are byte-identical between the CI-red commit and the CI-green commit.
- No first-parent merge of the branch (412a8bf ... 316baf8, 899ae36, 9b66189, ddb7c6c) touches `controller.py` or the test file (`git diff --stat <m>^1 <m>` per merge; only 316baf8 and ddb7c6c touch `onboard_apply.py`/install files).
- So no merge can be named as the cause. The defect is a non-deterministic test on the CI runner: one red out of three CI shard runs that contained it, and 0 of 2 local runs.
- Where the non-determinism plausibly lives (for the follow-up, NOT proven): the case sets `"never_started_after_s": 0.01` (test :34) and backdates a transcript `age=30`, then sleeps `0.05`. The fresh-key `apply("dispatch")` goes through the TR4-7 prelude `_holder_would_refuse` → `close_settled` (controller.py:4970-4996, :5022-5030, :7913-7932), which depends on wall-clock liveness. The empty refusal text means `apply` returned without raising, or raised a `ValueError`/`StateConflict` with an empty message (`controller_rework_common.refusal`, :106-111). I probed one hypothesis: every `dispatch` apply delayed by 0.05 s via an in-memory monkeypatch (stdin script, no file written). The case stayed green (`42/42 ok` at delay 0 and at 0.05). A slow runner alone does not explain it, and I did not find the root line.

### (d) The one fix

**No code fix on this branch.** Red 2 does not block wave 2: the converged head ddb7c6c is green on this file locally and on CI. The proposed node, which the coordinator opens: a finding in the controller's pile with class "flaky under CI: `test_controller_rework_repair_binding` fresh-key refusal empty once (run 43342086225, 9b66189), green on identical code in 43343938014" (FR-31: a test that fails only under load is a defect of the test). Owner: the pile owning TR4-7/t-2183. Its first step is to capture the actual exception object/type on the failing line: make the check print `repr` of the exception instead of `str`. An empty `str` and "no raise" cannot be told apart today, and that gap is itself the diagnosability defect. Pass/fail criterion: a repeat run under `--jobs 4` with the instrumented check names the path.

---

## Siblings (asked: other node pairs on this branch deciding opposite things about one install-paths row)

None found beyond Red 1. No wave-2 node merge touches `references/install-paths.json` (per-merge `git diff --stat`; only ddb7c6c, the main merge carrying OH3-9, does). `git diff 53025fc ddb7c6c -- ai-packages/qa-factory` grepped case-insensitively for `reporter-rehearsals|benefit-inputs|reporter-unread|coverage-map.receipt|listing['retire']|"class": ` matches only OH5-7's own lines. That is the positive control: the same grep finds the receipt pair. The other three rows OH3-9 reclassed (`reporter-rehearsals.json`, `reporter-unread/**`, `benefit-inputs.json`) are not decided the other way by any node on this branch. OF4-2 (remove `benefit-inputs` reader and row) is pending and not on the branch. When it lands it must follow the same rule: a carried row is never retired.

Class named: **"a node accepted on a base that lacks a sibling node's reclassification of the same install-paths row"** (surface: install-paths row class ↔ the installer's retire listing). Neighbouring cases walked: the other three rows reclassed by OH3-9 (above, none); hook-written rows (no wave-2 change); `moved_to` rows (no wave-2 change). The recurrence guard is process, not code: a node whose spec reads `listing["retire"]` for a named path should assert that path's class in its own test. OH5-7's test row 2 did this implicitly, which is why the semantic conflict surfaced at convergence and not in production. That is the right outcome. No new map axis is proposed.

## Duplication and consistency
After the fix, none. Before it, the branch carries two contradictory pins of one fact in one file: `MACHINE_LOCAL_KEPT` (:109-111, receipt kept) against `k_stale_receipt` (:868-869, receipt deleted). The fix removes the second. Grepped: `coverage-map.receipt` across the package (13 hits listed in the trail).

## Code quality
The `--ignore-receipt` branch is unreachable on ddb7c6c (carried rows never enter `listing["retire"]`, install_paths.py:59-61, :260-264). Unreachable gate code with a user-facing warning that names a false action ("this reinstall retires it") is a quality defect, and fix (b) removes it. Red 2: `refusal()` returning `str(exc)` makes "no exception" and "empty message" look the same, which is a diagnosability gap (proposed node above).

## One action, one road (item 12)
After the fix, the coverage check runs one way in the apply as everywhere else (no install-only flag). OH5-7 had introduced a second road (an install-only comparison skip); the fix removes it. Nothing is excluded for any language, project or case.

## Trail

Read: install-paths.json:89; check_coverage.py:195-300; onboard_apply.py:1355-1363, :1520-1600; install_paths.py grep `carried` (:57-61, :258-264, :576-633); test_reinstall_equals_fresh.py:100-120, :830-893; test_controller_rework_repair_binding.py:1-60, :150-252, main; controller_rework_common.py:106-111; controller.py:4955-5030, :5440-5485, :6096-6110, :7913-7953; event_store.py exception classes; batch-5 OH5-7 row (:37, :52, :58); onboarding-hooks/3 and onboarding-forge/1 OH3-9 rows; onboarding-forge/4 OF4-1..4; finding 20261112-kvitanciya-...md; finding B-248; spec t-167 §3.4 and receipt lines; reviews t-170, t-182 (Q3); journal t-202 lines 548-564; 8f40b43 stat and message; changelog.d/oh5-7-stale-receipt.md; git log -S on check_coverage.py; CI run 43342086225 jobs, shard-1 log and artifact; run 43343938014 shard artifacts.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "Red 1: OH5-7 (8f40b43) keys --ignore-receipt on listing retire, but OH3-9 (main, install-paths.json:89) made coverage-map.receipt.json carried, which never enters a retire listing (install_paths.py:59-61, 260-264); the onboard_apply.py:1549-1554 branch is dead and k_stale_receipt pins the pre-OH3-9 world, so test_reinstall_equals_fresh is 110/112 at ddb7c6c (112/112 at 9b66189)."
  ],
  "fixes": [
    "Carried is right (owner 22.10.2026, AR-25, AR-21; the receipt format is unchanged since 9ac00f0 and the move keeps the map bytes, so a reinstall never makes a receipt stale and a disagreeing receipt is a true project REJECT, reported in the regenerate step, non-fatal, receipt kept).",
    "One fix: delete onboard_apply.py:1549-1554 (the B-248 flag block); remove --ignore-receipt and its branch from check_coverage.py main; delete changelog.d/oh5-7-stale-receipt.md; rewrite test_reinstall_equals_fresh.k_stale_receipt: row1 expects [(False, 0)] (no flag, rc 0), row2 expects (True, []) (kept, not retired), new row: a receipt with a zeroed map_sha256 planted before the apply gives applied True, check_coverage rc 1 REJECT in the regenerate step, receipt byte-identical; delete the WITH-flag and flag-no-receipt rows; keep the REJECT and fresh-receipt rows; expected 111/111.",
    "Lead: rewrite the OH5-7 live-proof row (batch-5:58 and its live-runs copy) to: apply completes, the regenerate step reports the coverage REJECT, the receipt is kept; note on OF4-3 section 2 and on B-248 closure.",
    "Red 2: no code fix on this branch (not reproducible; code identical between CI-red 9b66189 and CI-green ddb7c6c); proposed node for the coordinator to open: FR-31 flaky finding, first step repr of the exception in the fresh-key check."
  ],
  "class_completeness": "Class: a node accepted on a base lacking a sibling node's reclass of the same install-paths row (surface: row class vs the installer's retire listing). Walked: the other three OH3-9 reclassed rows (reporter-rehearsals, reporter-unread, benefit-inputs): no wave-2 node decides them the other way (diff 53025fc..ddb7c6c grep, positive control = the OH5-7 receipt lines); no wave-2 merge touches install-paths.json; OF4-2 pending, not on branch. No new map axis proposed.",
  "trail": {
    "read": [
      "ai-packages/qa-factory/references/install-paths.json:89",
      "ai-packages/qa-factory/scripts/check_coverage.py:195-300",
      "ai-packages/qa-factory/scripts/onboard_apply.py:1355-1363,1520-1600",
      "ai-packages/qa-factory/scripts/install_paths.py grep carried",
      "ai-packages/qa-factory/scripts/tests/test_reinstall_equals_fresh.py:100-120,830-893",
      "ai-packages/qa-factory/scripts/tests/test_controller_rework_repair_binding.py:1-60,150-252",
      "ai-packages/qa-factory/scripts/tests/controller_rework_common.py:106-111",
      "ai-packages/qa-factory/scripts/controller.py:4955-5030,5440-5485,6096-6110,7913-7953",
      "plans/piles/onboarding-hooks/batch-5-nerazlozhennye-nakhodki.md OH5-7",
      "plans/piles/onboarding-forge/findings/20261112-kvitanciya-pokrytiya-otsutstvie-i-ustarevshaya.md",
      "plans/piles/onboarding-hooks/findings/B-248",
      "docs/tasks/specs/t-167-oh3-9-factory-files-by-class.md section 3.4",
      "docs/tasks/specs/reviews/t-182-oh3-9-diff.md Q3",
      "logs/journal t-202 lines 548-564",
      "CI 43342086225 shard-1 log and artifact; CI 43343938014 shard artifacts"
    ],
    "reruns": [
      {"command": "python -B scratch(9b66189)/ai-packages/qa-factory/scripts/tests/test_reinstall_equals_fresh.py", "result": "rc=0, 112/112 ok"},
      {"command": "python -B scratch(ddb7c6c)/ai-packages/qa-factory/scripts/tests/test_reinstall_equals_fresh.py", "result": "rc=1, 110/112 ok, the two stale-receipt FAIL rows"},
      {"command": "python -B scratch(ddb7c6c)/ai-packages/qa-factory/scripts/tests/test_controller_rework_repair_binding.py", "result": "rc=0, 235/235 ok"},
      {"command": "python -B scratch(9b66189)/ai-packages/qa-factory/scripts/tests/test_controller_rework_repair_binding.py", "result": "rc=0, 235/235 ok"},
      {"command": "stdin probe: never-started case with every dispatch apply delayed 0 and 0.05 s at 9b66189", "result": "42/42 ok both"},
      {"command": "git diff --stat 9b66189 ddb7c6c -- controller.py event_store.py and the test's imported test modules", "result": "empty"}
    ]
  }
}
```
