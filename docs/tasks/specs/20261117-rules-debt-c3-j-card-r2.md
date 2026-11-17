# Card C3-j r2: the stand's page load, measured by the factory or deleted (t-1116, node rules-debt/1/RD1-13, F19)

Designer draft for the Lead. It replaces §2 of `docs/tasks/specs/20261117-rules-debt-wave3-j-k-cards.md` (r1) whole.
§1 of r1 and the parent spec's shared items S-a..S-f still apply where this draft does not override them.

**Base.** The root checkout reads `main` = `origin/main` = `9a7acdf35888181795904260552b5974ce37d70c` (I read `.git/HEAD`,
`refs/heads/main` and `refs/remotes/origin/main` directly). Every `file:line` below was read on that tree. I had no shell, so
nothing was RUN. Every command is for the builder or the Lead.

## §0. The direction, from the owner's two words of 17.11.2026

1. Recorded at the end of r1: «…любой стенд который нам дали мы считаем готовым тестовым стендом если человек не скажет чего-то
   дополнительного…».
2. Relayed by the Lead during this dispatch, and it replaces the "run and say not measured" default of the brief: «зачем нам
   вообще знать этот лимит? Для того чтобы тесты правильно написать? Ну значит надо измерить и использовать. Человек точно этот
   лимит не знает. А если нам он не нужен, то вообще это понятие удалить».

What follows from them:
- No branch asks a person about this limit.
- The card first answers "who USES the limit". Then it takes direction (A) (the factory measures and uses it) or (B) (the
  concept is deleted).
- If the evidence is split, the choice comes back as a fork with a recommendation. It is split (§A), so it comes back as
  **F-j0**. The card below is written for the recommendation, so it can be run before the owner answers (PROJECT.md
  "Командная работа" п. 11).

## §A. Evidence: who produces and who uses the stand limit

The limit has two halves:
- the stand's measured page load, config `environments[].measured.e2e_page_load_s`;
- the page objects' wait, config `profiles[].page_object_max_wait_s`.

Search 1: Grep, case-insensitive, over `ai-packages/qa-factory/` without `**/tests/fixtures/**`, pattern
`page_object_max_wait_s|e2e_page_load_s|stand limit|_e2e_limit`. Search 2: Grep over the same tree without `**/tests/**`, pattern
`"measured"|measured\.|\.measured|page_object|max_wait`. Positive control: both calls found the known hits in
`gate_preflight.py:3118-3121`.

| half | PRODUCER (writes it) | READERS (do work with it) |
|---|---|---|
| page load | **none**. No script writes it. No `.md` of the package (skills, agents, references, design) tells onboarding or any role to record it. The only trace is the docstring "onboarding records it by hand (a headless-browser probe is a later B-line)", `gate_preflight.py:3106-3107` | (1) `gate_preflight._e2e_limit` :3089-3164, which feeds `check_s5_stand_limits` :3166-3218 (a note when unmeasured, a card when `over`, FACTORY_DEFECT when unreadable or incomplete), `check_s5_reporter`'s skip on `over` :3323-3330, and `_stand_limit_card`'s "another stand" :3247-3255; (2) **`manual_capture.timeout_for`** :555-558: the step limit of a manual capture is the measured load + 30 s, else `DEFAULT_TIMEOUT_S` 180 (:108-109). It is used by the gate's sign-in probe (`gate_preflight.py:2808`) and by every manual capture session (`manual_capture.py:3413`, :5439 region) |
| page objects' wait | **none** (same searches) | only `_e2e_limit`. No brief carries it: `brief_pack.py` has no hit for either key, so the automator never receives it, and no role reads it to write waits |

Nearby, and not this concept: `manual_capture.element_wait_for` / `ELEMENT_WAIT_S` 30 (:110-111, :565-572), config
`manual_capture.element_wait_s`. That is the element lookup limit of the factory's own manual browser, and it stays.

What the evidence says:
- **Nothing produces either half.** Every reader therefore reads its default or "unmeasured". M5 (t-1092) measured this on 3/3
  recorded stories (§F). This is an AR-22 defect today: fields are read, and nothing produces them.
- **The wait half has no worker.** Only the gate's comparison reads it. The wait itself lives in the project's test code, which
  the automator writes. Comparing it with a stand belongs to the automator (open variety: AR-2, AR-7, FR-47), not to a config
  number that a person "cannot know".
- **The load half has one worker today, and one it should have.** Today: `manual_capture.timeout_for`, which works without it
  (default 180 s). The one it should have: the automator, who writes page-object waits. It needs the stand's load BEFORE the
  work (AR-10). The cmp2 lesson in the docstring :3104-3107 is about exactly this: 70-110 s loads, waits of 5-30 s, about $2.3
  of automator dispatches before S5 found out.
- So the evidence is **split**: the load is needed (measure it and use it), and the wait plus the code comparison are not
  needed (delete them). That gives fork F-j0 (§D), recommended (C).

## §1. Architecture, rules, owners (designer rule 1)

FR sections walked:
- C3-j1: A (FR-3: a failed measurement is reported, never asked), B (new text a role and a person read: FR-6), C (FR-38/AR-10:
  the number reaches the automator before the work; FR-15: the path is given), D (FR-59: no gate is left that decides on it),
  F (FR-41: "not measured" and "at least" are never written as facts; FR-28: the measurer gets a test), G (FR-47: code measures,
  the role judges the fit).
- C3-j2: A, B (texts removed), D, E (no delivery or report text changes), G.

AR-n touched, with the change check each one demands in the DoD:

