# t-391 — diff gate, forge/6/F6-39 parts A1 + A2 (one topic)

Diff: `git -C .claude/worktrees/f6-39-a1 diff 5d79f97 0c9cda8` (c7da3ba = A1, 0c9cda8 = A2), 8 files, 381+/137-.
Worktree HEAD checked: `0c9cda87cccd6557137786620f89dfe60d776e6f`. Spec: `docs/tasks/specs/t-365-f6-39-ss1-11-specs.md` §1.0-§1.2, §3.

**VERDICT: fit_with_fixes (NEEDS WORK). 0 blocking findings, 4 fixes before merge (F1-F4), 7 non-blocking items (N1-N7).**
This is input to acceptance. The decision belongs to the Lead.

## Findings

### Fixes before merge (each one or two lines)

**F1 — `expire_archive_refs` checks against the short name `origin/main`, and a local branch or tag with that name shadows the pushed ref.**
`tools/worktree_sweep.py:81` `ARCHIVE_SAFE_REF = DEFAULT_REF`, used at `:696` (`rev-parse --verify --quiet origin/main^{commit}`) and `:708` (`merge-base --is-ancestor <sha> origin/main`).
Git resolves a short name in this order: `refs/heads/<n>` before `refs/remotes/<n>`. Probe in a scratch repo: `refs/remotes/origin/main` = B, then an unpushed commit U, then `git branch origin/main U`:
```
remote=bd34a0ca... local-branch-origin/main=8165d80c...
git rev-parse --verify --quiet "origin/main^{commit}"  -> 8165d80c...   (the LOCAL branch)
warning: refname 'origin/main' is ambiguous.
git merge-base --is-ancestor U origin/main             -> is-ancestor rc=0
```
So an old archive ref of an unpushed commit passes the guard. That breaks the invariant the docstring names at `:23`: "origin/main, always -- never the local main, which may hold unpushed commits". The commit is still reachable from that stray branch when the ref is deleted, which is why this is a fix and not a blocker.
Fix: a full refname for the two git calls (`refs/remotes/origin/main`). The display text can keep `origin/main`.
Pre-existing sibling outside this diff: `merged_verdict` / `resolve_ref` take the same short `DEFAULT_REF` before branch deletion. That goes to the queue line Q2 below.

**F2 — `update-ref -d <ref> <sha>` follows a symbolic ref, so a symref under the prefix deletes the branch it points to.**
`tools/worktree_sweep.py:718`. Probe in a scratch repo: `git symbolic-ref refs/worktree-sweep/x/sym refs/heads/keepme`. `for-each-ref` lists it with keepme's sha. Then `git update-ref -d refs/worktree-sweep/x/sym <sha>` gives `rc=0`, and `git branch --list keepme` prints nothing: **the branch is deleted**.
Only a hand-made symref triggers this, because the module writes only plain refs (`:496`). Still, the guarantee "only the listed archive ref is ever deleted" (E19) does not hold by construction.
Fix: `git update-ref --no-deref -d ref sha`. It costs one token.

**F3 — the `prune-rc1` row does not prove "the branch loop does not run after a failed prune" (E28). Git's own refusal hides the mutation.**
`tools/test_worktree_sweep.py:527`: `assert "pb" in repo.branches() and not has(rep, "REMOVED branch pb")`.
Probe on a byte copy: remove the new `return False` after `FAILED worktree prune`. The branch loop runs and logs `KEEP branch pb: error: cannot delete branch 'pb' used by worktree at '...'`. The branch survives because git refuses, so the line-527 assertion PASSES. The row still goes red, but only on the summary line at `:529`.
Fix: add `and not has(rep, "KEEP branch pb")` (no branch line at all), so the row pins the skipped loop itself.

