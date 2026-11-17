# Spec U7 "pass without getting stuck" (t-1240) - DRAFT for Lead acceptance

Designer draft from the Lead brief `docs/tasks/specs/20261117-u7-pass-without-stuck-brief.md`. Facts by pointer: digests
t-1203 (`r*`, `s*`, `dsg.*`, `an.*`), t-1200 (`a2D1`, `a2C2`), t-1238 (`n:*`). Every site below was read in code on
17.11.2026 at the cited `path::symbol`; where the code differs from a digest row the row is flagged (section 9). No git log
was run (no shell): "unchanged since the digests" means "the code read today says what the row says", nothing more.
Paths are from `ai-packages/qa-factory/` unless they start with `docs/`, `plans/` or `tools/`.

Goal (owner, 17.11.2026, verbatim in the brief): the factory, knowing nothing of a project's form, passes every stage
without getting stuck and lets the agent do its work; "role first": work code hands to a person today is tried by a role
first, the person gets only the remainder (a physical device, credentials). A door that leads to a person past the role is
not a pass. A stage may cost a little more if quality is bought; blocking is never acceptable.

**Lead acceptance (Architect session, 17.11.2026).** Draft accepted for the plan critic; spot-checked in code: D-4
(`s7_pretriage.py::s6_closed_by_code` reads `not_executed` as intended), D-5 (`stand_check` only at
`driver_stage_build.py:139`), D-1 (`_no_entry` names the data gap and the red-sandbox door). Forks decided by the Lead:
F-1 = (a); F-2 = (a); F-3 = (a); F-4 = (b), applied only if the r4 measurement shows S7 refusing; F-6 = (a); F-7 = the
split into seven streams; F-8 = (a), U7 waits for RD1-24; F-9 = (a); F-10 = (a), a new pile `universality` (the Lead's
choice until the owner's word). OPEN, the owner's: F-5 (whether starting a second local emulator or stand instance is an
authorized preparation by default). Q-2 and Q-4 (the two analogs of section 9) go to the plan critic as class-completeness
questions.

---------------------------------------------------------------------------------------------------------------------

## 1. Architecture, owners, variety walk

### 1.1 AR-n touched, with the change check each demands (copied into every stream's DoD)

| AR | how the spec touches it | change check (DoD) |
|---|---|---|
| AR-2 (passage rule) | every site of classes A-C ends in a role move or a declared default said out loud | for each changed site: one table row whose input is an unknown axis value and whose expected outcome is "a role move is offered / the default is said", never a refusal with no door and never silence |
| AR-1 | `surfaces.json` gains words/hands data (S1); no new list in code; `AGENT_HANDS` tuple stays the one reader of `hands` (a2D1 is NOT turned into data here: U8, brief "Решено") | `git diff` of the stream adds no tuple/set literal of surface, language or tool names to a `.py` file; the test greps the diff for none (row in the stream's table: "no platform word in code") |
| AR-9 | every new or reworded refusal/question names what it expected and a door its receiver can use | each new text has a row asserting the door token is one the receiver can execute (FR-2) |
| AR-17 | class-B sites move from "person first" to "seam first, site question as fallback" (S3 r9, S5a r8, S6 r10) | a row per site: the state reaches `driver_conductor.Conductor.conductor` (the one seam) before any `Person` of that site is raised; the site question stays reachable as `site_fallback` |
| AR-23 | S5's empty automate scope gets a declared empty outcome (r11): NE25 already declares it; code is made to match | `references/null-outcomes.json` NE3/NE4/NE25 rows still resolve (`test_null_outcomes.py` green); a row: empty derived scope closes S5 by code |
| AR-25 | every state the changed sites can record has a way out (r11's Refusal with no code move becomes a close) | a row per new state with its exit named |
| AR-28 / FR-59 | every change errs toward "unknown is not a pass": an announced default never upgrades a capability to `ok` that was not checked; an underived scope never closes S5 | a row per site with the unknown input (unreadable table, underived scope, crashed probe) whose outcome is "not closed / not ok / asked" |
| AR-12 | role-first costs role turns; bought quality (owner: "a little more expensive") | no new code step runs on a web/API project that did not run before: rows "web project: byte-identical output" kept green (existing pins in `test_surfaces.py`, `test_readiness.py`) |
| AR-13 / AR-14 | new readers go through existing one readers (`surfaces.declared_surfaces`, `env_probe.blocked_by_of`, `controller` op `code_only`) | no second reader of `surfaces.json`, of the readiness record or of stage status is added (review item, critic Q6) |
| AR-29 | checks altered: see 1.2 | census rows of changed units updated in `scripts/tests/fixtures/judgment-census.json`; ratchets only shrink |

AR-19 (stage twins): r11 makes S5 a twin of S6's `s6.nothing` close (`driver_stage_s6.py::stage_S6`, lines 502-513); the
twin is named, the S6 side is unchanged. AR-24, AR-26, AR-27: not met (no person words, requirements or findings change road).

### 1.2 Checks added or altered: owner and census class (AR-29, P27)

| check (unit) | change | owner it serves | census class |
|---|---|---|---|
| `surfaces.py::declared_surfaces` | `hands` value for unknown/none/no-stand rows: "person" -> "role" (agent first); new `undeclared` entry when nothing is declared | data (code reports what the table and config say; the role judges what to do) | shape |
| `planning_contract.py::_row_of_nobody` | a `hands: none` surface no longer keeps a row from becoming `manual-agent` (role tries first) | data | shape |
| `readiness.py::_check_plain_environment` | URL-less row that does not declare in-process: note says the default taken | data | shape |
| `driver_s0.py::Driver.s0_rest` | `missing` capability goes to the seam first | judgment (the conductor judges whether it can settle; a person's word above it) | shape (the readiness record is read by field) |
| `gate_preflight.py::Rehearsal.check_s5_executor` | missing launcher: finding becomes seam-first (fork F-2) | judgment | shape |
| `gate_preflight.py::Rehearsal.check_s5_runtime_probe` | unchanged code; a test pins the bounded loop | data | shape |
| `driver_stage_s5.py::DriverStageS5.stage_S5` (class name as in the file) | empty derived scope: close by code, not Refusal | data | shape |
| `controller.py` op `code_only` (validate) | allowed stages {S0,S6,S7,S8} -> {S0,S5,S6,S7,S8}, S5 only with an empty derived automate scope | data | xref (it joins the request to the plan's dispositions) |
| `driver_stage_build.py::DriverStageBuild.stand_check` | unconfirmed stand goes seam-first | judgment | shape |
| `execution_request.py` reporter `none` | the run record says the default; see F-4 | data | shape |
| `probe_by_code.py::_no_entry` | text only: role door first (red-sandbox), tooling finding second | data | shape |

Commit lines: every package commit carries the `architecture:` and `judgment:` lines in the form `tools/architecture_gate.py`
checks (its source is the one carrier of the grammar; this spec does not copy it). Prescribed content per stream is in
section 5; a `judgment: none` line is never written bare - it always carries ` -- <why>`.

### 1.3 Variety walk (architecture.md section A, "How the map is walked")

- axis 1: held by role -- the automator judges an unknown language/build tool; unknown value -> `probe_by_code` refusal names the red-sandbox road first (r5), the manifest door stays (`r6`, unchanged)
- axis 2: held by table|role -- `references/surfaces.json` rows; unknown value -> cases go to the agent role first (`hands: role`), person only for the remainder (a2D1, s6.unknownword, r2)
- axis 3: held by key|role -- profile `run.reporter` key; unknown value -> `none` is said out loud on the run record and the role judges the log (r4, F-4)
- axis 4: held by role -- an all-manual plan (no automate case) closes S5 by code (r11) instead of a Refusal
- axis 7: held by key|role -- `environments[]` rows, `environment.access`; unknown value -> URL-less row: default said (r3); unconfirmed stand: seam first (r10); a case needing a second stand/device instance: role tries with authorized preparation actions, remainder to the person (edge E-7, fork F-5)
- axis 13: held by role -- a story whose S0 capability is missing goes seam-first (r9)
- axes 5, 6, 8, 9, 10, 11, 12: n/a -- no site of this spec reads the tracker, delivery target, host, people/process, language, task size or check kinds

No `narrows` line. Any builder finding that a change narrows a project form returns it as a question, never as a non-goal.

---------------------------------------------------------------------------------------------------------------------

## 2. Sites: current behaviour read in code, target, edges, error direction, test

Test layer words are `docs/TESTING.md`'s (scenario on recorded artifacts / data seam / case table). "One parameterised test
per behaviour": every new case is a ROW of the table named; no new test file outside the keep rows of
`scripts/tests/test-layers.json`. If the file a row lands in is quarantined there, the builder stops and returns a question.

### Class A - silent defaults

**r1 - `skills/qa-onboarding/phases/p1-discovery.md` row "Mobile surface" (line 43) + `phases/p2-interview.md` line 218**
- Now (read): the row records `mobile_surface` only when "a manifest or a test file ... names Appium" (or WebdriverIO with
  mobile capabilities). p2's device batch is asked "only when phase 1 recorded a `mobile_surface` section". A native app
  whose tests use another tool, or has no UI tests, gets no section, so p2 runs the web stand interview (HTTP address) and
  `environments[]` gets no `surface`: the silent default that feeds r2 and r3.
- Target: the row reads what the PRODUCT is, from the application's own build/manifest files (an application module that
  builds an installable package, a project file of a native toolchain), not from a test tool's name; it records the section
  with the evidence path:line and, separately, whether a driver the factory knows (a `drivers` row of
  `references/surfaces.json`) is named. The text names no platform, language or tool (P2): "the names are examples, not a
  list" stays; the class is "the product runs on a device or as a native application". p2 asks its batch whenever the
  section is recorded; fields phase 1 could not read are offered with "I do not know", which leaves them empty and is said
  in the summary (the existing p2 rule); and the summary says plainly which default is taken when no driver is named:
  "the factory has no way to drive this application by itself; the agent will try these cases with what it can reach, and
  hands you only what it cannot".
- Edges: (empty) no app module found -> the row records nothing, as today (web/API road), after the file's positive-control
  rule; (absent) a split repo with the app checkout "not located" -> the row is a gap for p2, never "no mobile"; (conflict)
  a repo with both a web app and a native app -> both recorded, both rows written (p2 already supports "a project with both
  keeps both rows"); (both worlds) a project already onboarded without the section -> nothing changes until re-onboarding;
  the doctor line of r2 (`undeclared`) is the only signal before it.
- Invariant: a product form the factory cannot drive is never recorded as web by omission; the interview never asks a
  device question of a project with no device evidence.
- Error direction: toward recording the section (one extra batch the person answers "I do not know") rather than omitting it.
- Test: none in code (markdown). Doc-dispatch witness (CLAUDE.md rule 11): key-presence run with the keys quoted in
  section 5, stream 2, with a negative control. Live proof: section 6, L1.

**r2 - `scripts/surfaces.py::declared_surfaces` (lines 112-114)**
- Now (read): `if not named and capabilities <= _table_free_words(): return {}`. A config with no `surface` on any
  environment and no capability word (or only `web`/`api`) answers `{}`: readiness publishes no `surfaces` key, the
  doctor prints nothing, and every later reader takes the web road. For a project that declared `web`/`api` this is a
  declared default (data); for one whose profiles declare NO capability word at all it is undeclared.
- Target: when no environment names a `surface` AND the union of declared capability words is EMPTY (no profile carries a
  word, or no profile exists while `profiles` is present), answer `{"undeclared": {"hands": "agent", "stand": None,
  "words": <surfaces.json words.undeclared>}}`. New data row `words.undeclared` in `references/surfaces.json`, for example:
  "No test surface is declared for this project, so the factory takes the web and API road by default. If the product is
  something else (an application on a device, a desktop or command-line program), say so by running the onboarding again."
  A project that declares `web`/`api` keeps `{}` byte for byte (the existing pin).
- Edges: (empty) `profiles` key absent entirely -> today `profiles=[]`, capabilities empty -> NEW: `undeclared` (fork F-1:
  absent `profiles` vs legacy configs); (absent table) the table is needed now for the words: unreadable -> the module's
  `ValueError`, readiness publishes `unknown` (existing path, line 1310-1311); (conflict) `undeclared` beside a device row
  cannot happen (a row with `surface` makes `named` non-empty); (both worlds) readers before/after: `gate_preflight.
  _surface_level_fits` reads `if not surfaces.declared_surfaces(config)` - with `undeclared` it proceeds to read the table
  and finds no fit for a profile with no words -> `[]`, the same answer; `unsupported()` filters `hands == "person"` and
  stays unaffected (`hands: agent`); readiness/doctor print the words (intended).
- Invariant: a web or API project that declared its words reads no table and prints no new line (AR-12 pin); an undeclared
  project is never silent.
- Error direction: toward saying the line (an extra doctor line), never toward silence.
- Test: case table in `scripts/tests/test_surfaces.py` (the `declared_surfaces` table near lines 268-310): rows "no
  capability word, no surface -> undeclared with words", "`profiles` absent -> per F-1", "web+api -> {} and the table not
  read (counter 0)" kept, "unreadable table with no words -> ValueError". Data seam: `test_readiness.py` row "the
  readiness record carries `surfaces.undeclared`".

**r3 - `scripts/readiness.py::_check_plain_environment` (lines 877-883)**
- Now (read): a row with no `base_url`/`url`/`health_url` counts as in-process whatever it declares; when every row is so
  and no environment key is declared the capability is `OK` "in-process environment(s), nothing to probe". A row that only
  lacks an address (a device stand described without `surface`, a stand nobody filled) passes S0 as in-process.
- Target: split the list into DECLARED in-process (`kind` in the existing three words, or `probe: none`) and URL-LESS
  (neither). All declared -> today's `OK` and note byte for byte. Any URL-less row -> status `OK` stays (S0 is not blocked
  and `environment` is not a required capability of S0: `driver_s0.py::Driver.s0_rest` line 2396) but the note says the
  default: "stand `<name>` names no address and does not say it runs in-process: taken as in-process, nothing probed; the
  stand is asked about before tests run". Whether the status should be `unknown` instead is fork F-6 (recommended: `OK`
  with the announced note, because `unknown` changes downstream readers' behaviour - doctor colour, gate A warnings - for
  every legacy in-process config).
- Edges: (empty) `stands` empty -> today's next branch (unchanged); (conflict) a row with `kind: in-process` AND an address
  -> declared wins (in-process list), as today; (both worlds) configs written before -> same status, a longer note only
  when a row is URL-less and undeclared.
- Invariant: no row that names an address is ever "nothing to probe"; a declared in-process project's record is byte-identical.
- Error direction: toward saying more (note), never toward a stronger status than today.
- Test: case table in `scripts/tests/test_readiness.py` (environment capability rows): "declared in-process -> note
  unchanged", "URL-less undeclared -> OK + default sentence", "mixed -> the default sentence names only the URL-less row".

**r4 - `scripts/execution_request.py` `REPORTERS` (line 29)**
- Now (read): `REPORTERS = {"pytest", "junit-xml", "trx", "none"}`; `none` is accepted. That a run with no report is recorded
  `not_executed` rests on the scout's grep of `run_suite.py` (t-1203 T63) and is NOT re-read here; that S6/S7 then "trips"
  rests on the design doc `docs/factory-map/qa-factory-paths.md` section 8 (t-1203 `s6.exit`) while
  `scripts/s7_pretriage.py:311` documents `not_executed` as "what S6 left on purpose" (read in grep output, line 311).
  The claim "S6 trips" is therefore unverified (section 9, flag D-4).
- Target, step 1 (measure first, PROJECT.md package p.6a): one command on a recorded story with a profile `reporter: none`
  through S5 run record -> S6 close -> S7 entry, its verbatim result written into this spec's section 9 by the builder
  before any edit. Step 2 by the measurement: (a) S7 does not refuse -> the only change is that the run record and the S6
  digest SAY the default ("no machine-readable report: the result of this run is read from its log by the role, not by
  code"); (b) S7 refuses -> fork F-4 goes to the Lead before code.
- Edges: (empty) `reporter` key absent -> as today's default reader (unchanged); (both worlds) records written before the
  change carry no sentence; readers ignore an absent field.
- Invariant: a run with no report is never recorded `passed` by code (FR-58: code is no oracle); the log is the role's to judge.
- Error direction: toward `not_executed` plus a sentence, never toward a pass.
- Test: data seam in the `execution_request`/run-record test the witness command prints (row: "reporter none -> record
  carries the default sentence"); the measurement is attached verbatim, not committed.

### Class B - doors to a person past the role

The one road for "role first" (P31, AR-17): the state goes to the conductor seam (`driver_conductor.py`,
`Conductor.conductor` / `conductor_round`), which settles it with the moves it has or asks; the SITE's own closed question is
the seam's fallback (`driver_conductor.py::site_person`, `state["site_fallback"]`, the C1-3 form). No site invents a second
road. Which role acts behind the seam for a given site is the conductor's judgment (AR-2); code hands it the facts.

**a2D1 + s6.unknownword - `scripts/surfaces.py` lines 24, 87-88, 123-141; `references/surfaces.json` `words`, rows `cli`, `desktop`**
- Now (read): `_who(row)` -> "agent" when `hands` in `AGENT_HANDS = ("browser","http","driver")`, else "person". A
  capability word the table lacks -> `{"hands":"person", words.unknown_word}` ("those cases go to a person"); `cli` and
  `desktop` rows (`hands: none`) -> "person" with their words; a native profile with no device stand -> "person" with
  `words.no_stand`. `unsupported()` returns these; readiness publishes them; the doctor prints the words verbatim
  (`skills/qa-doctor/SKILL.md:111`). Sibling found in the same class, NOT in the brief's list:
  `scripts/planning_contract.py::_row_of_nobody` (lines 2277-2297) and its caller (2334-2346): a plan row whose profile's
  surface row is `hands: none` is NOT converted to `manual-agent` and "stays as planned" with the table's words - the
  agent never tries it. Fixed in this stream (owns widened, designer rule 2).
- Target: a new `hands` reading "role": the agent role tries these cases first with the hands it has, the person gets the
  remainder with what was tried. In code: `_who` returns "role" for rows whose `hands` is not in `AGENT_HANDS`, and the
  three `"hands": "person"` literals at 128, 137, 140 become "role" (the hands value is a closed word set read only here;
  no platform word is added). `unsupported()` keeps its name and contract "what does not have an agent's own hands":
  returns entries whose `hands` is "role" (its one test caller and no production caller - grep 17.11: only
  `test_surfaces.py`). Data: the three texts in `surfaces.json` (`words.unknown_word`, `words.no_stand`, rows `cli`,
  `desktop` `words`) are rewritten to the role-first form, for example: "This project declares a test surface called
  \"{word}\" that the factory has no driver for: the agent tries those cases with what it can reach and hands you only
  what it cannot, with what it tried." `planning_contract._row_of_nobody`: a `hands: none` row no longer returns the
  "stays as planned" words; the row is converted to `manual-agent` like any other, and one line says the agent tries it
  without a capture driver (the evidence road: fork F-3).
- Edges: (empty) no capability, no surface -> r2; (absent) table unreadable -> `ValueError` -> readiness `unknown` (unchanged);
  (conflict) `words_only_alone` (cli beside web stays silent) -> unchanged; a word both unknown and native -> both said
  (existing row 308); (both worlds) readiness records written before carry "person": the doctor prints what the record
  says; no reader branches on the literal "person" in production (grep 17.11 over `scripts/*.py` for `hands`: only
  `surfaces.py`, `planning_contract.py` (`== "none"`), `driver_stage_s6.py::_cases_all_on_driver` (`is_device_row`,
  unchanged)). Readers block: section 7.
- Invariant: an unknown surface word never becomes "supported" (the `unsupported` error direction of the module docstring
  holds: it errs toward saying too much); the agent's attempt never produces a `passed` without evidence the existing
  manual-evidence gates accept.
- Error direction (reused function in a more consequential role: `_row_of_nobody` moves from "keep as planned" to "convert"):
  it may err toward converting (one agent attempt that ends `handed_to_person` / inconclusive) never toward dropping a row.
  Adversarial inputs that must stay safe: a profile id the config lacks; a broken table; a profile whose words map to rows
  of different `hands` (`row_for_profile` answers None -> converted as before); an obligation list that is empty (the
  existing "lists nothing" line, unchanged).
- Test: case table `scripts/tests/test_surfaces.py` (rows 275-310 change their expected "person" to "role" and the words
  to the new data; add "no platform/language word in the words" - the existing `LANGUAGE_WORDS` row covers it); data seam
  in the planning_contract test the witness prints (row: "`hands: none` profile -> converted to manual-agent with the
  role-first line"). Live proof: L2.

**r5 - `scripts/probe_by_code.py::_no_entry` (lines 1455-1465)**
- Now (read): a suffix with no `assertion_probes` row -> `ToolRefusal`: "factory data gap ... Return it as a tooling
  finding. Until the row exists the probe that breaks the product in a throwaway copy works for any language:
  {RED_SANDBOX_DOOR}". Both doors are the ROLE's (digest row r5 says owner "person": flag D-1). The person enters only
  because the red-sandbox road leaves no receipt for a language without a probe row (B-337), so the window falls to a
  `probe_gap` a person must word: that is node RD1-24 (`plans/piles/rules-debt/batch-1-phase-2.md:52`, ожидает, the
  owner's word 17.11.2026 "Отдельный П1 на потом").
- Target in U7: text order only - the red-sandbox road first ("prove the test can fail with the throwaway-copy probe: ...")
  and the tooling finding second; no new road. The receipt itself is RD1-24's, not U7's (fork F-8).
- Edges: directory path -> `Refusal` (call's fault), unchanged; no suffix -> unchanged wording of `what`.
- Invariant: the probe never guesses a grammar; the refusal stays a ToolRefusal (owner: factory).
- Test: case table row in `scripts/tests/test_probe_by_code.py` (named slow/canon in rules-debt/1 line 11: check
  `test-layers.json` first): "unknown suffix -> the red-sandbox door appears before the tooling sentence". Order: after
  RD1-24 merges (it owns the same test file).

**r8 - `scripts/gate_preflight.py::Rehearsal.check_s5_executor` (2815-2875) + `executor_options` (525-537)**
- Now (read): launcher `missing` -> one `PERSON_DECIDES` card per profile, three answers: install it yourself / name an
  environment / you run these cases (`handed_to_person`). No profile keys the automate cases -> `no_profile_question`
  (onboard / name the command / handed). The person gets the card at gate A; no role tries first.
- Target: the missing-launcher state goes seam-first: the conductor gets the profile, the tool name, the cases and the
  project's own `execution_prerequisites` and may settle it (locate the tool on the machine, use the project's recorded
  install/preparation command when the environment preparation record authorizes it, name another configured environment);
  the three-answer card stays the fallback, unchanged in words. The mechanism (a new class of finding vs. a GATE_REPAIRS
  row whose move is a conductor turn) is fork F-2.
- Edges: (empty) no automate rows -> nothing, as today; (absent) `skip_executor` -> off, as today; (conflict) a profile the
  person already handed -> not asked (unchanged); (both worlds) a story whose gate A card was answered before the change ->
  the recorded answer stands.
- Invariant: nothing is installed without an authorization the project recorded (environment preparation contract) or a
  person's word; `handed_to_person` is never chosen by code.
- Error direction: toward the card (a question too many), never toward assuming a launcher exists.
- Test: case table in `scripts/tests/test_gate_preflight.py` (executor rows): "missing launcher -> routed to the seam with
  the card as fallback"; order with PC4-4 below.

**r9 - `scripts/driver_s0.py::Driver.s0_rest` (2385-2422)**
- Now (read): a required capability `missing` -> `s0_stop("readiness", ...)` raises a `Person` directly (`s0_stop`,
  727-739): retry / go on / stop. No role tries to settle (for example a `tests_root` that discovery saw elsewhere).
- Target: seam-first with the site question as fallback: the conductor gets the readiness record's missing capability
  names, notes and owners; it settles what it can by the moves it has, else the same `s0.readiness` question is asked
  (fallback via `site_fallback`, so the closed tokens `retry` / `go on` / `stop` and `s0_read_word` keep working).
- Edges: (empty) nothing missing -> goes on (unchanged); (absent) no record / exit outside {0,1} -> the existing
  `gate_refusal` (factory's fault), unchanged and NOT routed as a person question; (conflict) a block already passed by the
  person (`s0_passed("readiness")`) -> no seam turn, as today; local story -> `ticket_adapter` not required (unchanged).
- Invariant: a `missing` capability never becomes a pass without either a re-check that no longer says `missing` or a
  person's recorded word; a crash is never read as an answer (the docstring's error direction).
- Error direction: toward asking.
- Test: case table in the S0 test the witness prints for `driver_s0.py` (row: "missing test_repo -> one conductor turn,
  then the s0.readiness question"; row: "exit 2 -> gate_refusal, no conductor turn"). The seam's existing pins
  (`test_no_move_seam_*`) stay green.

**r10 - `scripts/driver_stage_build.py::DriverStageBuild.stand_check` (139-206)**
- Now (read): confirmed stand -> return; a person's word on block `stand not confirmed` (S5 or S6) -> go on; a named stand
  whose `env_probe.py` exits 0 -> confirmed; otherwise `site_seam_person("environment", stand_question_text(...))` - a
  Person with seam MOVES on its tokens, asked of the person first. `stand_check` lives only here (grep 17.11:
  `def stand_check` one hit, driver_stage_build.py:139); OF5-5's owns cell names `driver_stage_s6.py (s6_no_stand,
  stand_check)` - `s6_no_stand` is in driver_stage_s6.py:672, `stand_check` is not (flag D-5).
- Target: before the person, the conductor gets the stand facts (`why` = `env_probe.blocked_by_of(out)`, the login answer,
  the configured stand names, the project's authorized preparation actions) and may settle (bring the stand up with the
  recorded bring-up command, retry after a recorded wait, choose the only other configured stand when the project
  authorizes it); the existing question is the fallback, words unchanged. Done in ONE node with OF5-5 (brief stream 6):
  OF5-5's first step (do `waiver.names_whole` matchers diverge) runs first; its merge of readers into `waiver` and this
  routing touch the same function.
- Edges: (empty) no stand recorded -> the conductor may only point at onboarding; the question follows; (conflict) the
  person's word already given -> no seam turn (unchanged, the word wins); (both worlds) `environment_pending` legacy pair
  -> asked as today, via the seam first.
- Invariant (positional, from the docstring): called only by a stage with something to run, before its first role; a
  resumed dispatch is not gated. The new seam turn sits AFTER the word check and the probe, BEFORE the Person: what stays
  unreachable is a role starting on an unconfirmed stand no word and no settled seam turn passed.
- Error direction: toward the question.
- Test: case table in `scripts/tests/test_story_run_s6.py` (stand rows at 1827-1865) and `test_human_questions.py:467`
  (S5): "unconfirmed stand -> one conductor turn, then the stand question". Edge E-7 below. Live proof: L3.

**Edge E-7 (owner, 17.11.2026): a case needs a second stand or device instance (axis 7).**
- What code does: carries the need as the case designer wrote it (case preconditions; code counts no devices: the set of
  "what needs two" is open variety, AR-2) and the project's recorded authorized preparation actions; nothing else.
- What the role tries: the runner/manual-agent role, at S6, brings up the second instance with the tools and actions the
  project authorized (the same environment preparation contract), records what it did in the case's `tried.md`
  (`references/stages.json` S6 output `work/evidence/manual/<case>/tried.md`).
- What remains for the person: what the role cannot do (hardware, a licence, an account, an action the project did not
  authorize) - handed with what was tried.
- Invariant: no instance is started that the project did not authorize; no role text names "two emulators" (P2).
- Whether starting a new emulator/simulator counts as an authorized preparation action by default is the owner's
  (fork F-5).

### Class C - unproven doors

**r11 - `scripts/driver_stage_s5.py::stage_S5` (226-231) + `scripts/controller.py` op `code_only` (6080-6093)**
- Now (read): `if not scope.get("scope"): raise Refusal("S5: stage-scope returned no automate cases: ...")`. The controller
  prepares S5 for every story not skipped by a `policy` event (`controller.py` 9301-9331, 1932-1938), so an all-manual plan
  reaches this Refusal, which goes to the conductor seam. The conductor cannot close S5 by code either:
  `controller.py` op `code_only` refuses any stage outside {S0, S6, S7, S8} ("code-only receipts are allowed only for S0,
  S6, S7 or S8"). `references/null-outcomes.json` NE25 says "an S5 whose stage-scope is empty ... S5 closes as it did
  before the plan existed (E7)": design and code disagree (`dsg.empty`). This is closer to "blocks" than "unproven"
  (flag D-2).
- Target: a DERIVED empty automate scope (`scope["derived"] is True` and `scope["scope"] == []`) closes S5 by code, twin of
  `s6.nothing`: `self.close_by_code("S5", "nothing to automate: the approved plan names no automate case",
  [<evidence>], finalize=False, site="s5.nothing", digest="nothing to automate")`; the controller's `code_only` accepts S5
  only when its own `stage_scope("S5")` is derived and empty (xref against the plan, never the request's word). An
  UNDERIVED empty scope (`derived` False: plan rows without disposition, an unreadable plan - `controller.py::stage_scope`
  4233-4245) keeps a Refusal, reworded to FR-1 form with a door ("the plan's dispositions could not be read: <reason>;
  rework S3 or record dispositions, then S5 runs again").
- Edges: (empty, derived) closes; (empty, underived) refused with door; (absent artifact, both worlds)
  `work/automation-manifest.json` is S5's `required_outputs` (`references/stages.json` S5): if it exists, it is the
  evidence; if absent, the close cites `work/test-plan.json` and the manifest's absence is declared (needs a check of how
  `stage_done --status done` treats a missing required output on a code-only close - builder reads `stage_done.py` and
  returns a question if it refuses); (conflict) a returned last round or owed repair round with an empty scope cannot
  exist (no window); the close is placed BEFORE `s5_todo` and every window logic.
- Invariant (positional): the close sits right after `stage_scope` and before any window/repair logic; what stays
  unreachable: a close over a scope nobody could read, a close while a dispatch of S5 is live (the controller's
  `code_close_conflicts` refuses it, unchanged).
- Error direction: toward the Refusal on any doubt about derivation.
- Test: case table in `scripts/tests/test_s5_window_leftovers.py` (the `stage_S5` rig at 692 ff.) rows "derived empty ->
  close_by_code site s5.nothing", "underived empty -> Refusal with door"; controller row in the `test_controller_*` file
  that holds `code_only` validation (slow/canon) "S5 code_only with a non-empty derived scope -> refused".

**r12 - `scripts/gate_preflight.py::Rehearsal.check_s5_runtime_probe` (4254-4315), `_derive_probe` (4542-4601); `scripts/driver_gates.py` `GATE_REPAIRS`, `GATE_REPAIR_CAP = 2`, `probe_move`, `typed_argv_move`**
- Now (read): a device stand -> one INFO note, no docker walk (4549-4553): on a mobile project WITH a device row there is
  no loop. Without a device row: `matched`/`unknown` -> `factory_fixable` with the write argv; the driver's repair row runs
  `runtime_probe --suggest --write`; a registered probe is skipped next time (4306). A failed write is `RepairFailed` ->
  conductor. Rounds per series are capped (`GATE_REPAIR_CAP = 2`). `stage_done` refuses to close S4 over a remaining
  `factory_fixable` finding (`stage_done.py` 482-484), passable by the person's word on block "gate rehearsal". Not proven
  by a test: the case where the write exits 0 but the next rehearsal still derives a finding (entry not registered under
  the profile key).
- Target: no code change; one scenario row pins the bound: write exits 0, finding repeats -> after the cap the finding goes
  to the top of gate A (`direct`) / the conductor, never a third repair round, and S4's close names the person's word door.
- Invariant: no unbounded repair series at a gate.
- Test: scenario row in `scripts/tests/test_story_run_gate_repair.py` (t-261 block, 1020 ff.).

---------------------------------------------------------------------------------------------------------------------

## 3. Refusals, doors, text

Every reworded or new text: FR-1 (what is wrong, what was expected, how to satisfy), FR-2 (a door the receiver can use: a
role gets a command or a move it holds; a person gets a closed answer), FR-57 (no ban is a dead end). Person-facing words
(surfaces.json words, the S5 close digest, the readiness notes) obey `references/human-questions.md` (checked by
`human_text.problems` where the site already checks; the stand question keeps its existing check). Nothing in this spec
removes a door a role holds; the role-first routing adds a turn, never replaces the fallback question.

---------------------------------------------------------------------------------------------------------------------

## 4. Overlaps with open batches (t-1238) and order

| stream | neighbours (t-1238 ids) | order |
|---|---|---|
| 1 surfaces.py, surfaces.json, planning_contract.py::_row_of_nobody | none for surfaces.py (t-1238 `r2`, `a2D1`, `s6.unknownword`); planning_contract.py NOT scouted by t-1238 (OF5-1 owns `planning_contract.py` for `isinstance(then, int)` sites - another function) | free; Lead greps piles for `_row_of_nobody` before launch (question Q-1) |
| 2 p1-discovery.md, p2-interview.md | `n:XT2-1`, `n:TQ1-6` (ожидает), `n:OH3-35` (onboarding-forge/1, в работе, dev1; owns p1/p2/p4) | after OH3-35 merges, or the late node merges main and resolves (PROJECT.md teamwork p.3) |
| 3 readiness.py (r3), driver_s0.py (r9) | `n:readiness-set` (OF5-9 :301-307, SS1-2, GW1-4, C3-8 :660, OF3-4, OF1-4: other functions); `n:FV2-37` (`probe_reason`), `n:C5-8` (critic-queue mention of `s0_rest` length) | file-level only; free |
| 4 execution_request.py (r4), probe_by_code.py (r5) | `n:EP4-1` (`_probe_refusal`), `n:RD1-14` (provenance), FV2-3/FV2-43, OF5-4 (`build_mine_request`); `n:RD1-24` (same defect as r5's person tail), `n:PC4-2` (cut of probe_by_code.py, waits on PC4-1 which waits on the owner's word "не сейчас"), `n:probe-set`, `n:OH9-1` (census rows) | r4 free after measurement; r5 strictly after RD1-24 (shared test file and road); if PC4-2 lands first, r5 edits the part file that holds `_no_entry` |
| 5a gate_preflight.py (r8, r12 test) | `n:RD1-13` → `n:RD1-14` (queue `gate_preflight.py` C3-j → C3-k), `n:EP1-26`, `n:CX2-15`, `n:PC4-4` | after RD1-13 and RD1-14 (rules-debt queue on the same file), or as a separate function with D-0048; PC4-4 below |
| 5b driver_stage_s5.py, controller.py (r11) | none for driver_stage_s5.py (t-1238 `r11`); controller.py: `n:PC4-5` (cut, waits on PC4-3/4), `conductor/3` C3-24 | free; if PC4-5 starts first, r11 lands on the part that holds op `code_only` |
| 6 driver_stage_build.py::stand_check (r10) | `n:OF5-5` (same function), `n:DH2-1` (`stand_question_text` price key), `n:FV3-21` (live-run-fvf/3, в работе, dev1: `stand_question_text`, `manual_lane_plan`), `n:FV2-38` (login-retry text) | ONE node with OF5-5 (fork F-9 where it lives); after FV3-21 merges (same file, neighbouring function, batch in work) |

PC4-2 / PC4-4 read (`plans/piles/package-ci/batch-4-dieta-testov-td-11-td-15.md`, rows 23 and 25):
- PC4-2 cuts `probe_by_code.py` into `probe_by_code_*.py` parts with the old name as facade; depends on PC4-1, which waits
  on the owner's word ("не сейчас", 12.11.2026). `_no_entry` is a module function and will move into some part; which one
  is spec B §6-§10's map (not read here).
- PC4-4 cuts `class Rehearsal` (~165 `check_*` methods) into `rehearsal_*.py` mixins; depends on PC4-2. `check_s5_executor`
  and `check_s5_runtime_probe` are `Rehearsal` methods (read: both defined inside the class at 2815 and 4254), so both move.
- Order: U7 streams 4 (r5) and 5a go BEFORE PC4-2/PC4-4 (those are blocked on the owner's word); if the owner unblocks them
  first, U7 re-reads the part names and edits the same functions there (no behaviour of the cut changes).

---------------------------------------------------------------------------------------------------------------------

## 5. Streams as builder nodes (for a weaker model) and dispatch templates

All streams: given = this spec (section 2 rows of the stream) + `design/factory-rules.md` whole (PROJECT.md package p.1) +
`docs/TESTING.md`. Witness: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>` (one run
after all edits). FR walk per section A-G in the report (builder rule). Commit lines: `architecture:` naming the AR-n of the
stream, `judgment:` per `tools/architecture_gate.py` (never bare `none`). The header lines below are content for
`python -B tools/dispatch_new.py`, which prints them checked; they are not typed by hand.

**Stream 1 - surfaces (r2, a2D1, s6.unknownword, sibling `_row_of_nobody`)**
- items: (1) `surfaces.declared_surfaces`: `undeclared` entry (r2) - test row 1-3; (2) `_who` and three literals -> "role"
  - test rows (expected values flip); (3) `surfaces.json` words: `undeclared` new, `unknown_word`, `no_stand`, `cli`,
  `desktop` rewritten role-first - test row "no platform word"; (4) `planning_contract._row_of_nobody` and caller: convert,
  one line - planning_contract test row.
- commit: `architecture: AR-2, AR-1, AR-28` with how kept; `judgment:` naming the units of 1.2.
```
given: C:/QAFactory/forge-repo/docs/tasks/specs/20261117-u7-pass-without-stuck-spec.md (sections 1, 2 a2D1/r2, 3, 5 stream 1), C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md, C:/QAFactory/forge-repo/docs/TESTING.md
owns: C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/surfaces.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/surfaces.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/planning_contract.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_surfaces.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/<the planning_contract test witness-for prints>
non-goals: Android/iOS rows, drivers, AGENT_HANDS as data (U8); readiness.py; the doctor skill text
handoff: report in the builder's report folder; diff on branch
edges: spec section 2 a2D1/r2 edges (empty profiles per F-1; unreadable table -> ValueError; words_only_alone unchanged; web byte-identical)
DoD: rows of spec section 2 a2D1, r2 green; `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>`
siblings: planning_contract._row_of_nobody (same class, included); driver_stage_s6._cases_all_on_driver (reads is_device_row only: n/a)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261117-u7-pass-without-stuck-spec.md
```

**Stream 2 - onboarding discovery (r1)**
- items: (1) p1 row "Mobile surface" rewritten to read the product's own build/manifest evidence, driver named separately;
  (2) p2 line 218 condition and the "no driver named" summary sentence. Doc-dispatch witness keys (verbatim, before the run):
  K1 `application's own build`, K2 `a driver the factory knows`, K3 `The names are examples, not a list`, K4 `I do not know`,
  K5 `hands you only what it cannot`; negative control: K6 a key deliberately absent. Script attached in full, not committed.
- commit: `architecture: AR-2 -- ...`; `judgment: none -- markdown of a role's phase text, no code check`.
```
given: the spec (sections 1, 2 r1, 5 stream 2), factory-rules.md, docs/TESTING.md, references/surfaces.json (read only)
owns: C:/QAFactory/forge-repo/ai-packages/qa-factory/skills/qa-onboarding/phases/p1-discovery.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/skills/qa-onboarding/phases/p2-interview.md
non-goals: Appium/emulator words, device questions beyond the existing batch (U8); p4-generate.md
handoff: report with the doc-dispatch witness
edges: spec r1 edges (no app module; split repo not located; web+native both; already-onboarded project)
DoD: keys K1-K5 present, K6 control fails; `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>` (if it prints a row for these files)
siblings: none -- the row is the one place the surface is detected (t-1203 ob.detect)
designer: the spec path
```

**Stream 3 - readiness and S0 (r3, r9)**
- items: (1) `_check_plain_environment` split declared/URL-less, the default sentence - readiness table rows; (2) `s0_rest`
  missing -> seam first, `s0.readiness` as `site_fallback` - S0 rows.
- commit: `architecture: AR-17, AR-28 -- ...`; `judgment:` naming `s0_rest`.
```
owns: C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/readiness.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_s0.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_readiness.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/<the S0 test witness-for prints>
non-goals: the readiness `remedy.steps` text (OF5-9); probe_reason (FV2-37); environment as a required S0 capability
edges: spec r3, r9 edges (declared in-process byte-identical; record crash stays gate_refusal; passed block not re-asked)
DoD: rows of spec r3, r9; `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>`
siblings: none -- r3 and r9 are the only S0 sites of the class (t-1203 s0.*)
```

**Stream 4 - run record and probe text (r4, r5)**
- items: (1) r4 measurement, verbatim into the report; then by its outcome (a) the default sentence on the record or (b)
  stop and return F-4; (2) r5 text order (after RD1-24).
```
owns: C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/execution_request.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/probe_by_code.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/<the execution_request test witness-for prints>
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_probe_by_code.py
non-goals: the red-sandbox receipt (RD1-24); _probe_refusal (EP4-1); provenance (RD1-14); assertion_probes rows for new languages (U8)
edges: spec r4, r5 edges
DoD: measurement attached; rows green; `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>`
siblings: run_suite.py not_executed writer -- read only; changes only if the measurement says so (returned as a question)
```

**Stream 5a - gate A (r8, r12)**
```
owns: C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_preflight.py (check_s5_executor and helpers only)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_gates.py (only if F-2 picks the repair-row form)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_preflight.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_story_run_gate_repair.py
non-goals: check_s5_stand_limits (RD1-13), provenance (RD1-14), the Rehearsal cut (PC4-4)
edges: spec r8, r12 edges
DoD: rows green; `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>`
siblings: run_suite.py mid-S5 executor question (same wording, `executor_question`) -- its road follows the same seam-first form (question Q-2)
```

**Stream 5b - S5 empty scope (r11)**
```
owns: C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_stage_s5.py (stage_S5)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/controller.py (op code_only validation only)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_s5_window_leftovers.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/<the test_controller_* file holding code_only validation>
C:/QAFactory/forge-repo/ai-packages/qa-factory/design/controller-blocks.md (if the generator re-renders it)
non-goals: S6's s6.nothing close; window logic; null-outcomes rows (they already declare the outcome)
edges: spec r11 edges (derived vs underived; manifest present/absent; live dispatch)
DoD: rows green; `test_null_outcomes.py` green inside the witness; `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>`
siblings: S6 twin `s6.nothing` (unchanged, named, AR-19)
```

**Stream 6 - stand question (r10 with OF5-5)**
```
owns: C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_stage_build.py (stand_check, stand_question_text callers only)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/waiver.py, check_delivery.py (stand_word), driver_stage_s6.py (s6_no_stand) -- OF5-5's part
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_story_run_s6.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_human_questions.py
non-goals: the stand question's words and prices (DH2-1, FV2-38); manual_lane_plan (FV3-21)
edges: spec r10 edges and E-7
DoD: OF5-5 step 1 result attached; rows green; `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>`
siblings: build_check (same four call sites) -- no person-first door of this class found in it (questions come from the probe record): n/a
```

---------------------------------------------------------------------------------------------------------------------

## 6. Live proof (FR-33) - rows for pile `live-runs`

One run on the owner's mobile project (U6 stand, the library-sync story), planned to close all rows at once:
- L1: onboarding of a native project with no known driver records the surface and says the default (r1).
- L2: readiness/doctor print `undeclared` or the role-first words; the cases on the undriven surface are tried by the agent
  role, the person receives only the remainder with `tried.md` (a2D1, s6.unknownword, r2, E-7).
- L3: an unconfirmed stand and a missing launcher go to the conductor first; a person question appears only after (r8, r10).
- L4: an all-manual plan passes S5 by code (r11).
- L5: S0 with a URL-less device row says the default (r3); a missing capability gets one conductor turn (r9).
- L6: a run with reporter `none` passes S6/S7 per the r4 measurement.

---------------------------------------------------------------------------------------------------------------------

## 7. Readers of every touched file (designer rule 7)

The block of `python -B tools/owns_readers.py --paths <touched> --names <changed>` was NOT attached to the brief (question
Q-3). Hand grep, 17.11.2026, Grep tool over `ai-packages/qa-factory/scripts` (positive control: the same pattern found
the definitions in `surfaces.py`):
- `surfaces.declared_surfaces(` / `unsupported(`: `readiness.py:1309` (publishes) - unchanged code, record gains
  `undeclared`/`role` (stream 1); `gate_preflight.py:777` (`_surface_level_fits`) - unchanged, same answer (r2 edge);
  `test_surfaces.py` - changes in stream 1.
- `import surfaces` (other functions, unaffected by the two changed names): `driver_stage_build.py:319`, `brief_pack.py:354`,
  `gate_preflight.py:4359`, `device_stand.py:39`, `env_probe.py:552,983`, `driver_stage_s6.py:1080`, `manual_capture.py:3373`,
  `planning_contract.py:2289` (changes in stream 1), `runtime_probe.py:296,732,1413` - unchanged.
- readiness `surfaces` key readers: `skills/qa-doctor/SKILL.md:111` (prints words verbatim) - unchanged text, new words
  flow through; `tests/test_mobile_road.py:333-347` - expected values may change (stream 1 runs it if witness-for prints it).
- `references/surfaces.json`: one reader `surfaces.py` (its note says so; read).
- `stand_check` callers: `driver_machine.py:1508,1618`, `driver_stage_s6.py:517`, `driver_stage_s5.py:201,330`, test rigs
  (`test_story_run_s5_parallel.py:172`, `test_story_run_repair_limit.py:522`, `test_story_run_loop.py:288`) - signature
  unchanged (stream 6).
- `stage_S5` callers: `driver_machine.py:1355` (getattr) - unchanged; NE3/NE4 guards in `null-outcomes.json` name
  `driver_stage_s5.py::stage_S5` - unchanged guard name.
- controller op `code_only` callers: `driver_dispatch.py::code_only` (2536), `driver_stage_s7.py::close_by_code` (763) -
  unchanged; S5 becomes legal only under the derived-empty condition.
- Not covered by hand grep (needs the tool block): readers outside `scripts/` (`tools/`, `.githooks/`, `.claude/`) of the
  touched package files, and the census/role-load ratchets that count refusal sites in `driver_stage_s5.py` and
  `gate_preflight.py`.

---------------------------------------------------------------------------------------------------------------------

## 8. Rule 10 four questions

Not a forge mechanism: the spec changes package behaviour (checks and texts), carried by the architecture gate lines per
commit and the judgment census. One contract change a reader might count as a mechanism - the new `hands` word "role" in
`surfaces.py` - is a value of an existing field with one reader; its detector is the `test_surfaces.py` table.

---------------------------------------------------------------------------------------------------------------------

## 9. Digest rows flagged (edge "code differs from the digest")

- D-1 t-1203 `r5` owner "person": `_no_entry` names two ROLE doors; the person enters through RD1-24 (no receipt). 
- D-2 t-1203 `r11` "door not traced": traced - the conductor cannot close S5 (`code_only` refuses S5); NE25 and code disagree; closer to class (i).
- D-3 t-1203 `r12` "loop on mobile not proven": with a device row there is no docker walk (4549); without one the series is bounded by `GATE_REPAIR_CAP`; unproven only for "write ok, entry not registered".
- D-4 t-1203 `r4` / `s6.exit` "S6 trips": rests on the design doc; `s7_pretriage.py:311` documents `not_executed` as intended. Measurement first.
- D-5 t-1238 OF5-5 mismatch: `stand_check` is only in `driver_stage_build.py:139`; OF5-5's owns cell places it in `driver_stage_s6.py` (only `s6_no_stand` lives there, :672). The OF5-5 row's owns cell needs correcting by its pile's Lead.
- D-6 t-1203 `r9`: a Person is raised directly by `s0_stop` (727-739), not through `site_seam_person`; confirms class B.
- Analog outside the three classes (reported, not specified): `gate_preflight.check_s5_toolchain` (2940-2944) returns silently for a non-pytest command - a silent default of class A on axis 3 ("a project on another runner is not told") - the brief's U8 list names `s4.tool`/`s4.pytest`? It does not; Lead to decide (question Q-4).
- Analog: `run_suite.py` asks the same executor question mid-S5 (`executor_question` docstring) - person-first, class B (Q-2).

---------------------------------------------------------------------------------------------------------------------

## 10. Forks (returned, not decided)

- F-1 `profiles` key absent (legacy configs) in r2: (a) treat as undeclared -> doctor line for every such config;
  (b) only an explicit `profiles: []`/no words counts. Recommend (a): silence is the defect named by the owner; the cost is
  one doctor line on legacy configs.
- F-2 mechanism of "seam first" at gate A (r8): (a) a GATE_REPAIRS row whose move is one conductor turn (existing table,
  bounded by the cap); (b) the finding raised as a seam Refusal before the gate packet; (c) leave r8 person-first and add a
  fourth answer "let the factory try". Recommend (a): one road, bounded, no new door kind; (c) keeps the door to the person
  past the role (not a pass).
- F-3 evidence road for an agent's attempt on a surface with no capture driver (cli/desktop/unknown word): (a) the
  existing manual-agent lane with `tried.md` and an `inconclusive`/`handed_to_person` result; (b) a new disposition.
  Recommend (a): no new state; costs a check that the manual lane accepts a case with no capture surface (builder reads
  `manual_capture` and returns a question if it refuses).
- F-4 (only if the r4 measurement shows S7 refusing) `reporter none`: (a) S7 accepts `not_executed` with the role's
  log verdict as lower-proof evidence; (b) S6 asks the runner role to judge the log and record the result through the
  manual-evidence road. Recommend (b): the role judges (P27), code records; (a) lets code relabel a role-less outcome.
- F-5 is starting a new emulator/simulator/second stand instance an authorized preparation action by default? (a) no -
  only actions the project recorded at onboarding; (b) yes for local virtual instances. Owner's intent question (axis 7
  edge, "сообразит ли фабрика завести два эмулятора"). Recommend (a) with an onboarding question that records it, because
  installing/starting software on the person's machine is the owner's risk call.
- F-6 r3 status for a URL-less undeclared row: (a) `OK` + announced default; (b) `unknown`. Recommend (a) (reason in r3).
- F-7 stream cut: the brief's six streams vs. this draft's seven (5 split into 5a gate A and 5b S5, because r11 needs
  `controller.py`, a hot file with its own queue). Recommend the split: the two parts share no file.
- F-8 r5 vs RD1-24: (a) U7 changes only the text order and waits for RD1-24; (b) U7 absorbs RD1-24 (the owner said
  "отдельный П1 на потом"). Recommend (a); (b) needs the owner's word.
- F-9 where the r10+OF5-5 node lives: (a) in OF5-5's batch (onboarding-forge/5) with U7 as dependency; (b) in U7's home.
  Recommend (a): the function's other work is already planned there.
- F-10 (brief's expected fork) where U7's nodes are filed: (a) a new pile `universality`; (b) existing piles by file
  (rules-debt, onboarding-forge, package-ci). Recommend (a) with cross-pile `очередь:` lines for F-8/F-9: one owner of
  the idea's graph; Lead and owner decide.

## 11. Small choices closed by the designer

- The new hands word is "role" (not "agent-first"): matches the owner's "роль первой"; one word, one reader.
- r2's new key name `undeclared`; readiness publishes it under the existing `surfaces` key (no new readiness key).
- r11 site name `s5.nothing` and digest "nothing to automate" (twin of `s6.nothing`).
- Example texts in section 2 are drafts; final words are the builder's under `human-questions.md`.

## 12. Reading trail

Read: the brief; `20261117-universality-variety-map-brief.md`; digests t-1203 (whole), t-1238 (whole), t-1200 (grep
`a2D1|s6.unknownword|a2D4`); `scripts/surfaces.py` (whole); `references/surfaces.json` (whole); `readiness.py` 800-939,
1290-1339; `brief_pack.py` 340-379; `planning_contract.py` 2270-2309 + grep `_row_of_nobody(`; `gate_preflight.py`
495-619, 755-874, 2815-2949, 4254-4423, 4542-4652; `driver_stage_build.py` 1-340; `driver_stage_s5.py` 150-349;
`driver_stage_s6.py` 470-579, 1068-1107; `controller.py` 1915-1949, 2150-2239, 4219-4279, 4590-4629, 6800-6859, 9300-9332,
grep `code_only` (6080-6105); `driver_machine.py` grep `stage_` (1340-1398); `driver_gates.py` 20-69, 480-559, 600-679;
`stage_done.py` 470-549; `driver_s0.py` 727-767, 2380-2454; `driver_runner.py::site_seam_person`; `driver_conductor.py`
method list + 440-484; `probe_by_code.py` 1420-1509; `execution_request.py` 22-37; `references/stages.json` grep S5;
`references/null-outcomes.json` 1-40; `references/manual-capture-steps.json` grep; `p1-discovery.md` (whole);
`p2-interview.md` 140-239; `design/architecture.md` 62-75; `judgment-census.json` 1-5; `plans/piles/onboarding-forge/
batch-5-...md` (whole); `plans/piles/rules-debt/batch-1-phase-2.md` 1-55; `plans/piles/package-ci/batch-4-...md` 1-26.
Greps (Grep tool, case-sensitive unless noted): `unsupported\(|declared_surfaces\(|import surfaces|from surfaces` (scripts:
42 hits); `def (stand_check|s6_no_stand)|stand_check\(` (12); `"skipped"` (stage status writers); `stage_S5\b|def
stage_scope`; `returned no automate|def code_only|def close_by_code` (4). One empty grep
(`skip_when|...` with a multi-directory brace glob) is not used as a claim. Not read: `run_suite.py` not_executed writer,
`manual_capture.py` manual lane for undriven surfaces (F-3), `stage_done` handling of a missing required output on a
code-only close (r11 edge), `tests/test-layers.json` quarantine rows of the named test files.
