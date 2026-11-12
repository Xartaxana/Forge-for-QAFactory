# t-137 — critic on plan: OF3-1 draft (designer t-130, file `docs/tasks/specs/t-129-of3-1-knowledge-catalog.md`)

Critic (Opus), 12.11.2026. Plan gate (CLAUDE.md rule 3; PROJECT.md new-owner-idea step 6). DoD of the work = node row OF3-1
(`plans/piles/onboarding-forge/batch-3-znaniya-o-proekte-fazy-1-6.md:24`) + plan §4 phase 1 (`plans/project-knowledge-plan.md:208-216`)
as overridden by §7 (:319-366). Code read on the current working tree (branch `pile/onboarding-hooks/batch-4`, HEAD 8241f75).

**Verdict: ACCEPT WITH FIXES (NEEDS WORK) — 7 fixes block dispatch to any builder (F-1..F-7), 9 more are edits of the same round (F-8..F-16).**
The direction (catalogue as a new `knowledge` section, one reader, three ratchets, five nodes) is sound; the draft is not yet
executable "for a weaker model" because (i) removing the `KEYS` literal breaks three readers the draft does not name, (ii) the
"behaviour unchanged" claim is false in four items and the DoD's own STOP clause would fire on its own item 4, (iii) the stated edge
behaviour of `vcs_evidence` leads into an uncaught raise, (iv) test ownership in `test-layers.json` is not cut between nodes, and
(v) one node collides with a running stream. This verdict is an input; accepting the draft is the coordinator's/Lead's decision.

---

## Key 1 — fit to the node row and the plan

| item | covered? | evidence |
|---|---|---|
| 1.1 rows for every template key | yes (§2, F5) | draft :141-157 |
| 1.1 rows for "всем записям `records/`" | **partly — silently narrowed** | draft :157 takes only the five `project-knowledge.json` keys. `install-paths.json` lists other project records carrying facts: `qa-factory/records/environment-properties.json`, `stand-identity.json`, `project-decisions.json`, `report-adaptations.json`, `onboarding-approvals.jsonl`. §3 :178-179 defers only the *reader merge* of two of them to phase 3.2, not their catalogue rows. -> F-9 |
| 1.2 `rows/value/state/environment`, via `read_config_file` | yes | draft :159-182 |
| 1.3 three ratchets | yes, with detector defects | draft :216-221 -> F-6 |
| 1.4 reads folded by class, `test_data`/`environment`/`environments[]` first | `test_data` yes (item 6); `environment`/`environments[]` **moved** to F6 N-r1 (phase 3.2) | draft :237, :306-307 — moved explicitly, but the node row puts them FIRST in phase 1; the move needs the coordinator's acceptance as a deviation from the node row, written on the node |
| absorbs OH1-6 / B-319 | partly: `artifact_root` row + dispatch_liveness/vcs_evidence; env-file half via item 8 | class incomplete -> F-5 |
| absorbs forge `test_data` finding | yes (items 1-3, 5 of the finding) | draft :232-237; mapping unstated -> F-7 |
| absorbs GW1-38 | yes (seven sites) | draft :227-231; per-site direction not stated -> F-8 |
| absorbs OH3-42 | yes (item 8) | draft :242-248 |
| absorbs dead keys of OH3-35 | yes, measured down to three (F-12..F-14) | draft :56-65, :222-226 — verified, see key 7 |
| §7 C16 (two error directions, "per caller class which it takes") | partly | draft punts per-site direction to the builder's report (:229) -> F-8 |
| §7 C18 (≥ 3 writers of config.json — "оба факта входят в фазу 1", plan :356) | **silently dropped** | draft :31 cites "C16, C18" as a heading, but no line names the writers (`config_contract._write_config`, `project_decisions.resolve`, `runtime_probe.py:1489`, review 20261110 :383) nor moves them -> F-10 |
| plan witness "миграция конфига живой формы без изменений значений" | yes | item 1 test :208-211 |

## Key 2 — "behaviour unchanged"

The digest (:11-17) says only F3 (a) changes person-visible text. False in these items; the draft does not say so:

