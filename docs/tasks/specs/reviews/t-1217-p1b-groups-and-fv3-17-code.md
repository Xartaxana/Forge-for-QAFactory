# t-1217 — critic of one topic (R13-g): P1-b walk groups s5 (t-1193), s6-s9 (t-1194), FV3-9 (t-1204), FV3-17 code (t-1210)

Critic (Opus), 2026-11-17. Node `live-run-fvf/3/FV3-9` (topic). Spec: `docs/tasks/specs/20261117-p1b-finish-spec.md` §4 N4 card (edges 1-11),
§7.1 F-P4/F-P8 with the Lead decisions (t-958), batch-3 rows FV3-7/8/9/17; findings FV3-17 and FV3-25.

**Verdict: NEEDS WORK — 3 blocking findings (B1 s5, B2 s6-s9, B3 FV3-17), 9 fixes to land before merge.**
Per node: s5 — needs_work (B1); s6-s9 — needs_work (B2); FV3-9 — fit_with_fixes; FV3-17 — needs_work (B3).
This verdict is an input to acceptance. Accepting or rejecting the nodes, the decisions and the statuses belongs to the Lead.

## The fact the topic turns on: what a start snapshot `S<n>` is

`dry_world.drive_main` takes snapshot `S<n>` at the end of the turn in which stage `S<n>` became `done`
(`dry_world.py` `drive_main`: `if state[stage] == "done" and not (snaps / stage).is_dir(): snapshot(world, stage)`). A turn runs until
the next question (`--max-boundaries 60`). So `S<n>` is the world AFTER `S<n>` closed, waiting at the next question. I checked this
against real output, not only the code. The s5 canon 44122122853 (job 134176291628) prints:

```
NOTE dry-1/exits:s5/snapshots: S0: last closed S0? waiting at s1_review (S1)? stages S0 done, S1 running
NOTE dry-1/exits:s5/snapshots: S1: last closed S4? waiting at gate_A (S4)? stages S0 done, S1 done, S2 done, S3 done, S4 done
NOTE dry-1/exits:s5/snapshots: S4: last closed S4? waiting at gate_A (S4)? stages S0 done, S1 done, S2 done, S3 done, S4 done
NOTE dry-1/exits:s5/snapshots: S5: last closed S5? waiting at exit_limit (S6)? stages S0 done, ... S5 done, S6 running
```

What follows: a question asked INSIDE stage `S<n>` can never be reached from start `S<n>`. In this world, S1 to S4 close in one turn,
so snapshots S1, S2, S3 and S4 are all the same world, waiting at gate_A. A row that comes after its own stage fails `run_seed`. I traced
it: `_holds` is false because the pending ask is at S6, then `answers.get(("S6","exit_limit"))` is None, which returns
`met exit_limit at S6 with no answer in story.json (A1-E3)`. That is the exact "measured cause" of the s5 group and of the s6-s9 fix round.
gate_A rows are right with start S4 because gate_A is the question that comes AFTER S4 closes. The groups copied the form "start = the
stage label of the ask" without that property.

## Findings