| AR | how kept | change check (in the DoD) |
|---|---|---|
| AR-22 | j1 lands the first PRODUCER of the page load (`stand_load.record`) together with its readers (`stand_load.read` ← `brief_pack.stand_load_lines`, `manual_capture.timeout_for`, the gate note), in one commit. j2 deletes the wait key, which has readers and no producer | a test row per reader reads a record the writer wrote (round trip); a grep of `page_object_max_wait_s|e2e_page_load_s` over `scripts/` outside tests gives 0 after j2 |
| AR-10 | the S5 automator and code-critic briefs carry the measured load in the head, before the work | a `test_brief_pack.py` row: an S5 automator brief over a recorded measurement holds the line |
| AR-13 | `stand_load.read` is the only reader of the record; `timeout_for` and `brief_pack` call it | grep `stand-page-load.json` over `scripts/` outside tests: only `stand_load.py` |
| AR-14 | `stand_load.record` is the only writer of `qa-factory/records/stand-page-load.json` | the same grep |
| AR-7 / AR-29 | code measures a number (data). Whether the waits fit it is the automator's judgment, reviewed by the code critic. No code comparison is left (j2) | the census row of `check_s5_stand_limits` leaves (j2, a shrink, named); j1 adds no census unit |
| AR-4 | the record is keyed by the stand name and its definition sha (`stand_identity.definition_sha_for`), never by the machine or the layout | a row keyed under another definition sha is `none` |
| AR-12 | the measurement costs one headless page load at gate A, reused while the key holds | E8 rows |
| AR-15 | one staleness rule (`measurement_is_stale` moves into `stand_load`, and the gate copy goes in j2); one page-load reader for the timeout and the brief | grep `def measurement_is_stale` gives one hit after j2 |
| AR-28 | `none` / `failed` / `unreadable` are named in every reader. Nothing gates on them, so none is ever a pass at a boundary | rows per state |
| AR-20 | registry pins shrink (row deleted), census shrinks, D13 re-measured | the pins in j2 item 4, named |

Checks added, moved or removed (AR-29), with the owner each serves and its census class:

| check | node | owner | census class | blocks |
|---|---|---|---|---|
| `check_stand_page_load` (gate A: measure, or reuse a fresh row; a note either way) | j1 | data (code) | no unit: no refusal, no raise (notes only) | no |
| `stand_load.measure` / `record` / `read` | j1 | data | no unit (never raise; a write failure is a returned state) | no |
| `brief_pack.stand_load_lines` | j1 | data (reports a measurement) | no unit | no |
| whether the page objects' waits fit the load | j1 (moved from code to role) | judgment: `qa-automator`, reviewed by `qa-code-critic` (a tier above judges the role, AR-29) | none (role) | n/a |
| `check_s5_stand_limits` + `_e2e_limit` + `_stand_limit_card` (the `over` card and the defects) | j2 (deleted) | intent: the owner's word that a person is not asked and that an unneeded concept is deleted | `gate_preflight.py::check_s5_stand_limits` shape/data (`judgment-census.json:418`) leaves: a shrink, named in the verdict | was yes |

Commit lines: in the form `tools/architecture_gate.py` accepts. That file is the only carrier of the grammar; it is not
copied here. Each node gives the CONTENT below. `judgment: none` always carries its ` -- <why>`.

## §2. Node C3-j1: the factory measures the stand's page load and hands it to whoever writes or judges waits

Wave 3, gate_preflight HOT, in C3-j's queue slot (§E). It needs a plan critic before the build (a new owner direction:
PROJECT.md, package change п. 6 (г)).

given: `C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md` (whole), `C:/QAFactory/forge-repo/plans/builder-rules.md`, `C:/QAFactory/forge-repo/docs/TESTING.md`, this file §0-§F; under `C:/QAFactory/forge-repo/ai-packages/qa-factory/`: `scripts/gate_preflight.py:150-210,1665-1670,2689-2811,3089-3218,6078-6110`, `scripts/manual_capture.py:95-120,555-572,1636-1680,3405-3420,5430-5445` (and every `timeout_for(` hit), `scripts/brief_pack.py:2881-2894,3389-3407,4136-4150,4530-4560`, `scripts/env_probe.py` (`frontend_of`), `scripts/stand_identity.py` (`definition_sha_for`), `scripts/environment_record.py:1-60,200-230` (the record-file precedent: absent / unreadable / atomic write), `scripts/tests/test_gate_preflight.py:2734-2935`, `scripts/tests/test_manual_capture.py:165-185`, `scripts/tests/test_brief_pack.py` (grep `stand_lesson_lines`)
owns:
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/stand_load.py` (new: `measure`, `record`, `read`, `RECORD_REL`, `CAP_S`, and `is_stale`, which moves the logic of `gate_preflight.measurement_is_stale` here)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_preflight.py` (new `check_stand_page_load`; its place in `run`'s gate A steps; `run`'s docstring, "read-only except"; the module docstring line :57; nothing of `_e2e_limit` / `check_s5_stand_limits` / `_stand_limit_card`, which belong to j2) — HOT
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/manual_capture.py` (`timeout_for` and every caller of it in this file)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/brief_pack.py` (new `stand_load_lines`, new constant `STAND_LOAD_ROLES`, one call in the head build)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_manual_capture.py` (the `timeout_for` rows :171-179 flip; one new table for `stand_load`)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_preflight.py` (rows for `check_stand_page_load`; `check_stand_page_load` added to `NEW_CHECK_FUNCTIONS` :3651 and to the FR-6 scan list :3806-3809)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_brief_pack.py` (rows for `stand_load_lines`)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/changelog.d/rules-debt-c3-j1-stand-page-load.md` (new fragment)
non-goals: deleting anything of the old limit (j2); `config.json` of any project (the factory writes no config key); `references/gate-registry.json` (the measurement judges nothing, so it gets no gate row: §C small choices); `report_facts.py` (no report line: §C); `manual_capture.element_wait_for`; asking a person anything; any new test file
handoff: report path given by the Lead
edges: E1-E16 (§B)
DoD: `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/stand_load.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_preflight.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/manual_capture.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/brief_pack.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_manual_capture.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_preflight.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_brief_pack.py` plus the printed non-slow files; `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_registry.py --check` exits 0 with the debt block unchanged; `test_gate_preflight.py` and `test_judgment_census.py` are slow, judged by the batch canon and named in the report
siblings: axis 5, prose twins: the builder greps `skills/qa-story/phases/s4.md`, `s5.md`, `agents/qa-automator.md`, `agents/qa-code-critic.md`, `agents/qa-failure-analyst.md` for `page load|timeout|wait`, and gives each hit "checked, no edit" or an edit inside owns (an edit outside owns is a question); the first-look and stand-lesson head lines (`stand_lesson_lines` :2881) are the model for one formatter feeding several roles
designer: `C:/QAFactory/forge-repo/docs/tasks/specs/20261117-rules-debt-c3-j-card-r2.md` (C3-j1)