1. **Item 2 removes `KEYS`, whose users include a refusal text.** `project_knowledge.record_problems` :354-356 builds the refusal
   ``the key {key!r} is not a project-knowledge key (the keys: {', '.join(KEYS)})``. If the replacement is "all catalogue rows" the
   refusal lists ~60 config keys and the guard admits config keys as registry keys; if it is "registry rows" the order must equal
   today's dict order. Also `report_facts._key_of_mark` :1991-1993 (`PK.KEYS`, "exactly one key ends so") and
   `report_facts` :2180 (`for key in sorted(PK.KEYS): PK.subjects(...)`) — with all rows, marker matching and the report's fact list
   change. `scripts/tests/test_gate_role_accounts.py:82` (keep, scenario) reads `PK.KEYS[key]["scope"]`. None of the three is named. -> F-1
2. **Item 7 changes liveness answers.** Today `dispatch_liveness.py:800/:951` read the default folder even when the config is broken;
   after, `artifact_root` raises and the draft answers "unknown" (:196). For a configured root, evidence that was missed is now found.
   Both are fixes in the safe direction, but they are behaviour changes. -> F-3
3. **Item 5 (BOM).** Today a BOM config makes all seven readers fall to `None`/`{}`; after, they read the values. Intended fix, unstated.
4. **Item 8 (env parse).** `env_probe.parse_env_file` (:103-112) today yields key `export A` for `export A=1`, key `﻿A` for a BOM
   line, and strips BOTH quote kinds from `A="x'`; taking manual_capture's rules changes env_probe's (and so the login probe's) values for
   those lines; `stand_health` starts seeing the second `env_files` entry. Fix in the right direction, unstated.
5. **Item 6 (`data_cleanup`).** Mapping unstated and not identity: `CLEANUP_UNKNOWN` (env_probe.py:587) contains `""`,
   `TEST_DATA_UNKNOWN` (config_contract.py:890) does not ("" is silence -> `not_recorded`); `cleanup_owner: []` today -> falsy -> `""`
   -> `unknown`, via `test_data_states` -> status `none`; `test_data: "x"` today -> `AttributeError` (env_probe.py:600 `.get` on a str),
   via `test_data_states` -> `malformed`. -> F-7
6. **P31 opposite directions (load_config `{}` vs read_config_file raises).** The draft names them (F-4/F-5, F6) and keeps them —
   honest. But it ADDS a new pair: `rows()` reads `config-keys.json` through `hooklib.read_json` -> `[]` (:161-162), while the existing
   reader `config_contract.config_keys()` (config_contract.py:1326-1336) RAISES on an unreadable table ("a plugin install problem").
   Two readers of one reference file with opposite directions, created by this spec. -> F-11
7. **DoD self-contradiction.** :254 "STOP and return on ... any test expectation that must change to pass", while item 4 requires
   changing `test_config_migration.py:374-375` and — unnamed — `test_reinstall_equals_fresh.py:150` (keep, `SEVEN_KEYS` holds
   `records_policy`, `format_all`), and item 2 breaks `test_gate_role_accounts.py:82` (keep). -> F-2

## Key 3 — architecture

- AR-3 kept (rows with `absent_means`), AR-13 kept in intent, AR-22: **inconsistent** — §2 :154 withholds `question/answer/person_class`
  "because the fields arrive with their producers (AR-22)", yet introduces `ask_when` (null), `derive` (""), `while_unknown`
  (`default`/`gap` VALUES) and `about`, none of which has a reader in phase 1 (only `store`, `scope`, `compare`, `needed_by` are read).
  C6 asks only that `ask_when` be "заведено"; `while_unknown` values without C10's `safe_direction` are worse than null. -> F-12
- AR-13 broken by the draft itself at `rows()` (F-11) and incompletely kept at `KEYS` (F-1).
- AR touched, not named: **AR-14** (config writers, C18 -> F-10); **AR-9/FR-1** (the `record_problems` refusal text, F-1);
  **AR-18** is not touched.
- Census: every new check has a class (§1 :121-131): R1-R3 test-layer detectors, optional `catalogue_problems` `shape`. Correct; no
  judgment moved into code (rows judge names/presence). JUDGMENT key: none found.
- Ratchets (AR-20): the new R2 baseline is shrink-only and named; the axis-16 G5 census in `test_read_json.py` (`KEPT`) and
  `OUTSIDE_WALKS` (test_runtime_paths.py) may shrink by node b/e — the draft should tell builders to shrink, not leave, those rows (F-15).

## Key 4 — items, edges, witness

- File/function/behaviour/test per item: present for 1-8, but:
  - Item 2 test `test_keys_come_from_the_catalogue` "no `KEYS = {` literal left" is a source pin (`docs/TESTING.md:92` "Пин исходника");
    `test_state_unchanged_for_phase0_keys` is the "Как раньше" row (TESTING.md table); R1-R3 "a mutation row each" and item 5
    "revert one site -> red" are "Отрицательный контроль внутри теста" (forbidden). R2 and item 6's no-bypass grep are structural
    invariants — TESTING.md says one row in a common ratchet, not a node's own test. -> F-13
  - Item 6 node c: the `data_cleanup` and `brief_pack` changes have only QUARANTINED tests (`test_env_selected_stand.py`
    test-layers.json:7883, `test_project_approach.py` :8977 — both after the `quarantine` start :6966); "env_probe's existing
    expectations unchanged" names no keep test. -> F-7
  - Item 6 `brief_pack.py:2521` is stale: :2521 is `_stand_pick`; the strategy literal is now `brief_pack.py:2904`
    (`project / "qa-factory" / "strategy"`). Node c's owns says "(strategy line :2521 only)". -> F-14
- Edges required by the dispatch: template key without row (§4 :188 ✓), row without reader (:189 ✓ but detector weak, F-6), key read in
  code without row (:190 ✓ but pair-detector, F-6), BOM (:191 ✓), absent config (:192 ✓), empty `environments[]` (:194 ✓).
- **Edge stated wrongly — `vcs_evidence` broken root (§4 :196).** "vcs_evidence treats it as 'no story known' (its existing None path)".
  The None path is `left_out_by_person` vcs_evidence.py:611-615: `roots = ... sorted_paths(... Path(artifact_root()).iterdir() ...)`
  inside `except OSError:` only. A broken/empty/non-string root raises `ValueError` there — uncaught. Today, with a broken config and
  `--output` under `qa-factory/artifacts/<T>`, `_story_root_of` (:581-588) finds the story WITHOUT calling `artifact_root`, so :613 is
  never reached and the call works; after item 7, `_story_root_of` -> None -> :613 raises -> the tool crashes. Behaviour flips from
  working to crashing. Also `_story_root_of(output)` has no project root argument; the draft's `hooklib.artifact_root(root=...)` names no
  root source (line 613 uses the env-derived one). And for a config whose root is elsewhere, an `--output` under the OLD default folder
  stops naming its story — unstated. -> F-3
- `artifact_root` edges for node d: `artifact_root` raises `json.JSONDecodeError`/`UnicodeDecodeError` (ValueError subclasses) on a
  broken file, but `AttributeError` on a config that is a JSON list (hooklib.py:642-643 `cfg.get`) and `OSError` on an unreadable
  file. "dispatch_liveness catches it" must name all three (`in_flight_entry` already uses `(OSError, ValueError, AttributeError)`,
  dispatch_liveness.py:955). -> F-3
- Witness command: correct form (`scenario_walk.py --witness-for`, builder-rules.md 7b); reran for node a's owns and parts of b/c/d
  (trail). Gaps: `--witness-for scripts/check_coverage.py` does NOT print `test_read_json.py` (node b's new table), and
  `scripts/env_probe.py` does not print `test_manual_capture.py` (node e's table) — the new rows would not be in the nodes' own
  witness unless `covers` is edited in `test-layers.json`, which only node a owns. -> F-4

## Key 5 — the cut into nodes a-e

- `env_probe.py` split c/e: verified disjoint — c = `CLEANUP_UNKNOWN` :587 + `data_cleanup` :590-…, e = `parse_env_file` :103-112;
  `CLEANUP_UNKNOWN` has no other user (grep: :587, :612 only). Shared hazard: c adds `import config_contract` at the module head. If
  F-5 brings `env_probe._case_needs` :678 (hard-coded artifacts) into node d, env_probe gets a third writer — then put :678 in c.
- **`test-layers.json` is not disjoint**: a owns it ("fixture_owners line only"), e is told to edit `covers` (:248), b needs to edit
  `covers` (F-4). -> F-4
- Order: a first, b/c/d/e after — correct (R2's baseline and the no-bypass row need the folded sites; the draft says a's item-6 row
  waits for c, :268). But R1-R3 land in a BEFORE b-e: R2's baseline must then hold lines b/c/d/e remove, and each of b-e shrinks it in
  `knowledge-read-baseline.json` — a file only a owns. Either each of b-e owns its own baseline lines (D-0048 form) or a lands the
  ratchets last. -> F-4
- **Collision with running streams:** node d writes `scripts/dispatch_liveness.py` and `scripts/tests/test_dispatch_liveness.py` —
  stream "small" owns `scripts/dispatch_liveness.py`. No other node writes `hooklib.py`, `install_smoke.py`, `cost_capture.py`,
  `factory_dashboard.py`, `stage_guard.py`, `controller.py`, `story_run.py`, `question_register.py` (checked against §5 owns :256-268).
  Indirect: R2 scans all `scripts/*.py`; reads the "hot"/"hooklib" streams add to controller.py/story_run.py/hooklib.py after the
  baseline is cut turn R2 red on their merge — they must be told (queue line or announcement). -> F-4

## Key 6 — provisional fork answers

- **F1 (c)** — agree. Condition: `rows()` reads through `config_contract.config_keys()` (F-11), and R1 joins the two sections.
- **F2 null** — agree for `ask_when`; extend the same rule to `while_unknown`/`derive`/`about` (F-12).
- **F3 (a) to the owner** — agree with routing. Add for her: the change also touches keep tests `test_reinstall_equals_fresh.py:150`,
  `test_config_migration.py:374`, fixtures `test_project_decisions_stand_facts.py:45`, `config-projection.json:32` (`default_environment`
  row in a reference file outside a's owns). The draft's negative "hits only in …" (:60-63) misses these.
- **F4 (b)** — agree (zero migration effect), but it deviates from the OH1-6 row text "ключ `artifact_root` описан в шаблоне" and
  B-319 ("не описан ни в шаблоне, ни в документах пакета"): (b) documents it only in a table the person never opens. Record the
  deviation on the node and name where a person learns the key (a `references/` doc line). Not blocking.
- **F5** — agree.
- **F6 (b) to the owner** — agree with the content; rule 19 / brief item 12 (d): N-r1..N-r4 must leave as nodes with ids and an owner in
  a batch file (and C16's per-class direction must be in this spec, F-8), not as "the Lead takes the residual to the owner".
- **F7 five nodes** — agree, with F-4's ownership edits and d queued after stream "small".

## Key 7 — facts by trail (spot-checks)

| claim | result | carrier |
|---|---|---|
| judge_code.py:203 reads `seeds`/`generators` via `test_data_states` | VERIFIED (:203 `JUDGE_TEST_DATA_KEYS`, :208-227 through `config_contract.test_data_states(read_config_file(...))`) | judge_code.py:203-228 |
| ~49 `load_config` caller files | VERIFIED: 49 top-level `scripts/*.py` files contain `load_config(` (incl. hooklib's def) | grep -l count |
| `read_config_file` 9 files, :1349-1374, BOM tolerated, raises `ConfigUnreadable` | VERIFIED (9; :1349; `utf-8-sig`; `ConfigUnreadable(ValueError)` :1321) | config_contract.py |
| `hooklib.artifact_root` :636-649, raises on broken config | VERIFIED (and also raises AttributeError for a non-object config — not stated) | hooklib.py:636-649 |
| `load_config` :792-796 `{}` on broken | VERIFIED | hooklib.py:792-796 |
| dispatch_liveness :800/:951 hard-code, vcs_evidence :581-587 | VERIFIED | — |
| only those two hard-code `qa-factory/artifacts` (F-18 "hard-coded twins") | **NOT TRUE** — production also: `env_probe._case_needs` :678, `execution_scheduler._apply_budget` :354, `execute_schedule` :574, `local_keys._taken` :133, `role_load._task_root` :537; B-348 (traceability `--task-root`, BACKLOG.md:350) | grep `"qa-factory" / "artifacts"` |
| seven GW1-38 sites at the stated lines | VERIFIED all seven (check_coverage:99, environment_record:406, report_adapt:288, test_novelty:320, test_locations:745, import_test_receipt:57, grammar:293) | read ±4 lines each |
| `KEYS` used only by `_usable`/`_form` (implied by item 2) | **NOT TRUE** — also `record_problems` :354-356, `report_facts.py` :1991, :1993, :2180, `test_gate_role_accounts.py:82` | grep `KEYS\b` |
| brief_pack strategy line :2521 | **STALE** — now :2904 | grep `"strategy"` |
| dead keys appear only in the listed files (F-13) | **INCOMPLETE** — also `test_reinstall_equals_fresh.py:150`, `test_project_decisions_stand_facts.py:45`, config-projection fixtures | case-insensitive grep, positive control config-keys.json:186 |
| batch-1 row numbers OH1-6 :23 … | drifted (now :27, :31, :34, :35) — cosmetic | batch-1 file |

---

## Findings and fixes (each a concrete edit of the draft)

**Blocking dispatch:**

- **F-1 (item 2, §3) — `KEYS` has three more readers.** Add to item 2: keep a module-level `KEYS` derived at import from the catalogue
  rows whose `store` is `registry` (same five keys, same order as today), OR convert `report_facts._key_of_mark`/:2180 and
  `test_gate_role_accounts.py:82` — and put `report_facts.py` into node a's owns. State that `record_problems`' refusal (:356) lists
  exactly the registry keys in today's order (byte-equal text). Replace the source-pin test with a behaviour row: `record_problems` on
  a config-only key still refuses.
- **F-2 (DoD :254) — carve the STOP clause.** "STOP on any test expectation that must change, EXCEPT the named ones:
  `test_config_migration.py:374-375`, `test_reinstall_equals_fresh.py:150` (F3 (a))"; add `test_reinstall_equals_fresh.py` to a's owns.
- **F-3 (item 7, §4 :196) — artifact_root edges.** (a) dispatch_liveness: catch `(OSError, ValueError, AttributeError)` from
  `artifact_root` -> unknown; (b) vcs_evidence: state where the project root comes from (`hooklib.artifact_root()` env-derived, as :613),
  and the broken-root path: `_story_root_of` must not route into :613's uncaught raise — either widen :612-615's except to the same three
  classes (-> return None, "feature absent") or keep the default-folder recognition as a fallback; (c) say what happens to an `--output`
  under the old default folder when the root is configured elsewhere; (d) list these two liveness changes and the vcs change in a
  "behaviour that changes (fixes)" section of the digest.
- **F-4 (§5 owns) — test ownership and stream collision.** (a) Give every node its own `covers` edits in `test-layers.json` (D-0048
  form, disjoint rows) or move all covers edits into a; name for b: `test_read_json.py` covers += the seven files; for e:
  `test_manual_capture.py` covers += `env_probe.py`, `stand_health.py`. (b) R2 baseline: either a lands R1-R3 after b-e merge, or each of
  b-e owns the removal of its own baseline lines. (c) Queue node d after stream "small" (`очередь: small → OF3-1d`), or move d's
  dispatch_liveness half out until "small" merges. (d) Announce R2 to streams "hot"/"hooklib" (new config reads in their files need a row
  or baseline line).
- **F-5 (item 7, siblings) — artifact_root class incomplete.** Name `env_probe._case_needs:678`, `execution_scheduler.py:354/:574`,
  `local_keys._taken:133`, `role_load._task_root:537` and B-348 (traceability `--task-root`): fold them in d (with owns and a test row)
  or queue them as a named node; also name SIBLING_MAP axis 8 (story on disk) as the axis these live on.
- **F-6 (item 3) — R2/R3 are pair-detectors not scoped to one carrier (critic rule 15).** R2: "a `.get("k")` within the same function as
  a config reader call" fires on `pipeline.get("ticket")` in a function that also calls `load_config()`, and misses reads through a
  `cfg` parameter (e.g. `data_cleanup(full_cfg)` env_probe.py:590). Scope R2 to the NAME bound to the reader's return value (and
  parameters named in the baseline as config carriers), and state the miss direction. R3: "`needed_by` names an existing
  `file:function`" is green when the function exists but never reads the key — join R3 to R2's scan as (file, function, key) triples.
- **F-7 (item 6, node c) — `data_cleanup` mapping and tests.** Write the mapping table: status `not_recorded` -> `unknown`; `unknown` ->
  `unknown`; `recorded` with a `CLEANUP_NONE` word -> `absent`; other `recorded` -> `available`; `none` (empty list) -> `unknown` (as
  today, `[]` is falsy); block `absent` -> `unknown`; `malformed` -> `unknown` (today a crash — a stated fix). Name a keep test for
  `data_cleanup` and for the `brief_pack` strategy line (both current tests are quarantined) or record "no keep row covers" as the report
  line builder-rules 7b prescribes.

**Same round, non-blocking for dispatch but required before acceptance of the draft:**

- **F-8 (item 5, C16)** — put the per-site error direction in the spec, not the builder's report: check_coverage -> `None` on any error;
  environment_record -> `{}` on OSError/ValueError (non-object passes through); report_adapt, test_locations, grammar -> `{}` incl.
  non-object; test_novelty -> `{}`; import_test_receipt -> `ImportError` on OSError/JSONDecodeError. Note: moving import_test_receipt to
  `read_config_file` changes absent (`None`, then `.get` crash) and `ConfigUnreadable` (a ValueError, not caught by its
  `except (OSError, json.JSONDecodeError)`) — state the wrapping.
- **F-9 (§2, 1.1)** — enumerate the `records/` carriers (environment-properties, stand-identity, project-decisions, report-adaptations,
  onboarding-approvals) with a row each or an explicit move to the phase that reads them, with the reason.
- **F-10 (§0/§7, C18, AR-14)** — list the config writers (`_write_config` :1925, `project_decisions.resolve`, `runtime_probe.py:1489`)
  and either record them in the rows (`written_by`) or move C18 explicitly to phase 2 with a pointer; name AR-14 in §1.
- **F-11 (§3 `rows()`)** — read `config-keys.json` through `config_contract.config_keys()` wrapped to `[]` + problem, not through a
  second `read_json` road (AR-13, P31).
- **F-12 (§2)** — `while_unknown`, `derive`, `about`: null/absent in phase 1 like `ask_when` (AR-22, C6/C10), or name their phase-1 reader.
- **F-13 (tests)** — drop the source pin, the "as before" test, and the in-test mutation rows (TESTING.md table); R2 and the no-bypass
  grep go as rows of an existing structural ratchet or justify their place in `test_config_migration.py`; mutation probes stay in the
  builder's report as one-off runs.
- **F-14 (item 6)** — `brief_pack.py:2521` -> `:2904`; refresh batch-1 row numbers; mark UNVERIFIED env_probe numbers verified
  (`data_cleanup` :590, `CLEANUP_UNKNOWN` :587).
- **F-15 (item 5/8)** — tell b/e to shrink the axis-16 G5 `KEPT` rows and axis-8 `OUTSIDE_WALKS` entries they fold (AR-20).
- **F-16 (§6 F6, rule 19)** — write N-r1..N-r4 as nodes with ids in an onboarding-forge or project-knowledge batch with an owner (the
  coordinator opens them), plus the two "finding" notes (brief_pack literals FR-37; `load_env` priority — note its docstring calls the
  file-over-process order deliberate, env_probe.py:116-119, so B-319's "reversed" is itself a question for the owner).

## Standing questions

- **DUPLICATION AND CONSISTENCY:** one new duplicate road found — `rows()` beside `config_contract.config_keys()` (F-11). Otherwise the
  spec removes duplicates (env parse, BOM reads, test_data). Grepped: `config-keys.json|config_keys` over scripts/*.py;
  `"qa-factory" / "artifacts"`; `KEYS\b`.
- **CODE QUALITY:** plan gate, no code; spec-level: R2's heuristic scan is under-specified (F-6). Nothing else found.
- **ONE ROAD (P31, item 12):** (a) no language/project exclusion in the spec; the residual two-direction config readers stay as named
  nodes (F6) — acceptable only once F-16 makes them nodes with owners; (b) F4 `in_template: false` is a data field read by R1 — a data
  row, not a branch: fine; (c) the new `rows()` road is a fresh "one action, two roads" (F-11).

## Class completeness (SIBLING_MAP)

Axes walked: 16 (one JSON reader — GW1-38 folded, F-8 residual queued N-r4: ok), 8 (story on disk — artifact_root twins NOT all named,
F-5; `manual_capture.load_config` outside walk: named), 35 (`registry_sides`: queued N-r3), 30, 5: no change, correctly. The artifact_root
class is the incomplete one (F-5); the `KEYS` reader class is incomplete (F-1).

## Trail

Read: draft whole; batch-3 :20-26; plan §4 :200-217, §7 :319-366; critic review 20261110 :42, :122-128, :366-392; batch-1 rows OH1-6,
OH3-35, OH3-42, GW1-38; BACKLOG.md :327, :350, :370; judge_code.py:198-228; config_contract.py:886-930, :1321-1376, :1308-1336 (grep);
hooklib.py:630-652, :788-798; project_knowledge.py:45-56, :160-172 + def index + `KEYS` uses; report_facts.py:1984-1996, :2176-2184;
dispatch_liveness.py:140-160, :790-805, :944-956; vcs_evidence.py:575-625; env_probe.py:100-135, :585-615; brief_pack.py:2512-2528 and
`"strategy"` grep; the seven GW1-38 sites ±4 lines; runtime_paths.py HOME/home_dir; test-layers.json rows 2912, 4070, 6960-6970, 7883,
8977 + layer lookups; test_reinstall_equals_fresh.py:140-150; SIBLING_MAP axes 8 and 16; docs/TESTING.md :36-100; builder-rules.md 7b;
critic_verdict.schema.json; critic-diff-brief.md items 10-12.
Searches (positive controls): `KEYS\b` in project_knowledge.py [found :49]; `PK\.KEYS` over scripts [found report_facts]; dead-key names
case-insensitive over the package [config-keys.json:186]; `"qa-factory" / "artifacts"` over scripts/*.py [hooklib.py:645];
`load_config(` / `read_config_file(` file counts [hooklib.py def]; `data_cleanup` over tests [test_env_selected_stand.py].
Reruns: `scenario_walk.py --witness-for scripts/check_coverage.py scripts/env_probe.py scripts/vcs_evidence.py scripts/dispatch_liveness.py`
and `--witness-for <abs project_knowledge.py> <abs config-keys.json>` (outputs summarised in key 4/5).
Not read: architecture.md / factory-rules.md full texts beyond the session-loaded indexes; test_config_migration.py internals.
needed beyond the manifest: plans/BACKLOG.md, docs/tasks/specs/reviews/20261110-project-knowledge-plan-critic.md, scripts/report_facts.py,
scripts/tests/test_reinstall_equals_fresh.py, references/install-paths.json, tools/critic_verdict.schema.json, docs/tasks/critic-diff-brief.md.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "F-1 KEYS removal breaks unnamed readers: project_knowledge.record_problems :354-356 (refusal text), report_facts.py :1991/:1993/:2180, test_gate_role_accounts.py:82",
    "F-2 DoD STOP clause (draft :254) contradicts item 4, which must change keep tests test_config_migration.py:374 and test_reinstall_equals_fresh.py:150 (not in owns)",
    "F-3 vcs_evidence broken-root edge (draft :196) leads into an uncaught ValueError at vcs_evidence.py:613 (except OSError only): working call becomes a crash; dispatch_liveness must also catch AttributeError/OSError",
    "F-4 test-layers.json covers edits needed by b and e but owned only by a; R2 baseline shrink not owned by b-e; node d writes dispatch_liveness.py owned by running stream small",
    "F-5 artifact_root hard-code class incomplete: env_probe.py:678, execution_scheduler.py:354/:574, local_keys.py:133, role_load.py:537, B-348 unnamed",
    "F-6 R2/R3 pair-detectors not scoped to one carrier (critic rule 15): same-function heuristic false-matches other objects and misses cfg parameters; R3 checks function existence, not that it reads the key",
    "F-7 data_cleanup mapping onto test_data_states unstated and not identity (empty string, empty list, malformed block); only quarantined tests cover node c's changes"
  ],
  "fixes": [
    "F-1 keep a registry-only KEYS derived from rows in today's order, or convert report_facts and test_gate_role_accounts and add report_facts.py to node a owns; refusal text byte-equal",
    "F-2 carve named expected test edits out of the STOP clause; add test_reinstall_equals_fresh.py to node a owns",
    "F-3 state exception classes and project-root source for item 7; widen vcs_evidence.py:612-615 except or keep default-folder fallback; list liveness/vcs changes as behaviour changes",
    "F-4 per-node covers rows in test-layers.json; R2 baseline ownership; queue node d after stream small; announce R2 to streams hot and hooklib",
    "F-5 fold or queue the five extra artifact_root hard-codes and B-348; name SIBLING_MAP axis 8",
    "F-6 scope R2 to the name bound to the reader return value plus declared cfg parameters; join R3 to R2 hits as file-function-key triples; state miss direction",
    "F-7 write the status-to-state mapping table for data_cleanup; name a keep test or the no-keep-row report line",
    "F-8 per-site error direction table for the seven GW1-38 sites in the spec, incl. import_test_receipt wrapping of ConfigUnreadable and absent config",
    "F-9 catalogue rows or explicit move for records/ carriers beyond project-knowledge.json",
    "F-10 list config writers (C18) and name AR-14, or move C18 to phase 2 explicitly",
    "F-11 rows() reads config-keys.json through config_contract.config_keys(), not a second read_json road",
    "F-12 while_unknown, derive, about null or absent in phase 1 like ask_when (AR-22)",
    "F-13 remove source-pin, as-before and in-test mutation tests per docs/TESTING.md; place R2 and no-bypass grep in an existing structural ratchet or justify",
    "F-14 brief_pack strategy line is :2904 not :2521; refresh drifted row numbers",
    "F-15 instruct b and e to shrink axis-16 KEPT and OUTSIDE_WALKS rows they fold",
    "F-16 write N-r1..N-r4 and the two findings as nodes with ids and owners in a batch file"
  ],
  "class_completeness": "Axes 16, 8, 35, 30, 5 walked. Incomplete: artifact_root hard-code class on axis 8 (five production sites plus B-348 unnamed, F-5) and the KEYS reader class (report_facts, record_problems, a keep test, F-1). Axis 16 residual queued as N-r4 once written as a node (F-16).",
  "trail": {
    "read": [
      "docs/tasks/specs/t-129-of3-1-knowledge-catalog.md",
      "plans/piles/onboarding-forge/batch-3-znaniya-o-proekte-fazy-1-6.md:20-26",
      "plans/project-knowledge-plan.md:200-217,319-366",
      "docs/tasks/specs/reviews/20261110-project-knowledge-plan-critic.md:42,122-128,366-392",
      "plans/piles/onboarding-forge/batch-1-onboarding-roles-forge.md rows OH1-6 OH3-35 OH3-42 GW1-38",
      "plans/BACKLOG.md:327,350,370",
      "ai-packages/qa-factory/scripts/judge_code.py:198-228",
      "ai-packages/qa-factory/scripts/config_contract.py:886-930,1321-1376",
      "ai-packages/qa-factory/scripts/hooklib.py:630-652,788-798",
      "ai-packages/qa-factory/scripts/project_knowledge.py:45-56,160-172,KEYS uses",
      "ai-packages/qa-factory/scripts/report_facts.py:1984-1996,2176-2184",
      "ai-packages/qa-factory/scripts/dispatch_liveness.py:140-160,790-805,944-956",
      "ai-packages/qa-factory/scripts/vcs_evidence.py:575-625",
      "ai-packages/qa-factory/scripts/env_probe.py:100-135,585-615",
      "ai-packages/qa-factory/scripts/brief_pack.py:2512-2528,2904",
      "seven GW1-38 sites",
      "ai-packages/qa-factory/scripts/tests/test-layers.json rows 2912,4070,6960-6970,7883,8977",
      "ai-packages/qa-factory/scripts/tests/test_reinstall_equals_fresh.py:140-150",
      "docs/SIBLING_MAP.md axes 8,16",
      "docs/TESTING.md:36-100",
      "plans/builder-rules.md 7b",
      "docs/tasks/critic-diff-brief.md items 10-12"
    ],
    "reruns": [
      {
        "command": "python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for scripts/check_coverage.py scripts/env_probe.py scripts/vcs_evidence.py scripts/dispatch_liveness.py",
        "result": "check_coverage.py: six keep rows, test_read_json.py NOT among them; env_probe.py: three scenarios + keep rows, test_manual_capture.py NOT among them; vcs_evidence.py includes test_vcs_evidence.py; dispatch_liveness.py keep rows listed"
      },
      {
        "command": "python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <abs project_knowledge.py> <abs references/config-keys.json>",
        "result": "project_knowledge.py: 3 scenarios + 7 keep rows incl. test_gate_role_accounts.py and test_project_knowledge.py; config-keys.json: test_human_questions.py, test_readiness.py (no test_config_migration.py)"
      }
    ]
  }
}
```
