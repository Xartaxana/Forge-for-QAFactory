# t-094 — critic on code: PC2-3 (t-092, pile package-ci, batch 2; F19)

Diff under review: the UNCOMMITTED worktree `C:\QAFactory\forge-repo\.claude\worktrees\agent-a8a5c4097e72f3c66`
(base 0f289a0), 7 files, +70/-24. Spec: the Lead's dispatch items 1-4 (inline in the t-094 dispatch) and the finding
`plans/piles/package-ci/findings/20261105-hvosty-kritika-gm3-2-obshchie-helpery-priemki-s6-i-podpisi-byudzheta.md`.
Mechanical layer: the builder report `docs/tasks/specs/reports/t-092-pc2-3.md` (rounds 1 and 2), attached.

**Verdict: NEEDS WORK (fit_with_fixes) — 0 blockers, 5 fixes.** The verdict is an input to the Lead's acceptance, not the
acceptance itself.

## Findings

### F1 (fix before merge) — the move loosened the AWAITS checks: a bare word now passes where the driver would lose it

Surface: the test normaliser of the open-work word (`story_run_common.awaits`, `_Awaits.__eq__`).

- Before: `_Awaits.__eq__` was `getattr(other, "unresolved", None) == "stage_awaits_acceptance"`; a bare string compared
  False. After: `story_run_common.awaits(other) == ...`, and `awaits` returns a string as itself.
- Probe (run in the worktree): `T.AWAITS == 'stage_awaits_acceptance'` -> `True`; the old form on the same input -> `False`.
- Why that matters: `driver_dispatch.finish` (driver_dispatch.py:768-809) carries the word ONLY for an `OpenWork`
  (`isinstance(complete, OpenWork)`), then branches on `complete is True` / `complete is False`. A bare string
  `"stage_awaits_acceptance"` as `complete` is neither, so the finish sends neither `--complete` nor `--not-complete` and
  no `--unresolved`: the awaiting word is lost. Scenario: a regression in `consumer_awaits` (driver_stage_s6.py:165) that
  returns `acceptance.AWAITS_WORD` instead of `OpenWork(...)`. The old `_Awaits` turned red; the new one passes. The
  15 `AWAITS` uses in test_story_run_s6.py and test_story_run_deferred.py:107 (`[e["complete"] for e in launched] == [AWAITS]`,
  where `launched` holds the raw `complete`, story_run_common.py:698 / test_story_run_s6.py:335) are all weaker.
- Same loosening at test_story_run_s7.py E9 (`:966`): it was `getattr(ruled(complete), "unresolved", None)`; it is now
  `awaits(...)` with no type half. (ts5 at `:934` keeps `type(kept).__name__`, so it is still strict; q9c in test_s7_rejudge
  was loose before the diff too.)
- The builder flagged the change (report item 1, "Behavioural note"); nobody decided it. The finding's definition of `awaits`
  is fine for a NORMALISER. The fault is that two strict checks were swapped for the loose normaliser.
- Fix: keep `awaits` as specified. Give the strict sites the type half back, the way ts5 and test_story_run_refusals.py:3425
  already do: `_Awaits.__eq__` -> `type(other).__name__ == "OpenWork" and story_run_common.awaits(other) == "stage_awaits_acceptance"`;
  E9 -> `(type(x).__name__, awaits(x))` against `("OpenWork", "stage_awaits_acceptance")`. Witness: the three files' tallies,
  plus a one-line probe showing the bare word no longer equals `AWAITS`.

### F2 (fix before merge) — "the ONE writer" is false: a kept inline clone of the record writer remains

Surface: test writers of the `acceptance` record in pipeline.json (class of the finding, item 1).

- `story_run_common.accept_record`'s docstring says it is "The ONE writer of the record in the tests". But the KEPT file
  `scripts/tests/test_s7_investigation_replay.py:227-233` (not in `quarantine`, checked against test-layers.json) builds
  the same dict by hand: `{"stage": "S7", "role": "qa-failure-analyst", "acceptor": "qa-doc-scribe", "reviewed_dispatch": author,
  "verdict": "accept", "failure_class": None, "quote": "", "witness_paths": [], "at": "t"}`. It is byte-for-byte what
  `accept_record(task_root, "S7", author)` writes (stages.json:240-243: S7 roles[0] = qa-failure-analyst, acceptance_by =
  qa-doc-scribe). The next change to the record form will miss it, which is exactly the finding's class.
