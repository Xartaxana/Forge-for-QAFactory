# t-711 — code critic, topic FV1-30b tail (N4 `awaits_answer`, N5 `_terminal_runs` aliases)

Spec/DoD: `docs/tasks/specs/20261114-fv1-30b-n4-n5-cards-spec.md` (read whole, including the Lead's fork decisions). Diffs: N4 `wip/fv130b-n4` a3f9a49..b483ac8;
N5 `wip/fv130b-n5` d5d602d..5c90164. Brief: `docs/tasks/critic-diff-brief.md`.

## Verdict

- **N4 — fit_with_fixes** (0 blocking, 2 fix-before-merge, 1 queue).
- **N5 — unfit** (1 BLOCKING: an ambiguous spelling still credits one instance's run to another, which breaks N5-E5 and the commit's own AR-28 line).
- Topic JSON verdict: `blocker` (because of N5). Accepting is the Lead's decision, not mine.

## Blocking findings

**B1 (N5, blocks). `window_record.py:490-493`: the alias tuple stored as the VALUE of `owner` still holds the ambiguous spellings.**
The card's rule (N5-E5) is "that spelling maps to nobody; each entry's own other spellings still map". The code takes ambiguous spellings out of
the KEYS of `owner` only. `aliases_of[canonical]` is the entry's full `instance_id_aliases` list, so a run spelled with an UNambiguous alias of entry B
writes B's run under every alias of B, the ambiguous ones included (`:506`). Reproduced on the N5 worktree with a read-only probe (temp dirs, verbatim output):
```
  aliases test_x -> ['test_x', 'TC-5::test_x']
  aliases TC-9::test_x -> ['TC-9::test_x', 'test_x']
P2 bare == other canonical, run TC-9:: {'TC-9::test_x': ('TC-9::test_x', 'failed'), 'test_x': ('TC-9::test_x', 'failed')}
P1 shared bare, run TC-1:: {'TC-1::test_x[eu]': ('TC-1::test_x[eu]', 'failed'), 'test_x[eu]': ('TC-1::test_x[eu]', 'failed')}
CTRL w4 {'test_x[eu]': ('test_x[eu]', 'passed')}
```
- P2: entry A (canonical `test_x`, TC-5) never ran. After N5, the key `test_x` holds TC-9's FAILED run. `build` then gives A's window item B's outcome.
  The exclusions `i not in runs` (`window_record.py` ~`:1422`, `:1438`) take A out of `pending` and out of the handed list. `_red_source`/`red_by_requirement`
  can mark A red with B's row. This is exactly the forbidden error of §4.3 ("credit a run of instance X to instance Y").
- P1 (the card's own w4 world, with the run spelled `TC-1::…` instead of bare): the bare key gets TC-1's run. Entry TC-2 has no run of its own. Its first-alias
  walks land on the bare key: `proof_level.staleness` `proof_level.py:2018` and `acceptance._red_source.failed` `acceptance.py:876-881`. So TC-1's run is credited to TC-2.
- The precheck still says "no row" for A (`s5_precheck.check_run_mapping` joins against raw row ids). So N5 also opens a P31 divergence in the reverse direction.
- Origin: the code is the card's §4.1 item 1, copied verbatim. This is a spec defect (dispatcher side, a calibration case), but the node does not hold its own invariant.
  Row w4 misses it because its run is spelled with the ambiguous bare name itself.
- The report claims "ambiguity dropped: w3, w4 … none moves to its forbidden side", and commit 5c90164 says "AR-28 -- an ambiguous alias … credits no run".
  The probe above refutes both claims (critic rule 12).
- **Fix (one line + two rows):** `owner = {name: tuple(a for a in aliases_of[next(iter(keys))] if len(spellings[a]) == 1) for name, keys in spellings.items() if len(keys) == 1}`.
  Add rows to `ALIAS_ROWS` (`test_window_record.py:1203` area):
  - "w4b shared bare, run spelled `TC-1::test_x[eu]`" → keys only `TC-1::test_x[eu]`;
  - "w4c bare equals another canonical (`test_x`/TC-5 and `TC-9::test_x`), run `TC-9::test_x`" → keys only `TC-9::test_x`.
  - The docstring sentence stays true after the fix.
  - Fix round in a fresh builder; the witness is the direct call of `a_terminal_run_is_the_latest_by_the_clock` (as in the N5 report) plus the rows.

## Non-blocking findings

**F2 (N4, fix before merge). Door B makes the new texts false (FR-1, FR-10).**
- An open-oracle finding with no registered question (door B, `s5_precheck.py:1668-1671`) carries the same tag and so the same cause `awaits_answer` (Lead N4-F3 (a)).
- The footer clause (`s5_precheck.py:4807-4809`) still says "its own line names the author's repair and the question the person settles by answering it".
- The gate line (`story_step.py:2052-2056`) says "Each line above names the question and the command with which the conductor records the person's answer".
- For door B the finding's own line says "the case names no question the register holds", so the same packet contradicts itself. The text is the card's, verbatim.
- Fix (the Lead edits the card wording, the builder applies it):
  - footer: "… its own line names the author's repair and either the question the person settles by answering it or the road back to S4";
  - gate line: "Each line above names either the question and the command … or sends the case back to S4; until …".
  - The g1 pin "the conductor records the person's answer" can stay.

**F3 (N4, fix before merge, quality). `test_then_remainder.py:879-881`: two small defects in the k22 table.**
- The `passable` column is a dead column: it is asserted for 3 of the 9 rows only (`if label.startswith(("k22-1", "k22-5 no-b", "k22-5 env"))`). The other 6 values are never read.
- `for label in ("k22-5",):` is a loop of one iteration.
- Fix: assert `_passable` for every row (all 9 values in the table are correct: k22-7 → False because `_passable` lowers, k22-8 → True), and replace the loop with one statement.

**F4 (N4, queue). An upper-case waiting tag is star-passable at the gate (the card accepts this; it is not reachable today).**
- After `.lower()`, `THEN-REMAINDER-UNRECORDED-1` gets `""` (k22-7, card item 1 note).
- `exit_gate.word_class` (`exit_gate.py:1815`) compares `_finding_tag_of(record).startswith(WAITING_FINDING_TAGS)` without lowering, so such a record would become class `star` and `*` would pass it.
- The only producer spells the lowercase constant (`s5_precheck.py:1631`), so the path is not reachable. The `then handed` footer test `_finding_tag(f).startswith(THEN_REMAINDER_TAG)` has the same shape.
- Proposed line: `exit_gate.word_class and s5_precheck.report compare the waiting tag case-sensitively while refusal_cause/_passable lower it | узел: <new node, pile of FV1-30, owner Lead>`.

**F5 (N5, queue; duplication, AR-13, SIBLING_MAP axis 24). This is a third "which instance owns this run row" join.**
- Axis 24 says the join is answered ONCE, by `case_stamp.run_row_for` (`case_stamp.py:293-312`). Its rule is "a `::` tail two tests share joins nothing" (`_is_neighbour`).
- `acceptance.tests_by_alias` (`acceptance.py:568-576`) is a second alias→entry map. It breaks ties with "first row wins" and does not drop ambiguous spellings.
- N5 builds a third map, with "ambiguous drops" (correct after B1, and the safer direction), inside `_terminal_runs`. So three readers give three answers to "who owns `test_x[eu]`".
- The card chose `instance_id_aliases`, with the Lead's N5-F1 (a). The convergence is not queued in the spec. Neither report walked axis 24: the N5 report walked axes 17, 26 and 34.
- Proposed node: `one owner-of-a-spelling map (contract-level, ambiguity dropped) read by window_record._terminal_runs, acceptance.tests_by_alias and case_stamp._join; axis 24 names it | узел: <new node, owner Lead>`.

**F6 (N4, trivial).** `test_detector_verdict.py:487` (`:646` on tbw-t2): the label "every refusal line has family or predating" is stale, but the check reads `DV.REFUSAL_CAUSES` and passes.
The builder reported it. It belongs to tbw T2's function: fold it into whichever of N4/T2 merges later.

## Questions

**1) Fit to the DoD per node.**
- N4: items 1-6 are implemented as written. Branch order N4-E5 is kept (`refusal_cause`: waiting → open-oracle → `_passable` → predating). The constant is imported, never retyped.
- N4 rows: k22-1..8, g1..g6, the `test_exit_gate_scope` cause tuple and `tag_cases` d1/d2 are present. The four R6 pins are rewritten.
- N4 error direction (§3.2): `bool(refusal_cause)` is unchanged except the k22-7 spelling the card accepted (F4).
- N4 edges: N4-E1 (unknown cause → unreadable + defect, the sentence built from the tuple), E2 (g4), E3 (g5, k22-5), E4 (g2/g3), E7 (one commit) and E9 (text: see F2) all hold.
- N4 known Lead decisions: the footer reword "no word passes it" (b483ac8) and the open-form `judgment:` line are checked, not re-opened.
- N5: items 1-4 are implemented verbatim, and rows w1-w7 are present.
- N5-E5 fails (B1). E1 (w3), E2 (w5, w7), E3 (w2 both clock orders), E6 (contract) and E7 (w6) hold.

**2) N4: cause, reader, door.**
- AR-13/AR-18 are kept. There is one producer (`refusal_cause`) and one line reader (`detector_verdict.parse`/`_tag_lines`). `_gate_refusal` reads the parsed `Record.refused` field and compares it with `DV.AWAITS_ANSWER`.
- `exit_gate.word_class` is unchanged (any truthy cause → `refused`). `test_exit_gate_scope` pins `*` and `x:t` against `awaits_answer`.
- AR-9/FR-2: the door names a road the author can take (bind `expectation_unconfirmed`, or return the item) and gives the answer to the conductor. No `--block` door is offered (g1). The text is false for door B (F2).
- AR-29/question 11: no judgment moves into code. It is a join from a tag to a cause on an existing constant. No census row was added (`"function": "refusal_cause"` is absent; that is the card's grep, not re-run).

**3) N5: one place, all readers behind it?**
- Yes for the join's location: `_terminal_runs` is its only home. The 7 readers listed in R8 are the only `_terminal_runs` callers (grep `_terminal_runs` over `scripts/*.py`: acceptance `:445/:699/:865`, proof_level `:2003`, stand_gaps `:403`, story_step `:2965`, window_record `:1367`).
- Readers of "latest terminal run" that do NOT go through it:
  - `s5_precheck._latest_runs` (`:2161`, `:2299`): the precheck's own road; the spec lists it as a sibling.
  - `finalize_task._project_env_blocks` / ghost join (`:140`, `:202`) and `contract.superseding_terminal_result` (`:4226`): these join by case or exact id for env-block superseding. They answer a different question, so they are not siblings to change.
