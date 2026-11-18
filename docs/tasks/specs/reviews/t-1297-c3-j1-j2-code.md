# Code review: C3-j1 (t-1206) + C3-j2 (t-1269) + canon fix, branch worktree-agent-a5dcea7ed81ed1834 @ 6ee90c1e (t-1297, RD1-13, F19)

Spec: card r3 `docs/tasks/specs/20261117-rules-debt-c3-j-card-r3.md` (§2 j1, §3 j2, §B edges, the owner's correction at the end).
Diff: `git -C <worktree> diff origin/main...HEAD` (merge base 9d4ed53f).

**Verdict: NEEDS WORK (fit_with_fixes): accept once the fixes below are in. No blocking finding, so this is not a reject and carries no
failure_class.** The card is implemented as written and the four canon-fix choices hold (see C1-C4). What is left: one AR-4 contradiction
the Lead must decide (F1), docstrings that say something the code does not do (F2-F3), two copied blocks (F4), and a test volume over
budget, with builder-written `tests-over:` lines (F5). Deciding acceptance is the Lead's call (rule 6).

## The four canon-fix choices (asked by the dispatch)

- **C1 re-export drop: correct.** `gate_preflight.py:79` no longer imports `HANDED_MATCH_PREFIX`. Its only use in gate_preflight was
  `_stand_limit_card` (origin/main `gate_preflight.py:3370`, `waiver_command(f"{HANDED_MATCH_PREFIX} {profile_id}", ...)`), and j2
  deletes that function. No reader of `gate_preflight.HANDED_MATCH_PREFIX` is left: an `-i` grep over `ai-packages` and `tools` for
  `from gate_preflight import ...HANDED`, `getattr(...HANDED_MATCH`, `(GP|gate_preflight|G).HANDED_MATCH_PREFIX` → 0 hits. Positive
  control `(contract|C).HANDED_MATCH_PREFIX`, same flags → 9 hits. The handed reader `contract.handed_profiles` is still fed: option (c)
  of the executor question (`gate_preflight.py:511`) goes through waiver.py's phrase road (`waiver.py:1682`). Side effect: see N1.
- **C2 cache-asker pin 7: correct.** Enumerated `self.keyed_profiles()` in gate_preflight.py on the head: 2814 `check_s5_executor`, 2869
  `check_s5_dependencies`, 2945 `check_s5_toolchain`, 3069 `_page_load_due`, 3269 `check_s5_reporter`, 4257 `check_s5_runtime_probe`,
  4661 `_story_ids`. That is 7 sites, and the pin text names the same 7. origin/main also has 7 (with `check_s5_stand_limits`, without
  `_page_load_due`).
- **C3 moved probe anchors: correct.** Each anchor occurs exactly once in the source (`gate_preflight.py:3098`, `:3101`). Both are inside
  `self.note(check, f"...")` of `check_stand_page_load`, which is in `NEW_CHECK_FUNCTIONS` and in the expected set at
  `test_gate_preflight.py:3562`. So `source.replace(old, new, 1)` plants the token into a scanned message literal. The control stays a
  real negative control: if an anchor ever moves, "the scratch copy really differs" goes red loudly.
- **C4 scenario floor 20 → 15: acceptable.** My own count of `scenario_messages()` (`test_gate_preflight.py:3502-3555`) is a 9-label
  loop + 10 single `run()` calls = **19**. origin/main had 5 `limits` runs + the same 19 = 24, against a floor of 20. The arithmetic
  20 − 5 keeps the base's slack of 4 (24/20 → 19/15). The check's purpose is "not scanning nothing", so 15 is consistent with the base
  convention. A floor of 19 would be tighter but is not owed.
  **Siblings (floor pins in test_gate_preflight.py), none lowered:** `:3566` `len(literals) > 40` (same test); `:4607` waiver add sites
  `>= 18` (my static count: base 33 → head 30); `:4632` `WAIVER_SEEN > 40` (runtime; deleted k5 cards fed it; canon green); `:5044`
  add/note text sites `> 100` (base 205 → head 202); `:5064` `TEXTS_SEEN > 150` (runtime; canon green).

## Findings

**F1 (fix-before-merge; the decision is the Lead's): a machine fact is recorded in a carried record, which contradicts AR-4 and card E3.**
`project_knowledge.py:95` puts `no_browser` in `PAGE_LOAD_CAUSES`. `gate_preflight.py:3186-3218` (`_page_load_failed`) keeps any cause
in `records/project-knowledge.json`, which `project_knowledge.py:3-4` calls "carried by the project". At `attempts >= 2`,
`gate_preflight.py:3114-3120` stops measuring with no age limit (`page_load`, `project_knowledge.py:604-606`).
Scenario: machine A has no Playwright and runs gate A twice, so the reason `no_browser` gets attempts 2. Machine B, with a browser, runs
gate A on the same project: no attempt is made, and the note says "this machine has no browser the factory can start". That is false on
B (FR-41). B's `timeout_for` and briefs never get a number until somebody revokes the row.
Card E3 INVARIANT: "a machine fact never enters a carried record (AR-4)". Commit ae413f4e claims `AR-4 -- ... a machine fact is never
recorded`; 6aa3c34e then records it. The owner's correction («должна сохранятся причина») does not say "a machine's own fact too", and
the j1 builder raised exactly this question (report r1 Q2). The Lead decisions D1-D4 that answered it are not in my given, so I cannot
check them. Fix (Lead picks):
- (a) `no_browser` is not kept: noted per run, like the registry's own run-scoped `unreachable` state (`project_knowledge.py:152`);
- (b) the reason carries a machine identity and speaks only on that machine;
- (c) D1-D4 explicitly cover it: then correct the AR-4 commit line and the E3 wording.

**F2 (fix-before-merge): the "one row per stand / never appended" wording is false.**
- `project_knowledge.py:41`: "The row is replaced in place (one row per stand), never appended to."
- the `config-keys.json` `environments.page_load` note: "one row per stand".
- `gate_preflight.py:3083`: "keeps its REASON in the same row".
The code replaces in place ONLY when the held row is a reason (`project_knowledge.py:951`). A new measurement after 7 days is appended,
and so is a first failure that follows a measured row. The builder's own test asserts the append: `test_project_knowledge.py:1472-1474`
("the old append rule stands", 2 rows). Card §C also says "each new measurement is a new row". Fix: reword all three to "one subject per
stand; a kept reason is replaced in place; a measurement is a new row".

**F3 (fix-before-merge): after ff7f5b70, "the one list of writes" is incomplete.** `gate_preflight.py:1465` now points at `run()`'s
docstring as the single list. `run()` (`:6039-6042`) says "no other state file is written by this call or anything it calls". But
`_record_rehearsal` (`:3476`, via `:3828`) writes `qa-factory/state/reporter-rehearsals.json`, and the module docstring (`:19-23`) names
it together with `state/reporter-unread/`. The class docstring deleted by ff7f5b70 named the reporter write. Now no list at the class or
`run()` level is true. Fix: add the two reporter files to `run()`'s docstring (the false half of that docstring predates this branch; the
branch made it "the one list").

**F4 (fix-before-merge): two blocks copied inside the diff (Q6/Q7).**
(a) The urlsplit userinfo check, try/except included, appears twice word for word: `project_knowledge.py:744-749` and
`manual_capture.py:590-595`.
(b) The 120-character display cut with `…` appears twice: `gate_preflight.py:3142-3144` (`_page_load_address`) and
`brief_pack.py:2898, 2916-2918` (`STAND_LOAD_ADDRESS_CHARS`).
Fix: one helper each, beside `_safe_url` in manual_capture (both callers already lazy-import it). Smaller, a note only: the two `PK.record`
calls at `gate_preflight.py:3130-3132` and `:3205-3207` differ only in `value`.

**F5 (fix-before-merge, merge needs the Lead's reason): test volume is over budget, and builders wrote `tests-over:` lines (rule 20).**
`git diff --numstat origin/main...HEAD -- ai-packages/`:
- tests: +727 / −389 (test_project_knowledge +217, test_manual_capture +141, test_gate_preflight +295/−348, test_brief_pack +66,
  test_gate_registry +8);
- product (code + text): +467 / −252.
The branch is over by added lines and by net lines (+338 vs +215). `tests-over:` lines written by a builder: commit 6aa3c34e, commit
6ee90c1e, and the j2 report line 4. TESTING.md «Бюджет / Объём» gives the builder no such door. Rows to cut, weakest first:
1. `test_project_knowledge.py::test_page_load_kept_reason_shape` (`:1411-1447`, 22 rows). It is the write-side shape of a value only the
   gate builds (an internal boundary). The read door, a hand-edited file, is already covered by
   `test_page_load_a_broken_kept_reason_in_the_file_is_read_as_broken_never_as_a_pass` (`:1485-1501`). Rows "why at/over 200" also pin
   `PAGE_LOAD_WHY_MAX = 200`, a value the spec never named (Q5(b)). Keep at most "valid" and "cause not closed".
2. `test_project_knowledge.py::test_page_load_kept_reason_reads_replaces_in_place_and_is_never_a_pass` (`:1450-1482`). Its in-place,
   another-cause, number-replaces and another-definition assertions are asserted again through the factory's door by
   `test_gate_preflight.py::test_c3_j1_a_kept_reason_gets_one_more_try...` (`:5962-6032`). Keep only "a reason has no age" (`:1464-1466`)
   and "a number appends" (`:1472-1474`), which the gate test does not reach.
Cut 1+2 ≈ 60 lines. The rest of the gap comes from rows the card itself mandates (§2 item 6), so it is the dispatcher's budget defect
(TESTING.md: the dispatch lists rows by strength). The `--tests-over` reason at merge is the Lead's to give.

**F6 (note): the DOC-DISPATCH witness was never produced, and the prose key moved.** j1 report r1 :84-86 says no key-presence script
with a negative control was run (rule 7). The canon fix shortened `references/manual-evidence.md:56-57` (selftest `--limits` cap) to "A
step takes 180 s, or the stand's measured load + 30 s if longer". That is not the card's verbatim key, but the meaning is the same (V2
F2 floor). I checked it by reading. Lead: accept the wording, or have the witness run on the new key.

## Notes (no fix owed in this branch)

- N1: `contract.py:125` still says "`gate_preflight` writes `f"{HANDED_MATCH_PREFIX} {profile_id}"`". After C1, gate_preflight writes
  no such f-string (grep `HANDED_MATCH_PREFIX}` over `scripts/`, non-tests: only that docstring). This is outside owns: a one-line
  sibling for the Lead.
- N2: `_page_load_value_faults` reports an unparsable address (`urlsplit` ValueError, `project_knowledge.py:748-749`) as "carries a user
  name or password". The refusal still points the safe way, but its text is wrong.
- N3: the brief has no row for state `failed`. It goes through the same `!= "measured"` branch as `none` (`brief_pack.py:2914`), which
  `c3_j1_stand_page_load` covers. Given F5, no row is asked.
- N4: `check_stand_page_load` is 64 lines including an 11-line docstring (`gate_preflight.py:3076-3139`), at the ~60 threshold, nesting ≤ 3.
  `measure_page_load` (`manual_capture.py:573-633`) is about 60. No Q7 finding.

## Standing questions

- Q1 FIT: j1 items 1-7 match the card. Checked: `page_load`'s 11 steps in card order; `timeout_for` = `max(180, load+30)`; all 8 callers;
  StepTimeout caught before StepFailed (they are sibling classes, `manual_capture.py:140,178`); the `blocked` event shape matches
  `_record` (`:1765`, `"kind"`); the brief texts are verbatim; STAND_LOAD_ROLES; `s5_kind` is bound for every stage (`brief_pack.py:4501`);
  the gate A position. The owner's correction is implemented (reason row, one retry, then the note carries it; tested). j2 items 1-5 are
  done: grep of the 7 deleted names over the package → only `design/factory-rules-debt.md:111` (the known Lead residual), the j2
  changelog, `cost_capture._limit_seconds` (a different function), and `test_manual_capture.py:193` (a negative row). Deviations: F1, F6.
- Q2 BUILDER'S DECISIONS: identity in the reason value; a broken reason reads `none`/malformed (the safe side, retry); `_kept_page_load`
  deleted with its only reader; the k3 test world switched off the new writer (`skip_stand_limits`) and kept its "no file added"
  assertion. All point the safe way, except keeping `no_browser` (F1).
- Q3 SEAMS: additive and localized. The census row was replaced in place (same position, same class shape/data). The registry row was
  deleted, no reordering.
- Q4 CLASS-WIDE: axis 5 prose twins grepped by the builders (j1 r2, j2), and my own grep agrees. Lines for the Lead to put into «Остатки»:
  - `reporter timed_out card asks a person for a timeout | узел: <new id, rules-debt>` (F-j-reporter). The Lead decided to open it after
    j2; grep of `plans/piles/rules-debt/*.md` for `timed_out|reporter_timeout_s` → 0, so it is not opened yet. Positive control `RD1-13` → hits.
  - `design/factory-rules-debt.md:111 lists the deleted gate s5_stand_limits | узел: RD1-23 (S1b)`.
  - `B-282 (debt_ref of the deleted row) has no subject left | узел: <Lead closes B-282>`.
  - N1 (`contract.py:125`).
- Q5 TESTS: (a) the defect the node exists for is caught at the factory's own door: a recorded 160 s makes the sign-in probe open with
  190 s (`test_gate_preflight.py:6090-6107`); the measure/reuse/identity rows and the brief rows cover the rest. (b) values trace to the card
  (180/190/210, 120 cut) and to the owner's word (attempts 2). `PAGE_LOAD_WHY_MAX` 200 has no source: F5 row 1. (c) new doors have rows.
  (d) the deleted tests are listed by name in the j2 report, and the spec removed that behaviour. (e) duplicates: F5 row 2. (f) volume: F5.
  (g) no new file.
- Q6 DUPLICATION: F4. Searched: `urlsplit` userinfo pattern, `\[:120\]` / `120` cut in brief_pack and gate_preflight, and
  `stale_against_verified` (one body, moved verbatim; old body deleted).
- Q7 CODE QUALITY: F2, F3, N2; no dead branch found; nothing over the size threshold (N4).
- Q8 HYGIENE: 0 Cyrillic lines among the added package lines (python scan; control line → 1); 0 CR in the diff.
- Q9 RATCHETS: census row −1 +1, ceilings unchanged (j2 report; canon green). gate-registry debt 2 → 1 (shrink). Lint baseline not
  touched (`forge-check` success in canon). ROLE_BRIEF / S5_PLAN bytes equal before and after (j1 r2 witness). No raise.
- Q10 ARCHITECTURE: AR-3/4/10/13/14/22/25/28/29 are named in ae413f4e, AR-17/23 in 6aa3c34e, AR-7/15/20/22/28 in 76a73838. AR-14 walked:
  writers of `PAGE_LOAD_KEY` = the two `PK.record` calls in gate_preflight (one check); the reader is `PK.page_load` (j1 r2 grep, and my
  read agrees). AR-4: F1. AR-15 (the delegate) is not named in j1, only in j2: minor. VARIETY: an API-only or device stand → `n/a`, no note;
  a browserless machine → note, default limit, no block. On a team with mixed machines, F1 silently starves the capable machine. No stage
  is stopped.
- Q11 JUDGMENT: none moved. `check_stand_page_load` is a data/shape census row; the "two attempts" stop is machine policy, not a role's
  judgment.
- Q12 ONE ROAD: gate A is the point both roads pass (`run` tuple `:6052`). Searched the added product lines for language/runner names
  (`pytest|playwright|cypress|selenium|java|dotnet|node|kotlin|swift`, `-i`): 1 hit, the existing default `PlaywrightBackend`, not a branch.
  No exclusion stays.

## Spot-checks of the submitters' claims

- "canon 44196940524 success on the head": `gh run view` → conclusion success, event workflow_dispatch, created 2026-11-17T23:10:10Z,
  1 min after 6ee90c1e (00:09:09 +0100). Its `headSha` 200f39b3 is the dispatching ref on main, not the branch, so the branch sha
  itself was not read from the logs (estimate, not verified beyond the timing).
- "cache askers are seven": reproduced (C2). "five stand-limit scenarios deleted": reproduced (C4). "no other reader of the re-export":
  reproduced with a control (C1).
- "test_project_knowledge page-load rows pass": re-ran (trail).

## Trail

- Read: card r3 whole (1-638); both reports whole; critic.md (given). In the worktree: diffs of project_knowledge.py, manual_capture.py,
  investigation_probe.py, walk_session.py, brief_pack.py, references/*, scaffold.py, changelog.d, test_gate_registry.py; gate_preflight.py
  hunks + `:500-521, 1540-1555, 3055-3245, 6030-6060`; test_gate_preflight.py `:3270-3301, 3420-3589, 5862-6107`; test_project_knowledge.py
  `:1350-1534`; contract.py `:115-130`; stand_identity.py `:129-154`; manual_capture.py `_safe_url`, `_record`, `goto`; origin/main
  `scenario_messages` and `_stand_limit_card`.
- `python -B -m pytest scripts/tests/test_project_knowledge.py -q -k "page_load or five or FIVE"` (cwd the package, subshell) →
  `43 passed, 157 deselected in 4.80s`.
- `python -B <scratchpad>/sites.py gp_base.py gate_preflight.py` → `waiver add sites 33 / 205` (base), `30 / 202` (head).
- Enumeration of `self.keyed_profiles()` with enclosing defs → 7 (listed in C2); origin/main count → 7.
- Grep (above) for the deleted names, the re-export, Cyrillic, CR, and language names, each with its control.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "Canon-fix choices hold: the re-export has no reader left (control 9 hits), the asker pin 7 matches the 7 enumerated sites, the anchors are single live literals in a scanned function, the floor 15 keeps the base slack (count 19). Floor siblings in test_gate_preflight.py: 3566, 4607, 4632, 5044, 5064, none lowered. Residuals for the Lead: the reporter timed_out card (F-j-reporter node, not yet opened), design/factory-rules-debt.md:111 (RD1-23), B-282 with no subject left, contract.py:125 stale docstring.",
  "fixes": [
    "F1 fix-before-merge (Lead decides): no_browser reason kept in the carried registry contradicts AR-4/E3 (project_knowledge.py:95, gate_preflight.py:3186-3218, 3114-3120); drop no_browser from keeping, or key it by machine, or correct the AR-4 claim if D1-D4 cover it",
    "F2 fix-before-merge: project_knowledge.py:41, config-keys.json environments.page_load note, gate_preflight.py:3083 claim one row per stand / never appended; a measurement appends (project_knowledge.py:951, test_project_knowledge.py:1472-1474)",
    "F3 fix-before-merge: gate_preflight.py:1465 names run() docstring (6039-6042) as the one list of writes, but it omits state/reporter-rehearsals.json and state/reporter-unread/ (written via _record_rehearsal 3476)",
    "F4 fix-before-merge: copied blocks - urlsplit userinfo check (project_knowledge.py:744-749 = manual_capture.py:590-595) and the 120-char cut (gate_preflight.py:3142-3144 = brief_pack.py:2898,2916-2918); one helper each",
    "F5 fix-before-merge: test lines over budget (+727/-389 vs product +467/-252) with builder-written tests-over lines (6aa3c34e, 6ee90c1e, j2 report); cut test_project_knowledge.py::test_page_load_kept_reason_shape (1411-1447) and trim test_page_load_kept_reason_reads_replaces_in_place (1450-1482); the remaining gap is the Lead's merge reason",
    "F6 note: DOC-DISPATCH witness not produced; manual-evidence.md:56-57 wording differs from the card key (meaning equal)"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-rules-debt-c3-j-card-r3.md",
      "worktree docs/tasks/specs/reports/20261117-rules-debt-c3-j1-report.md",
      "worktree docs/tasks/specs/reports/20261117-rules-debt-c3-j2-report.md",
      "worktree ai-packages/qa-factory/scripts/project_knowledge.py (diff, 1-41, 239-253, record)",
      "worktree ai-packages/qa-factory/scripts/manual_capture.py (diff, _safe_url, _record, goto, events)",
      "worktree ai-packages/qa-factory/scripts/gate_preflight.py (diff hunks, 500-521, 1540-1555, 3055-3245, 6030-6060)",
      "worktree ai-packages/qa-factory/scripts/brief_pack.py (diff, _stand_pick, s5_kind binding)",
      "worktree ai-packages/qa-factory/scripts/tests/test_gate_preflight.py (3270-3301, 3420-3589, 5862-6107, floor pins)",
      "worktree ai-packages/qa-factory/scripts/tests/test_project_knowledge.py (1350-1534)",
      "worktree ai-packages/qa-factory/scripts/contract.py (115-130)",
      "worktree ai-packages/qa-factory/scripts/stand_identity.py (129-154)",
      "worktree references/config-keys.json, gate-registry.json, manual-evidence.md diffs",
      "origin/main gate_preflight.py _stand_limit_card, test_gate_preflight.py scenario_messages",
      "docs/TESTING.md Budget section"
    ],
    "reruns": [
      {"command": "python -B -m pytest scripts/tests/test_project_knowledge.py -q -k \"page_load or five or FIVE\"", "result": "43 passed, 157 deselected in 4.80s"},
      {"command": "gh run view 44196940524 --json conclusion,headSha,status,name", "result": "success, workflow_dispatch, created 23:10:10Z one minute after 6ee90c1e"},
      {"command": "static count of keyed_profiles() asks and of waiver/add-note sites (scratchpad sites.py)", "result": "7 askers; waiver add sites 33 -> 30; add/note text sites 205 -> 202"}
    ]
  }
}
```