**F4 — `gitcmd.main_checkout` promises "never raises", but it raises `ValueError` on a NUL in the answer.**
`tools/gitcmd.py:91` catches only `OSError` around `p.resolve()`. Probe with runner stdout `b".git\n.g\x00it\n"`: the result is `RAISED ValueError stat: embedded null character in path`.
Real git never prints this. Only an injected runner reaches it, and the effects are safe: the sweep crashes and removes nothing, and enforcement_probe fails closed. But the contract line at `:23` and in the docstring is false as written.
Fix: `except (OSError, ValueError)`.

### Non-blocking (queue or accept as is)

- **N1** `tools/test_worktree_sweep.py:513` `"dp" not in repo.branches()` is vacuous. The copy is detached `df`, so no `dp` branch can exist. This line was kept from the old test (deviation 6). Drop it, or assert something real (`"df" not in repo.branches()` is vacuous too, because the copy is detached).
- **N2** E30 (a stopped pass with prunables goes to `kept`) has no test row. The only stopped test (`:1197`) stops before the first copy, so `prunable` is empty. The code at `worktree_sweep.py:810-811` reads correctly, but nothing proves it.
- **N3** `sweep` calls `expire_archive_refs` (`:836`) outside any try. Per-copy errors and the prune's list failure are caught; this call is not. A raising runner leaves `crashed` with no summary line (deviation 7). The error direction is safe (nothing extra deleted), but it is a different road from its neighbours. Suggestion: wrap it in a try that turns an exception into one `KEEP archive refs: <Type>` line.
- **N4** `wiring_check.py:356` `resolve(root, timeout=5)` is not wrapped (deviation 2). Accept: the sibling `gitcmd.py` sits in the same directory as `wiring_check.py`, which is `sys.path[0]` when enforcement_probe runs it (`enforcement_probe.py:264-270`). A foreign `main_checkout` with another signature therefore has no realistic road in. A one-line `try` would make E7a hold by construction. Optional.
- **N5** Duplication: `gitcmd._first_line` (`gitcmd.py:63`) is a body-for-body copy of `worktree_sweep.first_line` (`:107`). Severity: queue. The two cannot be merged freely because worktree_sweep is a chain link that keeps its own helpers.
- **N6** A fourth `git status` reader that was not on the survivor: `tools/dup_ratchet.py:522-531` `status_changes`. It reads `--porcelain` WITHOUT `-z`, line by line, with `split(" -> ")[-1].strip('"')`. That is a different format, so the claim "the one reader of `status --porcelain=v1 -z`" is literally true. In the class sense ("one porcelain reader", P31), it is a sibling that is neither fixed nor queued. Suspected defect, NOT run: a C-quoted path (`a"b` comes out as `"a\"b"`) keeps its backslash after `strip('"')`.
- **N7** The axis 10 row "the one git runner" (`docs/SIBLING_MAP.md:260`) is still stale: it lists nine callers, F2-11 "wait", and no survivors named. Commit c7da3ba says "updated by the Lead". That edit is not in this diff, so it is owed in the Lead's merge commit, together with the stale comment at `mechanism_gate.py:255` (spec §6).

### Queue lines for the Lead («Остатки» form)
- Q1 `dup_ratchet.status_changes` reads non-z `--porcelain` by line: move it to `gitcmd.parse_status_z` (`-z`), or record why it stays | узел: <Lead opens, forge pile> (N6)
- Q2 short `origin/main` in `resolve_ref` / `merged_verdict` before a branch deletion: same shadowing as F1 | узел: <Lead opens>, unless F1's fix round takes it in (it is the same module and the same constant)

## K1 — fit to spec

