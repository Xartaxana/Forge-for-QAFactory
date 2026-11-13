# OF3-2 (phase 2 of the project-knowledge plan): the seam, the answer's memory across stories, scope of an answer, the conductor's door, project kinds — SPEC (designer draft)

Designer (Opus), 13.11.2026. Draft for Lead acceptance; forks are in §6 and every node runs on the recommendation until answered.
Sources: node OF3-2 `plans/piles/onboarding-forge/batch-3-znaniya-o-proekte-fazy-1-6.md:28`; `plans/project-knowledge-plan.md` §2.1-2.6, §4 «Фаза 2»
(:218-229), §6, **§7 (:319-366; §7 is the later word, :322)**; phase 0 spec `docs/tasks/specs/t-2142-project-knowledge-phase0.md` (§7 :1077-1088);
phase 1 spec `docs/tasks/specs/t-129-of3-1-knowledge-catalog.md`; `plans/piles/project-knowledge/batch-2-usloviya-zamena-oglavlenie.md` (PK2-1 :22,
PK2-2 :23, PK2-18 :39) and its finding `findings/20261111-chego-ne-hvataet-planu-znanij-po-vneshnemu-razboru.md` (PK-A :15-20, PK-B :22-29).
PKG / P = `C:\QAFactory\forge-repo\ai-packages\qa-factory`. Every `path:line` below was read on the worktree `.claude/worktrees/of5-3`
(origin/main 1dfe10a) in this round, unless marked UNVERIFIED.

## Digest

Phase 0 already built the registry the plan asked for (§7 C1): `records/project-knowledge.json`, rows keyed `(key, environment NAME, element)`,
one writer `project_knowledge.record` under a lock, `revoke`, provenance with the person's words, built on the `environment_record` helpers.
Phase 1 put the catalogue into `config-keys.json` section `knowledge` (§7 C5). So phase 2 is NOT a new store. It is:

