# FV3-31 card - the producer of `inputs_read` for the two S5 critic forms (draft, t-1314)

Node `live-run-fvf/3/FV3-31`, feature F19. Source: critic t-1257 F3 (`docs/tasks/specs/reviews/t-1257-fv3-19-code.md:87`), the cloud
builder's question report `docs/tasks/specs/reports/20261118-fv3-31-report.md` (Q1-Q3). Lead facts: Q1 (the table is
`references/stages.json`), Q2 decided (b) (a separate key read only by `brief_pack.reviewed_dispatch` on S5; absent = today;
`acceptance_by` stays off S5), Q3 open (laid out in §2.3, recommended in F1). Draft status: forks F1-F4 are the Lead's; the builder
card in §3 is written for the recommended options and names what changes when a fork goes the other way.

## §0 Facts the draft rests on (measured by the designer with Read/Grep; no shell)

| # | fact | carrier |
|---|---|---|
| f1 | S5 row has `roles: [qa-automator, qa-code-critic]`, no `acceptance_by`, `rework_mode: resume`; S4 has `acceptance_by: qa-case-critic` | `references/stages.json:136-212` |
| f2 | `reviewed_dispatch` has two branches: own-stage `acceptance_by == role` (S4) via `acceptance.stage_author_dispatch`; consumer search `acceptance_by == role and role not in roles` (S6->S7, S7->S8); else `("", "", False)` | `scripts/brief_pack.py::reviewed_dispatch` (3713-3728) |
| f3 | its callers: `reviewed_dispatch_id` -> `story_step._author_argv`; `reviewed_dispatch_lines` -> `build` head line | `brief_pack.py:3733,3745,4536`; `story_step.py:335` |
| f4 | `_author_argv` returns `[]` unless the contract text holds `handoff.AUTHOR_TOKEN` (`<the author's dispatch>`); it has no dispatch id or record parameter; `_handoff_form` holds `record` and `dispatch_id` at the call | `story_step.py:321-338, 351-370` |
| f5 | `fill_head` replaces `AUTHOR_TOKEN` text-wide and inserts `AUTHOR_NOTE` above `inputs_read:` only when filled | `handoff_init.py::fill_head` (152-180) |
| f6 | both S5 critic forms spell the author as `<the automator's dispatch>` in `inputs[0].path` and have ONE `inputs_read` row `<path exactly as the author listed it>`; no `AUTHOR_TOKEN` anywhere | `handoffs/s5-critic-to-automator.yaml:12-27`; `handoffs/s5-critic-plan-to-automator.yaml:23-41` |
| f7 | `<the automator's dispatch>` occurs in the package only in those two forms (+ prose in `tests/story_step_common.py:197`); `handoff.py:406` calls `AUTHOR_TOKEN` "the ONE token of the contracts that review a dispatch" | Grep over `ai-packages/qa-factory`, fixtures excluded |
| f8 | S5 critic contracts have no `repair_carries` row (carry nothing); no `acceptance_verdict_at` (so `drop_unowed_acceptance` returns them unchanged) | `handoffs/index.yaml:79-95`; Grep `acceptance_verdict_at` in `handoffs/` (2 hits, S7/S8) |
| f9 | `inputs_read[].version` has a deriver (sha256 of the row's path); `<hash>` is the template spelling of a measured version (4 forms use it) | `handoff_check.py:496-501, 752`; `handoff_init.py:231` |
| f10 | S5 runs parallel windows (`--parallel-window`, `parallel_windows != 1`); a plan dispatch (purpose `s5_plan`) precedes the windows | `driver_dispatch.py:671, 3043`; `controller.py:6719-6725` |
| f11 | `acceptance.stage_author_dispatch` = the LAST accepted dispatch of `roles[0]` in the current life, any scope, any purpose | `acceptance.py:1449-1462` |
| f12 | `brief_pack.advice_of` already walks "the latest ACCEPTED qa-automator window dispatch created before this critic whose scope shares a case" (break at own id; `s5_part_of != plan`; `probe_debt.bare_case_id`) | `brief_pack.py:3620-3645` |
| f13 | A22 form layer counts `handoff.contract_of(stage, role)` without purpose: `s5-critic-to-automator` only (the plan form is not a candidate) | `role_load.py::_form_candidates`, `_static_form_layer` (483-513) |
| f14 | process ratchet qa-code-critic 21782, slack 0 in BOTH directions (below the row is red too: "lower to") ; tokens = ceil(bytes/4) | `references/role-load.json:31`; `role_load.py:140-142, 280-287` |
| f15 | the only slice listing S5 critic keys: `references/slices/qa-code-critic/handoff-keys.md:20-23` (`inputs_read[].path` hint) | Grep `inputs_read\[\]\.path` over `references/slices` (1 hit) |
| f16 | brief ratchet `ROLE_BRIEF_BYTES_MAX["qa-code-critic"] = 7189`, measured on the `seed(root, "QA-9")` world | `tests/test_brief_pack.py:2411-2436` |
| f17 | test classes: `test_handoff_init.py` keep (table, fast); `test_brief_pack.py` keep but slow (27.3 s), `test_field_producers.py` keep but slow (17.1 s), `test_contract_slices.py` slow; `test_handoff_init_author.py`, `test_window_artifacts.py`, `test_stage_done.py` QUARANTINE | `tests/test-layers.json` (keep 42-7163, quarantine 7217-); `scripts/slow_tests.json:13,23,39` |
| f18 | `test_handoff_init_author.py::test_s5_contracts_get_no_author_arg` asserts the token is NOT in both S5 contracts and `_author_argv(S5, qa-code-critic) == []` | `test_handoff_init_author.py:58-63` |

Estimates (the Lead measures; no shell here): e1 the current qa-code-critic `process_tokens` equals 21782 after t-1257 F1 landed -
`python -B ai-packages/qa-factory/scripts/role_load.py --role qa-code-critic --json`; e2 the `seed(...,"QA-9")` world of
`role_brief_ratchet` holds no accepted qa-automator dispatch (so no new brief line there) - read `test_brief_pack.py::seed`;
e3 FV3-32 (t-1312) owns do not include `scripts/tests/test_handoff_init.py` - read t-1312's `owns:`.

## §1 Architecture walk

AR-n touched (`design/architecture.md`), each with the change check the builder runs and reports:

- AR-22 (every field read has a producer): the S5 critic's `inputs_read[0]` (the reviewed author's form) gains its producer
  (code prefill), its version stays the deriver's. Check: grep `inputs_read` over `scripts/`, `handoffs/`, `references/` for S5
  readers (case-insensitive, positive control on `s4-case-critic-to-designer`); narrow calls of `test_field_producers.py` (DoD).
