# t-371 — critic on plan: t-366 specs F6-37 (A), F6-35 (B), F6-58 (C)

Reviewed: `docs/tasks/specs/t-366-f6-37-f6-35-f6-58-specs.md` (read whole). Code tree: `.claude/worktrees/read-main` (origin/main)
unless marked "root". Nothing was modified; every command below is read-only (git queries, in-memory Python probes on pure
functions, transcript greps).

**Overall verdict: fit_with_fixes.** Per node: **A fit_with_fixes**, **B fit_with_fixes** (3 blocking spec edits),
**C fit_with_fixes** (4 blocking spec edits). The plan is sound and the forks are mostly well-argued. But the designer's
B6 estimate is refuted by measurement. B-F2 (a) contradicts the carrier that owns the fact. And node C over-claims what a
band prevents in the live case, and leaves the band reader open to two input-surface holes I reproduced. Every blocker
below comes with the exact spec edit. Before a builder dispatch these go into the spec, as a fix round of the same draft.
The decision on the forks and on acceptance stays with the Lead (rule 6).

---

## 1. Facts by trail

### Node A (spot-checks: 6 claims, all hold)
- A2: `handoff_gate.py:69` `GATED_KINDS = ("critic", "designer")`; `_in_folder` `:89-97` (direct child, trailing segments, `.md`);
  `_real` `:100-101`; `_gate` `:151-175` refuses NO_PATH `:167-169` and MANY `:170-172`, dedups by `_real` `:162-166`. **Holds.**
- A3: `dispatch_manifest.py:689-690`: the cheap exit for a non-builder without `owns`. `check_cut` `:827-828` returns
  `(0,"","",False)` for a non-builder with no owned path. **Holds.**
- A4: `handoff_paths` `:641-645` (absolute only). Readers `handoff_gate:163` and `dod_gate:378`. **Holds.**
- A5: `dod_gate.named_handoffs` `:377-382` uses `hg._in_folder` and `hg._real`. **Holds, but see §2.** It does carry its own copy of
  the candidate LOOP (dict by `_real`, count == 1). The spec's "no copy of its own" is true for the predicate and false for the loop.
- A6: `decide_full` `:703-750`. The completeness refusal comes at `:730-732`, then the path check, then the label check. **Holds.**
- A7: `waivers` `:380-389`, and `handoff` is an item of `KEY_GROUPS` `:84`. **Holds.**
- A-F1 evidence: root `docs/tasks/compact-snapshots/2026-11-13-1011-narrative.md:56` "My t-337 dispatch had no `handoff:` line".
  Root journal `dev1.jsonl:853` shows t-337 was a **designer**, and `:856` "partial draft saved by coord". The leak is real.

### Node B (spot-checks: 5 claims; **B6 refuted**)
- B5: `dispatch_gate.py:1768-1786` (`push_before_launch_warn`), wired at `:2035-2046`. `_git_out` `:1758-1765` returns None on
  any non-zero exit or empty output. **Holds.**
- B1: `plans/builder-rules.md` item 20 (lines 90-92): "Worktree агента режется от ЗАПУШЕННОГО `origin/main`". **Holds.** The same
  item also says "написать в диспатче «сначала слей <sha>»" (see blocker B-2).
- B2: `docs/RUNBOOK.md` §12 item 8 at 594-595. **Holds.** Items 7 and 10 sit at 591-593 and 600-601.
- B4 "host isolation still in use": the spec infers it from "own worktree" journal notes, which is weak (the spec says so itself). **I measured it:**
  `"isolation": "worktree"` (unescaped, so a real tool_input) occurs in 4 coordinator transcripts. Counts: acb1ecf0 = 4 (13.11),
  bd2e9107 = 11 (13.11 02:15), f92520fc = 47 (12.11), 1624cb4a = 42 (12.11). One 12.11 dispatch reads
  "Branch: pile/onboarding-hooks/batch-4 from origin/main (d5efb4b)". **The class is live**, so B-F1 (b) rests on measured ground.
