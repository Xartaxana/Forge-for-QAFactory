# PK2-6 - the stand's `default` account is decided once at gate A (draft spec)

task: t-1579 | node: project-knowledge/2/PK2-6 | feature: F04 | designer draft, 19.11.2026 | status: DRAFT for Lead acceptance
source finding: `plans/piles/project-knowledge/findings/20261111-default-ucherka-tri-karty-vne-invarianta.md` (direction chosen by the Lead:
the unmet `default` goes through ONE "decided once" function; the two other roads read its decision instead of asking).

Line numbers below were measured by Read/Grep on the working tree on 19.11 (the gitStatus snapshot names HEAD 486bc891; the brief's scout
read 6266f2b0 - the lines moved: the brief's :747/:1163/:2543/:2757-2787/:4731 are now :724/:1155/:2544/:2759-2844/:4689). Code is pointed at
by `path::symbol`; the line is only a reading aid.

## 1. Invariants, owners, variety

AR-n touched (`ai-packages/qa-factory/design/architecture.md`), each with the change check the builder's DoD carries:

- AR-28 (an unknown never becomes a pass) - the decision has a stated behaviour on absent / unreadable / revoked input (§4); a test row pins
  each (table rows R7-R9). Never zero questions for an unmet default.
- AR-15 (one survivor) - the "decided once" for `default` at gate A is ONE builder, `Rehearsal._default_account_card`, called from two steps
  and guarded so it emits once; the exact-`default` predicate gets one survivor `is_default_account` and every site in `gate_preflight.py`
  is wired to it (sites listed in §5 card, item 1). Change check: the report lists every site of `str(...).strip() == "default"` before and after.
- AR-13 (one reader) - the default keys are read only through `manual_capture._default_keys` and `gate_preflight.integration_login_keys`;
  the env values only through `_loaded_env_files` + `_env_names`; the need only through `default_login_needed`. No new parser.
- AR-19 (stage twins) - S6 `Driver.stand_login_problem` reads the same `default_login_needed`; its rule is NOT changed (non-goal, PK0-5/PK2-15).
  The report names S6 as the twin, unchanged.
- AR-16 (one question form) - the merged card's text passes `human_text.problems(kind="question")`; its literal is added to the FR-6 scan
  (`test_gate_preflight.py::NEW_CHECK_FUNCTIONS`).
- AR-29 (code judges data) - the checks this spec adds or alters, with owner and census class:
  - NEW `Rehearsal.check_default_account` (a `check_*` name = census unit u1): asks the person for a credential -> owner **intent**,
    class **safety** (same as `check_s5_credentials`); a row is added to `scripts/tests/fixtures/judgment-census.json`.
  - ALTERED `check_s5_credentials` (safety / intent, row unchanged), `check_actor_sign_in` via `_probe_actor` (safety / intent, unchanged),
    `check_case_preconditions` (shape / data, unchanged). No check here judges a role's content: presence of keys and joins only.
  - Commit line: the `judgment:` line in the form `tools/architecture_gate.py` checks (that file is the only carrier of the grammar; it is
    not copied here), naming `check_default_account` with class safety and owner intent. Never a bare `judgment: none`.
- AR-25 - no new recorded state: the in-story answer is an existing `stage_overrides` row whose way out is `waiver.py` revoke (FR-40).
- AR-14 - not touched: no new artifact, `state/sign-in-probe.json` keeps its one writer.

Variety walk (§ A):
- axis 7: held by key -- `environment.user_key` / `environment.secret_keys` / `extra_keys` (config) and the env files the runner loads;
  unknown value -> `manual_capture._default_keys` falls back to AUTH_USERNAME / AUTH_PASSWORD and the gate asks (one card), never a pass.
- axes 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13: n/a -- the change only merges the questions gate A already asks about one account; it reads
  no product, surface, runner, tracker, delivery, host, process, language, size or age value.

One road (P31, SIBLING_MAP axis 34): the change REMOVES two roads; no language/project/case is left out. The reserved `default` reaches the
same mark dict `_account_carded` the roles use (PK0-4), under a key no role form can produce (§3).

## 2. The three roads today (re-read on the tree)

Order of one gate-A run (`gate_preflight.py::run`, the `steps` tuple, ~:6175): `check_role_accounts` (skips `default`: `_declared_role_forms`
drops `config_contract.reserved_role`) -> `check_actor_sign_in` (ROAD 1) -> `check_s5_dependencies` ... `check_s5_runtime_probe` ->
`check_s5_credentials` (ROAD 2) -> `check_case_preconditions` (ROAD 3). So today road 1 fires first, road 3 last.

| road | path::symbol | fires when | what it asks the person today |
|---|---|---|---|
| 1 | `scripts/gate_preflight.py::Rehearsal._probe_actor` (called by `check_actor_sign_in`; actors from `_actors_of_manual_cases`) | a `manual-agent` case declares `{"stand_account": "default"}` and `_stand_account("default", ctx)` is `unmet` (a key of `manual_capture._default_keys` absent) | ONE PERSON_DECIDES finding, check `actor_sign_in`: "sign-in of the account default was not tried: the default account needs <keys>, not set where the runner reads it (...) (<cases>)", three answers + door `actor_sign_in-N: accept`. Its deferral `carded = self._account_carded.get(_role_form(actor))` never holds for `default` (never carded). |
| 2 | `scripts/gate_preflight.py::Rehearsal.check_s5_credentials` (the `missing` / `self.add` block after `needed = default_login_needed(...)`) | `default_login_needed` is True AND a key of `integration_login_keys(environment)` (user_key + secret_keys + extra_keys, NO defaults) is absent | ONE PERSON_DECIDES finding, check `s5_environment`: "<S5> needs credentials it does not have - keys not set anywhere this session: <keys, cut at 8> (names only; nothing here reads a value)", fix "answer with your approval: put them in `<rel>` ..., or accept the gap ...". No door word, no cases. |
| 3 | `scripts/gate_preflight.py::Rehearsal.check_case_preconditions` (`_sort_items` -> `_check_one_precondition` -> `_stand_account("default")`, then `_card_items` / `_case_question`) | EVERY case (any disposition) whose preconditions carry a `default` account item that is `unmet`; off under `gate_rehearsal.skip_preconditions` | ONE card PER CASE: a stand-gap card (scope `case`, when the item carries a valid `remedy`) or the case's own question (`_precondition_door` returns None for `default`: the general door). Two cases = two cards. |

Measured divergence the roads carry (load-bearing, read at `gate_preflight.py::integration_login_keys` and
`manual_capture.py::_default_keys`): road 2 reads `user_key`, all `secret_keys`, `extra_keys`, with NO default; roads 1 and 3 read
`user_key or AUTH_USERNAME`, `secret_keys[0] or AUTH_PASSWORD`. A project with no `environment.user_key` gets NO road-2 card while roads
1/3 ask for AUTH_USERNAME / AUTH_PASSWORD (fork F2).

Measured latent defect in the node's reach (fixed by this card, not filed): `_role_form("Default") == "default"` (`gate_preflight.py::_role_form`
lower-cases and folds separators) while `reserved_role` and `_stand_account` test the EXACT text `default`. A case naming a product role
`Default` gets a role card `RA-<stand>-default`; then (i) road 3 drops a reserved `default` item of another case because
`(stand, _role_form("default")) in self._role_carded`, and (ii) road 1 defers the reserved `default` actor to that role card. The person
answers about role `Default`; the default account stays missing.

