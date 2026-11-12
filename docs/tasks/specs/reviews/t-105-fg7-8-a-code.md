# t-105 FG7-8 part A — critic diff gate (TR2-9 + F1/F2/F3)

Reviewed: uncommitted diff (staged cherry-pick + unstaged edits) in
`C:\QAFactory\forge-repo\.claude\worktrees\agent-abf432fb6dd127353`, `git diff HEAD`, six files.
Paths below are relative to `ai-packages/qa-factory/` in that worktree.

**Verdict: ACCEPT WITH FIXES (fit_with_fixes). Blocking items: 0.** Every DoD item is met. One
pre-existing defect sits in `still_open`. The probe confirms it, and DoD item 6 tells the builder
not to touch it. The fix is three lines, but it means changing DoD 6, and only the Lead can do
that. My recommendation is to fix it in this round: F-1.

## Control runs (verbatim)

1. The new narrow test re-run:
   `python -B .../scripts/tests/test_gate_preflight_question_status.py | tail -5`
   ```
   PASS B-12 a row with no id is checked as it stands
   PASS B-12 matches: the first Q-1 only
   PASS B-12 matches: no view -> nothing

   === gate A: question status from the register: 16/16 ok ===
   ```
   This matches the builder's "16/16 ok" witness.
2. Probe for question (b). It was an inline `python -B -` heredoc that uses the
   `test_gate_preflight.story` rig and writes only temp story folders, which it cleans up. The
   handoff gate refused a scratch file, so it ran inline. Setup: row 1 `Q-1 "removed node"`, row 2
   `Q-1 "moved node"`. Row 1 is either answered in its own fields or driver-owned. The register
   records `not_needed` on row 1's `row_hash`.
   ```
   own-answered first | register Q-1 built from: Where must a removed node appear? | settled: True | duplicates: ['Q-1']
     gate A findings: ['Q-1 cannot be answered as it stands (2 defect']
     still_open listed: []
   driver-owned first | register Q-1 built from: Where must a removed node appear? | settled: True | duplicates: ['Q-1']
     gate A findings: ['Q-1 cannot be answered as it stands (2 defect']
     still_open listed: []
   ```
3. A positive-control grep for the own-answer predicate `("answer", "answered", "resolution")` over
   `scripts/*.py` returned exactly two hits: gate_brief.py:4115 and gate_preflight.py:1760.

## Answers

### a. DoD items and the FR pass

1. **Met.** gate_preflight.py:1741-1763. `settled_rows` is computed with
   `question_register.settled(m)` for each `matches(questions, view)` result. A settled row is
   skipped at :1762. Status is read through `load` + `settled`, the register's readers (AR-13).
   Covered by tests `..._answered_in_the_register_is_not_listed` and
   `..._changed_after_the_answer_is_checked_again`.
2. **Met.** `matches` (question_register.py:379-392) returns None for any row after the first one
   with the same id. Tests for 2 rows → 1 finding and 3 rows → 2 findings are in
   `test_only_the_first_row_of_an_id_takes_the_register_answer`. Probe 2 confirms it on the gate A
   side.
3. **Met as written.** There is one helper and both sites call it: gate_brief.py:4117 and
   gate_preflight.py:1747. The old `by_id`/`seen` copy in `still_open` is gone. See (b): the two
   callers pass it different row sets, so they still answer differently on the same file.
4. **Met.** The test-layers.json row `test_gate_preflight_question_status.py` lists `covers`:
   gate_preflight.py, question_register.py, tests/harness.py, tests/test_gate_preflight.py. These
   are exactly the test's imports (test file lines 14-20). Layer `data_join`, `named_by` AR-13 at
   architecture.md:161 (checked: line 161 is the AR-13 heading).
5. **Met.**
   - Unreadable register: the note path, tested.
   - No id: tested, and `matches` gives None.
   - Answered both ways: the own-answer `continue` at :1759 comes before the register check at
     :1762, so the row is skipped once.
   - Three rows: tested.
