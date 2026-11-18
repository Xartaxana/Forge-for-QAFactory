# t-1173 — code critic, FV3-21 + FV3-21b (one topic), branch worktree-agent-af279738b46568113

Spec: card r2 `docs/tasks/specs/20261117-s6-manual-half-no-stand-card-r2.md` (whole, incl. Lead decisions and the owner's §OQ answers).
Diff: `git diff origin/main...HEAD` = 3286d19f, 1b3bbb4b (FV3-21), a1e9a77a (FV3-21b); 14 files, 492+/37-.

**Verdict: NEEDS WORK** — 0 blocking findings, 7 to fix before merge. The design holds: B1 = (b2) is put in as the card says, and the
dry run's measured stop shows the analyst at S7 being dispatched. Both roads write byte-equal records. The defects are on
the skill road's edges, in one FV3-21b test, and in the witness and node bookkeeping.

## Answers to the dispatch questions

1. **Byte-equal reason and door: YES for the record.** Both roads get `words` from `waiver.stand_passing_word` over the
   same `pipeline.json`. On the driver it is read through `hooklib.read_json`, on the skill road through `story_step._read_pipeline`.
   Both read utf-8-sig and both turn a non-dict into "". Then both call `manual_evidence.no_stand_refusal(words)` and write through
   `manual_evidence.write_case_refusal(..., "left_unchecked")` with `by_first=False` (driver: `refuse_case` default,
   driver_dialog.py:227/237), so the bytes are `{"refused": {"reason", "door", "by"}}` on both roads. The console lines differ by design:
   the driver prints an em dash and `s0_quote`, the skill road prints ` - ` and adds a revoke door. That door is broken (F1).
2. **Every case recorded before exit 2, nothing else written: mostly yes.** Each case of the block gets either prepare's own record
   (`prepare_to_file` writes it, manual_evidence.py:1191) or `write_case_refusal`. The return comes before `stamp_run_mode`, the
   stamp, the dispatch and the brief (story_step.py:913-917). Only `request.json` files are written, from manual_evidence.py:1187-1194/1277/1300.
   Exception: a case already covered by an accepted manual block, or carried by a live S6 dispatch, is overwritten too (F2).
3. **S4 keeps prepare's record: YES.** The `if why:` arm does not write (story_step.py:1067-1068), and the record is the one
   `prepare_to_file` wrote. Row S4 asserts there is no `by`, and its stub writes the record the way the real prepare does.
4. **FV3-21c named correctly: in CONTENT yes, as a NODE no** (F6).

## Findings

**F1 (fix before merge; FR-2, FR-1; AR-13): the skill road's revoke door cannot be used.** story_step.py:1074-1076 prints
`waiver.py --task <T> --revoke --stage S6 --block "stand not confirmed"`. I ran it verbatim on a byte copy and got
`waiver.py: error: --revoke needs --task, --stage, --block and --decision or --words-file (why, in their words)`
(waiver.py:1986-1988 of the arg block). The door has two more defects. `run_revoke` matches the stage and the `match` exactly
(waiver.py:1203-1205). For a word recorded on S5 (row S2's own world) it answers `S6 has no live override matching ... nothing to
revoke`. For a `*` word (W6's world) `--block "stand not confirmed"` matches nothing. On top of that, the block name is a
literal, while the card's own AR-13 change check (§4.2) bans a `stand not confirmed` literal in the story_step diff and the module
already takes block names from `waiver` (`MODE_SWITCH = waiver.MODE_SWITCH_BLOCK`, :701). The card's code snippet had the same text, so
this is a card defect too. Fix: build the door from the passing record. `waiver` gets a sibling reader that returns the live override
(`stage`, `match`, `decision`) and `stand_passing_word` returns its decision, so there is still one reader. Then print
`--stage <its stage> --block <its match, or waiver.STAND_NOT_CONFIRMED_BLOCK> --decision "<why, in the person's words>"`.
Add a row S2/W6 assertion on the door's stage.

**F2 (fix before merge; P31/Q12, card E6 and I-1 on the second road): the skill-road branch overwrites the request of a case that
is done or live.** Trace: block `[TC-2]` where TC-2 is in `controller.manual_done_cases(state)` (controller.py:678).
`_half_membership_problems` (controller.py:4277-4310) and `manual_block_problems` do not check done cases. So the branch runs
`prepare_for_block`, then `write_case_refusal`, and TC-2's request now holds `by: left_unchecked` over an accepted walk. All of this
happens inside `_manual_block_check`, before any controller apply. The driver protects the same case with `manual_todo`
(W7, E6), and its branch is not taken while any S6 dispatch is running, blocked or paused (I-1, E15). The skill road has neither.
The card's §4 was silent on this, which makes it a spec gap. Fix this round:
(a) skip the cases in `manual_done_cases(state)`, with one line `<case>: checked already by an accepted block`;
(b) take today's road while a live S6 dispatch exists. To keep one predicate (AR-15), lift the body of `Driver.s6_live_scopes`
(driver_stage_s6.py:1703-1710) into a pure function over `state` that both call; this touches FV3-21's file, which is the Lead's call.
Otherwise (b) becomes a row of the FV3-21c node (F6) with an owner. Doing (a) also brings `_manual_block_check` (now ~95 lines) back
under Q7: move the branch into a helper.

**F3 (fix before merge; Q5b): the FV3-21b test takes its expected door from the code.** In test_story_step_manual_block.py,
`fv3_21b_...` sets `door_text = manual_evidence.NO_STAND_DOOR`. The card §4.4 says "Literals REASON/DOOR as in K1", and §4.2 says
"S1 asserts byte-equal reason/door with the driver's W1 literals". As written, a change to `NO_STAND_DOOR` turns W1 red and leaves S1 green.
Fix: use the literal `"record a stand for this project with the onboarding; the next run checks it by hand"`.

**F4 (fix before merge; Q5f, rule 20): a1e9a77a adds 67 test lines against 20 product lines and has no `tests-over:` line.** A reason
would hold: card rows S1-S7, one table, plus the outside-input row S3 for the person's words. The fix-round commit has to carry it.
FV3-21's `tests-over:` (239 test lines against ~160 product) is named and holds: one table over one rig, prescribed by the card, with the
adversarial rows W4/W5/W5a for outside input.

**F5 (fix before merge; rule 7, mechanical layer; not executed by me): FV3-21b's witness is incomplete.**
`scenario_walk.py --witness-for` over its three owns names 54 distinct test files, including `test_story_run_s6.py`,
`test_story_step_start.py` and the whole scenario layer: cart_1, dry_1, local_1_0108, local_1_arm_b, walk, world (card §8, F9).
The layer attached by the builder shows 5. FV3-21's 121/123 run was made on 1b3bbb4b, before story_step.py changed. The probe was
missing, and I ran it (trail). FV3-21's four probes (p1-p3 and the K2 probe, card §8 DoD) are not in what reached me: request their
verbatim output. The batch canon does not stand in for the node's own witness (CLAUDE.md rule 4).

**F6 (Lead's tier; Q4/Q12d): the residual exists only as card text.** `git grep FV3-21c origin/main -- plans docs/tasks` finds only
the card. The control is the same grep for `FV3-21`, which finds batch-3 row :50. batch-3 has no FV3-21b row and no FV3-21c row, yet
the Lead decision R2-F1 says "a named node of the same pile". Proposed line for the Lead: `the skill road closes S6's manual half
when nothing is left to dispatch (card r2 §4.5; + F2(b) if not fixed now) | узел: FV3-21c` with owns
`story_step.py, test_story_step_manual_block.py, phases/s6.md`. The FV3-21c description in §4.5 is accurate: no skill-road
`code_only` writer, and `_manual_block_door` prints "nothing was dispatched".

**F7 (fix before merge; Q7): `consumer_need_record` nests 4 levels deep in new code** (driver_stage_s6.py:333-343: `if site` /
`if isinstance` / `if awaits == author` / `if awaits != author`). The card prescribed it, but the Q7 limit is 3. Fix: extract
`consumer_await(stage, author, state, route) -> bool`. It returns False on an unreadable pipeline or when the wait would not hold, so
the raise stays the only raise.

## Q1-Q12 lines

- Q1 fit: K1.a-e, K2, K3, K5-K8 and K4.b1-b3 are implemented as written. The error direction of K6 is checked by W13c and W13e
  (Refusal, no marker, bytes unchanged) and by W13d (the person's pass wins). Gaps: F1, F2.
- Q2 builder's own decisions: the door variable is renamed `no_stand_door` because an inner `door()` exists. Safe; not a finding.
- Q3 seams: `consumer_need_record` returns bool. The other callers (:809, :838, s7.py:526) ignore it and their sites are not in
  `await_at`, so they are unchanged. The quarantined 2-arg stub returning None means the close goes on.
- Q4 class: axis 26 has one reader, plus the `stand_check` loop the card keeps and `check_delivery.stand_word`, which already belongs to
  node OF5-5 (`plans/piles/onboarding-forge/batch-5-ostatki-hf8-4-i-oh3-42.md:32`). The card §6 F6 slot can point at it. Axis 19
  twin: S7 is unchanged, as the card reasons. Artifact sweep: E23 siblings close through one site (W13b). Gaps: F2, F6.
- Q5 tests: killing power for the skill road was confirmed by my probe (26 FAIL). Expected values: F3. Volume: F4. W12-W12c and
  C1-C6 are rows at the door.
- Q6 duplication: none new. Grep `stand_block(|STAND_NOT_CONFIRMED_BLOCK|stand_passing_word(` over scripts finds the known
  readers only. Grep `{"refused": ` shows `_write_refused` (manual_evidence.py:1272) as a pre-existing sibling writer with
  another shape (trace, no `by`). `manual_todo` and `s6_live_scopes` remove two copies.
- Q7 quality: F7; plus F2's note on the length of `_manual_block_check`.
- Q8 hygiene: the em dash is in prints the card prescribed; there is no Cyrillic. Not run: `selftest --lang` belongs to the canon.
- Q9 ratchets: known_red `main/S6` is rewritten in place, its content replaced by the measured S7 stop, and `pins.known_red` stays 1.
  The Lead decision to keep the key holds: the walk prints `main/S6` (J2-2 label, non-goal 7.6). But card K3 step 2 requires the
  Lead to name the S7 analyst-stub node BEFORE FV3-21 merges. The note "owed (Lead)" is a merge precondition, not a standing
  state. Driver-layers: 4 rows, no upward edge.
- Q10 architecture: the AR rows of §1.2/§4.2 are kept. AR-14: grep `_write_json|atomic_json` over added non-test lines finds only
  `write_case_refusal` and the pipeline.json marker. AR-1: `"manual_close"` appears in no comparison; the control finds
  `"await_at": ("manual_close",)`. AR-13: F1.
- Q11 judgment: none moved. The census is 25/25 per the builder.
- Q12 one road: F2 (the skill road lacks the done and live filters), F6.

Lead-owed, not code findings: the SIBLING_MAP axis 26 lines (card §6) go in at wave merge. The R2-F3 dry-run marker finding is not
filed: `git grep -i acceptance_awaits origin/main -- plans` returns empty, and the control is the same grep finding the stand-word finding
in `onboarding-forge`.

## Trail

Read: card r2 (whole); critic.md rules 21-24; diff of all 14 files; story_step.py 880-925, 990-1130, 745-760; manual_evidence.py
1150-1200, 1270-1330; driver_core.py 310-330, 610-625; hooklib.read_json 873-883; waiver.py 52-58, 161-222, 1193-1210, 1960-2000;
controller.py 678-696, 4277-4312; driver_stage_build.py 150-215; TESTING.md 204-233; batch-3 file (grep); OF5-5 finding head.
Re-runs (on a `git archive a1e9a77a` copy in the scratchpad; the worktree was not touched, and `git status` shows 0 changes):
- `python -B .../test_story_step_manual_block.py` gave `=== test_story_step_manual_block: 234/234 ok ===` (1m22s). It matches the attached layer.
- PROBE on the copy (the `return` of the `if words:` branch turned into an assignment, ast-parsed) gave `=== ...: 208/234 ok ===`, with
  `FAIL S1: exit 2 — expected 2, got 0` and `FAIL S1: nothing dispatched — expected (16, []), got (17, ['TC-2,TC-3'])`.
  Restored from the byte copy: sha256 `5865be0e...86dd6` before and after.
- `python -B waiver.py --task QA-9 --revoke --stage S6 --block "stand not confirmed"` (the copy) gave `error: --revoke needs ... --decision`.
- `scenario_walk.py --witness-for <FV3-21b owns>`: 54 distinct test files.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "Axis 26: one reader waiver.stand_passing_word for driver and skill road; check_delivery.stand_word is node OF5-5. Axis 19: S7 twin unchanged, as the card reasons. E23 siblings close at the one site (W13b). Gaps: the skill road lacks the driver's done-case and live-dispatch filters (F2); the FV3-21c residual has no node row in batch-3 (F6, Lead).",
  "fixes": [
    "F1 story_step.py:1074-1076: the revoke door is refused by waiver argparse (no --decision), names --stage S6 for an S5 word and cannot match a star word; build it from the passing override's stage and match, use waiver.STAND_NOT_CONFIRMED_BLOCK, add --decision",
    "F2 story_step.py:1060-1076: skip cases in manual_done_cases(state) and take today's road while a live S6 dispatch exists (shared pure predicate lifted from Driver.s6_live_scopes), or move (b) into the FV3-21c node; move the branch into a helper",
    "F3 test_story_step_manual_block.py fv3_21b: door_text from manual_evidence.NO_STAND_DOOR; use the card's literal DOOR",
    "F4 a1e9a77a: 67 test lines against 20 product lines with no tests-over line; the fix-round commit carries it",
    "F5 FV3-21b witness: 54 files named by witness-for, 5 run (test_story_run_s6, test_story_step_start and the scenario layer missing); FV3-21 probes p1-p3 and the K2 probe output not attached",
    "F6 Lead: open FV3-21c (and record FV3-21b) as batch-3 node rows; name the S7 analyst-stub node in known_red before the merge (card K3 step 2)",
    "F7 driver_stage_s6.py:333-343: 4 nesting levels in consumer_need_record; extract a consumer_await helper"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-s6-manual-half-no-stand-card-r2.md",
      ".claude/agents/critic.md 178-282",
      "git diff origin/main...HEAD (14 files)",
      "ai-packages/qa-factory/scripts/story_step.py 745-760, 880-925, 990-1130",
      "ai-packages/qa-factory/scripts/manual_evidence.py 1150-1200, 1270-1330",
      "ai-packages/qa-factory/scripts/waiver.py 52-58, 161-222, 1193-1210, 1960-2000",
      "ai-packages/qa-factory/scripts/controller.py 678-696, 4277-4312",
      "ai-packages/qa-factory/scripts/driver_core.py 310-330, 610-625",
      "docs/TESTING.md 204-233",
      "plans/piles/live-run-fvf/batch-3-live-run-fvf.md (grep)",
      "plans/piles/onboarding-forge/batch-5-ostatki-hf8-4-i-oh3-42.md:32"
    ],
    "reruns": [
      {"command": "python -B <copy>/scripts/tests/test_story_step_manual_block.py", "result": "234/234 ok"},
      {"command": "PROBE: if-words return turned into assignment on the copy, same test", "result": "208/234 ok, S1-S4 red; restored, sha256 equal"},
      {"command": "python -B <copy>/scripts/waiver.py --task QA-9 --revoke --stage S6 --block \"stand not confirmed\"", "result": "argparse error: --revoke needs --decision or --words-file"},
      {"command": "scenario_walk.py --witness-for <FV3-21b owns>", "result": "54 distinct test files named"}
    ]
  }
}
```
