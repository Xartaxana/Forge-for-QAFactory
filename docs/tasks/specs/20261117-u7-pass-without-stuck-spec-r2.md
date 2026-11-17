# Spec U7 "pass without getting stuck" - r2 (fix round t-1249 of t-1240) - DRAFT for Lead acceptance

Fresh-worker fix round. Input: r1 `docs/tasks/specs/20261117-u7-pass-without-stuck-spec.md` (not edited), the plan critic's
verdict `docs/tasks/specs/reviews/t-1242-u7-pass-without-stuck-plan.md`, the brief `20261117-u7-pass-without-stuck-brief.md`,
and the Lead's decisions on the verdict (17.11.2026, carried below, not re-decided). This file is WHOLE: it replaces r1.
Every load-bearing code fact was re-read on 17.11.2026 at the cited `path::symbol` (trail, section 13). Paths are from
`ai-packages/qa-factory/` unless they start with `docs/`, `plans/` or `tools/`.

Goal (owner, 17.11.2026, verbatim in the brief): the factory, knowing nothing of a project's form, passes every stage without
getting stuck and lets the agent do its work; "role first": the person gets only the remainder (a device, credentials). A
stage may cost a little more if quality is bought; blocking is never acceptable.

**Lead decisions carried (17.11.2026).** B1-B6, M1-M8 accepted. B1: r4 is a block (class B); F-4(b) is the MAIN path, its own
node. B2: S5's code close writes the empty manifest through `manifest_put.py`; S6-S8 of an all-manual story are walked; the
B-006 items that still block enter U7 as nodes. B3: per site the usable rows are listed; no paid conductor call with no row
for the state. B4: test rows in keep files only. B5: the three missing-executor roads change together in stream 5a. B6: the
F-2(a) state exits like `s5_reporter`. M4: E-7 is a node NOT dispatched before the owner's F-5. M5: F-3 premise measured here.
Q12: said out loud in U7 (class A); the one-road fix is a U8 node. Forks F-1, F-2, F-3, F-6, F-7, F-8, F-9, F-10 as decided in
r1's header; F-4 = (b) main path; F-5 open (the owner's).

**What this round found that the Lead must see (new forks, section 11):** F-4(b)'s carrier "the manual-evidence road" refuses
an automate obligation today (`manual_evidence.py` 1029-1033) -> F-13. A manual `inconclusive` or `unprepared` result with no
failure makes the run report `not_executed` (`finalize_task.py` 629-637), which S7 refuses after a real S6 run
(`driver_stage_s7.py::failures_to_triage` 13-20): this blocks an all-manual story, F-3's agent attempt and F-4(b) alike -> F-12,
stream 7. r9 has no usable row -> its conductor turn is cut by B3 (F-11 only for an optional new row).

**Lead acceptance of r2 (Architect session, 17.11.2026; t-1249).** Accepted as the spec of U7; r1 is superseded. Spot-checks
by reading the carrier: `scripts/manual_evidence.py` 1029-1033 (an obligation whose `decision` is not `manual-agent` is
refused - F-13's premise holds); `scripts/finalize_task.py` 629-637 (`not_executed` unless a failure or all passed - F-12's
premise holds). New forks, decided by the Architect ("решила сама", the owner may reverse any of them):
- F-11 = (a): no new conductor row; a missing `test_repo` is the person's remainder.
- F-12 = (a): `failures_to_triage` triages manual targets whatever the status (stream 7); `execution_status` is NOT rewritten.
- F-13 = (a): `manual_evidence.py log-verdict`, admitted only under the three conditions of section 2 r4 (node 4b).
- F-14 = (b): the `unknown` reason joins only an existing card or note of the same profile.
- Q-U8: accepted as a node of U8 (`gate_preflight.py::collect_base` -> `launch_check.runner_row`, one road).
- F-5 stays OPEN, the owner's; node E7 and the onboarding question wait for it, no other stream does.
F-12, F-13 and the S5 code close that writes the empty manifest (5b) change the MEANING of a gate or a record: they go to a
second plan-critic pass (fix diff + verdict t-1242) BEFORE any builder dispatch of streams 4b, 5b, 7 (PROJECT.md, package
change p. 6). Streams whose text the re-review does not touch (1 items 1-3, 2, 3, 4a, 5a, 6) wait for the same verdict: one
pass per topic.

---------------------------------------------------------------------------------------------------------------------

## 0. Finding -> where fixed

