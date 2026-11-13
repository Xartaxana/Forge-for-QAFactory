# Spec draft — stand login: FV1-17, FV1-5 (parallel), FV1-15 (after both)

Pile `live-run-fvf`, batch 1. Designer draft, 13.11.2026, for Lead acceptance. Forks are in section 6 and are NOT decided
here; every node is executable on the recommended option until the Lead says otherwise.

## 0. Summary

The live run LR2-1 stopped twice on the stand (`runs/factory-14.log:12`): the onboarding recorded the login as
`local_login` at `/login` (a Next.js PAGE), the probe POSTed there, got 405, and the driver told the person "the stand
`local` did not answer" while `/api/health` answered 200. Three defects, one per node:

| Node | Defect | Fix in one line | Files (package-relative) |
|---|---|---|---|
| FV1-17 | onboarding has one way to look for a login and records the first refusal | login answers become a CLOSED set (data); a form-with-csrf login kind as a data row; a "roads" command tries every road and proves a harness login with a negative control; the role records the road that answers `in`, or asks the three answers | `scripts/stand_access.py`, `scripts/config_contract.py`, `references/login-roads.json` (new), `references/templates/config.json`, `references/config-keys.json`, `skills/qa-onboarding/phases/p4-generate.md`, `skills/qa-onboarding/phases/p2-interview.md`, `skills/qa-onboarding/SKILL.md`, `design/role-rules.json` (new rows), census rows, test rows |
| FV1-5 | the driver words EVERY non-zero exit of `env_probe.py` as "did not answer" | the probe names WHY it blocks (closed `blocked_by` words, one reader); the driver's texts say "did not pass its check" and, at the S5/S6 stand check, the real reason | `scripts/env_probe.py`, `scripts/driver_stage_build.py`, `scripts/driver_sources.py`, `scripts/driver_s0.py`, `scripts/driver_machine.py` (one function), `skills/qa-story/phases/s1.md`, `design/role-rules.json` (one row) |
| FV1-15 | a login recorded before the change, wrong door included, has no way out but `go on` | the probe's Layer-1 line and the stand question use the login `answer`; `wrong_door` points at the onboarding login step; old records re-read through one reader | `scripts/env_probe.py`, `scripts/driver_stage_build.py`, `scripts/stand_health.py` (one function), `references/stand-answers.json` |

Parallel: FV1-17 and FV1-5 share NO function; their only shared files are `design/role-rules.json` and
`scripts/tests/fixtures/judgment-census.json` (disjoint rows; the later merge resolves). FV1-15 starts after both are
merged. None of the three touches `scripts/onboarding_probe.py`, `scripts/execution_request.py` or
`scripts/profile_contract.py` — disjoint from FV1-18 (section 1.4).

## 1. Facts (read from the carrier, 13.11.2026, root checkout = origin/main per the brief)

### 1.1 Code

| # | Fact | Carrier |
|---|---|---|
| C1 | `access.kind` is one of five; the tuple is written twice | `scripts/stand_access.py:55` `KINDS`; `scripts/config_contract.py:109` `ACCESS_KINDS` |
| C2 | `stand_access.login()` is the one login act; `env_probe.probe()` calls it | `stand_access.py:478-506`; `env_probe.py:1108-1110` |
| C3 | a login receipt has four statuses `ok/failed/skipped/not_recorded` and two refusal tags (`body_shape`, `timeout`); there is NO word for "this address is not a login endpoint" | `stand_access.py:177-178`, `:224`, `:404`, `:482-485`; `config_contract.py:121-122` `LOGIN_OUTCOMES` |
| C4 | `_login_why` turns ANY non-2xx/non-400/422 code into `failed`, "POST <url> -> HTTP 405" | `stand_access.py:342-360` |
| C5 | `_open` returns `(status, body)` only: no headers, so no cookie and no `Location` can be read by a login | `stand_access.py:127-140`; `http_client.Answer` carries `headers` and `location` (`scripts/http_client.py:139-145`) |
| C6 | the body field pairs are a data row, one reader `config_contract._body_field_rows` | `references/login-body-fields.json:3-4`; `config_contract.py:267-283`, `:309-315` |
| C7 | the probe's Layer 1 has six login/stand line shapes, each with a fixed prefix | `env_probe.py:1125-1144` (`"the stand does not answer: "`, `"the stand has no address: "`, the body-shape fix, `"the login this project records did not finish in time: "`, `"the login this project records was refused: "`, `"<KEY> is not set, and the login needs it"`); fatal at `:1005-1017`; device at `:944-975` |
| C8 | the probe writes the ready `login_probe` object; the role copies it whole | `env_probe.py:906-928` `login_record`; `skills/qa-onboarding/phases/p4-generate.md:284-288` |
| C9 | the onboarding role's whole instruction for a failed login: body_shape -> fix fields; "any other `login: failed` ... is a stand problem: keep the block, write `login.record` whole ... `[DEFERRED: …]`". No step tries another road | `p4-generate.md:303-310` |
| C10 | discovery proposes ONE kind by priority from regex call sites; the `local_login` regex takes any quoted `"/login"` string | `scripts/project_inventory.py:175-190`, `:305-351` |
| C11 | THE FALSE TEXT is the driver's, not the probe's: S0 sets `environment_pending` on ANY exit != 0 and warns "it did not answer the check" | `scripts/driver_s0.py:2390-2403` |
| C12 | S1 says "The stand `<x>` did not answer when I checked it" whenever `environment_pending` | `scripts/driver_sources.py:735-738`; role text `skills/qa-story/phases/s1.md:233`; rule row `design/role-rules.json:332` (anchor "did not answer when I checked") |
| C13 | the S5/S6 stand question says "did not answer when I checked it just now" for any probe exit != 0 | `scripts/driver_stage_build.py:40-41` (text), `:110-124` (`stand_check` runs the probe and passes `out` only as details) |
| C14 | the refusal seam says "The stand did not answer when I looked at it just now" for any probe exit != 0 | `scripts/driver_machine.py:279-287` (`resume_on_refusal`), `:197-201` (`stand_probe`) |
| C15 | the probe's own text reader in the driver: `probe_reason` reads our output shape (the list under `THE ENVIRONMENT CANNOT BE USED`) | `driver_s0.py:2463-2477` |
| C16 | readers of `environment.access.login_probe` today — FOUR, no single reader: `stand_access.recorded_seconds` (only `seconds`), `env_probe._derived_frontend` (only `outcome == ok`), `stand_health._login_receipt` (everything), `config_contract.access_errors` (shape validation) | `stand_access.py:73-80`; `env_probe.py:518-521`; `stand_health.py:683-719`; `config_contract.py:378-402` |
| C17 | `manual_capture` reaches `environment.access` by its own road: only `local_login` is a request it knows; every other kind is `EnvBlocked` "not an HTTP request the factory knows" before anything is sent; `investigation_probe` logs in through it and sends `Authorization: Bearer` | `scripts/manual_capture.py:4959-4986`, `:5006-5013`; `scripts/investigation_probe.py:422-433`; words `references/manual-capture-steps.json:126` |
| C18 | `onboarding_probe.py` holds no login code (profile/report probing only) | its `def` list (`onboarding_probe.py:60-955`); a case-insensitive Grep `login|access` on it returned nothing — positive control of the same tool on the same file: `^def ` matched 30 lines |
| C19 | no package script reads the prose "login by code is not possible" (the old finding) | Grep `by code is not possible|login by code|no login by code` (-i) over the package outside tests: hits are only manual_capture's own `login by code:` lines and texts, none reading a finding |
| C20 | `stand_access.py` has no `keep` row; the login tables (`test_stand_access.py`, `test_login_body_fields.py`, `test_env_access_onboarding.py`) are in `quarantine` | `scripts/tests/test-layers.json:35` (keep starts), `:7067` (quarantine starts), `:7976`, `:8639`, `:9888`; Grep `"stand_access\.py"` in test-layers.json: no hit, while the same Grep found `"env_probe.py"` at `:776` etc. (positive control) |
| C21 | the keep table nearest to "what a host answered": `test_http_client.py` (layer `table`, "HTTP client refusals", has a local stub server) | `test-layers.json:2458-2466`; `scripts/tests/test_http_client.py:18`, `:44-91` |
| C22 | scenario doors are `exit_gate, joint, start, gate, delivery`; none runs `env_probe` or `stand_check` | `scripts/tests/scenario_walk.py:40-47` |

