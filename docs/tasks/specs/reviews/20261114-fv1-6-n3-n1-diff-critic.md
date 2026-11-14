# t-810 critic, diff gate: FV1-6 N3 (eefe80e6) and N1 (67b337af), one pass for the topic

Spec: `docs/tasks/specs/20261114-fv1-6-s4-only-spec.md` (cards N3 and N1, §3.1, §3.3, §3.4, §4). Plan verdict: `reviews/20261114-fv1-6-s4-only-plan-critic.md`.
Builder reports: `reports/20261114-fv16-n3-report.md` and `reports/20261114-fv16-n1-report.md`. Code read on the wave13 merge tree.
N2 has its own verdict and was not reviewed again.

## Verdicts

- **N3: GO WITH FIXES.** No blocker. Fixes N3-1 to N3-4 go in one fix round.
- **N1: GO WITH FIXES.** Fix N1-1 **blocks acceptance**: the person is told something false. Fixes N1-2 to N1-6 go in the same round.
- Lead decision (a), N3 bare case id: **upheld.** (b), N1 `budget=None`: **upheld.** (c), N1 no cap on the case list: **upheld, no cap owed.** The reasons are under "Lead decisions".

## Findings, N3

**N3-1 (should-fix, FR-41 / AR-28): an unknown printed as a count of 0.**
- Where: `report_facts.py:4203` (`_r_review_gaps`) and `:4190` (`gate_b_gap_lines`). The heading is built from `len(left['items'])`.
- Input: a remark list that cannot be read (`problem` set, items always `[]`).
- Output today: `### Case review remarks the automation did not act on — 0` followed by `Unknown — ...`. Row P9 pins exactly that.
- Why it is wrong: the heading states a count of 0 for something the code could not read. The sibling in the same function, ledger None, prints ` — unknown`.
- Fix: when `problem` is set and there are no items, the count word is `unknown` (packet: `(unknown)`). Flip P9.
- This is a spec defect: §3.4 points 4-5 wrote `len(items)`. The Lead corrects it as a continuation edit.

**N3-2 (minor, code quality: work nobody reads).**
- `report_facts.py:4116` still stores `"task_root": str(art)` in `left`.
- Since decision (a) the renderer does not read it. It is an absolute machine path left in the facts dict.
- Fix: drop the key, and its mention in the `case_remarks_left` docstring.

**N3-3 (minor, a docstring that lies).**
- The `case_remark_lines` docstring (`:4154`) says "a link to its file when it has one ... `gate_brief.case_ref`".
- The code prints the bare id.
- Fix: reword the docstring to say the bare id, and why (the report validator forbids `work/`).

**N3-4 (minor, report): the FR pass skips section D.**
- The N3 report covers A, B, C, E, F, G only. PROJECT.md «Как принимается изменение пакета» p.1 asks for one line per section.
- D does apply: FR-59, an unreadable answer is listed as unread, never as acted on; FR-16, the join on the `CR-<case>` id.
- Fix: add the D line to the report.

## Findings, N1

**N1-1 (BLOCKER for acceptance; FR-41, human-questions.md): the second ask says "its file could not be found" about case files that exist.**
- Where: `driver_stage_plan.py:855`, `wanted = [... for r in rows ...]`. `gate_brief.case_files` returns paths only for the ids it is given (`gate_brief.py:1876-1884`).
- `named()` then labels every case outside `wanted` as having no file.
- The earlier-answer paragraph calls `named()` on the cases of the earlier `round` entry (`:884`). Those are often cases the current round no longer rejects.
- Probe on the N1 test rig (`_s4_rig`, files TC-3/5/8 on disk). Earlier `round` entry for TC-3/5/8. Current round rejects TC-3 only. counted 3 of cap 2. Verbatim output:
  `You chose one more round 1 time for these cases; the case designer was then given the reviewer's findings on [TC-3](qa-factory/artifacts/QA-9/work/test-cases/TC-3.md), TC-5 (its file could not be found) and TC-8 (its file could not be found) to rework, and the reviewer looked again.`
