# t-1271 - code review, topic "U7 pass without getting stuck", streams 1, 5a, 5b, 7a

Spec: `docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r3.md` (the `given` path under `.claude/worktrees/arch-docs/` does not exist; I read the same file on main, commit 1323da2b, which is the base of all four branches). Diffs read with `git -C <worktree> diff origin/main...HEAD`.

**Verdict: NEEDS WORK** (JSON `fit_with_fixes`). No finding calls for a REJECT. Per stream:
- **stream 1 (t-1263): accept with fixes.** F1-1 must be settled before this branch merges.
- **5a (t-1264): accept with fixes.**
- **5b (t-1265): accept with fixes.**
- **7a (t-1266): accept with fixes.**

Acceptance stays with the Lead (rule 6).

Builder reports were not attached; only the test tails were. So the FR walks (K5) are mine, done on the diffs. Three mechanical items are missing and go back to the coordinator as requests (rule 21):
- (a) 5b's writer-check run and its `stage_done` S5 premise run, verbatim (r3 §2 r11 "Temporal" and "Writer check");
- (b) 7a's Walk 1 measurement before and after (r3 §2 r4, "Premise measurement");
- (c) the whole `test_gate_preflight.py` run, or its batch-canon line, for 5a's text sweeps.

## Findings

**F1-1 (stream 1; must be fixed before stream 1 merges; FR-10, FR-41).** The new words say the agent tries the cases. The code still hands them on untried. Item 4 (`_row_of_nobody` converts) is not in this diff.
- Input: a plan row whose profile has capability `cli` or `desktop`.
- Path: `planning_contract.py:2340-2345` (unchanged) gets the row's new words from `_row_of_nobody` and writes `"<ob> stays as planned - The factory has no driver for a command-line application: the agent tries those cases by hand with what it can reach..."`. The row is not converted to manual-agent.
- So one line says both "stays as planned" and "the agent tries". The readiness record says `hands: role`, and changelog bullet 2 says "before, the cases were handed to a person untried", both before that is true.
- The same diff's `architecture.md` axis 2 cell correctly keeps "cases of any other surface go to a person", so the branch also contradicts itself.
- Root cause is in the spec: r3 §6 dispatches items 2-3 now and item 4 after 7a.
- Fix, a fork for the Lead:
  - (i) recommended: move item 2 (`_who` and the three literals -> "role"), item 3's `cli`/`desktop`/`unknown_word`/`no_stand` words, and changelog bullet 2 into node 1b. Items 1, 5 and 6 stay here.
  - (ii) merge stream 1 and node 1b in one wave, with no release between them.

**F1-2 (stream 1, low, fix before merge; rule 22 Q7).** In `readiness.py::_check_plain_environment`, the URL-less test `not any(str(e.get(k) or "") for k in ("base_url","url","health_url"))` is written twice in the new code (the `in_process` comprehension and `by_default`). Make it one local helper. Also, two URL-less stands give "stand a, b names no address" (singular verb).

**F1-3 (stream 1 effect, low).** `gate_preflight.py::_surface_level_fits` (771-779) has the docstring "declares nothing beyond web/API words (the table is NOT read)". For a config with no capability word, `declared_surfaces` now returns `{undeclared}`, which is truthy, so the table IS read. I traced the result: it is unchanged, because no profile carries a capability word and `any(...)` is False. So only the comment lies. The file belongs to 5a: fix it in 5a's round, or have the Lead do it at merge.

**F1-4 (stream 1, low; Q7).** `surfaces.unsupported` has no production caller. A case-insensitive grep over `scripts/*.py`, excluding tests, finds only its own definition. Its docstring was reworded and nothing reads it. Delete it in the fix round. List the quarantined `test_surfaces.py` rows that call it in the report, as the stream already does for the other contradicted rows.

