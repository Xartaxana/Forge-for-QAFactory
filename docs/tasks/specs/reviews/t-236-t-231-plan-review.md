# t-236 — critic on PLAN: t-231 (OF1-1 + OF4-12, env sources)

Reviewer: critic (Opus), 13.11.2026. Under review: `docs/tasks/specs/t-231-env-sources-of1-1-of4-12.md` (parts A-E, §9 Lead decisions).
Dispatch DoD: an overall verdict, a verdict for each of F-a..F-i, and every fact found false, with file:line.
This verdict is an input to acceptance. The decision belongs to the Lead tier. The §9 decisions were taken in a lead_degraded window "по рекомендации, до слова владельца", so they stay provisional until the full Lead or the owner confirms them.

## Overall verdict: GO-WITH-FIXES

Parts A-D are GO once the fixes below are applied to the spec. Part E is NO-GO as drafted: its direction is right, but its edges and owns are incomplete (fix 9). E is conditional and sequenced after C, so holding it back does not hold A-D back.

Fixes that must land BEFORE a dispatch: 1, 2, 3, 4 (part A); 6 (part B); 8 (part C); 9 (part E). Fixes 5, 7 and 10-14 are spec-text fixes for the same round.

## Facts found false (file:line)

- F1. §1 census table rows 1-3 and §6 item 5 say "none expected: the name is outside the unit families". This is false for part A. A-2 makes `env_file_kind`, or its table loader, `raise ValueError`. Census rule u3 (`scripts/tests/test_judgment_census.py:22`: "the body holds a refusal site that `refusal_registry.sites()` sees (`deny`/`block`, `raise StateConflict|ValueError`)") makes that function a unit whatever its name. Without its row, C1 fails in the same commit. Fix 3.
- F2. §5 F-f: "secrets are protected by the `SECRET_NAME` filter and `safe_url`". This is false for a secret carried in a URL path. I ran the real functions (`env_probe.http_address_keys` + `http_client.safe_url`, verbatim output under Trail):
  `SLACK_WEBHOOK_URL -> https://hooks.slack.com/services/T0/B0/abcdefSECRET`, `TELEGRAM_BOT_URL -> https://api.telegram.org/bot123456:AAH-xyz/`.
  `SECRET_NAME` (`env_probe.py:92`, `(pass|secret|token|key|credential|auth)`) judges the NAME only. `safe_url` (`http_client.py:151-163`) keeps `parts.path`. Userinfo and query are cut correctly (`SENTRY_DSN`, `S3_URL` and `BASE_URL` came out clean). Fix 1.
- F3. §1 AR-1 row and §5 F-d say "three 'what is an env file' sites become one". A fourth site exists: `scripts/guard_secrets.py:20-22` `DEFAULT_SECRET_FILE_PATTERNS` (`\.env$`, `\.env\.`). It serves another purpose: blocking writes to secret files, project-overridable via `secret_file_patterns`, where over-blocking is the safe direction. Migrating it is not required, but it is unnamed. Fix 10.
- F4. B-1 names only `p1-discovery.md:45` and `:46` as the rows that send the role to values. `p1-discovery.md:44` ("Architecture and data | … external integrations (SDK/API clients, **env vars naming URLs**)") sends the role the same way. Fix 6.
- F5 (temporal edge without an owner). A-5 says `access_discovery` takes the declared files "from `env_probe.env_files` — after part C; until C is merged, from `env_file` as today". C and D do not own `project_inventory.py`, so nobody owns the switch. §2 lists `access_discovery :434` among the readers that must end on the chooser. After A→C→D, `access_discovery` still reads only `environment.env_file` (`project_inventory.py:434`), and `config-keys.json:769` already lists it under `env_files`, which it never reads. That is a second road, left behind. Fix 5.

