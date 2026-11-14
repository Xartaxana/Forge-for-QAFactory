# Cards redraft — FV1-17a, FV1-17c, FV1-17b, FV1-15 (stand login), after the plan critic t-757

Task t-767. Designer draft, 14.11.2026, for Lead acceptance. Sources: first draft
`docs/tasks/specs/20261113-fv1-17-5-15-stand-login-spec.md` (its §1-§2 facts and closed sets are the base; FV1-5 is built and
not redrafted), plan critic `docs/tasks/specs/reviews/20261114-fv1-17-15-plan-critic.md` (B1-B6, A1-A14, Key 13 — binding),
FV1-28 critic `docs/tasks/specs/reviews/20261114-fv1-28-plan-critic.md` (amendments 9-11: the seam). Lead decisions (final for
this draft): F1-F8 = (A) as amended; Q1 = (b) one "find the way in" answer recorded like `stand-account`/`stand-frontend`;
Q2 = the person's "the tests sign in through the UI only" wins over a later story's recorded code sign-in; the 4-node cut;
a cross-road attempt cap as data. Only NEW forks are returned (§8).

## 0. Completeness table (B1-B6, A1-A14 -> card line)

| Item | Where it lands | Note |
|---|---|---|
| B1 door does not render | FV1-15 items D1-D4 (the `find the way in` answer, Q1(b)) + D5 (`human_text.onboarding_note` third case, used only after a search in this story found nothing) | the door is a token with an executor, not a slash command; the onboarding command appears only as the fallback, in the answer block, with the honest words "run the onboarding again"; no "login only" scope is built (Q1(b) makes it unnecessary) |
| B2 new prefixes not in LAYER1 | FV1-15 item P1 + edge E-P1 (positional invariant) + one test row per prefix | |
| B3 lockout budget | FV1-17a item 7 (`budget` data row + stop rules) + §2.3 | Lead decision 4 |
| B4 refused_marker in raw Location | FV1-17a item 4 step 3 | |
| B5 wrong_door only on evidence; `unjudged` | §2.1, §2.2, FV1-17a items 2-3, FV1-15 P1 wording, FV1-15 P5 (L0 by answer `wrong_door` only) | |
| B6 rows in stand-answers.json | FV1-17a item 2 (`login_answers`, `env_probe.stand_answers`, `_row_takes`, `no_answer_cause`) | |
| A1 `--candidate` | FV1-17a item 6 (d) | at most 5 (data, `budget.candidates`) |
| A2 FR-50 three answers + I do not know | FV1-17c item 2 | |
| A3 token only a non-empty string | FV1-17a item 1 | |
| A4 negative control `passed` | FV1-17a item 6 (negative) | |
| A5 retry text per answer class | FV1-15 item D2 | |
| A6 status 100..599 | FV1-17a items 5, 8 | |
| A7 old plugin reads new config | FV1-17a item 10 (CHANGELOG line) | |
| A8 `_open` wraps `_exchange` | FV1-17a item 1 | |
| A9 secrets tuple, cookie iteration, `_safe` | FV1-17a item 4, item 6 output | |
| A10 role chooses among `in` roads; digest; AR-29 line | FV1-17c item 1; §6 checks table | |
| A11 census only reported units; config-keys three entries | each card's census line; FV1-17a item 9 | |
| A12 form schema scope; unrepresentable way | FV1-17a item 3 (`_note`), FV1-17c item 2 | |
| A13 receipt `source`; option only for source access | FV1-17a item 5 (`login(..., source=)`), FV1-15 E-D2, §5 | |
| A14 p4 `:269` form_login + ui_only; state-exits row | FV1-17c items 3-4 | the `state-exits.md` row is FV1-17c's (text file of the onboarding side) |
| Key 1 stale facts | §1 (re-read on origin/main e4df9c0) | |
| Key 14 axes | §7 enumeration 1-37 | |

## 1. Facts re-read (tree, carriers)

- Tree. `read-main` worktree HEAD = `ba903eb` (`.git/worktrees/read-main/HEAD`), origin/main = `e4df9c0`
  (`.git/refs/remotes/origin/main`): read-main is BEHIND and lacks FV1-5 (1a00352). Every code fact below was read in
  `.claude/worktrees/wave13`, whose reflog ends `0cd3ba4 -> e4df9c0 ... reset: moving to HEAD` (`.git/worktrees/wave13/logs/HEAD:10-11`):
  wave13 = origin/main e4df9c0. Uncommitted edits in wave13 were not ruled out (no git in this session; see §9).
- `env_probe.LAYER1` `:101-106` (login tuple = refused prefix, did-not-finish prefix, `stand_access.LOGIN_FIELD_FIX`);
  `_word_of_item` `:1220-1230` matches `item.startswith(LAYER1["login"])` (a tuple: every member counts) — so B2 is met by
  appending to that tuple. `blocked_by_of` `:1199-1217`. Probe login lines `:1145-1151`; skipped receipts built inside
  `probe()` `:1109-1120`; fatal `:1017-1030`; device `:955-960`; `login_record` `:917-939`; `_derived_frontend` `:516-574`
  (reads `login_probe.outcome` raw at `:530-531`).
- `env_probe.stand_answers` `:257-283` keeps ONLY the list keys `codes, no_answer, order, login_remedies` (`:268`): a new key
  `login_answers` is dropped unless that tuple and `_empty_stand_answers` `:239-241` gain it. `_row_takes` `:291-305`
  (`any` / `outcomes` / `codes` / `from..to` / `kinds` / `not_kinds`); `no_answer_cause` `:320-342`.
- `stand_access.py` (whole, 519 lines): `KINDS` `:55`, `_open` `:127-140` (raises TimeoutError on an unreadable 2xx),
  `token_value` `:152-168` (`str(node.get(name) or "")` — `True` -> "True", `[1]` -> "[1]": A3), `_receipt` `:177-178`,
  `_harness_command` `:191-234`, `_login_why` `:342-360`, `_local_login` `:363-405`, `_oidc_password` `:408-449`,
  `_bearer_env` `:452-475`, `login` `:478-506`, `login_keys` `:509-519`.
- `http_client`: `Headers` is a list of pairs, `get` returns the first (`:112-120`); `Answer.location` = `safe_url(...)`,
  query stripped (`:249-250`, `:151-163`); `classify` rules `:333-421`; `fetch(..., expect=...)` `:196-229`.
- `config_contract`: `ACCESS_KINDS` `:109`, `LOGIN_OUTCOMES` `:122`, `access_errors` `:347-403` (status: any int accepted,
  `:389-391`); callers of `validate`/`environment_errors`: `onboard_apply.py:1854`, `--check-environment` `:3049-3057`, p4
  `:276` — no story-path caller (Grep `(config_contract|CC|C)\.validate\(` over `scripts/*.py`).
- `stand_health._login_receipt` `:683-744`: status 0 (int) -> "contradicts itself" (`:714-717`); `_login_remedy` `:747-753`
  matches `login_remedies` by code/outcome through `_row_takes`.
- `driver_stage_build.stand_question_text` `:31-92` (classes `:42-45`; login retry `:63-67`; key `s6.stand_confirm` `:92`);
  `stand_check` `:94-149` (`why = env_probe.blocked_by_of(out)` `:141`; `answer_note=human_text.onboarding_note(...)` `:147`).
  `human_text.onboarding_note` `:134-139` returns "" for any named stand (B1 confirmed).
- `driver_machine._take_stand_answer` `:3958-3986` (a stand name, then `seam_tokens`, else `unread`);
  `take_seam_answer` `:2348-2399`. `driver_runner.SITE_MOVES` `:1304`; `site_seam_person` `:1306-1315` keeps only
  tokens in `SITE_MOVES`. Driver calls `project_decisions.py` as
  `self.py("project_decisions.py", "--root", str(self.project), ..., "--words-file", str(self.task_root / file))`
  (`driver_dispatch.py:3535`).
- `project_decisions`: `record_stand_account` `:607-675`, `record_stand_frontend` `:768-810`, `_record_stand_fact` `:678-685`
  (ONE CLI wrapper of a stand fact), `_project_config` `:582-595`, `upsert` `:400`, `resolve` `:450-523`
  (`_set_pointer` `:375` sets any JSON value), parser `:881-926`, `main` `:929-956`; no `no_trace` handling in the module
  (Grep `no_trace|def _set_pointer` -> only `_set_pointer`, the positive control of the same call).
- `question-prices.json` `s6.stand_confirm` `:240-244` (stand name / retry / go on); variant keys exist
  (`s0.ticket_read.not_needed_empty` `:9`). `test_conductor_doors.py` `PINNED_ELSEWHERE` `:636-665` + `census_problems`
  `:668-679`: a new raised key needs a pin entry. `test_story_run_s6.py` C16b asserts the `s6.stand_confirm` answers equal
  `["stand name", "retry", "go on"]` — a variant key leaves that pin true.
- p4 `:243-310` (environment block; `:267-270` capture sign-in per kind; `:272-310` login proof; `:303-310` the two failed
  cases). p2 topic 2 `:165-179`. SKILL.md phase table `:78-85`; no arguments `:116-122`.
- `config-keys.json` `environment.access`: `keys` `:219`, `asked_until_answered` `:685`, `knowledge` `:778` (`needed_by` list).
- `design/state-exits.md`: table header `:20`; no row for `access.kind` (FV1-17 critic Grep; not re-run).
- SIBLING_MAP on origin/main: 37 axes (Grep `^## Axis \d+ — ` in `.claude/worktrees/wave13/docs/SIBLING_MAP.md` -> 37 lines,
  last "Axis 37 — A repeat stop"). The FV1-28 critic's "36" read the behind read-main.
- Tests (`scripts/tests/test-layers.json` at e4df9c0; `quarantine` starts `:7169`; `scripts/slow_tests.json`):