1. **The registry learns the rest of an answer's life** (plan 2.1, PK2-1, PK2-2): the state `asked` gets a producer; any catalogued key with a
   `scope` can carry rows (not only the five phase-0 keys); a row carries an optional `condition` (the person's words, never parsed) and a
   `supersedes` link; two live answers not linked by `supersedes` are a CONFLICT the reader hands over whole, never "the later one wins";
   a stand-scoped `not_needed` becomes legal (phase 0's FK-4 deferral). A new PURE reader `fact()` gives the seam's step result (C9: the read
   half writes nothing).
2. **The seam's ask half on the driver side** (plan 2.1/2.3, C8, C9): `Driver.need_fact` runs the order of plan §2.3 (value; registry memory;
   ask through the one question form; `while_unknown`), writes `asked`, and a knowledge question that holds no case waits for the next stop
   by a catalogue field, not by a list of kind names (the TR3-10 tuple `("walk_supply", "data_change")`, driver_dialog.py:456).
3. **Memory of an answer across stories** (plan 2.3 as corrected by C7): the driver's text-hash memory (`already_answered`,
   driver_dialog.py:381-392, one story's `driver-answers.jsonl`) stays as it is; what was missing is memory BETWEEN stories, and that is the
   registry read by `fact()`.
4. **Scope of an answer** (plan 2.4, В3): closed answers carry their scope in the token; free words go to the conductor, which decides the
   scope (role judgment, P27), says it aloud in one line, narrows on doubt; `revoke` is the one undo.
5. **The conductor's door "remember for the project / this stand"** (plan 2.5): one command, `project_knowledge.py remember`, that writes a
   config-stored fact ONLY as a recorded writer (`project_decisions` upsert + resolve with its receipt — §7 C2) and a registry row second.
6. **Project-made kinds** (plan 2.6): `qa-factory/knowledge.json` (kinds a project defines), elements as registry rows, a table of contents
   printed by `show --contents`; carried by a reinstall.
7. **TR3-10 becomes the seam's first consumer** (plan «Поглощает», В4 second branch: TR3-10 was accepted with its own road).
8. **B-294 and the release-next finding**: the guard stops a role from writing config approvals; the conductor's road to a fact is the door.
9. **The missing map axis** "memory of a person's answer" (§7 C3; phase 0 promised it, it is not in `docs/SIBLING_MAP.md`).

Behaviour that changes for a person (everything else is byte-for-byte today's):
- (K3/K5) The two S6 supply questions are asked as knowledge questions: the same text plus, when an earlier story asked and got no answer, one
  line "asked in <story> on <date>, not answered then"; a project that answered once is not asked in a later story (today it is not asked either,
  because the config holds the answer — no visible change on a project that answered).
- (K3) A knowledge question offers `not needed` scoped (fork F4: token words are the owner's).
- (K4) The conductor, after recording a free answer, says one line: "recorded as a rule of <the project | stand X>: <words>; to undo, say so".

---

## §0 Facts (measured this round)

**Registry (phase 0, on main)**
- F-1 `scripts/project_knowledge.py`: `RECORD_REL = "qa-factory/records/project-knowledge.json"` (:36), lock `qa-factory/state/project-knowledge.lock`
  (:37), `KEYS, CATALOGUE_PROBLEM = _derive_keys()` (:101) — `KEYS` holds ONLY rows whose `store` is `registry` / `config+registry` (:91).
- F-2 `STATES = (KNOWN, NOT_NEEDED, NOTICED)` (:104); comment :103 "`asked` is RESERVED for phase 2 (no producer here); `unreachable` is
  run-scoped and never stored". `SOURCES = ("person", "role", "legacy_config")` (:105), `BY = ("conductor", "driver")` (:106).
- F-3 `_latest` (:190-204): the later `at` wins, tie -> later row — no `supersedes`, so two answers never conflict today (PK2-2's gap).
- F-4 `record_problems` (:502-556): `state` not in STATES refused (:515); a stand-scoped or side key accepts `known` only (:517-518) — the
  phase-0 FK-4 deferral (t-2142:29); `scope != spec["scope"]` refused (:519-521).
- F-5 `record` (:559-583): under `lock`, `load` -> `record_problems` -> `_refuse_no_trace` -> same live state AND value returns the held row
  (:574-576) -> new row `{id, key, environment, element, state, scope, value, provenance{source, words, story, by, where}, at}` (:577-581).
- F-6 `revoke` (:586-591) through `ER.revoke_row`: the row stays with `revoked_at`.
- F-7 `value()` (:328-385): catalogue first; registry rows through `state()`; config rows: a present non-None value is `known` (:381-382) — so a
  template PLACEHOLDER (`manual.accounts_way.words: "not known"`, templates/config.json:63) reads `known` through `value()` (the reason for fork F9).
- F-8 `notice_from_handoff` (:627-659) reads `roster()` without the lock, then `record()` (PK2-18's race; finding
  `plans/piles/project-knowledge/findings/20261111-zapis-zamechennoj-roli-gonka-proverki-i-zapisi.md`).
- F-9 Catalogue `references/config-keys.json` section `knowledge` from :705; rows carry `store`, `compare`, `scope` (registry rows only),
  `needed_by`, `ask_when` (null) — e.g. :706-713. Count of rows: 78 (scout digest; this round counted 79 matches of the pattern
  `"knowledge"|"store": "registry|...|"ask_when"` — the section header plus rows; not re-counted row by row: UNVERIFIED exact 78).

**Asking today**
- F-10 `DriverDialog.already_answered` (driver_dialog.py:381-392): the body hash `question_body_sha` (:29-38) against one story's
  `state/driver-answers.jsonl`; `ask()` adds "You have answered this exact question before" (:302-314). One story only (§7 C7).
- F-11 `Person` (driver_core.py:192-233): fields `holds` (:233), `why_person`, `checked`, `source` (:227), `offered`, `options` (:212); no fact key.
- F-12 `Driver.closed_question(key, lead, options)` (driver_runner.py:1205-1208): the priced section of a `question-prices.json` key.
- F-13 `DriverDialog.deferrable` (driver_dialog.py:446-461): first line `if getattr(person, "no_hold", False) and person.kind in ("walk_supply",
  "data_change"): return True` (:456-457) — closed variety in code (AR-1); every doubt -> asked at once (:450-451). `defer_question`
  (:488-521) parks it until gate B (`deferred_step` :523-).
- F-14 TR3-10 (row `plans/piles/thinking-roles/batch-3-parallelnost.md:31`, status «принято»): `walk_supply_raise` / `walk_ask_once`
  (driver_stage_s6.py:1445-1479) open a `project_decisions.py add` row (scope project, owner user) with field refs `/manual/accounts_way`,
  `/manual/data_way` or `/manual/data_way/may`; `walk_asked` (:1439-1443) = deferred item or `<kind>_asked` state key, one story;
  conductor rows `walk_supply_way`, `walk_account_words`, `data_change_words` (conductor-actions.json:36-38) resolve those DD rows.
  `design/state-exits.md:204-205` hold the rows of the two questions (exit proof `test_walk_supply.py`).
- F-15 Stand-gap words: `accept` / `accept always` (`lasting: true`) in `references/question-vocabulary.json:34-39`; the lasting write is
  `stand_gaps.record_lasting` (stand_gaps.py:1243-1254) -> `environment_record.record` (environment_record.py:326-348, `accept` only).
- F-16 `references/conductor-actions.json` rows :26-29 are the phase-0 doors `project_knowledge.py account|role|side|revoke`; no row records
  a fact "for the project" in general (whole file read).
- F-17 `references/question-prices.json` already prices a `not needed` answer (e.g. `s0.ticket_read`, :3-8).
- F-18 `references/person-owned.json` classes: access, requirement_intent, money, risk, outbound, team_agreement, subjective, gate_word (:5-12).

**Writing the config (§7 C2)**
- F-19 `config_contract.recorded_writes` (config_contract.py:2350-2388) keeps across `restore_config` only writes with a record: onboarding
  approvals, report adaptations, and `_decision_writes` (:2394-2414) = `project_decisions.resolve` receipts
  `state/decision-transactions/DD-n.json` with `recorded_at` and `before`. `project_decisions.resolve` (project_decisions.py:450-523) writes
  that receipt (:495-506) and the config (:509-510). `upsert` (:400-432) returns an existing OPEN row of the same refs (:421-423).
- F-20 The registry file is NOT `config.json`; `restore_config` does not touch it (it restores `qa-factory/config.json` only, :2498-).

**Guard**
- F-21 `guard_pre_tool.py:1787`: role refusal of `project_knowledge.py (account|role|revoke|side)`; `_SANCTIONED_CONFIG_SCRIPTS =
  {"config_contract.py": (), "project_decisions.py": (), "runtime_probe.py": ("--write",), "ticket_adapter.py": ("--migrate-method",)}`
  (:1900-1901) — `()` sanctions ANY argument of `config_contract.py` (B-294 (a) still open; the finding's line numbers :1359/:1656/:1700 are
  stale). Case-insensitive grep `record.approval|config_contract` over guard_pre_tool.py: hits :1610, :1900, :1970, :2194 only — no
  `--record-approval` / `--apply` recognition (positive control: the same call shape found `config_contract` at :1900).
- F-22 The main session (orchestrator, conductor, onboarding) is never refused by the config-write guard (comment :1894-1897).

**Records and install**
- F-23 `references/install-paths.json:56`: `qa-factory/records/project-knowledge.json` carried, reader `project_knowledge.py`. No row for
  `qa-factory/knowledge.json` (whole file read). Class names in the table: carried / regenerated / discarded / not_ours (:3) — the plan's
  "переносится" is `carried`.

**Map and tests**
- F-24 `docs/SIBLING_MAP.md` has axes 1-36 (headings grep :24-:606); none is "memory of a person's answer" (positive control: the same grep
  found every axis heading). Axis 34 is P31 (:582).
- F-25 `test-layers.json`: `keep` :35-7022, `quarantine` from :7023. Keep rows used here: `test_project_knowledge.py` (:3952, register;
  covers project_knowledge.py, config_contract.py, event_store.py, hooklib.py, project_decisions.py), `test_human_questions.py` (:2441, table),
  `test_walk_supply.py` (:6555, gate_named), `test_story_run_deferred.py` (:5514, detector — slow, CI only), `test_state_exits.py` (:5346),
  `test_driver_layers.py` (:1377), `test_conductor_doors.py` (:662), `test_guard_project_knowledge.py` (:2154), `test_guard_write_owners.py`
  (:2182), `test_install_paths.py` (:2629, slow per t-2142:1059 — CI), `test_judgment_census.py` (:2709, slow — CI), `test_person_owned.py`
  (:3480), `test_words_doors.py` (:6904). QUARANTINED (never edited, never a witness): `test_config_revert.py` (:7507),
  `test_project_decisions_stand_facts.py` (:9059), `test_guard_secrets.py` (:8268), every `test_project_decisions_*` row from :9042.
- F-26 Phase 1 node f (R2/R3, fixture `knowledge-read-baseline.json`, `needed_by` reconciliation in config-keys.json) is NOT on main (brief).

**Premise measured (brief item 6)**
- M-1 Real-run fixtures carry ONE story with a question log: `scripts/tests/fixtures/stories/local-1-arm-b/state/driver-questions.jsonl`
  (37 lines; a Grep of `"kind"` counted 37 matches in that file, and no other `driver-questions.jsonl` under fixtures). Kinds by
  Grep `-o "kind": ?"[a-z_0-9]+"`: conductor 13, refusal 5, halt 4, repair_limit 3, exit_limit 2, code_close 2, and one each of s1_review,
  s1_gap, questions, stand_identity, retro (34 lines matched; 3 lines had no match of that shape). By KIND only `stand_identity` (1 of 34) is a
  question about a lasting project/stand fact, and its fact is phase 3.2's (stand card). Whether any of the 13 conductor questions asked a
  lasting fact is a reading of their text — judgment, not countable by code. **Conclusion: the fixtures cannot measure what `need_fact` would
  have saved; the measurer is phase 6.2 (questions per story by key).** To measure before K5 starts, if the Lead wants the conductor share:
  `python -B -c "import json,pathlib;p=pathlib.Path(r'C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\stories\local-1-arm-b\state');[print(json.loads(l).get('kind'),json.loads(l).get('why_person')) for l in (p/'driver-questions.jsonl').read_text(encoding='utf-8').splitlines() if l.strip()]"`
  — UNMEASURED (no shell); then a reader judges each conductor question text against the catalogue keys.
- M-2 To measure before K1 starts (the legacy-row rule of F1): how many subjects of an existing registry hold two or more live rows —
  `python -B -c "import json,collections,pathlib,sys;d=json.loads(pathlib.Path(sys.argv[1]).read_text(encoding='utf-8-sig'));c=collections.Counter((r.get('key'),r.get('environment'),r.get('element')) for r in d.get('facts',[]) if not r.get('revoked_at'));print({k:v for k,v in c.items() if v>1})" <stand project>\qa-factory\records\project-knowledge.json`
  — UNMEASURED (no shell; the stand copy is outside the repo, `docs/RUNBOOK.md` §11).

---

## §1 AR-n touched, owners and census classes, FR sections

| AR | How OF3-2 keeps it | Change check in the DoD |
|---|---|---|
| AR-1 | the TR3-10 kind tuple in `deferrable` (driver_dialog.py:456) becomes a catalogue field `holds: "none"` read by key; `while_unknown`, `answer`, `question` are row fields | K3 row "a Person with `no_hold` and a fact whose row says `holds: none` is deferrable; the same flag on any other Person is asked at once"; K5 deletes the tuple; grep `"walk_supply", "data_change"` over scripts/ in the report (positive control: the same grep finds driver_dialog.py:456 before the edit) |
| AR-3 | the answer registry stays the second home of a project fact; a config-stored fact written by the seam goes through the recorded writer | K2 row "a fact remembered in a story is alive after `restore_config`" (C2, red-first) |
| AR-13 | registry read only through `state` / `fact` / `roster` / `value` / `kinds` / `contents`; a fact whose known-ness has its own reader (`config_contract.walk_supply`) is judged by it (F9) | K1/K5 rows; grep `project-knowledge.json` / `knowledge.json` reads outside project_knowledge.py in the report (positive control `install_paths`) |
| AR-14 | one writer of the registry (`record`) and of `knowledge.json` (`record_kind`); `remember` is the conductor's door and calls `project_decisions.resolve` for config, never writes `config.json` itself; the guard closes the new write subcommands to roles | K6 rows in `test_guard_project_knowledge.py`; `references/artifact-writers.json` is not touched (the registry is not a stage artifact; UNVERIFIED that it has no row — K2 greps it with a positive control and adds a row only if records are listed there) |
| AR-15 | one road for "a person's answer kept across stories": the registry + `need_fact`; TR3-10 leaves its DD-row road (K5); stand-gap `accept always` stays on `environment_record` until phase 3.2 (named, §5 non-goals) | K5 rows; the new axis 37 (K7) lists every carrier |
| AR-16 | a knowledge question is a `question-prices.json` key, built by `closed_question`, goes `Person` -> `ask` -> `take_answer`, passes `human_text.problems`; asked again in a later story its text changes (one line) | K3 rows in `test_human_questions.py` |
| AR-17 | free words go to the conductor; code reads only offered tokens; the question carries a `person-owned.json` class (`why_person`) from the catalogue row's `person_class` | K3 row "a knowledge Person carries `why_person` = the row's `person_class`"; K4 conductor rows |
| AR-20 | `driver-layers.json` gains rows for new Driver names (not a ratchet raise: names rows are not shrink-only; the upward-edge exceptions are, and none is added); `judgment-census.json` gains `shape` rows only (not ratcheted) | builder STOPs on any ratchet raise; lists added rows |
| AR-22 | every new catalogue field has a phase-2 reader (§2 table); `derive` is NOT added (no deriver in phase 2, fork F8) | K1 data-join row "every row with `ask_when: first_need` carries `question`, `while_unknown`, `scope`, `person_class`; every `while_unknown: default` carries `safe_direction`" |
| AR-23 | a list fact's empty outcome: no element rows = `elements: []` with `problem: ""` (distinct from an unreadable registry); `contents()` with no kinds = `[]` plus the line "the project has defined no kinds of its own" | K2 rows |
| AR-24 | the person's words reach the registry whole (`--words-file` through `person_words.read`, `door()` on empty); a `condition` is the person's words, whole, carried with the fact | K1/K2 rows; `test_words_doors.py` row for `remember` and `kind` |
| AR-25 | new stored state `asked` gets a `state-exits.md` row (reversed by a later `known`/`not_needed` row or `revoke`); conflict is computed, not stored, and exits by `remember --supersedes` or `revoke` | K1 row in `state-exits.md`; `test_state_exits.py` green |
| AR-28 | `fact()` errs toward asking: conflict, a conditional row, `asked`, `noticed_unconfirmed`, an unreadable registry or catalogue, a placeholder value — none suppresses a question or reads `known` | K1 parameterised row set (§3 adversarial inputs) |
| AR-29 | every code check here judges data (shape, presence, joins); scope of a free answer and applicability of a `condition` are judgment (conductor / role) | census table below |

Owners and census classes of every check this spec adds or alters (CLAUDE.md rule 10, P27, AR-29):

| check | where | owner | census class | why it is not judgment |
|---|---|---|---|---|
| `record_problems` (altered: `asked` state, stand `not_needed`, `supersedes` id exists and is of the same subject, `condition` is text, `project:<kind>` key exists in `knowledge.json`) | project_knowledge.py | data (code) | existing unit, `shape` (unchanged class) | presence and form of fields; an id resolves to a row |
| `kind_problems` (new: kind name form, `says` non-empty one line, `scope` in {project, stand}, `needed_by` a list of role names known to `references/stages.json` or empty) | project_knowledge.py | data | new unit, `shape`, roles `[]` | form and a join to a data file |
| `fact()` step selection | project_knowledge.py | data | not a unit (a reader; no refusal site) | presence of rows and states |
| `Driver.need_fact` routing | driver_dialog.py | data (routes) / intent (the person answers) | not a unit (raises a Person; `# remains:` comment per AR-17) | which step applies is presence of a value / row |
| `deferrable` first line (altered: catalogue `holds: none` instead of a kind tuple) | driver_dialog.py | data | existing unit, class unchanged | a field read by key |
| guard: role running `config_contract.py --record-approval|--apply`, `onboard_apply.py --apply`, `project_knowledge.py remember|kind` | guard_pre_tool.py | intent (only the person's onboarding approves; only the conductor records a person's word) | existing guard units, `safety` (protection of the person's words and approvals) — expected NO new unit; if the builder must add one, `safety` +1 is a named raise to approve BEFORE dispatch (R-1) | a command shape, not a meaning |
| conductor's scope of a free answer (В3) | references/conductor.md (role text) | judgment (conductor), accepted by the person (aloud line + revoke) | none (not code) | — |
| applicability of a `condition` to a story | the reading role / conductor | judgment | none | code stores and delivers, never parses (PK2-1) |

No ratchet raise of `judgment-census.json`, `NO_MOVE_BASELINE` or `role-load.json` is expected or approved except R-1 if it arises.

FR sections walked: A (FR-1/FR-2: every new refusal names what it expected and a door the caller can use — `remember`, `kind`, guard;
FR-57), B (FR-6/FR-7: knowledge questions through the form, a re-ask in a later story changes its text; FR-8: words whole), C (FR-13: kinds and
fields are data; FR-38: a check's requirement — catalogue row fields — is stated where the conductor reads it, conductor-actions row;
FR-39: what the rules let the conductor do the guard permits — the main session is never refused), D (FR-59: unknown -> ask or declared safe
default), E (FR-41: an unreadable registry is named, not empty), F (FR-53: a `no_trace` story writes no registry row — the existing
`_refuse_no_trace`, PK2-11/PK2-19 neighbours), G (FR-30 English, FR-32, FR-54 siblings by the map).

---

## §2 Catalogue fields added in phase 2 (`config-keys.json` section `knowledge`)

Only fields with a phase-2 reader (AR-22). `scope` already exists on the five registry rows (phase 0/1) and IS the plan's `about`
(plan §2.1 names it `about`; one fact, one field — small choice, §7). Values are set ONLY on rows a phase-2 consumer calls; every other row
keeps its phase-1 shape (`ask_when: null`) until phase 3/4.

| field | meaning | values | phase-2 reader | rows that get it in phase 2 |
|---|---|---|---|---|
| `scope` | where an answer holds (exists) | `project` · `stand` | `record_problems`, `fact` | + `manual.accounts_way`, `manual.data_way`, `manual.data_way.may` (new rows if absent — K1 checks; scope `project`) |
| `value` | one value or a growing list of elements | `one` · `list` | `fact` (list: elements = live rows; never "closed"), `contents` | the five registry rows (`product.roles` `list`; `environments.credentials_by_role` `list`; side keys `list`), the three TR3-10 rows `one` |
| `ask_when` | when the factory learns it | `first_need` on the rows above; `null` elsewhere (values for the rest: phase 4, C6) | `need_fact` (a row without `first_need` is never asked by the seam: returns `while_unknown` / unknown) | the three TR3-10 rows |
| `question` | the `question-prices.json` key of the question | a key that exists in question-prices.json | `need_fact` -> `closed_question` | TR3-10 rows: `walk_supply` / `data_change` keys as today (UNVERIFIED: K5 reads which price keys the two questions use today and names them; if none, `knowledge.first_need`) |
| `answer` | the answer's form | `closed` (tokens only) · `words` (the conductor reads) · `both` | `need_fact` (sets `offered`) | TR3-10: `both` |
| `person_class` | the `person-owned.json` class (`why_person`) | one of F-18 | `need_fact` | TR3-10: `access` (accounts_way), `team_agreement` (data_way.may) — small choice, §7 |
| `holds` | does the question hold cases | `none` (asked at the next stop the story makes anyway; holds nothing) · `cases` (the caller passes `holds`) | `deferrable` | TR3-10 rows `none` |
| `while_unknown` | what the factory does while no answer | `default` · `gap` · `hold` (C10: `in_turn` removed) | `need_fact` returns it to the caller | TR3-10: `default` |
| `safe_direction` | required with `default`: why the default is the safe side (C10) | one sentence | the K1 data-join row (presence) and the conductor (reads it) | TR3-10: accounts_way "no extra accounts: lanes run in turn"; data_way.may "only use what exists: no record is created or removed on the stand" |

Not added (with reason): `derive` (no deriver in phase 2 — fork F8, phase 4.2), `about` (= `scope`), `store` changes (none).

## §3 The registry (K1, K2) — `scripts/project_knowledge.py`

**States.** `STATES = (KNOWN, NOT_NEEDED, NOTICED, ASKED)`; `ASKED = "asked"`. `unknown` and `conflict` are computed, never stored;
`unreachable` is run-scoped and not stored here (C10; §5 small choice: the driver keeps it in its own state).

**Keys a row may carry (K1).** `_derive_keys` builds `KEYS` from EVERY catalogue row that has a string `scope` in {project, stand}
(today: only `store` registry rows, F-1); `compare` defaults to `exact` for a row without one. POSITIONAL invariant: the five phase-0 keys keep
their `scope`/`compare` and their order first (row order), so `report_facts` and `test_gate_role_accounts.py:82` read the same values; a row
with no `scope` is NOT a registry key (`record_problems` refuses it with today's text). Damaged catalogue: today's `CATALOGUE_PROBLEM` road.
Project kinds (K2) add keys `project:<kind name>` read from `knowledge.json` at call time (not at import: the file changes at runtime).

**Row fields (K1).** Today's row plus two OPTIONAL fields written by phase-2 `record`:
- `condition`: the person's words limiting where the answer holds ("only for the EU contour"), `""` = none. Stored whole (no cut; FR-8),
  surrounding blank space stripped, never parsed or matched by code (PK2-1). Returned by `state()`, `value()`, `fact()`, `roster()` entries.
- `supersedes`: the id of the row this answer replaces — the head the writer READ — or `null` ("I read no answer"). A row written by phase-2
  `record` ALWAYS carries the key; a legacy row (no key) follows fork F1 (recommended: read as superseding the subject's previous live row —
  today's later-wins, so no existing registry turns into conflicts).

**Heads and conflict (K1, PK2-2).** For a subject `(key, environment, element)`: the live rows (usable, not revoked) minus every row some
live row supersedes = the HEADS. One head -> that row decides `state`. Two or more heads -> `state: unknown` for every code reader, with
`conflicts: [ids]`; `roster()` lists each head with `conflict: True`; `value()` returns `value: None`, `conflicts`. Nothing picks one.
INVARIANT: between two rows written by phase-2 `record`, the later one never wins silently.
Revoking the only head -> the subject reads `unknown` (fork F2: the superseded predecessor does NOT revive — recommended).

**`record(root, *, key, environment, element, state, scope, value, words, source, story, by, where="", task_root=None, condition="",
supersedes=MISSING)`** (K1): `supersedes` MISSING (a phase-0 caller) = the current single head's id or `null` when none (today's callers keep
their meaning: they always saw the held row under the lock). Under the lock, as today: `load` -> `record_problems` -> `_refuse_no_trace`.
Then: the same live state, value AND condition as the current single head -> that row, `created` False (today's idempotence, now including
`condition`). Else a new row with `supersedes` as given. Two stories writing at once: both rows are saved (the lock serialises them); the second,
whose `supersedes` is not the current head, makes a conflict — that is the intended outcome (PK-B), not a refusal.
`record_problems` adds: `asked` is legal for any key and any scope (an `asked` row's `value` is `null`); `not_needed` legal for a stand-scoped
NON-side key (lifts FK-4; side keys stay `known`-only, :517); `supersedes` given and not an id of a row of the SAME subject -> refused ("PK-9 is
not an answer about <key> <element> on <stand>; nothing was recorded; `project_knowledge.py show` lists the ids"); `condition` not a string ->
refused.

**`fact(root, key, environment="", element="", story="", known=None, cfg=None) -> dict`** (K1; PURE, never raises, writes nothing — C9):
returns `{"step", "value", "row", "rows", "conflicts", "condition", "while_unknown", "problem"}` where `step` is one of
`known` · `not_needed` · `asked_here` · `asked_before` · `unknown`. ORDER (POSITIONAL invariant: the catalogue is read first, so a key
with no row can never read `known`; a value read before the registry, so the registry never overrides a value the carrier holds):
1. no catalogue row -> `unknown` + problem;
2. the value: `known` given (bool) by the caller's own reader of that fact wins (fork F9); else `value()`; a `known` value -> `step: known`;
3. the registry heads: conflict -> `unknown` + `conflicts`; a head `not_needed` with an EMPTY condition -> `not_needed`; a head `known`
   (registry-stored fact) -> `known`; a head `asked` whose `provenance.story == story` (non-empty) -> `asked_here`; a head `asked` of another
   (or no) story -> `asked_before` (row given so the text can say when); a head `noticed_unconfirmed` -> `unknown` (row given);
4. else `unknown`; `while_unknown` is the row's (`{"mode", "default", "safe_direction"}`), `None` when the row has none.
ERROR DIRECTION (a reader that now SUPPRESSES questions for any catalogued key — a more consequential role than phase 0's roles-only road):
it may err only toward asking. Adversarial inputs that must give `unknown` / `asked_before`, never `known` / `not_needed` (each a row of one
parameterised test, id = the input): unreadable registry; registry of another `schema_version`; damaged catalogue; key with no row; revoked
head; head of another scope; head on another stand (exact name, case differs); `not_needed` head WITH a non-empty condition; two heads
(conflict); `noticed_unconfirmed` head; `asked` head of another story; `asked` head with an empty `story`; a placeholder config value with
`known=False` from the caller; `value()` known but the caller says `known=False` (the caller's reader wins toward asking).

**Project kinds (K2).** File `qa-factory/knowledge.json` (absent until the first `kind` command):
`{"schema_version": 1, "kinds": {"<name>": {"says": "<one sentence>", "scope": "project"|"stand", "needed_by": ["<role>", ...],
"by": "conductor", "words": "<the person's words>", "story": "<id>", "at": "<iso>"}}}`.
- `kinds(root) -> {"kinds": {...}, "problem"}` (pure; absent file -> `{}` and `""`; unreadable / not an object / other schema -> `{}` and
  the problem). The one reader (AR-13).
- `record_kind(root, *, name, says, scope, needed_by, words, story, by, task_root)` under the SAME lock as `record`; refuses by
  `kind_problems` (name: 1-60 chars, letters/digits/space/`-`/`_`, not starting with a digit, case-folded unique among kinds; `says` one line
  1-200 chars; `scope`; `needed_by` list of role names that exist in `references/stages.json` (UNVERIFIED that roles are listed there by
  name — K2 checks; if not, `agents/<role>.md` exists); empty words of a person -> `person_words.door`), `_refuse_no_trace`. A kind of the same
  name with the same fields -> existing, `created` False; changed `says`/`needed_by` -> replaced in place with the previous fields kept under
  `history` (the kind is a definition, not an answer; its elements are answers).
- Elements: registry rows of key `project:<name>` (`value: list` semantics), written by `record`; `record_problems` accepts the key only
  when `kinds()` holds the name; scope from the kind.
- `contents(root, role=None) -> list[{"name", "says", "path", "elements"}]`: one line per factory list row with live elements and per project
  kind (`path` = `qa-factory/records/project-knowledge.json` or `qa-factory/knowledge.json`); `role` filters by `needed_by` (phase 5 wires briefs).
  A reference, never the values beyond a count (FR-15).

**The conductor's door (K2) — `remember(root, *, key, environment, element, value, words, scope, story, condition="", supersedes=MISSING,
by="conductor", task_root)`**: for a registry-stored key (or `project:<kind>`) -> `record(state=known, source=person)`. For a config-stored key
(`store: config:<path>`) -> FIRST `project_decisions.upsert` (field ref = the JSON pointer of the path; scope project; owner user) and
`project_decisions.resolve` with `{pointer: value}` (the recorded writer, receipt with `before` — C2), THEN a registry row `known` with the
provenance and condition (value `null`; the value's carrier is the config). A list-element pointer through `environments[]` resolves the stand
by NAME to its index at write time (`environment(name)`); a stand that is not found or is twinned -> refused, nothing written. Order and
partial failure: resolve fails -> nothing written; resolve succeeds and `record` refuses (e.g. a lock timeout) -> the config holds the value,
the command exits 2 and says "the settings hold it; the record of earlier answers does not — run the same command again" (config first,
registry second: today's `account` order, t-2142).
CLI: `project_knowledge.py remember --task T --key K [--stand N] [--element E] (--value-file F | --not-needed) --scope project|stand|story
[--condition-file C] [--supersedes PK-n] --words-file W`; `--scope story` = the story-only answer: the command refuses and names the door
`waiver.py --task <T> --stage <S> --block "<block>" --words-file <file>` (a story-only answer is a waiver, never a registry row — today's
`record_problems` text :520). `project_knowledge.py kind --task T --name N --says-file F --scope project|stand [--needed-by r1,r2]
--words-file W`. `project_knowledge.py show --contents` prints `contents()`.

## §4 Edges (behaviour + the invariant each protects)

| edge | behaviour | invariant |
|---|---|---|
| legacy registry row (no `supersedes`) | fork F1 (a): supersedes the subject's previous live row (later-wins as today) | no existing project's registry turns into conflicts by the upgrade |
| phase-2 row and a legacy row on one subject | the phase-2 row's `supersedes` decides; a legacy row after a phase-2 row (impossible: phase-2 code writes the key) | — |
| `supersedes` names a revoked row | allowed (the writer read it before it was revoked); heads are computed over live rows only | a revoke never blocks a person's new answer |
| `supersedes` names a row of another subject / an unknown id | refused, nothing written, door `show` | a link never ties two facts together |
| revoke of the only head | subject `unknown` (F2 a); the predecessor stays superseded | "ask again" means ask again; an old answer never comes back by itself |
| revoke while a conflict | the remaining head(s) decide; one left -> that one | a conflict exits by revoke or by a superseding answer (AR-25) |
| `condition` empty / blank / None | stored `""` = no condition | an unconditional answer is unchanged by the field (PK-A test) |
| `condition` very long / with line breaks / non-Latin | stored whole; shown through `brief_pack.person_words_whole` where printed | the person's words are never cut silently (FR-8) |
| `not_needed` with a condition | never suppresses a question in `fact()` (step 3 skips it) — the row is handed to the conductor/role with the question | code never decides that a condition applies (P27) |
| `asked` row in a `no_trace` story | `_refuse_no_trace` refuses it (P8); the driver still does not re-ask in this story (its hash memory, F-10) | an experiment leaves no trace; FR-7 still holds within it |
| `asked` row, then the story ends unanswered | next story: `asked_before` -> asked again with one line "asked in <story> on <date>, not answered then" | a question asked again changes its text (FR-7) and the unanswered state has a way out (AR-25) |
| two stories `asked` the same fact | two `asked` rows; the later supersedes the earlier only if it read it (it does: `need_fact` passes the head) | — |
| catalogue row with `ask_when: first_need` but no `question` / `while_unknown` | K1 data-join row red naming the key; at runtime `need_fact` returns `unknown` with problem and the caller keeps today's behaviour, no question | a seam question is never built without its price key and its unknown-mode |
| `while_unknown: default` without `safe_direction` | the same data-join row red | the default always names why it is the safe side (C10) |
| `holds: none` on a row, Person kind is a gate | `deferrable` false (gates are the stop itself) | the D.1 invariant: only a knowledge Person with the row's `holds: none` passes the first line |
| `no_hold` set on a Person without `fact_key` (after K5) | falls through to the `holds` test -> asked at once | a flag set by mistake never withholds a question |
| knowledge.json absent (temporal: before the first `kind`) | `kinds()` `{}`; `project:<x>` refused "the project defines no kind named <x>; create it with `project_knowledge.py kind`"; `contents()` lists factory lists only | absent ≠ unreadable |
| knowledge.json unreadable / not an object / other schema | `kinds()` `{}` + problem; `record_kind` refuses to write over it (door: `show`); `project:<x>` refused naming the problem | a damaged file is never overwritten (FR-41) |
| kind name twins by case / blank | refused | one kind, one name |
| `remember` on a config key whose stand is twinned / absent / list not a list | refused, nothing written | a stand fact never lands on a stand nobody named (phase 1 edge kept) |
| `remember` resolve OK, registry write fails | exit 2, the line names the half written | config first, registry second; the person is told what holds |
| `remember --scope story` | refused with the waiver door | a story-only answer is the story's (waiver), never the project's |
| `remember` / `kind` by a role | guard refusal (K6) with the door "put it in your digest; the conductor records it" | one writer of a person's words (AR-14, P15) |
| the conductor edits `config.json` by hand | not refused (F-22, the main session is never refused); `restore_config` reverts it at story end unless it was a recorded write; fork F5 | a fact meant to last goes through the door |
| `remember` in a `no_trace` story | refused (existing `_refuse_no_trace`), door: the story's words (waiver) | P8 |
| a placeholder config value (`"not known"`) | `fact()` with the caller's `known=False` -> `unknown` (F9 a) | a placeholder never reads as an answer |
| catalogue damaged | `fact()` `unknown`, `need_fact` returns unknown with problem, no question built, caller keeps today's path; `record` refuses with the damage sentence (phase 1) | a damaged table never asks a wrong question or records a fact |
| phase-1 node f not merged (temporal) | K1 does not start (F10 a) | the plan's order 1 -> 2 |
| K3 merged, K5 not (temporal) | the kind tuple stays in `deferrable` beside the catalogue road; TR3-10 Persons carry no `fact_key` and keep their road | no world where the two S6 questions lose their deferral |
| K5 merged | the tuple is gone; the two Persons carry `fact_key`; their rows say `holds: none` | one road |
| an open TR3-10 DD row from before K5 (`/manual/accounts_way` open) | read as `asked_before` (story unknown): asked again in the next story with the "asked earlier" line; K5's first ask closes nothing in `factory-backlog.md` (the DD row stays; the answer resolves it through `remember`, which `upsert`s the same refs and gets the open row back, F-19 :421-423) | the old open row is reused, never duplicated |

## §5 Nodes (each: files, functions, behaviour, tests, owns)

Every test is a row in an EXISTING keep file (F-25); no new test file; no source pin; no in-test negative control; mutation probes are one-off
runs in the builder's report (a reverted branch -> the named row red), never committed. Red-first: each node's FIRST commit adds its rows red.

DoD for every node: the node's rows green; the verification run, attached verbatim:
`python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <the node's owns>` and
`python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang`; slow files (`test_story_run_*`, `test_judgment_census.py`,
`test_install_paths.py`) are judged by CI only. A keep file red at quarantine entry is reported by row id; the node is judged on its own rows.
Package commits carry `architecture: AR-n -- <how kept>` and `judgment:` lines. STOP and return on: an unlisted ratchet raise; a test
expectation that must change to pass other than the ones named in the node; a reader whose error direction cannot be kept.
Hot files, named per node with functions: `project_knowledge.py` (K1 then K2, serial); the driver set (story_run lineage: `driver_core.py`,
`driver_dialog.py`, `driver_machine.py` — K3; `driver_dialog.py` `deferrable`, `driver_stage_s6.py`, `driver_dispatch.py` — K5 after K3);
`story_run.py`, `hooklib.py`, `stage_guard.py`, `gate_preflight.py`, `controller.py`, `brief_pack.py` — NOT written by any node of this spec.

### K1 — registry core (plan 2.1, PK2-1, PK2-2; C1, C9, C10)
- `project_knowledge.py`: `_derive_keys` (every row with `scope`; `compare` default `exact`), `STATES`/`ASKED`, `_usable` (asked rows;
  stand not_needed), `_latest` -> heads helper `_heads(rows, key, environment, element)` (used by `state`, `subjects`, `roster`, `record`),
  `state` (+`conflicts`, `condition`), `value` (+`conflicts`, `condition`), new `fact`, `record_problems` (§3), `record` (`condition`,
  `supersedes`). `notice_from_handoff` is NOT changed (PK2-18 neighbour; fork F3).
- `references/config-keys.json` section `knowledge`: §2 fields on the listed rows; the three TR3-10 rows added if absent (with `store`
  `config:<path>`, `needed_by` the readers `config_contract.py:walk_supply` and the S6 raise functions).
- `design/state-exits.md`: one row for `asked` (reversed by a later answer row or `revoke`; exit proof `test_project_knowledge.py`).
- Tests in `test_project_knowledge.py` (register): `test_fact_toward_asking` — one parameterised set over §3's adversarial inputs (ids = the
  input); `test_fact_steps` — known / not_needed / asked_here / asked_before / unknown, each from a minimal registry; `test_condition_carried`
  (PK2-1: a row with a condition reaches `state`, `value`, `fact`, `roster` with it; a row without is unchanged); `test_supersede_and_conflict`
  (PK2-2 table: replace with `supersedes` -> one head; two rows without a link -> both heads, `unknown`, `conflicts`; two writes through two
  threads under the lock -> both saved; read after revoke of the head -> `unknown`; legacy rows -> later wins (F1 a)); `test_catalogue_seam_join`
  (data join: every `first_need` row has `question` (a key present in question-prices.json), `while_unknown`, `scope`, `person_class`
  (a class in person-owned.json), `default` rows have `safe_direction`). Existing phase-0 rows stay green unchanged.
- Mutation probes (report only): `_heads` replaced by later-wins -> conflict rows red; step 3 not skipping a conditional `not_needed` -> its
  adversarial row red.
- given: this spec; P\design\factory-rules.md; plans\builder-rules.md; P\design\architecture.md (AR-13, AR-14, AR-25, AR-28)
- owns: `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\project_knowledge.py` (functions listed),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\references\config-keys.json` (`knowledge` section only),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\design\state-exits.md` (one row),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_project_knowledge.py`,
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json` (rows of altered units only, class unchanged),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\of3-2-k1.md`
- depends on: OF3-1 part f merged (F10); then nothing.

### K2 — project kinds, contents, the conductor's door (plan 2.5, 2.6; C2)
- `project_knowledge.py`: new `kinds`, `kind_problems`, `record_kind`, `contents`, `remember`; CLI `cmd_kind`, `cmd_remember`, `show
  --contents`; `record_problems` accepts `project:<kind>` (the one shared function with K1 — serial after K1).
- `references/install-paths.json`: rule `{"glob": "qa-factory/knowledge.json", "class": "carried", "reader": "project_knowledge.py", "note":
  "the kinds of knowledge a project defined itself (plan 2.6), with the person's words: committed, carried byte for byte"}` after the
  `config.json` row.
- Tests in `test_project_knowledge.py`: **first, red-first, the C2 row** `test_remembered_fact_survives_restore` — a story's window opened
  (`restore_config` snapshot taken as the story start does), `remember` of a config-stored key (`manual.data_way.may`), then
  `config_contract.restore_config` -> the value is still in `config.json` and the registry row exists; the same value written by a hand edit
  is reverted (contrast row, both from one world); `test_kinds_edges` (absent, unreadable, twin name, empty says, unknown role, replace keeps
  history); `test_project_elements` (add element, revoke element, list never closed: a new element after others is added, not replacing);
  `test_contents_lines` (factory list + project kind + role filter + empty -> the "no kinds" line); `test_remember_roads` (registry key;
  config key; `--scope story` refused with the waiver door; twinned stand refused; config written + registry refused -> exit 2 line).
  `test_install_paths.py` (CI): row "`qa-factory/knowledge.json` is carried, its reader exists". `test_words_doors.py`: rows for `remember`
  and `kind` (empty words -> `door()`).
- owns: `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\project_knowledge.py` (functions listed),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\references\install-paths.json` (one rule),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_project_knowledge.py`,
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_install_paths.py` (one row),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_words_doors.py` (two rows),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json` (`kind_problems` row, `shape`),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\of3-2-k2.md`
- depends on: K1.

### K3 — the seam's ask half in the driver (plan 2.1/2.3/2.4; C7, C8, C9)
- `driver_core.Person`: new attributes `fact_key = ""`, `fact_env = ""`, `fact_element = ""`, `no_hold = False` (formalises the ad-hoc
  attribute TR3-10 sets; F-13), with the comment style of :208-233.
- `driver_dialog.py`: new `DriverDialog.need_fact(self, key, *, stage, environment="", element="", holds=(), known=None) -> dict`:
  1. `PK.fact(self.project, key, environment, element, story=<this story id>, known=known)`;
  2. `known` / `not_needed` -> return it (`not_needed` and an earlier `known` from the registry print ONE line through `say_once`:
     "acting on your answer of <date> (<story>): <words, 160 chars>" — the generalisation of `acting_line`, project_knowledge.py:662);
  3. `asked_here` -> return `{"step": "asked_here", "while_unknown"}`, no question (FR-7);
  4. `unknown` / `asked_before` with the row's `ask_when == "first_need"` -> build the Person: kind `knowledge`, text =
     `closed_question(row.question, lead, options)` where lead = the row's question lead (K5 passes the TR3-10 texts) plus, for
     `asked_before`, the line "I asked this in <story> on <date> and got no answer then."; `fact_key`/`fact_env`/`fact_element`; `why_person`
     = `person_class`; `holds` = the caller's; `no_hold` = (row `holds == "none"`); `offered` = the closed tokens of §6 F4 that fit the row's
     scope (`answer` `closed`/`both`); write the `asked` row via `PK.record(state=asked, by=driver, source=person, words="", supersedes=<head
     read in 1>)` — refusals (no_trace, lock) are one stderr line and the question is still asked; raise the Person (`# remains:` comment);
  5. no `first_need` or no row -> return `{"step": "unknown", "while_unknown", "problem"}` (the caller keeps today's behaviour).
  `deferrable` first line becomes: `if getattr(person, "no_hold", False) and (person.kind in ("walk_supply", "data_change") or
  (getattr(person, "fact_key", "") and self._fact_holds_none(person.fact_key))): return True` — the tuple stays until K5 (temporal edge).
- `driver_machine.py` `take_answer` (UNVERIFIED function home: driver_machine.py around :3330 writes `question_sha`; K3 confirms by
  grep `def take_answer`): a branch keyed on `asked.kind == "knowledge"` (set by `ask()` from the Person; POSITION: before the generic token
  branch, after the gate branches, so a gate answer is never read as a knowledge answer): an offered token -> `PK.record` (`not_needed`, scope
  per token; `not needed now` -> `waiver.py --remark` with the words, no registry row); any other words -> the conductor with the words (the
  existing free-answer road), `asked` stays.
- `references/fixtures`: `scripts/tests/fixtures/driver-layers.json` rows for `need_fact`, `_fact_holds_none` (home `driver_dialog`).
- Tests: `test_human_questions.py` (table) rows — a knowledge question passes `human_text.problems`; asked again in a later story its body
  hash differs (the "asked earlier" line); it carries `why_person`; `test_story_run_deferred.py` (CI) row — a knowledge Person with
  `holds: none` is deferred and asked before gate B; the same `no_hold` on a gate Person is asked at once; `test_project_knowledge.py` is
  NOT owned here (K1/K2 own it).
- owns: `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\driver_core.py` (`Person.__init__` only),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\driver_dialog.py` (`need_fact`, `_fact_holds_none`, `deferrable` first line),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\driver_machine.py` (`take_answer` knowledge branch only),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\driver-layers.json` (rows),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_human_questions.py`,
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_story_run_deferred.py`,
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\of3-2-k3.md`
- depends on: K1. Parallel with K2 (no shared file).

### K4 — the conductor's door and the scope rule (plan 2.4, 2.5; В3)
- `references/conductor-actions.json` `actions`: one row `{"id": "remember", "says": "the person says, in other words, that something holds
  for the project or for a stand from now on (`remember`, or an answer to a knowledge question in their own words)", "run":
  "project_knowledge.py remember --task <T> --key <catalogue key or project:<kind>> [--stand <name>] [--element <e>] --value-file <file> |
  --not-needed --scope project|stand [--condition-file <file>] [--supersedes PK-<n>] --words-file <file>; a new kind first:
  project_knowledge.py kind ...; YOU decide the scope from their words: narrow on doubt (this story only = waiver, not this command); then say ONE
  line: `recorded as a rule of <the project|stand X>: <their words>; to undo, say so`; a conflict the command reports is settled by asking the
  person through a knowledge question, never by picking"}`.
- `references/conductor.md`: one paragraph "A person's lasting answer" (В3; scope judgment; aloud line; revoke door; never a hand edit of
  `config.json` for a lasting fact — fork F5 (a)).
- `references/question-prices.json`: key `knowledge.first_need` with the options of F4 (each priced: factory `record`, person `none`,
  delivery `unchanged`; `not needed` carries `unverified: whatever only that fact would have shown`).
- Tests: `test_conductor_doors.py` (keep) row — the `remember` action names a command the CLI accepts (UNVERIFIED that this file checks rows
  against CLIs: K4 reads its header first; if it does not, the row goes to `test_project_knowledge.py` via K2 — then K4 hands the row text to
  the Lead, no write there); `test_human_questions.py` is NOT owned (K3 owns it): the price key is checked by the existing price-table test
  (UNVERIFIED which; K4 names it from `grep question-prices` with a positive control).
- owns: `C:\QAFactory\forge-repo\ai-packages\qa-factory\references\conductor-actions.json` (one row),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\references\conductor.md` (one paragraph),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\references\question-prices.json` (one key),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_conductor_doors.py`,
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\of3-2-k4.md`
- depends on: K2 (the CLI exists). Runs on F4's recommended tokens.

### K5 — TR3-10 on the seam (В4; AR-15)
- `driver_stage_s6.py`: `walk_supply_raise` calls `need_fact("manual.accounts_way", ..., known=accounts["known"])` /
  `need_fact("manual.data_way.may", ..., known=data["may_known"])` with the existing texts as leads; `walk_ask_once` and `walk_asked` are
  removed (their roles: the `asked` row and `asked_here`); the `<kind>_asked` state keys stop being written (an old story that holds one is
  read as `asked_here` once, then ignored — UNVERIFIED reader set: K5 greps `walk_supply_asked|data_change_asked` with a positive control).
- `driver_dispatch.py`: `walk_supply_person`, `data_change_person` set `fact_key` and drop `no_hold` kind dependence; `_resolve_decision_row`
  callers for these two kinds go through `PK.remember` (which resolves the reused open DD row, F-19 :421-423) (UNVERIFIED line numbers
  :3271-3412; K5 reads them first).
- `driver_dialog.deferrable`: the tuple `("walk_supply", "data_change")` deleted (after K3).
- `references/conductor-actions.json`: rows `walk_supply_way`, `walk_account_words`, `data_change_words` (:36-38) say
  `project_knowledge.py remember ...` (MERGE ON WRITE rule kept in the row text) instead of `project_decisions.py resolve --id <DD-n>`.
- `design/state-exits.md:204-205`: the two rows restated on the `asked` state.
- Tests: `test_walk_supply.py` (gate_named) — its existing rows rewritten where the road changed (named expected edits: every row asserting
  a `project_decisions add` call or `<kind>_asked` key), plus rows: "answered once in story 1 -> story 2 is not asked"; "asked, not answered in
  story 1 -> story 2 asks with the 'asked earlier' line"; "an open legacy DD row -> asked again, the same DD row resolved".
- owns: `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\driver_stage_s6.py` (`walk_supply_raise`, `walk_ask_once`, `walk_asked`),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\driver_dispatch.py` (`walk_supply_person`, `data_change_person`, the two answer
  handlers), `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\driver_dialog.py` (`deferrable` first line only),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\references\conductor-actions.json` (three rows),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\design\state-exits.md` (two rows),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_walk_supply.py`,
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\of3-2-k5.md`
- depends on: K3 and K4.

### K6 — guard: approvals and the new write commands (B-294 (a); plan's "писатель фактов один")
- `guard_pre_tool.py`: `_SANCTIONED_CONFIG_SCRIPTS["config_contract.py"]` from `()` (any argument) to a role-refused shape for
  `--record-approval` and `--apply`; a role running `onboard_apply.py --apply` refused (B-294 (b), role side); the regex :1787 gains
  `remember|kind`. Refusal text names what is wrong and the door: "only the onboarding records an approval / only the conductor records a
  person's answer; put the point in your digest". Main session: unchanged (F-22).
- Tests: `test_guard_write_owners.py` rows (role `config_contract.py --record-approval` refused; `--show`-class read flags pass (K6 lists
  the read flags from `config_contract.py --help` and attaches it); role `onboard_apply.py --apply` refused; main session passes);
  `test_guard_project_knowledge.py` rows (`remember`, `kind` refused to a role; `show --contents` passes).
- owns: `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\guard_pre_tool.py` (`_SANCTIONED_CONFIG_SCRIPTS` and its check; the regex
  at :1787 and its refusal text :1740-1745),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_guard_write_owners.py`,
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_guard_project_knowledge.py`,
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\of3-2-k6.md`
- depends on: nothing (the regex may name `remember|kind` before K2 merges: a refusal of a command that does not exist yet costs nothing).
  Queue: `очередь: OF3-2/K6 → project-knowledge/2 PK2-9` (same file, PK2-9 rewrites the same regex as subcommand-anywhere).

### K7 — the map axis "memory of a person's answer" (§7 C3)
- `docs/SIBLING_MAP.md`: axis 37 — survivor `project_knowledge` (`state`/`fact`/`record`/`remember`) <-> its twins named in C3 and found
  here: `environment_record` (`accept always`, until phase 3.2), `stand_identity` (phase 3.2), `remembered_answers` (onboarding), 
  `asked_until_answered`, report adaptations RA-n, `waiver --carry-from`, `obligations.md`, the confirmed default stand, the driver's
  in-story hash memory (`already_answered`, stays by design, C7); each line names its phase or "stays — why".
- Doc dispatch witness (CLAUDE.md rule 11 DOC-DISPATCH): key-presence script with the keys quoted from this item before the run, full source in
  the report, a negative control.
- owns: `C:\QAFactory\forge-repo\docs\SIBLING_MAP.md`
- depends on: nothing; parallel.

### Order and parallel groups
G1 (start): K1 (after OF3-1f), K6, K7 — parallel. G2: K2 ‖ K3 (both after K1). G3: K4 (after K2). G4: K5 (after K3, K4).
Disjointness: `project_knowledge.py`, `test_project_knowledge.py`, `judgment-census.json` — K1 then K2 (serial); `driver_dialog.py` — K3 then K5
(serial); `conductor-actions.json` — K4 then K5; `state-exits.md` — K1 then K5; `guard_pre_tool.py` — K6 only. Writers at once: at most 3.
edges: §4. non-goals: §5 «Not in this phase». handoff: builder report + diff (+ the census of every new reader/writer site).
siblings: axis 34 (one road: the TR3-10 tuple folded, K5); axis 5 (stage twins: the S6 supply questions are the only consumer in phase 2;
gate A/B consumers are phase 3); axis 16/13 (one reader); new axis 37 (K7); axis 35 (side keys unchanged — `known` only).

### Mapping: every plan sub-item and §7 correction -> a node or "not in this phase"

| item | where |
|---|---|
| 2.1 `need()` with the order of §2.3 | K1 (`fact`, pure read, C9) + K3 (`need_fact`, ask half) |
| 2.1 state of a fact in the registry ("project_decisions обобщаются") | K1 on the phase-0 registry (C1: `project_decisions` stays the deferred-decisions registry) |
| 2.2 B-296 | not in this phase — dropped by C1 (stale after HF8-9); the real gaps (element add, rows by name) are phase 0's rows + K2's elements |
| 2.3 question carries the fact key; "already answered" by key | K3 (`fact_key`, cross-story memory via the registry); the in-story hash stays (C7) |
| 2.4 scope variants; record, aloud line, revoke common | K3 (tokens), K4 (conductor scope, aloud line), K1 (revoke semantics) |
| 2.5 conductor's "remember" door | K2 (`remember`), K4 (action row, conductor.md) |
| 2.6 lists with provenance; project kinds; contents; install-paths | K1 (`value: list`), K2 (kinds, elements, contents, install row) |
| Absorbs TR3-10 | K5 |
| Absorbs B-294 | K6 for (a) and the role side of (b); (c) audit of approvals without a person ref — not in this phase: the approvals journal is onboarding's (C9) and its audit lands with phase 4's readiness change |
| Absorbs release-next "role edits config past its owner" | roles: already refused by the guard (t-110, F-22 comment) + K6 closes the approval hole; conductor: K4 door + fork F5 |
| PK2-1 | K1 (`condition`) |
| PK2-2 | K1 (`supersedes`, heads, conflict, concurrent writes, revoke) |
| PK2-18 (neighbour) | not absorbed — fork F3 |
| C1 | K1 (built on phase 0's ER-helper registry) |
| C2 | K2 first test |
| C3 | K7 |
| C5 | §2 (fields in `config-keys.json`) |
| C7 | K3 (cross-story memory, in-story hash kept) |
| C8 | K3 (no-hold by catalogue) + K5 (TR3-10 moved) |
| C9 | K1 (`fact` pure) / K3 (driver asks and writes) |
| C10 | §2 (`safe_direction`, no `in_turn`), §3 (`unreachable` not stored) |
| C13 / В8 (a role-noticed element is unconfirmed) | already the `noticed_unconfirmed` state (phase 0); K2's `project:<kind>` elements accept `source: role, state: noticed_unconfirmed`; the role-side wiring is phase 5.1а |
| C14 (each comparison arm its own knowledge snapshot; `no_trace` closes knowledge writers) | writers: `_refuse_no_trace` covers `record`, `record_kind`, `remember` (K1/K2); per-arm snapshot — not in this phase: it is how a comparison run is prepared (`docs/RUNBOOK.md`, experiments), queued as a finding (§7) |
| 2.x witness "tests of the seam per state and per `while_unknown`; unknown never gives a pass" | K1 `test_fact_steps` + `test_fact_toward_asking`; K3 rows; `while_unknown` `gap`/`hold` have no phase-2 consumer — their rows are data-join only (the consumers come in phase 3) |

**Not in this phase:** phases 3-6 (gate A keys, stand card, stand choice, `product.roles`/`accounts_by_role` growth from stories, onboarding,
inject-map/briefs, S9 fold, metrics, live proofs); phase 1 part f; `derive` (F8); moving `accept always` onto the registry (phase 3.2);
PK2-11/PK2-19 (no_trace class, own nodes); PK2-12/PK2-13 (helpers, own nodes); PK2-9 (guard form, queued after K6).

## §6 Forks

| id | question | options and cost | recommendation | whose |
|---|---|---|---|---|
| F1 | Legacy registry rows (no `supersedes`) | (a) read as superseding the previous live row (today's later-wins); cost: two legacy rows that really disagreed stay "later wins" — measure M-2 first. (b) treat as unlinked heads -> every subject with two legacy rows becomes a conflict and is asked again; cost: repeated questions on every project with history | (a) | Lead |
| F2 | Revoking the only head: does the superseded answer come back? | (a) no -> `unknown`, asked again; cost: one question after a revoke. (b) yes; cost: an answer the person replaced revives silently | (a) | Lead (owner may overrule: what a person experiences) |
| F3 | PK2-18 (check-then-write guard for `noticed` in `record`) | (a) separate node right after K1 (same file, serial), as its batch row says; (b) fold into K1 (the heads helper is the same check) | (a); K1's `_heads` is written so PK2-18 calls it | Lead |
| F4 | The closed tokens a knowledge question shows | (a) `not needed now` (this story; a remark), `not needed for this stand` (stand rows), `not needed for the project` (project rows) — value answers are words; (b) reuse `accept` / `accept always` words; cost: those mean "stays blocked" on stand-gap cards, a second meaning; (c) only words, no tokens; cost: every answer costs a conductor session | (a) | OWNER (what a person is shown, P9) |
| F5 | The conductor's hand edit of `config.json` (release-next finding) | (a) door + conductor.md rule + detector: `restore_config`'s `reverted` pointers at story end become one finding line "a setting changed by hand in this story was given back: <pointer>; record it with `remember` if it should last" (a later node; cost: discipline until then); (b) refuse the main session's Write/Edit to config.json; cost: reverses the standing guard design (F-22) and blocks onboarding's own edits | (a); the detector line is queued as N-q1 (§7) | Lead |
| F6 | B-294 (c) audit | (a) phase 4 with the approvals journal; (b) here; cost: a new detector in `audit_factory.py` (not in any owns, hot for streams) | (a) | Lead |
| F7 | Where `asked` is written when the question is deferred | (a) at raise time (K3), even if deferred until gate B; (b) when shown; cost (b): a story that stops before gate B never records it, so the next story says nothing about the earlier ask | (a) | Lead |
| F8 | `derive` in phase 2 | (a) not added: no phase-2 row has a deriver (AR-22); the seam's step slot is stated for phase 4.2; (b) add the field and an empty map; cost: a field with no producer | (a) | Lead |
| F9 | Who decides `known` for a fact whose config holds a placeholder (`"not known"`) | (a) the caller passes `known` from the fact's own reader (`config_contract.walk_supply`); `fact()` never overrides it toward known; (b) a catalogue list `unknown_values` read by `value()`; cost: a second reader of the same rule (AR-13) and dict-valued facts need a sub-path | (a) | Lead |
| F10 | Start K1 before phase-1 node f merges? | (a) wait (the plan's order 1 -> 2 is mandatory, and both write `config-keys.json` rows on the same lines); (b) run with D-0048 (f: `needed_by` values; K1: new fields) and let the later merge resolve; cost: conflicts on one-line JSON rows | (a) | Lead |
| F11 | `knowledge.json` home | (a) `qa-factory/knowledge.json` (the plan's word, beside `config.json`: a definition table); (b) `qa-factory/records/knowledge.json` (with the other carried records) | (a) | Lead (technical; closed by me as small, reversible) |

Every node runs on the recommendations above until answered.

## §7 Queue entries and findings (the coordinator places them)

| id | what | owns (prefix P) | test | when |
|---|---|---|---|---|
| N-q1 | F5 (a) detector: `restore_config`'s reverted pointers of a story reach the report as one finding line naming `remember` | P\scripts\config_contract.py (`restore_config` caller side) or the report writer (designer names on drafting) | a row: a hand-edited pointer reverted -> the line; a recorded write kept -> no line | after K4; after OF1-2 (config_contract.py) |
| N-q2 | C14 per-arm knowledge snapshot for comparison runs (P8) | `docs/RUNBOOK.md` §9 procedure + `experiments/measurers/run_headless.py` (designer confirms) | a doc key-presence run, or a measurer test | before the next comparison run |
| N-q3 | PK2-18 if F3 (a) | P\scripts\project_knowledge.py (`record`, `notice_from_handoff`) | the finding's row | right after K1 |

Announcement: `очередь: onboarding-forge/3 OF3-2/K6 → project-knowledge/2 PK2-9` in both batch files; stream owners of the driver set are told
that K3/K5 touch `driver_core.py`, `driver_dialog.py`, `driver_machine.py`, `driver_stage_s6.py`, `driver_dispatch.py` (functions listed).

## Plan text vs section 7 (and vs the repo) — for the Lead to correct stale rows

| where | stale text | the later word / the fact | carrier |
|---|---|---|---|
| plan §4 2.1; batch-3 OF3-2 row | "`project_decisions.upsert / resolve` обобщаются: строка на ключ + окружение" | C1: the registry stands on `environment_record` helpers (done in phase 0: `project_knowledge.py`), `project_decisions` stays the deferred-decisions registry | plan :330; project_knowledge.py:1-6 |
| plan §4 2.2; batch-3 OF3-2 row | "B-296: реестр умеет указатель на элемент списка" | C1: dropped (stale after HF8-9) | plan :330 |
| plan §2.1, §2.6 table, §6 «решила сама»; batch-3 OF3-1 and OF3-4 «Пишет в» | `references/project-knowledge.json` (new table) | C5: section `knowledge` of `config-keys.json` (done in phase 1, :705) | plan :338 |
| plan §2.3 | one `need(key, env, story)` that reads and asks | C9: pure read `state()` (here `fact()`); asking and writing on the driver/conductor side | plan :339 |
| plan §2.3 p.4 | "вопрос к ближайшей остановке ... механика t-1957 §3.6 п.3, вынесенная из ходока" | C8: did not exist; since then TR3-10 built it for two kinds only (driver_dialog.py:456) — K3/K5 generalise | plan :340 |
| plan §1, §4 2.3 | "у вопроса нет постоянного ключа ... story_run.py:4387" | C7: 28 questions have a key; what is missing is memory BETWEEN stories; the hash now lives in driver_dialog.py:381-392 | plan :347 |
| plan §2.1 `while_unknown` values; §2.2 states | `in_turn` a general value; `unreachable` a stored state | C10: `in_turn` removed; `default` names its safe direction; `unreachable` run-scoped | plan :343 |
| plan §2.4 table "проект, всегда -> config.json" | a direct write | C2: only as a recorded writer (`project_decisions.resolve` receipt) | plan :331 |
| plan §4 «Поглощает: TR3-10 (первый потребитель шва, а не своим механизмом)» | as if TR3-10 waits | В4 second branch: TR3-10 is «принято» with its own road; phase 2 moves it (K5) | batch-3-parallelnost.md:31 |
| plan §7 C3 | the axis "память ответа человека" is created by the phase-0 commit | not in `docs/SIBLING_MAP.md` (axes 1-36) -> K7 | SIBLING_MAP headings |
| plan §2.1 field `about` | `about: project · environment` | the existing field is `scope: project · stand` (phase 0/1) — same fact, kept as `scope` | config-keys.json:706-710 |
| plan §3.1 / batch-3 OF3-3 (3.4а) | `environments[].accounts_by_role` | the key is `environments.credentials_by_role` (phase 3's to rename or keep) | config-keys.json:707; project_knowledge.py:42 |
| batch-3 OF3-1 status | «ожидает» | parts a-e on main, part f not (brief; not re-verified by me) | brief |
| batch-3 OF3-2 «Поглощает» release-next finding — «место не найдено» | no place | `plans/piles/release-next/findings/20261102-rol-pravit-konfig-proekta-v-obhod-hozyaina.md` | Grep this round |
| B-294 finding line numbers | guard :1359/:1656/:1700 | the sanction table is now guard_pre_tool.py:1900-1901 | Read this round |

## Small choices I closed
`scope` kept for the plan's `about`; `ASKED = "asked"`; heads helper name `_heads`; `fact()` step names; project keys namespaced
`project:<name>`; kind history kept under `history` in `knowledge.json`; `unreachable` kept in the driver's own state (`state/driver-state.json`
key `knowledge_unreachable`, run-scoped, D-0043) — no phase-2 producer yet beyond the slot, so K3 writes it only when a caller reports a probe
said "unreachable" (none in phase 2: the slot is stated, not built — K3 does NOT add it; recorded here for phase 3); TR3-10 `person_class`
values (`access`, `team_agreement`); price key `knowledge.first_need`; the aloud line's wording; the "asked earlier" line's wording; changelog
fragment per node; `knowledge.json` at `qa-factory/` (F11).

## Contradictions and notes for the Lead (not widened)
- Phase 0 promised axis C3 in its commit; it is absent (K7 fixes).
- `test_judgment_census.py` and `test_install_paths.py` are slow (t-2142:1059): CI only, never a local witness.
- The plan's witness wording "негативный контроль — неизвестный факт не даёт «прошло»" is a behaviour row here (`test_fact_toward_asking`),
  not an in-test negative control (docs/TESTING.md table).
- `while_unknown: gap` and `hold` have no consumer in phase 2 (only TR3-10's `default`); their consumers are phase 3 (gate A keys hold cases).
- Phase 0's `acting_line` serves accounts only; K3's line is its generalisation — `acting_line` stays for its gate A caller until phase 3.

## Trail
Read whole: plans/project-knowledge-plan.md; batch-3-znaniya-o-proekte-fazy-1-6.md; t-129-of3-1-knowledge-catalog.md; project-knowledge
batch-2 file; references/conductor-actions.json; references/install-paths.json; finding 20261111-zapis-zamechennoj-roli...; finding
20261102-rol-pravit-konfig...; finding B-294-odobreniya...
Read in part: project_knowledge.py :1-720; driver_dialog.py :1-60, :255-540; driver_core.py :185-274; driver_runner.py :1195-1244;
driver_stage_s6.py :1380-1479; environment_record.py :1-120, :300-369; stand_gaps.py :1235-1284; config_contract.py :2350-2499; project_decisions.py
:375-529; guard_pre_tool.py :1890-1929; question-vocabulary.json :20-49; question-prices.json :1-30; architecture.md :46-67, :134-280;
finding 20261111-chego-ne-hvataet... :1-32; t-2142 spec :1005-1089; docs/TESTING.md :36-135.
Greps (with controls): `def ` in project_knowledge.py / question_register.py / project_decisions.py; `already_answered|question_body_sha` over
scripts; `closed_question|deferrable|Person|no_move` defs; `accounts_way|data_way|no_hold|walk_supply` over the package; `knowledge` rows of
config-keys.json; test-layers.json row names (keep/quarantine boundary :35/:7023); `project_knowledge` / `record.approval|config_contract` in
guard_pre_tool.py (case-insensitive; control :1900); SIBLING_MAP headings; person-owned.json ids; fixtures driver-questions.jsonl kinds;
`approval_ref` in onboard_apply.py; TR3-10 row; PK2 rows in the project-knowledge README.
Not verified (UNVERIFIED in the text): exact 78 rows; `take_answer` home; driver_dispatch.py :3271-3412 internals; which price keys the S6
questions use; whether `test_conductor_doors.py` checks rows against CLIs; whether `references/artifact-writers.json` lists records; whether
`references/stages.json` lists roles by name; story_step.py:560 detector; OF3-1 parts a-e on main.
needed beyond the manifest: scripts/project_knowledge.py, driver_dialog.py, driver_core.py, driver_runner.py, driver_stage_s6.py,
environment_record.py, stand_gaps.py, config_contract.py, project_decisions.py, guard_pre_tool.py, onboard_apply.py (grep);
references/conductor-actions.json, install-paths.json, question-vocabulary.json, question-prices.json, person-owned.json;
docs/tasks/specs/t-2142-project-knowledge-phase0.md; plans/piles/release-next/findings/20261102-rol-pravit-konfig-proekta-v-obhod-hozyaina.md;
plans/piles/gates-and-words/findings/B-294-...; plans/piles/thinking-roles/batch-3-parallelnost.md (grep).

## Lead decisions on the forks (Lead, Fable, 13.11.2026 — "решила сама", the owner may overrule)

- F1 (a), F2 (a), F3 (a) (PK2-18 stays its own node right after K1), F5 (a), F6 (a), F7 (a), F8 (a), F9 (a), F10 (a) (K1 waits for
  the phase-1 node f), F11 (a): the designer's recommendations are taken as written.
- F4 is the OWNER's (what a person is shown, P9): open; the nodes run on recommendation (a) until the owner answers.
- State of this draft: accepted by the Lead as a draft; the critic-on-plan pass (mandatory for a new idea, PROJECT.md step 6) is
  review `docs/tasks/specs/reviews/of3-2-knowledge-phase2-plan-review.md`. No node of K1-K7 is dispatched before that review is read
  and its fix list is folded into this file. The next session starts from this file plus that review.
