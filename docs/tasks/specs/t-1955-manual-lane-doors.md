# t-1955 — manual lane doors: B-16 (S5 probe-gap word), B-17 (S6 recorder lock), B-18 (S6 unprepared outcome), B-19 (stale halt after `exit_limit`) — SPEC (designer, revised)

Status: revised 05.11.2026 after **critic-on-plan t-1958: fit_with_fixes; fixes 1–12 applied**:
- fix 1 (B, `asked` transport) → §3 N1 item 3 (the `rows` pattern: four functions named) + N1 owns;
- fix 2 (B, lead carries the class scope, no per-state `says`) → §3 N1 item 3 (exact lead text; `go on` option = the unchanged fallback row) + §5 Q1;
- fix 3 (B, `probe_gap_cases` only for `probe_could_not_run`) → §3 N1 item 1, E1.3 (invariant rewritten), E1.9;
- fix 4 (B, four more door carriers) → §2 F3, §3 N1 item 2 + N1 owns (`contract.py` docstring, `state-exits.md:71`, the controller's concrete ticket, `go_on_as_is.run`);
- fix 5 (N1 witness hygiene, two new tests) → §3 N1 DoD;
- fix 6 (N2 last-row predicate) → §3 N2 item 5, E2.2, E2.3, DoD;
- fix 7 (N2 `build_record`, `device_stand.py:544`, "no capture") → §3 N2 item 2, item 7, sibling table, owns, DoD;
- fix 8 (B, binder `_running_dispatch`) → §2 F21, §3 N3 item 1, E3.1;
- fix 9 (B, `OBSERVATION_FILE_COMMANDS`) → §3 N3 item 2, DoD;
- fix 10 (`attempt_id`, `walked` derived) → §3 N3 items 1–2, E3.9–E3.11, DoD;
- fix 11 (prompt line is THE direction; ratchet witness) → §2 F26, §3 N3 item 5 + owns (`qa-runner.md` dropped), DoD;
- fix 12 (F21 corrected, ratchet measurement with its command) → §2 F21, F26, reading trail.
Plus Lead decision 7: new node **N4 (B-19)**, root cause traced by reading (§2 F27–F33). §4 re-stated for N1–N4.

**Decided by the Lead, 05.11.2026** (moved out of §5): F1 = A (the driver executes `go on`; one `actions` row; no new token);
F2 = the case key always, restricted to `probe_could_not_run` instances; F3 = owner `factory`; F4 = step-evidence fallback, lock only when
the LAST `steps.jsonl` row has `outcome failed` and `command ui`; F5 = one record, `walked` DERIVED from steps on disk, `attempt_id` set;
F6 = a new `row_states` row `unprepared_walk`; F7 = the prompt-line route — measured slack 0 (§2 F26), so no charter line is added; this is
the direction, not a fallback. The F1 lead text is written "confirmed by the owner 05.11.2026 19:00 («по всем это ок»)" (§5 Q1).

Package under change: branch `experiment/thinking-roles`, worktree `D:/ws1/wt-fbfix` (package
`D:/ws1/wt-fbfix\ai-packages\qa-factory`, below `PKG\`). Every file:line was read in that worktree on 05.11.2026. The arm B driver ran
from `D:/ws1/exp-thinking-roles\pkg-b`; for N4 the two decisive lines were checked there too (§2 F33). Owner's word 05.11.2026
(notebook `experiments/mybooks/thinking-roles/thinking-roles.md:120`): «должен быть обходной вариант, например роль тестирует сама без кода.
Фабрика не должна вставать».

## §1 Goal, AR-n touched, owners of every check

Goal: in each of the four places of the arm B rerun where the factory stood and asked a person what only the factory could fix (or asked
again what the person had answered), a door exists that its receiver can actually use, and the factory goes on.

| node | bug | AR-n touched (change check -> in the node's DoD) | FR / P |
|---|---|---|---|
| N1 | B-16 S5 probe-gap word | AR-9 (the refusal names a door the reader reads), AR-13 (`contract.probe_gap_words` stays the ONE reader, logic unchanged; `PROBE_GAP_RECORD` the ONE door text), AR-16 (the lead through the one question form), AR-24 (the person's `go on` reaches the reader whole, by code), AR-25 (the seam has a move), AR-1 (the conductor's door is a data row), AR-29 (code joins ids; it never judges whether the gap is acceptable) | FR-1, FR-2, FR-8, FR-9, FR-10, FR-12, FR-41, FR-57; P13, P22 |
| N2 | B-17 S6 recorder lock | AR-9, AR-1 (new refusal sentences are data rows of `build-identity-methods.json` `refusals`), AR-13 (`LOGIN_UNKNOWN_CAUSE` one producer, readers import it), AR-25, AR-27 (the row names its true owner), AR-29 (gates read fields, never `probe_line` words) | FR-2, FR-12, FR-19, FR-46, FR-57; P15, P22 |
| N3 | B-18 S6 unprepared outcome | AR-14 (one writer of `work/manual-blocks/*`: `write_block`), AR-13 (one S6 binder `_running_dispatch`), AR-21/AR-22 (producer and readers change together), AR-23 (an unprepared case declares its empty outcome), AR-25, AR-27, AR-28, AR-10 (the command reaches the runner before the work, in its prompt line), AR-29 | FR-5, FR-23, FR-38, FR-59; P26, P27 |
| N4 | B-19 stale halt re-asked | AR-24 (the person's `exit_limit` words reach the role that halted), AR-25 (the answered state has a move), AR-16 (the priced option is true: a second literal question id), AR-22 (new `ask` field `halt`: producer `exit_limit_facts`, readers `exit_limit_person`, `_exit_go_on` — one commit) | FR-7, FR-8, FR-9, FR-10; P22 |

Owners and census class (AR-29; host adaptation 10; class words of `scripts/tests/fixtures/judgment-census.json`):

| check / executor (file :: function) | added / altered | owner it serves | census class | why it is not a judgment |
|---|---|---|---|---|
| `window_record.py :: probe_gap_cases` (new, N1) | added | intent (carries the person's word to its reader) | xref | joins green, word-owed, could-not-run instance ids to case keys through `scope_instances` + `proof_level.probe_could_not_run`; no verdict read |
| `controller.py :: _s5_completion_problems`, `_s5_gap_problems` (N1) | altered (refusal TEXT only) | data | (unchanged rows) | conditions unchanged; the door names the key the reader reads |
| `story_run.py :: seam_chosen` probe-gap branch (N1) | altered | intent | n/a (executor) | records `probe gap: <case>` for the cases the QUESTION named; the person chose |
| `manual_capture.py :: _account_steps_gate` (N2) | altered | data | shape (row `manual_capture.py/_account_steps_gate`, census :490, stays `shape`) | reads `owner`, `do_not_retry`, `cause`, and `outcome`/`command` of the LAST `steps.jsonl` row |
| `manual_capture.py :: choose_attempt`, `_blocked`; `manual_evidence.py :: build_record` env_blocked branch (N2) | altered (text by field) | data | shape | field `cause` selects the sentence |
| `manual_evidence.py :: write_block` missing-key refusal (N3) | altered | data | shape | key presence |
| `manual_evidence.py :: write_unprepared` (new writer, N3) | added | data (carries request.json, controller and attempt facts) | n/a (writer) | copies fields; `walked` is a count of rows on disk, not a judgment of the walk |
| `validate_artifacts.py :: check_run_report_coverage` (N3) | altered (refusal TEXT only) | data | xref (census :879, unchanged) | lanes counted unchanged |
| `story_run.py :: exit_limit_facts`, `_exit_go_on` (N4) | altered | intent (the person's words go to the role that halted) | n/a (executor) | equality of a digest hash; no reading of the role's words |

---

## §2 Measured facts (file:line, read in `D:/ws1/wt-fbfix`)

### B-16
- F1. `contract.prefix_value` (`PKG\scripts\contract.py:115-126`) returns a value only when it is ONE token. `stage_override_values` (:171-184)
  and `probe_gap_words` (:5154-5165) read `stage_overrides[]` through it.
- F2. An S5 window instance id is a phrase with spaces (live `pipeline.json` :562 `@regression LOCAL-1_TC_001 in-stock add shows success
  toast, badge 1 and one cart line`). It can never be a `probe gap:` value (F1).
- F3. Carriers of the instance-form door (critic t-1958 completed the list): `PKG\scripts\window_record.py:98` (`PROBE_GAP_RECORD`, used by
  `PROBE_GAP_DOOR` :99-100, the note at :1066, the `PROBE_GAP_UNRECORDED_KIND` row :328-331); `controller.py:6386-6390`
  (`_s5_completion_problems`; prints the concrete ticket `self._ticket()`); `controller.py:6563-6571` (`_s5_gap_problems`, same);
  `contract.py:5157-5158` (`probe_gap_words` docstring: `<instance id or case key>`); `PKG\design\state-exits.md:71` (`probe gap: <instance id
  or case key>`, twice); `PKG\skills\qa-story\phases\s5.md:164-165`; and `PKG\references\conductor-actions.json:121` (`go_on_as_is.run`:
  "waiver.py refuses any other" — false: a named block row of `block-names.json` is accepted, F4).
- F4. `waiver.block_name_row` (`waiver.py:589-608`) accepts a prefix row only with a one-token value; a block with spaces is refused
  `unmatched` (:746) — the 16:44 refusal (`thinking-roles.md:127`).
- F5. The case key IS read: `window_record.probe_gap_block` tries `[identity] + keys + [tooling]` (:636), `keys` = the case keys of the
  instance; `acceptance.probe_gap_named` the same (`acceptance.py:886-901`). Live `probe gap: LOCAL-1_TC_001` / `_002` closed S5.
- F6. `block-names.json:21` puts `class: probe_gap_accepted` on EVERY `probe gap: <x>` record, so any one such word (even a misspelled case
  key) is the class word for every green instance of the story whose probe the tool could not read (`contract.probe_gap_class_word`
  :5173-5205; `probe_gap_block` :638-640). A case key decides alone only where the class does not reach: a probe nobody ran (`not_run`) or a
  stand that was down — and there, by equality, it also closes sibling instances of that case (`probe_gap_block` excludes only `judged`,
  :645-647).
- F7. `proof_level.probe_could_not_run(task_root, identity, input_hash)` (`proof_level.py:1069-1082`): True for `incomplete` (not
  `cause: data_row`) or `not_executed` with `refused: tool` / `cause: tooling`; False for `not_run`, a stand down, a judged probe; never raises.
- F8. The seam: `Driver.window_round_gate` (`story_run.py:5924-6001`) → `no_move(call=False)` → `fallback_person`; `go on` → `take_seam_answer`
  → `seam_chosen` (:15990-16007) → `pass_block` (:4093-4103). The fallback options are data (`conductor-actions.json` `fallback` :208-212;
  `go on` says "go on without it; your words are recorded as the reason the story carries").
- F9. The `asked` transport of a list key exists for `rows`: `Person.__init__` (`story_run.py:481`), `_person_of` (:5109), `ask` (:3761-3762),
  `held_question` (:4089).
- F10. The driver rebuilds `work/windows/<critic dispatch>.json` on every finish (critic t-1958: `story_run.py:2918-2924`), so the record on
  disk is fresh at the seam.

### B-17
- F11. `manual_capture.http_login_source` (`manual_capture.py:4230-4257`): a kind other than `local_login` raises `EnvBlocked(..., "user",
  do_not_retry=True)` with NO `cause`; texts `manual-capture-steps.json:93-94`. A SENT and refused HTTP login is a `ValueError` (:4313-4332),
  never an env_blocked row (critic t-1958).
- F12. `_blocked` (:1311-1324) picks `blocked_login_user` (`build-identity-methods.json:119`, "... halt the block") for do_not_retry + no cause
  + owner user.
- F13. `_account_steps_gate` (:3048-3070), called by `ui` (:2806) and `app` (:3024), locks only on `do_not_retry is True and owner == "user"`.
- F14. `choose_attempt` (:317-348): a named do_not_retry attempt is refused with the login wording when `cause` is not `build`/`device`.
- F15. Live `work/evidence/manual/LOCAL-1_TC_014/a1/` (arm B tree): `env_blocked.json` (owner user, do_not_retry, no cause) and
  `probes.jsonl`, no `steps.jsonl`.
- F16. `steps.jsonl` rows are written by `Attempt.step` (`manual_capture.py:1130-1133`) with fields `at`, `command`, `step`, `outcome`,
  `detail`; a ui login refused after submit writes the failed `ui` step first (:2891) and then the row (:2889).
- F17. Readers of `do_not_retry` (excluding tests): `manual_capture.py` 24, `manual_evidence.py` 2 (`build_record` :1629-1643: "the login did
  not land: ... halt the block" for every do_not_retry row whose cause is not `build`), `device_stand.py` 2 (`_result` :542-544: `cause:
  "device"`, owner from the check), docs `references/manual-evidence.md:47-52,59`, `role-commands.json:45`, `design/state-exits.md:56`.

### B-18
- F18. No tool writes an `env_blocked` row for a manual case (`finalize_task.py:511-513` reads it only from run blocks).
- F19. An unprepared record is reducible: `finalize_task.py:536-562`; `write_block` accepts it (`manual_evidence.py:1281-1293`);
  `coverage_contract._validate_unprepared` (:685-702) checks reason = request, no `result`/`then_quotes`, same `obligation_ids`; extra keys in
  the `unprepared` dict are not refused.
- F20. `check_run_report_coverage` (`validate_artifacts.py:1930-2001`) counts `C.run_results` (:1979), which keys every
  `current_manual_checks` row by `case` (`contract.py:4284-4290`): a reduced unprepared record already passes the exit check.
- F21. (corrected, fix 8/12) The ONE S6 binder is `manual_evidence._running_dispatch(task, case)` (`manual_evidence.py:1367-1379`): the
  running S6 dispatch whose `scope` holds the case; none or two → `ValueError` with its own words. (`validate_artifacts._s6_runner_half`
  returns `(kind, case_ids)`, no id, no case scoping — not a binder.) `write_block` reads `dispatch_id`, `attempt_started_at`,
  `attempt_ended_at`, `source_revision` by `r[...]` (:1302-1305): a missing key is a `KeyError`; `main` catches `ValueError` only (:1988-1996).
- F22. `OBSERVATION_FILE_COMMANDS = ("build", "rejudge", "write-block")` (`manual_evidence.py:1772`): any other command given
  `--observations-file` is refused.
- F23. The runner's prompt line for an unprepared case (`story_run.py:12243-12246`, `run_manual_block`) names no command.
- F24. TC_014 `request.json` holds `unprepared.reason`, `obligation_ids: ["OB-14"]`, `source_revision`, `gate_a_decision_ref`.
- F25. `handoffs/vocabulary.yaml:30-68` has no row state for an unprepared walk.
- F26. (fix 11/12) Ratchet, measured by critic t-1958 (not re-run by the designer): `python -B PKG/scripts/role_load.py --role qa-runner
  --json` → `craft_tokens 1185`, `process_tokens 16701` = `role-load.json` `process_ratchet_tokens.qa-runner` 16701 (slack 0); total 17886 of
  `ratchet_tokens` 17887 (1 token). `qa-runner.md:51` today: "**Unprepared case:** walk it like any other."

### B-19 (traced by reading; logs `experiments/mybooks/thinking-roles/runs/arm-b-28.log` … `arm-b-32.log`)
- F27. Sequence S6-qa-runner-3: 17:35 halt answered `go on` (arm-b-28:2) → `resume_role` → `handoff` → exit gate refuses ("appears in no
  lane") → the free resume of `handoff_ladder` (`story_run.py:2602-2613`, log "resume S6-qa-runner-3: unclassified") → its result (17:47)
  is HALTING and becomes the saved result (`keep_resumed_result`) → next entry `_act_wait_existing_job` → `_finish_saved_result` → `handoff`
  → same set, already resumed (`handoff_ladder` :2596-2600) → `exit_limit(..., digest=digest)` → question at 17:49 whose lead says "The runner
  also says it cannot go on" (arm-b-28:25; built by `exit_limit_facts` :11270-11277 from `role_digest.is_halting(digest)`).
- F28. The person answered `go on` (arm-b-29:2): `_answer_exit_limit` → `_exit_go_on` (:11353-11381) writes one waiver per line and a
  finding, nothing else; `pending_words` stays empty (`exit_limit` popped it, :11147).
- F29. Next entry: `_act_wait_existing_job` (:15051) — no pending words (:15057), so the saved result → `_finish_saved_result` (:15128):
  `handoff` passes now (arm-b-29:6 "witness OK (re-run by the exit gate)"), then `_declared_halt(form, digest)` (:15135) on the SAME 17:47
  result → `Person("halt", ...)` (:15139) — the question of arm-b-29:7-38 (`asked_at` 17:00:35Z = 18:00 local).
- F30. Root cause: the halt check of `_finish_saved_result` (and of `resume_role` :3188) stands AFTER `handoff`, whose `exit_limit` seam
  already showed the halt to the person; the `go on` executor settles only the exit lines, and nothing records that this result's halt
  was put before the person. The halt road then asks it as new (FR-7).
- F31. Why the factory cannot simply finish over the halt: `story_step.finish`'s `_halt_gate` (`story_step.py:1854-1872`) refuses a declared
  halt unless `state/decisions/<D>.json` holds `open_work`/`close`. And `decide --close` is no executor here: for a stage-closing role it
  forces `complete = True` (`story_step.py:2404-2415`) — it would close S6 over the manual blocks still to run.
- F32. The control run: S6-qa-runner-4 (arm-b-32): its exit_limit lead has no "also says it cannot go on" (its later result did not halt);
  `go on` → "witness OK" → "accepted S6-qa-runner-4" — no second question. The defect needs a halting saved result at `exit_limit`.
- F33. `D:/ws1/exp-thinking-roles\pkg-b\...\story_run.py` (the driver that ran) has the same order: `_finish_saved_result` :15128,
  `handoff` :15130, `_declared_halt` :15135.
- F34. A pending word is the halt's own executor: `_act_wait_existing_job` resumes the role with `pending_words[dispatch]` BEFORE it looks at
  the saved result (:15057-15060); `resume_role` (:3141-3203) then judges the NEW result, and a new halt is asked with `again=True` (:3188-3192).
- F35. Prices are data per question id: `question-prices.json` `exit.resume_limit` (:161-166), `go on` = `factory: command` ("a factory
  command runs; no agent works"). The question-id census (`test_conductor_doors.py` K15, `QUESTION_SITE_RE` :626) reads literal ids of
  `closed_question("...")` call sites.

Analogs noticed, NOT widened (reported): `_stand_blocked` rows `remedy_no_revision` (:1264) and `remedy_no_probe_door` (:1292) are config
fixes with owner `user` (FR-46 class of N2); `_session_blocked` owner `environment` (:2659) is not locked; the "I cannot put that check's
reason" head of `question_from_refusal` for other refusals; where an accepted probe gap appears in the report — no reader in
`report_facts.py` (Grep `probe.gap|probe_gap` -i: no match there; positive control: the same Grep lists `check_delivery.py`,
`window_record.py` and 19 other files), so the N1 lead promises no report line (§5 Q2).

---

## §3 Nodes

### N1 — B-16: the door names the key the reader reads; `go on` at the seam reaches it

**Owns** (absolute; functions for hot files, D-0048):
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\window_record.py` (`PROBE_GAP_RECORD`, `PROBE_GAP_DOOR`, row `PROBE_GAP_UNRECORDED_KIND`, `probe_gap_cases` [new])
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\controller.py` (`_s5_completion_problems`, `_s5_gap_problems` — door text only)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\story_run.py` (`Person.__init__`, `_person_of`, `ask`, `held_question`, `window_round_gate`, `seam_chosen`, `probe_gap_lead` [new])
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\contract.py` (`probe_gap_words` — docstring only)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\conductor-actions.json` (`actions` row [new], `moves` `go_on_as_is.run`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\skills\qa-story\phases\s5.md` (:164-165)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\design\state-exits.md` (row :71)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json` (one row)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_gap_door.py` (new, fast)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-1955-n1.md` (new)

**Required behaviour**
1. `window_record.probe_gap_cases(window, root) -> list[tuple[str, list[str]]]` (new, pure, never raises): `[(case key, [instance ids])]`
   sorted by case key, from `window["scope_instances"]` (`{case: [iid]}`). An instance qualifies when ALL hold: `outcome == "passed"`; it is
   word-owed (the shape line `f"{iid}: {C.PROBE_MISSING_ERROR}"` is in `C.window_shape_errors(window)`, OR it carries a `probe_gap` block
   that `acceptance.probe_gap_named(window, root)` does not name); `proof_level.probe_could_not_run(root, iid, item["input_hash"])` is True.
   A case is listed only when EVERY green word-owed instance of it qualifies (one never-run or stand-down sibling keeps the whole case off
   the list: its instance keeps today's door). The list holds the qualifying instances of the case. A window that is no dict, no
   `scope_instances`, or an instance in no case → contributes nothing.
2. Door texts (F3), ONE constant: `PROBE_GAP_RECORD = person_words.door('waiver.py --task <T> --stage S5 --block "probe gap: <case key>"')`.
   The controller imports it and substitutes the ticket: `PROBE_GAP_RECORD.replace("<T>", self._ticket())` (both branches) — the printed
   door keeps the concrete ticket it prints today. Where the controller has the window it appends: `` The case keys this window needs:
   <k1>, <k2> (one record each). `` built from `probe_gap_cases` (omitted when the list is empty). `contract.py:5157-5158` docstring:
   `<case key>`; `state-exits.md:71`: `probe gap: <case key>` both times; `s5.md:164-165`: `<instance id or case id>` → `<case key>` plus
   "an instance id that is one token works too; a phrase with spaces is never a word the window reads". `go_on_as_is.run`: replace
   "one of the refusal's lines, whole; waiver.py refuses any other" by "one of the refusal's lines, whole, or a named block such as
   `probe gap: <case key>`; waiver.py refuses anything else".
3. The seam (transport on the `rows` pattern, F9): in `window_round_gate`, when `stage == "S5"` and `probe_gap_cases(<the record of
   work/windows/<refused dispatch>.json>, task_root)` is non-empty, the `no_move` state gains `"probe_gap_cases": [case keys]` and its
   `lead` is `probe_gap_lead(pairs)` instead of `lead + self.question_from_refusal(...)`. Transport: `Person.__init__` gets
   `self.probe_gap_cases = ()`; `_person_of` sets `person.probe_gap_cases = tuple(str(c) for c in state.get("probe_gap_cases") or ())`;
   `ask` writes `self.state["asked"]["probe_gap_cases"] = list(person.probe_gap_cases)` beside `rows` when non-empty; `held_question` restores
   `again.probe_gap_cases = tuple(str(c) for c in asked.get("probe_gap_cases") or ())`. No per-state `says`: the options are the unchanged
   `fallback` rows; the consequence lives in the lead.
   `probe_gap_lead(pairs)` — EXACT text (confirmed by the owner 05.11.2026 19:00 («по всем это ок»), §5 Q1; `human-questions.md` rules 1–4: what the factory
   did, why it cannot decide, whose gap, one question; no field, script, path or dispatch id; a case key is explained where it appears):
   > The review of this window of tests is finished. {n} test case(s) ran green, but for each of them the factory could not run the
   > check that proves the test would catch a broken product, because its own tool cannot read these tests: {list}. That is a gap in the
   > factory's tool, not a flaw in the tests, and only you can accept it.
   >
   > If you answer `go on`, the factory records your words once for each case named above. From then on your words cover every test of
   > this story whose check the tool could not read: the tests named here, other tests of the same cases, and tests in later windows of
   > this story. The tests themselves are not changed; they are only not checked that way.
   `{list}` = `; `-joined `<case key> (the test "<first instance id of the case>")`; more than 10 cases → the first 10, then `, and {k} more`.
   The `go on` option the person reads is the unchanged fallback row: "go on without it; your words are recorded as the reason the story
   carries" (`conductor-actions.json:210`), priced by its own row (`factory: record`, `person: none`, `delivery: not_known`).
4. `seam_chosen`: `move == "go_on_as_is"` and `asked.get("probe_gap_cases")` non-empty → for each case `self.pass_block("S5", f"probe gap:
   {case}", <the person's words file>, "Your word could not be recorded as the probe gap of " + case + ", so nothing more was passed.")`,
   then print `S5: the probe gap of <cases> is recorded on your word`. The existing `block` branch is unchanged and runs first when both are
   present.
5. `conductor-actions.json` `actions` row: `{"says": "the person accepts that tests whose probe cannot run here stay unprobed (a probe gap)",
   "run": "waiver.py --task <T> --stage S5 --block \"probe gap: <case key>\" --words-file <file>, once per case key the refusal names; never a
   line of the refusal and never `*`: the S5 window reads only this word; any one such word covers every test of the story whose check
   the tool could not read"}`; `go_on_as_is.run` gains "; at the S5 window, a probe gap: the `actions` row for it".
6. `question_from_refusal` is not changed (it stays for every other refusal; non-goal).

**Edges (each with its invariant)**
- E1.1 `probe_gap_cases` empty (red-only window, no record on disk, every instance never-run) → no state key; the seam is today's.
  INVARIANT: a red test is never closed by a person's word (FR-18).
- E1.2 An instance in two cases → both keys, if each case qualifies. INVARIANT: join by equality only.
- E1.3 (rewritten, fix 3) A probe nobody ran (`not_run`) or a stand that was down → its instance does not qualify, and its case is not
  listed; its existing door stays ("run the probe", or its own word). INVARIANT: the lead's "could not run" is true by data (FR-41), and a
  case word is never offered where it would close, by equality, a sibling nobody probed. A probe that JUDGED the current bytes, a record of
  other bytes and a red test still take no word (`probe_gap_block` :643-647, unchanged).
- E1.4 `pass_block` refused for one case → held question with the waiver's text; cases already recorded stay (append-only). INVARIANT:
  never "recorded" printed for an unrecorded word.
- E1.5 Temporal: words recorded before N1 (line waivers, `*`, case words) are read as today. INVARIANT: no retroactive pass (FR-4).
- E1.6 Positional: the probe-gap branch of `seam_chosen` runs only for move `go_on_as_is`. INVARIANT: no word recorded for a token the
  person did not choose.
- E1.7 (restated) The seam is `call: False`, the conductor is not consulted; an `asked` record written before N1 (no `probe_gap_cases`
  key) at a seam still open → today's path. INVARIANT: no key, no recording.
- E1.8 Limit: more than 10 cases → the lead lists 10 and "and <k> more"; all are recorded.
- E1.9 Next move after recording: `seam_chosen` returns, the loop goes back through `where` to the finish, the window record is rebuilt
  (F10). No other line left → S5 closes as in the live run. Other lines left → the set differs → the conductor or the cap, as today.
  INVARIANT: recording the probe-gap words never passes another line.
- E1.10 A misspelled key typed by a conductor through the `actions` row still acts story-wide (F6); the lead says so. INVARIANT: code never
  types a key itself — the keys come from `scope_instances`.

**Non-goals**: `probe_gap_words`, `probe_gap_block`, `probe_gap_named`, `waiver.py` logic; a new token; `question_from_refusal`; the probe
tool (N6 of t-1936); a report line for accepted probe gaps (§5 Q2).

**DoD** — `test_probe_gap_door.py` (fast; `Driver` stubbed as in `test_stage_review_person_pass.py`; NOT added to `slow_tests.json`):
`test_cases_from_shape_line_green_could_not_run`, `test_cases_from_unnamed_probe_gap_block`, `test_red_instance_gives_no_case`,
`test_instance_in_two_cases_gives_both`, `test_seam_go_on_skips_never_run_probe` (a case with one `not_run` sibling is not listed),
`test_door_text_names_case_key_placeholder` (all F3 sites print `<case key>`; none prints `<IID>` or `<instance id>`),
`test_controller_door_keeps_concrete_ticket`, `test_controller_refusal_lists_concrete_cases`,
`test_door_block_is_accepted_by_block_name_row` (`waiver.block_name_row("probe gap: LOCAL-1_TC_001", "S5")` is a row; the phrase form is
None), `test_asked_carries_probe_gap_cases_and_held_question_restores`, `test_lead_says_class_scope` (the lead holds "every test of this
story whose check the tool could not read" and "later windows"), `test_seam_go_on_records_one_word_per_case`,
`test_seam_go_on_without_cases_unchanged`, `test_seam_retry_records_nothing`, `test_recorded_case_word_is_read_by_probe_gap_words`.
Census row: `{"file": "window_record.py", "function": "probe_gap_cases", "class": "xref", "roles": ["conductor"], "owner": "intent"}`.
Witness (fast, from the worktree root): `python -m pytest ai-packages/qa-factory/scripts/tests/test_probe_gap_door.py
ai-packages/qa-factory/scripts/tests/test_judgment_census.py -q`. CI only (SLOW / slow files): `test_probe_gap_word.py`,
`test_controller_*`, `test_story_run_*`, `test_conductor_doors.py`. `architecture:` AR-1, AR-9, AR-13, AR-16, AR-24, AR-25, AR-29.

### N2 — B-17: a login the factory does not know is the factory's, and locks nothing

**Owns** (absolute):
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\manual_capture.py` (`LOGIN_UNKNOWN_CAUSE` [new], `http_login_source`, `_blocked`, `choose_attempt`, `_account_steps_gate`, `EnvBlocked` docstring)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\manual_evidence.py` (`build_record` — the env_blocked branch :1629-1643 only)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\build-identity-methods.json` (`refusals`: new key `blocked_login_unknown`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\manual-capture-steps.json` (`login.words.not_known_door`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\manual-evidence.md` (:47-52)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_manual_capture_login_unknown.py` (new, fast)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-1955-n2.md` (new)

**Required behaviour**
1. `http_login_source` (:4256): `EnvBlocked(<not_known_line>, <not_known_door>, "factory", do_not_retry=True, cause=LOGIN_UNKNOWN_CAUSE)`;
   `LOGIN_UNKNOWN_CAUSE = "login_unknown"` is a module constant (one producer). STABLE: spec t-1957 depends on its name and value.
2. `_blocked` (:1321): `cause == LOGIN_UNKNOWN_CAUSE` is tested FIRST → key `blocked_login_unknown`: "manual_capture: the login by code was
   not tried ({probe_line}); nothing was sent and nothing was captured. This is the factory's gap, not the account's: a screen case signs
   in through `fill-account` steps in a new attempt, and a seed the factory cannot do by API is done through the screens. The block goes
   on. Remedy for the project: {remedy}, owner {owner}". No "halt".
3. `not_known_door` (:94): "a screen case signs in with fill-account steps, and a seed is done through the screens; for the project: record
   manual_capture.login.http in config.json (path and token_field), or null if this kind of capture needs no login".
4. `choose_attempt` (:323-339): a named attempt whose row has `cause == LOGIN_UNKNOWN_CAUSE` → "attempt <a> holds a login by code that was
   not tried (nothing was sent); capture into a new attempt (leave --attempt out)". No "halt".
5. `_account_steps_gate` (:3064-3070) locks ONLY when the last attempt's row has `do_not_retry is True`, `owner == "user"`, and EITHER a
   `cause` other than `LOGIN_UNKNOWN_CAUSE`, OR no `cause` and the LAST parseable row of that attempt's `steps.jsonl` has `outcome ==
   "failed"` and `command == "ui"`. Order: the cause test first, then the step evidence. Refusal text when it locks: unchanged.
6. `manual-evidence.md:47-52`: one sentence for the new cause ("not tried, nothing sent: the factory's gap; sign in through `fill-account`
   and do the seed through the screens; the block goes on").
7. `manual_evidence.build_record` env_blocked branch (:1633-1640): `cause == LOGIN_UNKNOWN_CAUSE` (imported from `manual_capture`) → `why` =
   " (the login by code was not tried and nothing was sent: capture the case again as a new attempt, signing in through fill-account
   steps; the block goes on)" — no "halt"; and the leading "Put the case in env_blocked[] ..." sentence is NOT said for this cause (it is no
   gap of the stand): the message is "attempt <a> of <case> has no record: <probe_line>." + that `why`. Other causes: unchanged.

**do_not_retry sibling enumeration (rule 9; readers: `choose_attempt`, `_account_steps_gate`, `_blocked`, `build_record`)**

| site | row (owner / cause) | what a retry by the screen meets | verdict |
|---|---|---|---|
| `_stand_blocked` :1259 other build / content | user / build | the same stand | lock right — keep |
| :1264 no revision | user / build | the same refusal | keep (owner is a config fix: analog reported) |
| :1269 device unready | user / device | the same device | keep |
| :1271 word for another story | user / build | the same word | keep |
| :1274 unknown asks the person | user / build | the same unknown | keep |
| :1275 retry remedy | user / none, no lock | heals by itself | no lock — right |
| :1292 no runtime probe | user / build | the same missing probe | keep (analog reported) |
| :1303 probe raised | user / none, no lock | may heal | no lock — right |
| `AppiumBackend._blocked` :1947 | factory or user / device | the same device | keep |
| `device_stand._result` :542-544 | owner of the first problem check / device | the same device | keep (same verdict as the Appium row: `cause: device` stays locked by item 5's first branch) |
| `_login_blocked` via :2871 before submit | factory / none | another page route | not locked — right |
| `_login_blocked` via :2889 after submit | user / none, last step `ui` failed | the same refused account | keep (item 5's step branch) |
| `_session_blocked` :2659 not_landed | environment / stand | a changed stand | not locked — left (analog reported) |
| `http_login_source` :4256 not-known kind | user / none → factory / login_unknown | nothing was sent | WRONG today — changed by this node |
| `build_record` :1629-1643 (reader) | any do_not_retry row | — | "halt" for login_unknown WRONG — item 7 |

**Edges**
- E2.1 Temporal (F15): the a1 row of TC_014 (owner user, no cause, no `steps.jsonl`) → NOT locked (no cause, no failed `ui` last step).
  INVARIANT: an attempt where nothing was sent never locks the screen route. The row on disk is never rewritten.
- E2.2 An old row of a ui login refused after submit (last `steps.jsonl` row `command ui`, `outcome failed`) → locked. INVARIANT: "a refused
  account is not retried" (t-292 Q2) holds for every row that proves a sent login.
- E2.3 Error direction of item 5 (a reused gate in a more consequential role): it may err toward NOT locking. Must stay locked: a ui login
  refused after submit; a row with `cause` `build`/`device`. Must now be open: the F15 shape; an attempt whose earlier `ui` call failed a
  `see` step and whose LAST row is a later non-`ui` step or none of `ui` (the last-row rule). There is no producer of an "http account
  refusal row with no step" (F11: a sent HTTP login refusal is a `ValueError`, never a row). An unreadable `steps.jsonl` → "no failed `ui`
  last row" for a no-cause row only; a locking cause locks regardless.
- E2.4 Non-JSON lines of `steps.jsonl` are skipped; the last PARSEABLE row counts; an empty file = no row.
- E2.5 Positional: the cause test in `_blocked` and in `build_record` is FIRST. INVARIANT: a not-tried login is never told as "did not land"
  and never says halt.
- E2.6 `http --as` again after the row: the same refusal, a new attempt, no lock. A new row on `choose_attempt` without `--attempt` → a new
  attempt.

**Non-goals**: owner words of `remedy_no_revision`/`remedy_no_probe_door`; `_session_blocked`; writing `login.http` for the project; the
S6 lane of the case (N3); any `manual_evidence.py` function other than `build_record`.

**DoD** — `test_manual_capture_login_unknown.py` (fast, fakes as in `test_manual_capture_session.py`):
`test_not_known_kind_row_is_factory_login_unknown`, `test_blocked_text_says_not_tried_and_no_halt`, `test_steps_gate_open_after_login_unknown`,
`test_steps_gate_open_for_old_row_without_steps` (the F15 shape, byte-for-byte), `test_steps_gate_locked_for_old_row_last_ui_failed`,
`test_steps_gate_open_when_failed_see_then_later_row` (negative of the last-row rule: an earlier failed `see` step, a later no-cause http
row → not locked), `test_steps_gate_locked_for_build_cause`, `test_steps_gate_locked_for_device_cause`,
`test_choose_attempt_login_unknown_says_new_attempt`, `test_unreadable_steps_file_no_cause_not_locked`,
`test_build_record_login_unknown_says_new_attempt_no_halt`, `test_build_record_build_cause_unchanged`, `test_refusal_texts_are_data_rows`.
Witness (fast): `python -m pytest ai-packages/qa-factory/scripts/tests/test_manual_capture_login_unknown.py
ai-packages/qa-factory/scripts/tests/test_manual_capture_session.py ai-packages/qa-factory/scripts/tests/test_login_body_fields.py
ai-packages/qa-factory/scripts/tests/test_judgment_census.py -q` (none of these is in `slow_tests.json`: Grep of the four names gave no
match, positive control `test_conductor_doors.py` matched in the same call). `python -B ai-packages/qa-factory/scripts/selftest.py --lang`.
`architecture:` AR-1, AR-9, AR-13, AR-25, AR-27, AR-29.

### N3 — B-18: an unprepared case always has an outcome the runner's tool writes

**Owns** (absolute):
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\manual_evidence.py` (`write_unprepared` [new], `write_block` key check, `main` subcommand `unprepared`, `OBSERVATION_FILE_COMMANDS`, `unprepared_rows`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\story_run.py` (`run_manual_block` — the prompt line :12243-12246 only)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\validate_artifacts.py` (`check_run_report_coverage` — refusal text only)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\check_delivery.py` (`unprepared_records` — `to_check` text)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\handoffs\vocabulary.yaml` (`row_states`: `unprepared_walk` [new])
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_unprepared_outcome.py` (new, fast)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-1955-n3.md` (new)

**Producer and readers that change together (AR-22)**: `write_unprepared` → `write_block` (one writer, unchanged) → `finalize_task`
(:536-562, unchanged) → `run-report.json` `current_manual_checks` → `contract.run_results` (unchanged; F20), `coverage_contract`
(unchanged), `unprepared_rows` (+ `walked`, `not_walked`), `ledger.unprepared_walks` (unchanged), `check_delivery.unprepared_records`
(`to_check` "not walked: <why>" when `walked` is false), `s7_pretriage` (unchanged). `vocabulary.yaml` `unprepared_walk` is a data row
only: no `handoff_check` cross-check of row state against the run report exists (critic t-1958).

**Required behaviour**
1. `manual_evidence.write_unprepared(task, case, observations, not_walked="") -> Path` — SIGNATURE STABLE (spec t-1957 E2.7 calls it).
   Builds ONE record and calls `write_block(task, [record], declared=True)`. `dispatch_id = _running_dispatch(task, case)` (the one binder,
   F21; its `ValueError` is the refusal, unchanged). Walk evidence, from disk: the attempts of the case (`MC.attempts_of(<case evidence
   dir>)`) that hold ≥ 1 parseable `steps.jsonl` row; `walked` = at least one such attempt exists. When walked: `attempt_id` = the newest such
   attempt (so `_hand_surprises` carries its recorder `surprise` lines, P26), `attempt_started_at` / `attempt_ended_at` = the first / last
   `at` of its `steps.jsonl` + `probes.jsonl` rows. When not walked: no `attempt_id`, both times = now (UTC ISO). Fields: `case`;
   `unprepared` = `{"reason": <request.json unprepared.reason>, "walked": <derived>}` plus `"not_walked": <why, whitespace folded, cut at 300
   with "…">` when not walked; `obligation_ids` = the request's; `observations` = the given list (`[]` allowed); `source_revision` = the
   request's `unprepared.source_revision`, else the controller state's. No `result`, no `then_quotes`.
2. CLI: `manual_evidence.py unprepared --task-root <r> --case <C> [--observations-file <f>] [--not-walked "<why>"]`; `"unprepared"` is added
   to `OBSERVATION_FILE_COMMANDS`. `--not-walked` is REQUIRED when no attempt holds a step ("nothing of <C> was walked with the recorder: say
   why with --not-walked, or walk it first"), and REFUSED when one does ("<C> was walked (attempt <a> holds <n> step(s)): leave
   --not-walked out"); blank → "say why it was not walked".
3. `write_block`: a record missing `dispatch_id`/`attempt_started_at`/`attempt_ended_at`/`source_revision` → `ValueError` naming the keys.
4. `vocabulary.yaml` `row_states`: `unprepared_walk` — "an unprepared manual-agent case closed by `manual_evidence.py unprepared`, walked or
  not; no pass or fail", used_by qa-runner.
5. Prompt line (`run_manual_block`, the ONLY carrier, F26 — `qa-runner.md` is not changed): `<case>: unprepared - <reason>; walk it
   yourself with the recorder (manual_capture.py) or the browser and record every doubtful place; a seed the recorder cannot do by API is
   done through the screens, and a capture the factory refuses for its own gap halts nothing; close the case with `manual_evidence.py
   unprepared --task-root <r> --case <case> --observations-file <file>` (add `--not-walked "<why>"` when nothing was walked with the
   recorder); record no pass or fail`.
6. `check_run_report_coverage` text (:1993-1996) appends "An unprepared case is closed by `manual_evidence.py unprepared` (walked or not)."

**Edges**
- E3.1 No running S6 dispatch with the case in scope, two, or the case outside the running dispatch's scope → `_running_dispatch`'s own
  refusal; nothing written. INVARIANT: a record never binds to a guessed dispatch.
- E3.2 `request.json` without `unprepared` → refused ("this case was prepared; use `build`" / "was refused: not checked by hand").
  INVARIANT: the marker is honoured only where code wrote it.
- E3.3 `observations` not a list → the CLI's existing refusal. Empty list → legal (AR-23).
- E3.4 A second call for the same case → a second block; `finalize_task` keeps the latest per case::obligation. INVARIANT: no in-place edit.
- E3.5 A record with `result` cannot come from this command; a hand `write-block` with `result` + `unprepared` is still refused.
  INVARIANT: no pass/fail from an unprepared walk (FR-59).
- E3.6 Temporal: arm B's TC_014 has no manual record and an S6 `go on` word for the "no lane" line; after N3 the word stays and passes as
  today. A runner dispatch started BEFORE N3 lands has the old prompt line: its record is written by the NEXT runner dispatch of that case
  (the new line), never by the conductor; a hand `write-block` stays legal. INVARIANT: the record's writer is the runner's tool.
- E3.7 Positional: `write_unprepared` goes THROUGH `write_block`. INVARIANT: one writer of manual blocks.
- E3.8 `case` with `/` → the recorder's `case_dir_name` rules.
- E3.9 `walked` is never the runner's word: it is derived (P26). A runner that walked with the MCP browser and no recorder has no steps
  → `--not-walked` required; it says so and records its observations. INVARIANT: no "walked" without a recorder step on disk.
- E3.10 The case's attempts hold only env_blocked rows (TC_014 a1) → not walked. INVARIANT: an env_blocked attempt is not a walk.
- E3.11 `write_block` refuses an `attempt_id` on an unprepared record (not expected by reading `_validate_unprepared`) → the builder STOPS
  and returns the refusal as a question; the field is never dropped silently.
- E3.12 A 64-hex `source_revision` from the request is a plan hash, not a git head; it flows into the block `head`; no reader compares it
  to the stand revision (`finalize_task` uses the controller's own :639). Stated, unchanged.

**Non-goals**: an `env_blocked` lane for manual cases; `finalize_task`, `coverage_contract`, `ledger`, `s7_pretriage`; `qa-runner.md`; the
delivery verdict of a requirement checked only by an unprepared walk (t-1936 fork 13); the signature of `write_unprepared` after this node.

**DoD** — `test_unprepared_outcome.py` (fast): `test_write_unprepared_walked_record_shape` (attempt_id = newest attempt with steps; times
from its rows), `test_walked_carries_recorder_surprises`, `test_write_unprepared_not_walked_carries_reason`, `test_not_walked_required_without_steps`,
`test_not_walked_refused_with_steps`, `test_env_blocked_only_attempt_is_not_walked`, `test_no_running_dispatch_refused`,
`test_case_outside_dispatch_scope_refused`, `test_prepared_case_refused`, `test_blank_not_walked_refused`,
`test_observations_file_read_by_unprepared`, `test_write_block_missing_key_is_valueerror`,
`test_finalize_carries_record_into_current_manual_checks`, `test_exit_check_accepts_unprepared_case` (control: without the record the case is
named), `test_unprepared_rows_carry_walked`, `test_left_item_says_not_walked`, `test_prompt_line_names_the_command`,
`test_vocabulary_has_unprepared_walk`.
Witness (fast): `python -m pytest ai-packages/qa-factory/scripts/tests/test_unprepared_outcome.py
ai-packages/qa-factory/scripts/tests/test_validators.py ai-packages/qa-factory/scripts/tests/test_manual_evidence.py
ai-packages/qa-factory/scripts/tests/test_judgment_census.py -q`; ratchet: `python -B ai-packages/qa-factory/scripts/role_load.py --role
qa-runner --json` (`process_tokens` ≤ 16701, total ≤ 17887 — unchanged; `test_role_load.py` is not the ratchet). `architecture:` AR-10,
AR-13, AR-14, AR-21, AR-22, AR-23, AR-25, AR-27, AR-28, AR-29.

### N4 — B-19: the halt a person already answered at `exit_limit` is not asked again

Root cause: §2 F27–F31 (established by reading code and logs; the one fact not on disk any more — whether the 17:47 halt was in the form, the
digest or both — does not matter: the 17:49 lead proves the digest halted, F27).

**Owns** (absolute; functions):
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\story_run.py` (`exit_limit_facts`, `exit_limit_person`, `_exit_go_on`, `halt_key` [new staticmethod])
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\question-prices.json` (`questions` key `exit.resume_limit_halted` [new])
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_exit_limit_halt_answered.py` (new, fast)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-1955-n4.md` (new)

**Required behaviour** (direction = §5b fork F8, recommendation A; executable on it)
1. `Driver.halt_key(digest) -> str`: `hashlib.sha256(" ".join(str(digest or "").split()).encode("utf-8")).hexdigest()[:16]`, `""` for an
   empty digest.
2. `exit_limit_facts`: the returned dict gains `"halt": self.halt_key(digest) if halting and sid and why != "session_gone" else ""`. When
   `halt` is set, the `go on` option's `says` is `shown + f"; first {who} reads your words once in its own session and hands its work over
   again, because it also said it cannot go on"` and its `slots` are `{"role": who}`. Nothing else in the facts changes.
3. `exit_limit_person`: two literal sites, so the question-id census reads both (F35): `self.closed_question("exit.resume_limit_halted",
   lead, ask["options"])` when `ask.get("halt")`, else `self.closed_question("exit.resume_limit", lead, ask["options"])`.
4. `question-prices.json`: `exit.resume_limit_halted` = the four rows of `exit.resume_limit`, except `go on`: `{"answer": "go on",
   "factory": "role_round", "person": "none", "delivery": "not_known", "unverified": "what the check named stays as it is; your words are
   kept as the reason, with the decisions you made"}`.
5. `_exit_go_on`, LAST (after every `pass_block` and the `owe_row`): when `(rec.get("ask") or {}).get("halt")` equals
   `self.halt_key(self.digest_of(self.saved_result(dispatch).get("result") or ""))`, set `self.state["pending_words"][dispatch]` = the
   person's words WHOLE (the text of `self.task_root / file`, else `words`; FR-8) and print `{stage}: {dispatch} also said it cannot go on;
   it reads your words once in its own session, and the question it stopped on is not asked again`. `_answer_exit_limit` then saves state
   as today. The next entry resumes the role with those words (F34); `resume_role` judges the NEW result.

**Edges (each with its invariant)**
- E4.1 The lead did not say the role halted (`halt` == "") → `go on` as today; a halt found later is asked. INVARIANT: a halt is settled
  only by an answer to a question that SAID the role stopped (FR-7 applies to answered boundaries only).
- E4.2 Positional: the words are set AFTER every waiver row is written. INVARIANT: a refused waiver (held question) never leaves pending
  words behind — the role is never resumed over a pass that was not recorded.
- E4.3 The saved result changed between the ask and the answer (keys differ) → no words; the halt road asks the new result's halt.
  INVARIANT: only the halt the person saw is settled.
- E4.4 A NEW halt after the resume (`resume_role` :3188) → asked with "stopped again". INVARIANT: a halt the person has not seen is always
  asked (the Lead's invariant for this node).
- E4.5 `round` / `fresh` / `stop` and every non-token answer → unchanged (`round` already gives the role the words; `fresh` releases;
  `stop` holds). INVARIANT: only `go on` gains the words.
- E4.6 No session (`sid` "") or `why == "session_gone"` → `halt` is "", the old question id and prices, and the halt is asked afterwards as
  today. INVARIANT: no option promises a resume that cannot run (FR-10). Named residual: one extra question in this sub-case.
- E4.7 Temporal (a story on disk in that state): (a) an `exit_limit` question open when N4 lands has an `ask` without `halt` → E4.1, today's
  path; (b) a stale halt already asked (arm B, answered 18:02) → answered as today. INVARIANT: nothing is settled retroactively; the error
  direction is one extra question, never a lost halt. The halt key exists only from the first `exit_limit` raised after N4.
- E4.8 The resume fails with no words (session gone) → `resume_role`'s existing roads (`handoff` refusal; the words stay in
  `pending_words`, t-781 m2). INVARIANT unchanged.
- E4.9 The role answers the words and its new result still fails the exit lines that `go on` passed → the waivers pass them (`handoff`
  reads them); other new lines → the ladder as today.

**Non-goals**: the order of the halt check against `handoff` in `_finish_saved_result` / `resume_role` / `run_role` (fork F8 option C);
`story_step.finish` / `_halt_gate` / `decide`; the role's words in the halt question; other `exit_limit` callers.

**DoD** — `test_exit_limit_halt_answered.py` (fast; `Driver` stubbed, no `claude`): `test_facts_keep_halt_key_for_halting_digest`,
`test_facts_no_halt_key_without_halt`, `test_facts_no_halt_key_without_session`, `test_go_on_option_says_role_reads_words_when_halting`,
`test_person_uses_halted_question_id`, `test_go_on_after_shown_halt_sets_pending_words_whole`, `test_go_on_without_halt_sets_no_words`,
`test_go_on_saved_result_changed_sets_no_words`, `test_refused_waiver_sets_no_words`, `test_old_ask_without_halt_key_is_today`,
`test_wait_existing_job_resumes_instead_of_asking_halt` (pending words → `resume_role`, `_finish_saved_result` not called),
`test_new_halt_after_resume_is_asked_again`, `test_prices_row_exists_and_go_on_is_role_round`.
Witness (fast): `python -m pytest ai-packages/qa-factory/scripts/tests/test_exit_limit_halt_answered.py
ai-packages/qa-factory/scripts/tests/test_judgment_census.py -q`. CI only: `test_story_run_exit_limit.py`, `test_conductor_doors.py` (K15
census of question ids), `test_no_move_seam.py` (all in `slow_tests.json`). `python -B ai-packages/qa-factory/scripts/selftest.py --lang`.
`architecture:` AR-16, AR-22, AR-24, AR-25.

---

## §4 Parallelism

N1, N2, N3, N4 may run in parallel. Owns by function:
- `story_run.py` (hot): N1 {`Person.__init__`, `_person_of`, `ask`, `held_question`, `window_round_gate`, `seam_chosen`, `probe_gap_lead`};
  N3 {`run_manual_block`}; N4 {`exit_limit_facts`, `exit_limit_person`, `_exit_go_on`, `halt_key`} — disjoint (D-0048: the later node
  merges the batch branch, resolves, one critic after the merge).
- `manual_evidence.py`: N2 {`build_record` env_blocked branch}; N3 {`write_unprepared`, `write_block`, `main`, `OBSERVATION_FILE_COMMANDS`,
  `unprepared_rows`} — disjoint. N2's `build_record` imports `LOGIN_UNKNOWN_CAUSE` from `manual_capture.py` (N2's own file).
- `manual_capture.py` only N2; `controller.py`, `window_record.py`, `contract.py`, `conductor-actions.json`, `s5.md`, `state-exits.md`,
  `judgment-census.json` only N1; `question-prices.json` only N4; `vocabulary.yaml`, `validate_artifacts.py`, `check_delivery.py` only N3;
  `build-identity-methods.json`, `manual-capture-steps.json`, `manual-evidence.md` only N2.
- Text dependency, not an order: N3's prompt line carries N2's sentence (seed through the screens, no halt); each node is right on its own.
Each node's witness is its own fast test file(s) (rule 4, builder-rules 7b); the batch canon is CI on the batch branch. After this batch:
t-1957 (it calls `write_unprepared` and imports `LOGIN_UNKNOWN_CAUSE`, and edits `run_manual_block`).

## §5 Questions for the owner

- **Q1 (F1 lead wording, intent: what the person consents to).** The N1 lead (§3 N1 item 3) tells the person that `go on` covers every test
  of this story whose check the tool could not read — the named tests, other tests of the same cases, and tests in later windows — not only
  the list. Is this what the owner wants the person to consent to, in these words? Written by recommendation until the owner's word; N1 is
  executable on it.
- **Q2 (where an accepted probe gap reaches the person's report).** No reader in `report_facts.py` names accepted probe gaps (§2, analogs),
  so the lead promises no report line. Should accepted probe gaps be listed under "Left with you" (a new node, not this batch)?
  Recommendation: yes, as a finding into the report pile.

## §5b Fork for the Lead (from the N4 trace; technical)

- **F8 (executor of a halt shown inside `exit_limit`).** A (recommended; N4 as written): `go on` over a question that said the role halted
  hands the person's words to the role once (pending words; a new price row `role_round`); one question, one runner session; FR-7 holds; the
  new halt is still asked. B: record `story_step.py decide --close` — refused: for a stage-closing role it closes the stage over the work
  still to run (F31). C: move the halt check before `handoff` in `_finish_saved_result` and `resume_role` (as `run_role`'s early check), so a
  halting result never reaches `exit_limit`; it fixes new stories only (a story with an answered `exit_limit` and a halting saved result
  would still be asked), and it puts two questions where A puts one when the role also fails the exit gate. A and C combine; C is not needed
  for B-19.

Small choices closed by the designer (no design weight): constant name `LOGIN_UNKNOWN_CAUSE`; test file names; `not_walked` cut at 300
(`PROBE_GAP_WHY_LIMIT` value); timestamps `now` when no attempt holds steps; the lead cut at 10 cases; `probe_gap_cases` returns `(case,
[instances])` pairs and the lead names each case by its first instance id; `walked` reads ANY attempt with steps (not only the latest:
a later env_blocked attempt must not hide a walked one) and `attempt_id` = the newest such attempt; `halt_key` = 16 hex of sha256 over the
whitespace-folded digest.

## §6 Live proof (FR-33) on the arm B tree

All on a scratch COPY of `D:/ws1/mybooks-stand\tr-arm-b\qa-factory\artifacts\LOCAL-1` while a driver runs there (command hygiene 7(d)).
- N1: on the copy, revoke the two `probe gap:` words, rebuild the S5 window record, run `story_step finish`: the refusal names `probe gap:
  <case key>` with LOCAL-1_TC_001, LOCAL-1_TC_002 and the concrete ticket; `seam_chosen` with `go on` records both; `finish` closes S5.
- N2: on the copy, `manual_capture.py ui --task-root <copy> --case LOCAL-1_TC_014 --steps <fill-account steps>`: no `_account_steps_gate`
  refusal. Control: a copy whose a1 holds a last `steps.jsonl` row `command ui`, `outcome failed` → refused.
- N3: on the copy, with a running S6 dispatch scoped to TC_014, `manual_evidence.py unprepared --case LOCAL-1_TC_014 --not-walked "<why>"`,
  `finalize_task.py`, `validate_artifacts.py`: no "appears in no lane" line for TC_014.
- N4: the next live run in which a halting runner reaches `exit_limit` (Lead's call): the driver log shows `go on` → "<dispatch> also said
  it cannot go on; it reads your words once ..." → `resume <dispatch>` → no `kind: halt` question for the same result.

## Reading trail

Critic verdict `docs/tasks/specs/reviews/t-1958-critic-plan-manual-lane-doors.md` (whole). Notebook `thinking-roles.md:130-141`. Driver
logs `runs/arm-b-28.log`, `arm-b-29.log`, `arm-b-30.log`, `arm-b-31.log`, `arm-b-32.log` (whole). Live tree: `work/handoffs/S6-qa-runner-3.yaml`
(Grep `verdict`: now `concerns` — overwritten after the 18:02 answer). Package (wt-fbfix): `story_run.py` 470-510, 2470-2620, 2660-2920,
3060-3220, 3745-3770, 4078-4137, 5098-5127, 5550-5670, 11078-11433, 12236-12249, 15051-15210; `story_step.py` 1723-1752, 1845-1873,
2385-2424, 2571-2610, 2690-2850; `contract.py` 5152-5165; `controller.py` 6380-6393, 6558-6573; `window_record.py` 94-101, 620-649
(+ Grep `probe_could_not_run|input_hash`); `proof_level.py` 1069-1083; `manual_evidence.py` 1364-1380, 1620-1644, 1750-1772;
`manual_capture.py` 1130-1142 (+ the first draft's trail); `device_stand.py` 536-547; `qa-runner.md` 49-52; `references/human-questions.md`
13-114; `conductor-actions.json` 112-131, 200-213 (+ top-level keys); `question-prices.json` 155-175; `design/state-exits.md` 68-72;
`scripts/slow_tests.json` (Grep). pkg-b `story_run.py` (Grep: 3188, 15128-15135). Ratchet numbers: critic t-1958's run of `role_load.py`
(not re-run here). First draft's trail (unchanged facts): `contract.py` 115-184, 4252-4325, 5132-5240; `acceptance.py` 874-913;
`waiver.py` 580-760; `manual_capture.py` 175-348, 1243-1324, 1925-1954, 2654-2660, 2795-2929, 3040-3070, 4150-4284, 4440-4499;
`manual_evidence.py` 1256-1319, 1887-2006; `coverage_contract.py` 675-734; `finalize_task.py` 470-669; `validate_artifacts.py` 1890-2001;
`handoffs/vocabulary.yaml` 25-75; census rows :216, :490, :879.
Needed beyond the manifest: `story_step.py` (`_halt_gate`, `decide`, `_decision_of`) and `question-prices.json` for N4; `device_stand.py`
for the sibling row; the live `S6-qa-runner-3.yaml`; pkg-b `story_run.py`.
