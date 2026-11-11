# t-2027 — critic on the analyst's later nodes (spec t-1991: U0, U3b, U4) and the fix round t-2014

Critic (Opus), 06.11.2026. Tree read: `D:/ws1/wt-fbfix` at `95047228e`, clean. `PKG` = `ai-packages/qa-factory`, `PA` = `PKG/scripts/place_answers.py`, `SR` = `PKG/scripts/story_run.py`. Probes ran on harness temp stories only; the stand, `tr-walk` and the stand lease were not touched. The acceptance decision belongs to the Lead.

**Verdict: NEEDS WORK (`fit_with_fixes`). 3 blocking (F1-F3), 7 to fix before merge (F4-F10), 3 low (F11-F13). No redesign.**

The core holds on real code: the per-request lease works against a real second process, and the road from a place to a question at gate B works. What fails: a settle session's record is read as a case walk on every re-entry; the person's `bug` road has no carrier; and a DoD pin is red at head while CI is green, because CI cannot see that file.

## Blocking

**F1 (Q1, high). A settle record is read as a case walk: the U3b record broke the walker's "one site" hook.** `SR:3404` `walk_reopen` takes any `state/walks/<D>.json` with items as a case lane; it never reads the record's `place`. Called from `run_role` (`SR:2916`), `resume_role` (`SR:3269`) and `_finish_saved_result` (`SR:16004-16008`). The settle session writes that same path with place ids as items. The rig hides it: `test_place_session.py:66` stubs `walk_reopen`. Probe with the real function, a closed settle record, the rig otherwise as is:
```
A1 resume_role:
walk_session.py ('open', '--task-root', ..., '--walk', 'S7-qa-failure-analyst-1', '--items', 'req-R-1,case-TC-006', '--actor', 'guest')      <- no --place: a CASE lane
S6: req-R-1: the record of its walk was refused (work/evidence/manual/req-R-1/request.json does not exist ...); it is walked once more in the next lane
files: work/walks/S7-.../after.json, case-TC-006.json, req-R-1.json, timing.jsonl
walk_retry: {'req-R-1': {'refused': 1, ..., 'open': True}, 'case-TC-006': {...}}
A2 run_role continuation: the same case open, then open --place settle (real server: refused, already open); walk_after runs
A3 saved result, no role runs: walk_after still runs; after.json rows "req-R-1": {"state": "refused", ...}
```
Scenario: any resume (a halt, a threshold question) or a driver restart on an S7 triage dispatch. The role is told "its captures are under settle-<place id>", while the real server is a case lane: the attempts land under `manual/<place id>/` so `seen.capture` is refused; the lease is held for the session's life, so the analyst's own `run_suite` waits 1 800 s then gets `stand_busy`; `idle_s` applies; `finalize_task.py` runs; `walk_retry` gets place ids with `open: True`, read by S6 (`SR:12445`).
Fix: `walk_reopen` answers `([], "")` when the record's `place` is set and not `case`. `open_walk` must also write `place` in its "opening" record (`walk_session.py:1355`): a failed open leaves that record with no `place`, and `s7_settle_session` does not remove it (`walk_before` does, `SR:3361`). Test in `test_place_session.py` with the real `walk_reopen`, on all three roads; the rig's stub goes.