- Class gap: axis 24 (F5).

**4) Duplication and quality (brief items 6-7).**
- DUPLICATION: F5 (alias maps: `acceptance.py:568`, `case_stamp.py:293`, now `window_record.py:483-493`). There is no other duplicate in N4: grep `awaits_answer|REFUSAL_CAUSES` outside the tests finds only the declared sites, and the footer and gate line are two surfaces named by the card.
- QUALITY: F3.
  - N5 test: the run-block JSON writer is copied between the `ALIAS_ROWS` loop and the w7 block (`test_window_record.py` ~1255-1290). This is minor; a local helper would remove it.
  - `a_terminal_run_is_the_latest_by_the_clock` grows to about 90 lines, as the card dictated.
  - No new product function exceeds 60 lines or 3 nesting levels. In-tree ratchets: no row is raised by either diff.

**5) Where the branches meet.**
- `git merge-tree --write-tree` gave rc=0, i.e. no textual conflicts, for every pair checked: N4+N5, N4+379f687 (wave 8), N5+379f687, N4+tbw-t2, N5+tbw-t2.
- origin/main == a3f9a49 (the N4 base). The N5 base d5d602d is its ancestor.
- Wave 8 touches `acceptance.py` only in `stage_acceptance_refusal` (`@@ -1556`), not a terminal-run reader. tbw-t2 leaves `REFUSAL_CAUSES`/`_tag_lines`/`tag_cases` textually as they are (its own copy of `:223` still reads "family or predating"). After the merge the N4 text wins and T2's new `refusal`/`spoken` do not read causes.
- Canon risk:
  - `test_s5_precheck.py`: 4 pins plus the footer pin. Only the one function was re-run after b483ac8 (21/21); the whole file is judged by the canon.
  - Slow files that build a window over a manifest whose runs are alias-spelled and that expect the no-run branch could turn red after N5 (`test_window_record.py`, `test_red_window.py`, `test_blocked_by_env_window.py`). Not run (slow). A red there is either a correct reading (§4.3) or B1.
  - `test_row_fields.py:366-374` is already red in quarantine (N4-F4 (a)).

