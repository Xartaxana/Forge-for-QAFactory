# t-129 — OF3-1 (phase 1 of the project-knowledge plan): the catalogue and one reader — SPEC (designer draft, fix rounds t-139, t-145)

Designer (Opus), 12.11.2026; fix round t-139 on the critic verdict t-137 (`docs/tasks/specs/reviews/t-137-of3-1-plan-critic.md`,
ACCEPT WITH FIXES); fix round t-145 on the second-pass verdict t-142 (`docs/tasks/specs/reviews/t-142-of3-1-plan-critic-pass2.md`,
ACCEPT WITH FIXES, X-1..X-10; §9). Draft for Lead acceptance. Fork status is in §6 (who closed each one); open forks carry a
recommendation and every node can be run on it.
Sources: `plans/piles/onboarding-forge/batch-3-znaniya-o-proekte-fazy-1-6.md:22-24` (node OF3-1); `plans/project-knowledge-plan.md` §2.1, §2.2,
§4 «Фаза 1» (:208-216), §6, §7 (:319-366; **§7 overrides §1-4**, :322); phase 0 spec `docs/tasks/specs/t-2142-project-knowledge-phase0.md`
(closed 5498318); absorbed rows of `plans/piles/onboarding-forge/batch-1-onboarding-roles-forge.md` (OH1-6 :27, OH3-35 :31, OH3-42 :34,
GW1-38 :35 — numbers as the critic re-read them on 8241f75).
PKG = `C:\QAFactory\forge-repo\ai-packages\qa-factory`. `path:line` were read on `main` in the first round (dc71a1b) or in the fix rounds
(marked "t-139" / "t-145"); critic-read numbers are marked "t-137" / "t-142"; anything else is marked UNVERIFIED.

## Digest

Phase 1 is a refactor with a short list of named fixes: (a) every fact the factory knows about a project gets ONE catalogue row (data,
AR-1/AR-3/AR-22); (b) the existing `scripts/project_knowledge.py` (phase 0) becomes the one reader of facts — `rows`, `value`, `state`,
`environment(name)` — reading config through `config_contract.read_config_file` and the catalogue through `config_contract.config_keys`
(AR-13); `project_knowledge.KEYS` stays as a name, now DERIVED from the registry rows in today's order; (c) three ratchets tie template keys,
code reads and readers to the rows (R1 lands first, R2/R3 land last, after the folds); (d) the reads that bypass one reader are folded by
class: config read without BOM (GW1-38), `test_data` read past `test_data_states` (forge finding), env-file parsed three ways (OH3-42),
`artifact_root` hard-coded at seven sites (OH1-6 / B-319 / B-370), and the owner-approved removal of `format_all` and `records_policy`
(OH3-35 sub-item, owner 12.11.2026). The residual of the class (F6 (b), owner 12.11.2026) leaves as queue nodes N-r1..N-r4 (+ N-r5, N-r6,
OF3-1d2), §7.

**Behaviour that changes (fixes; every other path is byte-for-byte as today):**
1. Onboarding no longer asks for or writes `format_all` and `records_policy` (F3 (a), owner 12.11.2026); an old config holding them gets a
   `removed` line in the migration plan.
2. BOM config (item 5): the seven GW1-38 readers today fall to `None`/`{}` on a BOM file; after, they read its values.
3. `check_coverage` cases-root reader (item 5): a config that is a non-empty JSON list today crashes at check_coverage.py:102; after, it
   reads as "no `cases_root`" (None).
4. `import_test_receipt._trusted_producer` (item 5): a config that is a JSON non-object today crashes (`.get` on a list); after, it is the
   same `ImportError` refusal as an unreadable file; the absent-config message text changes (§4).
5. `env_probe.data_cleanup` (item 6): `test_data: "x"` or a config that is not an object today crashes (`AttributeError`); after,
   `unknown` with today's unknown note.
6. Env-file parse (item 8): `env_probe.parse_env_file` (and so the login probe) reads `export A=1` as `A`, strips a leading BOM from the
   first name, strips only one PAIRED quote (`A="x'` keeps its quotes); `stand_health` sees every `env_files` entry, later file wins,
   an empty value does not erase.
7. Configured `artifact_root` (item 7): `vcs_evidence` (an `--output` inside an existing story folder of the configured root),
   `env_probe._case_needs`, `execution_scheduler`, `role_load._task_root` look under the configured root; `local_keys._taken` already does
   (local_keys.py:130-133, t-145) and only stops crashing on a config that is a JSON list. With no root configured they look where they look
   today. A root that cannot be read: the reader sites look where they look today; the two `execution_scheduler` job-store sites (writers)
   raise before anything is read, created or launched, as every `hooklib.artifact_root` writer does (fork F12; today the scheduler never
   read the config). (`dispatch_liveness` is the queued node OF3-1d2: there a broken root reads `unknown`, a stated change.)
8. Damaged catalogue (item 2; a state that could not occur before, the literal could not be damaged): `record_problems` refuses a key with a
   sentence naming the catalogue damage and the door "reinstall the plugin", not "not a project-knowledge key (the keys: )".

---

## §0 Facts (measured)

**What phase 0 left (the reader exists)**
- F-1 `scripts/project_knowledge.py` exists: `KEYS` literal (:49-55, five registry keys in this order: `product.roles`,
  `environments.credentials_by_role`, `product.sides`, `environments.sides`, `environments.reference_for`; each `{"scope", "compare"}`) with
  the comment "Phase 1's catalogue replaces this literal" (:47-48); `load` (:108), `state(...)` (:215-232, pure, never raises, toward
  `unknown`), `subjects` (:235), `roster` (:258).
- F-1b (t-139) `KEYS` has readers beyond `_usable`/`_form`: `project_knowledge.record_problems` :354-356 (the refusal text
  ``the key {key!r} is not a project-knowledge key (the keys: {', '.join(KEYS)}); nothing was recorded``), :360, :368 (`SIDE_KEYS`);
  `report_facts.py:1991`, `:1993` (`_key_of_mark`, a marker token matched against `PK.KEYS`), `:2180` (`for key in sorted(PK.KEYS)`);
  `scripts/tests/test_gate_role_accounts.py:82` (keep, test-layers.json:1995) reads `PK.KEYS[key]["scope"]`. (t-145: :349-372 re-read;
  `record_problems` returns at :356 before any other check when the key is outside `KEYS`.)
- F-2 `project_knowledge._config` (:163-170) reads `qa-factory/config.json` with its OWN `json.loads(... "utf-8-sig")`, broken/absent -> `{}`.
- F-3 `KEYS` drives `_usable` (:131-141) and `_form` (:96-99): a row whose key is outside `KEYS` is skipped (toward asking).
- F-3b (t-139) `project_knowledge.py` already imports `config_contract` lazily (:268, :383); `config_contract.py` holds no `project_knowledge`
  text (Grep content search, same call shape found `def _write_config` in the same file) — an eager import has no cycle.

**The config and catalogue readers and their error directions (§7 C16, C18)**
- F-4 `config_contract.read_config_file(root)` (:1349-1374): absent -> `None`; unreadable / empty / not JSON / not an object -> raises
  `ConfigUnreadable(ValueError)` (:1321) with a door; BOM tolerated. 9 package scripts call it.
- F-4b (t-139) `config_contract.config_keys()` (:1326-1338) is the existing reader of `references/config-keys.json`: unreadable / not an
  object / no `keys` table -> RAISES `ValueError` "the plugin install is damaged - reinstall the plugin".
- F-5 `hooklib.load_config(event)` (hooklib.py:792-796) = `read_json(config_path, {}, errors=Exception, kind=dict)`: absent, broken, not an
  object -> `{}`. 49 top-level `scripts/*.py` files contain `load_config(` (t-137 count).
- F-5b (t-139) `hooklib.read_json(path, default=None, *, errors=(OSError, ValueError), kind=None)` (:694-711): `utf-8-sig`; the caller owns the
  error direction through `default`, `errors` and `kind`.
- F-6 `hooklib.artifact_root(event=None, root=None)` (:636-649, t-139, re-read t-145): project = `root` or `project_root(event)`; its own
  `json.loads(... "utf-8-sig")` raises on a broken file (`JSONDecodeError`/`UnicodeDecodeError`, both `ValueError`), `OSError` on an
  unreadable file, `AttributeError` on a config that is a JSON list (:643 `cfg.get`); `artifact_root` absent -> `<project>/qa-factory/artifacts`;
  empty or non-string -> `ValueError`. Its comment :640-641: a broken config "must raise here, not become `{}` ... and silently put the
  artifacts into the default root (AR-28, AR-4)" — the writer direction.
