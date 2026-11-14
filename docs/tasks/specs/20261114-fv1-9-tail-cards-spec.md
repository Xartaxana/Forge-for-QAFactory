# FV1-9 tail: builder cards for P1, P2, P4, P5, P6 (designer draft t-718)

Status: DRAFT for Lead acceptance. Forks are in §3. Each one has options, a recommendation and its cost; none is decided here. Every card can be
run on its recommendation before the answer comes (PROJECT.md «Командная работа» п. 11).
Source: the topic critic `docs/tasks/specs/reviews/20261114-fv1-9-topic-critic.md` («Proposed nodes»); the spec
`docs/tasks/specs/20261114-fv1-9-question-repeats-spec.md`; the fix report `.claude/worktrees/fv1-9-fix/docs/tasks/specs/reports/20261114-fv1-9-fix-report.md`.
Tree read: `C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-fix` (wip/fv1-9-fix). The hash ef5bdcf was NOT checked: no shell was available
(§6). All file:line references point at that tree.

## §0. Summary for the Lead

| item | outcome | card | waits on |
|---|---|---|---|
| P1 | card A, by fork F-1 (b). The Lead's literal road does not fit the facts (§1.1) | A | none |
| P2 | card C (with P5: the door sentence names `--stage`) | C | none (C and B touch `question_register.py` through disjoint functions) |
| P4 | card D | D | none |
| P5 | card C | C | as P2 |
| P6 | card B | B | none |
| P3, P7 | out of scope: one line each for the queue (§5) | - | - |

Order against N3 (T12/T13): N3 can be dispatched once **A and B** have merged into the topic branch. B is in the list because a crash replay
without B makes A tell roles false refusals; details are in §4. N3 also still waits on its own spec order, `TQ2-1 K1 -> A2 -> FV1-9 N3`
(spec §6, `qa-case-critic.md`). A2's status could not be established (§6). C and D do not hold N3 back.
Parallelism: A, B, C and D can all run at once (D-0048: disjoint functions). The shared files are listed under each card, and in each
pair the node that merges later merges `main` and resolves the conflict itself.

## §1. Facts the cards rest on (checked at the carrier)

### 1.1 Why `question_pass_lines` (Lead's road) cannot carry P1 as it stands
- `question_pass_lines` is `{dispatch: [lines]}`. It is written at `driver_dispatch.py:1674` (threshold stop), `:1802` (`take_question_answer`) and
  `:1815` (after the hand-over). It is popped ONLY by `question_resume_prompt` (`:1734`), which is called only by `resume_role` when it resumes
  after a stop (`:1059-1060`). The `driver-layers.json:1189` note reads "popped by question_resume_prompt".
- The three carriers run AFTER that dispatch's only stop:
  - `run_role` calls `question_threshold` at `:760` BEFORE `finish` (`:764`), and `finish` runs the `complete(digest)` callables (`:771-772`).
  - The S3 plan projection `s3_project` -> `PC.project_plan` (`:2726`) runs inside those callables (`s3_window_completion`
    `driver_stage_plan.py:503-523`, `s3_rework_completion` `:2696-2703`, `s3_ticket_completion` `:2731-2738`).
  - The acceptor's form raise `stage_acceptance_write` (`driver_stage_plan.py:641-651`) runs inside `stage_critic_completion.complete`
    (`:671`) and `s4_critic_completion.complete` (`:811`).
  - `critic_rollcall --apply-fixes` runs in `s4_after_critic` (`:759-762`) after the critic's finish, and at gate A in
    `driver_gates.raise_move` (`:595`).
  - No resume of the writing dispatch follows any of them, so a line stored under that dispatch's key would never be read.
- The receivers are the WRITING roles' NEXT sessions. For the designer and the planner that is a rework through `self.rework` -> `run_role`
  (`driver_dispatch.py:2785`; `stage_after_critic` `driver_stage_plan.py:630`; `s4_after_critic` `:766`). For the acceptor it is its next
  `run_role` (`stage_critic_route` `:616`). Every fresh or rework prompt is assembled in ONE place: `run_role` `:698-709`
  (`lines = [prompt]` ... `lines += list(extra)` ... `full_prompt`).
- The conductor is not the receiver of any of the three carriers. Its own `--repeat`/`--reword`/`--note` refusals reach it directly as the
  CLI's exit 2 text (`question_register._main_fv19` `:2336`, `:2348-2349`). So the stop hand-over carries doors (P2), not refusal lines.

### 1.2 The three silent outputs (verified)
- `project_plan` returns `SimpleNamespace(wrote, problems, notes)` (`planning_contract.py:3402`). Notes are written at `:3420` (approved plan)
  and `:3452-3453` (`_reword_plan_entries`). `s3_project` reads `.problems` only (`driver_dispatch.py:2726-2729`).
- `critic_rollcall.main --apply-fixes` prints ONE JSON line with `repeats`/`rewords`/`question_notes` (`critic_rollcall.py:1196-1201`; exit 1
  when skipped/errors). Both drivers' calls drop it: `s4_after_critic` (`driver_stage_plan.py:761`, return value unused) and `raise_move`
  (`driver_gates.py:595`, only the tail of `out`, and only on exit 1).
- `raise_from_handoff` adds `rewords`/`reword_problems` (`question_register.py:2222-2234`). The CLI prints it as indented JSON
  (`:2439`). `stage_acceptance_write` runs it with `check=True` and drops the output (`driver_stage_plan.py:647-649`).
- `Driver.py` returns `(exit code, stdout+stderr)` (`driver_runner.py:211-212`). The driver already parses JSON out of such output with
  `json.loads(out[out.index("{"):out.rindex("}") + 1])` (`driver_gates.py:331`, `driver_machine.py:1692`).

### 1.3 A carrier gap found while reading (beyond the brief; fork F-4)
`s4_after_critic` runs `critic_rollcall --apply-fixes` only when `fixes` (the findings say `approve_with_fixes`) or `self.unraised_cases()`
(`driver_stage_plan.py:759`). `unraised_cases` (`:871-886`) looks only for a Then whose ref is `raise`. A case that holds only
`question_repeats` or `reword_questions`, under an `approve` verdict, is therefore never executed. `raise_pending` itself does read all three
keys (`critic_rollcall.py:774`). The gate A repair also triggers only on `unraised_questions`. N1's POSITIONAL P3 widened the filter inside
`raise_pending` but not the driver's trigger. This is the same AR-22 class as P1 (a key with a producer, N3, and no reliable reader).