Spot-checks that HOLD (§0 and the reader table):
- `p1-discovery.md:45` (Test-data, `.env.example` naming test accounts) and `:46` (Candidate environments, `.env.example`).
- `:144-145` "Values are never read out of an env file, here or anywhere: names only."
- `p2-interview.md:137`.
- `project_inventory.py:232-233` `_is_env_file`; `env.example` is not matched.
- `:274-276` (the regex, at :275).
- `:307` sort by `(example, path)`; `:434` the declared file is `env_file` only; `:155` `MAX_FILES = 4000`; `:467`/`:473` the sample guards.
- `env_probe.py:131` `load_env` reads `env_file` only; `:965`, `:974` print values; `p4-generate.md:273`.
- `gate_preflight.py:1027-1053` (the chooser, and `env_values` drops empties); `:5072-5114` `_loaded_env_files`; `:5124-5137` the globs.
- `stand_health.py:439` already on `configured_env_files` (§7 is right).
- `manual_capture.py:614-631`; `source_inventory.py:52-66` (process first, then the union of `env_file` and `env_files`); `machine_facts.py:345` (`env_file` only, so D-2's leak claim is TRUE); `config_contract.py:1061-1069`; `project_decisions.py:636-641`; `readiness.py:621`; `brief_pack.py:2565`; `judge_run.py:321`.
- F-h's claim also holds: `scenario_walk.py --witness-for scripts/project_inventory.py` does not print `test_manual_capture.py` (Trail). The role-rules registry test exists by name: `test_role_rules.py`, which closes §8's "not verified".

## Per-decision verdicts (question 2)

- **F-a (b): agree.** `env_probe` already holds the one content reading. The gate keeps one-hop delegates. This is AR-13 with no new module.
- **F-b (a): agree, with fix 7.** The direction (empty means not set, so the factory asks or refuses) is the gate's rule today (`gate_preflight.py:1049-1052`) and the recorder's (`manual_capture.py:628`). But the §5 list puts "an empty value in a later file over a set one (must not erase)" on the "asks" side, and it sits on the other side: the earlier value survives and the factory proceeds. Its process twin is missing: a set process value with `A=` in the file keeps the process value. Both rows are defensible: they match python-dotenv's and node dotenv's default `override=False`, and they match today's pins. The spec should say so instead of claiming they fall under "never proceed". Missing adversarial rows: `A=''` (single quotes stripped to empty), `export A=`, and "set process value + empty file value".
- **F-c (a) + `process=False`: agree it is one road.** One function (`env_layers`) is reached by every reader. The parameter separates PURPOSES ("what the runner sees" vs "an account the project wrote down"), not a language, project or case. Under brief question 12 this is "an ordinary condition of the task", not an exclusion. Two strengthenings (fix 11):
  - Axis 37 should carry a consumer table, as axis 9 does: each reader, its `process` value and its safe direction. Then a new reader picks a row instead of a flag.
  - D-1 makes a stale file token beat a fresh shell token for the tracker reader. The tracker or doctor refusal should name the file the value came from (`source_of`, FR-37), so the person sees why their export did not count.
  The owner question in the morning report is right.
- **F-d (a): agree, with fixes 3 and 10.** A data table and one reader follow AR-1 and the axis-9 pattern. Missing: the census row for the raising loader (F1); the guard_secrets site named as a consumer (F3); and C's DoD has no AR-1 check for the globs `".env*"` / `"*.env"`. The grep in A's DoD (3) cannot see a glob, and on `gate_preflight.py` the words `template`/`dist` produce a large amount of noise. Add `grep -n -F '".env*"' -e '"*.env"'` with a positive control taken before the change (fix 12).
- **F-e (b): agree in direction (P31, axis 34). Part E is NOT dispatchable as drafted (fix 9).** What the change of meaning breaks without a stated edge:
  - (i) AR-3: `references/templates/config.json:47` and `config-keys.json` `environment.note` say "an empty env_file means values come from the process environment (CI secrets, a secret manager)". After E, a person has no way left in config to say "process only; ignore the stray `.env`". The onboarding answer loses a value it can express.
  - (ii) `env_files` would return `[<tests_root>/.env]` as the DEFAULT even when that file is absent (`gate_preflight.py:5114`). C-5 makes `load_env` fatal for "one configured file absent", so every process-only project turns fatal in `env_probe`. The `how` of the step (config / evidence / default) must decide fatality, and E must state it.
  - (iii) `manual_capture.read_login` reads `configured_env_files` (`manual_capture.py:678`). E changes its "None = names no file" branch, so `driver_stage_s6.py:1063` (`no_file`) and `walk_session.py:1277` (door text) change meaning unnamed. The delegate's name `configured_env_files` then lies: it returns files the config does not name.
  - (iv) The signature `env_files(env_cfg, root, *, tests_root=None)`: `tests_root` is a top-level config key, and the readers that hold only `env_cfg` (stand_health, the recorder) are not told where to get it.
  - (v) Owns gap. E-2's `note_history` entry needs `references/config-keys.json` and `references/templates/config.json` (whose note must END the history: `config-keys.json:2` "about", checked by `test_config_migration.py`). It also needs `references/environments.md:10` and the `env_probe.py` docstring `:34-36`. None of these is in E's owns. `config-keys.json` is also D's, so a `D → E` queue line is owed.
  - Recommended: keep (b), and either add a declared "process only" value (option (c)-lite, AR-3: template row + `config-keys.json` + interview topic), or keep "empty = process" for every reader except the gate's diagnosis and put that to the owner as a P31 fork. Taking either is the Lead's or the owner's call.
- **F-f (b): agree in principle (P5/P6: data by code; P27 holds, because code gives rows with their file and a sample flag and does not choose). Conditional on fixes 1 and 2.**
  - (1) Secret leak (F2). Recommended: `address` = the origin only (scheme://host[:port], through `env_probe.origin`, the one origin reader) plus `has_path: bool`. The person confirms the full base path in topic 2 anyway. Add the adversarial rows: a webhook path, a bot-token path, a DSN.
  - (2) The field name `stand_addresses` states a judgment that P27 reserves to the role: the field holds sample rows by design and does not know which address is the stand's. This is the same class as P27's "код никогда не называет свой индекс радиусом". Rename it to a data name, e.g. `env_file_addresses`.
  The narrowed p1 law (B-1 (b) wording) is consistent once both hold.
- **F-g (a): agree, with fix 4.** `render_access` prints `env file: <path>` (`project_inventory.py:567`) and `where = discovery["env_file"]` (`:588`). For a sample-only repo it prints "env file: env.example" with no mark, which is the OF1-1 class in code (FR-37). A owns only `_is_env_file, scan_sources, access_discovery`, so the "builder checks and names" route of F-g cannot fix it.
- **F-h (a): agree.** Verified that the witness line does not print the file for `project_inventory.py`, so naming it by hand is needed.
- **F-i (a): agree.** Leaving the extra readers on their own choosers is exactly the second road this topic removes. The «Ход» record is an allowed edit of a taken batch. Machine zone checks do not see paths outside the rows, so the `очередь:` lines with OF1-2 (`config_contract.py`, `config-keys.json`) carry it. Note for C-10/fix 8: writing axis 37 into `docs/SIBLING_MAP.md` is Lead-tier ("Keeping the map up to date"). In the current degraded window it goes to the Lead Queue, and AR-15's "same commit" can then be met only if the package commit of C waits for the full Lead.

## Question 3: edges, owns, order

- Temporal: A-3 and C-10 are stated correctly (the table is born in A; C waits for it). F5 is the unowned temporal switch (fix 5). E-2's `note_history` edge is stated, but its owns are missing (fix 9).
- Positional:
  - C-1 keeps "config first" in `_loaded_env_files`. That is right.
  - A-5's order (declared → non-sample → sample) is stated with its invariant. Add the comparison form: declared files are `Path(root)/entry` and rows are relative posix, so `./.env` and backslash entries must still match. Add the case of a DECLARED sample: the chosen file is a sample, `env_file_is_sample` is true, and pairs and candidates stay empty (fix 13).
  - C-5: a list where some files are present and some absent becomes silent (only the files read are named in `sources`). A configured file that is missing must stay a named detail line, not fatal and not silent (FR-41/FR-59) (fix 13).
- Owns disjointness: A and B are disjoint. A→C→D share `env_probe.py` and `test_manual_capture.py` in sequence, which is fine. D ∥ E becomes non-disjoint once fix 9 adds `config-keys.json` to E, so write the queue line. The hot-file lists hold: `gate_preflight.py` C (`configured_env_files, env_values, _stray_env_file`) vs E (`_loaded_env_files`) are sequential. OF4-23 (`env_probe.data_cleanup`, finding N-r1 :15) and OF4-26 (`env_probe.py:1114`) are disjoint from C's functions, so §4's claim is verified.
- Order (§4): correct. Option for the Lead: D-2 is a live secret-redaction leak and could go ahead of D as a solo node on the gate's current `configured_env_files`.

## Question 4: class completeness (SIBLING_MAP)

Axes this plan touches:
- **34**: F-c covered; F-e under fix 9. The Python-only loader scan `gate_preflight.py:5090-5112` has no row in `docs/tasks/specs/reports/t-2046-language-exceptions-census.md`: grep for `dotenv|_loaded_env_files` found nothing, while the same grep found `conftest` rows at :27 and :45. Until E lands, name it as a kept road with node OF4-12/E (brief q.12 (c)) (fix 14).
- **5**: the "How the stand logs in" row at `:127` names config `environment.env_file`, and C/D move that to `env_files`/`env_file` through `env_probe.env_files`. Update the row together with axis 37 (fix 14). The "Acquisition ladder" row (env_probe, stand_health) is touched only by inheritance.
- **9-like / new 37**: the "is this an env file" leaf. guard_secrets is an unlisted consumer (F3).
- **16**: the table loader must read through `hooklib.read_json`. It is given in A's manifest; also state it in A-2 (fix 3).
- **18/32**: the census row (F1).
- **3**: the new references file enters the release fingerprint automatically (`release_fingerprint.py --write`). n/a beyond that.
- **1, 2, 12, 13**: n/a (no forge policy or role file is changed by the package parts). The axis-37 mechanism commit owes its own axes block.

Unrouted after this review: guard_secrets (fix 10), the axis 5 row (fix 14), the t-2046 census row (fix 14), the p3 summary. OF1-1's row says "вопрос и сводка называют источник". B leaves `p3-summary-gate.md` as a report line, so the node's own scope is not met by any owner. B should own one line there, or the Lead records why n/a (fix 6).

## Question 5: census and judgment

No new check judges meaning. `env_file_kind` checks a name's form against a data table (shape/data). `env_layers` checks presence (shape). The stray finder is an xref. `secret_values` is safety. Only one class claim is wrong: F1, an unacknowledged u3 unit, which needs a `{class: shape, owner: data}` row. If the table-damage refusal is meant to guard the package, the class is `safety`, and the builder names whichever it is. The role-text part (B) adds no detector (FR-12 holds). The `stand_addresses` NAME is the one P27 issue: code naming its own index as the stand's (fix 2).

## Standing questions

- DUPLICATION AND CONSISTENCY: no second implementation planned. `http_address_keys`, `origin`, `parse_env_file` and `safe_url` are reused. Grepped: `\.env\*|"\*\.env"|env\.example` and `"\.env|'\.env|\.env\b` over `scripts/*.py`; the positive control was the known hits `gate_preflight.py:5096-5114` and `project_inventory.py:394/411/467`. New finding: `guard_secrets.py:20-22` (F3). Pre-existing, not this plan's: `SECRET_NAME` is duplicated at `judge_run.py:78`. A queue candidate, not a finding against this spec.
- CODE QUALITY: no code yet. Part E's delegate name `configured_env_files` would lie after E (fix 9 (iii)).
- ONE ROAD (q.12): F-c is not an exclusion (purpose condition, shared function reached). F-e is under fix 9. The kept Python-only scan is named in fix 14. No language branch is added by A-D: grepped for language/runner names in the spec's edges, none found.

## Fix list (each with § and the expected change)

1. §3 A-6, §5 F-f, §6.6: `address` = origin only (`env_probe.origin`, scheme://host[:port]) plus `has_path`, or else state a different path policy with its error direction. Add adversarial rows: Slack webhook path, Telegram bot path, DSN with userinfo. Correct the "secrets are protected by SECRET_NAME + safe_url" sentence. BLOCKS A.
2. §3 A-6/B-1..B-5, §5 F-f, §1 AR-22: rename `stand_addresses` to a non-judging data name (e.g. `env_file_addresses`), and `STAND_ADDRESSES_MAX` with it. BLOCKS A/B (B's field names are fixed in the spec).
3. §1 census table, §6.5, A-2: the raising loader is a u3 census unit. Add its row (shape/data, or safety) in the same commit as an explicit DoD key. The loader reads through `hooklib.read_json`. BLOCKS A.
4. §3 A owns + edges: add `project_inventory.render_access` (:567, :588). With `env_file_is_sample` true, the line says only a sample was found (`<path>`) and no file of this stand. Add a DoD row. BLOCKS A.
5. §3 D owns (or a late A step after C): `project_inventory.access_discovery` switches to `env_probe.env_files`, with a test row (`env_files`-only config chooses the listed file). §4 gets the queue line.
6. §3 B-1: add `p1-discovery.md:44` ("env vars naming URLs") to the rewritten rows. B gains one line in `p3-summary-gate.md` (an env value in the summary names its file, and a sample's value is never shown as the stand's), or the Lead records n/a against OF1-1's "сводка" with a reason. BLOCKS B.
7. §5 F-b and C-2: relabel "a later empty over a set one" and add "set process + empty file". Both stay set by design (dotenv `override=False`, today's pins); give the reason. Add rows `A=''` and `export A=`. Scope the error-direction sentence to "no non-empty value in any layer".
8. §3 C-10, §4: axis 37 is a Lead-tier write. In the degraded window, C's package commit waits for the full Lead or the deviation from AR-15's "same commit" is named. BLOCKS C's commit, not its build.
9. §3 Part E: state (i) the "process only" expressibility (an owner/Lead fork); (ii) `how`-dependent fatality in `load_env` for an absent default or evidence file; (iii) consequences for `read_login`, `driver_stage_s6.py:1063`, `walk_session.py:1277`, and the delegate's name; (iv) where `tests_root` comes from; (v) owns: `references/templates/config.json` (note), `references/config-keys.json` (note_history), `references/environments.md`, the `env_probe.py` docstring, plus a `D → E` queue line. BLOCKS E.
10. §1 AR-1, §5 F-d, axis 37 text: name `guard_secrets.py:20-22` as a consumer with its own safe direction (over-block, project-overridable). Keep it or queue it.
11. §5 F-c / axis 37: a consumer table with `process` and safe direction per reader. D-1: the tracker/doctor refusal names the source file (`source_of`).
12. §3 C DoD (3): an AR-1 grep for the globs `".env*"` / `"*.env"` with a positive control before the change. A's grep (3) scoped to `project_inventory.py`, with the noise on gate_preflight named.
13. §3 A-5: path normalisation for declared entries (`./.env`, backslashes) and the declared-sample case. C-5: a missing listed file among present ones is a named detail line, never silent.
14. §1/§7 and the axis-37 commit: update the axis 5 row `:127` (login carriers) to the chooser; add a kept-road row for the Python-only loader scan to the t-2046 census (node OF4-12/E).

## Trail

Read:
- the spec (whole); the OF1-1 finding (whole); `batch-1 :1-14, :67-74`; `batch-4 :1-14, :39, :50, :53`; finding N-r1..N-r8 (grep `env_probe`).
- `p1-discovery.md` (grep env/value; :40-50, :140-160); `p2-interview.md :130-145`; `p3-summary-gate.md` (grep).
- `project_inventory.py :225-240, :268-280, :395-500`, render_access grep.
- `env_probe.py :20-45, :92, :100-145, :330-355, :440-540, :796-808, :960-975`; `gate_preflight.py :1020-1060, :5068-5160`.
- `stand_health.py :428-448`; `manual_capture.py :600-650`; `source_inventory.py :50-70`; `machine_facts.py :340-350`; `config_contract.py :1058-1070`; `project_decisions.py :632-642`; `readiness.py :617-623`; `brief_pack.py :2562-2567`; `judge_run.py :318-324`.
- `driver_stage_s6.py :1020-1075`; `walk_session.py :1265-1282`; `guard_secrets.py :15-40`; `http_client.py :151-173`.
- `config-keys.json :2, :470-480, :620-630, :764-772`; `templates/config.json :47-49, :107`; `environments.md :10`.
- `test_judgment_census.py :16-40, :61`; `docs/SIBLING_MAP.md` headings, axes 5, 9, 16, 32-34, keeping-up-to-date; t-2046 census (grep); `docs/tasks/critic-diff-brief.md`; `tools/critic_verdict.schema.json`.

Reruns (verbatim):
- `python -B -c "...env_probe.http_address_keys(vals,set()) ... http_client.safe_url(...)"` →
  `SLACK_WEBHOOK_URL -> https://hooks.slack.com/services/T0/B0/abcdefSECRET` / `TELEGRAM_BOT_URL -> https://api.telegram.org/bot123456:AAH-xyz/` / `SENTRY_DSN -> https://o1.ingest.sentry.io/42` / `S3_URL -> https://b.s3.amazonaws.com/f` / `BASE_URL -> http://localhost:3000/api` (`API_KEY_URL` filtered by name, as designed).
- `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for scripts/project_inventory.py scripts/env_probe.py skills/qa-onboarding/phases/p1-discovery.md design/role-rules.json references/config-keys.json` →
  project_inventory: scenarios cart_1/local_1_0108/local_1_arm_b + keep test_exploration, test_exploration_identity, test_regression_scope, test_release_fingerprint (no test_manual_capture). env_probe: … keep test_manual_capture.py. role-rules.json: keep test_role_rules.py. config-keys.json: keep test_config_migration.py, test_human_questions.py, test_readiness.py.
- Axis-37 collision check: `grep -rln "Axis 37"` over docs/, plans/ and the worktree maps, plus every remote branch's SIBLING_MAP: only the spec itself, so no collision.
- A content grep for other env-file name sites over `scripts/*.py` (patterns in the DUPLICATION line). The positive control found the known `gate_preflight.py:5096-5114` hits. New hit: `guard_secrets.py:20-22`.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "A-6/F-f: safe_url keeps the URL path, so a secret in a path (Slack webhook, Telegram bot token) under a name SECRET_NAME does not match leaves through stand_addresses; empirically reproduced",
    "A-2/§1/§6.5: the raising table loader is a census u3 unit (test_judgment_census.py:22); the spec says no row is born, so C1 fails",
    "F-g/part A owns: render_access (project_inventory.py:567,:588) prints a sample as the env file and is not owned",
    "F-f naming: stand_addresses names a judgment P27 reserves to the role while carrying sample rows",
    "B-1: p1-discovery.md:44 also sends the role to env values; the p3 summary of the OF1-1 node scope has no owner",
    "Part E: an absent default .env would turn load_env fatal; empty env_file loses the process-only expressibility (AR-3); read_login/driver_stage_s6:1063/walk_session:1277 consequences unstated; owns miss templates/config.json, config-keys.json note_history, environments.md",
    "C-10: the axis 37 write is Lead-tier; in the degraded window the AR-15 same-commit condition needs the full Lead or a named deviation"
  ],
  "class_completeness": "Axes touched: 34 (F-c covered as one road with a declared purpose parameter; F-e direction right, part E not dispatchable; the Python-only loader scan gate_preflight.py:5090-5112 has no t-2046 census row, to be named as a kept road under OF4-12/E), 5 (row :127 login carriers names environment.env_file, to be updated with axis 37), new 37 (env-file name leaf and chooser; guard_secrets.py:20-22 is an unlisted consumer), 16 (the table loader through hooklib.read_json), 18/32 (census row for the raising loader), 3 (fingerprint automatic). Unowned temporal switch: access_discovery onto env_probe.env_files after C (no part owns project_inventory.py then). Axes 1, 2, 12, 13 n/a.",
  "trail": {
    "read": [
      "docs/tasks/specs/t-231-env-sources-of1-1-of4-12.md",
      "plans/piles/onboarding-forge/findings/20261112-discovery-nazyvaet-env-a-chitala-env-example.md",
      "plans/piles/onboarding-forge/batch-1-onboarding-roles-forge.md:1-14,67-74",
      ".claude/worktrees/of-batch4/plans/piles/onboarding-forge/batch-4-hvosty-onbordinga-i-forzha.md:1-14,39,50,53",
      "ai-packages/qa-factory/skills/qa-onboarding/phases/p1-discovery.md:40-50,140-160",
      "ai-packages/qa-factory/skills/qa-onboarding/phases/p2-interview.md:130-145",
      "ai-packages/qa-factory/scripts/project_inventory.py:225-240,268-280,395-500,567,588",
      "ai-packages/qa-factory/scripts/env_probe.py:20-45,92,100-145,330-355,440-540,796-808,960-975",
      "ai-packages/qa-factory/scripts/gate_preflight.py:1020-1060,5068-5160",
      "ai-packages/qa-factory/scripts/stand_health.py:428-448",
      "ai-packages/qa-factory/scripts/manual_capture.py:600-650",
      "ai-packages/qa-factory/scripts/source_inventory.py:50-70",
      "ai-packages/qa-factory/scripts/machine_facts.py:340-350",
      "ai-packages/qa-factory/scripts/config_contract.py:1058-1070",
      "ai-packages/qa-factory/scripts/project_decisions.py:632-642",
      "ai-packages/qa-factory/scripts/readiness.py:617-623",
      "ai-packages/qa-factory/scripts/brief_pack.py:2562-2567",
      "ai-packages/qa-factory/scripts/judge_run.py:318-324",
      "ai-packages/qa-factory/scripts/driver_stage_s6.py:1020-1075",
      "ai-packages/qa-factory/scripts/walk_session.py:1265-1282",
      "ai-packages/qa-factory/scripts/guard_secrets.py:15-40",
      "ai-packages/qa-factory/scripts/http_client.py:151-173",
      "ai-packages/qa-factory/references/config-keys.json:2,470-480,620-630,764-772",
      "ai-packages/qa-factory/references/templates/config.json:47-49,107",
      "ai-packages/qa-factory/scripts/tests/test_judgment_census.py:16-40,61",
      "docs/SIBLING_MAP.md axes 5,9,16,32,33,34 and Keeping the map up to date",
      "docs/tasks/specs/reports/t-2046-language-exceptions-census.md (grep)",
      "docs/tasks/critic-diff-brief.md"
    ],
    "reruns": [
      {
        "command": "python -B -c (env_probe.http_address_keys + http_client.safe_url over six sample values)",
        "result": "SLACK_WEBHOOK_URL -> https://hooks.slack.com/services/T0/B0/abcdefSECRET; TELEGRAM_BOT_URL -> https://api.telegram.org/bot123456:AAH-xyz/; SENTRY_DSN -> https://o1.ingest.sentry.io/42; S3_URL -> https://b.s3.amazonaws.com/f; BASE_URL -> http://localhost:3000/api"
      },
      {
        "command": "python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for scripts/project_inventory.py scripts/env_probe.py skills/qa-onboarding/phases/p1-discovery.md design/role-rules.json references/config-keys.json",
        "result": "project_inventory.py: keep test_exploration, test_exploration_identity, test_regression_scope, test_release_fingerprint (no test_manual_capture); env_probe.py: keep test_manual_capture.py among others; role-rules.json: keep test_role_rules.py; config-keys.json: keep test_config_migration.py, test_human_questions.py, test_readiness.py"
      },
      {
        "command": "grep -rln 'Axis 37' docs plans worktree maps + every remote branch SIBLING_MAP",
        "result": "only the t-231 spec itself; no collision"
      }
    ]
  },
  "fixes": [
    "§3 A-6/§5 F-f/§6.6: address = origin only (env_probe.origin) plus has_path, or a stated path policy; adversarial rows webhook path, bot-token path, DSN; correct the SECRET_NAME+safe_url claim",
    "§3 A-6, B-1..B-5, §5 F-f, §1 AR-22: rename stand_addresses to a non-judging data name (e.g. env_file_addresses) and its cap constant",
    "§1 census table, §6.5, A-2: the raising loader is a u3 census unit; its row (shape/data or safety) is a DoD key; the loader reads through hooklib.read_json",
    "§3 A owns/edges: add project_inventory.render_access (:567, :588) with a sample-only wording and a DoD row",
    "§3 D owns (or a late A step after C): access_discovery switches to env_probe.env_files with a test row; §4 queue line",
    "§3 B-1: add p1-discovery.md:44; B owns one p3-summary-gate.md line (env value names its file, sample never as the stand's) or the Lead records n/a for the OF1-1 summary scope",
    "§5 F-b/C-2: relabel later-empty-over-set and add set-process+empty-file as deliberately kept set (dotenv override=False, today's pins); add rows A='' and export A=; scope the error-direction sentence",
    "§3 C-10/§4: axis 37 is a Lead-tier write; C's package commit waits for the full Lead or names the AR-15 deviation",
    "§3 Part E: state process-only expressibility (fork), how-dependent fatality in load_env, consequences for read_login/driver_stage_s6:1063/walk_session:1277 and the delegate name, the source of tests_root; owns add templates/config.json, config-keys.json note_history, environments.md, env_probe docstring; D->E queue line",
    "§1 AR-1/§5 F-d/axis 37: name guard_secrets.py:20-22 as a consumer with its own safe direction (keep or queue)",
    "§5 F-c/axis 37: a consumer table with process flag and safe direction per reader; D-1 refusal names the source file (source_of)",
    "§3 C DoD (3): AR-1 grep for the globs .env* and *.env with a pre-change positive control; A's grep scoped to project_inventory.py",
    "§3 A-5: normalise declared paths (./.env, backslashes) and state the declared-sample case; C-5: a missing listed file among present ones is a named detail line",
    "§1/§7 + axis-37 commit: update SIBLING_MAP axis 5 row :127 to the chooser; add a kept-road row for the Python-only loader scan to the t-2046 census under OF4-12/E"
  ]
}
```