| Change | Status | Evidence |
|---|---|---|
| A1-1 `main_checkout` | met (F4 aside) | `gitcmd.py:68-97`: NamedTuple, `run = runner or git` looked up at call time, try around call+decode, two non-blank lines, codes and texts as spec |
| A1-2 `repo_context` | met, deviation 1 | `worktree_sweep.py:255-267`; texts kept for `git`/`resolve`; `not-a-checkout` text now embeds `why` (see K7) |
| A1-3 wiring_check | met | guarded import `:219-222` (`except Exception`), `getattr` `:353`, `.githooks` check kept, docstring sentence added |
| A1-4 `parse_status_z` | met | `gitcmd.py:99-114`; bytes decoded utf-8/replace, not `as_text`; `<4` skip; R/C consumes the origin |
| A1-5 callers | met | three copies deleted, `compact_snapshot.py:233,606`, `worktree_sweep.py:435,605`, `hygiene_gate.py:1484` (inside the try) |
| A1-6 docstring | met | caller grep pointer, F2-11 sentence, Contract gains both entries |
| A2-1 expiry | met (F1, F2 aside) | `worktree_sweep.py:688-726`, called at `:836` only when not stopped (a refused pass returns earlier at `:752`); constants `:80-81`; docstring paragraph `:22-28` |
| A2-2 detached re-read | met | `:585-596`, after `remove_traces`, before `worktree remove`, both texts as spec |
| A2-3 prune summary | met | `:788-789` (dry run only), `prune_registrations` `:677-686`, list failure `:817-818`, done/kept after the block `:820-823`, stopped `:810-811`, Exit-codes docstring `:36` |

| Edge | Status | How |
|---|---|---|
| E1 rc -1 | met | test row `e1_git_missing_rc_minus_one` |
| E1a runner raises | met | row `e1a_runner_raises` |
| E2 one line / empty | met | two rows |
| E3 relative `.git` | met | row `e3_*` |
| E4 linked | met | `test_main_checkout_real_linked_worktree_row` (real git) |
| E5 bare / separate dir | met | rows `e5_*`, three-line row too |
| E6 spaces / non-ASCII | met by reading | `as_text` UTF-8, quotepath off in `gitcmd.git`; no row (spec did not ask for one) |
| E7 GIT_DIR | met (stated, unchanged) | no new env handling |
| E7a broken/foreign gitcmd | met for None/no attribute (test rows); signature mismatch see N4 | `test_rev_parse_failure_...` loop |
| E8-E12 | met | parse rows, mutation M4 kills the 3-char row |
| E12a | met | rows: lone NUL, 3/4-char, NUL-free blob, surrogate str; `parse_status_z(None)` gives `[('No','e')]` (probe), which errs toward MORE entries, the declared side |
| main_checkout error direction | met except a NUL line (F4) | warning-first-line: a garbled git_dir makes `linked` True, so `--apply` is refused; second guard `list_worktrees` kept |
| E13 no ref | met, deviation 4 | `test_r1_no_archive_ref...` |
| E14 no origin/main | met | r1 row `no-origin-main` |
| E15 local-only commit | met by reachability (r1 `unmerged`); F1 is the hole in "origin/main" naming | |
| E16 future date | met by reading (`now - date <= ...`, a negative age is kept); no row | |
| E17 exactly N | met | r1 `exactly-N`, mutation M2 kills it |
| E18 unmerged | met | r1 `unmerged`, mutation M5 kills it |
| E18a / E18b | met (docstring `:24-28`) | |
| E19 moved ref | met by reading (old-value form) except a symref (F2); no row | |
| E20 tree ref | met | `test_r1_no_archive_ref_and_a_ref_that_is_not_a_commit...` |
| E21 packed refs | met by reading (`for-each-ref`); no row | |
| E22 dry run | met | r1 `dry-run` asserts no `update-ref -d` call |
| E23 cost | met by reading: one `is-ancestor` only after the age filter; the background loop repeats it once per pass (up to MAX_PASSES), a small cost | |
| E24 HEAD moved | met | q5 `moved`, mutation M1 kills it |
| E25 re-read fails | met | q5 `rc128` |
| E26 branch copy | met by reading (`if not wt.short`) | |
| E27 archive failure | met | b1 `archive-fails` |
| E28 failed prune | met in code; the test pins it only through the summary (F3) | |
| E29 prune ok | met | `test_b1_detached_unmerged_prunable...` / `test_prunable_is_listed_pruned...` in the A2 witness filter |
| E30 stopped | met by reading, not tested (N2) | |

