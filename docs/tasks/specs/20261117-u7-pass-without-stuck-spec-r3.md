# Spec U7 "pass without getting stuck" - r3 (fix round t-1258 of t-1252) - DRAFT for Lead acceptance

Fresh-worker fix round. Input: r2 `docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r2.md` (not edited), the plan critic's
second verdict `docs/tasks/specs/reviews/t-1252-u7-pass-without-stuck-plan-r2.md` (NEEDS WORK: N1-N3, M-a..M-i), the brief
`20261117-u7-pass-without-stuck-brief.md`, and the Architect's decisions on the verdict (17.11.2026, carried below, not
re-decided). This file is WHOLE: it replaces r2. Text the verdict does not touch is r2's, unchanged. Every load-bearing code fact
r3 adds or changes was re-read on 17.11.2026 at the cited `path::symbol` (trail, section 13). Paths are from
`ai-packages/qa-factory/` unless they start with `docs/`, `plans/` or `tools/`.

Goal (owner, 17.11.2026, verbatim in the brief): the factory, knowing nothing of a project's form, passes every stage without
getting stuck and lets the agent do its work; "role first": the person gets only the remainder (a device, credentials). A
stage may cost a little more if quality is bought; blocking is never acceptable.

**Lead decisions carried (17.11.2026, r2 header).** B1-B6, M1-M8 accepted; F-1 (a), F-2 (a), F-3 (a), F-6 (a), F-7 split, F-8 (a),
F-9 (a), F-10 (a), F-11 (a), F-14 (b), Q-U8 to U8; F-5 OPEN (the owner's).

**Architect decisions on t-1252 (17.11.2026), input to this round, not re-decided:**
- N1: F-13 (a), (b), (c) withdrawn; F-4 re-decided: a role's reading of a no-report run is the analyst's TRIAGE at S7, never a
  run result and never a manual-evidence record. Node 4b is REMOVED (no change to `manual_evidence.py`, `coverage_contract.py`,
  the reducer, `current_manual_checks`). r4 moves into stream 7: the S7 entry admits a `not_executed` report of a FINISHED S6 whose
  undecided rows a role can triage (manual targets, F-12, AND automated instances of a no-report run); one predicate, one home,
  read by both twins. Refused stays: an S6 halt, and a `not_executed` with nothing a role can triage. `execution_status` is never
  rewritten; code never turns a log into `passed` (FR-58). Delivery: such a run is not `run_not_deliverable`; it is its own KIND
  with verdict `after_checks`, unless the analyst found a failure (a red is a red). The runner/analyst instruction is one paragraph
  in the analyst's page.
- N2: one predicate in `s7_pretriage`, read by `failures_to_triage` and `check_delivery.run_reasons`, narrowed so a mixed story whose
  automated half broke keeps its honest `no`; `check_delivery.py` (run_reasons) joins stream 7.
- N3: `acceptance.py::run_witness_excused` gains an outcome bound to the controller's S5 code-close receipt (`stages.S5.code_only`),
  never to `tests == []` alone; that function joins 5b.
- M-a..M-i accepted as written in the dispatch of t-1258; M-g (2): stream 1 owns exactly the axis 2 and axis 7 cells of
  `design/architecture.md` section A and edits them in its own commit.

**What this round found that the Lead must see (code facts that differ from the verdict or the decision's wording; section 10):**
D-10 the no-report `parse_gap` lives in the run SUMMARY, not the run block; the block carries `evidence[].reporter` and per-instance
rows `not_run` / "report row missing". D-11 an instance of a no-report run is not a triage target today, and the reducer archives a
triage row bound to no current failure: the analyst's reading has no carrier -> fork F-15 (stream 7 is split: 7a dispatchable now,
7b on F-15). D-12 the delivery `no` of a no-report test comes from three producers (run_reasons, the ledger, the traceability gap),
not one. D-13 an unprepared walk reads trace gap `result:none` -> `chain_broken` (`no`, owner product), so the critic's walk "the
`unprepared_walk` record speaks after N2" does not hold in code -> fork F-16. D-14 `test-layers.json` is at `scripts/tests/`, and
`test_traceability.py` is quarantined.

**Lead acceptance of r3 (Architect session, 17.11.2026; t-1258).** Accepted as the spec of U7; r2 is superseded. Spot-checks by
reading the carrier: `scripts/contract.py::triage_targets` (only `failed`/`error` result rows are targets today - D-11 holds);
`scripts/acceptance.py::run_witness_excused` (takes the manifest only, returns `""` for empty lists - N3 and D-17 hold). New
forks, decided by the Architect ("решила сама", the owner may reverse any of them):
- F-15 = (a): a no-report instance becomes a triage target (`report_unread`), the analyst answers it, delivery says `run_unread`
  (`after_checks`) or the analyst's red.
- F-16 = (a): an unprepared walk speaks at delivery as its own `after_checks` item, not as `chain_broken` `no`. Ground: P21 (the
  third outcome is "part of the cases is left with the person"); Fork 13 A of an earlier spec yields to the owner's principle
  for THIS case only - coverage still keeps `verified` False (AR-28). It is node 7c, after 7b, written by the Lead in its dispatch.
- F-17 = (a): the owner word of `run_unread` is `factory`.
- F-5 stays OPEN, the owner's; only node E7 waits for it.
Dispatch order: streams 1 (items 1-3, 5, 6; item 4 is a later node 1b after 7a merges), 5a, 5b and 7a go to builders now - their
fixes are the plan critic's own (t-1252 N2, N3, M-a..M-h), verified by the Lead against this file. Streams 7b and 7c change the
MEANING of "a triage target" and of a trace gap: they go to one plan-critic pass (this file's 7b parts + F-15, F-16, F-17) before
their dispatch; they follow 7a anyway.

---------------------------------------------------------------------------------------------------------------------

## 0. Finding of t-1252 -> where fixed

Round 1 findings: fixed as r2 section 0, confirmed by t-1252 K1. Rows K1 marks "partly": B1 (-> N1 below), B2 (-> N2, N3, M-e,
M-g below), M8 (-> M-h below), Q13(d) (-> M-f below).

| finding | what r3 does | where |
|---|---|---|
| N1 node 4b / F-13 not executable | Node 4b removed, F-13 withdrawn (Architect). r4 is now stream 7: 7a admits the manual half at S7 and at delivery through one predicate; 7b (automated half of a no-report run) needs a carrier the code lacks (D-11) -> F-15, recommended (a): the instance becomes an analyst triage target through a producer field on the block row, and delivery reads it as the new kind `run_unread` (`after_checks`) unless the analyst's row is a failure verdict. Every producer of the `no` is named (D-12) | §2 r4, §6 7a/7b, §11 F-15, F-17 |
| N2 delivery twin unchanged | `s7_pretriage.triageable_not_executed` is the one predicate; `failures_to_triage` and `check_delivery.run_reasons` read it; narrowed: any automated row not passed (7a) or not a no-report row (7b) keeps the refusal and the honest `no`. Walk of an all-manual story with only `inconclusive`/`unprepared` rows written to the verdict, with which kind speaks (§3); the `unprepared` case does not reach `after_checks` in code (D-13) -> F-16. §3 (v) corrected | §2 r4, §3, §6 7a |
| N3 empty manifest fails the witness readers | `run_witness_excused(manifest, task_root=None)` gains outcome `nothing` bound to `stages.S5.code_only` + status `completed` + exactly empty lists; check_witness and validate_artifacts pass the task root; handoff_check unchanged (reads `pending` only). All readers of the manifest and of `run_witness` enumerated with a verdict | §2 r11, §6 5b, §8, §13 D5 |
| M-a two person contacts | The `s5_executor` finding's `fix` text (gate_preflight.py, stream 5a) tells the conductor to end its turn without asking; the card at the next rehearsal is the one question. The action row is not edited (its other context, the S5 note, keeps the person's offer) | §2 r8, §6 5a |
| M-b road 3 bound and role door | `executor_install` returns no command when `executor_turn_had` holds (one call per key on all three roads); `skills/qa-story/phases/s5.md:144` joins 5a with the corrected sentence. No driver code reads `executor_unavailable` (D-15), so the road "role stop -> conductor" is proved by a rig row before the edit, or the stream returns | §2 r8, §6 5a |
| M-c credentials | `check_s5_credentials` unchanged; B-006 (iii) "keys" OUT (the login is shared with S6, `gate_preflight.py:4627-4631`, AR-19; manual-agent cases need it at zero automate rows) | §3, §6 5a |
| M-d F-14 unowned | Item 9 of stream 5a: `check_s5_dependencies` keeps the `unknown` entries; their reason joins an existing card or note of the same profile; no card/note of that profile -> nothing said | §2 r8, §6 5a |
| M-e derived-empty reads past unknown | `controller.stage_scope` gains key `undisposed` (approved cases whose plan row has no disposition); the S5 close and `code_only` S5 require `derived`, `scope == []`, `unmapped_scope == []`, `undisposed == []` | §2 r11, §6 5b |
| M-f readers of r2's new paths | each of the 10 `more` lines, plus check_delivery.py and acceptance.py, answered | §8 |
| M-g stale texts | (1) SIBLING_MAP axis 5 row: exact replacement sentence, the Lead edits it in the commit merging 5b; S5 does NOT owe the same precondition and bound as S7 (§2 r11). (2) architecture.md cells: axis 2 and 7 new text, stream 1; axis 3 cell changes with 7b, so 7b owns that one cell (architecture.md:72 requires the same commit; D-16). (3) `driver_stage_s7.py` 14-16 and 87-93 comments: stream 7a | §2 r11, §6 1/5b/7a/7b |
| M-h census and ratchets | 5a owns `scripts/tests/fixtures/driver-exits/gates.json` (the group `dry_exits.py --check` names for a DriverGates road); 5b owns `s5.json`. §1.2: no `log-verdict` row (removed with 4b); a row per check r3 adds or alters | §1.2, §6 |
| M-i variety walk labels | relabeled in the form of architecture.md section A; axis 13 = F-1(a); r9's capabilities under axes 3, 5, 8; unknown-value outcome of axes 2, 3, 4 restated after N1-N3 | §1.3 |

---------------------------------------------------------------------------------------------------------------------

## 1. Architecture, owners, variety walk

### 1.1 AR-n touched, with the change check each demands (copied into every stream's DoD)

| AR | how the spec touches it | change check (DoD) |
|---|---|---|
| AR-2 | every changed site ends in a role move, a declared default said out loud, or the person's remainder named | per changed site, one row whose input is an unknown axis value and whose outcome is "a role move is offered / the default is said", never silence |
| AR-1 | `surfaces.json` words (stream 1); the new delivery kind and its states/gaps are rows of `references/delivery-verdict-kinds.json` (7b); no list of platform, language or tool names enters code | the diff adds no tuple/set literal of surface/language/tool words to a `.py` file (reviewed; the existing `LANGUAGE_WORDS` row of the readiness table covers the words) |
| AR-9 | every new or reworded refusal/note names what it expected and a door its receiver can use | a row per new text asserting its door token is one the receiver executes (FR-2) |
| AR-13 / AR-14 | new readers go through existing one readers; "a `not_executed` a role can triage" has ONE home (`s7_pretriage.triageable_not_executed`) read by S7 and delivery; "no run to witness" stays ONE reader (`acceptance.run_witness_excused`); the empty manifest is written by its one writer `manifest_put.py`; the executor-turn record has one writer (driver) and one reader (gate_preflight); run blocks are read through `run_history.read_run_blocks` | no second reader of `surfaces.json`, the readiness record, the manifest, the turn record or the S6/S5 receipts (critic Q6); `driver_stage_s7` and `check_delivery` call the predicate, they do not restate it |
| AR-17 | r8 and r10 go seam-first where a row exists; r9 stays person (no row) | r8/r10 rows: the conductor is called once before the person's card/question; with the row's precondition false, NO conductor call (counter 0); person contacts per missing launcher = 1 |
| AR-22 | S5's required output exists after a code close and every reader of it accepts it; the 7b field `reason_code: report_unread` has its producer (`run_suite.build_run_block`) and its readers (`contract.triage_targets`, the predicate) | a row: derived-empty S5 leaves `work/automation-manifest.json` with empty `tests`/`unresolved` AND `check_witness` / `validate_artifacts` accept it under the receipt |
| AR-23 | NE25's empty S5 outcome becomes true in code | `test_null_outcomes.py` green; the S5 row of the stream |
| AR-25 | every new state has a way out: the s5_executor fixable finding (-> card), the S5 code close (-> S6), S7 with a role-triageable `not_executed` (-> triage), a no-report instance (-> analyst row -> `run_unread` or red) | a row per new state with its exit |
| AR-27 | a delivery reason reaches the report under its own owner: a manual-only `not_executed` is no longer `run_not_deliverable` (owner factory); a no-report test reads `run_unread` (F-17), or the analyst's red under the product | the `test_check_delivery.py` rows of 7a/7b name the kind and the owner |
| AR-28 / FR-59 | unknown never a pass: an underived, unmapped or undisposed scope never closes S5; an unreadable controller never excuses a witness or admits S7; an unreadable turn record reads as "turn had"; a run with no report is never `passed` by code; a mixed story with a broken automated half keeps `no` | a row per site with the unknown input and outcome "not closed / not ok / asked / refused" |
| AR-12 | restated truthfully (B3): r2 adds a line for projects with NO capability word (legacy configs included, F-1(a)); r3 a longer note only for URL-less undeclared rows; r8 adds one conductor session before the card ONLY when the dependency check holds an install command for that profile and no turn was had for the key; r10 adds one conductor session ONLY when `Stand remedy:` is authorized and the stand has a `bring_up`; Q12 adds one gate note for a non-pytest collect command; 7a dispatches the analyst on a manual-only `not_executed` that S7 refused before (a role turn instead of a stop); 7b adds one analyst row per no-report instance. Web/API projects outside those conditions: byte-identical | existing pins kept green (`test_readiness.py:873-874, 917`; the web rows of `test_gate_preflight.py`); a row per added call asserting the call count is 0 when its precondition is false |
| AR-19 | S5 close is the twin of `s6.nothing` (`driver_stage_s6.py` 502-513); S6 side unchanged; S7 entry and delivery `run_reasons` are twins through one predicate | named in the stream's commit |
| AR-29 | checks altered: §1.2 | census rows unchanged (no class change); ratchets only shrink |

AR-24, AR-26: not met (no person words or requirements change road).

### 1.2 Checks added or altered: owner and census class (AR-29, P27; M2, M-h)

| check (unit) | change | owner | census |
|---|---|---|---|
| `surfaces.py::declared_surfaces` | `hands` "person" -> "role"; `undeclared` entry | data | no census row; none added |
| `planning_contract.py::_row_of_nobody` | a `hands: none` row converts to manual-agent | data | no census row; none added |
| `readiness.py::_check_plain_environment` | URL-less undeclared row: the note says the default | data | no census row; none added |
| `driver_s0.py::Driver.s0_rest` | no code change (r9 cut); one pin row | data | no census row |
| `gate_preflight.py::Rehearsal.check_s5_executor` | missing launcher with an install command and no turn yet -> `factory_fixable`; else the card | data (routing a state to the conductor keeps owner `data`; the judgment is the conductor's, outside the unit) | row 415 `owner: data`, class `shape`: unchanged |
| `gate_preflight.py::Rehearsal.check_s5_toolchain` | `not_started` on the same road; silent returns said; no collect at zero automate rows | data | no change of row (none read) |
| `gate_preflight.py::Rehearsal.check_s5_dependencies` | `unknown` reason joins an existing card/note of the profile (F-14 b) | data | census row not read: the builder checks `test_judgment_census.py`; none added |
| `gate_preflight.executor_install` (new helper) | install command known for P and no turn had for the key | data | none added |
| `driver_stage_s5.py::stage_S5` | derived-empty scope -> empty manifest + code close | data | no census row; none added |
| `controller.py` op `code_only` + `stage_scope` key `undisposed` | S5 allowed only over its own derived scope with `scope`, `unmapped_scope`, `undisposed` all empty | data | none added |
| `acceptance.py::run_witness_excused` | outcome `nothing` under the S5 code-close receipt | data (a join of the manifest to the controller's receipt) | census row not read; builder checks; none added |
| `driver_stage_build.py::DriverStageBuild.stand_check` | conductor turn when `stand_prepare` is open | data | row 1118 `owner: data`, `shape`: unchanged |
| `s7_pretriage.py::triageable_not_executed` (new) | the one predicate: `not_executed` of a finished S6 whose undecided rows a role can triage | data (it reads shapes and joins; what the rows mean is the analyst's judgment at S7, accepted by S7's consumer road) | none added |
| `driver_stage_s7.py::failures_to_triage` | reads the predicate | data | none added |
| `check_delivery.py::run_reasons` | reads the predicate | data | none added |
| `probe_by_code.py::_no_entry` | text order only | data | none added |
| 7b: `run_suite.py::build_run_block` field `reason_code: report_unread`; `contract.py::triage_targets` set `unread`; `ledger.py::test_state` / `plan_row_state` state `not_executed:report_unread`; `check_traceability.py` gap `result:report_unread` | (F-15 a) | data; the analyst's verdict on the instance is judgment (role), its row is checked for shape only | none added; builder checks |

If `test_judgment_census.py` names a changed unit as needing a row, the stream stops and returns a question (no row is
invented). Commit lines: `architecture:` and `judgment:` in the form `tools/architecture_gate.py` checks (the one carrier of
the grammar; not copied here); `judgment: none` always carries ` -- <why>`.

### 1.3 Variety walk (architecture.md section A, "How the map is walked")

- axis 1: held by table|role -- `probe_by_code` red-sandbox road, `launch_check` runner rows; unknown value -> the red-sandbox road is named first (r5); a collect command that is not pytest is SAID (Q12), the one-road row is U8's
- axis 2: held by table|role -- `references/surfaces.json` (`hands`), the manual-agent runner; unknown value -> the agent role tries first (`hands: role`), records `unprepared` with what it tried, the analyst triages it at S7 (7a); no word at all -> `surfaces.undeclared` said (r2); at delivery the walk reads `chain_broken` `no` today and `unprepared_walk` `after_checks` only by F-16 (a)
- axis 3: held by key|role -- `run.reporter`, the S0 test root, the failure analyst; unknown value -> a reporter `none` run is `not_executed` and said (`run_suite.no_report_words`); with 7b its instances are the analyst's triage targets at S7 and reach delivery as `run_unread` (`after_checks`) or as the analyst's red; without 7b S7 refuses at entry as today; a profile WITH a reporter whose report is missing keeps the S7 refusal and `run_not_deliverable` (a broken launcher cannot be told from a pass); a `tests_root` that does not exist at S0 is the person's remainder (r9, no conductor row)
- axis 4: held by role -- the plan's dispositions; unknown value -> an all-manual plan closes S5 by code with an empty manifest only over a derived scope with no unmapped and no undisposed case (5b), owes no `run_witness` under that receipt, and a manual-only `not_executed` reaches S7 triage and delivery's per-case kinds (7a); dispositions unreadable or a case undisposed -> S5 refused with a door, never closed
- axis 5: held by key -- the ticket route's credentials at S0; unknown value -> the person's `s0.readiness` question (r9; no conductor row)
- axis 7: held by key|role -- `environments[]`; URL-less row: default said (r3); unconfirmed stand: `stand_prepare` first when authorized (r10); a second instance: E-7 (waits on F-5)
- axis 8: held by key|role -- the profile's install command, git on PATH; unknown value -> a missing launcher gets one conductor turn when the project names an install command, else the person's card (r8); git missing at S0 is the person's question (r9)
- axis 13: held by key -- the config's schema; unknown value -> a legacy config with no `profiles` now reads `surfaces.undeclared` (F-1(a)); the other legacy readiness keys stay absent
- axes 6, 9, 10, 11, 12: n/a -- no site of this spec reads the delivery target, people/process, language, task size or check kinds

No `narrows` line. A builder finding that a change narrows a project form returns it as a question.

---------------------------------------------------------------------------------------------------------------------

## 2. Sites: current behaviour read in code, target, edges, invariant, error direction, test

Test layers are `docs/TESTING.md`'s. Every new case is a ROW of an existing table in a KEEP file of
`scripts/tests/test-layers.json` (keep block from line 36; quarantine from 7209). A builder that finds its named file
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

**r4 -> re-classed B (B1).** See class B, r4.

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
  `ui`, `http`, `app`); `manual_evidence.py::build` refuses an attempt with no captures (1877: "Capture first:
  `manual_capture.py ui ...` or `manual_capture.py http ...`"). The agent's attempt is therefore recorded with
  `manual_evidence.py unprepared --not-walked <why> --observations-file <what it tried>` (args 2152-2157): no result, and
  `contract.triage_targets` counts it a target (`contract.py:4659-4662`). So F-3(a) holds in this form: the analyst at S7
  judges it; the person gets the remainder through S7's own road. Without stream 7a the story would stop at S7 entry (the
  report is `not_executed`: `finalize_task.py:629-637`). Item 4 of stream 1 is therefore dispatched only after stream 7a merges.
  What the delivery says for such a case is F-16 (D-13).
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

**r4 - S7 and delivery over a `not_executed` a role can triage (N1, N2; F-12 as widened)** - streams 7a and 7b
- Now (read):
  - The reducer makes `execution_status` `not_executed` whenever no deciding row failed and not all passed
    (`finalize_task.py:629-637`); deciding rows are the current automated rows except join-failed ghosts, plus every current
    manual check (629-631). A manual `inconclusive`, an `unprepared` walk (result absent) and an automated `not_run` each do it.
  - S7 refuses `not_executed` unless S6 closed on a code-only receipt (`driver_stage_s7.py::failures_to_triage` 13-20, reading
    `s7_pretriage.s6_closed_by_code` 309-318). Delivery's twin refuses the same way: `check_delivery.run_reasons` 1282-1297 via
    `_s6_closed_by_code` 1301-1308, kind `run_not_deliverable` (`assess` 2623) = `{"verdict": "no", "owner": "factory"}`
    (`references/delivery-verdict-kinds.json:41`).
  - A no-report run (D-10): `run_suite.py::run` (2288-2293) writes `no_junitxml` and, when `reporter != "pytest"`, the
    `parse_gap` of `no_report_words` (359-368) into the SUMMARY (`work/evidence/<label>-<ts>.json`, 2370-2382). The run BLOCK
    (`build_run_block` 470-606) carries `evidence[].reporter` (585) and one row per selected instance with `status: not_run`,
    `reason: "report row missing"`, `report_matched: False` (536-540); no `parse_gap` key. The same `parse_gap` sentence is also
    written for a DECLARED `junit-xml`/`trx` reporter whose report file is missing (2248-2262 then 2288-2293), and
    `inferred_read_words` for a guessed format that read zero tests (2282-2287).
  - Such an instance is no triage target: `contract.triage_targets` counts a `current_results` row only when failed/error
    (4638-4639); the reducer archives every triage row not bound to a current failure (`finalize_task.py` 726-743) (D-11).
  - Its delivery `no` comes from three producers (D-12): `run_reasons` (above); the ledger, `ledger.py::test_state` 1245
    `not_executed:no result for this test in run-report.json` -> `ledger_states.not_executed` = kind `not_executed` (`no`, owner
    product, kinds 28, 92); the traceability gap, `check_traceability.py` 86-92 `result:not_run` -> `trace_gaps.result` =
    `chain_broken` (`no`, owner product; pinned `test_third_verdict.py:149`).
- Target, 7a (the manual half; dispatchable on Lead acceptance of r3): ONE predicate
  `s7_pretriage.triageable_not_executed(task_root, *, awaiting: str = "") -> bool`, True only when ALL hold:
  1. `work/run-report.json` reads as an object and its `execution_status` is `not_executed`;
  2. S6 FINISHED: the controller's `stages.S6.status == "completed"`, or `awaiting` is non-empty (the S6 runner's dispatch awaits
     its consumer, `acceptance.awaits_acceptance`, which `stage_S7` already reads at line 57 and passes in); the controller read
     is the same as `s6_closed_by_code`'s (309-318);
  3. every deciding automated row reads `passed` by `contract.result_status` (rows excluded exactly as the reducer excludes them:
     `current_reason == finalize_task.JOIN_FAILED`);
  4. every current manual check reads `passed`, or is a manual triage target of `contract.triage_targets` (in `manual`,
     `unnamed_manual`, or carrying `unprepared`);
  5. at least one manual target, or one observation, exists.
  Any exception, unreadable controller or unreadable report -> False.
  `failures_to_triage` (13-20): the refusal stands unless `status == "not_executed"` and (`s6_closed_by_code` OR
  `triageable_not_executed(self.task_root, awaiting=<stage_S7's awaiting>)`); `failures_to_triage` gains the keyword
  `awaiting=""`, its one caller (`stage_S7` line 74) passes its own `awaiting`. The reasons it builds are unchanged (the manual
  targets are already worded at 27-35). `check_delivery.run_reasons` 1290: excused when `s6_closed_by_code` OR
  `triageable_not_executed(artifacts)` (no awaiting: at delivery S6 is completed). Comments 14-16 and 87-93 restated (M-g 3):
  "a run that halted (`broken_run`, `timeout`, `env_blocked`), or a `not_executed` with neither an S6 code-only receipt nor a
  target a role can triage (`s7_pretriage.triageable_not_executed`), is never triaged, so no row is written over one".
- Target, 7b (the automated half of a no-report run; on F-15 (a), executable by the recommendation): (1)
  `run_suite.py::build_run_block` writes `reason_code: "report_unread"` (constant `REPORT_UNREAD_CODE` beside
  `PROJECT_TIMEOUT_CODE`, a FIELD, FR-12) on each row with `status == "not_run"` when the summary has `no_junitxml` AND
  `summary["reporter"] == "none"`; (2) `contract.triage_targets` gains set `unread` (one name per such current row, its names
  as for a result row, added to `names`/`all`), and `triage_failures` gives them kind `unread`; (3) the predicate's rule 3
  admits a row carrying that code; (4) the analyst's page `agents/qa-failure-analyst.md` gains one paragraph: for each `unread`
  target, read the run's log (the summary the block's `evidence[].summary` names, its `log_tail`) and write one triage row
  with the existing fields: verdict `NOT_EXECUTED` with `limitation` quoting what the log shows ("the log reads as passed:
  <quote>" or "cannot tell: <why>"), or the failure verdict the log shows (with the fields that verdict already requires); no
  platform word; (5) `ledger.py::test_state`, placed after the `env_blocked` branch (1239-1240) and before `_unknown_run_word`
  (1243): a row carrying the code reads the instance's triage row through `C.triage_row_for` (as the ledger does today):
  a failure verdict -> `failed:<verdict>` (the red road, kinds unchanged); else `not_executed:report_unread` (constant
  `REPORT_UNREAD_STATE`, inside the vocabulary like `HANDED_STATE`); `plan_row_state` applies the same reading where every
  run row of the row's cases carries the code; (6) `check_traceability.py` 86-92: a case whose run rows all carry the code
  reads gap `result:report_unread`; (7) kinds file: kind `run_unread` `{"verdict": "after_checks", "owner": <F-17>}`,
  `ledger_states["not_executed:report_unread"] = "run_unread"`, `trace_gaps["result:report_unread"] = "run_unread"`, and its
  words in the note; the left item's `to_check` says "the run's results could not be read by code; what the analyst read in the
  log: <limitation>; to make it count, set run.reporter and run.report_path in qa-factory/config.json"; (8) architecture.md
  axis 3 cell (§6 7b).
  No existing kind fits exactly: `not_executed` is `no`/product (a test nobody ran); `not_executed_code` is a manual check's
  code row (`needs: code_row`, bound to a MANUAL failure, `check_delivery._code_row_ok` 1126-1158); `unprepared_walk` is a
  manual walk read from the ledger's `unprepared_walks`.
- Edges: 7a - halted S6 (status not `not_executed`) -> the first branch refuses before the predicate (unchanged); S6 not
  completed and not awaiting -> False; mixed story, automated half broke (a `not_run`/`partial`/`skipped` row) -> False ->
  S7 refuses, delivery `run_not_deliverable` (Walk 2, honest); manual row with no result and no `unprepared` -> False; a stale
  manual record (the reducer made it `inconclusive`, `finalize_task.py` 557-562) -> a target, the analyst triages (pretriage leaves
  a reducer-made one to the analyst, `s7_pretriage.py:169-170`); reports written before -> same predicate, nothing to migrate
  (it reads only the report and the controller). 7b - a profile WITH a reporter whose report is missing -> no code -> refusal
  and `no` as today; an inferred reporter that read zero tests -> no code (reporter is not `none`) -> as today; blocks written
  before 7b carry no code -> as today (both worlds: the move that creates the field is the next run of the instance); no
  analyst row for an `unread` target -> S7's form check refuses the analyst's handoff by name as for any target, and at
  delivery `triage_gap` (`no`, factory); a stale analyst row (another attempt) -> archived by the reducer's binding as today.
- Invariant: `execution_status` is never rewritten; code never turns a log into `passed` (FR-58); a run that halted, a
  `not_executed` with nothing a role can triage, and a broken automated half are never admitted at S7 nor excused at delivery;
  a profile with a reporter is never read as "unread".
- Error direction (`s6_closed_by_code`'s twin reused as a gate on two readers): toward False (S7 refuses, delivery `no`), never
  toward admitting a row that is not a role-triageable target. Adversarial inputs that must stay False: a manual `pass` beside an
  automated `not_run` without the code; a report whose `current_manual_checks` is not a list; a controller that raises; S6
  `running`; a `not_executed` report with zero rows; an `unread` code on a row whose status is `passed` (7b: the code counts only
  on `not_run`).
- Premise measurement before code (PROJECT.md package p.6 (a)): the 7a builder runs `check_delivery.py` (`assess`) on a fixture
  all-manual story whose rows are one `inconclusive` and one `unprepared`, with S6 completed, BEFORE the edit, and attaches the
  kinds list and verdict verbatim; the expected today: `run_not_deliverable` plus the per-case kinds (§3 Walk 1).
- Test (B4): 7a - `scripts/tests/test_s7_pretriage.py` (keep): predicate table, one row per rule 1-5 and each adversarial input;
  `scripts/tests/test_story_run_s7.py` (keep): "inconclusive only -> triaged", "unprepared only -> triaged", "manual target +
  automated not_run -> refused", "no target -> refused", "code-only S6 -> as today"; `scripts/tests/test_check_delivery.py`
  (keep, gate_named; the table at 105-134): "not_executed + predicate -> no `run_not_deliverable`", "mixed broken half -> still
  `run_not_deliverable`". 7b - `test_s7_pretriage.py` rows for the code; `scripts/tests/test_ledger.py` (keep): "unread row, no
  triage row -> `not_executed:report_unread`", "unread row + APP_BUG row -> `failed:APP_BUG`", "declared reporter, report missing
  -> `not_executed:<NO_RUN_RESULT>` unchanged"; `scripts/tests/test_third_verdict.py` (keep): `result:report_unread` ->
  `run_unread` -> `after_checks`, and the kinds row; `test_check_delivery.py`: "reporter none, analyst NOT_EXECUTED rows -> verdict
  `after_checks` with one item per instance"; the `build_run_block` code row in `test_s7_pretriage.py` built from a summary
  fixture (`test_run_suite_reports.py` is quarantine: not edited; `test_traceability.py` is quarantine: not edited).

**r5 - `scripts/probe_by_code.py::_no_entry` (1455-1465)** - as r1 §2 r5 (text order only; after RD1-24; F-8 = (a)). Test row
in `scripts/tests/test_probe_by_code.py` (keep, test-layers.json:3690).

**r8 - missing launcher: three roads, one road (B3, B5, B6, F-2 = (a))** - stream 5a
- Now (read): road 1 `gate_preflight.py::Rehearsal.check_s5_executor` (2815-2875): launcher `missing` -> `PERSON_DECIDES`
  card `executor_question` (540-552) with three answers. Road 2 `check_s5_toolchain` `not_started` (2966-2977): the same card.
  Road 3 `run_suite.py::refuse_missing_executor` (1556-1578): prints `executor_unavailable` with the same question, exit 3. No
  driver code reads `executor_unavailable` (D-15: Grep over the package excluding tests finds only `skills/qa-story/phases/
  s5.md:144`, `references/halts.md:28`, `run_suite.py:1572` and changelogs); the automator runs `run_suite.py`, and s5.md:144 tells
  it to "stop, quote its `question` verbatim, record the answer the way s4.md does" - a door to a person past the role (M-b).
- The usable row (B3): `install_dependencies` (`conductor-actions.json:34`): runs the `command` of the `s5_dependencies` note
  once, then requires `dependency_drift.py ... --json` to print `in_sync`; never an install command the note did not name.
  Its source: `check_s5_dependencies` (2877-2903) keeps `self._drift` (entries `differs`/`missing_only` with `command`,
  `profiles`) and `self._drift_all` (every entry, `unknown` included, 2898). No other row settles a missing binary (a machine tool
  is the person's remainder).
- Target, one road for all three: a missing launcher of profile P gets ONE conductor turn exactly when an install command for
  P is known (a `_drift` entry whose `profiles` holds P and whose `command` is non-empty) and no turn was had for the key
  `(P, tool, command digest)`; otherwise the three-answer card as today, words unchanged.
  - Road 1 and 2 (gate): emit `factory_fixable` (check `s5_executor`, fields `profile`, `tool`, `cases`, `install_digest`,
    `fix`) INSTEAD of the card while the condition holds; the card otherwise. The `fix` text (M-a) is the
    `install_dependencies` row's `says` plus: "this turn came from the gate rehearsal: run the row, then end the turn without
    asking the person - if the launcher is still missing, the next rehearsal asks the person the one question". The action row
    itself is not edited (its other context, the S5 dependency note, keeps the person's offer).
  - Road 3 (mid-S5): the JSON gains `"install": <the same command or null>` from the same helper; `references/halts.md:28`
    "Read first" adds: "when its `install` names a command, the `install_dependencies` action once, then `retry`" (first cell
    unchanged: map `test_silent_passes.py:879`; 18 rows and the marker unchanged: `test_conductor_investigates_first.py`).
    `skills/qa-story/phases/s5.md:144` sentence becomes: "If `run_suite.py` answers `{"status": "executor_unavailable", ...}`
    (exit 3, nothing launched): stop the window and end your turn quoting that JSON verbatim, `install` included; do not ask the
    person and never hand cases over yourself - the factory hands it on (an install it knows first, then the person's one
    question)."
  - One helper `gate_preflight.executor_install(root, task_root, profile_id) -> (command dict | None, digest)` reads
    `dependency_drift.check_profiles` (AR-13) and returns `(None, digest)` when `executor_turn_had(task_root, key)` holds (M-b:
    one call per key on all three roads; a gate-A turn then a mid-S5 `executor_unavailable` pays no second install), imported by
    `run_suite.refuse_missing_executor` as it imports `executor_question` today (1565); `run_suite` passes the task root of its
    `--task`.
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
- Road 3 proof before the edit (D-15): the 5a builder adds, first, one driver-rig row "an automator stop quoting
  `executor_unavailable` reaches the conductor (`handle_refusal`, halts.md:28) before any Person" in `test_gate_preflight.py`;
  if the rig shows a Person first, the stream stops and returns the evidence (the road is then a fork for the Lead).
- F-14 (b) (M-d), item 9: `check_s5_dependencies` keeps `self._drift_all`; when a card or note is built for profile P (the
  executor card, the toolchain card, the drift note) and an entry with state `unknown` covers P, ONE clause joins it: "the
  packages installed for this profile could not be read: <the entry's own reason>". Edge: no card and no note of P -> nothing is
  said (no note of its own); an `unknown` entry with no reason -> "it could not be read"; two unknown entries for P -> one clause.
- Edges: no automate rows -> nothing (unchanged, 2841-2851); `skip_executor` -> off; a handed profile -> not asked; record
  absent -> no turn yet (both worlds: the first `close_executor_bound` creates it); record unreadable -> read as "turn had"
  (card, no second paid call: FR-59); record write fails -> printed, remembered in `self.state["executor_handed"]`, the finding
  goes to the top of the gate (as `adapt_handed`); a road with no driver -> `stage_done` refuses S4 over the fixable finding
  with its `[fix: ...]` and the existing person's-word door `--block "gate rehearsal"` (the same as `s5_reporter` today);
  the conductor's install fails -> it ends its turn without asking (the `fix` text) and the next rehearsal gives the card:
  ONE person contact per missing launcher (FR-7, axis 5 "one question for every stop").
- Invariant: nothing is installed but the command the project names (row text); `handed_to_person` is never chosen by code;
  one conductor call per key, on every road.
- Error direction: toward the card (a question too many), never toward assuming a launcher exists; never a second paid call.
- Test: rows in `scripts/tests/test_gate_preflight.py` (keep; its covers hold `driver_gates.py`, test-layers.json:1960):
  "missing + install known + no turn -> factory_fixable s5_executor"; "missing + no install -> card, words unchanged";
  "missing + turn recorded -> card"; "record unreadable -> card"; "toolchain not_started -> same decision"; "zero automate
  rows -> toolchain collect not run, no card" (§3 item iii); "the fixable finding's `fix` carries the end-without-asking clause";
  a driver-rig row "fixable s5_executor -> one conductor call, record written, next rehearsal card, conductor calls = 1, person
  contacts = 1"; "unknown dependency entry of P + P's card -> one clause; no card of P -> nothing" (F-14). Road 3: rows in
  `test_gate_preflight.py` calling `run_suite.refuse_missing_executor`: "JSON carries `install`", "turn recorded -> `install`
  null"; the D-15 rig row.

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
- Streams that do NOT depend on F-5: 1, 2, 3, 4a, 5a, 5b, 6, 7a, 7b (stream 6 runs on F-5(a), the status quo).

### Class C - unproven doors

**r11 - `scripts/driver_stage_s5.py::stage_S5` (226-231) + `scripts/controller.py` op `code_only` (6090-6116) + `stage_scope` (4229-4285) + `acceptance.py::run_witness_excused` (631-649)** - stream 5b
- Now (read): `if not scope.get("scope"): raise Refusal("S5: stage-scope returned no automate cases: ...")`; `code_only` refuses
  any stage outside {S0, S6, S7, S8} (6097-6098; pin `test_controller_state.py:1145`, per the critic's read). NE25 says S5
  closes. Axis 5 row "Code-only stage closes" (C3-2, 5378bbef) kept S5 refused; B-006 is the class carrier (§3).
  `stage_scope` returns `derived: True` as soon as ANY row has a disposition (4252-4256); rows with no disposition fall into no
  group (`_cases_by_disposition` 4223-4227) and the result names `unmapped_scope` (4274-4275) but no undisposed cases (M-e).
  `run_witness_excused(manifest)` (631-649) takes the manifest alone and returns `""` for `{"tests": [], "unresolved": []}`; its
  three readers then demand `run_witness`: `check_witness.RULES["automation-manifest.json"]` (228-235, via `_excused` 88-94),
  `validate_artifacts` (`PHASE_JSON_KEYS` 105; the excuse at 1731-1737), and `handoff_check._run_witness` (139-154, which reads
  only `== "pending"`); `check_delivery.witness_reasons` (711-724) turns the check_witness refusal into kind `factory_record`
  (`no`, factory) (N3).
- Target: a DERIVED empty automate scope - `scope["derived"] is True`, `scope["scope"] == []`, `scope["unmapped_scope"] == []`,
  `scope["undisposed"] == []` - placed right after `stage_scope` and before `s5_todo`: (1) if `work/automation-manifest.json` is
  ABSENT, the driver runs `manifest_put.py --task <T> --fragment '{"tests": [], "unresolved": []}'` once (AR-14: the one
  writer); (2) `self.close_by_code("S5", "nothing to automate: the approved plan names no automate case",
  ["work/automation-manifest.json", "work/test-plan.json"], finalize=False, site="s5.nothing", digest="nothing to automate")`.
  `driver_core.py::CODE_CLOSE_SITES` gains `"s5.nothing": ("S5", "there was nothing to automate")`. `stage_scope` gains key
  `undisposed`: the approved cases whose plan row's disposition is empty (`dispositions.get(row)` falsy), sorted, on the derived
  branch only (the two underived returns keep their keys). `code_only` accepts S5 only when the controller's own
  `stage_scope("S5")` meets the same four conditions (xref, never the request's word); the refusal text for every other stage
  keeps its meaning and names S5's condition. A scope that fails any condition keeps a Refusal reworded to FR-1 with a door
  ("the plan's dispositions could not be read: <reason>" / "cases <ids> have no plan row" / "plan rows of <ids> have no
  disposition"; "rework S3 or record dispositions, then S5 runs again").
  `acceptance.run_witness_excused(manifest, task_root=None)` gains outcome `"nothing"`, returned only when `task_root` is given,
  `manifest["tests"] == []` and `manifest.get("unresolved", []) == []` (exactly empty lists; a missing `tests` key is not empty),
  and the controller of `task_root` holds `stages.S5` with `status == "completed"` and `code_only is True` (read as
  `s7_pretriage.s6_closed_by_code` reads S6; anything unreadable -> `""`). The existing `handed`/`pending` outcomes are
  unchanged and are checked first. Readers: `check_witness` excuses `"nothing"` like `"handed"` (no `run_witness`, no collect
  owed) and passes the task root derived from the manifest path (its grandparent when the parent folder is `work`, else None ->
  no excuse); `validate_artifacts.check_phase_json` passes the same derivation from `path` (its truthiness test at 1736 then
  excuses `"nothing"` with no further change); `handoff_check._run_witness` unchanged (no handoff exists for a stage no role ran;
  its `== "pending"` test is untouched).
- Temporal (both worlds): the receipt exists before any validator reads the manifest at the close: `close_by_code` writes the
  `code_only` receipt (`driver_stage_s7.py:782`) BEFORE `record_close` -> `stage_done` (784-785), and the controller sets
  `{"status": "completed", "code_only": True}` (`controller.py:1950`). Before 5b no S5 receipt can exist (code_only refused S5),
  so every existing manifest reads as today. The builder runs `stage_done` S5 on a fixture story with the empty manifest and
  the receipt BEFORE claiming done (output in the report); a refusal there stops the stream with the evidence.
- Writer check (B2, AR-23), by reading `manifest_put.py` main path 2486-2706: the only refusal of an empty-content fragment is
  2498-2501 ("carries no manifest keys at all"), which a fragment with `tests` avoids; every later check iterates the
  fragment's lists; the commit (2651) then prints "cases now in the manifest: none" (2671) and returns 0. The builder confirms
  it with one run on a fixture story in its worktree BEFORE the edit (output in the report); if it refuses, the stream stops and
  returns the evidence (the one-writer road is then impossible: a fork to the Lead).
- Edges: manifest present (an earlier S5 wrote rows, the plan was reworked to all-manual) -> nothing is written; the close cites
  it (S6 takes its automation scope from the plan, not the file); its rows are not empty, so no witness excuse applies and its
  own witness rule stands; `manifest_put` exits `EXIT_COMMITTED_STALE` -> the driver runs `manifest_put.py --task <T> --recover`
  once and re-checks the file; any other non-zero exit, or still absent -> `Refusal` naming exit code and the door
  `manifest_put.py --task <T> --recover`, WITHOUT quoting the writer's text (its "event committed;" words would match
  `KNOWN_REFUSALS` row `committed_event`, `driver_dispatch.py:55`, whose `recover` does not rebuild the manifest projection,
  47-50); a live S5 dispatch -> `code_close_conflicts` refuses (unchanged); underived, unmapped or undisposed -> refused with
  door. The note at `driver_dispatch.py:47-50` ("the driver does not run manifest_put today") is corrected in the same commit.
  An empty manifest written by an automator (S5 completed by a dispatch, no `code_only`) -> no excuse, `run_witness` owed as
  today. A stale receipt (S3 rework after the close stales S5; a new S5 writes tests) -> `status` is no longer `completed` or
  `tests` is not empty -> no excuse.
- Invariant (positional): no close over a scope nobody could read, nobody mapped or nobody disposed; no close while a dispatch
  of S5 is live; the manifest is written only by `manifest_put.py`; no S5 close leaves the required output absent; an empty
  manifest is excused from `run_witness` only under the controller's S5 code-close receipt.
- Error direction (`run_witness_excused`, a gate excuse, widened): toward `""` (the witness owed, delivery `factory_record` `no`),
  never toward excusing a manifest an automator wrote or one with any row. Adversarial inputs: `{"tests": []}` with no receipt;
  the receipt with `tests: [x]`; the receipt with `unresolved: [x]`; `tests` key missing; `task_root` None; a controller that
  raises; S5 `code_only` True but status not `completed`.
- S5 vs the S7 precondition and bound (M-g 1): S5 does NOT owe S7's precondition (`s7_fresh`) and bound (one re-triage per
  life): no role ran, so there is nothing to re-judge or re-dispatch; its precondition is the derived, mapped, disposed, empty
  scope plus no live S5 dispatch (`code_close_conflicts`).
- Test: rows in `scripts/tests/test_s5_window_leftovers.py` (keep, rig at 692 ff.): "derived empty, no manifest -> manifest_put
  called with the empty fragment, close site s5.nothing"; "derived empty, manifest present -> not called, close"; "manifest_put
  stale -> recover once"; "underived -> Refusal with door"; "undisposed row -> Refusal naming it"; "unmapped case -> Refusal naming
  it"; `scripts/tests/test_controller_state.py` (keep) pin 1145 updated and rows "S5 code_only with a non-empty derived scope ->
  refused", "with an undisposed row -> refused", "`stage_scope` `undisposed` lists the row"; `scripts/tests/test_check_witness.py`
  (keep, scenario): "derived-empty S5 close -> no witness owed (check_witness and phase_errors)", "empty manifest without the
  receipt -> still refused", plus each adversarial input; the existing row 125 ("a manifest with no tests is not all pending")
  stays green; `test_null_outcomes.py` green.

**r12 - `gate_preflight.py::Rehearsal.check_s5_runtime_probe` bound** - no code change; the pin moves (B4) from the quarantined
`test_story_run_gate_repair.py` to a driver-rig row in `scripts/tests/test_gate_preflight.py`: "write exits 0, finding
repeats -> after `GATE_REPAIR_CAP` the list goes to the conductor once, never a third round". Stream 5a.

---------------------------------------------------------------------------------------------------------------------

## 3. All-manual story, S5 -> S8 (B2), and B-006

B-006 (`plans/BACKLOG.md:79`, frozen) items, each walked in code:

| item | today (read) | verdict |
|---|---|---|
| (i) S5 with no automate scope closes normally | refused (`driver_stage_s5.py:230-231`) | IN: r11, stream 5b |
| S6 of an all-manual story | auto scope empty, manual scope non-empty -> `stand_check`, `build_check`, manual lane (`driver_stage_s6.py` 502-518); the manifest exists after 5b; `check_delivery.py:712-714` refuses a MISSING manifest, so 5b's write is load-bearing; its witness is excused only under the S5 receipt (N3) | passes after 5b |
| (ii) S7 reads `not_executed` with nothing to triage | a manual `inconclusive` (`manual_evidence.py:35`) or `unprepared` row with no `fail` makes `execution_status` `not_executed` (`finalize_task.py:629-637`); S7 refuses it after a real S6 (`driver_stage_s7.py:13-20`) | IN: stream 7a |
| (iii) gate A does not ask about toolchain/keys at zero automate rows | executor: asks nothing (2841-2851); toolchain: collects whenever `tests_root` is a folder, and `not_started` raises a card about 0 cases (2971-2977); credentials: asks the default login on `default_login_needed`, "ONE rule with S6" (`gate_preflight.py:4627-4631`) | toolchain IN: stream 5a item 5 (no collect, no question when `automate_rows()` is empty). Keys OUT (M-c): the login is shared with S6 (AR-19) and manual-agent cases need it at zero automate rows; cutting it would move the question to S6 |
| (iv) required outputs per role (bug-reporter vs the scribe's `test-report.md`) | S8 `required_outputs` are the scribe's three files (`stages.json:296-300`), independent of automation | OUT: no automation dependence found in the stage contract; the role-order question is live-run territory (L4 reaches S8; a failure there opens a finding) |
| (v) delivery without automation is a legal outcome | corrected (N2, N3): `witness_reasons` gave `factory_record` for the empty manifest (fixed by 5b); `run_reasons` gave `run_not_deliverable` (fixed by 7a); the per-case kinds then decide (Walk 1 below) | IN: 5b + 7a; the `unprepared` case: F-16 |

Walk 1 - an all-manual story, S6 completed, rows only `inconclusive` / `unprepared`, after 5b and 7a (by reading; the 7a builder
measures it, §2 r4):
- reducer -> `not_executed` (`finalize_task.py:629-637`); S7 -> the predicate holds -> pre-triage writes a code row
  `NOT_EXECUTED` for an `inconclusive` whose record validated and carries the role's limitation (`s7_pretriage._why_not`
  154-181), leaves an `unprepared` walk to the analyst (163-164); S7 closes by code (`s7.pretriaged`) or dispatches the analyst.
- delivery: `witness_reasons` -> none (5b); `run_reasons` -> none (7a);
  - `inconclusive` case: trace gap `result:inconclusive` (`check_traceability.py:92`) -> `not_executed_code` (`after_checks`,
    product) when code's row re-derives (`_code_row_ok` 1126-1158), else `not_executed_unproven` (`no`, factory) - e.g. the
    analyst replaced code's row with its own `NOT_EXECUTED`, or the record carries no limitation of the role's own (kinds 130;
    `test_third_verdict.py:147-148`). Unchanged by U7 (AR-28: a not-execution code cannot re-derive is not proven).
  - `unprepared` case: `unprepared_records` gives `unprepared_walk` (`after_checks`, factory; `check_delivery.py` 1885-1906), but
    the case's own trace gap is `result:none` -> `chain_broken` (`no`, product): `run_results` puts `""` for a manual check with no
    result (`contract.py` 4486-4488), `case_lookup` returns the roll-up `""` (4509-4513, `rollup_status` 4421-4423), and
    `check_traceability.py:92` writes `result:` + (`result or 'none'`); `_lookup` falls to the `result` row (`delivery_verdict.py`
    147-156). So `no` speaks, owner product, beside the `unprepared_walk` item (D-13; the critic's walk named `unprepared_walk`
    as what speaks). The coverage leg (`coverage_reasons`, `coverage_gap` `no`/factory) is not read here: the 7a builder's
    measurement names it. -> F-16.

Walk 2 - a mixed story whose automated half broke (a `not_run` row of a declared reporter, or `partial`): the predicate is False;
S7 refuses as today; delivery `run_not_deliverable` (`no`, factory) - honest.

Sibling axes: SIBLING_MAP axis 5 (stage twins: `s5.nothing` <-> `s6.nothing`; code-only closes; S7 entry <-> delivery
`run_reasons`) and axis 38 (the dry census: `s5.nothing` is a new code-close site; `dry_exits.py --check` decides whether it is a
subject and the row lands in `scripts/tests/fixtures/driver-exits/s5.json` in the same commit).

---------------------------------------------------------------------------------------------------------------------

## 4. Refusals, doors, text

Every reworded or new text obeys FR-1, FR-2, FR-57; person-facing words obey `references/human-questions.md` (checked by
`human_text.problems` where the site already checks). Nothing removes a door a role holds; every seam turn keeps the site's
question as fallback. Notes inform and pass nothing (FR-4).

---------------------------------------------------------------------------------------------------------------------

## 5. Overlaps with open batches (t-1238) and order

| stream | neighbours | order |
|---|---|---|
| 1 surfaces, readiness r3, `_row_of_nobody`, architecture.md cells 2/7 | readiness-set (other functions); OF5-1 (`planning_contract.py`, another function) | items 1-3, 5 free; item 4 after stream 7a merges |
| 2 p1/p2 | OH3-35 (in work), XT2-1, TQ1-6 | after OH3-35, or late node merges main |
| 3 r9 pin | none (test only) | free |
| 4a r5 | RD1-24, PC4-2 | strictly after RD1-24 |
| 5a gate A | RD1-13 -> RD1-14 (same file queue: `gate_preflight.py`, `run_suite.py`), EP1-26, CX2-15, PC4-4; 7b (`run_suite.py`, another function) | after RD1-13/RD1-14; before PC4-4 (owner-blocked) |
| 5b S5 close | PC4-5 (controller cut), conductor/3 C3-24 | free; if PC4-5 lands first, edit the part holding `code_only`/`stage_scope` |
| 6 stand_check + OF5-5 | OF5-5, DH2-1, FV3-21 (in work), FV2-38; 7a (`check_delivery.py`: 6 owns `stand_word`, 7a owns `run_reasons` - disjoint functions) | one node with OF5-5 (F-9 = (a)); after FV3-21; OF5-5 owns cell corrected first (D-5); the later of 6 and 7a merges main into its tree before its own merge (PROJECT.md "Командная работа" item 3) |
| 7a S7 entry + delivery twin | 6 (`check_delivery.py`, above) | before stream 1 item 4 and 7b |
| 7b no-report half | 7a (same predicate, `test_s7_pretriage.py`, `test_check_delivery.py`), 5a (`run_suite.py`: 5a `refuse_missing_executor`, 7b `build_run_block`) | after 7a merges and the Lead's F-15/F-17 word; after 5a when both are open (same file) |
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
  `_row_of_nobody` converts (after stream 7a) - test_question_branches rows; (5) r3 split and note - test_readiness rows; (6)
  `design/architecture.md` section A map cells (M-g 2), in the commit of the items that make them true:
  - axis 2 "Held by today", with items 1-3: replace "an undeclared surface takes the web road silently" with "a config that
    declares no surface is said out loud (`surfaces.undeclared`)"; with item 4: replace "cases of any other surface go to a
    person" with "a case of any other surface is tried by the agent first and recorded `unprepared` with what it tried; the
    person gets what the role could not do".
  - axis 7 "Held by today", with item 5: replace "a row with no URL passes S0 as in-process, silently" with "a row with no URL
    passes S0 as in-process, and readiness says it took that default".
- commit: `architecture: AR-2, AR-1, AR-28 -- ...`; `judgment:` naming the units of 1.2.
```
given: C:/QAFactory/forge-repo/docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r3.md (sections 1, 2 r2/r3/a2D1, 4, 6 stream 1), C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md, C:/QAFactory/forge-repo/docs/TESTING.md
owns: C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/surfaces.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/surfaces.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/readiness.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/planning_contract.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_readiness.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_question_branches.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/design/architecture.md (section A map cells of axes 2 and 7 only)
non-goals: Android/iOS rows, drivers, AGENT_HANDS as data (U8); quarantined test files (test_surfaces.py, test_mobile_road.py); the doctor skill text; readiness remedy.steps (OF5-9); any other line of architecture.md
handoff: builder report with the witness; the list of quarantined assertions the change contradicts
edges: spec 2 r2 (profiles absent -> undeclared; unreadable table -> surfaces.unknown; web+api -> no key, 0 table reads), r3 (declared byte-identical; URL-less note; mixed), a2D1 (broken table / unknown profile / mixed hands -> old road)
DoD: rows of spec 2 r2, r3, a2D1 green in keep files; pins test_readiness.py:873-874,917 green; `python -B tools/architecture_index.py --check` green; `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>`
siblings: planning_contract._row_of_nobody (included); driver_stage_s6._cases_all_on_driver (reads is_device_row only: n/a)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r3.md
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

**Stream 5a - gate A (r8 three roads, B6, Q12, r12 pin, B-006 iii toolchain, F-14 b)**
- items: (1) `executor_install` helper (turn-bound, M-b) + decision in `check_s5_executor`; (2) the same in `check_s5_toolchain`
  `not_started`; (3) `run` tuple order; (4) driver side: `close_executor_bound`, `unturned_executors`, `hand_to_conductor` finally,
  series re-hand, `CHECK_WORDS`; (5) toolchain returns with no question at zero automate rows (`check_s5_credentials` UNCHANGED,
  M-c); (6) Q12 notes; (7) road 3 `install` field + halts.md row + s5.md:144 sentence, after the D-15 rig row; (8) r12 pin; (9)
  F-14 (b) clause; (10) the `fix` text's end-without-asking clause (M-a); (11) the `driver-exits/gates.json` row if
  `dry_exits.py --check` names the new road (M-h). Each item: its row in §2.
- commit: `architecture: AR-17, AR-25, AR-28, AR-14 -- ...`; `judgment:` naming check_s5_executor, check_s5_toolchain,
  check_s5_dependencies.
```
given: C:/QAFactory/forge-repo/docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r3.md (sections 1, 2 r8/Q12/r12, 3 item iii, 4, 6 stream 5a), C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md, C:/QAFactory/forge-repo/docs/TESTING.md
owns: C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_preflight.py (check_s5_executor, check_s5_toolchain, check_s5_dependencies, executor_install, executor_turn_had, run, and the cards/notes F-14 joins)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_gates.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/run_suite.py (refuse_missing_executor only)
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/halts.md (row `run_suite: executor_unavailable` only)
C:/QAFactory/forge-repo/ai-packages/qa-factory/skills/qa-story/phases/s5.md (the sentence at line 144 only)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_preflight.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/driver-layers.json (the two new DriverGates members)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/driver-exits/gates.json (if dry_exits names the road)
non-goals: check_s5_stand_limits (RD1-13), provenance (RD1-14), the Rehearsal cut (PC4-4), collect_base one-road (U8), check_s5_credentials (M-c), conductor-actions.json, run_suite.build_run_block (7b)
handoff: builder report with the witness, the D-15 rig output, and the FR walk
edges: spec 2 r8 (record absent/unreadable/write fails; no-driver road; install fails -> end without asking, one person contact; handed; zero automate; turn had -> no install on road 3; F-14 no card -> nothing), Q12
DoD: rows of spec 2 r8, Q12, r12 green; conductor calls 0 when no install known; person contacts 1 per missing launcher; `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>`; `dry_exits.py --check` 0 discrepancies
siblings: the three roads (all here); halts.md map (test_silent_passes.py:879, first cell unchanged); s5.md:144 role door (here)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r3.md
```

**Stream 5b - S5 close (r11, B2, N3, M-e)**
- items: (1) `stage_scope` key `undisposed`; (2) `code_only` S5 condition; (3) `stage_S5` branch + manifest write + close;
  (4) `CODE_CLOSE_SITES` row; (5) `run_witness_excused` outcome `nothing` and the two call sites passing the task root; (6) the
  `driver_dispatch.py` 47-50 note; (7) the `driver-exits/s5.json` row; (8) the writer-check and `stage_done` premise runs.
- commit: `architecture: AR-22, AR-23, AR-28, AR-14, AR-19 -- ...`; `judgment:` naming `run_witness_excused`, `code_only`.
- The Lead, in the commit that merges 5b (M-g 1), replaces in `docs/SIBLING_MAP.md` axis 5 row "Code-only stage closes" the
  clause "and S5 (conductor/3 C3-2, owes the same precondition and bound; the controller refuses `code_only` S5 today)" with:
  "and S5 (`s5.nothing`, U7 5b: the controller accepts `code_only` S5 only over its own derived S5 scope that is empty and has no
  unmapped and no undisposed case; S5 owes no repair-loop bound and not S7's freshness precondition - no role ran - and a manifest
  it wrote empty owes no `run_witness` only under that receipt, `acceptance.run_witness_excused`)".
```
given: C:/QAFactory/forge-repo/docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r3.md (sections 1, 2 r11, 3, 4, 6 stream 5b, 8), C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md, C:/QAFactory/forge-repo/docs/TESTING.md
owns: C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_stage_s5.py (stage_S5)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/controller.py (op code_only validation; stage_scope key undisposed)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_core.py (CODE_CLOSE_SITES row only)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_dispatch.py (the comment at 47-50 only)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/acceptance.py (run_witness_excused only)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/check_witness.py (_excused and the automation-manifest rule only)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/validate_artifacts.py (the excuse call at 1731-1737 only)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_s5_window_leftovers.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_controller_state.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_check_witness.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/driver-exits/s5.json (if dry_exits names s5.nothing)
C:/QAFactory/forge-repo/ai-packages/qa-factory/design/controller-blocks.md (if the generator re-renders it)
non-goals: S6's s6.nothing; window logic; null-outcomes rows; manifest_put.py itself; handoff_check.py; check_delivery.py; docs/SIBLING_MAP.md (the Lead's edit at merge)
handoff: builder report with the witness, the writer-check run and the stage_done premise run verbatim
edges: spec 2 r11 (derived/underived/unmapped/undisposed; manifest present/absent; stale -> recover once; other exit -> Refusal without the writer's text; live dispatch; excuse: no receipt, rows present, tests key missing, task_root None, controller raises, stale receipt)
DoD: the writer-check and stage_done runs in the report; rows green; pin 1145 updated; test_check_witness.py row 125 green; `test_null_outcomes.py` green; `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>`; `dry_exits.py --check` 0 discrepancies
siblings: S6 twin s6.nothing (unchanged, AR-19); B-006 items (section 3); the manifest and run_witness readers (section 13 D5)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r3.md
```

**Stream 6 - stand question (r10 with OF5-5)** - after FV3-21; OF5-5 owns cell corrected first
```
owns: C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_stage_build.py (stand_check)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/waiver.py, check_delivery.py (stand_word), driver_stage_s6.py (s6_no_stand) -- OF5-5's part
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_story_run_s6.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_human_questions.py
non-goals: the stand question's words and prices (DH2-1, FV2-38); manual_lane_plan (FV3-21); E-7; a new Driver member; check_delivery.run_reasons (7a)
edges: spec 2 r10 (no stand; word given; one turn per entry; not authorized -> no call)
DoD: OF5-5 step 1 result attached; rows green; NO_MOVE_BASELINE unchanged or lower; `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>`
siblings: build_check (no person-first door of this class: questions come from the probe record): n/a
```

**Stream 7a - S7 entry and its delivery twin over a manual-only `not_executed` (N2, F-12 as widened, B-006 ii)**
- items: (1) `s7_pretriage.triageable_not_executed` (rules 1-5, §2 r4); (2) `failures_to_triage` reads it (keyword `awaiting`),
  `stage_S7` passes its `awaiting`; comments 14-16 and 87-93 restated; (3) `check_delivery.run_reasons` reads it; (4) the
  premise measurement (Walk 1) before the edit.
- commit: `architecture: AR-13, AR-19, AR-27, AR-28 -- ...`; `judgment:` naming `triageable_not_executed`, `run_reasons`.
```
given: C:/QAFactory/forge-repo/docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r3.md (sections 1, 2 r4, 3, 4, 6 stream 7a), C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md, C:/QAFactory/forge-repo/docs/TESTING.md
owns: C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/s7_pretriage.py (triageable_not_executed only)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_stage_s7.py (failures_to_triage, its call in stage_S7, the comments at 14-16 and 87-93)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/check_delivery.py (run_reasons only)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_s7_pretriage.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_story_run_s7.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_check_delivery.py
non-goals: finalize_task.py execution_status; contract.triage_targets; the unread/no-report half (7b); check_traceability.py; delivery-verdict-kinds.json; stand_word (stream 6)
handoff: builder report with the witness and the Walk 1 measurement verbatim (before and after)
edges: spec 2 r4 7a edges (halted S6; S6 not finished; mixed broken half; manual row with no result; stale manual record; reports before)
DoD: rows of spec 2 r4 (7a) green; `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>`
siblings: B-006 (ii); s6_closed_by_code readers (both read the predicate now); stream 1 item 4 and 7b depend on it
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r3.md
```

**Stream 7b - the no-report half (r4, F-15 (a), F-17)** - after 7a, the Lead's F-15/F-17 word, and 5a when both are open
- items (§2 r4 7b): (1) `build_run_block` code; (2) `triage_targets` `unread` + `triage_failures` kind; (3) predicate rule 3;
  (4) analyst page paragraph; (5) ledger `test_state` / `plan_row_state`; (6) `check_traceability` gap; (7) kinds rows and words;
  (8) `design/architecture.md` axis 3 cell: replace "reporter `none` records a green run as not executed, silently" with
  "reporter `none` records a run as not executed and says so; its tests are the failure analyst's triage targets and reach
  delivery as items left with the person, or as the analyst's red"; (9) before code: the walk of every reader of
  `contract.triage_targets` / `triage_failures` (finalize_task refresh, driver_stage_s7, s7_pretriage.decide, handoff_check,
  check_delivery `_triage_failures`/`_code_row_ok`/triage_reasons, ledger, traceability, dashboard) with a verdict each in the
  report; and one check that the analyst's form accepts a `NOT_EXECUTED` row on a non-manual target - a refusal stops the stream.
- commit: `architecture: AR-1, AR-22, AR-27, AR-28 -- ...`; `judgment:` naming the units of 1.2's 7b row.
```
given: C:/QAFactory/forge-repo/docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r3.md (sections 1, 2 r4, 3, 4, 6 stream 7b, 11 F-15/F-17), C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md, C:/QAFactory/forge-repo/docs/TESTING.md
owns: C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/run_suite.py (build_run_block and the constant only)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/contract.py (triage_targets, triage_failures only)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/s7_pretriage.py (triageable_not_executed only)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/ledger.py (test_state, plan_row_state, the state constant)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/check_traceability.py (the run-result gap branch only)
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/delivery-verdict-kinds.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/agents/qa-failure-analyst.md (one paragraph)
C:/QAFactory/forge-repo/ai-packages/qa-factory/design/architecture.md (section A map cell of axis 3 only)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_s7_pretriage.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_ledger.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_third_verdict.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_check_delivery.py
non-goals: execution_status; manual_evidence.py; coverage_contract.py; the reducer; run_suite.refuse_missing_executor (5a); quarantined test_traceability.py and test_run_suite_reports.py; any platform word (P2)
handoff: builder report with the witness, the reader walk and the form check verbatim
edges: spec 2 r4 7b edges (reporter declared, report missing; inferred format; blocks before; no analyst row; stale analyst row; code on a passed row)
DoD: rows of spec 2 r4 (7b) green; `python -B tools/architecture_index.py --check` green; `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>`
siblings: the three producers of the no-report `no` (run_reasons via 7a, ledger, traceability: all here); judge_run (moves a summary only to env_blocked: n/a)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r3.md
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
S7 triages it (a2D1, r2, stream 7a); the delivery verdict and its kinds are recorded (F-16 decides which). L3 an unconfirmed
stand with an authorized remedy gets one conductor turn; a missing launcher with a known install command gets one; the person's
question only after, once (r8, r10). L4 an all-manual plan passes S5 by code (empty manifest, no witness owed under the S5
receipt) AND S6, S7, S8 through to a delivery verdict whose kinds name no `factory_record` and no `run_not_deliverable` (5b, 7a,
§3). L5 S0 with a URL-less row says the default (r3). L6 a `reporter: none` run: the analyst triages each instance from the log
at S7; delivery says `after_checks` with one `run_unread` item per instance, or the analyst's red (7b). E-7's row waits on F-5.

---------------------------------------------------------------------------------------------------------------------

## 8. Readers of every touched file (designer rule 7; Q13(d))

The `owns_readers.py` block was not attached to this dispatch; the critic ran it twice (r1: "readers: 724 outside owns ... base
b4eb74df"; r2's new paths: "readers: 598 outside owns, 10 lines below -- base origin/main 44585bce"). The Lead re-runs it over the
streams' owns of r3 (DoD of t-1258). r1's lines, answered:
- `config-keys.json` names declared_surfaces, _check_plain_environment, check_s5_executor: no function renamed, no config key
  added or removed -> unchanged (stream 1/5a builders confirm the rows name functions, not values).
- `gate-registry.json`, `block-names.json` name stand_check: name and block words unchanged -> unchanged.
- `driver-layers.json`: s0_rest, stage_S5, stand_check homes unchanged; two new DriverGates members -> changes in stream 5a
  (sole writer of the fixture in U7; stream 6 adds no member).
- `judgment-census.json`: rows 415/1118 unchanged; no row added (§1.2).
- `null-outcomes.json` names stage_S5 (NE3/NE4/NE25): guard name unchanged; NE25 becomes true -> unchanged.
- `test_silent_passes.py` (s0_rest, stand_check, halts map): members exist, first cells unchanged -> unchanged.
- `test_conductor_investigates_first.py` (halts.md 18 rows, markers): row count and marker unchanged -> unchanged.
- quarantined readers `test_surfaces.py`, `test_mobile_road.py`, `test_story_run_gate_repair.py`, `test_traceability.py`,
  `test_run_suite_reports.py`: not run by the canon; not edited; contradicted assertions listed in stream reports.
- `references/surfaces.json`: one reader `surfaces.py` -> changes in stream 1.
- `manifest_put.py` gains a caller (driver): `driver_dispatch.py:47-50` note -> changes in stream 5b.
- `state/executor-turns.json` (new): writer DriverGates.close_executor_bound, reader gate_preflight.executor_turn_had (now also
  through `executor_install`, read by run_suite) -> stream 5a.
- `stand_check` callers (`driver_machine.py:1508,1618`, `driver_stage_s6.py:517`, `driver_stage_s5.py:201,330`, rigs):
  signature unchanged.
- controller op `code_only` callers (`driver_dispatch.py::code_only`, `driver_stage_s7.py::close_by_code`): unchanged; S5 legal
  only under the derived-empty condition.

M-f, the 10 `more` lines of the r2 run, plus the two files N2/N3 add:
- `manual_evidence.py`: not touched by r3 (4b removed) -> unchanged.
- `skills/qa-story/phases/s6.md`: not touched by r3 (4b removed) -> unchanged.
- `driver_stage_s7.py`: interface kept: `failures_to_triage` returns the same `str`; the new keyword `awaiting=""` defaults to
  today's reading; its one caller is `stage_S7` in the same file (Grep `failures_to_triage(` over scripts: the definition at 10,
  the call at 74, test rigs) -> changes in stream 7a.
- `driver_core.py`: interface kept: `CODE_CLOSE_SITES` stays a dict of `site -> (stage, words)`; one row added; its readers (the
  site check in `close_receipt`, the dry census) read rows by key -> changes in stream 5b (+ `driver-exits/s5.json`).
- `driver_dispatch.py`: comment only -> interface kept (5b).
- `run_suite.py`: interface kept for every reader: `refuse_missing_executor` JSON gains `install` (additive; readers: the
  automator by s5.md:144 and the conductor by halts.md:28, both in 5a); `build_run_block` rows gain an optional
  `reason_code: report_unread` beside the existing optional `reason_code` (`PROJECT_TIMEOUT_CODE`, 556-557), readers named in 7b
  item 9 -> changes in streams 5a and 7b (disjoint functions).
- `references/halts.md`: one row's "Read first" cell; first cell and row count unchanged (pins above) -> 5a.
- `driver_gates.py`: two new members (driver-layers.json, 5a); `hand_to_conductor` signature kept -> 5a.
- `controller.py`: interface kept: `code_only` request shape unchanged (S5 newly legal under a condition); `stage_scope` result
  gains key `undisposed` on the derived branch (additive: readers read named keys) -> 5b.
- `driver_stage_s5.py`: `stage_S5` gains a branch before `s5_todo`; no signature change -> 5b.
- `check_delivery.py`: interface kept: `run_reasons(artifacts) -> list` unchanged; it returns `[]` in one more case; one reader,
  `assess` 2623 -> 7a; `stand_word` -> 6 (disjoint).
- `acceptance.py`: `run_witness_excused(manifest, task_root=None)`: the new parameter defaults to today's behaviour; a new return
  `"nothing"`. Readers (Grep `run_witness_excused` over scripts: 3 production callers + `test_check_witness.py`):
  `check_witness._excused` -> changes in 5b (passes the root, excuses `nothing`); `validate_artifacts` 1736 -> changes in 5b
  (passes the root; truthy test unchanged); `handoff_check._run_witness` 150 -> unchanged (`== "pending"` only; passes no root, so
  `"nothing"` never reaches it).
- New for 7b: `contract.py` (`triage_targets`, `triage_failures`), `ledger.py`, `check_traceability.py`,
  `delivery-verdict-kinds.json`, `agents/qa-failure-analyst.md`: readers are walked by the 7b builder before code (item 9);
  `delivery_verdict.load_kinds` validates every kind's owner word (`DELIVERY_REASON_OWNERS`, `contract.py:2166`) and the test
  that holds the table (`test_third_verdict.py`) -> changes in 7b.
- `design/architecture.md`: read by `tools/architecture_index.py` (generates `docs/ARCHITECTURE_INDEX.md` from the AR lines, not
  the map cells) -> the map cells change in streams 1 (axes 2, 7) and 7b (axis 3), disjoint lines; `--check` in their DoD.
Not covered without the tool block: readers in `tools/`, `.githooks/`, `.claude/` of the touched package files - the Lead
attaches the block at dispatch (KNOWN MISSES of rule 7).

---------------------------------------------------------------------------------------------------------------------

## 9. Rule 10 four questions

Not a forge mechanism: package behaviour, carried by the architecture gate lines and the census. The new value "role" of
`hands`, the new file `state/executor-turns.json`, the S5 receipt excuse, the predicate and (7b) the `report_unread` field and
`run_unread` kind are package contracts with named readers; detectors: the test rows named.

## 10. Flags (code differs from a digest, the brief or the verdict)

D-1..D-6 as r1 §9. D-7 r4's class A is already closed by `run_suite.py::no_report_words`. D-8 (r2) F-4(b)'s stated carrier
refused automate obligations - moot (4b removed). D-9 a manual `inconclusive`/`unprepared` without a `fail` makes `not_executed`.
New in r3:
- D-10 the no-report `parse_gap` is a SUMMARY key (`run_suite.py` 2287, 2293), not a run-block key; the block has
  `evidence[].reporter` (585) and rows `not_run` / "report row missing" (536-540). The same sentence also fires for a declared
  reporter whose report is missing (2248-2293). The Architect's wording "run block carries the no-report parse_gap" is executed as
  `reporter == "none"` plus `no_junitxml` at the producer (7b item 1), which excludes the declared-reporter case (honest `no`).
- D-11 an instance of a no-report run is no triage target (`contract.py:4638-4639`) and the reducer archives an unbound triage row
  (`finalize_task.py:726-743`): the analyst's reading has no carrier today -> F-15.
- D-12 three producers of the delivery `no` for such a test: `run_reasons`, `ledger.test_state` 1245 (kind `not_executed`),
  `check_traceability.py:92` (`result:not_run` -> `chain_broken`).
- D-13 the critic's Walk 1 says the `unprepared_walk` record speaks once `run_not_deliverable` is gone; in code the case's own trace
  gap `result:none` -> `chain_broken` (`no`, product) still speaks (§3 Walk 1) -> F-16.
- D-14 `test-layers.json` is at `scripts/tests/test-layers.json` (keep from 36, quarantine from 7209), not under `fixtures/`;
  `test_traceability.py` (10484) and `test_run_suite_reports.py` (9710) are quarantine.
- D-15 no driver code reads `executor_unavailable` (Grep over the package excluding tests: s5.md:144, halts.md:28,
  run_suite.py:1572, changelogs); the r2 claim "road 3 reaches the conductor through `handle_refusal`" is unproved in code ->
  the 5a rig row before the edit.
- D-16 architecture.md:72 requires the axis line edited in the same commit as the change that alters it: 7b alters axis 3, so 7b
  owns that cell (the Architect's M-g decision named axes 2 and 7, the only ones r2 changed).
- D-17 `run_witness_excused` takes no task root (631) and its check_witness caller passes the manifest dict only (88-94): the
  receipt-bound outcome needs a new optional parameter and two call sites.

## 11. Forks

Carried (Lead and Architect, 17.11.2026): F-1 (a); F-2 (a); F-3 (a) - premise measured, holds as `unprepared`; F-6 (a); F-7 split
(now: 1, 2, 3, 4a, 5a, 5b, 6, 7a, 7b, plus E7); F-8 (a); F-9 (a); F-10 (a); F-11 (a); F-12 (a) as widened by N1; F-14 (b) (executor:
5a item 9); Q-U8 a node of U8. Withdrawn: F-13 (a)-(c), node 4b. OPEN, the owner's: F-5.

New, returned:
- F-15 the carrier of the analyst's reading of a no-report instance (D-11). (a) the instance becomes a triage target:
  `run_suite.build_run_block` writes `reason_code: report_unread` (reporter `none`, no report), `contract.triage_targets` gains
  `unread`, the analyst answers each with an existing triage row (`NOT_EXECUTED` + `limitation` = its reading, or a failure
  verdict), the reducer keeps the bound row, the ledger and the trace read it, delivery says `run_unread` (`after_checks`) or red
  (stream 7b as written); (b) no analyst reading: the predicate admits a row with the code at S7 (the analyst triages only the
  manual targets) and delivery lists one `run_unread` item per instance with "set run.reporter", the person reads the log;
  (c) the automated half stays out of U7: reporter `none` keeps today's S7 refusal (7a ships alone). Recommend (a): it is the
  decision's road (the role judges, P27; a red found in the log travels as a red); cost: the one definition of "a target" changes,
  with every reader walked (7b item 9), and one producer field. (b) costs less but leaves the reading to the person; (c) leaves
  axis 3 stuck.
- F-16 what the delivery says for a case whose current manual check is an unprepared walk (D-13). (a) `check_traceability.py`
  reads such a case's gap as `unresolved:unprepared_walk` (a trace_gaps row -> kind `unprepared_walk`, `after_checks`), so the
  walk's own item speaks; the coverage leg is measured first (7a's Walk 1 measurement) and, if `coverage_gap` also fires, the
  node returns; (b) keep `chain_broken` `no` (owner product) beside the `unprepared_walk` item, as Fork 13 A reads ("the walk never
  proves a requirement; the requirement keeps its own kind", `check_delivery.py:1889-1890`). Recommend (a): the owner's U7 goal is
  "the person gets only the remainder" and `after_checks` claims no proof (P21's third outcome); it re-reads Fork 13 A, so it is
  the Lead's or the owner's word, and it would be a 7c node (`check_traceability.py`, `delivery-verdict-kinds.json`,
  `test_third_verdict.py`) after 7b (same files).
- F-17 the owner word of kind `run_unread`: (a) `factory` (the factory's reader could not read the run; the twin of
  `unprepared_walk`, `sides_unknown`); (b) `environment` (the project's config lacks a reporter); (c) `product`. Recommend (a).

## 12. Small choices closed by the designer

- r3 moved to stream 1 (one owner of `test_readiness.py`).
- The turn record path `<task root>/state/executor-turns.json`, `{"turns": [{"key", "at"}]}`; key `profile|tool|digest`.
- `check_s5_dependencies` moved before `check_s5_executor` in `run` (the only order change).
- r12's pin and every gate row in `test_gate_preflight.py`.
- r10's turn kept in `self.state["stand_turned"][stage]`; no new Driver member.
- Example texts are drafts; final words are the builder's under `human-questions.md`.
- M-a's instruction lives in the `s5_executor` finding's `fix` text (5a), not in the action row (the row's S5-note context keeps
  the person's offer; one stream, one file).
- `executor_install` takes the task root; `run_suite` passes its `--task` root.
- The predicate's name `triageable_not_executed`, its `awaiting` keyword, and its home `s7_pretriage.py` beside
  `s6_closed_by_code`.
- `stage_scope`'s new key `undisposed` (derived branch only); the excuse word `nothing`; the task root of check_witness and
  validate_artifacts derived from the manifest path's `work/` parent.
- 7b's names `REPORT_UNREAD_CODE` = `report_unread`, `REPORT_UNREAD_STATE` = `not_executed:report_unread`, gap
  `result:report_unread`, kind `run_unread`.
- Stream 7 split into 7a (dispatchable) and 7b (on F-15); the axis 3 map cell joins 7b (D-16).

## 13. Reading trail

r3 reads (17.11.2026, base the snapshot of this session; line ranges as read):
spec r2 (whole); verdict t-1252 (whole); the brief (whole); `driver_stage_s7.py` 1-140, Grep `def close_by_code` (763-803);
`s7_pretriage.py` (whole, 1-385); `contract.py` 2186-2215, 4411-4440, 4449-4530, 4590-4699, 5055-5094, Grep `TRIAGE_VERDICTS|
EXECUTION_STATUS|RUN_WORDS_KNOWN` (2153-2159, 2180, 4394), Grep `DELIVERY_REASON_OWNERS` (2166); `finalize_task.py` 38-63,
340-474, 525-674, 715-757; `run_suite.py` 290-399, 470-627, 1350-1381, 2240-2320, Grep `parse_gap` (scripts), Grep
`resolve_reporter|reporter_choice` ; `check_delivery.py` 103-123, 700-729, 1120-1159, 1265-1324, 1661-1721, 1880-1907,
2594-2718, Grep `unprepared|unprepared_walk|run_not_deliverable|factory_record|run_reasons\(` ; `delivery-verdict-kinds.json`
(whole); `delivery_verdict.py` 120-199; `ledger.py` 30-53, 1195-1249, Grep `^def ` (test_state 1163, plan_row_state 679), Grep
`"not_executed|not_executed:` ; `check_traceability.py` 55-116; `acceptance.py` 631-661, 1472-1502; `check_witness.py` 85-114,
220-241; `validate_artifacts.py` 1718-1745, 2424-2441; `handoff_check.py` 135-159, 350-364; `controller.py` 4222-4285,
6070-6143, Grep `["code_only"]|code_only=True|"code_only": True` (1950); `gate_preflight.py` 2870-2909;
`references/conductor-actions.json:34` (install_dependencies row); `skills/qa-story/phases/s5.md` 136-153; `docs/SIBLING_MAP.md`
126-132; `design/architecture.md` 18-73; Glob `scripts/tests/fixtures/driver-exits/*.json` (classes, hooks, s0, gates, s1-s4,
s5, s6-s9, known_red*); Glob `agents/qa-failure-analyst*` (1 hit); `scripts/tests/test-layers.json` Grep `"(keep|quarantine)"\s*:`
(36, 7209) and the seven file names (test_check_delivery 531, test_check_witness 575, test_ledger 2831, test_s7_pretriage 5054,
test_third_verdict 6516 - keep; test_run_suite_reports 9710, test_traceability 10484 - quarantine).

Greps behind negative claims, each with its positive control of the same shape:
- "no driver code reads `executor_unavailable`" (D-15): Grep `executor_unavailable` over `ai-packages/qa-factory` with glob
  `!**/tests/**` -> 5 hits (s5.md:144, halts.md:28, run_suite.py:1572, CHANGELOG.md:6420, changelog.d) - the run_suite producer
  hit is the positive control of the same call.
- "no other reader of `run_witness_excused`": Grep `run_witness_excused` over scripts -> validate_artifacts 1734/1736,
  acceptance 547/626/631 (definition and comments), check_witness 89/92, handoff_check 150, test_check_witness - the definition
  hit is the control.
- "no `parse_gap` key in the run block": Read of the block literal `build_run_block` 573-597 and the only later additions
  598-606 (`proof_stamp`, `reference_run`); Grep `parse_gap` over scripts -> producers 2287/2293 write `summary[...]`; readers
  execution_request 2471-2480, red_sandbox 985 read the summary.
- test-layers keys: the Grep `^  "(keep|quarantine)"` returned nothing (wrong indentation guess), the corrected
  `"(keep|quarantine)"\s*:` found both (36, 7209) - the first call is a miscall, not a claim.

D5 - class walk for the three fixes (verdict per item):
- Readers of the RUN REPORT's `execution_status` (Grep `.get("execution_status")|["execution_status"]` over scripts, 40 hits,
  the rest read run summaries, job records or blocks): `driver_stage_s7.failures_to_triage` 12 -> applied (7a);
  `check_delivery.run_reasons` 1286 -> applied (7a); `validate_artifacts.check_run_report_v0` 2430 -> n/a (vocabulary and
  env_preflight agreement only); `handoff_check._execution_status` 357-359 -> n/a (carries the field into a form); `ledger.py`
  815, 1239 -> n/a (reads `env_blocked` only); `finalize_task.py` 637/756 -> the producer, unchanged by decision. Other
  `"not_executed"` hits (probe verdicts in probe_by_code/proof_level/probe_debt/red_sandbox, job states in execution_request/
  retro_numbers, ledger states, `judge_run.DIAGNOSED` on a summary) are other vocabularies -> n/a; `judge_run` (192-199) is a role
  reading a run log that may move a SUMMARY only to `env_blocked` -> n/a (not a pass road; noted as the nearest sibling).
- Producers of `run_not_deliverable`: `check_delivery.assess` 2623 (`own(run_reasons(...), "run_not_deliverable")`) is the only
  producer (Grep `run_not_deliverable` over check_delivery.py: 2623; kinds file 41) -> applied (7a). Producers of the same `no`
  for a no-report test: ledger, traceability (D-12) -> applied (7b).
- Readers of `run_witness`: check_witness RULES 232 -> applied (5b); validate_artifacts `PHASE_JSON_KEYS` 105 + 1731-1737 ->
  applied (5b); handoff_check `_run_witness` 139-154 (fields `artifacts.run_witness`, `run.witness`, `rounds[].verify.witness`,
  730-733) -> n/a (a derivation for role forms; no form exists for a stage no role ran, and an S6 runner form derives `run.witness`
  from the run report, 145); `check_delivery.witness_reasons` 711-724 -> applied through check_witness (5b); `manifest_view.py:203`
  -> n/a (display copy); validate_artifacts 152 (next-step text) -> n/a; `run_suite.py` 3044/3070 (collect never a run_witness) ->
  n/a; `manifest_put.py` 98, 2783-2793 (writes/merges the scalar) -> n/a.
- Readers of `work/automation-manifest.json` for an EMPTY manifest (Grep `automation-manifest\.json` over scripts *.py: 53
  production files): the witness group (check_witness, validate_artifacts, acceptance, handoff_check, check_delivery) -> applied
  (5b) or n/a as above; presence readers (`stage_guard.manifest_unread`, `stage_status`, `guard_pre_tool`, `refusal_registry`,
  `runtime_paths`, `story_step`) -> n/a (a present file passes; critic K2c read stage_guard 1005-1034); list readers that iterate
  `tests`/`unresolved` (brief_pack, manifest_view, report_facts, ledger, ledger_fingerprint, traceability, check_traceability,
  check_coverage, coverage_contract, case_stamp, contract, contract_slices, finalize_task, s7_pretriage, s7_reorder,
  driver_stage_s6, driver_stage_s7, driver_stage_plan, driver_runner, driver_dispatch, probe_by_code, probe_debt, proof_level,
  red_sandbox, execution_request, judge_code, judge_results, bug_neighbours, branch_accounting, stand_gaps, interim_packet,
  delivery_summary, factory_dashboard, gate_brief, retro_numbers, window_record, manifest_from_tests, migrate_artifacts,
  controller, s5_precheck, manifest_put) -> n/a by Grep class, NOT by reading each body: the Grep
  `(no|zero|empty) (automated )?tests|tests\[\] is empty|not manifest_tests|if not tests\b|tests == \[\]|len\(tests\) == 0` (-i)
  over scripts finds no refusal of an empty `tests` list in them (its positive control in the same call: `test_check_witness.py:125`
  "a manifest with no tests" and `dry_stub.py:570-572`); `report_facts.py:3681` (`if not tests["count"]`) is a count statement,
  not a refusal. `s5_precheck` (the S5 exit gate, GW1-8) runs on a role's finish; no role finishes on a code close -> the 5b
  `stage_done` premise run is the proof.

Taken from the critic's trail, not re-read: `test_controller_state.py:1145`, `judgment-census.json` rows 415/1118, the two
owns_readers runs, `stage_guard.py` 1005-1034, `driver_gates.py` 890-1073, `no_move.py:37`, `coverage_contract.py` 771-857. Not read:
`check_delivery.coverage_reasons` (the 7a measurement names it), `handoff_check` S7 form for a non-manual `NOT_EXECUTED` row (7b
item 9 checks it), `dependency_drift` `unknown` reason field (5a item 9 reads it), `story_run.py stand_remedy` body, `qa-runner.md`
beyond r2's grep, the 41 list readers' bodies (above).
r2's trail (section 13 of r2) stands for every fact r3 carries unchanged.