| finding | what r2 does | where |
|---|---|---|
| B1 r4 premise | Re-read: S7 refuses `not_executed` without an S6 code-only receipt (`driver_stage_s7.py` 13-20); a no-report run is `not_executed` (`run_suite.py::no_report_words` 359-368, which ALREADY says the default out loud: class A is closed by today's text). r4 re-classed B. F-4(b) is node 4b; its carrier is F-13; the measurement stays only as a witness row | §2 r4, §6 stream 4b, §11 F-13 |
| B2 r11 starves the manifest | S5's close writes `{"tests": [], "unresolved": []}` through `manifest_put.py` (writer can produce it: §2 r11 "writer check"); all-manual walk S5->S8 written; B-006 items in/out listed; axis 5 row and pin `test_controller_state.py:1145` named | §2 r11, §3, §6 stream 5b, stream 7 |
| B3 moves that do not exist | Per site the existing rows: r8 `install_dependencies` action; r10 `stand_prepare` move; r9 none -> conductor turn cut. Paid call only when the row's precondition holds; AR-12 restated per site | §1.1 AR-12, §2 r8/r9/r10 |
| B4 quarantined test homes | `test_surfaces.py`, `test_story_run_gate_repair.py`, `test_mobile_road.py`, `test_planning_contract_not_planned.py`, `test_stage_done.py`, `test_run_suite_*.py` are quarantine (test-layers.json `quarantine` from line 7209); every row now lands in a keep file (§2 per site) | §2, §6 |
| B5 three roads | `check_s5_executor`, `check_s5_toolchain` `not_started`, `run_suite.refuse_missing_executor` (+ its `references/halts.md` row) all in stream 5a on one road | §2 r8, §6 stream 5a |
| B6 fixable exit | `s5_executor` fixable finding exits like `s5_reporter`: one conductor turn, a driver-written bound record, the next rehearsal gives the card | §2 r8 "transition", §6 stream 5a |
| M1 seam entry | r10: `Driver.no_move(state)` with `site_fallback`, `call` NOT False, kind not in `NM.EXCLUDED_KINDS` (`no_move.py:37` = `("s1_review",)`); r9 test file `test_no_move_seam_sites.py` | §2 r9, r10 |
| M2 census owner | owner `data` for check_s5_executor, stand_check (census rows 415, 1118, read by the critic) and s0_rest; units with no census row named; none added | §1.2 |
| M3 overlap | r3 moved into stream 1 (one owner of `test_readiness.py`); OF5-5 owns cell correction is a precondition of stream 6 | §6 |
| M4 E-7 owner | node E7 owns `agents/qa-runner.md`; current text has no preparation rule (grep, §13); not dispatched before F-5 | §2 E-7, §6 node E7 |
| M5 F-3 premise | measured by reading: `manual_evidence.py::build` refuses an attempt with no captures (1851-1853); capture surfaces are `ui`, `http`, `app` only (`manual-capture-steps.json:46-50`); a case with none is recorded `unprepared` (`--not-walked`, observations), a triage target (`contract.py:4662`), no result. F-3(a) holds in that weaker form and needs stream 7. Reverses EP1-41f N-17; basis P19 step 3 | §2 a2D1, §11 F-3 |
| M6 r3 clause | clause "asked about before tests run" dropped; the note says only what readiness did | §2 r3 |
| M7 r1 keys | K3, K4 replaced by keys new to the edit | §6 stream 2 |
| M8 axis 38, ratchets | named per stream: `dry_exits.py --check`, `NO_MOVE_BASELINE` (`audit_factory.py:1667`), `driver-layers.json`, `judgment-census.json` | §6 DoD lines |
| Q13(d) readers | each line of the critic's tool run answered | §8 |
| Q12 one road | class A note at the silent return (`gate_preflight.py:2941-2944`); U8 node named: `launch_check.runner_row` as the one road for the collect command (`gate_preflight.py::collect_base`) | §2 Q12, §6 stream 5a item 6, §11 |

---------------------------------------------------------------------------------------------------------------------

## 1. Architecture, owners, variety walk

### 1.1 AR-n touched, with the change check each demands (copied into every stream's DoD)

| AR | how the spec touches it | change check (DoD) |
|---|---|---|
| AR-2 | every changed site ends in a role move, a declared default said out loud, or the person's remainder named | per changed site, one row whose input is an unknown axis value and whose outcome is "a role move is offered / the default is said", never silence |
| AR-1 | `surfaces.json` words (stream 1); no list of platform, language or tool names enters code | the diff adds no tuple/set literal of surface/language/tool words to a `.py` file (reviewed; the existing `LANGUAGE_WORDS` row of the readiness table covers the words) |
| AR-9 | every new or reworded refusal/note names what it expected and a door its receiver can use | a row per new text asserting its door token is one the receiver executes (FR-2) |
| AR-13 / AR-14 | new readers go through existing one readers; the empty manifest is written by its one writer `manifest_put.py`; the executor-turn record has one writer (driver) and one reader (gate_preflight) | no second reader of `surfaces.json`, the readiness record, the manifest or the turn record (critic Q6) |
| AR-17 | r8 and r10 go seam-first where a row exists; r9 stays person (no row) | r8/r10 rows: the conductor is called once before the person's card/question; with the row's precondition false, NO conductor call (counter 0) |
| AR-22 | S5's required output exists after a code close | a row: derived-empty S5 leaves `work/automation-manifest.json` with empty `tests`/`unresolved` |
| AR-23 | NE25's empty S5 outcome becomes true in code | `test_null_outcomes.py` green; the S5 row of the stream |
| AR-25 | every new state has a way out: the s5_executor fixable finding (-> card), the S5 code close (-> S6), S7 with manual targets and `not_executed` (-> triage) | a row per new state with its exit |
| AR-28 / FR-59 | unknown never a pass: an underived scope never closes S5; an unreadable turn record reads as "turn had" (card, no second paid call); a run with no report is never `passed` by code | a row per site with the unknown input and outcome "not closed / not ok / asked" |
| AR-12 | restated truthfully (B3): r2 adds a line for projects with NO capability word (legacy configs included, F-1(a)); r3 a longer note only for URL-less undeclared rows; r8 adds one conductor session before the card ONLY when the dependency check holds an install command for that profile; r10 adds one conductor session ONLY when `Stand remedy:` is authorized and the stand has a `bring_up`; Q12 adds one gate note for a non-pytest collect command. Web/API projects outside those conditions: byte-identical | existing pins kept green (`test_readiness.py:873-874, 917`; the web rows of `test_gate_preflight.py`); a row per added call asserting the call count is 0 when its precondition is false |
| AR-19 | S5 close is the twin of `s6.nothing` (`driver_stage_s6.py` 502-513); S6 side unchanged | named in the stream's commit |
| AR-29 | checks altered: §1.2 | census rows unchanged (no class change); ratchets only shrink |

AR-24, AR-26, AR-27: not met (no person words, requirements or findings change road).

### 1.2 Checks added or altered: owner and census class (AR-29, P27; M2)

| check (unit) | change | owner | census |
|---|---|---|---|
| `surfaces.py::declared_surfaces` | `hands` "person" -> "role"; `undeclared` entry | data | no census row; none added |
| `planning_contract.py::_row_of_nobody` | a `hands: none` row converts to manual-agent | data | no census row; none added |
| `readiness.py::_check_plain_environment` | URL-less undeclared row: the note says the default | data | no census row; none added |
| `driver_s0.py::Driver.s0_rest` | no code change (r9 cut); one pin row | data | no census row |
| `gate_preflight.py::Rehearsal.check_s5_executor` | missing launcher with an install command and no turn yet -> `factory_fixable`; else the card | data (routing a state to the conductor keeps owner `data`; the judgment is the conductor's, outside the unit) | row 415 `owner: data`, class `shape`: unchanged |
| `gate_preflight.py::Rehearsal.check_s5_toolchain` | `not_started` on the same road; silent returns said | data | no change of row (none read) |
| `driver_stage_s5.py::stage_S5` | derived-empty scope -> empty manifest + code close | data | no census row; none added |
| `controller.py` op `code_only` | S5 allowed only over its own derived-empty `stage_scope("S5")` | data | none added |
| `driver_stage_build.py::DriverStageBuild.stand_check` | conductor turn when `stand_prepare` is open | data | row 1118 `owner: data`, `shape`: unchanged |
| `driver_stage_s7.py::failures_to_triage` | `not_executed` with manual triage targets is triaged (F-12 rec.) | data | none added |
| `probe_by_code.py::_no_entry` | text order only | data | none added |

If `test_judgment_census.py` names a changed unit as needing a row, the stream stops and returns a question (no row is
invented). Commit lines: `architecture:` and `judgment:` in the form `tools/architecture_gate.py` checks (the one carrier of
the grammar; not copied here); `judgment: none` always carries ` -- <why>`.

### 1.3 Variety walk (architecture.md section A, "How the map is walked")

- axis 1: held by role -- unknown language at `probe_by_code`: red-sandbox road named first (r5); a collect command that is not pytest is SAID (Q12), the one-road row is U8's
- axis 2: held by table|role -- `references/surfaces.json`; unknown word -> agent role first (`hands: role`), person only the remainder (a2D1, s6.unknownword); no word at all -> `undeclared` said (r2)
- axis 3: held by key|role -- `run.reporter`; `none` is said by `run_suite.py::no_report_words`; the result is the runner role's log judgment (4b, F-13)
- axis 4: held by role -- an all-manual plan closes S5 by code with an empty manifest and reaches S7 triage (r11, stream 7)
- axis 7: held by key|role -- `environments[]`; URL-less row: default said (r3); unconfirmed stand: `stand_prepare` first when authorized (r10); a second instance: E-7 (waits on F-5)
- axis 13: held by role -- a missing S0 capability is the person's remainder (no conductor row: r9, F-11)
- axes 5, 6, 8, 9, 10, 11, 12: n/a -- no site of this spec reads the tracker, delivery target, host, people/process, language, task size or check kinds

No `narrows` line. A builder finding that a change narrows a project form returns it as a question.

---------------------------------------------------------------------------------------------------------------------

## 2. Sites: current behaviour read in code, target, edges, invariant, error direction, test

Test layers are `docs/TESTING.md`'s. Every new case is a ROW of an existing table in a KEEP file of
`scripts/tests/test-layers.json` (keep block lines 36-7155; quarantine from 7209). A builder that finds its named file
quarantined stops and returns a question.

### Class A - silent defaults

**r1 - `skills/qa-onboarding/phases/p1-discovery.md` row "Mobile surface" (line 43) + `phases/p2-interview.md` (line 218)**
As r1 §2 r1 (current, target, edges, invariant, error direction unchanged), with two corrections: (i) the onboarding question
that would RECORD whether starting a second local instance is authorized is NOT part of this site (it waits on F-5, node E7);
(ii) witness keys K3/K4 replaced (stream 2). Test: doc-dispatch witness (CLAUDE.md rule 11), no code.

**r2 - `scripts/surfaces.py::declared_surfaces` (112-114)**
As r1 §2 r2. Lead decision F-1 = (a): `profiles` absent counts as undeclared. This changes the promise of
`readiness.py` 1314-1315 ("Configs written before this contract retain the exact legacy readiness shape") for ONE key: a
legacy config with no profiles now gets `surfaces.undeclared`; the `profiles`/`implementation_repos`/`profile_contract` keys
stay absent as before. The comment at 1314-1315 is amended in the same commit to say so (FR-37).
- Test (B4): data-seam rows in `scripts/tests/test_readiness.py` (keep, detector; its `covers` holds `surfaces.py`): "no
  capability word, no surface -> record carries `surfaces.undeclared` with the table's words"; "`profiles` absent ->
  `surfaces.undeclared`"; "web+api -> no `surfaces` key, table read 0 times"; "table unreadable with no words -> `surfaces.unknown`".
  `test_surfaces.py` is quarantine: NOT edited (its rows 268-310 and 444-489 will contradict the new behaviour; the stream's
  report lists them for `tools/test_quarantine.py`'s owner; the canon does not run them).

**r3 - `scripts/readiness.py::_check_plain_environment` (874-883)** - moved to stream 1 (M3)
- Now (read): a row with no `base_url`/`url`/`health_url` joins `in_process` whatever it declares; all rows so and no env key
  declared -> `OK` "in-process environment(s), nothing to probe".
- Target: split declared in-process (`kind` in the three words, or `probe: none`) from URL-less. All declared -> today's note
  byte for byte. Any URL-less row -> `OK` stays (F-6 = (a)); the note adds: "stand `<name>` names no address and does not say
  it runs in-process: it was taken as in-process and nothing was probed here". M6: the r1 clause "the stand is asked about
  before tests run" is DROPPED - readiness cannot know what S0's `env_probe.py --env` will answer (a row with an address in an
  env file is probed there: `env_probe.py` 62-74).
- Edges: `stands` empty -> next branch (unchanged); `kind: in-process` with an address -> declared (unchanged); records
  written before -> same status, a longer note only for a URL-less undeclared row.
- Invariant: no row naming an address is ever "nothing to probe"; a declared in-process record is byte-identical.
- Error direction: toward saying more, never a stronger status.
- Test: rows in `scripts/tests/test_readiness.py` beside the pins 873-874 and 917 (kept): "declared in-process -> note
  unchanged", "URL-less undeclared -> OK + the default sentence", "mixed -> the sentence names only the URL-less row".

**r4 -> re-classed B (B1).** See class B, r4/F-4(b).

**Q12 (critic) - `gate_preflight.py::Rehearsal.check_s5_toolchain` silent returns (2938-2944)** - class A, stream 5a
- Now (read): `tests_root` not a directory -> `return` (2938-2939); `collect_base` empty (a non-pytest command) -> `return`
  with the comment "A project on another runner is not told" (2941-2944).
- Target: each return first writes ONE `self.note(check, ...)`: "the existing tests were not collected before S5: <the
  project's tests folder `<tests_root>` is not a folder here | the project's test command is not one this check knows how to
  collect>; S5 meets the toolchain first". No finding, no question (FR-4: informs).
- Sweep of the same function (rule 9): the timeout card (2978-2984) stays a `PERSON_DECIDES` card - no conductor row settles a
  slow collect (B3), and its answer is the person's risk word; `unavailable` branch unchanged.
- The one-road fix (U8 node, opened by the Lead): `gate_preflight.py::collect_base` keys on `PYTEST_TOKENS`; the collect
  command of any runner should come from `launch_check.runner_row` (already data). File `scripts/gate_preflight.py`, function
  `collect_base`; named in §11 Q-U8.
- Test: rows in `scripts/tests/test_gate_preflight.py` (keep, gate_named): "non-pytest command -> one note, no finding";
  "tests_root missing -> one note, no finding".

### Class B - doors to a person past the role

One road (P31, AR-17): the conductor seam `Driver.no_move(state)` (`driver_conductor.py:617`), entered with `site_fallback`
(the site's own question) and `call` not False; the conductor acts only through `references/conductor-actions.json`. No
site gets a paid call when no row of that file can settle its state (B3).

**a2D1 + s6.unknownword - `scripts/surfaces.py` (`_who` 87-88; literals 128, 137, 140); `references/surfaces.json`; sibling `planning_contract.py::_row_of_nobody` (2277-2297) and caller (2334-2346)**
- Now, target, edges: as r1 §2 a2D1 (hands "person" -> "role"; words role-first; `_row_of_nobody` converts).
- M5 premise, measured by reading: an undriven surface has no capture surface (`references/manual-capture-steps.json:46-50`:
  `ui`, `http`, `app`); `manual_evidence.py::build` refuses an attempt with no captures (1851-1853: "Capture first:
  `manual_capture.py ui ...` or `manual_capture.py http ...`"). The agent's attempt is therefore recorded with
  `manual_evidence.py unprepared --not-walked <why> --observations-file <what it tried>` (args 2152-2157): no result, and
  `contract.triage_targets` counts it a target (`contract.py:4659-4662`). So F-3(a) holds in this form: the analyst at S7
  judges it; the person gets the remainder through S7's own road. Without stream 7 the story would stop at S7 entry (the
  report is `not_executed`: `finalize_task.py:629-637`). Item 4 of stream 1 is therefore dispatched only after stream 7 merges.
- This reverses EP1-41f N-17 (`_manual_agent_pass` docstring at `test_surfaces.py:445`: "leaves the obligations of a `hands:
  none` row as planned"); basis: P19 step 3 (`docs/OWNER_PRINCIPLES.md:58-61`: "the agent checks by hand and shows the
  person before/after").
- Invariant: an unknown surface word never becomes "supported"; the agent's attempt never produces `passed` without the
  evidence the manual gates accept (an `unprepared` row has no result).
- Error direction (reused `_row_of_nobody` in a more consequential role, keep -> convert): toward converting (one agent turn
  ending `unprepared`), never toward dropping a row. Adversarial inputs that stay safe: a profile id the config lacks; a broken
  table (a line, the old road); words of rows with different `hands` (`row_for_profile` -> None, the old road); an empty
  obligation list.
- Test (B4): rows in `scripts/tests/test_question_branches.py` (keep; already holds the `_manual_agent_pass` rows at
  2386-2524): "`hands: none` profile -> converted to manual-agent with the role-first line"; "unknown profile / broken table /
  web profile -> the old road". Surfaces rows: `test_readiness.py` data seam "the record's `surfaces` entries carry `hands:
  role` and the role-first words for cli/desktop/unknown word/no stand".

**r4 / F-4(b) - a run with `reporter: none` (B1)** - node 4b
- Now (read): `run_suite.py::no_report_words` (359-368) already says out loud "A run with no report is recorded as
  not_executed however green its log is"; the summary carries a `parse_gap`. S7: `driver_stage_s7.py::failures_to_triage`
  (13-20) accepts `not_executed` only after an S6 code-only receipt (`s7_pretriage.s6_closed_by_code`); after a real S6 run it
  raises `Refusal("S7 entry: ... nothing to triage yet; the S6 halt that produced it stands")`. Blocks.
- Target (Lead: F-4(b) main path): the runner role at S6 reads the run's log for each instance of a no-report run and gives
  its verdict per case (`pass | fail | inconclusive`, P27: the role judges, code records). Carrier: `manual_evidence.py`
  refuses an obligation whose decision is not `manual-agent` (1029-1033), so the stated road does not exist today -> fork
  F-13. By its recommendation (a): a new command `manual_evidence.py log-verdict --case <id> --run-block <path> --result
  <word> --actual <words> --log-quote N=<words>` admitted ONLY when (i) the case's obligation is `automate` and in the S6
  scope, (ii) the named run block exists for that case's instance, carries the no-report `parse_gap` and was run on the
  case's current bytes (its `execution_fingerprint` equals the current one), (iii) the profile's `run.reporter` is `none`.
  The record joins `current_manual_checks` with `judged_from: log` (the reducer already counts manual results:
  `finalize_task.py:622, 631`). The runner's instruction is one paragraph in `skills/qa-story/phases/s6.md`.
- Edges: no log in the block -> refused (door: run the case again with output kept); a run block of other bytes -> refused
  (invariant below); a profile WITH a reporter -> refused (its report is read by code); `reporter` key absent -> as today's
  default reader; records written before -> no log verdicts, S7 refuses as today (both worlds: the move that creates the new
  record is the runner's `log-verdict` call).
- Invariant: a log verdict measured on other bytes never counts; code never turns a log into `passed` (FR-58); an automate
  obligation with a reporter is never admitted.
- Error direction (manual_evidence's admission, a gate, widened): toward refusing (the case stays `not_executed`, S7 asks),
  never toward admitting a case whose run produced a report or whose block is stale. Adversarial inputs: a fabricated block
  path outside `work/evidence/`; a block of another case; a fingerprint mismatch; `--result passed` spelled as the reducer's
  word (refused: `RESULTS = ("pass", "fail", "inconclusive")`, `manual_evidence.py:35`).
- Test: rows in `scripts/tests/test_manual_evidence.py` (keep) for each admission condition; row in
  `scripts/tests/test_story_run_s7.py` (keep): "reporter none + log verdicts pass -> S7 entry accepts (`passed`)"; the
  `reporter: none` -> S7 measurement is attached to the report verbatim as a witness, not committed.

**r5 - `scripts/probe_by_code.py::_no_entry` (1455-1465)** - as r1 §2 r5 (text order only; after RD1-24; F-8 = (a)). Test row
in `scripts/tests/test_probe_by_code.py` (keep, test-layers.json:3690).

**r8 - missing launcher: three roads, one road (B3, B5, B6, F-2 = (a))** - stream 5a
- Now (read): road 1 `gate_preflight.py::Rehearsal.check_s5_executor` (2815-2875): launcher `missing` -> `PERSON_DECIDES`
  card `executor_question` (540-552) with three answers. Road 2 `check_s5_toolchain` `not_started` (2966-2977): the same card.
  Road 3 `run_suite.py::refuse_missing_executor` (1556-1578): prints `executor_unavailable` with the same question, exit 3;
  the driver has no `KNOWN_REFUSALS` row for it (`driver_dispatch.py:38` ff.), so it reaches the conductor through
  `handle_refusal` (map `test_silent_passes.py:879`), which reads `references/halts.md:28`.
- The usable row (B3): `install_dependencies` (`conductor-actions.json:34`): runs the `command` of the `s5_dependencies` note
  once, then requires `dependency_drift.py ... --json` to print `in_sync`; never an install command the note did not name.
  Its source: `check_s5_dependencies` (2877-2903) keeps `self._drift` (entries `differs`/`missing_only` with `command`,
  `profiles`). No other row settles a missing binary (a machine tool is the person's remainder).
- Target, one road for all three: a missing launcher of profile P gets ONE conductor turn exactly when an install command for
  P is known (a `_drift` entry whose `profiles` holds P and whose `command` is non-empty) and no turn was had for the key
  `(P, tool, command digest)`; otherwise the three-answer card as today, words unchanged.
  - Road 1 and 2 (gate): emit `factory_fixable` (check `s5_executor`, fields `profile`, `tool`, `cases`, `install_digest`,
    `fix` = the `install_dependencies` row's `says`) INSTEAD of the card while the condition holds; the card otherwise.
  - Road 3 (mid-S5): the JSON gains `"install": <the same command or null>` from the same helper; `references/halts.md:28`
    "Read first" adds: "when its `install` names a command, the `install_dependencies` action once, then `retry`" (first cell
    unchanged: map `test_silent_passes.py:879`; 18 rows and the marker unchanged: `test_conductor_investigates_first.py`).
  - One helper `gate_preflight.executor_install(root, profile_id) -> (command dict | None, digest)` reads
    `dependency_drift.check_profiles` (AR-13), imported by `run_suite.refuse_missing_executor` as it imports
    `executor_question` today (1565).
- Position (B6, invariant): in `gate_preflight.run` (6086-6094) `check_s5_dependencies` moves BEFORE `check_s5_executor`, so
  `_drift` is set before both readers (executor, toolchain); nothing else in the tuple moves. What must stay unreachable: an
  executor decision read over an unset `_drift` (the helper reads `getattr(self, "_drift", None)`; None -> no install known
  -> the card).
- Transition (B6, modelled on `s5_reporter`, `driver_gates.py` 30-33, 1039-1073): the driver hands the `s5_executor` findings
  to the conductor through `hand_to_conductor` (no code move: `gate_stop` reason `no_move`); in that method's `finally`,
  besides `close_reporter_bound(rest)`, a new `close_executor_bound(rest)` appends `{key, at}` to
  `<task root>/state/executor-turns.json` (ONE writer: this method; ONE reader: `gate_preflight.executor_turn_had`) whatever
  the conductor did. The series-stopped branch (930-934) re-hands unturned executors once, like `unadapted_reporters`. The next
  rehearsal (a) finds the launcher -> nothing; (b) finds it missing with the key recorded -> the card. `CHECK_WORDS` gains
  `"s5_executor": "launcher to install"`.
- Edges: no automate rows -> nothing (unchanged, 2841-2851); `skip_executor` -> off; a handed profile -> not asked; record
  absent -> no turn yet (both worlds: the first `close_executor_bound` creates it); record unreadable -> read as "turn had"
  (card, no second paid call: FR-59); record write fails -> printed, remembered in `self.state["executor_handed"]`, the finding
  goes to the top of the gate (as `adapt_handed`); a road with no driver -> `stage_done` refuses S4 over the fixable finding
  with its `[fix: ...]` and the existing person's-word door `--block "gate rehearsal"` (the same as `s5_reporter` today);
  the conductor's install fails -> `install_dependencies` row says "tell the person ... offer install it yourself / go on
  without / stop" and the next rehearsal gives the card.
- Invariant: nothing is installed but the command the project names (row text); `handed_to_person` is never chosen by code;
  one conductor call per key.
- Error direction: toward the card (a question too many), never toward assuming a launcher exists; never a second paid call.
- Test: rows in `scripts/tests/test_gate_preflight.py` (keep; its covers hold `driver_gates.py`, test-layers.json:1960):
  "missing + install known + no turn -> factory_fixable s5_executor"; "missing + no install -> card, words unchanged";
  "missing + turn recorded -> card"; "record unreadable -> card"; "toolchain not_started -> same decision"; "zero automate
  rows -> toolchain collect not run, no card" (§3 item iii); a driver-rig row "fixable s5_executor -> one conductor call, record
  written, next rehearsal card, conductor calls = 1". Road 3: row in `test_gate_preflight.py` calling
  `run_suite.refuse_missing_executor` "JSON carries `install`".

**r9 - `scripts/driver_s0.py::Driver.s0_rest` (2385-2422)** - cut by B3
- Now (read): a required capability `missing` -> `s0_stop` (727-739) raises the `s0.readiness` Person (retry / go on / stop).
  `missing` comes from: `check_vcs` "git is not on PATH" (698), `check_test_repo` "tests_root ... does not exist" (409-410),
  the ticket route (credentials), `check_config_schema`. No row of `conductor-actions.json` settles any of them
  (`readiness.py --write --probe-vcs` probes remote access, it does not put git on PATH).
- Target: no conductor turn (B3: no paid call with no row). The person's question stays: these are the person's remainder (a
  machine tool, credentials, a folder the config names, a config). A new row for `test_repo` is F-11 (recommended: no).
- Test: pin row in `scripts/tests/test_no_move_seam_sites.py` (keep; holds the `s0.ticket_auth` rows): "missing test_repo
  -> the s0.readiness question, conductor calls 0"; "exit 2 -> gate_refusal, no Person".

**r10 - `scripts/driver_stage_build.py::DriverStageBuild.stand_check` (139-206)** - stream 6, with OF5-5
- The usable row (B3): move `stand_prepare` (`conductor-actions.json:157-171`): runs the stand's `bring_up` from
  `config.environments[]`, then `stand_health.py --probe --env <name>`; precondition: the `Stand remedy:` line says authorized
  (`story_run.py stand_remedy`).
- Target: after the word check and the probe, before the person: when `stand_remedy` says authorized AND the stand row has a
  `bring_up`, ONE seam turn: `self.no_move({"why": "refusal", "kind": "environment", "stage": stage, "dispatch": "", "lead":
  <stand facts: name, env_probe.blocked_by_of(out), login answer>, "text": <probe output>, "site_fallback": lambda said:
  <the existing stand question, built as today>, "site_doors": <its tokens>}, moves=["stand_prepare", "person_does",
  "go_on_as_is", "stop_here"])` - the shape of `driver_machine.py:2153-2155` WITHOUT `"call": False` (M1); kind
  `environment` is not in `NM.EXCLUDED_KINDS`. Otherwise today's `site_seam_person("environment", ...)`, byte-identical.
  No new Driver member (the call is inline in `stand_check`).
- Edges: no stand recorded -> no turn (no `bring_up`), the question; the person's word already given -> no turn (the word
  wins); conductor `continue`/`retry` -> `stand_check` probes again (the docstring's loop), a second failure goes to the
  question with no second turn (one turn per `stand_check` entry, kept in `self.state["stand_turned"][stage]`); legacy
  `environment_pending` -> as today, via this road.
- Invariant (positional): called only by a stage with something to run, before its first role; the turn sits AFTER the word
  check and the probe, BEFORE the Person; what stays unreachable: a role starting on an unconfirmed stand that no word and no
  successful re-probe passed; a bring-up the project did not authorize.
- Error direction: toward the question.
- Test: rows in `scripts/tests/test_story_run_s6.py` (keep, stand rows 1827-1865) and `test_human_questions.py:467` (S5):
  "unconfirmed stand + authorized remedy + bring_up -> one conductor turn, then the question"; "not authorized -> question,
  conductor calls 0".

**Edge E-7 - a case needs a second stand or device instance (axis 7)** - node E7, NOT dispatched before F-5
- What code does: carries the need as the case designer wrote it and the project's recorded preparation actions; counts
  nothing (AR-2).
- What the role tries: the runner, at S6, brings up another instance only with actions the project authorized, records it in
  `work/evidence/manual/<case>/tried.md`. Current text: `agents/qa-runner.md` names `tried.md` (line 65) and has no rule on
  preparation actions (grep `tried\.md|authoriz|prepar`, §13) -> the rule is new text in node E7.
- What remains for the person: hardware, a licence, an account, an action the project did not authorize - handed with what was
  tried. Invariant: no instance is started that the project did not authorize; no role text names "two emulators" (P2).
- Streams that do NOT depend on F-5: 1, 2, 3, 4a, 4b, 5a, 5b, 6, 7 (stream 6 runs on F-5(a), the status quo).

### Class C - unproven doors

**r11 - `scripts/driver_stage_s5.py::stage_S5` (226-231) + `scripts/controller.py` op `code_only` (6080-6098)** - stream 5b
- Now (read): `if not scope.get("scope"): raise Refusal("S5: stage-scope returned no automate cases: ...")`; `code_only` refuses
  any stage outside {S0, S6, S7, S8} (6087-6088; pin `test_controller_state.py:1145`, per the critic's read). NE25 says S5
  closes. Axis 5 row "Code-only stage closes" (C3-2, 5378bbef) kept S5 refused; B-006 is the class carrier (§3).
- Target: a DERIVED empty automate scope (`scope["derived"] is True`, `scope["scope"] == []`), placed right after
  `stage_scope` and before `s5_todo`: (1) if `work/automation-manifest.json` is ABSENT, the driver runs `manifest_put.py --task
  <T> --fragment '{"tests": [], "unresolved": []}'` once (AR-14: the one writer); (2) `self.close_by_code("S5", "nothing to
  automate: the approved plan names no automate case", ["work/automation-manifest.json", "work/test-plan.json"],
  finalize=False, site="s5.nothing", digest="nothing to automate")`. `driver_core.py::CODE_CLOSE_SITES` gains `"s5.nothing":
  ("S5", "there was nothing to automate")`. `code_only` accepts S5 only when the controller's own `stage_scope("S5")` is
  derived and empty (xref, never the request's word); the refusal text for every other stage keeps its meaning and names S5's
  condition. An UNDERIVED empty scope keeps a Refusal reworded to FR-1 with a door ("the plan's dispositions could not be
  read: <reason>; rework S3 or record dispositions, then S5 runs again").
- Writer check (B2, AR-23), by reading `manifest_put.py` main path 2486-2706: the only refusal of an empty-content fragment is
  2498-2501 ("carries no manifest keys at all"), which a fragment with `tests` avoids; every later check iterates the
  fragment's lists; the commit (2651) then prints "cases now in the manifest: none" (2671) and returns 0. The builder confirms
  it with one run on a fixture story in its worktree BEFORE the edit (output in the report); if it refuses, the stream stops and
  returns the evidence (the one-writer road is then impossible: a fork to the Lead).
- Edges: manifest present (an earlier S5 wrote rows, the plan was reworked to all-manual) -> nothing is written; the close cites
  it (S6 takes its automation scope from the plan, not the file); `manifest_put` exits `EXIT_COMMITTED_STALE` -> the driver runs
  `manifest_put.py --task <T> --recover` once and re-checks the file; any other non-zero exit, or still absent -> `Refusal`
  naming exit code and the door `manifest_put.py --task <T> --recover`, WITHOUT quoting the writer's text (its "event committed;"
  words would match `KNOWN_REFUSALS` row `committed_event`, `driver_dispatch.py:55`, whose `recover` does not rebuild the
  manifest projection, 47-50); a live S5 dispatch -> `code_close_conflicts` refuses (unchanged); underived -> refused with door.
  The note at `driver_dispatch.py:47-50` ("the driver does not run manifest_put today") is corrected in the same commit.
- Invariant (positional): no close over a scope nobody could read; no close while a dispatch of S5 is live; the manifest is
  written only by `manifest_put.py`; no S5 close leaves the required output absent.
- Error direction: toward the Refusal on any doubt about derivation.
- Test: rows in `scripts/tests/test_s5_window_leftovers.py` (keep, rig at 692 ff.): "derived empty, no manifest -> manifest_put
  called with the empty fragment, close site s5.nothing"; "derived empty, manifest present -> not called, close"; "manifest_put
  stale -> recover once"; "underived -> Refusal with door"; `scripts/tests/test_controller_state.py` (keep) pin 1145 updated and
  row "S5 code_only with a non-empty derived scope -> refused"; `test_null_outcomes.py` green.

**r12 - `gate_preflight.py::Rehearsal.check_s5_runtime_probe` bound** - no code change; the pin moves (B4) from the quarantined
`test_story_run_gate_repair.py` to a driver-rig row in `scripts/tests/test_gate_preflight.py`: "write exits 0, finding
repeats -> after `GATE_REPAIR_CAP` the list goes to the conductor once, never a third round". Stream 5a.

---------------------------------------------------------------------------------------------------------------------

## 3. All-manual story, S5 -> S8 (B2), and B-006

B-006 (`plans/BACKLOG.md:79`, frozen) items, each walked in code:

| item | today (read) | verdict |
|---|---|---|
| (i) S5 with no automate scope closes normally | refused (`driver_stage_s5.py:230-231`) | IN: r11, stream 5b |
| S6 of an all-manual story | auto scope empty, manual scope non-empty -> `stand_check`, `build_check`, manual lane (`driver_stage_s6.py` 502-518); the manifest exists after 5b; `check_delivery.py:712-714` refuses a MISSING manifest, so 5b's write is load-bearing | passes after 5b |
| (ii) S7 reads `not_executed` with nothing to triage | a manual `inconclusive` (`manual_evidence.py:35`) or `unprepared` row with no `fail` makes `execution_status` `not_executed` (`finalize_task.py:629-637`); S7 refuses it after a real S6 (`driver_stage_s7.py:13-20`) | IN: stream 7, F-12 |
| (iii) gate A does not ask about toolchain/keys at zero automate rows | executor: asks nothing (2841-2851); toolchain: collects whenever `tests_root` is a folder, and `not_started` raises a card about 0 cases (2971-2977) | IN: stream 5a item 5 (toolchain returns with no question when `automate_rows()` is empty); keys: `check_s5_credentials` not read here -> same item: the builder reads it; if it raises a card at zero automate rows it returns like 2841-2851, else no change |
| (iv) required outputs per role (bug-reporter vs the scribe's `test-report.md`) | S8 `required_outputs` are the scribe's three files (`stages.json:296-300`), independent of automation | OUT: no automation dependence found in the stage contract; the role-order question is live-run territory (L4 reaches S8; a failure there opens a finding) |
| (v) delivery without automation is a legal outcome | `check_delivery.py` reads the manifest (337, 472, 712, 732, 844); with an empty one present no refusal of "missing" fires | OUT of code change: L4 proves it live |

Sibling axes: SIBLING_MAP axis 5 (stage twins: `s5.nothing` <-> `s6.nothing`; code-only closes) and axis 38 (the dry census:
`s5.nothing` is a new code-close site; `dry_exits.py --check` decides whether it is a subject and the row lands in
`scripts/tests/fixtures/driver-exits/s5.json` in the same commit).

---------------------------------------------------------------------------------------------------------------------

## 4. Refusals, doors, text

Every reworded or new text obeys FR-1, FR-2, FR-57; person-facing words obey `references/human-questions.md` (checked by
`human_text.problems` where the site already checks). Nothing removes a door a role holds; every seam turn keeps the site's
question as fallback. Notes inform and pass nothing (FR-4).

---------------------------------------------------------------------------------------------------------------------

## 5. Overlaps with open batches (t-1238) and order

| stream | neighbours | order |
|---|---|---|
| 1 surfaces, readiness r3, `_row_of_nobody` | readiness-set (other functions); OF5-1 (`planning_contract.py`, another function) | items 1-3 free; item 4 after stream 7 merges |
| 2 p1/p2 | OH3-35 (in work), XT2-1, TQ1-6 | after OH3-35, or late node merges main |
| 3 r9 pin | none (test only) | free |
| 4a r5 | RD1-24, PC4-2 | strictly after RD1-24 |
| 4b F-4(b) | EP1-* manual evidence nodes (Lead greps piles for `manual_evidence.py` before launch) | after F-13 word and a plan critic (meaning change, PROJECT.md package p.6) |
| 5a gate A | RD1-13 -> RD1-14 (same file queue), EP1-26, CX2-15, PC4-4 | after RD1-13/RD1-14; before PC4-4 (owner-blocked) |
| 5b S5 close | PC4-5 (controller cut), conductor/3 C3-24 | free; if PC4-5 lands first, edit the part holding `code_only` |
| 6 stand_check + OF5-5 | OF5-5, DH2-1, FV3-21 (in work), FV2-38 | one node with OF5-5 (F-9 = (a)); after FV3-21; OF5-5 owns cell corrected first (D-5) |
| 7 S7 entry | none read | before stream 1 item 4 and node 4b |
| E7 runner text | F-5 | not before the owner's answer |

PC4-2/PC4-4: as r1 §4 (both owner-blocked; U7 goes first; if unblocked first, U7 re-reads the part names).

---------------------------------------------------------------------------------------------------------------------

## 6. Streams as builder nodes and dispatch templates

All streams: given = this spec (its sections for the stream) + `design/factory-rules.md` whole + `docs/TESTING.md`. Witness:
`python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>` once after all edits. FR walk A-G in the
report. Commit: `architecture:` naming the stream's AR-n and how kept, `judgment:` per `tools/architecture_gate.py` (never bare
`none`). Header lines are content for `python -B tools/dispatch_new.py`, which prints them checked. Every stream also runs
`python -B ai-packages/qa-factory/scripts/tests/dry_exits.py --check` (axis 38) when it adds a close site, a route or a Person
kind, and keeps `NO_MOVE_BASELINE` (`audit_factory.py:1667`) shrink-only.

**Stream 1 - surfaces and readiness (r2, r3, a2D1, s6.unknownword, `_row_of_nobody`)**
- items: (1) `declared_surfaces` `undeclared` + readiness comment 1314-1315 - test_readiness rows; (2) `_who` and three literals
  -> "role" - test_readiness data-seam row; (3) `surfaces.json` words role-first + `words.undeclared` - same row; (4)
  `_row_of_nobody` converts (after stream 7) - test_question_branches rows; (5) r3 split and note - test_readiness rows.
- commit: `architecture: AR-2, AR-1, AR-28 -- ...`; `judgment:` naming the units of 1.2.
```
given: C:/QAFactory/forge-repo/docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r2.md (sections 1, 2 r2/r3/a2D1, 4, 6 stream 1), C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md, C:/QAFactory/forge-repo/docs/TESTING.md
owns: C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/surfaces.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/surfaces.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/readiness.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/planning_contract.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_readiness.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_question_branches.py
non-goals: Android/iOS rows, drivers, AGENT_HANDS as data (U8); quarantined test files (test_surfaces.py, test_mobile_road.py); the doctor skill text; readiness remedy.steps (OF5-9)
handoff: builder report with the witness; the list of quarantined assertions the change contradicts
edges: spec 2 r2 (profiles absent -> undeclared; unreadable table -> surfaces.unknown; web+api -> no key, 0 table reads), r3 (declared byte-identical; URL-less note; mixed), a2D1 (broken table / unknown profile / mixed hands -> old road)
DoD: rows of spec 2 r2, r3, a2D1 green in keep files; pins test_readiness.py:873-874,917 green; `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>`
siblings: planning_contract._row_of_nobody (included); driver_stage_s6._cases_all_on_driver (reads is_device_row only: n/a)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r2.md
```

**Stream 2 - onboarding discovery (r1)**
- Doc-dispatch witness keys (verbatim, before the run): K1 `application's own build`, K2 `a driver the factory knows`, K3
  `the product runs on a device or as a native application`, K4 `the agent will try these cases with what it can reach`, K5
  `hands you only what it cannot`; negative control K6 absent. Script attached in full, not committed. K3/K4 are new (M7:
  `The names are examples, not a list` and `I do not know` already stand at p1:43 and p2:226).
- commit: `architecture: AR-2 -- ...`; `judgment: none -- markdown of a role's phase text, no code check`.
```
owns: C:/QAFactory/forge-repo/ai-packages/qa-factory/skills/qa-onboarding/phases/p1-discovery.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/skills/qa-onboarding/phases/p2-interview.md
non-goals: the authorization question for starting another instance (F-5, node E7); platform/tool words (U8); p4-generate.md
edges: spec r1 edges (no app module; split repo not located; web+native both; already onboarded)
DoD: K1-K5 present, K6 control fails; `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>` if it prints rows for these files
siblings: none -- the row is the one place the surface is detected (t-1203 ob.detect)
```

**Stream 3 - S0 pin (r9)**
```
owns: C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_no_move_seam_sites.py
non-goals: driver_s0.py code; any new conductor row (F-11)
edges: missing capability -> s0.readiness question, conductor calls 0; exit 2 -> gate_refusal
DoD: two rows green; `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>`
siblings: none -- r9 is the only S0 site of the class
```

**Stream 4a - probe text (r5)** - after RD1-24
```
owns: C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/probe_by_code.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_probe_by_code.py
non-goals: the red-sandbox receipt (RD1-24); _probe_refusal (EP4-1); new assertion_probes rows (U8)
DoD: row "red-sandbox door before the tooling sentence" green; `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>`
```

**Node 4b - F-4(b) log verdict (r4)** - after the Lead's F-13 word and a plan critic
```
owns: C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/manual_evidence.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/skills/qa-story/phases/s6.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_manual_evidence.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_story_run_s7.py (rows of 4b only; stream 7 merges first)
non-goals: run_suite.py (its no-report sentence already stands); execution_request.py; reducer changes
edges: spec 2 r4 (no log; stale block; profile with a reporter; reporter absent; records before)
DoD: admission rows and the S7 row green; the reporter-none measurement attached verbatim; `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>`
siblings: run_suite.no_report_words (read only: already says the default)
```

**Stream 5a - gate A (r8 three roads, B6, Q12, r12 pin, B-006 iii)**
- items: (1) `executor_install` helper + decision in `check_s5_executor`; (2) the same in `check_s5_toolchain` `not_started`;
  (3) `run` tuple order; (4) driver side: `close_executor_bound`, `unturned_executors`, `hand_to_conductor` finally, series
  re-hand, `CHECK_WORDS`; (5) toolchain returns with no question at zero automate rows; `check_s5_credentials` read and aligned;
  (6) Q12 notes; (7) road 3 `install` field + halts.md row; (8) r12 pin. Each item: its row in §2.
- commit: `architecture: AR-17, AR-25, AR-28, AR-14 -- ...`; `judgment:` naming check_s5_executor, check_s5_toolchain.
```
owns: C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_preflight.py (check_s5_executor, check_s5_toolchain, check_s5_credentials, executor_install, executor_turn_had, run)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_gates.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/run_suite.py (refuse_missing_executor only)
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/halts.md (row `run_suite: executor_unavailable` only)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_preflight.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/driver-layers.json (the two new DriverGates members)
non-goals: check_s5_stand_limits (RD1-13), provenance (RD1-14), the Rehearsal cut (PC4-4), collect_base one-road (U8), check_s5_dependencies unknown (F-14)
edges: spec 2 r8 (record absent/unreadable/write fails; no-driver road; install fails; handed; zero automate), Q12
DoD: rows of spec 2 r8, Q12, r12 green; conductor calls 0 when no install known; `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>`; `dry_exits.py --check` 0 discrepancies
siblings: the three roads (all here); halts.md map (test_silent_passes.py:879, first cell unchanged)
```

**Stream 5b - S5 close (r11, B2)**
```
owns: C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_stage_s5.py (stage_S5)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/controller.py (op code_only validation only)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_core.py (CODE_CLOSE_SITES row only)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_dispatch.py (the comment at 47-50 only)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_s5_window_leftovers.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_controller_state.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/driver-exits/s5.json (if dry_exits names s5.nothing)
C:/QAFactory/forge-repo/ai-packages/qa-factory/design/controller-blocks.md (if the generator re-renders it)
non-goals: S6's s6.nothing; window logic; null-outcomes rows; manifest_put.py itself
edges: spec 2 r11 (derived/underived; manifest present/absent; stale -> recover once; other exit -> Refusal without the writer's text; live dispatch)
DoD: the writer-check run in the report; rows green; pin 1145 updated; `test_null_outcomes.py` green; `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>`; `dry_exits.py --check` 0 discrepancies
siblings: S6 twin s6.nothing (unchanged, AR-19); B-006 items (section 3)
```

**Stream 6 - stand question (r10 with OF5-5)** - after FV3-21; OF5-5 owns cell corrected first
```
owns: C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_stage_build.py (stand_check)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/waiver.py, check_delivery.py (stand_word), driver_stage_s6.py (s6_no_stand) -- OF5-5's part
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_story_run_s6.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_human_questions.py
non-goals: the stand question's words and prices (DH2-1, FV2-38); manual_lane_plan (FV3-21); E-7; a new Driver member
edges: spec 2 r10 (no stand; word given; one turn per entry; not authorized -> no call)
DoD: OF5-5 step 1 result attached; rows green; NO_MOVE_BASELINE unchanged or lower; `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>`
siblings: build_check (no person-first door of this class: questions come from the probe record): n/a
```

**Stream 7 - S7 entry over manual targets (F-12, B-006 ii)**
- Target by F-12 (a): in `failures_to_triage`, a report whose `execution_status` is `not_executed` and whose
  `contract.triage_targets(report)` holds manual targets (`manual`, `unnamed_manual`, `observations`, unprepared) is triaged:
  the refusal at 18-20 is kept for a report with no such target. Error direction: toward dispatching the analyst (a role turn),
  never toward a pass: `execution_status` is not rewritten, delivery still reads `not_executed`. Adversarial: an automated run
  that broke (no results) beside a manual inconclusive -> the analyst triages the manual targets; the automated half stays
  `not_executed` in the report and reaches delivery under its own reason.
```
owns: C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_stage_s7.py (failures_to_triage)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_story_run_s7.py
non-goals: finalize_task.py execution_status; s7_pretriage
edges: not_executed + targets -> triage; not_executed + none -> the refusal as today; code-only S6 -> as today
DoD: rows "inconclusive only -> triaged", "unprepared only -> triaged", "no target -> refused" green; `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>`
siblings: B-006 (ii); 4b and stream 1 item 4 depend on it
```

**Node E7 - runner preparation text (E-7)** - NOT dispatched before F-5
```
owns: C:/QAFactory/forge-repo/ai-packages/qa-factory/agents/qa-runner.md
non-goals: code; any platform word (P2)
DoD: doc-dispatch witness with keys written after F-5's answer
```

---------------------------------------------------------------------------------------------------------------------

## 7. Live proof (FR-33) - rows for pile `live-runs`

L1 onboarding of a native project with no known driver records the surface and says the default (r1). L2 readiness/doctor
print `undeclared` or role-first words; an undriven case is walked by the agent and recorded `unprepared` with what it tried;
S7 triages it (a2D1, r2, stream 7). L3 an unconfirmed stand with an authorized remedy gets one conductor turn; a missing
launcher with a known install command gets one; the person's question only after (r8, r10). L4 an all-manual plan passes S5 by
code AND S6, S7, S8 through to a delivery verdict (B2, §3). L5 S0 with a URL-less row says the default (r3). L6 a `reporter:
none` run: the runner's log verdicts carry S7 (4b). E-7's row waits on F-5.

---------------------------------------------------------------------------------------------------------------------

## 8. Readers of every touched file (designer rule 7; Q13(d))

The `owns_readers.py` block was not attached to this dispatch; the critic ran it ("readers: 724 outside owns ... base
b4eb74df"; HEAD f7ab564a with no diff of the read files). Its lines, answered:
- `config-keys.json` names declared_surfaces, _check_plain_environment, check_s5_executor: no function renamed, no config key
  added or removed -> unchanged (stream 1/5a builders confirm the rows name functions, not values).
- `gate-registry.json`, `block-names.json` name stand_check: name and block words unchanged -> unchanged.
- `driver-layers.json`: s0_rest, stage_S5, stand_check homes unchanged; two new DriverGates members -> changes in stream 5a
  (sole writer of the fixture in U7; stream 6 adds no member).
- `judgment-census.json`: rows 415/1118 unchanged; no row added (§1.2).
- `null-outcomes.json` names stage_S5 (NE3/NE4/NE25): guard name unchanged; NE25 becomes true -> unchanged.
- `test_silent_passes.py` (s0_rest, stand_check, halts map): members exist, first cells unchanged -> unchanged.
- `test_conductor_investigates_first.py` (halts.md 18 rows, markers): row count and marker unchanged -> unchanged.
- quarantined readers `test_surfaces.py`, `test_mobile_road.py`, `test_story_run_gate_repair.py`: not run by the canon; not
  edited; contradicted assertions listed in stream reports.
- `references/surfaces.json`: one reader `surfaces.py` -> changes in stream 1.
- `manifest_put.py` gains a caller (driver): `driver_dispatch.py:47-50` note -> changes in stream 5b.
- `state/executor-turns.json` (new): writer DriverGates.close_executor_bound, reader gate_preflight.executor_turn_had -> stream 5a.
- `stand_check` callers (`driver_machine.py:1508,1618`, `driver_stage_s6.py:517`, `driver_stage_s5.py:201,330`, rigs):
  signature unchanged.
- controller op `code_only` callers (`driver_dispatch.py::code_only`, `driver_stage_s7.py::close_by_code`): unchanged; S5 legal
  only under the derived-empty condition.
Not covered without the tool block: readers in `tools/`, `.githooks/`, `.claude/` of the touched package files - the Lead
attaches the block at dispatch (KNOWN MISSES of rule 7).

---------------------------------------------------------------------------------------------------------------------

## 9. Rule 10 four questions

Not a forge mechanism: package behaviour, carried by the architecture gate lines and the census. The new value "role" of
`hands` and the new file `state/executor-turns.json` are package contracts with one reader each; detectors: the test rows named.

## 10. Flags (code differs from a digest or the brief)

D-1..D-6 as r1 §9. New: D-7 r4's class A is already closed by `run_suite.py::no_report_words`. D-8 F-4(b)'s stated carrier
refuses automate obligations (`manual_evidence.py:1029-1033`). D-9 a manual `inconclusive`/`unprepared` without a `fail` makes
`not_executed` (`finalize_task.py:629-637`), an S7 stop for any story, not only all-manual.

## 11. Forks

Carried (Lead, r1 header and 17.11.2026): F-1 (a); F-2 (a); F-3 (a) - premise measured, holds as `unprepared`; F-4 (b) main
path; F-6 (a); F-7 split (now nine nodes: 1, 2, 3, 4a, 4b, 5a, 5b, 6, 7, plus E7); F-8 (a); F-9 (a); F-10 (a). OPEN, the
owner's: F-5.

New, returned:
- F-11 r9 row for `test_repo` missing: (a) none - the person's remainder (a folder the config names); (b) a new action row
  "record the tests folder discovery saw" in `conductor-actions.json` with a stream's owns. Recommend (a): no evidence of a leak;
  (b) writes a project fact on a role's reading.
- F-12 S7 over `not_executed` with manual targets: (a) `failures_to_triage` triages manual targets whatever the status (stream
  7); (b) `finalize_task` decides `failed` for an `inconclusive`/`unprepared` manual row. Recommend (a): narrow, the report's
  meaning unchanged; (b) changes `execution_status` for every reader (delivery, gate B). Meaning change either way: plan critic.
- F-13 carrier of F-4(b): (a) a `manual_evidence.py log-verdict` command admitted only under the three conditions of §2 r4; (b)
  the runner re-plans such cases as manual-agent through an S3 rework (a role round per story); (c) a typed log-verdict field in
  `run_suite.py`'s run block. Recommend (a): one existing writer of role verdicts, a narrow admission; (c) puts a role verdict
  into code's run record.
- F-14 `check_s5_dependencies` silent `unknown` (critic K5): (a) one gate note per unknown environment; (b) the reason joins
  only an existing card/note of the same profile; (c) U8 with the lock-format set. Recommend (b): says it where it matters
  without a note on every non-Poetry project.
- Q-U8 (Lead opens): `gate_preflight.py::collect_base` -> `launch_check.runner_row` as the one road for every runner's collect.

## 12. Small choices closed by the designer

- r3 moved to stream 1 (one owner of `test_readiness.py`).
- The turn record path `<task root>/state/executor-turns.json`, `{"turns": [{"key", "at"}]}`; key `profile|tool|digest`.
- `check_s5_dependencies` moved before `check_s5_executor` in `run` (the only order change).
- r12's pin and every gate row in `test_gate_preflight.py`.
- r10's turn kept in `self.state["stand_turned"][stage]`; no new Driver member.
- Example texts are drafts; final words are the builder's under `human-questions.md`.

## 13. Reading trail

Read: r1 spec (whole); verdict t-1242 (whole); brief (whole); `conductor-actions.json` (whole); `test-layers.json` 1-30,
1901-1930, 3224-3263, 4295-4334, 4730-4759 + Grep of test names and `covers` entries (keep 36-7155, quarantine 7209+);
`surfaces.py` 1-230; `readiness.py` 793-892, 1296-1320 + Grep check_* (404-410, 696-713, 1180-1256); `test_readiness.py`
840-929; `driver_s0.py` 420-449, 725-744, 2380-2439; `driver_machine.py` 2135-2164; `driver_conductor.py` 424-719;
`no_move.py` Grep (37, 41, 176-188, 521-560); `driver_gates.py` 1-80, 353-375, 612-680, 848-952, 985-1073;
`gate_preflight.py` 520-619, 2815-2994, 6075-6104 + Grep `check_s5_`; `dependency_drift.py` Grep states; `run_suite.py`
340-384, 1540-1589; Grep `refuse_missing_executor|executor_unavailable` (package); `skills/qa-story/phases/s5.md` 138-151;
`references/halts.md` 1-31; `test_silent_passes.py` 860-921; `driver_dispatch.py` 30-89; `stage_done.py` 460-499;
`driver_stage_s7.py` 1-40; `finalize_task.py` 600-659; `contract.py` 2157-2161, 4249-4265, 4385-4398, 4645-4669;
`manual_evidence.py` 1015-1049, 1840-1884, 2152-2163 + Grep (35, 1572, 1769, 1852); `manual_capture.py` 410-480;
`manual-capture-steps.json` 46-58; `import_test_receipt.py` 1-140; `judge_run.py` 1-60; `manifest_put.py` 2486-2706 + Grep;
`stages.json` 179-303; `check_delivery.py` Grep manifest; `driver_stage_s6.py` 470-529; `driver_core.py` 375-409;
`controller.py` 6076-6100; `driver_stage_s5.py` 215-239; `env_probe.py` 60-77, 1125-1149 + Grep; `audit_factory.py`
1655-1684; `docs/SIBLING_MAP.md` 640-659 + Grep axis 5 heading (116); `plans/BACKLOG.md:79`; `docs/OWNER_PRINCIPLES.md` 58-61.
Greps (Grep tool, case-sensitive unless noted): `_row_of_nobody|stays as planned|row_for_profile` (scripts); `s6\.nothing`
(package, tests); `tried\.md|authoriz|prepar` in `agents/qa-runner.md` (2 hits: 51 "Unprepared", 65 "tried.md" - the hit on
"Unprepared" is the positive control of the lower-case stem; a line starting with capital "Prepar"/"Authoriz" would be missed).
Taken from the critic's trail, not re-read: `test_controller_state.py:1145`, `judgment-census.json` rows 415/1118, the
owns_readers run. Not read: `check_s5_credentials` (stream 5a item 5 reads it with both branches stated), `story_run.py
stand_remedy` body, `qa-runner.md` beyond the grep. One Glob timed out (not used as a claim).