## K2 — error direction of every degraded path
- `main_checkout` failures go to None. In the sweep that is a Refuse (nothing removed). In wiring, only `<root>/.githooks` is accepted (narrower). Both are the declared safe side. A raise on NUL (F4) still lands safe (crash / fail-closed), but outside the contract.
- `parse_status_z` errs toward more entries: a refusal in hygiene_gate, a keep in the sweep. Verified by rows and by the `None` probe.
- hygiene_gate with a stale gitcmd (deviation 3): AttributeError, then a marker, then the rollback passes with a "not checked" note. This is the DECLARED degraded direction of `_measure_rollback` (`:1522` "never a refusal from an exception", the same path as `gitcmd is not importable` at `:1463`; spec E12a names "the marker lets the rollback pass"). So it is consistent, not a new direction.
- Expiry: listing fails gives KEEP. origin/main unresolved gives KEEP, none expired. `is-ancestor` rc not 0/1 gives `unknown`, not deleted. A delete refused gives KEEP. All are safe. The holes are F1 and F2.
- Re-read: rc != 0 or a moved HEAD keeps the copy (FR-59).
- Prune: a skipped or failed prune gives FAILED, exit 3, prunables kept, branch loop skipped.

## K3 — destructive safety of A2: the guard for each delete call
| Delete | Guards |
|---|---|
| `update-ref -d` (`:718`) | (1) commit date older than 30 days, strict; (2) `merge-base --is-ancestor <sha> origin/main` rc 0 (hole F1: the short name can resolve to a local branch or tag); (3) old-value `<sha>` (hole F2: no `--no-deref`, a symref deletes its target); (4) only with `apply` |
| `worktree remove` (`:597`) | the evaluate verdict + the archive of a detached HEAD + NEW re-read of the detached HEAD + no `--force` (git refuses dirty files); a branch copy keeps its commits in the branch, and `archive_and_delete_branch` refuses a moved branch |
| `worktree prune` (`:680`) | every unreachable detached registration is archived first; if one archive fails, prune does not run (FAILED) |
| `branch -D` of prunables (`:832`) | runs only when `pruned` is True (NEW); `merged_verdict` ancestor/patch-equal; archive before delete; git refuses a branch still used by a registration (seen in the F3 probe) |
Can work not in origin/main be deleted? Not under normal refs. Yes under F1 (a local `origin/main` branch or tag; the commit is still reachable from it at that moment) and under F2 (a symref under the prefix deletes a live branch). Both are fixes of this round.

## K4 — class-wide completeness, axis 10
- Main-checkout resolvers: `git grep -niE "git-common-dir|git-dir" -- 'tools/*.py'` (excluding tests) found only `gitcmd.py:74` (the survivor), `wiring_check` docstrings, `hygiene_gate:726` (a flag recognizer), `piles.py:2518` (an "is a repo" probe, not a resolver), and `collect_intake:446` (`--is-inside-work-tree`). A second search `main.checkout|main_path|commondir|common\.parent|...` found no other resolver. Positive control: the same calls found `gitcmd.py:74`. **No remaining private resolver.**
- Porcelain readers: `git grep -niE "porcelain"` found `dup_ratchet.py:524-527` `status_changes` (non-z, N6/Q1), `worktree_sweep` worktree-list readers (a different command), and the survivor's callers. `git grep -nF '\0' | grep -i split` found only path-list splitters (`ls-files`/`diff --name-only -z`), not status parsers. Positive control: the survivor's own `gitcmd.py:104` showed up in the same run. **One sibling (dup_ratchet) is neither fixed nor queued: Q1.**
- Map row staleness: N7.