- Quarantined copies (test_consumer_close_route.py:65 `accept_record(kind, reviewed)`, test_stage_acceptance_consumer.py:617)
  are out of scope on purpose, but the docstring claim does not say "kept".
- `awaits`' docstring says "The ONE reading of the attribute in the kept tests". Strict direct `.unresolved` reads stay in
  kept files (test_story_run_refusals.py:3425, test_s7_investigation_driver.py:370, test_story_run_s3_windows.py:160,276). They
  are legitimate (they carry the type half), but the sentence is wrong. It should say "the one normaliser".
- Fix: route test_s7_investigation_replay.py:227-233 through `story_run_common.accept_record` (its `accepted_for` guard
  stays). Narrow both docstrings to what is true: kept tests, normaliser. Optional, same round: test_story_run_deferred.py:52-53
  goes through `test_controller_state` just to reach the wrapper and could call `accept_record` directly.

### F3 (fix before merge) — the comment above the later K3 rigs describes a world that is not the one they run in

Surface: the consumer-gate world of the S6 test fixtures (`ACCEPTED_S6` / `RUNNING_S6` without `role`).

- The new comment (test_story_run_s6.py, before "once per life") says the later rigs run "with the consumer switched off ON
  PURPOSE". They do not. `acceptance.consumer_of("S6")` still answers `qa-failure-analyst` in them, and `consumer_awaits` still
  wraps `complete` (driver_stage_s6.py:163-165). What is off is the AUTHOR: the role-less dispatches make
  `stage_author_dispatch` return `""` (acceptance.py:1400-1410). `consumer_pending` and the close site then read
  "the author never ran" (acceptance.py:1481-1482), a state the controller never produces next to an accepted runner dispatch.
- The same scenario now models "no consumer" two ways: item 3 patches `acceptance.consumer_of` (the honest no-consumer
  table, "older pipelines"), while the later rigs rely on an impossible fixture. Two roads for one condition inside one
  scenario (critic-diff-brief item 12 asked in the small; the product road is single).