**6) Analogs worth a node.** F4 and F5 (proposed above, owner Lead). F6 folds into the later merge. N5 reported no analogs.

**ONE ROAD (item 12).** None found beyond F5. Grep: no language, runner or project branch in either diff (both diffs read whole). The N5 window/precheck precedence difference (N5-E4) is stated in the spec; it is not a new exclusion.

## Spot-checks

- The N4 control re-run matches the witness (348/348).
- Report claim "AR-28 ambiguity credits no run" (N5): refuted by the probe (B1).
- The N4 claim that the `family` pins outside the four R6 pins are not about open-oracle: my grep for `author's repair|carry the source's .refused` over the tests outside `test_then_remainder` gives 1 unrelated hit (`test_red_window.py:524`). Grep `open-oracle|OA_TAG` gives the hit in `test_exit_gate_advice.py:214`, which was read and carries no cause pin.
- Positive control: the same grep finds the known `test_then_remainder.py:831` on 379f687.

## Trail

- Read: the spec (whole); critic-diff-brief; both diffs (whole); both reports; `s5_precheck.py` `:1640-1700`, `:3960-4010`, `:4770-4825`; `story_step.py` `:2005-2070`; `exit_gate.py` `:1780-1820`; `contract.py` `:4040-4110`, `:4205-4235`; `window_record.py` `_load`, `:1365-1450`; `proof_level.py` `:2015-2022`; `acceptance.py` `:568-576`, `:874-884`; `case_stamp.py` `:293-312`; `finalize_task.py` `:120-215`; tbw-t2 `detector_verdict.py` `:140-200`, `:295-340`; `SIBLING_MAP.md` axes 17, 24-26, 34; `test_exit_gate_advice.py` `:205-225`; commit messages eabcc44, b483ac8, 5c90164.
- Re-run: `python -B …/fv130b-n4/…/tests/test_then_remainder.py` → `=== test_then_remainder: 348/348 ok ===` (16 s).
- Probe: an inline read-only python on the N5 worktree in temp dirs, output quoted under B1.
- `git merge-tree --write-tree --name-only` for 5 pairs → rc=0 each.
- No slow file, full set or mutation was run.