Items:
1. **`stand_load.py`** (new, stdlib plus lazy imports; it writes only through `record`).
   - `RECORD_REL = ("qa-factory", "records", "stand-page-load.json")`, beside the environment record. It is project-level, so one
     measurement serves every story on the same stand definition.
   - `CAP_S = manual_capture.DEFAULT_TIMEOUT_S` (180), read through a lazy import so there is one number.
   - `measure(cfg, stand: dict, project_root, *, backend=None) -> dict`. It never raises. Steps:
     - The address is `env_probe.frontend_of(...)`, the one reader of the frontend address (AR-13). No address, or an address
       that reader refuses (credentials in it) → `{"state": "failed", "why": "the stand has no web address the factory may
       open"}`.
     - The backend is `manual_capture.BACKEND_FACTORY()` when set (the test seam), else `manual_capture.PlaywrightBackend()`.
       It is opened with `timeout_s=CAP_S` and the stand's hosts (`MC.stand_hosts`). There is ONE navigation to the address,
       signed out. The wall-clock time runs until the load event. `close()` runs in `finally`.
     - Result: `{"state": "measured", "load_s": <float, 1 decimal>, "at_least": False, "address": <address>, "at": <ISO now>,
       "how": "the factory's headless browser, signed out, one full load"}`.
     - A navigation that times out at the cap → `"state": "measured", "load_s": CAP_S, "at_least": True` (E4/E5).
     - No browser, a launch error or any exception → `{"state": "failed", "why": "<type>: <first 160 chars>"}`.
     - If the backend has no navigation call to time, the builder STOPS and returns a question. The name of the backend's goto
       is read in `manual_capture.py:1636-1700`; this draft did not read it.
   - `record(project_root, key: dict, result: dict) -> str`: the one writer. The key is
     `{"environment": <stand name>, "definition_sha": <stand_identity.definition_sha_for(cfg, stand)>}`. One row per key,
     replaced whole. The write is atomic (`event_store.atomic_json`, as `check_actor_sign_in` :2711-2714). Returns `""`, or the
     reason the write failed. It never raises. A file that exists and cannot be read is NOT overwritten: the return says why
     (E7).
   - `read(project_root, cfg, stand) -> dict`: the one reader. It returns one of:
     - `{"state": "none"}`: no file, no row under today's key (another definition sha), a placeholder or absent stand, or a
       stale row (`is_stale(row["at"], stand.get("verified"))` non-empty);
     - `{"state": "unreadable", "why": ...}`;
     - the row (`measured`, or `failed` with its `why`).
     A `failed` row is reused like a `measured` one, so a stand with no browser is not retried in every rehearsal. A new
     definition sha or a stale `at` measures again.
   - `is_stale(at, verified) -> str`: the body of `gate_preflight.measurement_is_stale` (:195-206 region), moved. In j1 the gate
     keeps its own copy until j2 deletes it (E13).
   - expected from: the owner's word (measure and use it), FR-50/P5 (every route before a person, and here the factory's own
     browser is the route), FR-41, AR-13/14.
2. **`check_stand_page_load` (gate A)**, a `Rehearsal` method, inserted in `run`'s gate A tuple right after
   `check_s5_stand_limits` (j2 removes that one). It runs only when something will use the number:
   - the plan has an `automate` row of level `E2E_LEVEL` keyed to a profile that is not handed (`keyed_profiles`, `_handed`), OR
     a manual case (`_actors_of_manual_cases` is non-empty, or the plan has a `manual-agent` row);
   - and a stand is selected;
   - and `gate_rehearsal.skip_stand_limits` is not true. This key is kept as the project's existing off switch (E9).
   Body:
   - `got = stand_load.read(...)`. `measured` / `failed` → no browser, and one note that reuses the brief's words.
     `none` → `measure`, then `record`, then one note. `unreadable` → measure, do not record, one note saying the result could
     not be kept and why.
   - It is NEVER a finding (`add`): it blocks nothing, and a person is asked nothing (owner, 17.11.2026; FR-3). The note
     carries `extra` machine fields (`state`, `load_s`, `at_least`, `address`, `why`) and no field path in the sentence (FR-6;
     the precedent is the K5 rows :2815).
   - Note texts:
     - measured: "the stand's full page load is {load_s:g} s ({address}, measured {at} by the factory's browser, signed out) -
       the S5 briefs carry it, and the page objects' waits are written to fit it";
     - at least: "... at least 180 s (it had not finished loading by then) ...";
     - failed: "the factory could not measure the stand's page load ({why}) - a defect of the factory; manual checks use 180 s per
       page, and the S5 briefs say it was not measured".
   - `run`'s docstring now names the second file the rehearsal writes (`qa-factory/records/stand-page-load.json`, project
     level).
   - expected from: P31 (gate A is the one point both the driver road and the skill road pass: `driver_gates.py:120`,
     `skills/qa-story/phases/s4.md:19`), FR-3, FR-59 (no decision is taken on it).