6. **Met.** I traced old against new `still_open`. Old: skip non-dict / own-answer / driver_owned;
   `mine = by_id[qid] if qid not in seen`; `seen.add`. New: the same three filters build `listed`,
   then `matches(listed, view)` applies the same `seen` logic over the same surviving rows, with
   the same strip and the same `by_id` key (`_merge` stores the stripped id, question_register.py:262).
   The behaviour is the same. The new code is also more tolerant of a non-dict `view["questions"]`
   entry and of `questions: None`, where the old code would have crashed.

FR pass spot-check:
- "B: no text to a person changed" holds: the finding text at gate_preflight.py:1786-1791 is
  untouched, and the new strings are rehearsal notes.
- "FR-59: an unknown never becomes a pass" holds for gate A (see e). It does not hold for
  `still_open` on the duplicate-id edge (b, F-1), but that defect predates this diff.
- The FR-17 / AR-13 claims hold.

### b. The declared deviation: which reading is right

`question_register.load` (question_register.py:307-323) keeps the first row of an id in **file
order**, over every dict row with a non-blank string id. It does not look at the row's own
`answer` or its `asked_by`. `_merge` fingerprints that row (`row_hash`), and a record's
`changed_since_answer` is measured against that row (:262-272). So the register's answer belongs to
the first row **in the file**.

- **Gate A is right.** It passes all of its dict rows to `matches`. Non-dict and no-id rows
  never take a "first" slot in either `load` or `matches`, so its idea of "first" is exactly
  `load`'s.
- **`still_open` is wrong on this edge.** It drops own-answered and driver-owned rows before
  calling `matches`. The second row of the id then becomes "first", inherits the register question
  built from row 1's bytes, and `QR.settled(mine)` reads row 1's hash.
  - Probe 2: a different question that nobody answered ("moved node") disappears from the
    person's list (`still_open listed: []`). That is an unknown turned into "settled" (FR-41,
    AR-28).
  - When the register is not settled, the card for row 2 carries `shown_hash` = row 1's hash
    (gate_brief.py:4135). An answer the person gives to that card is then stored against row 1's
    bytes.

**The divergence is a defect, and `still_open` is the side that moves.** The old `seen` set had
the same behaviour, so it is not new. Per rule 19 it stays a fix of this round (F-1); if the Lead
keeps DoD 6, it becomes a node instead.

Mitigation: `load` already reports a duplicate id as a problem ("the S2 role must renumber"), and
gate A now names row 2 as a finding. So the duplicate is not silent anywhere; only the person's
list loses the row.

### c. Home and shape of `matches`; other callers

`question_register` is the right home: it is the module that defines "the first row of an id"
(`load`). Returning "the register question or None" and leaving `settled` to the caller is the
right split, because `still_open` needs the whole matched dict.

There is one inaccuracy (item 7, "a name that lies"): the docstring at :382 says "by the id exactly
and case-sensitively", but :388 strips whitespace. The strip is correct and mirrors `load` :316;
the docstring should say "stripped, then exact and case-sensitive". See F-3.

Sibling walk. No SIBLING_MAP axis carries the question-status readers: I grepped the map for
`still_open|question_register|check_open_questions` case-insensitively and got 4 hits, none on
this class. I walked them by an artifact grep `by_id\s*=\s*\{.*(questions|view)` (case-insensitive,
9 hits):

| site | verdict |
|---|---|
| controller.py:9376-9388 `_unchanged_branches` | Builder's claim confirmed. It dedups ids from the words view (`recorded`/`already`) and never matches readiness rows to the register. Not applicable. |
| planning_contract.py:648-655 | Confirmed. `by_id` is built over `load()` output, which is already deduplicated; `seen` dedups output ids. Not applicable. |
| planning_contract.py:3007, :3061; driver_dispatch.py:1966; traceability.py:322, :460 | All key `load()` output, which is already the first-row view. Not applicable. |
| claim_projector.py:610 (builder did not examine it) | Raw readiness rows, `{q["id"]: q}`, so the last row wins, with no strip. It is a claim-link lookup (`C.claim_link_index` / `claim_row_errors`) over rows the projector itself just numbered (`top+1`, :552-562). It never reads a question's register status, so it is not this class. Note only: first-wins vs last-wins over raw rows is an untested mirror; queue it if the Lead wants. |
| question_register.py:466-482 `statuses_for` (same module) | A different rule on duplicates: every row of an id gets the record, fingerprinted from that row. A later row with different bytes therefore gets `changed_since_answer: True` and is not settled. That is the safe direction, so not a defect, but it is a second reading of "which row owns an answer". Not applicable now. Queue a note if the publish path can ever see duplicate ids. |