- F-6b (t-145) `hooklib.is_story_folder(parent, name)` (hooklib.py:255-) is THE leaf "is the folder `name` under `parent` a story?" (axis 8):
  True only for one clean path component spelled exactly as in the listing of `parent` and being a directory; error direction "no" (its
  docstring :264-266: it may call a real story "no", never a file, an alias or a missing folder "yes"). It does NOT tell a story from any
  other directory under the parent. `pipeline.json` sits in a story folder (local_keys.py:127-128: "a folder without `pipeline.json` takes a
  number too"; hooklib.py:501-504 `pipeline.json` fields of a story).
- F-7 Direct project-config reads WITHOUT BOM — the seven GW1-38 sites, each read this round with its handler (t-139):

  | site | today: error -> | today: non-object document -> |
  |---|---|---|
  | check_coverage.py:99 (cases-root reader, :94-103) | any `Exception` -> return `None` | `[]` -> `{}` -> None; non-empty list -> `AttributeError` at :102 (crash) |
  | environment_record.py:406 | `(OSError, ValueError)` -> `{}` | passes through |
  | report_adapt.py:288 (`_context`) | `(OSError, ValueError)` -> `{}` | `{}` (:291) |
  | test_novelty.py:320 | any `Exception` -> `{}` | passes through; the next line checks `isinstance(cfg, dict)` |
  | test_locations.py:745 (`_config_of`) | any `Exception` -> `{}` | `{}` |
  | grammar.py:293 (`load_overrides`) | any `Exception` -> `{}` | `{}` |
  | import_test_receipt.py:57 (`_trusted_producer`) | `(OSError, JSONDecodeError)` -> `ImportError("configured external receipt adapter is unavailable: <exc>")`; absent -> `OSError` -> that refusal | `AttributeError` at :60 (crash) |

  install_smoke.py:414 reads a config too (not GW1-38; a parallel stream owns that file — N-r4).
- F-8 Direct reads WITH BOM but bypassing every reader: controller.py:4256/:4275/:4292, branch_accounting.py:200, dashboard_refresh.py:28,
  dispatch_liveness.py:94-95, env_probe.py:1114, factory_dashboard.py:725, judge.py:117 (+ the rest in item 6's census) — N-r4.
- F-8b Config WRITERS (§7 C18, AR-14; t-139): `config_contract._write_config` (:2190, docstring "The ONE writer of `qa-factory/config.json`");
  `project_decisions.py:455-460` (the decision-resolution path sets field pointers into the config it read); `runtime_probe.py:1487-1494`
  (`--suggest --write` sets `execution.runtime_probes.<profile>`). Three writers of one file (the plan's "≥ 3", review 20261110 :383).
  Inside the writer module a SECOND write site (t-145): `config_contract.restore_config` (:2529) writes the config itself at :2604
  (`_replace_bytes(target, final)`) when it reverts a story's window; what it keeps is decided by `_kept_pointers` (:2456) over
  `recorded_writes` (:2381), not by `written_by`.
- F-8c (t-145) The `written_by` table (`config-keys.json:705-714`: `execution.runtime_probes -> runtime_probe.py`,
  `adapters.ticket.method -> ticket_adapter.py`). Case-insensitive grep `written_by` over the package (positive control: the same call
  found `source_inventory.py:1130`): the table is pinned by `test_config_migration.py:193-197` and NAMED in a comment at
  `onboard_apply.py:971-973`; no production code reads it as data; `config_contract.py` has no hit (t-142 control `_write_config`).

**The catalogue's candidate home**
- F-9 `references/config-keys.json` carries per top-level template key `since`, `absent_means`, `project_fact` (:4-307), `notes`, `removed`
  (:666-691), `renamed`, `reasked`, `asked_until_answered`, `value_migrations`, `written_by` (:705-714). Its `about` (:2) says it is read by
  `config_contract.migration_plan` and `readiness.py`.
- F-10 `references/templates/config.json` (177 lines) has NO `artifact_root` and NO `default_environment`; it has `format_all` (:139),
  `records_policy` (:141), `test_data.seeds` / `.generators` (:75-76), `requirements_sources` (:92).
- F-11 `config-keys.json` has rows for `format_all` (:186-189) and `records_policy` (:190-193); `config-projection.json:32` lists
  `default_environment` under `decision_only` as "no reader in the package" (t-139); `config-projection.json` has no row for `format_all` or
  `records_policy` (t-139 grep, positive control the same call found :32).

**The dead keys (OH3-35)**
- F-12 `test_data.seeds` and `.generators` HAVE a reader (`judge_code.JUDGE_TEST_DATA_KEYS` :203, via `test_data_states`) — they stay.
- F-13 `records_policy`, `format_all`, `default_environment`: no reader in `scripts/*.py`. Hits outside production code (t-137 + t-139):
  config-keys.json, config-projection.json:32, templates/config.json, p2-interview.md:281-288, p4-generate.md:129/:393-394, CHANGELOG,
  fixture `run-12586-stand-config/qa-factory/config.json:63`, test_config_migration.py:374-375, test_config_revert.py:452,
  **test_reinstall_equals_fresh.py:150** (keep, test-layers.json:4259; `SEVEN_KEYS` holds `records_policy`, `format_all`),
  **test_project_decisions_stand_facts.py:45** (QUARANTINED, test-layers.json:9002; a fixture config holding `default_environment`).
- F-14 `requirements_sources` is excluded by the owner's word 31.10 (node OH3-39). The "six" is five names; three are dead; the owner
  (12.11.2026) removes two of them (`format_all`, `records_policy`); `default_environment` gets a `removed` row only (it is in no template).

**test_data (forge finding)**
- F-15 Finding `plans/piles/forge/findings/20261102-chitateli-test-data-mimo-odnogo.md`. One reader `config_contract.test_data_states`
  (:893-927, t-139): `absent` (no config / not an object / no `test_data`), `malformed` (block not an object), else per key
  `not_recorded` (missing, `None`, blank text), `unknown` (`TEST_DATA_UNKNOWN` :890 = `("unknown", "tbd", "?")`, any case), `none` (empty
  list), `recorded` (anything else, non-string included). Bypassers: `env_probe.data_cleanup` (:590-623, t-139; `CLEANUP_NONE` :586,
  `CLEANUP_UNKNOWN` :587 = `("", "unknown", "tbd", "?")`; `owner = str(td.get("cleanup_owner") or "").strip()` :604), `audit_factory.py:766`
  (UNVERIFIED this round; from the finding).

**Env file parse (OH3-42)**
- F-16 Finding `plans/piles/onboarding-forge/findings/20261031-dva-razbora-env-fajla.md`: `env_probe.parse_env_file` (:103-112, t-137),
  `manual_capture._env_values` (:533), `stand_health._env_values` (:431), `gate_preflight.configured_env_files` (:702), `env_values` (:718),
  `brief_pack._env_file_key_names` (:2239). The last five numbers UNVERIFIED (finding of 31.10).
- F-17 B-319 (BACKLOG.md:327): `env_probe.load_env` merges file over process; its docstring calls that order deliberate (env_probe.py:116-119,
  t-137) — so "reversed" is itself a question for the owner (§6 F11).

**artifact_root (OH1-6, B-319, B-370, B-348)**
- F-18 Readers through `hooklib.artifact_root`: archive_task, baseline_contract, audit_factory, collect_pack, driver_journal, check_coverage,
  dashboard_refresh, controller, execution_request, estimate_record, exit_gate (+ more).
- F-18b Hard-coded `"qa-factory" / "artifacts"` in production code (t-139 grep over `scripts/*.py`, positive control dispatch_liveness.py:800):
  `dispatch_liveness.py:800`, `:951`; `env_probe._case_needs` :678; `execution_scheduler.py:354`, `:574` (t-145 re-read: both build the
  job-store path `<...>/<task>/state/execution-jobs` the scheduler reads and then writes — :355 in `_apply_budget` after the
  `policy is None` return :348-349; :574 inside `execute_schedule`'s launch loop, after `state_dir.mkdir` :565-566);
  `local_keys._taken` :133 — a FALLBACK literal, not a hard-code (t-145): `_taken` already reads `hooklib.artifact_root(root=project)` :131
  and falls to the literal on `(OSError, ValueError)` :132-133; a config that is a JSON list raises `AttributeError` there, uncaught;
  `role_load._task_root` :537. Other hits of the grep are inline self-tests (archive_task.py:311-333, external_writes.py:1056-1158) and
  test files. `vcs_evidence._story_root_of` (:581-589) recognises a story only by the path parts `qa-factory`/`artifacts`;
  `left_out_by_person` (:592-) calls it at :611 OUTSIDE any try, then `Path(artifact_root()).iterdir()` at :613 inside `except OSError:`
  only (:612-615); with no story recognised every directory under the root is consulted (:613, docstring :596-601).
- F-18c B-348 (BACKLOG.md:350): `traceability.py --task-root <dir>` takes the bugs root as `parents[1]`, `--task <T>` takes
  `<project>/qa-factory`; with a configured `artifact_root` they read different folders.
- F-18d `brief_pack.py` prints `qa-factory/artifacts/<T>/...` literals (≥ 20 sites): text for roles, FR-37 class — finding, §7.

**Tests (docs/TESTING.md, plans/builder-rules.md 7b)**
- F-19 `scripts/tests/test-layers.json`: `keep` from :35, `quarantine` from :6966; `enforce_listing: true` (:12). Keep rows used here:
  `test_config_migration.py` (:729), `test_project_knowledge.py` (:3938), `test_read_json.py` (:4070; its G5 census `KEPT` at :388-426 is
  shrink-only with a stale-row check, :583-587), `test_audit_rules.py` (:157), `test_brief_pack.py` (:276), `test_config_projection.py` (:753;
  covers `env_probe.py` and `execution_scheduler.py`, :763, :766), `test_dispatch_liveness.py` (:1293), `test_gate_role_accounts.py` (:1995),
  `test_local_keys.py` (:2804), `test_manual_capture.py` (:2912), `test_reinstall_equals_fresh.py` (:4259), `test_report_facts.py` (:4292),
  `test_role_load.py` (:4448), `test_vcs_evidence.py` (:6387), `test_bug_records.py` (:364; covers `traceability.py`, :404).
  **Red at quarantine entry** (cohort 8073673, `keep_fail_at_entry`, :6934-6944): `test_audit_rules.py`, `test_brief_pack.py`,
  `test_role_load.py` — a builder adding a row there reports the pre-existing red rows by id and is judged on its own rows.
  QUARANTINED (no new case, never a witness): test_check_coverage.py, test_import_test_receipt.py, test_judge_code.py, test_report_adapt.py,
  test_stand_health.py, test_test_novelty.py, test_env_selected_stand.py (:7883), test_execution_scheduler.py (:7947),
  test_project_approach.py (:8977), test_project_decisions_stand_facts.py (:9002), test_traceability*.py (:10241-).
- F-19b (t-137 rerun) `--witness-for scripts/check_coverage.py` does not print `test_read_json.py`; `--witness-for scripts/env_probe.py` does
  not print `test_manual_capture.py`; `--witness-for references/config-keys.json` does not print `test_config_migration.py`.
- F-19c `test_runtime_paths.py` `OUTSIDE_WALKS` (:319-324) is shrink-only (:477-480) and holds `("manual_capture.py", "load_config")`.
- F-19d (t-145) Stream "tests" (t-135, branch `wip/of-tests`; `docs/tasks/onboarding-streams-2026-11-12.md:20`) runs OH3-25, whose row
  (`batch-2-onboarding-roles-forge-p3.md:61`) writes 13 test files, `test_brief_pack` and `test_report_facts` among them, plus
  `scripts/tests/harness.py`, `test_sizing.py`, `test_red_window.py`, `test_run_suite_mine.py`.
- F-20 Witness command (builder-rules.md 7b): `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>`.

**Map**
- F-21 SIBLING_MAP axis 16 (:360-371) "one JSON reader" lists "the project-config reader class" as a twin (:367); axis 8 (:216) lists
  `manual_capture.load_config` among outside walks and is the "story on disk" axis the artifact_root twins live on; axis 35 (:599)
  `contract.registry_sides`; axis 30 (:462) `profiles[].commands`; axis 5 row (:127) the stand-login carriers. Axis 34 is P31 (:582);
  no "memory of an answer" axis exists.

**Records carriers (plan 1.1 "всем записям records/")**
- F-22 (t-139) `references/install-paths.json:47-56` names project records: `journal.jsonl`, `estimation-ledger.jsonl`, `coverage-map.md`,
  `project-decisions.json`, `onboarding-approvals.jsonl`, `config-migrations/**`, `stand-identity.json`, `report-adaptations.json`,
  `environment-properties.json`, `project-knowledge.json`.

---

## §1 AR-n touched, owners and census classes, FR sections

| AR | How OF3-1 keeps it | Change check in the DoD |
|---|---|---|
| AR-1 | the `KEYS` literal (closed variety in code) becomes catalogue rows; `KEYS` survives as a value DERIVED from rows; the comparator stays a named function selected by a row field | item 2 row `record_problems` refuses a config-only key with the byte-equal text listing exactly the five registry keys in today's order |
| AR-3 | every template key has a row; `artifact_root` gets its row (F4 (b)) | R1 in test_config_migration.py (node a) |
| AR-4 | a configured `artifact_root` is honoured at every site that builds a story path: five sites here (c: `env_probe._case_needs`, `execution_scheduler.py:354`, `:574`; d: `role_load._task_root`, the `vcs_evidence` story recognition), two in OF3-1d2; `local_keys._taken` already honours it (d adds the third exception class only, t-145) | item 7 rows in test_vcs_evidence.py, test_config_projection.py, test_role_load.py; the list-config row in test_local_keys.py |
| AR-9 / FR-1 | the one refusal touched (`record_problems` :356) keeps its text and door byte-equal while the catalogue reads; with a damaged catalogue (`CATALOGUE_PROBLEM` set, §3) it names the damage and the door "reinstall the plugin" instead of a false cause and an empty key list (t-142 X-2); `import_test_receipt`'s refusal keeps its prefix and gains a cause for absent / non-object | item 2 rows (healthy: byte-equal; damaged: the damage sentence, nothing recorded); item 5 row |
| AR-13 | one reader per fact: `project_knowledge.value/state/environment`; config through `read_config_file`; catalogue through `config_keys`; `test_data` through `test_data_states`; env file through `env_probe.parse_env_file`; JSON through `hooklib.read_json`; artifacts through `hooklib.artifact_root`; "is it a story" through `hooklib.is_story_folder` | items 2, 5, 6, 7, 8 rows + R2 |
| AR-14 | the three config writers (F-8b) and `restore_config`'s write site inside the writer module are NAMED; this spec adds no writer and changes none; folding them into one is N-r6 | §7 N-r6 exists with owns and a test; no node a-f writes a config |
| AR-15 | one survivor per shared problem (env parse, BOM read, artifact root) | items 5, 7, 8 |
| AR-20 | R2 baseline, G5 `KEPT`, `OUTSIDE_WALKS` are shrink-only; folded sites DELETE their allow-list rows; any raise named in the verdict | items 3b, 5; builder STOPs on a raise |
| AR-22 | row ↔ reader: no row without a reader (R3 as (file, function, key) triples), no read without a row (R2); row fields without a phase-1 reader are absent | R1-R3; §2 field table |
| AR-28 | the reader never turns an unknown into a value; `value()` errs toward `unknown`; no artifact-root fallback reads a story the broken config did not point to that today's code would not have read; `vcs_evidence` narrows the consulted stories only to an existing story folder, so a folder that is not a story never hides a person's word (t-142 X-3); a writer site never writes into the default folder on a broken config (F12) | item 2 adversarial rows; item 7 rows, including "output under a configured root but not in a story folder: every story consulted" and "broken config: the scheduler raises, nothing created or launched" |
| AR-29 | the ratchets judge DATA (shape, join, presence) only | census below |

Owners and census classes of every check this spec adds or alters (CLAUDE.md rule 10, P27, AR-29):

| check | where | owner | census class | why it is not judgment |
|---|---|---|---|---|
| R1 template key ↔ catalogue row | test_config_migration.py | data (code) | not a census unit (a test); detector layer | set equality of key names |
| R2 key read off a config-bound name ↔ row (+ shrink-only baseline) | test_config_migration.py | data | detector | a name found by an AST scan is present in a table |
| R3 row ↔ reader triple | test_config_migration.py | data | detector | a (file, function, key) triple exists in R2's scan |
| `record_problems` refusal (text unchanged on a healthy catalogue; on a damaged one it states `CATALOGUE_PROBLEM` with its door, t-145) | project_knowledge.py | data | existing unit, class unchanged | presence of a key in a table; whether the table was read |
| `project_knowledge.catalogue_problems` (ONLY if the builder needs a validator) | project_knowledge.py | data | `shape`, roles `[]`, a row in `judgment-census.json` | form and presence; returns reasons, never raises |
| `value()`, `rows()`, `environment()`, derived `KEYS` | project_knowledge.py | data | not units (no refusal site) | readers |
| `vcs_evidence._story_root_of` configured-root recognition (t-145) | vcs_evidence.py | data | not a unit (a reader feeding an existing refusal) | a folder is in a listing and holds a named file |

No ratchet raise of `judgment-census.json` is expected or approved; a builder whose code would raise one STOPs and returns (AR-20).

FR sections walked: A (FR-1 the `record_problems` refusal unchanged on a healthy catalogue and naming the cause and door on a damaged one;
`import_test_receipt` refusal keeps its door), C (FR-13, FR-14, FR-17), D (FR-59), F (FR-41), G (FR-30, FR-32, FR-54), E (FR-37
`artifact_root`), B (onboarding loses the asks for `format_all` / `records_policy`, F3 (a); `p4-generate.md` gains one sentence on the
optional `artifact_root`, F4.1; no other person text changes).

---

## §2 The catalogue (F1 (c))

A new top-level section `knowledge` in `references/config-keys.json`, one row per fact key. Phase-1 fields are ONLY those with a phase-1
reader, plus `ask_when` (C6 asks that the field exist):

| field | meaning | phase-1 value | phase-1 reader |
|---|---|---|---|
| key (the object key) | the fact's permanent name = its config path (dotted; list element as `environments[].x`) or a registry key | e.g. `test_data.seeds`, `environments[].credentials_by_role`, `product.roles` | `value()`, R1-R3 |
| `store` | where the value lives | `config:<dotted path>` · `registry` · `config+registry` (accounts: config first, F-1) | `value()`, derived `KEYS` |
| `compare` | element comparator for registry keys | `role_form` · `exact` (moved from `KEYS`); absent for config-only rows | `_form` |
| `scope` | registry row scope | `project` · `stand` (moved from `KEYS`); absent for config-only rows | `_usable`, `record_problems`, `test_gate_role_accounts.py:82` via `KEYS` |
| `needed_by` | readers, as `file.py:function` | every reader R2's scan finds for the key; non-empty. Node a fills it from its own grep (attached); node f reconciles it through R3 (t-145) | R3 |
| `in_template` | `false` only for a key that is a fact but not a template key (`artifact_root`, F4 (b)) | absent = true | R1 |
| `ask_when` | when the factory learns it | `null` in every row (F2) | none in phase 1 (C6: introduced; phase 4 sets values with its ≤ 10 ratchet) |
| `about`, `derive`, `while_unknown`, `question`, `answer`, `person_class` | phase 2-4 fields | ABSENT in phase 1 (F-12 of t-137: no reader, AR-22; `while_unknown` waits for C10's `safe_direction`) | — |

Row order: the five registry keys appear in the section in the order of today's `KEYS` (F-1), so the derived `KEYS` keeps that order.

Granularity (F5): one row per top-level template key, plus a row per nested key that a reader reads by name in the classes of items 5-8
(`test_data.*`, `environment.*`, `environments[].*`), plus the five registry keys of F-1, plus `artifact_root`.

**Records carriers (plan 1.1, F-22; fork F8):** rows are made only for facts held in `project-knowledge.json` (the five registry keys). The
other carriers move with a reason: `environment-properties.json`, `stand-identity.json` -> phase 3.2 (the stand card merges them;
`environment()` reads config only until then); `project-decisions.json`, `report-adaptations.json` -> phase 2 (they carry decisions and
answers — the `question`/`answer` fields arrive there); `onboarding-approvals.jsonl`, `journal.jsonl`, `estimation-ledger.jsonl`,
`coverage-map.md`, `config-migrations/**` -> no row (logs and receipts of what happened, not facts about the project).

## §3 The reader `project_knowledge.py` (item 2)

- `rows(key=None) -> list[dict]`: the `knowledge` rows (copied dicts) read through `config_contract.config_keys()` (F-4b; ONE road to the
  table, t-137 F-11). Its `ValueError` (damaged plugin install) -> `[]` and a module-level `CATALOGUE_PROBLEM` string holding the message
  (200 chars); `rows()` itself never raises. A `config_keys()` dict with no `knowledge` section, or a section that is not an object -> `[]`
  with problem "references/config-keys.json has no `knowledge` section".
- `KEYS` (t-137 F-1): a module-level dict built ONCE at import from `rows()`: `{key: {"scope": row["scope"], "compare": row["compare"]}}` for
  every row whose `store` is `registry` or `config+registry`, in row order. Same five keys, same order, same values as today's literal.
  `report_facts` (:1991, :1993, :2180) and `test_gate_role_accounts.py:82` are NOT edited and keep working. A row with
  `store: registry` lacking `scope` or `compare` is left out of `KEYS` (toward "not a project-knowledge key" — refusal, never a guess) AND
  sets `CATALOGUE_PROBLEM` ("the knowledge row <key> has no scope/compare"; the first problem found is kept) (t-145).
- `record_problems` (t-142 X-2; the one edit of an existing function besides `_config`): when `key` is not in `KEYS` AND `CATALOGUE_PROBLEM`
  is non-empty, it returns ONE sentence ``the key {key!r} cannot be checked: the project-knowledge catalogue is damaged
  ({CATALOGUE_PROBLEM}); reinstall the plugin; nothing was recorded`` — never the "not a project-knowledge key (the keys: ...)" text. With
  `CATALOGUE_PROBLEM` empty the refusal is today's, byte-equal. POSITIONAL invariant: the damage branch sits ONLY on today's not-in-`KEYS`
  branch (:355), so a key present in `KEYS` is judged by today's checks and a healthy catalogue never reaches the new text; on both
  branches nothing is recorded. Error direction: a refusal either way, never a record; the only thing that changes is that the stated cause
  is the true one.
- `value(root, key, environment="", cfg=None) -> {"value", "state", "source", "problem"}`: PURE, never raises, writes nothing.
  - Order (POSITIONAL invariant: the catalogue is consulted first, so a key with no row can never read as `known`):
    (1) no row -> `state: unknown`, `problem: "no catalogue row for <key>"`; (2) `store` registry -> delegate to `state()`; (3) `store` config ->
    the config through ONE helper `_config(root, cfg)` calling `config_contract.read_config_file(root)`: `None` -> `state: unknown`,
    `source: "absent"`, `problem: ""`; `ConfigUnreadable` -> `state: unknown`, `problem: <its message, 200 chars>`; path missing ->
    `state: unknown`, `source: "config"`; present -> `state: known`, `value` as stored (no default substituted); (4) `environments[].x` keys need
    `environment` (a NAME, exact) and read through `environment(name)`.
  - ERROR DIRECTION (a reader that later feeds a gate, plan §2.3): toward `unknown`, never toward `known`. Adversarial inputs that must stay
    `unknown` (each a row of one parameterised test): absent config; BOM-only file; empty file; `[]` / `"x"` / `null` document; a non-dict
    parent (`test_data: "x"` asked `test_data.seeds`); a key with no row; a damaged catalogue; `environments` not a list; two stands of one
    name; stand name differing by case. The value present but `""` -> `state: known`, value `""` (NOT a default; the consumer keeps its own
    "blank = not recorded" rule).
- `state(...)`: unchanged contract; its `_config` switches to the same helper (`ConfigUnreadable` -> `{}` as today, so accounts read
  `unknown`, the same direction). `_usable` / `_form` read `KEYS` as today (now derived).
- `environment(name, root=None, cfg=None) -> {"found", "entry", "problem"}`: config only in phase 1: exact name match in `environments[]`;
  empty or absent list -> `found: False, problem: "the project records no stand"`; not a list -> `problem: "environments is not a list"`;
  two of one name -> `found: False, problem: "two stands are named <name>"`; `name == ""` -> `found: False` (the choice of "the only
  stand" stays with `stand_gaps.stand_name`; AR-13).

## §4 Edges (behaviour + the invariant each protects)

| edge | behaviour | invariant |
|---|---|---|
| a template key with no catalogue row | R1 red naming the key and the door "add a row to config-keys.json `knowledge`"; at runtime `value(key)` -> `unknown` + problem | no template fact is outside the catalogue; an uncatalogued key never reads as known |
| a row with `in_template: false` whose key IS in the template, or a key with no row and not in the template | R1 red naming it | `in_template` cannot hide a template key |
| a catalogue row with no reader | R3 red unless a (file, function, key) triple from R2's scan backs each `needed_by` entry (registry rows: the named function references the key's constant or literal); door: add the reader, or move the key to `removed` | no row survives that nothing reads (AR-22); a function that exists but never reads the key does not count |
| a key read off a config-bound name with no row | R2 red naming `file:function:key`; door: a row, or a baseline line `<file>:<function>:<key> -- <reason>` (shrink-only) | a new read of an uncatalogued key cannot land silently |
| R2 scan misses (an alias, a reassignment, a helper taking cfg under a name not in the carrier list) | silence (miss), never a false red on a non-config object; the item-6 census is the complementing list, and its bypass rows are N-r4 | the detector errs toward missing, so it never forces a row for a non-config object; misses are named in R2's docstring "BLIND TO" |
| damaged `config-keys.json` (unreadable, no `knowledge` section, section not an object) | `rows()` -> `[]`, `KEYS` -> `{}`, `CATALOGUE_PROBLEM` set: `record_problems` refuses every key with the damage sentence (§3) naming `CATALOGUE_PROBLEM` and the door "reinstall the plugin", nothing recorded; `_usable` skips every registry row (toward asking), `value` -> `unknown`, `report_facts` lists no fact; `config_contract`'s own callers (migration, readiness) still raise and name the damage | a damaged table never records or reads a fact as known, and a refusal never states a false cause or an empty door (FR-1; t-142 X-2) |
| a registry row lacking `scope` or `compare` (a half-damaged table) | that key is left out of `KEYS`, `CATALOGUE_PROBLEM` names the row; `record_problems` on that key -> the damage sentence; the other registry keys work as today | a half-read table never yields a guessed scope/comparator, nor the false cause "not a project-knowledge key" for a key the catalogue meant to carry |
| `record_problems` on a config-only key (e.g. `test_data.seeds`) with a healthy catalogue | refuses with today's text, the key list = exactly the five registry keys in today's order | config keys never enter the registry by the catalogue's growth |
| a config value / file with BOM | each of the seven item-5 readers returns the same values as for the BOM-less file | a BOM never turns a project's config into defaults (FR-4) |
| the config file absent | `value` `unknown`/`absent`; `load_config` keeps `{}`; `artifact_root` keeps the default folder; the converted readers keep their "no config" behaviour (F-7 table) | absent ≠ unreadable; neither becomes known |
| config unreadable / not an object | per site exactly the F-7 "today" column, except the two crash cells (check_coverage non-empty list -> None; import_test_receipt non-object -> refusal) | no reader flips its error direction; a crash becomes the reader's own "nothing there" or refusal, never a value |
| `import_test_receipt`, config absent | `ImportError("configured external receipt adapter is unavailable: qa-factory/config.json does not exist")` (today the same prefix + the OSError text) | an absent config never becomes "no producer configured = trusted" |
| `environments[]` empty / absent / not a list; two stands of one name | `environment(name)` -> `found: False` with the problem | a stand fact never lands on a stand nobody recorded; a doubt is never one stand |
| `artifact_root` unset | every item-7 site reads `<project>/qa-factory/artifacts` as today | the default world is byte-for-byte today's |
| `artifact_root` set to another folder | item-7 sites look there; `vcs_evidence._story_root_of` recognises `<configured root>/<T>` ONLY when `hooklib.is_story_folder(<root>, <T>)` is true AND `<root>/<T>/pipeline.json` is a file, where `<T>` is the first part of `--output` relative to the resolved root and `--output` lies BELOW `<root>/<T>`; else today's `qa-factory/artifacts/<T>` path-parts recognition; else no story (today's recognition kept as the second test) | a configured root is honoured; no `--output` that names its story today stops naming it |
| `--output` under a configured root but NOT in a story folder (e.g. `artifact_root: "."`, story `<project>/S-1` recorded "do not read MR U", `--output <project>/tmp/x.json`); also a story folder without `pipeline.json`, a file directly in the root, an `--output` on another drive or outside the root (`relative_to` fails) | no story recognised by the configured-root test -> today's path-parts test -> none -> every story under the root consulted (:613) -> S-1's word refuses | the person's "do not read" word is never skipped by narrowing the consultation to a folder that is not a story (t-142 X-3) |
| `artifact_root` empty / non-string / config broken / config a list / config unreadable (`ValueError`, `AttributeError`, `OSError`) | READER sites (`_case_needs`, `vcs_evidence`, `local_keys._taken`, `role_load._task_root`) catch exactly these three classes and fall back to today's path (the default folder; `vcs_evidence`: today's path-parts recognition). `vcs_evidence.py:612-615` is NOT widened (fork F10): with no story recognised, :613 behaves as today. WRITER sites (`execution_scheduler.py:354`, `:574`, job stores) do NOT catch: the root is resolved once per function before anything is read, created or launched, and a broken config raises (fork F12) | a broken config never makes a site read a folder today's code would not read; the person's "do not read this MR" word is never skipped by a new `return None`; a writer never splits a story's job store between the configured and the default folder (a job launched twice) |
| env-file lines `A=1`, `export A=1`, `A="x"`, `A='x'`, `A="x'`, `=x`, `#c`, BOM first line, CRLF | one result for every reader (the finding's table): `A`, `A`, `x`, `x`, `"x'` (unpaired, kept), skipped, skipped, `A`, no `\r` | one line means one thing to the brief and to the sign-in (AR-13) |
| `env_files` with two files | `stand_health` and `brief_pack` see both, later file wins, an empty value does not erase | the runner, the gate and the brief read the same files |
| `data_cleanup` mapping (item 6) | see the table in item 6 | no `test_data` value that reads `unknown` today reads `available` after |
| removed key still in an old project config (F3 (a)) | migration reports it under `removed` with the reason; no value is used | an old config keeps working; a dead setting is named |
| the catalogue section absent (temporal) | before node a: the `KEYS` literal; after: rows. The same commit removes the literal and adds the rows | no world with both or neither |
| R2/R3 absent (temporal: nodes a-e merged, f not yet) | R1 alone guards; reads added meanwhile are caught when f cuts its baseline from the then-current `main` | no read lands uncounted: f's baseline is cut after the last fold |
| node c before stream "tests" merges (temporal; t-142 X-1) | c is not dispatched; it starts from a `main` that holds OH3-25's `test_brief_pack.py` | no two writers on `test_brief_pack.py` at once |

## §5 Items (each: file/function, behaviour, test)

Every test is a variant/table row in an EXISTING keep file (F-19); no new test file; no source pin, no "as before" test, no in-test
mutation row (docs/TESTING.md table; t-137 F-13). Mutation probes (a row deleted, a site reverted -> red) are one-off runs in the builder's
report, never committed.

1. **Catalogue rows** (node a) — `references/config-keys.json`: section `knowledge` per §2; `about` names the section and its reader.
   `needed_by` (t-145, X-7): node a fills each row from its own grep of the readers (attached to the report, one line per row); R2 does not
   exist yet, so f reconciles the values through R3 (f owns the `needed_by` values).
   Test: `test_config_migration.py` row "`migration_plan` on `fixtures/config-live-shape.json` is byte-equal with the `knowledge` section
   present" (the plan's witness).
2. **The reader** (node a) — `scripts/project_knowledge.py`: `rows`, `value`, `environment` new; `_config` -> `read_config_file`; `KEYS`
   derived; `record_problems` gains the damage branch (§3). Tests in `test_project_knowledge.py`: `record_problems` on a config-only key
   refuses with the byte-equal text (behaviour row, replaces the source pin); one parameterised row set "damaged catalogue: the refusal
   names the damage and the door, nothing recorded" with ids `config_keys_raises`, `no_knowledge_section`, `registry_row_without_scope`
   (the damaged state is an INPUT: `config_contract.config_keys` patched to raise / to return a table without the section / with a
   registry row lacking `scope`, and the module re-imported so `KEYS` and `CATALOGUE_PROBLEM` are rebuilt — not a source mutation); one
   parameterised `test_value_toward_unknown` over §3's adversarial inputs (ids name the input); `test_environment_card_edges` (empty,
   absent, not a list, twins, case, `""`). The existing phase-0 tests of `test_project_knowledge.py`, `test_gate_role_accounts.py`,
   `test_report_facts.py` stay green unchanged (that is the "unchanged" proof; no new test for it).
3a. **R1** (node a) — `test_config_migration.py`: template key ↔ row, honouring `in_template: false`. One test.
3b. **R2, R3** (node f, after b-e merge) — `test_config_migration.py` + shrink-only baseline `scripts/tests/fixtures/knowledge-read-baseline.json`
   (registered under `fixture_owners` in test-layers.json). Place: test_config_migration.py is the registered "sole AR-3 detector" over config
   keys (test-layers.json:729-752); R2/R3 are joins of the same key table, so they live with R1 (t-137 F-13 "justify").
   R2's scan (AST, `scripts/*.py`, tests excluded): names BOUND to the return value of a config reader call (`x = load_config(...)`,
   `x = read_config_file(...)`, `x = CC.read_config_file(...)`, `x = _config(...)`, `x = read_json(<...config.json>, ...)`), plus parameters
   listed in the baseline's `carriers` list (e.g. `env_probe.data_cleanup:full_cfg`, `test_novelty.<fn>:cfg`); reads `x.get("k")`, `x["k"]`,
   and one nested level `(x.get("a") or {}).get("b")` / `x.get("a", {}).get("b")` / `x["a"]["b"]`. It yields (file, function, key) triples.
   Miss direction stated in its docstring: BLIND TO aliases, reassignment, helpers outside `carriers`; never red on a name not bound to a
   config reader. The no-bypass check of the forge finding (item 3 there) is NOT a separate test: `test_data.*` reads past `test_data_states`
   are R2 hits with no baseline line -> red (positive control in the report: one deliberate bypass on a scratch copy turns R2 red).
   R3: every `needed_by` entry of a `config:` row is backed by a triple; of a registry row, the named function references the key's
   constant or literal. One test each for R2 and R3.
4. **Removal of dead keys** (node a; F3 (a), owner 12.11.2026) — `config-keys.json`: `removed` rows `format_all`, `records_policy`,
   `default_environment` with reason; the `format_note` / `records_policy_note` note rows follow the existing note rule;
   `references/templates/config.json` loses the two keys and their notes; `skills/qa-onboarding/phases/p2-interview.md:281-288` and
   `p4-generate.md:129, :393-394` lose the lines that ask/write them. `test_data.seeds` / `.generators` STAY. `config-projection.json:32`
   is not edited (its `decision_only` line for `default_environment` stays true; small choice). Tests: `test_config_migration.py` rows "an
   old config holding each removed key: the plan names it under `removed`, no value used"; expected edits (carved out of STOP, DoD):
   `test_config_migration.py:374-375`, `test_reinstall_equals_fresh.py:150` (`SEVEN_KEYS` loses `records_policy`, `format_all`).
   `test_project_decisions_stand_facts.py:45` is quarantined: not edited, not a witness.
   **F4.1 sentence (t-145, X-7)** — `skills/qa-onboarding/phases/p4-generate.md`, in the paragraph listing the keys the phase writes,
   right after the sentence ending "unless an approved project mapping overrides it." (:131-132, before "A gap answered "later"..."):
   "`artifact_root` is optional and is not written by default: absent, the story folders live in `qa-factory/artifacts`; write it only
   when the team asks for the story folders elsewhere (a path relative to the project, or absolute)." A doc line, no test (no test reads
   phase prose; FR-33's live run is the proof of a role's behaviour).
5. **BOM / one config reader (GW1-38)** (node b) — each site takes the call whose error direction equals its F-7 "today" column:

   | site | new read | differs from today only in |
   |---|---|---|
   | check_coverage.py:99 | `hooklib.read_json(path, None, errors=Exception, kind=dict)` | BOM read; non-empty list -> None (was crash) |
   | environment_record.py:406 | `hooklib.read_json(path, {})` (default `errors=(OSError, ValueError)`, no `kind`) | BOM read |
   | report_adapt.py:288 | `hooklib.read_json(path, {}, kind=dict)` | BOM read |
   | test_novelty.py:320 | `hooklib.read_json(path, {}, errors=Exception)` | BOM read |
   | test_locations.py:745 `_config_of` | `hooklib.read_json(path, {}, errors=Exception, kind=dict)` | BOM read |
   | grammar.py:293 `load_overrides` | `hooklib.read_json(config_path, {}, errors=Exception, kind=dict)` | BOM read |
   | import_test_receipt.py:57 | `config_contract.read_config_file(root)`; `None` -> `ImportError("configured external receipt adapter is unavailable: qa-factory/config.json does not exist")`; `ConfigUnreadable` and `OSError` -> `ImportError(f"configured external receipt adapter is unavailable: {exc}") from exc` | BOM read; non-object -> refusal (was crash); absent-message cause text |

   Test: one table row set in `test_read_json.py` — a BOM config and the same config without BOM give equal results from each of the seven
   readers (ids = reader names), plus rows for the two changed crash cells. Allow-lists (t-137 F-15): delete the G5 `KEPT` rows
   `grammar.load_overrides` and `test_locations._config_of` (test_read_json.py:409, :423) — G5's stale-row check turns red otherwise.
6. **Census + the test_data class** (node c) — (a) the builder attaches a grep census of every project-config read in `scripts/*.py`
   (F-5, F-7, F-8) with a verdict per site: `read_config_file` / `load_config` / `read_json` / bypass; the census is input to N-r2/N-r4 and
   to f's baseline. (b) `env_probe.data_cleanup` reads `test_data` via `config_contract.test_data_states`; `CLEANUP_UNKNOWN` removed
   (`CLEANUP_NONE` stays). Mapping (t-137 F-7, completed t-139):

   | `test_data_states` result for `cleanup_owner` | `data_cleanup` state | note text | today |
   |---|---|---|---|
   | state `absent` (no config, non-object config, no `test_data`) | `unknown` | today's unknown note | same, except non-object config crashed |
   | state `malformed` (`test_data` not an object: `"x"`, `[]`, `null`) | `unknown` | today's unknown note | `"x"` crashed; `[]`/`null` -> unknown |
   | `not_recorded` (missing, `None`, blank) | `unknown` | unchanged | same |
   | `unknown` (`unknown`/`tbd`/`?`, any case) | `unknown` | unchanged | same |
   | `none` (empty list) | `unknown` | unchanged | same (`[]` falsy -> `""`) |
   | `recorded`, a falsy non-list (`False`, `0`) | `unknown` | unchanged | same (`str(x or "")` -> `""`) |
   | `recorded`, `str(value).strip().lower()` in `CLEANUP_NONE` | `absent` | `nobody resets this data (cleanup_owner: <str(value)>)` | same |
   | `recorded`, anything else (non-empty list included) | `available` | `cleanup_owner: <str(value).strip()>` | same |

   The stand part (`environments[]`, `safe_to_break`) is unchanged (N-r1). `audit_factory.py:766` reads theme 3 via `test_data_states`.
   `brief_pack.py:2904` strategy path via `RP.home_dir(project) / "strategy"` (t-137 F-14; the draft's :2521 was stale).
   Tests: `test_config_projection.py` (keep, covers env_probe.py) one table row set over the mapping above (ids = the left column); one
   `test_audit_rules.py` row set (template block / no block / `"x"`) asserting theme 3 and `data_cleanup` agree on "recorded vs not"
   (the join the finding names: two "unknown" tuples can no longer disagree); `test_brief_pack.py` row "a configured home folder: the
   strategy names come from `<home>/strategy`" (written after stream "tests" merges, on top of OH3-25's edit of that file; X-1).
7. **artifact_root (OH1-6, B-319, B-370; t-137 F-3, F-5; t-142 X-3, X-6, X-10)** — catalogue row `artifact_root` (store
   `config:artifact_root`, `in_template: false`, F4 (b); its `needed_by` = `hooklib.py:artifact_root`). Every site reads
   `hooklib.artifact_root(root=<the project root the site already has>)`. The caller owns its error direction (F-5b doctrine), by the
   site's KIND: a READER site catches `(OSError, ValueError, AttributeError)` -> today's path (§4); a WRITER site does not catch — it raises
   as every hooklib-routed writer does (F-6 :640-641; fork F12).
   - node c: `env_probe._case_needs` :678 (reader; root = `root or project_root()`; catches -> today's folder).
     `execution_scheduler.py:354`, `:574` (writers of job stores; root = `project_root`; X-10, fork F12): the root is resolved ONCE per
     function, before its loop and NOT caught — in `_apply_budget` right after the `policy is None` return (:348-349), in `execute_schedule`
     before `state_dir.mkdir` (:565) — so a broken config raises before any job store is read, any folder is created or any job launched;
     each request's store is `<root>/<task>/state/execution-jobs`. Why not today's folder: once a configured root is honoured, a story's
     jobs live under it; a fallback to the default folder on a broken config would make `store.read(idempotency_key)` miss them and LAUNCH
     the same job again (a split store), and would put artifacts where the config did not point (AR-28, AR-4). Today the scheduler never
     read the config, so the raise is a stated change (digest item 7). The traceback a writer prints instead of a refusal with a door is
     class-wide and pre-existing: finding (4), §7.
     Tests: `test_config_projection.py` rows "configured root: case needs found there" / "configured root: job store found there" /
     "broken config: case needs from today's folder" / "broken config: the scheduler's job-store path raises `ValueError`, no
     `state/scheduler-requests` or job-store folder is created and nothing is launched".
   - node d: `vcs_evidence._story_root_of` (reader; root = `hooklib.artifact_root()` with no arguments, the env-derived project root :613
     already uses). Recognition order (POSITIONAL invariant: a narrowed consultation is reached ONLY for a folder that is a story; every doubt
     falls through to the wider consultation): (1) `output` resolved, made relative to the resolved root (`ValueError` from `relative_to` =
     not under it); with at least two parts `<T>/<...>`, the story is `<root>/<T>` when `hooklib.is_story_folder(root, T)` is true AND
     `<root>/<T>/pipeline.json` is a file (F-6b); (2) else today's `qa-factory`/`artifacts` path-parts recognition; (3) else None -> every
     story consulted. A broken config (the three classes) skips (1) only. The reused leaf `is_story_folder`, in this more consequential role
     (it now narrows whose "do not read" words are consulted), may err ONLY toward "not a story" (= wider consultation); the `pipeline.json`
     marker is there because the leaf alone calls any directory under the root a story. Adversarial inputs that must stay on the safe side
     (no story by (1)): a plain folder under the root (`<project>/tmp` with `artifact_root: "."`); a story-named folder without
     `pipeline.json`; a file directly in the root; an `output` with `..` (resolved first); an `output` on another drive; a name differing
     from the listing by case or a trailing blank.
     `local_keys._taken` :132 (reader; X-6): the existing catch widens from `(OSError, ValueError)` to `(OSError, ValueError, AttributeError)`
     — nothing else changes (it already reads `hooklib.artifact_root(root=project)`). `role_load._task_root` :537 (reader; catches -> today's
     folder).
     Tests: `test_vcs_evidence.py` rows "output inside a story folder of the configured root names its story" / "output under the old
     default folder with a root configured elsewhere still names its story" / "output under a configured root but not in a story folder
     (`artifact_root: "."`, `--output <project>/tmp/x.json`, story S-1 recorded the MR): every story consulted, S-1's word refuses" / "a
     story folder without `pipeline.json` under a configured root: every story consulted" / "broken config: today's recognition, no
     traceback"; `test_local_keys.py` row "config a JSON list: today's folder, no crash" (the configured-root case is today's behaviour, no
     new row); `test_role_load.py` rows "configured root honoured; broken config -> today's folder".
   - queued OF3-1d2: `dispatch_liveness.py:800`, `:951` (§7).
   SIBLING_MAP axis 8 ("story on disk") is the axis these live on. B-348 (traceability `--task-root`) is N-r5. The `brief_pack` literal paths
   (F-18d) are not changed: finding (§7).
8. **One env-file parse (OH3-42)** (node e) — `env_probe.parse_env_file` takes `manual_capture._env_values`' rules (BOM, `export `, empty name
   skipped, one paired quote stripped); `manual_capture._env_values` calls it and keeps only `_env_files_state`; `stand_health._env_values`
   reads the file list through `gate_preflight.configured_env_files`; `brief_pack._env_file_key_names` unchanged in call. First step: the
   reader table of finding item 3 (builder e's own grep with verdicts, attached). `env_probe.load_env`'s merge order is stated in the table
   and NOT changed (F11). Tests: the finding's line table as one parameterised row set in `test_manual_capture.py` calling each reader;
   a two-file `env_files` row. Allow-lists: e changes no function listed in G5 `KEPT` (`stand_health._read`, `manual_capture._env_blocked_row`
   stay) and no outside walk (`manual_capture.load_config` stays in `OUTSIDE_WALKS`, N-r2) — no allow-list row moves.

**DoD (every node)**: acceptance = the node's rows green + the census/report lines attached; verification run, attached verbatim:
`python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <the node's owns>` and
`python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang`. Slow files are judged by CI only. A keep file red at quarantine entry
(F-19) is reported by row id; the node is judged on its own rows. Every package commit carries `architecture: AR-n -- <how kept>` and
`judgment:` lines. STOP and return on: an unlisted ratchet raise; a reader whose error direction cannot be kept; any test expectation that
must change to pass, EXCEPT the named expected edits: `test_config_migration.py:374-375` and `test_reinstall_equals_fresh.py:150` (node a,
F3 (a)), the G5 `KEPT` rows of item 5 (node b).

### Nodes and owns (absolute paths; prefix P = `C:\QAFactory\forge-repo\ai-packages\qa-factory`)

Order: a first; then b, d, e in parallel; c when a has merged AND stream "tests" (t-135, OH3-25, branch `wip/of-tests`) has merged into
`main` (X-1); f last (after b-e merge). None writes a file a live stream owns (`docs/tasks/onboarding-streams-2026-11-12.md:15-29`):
hooklib — `hooklib.py`, `install_smoke.py`, `hooks/run-py.cmd`, `references/launch-causes.json`, `cost_capture.py`, `factory_dashboard.py`
and their tests; hot — `stage_guard.py`, `controller.py`, `story_run.py`, `question_register.py` and their tests; handoff —
`handoff_init.py`, `handoff_check.py`, `test_handoff_init.py`, `test_handoff_values.py`; small — `dispatch_liveness.py`, `story_progress.py`,
`codex_usage.py`, `references/code-review-rubric.md`, `references/test-code-patterns.md`, `references/common-rules.md`,
`references/slices/`, `agents/qa-runner.md` and their tests; hooks4 — `gate_brief.py`, `test_gate_brief_and_retro.py`; tests (t-145) —
`scripts/tests/harness.py`, `test_run_suite_mine.py`, `test_red_window.py`, `test_sizing.py` and OH3-25's 13 files
(`test_traceability_report`, `test_grounding_table`, `test_validate_artifacts_report`, `test_oracle_provenance`, `test_s3_s4_chain`,
`test_s1_s2_contract`, `test_gate_question_form`, `test_brief_pack` — node c only after the stream merges, `test_exit_gate_grounding`,
`test_judge_results`, `test_judge`, `test_report_facts`, `fixtures/manual-evidence/scaffold.py`); misc — `friction.py`; doctor —
`skills/qa-doctor/`, `readiness.py`, `gate_preflight.py`, `project_gitignore.py`. Nodes c and d CALL `hooklib.artifact_root` /
`hooklib.is_story_folder`; neither writes `hooklib.py`.

- **a** (items 1, 2, 3a, 4; `covers` edits for all nodes):
  given: this spec; P\design\factory-rules.md; plans\builder-rules.md
  owns: `C:\QAFactory\forge-repo\ai-packages\qa-factory\references\config-keys.json`, `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\project_knowledge.py`,
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_project_knowledge.py`, `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_config_migration.py`,
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_reinstall_equals_fresh.py` (`SEVEN_KEYS` line only),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test-layers.json` (`covers` lines only: `test_read_json.py` += check_coverage.py, environment_record.py, import_test_receipt.py, report_adapt.py, test_locations.py, test_novelty.py, grammar.py; `test_manual_capture.py` += env_probe.py, stand_health.py; `test_config_migration.py` += references/config-keys.json, project_knowledge.py; `test_brief_pack.py` += brief_pack.py if absent),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\references\templates\config.json`, `C:\QAFactory\forge-repo\ai-packages\qa-factory\skills\qa-onboarding\phases\p2-interview.md`,
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\skills\qa-onboarding\phases\p4-generate.md`, `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\config_contract.py` (ONLY if item 1's row shows `migration_plan`/`readiness` reading the new section — expected: no edit),
  `C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\t-129-of3-1a.md`
- **b** (item 5): P\scripts\check_coverage.py, P\scripts\environment_record.py, P\scripts\import_test_receipt.py, P\scripts\report_adapt.py,
  P\scripts\test_locations.py, P\scripts\test_novelty.py, P\scripts\grammar.py, P\scripts\tests\test_read_json.py, P\changelog.d\t-129-of3-1b.md
- **c** (item 6; item 7 env_probe + scheduler): P\scripts\env_probe.py (`CLEANUP_UNKNOWN`, `data_cleanup`, `_case_needs` only, and the
  `import config_contract` line), P\scripts\execution_scheduler.py (`_apply_budget` :348-355 and `execute_schedule` :561-574 root lines
  only), P\scripts\audit_factory.py (theme-3 check only), P\scripts\brief_pack.py (strategy line :2904 only),
  P\scripts\tests\test_config_projection.py, P\scripts\tests\test_audit_rules.py, P\scripts\tests\test_brief_pack.py,
  P\changelog.d\t-129-of3-1c.md.
  **Depends on (t-142 X-1): stream "tests" (t-135, OH3-25, branch `wip/of-tests`) merged into `main`** — that stream writes
  `test_brief_pack.py`; c is dispatched only after it merges, from a `main` that holds it (`очередь: tests → OF3-1c`, §7 announcement).
- **d** (item 7 rest): P\scripts\vcs_evidence.py (`_story_root_of` only), P\scripts\local_keys.py (`_taken` except clause only),
  P\scripts\role_load.py (`_task_root` only), P\scripts\tests\test_vcs_evidence.py, P\scripts\tests\test_local_keys.py,
  P\scripts\tests\test_role_load.py, P\changelog.d\t-129-of3-1d.md
- **e** (item 8): P\scripts\env_probe.py (`parse_env_file` only), P\scripts\manual_capture.py (`_env_values` only), P\scripts\stand_health.py
  (`_env_values` only), P\scripts\tests\test_manual_capture.py, P\changelog.d\t-129-of3-1e.md
- **f** (item 3b): P\scripts\tests\test_config_migration.py (R2, R3 only), P\scripts\tests\fixtures\knowledge-read-baseline.json (new fixture),
  P\scripts\tests\test-layers.json (`fixture_owners` line only), P\references\config-keys.json (`needed_by` values only, if R3 shows a gap),
  P\changelog.d\t-129-of3-1f.md. f follows a serially on the shared files; no parallel overlap.
- Disjointness: the only shared file among parallel nodes is `env_probe.py` (c: `CLEANUP_*`, `data_cleanup`, `_case_needs`, import line;
  e: `parse_env_file`) — D-0048 form: the later of c/e merges `main` first. `test-layers.json` and `test_config_migration.py`, `config-keys.json`
  are written by a and f only, serially. `test_brief_pack.py` is shared with stream "tests" only in time: c starts after it merges (X-1).
- Witness scope: because a lands the `covers` edits first, b's and e's `--witness-for` print their new rows (F-19b closed).
- edges: §4. non-goals: §7 queue nodes; `load_env` order; `brief_pack` literals; `config-projection.json`. handoff: builder report + diff.

**Siblings (SIBLING_MAP walk)**
- axis 16 (:367): GW1-38 seven folded (b); `project_knowledge._config` folded (a); the remaining `utf-8-sig` direct reads (F-8) and
  `install_smoke.py:414` -> N-r4; `hooklib.artifact_root`'s own read stays (raises on purpose, F-6) and gets a baseline line in f.
- axis 8 (:216): artifact_root twins folded at five sites (c: 3, d: `role_load`, the `vcs_evidence` recognition), `local_keys._taken`
  gains the third exception class, two sites queued (OF3-1d2), B-348 -> N-r5; `manual_capture.load_config` -> N-r2; "is it a story" goes
  through `hooklib.is_story_folder` (+ the `pipeline.json` marker at the one site where a wrong "yes" hides a person's word).
- axis 35 (:599): `contract.registry_sides` keeps working (derived `KEYS`); folding it -> N-r3.
- axis 30 (:462), axis 5 row (:127): rows name their readers; no change.
- `KEYS` reader class (t-137 F-1): `record_problems`, `report_facts` ×3, `test_gate_role_accounts.py:82` — kept working by the derived `KEYS`.

## §6 Forks (status, who closed it)

| fork | answer | closed by |
|---|---|---|
| F1 catalogue home | (c) new section `knowledge` in `config-keys.json`, read through `config_contract.config_keys()` | coordinator provisional (Opus, 12.11) + critic t-137 concurrence with its condition (applied, F-11) |
| F2 `ask_when` in phase 1 | `null`; extended: `about`, `derive`, `while_unknown` absent | coordinator provisional + critic (t-137 F-12) |
| F3 dead keys | (a) remove `format_all`, `records_policy` (two fewer onboarding asks); `default_environment` a `removed` row; keep `seeds`/`generators` | **owner, 12.11.2026** |
| F4 `artifact_root` in the template | (b) catalogue row, `in_template: false`, no migration effect | coordinator provisional + critic. Sub-question F4.1 below (critic t-142 agrees with (a); the sentence is now in item 4) |
| F5 granularity | top-level keys + nested keys read by name in items 5-8 + five registry keys + `artifact_root` | coordinator provisional + critic |
| F6 how far 1.4 goes | (b) the classes named here + census + shrink-only R2; residual N-r1..N-r4 (§7). This also covers the move of `environment`/`environments[]` readers to N-r1 (phase 3.2), a deviation from the node row that the owner's word accepts | **owner, 12.11.2026** |
| F7 cut | was five nodes a-e (coordinator provisional); t-139 changed it to a-f + queued OF3-1d2 (t-137 F-4 (b), (c)); t-145 adds an ORDER only (c after stream "tests") | OPEN — re-accept the new cut (critic t-142 agrees, with X-1 applied) |
| F8 records carriers | §2: only `project-knowledge.json` keys get rows; the others move to phase 2 / 3.2 or get no row, reasons given | OPEN (new, t-137 F-9; critic t-142 agrees) |
| F9 C18 config writers | record them (F-8b) and fold in N-r6; NOT add them to `written_by` in phase 1. Reason (corrected t-145, F-8c): no production code reads the `written_by` table as data — it is pinned by test_config_migration.py:193-197 and named in a comment at onboard_apply.py:971-973; the revert keys on `recorded_writes` (:2381) / `_kept_pointers` (:2456). A row added now would change no outcome and fold nothing (a record without a reader, AR-22); `execution.runtime_probes -> runtime_probe.py` is already a row | OPEN (new, t-137 F-10; critic t-142 agrees with (a)) |
| F10 vcs_evidence broken root | keep today's path-parts recognition as fallback; do NOT widen :612-615 (t-137 F-3 (b) offered either) | OPEN (new; critic t-142 agrees) |
| F11 `load_env` file-over-process order | keep today's order (the configured file over the process environment); B-319's "reversed" sub-claim closes as by design. ADDED by the owner: when a value proves wrong and the person says to change it (e.g. the stand address), the change is written into the project's configuration (the configured file / config), not kept only in the run — a new queue entry N-r7 (§7) | **owner, 12.11.2026** |
| F12 writer sites on a broken config (t-145, from t-142 X-10) | (a) the two `execution_scheduler` job-store sites raise (no catch), the root resolved once per function before anything is read, created or launched | OPEN (new) — node c runs on (a) |

- **F4.1 Where a person learns `artifact_root`.** F4 (b) deviates from the OH1-6 row ("описан в шаблоне") and B-319; the catalogue is not a text
  a person opens. Options: (a) one sentence in `p4-generate.md` (node a owns it) naming the optional key and its default; (b) a line in a
  `references/` doc read at onboarding; (c) nothing until the template takes it. **(a)**: one sentence, already in a's owns; its place and
  text are in item 4 (t-145). Record the deviation on the node row.
- **F7 (re-open).** Five nodes became six plus one queued: R2/R3 moved from a to f so that no parallel node writes the baseline (the
  alternative, each of b-e removing its own baseline lines in one shared JSON file, invites merge conflicts); d lost `dispatch_liveness.py`
  to stream "small" (OF3-1d2 queued); c gained `_case_needs` and `execution_scheduler` (env_probe must not get a third writer; the only
  keep test covering `execution_scheduler.py` is `test_config_projection.py`, owned by c); d gained `local_keys`, `role_load`. **Accept
  a-f + OF3-1d2.** Alternative: d carries every artifact site and c leaves `_case_needs` (env_probe gets a third writer; d then also owns
  `test_config_projection.py`, which c needs for `data_cleanup`). t-145: c waits for stream "tests" (shared `test_brief_pack.py`); the
  test is not moved to another file — no other keep file covers `brief_pack.py` (F-19).
- **F8.** Options: (a) rows only for `project-knowledge.json` keys, the rest moved with reasons (§2); (b) a row per carrier now with
  `store: record:<file>` and `needed_by` naming today's readers — `value()` would have to return `unknown` "read through <reader>" for them,
  a row with no phase-1 reader through the one reader (AR-22 strain). **(a)**; it deviates from the node row's "всем записям records/"
  and the coordinator records the deviation on the node.
- **F9.** Options: (a) record the writers here, fold in N-r6; (b) fold them into `_write_config` now (writes `project_decisions.py`,
  `runtime_probe.py` and `config_contract.py`'s `recorded_writes` / `_kept_pointers`; changes write paths and the revert's kept-pointer
  logic — not a refactor). **(a)**. The plan (:356) says C18 "входит в фазу 1": this is a move, recorded on the node. Re-judged on the
  corrected fact (t-145): the reason "adding `written_by` rows could change revert outcomes" was false (nothing reads the table); (a) still
  wins on (b)'s cost alone.
- **F10.** Options: (a) fallback to today's recognition, :612-615 untouched — a broken config with no story recognised still raises at :613
  as it does today (a traceback; a pre-existing defect, finding §7); (b) widen :614 to `(OSError, ValueError, AttributeError)` -> `return None`
  — `None` means "nothing recorded, the tool runs", so a broken config would SKIP the person's "do not read this MR" word (unsafe direction;
  the docstring :599-601 says the tool "must not be the door around the word"). **(a)**.
- **F11.** B-319 calls `env_probe.load_env`'s file-over-process order "reversed"; env_probe.py:116-119 calls it deliberate. The owner says
  which is meant; until then nothing changes (item 8 states the order in its table). **Recommendation (t-145):** keep today's order (the
  project's file beats the process environment, as the docstring states) until the owner says otherwise, and on the owner's yes close
  B-319's sub-claim "reversed" as "by design". Cost of the other answer: one node on `env_probe.load_env` (order flip + a row in
  `test_manual_capture.py`), after node e.
- **F12 (new, t-145).** Item 7 had the scheduler's two job-store sites fall back to the default folder on a broken config, while
  `hooklib.artifact_root`'s own comment (:640-641) requires a broken config to raise for writers and every hooklib-routed writer raises
  (one action, two directions — P31). Options: (a) the sites raise: root resolved once per function before its loop, no catch — a broken
  config stops the scheduler before anything is read, created or launched; cost: a traceback instead of a refusal with a door (pre-existing,
  class-wide for writers: finding (4)), and a change from today, where the scheduler never read the config; (b) fall back to today's
  folder, with the direction and reason stated — cost: once a configured root is honoured, a broken config splits a story's job store and
  `store.read(idempotency_key)` misses the jobs under the configured root, so a job is launched a second time; artifacts land where the config
  did not point (AR-28, AR-4). **(a)** — one road with every writer; the one-road option is recommended by designer rule 6.

**Owner's word 12.11.2026 (in the coordinator session):** F3 — (a): remove `format_all` and `records_policy` (two fewer onboarding asks), keep `seeds` and `generators`; F6 — (b): phase 1 converts the classes named here and lands the census + shrink-only R2 baseline; the residual becomes four nodes N-r1..N-r4 with tests. Provisional coordinator answers (Opus, until the critic on plan t-137): F1 (c), F2 `null`, F4 (b), F5 as recommended, F7 five nodes a-e.

## §7 Queue entries (the coordinator places them in a batch file with ids and an owner; t-137 F-16)

Each is a node: owns + test. Target batch (t-145, X-8): a NEW `onboarding-forge` batch-4 (`batch-4-<slug>.md`, status «ожидает», a row in
the card's «Пачки» table — D-0044): batches 1-3 are all taken (Glob of `plans/piles/onboarding-forge/batch-*.md`: three files; t-142 read
batch-3's header "в работе"), and a taken batch takes no new nodes (PROJECT.md «Командная работа» 2). A node may instead go to the
project-knowledge phase batch it names.

| id | what | owns (prefix P) | test | when |
|---|---|---|---|---|
| OF3-1d2 | `dispatch_liveness.py:800`, `:951` read `hooklib.artifact_root(root=project_root)`, catching `(OSError, ValueError, AttributeError)` -> `unknown` (nothing is closed by absence, config-keys.json:465; `in_flight_entry` already catches these three, :955). Behaviour change: broken config reads `unknown` (today: the default folder) | P\scripts\dispatch_liveness.py, P\scripts\tests\test_dispatch_liveness.py | `test_dispatch_liveness.py` rows "configured root: driver-runs/driver-state found there; broken config -> unknown" | `очередь: small → OF3-1d2`; and `очередь: OF3-1d2 → N-r4` (both write `dispatch_liveness.py`) |
| N-r1 | `environment` / `environments[]` readers through `project_knowledge.environment` (the stand card) | the env-class rows of node c's census (known now: P\scripts\stand_gaps.py, P\scripts\env_probe.py `data_cleanup` stand lookup), P\scripts\project_knowledge.py | `test_project_knowledge.py` row: each census env reader gives the same stand as `environment(name)` over §4's stand edges; R2 baseline shrinks | phase 3.2 |
| N-r2 | `load_config` callers through one reader with a declared error direction per caller class (§7 C16) | P\scripts\hooklib.py (`load_config`) + the callers in the census; P\scripts\manual_capture.py (`load_config`, leaves `OUTSIDE_WALKS`) | `test_read_json.py` row set per caller class; `OUTSIDE_WALKS` shrinks | after streams "hooklib", "hot" merge AND node c's census is accepted (its owns are read off the census) |
| N-r3 | `contract.registry_sides` through `project_knowledge.state` | P\scripts\contract.py, P\scripts\project_knowledge.py | `test_project_knowledge.py` row: side keys give equal answers through both before the fold | after a |
| N-r4 | the remaining `utf-8-sig` direct config reads (F-8 + census) and `install_smoke.py:414` | P\scripts\controller.py, branch_accounting.py, dashboard_refresh.py, dispatch_liveness.py, env_probe.py (:1114), factory_dashboard.py, judge.py, install_smoke.py + census rows | `test_read_json.py` BOM rows per site; R2 baseline shrinks | after the streams owning those files merge; `очередь: OF3-1d2 → N-r4` (`dispatch_liveness.py`); `очередь: OF3-1c, OF3-1e → OF1-1 → N-r4` (`env_probe.py`) |
| N-r5 | B-348: `traceability.py --task-root` and `--task` read the bugs root by one rule (`hooklib.artifact_root`) | P\scripts\traceability.py | `test_bug_records.py` (keep, covers traceability.py) row: with `artifact_root: qa-artifacts`, both forms read the same folder | after d |
| N-r6 | C18: the three config writers (F-8b) end in `config_contract._write_config` (AR-14) | P\scripts\project_decisions.py, P\scripts\runtime_probe.py, P\scripts\config_contract.py (`_write_config` signature — it requires an `approval_ref` / `input_hash` the probe does not have; `recorded_writes`; `_kept_pointers`) | `test_config_migration.py` rows: each writer's change lands through `_write_config` (or a `written_by` row, decided in the node's spec); the revert keeps each writer's pointers as today (`restore_config`) | phase 2 (F9); after a and f (`test_config_migration.py`) and OF1-2 (`config_contract.py`) |
| N-r7 | Owner 12.11.2026 (F11): a stand value that proves wrong (e.g. the address) and that the person tells the factory to change is written into the project's configuration — the configured env file or config.json, whichever carries the key — not kept only in the run; the next run reads the corrected value | designer drafts first (where the person's correction is received today, which writer owns each carrier — AR-14, AR-24) | a row: a person's correction of a configured value lands in its carrier; a second run reads it | phase 2 or 3.2 (with N-r1, the stand card) |
| N-r8 | Owner 12.11.2026 (critic t-154 F2): `format_changed` (format only the files the story touched; TP2-2520) has no reader in code or role texts; it is passed to the automator (S5) so the role knows the one formatting command it may run; `format_all` stays removed | builder after OH5-9 merges (`brief_pack.py` is owned there): the S5 automator brief carries `format_changed` through `project_knowledge.value()`; the catalogue row's `needed_by` names that reader; empty value -> the brief says no narrow formatter is configured and the role does not format (never falls back to a wide command) | a row: configured value reaches the S5 brief; empty value gives the no-format line; R3 no longer finds an empty `needed_by` | node f or onboarding-forge batch-4 |

Announcement (t-137 F-4 (d); t-142 X-1): streams "hot" and "hooklib" are told, in their batch files as `очередь:` lines, that after node f
merges a new config read in their files needs a `knowledge` row or a baseline line; before f, f's baseline absorbs what they add. Stream
"tests" and node OF3-1c: the line `очередь: tests → OF3-1c` (shared `scripts/tests/test_brief_pack.py`; OH3-25 writes it first) is
appended in BOTH carriers — `batch-2-onboarding-roles-forge-p3.md` (OH3-25's batch) and `batch-3-znaniya-o-proekte-fazy-1-6.md` (OF3-1's
batch); a taken batch accepts appended `очередь:` lines (PROJECT.md «Командная работа» 2).

Findings to file (not nodes of this spec): (1) `brief_pack` prints `qa-factory/artifacts/...` literals — a configured root is not what roles
are told (FR-37); (2) `vcs_evidence.left_out_by_person` with a broken config and no story raises a traceback at :613 instead of a refusal
with a door (FR-1; pre-existing, F10); the same function, given an `--output` file placed directly in `qa-factory/artifacts/`, takes
`artifacts/<file>` for a story (`_story_root_of` :586-588) and consults only it — the person's word in a real story is skipped
(pre-existing; t-142 X-3 note); (3) F11 for the owner; (4) every writer routed through `hooklib.artifact_root` prints a traceback on a broken
config instead of a refusal with a door (FR-1; pre-existing, class-wide; F12 joins the scheduler to that class).

Files ALSO written by the absorbed batch-1 nodes (keep these out of parallel batch-1 streams): OH1-6 — `hooklib.py`, `gate_preflight.py`,
`dispatch_liveness.py`, `vcs_evidence.py`; OH3-42 — `env_probe.py`, `manual_capture.py`, `stand_health.py`, `brief_pack.py`; GW1-38 — the
seven item-5 files; OH3-35 (key removal only) — `p2-interview.md`, `p1-discovery.md`, `p4-generate.md`, `config-keys.json`,
`templates/config.json`, `automation-candidacy.md`, `config_contract.py`, `onboard_apply.py`, `evals/evals.json`. Non-absorbed batch-1
nodes on the same files (queue lines): OF1-1 (`env_probe.py`, after c and e; before N-r4); OF1-2 (`config_contract.py`, `config-keys.json`,
`onboard_apply.py`, `p4-generate.md`, after a and f); OF1-4 (`gate_preflight.py`); OH1-3, DC1-7, CD1-11, LR1-5, OH3-36 (`hooklib.py`, not
edited here); SC2-2 (`brief_pack.py`, c edits one line).

## Contradictions and notes for the Lead (not widened)
- The batch-3 row says the forge `test_data` finding has "no place"; it is `plans/piles/forge/findings/20261102-chitateli-test-data-mimo-odnogo.md`.
- The batch-1 rows of OH1-6, OH3-35, OH3-42, GW1-38 carry no `перенос:` line to OF3-1/OF3-4 yet.
- Phase 0 planned SIBLING_MAP axis 34 "an answer kept across stories"; axis 34 is P31 and no such axis exists — the memory axis is missing.
- Deviations from the node row to record on it: `environment`/`environments[]` to N-r1 (owner's F6 word); records carriers (F8);
  C18 to N-r6 (F9); `artifact_root` not in the template (F4).
- (t-145) The verdict t-142 says `written_by` "is read by onboard_apply.py:973"; that line is a COMMENT (:971-973) naming the table; no code
  there reads it (F-8c). F9's corrected reason rests on F-8c, not on that phrase.
- (t-145) The stream plan gives doctor `skills/qa-doctor/`, `readiness.py`, `gate_preflight.py`; the dispatch also names
  `project_gitignore.py` for doctor and `friction.py` for misc. All five are in §5's no-write list; none is in a-f's owns.
- (t-145) The dispatch's `handoff:` line named the spec itself; the handoff gate refused the Write (no new path inside docs/tasks/specs), so
  this revision travels as text in the designer's final message (designer rule 5 fallback).

## Small choices I closed
Section name `knowledge`; baseline fixture name `knowledge-read-baseline.json`; `value()` returns no default; `environment()` reads config
only in phase 1; problem texts cut at 200 chars; `KEYS` derived eagerly at import (no cycle, F-3b); `config-projection.json:32` untouched;
the env table in `test_manual_capture.py`, the BOM table in `test_read_json.py`, the `data_cleanup` table in `test_config_projection.py`;
changelog fragment per node; the absent-config `ImportError` cause text.
t-145: the damage sentence of `record_problems` (§3) and that it also covers a registry row lacking `scope`/`compare` (the first problem
found is kept); the damaged-catalogue test builds its state by patching `config_contract.config_keys` and re-importing; the story marker
`pipeline.json` (F-6b); the F4.1 sentence's wording and place; the scheduler's root is resolved before `state_dir.mkdir`.

## §8 Fix round t-139

| fix | applied | where in the spec |
|---|---|---|
| F-1 `KEYS` readers | applied: `KEYS` kept, derived from registry rows in today's order; refusal byte-equal; source pin replaced by a behaviour row | §0 F-1b; §2 row order; §3 `KEYS`; §4 two rows; item 2; §1 AR-1, AR-9 |
| F-2 STOP clause | applied: named expected edits carved out; `test_reinstall_equals_fresh.py` in a's owns | DoD; item 4; node a |
| F-3 artifact_root edges | applied: three exception classes; project-root source per site; old-default `--output` still names its story; behaviour-change list in the digest. Of (b)'s two options the fallback is taken, the except NOT widened — fork F10 with reason | digest list; §0 F-6, F-18b; §4 three rows; item 7; §6 F10; §7 OF3-1d2 |
| F-4 test ownership, collision | applied: all `covers` edits in a (lands first); R2/R3 to a new last node f; d's `dispatch_liveness` half queued `очередь: small → OF3-1d2`; R2 announcement to "hot"/"hooklib" | node a, f; §7 OF3-1d2, announcement; §6 F7 re-open |
| F-5 artifact_root class | applied: `env_probe._case_needs` and `execution_scheduler` in c, `local_keys`, `role_load` in d, B-348 -> N-r5; axis 8 named | §0 F-18b, F-18c; item 7; §5 siblings; §7 N-r5 |
| F-6 R2/R3 scope | applied: R2 bound to the name holding a reader's return value + declared `carriers`; miss direction stated; R3 as triples | item 3b; §4 rows |
| F-7 `data_cleanup` mapping, tests | applied: full mapping table (adds the falsy non-list and non-object cases); keep tests named (`test_config_projection.py`, `test_audit_rules.py`, `test_brief_pack.py`) | §0 F-15; item 6; §4 row |
| F-8 per-site direction | applied: table read this round, new call per site, `import_test_receipt` wrapping | §0 F-7; item 5; §4 rows |
| F-9 records carriers | applied as a move with reasons; fork F8 (deviation from the node row) | §0 F-22; §2; §6 F8 |
| F-10 C18 writers, AR-14 | applied: writers listed, AR-14 named, fold moved to N-r6; fork F9 | §0 F-8b; §1 AR-14; §6 F9; §7 N-r6 |
| F-11 `rows()` road | applied: `rows()` through `config_contract.config_keys()`, wrapped to `[]` + problem | §3; §4 damaged-catalogue row |
| F-12 phase-1 fields | applied: `about`, `derive`, `while_unknown` absent; `ask_when` null | §2 |
| F-13 tests | applied: source pin, "as before" test and in-test mutation rows dropped; R2/R3 place justified; no-bypass grep folded into R2 | §5 header; items 2, 3b, 5 |
| F-14 numbers | applied: `brief_pack.py:2904`; batch-1 rows :27/:31/:34/:35; env_probe `:587`, `:590` verified this round | header; §0 F-15; item 6; node c |
| F-15 allow-lists | applied: b deletes G5 `KEPT` rows `grammar.load_overrides`, `test_locations._config_of`; e moves none (stated) | item 5; item 8; §0 F-19c |
| F-16 residual as nodes | applied: N-r1..N-r4 (+ OF3-1d2, N-r5, N-r6) as queue entries with owns and a test; the two findings filed as notes; `load_env` -> owner (F11) | §7; §6 F11 |

Fixes kept as forks: none skipped. F-3 is applied with one of its two offered options; the choice is fork F10. F-9 and F-10 are applied
as moves; the moves are forks F8 and F9 (they deviate from the node row and the plan's "C18 входит в фазу 1").

**Did a fix change the architecture?** Yes, in both senses the dispatch names:
- AR-n set: AR-14 and AR-9 are added to §1 (AR-14 named, its fold moved to N-r6; AR-9 kept for the `record_problems` and
  `import_test_receipt` refusals).
- The cut: five nodes became a-f plus the queued OF3-1d2 (R2/R3 split off into f; `dispatch_liveness` out of d; artifact sites added
  to c and d). By PROJECT.md step 6 a second critic pass is owed; it can be narrow: §1, §5 nodes and owns, §6 F7-F10, §7.

**Picks and records of fix round t-145** (the coordinator's decisions applied; one line each):
- X-1: c depends on stream "tests" merging; `очередь: tests → OF3-1c` in both batch files; the test stays in `test_brief_pack.py` (no
  other keep file covers `brief_pack.py`, so a move is not the only fix); stream "tests" (and doctor, misc, hooks4) added to the no-write list.
- X-2 pick: `record_problems` names `CATALOGUE_PROBLEM` and the door "reinstall the plugin" whenever the key is outside `KEYS` and the
  catalogue is damaged — extended to a half-damaged table (a registry row lacking `scope`/`compare` also sets the problem) so no damaged
  state yields the false cause; a healthy catalogue keeps today's text byte-equal; nothing is recorded on any branch.
- X-3 pick: the critic's first option — `<root>/<T>` is a story only by `hooklib.is_story_folder` AND a `pipeline.json` file, else
  today's recognition, else every story consulted; every doubt widens the consultation, so a person's "do not read" word is never skipped.
- X-4: F9's reason replaced by F-8c (nothing reads `written_by` as data; onboard_apply.py:973 is a comment; the revert keys on
  `recorded_writes`/`_kept_pointers`); "UNVERIFIED" dropped; re-judged in one line, outcome (a) and the move to N-r6 stand.
- X-5: N-r6 owns gain `config_contract.py` (`_write_config` signature, `recorded_writes`, `_kept_pointers`) and the `restore_config` row;
  F-8b names `restore_config` :2604 as the writer module's second write site.
- X-6: F-18b, digest item 7 and item 7 say `local_keys._taken` already reads the configured root; d widens its catch only; its only new
  test row is the list-config row.
- X-7: the F4.1 sentence is in item 4 (file, place, text; doc line, no test); item 1 and §2 say a fills `needed_by` by grep, f reconciles.
- X-8: target is a new `onboarding-forge` batch-4; queue lines `OF3-1d2 → N-r4` and `OF3-1c, OF3-1e → OF1-1 → N-r4`; N-r2 waits for c's
  census.
- X-9: F11 carries the recommendation "keep today's order until the owner says otherwise; close B-319's sub-claim as by design on the
  owner's yes".
- X-10: the writer-site direction is stated — the scheduler's job-store sites raise like every hooklib writer; returned as new fork F12
  (recommended (a)); node c runs on (a).

## §9 Fix round t-145 (verdict t-142)

| X | applied | how | where |
|---|---|---|---|
| X-1 | applied | c waits for stream "tests" (OH3-25) to merge; `очередь: tests → OF3-1c` in batch-2 and batch-3; stream "tests" files (and doctor, misc, hooks4, the rest of hooklib/small) in the no-write list; test not moved | §0 F-19d; §4 temporal row; item 6 test line; §5 Order + no-write list, node c row, disjointness; §6 F7; §7 announcement |
| X-2 | applied | damage branch on today's not-in-`KEYS` branch of `record_problems`; half-damaged row also sets `CATALOGUE_PROBLEM`; row set of three ids in `test_project_knowledge.py`; AR-9 row corrected | digest item 8; §1 AR-9, census row, FR line; §3 `KEYS`, `record_problems`; §4 two rows; item 2 |
| X-3 | applied | configured-root recognition only for `is_story_folder` + `pipeline.json`; order and error direction of the reused leaf stated; adversarial inputs listed; two new `test_vcs_evidence.py` rows; the `artifacts/<file>` case into finding (2) | §0 F-6b, F-18b; §1 AR-13, AR-28, census row; §4 two rows; item 7 node d; §5 siblings; §7 finding (2) |
| X-4 | applied | false citation replaced by F-8c; F9 re-judged in one line; outcome (a), move to N-r6 kept | §0 F-8c; §6 F9 row and paragraph; contradictions note |
| X-5 | applied | N-r6 owns + `config_contract.py` (three functions), revert row added, order after a/f/OF1-2; F-8b second write site | §0 F-8b; §1 AR-14; §7 N-r6 |
| X-6 | applied | `local_keys._taken` described as already honouring the root; d widens the catch only; test row reduced to the list-config row | digest item 7; §0 F-18b; §1 AR-4; item 7 node d; node d owns; §5 siblings |
| X-7 | applied | F4.1 sentence placed in item 4 with file, place and text, "doc line, no test"; `needed_by` filled by a, reconciled by f | §2 `needed_by` row; item 1; item 4; §6 F4 row, F4.1 |
| X-8 | applied | new batch-4 as target; queue lines on `dispatch_liveness.py` and `env_probe.py`; N-r2 waits for c's census | §7 header, OF3-1d2, N-r2, N-r4 rows; batch-1 queue paragraph |
| X-9 | applied | recommendation and the other answer's cost added | §6 F11 row and paragraph |
| X-10 | applied as fork F12 (recommended (a), node c runs on it) | reader sites catch, writer sites (scheduler :354, :574) raise; root resolved once before anything is read, created or launched; split-store reason stated; test row "broken config: raises, nothing created or launched"; finding (4) | digest item 7; §1 AR-28; §4 broken-config row; item 7 node c; node c owns; §6 F12; §7 finding (4) |

**Did a fix change the architecture?** No for the AR set and the cut: §1 names no new AR-n (AR-4, AR-9, AR-13, AR-14, AR-28 rows are
corrected or widened in their change checks only); nodes a-f and their owns are the same files (c's `execution_scheduler.py` scope is
re-worded to the two functions holding the same lines; d's `local_keys` scope narrows to the except clause). Two things the Lead should
see: one ORDER dependency (c after stream "tests") and one new direction decision, fork F12 (a stated behaviour change at node c's writer
sites). Neither moves a file between nodes or into a live stream.

## Trail
First round: batch-3 file whole; project-knowledge-plan.md whole; t-2142 spec whole; batch-1 file whole; findings 20261030, 20261031,
20261102; BACKLOG.md:327, :370; config-keys.json whole; templates/config.json whole; config_contract.py:1340-1379; hooklib.py:630-670,
:690-797; judge_code.py:200-229; dispatch_liveness.py:84-103; project_knowledge.py:1-260; test-layers.json:1-60, :725-754, :3936-3951;
SIBLING_MAP.md :120-129, :202-227, :360-372, :460-463, :582-619.
This round (t-139): the critic verdict t-137 whole; project_knowledge.py:44-57 + `KEYS\b` grep (:49, :98, :136, :354, :356); `PK\.KEYS` grep
over scripts (report_facts.py:1991, :1993, :2180; test_gate_role_accounts.py:82); project_knowledge.py import grep; `project_knowledge` grep
in config_contract.py (empty; same call shape found `def _write_config`); config_contract.py:884-931, :1318-1339, writer grep (:2190);
vcs_evidence.py:575-624; env_probe.py:580-684; dispatch_liveness.py:794-803; hooklib.py:634-650, :694-711; the seven GW1-38 sites ±5 lines;
project_decisions.py:440-464 + config grep; runtime_probe.py:1480-1494; install-paths.json `qa-factory/records/` grep (:47-63);
`"qa-factory" / "artifacts"` grep over scripts/*.py (persisted output; production hits filtered); `"strategy"` / dead-key grep
(brief_pack.py:2904; test_reinstall_equals_fresh.py:150); test_project_decisions_stand_facts.py:38-49; config-projection.json:1-40 + dead-key
grep (:32 only); BACKLOG.md:350; test_read_json.py:376-495; test_runtime_paths.py:319-325, :477-480; test-layers.json rows: names grep,
:157-166, :753-776, :2912-2921, :6908-6969, covers grep for execution_scheduler/traceability/local_keys/role_load/vcs_evidence.
Not read (UNVERIFIED): audit_factory.py:766; manual_capture/stand_health/gate_preflight/brief_pack env numbers; docs/TESTING.md text (taken
from t-137).
Fix round t-145: the verdict t-142 whole; the spec whole; local_keys.py:120-140; execution_scheduler.py:343-362, :545-584;
hooklib.py:632-653, :255-269 (`is_story_folder`), `pipeline.json` grep in hooklib.py (:501-504; a first call with the pattern
`/ "pipeline\.json"` returned nothing — a shape miss, the plain pattern found the hits); project_knowledge.py:345-372;
vcs_evidence.py:575-624; config_contract.py def/`_replace_bytes(` grep (:2190, :2210, :2381, :2456, :2529, :2604) + :2590-2605;
case-insensitive `written_by` grep over the package (config-keys.json:705-714, onboard_apply.py:973, test_config_migration.py:193-197;
control: the same call found source_inventory.py:1130); config-keys.json:703-715; onboard_apply.py:962-985; `execution-jobs` grep over
scripts (run_suite/execution_request reach the job store through the artifact root); `def artifacts_dir|artifact_root\(` grep in
execution_request.py/run_suite.py; `def is_story|story_root...` grep; batch-2 :61 (OH3-25 row) + `test_brief_pack` grep over the pile;
Glob `plans/piles/onboarding-forge/batch-*.md` (three files); docs/tasks/onboarding-streams-2026-11-12.md whole; p4-generate.md:120-135 +
key grep (:129, :393-394).
needed beyond the manifest: plans/BACKLOG.md, references/install-paths.json, references/config-projection.json, scripts/report_facts.py
(grep only), scripts/project_decisions.py, scripts/runtime_probe.py, scripts/tests/test_read_json.py, scripts/tests/test_runtime_paths.py;
t-145: scripts/local_keys.py, scripts/execution_scheduler.py, scripts/hooklib.py, scripts/project_knowledge.py, scripts/vcs_evidence.py,
scripts/config_contract.py, references/config-keys.json, scripts/onboard_apply.py, skills/qa-onboarding/phases/p4-generate.md,
plans/piles/onboarding-forge/batch-2-onboarding-roles-forge-p3.md, docs/tasks/onboarding-streams-2026-11-12.md.