## K5 — duplication and code quality (brief items 6-7)
- DUPLICATION AND CONSISTENCY: five copies collapsed into two survivors (verified by grep, K4). What remains: `gitcmd._first_line` duplicates `worktree_sweep.first_line` (N5, queue); dup_ratchet's status reader (N6/Q1); `expire` is not wrapped while its neighbours are (N3). Clone ratchet: not attached. It is the `forge-check` job's, read at batch level, not re-run here.
- CODE QUALITY: new functions are under 60 lines (`expire_archive_refs` `:688-726` = 39 lines, nesting 3). `sweep` was already ~120 lines (`:728-845`) and grows by ~10. That is pre-existing; queue only if the Lead wants it. Lying names or annotations: the "never raises" annotation of `main_checkout` (F4). Vacuous assertion (N1). No dead branches found. Lint ratchet attached: 0 new.
- ONE ROAD (item 12): no language, project or case exclusion. `expire` always uses origin/main while the background sweep judges copies against local main (`BACKGROUND_REF`). That split is the spec's own fork F-A1 (a), Lead 13.11.2026, read in §3, and it is the safe side.

## K6 — do the tests kill their mutations (byte copy outside the tree)
Copy: `cp -r <wt>/tools <scratchpad>/mut/tools`. Baseline on the copy: `26 passed, 155 deselected in 33.11s`. Each mutation was restored from a byte copy, and `cmp` printed `restored-identical`.
| Mutation | Row that went red |
|---|---|
| M1 `if now_head != wt.head:` changed to `if False:` | `test_q5_...[moved]` (1 failed) |
| M2 `<=` changed to `<` in the age check | `test_r1_...[exactly-N]` |
| M3 drop `return False` after a failed prune | `test_b1_...[prune-rc1]`, ONLY via the summary line (F3) |
| M4 `len(rec) < 4` changed to `< 3` | `test_parse_status_z_rows[ Mx\x00 M ab.txt\x00-expected10]` |
| M5 `if rc == 0:` changed to `if True:` (reachability dropped) | `test_r1_...[unmerged]` |

## K7 — the seven declared deviations
1. `not-a-checkout` text now embeds `why`: **accept**. It keeps the "cannot tell the main worktree" prefix and the door. Only humans read it, and W18 / not_a_git pass in the witness. The spec said "today's text", so the Lead notes it.
2. TypeError on a foreign `main_checkout` signature: **accept**, no realistic road (N4). A `try` is optional.
3. Stale gitcmd, then marker, then the rollback passes: **accept**. It is the declared degraded direction (K2).
4. E13 with the full format including the parenthetical: **accept**. The format of spec (e) governs, and E13 is shorthand.
5. `expire_archive_refs` always resolves origin/main: **accept, correct**. F-A1 says "always origin/main". Using `ref` would expire against local main in background runs. The name form is F1.
6. Vacuous `"dp"` assertion kept: **fix or drop** (N1, non-blocking).
7. No try around expire/prune/list in sweep: **accept with suggestion** (N3). Safe direction, but a different road from the per-copy catch.

## Witness consistency (rule 12)
- A1 4-file run: 460 = Lead's 3-file re-run 196 + hygiene 264. My hygiene run: 6 + 258 deselected = 264. Consistent.
- A2 run: 23 + 121 = 144. A1's sweep run: 13 + 121 = 134. The +10 rows match the diff: b1 +1, r1 6+1, q5 2. My copy baseline: 181 = 144 + test_gitcmd 37. Consistent.
- A1 grep negative re-done with my own shapes (K4).