- **B6 — the estimate "push_before_launch_warn is silent in the root" is REFUTED.** Experiment B0, run from the root, with the
  same subprocess form the hook uses (`capture_output`, `text=True`, `timeout=5`):
  - `git rev-parse origin/main` → `14c089f…`, exit 0, empty stderr;
  - `git rev-parse refs/remotes/origin/main` → the same sha, exit 0;
  - `git rev-list --count origin/main..main` → `53`, exit 0, empty stderr (the same with qualified refs);
  - `git rev-parse main` → exit 0.
  The three calls the WARN makes all succeed, so the WARN is NOT silenced by the directory. The ambiguity is real only for
  **single-revision** forms: `git log -1 origin/main` and `git rev-list --count origin/main` both give `fatal: ambiguous argument
  'origin/main': both revision and filename`, exit 128. That is what the coordinator hit in snapshot 0245:8 ("cherry-pick во
  временный worktree … от `refs/remotes/origin/main` (не `origin/main` …)").
  **Root cause, measured:** the directory is a REGISTERED git worktree, not a stray copy. `git worktree list` shows
  `C:/QAFactory/forge-repo/origin/main 0b76112 (detached HEAD)`, and `origin/main/.git` reads `gitdir: …/.git/worktrees/main`.
  It was created 13.11 01:32-01:33 (stat), almost certainly by `git worktree add origin/main` meant as a base.
  Side measurement: root local `main` has diverged (53 ahead, 279 behind `refs/remotes/origin/main`, merge-base `1fd1b104e`).
  So today the push WARN fires on every isolation dispatch from the root, with "53 commits ahead". Whether that is read or is
  noise is a question for the Lead (WARN fatigue, see §3).

### Node C (spot-checks: 6 claims, all hold; 2 new surface holes)
- C1/C2: `journal_validator.py:895-896` (`seen_task_ids`, `max_num`), `:940-955` (9a), `:1088-1092` (max grows).
  `extract_task_ids` `:345-357` counts any event's task_id. **Holds.**
- C3: grep `max_task_num|extract_task_ids|next_free_id|next free`, case-insensitive, over `tools/`. It finds exactly the three next-id
  readers (`journal_validator.py:360`, `journal_keys.py:627`, `compact_snapshot.py:325`) and no caller of `max_task_num` outside its module.
  The grep found all of them, which is its own positive control. **Holds.**
- C4: `journal_echo.py:2337` calls `journal_validator.decide(disk_text, head_text, now, seed_text=…)`. **Holds.**
- C5: `_collision_warning` `:1432-1503` is a WARN with the `declare` door. **Holds.**
- C7: root `dev1.jsonl:880-930`, read line by line. The notes at 889, 890, 892, 900, 905 and 908 say what the spec says. **Holds.**
- Import direction (load-bearing for §C.3 step 1): `journal_validator.py:242-246` imports `journal_keys` at module level, and
  `journal_keys.py` (imports at `:40-50`) imports no validator and has no `TASK_ID_RE` (its own `^t-(\d+)$` sits at `:631`). See blocker C-2.
- Negative "no `id_band` anywhere in logs yet": Grep `id_band`, case-insensitive, over root `logs/` → 0. Positive control with the same
  shape: `worker_ref` → 431 hits in `logs/journal/dev1.jsonl`.
- No short task ids exist (so narrowing the id regex changes nothing in practice). grep `"task_id": ?"t-[0-9]{1,2}"` over the root
  journals → 0. Control `t-[0-9]{3}` in dev1 → 845.

---

## 2. Node A — handoff folder checked before launch

**One road (P31)?** The PREDICATE is one road: `_in_folder` and `_real` are reused, and `HANDOFF_DIRS` and `handoff_paths` are the only readers.
The CANDIDATE RULE is not. Step 2.6 writes a third copy of the loop "dedupe the in-folder handoff paths by `_real`, then
count". The first copy is `handoff_gate._gate:162-166`, the second is `dod_gate.named_handoffs:377-383`. Three copies of one rule can drift: one
of them changes the dedup key and the gates disagree on "one path". That is a duplication finding (rule 18), and a fix of this round (F-A1).

**Refusal texts (P15/FR-1/FR-2).** NO_LINE, WRONG_FOLDER and NO_PATH each say what is wrong, what is expected and give a door
(`manifest-skip: handoff -- <reason>`) the coordinator can use. MANY names the paths and its door (keep one). NOTE_UNCHECKED and
SKIP_NOTE are informative. Complete. One wording point: `<repo root>` in "Expected" is a placeholder the coordinator must
resolve. Acceptable: the write gate's text uses the folder only.

**Could it refuse a dispatch that is legal today?** I traced `decide_full` with the new call placed after `:732`:
- A critic or designer dispatch with NO handoff that writes nothing (report as its final message) is legal today: the write gate never fires. It is
  **refused** under A-F1 (a). This is intended (R11-h, `CLAUDE.md:236`) and the door exists. But A.4's error-direction sentence ("never REFUSE a
  dispatch whose write the write gate would accept") does not describe it: there is no write. The spec must say plainly that
  NO_LINE/NO_PATH promote R11-h from discipline into a code gate. That is a mechanism promotion backed by the t-337 leak, which rule 10(d) allows on evidence. (F-A3)
- Wrong folder, two paths, a quoted line or a relative path: today the write gate refuses these at the first Write, so the dispatch fails anyway.
  Same verdict, only earlier.
- A degraded cut or an import failure gives pass+NOTE. This is right, an unknown is not a launch refusal.
- Unaccounted consumers of `decide_full`: `decide()` is called by `owns_gate.py:1112` and by `critic_snapshot` (its docstring
  `:133-152`: a dispatch that `dispatch_gate.decide` blocks does not overwrite the snapshot). With node A, a critic dispatch refused for its
  handoff no longer overwrites `.claude/critic_snapshot.json`. That is the desired direction, but the spec names neither consumer, and
  `decide_full`'s docstring order ("completeness → path → label") must change. (F-A2)

Edge table e1-e23: complete for the battery (magnitude e17/e19, nesting e11/e12/e21, encoding e20, empty e18).

---

## 3. Node B — worktree base

**"The defect no longer applies as written, only the narrowed class remains"** is supported, partly by the spec and fully by
my measurement (§1 B4: isolation dispatches are still made, 4 of them in today's coordinator session). Item (a) of the finding is
done (builder-rules item 20). The finding's item (b), the WARN, and item (c), the merge-first template line, remain. B-F2 (a) deliberately drops (c).

**Is a WARN the right strength?** Yes. P1 says code reports, and rule 10(d) says promotion follows a leak. The dispatch has
ALREADY gone out when the WARN arrives (`main()` `:1987` writes allow first), so the coordinator reads it in its
additionalContext and must stop or re-dispatch. That is the same channel as the push WARN, which demonstrably fires
(4 hits in f92520fc). Who reads it: the coordinator model, at that turn. There is no detector that it is acted on, except node B's own
proposed calibration line. Caution: the root's diverged main (53 ahead) makes the push WARN fire on every isolation dispatch
today. A second WARN on the same dispatches adds to fatigue. `tools/warn_density.py` (t-362) is the measurer the Lead
can point the detector at.

**Blocking issues.**
- **B-1 (B6 refuted).** B0 is already measured (§1). Step 1's motivation, the "NOTICED DEFECT" row B6 and row b12 ("ambiguous in
  the fake git … defect B6 fixed") encode a git behaviour that git does not have for these forms. A fake that answers
  "ambiguous" to `rev-parse origin/main` pins a fiction.
- **B-2 (B-F2 (a) leaves the owning carrier on the dropped road).** `plans/builder-rules.md` item 20 (lines 90-92) still says
  "запушить `main` либо написать в диспатче «сначала слей <sha>»". RUNBOOK item 8, as rewritten by B, says it "points to builder-rules
  item 20, which owns the fact" (B.6 axis 31). After B lands, the owner carrier sanctions the road that both WARNs now forbid.
  That is two roads for one action (P31, axis 31/34). Node B's owns lack `plans/builder-rules.md`.
- **B-3 (`_git_out` cannot answer step 2.4).** `merge-base --is-ancestor` prints nothing, and its meaning is the exit code
  (0 = contained, 1 = not). `_git_out` (`:1758-1765`) maps exit 0 with empty output, exit 1 and errors all to None. A Sonnet builder
  that reuses it, as the spec's "the same as `_git_out`" invites, gets a WARN that never fires (every name reads as "unknown → skip").

**Non-blocking.** The token scan reads the whole prompt, so a branch named only inside a fence (a quoted older dispatch) counts.
This is allowed for a WARN, but there is no row, and axis 13's closing rule asks new readers to use the cut (`decision.cut` exists for a builder).
A pile branch that exists only on the remote and is named bare (`pile/x`, ref `origin/pile/x`) is silent, and this is not named.
`worktree_base_warn` and `push_before_launch_warn` share a prelude (tool + isolation guard). Extract it. (F-B1, F-B2)

---

## 4. Node C — id bands

### The live sequence of 13.11 walked under the proposed rule
Writers: S1 (wrote 885-886, 900) and S2 (wrote 889-892, 903-908). S2 is "the second writer".

| step | live (root dev1.jsonl) | under rule 9e |
|---|---|---|
| 1 | ~10:21-10:28: S1 composes t-347 and t-348 (scouts). S2, reading the same `where`, composes t-347 (builder), t-348 (scout) and t-349 (fix builder) into its dispatch texts. Neither knows the other exists. | **Nothing changes.** A band is opened by "the second writer", and no one knows they are second. No code tells them (C.5's last bullet: no session field). The dispatch texts already carry colliding ids. **Not prevented.** |
| 2 | 10:28:00-01: S1 writes 885/886 (t-347, t-348). | Same. |
| 3 | 10:28:32-35: S2 re-reads the tail and hand-writes t-349, t-350 and t-351 (889, 890, 892), noting the mismatch. The gate never fired, because S2 renumbered before writing. | S2 sees the mismatch the same way. Through the new CLAUDE.md sentence, S2 can open its band on the renumbered line (C-F1 (a): `delegated t-400 id_band "t-400..t-449"`). **This is the first point where the rule steers S2,** and only through the text, unless S2 actually tries t-347 and meets the NOVELTY text, which now names the band door. |
| 4 | 10:36-10:38: S1 takes t-354 (900). S2 had put t-354 into a critic report name and t-356 into a designer handoff (905, 908). | S2 now composes from its band (t-401, t-402). S1 stays on main (t-352…). **Collision round 2 is prevented.** |

So the band prevents the second and later collisions, and NOT the first. §C.1's "A CLOSED band can [serve two writers]" is true
only after the writers know about each other. The spec presents the band as closing the 13.11 case without that qualifier
(blocker C-3).

### The asked edges
- **A band reserved and never used:** the main sequence skips it forever (`main` jumps to `hi+1`), and the ids are burned. This is harmless, but `where`
  prints "band t-A..t-B: next t-A" forever, and every band ever declared adds a line. Unbounded output, and an invitation for a later
  session to take ids from a dead band. (F-C2)
- **Overlapping bands, same file:** impossible by BELOW (`lo > top`, and top includes closed ends). **Concurrent declaration:** two sessions
  compute the same band at the same moment. The second line meets BELOW only after its dispatch already went out with a band id, which is the 13.11 class again, one
  level up. This is not named. (F-C4)
- **A band declared after an id inside it was written:** refused by BELOW, because `top` includes every id. Correct. **Sharper variant:** the
  BELOW text and the CLAUDE.md sentence steer the writer to `t-{top+1}`, i.e. a band ADJACENT to main. Then S1's next `main` (composed
  before S2's band line lands) is S2's band start, and the 13.11 race recurs exactly. A band protects only through DISTANCE from
  the main sequence, and nothing requires or suggests a gap (blocker C-1).
- **A merge of two clones:** each side's valid bands enter the state. `main_floor` excludes ids inside closed bands, and `main` jumps past
  any band, so the merged state never re-issues an id. Independent overlapping bands are reported by the collision WARN clause (C-F2 (a)).
  Kept lines are not re-validated. **Correct as specified.**
- **Append-only:** preserved. The field exists only on new lines, a malformed band on an old line is ignored (j12), nothing is rewritten, and
  the `t-499` filler stays.

### Blocking issues
- **C-1 (no gap, so the band does not keep the race away).** See above.
- **C-2 (circular import / second copy).** §0 "Small choices" says each band end "is parsed with `TASK_ID_RE` (`journal_validator.py:311`)",
  but the reader lives in `journal_keys`, which the validator imports at module level (`:242-246`). Following the spec literally either
  creates a circular import or copies the regex.
- **C-3 (over-claim on the live case).** See the walk. The spec must state the residual and give the Lead the awareness fork.
- **C-4 (surface: the task-id / band NUMBER parser; the battery is incomplete).** Reproduced in memory:
  `re.match(r'^t-(\d{3,})\.\.(?:t-(\d{3,}))?$', 't-４００..t-４４９')` matches, and `int()` gives (400, 449). A fullwidth band is accepted as a
  different string with the same numbers (encoding). Python 3.12.10 `int('9'*5000)` raises `ValueError: Exceeds the limit (4300 digits)`,
  so an unbounded `\d{3,}` band crashes the reader (magnitude). Neighbouring classes walked: empty (`""` is in j5, handled), nesting (n/a,
  scalar), broken form (j5). **The same surface already has both holes in today's validator:** `validate_new_lines` on a new
  `delegated` with `task_id` = `"t-" + "9"*5000` **raised ValueError**, and with `"t-００２"` returned **no violation** (accepted as the next
  id t-002, while key readers see a different string). These two existing holes are outside this diff, so they go to a finding (rule 5/14). The band reader must not inherit them.

---

## 5. The forks

| fork | recommendation right? | cost | who decides |
|---|---|---|---|
| A-F1 (a) refuse no-handoff critic/designer | **Yes.** The leak is on record (t-337 designer, `dev1.jsonl:853,856`). | One skip line per deliberate text-report dispatch. | Lead (code enforcement of an existing duty, R11-h). |
| A-F2 (b) scout path relative, dod_gate → finding | **Yes as a stopgap.** Hidden cost: node C's detector reads `t-NNN` from ABSOLUTE handoff paths (`hop_metrics` → `handoff_paths`), so scout dispatches become invisible to it (1 of the 5 collided dispatches of 13.11 was a scout, `dev1.jsonl:890`). | Finding + batch line; the detector must read the relative form or the description (F-C5). | Lead. |
| B-F1 (b) WARN + RUNBOOK | **Yes**, on my measurement (§1 B4), not on the spec's inferred trail. | ~40 lines + table. | Lead. |
| B-F2 (a) one road, drop "merge first" | **Yes on the t-065 evidence, incomplete as written:** builder-rules item 20 must change in the same node (B-2). | One more owned file and one sentence. | Lead (builder-rules is a forge carrier under Lead); highlight "решила сама" to the owner, because it retires a road a team member's finding proposed. |
| C-F0 (c) one field, two forms | **Yes**, with C-1 (gap) and C-3 (awareness) added. | One reader. | Lead. If the Lead picks the awareness option "every session opens a band", that changes every session's routine: tell the owner. |
| C-F1 (a) any event | **Yes.** (b) recreates the filler, (c) adds an event. | None. | Lead. |
| C-F2 (a) WARN at merge | **Yes** (one road with `declare`). It reverses item 3 of the finding, which the batch Lead chose "по рекомендации; владелец может отменить". | One clause. | Lead; flag it to the owner as a reversal of a recorded direction. |
| C-F3 (a) 1000 / 10000 | **Yes**, plus a new constant BAND_GAP_MIN (C-1). Measured rate: 17 ids / 30 min / 2 sessions (root `dev1.jsonl:883-914`, recounted: t-345…t-366 between 10:21 and 10:48). | None. | Lead (technical). |
| C-F4 (a) compact_snapshot fallback | **Yes**, and widen it: the MAIN path (`compact_snapshot.py:537-543`, `journal.next_free_id`) must print bands too (F-C3). | ~10 lines. | Lead (technical). |
| C-F5 (a) rule 9b continuation → finding | **Yes**, a different predicate. | One finding. | Lead. |
| Queue F6-58 before F6-59 | A real conflict: batch-1 line 13 `очередь: onboarding-forge/1 → onboarding-forge/2`, while F6-59 depends on F6-58. | One added `очередь:` line (allowed in a taken batch, PROJECT.md «Командная работа» п. 2). | Lead. |
| **Missing fork C-F6 (awareness)** | See C-3: (i) a SessionStart/journal_echo NOTE when another main-session transcript of this project was written in the last N minutes (reader: `transcripts`, axis 14; a NOTE, never a refusal); (ii) every session opens a band at its first id; (iii) accept the residual and rely on the detector. My recommendation: **(i)**. It uses an existing reader, costs one line, and turns the first collision into a steer. | (i) ~30 lines in one hook + a row. | Lead; (ii) would need the owner told. |

---

## 6. Mechanism questions (rule 10)

| node | (a) cost | (b) axes | (c) detector | (d) on the path |
|---|---|---|---|---|
| A | stated (one parse, one skip line, the coordinator pays) | enumerated, but **"axes 20-30: n/a" is a range, not one line per axis** (rule 10(b) asks for a line per axis) | check 28(d), registered (`PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:873-880`, verified) | the dispatch_gate PreToolUse hook (`.claude/settings.json:29`) |
| B | stated | **"axes 16-30" is a range**; axis 13 n/a is argued (whole-prompt layer) but contradicts axis 13's closing rule (a new reader uses the cut) | **not registered**: "the Lead registers it (the number is the Lead's)". Acceptable only as an explicit Lead step in the same commit (F-X2) | WARN on the hook, by design |
| C | stated | **"axes 16-30" is a range**; axis 14 should read "covered" if C-F6 (i) is taken | **not registered** (same as B); and as designed it misses relative scout paths (F-C5) | validator (pre-commit, journal_echo, CI). Opening a band stays on discipline: a named line, detector (c) |

No question is unanswered, but (c) for B and C is a promise, not a registration. Rule 10(c) says "a mechanism with no registered
detector is a wish". This is fixable by making the registration part of the Lead's commit checklist (F-X2), so it is not a blocker.

---

## 7. Feasibility and cut

- **Sonnet-executable with nothing to invent?** A: yes (after F-A1 names the shared function). B: no until B-3 names the exit-code
  helper. C: no until C-2 says where the regex lives, and until the incremental state has a named API (§C.3 step 3 says "recomputed
  incrementally" while `next_ids` is a batch function, F-C6).
- **Owns:** A and B share `dispatch_gate.py`, `test_dispatch_gate.py` and RUNBOOK §12, so they are correctly ordered A → B (§D). B must add
  `plans/builder-rules.md` (B-2). F-A1 adds `handoff_gate.py` and `dod_gate.py` to A. Both are live hooks (`.claude/settings.json:51` for handoff_gate;
  dod_gate is a Stop hook), so they are STAGED in the worktree and the Lead places them. C is disjoint from A and B.
- **Live-hook protection while half-landed:** the hooks run as `python tools/<x>.py` relative to the session cwd (settings.json :29, :51, :66),
  i.e. the ROOT checkout's tree. A builder editing in a coordinator-made worktree and leaving the change staged never touches the live
  path. The Lead's merge into the root is the placement, which satisfies the enforcement-file review rule. Failure modes at placement:
  - dispatch_gate: a crash in `decide_full` fails open (`main()` `:1967-1972`), but a SyntaxError makes the hook exit 1 (non-blocking).
  - journal_validator: a crash blocks every commit through pre-commit.
  - journal_echo: a crash only warns.

  So C is the riskiest node to land. The spec should name a post-merge step: `python -B tools/hook_liveness_probe.py` (if that is the
  canonical form) plus one `journal_keys.py where` run (F-X2). Note: the root `main` is diverged (53/279). Landing means updating the
  root, and the Lead must do that knowingly.

---

## 8. Edges and tests (docs/TESTING.md)

One parametrized table per node. That is right for the table layer. Battery gaps:
- A: complete.
- B: **nesting missing.** Add a row: the branch only inside a fence/blockquote, with the decided expectation. Also a row for a remote-only branch named bare
  (expected: silent, named limit).
- C: **encoding and magnitude missing** (C-4): rows for a fullwidth band, a 10-digit and a 5000-digit band. AT/BEYOND on the
  digit bound, and on BAND_GAP_MIN (C-1). The rows for `where` bounded output (F-C2), and the compact_snapshot main path with a band (F-C3).

Empty/absent inputs are named in all three nodes (A e18, B b9, C j13 and "absent"). Conflicting pairs: A position invariant (i)-(iii),
B "WARN never changes the verdict", C "band first, then 9a on the same line". These are named.

---

## 9. Duplication, code quality, class-wide completeness

- **DUPLICATION AND CONSISTENCY:** found.
  - (1) The handoff candidate loop would exist in 3 copies (`handoff_gate.py:162-166`, `dod_gate.py:377-383`, the new A step 2.6), F-A1.
  - (2) The id regex: `journal_validator.TASK_ID_RE` `^t-(\d{3,})$` (`:311`) and `journal_keys` `^t-(\d+)$` (`:631`) already diverge.
    `next_ids` must be the one reader, with one bounded ASCII regex (C-2).
  - (3) The isolation-guard prelude would be twinned in the two B WARNs (F-B2).
  - (4) B-2: the "merge first" road would live on in builder-rules.

  Grepped: `"origin/main"` over `tools/*.py` (hits in dispatch_gate, piles.py `ORIGIN`, worktree_sweep `DEFAULT_REF`, tests);
  `dispatch_gate\.(decide|decide_full)|import dispatch_gate` (owns_gate, critic_snapshot, tests); the next-id grep of §1.
- **CODE QUALITY:** the plan's code shape is sound (lazy imports with a NOTE, try-wrapped layers, table tests). Issues: the B-3 helper,
  the C-2 regex placement, the C §C.3 step 3 state API (F-C6). These are listed above.
- **CLASS-WIDE COMPLETENESS (SIBLING_MAP):**
  - Axis 13: A adds a cut consumer, and the map line is owed by the Lead (stated).
  - Axis 1: C adds the next-id reader line (stated).
  - Axis 31/34: B-2 (open).
  - **Class "a short `origin/main` used as a single revision"** (the real class behind B6): the root cause is the registered
    worktree at `C:/QAFactory/forge-repo/origin/main`. The class-level fix is to remove it (`git worktree remove`), an environment act for the Lead.
    Its sibling producer is F6-39 (worktree sweep), which could flag a worktree whose path shadows a ref.
    I did not enumerate how `piles.py ORIGIN` and `worktree_sweep.DEFAULT_REF` are passed to git (single revision or range). **Request to the coordinator:**
    a scout question, "every git argv in tools/*.py that passes `origin/main` as a single revision", or make it moot by removing the worktree.
  - **Surface "task-id number parser"** (C-4): the two existing validator holes (5000-digit raise, fullwidth accepted) go to a
    finding with owns `tools/journal_validator.py` and a row each (P31 rule 19: a residual leaves as a node with an owner; the Lead opens it).
- **ONE ACTION, ONE ROAD (question 12):** B-F2 (a) is one road only after B-2. A: one predicate, three copies of the loop (F-A1).
  C: one door for the two id cases, plus `declare` for after-the-fact collisions. These are two roads at two different moments (before issuing, after
  merging), which is legitimate, but the spec should say why `declare` labels are not the road for one file (one sentence, F-C7).
  No language/project/case exclusion found.

---

## Spec edits

### Blockers (edit the spec before any builder dispatch)

**B-1** — §B.1 row B6: replace it with: "MEASURED 13.11 (critic t-371): from the root, `git rev-parse origin/main`,
`git rev-parse main` and `git rev-list --count origin/main..main` all exit 0 with empty stderr, so the push WARN is NOT silenced.
Single-revision forms (`git log origin/main`, `git rev-list --count origin/main`, `git worktree add <p> origin/main`) fail with
'ambiguous argument', because the root holds a registered worktree at `origin/main` (`git worktree list`)." §B.2 step 0: "done
(see B6)". Step 1: keep the qualified refs as hardening, and drop "defect B6 fixed". Row b12 becomes: "the fake git answers only the
qualified argv → the push WARN fires (pins the new argv)". Add to §0 a Lead-side environment item: remove the stray worktree.

**B-2** — §B.5 owns: add `<worktree>/plans/builder-rules.md`. §B.2: add a new step 4a. In item 20, replace "запушить `main` либо написать в
диспатче «сначала слей <sha>»" with "запушить `main` либо создать worktree самому (`git -C <repo> worktree add <path> -b <branch>
<base>`) и диспатчить без `isolation`". Non-goals: "builder-rules only item 20, that clause". Siblings: add "builder-rules item 20 (axis 31 owner)".

**B-3** — §B.2 step 2.4: "Use a new helper `_git_rc(args, cwd) -> int | None` beside `_git_out`. It runs `subprocess.run(['git']+args,
cwd=cwd, capture_output=True, timeout=5)` and returns `returncode`, or None on any exception. Never use `_git_out` for `merge-base
--is-ancestor` (it maps exit 0 and exit 1 both to None)." Add row b8a: is-ancestor exit 1 gives WARN, exit 0 is silent (the fake returns codes).

**C-1** — §C.2 and §C.4: add `BAND_GAP_MIN = 50` (fork C-F3 extension). A closed band needs `lo >= top + BAND_GAP_MIN`, else the
refusal NEAR: `{tag}: id_band {v} starts {gap} ids above t-{top:03d}; a closed band starts at least 50 ids above, or the other
writer's next id can land on its first id before this line is written -- start it at t-{s:03d} (rule 9e)`, where `s` = `top + 50` rounded up to
a multiple of 50. BELOW and JUMP suggest the same `s`. The open form keeps `lo > top`. `where` prints `suggested band:
t-{s}..t-{s+49}`. Rows: gap 49 → NEAR, gap 50 → pass. The CLAUDE.md sentence (§C.3 step 8) adds: "at least 50 above".

**C-2** — §0 "Small choices" and §C.3 step 1: "The band and id regexes live in `journal_keys` (the validator imports
journal_keys at module level, `:242-246`; the reverse would be circular): `BAND_RE = ^t-([0-9]{3,9})\.\.(?:t-([0-9]{3,9}))?$` and
`ID_NUM_RE = ^t-([0-9]{3,9})$`, used by `next_ids` and `id_band_of`. `journal_validator.TASK_ID_RE` is unchanged in this node (its holes:
finding)." State that `where`/`next_free_id` move from `\d+` to `ID_NUM_RE`, with no effect on today's journals (0 ids under 3 digits, measured).

**C-3** — §C.1 after C7, and §C.5's last bullet: "A band prevents a collision only after the writers know about each other. On 13.11 the
first round (t-347/t-348/t-349, lines 885-892) happened before either session knew, and is NOT prevented. The second round
(lines 900-908) is." Add fork **C-F6 (awareness)** with the options of §5 and recommendation (i): a NOTE from the SessionStart hook / journal_echo, when another
main-session transcript of this project changed within 10 minutes, naming `id_band`.

**C-4** — §C.6 j5: add the fullwidth band `"t-４００..t-４４９"` → FORM, `"t-1234567890.."` (10 digits) → FORM and `"t-"+"9"*5000+".."` → FORM
with no exception, and "9 digits" → pass. §C.5: "the number parser is ASCII and bounded (9 digits)". Siblings: "finding for
`journal_validator.TASK_ID_RE`: a 5000-digit task_id raises ValueError in `validate_new_lines`, and `t-００２` is accepted as t-002 (both
measured by critic t-371)", written by the Lead with a batch line (D-0044).

### Fixes (same fix round)

**F-A1** — Add `handoff_gate.handoff_candidates(cut, folders, base) -> list` (the dedup loop of `_gate:162-166`). `_gate`,
`dod_gate.named_handoffs` and `handoff_folder_check` call it. Owns: add `tools/handoff_gate.py`, `tools/dod_gate.py`, staged, and the Lead places
them (live hooks). The DoD already runs `test_handoff_gate.py`; add `test_dod_gate.py`.

**F-A2** — §A.2 step 3: update `decide_full`'s docstring order. Siblings: `owns_gate.py:1112` and `critic_snapshot` (`decide()`), and say that a refused
critic dispatch no longer overwrites the critic snapshot (desired). Add one row in `test_critic_snapshot.py`, or state that the existing M2-1 test
covers it.

**F-A3** — §A.4: add "NO_LINE and NO_PATH refuse a no-write critic/designer dispatch that the write gate never sees. This promotes
R11-h from discipline to a code gate, on the evidence of t-337 (`dev1.jsonl:853,856`)."

**F-B1** — §B.2 step 2.3: read tokens from UNQUOTED lines through `decision.cut` when it is not None and not degraded, else the whole prompt.
Add row b13 (branch only in a fence → silent) and row b14 (remote-only branch named bare → silent, named limit).

**F-B2** — Extract `_isolation_dispatch(payload) -> bool`, shared by both WARNs.

**F-C2** — `where` prints at most the 3 latest closed bands that still have a free id. A file whose bands are all used up prints none of them. Add a row.

**F-C3** — C-F4 widened: `compact_snapshot`'s main path (`:537-543`) prints the band lines next to NEXT FREE ID, so a session
keeps its band across /compact. Add row s2.

**F-C4** — §C.5 names the residual: two writers who declare overlapping bands at the same moment. The second meets BELOW after its dispatch
went out. Door: renumber as today. The rarity follows from C-F6.

**F-C5** — §C.8 (c): the detector reads the `t-NNN` of the dispatch's handoff section INCLUDING relative entries (scouts, per A-F2 (b)).
Name the reader: a new `dispatch_manifest.handoff_mentions(cut)` on `_section_paths` without the absolute filter, or the dispatch `description`.

**F-C6** — §C.3 step 3: name the state API: `journal_keys.BandState` with `add(obj)` (band first, then id) and `issuable() -> (main,
{band: next})`. `next_ids(objs)` is `BandState` fed over `objs`, and the validator feeds it line by line.

**F-C7** — §C.3 step 8: amend the existing clause "max(t-NNN)+1" itself ("the next id `journal_keys.py where` prints for your sequence or
your band"). Add one sentence on why `declare` labels are the after-the-fact road and bands the before-issuing road.

**F-X1** — Rule 10(b): replace "axes 20-30" and "axes 16-30" with one line per axis in all three blocks.

**F-X2** — §D: add the Lead's acceptance checklist per node:
- the SIBLING_MAP lines (A axis 13, C axis 1, C axis 14 if C-F6 (i));
- the calibration checks for B and C, registered in `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` in the same commit;
- the CLAUDE.md sentence (C) and the R11-h clause (A);
- the findings: A-F2 dod_gate, C-F5, C-4 TASK_ID_RE, and the `origin/main` single-revision class;
- the `очередь:` line F6-58 → F6-59;
- after the merge, a hook liveness probe and one `journal_keys.py where` run.

---

## Trail

Read:
- `docs/tasks/specs/t-366-f6-37-f6-35-f6-58-specs.md` (whole).
- read-main `tools/handoff_gate.py` (whole); `tools/dispatch_manifest.py` 60-209, 370-399, 630-894;
  `tools/dispatch_gate.py` 695-759, 1750-1800, 1960-2059; `tools/dod_gate.py` 286-395; `tools/journal_validator.py` 236-249,
  340-369, 870-1099, 1430-1509; `tools/journal_keys.py` 600-645 (+ grep of imports and labels); `tools/compact_snapshot.py` 320-334;
  `tools/critic_snapshot.py` 115-189; `.claude/settings.json` (grep of hook commands); `tools/critic_verdict.schema.json`.
- `docs/SIBLING_MAP.md` headings, 24-43, 311-346, 582-594; `docs/RUNBOOK.md` 575-605; `plans/builder-rules.md` 86-95;
  `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` 870-882; `CLAUDE.md` 234-238.
- The three findings (whole); `batch-1-onboarding-roles-forge.md` 1-16 and 58-72.
- Root: `logs/journal/dev1.jsonl` 880-930 (parsed), plus grep of t-337 and of isolation notes; snapshots
  `2026-11-13-1011-narrative.md:56` and `2026-11-13-0245-narrative.md:7-8`.
- Main-session transcripts (counts only): `acb1ecf0`, `bd2e9107`, `f92520fc`, `1624cb4a`.

Commands and results:
- `git -C <root> rev-parse origin/main` → 14c089f…, exit 0, stderr empty. `rev-parse refs/remotes/origin/main` → the same, exit 0.
- `git -C <root> rev-list --count origin/main..main` → 53, exit 0. The qualified form → 53, exit 0. The Python subprocess in hook form gives `0 '53\n' ''`.
- `git -C <root> log -1 origin/main` → fatal ambiguous, exit 128. `rev-list --count origin/main` → fatal ambiguous, exit 128.
- `git -C <root> worktree list | grep origin` → `C:/QAFactory/forge-repo/origin/main 0b76112 (detached HEAD)`; `origin/main/.git` →
  `gitdir: C:/QAFactory/forge-repo/.git/worktrees/main`; stat → created 2026-11-13 01:32-01:33.
- `git -C <root> rev-list --count main..origin/main` → 279; the merge-base is 1fd1b104e.
- Transcript grep for unescaped `"isolation": "worktree"`: 4 / 11 / 47 / 42. `PUSH BEFORE LAUNCH` hits: 0 / 0 / 4.
- Python 3.12.10: the band regex on fullwidth digits → True (400, 449). `int('9'*5000)` → ValueError.
- In memory, `journal_validator.validate_new_lines` (read-main), new delegated with task_id `t-`+5000×'9' → RAISED ValueError; with `t-００２` → [] (no violation).
- Grep `id_band` (-i) over root `logs/` → 0. Control `worker_ref` → 431.
- Grep short ids `t-[0-9]{1,2}` → 0. Control `t-[0-9]{3}` → 845.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B-1 (node B): B6 refuted by measurement. From the root, rev-parse origin/main, rev-parse main and rev-list --count origin/main..main all exit 0, so the push WARN is not silenced. The ambiguity hits single-revision forms only, and its cause is a registered worktree at C:/QAFactory/forge-repo/origin/main. Edit B6, step 0, step 1 and row b12 as in the review.",
    "B-2 (node B): B-F2 (a) drops the merge-first road, but plans/builder-rules.md item 20, which RUNBOOK item 8 calls the owner of the fact, still sanctions it. Add builder-rules.md to the owns and replace the clause.",
    "B-3 (node B): step 2.4 needs exit codes, and _git_out maps exit 0, exit 1 and errors all to None. Name a _git_rc helper and add row b8a.",
    "C-1 (node C): a band protects only by distance, yet BELOW and the CLAUDE.md sentence steer to top+1, which re-creates the 13.11 race at the band start. Add BAND_GAP_MIN=50 and the NEAR refusal, suggested starts and rows at 49/50.",
    "C-2 (node C): the band reader in journal_keys cannot use journal_validator.TASK_ID_RE (circular import, the validator imports journal_keys at module level 242-246). Define BAND_RE and ID_NUM_RE in journal_keys, ASCII, at most 9 digits.",
    "C-3 (node C): over-claim on the live case. Under rule 9e, collision round 1 (lines 885-892) is not prevented because neither session knew of the other; only round 2 (900-908) is. State the residual and add fork C-F6 (awareness), recommending a NOTE when another main-session transcript changed within 10 minutes.",
    "C-4 (node C): the band number parser accepts fullwidth digits (t-400..t-449 written fullwidth parses to 400,449, measured) and crashes on more than 4300 digits (int ValueError, measured). Add an ASCII bounded regex and rows in j5. The existing validator has both holes on task_id (measured: a 5000-digit id raises, fullwidth t-002 is accepted), so open a finding with owns journal_validator.py."
  ],
  "fixes": [
    "F-A1: one handoff_gate.handoff_candidates(cut, folders, base) called by _gate, dod_gate.named_handoffs and the new launch check (now 3 copies of the dedup loop); add handoff_gate.py and dod_gate.py to the owns, staged, Lead places them.",
    "F-A2: decide_full docstring order; name owns_gate and critic_snapshot as decide() consumers (a refused critic dispatch no longer overwrites the snapshot).",
    "F-A3: A.4 states that NO_LINE/NO_PATH promote R11-h into a code gate on the t-337 evidence.",
    "F-B1: token scan reads unquoted lines through decision.cut; rows b13 (fenced branch) and b14 (remote-only branch named bare, silent).",
    "F-B2: shared _isolation_dispatch(payload) prelude for both WARNs.",
    "F-C2: where prints at most the 3 latest closed bands with free ids.",
    "F-C3: compact_snapshot main path prints the band lines next to NEXT FREE ID (survives /compact); row s2.",
    "F-C4: name the residual of two concurrent band declarations.",
    "F-C5: detector reads t-NNN from relative handoff entries too (scouts under A-F2 (b)); name the reader.",
    "F-C6: name the incremental state API journal_keys.BandState add/issuable shared by next_ids and the validator.",
    "F-C7: amend the CLAUDE.md max(t-NNN)+1 clause itself; one sentence on declare (after the fact) versus band (before issuing).",
    "F-X1: one line per SIBLING_MAP axis in all three blocks (no ranges 16-30 or 20-30).",
    "F-X2: Lead acceptance checklist in section D: map lines, calibration checks for B and C registered in the same commit, CLAUDE.md sentence and R11-h clause, findings (A-F2 dod_gate, C-F5, TASK_ID_RE holes, origin/main single-revision class), the queue line F6-58 before F6-59, post-merge hook liveness probe and one journal_keys where run."
  ],
  "class_completeness": "Axis 13 (A new cut consumer) and axis 1 (C next-id reader) lines are owed by the Lead and stated. Axis 31/34 is open until B-2. The class behind B6 (short origin/main used as a single revision) has its root cause in a registered worktree at the repo root; the fix is to remove it (Lead). Siblings piles.py ORIGIN and worktree_sweep DEFAULT_REF were not enumerated: request a scout or make them moot by removing the worktree. Surface task-id number parser: two existing validator holes (measured) go to a finding with owns. Handoff candidate loop: three copies, fix F-A1.",
  "trail": {
    "read": [
      "docs/tasks/specs/t-366-f6-37-f6-35-f6-58-specs.md (whole)",
      "read-main tools/handoff_gate.py (whole)",
      "read-main tools/dispatch_manifest.py 60-209, 370-399, 630-894",
      "read-main tools/dispatch_gate.py 695-759, 1750-1800, 1960-2059",
      "read-main tools/dod_gate.py 286-395",
      "read-main tools/journal_validator.py 236-249, 340-369, 870-1099, 1430-1509",
      "read-main tools/journal_keys.py 600-645 and import/label grep",
      "read-main tools/compact_snapshot.py 320-334",
      "read-main tools/critic_snapshot.py 115-189",
      "read-main .claude/settings.json hook commands (grep)",
      "read-main docs/SIBLING_MAP.md headings, 24-43, 311-346, 582-594",
      "read-main docs/RUNBOOK.md 575-605",
      "read-main plans/builder-rules.md 86-95",
      "read-main PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md 870-882",
      "read-main CLAUDE.md 234-238",
      "read-main the three findings (whole) and batch-1-onboarding-roles-forge.md 1-16, 58-72",
      "root logs/journal/dev1.jsonl 880-930, t-337 lines 853/856, isolation-note grep",
      "root snapshots 2026-11-13-1011-narrative.md:56, 2026-11-13-0245-narrative.md:7-8",
      "main-session transcripts acb1ecf0, bd2e9107, f92520fc, 1624cb4a (counts only)"
    ],
    "reruns": [
      {"command": "git -C <root> rev-parse origin/main ; rev-parse refs/remotes/origin/main", "result": "both 14c089f..., exit 0, stderr empty"},
      {"command": "git -C <root> rev-list --count origin/main..main (short and qualified; also via python subprocess in hook form)", "result": "53, exit 0, stderr empty"},
      {"command": "git -C <root> log -1 origin/main ; git rev-list --count origin/main", "result": "fatal: ambiguous argument 'origin/main': both revision and filename, exit 128"},
      {"command": "git -C <root> worktree list (grep origin); cat origin/main/.git; stat origin/main", "result": "C:/QAFactory/forge-repo/origin/main 0b76112 (detached HEAD); gitdir .git/worktrees/main; created 2026-11-13 01:32"},
      {"command": "git -C <root> rev-list --count main..origin/main ; merge-base", "result": "279; 1fd1b104e (local main diverged 53/279)"},
      {"command": "grep unescaped isolation worktree and PUSH BEFORE LAUNCH in 4 main transcripts", "result": "isolation 4/11/47/42; push WARN 0/0/4"},
      {"command": "python: band regex on fullwidth digits; int of 5000 nines", "result": "match True (400, 449); ValueError digit limit"},
      {"command": "python in-memory journal_validator.validate_new_lines with task_id of 5000 nines, and fullwidth t-002", "result": "RAISED ValueError; [] no violation"},
      {"command": "Grep -i id_band over root logs/ ; control worker_ref", "result": "0 ; 431"},
      {"command": "grep task ids of 1-2 digits in root journals ; control 3 digits in dev1", "result": "0 ; 845"}
    ]
  }
}
```
