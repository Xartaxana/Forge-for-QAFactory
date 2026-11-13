# t-231 — where env values and env-file names come from (OF1-1 + OF4-12): DRAFT SPEC

Status: DRAFT by designer (t-231), 13.11.2026. Not accepted. Every fork in §5 is the Lead's; nothing in this draft decides one.
Nodes: `onboarding-forge/1/OF1-1` (batch 1, taken, frozen) and `onboarding-forge/4/OF4-12` (batch 4, taken, frozen).
Findings: `plans/piles/onboarding-forge/findings/20261112-discovery-nazyvaet-env-a-chitala-env-example.md` (OF1-1);
`.claude/worktrees/of-batch4/plans/piles/onboarding-forge/findings/20261112-spisok-env-fajlov-i-pustye-znacheniya-chitayutsya-raznymi-dorogami.md` (OF4-12).
Package paths below are written from the main checkout `C:\QAFactory\forge-repo\`; the coordinator maps them to the worktree of the batch branch.

---

## 0. The real route of the OF1-1 value (stated, with its evidence)

**What the person saw** (verified, `experiments/mybooks/factory-vs-free-agent/runs/onboarding-3.json`, the `result` text):
"The test repo's `.env` holds `BASE_URL` (`:3002`) and `API_URL` (`…/api`) … Is the port 3002 the one you use (the README says 3000)?"
and in `runs/onboarding-4.json`: "the 3002 came from `env.example`, which isn't the stand."

**Code cannot have produced the value** (verified by reading):
- `scripts/project_inventory.py` `access_discovery` (:430-496) outputs key NAMES only: `env_files` rows are `{path, keys, example}`
  (:274-276), `env_keys`, `account_pairs`, `frontend_candidates` / `frontend_same_origin` (names; values are read inside
  `frontend_candidates` :401 / `same_origin_keys` :420 and never returned).
- `_is_env_file` (:232-233) is `name == ".env" or name.startswith(".env.") or name.endswith(".env")`: a file named
  `env.example` (no leading dot) is NOT scanned at all, so the inventory did not even list it.
- `env_probe.py` prints values (`account (<user_key>): <value>` at :965, `extra_keys` values at :974, the liveness URL), but it
  reads only the CONFIGURED env file and onboarding runs it in phase 4 (`p4-generate.md:273`), after the batch-3 question.

**The route is the role's own read of the sample, sent there by the phase text** (verified by reading):
- `skills/qa-onboarding/phases/p1-discovery.md:46` — signal row "Candidate environments | `docker-compose*.yml`, `.env.example`, …"
  and `:45` — "Test-data lifecycle | … `.env.example` naming test accounts" — direct the role to OPEN the sample for
  environment facts, i.e. for values (ports, addresses).
- The same file says at `:144-145` "Values are never read out of an env file, here or anywhere: names only." — the carrier
  contradicts itself; the role followed the signal table.
- `p2-interview.md:137` ("When discovery found no address for a stand, ask for it outright") makes "discovery found an address"
  the default path; the role then attached the sample's address to the key names the inventory had given for `.env`.

So: names from the inventory's `.env` row (true) + a value from the role's own read of `env.example` (a sample) = a fact shown
with the name of a carrier it was not read from (FR-37, FR-41). The finding's sentence "the inventory gives values from
`env.example`" does not match the code.
**Unverified part (label: estimate, not verified):** the `runs/*.json` files hold only each turn's final `result`, not the
tool calls; that the role opened `env.example` with Read is inferred from the admission in `onboarding-4.json` plus the code
paths above. The session transcript of the onboarding (its `session_id` is in `runs/onboarding-*.json`) would show the Read
call; per PROJECT.md "package change" rule 6(a) the Lead may run ONE scout read of that transcript before accepting §0.

**Therefore the fix for OF1-1** is (P27): the judgment "is this value the stand's" stays with the role and the person
(text, part B), and code carries the DATA the role was missing so it never needs to open a sample: the sample marker as a data
row (AR-1, part A), `env.example` scanned and marked (part A), and — fork F-f — the stand's non-secret addresses with the file
each was read from. Not a phrase detector over the role's text (FR-12).

---

## 1. Package invariants touched, owners, census classes

**AR-n touched, each with the change check written into the DoD of the part that touches it:**

| AR | how this spec touches it | change check (in the DoD of part …) |
|---|---|---|
| AR-1 | the env-file name rule and the sample markers move from code (`project_inventory.py:233`, `:275` regex; `gate_preflight._stray_env_file` globs `.env*`, `*.env` :5128) into one data file | grep `scripts/` for the SHAPE (`.env`, `example`, `sample`, `template`, `dist` near a file name) with a positive control; the only hit left is the table reader (A, C) |
| AR-2 | which file is the stand's and whether a value is the stand's stays the role's and the person's judgment; code marks `example` and names the file | name what the role still decides (A, B): "which of the found addresses is this stand's, and whether a sample's address means anything for it" |
| AR-11 | p1/p2 text changes the onboarding role's load | `role_load.py --all` before and after (B) |
| AR-13 | one chooser of the env-file list, one layering of values; `parse_env_file` stays the one content reading | grep for `get("env_file")` / `get("env_files")` / `os.environ` merges with a positive control; every reader calls the survivor (C, D) |
| AR-15 | the survivor is wired at every site; a new survivor gets a SIBLING_MAP axis in the same commit | list every site (§2 table); new axis 37 row (C) |
| AR-22 | new inventory fields (`env_file_is_sample`, and under F-f (b) `stand_addresses`) each have a reader (p1, p2); `references/config-keys.json` `needed_by` rows of `environment.env_file` / `env_files` name the new reader | grep the field names over `scripts/ agents/ skills/ references/ handoffs/` (A, B, D) |
| AR-28 / FR-59 | an absent or unreadable env file is never read as "the key is not there" silently beyond what each caller does today | the edge rows of C state each caller's consequence; a test row per state (C) |
| AR-29 | every check this spec adds or alters is named with its class and owner below | `python -m pytest ai-packages/qa-factory/scripts/tests/test_judgment_census.py -q` (A, C, D) |

AR-3 (no new config key unless F-c option 3 or F-e is taken: then a template row + `config-keys.json` row + interview topic in one
commit), AR-4 (paths stay relative; absolute and `..` entries keep today's behaviour), AR-9 (one refusal text changes: `load_env`'s
fatal line for several files; door unchanged) — touched only as noted in the edges.

**P31 / axis 34 (one road).** No language, project or framework is branched on. Two per-PURPOSE differences exist and are put
to the Lead as forks, not closed: the recorder and the stand-key readers take no process layer (F-c), and the gate alone looks
at the project's conftest / pytest-dotenv setup when the config names no file — a Python-only road (F-e).

**Checks added or altered — owner and census class (AR-29, P27):**

| check | where | class | owner it serves | census row |
|---|---|---|---|---|
| is a file NAME an env file / a sample (`env_probe.env_file_kind`) | A | shape (the name's form against a data table) | data (code) | none expected: the name is outside the unit families (`*_problems`, `validate*`, `refuse*`, `check`, `run`, `*_errors`, `*_check`); if the builder's name falls in one, row `{class: shape, owner: data}` |
| an empty or blank value is "not set" (`env_probe.env_layers`) | C | shape (presence) | data | none expected (same reason) |
| which files count (`env_probe.env_files`) | C | shape (config read) | data | none expected |
| a variable sits in a file nothing loads (`gate_preflight._stray_env_file`, now skipping samples) | C | xref (value present in a file not in the loaded list) | data | none today; unchanged |
| is this address the stand's; is a sample's value relevant | B (role text) | — not code | judgment (onboarding role), accepted by the person at the summary gate (intent) | none: no code check is added; FR-12 forbids a detector over the role's wording |
| redaction candidates from every configured file (`machine_facts.secret_values`) | D | safety | data (protection of secrets) | none today |

---

## 2. The one model (what every reader ends on)

| fact | survivor (recommended; F-a decides) | today's readers that must end on it |
|---|---|---|
| the CONTENT of one env file | `env_probe.parse_env_file` (unchanged) | already all; `project_inventory.env_file_keys` and `machine_facts._env_file_values` are t-230's (not owned here) |
| WHICH files count | `env_probe.env_files(env_cfg, root) -> (list[Path], how)` — the body of today's `gate_preflight.configured_env_files`, moved; the gate's name stays a one-line delegate | `gate_preflight.configured_env_files` (delegate), `stand_health._env_values`, `env_probe.load_env` :131, `env_probe._derived_frontend` :483, `env_probe._frontend_hint` :518, `source_inventory.runtime_credential_values` :58-66, `machine_facts.secret_values` :345, `config_contract.env_key_names` :1061-1069, `project_decisions.record_stand_account` :636-641, `readiness.config_fails_own_probe` :621, `brief_pack._stand_address_lines` :2565, `judge_run._env_files` :321 (its `environment` part), `project_inventory.access_discovery` :434 |
| the VALUES set for a reader | `env_probe.env_layers(files, *, process=True) -> (values, source_of, problems)`: process layer (if `process`) then each listed file in order; a later layer wins; an empty or blank value is never a value and never erases one (F-b, F-c) | `gate_preflight.env_values` (delegate), `stand_health._env_values`, `manual_capture._env_files_state` (`process=False`), `env_probe.load_env`, `env_probe._derived_frontend` / `_frontend_hint` (`process=False`), `source_inventory.runtime_credential_values` |
| is a file NAME an env file, a sample, or neither | `env_probe.env_file_kind(name) -> "env" \| "sample" \| ""` over `references/env-file-names.json` (F-d) | `project_inventory._is_env_file` :232, the regex :275, `gate_preflight._stray_env_file` globs :5128 |
| the files the RUNNER loads when the config names none | stays `gate_preflight._loaded_env_files` unless F-e (b) | — |

`machine_facts.secret_values` reads the chooser's files but does NOT layer: redaction needs every value of every file (union),
not the winner — a different action, stated so it is not mistaken for a second layering road.

---

## 3. Parts (builder dispatch drafts)

Order and hot files: §4. Each part's `designer:` line will be filled by the Lead at acceptance (the accepted path of this file).

### Part A — OF1-1 code: the env-file name table, `env.example` scanned and marked, the inventory's sample flag (and F-f data)

given: this spec §0-§2 and §5 (as accepted); `ai-packages/qa-factory/design/factory-rules.md` whole; `plans/builder-rules.md`; `ai-packages/qa-factory/design/architecture.md` AR-1, AR-2, AR-13, AR-22, AR-29; `scripts/project_inventory.py` (:217-308, :392-496); `scripts/env_probe.py` (:103-120 `parse_env_file`, :502-511 `http_address_keys`); `scripts/http_client.py` `safe_url`; `scripts/hooklib.py` `read_json`; `scripts/judge_discovery.py` :10, :44 (reader of `example`); `scripts/tests/test_manual_capture.py` :1975-2034 (the reader table); `scripts/tests/test-layers.json` (keep rows); `docs/TESTING.md`; the OF1-1 finding
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\env-file-names.json (new)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\env_probe.py (env_file_kind and its table loader only — new functions)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\project_inventory.py (_is_env_file, scan_sources, access_discovery; under F-f (b) one new function for the address rows) — NOT env_file_keys (t-230)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_manual_capture.py (one new table function beside of3_1e_one_env_file_parse, registered in main())
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\ (one fragment)
non-goals: no value of a secret-looking name leaves any function; no change to `parse_env_file`, `env_file_keys`, `machine_facts`; no phase text (part B); no rename of the `example` field; no detector over a role's wording (FR-12); no edit to quarantined tests (test_project_inventory.py, test_env_access_onboarding.py); no batch-file edit
handoff: builder report per `.claude/agents/builder.md` rule 7 with the FR walk (sections A, C, D, E, G) and the witness, to the coordinator
edges:
- A-1 (the name rule, F-d): `env_file_kind(name)` splits `name` on `.`, drops empty parts, lower-cases. "env" when the name matches the env-file rule of the table (rows: exact `.env`; prefix `.env.`; suffix `.env` — today's `_is_env_file`, unchanged in reach); "sample" when it is an env file AND any part equals a sample marker (`example`, `sample`, `template`, `dist`, plural forms as data rows), OR the name is exactly `env.<marker>` (the bare form, e.g. `env.example`); otherwise "". Invariant: a sample is never classified "env" — the marker errs toward "sample". Adversarial rows that must stay on that side: `.env.example`, `.env.EXAMPLE`, `.env.example.local`, `.env.local.example`, `example.env`, `env.example`, `env.sample`, `env.template`, `env.dist`, `.env.dist`, `.env.template.bak` → sample; `.env`, `.env.local`, `.env.test`, `.env.production`, `my.env` → env; `env.example.py`, `env.py`, `.envrc`, `environment.ts`, `` (empty name) → "". A non-ASCII name (`.env.пример`) → "env" (no marker matches; listed, not a sample).
- A-2 (table absent or unreadable): the table ships with the package. `env_file_kind` raises `ValueError` naming `references/env-file-names.json`, what it expected (the keys) and that the package copy is damaged (FR-1); it never falls back to a built-in list (that would be the list in code AR-1 removes). Invariant: no silent classification without the table.
- A-3 (temporal): the table is born in this part. Before it (main today) the inventory reads the regex; after it, the regex at :275 and the `_is_env_file` expression are gone and both read `env_file_kind`. Part C's `_stray_env_file` reads the table only after A is merged (queue §4).
- A-4 (`env.example` now scanned): it enters `env_files` with `example: true`, sorted after real files (`env_files.sort` by `(example, path)`, unchanged). It counts against `MAX_FILES` like any scanned file (no new cap). Invariant: a real env file is still listed before every sample.
- A-5 (the chosen file, positional, F-g): `access_discovery` takes the declared files from `env_probe.env_files` — after part C; until C is merged, from `env_file` as today — and picks the first scanned row whose path is a declared file, else the first non-sample row, else the first sample row (today's fallback kept so the names still feed `propose_access`). New field `env_file_is_sample: bool` — true exactly when the chosen row is a sample. Invariant: `account_pairs`, `frontend_candidates`, `frontend_same_origin` stay empty for a sample-chosen file (today's guards :468, :475 kept), and a sample is never the chosen file while a real env file exists.
- A-6 (F-f (b) only — the address rows): new field `stand_addresses`: one row `{key, address, path, sample}` per key whose value in a scanned env file (real or sample) is an http(s) address, keys from `env_probe.http_address_keys(values, set())` (so a secret-looking name never appears), `address` = `http_client.safe_url(value)` (no userinfo, query, fragment). Order: `env_files` order (real files first), then the file's key order. Cap `STAND_ADDRESSES_MAX = 10` rows with `stand_addresses_more: N`; invariant of the cut: a real file's row is never cut while a sample's row is kept. An address longer than 300 characters after `safe_url` is not listed (row omitted, counted in `stand_addresses_more`); AT 300 listed, 301 not. An unreadable file (OSError, ValueError) gives no rows and no exception. An empty file, a file with no http value, no env files at all → `stand_addresses: []` (declared empty outcome, AR-23). Invariant: no value of any other key is ever output.
- A-7 (empty / absent inputs): no env file anywhere → `env_files: []`, `env_file: ""`, `env_file_found: false`, `env_file_is_sample: false` (today's shape plus the false flag). `config` None or without `environment` → declared files empty, the rest as A-5.
siblings: `gate_preflight._stray_env_file` (the third "what is an env file" site) — part C; `judge_discovery.py` reads `example` (unchanged meaning, no edit); `p1-discovery.md:156` passes `"example":false` (unchanged).
DoD: (1) `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for scripts/env_probe.py scripts/project_inventory.py references/env-file-names.json scripts/tests/test_manual_capture.py` and every file it prints, each in its canonical form, PLUS `python -B ai-packages/qa-factory/scripts/tests/test_manual_capture.py` by name (keep; covers env_probe.py) — green; (2) the new table function in test_manual_capture.py holds: every A-1 row through `env_file_kind`; one fixture `.env` (`BASE_URL=http://localhost:3000`) + `env.example` (`BASE_URL=http://localhost:3002`) through `access_discovery`: `env.example` listed with `example: true`, `env_file == ".env"`, `env_file_is_sample` false and, under F-f (b), `stand_addresses` = the `.env` row (3000, `sample: false`) before the `env.example` row (3002, `sample: true`); one fixture with only `env.example` → `env_file_is_sample` true, pairs and candidates empty; F-f (b) rows: secret-looking name with a URL not listed, `http://u:p@host/x?q=1` shown as `http://host/x`, the cap AT 10 and BEYOND (11 → `stand_addresses_more: 1`, the cut row a sample's), address AT 300 / 301 characters; the table file absent → `ValueError` naming it (a byte copy of the table restored after, hygiene pt. 7); (3) AR-1 check: `grep -n -i -E "example\|sample\|template\|dist" scripts/project_inventory.py scripts/gate_preflight.py` lists no file-name test outside the table reader (positive control: the same grep finds the current regex at project_inventory.py:275 before the change); (4) `python -m pytest ai-packages/qa-factory/scripts/tests/test_judgment_census.py -q` green, no count raised; (5) `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang` green; (6) the report names what the role still decides (AR-2): which found address is this stand's, and that a sample's address is never it.
designer: <accepted path of this file, filled by the Lead>

### Part B — OF1-1 text: the role never presents a sample's value as the stand's

given: this spec §0, §1, §5 (as accepted, F-f's option fixes the wording); part A's field names (`example`, `env_file_is_sample`, and under F-f (b) `stand_addresses` with `{key, address, path, sample}`); `skills/qa-onboarding/phases/p1-discovery.md` (:30-50, :89-145); `skills/qa-onboarding/phases/p2-interview.md` (:130-190); `references/human-questions.md`; `design/role-rules.json` (row format, e.g. :5); `scripts/role_load.py`; `docs/TESTING.md` («Правила ролей не теряются»); `design/factory-rules.md` whole; `plans/builder-rules.md`
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\skills\qa-onboarding\phases\p1-discovery.md
C:\QAFactory\forge-repo\ai-packages\qa-factory\skills\qa-onboarding\phases\p2-interview.md
C:\QAFactory\forge-repo\ai-packages\qa-factory\design\role-rules.json (one new row)
non-goals: no code; no new question (the stand question of topic 2 keeps its count); no phrase list the code would match (FR-12); no other phase file; no batch-file edit
handoff: builder report with the FR walk (B, C, E) and the witness, to the coordinator
edges:
- B-1 (the contradiction inside p1): rows `:45` and `:46` no longer send the role into `.env.example` for values. They read: the inventory's env-file rows marked `example` are SAMPLES — they show which key names a project expects (test accounts, environments); their values are the sample's, never the stand's. `:144-145` is rewritten to one law that matches the rows: under F-f (b) "you never read values out of an env file: the inventory gives the stand's addresses it may (`stand_addresses`, each with its file); every other value — names only"; under F-f (a) "values are never read out of an env file, a sample included: names only; an address comes from the person or from a README / compose line you cite". Invariant: no line of p1 tells the role to open an env file or a sample for a value.
- B-2 (the value a person sees): every value shown to a person names the file it came from as the inventory gives it ("`.env`: `BASE_URL` = http://localhost:3000"). A row with `sample: true` is shown, if at all, only as "the sample file `env.example` shows …", apart from the stand's facts, and is never the default answer of a question. `env_file_is_sample: true` is said as "the repository holds only a sample env file (`<path>`): no file of this stand was found". Invariant: a sample's value never reaches a person as the stand's value.
- B-3 (p2 topic 2, positional — `p2-interview.md:137-143`): "When discovery found no address" now means: no `stand_addresses` row of a non-sample file (F-f (b)) / no cited README or compose address (F-f (a)). The stand question proposes the non-sample address with its file; when two non-sample files disagree, both are shown with their files and the person picks (the role does not choose silently, AR-2). Invariant: a sample's address is never proposed even when it is the only address found — then the question asks outright, as `:137` already says.
- B-4 (rule kept from loss): one `design/role-rules.json` row, id `env-sample-value-not-stand`, rule "A sample env file's value is never shown as the stand's; every value shown names the file it came from", carriers p1 and p2 with a 2-6 word anchor each present in the new text.
- B-5 (empty outcomes): no env file → unchanged text path (the address is asked); no `stand_addresses` (F-f (b)) → the address is asked outright; the role never fills the gap from a sample.
siblings: `p4-generate.md` runs `env_probe.py` (prints the configured file's values: address, account) — reads the configured file, not a sample: no edit, named for the critic; `p3-summary-gate.md` shows found facts — check its env lines name the file (report line if it does not; no edit here).
DoD: (1) `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for skills/qa-onboarding/phases/p1-discovery.md skills/qa-onboarding/phases/p2-interview.md design/role-rules.json` and every file it prints, green; (2) the role-rules registry test (the keep file that reads `design/role-rules.json`, named by the witness line) green with the new row; (3) `python -B ai-packages/qa-factory/scripts/role_load.py --all` before and after, both outputs pasted, the onboarding role's number stated (AR-11); (4) `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang` green; (5) a doc-dispatch key-presence run (CLAUDE.md rule 11, three properties): keys quoted verbatim from B-1..B-4 (the new law line of p1, the "sample file" wording, the p2 proposal rule, the role-rules id), the script attached in full, with a negative control.
designer: <accepted path of this file, filled by the Lead>

### Part C — OF4-12 core: one chooser, one layering; the gate, stand_health, the recorder and env_probe on them

given: this spec §1, §2, §5 (as accepted); `design/factory-rules.md` whole; `plans/builder-rules.md`; `design/architecture.md` AR-13, AR-15, AR-28, AR-29; `scripts/gate_preflight.py` :1027-1053, :5072-5136, :5149-5158; `scripts/env_probe.py` :103-141, :336-352, :440-535, :905-975; `scripts/stand_health.py` :432-444, :492, :810; `scripts/manual_capture.py` :607-680, :4975-4985; `scripts/walk_pool.py` :143-149; `scripts/project_decisions.py` :697-730 (caller of `env_values`); `scripts/tests/test_manual_capture.py` :1975-2034; `scripts/tests/test_manual_actor.py` :545-640 (quarantined: read only, it pins the recorder's rules); `docs/SIBLING_MAP.md` (axis format); the OF4-12 finding
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\env_probe.py (new env_files, env_layers; load_env, _block_frontend, _derived_frontend, _frontend_hint)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\gate_preflight.py (configured_env_files, env_values, _stray_env_file) — HOT file, function list
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\stand_health.py (_env_values)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\manual_capture.py (_env_files_state)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_manual_capture.py (of3_1e_one_env_file_parse and one new layering table function)
C:\QAFactory\forge-repo\docs\SIBLING_MAP.md (new axis 37 only; staged, committed by the Lead — mechanism path, builder-rules 18)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\ (one fragment)
non-goals: no change to `parse_env_file`; nothing of t-230's two functions; `_loaded_env_files` untouched (part E, F-e); no caller migration off the gate's delegate names (`configured_env_files`, `env_values` keep their signatures); no edit to quarantined tests (test_stand_health.py, test_manual_actor.py, test_frontend_reader.py); no batch-file edit
handoff: builder report with the FR walk (A, C, D, E, G) and the witness, to the coordinator
edges:
- C-1 (the chooser, F-a): `env_probe.env_files(env_cfg, root)` = today's `configured_env_files` body byte-for-byte in behaviour: a non-empty list `env_files` wins (blank entries dropped, order kept, no de-duplication — `[a, b, a]` reads `a` last, as today); `env_files` empty or not a list → `env_file`; neither → `([], "")`; `env_cfg` not a dict → `([], "")`. Absolute and `..` entries resolve as `Path(root) / entry` does today (AR-4 unchanged). `gate_preflight.configured_env_files` becomes a one-line delegate. Invariant (positional): `_loaded_env_files` still asks the config first, so a file the config names always beats the conftest fallback (the TP1-15045 class stays closed).
- C-2 (the empty rule, F-b): in `env_layers` a value whose `.strip()` is empty is never a value: `A=`, `A=""`, `A="   "`, a process `A=""` / `A="  "` → the key is absent from `values`; an empty value never erases a non-empty one held by an earlier layer. A non-blank value is kept as `parse_env_file` returned it (no strip added). `A="` (a lone quote) → `"` → set: the direction the t-172 critic accepted, unchanged. NAMES readers are not touched: a key with an empty value is still a NAME the file holds (`parse_env_file` keys, `brief_pack._env_file_key_names`, `env_file_keys`). Invariant: an empty or blank value never answers a key as set, in any reader of values. Behaviour change named: `stand_health._env_values` and `load_env` stop returning `""` for such keys (callers read `.get(k, "")` / `or` — the builder greps each caller for `in values` / `in env` membership tests and lists them in the report; none found at :965-974, :1046 of env_probe, readiness :618).
- C-3 (the layering, F-c): process layer first (when `process=True`), then each listed file in order; a later layer wins. `manual_capture._env_files_state` calls `env_layers(files, process=False)`; `_derived_frontend` (:483) and `_frontend_hint` (:518) read the stand's own keys with `process=False`. Invariant: the recorder's account never comes from a machine variable (`USERNAME`, `USER`) and never from two sources (the user in a file, the password in the process: `test_manual_actor.py:592-597` stays true); a machine proxy variable (`HTTP_PROXY`) never becomes a frontend candidate.
- C-4 (absent, not-a-file, unreadable): `env_layers` returns `problems` = `[(path, "absent" | "unreadable")]`; "unreadable" = exists but is not a regular file, or `OSError` on read. Each caller's consequence is TODAY's, read from `problems`: the recorder → `({}, "unreadable")` at the first unreadable, `"file"` when none exists, `"ok"` otherwise (byte-equal states); `stand_health` → skips (today's silent skip; FR-41 residual named in §7); `gate_preflight.env_values` (delegate, returns the dict only) → absent and not-a-file skipped, an `OSError` on a regular file propagates as today. Invariant: no caller turns an absent or unreadable file into "the key is set"; none gets a weaker consequence than today.
- C-5 (`load_env`, positional and temporal): reads `env_files` (C-1) and `env_layers(process=True)`. One configured file absent → fatal with today's text byte-for-byte; several configured, none exists → fatal naming every file; some exist → not fatal, `sources` = `"process environment + <each file read, in order>"`. `_block_frontend`'s note (:349) and `_derived_frontend`'s note (:472-473, :489-490) say "environment.env_file / env_files" only when the config used `env_files`; with `env_file` alone they stay byte-equal. Invariant: `load_env` never returns `fatal` None while every configured file is absent (an unknown is not a pass, FR-59).
- C-6 (`_frontend_hint` text, FR-37): the line names the file(s) each shown key was read from (`source_of`), distinct files joined with ", " in list order; with one configured file the line is byte-equal to today.
- C-7 (`_stray_env_file`, F-d): candidates are files of the same folders whose `env_file_kind` is "env" (samples excluded) instead of the globs `.env*` / `*.env`. Behaviour change named: `.envrc`, `.env-backup` and similar are no longer candidates; a sample holding the variable is never named. Invariant: a sample is never named to a person as the file their variable sits in. Values still never leave the function (names only).
- C-8 (BOM literals, finding item 3): the U+FEFF characters inside string literals of `of3_1e_one_env_file_parse` (the "BOM on the first line" and "BOM before export" rows, and the two-file fixture) are written `\ufeff`; the bytes the test writes are unchanged. Invariant: no invisible character inside a test literal.
- C-9 (the reader table, test): the "empty value" rows (`A=`, `A=""`) keep their `parse_env_file` / `manual_capture._env_values` expectation `{"A": ""}` (content reading keeps empties) and the `stand_health._env_values` expectation becomes "absent"; a new layering table function judges `env_layers`, `gate_preflight.env_values`, `stand_health._env_values`, `manual_capture._env_files_state` and `load_env` on ONE set of rows: empty in the file / in the process / in both; blank quoted; a later file empty over an earlier value; process vs file (F-c); `env_files` of two; `env_files` beats `env_file`; a missing file in the list; a directory in the list; none exists; `process=False` ignores the process. The row id names the case and the reader (P16).
- C-10 (temporal): no package artifact is created by this part. It reads `references/env-file-names.json` (born in part A) — C is queued after A; on a tree without A, C does not start. The SIBLING_MAP axis 37 row is born here (the Lead commits it with the package commit: AR-15 "same commit").
siblings: axis 37 lists every site of §2; `walk_pool._env_key_names` (calls `_env_files_state`: inherits C-2 — a quoted-blank value now drops; no edit); `project_decisions.record_stand_frontend` path via `env_values` (inherits; no edit); `brief_pack._env_file_key_names` (names reader; no change); part D readers; t-230's `machine_facts._env_file_values` / `project_inventory.env_file_keys` (not owned).
DoD: (1) `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for scripts/env_probe.py scripts/gate_preflight.py scripts/stand_health.py scripts/manual_capture.py scripts/tests/test_manual_capture.py` and every file it prints (it names test_manual_capture.py and test_gate_preflight.py among others), each in its canonical form — green; (2) the C-9 rows green, each row id naming case and reader; (3) AR-13 check: `grep -n -E "get\(\"env_files?\"\)" ai-packages/qa-factory/scripts/*.py` — after the change the hits in the files this part owns are `env_probe.env_files` only (positive control: the same grep before the change hits env_probe.py:131); (4) `python -m pytest ai-packages/qa-factory/scripts/tests/test_judgment_census.py -q` green, no count raised; (5) `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang` green; (6) the report lists every caller membership test found under C-2 and the axis 37 row text.
designer: <accepted path of this file, filled by the Lead>

### Part D — OF4-12 readers: every other reader of the list ends on the chooser

given: this spec §1, §2, §5 (as accepted); part C's merged functions `env_probe.env_files` / `env_layers`; `design/factory-rules.md` whole; `plans/builder-rules.md`; `scripts/source_inventory.py` :36-82; `scripts/machine_facts.py` :308-360 (`_env_file_values` is t-230's: call it, never edit it); `scripts/config_contract.py` :1054-1070; `scripts/project_decisions.py` :605-660; `scripts/readiness.py` :198-220, :600-625; `scripts/brief_pack.py` :2551-2570; `scripts/judge_run.py` :316-337; `references/config-keys.json` :768-769; `scripts/tests/test_manual_capture.py` (the layering table of part C); `scripts/tests/test_readiness.py` :760-770; `scripts/tests/test_brief_pack.py`
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\source_inventory.py (runtime_credential_values)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\machine_facts.py (secret_values) — NOT _env_file_values (t-230)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\config_contract.py (env_key_names)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\project_decisions.py (record_stand_account)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\readiness.py (config_fails_own_probe)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\brief_pack.py (_stand_address_lines)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\judge_run.py (_env_files)
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\config-keys.json (the needed_by lists of environment.env_file and environment.env_files only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_manual_capture.py (rows added to part C's layering table)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\ (one fragment)
non-goals: no change to what `secret_values` prints or logs (values never leave); `judge_run`'s `environments[].env_file` reading kept as is; no edit to quarantined tests (test_source_inventory.py, test_collect_redact.py, test_project_decisions_stand_facts.py, test_judge_run.py) — their stale rows are report lines; no batch-file edit
handoff: builder report with the FR walk and the witness, to the coordinator
edges:
- D-1 (`runtime_credential_values`, F-c): files from `env_files`, values from `env_layers(process=True)` with `environ` as the process layer when given. Behaviour change named: a non-empty process value no longer beats a file value, and with `env_file` + `env_files` both set only `env_files` is read. Invariant: the doctor (`readiness` :204-215) and the tracker reader resolve one name to the same value (both call this function — unchanged pairing). Quarantined `test_source_inventory.py` :353 ("process wins") and :368 ("env_file first") go red in quarantine-watch: one report line naming both, no edit.
- D-2 (`secret_values`, safety): candidates from `environ` AND every file `env_files` names (union, not layered), each file through t-230's `_env_file_values(rel, root, gaps)`. Today a config with only `env_files` contributes NO file value to redaction — a leak this part closes. Error direction: over-redaction is the safe side. Adversarial inputs that must stay safe: `env_files` only; a value only in the second file; one key with different values in two files (both candidates); an empty value (no candidate); a listed file absent (a gap row per file, naming the file); a ` # note` tail (both candidates, as today).
- D-3 (`env_key_names`): names from the chooser's files (env_files wins) plus the process names. Behaviour change named: with both keys set, a name only in `env_file` is no longer available. Invariant: a name the gate cannot read is never reported available.
- D-4 (`record_stand_account` :636-641): `named` = the chooser returned files; `where` = the first chooser file, relative. Invariant: the file the refusal names is a file the gate reads (FR-37).
- D-5 (`config_fails_own_probe` :621) and (`_stand_address_lines` :2565): the place named is the chooser's file list as a person reads it (`manual_capture._file_names`), "the process environment" when it is empty. Invariant: never the word `None`, and with `env_file` alone byte-equal to today.
- D-6 (`judge_run._env_files`): the `environment` block's files come from the chooser (so `env_files` entries appear); `environments[].env_file` entries appended as today; names only, order: chooser files, then stand entries, de-duplicated as today.
- D-7 (`config-keys.json`): both rows' `needed_by` gain `env_probe.py:env_files`; entries whose function still exists stay; `gate_preflight.py:configured_env_files` stays (delegate). Invariant: every function that reads the key directly is listed (AR-22).
siblings: `audit_factory._declared_paths` (:1021-1024, reads `env_file` for a path audit, not values — n/a: it audits the stored path, kept, named for the critic); `walk_pool` (inherits via C).
DoD: (1) `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for scripts/source_inventory.py scripts/machine_facts.py scripts/config_contract.py scripts/project_decisions.py scripts/readiness.py scripts/brief_pack.py scripts/judge_run.py references/config-keys.json scripts/tests/test_manual_capture.py` and every file it prints (test_readiness.py, test_brief_pack.py among the keep rows), plus test_manual_capture.py by name — green; (2) rows in the layering table, one config set through every D reader: `env_files` only; both keys; `env_file` only; a value only in the second file; empty in the later file; process vs file; plus the D-2 adversarial rows through `secret_values` (redaction candidates include the second file's value); (3) the AR-13 grep of part C over these files leaves no direct `get("env_files")` / `get("env_file")` read except `judge_run`'s `environments[]` rows and `audit_factory` (positive control as in C); (4) `python -m pytest ai-packages/qa-factory/scripts/tests/test_judgment_census.py -q` green; (5) `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang` green.
designer: <accepted path of this file, filled by the Lead>

### Part E — conditional on F-e (b): the runner's own loading joins the one chooser

Drafted only as the named rest of the slice (designer rule 6: a slice is no exclusion when the rest is a named node). Not
dispatchable before F-e is decided; under F-e (a) it becomes a finding for the next untaken batch (both batches are frozen).

given: this spec §2, §5 F-e; `scripts/gate_preflight.py` :5072-5119, :4532-4537, :4980, :5479; `scripts/planning_contract.py` :3606; part C's `env_files`; `references/env-file-names.json`; `references/config-keys.json` :477, :625
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\gate_preflight.py (_loaded_env_files) — HOT file, function list
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\env_probe.py (env_files: the no-config step)
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\env-file-names.json (loader-call rows)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_gate_preflight.py (rows in the existing loaded-files table)
non-goals: no new config key unless the Lead takes F-e option (c); no change to what the gate asks
handoff: builder report with the FR walk and the witness
edges:
- E-1: `env_files(env_cfg, root, *, tests_root=None)`: config list → loader evidence (data rows: python-dotenv `load_dotenv(` / `dotenv_values(` literal paths and the bare walk-up; pytest-dotenv `env_files =`; further languages as rows) → `<tests_root>/.env` default. Invariant: a config-named file always wins; the evidence step reads code by data rows read through one reader, never a language branch (AR-1, P31).
- E-2 (temporal, the meaning of an empty `env_file`): `config-keys.json` :625 says "an empty env_file means values come from the process environment". Under E every reader that today reads only the process in an unconfigured project starts reading discovered files. The note gets a `note_history` entry in the same commit (AR-3 change check).
DoD: `scenario_walk.py --witness-for` on the owns, green; rows: config wins; conftest literal; bare `load_dotenv()` walk-up; pytest-dotenv; default `.env`; no evidence and no file.
designer: <accepted path of this file, filled by the Lead>

---

## 4. Order, hot files, the «Командная работа» p.3 rule

| queue | why |
|---|---|
| t-230 → A, t-230 → C, t-230 → D | t-230 owns `project_inventory.env_file_keys`, `machine_facts._env_file_values` and a row in `test_manual_capture.py` (journal `dev1.jsonl:609`); A, C, D write those files (other functions) and `test_manual_capture.py` |
| A → C | batch order `очередь: onboarding-forge/1 → onboarding-forge/4` (batch-4 file :10); `env_probe.py` and `test_manual_capture.py` shared; C reads A's table |
| A ∥ B | disjoint owns; B's field names are fixed in this spec |
| C → D | D calls C's functions and adds rows to C's table |
| C → E | E extends C's chooser; both touch `gate_preflight.py` |

Hot files (PROJECT.md «Командная работа» p.3): `gate_preflight.py` is HOT — C owns `(configured_env_files, env_values, _stray_env_file)`,
E owns `(_loaded_env_files)`; they are sequential anyway. Other in-work nodes on `gate_preflight.py`: OF1-4 (batch 1, the
recorder browser probe) — a disjoint function list, and batch 1 merges before batch 4. Not hot but shared within batch 4:
`env_probe.py` with OF4-23 (`environment` readers) and OF4-26 (direct `utf-8-sig` config read) — the dispatches give disjoint
function lists; `brief_pack.py` with OF4-21 / OF4-30; `project_decisions.py` with OF4-8 / OF4-14 / OF4-28; `source_inventory.py`
with OF4-14; `config_contract.py` with OF4-28 and OF1-2 (batch 1); `references/config-keys.json` with OF1-2 — each by function
list (D lists its functions), the later node merges `main` and resolves.

Node rows vs owns (needs the Lead, F-i): OF1-1's «Пишет в» does not list `references/env-file-names.json` or
`design/role-rules.json`; OF4-12's does not list `manual_capture.py`, `config_contract.py`, `project_decisions.py`, `readiness.py`,
`brief_pack.py`, `judge_run.py`, `references/config-keys.json`, `docs/SIBLING_MAP.md`.

---

## 5. Forks (returned; each with options and a recommendation)

**F-a — the survivor of "which files count" and of the layering.**
(a) `gate_preflight.configured_env_files` / `env_values` stay the survivors; every reader imports the gate. (b) Both move to
`env_probe` (`env_files`, `env_layers`), the gate keeps one-line delegates of the same names. (c) A new small module
(`env_sources.py`). — **Recommend (b):** `env_probe` already holds the one content reading (`parse_env_file`) and says in its
docstring it exists so no role parses `.env` itself; the hot file shrinks instead of growing; `source_inventory`, `machine_facts`
and `config_contract` would otherwise import a 5,000-line gate for one helper. Cost: two delegates remain in the gate (one hop);
(c) adds a module and an import edge for no gain.

**F-b — the empty-value rule, and its error direction when a stand key is empty.**
(a) Empty or blank = not set, in every reader of VALUES (the gate's rule today); names readers keep the name. (b) Empty = set to
"" (stand_health and `load_env` today). — **Recommend (a).** Error direction: a stand key that is empty in the file reads as
"missing" — the probe says MISSING, the gate asks, the recorder refuses with `key`: the factory asks or reports, it never
proceeds as if an address or a credential existed. Adversarial inputs that must stay on that side: `A=`, `A=""`, `A="   "`,
process `A=""`, an empty value in a later file over a set one (must not erase), an empty process value under a set file value.
Kept on the other side on purpose: `A="` (lone quote → `"`, set; accepted by critic t-172). Cost: `stand_health` and `load_env`
callers see `None` where they saw `""` (C-2 asks the builder to list membership tests).

**F-c — the layering order (process vs file; first vs later file).**
(a) File over process, later file over earlier — the gate, `stand_health`, `load_env` and the recorder's file order today; and
the pinned tests (`test_manual_capture.py:2023`, `test_manual_actor.py:605-609`). (b) Process over file, first file wins —
`source_inventory` today, and also the default of python-dotenv (`override=False`) and of node dotenv: a variable already in
the process is not replaced, and a later loaded file does not replace an earlier one. (c) A per-project config key
(`environment.env_override`) asked at onboarding (AR-3). — **Recommend (a)** for this node: it is what four readers and the
gate's question texts already say, and the gate's file list is what the doors name (FR-37); `source_inventory` moves.
Costs named: (1) a person who exports a token in the shell while a stale file holds another gets the file's token in the tracker
reader (today the shell's); (2) where a project's runner uses dotenv defaults, a process variable that the runner would keep is
reported as replaced by the file — the gate's "what the runner sees" can differ from the runner in that one case. Measuring (2)
on one live project (PROJECT.md rule 6(a)) is cheaper than building (c). The PURPOSE exception inside (a): the recorder and the
stand-key readers pass `process=False` — the account must come from a file the project wrote (`USERNAME` / `USER` of the machine
would otherwise answer a `user_key` of that name) and a machine proxy variable is not a stand key. Under P31 this is one function
with a declared parameter, not a second road — the Lead confirms that reading, or takes it to the owner.

**F-d — where the sample-name list (and the env-file name rule) lives.**
(a) A new data file `references/env-file-names.json` (env-file rule + sample markers), read only by `env_probe.env_file_kind`,
used by the inventory and by the gate's stray finder (samples excluded there). (b) A row in an existing references table.
(c) Keep the regex in code (AR-1 breach, today). — **Recommend (a)**, with the stray finder reading it too (C-7): three "what is an
env file" sites (`_is_env_file`, the regex, the gate's globs) become one. Cost: one new file in the release fingerprint, one
loader; the stray finder stops considering `.envrc` / `.env-backup`-shaped names (advice only, never a block). No existing table
fits (b): the nearest, `test-path-markers.json`, is about test files.

**F-e — whether `_loaded_env_files`' conftest fallback joins the one chooser.**
(a) It stays the gate's own step: its question differs ("what does the runner really load when the config names nothing", from
project code); other readers keep reading only what the config names. (b) The one road: the whole order (config → loader
evidence as data rows → `<tests_root>/.env`) moves into `env_probe.env_files`, every reader gets it (part E). (c) (b) plus a config
key recording the runner's loading. — **Recommend (b)** (designer rule 6: the one-road option), as part E after C. What covering
the left-out side costs: today in a project whose config names no file, the gate reads the conftest's `.env` while the recorder
reads none (state `file`) and stand_health reads only the process — one stand, three answers. (b) costs: the loader evidence
becomes data rows (python-dotenv, pytest-dotenv now; node dotenv and others as rows — the present scan is Python-only, itself a
road off axis 34); the documented meaning "an empty `env_file` means the process environment" (`config-keys.json:625`, the
`env_probe` docstring :34-36) changes and gets a `note_history` entry. If the Lead takes (a), the Python-only scan is an axis-34
residual and must become a node with owns and a test (finding into the next untaken batch).

**F-f — does the inventory carry the stand's addresses (values) with their files?** (not in the brief's list; raised by §0)
(a) Names only, as today; the per-key source is already in `env_files` rows (`path` + `keys`); the role proposes no value: the
address is asked outright or quoted from a cited README / compose line. (b) A new field `stand_addresses` (A-6): for every
scanned env file, real and sample, the non-secret-named keys whose value is an http(s) address, value through `safe_url`, each
row with its `path` and `sample` flag, real files first, capped. — **Recommend (b):** it removes the role's only reason to open an
env file (P5/P6: data by code; P27: code owns data, the role judges which address is the stand's), and it is where the brief's
"per-key source file" carries meaning — a source per VALUE; a separate names-only `key_sources` index would duplicate
`env_files` rows. Cost: the p1 law "values are never read out of an env file" is narrowed to "except the addresses the inventory
gives" (a change of meaning of a phase law: PROJECT.md "package change" rule 6(b) — critic on plan before the builder); secrets are
protected by the `SECRET_NAME` filter and `safe_url`. Under (a), part A drops A-6 and part B uses the (a) wording of B-1 / B-3.

**F-g — the chosen file when only samples exist.**
(a) Keep the sample as `env_file` (its names feed the access proposal, today's behaviour and the quarantined pins K-9.1 / K-10.1)
and add `env_file_is_sample: true`. (b) `env_file: ""`, `env_file_found: false`, the sample's names used under a separate field.
— **Recommend (a):** no field changes meaning (AR-22 readers unchanged), the flag carries the fact, part B says it to the person.
Cost: a reader that ignores the flag still sees a sample path under `env_file` — the readers are p1/p2 (part B) and
`render_access` (:588 "where"), which the builder checks and names.

**F-h — the home of the new test rows.**
(a) Table functions in `test_manual_capture.py` (keep; its `covers` already lists `env_probe.py`, `gate_preflight.py`,
`stand_health.py`), named by the DoD explicitly where `--witness-for` does not print it (project_inventory.py, source_inventory.py
and the other D files are covered by other keep rows or none). (b) Variant rows of a scenario story. — **Recommend (a):** the reader
table already exists there (`of3_1e_one_env_file_parse`), one table per behaviour (docs/TESTING.md); no new test file. Cost: the
file's `covers` list does not name `project_inventory.py` etc., so `--witness-for` on those paths alone will not print it — the DoD
names it by hand; widening `covers` is `tools/test_quarantine.py`'s, not a builder's.

**F-i — owns beyond the frozen node rows.**
(a) Widen the dispatches' owns as drafted and record it in each batch's «Ход» (an allowed edit of a taken batch). (b) Keep the
nodes to their rows and file the extra readers (part D's `project_decisions`, `readiness`, `brief_pack`, `judge_run`,
`config-keys.json`; part C's `manual_capture`) as a finding for the next untaken batch. — **Recommend (a):** leaving those readers
on their own choosers is the second road this topic exists to remove (P31); the row text "один читатель … списка env-файлов"
covers them in meaning. Cost: the zone check (б) between in-work batches sees paths not in the rows; the queue lines of §4 carry it.

---

## 6. Small technical choices closed by the designer

1. The `example` field of `env_files` rows keeps its name (readers: `judge_discovery.py:10,44`, `p1-discovery.md:156`); its meaning
   ("a sample") is unchanged — only its source moves to the table.
2. The gate keeps `configured_env_files` / `env_values` as delegates with unchanged signatures; callers (`brief_pack`, `walk_pool`,
   `manual_capture`, `project_decisions`, `stand_health`) are not migrated in this spec (one hop, one reader).
3. No de-duplication of `env_files` entries (C-1): today's later-wins order on `[a, b, a]` is kept.
4. An absent or unreadable `references/env-file-names.json` raises a `ValueError` that names the file (A-2), no built-in fallback.
5. Function names `env_files`, `env_layers`, `env_file_kind` sit outside the census unit-name families, so no census row is born.
6. `STAND_ADDRESSES_MAX = 10` and the 300-character address limit (A-6, under F-f (b)).
7. `_frontend_hint` names the distinct winning files of the shown keys, in list order (C-6).
8. `config-keys.json` `needed_by`: add `env_probe.py:env_files`, remove nothing whose function still exists (D-7).

---

## 7. Analogs and contradictions noticed (reported, not widened)

- **Secrets leak (safety):** `machine_facts.secret_values` (:345) reads only `environment.env_file`: a project with only
  `env_files` gets no file value redacted in `collect_pack` (:629). Closed by part D (D-2); the Lead may want it first.
- `brief_pack._stand_address_lines` :2565 prints `block.get('env_file')` — the word `None` with an `env_files`-only config (D-5).
- `env_probe.probe` prints the ACCOUNT value (:965) and non-secret `extra_keys` values (:974) to the role — by design (comment
  :962-964), reads only the configured file; noted because §0's claim "code gave no value" is about the batch-3 route only.
- `stand_health._env_values` silently skips an unreadable file (FR-41); kept in C-4, a residual for the next untaken batch.
- `judge_run._env_files` and `audit_factory` read `environments[].env_file` — a per-stand key that `config-keys.json` has no row
  for (grep `env_file` there: only `environment.env_file` / `env_files`); AR-22 question for the Lead, not touched.
- `test_frontend_reader.py:179` (quarantined) still expects `export FRONTEND_URL` unread (t-229 digest); not touched.
- The OF4-12 finding says `stand_health._env_values` reads one `cfg["env_file"]`; on main it already reads
  `gate_preflight.configured_env_files` (`stand_health.py:439`) — only the empty rule differs now.
- The OF4-12 finding's item 1 direction ("`stand_health._env_values` calls `gate_preflight.env_values`") is met by F-a (b) through
  `env_layers`; its item 4 names `test_stand_health.py` (quarantined) — rows go to the keep file instead (F-h).
- No SIBLING_MAP axis covers env files today (grep `env_file|configured_env_files|parse_env_file` over `docs/SIBLING_MAP.md`,
  case-insensitive: one hit, axis 5 row :127, the login carriers) — axis 37 is new (part C).

---

## 8. Reading trail

Read (whole or the cited ranges):
- `plans/piles/onboarding-forge/findings/20261112-discovery-nazyvaet-env-a-chitala-env-example.md` (whole)
- `.claude/worktrees/of-batch4/plans/piles/onboarding-forge/findings/20261112-spisok-env-fajlov-i-pustye-znacheniya-chitayutsya-raznymi-dorogami.md` (whole)
- `plans/piles/onboarding-forge/batch-1-onboarding-roles-forge.md` :1-12, :60-71 (OF1-1 row :67; status «в работе»)
- `.claude/worktrees/of-batch4/plans/piles/onboarding-forge/batch-4-hvosty-onbordinga-i-forzha.md` :1-60 (OF4-12 row :39; queue :10)
- `ai-packages/qa-factory/scripts/env_probe.py` :1-170, :330-354, :460-536, :900-980
- `ai-packages/qa-factory/scripts/gate_preflight.py` :1015-1064, :5060-5159
- `ai-packages/qa-factory/scripts/stand_health.py` :415-454
- `ai-packages/qa-factory/scripts/manual_capture.py` :595-644
- `ai-packages/qa-factory/scripts/source_inventory.py` :25-94
- `ai-packages/qa-factory/scripts/machine_facts.py` :290-350
- `ai-packages/qa-factory/scripts/project_inventory.py` :220-509
- `ai-packages/qa-factory/scripts/config_contract.py` :1050-1079
- `ai-packages/qa-factory/scripts/brief_pack.py` :2528-2567
- `ai-packages/qa-factory/scripts/readiness.py` :198-220, :605-624
- `ai-packages/qa-factory/scripts/walk_pool.py` :138-157
- `ai-packages/qa-factory/scripts/judge_run.py` :310-349
- `ai-packages/qa-factory/scripts/project_decisions.py` :628-647 and its def list
- `ai-packages/qa-factory/scripts/tests/test_manual_capture.py` :1970-2034; `test_manual_actor.py` :586-613
- `ai-packages/qa-factory/scripts/tests/scenario_walk.py` :880-936 (`witness_for`)
- `ai-packages/qa-factory/scripts/tests/test-layers.json` :1-60, :1560-1604, :2910-2939, :4255-4309; greps for the env readers' test files (keep < :6985 `quarantine`)
- `ai-packages/qa-factory/scripts/tests/test_judgment_census.py` (grep: `units_of`, the C1 rule and unit-name families)
- `ai-packages/qa-factory/skills/qa-onboarding/phases/p1-discovery.md` :30-165; `p2-interview.md` :135-190
- `ai-packages/qa-factory/design/architecture.md` :44-228 (AR-1…AR-21, AR-29); change-check lines grep (:53-280)
- `ai-packages/qa-factory/references/config-keys.json` :768-769 and grep `env_file`
- `ai-packages/qa-factory/design/role-rules.json` (row format)
- `docs/SIBLING_MAP.md` axis headings, :127, :582-594; `docs/TESTING.md` :100-139 and grep `covers`; `plans/builder-rules.md` 7b
- `experiments/mybooks/factory-vs-free-agent/notebook.md` :104-143; `runs/onboarding-3.json`, `runs/onboarding-4.json` (grep, `result` text)
- `logs/journal/dev1.jsonl` :606-609 (t-229, t-230)

Greps with their controls:
- `get\("env_file"\)|\["env_file"\]|env_files` over `scripts/*.py` — 133 hits read (found `judge_run`, `project_decisions` :636, `readiness` :621, `audit_factory`, not in the t-229 digest).
- `configured_env_files|env_values\(|load_env\(|runtime_credential_values|_env_files_state\(|parse_env_file\(|secret_values\(` — callers list (brief_pack, walk_pool, readiness, collect_pack added to the digest's).
- `env_probe|stand_health` over `skills/qa-onboarding` — only `p4-generate.md` (:273, :309, :319): env_probe is not run before the batch-3 question.
- `3002` over `runs/onboarding-3.json` — found (positive control for the `.{0,N}x.{0,N}` form); `env.example` over all `runs/` first returned nothing with a 160-char window, then found in `onboarding-4.json` with `sample|stand` — the first empty result was a miscall, not used as a negative.
- `env_file|configured_env_files|parse_env_file|env-file` over `docs/SIBLING_MAP.md` (case-insensitive) — one hit :127 (control: the same call found it).
- census: `configured_env_files|env_values|…` over `judgment-census.json` — no hit; positive control `"gate_preflight.py"` — 28 hits.
- `**/env.example` under `C:\QAFactory\exp-fvf` — nothing; the stand copies are elsewhere and were not located: the layout of the
  MyBooks test repo (`env.example` without a dot) is taken from the finding and the role's own words, not verified on disk.

Not verified (labelled): the route's tool call (§0); whether `scenario_walk.py --witness-for` prints `test_manual_capture.py` for
`project_inventory.py` (no Bash in this role: the DoD names it by hand, F-h); the existence of a role-rules registry test by name
(B DoD point 2 relies on the witness line).

---

## 9. Lead decisions (coordinator Opus, lead_degraded window; «по рекомендации, до слова владельца», 13.11.2026 01:4x)

- F-a: (b). `env_probe` holds `env_files` / `env_layers`; the gate keeps one-line delegates.
- F-b: (a). Empty or blank means not set in every VALUE reader; readers of names keep the name. Error direction: ask or refuse, never proceed.
- F-c: (a). File over process, a later file over an earlier one. The PURPOSE parameter `process=False` for the recorder and the stand-key readers is read as ONE function with a declared parameter (P31); it goes to the owner as a question in the morning report.
- F-d: (a). `references/env-file-names.json`, read only by `env_probe.env_file_kind`; the stray finder reads it too.
- F-e: (b). One road, part E after C. The meaning change of an empty `env_file` gets a note_history entry.
- F-f: (b). A `stand_addresses` field. The p1 law is narrowed, which changes the meaning of a phase law, so a critic on the plan (t-238; report file t-236-t-231-plan-review.md) runs before any builder.
- F-g: (a). Keep the sample as `env_file`, plus `env_file_is_sample: true`.
- F-h: (a). Table functions in test_manual_capture.py, named by hand in the DoD.
- F-i: (a). Widen the owns and record this in each batch's «Ход».

Order: A and B start after t-230 merges (accepted, wip/oh3-42r b4e0fbc); C after A; D after C; E after C.
Status: decisions taken. NOT dispatchable until the critic on the plan, t-238, is accepted.