3. **`manual_capture.timeout_for`** becomes `timeout_for(project_root, cfg, stand) -> float`: `stand_load.read(...)` measured →
   `load_s + TIMEOUT_MARGIN_S`; any other state → `DEFAULT_TIMEOUT_S`. It no longer reads `stand["measured"]`. Every caller
   changes; the builder greps `timeout_for\(` over `scripts/` (known: `gate_preflight.py:2808`, `manual_capture.py:3413`, the
   :5430-5445 region) and gives a report line per hit. expected from: AR-13 (one reader), AR-22, E12's safe direction (a
   missing measurement never shortens a limit).
4. **`brief_pack.stand_load_lines(project, cfg, env_name) -> list`**: one formatter, called in the head for
   `STAND_LOAD_ROLES = {("S5", "qa-automator"), ("S5", "qa-code-critic"), ("S6", "qa-runner"), ("S7", "qa-failure-analyst")}`.
   That set sits beside `FIRST_LOOK_KIND` :4141, the same wiring form. The stand comes from `_stand_pick(...)` as for
   `stand_lesson_lines` :4544. Lines, one each:
   - measured: `- Stand page load: {load_s:g} s for {address} (measured {at} by the factory's browser, signed out; a page behind the sign-in or a heavier route can take longer - your own runs show it). Page-object waits are written to fit it.`
   - at least: `... at least 180 s (it had not finished loading) ...`
   - failed: `- Stand page load: not measured - the factory could not ({why}), a defect of the factory; your own runs show it.`
   - none: `- Stand page load: not measured yet.`
   - unreadable: `- Stand page load: the record could not be read ({why}).`
   - The address is cut at 120 characters with `…` (E16). The line never raises: an exception is the line
     `- Stand page load: not read ({type}), a defect of the factory` (the precedent is `test_timeout_line` :3405-3407).
   - It is a courtesy and reports; it judges nothing (P1, AR-7).
   - expected from: AR-10, FR-38, FR-41, FR-15.
5. **Tests: rows in existing keep tables.** Expectations come from this card, never from the code's output.
   - `test_manual_capture.py` (keep, detector). Table `stand_load`, with a fake backend through `BACKEND_FACTORY`:
     measured 12.34 → `load_s` 12.3; a timeout at the cap → `at_least` True and `load_s` 180; no address → failed; an address
     with credentials → failed; a backend that raises at open → failed with the type name; record then read → the same row
     (AR-22 round trip); another definition sha → none; a stale `at` → none; an absent file → none; 0 bytes, broken JSON, a
     list instead of an object → unreadable, and record refuses to overwrite (the file bytes are unchanged); a 10 000-row file
     reads (magnitude); a non-ASCII stand name round-trips.
   - The `timeout_for` rows :171-179 flip: the config's `measured` is no longer read (a config value of 70 now gives 180); a
     recorded measurement of 70 gives 100; `failed` / `none` / `unreadable` give 180.
   - `test_gate_preflight.py` (keep, gate_named), with a stub of `stand_load.measure`:
     - an e2e row and no record → one note, no finding, the record written, the backend called once;
     - a second rehearsal → no second call (reuse);
     - a failed measurement → a note that says "a defect of the factory", no finding, `can_proceed` unchanged;
     - no e2e row and no manual case → nothing measured, no note;
     - `skip_stand_limits` → nothing measured, no note;
     - an unreadable record → measured, not written, and the note says it could not be kept;
     - the off-road: only a handed profile, no manual case → nothing.
   - `test_brief_pack.py` (keep, detector): each of the five lines for the S5 automator; the same line for S7
     qa-failure-analyst; no line for S3 qa-test-strategist; a 200-character address is cut at 120 with `…` (AT 120 whole, 121
     cut).
6. **Changelog fragment**: one entry in English (FR-30). The gate measures the stand's page load once per stand definition, and
   the S5/S6/S7 briefs and the manual capture's page limit use it.

architecture content: `AR-22 -- the first producer of the page load (stand_load.record) lands with its readers (read, timeout_for, stand_load_lines, the gate note)`; `AR-10 -- the automator's brief carries the measured load before the work`; `AR-13 -- one reader stand_load.read`; `AR-14 -- one writer stand_load.record`; `AR-4 -- keyed by stand and definition sha`; `AR-28 -- none/failed/unreadable named in every reader, nothing gates on them`; `AR-29 -- no new census unit; the fit is the automator's judgment`. judgment content: `none -- code measures a number and reports it; whether waits fit it is the automator's judgment, reviewed by the code critic; no check moves into or out of a role`.

## §3. Node C3-j2: the wait and the code comparison deleted whole