**F5a-1 (low).** One phrase of the `install_dependencies` row is wrong.
- `_missing_launcher`'s fix text says "the project's own install command is `...`".
- But `dependency_drift.install_command` (118-130) can return `source: "table"`, a command the factory guessed from the package manager.
- Fix: say "the install command" when `command["source"] != "profile"`, or name the source.

**F5a-2 (low; spec text defect too).** The F-14 clause with no reason reads "the packages installed for this profile could not be read: it could not be read". When `why` is empty, drop the tail after the colon. The r3 §2 r8 F-14 edge line should say the same.

**F5a-3 (tests; Q5(e)).** `test_u7_5a_r8_the_dependency_check_runs_before_the_executor_check` duplicates the rig row.
- The rig rehearses through `gate_preflight.run` with the same fake `check_s5_dependencies`.
- If the tuple order were wrong, `_drift` would be unset, the finding would be a card, and the rig's `len(rig.calls) == 1` would fail.
- So cut the separate test (about 17 lines).

**F5a-4 (signature; for K2's node).** `executor_install(task_root, profile_id, tool, drift)` takes Rehearsal state (`_drift`), not `(root, task_root, profile_id)` reading `dependency_drift.check_profiles` (r3 §2 r8).
- For roads 1 and 2 this is correct and keeps the B6 invariant (None = check not run = card).
- Road 3 (`run_suite`) has no `_drift`. It would have to re-derive the filter `state in ("differs","missing_only")` (`gate_preflight.py` ~2985), which would be a second filter.
- The K2 node should lift that filter into one module function that both call.

**F5b-1 (5b and 7a, fix before merge; AR-13, rule 22 Q6).** The "stage X closed by code" reader now exists three times:
- `s7_pretriage.s6_closed_by_code` (309-318), the existing one; `check_delivery._s6_closed_by_code` already delegates to it;
- `acceptance._s5_closed_by_code` (new, 5b): the same body with the stage changed;
- 7a's rule 2 inside `triageable_not_executed`: a third inline `Controller(task).state()["stages"]["S6"]` read.

Fix: one `stage_closed_by_code(task_root, stage)` and one `stage_status(task_root, stage)` beside it, in `s7_pretriage`. `s6_closed_by_code` becomes a wrapper; `acceptance` imports it lazily, and the predicate's rule 2 calls it. The owns widen by one function each (the Lead's call). Do it in one fix round after 7a merges.

**F5b-2 (Lead at merge; FR-2 / AR-9 in a design document).**
- The door key `"code-only receipts are allowed only for S0, S6, S7 or S8"` at `tools/controller-blocks-gen.py:227` also matches the new `_s5_code_only_problems` StateConflict.
- So `design/controller-blocks.md` gives that row the door "a stage with a role is closed by that role, not by code". The refusal's real doors are "rework S3 or record dispositions" and "S5 runs its author and critic".
- Fix: add a more specific key for "and for S5 only over its own empty derived plan scope:", check whether the generator takes the first match or the longest, then regenerate. This is the door note the 5b builder asked for.

**F5b-3 (noted, not a fix).** `stage_S5` and `Controller._s5_code_only_problems` both state the four conditions, with different wording. r3 asks for exactly this (the driver decides, the controller re-checks from its own scope), so it is accepted. A future wording change must touch both.

**F7a-1 (low, fix before merge; owns widen).** `driver_machine.py:4212`, the dry "would" print, calls `failures_to_triage()` without `awaiting`.
- When S6's runner awaits its consumer (S6 not `completed`), the dry print says "S7 entry: refused" while the live path admits the story.
- r3 §8 says "its one caller is stage_S7", and that premise is false.
- Fix: pass `awaiting=acceptance.awaits_acceptance(self.controller_state(), "S6", self.pipeline())`.