**B1 (blocks, s5 / FV3-7): the 36 `live_only` rows of nine S5 keys rest on a start that comes after the ask; the measured cause is wrong.**
`exits/s5.json` gives `s5.repair_limit`, `s5.nobody_review|environment|tooling`, `exit.resume_limit`, `exit.resume_limit_halted`,
`code_close.stage|factory_file|behind` all start `S5` (my per-class tally, trail). Their canon 44119861422 failure comes from that start,
not from the world: S5 was already closed, so the stub control `qa-code-critic verdict reject` never ran. From S4 the row's drive would
answer gate_A with the story's words (`story.json` walk S4 `gate_A`) and S5 would run under the control. The Lead decision "S5-question
rows live_only with measured cause" therefore hides rows that no measurement has tried. That breaks the dispatch key "no row hidden as
live_only that a seed can reach" and edge 3. The 36 `raised_by` entries of round 3 name the same false cause. So does finding FV3-25
("сухая S5 проходит чисто"): no row of it ran S5.
Fix: the asks inside S5 start from `S4` with `drive_until {S5, <key>}`. Put back the round-2 recipes and the critic-reject stub on
`s5.repair_limit`. The canon then judges. Only rows that still are not reached become `live_only`, with the new cause and their
`raised_by`. Rewrite FV3-25's "Что не так" from the new run.
The same surface (start vs ask stage) also covers the S6 rows of this group: `s6.walk_*`, `s6.data_change` and `kind:data_change|walk_*`
start `S6`. The asks are in `driver_dispatch.py:3529/3652/3700`, inside S6. They print `after:FV3-21` today, but once FV3-21 lands they can
never be reached (S6 will be closed in snapshot S6). They belong at start `S5`. They will then be red for the main stop's own cause
(exit_limit at S6) and need a `known_red/s5.json` label with the id already issued for that cause (FV3-21). That is a ledger raise and
must be named. `code_close.closed_story` starts `S9`, but the ask is the code close of stage S9 (`driver_machine.py:2094`). Read it before
keeping S9: it is likely `S8` (estimate, not verified).

**B2 (blocks, s6-s9 / FV3-8): the Lead decision "stand_confirm start moved to S6" contradicts the ask site; the 7 rows can be reached today and are hidden under `after:FV3-21`.**
The dry story asks the stand at S5. `driver_stage_s5.py:201` and `:330` call `self.stand_check("S5")`. `story.json` walk S5 answers
`environment`. The main ledger's own text says so too (`known_red.json` `main/S6`: "after the person's `go on` on the stand (answers S5
`environment`, price key s6.stand_confirm)"). The fix round reasoned that the pass "went through S5 with no such ask". That is the same
start artifact: from snapshot S5 the pass never re-ran S5. With start S6 the rows are notes today. After FV3-21 they can never be reached,
because S6 will already be closed. Fix: `s6.stand_confirm/*` start `S4` with recipe `drive_until {S5, s6.stand_confirm}`. `_holds` matches
the ask by its window's last key (`window[-1].key`), even though the ask's kind is `environment`. Read the ask site of
`s6.stand_confirm.login` for its stage the same way.
The same class runs through the rest of the group, one stage too late each time: `s6.stand_login` (ask `driver_stage_s6.py:1240`),
`s6.gate_a_dry` (`:1016`, stage S6) → `S5`; `s7.*` (`driver_dispatch.py:3375-3382`) → `S6`; `s8.*` → `S7`. `closed.held`: the ask is
raised with the stage of the held piece, `Person("closed_held", text, str(held[0].get("stage") or ""))` (`driver_machine.py:1452`), not
S9. So the recipe `drive_until {S9, closed.held}` can match only when the held piece is an S9 piece. Read the site and fix the recipe stage
or its cause. All these rows print `after:FV3-21` today, so none of them is red yet. They are still wrong rows: each turns into a FAIL
"seed did not reach" once the main pass moves on.

**B3 (blocks, FV3-17): Cyrillic in a package file.** `scripts/tests/dry_exits.py:2563` reads
`("FV3-17 offered_if a unicode key", wrow(offered_if="факт"), ...)`. It is a raw UTF-8 literal (bytes `\xd1\x84\xd0\xb0\xd0\xba\xd1\x82`),
not escapes, as the report claims ("unicode test key written as escapes"). On the merged tree, `selftest.py --lang` gives
`FAIL lang: no Cyrillic anywhere in the package — 1 file(s) - scripts\tests\dry_exits.py` (FR-30, Q8). Fix: `"факт"`.
This was a false load-bearing claim in the report (rule 12).

**F1 (fix before merge, FV3-17, error direction): the condition's early return drops the always-checks.**
`judge_row` returns `_offered_if_outcome` BEFORE the listed checks, `_na_guards` and `_judge_always` (K15/E17, E18, route record). Take a
row `s1.review/unavailable` + `offered_if` in a world where the inventory is complete and the product records no price row. K15 would
FAIL, and the verdict prints NOTE `unreached`. A FAIL becomes a NOTE (AR-28). The spec gave a verdict for the condition only. Fix: work
out the condition's outcome, still run the checks that judge the ASK and not the answer, and let a FAIL win.