**F2 (high; fix round, U4 key). A DoD pin is red at head and CI cannot see it.** The dispatch's "canon fully green" does not cover this file.
```
FAILED test_charters_s5_s9.py::test_craft_keys_stand_verbatim[qa-failure-analyst]
the craft key `an expectation the factory derived itself is no requirement` is not in the charter
1 failed, 58 passed in 3.49s
```
`test_charters_s5_s9.py:61` holds U4's key; `agents/qa-failure-analyst.md:54` says "one the factory derived itself is no requirement", reworded by `fa688b70d` (t-2021), whose message says "pins follow". Why CI stays green: `selftest.py:396` runs each test file as a script; this file has no script entry (`python -B test_charters_s5_s9.py`: no output, `exit 0`); `.gitlab-ci.yml` has `-m pytest` only for `tools/` (:110). Fix: restore the words or change the pin, by the Lead's choice (role-load margin 8 B at U4). **Class, for the Lead:** by an AST count, 13 of 680 test files define `test_*` and run nothing as a script: `test_charters_s5_s9`, `test_charter_form`, `test_exit_gate_advice`, `test_exit_limit_halt_answered`, `test_handoff_init_author`, `test_open_list_fields`, `test_open_vocabularies`, `test_probe_gap_door`, `test_probe_target_fact`, `test_rework_dispatch_files`, `test_rows_owed`, `test_stage_review_person_pass`, `test_walk_charter`. Three of them are this batch's or the walker's. Each needs a script entry, or `selftest` must refuse a file that ran nothing. I did not check whether the other twelve are red: a scout or one batch run.

**F3 (Q5, high; SPEC, t-2010 F15 still open). The person's own `bug` has no road.** `PA:351-359` requires `expectation.id` = a file under `state/words/`; the door says "as the brief gives it". No brief gives it: 0 hits for `state/words` in `brief_pack.py` and `story_step.py`, case-insensitive; the same grep finds it in `story_run.py` :1401, :1447, :5332, all docstrings. `s7_place_lines` and the rework prompt carry the words, never the path (`SR:2890`: `Rework reason: <words>`). Scenario: a question at gate B, the person writes `bug`, one rework; the analyst cannot name the file; `source: none` and an unconfirmed `requirement` are refused, so the record stays `requirement_silent`. That is §3.4's road and the owner's case. Whether the role could find the file by listing the folder was not established; a road that rests on that is no carrier (AR-8, FR-15). Fix (recommended; SPEC, rule 5): for `person`, `id` may be empty and the quote is checked against the dispatch's `reason`, keeping the `person_words` mark. That is the same invariant with no path to carry.

## Fix before merge

**F4 (medium, E3b.2).** `close` waits for the lease and then does not close. `walk_session.py:968` with `LEASE_OPS` (:64, incl. `close`). Probe, another job holding the stand: `close: 3 stand_busy state: ready watchdog: ''`. The session then outlives its dispatch by up to `max_s` (90 min): the driver is alive and `idle_s` is exempt. `s7_settle_close` prints "the server ends by itself", and `s7_walk` says `closed`. Fix: on `StandHeld`, a `close` shuts down without the end probe (`probe=False`), with a note. SPEC: §3.6 lists `close` as page-touching.

**F5 (medium, FR-10/AR-8).** The reopen row is stale after c9aa9ad32: `role-commands.json:67` says `--items free`, as does the docstring `SR:13519`. The Commands card gives it; following it opens a session with the one item `free`, and every `--item <place id>` is refused. The brief line (`SR:13511`) is right. Two texts, one wrong. Fix the row: "the items your brief's session line names".

**F6 (medium, FR-2).** The reopen door dies with the shell: `open_walk` uses `os.getppid()` (`walk_session.py:1347`), the role's Bash; the watchdog ends the server within `parent_check_s` 5 s (:1172). By reading, not run; the spec's F38 expected it, the door still says "reopens it". Fix: the session line passes `--parent-pid <the driver's pid>`, or the door names only `manual_capture`.

**F7 (medium, AR-10).** The analyst has no card for the session's steps: `walk_session.py step|look|final|status` rows name `qa-runner` only (`role-commands.json:77-112`), and the brief line omits `--line` / `--steps-file`. A refusal names them, at the price of one failed call per run. Fix: add the role to those four rows (`test_role_commands.py` keeps BROKEN entries); `verdict`, `item`, `done` stay out.

**F8 (medium, AR-2, E1.18).** Session items are frozen at open. Probe: `item 'new-x' is not in walk ... (items: p1)`; the door is only `status`. The role's own `new-<slug>` and a draft written in the dispatch cannot use the session, and the refusal does not name `manual_capture`. Fix: a settle lane accepts any id passing `LANE_ID`; or the refusal names the capture road.

