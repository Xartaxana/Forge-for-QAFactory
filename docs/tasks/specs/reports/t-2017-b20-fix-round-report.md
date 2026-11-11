# t-2017 B-20 fix round (critic verdict t-2015)

Commit bb94423e3 on bfix (wt-fb6), no push. All paths under `D:/ws2/wt-fb6/ai-packages/qa-factory/scripts/`.

## Per finding
- F1 DONE (decision: spec F2 (b)). `consumer_person_pass` computes `since` through the new one reader `Driver.accepted_at(author)` (last `accept` event, `controller.stamp_utc`); no `answer` -> a waiver is honoured only when later; unreadable acceptance time or word time = not honoured. `answer=` stays exempt. `consumer_word_step` is a plain loop again; the `since` parameter of `consumer_person_pass` is gone. Sites covered: `consumer_need_record` (S6, S7), `consumer_settled`, `s7_await_scribe`, the three S6 sites. Red: `test_f1_*` (consumer_close_route).
- F2 DONE. `person_pass` (the one body every site goes through): `self.dry` -> prints "dry run - a word would pass ...", returns `{}`, writes nothing. Red: `test_f2_dry_run_records_nothing`. (Guard sits in `person_pass`, not in `consumer_word_step`, so it covers every site and `stage_review_exhausted`.)
- F3 DONE (decision: no id in person text). `stuck_facts(..., place=None, ids=True)`: `ids=False` gives the person's lines (stage by `stage_place`, role by `role_words`, no dispatch id, no reason); `ids=True` is the factory's lines. New `stuck_facts_for(stage) -> (person, factory)`. The stuck lead gets the person lines; `text` (conductor + details file) = signature + the factory lines. `human_broken` rows: lead is `[]`, raw line is `['dispatch_id']`. Red: `test_f3_*`, loop rows N5.5/F3 (test_stuck_facts).
- F4 DONE. `import json` removed (test_consumer_close_route), `import harness` removed (test_stuck_facts). Lint ratchet: neither file is in the new findings.
- F5 DONE. `consumer_person_pass` catches the Refusal of `person_pass`, sets `retry` to the whole pass, re-raises. Red: `test_f5_*`.
- F6 DONE. `run()` start: `stuck_pending` is popped when `asked` is empty. Red: `test_f6_*` (test_stuck_facts).
- F7 DONE. `test_f7_the_refusal_sentence_is_pinned_to_its_source` (test_code_close_behind): `controller.code_close_conflicts` still yields the sentence, and story_run.py still contains it. No red possible (pin on unchanged code); the pin goes red on a rewording.
- F8 DONE. Comment moved above `CODE_CLOSE_IDLE_CAP`; N5 variable renamed `told`; constant `BY_PERSON` (writer `person_pass`, reader `consumer_close_words`).
- `refused_text` analog DONE: appends the person lines for the stage (none when no stage). Test: `test_f3_the_cap_lead_names_the_earlier_stages_without_ids`.
- U3a die at test_stage_acceptance_consumer.py:260 DONE. Cause: `s7_close` calls `s7_close_places` and `s7_gap_reason` (t-2005); the stub and the Rig gained them. A second die (`accepted_at` not bound on stubs) fixed by adding it to the two bound lists. Words in that file's two waivers: `"at": "t"` -> `LATER` (unreadable time is no longer honoured, F1).

## Deviations / outside owns
- `tests/fixtures/driver-layers.json`: 3 rows (`BY_PERSON`, `Driver.accepted_at`, `Driver.stuck_facts_for`), otherwise test_driver_layers fails L1.
- `tests/test_stage_review_person_pass.py`: stub gets `accepted_at`; `test_consumer_person_pass_unchanged` was already stale (expected no finding; the pass files one since N2) and pinned any-age: now old word -> False, later word -> True, one finding.
- Not run (slow, CI-only): test_story_run_s7_live, test_s7_investigation_replay (started once, killed). If they pin any-age waivers they will be red on CI: fix is the same (`at` later than the acceptance).
- Pre-existing, not mine: `test_judgment_census` 20/21, `blocking_per_role.conductor` 468 > 467. The same at HEAD (checked with HEAD story_run.py swapped in, byte copy restored, cmp identical). Lint ratchet `--check`: 4 new findings, all walker's (test_walk_brief:116, test_walk_lanes:24, test_walk_places:15, walk_session.py:58).
- Queue (verdict), not done: `stuck_asked` vs `already_answered` merge, S7/S8 thresholds, one helper for the three add-finding passes, `_next_action_for_state` pipeline required.

## Witness (verbatim closing lines)
```
pytest test_consumer_close_route.py -q        -> 17 passed in 97.75s
test_code_close_behind.py                     -> === test_code_close_behind: 52/52 ok ===
test_stuck_facts.py                           -> === test_stuck_facts: 40/40 ok ===
test_stage_acceptance_consumer.py             -> === test_stage_acceptance_consumer: 129/129 ok ===
test_driver_layers.py (after the 3 rows)      -> === test_driver_layers: 52/52 ok ===
test_judgment_census.py                       -> === judgment_census: 20/21 ok ===  (FAIL c3 conductor 468>467, same at HEAD)
pytest test_stage_review_person_pass.py -q    -> 29 passed in 14.24s
lint_ratchet.py --check                       -> 33 findings, 29 in baseline, 4 new (all walker's; none in my two files)
```
Red run (HEAD story_run.py swapped in, restored byte-identical, sha256 f0eb0a6fb414a31836640decde63ef36bc6c5db837f10996a195b10283bbbcab): `pytest -k "f1 or f2 or f5"` -> `5 failed, 12 deselected in 29.95s`; test_stuck_facts -> FAIL "F3 refused_text carries the facts".

Needed beyond the manifest: `driver-layers.json`, `test_stage_review_person_pass.py`, `controller.py` (code_close_conflicts), `no_move.py` use of `text`.
