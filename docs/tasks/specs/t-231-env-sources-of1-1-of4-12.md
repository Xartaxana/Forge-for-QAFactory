# t-231 — where env values and env-file names come from (OF1-1 + OF4-12): SPEC

Status: fixes applied (t-239); dispatchable for A-D after the coordinator's check. Part E deferred (appendix), F-e switched to (a) (§5, §9).
History: DRAFT by designer (t-231), 13.11.2026; Lead decisions §9; critic on plan t-236/t-237 (GO-WITH-FIXES A-D, NO-GO E); fix round t-239 (§10).
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
- `skills/qa-onboarding/phases/p1-discovery.md:46` — signal row "Candidate environments | `docker-compose*.yml`, `.env.example`, …",
  `:45` — "Test-data lifecycle | … `.env.example` naming test accounts" and `:44` — "Architecture and data | … external
  integrations (SDK/API clients, env vars naming URLs)" — direct the role to OPEN env files and the sample for environment facts,
  i.e. for values (ports, addresses).
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
row (AR-1, part A), `env.example` scanned and marked (part A), and (F-f (b), decided) the origins of the http addresses the env
files hold, each with the file it was read from and a sample flag — field `env_file_addresses`. Not a phrase detector over the
role's text (FR-12).

---

## 1. Package invariants touched, owners, census classes

**AR-n touched, each with the change check written into the DoD of the part that touches it:**

| AR | how this spec touches it | change check (in the DoD of part …) |
|---|---|---|
| AR-1 | the env-file name rule and the sample markers move from code (`project_inventory.py:233`, `:275` regex; `gate_preflight._stray_env_file` globs `.env*`, `*.env` :5128) into one data file. A fourth name site, `guard_secrets.py:20-22` `DEFAULT_SECRET_FILE_PATTERNS`, serves another action (blocking writes to secret files, project-overridable through `secret_file_patterns`, over-blocking is its safe side): KEPT, named as a consumer in axis 37 (§2a) | A: `grep -n -i -E "example\|sample\|template\|dist" scripts/project_inventory.py` (positive control before the change: the regex at :275); C: `grep -n -F -e '".env*"' -e '"*.env"' scripts/gate_preflight.py` (positive control before the change: the globs of `_stray_env_file`). After: no file-NAME test outside the table reader |
| AR-2 | which file is the stand's and whether a value is the stand's stays the role's and the person's judgment; code marks `example`, names the file, and gives only an origin with `has_path` | name what the role still decides (A, B): "which of the found addresses is this stand's, its full base path, and whether a sample's address means anything for it" |
| AR-11 | p1/p2/p3 text changes the onboarding role's load | `role_load.py --all` before and after (B) |
| AR-13 | one chooser of the env-file list, one layering of values; `parse_env_file` stays the one content reading; `env_probe.origin` stays the one origin reader | grep for `get("env_file")` / `get("env_files")` / `os.environ` merges with a positive control; every reader calls the survivor (C, D) |
| AR-15 | the survivor is wired at every site; a new survivor gets a SIBLING_MAP axis. **Named deviation (t-239, Lead):** the axis-37 row is a Lead-tier write (SIBLING_MAP «Keeping the map up to date»: below-lead sessions put drafted axes into `CURRENT_CONTEXT.md` «Lead Queue»). In this lead_degraded window C's package commit goes WITHOUT the SIBLING_MAP row; the row text is drafted in §2a and queued to the full Lead with a pointer to this spec; "same commit" is NOT met and is recorded as such | list every site (§2 table); C's report confirms the §2a draft against the built code; the coordinator writes the Lead Queue entry (C) |
| AR-22 | new inventory fields (`env_file_is_sample`, `env_file_addresses`, `env_file_addresses_more`) each have a reader (p1, p2, p3, `render_access`); `references/config-keys.json` `needed_by` rows of `environment.env_file` / `env_files` name the new reader | grep the field names over `scripts/ agents/ skills/ references/ handoffs/` (A, B, D) |
| AR-28 / FR-59 | an absent or unreadable env file is never read as "the key is not there" silently beyond what each caller does today; a listed-but-missing file among present ones is a named detail, never silent | the edge rows of C state each caller's consequence; a test row per state (C) |
| AR-29 | every check this spec adds or alters is named with its class and owner below | `python -m pytest ai-packages/qa-factory/scripts/tests/test_judgment_census.py -q` (A, C, D); the loader's row is an explicit DoD key of A |

AR-3 (no new config key: F-e is (a) for now, so no key and no meaning change of an empty `env_file`), AR-4 (paths stay relative;
absolute and `..` entries keep today's behaviour), AR-9 (one refusal text changes: `load_env`'s fatal line for several files;
door unchanged) — touched only as noted in the edges.

