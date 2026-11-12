# t-161 (journal t-163) — critic re-review of the batch onboarding-forge/2 fix rounds after t-147

One pass for the topic (R13-g). Inputs: the verdict `docs/tasks/specs/reviews/t-147-of2-batch-critic.md` and the four fix commits,
read in full with `git show`: of-hot 0013879, of-small c26ac17, of-handoff d80a3e3, of-tests 4710bc5. Out of scope (non-goals):
items closed in t-147 and new scope. The journal id is t-163 (coordinator's correction); the report path stays as dispatched.

## Verdict per stream

- **hot (H1-H5): fix round, one blocking finding (H1-r, a history gate).**
  - H2, H3, H4 and H5 are closed.
  - H1 is closed in substance: the pins run in a canon file, and the quarantined file is back to origin/main bytes.
  - But the earlier commit 336d909 is still on the branch, and it edits a quarantined file with no door. The `quarantine-edit:` line
    in 0013879 covers 0013879 only. `tools/test_quarantine.py check` on the worktree gives 1 violation, rc=1.
- **small (S1, S3): accept.**
  - S1 and S3 are closed. The builder's part of S2 (narrowing the claim) is closed too.
  - The S2 carrier is coordinator work and still open (see S2). It is not counted against the builder.
- **handoff (HO1, HO2): accept.** Both are closed.
- **tests (T1): accept.** T1 is closed.
- **Batch: NEEDS WORK until H1-r is closed.** The fix is one commit-message line, or a squash. Accepting the batch is the
  coordinator's call (rule 6).

## Per finding

### H1: closed in substance; new blocking residual H1-r

What I verified:
- `git diff origin/main 0013879 -- .../test_answer_rework_pairs.py` is empty, so the file's bytes equal origin/main.
- `d17_one_carrier_each` in `test_gate_words_road.py` is the old D1/D2 body, adapted to that file's names `QR`, `CTL` and
  `SCRIPTS`. `main()` calls it.
- `test_gate_words_road.py` is a `keep` row in test-layers.json (layer data_join).

**H1-r (BLOCKING): the branch history still fails the quarantine history check.**
- How the check works: `tools/test_quarantine.py check_history` (lines 1690-1694 and 1728-1731) walks EVERY commit. It flags a
  commit that touches a quarantined file without `quarantine-edit: <name>` in that commit's own message. A LATER commit that
  carries `quarantine-accept: <sha> -- <reason>` (line 1520) clears the flag.
- `git show --name-only 336d909` lists `scripts/tests/test_answer_rework_pairs.py`.
- `git log --format=%B origin/main..0013879 | grep "^quarantine-"` finds exactly one line: the `quarantine-edit:` of 0013879. There
  is no `quarantine-accept: 336d909`.
- The live run confirms it: `check` reports 336d909b and exits rc=1 (verbatim output below). A merge-commit integration would carry
  this violation into main, where forge-check runs `check`.
- Fix: put this line in a later commit message on the branch, for example the next fix commit:
  `quarantine-accept: 336d909 -- DC1-27 pins edit, reverted and moved to a keep file in 0013879 (t-147 H1)`. Squashing the stream
  also works. This is the tool's own door: its refusal names it.
- Non-blocking note:
  - The keep row's `why` reads "held by import: test_question_branches.py imports it; leaves the canon when the import is cut
    (TD-15.8)". The pins therefore stay in the canon only while that import stays.
  - Whoever cuts the import (TD-15.8) has to carry d17 into another keep file. One line in the TD-15.8 node covers it.

### H2: closed
- The `refusal_registry.py` row SG-resume-stopped now names:
  - the incomplete branch and `Controller.incomplete_words`;
  - the `--operation recover` door;
  - the `retry_packets` condition;
  - ALLOW for a story-budget stop and for a later record.
- `unpassable_because` is extended.
- K1-9 pins all three substrings.

### H3: closed
- Trace: `_resume_status_problems` calls `_incomplete_problem(d)`, which picks one of three doors:
  - (a) `retry_packets()` lists the id: `incomplete_words` (the recover door).
  - (b) `reason == BUDGET_EXHAUSTED`: `_budget_words`. `_retry_packet` returns None for this reason (controller.py:8802), so (a) is
    never true for it, and the order of the checks is safe.
  - (c) anything else: a `next` sentence.
- `retry_packets(state=None)` reads `self.state()`. That is the same reader `recover` prints and the guard asks
  (`ctl.retry_packets(ctl.state())`), so the two sides agree.
- K1-11 covers all three cases. It includes a control that `retry_packets` holds no packet for the budget case.
- Re-run: 123/123.

### H4: closed
- `_one_open_record` is the one head both targets read.
  - I traced it against both old heads, and it is equivalent:
    - the statuses are `RESUMABLE_STOPPED` / `(INCOMPLETE,)`;
    - the non-dict guard is the same;
    - the exactly-one test against `_SETTLED_BESIDE_STOP + statuses` is the same.
- `_recover_words` is the one spelling, used by `incomplete_words`, `_resume_stop_problems` and the no-stop sentence of
  `build_resume_request`.
- `_budget_words` is shared.
- The K1-11 source pins are present.
- Siblings (rule 5). The builder reported other recover sentences in controller.py, and I read each one:
  - 4956: a different meaning (it "refreshes" a stale revision). Not applicable.
  - 9632 (`apply_door`, "dispatch"): a hint inside a refusal, with a different shape. Not applicable to one-spelling.
  - 5701 and 5768-5775: a semantic sibling of H3. See N1 under "New observations".
- The commit's AR-15 claim is scoped to the three sites it names, and for that scope it is true.

### H5: closed
- The builder's report lists 30 witness-for files, all rc=0, including `test_gate_words_road` 225/225 (+6 D1/D2).
- The stated deviation is true and explained.
  - `scenario_walk --witness-for` does not name `test_gate_words_road` for the three owned paths. The file is reached through its own
    keep row instead.
  - This matches the keep row's `covers` list: harness.py, test_gate_decision_manual_pass.py and test_gate_b_orders.py.

### S1: closed
- Both readers now use `naive="utc"`.
- No `naive="local"` call is left in the package scripts: a grep over scripts/*.py outside tests finds none. The positive control is
  the same grep for `naive=`, which finds all 5 call sites.
- The `NAIVE_READINGS` comment is corrected.
- The new test feeds each reader one row each of: zone-less, Z, +02:00, empty, None, garbage and a number.
- The negative control (naive="local" gives 421/423) shows the pin kills the old reading on a non-UTC machine.
- Note (non-blocking):
  - On a runner whose TZ is UTC, a zone-less row reads the same under "local" and "utc". There the pin cannot tell the two readings
    apart, so it only works on a non-UTC machine.
  - To make it portable: set TZ for that one case, or assert `epoch_of(..., naive="local") != utc` as a precondition and skip when
    the two are equal.
- The optional route from t-147 (`driver_journal.parse_ts` for driver-runs) is not done. It belongs to S2.

### S2: builder part closed; carrier OPEN (coordinator)
- The `architecture: AR-13` line is narrowed to the two liveness readers. It names `driver_journal.parse_ts`,
  `cost_capture.parse_ts` and `codex_usage.stamp` as not claimed and queued.
- Carrier check: there is no time-readers finding yet.
  - A grep of `plans/piles/*/findings` for `parse_ts` finds nothing.
  - Control: the same grep for `epoch_of` finds 7 findings files.
  - `docs/SIBLING_MAP.md` has no time-readers axis.
  - `git status plans/ docs/SIBLING_MAP.md` shows no such new file.
- Per the dispatch, writing the carrier is the coordinator's and the Lead's work, so it is not counted against the builder.
- The class does not count as queued (rule 5) until the carrier exists. The census list and the axis proposal are in t-147 S2.

### S3: closed
- The project fact is replaced by a generic rule: a flag sent in the query string does not go in the JSON body.
- role-load `process_ratchet_tokens` for qa-runner goes 14433 -> 14432. It only shrinks (AR-20).
- The builder reports test_audit_rules 333/333.

### HO1: closed

Trace: `_near` calls `_near_row(near, held=<the person's indexes>, _template_nodes(contract), doc)`.
- `_concrete_head(generic, nodes, held)` keeps the person's index, whether or not that row holds the field: `_concrete`
  (line 2122) takes `held[k]` unconditionally.
- That is why `_held_in` then asks whether the form or the template holds a line at that path.
- When neither holds it, `_near_row` falls back to `_concrete_head` without `held`, which gives the first row that holds the field.
- When no row holds the field, the result is "" (no hint).

What this gives on the probes from t-147:
- `inputs_read.rows` on s8 is now offered as `inputs_read[1].rows`, which applies 1.
- `inputs_read[0].row` is offered as `inputs_read[1].rows`.
- A homogeneous list keeps the person's row (`scope[0].reason`).
- With no template (`nodes is None`) the result is "", so there is no hint. That is the safe direction, and it is documented.
- A trailing `[]` (a list of values) goes through `_concrete_head`, so the list is still written whole.

Nested lists with a partial `held`:
- The inner index is the minimum over all outer rows, so it can miss the person's row.
- Then `_held_in` fails, and the fallback is the first row that holds the whole path.
- That path is writable, so this is the safe direction.

K-HO1 pins 3 typed forms plus controls. Re-run: 6470/6470.

### HO2: closed
- `_writable_lines` now also drops a pair when `found or not count`.
- K-HO2 pins the result, in order:
  - dropped: `inputs_read[0].rows`, `no_such.field`;
  - kept: `inputs_read[1].rows`, `header.window`.
- The error direction is unchanged: an exception keeps every line.

### T1: closed
- `scaffold.py:369` and `test_brief_pack.py:3201` now write through `harness.write_register(..., head="")`.
- Both files import `harness`: scaffold.py at line 22, test_brief_pack through its existing import.
- `write_register` calls `mkdir(parents=True, exist_ok=True)`. So the earlier `(tmp/"work").mkdir()` in test_brief_pack does not
  collide with it.
- The only byte change is CRLF -> LF on Windows, which is the one writer's contract. The builder's scratch run shows the bytes equal
  the oracle for head="".

## New observations (outside the fix diffs; for the coordinator to queue; not blocking this round)

**N1: the H3 defect (naming `recover` when it prints no packet) also stands at two older controller sites.**
- (a) `controller.py:5767-5775`, `accept` of a STOPPED dispatch:
  - The refusal says "`--operation recover` prints the ready packet", with no condition.
  - `retry_packets` skips a `BUDGET_EXHAUSTED` stop (8802) and a dispatch with a later record of the same stage and role (8576-8578).
    For those dispatches the named door is dead (FR-2).
- (b) `controller.py:5701`, the relaunch_of refusal:
  - It says "to resume a stopped role use its retry packet (`--operation recover` prints it)", with the same gap.
- Surface: the controller's refusals of a stopped dispatch.
- Fix shape: route both refusals through the door choice of `_incomplete_problem`, generalised to the stopped statuses:
  - `retry_packets` lists the dispatch: name recover;
  - a story-budget stop: `_budget_words`;
  - anything else: `next`.
- The builder reported these sites but did not queue them. They need a node with an owner (rule 5); queuing it is the coordinator's
  move.

## Standing questions (re-review scope)

- **DUPLICATION AND CONSISTENCY:**
  - Closed: H4 (one head, one recover spelling across the three named sites, one budget sentence) and T1 (one register writer).
  - Remaining: the recover sentences at 5701, 5771 and 9632 are worded differently from `_recover_words`. At 5701 and 5771 they mean
    the same thing, and both carry the N1 defect.
  - Search: "operation recover" in controller.py, 8 hits, all read.
  - Nothing new in the handoff and small diffs. `_held_in` and `_near_row` reuse `_concrete_head` rather than copying it.
    Search: `_concrete` in handoff_check.py, both definitions and their callers read.
- **CODE QUALITY:**
  - Function sizes are small: `_incomplete_problem` 12 lines, `_one_open_record` 12, `_near_row` 9.
  - One cosmetic point: the S1 test comment says "a mixed file", but the rows are written one per file.
  - None found beyond that in the four diffs, read in full.
- **ONE ROAD (item 12):** none found. None of the four diffs branches on a language, project or runner, and S3 removed the one
  project fact.
- **AR claims:**
  - 0013879:
    - AR-13 true: the pins are in a canon file.
    - AR-15 true for the named sites.
    - AR-18 true.
    - AR-25 true on both sides for an incomplete dispatch. The N1 sites are outside its claim.
  - c26ac17: AR-13 (narrowed), AR-3 and AR-20 are true.
  - d80a3e3: AR-9 true.
  - 4710bc5: `architecture: none` is fair (test support only).

## Trail

- Read:
  - the t-147 verdict;
  - `git show` of 0013879, c26ac17, d80a3e3 and 4710bc5, in full;
  - of-hot controller.py 5690-5779, 6205-6262, 8560-8590, 8780-8804 and 9601-9636;
  - tools/test_quarantine.py 1515-1522, 1600-1733 and `cmd_check`;
  - the test-layers.json row of test_gate_words_road.py;
  - of-handoff handoff_check.py 2097-2136;
  - of-tests harness.py `write_register` (300-308) and the scaffold.py imports.
- Greps:
  - `naive=` in of-small scripts: no `local` call left; control: 5 sites found.
  - `parse_ts` and `epoch_of` in plans/piles findings: 0 and 7.
  - `operation recover` in controller.py: 8 hits.
  - `git log origin/main..0013879 | grep ^quarantine-`: 1 line, the edit door of 0013879.
  - `git show --name-only 336d909`: it touches the quarantined file.
- Re-runs:
  - of-hot `test_resume_stopped.py`: 123/123 ok.
  - of-handoff `test_handoff_values_refusal.py`: 6470/6470 ok.
  - the live quarantine check, `python -B tools/test_quarantine.py check --root .claude/worktrees/of-hot`. Verbatim output:

    quarantine check: 336d909b: quarantined file test_answer_rework_pairs.py was changed, deleted or renamed -- expected a line 'quarantine-edit: test_answer_rework_pairs.py -- <reason>' in this commit message; or or a later commit line "quarantine-accept: <sha> -- <reason>"
    quarantine check: 1 violation(s)
    rc=1

- What the check shows:
  - Exactly one violation. 0013879 itself passes, and the rest of the history is clean.
  - Side note: the refusal text says "or or". It is cosmetic and comes from `_ACCEPT`, which starts with "or".

## Verdict line

- **hot: NEEDS WORK, 1 blocking finding (H1-r).**
- **small, handoff, tests: ACCEPT.**
- Coordinator moves: the S2 carrier (a time-readers finding plus the axis proposal) and N1 (a node for the recover-door siblings).
- Deciding acceptance belongs to the coordinator of the proper tier.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "H1-r hot: commit 336d909 on the branch edits quarantined test_answer_rework_pairs.py with no door; the quarantine-edit line of 0013879 covers only itself; tools/test_quarantine.py check --root of-hot gives 1 violation, rc=1 -- add a later commit line quarantine-accept: 336d909 -- <reason>, or squash the stream"
  ],
  "fixes": [
    "H1-r hot: a later commit message on the pile branch carries 'quarantine-accept: 336d909 -- DC1-27 pins edit reverted, moved to keep test_gate_words_road.py (t-147 H1)'; re-run tools/test_quarantine.py check --root of-hot, expect 0 violations (BLOCKS)",
    "S1 note (optional): the zone-less pin cannot kill naive=local on a TZ=UTC runner; set TZ for that case, or assert local != utc as a precondition",
    "S2 coordinator: write the time-readers finding (driver_journal.parse_ts, cost_capture.parse_ts, codex_usage.stamp, about 39 files) with a batch row, and the SIBLING_MAP axis proposal to Lead",
    "N1 coordinator: queue a node -- controller.py 5767-5775 (accept of a stopped dispatch) and 5701 (relaunch_of refusal) name recover unconditionally; the door is dead for BUDGET_EXHAUSTED or a later record; route both through the door choice of _incomplete_problem",
    "H1 note: the TD-15.8 node carries d17_one_carrier_each into a keep file when the test_question_branches import is cut"
  ],
  "class_completeness": "H3 class (recover named when it prints no packet): fixed for the incomplete resume on both sides; two pre-existing controller siblings (5701, 5767-5775) were reported by the builder but not queued (N1). H4 one-spelling: true for the three named sites; 4956 has a different meaning, 9632 a different shape. CX2-12 time readers: builder claim narrowed; the carrier is still absent (no finding with parse_ts, no SIBLING_MAP axis) -- coordinator. HF8-28 _near: closed, including the no-template and no-row directions. OH3-25: the last two inline writers go through write_register.",
  "trail": {
    "read": [
      "docs/tasks/specs/reviews/t-147-of2-batch-critic.md",
      "git show 0013879 (of-hot), c26ac17 (of-small), d80a3e3 (of-handoff), 4710bc5 (of-tests) in full",
      "of-hot controller.py 5690-5779, 6205-6262, 8560-8590, 8780-8804, 9601-9636; test-layers.json row test_gate_words_road.py",
      "tools/test_quarantine.py 1515-1522, 1600-1733, cmd_check",
      "of-handoff handoff_check.py 2097-2136",
      "of-tests harness.py write_register 300-308; scaffold.py imports",
      "greps: naive= in of-small scripts; parse_ts and epoch_of in plans/piles findings; operation recover in controller.py; git log origin/main..0013879 quarantine lines; git show --name-only 336d909"
    ],
    "reruns": [
      {"command": "of-hot: python -B scripts/tests/test_resume_stopped.py", "result": "123/123 ok"},
      {"command": "of-handoff: python -B scripts/tests/test_handoff_values_refusal.py", "result": "6470/6470 ok"},
      {"command": "python -B tools/test_quarantine.py check --root .claude/worktrees/of-hot", "result": "1 violation (336d909b, quarantine-edit missing), rc=1"}
    ]
  }
}
```