**F2 (fix before merge, FV3-17, the builder's own decision): "condition not met, token offered" is judged as before.**
The product offers the answer while the walker's fact says it should not. That is exactly the drift between the walker's copied
predicate and the product's (F3). The judge now passes it without a word. Fix: FAIL `offered_if <key> does not hold, yet <token> was
offered: the row's condition or the product's offer rule changed`. That is the detector of F3's duplication.

**F3 (Q6 duplication, node): the predicate is copied, and its edges disagree.** `dry_world.inventory_unavailable` copies
`driver_sources.py:755-761`, the same calls `SI.completeness(SI.load_inventory(..), **SI.class_kwargs(..))` with
`unavailable or unavailable_materials`. The product reads a missing or unreadable inventory as offered (`asked_open = True`, `:754`,
`:762`). The walker returns None, which gives a FAIL "no world". So the claim "nothing re-implemented" is half true. FV3-17 cannot edit
product code (its owns). Proposed node, owner Lead: one product predicate (e.g. `source_inventory.asked_open(task_root)`), called by
`driver_sources` and by `WORLD_FACTS`. Until then F2 is the guard.

**F4 (Q7, FV3-17):** `inventory_unavailable` has `except Exception: return None`. A broken reader (a signature change of `class_kwargs`)
reads as "no world" and points the door at "add a reader". Narrow the catch to `OSError`/`ValueError` or carry the exception text into the
fact. `judge_row`: `na =(row.get(...` lost its space. The comment at `dry_exits.py:59-60`, "closed vocabularies are data tuples HERE and
nowhere else", is now false for `WORLD_FACTS`. Name the exception there.

**F5 (FV3-17 class completeness, node): one fact for a class of about 20 rows.** Edge 10 left 13 answers out of s5 (s5 report round 2:
`s5.repair_limit/round|fixed`, `exit.resume_limit*/round|fresh|go on`, `code_close.behind/go on`, `code_close.closed_story/full retro|retry|go on`)
and 6 out of s6-s9 (report: `s6.stand_confirm/retry|stand name`, `.login/find the way in|stand name`, `s7.repair_limit/round`,
`s6.gate_a_dry/reapprove`). Each is written "→ FV3-17". FV3-17 ships only `inventory_unavailable`, and its item 2 (bring
`s1.review/unavailable` back) has no node. Nobody owns them, so per rule 9 they need a node with an executor: the readers per condition,
or Lead's word that a given condition stays dropped. Item 2 must follow the FV3-9 merge (FV3-9 owns `exits/s1-s4.json`).

**F6 (FV3-9, rule 7): the report does not describe the branch.** The report on `d3f4f41b` still says "node NOT green, 1 discrepancy", and
still lists questions 1-3 as open. The branch's commits `a5ef84e6` (153 `raised_by`, FV3-16 labels) and `d3f4f41b` (`halt/stop` label,
canon 44124601253) carry no witness in it. Fix: add a final-round section with the `--check` tail and the Lead's answers. My control run
on the merged tree is green (trail).

**F7 (FV3-9, dispatch key "no row hidden as live_only"): `package.mode/*` (5 rows) is `live_only` though an allowed op is named and untried.**
Its `why_unreached` reads "Candidate not tried: a seed op story_step.py start would stamp mode desktop". `story_step` is on the closed op
list (`dry_world.run_seed`). Fix: write it as a `story` row with recipe `op story_step.py start …` + `drive_until`, and let the canon
measure it. `live_only` only with the measured cause.

**F8 (FV3-9, start claims): S(n-1) is not this world's rule.** `questions*` start S1, `s3.*`/`first_look.*` start S2 and
`s4.repair_limit` starts S3. Those snapshots all sit at gate_A with S4 closed (canon lines above). Every one of these rows is `live_only`,
so no verdict changes today, but `start` is a claim the next story conversion inherits. Fix: start `S0` (waiting at s1_review, S1
running) for asks inside S2-S4.

**F9 (FV3-9, data quality):** the 153 new `raised_by` entries in `driver-exits/s0.json` and `s1-s4.json` are cut at 200 chars mid-word
("...ticket fails f", "...has a ", "...dry world'"). Write the `who, where` + "same reason as walk/<id> why_unreached" form the file
already uses (`N4:s0 t-824: same reason as ...`).

## Lead decisions judged

| Decision | Judgment |
|---|---|
| S5 rows live_only, measured cause, `raised_by` per row (F-P8 reading 2, double count) | The double count stands as decided: a census row plus walk rows, with FV3-14 later. The measured cause is wrong: B1 |
| stand_confirm start moved S5 → S6 | Wrong direction: the ask is at S5, so the start is S4 (B2) |
| halt/words, halt/free words, halt/stop → FV3-16 | Holds. Same ask and words as `kind:halt/free words` (FV3-16). `halt/stop` follows the precedent of `gate_A/stop` → FV3-16 (`known_red/gates.json`, critic t-1077). The canon green on a pin of 4 shows all three are red as labelled (`known_red.py` reconcile would make a green row "stale") |
| FV3-17: `inventory_unavailable` through `source_inventory.completeness` + `WORLD_FACTS` | Right reader, right place. Edges diverge (F3), drift goes undetected (F2), and the early return drops the always-checks (F1) |

## Standing questions

- Q1 fit: s5 and s6-s9 fail the key "start read at its ask site" (B1, B2). FV3-9: F7, F8. FV3-17: the three outcomes are implemented as the finding asks (selftest rows).
- Q2 the builder's own decisions: FV3-17's "not met + offered → as before" is not in the safe direction (F2).
- Q3 seams: the four file sets are disjoint. None of these files changed on main since each branch's merge base (`git diff --name-only <base> origin/main -- <files>`: empty for all four). `merge-tree` against `origin/main` is clean for all four.
- Q4 class: start vs ask stage runs through both groups and FV3-9 (B1, B2, F8). A walker detector would close this class for every group. In `run_seed`'s `drive_until`, when the target stage is already `done` in the start copy and no ask is pending at it, say "start S<n> is past stage S<m>" instead of a misleading `met <x> at <y>`. Proposed node in `dry_world.py`, owner Lead. Conditional offers: F5. Axis 5: the twins `kind:halt`/`halt` and `kind:walk_*`/`s6.walk_*` both have rows, so it is covered. Axis 34: no new road. Axis 38: census rows are added with `raised_by`.
- Q5 tests: FV3-17 adds 7 grammar rows + 6 judge rows, all in the existing table (`--selftest` 214/214). Expected values trace to finding FV3-17 «Что именно менять» items 1 and 3. The reader `inventory_unavailable` has no row through a real inventory: its scenario is item 2 (F5). The group diffs are data rows. Each report gives the reason for its volume: s5 has an explicit `tests-over:` line; s6-s9 and FV3-9 count their rows (56; +104/+53) and the card's key-coverage rule but write no `tests-over:` line, and the commit's line is the Lead's to check at merge.
- Q6 DUPLICATION AND CONSISTENCY: F3. Searched: `grep -n unavailable driver_sources.py`, which found the predicate at `:752-770`; no other `completeness(` caller in `scripts/tests/` except the new one.
- Q7 CODE QUALITY: F4. The new functions are short: `_walk_offered_if_problems` 15 lines, `_offered_if_outcome` 19, `inventory_unavailable` 14.
- Q8 hygiene: B3 (FR-30). Group JSON is ASCII (`ensure_ascii`).
- Q9 ratchets, row by row. s5: `unwalked` base 33 → 0; `live_only` +66 `raised_by` (30 census joints + 36 walk rows, the latter wrong per B1). s6-s9: `unwalked` 6 → 0; +6 census `live_only`. FV3-9: +100 (s0) +53 (s1-s4) `live_only` `raised_by`; `known_red/s0.json` pin 1 → 4 (`halt/words`, `halt/free words`, `halt/stop` → FV3-16, an existing node). FV3-17: no ratchet.
- Q10 architecture: FV3-17 names AR-1, AR-28 and AR-29. AR-13 is claimed and is half kept (F3). AR-28 is weakened by F1.
- Q11 judgment: none. The condition is a data key read through a fact table; no role output is classified.
- Q12 ONE ROAD: none found. Searched the diffs for a language/project/runner branch: the FV3-17 code has none; the groups are data.
- Merge order: no textual conflicts, and the census merges cleanly (merged tree `--check` 0). The only order is FV3-9 before FV3-17 item 2. Fix rounds of B1/B2 add `known_red/s5.json` / `known_red/s6-s9.json`, new files, no overlap.

## Spot-checks of submitters' claims

- "dry world asks stand_confirm at S6" (s6-s9 fix round): refuted, `driver_stage_s5.py:201,330` + `story.json` S5 `environment`.
- "S5 fault states unreachable, measured" (s5 round 3, FV3-25): refuted as a measurement (snapshot S5 line above).
- "unicode key written as escapes" (FV3-17): refuted (byte scan, `--lang` FAIL).
- "FV3-17 reads the product's own call": confirmed for the readable path (`driver_sources.py:757-759`), diverges on missing/unreadable (F3).
- FV3-9 "1 discrepancy": stale; merged tree 0.

## Trail

Read: the spec §4 N4 card, §7.1, Lead decisions (`:773-837`); batch-3 rows 36-54 and «Ход»; findings FV3-17 and FV3-25; four reports
(worktree paths as given); `git diff --stat` + per file for the four branches; the FV3-17 code diff whole; samples per class of
`exits/{s5,s6-s9,s0,s1-s4}.json` (scratch tallies by key/start/reach/seed); `seeds/{s5,s6-s9,gates}.json`; `driver-exits/known_red/{s0,gates}.json`,
`known_red.json`; `dry_world.py` (`drive_main` 888-915, `_holds`, `run_seed`, `run_exit_row`), `dry_exits.py` `judge_row`;
`driver_sources.py:740-771`, `source_inventory.py` `class_kwargs`/`completeness` signatures; `driver_stage_s5.py:201,330`,
`driver_stage_s6.py:517,976-1016,1240`, `driver_machine.py:1428-1456,2094`, `driver_dispatch.py:3375-3382,3529,3652,3700`;
`question-prices.json` `halt`; `story.json` walk answers.

Runs (merged tree = `origin/main` b5fca9bd + the four branches' files, archived to scratch):
- `python -B <merged>/scripts/tests/dry_exits.py --check` → `NUMBER ratchet (rows now / base): live_only 293/0, after 0/0, unwalked 231/0, hook_layer 77/77; raised_by 524` … `dry_exits --check: 0 discrepancies`
- `python -B <merged>/scripts/tests/dry_exits.py --selftest` → `dry_exits selftest: 214/214 cases`
- `python -B <merged>/scripts/selftest.py --lang` → `FAIL lang: no Cyrillic anywhere in the package — 1 file(s)  - scripts\tests\dry_exits.py`; `=== qa-factory selftest: 1/2 ok ===`
- `git merge-tree --write-tree --name-only origin/main origin/<branch>` ×4 → a tree id, no conflict lines
- `python -B tools/ci_read.py log 134176291628 --grep dry-1` → the snapshot and `after:FV3-21` lines quoted above

```json
{
  "verdict": "blocker",
  "blockers": [
    "B1 s5/FV3-7: 36 live_only rows of nine S5 keys start S5 = after S5 closed (canon snapshot S5: S5 done, waiting at exit_limit S6); the measured cause is an artifact of the start; asks inside S5 start S4 with drive_until S5; S6 rows of the group start S5 with a FV3-21 label",
    "B2 s6-s9/FV3-8: stand_confirm start S6 contradicts the ask site driver_stage_s5.py:201,330 and story.json S5 environment; reachable today from S4, hidden under after:FV3-21; the rest of the group starts one stage late (s6 to S5, s7 to S6, s8 to S7; closed.held recipe stage vs held[0].stage)",
    "B3 FV3-17: Cyrillic literal in scripts/tests/dry_exits.py:2563 (offered_if unicode case); selftest.py --lang FAIL on the merged tree; the report's claim of escapes is false"
  ],
  "fixes": [
    "F1 FV3-17 judge_row: the offered_if early return skips the always-checks; run the ask checks and let a FAIL win over the unreached NOTE",
    "F2 FV3-17: condition not met but token offered must FAIL as drift instead of passing",
    "F3 node (Lead): one product predicate for the s1.review unavailable offer, called by driver_sources and dry_world.WORLD_FACTS; edges on a missing or unreadable inventory diverge today",
    "F4 FV3-17: narrow except Exception in inventory_unavailable; restore the space in na =(; update the closed-vocabulary comment at dry_exits.py:59-60",
    "F5 node (Lead): readers or Lead word for the 19 conditionally offered answers dropped in s5 and s6-s9, plus FV3-17 item 2 after the FV3-9 merge",
    "F6 FV3-9: report final-round section with the check tail and the Lead answers",
    "F7 FV3-9: package.mode rows as story rows with the story_step start op recipe, measured by the canon",
    "F8 FV3-9: rows asked inside S2-S4 start S0, not S1-S3",
    "F9 FV3-9: raised_by entries cut mid-word at 200 chars; use the file's same-reason form"
  ],
  "class_completeness": "Class start-versus-ask-stage spans s5, s6-s9 and FV3-9 rows (B1, B2, F8); proposed walker detector node in dry_world.run_seed. Conditional offers: one fact shipped for about 20 dropped answers (F5). Axis 5 twins covered; axis 34 no new road; axis 38 census raises named row by row.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-p1b-finish-spec.md (section 4 N4, 7.1, Lead decisions)",
      "plans/piles/live-run-fvf/batch-3-live-run-fvf.md",
      "plans/piles/live-run-fvf/findings/20261117-p1b-uslovnyj-otvet-bez-usloviya-u-hodoka.md",
      "plans/piles/live-run-fvf/findings/20261117-p1b-s5-fault-states-unreachable-in-dry-world.md",
      "four builder reports (s5, s6-s9, fv3-9, fv3-17)",
      "git diff origin/main...origin/<branch> for the four branches; FV3-17 code diff whole",
      "fixtures/stories/dry-1/exits and seeds of s5, s6-s9, s0, s1-s4, gates (sampled by class)",
      "fixtures/driver-exits/known_red.json, known_red/s0.json, known_red/gates.json",
      "scripts/tests/dry_world.py drive_main, _holds, run_seed, run_exit_row",
      "scripts/tests/dry_exits.py judge_row",
      "scripts/driver_sources.py 740-771; scripts/source_inventory.py class_kwargs, completeness",
      "scripts/driver_stage_s5.py 201, 330; driver_stage_s6.py 517, 976-1016, 1240; driver_machine.py 1428-1456, 2094; driver_dispatch.py 3375-3382, 3529, 3652, 3700",
      "references/question-prices.json halt; fixtures/stories/dry-1/story.json walk answers"
    ],
    "reruns": [
      {"command": "python -B <merged tree>/ai-packages/qa-factory/scripts/tests/dry_exits.py --check", "result": "dry_exits --check: 0 discrepancies (live_only 293/0, unwalked 231/0, raised_by 524)"},
      {"command": "python -B <merged tree>/ai-packages/qa-factory/scripts/tests/dry_exits.py --selftest", "result": "dry_exits selftest: 214/214 cases"},
      {"command": "python -B <merged tree>/ai-packages/qa-factory/scripts/selftest.py --lang", "result": "FAIL lang: no Cyrillic anywhere in the package - 1 file(s): scripts/tests/dry_exits.py; selftest 1/2 ok"},
      {"command": "git merge-tree --write-tree --name-only origin/main origin/<branch> (x4)", "result": "clean, tree ids only"},
      {"command": "python -B tools/ci_read.py log 134176291628 --grep dry-1", "result": "snapshot S5: S5 done, waiting at exit_limit (S6); S1..S4 all waiting at gate_A; S6-start rows after:FV3-21"}
    ]
  }
}
```
