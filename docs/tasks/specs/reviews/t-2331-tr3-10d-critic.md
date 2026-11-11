TR3-10 Part D review (t-2331): the verdict is **fit with notes** (fit_with_fixes in the JSON): no blockers and 8 notes. N1 and N2 should be fixed before the merge; N3–N8 can be fixed or queued. Accepting the part is your call.

The report file was not written. The handoff hook only lets this worker write `t-2272-tr3-10c-critic.md`, so it refused `t-2331-tr3-10d-critic.md`. The full verdict is below so `tools/handback_extract.py` can pull it out. `t-2272-tr3-10c-critic.md` is unchanged and still ends with the Part C re-review block (fit).

Summary, one line per note:
- **N1:** the census raise 132→134 comes from two `raise ValueError` lines that their own functions catch, not from refusals. Use an early exit instead, drop the 2 rows, and set the ceiling back to 132.
- **N2:** the road back for the tied cases after `added` is not proven. Add a junction test, or reword the promise in the question.
- **N3:** a crash between registering the dispatch and `walk_before` leaves the walk's records held for the rest of the story, with no exit.
- **N4:** `walk_ask_once` opens the registry row before the role check that can refuse. Harmless, but the check should come first.
- **N5:** the stand is read in three places (two inline copies), and private helpers are used from other modules.
- **N6:** my Part C note R3 is still open (the two kind-folding functions).
- **N7:** when an assigned lane's walk fails to open, the old road signs in with the case's own account. It is safe only because the recorder takes the stand exclusively; say so in a comment or state-exits.
- **N8:** `walk_assign_step` is about 135 lines; queue a split.
- **Points 7 and 9:** moving `walk_refuse_gaps` to the stages layer is legal. Of my Part C notes, R1, R2 and R4 are closed by D; R3 is open (N6).
- **Control rerun:** `test_walk_account.py` gave 188/188, matching the witness.

---

# t-2331 critic: TR3-10 Part D (branch tr/tr3-10d, everything after d140e4c9b)

**Verdict: fit with notes (= fit_with_fixes): 0 blockers, 8 notes. N1-N3 should be fixed before the merge; N4-N8 can be fixed or queued.** Accepting the diff is the Lead's call.

Reviewed against: spec t-2174 Part D, §10 and §11 (L1-L7), and the standing brief. Line numbers are those of `story_run.py` at the HEAD of wt-tr3-10d unless a diff line is named.

## Notes

- **N1 The census raise comes from control-flow raises, not from refusals (fix).** `walk_assign_step` has `raise ValueError("the controller record holds no dispatches")` and `walk_assign_clear` has `raise ValueError("no dispatches")`. Both are caught by the function's OWN `except Exception` a few lines below and never reach a role. The scanner counts a literal `raise ValueError` as a refusal site (u3), so two `shape` rows appeared and `blocking_per_role.qa-runner` went 132 -> 134. Fix: replace both raises with an early exit (`if not isinstance(dispatches, dict): <note>; skip`), delete the two census rows, and set the ceiling back to 132 (AR-20: the raise is avoidable). This answers point 1: the two functions should not be blocking units at all.

- **N2 The `added` road back for the tied cases is not proven (fix: a junction test, or change the promise).** `walk_refuse_gaps` closes the tied cases `left_unchecked` and overwrites their request.json with `{"refused": ...}`. The question then promises the person "these checks rejoin the plan" (`walk_account_text`, option `added`). Re-joining would work through `manual_plan`, which prepares every case no ACCEPTED dispatch carried (`manual_done`), so a case refused by the gap is prepared again at the next S6 entry. But that only happens if an S6 entry comes after the conductor records the key.
  The one test, `walk_account_added_records_and_probes` (test_walk_account.py:355-375), stops at the conductor's `stand-account`. Its "rejoin" check only asserts that the answer itself refused nothing (`len(rig.refused) == 2`). I could not establish that S6 re-enters after a deferred `walk_account` answer instead of closing over the refused cases. If it does not, the option text promises what is not done (P22, FR-9).
  Fix: one junction test (answer `added` -> the conductor records the key -> next S6 entry -> the tied case is prepared and dispatched). If the road isn't real, reword the option to "the next run checks them".