Serial after j1 is merged (same HOT file; its tests read j1's world).

given: as j1, plus the merged j1 diff; `C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json:479-499`; `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py:36-75,200-210,245-255,320-350,735-750,1000-1060`; `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json:410-420`; `C:/QAFactory/forge-repo/tools/architecture_gate.py` (its census rule, `CENSUS_REL` :88)
owns:
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_preflight.py` (delete `_e2e_limit`, `check_s5_stand_limits`, `_stand_limit_card`, `limit_seconds` :157-164, `measurement_is_stale` :195-, their two selftest lines :6394, :6398, the `check_s5_stand_limits` entry in `run` :6089, `check_s5_reporter`'s `over` skip :3323-3330, and the docstring mentions :57, :804, :3104-3107) — HOT
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json` (delete row `s5_stand_limits` only)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json` (delete the row `gate_preflight.py::check_s5_stand_limits` :418 only)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_preflight.py` (delete the §5 stand-limit tests :2734-2935, `test_the_reporter_skips_a_profile_whose_e2e_limit_card_is_open` :3065 and its runner line :6248, `test_c2_the_stand_limit_card_offers_only_doors_that_have_an_executor` :3624 and :6264, the three names in `NEW_CHECK_FUNCTIONS` :3651 and in :3809, the `_e2e_limit` entry at :3715, the `s5_stand_limits` samples at :3758-3760, and any row of :4070-4120 that asserts on the stand-limit card. Every hit of `e2e_stand_limit|s5_stand_limits|_e2e_limit|page_object_max_wait_s|e2e_page_load_s` gets a report line)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py` (`EXPECTED_IDS` :45 and `EXPECTED_DEBT` :63 lose the row; K-T1.2 :252 and K-T1.14 :328, :342-343 by the delta; D13 if it moves)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/changelog.d/rules-debt-c3-j2-stand-limit-removed.md` (new)
non-goals: `test_story_run_delivery_b.py:555` and `_c.py:975, :987` (they use the check id `e2e_stand_limit` as sample data for a generic person_decides finding; no code of theirs reads the check, so they stay, each with a report line); `design/factory-rules-debt.md` (the B-282 line is moved by S1b, finding `20261117-rd2-c3-j-…md`); `environment_record.py`, `gate_brief.py`, `stand_gaps.py` (r1's road is dropped whole); any new test file
handoff: report path given by the Lead
edges: E13-E15, E17 (§B)
DoD: `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_registry.py --check` exits 0, `s5_stand_limits` is absent from the output, and the debt count is one lower than on the base; the Grep tool, case-insensitive, over `ai-packages/qa-factory/scripts/` excluding `tests/`, pattern `page_object_max_wait_s|e2e_page_load_s|_e2e_limit|check_s5_stand_limits|_stand_limit_card|measurement_is_stale` gives 0, with a positive control (the same call finds `stand_load` in `scripts/`); then `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_preflight.py C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_preflight.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py` plus the printed non-slow files; `test_gate_preflight.py`, `test_gate_registry.py` and `test_judgment_census.py` are slow: canon, named
siblings: axis 5 (row ↔ sites ↔ prose): the builder greps the package `.md` files for `stand limit|page load|page_object` (§A: 0 hits on 9a7acdf3 outside gate_preflight docstrings) and gives each hit a line; the A1 class ("a word compared in an unregistered function"): `check_s5_reporter`'s `== "over"` leaves with the skip
designer: `C:/QAFactory/forge-repo/docs/tasks/specs/20261117-rules-debt-c3-j-card-r2.md` (C3-j2)

Items:
1. **gate_preflight deletions**, as listed in owns.
   - After the deletion, `check_s5_reporter` rehearses every keyed, non-handed profile. On a slow stand the rehearsal's own
     timeout (`reporter_timeout_s`, default 180, :3312) and its existing outcome states say what happened (E14).
   - `run`'s gate A tuple loses `r.check_s5_stand_limits`; `r.check_stand_page_load` (j1) stays where j1 put it.
2. **Registry**: row `s5_stand_limits` deleted. The gate is gone, so FR-59 has no gate left to decide on an unknown. No
   other row is touched (row-disjoint, parent spec E-d).
3. **Census**: the row :418 is deleted. `test_judgment_census.py` is a shrink-only ratchet, and the shrink is named in the verdict
   (AR-20). The builder reads `tools/architecture_gate.py` for what the commit's `judgment:` line must say about a census
   change. If it demands something this card does not give, the node stops and returns a question.
4. **`test_gate_registry.py` pins**, measured "at build" as deltas from j2's base (S-f):
   - `EXPECTED_IDS` and `EXPECTED_DEBT` lose `s5_stand_limits`;
   - K-T1.2 reads `"<N-1> gate(s) left as debt:"`, where N is the base's count (6 on 9a7acdf3; fewer if C3-b2/C3-d merged first);
   - K-T1.14: the debt list follows `EXPECTED_DEBT`, its message's "six rows" wording moves, and the split goes debt -1, total
     -1, converted unchanged;
   - an AR-20 comment line `C3-j2, t-<id>: s5_stand_limits deleted (owner, 17.11.2026)`;
   - F4 :743-747: unchanged (the row was `target`);
   - D13 re-measured with `GR.analyse(PLUGIN_ROOT)` before and after. Expected: no triple leaves. The row's words today are
     `matched/mismatched/unknown`, and `check_s5_stand_limits` compares none of them; M6 counted +5 only under r1's code words.
     The count moves only if the scan attributed items to `check_s5_reporter`'s `"over"`. A different set of triples is a stop
     and a question.
5. **Changelog fragment**: the gate no longer compares a recorded page-object wait with the stand; the config keys
   `environments[].measured.e2e_page_load_s` and `profiles[].page_object_max_wait_s` are no longer read (a project's file that
   carries them is unaffected; they are ignored).

architecture content: `AR-22 -- the wait key, read with no producer, is deleted with every reader`; `AR-7 -- no code compares a test's waits with the stand; the automator does, with the measured number`; `AR-20 -- registry row and census unit removed, pins moved by the named delta, D13 re-measured`; `AR-28 -- no gate is left on this unknown`. judgment content: `none -- a check is deleted on the owner's word; nothing moves into judgment and no person is asked`.

## §B. Edges (each with the INVARIANT it protects)

- **E1 (no stand, a placeholder stand)**: nothing is measured or recorded; the brief says "not measured yet". INVARIANT: nothing
  is recorded under a placeholder or empty key.
- **E2 (a stand with no web address, an API-only stand)**: `measure` → failed, "no web address". The note and the brief say so.
  INVARIANT: a failure is never shown as a number.
- **E3 (no browser on the machine)**: failed, with the factory's reason; manual capture uses 180 s. INVARIANT: a factory-owned
  reason is reported, never asked (FR-3), and it blocks nothing.
- **E4 (limit: the load is beyond the cap)**: `at_least` True, `load_s` 180; every text says "at least". INVARIANT: an unfinished
  load is never written as its true value (FR-41).
- **E5 (limit: AT the cap)**: a load that finishes within the backend's limit is `measured` with its value; only the backend's
  timeout makes `at_least`. Rows at 179.9 and at the timeout.
- **E6 (signed out)**: the factory measures what loads at the address without an account (possibly a login page). The texts say
  "signed out" and name the address. INVARIANT: no text claims a route or a signed-in page was measured.
- **E7 (record unreadable)**: never overwritten; the measurement of this rehearsal is told in the note only; the brief says the
  record could not be read. INVARIANT: a file the factory cannot read is never replaced (other stands' rows are not lost).
- **E8 (reuse and staleness)**: reused while `definition_sha` is the same and `at` is not older than the stand's `verified`;
  otherwise measured again. INVARIANT: a measurement of another stand definition or build never speaks for this one.
- **E9 (the off switch `skip_stand_limits`)**: no measurement and no note; the brief says "not measured yet". INVARIANT: an
  informed switch stays informed.
- **E10 (no e2e rows and no manual case)**: nothing measured. INVARIANT: no browser is opened for a number nothing uses
  (FR-56/AR-12).
- **E11 (a handed profile)**: it counts as no e2e use. A manual case still triggers the measurement.
- **E12 TEMPORAL (stories and projects from before j1)**: the record file does not exist until the first gate A after j1, so every
  reader is `none` → 180 s and "not measured yet". The move that creates the file is j1's first gate A rehearsal on a project.
  A project whose config carries a hand-written `measured.e2e_page_load_s`: from j1 on, `timeout_for` stops reading it.
  Before the first measurement that gives 180 s instead of value+30. That is never shorter when value+30 ≤ 180, and it is
  shorter only for a hand value > 150, which no recorded story carries (M5). INVARIANT: no recorded story changes; every new
  limit comes from a measurement or the declared default. Recorded fixtures: no fixture holds the old note text or the check id
  (Grep, case-insensitive, over `scripts/tests/fixtures/`: only `judgment-census.json` matches, which is the positive control).
- **E13 TEMPORAL (between j1 and j2)**: the old check and the new step both run. The old one reads keys nobody writes and keeps
  its note, as today. `measurement_is_stale` exists twice for one merge window. INVARIANT: j2 leaves one copy (AR-15).
- **E14 POSITIONAL**: `check_stand_page_load` sits in the gate A tuple where `check_s5_stand_limits` was, before
  `check_s5_reporter` and `check_s5_runtime_probe`. INVARIANT: the reporter reads nothing of it (after j2 no step reads the
  limit). The sign-in probe (`check_actor_sign_in`, earlier in the tuple) uses `timeout_for`, so in the FIRST rehearsal of a
  project it gets 180 s. That is the safe direction.
- **E15 (the wait half)**: deleted. INVARIANT: no code compares a test's waits with the stand (AR-7, FR-47).
- **E16 (outside input: the address from the project's config, the record file on disk)**: an address with credentials → refused
  by `frontend_of` (failed); an address of 200 characters → the line cuts at 120 (rows AT and BEYOND); a non-ASCII stand name
  round-trips; the record file at 0 bytes, broken, a list, or 10 000 rows (E7 / magnitude).
- **E17 (j2: projects that set `skip_stand_limits`)**: the key keeps meaning "do not measure" (j1). INVARIANT: a project's
  existing switch keeps a meaning; no config key becomes an error.
- **Brief edges now moot**: the brief asked for `n/a`, each of the four `unmeasured` returns (:3124, :3151, :3155, :3160), a
  stale measurement, a profile with no e2e rows, and a stand with no environment record. All four returns are deleted in j2.
  Their successors are E1/E2/E8/E10, and the stand with no record is E12.

## §C. Small technical choices I closed

- The measurement gets no gate-registry row. It judges no validity, compares no anchor word, and nothing accepts or refuses on
  it, so A26 has nothing to scan.
- No delivery-report line. The number is not a story gap. A failed measurement is a factory defect said at gate A and in the
  briefs. AR-27 concerns a story's findings and bugs.
- The record is project-level under `qa-factory/records/`, beside `environment-properties.json`, keyed as AR-4 asks, so one
  load serves every story on that stand definition.
- `gate_rehearsal.skip_stand_limits` is kept as the off switch, so no project's config breaks.
- A `failed` row is reused like a measurement (no browser retry per rehearsal); a new definition sha or a stale date retries.
- `STAND_LOAD_ROLES` is a code set beside `FIRST_LOOK_KIND`: the factory's own stage wiring, the same form as the precedent.
- The cap is the existing `DEFAULT_TIMEOUT_S` (180), so the factory holds one number.
- The address is cut at 120 characters.

## §D. Forks (returned, not decided)

- **F-j0 — the direction (the owner's two options against split evidence).**
  - (A) Measure BOTH halves and keep a code comparison: the factory measures the load and also reads the waits from the
    project's tests. That is open variety (frameworks, languages): role work or a language table (AR-1/AR-2). The gate card
    would stay, so a person would still be asked when `over`, against the owner's word. Not recommended.
  - (B) Delete everything, including `manual_capture.timeout_for`'s measured branch: the 180 s default for every page, and
    nothing in the automator's brief. It is the cheapest (j2 only, plus the timeout edit), but it loses the cmp2 lesson (waits
    written blind on a slow stand).
  - (C) **Recommended**: measure the LOAD (j1: the factory's browser at gate A, given to the automator, code critic, runner and
    failure analyst, and to the manual capture's page limit); delete the WAIT and the code comparison (j2). It follows the
    evidence: the load has workers, the wait has none.
  - Cost of (C): two serial nodes on the HOT file. The measurement costs a headless load per stand definition.
- **F-j-route — what is measured.** (a) **Recommended**: the stand's frontend address, signed out (E6), with the texts saying
  so. (b) A signed-in load of the page the cases open first. That needs an account and a route chosen per case (open variety),
  and it would be a later node over the sign-in probe (`_probe_sign_in` :2803 already opens a signed-in context: its landing
  time could be recorded there). Recommended as a separate, later node, which the card does not need.
- **F-j-split — node count.** (a) **Recommended**: j1 then j2, serial. Each stays well under a worker budget, and j1 has no
  window in which the old protection is gone with nothing to replace it. (b) One node: one HOT slot, about twice the review
  size (the J10 concern).
- **F-j-defects — moot.** The brief asked whether `unreadable` / `incomplete` keep today's FACTORY_DEFECT cards. Both are deleted
  with the config record in j2: the factory's own measurement replaces the hand record, and its failure is reported (FR-3), not
  carded. If the owner picks (A), this fork reopens: those cards put a factory-owned reason to a person as "pass anyway"
  (FR-3), and I would recommend reporting them, not carding them.
- **F-home — where the owner's stand principle lives.** (a) **Recommended**: both of the following.
  - A new owner principle **P32** in `docs/OWNER_PRINCIPLES.md` (the index regenerates). Proposed text: «Любой стенд, который
    нам дали, — готовый тестовый стенд, пока человек не скажет иного. Что фабрике нужно знать о стенде, она измеряет сама;
    человека не спрашивают о числе, которого он не знает; понятие, которое никто не использует, удаляется.»
  - A sentence added to **FR-50** (`design/factory-rules.md:98`, section A): it is the "every route before a person" rule, and
    this sharpens it for stand properties. Proposed English: "A stand the factory is given is a ready test stand unless a person
    says otherwise: what the work needs to know about it the factory measures with its own tools, and a person is never asked
    for, nor waited on for, a number they cannot know."
  - Not FR-36 (a run's standing decision about a capability) or FR-21 (the product lacking what a requirement demands): neither
    is about measuring the stand.
  - FR-41 and FR-59 already hold the "never a fact, never a pass" half.
  - (b) Only P32, with FR-50 untouched.
  - The owner or the architect places it (the Lead writes DECISIONS/principles; a package FR edit is its own package change).

## §E. Serial order with the other wave-3 cards

- gate_preflight HOT: j1 and j2 take C3-j's slot. From r1: `C3-rr (merged) → C3-j1 → C3-j2 → C3-k2 → C3-h`. j2 deletes
  functions disjoint from C3-k2 (`_observed_identity`) and C3-h.
- `references/gate-registry.json` and `test_gate_registry.py`: only j2 touches them (one row deleted; pins by the delta). From
  r1: `… C3-d → C3-j2 → C3-k1 → C3-k2 → C3-k3 → C3-k4 → C3-h`. Each later card re-measures its own deltas on its base (S-f).
- `test_gate_preflight.py`: j1 adds, j2 deletes; C3-k2 edits the stub at :4261, which is disjoint.
- **Not read by me** (context budget): `20261117-rules-debt-wave3-g-h-cards-r2.md`, `…-wave3-k-cards-r2.md`,
  `…-c3-fix-conversions-cards-r2.md` §4. The queue above is r1 §3's, plus the t-1092 critic. The Lead confirms that the r2
  cards hold the same order. If one of them writes `brief_pack.py`, `manual_capture.py` or `judgment-census.json`, that is a
  new conflict for j1/j2 and gets ordered first.

## §F. The measured premise (M5) and the t-1092 remarks

**M5, restated.** t-1092 decoded `state/config-at-start.json` of the three recorded stories with a config: cart-1,
local-1-0108 and local-1-arm-b (Glob: exactly these three files). In each, profile `web` has no `page_object_max_wait_s` and
environment `local` has no `measured`. Their e2e-ui rows on `web` are 1/10, 13/21 and 10/17. So `_e2e_limit` returns
`unmeasured` on 3/3. In this card that premise is the evidence that **nothing produces the limit** (§A).

The files hold the config base64-encoded (key `bytes_b64`, read here at line 2 of cart-1's file). The config half can be
reproduced with this command (not run here):
`python -B -c "import json,base64,glob;[print(p,[(x.get('profile_id'),x.get('page_object_max_wait_s')) for x in c.get('profiles',[])],[(e.get('name'),(e.get('measured') or {}).get('e2e_page_load_s')) for e in c.get('environments',[])]) for p in sorted(glob.glob('C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/stories/*/state/config-at-start.json')) for c in [json.loads(base64.b64decode(json.load(open(p,encoding='utf-8'))['bytes_b64']).decode('utf-8-sig'))]]"`
- Expected: three lines, each with `('web', None)` and `('local', None)`.
- The positive control is the same output: a profile id printed proves the decode worked.
- The row counts (1, 13, 10) stand on t-1092's run.

| t-1092 remark | where in r2 |
|---|---|
| M5 (premise inverted) | §F: restated as the evidence that no producer exists (§A) |
| J1 (what `accept` / `accept always` do) | moot: no card, no answer, no person asked (owner, 17.11.2026) |
| J2 (no key, so nothing persists) | moot: there is nothing to persist for a person; the factory's measurement persists by its own key (§2 item 1, E8) |
| J3 (profile-level gap readers in gate_brief/driver) | moot: no stand-gap row is created; `gate_brief.py`, `stand_gaps.py`, `driver_machine.py` are untouched |
| J4 (`limit_seconds` lives in gate_preflight) | moot: deleted in j2 with its selftest line; `stand_load` validates its own floats |
| J5 (F-j4 (b) block text) | moot: no unmeasured card, no block, so F-j4 falls away |
| J6 (row-then-add order) | moot: no row |
| J7 (`wait` near-miss word on `environment_property_cover`) | moot: that row is untouched |
| J8 (`scope_keys` / `binding_keys` contradiction) | moot: the row is deleted (j2 item 2) |
| J9 (flipping tests, FR-6 scans, CLI battery) | re-placed: the flipping tests are deleted by name (j2 owns); `check_stand_page_load` joins `NEW_CHECK_FUNCTIONS` and the FR-6 scan list (j1 owns); the outside-input battery moves to the address and the record file (E16, j1 item 5) |
| J10 (size) | re-placed: F-j-split, j1 / j2 |

## §G. Readers of every touched file (rule 7)

Grep, count mode, over `C:/QAFactory/forge-repo/tools`, pattern
`gate_preflight|gate-registry|manual_capture|brief_pack|stand_load|judgment-census|check_s5_stand_limits|page_object_max_wait_s|e2e_page_load_s`:
19 hits in 6 files (content read for 4 of them).

| touched | reader | verdict |
|---|---|---|
| `gate-registry.json` (j2) | `tools/source-split-carriers.json:15, :35`; `tools/source_split.py` (10 hits, the carrier tool); `tools/test_quarantine.py:2199` (path) | unchanged: file name and row form unchanged; a deleted row changes no carrier form |
| `judgment-census.json` (j2) | `tools/architecture_gate.py:88` (`CENSUS_REL`); `tools/source-split-carriers.json:13, :21` | j2 reads `architecture_gate.py`'s census rule before committing (item 3); the carrier form is unchanged |
| `brief_pack.py` (j1) | `tools/test_forge_metrics.py:432, :438` (path as a feature sample) | unchanged |
| `gate_preflight.py`, `manual_capture.py`, `stand_load.py` (new) | no hit in tools/ beyond `source_split.py` strings (not read per hit) | unchanged: no file renamed |
| `tools/test_piles_split.py` (1 hit, not read) | pile split sample strings | unchanged: no file renamed |
| `.githooks/`, `.claude/` | not grepped in this dispatch | the Lead runs the same grep there before dispatch (rule 7 gap, named) |
| package readers of the deleted names | §A searches: only gate_preflight itself, `manual_capture.timeout_for` (j1 re-points it), and tests (j2 owns, except the two delivery tests named in non-goals) | change in j1 / j2 as listed |

## §H. Reading trail

- The two given files, whole (r1 :1-901, t-1092 :1-439).
- `gate_preflight.py` :150-169, :1560-1670, :2689-2729, :2800-2830, :3080-3339, :6060-6337 (plus greps of notes, info, `run(`
  callers, the stand-limit names).
- `gate_brief.py` :405-425, :3170-3197; `stage_done.py` :450-479; `driver_gates.py` :95-134.
- `report_facts.py` :305-329, :885-910, :3105-3195, :3366-3381 (the r2-before-redirect trace; no longer used).
- `brief_pack.py` :255-294, :2870-2909, :3375-3407, :4136-4149, :4520-4579.
- `manual_capture.py` greps (`timeout_for`, `element_wait_for`, `ELEMENT_WAIT_S`, headless).
- `gate-registry.json` :1-8, :395-714; `gate_registry.py` :1-135, :485-681; `gate_template.py` whole.
- `test_gate_registry.py` :36-75, :320-349, :734-753, :1030-1054; `test_gate_preflight.py` :2730-2935.
- `test-layers.json` entries of the named test files; `judgment-census.json` (grep).
- Finding `20261117-rd2-c3-j-…otvet-v-reestre.md`; parent spec :340-409; `factory-rules.md` :98-109 and the section index.
- Glob of `config-at-start.json`.

Not read: the three r2 sibling cards (§E); the backend's navigation method in `manual_capture.py:1636-1700` (j1 item 1 stops
if it is absent); `stand_identity.definition_sha_for`'s signature; `env_probe.frontend_of`'s signature; the tests at
`test_gate_preflight.py:4070-4120` and `:3700-3815` beyond grep lines; `.githooks/`, `.claude/` for rule 7.

## Lead decisions (17.11.2026, Lead of the session; forks by the owner's word of 17.11 and by recommendation)

- **F-j0 = (C)**: it is the owner's word applied to each half — the page load has users, so the factory measures it and
  hands it over (j1); the page objects' wait and the code comparison have no user, so they are deleted whole (j2). No branch
  asks a person. Told to the owner in plain words the same turn.
- **F-j-route = (a)**: the frontend address, signed out; the signed-in load is a later node, not opened now.
- **F-j-split = (a)**: j1 then j2, serial on the HOT file.
- **F-j-defects**: moot under (C).
- **F-home**: the text of P32 and the FR-50 sentence go to the owner as written in §D; nothing is placed until her word.
  j1 and j2 do not wait for it (the cards cite AR-22, AR-10, FR-3, FR-41, FR-59, which already hold).
- §E: the Lead confirms the order against the r2 cards before the j1 dispatch (the designer did not read them).
- Plan critic: mandatory (a gate's meaning changes; PROJECT.md package change item 6) — dispatched next.

## Lead decisions on the forks (architect-rank session, 17.11.2026; by recommendation, until the owner's word)

- F-j0 = (C): the factory measures the LOAD and hands it to the roles that write and judge waits; the WAIT and the code
  comparison are deleted (j2). It is the owner's "measure and use" for the half that has users and "delete" for the half
  that has none. No branch asks a person.
- F-j-route = (a); the signed-in load is a later node, not opened now.
- F-j-split = (a): j1 then j2, serial.
- F-j-defects: moot under (C).
- F-home: NOT decided by the Lead. The proposed P32 text and the FR-50 sentence are shown to the owner; j1 and j2 do not
  wait for it.
- Plan critic: mandatory (a meaning change, PROJECT.md package change item 6) -- t-1125 (report file named t-1123-… by a Lead id error).