```json
{
  "verdict": "blocker",
  "blockers": [
    "N5 window_record.py:490-493 -- owner values keep ambiguous spellings: a run under an unambiguous alias of entry B is keyed under B's shared/bare spelling, so another instance's canonical (probe P2: test_x gets TC-9::test_x failed) or first-alias walk (P1) reads B's run; violates N5-E5 and the commit's AR-28 line. Fix: filter the value tuple to spellings with len(spellings[a]) == 1; add rows w4b/w4c."
  ],
  "fixes": [
    "N4 s5_precheck.py:4807-4809 and story_step.py:2052-2056 -- texts claim the line names the question; false for door B (no registered question): say either the question or the road back to S4 (Lead edits card wording).",
    "N4 test_then_remainder.py:879-881 -- assert _passable on every k22 row (dead column) and drop the one-iteration loop.",
    "Queue: exit_gate.py:1815 word_class and s5_precheck.report compare the waiting tag case-sensitively while refusal_cause lowers it (unreachable today; node, owner Lead).",
    "Queue: a third alias/ownership join beside acceptance.tests_by_alias (acceptance.py:568) and case_stamp.run_row_for (axis 24); one contract-level owner map with ambiguity dropped (node, owner Lead).",
    "Fold: test_detector_verdict.py:487 stale label into the later N4/tbw-T2 merge."
  ],
  "class_completeness": "N4: axis 17 producer/readers changed together; door-B text sibling inside the same artifact missed (F2). N5: SIBLING_MAP axis 24 (one run-row join, case_stamp.run_row_for) not walked; three ownership maps now coexist (F5, proposed node). All seven _terminal_runs callers are behind the one change (grep).",
  "trail": {
    "read": [
      "docs/tasks/specs/20261114-fv1-30b-n4-n5-cards-spec.md",
      "docs/tasks/critic-diff-brief.md",
      "N4 diff a3f9a49..b483ac8 and report",
      "N5 diff d5d602d..5c90164 and report",
      "s5_precheck.py 1640-1700, 3960-4010, 4770-4825",
      "story_step.py 2005-2070",
      "exit_gate.py 1780-1820",
      "contract.py 4040-4110, 4205-4235",
      "window_record.py _load, 1365-1450",
      "acceptance.py 568-576, 874-884; proof_level.py 2015-2022; case_stamp.py 293-312; finalize_task.py 120-215",
      "tbw-t2 detector_verdict.py 140-200, 295-340",
      "docs/SIBLING_MAP.md axes 17, 24-26, 34"
    ],
    "reruns": [
      {"command": "python -B .claude/worktrees/fv130b-n4/ai-packages/qa-factory/scripts/tests/test_then_remainder.py", "result": "=== test_then_remainder: 348/348 ok ==="},
      {"command": "inline read-only probe of window_record._terminal_runs on the N5 worktree (temp dirs)", "result": "P2: key test_x holds TC-9::test_x failed; P1: key test_x[eu] holds TC-1::test_x[eu] failed; control w4 unchanged"},
      {"command": "git merge-tree --write-tree for N4+N5, N4+379f687, N5+379f687, N4+tbw-t2, N5+tbw-t2", "result": "rc=0 for every pair (no textual conflict)"}
    ]
  }
}
```
