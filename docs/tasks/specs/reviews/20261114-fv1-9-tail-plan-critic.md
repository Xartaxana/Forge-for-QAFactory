# Plan critic: FV1-9 tail, cards A (P1), B (P6), C (P2+P5) and the Lead's §7a decisions

Critic (Opus), ONE pass, 14.11.2026. Reviewed: `docs/tasks/specs/20261114-fv1-9-tail-cards-spec.md`, cards A, B and C plus §7a
(F-1 (b), F-2 (a), F-3 (a), F-4 (a) inside A, F-5 (b), F-6 (a), F-7 (a)). Card D is not reviewed. Nothing I read in passing puts it
against a rule.

**Code base read.** `.claude/worktrees/read-main` is at 50d9012 and does NOT contain 9c15423 (`git merge-base --is-ancestor 9c15423 50d9012`
exits 1), so I read `.claude/worktrees/fv1-9-td` (HEAD 9c15423; its only dirty paths are card D's `report_facts.py` and
`test_retro_numbers.py`). `origin/main` is 9c15423 plus two commits that touch only `gate_brief.py`.
All file:line below are 9c15423 lines.
**The spec's own anchors are stale.** They are wip/fv1-9-fix lines, and `git diff wip/fv1-9-fix 9c15423` moves `driver_dispatch.py` by about 15 lines
(`run_role` is 617-781, not 602-722; `s3_project` is 2720, not 2705; `register_words_to_conductor` is 1833). It also reshapes
`stage_acceptance_write`: it is now wrapped in `try/except Refusal` (FV1-22 N2, `driver_stage_plan.py:646-656`). Builders must anchor by
function name and text, not by number (finding G-1).

Verdict per card:
- **A: fit_with_fixes**, three of its amendments blocking (A-1, A-2, A-3).
- **B: fit_with_fixes**, one blocking amendment (B-1).
- **C: fit_with_fixes**, no blocking amendment.

Overall: **NEEDS WORK, 4 blocking findings.** Accepting the plan is the Lead's decision; this verdict is an input to it.

---

## Key 1. §1.1: the dispatch-keyed road and `run_role` as the one assembly point

**(a) A line stored under the writing dispatch's key would never be read. HOLDS.**
- `question_pass_lines` is touched at four sites only:
  - writers: `driver_dispatch.py:1689` (threshold), `:1817` (`take_question_answer`), `:1830` (after the hand-over);
  - the one pop: `:1749`, in `question_resume_prompt`.
  - Grep `question_pass_lines` over `scripts/*.py` gives exactly these four; the same grep finds the fixture key, which is its positive control.
- `question_resume_prompt` is called only from `resume_role` when `by_stop` holds (`:1074-1075`). `by_stop` needs `question_stop.resume` and
  `question_stop.dispatch == dispatch`. Both are written only at the threshold stop (`:1683`) and on its answer (`:1820`), and both happen before
  `finish` (`:775` before `:779`; `:1133` before `:1139`).
- The carriers all run inside or after `finish`:
  - `s3_project` runs inside `complete(digest)`;
  - `stage_acceptance_write` runs inside the critic's or consumer's `complete`;
  - `critic_rollcall --apply-fixes` runs in `s4_after_critic` (`driver_stage_plan.py:765-768`) and in `raise_move` (`driver_gates.py:595`).
- The refusal roads that resume the same dispatch afterwards (`resume_with` `:2213-2229`; `driver_machine.py:578`; the recovery road
  `_finish_saved_result`, `driver_machine.py:1550-1562`) never call `question_threshold` or `question_resume_prompt` (grep
  `question_threshold(`: only `:775` and `:1133`). F-1 (a) is correctly withdrawn.

**(b) `run_role` as the ONE assembly point of every FRESH and REWORK prompt. HOLDS, with a gap the card leaves silent.**
- Every `run_claude("role", ...)` call: `driver_dispatch.py:566` and `:597` (handoff resumes), `:729` (`run_role`), `:1101` (`resume_role`),
  `:2229` (`resume_with`), and `driver_machine.py:578` (structured-refusal resume).