**F7a-2 (tests; Q5(e)).** Several door rows repeat what the predicate table already asserts:
- `test_check_delivery.py`: "no target", "S6 not finished" and the second admit row ("unprepared") repeat predicate rows. Keep one admit row and the broken-half row.
- `test_story_run_s7.py`: "no target" and "S6 not finished" repeat predicate rows. Keep inconclusive (code close), unprepared (analyst), broken half and code-only S6, because those reach different moves.
- `test_s7_pretriage.py`: "reads only: the report is byte for byte as it was" checks that a reader does not write. It is the «Как раньше» row type of TESTING.md's "Что не пишется" table: cut it.

## K1 fit to spec

- **Stream 1.** Done:
  - item 1: `undeclared` for profiles absent, no capability word or an empty list; an unreadable table gives `unknown`; web/API reads the table 0 times;
  - items 2-3 as written (but F1-1);
  - item 5 matches the target text; declared rows are byte-identical (the pins are kept);
  - item 6: the axis 2 and axis 7 cells use r3's exact sentences.

  Item 4 is a later node. The readiness comment at 1314-1315 is amended (FR-37). The `in_process` keyword tuple is pre-existing (AR-1 holds).
- **5a.** Done:
  - items 1-2: the decision is in one method, `_missing_launcher`, used by both roads;
  - item 3: tuple order, `gate_preflight.run` 6189;
  - item 4: `close_executor_bound` in `hand_to_conductor`'s `finally`, `unturned_executors`, the series re-hand, `CHECK_WORDS`;
  - item 5: zero automate rows skip the collect, but an unreadable plan still collects;
  - items 6, 8, 9 and 10.

  Item 7 was stopped (K2). Item 11: the coordinator measured 0 discrepancies, so no row is owed. The record edges hold as traced:
  - absent -> `[]`;
  - unreadable or wrong shape -> `None` -> "turn had";
  - write fails -> printed, `executor_handed`, no re-hand.

  The no-install path makes no conductor call by construction, because only `FACTORY_FIXABLE` findings reach `hand_to_conductor`.
- **5b.** Done:
  - items 1-5, including `undisposed` on the derived branch only. `_case_rows` maps approved cases only, so no unapproved case is listed.
  - item 6 is the comment fix;
  - item 7: no s5.json row is owed, since dry_exits shows 0 discrepancies;
  - item 8: the runs were not attached (request (a)).

  Positions hold: the branch sits after `stage_scope` and before `s5_todo`; stale -> recover once; another exit -> a Refusal that does not quote the writer.
- **7a.** Done:
  - rules 1-5 as written;
  - the join-failed exclusion is `finalize_task.JOIN_FAILED`;
  - rule 4 uses a per-row `triage_targets` call, which agrees with the whole-report reading (traced at `contract.py:4655-4690`);
  - `failures_to_triage(awaiting="")` with the caller passing `awaiting`;
  - the comments are restated;
  - `run_reasons` reads the predicate.

  Deviation: F7a-1.

## K2 road 3

Verified by reading.
- `driver_dispatch.py:98` holds `("executor", r"executor[_ ]unavailable", "ask_person")`.
- `driver_machine.py::handle_refusal`: `route_known` matches the row. The `ask_person` branch (480-485) returns `self.no_move({... "call": False ...})`, so the person is reached with 0 conductor calls. The r3 road-3 premise is false.

Does leaving road 3 person-first break the goal? Yes, for a remainder case. Gate A normally catches a missing launcher first, and a turn already had there makes a card correct anyway. But a launcher that goes missing after gate A, or `skip_executor`, still reaches the person with no turn while an install command is known. That is a second road for one action (P31, Q12(a)).

Minimal fix, a node with an owner (the Lead opens it):
- (1) `run_suite.py::refuse_missing_executor` adds `install` and `install_digest`, from the shared drift filter (F5a-4) and `executor_install`.
- (2) `driver_machine.py::handle_refusal`: before the `ask_person` branch, when `name == "executor"` and the refusal's JSON `install` is non-null (read as a FIELD, FR-12, never as a phrase), go to the seam WITHOUT `call: False`. Use moves `["install_dependencies", "person_does", "stop_here"]` and keep today's question as `site_fallback`. Record the key through the same writer, `close_executor_bound` (one writer, AR-14).
- (3) `halts.md:28` and `s5.md:144` sentences as in r3.
- (4) Test rows in `test_gate_preflight.py`'s rig:
  - `install` set, no turn -> conductor calls 1, record written;
  - `install` null -> Person, calls 0;
  - turn recorded -> Person, calls 0.