- Whether the later rigs hide a PRODUCT defect: no. The builder's round-1 reds show that with the record standing and no mark,
  S6 closes at `s6.accepted` (driver_stage_s6.py:418-424), which is the X7-6 rule. So option (a) (the Lead's decision) is
  sound as a scope choice. Its comment, though, is false (critic-diff-brief item 7: an annotation that lies).
- Fix (one of): (a) wrap the later rigs in the same `mock.patch("acceptance.consumer_of", lambda stage, table=None: "")` as
  item 3, so "consumer off" is real, and re-run the scenario (the expectations should hold, but that is unverified); or
  (b) at minimum, rewrite the comment to say what is true ("no author is named: role-less dispatches, a state the
  controller does not produce; the consumer gate is not reached") AND open a finding/node for the class: every
  `ACCEPTED_S6`/`RUNNING_S6` rig in test_story_run_s6.py (the B-K1 loop included, builder's "Analogs noticed") runs with the
  author unnamed. The builder reported the analog; the coordinator owns where it goes (rule 9, CLAUDE.md).

### F4 (fix before merge) — the same note still prints the ceiling, a budget figure, under plain "B"

Surface: unit labels of measured sizes in brief_pack's conductor note (FR-37/FR-41 sense; AR-16 is not touched: this is a
stdout note, not a question).

- brief_pack.py:4532-4533 now print, in ONE line, `", 4,174 budget B against the ceiling, over the 6144 B ceiling after every
  cut: ..."`. `BRIEF_MAX_BYTES` is compared against `budget_of(text)` (brief_pack.py:4442, 4452-4453), so the ceiling is a
  budget-byte figure. The second clause names it in the unit the diff just retired from the first.
- Fix: `over the {BRIEF_MAX_BYTES} budget B ceiling` at :4533. (:4462, `over its {BRIEF_MAX_BYTES} B budget`, in the role's
  brief, already names the number as the budget: n/a. If it is aligned anyway, the kept pin test_brief_pack.py:2435 moves in
  the same commit.)
- Product readers of the old strings: none. Grepped `head over cap|against the ceiling|budget B`, case-insensitive, over the
  whole worktree except *.jsonl. Hits: brief_pack.py itself, detector_verdict.py:445 (an unrelated docstring), docs and
  reviews, and the quarantined readers the builder listed (test_brief_pack_sd_head.py:204,206;
  test_story_run_s6_w1_frozen.py:158,163,260-262 with fixtures/s6-w1-frozen/console.json; test_story_step_materialize.py:247).
  Positive control: the same call found brief_pack.py:3652 and :4532 (the new text). The driver golden that SIBLING_MAP
  line 166 names (`experiments/driver-golden/`) does not exist in this clone or in the main repo (`ls experiments` -> only
  `measurers`; `git ls-files experiments | grep golden` empty), so no normalisation row is owed here.
- The three quarantined pins will go red in quarantine-watch. The Lead marks them, as the dispatch says.

### F5 (for the commit, Lead) — no AR-n is named

The report's FR pass names no AR-n (critic-diff-brief item 10; CLAUDE.md rule 10). Touched: AR-22 (the brief note is a
produced text; its readers were walked both ways and only quarantined tests read it) and AR-15 (the record writer
converged at one helper in the tests; F2 is its remainder). The package commit's `architecture:` line names them.

## Answers to Q1-Q5

- **Q1.** Behaviour is preserved for the callers of `record_stage_acceptance`: the wrapper keeps the name, the signature and
  the parameter name `reviewed_dispatch` (test_story_run_freshness_k6_k7.py:76 passes it BY KEYWORD, so keeping the name
  matters). It passes positionally to `accept_record(root, stage, dispatch="")`, whose body and dict are identical to the
  removed one. `json` is a module import of story_run_common; `contract` is imported in the function, as before. No cycle:
  story_run_common does not import test_controller_state. Witness consistency: test_controller_state 326/326 exercises the
  wrapper. Normaliser key: `getattr\(.*unresolved` (case-insensitive) over scripts/ finds 1 kept line (story_run_common.py:314)
  plus quarantined test_repair_route.py:559, test_stage_critic_route.py:158,303 and test_stage_acceptance_consumer.py:164,222,654.
  Its positive control is the same call finding those six (and story_step.py:2262,2377 outside tests). So the key holds. The
  remaining clone the builder missed is the record WRITER in test_s7_investigation_replay.py (F2). The loosening is F1.
- **Q2.** The new key's expectation comes from the requirement, not the code's answer. X7-6 POSITION at driver_stage_s6.py:418-421
  says a mark falls through to the flow whose close sites find the record; :493-494 says the proofs run in `s6_reentry` after
  the record. So "refused, nothing proved, nothing closed" is the stated rule. The refusal prefix pins the door's wording,
  which must name the missing record and its dispatch (FR-1); it was observed from the run, which is legitimate for a door
  pin, not an oracle on behaviour. `s6.reprobed` after the record is the faithful reading: the mark is set (`mark="S6-qa-runner-1"`),
  so :418 is skipped, `auto_done` leads to `s6_reentry` (:507-508), and the close is the re-probed one. `s6.accepted` would be wrong
  here, because it fires only with no mark. Discrimination is proven by the builder's probe (i): the record line replaced by
  `pass` made the post-record entry raise; sha256 restored equal (74AE69BD...14EF). The later rigs: F3.
- **Q3.** The key reaches the :496 else branch. `acceptance.consumer_of` is read by attribute at call time in stage_S6 (:496),
  `consumer_pending` (:172) and `consumer_awaits` (:163). The only `from acceptance import consumer_of` (controller.py:5514) is
  function-local, so it is patched too, and the controller is stubbed in `reprobe_rig` anyway. With the patch, the
  consumer branch would yield an `OpenWork` (never `False`/`True`), so `[[False], [True]]` separates the branches. The builder's
  mutation `not owed` -> `owed` flipped it to `[[True], [False]]`, with driver_stage_s6.py sha256 equal after restore
  (4BF7EFE1...F841). No leak: `mock.patch` is a context manager per iteration, restored on exit or exception, and it is the
  scenario's last block before `finally`. (The lambda blanks every stage, not only S6; harmless in this rig.)
- **Q4.** F4: a third figure, the ceiling, still prints under plain "B" in the same line. No product reader (grep and control
  in F4).
- **Q5.** Carriers outside the diff: `record_stage_acceptance` stays as a name, so its ~25 importers (story_step_common.py:175,
  controller_rework_common.py:78,152, test_gate_vocabulary.py:24, test_s6_lane_admission.py:328,346,
  test_person_word_stages.py:116, ...) need nothing. design/: no mention of story_run_common or record_stage_acceptance (grep,
  case-insensitive; positive control: the same call over design/ counts `story_run.py|harness` in 5 files). SIBLING_MAP names
  story_run_common only for `run_scenarios` (line 166), which is untouched. docs/ hits are historical specs and reports. The
  test-layers.json covers are unaffected: no file was added and story_run_common.py was already a shared module.

## Standing questions

- **DUPLICATION AND CONSISTENCY:** one remaining clone, F2 (test_s7_investigation_replay.py:227-233). Grepped
  `reviewed_dispatch` (case-insensitive) over scripts/tests: 17 files, each checked against the quarantine section, and the
  only kept inline writer is the one named. Also grepped `getattr\(.*unresolved` and `\.unresolved\b|hasattr\(...unresolved`
  over tests. The label inconsistency is F4.
- **CODE QUALITY:** two annotations do not tell the truth: the docstrings of F2 and the comment of F3. The new code
  adds no function over 60 lines (it extends `hf2_11b_...`, which was already long, by ~35 lines in two flat blocks). No dead
  branch; the function-local `import story_run` and `from unittest import mock` follow the file's existing habit.
- **IN-TREE RATCHETS (item 9):** no raise. The report shows lint 36/36 and dup 9/9 + 16/16. I checked that this is consistent
  with the diff (no new module and no copied block over the dup threshold) but did not re-run it.
- **ARCHITECTURE (item 10):** F5.
- **JUDGMENT (item 11):** none. No check classifies a role's judgment, and no census row or scan constant is touched.
- **ONE ROAD (item 12):** the product road is unchanged and single. Inside the test scenario, "no consumer" is modelled two
  ways (F3), and that is fixed this round.
- **Hygiene (item 8):** English only (`selftest --lang` 4/4 in the report). No control bytes are added.

## Class completeness (SIBLING_MAP)

Class: a stage-closing record or word written or read by a test in its own way. Artifact sweep:
- story_run_common: both helpers present.
- test_controller_state: wrapper.
- test_story_run_s6: `record_failure_analyst_accept` and `_Awaits` applied; `_Awaits` loosened, F1.
- test_s7_rejudge: applied.
- test_story_run_s7: applied twice; E9 loosened, F1.
- test_story_run_deferred: uses the wrapper (optional cleanup, F2).
- test_story_run_freshness_k6_k7: uses the wrapper by keyword; kept.
- test_s7_investigation_replay: NOT applied, F2.
- Quarantined files: n/a by edge.
Map walk: the axes of AR-15/AR-14 (one writer) and of driver twins (the golden at line 166) are n/a here, because no product
code changed except the two labels and the golden is absent. The role-less fixture class is queued under F3 (b), unless F3 (a)
is taken.

## Trail

Read: the full diff (`git -C <worktree> diff`); the builder report; the finding; driver_stage_s6.py:158-182, 395-513;
acceptance.py:1397-1410, 1472-1486; driver_dispatch.py:755-809; brief_pack.py:3585-3596, 4440-4469 and the :3652/:4532 sites;
test_story_run_s6.py reprobe_rig/row/stale_probe/ACCEPTED_S6 (2075-2135); test_story_run_deferred.py:40-110;
test_s7_investigation_replay.py:218-239; stages.json acceptance_by rows; test-layers.json `quarantine` membership of 19 named
files; critic-diff-brief.md items 6-12; critic_verdict.schema.json.
Reruns: test_s7_rejudge.py in the worktree -> `=== test_s7_rejudge: 161/161 ok ===` (matches the report). AWAITS probe in
the worktree -> new form `True`, old form `False` on a bare word.
Not re-run (by the non-goals): test_story_run_s6.py (566/566 in the report, slow) and the mutation probes. Their hashes
and red lines agree with the diff and the driver lines they target.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "F1: restore the type half at the strict sites: _Awaits.__eq__ in test_story_run_s6.py -> type(other).__name__ == 'OpenWork' and story_run_common.awaits(other) == 'stage_awaits_acceptance'; test_story_run_s7.py E9 (:966) -> (type(x).__name__, awaits(x)) vs ('OpenWork', 'stage_awaits_acceptance'). Today a bare word passes where driver_dispatch.finish would drop it (probe: AWAITS == bare word -> True, old form False).",
    "F2: route the kept inline record writer test_s7_investigation_replay.py:227-233 through story_run_common.accept_record(task_root, 'S7', author); narrow the docstrings of accept_record ('the one writer in the kept tests') and awaits ('the one normaliser', not 'the one reading of the attribute').",
    "F3: the comment above the later K3 rigs says 'consumer switched off' but consumer_of still answers qa-failure-analyst; only the author is unnamed (role-less dispatch, a state the controller never produces). Either wrap those rigs in the same consumer_of patch as item 3 and re-run the scenario, or correct the comment and open a finding/node for the role-less ACCEPTED_S6/RUNNING_S6 fixture class in test_story_run_s6.py.",
    "F4: brief_pack.py:4533 prints the ceiling (a budget-byte figure) as 'over the N B ceiling' right after 'budget B against the ceiling' in the same line; make it 'N budget B ceiling'.",
    "F5 (Lead, at commit): the architecture line names AR-22 (the brief note's readers walked: only quarantined tests) and AR-15 (the record writer converged; F2 is its remainder)."
  ],
  "class_completeness": "Class: tests writing the stage acceptance record or reading the awaiting word their own way. Kept files swept: story_run_common, test_controller_state, test_story_run_s6, test_s7_rejudge, test_story_run_s7 applied; test_story_run_deferred and test_story_run_freshness_k6_k7 use the kept wrapper; test_s7_investigation_replay:227-233 NOT applied (F2). Strict sites loosened by the move: F1. Quarantined copies n/a by edge. Role-less S6 fixture class: F3 (fix or queue). Golden normalisation axis (SIBLING_MAP line 166): n/a, the golden is absent from the clone.",
  "trail": {
    "read": [
      "git -C .claude/worktrees/agent-a8a5c4097e72f3c66 diff (7 files)",
      "docs/tasks/specs/reports/t-092-pc2-3.md",
      "plans/piles/package-ci/findings/20261105-hvosty-kritika-gm3-2-obshchie-helpery-priemki-s6-i-podpisi-byudzheta.md",
      "ai-packages/qa-factory/scripts/driver_stage_s6.py:158-182,395-513",
      "ai-packages/qa-factory/scripts/acceptance.py:1397-1410,1472-1486",
      "ai-packages/qa-factory/scripts/driver_dispatch.py:755-809",
      "ai-packages/qa-factory/scripts/brief_pack.py:3585-3596,3652,4440-4469,4532-4533",
      "ai-packages/qa-factory/scripts/tests/test_story_run_s6.py:2075-2135 and the diff hunks",
      "ai-packages/qa-factory/scripts/tests/test_story_run_deferred.py:40-110",
      "ai-packages/qa-factory/scripts/tests/test_s7_investigation_replay.py:218-239",
      "ai-packages/qa-factory/references/stages.json acceptance_by rows",
      "ai-packages/qa-factory/scripts/tests/test-layers.json quarantine membership",
      "docs/SIBLING_MAP.md line 166",
      "docs/tasks/critic-diff-brief.md items 6-12",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "python -B <worktree>/ai-packages/qa-factory/scripts/tests/test_s7_rejudge.py", "result": "=== test_s7_rejudge: 161/161 ok === (matches the report)"},
      {"command": "python -B -c (import test_story_run_s6; AWAITS == bare word; old getattr form on bare word), in the worktree tests dir", "result": "new AWAITS == bare word: True; old form on bare word: False"}
    ]
  }
}
```