## 3. The ONE decision

Where it is recorded: in the rehearsal, in memory - the existing PK0-4 mark dict `Rehearsal._account_carded`, under the module constant key
`DEFAULT_MARK = ("reserved", "default")` (a tuple: no `_role_form` string can equal it). Values: `"login"` (the card is in `findings`) or
`"accepted"` (the card was raised and `add` dropped it because the person's recorded word passes it). Nothing is persisted: the person's
answer lives where it lives today - the keys in the env file the runner loads (next rehearsal reads `met`), or a `stage_overrides` row of
`pipeline.json` written by the existing word road (the card's door, fork F4). Cross-story storage: fork F3.

How it is made: `Rehearsal._default_account_decision()` (pure, memoised on `self._default_decided`, never raises; name outside the census
`UNIT_NAME_RE`) returns `{"needed", "state", "missing", "cases", "detail", "rel"}`:
1. `needed` = `default_login_needed(self.task_root, self.config)` (unchanged rule; True on any exception).
2. `cases` = ids of the cases a road would ask about: the cases whose parsed preconditions name `default` through `case_account_roles`
   filtered by `is_default_account` (read once through `self._case_checks()`), in file order; under `gate_rehearsal.skip_preconditions`
   only those whose plan row is `manual-agent` (`plan_rows_of(..., ("manual-agent",))`) - road 3 would not ask the rest.
3. `needed` False -> `state = "not_needed"` (by rule (a) of `default_login_needed` a declaring case makes `needed` True, so `cases` is empty).
4. env read (`_loaded_env_files`, `_env_names`) raises -> `state = "error"`, `detail` = the reason. Any other exception -> `"error"`.
5. `missing` = absent keys of `integration_login_keys(environment)` (road 2's set), then - only when `cases` is non-empty - absent keys of
   `manual_capture._default_keys(environment)` (roads 1/3's set), order kept, duplicates dropped (fork F2, recommendation (c)).
6. `missing` non-empty -> `"unmet"`, else `"met"`. `rel` = `_place_of(files, how)`.

Who writes the card: `Rehearsal._default_account_card()` (idempotent; guarded by `self._default_card_done`, set only after success):
`state == "unmet"` -> ONE `self.add("s5_environment", PERSON_DECIDES, <message>, <fix>, subject="default-login", cases=<cases>)`, then
`self._account_carded[DEFAULT_MARK] = "login"` if the finding count grew, else `"accepted"`. Card BEFORE mark: a mark never exists
without its card having been raised. Any other state: no card, no mark.
- message: today's road-2 sentence unchanged up to and including the key list and its cut (so a word recorded on today's card still
  matches), plus, when `cases` is non-empty, the cases that sign in with the stand's default account (`_cases_phrase`: up to `ROLE_NAMED`
  ids, else "the N cases"), plus today's "(names only; nothing here reads a value)". Wording is the builder's; it passes `human_text.problems`.
- fix: today's road-2 fix (it names `rel`), plus `self.waiver_command(DEFAULT_ACCOUNT_BLOCK, "", "accept")` with
  `DEFAULT_ACCOUNT_BLOCK = "the stand's default account"` (fork F4).

Who calls it: NEW step `check_default_account` (returns at once when `project_root is None`; else calls `_default_account_card()`),
registered in `run` right AFTER `check_role_accounts` and BEFORE `check_actor_sign_in`; and `check_s5_credentials` calls the same builder
where its login block stood (a no-op when already done) - so a rehearsal that runs road 2 alone still asks exactly as today.
POSITION invariant: the mark exists before road 1 and road 3 read it; road 2's call can never raise a second card (the guard).

What the readers do once the mark exists:
- ROAD 1 `_probe_actor`: the lookup key is `DEFAULT_MARK` when `is_default_account(actor)`, else `_role_form(actor)` (so a role `Default`
  never reads the default mark and the reserved `default` never reads a role card). `unmet` + mark -> NO finding, one note: `"login"` ->
  today's "the sign-in of default waits for the card about its account"; `"accepted"` -> "the sign-in of default was not tried: you accepted
  the gap of its account". The row stays `not_proved` (S6 still refuses a default session without an `ok` row). Extras (`_extra_accounts`)
  unchanged. `met` -> the real sign-in as today.
- ROAD 2 `check_s5_credentials`: reads `needed` from the decision (no second `default_login_needed` call); keeps the env-file-absent card
  and the "default account is not asked" note; the login card only through the builder.
- ROAD 3 `check_case_preconditions`: in the existing PK0-4 filter (after `_sort_items`, BEFORE `_card_items`) an open `stand_account` item
  leaves `open_items` when `is_default_account(spec) and DEFAULT_MARK in self._account_carded`, or when NOT `is_default_account(spec)` and
  `(stand, _role_form(spec)) in self._role_carded`. Other items of the same case keep their card/question. No note (the card names the cases).
- A reader that finds no mark (step not run, raised, or state not `unmet`) behaves exactly as today.

## 4. Edges (behaviour + the invariant it protects)

| # | edge | behaviour | invariant |
|---|---|---|---|
| E1 | decision ABSENT (step skipped/raised; a road run alone; the world before this change) | no mark when a reader looks: road 1 (runs before road 2) asks itself as today; road 2 raises the card through the builder and so sets the mark; road 3 (after road 2) then defers to it - 2 questions, not today's 2+N; road 3 run alone asks as today; a raise of the step is `unavailable("default_account")`, a FACTORY_DEFECT that holds the gate | absence never removes a question (never zero, AR-28); a road defers only to a card already raised |
| E2 | decision UNREADABLE (env files unreadable; any exception in the decision) | `state = "error"`: no card, no mark; each road says its own finding as today (road 2 `unavailable`, road 1 FACTORY_DEFECT, road 3 a broken-check FACTORY_DEFECT) | an unknown is never `met` and never silences a road; the gate is held |
| E3 | decision REVOKED (the person's accept row gets `revoked_at`; or keys removed from the env file after `met`) | next rehearsal: the card is raised again -> mark `"login"` -> exactly one card; roads 1/3 defer again | revocation brings back exactly ONE card, never zero, never three |
| E4 | answer CONFLICTS with the probe - (a) the person said the keys are set, the decision still finds one absent | `unmet`: the card again (the data wins) | a person's claim never reads as `met` without the keys |
| E4b | (b) keys present, the stand refuses the sign-in (`not_landed`) | decision `met`: no login card; road 3 counts the item held; road 1's own "the stand did not let it in" card is the ONE card. A recorded accept of `DEFAULT_ACCOUNT_BLOCK` does NOT pass it (another block) | a word about missing keys never passes a refused sign-in |
| E4c | (c) an accept is recorded, the keys are now present and the sign-in lands | no card; the accept is inert; the cases run | a stale accept never blocks a working account |
| E5 | accepted (the card's door word recorded) | `add` drops the card, mark `"accepted"`: zero findings about `default` from all three roads; road 1 notes "you accepted" | one word decides all three roads (FR-10) |
| E6 | a word recorded BEFORE this change on a retired road (road 1 block "sign-in of the account default"; a per-case card) | it does not pass the merged card (different block): asked once more | a word about one block never passes another (fork F5) |
| E7 | product role spelled `Default` / `DEFAULT` / `default_` plus a reserved `default` item | the role card holds only the role's cases; the reserved item goes to the default card: two cards, two facts | a role never reads the default mark; `default` never reads a role card |
| E8 | ` default ` (spaces) | the reserved account (stripped, as K-27.2) | same predicate everywhere (`is_default_account`) |
| E9 | needed by automate only, no case declares `default` | card lists road 2's keys only, no cases, no AUTH_* fallback keys | the asked key set is exactly what today's roads ask (F2 (c)) |
| E10 | needed, `integration_login_keys` empty, no declaring case | `met`, no card (as today) | no new question appears |
| E11 | `environment` config not an object | `environment` read as `{}`; road 2 still returns early as today; the step asks only when a declaring case lacks AUTH_* | a broken block never silences a declared need |
| E12 | `skip_preconditions: true` | `cases` = manual-agent declaring cases only; road 3 off | the card names only cases a road would ask about |
| E13 | key list > 8 | today's cut "and N more" | a cut list says it is cut (L1) |
| E14 | declaring cases = `ROLE_NAMED` (3) / 4 | AT: three ids named; BEYOND: "the 4 cases" | never names an id the card's lines do not explain |
| E15 | the builder raises while adding | no finding appended, guard not set, no mark: the step is `unavailable`; road 2's call retries once | at most one successful card per rehearsal |
| E16 | `project_root is None` | all three roads return; no decision | unchanged |

Reuse in a more consequential role: `default_login_needed` (advice -> it now also gates whether the card exists). Its error direction is
toward True (a question too many); that direction is kept: every exception, unreadable plan/case, unknown disposition stays "needed".
Adversarial inputs that must stay on the asking side: a broken `test-plan.json`, a case whose preconditions do not parse, a disposition
outside `contract.DISPOSITIONS`, an unreadable registry - each yields `needed` True (pinned by `test_login_need.py`, unchanged).

## 5. Builder node PK2-6a

given: this spec (§2-§4); the finding `C:\QAFactory\forge-repo\plans\piles\project-knowledge\findings\20261111-default-ucherka-tri-karty-vne-invarianta.md`; `scripts/gate_preflight.py::Rehearsal._probe_actor`, `::Rehearsal.check_s5_credentials`, `::Rehearsal.check_case_preconditions`, `::Rehearsal._write_role_accounts`, `::default_login_needed`, `::case_account_roles`, `::integration_login_keys`, `::run`; `scripts/manual_capture.py::_default_keys`; the helpers `story`, `pc`, `override`, `found` and `test_run_cards_the_role_before_the_sign_in_probe` in `scripts/tests/test_gate_role_accounts.py`
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\gate_preflight.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_gate_role_accounts.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_gate_preflight.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json
non-goals: no change of `default_login_needed`'s rule (PK0-5/PK2-15); no S6 change (`Driver.stand_login_problem`); no registry key or pipeline field (F3); no gate_brief renderer change; no edit of `test_manual_actor.py` (quarantine) or any other test file; `test_gate_preflight.py` gets only the `NEW_CHECK_FUNCTIONS` entry
handoff: the branch + report: the sites list of `is_default_account` (before/after), the witness tail, `tests not written:` lines if over budget, `red-before:` for row R10 (the latent defect: `red-before: <cmd> -> <tail>` on test_gate_role_accounts.py before the code)
edges: §4 E1-E16 of this spec, each with its invariant (inline there; the table rows below pin E1-E5, E7, E9, E14)
DoD: `python -m pytest ai-packages/qa-factory/scripts/tests/test_gate_role_accounts.py ai-packages/qa-factory/scripts/tests/test_login_need.py ai-packages/qa-factory/scripts/tests/test_not_needed_role.py "ai-packages/qa-factory/scripts/tests/test_gate_preflight.py::test_c3_the_new_checks_speak_in_the_storys_words" "ai-packages/qa-factory/scripts/tests/test_gate_preflight.py::test_the_credentials_of_the_next_stage_name_the_file_that_reads_them" "ai-packages/qa-factory/scripts/tests/test_gate_preflight.py::test_gw1_27_k2_default_is_the_stands_default_account" "ai-packages/qa-factory/scripts/tests/test_judgment_census.py::test_c1_every_unit_has_a_row_and_every_row_a_unit" -q`
siblings: S6 `story_run.Driver.stand_login_problem` (AR-19 twin, reads the same `default_login_needed`; unchanged); PK0-4 role card (`check_role_accounts`; the same mark dict, unchanged behaviour); PK0-9 `not_needed` branch of `_probe_actor` (unchanged, pinned by test_not_needed_role.py)
designer: C:\QAFactory\forge-repo\docs\tasks\specs\20261119-pk2-6-default-account-card.md
test: ai-packages/qa-factory/scripts/tests/test_gate_role_accounts.py::test_default_account_reaches_one_card (new table, rows R1-R14 below, top-down) | expected from: §3-§4 of this spec; the finding's "Ожидаемое поведение"; t-2142 PK0-4 invariant (spec :531-533)
test: ai-packages/qa-factory/scripts/tests/test_gate_preflight.py::NEW_CHECK_FUNCTIONS gets `check_default_account` (the FR-6 scan reaches the moved literal; witnessed by test_c3) | expected from: AR-16, FR-6

Work items:
1. Module level: `DEFAULT_ACCOUNT = "default"`, `is_default_account(spec) -> bool` (`str(spec).strip() == DEFAULT_ACCOUNT`), `DEFAULT_MARK`,
   `DEFAULT_ACCOUNT_BLOCK`. Wire the existing exact comparisons to it: `default_login_needed` (the `any(...)` of rule (a)),
   `Rehearsal._actors_of_manual_cases` (`real = ...`), `Rehearsal._stand_account` (`if role == "default"`), `Rehearsal._precondition_door`
   (`!= "default"`); `config_contract.reserved_role` stays as it is (other file, other set).
2. `Rehearsal.__init__`: `self._default_decided = None`, `self._default_card_done = False` (comment beside the PK0-4 lines).
3. `_default_account_decision`, `_default_account_card`, `check_default_account` as §3; register the step in `run` between
   `check_role_accounts` and `check_actor_sign_in`; its docstring states the POSITION invariant.
4. `check_s5_credentials`: `needed` from the decision; the login `missing`/`add` block replaced by the builder call at the same place.
5. `_probe_actor`: the lookup key and the `"accepted"` note (§3 road 1).
6. `check_case_preconditions`: the filter (§3 road 3), comment updated (PK0-4 + PK2-6).
7. `judgment-census.json`: one row `{"file": "gate_preflight.py", "function": "check_default_account", "class": "safety", "roles": ["conductor"], "owner": "intent"}` in file order.
8. `test_gate_preflight.py`: `"check_default_account"` added to `NEW_CHECK_FUNCTIONS`.

## 6. The test table (one parameterised test, strongest first)

Place: `scripts/tests/test_gate_role_accounts.py` (keep, scenario, "one card per (stand, role) at gate A" - the default account is the same
behaviour; fast, not on the slow list). One world builder per row through the file's `story()` (cases with `pc(n, "default", remedy=...)`),
run through `GP.run(task)` with every `check_*` except `check_role_accounts`, `check_default_account`, `check_actor_sign_in`,
`check_s5_credentials`, `check_case_preconditions` replaced by a no-op (the pattern of `test_run_cards_the_role_before_the_sign_in_probe`);
road-1 rows set `_actors_of_manual_cases` to `{"default": [...]}`; a row where the sign-in is tried stubs `Rehearsal._probe_sign_in`
(no browser). Count = PERSON_DECIDES findings whose subject is the default account, over ALL checks.

| row | world | expected |
|---|---|---|
| R1 | roads 1+2+3 at once: `user_key: LOGIN_U`, `secret_keys: [LOGIN_P, EXTRA]`, empty env file; TC-1 (item with remedy) and TC-2 (no remedy) declare `default`; manual actor `default` on TC-1 | exactly 1 finding: check `s5_environment`, id `s5_environment-default-login`, keys LOGIN_U, LOGIN_P, EXTRA, cases [TC-1, TC-2]; 0 `actor_sign_in`, 0 `case_preconditions` findings, 0 `case`-scope stand gaps; the probe note present |
| R2 | road 3 only: two declaring cases, no `user_key` | 1 card naming AUTH_USERNAME, AUTH_PASSWORD and both cases (today: 0 road-2 + 2 per-case) |
| R3 | road 1 only: manual actor `default`, no case file item | 1 card; note "waits for the card"; probe row `not_proved` |
| R4 | road 2 only: `user_key` set and absent, automate row, no declaring case | 1 card, no cases phrase, no AUTH_* keys (E9) |
| R5 | control: R1 world with all keys in the env file, sign-in stubbed `signed_in: True` | 0 findings about `default` |
| R6 | R1 world + override on the card's door (`accept`) | 0 PERSON_DECIDES about `default`; mark `"accepted"`; road-1 note "you accepted" (E5) |
| R7 | R6 with the override `revoked_at` set | exactly 1 card (E3) |
| R8 | R1 world, `_loaded_env_files` raises | no mark, no `s5_environment-default-login`; at least one FACTORY_DEFECT; `can_proceed` False (E2) |
| R9 | R1 world, `check_default_account` replaced by a no-op (the step absent) | exactly 2 PERSON_DECIDES about `default`: road 1's own `actor_sign_in` card and the `s5_environment-default-login` card (raised by road 2's builder call); 0 `case_preconditions` (road 3 defers to the raised card) (E1) |
| R10 | product role `Default` (TC-3) + reserved `default` (TC-4), no keys | role card `RA-dev-default` holds [TC-3] only; the default card holds [TC-4]; 2 cards (E7; red before the code) |
| R11 | keys present, sign-in stubbed `kind: not_landed`, + accept override of `DEFAULT_ACCOUNT_BLOCK` | exactly 1 finding: `actor_sign_in` "did not let it in"; no login card (E4b) |
| R12 | ` default ` with spaces in TC-1 | same as R2 for one case (E8) |
| R13 | 3 declaring cases / 4 declaring cases | AT: three ids named; BEYOND: "the 4 cases" (E14) |
| R14 | every text of R1 | `human_text.problems(kind="question")` empty for the card's message + fix |

The builder writes rows top-down until test lines reach code lines and reports the rest as `tests not written: <row> -- over budget`.

## 7. Readers of every touched file

No `tools/owns_readers.py` block was attached to the brief; the designer has no shell. The Lead runs:
`python -B tools/owns_readers.py --paths ai-packages/qa-factory/scripts/gate_preflight.py ai-packages/qa-factory/scripts/tests/test_gate_role_accounts.py ai-packages/qa-factory/scripts/tests/test_gate_preflight.py ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json --names check_s5_credentials _probe_actor check_case_preconditions run _account_carded check_default_account is_default_account --readers`
and attaches the block before dispatch (label: `estimate` until then). Hand reads done (Grep tool, counts with positive controls):

| reader | what it reads | verdict |
|---|---|---|
| `scripts/tests/test_login_need.py::test_gate_a_note_when_not_asked` | `check_s5_credentials` alone: "keys not set" finding when needed, the note when not | unchanged: road 2 alone still raises the card through the builder |
| `test_gate_preflight.py::test_the_credentials_of_the_next_stage_name_the_file_that_reads_them` | full `run`: one `s5_environment` finding, names AUTH_PASSWORD not AUTH_USERNAME, fix names `harness/.env` | unchanged (prefix and fix kept); in the DoD |
| `test_gate_preflight.py::test_gw1_27_k2_default_is_the_stands_default_account` (`_gw_findings` runs only `case_preconditions`) | road 3 alone asks one question for `default` | unchanged (mark absent, E1); in the DoD |
| `test_gate_preflight.py::test_c3_...` / `NEW_CHECK_FUNCTIONS` / `message_literals` | the literal of every person message of listed functions | changes in this node (item 8) |
| `test_gate_preflight.py` probe tests K-P1..K-P5 (`_probe_story`, roles `user`/`admin`) | `actor_sign_in` findings for roles | unchanged (no `default` actor) |
| `test_gate_role_accounts.py` :237, :300 (`_account_carded == {...}`), :258-282 (probe deferral, `run` order with all other `check_*` nulled) | the mark dict for roles; the step list | unchanged: no default in those worlds; the new step is nulled by the `dir()` loop |
| `test_not_needed_role.py` (PK0-9 branch of `_probe_actor`, road 3 filter) | `not_needed` mark | unchanged; in the DoD |
| `scripts/gate_brief.py::_blocked_form` (:3042) | offers "accept as blocked" when a `case_preconditions` PERSON_DECIDES finding exists | changes in behaviour only: a story whose only per-case question was `default` no longer offers that line (the card's own door replaces it) - same as PK0-4 for roles |
| `judgment-census.json` + `test_judgment_census.py::test_c1` | every `check_*` unit has a row | changes in this node (item 7); c1 in the DoD |
| `references/config-keys.json` `needed_by` (:743 `gate_rehearsal`, :784 `environment`) + `test_config_migration.py` R3 | each listed function still names its key | unchanged: `check_actor_sign_in`, `check_case_preconditions`, `check_s5_credentials` keep their key reads |
| `tools/`, `.githooks/`, `.claude/agents`, `.claude/hooks` | the three function names | none: Grep `check_s5_credentials|_probe_actor|check_case_preconditions` over `tools/` = 0 (control: `gate_preflight` over `tools/` = 9, all `language-sites-baseline.json`, unrelated rows) |
| `scripts/test_manual_actor.py` | `manual_capture.resolve_actor` for `default` | not a reader of the changed code; in QUARANTINE (test-layers.json :10018) - not run, not edited |
| driver / `story_run.py` | `s5_environment` findings | none: Grep `s5_environment|keys not set` over `scripts/*.py` hits only gate_preflight.py and tests (control: gate_preflight.py 5) - see F1 |

## 8. Forks (for the Lead)

- **F1 - which card is the ONE card.** (a) road 2's login card (check `s5_environment`), emitted early by the new step [recommended:
  it already names the env file, it is the only road that also fires with no declaring case, PK0-5's site]. Cost, measured: no driver
  reads `s5_environment` findings, so an ACCEPT of this card does not carry the declaring cases as stand gaps (today an accepted per-case
  `default` stand-gap card is carried by the B-414 road); the cases then meet S6's `stand_login_problem` (same rule) - whether that is a
  second stop is an `estimate`; the Lead checks with `Grep "stand_login_problem" ai-packages/qa-factory/scripts/story_run.py` and reads
  its refusal. If it is a second stop, take (b). (b) a stand-gap row of a new scope (or `role` with variant `default`) holding the cases,
  carried by the driver - costs a renderer variant in `gate_brief.py`, new `_role_options`/`_role_lead` text and remedy (default keys are
  config-named, not "two variables for the role"), one more owned file. (c) the probe card - fires only for manual-agent; rejected.
- **F1b - emission site.** (a) new step `check_default_account` in `run` before road 1 + builder fallback in road 2 [recommended: the
  card exists before any reader defers, by construction, like PK0-4; costs a census row]. (b) the idempotent builder called at the head of
  each road, no new step - no census row, but `test_gw1_27_k2` (road 3 alone) would see an `s5_environment` card instead of its own: one
  slow-file test edit, and the card is raised inside another step's attribution.
- **F2 - the key set of the one card.** (a) union of both readers always when needed (toward asking, but asks AUTH_* on automate-only
  projects that never read them); (b) only `_default_keys` (loses `extra_keys`/extra secrets road 2 asks today); (c) exactly what today's
  firing roads ask: road 2's set when needed, plus `_default_keys` when a declaring case exists [recommended: no new question, no lost one].
- **F3 - where the decision lives across stories.** (a) in-run mark only; the persistent carriers stay the env file and the story's
  `stage_overrides` [recommended: `default` is reserved and never written to the registry (HF8-9); a cross-story "no default login" word
  would change `default_login_needed`'s rule - a non-goal]. (b) `project_knowledge` new key (e.g. `environments.default_login`) - costs a
  catalogue row, a writer command, a `design/state-exits.md` row (AR-25), and touches the PK0-5 rule. (c) a `pipeline.json` field - a
  second writer of `pipeline.json` (AR-14) or a `stage_done` change.
- **F4 - a door word on the merged card.** (a) add `waiver_command(DEFAULT_ACCOUNT_BLOCK)` [recommended: roads 1 and 3 had a word door; without
  it "accepted" and "revoked" have no carrier but the gate approval]; (b) keep today's road-2 fix only (approval words) - E3/E5 then
  happen only through the whole-gate approval.
- **F5 - words recorded on the retired roads' cards before this change.** (a) they do not pass the merged card; asked once more
  [recommended: an accept of "sign-in of the account default" was about manual sign-ins, narrower than the default login of S5 - passing
  the wider card on it is a word about one block passing another]; (b) list the old block among the card's `waives` as an alias.
- **F6 - the brief's DoD names `test_manual_actor.py`.** It is in quarantine (test-layers.json :10018, cohort 8073673) and does not test
  the changed code; TESTING.md :107 forbids running or editing it. Replaced by `test_gate_role_accounts.py` (the PK0-4 home) and
  `test_not_needed_role.py`. Lead confirms.

## 9. Small choices closed by the designer

- The mark key is a tuple constant in the existing dict (one mechanism with PK0-4, no collision) rather than a second attribute.
- The card keeps check id `s5_environment` and gets `subject="default-login"` (stable id `s5_environment-default-login`; ordinals of the
  other `s5_environment` findings no longer depend on order).
- Road 3 drops filtered `default` items silently (the card names the cases), as PK0-4 does for roles.
- `state == "error"` sets no mark (each road keeps its own factory finding) rather than one merged factory finding.
- Helper names avoid the census `UNIT_NAME_RE` (`_default_account_decision`, `_default_account_card`); only the run step is a unit.
- `is_default_account` stays inside `gate_preflight.py`; `config_contract.reserved_role` is not rewired (other file, other set).

## 10. Contradictions and notes for the Lead

- The brief's line numbers (scout t-1573 at 6266f2b0) are stale against the tree read here; §2 gives the current ones.
- The brief asks a test "for each road"; road 2 alone has no deduplication to test (it was already one card) - R4 pins that it stays one
  card with no new keys.
- `test_judgment_census.py` and `test_gate_preflight.py` are on the slow list (slow_tests.json :68, :44): only node ids are in the DoD.

## 11. Reading trail

- Read: the finding (whole); `gate_preflight.py` :680-799, :1555-1584, :1600-1719, :2315-2344, :2370-2469, :2500-2559, :2560-2844,
  :4287-4336, :4680-4809, :5340-5397, :5461-5485, :5547-5786, :6160-6198; `manual_capture.py::_default_keys` (:772-776);
  `integration_login_keys` (:1262-1266); `_role_form` (:1155-1158); `config_contract.py::reserved_role` (:212-216);
  `project_knowledge.py` :227-338, :1171-1211; `environment_record.py` :118-147 (`KEYED_CHECKS` = env/http/integration: a `stand_account`
  item is never covered by the environment record); `test_gate_role_accounts.py` :1-110, :230-309; `test_login_need.py` :195-209;
  `test_gate_preflight.py` :1572-1604, :3705-3734, :3850-3880, :5665-5690, :5699-5724, :6040-6155; `gate_brief.py` :3030-3050;
  `docs/TESTING.md` :75-164, :213-251; `design/architecture.md` :33-72, :173-184, :200-224, :295-334; t-2142 spec :525-533;
  `test-layers.json` :1-60, :2085-2099, :2884-2895, :3400-3403, :10015-10025; `test_judgment_census.py` :10-34.
- Greps (Grep tool): `_account_carded|...` over the package (counts: gate_preflight 12, test_gate_role_accounts 3, test_login_need 1,
  test_story_run_s6_t292 1 - an unrelated S6 string); SIBLING_MAP for the five symbols = 0 (control: `project_knowledge|gate_preflight`
  = 15); census rows for private helpers = 0 (control: `check_role_accounts` row found, same form); slow_tests.json: test_gate_preflight
  57.0, test_judgment_census 96.9, test_gate_role_accounts / test_login_need absent.
- Size of this file: `estimate` ~32 KB (under the 40,000-byte cap); the Lead measures with
  `python -B -c "import os,sys;print(os.path.getsize(sys.argv[1]))" docs/tasks/specs/20261119-pk2-6-default-account-card.md`.

## Lead decisions (19.11.2026, accepting t-1579)

- F1: road 2's login card is the one card. Edge the builder must measure first: after an accept of that card, does S6 `stand_login_problem` ask the default account again? One table row pins it. If it does ask again, STOP and return the question (no second carrier invented).
- F1b: the guarded card builder is called at the head of each road (no new run step). F2: exactly the keys the roads ask today. F3: the in-run mark. F4: yes, a word door. F5: accepted (older accepts on retired cards do not pass; one changelog line names it). F6: DoD uses test_gate_role_accounts.py and test_not_needed_role.py by node id.
- R10 (`_role_form("Default")` collides with the reserved default) is fixed inside the node, as drafted.
