# t-1971 — critic gate on the DIFF, batch t-1955 «manual-lane doors» (N1 B-16, N2 B-17, N3 B-18, N4 B-19 + integration + fix round)

Diff: `git -C D:/ws1/wt-fbfix diff d85a91e0a 2447ec263 -- ai-packages plans/features.json` (38 files, +1458/-82; tree read at 32c1223c7).
Against: spec `docs/tasks/specs/t-1955-manual-lane-doors.md` (whole, §1–§6, the «Decided» lists), brief `docs/tasks/critic-diff-brief.md`
(items 1–11), reports t-1961/1962/1963/1964/1966/1969, notebook `experiments/mybooks/thinking-roles/thinking-roles.md` lines 127–169.

**Verdict: fit_with_fixes.** The four doors open on the live evidence as specified. Two MERGE-BLOCKING mechanical reds on CI pipeline 8042123
(both caused by this diff, both one-line fixes), plus non-blocking fixes for the same fix round (F6-30: minor findings are fixed, not carried).

## Blocking (the merge waits for these; both one line)

- **B1. lint ratchet red (`forge-check`, job 28211416):** `manual_evidence.py:1442` `request = _load_request(...)` — "local variable 'request' is
  assigned to but never used [UnusedVariable]". The call is made for its refusal only; drop the assignment (call it bare). Also brief item 7
  (work whose result nobody reads).
- **B2. A22 process ratchet red (`package-fast` job 28211417 audit A-K1 and `install-smoke` 28211421):** "qa-runner carries 16,699 process
  tokens, below its row 16,701: lower to 16699 (`process_ratchet_tokens` in references/role-load.json)". The fix round's shrink of
  `references/manual-evidence.md` left slack the shrink-only ratchet must absorb: `references/role-load.json:32` 16701 -> 16699 (a LOWER,
  axis 18 allows it; named here). Check the total row `:18` (17887; measured 17884) with the same audit after the edit.

## Non-blocking findings (fix in the same fix round unless marked queue)

1. **DUPLICATION — two new tolerant JSONL readers of the same file `steps.jsonl`:** `manual_capture._last_step_row` (`manual_capture.py:3071`)
   and `manual_evidence._rows_of` (`manual_evidence.py:1398`), beside the strict `manual_evidence._jsonl` (:1339), `Attempt._lines`
   (`manual_capture.py:1096`) and `story_run._read_jsonl` (:565). `manual_evidence` already imports `manual_capture` (`_recorded_walks`):
   one tolerant `MC.step_rows(attempt_dir)` with `_last_step_row = rows[-1]` removes a twin and keeps N2's "last parseable row" and N3's
   "≥ 1 parseable row" on ONE reading. Fix now (cheap).
2. **DUPLICATION — the controller's "case keys this window needs" suffix is copy-pasted** in `_s5_completion_problems` (`controller.py:6392`)
   and `_s5_gap_problems` (:6574), two styles (one with a walrus). The spec makes `PROBE_GAP_RECORD` the ONE door text (AR-13); the suffix
   belongs next to it (`window_record.probe_gap_keys_line(window, root)`). Fix now.
