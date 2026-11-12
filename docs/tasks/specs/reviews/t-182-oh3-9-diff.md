# t-182 — critic of code, OH3-9 (builder t-175, commit 8b41fe6 on wip/oh3-9)

Spec: `docs/tasks/specs/t-167-oh3-9-factory-files-by-class.md` (attempt 2, accepted queued-to-lead after t-170).
Out of scope by dispatch: F-6 (honesty of `rebuilt_by`), the SIBLING_MAP:76 clause (Lead item, not built).
Line numbers below are of the branch (worktree `.claude/worktrees/oh3-9` at 8b41fe6).

## Verdict

**fit_with_fixes** (proposed; acceptance is the Lead's). There are no blockers. One medium finding (F1) and four small ones
(F2-F5) can all be fixed in one cheap fix round. Every spec item is built, and the witness re-ran consistently.

## Findings, ranked

### F1 — medium, fix before merge: `apply(after_summary=...)` trusts the caller's rows, and `_retire` does not re-check what the builder says it does
`onboard_apply.py:1516` `settled = drift["settled"] + list(after_summary or [])` and `:1566-1568` (`by_rel`, `effective`).
- Trace 1: a library caller passes `{"kind": "changed", "action": "delete", "item": {"rel_path": <a listed move-mode file, e.g. an unrecognised person's note>, "sha256": <its current sha>, "retire_mode": "delete"}}`. `by_rel` picks it up, because `kind != "new"` and the action is `delete`. The sealed listed item is replaced by the caller's item. In `_retire` (:1408-1430) the fold check, the readiness guard, the lexists check, the hook-written, carried and link checks all pass. `sha == item["sha256"]` holds because the caller supplied that sha, and `retire_mode == "delete"` holds, so the file is unlinked. This breaks invariant 5 (an undetermined file is never moved or deleted unless a summary listed it with its current bytes) and invariant 8 (only delete-mode AND machine-local rows go).
- Trace 2: a `new` row for `src/x.py` with action `delete` is appended to `effective` and deleted. Invariant 2 (outside the home refuses) is not defended, yet the `apply` docstring (:1474-1476) promises that apply REFUSES "a path OUTSIDE the factory's home ... new since the summary". The docstring is wrong for every caller other than `main`.
- Deviation (3) says "`_retire` re-checks sha and class". That claim is incomplete. The class re-check covers only `carried` and `hook_written`. It does not cover `machine_local`, `in_home` or `retire_mode`, and the sha is the one the caller supplied.
- Reach: today only `main` calls `apply` in production. My search for `[A-Za-z_]+\.apply\(root|\bOA\.apply\(|onboard_apply\.apply\(` with `-i` over `scripts/` outside tests found 0 hits. The positive control, the same pattern over `scripts/tests`, found test_config_migration.py:1431 and test_install_retire.py:344 and :369. So this is a hole at a library boundary, not a live defect. It is still the seam the spec built on purpose: S-10 and t-170 m1's "a library call does not go round the gate" (OH3-26, :1486-1487 states the same principle for `blocked`).
- Surface: the `after_summary` input of `apply`. Neighbouring classes walked: empty or None works (`[]`). A duplicate (a caller row for a rel that is also listed) produces two `after_summary` output rows for one file. An unknown `kind` (e.g. `"unreadable"` with `delete`) goes into `by_rel` like trace 1. A large input has no cap and needs none. All of these are closed by the same fix.
- Fix (one road, about 3 lines): make `apply` re-judge the rows through the one function instead of trusting them. Replace :1514-1516 with `drift = summary_drift(root, listing["retire"], [r["item"] for r in (after_summary or []) if r.get("kind") == "new"], table)`, refuse on `drift["refuse"]` as today, and set `settled = drift["settled"]`. `summary_drift` already skips listed rels by casefold, refuses outside the home, and gives `delete` only to delete-mode machine-local items. A new item that already carries `after_summary: True` comes out the same. Add one Table B row `apply-untrusted-after-summary` (apply() entry): an outside-home `new` row leads to ApplyRefused with nothing written; a listed move-mode file passed as `changed/delete` stays byte for byte. The docstring then becomes true.

### F2 — small, fix before merge: the new code duplicates the unreadable-file read (brief item 6)
`summary_drift` :1312-1320 handles `OSError` around `I.sha256_file` inline. The new helper `_sha_or_none` (:1389-1393), added in the same commit, does exactly that and is used only by `_retire`. Fix: `summary_drift` calls `_sha_or_none` (see F3). That gives one place where "unreadable" is decided.

### F3 — small, fix before merge: `summary_drift` nests 5 levels deep (brief item 7)
`onboard_apply.py:1280-1332` (53 lines). The nesting is for, then if/else on `is_new`, then if/else on is_file, then try/else, then if. The brief's ceiling is 3. Fix together with F2: add a small helper `_listed_kind(root, item) -> (kind | None, sha)` that returns None for "gone" and for "same bytes", and uses `_sha_or_none`. The loop then has 2 levels.

### F4 — small, fix before merge: a note written in this commit already cites a stale line
`references/install-paths.json:92` (the `install-manifest.json` row, `note`) says "a missing one is read as no manifest (onboard_apply.py:1496-1497)". On this branch that read is at onboard_apply.py:1579 (`old = I.read_manifest(...)`). The text came from the spec verbatim, but the diff moved the line. A data note is the reviewable carrier of the `rebuilt_by` claim (F-6), so it should not point at a moving line. Fix: name the function instead ("`apply` reads it with `read_manifest`; None is a fresh install").

### F5 — trivial, fix before merge: whitespace typo in a touched line
`install_paths.py:834` `nones =[r for r ...` (the diff turned `nones = [` into `nones =[`).

### Observations (not findings)
- `_retire` :1416 and :1418 call `I.classify(rel, table=table)` twice in a row. Computing it once is cleaner. Not a defect, so do it only if F1-F5 are being fixed anyway.
- `apply` :1574-1575 (`result or "kept: the next summary lists it"`) would hide a row that went to `_retire` and came back with no result. `_retire` returns one row per item, so this cannot happen today.

## The builder's deviations

1. **Eval 16 rewording: accepted.** I checked the trap myself. `CORPUS_DIRS` includes `skills` (install_paths.py:73). `.json` is in `CORPUS_SUFFIXES` (:74). `CORPUS_EXCLUDED` holds only the table and install_paths.py (:77). The walk drops only `scripts/tests` (:516). So `skills/qa-onboarding/evals/evals.json` is part of the reader corpus. The `qa-factory/state/jira-probe-*.json` row is `reader: none` (install-paths.json:121), so the literal `jira-probe-` in an eval prompt makes the G4 check report a reader that does not exist (`reader_contradicted`). Outside the table, a case-insensitive grep for `jira-probe-` across the package corpus finds nothing; the positive control is that the same grep finds the table itself. The reworded prompt keeps the expected outcome: "a stale Jira probe receipt under qa-factory/state/" is either `jira-probe-*.json` (discarded, delete-mode, machine-local) or `integrations/jira-direct-probe.json` (regenerated, machine-local, retired as unbuilt). Both are deleted, so the expected output holds whichever file the eval runner creates. A better fix lies outside the owns (`_corpus`), so it goes to the queue (Q1). **Is it a class worth a finding? Yes, low priority.** The reader corpus counts eval prose (`skills/*/evals/`), which is test material like `scripts/tests`, as a consumer. Every eval about a `reader: none` or discarded path is pushed to hide the path it tests. That weakens eval determinism, and the opposite mistake is also possible: a stray mention can make an unread row look read.
2. **`_sha_or_none`: acceptable.** It is a 4-line pure helper with the spec's semantics (§4.2, the `_retire` OSError branch → `kept: cannot be read`), and walrus use keeps the elif chain flat. The only problem is that it is not used in `summary_drift` (F2).
3. **The caller's `delete` rows are trusted: not acceptable as it stands. See F1.** The `_retire` re-check does not cover machine_local, in_home or retire_mode.

## Fit to the spec (§6.4 acceptance criteria)
| # | criterion | verdict | how checked |
|---|---|---|---|
| 1 | four rows carried machine-local in the carried block; every regenerated row has its basis and every `rebuilt_by` row its §3.3 note; three description sentences | met | data diff read row by row against §3.3/§3.4 (rows :88-117 in the spec's numbering); shipped table validates (test_install_paths 334/334, re-run) |
| 2 | `regenerated_without_basis` + shape rules, resolved via `_reader_path`/`_read_lower` and not `_corpus`; one error per row | met | `_basis_errors` read (install_paths.py diff); Table A rows present (grep of each spec id in test_install_paths.py: all ≥1; `rebuilt-by-on-{c}` generated at :851) |
| 3 | `summary_drift` is the one function, `_changed_since_summary` is gone, §4.4 invariants hold, `after_summary` on every return | met for `main`; for `apply()` as a library entry, invariants 2/5/8 rest on the caller (F1) | traced §4.2 table branch by branch; `out` literal carries the key (:1484); Table B ids present (all 15 grep ≥1) |
| 4 | `_retire` keeps carried and unreadable | met | diff :1418-1422 |
| 5 | p4 §0, SKILL Digest, two role-rules rows, eval 16 | met (eval reworded: deviation 1) | diff read; anchors "Never ask the person what" and "settled after the summary" are in their carriers |
| 6 | FR walk / AR lines in the report and commit | commit: met (`architecture:`, `judgment:`, axis block 1-36 present). I did not have the builder's report, so I could not check its FR walk | `git log -1 --format=%B 8b41fe6` |
Edges E1-E18: E1, E3, E13, E16 are by construction (read). E7 is covered by Table B `older-listing-names-evidence`. E14 is covered by `listed-tracked-discarded-changed` and `new-tracked-discarded`. E15 is covered by `listed-unreadable`/`outside-unreadable`. E18 is covered by the `qa-factory./x` and `qa-factory /x` rows. E17: `item.get("retire_mode") == "delete"` makes a missing mode `keep` (:1323).

## Duplication and consistency (brief item 6)
- F2: `summary_drift` vs `_sha_or_none` (inside the diff).
- `scan_tree`'s inline home test is at **install_paths.py:1191** on this branch (the builder's "~:1126" is the pre-diff line). It is the same expression as `in_home` (:289-300). Spec §10 and S-7 name it as an analog and keep it out of scope (non-goal). By the brief, a queued analog named in the spec is not a finding. It still has no node in any pile, so see Q2.
- Searched for a second drift or home function: `-i` grep over the onboard_apply.py diff for `qa-factory"`, `'qa-factory`, `_match(`, `fnmatch`, `os.unlink(` gave 0 added lines. `os.unlink(` occurs 3 times in the file before and after the diff (positive control: `git show` of both revisions), so the unlink site count did not grow. The clone ratchet output was not attached to the mechanical layer and I did not derive it.

## Code quality (brief item 7)
F3 (nesting), F5 (typo). `apply` itself is long, but it was long before; the diff added about 15 lines to it and no new nesting level. `_basis_errors` is 33 lines with 3 levels: fine. No dead branches. The names and the `_retire` docstring are accurate. The `apply` docstring is not accurate for library callers (F1).

## Judgment (q10-q11, AR-29) and architecture
- q11: `_basis_errors` checks presence plus a text join (the script exists and contains the key). That is a data check, census `xref`/`data` (judgment-census.json, one row added). The claim behind `rebuilt_by` is left to the note and to F-6, which is correct. `summary_drift` judges data only (class and machine_local via `classify`, home via the table, bytes vs sha). It does not judge a role's output. Role text: the p4 §0 sentence replaces a procedural sentence with a longer one ("relay the `after_summary` lines"). It is procedural, but it carries the owner's "never ask" and removes a question. `test_role_load.py` re-run: 165/165 ok, so the ratchet is not raised. No `blocks_override`, no census scan constants and no `kind: craft` marker were added (data diff read).
- AR-20: the census raise is named here: **+1 row, `install_paths.py _basis_errors`, class `xref`, owner `data`**. The commit's axis 18 line names it too. `test_judgment_census.py` re-run: 22/22 ok.
- AR lines claimed by the commit: AR-1, 9, 13, 14, 15, 21, 22, 25, 28, 29. Checked: AR-1 and AR-13 (greps above: no literal, no glob parse added); AR-14 (unlink count 3→3, `_retire` is the one record writer); AR-15 (both sites call `summary_drift`, at :1514 and :1966, and `_changed_since_summary` is gone; AR-15 is weakened only by F1's trusted second input); AR-22 (`after_summary`: producer `apply`, readers p4 §0, SKILL Digest, and role-rules points at both; positive control `retire_mode` found the same way. `rebuilt_by`: producer the table rows, reader `_basis_errors`/`_shape_errors`). AR-28: inside the home an unreadable file is kept, outside it refuses (read). I found no AR touched but left unnamed.
- q12 (one road, axis 34): home membership is read through `in_home` from the table's `home`, with no language, project or case branch. The search was the onboard_apply.py diff for `qa-factory` literals (0). The only second road is F1's trusted input.

## Mechanical layer: consistency of the witness
I re-ran these cheap controls in the worktree:
```
=== install paths: 334/334 ok ===
=== test_install_retire: 352/352 ok ===
=== role_load (the one measure of a role's start load): 165/165 ok ===
=== judgment_census: 22/22 ok ===
```
The first two and the census match the attached witness. `role_load` was not in the witness, so I added it. Every witness row is consistent with the diff. The negative controls name branches that exist in the diff: the `_retire` carried branch, the machine_local guard in the `deletable` expression, the `in_home` polarity, the `_basis_errors` call, and the reporter-rehearsals row. Tests that were not run (test_story_run_monorepo, test_scenario_cart_1, test_scenario_local_1_0108) are left to CI, as the batch canon requires. No witness row looks inconsistent.

## Queue (outside the diff; each needs an owner and a node, rule 19 (d))
- **Q1 — `_corpus` counts skill eval prose as a reader** (install_paths.py:507-525, `CORPUS_EXCLUDED` :77). Fix: drop `skills/*/evals/` in the walk filter, as `scripts/tests` is dropped (:516). After that, eval 16 can name `qa-factory/state/jira-probe-x.json` again. Proposed node: onboarding-forge, a finding file plus a row in the unfrozen batch. The pile Lead opens it.
- **Q2 — the analogs promised in spec §10 / t-170 m6 are not filed.** I searched for `benefit.inputs|check_coverage.{0,40}receipt|in_home` case-insensitively with `git log --all -G` over `plans/piles`: 0 commits. The positive control, the same command with `OH3-9`, found 028733f and 6766732. The working tree has no such finding either (grep -rli over plans/piles; control `OH3-9` found 3 files). Spec §10 says the pile's Lead files three analogs "at acceptance of this spec and before the builder dispatch": (1) AR-22, the spec's claim that `benefit-inputs.json` has a reader and no producer; (2) AR-28, an absent receipt silently skips the binding check; (3) the `scan_tree` :1191 / `in_home` convergence (AR-15). This is the Lead's action and still open.
- **Q3 — a sibling not named by the spec: B-248 / OH5-7** (plans/piles/onboarding-hooks/batch-5-nerazlozhennye-nakhodki.md:35, status «ожидает»). On reinstall, a stale `coverage-map.receipt.json` from an older generation makes `check_coverage` REJECT. Before OH3-9, the retire step at least removed it afterwards. Now the receipt is `carried` and is never retired, so the stale receipt stays across every reinstall, and OH5-7's chosen direction (ignore a receipt from another package generation) is the only cure left. OH3-9 itself is not wrong: the witness row test_reinstall_equals_fresh 105/105 keeps the fixture receipt byte for byte, and the decision is the owner's word. But OH5-7 should name this dependency, through a line in that batch or a finding by the Lead.

## Trail
Read: spec t-167 (all, 455 lines); critic-diff-brief.md items 6-7 and 10-12; the full diff of onboard_apply.py and install_paths.py; the changed lines of install-paths.json, role-rules.json, judgment-census.json, evals.json, p4-generate.md, SKILL.md, the changelog fragment and test_reinstall_equals_fresh.py; `_retire` in full (branch :1396-1462); `_corpus` and the CORPUS_* constants; the commit message (architecture/judgment/axis lines); the B-248 finding and the OH5-7 row.
Searches, each with its control: production callers of `apply` (control: test callers found); `after_summary` across the package (7 files); `jira-probe-` across the corpus (control: the table); filed analogs across all branches (control: OH3-9); a literal, glob parse or unlink added in onboard_apply.py (control: unlink count on both revisions); every Table A/B id in the tests.
Re-runs: test_install_paths.py, test_install_retire.py, test_role_load.py, test_judgment_census.py (outputs above).
Traced: the §4.2 action table through `summary_drift` → `apply` (`by_rel`/`effective`) → `_retire` → `after_summary` lines, for kinds new/changed/not_a_file/unreadable × delete/keep; phase early; `listing_given is None`; the two F1 library traces.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "F1 onboard_apply.py:1514-1516,1566-1568: apply trusts caller after_summary rows (a library call can delete a listed move-mode file or an outside-home path; _retire re-checks only carried/hook_written and the caller's own sha). Re-judge: drift = summary_drift(root, listing['retire'], [r['item'] for r in after_summary or [] if r.get('kind') == 'new'], table); refuse on drift['refuse']; settled = drift['settled']; add Table B row apply-untrusted-after-summary",
    "F2 onboard_apply.py:1312-1320: summary_drift duplicates _sha_or_none (:1389); call the helper",
    "F3 onboard_apply.py:1280-1332: summary_drift nests 5 levels; extract _listed_kind(root, item) using _sha_or_none",
    "F4 install-paths.json:92 note cites onboard_apply.py:1496-1497, now :1579; name the function (apply reads it with read_manifest) instead of a line",
    "F5 install_paths.py:834: 'nones =[' whitespace typo"
  ],
  "class_completeness": "Spec items 1-5 all built; sibling SIBLING_MAP:76 twin (_retire carried branch) built, its map clause is a Lead item. Queue: Q1 _corpus counts skills/*/evals prose as a reader (class behind deviation 1); Q2 the three analogs promised by spec section 10 / t-170 m6 (benefit-inputs AR-22, receipt AR-28, scan_tree:1191 vs in_home AR-15) are filed nowhere (git log --all -G over plans/piles, control OH3-9 found); Q3 unnamed sibling B-248/OH5-7: the receipt is now carried, so OH5-7 is the only cure for a stale-receipt REJECT on reinstall.",
  "trail": {
    "read": [
      "docs/tasks/specs/t-167-oh3-9-factory-files-by-class.md (all)",
      "docs/tasks/critic-diff-brief.md items 6-7, 10-12",
      "git diff origin/main...wip/oh3-9 (onboard_apply.py, install_paths.py full; data, skill, role-rules, census, evals, changelog, test_reinstall_equals_fresh changed lines)",
      "worktree onboard_apply.py _retire :1396-1462; install_paths.py _corpus :507-525, CORPUS constants :73-77",
      "commit 8b41fe6 message",
      "plans/piles/onboarding-hooks/findings/B-248-pereustanovka-poryadok-proverka-pokrytiya-ubrat.md; batch-5 row OH5-7"
    ],
    "reruns": [
      {"command": "python -B ai-packages/qa-factory/scripts/tests/test_install_paths.py (worktree oh3-9)", "result": "334/334 ok"},
      {"command": "python -B ai-packages/qa-factory/scripts/tests/test_install_retire.py (worktree oh3-9)", "result": "352/352 ok"},
      {"command": "python -B ai-packages/qa-factory/scripts/tests/test_role_load.py (worktree oh3-9)", "result": "165/165 ok"},
      {"command": "python -B ai-packages/qa-factory/scripts/tests/test_judgment_census.py (worktree oh3-9)", "result": "22/22 ok"}
    ]
  }
}
```