**F9 (medium; a project's case ids).** One odd id loses the session for all places. Probe: `['req-R-1','draft-a__b']`, and the same for `draft-BUG 1` and `case-TC/6`: refused as "not a plain id". `case_dir_name` accepts `area/TC` as a case id, so a project with area cases gets `failed: session` on every S7. Fix: `s7_settle_session` opens the ids that pass, and the line names the rest with the capture road.

**F10 (medium, fix-round's own, the F2 class of t-2010).** A stale `place-gap-` line survives a settled place. Probe:
```
withdrawn EX-2 settled / no lift: carrier missing
close ['EX-3','EX-4'] ['req-R-1: its chain was withdrawn; the gap is written under place-gap-req-R-1']
settled again: settled / close2 [] []
place-gap active after settled: True "the run left this suspicion unchecked: R-1 ..."
gate gaps: ['- the run left this suspicion unchecked: R-1: ...']
```
`PA:578-593` looks only at `chains[place id]`. Fix: the withdraw loop also withdraws an active `gap_target_prefix + id` line of `by_close`. Rare path, false text to the person.

## Low

**F11.** `SR:13549` `"stand" in why.lower()` classifies on free text; "understand" or a path holding "stand" gives "the stand could not be reached" (FR-12, FR-41). Use the exit and `status` of `open`'s answer.
**F12.** `SR:2907-2910` and `:2920-2923` are the same block twice (merge residue), and `retire_infra_result` is called twice. Delete the first or second.
**F13.** Charter :65 `the publication.- Verdict words:` merges two bullets (U4). The file lost its last newline.

## Answers

1. **One site per concern: the insertions yes, the hook no (F1).** Place lines: one site, `test_one_site_for_place_lines`; `stage_S7`'s append removed. Session: one opener, called by `run_role` and `resume_role`, one closer in each `finally`, deviation 1 is required by E3b.5 and safe. The walker's hook is the defect: its t-2016 definition "a dispatch with a walk record is a walk" was not updated. **Two live servers on one dispatch: no** (one record path; `request_problems` "already open", by reading; `s7_is_triage` needs `qa-failure-analyst`, a case lane is `qa-runner`). **The real failure is worse: one settle record gets reopened AS a case session** (A1). Openers `walk_before` / `s7_settle_session` and closers `walk_after` / `s7_settle_close` duplicate the reason-to-text code (builder's note): queue.
2. **E0.4 on real code: holds for page requests, fails for `close`.** Real second process holding through `stand_lease.hold`: `step` waited and ran (`0 done`, 10.1 s, holder 6 s); lease set empty after. Held past the wait: `step: 3 stand_busy suite:other`, session `ready`. `test_walk_places`: 69/69 at head. The boundary at 60/61 s is pinned with a fake clock, and the assertion reads right. `close`: F4. **F1 voids E0.4 on a resumed dispatch** (a case lane holds the lease for life).
3. **Yes, the narrowing is safe; I propose the Lead confirms it.** The section is the filed `bugs/BUG-n.md` header, written by the reporter after gate B. Slice check on the analyst's page: `title, impact, violates, case, triage_ref, manual_steps, oracle, fact, check_state, reproduction, walk` all present; control `no_such_key_x` absent. No `BUG-n` reference is left dangling (grep of the analyst's slices and charter: none; the same grep finds it in `qa-doc-scribe`'s). The draft section stays whole. U4's OTHER cuts need the Lead's eye:
   - `faq.md` is gone from everything the analyst loads (grep: none); it left with F-I, allowed by E4.1.
   - "quarantine is gate B's": the report says it is in the slice; grep finds no `quarantine` there. A false report line, low.
   - "Two readings both tenable: one question with both quotes" removed. Charter :53 "the product bug is the default" now stands alone. That also removes an old clash, in favour of `bug`. It does not break the owner's word: :50 keeps silent -> question. It is a meaning change made by a load cut: **the Lead's decision, SPEC.**
4. **Experience, yes; principle numbers, none.** Grep of `P<n>`, `FR-`, `AR-`, `AC`, "must run", "Step <n>" in the charter: none; the same test's numbers pin is in a file CI does not see (F2), so I grepped. "Find out the truth on the page" is a tester's craft: what to do, how to look, which words decide. The Tools line naming `place-gap-<id>` (from U3b, item d) is process the role cannot act on: cost low, in a `process` section, no census effect. Craft share 0.58 by the test's own print.
5. **The road holds up to gate B and breaks after it.**
   - Only the unconfirmed: `PA:260`, triage verdicts are no place: holds.
   - A silent requirement is a question: `requirement_silent` -> `unresolved_question`, `owner_question`. Probe: `'text': '- R-1: ... The question: Should the total show two decimals? No test case is named for it - answer in words.', 'addressable': False`; on `case-TC-006`: `addressable: True`. **This settles the spec's "could not establish" (F4 of §2):** a `req-` place is shown, not addressable; its answer is free words to the conductor.
   - Never a bug: `none` refused, unconfirmed R refused, `requirement_silent` cannot lift (`R_WALK_ANSWER`, tests).
   - The report reads the same register (`report_facts.py:292`, by reading, not run).
   - After the person's `bug`: **F3.** After the person's `intended`: `settled_answer` accepts `by` `person` / `person:`; the driver's real `by` was not traced: a live key.
   - A silent answer beside an unconfirmed draft reads `conflict` and keeps its question (F5 of t-2010 holds), and the draft still stands as unconfirmed beside it: said out loud, not hidden.
6. **Owed first, for a live proof on 3-5 places:**
   - Before any run: **F1** (one resume or restart corrupts S7), **F2**'s pin, **F5**, **F7**, **F4** (a live stand is often held).
   - Before key (3) on the person's road: **F3**.
   - **U2b is on branch `au2b`, not in this head** (`test_walk_oracle.py` absent; commit `d257a48e9`): without it F-J reads as t-2010 F14, and an `obs-` join is still not stated.
   - **t-2010 F13** (two drafts of one place): arm B has 7 drafts on R-12/13/14; a second draft reads settled-with-unconfirmed. Decide before reading key (2).
   - **The account (U3b Q2):** a session is `guest` only (`SR:13479`); whether `fill-account` works there is not established. MyBooks places behind a sign-in go by `manual_capture`. Lead's question.
   - Not established, watch first: `manual_capture.py ui|http --case settle-*` with no `request.json` (spec F9, t-2010); F6 on a real shell; N3 (a `settle-` folder named as an unknown case).

## Fix round t-2014, finding by finding

F1, F2: `PA:713` withdraws only when settled; probe B3 reads `withdrawn EX-2 settled`, then the gap under `place-gap-`: closed, F10 is its residue. F3: `investigation.py` `_settled_by_analyst`, `test_investigation` 260/260 re-run: closed. F4: U3b `gate_brief.py:4336`, test in `test_place_session` 12 passed: closed. F5 (a-c): `PA:597`, `:612`, `:627`, `:506` read; B2 shows the question addressable: closed. F6, F8, F9, F11, F12: read against the diff: closed; `gap_reason_names` repeats `gap_reasons`, pinned equal, the builder named it: accept. F7: code closed, **spec §3.2:287 still says `impossible`**. F10: `SR:13464` names the keys: closed. F13-F15 stay as t-2010 SPEC items: F15 is F3 here, F14 needs U2b. `test_place_answers` and `test_walk_receipt` were not re-run: the witness 89 passed is consistent with the diff, and both have script entries.

## Standing questions

- **Fit to the spec:** U0 as written, E0.1-E0.6 read and E0.4 run, except `close`. U3b: F1, F5. U4: above F-I it cut text the spec did not name; E4.1 said STOP. The builder asked instead of stopping: the Lead's call, the cuts are listed.
- **Builder's decisions:** U0's `_take_final` flush is right; U3b's Q1 was answered by c9aa9ad32 and left F5; Q3 (unreadable kind -> no session) is the safe side.
- **Seams:** `run_role` additive except the block F12; `test_story_run_s7.py` pins changed by report.
- **Class-wide (SIBLING_MAP):** axis 5 twins: `s7.md` names the close order and `place-gap-`: covered. Axis 31: charter + investigation line: covered. Readers of `state/walks/*.json` by grep, `state/walks`, positive control the known `SR:3404`: `SR` (hook, F1), `brief_pack.py:3221` (gated on `qa-runner`, safe), `walk_session.py`, `walk_timing.py:64` reads `work/walks`. **`timing_line` writes `PLACE = "case"` (`walk_session.py:329`, :549) for a settle item:** Stage 2's "grouped by place `settle`" (§4) cannot be read as written; add to F8's node. Rest of the map: not walked beyond these.
- **Tests:** `test_session_closed_when_role_crashes` kills its mutant, by reading. Missing: the real `walk_reopen` on a settle record; `close` under a held lease; place-gap after settle.
- **DUPLICATION AND CONSISTENCY:** F12; opener and closer pairs (queue); `s7_session_line`'s door text twice in one function, `SR:13504-13507`. `U3b` reuses `_hold_stand`, `case_root`, `_refuse`. No second lease or attempt root: grep `hold_stand|case_root` in `walk_session.py` finds only the helpers.
- **CODE QUALITY:** F11-F13. `s7_place_lines` about 40 lines, `s7_settle_session` about 40, under the limit. `run_role` is over 60 by history.
- **Ratchets:** `role-load` analyst 17,753 -> 17,751, 16,145 -> 15,999 at U4, lowered; `fa688b70d` says kept; no raise seen in these commits. Census not raised by U3b (`de7fa296e`).
- **ARCHITECTURE:** U0, U3b, U4 name their AR. **F1 breaks AR-13/AR-14 by the hook's reading; F3 breaks AR-8, AR-24; F10 AR-27.**
- **JUDGMENT:** none moved into code; F11 is a code word about code's own text, not a role's. No new `kind: craft` marker in the diff.
- **Hygiene:** FR-30 by witnesses, not re-run. SPEC sync owed: §3.2:287, §3.6 `--items free`, `close`.

## Spot-checks

- Negative "no carrier of the words path": above, with a positive control.
- Negative "no `BUG-n` for the analyst": above, with a positive control.
- Witness consistency: U3b 12 tests in `test_place_session` matches my re-run; U0 69/69 matches.
- "Canon green": **did not reproduce for one file**, F2.

## Trail

Read: spec t-1991 whole; t-2010; the brief; reports t-2011, t-2012, t-2014, t-2019; diffs of 909a2394a, 67d4392f7 (charter, s7, role-commands), ed0045010 (investigation, bug_records, data); `PA` whole; `SR` `run_role`, `resume_role`, `walk_before`, `walk_reopen`, `walk_after`, `s7_*`, :12445, :12822, :16004; `walk_session.py` lease, roots, ops, `request_problems`, `open_walk`, `call`, `watchdog`; `manual_capture._hold_stand`, `case_dir_name`; `run_suite.hold_stand`; `report_facts` `_annotate_cases`, `exploratory_gate_parts`; `brief_pack` :3205-3303, :3425, :3490; `selftest.py` :147-156, :390-416, :540-575; `.gitlab-ci.yml` greps; helpers of `test_place_session`, `test_place_answers`, `test_walk_places`.

Needed beyond the manifest: `selftest.py`, `.gitlab-ci.yml`, `report_facts.py`, `brief_pack.py`.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "F1 story_run.py:3404 walk_reopen reads a settle record as a case walk on resume, continuation and saved result: a case lane is opened for place ids, lease for life, walk_after builds case records and walk_retry gets place ids; the rig stubs it at test_place_session.py:66",
    "F2 test_charters_s5_s9.py:61 U4's key is red at head against the charter :54 (fa688b70d); selftest.py:396 runs files as scripts, so 13 of 680 pytest-only test files assert nothing in CI",
    "F3 place_answers.py:351-359 the person source needs a state/words path that no brief gives (t-2010 F15): the person's gate-B bug has no road"
  ],
  "fixes": [
    "F1: walk_reopen answers empty for a record whose place is not case; open_walk writes place in the opening record; a test with the real walk_reopen on three roads",
    "F2: the Lead chooses the words or the pin; each of the 13 files gets a script entry or selftest refuses a file that ran nothing",
    "F3 (SPEC): for person, id may be empty and the quote is checked against the dispatch reason, the person_words mark kept",
    "F4: close under a held lease shuts down without the end probe; spec 3.6",
    "F5: role-commands.json:67 and the docstring story_run.py:13519 drop --items free",
    "F6: the session line passes --parent-pid of the driver, or the door names only manual_capture",
    "F7: qa-failure-analyst added to the walk_session step, look, final, status rows",
    "F8: a settle lane accepts an id passing LANE_ID, or the refusal names manual_capture; timing_line writes the lane's place, not the constant",
    "F9: s7_settle_session opens the ids that pass and names the rest",
    "F10: the close withdraws an active place-gap line of a place now settled",
    "F11: the failure class reads the exit and status, not a word in the text",
    "F12: delete the repeated saved-result block in run_role",
    "F13: split the merged bullet at charter :65, restore the last newline",
    "SPEC: section 3.2:287 drops impossible; the Lead decides on the removed two-readings line and on the U4 cuts beyond F-I; the account of a session; merge of au2b; t-2010 F13"
  ],
  "class_completeness": "Readers of state/walks walked by grep: story_run hook (F1), brief_pack (gated on qa-runner), walk_session, walk_timing (place constant, F8). Surface of F1 walked: resume, continuation, saved result, failed open. Surface of F4: each LEASE_OPS op under a held lease by reading, step and close by probe. Pytest-only test files: counted, 13 of 680; whether the other 12 are red is a request for one batch run. Axes 5 and 31 covered; axis 18 no raise; the rest of the map not walked beyond these.",
  "trail": {
    "read": [
      "docs/tasks/specs/t-1991-analyst-settles-places.md whole; reviews/t-2010; docs/tasks/critic-diff-brief.md; reports t-2011, t-2012, t-2014, t-2019",
      "wt-fbfix at 95047228e: place_answers.py whole; story_run.py run_role, resume_role, walk hook, s7_*; walk_session.py lease, roots, ops, open_walk; report_facts.py gate parts; brief_pack.py walk card; selftest.py runner; .gitlab-ci.yml greps",
      "git show 909a2394a, 67d4392f7, ed0045010; commit lines of 246f9405f, c9aa9ad32"
    ],
    "reruns": [
      {"command": "real walk_reopen with a settle record on the rig of test_place_session (resume, continuation, saved result)", "result": "case open without --place; records refused; walk_retry holds place ids; as quoted in F1"},
      {"command": "python -B -m pytest -p no:cacheprovider PKG/scripts/tests/test_charters_s5_s9.py -q", "result": "1 failed, 58 passed in 3.49s"},
      {"command": "python -B PKG/scripts/tests/test_charters_s5_s9.py", "result": "no output, exit 0"},
      {"command": "python -B PKG/scripts/tests/test_walk_places.py", "result": "=== test_walk_places: 69/69 ok ==="},
      {"command": "python -B PKG/scripts/tests/test_place_session.py", "result": "test_place_session: 12 passed, 0 failed"},
      {"command": "python -B PKG/scripts/tests/test_investigation.py", "result": "=== test_investigation: 260/260 ok ==="},
      {"command": "lease probes on temp projects: second process holding; a job holding with a 1 s wait", "result": "step 0 done after the holder ended; step 3 stand_busy; close 3 stand_busy, state ready, watchdog empty"},
      {"command": "gate B and place-gap probes on temp stories", "result": "req place addressable False, case place True; place-gap active after settled, as quoted in F10"},
      {"command": "grep state/words -i in brief_pack.py, story_step.py; control story_run.py", "result": "0 hits; control 3 docstring hits"},
      {"command": "AST count of test files with test_ defs and no script entry", "result": "13 of 680"}
    ]
  }
}
```