3. **N1 edge the spec left silent — a case key that `contract.prefix_value` refuses** (whitespace inside, a leading colon) is still offered
   by `window_record.probe_gap_cases` (:655-683); `seam_chosen`'s `pass_block` is then refused, the question is HELD (E1.4) and `go on` can
   never open it (FR-2/FR-57: a door named that does not open). Filter in `probe_gap_cases`: keep a case only when
   `C.prefix_value(f"{C.PROBE_GAP_MATCH_PREFIX} {case}", C.PROBE_GAP_MATCH_PREFIX) == case` (that case keeps today's door). Low likelihood
   (case ids are tokens), cheap; fix now.
4. **N1 lead wording, minor:** `probe_gap_lead` says "{n} test case(s) ran green"; a listed case may also hold a RED instance (red ones are not
   word-owed, so they do not stop the listing, and the word passes no red — FR-18 holds). The sentence is about the listed tests; the
   owner-confirmed text stays as is. Note only.
5. **N2 — the lock reads only the LAST attempt** (`_account_steps_gate`, `manual_capture.py:3120-3122`): a ui login refused after submit
   (a1, locked) followed by a seed `http --as` that writes a `login_unknown` row (a2) unlocks `fill-account` for the refused account. Within
   the spec's stated error direction (E2.3 "may err toward NOT locking") and pre-existing in kind (any later non-env_blocked attempt did the
   same before N2), so **queue**: `_account_steps_gate reads only known[-1]; a later login_unknown attempt hides a refused one | узел: <next
   batch of the manual-lane pile>`; suggested fix: pick the newest env_blocked attempt whose cause is not `login_unknown`.
6. **`agents/qa-runner.md:51` "`unprepared` writes it."** (integration item 7 / fix round item 3; spec F26 + fix 11 said the charter is NOT
   changed: the prompt line is THE direction). In context it is weak: it sits in `<!-- kind: craft -->` "Techniques" (line 39), replaces a
   craft direction ("walk it like any other") with a command pointer (brief item 11: process text in a craft section), "it" has no
   referent, and nothing in the charter or `references/manual-evidence.md` names `unprepared` as a `manual_evidence.py` command (grep:
   only line 51; positive control — line 60 names `build`/`rejudge`). It is legible only with the prompt line (`story_run.py`
   `run_manual_block`), which does carry the full command. Recommendation for the Lead: revert to "walk it like any other." (same 23 bytes,
   spec as decided). Lead's call; non-blocking.
7. **`references/build-identity-methods.json:122`** — the untouched `blocked_device` row lost its space after the colon (`"blocked_device":"`):
   noise in a data row; restore. Trivial.
8. **`manual_capture.choose_attempt` (:329-345)** reads `_env_blocked_row(root / explicit)` three times and `attempt_state` three times in
   consecutive branches; read once. Quality, trivial.
9. **N3 edge, note:** when the request marker has no `source_revision` and the controller state has none, `write_block`'s new refusal
   (`manual_evidence.py` write_block absent-key check) tells the runner to use `unprepared` — the command that just failed (a circular door).
   F24 says live requests carry it; queue only if it recurs.

## Verdict-layer questions

**Q1 — doors on the live evidence.**
- N1: at the live seam (`window_round_gate` same_set, notebook :127-129) the refused dispatch is the critic's (`refusal_dispatch`), whose record
  `work/windows/<critic>.json` the driver rebuilds at finish (`story_run.py:2924`); `probe_gap_cases` lists LOCAL-1_TC_001/_002 when every
  green word-owed instance has `proof_level.probe_could_not_run`; the state key travels `no_move -> fallback_person -> _person_of ->
  ask -> asked` (traced :5104, :5182, :3766); `go on` -> `seam_chosen` -> `pass_block("S5", "probe gap: <case>")` per case -> the record
  `contract.probe_gap_words` reads (one-token `prefix_value`); test `test_recorded_case_word_is_read_by_probe_gap_words`. The lead's
  "could not run" is true by data (E1.3 filter). Holds.
- N2: the negative holds. The ONLY producer of an owner-`user`, no-cause, `do_not_retry` row is `_login_blocked(..., "user")` at
  `manual_capture.py:2912` (grep of every `EnvBlocked(`/`_login_blocked(` site), and it appends `attempt.step("ui", login_step, "failed")`
  (:2914-2916) with no step after it — so "last row is a failed `ui` step" is exactly a sent-and-refused login. The before-submit row
  (:2894) is owner `factory` and never locked. TC_014 a1 (no steps) opens. See finding 5 for the residual.