| File | Section | Slow? | Use here |
|---|---|---|---|
| `test_http_client.py` `:2516` | keep `table`, covers http_client.py, story_version.py, tests/harness.py | no | login-answer table (F6(A), Lead list decision — §8 F-N3) |
| `test_human_questions.py` `:2525` | keep `table`, covers human_text + every driver module | no | driver-text rows |
| `test_role_rules.py` `:4662` | keep `register` | no | FV1-17c rows |
| `test_state_exits.py` `:5491` | keep `detector` | no | FV1-17c state-exits row |
| `test_judgment_census.py` `:2793` | keep | no | every card |
| `test_conductor_doors.py` `:672` | keep `register` | YES 53.0 s | FV1-15 pin entry; judged by the batch canon |
| `test_story_run_s6.py` `:6136` | keep `gate_named` | YES 218.8 s | not touched (variant key) |
| `test_manual_capture.py` `:3000` | keep `detector` | YES 10.6 s | FV1-17b rows; judged by the batch canon |
| `test_config_migration.py` `:741` | keep | YES 17.7 s | not a local witness |
| `test_stand_access.py`, `test_login_body_fields.py`, `test_env_access_onboarding.py`, `test_stand_health.py` `:10016`, `test_project_decisions_stand_facts.py` `:9205` | quarantine | — | no home, never a witness |

  Slow-file negatives: Grep of `test_http_client|test_human_questions|test_project_decisions_stand_facts|test_state_exits|test_role_rules`
  in `slow_tests.json` -> 0; the same call shape found `test_config_migration.py` and `test_story_run_s6.py` (positive control).

AR-n touched by the four cards (change check in each DoD): AR-1, AR-2, AR-3, AR-6, AR-9, AR-13, AR-14, AR-15, AR-16,
AR-17, AR-18, AR-20, AR-22, AR-23, AR-25, AR-28, AR-29 (§6 lists the owner and census class of every check).

## 2. Closed sets and data

### 2.1 `answer` — what ONE sign-in attempt came to (`stand_access.ANSWERS`, one tuple; `config_contract.LOGIN_ANSWERS = stand_access.ANSWERS`)

| answer | decided by | receipt `status` |
|---|---|---|
| `in` | CODE, positive proof only, BEFORE any table: a non-empty string token (A3); a form session with a non-empty value at `proof_at`; a harness exit 0; a `bearer_env` 2xx (today's proof, unchanged) | `ok` |
| `credentials_refused` | table row (401 service; 400/422 service naming only sent fields) or a form `refused_marker` | `failed` |
| `fields_unconfirmed` | a form refusal while the body fields are not recorded and the row says `field_errors_reported: false` | `failed` |
| `body_shape` | today's rule in code (`ran_out_of_pairs`) | `failed` |
| `wrong_door` | table, positive evidence only: 404, 405, an HTML page on 2xx, a 2xx/3xx without a session from a JSON login road, a csrf step answering 2xx without a token | `failed` |
| `unjudged` | table catch-all (401 empty, 401/403 page, 403 service, any other code), a form session without proof, AND every HTTP answer when the table cannot be read | `failed` |
| `throttled` | table (429) | `failed` |
| `stand_error` | table (5xx) | `failed` |
| `no_answer` | any exception (through `env_probe.no_answer_cause` for the words), a stalled 2xx body | `failed` |
| `did_not_finish` | harness over its ceiling (today's `refusal: timeout`) | `failed` |
| `command_failed` | harness exit != 0 | `failed` |
| `command_missing` | harness program not runnable (FileNotFoundError / OSError) | `failed` |
| `not_tried` | nothing was sent (`skipped`, `not_recorded`, budget stop, `ui_only`) | `skipped` / `not_recorded` |

INVARIANTS: (I1) `in` only from the code's positive proof; no table row can yield `in` (a row whose `answer` is `in` or
outside `ANSWERS` is ignored by the reader). (I2) an unreadable table never turns a proven login into a failure (proof is
checked first) and never yields `credentials_refused` or `wrong_door` (it yields `unjudged`). (I3) an exception is never
`in`. ERROR DIRECTION of the reused `http_client.classify` / `env_probe._row_takes` (now part of a recorded answer that
blocks a story and words a person's sentence): they may err toward `unjudged`, never toward `credentials_refused` (which
sends a person to fix a good password) and never toward `in`. `wrong_door` is reached only on the listed evidence.
The four statuses and `LOGIN_OUTCOMES` do not change (F2 (A)).

### 2.2 `login_answers` rows (new key of `references/stand-answers.json`; reader `env_probe.stand_answers`; matcher `env_probe._row_takes`)

First match wins; `kinds` are `http_client.classify` kinds; `roads` (new key) lists the road kinds a row applies to (absent = all).

| id | match | answer |
|---|---|---|
| LA1 | `codes` [404, 405] | `wrong_door` |
| LA2 | `from` 200 `to` 299, `kinds` [page] | `wrong_door` |
| LA3 | `from` 200 `to` 299, `roads` [local_login, oidc_password] | `wrong_door` |
| LA4 | `from` 300 `to` 399, `roads` [local_login, oidc_password] | `wrong_door` |
| LA5 | `codes` [429] | `throttled` |
| LA6 | `from` 500 `to` 599 | `stand_error` |
| LA7 | `codes` [401], `kinds` [service] | `credentials_refused` |
| LA8 | `codes` [400, 422], `kinds` [service], `roads` [local_login, oidc_password] | `credentials_refused` |
| LA9 | `any` | `unjudged` |

`_note` of the file gains one sentence naming `login_answers` (what it means, `roads`, "a row never yields `in`").

### 2.3 Attempt budget (Lead decision 4; `references/login-roads.json` key `budget`)

`"budget": {"real_secret_failures": 1, "candidates": 5}`. Read by `stand_access.login_roads()`.
- A road SPENDS when it sent the real secret and its answer is one of `credentials_refused, fields_unconfirmed, body_shape,
  unjudged, stand_error, no_answer, did_not_finish, command_failed`. `in`, `wrong_door` (no sign-in endpoint judged it),
  `command_missing`, `not_tried` do not spend.
- Stop rules, checked after every road, in this order: (1) `throttled` -> every later road `not_tried`, why "the stand limits
  requests (HTTP 429); nothing more was sent in this run"; (2) `credentials_refused` -> every later road `not_tried`, why
  "the account was refused at road <n>; another way would only fail the same account - fix the account first (its values in
  the env file)" (regardless of the budget: B3); (3) spent count == `real_secret_failures` -> every later road `not_tried`,
  why "the attempt budget of this run is spent (<k> failed sign-in(s) with the real account)".
- The negative control is a SEPARATE budget of one junk-secret run per roads run (only the first harness road that is `in`).
- Data edges: `real_secret_failures` absent, not an int, a bool, 0 or negative -> 1 (the safe default, FR-59); 1..3 -> as
  given; above 3 (`REAL_SECRET_FAILURES_CEILING = 3`, a code constant — the data may lower the risk, never raise it past the
  ceiling) -> 3 and the output carries `budget_note: "budget.real_secret_failures <v> is above the ceiling 3; 3 is used"`.
  `candidates`: same rule with default 5, ceiling 5; candidates beyond it are not tried and the output says
  "<n> candidate(s) beyond <cap> were not tried".
- INVARIANT: within one roads run at most `real_secret_failures` (<= 3) failed real-secret sign-ins plus one junk-secret run
  reach the account; S0/S5 probes stay one attempt each (unchanged). Across runs nothing is counted (see §8 F-N2).

## 3. Cards