**P31 / axis 34 (one road).** No language, project or framework is branched on by A-D. One per-PURPOSE difference: the recorder
and the stand-key readers call the same `env_layers` with `process=False` (F-c, one function with a declared parameter; the
consumer table §2a lists every reader's value). One road left behind and named: the gate alone looks at the project's conftest /
pytest-dotenv setup when the config names no file — a Python-only scan (`gate_preflight.py:5090-5112`). Under F-e (a) (t-239) it
stays for now as an axis-34 residual: **the coordinator files it as a finding** into the next untaken onboarding-forge batch,
with owns `scripts/gate_preflight.py (_loaded_env_files)`, `scripts/env_probe.py (env_files)`, `references/env-file-names.json`
(loader-call rows) and the test named (rows in the existing loaded-files table of `scripts/tests/test_gate_preflight.py`), and adds
the kept-road row of §7 to `docs/tasks/specs/reports/t-2046-language-exceptions-census.md`. The deferred part E (appendix) is that
finding's starting text.

**Checks added or altered — owner and census class (AR-29, P27):**

| check | where | class | owner it serves | census row |
|---|---|---|---|---|
| the name table is present and well-formed (`env_probe._env_file_names`, the loader: reads through `hooklib.read_json`, `raise ValueError` when absent or malformed) | A | shape (the form of a package data file) | data (code) | **NEW row required** (census rule u3, `test_judgment_census.py:22`: a body with `raise ValueError` is a unit whatever its name): `{file: scripts/env_probe.py, function: _env_file_names, class: shape, owner: data}` in the census's own row format, same commit. `shape` carries no ceiling, so no ratchet moves |
| is a file NAME an env file / a sample (`env_probe.env_file_kind`) | A | shape (the name's form against a data table) | data | none: the name is outside the u1 families and its body holds no refusal site (the raise lives only in the loader) |
| an empty or blank value is "not set" (`env_probe.env_layers`) | C | shape (presence) | data | none expected (u1/u3 do not apply) |
| which files count (`env_probe.env_files`) | C | shape (config read) | data | none expected |
| a variable sits in a file nothing loads (`gate_preflight._stray_env_file`, now skipping samples) | C | xref | data | none today; unchanged |
| the doctor's direct-Jira credential check (`readiness.check_jira_direct`, its resolver loop and source note) | D | its existing row (u1 `check_*`) | data | existing row, class unchanged; the builder confirms the row and states it in the report |
| is this address the stand's; is a sample's value relevant; the full base path | B (role text) | — not code | judgment (onboarding role), accepted by the person at the summary gate (intent) | none: no code check is added; FR-12 forbids a detector over the role's wording |
| redaction candidates from every configured file (`machine_facts.secret_values`) | D | safety | data (protection of secrets) | none today |

---

## 2. The one model (what every reader ends on)

| fact | survivor (F-a (b), decided) | today's readers that must end on it |
|---|---|---|
| the CONTENT of one env file | `env_probe.parse_env_file` (unchanged) | already all; `project_inventory.env_file_keys` and `machine_facts._env_file_values` are t-230's (not owned here) |
| WHICH files count | `env_probe.env_files(env_cfg, root) -> (list[Path], how)` — the body of today's `gate_preflight.configured_env_files`, moved; the gate's name stays a one-line delegate | `gate_preflight.configured_env_files` (delegate), `stand_health._env_values`, `env_probe.load_env` :131, `env_probe._derived_frontend` :483, `env_probe._frontend_hint` :518, `source_inventory.runtime_credential_values` :58-66, `machine_facts.secret_values` :345, `config_contract.env_key_names` :1061-1069, `project_decisions.record_stand_account` :636-641, `readiness.config_fails_own_probe` :621, `brief_pack._stand_address_lines` :2565, `judge_run._env_files` :321 (its `environment` part), `project_inventory.access_discovery` :434 (switched by part D, D-8) |
| the VALUES set for a reader | `env_probe.env_layers(files, *, process=True) -> (values, source_of, problems)`: process layer (if `process`) then each listed file in order; a later layer wins; an empty or blank value is never a value and never erases one (F-b, F-c) | `gate_preflight.env_values` (delegate), `stand_health._env_values`, `manual_capture._env_files_state` (`process=False`), `env_probe.load_env`, `env_probe._derived_frontend` / `_frontend_hint` (`process=False`), `source_inventory.runtime_credential_values` (and through it `readiness.check_jira_direct`) |
| is a file NAME an env file, a sample, or neither | `env_probe.env_file_kind(name) -> "env" \| "sample" \| ""` over `references/env-file-names.json` (F-d) | `project_inventory._is_env_file` :232, the regex :275, `gate_preflight._stray_env_file` globs :5128 |
| the origin of an address | `env_probe.origin` (unchanged; the ONE origin reader) | `project_inventory` `env_file_addresses` rows (A-6) |
| the files the RUNNER loads when the config names none | stays `gate_preflight._loaded_env_files` (F-e (a), t-239); axis-34 residual filed as a finding (§1) | — |

`machine_facts.secret_values` reads the chooser's files but does NOT layer: redaction needs every value of every file (union),
not the winner — a different action, stated so it is not mistaken for a second layering road.

### 2a. Draft SIBLING_MAP rows (queued to the full Lead; NOT written by any part)

The coordinator puts both drafts into `CURRENT_CONTEXT.md` «Lead Queue» with a pointer to this section when part C is accepted;
the full Lead writes them into `docs/SIBLING_MAP.md` (its own mechanism commit with its axes block). C's report confirms the
function names against the built code and lists any difference.

**New axis 37 — "Env files: which files, which values, which names" (draft).** Survivors: `env_probe.env_files` (which files),
`env_probe.env_layers` (which values), `env_probe.parse_env_file` (content), `env_probe.env_file_kind` over
`references/env-file-names.json` (is a name an env file / a sample). A new reader picks a ROW of the consumer table, never a new
flag or a new list:

| reader | layering | safe direction |
|---|---|---|
| `gate_preflight.env_values` (delegate) | `process=True` | empty = not set: the gate asks |
| `stand_health._env_values` | `process=True` | empty = not set: the probe reports missing; unreadable file skipped (FR-41 residual, §7) |
| `env_probe.load_env` | `process=True` | every configured file absent → fatal; a listed file missing among present ones → named in `sources` |
| `source_inventory.runtime_credential_values` (→ `readiness.check_jira_direct`) | `process=True` | empty = missing; the doctor names the file a winning value came from |
| `manual_capture._env_files_state` (→ `walk_pool._env_key_names`) | `process=False` | the account comes only from a file the project wrote; unreadable → refuse |
| `env_probe._derived_frontend` / `_frontend_hint` | `process=False` | a machine variable never becomes a stand key or a frontend candidate |
| `machine_facts.secret_values` | union of process + every listed file, no layering | over-redaction |
| `config_contract.env_key_names`, `brief_pack._env_file_key_names`, `project_inventory.env_file_keys` | names only | a name the gate cannot read is never reported available |
| `project_inventory` scan / `render_access`, `gate_preflight._stray_env_file` | `env_file_kind` | a sample is never named as the stand's file |
| `guard_secrets.DEFAULT_SECRET_FILE_PATTERNS` | own patterns, project-overridable (`secret_file_patterns`) | over-block (kept; not a reader of the table — a different action) |
| `gate_preflight._loaded_env_files` (conftest fallback) | own step when the config names no file | axis-34 residual, finding filed (§1) |

**Axis 5, row "How the stand logs in" (:127) — edit (draft).** Replace "config `environment.env_file`/`user_key`/`secret_keys`"
with "config `environment.env_file` / `env_files` read through `env_probe.env_files` (axis 37), `user_key`/`secret_keys`".

---

## 3. Parts (builder dispatch drafts)

Order and hot files: §4. Each part's `designer:` line will be filled by the Lead at acceptance (the accepted path of this file).

### Part A — OF1-1 code: the env-file name table, `env.example` scanned and marked, the inventory's sample flag and address rows

given: this spec §0-§2 and §5 (as accepted); `ai-packages/qa-factory/design/factory-rules.md` whole; `plans/builder-rules.md`; `ai-packages/qa-factory/design/architecture.md` AR-1, AR-2, AR-13, AR-22, AR-29; `scripts/project_inventory.py` (:217-308, :392-496, :564-620 `render_access`); `scripts/env_probe.py` (:92 `SECRET_NAME`, :103-120 `parse_env_file`, :502-511 `http_address_keys`, :796-807 `origin`); `scripts/hooklib.py` `read_json`; `scripts/judge_discovery.py` :10, :44 (reader of `example`); `scripts/tests/test_manual_capture.py` :1975-2034 (the reader table); `scripts/tests/test_judgment_census.py` :16-40 (unit rules u1-u3); `scripts/tests/fixtures/judgment-census.json` (row format); `scripts/tests/test-layers.json` (keep rows); `docs/TESTING.md`; the OF1-1 finding
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\env-file-names.json (new)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\env_probe.py (env_file_kind and its table loader _env_file_names only — new functions)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\project_inventory.py (_is_env_file, scan_sources, access_discovery, render_access; one new function for the address rows) — NOT env_file_keys (t-230)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json (one new row: the loader)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_manual_capture.py (one new table function beside of3_1e_one_env_file_parse, registered in main())
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\ (one fragment)
non-goals: no value of a secret-looking name leaves any function; no URL path, query, fragment or userinfo leaves any function; no change to `parse_env_file`, `origin`, `env_file_keys`, `machine_facts`; no phase text (part B); no rename of the `example` field; no detector over a role's wording (FR-12); no edit to quarantined tests (test_project_inventory.py, test_env_access_onboarding.py); no change to `guard_secrets.py`; no switch of `access_discovery` onto `env_probe.env_files` (part D, D-8); no batch-file edit
handoff: builder report per `.claude/agents/builder.md` rule 7 with the FR walk (sections A, C, D, E, G) and the witness, to the coordinator
edges:
- A-1 (the name rule, F-d): `env_file_kind(name)` splits `name` on `.`, drops empty parts, lower-cases. "env" when the name matches the env-file rule of the table (rows: exact `.env`; prefix `.env.`; suffix `.env` — today's `_is_env_file`, unchanged in reach); "sample" when it is an env file AND any part equals a sample marker (`example`, `sample`, `template`, `dist`, plural forms as data rows), OR the name is exactly `env.<marker>` (the bare form, e.g. `env.example`); otherwise "". Invariant: a sample is never classified "env" — the marker errs toward "sample". Adversarial rows that must stay on that side: `.env.example`, `.env.EXAMPLE`, `.env.example.local`, `.env.local.example`, `example.env`, `env.example`, `env.sample`, `env.template`, `env.dist`, `.env.dist`, `.env.template.bak` → sample; `.env`, `.env.local`, `.env.test`, `.env.production`, `my.env` → env; `env.example.py`, `env.py`, `.envrc`, `environment.ts`, `` (empty name) → "". A non-ASCII name (`.env.пример`) → "env" (no marker matches; listed, not a sample).
- A-2 (table absent or unreadable): the table ships with the package. The loader `_env_file_names()` reads it through `hooklib.read_json` (axis 16) and raises `ValueError` naming `references/env-file-names.json`, what it expected (the keys) and that the package copy is damaged (FR-1); `env_file_kind` calls the loader and holds no raise of its own; nothing falls back to a built-in list (that would be the list in code AR-1 removes). The loader is a census unit (u3): its row `{class: shape, owner: data}` lands in `judgment-census.json` in the same commit. Invariant: no silent classification without the table.
- A-3 (temporal): the table is born in this part. Before it (main today) the inventory reads the regex; after it, the regex at :275 and the `_is_env_file` expression are gone and both read `env_file_kind`. Part C's `_stray_env_file` reads the table only after A is merged (queue §4).
- A-4 (`env.example` now scanned): it enters `env_files` with `example: true`, sorted after real files (`env_files.sort` by `(example, path)`, unchanged). It counts against `MAX_FILES` like any scanned file (no new cap). Invariant: a real env file is still listed before every sample.
- A-5 (the chosen file, positional, F-g): `access_discovery` takes the declared file from `environment.env_file` as today (part D, D-8, switches it to `env_probe.env_files`). The declared entry is normalised before it is compared with the scanned rows (relative posix paths): `PurePosixPath(entry.strip().replace("\\", "/")).as_posix()`, so `./.env` and `.\.env` match the row `.env`; an absolute entry or one with `..` matches no row (AR-4, today's behaviour); no case-folding. The chosen row is the first scanned row whose path equals a declared file, else the first non-sample row, else the first sample row (today's fallback kept so the names still feed `propose_access`). New field `env_file_is_sample: bool` — true exactly when the chosen row is a sample. A DECLARED sample (the config names `.env.example`) is chosen as declared — the person's word — and then `env_file_is_sample` is true. Invariant: `account_pairs`, `frontend_candidates`, `frontend_same_origin` stay empty whenever the chosen file is a sample, declared or fallen back to (today's guards :468, :475 kept); a sample is never the chosen file while a real env file exists UNLESS the config declares that sample, and then the flag says so.
- A-6 (F-f (b) — the address rows): new field `env_file_addresses`: one row `{key, address, has_path, path, sample}` per key whose value in a scanned env file (real or sample) is an http(s) address, keys from `env_probe.http_address_keys(values, set())` (so a secret-looking NAME never appears). `address` is the ORIGIN only, built from `env_probe.origin(value)` = `(scheme, host, port)`: `scheme://host` plus `:port` only when the port is not the scheme default (80 / 443); an IPv6 host is bracketed (`http://[::1]:3000`). `has_path` = the value's `urlsplit(...).path.strip("/")` is non-empty. Userinfo, path, query and fragment never leave the function. Error direction: the row errs toward showing LESS — a secret carried in a URL path (a webhook, a bot token) or in userinfo (a DSN) is never output; what still shows is the host, which is the address the person must confirm (a secret placed in a hostname is the named residual of this direction). A value whose `origin()` is `()` (bad port, no host) gives no row and is not counted. Order: `env_files` order (real files first), then the file's key order. Cap `ENV_FILE_ADDRESSES_MAX = 10` rows with `env_file_addresses_more: N`; invariant of the cut: a real file's row is never cut while a sample's row is kept. An address longer than 300 characters is not listed (row omitted, counted in `env_file_addresses_more`); AT 300 listed, 301 not. An unreadable file (OSError, ValueError) gives no rows and no exception. An empty file, a file with no http value, no env files at all → `env_file_addresses: []` (declared empty outcome, AR-23). Invariant: no value of any other key is ever output, and no part of an address beyond its origin.
- A-7 (empty / absent inputs): no env file anywhere → `env_files: []`, `env_file: ""`, `env_file_found: false`, `env_file_is_sample: false`, `env_file_addresses: []` (today's shape plus the new fields). `config` None or without `environment` → declared files empty, the rest as A-5.
- A-8 (`render_access`, FR-37; :567, :588): with `env_file_is_sample` true, the first line reads `env file: none of this stand found - only a sample: <path> (<n> key names)` and `where` (:588) reads `the sample <path>`; with it false both lines are byte-equal to today. One new line when `env_file_addresses` is non-empty: `http address origins in env files: <path> <key> <address>[ (has a path, not shown)]; …` with a sample's rows prefixed `sample ` and `; and N more` from `env_file_addresses_more`. Invariant: the rendered text never prints a sample's path after `env file:` without the word "sample", and never prints more of an address than its origin.
siblings: `gate_preflight._stray_env_file` (the third "what is an env file" site) — part C; `guard_secrets.py:20-22` (fourth site, another action, kept — §2a); `judge_discovery.py` reads `example` (unchanged meaning, no edit); `p1-discovery.md:156` passes `"example":false` (unchanged); `access_discovery`'s switch to the chooser — part D (D-8).
DoD: (1) `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for scripts/env_probe.py scripts/project_inventory.py references/env-file-names.json scripts/tests/test_manual_capture.py scripts/tests/fixtures/judgment-census.json` and every file it prints, each in its canonical form, PLUS `python -B ai-packages/qa-factory/scripts/tests/test_manual_capture.py` by name (keep; the witness line does not print it for project_inventory.py, critic t-236) — green; (2) the new table function in test_manual_capture.py holds: every A-1 row through `env_file_kind`; one fixture `.env` (`BASE_URL=http://localhost:3000`) + `env.example` (`BASE_URL=http://localhost:3002`) through `access_discovery`: `env.example` listed with `example: true`, `env_file == ".env"`, `env_file_is_sample` false, `env_file_addresses` = the `.env` row (`http://localhost:3000`, `sample: false`) before the `env.example` row (`http://localhost:3002`, `sample: true`); one fixture with only `env.example` → `env_file_is_sample` true, pairs and candidates empty, and `render_access` prints "only a sample: env.example"; a declared `./.env` and a declared `.\.env` choose `.env`; a declared `.env.example` beside a real `.env` → chosen `.env.example`, `env_file_is_sample` true, pairs and candidates empty; address rows: `SLACK_WEBHOOK_URL=https://hooks.slack.com/services/T0/B0/abcdefSECRET` → `https://hooks.slack.com`, `has_path` true, the secret absent from the whole `access_discovery` output and from `render_access`; `TELEGRAM_BOT_URL=https://api.telegram.org/bot123456:AAH-xyz/` → `https://api.telegram.org`, `has_path` true, the token absent; `SENTRY_DSN=https://k3y@o1.ingest.sentry.io/42` → `https://o1.ingest.sentry.io`, `has_path` true, `k3y` absent; `http://u:p@host/x?q=1` → `http://host`, `has_path` true; `http://localhost:3000/` → `has_path` false; `http://[::1]:3000` → `http://[::1]:3000`; `http://host:99999` → no row; a secret-looking NAME with a URL (`API_KEY_URL`) → no row; the cap AT 10 and BEYOND (11 → `env_file_addresses_more: 1`, the cut row a sample's); an address AT 300 / 301 characters; the table file absent → `ValueError` naming it (a byte copy of the table restored after, hygiene pt. 7, hash compared); (3) AR-1 check: `grep -n -i -E "example|sample|template|dist" ai-packages/qa-factory/scripts/project_inventory.py` — the report lists every hit and shows none is a file-NAME test (comparison, regex or glob on a name); comments and the `example` field are listed and judged (positive control: the same grep before the change finds the regex at :275); gate_preflight.py is NOT grepped here (its `template`/`dist` words are noise; its globs are C's check); (4) `python -m pytest ai-packages/qa-factory/scripts/tests/test_judgment_census.py -q` green WITH the new loader row (`scripts/env_probe.py` `_env_file_names`, class `shape`, owner `data`) present in the diff of `judgment-census.json`, and no ceiling raised; (5) `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang` green; (6) the report names what the role still decides (AR-2): which found address is this stand's, its full base path when `has_path` is true, and that a sample's address is never it.
designer: <accepted path of this file, filled by the Lead>

### Part B — OF1-1 text: the role never presents a sample's value as the stand's

given: this spec §0, §1, §5 (as accepted); part A's field names (`example`, `env_file_is_sample`, `env_file_addresses` with `{key, address, has_path, path, sample}`, `env_file_addresses_more`); `skills/qa-onboarding/phases/p1-discovery.md` (:30-50, :89-145); `skills/qa-onboarding/phases/p2-interview.md` (:130-190); `skills/qa-onboarding/phases/p3-summary-gate.md` (:55-70, «What was found»); `references/human-questions.md`; `design/role-rules.json` (row format, e.g. :5); `scripts/role_load.py`; `scripts/tests/test_role_rules.py` (the registry test); `docs/TESTING.md` («Правила ролей не теряются»); `design/factory-rules.md` whole; `plans/builder-rules.md`
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\skills\qa-onboarding\phases\p1-discovery.md
C:\QAFactory\forge-repo\ai-packages\qa-factory\skills\qa-onboarding\phases\p2-interview.md
C:\QAFactory\forge-repo\ai-packages\qa-factory\skills\qa-onboarding\phases\p3-summary-gate.md (one line in «What was found», :59-62)
C:\QAFactory\forge-repo\ai-packages\qa-factory\design\role-rules.json (one new row)
non-goals: no code; no new question (the stand question of topic 2 keeps its count); no phrase list the code would match (FR-12); no other phase file; no other p3 line; no batch-file edit
handoff: builder report with the FR walk (B, C, E) and the witness, to the coordinator
edges:
- B-1 (the contradiction inside p1): rows `:44`, `:45` and `:46` no longer send the role into env files or `.env.example` for values. `:44` reads "env var NAMES that hold URLs (the inventory's `env_file_addresses` gives their origins with the file)"; `:45` / `:46` read: the inventory's env-file rows marked `example` are SAMPLES — they show which key names a project expects (test accounts, environments); their values are the sample's, never the stand's. `:144-145` is rewritten to one law that matches the rows: "you never read values out of an env file: the inventory gives the address origins it may (`env_file_addresses`, each with its file and a sample flag); every other value — names only". Invariant: no line of p1 tells the role to open an env file or a sample for a value.
- B-2 (the value a person sees): every value shown to a person names the file it came from as the inventory gives it ("`.env`: `BASE_URL` → http://localhost:3000"); when `has_path` is true the role says the file's value carries a path the inventory does not show, and the person gives the full base. A row with `sample: true` is shown, if at all, only as "the sample file `env.example` shows …", apart from the stand's facts, and is never the default answer of a question. `env_file_is_sample: true` is said as "the repository holds only a sample env file (`<path>`): no file of this stand was found" (a declared sample: "the config names a sample file (`<path>`)"). Invariant: a sample's value never reaches a person as the stand's value; a path the inventory withheld is never invented.
- B-3 (p2 topic 2, positional — `p2-interview.md:137-143`): "When discovery found no address" now means: no `env_file_addresses` row of a non-sample file. The stand question proposes the non-sample origin with its file (and asks for the base path when `has_path` is true); when two non-sample files disagree, both are shown with their files and the person picks (the role does not choose silently, AR-2). Invariant: a sample's address is never proposed even when it is the only address found — then the question asks outright, as `:137` already says.
- B-4 (rule kept from loss): one `design/role-rules.json` row, id `env-sample-value-not-stand`, rule "A sample env file's value is never shown as the stand's; every value shown names the file it came from", carriers p1, p2 and p3 with a 2-6 word anchor each present in the new text.
- B-5 (empty outcomes): no env file → unchanged text path (the address is asked); `env_file_addresses: []` → the address is asked outright; the role never fills the gap from a sample.
- B-6 (p3 summary, OF1-1 row "вопрос и сводка называют источник"): one line in «What was found» (`p3-summary-gate.md:59-62`): an env value in the summary names the file it came from, and a sample's value is never shown as the stand's (it may appear only labelled as the sample's). Invariant: the summary the person accepts never carries a value without its file.
siblings: `p4-generate.md` runs `env_probe.py` (prints the configured file's values: address, account) — reads the configured file, not a sample: no edit, named for the critic; `p2b-rediscovery.md:31` runs `project_inventory.py --access` per repository and inherits A-8's render (no edit).
DoD: (1) `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for skills/qa-onboarding/phases/p1-discovery.md skills/qa-onboarding/phases/p2-interview.md skills/qa-onboarding/phases/p3-summary-gate.md design/role-rules.json` and every file it prints, green; (2) `test_role_rules.py` (keep, named by the witness line for role-rules.json) green with the new row; (3) `python -B ai-packages/qa-factory/scripts/role_load.py --all` before and after, both outputs pasted, the onboarding role's number stated (AR-11); (4) `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang` green; (5) a doc-dispatch key-presence run (CLAUDE.md rule 11, three properties): keys quoted verbatim from B-1..B-6 (the new law line of p1, the `:44` names line, the "sample file" wording, the p2 proposal rule, the p3 summary line, the role-rules id), the script attached in full, with a negative control.
designer: <accepted path of this file, filled by the Lead>

### Part C — OF4-12 core: one chooser, one layering; the gate, stand_health, the recorder and env_probe on them

given: this spec §1, §2, §2a, §5 (as accepted); `design/factory-rules.md` whole; `plans/builder-rules.md`; `design/architecture.md` AR-13, AR-15, AR-28, AR-29; `scripts/gate_preflight.py` :1027-1053, :5072-5136, :5149-5158; `scripts/env_probe.py` :103-141, :336-352, :440-535, :905-975; `scripts/stand_health.py` :432-444, :492, :810; `scripts/manual_capture.py` :607-680, :4975-4985; `scripts/walk_pool.py` :143-149; `scripts/project_decisions.py` :697-730 (caller of `env_values`); `scripts/tests/test_manual_capture.py` :1975-2034; `scripts/tests/test_manual_actor.py` :545-640 (quarantined: read only, it pins the recorder's rules); the OF4-12 finding
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\env_probe.py (new env_files, env_layers; load_env, _block_frontend, _derived_frontend, _frontend_hint)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\gate_preflight.py (configured_env_files, env_values, _stray_env_file) — HOT file, function list
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\stand_health.py (_env_values)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\manual_capture.py (_env_files_state)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_manual_capture.py (of3_1e_one_env_file_parse and one new layering table function)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\ (one fragment)
non-goals: no change to `parse_env_file`; nothing of t-230's two functions; `_loaded_env_files` untouched (F-e (a): it stays the gate's own step; residual finding §1); no caller migration off the gate's delegate names (`configured_env_files`, `env_values` keep their signatures); no write to `docs/SIBLING_MAP.md` (axis 37 and the axis-5 edit are queued to the full Lead, §2a); no edit to quarantined tests (test_stand_health.py, test_manual_actor.py, test_frontend_reader.py); no batch-file edit
handoff: builder report with the FR walk (A, C, D, E, G) and the witness, to the coordinator
edges:
- C-1 (the chooser, F-a): `env_probe.env_files(env_cfg, root)` = today's `configured_env_files` body byte-for-byte in behaviour: a non-empty list `env_files` wins (blank entries dropped, order kept, no de-duplication — `[a, b, a]` reads `a` last, as today); `env_files` empty or not a list → `env_file`; neither → `([], "")`; `env_cfg` not a dict → `([], "")`. Absolute and `..` entries resolve as `Path(root) / entry` does today (AR-4 unchanged). `gate_preflight.configured_env_files` becomes a one-line delegate. Invariant (positional): `_loaded_env_files` still asks the config first, so a file the config names always beats the conftest fallback (the TP1-15045 class stays closed).
- C-2 (the empty rule, F-b): in `env_layers` a value whose `.strip()` is empty is never a value: `A=`, `A=""`, `A=''`, `A="   "`, `export A=`, a process `A=""` / `A="  "` → the key is absent from `values` unless another layer holds a non-empty value. An empty value never erases a non-empty one held by an earlier layer: a set file value under a later empty file value stays set, and a set PROCESS value under an empty file value stays set — both deliberately (python-dotenv's and node dotenv's default `override=False` do the same, and today's pins hold it); they are NOT the "ask or refuse" side: the factory proceeds with the earlier non-empty value. A non-blank value is kept as `parse_env_file` returned it (no strip added). `A="` (a lone quote) → `"` → set: the direction the t-172 critic accepted, unchanged. NAMES readers are not touched: a key with an empty value is still a NAME the file holds (`parse_env_file` keys, `brief_pack._env_file_key_names`, `env_file_keys`). Invariant: when NO layer holds a non-empty value for a key, the key never answers as set in any reader of values. Behaviour change named: `stand_health._env_values` and `load_env` stop returning `""` for such keys (callers read `.get(k, "")` / `or` — the builder greps each caller for `in values` / `in env` membership tests and lists them in the report; none found at :965-974, :1046 of env_probe, readiness :618).
- C-3 (the layering, F-c): process layer first (when `process=True`), then each listed file in order; a later layer wins. `manual_capture._env_files_state` calls `env_layers(files, process=False)`; `_derived_frontend` (:483) and `_frontend_hint` (:518) read the stand's own keys with `process=False`. Every reader's value is the §2a consumer table. Invariant: the recorder's account never comes from a machine variable (`USERNAME`, `USER`) and never from two sources (the user in a file, the password in the process: `test_manual_actor.py:592-597` stays true); a machine proxy variable (`HTTP_PROXY`) never becomes a frontend candidate.
- C-4 (absent, not-a-file, unreadable): `env_layers` returns `problems` = `[(path, "absent" | "unreadable")]`; "unreadable" = exists but is not a regular file, or `OSError` on read. Each caller's consequence is TODAY's, read from `problems`: the recorder → `({}, "unreadable")` at the first unreadable, `"file"` when none exists, `"ok"` otherwise (byte-equal states); `stand_health` → skips (today's silent skip; FR-41 residual named in §7); `gate_preflight.env_values` (delegate, returns the dict only) → absent and not-a-file skipped, an `OSError` on a regular file propagates as today. Invariant: no caller turns an absent or unreadable file into "the key is set"; none gets a weaker consequence than today.
- C-5 (`load_env`, positional and temporal): reads `env_files` (C-1) and `env_layers(process=True)`. One configured file absent → fatal with today's text byte-for-byte; several configured, none exists → fatal naming every file; some exist → not fatal, `sources` = `"process environment + <each file read, in order>"` followed by `"; listed but not found: <rel>[, <rel>]"` for every listed file in `problems` (absent or unreadable). With `env_file` alone, `sources` is byte-equal to today. `_block_frontend`'s note (:349) and `_derived_frontend`'s note (:472-473, :489-490) say "environment.env_file / env_files" only when the config used `env_files`; with `env_file` alone they stay byte-equal. Invariant: `load_env` never returns `fatal` None while every configured file is absent (an unknown is not a pass, FR-59), and a configured file that is missing is never silent: it is fatal (all missing) or a named detail in `sources` (some missing).
- C-6 (`_frontend_hint` text, FR-37): the line names the file(s) each shown key was read from (`source_of`), distinct files joined with ", " in list order; with one configured file the line is byte-equal to today.
- C-7 (`_stray_env_file`, F-d): candidates are files of the same folders whose `env_file_kind` is "env" (samples excluded) instead of the globs `.env*` / `*.env`. Behaviour change named: `.envrc`, `.env-backup` and similar are no longer candidates; a sample holding the variable is never named. Invariant: a sample is never named to a person as the file their variable sits in. Values still never leave the function (names only).
- C-8 (BOM literals, finding item 3): the U+FEFF characters inside string literals of `of3_1e_one_env_file_parse` (the "BOM on the first line" and "BOM before export" rows, and the two-file fixture) are written `\ufeff`; the bytes the test writes are unchanged. Invariant: no invisible character inside a test literal.
- C-9 (the reader table, test): the "empty value" rows (`A=`, `A=""`) keep their `parse_env_file` / `manual_capture._env_values` expectation `{"A": ""}` (content reading keeps empties) and the `stand_health._env_values` expectation becomes "absent"; a new layering table function judges `env_layers`, `gate_preflight.env_values`, `stand_health._env_values`, `manual_capture._env_files_state` and `load_env` on ONE set of rows: empty in the file / in the process / in both; `A=''`; `export A=`; blank quoted; a later file empty over an earlier value (stays set); a set process value under an empty file value (stays set, `process=True` readers); process vs file (F-c); `env_files` of two; `env_files` beats `env_file`; a missing file in the list (`load_env`'s `sources` names it); a directory in the list; none exists; `process=False` ignores the process. The row id names the case and the reader (P16).
- C-10 (temporal): no package artifact is created by this part. It reads `references/env-file-names.json` (born in part A) — C is queued after A; on a tree without A, C does not start. The axis-37 row and the axis-5 edit are NOT written here: §2a's drafts go to the full Lead's queue (AR-15 deviation named in §1); C's package commit goes without them.
siblings: §2a axis-37 consumer table (every site of §2); `walk_pool._env_key_names` (calls `_env_files_state`: inherits C-2 — a quoted-blank value now drops; no edit); `project_decisions.record_stand_frontend` path via `env_values` (inherits; no edit); `brief_pack._env_file_key_names` (names reader; no change); `guard_secrets.py:20-22` (own patterns, kept); part D readers; t-230's `machine_facts._env_file_values` / `project_inventory.env_file_keys` (not owned).
DoD: (1) `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for scripts/env_probe.py scripts/gate_preflight.py scripts/stand_health.py scripts/manual_capture.py scripts/tests/test_manual_capture.py` and every file it prints (it names test_manual_capture.py and test_gate_preflight.py among others), each in its canonical form — green; (2) the C-9 rows green, each row id naming case and reader; (3) AR-13 check: `grep -n -E "get\(\"env_files?\"\)" ai-packages/qa-factory/scripts/*.py` — after the change the hits in the files this part owns are `env_probe.env_files` only (positive control: the same grep before the change hits env_probe.py:131); AR-1 check: `grep -n -F -e '".env*"' -e '"*.env"' ai-packages/qa-factory/scripts/gate_preflight.py` — 0 hits after (positive control: the same command before the change lists the globs of `_stray_env_file`); (4) `python -m pytest ai-packages/qa-factory/scripts/tests/test_judgment_census.py -q` green, no ceiling raised; (5) `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang` green; (6) the report lists every caller membership test found under C-2, and confirms (or lists the differences from) the §2a axis-37 draft and axis-5 edit against the built function names.
designer: <accepted path of this file, filled by the Lead>

### Part D — OF4-12 readers: every other reader of the list ends on the chooser

given: this spec §1, §2, §2a, §5 (as accepted); part C's merged functions `env_probe.env_files` / `env_layers`; part A's merged `access_discovery` (A-5 normalisation); `design/factory-rules.md` whole; `plans/builder-rules.md`; `scripts/source_inventory.py` :36-82; `scripts/machine_facts.py` :308-360 (`_env_file_values` is t-230's: call it, never edit it); `scripts/config_contract.py` :1054-1070; `scripts/project_decisions.py` :605-660; `scripts/readiness.py` :175-232 (`check_jira_direct`), :600-625; `scripts/brief_pack.py` :2551-2570; `scripts/judge_run.py` :316-337; `scripts/project_inventory.py` :430-440; `references/config-keys.json` :768-769; `scripts/tests/test_manual_capture.py` (the layering table of part C, the table function of part A); `scripts/tests/test_readiness.py` :760-770; `scripts/tests/test_brief_pack.py`
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\source_inventory.py (runtime_credential_values)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\machine_facts.py (secret_values) — NOT _env_file_values (t-230)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\config_contract.py (env_key_names)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\project_decisions.py (record_stand_account)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\readiness.py (config_fails_own_probe; check_jira_direct: the resolver loop :204-215 and with_source :226-231 only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\brief_pack.py (_stand_address_lines)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\judge_run.py (_env_files)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\project_inventory.py (access_discovery: the declared-files lookup :434-438 only) — NOT env_file_keys (t-230)
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\config-keys.json (the needed_by lists of environment.env_file and environment.env_files only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_manual_capture.py (rows added to part C's layering table and part A's table function)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\ (one fragment)
non-goals: no change to what `secret_values` prints or logs (values never leave); no credential value in any note (`check_jira_direct` names keys and files only); `judge_run`'s `environments[].env_file` reading kept as is; no other function of `readiness.py` or `project_inventory.py`; no edit to quarantined tests (test_source_inventory.py, test_collect_redact.py, test_project_decisions_stand_facts.py, test_judge_run.py) — their stale rows are report lines; no batch-file edit
handoff: builder report with the FR walk and the witness, to the coordinator
edges:
- D-1 (`runtime_credential_values`, F-c): files from `env_files`, values from `env_layers(process=True)` with `environ` as the process layer when given. A new keyword `sources: dict | None = None`: when given, it is filled `{name: "<rel file>" | "process environment"}` for every name in the result (the winning layer, from `source_of`); the return value's shape is unchanged for every other caller. Behaviour change named: a non-empty process value no longer beats a file value, and with `env_file` + `env_files` both set only `env_files` is read. Quarantined `test_source_inventory.py` :353 ("process wins") and :368 ("env_file first") go red in quarantine-watch: one report line naming both, no edit.
- D-1a (`readiness.check_jira_direct`, FR-37, the doctor's source note): today the doctor consults the resolver only when `os.environ` lacks the name (:210) and records `from_file` only then, so after D-1 a name set in both the shell and the file would be reported as the shell's while the tracker reader uses the file's value — two records of one fact, the class the comment at :200-203 forbids. After: the loop always asks `runtime_credential_values(cfg, root, sources=…)` once; a name is present when the resolver holds a non-empty value; `from_file` = the names whose source is a file, and `with_source` names that file ("was found in the project's configured env file `<rel>`, which wins over this session's process environment"). The refusal (`cap(MISSING, …)`) is unchanged: it fires only when no layer holds the name, and then no source exists to name. Invariant: the doctor and the tracker reader resolve each name through the same layering, and whenever a file value wins the person is told which file. Values never appear in a note.
- D-2 (`secret_values`, safety): candidates from `environ` AND every file `env_files` names (union, not layered), each file through t-230's `_env_file_values(rel, root, gaps)`. Today a config with only `env_files` contributes NO file value to redaction — a leak this part closes. Error direction: over-redaction is the safe side. Adversarial inputs that must stay safe: `env_files` only; a value only in the second file; one key with different values in two files (both candidates); an empty value (no candidate); a listed file absent (a gap row per file, naming the file); a ` # note` tail (both candidates, as today).
- D-3 (`env_key_names`): names from the chooser's files (env_files wins) plus the process names. Behaviour change named: with both keys set, a name only in `env_file` is no longer available. Invariant: a name the gate cannot read is never reported available.
- D-4 (`record_stand_account` :636-641): `named` = the chooser returned files; `where` = the first chooser file, relative. Invariant: the file the refusal names is a file the gate reads (FR-37).
- D-5 (`config_fails_own_probe` :621) and (`_stand_address_lines` :2565): the place named is the chooser's file list as a person reads it (`manual_capture._file_names`), "the process environment" when it is empty. Invariant: never the word `None`, and with `env_file` alone byte-equal to today.
- D-6 (`judge_run._env_files`): the `environment` block's files come from the chooser (so `env_files` entries appear); `environments[].env_file` entries appended as today; names only, order: chooser files, then stand entries, de-duplicated as today.
- D-7 (`config-keys.json`): both rows' `needed_by` gain `env_probe.py:env_files`; entries whose function still exists stay; `gate_preflight.py:configured_env_files` stays (delegate); `project_inventory.py:access_discovery` under `env_files` (already listed, :769) becomes true. Invariant: every function that reads the key directly is listed (AR-22).
- D-8 (`access_discovery` onto the chooser, temporal — the switch A-5 leaves open): the declared files come from `env_probe.env_files(environment, root)`; each returned `Path` under `root` is turned into its relative posix form (`path.relative_to(root).as_posix()`), a path outside `root` matches no row (AR-4). The chosen row is the scanned row of the FIRST declared file found, in declared order (see fork F-j for the names of the later files); the fallback (first non-sample, then first sample) and the A-5 invariants are unchanged. Invariant: an `env_files`-only config chooses its listed file, never a fallback row, when that file is scanned; with `env_file` alone the output is byte-equal to A's.
siblings: `audit_factory._declared_paths` (:1021-1024, reads `env_file` for a path audit, not values — n/a: it audits the stored path, kept, named for the critic); `walk_pool` (inherits via C); `source_inventory.JiraClient` (inherits D-1 through `runtime_credential_values`, no edit).
DoD: (1) `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for scripts/source_inventory.py scripts/machine_facts.py scripts/config_contract.py scripts/project_decisions.py scripts/readiness.py scripts/brief_pack.py scripts/judge_run.py scripts/project_inventory.py references/config-keys.json scripts/tests/test_manual_capture.py` and every file it prints (test_readiness.py, test_brief_pack.py among the keep rows), plus test_manual_capture.py by name — green; (2) rows in the layering table, one config set through every D reader: `env_files` only; both keys; `env_file` only; a value only in the second file; empty in the later file; process vs file; plus the D-2 adversarial rows through `secret_values` (redaction candidates include the second file's value); `check_jira_direct` with the token set in both the process and the file → present, the note names the file; set only in the process → present, no file named; set nowhere → MISSING as today; `access_discovery` with an `env_files: [".env.qa"]`-only config and both `.env` and `.env.qa` scanned → chosen `.env.qa`; (3) the AR-13 grep of part C over these files leaves no direct `get("env_files")` / `get("env_file")` read except `judge_run`'s `environments[]` rows and `audit_factory` (positive control as in C); (4) `python -m pytest ai-packages/qa-factory/scripts/tests/test_judgment_census.py -q` green, the `check_jira_direct` row's class unchanged; (5) `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang` green.
designer: <accepted path of this file, filled by the Lead>

### Part E — DEFERRED (t-239). Not dispatchable. Text kept as the appendix at the end of this file.

---

## 4. Order, hot files, the «Командная работа» p.3 rule

| queue | why |
|---|---|
| t-230 → A, t-230 → C, t-230 → D | t-230 owns `project_inventory.env_file_keys`, `machine_facts._env_file_values` and a row in `test_manual_capture.py` (journal `dev1.jsonl:609`); A, C, D write those files (other functions) and `test_manual_capture.py` |
| A → C | batch order `очередь: onboarding-forge/1 → onboarding-forge/4` (batch-4 file :10); `env_probe.py` and `test_manual_capture.py` shared; C reads A's table |
| A ∥ B | disjoint owns; B's field names are fixed in this spec |
| C → D | D calls C's functions and adds rows to C's table |
| A → D | D edits `project_inventory.access_discovery` after A's edit of the same function (D-8); holds anyway through A → C → D |
| C → Lead Queue | on C's acceptance the coordinator queues §2a's axis-37 draft and axis-5 edit to the full Lead (AR-15 deviation, §1) |
| E | deferred; its successor is the axis-34 residual finding (§1) |

Hot files (PROJECT.md «Командная работа» p.3): `gate_preflight.py` is HOT — C owns `(configured_env_files, env_values, _stray_env_file)`.
Other in-work nodes on `gate_preflight.py`: OF1-4 (batch 1, the recorder browser probe) — a disjoint function list, and batch 1
merges before batch 4. Not hot but shared within batch 4: `env_probe.py` with OF4-23 (`environment` readers) and OF4-26 (direct
`utf-8-sig` config read) — the dispatches give disjoint function lists; `brief_pack.py` with OF4-21 / OF4-30; `project_decisions.py`
with OF4-8 / OF4-14 / OF4-28; `source_inventory.py` with OF4-14; `config_contract.py` with OF4-28 and OF1-2 (batch 1); `readiness.py`
(D owns `config_fails_own_probe`, `check_jira_direct`); `references/config-keys.json` with OF1-2 — each by function list (D lists its
functions), the later node merges `main` and resolves.

Node rows vs owns (F-i (a), decided): OF1-1's «Пишет в» does not list `references/env-file-names.json`, `design/role-rules.json`,
`p3-summary-gate.md` or `judgment-census.json`; OF4-12's does not list `manual_capture.py`, `config_contract.py`, `project_decisions.py`,
`readiness.py`, `brief_pack.py`, `judge_run.py`, `project_inventory.py`, `references/config-keys.json`. Recorded in each batch's «Ход».

---

## 5. Forks (returned; each with options and a recommendation; Lead decisions in §9)

**F-a — the survivor of "which files count" and of the layering.**
(a) `gate_preflight.configured_env_files` / `env_values` stay the survivors; every reader imports the gate. (b) Both move to
`env_probe` (`env_files`, `env_layers`), the gate keeps one-line delegates of the same names. (c) A new small module
(`env_sources.py`). — **Recommend (b):** `env_probe` already holds the one content reading (`parse_env_file`) and says in its
docstring it exists so no role parses `.env` itself; the hot file shrinks instead of growing; `source_inventory`, `machine_facts`
and `config_contract` would otherwise import a 5,000-line gate for one helper. Cost: two delegates remain in the gate (one hop);
(c) adds a module and an import edge for no gain.

**F-b — the empty-value rule, and its error direction when a stand key is empty.**
(a) Empty or blank = not set, in every reader of VALUES (the gate's rule today); names readers keep the name. (b) Empty = set to
"" (stand_health and `load_env` today). — **Recommend (a).** Error direction, scoped to a key that has NO non-empty value in any
layer: it reads as "missing" — the probe says MISSING, the gate asks, the recorder refuses with `key`: the factory asks or reports,
it never proceeds as if an address or a credential existed. Adversarial inputs that must stay on that side: `A=`, `A=""`, `A=''`,
`A="   "`, `export A=`, process `A=""`, an empty process value under an empty file value. Kept on the OTHER side on purpose
(the earlier non-empty value survives and the factory proceeds with it): an empty value in a later file over a set one, and a set
process value under an empty file value — python-dotenv's and node dotenv's default `override=False` behave the same, and today's
pins (`test_manual_capture.py:2023`, `test_manual_actor.py:605-609`) hold it; an empty value is never an instruction to unset. Also
kept on the other side: `A="` (lone quote → `"`, set; accepted by critic t-172). Cost: `stand_health` and `load_env` callers see
`None` where they saw `""` (C-2 asks the builder to list membership tests).

**F-c — the layering order (process vs file; first vs later file).**
(a) File over process, later file over earlier — the gate, `stand_health`, `load_env` and the recorder's file order today; and
the pinned tests (`test_manual_capture.py:2023`, `test_manual_actor.py:605-609`). (b) Process over file, first file wins —
`source_inventory` today, and also the default of python-dotenv (`override=False`) and of node dotenv: a variable already in
the process is not replaced, and a later loaded file does not replace an earlier one. (c) A per-project config key
(`environment.env_override`) asked at onboarding (AR-3). — **Recommend (a)** for this node: it is what four readers and the
gate's question texts already say, and the gate's file list is what the doors name (FR-37); `source_inventory` moves.
Costs named: (1) a person who exports a token in the shell while a stale file holds another gets the file's token in the tracker
reader (today the shell's) — mitigated by D-1a: the doctor's note names the file that wins; (2) where a project's runner uses dotenv
defaults, a process variable that the runner would keep is reported as replaced by the file — the gate's "what the runner sees" can
differ from the runner in that one case. Measuring (2) on one live project (PROJECT.md rule 6(a)) is cheaper than building (c). The
PURPOSE exception inside (a): the recorder and the stand-key readers pass `process=False` — the account must come from a file the
project wrote (`USERNAME` / `USER` of the machine would otherwise answer a `user_key` of that name) and a machine proxy variable is
not a stand key. Under P31 this is one function with a declared parameter, not a second road (critic t-236 agrees); every reader's
value and safe direction is a row of the §2a consumer table.

**F-d — where the sample-name list (and the env-file name rule) lives.**
(a) A new data file `references/env-file-names.json` (env-file rule + sample markers), read only by `env_probe.env_file_kind`,
used by the inventory and by the gate's stray finder (samples excluded there). (b) A row in an existing references table.
(c) Keep the regex in code (AR-1 breach, today). — **Recommend (a)**, with the stray finder reading it too (C-7): three "what is an
env file" sites (`_is_env_file`, the regex, the gate's globs) become one. A fourth site, `guard_secrets.py:20-22`, answers another
question (which file a write must be blocked to, project-overridable, over-blocking safe) and is kept as a named consumer (§2a); it
already over-blocks `.env.example` through `\.env\.`, the safe side for its action. Cost: one new file in the release fingerprint,
one loader (a census unit, §1); the stray finder stops considering `.envrc` / `.env-backup`-shaped names (advice only, never a
block). No existing table fits (b): the nearest, `test-path-markers.json`, is about test files.

**F-e — whether `_loaded_env_files`' conftest fallback joins the one chooser.**
(a) It stays the gate's own step: its question differs ("what does the runner really load when the config names nothing", from
project code); other readers keep reading only what the config names. (b) The one road: the whole order (config → loader
evidence as data rows → `<tests_root>/.env`) moves into `env_probe.env_files`, every reader gets it (part E). (c) (b) plus a config
key recording the runner's loading. — Designer recommended (b) (rule 6, the one-road option). What covering the left-out side
costs: today in a project whose config names no file, the gate reads the conftest's `.env` while the recorder reads none (state
`file`) and stand_health reads only the process — one stand, three answers.
**Switched to (a) by the Lead in t-239** («по рекомендации, до слова владельца»). Reason: the critic on plan (t-236, fix 9 (i))
showed that (b) removes a value a person can say today. In the template (`references/templates/config.json:47`) and
`config-keys.json` `environment.note`, an empty `env_file` means "values come from the process environment (CI secrets, a secret
manager)"; under (b) an empty `env_file` would make every reader go looking for the runner's `.env`, and the config would have no way
left to say "process only; ignore the stray `.env`". Whether to add a "process only" setting, or to keep "empty = process" for every
reader except the gate's diagnosis, is the owner's call, not ours tonight.
**Question for the owner (plain words; for the morning report):** "When a project's settings name no env file, should every part of
the factory (the stand probe, the recorder, the stand health check) look for the `.env` that the project's test runner loads by
itself — the way the gate already does — or should 'no file named' keep meaning 'use only the variables of the process'? If the
first, we add a separate setting so a project can still say 'process only, ignore any stray `.env`'." / «Если в настройках проекта
env-файл не указан, должны ли все части фабрики (зонд стенда, рекордер, проверка стенда) сами искать `.env`, который грузит раннер
тестов проекта, как уже делает гейт, — или «файл не указан» по-прежнему значит «только переменные процесса»? Если первое — добавим
отдельную настройку, чтобы проект мог сказать «только процесс, лишний `.env` не читать».»
Per this fork's own (a) clause the Python-only loader scan is an axis-34 residual: the coordinator files it as a finding (owns +
test named, §1) and adds the kept-road row to the t-2046 census (§7). Part E stays as the deferred appendix with the critic's open
points.

**F-f — does the inventory carry the stand's addresses (values) with their files?** (not in the brief's list; raised by §0)
(a) Names only, as today; the per-key source is already in `env_files` rows (`path` + `keys`); the role proposes no value: the
address is asked outright or quoted from a cited README / compose line. (b) A new field `env_file_addresses` (A-6): for every
scanned env file, real and sample, the non-secret-named keys whose value is an http(s) address, each row the ORIGIN of the value
(`env_probe.origin`) with `has_path`, its `path` and `sample` flag, real files first, capped. — **Recommend (b):** it removes the
role's only reason to open an env file (P5/P6: data by code; P27: code owns data, the role judges which address is the stand's), and
it is where the brief's "per-key source file" carries meaning — a source per VALUE; a separate names-only `key_sources` index would
duplicate `env_files` rows. The field name is a DATA name (critic t-236 fix 2): it carries sample rows by design and does not claim
any row is the stand's (P27, the same class as "code never calls its index a radius"). Cost: the p1 law "values are never read out
of an env file" is narrowed to "except the address origins the inventory gives" (a change of meaning of a phase law: PROJECT.md
"package change" rule 6(b) — critic on plan before the builder, done t-236). Secrets: the `SECRET_NAME` filter judges the NAME only
and `safe_url` would keep the URL path, so a secret carried in a path (a webhook, a bot token) would leave under an innocent name
(critic t-236 F2, reproduced); hence the origin only — userinfo, path, query and fragment never leave, `has_path` tells the role a
path exists and the person supplies the full base in topic 2.

**F-g — the chosen file when only samples exist.**
(a) Keep the sample as `env_file` (its names feed the access proposal, today's behaviour and the quarantined pins K-9.1 / K-10.1)
and add `env_file_is_sample: true`. (b) `env_file: ""`, `env_file_found: false`, the sample's names used under a separate field.
— **Recommend (a):** no field changes meaning (AR-22 readers unchanged), the flag carries the fact, part B says it to the person.
The readers that would otherwise show the sample unmarked are p1/p2/p3 (part B) and `render_access` (:567 "env file:", :588
"where"), which part A now owns and marks (A-8).

**F-h — the home of the new test rows.**
(a) Table functions in `test_manual_capture.py` (keep; its `covers` already lists `env_probe.py`, `gate_preflight.py`,
`stand_health.py`), named by the DoD explicitly where `--witness-for` does not print it (project_inventory.py, source_inventory.py
and the other D files are covered by other keep rows or none). (b) Variant rows of a scenario story. — **Recommend (a):** the reader
table already exists there (`of3_1e_one_env_file_parse`), one table per behaviour (docs/TESTING.md); no new test file. Cost: the
file's `covers` list does not name `project_inventory.py` etc., so `--witness-for` on those paths alone will not print it — the DoD
names it by hand (verified by critic t-236); widening `covers` is `tools/test_quarantine.py`'s, not a builder's.

**F-i — owns beyond the frozen node rows.**
(a) Widen the dispatches' owns as drafted and record it in each batch's «Ход» (an allowed edit of a taken batch). (b) Keep the
nodes to their rows and file the extra readers as a finding for the next untaken batch. — **Recommend (a):** leaving those readers
on their own choosers is the second road this topic exists to remove (P31); the row text "один читатель … списка env-файлов"
covers them in meaning. Cost: the zone check (б) between in-work batches sees paths not in the rows; the queue lines of §4 carry it.

**F-j — the key names of the LATER declared files in `access_discovery` (new in t-239, raised by fix 5 / D-8).**
`access_discovery` gives ONE chosen file's names (`env_keys`, `keys_absent_from_env_file`, `account_pairs`). With `env_files: [a, b]`
the chooser makes `b` the winning layer for values, but the inventory's names come from one file. (a) The first declared file found
(D-8 as drafted); a key held only by `b` is reported "absent from the env file". Error direction: the interview asks about a key
the stand already has — it asks more, never proceeds on a missing key (safe side); the residual becomes a finding. (b) `env_keys` =
the union of every declared file's names in list order, `env_file` = the first; `render_access` names all files. Changes the
meaning of `env_keys` (one file → several) for its readers (`propose_access`, p1, p2). — **Recommend (a)** for this node, with (b)
as a finding for the next untaken batch: (a) keeps every field's meaning and errs to the asking side; (b) is a field-meaning change
that deserves its own critic pass. D-8 is executable by the recommendation until the Lead decides.

---

## 6. Small technical choices closed by the designer

1. The `example` field of `env_files` rows keeps its name (readers: `judge_discovery.py:10,44`, `p1-discovery.md:156`); its meaning
   ("a sample") is unchanged — only its source moves to the table.
2. The gate keeps `configured_env_files` / `env_values` as delegates with unchanged signatures; callers (`brief_pack`, `walk_pool`,
   `manual_capture`, `project_decisions`, `stand_health`) are not migrated in this spec (one hop, one reader).
3. No de-duplication of `env_files` entries (C-1): today's later-wins order on `[a, b, a]` is kept.
4. An absent or unreadable `references/env-file-names.json` raises a `ValueError` that names the file (A-2), no built-in fallback;
   the raise lives in the loader `_env_file_names` only, read through `hooklib.read_json`.
5. Census: the loader `_env_file_names` IS a unit (u3, the raise) and gets a row `{class: shape, owner: data}` — the refusal judges
   the form of a package data file; `shape` has no ceiling, so no ratchet is raised (class `safety` would raise its ceiling, AR-20).
   `env_file_kind`, `env_files`, `env_layers` hold no refusal site and sit outside the u1 families: no row.
6. `ENV_FILE_ADDRESSES_MAX = 10` and the 300-character address limit (A-6).
7. `_frontend_hint` names the distinct winning files of the shown keys, in list order (C-6).
8. `config-keys.json` `needed_by`: add `env_probe.py:env_files`, remove nothing whose function still exists (D-7).
9. Address render (A-6): `scheme://host`, `:port` only when not the scheme default, IPv6 bracketed; `has_path` from the path only
   (query and fragment are dropped without a flag — the person confirms the full base in topic 2 anyway).
10. Declared-path normalisation (A-5): `PurePosixPath(entry.strip().replace("\\", "/")).as_posix()`; D-8 compares
    `path.relative_to(root).as_posix()`; no case-folding.
11. `load_env`'s `sources` for a partly missing list: `"; listed but not found: <rel>[, <rel>]"` appended (C-5).
12. `runtime_credential_values` gains a keyword `sources=` instead of a new return shape (D-1), so no other caller changes.
13. `render_access` gets one line for `env_file_addresses` (A-8): a field a role reads in the non-JSON render must be in the render
    (AR-21), and A owns the function anyway.
14. Parts A and B carry only F-f (b) wording (the Lead decided (b)); the (a) alternatives are dropped from the edges.

---

## 7. Analogs and contradictions noticed (reported, not widened)

- **Secrets leak (safety):** `machine_facts.secret_values` (:345) reads only `environment.env_file`: a project with only
  `env_files` gets no file value redacted in `collect_pack` (:629). Closed by part D (D-2); the Lead may want it first (critic t-236:
  a solo node on the gate's current `configured_env_files` is possible).
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
  case-insensitive: one hit, axis 5 row :127, the login carriers) — axis 37 is new (§2a, queued to the full Lead); axis-37 collision
  check by critic t-236: no other "Axis 37".
- `guard_secrets.py:20-22` is a fourth env-file name site (critic t-236 F3), another action, kept and named in §2a.
- `SECRET_NAME` is duplicated at `judge_run.py:78` (critic t-236, pre-existing): a queue candidate, not this spec's.
- **Kept-road row for the t-2046 census** (the coordinator adds it with the axis-34 finding, §1), in that file's row format:
  `| runner's env-file loading when the config names none | gate_preflight.py : _loaded_env_files 5090-5112 | Python: conftest literal load_dotenv/dotenv_values paths, bare walk-up, pytest-dotenv env_files; other languages: only <tests_root>/.env | a Node/other project whose runner loads a differently named file gets the default .env in the gate's diagnosis | code | M |`
  (node: the residual finding; its starting text is the deferred part E).
- F-j's residual (union of declared files' names in `access_discovery`) — a finding if the Lead takes F-j (a).

---

## 8. Reading trail

Read (whole or the cited ranges), t-231:
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
- `ai-packages/qa-factory/scripts/tests/test-layers.json` :1-60, :1560-1604, :2910-2939, :4255-4309
- `ai-packages/qa-factory/scripts/tests/test_judgment_census.py` (grep: `units_of`, the C1 rule and unit-name families)
- `ai-packages/qa-factory/skills/qa-onboarding/phases/p1-discovery.md` :30-165; `p2-interview.md` :135-190
- `ai-packages/qa-factory/design/architecture.md` :44-228; `references/config-keys.json` :768-769 and grep `env_file`
- `ai-packages/qa-factory/design/role-rules.json` (row format); `docs/SIBLING_MAP.md` axis headings, :127, :582-594;
  `docs/TESTING.md` :100-139; `plans/builder-rules.md` 7b
- `experiments/mybooks/factory-vs-free-agent/notebook.md` :104-143; `runs/onboarding-3.json`, `runs/onboarding-4.json` (grep)
- `logs/journal/dev1.jsonl` :606-609 (t-229, t-230)

Read in t-239 (fix round), to verify the fixes before applying them:
- `docs/tasks/specs/reviews/t-236-t-231-plan-review.md` (whole)
- `scripts/project_inventory.py` :425-614 (`access_discovery` :430-496, `render_access` :564-614: :567 "env file:", :588 `where`)
- `scripts/env_probe.py` :122-141 (`load_env`, `sources` string), :502-511 (`http_address_keys`: NAME filter + `http(s)://` prefix),
  :796-807 (`origin` returns `(scheme, host, port)` with the default port filled, `()` when not an absolute http(s) URL)
- `scripts/tests/test_judgment_census.py` :1-40 (u3 at :22), grep `ratchet|CEILING` (`CLASS_CEILING_KEYS` = word-list,
  meaning-proxy, meaning, safety: `shape` has no ceiling)
- `scripts/readiness.py` def list; :196-240 (`check_jira_direct`: resolver only when `os.environ` lacks the name :210, `with_source` :226-231)
- `scripts/source_inventory.py` :36-82 (`runtime_credential_values`: process first, file fills gaps)
- `scripts/stand_health.py` :430-445 (process layer + files: `process=True` in §2a)
- `scripts/guard_secrets.py` :14-29 (`DEFAULT_SECRET_FILE_PATTERNS` :20-27)
- `skills/qa-onboarding/phases/p1-discovery.md` :42-46 (:44 "env vars naming URLs" — critic F4 holds)
- `skills/qa-onboarding/phases/p3-summary-gate.md` :55-66 («What was found», :59-62); grep `env` (case-insensitive): :61, :123 — no
  env-value line today
- grep `project_inventory|--access|--json` over `skills/qa-onboarding/phases` (p1 :3, :47, :98-124; p2b :31 — the role reads both the
  render and `--json`, hence A-8's render line)
- `docs/SIBLING_MAP.md` :120-131 (axis 5 row :127), :632-641 (Lead-tier write; «Lead Queue» in `CURRENT_CONTEXT.md`)
- `docs/tasks/specs/reports/t-2046-language-exceptions-census.md` grep `conftest` (rows :27, :45: the row format used in §7)

Greps with their controls (t-231):
- `get\("env_file"\)|\["env_file"\]|env_files` over `scripts/*.py` — 133 hits read.
- `configured_env_files|env_values\(|load_env\(|runtime_credential_values|_env_files_state\(|parse_env_file\(|secret_values\(` — callers list.
- `env_probe|stand_health` over `skills/qa-onboarding` — only `p4-generate.md` (:273, :309, :319).
- `3002` over `runs/onboarding-3.json` — found (positive control); `env.example` over `runs/` — found in `onboarding-4.json` after a
  first miscall (not used as a negative).
- `env_file|configured_env_files|parse_env_file|env-file` over `docs/SIBLING_MAP.md` (case-insensitive) — one hit :127.
- census: `configured_env_files|env_values|…` over `judgment-census.json` — no hit; positive control `"gate_preflight.py"` — 28 hits.
- t-239: a Glob for `*QUEUE*.md` at the repo root returned nothing; not used as a negative — the Lead Queue's carrier was then read
  positively at `docs/SIBLING_MAP.md:639` (a section of `CURRENT_CONTEXT.md`).

Not verified (labelled): the route's tool call (§0); the census row's exact JSON keys (A's builder copies the format from
`judgment-census.json`, which A's given names); `parse_env_file`'s handling of `A=''` and `export A=` (taken from critic t-236; the
C-9 rows will show it).

---

## 9. Lead decisions (coordinator Opus, lead_degraded window; «по рекомендации, до слова владельца», 13.11.2026)

- F-a: (b). `env_probe` holds `env_files` / `env_layers`; the gate keeps one-line delegates.
- F-b: (a). Empty or blank means not set in every VALUE reader; readers of names keep the name. Error direction (scoped in t-239):
  when no layer holds a non-empty value — ask or refuse, never proceed; a later empty value never erases an earlier set one (kept
  set on purpose, dotenv `override=False`).
- F-c: (a). File over process, a later file over an earlier one. The PURPOSE parameter `process=False` for the recorder and the
  stand-key readers is read as ONE function with a declared parameter (P31); it goes to the owner as a question in the morning report.
- F-d: (a). `references/env-file-names.json`, read only by `env_probe.env_file_kind`; the stray finder reads it too.
- F-e: **switched to (a) in t-239.** `_loaded_env_files`' conftest fallback stays the gate's own step for now. Reason: critic fix 9
  (i) — under (b) an empty `env_file` could no longer say "process only", and whether to add a setting for that is the owner's call.
  The owner question is in §5 F-e (plain words, English and Russian). Part E is deferred (appendix, with the critic's (i)-(v) as open
  points). The Python-only loader scan is an axis-34 residual: the coordinator files it as a finding (owns + test named, §1) and adds
  the t-2046 census row (§7).
- F-f: (b), field renamed `env_file_addresses` (t-239, fix 2), address = origin only + `has_path` (fix 1). The p1 law is narrowed
  (meaning change: critic on plan done, t-236).
- F-g: (a). Keep the sample as `env_file`, plus `env_file_is_sample: true`; `render_access` marks it (A-8).
- F-h: (a). Table functions in test_manual_capture.py, named by hand in the DoD.
- F-i: (a). Widen the owns and record this in each batch's «Ход».
- F-j (new in t-239): (a) — names from the first declared file found; the union residual goes as a finding at D's acceptance (coordinator, 13.11 02:05, по рекомендации).
- AR-15 deviation (t-239, fix 8): axis 37 waits for the full Lead; C's code commit goes without the SIBLING_MAP row; §2a's drafts
  are queued to the full Lead («Lead Queue» in `CURRENT_CONTEXT.md`) with a pointer to this spec.

Fixes of critic t-236 applied in t-239: 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14 (where: §10). Fix 9: not applied — part E deferred.
Order: A and B start after t-230 merges (accepted, wip/oh3-42r b4e0fbc); C after A; D after C (and A). E deferred.
Status: fixes applied (t-239); dispatchable for A-D after the coordinator's check.

---

## 10. Fix round t-239

One line per item of the critic's fix list (t-236), applied (where) or returned (why):

1. Applied — A-6 (origin only through `env_probe.origin`, `has_path`, error direction, the hostname residual), A DoD (2) (Slack
   webhook, Telegram bot, DSN, userinfo/query, IPv6, bad port rows), §5 F-f (the "SECRET_NAME + safe_url" claim corrected), §6.9,
   A non-goals; `safe_url` dropped from A's given in favour of `origin`.
2. Applied — field `env_file_addresses`, cap `ENV_FILE_ADDRESSES_MAX`, `env_file_addresses_more`, everywhere: §0, §1 AR-22, §2,
   A-6/A-7/A-8 and A DoD, B given and B-1..B-5, §5 F-f, §6.6; the old name has no occurrence left in this file.
3. Applied — §1 census table (loader `_env_file_names`, u3 unit, row `{class: shape, owner: data}`), A-2 (`hooklib.read_json`,
   raise only in the loader), A owns (`judgment-census.json`), A DoD (4) (the row is an explicit key), §6.5.
4. Applied — A owns (`render_access`), A-8 (sample-only wording at :567 and :588, plus the address line), A DoD (2) row, §5 F-g.
5. Applied — D owns (`project_inventory.access_discovery`, the declared-files lookup only), D-8, D DoD (1)/(2) row, §2 reader
   table, §4 queue line A → D; the names of later declared files raised as the new fork F-j.
6. Applied — B-1 (`p1-discovery.md:44`), B owns `p3-summary-gate.md` (one line, B-6), B-4 carriers include p3, B DoD (1)/(5), §0.
7. Applied — §5 F-b (the two "stays set" rows relabelled with the dotenv `override=False` reason; error direction scoped to "no
   non-empty value in any layer"), C-2 and C-9 (rows `A=''`, `export A=`, set process + empty file), §9 F-b line.
8. Applied as the Lead decided — SIBLING_MAP removed from C's owns, C non-goals, C-10, C DoD (6), §1 AR-15 (deviation named),
   §2a (axis-37 draft), §4 (queue line to the Lead Queue), §9.
9. Not applied — part E deferred by the Lead's decision (F-e switched to (a)); the critic's (i)-(v) are kept as open points in the
   deferred appendix; the residual is the coordinator's finding (§1).
10. Applied — §1 AR-1 row, §5 F-d, §2a consumer table, §7, A/C siblings: `guard_secrets.py:20-22` named, kept, with its own safe
    direction (over-block, project-overridable).
11. Applied, with one correction of its premise — the consumer table is §2a (every reader, its `process` value and safe direction),
    referenced from §5 F-c and C-3. The source naming: the doctor's refusal fires only when no layer holds the name, so there is no
    source to name there; the real two-records gap is `check_jira_direct`'s `from_file` note, which consults the resolver only when the
    process lacks the name (`readiness.py:210`). Applied as D-1 (`sources=` keyword) + D-1a (the doctor always asks the resolver and
    names the winning file), D owns, D DoD (2).
12. Applied — C DoD (3) (`grep -F` for `".env*"` / `"*.env"` on gate_preflight.py with a pre-change positive control), A DoD (3)
    scoped to project_inventory.py with the gate_preflight noise named, §1 AR-1 row.
13. Applied — A-5 (normalisation of `./.env` and backslash entries; the declared-sample case, with the invariant corrected so a declared
    sample is legal and flagged), A DoD (2) rows; C-5 (`sources` names every listed-but-missing file; invariant: never silent), C-9 row.
14. Applied as text, written by others — the axis-5 row edit is drafted in §2a and queued to the full Lead with axis 37 (Lead-tier
    write); the t-2046 kept-road row is drafted in §7 and added by the coordinator with the axis-34 finding (§1), its node being that
    finding instead of OF4-12/E (E is deferred).

---

## Appendix — deferred part E (NOT dispatchable; starting text for the axis-34 residual finding)

Deferred in t-239: F-e is (a) for now (§5, §9). The text below is the t-231 draft, kept for the finding that carries the residual.
**Open points from critic t-236 (fix 9), each to be closed before any dispatch:**
- (i) AR-3 expressibility: `references/templates/config.json:47` and `config-keys.json` `environment.note` say "an empty env_file
  means values come from the process environment (CI secrets, a secret manager)"; after E a person has no way left in config to say
  "process only; ignore the stray `.env`". Owner question (§5 F-e): a declared "process only" value (template row + `config-keys.json`
  + interview topic), or "empty = process" for every reader except the gate's diagnosis.
- (ii) `env_files` would return `[<tests_root>/.env]` as the DEFAULT even when absent (`gate_preflight.py:5114`); C-5 makes `load_env`
  fatal for "one configured file absent", so every process-only project would turn fatal. The `how` of the step (config / evidence /
  default) must decide fatality, and E must state it.
- (iii) `manual_capture.read_login` reads `configured_env_files` (`manual_capture.py:678`); E changes its "None = names no file" branch,
  so `driver_stage_s6.py:1063` (`no_file`) and `walk_session.py:1277` (door text) change meaning unnamed; the delegate's name
  `configured_env_files` would lie (it would return files the config does not name).
- (iv) the signature `env_files(env_cfg, root, *, tests_root=None)`: `tests_root` is a top-level config key; the readers holding only
  `env_cfg` (stand_health, the recorder) are not told where to get it.
- (v) owns gap: E-2's `note_history` entry needs `references/config-keys.json` and `references/templates/config.json` (whose note must
  END the history: `config-keys.json:2`, checked by `test_config_migration.py`), `references/environments.md:10` and the `env_probe.py`
  docstring `:34-36`; `config-keys.json` is also D's, so a `D → E` queue line is owed.

Draft (t-231), unchanged:

given: this spec §2, §5 F-e; `scripts/gate_preflight.py` :5072-5119, :4532-4537, :4980, :5479; `scripts/planning_contract.py` :3606; part C's `env_files`; `references/env-file-names.json`; `references/config-keys.json` :477, :625
owns (draft, incomplete per (v)): `scripts/gate_preflight.py (_loaded_env_files)` — HOT file, function list; `scripts/env_probe.py (env_files: the no-config step)`; `references/env-file-names.json (loader-call rows)`; `scripts/tests/test_gate_preflight.py (rows in the existing loaded-files table)`
non-goals: no new config key unless option (c) is taken; no change to what the gate asks
edges (draft):
- E-1: `env_files(env_cfg, root, *, tests_root=None)`: config list → loader evidence (data rows: python-dotenv `load_dotenv(` / `dotenv_values(` literal paths and the bare walk-up; pytest-dotenv `env_files =`; further languages as rows) → `<tests_root>/.env` default. Invariant: a config-named file always wins; the evidence step reads code by data rows read through one reader, never a language branch (AR-1, P31).
- E-2 (temporal, the meaning of an empty `env_file`): `config-keys.json` :625 says "an empty env_file means values come from the process environment". Under E every reader that today reads only the process in an unconfigured project starts reading discovered files. The note gets a `note_history` entry in the same commit (AR-3 change check).
DoD (draft): `scenario_walk.py --witness-for` on the owns, green; rows: config wins; conftest literal; bare `load_dotenv()` walk-up; pytest-dotenv; default `.env`; no evidence and no file.