- N3: `write_unprepared` -> `write_block(declared=True)` -> `finalize_task` (:535-566 keeps the marker whole; the unprepared branch of
  `validate_manual_current` returns only `UNPREPARED`, so `attempt_id` on a walked record adds no issue and no `result`) -> `ledger`
  (:1281 copies `unprepared_rows` whole) -> `check_delivery.unprepared_records`. `walked` = attempts not env_blocked with ≥ 1 parseable step.
  Holds.
- N4: `halt` = 16-hex of the digest shown (`exit_limit_facts`), compared in `_exit_go_on` (`story_run.py:11431`) against the saved
  result's digest by equality; set -> `pending_words`, which `_act_wait_existing_job` reads before the saved result (F34); a new halt
  after the resume goes through `resume_role`'s halt road (asked). A digest that differs (fresh run result not yet saved, form-only halt)
  falls to today's path — one extra question, never a lost halt (E4.1/E4.3). Holds.

**Q2 — class completeness (rule 9; SIBLING_MAP axes 5, 16, 18, 32 walked).**
- `repair_limit_gate` re-asking a shown halt (N4 analog): at `_finish_saved_result` (:15188) the halt check runs BEFORE `repair_limit_gate`,
  so this site cannot show a halt then ask it; other callers not traced -> **queue** with a pointer (spec non-goal "other exit_limit
  callers"): `repair_limit/s7.repair_limit may show a halt the halt road re-asks (N4 analog) | узел: <next doors batch>`.
- `remedy_no_revision` / `remedy_no_probe_door` owner `user` (`manual_capture.py:1286`, `:1314`): the LOCK is right (the build is unknown —
  FR-59: no capture on an unknown); only the owner word is wrong by FR-46 (config is the project's/factory's). Not a stall -> **queue**
  as a finding in the manual-lane pile.
- Seam floor without `probe_gap_cases` (N1 analog): **no fix needed** — `last_resort` passes the state whole to `_person_of`
  (`story_run.py:5239`), so the floor's `go on` (TOKEN_MOVES) carries the cases too; `site_fallback` is not set on this state; the conductor
  road (:5493) also passes `dict(state, ...)` but this seam is `call: False`. The analog in the N1 report is false.
- Door-text siblings: every copy now says `<case key>` (integration grep table + fix round; my grep of the diff: 67 `probe gap` lines, no
  `<IID>`/`<instance id>` left in the changed carriers). `design/controller-blocks.md` regenerated, no change.

**Q3 — AR-29 / FR-12.** No new check reads wording: `halt_key` is a hash equality; `_row_locks_screen_route` reads fields `owner`, `cause`,
`do_not_retry`, `outcome`, `command`; `probe_gap_cases` joins ids; `write_unprepared` counts rows on disk and refuses on data, never on the
runner's words. Census raise `blocking_per_role.qa-runner` 131 -> 132 for `manual_evidence.py::write_unprepared` (class xref, owner data):
**reason sound** (a new writer with refusal sites; a ratchet raise for a new unit is the named form, axis 18), **role right** (the runner
calls it from its prompt line; precedent `coverage_contract._validate_unprepared` roles `qa-runner`, census :216). Inconsistency to queue:
the sibling rows `build_record`/`rejudge_record`/`main` (:536-538) say `conductor` though the runner calls them too — a census accuracy
finding, not this diff's. `probe_gap_cases` has no census row because the scanner does not see it as a unit (N1 report) — acceptable.

**Q4 — integration decisions.** Surface pin: one string, equal to `manual-capture-steps.json` `not_known_door` (diff compared). Re-pins
compared string by string: `test_probe_gap_word.py` K2 :162/:171, K3 :197, K13 :589 equal `PROBE_GAP_RECORD` (`person_words.door` appends
`--words-file <file>` unchanged) with `<T>` replaced by the ticket where the controller prints it; `test_conductor_doors.py` c27 wanted ==
substring of `conductor-actions.json` `go_on_as_is.run`, and its negative control still bites; K15 `PINNED_ELSEWHERE` names the new id;
`test_decision_classes.py` :214/:521 equal `block-names.json:21`. The nine cuts of `manual-evidence.md`: no RULE lost — "a pass without
`--state-url` is refused" is still stated by the quoted refusal line above it; weakened wording: "of any kind" dropped from "make no further
capture in this block" (the refusal rows in `build-identity-methods.json` still say it) and "it passes every rule" (:~93) where "it" could
read as `record.json` — acceptable. Line 51: finding 6.

**Q5 — B-20.** Nothing in this diff touches the S6 acceptance chain: grep of the diff for `stage acceptance|consumer_need_record|code_close|
s6_reentry|manual_close` finds only two context lines of `test_conductor_doors.py` (positive control: `probe gap` matches 67 lines). It makes
B-20 LESS likely to be reached by a person's words (N3: the unprepared cases land in a lane, so no S6 `exit_limit` `go on`; N4: no
re-asked halt) and no worse (N4 adds one runner session before S6 closes; acceptance unchanged). Needs its own node (not this batch):
«closing a stage that has a consumer after the person's `stage acceptance` word, from any driver site, and the analyst's S6 acceptance record
when its form is not complete; `code_close` with a door» — owner the Lead, files `story_run.py` (`where`, the S6 close sites), `controller.py`
`code_only`; FR-2, FR-40, FR-57.