- AR-13 (one reader per fact): "which qa-automator dispatch this S5 critic reviews" has one walker - extracted from `advice_of`
  (f12) and called by `advice_of` and `reviewed_dispatch`; S4 keeps the gate's reader (`stage_author_dispatch`) so its brief line
  and `stage_done` still bind the same id. Check: grep `scripts/` for `role") == "qa-automator"` walks with `status") == "accepted"`;
  name each (known: `advice_of`, `brief_pack.delta_lines` - other predicate: either role, not DISCOUNTED, form on disk -
  `controller.py:7015` - "a critic ran" -, neither the same fact).
- AR-15 (one survivor): `<the automator's dispatch>` is a second spelling of `AUTHOR_TOKEN`; both forms move to the one token.
  Check: grep `the automator's dispatch` over the package -> 0 template hits after.
- AR-1 (closed variety is a data row): the reviewer of S5 is a `stages.json` key, read by key; the new code branch never compares
  a stage id or a role name. Check: the diff of `reviewed_dispatch` holds no `"S5"` / `"qa-code-critic"` literal.
- AR-28 / FR-59 (an unknown never passes; a guessed author never stands): every unknown -> no id, token stays a placeholder (§3 edges).
- AR-20 (ratchets): no raise of `process_ratchet_tokens` (A22) nor `ROLE_BRIEF_BYTES_MAX`; measured before/after.
- AR-21 (`inputs_read` is the proof of reading): the row binds the review to the author's form it read.
- AR-19 (stage twins): S4 critic prefill (token road) is the twin; S5 joins the same road; S7/S8 consumers unchanged.
- AR-10: the requirement (`Reviewed dispatch:` line) reaches the S5 critic before the work.

Checks added or altered: none. The new branch is a reader (owner: data/code), the prefill and the brief line produce data; no
refusal, no verdict, no census unit (`judgment-census.json` names none of `reviewed_dispatch`, `advice_of`, `_author_argv`: Grep 0,
control `brief_pack` 3). AR-29 census class: n/a. Commit lines: an `architecture:` line naming the AR-n above and a
`judgment: none -- <why>` line, both in the forms `tools/architecture_gate.py` carries (its module docstring, items 1 and 6).