### 1.4 Other facts
- `--stage` is refused with any operation but `--raise` (`question_register.py:2423-2424`; help `:2390`). `_main_fv19` hard-codes `stage=""`
  for `declare_repeat` (`:2340`) and `reword` (`:2343`). Its docstring says "the stage is not known" (`:2295`). The retro prints "an unrecorded
  stage" (`retro_numbers.py:2845`). The stage table is read through `contract._stage_entry` (`contract.py:5848-5859`, never raises, `{}` for
  an unknown id); `acceptance.stage_def_of` (`acceptance.py:1286-1292`) wraps it. `stages.json` has 10 `"id": "S<n>"` rows (Grep count).
  `ROLE_QUESTION_STAGES = ("S1","S2","S3","S4")` (`question_register.py:2067`) is a role-form list and NOT the CLI's stage vocabulary.
- The hand-over (`register_words_to_conductor`, `driver_dispatch.py:1818-1906`):
  - It names the answer door at `:1854-1856`, without `--task`.
  - It names the reword door at `:1857-1859`, without `--task` and without `--stage`.
  - The `--show` door, the only one with `--task`, is at `:1860`.
  - It names no `--repeat` door.
  - The text is built only when `recorded is not None`, and that happens only at stages whose `"<stage> stop"` is in the vocabulary.
    `record_halt_words` returns None otherwise (`:1937-1938`), and `question_threshold` returns early (`:1624-1625`). The vocabulary holds
    `S2 stop`, `S3 stop`, `S4 stop` (`question-vocabulary.json:5`). So `--where "<stage> stop"` is always a valid value there.
  - No test pins either FV1-9 sentence. A Grep for `--answer QID --reading|--reword QID|could not tell what it asks` over the package finds
    only `driver_dispatch.py:1855,1857-1858` (that same search is its own positive control).
- Fast keep file that already builds a `Driver`: `test_gate_question_form.py` (keep row `test-layers.json:1995-2028`, covers
  `driver_dispatch.py`, `driver_stage_plan.py`, `driver_gates.py`, `question_register.py`, `planning_contract.py`; it builds
  `story_run.Driver.__new__(...)` at `:768`, `:830`, `:891`). It is absent from `slow_tests.json` (measured 2026-11-12, threshold 10 s), so it
  is fast. The same holds for `test_question_register.py` (keep `:4203`) and `test_retro_numbers.py` (keep `:4569`). `test_report_facts.py`
  is slow (55.6 s); `test_driver_layers.py` is slow (32.5 s); `test_s3_strategist_rounds.py` is slow (15.9 s).
- `test_driver_layers.py` is a census of every name of the driver family (`:1`, `--draft-missing` `:23`). A new `Driver` method needs a row
  in `fixtures/driver-layers.json` (rows of the form `:199`, `:207`), and so does a change of meaning of a state key (`:1189`).
- The judgment census counts units per FUNCTION (`judgment-census.json:860-874`: `reword`, `declare_repeat`, `main`, `_refuse` ...).
  `_main_fv19` has no row, because its refusals go out through `_refuse`. A new problem line inside `_main_fv19`, `main` or `reword` therefore
  adds no unit. The cards add no census row; if the scan says otherwise, that is a STOP.
- `question_count` (`report_facts.py:2399-2412`) counts every register row except `with_designer`. Its one caller is `retro_numbers.py:2225`.
  Fixture rows: `test_report_facts.py:4428-4433` (slow). `test_retro_numbers.py:346-408` (`test_fv19_retro_lists_merged_questions`, fast)
  already builds a 4-row register and merges Q16, Q17 and Q18 into Q7 (`:358-374`).
- P6 crash window (verified):
  - Case carrier: `rewords_for_case` -> `reword` writes the readiness file (`question_register.py:1640-1656`); `raise_pending` writes the
    case afterwards (`critic_rollcall.py:792`).
  - Plan carrier: `QR.reword` (`planning_contract.py:3378`) runs before `_write_plan_rows` (`:3456`).
  - Handoff carrier: the form is never rewritten, so a retried finish re-runs every `rewords` item (`question_register.py:2222-2234`).
  - On replay, `reword` refuses rule 3 (`:1603-1605`, the bytes changed) and rule 6 (`:1627-1628`, "nothing changed").
- The sibling count sites of P4 are already safe: `question_stop.over_threshold` (`question_stop.py:251`), `batch_text` (`:495`, `:499`) and
  `settle_role_questions` (`driver_stage_plan.py:933`) all go through `QR.is_open`/`QR.settled`, which hide a merged repeat.
  `report_facts._questions` skips it (`report_facts.py:2646-2650`).

## §2. Cards

Common to every card:
- given: `ai-packages/qa-factory/design/factory-rules.md` (whole); `plans/builder-rules.md`; `design/architecture.md` (the AR rows named);
  `docs/TESTING.md`; this file (§1 and the card); the spec §3 D3/D4 (lines 207-294).
- handoff: a report under `docs/tasks/specs/reports/` in the builder's tree. Form: rule 7 of `.claude/agents/builder.md`, with the FR walk of
  the touched sections.
- Witness scope: the fast files that `scenario_walk.py --witness-for <owns>` prints, run as `python -B <file>`. Slow files are only named as
  "judged by the batch canon". No CI run, no CI wait, no mutation pass (PROJECT.md п. 13; builder-rules 7b).
- No change to `references/conductor.md` (11897 bytes, cap 12000), and no cap or ratchet raise. `judgment-census.json` is untouched.

### Card A — P1: the reword/repeat refusal lines reach the role that wrote them, at its next session  [builder -> topic critic]

