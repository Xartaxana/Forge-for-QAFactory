# t-1292 - code review of U7 node 1b (universality/1/U1-2), branch `worktree-u7-1b` at 5f9b025c

**Verdict: NEEDS WORK.** One finding blocks the merge (F1, with `failure_class: spec`, because the spec's M5 premise does not hold). Two findings should be fixed before merge (F2, F3). Three are low (F4-F6).
The decision to accept is the Lead's (rule 6).

What I reviewed: `git -C .claude/worktrees/u7-1b diff origin/main...HEAD`, 7 files, +54/-30. Spec: r3 section 2 "a2D1 + s6.unknownword" (lines 228-250) and section 6 stream 1 (lines 617-643). Reason for the node: t-1271 findings F1-1 and F1-4.

## Answers per key

**K1 (are the words true, F1-1): NO. The road stops at `manual_evidence.py unprepared`, and the new line about it is untrue. See F1.**
I traced one row of a `cli` or `desktop` profile:
- `_manual_agent_pass` (planning_contract.py:2339-2344, 2424-2431) converts it to `manual-agent` and adds the line "... What the agent cannot do is recorded `unprepared`, with what it tried."
- At S6, `Driver.manual_plan` (driver_stage_s6.py:964-985) calls `manual_evidence.prepare_for_block`, which calls `prepare_to_file` and then `prepare_request` (manual_evidence.py:969-1065). Nothing in `prepare_request` reads the surface or the profile:
  - Grep `execution_profile|row_for_profile|hands` with `-i` over manual_evidence.py: 0 hits.
  - Positive control with the same shape (`walkable|POLICIES`): 20 hits.
  - So the case is **prepared normally**. Its `request.json` holds a normal request with no `unprepared` marker, and it does not appear in `plan["unprepared"]`.
- The runner's block lines are therefore the generic ones (driver_stage_s6.py:1954-1957: "execute the approved manual-agent cases ... record each observation as manual evidence"). The `unprepared` door text (1958-1963) is given only to cases in `plan["unprepared"]`.
- The runner has no capture surface for cli or desktop. `capture_surfaces` lists only `ui`, `http` and `app` (references/manual-capture-steps.json:46-50, read).
- `build` refuses an attempt with no captures (manual_evidence.py:1875-1877: "Capture first: `manual_capture.py ui ...`").
- **`manual_evidence.py unprepared` refuses this case outright.** `write_unprepared` (manual_evidence.py:1507-1512) checks `unprepared_request(...) is None` and raises: "`<case>` was prepared (its request.json holds no `unprepared`): close it with `manual_evidence.py build`".
- The first place where the road stops is that refusal at manual_evidence.py:1511. The first untrue text is the new line at planning_contract.py:2430-2431. The same claim is in the comment at 2337, the changelog fragment, the architecture.md axis 2 cell and the commit's AR-28 line.
- What actually happens: a runner is dispatched (a paid turn) and cannot write a record by either command. The case then ends with no record and closes `left_unchecked` / not checked (manual_close, driver_stage_s6.py:1060-1085). That direction is safe (no pass), but it is not the `unprepared` attempt with observations that S7 triages, which is what r3 M5 promised.

**K2 (the old road): same decisions and same lines for every doubt input.** By reading:
- Main's `if hands_of[profile]: ...; continue` fired only on a non-empty string. Every doubt input makes `_row_of_nobody` return "" on both sides, so `by_hand == ""` and the new `if by_hand:` at 2429 never fires.
- Per input:
  - A profile the config lacks: `profile_words` is empty, so `row_for_profile` returns None.
  - An unreadable config: `cfg` is None, so nothing is said.
  - A broken table: the same single line from `_row_of_nobody` 2294-2297.
  - Web: `row_for_profile` returns None before reading the table (surfaces.py:214-215).
  - Mixed hands: None (surfaces.py:208-210).
  - An empty obligation list: the profile branch is skipped on both sides, and the same "plan lists nothing" line follows.
- By run: I ran the branch's new test against origin/main's `planning_contract.py`. Its three old-road rows PASS there as well as on the branch, and the target row is red (trail R2).

**K3 (invariants): both hold.**
- An unknown word: `found.setdefault(word, {"hands": "role", ...})` (surfaces.py:138). `_who` gives "agent" only for `AGENT_HANDS`. `row_for_profile` returns None for a word no row fits, which is the old road with no line.
- No `passed` without evidence: a converted case reaches only `build`, and `build` keeps every gate (captures, phases, Then quotes, masked). With F1 in place it cannot reach `unprepared` at all.
- Caveat (part of F1): the commit and comment claim "never `passed`". That is stronger than the code. A desktop-only project has one profile, so `manual_capture ui` takes it (`capture_profile` step (4), manual_capture.py:442). A browser capture that meets the gates could then build a `pass`. That is allowed by the spec's own wording of the invariant ("without the evidence the manual gates accept"). The F1 fix makes the claim true, because an `unprepared` request never reaches `build`.

**K4 (readers): no reader is left behind.**
- Readers of `declared_surfaces`:
  - readiness.py:1321 publishes the record, and the doctor prints `words` verbatim (skills/qa-doctor/SKILL.md:111).
  - gate_preflight.py:832 tests truthiness only.
- Comparisons of `hands`: grep `get("hands")|hands ==` over scripts and hooks (prod) finds only table-row reads ("none", "driver", AGENT_HANDS), never the record's "person" or "role". Grep for a `"person"` literal near hands or surface: only the new explanatory comment at surfaces.py:91. Grep for an enum of hands values: none.
- `unsupported(` in prod: only `red_sandbox._unsupported` (an unrelated name). The control with the same shape over tests finds test_surfaces.py:291, 297, 303 and 308.
- forge `tools/`: 0 hits.

**K5 (texts): F1 makes three texts untrue (the 2430 line, the 2337 comment, the changelog and axis 2 cell); F4 lists stale docstrings.**
- skills/qa-doctor/SKILL.md carries no surface words of its own (it prints them). skills/qa-onboarding/phases/p2-interview.md:227 already says role-first, which agrees with the branch.
- I found no product text that says cli, desktop or an unknown word "goes to a person". Grep over md, json and py (`go(es)? to a person|Agent checks on a|not supported`) finds only generic vocabulary (`wait` = handed to a person) and quarantined test rows.
- The axis 2 cell is exactly r3 §6's sentence, and it is the only line changed (diff: one -/+ pair at architecture.md:48). Its truth depends on F1.

**K6 (tests): the target row kills; there are three low notes (F5).**
- Killing power, by run: on origin/main's planning_contract the row "a `hands: none` profile" FAILS (`expected ('manual-agent', True, False), got ('new', False, True)`). The readiness row is red on main by reading: main's `_who` gives "person".
- Duplicates: none. Existing `_manual_agent_pass` rows (test_question_branches.py:2386-2524, through `run_pass`) do not cover a profile.
- Volume (`git diff --numstat origin/main...HEAD`): product +27 (planning_contract 12, surfaces.py 11, surfaces.json 4) against tests +25. That is within the rule.

**K7 (merge and quarantine): clean merge; the list is complete.**
- `git merge-tree --write-tree origin/main HEAD` gives tree c52974d1, exit 0. origin/main (221548d2) is 3 commits past the base d9876b30, and none of them is in `ai-packages/`.
- Quarantine: test_surfaces.py is quarantined (test-layers.json:10385). I read lines 262-312 and 444-476. The contradicted assertions are 277, 279, 286, 291, 297, 302, 303, 308 and 445-476, which matches the builder's list. Line 288 (`no stand for an agent's hands is described` in words) still holds against the new no_stand words.
- One note for the list: 291 raises `AttributeError`, which aborts the rest of `declared()` (lines 293-312+), so those later rows stop running too.
- Other test files: the grep finds no other assertion of "person" hands, the old words or `unsupported(`. Hits in test_code_close_behind, test_question_lines_unread, test_s7_repair_review, test_story_run_s7, test_then_remainder and test_ticket_adapter are an unrelated `person` / `Person` kind. test_mobile_road.py: 0 hits.

## Findings

**F1 - BLOCKS THE MERGE (failure_class: spec). A converted `hands: none` case cannot be closed `unprepared`, so the node's role-first words are still untrue (F1-1 not settled).**
- Evidence: K1. Input: a manual-agent plan row whose profile has capability `desktop`.
  1. planning_contract.py:2408 sets `decision=manual-agent`, and 2430 prints "recorded `unprepared`".
  2. manual_evidence.py:1058 `prepare_request` writes a normal request.
  3. The runner gets no `unprepared` door (driver_stage_s6.py:1954-1964).
  4. `manual_evidence.py unprepared` refuses at manual_evidence.py:1511, and `build` refuses at 1877.
- Root cause: r3 §2 M5's premise ("The agent's attempt is therefore recorded with `manual_evidence.py unprepared`") is not checked against `write_unprepared`'s precondition. It needs an `unprepared` marker that only a `walkable` `Refused` writes (prepare_to_file 1188-1189).
- The fix is outside this node's owns, so the Lead decides:
  - (i) Widen the round to `manual_evidence.py::prepare_request`. After the story-owned checks (the POSITION INVARIANT at 1042-1044 is kept), a case whose plan row's profile resolves to a `hands: none` table row (`surfaces.row_for_profile`, the reader `_row_of_nobody` already uses; any doubt keeps the old road) raises `Refused(<the table's words>, walk_door, walkable=True)`.
    - `request.json` then carries `unprepared`.
    - S6 gives the runner the door at 1958-1963, `write_unprepared` accepts the case, and `build` is unreachable, so "never passed" becomes true by construction.
    - The fix covers both roads, because `story_step.py start` calls the same `prepare_for_block` (manual_evidence.py:1311-1312).
    - Add one row at the door (S6 prepare of such a case leads to an `unprepared` marker).
  - (ii) Hold the merge of 1b until (i) lands as its own node in the same wave.

**F2 - fix before merge. The untrue claims stay true only with F1; until then they are wrong at:**
- planning_contract.py:2430-2431 (the person-facing line);
- 2336-2337 (comment: "Its attempt ends `unprepared` (no capture surface), never `passed`");
- changelog.d/universality-1-role-tries-an-undriven-surface-first.md ("The attempt ends `unprepared` ... never `passed`");
- architecture.md:48 ("recorded `unprepared` with what it tried");
- the commit's AR-28 line.

With fix (i) of F1 they all become true and no edit is needed. With (ii) they are correct once both nodes merge. If F1 is not fixed, the line and the changelog must not claim `unprepared`.

**F3 - fix before merge (VARIETY, Q10).** On a CLI-only or desktop-only project, the branch is worse at S6 than main until F1 is fixed:
- Main left the obligation as planned, with an honest line.
- The branch dispatches a runner that has no way to record, and then closes the case `left_unchecked`. That costs a paid turn and gives the person nothing the analyst could triage.

There is no silent default and no false pass, but the stage gets no better. This resolves with F1.

**F4 - low (K5, stale docstrings).**
- planning_contract.py:2307-2308: the `_manual_agent_pass` docstring says "one [line] per row that changed". A converted `hands: none` row now gets two.
- planning_contract.py:2278: `_row_of_nobody`'s first line still cites "EP1-41f N-17" as its basis, but that rule is now reversed. Name a2D1 there.

**F5 - low (Q5).**
- (c) The new conversion row calls `PC._manual_agent_pass` directly and mocks `_manual_cases_by_row`. That is the shape of the quarantined test_surfaces row, not the `run_pass` door (`apply_gate_answers`) that the neighbouring rows at test_question_branches.py:2349-2356 use.
- (b) Its expected text appends code's own sentence " What the agent cannot do is recorded `unprepared`" (test_question_branches.py:3153). No spec value names that sentence, and it pins the untrue claim of F1.
- The readiness row (test_readiness.py:867-870) asserts `declared_surfaces`, not "the record's `surfaces` entries" that r3 names. That is acceptable as a data seam, so the note is low.

**F6 - low (mechanical layer, rule 21 / rule 7).** These were not attached to this dispatch, so I am returning them as a request and not running them myself:
- the builder's handoff with its DoD run tails (`architecture_index.py --check`, `scenario_walk.py --witness-for`);
- the branch's `forge-check` job result.

My two narrow reruns (R1, R3) are green.

## Standing questions

- **Q1 fit to the spec:** items 2, 3, 4 and the axis 2 cell are implemented as written. Item 4's intent (the case reaches the agent and ends `unprepared`) is not met (F1).
- **Q2 builder's own decisions:** the line is added only when the row changed (safe). The line is computed after the conversion (nothing is said for a row that converted nothing). OK.
- **Q3 seams:** the edits are additive and localized. No order changed in `_manual_agent_pass` (the profile read still precedes the empty-list check, same as main).
- **Q4 class completeness:** the sibling `story_step.py start` road shares `prepare_for_block`, so the F1 fix there covers both roads. `driver_stage_s6._cases_all_on_driver` reads `is_device_row` only, which is n/a (spec). Analog outside the owns: manual_evidence.py::prepare_request (F1).
- **Q6 DUPLICATION AND CONSISTENCY:** none found. I grepped `unsupported(`, `declared_surfaces` and `row_for_profile` (prod). The conversion reuses `_row_of_nobody` and `row_for_profile`, and no second reader is added.
- **Q7 CODE QUALITY:** none found in the new code. `_manual_agent_pass` is long (2301-2434), but that is pre-existing and the diff removes a nesting level. There is no dead branch: `unsupported` is deleted.
- **Q8 hygiene:** 0 Cyrillic in added lines (positive control: CLAUDE.md, 15 lines). 0 CR in the planning_contract diff.
- **Q9 ratchets:** none touched (no file of axis 18 in the diff).
- **Q10 architecture:** AR-1 and AR-28 are named and kept. AR-2's "role move" is named but not yet true (F1). VARIETY: F3.
- **Q11 judgment:** no census row, no `blocks_override`, no scan constant. The `judgment:` line names the move to role. OK.
- **Q12 ONE ROAD:** none found. The diff adds no branch on a language, runner or project name (read all +lines). Surface words stay data in surfaces.json.
- **Q5 tests:** K6 and F5. **Q13:** n/a (code gate).

## Spot-checks

- Builder claim "contradicted quarantined assertions 277...476": verified by reading, and the list is complete (K7).
- Claim "no production caller of `unsupported`": verified by grep, with the test-side control finding 4 hits.
- r3 M5 premise "recorded with `manual_evidence.py unprepared`": **does not reproduce** (write_unprepared 1507-1512). This is F1.

## Trail

- Read (tree `.claude/worktrees/u7-1b`, ai-packages/qa-factory/):
  - scripts/planning_contract.py:2270-2434
  - scripts/driver_stage_s6.py:930-1009, 1060-1085, 1340-1408, 1920-1966
  - scripts/manual_evidence.py:969-1098, 1230-1342, 1500-1629, 1850-1884
  - scripts/surfaces.py:30-45, 87-152, 204-216
  - scripts/manual_capture.py:436-461
  - scripts/readiness.py:1305-1336
  - scripts/gate_preflight.py:826-840
  - references/manual-capture-steps.json:40-56
  - skills/qa-doctor/SKILL.md (grep)
  - skills/qa-onboarding/phases/p2-interview.md:222-232
  - scripts/tests/test_surfaces.py:262-312, 436-482
  - scripts/tests/test_readiness.py:840-916
  - scripts/tests/test_question_branches.py:2188-2189, 2343-2356, 3149-3166
  - scripts/tests/test-layers.json:10385-10392, 8980-8986
  - spec r3:225-250, 612-643; review t-1271 F1-1, F1-4.
- R1: the new test function alone on the branch (`python -B <scratch>/run_one.py <scripts> <tests>`) gave PASS x4.
- R2: the same function against origin/main's planning_contract.py and references/surfaces.json, preloaded (`python -B <scratch>/run_main.py ...`):
  - `FAIL a hands: none profile ... got ('new', False, True)`
  - the three old-road rows PASS
- R3: `test_readiness.surfaces_said_aloud()` alone on the branch gave 14 PASS, including the cli, desktop, zzz and native role rows.
- R4: `git merge-tree --write-tree origin/main HEAD` gave c52974d1fb5a1e031fd442709fb92f52f4691cca, exit 0. `git diff --name-only <base> origin/main | grep ai-packages` gave empty output.
- Greps (case-insensitive where content-negative, each with a control of the same shape):
  - `unsupported(` (prod 1 unrelated hit, tests 4);
  - `execution_profile|row_for_profile|hands` in manual_evidence.py: 0 (control 20);
  - hands comparisons and the `"person"` literal (prod);
  - stale-phrase grep over md, json and py.

```json
{
  "verdict": "blocker",
  "blockers": [
    "F1 (failure_class spec): a converted hands:none case is prepared normally by manual_evidence.prepare_request (no surface read), so manual_evidence.py unprepared refuses it at manual_evidence.py:1511 and build refuses with no captures at 1877; the line at planning_contract.py:2430 'recorded unprepared' is untrue and F1-1 is not settled"
  ],
  "fixes": [
    "F1 (blocks): widen the round to manual_evidence.py::prepare_request - after the story-owned checks, a case whose plan-row profile resolves to a hands:none table row raises Refused(walkable=True) so request.json carries the unprepared marker (both roads via prepare_for_block); one row at the S6 prepare door; or hold 1b until that node merges in the same wave (Lead fork)",
    "F2 (fix before merge): planning_contract.py:2430-2431, 2336-2337, the changelog fragment, architecture.md:48 and the AR-28 commit line claim unprepared/never passed - true only with F1",
    "F3 (fix before merge, VARIETY): CLI/desktop projects get a paid runner turn that cannot record, then left_unchecked - resolves with F1",
    "F4 (low): planning_contract.py:2307-2308 docstring line count; 2278 cites the reversed EP1-41f N-17",
    "F5 (low): the new row calls _manual_agent_pass directly instead of the run_pass door; its expected text pins code's own unprepared sentence (test_question_branches.py:3153)",
    "F6 (low, request): builder DoD run tails and the forge-check job result were not attached"
  ],
  "class_completeness": "Sibling road story_step.py start shares manual_evidence.prepare_for_block, so the F1 fix in prepare_request covers both; analog outside owns named: manual_evidence.py::prepare_request. Readers of hands values and callers of unsupported: none left (grep with controls). Quarantined list test_surfaces.py 277,279,286,291,297,302,303,308,445-476 complete.",
  "trail": {
    "read": [
      "ai-packages/qa-factory/scripts/planning_contract.py:2270-2434",
      "ai-packages/qa-factory/scripts/driver_stage_s6.py:930-1009,1060-1085,1340-1408,1920-1966",
      "ai-packages/qa-factory/scripts/manual_evidence.py:969-1098,1230-1342,1500-1629,1850-1884",
      "ai-packages/qa-factory/scripts/surfaces.py:30-45,87-152,204-216",
      "ai-packages/qa-factory/scripts/manual_capture.py:436-461",
      "ai-packages/qa-factory/scripts/readiness.py:1305-1336",
      "ai-packages/qa-factory/scripts/gate_preflight.py:826-840",
      "ai-packages/qa-factory/references/manual-capture-steps.json:40-56",
      "ai-packages/qa-factory/scripts/tests/test_surfaces.py:262-312,436-482",
      "ai-packages/qa-factory/scripts/tests/test_readiness.py:840-916",
      "ai-packages/qa-factory/scripts/tests/test_question_branches.py:2188,2343-2356,3149-3166",
      "docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r3.md:225-250,612-643",
      "docs/tasks/specs/reviews/t-1271-u7-code-streams-1-5a-5b-7a.md F1-1,F1-4"
    ],
    "reruns": [
      {"command": "new test function alone on the branch (run_one.py)", "result": "PASS x4"},
      {"command": "new test function against origin/main planning_contract.py (run_main.py)", "result": "hands:none row FAIL got ('new', False, True); 3 old-road rows PASS"},
      {"command": "test_readiness.surfaces_said_aloud() alone on the branch", "result": "14 PASS"},
      {"command": "git merge-tree --write-tree origin/main HEAD", "result": "c52974d1, exit 0; origin/main adds nothing under ai-packages since base"}
    ]
  }
}
```