- **N3 A crash between dispatch registration and `walk_before` leaves held rows with no exit (fix or queue).** `run_manual_lane` registers the controller dispatch (`controller.apply("dispatch", ...)`) and only then calls `walk_before`. If the driver dies between the two, the reserved id is "taken". `walk_assign_clear` skips taken ids, so that walk's `in_use` rows (no record) stay HELD for the rest of the story. This is the over-refusal side: the record is never handed to two walks, but it has no exit (AR-25, FR-40). The builder lists it as a residual.
  Fix: in `walk_assign_clear`, settle `dirty` an id whose dispatch is no longer running and whose walk has no record (`settle_unopened` already leaves walks with a record alone). Otherwise queue it with an executor line.

- **N4 `walk_ask_once` adds the registry row before `build` can refuse (queue, low).** `walk_account_person` refuses a role with a space or a non-ASCII character AFTER `project_decisions.py add` has opened the row. The result is an open registry row with no question, and the same note in every story (the next `add` reuses the row and `build` refuses again). Harmless otherwise: the row can still be resolved by the conductor's `stand-account`, and the tied cases are already closed. Fix: run the role check before the `add`. The rows of roles that `walk_account_raise` drops "unasked" stay open the same way and are reused at the next need; that part is fine. Answers point 3: harmless, not a state without an exit, but cheap to tidy.

- **N5 Duplication (fix or queue).**
  - The "first stand of the config" idiom is written inline in `walk_gap_role` and in `_answer_walk_supply`. `walk_pool._stand_of` already does this, and `project_decisions._stand_of` is a third reader.
  - Private helpers are used across modules: `project_decisions._stand_of` / `_ptr` (`walk_account_raise`, :3718/:3732), `walk_pool._stand_of` / `_needs` (`walk_assign_step`), `walk_pool._by_role` (`gate_preflight`), `guard_secrets._patterns` (the secret mask in `run_manual_lane`). Make them public or give each module one public entry.
  - `walk_gap_role` repeats `walk_pool._part_handle`'s test "a role whose note names two keys".
  - Settled (point 8): the two resolve bodies are now one (`_resolve_decision_row`). The secret mask has one inline site (`grep -c secret_pattern_hit` = 1). `"missing": True` has one site at HEAD (:3835).

- **N6 My Part C note R3 is still open.** `walk_pool._kind_key` and `fold_kind` still differ on inner double spaces. It needs a queue line with an executor (the pool keys in `config_contract`).

- **N7 A failed open of an assigned lane falls back to the old road.** That road signs in with the case's own account key, not the assigned handle. It is safe today only because the recorder takes the stand lease `exclusive` (`manual_capture._hold_stand`, mode default) and so never runs beside a walk. Name this in a comment or state-exits, so that a later shared lease for the recorder doesn't silently put two lanes in one account.

- **N8 Code quality (queue).**
  - `walk_assign_step` (diff :664-800, about 135 lines): well over 60. It is three steps (pools and lanes, entities and reservations, alone lanes) and should be split.
  - `_answer_walk_account` (about 57 lines) and `walk_account_raise` (nested loops with mutation of the state inside the raise loop): acceptable.
  - `walk_gap_role` catches `Exception` around the whole body. That is P1, but it would also hide a typo.

## The Lead's points