`variety: none -- internal S5 reviewer wiring (a stage row key, a reader branch, two form rows); no project-shape axis is read, held or narrowed`

## §2 Design

### 2.1 The Q2 (b) key

- Name and shape: `"reviewed_by": "qa-code-critic"` on the S5 row of `references/stages.json`, beside `roles`. A role id string.
  `reviewed_by` = "the role of this stage that reviews its author's dispatch without accepting the stage"; it is NOT
  `acceptance_by` (the gate switch) and NOT `stage_critic` (the name the cloud report floated: it collides with
  `brief_pack.stage_critic_names`, which is keyed on `acceptance_by` and must not start reading this key - X2-1 brief files).
- Valid only when: a non-empty string, a member of the row's `roles`, not `roles[0]` (the author), not equal to the row's
  `acceptance_by`. Anything else reads as absent and prints one stderr line `brief_pack: reviewed_by of <stage> is <repr>: not a
  reviewing role of the stage; read as absent` (precedent: `acceptance_reads`, `brief_pack.py:3699-3709`).
- The ONE reader: `brief_pack.reviewed_dispatch`. Nobody else reads it (not `stage_critic_names`, `awaits_acceptance`,
  `acceptance.*`, `stage_done`, `stage_guard`, `controller`, `driver_*`).
- Position in `reviewed_dispatch`: AFTER the own-stage `acceptance_by` branch, BEFORE the consumer search. Invariant: every answer
  the two existing branches give today stays byte-identical (S4 critic, S6/S7 consumers, every other role); the new branch is
  reachable only for `role == own["reviewed_by"]` on a valid row, and a stage whose `acceptance_by` names the role never reaches it.

### 2.2 Which author the S5 critic is told (F2)

Recommended (F2 a): `reviewed_dispatch(stage, role, state, pipeline, dispatch=None)` - `dispatch` is the reviewing dispatch's
record (`id`, `scope`, purpose binding). On the `reviewed_by` branch the author is `reviewed_author_of(state, dispatch, stage,
roles[0], part)`, the walk extracted from `advice_of` (f12): the LAST dispatch, in `dispatch_identity.records` order and created
before `dispatch` (the walk stops at its own id), of `stage` and `roles[0]`, status `accepted`, of the same `s5_part_of` part as
`dispatch`, and - for the part `window` - sharing a `bare_case_id` with `dispatch["scope"]` (the part `plan` needs no case
overlap). It returns `(id, met_self)`. Answer: `(stage, id, True)` when `met_self` and `id`; else `("", "", False)` (today).
`advice_of` calls the helper with part `window` and keeps its result byte-identical (it ignores `met_self`, as today).