Worktrees: `fv1-17a`, `fv1-17c`, `fv1-17b`, `fv1-15` under `C:\QAFactory\forge-repo\.claude\worktrees\`, each from origin/main
(e4df9c0 or later). Every card's given also carries, whole: `ai-packages/qa-factory/design/factory-rules.md`,
`plans/builder-rules.md`, `docs/TESTING.md`, this file §0-§2 and §5-§7.

---

### FV1-17a — the sign-in answers, the form road, the roads command (code)

given: this file §1-§3 (card FV1-17a), §5, §6, §7; first draft §1.2 (E1-E5 real-run evidence) and §2.2 (host battery H1-H17, as amended by §2.1-§2.2 here); plan critic Keys 5-6, 11-12; `design/factory-rules.md` whole; `plans/builder-rules.md`; `docs/TESTING.md`; carriers named in §1 (file:line)
owns:
C:\QAFactory\forge-repo\.claude\worktrees\fv1-17a\ai-packages\qa-factory\scripts\stand_access.py (whole file)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-17a\ai-packages\qa-factory\scripts\env_probe.py (`_empty_stand_answers`, `stand_answers`, `_row_takes` only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-17a\ai-packages\qa-factory\scripts\config_contract.py (`ACCESS_KINDS`, new `LOGIN_ANSWERS`, `access_errors` only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-17a\ai-packages\qa-factory\references\login-roads.json (new)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-17a\ai-packages\qa-factory\references\stand-answers.json (`_note` sentence, new key `login_answers` only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-17a\ai-packages\qa-factory\references\templates\config.json (the `access` object only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-17a\ai-packages\qa-factory\references\config-keys.json (`environment.access` in `keys`, `asked_until_answered`, `knowledge` only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-17a\ai-packages\qa-factory\scripts\tests\test_http_client.py (one new parameterised table + its stub routes)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-17a\ai-packages\qa-factory\scripts\tests\test-layers.json (the `test_http_client.py` row: `why`, `covers` only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-17a\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json (rows for units the census test reports in the owned functions only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-17a\ai-packages\qa-factory\changelog.d\fv1-17a-stand-login-roads.md (new)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-17a\docs\SIBLING_MAP.md (axis 5 row "How the stand logs in": a DRAFTED line in the report, not an edit — the Lead writes it, rule 9)
non-goals: `env_probe.probe`, `login_record`, `_derived_frontend`, `LAYER1`, `main` (FV1-15); the driver; `stand_health.py` (FV1-15); onboarding text (FV1-17c); `manual_capture.py`, `investigation_probe.py` (FV1-17b); `project_inventory.LOGIN_RES` (queued, first draft §5); writing config from code; any quarantined or slow test file; running CI or mutations.
handoff: builder report per `.claude/agents/builder.md` rule 7: the witness (verbatim output), the FR pass (sections A, C, D, F, G), the `architecture:` and `judgment:` lines, census rows added (or "none reported"), the drafted axis-5 row line, test lines vs product lines (one-line reason if over).
edges: see "edges" below (every item there is part of the DoD)
DoD: the acceptance list below, verification `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for scripts/stand_access.py scripts/env_probe.py scripts/config_contract.py references/login-roads.json references/stand-answers.json references/templates/config.json references/config-keys.json` and every file it prints that is not slow (`scripts/slow_tests.json`) and not quarantined; slow ones named in the report as "judged by the batch canon"; plus `test_judgment_census.py` and `python -B ai-packages/qa-factory/scripts/selftest.py --lang`; no CI, no mutations
siblings: `manual_capture.http_login_source` (FV1-17b); `config_contract.ACCESS_KINDS` duplicate (closed here, item 8); `project_inventory.LOGIN_RES` (queued); `stand_health._login_receipt` and `env_probe._derived_frontend` migrate to `recorded_login` in FV1-15
designer: C:\QAFactory\forge-repo\docs\tasks\specs\20261114-fv1-17-15-cards-redraft-spec.md (this draft, once accepted)

What to build:

1. HTTP seam (A8, A3). New `stand_access._exchange(url, method, data, headers, timeout, expect="any") -> http_client.Answer`:
   `http_client.fetch(..., max_body=262144, expect=expect)`; when `answer.unreadable and 200 <= answer.status < 300` raise
   `TimeoutError("the body of the answer did not arrive")`. `_open` becomes `answer = _exchange(...)`; `return (answer.status,
   answer.body.decode("utf-8", errors="replace"))` — its contract is unchanged. `token_value`: a value counts only when it is a
   `str` whose `.strip()` is non-empty (bools, numbers, lists, dicts, None are skipped); the walk order is unchanged.
2. Classifier (B5, B6). `env_probe`: `_empty_stand_answers` and the list-key tuple in `stand_answers` gain `"login_answers"`;
   `_row_takes(row, code, kind, outcome=None, *, road=None, answer=None)`: FIRST `if "roads" in row and road not in
   row["roads"]: return False`; then `any`; then `outcome in row["outcomes"]` OR `answer is not None and answer in
   row.get("answers", [])` -> True; the rest unchanged (existing callers pass neither keyword: behaviour byte-identical).
   `stand_access.ANSWERS` (the tuple of §2.1). `stand_access.answer_of(code, text, *, road, headers=None) -> str`: lazily
   `import env_probe, http_client`; `kind = http_client.classify(code, headers, text, expect="any" if road == "bearer_env"
   else "json")["kind"]`; `tables = env_probe.stand_answers()`; table not `ok` -> `"unjudged"`; else the first
   `login_answers` row with `_row_takes(row, code, kind, road=road)` whose `answer` is in `ANSWERS` and is not `"in"` ->
   its answer; none -> `"unjudged"`. It never returns `in`, `no_answer`, `body_shape`, `not_tried` or a command word
   (callers decide those). Exceptions: callers set `"no_answer"` and take the words class from
   `env_probe.no_answer_cause(exc)["cause"]` into `why` (e.g. "NO ANSWER (timeout)"), never a second exception classifier.
   Note the double import: run as `python stand_access.py`, `import env_probe` loads a second copy of `stand_access` under its
   own name; both read the same files, so the answers agree (state it in the module docstring; no workaround).
3. Answers in every road. `_receipt(status, why, code=None, user_key="", *, answer)` (keyword required, every call site
   passes one). `_login_why` returns `(status, answer, why)`: error attempt -> `no_answer`; 2xx with token -> `in`; else
   `answer_of(code, text, road=...)`; `ran_out_of_pairs` -> `body_shape` (today). `_oidc_password`, `_bearer_env`: same rule
   (bearer 2xx -> `in`, today). `_harness_command`: exit 0 -> `in`; exit != 0 -> `command_failed`; FileNotFoundError /
   OSError -> `command_missing`; TimeoutExpired -> `did_not_finish`. `login()`'s `not_recorded`/`skipped` receipts ->
   `not_tried`. A `wrong_door` why ends with " - the address answered, but its answer does not look like a sign-in"; an
   `unjudged` why ends with " - its answer does not show whether a sign-in is there". Existing why texts otherwise unchanged.
4. Kind `form_login` (F1 (A) for rows, B4, A9, A12). `KINDS` gains `"form_login"` and `"ui_only"`. Config keys of a
   `form_login` access: `form` (a row id; empty/absent = the FIRST valid row, AR-3), `url` (optional base address or key NAME,
   through `resolve_url`; empty = the stand's `base_url`), `user_key`, `secret_key`, `user_field`, `secret_field` (empty = the
   row's `fields`; recorded wins, as `body_field_candidates`). `_form_login(access, values, base_url, timeout)`:
   step 1 GET `<base><row.csrf.path>` through `_exchange(expect="json")`; exception -> `no_answer`; non-2xx -> `answer_of(...,
   road="form_login")`; 2xx without a non-empty string at `token_at` -> `wrong_door` ("the sign-in form's first step answered
   without the token it hands out"); nothing is submitted in any of these. Step 2 cookie jar: iterate `answer.headers` pairs,
   every pair whose name lower-cased is `set-cookie` contributes `name=value` (text before the first `;`, split at the first
   `=`; later names overwrite earlier); never `Headers.get`. Step 3 POST `<base><row.submit.path>`: body = `{csrf_field:
   token, user_field: user, secret_field: secret, **row.submit.extra}` urlencoded (`encoding: form`) or JSON (`json`);
   headers Content-Type, `Accept: application/json`, `Cookie: n1=v1; n2=v2`. The `refused_marker` is looked for in the RAW
   `answer.headers.get("Location")` (B4; never `Answer.location`, whose query is stripped) and in a 2xx JSON body's `url`
   string; found -> `credentials_refused`, or `fields_unconfirmed` when the fields are not recorded in `access` and the row's
   `field_errors_reported` is false. The raw Location is never printed or stored. Submit exception -> `no_answer`; a submit
   code outside 2xx/3xx -> `answer_of(..., road="form_login")`. Step 4 GET `<base><row.session.path>` with every cookie: 2xx
   and the value at `proof_at` is a non-empty dict or non-empty string -> `in`; otherwise -> `answer_of(code, text,
   road="form_login", headers=answer.headers)` (a page -> `wrong_door`, `{}` / `{"user": {}}` / `{"user": ""}` -> LA9
   `unjudged`). At most 3 requests per form road; ONE submit, never a pair loop (lockout). SECRETS (A9): every
   `_who_answered`/why of a form road redacts `(user, secret, csrf token, every cookie value)`; urls only through `_safe`.
   `login_keys` of `form_login` -> `user_key`, `secret_key`; missing values -> `skipped`/`not_tried` as `local_login`;
   unknown `form` id -> `not_recorded`, why naming the known ids; no valid row -> `not_recorded`, why "no sign-in form is known
   (references/login-roads.json has no valid row)".
5. Kind `ui_only`, the one reader, the source (F5 (A), A6, A13, Q2). `login()` on `ui_only` -> `skipped`, `not_tried`, why
   "this project signs in through its UI only (the person's word at onboarding); there is no sign-in by code to check";
   `login_keys` -> `[]`. New `stand_access.code_login_declined(access) -> bool` (True iff kind == `ui_only`): the ONE reader of
   the person's word for FV1-28 D1 (Q2). `login(access, values, base_url="", timeout=8.0, health_url="", cwd=None, *,
   source="access")` sets `receipt["source"] = source` on EVERY receipt it returns (FV1-28 D1 passes `"registry"`).
   `stand_access.valid_status(value) -> int | None`: an int (not bool) in 100..599, else None. `stand_access.recorded_login(access)
   -> dict` — THE reader of `environment.access.login_probe`: `{"recorded": bool (a dict with a non-empty user_key), "user_key",
   "outcome": word in LOGIN_OUTCOMES else None, "answer": word in ANSWERS else None, "status": valid_status(...), "checked_at",
   "seconds": recorded_seconds(...), "user_field", "secret_field"}` (strings stripped, non-strings -> ""); never raises.
6. Roads: `stand_access.try_roads(full_cfg, root, *, env_name="", command="", candidates=(), user_key="", secret_key="",
   negative=True) -> dict` and the CLI `python -B stand_access.py --project-root DIR --roads [--env NAME] [--command "<cmd>"]
   [--candidate <kind>=<url>]... [--user-key NAME --secret-key NAME] [--no-negative] --json`. Each road runs the PROBE'S way
   (one road for one action, P31): a deep copy of `full_cfg` whose `environment.access` is the road's access, through
   `env_probe.probe(copy, env_name, root=root)`, and the road's receipt is `result["login"]` (a dead stand gives `not_tried`
   for every road, as the probe skips the login). Roads IN THIS ORDER: (a) the recorded access, when its kind is recorded and
   is not `none`/`ui_only`; (b) one `form_login` road per valid `forms` row (skipped when (a) is that row); (c)
   `harness_command` with `--command`, when given (the ROLE composes it, AR-2; code never guesses), skipped when equal to (a);
   (d) each `--candidate`, in the given order, kinds `local_login` / `oidc_password` only (another kind -> CLI refusal "a
   candidate is <local_login|oidc_password>=<url or path>", exit 2, nothing sent), skipped when equal to (a); at most
   `budget.candidates`. Key names for (b)-(d): the recorded access's `user_key`/`secret_key`, else `--user-key`/`--secret-key`;
   none -> that road `not_tried`, why "no sign-in key names are recorded or given". Budget and stops: §2.3, applied between
   roads. Negative control (A4): for the FIRST harness road whose answer is `in`, when `negative` and its `secret_key` is named:
   `stand_access.login(access, values_with_junk, "", timeout, "", root)` where `values` come from
   `env_probe.load_env(env_probe.selected_probe_config(full_cfg, env_name)[0], root)[0]` and the secret is replaced by
   `"qa-factory-wrong-" + secrets.token_hex(12)` (never printed or written). Exit != 0 -> `negative: "refused"`; exit 0 ->
   `negative: "passed"` and why gains " - it passes with a wrong secret too (or reads the secret from elsewhere), so it may not
   prove a sign-in: judge it"; the answer STAYS `in`; no secret_key -> `negative: "not_run"`. Output (JSON, exit 0 always: a
   report, P1; it writes nothing): `{"roads": [{"road": "a|b:<row id>|c|d:<n>", "kind", "access" (names and `_safe` urls
   only), "status", "answer", "why", "negative"?, "record"? (the probe's `login.record`)}], "first_in": index|null, "tried": n,
   "spent": k, "budget": {...}, "budget_note"?, "table": "ok|unreadable"}`.
7. `references/login-roads.json` (new): `schema_version: 1`; `_note` naming its one reader `stand_access.login_roads()` and
   the SCOPE (A12): "a row describes a sign-in form whose csrf step answers JSON and whose session step answers JSON; a form of
   another shape (a csrf token in a cookie, no session endpoint, a cookie-session JSON sign-in) is a finding and a schema
   change, never a code branch"; `budget` (§2.3); `forms`: rows `{id, seen_in, csrf: {path, token_at: [keys]}, submit: {path,
   encoding: "form"|"json", csrf_field, extra: {name: string}}, session: {path, proof_at: [keys]}, refused_marker, fields:
   [user, secret], field_errors_reported: bool}`. ONE row: `csrf-credentials-form`, `seen_in` "NextAuth.js / Auth.js
   credentials provider", `/api/auth/csrf` `["csrfToken"]`, `/api/auth/callback/credentials` `form` `csrfToken` extra
   `{"json": "true"}`, `/api/auth/session` `["user"]`, marker `"error="`, fields `["email", "password"]`,
   `field_errors_reported: false`. Reader `login_roads() -> {"forms": [...], "budget": {...}, "table": "ok"|"unreadable"}`
   through `hooklib.read_json` (lazy import, as `_login_error_shapes`); a row with a missing key, a wrong type, a path not
   matching `config_contract.API_PATH_RE` is dropped; at most 20 rows (more: ignored, `forms_note` says how many).
8. `config_contract` (one tuple, AR-13; A6): `ACCESS_KINDS = stand_access.KINDS` (module-level import: `stand_access` loads
   stdlib only); `LOGIN_ANSWERS = stand_access.ANSWERS`. `access_errors`: `form_login` needs nothing more than the keys
   (`form` unknown -> "environment.access.form must be one of <ids>"); `ui_only` needs nothing; `login_probe.answer` present
   and not in `LOGIN_ANSWERS` -> error naming the words; `login_probe.status` present, not None, and `valid_status(...)` None ->
   "environment.access.login_probe.status must be an HTTP code (100..599); leave it out (null) for a sign-in command, which
   has none" (the same test as `recorded_login`, A6).
9. Template and catalogue (AR-3, A11): `templates/config.json` `access` keeps `kind: ""` and gains `"form": ""`; the template
   comment lists the seven kinds. `config-keys.json`: `keys["environment.access"]` description names `form_login` / `ui_only`
   and `form`; `asked_until_answered["environment.access"].question` lists "a sign-in form" and "only through the UI" among
   the schemes in plain words; `knowledge["environment.access"].needed_by` gains `stand_access.py:recorded_login`,
   `stand_access.py:try_roads`, `project_decisions.py:record_stand_login`.
10. CHANGELOG fragment (A7): includes "A config written by this version (`form_login`, `ui_only`, `login_probe.answer`) is
    refused by `--check-environment` of an older installed plugin: install this version on every machine that runs the
    project's factory."
11. Tests (F6 (A) as the Lead's list decision, §8 F-N3): the `test_http_client.py` row's `why` becomes "table (B.2 criterion
    5): HTTP client refusals and the sign-in answers built on them"; `covers` gains `stand_access.py`,
    `references/login-roads.json`, `references/stand-answers.json`. ONE parameterised table `SIGN_IN_ROWS` against the file's
    local stub (routes: `/login` 405 on POST; `/api/auth/csrf` JSON + two `Set-Cookie` lines; `/api/auth/callback/credentials`
    302 + session cookie on the right fields, 302 to `/api/auth/signin?error=CredentialsSignin` otherwise;
    `/api/auth/session` `{"user": {...}}` with the cookie, `{}` without). Ids name the case. Rows (input from outside = the
    host's answer and the project config: magnitude, nesting, encoding, empty):
    `H-404-local`, `H-405-local` (wrong_door), `H-200-html-token-word` (wrong_door), `H-200-json-no-token` (wrong_door),
    `H-200-empty` (wrong_door), `H-302-local` (wrong_door), `H-401-empty` (unjudged), `H-401-detail-json` (credentials_refused),
    `H-403-csrf-json` (unjudged), `H-403-html` (unjudged), `H-400-sent-fields-service` (credentials_refused), `H-400-unsent-field`
    (body_shape after the pairs), `H-429` (throttled), `H-503` (stand_error), `H-timeout` and `H-refused` (no_answer),
    `H-stalled-2xx` (no_answer), `adv-token-true`, `adv-token-list`, `adv-token-empty`, `adv-token-null` (none `in`),
    `body-at-262144` (token parses -> in), `body-beyond-262144` (cut -> never in), `form-csrf-ok-in`, `form-wrong-password`
    (marker in the RAW query -> credentials_refused), `form-unrecorded-fields-refused` (fields_unconfirmed), `form-csrf-404`
    (wrong_door, nothing submitted), `form-csrf-no-token` (wrong_door), `form-session-empty` (unjudged), `form-session-html`
    (wrong_door), `form-location-other-host` (decided by the session, url never printed), `form-two-set-cookie` (both sent back),
    `secret-echo` (the password, csrf and cookie values absent from `why`), `table-unreadable` (HTTP -> unjudged, exception ->
    no_answer, token -> in), `roads-e1-shape` (recorded `local_login /login` -> road (a) wrong_door, road (b) in, first_in = b),
    `budget-refused-stops`, `budget-unjudged-spends-1`, `budget-throttled-stops`, `budget-value-absent`/`0`/`"x"`/`3`/`4`
    (-> 1/1/1/3/3 + note), `candidates-5-at`, `candidates-6-beyond`, `candidate-bad-kind` (exit 2), `negative-refused`,
    `negative-passed` (answer stays in), `no-key-names` (not_tried), `ui-only` (skipped, not_tried), `source-registry`,
    `recorded-login-e5-status-0` (status None), and contract joins: `record-answer-validates`, `form-unknown-id-refused`,
    `answer-word-refused`, `status-0-refused`. No row for an internal boundary.

edges:
- E1 LOCKOUT: one submit per road; the pair loop only on `body_shape` (today); budget §2.3; the junk-secret run once per roads
  run and never in an S0/S5 probe. INVARIANT: at most 3 failed real-secret sign-ins + 1 junk run per roads run.
- E2 SECRETS: no credential, csrf value, cookie value, token value or raw Location in a receipt, why, stdout, config, report or
  fixture; fixtures use `admin@example.invalid` / `not-a-real-secret`. INVARIANT: the redaction tuple of a form road holds all
  four kinds of value.
- E3 LIMITS: body cut at 262144 (AT parses, BEYOND never `in`); form road <= 3 requests x 8 s; harness <= 2 runs x its ceiling
  (60..300 s); rows <= 20; candidates <= 5; budget <= 3.
- E4 EMPTY/ABSENT: no `environment.access` -> road (a) absent, (b)-(d) need key names (else `not_tried`); `forms` empty or
  file unreadable -> no (b) roads, `table: "unreadable"`; `login_answers` absent or `stand-answers.json` unreadable -> every HTTP
  non-proof answer `unjudged` (I2); `--command ""` = no (c); a `login_probe` that is not a dict -> `recorded: false`.
- E5 TEMPORAL: (world before) configs without `form`/`answer`/`ui_only` read as today (`recorded_login.answer` None:
  "predates the field", never guessed); (world after) `login-roads.json` and `login_answers` exist from this commit; the
  template and the catalogue gain the keys in the same commit (AR-3). An older plugin refuses the new kinds (A7: release note).
- E6 CONFLICT: recorded fields vs the row's `fields` -> recorded wins; two roads `in` -> `first_in` is the first in road order,
  a HINT; the role chooses (FV1-17c, A10); table says X vs code proof -> code proof wins (I2).
- E7 POSITIONAL: in `answer_of`, the positive-proof checks happen in the CALLER before `answer_of` is called (what stays
  unreachable: a table row producing `in`); in `_row_takes` the `roads` filter comes FIRST (what stays unreachable: a road-scoped
  row taking another road's answer via `any`/`outcomes`).
- E8 awkward host answers: 3xx to a sign-in page (local/oidc -> wrong_door; form -> marker/session; bearer -> unjudged), 403
  (unjudged), 405 (wrong_door), 200 with an error body (local/oidc: no token -> wrong_door; form: session decides), csrf two-step
  (item 4), no response (no_answer).

Census / owners: `answer_of` + `login_answers` — data, `shape`; `login_roads` row validation — data, `shape`; `access_errors`
new branches — data, `shape`; budget stops — data, `safety` (they refuse to send); form-road redaction — data, `safety`;
negative control — data, `shape` (evidence only, never a refusal). Census rows only for the units `test_judgment_census.py`
reports in the owned functions; none expected for `answer_of`/`try_roads` (they raise nothing) — a builder never invents rows.
architecture: AR-1 (form row, answers, budget are data; Grep `-i "next-?auth|callback/credentials|csrfToken"` over
`scripts/*.py` = 0, positive control on `references/login-roads.json`), AR-6, AR-13 (one kinds tuple, one answers tuple, one
`login_probe` reader, one status test), AR-15/AR-18 (one matcher `_row_takes`, one exception classifier), AR-22 (`answer`,
`source` produced; readers FV1-15, FV1-28 D1), AR-23 (`tried: 0`, `first_in: null` declared), AR-28 (I1-I3), AR-29 (above),
AR-3 (template + catalogue same commit).
judgment: the road choice and whether code sign-in matters stay with the onboarding role and the person; code reports answers.

---

### FV1-17c — the onboarding runs the roads before any question (text)

given: this file §2, §3 (cards FV1-17a item 6 = the frozen CLI contract, FV1-17c), §6, §7; `design/factory-rules.md` whole (FR-6, FR-50); `plans/builder-rules.md`; `references/human-questions.md`; carriers p4 `:243-310`, p2 `:165-179`, SKILL.md `:78-85`, `design/state-exits.md:20`
owns:
C:\QAFactory\forge-repo\.claude\worktrees\fv1-17c\ai-packages\qa-factory\skills\qa-onboarding\phases\p4-generate.md (lines 243-310 only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-17c\ai-packages\qa-factory\skills\qa-onboarding\phases\p2-interview.md (topic 2, lines 165-179 only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-17c\ai-packages\qa-factory\skills\qa-onboarding\SKILL.md (phase-4 row, line 85 only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-17c\ai-packages\qa-factory\design\role-rules.json (new rows only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-17c\ai-packages\qa-factory\design\state-exits.md (one new row)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-17c\ai-packages\qa-factory\changelog.d\fv1-17c-onboarding-roads.md (new)
non-goals: any `.py`; `references/*`; p0 (no "login only" scope: Q1(b)); a text pin test; CI, mutations.
handoff: builder report: witness, FR pass (A, B, C, E, G), `architecture:` / `judgment:` lines.
edges: see "edges" below
DoD: role-rules rows carry the anchors below and the registry test passes; the state-exits row exists; verification `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for skills/qa-onboarding/phases/p4-generate.md skills/qa-onboarding/phases/p2-interview.md skills/qa-onboarding/SKILL.md design/role-rules.json design/state-exits.md` and every non-slow, non-quarantined file it prints (expected among them `test_role_rules.py`, `test_state_exits.py`); plus `python -B ai-packages/qa-factory/scripts/selftest.py --lang`; no CI, no mutations
siblings: the p4 `:269` capture branch (item 3); `manual_capture` (FV1-17b)
designer: C:\QAFactory\forge-repo\docs\tasks\specs\20261114-fv1-17-15-cards-redraft-spec.md (this draft, once accepted)

What to build:
1. p4, replacing case (b) of `:306-310` (case (a) body_shape stays): when the proof login's `login.status` is not `ok` (and
   liveness is not dead), run `python "${CLAUDE_PLUGIN_ROOT}/scripts/stand_access.py" --project-root . --roads --json`, adding
   `--command "<line>"` when discovery found the project's own sign-in test (you compose it from that test and the run
   template), one `--candidate <kind>=<url>` per other login site discovery listed (`evidence` / `other_evidence`, at most 5),
   and `--user-key`/`--secret-key` when the block records no key names. Read every road. `first_in` is a hint: YOU choose among
   the roads whose `answer` is `in` (A10) — prefer the project's own command; a road with `negative: "passed"` proves nothing
   alone; choosing a road that is not `harness_command` means the stand's own address is no longer taken as its UI (say so).
   Write the chosen road's `access` as `environment.access`, run `config_contract.py --check-environment` and `env_probe.py
   --project-root . --json` again, copy `login.record` whole (today's step). In the phase-4 digest list EVERY road tried with
   its answer and, when you replaced the approved access, that you did (A10). Run the roads command at most twice per
   onboarding; after a `credentials_refused` do not run it again — ask (the account is wrong, another run only fails it again).
2. No road `in`: never write that sign-in by code is impossible, in a finding, a note or a decision. Ask the person ONE closed
   question, written by `references/human-questions.md` (FR-6; plain words, the unknown said as unknown — e.g. "I tried <n>
   ways to sign in to the stand by code; none of them signed in, and for <m> of them the answer did not show whether a sign-in
   is there"), with four answers (FR-50 + A2): `not needed: the tests sign in through the UI only` -> `access.kind: "ui_only"`,
   recorded with `project_decisions.py --root . add` and the person's words; `here is how to get it` -> the way they name:
   record it as a kind and prove it with the roads command; a way no kind represents (a cookie-session JSON sign-in, a csrf
   token in a cookie) -> record it as a `harness_command` you compose from their words, or a `[DEFERRED: …]` naming the way
   (A12); `here it is as text` -> they paste the sign-in request or command (never a secret value; if a value is in it, do not
   repeat it, ask for the variable NAME): record and prove as above; `I do not know` -> keep the block, write `login.record`
   whole, and a `[DEFERRED: …]` line naming every road tried and its answer.
3. p4 `:267-270` (A14): `form_login` -> the capture refuses until FV1-17b lands: ask the existing question "Does the
   application sign in by a request that returns a token? ..." exactly as for `harness_command`; `ui_only` -> write nothing:
   screens sign in through `fill-account` (say so to the person).
4. `design/state-exits.md`, one row in the story's-state section style: state `environment.access.kind = ui_only` (the
   person's word at onboarding that the tests sign in through the UI only); entered by the onboarding (`p4`, item 2) with
   `project_decisions.py add`; way out: run the onboarding again and answer topic 2 differently, or record another access
   (`project_decisions.py stand-login`, FV1-15) — the probe then checks a sign-in by code again; proven by
   `test_http_client.py` (`ui-only` row). If `test_state_exits.py` enumerates states only from code sources and this row has
   no source, it still passes (a row for a config value); if it fails, stop and report (do not change the test).
5. p2 topic 2 `:165-179`: the scheme list names seven kinds in plain words ("a sign-in form" for `form_login`, "only through the
   UI" for `ui_only`); one sentence: "a failed proof sign-in goes through the roads command in phase 4 before any question".
6. SKILL.md row 4: one clause "a failed proof sign-in runs every road (`stand_access.py --roads`) before any question".
7. `design/role-rules.json` new rows (anchors exact strings in p4): `p4-roads-before-asking` ("run every road before you
   ask"), `p4-never-writes-impossible` ("never write that sign-in by code is impossible"), `p4-four-answers` ("four
   answers"), `p4-role-chooses-road` ("first_in is a hint"). Sources `FV1-17c; (test_role_rules)`.

edges:
- E1 ORDER: roads before the question; the question only when no road is `in`. INVARIANT: no onboarding writes "impossible".
- E2 LOCKOUT: at most two roads runs per onboarding, none after `credentials_refused`.
- E3 EMPTY: no login sites found -> only (a)/(b) roads; no key names anywhere -> the question asks for the NAMES first.
- E4 TEMPORAL: an earlier finding "login by code is impossible" (E2 of the first draft) stays history; the new record
  supersedes it; nothing reads it (first draft C19).
- E5 CONFLICT: two `in` roads -> the role chooses and says why; a person's `ui_only` vs a working road -> the person's word
  wins (Q2) and the road is reported.
Census: none (no code). judgment: road choice = the onboarding role's judgment, shown to the person in the phase-4 digest
(A10; the phase-3 gate is BEFORE the roads run); `ui_only` = intent. architecture: AR-2, AR-6, AR-16, AR-25, AR-29.

---

### FV1-17b — the manual capture signs in through the form road (after FV1-17a)

given: this file §2, §3 (FV1-17a items 4-5, FV1-17b); first draft F4 (A); `design/factory-rules.md` whole; `plans/builder-rules.md`; carriers `manual_capture.py:4959-4986`, `:5006-5013`, `investigation_probe.py:422-433`, `references/manual-capture-steps.json:126` (first-draft line numbers, re-read on the branch)
owns:
C:\QAFactory\forge-repo\.claude\worktrees\fv1-17b\ai-packages\qa-factory\scripts\stand_access.py (new `form_session` only, extracted from `_form_login`)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-17b\ai-packages\qa-factory\scripts\manual_capture.py (`http_login_source`, `_http_login` only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-17b\ai-packages\qa-factory\scripts\investigation_probe.py (the login block at lines 422-433 only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-17b\ai-packages\qa-factory\references\manual-capture-steps.json (`login.words` only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-17b\ai-packages\qa-factory\scripts\tests\test_http_client.py (`SIGN_IN_ROWS` new rows only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-17b\ai-packages\qa-factory\scripts\tests\test_manual_capture.py (new rows only; slow, judged by the batch canon)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-17b\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json (reported units only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-17b\ai-packages\qa-factory\changelog.d\fv1-17b-capture-form-login.md (new)
non-goals: `manual_capture.login_recipe` (FV1-28e); other kinds' capture behaviour; p4 text (FV1-17c already routes `form_login` through the existing question until this lands — after it lands that branch is a follow-up row, §8 F-N4); CI, mutations.
handoff: builder report: witness, FR pass (A, C, D, G), `architecture:` / `judgment:`, census.
edges: see "edges" below
DoD: `form_session(access, values, base_url, timeout) -> (receipt, cookie_header | None)` is the one implementation (`_form_login` returns its receipt); `manual_capture._http_login` sends `Cookie: <cookie_header>` (never `Authorization: Bearer`) for `form_login`; `investigation_probe` signs in the same way; verification `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for scripts/stand_access.py scripts/manual_capture.py scripts/investigation_probe.py references/manual-capture-steps.json` and every non-slow, non-quarantined file it prints; `test_manual_capture.py` named "judged by the batch canon"; no CI, no mutations
siblings: `manual_capture.http_login_source` kinds list; `investigation_probe` (same class, same node)
designer: C:\QAFactory\forge-repo\docs\tasks\specs\20261114-fv1-17-15-cards-redraft-spec.md (this draft, once accepted)

edges: E1 the cookie header is a secret: never printed, logged, stored or put in evidence (redact like a token); INVARIANT: no
evidence file holds a cookie value. E2 `form_session` with a non-`in` receipt returns `None` and the capture refuses with the
receipt's why, nothing else sent. E3 one submit (FV1-17a E1). Rows: `capture-form-in` (Cookie sent), `capture-form-refused`
(nothing sent after), `capture-cookie-redacted` (test_http_client rows for `form_session`; manual_capture rows in the slow file).
Census: `form_session` — data, `shape`/`safety` as reported. architecture: AR-13, AR-15, AR-34-class one road (axis 34),
AR-28. judgment: none moved.

---

### FV1-15 — the probe words the answer; a recorded sign-in has a way out (after FV1-17a; parallel with FV1-17c/17b)

given: this file §1-§3 (FV1-17a items 2-6 as merged, FV1-15), §5, §6, §7; plan critic Keys 7-8, 10; FV1-28 critic amendments 9-11; first draft E1, E2, E5; `design/factory-rules.md` whole; `plans/builder-rules.md`; `references/human-questions.md`; carriers named in §1
owns:
C:\QAFactory\forge-repo\.claude\worktrees\fv1-15\ai-packages\qa-factory\scripts\env_probe.py (`LAYER1`, new `LOGIN_PREFIX_ANSWER`, new `login_answer_of`, `probe` login lines and the receipts it builds itself, `login_record`, `_derived_frontend` only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-15\ai-packages\qa-factory\scripts\stand_health.py (`_login_receipt`, `_login_remedy` only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-15\ai-packages\qa-factory\references\stand-answers.json (`login_remedies` new first row L0 only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-15\ai-packages\qa-factory\scripts\driver_stage_build.py (`stand_question_text`, `stand_check` only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-15\ai-packages\qa-factory\scripts\human_text.py (`ONBOARDING_NOTE` neighbour constant, `onboarding_note` only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-15\ai-packages\qa-factory\scripts\driver_runner.py (`SITE_MOVES` only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-15\ai-packages\qa-factory\scripts\driver_machine.py (`_take_stand_answer`, new `_take_find_way_in` only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-15\ai-packages\qa-factory\scripts\project_decisions.py (new `record_stand_login`, new `_record_stand_login`, the `stand-login` subparser in `_build_parser`, one `elif` in `main` only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-15\ai-packages\qa-factory\references\question-prices.json (new key `s6.stand_confirm.login` only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-15\ai-packages\qa-factory\scripts\tests\test_human_questions.py (new table rows only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-15\ai-packages\qa-factory\scripts\tests\test_http_client.py (`SIGN_IN_ROWS` new join rows only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-15\ai-packages\qa-factory\scripts\tests\test-layers.json (`test_http_client.py` `covers` += `project_decisions.py`, `stand_health.py` only — §8 F-N3)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-15\ai-packages\qa-factory\scripts\tests\test_conductor_doors.py (`PINNED_ELSEWHERE` one entry only; slow, judged by the batch canon)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-15\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json (reported units only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-15\ai-packages\qa-factory\changelog.d\fv1-15-recorded-login-way-out.md (new)
non-goals: FV1-28 D1 (no registry reader, no precedence, no `sign_in` read); `stand_access.py` (FV1-17a); onboarding text; `no_address`/`stand_dead` sentences (FV1-5, its Lead amendment); `s6.stand_confirm` row (unchanged); CI, mutations.
handoff: builder report: witness, FR pass (A, B, C, D, E), `architecture:` / `judgment:`, census rows, test vs product lines.
edges: see "edges" below
DoD: the acceptance list below; verification `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for scripts/env_probe.py scripts/stand_health.py references/stand-answers.json scripts/driver_stage_build.py scripts/human_text.py scripts/driver_runner.py scripts/driver_machine.py scripts/project_decisions.py references/question-prices.json` and every non-slow, non-quarantined file it prints; slow ones (expected: `test_conductor_doors.py`, `test_story_run_*`) named "judged by the batch canon"; plus `test_judgment_census.py`, `selftest.py --lang`; no CI, no mutations
siblings: `stand_health._login_remedy` (L0, same node); the three other `onboarding_note` callers (`driver_dispatch.py:424`, `:777`, `driver_machine.py:498`) keep the default (no login door) — not applicable, they are not stand-login questions; FV1-28 D1 (§5)
designer: C:\QAFactory\forge-repo\docs\tasks\specs\20261114-fv1-17-15-cards-redraft-spec.md (this draft, once accepted)

Part P — the probe and its readers:
- P1 (B2, B5). `LAYER1["login"]` becomes the tuple: today's three members FIRST and unchanged, then
  `"the address recorded for signing in did not sign us in, and its answer does not look like a sign-in: "` (wrong_door),
  `"the sign-in recorded for this project came back with an answer that does not show whether a sign-in is there: "`
  (unjudged), `"the login this project records got no answer: "` (no_answer), `"the stand failed the sign-in with a server
  error: "` (stand_error), `"the stand limits requests, so the sign-in was not judged: "` (throttled), `"the project's own
  sign-in command did not get in: "` (command_failed, command_missing). `LOGIN_PREFIX_ANSWER`: an ordered tuple of (prefix,
  answer) pairs built from those constants (refused -> `credentials_refused`, did-not-finish -> `did_not_finish`, the fix ->
  `body_shape`, then the six above). `probe()` `:1145-1151`: `body_shape` and `did_not_finish` lines as today; otherwise the
  prefix by `receipt.get("answer")` from `LOGIN_PREFIX_ANSWER`; `credentials_refused`, `fields_unconfirmed`, an absent or
  unknown answer -> today's refused prefix. Every such line appends `"login"` to `blocked_by` (FV1-5's set does not grow, F8).
- P2. Receipts `probe()` builds itself (`:1021`, `:1110-1120`) and the device receipt (`:956`) gain `"answer": "not_tried"`
  and `"source": "access"`. `login_record` copies `receipt["answer"]` into the record when it is in `stand_access.ANSWERS`.
- P3. `env_probe.login_answer_of(out) -> str | None`: the answer of the FIRST Layer-1 item that `_word_of_item` reads as
  `login`, by the longest matching prefix of `LOGIN_PREFIX_ANSWER`; None when there is none (also for empty/None/crash text).
  Reads our own output only (FR-12).
- P4 (AR-13). `_derived_frontend` reads `stand_access.recorded_login(access)` (`outcome == "ok"`), not the raw dict.
  `stand_health._login_receipt` reads through `recorded_login` (status via `valid_status`: E5's `status: 0` -> "proved ... (the
  project's sign-in command)"); when `answer` is present the failed sentence ends "(<answer in plain words>)": wrong_door "its
  answer did not look like a sign-in", unjudged "its answer did not show whether a sign-in is there", others the word's plain
  form from one dict beside the function.
- P5 (B5). `login_remedies` gains a FIRST row `{"id": "L0", "answers": ["wrong_door"], "remedy": "The address recorded for
  signing in did not sign us in and its answer does not look like a sign-in: answer `find the way in` at the stand question,
  or run the onboarding again."}`; `_login_remedy(answers, code, outcome, user_key, answer=None)` passes `answer=` to
  `_row_takes` (FV1-17a). L0 matches `wrong_door` only; an old record without `answer` never reaches L0.

Part D — the door (Q1 (b), B1, A5, A13):
- D1. `stand_check`: after `why = env_probe.blocked_by_of(out)`, `answer = env_probe.login_answer_of(out)` when `why[0]` is
  `login`; pass `answer` and `searched = environment in (self.state.get("login_search") or {})` to `stand_question_text`.
- D2 (A5). `stand_question_text(..., why=None, answer=None, searched=False)`: for reason `login` the class by answer:
  `way` = {wrong_door, unjudged}; `stand` = {stand_error, no_answer}; `wait` = {throttled}; `account` = everything else and
  None. Body sentences: way/wrong_door "the stand `<x>` answers, but the address recorded for signing in did not sign us in,
  and its answer does not look like a sign-in. "; way/unjudged "... and its answer does not show whether a sign-in is there. ";
  stand "the stand `<x>` answers its health check, but its sign-in failed with a server error or gave no answer. "; wait "the
  stand `<x>` limits requests, so I could not check the sign-in just now. "; account = today's login sentence. Retry
  `what`/`says`: way -> "fix the sign-in the project records, or name the way the project signs in; I check again"; stand ->
  "look at the stand (its sign-in failed on its side), then I check again"; wait -> "wait a few minutes; I check again";
  account -> today's. For class `way` and NOT `searched`: options gain FIRST `{"answer": "find the way in", "token": "find the
  way in", "says": "I try every way in I know, record the one that signs in in place of the recorded one, and check the stand
  again"}` and the key is `"s6.stand_confirm.login"`; otherwise `"s6.stand_confirm"` (unchanged). For class `way` AND
  `searched`: no such option; the body gains "I already tried every way in I know for this stand in this story and none
  signed in; the onboarding, which asks you how the project signs in, is named below. "; `stand_check` passes
  `answer_note=human_text.onboarding_note(environment, names, login_door=True)`.
- D3. `question-prices.json` `s6.stand_confirm.login`: `find the way in` (`factory: command`, `person: none`, `delivery:
  unchanged`), then the three rows of `s6.stand_confirm` verbatim. `test_conductor_doors.py` `PINNED_ELSEWHERE`
  `"s6.stand_confirm.login": "test_human_questions.py (FV1-15: the stand-login variant, its find-the-way-in token and executor)"`.
- D4. `driver_runner.SITE_MOVES` gains `"find the way in": NM.SITE_DOOR`. `driver_machine._take_stand_answer`: after the
  stand-name branch and BEFORE `if token in self.seam_tokens(asked)`: `if token == "find the way in" and token in
  self.seam_tokens(asked): return self._take_find_way_in(stage, words)`. `_take_find_way_in(stage, words) -> bool`:
  `self.answer_file()`; `self.answer_row(f"{stage} (find the way in): ", words.strip(), what="your answer to the question")`;
  `code, out = self.py("project_decisions.py", "--root", str(self.project), "stand-login", "--stand", environment,
  "--words-file", str(self.task_root / self.answer_file()))`; record `self.state.setdefault("login_search", {})[environment] =
  {"at": _now(), "exit": code}` and `save_state()`; print one line: exit 0 -> "<stage>: a way in was found and recorded; the
  stand is checked again"; else "<stage>: no way in signed in; the question comes back" (+ the refusal's first line, cut at
  300); return True (the step runs again, as `retry`: `stand_check` probes the stand anew).
- D5 (B1). `human_text`: `ONBOARDING_LOGIN_NOTE = "The onboarding, which asks how the project signs in: `/qa-factory:qa-onboarding`."`;
  `onboarding_note(environment, stands, *, login_door=False)`: `login_door` True -> `ONBOARDING_LOGIN_NOTE` whatever the
  stands; else today's rule. The body never carries the command (human-questions.md rule 5).
- D6. `project_decisions.record_stand_login(root, *, stand="", words) -> dict` and CLI `stand-login [--stand NAME]
  --words-file F` through `_record_stand_fact` (one wrapper): `config = _project_config(root, "the way the project signs
  in")`; `_stand_of(config, stand)` when `environments[]` has rows (refusals as today), else no stand; `report =
  stand_access.try_roads(config, root, env_name=stand)` (no `--command`, no candidates: code never composes a command);
  `first_in` None -> `ValueError("no way in signed in (<road>: <answer>; ...names only); nothing was written")`; road (a) is
  `first_in` -> `{"unchanged": True}`; else `new = <the road's access> + {"login_probe": <road's record with answer>}`,
  `config_contract.access_errors(new)` non-empty -> refusal naming the first error, nothing written; else `upsert(root,
  field_refs=["/environment/access"], essence=f"how the project signs in to the stand {stand or '(the only one)'}",
  asked="stand check: the sign-in the project records did not get in; find the way in", scope="project", owner="user")` and
  `resolve(root, row["id"], words, f"stand-login {stand or 'block'}", {"/environment/access": new})`. Returns `{"road",
  "kind", "replaced": <old kind>, "decision", "tried": n}` (names only).

edges:
- E-P1 POSITIONAL (B2): new prefixes are appended AFTER today's three members of `LAYER1["login"]`; INVARIANT: every login
  Layer-1 line reads `login` through `blocked_by_of` (one row per prefix), and no new prefix starts with another member (the
  longest-prefix read stays unambiguous).
- E-P2 INVARIANT (FV1-5): a dead stand still gets "did not answer"; `no_address` still gets the config sentence; nothing here
  lets a stand pass without exit 0 or a person's word.
- E-D1 POSITIONAL (`_take_stand_answer`): the find-the-way-in branch sits after the stand-name branch (a stand literally named
  "find the way in" keeps its road) and before the generic seam (which would send the SITE_DOOR move to the conductor).
  INVARIANT: the token is executed only when THIS question offered it.
- E-D2 (A13): the option opens only on the access-source prefixes (`way` class from `LOGIN_PREFIX_ANSWER`); a prefix FV1-28 D1
  adds for a registry-source failure is not in that class, so `login_answer_of` returns its own word or None and no option
  appears. INVARIANT: re-recording `environment.access` is never offered while a registry way would still shadow it (§5).
- E-D3 LOOP: one search per stand per story (`login_search`); after it, only retry / go on / another stand + the onboarding
  note. A driver restart keeps `state` (no second search). A NEW story searches again (its own state).
- E-D4 LOCKOUT: the search is one roads run (FV1-17a budget) right after a probe that already failed once: worst case per
  story = S0 probe + S5 probe + budget (<= 3) + S6 probe. Stated, accepted under Lead decision 4.
- E-D5 TEMPORAL: (before FV1-15) a config `local_login /login {405, failed}` without `answer` — the live probe now returns
  `wrong_door` (FV1-17a) and the S5 question offers `find the way in`; the old record reads `answer: None` and is never
  guessed. (after the search) `environment.access` holds the found road, the decision row keeps the person's words, the
  receipt of `resolve` keeps `before` (revert road). A no-trace story writes it like `stand-account` (no `no_trace` rule in
  `project_decisions`; §8 F-N5).
- E-D6 CONFLICT: `ui_only` recorded -> login `skipped`, no Layer 1, no question about sign-in; whether API cases can sign in is
  the strategist's judgment (P27). A search whose `first_in` is a non-harness road replaces a `harness_command` access: the
  stand's own address stops being derived as its UI (`_derived_frontend`); the success line says the kind replaced.
- E-D7 EMPTY: `out` empty/None -> `answer` None -> class `account` (today's words); `environment` empty -> no login class
  (today's no-name branches); `stand-login` on a project without config -> today's `_project_config` refusal.
- E-D8 TEXT: every sentence passes `human_text.problems`; unknowns said as unknowns ("does not show whether"); no probe
  vocabulary, URL or credential in the body (details file only).

Tests: `test_human_questions.py` ONE table `STAND_LOGIN_ROWS` (driver side of the probe text, outside input = our probe's
text): per Layer-1 prefix `prefix-<answer>` -> `blocked_by_of == ["login"]` and `login_answer_of == <answer>`; `class-way-wrong`,
`class-way-unjudged`, `class-stand`, `class-wait`, `class-account`, `answer-none`, `out-empty`, `out-traceback`: sentence +
options + key, each `human_text.problems == []`; `searched-no-option` (+ onboarding login note in the answer block);
`find-way-token-executed` (the `_take_find_way_in` call, exit 0 and exit 2), `stand-named-find-the-way-in` (name wins).
`test_http_client.py` join rows (F-N3): `stand-login-e1` (E1 config on the stub -> `record_stand_login` writes `form_login`,
then `env_probe.probe` exit 0), `stand-login-none-in` (refusal, config bytes unchanged), `stand-login-a-in` (unchanged),
`stand-health-e5` (`_login_receipt` "proved ... sign-in command" for `status: 0`), `remedy-l0` (answer wrong_door -> L0; no
answer + 405 -> today's).

Census / owners: `login_answer_of` — data, `shape` (own output form); the `way` branch of `stand_question_text` — data,
`shape`; L0 — data row; `record_stand_login` refusals — data, `shape` (selection, no road in, access_errors) as the census
test reports; whether to search, go on or re-onboard — intent (the person's token); WHICH road is recorded at story time —
data under the person's word (first `in` in the fixed road order; §8 F-N1).
architecture: AR-9 (each refusal names what it expected and a door), AR-13 (`recorded_login`, `valid_status` adopted),
AR-14 (config written only through `upsert`+`resolve`), AR-16 (texts through the one question form, priced variant key),
AR-17/AR-25 (a recorded wrong sign-in has a move: `find the way in`, then the onboarding), AR-18 (one more output reader
beside `blocked_by_of`, same constants), AR-20 (census ratchet), AR-22 (`answer`, `source` read), AR-28.
judgment: no role judgment moves into code; the person decides the search; the road choice at story time is the open fork F-N1.

## 4. Order, parallelism, live branches

```
FV1-17a ──┬──> FV1-17b
          ├──> FV1-15
FV1-17c (now, parallel with 17a: no shared file)
```
- Parallel NOW: FV1-17a ∥ FV1-17c (file-disjoint). FV1-17b and FV1-15 wait for FV1-17a (they call `form_session` /
  `answer`, `recorded_login`, `_row_takes(answer=)`); then FV1-17b ∥ FV1-15 except two shared files, cut by rows:
  `test_http_client.py` (`SIGN_IN_ROWS` new rows, append only) and `judgment-census.json` (rows) — the later merge resolves.
  `env_probe.py` is touched by 17a (`_empty_stand_answers`, `stand_answers`, `_row_takes`) and FV1-15 (other functions):
  serialised by the dependency, also function-disjoint.
- Live branches (Lead decision 3). `git diff --name-only` could NOT be run (no shell in this session). Evidence instead:
  (i) FV1-17 critic: `wip/tbw-t1r` touches, of these files, only `judgment-census.json` (rows) and `hooklib.py` (read-only
  here); (ii) a line-count comparison of 22 card files (Grep `^` count) between wave13 (origin/main) and each worktree:
  `fv1-24-k1`, `fv123-a5`, `sc-n7` equal main on all 22 (stand_access 519, env_probe 1273, driver_stage_build 606,
  test_human_questions 971, test-layers 10713, judgment-census 1272, ...); `tbw-t1r` and `tbw-t3a` differ on env_probe 1226 /
  driver_stage_build 581 / test_human_questions 839 / state-exits 281 — their base is older than FV1-5 (pre-1a00352), so the
  difference is main moving, not their edit; `test-layers.json` (10714 / 10708) and `judgment-census.json` (1269) differ for
  both tbw branches — rows of those two shared registries, append-only, resolved at merge. A line count is a HEURISTIC, not a
  diff: the Lead runs `git diff --name-only origin/main...origin/<branch>` for the five before launch.
- One critic pass for the topic (R13-g) after FV1-15 and FV1-17b, or one for 17a+17c and a re-review by diff (Lead).

## 5. Seam with FV1-28 (its amendments 9, 10, 11)

- 9a — the executor D1 calls: `stand_access.login(access, values, base_url, timeout, health_url, cwd, source="registry")`, the
  same one act the probe calls, with an `environment.access`-shaped object validated first by
  `config_contract.access_errors`; `form_login` carries the csrf two-step (FV1-17a item 4). D1 needs nothing else from these
  cards. For a search of every way, D1 has `stand_access.try_roads(full_cfg, root, env_name=...)` (not required by D1).
- 9b / Q2 — `stand_access.code_login_declined(access)` is the one reader of the person's `ui_only`. Q2 (Lead): D1 checks it
  FIRST; when True the registry `http` way is shown in briefs and never probed into a Layer-1 stop. INVARIANT for D1: a role's
  record never overrides the person's word into a stop.
- 10 — D1's failure line is D1's own prefix; D1 must add it to `LAYER1["login"]` (B2 invariant) and must NOT add it to the
  `way` class of `LOGIN_PREFIX_ANSWER` (E-D2) — its door is `project_knowledge.py revoke --id PK-n`, not `find the way in`.
- 11 — one precedence order (registry > `environment.access` > default) lives beside `project_knowledge.sign_in`; these cards
  add no precedence. What differs from the FV1-28 review's words: the receipt field is `source` (values `access` |
  `registry`), set by `login(..., source=)`, not by the caller; `ui_only` is read through `code_login_declined`, not by a
  string compare in D1.
- The shadowing loop (FV1-17 critic Key 7.1) is D1's choice; these cards make it possible: `find the way in` is offered only
  on access-source answers, so it never re-records an access a registry way shadows.

## 6. Checks, owners, census classes (AR-29), and the four questions (rule 10)

| Check / decision | Card | Owner | Census class |
|---|---|---|---|
| `answer_of` + `login_answers` rows | 17a | data (code) | shape |
| `login_roads` row validation | 17a | data | shape |
| `access_errors` new branches (kind, form id, answer word, status) | 17a | data | shape |
| budget stops in `try_roads` | 17a | data | safety |
| form-road redaction | 17a/17b | data | safety |
| negative control | 17a | data (evidence only) | shape |
| which road at onboarding | 17c | judgment of the onboarding role, shown to the person in the phase-4 digest | — (no code) |
| `ui_only` | 17c | intent (the person) | — |
| `login_answer_of`, the `way` branch | 15 | data | shape |
| `record_stand_login` refusals | 15 | data | shape (as reported) |
| search / go on / re-onboard | 15 | intent (the person's token) | — |
| which road at story time | 15 | data under the person's word (F-N1) | — |

Four questions, per mechanism:
- M1 sign-in answers + form road + roads command (17a). (a) cost: up to 3 requests x 8 s per form row, up to 2 x 60..300 s per
  harness road, a liveness GET per road (the probe road); at most 3 failed real-secret sign-ins + 1 junk run per roads run —
  paid by onboarding / one story search. (b) axes: §7. (c) detector: `SIGN_IN_ROWS` (test_http_client), `test_judgment_census.py`;
  the leak (an onboarding that asks or writes "impossible" before the roads) — the FR-33 `live-runs` row and a calibration
  line reading onboarding transcripts for the four-answer question with no roads output before it (Lead to register in
  `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`; §8 F-N6). (d) on the path: the probe calls `login()` by code at S0/S5; the roads
  command is called by the role (17c) and by the story executor (15) by code.
- M2 onboarding roads-first (17c). (a) one roads run per failed proof. (b) §7. (c) role-rules registry rows + the calibration
  line above. (d) DISCIPLINE ALONE (the role text calls the command); detector named in (c).
- M3 probe words + the door (15). (a) one more priced option; one search per stand per story. (b) §7. (c) `STAND_LOGIN_ROWS`,
  the join rows, `test_conductor_doors.py` census (canon). (d) code: `stand_check` raises the question; the token's executor is
  code (FR-9).
- FR-33 live proof (one `live-runs` row, moved there when the nodes are accepted): "MyBooks onboarding from the E1 config
  records `form_login` through the roads without the operator; a MyBooks story whose recorded sign-in is `local_login /login`
  answers `find the way in` and passes the stand check."

## 7. SIBLING_MAP axes (origin/main, 37 axes) — one block for M1-M3

- axis 1: n/a — no policy/role-file/journal change.
- axis 2: n/a — no exam instrument.
- axis 3: covered — the package change ships by the release copy; nothing of the release flow changes.
- axis 4: n/a — no factory rule text changes; FR-50 is applied, not edited.
- axis 5: covered — rows "How the stand logs in" (new kinds, one reader `recorded_login`, one classifier, the roads, the story
  writer `stand-login`: the row is updated in the 17a commit by the Lead from the builder's drafted line, and again by FV1-15
  for `stand-login`), "Redactor <-> secret guard" (`_safe`, the form redaction tuple), "Onboarding answer <-> its written place"
  (topic 2 -> p4 -> readers).
- axis 6: n/a — no measurer reads these fields.
- axis 7: n/a — no per-test identity.
- axis 8: n/a — no story path resolution.
- axis 9: n/a.
- axis 10: n/a.
- axis 11: n/a — the harness command is split by the existing `_argv`.
- axis 12: covered — findings/rows go through the pile (no BACKLOG line).
- axis 13: n/a — dispatch text unchanged.
- axis 14: n/a.
- axis 15: n/a.
- axis 16: covered — `login-roads.json` read through `hooklib.read_json`; `stand-answers.json` through its one reader.
- axis 17: covered — the probe's output shape gains no new key; `login_answer_of` reads it beside `blocked_by_of`.
- axis 18: covered — census rows only as reported; no ratchet raise expected (a raise is named in the verdict).
- axis 19: n/a.
- axis 20: n/a.
- axis 21: n/a — no markdown table reader.
- axis 22: n/a.
- axis 23: n/a.
- axis 24: n/a.
- axis 25: n/a — `checked_at` unchanged.
- axis 26: n/a — `stand not confirmed` block literal untouched; the new token passes no block.
- axis 27: n/a.
- axis 28: n/a.
- axis 29: n/a — no jsonl writer.
- axis 30: n/a.
- axis 31: covered — p2/p4/SKILL carriers; one owner per aspect (p4 owns the roads step, SKILL.md points).
- axis 32: covered — census classes in §6.
- axis 33: n/a.
- axis 34: covered — one sign-in act `stand_access.login` for probe, roads and story search; `form_login` reaches the capture in
  FV1-17b (a node with owns, not an exclusion); `ui_only` is one road for D1 (§5).
- axis 35: n/a.
- axis 36: n/a.
- axis 37: n/a — the stand question is not a repeat-stop site (the search runs once, E-D3).

## 8. NEW forks (recommendation first)

- F-N1 — which road the story-time search records. (A, recommended) the first `in` in the fixed road order (recorded, form rows
  by data order) under the person's `find the way in`; the success line names the replaced kind. (B) the conductor reads the
  roads report and chooses (a role's judgment, AR-2; one more paid call, slower). Cost of A: a story could replace a
  harness access with a form access and lose the derived UI address (E-D6), said in the line.
- F-N2 — attempts across runs. (A, recommended) no persisted counter; per-run budget + "at most two roads runs per onboarding,
  none after credentials_refused" (17c) + one search per stand per story (15). (B) a persisted per-stand failure ledger with a
  cool-down (new state file, new writer, AR-14 review). Cost of A: several stories in one hour each spend up to 3 failures.
- F-N3 — homes of rows whose natural file is quarantined/slow (`test_stand_access.py`, `test_stand_health.py`,
  `test_project_decisions_stand_facts.py` quarantined; `test_config_migration.py` slow). (A, recommended) the Lead's list
  decision: `test_http_client.py` `covers` += `stand_access.py`, `references/login-roads.json`, `references/stand-answers.json`
  (17a) and `project_decisions.py`, `stand_health.py` (15, join rows only). (B) the Lead registers a new keep table for
  `stand_access.py` (TESTING.md: by the Lead's list). Cost of A: one table file carries two modules' rows.
- F-N4 — p4 `:269` after FV1-17b lands: `form_login` still routed to the token question. (A, recommended) one follow-up row
  in the next untaken batch of `live-run-fvf` ("p4 `:269`: `form_login` signs in by the form road"), opened by the Lead when
  17b is accepted. (B) put it in 17b's owns (crosses into text; 17b becomes a code+text node).
- F-N5 — `stand-login` in a no-trace (comparison) story: (A, recommended) as `stand-account` (no special rule; the project's
  own factory folder is not a project trace under P8). (B) refuse in no-trace (the comparison run then cannot pass the stand
  check by the search).
- F-N6 — the calibration line for the leak of M1/M2 (rule 10 (c)): a Lead-tier write into
  `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`; recommended in the same batch, Lead.
- F-N7 — FV1-15 size (~9 files, two parts P and D). (A, recommended) one node, two parts, one critic. (B) split FV1-15a (P) /
  FV1-15b (D) serial — not in the Lead's cut; only if the builder's budget warns.

## 9. What I did NOT establish

- No `git` command ran (no shell in this session): the live-branch overlap (§4) rests on a line-count heuristic plus the
  FV1-17 critic's diff of `wip/tbw-t1r`; uncommitted edits in wave13 were not ruled out.
- `test_state_exits.py` — whether it enumerates config values (the `ui_only` row may be ignored by it or may need a source):
  not read; 17c item 4 says stop and report on failure.
- `test_judgment_census.py` — which new units it will report (expected: refusal transports in `record_stand_login`, maybe
  `access_errors`): not run.
- `scenario_walk.py --witness-for` output for these owns: not run (the builder's DoD runs it).
- How `test_conductor_doors.py` collects "raised" keys (literal at the site vs computed): read only `census_problems`; the
  variant key is passed as a literal in `stand_question_text` so either way it is seen.
- `manual_capture.py` / `investigation_probe.py` lines for 17b: first-draft numbers, not re-read on e4df9c0 (no commit to those
  files since 13.11 per the FV1-17 critic's `git log`).
- The real MyBooks stand's answers (E4) were not re-measured; the NextAuth row rests on the operator's measurement.
- `references/human-questions.md`, `docs/TESTING.md`, `plans/builder-rules.md` were not re-read in this pass (their rules are
  quoted from CLAUDE.md, PROJECT.md and the two critics).

## 10. Small choices closed by the designer

- Roads run through `env_probe.probe` per road (one road with the probe, P31) rather than a second base/values computation.
- `REAL_SECRET_FAILURES_CEILING = 3`, `CANDIDATES` ceiling 5 as code constants above the data defaults (1, 5).
- `wrong_door` vs `unjudged` for a form session without proof: `unjudged` (no positive evidence).
- `bearer_env` 3xx -> `unjudged` (an expired token redirected to an identity provider is a token judgment, not a wrong door).
- `form_login.url` optional base (frontend on another origin); empty = the stand base.
- Variant price key `s6.stand_confirm.login` instead of a fourth row in `s6.stand_confirm` (keeps the slow C16b pin true).
- `source` is set inside `login()` (one place), default `"access"`.
- The story-time search passes no `--command` (code never composes a command).

## 11. Reading trail

Read whole: first draft spec; FV1-17/15 plan critic; FV1-28 plan critic; `stand_access.py` (wave13). Read in part (wave13 =
origin/main e4df9c0): `env_probe.py` `:88-117`, `:228-357`, `:510-579`, `:835-1274`; `http_client.py` `:105-264`, `:330-470`;
`config_contract.py` `:100-129`, `:265-409`, `:1005-1029`, `:3035-3080`; `stand_health.py` `:675-754`;
`driver_stage_build.py` `:1-190`; `human_text.py` `:120-164`; `project_decisions.py` `:375-387`, `:440-700`, `:760-959`;
`driver_machine.py` `:2340-2429`, `:3950-4019`; `driver_runner.py` `:1290-1329`; `references/stand-answers.json` (whole);
`references/question-prices.json` `:1-30`, `:230-259`; `p4-generate.md` `:235-324`; `p2-interview.md` `:155-214`;
`SKILL.md` `:70-129`; `design/state-exits.md` `:1-25`, `:60-79`; `test_conductor_doors.py` `:630-694`;
`test-layers.json` rows `:2516-2552`, `:5491-5500`, `:6136-6145`; FV1-28 spec `:270-309`.
Greps (with controls): git refs/HEADs in `.git/worktrees/*` (control: `ba903eb` found in read-main HEAD); `login_probe` readers
not re-run (critic's list, C16); `onboarding_note\(|ONBOARDING_NOTE` (4 callers); `stand_confirm` (package); `def
(_take_stand_answer|take_seam_answer|site_seam_person|closed_question|stand_names)`; `access_errors\(|environment_errors\(`;
`(config_contract|CC|C)\.validate\(`; `"project_decisions\.py"` in `driver_*.py`; `no_trace|def _set_pointer` (control =
`_set_pointer`); test-layers keys for 10 test files; `slow_tests.json` (control: `test_config_migration`, `test_story_run_s6`
found); `"quarantine"` head `:7169`; `"environment\.access"` in config-keys (3 entries); SIBLING_MAP `^## Axis \d+ — ` (37);
line counts of 22 card files in wave13 and five live worktrees; journal `dev1.jsonl` lines naming the five branches.
Needed beyond the manifest: none written; read beyond the brief's list: `driver_machine.py`, `driver_runner.py`,
`question-prices.json`, `test_conductor_doors.py`, `project_decisions.py`, FV1-28 spec (for the executor seam).