- Fresh and rework prompts both go through `run_role:713-724` (the `rework` branch builds its prompt at `:652` and joins the same `lines`).
- `question_rework` (`:1756-1773`) re-enters through `run_role`.
- The S1 review and halt answers are resumes. The skill road (`story_step` through `phases/*.md`) does not use the driver at all (P3).
- **Gap (finding A-4, not blocking).** Card A's sibling line says "`question_resume_prompt` is n/a: a resumed session always follows a
  `run_role` start of the same dispatch, which already carried the lines". That is false for lines made by that dispatch's OWN finish.
  - **S3:** `s3_project` tells and then raises `Refusal` on `planned.problems` (that is card A's own position). The planner's same session is
    then resumed by `resume_with` or `driver_machine.py:578`. That resumed session is the writing role's next session in time, but it is not
    a `run_role` start, so it is not told.
  - **S4 acceptor:** `stage_acceptance_write` tells, then `stage_done --acceptance` refuses, and the critic is resumed in its own session
    without the lines.
  - No line is lost: they stay in the store under F-2. But the card must name this edge, either "a refusal resume of the same dispatch does
    not carry them; the next `run_role` does", or append `next_session_lines` in `resume_with`, which is a second reader (see key 11).

## Key 2. Card A: store, receiver and removal

- **Collision `next:<stage>:<role>` vs a dispatch id: HOLDS.**
  - Dispatch ids are `S\d+-qa-[a-z-]+-\d+` (`driver_dispatch.py:2210`).
  - `question_resume_prompt` pops only `dispatch` (`:1749`).
  - Nothing iterates the dict. The 4-site grep above is the evidence.
- **A second window or a second same-name role at one stage: HOLDS.**
  - S3 windows run one after another (`stage_S3` → `run_role` exit after the window-1 accept). S4 runs one designer at a time (`stage_S4:531`,
    `s4_after_critic` → `rework`).
  - The case lines carry their case id (`_apply_case_key` prefixes `{case_id}: `, `question_register.py:1733`), so a designer rework scoped to
    other cases still sees whose entry each line is.
  - S5 parallel chains are no receiver.
- **The receiver for each carrier.**
  - **S3 planner (`stages()["S3"]["roles"][0]`): right.** It equals the plan carrier's hard-coded role `qa-test-strategist`
    (`planning_contract.py:3375`), and window 2 hears window 1's notes. It is unchanged by `sc-a1a`, whose S3 roles are
    `["qa-test-strategist"]`.
  - **S4 designer (`s4_after_critic`, `raise_move`): right.** The rework through `self.rework` → `run_role` reads the lines in its first
    prompt.
  - **Acceptor: DEFECT A-1 (blocking).** The card takes stage = the ACCEPTED stage and role = `stage_acceptor(stage)`. That holds for the
    stage critics (S2/S3/S4: the critic runs at the stage it accepts), but not for the CONSUMER acceptors.
    - `stage_acceptance_write` is also called by `consumer_completion` (`driver_stage_s6.py:359`) and by `consumer_settled` (`:391`).
      Those are for S6, accepted by `qa-failure-analyst`, and S7, accepted by `qa-doc-scribe` (`stages.json`; `CONSUMER_ROUTES`
      `driver_stage_s6.py:146-151`: `consumer_stage` S7 and S8).
    - The consumer's own sessions run at `consumer_stage`: `driver_stage_s7.py:133`, `driver_stage_s8s9.py:79`.
    - So lines go to `next:S7:qa-doc-scribe`, while the scribe's next session calls `next_session_lines("S8", "qa-doc-scribe")`. They are
      never read.
    - This is reachable. `raise_from_handoff` executes `rewords` items for ANY stage (they are taken out before `role_question_errors`, the
      S1-S4 check: `question_register.py:2206-2213`), and the scribe's form carries `questions` (`handoffs/s8-scribe-to-gate-b.yaml`).
    - After the unmerged `sc-a1b` (which removes `acceptance_by` from S2/S3, `git diff 9c15423...wip/sc-a1b -- references/stages.json`), the
      consumer roads plus S4 are the ONLY callers of this carrier.
    - §1.1 names only `stage_critic_completion` and `s4_critic_completion` as callers. The `driver_stage_s6.py` callers were missed.
    - Fix (paste): "In `stage_acceptance_write`, key the acceptor's lines by the stage its own session runs at — the `stage` of
      `controller_state()["dispatches"][dispatch]`, falling back to `stage` — not by the accepted stage. Add a carrier row: S7 accepted by
      `qa-doc-scribe`, whose next S8 session reads the line."
  - **Empty acceptor (silent edge, A-5).** `stage_acceptor` returns `""` for a stage with no `acceptance_by` (`driver_stage_plan.py:579-581`),
    so `tell_next_session(stage, "", ...)` would write `next:S2:`, which nobody reads. Fix: "an empty role stores nothing and prints the
    `note:` lines only".
- **F-3 (a): lines stay forever when the role never runs again.**
  - Acceptable under FR-9/AR-24: those rules carry a PERSON's words, and these are code's own refusal texts.
  - Acceptable under AR-25 too, because the state is inert: no gate or move reads it, and a refused entry keeps the OLD words, toward
    asking.
  - BUT FR-40 is explicit: "a field that a story can sit in ... Read this when you add a state" (`design/state-exits.md` header). The driver
    section "What the driver keeps (`state/driver-state.json`)" (`state-exits.md:179`) has no row for `question_pass_lines`. That gap is old,
    and card A adds a key form to it.
  - Fix (A-6, fix before merge): "Add `design/state-exits.md` to card A's owns: one row in the driver-state section for `question_pass_lines`
    (dispatch keys: popped by `question_resume_prompt`; `next:<stage>:<role>` keys: removed by `forget_told` after the role's next saved
    session; terminal and inert when that role never runs again, already printed as `note:`)."
  - The S4 designer under `approve` (no rework) is the main terminal case. That is the FR-10 truth of the tail, which F-4 handles.
- **`forget_told` after `_write_json` only: DEFECT A-2 (blocking).**
  - `run_role:729-731` saves WHATEVER `run_claude` returned, a dead session included (`is_error` with empty `result`). The next `run_role`
    of that dispatch starts a NEW session because `if not result.get("result")` (`:726`), and `retire_infra_result` sets an infrastructure
    failure aside (`driver_runner.py:1091-1104`). In both cases the session that got the lines produced nothing.
  - A `forget_told` placed after `_write_json` would drop the lines although nobody read them. That breaks the card's own invariant, "losing
    a line is forbidden".
  - The precedent for the right condition is in the same file: `resume_role:1121-1123` pops `pending_words` only when
    `str(result.get("result") or "").strip()` ("an error with no words answered nothing").
  - Fix (paste): "`forget_told` runs only when the saved result carries words (`str(result.get("result") or "").strip()`, the
    `resume_role:1121` rule); a dead or empty result keeps the lines. Add a row: a dead result leaves the store unchanged."
  - The other exits are right as named: `run_claude` raising (the `finally` path), and the reused saved result (`:732-733`, no session: no
    forget). The reused branch tells nothing new: the replayed carriers dedupe by exact string.
  - Silent edge A-7: `forget_told(stage, role, [])` must not touch or save state. `run_role` runs on S5 chain threads, and "saves" with an
    empty `sent` would add a state write on every launch.

## Key 3. Card A carriers: positions, parse, exit codes

- **`s3_project`: tell before the `planned.problems` Refusal: HOLDS** (`driver_dispatch.py:2741-2744`). `project_plan` fills `notes` only
  on the path that also wrote or tried rewords (`planning_contract.py:3420`, `:3452-3453`), so early-return problems carry no notes and
  nothing is lost.
- **`stage_acceptance_write`: tell before `stage_done --acceptance`: HOLDS against the code, as long as the tell sits INSIDE the new `try`.**
  The `question_register` call is `check=True`: a non-zero exit raises before `out` exists, which is the existing refusal road, so that case
  needs no line. Name the inside-the-try placement, because the card's text predates the FV1-22 wrapper (G-1).