Direction of error (rule 1: an advice walk now decides a prefilled row and a brief instruction): it may err only toward naming
NOTHING, never a wrong dispatch. Adversarial inputs that must stay on that side: two accepted parallel windows, the critic of W1
created after W2's automator (-> W1's automator); an automator of the same cases accepted AFTER the critic was created (-> not
named); a plan critic with window automators present (-> the plan automator only) and a window critic with an accepted plan
automator (-> never the plan's); a critic window with an empty scope (-> nothing); the critic's own id absent from the records
(-> nothing); instance-suffixed case ids (normalised by `bare_case_id`); a released/cancelled automator (status not `accepted`
-> skipped); a superseded accepted automator followed by its accepted rework (-> the rework, the later one).

### 2.3 Q3 - the prefill road (F1)

Option A (recommended): put `AUTHOR_TOKEN` in both S5 critic forms. `inputs[0].path` becomes
`work/handoffs/<the author's dispatch>.yaml` (-3 bytes); a new FIRST `inputs_read` row
`- path: work/handoffs/<the author's dispatch>.yaml` / `version: <hash>` (about 73 bytes, f9); the comment above `inputs_read`
says row 0 is the author's form and the rest one row per entry of the author's `inputs`. `fill_head`, `drop_unowed_acceptance`,
`_author_argv`'s token gate, `form_filler` (ctx `author_dispatch`) and `dry_stub.author_dispatch_of` (the brief line) all
already serve the token: zero code in `handoff_init.py`. Costs: (i) `s5-critic-to-automator.yaml` must net to the SAME process
tokens (f14, slack 0 both ways; role-load.json never edited) - about 70 bytes trimmed from its own comments, meaning kept; (ii)
the qa-code-critic slice regenerates (f15) and counts inside the same measure; (iii) the quarantine pin f18 turns red by design
(F4); (iv) the plan form grows about 70 bytes (not an A22 candidate, f13).

Option B: a token-less prefill rule in `fill_head` (e.g. "an `author_dispatch` with no token in the text inserts a first
`inputs_read` row"). Costs: (i) a second road for one action (prefill the reviewed row) beside the token road of S4/S7/S8 -
rule 6 / P31 / SIBLING_MAP axis 34: a spec defect unless the owner says so; (ii) `_author_argv`'s token gate must open for these
contracts by a contract list in code (AR-1 breach) or a contract key (A22 bytes again); (iii) contract-neutrality fails: the
template, the slice, `handoff.spec`, `form_filler` and the dry worlds never see the inserted row, so dry and live forms diverge;
(iv) `drop_unowed_acceptance` removes rows by the token, a third shape it would not know; (v) it edits `handoff_init.py`, so it
waits for FV3-32 (t-1312) on that file. Gain: zero form bytes, no slice change.

### 2.4 Both worlds (TEMPORAL, rule 11 (i))

The move that creates the new artifacts is the builder's ONE commit: the `reviewed_by` key and the token rows land together, so
the shipped package is never half-way.
- Before (today's package): no key, no token -> no brief line, no prefill (f2, f4).
- After: key + token -> the matched author is named in the brief and prefilled in `inputs[0]`/`inputs_read[0]` of the critic's
  copy, with `AUTHOR_NOTE` above `inputs_read`.
- Key absent/invalid with the token present (an edited or broken `stages.json`): the reader answers today; `_author_argv` sees
  the token, gets `""`, passes nothing; the token stays a placeholder in both rows (the S4 unknown world; the role fills it).
- Key present, token absent (forms reverted): the brief line is printed, `_author_argv` returns `[]`; the role follows the line.

## §3 Builder card

given: C:/QAFactory/forge-repo/docs/tasks/specs/20261118-fv3-31-s5-critic-inputs-read-card.md (§0-§2, §4); C:/QAFactory/forge-repo/docs/tasks/specs/reports/20261118-fv3-31-report.md; C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/brief_pack.py::reviewed_dispatch, ::reviewed_dispatch_id, ::reviewed_dispatch_lines, ::advice_of, ::build; C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/story_step.py::_author_argv, ::_handoff_form; C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/handoff_init.py::fill_head, ::drop_unowed_acceptance; C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/role_load.py::process_ratchet_problems
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/stages.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/brief_pack.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/story_step.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/handoff.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/handoffs/s5-critic-to-automator.yaml
C:/QAFactory/forge-repo/ai-packages/qa-factory/handoffs/s5-critic-plan-to-automator.yaml
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/slices/qa-code-critic/handoff-keys.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_handoff_init.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_brief_pack.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/changelog.d/fv3-31-s5-critic-reviewed-row.md
non-goals: the S5 acceptance gate (`acceptance_by` stays off S5; no `stage_done --acceptance` S5 wording, no X2-1 brief files); references/role-load.json (never edited); handoff_init.py (no change: FV3-32 t-1312 owns `empty_optional_lists`); any quarantine file (`test_handoff_init_author.py`, `test_window_artifacts.py`, `test_stage_done.py`: not run, not fixed, not edited); agents/qa-code-critic.md (A22); `brief_pack.delta_lines`
handoff: C:/QAFactory/forge-repo/docs/tasks/specs/reports/20261118-fv3-31-build-report.md (items, witness, the base and after A22 numbers, the bytes trimmed and why, the regenerated slice diff stat, report lines for canon-judged and quarantine files)
edges: E1-E14 below, each with its invariant
DoD: `python -B ai-packages/qa-factory/scripts/tests/test_handoff_init.py` + the narrow calls N1-N4 below, from the worktree root
siblings: FV3-32 (t-1312, `handoff_init.empty_optional_lists`): no shared code file under option A (this node does not edit handoff_init.py; check e3 for test_handoff_init.py); SIBLING_MAP axis 34 (one road: the S5 prefill rides the S4 token road); AR-19 twin S4 critic prefill (unchanged)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261118-fv3-31-s5-critic-inputs-read-card.md

### Items (top-down; the A22 measure first)

0. Base: record `python -B ai-packages/qa-factory/scripts/role_load.py --role qa-code-critic --json` (`process_tokens`, `total_bytes`)
   and run `test_handoff_init.py` green before any edit.
1. `references/stages.json`: add `"reviewed_by": "qa-code-critic"` to the S5 row right after `roles`. Nothing else in the file.
2. `brief_pack.py`:
   (a) extract `reviewed_author_of(state, dispatch, stage, author_role, part) -> (str, bool)` from `advice_of`'s walk (§2.2);
   `advice_of` calls it with `("S5", "qa-automator", "window")` and returns exactly what it returns today;
   (b) `reviewed_dispatch(stage, role, state, pipeline, dispatch=None)`: the `reviewed_by` branch of §2.1-§2.2 at the position of
   §2.1; the validity rule and the one stderr line of §2.1; docstring names the key and the `dispatch` argument;
   (c) `reviewed_dispatch_id` and `reviewed_dispatch_lines` take `dispatch=None` and pass it through, nothing else changes in them;
   (d) `build`: the `reviewed_dispatch_lines(...)` call passes `dispatch=dict(dispatch or {}, id=dispatch_id)`.
3. `story_step.py::_author_argv`: an optional `dispatch=None` parameter passed to `reviewed_dispatch_id`; `_handoff_form` passes
   `dict(record if isinstance(record, dict) else {}, id=dispatch_id)`. The token gate and the `except` stay as they are.
4. Both S5 critic forms, option A of §2.3: `inputs[0].path` -> `work/handoffs/<the author's dispatch>.yaml`; a new first
   `inputs_read` row `path: work/handoffs/<the author's dispatch>.yaml`, `version: <hash>`; the comment above `inputs_read` says
   row 0 is the author's form, then one row per entry of the author's `inputs`. `s5-critic-to-automator.yaml`: trim its own
   comments so item 0's `process_tokens` is reached EXACTLY again (E11); name each trimmed sentence and why its meaning holds.
5. `handoff.py:406`: the comment of `AUTHOR_TOKEN` adds "the S5 code critic" to its list. Comment only.
6. `python -B ai-packages/qa-factory/scripts/contract_slices.py --write`; commit the regenerated slice only (never hand-edited);
   re-measure item 0 after it (the slice is inside the same measure).
7. `changelog.d/fv3-31-s5-critic-reviewed-row.md`: English, no Cyrillic: the S5 code critic's form arrives with the reviewed
   automator dispatch filled; `stages.json` `reviewed_by`.
8. Tests: the `test:` lines below, top-down until the test lines reach the code lines; the rest is reported as not written.
9. Commit: `architecture:` and `judgment: none -- <why>` lines in the forms of `tools/architecture_gate.py`.

### Edges (behaviour + invariant)

- E1 key absent (TEMPORAL "before" world, or removed): S5 answers `("", "", False)`; no brief line; `_author_argv` -> `[]`; token
  stays in both rows. Invariant: absent key = today's reader answer; no author is guessed (FR-59).
- E2 key invalid (not a string, empty, not in `roles`, `roles[0]`, equal to `acceptance_by`): as E1 plus one stderr line. Invariant:
  `reviewed_by` never changes an answer `acceptance_by` gives and never reaches the consumer search, `awaits_acceptance`,
  `stage_critic_names` or any gate.
- E3 `stages.json` unreadable (`hooklib.load_ref_json` -> `{}`): every role `("", "", False)` as today; `_author_argv` -> `[]`.
  Invariant: an unreadable table names no author and raises nothing out of `_author_argv`.
- E4 no reviewing record (`dispatch=None`), or its id not met in the records: `("", "", False)`. Invariant: S5 never names an
  author it could not bind to THIS dispatch.
- E5 parallel windows / created-after: per §2.2. Invariant: a review row never names another window's dispatch, nor one created
  after the critic.
- E6 plan vs window: same part only. Invariant: a plan review never names a window author and a window review never the plan's.
- E7 no match: `("", "", False)`, NOT the "none yet" line. Invariant: no false "no accepted dispatch exists at S5" claim while
  other windows have one.
- E8 a form without the token (any other contract) or a template without `inputs_read:`: `_author_argv` `[]`, no `AUTHOR_NOTE`
  (as today). An author form with no `inputs`: row 0 alone keeps `inputs_read` non-empty; row 1 is the role's, as on S4.
  Invariant: the S5 forms behave as the S4 form in the same world.
- E9 carried/prefilled rows: no `repair_carries` row for S5 critics (f8), so a rework critic's form gets the CURRENT matched author,
  never the parent's row; an existing form on disk is never rewritten (`handoff_init` exists check); `empty_optional_lists` (runs
  last) never touches `inputs_read` (a required list); `drop_unowed_acceptance` returns S5 forms whole; `version: <hash>` is filled
  by the deriver at check time. Invariant: a row naming an older author's form is never carried into a new review.
- E10 both S5 critic forms get items 4 identically. Invariant: after the commit `<the automator's dispatch>` exists in no template.
- E11 A22: `process_tokens` after == base, exactly (below is red too, f14); role-load.json untouched. If the meaning of the trimmed
  comments cannot be kept, stop and return a question - never a raise, never a lowered row.
- E12 brief ratchet: if `role_brief_ratchet` would go red for qa-code-critic (e2 false), no raise: return a question with the number.
- E13 the S5 brief line says "must" (`stage_done.reviewed_row_rule`) and no S5 gate reads it: keep the one wording (F3).
- E14 dry worlds: `dry_stub.author_dispatch_of` now fills the S5 critic token from the brief line; a dry S5 critic with no line
  keeps an unfillable token (`form_filler` E12) - canon judges `test_story_run_s5*`; a report line, not a local run.

### Test lines (strongest first)

1. `test: test_handoff_init.py::AUTHOR_ROWS (new table beside ROWS, one call of the real script per row) - S5 critic usual
   contract and `--purpose s5_plan`, each with `--author-dispatch <id>`: `inputs[0].path` and `inputs_read[0].path` are
   `work/handoffs/<id>.yaml`, `AUTHOR_NOTE` is the line above `inputs_read:`, `inputs_read[1].path` keeps its placeholder; the same
   two without `--author-dispatch`: the token stays in both rows, no `AUTHOR_NOTE`, `header` and `review` present | expected from:
   §2.3 option A, E8-E10, FR-59, `handoff_init.fill_head` docstring`
2. `test: test_brief_pack.py::s5_reviewed_dispatch_rows (new table function, registered in main) - rows: two parallel windows ->
   the critic's own automator, and the `Reviewed dispatch:` line names its path; an automator of the same cases created after the
   critic -> not named; plan critic -> plan automator; no matching window -> ("", "", False) and no line; `dispatch=None` ->
   ("", "", False); the S5 row without `reviewed_by` (patched `_stages`) -> ("", "", False); S4 critic and S7 analyst answers
   unchanged | expected from: §2.1-§2.2, E1, E4-E7, AR-13, FR-59`
3. `test: test_brief_pack.py::s5_reviewed_dispatch_rows row "prefill = brief" - `story_step._author_argv("S5", "qa-code-critic",
   "s5-critic-to-automator", root, dispatch=<critic>)` returns the id the line names (Controller patched) | expected from:
   `reviewed_dispatch` docstring TR4-12 (2) ("they never name different dispatches")`
4. `test: none -- A22 is a measure of an existing ratchet, judged in canon by test_role_load.py / audit A22 | expected from: f14, Lead fact Q3`

red-before: none is a defect line (new behaviour); rows in `test_brief_pack.py` carry `red-before: not run -- test_brief_pack.py canon judges`.

### Narrow calls of the DoD (canon-class files are never run whole here)

- N1 `python -B -c "import sys; sys.path[:0]=['ai-packages/qa-factory/scripts/tests','ai-packages/qa-factory/scripts']; import test_brief_pack as T; T.s5_reviewed_dispatch_rows()"`
- N2 `python -B -c "import sys; sys.path[:0]=['ai-packages/qa-factory/scripts/tests','ai-packages/qa-factory/scripts']; import test_field_producers as T; T.an_excused_list_stays_untouched_and_a_required_one_is_refused_when_no_file_exists(); T.every_derived_field_meets_its_deriver()"`
- N3 `python -B ai-packages/qa-factory/scripts/role_load.py --role qa-code-critic --json` (after item 6; equals item 0)
- N4 a two-window `advice_of` probe on a synthetic state, before and after item 2(a), outputs compared verbatim (`test_window_artifacts.py` is quarantined)
- report lines: `not run locally: test_brief_pack.py, test_field_producers.py, test_contract_slices.py, test_handoff.py, test_story_run_s5*.py, test_judgment_census.py, canon judges`; the quarantine pin f18 (F4).

## §4 Readers of every touched file (rule 7)

The `owns_readers` block was NOT attached to the brief. The Lead runs before the builder dispatch and attaches:
`python -B tools/owns_readers.py --paths ai-packages/qa-factory/references/stages.json ai-packages/qa-factory/scripts/brief_pack.py ai-packages/qa-factory/scripts/story_step.py ai-packages/qa-factory/scripts/handoff.py ai-packages/qa-factory/handoffs/s5-critic-to-automator.yaml ai-packages/qa-factory/handoffs/s5-critic-plan-to-automator.yaml ai-packages/qa-factory/references/slices/qa-code-critic/handoff-keys.md --names reviewed_dispatch reviewed_dispatch_id reviewed_dispatch_lines advice_of _author_argv reviewed_by --readers`.
Hand greps meanwhile (Grep tool, each with its count):

| touched | reader | verdict |
|---|---|---|
| stages.json (Grep `stages\.json` over `scripts/*.py`: 237 hits / 73 files; over `tools/`: 0, control `def main` in `tools/hygiene_gate.py` 1) | every package reader reads named keys; no stage-key allow-list found (Grep `"acceptance_by",\|STAGE_ROW_KEYS` 0; sampled `stage_joints.py:179-188`, `contract_slices.py:519-548`, `test_stages.py`) | unchanged; `reviewed_by` read only by `reviewed_dispatch` (this stream) |
| stages.json | `role_load._form_candidates` (roles per stage) | unchanged (roles untouched) |
| `reviewed_dispatch`/`_id`/`_lines` | `brief_pack.py:3733, 3745, 4536`; `story_step.py:335` | changes in this stream |
| same | `tests/dry_stub.py:331-338` (regex on the line) | unchanged code; now also fires for S5 critics (E14) |
| same | `test_handoff_init_author.py` (6), `test_stage_done.py` (10) - quarantine | S2/S4/S7 rows unchanged; f18 flips (F4) |
| `advice_of` | `brief_pack.py:4577`; `test_window_artifacts.py:404-429` (quarantine) | output byte-identical (item 2(a), N4) |
| `_author_argv` | `story_step.py:370`; `test_handoff_init_author.py:63-89, 216-250` (4-argument calls) | changes in this stream; old calls stay valid (optional parameter) |
| S5 critic forms | `handoff_init.fill_head` / `drop_unowed_acceptance` | unchanged code (token road; f8) |
| same | `handoff_check._version_of` / `DERIVERS` | unchanged; derives the new row's version |
| same | `role_load._static_form_layer` (A22) | measured, equal (E11) |
| same | `contract_slices.py` -> `slices/qa-code-critic/handoff-keys.md` | regenerated in this stream (item 6) |
| same | `tests/form_filler.py` (token -> ctx `author_dispatch`), `test_field_producers.py` rounds | unchanged code; N2 |
| same | `references/null-outcomes.json` NE45/NE46 (`inputs_read` never empty) | unchanged; still holds |
| same | `fixtures/form-rounds.json` 3 S5 rows (`probes.*`, `review.receipt_ref`) | unchanged (none on `inputs_read`) |
| same | `test_handoff.py` (13), `test_handoff_inline_values.py` (5), `test_repair_route.py` (4), `test_charters_s5_s9.py` (3), `test_rows_owed.py` (2), others with 1 (Grep count over the package) | canon judges; report line |
| same | frozen story fixtures `fixtures/stories/*/work/handoffs/S5-qa-code-critic-*.yaml` | filled forms, not templates: unchanged |
| `handoff.py:406` comment | none (a comment) | - |
| slice file | role injection of qa-code-critic | inside N3's measure |

KNOWN MISS to settle with the block: whether any `tools/` gate pins `brief_pack.py` function signatures (the hand grep covered
`stages.json` only).

## §5 Forks (the Lead's)

- F1 (Q3) the prefill road. (a) token in both S5 forms, bytes netted in `s5-critic-to-automator.yaml` - RECOMMENDED: one road
  (P31, axis 34), no code in `handoff_init.py` (no FV3-32 wait), dry and live forms equal. (b) a token-less `fill_head` rule -
  a second road (rule 6 defect unless the owner's word), an AR-1 list or new contract key, FV3-32 sequencing, contract-neutrality
  lost (§2.3). Under (b) the card changes: owns + `handoff_init.py`, the forms leave owns, item 4 becomes a `fill_head` rule and
  `_author_argv` needs its own gate.
- F2 the S5 author pick. (a) the part- and scope-matched walk extracted from `advice_of`, bound to the critic's record -
  RECOMMENDED: S5 has parallel windows and a plan (f10), so "last accepted automator" (f11) names a sibling's dispatch; the walk is
  the fact's existing reader (AR-13). (b) `stage_author_dispatch` as on S4 - simpler (no `dispatch` argument, no `story_step.py`
  change), but it can prefill and instruct "must be" with a wrong dispatch under parallel windows or a plan/window interleave
  (FR-59). Is (a) a second road beside S4? No: S4's fact is "the dispatch the S4 gate binds" (its reader must stay the gate's);
  S5 has no gate and its fact is "the automator dispatch of this critic's window/plan" - two facts, one reader each.
- F3 the wording at S5. (a) the one wording `stage_done.reviewed_row_rule` ("must be ..."), no gate behind it on S5 - RECOMMENDED
  (one text, AR-22 "the ONE wording"); (b) a softer S5 sentence - a second wording to keep in step. Low weight.
- F4 the quarantine pin f18 turns red by the decided change. (a) a report line; the quarantine watcher's judge reads it as
  intended - RECOMMENDED (TESTING.md: a builder never runs, fixes or edits a quarantine file). (b) the Lead removes the row with
  `tools/test_quarantine.py` in the same wave. The SessionStart alert may show it; the Lead tells the owner if it does (rule 11).

## §6 Small choices closed by the designer

- Key name `reviewed_by` (§2.1 reason); placed after `roles`; no edit of the `stages.json` `note` (no stage key is documented there).
- Invalid key -> one stderr line (precedent `acceptance_reads`), not silence.
- The helper returns `met_self` so `advice_of` stays byte-identical while the reviewed path is strict.
- `version: <hash>` for the author row (deriver-measured, f9), not S4's prose placeholder.
- `inputs[0].path` also moves to the token (AR-15; -3 bytes help E11).
- `handoff.py:406` comment updated (the token's list of users).
- No `agents/qa-code-critic.md` edit: `AUTHOR_NOTE` in the filled copy tells the critic; the charter is inside A22.
- If `tools/dispatch_manifest.py` reads N1/N2 as whole runs of canon-class files, the dispatch carries
  `manifest-skip: dod-run -- N1/N2 import one function of a canon-class file, not the file`.

## §7 Reading trail

Read: the report (whole); t-1257 review (Grep F3 lines 3-91); `stages.json:1-20, 130-259`; `brief_pack.py:96-125, 1141-1143,
2622-2666, 3620-3645, 3660-3784, 4520-4539`; `story_step.py:300-388`; `handoff_init.py:100-209, 228-287, 470-529`; both S5 forms
(Grep + `1-30`, `22-43`); `handoff.py:406, 462-470, 551-562, 607-609, 674-677`; `acceptance.py:1433-1512`; `controller.py:5596-5625,
6694-6733, 6990-7079`; `hooklib.py:831-838`; `role_load.py:140-142, 255-290, 483-513`; `role-load.json:1-40`; `null-outcomes.json:165-176`;
`index.yaml:51-57, 70-95`; `test_handoff_init_author.py:1-92`; `test_handoff_init.py:1-78`; `test_field_producers.py:1370-1440, 1555-1594`;
`test_brief_pack.py:2400-2439`; `dry_stub.py:325-358`; `test-layers.json:1-40, 294-301, 858-867, 1694-1701, 2331-2338, 7185-7196,
8490-8501, 10728-10735`; `slow_tests.json:1-12` + Grep; `design/architecture.md:33-95, 173-335`; `tools/architecture_gate.py` (Grep
`judgment:`); `docs/TESTING.md:60-159`; `SIBLING_MAP.md:590`. Greps with counts are cited at their facts and in §4.
Contradiction noticed in the brief: none beyond Q1 (already corrected by the Lead). Analog noticed: `brief_pack.py:108-112` calls
"a form with no row here and no `acceptance_by`" a residual for `tried` readers - a different fact (the `tried` table), left alone.

## Lead decisions (Lead, 18.11.2026, Opus; «решила сама»)

F1 = (a) the AUTHOR_TOKEN in both S5 critic forms, bytes netted inside `s5-critic-to-automator.yaml` (one road, axis 34; no
`handoff_init.py` edit, so no wait on FV3-32). F2 = (a) the part- and scope-matched walk extracted from `advice_of`, bound to the
critic's own record (parallel windows defeat "last accepted automator"). F3 = (a) the one wording `stage_done.reviewed_row_rule`.
F4 = (a) a report line; the quarantine watcher judges the pin. Added to the DoD: one CI dry run (`ci_read.py start --ref <branch>
--var dry_only=true`) whose red set is a subset of main's latest (E14: the dry S5 critic token now fills from the brief line).
critic on this plan: skipped -- every fork follows the designer's recommendation, no existing field changes meaning; the code
gets the topic critic.