## Trail
Read: spec §1.0-§1.2, §3, §6 (t-365); critic-diff-brief.md :8-87; SIBLING_MAP.md :248-267; both commit messages; the whole diff 5d79f97..0c9cda8; worktree files `worktree_sweep.py` :85-125, :560-640, :688-850, :1155-1185; `wiring_check.py` :1-30, :85-100, :215-400, :740-800; `hygiene_gate.py` :55-66, :1454-1535; `gitcmd.py` whole; `enforcement_probe.py` :250-275; `dup_ratchet.py` :520-545; `test_worktree_sweep.py` :1188-1200 and the diff rows.
Runs: the control re-run, five mutations, the M3 line probe, two scratch-repo git probes (F1, F2), and one Python probe (F4, `parse_status_z(None)`). All outputs are quoted above.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "F1 worktree_sweep.py:81/:696/:708 -- use the full refname refs/remotes/origin/main for rev-parse and merge-base --is-ancestor; a local branch or tag named origin/main shadows the remote (probe: is-ancestor rc 0 for an unpushed commit)",
    "F2 worktree_sweep.py:718 -- git update-ref --no-deref -d ref sha; without it a symref under refs/worktree-sweep/ deletes its target branch (probe: keepme deleted, rc 0)",
    "F3 test_worktree_sweep.py:527 -- add not has(rep, 'KEEP branch pb') so the prune-rc1 row pins the skipped branch loop; today git's own refusal hides the mutation and only the summary line catches it",
    "F4 gitcmd.py:91 -- except (OSError, ValueError): a NUL in the rev-parse answer raises ValueError, so the never-raises contract is false"
  ],
  "class_completeness": "Axis 10: no private main-checkout resolver remains in tools (grep with positive control). Porcelain: three -z copies collapsed; dup_ratchet.status_changes (non-z --porcelain line reader, dup_ratchet.py:522-531) is a sibling neither fixed nor queued -- queue line Q1. Short origin/main in resolve_ref/merged_verdict before branch deletion: same shadowing as F1, queue line Q2 unless the F1 round takes it. SIBLING_MAP axis 10 row :260 still stale -- owed in the Lead merge commit with the mechanism_gate.py:255 comment.",
  "trail": {
    "read": [
      "docs/tasks/specs/t-365-f6-39-ss1-11-specs.md sections 1.0-1.2, 3, 6",
      "docs/tasks/critic-diff-brief.md :8-87",
      "docs/SIBLING_MAP.md :248-267",
      "git diff 5d79f97 0c9cda8 (all 8 files) and both commit messages",
      ".claude/worktrees/f6-39-a1/tools/worktree_sweep.py :85-125 :560-640 :688-850 :1155-1185",
      ".claude/worktrees/f6-39-a1/tools/wiring_check.py :1-30 :85-100 :215-400 :740-800",
      ".claude/worktrees/f6-39-a1/tools/hygiene_gate.py :55-66 :1454-1535",
      ".claude/worktrees/f6-39-a1/tools/gitcmd.py whole",
      ".claude/worktrees/f6-39-a1/tools/enforcement_probe.py :250-275",
      ".claude/worktrees/f6-39-a1/tools/dup_ratchet.py :520-545",
      ".claude/worktrees/f6-39-a1/tools/test_worktree_sweep.py :1188-1200 and diff rows"
    ],
    "reruns": [
      {"command": "python -B -m pytest tools/test_hygiene_gate.py -q -k rollback (in the worktree, subshell)", "result": "6 passed, 258 deselected in 2.42s"},
      {"command": "byte copy baseline: pytest test_worktree_sweep.py test_gitcmd.py -k 'q5_ or r1_ or b1_archive_failure_skips or parse_status_z'", "result": "26 passed, 155 deselected in 33.11s"},
      {"command": "mutations M1-M5 on the byte copy, restored and cmp-verified", "result": "each mutation turned its named row red (q5 moved, r1 exactly-N, b1 prune-rc1 via summary only, parse 3-char row, r1 unmerged); restored-identical"},
      {"command": "scratch repo: local branch origin/main over an unpushed commit, merge-base --is-ancestor U origin/main", "result": "rev-parse resolves the local branch, warning ambiguous, is-ancestor rc=0"},
      {"command": "scratch repo: symref refs/worktree-sweep/x/sym -> refs/heads/keepme, update-ref -d it with its sha", "result": "rc=0, branch keepme deleted"},
      {"command": "python probe: gitcmd.main_checkout with runner stdout containing a NUL; parse_status_z(None)", "result": "RAISED ValueError embedded null character; [('No', 'e')]"}
    ]
  }
}
```
