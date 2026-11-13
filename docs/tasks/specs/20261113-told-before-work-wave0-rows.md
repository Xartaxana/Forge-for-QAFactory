# Wave 0 — owed row drafts of §5.6 (told-before-work)

Draft by the designer, 2026-11-13. Parent spec: `docs/tasks/specs/20261113-told-before-work-mechanism-spec.md` (accepted).
Forks are RETURNED, never decided. Package code read ONLY from
`C:\QAFactory\forge-repo\.claude\worktrees\read-main\ai-packages\qa-factory\` (file:line below are of that tree;
paths are package-relative). Nothing in §5.2–§5.5 is edited; items 8 and 9 give corrected rows HERE.

## 0. Row form used here

Every row carries the §2.2 fields. Tables use these columns:

- `check` — id `<stem>:<family>`, sub-ids `<check_of>.<part>` (C14);
- `roles` — the qa- roles that can meet the refusal;
- `when` — `when_kinds` tokens (always, shell, no_shell, plan, window, manual, first_look, not_first_look, walk,
  conductor_answer, `move:<id>`);
- `requirement` — the sentence, in the role's terms, of what the code expects (FR-1, FR-38); where
  `requirement_from` names a carrier, the sentence column holds the carrier's key and the requirement text is
  generated from it;
- `door` / `door_needs` — what the refused role does next; `shell` when the door needs Bash, `none` otherwise;
- `role_rule` — the page the told text goes on (the key page of the role, per §2.3/§2.8); "agents/<role>.md"
  means the role's agent file;
- `sites` — file:line of the body each sentence was read from.

`text: byte-identical (<reader>)` marks a refusal text read byte-for-byte by another process; the row then
carries the text unchanged and the told sentence paraphrases nothing that the reader matches.

Status words: **drafted** (sentence read from the body), **not drafted -- body not read** (the site was located
but its condition was not read in full; never guessed), **no row** (with the reason), **not found** (with the trail).

---

## Item 1 — T6 `scripts/handoff_check.py` problem builders

Ids: the brief asks for `handoff_check:<path, list indices dropped>`. A path is computed from the contract
(dynamic), which conflicts with E1 (the id is a literal or a module constant). See **F-W1**; rows below are
drafted in form (a) (literal per builder), and the field-level family carries `requirement_from: handoff_form`
so the per-path text is generated from the contract, keeping the brief's per-path intent without a dynamic id.

Roles for every row: every qa- role that fills a handover form (census: handoff_check units are every role).
`when: always`. `role_rule: references/common-rules.md` (the handover-form section) unless noted.

| check | when | requirement | door | door_needs | requirement_from | sites |
|---|---|---|---|---|---|---|
| `handoff_check:field.blank` | always | (generated per field) every field of the form that the contract marks required is filled; a blank field is "not filled", and the form names the hint and the allowed values | write the value as a `path: value` line in the values file, then run the check again | shell / no_shell by `_doors` (see note R1) | handoff_form | :1569-1574 |
| `handoff_check:field.value` | always | (generated per field) a field with a closed list holds one of its words; a field with an open list (OPEN_LIST_CONTRACTS / OPEN_LIST_FIELDS) holds one of its words or `new: <word> -- <why>` | write one of the listed words (or `new: <word> -- <why>` where the list is open) | as R1 | handoff_form | :1579-1611, :1647-1664; text: byte-identical (`driver_dispatch.KNOWN_REFUSALS["form_vocabulary"]`, regex `is not a value of this field\|Write one of:`) |
| `handoff_check:field.max_len` | always | (generated per field) a field with a length limit is at most that many characters | shorten it (`--shorten` with `--fix`) or rewrite | as R1 | handoff_form | :1612-1617 |
| `handoff_check:required_rows` | always | a required list has one row per item in scope: the id, a state and a reason of at most 80 characters | write the rows as index lines in the values file, then run this check again | as R1 | — | :1494-1497 |
| `handoff_check:required_rows.owed_by_verdict` | always | when the verdict owes rows (the verdict word names work done on items), the list is not empty | write the rows the verdict owes, or change the verdict | as R1 | — | :1501-1511 |
| `handoff_check:required_rows.null_word` | always | a list's null-outcome word (the declared empty outcome) stands only when the list has no rows; never both | remove the word or remove the rows | as R1 | — | :1525-1532 |
| `handoff_check:tried` | always | in a contract that asks what was tried (TRIED_CONTRACTS), each tried entry states what was tried and the error it gave (TRIED_MEANING) | fill the tried entry with the attempt and its error | as R1 | — | :1680-1697 |
| `handoff_check:blocked_problem` | always | a row in state `blocked` carries `blocked.problem`; `blocked_by_env` is used only where `options_for_role` offers it to this role | write the problem, or pick a state the role is offered | as R1 | — | :1700-1735 |
| `handoff_check:findings_tooling` | always | a finding whose cause is `tooling` is repeated in `tooling_findings` | add it to `tooling_findings` | as R1 | — | :1764-1769 |
| `handoff_check:claims` | always | what the form claims is true is true on disk ("the form claims this is true, and it is not") | fix the claim or make it true | as R1 | — | `_fill_claims` :1824-1830, `_check_claims` :1851-1854 |
| `handoff_check:null_outcome` | always | a null outcome of the run view (no failure) holds only when the triage agrees: every failure shown is triaged once, rows have names, the report is readable, nothing listed is missing, nothing extra | sub-ids below | as R1 | — | `_null_outcome_view` :1268-1359 |
| `handoff_check:null_outcome.repairs` | always | no repair is pending when the null outcome is claimed | finish or record the repair | as R1 | — | :1268-1359 (branch) |
| `handoff_check:null_outcome.verdict` | always | the triage verdict is a known word | write a known verdict | as R1 | — | same |
| `handoff_check:null_outcome.names` | always | every row has a name | name the row | as R1 | — | same |
| `handoff_check:null_outcome.report` | always | the run report is readable | rerun / point at the readable report | as R1 | — | same |
| `handoff_check:null_outcome.failures` | always | each shown failure is triaged once (not untriaged, not ambiguous, not multiple) | triage it once | as R1 | — | same |
| `handoff_check:null_outcome.listing` | always | everything named in `listed_in` exists, and nothing extra stands | list exactly what exists | as R1 | — | same |
| `handoff_check:binding` | always | not drafted -- body read at :1156-1158 only (the message), condition above it not read | — | — | — | :1156-1158 |
| `handoff_check:investigation` | always | not drafted -- message at :1434-1442 read, the view's condition not read in full | — | — | — | :1434-1442 |
| `handoff_check:values_file` | always | the values file is `path: value` lines (or a JSON object): valid JSON, an object not a list, each path given once, each key a field path, no nested value | fix the line the refusal names (FILE_FIX) | as R1 | — | `parse_values` :2330-2396 |
| `handoff_check:values_apply` | always | each path names a field of this contract, by its index where it is a list row, not a contract-owned path; a list field gets a list and a one-value field one value; rows open in order | correct the path (the refusal suggests "did you mean") | as R1 | — | `_apply_one` :2532-2577, `_open_rows_for` :2466-2468, `_text_of` :2612 |
| `handoff_check:cli` | always | the call names an existing UTF-8 form with a `contract:` line and an existing values file; `--shorten` only with `--fix` | the refusal's door; a non-UTF-8 form: run `handoff_init` again (:3040-3041) | as R1 | — | `main` :3026-3058; rename failure :3088-3091 |

Head text: `refusal_text` :2821-2857 heads every block with `handoff_check: {contract} is not ready - N field(s)
below.` — text: byte-identical (`driver_dispatch.KNOWN_REFUSALS["handover_form"]`, regex `handoff_check: .* is not
ready`; resume_handoff). The head is a transport line, not a row.

Note R1 (door_needs): `_doors` picks the shell door or the no-shell door by whether the role's tools carry Bash
(role_tools). The row carries `door_needs: shell` for the shell door and the generator emits the no-shell door
for no_shell roles; the told text names both. Small choice closed (S1).

Advice: `_ask_judge` — not a refusal — no row (census: advice).

Item 1 count: 22 rows (2 not drafted -- body not read), 1 advice.

---

## Item 2 — T7a-8: the 8 `scripts/validate_artifacts.py` functions

§5.2 T7a-8 rule: a row only for a function with a qa- writer; otherwise it is conductor-facing.

| function | sites | writer | verdict |
|---|---|---|---|
| check_escape_ledger | :930-966 (docstring "V1, DORMANT IN v0") | none outside tests (`collect_pack.py:1174` "escape-ledger.jsonl has no writer") | no row: dormant, no qa- writer |
| check_charter (+ charter_form :1007-1057) | :969-1004 (dormant) | none outside tests | no row |
| check_nfr_report | :1646-1708 (dormant) | none outside tests | no row |
| check_pipeline | :1558-1566 | `stage_done.py` (`references/artifact-writers.json:12-18`) | no row: code writer |
| check_pipeline_v0 | :2586-2605 | `stage_done.py` | no row: code writer |
| check_estimation_ledger | :1569-1605 | `estimate_record.py:90` | no row: code writer |
| check_config | :2610-2620 | no writer row; PT-config-write forbids role writes | no row: conductor/person-facing |
| dispatch | :2645-2655, :1718-1719 | — | no row: router |

Item 2 count: 0 rows. Empty outcome: no function of the 8 has a qa- writer; no row is owed.

---

## Item 3 — T7b–T7f

### 3a `scripts/planning_contract.py` (T7b) — roles: qa-test-strategist; when: plan; role_rule: references/artifact-contract-plan.md

The detector (`_detector_body` :4368-4481) prints REJECT blocks that the S3 exit gate reads (`stages.json:134` lists
it as the S3 detector) — text: byte-identical (exit_gate detector_errors, `exit_gate.py:611-623`). Each family:

| check | requirement | door | door_needs | sites |
|---|---|---|---|---|
| `planning_contract:plan` | the plan validates: every obligation of the registry has its row, coverage revisions and revision marks are consistent (validate_plan + coverage_revision_errors + unmarked_revision_errors) | fix the plan row the block names, then end the step again | none | `gate_plan_errors` :286-291, validate_plan :142-214, :252-270, :273-283 |
| `planning_contract:plan.obligations` | (generated from coverage_contract.validate_obligations, see 3b) | as above | none | coverage_contract :320-456 |
| `planning_contract:contradictions` | no two plan rows contradict each other on the same requirement | resolve the contradiction in the plan | none | :1468-1494 |
| `planning_contract:branches` | every question branch kind of S3_EXIT_KINDS is accounted for (the messages :1786-2035 name what each kind expects) | write the branch the block names | none | `_branch_block_lines` :3901-3910, S3_EXIT_KINDS :1537, messages :1786-2035 |
| `planning_contract:branches.new_questions` | a new question the plan raises is well formed (as `bad_branch`) | fix the question entry | none | `s3_branch_refusals` :3214-3244, :3119-3142, :3172, :3186 |
| `planning_contract:fence.plan_row` | every requirement has a plan row | add the row | none | `fence_lines` :3867-3898 |
| `planning_contract:fence.r_column` | the md plan's R column names the requirement | fill the R column | none | same |
| `planning_contract:fence.candidate_defects` | a candidate defect is carried to its row | carry it | none | same |
| `planning_contract:fence.waiting_branch` | a row waiting on an answer has its branch | add the branch | none | same |
| `planning_contract:regression` | the regression list holds only existing tests at real paths with one runnable command per item (P24) | fix the item the block names | none | `regression_scope.problems` (`regression_scope.py:140-219`) |
| `planning_contract:targets` | a fit target names a real place | correct the target | none | `_target_line` / `fit_target_block` :4166-4248 |
| `planning_contract:requests` | a request row is in its form (shown capped by `branch_accounting.limit("refusal_units_shown")`) | fix the request | none | `_request_form` / `_request_findings` :4255-4354 |
| `planning_contract:plan_json` | the plan JSON is readable | write valid JSON | none | :4379-4382 |

Not rows:
- WARN lines (plan_warnings :294, target warnings, S3_WARN_KINDS): not a refusal — no row.
- UNREADABLE exit 3: belongs to the exit gate (FR-59), no role row.
- the waiver line :4470-4480: a person's door (PT-human-word stops a role running `waiver.py --stage`): no row.
- `unmarked_revision_errors` door is the conductor's ("reruns the S3 step (never the role)"): the row
  `planning_contract:plan` covers its requirement; its own door is conductor-side — see **F-W4**.
- `validate_case_actions` :4484-4509, `publication_manifest` :4512-4545: CLI `--kind` only, no role caller found: no row.
- CLI "not a file" stderr exit 2 :4567-4573: caller error, conductor-facing: no row.

Contradiction noticed (report, not fixed): `_regression_findings` docstring says the regression "never holds a story",
yet regression problems REJECT at :4425 and :4452. See **F-W5**.

### 3b `scripts/coverage_contract.py` (T7c)

| check | roles | when | requirement | door | door_needs | requirement_from | sites |
|---|---|---|---|---|---|---|---|
| `coverage_contract:obligations` | qa-test-strategist | plan | each obligation in the plan names its requirement, its coverage and a known state, per the messages of validate_obligations | fix the obligation entry | none | — | :320-456 (reached through validate_plan) |
| `coverage_contract:manual_current` | qa-runner | manual | points at `role_cli:manual_evidence.py write-block` (requirement_from role-commands.json) — see **F-W3** | — | — | role-commands.json | `_validate_unprepared` :694-711, `validate_manual_current` :714-800; reached by `manual_evidence.py:1320-1359` (`raise ValueError(compound(issues))`), `role-commands.json:12-17` |

Not rows: the same functions used as projection filters (`finalize_task` :566, ledger :1642, `delivery_manifest` :82):
no refusal there. `observation_contract.validate_observation_contract` (:453-455): not drafted -- body not read.

### 3c `scripts/check_delivery.py` (T7d)

No row. `main` :2630-2676 computes the delivery verdict and exits 1 when not ready; the doc scribe quotes the word
(`agents/qa-doc-scribe.md:22`). A verdict is not a refusal of a role's work; census units :84-91 are `["conductor"]`.
Empty outcome: no role-facing refusal.

### 3d `scripts/gate_preflight.py` (T7e)

No row. `main` :6399-6411 always returns 0 (prints the result; exit 2 only on bad args). Its findings reach the role
only through `stage_done.run` :1139-1155 ("stands in front of gate", driver `gate_stage` → continue), which is a
conductor road. Census :368-396 are `["conductor"]`. Empty outcome: no role-facing refusal.

### 3e `scripts/stage_done.py` (T7f) — `run`, `report_problems`, `refused`

No role row. Refusals of `run` :1086-1300: no pipeline :1100; `current_code_diff_refusal` :1105; S1 inventory :1124;
gate rehearsal :1148-1155; S9 still running :1173-1179; s9_exit (report check); journal validation :1200;
consumer_close :1222; no accepted controller stage :1241-1250; already accepted :1280-1293. Every door is the
conductor's or the person's (controller recover/rework, waiver.py, story_step finish). No agent file and no
role-commands entry names `stage_done` (trail §T). `refused` (census :952) is the inner helper of `selftest`
(:1435), not a refusal. `report_problems`: reached through s9_exit; the report-check text is read by the driver
(`KNOWN_REFUSALS["report_check"]`, `report check:` → rebuild_report) — text: byte-identical; the qa-doc-scribe meets
it through the driver's rebuild, which §5.2–§5.4 already route (no new row from this item).
`coerce_value` :92-154 (raises on `--set`) is the conductor command of `move:story_fact` — item 11 row.

Census labels units :948-954 every role + conductor by hand; with no role road, K6 "untold" would count them.
See **F-W2**.

Item 3 count: 13 (3a) + 2 (3b, one a pointer) = 15 rows; not-a-refusal 8; forks F-W2, F-W3, F-W4, F-W5.

---

## Item 4 — T5b: `MineRefusal` sites of `scripts/execution_request.py`

Sites were located (grep with two lines of context); the conditions around most of them were NOT read in full.
Per the edge invariant, a sentence is drafted only where the body was read whole.

| check | roles | when | requirement | door | door_needs | sites | status |
|---|---|---|---|---|---|---|---|
| `execution_request:sandbox` | qa-runner, qa-automator (callers of run_suite mine requests) | shell | the sandbox run directory is a task-local path the factory placed, inside the story root | name the directory the refusal prints, or let the factory place it | shell | `sandbox_run_directory` :2610-2665, `_sandbox_refusal` :2606 | drafted |
| `execution_request:place_rows` | same | shell | each placed row names a known case once | correct the row | shell | `_place_rows` :2668-2685 | drafted |
| `execution_request:active_dispatch` | — | — | — | — | — | `find_active_dispatch` :878 (:915, :927) | not drafted -- body not read |
| `execution_request:s6_close` | — | — | — | — | — | `s6_close_from_state` :952 (:957-1016) | not drafted -- body not read |
| `execution_request:case_entries` | — | — | — | — | — | `_entries_of_case` :1159 (:1193-1225) | not drafted -- body not read |
| `execution_request:profile` | — | — | — | — | — | `_profile_for` :1705 (:1721-1801) | not drafted -- body not read |
| `execution_request:profile_command` | — | — | — | — | — | `_command_from_profile` :1821 (:1828-1839) | not drafted -- body not read |
| `execution_request:precedent` | — | — | — | — | — | `_observe_precedent` :2803 (:2827) | not drafted -- body not read |
| `execution_request:stand` | — | — | — | — | — | `_observe_stand` :2845 (:2861, :2871, :2877) | not drafted -- body not read |
| `execution_request:mine_request` | — | — | — | — | — | `build_mine_request` :3186 (:3226-3262, :3298, :3316, :3333, :3435, :3446, :3459, :3474, :3499, :3585, :3604, :3724) | not drafted -- body not read |

The two drafted sentences rest on bodies read whole; their `roles` column is an inference from run_suite's callers
and is marked for the Lead's check (small choice S4). Transport: these refusals reach the role through run_suite
`main` :2857 (item 5).

Item 4 count: 2 rows drafted, 8 not drafted -- body not read.

---

## Item 5 — `scripts/run_suite.py`

| check | roles | when | requirement | door | door_needs | sites | status |
|---|---|---|---|---|---|---|---|
| `run_suite:detail_target` | — | — | duplicates §5.4 row 35 (`run_suite:detail_target`): `--detail` needs a readable request, or `--task` and `--label`; printed as `invalid_request` on stdout, exit 2 | — | — | `resolve_detail_target` :1102-1119 | pointer to §5.4 row 35 (confirmed against the body) |
| `run_suite:reparse` | qa-runner | shell | a reparse names an existing task-local run block by its canonical immutable block_id, with machine reporter evidence whose raw file is present, safe and unchanged; a mapping (needs instance_contracts) covers exactly the prior selected instances, with reporter ids non-empty and unique, and no projection collision | fix the block id / mapping the refusal names; when the evidence is missing, run the suite again instead of reparsing | shell | `main` :2740 → `reparse_run_block` :738-818 | drafted |
| `run_suite:schedule` | — | — | — | — | — | :2758 (any exception printed) | no row: a catch-all print of an unexpected error, no stated requirement; reaches the conductor seam (P22) |
| `run_suite:recover` | — | — | — | — | — | :2771 → `JobStore.recover` | not drafted -- body not read |
| `run_suite:request` | — | — | — | — | — | :2857 | no new row: transport of `validate_request` RequestError (§5.4 rows 10-19), MineRefusal (item 4 rows), StoryRootError; points at those rows |
| `run_suite:begin` | — | — | — | — | — | :2904 → `store.begin` RequestError | not drafted -- body not read |

Not rows: `run_refused` :2847, :2880 (budget refusal, conductor-facing — the budget is not the role's to change):
no row; see small choice S5.

Item 5 count: 1 row drafted + 1 pointer; 2 not drafted -- body not read; 2 no row.

---

## Item 6 — `scripts/first_look.py` `put` (roles: qa-runner; when: first_look; role_rule: agents/qa-runner.md first-look section)

| check | requirement | door | door_needs | sites |
|---|---|---|---|---|
| `first_look:put.null_reason` | a null first look carries a reason from the closed list | write one of the listed reasons | shell | :517-518 |
| `first_look:put.walked` | a first look is put once: when a walked current record exists, it is not overwritten | none for the role — it reads the current record (see F-W6) | none | :521-523 |
| `first_look:put.walk_open` | a first look is put only while its walk is open | open the walk first (the refusal's command) | shell | :529-532 |
| `first_look:put.inputs_current` | the code and the register the first look was taken on are still the current ones | take the first look again on the current code/register | shell | :535-538 |
| `first_look:put.input` | the input file is readable in the first-look form | fix the input file | shell | `_load_input` :478-491 |
| `first_look:put.rows` | each row states its path, API, auth and locator correctly (sub-ids below from the problem builders) | fix the row the problem names | shell | `put_problems` :394-428 |
| `first_look:put.rows.row` | each row has its required fields | fill them | shell | `_row_faults` :346-391 |
| `first_look:put.rows.path` | a path names a real place of the product | correct it | shell | `_path_faults` :323-343 |
| `first_look:put.rows.api` | an API entry names method and route | correct it | shell | `_api_faults` :304-320 |
| `first_look:put.rows.auth` | an auth entry names how access is got | correct it | shell | `_auth_faults` :297-301 |
| `first_look:put.rows.locator` | a locator is in the accepted form | correct it | shell | `_locator_faults` :287-294 |
| `first_look:put.rows.list` | a list field is a list | write it as a list | shell | `_list_faults` ~:280-284 |

Wording of `.rows.path/api/auth/locator` sentences is the gist of each builder's messages; the exact field names come
from the builders at drafting of T3b (small choice S6). `_store` :494-501: writes, no refusal — no row.
Census: `first_look.put_problems` (:362) qa-runner — consistent.

Item 6 count: 12 rows; 1 fork (F-W6).

---

## Item 7 — the 9 legacy legs, re-legged to the key page

Each leg of `references/stage-joints.json` re-pointed to the role's key page (§2.8); the told text stays the
same requirement as the exit gate body.

| leg | joint | roles | old told page (stage-joints line) | new leg (key page) | gate body read |
|---|---|---|---|---|---|
| L1 | `exit:scoped_errors` | qa-runner, qa-failure-analyst | artifact-contract-run.md "witness" (:58) | references/artifact-contract-run.md (key page of both; unchanged page, anchored as key) | `exit_gate.py` :1406-1418 |
| L2 | `exit:scoped_errors` | requirements-tester, case-designer, case-critic, bug-reporter | agents digest marker (:75, gap F6-51/1) | agents/<role>.md digest section (closes gap F6-51/1 when written) | :1406-1418 |
| L3 | `exit:witness_errors` | qa-code-critic | artifact-contract-automation.md (:172) | agents/qa-code-critic.md | :114-126 |
| L4 | `exit:digest_errors` | 12 roles | agents/<role>.md (:262) | agents/<role>.md (kept) | :1186-1235 |
| L5 | `exit:digest_errors` | same 12 | common-rules.md "Your final message IS the digest" (:266) | dropped as a duplicate of L4 once L4 carries the sentence (one road, AR-15) — see F-W7 | :1186-1235 |
| L6 | `exit:required_outputs_errors` | qa-code-critic | artifact-contract-automation (:336) | agents/qa-code-critic.md | :904-916 |
| L7 | `detector:S3:qa-test-strategist:branch_accounting.py` | qa-test-strategist | artifact-contract-plan.md "branch_accounting" (:463) | references/artifact-contract-plan.md (key page; kept) | :611-623 |
| L8 | `detector:S4:qa-case-critic:critic_rollcall.py` | qa-case-critic | agents (:486) | agents/qa-case-critic.md | :611-623 |
| L9 | `detector:S4:qa-case-critic:branch_accounting.py` | qa-case-critic | agents (:509, gap F6-51/4) | agents/qa-case-critic.md (closes F6-51/4 when written) | :611-623 |

Requirement of `exit:digest_errors` (read :1186-1235): the digest is refused only for what is absent — the path, a
line per scope id, the header. `RD.check` (the row-digest checker it calls) was not read: the sentence above covers
the absence checks only; any shape check inside `RD.check` is not drafted -- body not read.

Which page is "key" for each role is the §2.8 assignment; where my reading of a role's key page may differ from the
Lead's (L1, L3, L6), see F-W7.

Item 7 count: 9 legs (8 re-legged, 1 proposed dropped); fork F-W7.

---

## Item 8 — `host_adapter.role_policy` vs rows 32–39; `stage_guard` vs rows 28–31

### 8a host_adapter (`scripts/host_adapter.py` :567-625)

| row | verdict | corrected row (only where changed) | body |
|---|---|---|---|
| 32 | confirmed: the transport refusal dict for any host, before the Codex/config return, prints "FACTORY HOST POLICY: {what}. Expected: {expected}. Door: {door}."; door = the refusal's Door | — | :576-580 |
| 33 | corrected: the condition holds only on Codex with config | requirement: "On Codex, every command call carries its command text (the field words of FIELD_WORDS; in a code cell, the literal `tools.exec_command({cmd: ...})`)" | :585-588 |
| 34 | corrected: on Codex only | requirement: "On Codex, a role with its own agent file does not delegate to another agent" | :597-598 |
| 35 | corrected: on Codex only | requirement: "On Codex without a shell, Bash is used only to read: rg or Get-Content, no chaining; otherwise the CODEX_DESKTOP_TOOLS" ; door: the CODEX_DESKTOP_TOOLS tool | :599-604 |
| 36 | corrected `when` | `when: always` (no shell condition in the body); "On Codex, write_stdin carries chars" | :607-608 |
| 37 | corrected `when` | `when: always`; "On Codex, a tty is not requested" | :609-610 |
| 38 | confirmed with wording: a connector call is allowed only if read-only — listed in host_tools.read_only, an exact call in read_only_calls, or an operation name starting get/list/read/search/find/fetch/view/describe | — | :612-625 |
| 39 | confirmed: no_shell → door CODEX_DESKTOP_TOOLS; otherwise the orchestrator door, which the role cannot open, so the §5.3 door "name it in the digest" stays | — | :612-625 |

Doctor :583-584: a probe, not a refusal — no row. The "On Codex" corrections follow from :581 (everything after it
is Codex + config only); small choice S7: the qualifier goes in the sentence, not as a new `when` token (no
`codex` token exists in when_kinds) — if the Lead wants a token, that is F-W8.

### 8b stage_guard (`scripts/stage_guard.py`)

| row | verdict | corrected row | body |
|---|---|---|---|
| 28 | corrected: one row held two requirements (pathspec and manifest) — split by C14 | `stage_guard:commit.pathspec` — "a commit names its paths (or uses `--`) and never `-a`/`--all`"; door `git commit -m "..." -- <paths>`; door_needs shell. `stage_guard:commit.manifest` — "a commit does not leave a manifest case unresolved without a reason from the closed vocabulary (closed_unresolved_reasons() or `deferred:<gate>`)"; door: write the reason on the case | `rule_pathspec` :2392-2427; `rule_manifest` :1035-1051 |
| 29 | confirmed: a stash names paths after `--` that do not name qa-factory, or uses an exclude pathspec; door `git stash push -u -- <paths>` or `-- . ':(exclude)qa-factory'` | — | `rule_stash` :2441-2473 |
| 30 | corrected sentence | "before gate B the ledger word is `yes`/`after_checks` or a deliver_with_risks journal line stands; a delivery form written before that is refused — write it without those words, split it, or file it" | `rule_delivery` :1133-1164 |
| 31 | duplicate: `check` denies a WalkerError with `hooklib.WALKER_DOOR`, the same door as row 22 (PT-walker-error) → row 31 points at row 22 | `stage_guard:walker` → pointer: see row 22 | `check` :1222-1242 |

Item 8 count: 16 rows examined; 9 corrected or split (33, 34, 35, 36, 37, 28→2, 30, 31→pointer), 7 confirmed.

---

## Item 9 — `scripts/controller.py` 6443-6463 and 6886 (§5.3a owed rows)

| check | roles | when | requirement | door | door_needs | sites |
|---|---|---|---|---|---|---|
| `controller:code_review_receipts` (draft → full) | qa-code-critic | always | the review's evidence_refs name the findings file (a name containing `findings`, e.g. `work/test-code/critic-findings-<dispatch>.md`); every obligation binding carries `review_receipt_ref`, written through manifest_put; each new or changed test that is not red-by-requirement carries a sensitivity_proof or a reason | add the ref / receipt / proof the refusal names (REPAIR_MARKER, road (b)) | none | `_code_review_refusal` :6443-6463, `_code_review_problems` :7563-7627; text: byte-identical (driver `_mechanical` REPAIR_MARKER) |
| `controller:s5_plan_gaps.rework_rows` (owed second clause) | qa-test-strategist (S3 rework) | plan | a plan rework changes only blocker rows, new cases and test neighbours of new or dropped cases; the plan and the review stay readable | keep the rework to those rows | none | `_plan_rework_rows_problems` :6886-6924 |

The waiver line printed by `_code_review_refusal` and the `--words-file` door of :6886-6924 belong to the person:
not role doors, no row (they stay in the text). Item 9 count: 2 rows.

---

## Item 10 — `s5_precheck.check_sides`; `manifest_put` provisional / expectation changes

| check | roles | when | requirement | door | door_needs | sites | status |
|---|---|---|---|---|---|---|---|
| `s5_precheck:sides.declared` | qa-automator | window | each test declares its sides | declare them | none | `_sides_declared` :2042-2075 | drafted (refines §5.4 row 9 draft) |
| `s5_precheck:sides.provisional` | qa-automator | window | a provisional side is backed by a provisional manifest row | write the row through manifest_put | shell | `_sides_provisional` :2078-2142 | drafted |
| `s5_precheck:sides.pending` | qa-automator | window | no side stays pending at the window's end | settle it | none | `_sides_pending` :2145-2172 | drafted |
| `s5_precheck:sides.settled` | — | — | — | — | — | `_sides_settled` :2175+ | not drafted -- body not read |
| `s5_precheck:sides.placeholders` | — | — | — | — | — | `_sides_placeholders` :2320+ | not drafted -- body not read |
| `manifest_put:provisional` | qa-automator | window | duplicates §5.4 row 25; body :717-763 read whole and confirms it | — | — | :717-763 | pointer to §5.4 row 25 |
| `manifest_put:expectation_changes` | qa-automator | window | an expectation change names its function(s), red_attempt, green_attempt (or null), then_refs as `[{case, then: int}]`, what_changed, and a reason for a new row; the patch verdict joins; critic_verdict is a list, critic_note a string, and a note stands for each NOTE_REQUIRED_VERDICTS verdict | fix the entry the refusal names | shell | `expectation_change_problems` :1207-1305 | drafted (completes §5.4 row 28 draft; read to :1305, the function's tail past it not read) |

Advice only (census): check_copies, check_parameterization, check_relative_oracle, check_smells — not a refusal — no row.
Item 10 count: 4 drafted + 1 pointer, 2 not drafted -- body not read.

---

## Item 11 — command rows per conductor move (§5.5)

Source: `references/conductor-actions.json` :64-213 (`moves[].run`). Roles: conductor only (`when: move:<id>`).
F16 (a) binding: `precondition` / `forbidden_when` stay move data the conductor judges; these rows state only what the
COMMAND refuses.

| move | run | command row | status |
|---|---|---|---|
| rework_stage (:66) | `controller.py --operation rework …` | `controller:rework` — not drafted -- body of the rework operation not read | not drafted |
| approve_gate (:81) | nothing (driver) | no row: no command | no row |
| resume_with_words (:96) | nothing | no row | no row |
| release_and_restart (:112) | `controller.py --operation release --dispatch <id> --words-file` | `controller:release` — not drafted -- body not read | not drafted |
| go_on_as_is (:127) | `waiver.py --task --stage --block … --words-file` / `--remark` | `waiver:block` — not drafted -- body not read; the move text says "waiver.py refuses anything else" | not drafted |
| story_fact (:142) | `stage_done.py --task <T> --set key=value` | `stage_done:set` (when `move:story_fact`) — "the value of `--set key=value` is coerced to the key's type; a value that does not coerce is refused" ; door: give a value of the key's type | drafted from `coerce_value` :92-154 |
| stand_prepare (:158) | project `bring_up`; `stand_health.py --probe --env` | `stand_health:probe` — not drafted -- body not read; `bring_up` is the project's command (no factory row) | not drafted |
| revoke_exclusion (:173) | `source_exclusions.py --revoke … --words` | `source_exclusions:revoke` — not drafted -- body not read | not drafted |
| person_does (:189) | nothing | no row | no row |
| stop_here (:204) | nothing | no row | no row |
| words_carry (:25) | `waiver.py --carry-from` | `waiver:carry` — not drafted -- body not read | not drafted |

F16 contradiction check: none verified. To check once waiver.py is read: the `run` text of go_on_as_is says a block
is "one of the refusal's lines, whole, or a named block such as `probe gap: <case key>`" — the `waiver:block` row must
state exactly what waiver.py accepts, and if it accepts more or less, that is a contradiction to name.
rework_stage's precondition names a "pass of that round, as the refusal prints it" — the controller rework row must
match that printed pass.

Item 11 count: 1 row drafted, 6 not drafted -- body not read, 4 no row.

---

## Forks (returned, not decided)

- **F-W1 (item 1) — ids of T6.** The brief's `handoff_check:<path>` is computed, against E1 (literal / module constant).
  (a) literal ids per problem builder, field-level family generated from `requirement_from: handoff_form`
  (as drafted); (b) an E1 exception for computed ids, like `check_of`. Recommend (a): E1 stays whole, per-path text
  still comes from the form. Cost of (b): a second id road (P31).
- **F-W2 (item 3e) — stage_done census.** Census labels :948-954 every role + conductor by hand, but no role road reaches
  `stage_done`. (a) relabel to `["conductor"]` (a census edit, shrink-only stays: the units do not vanish); (b) keep
  and give a role row; (c) leave and accept K6 counting them untold. Recommend (a). `refused` (:952) is a selftest
  helper either way.
- **F-W3 (item 3b) — manual_current.** (a) point at `role_cli:manual_evidence.py write-block` (one road, AR-15);
  (b) a separate `coverage_contract:manual_current` row. Recommend (a).
- **F-W4 (item 3a) — unmarked_revision_errors door.** Its printed door is the conductor's ("reruns the S3 step (never
  the role)"). (a) keep it inside `planning_contract:plan` with the role door "fix the plan row"; (b) split a
  conductor-only sub-row. Recommend (b) if the role can never satisfy it; I could not establish which from the body
  read (:273-283).
- **F-W5 (item 3a) — regression REJECT vs docstring.** `_regression_findings` says regression "never holds a story";
  :4425/:4452 REJECT. (a) the docstring is stale — row stays; (b) the REJECT is a defect — row drops and the code
  changes (out of this wave). Recommend: the Lead reads :4420-4455 and decides; the row is drafted on present behavior.
- **F-W6 (item 6) — `first_look:put.walked`.** The role has no door (a walked current record is not overwritten).
  (a) the door is "read the current record and go on" (not a refusal of the role's work → advice, no row);
  (b) keep a row with door "none -- report it in the digest". Recommend (a) if the walk record is the role's own
  result; the brief's rule returns door-less rows as a fork.
- **F-W7 (item 7) — key pages.** L1/L3/L6 re-legs depend on which page is the role's key page (§2.8), and L5 is
  proposed dropped as duplicate of L4. (a) as drafted; (b) keep L5 as a second leg. Recommend (a) (one road).
- **F-W8 (item 8a) — a `codex` when token.** Rows 33-37 hold only on Codex. (a) qualifier in the sentence (drafted);
  (b) add a `when` token `codex`. Recommend (a): no new token road for one host (AR-5).

## Lead acceptance, 13.11.2026 (t-480) — forks decided, remainder re-dispatched

The drafted rows are accepted as the input of wave 3; "not drafted -- body not read" rows are NOT accepted as absent:
they go to two fresh designer drafts — role-facing remainder (items 1, 3, 4, 5, 7, 10) in
`20261113-told-before-work-wave0-rows-part2.md`, conductor moves (item 11 + the F16 check) in
`20261113-told-before-work-wave0-rows-part3.md`. A wave-3 node whose rows sit in part 2 or 3 waits for that part.

| fork | decided | why |
|---|---|---|
| F-W1 | (a) literal ids per problem builder | E1 stays whole, one id road (P31) |
| F-W2 | (a) census relabel of the `stage_done` units to `["conductor"]` | no role road reaches `stage_done`; units do not vanish, the ratchet holds; the edit rides in T7f |
| F-W3 | (a) pointer at `role_cli:manual_evidence.py write-block` | one road (AR-15) |
| F-W4 | (b) conductor-only sub-row `planning_contract:plan.unmarked_revision` | Lead read :273-283: the printed door is "the conductor reruns the S3 step (never the role)" — the role cannot satisfy it |
| F-W5 | (a) the row stays | Lead read :3913-3926 and :4408-4456: "never holds a story" in the docstring speaks of a check that CANNOT RUN (WARN, `[]`); found problems REJECT the S3 exit by P24 (the list is right the first time). Docstring is ambiguous, not the code; rewording it rides in T7b |
| F-W6 | (a) advice, no row | a walked current record is the role's own result; nothing of its work is refused |
| F-W7 | (a) as drafted, L5 dropped | one road |
| F-W8 | (a) "On Codex" in the sentence | no token road for one host (AR-5) |

Small choice S4 (roles of the two `execution_request` rows) is checked in part 2 against the callers, not by inference.

## Small choices closed

- S1: `door_needs` for handoff_check rows is the shell door; the no-shell door is generated by `_doors` from role_tools.
- S2: sub-ids for `_null_outcome_view` follow its branch groups, not each message.
- S3: dormant / code-written validators get "no row" with their writer named, not a fork (§5.2 T7a-8 rule settles it).
- S4: roles of the two drafted execution_request rows inferred from run_suite callers; marked for the Lead's check.
- S5: budget refusals of run_suite are conductor-facing, no row.
- S6: first_look sub-row wording is the gist of each builder; exact field names fixed when T3b writes the told text.
- S7: "On Codex" goes in the sentence.

## Closing table

| item | rows (drafted + pointers) | not drafted -- body not read | not-a-refusal / no row | forks |
|---|---|---|---|---|
| 1 T6 handoff_check | 20 | 2 | 1 (`_ask_judge`) + head line | F-W1 |
| 2 T7a-8 | 0 | 0 | 8 | — |
| 3 T7b-f | 15 (1 pointer) | 1 (observation_contract) | 8 + check_delivery, gate_preflight, stage_done | F-W2, F-W3, F-W4, F-W5 |
| 4 T5b | 2 | 8 | 0 | — |
| 5 run_suite | 2 (1 pointer) | 2 | 2 (+ budget) | — |
| 6 first_look put | 12 | 0 | 1 (`_store`) | F-W6 |
| 7 legacy legs | 9 legs | RD.check | — | F-W7 |
| 8 host_adapter / stage_guard | 16 examined (9 corrected/split, 7 confirmed) | 0 | 1 (doctor) | F-W8 |
| 9 controller | 2 | 0 | 2 person doors | — |
| 10 s5_precheck / manifest_put | 5 (1 pointer) | 2 | 4 advice | — |
| 11 conductor moves | 1 | 6 | 4 | — (F16 check pending waiver.py) |

## Trail (read-main tree, package-relative)

- spec: whole (§0–§11, fix rounds).
- `scripts/handoff_check.py` 600-660, 1131-1186, 1241-1445, 1446-1631, 1680-1855, 2312-2397, 2411-2485, 2528-2647, 2808-2930, 2954-3101.
- `scripts/validate_artifacts.py` 930-1057, 1558-1605, 1646-1719, 2586-2655; `scripts/collect_pack.py:1174` (grep);
  `references/artifact-writers.json` 1-40.
- `scripts/planning_contract.py` 142-291, 1468-1494, 1537, 1786-2035, 3119-3244, 3867-3910, 4166-4573; `scripts/regression_scope.py` 138-247.
- `scripts/coverage_contract.py` 320-456, 694-800; `scripts/manual_evidence.py` 780-799, 1300-1369; `references/role-commands.json` 1-30.
- `scripts/check_delivery.py` 2630-2676; `scripts/gate_preflight.py` 6399-6411; `scripts/stage_done.py` 92-154, 1086-1300, 1435.
- `scripts/execution_request.py`: grep -A2 on `MineRefusal(`; read whole 2600-2685.
- `scripts/run_suite.py` 738-818, 1102-1119, 2733-2776, 2840-2910.
- `scripts/first_look.py` 280-553.
- `references/stage-joints.json` (the 9 legs); `scripts/exit_gate.py` 114-126, 611-623, 904-916, 1186-1235, 1406-1418.
- `scripts/host_adapter.py` 567-625; `scripts/stage_guard.py` 1035-1051, 1133-1164, 1222-1242, 2392-2473.
- `scripts/controller.py` 6443-6463, 6886-6924, 7563-7627.
- `scripts/s5_precheck.py` 2042-2172; `scripts/manifest_put.py` 717-763, 1207-1305.
- `references/conductor-actions.json` 1-213; `scripts/driver_dispatch.py` 65-106.
- `scripts/tests/fixtures/judgment-census.json` (units of the files above).
- Negative claims with controls: "no agent file names stage_done" — Glob of `agents/*.md` (12 files) plus a `\.py`
  count over them as the positive control, then the count for `stage_done` = 0; the brace-glob Grep form failed its
  control and was not used for any claim. "role-commands has no stage_done key" — same method on
  `references/role-commands.json` (control: key `manual_evidence.py write-block` found).