## K3 test volume

- **Stream 1 (113 test lines / 37 code lines).** The reason "one parameterised table per behaviour" does not hold. Cut:
  - the text pins "agent tries" in `words[key]`, "declares no test surface", "undeclared words are the table's", and "factory defect" in the error (TESTING.md "Что не пишется": pins on text);
  - the four `row_for_profile` rows, which test unchanged code that belongs to item 4 (`test_question_branches.py`);
  - the `unsupported` row, which tests a function with no caller.

  Keep the declared_surfaces table, the 0-read row, the record rows and the r3 table. The result is about 70 lines; the rest is earned by the seam.
- **5a (317/168).** The reason "seven table rows cover three roads" is false: road 3 is not built. Amend the `tests-over:` line. Cut F5a-3. The `LauncherRig` (about 45 lines) is earned: it is the only driver rig in this keep file, and r12 reuses it.
- **5b (161/123).** The reason holds. Cut the internal-only row "stage_scope on the underived branch keeps its keys".
- **7a (170/73).** The reason partly holds, since the table form is right. Cut the F7a-2 rows, about 25 lines.

## K4 open points

- **(5b) empty approved scope -> S5 closes by code.** Correct; not a silent pass.
  - `_case_rows` gives an empty mapping, and every list is empty. The close carries a receipt with its reason, and it twins `s6.nothing`.
  - Gate A approval of the scope is the person's word.
  - Delivery's coverage leg still reads the requirements.
- **(5b) two readers.** Yes, AR-13: see F5b-1.
- **(5b) FR walk read only through the index.** This misses the *Check* lines. FR-2's *Check* line ("a test opens it") is not in the index. The driver refusal's door ("rework S3 or record dispositions") has a conductor row ("rows go back to qa-test-strategist at S3", conductor-actions.json), but no test opens it. FR-59 holds: every unknown refuses.
- **(5a) signature.** See F5a-4. The tautology is F5a-2.
- **(5a) dead code?** No, but the condition is narrow.
  - `dependency_drift.check` gives `differs`/`missing_only` only when an environment exists (376-389). That covers an existing venv or node_modules with the launcher package missing or stale, so the node fires there.
  - The commonest case is no environment at all (`env is None` -> `unknown`, 376-377). It stays card-first, even though `command` is computed.
  - Proposed node: `dependency_drift` answers a field for "no environment", and the gate treats that `unknown` with a profile command like `missing_only`. The `install_dependencies` row's `run` then needs a source other than the s5_dependencies note.
  - Variety: on an npm or poetry project with no environment, the factory asks the person where a free agent would run the install. That is worse than a free agent, but no worse than main.
- **(1) `unsupported()`.** See F1-4. The quarantined test_surfaces rows are not edited (spec); the list goes in the report.
- **(7a) second caller.** See F7a-1.

## K5 FR, AR, variety