### d. Duplication and code quality (brief items 6-7); note text against FR-1/FR-41

**DUPLICATION AND CONSISTENCY:** one finding, F-2. The own-answer predicate
`any(str(row.get(k) or "").strip() for k in ("answer","answered","resolution"))` is written twice:
gate_preflight.py:1759-1760 and gate_brief.py:4115. Grep result 3 shows these are the only two
copies. This is the same "is this question answered" fact that F3 set out to keep in one place, and
the diff touches both lines. Nothing else is duplicated: the old `by_id`/`seen` copy in `still_open`
was removed.

**CODE QUALITY:**
- No new function is over 60 lines. `check_open_questions` was already long; the diff adds 21
  lines to it, at no deeper nesting.
- No dead branches.
- One annotation lies: the `matches` docstring, F-3.
- The exception path can lie, F-4.
- The note silently truncates `problems` to 2 entries without saying so, F-5.

**Note text:**
- "the question register was read with problems (...), so a question it does not show as settled
  is checked as it stands" says what happened, what it caused, and the safe default. FR-1 and FR-41
  are met.
- "could not be read from the question register (OSError), so every question is checked as it
  stands" is also fine, except in the corner case of F-4.

### e. Can the `settled_rows` default or the exception path turn an unknown into a pass (AR-28)?

No.
- The default is all `False`. If `load` raises, nothing is skipped by the register and every row
  goes through `question_errors`.
- A `view` with no questions, an id the register does not hold, a later duplicate, a changed row
  (`_holds`) and an unknown status (set aside in `_answers` :194) all yield `settled` False.
- If gate A reads the legacy flat path (`contract.artifact` falls back to `<artifacts>/<name>`)
  while `load` reads `work/`, the register is empty, which is again the safe direction.

The only flaw is in the text, not the verdict (F-4). If an exception were raised after line 1747
had already assigned real values (in the note-building lines 1748-1753), the real `settled_rows`
would stand, but the note would claim "every question is checked as it stands". This is
practically unreachable today, because `skipped` and `problems` are built by `load` itself.

## Findings

Blocking: none.

Non-blocking:

- **F-1 (fix this round; the Lead decides because it changes DoD 6). Fixed by this probe: `still_open` hides an unanswered duplicate-id row behind the register answer given on an earlier row.**
  - Where: gate_brief.py:4113-4117.
  - Fix: match first, filter second:
    `rows_d = [r for r in rows if isinstance(r, dict)]`; then
    `for row, mine in zip(rows_d, QR.matches(rows_d, view))`. Inside the loop, `continue` on own
    answer or `QR.driver_owned(row)` as before.
  - Test: add a row to `test_gate_brief_and_retro.py`, or to the new file, with probe 2's input:
    row 2 must be listed with `status` open, not dropped.
  - Then the two readers agree, and DoD 3 holds in effect, not only in letter.
  - Fallback if the Lead keeps DoD 6: open a node in the forge pile (owner: the Lead of the forge
    pile) carrying probe 2 as its red case.
- **F-2 (fix before merge, cheap).** Move the own-answer predicate into `question_register`, for
  example `has_own_answer(row)`, and call it at gate_preflight.py:1759 and gate_brief.py:4115.
- **F-3 (fix before merge).** question_register.py:382: change the docstring to "by the id stripped
  of surrounding whitespace, then exactly and case-sensitively (as `load` keys it)".
- **F-4 (queue or fix).** gate_preflight.py:1747: compute into a local (`got = [...]`) and assign
  `settled_rows = got` as the last statement of the `try`, after the note. Otherwise the except
  note can contradict what actually happened.