## Standing questions
- Fit to the spec: yes, all items N1–N4 as written; deviations named by the builders (no N1 census row; N3 census row) settled by the Lead.
- Builder decisions: safe direction (choose_attempt's new old-row branch still refuses the named attempt; only wording).
- Seams: `story_run.py` functions disjoint (N1/N3/N4), `manual_evidence.py` disjoint (N2/N3); nothing reordered.
- DUPLICATION AND CONSISTENCY: findings 1, 2 (grep `def .*jsonl|def _lines|def _rows_of` over `scripts/*.py`; grep "case keys this window
  needs").
- CODE QUALITY: B1, findings 7, 8; new functions under 60 lines (`write_unprepared` 1432-1474, `probe_gap_cases` 655-685).
- Hygiene: `selftest --lang` green (reports); size cap green after the fix round (`--limits` witness); finding 7.
- In-tree ratchets: census `qa-runner` 131 -> 132 (named, sound); `role-load.json` process 16701 -> 16699 owed (B2).
- ARCHITECTURE: AR-9, AR-13, AR-14, AR-16, AR-22, AR-24, AR-25, AR-29 touched and named by the spec/commits; AR-13 dented by findings 1-2.
- JUDGMENT: none moved into code (Q3); finding 6 is process text in a craft section.

## Trail
Read: spec t-1955 (whole); brief; six reports; notebook :127-169; the diff (all 38 files); `story_run.py` 2439-2450, 2525-2606, 2905-2935,
5104-5245, 5524-5530, 5945-6040, 11169-11320, 11401-11440, 15188-15205; `window_record.py` imports, 94-104, 650-685; `acceptance.py`
874-899; `contract.py` 112-128; `manual_capture.py` 1095-1110, 1150-1158, 2440-2466, 2880-2916, all `EnvBlocked(`/`do_not_retry` sites;
`manual_evidence.py` 1182-1200, 1262-1335, 1336-1352, 1376-1475; `coverage_contract.py` 300-320, 685-740; `finalize_task.py` 530-566;
`ledger.py:1281`; `person_words.door`; census rows :216, :490-544; `role-load.json`; `qa-runner.md` 39-60; `SIBLING_MAP.md` axes list, 5, 16.
Reruns: below. CI: `ci_read.py jobs 8042123` (forge-check failed, package-fast failed, install-smoke failed, package-full 1/2 2/2 running
at read time) and the three failed logs. Deviation: one recon command was prefixed with `cd` (Bash, cwd resets; hook WARN only, nothing
changed). Needed beyond the manifest: `coverage_contract.py`, `finalize_task.py`, `ledger.py`, `person_words.py`, `references/role-load.json`.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1 forge-check red: manual_evidence.py:1442 unused variable 'request' (lint ratchet, pyflakes UnusedVariable) - call _load_request bare",
    "B2 package-fast and install-smoke red: A22 process ratchet - references/role-load.json:32 process_ratchet_tokens.qa-runner 16701 -> 16699 (a lower; recheck the total row :18)"
  ],
  "fixes": [
    "B1 manual_evidence.py:1442 drop the unused assignment",
    "B2 references/role-load.json:32 qa-runner 16701 -> 16699",
    "F1 one tolerant steps.jsonl reader in manual_capture used by _last_step_row (manual_capture.py:3071) and _recorded_walks (manual_evidence.py:1398)",
    "F2 one helper for the 'case keys this window needs' suffix next to PROBE_GAP_RECORD; used by controller.py:6392 and :6574",
    "F3 probe_gap_cases (window_record.py:655) keeps only case keys contract.prefix_value accepts as one token",
    "F6 qa-runner.md:51 - Lead's call: revert to 'walk it like any other.' (spec F26) or reword with a referent",
    "F7 build-identity-methods.json:122 restore the space after the blocked_device key",
    "F8 choose_attempt (manual_capture.py:329-345) read the env_blocked row and the attempt state once",
    "queue: _account_steps_gate reads only known[-1], a later login_unknown attempt hides a refused one (finding 5)",
    "queue: repair_limit / s7.repair_limit may re-ask a shown halt (N4 analog); remedy_no_revision / remedy_no_probe_door owner word (FR-46); census roles of build_record/rejudge_record/main",
    "B-20 needs its own node: stage-with-consumer close after the person's stage acceptance word from any driver site, code_close with a door"
  ],
  "class_completeness": "N1 door-text copies all say <case key> (integration grep + fix round); seam floor analog is moot (last_resort passes state whole to _person_of, story_run.py:5239). N2 do_not_retry producers enumerated: only _login_blocked(user) at manual_capture.py:2912 makes a no-cause user row and it always ends with a failed ui step; remedy_no_revision/remedy_no_probe_door lock correctly, owner word queued. N4 repair_limit analog queued with pointer. Axes 5, 16 (new JSONL twins: finding 1), 18 (census raise named, role-load lower owed), 32 (no judgment moved) walked.",
  "trail": {
    "read": [
      "docs/tasks/specs/t-1955-manual-lane-doors.md",
      "docs/tasks/critic-diff-brief.md",
      "docs/tasks/specs/reports/t-1961-n1-report.md, t-1962, t-1963, t-1964, t-1966, t-1969",
      "experiments/mybooks/thinking-roles/thinking-roles.md:127-169",
      "wt-fbfix diff d85a91e0a..2447ec263 (38 files)",
      "wt-fbfix scripts: story_run.py, window_record.py, controller.py, manual_capture.py, manual_evidence.py, coverage_contract.py, finalize_task.py, ledger.py, acceptance.py, contract.py, person_words.py (ranges in the Trail section)",
      "wt-fbfix references/role-load.json, judgment-census.json, agents/qa-runner.md",
      "docs/SIBLING_MAP.md axes 5, 16, 18, 32"
    ],
    "reruns": [
      {"command": "python -m pytest D:/ws2/wt-fbfix/ai-packages/qa-factory/scripts/tests/test_probe_gap_door.py -q -p no:cacheprovider", "result": "32 passed in 24.39s"},
      {"command": "python -B D:/ws2/wt-fbfix/ai-packages/qa-factory/scripts/tests/test_manual_capture_login_unknown.py", "result": "14 ok lines, no FAIL"},
      {"command": "python -B tools/ci_read.py jobs 8042123 (+ log 28211416, 28211417, 28211421)", "result": "forge-check failed (lint: manual_evidence.py:1442 unused request); package-fast failed (A22 qa-runner 16699 below row 16701); install-smoke failed (same A22); package-full running"}
    ]
  }
}
```