1. **Census:** see N1. The raise is not right; these are not refusals.
2. **The three question texts:** they follow human-questions.md: no key path, no file of ours (the environment file is the person's own and is named because the question asks them to edit it), one question, priced options, nothing recommended. The executors match the WHOLE normalised answer against the closed token set (`s0_normalize(words) == token`), so no phrase list (FR-12). `added: <keys>` is not a bare token, so it goes whole to the conductor. No `offered` (L5). The `take_answer` branches sit before the generic `offered` branch (diff :970-982).
3. **`walk_ask_once` row before the Person:** see N4.
4. **The `added` road back:** see N2. It is real only if an S6 entry follows the recording, and that is unproven; for now it is a promise.
5. **Walkers 1:** the no_pair raise runs at walkers 1, and the fast test `no_pair_question_applies_at_walkers_one` pins it. The frozen file is not re-pinned, against L6. The builder's reason holds: my grep for `no_pair|walk_refuse_gaps|credentials_by_role|stand_account` over `test_story_run_s6_w1_frozen.py` is empty, while the same grep over `test_walk_account.py` matched (control). The frozen story is guest-only, so it never reaches the site.
   Is "none of items 1-13 runs at walkers 1" true by the code? False for item 13 (the report says so itself). For items 1-12 it holds:
   - `walk_assign_clear` reads nothing when the state has no key.
   - `walk_before` without `assigned` is today's code.
   - The dispatch id is `len(prior)+1` unless that id is taken.
   - `deferrable`'s first line passes only `no_hold` walk_supply/data_change Persons.
   - `s6_lane_holds` without handles is today's.
   A raised deferrable Person is deferred by the top-level handler (:18355-18368), so the last `walk_account` question being "raised" doesn't stop S6.
6. **Claims and ids:**
   - L1: the id `assign_entities` writes is the id `run_manual_lane` opens under (`walk_lane_facts["id"]`, when no dispatch has it yet).
   - L4: a stale reservation is settled `free` in `walk_assign_clear`; a failed open is settled `dirty` right after the record unlink in `walk_before` (diff :45). `settle_unopened` skips walks that have a record.
   - Never handed to two walks: account holds are per handle per entry (`+`-joined actor plus per-handle holds), and a record row is held until settled.
   - Held forever: yes, in the crash case only (N3).
7. **`walk_refuse_gaps` moved dispatch -> stages:** legal. Its only caller is `manual_lane_plan` (stages); grep shows one call (:14026). It now calls `walk_account_raise` (stages), so it can't stay in dispatch without an upward edge. Moving it up to the caller's layer removes that edge instead of hiding it; its own calls (`refuse_case`, `owe_row`) point downward.
8. **The duplicates the builders named:** see N5.
9. **My Part C notes R1-R4:**
   - R1 closed: `walk_session.settle_unopened`, called at the unlink, plus the L4 free for stale reservations.
   - R2 closed: `assign_lanes` counts `active` lanes per ROLE across parts, and shared pool handles don't count.
   - R3 open: N6.
   - R4 closed: `held_walks`, and `free = [`.

## Standing questions (brief)

- **Fit to spec:** items 1-14 present. L1-L7 applied, except the L6 re-pin (point 5, justified). D.5: walkers 1 is unchanged except item 13.
- **The builders' own decisions:** obtain shown as a note on a stand that may not be changed. Alone lanes are judged from the data words. A stale id is settled free. All on the safe side, apart from N3.
- **Seams:** gate_preflight (D8) changes only `_actors_of_manual_cases` and `_probe_actor`; an extra account that fails is a note, never a question. `s6_settling_lanes` gets one clause (L2).
- **Class completeness:** N2, N3 and N6 are open. Stage twins (axis 5): the S7 walks take no assignment (n/a, as the spec says).
- **Tests:** the junction test for the `added` road is missing (N2), as is a crash-between test (N3). The rest pin their keys. My control rerun is below.
- **DUPLICATION:** N5. Grepped: `walk_refuse_gaps\(|_stand_of\(|_ptr\(`, `secret_pattern_hit`, `"missing": True`.
- **CODE QUALITY:** N8.
- **Hygiene:** selftest `--limits --lang --hygiene` 4/4 per the attached witness.
- **Ratchets:**
  - census `blocking_per_role.qa-runner` 132 -> 134: named, but avoidable (N1);
  - driver-layers rows added for every new member and state key, plus the `walk_refuse_gaps` re-home;
  - role-load: per the witness, 165/165.
- **ARCHITECTURE:**
  - AR-13: one assignment reader, `walk_lane_facts`.
  - AR-14: one claims writer; `settle_unopened` lives in walk_session.
  - AR-15: `lane_handles` / `walk_env_pair` are now the driver's only bodies; one resolve helper.
  - AR-25: N3.
  - AR-24: the words go whole to the conductor.
- **JUDGMENT (AR-29):** none moved. Code compares tokens and reads data. Free words go to the conductor. Whether a case can be checked stays with the person and the conductor.
- **KNOWN RED (outside this verdict):** `test_walk_charter` (the claim line of the lanes' prompt has no row), already being fixed by a separate worker.

## What still has to happen

N1 and N2 before the merge (a small fix round). N3 and N4 as a fix or as queue lines with an executor. N5, N6 and N8 as queue lines. N7 as a comment or a state-exits line.

## Trail

- Read:
  - spec t-2174 §11 (whole) and Part D item 13 (:680-700);
  - report t-2313 (frozen-file divergence, the `added` fix);
  - the story_run.py diff d140e4c9b..HEAD, whole (985 lines);
  - story_run.py manual_done, refuse_case, the top-level `except Person` handler (:18355-18368), manual_capture `_hold_stand` signature;
  - the walk_pool.py and walk_session.py diffs, the gate_preflight.py diff, the census and driver-layers diffs;
  - test_walk_account.py :355-375.
- Greps (with controls): frozen-file grep, empty (control: test_walk_account.py); `walk_refuse_gaps\(` (one call); `secret_pattern_hit` count 1; `"missing": True` one site.
- Control rerun (one): `python -B D:/ws1/wt-tr3-10d\ai-packages\qa-factory\scripts\tests\test_walk_account.py` gave `=== test_walk_account: 188/188 ok ===`, matching the witness.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "N1 walk_assign_step / walk_assign_clear: replace the locally caught raise ValueError control flow with an early exit, drop the two census rows, blocking_per_role.qa-runner back to 132",
    "N2 a junction test: walk_account answer added -> conductor stand-account -> next S6 entry prepares and walks the tied case; or reword the added option to 'the next run checks them'",
    "N3 walk_assign_clear: settle dirty a reserved id whose dispatch is no longer running and whose walk has no record (crash between dispatch registration and walk_before), or queue with an executor",
    "N4 walk_account_raise: check the role before project_decisions add (no open row for an unaskable role)",
    "N5 one stand reader (walk_pool._stand_of / project_decisions._stand_of / two inline copies); private helpers used across modules made public; walk_gap_role reuses the two-key role test",
    "N6 Part C R3 still open: queue line for pool keys by fold_kind in config_contract",
    "N7 name the old-road fallback of an assigned lane whose open failed (case key, safe only under the recorder's exclusive lease)",
    "N8 split walk_assign_step (about 135 lines) - queue"
  ],
  "class_completeness": "R1, R2, R4 of Part C closed by D; R3 open (N6). Held rows: exits for a stale reservation (free) and a failed open (dirty) exist; the crash between dispatch registration and walk_before has none (N3). The added road back (N2) is unproven. Axis 5: S7 walks take no assignment, n/a. Stand reader triplicated (N5).",
  "trail": {
    "read": [
      "wt-tr3-10d docs/tasks/specs/t-2174-tr3-10-accounts-and-data.md section 11, Part D item 13",
      "wt-tr3-10d docs/tasks/specs/reports/t-2313 report",
      "git diff d140e4c9b HEAD story_run.py (whole), walk_pool.py, walk_session.py, gate_preflight.py, judgment-census.json, driver-layers.json",
      "story_run.py manual_done, refuse_case, top-level Person handler 18355-18368",
      "manual_capture.py _hold_stand signature",
      "test_walk_account.py 355-375"
    ],
    "reruns": [
      {
        "command": "python -B D:/ws/wt-tr3-10d\\ai-packages\\qa-factory\\scripts\\tests\\test_walk_account.py",
        "result": "=== test_walk_account: 188/188 ok ==="
      }
    ]
  }
}
```