- Row Q2 misses this because its earlier cases and current cases are the same.
- Fix:
  - Build `files` over the current cases plus the cases of the newest earlier entry, after `earlier` is computed.
  - Add a Q2 variant row: an earlier case that the current round does not reject, whose file exists, gets a link and no "could not be found".

**N1-2 (should-fix, AR-22 and a data-table sibling): the new store has no reader row.**
- The new store `repair_limit_s4` has no row in `references/collect-loops.json` L4.
- Its two sibling stores do: `:13` `repair_limit`, `:14` `repair_limit_s7`. `collect_stall.py:67` names only those two.
- So collect-time stall measurement never sees an S4 answer.
- The builder wrote "analog queued", but named no node: by brief item 4 that is a finding.
- Fix (one data row, outside N1's owns, so the Lead adds it to the fix round's owns): an `L4` row with key `repair_limit_s4` and values `["round", "go on"]`; add the name to the `collect_stall.py:67` docstring.
- For `docs/SIBLING_MAP.md:630` ("not members ... `repair_limit` / `repair_limit_s7`"): add `repair_limit_s4` there (the Lead's file).
- L7 needs nothing: the S4 Person has kind `repair_limit`.

**N1-3 (should-fix, CODE QUALITY): `s4_review_limit` is 110 lines.**
- `driver_stage_plan.py:785-895`, with two nested closures (`plural`, `named`). The brief's ceiling is about 60.
- Fix: split it into three, which also makes N1-1 a local change:
  - (i) the unknowns: findings, count, roll-call, Q1 word;
  - (ii) the stored answer: `round` / `go on`;
  - (iii) a lead builder, `s4_limit_lead(rows, counted, cap, earlier)`.

**N1-4 (minor, AR-13 / duplication): one store, three reads.**
- The S4 store is read three times without one reader: `s4_round_bought` `:783`, and in `s4_review_limit` the `entry` read (`(... or {}).get(dispatch)`) and the `store` read.
- The "S4 `qa-case-critic` dispatches" filter is also written twice.
- Failure: `state["repair_limit_s4"]` that is not a mapping (a list) gives `AttributeError` in `s4_review_limit`. `s4_round_bought` guards against exactly that.
- Fix: one reader, `s4_limit_store()`, that returns a dict (`{}` for anything that is not a mapping), used by all three.

**N1-5 (minor, duplication; part of the fix is another pile's).**
- The nested `plural` is byte-identical to `question_stop._times` (`question_stop.py:193`). It is a fifth pluralizer, after `report_facts._plural:95`, `story_budget._plural:189` and `task_price._plural:87`.
- The S5 twin's opening has no plural at all: `driver_dispatch.py:3319`, `"... sent the tests back {counted} times; ... {cap} rounds"`. With counted 1 it prints "1 times".
- In this round: keep it as is (the package has no shared plural helper to reuse).
- Residual: a proposed node for the Lead to open in an untaken batch: `one pluralizer for person text (report_facts/story_budget/task_price/question_stop/driver_stage_plan) and the S5/S7 repair-limit opening plurals | узел: <the Lead opens it>`.

**N1-6 (minor, FR-41, conductor text): the Q1 seam text names the wrong round.**
- The text says "the case critic's last round in {path} is marked `<word>`".
- The word comes from `declared_verdict` over the whole file (the first `Verdict:` line), not from the round cut `current_rejected` reads.
- A newest round with no `Verdict:` line therefore reports an older round's word.
- Both branches still reach the conductor seam, so the person is never affected.
- Fix, inside the owns: word it as "the findings file {path} is marked ...", or take the word from the newest round only.

## Lead decisions

- **(a) N3 bare case id: upheld.**
  - It matches the report's own siblings: `_test_head` (`report_facts.py:4035`) and `_window_lines` (`:4058`) name cases bare, through `_shown`.
  - `validate_artifacts.REPORT_ID_SHAPES` (`:1389-1394`) refuses `work/` in a report body, and `case_files` returns the `work/test-cases/` authoring copy (`gate_brief.py:1868-1872`). A link would make the report fail its own check.
  - Report and packet stay on one renderer (FR-10).
- **(b) N1 `budget=None`: upheld.**
  - In production both callers pass the budget: `stage_S4` `:586`, `completion_for` passes `budget or {}`.
  - An unreadable budget means `counted` / `cap` are None, which goes to the step-b seam.
  - Only tests reach step f with None, and there the `repair_older_controller` refusal is the right answer.
  - Reading it as "no budget means the old direct seam" would contradict the card's refusal rows.
- **(c) N1 no cap on the case list: upheld, no cap owed.**
  - `human-questions.md` rule 3 asks for one question for N items of one kind, and it is one question. The form sets no length limit.
  - The S5 twin (`repair_limit_facts` `:3337-3339`) lists every blocking finding, uncut. A cap only at S4 would be a second road (P31).
  - If a cap is ever wanted, it belongs to the shared repair-limit lead for S4, S5 and S7 together, as a node.

## Standing questions

1. **Fit, N3:**
   - §3.4 points 1-6 are implemented.
   - Edges E-N3-1 to E-N3-11 hold: P1-P10 plus the extra rows, re-run green below.
   - E-N3-4: the manifest is read by `json.loads` itself, because `C.load_json` would turn "unreadable" into `{}`. That is the safe direction.
   - The one gap is N3-1.
2. **Fit, N1:**
   - Steps a-g are implemented in the card's order, and the `stage_acceptor` guard stays in front (E-N1-1).
   - Every unknown goes to the conductor seam with `unreadable=True`: K1, U1, E2, G4.
   - E1 is the B4 seam, not unreadable. The tokens are R1-R3, Q5. B1-B3: the bought round starts with no new critic.
   - E-N1-10: AT 300 / BEYOND 301.
   - The critic's Q1 (from the N2 review) is applied as row E2.
   - The one gap is N1-1, in §4.2.
3. **Builder's own choices:** all in the safe direction.
   - N1 dev 3: the no-number line when the count is no int.
   - N1 dev 4: `d.get("id") or key`.
   - N3: an empty `not_applicable` reason prints `not recorded`.
4. **Seams:**
   - `stage_review_exhausted`: only the one `person_closes` line changed, hoisted into `review_pass_finding`, the same idempotency key on both roads.
   - `completion_for`: only the S4 call changed. `render_gate_b`: only the one call.
   - S5/S7 are byte-identical: R4 and R6 pin `--stage S5`, the S5 store and slot, the default roles, and the older-controller text.
   - Known and spec-decided (X-1), not a finding: a story parked at the old seam question meets the new question at its next finish on a readable last round.
5. **Tests:**
   - Both new table functions would catch the defect each node exists for: P2 / P4 / P8 for N3; L1 / Q1 / B1 / R1 for N1.
   - Gap: Q2 lacks the variant that catches N1-1. Its row is part of the fix.
   - Test lines exceed product lines in N1 (+341 vs +218). The reason is named: about 30 card rows. Accepted.
6. **DUPLICATION AND CONSISTENCY:** N1-4 and N1-5.
   - N3 reuses `_shown` / `_overflow` / `GAP_TESTS_MAX` / `SHORTENED`. Grep `def _shown|def _overflow|GAP_TESTS_MAX` found one definition each.
   - N1 reuses `closed_question` / `repair_limit_raise` / `_answer_repair_limit` / `person_pass`. No new `Person(` (the DoD grep in the N1 report; the `Person(` line at `driver_dispatch.py:3390` is the existing one).
7. **CODE QUALITY:** N1-3 (110-line function), N2-free; N3-2 (dead key), N3-3 (lying docstring). No other function over 60 lines in the new code: `case_remarks_left` is 43 lines, `case_remark_lines` 20.
8. **Hygiene:** `selftest --lang` is green in both mechanical layers. The changelog fragments are English.
9. **RATCHETS:**
   - `driver-layers.json` +4 rows. These are homes for new methods (rows 67/68), not upward edges, so not a raise.
   - No census row. No `known_red` row.
   - The `_answer_repair_limit` held_question baseline (`audit_factory.py:1672`, 4) is unchanged: the diff adds no `held_question` in that function.
10. **ARCHITECTURE:**
    - N3 names AR-13, AR-22, AR-27: kept. One merged store; owner named, "the case reviewer" / "the test writer".
    - N1 names AR-13/15/16/17/19/24/25/28: kept, except AR-22 on the S4 store's collect reader (N1-2).
    - AR-21: no handoff changed.
    - AR-16: one renderer; three price lines per token (probe output above).
    - AR-17: the seam is `stage_review_exhausted` / `no_move(call=False)` only.
    - AR-25: three tokens, each with an executor. Free words go to `unread`.
    - AR-27: N3's sub-section sits under its own owner, and never touches `_verdict` (P1 checks the verdict with and without).
11. **JUDGMENT (P27 / P22):**
    - Code carries tokens, counts, presence and the critic's closed cell words. It never judges a remark (N3's `applied` / `not_applicable` join is a closed-token join).
    - A self-contradicting critic output (E1, E2) goes to the conductor, never closed by code.
    - The person gets every option with its three price lines. Code reads only the offered tokens.
    - No census rows, no `blocks_override`, no craft markers.
12. **ONE ROAD:** S4 joins the S5/S7 repair-limit road (F1, the owner's «ок» in the spec's Decisions section). None found otherwise: no language, runner or project branch in either diff (both diffs read in full).

Class completeness (axis 5, stage twins S4/S5/S7):
- Same shape: the store, the slot (dispatch, as at S7), the handler, the waiver, the price data row.
- Named differences:
  - S4 has the FR-7 earlier-answer paragraph.
  - S4 pluralizes, S5 does not (N1-5 residual).
- The collect L4 reader is missing for S4 (N1-2).

## Trail

- Read in full: `docs/tasks/critic-diff-brief.md`; the spec (890 lines); both builder reports.
- Diffs: `git diff eefe80e6^1 eefe80e6 -- ai-packages` (5 files) and `git diff 67b337af^1 67b337af -- ai-packages` (7 files), including both test diffs in full.
- `driver_dispatch.py:3293-3481` (`repair_limit_facts` .. `repair_store_name`).
- `driver_stage_plan.py:592-610`, `:709-739`, `:763-895`.
- `gate_brief.py:1858-1890`.
- `report_facts.py:194-202`, `:2536-2537`, `:4014-4071`, `:4840-4866`.
- `validate_artifacts.py:1389-1419`.
- `critic_rollcall.py:160-164`, `:433-447`.
- `human-questions.md:15-62`.
- `controller.py:2044-2045`.
- `question_stop.py:190-195`.
- `tools/critic_verdict.schema.json`.
- Searches:
  - `repair_limit` over the package excluding tests: found the collect-loops rows `:13-14`, `collect_stall.py:67`, `audit_factory.py:1672`.
  - `def _?plural|def _?(times|...)` (case-insensitive): 7 hits.
  - `OPEN QUESTION` over scripts: 1 hit, in `test_execution_request.py` (positive control). None in `report_facts.py`.
  - `json\.dumps\(facts|dump\(facts|facts\.json|report-facts` (case-insensitive): no writer of `report_facts` facts to disk.
- Control re-run (N3), from the tests directory: `python -B -c "import test_report_facts as T; T.fv16_case_remarks_left(); T.finish('fv16-n3')"` gave `=== fv16-n3: 36/36 ok ===`.
- Probe (N1-1): scratch script `probe/p1.py` calling the test module's own `_s4_rig` / `_s4_limit`. Output quoted under N1-1.
- Not run (batch canon): `test_story_run_refusals.py` (rows `:3584`/`:3585` traced by reading: a `# findings` file with no table leads to the U1 seam; `None`/`"x"` leads to the step-b seam), `test_report_facts.py` (rest), `test_conductor_doors.py` (K15 known, t-806).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "N1-1 driver_stage_plan.py:855/884 s4_review_limit: the second-ask paragraph says '(its file could not be found)' for earlier-round cases whose files exist, because case_files is called with the current rows' ids only (probe output in the review)"
  ],
  "fixes": [
    "N1-1 build files over current cases plus the newest earlier entry's cases; add a Q2 variant row (an earlier case not rejected now gets its link)",
    "N1-2 add an L4 row repair_limit_s4 (values round, go on) to references/collect-loops.json and name it in collect_stall.py:67 (owns extended by the Lead); SIBLING_MAP.md:630 gets the name",
    "N1-3 split s4_review_limit (785-895, 110 lines) into the unknowns, the stored-answer branch and a lead builder",
    "N1-4 one reader of the repair_limit_s4 store returning a dict (a non-mapping store crashes s4_review_limit today), used by s4_round_bought and s4_review_limit",
    "N1-5 keep the local plural this round; the Lead opens a node for one pluralizer plus the S5/S7 repair-limit opening plurals (driver_dispatch.py:3319 prints '1 times')",
    "N1-6 Q1 seam text: say 'the findings file is marked' or read the word from the newest round only",
    "N3-1 report_facts.py:4190/4203 heading count reads 'unknown' when problem is set and items are empty; flip row P9 (spec 3.4 points 4-5 corrected by the Lead)",
    "N3-2 drop the dead task_root key of case_remarks_left (report_facts.py:4116) and its docstring mention",
    "N3-3 reword the case_remark_lines docstring: bare id, not a case_ref link",
    "N3-4 add the missing FR section D line to the N3 builder report"
  ],
  "class_completeness": "Axis 5 (S4/S5/S7 repair-limit twins): same store/slot/handler/waiver/price shape; named differences: the S4 FR-7 paragraph and S4 plurals (S5 lacks them, N1-5 node). Missing sibling: the collect-loops L4 reader row for repair_limit_s4 (N1-2). Report-renderer siblings (_test_head, _window_lines) use the bare id like N3; the ledger-None heading uses 'unknown' (N3-1).",
  "trail": {
    "read": [
      "docs/tasks/critic-diff-brief.md",
      "docs/tasks/specs/20261114-fv1-6-s4-only-spec.md",
      "docs/tasks/specs/reports/20261114-fv16-n3-report.md",
      "docs/tasks/specs/reports/20261114-fv16-n1-report.md",
      "git diff eefe80e6^1 eefe80e6 -- ai-packages",
      "git diff 67b337af^1 67b337af -- ai-packages",
      "ai-packages/qa-factory/scripts/driver_dispatch.py:3293-3481",
      "ai-packages/qa-factory/scripts/driver_stage_plan.py:592-610,709-739,763-895",
      "ai-packages/qa-factory/scripts/gate_brief.py:1858-1890",
      "ai-packages/qa-factory/scripts/report_facts.py:194-202,2536-2537,4014-4071,4840-4866",
      "ai-packages/qa-factory/scripts/validate_artifacts.py:1389-1419",
      "ai-packages/qa-factory/scripts/critic_rollcall.py:160-164,433-447",
      "ai-packages/qa-factory/references/human-questions.md:15-62",
      "ai-packages/qa-factory/references/collect-loops.json (grep)",
      "ai-packages/qa-factory/scripts/question_stop.py:190-195",
      "docs/SIBLING_MAP.md:122,630",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {
        "command": "( cd ai-packages/qa-factory/scripts/tests && python -B -c \"import test_report_facts as T; T.fv16_case_remarks_left(); T.finish('fv16-n3')\" )",
        "result": "=== fv16-n3: 36/36 ok ==="
      },
      {
        "command": "python -B scratchpad/probe/p1.py (test module _s4_rig/_s4_limit; earlier round entry TC-3/5/8, current round rejects TC-3 only, counted 3 of 2)",
        "result": "paragraph prints 'TC-5 (its file could not be found) and TC-8 (its file could not be found)' although both files exist in the rig"
      }
    ]
  }
}
```