given: the common list; `driver_dispatch.py:602-722` (`run_role`), `:1730-1739`, `:2705-2729`; `driver_stage_plan.py:641-651`, `:749-772`,
`:871-886`; `driver_gates.py:583-610`; `critic_rollcall.py:739-796`, `:1187-1202`; `question_register.py:2181-2235`;
`planning_contract.py:3389-3462`; `fixtures/driver-layers.json:199-207`, `:1189`; `tests/test_gate_question_form.py:760-900` (how a `Driver` is
built with `__new__`).
owns:
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-ta\ai-packages\qa-factory\scripts\driver_dispatch.py (`run_role`: the prompt lines and the point after `_write_json(saved, result)` only; `s3_project`; NEW `tell_next_session`; NEW `next_session_lines`; NEW `forget_told`)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-ta\ai-packages\qa-factory\scripts\driver_stage_plan.py (`s4_after_critic`; `stage_acceptance_write`; NEW `cases_with_question_entries` — only if F-4 = include)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-ta\ai-packages\qa-factory\scripts\driver_gates.py (`raise_move` only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-ta\ai-packages\qa-factory\scripts\tests\fixtures\driver-layers.json (rows for the new methods; the note of the `question_pass_lines` key)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-ta\ai-packages\qa-factory\scripts\tests\test_gate_question_form.py (new rows only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-ta\ai-packages\qa-factory\changelog.d\fv1-9-tail-told-lines.md

non-goals:
- No change to `critic_rollcall.py`, `question_register.py` or `planning_contract.py`: their outputs are already right, they just have no reader.
- No change to `question_resume_prompt` or to the dispatch-keyed entries of `question_pass_lines` (H36 stays as it is).
- No new conductor call, no retro line (F-3), no cut of any line, no change to `references/*.md`.
- No skill-road change (P3).

What to build:
1. Store (F-1 (b)). The state key `question_pass_lines` stays, with the same shape `{key: [lines]}`. A NEW key form
   `next:<stage>:<role>` holds lines for the NEXT session of `role` at `stage`, whatever dispatch it gets.
   - `tell_next_session(stage, role, lines, tail)` appends `f"{line} ({tail})"` for each non-blank line that is not already stored under that
     key (exact-string dedupe: a replay stores nothing twice). It prints `note: {stage} {role}: {line}` for each NEW line, then calls
     `save_state()` once.
   - An empty or all-blank `lines` writes no key, prints nothing and does not save.
2. Reader. `next_session_lines(stage, role) -> list` returns `[]` when the key is absent or empty, and otherwise
   `[TR1, *("- " + l for l in stored)]`. It reads only; it does not pop. TR1 (role-facing, verbatim): "Code did not carry out these
   question entries from your earlier work; nothing was changed for them, and each line says why:".
   - `run_role` adds `told = self.next_session_lines(stage, role)` to `lines` right BEFORE `lines += list(extra)` (`:704`).
   - After `_write_json(saved, result)` (`:716`), and only on that branch, `run_role` calls `forget_told(stage, role, told)`.
     `forget_told(stage, role, sent)` removes from the key exactly the stored lines that were sent (lines added meanwhile stay), drops an
     emptied key, and saves.
3. Carriers.
   - `s3_project`: right after `planned = PC.project_plan(...)` and BEFORE the `if planned.problems` refusal:
     `self.tell_next_session("S3", self.stages()["S3"]["roles"][0], planned.notes, "it stays on your plan row and is tried again when S3
     closes next; remove it if it no longer holds")`.
   - `s4_after_critic`: capture `code, out` of the `critic_rollcall.py` call (`:761`). Parse the output with the slice expression of §1.2.
     Lines = `result.get("question_notes") or []`. Then `self.tell_next_session("S4", "qa-case-designer", lines, "it stays in your case and
     is tried again when S4 closes next; remove it if it no longer holds")`. All of this happens BEFORE `self.pin_cases()` and before the
     `self.rework(...)` at `:766`.
   - `raise_move` (`driver_gates.py:595`): the same parse and the same call, stage "S4", role "qa-case-designer", same tail.
   - `stage_acceptance_write`: capture `code, out` of the `question_register.py --raise --from-handoff` call. Lines =
     `result.get("reword_problems") or []`. Then `self.tell_next_session(stage, self.stage_acceptor(stage), lines, "an item of a handoff
     form is not tried again: write it again in your next form if it still holds")`. This sits BEFORE the `stage_done.py --acceptance` call.
   - If the output cannot be parsed (no `{...}` that `json.loads` reads as an object), tell ONE line to the same role: "the factory could not
     read what this step reported, so whether your question entries were carried out is not known; look at them in your work".
4. F-4 (include, per the recommendation). NEW `cases_with_question_entries()` in `driver_stage_plan.py` returns the case stems whose front
   matter holds a non-empty `question_repeats` or `reword_questions` line. It reads through `contract.case_files` and
   `contract.front_line(text, key)`, the readers `raise_pending` relies on; a structural key read, not a phrase (FR-12). It returns `[]` on
   any read error, as `unraised_cases` does. The trigger at `:759` becomes
   `if fixes or self.unraised_cases() or self.cases_with_question_entries():`.
5. `driver-layers.json`: one method row per new method, home `driver_dispatch` (or `driver_stage_plan` for item 4), in the form of `:207`.
   The note of the `question_pass_lines` key (`:1189`) gains: "; `next:<stage>:<role>` keys: lines for the role's next session, written by
   tell_next_session (carriers: s3_project, s4_after_critic, raise_move, stage_acceptance_write), read by next_session_lines in run_role,
   removed by forget_told after the session's result is saved".

edges (each with the invariant it protects):
- Empty notes / empty `question_notes` / no `reword_problems` key (a form with no `rewords` item has no key, `question_register.py:2222`):
  nothing stored, no TR1. Invariant: no header without a line (AR-23).
- Output that cannot be parsed: one "not known" line. Invariant: an unknown is said, never taken as "nothing refused" (AR-28, FR-41).
- A replay (crash, retried finish) produces the same line again: it is stored once. Invariant: a role reads each refusal once per pending
  state.
- `forget_told` timing (TEMPORAL with F-2): lines leave the store only after the session's result is on disk. A crash during the session, a
  `run_claude` that raises, or a reused saved result (`:717-718`, no session ran) leaves them in the store. Invariant: the allowed error is
  to tell twice; losing a line is forbidden.
- POSITIONAL:
  - `s3_project` tells before raising on `planned.problems`. Invariant: a projection problem never swallows the notes.
  - `stage_acceptance_write` tells before `stage_done --acceptance`. Invariant: a refused acceptance write never loses the lines.
  - `s4_after_critic` tells before `rework`. Invariant: the round the critic sends back hears the lines in its first prompt.
  - `run_role` puts the lines before `extra`. Invariant: the "Plugin root" and HANDOFF_FORM lines stay last, unchanged.
- TEMPORAL (both worlds):
  - A driver state from before this card has no `next:` key, so every prompt is byte-identical to today's. Proof row:
    `next_session_lines` returns `[]`.
  - The first `tell_next_session` creates the new world. `question_resume_prompt` pops only its own dispatch key, and a dispatch id
    (`S2-qa-requirements-tester-2` form, `fixtures/stories/local-1-arm-b/state/driver-state.json:135`) never starts with `next:`. Invariant:
    the two key forms never collide.
- A role that never runs again: its lines stay in `driver-state.json`; they were printed as `note:` at the time (F-3).
- Size: no cut (FV1-4, FR-49). Each line is the carrier's own text, whole.
- Conflicting pair: the handoff tail says "not tried again", while the replay of a retried finish does re-run the item. With card B the
  replay is "done" and no line is made. Without B a replay line could tell the acceptor that a reword failed when it was in fact applied.
  That is why B goes before or with A (§4).
- Who is the receiver: the stage key and role come from the carrier's own call site (S3 planner from `stages()["S3"]["roles"][0]`, the S4
  designer by the literal its function already uses at `:766`, the acceptor from `stage_acceptor(stage)`). No role name is added to a list
  (AR-1).

siblings:
- The skill road (axis 5): `phases/s4.md` runs `critic_rollcall` and the orchestrator reads its stdout JSON itself, so n/a here. P3 stays queued.
- `driver_gates.raise_move` is in owns (the second caller of the same command).
- `question_resume_prompt` is n/a: a resumed session always follows a `run_role` start of the same dispatch, which already carried the lines.
- Axis 13 / axis 33 n/a: no dispatch id is guessed; the key is by role.

DoD rows (`test_gate_question_form.py`, one parameterised function per behaviour):
- `fv19_told_next_session_store` (table):
  - notes -> key `next:S3:<planner>` holds the lines with their tail, plus `note:` prints;
  - empty -> no key and `save_state` not called;
  - the same line twice -> stored once;
  - two roles -> two keys.
- `fv19_told_lines_in_prompt` (table on `next_session_lines` + `forget_told`):
  - none -> `[]`;
  - lines -> TR1 first;
  - another stage or role -> `[]`;
  - `forget_told` removes the sent lines and keeps a line added after the read;
  - the key is gone once emptied.
- `fv19_carriers_tell` (table, `Driver.__new__`, `py` stubbed to return the real JSON shapes of `critic_rollcall.py:1201` and
  `question_register.py:2439`):
  - `s4_after_critic` with `question_notes` -> designer key; with none -> no key; with output that is not JSON -> the one unknown line;
  - `stage_acceptance_write` with `reword_problems` -> acceptor key, written before the acceptance call (call order recorded by the stub);
  - `s3_project` with notes and problems -> the key is written and then the Refusal is raised;
  - `raise_move` -> designer key.
- `fv19_s4_trigger_reads_entry_keys` (F-4; table): a case with only `question_repeats` -> listed; only `reword_questions` -> listed; neither
  -> `[]`; an unreadable case file -> `[]`.
- The `run_role` wiring (the lines enter the prompt; removal only after `_write_json`) is judged by the slow `test_story_run_*` files and by
  `test_driver_layers.py` (map rows) in the batch canon: name them in the report as "judged by the batch canon".

DoD:
- `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/driver_dispatch.py ai-packages/qa-factory/scripts/driver_stage_plan.py ai-packages/qa-factory/scripts/driver_gates.py ai-packages/qa-factory/scripts/tests/fixtures/driver-layers.json`
  then run the fast files it prints, at least `python -B ai-packages/qa-factory/scripts/tests/test_gate_question_form.py`.
- `python -B ai-packages/qa-factory/scripts/selftest.py --lang` (the new texts are English, FR-30).
- `python -B ai-packages/qa-factory/scripts/tests/test_console_encoding.py` (the new `note:` prints, builder-rules 7b).
- grep `question_pass_lines` in `scripts/*.py`: the writers are the three existing sites plus `tell_next_session`; the readers are
  `question_resume_prompt`, `next_session_lines` and `forget_told` only (AR-13).
- The changelog fragment names the class.

architecture: AR-22 -- the three carriers' refusal lines get a reader (the writing role's next prompt); AR-10 -- a role told of a key (N3)
hears its refusals; AR-15/AR-18 -- one store (`question_pass_lines`), one reader function, no second transport; AR-13 -- one reader; AR-14 --
one writer of the key (driver_dispatch); AR-28 -- unparseable output is an unknown line; AR-1 -- no role list added. Change check:
`test_driver_layers.py` rows (canon) and the grep above.
judgment: none -- a transport of code's own refusal texts; whether to rewrite an entry stays the role's.
Checks added, census class, owner: none is a refusal. `cases_with_question_entries` is a presence read (data, code); it is not a census unit,
because it refuses nothing and only decides whether to run a carrier.
Hot file `driver_dispatch.py`: function list `run_role` (prompt lines + post-save point), `s3_project`, `tell_next_session`,
`next_session_lines`, `forget_told` (D-0048).

