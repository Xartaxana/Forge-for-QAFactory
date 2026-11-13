# FV1-18 — the selector contract never stops the automator's run, and the factory can produce "verified" itself (DRAFT)

Status: DRAFT by the designer for the Lead (13.11.2026); Lead fork decisions in §9a (t-482); fix round after the critic on
the plan in §9b (t-493 verdict, fix round t-500). Forks still open are in §9 (F6, F7) and are NOT decided here. This spec
changes the MEANING of a gate (a refusal becomes a report line), so PROJECT.md "package change" item 6 applies: the premise in
§0.2 is measured (§9a), and the text passes a critic-on-plan before any builder (CLAUDE.md rule 3).

Pile / node: `live-run-fvf` / batch 1 / FV1-18 (row `batch-1-live-run-fvf.md:50`, declared files `scripts/execution_request.py`,
`scripts/profile_contract.py`, `scripts/onboarding_probe.py`). Finding:
`plans/piles/live-run-fvf/findings/20261112-kontrakt-selektorov-nikogda-ne-proveren.md` (worktree `findings-1413c`).
All package line numbers below are from `C:\QAFactory\forge-repo\.claude\worktrees\read-main\ai-packages\qa-factory\` (origin/main).
`PKG` = `ai-packages/qa-factory`.

---

## 0. Facts read first (carrier:line)

### 0.1 Who writes, who reads, who refuses

| Fact | Carrier |
|---|---|
| The refusal: for every behavioural purpose, `command.selector_contract_verified is not True` -> "behavioral command requires a verified adapter selector contract" | `scripts/execution_request.py:293-296` (`validate_request`) |
| The `--mine` producer of that field: a pytest command gets `True` by its NAME ("a node id as an argument IS pytest's contract"); any other command gets `profile_contract.selectors_verified(profile_doc, project_root)` — but ONLY when the field is not already in `command` | `execution_request.py:3668-3673` (`build_mine_request`) |
| The pytest test of the old producer reads the REQUEST's command (the one that runs), not the profile's: `pytest_run = is_pytest_command(command.get("argv"))`; `pytest_run` is also read at `:3473`, `:3475` | `execution_request.py:3465` |
| A command copied from a precedent job keeps every key but `selector_args` — so a precedent's old `selector_contract_verified` survives and line 3671 never recomputes it | `execution_request.py:3404-3405` |
| A precedent's command is copied only when its argv equals the profile's one-test argv with placeholders dropped and its `env` equals the profile's (or either side is unreadable: "not compared", copied as is) | `execution_request.py:3378-3416`; `_profile_argv` `:1804-1812`, `_profile_env` `:1815-1818` |
| A command built from the profile drops `<placeholder>` words (`one_test_argv(profile, drop_placeholders=True)`) and refuses a foreign `env` | `execution_request.py:1821-1831` (`_command_from_profile`) |
| `execution_request` imports `profile_contract` at module top, so `profile_contract` may import `execution_request` only inside a function (cycle) | `execution_request.py:17`; the existing lazy import at `:3672` goes the other way |
| The typed-request road (`run_suite.py --request`, the door the guard sends a role to) pre-fills `"selector_contract_verified": True` in the template the role copies | `scripts/run_suite.py:2443-2453` (`REQUEST_TEMPLATE_FIELDS`, `command` entry); guard door `scripts/guard_pre_tool.py:2447-2449` |
| The ONE answer `selectors_verified(profile, root)`: hand literal `selectors.verified` wins both ways (a non-bool literal is neither and falls through to the record); else `launch_check.runner_identity(argv)["selection"]` must exist AND `onboarding_probe.earlier_proof(root, profile_id, argv)["state"] == "same_command"`, with `argv = onboarding_probe._one_test_argv(profile)`; a `selectors` that is not an object raises inside and gives False; error direction False | `scripts/profile_contract.py:343-374` |
| `_one_test_argv` = `profile_contract.one_test_argv(profile)[0]`: the argv WORDS only (placeholders kept, `env` NOT included) | `scripts/onboarding_probe.py:209-211`; `profile_contract.py:333-340` |
| `command_identity(spec)` = argv words + `"\u0000env"` + `NAME=value`; a FOREIGN `env` (not an object, a bad name, a value other than `{report_path}`) reads as NO env there — `command_env` returns `({}, problem)` | `profile_contract.py:320-330`, `:299-317` |
| The record `qa-factory/state/reporter-rehearsals.json` is written by gate A (`Rehearsal._record_rehearsal`) with `argv = self._rehearsing_argv = command_id`, where `command_id = command_identity(spec)` | `scripts/gate_preflight.py:3525-3534`, `:3825`, `:3848`, `:3568` |
| The onboarding probe overrides the row with `argv_digest(self.proved_argv)`, `proved_argv` = the `argv` passed to `_rehearsal_key` = the same `command_id` | `onboarding_probe.py:336-337`, `:352-358`; `gate_preflight.py:3834` |
| `argv_digest` documents that callers pass the IDENTITY (EP1-22 B-2); gate A's own reader passes the identity | `onboarding_probe.py:366-370`; `gate_preflight.py:3614`, `:3947-3954` |
| The Playwright shape sample carries `env: {"PLAYWRIGHT_JUNIT_OUTPUT_NAME": "{report_path}"}` on `one_test`; the Playwright report cure adds that same `env` | `references/profile-shape.json:11`; `references/report-cures.json:69-72` |
| `earlier_proof` returns `same_command` / `command_changed` / `none` / `unreadable` and the newest row's day; it does not read a row's `tests` | `onboarding_probe.py:373-394` |
| Onboarding DOES rehearse the command: `onboard_apply.py --apply` runs the probe itself after writing the profiles; the skill re-runs `onboarding_probe.py --probe-profiles` after a "no" | `skills/qa-onboarding/phases/p4-generate.md:191-205` |
| Only one run form carries a `selection` row in data: `playwright-test`; the `pytest` row carries `id`, `argv`, `diagnostics` only | `references/launch-causes.json:30`, `:35-36`; reader `scripts/launch_check.py:176-204`, `:701-732` |
| `hooklib`'s run-forms loader keeps only `id`, `argv`, `diagnostics`, `negators` of a row and drops any other key; `launch_check._selection_rows` re-reads the raw file "for the one key it does not" | `scripts/hooklib.py:1216-1229`; `launch_check.py:176-181` |
| A wrong True gives no pass in S5: `run_suite.build_run_block` binds every selected instance by EXACT `report_test_id`; no row -> `not_run`, reason "report row missing"; more than one -> `not_run`, "report identity is ambiguous"; a contract with a `file` goes through `_file_verdict`: no row -> `not_run`, "id not in report" (`reason_code` `id_not_in_report`), ambiguous -> `not_run` | `run_suite.py:469` (`build_run_block`), `:505-539`, `:681-692` (`_file_verdict`); `validate_request` still refuses a selected instance without `instance_contracts.<id>.report_test_id` (`execution_request.py:336-355`). The red probe's own binder is `red_sandbox.bind_row` (`red_sandbox.py:1045-1070`) |
| The reuse identity of a request: `request_digest` hashes the whole request (the `command` included) minus four keys; `_match`/`covered` do not compare the whole command | `execution_request.py:373-380`; `:2045-2100` (critic t-493, M1) |
| The second consumer of the same answer: the mutation probe's shape check R6(a) refuses when `selectors_verified` is False, sentence "profile <id> does not say its selector contract is verified (selectors.verified in qa-factory/config.json: the onboarding's gap)" | `scripts/probe_by_code.py:2749-2794` (sentence `:2787-2789`) |
| Keep tests that read that sentence: `"selector contract"` (`test_probe_fix_round.py:38`, keep `data_join`, `test-layers.json:3699`); `"selector contract is verified"` and `"selectors.verified"` (`test_probe_by_code_languages.py:1374`); `"selector contract"` (`:1891`; keep `gate_named`, `test-layers.json:3648`) | carriers named |
| The probe-walk World's config is `{}` (`ProbeCtx(..., {}, ...)`), so its profile has no command | `scripts/tests/test_probe_walk.py:55` |
| `executor_gap`'s profile lookup is inline code, no helper; `executor_gap` is called in `main` and witnessed by run_suite's own selftest and the keep test `test_handed_to_person.py` (`detector`, covers `run_suite.py`, `test-layers.json:2215-2233`) | `run_suite.py:1575-1598` (lookup `:1585-1586`); calls `:2500-2505`, `:2884`; `test_handed_to_person.py:240-251` |
| The gate registry describes `validate_request` as deciding "... selector contract ..." | `references/gate-registry.json:95` |
| The P31 census already lists this branch: "selector contract verified — pytest: a node id ...; others ask `selectors_verified` — same outcome but with a different gate" | `docs/tasks/specs/reports/t-2046-language-exceptions-census.md:63` (M4) |
| The first look records PAGE locators (`locator.what/selector/seen`), it never runs the test command | `scripts/first_look.py:8-17`, `:65`, `:289-291` |
| The Lead's own correction: profile `selectors` = how the RUNNER selects a test, not page locators; the first look cannot be its producer | `docs/tasks/specs/20261113-plan-fabrika-ne-huzhe-agenta.md:355-358`; FV1-29 finding lines 21-22 |

### 0.2 What actually broke (cause) — the premise (MEASURED, §9a)

The finding says the record and the check compare "different forms of the command (`_one_test_argv` gives a template with
`<test-file>`)". The code says otherwise: both sides keep the `<test-file>` placeholder (neither passes `drop_placeholders`).
The sides differ by the **`env` part of the identity**: every writer of the record digests `command_identity(spec)` (argv +
`env`), `selectors_verified` digests the argv words alone. For any profile whose `one_test` sets `env` — the shipped Playwright
shape does — a fresh, proven rehearsal reads `command_changed` forever. That is exactly the observed state (`proven` probe,
then `earlier_proof -> command_changed`). Measured on the arm's config (§9a): `env` IS set; the critic confirmed the cause (K1).

### 0.3 What "used to work" was

- CART-1 (package 0.10.6, MyBooks, Playwright through a wrapper `node scripts/run-playwright.mjs`) ran its S5 windows with
  `selector_contract_verified: true` in requests the ROLE wrote from the template: `scripts/tests/fixtures/stories/cart-1/work/
  requests/s5-2-initial.json:123-134` (file names `s5-*-initial.json`, not the `mine-...` names `write_mine_request` gives,
  `execution_request.py:3877-3887`), while profile `web` had no `selectors.verified`
  (`plans/piles/execution-probes/findings/20261031-proba-chuvstvitelnosti-ne-chitaet-playwright-ts-18-iz-18.md:15`).
- `selectors_verified` arrived in 0.10.8 (EP1-36 item 8): `CHANGELOG.md:1264`. Since then `--mine` asks it; the template road
  still writes `True` by hand.
- So the "regression" is: in 0.11.0 the automator used `--mine` (the road the factory now prefers), which computes the answer,
  and the computed answer cannot become True for an `env` command (§0.2) nor for a wrapper script (no `selection` row,
  `test_profile_contract.py:185-187`). The template road would still pass. **The exact commit that made `--mine` refuse could
  not be established: this designer has no git tool (Read/Grep/Glob only).** The CHANGELOG line and the fixtures are the
  carriers; the Lead may pin the commit with `git -C <read-main> log -S "selectors_verified(profile_doc" -- PKG/scripts/execution_request.py`.

### 0.4 Contradictions in the brief / plan (reported, not resolved)

1. Brief: "the selectors are gathered by the first-look runner". The Lead's plan (`20261113-plan...md:355-358`) and the code
   (`first_look.py:65`, `profile_contract.py:351`) say the profile's selector contract is test SELECTION by the runner; the first
   look records page locators and never runs the test command. -> fork F1 (decided (a) in §9a until the owner's word).
2. Brief: "onboarding never rehearses the command". It does (`p4-generate.md:191-205`). Why the LR2-1 onboarding of 17:22 left
   no usable record is **not established** (the arm's `state/` was not read): either no row was written (state `no_test` /
   `not_checked` / `--no-probe`), or a row was written and read as `command_changed` by the same `env` mismatch.
3. Plan table row (`20261113-plan...md:323`) says "the first look writes selectors in a readable form"; the same plan's
   correction at `:355-358` contradicts it.
4. The finding's quoted refusal text "no verified adapter selector contract; profile selectors empty; settle by declaring
   selectors ..." is not a package string: a case-insensitive Grep for `selectors empty|declaring selectors` over `PKG` finds
   nothing, while the same tool and flags find `selector contract` (positive control: `execution_request.py:296`,
   `profile_contract.py:344`). It is the role's or the conductor's paraphrase of `execution_request.py:296`.
5. (fix round) The critic's hand-back says T5 §5.4 rows 11, 16 and 18 shift after N2. Read: row 11 cites `:132-139, 298, 304`
   and row 18 `:296-330` (both after the deleted `:295-296`, shift by −2); row 16 cites `:207-264`, ABOVE the deletion, so
   N2 alone does not shift it. Recorded in §8 as "re-read against the merged file", not resolved here.
6. (fix round) The critic's item D6 and the Lead's D6 speak of the literal "selector contract is verified" at
   `test_probe_fix_round.py:38`; that line reads only `"selector contract"`. The full literal is read at
   `test_probe_by_code_languages.py:1374`. N3 keeps both (§5 N3).

---

## 1. Architecture, principles, owners (designer rule 1)

### 1.1 AR-n touched, and the change check each demands (written into the DoD of §6)

| AR | How this spec touches it | Change check (DoD) |
|---|---|---|
| AR-7 (code is an instrument, never a substitute) / AR-2 | the selector question stops being a stop; code reports it, the role decides what to do with rows that come back `not_run` | N2 row R-N2-1: `validate_request` resolves a request with an unverified contract; R-N2-4: the note is printed for it |
| AR-13 (a fact with a reader function is read only through it) | `selector_contract` becomes the one answer; `selectors_verified` its bool view; the digest input becomes `command_identity`, the one input every writer uses; the "same command as the profile's" test reads through `one_test_argv(..., drop_placeholders=True)` and `command_env`, the readers `_profile_argv`/`_profile_env` already use | R-N1-1/2/9; grep in the critic's mechanical layer: `selectors_verified\|selector_contract` sites in `scripts/*.py` = `profile_contract.py`, `probe_by_code.py`, `run_suite.py`, `execution_request.py` only |
| AR-15 (one survivor, wired everywhere) | both roads (`--mine`, `--request`) get the answer from one site in `run_suite.main` (F2 = B); the profile lookup by `profile_id` becomes ONE helper `run_suite.request_profile`, called by `executor_gap` and by the note | R-N2-2, R-N2-5 (helper, both callers) |
| AR-22 (every field produced has a reader) | `selector_contract_verified` loses its only reader (the refusal) -> dropped from new requests (F2 = B, §9a); no new key is added to `earlier_proof` (D1) | R-N2-3: no new request carries a field nothing reads |
| AR-28 (an unknown never becomes a pass) / AR-25 | an unverified contract becomes neither a pass nor a stop: a selected test the runner did not run comes back `not_run` (reason "report row missing", or "id not in report" for a contract with a `file`) under its report id; the note names the door | R-N2-4: an instance whose report row is absent is `not_run` with reason "report row missing", never `passed`, on a build of a request that carries no `selector_contract_verified` |
| AR-9 (a refusal names a door its receiver can use) | the probe's R6(a) door names the onboarding probe command that writes the record (F3 = a, N3); the note names the same command | R-N2-4 (note text), R-N3-1 |
| AR-29 (a code check judges data) | `validate_request` keeps judging shape (selector_args, report ids); it stops judging a property it could never establish | R-N2-1 negative controls |
| AR-1 (closed variety is a data row) | the pytest branch by name moves into `selector_contract` (N1, one place) and then becomes the data key `selection_by_node_id` of the `pytest` run form (N4, F4 = a) | R-N4-1..3; census row M4 closed by N4 |
| AR-17 (a state with no move goes to the conductor) | after the change no state here lacks a move, so no conductor call is added (P22 holds: nothing stops) | none beyond R-N2-1 |

FR walked by section (builder repeats in the report): A (FR-1, FR-2, FR-4, FR-5, FR-59), C (FR-11, FR-13, FR-14), D (FR-17,
FR-18), E (FR-41), G (FR-30, FR-32, FR-47). B: no text to a person changes (notes go to the role; no `human-questions` text).

### 1.2 Every check added or altered: owner and census class

| Check | Change | Owner it serves | Census class / row |
|---|---|---|---|
| `execution_request.validate_request` — the selector-contract refusal (`:295-296`) | REMOVED | data (it never judged data it had; it judged a fact no producer could make) | unit stays `safety`, `owner: data` (`judgment-census.json:312`); the unit keeps other refusals, so no row change; no ratchet raise |
| `profile_contract.selector_contract` (new) / `selectors_verified` | ALTERED reader (identity digest; foreign `env` -> `no_command`; the run's command judged when given) | data | not a check unit (returns data, never raises): no census row |
| `run_suite.main` — the `SELECTORS (note)` line (`selector_note`) | ADDED report line, never a refusal | data | not a refusal site: no census row |
| `run_suite.request_profile` (extracted from `executor_gap`) | MOVED lookup, same answer | data | not a check: no census row |
| `probe_by_code.run_shape_checks` R6(a) | refusal UNCHANGED; its input answers True in more true cases (env commands with a proof, pytest-shaped commands); its sentence gains the `why` and the door (N3) | data | `xref`, `owner: data` (`judgment-census.json:757`), unchanged |
| `launch_check.runner_identity` — `node_id_selection` (N4) | ADDED data field, read from a data key | data | not a refusal site: no census row |

No judgment (role) or intent (person) check is added. The person decides nothing new.

---

## 2. The mechanism

1. **The answer is one function and says why.** `profile_contract.selector_contract(profile, root, command=None) ->
   {"verified": bool, "state": <word>, "why": <sentence>}`. `command` is the command that RUNS (a request's `command` object)
   when there is one; `None` means "judge the profile's `commands.one_test`" (the probe's R6(a) and `selectors_verified`).
   `selectors_verified(profile, root)` returns `selector_contract(profile, root)["verified"]` (signature and every existing
   caller unchanged). `execution_request` is imported INSIDE the function (it imports `profile_contract` at module top, §0.1).
   States, in this order of precedence (the positional invariant: the hand first, then the command, then the record):
   1. `no_command` when the profile is not an object -> False.
   2. `hand_unreadable` when `selectors` is present and not an object (`"yes"`, a list) -> False.
   3. `hand_false` (`selectors.verified is False`) -> False; `hand_true` (`is True`) -> True. A `verified` literal that is not a
      bool (`"true"`, `1`, `null`) is "not said": it is not read as either and the order goes on; the final `why` gains the
      clause "selectors.verified is not true or false and was not read" (today's behaviour, `profile_contract.py:359-363`).
   4. The command judged: `command` when given, else the profile's `one_test` spec (`profile_command(profile, "one_test")`).
      `no_command` when there is no root, the spec is absent or not an object, its argv is empty or unreadable
      (`command_argv`), or its `env` is FOREIGN (`command_env` returns a problem, D5) -> False. Never a match on the argv
      alone: a foreign `env` reads as no env inside `command_identity`, so it would match an older row of the same argv.
   5. `node_id` — the judged command's argv words are pytest-shaped (`execution_request.is_pytest_command`, moved here from
      `build_mine_request:3669-3670`; after N4 the data key, §5 N4) -> True.
   6. `no_selection_form` — `launch_check.runner_identity(<argv words>)["selection"]` is None -> False; `why` carries the
      `problem` words when the table could not be read.
   7. Only when `command` was given: `command_not_profile` — the run's command is not the profile's one-test command: its argv
      words differ from `one_test_argv(profile, drop_placeholders=True)[0]`, or its `env` (through `command_env`) differs from
      the one-test `env` (absent and `{}` equal), or the profile's `one_test` is absent or unreadable -> False. This is the
      comparison `build_mine_request` already calls "the same command" (`:3388-3389`), through the same readers.
   8. The record: `onboarding_probe.earlier_proof(root, profile_id, command_identity(<the profile's one_test spec>))`:
      `same_command` -> True; `command_changed`, `none`, `unreadable` -> the same word, False. A record row is judged as today:
      its `tests` is not read (D1).
   9. Any exception -> `error`, False.
2. **The record is read with the identity the writers wrote.** `earlier_proof` is called with `command_identity(spec)` of the
   PROFILE's `one_test` (argv with placeholders + `env`) — the bytes every writer digests — never with the argv words and never
   with the run's command (whose placeholders are dropped). `runner_identity` is called with argv WORDS (`command_argv`),
   never with the identity (its `"\u0000env"` word is not a runner word).
3. **The run never stops on it.** `validate_request` no longer refuses on `selector_contract_verified`. Every other refusal of
   the behavioural block stays (selected non-empty, `selector_args` per selected instance, the join rules, `report_test_id` per
   selected instance, ambiguity). `run_suite.main` prints, for a behavioural request whose `selector_contract` is not verified,
   ONE line on stderr: `SELECTORS (note): profile <id>: the factory has not verified how this runner selects one test (<why>).
   The run goes by each instance's selector_args; a selected test the runner did not run comes back not_run under its report
   id, never passed. To verify: python <plugin>/scripts/onboarding_probe.py --root <project> --probe-profiles --profile <id>
   --proposals-dir <a temporary folder outside the project>` (the command shape as `onboarding_probe.py:11` documents it).
   Why nothing is lost by dropping a `tests` count (D1): a wrong or empty selection cannot come out green — `build_run_block`
   binds rows by exact report id and gives `not_run` (`run_suite.py:505-539`, `:688-692`; critic K3); the count would only
   have refused rows that no writer produces (writers record only a proven run, `gate_preflight.py:3856`).
4. **Both roads are one road.** The note is printed where `--mine` and `--request` both pass (`run_suite.main`, beside the
   `NODE IDS (note)` lines `:2888-2891`), by `selector_note(request, cfg, root)`, which finds the profile through
   `request_profile(request, cfg)` and judges `request["command"]` (item 1, `command=`). Per F2 = B: `build_mine_request` no
   longer writes `selector_contract_verified` (`:3668-3673` keep only `command["selector_args"] = selector_args`; `pytest_run`
   at `:3465` stays, it is read at `:3473`, `:3475`), the precedent copy drops the key (`:3404-3405` filters it with
   `selector_args`), the template no longer pre-fills it (`run_suite.py:2452`), and `validate_request` ignores the key when a
   request still carries it (old requests on disk).
5. **The factory can produce "verified" (FR-5).** With item 2 the record that the onboarding probe and gate A already write makes
   the answer True for a selecting run form (`playwright-test` today) with no hand literal, on both roads as long as the run's
   command is the profile's. A wrapper script (`no_selection_form`) stays False by design — the run still goes, with the note.
6. **Consequence for the probe's R6(a) (stated, critic t-493).** `selectors_verified` now answers True for a pytest-shaped
   one-test command (state `node_id`) and for an `env` command with a proof. R6(a) therefore passes on pytest-shaped profiles
   where it refused before; its refusal for every other unverified state is unchanged. This is the intended direction: for
   pytest the node id IS the selection, the same truth `build_mine_request` used.

Cost of compliance (rule 10 a): one reader change, one refusal removed, one note line, one extracted lookup helper; the role
pays nothing new; the person pays nothing (no question added).

---

## 3. Edge behaviour, each with the invariant it protects

| # | Edge | Behaviour | Invariant |
|---|---|---|---|
| E1 | No rehearsal record at all (`state/reporter-rehearsals.json` absent) | `selector_contract` -> `none`, False; `--mine`/`--request` LAUNCH; one `SELECTORS (note)`; probe R6(a) still refuses (F3 = a) | a selected test with no bound report row is `not_run` (reason "report row missing" / "id not in report"), never `passed`; the run never stops on an absent record |
| E2a | Profile `selectors` is `{}` or absent (the LR2-1 state) | no literal -> the command and record road (item 1) | an absent literal is "not said", never `false` |
| E2b | Profile `selectors` is not an object (`"yes"`, a list) | state `hand_unreadable`, False; `selectors_verified` False as today (`test_profile_contract.py:197`) | a foreign shape never reads as a hand True |
| E2c | A record row of THIS command without `tests`, or with `tests: 0` (only a hand edit writes the latter) | judged as today: `same_command`, True (D1) | a wrong True still gives no pass: binding by exact id gives `not_run` (§0.1, K3) |
| E2d | `selectors.verified` is not a bool (`"true"`, `1`, `null`) | not read as hand True or False; the order goes on to the command and the record; the `why` names the unread literal (M3) | a non-bool literal neither certifies nor vetoes; only a JSON `true`/`false` is the hand |
| E3 | Record older than the profile | age is NOT read; the identity digest is. Same argv+env words -> the record counts even if `cwd` or dependencies moved; other words -> `command_changed` | a receipt measured on another COMMAND never counts; a moved cwd can at worst give a wrong True, which binding by id turns into `not_run` (error direction of §4) |
| E4 | Project with no UI (API-only) | identical: the selector contract is about the runner, not the UI; an API Playwright or pytest suite follows items 1-4 | no branch on "has UI"; the first look is not read |
| E5 | Record of another profile, or of the same profile with another (valid) `env` value | `command_changed` / `none`, False | another command's proof never counts (`test_profile_contract.py:182`) |
| E6 | `root` is a sandbox clone (red probe caller passing `--sandbox-root`) | False there (no record), as today (`profile_contract.py:354`); the run still goes. `run_suite.main` passes `project_root()`, never the clone | the project's record is read only at the project root |
| E7 | Hand literal `selectors.verified: false` on a selecting, rehearsed command | False, note printed, run goes | the person's `false` is never overridden by a record |
| E8 | A request on disk written before the change, carrying `selector_contract_verified: false` (or `true`) | ignored by `validate_request`; the note is computed fresh | an old field neither refuses nor certifies |
| E9 | Purpose not behavioural (`build`, `collect`, `manual`, `quality`) | no note | the note speaks only where tests are selected |
| E10 | `runner_identity` table unreadable (`problem` set) | `selection` None -> `no_selection_form`, False, `why` carries the problem words | a table problem is "cannot tell", never True (`launch_check.py:705-706`) |
| E11 | The judged command's `env` is FOREIGN (not an object; a bad name; a value other than `{report_path}`) — on the profile's `one_test` or on the run's command (D5) | `no_command`, False; no record is read | a command whose identity cannot be formed is never matched on its argv alone against an older row |
| E12 | `--request` road: the role's hand-written `command` differs from the profile's one-test command (other argv words, other `env`, extra words such as a flag the probe appends) (D2) | `command_not_profile`, False, note printed, run goes | the record proves only the profile's command; a different command never borrows its proof |
| E13 | `--request` road: the role's `command` IS the profile's (argv = one-test argv with placeholders dropped, same `env`) | the record road (item 1.8): True after a proven rehearsal | the factory's own proof reaches the template road too (one road, P31) |
| E14 | `--mine` with a precedent command copied (equal to the profile's, or copied "not compared" because one side was unreadable) (D2) | the copied command is the judged one: equal -> the record road; unreadable profile side -> `command_not_profile`, False | what runs is what is judged; an uncompared copy never reads as verified |
| E15 | Run command pytest-shaped (`--request` or `--mine`), whatever the profile's one-test command | `node_id`, True, no note | pytest's node id is the selection on whichever road runs it (as `:3465` judged the request's command) |
| E16 | Profile has no `one_test`, the run's command is not pytest-shaped (D2) | `command_not_profile` (run road) / `no_command` (profile road), False, note | no record can prove a command the profile does not name |
| E17 | A job on disk built before the upgrade carries `selector_contract_verified` in its `command`; the new request does not (M1) | `request_digest` (`execution_request.py:373-380`) hashes the whole command: the digests differ, the new request is not answered by the old job; `_match`/`covered` do not compare the whole command, so instance reuse is unaffected | at worst ONE extra launch per story in flight, never a false reuse |
| E18 | `selector_note` or `request_profile` meets a request with no `profile_id`, a `cfg` with no `profiles`, or a profile id nobody has | `request_profile` returns `{}` (as `executor_gap` does today); `selector_contract({}, ...)` -> `no_command`? No: a `{}` profile is an object with no `one_test` -> on the run road `command_not_profile`, False; the note names the profile id as written, or "the selected profile" when empty; never raises | a missing profile never reads as verified and never stops the run |

TEMPORAL (rule 11 i): this change brings NO artifact into existence. The record file already exists or not; its writers are
untouched. N4 adds a data key to a shipped file in the same commit as its reader, so no world has the key without the reader;
a project-local copy of `launch-causes.json` is not a factory input (the file is read from the plugin). World before (package
<= 0.11.0): `--mine` refuses an unverified contract. World after: no refusal; a stand whose record was written by any
onboarding or gate A since EP1-22 reads True at once (its rows already carry the identity digest); a stand with no record runs
with the note; a stand with the hand literal (the LR2 arm) keeps its answer.

POSITIONAL (rule 11 ii):
- `validate_request`: the removed lines are the first `if` of the `if purpose in BEHAVIORAL:` block (`:294-296`). Invariant: every
  other check of that block still refuses exactly as before (R-N2-1 negative controls), and no check before or after moves.
- `run_suite.main`: the note goes AFTER the `verify_node_ids` notes (`:2888-2891`) and BEFORE `hold_stand` (`:2899`). Invariant: a
  request refused earlier (budget, executor gap, invalid) prints no `SELECTORS` note; nothing that was refused before is
  accepted now except the selector-contract case.
- `selector_contract` order (item 1): object check, hand shape, hand literal, command, pytest shape, selection form, run vs
  profile, record. Invariants: a hand `false` is unreachable by any record; a hand shape that is not an object is never read
  as a literal; the `node_id` answer is unreachable for a command `is_pytest_command` rejects (after N4: a form without the
  key); the record is unreachable for a command whose `env` is foreign or which is not the profile's.
- `build_mine_request:3404-3405`: the key is filtered at the copy. Invariant: no precedent value ever reaches a new request.
- `executor_gap`: the inline lookup `:1585-1586` is replaced by `request_profile(request, cfg)`. Invariant: `executor_gap`
  returns exactly what it returned before on every input (its selftest rows `:2500-2505` and `test_handed_to_person.py:240-251`
  stay green unchanged).

Conflicting requirement pairs:
- "the hand wins" vs "the factory produces it itself" — the hand wins (E7); the factory's record only answers where the hand is
  silent.
- "judge the command that runs" (D2) vs "the record proves the profile's command" — both hold: the run's command is judged for
  its shape (items 1.5-1.6) and compared with the profile's (1.7); the record is read only for the profile's identity (1.8).

---

## 4. Error direction of the reused function (designer rule 1)

`selectors_verified` moves from GATE to ADVICE on the run (less consequential) but stays a GATE in `probe_by_code` R6(a)
(unchanged role). The change makes it answer True in more cases (env commands with a proof; pytest-shaped one-test commands,
item 2.6). Allowed direction: **False when in doubt.** A wrong True is tolerated only because binding is by exact report id
(`run_suite.build_run_block` `:505-539` in S5; `red_sandbox.bind_row` `:1049-1056` in the red probe).

Adversarial inputs that must stay False (each a row in R-N1-1): a record of another profile; a record whose digest is the argv
WORDS only for a command that sets `env`; a record of the same argv with another valid `env` value; a command with a FOREIGN
`env` whose argv words alone are on record (D5); a wrapper script with its digest on record; a form with no `selection`
(`npx jest`) with its digest on record; an unreadable record; `root=None`; a root that is no directory; a `selectors` that is not
an object; a profile that is no object; a hand `false`; a `verified` literal `"true"` with no record; a run command that differs
from the profile's by one argv word, or by its `env`, with the profile's digest on record (D2); the identity (with its
`"\u0000env"` word) handed to `runner_identity` must not change its answer (it is never handed: a source-level row).

---

## 5. Nodes (for a weaker model; owns by FUNCTION in hot files)

Order and merges: **N1 first**; N2, N3 and N4 each branch from a `main` that already holds N1 (each calls or rewrites what N1
provides), and may then run in parallel: their owns do not overlap except `test_execution_request.py`, where N2 and N4 own
disjoint functions (N2: new `fv1_18_no_stop_one_note` and its call in `main`; N4: the body of N1's `fv1_18_selector_contract`
rows R-N1-6 only) — the later of the two merges `main` into its tree and resolves (PROJECT.md «Командная работа» п. 3,
D-0048). No node depends on a row an unmerged node provides. All tests are ROWS in keep files
(`scripts/tests/test-layers.json` keep rows: `test_execution_request.py` `:1497` covering `execution_request.py`,
`profile_contract.py`, `run_suite.py`; `test_probe_by_code_languages.py` `:3648` covering `probe_by_code.py`; `test_run_forms.py`
`:4552` covering `launch_check.py`, `references/launch-causes.json`). NOT in quarantined files (`test_profile_contract.py`,
`test_onboarding_probe.py`, `test_run_suite_mine.py`, `test_report_env.py`, `test_reporter_rehearsal.py`, `test_launch_check.py`
are under `quarantine`, `test-layers.json:7046+`): the builder neither runs nor edits them.

Keep tests a node touches but does not own must stay GREEN UNCHANGED; one that goes red is a question to the Lead, never an
edit: N1 — `test_probe_by_code_languages.py:1887-1894` (its fixture `:1861-1867` writes a row without `tests` digested from argv
words of a command with no `env`, i.e. its identity; green under D1), `test_probe_fix_round.py:38` (its World's config is `{}`,
`no_command`, refusal stays); N2 — `test_handed_to_person.py:240-251` (executor_gap); the scenario keep rows `scenario_walk`
prints for `execution_request.py`/`run_suite.py` (E17: a scenario that asserted a reuse across the dropped key is a question).

### N1 — the one answer reads the identity and the command that runs (profile_contract)

owns: `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\profile_contract.py` (`selectors_verified`; new `selector_contract`),
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_execution_request.py` (one new function `fv1_18_selector_contract` + its call in `main`)

1. `selector_contract(profile, root, command=None)` per §2 item 1, pure, never raises, writes nothing; `import execution_request`,
   `import launch_check`, `import onboarding_probe` inside the function (M4: `execution_request` imports `profile_contract` at
   module top). `why` sentences: one per state, English, naming what was missing (e.g. `none`: "no proven rehearsal of this
   command is on record"; `command_changed`: "the record proved another command of this profile on <at>";
   `no_selection_form`: "this runner form has no selection row in the run-form data"; `command_not_profile`: "the run's
   command is not the profile's one_test command, and the record proves only that one"; `no_command`: names the missing or
   foreign part, e.g. "commands.one_test.env is not exactly {report_path}"; `hand_unreadable`: "selectors in
   qa-factory/config.json is not an object").
2. `selectors_verified` -> `selector_contract(profile, root)["verified"]`; docstring updated (identity digest, foreign `env`,
   the order). `onboarding_probe.py` is NOT edited (no `tests` key: D1).
3. Tests (rows of `fv1_18_selector_contract`, fixtures built as `test_profile_contract.py:160-172` builds them — copy the
   helpers' SHAPE, not the file): R-N1-1 one row per adversarial input of §4 (False, state named); R-N1-2 a Playwright profile
   WITH `env` and a row digested from `command_identity` -> True, state `same_command` (the LR2-1 regression row; must be False
   on origin/main = the red control, quoted in the report); R-N1-3 same profile, row digested from argv words only -> False,
   `command_changed`; R-N1-4 a row of this command WITHOUT `tests` -> True (D1, judged as today); R-N1-5 every state's `why` is
   non-empty and contains no Cyrillic; R-N1-6 a pytest command -> True, state `node_id` (profile road and `command=` road);
   R-N1-7 foreign `env` (three shapes: a string, a bad name, a value other than `{report_path}`) with the argv's digest on
   record -> `no_command`, False (D5); R-N1-8 the run road: `command` = the profile's argv with placeholders dropped + same
   `env`, profile digest on record -> True; one argv word more -> `command_not_profile`; same argv, `env` absent while the
   profile sets it -> `command_not_profile`; profile with no `one_test` and a non-pytest `command` -> `command_not_profile`
   (D2); R-N1-9 `selectors` `"yes"` -> `hand_unreadable`; `verified` `"true"` with no record -> `none`, False, `why` names the
   unread literal; `verified` `"true"` with a proof -> True (M3); R-N1-10 a pytest-shaped one-test profile with no record:
   `selectors_verified` True (the R6(a) consequence of §2 item 6, stated in the row name).

### N2 — no stop, one note on both roads (execution_request, run_suite)

owns: `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\execution_request.py` (`validate_request`: lines `:294-296` only; `build_mine_request`: the precedent copy filter `:3404-3405` and the block `:3668-3673` only),
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\run_suite.py` (`main`: one note call after `:2891`; `executor_gap`: the lookup `:1585-1586` only; new `request_profile`; new `selector_note`; `REQUEST_TEMPLATE_FIELDS` `command` entry `:2443-2453`),
`C:\QAFactory\forge-repo\ai-packages\qa-factory\references\gate-registry.json` (`:95` `decides` text: drop "selector contract"),
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_execution_request.py` (one new function `fv1_18_no_stop_one_note` + its call in `main`; the `base_request` key at `:53` stays — it is an old request, E8)

1. Delete `:295-296`. Leave `:297-355` byte-identical.
2. `build_mine_request`: filter `selector_contract_verified` at `:3404-3405` beside `selector_args`; replace `:3669-3673` with
   nothing (the pytest truth now lives in `selector_contract`, N1). `pytest_run` (`:3465`) stays.
3. `run_suite.request_profile(request: dict, cfg: dict) -> dict`: the profile row whose `profile_id` equals
   `str(request.get("profile_id") or "")`, else `{}` — exactly the expression at `:1585-1586`, moved (D3, AR-15). `executor_gap`
   calls it in place of the inline code; nothing else in `executor_gap` changes.
4. `run_suite.selector_note(request: dict, cfg: dict, root) -> str`: "" unless `request.get("purpose")` is in
   `execution_request.BEHAVIORAL`; else `selector_contract(request_profile(request, cfg), root, command=request.get("command"))`
   and, when not verified, the `SELECTORS (note)` line of §2 item 3 (profile id as written, or "the selected profile"). Any
   exception -> "". `main` after `:2891`: `note = selector_note(request, cfg, project_root())`; print it to stderr when non-empty.
5. Template: drop `"selector_contract_verified": True` from the `command` skeleton; the legend says nothing about it.
6. Tests: R-N2-1 `validate_request` on `base_request()` with the key removed, and with `False` -> resolves (was refused);
   negative controls in the same row: no `selected_instance_ids` -> still refused; `selector_args` missing an instance ->
   still refused; no `report_test_id` -> still refused (quote each message). R-N2-2 a `--mine` build in the fixture of
   `ep1_37_build_mine_request_role_wins` (`test_execution_request.py:1760-1812`) with `"selectors": {}` instead of
   `{"verified": True}` -> the request is built, carries no `selector_contract_verified`; the template skeleton has no such key.
   R-N2-3 a precedent job whose command carries `selector_contract_verified: false` -> the new request has no such key.
   R-N2-4 `selector_note`: unverified `initial` request -> the line with the profile id, the `why`, the words "not_run" and
   "never passed", and the `--probe-profiles --profile <id>` door, and NOT the word `not_executed`; verified (pytest command)
   -> ""; purpose `collect` -> ""; a `--request`-shaped request whose command differs from the profile's -> the line with the
   `command_not_profile` why (D2); and `build_run_block` on a summary with no report row for the selected instance -> its row
   `status` `not_run`, `reason` "report row missing" (D4; the AR-28 change check). R-N2-5 `request_profile`: found, absent id,
   `cfg` without `profiles`, a non-dict row -> the row / `{}` / `{}` / skipped; and `executor_gap`'s two selftest inputs
   (`run_suite.py:2500-2505`) give the same answers after the move.

### N3 — the probe's door names the command that writes the record (F3 = a)

owns: `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\probe_by_code.py` (`run_shape_checks`: the sentence at `:2787-2789` only),
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_probe_by_code_languages.py` (`ep1_36_shape`: one new `check_in` row after `:1891`; rows `:1374`, `:1887-1894` unchanged)

The `not verified` problem keeps its head word for word — `profile <id> does not say its selector contract is verified` — so
`test_probe_fix_round.py:38` (`"selector contract"`) and `test_probe_by_code_languages.py:1374` (`"selector contract is verified"`,
`"selectors.verified"`) stay green without edits and `test_probe_fix_round.py` stays outside the owns (D6). It then gives
`selector_contract(profile, root)["why"]` and the door: `(<why>; the onboarding probe writes the proof:
onboarding_probe.py --root <project> --probe-profiles --profile <id> --proposals-dir <a temporary folder outside the project>,
or a person writes selectors.verified in qa-factory/config.json)`. Refusal stays (FR-4: the probe's mutated test must be the
selected one). Test R-N3-1: the `shape(pw, rehearsed=False)` refusal also contains `--probe-profiles --profile pw` and the
`none` why.

### N4 — pytest's "a node id is the selection" as a data row (F4 = a, D7)

owns: `C:\QAFactory\forge-repo\ai-packages\qa-factory\references\launch-causes.json` (the `pytest` row of `run_forms.forms`, `:30`: add `"selection_by_node_id": true`),
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\launch_check.py` (`_selection_rows` `:176-204`, the `load_data` line `:172`, `runner_identity` `:701-732`),
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\profile_contract.py` (`selector_contract`: the `node_id` step only),
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_run_forms.py` (one new function `fv1_18_node_id_selection` + its call in `main`),
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_execution_request.py` (`fv1_18_selector_contract`: rows R-N1-6 rewritten to read the capability)

1. Data key, literal name: `selection_by_node_id` on a `run_forms.forms` row; value `true` means "a node id given as an argument
   selects one test with this form". Only the `pytest` row carries it.
2. Where it is admitted: `hooklib._load_run_forms` keeps `id, argv, diagnostics, negators` and drops other keys
   (`hooklib.py:1229`) — it stays untouched (the guard does not need the key). `launch_check` reads the raw file itself for keys
   hooklib drops (`_selection_rows`, `:176-181`); that function also collects `selection_by_node_id` per form id into a map
   `node_id_by_form` (returned beside `selection_by_form`/`selection_problems`; `load_data` stores it at `:172`). Value shapes:
   absent -> not listed (False); `true` -> True; any other value (`false`, `"yes"`, `1`, `null`) -> False and the words
   "`selection_by_node_id` must be true when present" in `selection_problems` for that form id (which also blanks that form's
   `selection`, as every problem of the row does today — the pytest row has none).
3. `runner_identity` gains `node_id_selection: bool` = `node_id_by_form.get(form_id, False)`; False whenever `problem` is set.
4. `selector_contract`'s `node_id` step reads `launch_check.runner_identity(argv)["node_id_selection"]`; `is_pytest_command` is
   no longer called there. Census row M4 of `t-2046` closed in the same commit (axis 34).
5. Tests R-N4-1 (`test_run_forms.py`, through `with_data` as k6 does): key `true` on pytest -> `runner_identity(["pytest"])
   ["node_id_selection"]` True; key absent -> False; key `"yes"` -> False and a problem naming the form; shipped data:
   `pytest`, `python -m pytest`, `poetry run pytest`, `uv run pytest` -> True; `npx playwright test` -> False. R-N4-2 the
   rewritten R-N1-6 rows: a pytest one-test command -> `node_id` through the capability. R-N4-3 the launchers that
   `is_pytest_command` accepts and `direct_test_form` may not (`py.test`, `tox -e py`): their answer under N4 is printed in the
   report and judged against F6 (no silent change).

---

## 6. DoD (per node; witness scope = builder-rules 7b)

Per node, the builder's verification run is exactly:

`python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <the node's owns paths>`

then each test file it prints (a quarantined file is never run). Expected at least: N1 — `test_execution_request.py` and the
keep rows covering `profile_contract.py`; N2 — `test_execution_request.py`, `test_handed_to_person.py` (covers `run_suite.py`),
`test_gate_registry.py` for `gate-registry.json`; N3 — `test_probe_by_code_languages.py`, `test_probe_fix_round.py`,
`test_profile_reader.py` (covers `probe_by_code.py`); N4 — `test_run_forms.py`, `test_execution_request.py`. A line "no scenario
or keep row covers" is a report line, not a reason for a new file. Also `python -B ai-packages/qa-factory/scripts/selftest.py
--lang` (FR-30) on the touched files.

Acceptance keys: R-N1-1..10, R-N2-1..5, R-N3-1, R-N4-1..3 green; R-N1-2 shown RED on origin/main first (verbatim); every keep test
named "touched, not owned" in §5 green unchanged; the AR change checks of §1.1 answered in the report; `judgment-census.json`
and `test_judgment_census.py` unchanged and green (no unit added; if the census test reports a changed unit, that is a
question, not an edit); FR sections A/C/D/E/G walked in the report.

siblings (for the dispatch header): axis 30 (profile commands reader: `command_identity`, `command_env`, `one_test_argv` read
through `profile_contract`; no new `commands` parse), axis 34 (one road: `--mine`/`--request`; pytest branch -> N4), axis 5
(stage twins: S6 runner `--request` road gets the same note — same `main`), axis 18 (no ratchet raised), axis 11
(shell-command recognizers: `runner_identity` gains one data-read field in N4; `py.test`/`tox` divergence -> F6).

---

## 7. Four questions (CLAUDE.md rule 10)

(a) Cost: one reader fix, one refusal removed, one note, one extracted lookup helper, one data key with its reader; roles and
the person pay nothing; the conductor loses a stop it could not settle (the LR2-1 "declare the selectors" question disappears).

(b) Axes (36), mechanism "selector contract: one answer, no stop":
axis 1 — policy/role files/journal: n/a, no deployment policy changes.
axis 2 — exam instruments: n/a.
axis 3 — package/release/installed: covered by the release procedure; no install-time file.
axis 4 — rules/debt/backlog/principles: covered — FR-4/FR-5 hold; no debt row; no BACKLOG row (frozen).
axis 5 — stage twins: covered — S5 `--mine` and S6/S7 `--request` pass the same `main` note.
axis 6 — measurement tools: n/a, no measurer reads the field.
axis 7 — per-test identity: covered — binding by `report_test_id` unchanged and still required.
axis 8 — story on disk: n/a.
axis 9 — "is a test file": n/a.
axis 10 — git-top readers: n/a.
axis 11 — shell-command recognizers: covered — `runner_identity` read; N4 adds one data-read field; launcher divergence -> F6.
axis 12 — work-plan carriers: covered — the finding/node move by the batch rules.
axis 13 — dispatch text: n/a.
axis 14 — transcript readers: n/a.
axis 15 — console stream: n/a (stderr line like its neighbours).
axis 16 — JSON reader: covered — `earlier_proof` keeps its reader and its keys; `launch-causes.json` read by its existing raw reader.
axis 17 — detector verdict shape: n/a, no detector.
axis 18 — shrink-only ratchets: covered — none raised; census unchanged.
axis 19 — role `tools:` line: n/a.
axis 20 — host receipt names: n/a.
axis 21 — markdown tables: n/a.
axis 22 — host return form: n/a.
axis 23 — `tests[]` row fields: n/a (no field required or dropped on a row).
axis 24 — execution record join: covered — `not_run` by id ("report row missing") unchanged.
axis 25 — freshness predicates: n/a.
axis 26 — `stand not confirmed`: n/a.
axis 27 — profile of a test row: covered — the note reads the request's `profile_id` through `request_profile`, the row's profile reader untouched.
axis 28 — render site of the row form: n/a.
axis 29 — jsonl writers: n/a.
axis 30 — profile commands: covered — identity via `command_identity`, argv via `command_argv`/`one_test_argv`, env via `command_env`.
axis 31 — role carriers: n/a (no role file text; FV1-29 owns the automator's card).
axis 32 — where judgment lives: covered — §1.2.
axis 33 — which dispatch: n/a.
axis 34 — one road: covered for `--mine`/`--request` (one note, one judged command); pytest-by-name -> N4 (node with owns and test).
axis 35 — sides of a story: n/a.
axis 36 — rows against a substitute: n/a.

(c) Detector: R-N1-2 (the regression row) and R-N2-1 in `test_execution_request.py` (keep, canon); for the leak class "a
selector question stops S5 again", calibration check 41 (judgment census) does not see a removed refusal coming back — the
live-runs row of FV1-18 (FR-33) and the critic's question 12 (axis 34) are the detectors.

(d) What stops skipping: code on the path — `run_suite.main` calls `selector_note` on every request it launches; there is no
gate left to skip.

---

## 8. Crossings with work in flight

| Work | Crossing | Needed |
|---|---|---|
| T5 (told-before-work spec §5.1 row T5, §5.4 row 18 `execution_request:selector` `:296-330`) | owns `validate_request`; its row 18 sentence says "A behavioural command has a verified adapter selector contract" — false after N2 | FV1-18 lands first (wave 1, §5.0 line 371/374); the Lead re-words row 18 before T1r lands it (drop the contract clause) |
| T5 §5.4 line numbers (mechanism spec `20261113-told-before-work-mechanism-spec.md:541, 546, 548`) | N2 deletes `execution_request.py:295-296`: row 11 (`:132-139, 298, 304`) and row 18 (`:296-330`) shift by −2; row 16 (`:207-264`) lies above the deletion — named by the critic, re-read against the merged file | the Lead (or T5's designer) re-pins rows 11, 16, 18 against `main` after N2 merges; a T5 row pointing at the deleted lines is a T5 spec defect, not N2's |
| T5 `run_suite.py` | T5 owns `main`'s `invalid_*` prints `:2740, 2771, 2857, 2904`; N2 adds one note call in `main` after `:2891` and edits `executor_gap` `:1585-1586` | `очередь: FV1-18 → T5` on `run_suite.py (main, executor_gap)`; T5 merges `main` |
| T5b (`MineRefusal` sites incl. `build_mine_request`) | N2 edits `build_mine_request` `:3404-3405` and `:3668-3673` only, no `MineRefusal` site | `очередь: FV1-18 → T5b` on `execution_request.py (build_mine_request)` |
| FV1-29 (automator gets the walker) | page locators, not runner selection; files `agents/qa-automator.md`, `scripts/brief_pack.py` — no overlap | none; FV1-29's text "missing selectors never stop it" is satisfied for runner selection by N2 |
| first-look finding `20261113-pervyj-vzglyad-ne-dohodit-do-avtomatora.md` | page locators to the automator; no shared file | none |
| FV1-26 (`report_facts.py`, depends on FV1-18) | after N2 an unverified contract is a note, never a "could not check" gap | FV1-26 must not count it as a gap |
| FV1-19 (wave 1, parallel) | `s5_precheck` row fields; no shared file per the plan | none |
| probe_by_code (EP1-36 owner area) | same answer, now True for env commands with a proof and for pytest-shaped commands (§2 item 6) | N3 (door words only) |
| hooklib run-forms guard | N4 adds a key hooklib drops; the guard's reading of the `pytest` row is unchanged | none; F6 names the `py.test` analog |

---

## 9. Forks

F1–F5: decided in §9a. F2 additionally answered by measurement (M1): `_match`/`covered` (`execution_request.py:2045-2100`)
do not compare the whole command; `request_digest` (`:373-380`) does, so a request built before the upgrade costs at most one
extra launch, never a false reuse (E17). The original text of F1–F5 follows unchanged for the record.

**F1 — who produces the selector-contract fact (owner's word "the first look gathers the selectors").**
(a) The reporter rehearsal record that onboarding and gate A already write, read with the right identity (N1). Consequence: no
new producer; works on every project with a selecting run form; a wrapper script stays "not verified" (runs anyway). (b) The
first look writes it. Consequence: impossible as stated — the first look walks the stand UI and never runs the test command; it
would be page locators under the same word (P27/AR-14 conflict, a fact with no evidence). (c) (a) plus S5's own first run that
binds every selected row records a proof row. Consequence: a new writer of the record (AR-14: today two writers share one
`_record_rehearsal`), more code, covers wrapper scripts. **Recommendation: (a).** Owner question (plain language, product
meaning): "In the refusal, 'selectors' meant how the test runner picks one test to run — not the page element locators the
first look collects. We propose: the factory never stops on it, and the check of the test command at onboarding (which already
runs one test) counts as the proof. The page locators stay with the first look and the automator's own look at the stand
(FV1-29). Is that what you meant?"

**F2 — the request field `selector_contract_verified` after the refusal is gone.**
(A) Keep it, written by code on `--mine` always (never copied), absent from the template; reader = the note. Consequence: the
`--request` road still has no code-written value (two roads differ by a label), and a field whose only reader is a print.
(B) Drop it from new requests; the answer is computed once in `run_suite.main` for both roads; old requests' key ignored.
Consequence: one road; request digests of new `--mine` requests lose one key (answered, M1: `request_digest` compares the whole
command, `_match`/`covered` do not — one extra launch, never a false reuse). **Recommendation: (B).**

**F3 — the mutation probe's R6(a) on an unverified contract.**
(a) Keep the refusal (the mutated test must be the one the run selects), fix its door to the onboarding probe command (N3).
(b) Demote it to a note too. Consequence: a mutation that the run did not select could read as survived unless the probe's
binding is proven to turn it into `not_run` — not verified by this designer. (c) Leave untouched, queue. **Recommendation: (a)**
— the owner's word speaks of the automator's run; the probe's question is a different consequence; its door must still be one
the factory can open (FR-2, FR-5).

**F4 — the pytest branch by language name (P31, AR-1).**
(a) Move it into `selector_contract` now (one place, every road) and open N4 (data row) in this batch. (b) Move it now and queue
N4 to TR2-16 (census M4). (c) Leave it in `build_mine_request` (then the `--request` road and the note would call pytest
"not verified" — wrong). Cost of covering the left-out side fully (N4): one data key, one reader line, one test row.
**Recommendation: (a)**; (b) acceptable if the batch is full.

**F5 — should the note also reach the report/person?** (a) No: it is a run note for the role; `not_run` rows already reach
the report under their own owner (AR-27). (b) Yes, a report line. **Recommendation: (a).** (Technique, but it changes what a
person reads — returned.)

**F6 (new, fix round) — launchers `is_pytest_command` accepts but the `pytest` run form may not match (`py.test`, `tox -e py`).**
N4 reads the capability through `runner_identity` -> `hooklib.direct_test_form`, which matches `argv: ["pytest"]` behind the
data launchers (`python -m`, `poetry run`, `uv run`); `is_pytest_command` (N1) also accepts `py.test` and `tox -e`. After N4 such
a profile would read `no_selection_form` (False: a note on the run, R6(a) refuses — origin/main's behaviour, no regression
against today, but a narrowing against N1). Options: (a) accept the narrowing; R-N4-3 prints the answers; the guard's own gap
(a direct `py.test` launch is not a `run_forms` form, so the guard does not see it) goes to the Lead as an analog finding.
(b) Add `py.test` as a second `argv` of the pytest form / a launcher row — this also widens the guard (it would start refusing
direct `py.test` launches outside `run_suite.py`), a guard change outside this node. (c) Keep `is_pytest_command` beside the
key (two roads for one question: P31 defect). Cost of covering the left-out side (b): one data row plus the guard's test rows in
`test_run_forms.py` (keep). **Recommendation: (a)** now, with the guard analog filed; (b) as its own node if the Lead wants the
guard widened. One-road check: (a) leaves one road (the data key), with a known data gap, not a second branch.

**F7 (new, fix round) — how strictly the run's command must equal the profile's for the record to count (D2).**
(a) Strict: argv words equal to the one-test argv with placeholders dropped, `env` equal — the comparison `build_mine_request`
already uses (`:3388-3389`). Consequence: a run whose command carries extra words (a flag the probe appends, a role's own flag on
`--request`) reads `command_not_profile` and prints the note; never a wrong True. (b) Prefix: the run's argv starts with the
profile's words, `env` equal. Consequence: fewer notes, but an appended word can change selection (`--grep`, `--project`), so a
proof of another command could count. **Recommendation: (a)** (error direction False, FR-59; the note costs nothing). Closed in
the draft by the recommendation; the Lead confirms.

## 9a. Lead acceptance of the draft, 13.11.2026 (t-482) — premise measured, forks

**Premise of §0.2 MEASURED (PROJECT.md package change item 6a).** Command: a read of `profiles[].commands.one_test` in
`C:\QAFactory\mybooks-stand\arm-factory\test-automation-framework\qa-factory\config.json.before-selectors-verified-20261112`
(and the current `config.json`). Result, both files: `"argv": ["npx","playwright","test","--project","chromium","--reporter=junit","<test-file>"], "cwd": ".", "env": {"PLAYWRIGHT_JUNIT_OUTPUT_NAME": "{report_path}"}`;
`selectors` was `{}` before and is `{"verified": true}` now (typed by hand in the run). `env` IS set — §0.2 holds, N1 stands.

| fork | decided | by | note |
|---|---|---|---|
| F1 | (a) the rehearsal record onboarding and gate A already write, read with the right identity | Lead, by recommendation, UNTIL the owner's word | the owner's words named the first look; the code's "selectors" is test selection by the runner. Her question is asked in plain language (non-blocking); N1/N2 do not change under (a) vs her answer unless she wants page locators to gate the run |
| F2 | (B) the field is dropped from new requests, one answer computed for both roads | Lead | one road (P31); the builder reports whether `_match`/`covered` compare the whole command |
| F3 | (a) the mutation probe keeps its refusal, its door names the command that writes the record (N3) | Lead | a different consequence from the automator's run; the door must open (FR-2, FR-5) |
| F4 | (a) the pytest branch moves into `selector_contract` and N4 (data row) rides in this batch | Lead | P31, AR-1 |
| F5 | (a) the note stays a run note for the role | Lead | nothing a person reads changes |

Next: critic on the plan (hot files `execution_request.py`, `run_suite.py`, `profile_contract.py`; a refusal becomes a note), then N1.

## 9b. Fix round after the critic on the plan (t-493)

Verdict: `docs/tasks/specs/reviews/20261113-fv1-18-plan-critic.md` (fit_with_fixes). Lead decisions D1–D7, M1–M5 (t-500).

| item | what changed | where |
|---|---|---|
| D1 | `not_counted` state and the `tests >= 1` rule dropped; a row without `tests` is judged as today; why nothing is lost (K3: exact-id binding gives `not_run`); `earlier_proof` gets no `tests` key and `onboarding_probe.py` leaves N1's owns; keep test `test_probe_by_code_languages.py:1887` stays green unowned | §2 items 1.8, 3; §3 E2c; §4 (row removed); §5 N1 (owns, items 2-3, R-N1-4), "touched, not owned"; §1.2 |
| D2 | `selector_contract(profile, root, command=None)`: on `--request` and `--mine` the request's command is judged (shape: `node_id`, `no_selection_form`), and compared with the profile's one-test command before the record counts (`command_not_profile`); the profile's `one_test` is read only when no command is given | §0.1 (`:3465`, `:3378-3416`, `:1821-1831` rows); §2 items 1, 2, 4; §3 E12-E16, E18, conflicting pair; §4; §5 N1 R-N1-8, N2 item 4 and R-N2-4; F7 |
| D3 | helper `run_suite.request_profile(request, cfg)` extracted from `:1585-1586`; `executor_gap` and `selector_note` both call it; N2 owns `executor_gap` (lookup only), `request_profile`, `selector_note`; keep rows R-N2-5 plus `test_handed_to_person.py` and the selftest rows green | §1.1 AR-15; §1.2; §3 POSITIONAL; §5 N2 owns, items 3-4, R-N2-5; §8 T5 row |
| D4 | every `not_executed` replaced by `not_run` (reason "report row missing"; "id not in report" for a contract with a `file`) | §1.1 AR-7, AR-28 rows; §2 item 3 (note text); §3 E1, E3; §5 R-N2-4 (asserts the words and the `build_run_block` row); §7 axis 24; §9 F5 |
| D5 | a foreign `env` gives `no_command`, False, before any record is read; never a match on argv alone | §0.1 (`command_identity` row); §2 item 1.4; §3 E11; §4; §5 R-N1-7 |
| D6 | N3 keeps the head "profile <id> does not say its selector contract is verified" word for word, so `test_probe_fix_round.py:38` and `test_probe_by_code_languages.py:1374` stay green; `test_probe_fix_round.py` stays outside the owns (chosen: keep the words, because they stay true and right for the person's reader); the `:38` literal is only "selector contract" (§0.4.6) | §0.1 (keep-tests row); §0.4.6; §5 N3 |
| D7 | key named `selection_by_node_id` on the `pytest` row; admitted by `launch_check._selection_rows` (hooklib drops it, `hooklib.py:1229`, untouched); `runner_identity.node_id_selection`; rows for present / absent / unknown value in `test_run_forms.py` | §0.1 (hooklib row); §5 N4 items 1-5, R-N4-1..3; F6 |
| M1 | F2 answered: `request_digest` compares the whole command, `_match`/`covered` do not — one extra launch, never a false reuse | §0.1 (reuse row); §3 E17; §9 head and F2 |
| M2 | `run_suite.build_run_block` cited as the S5 binder (`bind_row` is the red probe's) | §0.1 (wrong-True row); §4 |
| M3 | non-bool `selectors.verified` = "not said" (order goes on, `why` names it); `hand_unreadable` is step 2, after the object check and before the literal | §2 item 1.2-1.3; §3 E2d; §3 POSITIONAL; §5 R-N1-9 |
| M4 | `profile_contract` imports `execution_request` inside the function (cycle: `execution_request.py:17`) | §0.1 (import row); §2 item 1; §5 N1 item 1 |
| M5 | "a rehearsal of the command as declared runs the whole command and still counts as proof" queued as a candidate, not a node | §12 |
| also | R6(a) now passes on pytest-shaped profiles — stated; line shifts of T5 §5.4 rows 11, 16, 18 after N2 — a Crossings row (row 16 lies above the deletion: §0.4.5) | §2 item 6; §5 R-N1-10; §8 rows 1-2 |

## 9c. Lead acceptance of the fix round, 13.11.2026 (t-500)

Checked: §9b carries a row per D1-D7 / M1-M5; N1 (owns, rows R-N1-1..10) and the Crossings table read whole.

| fork | decided | by | note |
|---|---|---|---|
| F6 | (a) accept the narrowing; the guard's `py.test` gap is filed as an analog finding | Lead ("решила сама") | one road (the data key); (b) is its own node if the guard is widened |
| F7 | (a) strict equality of argv and `env` | Lead | error direction False (FR-59); a note costs nothing |

N1 is dispatched now; N2, N3, N4 branch from a tree that holds N1. F1 stays "(a) by recommendation until the owner's word".

## 10. Small choices closed by the designer (no design weight)

- `selector_contract` returns a dict; `selectors_verified` stays as its bool view (callers unchanged).
- The record's age is not compared with the profile (no portable profile timestamp; AR-4); the identity decides (E3).
- The note goes to stderr with the `<WORD> (note):` prefix the neighbours use (`run_suite.py:2874, 2891`).
- A `selectors` that is not an object gets its own state word `hand_unreadable` (E2b) rather than reusing `no_command`.
- The note helper `selector_note` and the lookup `request_profile` live in `run_suite.py` so a row can test them without a
  subprocess.
- (fix round) The record is always read with the PROFILE's one-test identity, also on the run road: the run's command has its
  placeholders dropped (`_command_from_profile`), so its own identity never equals any written row; judging it directly
  would make the run road never verified (FR-5 lost). Hence the compare-then-read step 1.7 (D2's consequence, not a new intent).
- (fix round) A profile with no `one_test` on the run road reads `command_not_profile`, on the profile road `no_command`
  (the word says which side is missing).
- (fix round) An invalid `selection_by_node_id` value is named in `selection_problems` (the existing problem channel of that
  reader), not in a new channel.

## 11. Reading trail

Read (read-main unless noted): finding FV1-18 (worktree `findings-1413c`) whole; batch row `batch-1-live-run-fvf.md:1-30, 50,
55, 62`; FV1-29 finding whole; first-look finding (grep: lines 12, 46); plan `20261113-plan-fabrika-ne-huzhe-agenta.md`
(grep FV1-18; lines 340-379); mechanism spec `20261113-told-before-work-mechanism-spec.md` §5.0 (`:360-383`), rows T5/T5b
(`:396-397`), §5.4 row grep (`:541, 546, 548`), crossings (`:621, 631`); `profile_contract.py:1-1066` whole;
`execution_request.py:1-372, 1804-1853, 3370-3489, 3600-3740, 3877-3891`; `onboarding_probe.py:1-760`;
`gate_preflight.py:3505-3639, 3815-3956`; `launch_check.py:170-204, 700-732`; `probe_by_code.py:2745-2804`;
`run_suite.py:2020-2036, 2425-2461, 2830-2919`; `first_look.py:1-60` (+ grep `selector`); `red_sandbox.py:1045-1070`;
`test_profile_contract.py:130-200`; `test_execution_request.py` (def list; `:1695-1812`); `test-layers.json:1-35, 1497-1517,
3919-3950` (+ key list); `judgment-census.json:1-30` (+ grep rows 305, 312, 677, 757); `SIBLING_MAP.md` axis list, axes 30, 34,
36; `builder-rules.md:14-23`; `p4-generate.md:190-214`; `CHANGELOG.md:1263-1264` (grep); `t-2046 census:50-74`;
`execution-probes` finding `20261031-proba-chuvstvitelnosti...md` whole; cart-1 `s5-2-initial.json:114-140`;
`experiments/mybooks/factory-vs-free-agent/answers/s5-selectors-declared-restart.md`; notebook grep (`:299-310`);
`scenario_walk.py` grep (`:14, 45-47, 833-931`).

Fix round (t-500), read in read-main: critic hand-back `reviews/20261113-fv1-18-plan-critic.md` whole; `run_suite.py:495-549,
680-699, 1560-1609, 2488-2512, 2860-2904` (+ grep `def build_run_block` `:469`, `from profile_contract` `:123`, no
`request_profile`/`profile_of` def); `execution_request.py:373-392, 3440-3479, 3660-3677` (+ grep imports `:2-22`,
`def is_pytest_command` `:623`, `def _match` `:2045`, `def covered` `:2076`, `_profile_argv`/`_profile_env`/`_command_from_profile`
`:1804-1835`); `profile_contract.py:1-40, 255-375`; `probe_by_code.py:2745-2799`; `launch_check.py:150-209, 698-737` (+ grep
`run_forms|selection`); `hooklib.py:1205-1234, 2285-2314` (+ grep `run_forms`); `launch-causes.json` grep (`run_forms`, form ids
`:28-52`, launchers `:56-60`, wrappers `:7, 11`); `test_probe_by_code_languages.py:1855-1894`; `test_probe_fix_round.py:1-60`;
`test_probe_walk.py:35-109`; `test_probe_every_check.py` grep (`flip`, `flip_refusal`); `test_handed_to_person.py:232-256`;
`test_run_forms.py` def list; `test-layers.json:1495-1517, 2215-2234, 3640-3714, 3905-3934, 7015-7049, 8545-8564` (+ grep keep
rows covering `launch_check.py` / `launch-causes.json`).

Searched and not found (with controls): the refusal paraphrase `selectors empty|declaring selectors` in PKG (-i) — none;
control `selector contract` (-i, same tool) hits `execution_request.py:296`. A writer of `selectors.verified` in package code
(`"selectors"|selectors\.verified` outside tests) — only readers (`profile_contract.py:359`, `probe_by_code.py:2789`,
`execution_request.py:3431`) and the empty sample `profile-shape.json:14`. A decision on the selector contract in
`DECISIONS.md` / `docs/DECISIONS_ARCHIVE.md` — none (grep `selector|rehears`, -i, per file; control: the same grep hits
`D-0019` rehearsal text in the archive `:31`). `selector_contract` in `test_run_suite_mine.py` — none (the files-with-matches
run of the same pattern lists 8 files, not that one). `record_schema`/references mentioning `selector_contract` — none (same run).
Fix round: `selector_contract_verified` in PKG outside fixtures — only `execution_request.py:295, 3670-3673`, `run_suite.py:2452`
and five test files that build OLD-shape requests (`test_execution_scheduler.py:46`, `test_execution_pipeline.py:43`,
`test_execution_request.py:53`, `test_import_test_receipt*.py`, `test_run_budget.py:1054`; all keep resolving under E8); no
schema in `references/` names it (same run, a content mode that does list the code sites). `verified adapter` in tests (-i) —
none; control: the same search hits `selectors_verified` in `test_profile_contract.py`. A `profiles`/`commands` word in
`test_probe_walk.py` — none; control: the same tool with `class World|cfg` (-i) hits `:35`, `:76`, and `:55` shows the `{}` cfg.
Not established: the commit that introduced the `--mine` refusal (no git tool); why the LR2-1 onboarding left no usable record
(§0.4.2); whether any scenario keep row asserts a reuse across the dropped key (E17: left to the witness run).

Needed beyond the manifest: `C:\QAFactory\forge-repo\experiments\mybooks\factory-vs-free-agent\` (answers file, notebook
grep) and `plans/piles/execution-probes/findings/20261031-proba-chuvstvitelnosti-ne-chitaet-playwright-ts-18-iz-18.md` (the 0.10.6
precedent); fix round: read-main `scripts/hooklib.py`, `scripts/tests/test_probe_walk.py`, `test_probe_every_check.py`,
`test_handed_to_person.py`, `test_run_forms.py`, `test-layers.json`, `references/launch-causes.json`.

## 12. Queue (candidates, not nodes)

- M5 (critic t-493): "a rehearsal of the command as declared runs the whole command and still counts as proof" — the record
  proves the declared one-test command ran and reported, not that its selector selected exactly one test; today this is
  tolerated by exact-id binding (§4). Candidate for the execution-probes pile: whether a proof row should carry what it
  selected. Not a node of FV1-18.
- F6 analog: a direct `py.test` / `tox -e` launch is not a `run_forms` form, so the guard does not see it — to the Lead as an
  analog finding (CLAUDE.md rule 9; not widened here).