### 1.2 Real-run evidence (premises measured, PROJECT.md acceptance 6a)

| # | Premise | Evidence |
|---|---|---|
| E1 | the onboarding recorded `local_login`, `url: /login`, `login_probe {status 405, outcome failed}` | `C:\QAFactory\mybooks-stand\arm-factory\test-automation-framework\qa-factory\records\config-migrations\24e204cf9a25a6dbe1db555a8119592483113bf191b537a9b276aad4b759e3c2.json:209-228` |
| E2 | the record "login by code impossible" is a FINDING (FB-3), not a decision: `essence "local_login by code is not possible: the stand signs in through NextAuth (csrf form); POST /login answers 405..."`, status `open`, decision `—` | same project `qa-factory\records\project-decisions.json:24-32` |
| E3 | the person was told "the stand `local` did not answer when I checked it just now" | `experiments/mybooks/factory-vs-free-agent/runs/factory-14.log:12` |
| E4 | at that moment `/api/health` -> 200 and the details said `login: failed HTTP 405 — POST /login`; the operator logged in by code via `/api/auth/csrf` -> `/api/auth/callback/credentials` | `experiments/mybooks/factory-vs-free-agent/notebook.md:282-286` (operator's measurement; NOT re-measured by this designer) |
| E5 | the operator's way out: `harness_command` = the project's own login test, exit 0 / exit 1 with a wrong password, `login_probe {outcome ok, seconds 60}`; the probe then said `login: ok` | `notebook.md:287-289`; current config of the arm `qa-factory\config.json:206-226` |
| E6 | the first stop (19:43) was honest: the whole stand was down (503) | `notebook.md:275-277` |
| E7 | NOT FOUND: `config.json.before-harness-login-20261112` named by the findings | Grep with glob `*.json*` over the arm's `qa-factory\` listed `config.json` and `config.json.before-selectors-verified-20261112` (positive control of the glob) and no `before-harness-login` file; E1 (the migration record) carries the pre-fix block instead |
| E8 | NOT READ: `discovery.yaml:76` (the UI login recipe in `global-setup.ts`) — the onboarding state folder was not opened; the claim rests on the finding | — |

### 1.3 What this changes against the findings' wording

- FV1-5's finding says the probe "guessed" `POST /login`. It did not: it used the address the onboarding recorded (E1,
  C2). The probe's own lines were true ("login ... was refused: ... 405"); the FALSE sentence is the driver's (C11-C14).
  So FV1-5 is mostly a driver change; the batch row's "Пишет в: `scripts/env_probe.py`" is incomplete (rows are
  estimates, batch file line 16).
- FV1-15's (в) "do not stop on a refusal already recorded as known and decided": no person decided anything at
  onboarding (E2: FB-3 status open, decision `—`). A login refusal stays Layer 1 unless a PERSON's answer is recorded;
  FV1-17 records that answer as data (kind `ui_only`, F5), and then nothing blocks. See FV1-15 edges.

### 1.4 FV1-18 and other nodes

- FV1-18 writes `execution_request.py`, `profile_contract.py`, `onboarding_probe.py`: none of these nodes touches them (C18).
- FV1-6 owns `driver_machine.py` (S2 door): FV1-5 touches ONLY `DriverMachine.resume_on_refusal` lines 279-287 (one
  sentence) and the `stand_probe` docstring; per PROJECT.md «Командная работа» 3 the function lists are disjoint; the
  later merge resolves. FV1-7/8/16 own `driver_gates.py`: not touched.

## 2. The closed sets

### 2.1 `answer` — what ONE login attempt came to (FV1-17 produces; FV1-5 does not read it; FV1-15 reads it)