### Card B — P6: a reword that already stands is done on replay  [builder -> topic critic]

given: the common list; `question_register.py:1573-1665` (`reword`), `:1700-1784` (carriers), `:2181-2235`; `planning_contract.py:3351-3386`;
`critic_rollcall.py:776-795`; `tests/test_question_register.py:2560-2720` (the `fv19_reword_*` and carrier rows).
owns:
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-tb\ai-packages\qa-factory\scripts\question_register.py (`reword` only; its docstring)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-tb\ai-packages\qa-factory\scripts\tests\test_question_register.py (new rows only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-tb\ai-packages\qa-factory\changelog.d\fv1-9-tail-reword-replay.md

non-goals:
- No change of write order in any carrier (F-5 (c) is rejected below).
- No change to the carriers, `declare_repeat`, the CLI output shape or `reworded[]`'s shape.
- No re-carrying of repeats on the no-op path.

What to build (F-5 (b)): `reword` gets a REPLAY rule.
- Placement: after the register checks (`_unusable_register`, no such id; both still refuse) and after `spec`/`text`/`given` are parsed, and
  BEFORE every other check (status, showing, who-may, readings frozen, `why`, nothing-changed, shape).
- `produced = [r["was"] for r in reworded[1:]] + [current question]` when the row's `reworded` is a non-empty list; otherwise `[]`.
- The entry is DONE when `_squeeze(text)` equals `_squeeze(p)` for some `p` in `produced`, AND, when `readings` is given and the match is
  the current question, `[_squeeze(x) for x in given] == [_squeeze(x) for x in _reading_texts(row)]`.
- A match in the history (an earlier reword's result) compares the question only.
- DONE returns `load(root)`'s current row. It writes nothing: no lock, no `_write_readiness`, no repeat re-declaration.
- The docstring gains one sentence: "A reword whose words already stand, or stood as the result of an earlier reword, is done: nothing is
  written (a replay after a crash)."

edges (invariant per row):
- Allowed error: an entry is treated as done when its words stand, even if another party (the conductor, another role) wrote them; the
  person sees exactly the requested words. Forbidden: dropping an entry whose words do NOT stand now and never stood as a reword result.
- Same text as the ORIGINAL wording, with no reword history -> NOT done; refused "nothing changed" as today. Invariant: the replay rule
  never turns a no-op request into a success.
- Replay after the person answered the reworded row -> done, not "answered". Invariant: a carried-out reword never sticks in the key.
- Replay when the register cannot be read, or the id is gone -> refused as today.
- Whitespace-only differences -> equal (the same `_squeeze` as the nothing-changed rule; bytes, not meaning, AR-29).
- `readings` given and different while the question is equal -> not done, so the normal checks run.
- A crash after the readiness write but before the repeats are re-declared (`:1658-1664`): the replay does not re-carry them, so they show
  again (`target_changed`). ACCEPTED toward asking, the same direction as the existing `except Refused: continue`.
- POSITIONAL: the rule sits before the showing check (rule 3). Otherwise a replay is refused forever "not shown", because its own write
  changed the bytes; that is exactly the defect.
- Adversarial: the entries are role- or conductor-written, so the shape battery stays `reword_entry`'s (N1). No new outside input is added.

siblings:
- `declare_repeat`'s replay (`spec §3 D3 step 2`, "already a hidden repeat of the same target -> no-op") is the same shape, already there.
- All three carriers get the fix through the one writer (AR-15): the case and plan entries are dropped, and a handoff item replay lands in
  `rewords`, not in `reword_problems`.

DoD rows (`test_question_register.py`, one table `fv19_reword_replay_is_done`):
- (a) the same spec twice with no new showing -> the second returns the row, `len(reworded) == 1`, readiness bytes unchanged;
- (b) after an answer on the reworded bytes -> done;
- (c) `rewords_for_case` run, the case text NOT written, run again on the original text -> entry dropped, `problems` == [];
- (d) `planning_contract._reword_plan_entries` twice on the same rows -> the second leaves no key and no note;
- (e) `raise_from_handoff` twice -> the second has the id in `rewords` and an empty `reword_problems`;
- (f) the spec equal to the original text with no history -> refused "nothing changed";
- (g) a spec differing from the current text and from the history -> refused "not shown" (unchanged);
- (h) readings given and equal -> done; readings differ -> not done;
- (i) text1 applied, a new stop shows it, text2 applied, then text1 replayed -> done (history) and the question still reads text2.

DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/question_register.py`, then
the fast files it prints, at least `python -B ai-packages/qa-factory/scripts/tests/test_question_register.py`. Also
`python -B ai-packages/qa-factory/scripts/tests/test_judgment_census.py`: unchanged; any other count is a STOP, returned as a question.
architecture: AR-25 -- the "not carried out" state of an entry has a way out after a crash; AR-14 -- one writer; AR-15 -- fixed at the
writer, all carriers. Change check: rows (c)-(e).
judgment: none -- byte equality of texts (data).
Checks altered, census class, owner: `reword`'s refusal unit is unchanged (xref, data). The replay predicate is shape (byte equality),
owner data (code), and no new unit.
Hot file: `question_register.py` is not on the hot list; function `reword` only (disjoint from card C's `main`/`_main_fv19`).

### Card C — P2 + P5: the conductor's `--repeat` door in the hand-over, both doors with `--task`/`--stage`, and `--stage` accepted  [builder -> topic critic]

given: the common list; `driver_dispatch.py:1818-1906`; `question_register.py:2293-2440`; `contract.py:5848-5859`; `retro_numbers.py:2840-2850`;
`references/question-vocabulary.json:1-20`; `tests/test_question_register.py` (`fv19_cli_repeat_reword_note`, near `:2700-2720`);
`tests/test_gate_question_form.py:760-900`.
owns:
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-tc\ai-packages\qa-factory\scripts\question_register.py (`main`: the `--stage` guard `:2423-2424` and the `--stage` help `:2390`; `_main_fv19` and its docstring)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-tc\ai-packages\qa-factory\scripts\driver_dispatch.py (`register_words_to_conductor` only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-tc\ai-packages\qa-factory\scripts\tests\test_question_register.py (new rows only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-tc\ai-packages\qa-factory\scripts\tests\test_gate_question_form.py (new rows only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-tc\ai-packages\qa-factory\changelog.d\fv1-9-tail-conductor-doors.md

non-goals:
- No row in `conductor.md` (cap).
- No `--stage` for `--note` (a note has no stage field).
- No change to `ROLE_QUESTION_STAGES` or to the `--raise --from-handoff` road.
- No conductor door to split a merge (owner 14.11, B2).

What to build:
1. P5, CLI.
   - The guard becomes: `--asked-by` and `--from-handoff` go with `--raise` only; `--stage` goes with `--raise --from-handoff`, `--repeat`
     or `--reword`. The refusal text names that.
   - In `_main_fv19`, with `--note`: a given `--stage` joins `stray` ("has no meaning with --note").
   - With `--repeat`/`--reword`: `stage = ns.stage.strip()`. Blank -> `""` (as today). Non-blank and `_contract()._stage_entry(stage) == {}`
     -> a problem line "stage '<v>' is not a stage of the factory. Valid: <ids of stages.json in order>". Otherwise pass `stage=stage` to
     `declare_repeat` and `reword`.
   - The docstring drops "the stage is not known".
2. P2, text. In the `recorded is not None` block of `register_words_to_conductor`:
   - (a) the answer sentence gains `--task {self.task}` after "with" (`:1855`: `with --task {self.task}, --words-file, ...`; this is the
     sweep neighbour, the CLI requires `--task`);
   - (b) the reword sentence becomes, verbatim: " A question their words show they could not tell what it asks is reworded with
     `question_register.py --task {self.task} --reword QID --question-file <file> --by conductor --where \"{stage} stop\" --stage {stage}`;
     the file is JSON with `question`, `why` and optionally `readings`.";
   - (c) NEW right after it, verbatim: " When their words say two of these questions ask the same thing, the later one is merged into the
     earlier with `question_register.py --task {self.task} --repeat QID --same-as QID --words-file <file> --by conductor --where \"{stage}
     stop\" --stage {stage}` (the file holds one line: why both ask the same); the person is then asked once, under the earlier id, and the
     merge is refused while a plan row or a case still rests on the later id."

edges:
- `--stage` is outside input (the conductor's command line), so the mini-battery applies: absent, `""`, `"  "` -> `""` recorded; `S3`; `" S3 "`
  -> `S3`; `s3` (case) refused; `S10`, `gate A` refused; a 10 000-character value refused, with the value shown cut to its first 80
  characters in the refusal; non-ASCII `С3` (Cyrillic) refused. A value with a newline is refused (no id contains one).
  Invariant: only a stage of `stages.json` is ever stored as `stage`.
- `--stage` with `--note`, `--answer`, `--show`, or `--raise` without `--from-handoff` -> refused as today, plus the `--note` stray line.
  Invariant: no operation silently ignores a flag (FR-1).
- TEMPORAL: a conductor following an older hand-over (no `--stage`) still succeeds and records `""`, and the retro says "an unrecorded
  stage" (unchanged). The new world starts with the first hand-over text this card prints.
- POSITIONAL: all three sentences stay inside the `recorded is not None` block and before `## The question` (the function's own POSITION
  INVARIANT, `:1823-1824`). The `s1_review` and `recorded is None` texts are unchanged.
- FR-2: every flag a door sentence names is accepted by `question_register.main` after item 1. Proved by the CLI row below, with the flags
  exactly as the sentences name them.
- `{stage}` is always one of S2/S3/S4 here (§1.4), so `--where "{stage} stop"` and `--stage {stage}` are always valid values.

siblings:
- `driver_gates.conductor_text` T10 already prints `--task {self.task}` (fix round F5). Covered.
- `conductor.md:35` (the `--operation` form) is not touched.
- The skill road has no door (P3, queued).

DoD rows:
- `test_question_register.py`, `fv19_cli_stage_on_repeat_and_reword` (table, the CLI through `main([...])` as the existing
  `fv19_cli_repeat_reword_note` row does):
  - `--repeat ... --stage S3` -> exit 0 and the record's `stage` == "S3";
  - `--reword ... --stage S4` -> `reworded[-1].stage` == "S4";
  - no `--stage` -> "";
  - each battery value above -> refused (exit 2) naming the valid ids, or recorded as stated;
  - `--note ... --stage S3` -> refused, "no meaning with --note";
  - `--answer ... --stage S3` -> refused, with the new guard text.
- `test_gate_question_form.py`, `fv19_handover_names_the_doors` (table, `Driver.__new__` with `unread` capturing the text and
  `apply_question_answers` stubbed):
  - kind `questions` at S3 and kind `halt` at S4 -> the text holds sentences (b) and (c) with `--task T-1`, `--where "S3 stop"` (or S4) and
    `--stage S3` (or S4), and the answer sentence with `--task T-1`; every one sits before `## The question`;
  - `recorded=None` -> none of the three (control).

DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/question_register.py ai-packages/qa-factory/scripts/driver_dispatch.py`,
then the fast files it prints, at least `python -B ai-packages/qa-factory/scripts/tests/test_question_register.py` and
`python -B ai-packages/qa-factory/scripts/tests/test_gate_question_form.py`. Also `python -B ai-packages/qa-factory/scripts/selftest.py --lang`
and `python -B ai-packages/qa-factory/scripts/tests/test_judgment_census.py` (unchanged; another count is a STOP).
architecture: AR-10 -- the conductor is told the `--repeat` door where the person's words call for it; AR-9/FR-2 -- every named flag is
accepted; AR-22 -- `stage` on a conductor's repeat/reword record now has a producer; AR-13/AR-1 -- the stage vocabulary is read from
`stages.json` through its one reader, not a code list; AR-17 -- the one hand-over seam, no second text.
judgment: none -- the conductor still judges sameness and clarity; code checks the stage id against data.
Checks added, census class, owner: the `--stage` value check in `_main_fv19` is xref (a value of `stages.json`), owner data (code), refused
through the existing `_refuse` unit, so no new census unit. The guard change in `main` is shape (`main`'s existing unit).
Hot file `driver_dispatch.py`: function `register_words_to_conductor` only (disjoint from card A).

### Card D — P4: the retro's question count counts a merged question once  [builder -> topic critic]

given: the common list; `report_facts.py:2399-2412`; `question_register.py` `hidden_repeat` (via `QR`); `retro_numbers.py:2215-2230`;
`tests/test_retro_numbers.py:346-408`; `tests/test_report_facts.py:4418-4435`.
owns:
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-td\ai-packages\qa-factory\scripts\report_facts.py (`question_count` only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-td\ai-packages\qa-factory\scripts\tests\test_retro_numbers.py (rows inside `test_fv19_retro_lists_merged_questions` only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-9-td\ai-packages\qa-factory\changelog.d\fv1-9-tail-question-count.md

non-goals:
- No count of showings (F-7 (b)), no change to `question_count_line` or to the report's open-questions section, no change to
  `test_report_facts.py` (slow; its FL-8 F1 rows keep their meaning).

What to build (F-7 (a)): `question_count` excludes a row when `q.get("status") == "with_designer" or QR.hidden_repeat(q)`. `QR.hidden_repeat`
is the one predicate. The docstring gains: "and a question merged into another one (`QR.hidden_repeat`): the person is asked it once,
under the earlier id".

edges:
- An unresolved repeat (gone, cycle, target changed, own words changed) is shown, so it is counted. Invariant: the allowed error is
  over-counting; counting a merged twin as a second question is forbidden.
- A merged question the person answered anyway -> status `answered` -> counted (P13: their word stands).
- No register, unreadable, or empty -> unchanged (`unmeasured` / measured 0).
- TEMPORAL: a story with no `repeat` record counts exactly as before.
- The count is still "questions put to the person" in the register sense, not "showings". A showing count has no producer (spec D1, B3(e)).
  F-7 records this; it is not a silent narrowing.

siblings: the threshold count, `batch_text` and `settle_role_questions` already hide merged repeats through `is_open`/`settled` (§1.4). The
report's `_questions` skips them (N2). No other count site was found among the `with_designer` exclusion sites (Grep, §7).

DoD rows (`test_retro_numbers.py`, inside `test_fv19_retro_lists_merged_questions`; the register already holds Q7, Q16, Q17, Q18):
- `report_facts.question_count(troot)` == 4 before the merges (after `:360`);
- == 1 after the three merges (after `:374`);
- after `QR.record(... "Q18", "open" ...)` (`--reopen` road) == 2.

DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/report_facts.py` (it prints
`test_report_facts.py` etc.; the slow ones are "judged by the batch canon"), and `python -B ai-packages/qa-factory/scripts/tests/test_retro_numbers.py`
(the owned test file, fast).
architecture: AR-13 -- one predicate `hidden_repeat`; AR-12 -- the retro measurement counts what the person is asked; AR-27 -- a merged
question reaches the retro under its target. Change check: the three rows.
judgment: none (a count).
Checks added: none.

## §3. Forks (options, recommendation, cost)

- **F-1 (P1 transport).**
  - (a) The Lead's literal road: dispatch-keyed `question_pass_lines` + `question_resume_prompt`. Not workable: the carriers run after the
    writing dispatch's only stop, and nothing resumes it (§1.1), so the lines would never be read.
  - (b) RECOMMENDED: the same store, a `next:<stage>:<role>` key, one reader in `run_role` (the one assembly point of every fresh and rework
    prompt). Cost: about 40 lines; an edit to a hot function (`run_role`, two points); 3 driver-layers rows; 4 fast test rows. It keeps
    "one store, one road" and adds no new state key.
  - (c) The rework `extra` of the same function only. Cheaper, but it loses the S3 notes and the acceptor's lines (no same-function rework)
    and is not crash-safe.
  - (d) The conductor through `settle_role_questions`. Wrong receiver: the role wrote the entry. It pays a conductor call for mostly-timing
    refusals ("not shown yet"), which is FR-55 friction.
- **F-2 (when told lines leave the store).**
  - (a) RECOMMENDED: after the session's result is saved (duplicate rather than lose).
  - (b) At prompt build, as H36 does. Simpler, but loses the lines if the session crashes. (a) differs from H36's pop. H36 is left alone
    (dispatch keys, resume road); aligning H36 is a queue line, not this card.
- **F-3 (lines whose role never runs again).**
  - (a) RECOMMENDED: they stay in the driver state and were printed as `note:`; nothing more.
  - (b) A retro line "question entries not carried out". This adds a reader in `retro_numbers` (card D's file, other function), about 20
    lines plus a row.
  - (c) A conductor call at stage close: a paid call.
- **F-4 (the S4 trigger gap, §1.3, beyond the brief).**
  - (a) RECOMMENDED: include it in card A (same function `s4_after_critic`, same AR-22 class). Without it, card A's tail "tried again when S4
    closes next" can be false (FR-10). Cost: 1 method, 1 map row, 1 table row.
  - (b) A separate node. Then card A's S4 tail must drop "and is tried again ...".
- **F-5 (P6 replay rule).**
  - (a) Match the current text only. The simplest, but it leaves a corner: a crash, then someone else's later reword and a new showing,
    and the stale entry re-applies the old words.
  - (b) RECOMMENDED: current text + the reword history (`reworded[1:].was`). One list more; it closes the corner.
  - (c) Swap the write order (artifact before register). Rejected: a crash then loses the request silently and the role believes it was done.
- **F-6 (P5 `--stage` optional or required).**
  - (a) RECOMMENDED: optional. Older texts keep working, the retro already has an empty outcome, and no new refusal unit is added.
  - (b) Required for `--repeat`/`--reword`. A record without a stage becomes impossible, but a conductor following an older text is refused
    once.
- **F-7 (P4 meaning).**
  - (a) RECOMMENDED: exclude merged repeats at count time.
  - (b) Count actual showings. It needs a showing history that has no producer (spec B3(e)): a new mechanism.
- **F-8 (P31 / designer rule 6: P3 out).** The skill road (`phases/s2.md:108`, `phases/s4.md:222`) gets no `--note`/`--reword`/`--repeat` door
  here. The one-road option is a node with owns and a test. The alternative is an explicit n/a while the phases retire (t-301 N6), written
  into the pile with the owner's word. Recommendation: open the node (about 10 lines in two phase files plus a doc-dispatch witness) unless
  t-301 N6 retires them within this batch. The Lead takes it to the owner.

## §4. Order and N3

- A ∥ B ∥ C ∥ D. Shared files:
  - A and C: `driver_dispatch.py` (disjoint functions) and `test_gate_question_form.py` (new functions).
  - B and C: `question_register.py` (`reword` vs `main`/`_main_fv19`) and `test_question_register.py` (new functions).
  - In each pair the node that merges later merges `main` into its tree and resolves the conflict (PROJECT.md «Командная работа» п. 3,
    D-0048).
- One topic critic after the last of the four (R13-g).
- N3 (T12/T13, the keys told to the roles) may be dispatched right after **A and B** have merged.
  - A: a role told of a key must hear its refusals (AR-10, critic P1).
  - B: without it, a crash replay makes A deliver a false "not asked again", and the entries stick.
  - N3 also waits on `TQ2-1 K1 -> A2` for `agents/qa-case-critic.md` (spec §6; status not established).
  - C and D are independent of N3.
- N3 text note for the Lead: T12/T13 need no change for A; the refusals arrive by TR1 in the next session.

## §5. Out of scope: lines for the Lead's queue

- P3: skill road phases `s2.md:108` / `s4.md:222` have no `--note`/`--reword`/`--repeat` door and no T10 equivalent (axis 5). Open a node or
  record n/a until the phases retire (t-301 N6); see F-8.
- P7: split `question_register.reword` (about 93 lines, now plus the replay rule), `gate_brief._help_lines` (4 levels of nesting) and
  `question_card` (about 110 lines): validation apart from the write; a code-quality node after this tail merges (it touches card B's
  function).

## §6. Could not establish

- The branch head `ef5bdcf` of wip/fv1-9-fix: no shell was available; files were read as they stand in the worktree.
- What `scenario_walk.py --witness-for` prints for each card's owns: not run (no shell). The DoDs name the command; the fast files named in
  them come from `test-layers.json` covers and `slow_tests.json` (measured 2026-11-12).
- The status of stage-critics A2 / TQ2-1 K1: Grep over `plans/piles` found no A2 row of that topic.
- Whether an N3 worktree exists: Glob does not walk `.claude/worktrees` (the positive control on the fix tree also returned nothing, so the
  tool is the limit, not the tree).
- The meaning of the `"row"` field in `driver-layers.json` method rows: card A tells the builder to copy the form of `:207`, and the layer
  test (canon) judges it.
- Whether `question_register.py --from-handoff` writes anything to stderr beside its JSON: the slice parse plus the unknown line cover both
  cases.

## §7. Small choices closed by the designer

- The fast homes for the rows: `test_gate_question_form.py` (A, C), `test_question_register.py` (B, C), `test_retro_numbers.py` (D, where a
  merged register already exists). These are keep rows; no new file.
- The tails passed per call site, rather than a code dict of carrier kinds (AR-1).
- The planner role read from `stages()["S3"]["roles"][0]` (precedent `stage_S2` `driver_stage_plan.py:586`).
- The JSON parse uses the existing slice expression (`driver_gates.py:331`), not a new helper.
- `--task` added to the answer sentence too (the sweep neighbour in the same block; no test pins it, per the §1.4 grep).
- The stage value is stripped; the case is exact; the valid list comes from `stages.json` in its order.
- The P6 no-op returns the current row (the CLI output shape is unchanged).

## §7a. Lead decisions (14.11.2026, owner away: by recommendation, reversible, in the morning report)

- F-1 (b) `next:<stage>:<role>` key read in `run_role` (the Lead's dispatch-keyed road is withdrawn: §1.1 shows no reader).
  F-2 (a). F-3 (a). F-4 (a) inside card A. F-5 (b). F-6 (a). F-7 (a).
- F-8: P3 becomes a queue line with an owner question (open the node vs n/a until the phases retire); not built tonight.
- Base: the cards were read on wip/fv1-9-fix; that tree is in `main` since 9c15423 — every card starts from origin/main and
  merges it again before its report. Topic "stage critics removed" (A1b, not yet in main) deletes `stage_critic_route` /
  `stage_critic_completion` next to card A's `stage_acceptance_write`: the later of the two merges resolves it.
- Card D is dispatched now (one predicate in one count). Cards A, B, C go through ONE plan critic first: B moves a rule in
  front of `reword`'s refusals, A adds a state-key form and edits `run_role`, C widens a CLI guard.

## §7b. BINDING amendments after the plan critic (t-728, `docs/tasks/specs/reviews/20261114-fv1-9-tail-plan-critic.md`)

All cards: line numbers in this file are wip/fv1-9-fix's; anchor by FUNCTION NAME and quoted text on origin/main. Slow files
named in a DoD (`test_judgment_census.py`, `test_console_encoding.py`, `test_driver_layers.py`, `test_story_run_*`) are NOT run
by the builder: "judged by the batch canon".

Card A (dispatched after topic "stage critics removed" A1c is in main — both edit `driver_stage_plan.py`):
1. A-1: in `stage_acceptance_write` the acceptor's lines are keyed by the stage of the acceptor's OWN dispatch record
   (`controller_state()["dispatches"][dispatch]["stage"]`, falling back to `stage`), not by the accepted stage; the tell sits
   INSIDE the function's `try/except Refusal`. Row: S7 accepted by `qa-doc-scribe` -> read by its S8 session.
2. A-2: `forget_told` runs only when the saved result carries words (`str(result.get("result") or "").strip()`, the
   `resume_role` rule); a dead or empty result keeps the lines (row).
3. A-3: a parsed `critic_rollcall` object with an `errors` list adds the unknown line (row `{"errors": ["raise_questions: X"]}`).
4. A-4: named edge — a refusal resume of the same dispatch does not carry the lines; the next `run_role` does (no second reader).
5. A-5/A-7: an empty role stores nothing (prints the `note:` lines only); `forget_told` with nothing sent neither writes nor saves.
6. A-6: owns gain `design/state-exits.md`: one driver-state row for `question_pass_lines`, both key forms (dispatch key: popped
   by `question_resume_prompt`; `next:<stage>:<role>`: removed by `forget_told` after the role's next saved session with words;
   terminal and inert when the role never runs again, already printed as `note:`).
7. A-8: `raise_move` parses and tells on exit 0/1; on any other exit it tells the unknown line BEFORE `RepairFailed`. No
   `check=True` is added at either `critic_rollcall` site; exit 1 stays legal.
8. A-9: `cases_with_question_entries` lists a case when `contract.parse_json_list(front_line(...))` is a non-empty list OR the key
   is malformed; it reads through `contract.case_files` (the reader `unraised_cases` uses).
9. A-10: gate A's repair trigger is n/a: with F-4 the entries run at every S4 close, gate A meets refused leftovers only.
10. A-11: TR1 = "Code did not carry out these question entries from your earlier work, or could not tell whether it did; each
    line says which and why:".
11. T-1/T-2: the store and reader tables fold into `fv19_carriers_tell` (each carrier row asserts through
    `next_session_lines(<receiving stage>, <role>)` and `forget_told`); ONE row is added to an existing `test_story_run_*`
    scenario that drives an S4 rework (the rework prompt holds TR1 and the line; the store is empty after the session) — slow,
    judged by the canon.
12. One private helper `told_from(out, keys) -> list` in `driver_dispatch` for the three parses (lines, or the unknown line, or
    the `errors` lines).
13. `plan_notes` of the `critic_rollcall` object is told the same way to the S3 planner's key (same carrier, same class);
    `skipped`, `repeats`, `rewords`, `raised`, `applied` are n/a (successes / gate A's own finding).

Card B:
1. B-1: a HISTORY match counts only when the entry that PRODUCED that text (`reworded[k]` for the text `reworded[k+1].was`, the
   last entry for the current text) has the caller's `role` and the same `_squeeze(why)` as the request; otherwise the normal
   checks run. Direction sentence corrected: a history match drops only the same party's replayed entry. Row (j): text1, then
   text2 by another party, then text1 again with a NEW `why` -> not done.
2. B-2: row (k): reword once, then ask for the ORIGINAL text -> not done.
3. B-3/B-4: readings are compared only when `given` is a list (otherwise the replay rule does not apply and the shape check
   refuses as today); a `reworded` element that is not an object or has no string `was` is skipped, never raises.
4. Rows (f), (g), (h-second half) are labelled CONTROLS.

Card C:
1. C-1: no `_main_fv19` stray item for `--note`; the `--note --stage` row expects the guard's text.
2. C-2: the stage is validated through `acceptance.stage_def_of(stage)`; the valid list in the refusal is
   `null_outcomes.stage_ids()` sorted by the number after `S`; no new reader of `stages.json`, `contract.py` untouched.
3. C-3: an unreadable stage table refuses a non-blank `--stage` with "the stage table could not be read"; a blank still records "".
4. C-4: the same value check applies to `--raise --from-handoff --stage` (one rule for the flag on all three operations).
5. C-5: `--where` validated and then dropped by `declare_repeat` / `reword` is NOT carried here: queue line, owner the FV1-9 Lead.
6. C-6: sentences (a)-(c) name the script as the `--show` door does: `python {self.scripts / 'question_register.py'}`.

Queue (Lead): H36 removal after a saved result and `question_rework` reading the dispatch key (critic key 11 (a)); C-5 `--where`.

## §8. Reading trail

- Read whole: the topic critic review; the fix report.
- Spec: §3 D1-D8, §4, §5 N1-N5, §6 (lines 183-627); Grep of headings and forks.
- `driver_dispatch.py`: 602-722, 735-794, 1596-1906 (parts), 1928-1942, 2680-2770.
- `driver_stage_plan.py`: 470-680, 749-886, 921-960.
- `driver_gates.py`: 578-605.
- `critic_rollcall.py`: 739-796, 1160-1219.
- `question_register.py`: 1573-1802, 2181-2250, 2293-2537.
- `planning_contract.py`: 3351-3475.
- `report_facts.py`: 2395-2474, 4140-4174.
- `question_stop.py`: 240-264, 488-512.
- `contract.py`: 5846-5863. `acceptance.py`: 1284-1293. `driver_conductor.py`: 90-115.
- `slow_tests.json` (whole); `test-layers.json` (header, the keep rows of `test_gate_question_form`, `test_question_register`,
  `test_retro_numbers`, plus a Grep of file/covers lines).
- `test_retro_numbers.py`: 300-408. `test_report_facts.py`: 4410-4439.
- `judgment-census.json` (Grep `question_register`); `driver-layers.json` (Grep).
- `SIBLING_MAP.md` headings, axes 13, 33, 34.
- `plans/builder-rules.md` 7b.
- Greps:
  - `question_pass_lines|register_words_to_conductor|project_plan\(|reword_problems|question_notes` in `driver_*.py`;
  - `register_words_to_conductor|question_resume_prompt|question_pass_lines` in tests;
  - `--answer QID --reading|--reword QID|could not tell what it asks` in the package (control: driver_dispatch hit);
  - `with_designer` exclusion sites;
  - `apply-fixes|raise_pending|unraised_cases\(`;
  - `question_count\(`;
  - `def py\(`;
  - `json.loads\(out`;
  - `"id": "S\d"` count in `stages.json`.
- Not read: `phases/s2.md`, `phases/s4.md` (P3 is out); `story_step._prompt`; `driver_runner.py` beyond `py`'s docstring.