- **FR sections touched.**
  - A: new doors are usable (the 5a fix text names a conductor row; the 5b driver and controller refusals name S3 rework).
  - B: F1-1 (FR-10) and F5a-2.
  - C: FR-12 holds (5a keys on finding fields, 7a on status fields).
  - D: FR-58 and FR-59 hold (7a never rewrites `execution_status`; 5b's excuse is bound to the receipt).
  - E/F: F5a-1 (FR-41).
  - G: no Cyrillic and no control bytes in the added lines (with positive controls); all blobs are LF on both sides (per-file CRLF counts are 0 on main and HEAD).
- **AR lines in the commits are kept,** except AR-13 (F5b-1) and stream 1's AR-2 claim "a role move", which is premature (F1-1).
- **Variety.**
  - Stream 1: legacy web configs get one informing line, and a broken table now says `unknown` for them (informs).
  - 5b and 7a: all-manual and mobile/desktop/CLI manual stories now pass S5 and S7. That is better.
  - 7a: a mixed story whose automated half broke is still refused (honest).
- **Ratchets (Q9).** None raised. `driver-layers.json` gains 2 members; it is not a shrink-only ratchet. The `forge-check` result was not attached.
- **Judgment (Q11).** No census row added, and the `judgment:` lines name shape joins. OK.

## K6 duplication, quality, class

- Q6: F5b-1, F5b-3, F1-2 and F5a-4.
- Q7: no new function is over 60 lines. Each of these sits at three nesting levels or fewer:
  - `close_executor_bound`, about 28 lines;
  - `_missing_launcher`, about 20;
  - `triageable_not_executed`, about 35;
  - `_s5_code_only_problems`, about 25.
- Class (axis 5 "Code-only stage closes"):
  - the `s5.nothing` site is in `CODE_CLOSE_SITES`;
  - the `stage_transition` marks carry `code_only` over `stage_done` (axis note C3-14), so the receipt survives the close.
- S7 entry twin: the only readers of the S6 receipt and of `not_executed` admission are `driver_stage_s7:20` and `check_delivery:1290`. Both now read the predicate. Grep shown in the trail.
- architecture.md cells 2 and 7: done. Cell 3 belongs to 7b.

## K7 merge

- The four branches share no file. Each tip merges cleanly onto origin/main 3e1df1e4: `git merge-tree --write-tree` exits 0 for all four. On main since the base, only `docs/SIBLING_MAP.md` and p1/p2 changed.
- The Lead edits at merge:
  - (1) SIBLING_MAP axis 5: the clause "and S5 (conductor/3 C3-2, owes the same precondition and bound; the controller refuses `code_only` S5 today)" is still verbatim at line 130 of origin/main, so r3 §6's replacement applies.
  - (2) `tools/controller-blocks-gen.py:227` (F5b-2), then regenerate.
  - (3) F1-3, if 5a's round does not take it.
- Order: 7a before 5b's F5b-1 round; 1b after 7a; stream 1 per the F1-1 fork. 5a is free.

## Spot-checks

- Mechanical "registration of the 5a functions unverified": verified by reading. All seven are in `test_gate_preflight.py` main at 6547-6553.
- Re-run of 5b `test_check_witness.py`: 53/53, the same as attached.
- "No production caller of `unsupported`": grep `unsupported(` over scripts/*.py, excluding tests. The positive control is the same grep finding `red_sandbox._unsupported`.

## Trail

- Read: spec r3 §0-§8; TESTING.md 180-219; factory-rules.md FR-2, FR-10, FR-37, FR-59.
- Diffs of all four branches, read whole.
- `driver_gates.py` 849-1045 (gate_repair, gate_stop, hand_to_conductor, fixable_findings).
- `driver_dispatch.py` 85-105.
- `driver_machine.py` 50-70, 440-485, 4195-4225.
- `dependency_drift.py` 118-135, 335-395.
- `gate_preflight.py` 712-727, 760-785, 1592-1596, 2955-3005.
- `planning_contract.py` 2277-2345.
- `controller.py` 2516-2545, 4215-4282.
- `acceptance.py` 645-668, 1472-1487.
- `s7_pretriage.py` 309-318.
- `check_delivery.py` 1290-1316.
- `contract.py` 4595-4690.
- `driver_stage_s5.py` 180-230.
- `driver_stage_s7.py` 40-80, 763-786.
- `manifest_put.py` 2177-2191.
- `stages.json` S5.
- `conductor-actions.json` row 34.
- `tools/controller-blocks-gen.py` 215-235.
- SIBLING_MAP line 130 on origin/main.
- Commands:
  - `git merge-tree --write-tree origin/main <tip>`: exit 0 for f6fa3c74, 45f38f29, 2e765baa and 4b8dac2b;
  - `python -B .../agent-a9f7ad5ad9ddbe8fc/.../tests/test_check_witness.py` -> `=== check witness: 53/53 ok ===`.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "Axis 5 code-only closes: s5.nothing row and receipt marks carried; S7 entry twin: both readers (driver_stage_s7:20, check_delivery:1290) read the one predicate; gaps: AR-13 reader of the code-only receipt cloned in acceptance and inlined in the predicate (F5b-1); dry print caller driver_machine:4212 (F7a-1); road 3 of the missing launcher stays person-first, node proposed (K2).",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r3.md",
      "docs/TESTING.md",
      "ai-packages/qa-factory/design/factory-rules.md",
      "ai-packages/qa-factory/scripts/driver_gates.py",
      "ai-packages/qa-factory/scripts/driver_dispatch.py",
      "ai-packages/qa-factory/scripts/driver_machine.py",
      "ai-packages/qa-factory/scripts/dependency_drift.py",
      "ai-packages/qa-factory/scripts/gate_preflight.py",
      "ai-packages/qa-factory/scripts/planning_contract.py",
      "ai-packages/qa-factory/scripts/controller.py",
      "ai-packages/qa-factory/scripts/acceptance.py",
      "ai-packages/qa-factory/scripts/s7_pretriage.py",
      "ai-packages/qa-factory/scripts/check_delivery.py",
      "ai-packages/qa-factory/scripts/contract.py",
      "ai-packages/qa-factory/scripts/driver_stage_s5.py",
      "ai-packages/qa-factory/scripts/driver_stage_s7.py",
      "tools/controller-blocks-gen.py",
      "docs/SIBLING_MAP.md"
    ],
    "reruns": [
      {"command": "python -B .claude/worktrees/agent-a9f7ad5ad9ddbe8fc/ai-packages/qa-factory/scripts/tests/test_check_witness.py", "result": "=== check witness: 53/53 ok ==="},
      {"command": "git merge-tree --write-tree origin/main <tip> for f6fa3c74 45f38f29 2e765baa 4b8dac2b", "result": "exit 0 for all four"}
    ]
  },
  "fixes": [
    "F1-1 stream 1 before merge: move item 2 hands relabel, item 3 words and changelog bullet 2 to node 1b, or merge stream 1 with 1b in one wave (Lead fork); planning_contract.py:2340-2345 prints 'stays as planned - ... the agent tries' today",
    "F1-2 readiness.py _check_plain_environment: one helper for the URL-less test; grammar for several stands",
    "F1-3 gate_preflight.py:771 docstring of _surface_level_fits no longer true for a no-capability config",
    "F1-4 delete surfaces.unsupported (no production caller), list the quarantined rows",
    "F5a-1 fix text says the project's own install command when command.source can be table",
    "F5a-2 F-14 clause tautology when the entry has no reason",
    "F5a-3 cut the order test duplicated by the rig; amend the tests-over line (road 3 not built)",
    "F5b-1 one stage_closed_by_code reader in s7_pretriage used by acceptance and the 7a predicate (AR-13)",
    "F5b-2 Lead at merge: specific door key in tools/controller-blocks-gen.py:227 for the S5 code_only refusal, regenerate",
    "F7a-1 driver_machine.py:4212 dry print passes awaiting",
    "F7a-2 cut duplicate door rows in test_check_delivery and test_story_run_s7 and the reads-only row; stream 1 cut text pins and row_for_profile rows (K3)",
    "Mechanical layer requests: 5b writer-check and stage_done premise runs; 7a Walk 1 before/after; whole test_gate_preflight.py or its canon line",
    "Node for the Lead: road 3 of the missing launcher through the seam (K2 file/function/test rows); node: no-environment unknown with a profile install command (K4)"
  ]
}
```
