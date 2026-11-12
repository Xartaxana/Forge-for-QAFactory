# t-129 — OF3-1 (phase 1 of the project-knowledge plan): the catalogue and one reader, behaviour unchanged — SPEC (designer draft)

Designer (Opus), 12.11.2026. Draft for Lead acceptance. Forks are in §6 and are NOT closed; every node is executable on the recommendation.
Sources: `plans/piles/onboarding-forge/batch-3-znaniya-o-proekte-fazy-1-6.md:22` (node OF3-1); `plans/project-knowledge-plan.md` §2.1, §2.2,
§4 «Фаза 1» (:208-216), §6, §7 (:319-366; **§7 overrides §1-4**, :322); phase 0 spec `docs/tasks/specs/t-2142-project-knowledge-phase0.md`
(closed 5498318); absorbed rows of `plans/piles/onboarding-forge/batch-1-onboarding-roles-forge.md` (OH1-6 :23, OH3-35 :27, OH3-42 :30, GW1-38 :31).
PKG = `C:\QAFactory\forge-repo\ai-packages\qa-factory`. All `path:line` below were read in THIS round on `main` (dc71a1b) unless marked UNVERIFIED.

## Digest

Phase 1 is a pure refactor: (a) every fact the factory knows about a project gets ONE catalogue row (data, AR-1/AR-3/AR-22); (b) the
existing `scripts/project_knowledge.py` (phase 0) becomes the one reader of facts — `rows`, `value`, `state`, `environment(name)` —
reading config through `config_contract.read_config_file` (AR-13); (c) three ratchets tie template keys, code reads and readers to the
rows; (d) the reads that bypass one reader are folded by class, starting with the absorbed nodes: config read without BOM (GW1-38),
`test_data` read past `test_data_states` (forge finding), env-file parsed three ways (OH3-42), `artifact_root` undocumented and
hard-coded (OH1-6 / B-319 / B-370), and the owner-approved removal of keys nobody reads (OH3-35 sub-item). No question, gate, brief or
onboarding text changes meaning, except the removal of interview lines for removed keys if fork F3 (a) is taken.

---

## §0 Facts (measured)

**What phase 0 left (the reader exists)**
- F-1 `scripts/project_knowledge.py` exists: `KEYS` literal (:49-55, five registry keys: `product.roles`, `environments.credentials_by_role`,
  `product.sides`, `environments.sides`, `environments.reference_for`) with the comment "Phase 1's catalogue replaces this literal" (:47-48);
  `load` (:108), `state(root, key, environment, element, cfg)` (:215-232, pure, never raises, toward `unknown`), `subjects` (:235), `roster` (:258).