- **`s4_after_critic`: tell after `critic_rollcall`, before `pin_cases` and `rework`: HOLDS** (`driver_stage_plan.py:767-775`; `pin_cases` is
  `check=True` and can raise, so telling first keeps the lines).
- **`raise_move`: the position is SILENT (A-8).** `code not in (0, 1)` raises `RepairFailed` (`driver_gates.py:596-598`). The card must say
  whether the tell comes before that raise. Fix: "Parse and tell on exit 0/1. On any other exit, tell the one unknown line BEFORE
  `RepairFailed`."
- **The slice parse is SAFE.**
  - `py` returns stdout then stderr (`driver_runner.py:227`).
  - `critic_rollcall --apply-fixes` prints one compact JSON line and nothing else on that path (`critic_rollcall.py:1201`).
  - `question_register` prints indented JSON (`:2439`) and refuses only on stderr (`:2265`).
  - A stray brace in stderr breaks `json.loads` and gives the "unknown" line. That is the allowed direction (AR-28).
- **Exit-code handling of `critic_rollcall`: unchanged** in both sites as long as no `check=True` is added. Card A should state "no `check`
  added; exit 1 stays legal", because "capture `code, out`" invites one.
- **DEFECT A-3 (blocking). A parsed output that reports a failure is read as "nothing refused".**
  - When `raise_pending` itself raises, `critic_rollcall` records `errors: ["raise_questions: <exc>"]` and NO `question_notes`
    (`critic_rollcall.py:1197-1198`).
  - Card A reads only `question_notes`, so it stores nothing: the designer's `question_repeats`/`reword_questions` were not executed at all,
    and nobody is told. That is FR-41/AR-28, exactly the class the card's "unknown" line is meant to close, and it is the card's own
    invariant.
  - Fix (paste): "In both `critic_rollcall` carriers, an `errors` list in the parsed object adds the unknown line (or its `raise_questions:`
    lines) to the designer's key. Add a row with `{"errors": ["raise_questions: X"]}` → one line stored."
- **Sweep of the same artifact (sweep-the-artifact-first rule): the keys of that one JSON object.** Card A reads one key and does not
  enumerate the rest.
  - `question_notes` — applied.
  - `errors` — A-3.
  - `plan_notes` ("raised, but the plan row was not told", `:1193-1194`) — the same AR-22 class with no driver reader; its receiver is the
    planner. Not in card A: queue it or apply it, by name.
  - `skipped` — n/a. Gate A's `unraised_questions` rehearsal names it (`raise_pending` docstring).
  - `repeats`, `rewords`, `raised`, `applied` — n/a: these are successes.

## Key 4. F-4 (§1.3)

- **The gap is REAL.**
  - The trigger is `fixes or self.unraised_cases()` (`driver_stage_plan.py:765`). `fixes` needs the literal `approve_with_fixes` (`:761`), and
    `unraised_cases` matches only a Then whose ref is `raise` (`:888`).
  - So a case holding only `question_repeats`/`reword_questions` under `approve` never reaches `raise_pending`, although `raise_pending`
    reads all three keys (`critic_rollcall.py:772`).
- **Cost for stories with no such key:** one in-process scan of the case files, returning `[]`. No subprocess, no change of order. When the
  trigger fires, `pin_cases` already follows `critic_rollcall`, the order `raise` Thens have today. So **no behaviour change** for stories
  without the keys.
- **Wording.** The new reader goes through `contract.case_files`, which returns the PINNED versions for a pinned story (`contract.py:3426-3445`).
  That is `unraised_cases`' reader, not what `raise_pending` reads: it uses `story_case_links` plus `_resolve_source`, the authoring file
  (`critic_rollcall.py:637-660`, `:758-765`). The trigger is equivalent at that point (the pins were just taken), but the card's sentence
  "the readers `raise_pending` relies on" is inaccurate.
- **Edge left silent (A-9).** A key holding `[]` or a non-list is a non-empty `front_line`, so it fires a run that does nothing. Say:
  "listed when `contract.parse_json_list(front_line(...))` gives a non-empty list; a malformed key also lists the case (it makes a line
  in `question_notes`)".
- **Gate A's repair trigger has the same gap, left open and NOT queued (A-10).**
  - `raise_move` runs only for the `unraised_questions` finding (`raise_precondition`, `driver_gates.py:583-587`).
  - With F-4, the entries run at every S4 close, so what reaches gate A is refused leftovers only.
  - Rule 5: name it as n/a with that reason, or put it as a queue line with an owner. §1.3 states the gap, and §5 does not carry it.

## Key 5. Card B: a MEANING change at a refusal

- **The shape of `reworded[]` (verified).** Each entry is `{at, by, role, stage, why, was[, was_readings]}`, where `was` is the text BEFORE
  that reword (`question_register.py:1636`). Index 0's `was` is the ORIGINAL. So `[r.was for r in reworded[1:]] + [current]` is exactly the
  list of reword RESULTS. The slice is right, and F-5 (b)'s list is right as a list of texts.
- **Skipped checks and false "done".** Done writes nothing, so "done" for a party that may not reword can only drop an entry whose words
  already stand. That is harmless on the CURRENT-text match: an answered question, a hidden repeat or another party's question already
  reads those words.