| answer | meaning | receipt `status` |
|---|---|---|
| `in` | positively proved session (a token, a proven session, a harness exit 0 whose negative control failed or was not run) | `ok` |
| `credentials_refused` | the endpoint's OWN answer judged the account | `failed` |
| `fields_unconfirmed` | refused, but the body field names were not recorded and the endpoint does not report field errors (row `field_errors_reported: false`): fields OR account, unknown | `failed` |
| `body_shape` | 400/422 asking for fields that were not sent (today's `refusal: body_shape`, unchanged) | `failed` |
| `wrong_door` | the address answered, and the answer shows no login there (page, 404, 405, redirect without a session, JSON without a token; a harness command that also exits 0 with a wrong secret) | `failed` |
| `throttled` | 429 | `failed` |
| `stand_error` | 5xx | `failed` |
| `no_answer` | nothing usable arrived (refused, reset, DNS, TLS, timeout, stalled body) | `failed` |
| `did_not_finish` | harness command over its ceiling (today's `refusal: timeout`) | `failed` |
| `command_failed` | harness command exited non-zero: which of account / harness is unknown | `failed` |
| `command_missing` | harness program not on PATH / not runnable | `failed` |
| `not_tried` | `skipped` or `not_recorded` (nothing was sent) | `skipped` / `not_recorded` |

The four statuses and `LOGIN_OUTCOMES` stay as they are (F2). `answer` is a new key of the receipt and of
`login_probe` (optional; absent = recorded before the field).

### 2.2 Host-answer battery -> `answer` (outside input: the host's answer, CLAUDE.md rule 11)

For `local_login` (POST JSON), `form_login` (submit step) and `oidc_password`; `bearer_env` (GET) in the last column
where it differs. "service" = `http_client` classified the body as the stand's own JSON; "page" = HTML / intermediary /
unclear.

| # | host answer | local_login / oidc | form_login | bearer_env |
|---|---|---|---|---|
| H1 | 200 + token in body | `in` | n/a (session decides) | — |
| H2 | 200, no session: JSON without a token | `wrong_door` | submit JSON whose `url` carries the row's `refused_marker` -> `credentials_refused` (or `fields_unconfirmed`, rule F3); else session check decides (H2s) | `in` (2xx is the proof today) |
| H2s | (form) session path answers JSON with a NON-EMPTY value at `proof_at` | — | `in` | — |
| H2e | (form) session path answers `{}` / empty value / page / non-2xx | — | `wrong_door` unless the submit already said refused | — |
| H3 | 302/303/307 to a login page (no session) | `wrong_door` | `Location` carries `refused_marker` -> `credentials_refused`/`fields_unconfirmed`; else session check (H2s/H2e) | `wrong_door` |
| H4 | 401 service | `credentials_refused` | `credentials_refused` / `fields_unconfirmed` | `credentials_refused` |
| H4p | 401/403 page | `wrong_door` | `wrong_door` | `wrong_door` |
| H5 | 403 service | `credentials_refused` | as H4 | `credentials_refused` |
| H6 | 404 | `wrong_door` | `wrong_door` | `wrong_door` |
| H7 | 405 | `wrong_door` | `wrong_door` | `wrong_door` |
| H8 | 400/422 naming an unsent field | `body_shape` (today) | `wrong_door` (a form endpoint is not walked through pairs) | — |
| H8b | 400/422 naming only sent fields / nothing, service | `credentials_refused` (today's meaning) | `credentials_refused` / `fields_unconfirmed` | — |
| H9 | 429 | `throttled` | `throttled` | `throttled` |
| H10 | 500/502/503/504 | `stand_error` | `stand_error` | `stand_error` |
| H11 | timeout / stalled 2xx body | `no_answer` | `no_answer` | `no_answer` |
| H12 | connection refused | `no_answer` | `no_answer` | `no_answer` |
| H13 | empty 200 body | `wrong_door` | session check decides | `in` |
| H14 | huge body (over `max_body` 262144, cut) | classified on the cut; a cut JSON does not parse -> `wrong_door`, NEVER `in` | same | 2xx -> `in` |
| H15 | non-JSON 200 body | `wrong_door` | session check decides | `in` |
| H16 | any other 4xx (409, 410, ...) | `wrong_door` | `wrong_door` | `wrong_door` |
| H17 | csrf step (form): non-2xx, non-JSON, or no value at `token_at` | — | `wrong_door` (nothing is submitted) | — |

Harness (`harness_command`): exit 0 -> `in`; exit != 0 -> `command_failed`; FileNotFoundError/OSError ->
`command_missing`; over ceiling -> `did_not_finish`. Roads mode only: exit 0 with a wrong secret (negative control)
-> `wrong_door`.

The mapping is a data table `answers` in `references/login-roads.json` (rows matched by `codes` / `from`..`to` /
`kinds` / `not_kinds`, first match wins, a catch-all row last = `wrong_door`), read only by `stand_access`.
INVARIANT of every row: an answer is `in` ONLY on a positive proof (a token value parsed, a non-empty session value, an
exit 0). A row may move an answer between failures; no row may produce `in`. A table that cannot be read classifies
every HTTP answer as `wrong_door` and every exception as `no_answer` (never `in`, never `credentials_refused`).

ERROR DIRECTION of the reused `http_client.classify`/`unattributed` (advice -> part of a recorded answer): it may err
toward `wrong_door` (unknown), never toward `credentials_refused` and never toward `in`. Adversarial inputs that must
stay on the safe side (each a table row): an HTML login page answering 200 that contains the word `token`; JSON
`{"token": ""}`; JSON `{"data": {"token": null}}`; a session path answering `{"user": {}}` or `{"user": ""}`; a session
path answering an HTML page with 200; a 302 whose `Location` is on another host; a 403 WAF page with a JSON-looking
title; a body that echoes the password (redacted in `why`, never printed).

### 2.3 `blocked_by` — why the probe blocks (FV1-5 produces in `env_probe.probe()`; driver reads)

One word per Layer-1 entry, in Layer-1 order: `selection` (environment name missing/ambiguous), `env_file` (env file
not found), `stand_dead` (liveness dead), `no_address` (unchecked under `--env`), `login` (the recorded login did not
get in: refused, body shape, did not finish), `login_key` (a key the login needs is not set), `device` (device stand
not ok). Exit 0 = `[]`. Reader of the TEXT output (what the drivers hold): `env_probe.blocked_by_of(out) -> list`:
`[]` when the text has no `THE ENVIRONMENT CANNOT BE USED` block and no `ENVIRONMENT:` line; `["not_configured"]` for
the `ENVIRONMENT: not configured` line; a Layer-1 item whose prefix matches none -> `"unknown"`; text that is empty or
not the probe's (a crash) -> `["unknown"]`. FR-41: `unknown` is never worded as "did not answer".

## 3. Nodes

### FV1-17 — the onboarding finds a way in by every road (designer -> builder -> critic)

given: this spec; `ai-packages/qa-factory/design/factory-rules.md` whole; `plans/builder-rules.md`; the finding
`plans/piles/live-run-fvf/findings/20261112-onbording-ne-umeet-opredelit-kak-vojti-na-stend.md`; carriers C1-C10,
C16, C17, C20, C21 (file:line above); E1-E5.
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\stand_access.py (whole file)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\config_contract.py (`ACCESS_KINDS`, `access_errors`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\login-roads.json (new)
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\templates\config.json (the `access` object)
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\config-keys.json (rows for the new keys)
C:\QAFactory\forge-repo\ai-packages\qa-factory\skills\qa-onboarding\phases\p4-generate.md (the login-proof section, lines 267-310)
C:\QAFactory\forge-repo\ai-packages\qa-factory\skills\qa-onboarding\phases\p2-interview.md (topic 2, the access-scheme question)
C:\QAFactory\forge-repo\ai-packages\qa-factory\skills\qa-onboarding\SKILL.md (phase-4 table row, line 85)
C:\QAFactory\forge-repo\ai-packages\qa-factory\design\role-rules.json (NEW rows only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json (rows for new/changed functions of stand_access.py and config_contract.py only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_http_client.py (new table rows, per F6)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test-layers.json (the `covers` of `test_http_client.py` only, per F6)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\fv1-17-stand-login-roads.md (new fragment)
non-goals: `env_probe.py` (FV1-5/FV1-15); the driver; `manual_capture.py` / `investigation_probe.py` (F4, node
FV1-17b); `project_inventory.LOGIN_RES` (analog queued, section 5); writing config from code; any quarantined test file.
handoff: builder report per `.claude/agents/builder.md` rule 7 with the witness below, the FR pass (sections A, C, D, F,
G), the AR line, the census rows added.

What to build (each item = behaviour + where):

1. `references/login-roads.json` (new, `schema_version: 1`, `_note` naming its one reader `stand_access.login_roads()`):
   - `forms`: list of rows `{id, seen_in, csrf: {path, token_at: [keys]}, submit: {path, encoding: "form"|"json",
     csrf_field, extra: {name: constant}}, session: {path, proof_at: [keys]}, refused_marker, fields: [user, secret],
     field_errors_reported: false}`. ONE row now: `id: "csrf-credentials-form"`, `seen_in: "NextAuth.js / Auth.js
     credentials provider"`, csrf `/api/auth/csrf` token_at `["csrfToken"]`, submit `/api/auth/callback/credentials`
     encoding `form`, csrf_field `csrfToken`, extra `{"json": "true"}`, session `/api/auth/session` proof_at `["user"]`,
     refused_marker `"error="`, fields `["email", "password"]`. The framework name appears ONLY as the `seen_in` value;
     no code branches on it (AR-1, P2).
   - `answers`: the rows of 2.2 in matcher form (see 2.2 invariant).
   - Reader `stand_access.login_roads() -> {"forms": [...], "answers": [...], "table": "ok"|"unreadable"}` through
     `hooklib.read_json` (the one JSON reader, lazily imported like `_login_error_shapes`, `stand_access.py:237-241`). A
     row missing a required key or of a wrong type is dropped; at most 20 `forms` rows are read (more: ignored, the
     receipt of a roads run says "N rows beyond 20 not read").
2. `stand_access.answer_of(code, text, headers, *, step) -> str`: the ONE classifier (2.2), used by `_login_why`,
   `_oidc_password`, `_bearer_env`, `_form_login`. `_receipt` gains `answer` (required argument; every call site passes
   one). `_harness_command` sets `did_not_finish` / `command_failed` / `command_missing` / `in`. `login()`'s
   `not_recorded`/`skipped` receipts carry `not_tried`. `why` texts: the existing ones stay, and a `wrong_door` why
   ends with "- the address answered, but no login is there (a page, a missing path or a method it does not take)".
3. New kind `form_login` (add to `KINDS`; `config_contract.ACCESS_KINDS` becomes `stand_access.KINDS` — one tuple,
   AR-13). Config keys: `access.form` (row id; empty = the FIRST row — the default, AR-3), `user_key`, `secret_key`,
   `user_field`/`secret_field` (empty = the row's `fields`). `_form_login(access, values, base_url, timeout)`:
   GET csrf -> read value at `token_at` (H17 on failure, nothing submitted) -> POST submit with `csrf_field`, the two
   fields, `extra`, the csrf answer's cookies sent back -> session GET with all cookies -> `answer_of`. Requests go
   through a new `_exchange(url, method, data, headers, timeout) -> http_client.Answer` (redirects not followed,
   `max_body` 262144); `_open` is not changed. ONE attempt only: no pair loop on a form row (lockout invariant below).
   `login_keys` returns `user_key`, `secret_key` for `form_login`. Missing keys -> `skipped`/`not_tried` as for
   `local_login`; unknown `form` id -> `not_recorded` with why naming the known ids.
4. New kind `ui_only` (F5): `login()` returns `skipped`, answer `not_tried`, why "this project signs in through its
   UI only (the person's word at onboarding); there is no login by code to check". `login_keys` -> `[]`.
5. `stand_access.recorded_login(access) -> dict` — THE ONE READER of `environment.access.login_probe` (C16): returns
   `{"recorded": bool, "outcome": word|None, "answer": word|None, "status": int|None, "user_key", "checked_at",
   "seconds": float|None, "user_field", "secret_field"}`; an outcome outside `LOGIN_OUTCOMES` -> None; an answer outside
   2.1 -> None; `seconds` through the existing `recorded_seconds` (kept, now called from here). Callers migrate in
   FV1-15 (`env_probe._derived_frontend`, `stand_health._login_receipt`); `config_contract.access_errors` keeps
   validating the RAW object (a validator judges shape, AR-29 `shape`).
6. Roads: `stand_access.try_roads(full_cfg, root, *, command="", negative=True) -> dict` and a CLI
   `python -B stand_access.py --project-root DIR --roads [--command "<harness command>"] [--no-negative] --json`.
   Builds the candidate roads IN THIS ORDER: (a) the recorded `environment.access` (if a kind is recorded); (b) one
   `form_login` road per `forms` row, with the recorded `user_key`/`secret_key`/fields; (c) `harness_command` with
   `--command` when given (the ROLE composes it from the project's own login test and run template — AR-2; code never
   guesses a command); (d) `local_login` at the recorded `access.url` when (a) was not already it. Each road through
   `login()`; for a harness road whose positive run is `in` and `negative` is on and `secret_key` is named, a second run
   with the secret replaced by `"qa-factory-wrong-" + secrets.token_hex(12)` (never written anywhere): exit != 0 ->
   road stays `in` with `negative: "refused"`; exit 0 -> road becomes `wrong_door` with why "the command passes with a
   wrong secret, so it does not prove a login"; no `secret_key` -> `negative: "not_run"`. Env values come from
   `env_probe.load_env` and the address from `env_probe.selected_probe_config` (imported read-only, no edit). Output:
   `{"roads": [{"road", "access" (names only), "status", "answer", "why", "negative"?, "seconds"?}], "first_in": index|null,
   "tried": n}`; exit 0 always (it is a report, P1); the command writes nothing.
7. Onboarding text (`p4-generate.md`, replacing C9's "any other failed" clause): when the proof login is not `ok`, run
   the roads command (with `--command` when discovery found the project's own login test); write the FIRST road whose
   answer is `in` as `environment.access`, then run `env_probe.py --project-root . --json` again and copy
   `login.record` whole (today's step). No road `in`: write NO conclusion about possibility; ask the person ONE closed
   question with three answers (FR-50): `not needed: the tests sign in through the UI only` (-> `access.kind: ui_only`,
   recorded with `project_decisions.py add` and the person's words); `here is how the project signs in` (their words ->
   the role records the road they name and proves it); `I do not know` (-> keep the recorded block, `login_probe` with
   its `answer`, and a `[DEFERRED: …]` line naming every road tried and its answer). A finding or note saying "login
   by code is impossible" is never written; an earlier one (E2) stays as history and is superseded by the new record.
   `p2-interview.md` topic 2: the access-scheme question lists the roads the command found with their answers.
   `SKILL.md` row 4: one clause "a failed proof login goes through the roads command before any question".
8. Role rules: new rows in `design/role-rules.json` for item 7 (anchors: "run the roads command", "never written",
   "three answers"); no text pin test.

edges:
- LOCKOUT INVARIANT: one wrong password never becomes many — a form road is ONE submit; the body-pair loop runs only
  on `body_shape` (today); the negative control is ONE run with a junk secret and only in roads mode, never in S0/S5
  probes.
- SECRETS: no credential, csrf value, cookie value or token value goes into a receipt, `why`, stdout, a config, a
  report or a fixture; fixtures use `admin@example.invalid` / `not-a-real-secret`-style literals (C20 files' style).
  The negative junk secret is generated per run and never printed.
- LIMITS: a form road = at most 3 requests x `timeout` (8 s from env_probe; the roads CLI uses the same 8 s); a harness
  road = at most 2 runs x `command_timeout` (60..300 s); at most 20 form rows; bodies cut at 262144 (H14 never `in`).
- EMPTY/ABSENT: no `environment.access` -> roads (b)-(d) still run when `user_key`/`secret_key` can be taken from...
  NOT taken: without recorded key NAMES every road is `not_tried` with why "no login key names are recorded"; the role
  records them from discovery first. `forms` empty/unreadable -> no (b) roads, the output says `table: unreadable`.
- TEMPORAL: `login_probe` written before the change has no `answer` -> `recorded_login` returns `answer: None`
  ("predates the field"), never a guessed answer. `form`/`ui_only` absent from a config written before -> the kinds are
  simply not used; `access.form` absent = default row. The template and `config-keys.json` gain the keys in the SAME
  commit (AR-3).
- CONFLICT: recorded `user_field`/`secret_field` vs the row's `fields` -> recorded wins (as `body_field_candidates`).
- CONFLICT: two roads `in` -> the FIRST in the order of item 6 is reported as `first_in`; the role writes that one.

DoD:
- every receipt of `stand_access.login()` carries `answer` from 2.1; H1-H17 and the harness rows map exactly as 2.2,
  each a row of the table named by F6 against a local stub (the NextAuth-shaped stub: `/login` 405 on POST,
  `/api/auth/csrf` JSON + cookie, `/api/auth/callback/credentials` 302 + session cookie on the right fields and 302 to
  `?error=CredentialsSignin` otherwise, `/api/auth/session` with/without `user`) — the roads run on that stub reports
  road (a) `wrong_door` (405) and the form road `in`;
- the adversarial rows of 2.2 stay on the safe side;
- `config_contract.access_errors` accepts `form_login`/`ui_only`, refuses an unknown `form` id naming the ids, accepts
  `login_probe.answer` from 2.1 and refuses another word;
- no line of code names `NextAuth`/`next-auth` (Grep `-i "next-?auth"` over `scripts/` with a positive control on
  `references/login-roads.json`);
- verification: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for scripts/stand_access.py scripts/config_contract.py references/login-roads.json references/templates/config.json references/config-keys.json skills/qa-onboarding/phases/p4-generate.md skills/qa-onboarding/phases/p2-interview.md skills/qa-onboarding/SKILL.md design/role-rules.json`
  and every file it prints, plus `test_judgment_census.py` and `selftest.py --lang`.
siblings: `manual_capture.http_login_source` (C17) — F4/FV1-17b; `project_inventory.LOGIN_RES` (C10) — queued
(section 5); `config_contract.ACCESS_KINDS` duplicate (C1) — fixed in item 3.

AR touched (change check into DoD): AR-1 (new value in a table; Grep `scripts/` for `next-?auth`, `callback/credentials`,
`csrfToken` — must be zero), AR-2 (the role chooses the road and composes the harness command; code reports), AR-3
(template row + config-keys row + read with default + interview topic, one commit; run `test_config_migration.py` when
witness-for prints it), AR-6 (every road tried before a person is asked), AR-13 (one reader of `login_probe`:
`recorded_login`; one kinds tuple), AR-15 (one login act `stand_access.login`), AR-22 (`answer` has producer
`_receipt`/`login_record` and readers `recorded_login`, env_probe in FV1-15), AR-23 (`roads` empty outcome declared:
`tried: 0`), AR-28 (unknown -> `wrong_door`/`not_tried`, never `in`), AR-29 (below).

Checks and owners (AR-29): `answer_of` — owner data, class `shape` (classifies a host answer's code/body form, not a
role's work); `login_roads` row validation — data, `shape`; `access_errors` new branches — data, `shape`; negative
control — data, `shape` (exit code comparison), it never blocks: it changes the road's `answer`; WHICH road is the
project's and whether login by code matters for the story — judgment of the onboarding role, accepted by the person at
the phase-3 summary gate; `ui_only` — intent (the person's word).

### FV1-5 — the probe says why it blocks; the driver stops saying "did not answer" (designer -> builder -> critic)

given: this spec; `design/factory-rules.md` whole; `plans/builder-rules.md`; the finding
`.../findings/20261112-proba-stenda-lozhno-govorit-ne-otvechaet.md`; carriers C7, C11-C15, C22; E3, E4, E6.
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\env_probe.py (`probe`, `main` JSON keys, new `LAYER1` constants, new `blocked_by_of`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\driver_stage_build.py (`stand_question_text`, `stand_check`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\driver_sources.py (`s1_review_text`, lines 735-738)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\driver_s0.py (`s0_rest`, lines 2390-2403)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\driver_machine.py (`resume_on_refusal` lines 279-287, `stand_probe` docstring)
C:\QAFactory\forge-repo\ai-packages\qa-factory\skills\qa-story\phases\s1.md (the sentence at line 233)
C:\QAFactory\forge-repo\ai-packages\qa-factory\design\role-rules.json (row `s1-tells-the-person-the-stand-did-not-answer`, line 332, anchor only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json (rows for `blocked_by_of` only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_human_questions.py (rows, per F6)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\fv1-5-stand-check-words.md (new fragment)
non-goals: `stand_access.py` (FV1-17); the login `answer` (FV1-15); a new `pipeline.json` field; new question options
or price rows; `--json` output shape for existing keys.
handoff: builder report with witness, FR pass (A, B, C, D, E), AR line, census rows.

What to build:
1. `env_probe.py`: module constants `LAYER1 = {"stand_dead": "the stand does not answer: ", "no_address": "the stand
   has no address: ", "login": ("the login this project records was refused: ", "the login this project records did
   not finish in time: ", <LOGIN_FIELD_FIX prefix>), "login_key": " is not set, and the login needs it"}` used BY the
   producer lines of `probe()` (C7) — the words of today's lines do not change; `probe()` returns `blocked_by` (2.3)
   beside `layer1`, same order, and `main --json` prints it (a new key; the four existing keys unchanged; the fatal
   and device returns carry `["selection"]`/`["env_file"]`/`["device"]`).
2. `env_probe.blocked_by_of(out: str) -> list` — the one reader of the probe's TEXT shape for words (2.3), beside the
   producer. `driver_s0.probe_reason` stays the reader of the reason LINE.
3. Driver words (one closed mapping, in `stand_question_text`, new parameter `why: list`):
   `stand_dead` / `no_address` / `device` -> today's sentence ("did not answer when I checked it just now");
   `login` / `login_key` -> "the stand `<x>` answers, but the login recorded for this project did not get in when I
   checked it just now"; `selection` / `env_file` / `not_configured` -> "the stand `<x>` could not be checked: its
   setting in the project's config is missing or broken"; `unknown` or empty -> "I could not check the stand `<x>`".
   The `retry` option's `says`/`what`: `login*` -> "fix the login the project records (the details name what came
   back), or name the way the project signs in; I check again"; others unchanged. `stand_check` passes
   `env_probe.blocked_by_of(out)` (import from the scripts folder as other driver modules do).
4. `driver_s0.s0_rest` warning: "stand <x>: it did not pass the check (<probe_reason>)" (was "did not answer the
   check"); the print line unchanged.
5. `driver_sources.s1_review_text`: "The stand `<x>` did not pass its check at the start; planning goes on, I check it
   again before the tests run; name another stand here if you want one." `s1.md:233` gets the same sentence;
   `role-rules.json:332` anchor becomes "did not pass its check" (rule id unchanged).
6. `driver_machine.resume_on_refusal` line 285: "The stand did not pass its check when I looked at it just now, so
   what the role was stopped by has not changed." (`stand_probe` docstring: "does not answer" -> "does not pass").

edges:
- INVARIANT: no person ever reads "did not answer" unless `blocked_by` contains `stand_dead`, `no_address` or `device`
  — the probe's evidence of a dead stand. A crashed/empty probe is `unknown` -> "I could not check", never "did not
  answer" and never "answers" (FR-41).
- POSITIONAL: `blocked_by` is computed from the same branches that append to `layer1`, appended in the same statement
  order; an exit-0 probe has `blocked_by == []` (what must stay unreachable: a non-empty `blocked_by` with exit 0).
- Several words (stand dead AND a key missing): the FIRST word decides the sentence (Layer-1 order puts the stand
  first).
- EMPTY: `out` empty or None -> `["unknown"]`; `environment` empty -> the existing no-name branches, `why` unused.
- TEMPORAL: stories already holding a warning "did not answer the check" keep it (history; nothing reads it by text —
  `warnings[]` are shown, not parsed); new stories get the new words.
- What is never done: no probe output, key value or URL with userinfo enters the question body (details file only,
  as today).

DoD:
- `stand_question_text` gives the four sentence classes for the `why` words of 2.3, each passing `human_text.problems`
  (rows of the table named by F6), and the battery `out` = probe text with each Layer-1 shape, the not-configured
  line, empty string, a traceback text -> the words of 2.3;
- the E3/E4 shape (liveness alive 200, login failed 405) yields `["login"]` and the "answers, but the login ... did not
  get in" sentence;
- Grep `did not answer when I` over `scripts/` (positive control: the same Grep before the change finds C12-C14) finds
  only the `stand_dead` branch;
- verification: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for scripts/env_probe.py scripts/driver_stage_build.py scripts/driver_sources.py scripts/driver_s0.py scripts/driver_machine.py skills/qa-story/phases/s1.md design/role-rules.json`
  and every file it prints (the role-rules registry test included), plus `test_judgment_census.py`.
siblings: the four driver sites C11-C14 are all in this node; `driver_stage_s6.py:601` uses `environment_pending` without
words (checked: no "did not answer" hit there in the Grep of section 1.1).

AR touched: AR-9 (the refusal names what it expected — the reason class), AR-13 (one reader of the probe's text:
`blocked_by_of`, beside `probe_reason`), AR-16 (texts pass the one question form; no new question), AR-18 (the probe's
output shape gains one key, its reader in the same commit), AR-22 (`blocked_by` producer `probe()`, readers
`stand_check` and `--json` consumers), AR-28 (`unknown` never worded as a verdict).
Checks and owners: `blocked_by_of` — data, `shape` (reads our own output form, FR-14; never a person's words);
whether to retry, go on or name another stand — intent (the person's answer), unchanged.

### FV1-15 — a recorded login has a way out; the probe says "wrong door" (designer -> builder -> critic; after FV1-5 and FV1-17)

given: this spec; `design/factory-rules.md` whole; `plans/builder-rules.md`; the finding
`.../findings/20261112-onbording-zapisal-vhod-kodom-nevozmozhen-oshibochno.md`; FV1-17 and FV1-5 merged
(`stand_access.answer_of`, `recorded_login`, `env_probe.blocked_by_of`); carriers C8, C13, C16; E1, E2, E5.
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\env_probe.py (`probe` login Layer-1 line, `login_record`, `_derived_frontend`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\driver_stage_build.py (`stand_question_text`, `stand_check`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\stand_health.py (`_login_receipt`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\stand-answers.json (`login_remedies`, `texts`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json (rows of the changed functions only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_human_questions.py (rows, per F6)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\fv1-15-recorded-login-way-out.md (new fragment)
non-goals: writing `environment.access` from a story (F7); new question options; `stand_access.py`; onboarding text.
handoff: builder report with witness, FR pass (A, B, D, E), AR line, census rows.

What to build:
1. `env_probe.probe`: the login Layer-1 line by `receipt["answer"]`: `wrong_door` -> "the login this project records
   is not a login endpoint: <why>"; `credentials_refused`/`fields_unconfirmed` -> today's "was refused: <why>";
   `did_not_finish` -> today's; `body_shape` -> today's fix line; `no_answer` -> "the login this project records got no
   answer: <why>"; `stand_error` -> "the stand failed the login with a server error: <why>"; `throttled` -> "the stand
   limits requests; the login was not judged: <why>"; `command_failed`/`command_missing` -> "the project's login
   command did not get in: <why>". All stay `blocked_by: login` (FV1-5's set does not grow; F8). `ui_only` -> `skipped`,
   no Layer 1 (FV1-17 item 4).
2. `env_probe.login_record` copies `answer` into the record. `_derived_frontend` reads `stand_access.recorded_login`
   (`outcome == "ok"`), not the raw dict; `stand_health._login_receipt` reads through `recorded_login` too (its
   sentences unchanged; `answer` shown when present: "(<answer>)").
3. `driver_stage_build`: when `stand_check` gets `blocked_by == ["login"]` and the probe JSON-free text's login line
   is the wrong-door line (read by `blocked_by_of` returning `login` plus a second reader output — implement as
   `env_probe.login_answer_of(out) -> answer|None`, reading the login VERDICT line `login: failed HTTP <code> — ...`
   is NOT enough; read the Layer-1 prefix of item 1 instead, same module, same constants), the `retry` option's
   `what` becomes "run the login step of onboarding again (named below): it now tries every way in", with the existing
   `answer_note=human_text.onboarding_note(...)` door; the question sentence: "the stand `<x>` answers, but the address
   recorded as its login is not a login endpoint".
4. `stand-answers.json`: `login_remedies` gains a first row `{"id": "L0", "codes": [404, 405], "remedy": "The recorded
   login address is not a login endpoint: run the onboarding login step again; it tries every way in."}`.

edges:
- TEMPORAL (the brief's case): a config written before FV1-17 with `local_login`, `url: /login`, `login_probe {405,
  failed}` and no `answer` — the record is NOT what blocks: S0/S5 re-run the recorded login live, it now comes back
  `wrong_door` (FV1-17 H7), the Layer-1 line says "not a login endpoint", the S5 question offers the onboarding step
  (way out, FR-40) or `go on`. The old record is re-read through `recorded_login` as `answer: None`; nothing guesses an
  answer for it. The old finding FB-3 (E2) has no code reader (C19) and stays history; the onboarding re-run writes the
  new access and record (FV1-17 item 7).
- A record `outcome: ok` written before: unchanged everywhere (`_derived_frontend` still takes it).
- INVARIANT (positional, `stand_check`): the onboarding option is offered only when the probe's login line is the
  wrong-door line; a dead stand still gets "did not answer" (FV1-5), a refused account still gets the FV1-5 login
  sentence; nothing here lets a stand pass without exit 0 or a person's word.
- CONFLICT: `access.kind: ui_only` recorded AND a story whose cases need API login: the probe passes (skipped); that the
  story's API cases cannot sign in is the strategist's judgment (P27), not this check's.
- What is never done: the factory does not edit `config.json` from a story; no credential appears in the question.

DoD:
- the E1 config shape against the FV1-17 NextAuth stub: probe exit 1, `blocked_by ["login"]`, Layer-1 "is not a login
  endpoint", the stand question's wrong-door sentence and onboarding option (rows of the F6 table); the E5 shape
  (`harness_command`, ok): exit 0;
- `recorded_login` is the only reader of `login_probe` outside `config_contract.access_errors` (Grep
  `login_probe` over `scripts/` with a positive control);
- verification: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for scripts/env_probe.py scripts/driver_stage_build.py scripts/stand_health.py references/stand-answers.json`
  and every file it prints, plus `test_judgment_census.py`.
siblings: `stand_health._login_remedy` reads `login_remedies` (gets L0 for free); `manual_capture` (F4).

AR touched: AR-13 (one reader `recorded_login` adopted), AR-17/AR-25 (a recorded wrong login has a move: the onboarding
step; `go on` as before; `state-exits.md` row added if the critic finds the state new — none is added by design: no new
recorded state), AR-22 (`answer` read), AR-28. Checks and owners: the wrong-door branch of `stand_check` — data,
`shape` (our own output form); `L0` — data row; whether to re-run onboarding — intent.

## 4. Order and parallelism

```
FV1-17 ──┐
         ├──> FV1-15
FV1-5 ───┘
```

FV1-17 and FV1-5: parallel, two worktrees, disjoint functions; both write NEW rows to `judgment-census.json` and
FV1-5 edits one row of `role-rules.json` while FV1-17 appends rows — the later merge resolves (PROJECT.md «Командная
работа» 3). One critic pass for the topic (R13-g) after FV1-15, or one for 17+5 and a re-review of 15 by diff (Lead).

## 5. Analogs reported, not widened

- `project_inventory.LOGIN_RES` / `KIND_PRIORITY` (`project_inventory.py:175-190`) are closed variety in code (AR-1
  debt) and the `local_login` regex takes any quoted `/login` — the likely source of E1's `url: /login` (inference; the
  discovery file was not read, E8). Queue: a finding in `live-run-fvf` or `factory-rules-debt.md` row.
- `config_contract.ACCESS_KINDS` duplicates `stand_access.KINDS` — closed in FV1-17 item 3.
- `manual_capture` login road (C17) — F4.

## 6. Forks (returned, recommendation first)

- F1 — where the form rows and the answer table live. (A, recommended) new `references/login-roads.json`, one reader
  `stand_access.login_roads()`: `login-body-fields.json`'s note names one reader (`config_contract`) and scopes it to
  body pairs; adding keys gives that file two readers. (B) new keys in `login-body-fields.json` as the finding and the
  brief say. Cost of A: one more data file; of B: AR-13 split readers of one file.
- F2 — `wrong_door` and friends as a key `answer` beside the four statuses (A, recommended: no reader of
  `LOGIN_OUTCOMES`/`outcome` breaks, `failed` stays true: the recorded login did not get in) vs a fifth outcome
  `unknown` (B: changes `config_contract.LOGIN_OUTCOMES`, `stand_health` word mapping, the template comment; truer to
  FR-41 in one word).
- F3 — a refusal from a form endpoint with UNRECORDED field names: (A, recommended) answer `fields_unconfirmed`, one
  attempt, the role records the fields from the project's auth code; (B) try the row's pairs in turn (each a failed
  login against the account: lockout risk); (C) refuse to try without recorded fields (`not_recorded`).
- F4 — P31: `form_login` reached by the probe but not by `manual_capture`/`investigation_probe` (which keep raising
  "not an HTTP request the factory knows", as for `harness_command` today). (A, recommended) node FV1-17b after FV1-17:
  `stand_access.form_session(access, values, base_url, timeout) -> (receipt, cookie_header)` is the one implementation,
  `manual_capture._http_login` sends `Cookie:` instead of `Authorization: Bearer` for it; owns
  `scripts/manual_capture.py` (`http_login_source`, `_http_login`), `scripts/investigation_probe.py` (lines 422-433),
  `references/manual-capture-steps.json` (`login.words`); test rows in `test_manual_capture.py` (keep, C21 area). (B)
  leave it: a residual of P31 — only with the owner's word.
- F5 — how the person's "no login by code, the tests sign in through the UI" is recorded: (A, recommended) new kind
  `ui_only`; (B) `kind: none` (wrong meaning: "the stand needs no login"); (C) a separate flag `access.by_code:
  "declined"`.
- F6 — where the battery rows live (no new test file allowed; `stand_access.py` has no keep row, C20). (A, recommended)
  login-answer rows in `test_http_client.py` (keep `table`, has a stub server), its `covers` extended with
  `stand_access.py` and `references/login-roads.json`; driver-text rows in `test_human_questions.py` (keep `table`,
  covers the driver modules). (B) the Lead registers `stand_access.py` in the table layer with one table file.
- F7 — FV1-15's way out: (A, recommended) the existing onboarding door (person runs the login step; it now tries
  every road), no config write from a story; (B) a `find login` option whose executor runs the roads command and
  writes the found access via a new `project_decisions.py stand-login` command (FR-9 executor; new question option,
  price row, writer of `environment.access` outside onboarding — AR-14 one writer).
- F8 — `blocked_by` granularity: (A, recommended) one `login` word, the answer read separately in FV1-15; (B)
  `login_wrong_door` etc. as words of `blocked_by` (the FV1-5 set would depend on FV1-17 — breaks the parallelism).
- F9 — node shape: FV1-5's real carrier is the driver (1.3), wider than the batch row; (A, recommended) keep it one
  node as specified; (B) split FV1-5a (`env_probe`) / FV1-5b (driver words).

## 7. Small choices closed by the designer

- `config_contract.ACCESS_KINDS = stand_access.KINDS` (module-level import; `stand_access` imports only the standard
  library at load, so no cycle).
- 20 as the cap of form rows read; 8 s per form request (env_probe's `LOGIN_TIMEOUT_S`); junk secret prefix
  `qa-factory-wrong-`.
- Roads CLI lives in `stand_access.py` (so FV1-17 does not touch `env_probe.py` and stays parallel with FV1-5).
- S1's sentence is generic ("did not pass its check"): S1 reads `pipeline.json` only and no new pipeline field is added.
- `_open` keeps its contract; the form road uses a new `_exchange` returning the whole `http_client.Answer`.

## 8. Four questions (for the mechanism commits)

(a) cost: the roads run costs the onboarding up to ~1 min more per harness road (x2 with the negative control) and
seconds per form row; paid once per onboarding. (b) axes: the builder's commit enumerates every SIBLING_MAP axis; known
here: axis 34 (P31 one road — F4), the env-file / frontend axes of `env_probe` (29, 37) untouched; the designer did not
read `docs/SIBLING_MAP.md` (critic walks it). (c) detector: `test_judgment_census.py`, the role-rules registry test, the
F6 table rows; live proof (FR-33) — a `live-runs` row: onboarding of MyBooks records a working login without the
operator. (d) on the path: the onboarding text calls the roads command before any question; the probe runs at S0/S5 by
code.

## 9. Reading trail

Read: batch file `plans/piles/live-run-fvf/batch-1-live-run-fvf.md` (whole); the three findings (whole);
`stand_access.py` (whole); `env_probe.py` (whole, two reads); `references/login-body-fields.json`;
`references/stand-answers.json`; `config_contract.py:110-139, 255-439`; `project_inventory.py:140-540`;
`manual_capture.py:4900-5029`; `investigation_probe.py:405-444`; `stand_health.py:680-719`;
`driver_stage_build.py:10-160`; `driver_sources.py:715-749`; `driver_s0.py:2360-2484`; `driver_machine.py:175-294`;
`p4-generate.md:255-329`; `SKILL.md:78-87`; `scenario_walk.py:1-60, 833-932`; `test-layers.json` (keep head, rows at
740-779, 1415-1444, 1645-1659, 2458-2466, 2925-2952, 4395-4414, 5890-5914, 6025-6044); `docs/TESTING.md`;
`plans/builder-rules.md` 7b; `design/architecture.md:134-158` + change-check lines; real-run files listed in 1.2.
Greps: `did not answer` (package, non-test), `login_probe` (package, non-test), `environment_pending`, `stand_access.`
callers, `by code is not possible|login by code` (-i), `login|access` (-i) on `onboarding_probe.py` (control: `^def `),
`"stand_access\.py"` in test-layers.json (control: `"env_probe.py"`). Not read: `docs/SIBLING_MAP.md`,
`references/question-prices.json`, `references/config-keys.json` rows, `p2-interview.md`, `test_http_client.py` table
body, `test_human_questions.py` body, the onboarding state folder (E8).