- **F-5 (queue or fix).** gate_preflight.py:1751 uses `[:2]`. Append `"and N more"` when
  `len(problems) > 2`, so the truncation is stated (FR-41: nothing dropped silently).

## Verdict lines

- DUPLICATION AND CONSISTENCY: one finding (F-2); grep `("answer", "answered", "resolution")` over
  `scripts/*.py` gives 2 hits. The old `still_open` copy of the first-row rule was removed.
- CODE QUALITY: F-3 (an annotation that lies), F-4, F-5. No oversize new function and no dead
  code.
- ONE ROAD (item 12): the diff excludes no language, project or case. The only divergence is
  between the two callers of one helper (F-1), and it is a fix of this round, not a hand-off line.
- JUDGMENT (item 11): none. The change is a data join (register status by id) and adds no new
  refusal on a role's content.
- The acceptance decision belongs to the coordinator (the Lead tier); this verdict is an input to
  it.

Needed beyond the manifest: question_register.py `load` / `_merge` / `_answers` / `statuses_for`,
contract.py `artifact`, claim_projector.py:540-630, controller.py:9376-9416,
planning_contract.py:636-657, traceability.py:310-334 and :450-462, SIBLING_MAP.md grep.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "No SIBLING_MAP axis carries question-status readers (map grep: 4 hits, none on this class). Artifact walk over 9 by_id sites: controller._unchanged_branches, planning_contract:648/3007/3061, driver_dispatch:1966 and traceability:322/460 key load() output, so not applicable. claim_projector:610 is a claim-link lookup, not register status. statuses_for uses a per-row hash, which is the safe direction. Residual in the class: still_open pre-filters before matches and hides an unanswered duplicate-id row (F-1, probe 2), a fix of this round or a node owned by the Lead of the forge pile.",
  "trail": {
    "read": [
      "git diff HEAD of worktree agent-abf432fb6dd127353 (6 files)",
      "docs/tasks/specs/reports/t-105-fg7-8-a.md",
      "scripts/question_register.py:120-494",
      "scripts/gate_preflight.py:1700-1810",
      "scripts/gate_brief.py:4095-4157",
      "scripts/claim_projector.py:540-630",
      "scripts/controller.py:9376-9416",
      "scripts/planning_contract.py:636-657",
      "scripts/traceability.py:310-334,450-462",
      "scripts/contract.py:2791-2803",
      "scripts/tests/test-layers.json rows test_gate_preflight.py and the new row",
      "design/architecture.md:155-165",
      "docs/tasks/critic-diff-brief.md items 6,7,11,12",
      "plans/piles/forge/findings/20261111-ostatki-sliyaniya-eksperimenta-v-main.md FG7-8",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {
        "command": "python -B scripts/tests/test_gate_preflight_question_status.py",
        "result": "=== gate A: question status from the register: 16/16 ok ==="
      },
      {
        "command": "inline probe: rows [Q-1 own-answered or driver-owned, Q-1 different text], register not_needed on row 1 hash; gate A vs still_open",
        "result": "gate A: 1 finding for row 2; still_open listed: [] in both variants (row 2 hidden)"
      },
      {
        "command": "grep the own-answer tuple over scripts/*.py",
        "result": "2 hits: gate_brief.py:4115, gate_preflight.py:1760"
      }
    ]
  },
  "fixes": [
    "F-1 gate_brief.py:4113-4117: call QR.matches over all dict rows, then apply the own-answer and driver_owned filters inside the loop; add the probe-2 case as a test. Needs the Lead to change DoD 6; otherwise open a forge node owned by the Lead of the forge pile",
    "F-2 move the own-answer predicate into question_register (has_own_answer) and call it at gate_preflight.py:1759 and gate_brief.py:4115",
    "F-3 question_register.py:382: the docstring should say the id is stripped before the exact, case-sensitive match",
    "F-4 gate_preflight.py:1747: assign settled_rows as the last statement of the try so the except note cannot contradict it",
    "F-5 gate_preflight.py:1751: state the truncation of problems ([:2]) with 'and N more'"
  ]
}
```