- **DEFECT B-1 (blocking): the HISTORY match is a pair detector that is not scoped (critic rule 15), and the card's direction statement is
  false for it.**
  - The card says "Allowed error: ... the person sees exactly the requested words". On a history match the person sees the CURRENT text,
    not the requested one.
  - Failure scenario: the designer's text1 is applied; the conductor later rewords to text2 after a showing; a NEW designer entry
    deliberately asks for text1 again (to undo text2's damage). F-5 (b) then returns DONE: the entry is dropped and listed under `rewords`
    as carried out, nothing is written, and the person keeps seeing text2. That is a silent drop dressed as success, the forbidden direction.
  - The replay a history match exists for is the SAME entry. Each `reworded` entry stores `role` and `why`.
  - Fix (paste): "A history match counts only when the reword that PRODUCED that text — the entry `reworded[k]` for the text
    `reworded[k+1].was` — has the same `role` as the caller and the same `_squeeze(why)` as the request. Text and identity are read from one
    entry. Otherwise the normal checks run. Correct the direction sentence: a history match drops only the same party's replayed entry."
  - Add row (j): text1 then text2 as above, then a request for text1 with a NEW `why` → not done (refused or applied by the normal rules).
- **The direction statement is otherwise complete.** "Same text as the ORIGINAL with no history → nothing changed" holds, because `produced` is
  `[]` when `reworded` is empty.
- **The `[1:]` boundary has no row (B-2).** The original text WITH a history is not a reword result, so it must not be done. Add row (k):
  reword once, then ask for the original text → not done.
- **Silent edges the card creates.**
  - **B-3.** The rule sits BEFORE the shape check of `readings`, and compares `[_squeeze(x) for x in given]` when the question matches. A CLI
    `--question-file` with `"readings": 5` (outside input: `_main_fv19` JSON-loads it, `:2321-2326`, and `reword_entry`'s check is not on
    that road) then raises `TypeError`. The CLI has no `run_guarded` (`question_register.py` bottom: `sys.exit(main())`), so that is a
    traceback, where today it is a refusal (`:1608-1611`). Fix: "readings are compared only when `given` is a list; otherwise the replay rule
    does not apply and the shape check refuses as today".
  - **B-4.** A `reworded` element that is not an object, or has no string `was`, must be skipped, not raise.
- **Rows (a)-(i): each traced against today's code.**
  - Fail today, pass after: (a), (b), (c), (d), (e), (i). Today: (a) and (b) are refused "not shown" (rule 3, `:1603-1605`) or "answered"
    (`:1600`); in (c)-(e) the entry stays with a note.
  - Pass both before and after: (f), (g), (h-second half). Today (f) is refused "nothing changed", (g) "not shown", (h-second half) "not
    done". Label them as CONTROLS of the meaning change.
  - Missing: (j) from B-1 and (k) from B-2.
- **Sibling claim: holds.** `declare_repeat`'s "already a hidden repeat of the same target → return the record" (`:2017-2019`) is the same
  shape. All three carriers reach the fix through the one writer (AR-15).

## Key 6. Card C: the doors, `--stage`, FR-2

- **Every flag in sentences (a)-(c) is accepted by `main` exactly as printed, after the guard change.**
  - `--task` is required (`main`); `--words-file` (`:2381`) and `--question-file` (`:2393`) exist.
  - `--by conductor`: `by` holds `conductor` (`question-vocabulary.json`). `--where "S2 stop|S3 stop|S4 stop"`: they are in `where`.
  - `--same-as` (`:2399`), and `--repeat` with `--same-as` plus `--words-file`: `_main_fv19:2328-2337`.
  - `--register-hash` and `--reading` stay stray for these two operations.
  - **FR-2 HOLDS.** The existing reword sentence lacks `--task`, so a conductor copying it fails today on argparse's required argument.
    Card C fixes a live FR-2 defect.
- **"Refused while a plan row or a case still rests on the later id": HOLDS.** `declare_repeat` refuses on `_dependant_lines(..., bare_ok=False)`
  after repointing bare `question_refs` (`:2040-2052`).
- **CONFLICT inside the card (C-1).** Item 1 makes the guard accept `--stage` only with `--raise --from-handoff`, `--repeat` or `--reword`. So
  `--note --stage S3` is refused by the GUARD in `main`, `_main_fv19` is never reached, and the "joins `stray` ... no meaning with --note"
  line is dead code. Yet the DoD row expects "refused, 'no meaning with --note'". Fix (paste): "Drop the `_main_fv19` stray item; the
  `--note --stage` row expects the guard's text."
- **The stage vocabulary (C-2).**
  - `contract._stage_entry` is documented as "THE private reader of that table for `stage_roles` and `rework_mode`" (`contract.py:5848-5852`).
    Its only cross-module caller is `acceptance.stage_def_of` (`acceptance.py:1290`).
  - The card's refusal text needs "the ids of `stages.json` in order", and no ordered public reader exists. `null_outcomes.stage_ids()`
    (`null_outcomes.py:213`) returns an unordered set; grep `def .*stage_ids|stage_list|all_stages` over `scripts/*.py`, non-test, finds only
    that one.
  - A builder will open `stages.json` a second time (AR-13) or touch `contract.py`, which is not in owns.
  - Fix (paste): "Validate through `acceptance.stage_def_of(stage)`, the public wrapper. Read the valid list from
    `null_outcomes.stage_ids()` sorted by the number after `S`; no new reader of `stages.json`."
- **Silent edge (C-3).** `stages.json` that cannot be read makes `_stage_entry` give `{}` for every id, so EVERY non-blank `--stage` would be
  refused with "Valid: " followed by nothing. Name it (FR-59): "an unreadable table refuses with the reason 'the stage table could not be
  read', and a blank `--stage` still records `""`".
- **The adversarial battery** (absent, blank, case, out-of-table, 10,000 characters cut to 80, Cyrillic, a newline) is right for outside input,
  and every limit has a row at and beyond it. One edge is left silent: `--stage S4` with `--where "S3 stop"`. Not harmful (see C-5), but
  name it.
- **One road (C-4, rule 19).** The new value check covers `--repeat`/`--reword` while `--raise --from-handoff --stage` stays free text (help
  still says "S1-S4"). The same flag is checked on two operations and not on the third, with no reason given. Fix: "apply the same
  `stage_def_of` check to `--raise --from-handoff`, or state why the driver-only road is exempt".
- **The sibling on the same surface (rule 14), C-5: the conductor's `--where` has no carrier.** `_main_fv19` requires and validates `--where`
  (`:2311-2315`), but never passes it on: `declare_repeat` records `where="stage ran"` hard-coded (`:2056`), and `reword` takes no `where` at
  all. The doors in sentences (b) and (c) ask for a value that is dropped. That is the AR-22 class card C cites for `stage`. Queue it as a
  line with an owner, or carry it here.
- **Paths (C-6, FR-15/AR-8).** Sentences (b) and (c) name a bare `question_register.py`, while the `--show` door in the same text gives
  `python {self.scripts / 'question_register.py'}` (`:1875`). One form in one text: use the full path in (b) and (c), and in (a) too.
- **Cap or ratchet on the hand-over text: none found.**
  - `references/role-load.json` measures role start load per role (keys `ratchet_tokens`, `process_ratchet_tokens`), not the conductor's
    `unread` text.
  - The grep `HANDOVER_MAX|PROMPT_MAX|unread.*bytes` over `scripts/` finds nothing relevant. The positive control is the same grep's hits in
    `device_stand.py:207` and `host_probe.py:929`.
  - The question part is cut at 6000 (`:1880`), and instructions precede it (the POSITION INVARIANT at `:1838-1839`), so the growth is
    bounded and safe. `conductor.md` is untouched (11897/12000).

## Key 7. Edges left silent, all cards

| card | edge | status |
|---|---|---|
| A | consumer acceptor runs at another stage | A-1 (blocking) |
| A | dead or empty saved result | A-2 (blocking) |
| A | parsed output with `errors` | A-3 (blocking) |
| A | same-dispatch refusal resume gets no lines | A-4 |
| A | empty acceptor role | A-5 |
| A | `forget_told` with nothing sent: no write | A-7 |
| A | `raise_move` position vs `RepairFailed`; no `check` added | A-8 |
| A | F-4 key `[]` or malformed | A-9 |
| A | TR1 says "did not carry out" while the unknown line says "not known" — one packet contradicts itself (FR-10). Fix: TR1 = "Code did not carry out these question entries from your earlier work, or could not tell whether it did; each line says which and why:" | A-11 |
| B | history match from another party or another `why` | B-1 (blocking) |
| B | the original text with history | B-2 |
| B | non-list `readings` on the CLI road | B-3 |
| B | malformed `reworded` element | B-4 |
| C | `--note` guard vs stray | C-1 |
| C | unreadable stage table | C-3 |
| C | `--stage`/`--where` mismatch | named above |

TEMPORAL is stated in both worlds for A and C. POSITIONAL is stated for A, except `raise_move` (A-8), and for B and C.

## Key 8. Tests by `docs/TESTING.md`

- **Homes: right.** `test_gate_question_form.py`, `test_question_register.py` and `test_retro_numbers.py` are keep rows of `test-layers.json`
  and absent from `slow_tests.json`. No quarantined file is edited.
- **Card A's tables are too many receipts for TESTING.md (T-1).** TESTING.md:55 rules out "a test per function, branch, spec edge or DoD key"
  and "mini-batteries on an internal function". `fv19_told_next_session_store` and `fv19_told_lines_in_prompt` are exactly that: store and
  reader tables of internal functions. Fix: "Fold them into `fv19_carriers_tell`. Each carrier row asserts through
  `next_session_lines(<receiving stage>, <role>)` and `forget_told`. Add the rows A-1 (S7 → S8 scribe), A-2 (dead result keeps the store)
  and A-3 (`errors` → the unknown line)."
- **LOAD-BEARING WITH NO TEST IN EITHER LAYER (T-2).** The `run_role` wiring: lines enter the prompt before `extra`, and removal happens only
  after a saved result with words. Card A says "judged by the slow `test_story_run_*` files ... in the batch canon", but it adds no row to
  any of them, so the canon would judge nothing new. Fix (paste): "Add one row to an existing `test_story_run_*` scenario that drives an S4
  rework (owned by A, slow, judged by the canon): the rework prompt holds TR1 and the line, and the store is empty after the session."
- **Card B:** one table, with defect rows that fail today plus labelled controls (key 5). Right for a meaning change. Add (j) and (k).
- **Card C:** the CLI battery is the right kind (outside input), and the hand-over row has the `recorded=None` control.
- **DoD runs of slow files (T-3).** `test_judgment_census.py` (33.3 s, cards B and C) and `test_console_encoding.py` (22.7 s, card A) are on
  `slow_tests.json` (`:63`, `:22`). PROJECT.md (package change item 2) says a SLOW_TESTS file is not run locally. builder-rules 7b names
  `test_console_encoding` by edit type, so the two rules pull against each other. The cards must pick one, by rule. The ratchet-only
  reading favours "judged by the batch canon".

## Key 9. Census and architecture lines

- **"No new census unit": HOLDS on reading.**
  - Units come from refusal sites; the callee name `refuse` is a wide transport (`refusal_registry.py:75`, `:1495`). `_refuse` is itself
    the unit (`judgment-census.json:862`), so `_main_fv19` calling `_refuse` creates none, and it has no row. LIST transport (`append`)
    never creates or flips a unit (`test_judgment_census.py` docstring, lines 27-29).
  - Card C adds `problems.append` lines in `_main_fv19` and `main`. Card B adds an early `return` in `reword` (row 871, xref). Card A adds no
    raise.
  - Card A's DoD lacks the census run that B and C carry: harmless by reading, but asymmetric.
- **AR lines.**
  - A's AR-15/AR-18 claim "no second transport" is only true for the store; there are two readers with two removal rules (key 11).
  - A's AR-14 (one writer of the key: `driver_dispatch`) holds.
  - C's AR-13/AR-1 claim fails as drafted (C-2).
  - B's AR-25/AR-14/AR-15 hold.
  - `judgment: none` holds for all three: these are transport, byte equality and a data value check.

## Key 10. Feasibility and the cut

- **The functions are disjoint.**
  - `driver_dispatch.py`: A owns `run_role`, `s3_project` and the new methods; C owns `register_words_to_conductor`.
  - `question_register.py`: B owns `reword`; C owns `main`/`_main_fv19`, which call `reword` with an unchanged signature.
  - The test files: new functions only (a textual conflict at most).
- **Against the unmerged stage-critics topic.**
  - `sc-a1b` (and `sc-a1c` on top) deletes `stage_S2`, `stage_critic_route`, `stage_after_critic`, `stage_critic_form` and
    `stage_critic_completion`. It keeps `stage_acceptance_write` but carries its PRE-FV1-22 body, so the conflict is in A's function.
  - It changes `s3_ticket_completion`, which is adjacent to A's `s3_project`, not the same function.
  - It edits `driver-layers.json`, which A also edits (rows, textual).
  - A1c's uncommitted diff (`.claude/worktrees/sc-a1c`) touches `driver_stage_plan.py:907` (the T2 rule), not A's functions.
  - **Semantic coupling:** after A1b the S2/S3 acceptor road is gone. A's acceptor rows must use S4 or the consumer stages, never S2/S3
    (otherwise `stage_acceptor` is `""`, see A-5).
- **FV1-20 B-1** (`.claude/worktrees/fv120-b1`, branch `wip/fv120-b1`): `brief_pack.py` and its test only. No collision.
- **"N3 after A and B": RIGHT.**
  - A gives the hearing (AR-10).
  - B removes the false replay lines.
  - F-4 inside A makes the S4 tail true for an `approve` story, and N3 tells the designer the keys.
  - C and D are independent.
  - A-1 matters to N3 only if N3 also tells consumer roles about `rewords`.

## Key 11. Class completeness and P31

- **Axis 5 (stage twins)**
  - S3 plan carrier and S4 case carrier: covered (A).
  - Handoff carrier: covered for S4. NOT covered for the consumer stages (A-1).
  - Skill road: P3, queued with an owner question (F-8). Accepted as queued.
  - The author + critic loop of S5/S7: n/a, because no reword/repeat entry exists there.
- **Axis 13: n/a** (no dispatch text cut).
- **Axis 33: n/a** in the card's sense: the key is by role, no dispatch is guessed. But A-1 is the axis-33 shape at the stage level: which
  stage is this session's. The fix reads the dispatch record, not a guess.
- **Axis 34 / P31 (rule 19).**
  - (a) **A two-road residual.** Card A adds `next:` keys read by `next_session_lines` (removed after a saved result, F-2 (a)) next to H36's
    dispatch keys popped at prompt build (`question_resume_prompt`, `:1749`). Two receivers justify two KEYS. The two REMOVAL rules are an
    unjustified divergence, and H36's rule loses lines today:
    - `resume_role` builds the prompt (pop) at `:1074-1075`, then returns `question_rework` when there is no session (`:1080-1083`) or the
      session is gone (`:1112-1115`).
    - `question_rework` → `run_role(rework=...)` never reads the dispatch key, and `save_state()` (`:1769`) persists the loss.
    - F-2's text promises "aligning H36 is a queue line", but §5 does not carry it.
    - **Proposed node** (owner: the FV1-9 Lead; opening it is the Lead's call): "H36 removal after the session's saved result, as F-2 (a);
      `question_rework`'s `run_role` reads the dispatch key, so the plan lines reach the replacement session."
  - (b) **The `--stage` check on two of three operations** (C-4).
  - (c) **No second transport toward the conductor.** The conductor still gets its own refusals as CLI exit-2 text. Holds.

## DUPLICATION AND CONSISTENCY (critic-diff-brief item 6)

- **A: the parse is copied three times (fix before merge).** The same `json.loads(out[out.index("{"):out.rindex("}") + 1])` plus the
  unknown-line fallback would sit in `s4_after_critic`, `raise_move` and `stage_acceptance_write`, on top of two existing copies
  (`driver_gates.py:331`, `driver_machine.py:1692`). Fix: one private helper in `driver_dispatch` (A owns it),
  `told_from(out, keys) -> list`, used by the three carriers. It returns the lines, or the one unknown line, or the `errors` lines (A-3).
- **C:** a second stage-id reader would be a duplicate (C-2); `null_outcomes.stage_ids` already exists.
- **B:** none found. The predicate reuses `_squeeze` and `_reading_texts` (`question_register.py:1551-1556`).
- **What I grepped:** `json.loads\(out` over `scripts/*.py` (the two hits above); `def .*stage_ids` (one hit).

## CODE QUALITY (critic-diff-brief item 7)

- No new function over 60 lines is planned.
- `run_role` (165 lines today) gains 2 lines. The split is out of scope, and P7 is queued for `reword`.
- The one copy-paste risk is the triple parse above.
- **Work whose result nobody reads:** C-5 (`--where` is validated and dropped) is an existing instance on the surface card C edits.

## ONE ROAD (critic-diff-brief item 12)

- Key 11 (a) is a residual, written as a proposed node above.
- C-4 is a fix of this round.
- No language, project or case is excluded.

## G-1 (all cards)

The anchors are wip/fv1-9-fix lines, and §7a says every card starts from origin/main. Add to the common list: "line numbers are wip/fv1-9-fix's;
anchor by function and quoted text. `stage_acceptance_write` now has a `try/except Refusal` (FV1-22 N2): the tell goes inside it."

---

## Binding amendments (one sentence each, for the Lead to paste)

Card A:
1. (A-1, blocking) Key the acceptor's lines by the stage of its own dispatch record (`controller_state()["dispatches"][dispatch]["stage"]`,
   falling back to `stage`), not the accepted stage. Row: S7 accepted by `qa-doc-scribe` → read by its S8 session.
2. (A-2, blocking) `forget_told` only when the saved result carries words (the `resume_role:1121` rule). Row: a dead result keeps the store.
3. (A-3, blocking) A parsed `critic_rollcall` object with `errors` adds the unknown line (or its `raise_questions:` lines). Row with
   `errors` only.
4. (A-4) Name the edge: a refusal resume of the same dispatch does not carry the lines; the next `run_role` does.
5. (A-5, A-7) An empty role stores nothing. `forget_told` with nothing sent writes nothing.
6. (A-6) Add `design/state-exits.md` to owns: one driver-state row for `question_pass_lines`, both key forms.
7. (A-8) `raise_move`: tell on exit 0/1, the unknown line before `RepairFailed` on any other exit. No `check` added at either
   `critic_rollcall` site.
8. (A-9) F-4 lists a case when `parse_json_list(front_line(...))` is a non-empty list or malformed. Fix the "readers `raise_pending`
   relies on" wording.
9. (A-10) Gate A's trigger: state n/a with the reason (F-4 executes the entries at every S4 close) or queue a line with an owner.
10. (A-11) The TR1 wording that covers the unknown line (key 7 table).
11. (T-1, T-2) Fold the store and reader tables into the carrier table. Add one S4-rework row to an existing `test_story_run_*` scenario
    for the `run_role` wiring.
12. (duplication) One `told_from` helper for the three parses.
13. Sweep the `critic_rollcall` keys: `plan_notes` applied, or queued by name.

Card B:
1. (B-1, blocking) A history match counts only when the producing entry `reworded[k]` has the caller's `role` and the same `_squeeze(why)`.
   Correct the direction sentence. Row (j).
2. (B-2) Row (k): the original text with a history → not done.
3. (B-3, B-4) Compare readings only when `given` is a list. Skip malformed `reworded` elements.
4. Label (f), (g) and (h-second half) as controls.

Card C:
1. (C-1) Drop the `_main_fv19` stray item for `--note`. The row expects the guard's text.
2. (C-2) Validate through `acceptance.stage_def_of`. The valid list is `null_outcomes.stage_ids()` sorted numerically; no new reader of
   `stages.json`.
3. (C-3) An unreadable stage table refuses with that reason.
4. (C-4) The same check for `--raise --from-handoff --stage`, or a stated exemption.
5. (C-5) The `--where` that is validated and dropped: a queue line with an owner, or carried here.
6. (C-6) The full script path in sentences (a)-(c), the form of the `--show` door.

All: (G-1) the anchor note. (T-3) Name the slow DoD files "judged by the batch canon", or cite the rule that makes them local.

Proposed node (the Lead's call, rule 6): H36 removal after a saved result, and `question_rework` reads the dispatch key (key 11 (a)).

## Trail

- **Read:**
  - the spec under review (whole);
  - the topic critic's "Proposed nodes";
  - `driver_dispatch.py`: 174-190, 538-600, 617-796, 1057-1140, 1619-1960, 2195-2232, 2720-2760;
  - `driver_stage_plan.py`: 480-899;
  - `driver_stage_s6.py`: 146-160, 300-400;
  - `driver_gates.py`: 325-335, 580-619;
  - `driver_runner.py`: 211-235, 1091-1105;
  - `driver_machine.py`: 555-590;
  - `critic_rollcall.py`: 700-830, 1150-1225;
  - `question_register.py`: 1551-1800, 1990-2060, 2181-2236, 2293-2480;
  - `planning_contract.py`: 3351-3470;
  - `contract.py`: 3426-3445, 5833-5862;
  - `null_outcomes.py`: 205-217;
  - `references/stages.json` (roles, `acceptance_by`), `question-vocabulary.json:1-30`, `role-load.json` keys;
  - `handoffs/` (`questions` carriers);
  - `design/state-exits.md`: headings, row 188;
  - `judgment-census.json` (`question_register` rows); `test_judgment_census.py` docstring; `refusal_registry.py:75`, `:1495`;
  - `slow_tests.json`, `test-layers.json` (the keep/quarantine lookup);
  - `docs/TESTING.md:14-73`; `plans/builder-rules.md:14-40`; `docs/SIBLING_MAP.md` axes 5, 13, 33, 34;
  - `docs/tasks/critic-diff-brief.md:1-60`; `tools/critic_verdict.schema.json`.
- **Branches and trees checked:**
  - `git diff wip/fv1-9-fix 9c15423` (driver files);
  - `git diff 9c15423...wip/sc-a1a` (`stages.json`);
  - `git diff 9c15423...wip/sc-a1b` (stat, `driver_stage_plan.py`, `driver_dispatch.py`, `test_question_register.py`);
  - the uncommitted diff of `.claude/worktrees/sc-a1c`; `.claude/worktrees/fv120-b1` (stat).
- **Negative claims, each with a positive control of the same shape:**
  - `question_pass_lines` sites: the grep also hits the fixture.
  - `question_threshold(` callers: two hits.
  - `--answer QID --reading|could not tell what it asks|--reword QID` (case-insensitive, package): the hits in `driver_dispatch.py` and the
    CLI's refusal pin at `test_question_register.py:2714`; no hand-over pin.
  - `with --words-file|An answer they gave...` (case-insensitive): hits elsewhere, no pin on the hand-over.
  - `def .*stage_ids`: one hit.
  - The cap grep: hits in other files.
- **Not done:** no test run, since this is a plan review with no mechanical layer. Card D was not reviewed.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "A-1: the acceptor carrier keys lines by the ACCEPTED stage, but consumer acceptors (S6 by qa-failure-analyst, S7 by qa-doc-scribe; driver_stage_s6.py:359,:391; CONSUMER_ROUTES :146-151) run their next session at S7/S8, so next:S7:qa-doc-scribe is never read; reachable (raise_from_handoff runs rewords for any stage, question_register.py:2206-2213)",
    "A-2: forget_told after _write_json drops lines after a dead or empty saved result (run_role:729-731 saves any result; :726 reruns when result is empty), which breaks the card's own 'losing a line is forbidden'; precedent rule resume_role:1121",
    "A-3: a parsed critic_rollcall object with errors (raise_pending crashed, critic_rollcall.py:1197-1198) carries no question_notes, and card A reads it as nothing refused (FR-41/AR-28)",
    "B-1: the F-5 (b) history match is an unscoped pair detector (critic rule 15): a deliberate request for an earlier reword text is returned DONE while the person sees the current text; the card's direction sentence is false for history matches; scope the match to the producing reworded[k] entry's role and why"
  ],
  "class_completeness": "Axis 5: plan and case carriers covered; handoff carrier covered for S4, not for the consumer stages (A-1); skill road P3 queued (F-8). Axis 13 n/a. Axis 33 n/a by key, but A-1 is its stage-level shape. Axis 34/P31: two removal rules on one store (H36 pop at prompt build loses lines on the question_rework fallback, driver_dispatch.py:1074-1083,:1112-1115) - proposed node, owner the FV1-9 Lead; the --stage value check on two of three operations (C-4). Same-artifact sweep: the critic_rollcall JSON keys - errors (A-3), plan_notes not enumerated (A-13). Rule 14 sibling on card C's surface: the --where flag is validated and dropped (C-5). Gate A trigger gap stated in section 1.3 but neither fixed nor queued (A-10).",
  "trail": {
    "read": [
      "docs/tasks/specs/20261114-fv1-9-tail-cards-spec.md",
      "docs/tasks/specs/reviews/20261114-fv1-9-topic-critic.md (Proposed nodes)",
      ".claude/worktrees/fv1-9-td/ai-packages/qa-factory/scripts/driver_dispatch.py",
      ".claude/worktrees/fv1-9-td/ai-packages/qa-factory/scripts/driver_stage_plan.py",
      ".claude/worktrees/fv1-9-td/ai-packages/qa-factory/scripts/driver_stage_s6.py",
      ".claude/worktrees/fv1-9-td/ai-packages/qa-factory/scripts/driver_gates.py",
      ".claude/worktrees/fv1-9-td/ai-packages/qa-factory/scripts/driver_runner.py",
      ".claude/worktrees/fv1-9-td/ai-packages/qa-factory/scripts/driver_machine.py",
      ".claude/worktrees/fv1-9-td/ai-packages/qa-factory/scripts/critic_rollcall.py",
      ".claude/worktrees/fv1-9-td/ai-packages/qa-factory/scripts/question_register.py",
      ".claude/worktrees/fv1-9-td/ai-packages/qa-factory/scripts/planning_contract.py",
      ".claude/worktrees/fv1-9-td/ai-packages/qa-factory/scripts/contract.py",
      ".claude/worktrees/fv1-9-td/ai-packages/qa-factory/scripts/null_outcomes.py",
      ".claude/worktrees/fv1-9-td/ai-packages/qa-factory/references/stages.json",
      ".claude/worktrees/fv1-9-td/ai-packages/qa-factory/references/question-vocabulary.json",
      ".claude/worktrees/fv1-9-td/ai-packages/qa-factory/references/role-load.json",
      ".claude/worktrees/fv1-9-td/ai-packages/qa-factory/design/state-exits.md",
      ".claude/worktrees/fv1-9-td/ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json",
      ".claude/worktrees/fv1-9-td/ai-packages/qa-factory/scripts/slow_tests.json",
      ".claude/worktrees/fv1-9-td/ai-packages/qa-factory/scripts/tests/test-layers.json",
      "docs/TESTING.md",
      "plans/builder-rules.md",
      "docs/SIBLING_MAP.md (axes 5, 13, 33, 34)",
      "docs/tasks/critic-diff-brief.md",
      "git diff wip/fv1-9-fix 9c15423; git diff 9c15423...wip/sc-a1a and wip/sc-a1b; sc-a1c and fv120-b1 worktrees"
    ],
    "reruns": [
      {"command": "git -C .claude/worktrees/read-main rev-parse --short HEAD; git merge-base --is-ancestor 9c15423 50d9012", "result": "50d9012; exit 1 (read-main is behind, so fv1-9-td at 9c15423 was read)"},
      {"command": "grep -n question_pass_lines scripts/*.py (fv1-9-td)", "result": "4 sites: driver_dispatch.py:1689,1749,1817,1830; the fixture driver-layers.json:1192 is a positive control"},
      {"command": "grep -n 'question_threshold(' scripts/*.py", "result": "driver_dispatch.py:775 and :1133 only"},
      {"command": "grep -n stage_acceptance_write scripts/*.py (9c15423 and wip/sc-a1b)", "result": "driver_stage_plan.py:676,817 and driver_stage_s6.py:359,391; after a1b only S4 and the consumer callers remain"}
    ]
  },
  "fixes": [
    "A-1 key the acceptor's lines by its own dispatch record's stage; add an S7 to S8 scribe row",
    "A-2 forget_told only when the saved result carries words; add a dead-result row",
    "A-3 a critic_rollcall errors list adds the unknown line; add a row",
    "A-4 name the same-dispatch refusal-resume edge",
    "A-5/A-7 an empty role stores nothing; forget_told with nothing sent writes nothing",
    "A-6 add a design/state-exits.md driver-state row for question_pass_lines, both key forms",
    "A-8 raise_move: tell on exit 0/1, the unknown line before RepairFailed; no check added",
    "A-9 F-4 lists a case on a non-empty or malformed parsed list; correct the reader wording",
    "A-10 gate A trigger: n/a with the reason, or a queue line with an owner",
    "A-11 TR1 wording that covers the unknown line (FR-10)",
    "A-12 one told_from helper in place of three copied parses",
    "A-13 sweep critic_rollcall keys: plan_notes applied or queued by name",
    "T-1/T-2 fold the store and reader tables into the carrier table; add one S4-rework row to an existing test_story_run scenario for the run_role wiring",
    "B-1 scope the history match to the producing entry's role and why; correct the direction sentence; add row (j)",
    "B-2 add row (k): the original text with a history is not done",
    "B-3/B-4 compare readings only when given is a list; skip malformed reworded elements",
    "C-1 drop the _main_fv19 stray item for --note; the row expects the guard text",
    "C-2 validate through acceptance.stage_def_of; the valid list is null_outcomes.stage_ids sorted numerically",
    "C-3 an unreadable stage table refuses with that reason",
    "C-4 the same check for --raise --from-handoff --stage, or a stated exemption",
    "C-5 the --where flag validated and dropped: a queue line with an owner, or carried here",
    "C-6 the full script path in hand-over sentences (a)-(c)",
    "G-1 anchor by function and text; the tell goes inside the FV1-22 try in stage_acceptance_write",
    "T-3 name the slow DoD files as judged by the batch canon, or cite the rule that makes them local"
  ]
}
```