- F-2 `project_knowledge._config` (:163-170) reads `qa-factory/config.json` with its OWN `json.loads(... "utf-8-sig")`, broken/absent -> `{}` —
  a config reader beside `read_config_file` and `load_config` (the plan's "≥ 3 roads", §7 C16).
- F-3 `KEYS` drives `_usable` (:131-141) and `_form` (:96-99): a row whose key is outside `KEYS` is skipped (toward asking).

**The config readers and their error directions (§7 C16, C18)**
- F-4 `config_contract.read_config_file(root)` (config_contract.py:1349-1374): absent -> `None`; unreadable / empty / not JSON / not an object ->
  raises `ConfigUnreadable` with a door; BOM tolerated (`utf-8-sig`, :1360). Called from 9 package scripts + tests (grep count `read_config_file\(`).
- F-5 `hooklib.load_config(event)` (hooklib.py:792-796) = `read_json(config_path, {}, errors=Exception, kind=dict)`: absent, broken, not an
  object -> `{}` ("no-op here"); BOM tolerated. Called from ~49 package scripts (grep count `load_config\(` over scripts/*.py: 136 hits / 64 files incl. tests).
- F-6 `hooklib.artifact_root` (hooklib.py:636-649): its own `json.loads(... "utf-8-sig")`, a broken config RAISES on purpose ("must raise here,
  not become `{}`", :640-641); `artifact_root` absent -> `<project>/qa-factory/artifacts`; empty or non-string -> `ValueError`.
- F-7 Direct project-config reads WITHOUT BOM (grep `config\.json.{0,40}read_text\(encoding="utf-8"\)`, production files only):
  check_coverage.py:99, environment_record.py:406, report_adapt.py:288, test_novelty.py:320, test_locations.py:745; same class, other form:
  import_test_receipt.py:57, grammar.py:293 (`load_overrides(config_path)`). The GW1-38 row's numbers drifted by 1-20 lines (it says :405, :56, :273).
  install_smoke.py:414 reads a config too (not in GW1-38; it is the installer's smoke — see §5 siblings).
- F-8 Direct reads WITH BOM but bypassing every reader (same grep with `utf-8-sig`): controller.py:4256/:4275/:4292, branch_accounting.py:200,
  dashboard_refresh.py:28, dispatch_liveness.py:94-95, env_probe.py:1114, factory_dashboard.py:725, judge.py:117 (+ more in the persisted grep
  output; the builder's census in item 6 lists them all).

**The catalogue's candidate home**
- F-9 `references/config-keys.json` already carries per top-level template key `since`, `absent_means` (`default` | `required`), `project_fact`
  (:4-307), plus `notes` (:308-665), `removed` (:666-691, `reason`), `renamed`, `reasked`, `asked_until_answered` (:694-698,
  `environment.access`), `value_migrations`, `written_by` (:705-714). Its `about` (:2) says it is read by `config_contract.migration_plan` and
  `readiness.py`; dotted keys appear only "to give a nested key its own `since` or `absent_means`".
- F-10 `references/templates/config.json` (177 lines) has NO `artifact_root` (confirmed by reading the whole file) and NO `default_environment`;
  it has `format_all` (:139), `records_policy` (:141), `test_data.seeds` / `.generators` (:75-76), `requirements_sources` (:92).
- F-11 `config-keys.json` has rows for `format_all` (:186-189) and `records_policy` (:190-193); `config-projection.json:32` says of
  `default_environment`: "no reader in the package".

**The six "dead" keys (OH3-35; the plan §7 says "not re-verified by the critic", :356)**
- F-12 `test_data.seeds` and `test_data.generators` HAVE a reader: `judge_code.JUDGE_TEST_DATA_KEYS` (judge_code.py:203) read by
  `test_data_for_judge` (:208-227) through `config_contract.test_data_states`; `audit_factory.py:777` checks the word `seeds` in onboarding theme 3.
  They are NOT dead today (TQ1-11 added the reader after the audit of 30.10).
- F-13 `records_policy`, `format_all`, `default_environment`: no reader in `scripts/*.py` (case-insensitive grep over the package; hits only in
  config-keys.json, config-projection.json, templates/config.json, p2-interview.md:281-288, p4-generate.md:129/:393-394, CHANGELOG, a test
  fixture `run-12586-stand-config/qa-factory/config.json:63`, test_config_migration.py:374, test_config_revert.py:452; `DEFAULT_ENVIRONMENT` in
  stand_lease.py:45 is an unrelated constant). Positive control: the same grep finds config-keys.json:186 `format_all`.
- F-14 `requirements_sources` is excluded from removal by the owner's word 31.10 (gets producer and reader, node OH3-39; batch-1 :27).
  So OH3-35's "six" is five names; of them three are dead.

**test_data (forge finding)**
- F-15 The finding exists: `plans/piles/forge/findings/20261102-chitateli-test-data-mimo-odnogo.md` (the batch-3 row :22 says "место не найдено" —
  it is found). One reader `config_contract.test_data_states` (now config_contract.py:893-; `TEST_DATA_UNKNOWN` :890); bypassers named there:
  `env_probe.py:603` (`data_cleanup`, own `CLEANUP_UNKNOWN`), `audit_factory.py:766`. Its «Что именно менять» items 1-3 and 5 are builder items here;
  item 4 is the Lead's map edit. UNVERIFIED this round: the env_probe/audit line numbers (from the finding, 02.11).

**Env file parse (OH3-42)**
- F-16 Finding `plans/piles/onboarding-forge/findings/20261031-dva-razbora-env-fajla.md`: `env_probe.parse_env_file` (:103), `manual_capture._env_values`
  (:533, BOM/`export`/empty name/paired quotes), `stand_health._env_values` (:431, reads only `env_file`), `gate_preflight.configured_env_files` (:702)
  and `env_values` (:718), `brief_pack._env_file_key_names` (:2239). UNVERIFIED this round: these line numbers (finding of 31.10). Item 3 of the
  finding asks a scout's reader table first (12 files by grep).
- F-17 B-319 (BACKLOG.md:327) adds: `env_probe.load_env` merges with REVERSED priority (file over process); duplicated parse in
  `gate_preflight._loaded_env_files`, `config_contract.py:310`, `judge_run._env_files`, `project_inventory.py:338` (numbers of 05.10, UNVERIFIED).

**artifact_root (OH1-6, B-319, B-370)**
- F-18 Readers through `hooklib.artifact_root`: archive_task, baseline_contract, audit_factory, collect_pack, driver_journal, check_coverage,
  dashboard_refresh, controller, execution_request, estimate_record, exit_gate (+ more; grep). Hard-coded twins: `dispatch_liveness.py:800`
  (`driver-runs.jsonl`) and `:951` (`driver-state.json`) build `project_root / "qa-factory" / "artifacts"`; `vcs_evidence._story_root_of`
  (vcs_evidence.py:581-587) recognises a story only under `qa-factory/artifacts`. `brief_pack.py` prints `qa-factory/artifacts/<T>/...` literals
  (≥ 20 sites, e.g. :1135, :1852, :4068) — text for roles, FR-37 class, NOT in OH1-6's owns.

**Tests (where a new case may go; docs/TESTING.md, plans/builder-rules.md 7b)**
- F-19 `scripts/tests/test-layers.json`: `keep` = lines 35-6911, `quarantine` from :6966; `enforce_listing: true` (:12). Keep rows relevant here:
  `test_config_migration.py` (:729, detector, "sole AR-3 detector", covers config_contract.py and `fixtures/config-live-shape.json`),
  `test_project_knowledge.py` (:3938, register), `test_read_json.py` (:4070, data_join), `test_audit_rules.py` (:157), `test_dispatch_liveness.py`
  (:1293), `test_environment_record.py` (:1459), `test_grammar.py` (:2057), `test_manual_capture.py` (:2912), `test_test_locations.py` (:6230),
  `test_vcs_evidence.py` (:6387), `test_archive_task.py` (:86), `test_brief_pack.py` (:276). QUARANTINED (no new case, never a witness):
  test_check_coverage.py (:7325), test_import_test_receipt.py (:8357), test_judge_code.py (:8423), test_manual_actor.py (:8570),
  test_report_adapt.py (:9222), test_stand_health.py (:9813), test_test_novelty.py (:10184). No `test_env_probe*.py` row exists.
- F-20 Witness command (builder-rules.md:18): `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>`.

**Map**
- F-21 SIBLING_MAP axis 16 (:360-371) "one JSON reader" lists "the project-config reader class" as a twin still standing (:367); axis 8 (:216)
  lists `manual_capture.load_config` among outside walks; axis 35 (:599) names `contract.registry_sides` "the only reader of `product.sides` /
  `environments.sides` / `environments.reference_for` by key"; axis 30 (:462) one reader of `profiles[].commands`; axis 5 row (:127) the stand-login
  carriers. Axis 34 is P31 (:582), NOT the "memory of an answer" axis phase 0 planned (no axis names `remembered_answers` /
  `asked_until_answered`; case-insensitive grep, positive control `environment_record` at :462).

---

## §1 AR-n touched, owners and census classes, FR sections

| AR | How OF3-1 keeps it | Change check in the DoD |
|---|---|---|
| AR-1 | the `KEYS` literal of project_knowledge.py (closed variety in code) becomes catalogue rows (data); the comparator stays a named function selected by a row field | item 2 test `test_keys_come_from_the_catalogue` (no `KEYS = {` literal left; same five keys, same scope/compare) |
| AR-3 | every template key has a row with a default/`absent_means`; `artifact_root` gets its row (F4) | item 3 ratchet R1 in test_config_migration.py |
| AR-4 | `artifact_root` read by every story-path builder, no hard-coded `qa-factory/artifacts` in dispatch_liveness/vcs_evidence | item 7 tests in test_dispatch_liveness.py / test_vcs_evidence.py |
| AR-13 | one reader per fact: `project_knowledge.value/state/environment`; config through `read_config_file`; `test_data` through `test_data_states`; env file through `env_probe.parse_env_file`; JSON through `hooklib.read_json` | items 2, 5, 6, 8 tests + census R2 |
| AR-15 | one survivor per shared problem (env parse, BOM read), wired everywhere named | items 6, 8 |
| AR-20 | R2 and the read census are shrink-only; any raise named in the verdict | item 3 baseline file is shrink-only; builder STOPs on a raise |
| AR-22 | row ↔ reader: no row without a reader, no read without a row | ratchets R1-R3 |
| AR-28 | the reader never turns an unknown (absent / unreadable config, no row, twins) into a value; `value()` errs toward `unknown` | item 2 adversarial tests |
| AR-29 | the ratchets judge DATA (shape, join, presence) only; no meaning is judged | census below |

Owners and census classes of every check this spec adds or alters (CLAUDE.md rule 10, P27, AR-29):

| check | where | owner | census class | why it is not judgment |
|---|---|---|---|---|
| R1 template key ↔ catalogue row | test_config_migration.py (test, not a package unit) | data (code) | not a census unit (a test); detector layer | set equality of key names |
| R2 key read in code ↔ row (+ shrink-only exemption baseline) | test_config_migration.py | data | detector | a name found by a scan is present in a table |
| R3 row ↔ reader (`needed_by` names an existing `file:function`) | test_config_migration.py | data | detector | a name exists in a file |
| `project_knowledge.catalogue_problems` (ONLY if the builder needs a validator; u1 `*_problems`) | project_knowledge.py | data | `shape`, roles `[]`, row in `judgment-census.json` | form and presence; returns reasons, never raises |
| `value()`, `rows()`, `environment()` | project_knowledge.py | data | not units (names outside `UNIT_NAME_RE`, no refusal site) | readers |

No ratchet raise of `judgment-census.json` is expected or approved; a builder whose code would raise one STOPs and returns (AR-20).

FR sections walked: C (FR-13 closed variety in data; FR-17 one tool wired everywhere; FR-14 output shape of `value()`), D (FR-59 unknown never a
pass), F (FR-41 unknown never reported as fact — `value()` returns `problem`), G (FR-30 English, FR-32 root cause + test, FR-54 siblings by map),
E (FR-37 path the code writes = path named: `artifact_root`). A, B: no refusal or person text changes (B only if F3 (a): interview lines removed).

---

## §2 The catalogue (shape — subject to fork F1)

Recommended home (F1 (c)): a new top-level section `knowledge` in `references/config-keys.json`, one row per fact key:

| field | meaning (plan §2.1, as amended by §7 C6/C10) | phase-1 value |
|---|---|---|
| key (the object key) | the fact's permanent name = its config path (dotted; list element as `environments[].x`) or a registry key | e.g. `test_data.seeds`, `environments[].credentials_by_role`, `product.roles` |
| `about` | `project` · `environment` | from the key: `environments[]`/`environment.*` -> `environment`, else `project` |
| `store` | where the value lives | `config:<dotted path>` · `registry` (records/project-knowledge.json) · `config+registry` (accounts: config first, F-1 :194-212) |
| `compare` | element comparator for registry keys | `role_form` · `exact` (moved from `KEYS`); absent for config-only rows |
| `scope` | registry row scope | `project` · `stand` (moved from `KEYS`); absent for config-only rows |
| `ask_when` | when the factory learns it | see fork F2 (recommended: `null` everywhere in phase 1) |
| `derive` | probe/deriver name or `""` | `""` unless a deriver is already wired (the builder fills only ones it can cite file:function for) |
| `while_unknown` | what happens while unknown | phase 1: `default` for `absent_means: default` rows, `gap` for `required`, with C10's `safe_direction` text left `""` (filled in phase 2) |
| `needed_by` | readers, as `file.py:function` | every reader the census of item 6 finds; non-empty (R3) |
| `question`, `answer`, `person_class` | phase 2/4 fields | absent in phase 1 (the plan's fields arrive with their producers; AR-22) |

Granularity (fork F5): one row per top-level template key, plus a row per nested key that a reader reads by name in the classes of item 6
(`test_data.*`, `environment.*`, `environments[].*`), plus the five registry keys of F-1.

## §3 The reader `project_knowledge.py` (items 1.2)

- `rows(key=None) -> list[dict]`: the catalogue rows (copied dicts), read through `hooklib.load_ref_json`-style package read with BOM
  tolerance (`hooklib.read_json(ref("config-keys.json"), {}, kind=dict)`); an unreadable catalogue -> `[]` + module-level problem; never raises.
- `value(root, key, environment="", cfg=None) -> {"value", "state", "source", "problem"}`: PURE, never raises, writes nothing.
  - Order (POSITIONAL invariant: the catalogue is consulted first, so a key with no row can never read as `known`):
    (1) no row -> `state: unknown`, `problem: "no catalogue row for <key>"`; (2) `store` registry -> delegate to `state()`; (3) `store` config ->
    the config through ONE helper `_config(root, cfg)` that now calls `config_contract.read_config_file(root)`: `None` (absent) ->
    `state: unknown`, `source: "absent"`, `problem: ""`; `ConfigUnreadable` -> `state: unknown`, `problem: <its message, 200 chars>`;
    path missing -> `state: unknown`, `source: "config"`; present -> `state: known`, `value` as stored (no default substituted: the default
    belongs to the consumer in phase 1, so behaviour is unchanged); (4) `environments[].x` keys need `environment` (a NAME, exact) and read
    through `environment(name)`.
  - ERROR DIRECTION (a reader that later feeds a gate, plan §2.3): toward `unknown`, never toward `known`. Adversarial inputs that must stay
    `unknown` (each a test row): absent config; BOM-only file; empty file; `[]` / `"x"` / `null` document; a key with a row but a
    non-dict parent (`test_data: "x"` asked `test_data.seeds`); a key with no row; an unreadable catalogue; `environments` not a list;
    two stands of one name; stand name differing by case; the value present but `""` (state `known`, value `""` — NOT a default; the
    consumer keeps its own "blank = not recorded" rule, e.g. `test_data_states`).
- `state(...)`: unchanged contract (F-1); its `_config` switches to the same helper (`read_config_file`; `ConfigUnreadable` -> `{}` as today, so
  accounts read `unknown`, the same direction as now). `_usable` / `_form` read `scope` / `compare` from `rows()`.
- `environment(name, root=None, cfg=None) -> {"found", "entry", "problem"}`: the stand card from config only in phase 1 (no
  `environment-properties.json` / `stand-identity.json` merge — that is phase 3.2): exact name match in `environments[]`; empty or absent
  list -> `found: False, problem: "the project records no stand"`; not a list -> `problem: "environments is not a list"`; two of one name ->
  `found: False, problem: "two stands are named <name>"`; `name == ""` -> `found: False` (the choice of "the only stand" stays with
  `stand_gaps.stand_name`, F-1 phase 0 F-23 — no second picker; AR-13).

## §4 Edges (behaviour + the invariant each protects)

| edge | behaviour | invariant |
|---|---|---|
| a template key with no catalogue row | R1 red in CI naming the key and the door "add a row to config-keys.json `knowledge`"; at runtime `value(key)` -> `unknown` + problem | no template fact is outside the catalogue; an uncatalogued key never reads as known |
| a catalogue row with no reader (`needed_by` empty or naming a missing `file:function`) | R3 red naming the row; door: add the reader, or move the key to `removed` with a reason | no row survives that nothing reads (AR-22) |
| a key read in code with no row | R2 red naming `file:line` and the key; door: a row, or a baseline exemption line `<file>:<key> -- <reason>` (shrink-only; a new line is a raise named in the verdict) | a new read of an unknown key cannot land silently |
| a config value / file with BOM | every reader named in item 5 returns the SAME values as for the BOM-less file (one table test calling each) | a BOM never turns a project's config into defaults (FR-4) |
| the config file absent | `read_config_file` -> None -> `value` `unknown`/`absent`; `load_config` keeps `{}`; `artifact_root` keeps the default folder; the converted readers keep their present "no config" behaviour byte for byte | absent ≠ unreadable; neither becomes known; no reader changes its "not onboarded" behaviour |
| the config file unreadable (not JSON / not an object) | `value` `unknown` + the `ConfigUnreadable` message; GW1-38 readers keep their CURRENT fallback (each one's error direction is quoted in the report before/after; a reader that used to fall back to `{}` still does) | the refactor does not flip any reader's error direction (behaviour unchanged) |
| `environments[]` empty / absent / not a list | `environment(name)` -> `found: False` with the problem; no default stand invented | a stand fact never lands on a stand nobody recorded |
| two stands with one name | `found: False`, problem names it | a doubt is never one stand |
| `artifact_root` unset / set / empty / non-string / config broken | unset -> default folder as today; set -> dispatch_liveness and vcs_evidence look there; empty/non-string -> `hooklib.artifact_root` raises `ValueError` today: dispatch_liveness catches it and answers "unknown" (nothing is closed by absence — its own doctrine, config-keys.json:465), vcs_evidence treats it as "no story known" (its existing None path) | a configured root is honoured everywhere a story path is built; an unreadable root never closes a dispatch |
| env-file lines `A=1`, `export A=1`, `A="x"`, `A='x'`, `A="x'`, `=x`, `#c`, BOM first line, CRLF | one result for every reader (the finding's table) | one line means one thing to the brief and to the sign-in (AR-13) |
| `env_files` with two files | `stand_health` and `brief_pack` see both, later file wins, an empty value does not erase (manual_capture's rule) | the runner, the gate and the brief read the same files |
| `test_data` block absent / `none` / recorded / `unknown` | `env_probe.data_cleanup` returns what it returns today, now via `test_data_states` | two "unknown" tuples can no longer disagree |
| removed key still present in an old project config (F3 (a)) | migration reports it under `removed` with the reason (the existing road, config-keys.json:666-691); no value is used | an old config keeps working; a dead setting is named, not silently kept |
| the catalogue section absent (temporal: before the commit that creates it) | before: `KEYS` literal; after: rows. The same commit removes the literal and adds the rows (no world with both or neither); a package with an unreadable catalogue -> registry readers skip every row (toward asking) and `value` -> `unknown` | the change itself creates the section; no reader survives it half-wired |

## §5 Items (each: file/function, behaviour, test)

Recommended split into five parallel nodes (fork F7); items are numbered so either form works. Every test is a variant/table row in an EXISTING
keep file (F-19); no new test file.

1. **Catalogue rows** — `references/config-keys.json`: section `knowledge` per §2 (F1 (c), F2, F5); `about` string updated to name the section and
   its reader. Behaviour: none (no existing reader of config-keys.json reads `knowledge`). Test: `test_config_migration.py` row "the
   `knowledge` section does not change `migration_plan` on `fixtures/config-live-shape.json`" (the plan's witness "migration of a live-shape config
   with no value change": plan of the live fixture before == after, byte-equal).
2. **The reader** — `scripts/project_knowledge.py`: `rows`, `value`, `environment` new; `_config` -> `read_config_file`; `KEYS` literal removed,
   `_usable`/`_form` read the rows (AR-1). Tests in `test_project_knowledge.py`: `test_keys_come_from_the_catalogue`; one parameterised
   `test_value_toward_unknown` over every adversarial input of §3 (ids name the input); `test_environment_card_edges` (empty, absent, not a
   list, twins, case, `""`); `test_state_unchanged_for_phase0_keys` (the phase-0 fixtures give the same `state()` dicts).
3. **Ratchets R1-R3** — `scripts/tests/test_config_migration.py` + a shrink-only baseline `scripts/tests/fixtures/knowledge-read-baseline.json`
   (a fixture of that keep test: the builder registers it under `fixture_owners` in test-layers.json — a one-line data edit, not a new test file).
   R2's scan: in `scripts/*.py` (tests excluded), string keys read off an object that a config reader returned (`load_config(`,
   `read_config_file(`, `_config(`, `artifact_root`'s own) — a `.get("k")` / `["k"]` within the same function; nested keys only for the item-6
   classes. Every hit not covered by a row is a baseline line with a reason (e.g. `grammar.py:defect_classes_extra -- project extension key with
   no template row, queued`). Tests: R1, R2, R3 each one test; a mutation row each (a row deleted / a fake read added -> red).
4. **Removal of dead keys** (F3) — `config-keys.json` `removed` rows `format_all`, `records_policy`, `default_environment` (+ the `format_note` /
   `records_policy_note` note rows' fate per the existing note rule), `references/templates/config.json` the two keys and their notes; on F3 (a)
   also `skills/qa-onboarding/phases/p2-interview.md:281-288` and `p4-generate.md:129, :393-394` lose the lines that ask/write them.
   `test_data.seeds` / `.generators` STAY (F-12). Tests: `test_config_migration.py` rows "an old config holding each removed key: the plan names
   it under removed, no value used"; the existing list at test_config_migration.py:374-375 updated.
5. **BOM / one config reader (GW1-38)** — `check_coverage.py:99`, `environment_record.py:406`, `import_test_receipt.py:57`, `report_adapt.py:288`,
   `test_locations.py:745`, `test_novelty.py:320`, `grammar.py:293` read through `hooklib.read_json(..., kind=dict)` or
   `config_contract.read_config_file`, choosing per site the call whose error direction equals the site's current one (stated per site in the
   report). Test: one table row set in `test_read_json.py` — a BOM config and the same config without BOM give equal results from each of the
   seven readers (ids = reader names). Mutation: revert one site -> its row red.
6. **Census of reads past one reader + the test_data class** — (a) the builder runs and attaches a grep census of every project-config read in
   `scripts/*.py` (F-5, F-7, F-8) with a verdict per site: through `read_config_file`, `load_config`, `read_json`, or bypass; (b)
   `env_probe.data_cleanup` reads via `config_contract.test_data_states`, `CLEANUP_UNKNOWN` removed; `audit_factory.py:766` reads theme 3 via
   `test_data_states`; `brief_pack.py:2521` strategy path via `RP.home_dir(project) / "strategy"` (forge finding items 1-3, 5).
   Tests: `test_audit_rules.py` rows (template / no block); the no-bypass grep test of finding item 3 as a row in `test_config_migration.py`
   (positive control `config_contract.py`); env_probe's existing expectations unchanged. `environment` / `environments[]` readers: fork F6.
7. **artifact_root (OH1-6, B-319, B-370)** — catalogue row for `artifact_root` (store `config:artifact_root`, `absent_means: default`, template per
   F4); `dispatch_liveness.py:800` and `:951` and `vcs_evidence._story_root_of` read `hooklib.artifact_root(root=...)` with the §4 error behaviour.
   Tests: `test_dispatch_liveness.py` row "configured artifact_root: driver-runs/driver-state found there; broken root -> unknown";
   `test_vcs_evidence.py` row "output under a configured root names its story". The `brief_pack` literal paths (F-18) are NOT changed: queued (§7).
8. **One env-file parse (OH3-42)** — `env_probe.parse_env_file` takes `manual_capture._env_values`' rules (BOM, `export `, empty name skipped, one
   paired quote stripped); `manual_capture._env_values` calls it and keeps only `_env_files_state`; `stand_health._env_values` reads the file list
   through `gate_preflight.configured_env_files`; `brief_pack._env_file_key_names` unchanged in call, now consistent. First step: the reader table
   of finding item 3 (the builder's own grep with verdicts, attached; a scout dispatch is the Lead's call — fork F7 note). `env_probe.load_env`'s
   reversed priority (F-17) is stated in the table and NOT changed here (it changes behaviour) — queued.
   Tests: the finding's line table as one parameterised row set in `test_manual_capture.py` (keep; covers manual_capture.py — the builder confirms
   `covers` lists env_probe.py/stand_health.py or adds them to that row's `covers`, a data edit), calling each reader; two-file `env_files` row.

**DoD (every node)**: acceptance = the items' tests green + the census/report lines attached; verification run, attached verbatim:
`python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <the node's owns>` and
`python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang`. Slow files (scripts/slow_tests.json) are judged by CI only.
Every package commit carries `architecture: AR-n -- <how kept>` and `judgment:` lines. STOP and return on: an unlisted ratchet raise; a reader whose
error direction cannot be kept; any test expectation that must change to pass (behaviour changed).

**Builder owns (absolute paths; one node, or cut per F7 as marked a-e)**
- a: `C:\QAFactory\forge-repo\ai-packages\qa-factory\references\config-keys.json`, `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\project_knowledge.py`,
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_project_knowledge.py`, `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_config_migration.py`,
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\knowledge-read-baseline.json` (new fixture), `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test-layers.json` (fixture_owners line only),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\references\templates\config.json` (items 4, 7 per F3/F4), `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\config_contract.py` (ONLY if item 1's test shows `migration_plan`/`readiness` reading the new section — expected: no edit),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\skills\qa-onboarding\phases\p2-interview.md`, `C:\QAFactory\forge-repo\ai-packages\qa-factory\skills\qa-onboarding\phases\p4-generate.md` (F3 (a) only),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\t-129-of3-1a.md`
- b (item 5): `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\check_coverage.py`, `...\scripts\environment_record.py`, `...\scripts\import_test_receipt.py`, `...\scripts\report_adapt.py`,
  `...\scripts\test_locations.py`, `...\scripts\test_novelty.py`, `...\scripts\grammar.py`, `...\scripts\tests\test_read_json.py`, `...\changelog.d\t-129-of3-1b.md` (prefix `C:\QAFactory\forge-repo\ai-packages\qa-factory`)
- c (item 6): `...\scripts\env_probe.py` (`data_cleanup` only), `...\scripts\audit_factory.py` (theme-3 check only), `...\scripts\brief_pack.py` (strategy line :2521 only), `...\scripts\tests\test_audit_rules.py`, `...\changelog.d\t-129-of3-1c.md`
- d (item 7): `...\scripts\dispatch_liveness.py`, `...\scripts\vcs_evidence.py`, `...\scripts\tests\test_dispatch_liveness.py`, `...\scripts\tests\test_vcs_evidence.py`, `...\changelog.d\t-129-of3-1d.md`
- e (item 8): `...\scripts\env_probe.py` (`parse_env_file` only), `...\scripts\manual_capture.py` (`_env_values` only), `...\scripts\stand_health.py` (`_env_values` only), `...\scripts\tests\test_manual_capture.py`, `...\changelog.d\t-129-of3-1e.md`
- c and e share `env_probe.py` with disjoint functions (D-0048 form: the later merges main first). a's test_config_migration row of item 6 (no-bypass grep) waits for c.

**Siblings (the "one reader" class; SIBLING_MAP walk)**
- axis 16: the project-config reader class (:367) — folded here for the GW1-38 seven; the remaining `utf-8-sig` direct reads (F-8) and
  `install_smoke.py:414` are listed by item 6's census and queued as a node (F6); axis 16's twins row gets the census pointer (Lead).
- axis 8 (:216): `manual_capture.load_config` (an outside walk + its own config read) — census row; not changed (AR-13 residual, F6).
- axis 35 (:599): `contract.registry_sides` reads the registry by key past `project_knowledge` — it must keep working when `KEYS` moves to the
  catalogue (item 2 test reads the side keys); folding it into `project_knowledge.state` is queued (F6).
- axis 30 (:462): `profile_contract` is the one reader of `profiles[].commands` — its catalogue row's `needed_by` names it; no change.
- axis 5 row (:127): stand-login carriers — `environment.access` rows name their readers; no change in phase 1.
- `project_knowledge._config` (F-2) folded in item 2; `hooklib.artifact_root`'s own read stays (it raises on purpose, F-6) and gets a census
  exemption line with that reason.

## §6 Forks (returned; recommendation in bold, nodes executable on it)

- **F1 Where the catalogue lives.** The node row/§4 say a new `references/project-knowledge.json`; §7 C5 (which overrides §4, plan :322, :338)
  says "extend `config-keys.json`". Options: (a) new file (node row); (b) extend each `keys.<k>` row in place and add registry-only keys to
  `keys` — every existing reader of `keys` (`migration_plan`, `readiness`) would then see rows with no template key: a behaviour risk;
  (c) same file, new section `knowledge`. **(c)**: honours C5 (one file, joined by test), no existing reader sees the new rows. Cost: two
  sections joined by R1 instead of one map.
- **F2 `ask_when` values in phase 1.** Node row: fill `required -> onboarding`; §7 C6: "only introduce the field; values and the ≤ 10 ratchet in
  phase 4". **`null` in every row in phase 1** (C6 literally; nothing reads it; phase 4 sets values with its ratchet). Alternative: the node
  row's mapping without a ratchet (20 `onboarding` rows that phase 4 must undo).
- **F3 The "six dead keys".** Measured: `seeds`/`generators` are read (F-12); `requirements_sources` excluded by the owner (F-14);
  `default_environment` is not in the template (F-10). Options: (a) remove `format_all`, `records_policy` (template + `removed` rows) and add a
  `removed` row for `default_environment`, and strike their interview/generate lines (the only person-visible change: two fewer onboarding asks,
  under the owner's word 31.10); (b) defer the whole removal to OF3-4 with OH3-35; (c) remove from template only, leave the prose (an
  interview then asks for a key the template lacks — contradiction). **(a)**, and the Lead tells the owner that `seeds`/`generators` are NOT
  dead (the 31.10 word was given on the 30.10 audit) — keep them unless the owner says otherwise.
- **F4 `artifact_root` in the template.** (a) template key `"artifact_root": "qa-factory/artifacts"`: `migration_plan` fills it into every
  project config (bytes change, value equal) and `config-projection.json` may need a row so execution fingerprints do not go stale; (b)
  catalogue row + a documented note in the catalogue/`references` text, key stays out of the template (`in_template: false`, R1 allows it);
  **(b)**: documents the key (B-319's defect) with zero migration effect; behaviour unchanged.
- **F5 Catalogue granularity.** **top-level template keys + nested keys a reader reads by name in item-6 classes + the five registry keys**;
  alternative: every leaf of the template (~200 rows, most with no individual reader — R3 would force placeholder readers).
- **F6 How far 1.4 goes (one road, rule 6 / P31).** After OF3-1 about 49 scripts still read config through `load_config` (`{}` on error) beside
  `read_config_file` (raises) — two roads for one action with opposite error directions. Options: (a) convert all now (large, every
  `load_config` caller's "no-op on `{}`" doctrine must be re-proved — not a refactor); (b) phase 1 converts the classes named here and lands the
  census + R2 baseline as the shrink-only detector, each residual class a named node with owns and a test: N-r1 "`environment` /
  `environments[]` readers through `project_knowledge.environment`" (to phase 3.2, where the stand card is built), N-r2 "`load_config` callers
  through one reader with a declared error direction", N-r3 "`contract.registry_sides` through `project_knowledge`", N-r4 the remaining
  `utf-8-sig` direct reads (F-8). **(b)**; the cost of (a) is roughly 49 files and every hook's fail-open contract. The Lead takes the
  residual to the owner as P31 requires.
- **F7 One node or five.** **Five nodes a-e** (§5 owns): file-disjoint except `env_probe.py` (function-disjoint c/e); a first, b/c/d/e in
  parallel after it; OH3-42's "scout first" table is done by builder e as its first attached step (the Lead may instead dispatch a scout).

## §7 Files ALSO written by the absorbed batch-1 nodes (keep these nodes out of parallel batch-1 streams)

- OH1-6 (batch-1 :23): `scripts/hooklib.py`, `scripts/gate_preflight.py`, `scripts/dispatch_liveness.py`, `scripts/vcs_evidence.py`.
- OH3-42 (:30): `scripts/env_probe.py`, `scripts/manual_capture.py`, `scripts/stand_health.py`, `scripts/brief_pack.py`, their tests.
- GW1-38 (:31): `scripts/check_coverage.py`, `scripts/environment_record.py`, `scripts/import_test_receipt.py`, `scripts/report_adapt.py`,
  `scripts/test_locations.py`, `scripts/test_novelty.py`, `scripts/grammar.py`, their tests.
- OH3-35 (:27; only the key removal comes here, the rest goes to OF3-4): `skills/qa-onboarding/phases/p2-interview.md`, `p1-discovery.md`,
  `p4-generate.md`, `references/config-keys.json`, `references/templates/config.json`, `references/automation-candidacy.md`,
  `scripts/config_contract.py`, `scripts/onboard_apply.py`, `evals/evals.json`, their tests.
- Non-absorbed batch-1 nodes touching the same files (queue lines needed): OF1-1 (`env_probe.py`, depends on OH3-42 -> after node e);
  OF1-2 (`config_contract.py`, `config-keys.json`, `onboard_apply.py`, `p4-generate.md` -> queue with node a); OF1-4 (`gate_preflight.py`);
  OH1-3, DC1-7, CD1-11, LR1-5, OH3-36 (`hooklib.py` — OF3-1 does not edit hooklib.py on the recommendations); SC2-2 (`brief_pack.py`, node c
  edits one line).

## Contradictions and notes for the Lead (not widened)
- The batch-3 row says the forge `test_data` finding has "no place"; it is `plans/piles/forge/findings/20261102-chitateli-test-data-mimo-odnogo.md`.
- The batch-1 rows of OH1-6, OH3-35, OH3-42, GW1-38 carry no `перенос:` line to OF3-1/OF3-4 yet.
- GW1-38's line numbers drifted (F-7). OH3-35's "six keys" is five names, of which three are dead (F-12..F-14).
- Phase 0 planned SIBLING_MAP axis 34 "an answer kept across stories"; axis 34 is P31 and no such axis exists (F-21) — the memory axis is missing.
- `brief_pack` prints `qa-factory/artifacts/...` literals (F-18): a configured `artifact_root` is not what roles are told (FR-37) — a finding.
- `env_probe.load_env` reversed priority (F-17, B-319) is a behaviour change, not in this refactor — a finding/node.

## Small choices I closed
Section name `knowledge`; baseline fixture name `knowledge-read-baseline.json`; `value()` returns no default (consumer keeps its own);
`environment()` reads config only in phase 1; problem texts cut at 200 chars; tests as rows of existing keep files (F-19), the env table in
`test_manual_capture.py`, the BOM table in `test_read_json.py`; changelog fragment per node.

## Trail
Read: batch-3 file whole; project-knowledge-plan.md whole; t-2142 phase-0 spec whole; batch-1 file whole; findings 20261030 (BOM),
20261031 (env parse), 20261102 (test_data); BACKLOG.md:327 (B-319), :370 (B-370); config-keys.json whole; templates/config.json whole;
config_contract.py:1340-1379; hooklib.py:630-670, :690-797; judge_code.py:200-229; dispatch_liveness.py:84-103; project_knowledge.py:1-260 + def index;
test-layers.json:1-60, :725-754, :3936-3951 + section index; SIBLING_MAP.md heading index, :120-129, :202-227, :360-372, :460-463, :582-619;
audit 20261030 grep (:25, :42); builder-rules.md grep 7b.
Searches (positive controls in brackets): dead-key names case-insensitive over PKG [config-keys.json:186]; `artifact_root` over scripts [hooklib.py:636];
config.json `utf-8` / `utf-8-sig` reads [check_coverage.py:99, controller.py:4256]; `read_config_file\(` and `load_config\(` counts; test-layers names
[`test_config_migration.py` :729]; SIBLING_MAP memory-axis names [`environment_record` :462].
Not read (UNVERIFIED): docs/TESTING.md text; env_probe/manual_capture/stand_health/brief_pack line numbers of the OH3-42 finding; audit_factory.py:766;
architecture.md AR texts beyond the index; test_config_migration.py internals.
needed beyond the manifest: none read beyond the repo paths above.
