# Wave 0 — owed row drafts of §5.6, part 2 (role-facing remainder of items 1, 3, 4, 5, 7, 10)

Draft by the designer, 2026-11-13 (task t-488). Continues `20261113-told-before-work-wave0-rows.md` (part 1) in its
row form (part 1 §0). Parent spec: `20261113-told-before-work-mechanism-spec.md`. Forks are RETURNED, never decided.
Package code read ONLY from `C:\QAFactory\forge-repo\.claude\worktrees\read-main\ai-packages\qa-factory\`; file:line
below are of that tree, paths package-relative. Lead decisions applied: F-W1 (a) literal ids, F-W4 (b) conductor-only
sub-row when the only door is the conductor's, F-W6 (a) a refusal of nothing of the role's work is advice, F-W8 (a)
a host-only condition is words in the sentence.

Status words as part 1: **drafted** (sentence read from a body read whole), **no row** (reason class: not a refusal /
advice / conductor-facing / transport pointer / code road), **still not read** (with why), **fork** (returned below).

---

## Item 4 — `scripts/execution_request.py` `MineRefusal` sites (done first)

Transport (read whole): `run_suite.mine` :1945-2027 prints a `MineRefusal` as stdout
`{"status": "mine_refused", "error": <text>}`, exit 2; `WindowFirst` (a `MineRefusal` subclass, :530-538) as its
payload + `error`, exit 2; `resolve_mine_detail` :3031-3042 prints `find_active_dispatch` refusals the same way with a
hint. `probe_by_code` calls `build_mine_request` in process (:2924-2927, `profile_door=False`, `cwd=` its profile
directory) and wraps `_profile_for` refusals as `Refusal("probe_by_code: ...")` (:2679-2689). `red_sandbox._run_mine`
(:1249-1284) runs `run_suite.py --mine ... --purpose red_probe --sandbox-root <clone>` and reads the stdout summary
(stderr `invalid_request` form as a fallback).

Who meets these refusals (checked against callers, not inferred):

| caller road | roles | carrier |
|---|---|---|
| `run_suite.py --mine` (card `RUN_MINE`) | qa-automator, qa-runner | `brief_pack.py:142-147, 223-224, 256-257` |
| `run_suite.py --mine` (told by the section "Every run goes through run_suite.py") | qa-automator, qa-code-critic | `references/execution-lifecycle.md:109-117` |
| `probe_by_code.py --dispatch` (in-process build) | qa-code-critic | `brief_pack.py:236-247`; `probe_by_code.py:2924` |
| `red_sandbox.py --probe` → `--mine --sandbox-root` | qa-code-critic | `brief_pack.py:248-252`; `red_sandbox.py:1537, 1664-1668` |
| `red_sandbox.py --diagnostic` → `--mine --sandbox-root` | qa-failure-analyst | `brief_pack.py:274-276`; `red_sandbox.py:2030, 2168` |
| `probe_by_code.py --s6-close` | the driver only (`driver_stage_s6.py:591-668`; "the driver's door (`--s6-close`) is not shown to the critic", `probe_by_code.py:8327`) | — |
| `fresh_evidence` (`evidence_only`) | code: `driver_stage_s6.py:539`, `red_sandbox._fresh_instances` :1372-1386 (both callers catch: :1412-1417, :2018-2023) | — |

"All --mine roles" below = qa-automator (S5), qa-runner (S6), qa-code-critic (S5), qa-failure-analyst (S7, only through
`red_sandbox --diagnostic`). Every row: `when: shell`, `door_needs: shell`, `role_rule: references/execution-lifecycle.md`
for automator/critic, `agents/<role>.md` (tools section) for runner/analyst (S-P2-8).

### 4.0 Roles check of the two rows part 1 drafted (S4 → checked)

| row | part 1 roles | verdict from callers | sentence check against the body (noticed, see N1/N2) |
|---|---|---|---|
| `execution_request:sandbox` | qa-runner, qa-automator | **corrected: qa-code-critic, qa-failure-analyst.** `--sandbox-root` is passed only by `red_sandbox._run_mine` (:1256-1259); the `RUN_MINE` card names no `--sandbox-root`/`--cwd` (`brief_pack.py:142-147`, read directly); no agent file names `--sandbox-root` (Grep `--mine\|--sandbox-root\|red_sandbox` -i over `agents/`: control `--mine` found in qa-automator.md:68) | part 1's sentence ("a task-local path the factory placed, inside the story root") is not what the body checks — corrected row below |
| `execution_request:place_rows` | qa-runner, qa-automator | **corrected: all --mine roles** (any pytest `--mine`, incl. probe_by_code's `--cwd` build and red_sandbox runs) | part 1's sentence ("each placed row names a known case once") is not what the body checks — corrected row below |

Corrected rows (offered, since part 1 is accepted the Lead takes or leaves them — N1, N2):

| check | roles | requirement | door | sites |
|---|---|---|---|---|
| `execution_request:sandbox` | qa-code-critic, qa-failure-analyst | A run in a sandbox clone runs in the profile's own directory inside the clone: the profile's `commands.one_test.cwd` (when set) lies inside the project root; the sandbox root is a directory; the run directory resolves inside the clone (no link out of it) and exists there; and every test file the run needs is a file the clone holds. | name it as `tooling` in your digest (the card's rule for an incomplete probe); a test file the clone lacks: add it to the repository or run the probe on a tracked copy — see **F-P2-5** | `sandbox_run_directory` :2610-2665, `_sandbox_refusal` :2606-2607, `build_mine_request` :3599-3607 |
| `execution_request:place_rows` | all --mine roles | Every test file the manifest names for an asked case exists under the run directory or the project root (a path relative to the project root). | correct `file` through `manifest_put.py` (path relative to the project root), or pass `--cwd` when the test lives in a sandbox | `_place_rows` :2668-2685 (called :3476, :3513) |

### 4.1 The 8 site groups

| # | group (part 1 id) | status | check | roles | requirement | door | sites | text |
|---|---|---|---|---|---|---|---|---|
| 1 | `find_active_dispatch` | drafted | `execution_request:active_dispatch` | all --mine roles (probe_by_code `--dispatch` too, :4735-4744) | A `--mine` call belongs to exactly one running dispatch: the controller of the story has one open (with `--dispatch ID`, that running dispatch or one it resumes through `parent_retry`); when several are open, `--dispatch ID` (and `--task TICKET` across stories) names yours. | pass `--dispatch <your prompt's Dispatch id>` (and `--task <T>`); when none is open, name it in your digest (the conductor opens dispatches) | :878-929 (raises :915-920, :927-928) | — |
| 2 | `s6_close_from_state` | **no row: conductor-facing** (the driver's `--s6-close` road, G-code §2.8) | — | — | (every refusal names a door "its receiver (the driver or the conductor) can use", :944) | — | :952-1020 (raises :957, :979, :986, :992, :998, :1003, :1007, :1014); caller `s6_close_dispatch` :932-949 | — |
| 3 | `_entries_of_case` | drafted | `execution_request:case_entries` | all --mine roles | An asked case id names one case: a bare id the story holds under more than one area is asked with its area (`<area>/<id>`), and the manifest row's `covers` names the same area as the dispatch scope (a row that names no area is not run for a qualified id when the story holds the number under several areas, or once another row names one). | `--mine <area>/<id>`; or correct the row's `covers` through `manifest_put.py`; or hand the case back in your digest | :1159-1229 (raises :1193-1195, :1208-1211, :1223-1228); strict only for `--mine` (:1186-1196) | — |
| 4 | `_profile_for` | drafted (+ sub-row fork) | `execution_request:profile` | all --mine roles | The execution profile of the run is known without a guess: a profile named by `--profile` or a manifest row's `profile_id` is one `qa-factory/config.json` holds; the asked cases run under one profile; a row that names no profile and whose file lies under another profile's test root, or a root several profiles share, names its `profile_id`; when nothing else tells, `--profile` names it. | `profile_id` on the manifest row through `manifest_put.py --fragment`, or `--profile ID` (only where the caller takes it: `run_suite --mine`, never `probe_by_code`, :1707-1708, :1728); cases of two profiles: one `--mine` per profile | :1705-1801 (raises :1721, :1730-1732, :1735, :1750-1754, :1756-1760, :1774-1776, :1781-1783, :1799-1801); `unknown_profile_refusal` :1676-1684 | — |
| 4b | `_profile_for` (no profile at all) | **fork F-P2-3** | `execution_request:profile.none` | — | `config.json` holds no execution profile: the text says "a gap of the onboarding, not of your test" and names only the gate-A rehearsal and `/qa-factory:qa-onboarding` (a person's road) | none for the role in the text | :1790-1797 | — |
| 5 | `_command_from_profile` | drafted | `execution_request:profile_command` | all --mine roles | The profile's one-test command in `qa-factory/config.json` is readable: `commands.one_test.argv` present and in shape, its `env` in shape, and a `selectors.join` rule (when the profile has one) of the form `{"option", "separator", "group"?}`. | report it in your digest as an onboarding gap, and write this one run with `run_suite.py --template request` | :1821-1853 (raises :1828-1831, :1839-1844); `build_mine_request` :3428-3439 (join rule, `selector_join_problem` :49-67) | — |
| 6 | `_observe_precedent` | drafted (shares the row of 7a) | `execution_request:stand` | all --mine roles | (see 7a) | (see 7a) | :2803-2842 (raise :2827, only when not `evidence_only`; a freshness read notes it, :2828) | text from `run-budget.json` words `not_observed` (data) |
| 7a | `_observe_stand` | drafted | `execution_request:stand` | all --mine roles | The stand the run would stand on can be looked at now, and it runs this story's build. | name it as `environment` in your digest (`stand_health.py --probe --env <environment>`); a stand that runs another build: the person's word at the build question of the stage entry | :2862-2871 (raise :2871, `ProvenanceRefused`); :2827; `_stand_refusal` :2471-2488; `run-budget.json:37-38` | words data (`run-budget.json` `not_observed`, `build_refused`) |
| 7b | `_observe_stand` | drafted | `execution_request:stand.probe` | all --mine roles | The story's first typed run on a profile has a way to identify the stand: an `execution.runtime_probes` entry for the profile (or `*`) with an `argv`, or an earlier typed run of the story on the profile to copy the probe from. | the probe write command the refusal prints when there is one (`runtime_probe.py --suggest --write --profile <p>`), else write this one request from `run_suite.py --template request` (every later `--mine` copies its probe) | :2859-2861; `_probe_refusal` :2769-2794; `_probe_door` :2738-2766 | — |
| 7c | `_observe_stand` | drafted | `execution_request:stand.reference` | all --mine roles | The story's record does not name its own stand (`pipeline.json` `environment`) as the reference (old version) of a side as well. | tell the conductor in your digest which stand runs the new version (the record is corrected by `stage_done.py --set sides.<side>.reference=...`, a conductor command — F-W2) | :2872-2877; `reference_target_problem` :2512-2534 | — |
| 8 | `build_mine_request` | drafted (grouping S-P2-1) | see 8a-8j | | | | :3186-3874 read whole | |

Note on 7b's door: whether a role may run `runtime_probe.py --suggest --write` (it writes `qa-factory/config.json`;
`PT-config-write` refuses a role's write of that file "by Write, Edit, NotebookEdit or a shell write shape") was NOT
checked — the guard body `guard_pre_tool.py:1884-1894, 2221-2256` was not read in this draft. The door column keeps
`--template request` as the door that surely stands; the builder of T5b checks the first door against the guard.

### 4.2 `build_mine_request` — the ~12 sites grouped by requirement (S-P2-1)

| # | check | status | roles | requirement | door | sites | text |
|---|---|---|---|---|---|---|---|
| 8a | `execution_request:mine_call` | drafted | all --mine roles | A `--mine` call names at least one case id (in the project's case-id form), a `--purpose` of `initial`, `repair_verify` or `red_probe` (any other purpose goes through `--request`), `--node-id` only with ONE case, at most one of `--cwd` and `--sandbox-root`, and a red probe always one of them (never the author's tree). | correct the call as the refusal names (`--template request` for another purpose; `red_sandbox.py --probe` prepares and passes the sandbox) | :3222-3227, :3228-3230, :3314-3316, :3445-3448, :3456-3462; `MINE_PURPOSES` :541 | — |
| 8b | — | no row: conductor-facing (S6 close context, the driver's road) | — | — | — | :3231-3241, :3246-3255 | — |
| 8c | — | no row: code road (`evidence_only` callers catch the refusal and note it; see 4.0 table) | — | — | — | :3256-3264 | — |
| 8d | `execution_request:scope` | drafted | all --mine roles | A dispatch runs only the cases it was given: every asked case is in the dispatch's scope (a stale live check of a qa-code-critic red probe is admitted by code; anything else passes only on a person's recorded word). | hand the case back in your digest; the conductor dispatches it or records the person's word (`waiver.py`, block "outside its scope") | :3283-3301; `scope_refusal` :1041-1050; `_admitted_outside` :1069-1097 | byte-identical (`person_passed` matches stage overrides by this text, :1035-1038; `probe_debt` says the same sentence, :1043-1045) |
| 8e | `execution_request:no_test` | drafted | all --mine roles | Every asked case has a test to run: a manifest row with file and selector, or (pytest only) a file the manifest names whose tests mention the case in a marker, comment or docstring. | put the test in the manifest through `manifest_put.py` (file + selector), or name it for this run: `--mine <case> --node-id <file>::<test function>` | :3331-3333, :3472-3474, :3480-3503; `_no_test_refusal` :1148-1156 | — |
| 8f | (folded into `execution_request:profile_command`) | drafted | — | — | — | :3434-3439 | — |
| 8g | `execution_request:selector_args` | drafted | all --mine roles | A manifest row of a profile that does not run pytest carries `selector_args` (the framework's own arguments) and `report_test_id`, unless the factory can build the selection from a `run_forms` direct form. | give the row `selector_args` and `report_test_id` through `manifest_put.py` once; until then run through `--template request` | :3571-3593 | — |
| 8h | (folded into `execution_request:sandbox`) | drafted | — | — | — | :3599-3607 | — |
| 8i | `execution_request:window_first` | drafted (not in part 1's site list: a `WindowFirst` raise, found by reading the body whole — S-P2-5) | all --mine roles | A run that picks part of a case (`--node-id`) does not leave tests of the same file in the dispatch's scope that have never run in this window: one call runs them together. | run the command the answer names (`run_suite.py --mine <cases>`); only what a repair touched: `--purpose repair_verify`; this exact run once more: `--again` | :3642-3666; payload printed by `run_suite.mine` :2009-2014 | byte-identical (`person_passed` matches by this text, :3659) |
| 8j | `execution_request:fingerprint` | **fork F-P2-6** | — | the inputs of the run cannot be fingerprinted (`execution_fingerprint.build` ValueError: an input unavailable, bytes changed while hashed, a malformed record — raise lines `execution_fingerprint.py:52-160`, bodies not read) | none in the text | :3715-3724 | — |

Item 4 count: 8 groups → 7 drafted (groups 1, 3, 4, 5, 6, 7, 8; group 4 with fork F-P2-3 on its sub-row, group 8 with
fork F-P2-6 on 8j), 1 no row (group 2, conductor-facing). Rows produced: `active_dispatch`, `case_entries`, `profile`,
`profile_command`, `stand`, `stand.probe`, `stand.reference`, `mine_call`, `scope`, `no_test`, `selector_args`,
`window_first` = 12 drafted + 2 forks (`profile.none`, `fingerprint`) + 2 corrected part-1 rows.

---

## Item 5 — `scripts/run_suite.py`

| check | status | roles | when / door_needs | requirement | door | sites |
|---|---|---|---|---|---|---|
| `run_suite:recover` | drafted | qa-runner (card, `brief_pack.py:260`), qa-automator, qa-code-critic (`--recover` passes the stage guard, `execution-lifecycle.md:115-117`) | shell / shell | `--recover <KEY> --task <T>` names the idempotency key of a job recorded in that story's job store, and the job's file is readable JSON. | the `idempotency_key` the earlier answer printed (the not-launched answer names `--recover <idempotency_key> --task <task>`, `run_suite.py:3026-3027`) and your prompt's task; a job file that cannot be read is the factory's: name it in your digest | `main` :2764-2776 → `JobStore.recover` :452-468 (raise :456), `JobStore.read` :398-405 (raise :405); printed `invalid_recovery` on stderr, exit 2 |
| `run_suite:begin` | drafted | qa-automator, qa-runner, qa-failure-analyst (`RUN_REQUEST`, `brief_pack.py:163-164, 224, 257, 271`), qa-code-critic (`execution-lifecycle.md:112-113`; red_sandbox reads this refusal from stderr, `red_sandbox.py:1271-1283`) | shell / shell | A request's `idempotency_key` is new, or names the very request (same digest) already recorded under it; a key another process is claiming at the same moment is not reused. | write the request with a new `idempotency_key` (a `--mine` run takes a key of its own: run it again); a claim that cannot be read: `--recover <key> --task <T>` | `JobStore.begin` :414-445 (raises :419, :438, :440; read :405); sites `run_suite.py:2852` (printed by :2856-2858) and :2901-2905; both print `invalid_request` on stderr, exit 2 |

Item 5 count: 2 → 2 drafted. Note (N5): the :2856-2858 transport also carries `RequestError` "runtime probe does not
match requested profile/source/runtime" (:2837-2838) and `StoryRootError` (:2807), which part 1 pointed at §5.4 rows
10-19 (those are `validate_request` rows); neither has a row. Reported, not drafted (outside this brief's scope).

---

## Item 10 — `s5_precheck.check_sides` remainder; `manifest_put` placeholders path

Roles qa-automator; `when: window` (as part 1); door_needs shell (the doors are `manifest_put.py` / `run_suite.py`);
`check_sides` :2371-2405 read whole (orchestrates the five helpers; a story with every side real and no provisional
rows runs nothing, :2386-2388; a person's word may pass only `sides-undeclared` and `provisional-open-on-real`, :2375).

| check | status | requirement | door | sites |
|---|---|---|---|---|
| `s5_precheck:sides.settled` | drafted | A provisional row whose side is now real is not left open (unless it is a first-look accounting row): it is settled in the bind round, retracted, or kept by decision citing the person's word `substitute kept: <side>`; a settled row (`settled_matched` / `settled_edited`) cites in `evidence.run` a run block that is not a collect and whose stamp says its side was real, keeps the comment `qa-provisional: <id>` on its home line, and its status agrees with that line: `settled_matched` when the line is unchanged since `home_hash`, `settled_edited` when it changed and stands as the tool recorded in `evidence.home_hash_after`. | run the test on the real side, then send the row with `status` and `evidence: {run: <block id>}` through `manifest_put.py --fragment` (the tool records the hashes itself); or retract it | `_sides_settled` :2175-2222 |
| `s5_precheck:sides.placeholders` | drafted | Every id a test names in `provisional` is a row of `provisional[]`; an open first-look accounting row (a `placeholder_locator` assumed from `first_look:<R-n>`, on a real side) stands only while the current, fresh first-look record holds that requirement missing or unreachable because of the product; and every test linked to such a row declares it in `provisional`, sits in no `blocked_by_env` unresolved row, is not handed to the person, and has a passed or failed run row. | the finding's `fix`: drop or send the id / row through `manifest_put.py --fragment`; retract the row (`status: retracted`) or ask the conductor for a new first look; take the test out of the env row or the hand-off; run it once (`run_suite.py --mine <case>`) | `_sides_placeholders` :2320-2368; `_accounting_row` :2225-2230; `_first_look_basis` :2233-2246; `_basis_refusal` :2249-2268; `_linked_tests` :2271-2285; `_terminal_run_of` :2288-2292; `_env_blocked` :2300-2312; `_handed` :2315-2317 |

`manifest_put` placeholders path: no new row. The provisional keys are refused by `provisional_row_problems`
(:717-763, part 1's pointer to §5.4 row 25). `stamp_provisional` (:821-860, called :2468) only prints sentences
("no home_hash was recorded ...") and the fragment is still committed — not a refusal: advice, no row. Negative claim
"manifest_put has no `placeholder` code of its own": Grep `placeholder|first_look_row|accounting` -i over
`manifest_put.py` = 0; control with the same tool and flags (`provisional|expectation_change_problems`, -i, count) = 52.

Item 10 count: 2 → 2 drafted.

---

## Item 1 — `scripts/handoff_check.py` (the 2 builders part 1 did not read)

Roles qa-failure-analyst (the only contract with `not_for_repair` / `scope[].state` TEST_BUG..., its key page
`references/slices/qa-failure-analyst/handoff-keys.md:26-44`); `when: always`; door_needs as R1 (part 1).

| check | status | requirement | door | sites |
|---|---|---|---|---|
| `handoff_check:binding` | drafted (overlap with part 1's `null_outcome.failures` — **F-P2-1**) | Each failure of the run report has at most one triage row and each triage row answers one failure: a row that names several failures is a verdict for none of them, and several rows for one failure keep one — on both paths of the S7 form (its repair list empty or not). | triage every failure in `work/triage.json` with ONE row under that failure's own `instance_id`, then run this check again | `_binding_problems` :1146-1158 (condition read: rows present and the report readable, :1150-1151), `_binding_texts` :1131-1143, `_untriaged_failures` :1161-1183; caller `_null_outcome_view` :1258-1259 |
| `handoff_check:investigation` | drafted (dispatch-kind qualifier — **F-P2-2**) | In an S7 investigation dispatch the form hands nothing for repair and relists no triage row: `scope` and `not_for_repair` are each an empty list (or absent). | write `scope: []` and `not_for_repair: []` | `_investigation_view` :1429-1443; `_investigation_dispatch` :1417-1426 (a record that cannot be read answers False: the full check runs, AR-28); callers in `check` :1449, :1471, :1492, :1518 |

Item 1 count: 2 → 2 drafted.

---

## Item 3 — `observation_contract` (the one T7b–f unit not drafted)

`scripts/observation_contract.py` read whole (:1-152). Reached only through `coverage_contract.validate_obligations`
(:453-455, `errors.extend(...)`, `required` when the plan's coverage contract revision is current), i.e. the strategist's
S3 plan check (part 1's `coverage_contract:obligations` / `planning_contract:plan.obligations`).

| check | status | roles | when | requirement | door | door_needs | sites |
|---|---|---|---|---|---|---|---|
| `coverage_contract:obligations.observation` (id form: **F-P2-4**) | drafted | qa-test-strategist | always, stages S3 (see N3) | When the coverage contract revision requires it, every obligation carries an `observation_contract` object: `claim_kind` a non-empty list from `state_unchanged, no_write_attempt, response_parity, no_leak, rendered_behavior, ordinary`; `oracle_ref` `{ref, revision}` that joins a requirement of the obligation's `requirement_refs` at its revision, or a declared source-conflict decision; non-empty `surfaces`, each an object with a unique `id`, a `boundary` and a status `planned`, `observed` or `gap` — a gap with a `gap_reason` (and then no coverage of the obligation is `sufficient`), any other with an `assertion_ref` naming an existing check or step; `controls` and `completion_ref` naming existing checks or steps; `independent_expectations` a list of `{partition_ref, expected_ref, attribution_assertion_ref}` whose attribution names an existing assertion (for `response_parity` two or more, with unique partitions); `source_conflicts` a list of declared decision ids; for `state_unchanged` / `no_write_attempt` a `sequence` of exactly `before_read, action, completion, after_read` over existing refs, a separate `positive_control_ref` and a `reachability_assertion_ref`; for `no_leak` a `payload_assertion_ref`. | fix the field of the obligation's `observation_contract` the line names, then end the step again | none | `validate_observation_contract` :43-152; refs `_known_refs` :30-40, `_declared_refs` :17-27; vocabularies :7-10 |

Item 3 count: 1 → 1 drafted.

---

## Item 7 — `RD.check` (`scripts/role_digest.py`)

Read whole: `check` :368-386, `parse` :226-283, `_parse_header` :183-207, `_parse_row` :210-223, `_row_state`
:159-173, `_is_path` :176-180, `covers` :341-351, `is_halting` :354-365, `FIXABLE` :499; how the gate uses it:
`exit_gate.digest_errors` :1186-1235, `_digest_word_split` :1245-1258, `_mended_digest` :1175-1183.

Status: **drafted** — completes the requirement of joint `exit:digest_errors` (legs L4, part 1 item 7; no new id,
S-P2-6). Full sentence:

> Your final message is the handoff form: a header `<role> <stage> <window> · ok|concerns|halt|impossible`; one line
> `<id> · <state> · <reason of at most 80 characters>` for every item of the dispatch's scope (a halting digest owes no
> scope lines); nothing but those lines between the header and the path; and, last, the task-relative path of what you
> wrote (a halting digest may omit it). A verdict or a state word outside the form's list is advice, not a refusal; a
> reason over 80 characters, an absolute path under the task root, prose before the header and a missing path the
> witness names are mended by code when mending makes the form pass.

Grounds: refused = what `RD.check` still finds after the words are neutralised (`_digest_word_split` :1256-1258) and
code mending failed (:1225-1228); an empty digest is no finding (:1195). Door: as L4 (agents/<role>.md digest section).

Item 7 count: 1 → 1 drafted.

---

## Closing table per item (counts add up to part 1's "not drafted")

| item | part 1 not drafted | drafted | no row (+reason) | fork | still not read |
|---|---|---|---|---|---|
| 1 handoff_check | 2 | 2 (`binding`, `investigation`) | 0 | (F-P2-1, F-P2-2 on drafted rows) | 0 |
| 3 observation_contract | 1 | 1 | 0 | (F-P2-4 id form) | 0 |
| 4 MineRefusal groups | 8 | 7 (groups 1, 3, 4, 5, 6, 7, 8 → 12 rows) | 1 (group 2 `s6_close_from_state`: conductor-facing) | F-P2-3 (`profile.none`), F-P2-6 (`fingerprint`) inside groups 4 and 8 | 0 |
| 5 run_suite | 2 | 2 (`recover`, `begin`) | 0 | 0 | 0 |
| 7 RD.check | 1 | 1 (completes `exit:digest_errors`) | 0 | 0 | 0 |
| 10 sides | 2 | 2 (`sides.settled`, `sides.placeholders`) | 0 (manifest_put stamp notes: advice) | 0 | 0 |
| **total** | **16** | **15** | **1** | — | **0** |

Plus: 2 part-1 rows roles-checked and corrected (`execution_request:sandbox`, `:place_rows`), with corrected sentences.

---

## Forks (returned, not decided)

- **F-P2-1 (item 1) — `binding` vs `null_outcome.failures`.** Part 1's `null_outcome.failures` says "each shown failure
  is triaged once (not untriaged, not ambiguous, not multiple)" for the EMPTY path; `_binding_problems` says the
  ambiguous/multiple half on the NON-EMPTY path with the same text (`_binding_texts`, "ONE wording for both S7 paths").
  (a) narrow `null_outcome.failures` to "every shown failure has a row" and let `binding` own "once" on both paths (one
  requirement, one row); (b) keep both rows as drafted (two rows state "once"); (c) fold `binding` into
  `null_outcome.failures` as a site (then that row's sentence must say it holds on both paths). Recommend (a).
- **F-P2-2 (item 1) — investigation qualifier.** No `when` token names an S7 investigation dispatch. (a) words in the
  sentence ("In an S7 investigation dispatch ..."), `when: always` (as drafted, like F-W8 (a)); (b) a new dispatch token
  `investigation` computed by `brief_pack.dispatch_groups` from `controller.s7_part_of` (then the prompt line names it).
  Recommend (a): one row, no new token road; cost: the analyst reads the sentence in every S7 dispatch.
- **F-P2-3 (item 4) — `execution_request:profile.none` has no role door.** Text (:1794-1797) names only the gate-A
  rehearsal and `/qa-factory:qa-onboarding`. (a) role row with door "report it in your digest as an onboarding gap and
  write this one run with `--template request`" — the text gains that door in T5b, the same door `_command_from_profile`
  gives (one road); (b) conductor-only sub-row (F-W4 (b)) — but no conductor launch runs `--mine` (§2.8), so it would be
  counted `conductor_only`; (c) no row: gate A asks about it first (`gate_preflight.py:559-591`, not read whole).
  Recommend (a).
- **F-P2-4 (item 3) — id of the observation rows.** (a) sub-id `coverage_contract:obligations.observation` (C14 form,
  the transport's family); (b) own family `observation_contract:contract` (stem of the file holding the literals);
  (c) fold into `coverage_contract:obligations` (its sentence then must carry the whole observation clause). Recommend
  (a): one sentence for `obligations` cannot state it, and the errors reach the role only joined in that list.
- **F-P2-5 (item 4) — door of `execution_request:sandbox` for red_sandbox roles.** The clone and `--sandbox-root` are
  built by `red_sandbox`, not the role; the config door (`commands.one_test.cwd`) is the onboarding's. (a) door "name it
  as `tooling` in your digest" (the card's rule, `brief_pack.py:251-252`), plus "add the test file to the repository" for
  :3604; (b) no row: a code-built call the role cannot meet (code road). Recommend (a). How `red_sandbox.probe` turns a
  `mine_refused` summary into its own answer was not read (only `_run_mine` :1249-1284).
- **F-P2-6 (item 4) — `execution_request:fingerprint` (:3724) has no door.** (a) row with door "report it in your digest
  and write this one run with `--template request`" — the door `run_suite.mine` already gives `mine_unavailable` for an
  OSError/ValueError (:2019-2027); the text gains it in T5b (one road); (b) no row: factory-internal state, counted.
  Recommend (a).
- **F-P2-7 (noticed in part 1, N3) — `when: plan` on S3 rows.** Part 1 gives `when: plan` to the S3 strategist rows (3a
  header, 3b `coverage_contract:obligations`, item 9 `controller:s5_plan_gaps.rework_rows`), but `plan` is the S5
  plan-dispatch token (§2.2 `when_exclusive` with `window`; §2.6 computes it from `_s5_kind`): in an S3 dispatch it never
  holds, so those rows would sit under "Only in a plan dispatch" and never in the prompt line of an S3 dispatch.
  (a) `when: always` with `stages: ["S3"]`; (b) keep `plan`. Recommend (a); the new row of item 3 is drafted in (a).

## Lead acceptance, 13.11.2026 (t-488) — forks decided

Accepted: 15 of 16 drafted, 1 no row with reason, 0 unread; the counts add up to part 1's "not drafted". Every fork is
decided by the recommendation: **F-P2-1 (a)** `binding` owns "once" on both paths; **F-P2-2 (a)** words in the sentence;
**F-P2-3 (a)** and **F-P2-6 (a)** the role door "report it in your digest and write this one run with `--template request`"
— the refusal text gains it in T5b (one road with `_command_from_profile` / `mine_unavailable`); **F-P2-4 (a)** sub-id
`coverage_contract:obligations.observation`; **F-P2-5 (a)** door `tooling` in the digest; **F-P2-7 (a)** `when: always`
with `stages: ["S3"]` — part 1's three S3 rows are read with this correction. Corrections N1, N2 (sentences of
`execution_request:sandbox`, `:place_rows`) and N4 (`s5_precheck:sides.pending`, `sides.provisional`) REPLACE part 1's
sentences: T5/T5b take the rows from this file where the two differ. N5 (two transports with no row) and N6 go to T5b's
dispatch as named edges.

## Contradictions / analogs noticed (reported, scope not widened)

- N1: part 1 `execution_request:sandbox` sentence ≠ body (corrected row in 4.0).
- N2: part 1 `execution_request:place_rows` sentence ≠ body (corrected row in 4.0).
- N3: `when: plan` on S3 rows (F-P2-7).
- N4: part 1 `s5_precheck:sides.pending` ("no side stays pending at the window's end") ≠ body :2145-2172: a
  `pending_implementation` row is excused only by an `absent` declared side; an instance that can run owes its run;
  a row whose instances all ran real on every side is retracted. Part 1 `sides.provisional` ("a provisional side is
  backed by a provisional manifest row") covers only the marker check of :2127-2142; the body also checks the kinds
  file, `settles_on`, the home marker and `dependents` (:2078-2126).
- N5: run_suite :2856-2858 transport also carries :2837 (runtime moved) and :2807 (`StoryRootError`) with no row.
- N6: 7b's first door may meet `PT-config-write` (not checked; builder of T5b checks).

## Small choices closed

- S-P2-1: `build_mine_request` grouped by requirement: call shape (8a), S6-close (8b, no row), freshness read (8c, no
  row), scope (8d), no test (8e), join rule → `profile_command` (8f), non-pytest selector (8g), clone file → `sandbox`
  (8h), window first (8i), fingerprint (8j, fork).
- S-P2-2: one row for the `--mine` flag refusals (one door: correct the call as the refusal names).
- S-P2-3: :2827 and :2871 share `execution_request:stand` (one `_stand_refusal`, the same `run-budget.json` words).
- S-P2-4: part 1's separate `precedent` id dropped into `stand` (same requirement).
- S-P2-5: `WindowFirst` (:3661) drafted although part 1's site list (grep of `MineRefusal(`) missed it.
- S-P2-6: `RD.check` completes the `exit:digest_errors` sentence; no new id.
- S-P2-7: the `profile` door names both forms; `--profile` only where the caller takes it (`profile_door`).
- S-P2-8: every execution_request / run_suite row `when: shell`, `door_needs: shell`; stages per role (S5 automator and
  code critic, S6 runner, S7 analyst).

## Trail (read-main tree, package-relative)

- spec: §2.0-§2.9 (:84-313), §5.2-§5.6 and §9 (:410-659). Part 1: whole.
- `scripts/execution_request.py`: 1-125, 370-539 (JobStore :383-511, MineRefusal/WindowFirst :526-543), 840-1239
  (`find_active_dispatch`, `s6_close_*`, `scope_refusal`, `_admitted_outside`, `_no_test_refusal`, `_entries_of_case`),
  1660-1868 (`_profile_for`, `_command_from_profile`), 2471-2540, 2600-2704, 2730-2889 (`_probe_door`, `_probe_refusal`,
  `_observe_precedent`, `_observe_stand`), 3150-3877 (`build_mine_request` whole). Grep `^def |raise |WindowFirst` for
  the function map (unlimited).
- `scripts/run_suite.py`: 1945-2034 (`mine`), 2730-2920 (`main`), 3025-3049 (`resolve_mine_detail`).
- `scripts/probe_by_code.py`: 2670-2704, 2905-2944; grep lines :35, :47, :4735-4744, :8327.
- `scripts/red_sandbox.py`: 1235-1294, 1362-1386; grep of `_fresh_instances` with context (:1412-1417, :2018-2023);
  grep `_run_mine\(` (:1664, :1668, :2168).
- `scripts/brief_pack.py`: 142-301.
- `agents/qa-runner.md`: 50-69; grep of `run_suite` and `--mine|--sandbox-root|red_sandbox` over `agents/`.
- `references/execution-lifecycle.md`: 105-124; `references/slices/qa-runner/common-rules.md`: 28-37;
  `references/run-budget.json`: grep lines 32, 37, 38; `references/slices/qa-failure-analyst/handoff-keys.md`: grep.
- `scripts/s5_precheck.py`: 2030-2423.
- `scripts/manifest_put.py`: 821-860, 2460-2479; grep of `provisional` (all lines).
- `scripts/handoff_check.py`: 1095-1194, 1241-1270, 1405-1524.
- `scripts/observation_contract.py`: whole (1-153); `scripts/coverage_contract.py`: 436-456.
- `scripts/role_digest.py`: 100-399; `scripts/exit_gate.py`: 1160-1269.
- `scripts/execution_fingerprint.py`: grep of `raise ValueError` only (bodies not read — F-P2-6 states so).
- Negative claims and their positive controls:
  - "no agent file names `--sandbox-root`": Grep `--mine|--sandbox-root|red_sandbox` -i over `agents/`; the same call
    found `--mine` (qa-automator.md:68) and `red_sandbox` (qa-code-critic.md:68, qa-failure-analyst.md:73).
  - "`RUN_MINE` names no `--sandbox-root`/`--cwd`": read directly, `brief_pack.py:142-147` (Read, not a search).
  - "manifest_put has no placeholder code": see item 10 (control count 52, same flags).
  - "no driver_*.py prints/reads `mine_refused`/`invalid_request`/`invalid_recovery`/`run_the_window_first`":
    Grep over `scripts/` glob `driver*.py` = 0; control, same glob and shape, `mine_refused|fresh_evidence|...` found
    `driver_stage_s6.py:519, 539`.
  - A first Glob `agents/*.md` returned nothing (miscall: no claim rests on it; the agent files were reached by Grep).
