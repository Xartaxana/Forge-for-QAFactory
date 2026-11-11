# t-1957 — one fast manual walker for the three by-hand places (S6 cases, S7 control experiments, exploratory walk) — SPEC (designer, revised)

Status: **critic-on-plan t-1960: fit_with_fixes; fixes 1–16 applied** (verdict `docs/tasks/specs/reviews/t-1960-critic-plan-fast-manual-walker.md`).
Revised in place by the designer on 05.11.2026 per the Lead's decisions and two later owner's words (below). Package under change: worktree
`D:/ws1/wt-fbfix` (below `PKG\` = `D:/ws1/wt-fbfix\ai-packages\qa-factory`). Every file:line in §2 was read in that worktree (or the
named carrier) on 05.11.2026; a number with no file:line is marked **estimate**. The work is cut into three SLICES (§4); each lands and is proved
live on its own.
Revised again in place by the designer on 05.11.2026 (evening) for the batch decision and the owner's word on it below: §1 (AR-1 row, census
rows), §2 F44–F45, §3.2, §3.10, N1a, N2, N4, §6 (forks F11–F13 with recommendations; the nodes are executable by them until the Lead answers), §7,
§8, a one-line note at Slices 2 and 3.

Fixes of t-1960 (its JSON `fixes` list, in order) -> where applied:
1. After-step inside `run_role` between the role's return and `bind` -> §3.5, N5s (owns the `run_role` hook; E5s.1 POSITIONAL).
2. End probe copied into every item attempt at close; `requests_seen` flushed per item; `call_surprises` reset per call -> §3.2, N1a (E1.10, E1.13, E1.14).
3. A factory-owned sign-in failure (`login_unknown`, or not proven at gate A) opens the session UNSIGNED with the `fill-account` door; only owner `user` is dead -> §3.2, N1a E1.5.
4. `look`/`final` obey `SessionAccount.window`/`NO_SHOT_IN_WINDOW` -> N1a E1.11; lock on `CreatedAccounts.add` and the email template of `fill-new-account` -> N1c.
5. N1 split into N1a/N1b/N1c; the lease shape names all readers; the server releases its own lease; `_same_process` for the parent; a fresh profile dir per open; Job object / `killpg` -> N1a (E1.2, E1.7, E1.8), N1b.
6. `ActorSession(folder=)` reused for the walk profile -> §3.2, N1a.
7. The accounts/data question holds no case (F10); extra lanes run in turn on recorded accounts -> §3.6, N8 (E8.0), §6.
8. N7: a new optional field `home` on `request_homes`, the S3 brief line and the strategist charter; where a ROW's requests are walked -> N7. Its «old plans keep today's cells» part: **not supported by decision of the owner — a story is not carried across package versions** (owner's word 1 below).
9. N8: the correct `resolve` CLI; same-role lists as `env:` handles in a mapped list; `report_facts.created_accounts_line` reused; `authorized_actions` is prose (the conductor's resolved mapping is the authorization); question key in `question-prices.json` + a `closed_question` site; a mapped "only one account" field -> §2 F26–F28, §3.6, N8.
10. Kinds compared after casefold+strip, an unpaired kind runs alone; a `claim` step for `obtain-data` instances -> §3.7, N8 (E8.1, E8.14).
11. The census file has an owner per slice; `verdict_problems` is class `xref`; the blocking count and its ONE named raise -> §1 census table, N1a, N2.
12. §7: per-item time = dispatch wall; last cumulative cost per session; cost by item index; conductor spend reported; Sonnet 5.5 -> §3.10, N2 (`walk_timing.py`), §7.
13. F5: the owner's default 3 as a project config key; a `note:` line when t-1937 P1 is absent -> N5p, §6.
14. The axis-5 twins `phases/s6.md`, `story_step._manual_block_door`, `story_progress.py:403` -> owned by N5s.
15. Resume edge: the driver reopens a walk session before resuming a running walk dispatch (within one run) -> N1a E1.16, N5s E5s.6.
16. First slice = N1a+N2+N3+N4+N5s+form by code + the per-call experiment; N8 and N7 split off -> §4 (Slices 1–3).
Also applied: §2 facts W1–W10 of the verdict corrected (§2 F2, F12, F25–F28, F35–F41); every «could not establish» of the draft replaced by the
established fact; what is still open is listed in the reading trail.

Decided by the Lead, 05.11.2026 (not re-opened here): fixes 1–16 accepted; the slice cut; F1 = our kept-session recorder (a); F2 = up to 3 items
per dispatch in Slice 1, re-decided by the live measurement (cost by item index); F3 = (a); F4 = (a); F6 = (a); F7 = (a); F10 = the
accounts/data question holds no case.

**Decided by the Lead, 05.11.2026: step batches with stop at the first deviation (owner's question about scripts)** — the owner asked «Шаги после
тест-плана будут и у мануального агента. А как быть со скриптами?»; the walker takes the speed of a script without a script: (1) the role MAY hand
the recorder all the steps of an item in ONE call, as data in the recorder's step vocabulary, never code; (2) the session recorder runs them in
order on the live page and writes its evidence per step as designed; (3) at the FIRST deviation (a closed, data-defined list: FR-13, AR-1) it
STOPS the batch and returns to the role which step, what happened and a text snapshot of the page, the session staying open; the recorder never
judges whether the deviation is a bug (AR-29); (4) a smooth S6 case costs one or two recorder calls, an item where the page does not behave as
planned costs more, and that is where the role's judgment is wanted (P26). Applied in §3.2, §3.10, N1a, N2, N4, §7.

**Owner's word on the batches (05.11.2026 ≈21:20):** «шаги заранее известны только в одном месте из трёх, где нужен ходок. На стадии анализа не
уверена, что можно сделать пакетные шаги». Hence: **the batch is an OPTION of the step call, never an obligation** — the recorder accepts 1..N
steps in a call, and a single step is a batch of one (the same call). Where the steps are known in advance — the S6 manual case, whose steps come
from the case — the charter's experience is «plan the item's steps as one batch». In the other two places — the analyst's control experiments
at S7 and the exploratory walk — the role does not know the next step before it sees the page: there the normal mode is ONE step (or a short
run of two or three obvious ones) per call, look, decide. The expected numbers are given PER PLACE (§3.10): the «one or two recorder calls per
item» claim holds only for S6 manual cases with known steps; the plain-agent comparison of §7 is valid for that S6-like load only.

Decided by the owner, 05.11.2026:
- F5 = 3 walkers by default («пусть будет 3», 18:55, `experiments/mybooks/thinking-roles/thinking-roles.md:150`) — a project config key, default 3.
- The 24-place check runs on **Sonnet 5.5** («это должен быть соннет 5,5», 18:48, `:149`).
- The factory never stands still over accounts («Фабрика не должна вставать», Lead brief).
- **No compatibility with older package versions** («Какие старые планы? Старые варианты фабрики. Их можно не учитывать, так как одну стори 2 раза
  прогонять не будут и на разных версиях тоже»): stories, plans and evidence written by an older package version are not read, migrated or kept
  working; a story runs once, on one version (P24). TEMPORAL edges in this spec cover only what the change creates WITHIN one run on the new
  version (a file absent before a step and present after; a walker that died mid-walk; a config key not yet answered).
- **MyBooks allows self sign-up** («На этом проекте можно самим создавать учётки») — a PROJECT FACT of the live-proof stand, recorded in §7
  (Slice 2) through the designed registry route as the first real answer; the general design is unchanged (asked once per project, open answer).
- **Batches are an option, known steps only at S6** (≈21:20, the paragraph above).

Open for the owner: only F8 and F9(b) (§5). Found while revising, for the Lead: L1, L2 at the end of §4; F11, F12, F13 in §6.

Owner's words that set the goal (05.11.2026, `thinking-roles.md:135, :141-147`): «ручное тестирование было быстрым и дешёвым как у той фабрики (с
нашим сбором улик)»; «3 места. Надо взять технику у той фабрики»; parallel walkers each with its own browser; overlapping cases separated by DATA
(«засидить разные книги…»), «run alone» only the fallback; how a project gets more accounts/data is a PROJECT FACT in open variety («Сначала спросить
пользователя… и запомнить»; «почему закрытым списком?»).

---

## §1 Goal, AR-n and FR touched, owners of every check

Goal: a manual item (an S6 case, an S7 control experiment, an exploration cell group) is walked live with full recorder evidence (P26), several
items per dispatch, several walkers in parallel where the project's accounts and data allow, and the role does no plumbing; an S6 case in ≤ 7 min
and ≤ $0.50 (the other two places have their own, higher estimates, §3.10). Slice 1 proves the speed claim with one walker on S6 cases; Slice 2
adds parallel walkers and the accounts/data way; Slice 3 moves S7 controls and exploration onto the walker. Where the steps are known in advance
(an S6 case) the walker gets a script's speed without a script: the item's steps go to the recorder as ONE batch of data and the recorder stops at
the first deviation (§3.2); where they are not (S7 controls, exploration) the same call carries one step or a short obvious run.

| AR | how touched | change check in the DoD of node |
|---|---|---|
| AR-1 closed variety is a data row | what counts as a deviation that stops a batch (step outcomes, surprise kinds, the status range) and the batch limits live in `manual-capture-steps.json` (`walk_session` object); the role's `--stop-on` names kinds from that list | N1a: `test_stop_rules_from_data`, `test_stop_on_unknown_kind_refused_names_kinds` |
| AR-2 open variety is a role's judgment | the project's way of getting accounts/data is the person's words; the walker follows them; code acts only on fields the conductor mapped; how many steps go in one call is the role's choice | N8: no phrase list over the words; `test_never_refuses_unmapped_way`; N1a: `test_single_step_call_is_a_batch_of_one` |
| AR-7 / AR-29 code = instrument, role = judgment | the server carries steps and writes evidence; the role decides every step, every batch and every Then; a stop says what happened, never that it is a bug | N1a, N2: no function reads a Then's words to decide; census rows below |
| AR-8 a role is handed paths/commands | app card + walk brief hand routes, accounts, commands; "read app sources" goes | N3 key-presence test |
| AR-10 a check's requirement reaches the role first | "evidence before pass" (`final`) and the step-call modes in the walk charter and `verdict --help`; `home`/`walk_data` in the S3 brief + strategist charter | N2, N4, N7, N8 |
| AR-11 only the tools/context the work needs | `manual-evidence.md` (11 995 B) leaves the runner's injection; the walk brief has no manifest/repo map | N4: `role-load.json` qa-runner rows go DOWN |
| AR-12 friction measured | per-item wall, cost by item index, tool calls and recorder calls per item, per place (`walk_timing.py`) | N2, §7 |
| AR-13 / AR-15 one reader, one survivor | `walk_session` imports `manual_capture` (`PlaywrightBackend`, `Attempt`, `_run_steps`, `parse_steps`, `stand_probe`, `sign_in`, `await_landing`, `ActorSession`, `SessionAccount`, `_store_requests_seen`); every step call, of one step or many, runs through the SAME `_run_steps` as a `ui` call (one keyword added); lanes cut by ONE function `controller.walk_lanes` read by driver, door and progress; leftover accounts line = `report_facts.created_accounts_line`; liveness = `execution_scheduler._same_process`; the person's words through `person_words` | N1a, N5s, N8 |
| AR-14 one artifact, one writer | `state/walks/<W>.json` and `state/walks/<W>/batches/` (server), `work/walks/<W>/<item>.json` (server `verdict`), case record (`build_record`/`write_unprepared` -> `write_block`), the form through `<dispatch>.values.yaml` + `handoff_check.py` (existing path), registry rows (`project_decisions`) | N1a, N2, N5s, N8 |
| AR-3 config default for every key | `manual.walkers` (3), `manual.accounts_way`, `manual.data_way` (every field `"not known"` by default) — Slice 2 | N5p, N8 |
| AR-19 stage twins change together | driver lanes, `story_step._manual_block_door`, `story_progress._block_position`, `phases/s6.md` cut by the same lanes | N5s |
| AR-20 shrink-only ratchets | `role-load.json` qa-runner rows down; `judgment-census.json` `blocking_per_role.conductor` +1 — the ONE raise, named for the Lead's verdict (the batch adds none) | N1a, N4 |
| AR-21 / AR-22 producer and reader together | walk record -> case record -> `run-report.json`; walk record -> form values; walk record -> triage `control` (Slice 3); registry -> config -> `walk_pool` -> brief (Slice 2); the `status` number of a `surprise` line (producer `manual_capture`, reader `walk_session.stop_at`) | N1a, N2, N5s, N6, N8 |
| AR-23 every list declares its empty outcome | no observation, no verdict, no timing line, an empty step call (refused), no `not_run` step, ways `"not known"`, no `explore` home | N1a, N2, N7, N8 |
| AR-25 every state a way out | session `opening/ready/closed/dead`; a step call `running/done/stopped` (a stopped call leaves the session `ready`); entity `free/in_use/dirty`; question row `open/resolved` | N1a, N8 |
| AR-26 requirements are the unit | the walk verdict is per Then of the case | N2 |
| AR-27 a finding reaches the report under its owner | created accounts left on the stand: the existing `created_accounts_line`, owner `factory` | N8 |
| AR-28 unknown never a pass | a dead walker's items `inconclusive`; an unknown account way never means "create"; a `status` line whose number cannot be read stops the call (never read as "below 500") | N1a, N2, N8 |
| AR-9 refusal names a door | every refusal of the server names its door (a step call while one runs: wait / `status`) | N1a |
| AR-16 one question form | the accounts/data questions are `closed_question` keys priced in `question-prices.json` | N8 |
| AR-17 a state code has no move for goes to the conductor | a walker's `needs` record -> the conductor seam | N8 |

FR touched: FR-1, FR-2, FR-6, FR-7 (asked once), FR-8 (words whole), FR-11, FR-12 (no phrase list over the answer), FR-13, FR-14, FR-15, FR-18,
FR-23, FR-33 (§7), FR-38, FR-41, FR-47, FR-48, FR-50, FR-51, FR-53, FR-55, FR-56, FR-57, FR-58, FR-59. Principles: P2, P5 (D-0043), P8, P9, P11,
P14, P19, P22, P24, P26, P27, P28.

**Checks added or altered: owner served and census class** (AR-29; host adaptation 10). Class words are the closed list
`shape, xref, word-list, meaning-proxy, meaning, safety` (`PKG\scripts\tests\test_judgment_census.py:74`); ONE class per function, the higher wins
(`CLASS_ORDER` :60). A unit COUNTS toward `blocking_per_role` only when a refusal site (`raise ValueError|StateConflict`, `deny`/`block`;
`refusal_registry.py:57-58`) sits in it or its file is on the blocking path (`units_of` :256-261); the ratchet is DENSE — a count below its
ceiling is red too (`compare` :365-373). Labels follow the convention of the recorder files: `manual_capture.py`/`manual_evidence.py` rows are
`roles: ["conductor"]` (census `:489-543`).

| check (file :: function) | slice/node | added/altered | owner served | class | blocks? | why not a judgment |
|---|---|---|---|---|---|---|
| `walk_session.py :: request_problems` (token, walk state, item in the walk's scope, step file parse via `manual_capture.parse_steps`, actor held by a live session, `look`/`final` inside the sign-in window; for a step call: at least one step, at most `max_batch_steps`, every `--stop-on` token a kind of `surprise.kinds` or `status:<lo>-<hi>`, no step call already running in this walk) | 1 / N1a | added | data | xref | no (returns a list) | keys, membership, counts, a join to the live-session registry and the server's own busy flag |
| `walk_session.py :: _refuse` (the ONE `raise ValueError` of the server; turns a problem list into exit 2 + door) | 1 / N1a | added | data | shape | **yes** | formats and raises what the `*_problems` functions return |
| `walk_session.py :: stop_at` (after each step of a call: the step's outcome is not `ok`, or a `surprise` line of this step matches a rule the role sent / the data default, or the role's own `expect=` reads otherwise (F12), or the call's time budget is spent -> the stop reason) | 1 / N1a | added | data (the role chose the rules; the role judges what the stop means) | shape | no (returns a reason or none; nothing refused, the session stays `ready`) | kind membership and a number range over facts the detector recorded; never says whether the fact is a defect. Its name matches no `UNIT_NAME_RE` pattern (`test_judgment_census.py:58`) and it holds no refusal site, so it is no census unit; the row is here for the reader |
| `walk_session.py :: verdict_problems` (each Then has `result`; pass/fail has a `quote` found in a capture of THIS item's attempt via `manual_evidence._quote_in`; a `pass` has a `final` capture after the last action; teardown present when named) | 1 / N2 | added | data (the verdict stays the role's, accepted at S7 by the analyst) | xref | no | presence of quoted bytes, order of stored captures |
| `walk_session.py :: claim_problems` (an `obtain-data` instance is not `in_use` by another running walk) | 2 / N8 | added | data | xref | no | set membership |
| `planning_contract.py :: _walk_data_problems` (S3 exit: `walk_data` well formed when present) | 2 / N8 | added | data | shape | decided by the census run (blocks only if `planning_contract.py` is a non-advice `stages.json` detector) | form only; ABSENT is legal |
| `planning_contract.py :: _request_findings` (accepts `home: "explore"`) | 3 / N7 | altered | data | unchanged | unchanged | a field value from a closed set |
| `controller.py` op `dispatch` admission, S6 clause (disjoint scope, distinct `walk_actor`, count ≤ walkers) | 2 / N5p | altered (extends t-1937 N-P1-1) | data | unchanged (inside op `dispatch`) | unchanged | set disjointness |

**Ratchet verdict (AR-20), for the Lead:** Slice 1 adds exactly ONE blocking unit, `walk_session.py::_refuse`, labelled `["conductor"]` ->
`blocking_per_role.conductor` = (its value on `main` after t-1955 lands) **+ 1**; qa-runner's row is unchanged (131 today, census `:4`). No offset
exists honestly: the runner's `manual_capture`/`manual_evidence` road stays as the fallback door (E5s.4), so none of its units leave. The batch
rule adds no unit: its refusals go through `request_problems` -> `_refuse`; `stop_at` and the `stop=` keyword of `manual_capture._run_steps` hold no
refusal site. Slices 2 and 3 add no blocking unit except, possibly, `_walk_data_problems` (N8 names the census run's answer and, if it counts,
`blocking_per_role.qa-test-strategist` + 1 as a second named raise). Driver functions (`walk_before`, `walk_after`), `controller.walk_lanes`,
`app_card.py`, `walk_timing.py`, `walk_pool.py` hold no refusal site and no unit-pattern name (`UNIT_NAME_RE` :58) — a builder who needs a refusal
there routes it through `_refuse` or reports the raise.

---

## §2 Measured facts (file:line; anything else marked estimate)

### Cost and time (carrier: `docs/tasks/specs/reports/t-1954-scout-manual-lane-cost.md`)
- F1. No manual case was walked in either arm; TC_014 cost $0.572 and 792.7 s of runner sessions for 0 browser steps (t-1954 :12-15, :45).
  Split (t-1954 :88-100): reading 62 s, `manifest_view.py` 74 s, `env_probe.py` 88 s, reading MyBooks sources 77 s, recorder/register 130 s,
  `finalize_task.py` 88 s, `manual_evidence.py` 35 s, forms 117 s, model pauses 62 s. Hooks 117.9 s, of them `cost_capture.py` at `Stop` 60.5 s
  (t-1954 :106; `PKG\hooks\hooks.json:119-140`). `total_cost_usd` is cumulative over resumes of one session (t-1954 :37).
- F2. Recorder speed when it walked (CART-1 archive, 31.10, an OLDER package): 37 steps in 24 s ≈ 0.65 s/step (t-1954 :123-126). The per-CALL
  overhead of TODAY's recorder (python start, harness re-exec `manual_capture.py:2244-2255`, chromium start, two `stand_probe`s, lease, profile
  resume) is measured NOWHERE — pre-step P0 of Slice 1 measures it (critic W10).
- F3. Other factory: ~6.6 min/case incl. the lead's overhead, $0.32–0.72, mean $0.44/case, a FRESH subagent per case
  (`experiments/mybooks/thinking-roles/other-factory-survey.md:67-68, :75`).
- F4. S6/S7 of arm B: S6 0:18:20, S7 0:10:28 (`experiments/mybooks/thinking-roles/time-analysis.md:145-146`); S7 investigation $0.241, 0 probes
  (t-1954 :66).
- F42. **Cost per item grows with its index in a shared session** (critic t-1960 §3): every turn re-reads the whole context; at ~150K context a
  Sonnet turn ≈ $0.05 of cache read, × 15 turns ≈ $0.7 for item 5 — **estimate**. Hence F2 = 3 and the cost-by-index measurement (§7).
- F45. **The plain agent on the same 24 places** (`experiments/mybooks/disputed-check-plain-agent/SUMMARY.md:41-52`): three Sonnet 5.5 agents in
  parallel, no factory, no recorder, ONE script per card run whole; dispatch time 849 + 1162 + 1264 = 3 275 s -> **136 s per card**; 90 tool calls
  -> **3.75 per card**; host counter `subagent_tokens` 496 636 -> **≈ 20.7K tokens per card**; wall of the set ≈ 21 min; the cards' own
  `seconds` (741 s in sum, ≈ 31 s per card) are script run time, not agent time (:49); dollars NOT available (the host gives one token sum, no
  input/output/cache split, :50); no per-card cost (:51). Its weaknesses (the Lead's brief, SUMMARY.md :37): it does not look at the page between
  steps, and its evidence is written by its own code. Its outcome: 8 bugs, 1 product gap, 9 places for the product owner, 4 not bugs, card 24
  three of four scenarios as expected (:35); card 20 withdrawn by the owner as "not a case" (:70). The load was S6-like: each card's steps were
  written in advance («Руками», `add-to-cart-disputed-places.md`), so these numbers compare only with S6 manual cases (owner's word 21:20).

### Place (1) — S6 manual cases
- F5. `PKG\scripts\controller.py:491` `MANUAL_BLOCK_CASES = 5` (ceiling), `:495` `MANUAL_WINDOW_CASES = 1`; `manual_blocks` `:575`; driver
  `PKG\scripts\story_run.py:11794` `MANUAL_BLOCK_MAX = MANUAL_WINDOW_CASES`, `manual_plan` `:11820-11837`, `run_manual_block` `:12173-12249`
  ("ONE block per entry"; deferred questions hold their cases `:12183-12188`, RN1-24). Pinned by `test_manual_window.py:30` `(1, 5)` (fast) and
  `test_story_progress.py:881-882` (SLOW: `slow_tests.json:145`). Twins that cut by COUNT: `story_step._manual_block_door` (`story_step.py:1019-1045`,
  `manual_blocks(cleaned, MANUAL_WINDOW_CASES)` :1037), `story_progress._block_position` (`story_progress.py:386-405`, `math.ceil(len(left) /
  controller.MANUAL_WINDOW_CASES)` :403), `PKG\skills\qa-story\phases\s6.md:6-7, :46` ("a manual window is one case").
- F6. The prompt tells the runner to run `finalize_task.py` itself (`story_run.py:12239-12240`); t-1955 N3 rewrites the unprepared prompt line
  `:12243-12246`. Brief "Read these files" -> `manifest_view.py`; Commands card lists `env_probe.py`, `manual_evidence.py prepare|validate|write-block`,
  `finalize_task.py`, `manifest_view.py` (arm B brief `...\S6-qa-runner-3.md:95-97, :116-123` — stand file, read by the draft's designer; not
  re-read by the critic). Charter Tools: `PKG\agents\qa-runner.md:59-61`.
- F7. The case's Thens are in its prepared request (arm B `work\evidence\manual\LOCAL-1_TC_014\request.json:17-21`).
- F8. Recorder: one browser per `ui` call (`manual_capture.py:1355-1363`); a call holds the stand lease and probes the stand at start and end
  (`_session_cycle` :2945-2956, `_session_cycle_held` :2958-2985: start probe :2961, `_store_requests_seen` once before the browser closes :2967,
  end probe :2978); lease `_hold_stand` :3846. `--session <actor>` keeps cookies in `<attempt>/sessions/<slug>/profile` (`ActorSession` :2486-2494,
  which takes `folder=` :2491). `attempt.call_surprises` accumulates per `Attempt` (:1070) and `_run_steps` writes it as one file per call
  (:3150-3175). Character typing: `explore-charter.md:74-81`. A seam `BACKEND_FACTORY` exists (`_new_backend` :2709-2712).
- F44. **What the recorder already does with a list of steps** (read 05.11.2026 in wt-fbfix): a `ui` call already takes a steps FILE, one step per
  line, tokens split as a shell would (`manual-capture-steps.json:4`); `_run_steps` runs them in order and ALREADY stops at the first step whose
  outcome is not `ok` (`manual_capture.py:3225-3227`); step outcomes are `ok|failed|timeout|refused` (:34); an element lookup waits up to
  `ELEMENT_WAIT_S` = 30 s (:105) and a step up to its stand's limit (`DEFAULT_TIMEOUT_S` 180 s when never measured, :103, `timeout_for` :531);
  the first `OBSERVE_MAX_STEPS` = 40 steps of a call are observed with a screenshot and an excerpt (:113, :3209-3213). The surprise detector
  (`_surprises_after` :3671-3694) "refuses, stops or judges nothing" (:3676); its kinds are the data list `request, status, failed, console, url,
  field, text, blocked_host` (`manual-capture-steps.json:64`); a `status` line is written for ANY answer ≥ 400 that is not the role's own
  `fail_request` (`_candidates` :3584-3586; the role's own failures are marked `ours` BEFORE they answer, :1828), so 4xx and 5xx share one kind
  and the number lives only inside the `fact` text (`Attempt.surprise` :1104-1111 stores `step, word, kind, fact`); `url` is written only when a
  `goto` lands elsewhere or the address changes on a step that does not act (:3609-3612), so it already means "a navigation the step did not
  ask for"; `field` is "a value the application changed or a lost focus" while typing (:3613-3617, `_field_fact` :3641-3657); console errors and
  page errors are kind `console` (:3590-3594). The step vocabulary has `read` (`manual-capture-steps.json:21`) but NO word that compares a read
  with an expected value (the `steps` object :7-23; a Read of the whole file).

### Place (1) — S6 manual cases (continued)
- F9. Lease exclusive when `run.parallel` is false (`run_suite.py:1354-1361`, `hold_stand` :1365-1395); MyBooks `"parallel": false` (arm B
  `qa-factory\config.json:532`). `run.parallel: false` is onboarding's "localhost has one account" (`run_suite.py:1356`, critic §5).
- F10. A record binds to the ONE running S6 dispatch holding the case (`manual_evidence._running_dispatch` :1367-1379): no running dispatch ->
  `ValueError` :1372-1375.
- F11. Account creation: `generated_account` (`manual_capture.py:710`), store of NAMES `created_names_path` :718, `CreatedAccounts` :724 with
  `add` :754-761 (read-modify-write, no lock), `resolve_actor` :769 (forms `env:U/S`, `created:<name>`); `_CREATE_ROUTE` :693 tells the role to
  find a create-user endpoint. Arm B `credentials_by_role`: `admin`, `user` (config `:307-310`), "tests may register their own users" (:309).
- F12. Controller refuses a second running dispatch: `controller.py:4928-4941`. t-1937 is a DRAFT read against `exp-thinking-roles\pkg-b`
  (c75ec3789), not wt-fbfix (`t-1937-s5-parallel-windows.md:3, :5`). Its REAL names: admission inside op `dispatch` (no function of its own,
  `:186-189`, node N-P1-1 `:287`); the chain runner `S5Scheduler` in `stage_S5`, one driver lock `self._book` (RLock), `launch` releasing it around
  `communicate` (`:175-178`, node N-P1-4 `:290`); config key `dispatch.parallel_windows` (N-P1-3, `:179-181, :289`); launch rule (iii) "no
  question is pending" (`:184`). **Not landed in wt-fbfix:** a Grep for `S5Scheduler|s5_parallel|parallel_windows` over `PKG` found nothing;
  the same tool and path found `MANUAL_WINDOW_CASES` (positive control).
- F13. `run_role` (`story_run.py:2787-2893`): start/rework -> `run_claude` (:2851) -> saved result (:2853; a saved result is REUSED on a rerun,
  :2854-2855) -> `bind` (:2856-2860) -> halt check / `handoff` (:2869-2880) -> `question_threshold` (:2887) -> `repair_limit_gate` (:2890) ->
  `finish` (:2891, def :2895). `resume_role` :3141. **POSITION**: anything that must bind to the running dispatch must run before `finish`.
- F25. Stand flags: `safe_to_break: true` (arm B config `:311`); `authorized_actions` is FREE PROSE ("everything needed to test the product…",
  `:312`), not a list (critic W8).
- F29. `_attempt_files` (`manual_evidence.py:1527-1555`) refuses an attempt: holding a live `sessions/*/profile` (:1532-1536); with no captures
  (:1538-1539); with two stand profiles (:1541-1549); with no probe at its start OR its end (:1550-1554).
- F30. The role's Stop gate: `exit_gate.required_outputs_errors` (`exit_gate.py:803-838`) refuses the stop while the S6 `required_outputs`
  `work/run-report.json` (`references/stages.json:209-211`) is not on disk (:831). The handover form is NOT checked at the stop
  (`exit_gate.py:941-943`): `story_step finish` checks it, and `handoff_check.form_view` reads "the form plus its waiting values file"
  (`exit_gate.py:792`). The form `work/handoffs/<dispatch>.yaml` (`story_step.py:298`) is "created by code, filled by the role (… or through
  <dispatch>.values.yaml, which handoff_check.py applies)" (`references/artifact-writers.json:219-226`).
- F31. In S6 the automated half runs first; the manual half enters on the next loop (`story_run.py:11468-11485`); a story with NO automated scope
  reaches `run_manual_block` before any `run-report.json` is written.
- F32. The brief of a manual dispatch is assembled by `brief_pack.build` (:3203); the manual branch adds `exploration_lines` (:3318-3319).
  `brief_pack.walk_lines` (:2912) EXISTS and is the S3 "Functions to walk" line — a new function must not reuse that name.
- F33. Census (above): refusal sites count; recorder rows are labelled `conductor`; `blocking_per_role` qa-runner 131, conductor 466
  (`judgment-census.json:4`); live `role_load.py --role qa-runner` = 17 886 tokens, ceiling 17 887 (critic rerun).
- F34. Slow test files (CI only): `test_brief_pack*.py` (`slow_tests.json:16-18`), `test_role_commands.py` (:116), `test_story_progress.py` (:145),
  `test_story_step_manual_block.py` (:174), `test_project_decisions_*` (:97-98), `test_report_facts.py` (:111). Fast (a Grep of `slow_tests.json`
  for their names found none, the same Grep found the slow names above): `test_manual_window.py`, `test_manual_evidence.py`,
  `test_manual_capture_session.py`, `test_manual_requests_seen.py`, `test_stand_lease.py`, `test_judgment_census.py`, `test_role_load.py`,
  `test_charter_form.py`, `test_artifact_writers.py`, `test_config_migration.py`, `test_manual_actor.py`, `test_triage_control.py`,
  `test_flow_requests.py`, `test_exploration_perturbations.py`.

### The project decision registry (Slice 2)
- F26. `PKG\scripts\project_decisions.py`: rows matched by `field_refs` only (`:1-6`); `upsert` (:377) returns the OPEN row for the same refs;
  `resolve` (:427) writes ONLY `field_values[pointer]` and refuses when a pointer has no value (:441-443 "resolution must provide exact values for
  field_refs"); CLI `resolve --id <DD-n> --resolution-ref <ref> [--decision <words> | --words-file <f>] [--field-values '<json>']` (:866-876),
  `--id` and `--resolution-ref` REQUIRED, the person's words through `person_words.read` (:905-907). `_set_pointer` (:352) creates nested objects,
  so `/manual/accounts_way/words` is writable (critic W1).
- F27. `record_stand_account` (:578) writes `environments[i].credentials_by_role[<role>]` — ONE entry per role, a second of the same role refused
  without `--replace` (:638-644); CLI `stand-account --role --user-key --secret-key --words-file [--replace]` (:877-884). It cannot hold several
  accounts of one role: those live only as `env:U/S` handles (`resolve_actor` :769) in a mapped list (critic W2). Readers of a stand account:
  `manual_capture.read_login(..., actor=)` (:634) -> `resolve_actor`; `gate_preflight.account_keys`/`account_role` (used at `manual_capture.py:856-857`).
- F28. Question keys and prices are data in `references/question-prices.json` (`questions`: `s6.stand_login` :195, `s6.stand_confirm` :200,
  `s6.gate_a_dry` :205, `exit.resume_limit` :161); texts are built at the driver site by `Driver.closed_question(key, lead, options)`
  (`story_run.py:4035`) — not in `human-questions.md`, a rules file (critic W4).
- F35. Deferred questions (RN1-24): `deferrable` (`story_run.py:3874-3883`) is False when the question holds no case (`not holds`) or when the S6
  scope has no case outside `holds` (`holds_can_wait` :3885-3895) — then the question STOPS the run; a deferred one is asked only before gate B
  (`deferred_step` :3945-3955); its held cases close as `left_unchecked` (:11920-11929). So RN1-24 is NOT "queue in turn" (critic Q5-a).
- F36. The leftover-accounts line exists: `report_facts.created_accounts_line` (`report_facts.py:924`) over `created_names_path` (critic W3).
- F43. **MyBooks sign-up** (stand source, read only): page route `register: '/register'` (`D:/ws1/mybooks-stand\MyBooks\src\lib\routes.ts:10`);
  API `POST` in `src\app\api\register\route.ts:11` taking `{ email, password, name }` (:21, `registerSchema`), refusing an email already used
  (`EMAIL_TAKEN` :24-28), rate-limited per IP when limiting is on (`registerLimiter` :14-18), answering 201 (:51); the account works at once,
  ordering needs a confirmed email when `emailVerificationRequired()` (:41-48). Add to cart is not ordering.

### Place (2) — S7 control experiments
- F14. `PKG\agents\qa-failure-analyst.md:50-53` (control experiment; through an independent route), Tools `:66-67`, `:70` ("output … goes under the
  task's `evidence/`"); `PKG\skills\qa-story\phases\s7.md:98-99`.
- F15. `contract.TRIAGE_CONTROL_RESULTS` (`contract.py:2133`), reader `triage_control_problems` :2151-2214: `control.evidence` is a file under
  `evidence/` (:2197-2202, `evidence_ref_issue(..., under="evidence")` :5408-5436). The recorder writes under `work/evidence/manual/` (`manual_capture.py:27`).
- F37. The sibling convention: `red_sandbox.py --diagnostic` writes the flat file `evidence/diagnostic-<label>.json` (`red_sandbox.py:2093`; writer
  row `artifact-writers.json:152-155`); `triage_diagnostic_problems` refuses any other name for a `diagnostic` block (`contract.py:2362-2363`).
- F16. The S7 investigation pass: read-only HTTP (`investigation-budget.json:4-7`), `story_run.py:12780-12845`; never a browser (not re-checked by
  the critic).
- F17. No S7 dispatch of arm B went to the stand; the analyst read MyBooks sources (≈ 40 % of exec; t-1954 :65-66, :117-118).
- F38. A role at S7 opening a detached server from inside `claude`'s Bash is UNMEASURED (the host may kill a child at tool end or session end;
  critic N1-h) — Slice 3 pre-measurement.

### Place (3) — the exploratory walk
- F18. It lives INSIDE the first S6 manual window: `brief_pack.exploration_lines` (:2993-3022; empty once any `tried.md` exists :3001-3002),
  cells `exploration_cell_lines` :2957-2990, charter `explore-charter.md` (:1-6, "Take every request cell" :48-49, "Fail ONE request per `ui` call"
  :50-51); axes `perturbations.json` (4). `tried.md` writer: the role (`artifact-writers.json:169-172`).
- F19. TC_014's cells: 12 request lines + "12 more" + 3 axis lines, incl. admin/reviews/wishlist requests outside the case's flow (arm B
  `work\briefs\S6-qa-runner-3-cells.md:4-19`).
- F20. `qa-explore` is NOT a stand walk (`explore_step.py:1-8`, `exploration.json:37-63`); skills: qa-collect, qa-doctor, qa-onboarding, qa-story
  (critic confirmed). Out of scope (§8).
- F21. The S3 exit OWES every flow request each failure kind on a row or a `request_homes` entry (`planning_contract._request_findings`
  :4214-4254). A `request_homes` entry is `{request, failure, reason}` — NO `home` key (`REQUEST_HOME_FIX` :4167; critic W7).
- F39. The S3 lines that name requests: `brief_pack.request_lines` (:2882, its closing line names `request_homes`) and
  `Driver.s3_strategist_lines` / `s3_counted_lines` (`story_run.py:8801, :8834`) — critic W6.

### App card data, load, liveness
- F22. Stand address, accounts by role (names), env key names, case actors: `brief_pack.manual_stand_lines` (:2426); sign-in proof
  `state/sign-in-probe.json` (`manual_capture.py:16-19`): a `ui --session` call signs in by code ONLY for a sign-in gate A proved, else refused
  before anything opens (:17-18); steps that sign in by `fill-account` need no proof (:2813-2822); `ActorSession.prove_after_form` records it (:2511).
  `project-profile.md` sections (`p4-generate.md:447-469`), injected to the runner (`inject-map.json:77-85`). MISSING as data: UI selectors per
  page; the project's way to get more accounts and distinct data.
- F23. Runner start load: `inject-map.json:77-85` (incl. `plugin:references/manual-evidence.md` :80); ratchets `role-load.json:18` (17 887),
  `:32` (16 701); analyst `:19`/`:33` (17 753 / 16 145). `role_load` counts the role's heaviest handover form as a static layer
  (`role_load._static_form_layer` :433-449; `handoffs/s6-runner-to-analyst.yaml` 6 923 B per the critic's rerun) — it stays while the automated
  half fills that form.
- F40. A case's actors are read by `manual_capture._case_actors(task_root, case)` (used by `auto_actor` :829-858); a case naming two accounts is
  refused by `auto_actor` with "one call per account" (:843-846).
- F41. Process liveness by pid + birth: `execution_scheduler._same_process(pid, started)` (`execution_scheduler.py:59`); the lease records the
  holder the same way (critic N1-e, `stand_lease.py:109`). Lease file readers outside `stand_lease.py`: `probe_debt.py:409-410` (`status`),
  `onboard_apply.py:210-211` (`_holder_state`), `:378-381` (door text), fixture `test_install_retire.py:~507-520`. One record per environment
  (`_try_acquire` :176); released only by the same pid (:189).

### The technique taken (`D:/ws1/mybooks-stand\test-automation-framework\.claude\agents\test-runner\AGENT.md`)
- Two files then the browser (`:58-60`); one live browser per case; snapshot as primary verification (`:69`, `:97-100`); evidence before PASS
  (`:21`, `:103-106`); failure protocol with ONE retry (`:126-134`); one JSON result (`:142-160`); tool-call economy (`:25-43`); teardown (`:102`).

---

## §3 Design

### 3.1 One mechanism, three inputs

```
            before (code)                        dispatch (role)                          after (code, INSIDE run_role, before bind)
 lanes, prepare items, app card, stand     walk_session.py step/look/final/verdict   close (end probe into every attempt) -> records
 probe, open session (sign-in by code      on ONE live browser per walker; a step    (build_record / write_unprepared -> write_block)
 only when gate A proved it)               call carries 1..N steps (S6: the item as  -> finalize_task -> form values -> timing
                                           one batch; S7/explore: one step, look),
                                           stop at the first deviation (P26 evidence
                                           written by the server)
```

| place | item handed in | steps known in advance? -> normal step-call mode | who judges the outcome (tier above) | slice |
|---|---|---|---|---|
| S6 case | Given, steps, Thens (`request.json`), its account(s) | yes (the case's steps) -> the item as ONE batch | runner per Then; analyst at S7 accepts/returns (existing) | 1 |
| S7 control | the red's action, the "without the change" variant, the requirement quote | no (the analyst finds the route on the page) -> ONE step (or 2–3 obvious ones) per call | analyst writes `control`; S7 acceptance (existing) | 3 |
| exploration | charter + the cells the plan homes to `explore` | no (the next probe depends on what the page did) -> ONE step (or 2–3 obvious ones) per call | observations -> analyst at S7 (existing `#obs`) | 1: today's cells ride the FIRST lane unchanged; 3: own dispatch |

### 3.2 The session: a kept recorder process per walker (Slice 1, N1a)

New script `PKG\scripts\walk_session.py`. It IMPORTS, never copies, the `manual_capture` pieces listed in §1 (AR-15). Walk id `W` = the dispatch id
(`S6-qa-runner-<n>`): no new controller field in Slice 1.

- **Open (code, `walk_before`):** `walk_session.py open --task-root T --walk W --items <i1,…> --actor <handle|guest> [--actor2 <handle>]` spawns a
  detached server (Windows `CREATE_NEW_PROCESS_GROUP | DETACHED_PROCESS`, POSIX `start_new_session=True`; log `state/walks/<W>.log`). The server:
  assigns itself to a Windows Job object with `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE` (POSIX: its own process group; `close` uses `os.killpg`);
  binds `127.0.0.1:0`; holds TODAY's exclusive stand lease for its whole life (`manual_capture._hold_stand`, job `walk:<W>`; the SERVER process is
  the holder, so only the server releases it); opens ONE Playwright persistent context per actor through
  `ActorSession(folder=state/walks/<W>/sessions/<slug>-<open n>)` — a FRESH folder per open (an orphan's locked profile never blocks the next);
  runs the stand probe ONCE; signs in by code ONLY when gate A proved the recipe (`state/sign-in-probe.json`, F22). Otherwise — no proof, or the
  login by code raised t-1955's `LOGIN_UNKNOWN_CAUSE` (owner `factory`) — it opens UNSIGNED, `signed_in: false`, and the brief tells the walker
  to sign in with `fill-account <selector> <actor> user|secret` steps (the existing door). Only a login refused after the submit (owner `user`)
  makes that actor's session `dead`. Then it writes `state/walks/<W>.json` `{pid, started (birth), port, token (32 random bytes hex), parent_pid,
  parent_started, actors, items, state: "ready", signed_in, landed_on}` atomically. `open` polls ≤ `open_wait_s` (90) and prints ONE JSON line.
- **Items:** `item --walk W --item i` opens the item's next attempt `aN` under `work/evidence/manual/<case>/` and copies the session's START probe
  row into its `probes.jsonl` (`when: start`). A `step` for an item whose attempt is not open yet opens it the same way first (one role call
  saved; `item` stays for an item the role wants to open without a step). At `close` the session's END probe row is appended to EVERY item
  attempt of the walk (`when: end`): one stand identity brackets all items, so `_attempt_files` (F29) accepts each (critic N1-a).
- **Steps: one call carries 1..N steps; the batch is an OPTION, never an obligation (the Lead's decision and the owner's word, 05.11.2026):**
  `step --walk W --item i [--as <actor>] (--steps-file F | --line "<one step>") [--stop-on <rules>] [--final]`. A call holds as many steps as the
  role chooses, from one to `max_batch_steps`, one per line, in the recorder's existing step vocabulary (`manual-capture-steps.json` `steps`:
  `goto`, `click`, `fill` by character, `type`, `press`, `paste`, `fill-account`, `look`, `read` (+ `expect=`, F12), `watch`, `wait`,
  `fail_request`, `restore_request`, `drag`, `capture`) — data, never code; `--line` (or a steps file of one line) is a batch of one, the SAME call
  with the same answer shape, rules and evidence. Which size fits is the role's judgment (AR-2, P27), taught by the charter per place (N4): an S6
  case's steps are known from the case, so the item normally goes as ONE batch; at S7 and in exploration the next step is known only after the
  page is seen, so the normal call is ONE step or a short run of two or three obvious ones. The server runs the call's steps in order through
  `manual_capture._run_steps` on the live page with ONE new keyword `stop=` (F44: `_run_steps` already stops at a step whose outcome is not `ok`;
  the keyword adds the call-back `walk_session.stop_at` after each step's surprise lines are written, and `stop=None`, the `ui` road, behaves
  exactly as today). Evidence per step is written as designed: the step row, its observation, its `surprise:` lines, the call's `surprises` file,
  reads and looks as captures; `attempt.call_surprises` is reset at the start of every call (critic N1-b).
  - **Deviation = the closed, data-defined list** (FR-13, AR-1; `manual-capture-steps.json` `walk_session.stop_reasons`): (1) a step whose outcome
    is not `ok` — element not found or not actionable (`failed`), the step's limit spent (`timeout`), a step the recorder refused (`refused`);
    always a stop, `--stop-on` cannot switch it off, because a later step would act on a page the plan did not reach; (2) a `surprise:` line of
    this step that matches a stop rule; (3) the role's own `read … expect=<text>` reading otherwise (F12; a stop by the role's own planned value,
    never by code's opinion). A stop is NOT a verdict: the recorder never says whether the deviation is a bug (AR-29); it reports facts and stops.
    The call's own limits (`max_batch_steps`, `batch_max_s`) are LIMITS, not deviations: an over-long call is refused before it runs, a spent
    time budget stops the call between steps with reason `batch_time`. In a call of one step a deviation is reported the same way (`stopped` at
    k = 1, `not_run` empty).
  - **Stop rules — default and the role's field.** Data default `walk_session.stop_on_default` = `["status:500-599", "console", "url"]`: an HTTP
    5xx the role did not cause, a console or page error, a navigation no step asked for (`url` is written only then, F44). Recorded as
    `surprise:` but NOT stopping by default: a 4xx (`status:400-499`), a value the application changed while typing (`field`), a watched text
    change (`text`), a repeated or unasked request (`request`), a dropped request (`failed`), a blocked host (`blocked_host`). WHY this default:
    a 4xx and an application-changed value are usually what a negative step is SENT to provoke (MyBooks: «Only 15 in stock» is a 400, «0, 1.5,
    abc become 1» is a `field` line, SUMMARY.md cards 1–4, 17) — stopping there would turn every input-validation S6 item back into single steps
    and buy nothing, because the line is recorded and shown in the answer either way; a 5xx, a console error or an unasked navigation means the
    page is in a state the plan did not foresee, so the next planned step would act blind — the case the plain agent's script could not see (F45).
    A response the role's own `fail_request` produced is never a `status` line (F44, `ours`), so a planned failure never stops the call. The
    role widens or narrows per call: `--stop-on default` (the data list), `--stop-on none` (only rule (1) stops), `--stop-on +field,+status:400-499`
    (add to the default), `--stop-on -console` (remove from it), `--stop-on status:400-599,url` (replace). A token is a kind of `surprise.kinds`
    or `status:<lo>-<hi>` with 400 ≤ lo ≤ hi ≤ 599; anything else refuses the call before it runs (door lists the kinds from the data). A plan
    row's own stop field is F11 (§6). To match `status` by number, `Attempt.surprise` stores the answer's `status` as a number on a `status` line
    (an additive field, written by `_candidates`/`_surprises_after`; readers that ignore it are unchanged); a `status` line whose number is absent
    or unreadable matches every `status:` rule (AR-28: an unknown is never read as "below 500"; the cost of the error is one extra stop).
  - **The answer.** Exit 0 `{"status": "done", walk, item, batch, steps: [{k, step, outcome, surprise: [...]}], last_excerpt, console,
    answer_file}`; exit 1 `{"status": "stopped", …the same up to step k…, stopped_at: {k, step, reason: failed|timeout|refused|surprise|expect|
    batch_time, detail, facts: [the surprise lines that matched]}, not_run: [the step lines after k], page: {url, snapshot_file, excerpt}}`; exit 2
    refused (nothing run); exit 3 the session is not `ready`. The page snapshot of a stop is the `look` reader's text (accessibility tree, else the
    page's text) stored as a state file of the item's attempt (phase `supporting`, label `stop-<batch>-<k>`), its excerpt ≤ `stop_look_chars`
    (1 500) in the answer. The whole answer is ≤ `batch_answer_chars` (4 000) — beyond it the E1.6 cut naming the file; the full answer is always
    stored at `state/walks/<W>/batches/<item>-b<n>.json` before the reply is sent. A stop leaves the session `ready` on the page as it is: the
    role looks, decides and sends the next call (of one step or many) from there.
  - `--final` (done calls only): after the last step, `final --item i` runs as part of the same call. A stopped call takes no `final`.
- `look [<sel>]` stores the accessibility-tree text as a state file; `final --item i` stores the final snapshot and ONE screenshot (phase
  `post_action`, label `final`). Both are refused with `NO_SHOT_IN_WINDOW` (`manual_capture.py:122`) while `SessionAccount.window` is open (so is the
  stop snapshot: the answer says "no snapshot: the sign-in window is open"). `--as <actor2>` acts in the second actor's context (≤ `max_actors` 2
  per walk; a case naming two accounts, F40).
- **Requests seen per item:** `_store_requests_seen` (F8) is called for the item at the first of `final` / `verdict` / the next `item` /
  `close`, with the index of the backend's request log where this item began (critic N1-b).
- **One step call at a time, never two on one page:** the server accepts connections on a `socketserver.ThreadingTCPServer` thread but runs EVERY
  page-touching request (`item`, `step`, `look`, `final`, `verdict`, `close`) on ONE executor — the main thread, which owns the Playwright sync API
  — behind a non-blocking busy lock. A page-touching request that finds the lock held is answered AT ONCE with a refusal through `_refuse`
  ("call <b> of item <i> is running: step <k> of <n> since <t>; wait for its answer — it is also stored at <path> — or ask `status --walk W`");
  `status` is always answered (read-only). A request without the token is refused (through `_refuse`) and logged.
- **Lifetime:** `walk_after` calls `close --walk W` (end probe, copy into attempts, flush, close contexts, delete the profile folders — a
  deletion failure is a note line, never a block —, release the lease, state `closed`). The server also exits after `idle_s` (900) without a
  request, after `max_s` (5 400), or when the parent is gone — `execution_scheduler._same_process(parent_pid, parent_started)` every 5 s
  (Windows reuses pids) — writing state `dead` with the reason.
- **Resume / rerun within the run:** a walk dispatch the driver resumes or reruns (`resume_role`, or `run_role` reusing a saved result) whose
  server is not `ready` gets a NEW server for the same `W` BEFORE the role runs again; the resume words say "your walk session was reopened
  (<signed_in>, <landed_on>); items with a verdict are done; continue with the next".

### 3.3 The thin brief and the app card (Slice 1, N3)

A walk dispatch's brief (written by `brief_pack.build` when `state/walks/<dispatch>.json` exists): header lines, `Walk: <W>, account(s)
<handles|guest>, signed in: <yes on <path> | no: sign in with fill-account>`, the items (id, Given, steps, Thens verbatim, teardown), the app card
path, the commands (`walk_session.py step|look|final|item|verdict|done` only), the rule line "Do not read the application's sources: the app
card and the page are your map; a selector the card lacks is found with `look`". In Slice 1 the FIRST lane of the story also carries today's
`exploration_lines` unchanged (§3.1). No manifest line, no repo map, no `env_probe`, no `finalize_task`, no "Read these files". The fallback brief
(E5s.4: the server could not start) is today's brief plus the PATH of `references/manual-evidence.md` (its grammar is no longer injected, N4).

**App card** `work/app-card.md`, one per story, written by `app_card.py build` (rebuilt when its inputs' hash changes): stand address and entry
routes (project-profile; flow-requests routes with `path:line`), sign-in route and fields (`manual_capture.login_recipe`, proof), accounts as
NAMES and handles (`credentials_by_role`; Slice 2 adds the account way), test data (project-profile "Test data", `config.json test_data`), page
objects of the repo map, walkers' notes `work/app-card-notes.jsonl` (observations `about: card`). Missing data is a line that says so.

### 3.4 The result record (one per item; Slice 1, N2)

`work/walks/<W>/<item>.json`, written by the server on `verdict --walk W --item i --file <verdict.json>`: `{walk, place, item, index, actor,
attempt, started_at, ended_at, steps, batches, stops, thens: [{n, result: pass|fail|inconclusive|unreached, quote, capture}], final: {snapshot,
screenshot} | null, observations: [{step, expected, seen, capture, quote, surprise?, about: case|card}], teardown: done|not_done|none,
limitation?}` (Slice 2 adds `entities`, `needs`; Slice 3 adds `control`, `cells`). `verdict_problems` refuses (via `_refuse`, exit 2, door named): a
Then without result; a pass/fail without a quote found in a capture of THIS item's attempt; a `pass` with no `final` capture after its last action;
`teardown` missing when the item named one. Steps that ran inside a call of many are rows and captures of the item's attempt exactly like steps
sent one per call: the verdict cites them the same way (N2 E2.10). `done --walk W` ends the role's work.

### 3.5 What code does before and after (Slice 1, N5s)

Before (`walk_before`, per lane): `prepare_for_block` (exists); `work/run-report.json` present, else `finalize_task.py <T>` over what is on disk
(F30, F31: the walker's Stop gate needs it); `app_card.py build` if stale; `walk_session.py open`.
After (`walk_after`, called by `run_role` through a new keyword `after=` RIGHT AFTER the result is in hand (fresh or reused, :2851-2855) and
BEFORE `bind` (:2856)): `close`; per S6 item `manual_evidence.record_from_walk` -> `build_record` -> `write_block` (prepared case) or
`write_unprepared` (t-1955 N3, unprepared case); `finalize_task.py <T>`; the form's values `work/handoffs/<dispatch>.values.yaml` from the
records (applied by `handoff_check.py`, the existing path, F30); the timing lines. POSITIONAL INVARIANT: the dispatch is still `running` when
`build_record`/`write_unprepared` call `_running_dispatch` (F10, F13), and the records exist before `handoff`'s exit check and before `finish`.
The role's final message is the digest (one line per item).

### 3.6 Several items, parallel walkers, accounts

- **Lane rule (Slice 1):** `controller.walk_lanes(cases, keys, size)` — group prepared cases by the KEY of their account set (the canonical JSON of
  the sorted `check` objects of `manual_capture._case_actors`, `""` = guest; an unreadable request -> the case id itself, a lane of its own),
  plan-row order inside a key, cut at `size` = `MANUAL_WINDOW_CASES` = **3** (F2). The driver, the door and the progress line call this ONE
  function (AR-15, AR-19). A failing item never stops the dispatch ("evidence, one retry, fail or inconclusive, next item").
- **Parallel (Slice 2):** up to `manual.walkers` (default **3**, owner) dispatches at once on t-1937's chain runner, each with its own server,
  profile, account, attempt folders (disjoint scopes) and `work/walks/<W>/`. A dead walker: its items `inconclusive`, the others go on; S6 closes
  when every lane has finished.
- **Accounts per walker — the project's way, never assumed (Slice 2):**
  1. **Recorded accounts first:** `credentials_by_role` (ONE per role, F27), the mapped list `manual.accounts_way.accounts_by_role.<role>`
     (`env:U/S` handles, F27), and `created:<name>` handles this project's way produced. One signed-in lane per distinct account.
  2. **More lanes than recorded accounts -> IN TURN on the recorded accounts** (the factory never stops, never guesses): those lanes wait for a
     free account; every other lane runs. Code acts only on a MAPPED field: `self_sign_up` (`{page, request: {method, url, body}}` — the walker
     creates its own user with `fill-new-account` on the page, or code creates it before the dispatch through `manual_capture http` with
     `{generated_username}`); `accounts_by_role`; `command` only when its registry row was resolved from a person's words AND the stand is
     `safe_to_break: true` — the conductor's resolved mapping IS the authorization, because `authorized_actions` is prose (F25);
     `limit_by_role.<role>` = n (e.g. 1 for "there is only one account"). Unmapped words go whole to the lane's walker with a first item
     `obtain-account`.
  3. **The question (once per project, D-0043) HOLDS NO CASE (F10):** when lanes wait for accounts and `words` is `"not known"`, the driver raises
     `closed_question("s6.accounts_way", …)` as a deferred question with `holds: []` and a flag that lets `deferrable` take it (F35): it is put at
     the next stop the run makes anyway (gate B at the latest), it stops nothing, and no case is closed `left_unchecked` for it. Before asking,
     `project_decisions.upsert(field_refs=["/manual/accounts_way/words"], …)` opens the registry row (an open row for the pointer -> no new
     question, FR-7). The ANSWER is read by the CONDUCTOR (FR-48, FR-12): `project_decisions.py resolve --id DD-<n> --words-file <f>
     --resolution-ref <ref> --field-values '{"/manual/accounts_way/words": "<the words, whole>"}'` (F26), then rows it opens for the fields it
     can map; env accounts of a role already recorded go into `accounts_by_role` (never a second `stand-account` of the same role, F27).
     `walk_pool.accounts_for` reads the config at EVERY lane launch: an answer that arrives while lanes still wait serves this story; otherwise it
     serves every next story. Unanswered: the registry row stays open (`project_decisions.due`) and is shown again at the next story's first need.
  4. **The walker cannot follow the words:** `needs: {what, how_many}` -> conductor seam (`no_move`, P22); the lane's cases run in turn on the
     recorded accounts.
  5. **Privileged roles:** only recorded distinct accounts or a mapped `accounts_by_role.<role>`; else in turn on the one recorded account.
- **Created accounts after the run:** removed when a mapped `delete_request` exists; else named by the EXISTING `report_facts.created_accounts_line`
  (F36). Data on a `safe_to_break: true` stand is not a project trace (P8/FR-53) but is named; on a stand not `safe_to_break`, code creates nothing.
- **Machine load (estimate):** a walker ≈ one `claude` (0.3–0.5 GB) + headless chromium (0.3–0.5 GB) + server (0.1 GB) ≈ 1 GB; 3 walkers ≈ 3 GB.

### 3.7 Data isolation per walker (Slice 2, N8)

- **Plan field (judgment, S3 strategist; carried by code):** a manual-agent plan row may carry `walk_data: [{kind, exclusive: true|false,
  changes}]` and `walk_global: "<reason>"`. Carried into `request.json` by `prepare_request`. The strategist is told in the S3 brief
  (`brief_pack.request_lines` / `Driver.s3_strategist_lines`, F39) and in its charter (FR-38/AR-10). Kinds are compared after casefold+strip.
- **The project's way to distinct instances:** `manual.data_way` `{words, pools: {<kind>: {existing, create_request, delete_request, command}}}`,
  every field `"not known"` by default; the question `s6.data_way` follows §3.6 step 3 (holds no case).
- **Assignment (`walk_pool.assign`, under the driver lock):** an exclusive kind gets a distinct instance across RUNNING lanes from a mapped pool
  (state `free` in `state/walk-entities.json`), else a mapped create; all entries of one item together or none. With only `words`, the walker
  gets them and a first item `obtain-data`; it CLAIMS the instance it picked with `walk_session.py claim --walk W --kind K --instance I`
  (refused when `in_use` by another running walk) BEFORE changing it.
- **Alone (error direction: toward alone, never toward a collision):** no `walk_data` and no `walk_global` on the row; `walk_global` set; an
  exclusive kind with no mapped pool and no words; an exclusive kind of one running lane that matches no other lane's or pool's kind after
  normalisation.
- **Dirty entities:** `in_use` until the verdict says `teardown: done` (-> `free`), else `dirty`; never re-assigned in the story; a dead walker's
  instances are `dirty`.

### 3.8 The exploratory walk (Slice 3, N7)

The exploration leaves the first case lane and becomes its own walk dispatch at the end of the S6 manual half: the charter and the cells =
`request_homes` entries with the NEW optional field `home: "explore"` plus the field/reload/sign-in axes for pages of the story's own flow.
A ROW's own `requests` failures stay where the row puts them (its case walk or its test). `tried.md` is written by code from the explore record's
`cells`. Plans written by an older package version: not supported by decision of the owner — a story is not carried across package versions.

### 3.9 S7 control experiments (Slice 3, N6)

The analyst decides per red whether it needs a browser (F4). Pre-measurement (F38): one experiment — the analyst opens a server from its Bash
and the server survives the tool call and the session end. If it does not, the S7 DRIVER opens the control walk on the analyst's request line
in its form (the role never spawns it). Evidence follows the diagnostic sibling (F37): the record `evidence/control-<label>.json` and its attempt
under `evidence/control-<label>/aN/`, so `control.evidence` satisfies `under="evidence"` (F15).

### 3.10 Expected numbers and their carriers — PER PLACE

All walker numbers below are **estimates** (no walker has run); the plain-agent numbers are measured (F45). The estimate is built from one turn
per tool call of ≈ 6–12 s (Sonnet), browser steps of ≈ 1.5–2.5 s (each step settles, is observed and watched by the detector, keys at a person's
pace; F2's 0.65 s/step had no detector), up to `ELEMENT_WAIT_S` 30 s for a step whose element is missing (F44), and the item's share of open +
after-step (records, `finalize_task`) + reading the brief ≈ 30–40 s. The «one or two recorder calls per item» claim holds ONLY for the S6 case,
whose steps are known in advance (owner's word 21:20).

**(1) S6 manual case — steps known from the case; the item goes as ONE batch.** Smooth item = Write the steps file, `step --steps-file … --final`,
Write the verdict file, `verdict` = 4 role tool calls, 1 recorder call; plus its share of the lane's own calls (reading the brief and the card ≈ 2,
`done` 1, per ≤ 3 items) ≈ 1 → **≈ 5 tool calls**; a stopped item adds a look-and-decide turn and one more steps file + call per stop, 1–2 stops
→ **≈ 7–9 tool calls, 2–4 recorder calls**.

**(2) S7 control experiment — steps NOT known in advance; ONE step (or 2–3 obvious ones) per call.** The analyst finds the route to the red's
action on the page, does it once with and once without the change's condition, and compares: ≈ 8–15 steps sent as ≈ 6–10 calls, each followed by
a look-and-decide turn, plus `final` and the control record → **≈ 12–20 tool calls, ≈ 6–10 recorder calls, ≈ 3–6 min**. Not compared with the
plain agent: its load had its steps written in advance.

**(3) Exploration — steps NOT known in advance; ONE step (or 2–3 obvious ones) per call.** Per cell: put the failure on, act, look, read what
the page told the person, restore: ≈ 3–6 calls, each a look-and-decide turn → **≈ 5–10 tool calls and ≈ 1.5–3 min per cell**. Not compared with
the plain agent.

| place | expected per item | basis | carrier that can refuse it |
|---|---|---|---|
| per-call overhead of today's recorder | measured by P0 (Slice 1 pre-step) | unmeasured today (F2); paid ONCE per walk now, not per call | `experiments/mybooks/thinking-roles/walker-call-overhead.md` (P0 writes the number HERE and into this row) |
| S6 case, smooth (no stop) | ≈ 110–140 s wall, ≈ 5 tool calls, 1 recorder call | (1) above — **estimate** | `walk_timing.py --task T --summary` (wall, tool calls, recorder calls per item) |
| S6 case, stopped 1–2 times | ≈ 170–230 s, ≈ 7–9 tool calls, 2–4 recorder calls | (1) — **estimate** | same |
| S6 case, mean over the 24 disputed places | ≈ 140–170 s, ≈ 6 tool calls, ≈ 1.7 recorder calls; ≤ 7 min and ≤ $0.50 still the refusing limit (§7 step 4) | about one item in three stops (the disputed places are where the page misbehaves, but most of their faults are `fail_request` (ours, no stop) or `field`/4xx lines (no stop by default)) — **estimate**; cost rises with index (F42) | `walk_timing.py --task T --summary`: dispatch wall ÷ items from `state/driver-runs.jsonl` + the after-step's end line; cost by item index from the transcript |
| S6 tokens per item | printed in four parts (uncached input, cache creation, cache read, output) and as the dispatch's final context ÷ items; ≈ 1–2K output tokens per item (a 10-line steps file and a verdict file instead of a 60–150-line script) — **estimate** | which quantity the host's `subagent_tokens` counts is NOT established (F45); compared only on the same quantity (§7) | `walk_timing.py --task T --summary --json` |
| S7 control (UI, Slice 3) | ≈ 3–6 min, ≈ 12–20 tool calls, ≈ 6–10 recorder calls, ≤ $0.40 | (2) above — **estimate**; no plain-agent speed promised | same, place `control` |
| exploration (Slice 3) | ≈ 1.5–3 min and ≈ 5–10 tool calls per cell; ≤ 30 min, ≤ $1.80 per story of ≈ 10 cells | (3) above — **estimate**; no plain-agent speed promised | same, place `explore` |
| 24 disputed places (§7, S6-like), 1 / 3 walkers | ≈ 55–70 min / ≈ 20–30 min wall | 24 × 140–170 s; three lanes in parallel, admin lanes in turn — **estimate** | `walk_timing.py --task T --summary` |

**Against the plain agent — S6-like load only (F45: 136 s, 3.75 tool calls, ≈ 20.7K tokens per card; its cards had their steps written in
advance, so nothing here speaks for S7 controls or exploration):**
- On S6 cases the walker should be about as fast to **≈ 1.3× slower per item** (≈ 140–170 s against 136 s) and use **more tool calls** (≈ 6
  against 3.75). Where it is slower and why: (1) evidence per step — every step settles, is observed (screenshot + excerpt) and watched by the
  surprise detector, where the plain agent's script screenshotted only where it chose; (2) it STOPS where the page does not behave as planned and
  the role looks and decides (2–4 more tool calls on such an item) — the plain agent's script ran blind to its end; this is the judgment the owner
  wants (P26) and the place where the plain agent's evidence is weakest; (3) the verdict cites recorded words checked by code, and the after-step
  builds the case records and `run-report.json` — work the plain agent did not do; (4) a dispatch holds ≤ 3 items (F2), so the start load
  (≈ 15–18K tokens, F33 minus N4) is paid per 3 items, where the plain agent paid it per 8.
- Where it should be faster: no code is written per item (a steps file of ≈ 10 data lines instead of a script), so no script debugging and
  re-runs (part of the plain agent's 3.75 calls); one browser and one sign-in per walk instead of per script.
- Tokens: no honest number can be compared until the quantity is the same (above); the walker's output tokens per item should be lower, its
  context re-reads per item higher (more turns).

---

## §4 Slices and nodes (each node written for a weaker model; direction chosen)

General for every node: tests are FAST files only; slow files (F34; `test_story_run_*`, `test_controller_*`) are judged by CI. Every package
commit carries `architecture:` and `judgment:` lines. `python -B ai-packages/qa-factory/scripts/selftest.py --lang` (FR-30) in each witness.
Witness commands run from `D:/ws1/wt-fbfix`. `owns:` paths are absolute; for the hot files (`story_run.py`, `controller.py`,
`manual_capture.py`, `manual_evidence.py`, `brief_pack.py`) the functions are named and nothing else in that file is touched. Compatibility with
stories, plans, evidence or state written by an older package version is **not supported by decision of the owner — a story is not carried
across package versions**: no node reads, migrates or tests an old shape.

### SLICE 1 — «serial fast walk» (build first; proves the speed claim; executable right after t-1955 lands; NO dependency on t-1937)

Order: t-1955 merged -> P0 (any time, no code); N1a ‖ N4 ‖ N3 (`app_card.py` part) -> N2 (after N1a) -> N3 (`brief_pack.py`, `role-commands.json`
after N1a) -> N5s (after N1a, N2, N3). Shared files inside the slice, in this order: `walk_session.py` N1a then N2; `judgment-census.json` N1a
then N2; `artifact-writers.json` N1a then N2. One walker; today's exclusive lease; no new config key.

#### P0 — one experiment: today's recorder, per call (Lead, environment run; pt.6a)

Run in a COPY of the MyBooks stand project (never the arm B tree while its driver runs; the Lead names the copy `<C>` and a prepared guest case
`<TC>`), three times each: (a) a 2-step file `goto <frontend>/` + `read body` without `--session`; (b) the same with `--session user` after a
`fill-account` sign-in in the first call. Command (PowerShell, no cwd change):
`Measure-Command { python -B D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\manual_capture.py ui --task-root <C>\qa-factory\artifacts\<TICKET> --case <TC> --steps-file <scratch>\two-steps.txt }`
Per-call overhead = wall − (last − first `at` of the call's `steps.jsonl` rows). Written: the three walls, the step span, the median overhead
into `D:/ws1/yml-text-factory\experiments\mybooks\thinking-roles\walker-call-overhead.md` and into the §3.10 row. The number does not gate
N1a (in-page state between calls is the main reason, critic §2) but sets the expected saving. Also measured (same file, same run): (c) a
10-step guest file, to give the per-step time of today's recorder WITH the surprise detector (the §3.10 basis uses 1.5–2.5 s, an estimate).

#### N1a — the kept-session server `walk_session.py` (step calls of 1..N steps, items, lifecycle)

**owns:**
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\walk_session.py` (new: `open`, `item`, `step` (1..N steps), `look`, `final`, `done`, `close`, `status`, `request_problems`, `_refuse`, `stop_rules`, `stop_at`, `serve`, verdict storing without checks — N2 adds them)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\manual_capture.py` (`_store_requests_seen` — optional keyword `since=` (request-log index); `lane_key` new: the canonical key of a case's account set from `_case_actors`; `_run_steps` — optional keyword `stop=None` (called after each step's surprise lines; a returned reason ends the loop like a non-`ok` step, the row's own outcome unchanged; `None` = today exactly); `_candidates`, `_surprises_after`, `Attempt.surprise` — the answer's `status` as a number on a `status` line only; per F12 (a): `parse_steps` (arity of `read`) and the `read` branch of `_run_step` (`expect=`); nothing else)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\manual-capture-steps.json` (object `walk_session`: `open_wait_s` 90, `idle_s` 900, `max_s` 5400, `answer_chars` 2000, `parent_check_s` 5, `max_actors` 2, `max_batch_steps` 20, `batch_max_s` 100, `batch_answer_chars` 4000, `stop_look_chars` 1500, `stop_on_default` `["status:500-599", "console", "url"]`, `stop_reasons` `["failed", "timeout", "refused", "surprise", "expect", "batch_time"]`, and a `does` text that says a call holds 1..`max_batch_steps` steps (one step is a call of one) and why the default stops on 5xx/console/url and not on 4xx/field (§3.2); per F12 (a): `steps.read` arity `[1, 3]` and its `does` text for `expect=<text>`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\artifact-writers.json` (`work/evidence/` machinery + `walk_session.py`; new key `state/walks/` (incl. `state/walks/<W>/batches/`) writer `walk_session.py`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json` (rows `walk_session.py::request_problems` xref, `::_refuse` shape, roles `["conductor"]`, owner data; `blocking_per_role.conductor` + 1)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_walk_session.py` (new)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_walk_batch.py` (new; the step-call rule, fake backend)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-1957-n1a.md` (new)

**non-goals:** step words and their behaviour (except, per F12 (a), `read … expect=`); observe caps; surprise detection (except the `status`
number on a `status` line); what the detector writes for a `ui` call; `manual_capture ui/http/app` behaviour (a `ui` call passes `stop=None`
and stays byte-for-byte as today); lease file shape (N1b); `fill-new-account` (N1c; see L1); verdict checks (N2); driver wiring (N5s); a plan
row's stop field (F11); any rule on how many steps a role puts in a call (the role's judgment, taught by N4).

**Required behaviour:** §3.2 exactly. Backend through `manual_capture._new_backend` (honours `BACKEND_FACTORY`, F8): tests run the server
in-process with a fake backend and never spawn a browser. Every refusal goes through `_refuse(problems)` (the ONE raise site). The step call:
`request_problems` checks it BEFORE any step runs (parse through `manual_capture.parse_steps`; 1 ≤ steps ≤ `max_batch_steps`; every
`--stop-on` token through `stop_rules`; no call running); a call of one step and a call of many take the SAME path (no separate single-step
code); `stop_rules(tokens, data)` returns the rule list (default from data, `+`/`-`/replace, `none`); `stop_at(row, found, rules, started,
data)` returns `None` or `{reason, detail, facts}` in this order: the row's outcome not `ok` -> `failed|timeout|refused`; a `read … expect=` that
read otherwise -> `expect`; a surprise line of THIS step matching a rule -> `surprise`; the call's time spent beyond `batch_max_s` ->
`batch_time`. On a stop: the stop snapshot (`look` reader, unless the sign-in window is open), the answer with `not_run`, the answer file, state
`ready`. Error direction of `stop_at` (a reused detector's facts in a more consequential role: advice -> a stop): it may stop where the role
would have gone on (cost: one more role call); it never runs a planned step on after a step that did not run, after a 5xx the role did not
cause, a console error or an unasked navigation under the default rules. Adversarial inputs that must stay on the safe side: a `status` line
whose fact was replaced by `not kept: …` (secret scan) and so has no readable number -> stops; a 5xx that arrives AFTER the last step (the late
pump, F44 :3229-3237) -> the call answers `stopped` at the last step, not `done`; a `url` line on a `goto` that was redirected to the sign-in
page -> stops; a `fail_request` 500 the role set -> never a `status` line, never stops; `--stop-on none` with a step that timed out -> still stops.

**edges (each with its invariant):**
- E1.1 `open` with an actor held by a live session (`state/walks/*.json` `ready` and `_same_process` true) -> refused "account <handle> is walking
  in <W>; wait or name another account". INVARIANT: two live sessions never share an account.
- E1.2 a record whose server died (`_same_process` false) -> taken over: state `dead (taken over)`, its profile folder deleted when possible
  (failure = one note line); the new open uses a FRESH folder `-<n+1>`. INVARIANT: an orphan never blocks an account or a profile.
- E1.3 `step` with a wrong token, an unknown/closed walk, or an item outside the walk -> refused naming `status --walk W`; nothing executed.
- E1.4 server not ready within `open_wait_s` -> killed (job / process group), exit 3 "the walk session did not start: <log tail ≤ 300 chars>".
  INVARIANT: no half-open session is handed to a role.
- E1.5 sign-in: gate A proof present and the login by code lands -> `signed_in: true`. No proof, or `LOGIN_UNKNOWN_CAUSE` (owner `factory`) ->
  open UNSIGNED, `signed_in: false`, the walk lives. Owner `user` (refused after submit) -> that actor's session `dead`, `env_blocked.json` per
  item as `manual_capture._blocked` writes it. INVARIANT: a factory-owned sign-in failure never kills the walk (t-1955 N2: only `user` locks).
- E1.6 answer longer than `answer_chars` (a step call: `batch_answer_chars`) -> cut with "[cut: N more chars in <file>]". INVARIANT: the stopped
  step, its reason and the `not_run` count are never the part that is cut (they are written first).
- E1.7 idle / max / parent gone -> contexts closed, profiles deleted when possible, lease released BY THE SERVER, state `dead`; a later `step`
  -> E1.3. INVARIANT: the lease never outlives its holder by more than `parent_check_s`.
- E1.8 Windows hard kill of the server -> the Job object kills node + chromium; POSIX -> `killpg` at close. INVARIANT: no browser outlives its
  server (a failure of this is a note in `status`, measured in §7).
- E1.9 TEMPORAL (within the run): a case already walked through the fallback road (`manual_capture ui`, E5s.4) has attempts on disk; a walk
  opens the NEXT `aN`. INVARIANT: evidence on disk is never rewritten.
- E1.10 POSITIONAL: the stand probe runs at `open` and `close` only; each item attempt gets the session's start row when it opens and the end
  row at close. INVARIANT: every item attempt has a start AND an end probe of the same stand (F29), so `build_record` accepts it; a stand that
  changed between open and close shows as a provenance change on every item, never hidden on some.
- E1.11 `look`/`final` (and the stop snapshot) while `SessionAccount.window` is open -> refused with `NO_SHOT_IN_WINDOW` (the stop snapshot: the
  answer says so instead). INVARIANT: no screen or text of the sign-in window is stored (axis 5 "How the stand logs in").
- E1.12 paths with spaces / non-ASCII case ids -> `manual_capture.case_dir_name` rules (reused).
- E1.13 requests seen: item k's file holds only requests from item k's first step to its flush. INVARIANT: a request is never attributed to
  another item's attempt.
- E1.14 `call_surprises` reset per step call. INVARIANT: a surprise line appears once, in the file of the call that met it.
- E1.15 walk profiles live under `state/walks/<W>/sessions/`, never under an attempt. INVARIANT: `_attempt_files`' live-profile refusal (F29
  :1532-1536) never fires for a walk attempt; cookies never sit beside a record.
- E1.16 TEMPORAL (resume within the run): `open` for a `W` whose record is `dead`/`closed` -> new server, same `W`, `reopened: n` in the record.
  INVARIANT: items with a verdict on disk are never walked again in that dispatch.
- E1.17 `--as <actor2>` beyond `max_actors` -> refused naming the limit. Empty `--items` -> refused "a walk has at least one item".
- E1.18 EMPTY step call (a steps file with no step: empty, blank lines or `#` lines only) -> refused "a step call has at least one step",
  nothing run, no attempt opened. INVARIANT: an answer `done` always means at least one step ran.
- E1.19 a call over `max_batch_steps` -> refused before any step runs: "<n> steps; a call holds at most <max>: send steps 1–<max> now and the
  rest as the next call". INVARIANT: a call runs as sent up to its first deviation, or not at all — never silently cut. Boundary: exactly
  `max_batch_steps` runs; one more is refused.
- E1.20 the FIRST step deviates -> `stopped` at k = 1, steps 2..n listed in `not_run`, the page snapshot returned, step 1's row and evidence
  written. INVARIANT: no step after a deviation ever runs in that call.
- E1.21 the LAST step deviates (its own outcome, a matching surprise line, or a late surprise line after it) -> `stopped` at k = n, `not_run`
  empty, the page snapshot returned, no `--final` taken. INVARIANT: an answer is `done` only when no deviation happened — a deviation is always
  shown to the role, even when nothing was left to skip (P26: every doubtful place reaches the role). A call of ONE step is this edge's
  everyday case.
- E1.22 a second step call (or `look`/`final`/`item`/`verdict`) while a call of the same walk runs -> refused AT ONCE through `_refuse` with
  the door "wait for call <b> (step <k> of <n> since <t>); its answer is stored at <path>; `status --walk W` shows it"; `status` answered.
  INVARIANT: two calls never act on one page at once, and the running call is never interrupted by the refusal.
- E1.23 the caller of a step call is gone (the host ended the role's shell call) -> the server finishes the call (or stops it at
  `batch_max_s`), stores the answer file, frees the busy lock; `status` names the last call and its file. INVARIANT: a call's evidence and
  answer are never lost because nobody waited for them. (A single step may itself run up to its stand's limit, F44; `batch_max_s` is checked
  between steps.)
- E1.24 a stopped call does not end the item: its attempt stays open, the next call of the same item writes into the same attempt, and the END
  probe is copied into it at `close` as for every item (E1.10); an item the role leaves after a stop (the next `item`/`step` of another item)
  is flushed (E1.13) and still gets its end probe at `close`. INVARIANT: a stop never leaves an attempt that `build_record` must refuse.
- E1.25 `--stop-on` with an unknown kind, a malformed range, or `status:` outside 400–599 -> refused before any step, the door lists
  `surprise.kinds` and the range form from the data. INVARIANT: the stop list stays the closed data list (FR-13).
- E1.26 `--stop-on none` -> only reason (1) of §3.2 stops; a `status:` rule never matches a line the role's own `fail_request` caused (it is not
  written, F44). INVARIANT: a step that did not run is never followed by a step that assumes it ran.
- E1.27 `--final` on a call that stopped -> no final capture; the answer says "no final: the call stopped". INVARIANT: a `final` is taken only
  after the item's planned last action ran (N2 E2.3 then refuses a pass until the role's own later `final`).
- E1.28 the `ui` road (`manual_capture ui`, `stop=None`) -> identical rows, files and exit codes to today. INVARIANT: the fallback road (E5s.4)
  and every existing caller of `_run_steps` are unchanged.
- E1.29 a call of one step (`--line`, or a steps file of one line) -> the same path, answer shape, stop rules and evidence as a call of many;
  nothing in the server prefers or requires a batch. INVARIANT: the batch is an option, never an obligation (owner's word 21:20) — a role that
  walks one step at a time (S7, exploration) is never refused, slowed or warned for it.

**DoD — `test_walk_session.py` (fast, fake backend):** `test_open_writes_state_with_token_loopback_and_birth`,
`test_step_runs_on_kept_page_no_reopen` (backend opened once for three `step`s), `test_fill_keys_by_character_kept`, `test_surprise_lines_once_per_call`,
`test_look_stores_state_file`, `test_final_one_snapshot_one_screenshot`, `test_look_final_refused_in_signin_window`, `test_wrong_token_refused_nothing_run`,
`test_actor_held_refused`, `test_dead_record_taken_over_fresh_profile_dir`, `test_profile_delete_failure_is_a_note`, `test_idle_exit_releases_lease`,
`test_parent_gone_by_same_process`, `test_answer_cut_names_file`, `test_next_attempt_after_fallback_attempts`, `test_every_item_attempt_has_start_and_end_probe`
(`manual_evidence._attempt_files` accepts each), `test_requests_seen_split_per_item`, `test_login_unknown_opens_unsigned`,
`test_user_refused_signin_is_dead`, `test_reopen_keeps_items_with_verdict`, `test_second_actor_context`, `test_step_opens_item_attempt_when_not_open`.
**DoD — `test_walk_batch.py` (fast, fake backend whose steps and surprise lines are scripted):** `test_batch_runs_all_steps_in_one_call_done`,
`test_single_step_call_is_a_batch_of_one` (E1.29: `--line` and a one-line file give the same answer shape and evidence as a many-step call),
`test_batch_empty_refused_nothing_run` (E1.18), `test_batch_at_limit_runs_over_limit_refused` (E1.19, at and beyond),
`test_first_step_deviation_stops_rest_not_run` (E1.20), `test_last_step_deviation_says_stopped` and `test_late_5xx_after_last_step_says_stopped`
(E1.21), `test_second_batch_while_running_refused_with_door` and `test_status_answered_while_batch_runs` (E1.22; a fake step that blocks on an
event), `test_batch_answer_stored_when_caller_gone` (E1.23), `test_stopped_item_keeps_attempt_end_probe_at_close` and
`test_next_batch_runs_from_the_same_page` (E1.24), `test_stop_on_unknown_kind_refused_names_kinds` (E1.25), `test_stop_on_none_still_stops_on_failed_step`
(E1.26), `test_final_flag_only_on_done` (E1.27), `test_ui_call_unchanged_without_stop` (E1.28), `test_default_stops_on_5xx_console_url`,
`test_default_records_4xx_and_field_without_stop`, `test_stop_on_widened_and_narrowed_per_call`, `test_own_fail_request_never_stops`,
`test_status_number_recorded_on_status_line`, `test_unreadable_status_number_stops`, `test_stop_snapshot_state_file_and_excerpt`,
`test_no_stop_snapshot_in_signin_window`, `test_batch_time_budget_stops_between_steps`, `test_stop_rules_from_data`; per F12 (a):
`test_read_expect_differs_stops_and_records`, `test_read_expect_in_ui_call_only_recorded`.
Negative controls: with the end-probe copy disabled, `test_every_item_attempt_has_start_and_end_probe` fails; with `stop=` not passed by the
server, `test_default_stops_on_5xx_console_url` fails (the builder shows each red once).
Witness: `python -m pytest ai-packages/qa-factory/scripts/tests/test_walk_session.py ai-packages/qa-factory/scripts/tests/test_walk_batch.py ai-packages/qa-factory/scripts/tests/test_manual_capture_session.py ai-packages/qa-factory/scripts/tests/test_manual_requests_seen.py ai-packages/qa-factory/scripts/tests/test_artifact_writers.py ai-packages/qa-factory/scripts/tests/test_judgment_census.py -q`
`architecture:` AR-1, AR-2, AR-9, AR-13, AR-14, AR-15, AR-20 (raise named), AR-22, AR-25, AR-28, AR-29.

#### N2 — the result record, the reducer to the case record, timing

**owns:**
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\walk_session.py` (`verdict_problems`, `write_verdict`, `timing_line` only — after N1a)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\manual_evidence.py` (`record_from_walk` new; nothing else)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\walk_timing.py` (new: `--task T [--summary] [--json]`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\artifact-writers.json` (key `work/walks/` writer `walk_session.py` — after N1a)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json` (row `walk_session.py::verdict_problems` xref, non-blocking — after N1a)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_walk_record.py` (new)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-1957-n2.md` (new)

**non-goals:** `build_record`, `write_block`, `write_unprepared`, `finalize_task`, the handoff vocabulary, the driver; how a step call runs (N1a).

**Required behaviour:** §3.4. `verdict_problems` uses `manual_evidence._quote_in`. It reads the item's attempt (steps.jsonl, captures.jsonl) and
NEVER the call answer files: a step's evidence is the same whether it ran alone or inside a call of many, so the verdict is checked the same way.
"The last action" = the last EXECUTED action row of the item's `steps.jsonl` (a `not_run` step has no row). `record_from_walk(task, case,
walk_record) -> dict` calls `build_record(task, case, result, actual, masked=True, attempt=<the item's attempt>, quotes=[f"{n}={quote}" …],
observations=…)` with `result` = `fail` if any Then is `fail`, else `inconclusive` if any is `inconclusive`/`unreached`, else `pass` (a pure fold
of the role's own per-Then words, said in the docstring); for an unprepared case it calls `write_unprepared(task, case, observations)` instead.
`timing.jsonl`: one line per item `{item, index, place, started_at, ended_at, steps, batches, stops, attempt}` (`batches` = recorder step calls,
`stops` counted from `state/walks/<W>/batches/<item>-b*.json`). `walk_timing.py`: per dispatch, wall = its first `launched` row in
`state/driver-runs.jsonl` -> the `walk_after` end line (`work/walks/<W>/timing.jsonl` `{after_end}`), ÷ items, and the role-session wall alone
(launched -> the role's result) for the comparison with a plain agent that has no after-step; cost = the LAST `total_cost_usd` per `session_id`
(cumulative over resumes, F1); cost by item index = the session transcript's requests (`cost_capture.scan_file` -> `{key: (model, usage, ts)}`,
valued by `cost_capture.value_usage`) summed inside each item's `[started_at, ended_at)`; tool calls per item = the transcript's `tool_use`
blocks inside the same windows, plus the dispatch's calls outside any item window ÷ items; tokens per item in four parts (uncached input, cache
creation, cache read, output) and the dispatch's final context ÷ items; recorder calls and stops per item from `timing.jsonl`; every figure
grouped by `place` (S6 case, control, explore), never averaged across places; prints the conductor's spend of the same story separately when its
cost record exists (P18).

**edges:**
- E2.1 a `pass` Then without quote -> refused ("quote the capture that shows it"). INVARIANT: no pass without recorded words (P26).
- E2.2 a quote found only in another item's attempt -> refused. INVARIANT: a receipt measured on other bytes never counts.
- E2.3 a `pass` with no `final` capture after the last action -> refused (door `final --item i`). Error direction: may refuse a pass an earlier
  capture showed (cost: one `final` call); never accepts a pass with no capture after the last action. Adversarial inputs that stay refused:
  `final` BEFORE the last action; `final` of another item; a `final` file deleted after; a `final` taken after a STOPPED call but before the
  corrected call's actions.
- E2.4 no verdict when the session ends -> every Then `inconclusive`, limitation "the walker ended before its verdict" (AR-28); the record is
  still built (FR-23).
- E2.5 `unreached` Thens -> `build_record`'s unreached path.
- E2.6 empty `observations` -> legal (AR-23).
- E2.7 an unprepared case -> `write_unprepared` with the observations, never `build_record`. INVARIANT: no pass/fail from an unprepared walk.
- E2.8 `build_record` refuses an item (e.g. no captures) -> `record_from_walk` returns `{"refused": <text>}`; N5s re-queues the case ONCE.
  INVARIANT: a refusal is never swallowed into a pass and never loses the case.
- E2.9 `walk_timing.py` with no `timing.jsonl` -> "no walk timed for <task>", exit 0; a broken line is counted and named (FR-41); no transcript
  found for a session -> cost by index, tool calls and tokens "not measured: <why>", never 0.
- E2.10 a step that ran inside a call of many is a row and its captures are captures of the item's attempt, exactly as a step sent alone.
  INVARIANT: a quote's validity never depends on how the steps were grouped — the same steps sent as one call or one by one give the same
  `verdict_problems` result.
- E2.11 `not_run` steps of a stopped call have no row and no capture. INVARIANT: a step that never ran is never evidence and never "the last
  action".
- E2.12 the stop snapshot is a `supporting` state file of the item's attempt: quotable like a `look`. INVARIANT: a stop snapshot of ANOTHER item
  stays refused (E2.2); a stop snapshot is never a `final` (a pass still needs a `final` after the last action).
- E2.13 a `--final` capture taken by a `done` call is after that call's last step by construction and satisfies E2.3 when no later action ran.
- E2.14 an item with calls but no verdict and a last call `stopped` -> E2.4, with the stop's step and reason added to the limitation.
  INVARIANT: the record says where the walk stopped; never a silent inconclusive.

**DoD — `test_walk_record.py` (fast):** `test_pass_without_quote_refused`, `test_quote_from_other_item_refused`, `test_pass_needs_final_after_last_action`,
`test_final_before_last_action_refused`, `test_final_of_other_item_refused`, `test_fold_fail_wins`, `test_missing_verdict_is_inconclusive`,
`test_record_from_walk_builds_valid_record` (`manual_evidence.validate_record` -> no problem), `test_unprepared_goes_to_write_unprepared`,
`test_build_refusal_returned_not_raised`, `test_timing_wall_from_driver_runs`, `test_cost_last_value_per_session`, `test_cost_by_item_index`,
`test_timing_absent_says_so`, `test_batch_and_single_steps_give_same_verdict_problems` (E2.10), `test_not_run_steps_are_not_actions` (E2.11),
`test_stop_snapshot_quotable_not_final` and `test_stop_snapshot_of_other_item_refused` (E2.12), `test_final_flag_capture_satisfies_pass` (E2.13),
`test_final_between_stopped_and_corrected_batch_refused` (E2.3), `test_stopped_without_verdict_names_stop` (E2.14),
`test_tool_calls_and_tokens_per_item_from_transcript`, `test_batches_and_stops_per_item`, `test_figures_grouped_by_place`,
`test_tool_calls_not_measured_says_why` (E2.9).
Negative control: with the attempt read replaced by the call answer files, `test_batch_and_single_steps_give_same_verdict_problems` fails. Witness:
`python -m pytest ai-packages/qa-factory/scripts/tests/test_walk_record.py ai-packages/qa-factory/scripts/tests/test_walk_session.py ai-packages/qa-factory/scripts/tests/test_walk_batch.py ai-packages/qa-factory/scripts/tests/test_manual_evidence.py ai-packages/qa-factory/scripts/tests/test_artifact_writers.py ai-packages/qa-factory/scripts/tests/test_judgment_census.py -q`
`architecture:` AR-12, AR-14, AR-21, AR-22, AR-23, AR-28, AR-29.

#### N3 — the app card and the walk brief

**owns:**
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\app_card.py` (new: `build --task-root T`; prints a line, never refuses)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\brief_pack.py` (`walk_brief_lines` new; `build` — the manual branch :3318-3319 only: when `state/walks/<dispatch_id>.json` exists, the walk brief; the first lane keeps `exploration_lines`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\role-commands.json` (rows for `walk_session.py` subcommands — after N1a; `test_role_commands.py` feeds every registered command a broken file, CI)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_app_card.py` (new)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_walk_brief.py` (new; a temp task, no repo map)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-1957-n3.md` (new)

**non-goals:** S5 briefs; the automated half of S6; the repo map builder; the account/data way (Slice 2); `brief_pack.walk_lines` (S3).

**Required behaviour:** §3.3. Card sections in order, each a line or "not known: <why>": Stand, Entry routes, Sign-in, Accounts, Test data,
Page objects, Notes from walkers. Readers reused: `env_probe.frontend_of`, `manual_capture.login_recipe`, `brief_pack.manual_stand_lines` parts,
`user_path_failures.read_requests`, `created_names_path`, `report_facts.created_accounts_line`, `manual_capture.read_login` (names only). Card ≤
8 000 B; beyond -> entry routes cut ("+N more: work/flow-requests.json").

**edges:** E3.1 no project-profile -> "not known: no strategy/project-profile.md (onboarding)". E3.2 no sign-in proof -> "Sign-in: not proven
at gate A — sign in with fill-account" (matches N1a E1.5). E3.3 a secret-looking value in any input -> never printed. INVARIANT: the card holds no
credential value. E3.4 first line "routes and data to walk with; expectations come only from the case's Thens" (FR-58). E3.5 TEMPORAL (within the
run): a dispatch with no `state/walks/<id>.json` (the fallback road, E5s.4) -> today's brief plus the PATH of `references/manual-evidence.md`.
INVARIANT: a role on the fallback road has the recorder grammar within one read. E3.6 POSITIONAL: the walk branch sits AFTER `sd_head_lines`
(:3316-3317) so the charter header lines stay; `exploration_lines` is added only for the story's first lane. INVARIANT: exploration cells are
neither dropped (Slice 1) nor repeated in later lanes.

**DoD:** `test_app_card.py`: `test_sections_in_order_with_not_known`, `test_no_secret_values`, `test_cut_at_limit_names_rest`,
`test_hash_rebuild_only_on_change`, `test_first_line_says_no_oracle`, `test_walker_notes_included`, `test_created_handles_names_only`.
`test_walk_brief.py`: presence of `Walk:`, `App card:`, each item's Thens verbatim, `walk_session.py step`, `fill-account` when unsigned;
absence of `manifest_view`, `env_probe`, `finalize_task`, `Read these files`; `test_first_lane_keeps_cells_later_lanes_do_not`;
`test_fallback_brief_names_manual_evidence_path`; negative control: an item whose Thens are removed fails `test_item_thens_present`. Witness:
`python -m pytest ai-packages/qa-factory/scripts/tests/test_app_card.py ai-packages/qa-factory/scripts/tests/test_walk_brief.py -q`
(CI: `test_role_commands.py`, `test_brief_pack*.py`). `architecture:` AR-8, AR-11, AR-13, AR-23.

#### N4 — the walk charter; shorter runner texts (ratchet down)

**owns:**
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\walk-charter.md` (new, ≤ 4 500 B)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\agents\qa-runner.md`
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\explore-charter.md` (the tool words of `:50-51` only: "per `ui` call or `walk_session.py step` call")
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\inject-map.json` (qa-runner: `plugin:references/manual-evidence.md` -> `plugin:references/walk-charter.md`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\role-load.json` (qa-runner rows DOWN to the measured value)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_walk_charter.py` (new; key presence of the step-call paragraph)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-1957-n4.md` (new)

**non-goals:** the analyst's charter (Slice 3; N6 points the analyst at the same paragraph); the strategist; `manual-evidence.md` itself (stays:
automated half, analyst, fallback).

**Required behaviour — walk-charter.md (craft, P27):** read the item and the app card, then the browser; sign in with `fill-account` when the
walk says unsigned; **[the step-call paragraph below]**; then `fail` or `inconclusive` (stand vs product, `qa-runner.md:49`) and on to the next
independent Then or item; evidence before pass: `final --item i` (or `--final` on a call that ends the item); every doubtful place an observation
when met (P26); type as a person; teardown of your own data; independent calls together; never read application sources. `qa-runner.md`: Tools ->
two lines (walk commands; automated half `run_suite.py`); delete "Error guessing from the code facts" (`:50`) and the
`env_probe`/`finalize_task`/seed lines (`:61`); point 4 (`:26`) moves to explore-charter.

The step-call paragraph, EXACT text (package English, ≈ 1 350 B). It REPLACES the single-step loop of the earlier draft of this charter — "act ->
read the answer (excerpt, surprises, console) -> `look` when the excerpt does not decide; a failed step: `look` + actual vs expected in one
sentence + a hypothesis -> ONE retry with another locator" — so the charter grows by ≈ 1 050 B against that draft and stays ≤ 4 500 B; the
role-load ratchet still goes DOWN, because the injected `manual-evidence.md` (11 995 B) leaves (E4.1). The walk charter is the runner's (S6 cases
and, in Slice 1, the exploration cells of the first lane); it says which mode fits which place because the same runner meets both:

> **How many steps per call.** A `walk_session.py step` call takes one step or many; choose by what you know. A manual case gives you its steps:
> write every step you plan for the item, from the first action to the last read, into one steps file and send it with
> `walk_session.py step --item <i> --steps-file <f> --final`. Exploration cells, and any walk where the next step depends on what the page shows,
> do not: send ONE step, or two or three obvious ones, look at the answer, decide the next. The recorder runs the steps in order, keeps the
> evidence of each, and stops at the first deviation: a step that could not run, an error the page did not expect (by default a 5xx, a console
> error, a navigation no step asked for), or a `read ... expect=` that read otherwise. Add `--stop-on +field` or `+status:400-499` when the item
> is about values or refusals the page must not produce; the default records them without stopping. When the recorder stops, look before you
> act: read the stopped step, its facts and the page snapshot in the answer, and say in one sentence what you planned and what the page did.
> Then decide: a locator to correct, a page state your plan did not foresee, or a doubtful place to record as an observation. Continue from the
> page as it is now. Never send the same steps again unchanged: one corrected call per stopped step; a second stop on that step is a result
> (`fail` or `inconclusive`), not a reason to retry. Every stop and every `surprise:` line you did not plan is an observation of the item.

**edges:** E4.1 role-load grows -> STOP and report (no raise). INVARIANT: the ratchet only shrinks (AR-20). E4.2 the handover form's static
layer (F23) stays — the automated half still fills it; the walk dispatch's live load (`role_load.py --dispatch`) shows it gone, reported, not
claimed in the ratchet. E4.3 FR-30. E4.4 a runner on the fallback road reads the grammar by the path its brief names (N3 E3.5). E4.5 the
charter names only the stop kinds and flags N1a's data defines (`status:`, `field`, `console`, `url`, `--final`, `expect=`); a word the data
does not hold is a defect of the charter. INVARIANT: the role is told the stop list the recorder actually applies (AR-10). E4.6 per F12: if the
Lead answers (b), the clause "or a `read ... expect=` that read otherwise" is deleted from the paragraph and from the key list. E4.7 the
paragraph never makes a batch a duty: it names the mode per place and the reason (known steps vs steps found on the page). INVARIANT: the
batch stays an option (owner's word 21:20); a charter line that orders every item into one batch is a defect.

**DoD:** `test_walk_charter.py` (fast): `test_step_call_paragraph_present` — keys quoted VERBATIM from the paragraph above, written before the
run: "A `walk_session.py step` call takes one step or many", "A manual case gives you its steps", "send ONE step, or two or three obvious ones",
"stops at the first deviation", "look before you act", "Never send the same steps again unchanged", "a second stop on that step is a result";
`test_charter_words_exist_in_data` (E4.5: every `--stop-on` token and flag the charter names is in `manual-capture-steps.json`
`walk_session`/`surprise.kinds`); negative control: the test run on a copy of the charter with "send ONE step, or two or three obvious ones"
removed fails. `python -m pytest ai-packages/qa-factory/scripts/tests/test_walk_charter.py ai-packages/qa-factory/scripts/tests/test_role_load.py ai-packages/qa-factory/scripts/tests/test_charter_form.py -q` and
`python -B ai-packages/qa-factory/scripts/role_load.py --role qa-runner` output attached; rows lowered to the measured values (< 17 887 / < 16 701).
`architecture:` AR-2, AR-10, AR-11, AR-20.

#### N5s — the driver: serial walk lanes, code before/after inside `run_role`, twins

**owns:**
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\story_run.py` (`run_role` — keyword `after=` and its one call between :2855 and :2856, nothing else; `resume_role` — the reopen before the resume and the same `after` call; `run_manual_block`; `manual_plan`; `walk_before` new; `walk_after` new)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\controller.py` (`MANUAL_WINDOW_CASES` 1 -> 3; `walk_lanes` new, pure; nothing else)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\story_step.py` (`_manual_block_door` — `walk_lanes` instead of `manual_blocks`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\story_progress.py` (`_block_position` — total from `walk_lanes`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\skills\qa-story\phases\s6.md` (lines 6-7, 46: "a manual window is up to 3 cases that share one account set")
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_manual_window.py` (pin `(3, 5)`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_story_progress.py` (C4 pin :881-882 only; SLOW — CI)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_walk_lanes.py` (new; `Driver` stubbed as in `test_manual_window.py`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-1957-n5s.md` (new)

**non-goals:** controller op `dispatch` (one running dispatch, as today); parallel lanes (Slice 2); the automated half; `stand_login_gate`;
t-1955 N3's unprepared prompt line (kept as it lands, used only on the fallback road); the skill road opening walk sessions (queued, below);
stories started on an older package version (not supported by decision of the owner).

**Required behaviour:** `manual_plan` cuts `ready` with `walk_lanes(ready, {c: manual_capture.lane_key(T, c)}, MANUAL_BLOCK_MAX)`
(`MANUAL_BLOCK_MAX = MANUAL_WINDOW_CASES` line kept: `test_story_run_s6.py` T329-g pins it). `run_manual_block` runs ONE lane per entry, as
today's one block per entry: registers the dispatch (unchanged path), `walk_before(lane, dispatch_id)` (§3.5), then `run_role(…,
after=lambda d, r: self.walk_after(lane, d, r))` with the walk brief and no `finalize_task` line. `walk_after` (§3.5): `close`;
`record_from_walk`/`write_unprepared` per item; a `refused` item (N2 E2.8) re-queued ONCE into the next lane, a second refusal -> the existing
`manual_close` road with the refusal as the reason (`left_unchecked`); `finalize_task.py <T>`; `work/handoffs/<dispatch>.values.yaml` from the
records; timing end line. `walk_after` is idempotent (records already on disk are skipped), so a reused saved result runs it safely.

**edges:**
- E5s.1 POSITIONAL: `after` runs after the result exists (fresh or reused) and BEFORE `bind`, `handoff`, `question_threshold`,
  `repair_limit_gate`, `finish`. INVARIANT: the dispatch is `running` when `_running_dispatch` binds the records (F10), the records and
  `run-report.json` exist before the exit check, and `finish` never closes a lane whose records were not attempted.
- E5s.2 the role crashes / `Refusal` / empty result -> `after` still runs (a `try/finally` at the hook site); items without a verdict ->
  `inconclusive` (N2 E2.4). INVARIANT: «Фабрика не должна вставать»; no case vanishes.
- E5s.3 TEMPORAL (within the run): `walk_before` finds no `run-report.json` (F31) and `finalize_task` cannot make one from zero blocks -> the walk
  brief gets today's line "then `finalize_task.py <task root>`" as the walker's last command. INVARIANT: the walker's Stop is never refused for a
  file it cannot make.
- E5s.4 POSITIONAL: assignment and `open` happen BEFORE the role starts and after the dispatch is registered; `open` fails (exit 3) -> the lane
  runs on today's road: no walk record, today's brief + the path of `manual-evidence.md` (FR-57). INVARIANT: a registered running dispatch always
  has its brief lines (the G3 rule of `run_manual_block` :12228-12235).
- E5s.5 cases accepted earlier IN THIS RUN (`manual_done_cases`) are never dispatched again; rework dispatches keep their `--scope`.
- E5s.6 TEMPORAL (resume within the run): `resume_role` of a walk dispatch whose server is not `ready` -> `walk_session.py open` (N1a E1.16)
  BEFORE the resume words, which name the reopened session; then the same `after`. INVARIANT: a resumed walker never holds a dead `W`.
- E5s.7 unprepared cases (t-1955 N3) -> walked in their lane, closed by N2 E2.7.
- E5s.8 a lane key that is a single case (unreadable request) -> a lane of one. INVARIANT: an account is never guessed for a case.
- E5s.9 the twins: the door and the progress line count lanes with the same function and size. INVARIANT: the skill road, the driver and the
  progress line never disagree on the number of manual dispatches (AR-19).

Queued (not owned, reason): the SKILL road opening walk sessions (no driver there; `story_run.py:3860` precedent "the skill road has no code for
it yet") — a row for the Lead's pile; `s6.md` says the skill road walks with `manual_capture` until then.

**DoD — `test_walk_lanes.py` (fast):** `test_groups_by_account_set_and_cuts_at_three`, `test_guest_cases_one_lane`, `test_unreadable_request_lane_of_one`,
`test_after_runs_before_bind` (stub `bind` records whether records exist), `test_after_runs_on_reused_saved_result`, `test_after_runs_when_role_crashes`,
`test_after_is_idempotent`, `test_build_refusal_requeued_once_then_closed`, `test_open_failure_falls_back_to_capture_road`,
`test_run_report_made_before_walk`, `test_done_cases_not_redispatched`, `test_resume_reopens_session_first`, `test_door_and_progress_use_walk_lanes`.
Negative control: `after` moved after `finish` in a stub makes `test_after_runs_before_bind` fail. Witness:
`python -m pytest ai-packages/qa-factory/scripts/tests/test_walk_lanes.py ai-packages/qa-factory/scripts/tests/test_manual_window.py -q`;
CI: `test_story_progress.py`, `test_story_run_s6.py`, `test_story_step_manual_block.py`. Critic mandatory (core). `architecture:` AR-14,
AR-15, AR-19, AR-25, AR-28, AR-29.

Inside Slice 1: N1a, N4 and the `app_card.py`/`test_app_card.py` part of N3 run in parallel (disjoint files); N2 after N1a; N3's
`brief_pack.py`/`role-commands.json` part after N1a; N5s last. `story_run.py` and `manual_evidence.py` functions are disjoint from t-1955's
(t-1955 N3 owns the `run_manual_block` prompt line :12243-12246 and `write_unprepared`/`write_block`; N5s edits `run_manual_block` after t-1955
merges, D-0048).

### SLICE 2 — «parallel walkers» (after Slice 1 is proved live)

Step calls of 1..N steps (N1a) work the same in every walker of Slices 2 and 3; no node below changes them.

Dependency: t-1937 P1 — N-P1-1 (op `dispatch` admission), N-P1-3 (config key), N-P1-4 (`S5Scheduler`, `self._book`, `launch` releasing it).
**If t-1937 P1 is not landed** (today: not in wt-fbfix, F12): Slice 2 ships N1b, N1c and N8 with walkers forced to 1 and prints ONE
`note: parallel walkers are not available yet (S5 parallel windows not installed); walking with 1` per S6 entry; N5p waits.

#### N1b — shared `walk` lease mode and every reader of the lease file

**owns:**
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\stand_lease.py` (`hold` — `mode="exclusive"|"walk"`, `max_shared`; `_try_acquire`; `status`; `release_by_person`; `_holder_state`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\run_suite.py` (`hold_stand` — pass `mode`, default exclusive)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\probe_debt.py` (the reader at :409-410 only)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\onboard_apply.py` (readers :210-211 and the door text :378-381 only)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_install_retire.py` (the lease fixture ~:507-520 only)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\walk_session.py` (`open`/`close` lease mode only — after Slice 1)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_stand_lease_walk.py` (new)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-1957-n1b.md` (new)

**non-goals:** the lease wait policy; `run.parallel` semantics; stand probes; lease records written by an older package version (not supported
by decision of the owner).

**Required behaviour:** the lease record per environment holds `holders: [{job, pid, started, mode}]`; `walk` holders ≤ `max_shared` with
distinct jobs; an exclusive request waits for zero `walk` holders and vice versa; each holder releases only itself (pid + birth). Every reader
above reads the new shape (producer and readers in one commit, AR-22).

**edges:** E1b.1 a suite and a walk never overlap on a serial stand. E1b.2 `run.parallel: false` came from onboarding's "one account" (F9) ->
walkers > 1 only on accounts recorded per walker (N8); from `execution.parallel.mode: serial` -> walkers 1 always. INVARIANT: the shared mode
never re-reads a project fact. E1b.3 a person's `--release` releases every holder of the stand, each named. E1b.4 a holder whose process is
gone (`_same_process` false) -> dropped at the next acquire, named in the notes. INVARIANT: a dead walker never holds the stand.

**DoD:** `test_stand_lease_walk.py`: `test_two_walk_holders_admitted`, `test_walk_over_max_waits`, `test_exclusive_waits_for_walk`,
`test_walk_waits_for_exclusive`, `test_each_holder_releases_itself`, `test_dead_holder_dropped`, `test_status_lists_all_holders`. Witness:
`python -m pytest ai-packages/qa-factory/scripts/tests/test_stand_lease_walk.py ai-packages/qa-factory/scripts/tests/test_stand_lease.py ai-packages/qa-factory/scripts/tests/test_manual_requests_seen.py -q`
(CI: `test_install_retire.py`, `test_run_suite_mine.py`). `architecture:` AR-13, AR-22, AR-25.

#### N1c — `fill-new-account` and a lock on `CreatedAccounts.add`

**owns:**
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\manual_capture.py` (`CreatedAccounts.add` — a file lock around read-modify-write; `_run_steps` — the step word `fill-new-account`; `parse_steps` — its arity; nothing else)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\manual-capture-steps.json` (word `fill-new-account <selector> user|secret [template]`; data row `generated_user_template` default `{generated_username}`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_fill_new_account.py` (new)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-1957-n1c.md` (new)

**non-goals:** account removal; the account way (N8).

**Required behaviour:** `user` -> `generated_account` makes the pair; the name, shaped by the template (`{generated_username}@<domain>` when the
form validates email — the template is the walker's argument or the project's data row), goes to `created-accounts.json` through
`CreatedAccounts.add` under the lock; the value is typed by character; `secret` -> the same pair's password; log, answer and evidence carry
`created:<name>` and `[generated]`, never a value; the step opens the sign-in window like `fill-account`.

**edges:** E1c.1 `secret` with no `user` before it in the item -> refused "type the user first". E1c.2 two walkers add at once -> both rows kept.
INVARIANT: a created account's password is never lost. E1c.3 a generated value matching `secret_content_patterns` is never stored in a text file.
INVARIANT: no credential value in any text a role or a person reads. E1c.4 a stand not `safe_to_break` -> refused "this stand may not be
changed". E1c.5 template without `{generated_username}` -> refused naming the placeholder. E1c.6 the app refuses the sign-up (e.g. MyBooks
`EMAIL_TAKEN` or its rate limit, F43) -> the step fails with the page's words; the account is recorded `unconfirmed`, never used as an identity.

**DoD:** `test_fill_new_account.py`: `test_records_name_never_value`, `test_secret_before_user_refused`, `test_concurrent_add_keeps_both`
(two processes), `test_email_template`, `test_not_safe_to_break_refused`, `test_opens_signin_window`, `test_refused_signup_is_unconfirmed`. Witness:
`python -m pytest ai-packages/qa-factory/scripts/tests/test_fill_new_account.py ai-packages/qa-factory/scripts/tests/test_manual_actor.py ai-packages/qa-factory/scripts/tests/test_manual_capture_session.py -q`.
`architecture:` AR-14, AR-25. Census: no new unit (refusals inside the existing `_run_steps`/`parse_steps` flow; the builder confirms with
`test_judgment_census.py` and names any change).

#### N5p — parallel lanes on t-1937's runner (default 3 walkers)

**owns:**
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\story_run.py` (`run_manual_block` lane scheduling; a shared chain base extracted from `S5Scheduler` and used by both — after t-1937 N-P1-4)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\controller.py` (op `dispatch` admission: the S6 clause beside t-1937's S5 clause; optional dispatch field `walk_actor`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\templates\config.json`, `D:/ws1/wt-fbfix\ai-packages\qa-factory\references\config-keys.json`, `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\config_contract.py` (key `manual.walkers`, int ≥ 1, default **3**)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_walk_lanes_parallel.py` (new)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-1957-n5p.md` (new)

**non-goals:** S5 scheduling; the account way (N8); the lease (N1b).

**Required behaviour:** launch up to `manual.walkers` lanes at once for which N8 gives distinct accounts and free entities; an `alone` lane only
when nothing runs; each lane's code steps under `self._book`, the role session outside it (t-1937 discipline). `walk_after` of parallel lanes
writes story-wide files (`finalize_task`, `created-accounts.json`) under `self._book`; `finalize_task` of lane A tolerates lane B's attempts
without records. Controller: running dispatches coexist only when ALL are S5 windows (t-1937) OR ALL are S6 `execution_kind: manual` with
pairwise disjoint `scope`, pairwise distinct `walk_actor` (absent = guest) and count ≤ the walkers value given. Launch rule (iii) of t-1937 ("no
question is pending") counts only LIVE questions: a deferred question that holds no case (F10) is not pending.

**edges:** E5p.1 `manual.walkers` absent in the config (a project not yet answered) -> 3; not an int ≥ 1 -> 3 + one `note:` line; t-1937 absent ->
1 + the note (above). INVARIANT: never silently 1. E5p.2 a lane crashes -> its `after` runs; others go on; S6 closes on the finish that leaves no
lane open (a lane whose state cannot be read counts as open, FR-59). E5p.3 no S6 walk beside an S5 window, a suite or another stage's dispatch;
two running dispatches never share a case or an account. E5p.4 `walkers: 1` -> Slice 1 behaviour exactly (parity test).

**DoD:** `test_walk_lanes_parallel.py`: `test_walkers_default_three`, `test_bad_value_three_with_note`, `test_no_t1937_one_with_note`,
`test_walkers_1_is_serial_parity`, `test_two_lanes_distinct_accounts_overlap` (fake `run_role` records overlap), `test_alone_lane_runs_by_itself`,
`test_lane_crash_others_go_on`, `test_story_files_written_under_lock`, `test_deferred_no_hold_question_not_pending`. Witness:
`python -m pytest ai-packages/qa-factory/scripts/tests/test_walk_lanes_parallel.py ai-packages/qa-factory/scripts/tests/test_walk_lanes.py ai-packages/qa-factory/scripts/tests/test_config_migration.py -q`;
CI: `test_controller_state.py`, `test_story_run_s5_parallel.py`. Critic mandatory (core). `architecture:` AR-3, AR-14, AR-15, AR-25, AR-28.

#### N8 — the project's way to accounts and data (asked once, holds no case), isolation per walker

**owns:**
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\walk_pool.py` (new: `accounts_for`, `assign`, `release`, `mark_dirty`, `ask_accounts_way`, `ask_data_way`, `delete_created`, `status`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\walk_session.py` (`claim`, `claim_problems` only — after N1b)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\story_run.py` (`deferrable` — the holds-nothing clause; `defer_question` — `holds: []` kept; the two `closed_question` sites `s6.accounts_way`, `s6.data_way` inside `walk_before`'s account step — after N5p)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\manual_capture.py` (`_CREATE_ROUTE` text only: "this project's way of getting accounts is in config `manual.accounts_way`; the factory asks the person once" — after N1c)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\manual_evidence.py` (`prepare_request` — carry `walk_data`/`walk_global` from the plan row)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\planning_contract.py` (`_walk_data_problems` new, called from the S3 exit)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\brief_pack.py` (`request_lines` — one line on `walk_data`/`walk_global` for manual-agent rows)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\agents\qa-test-strategist.md` (one craft paragraph on `walk_data`; its `role-load.json` row must not grow — E8.15)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\templates\config.json`, `D:/ws1/wt-fbfix\ai-packages\qa-factory\references\config-keys.json`, `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\config_contract.py` (keys `manual.accounts_way` `{"words": "not known"}` with optional `self_sign_up`, `accounts_by_role`, `limit_by_role`, `delete_request`, `command`; `manual.data_way` `{"words": "not known", "pools": {}}` — after N5p)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\question-prices.json` (keys `s6.accounts_way`, `s6.data_way` — after t-1955 N4)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\conductor-actions.json` (one `actions` row "the person told how this project gets accounts/data" — after t-1955 N1)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json` (rows `walk_session.py::claim_problems` xref, `planning_contract.py::_walk_data_problems` shape; any blocking change named)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_walk_pool.py` (new)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-1957-n8.md` (new)

**non-goals:** writing MyBooks's ways into its config (§7 does it through the conductor's route); the onboarding interview (F9(b), owner); a new
leftover line (`report_facts.created_accounts_line` is the one).

**Required behaviour (who asks, who writes, who reads):** §3.6 steps 1–5 and §3.7. `accounts_for(task_root, lanes, cfg)` reads
`credentials_by_role`, `manual.accounts_way` (words + mapped fields), `created-accounts.json`; lanes beyond the accounts run IN TURN, except that a
mapped `self_sign_up` gives each extra ordinary lane a first item `obtain-account` (the walker registers with `fill-new-account`), privileged
roles excluded. `ask_accounts_way(task_root, need)` calls `project_decisions.upsert(field_refs=["/manual/accounts_way/words"], essence="how this
project gets more test accounts", asked=<text>, scope=…, owner="person")` and returns the question for `closed_question("s6.accounts_way", lead,
options)` with `holds=()`; options are examples, free words taken (P9, P22). The conductor's resolution: `project_decisions.py resolve --id
DD-<n> --words-file <f> --resolution-ref <ref> --field-values '{"/manual/accounts_way/words": "<words>"}'`; further rows for mapped fields.
`walk_pool` reads a mapped value that matches `secret_content_patterns` as absent (a note line, never used, never printed).

**edges (invariant each):**
- E8.0 the question holds no case: `deferrable` True for `holds: []` with the no-hold flag; it is asked at the next stop the run makes (gate B
  at the latest) and never stops the run by itself; no case is closed `left_unchecked` for it. INVARIANT: the factory never stands still and
  never drops a case over an accounts/data question.
- E8.1 a row without `walk_data` and without `walk_global` -> ALONE ("the plan does not say what the walk changes"). Error direction: toward
  alone (slower), never toward a collision. Adversarial inputs that stay alone: `Book` vs `books` vs ` book ` from one planner (casefold+strip
  equates only the first and third; an unpaired kind runs alone); `walk_data: []` on a row a later walker changes (the planner's judgment,
  accepted at S7).
- E8.2 a pool smaller than the lanes needing the kind -> later lanes wait for a `free` instance. E8.3 dirty instance -> never re-assigned.
- E8.4 two kinds -> all or none; partial -> wait one round -> alone with reason.
- E8.5 a Then asserting on a collection other walkers change -> the planner writes `walk_global`; code reads it -> alone.
- E8.6 `accounts_by_role` shorter than the lanes -> the listed accounts used; the rest IN TURN; NO new question (D-0043); the run output names
  "<k> lanes wait: the project's list holds <n> accounts". `limit_by_role.<role>: 1` -> one lane of that role at a time, no question ever.
- E8.7 the answer changes later -> a new row for the same pointer; running lanes keep their assignment; the next `accounts_for` reads the new
  value. INVARIANT: an assignment in flight is never re-pointed.
- E8.8 the walker cannot follow the words, or a self sign-up fails (N1c E1c.6) -> `needs` -> conductor seam; the lane's cases run in turn on
  recorded accounts.
- E8.9 stand not `safe_to_break` (or flag absent) -> code creates nothing; the brief says so. INVARIANT: FR-53.
- E8.10 a secret in the person's words -> the registry keeps the words as written; the brief masks secret-pattern hits as `[masked]` — the
  owner's F8 (§5) may change the registry side.
- E8.11 a mapped `command` whose registry row was NOT resolved from a person's words -> never run by code. INVARIANT: prose
  `authorized_actions` never authorises code (F25).
- E8.12 TEMPORAL (within the project's life on this version): ways `"not known"` until answered; plans without `walk_data` -> E8.1;
  `created-accounts.json` written earlier in the run read as this story's handles; other registry rows untouched.
- E8.13 a mapped `accounts_by_role` entry naming a missing env key -> skipped with a note; values never printed.
- E8.14 `claim` of an instance `in_use` by another running walk -> refused naming the holder walk. INVARIANT: two walkers never change one
  instance.
- E8.15 the strategist's `role-load.json` row grows -> STOP and report (AR-20).

**DoD — `test_walk_pool.py` (fast):** `test_recorded_accounts_first`, `test_extra_lanes_in_turn_no_stop`, `test_question_holds_no_case`,
`test_question_asked_once_open_row_reused`, `test_answer_in_time_serves_remaining_lanes`, `test_self_sign_up_gives_obtain_item_ordinary_only`,
`test_words_only_hands_words_and_obtain_item`, `test_never_refuses_unmapped_way`, `test_list_shorter_than_walkers_waits_no_question`,
`test_limit_one_never_asks`, `test_changed_answer_next_assignment_only`, `test_unresolved_command_never_run`, `test_not_safe_to_break_creates_nothing`,
`test_secret_looking_mapped_value_ignored`, `test_distinct_instances_per_running_lane`, `test_kind_normalised_unpaired_alone`, `test_claim_in_use_refused`,
`test_pool_too_small_waits`, `test_dirty_not_reassigned`, `test_two_kinds_all_or_none`, `test_no_field_runs_alone_with_reason`, `test_global_runs_alone`,
`test_defaults_without_keys`. Witness:
`python -m pytest ai-packages/qa-factory/scripts/tests/test_walk_pool.py ai-packages/qa-factory/scripts/tests/test_config_migration.py ai-packages/qa-factory/scripts/tests/test_manual_actor.py ai-packages/qa-factory/scripts/tests/test_judgment_census.py ai-packages/qa-factory/scripts/tests/test_role_load.py -q`;
CI: `test_project_decisions_*.py`, `test_report_facts.py`, `test_brief_pack*.py`. Critic mandatory. `architecture:` AR-2, AR-3, AR-13, AR-14, AR-15,
AR-16, AR-17, AR-22, AR-23, AR-24, AR-25, AR-27, AR-29.

Inside Slice 2: N1b ‖ N1c (disjoint files: `stand_lease`/readers vs `manual_capture.CreatedAccounts.add`/`_run_steps`/`parse_steps`); N5p after
t-1937 P1 and N1b; N8 after N1c (`manual_capture._CREATE_ROUTE`), N1b (`walk_session.py`), N5p (`story_run.py`, config files). `story_run.py`: N5p
{`run_manual_block`, chain base} then N8 {`deferrable`, `defer_question`, the question sites}. N1c touches `_run_steps`/`parse_steps` AFTER N1a's
`stop=` keyword and `read` arity landed (Slice 1 merged first).

### SLICE 3 — S7 controls and exploration on the walker

The same step call (N1a) serves a control walk and the explore walk; there the role does not know the next step before it sees the page, so its
normal call is ONE step or a short obvious run (owner's word 21:20; the walk charter's paragraph, N4); no node below changes the call.

#### N6 — S7 control experiments through the walker

Pre-measurement (F38): one live S7 dispatch in a stand copy where the analyst runs `walk_session.py open --place control …` from its Bash; the
record says whether the server survives the tool call and the session end. Survives -> the role opens it (F4 (a)); not -> the S7 driver opens
it on the analyst's request (a form line) and the role only steps.

**owns:**
`D:/ws1/wt-fbfix\ai-packages\qa-factory\agents\qa-failure-analyst.md` (Tools: one line `walk_session.py --place control`; delete `manifest_view.py`/`env_probe.py` from `:66`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\role-commands.json` (analyst rows for `walk_session.py … --place control`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\role-load.json` (analyst rows down)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\walk_session.py` (`--place control` roots: `evidence/control-<label>.json` + `evidence/control-<label>/aN/`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\artifact-writers.json` (key `evidence/control-*.json` writer `walk_session.py`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\story_run.py` (`stage_S7` — one `walk_session.close_all(task_root, place="control")` in a `finally` after the analyst's `run_role`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_walk_control.py` (new)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-1957-n6.md` (new)

**non-goals:** the investigation pass; API controls (`run_suite --request`/HTTP stay); triage verdicts.

**edges:** E6.1 the stand cannot run the control -> `control.result: impossible` with `why` (unchanged). E6.2 a control record outside
`evidence/` -> refused by the existing reader. INVARIANT: the control's evidence is a file the RUN wrote. E6.3 sessions left by a dead analyst
-> closed by the S7 `finally` and N1a E1.7. E6.4 the analyst's role-load grows -> STOP (AR-20).

**DoD:** `test_walk_control.py`: `test_control_record_under_evidence`, `test_triage_control_accepts_walk_record` (`contract.triage_control_problems`
-> `[]`), `test_work_evidence_path_refused`, `test_close_all_after_role`. Witness:
`python -m pytest ai-packages/qa-factory/scripts/tests/test_walk_control.py ai-packages/qa-factory/scripts/tests/test_triage_control.py ai-packages/qa-factory/scripts/tests/test_role_load.py ai-packages/qa-factory/scripts/tests/test_artifact_writers.py -q`.
Census: no new unit. `architecture:` AR-13, AR-14, AR-21, AR-29.

#### N7 — the exploratory walk as its own dispatch

**owns:**
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\planning_contract.py` (`REQUEST_HOME_FIX` and `_request_findings` — optional `home: "explore"`; nothing else)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\user_path_failures.py` (`exploration_cells` — argument `homes`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\brief_pack.py` (`request_lines` — the `home` line; `build` manual branch — cells leave the case lanes when the explore walk runs — after N8)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\agents\qa-test-strategist.md` (one sentence: a request homed `explore` is walked by the exploration, not by a row — after N8)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\story_run.py` (`run_explore_walk` new, called by `run_manual_block` after the last lane; `s3_strategist_lines` — the `home` line)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\walk_session.py` (`write_tried` only)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\artifact-writers.json` (`work/evidence/manual/<case>/tried.md` writer -> `walk_session.py`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_explore_walk.py` (new)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-1957-n7.md` (new)

**non-goals:** `perturbations.json` axes; the S3 obligation itself (F21 kept); plans written by an older package version (not supported by
decision of the owner — a story is not carried across package versions).

**edges:** E7.1 a ROW's own requests -> walked where the row puts them (its case or its test), never a cell. E7.2 a cell whose request is never
sent -> `not tried: the request was not sent` (existing `failures_without_hits`). E7.3 an `explore` home for a request not in
`flow-requests.json` -> the S3 refusal names it (existing identity join). E7.4 no `explore` home -> "S6: no exploration cells in the plan"
(declared empty, AR-23). E7.5 the strategist's role-load grows -> STOP (AR-20). E7.6 POSITIONAL: `run_explore_walk` runs after the LAST case
lane's `after` and before S6's closing finish. INVARIANT: S6 never closes before the explore walk's record exists or is declared empty.

**DoD:** `test_explore_walk.py`: `test_only_explore_homed_requests_are_cells`, `test_row_requests_not_cells`, `test_no_home_no_walk_line`,
`test_tried_written_by_code_from_cells`, `test_explore_home_satisfies_s3_obligation`, `test_home_named_in_s3_brief`, `test_explore_walk_before_close`.
Witness: `python -m pytest ai-packages/qa-factory/scripts/tests/test_explore_walk.py ai-packages/qa-factory/scripts/tests/test_flow_requests.py ai-packages/qa-factory/scripts/tests/test_exploration_perturbations.py ai-packages/qa-factory/scripts/tests/test_role_load.py -q`.
`architecture:` AR-10, AR-14, AR-21, AR-23, AR-26.

Inside Slice 3: N6 ‖ N7 (`story_run.py` {`stage_S7`} vs {`run_explore_walk`, `s3_strategist_lines`}; `walk_session.py` {control roots} vs
{`write_tried`}; `artifact-writers.json` N6 then N7).

### Open for the Lead (found while revising; not decided here)
- **L1. Card 21 of §7 needs a NEW user in Slice 1** ("registration -> sign-in"), but `fill-new-account` is N1c (Slice 2) and the walker may not
  type a credential with `fill`. Options: (a) move the step word (without the lock — one walker) into N1a; (b) card 21 walks up to the
  registration and ends `inconclusive` with the reason in Slice 1, fully in Slice 2 (where MyBooks' self sign-up is recorded, §7). Recommendation:
  (a) — the lock is only needed for parallel walkers.
- **L2. `finalize_task.py` on a story with no run block yet** (F31) — whether it writes `run-report.json` was not established; N5s E5s.3 gives
  the safe behaviour either way.

---

## §5 Questions for the owner (only these two)

- **F8. A secret typed into the free answer.** When you answer the factory's question about accounts in your own words and the words contain
  something that looks like a password or a token, should the factory keep your words exactly as you wrote them in the project's decision log
  (the log is the project's own file) and only hide that part (`[masked]`) in what it shows its agents? Or should it hide that part in the log
  too (then your words are no longer kept whole)? **Recommendation: keep the words whole in the log, hide the secret-looking part from agents;**
  the factory never copies a value into its settings in either case.
- **F9(b). Ask about accounts and data already at onboarding?** Today the factory would ask «how does this project get more test accounts / more
  distinct test data» only when a run first needs it (the run does not stop for it). Should the onboarding interview ask it up front too (one
  more question at onboarding, but the very first parallel run already knows the answer)? **Recommendation: yes, add it to onboarding as an
  optional question the person may skip;** the in-run question stays for projects onboarded earlier.

The batch decision raises no new owner question: it answers her own question about scripts, her word of 21:20 is applied (the batch is an
option; per-place numbers), and the stop default is a technical trade-off the Lead may change (F11–F12 below).

---

## §6 Forks — record of decisions (closed by the Lead/owner, 05.11.2026) and forks still open for the Lead

- F1 = (a) our kept-session recorder (Lead). F2 = up to 3 items per dispatch (`MANUAL_WINDOW_CASES` = 3), re-decided by §7's cost by item index
  (Lead). F3 = (a) keep the S3 obligation, add `home: "explore"` (Lead; N7). F4 = (a) the analyst decides per red (Lead; N6). F5 = 3 walkers by
  default, config key `manual.walkers` (owner, 18:55). F6 = (a) the strategist fills `walk_data` (Lead). F7 = (a) the form's values written by
  code (Lead; N5s through `<dispatch>.values.yaml`). F10 = the accounts/data question holds no case (Lead; N8 E8.0). F8, F9(b) — §5.
- Step batches with stop at the first deviation — decided by the Lead; the batch is an option, known steps only at S6 — the owner (Status block).

**Open for the Lead (returned by the designer, 05.11.2026 evening; the nodes are written to the recommendation):**
- **F11. Who marks an item's stop kinds besides the role?** The Lead's decision names "the `surprise:` kinds the plan row or the role marked as
  stopping". (a) Slice 1: the role's per-call `--stop-on` only; the role reads the plan row's words and sets it; a plan-row field `walk_stop_on`
  (S3 strategist, carried by `prepare_request` into `request.json`, default for that item's calls) is added in Slice 2 by N8, which already
  owns `prepare_request` and the strategist's craft paragraph. (b) Add the plan-row field in Slice 1 (touches `planning_contract`, the
  strategist charter and `prepare_request` in Slice 1, and the strategist's role-load ratchet). **Recommendation (a):** the role has the plan
  row in its brief and judges per item anyway (P27); Slice 1 stays free of S3 changes; the field joins the S3 change already planned.
- **F12. A planned expectation as a stop: `read <selector> [mode] expect=<text>`?** The Lead's vocabulary list names "expect-read", but the
  recorder has no such word (F44) and the Lead's closed deviation list does not name it. (a) Add the optional `expect=` argument to `read`
  (compare the read value with the role's own text after collapsing whitespace; a different value is recorded in the step line and stops a
  walk call with reason `expect`; in a `ui` call it is only recorded); the expected text is the role's (from the requirement), the code
  compares bytes and never says who is right (AR-29, FR-58). (b) No new argument: a wrong value never stops the call; the role reads every
  `read` value in the answer after the call. **Recommendation (a):** without it a batch cannot stop where "the page does not behave as
  planned" unless the page also errs, so the role walks on blind exactly where the plain agent did (F45); cost: one argument, two tests, one
  data line. Error direction: equality after whitespace collapse may stop on a cosmetic difference (one more call), never misses a different
  value. In a one-step call it is merely a recorded comparison the role reads at once.
- **F13. Card 20 in the §7 set.** The owner withdrew card 20 after the plain-agent run («Невозможный на практике кейс», SUMMARY.md :70). (a)
  Walk 23 places; compare per item (the plain agent's per-card numbers include card 20, a small bias stated in the table). (b) Walk all 24 for an
  identical set. **Recommendation (a):** the owner's word; card 20 (five parallel adds) is not walkable by one walker anyway.

Small choices closed by the designer: walk id = dispatch id; loopback TCP + token; data rows `open_wait_s` 90, `idle_s` 900, `max_s` 5 400,
`answer_chars` 2 000, `parent_check_s` 5, `max_actors` 2; app card ≤ 8 000 B; names `walk_session.py`, `walk_timing.py`, `app_card.py`,
`walk_pool.py`, `walk_brief_lines` (not `walk_lines`, F32), `controller.walk_lanes`, `manual_capture.lane_key`; census labels `["conductor"]` by
the recorder convention; ONE raise site `_refuse` in the server; the fold fail > inconclusive > pass; control evidence `evidence/control-<label>.json`
(sibling of the diagnostic convention, F37); a fresh profile folder per open; `MANUAL_WINDOW_CASES` stays a constant (not a project fact);
`limit_by_role` as the mapped "only one account" field; `self_sign_up` `{page, request}` as the mapped sign-up field.
Step-call choices closed by the designer (05.11.2026 evening): `max_batch_steps` 20 (below `OBSERVE_MAX_STEPS` 40, so every step of a call is
observed; a smooth S6 item of the 24 cards needs ≈ 6–15 steps — **estimate** from their «Руками» lines); a call over the limit is REFUSED whole,
never cut (a cut would run steps the role planned as a whole); `batch_max_s` 100, checked between steps (below the host's default shell-call
limit of 120 s — **estimate, not verified** on this host; the answer file covers a call the host ended, E1.23); `batch_answer_chars` 4 000 and
`stop_look_chars` 1 500 (= `look.short_chars`); `--final` folded into a done call and `step` opening the item's attempt (one role call each
saved on a smooth item); one path for a call of one step and of many (no single-step special case); the stop is a call-back keyword on the ONE
`_run_steps` (no second step loop, AR-15); `status` as a number on a `status` surprise line rather than parsing the fact text (the text may be
replaced by the secret scan); the busy refusal through a threaded acceptor and ONE page executor (a single-threaded server would queue the second
call instead of refusing it); call answers kept under `state/walks/<W>/batches/` (N1a's own key, not N2's `work/walks/`); `--stop-on` grammar
`default | none | [+|-]<kind> | [+|-]status:<lo>-<hi>`.

---

## §7 Live proof (FR-33) on MyBooks LOCAL-1 — the 24 disputed places

Load: `D:/ws1/yml-text-factory\experiments\mybooks\add-to-cart-disputed-places.md` (24 cards, «Руками» steps). Run in a COPY of the stand
project (never the arm B tree while its driver runs). Walker model: **Sonnet 5.5** (owner, 18:48) — set the way the earlier arm runs set the
runner's model (the setting was not established by this designer; the Lead names it in the run notes). Card 20 per F13 (recommendation: not
walked). **This load is S6-like** — each card's steps were written in advance — so this proof and its plain-agent comparison speak for S6 manual
cases only; S7 controls and exploration are proved by the Slice 3 run with their own numbers (§3.10 (2), (3)).

**Slice 1 run — one walker.**
1. The Lead turns the 24 cards into manual-agent cases (Given/steps/Thens from «Руками»; expectation from «Ждали» with its source; a silent
   requirement -> `unresolved` Then + question, P20); each case names its account(s): MyBooks' recorded `admin` and `user` (`credentials_by_role`,
   F11) or guest; a case needing both names both (`--as` second actor). Card 21 per L1.
2. Run the S6 manual half. Lanes: by account set, ≤ 3 items each. The walker chooses its calls by the charter (N4): with the steps written in the
   case it normally sends each item as one batch; nobody tells it the plain agent's results.
3. Measure with `python -B ai-packages/qa-factory/scripts/walk_timing.py --task LOCAL-1 --summary --json` (in the copy): per item = the
   dispatch's wall (first `launched` row of `state/driver-runs.jsonl` -> the after-step's end line) ÷ its items, AND the role-session wall alone;
   cost = the LAST `total_cost_usd` per session ÷ items, AND cost by item index (1, 2, 3) from the transcript; tool calls per item; tokens per
   item in four parts and as the final context ÷ items; recorder calls and stops per item; the conductor's spend of the run printed SEPARATELY
   (P18); P18 second source: the same totals from `cost_capture`.
4. **The claim (≤ 7 min, ≤ $0.50 per item) is REFUSED** when the median item time or the median item cost exceeds it, OR when items 3+ of a
   dispatch exceed it (by wall share or by cost at that index). Then: `MANUAL_WINDOW_CASES` is lowered (3 -> 2, then 1) and the 24 are walked
   again; at 1 item per dispatch still over the limit -> the result goes to the Lead as a finding with the numbers (not argued).
5. **Comparison with the plain agent (F45) — valid for this S6-like load only** — written into
   `experiments/mybooks/thinking-roles/walker-vs-plain-agent.md` by the Lead, the walker's column from step 3, the plain agent's from SUMMARY.md
   :41-52 as measured (no recount):

   | per item (unless said) | plain agent, 3 lanes (SUMMARY.md) | walker, Slice 1 (1 walker) | walker, Slice 2 (3 walkers) |
   |---|---|---|---|
   | dispatch seconds per item | 136 s (3 275 s / 24; host counter) | measured: role-session wall ÷ items, and with the after-step; expected 140–170 s | measured, same two forms |
   | tool calls per item | 3.75 (90 / 24) | measured from the transcript; expected ≈ 6 | measured |
   | recorder calls per item | — (one script run per card) | measured; expected ≈ 1.7 (1 smooth, 2–4 stopped) | measured |
   | tokens per item | ≈ 20.7K (496 636 / 24, host `subagent_tokens`; quantity not established) | measured in four parts + final context ÷ items; compared only on the quantity the host counter is shown to count | measured |
   | dollars per item | not available (host gives tokens only, :50) | measured (`total_cost_usd`, cost by index); ≤ $0.50 | measured |
   | wall of the whole set | ≈ 21 min (three in parallel) | measured; expected ≈ 55–70 min | measured; expected ≈ 20–30 min |
   | who wrote the evidence | the agent's own scripts | the recorder, per step; quotes checked by code | same |
   | looked at the page between steps | no (script ran whole) | yes, at every stop | same |
   | outcome per card | SUMMARY.md :9-33 | the walker's verdicts; every card where the two disagree is listed for the Lead, with both evidences | same |

   The comparison is reported, not a gate (the gate is step 4). If the walker is more than 1.5× the plain agent's seconds per item, the report
   splits its time into model turns, browser steps, waits on missing elements and the after-step, so the Lead sees where it went. Per-item
   numbers are divided by the cards actually walked (F13); the plain agent's include card 20 — said in the table's note. The table's header
   says: "S6 manual cases with steps known in advance; not a measure of S7 controls or exploration".
6. FR-33 witness: case records under `work/evidence/manual/*/aN/` (each with start AND end probe), `work/walks/*/timing.jsonl`, `final` captures
   per pass, `surprise_detection` present, `state/walks/*/batches/*.json` with at least one `stopped` answer and the next call run from the same
   page, the S7 targets of observations; P0's number in §3.10.

**Slice 2 run — three walkers.**
1. **Before the run, the project's answer is recorded through the designed route** (the owner's word «На этом проекте можно самим создавать
   учётки» — the FIRST real answer to `s6.accounts_way`; the design is unchanged, the way is still asked once per project): the conductor opens the
   row (`project_decisions.py add --field-ref /manual/accounts_way/words --field-ref /manual/accounts_way/self_sign_up --essence "how this project
   gets more test accounts" --asked "<the s6.accounts_way text>" --owner person`), writes the owner's words verbatim to a file, and resolves it:
   `project_decisions.py resolve --id DD-<n> --words-file <that file> --resolution-ref "owner 05.11.2026" --field-values '{"/manual/accounts_way/words":
   "На этом проекте можно самим создавать учётки", "/manual/accounts_way/self_sign_up": {"page": "/register", "request": {"method": "POST", "url":
   "/api/register", "body": {"email": "{generated_username}@example.test", "password": "{generated_password}", "name": "{generated_username}"}}}}'`
   (route and body from MyBooks' source, F43; the email domain is the conductor's choice). Admin stays the ONE recorded account (`admin` of
   `credentials_by_role`); no admin is created.
2. Config of the copy: `manual.walkers: 3`; `manual.data_way` left `"not known"` ON PURPOSE, so the data question runs the holds-no-case road.
3. Run the 24: ordinary lanes beyond the recorded `user` start with an `obtain-account` item — the walker registers on `/register` with
   `fill-new-account` (N1c) and walks as `created:<name>`; admin lanes run in turn on the one admin.
4. Accept: wall of the 24 vs the Slice 1 run and vs the plain agent's ≈ 21 min (table of step 5 above, third column); per-item numbers as in
   Slice 1 step 4; no `s6.accounts_way` question asked (answered before the run); the `s6.data_way` question asked once, holding no case, its row
   resolved with the words whole; no case `left_unchecked` because of a question; created users named by `created_accounts_line` (MyBooks has no
   mapped delete); at least one pair of overlapping cards (1–4, 18, 19) run in parallel on distinct books, or alone with the reason as data. A
   sign-up refused by MyBooks (`EMAIL_TAKEN`, rate limit, F43) shows as N1c E1c.6, never as a product failure of a case.

**Slice 3 run.** At least one S7 control walk (card 3 «12» vs TF-011 «17»: the same keying from a start quantity of 1 vs 2); the explore walk on a
plan with `home: "explore"`. Measured per place with `walk_timing.py` (place `control`, place `explore`) against §3.10 (2) and (3); no
plain-agent comparison (no measured counterpart with steps unknown in advance).

---

## §8 What is deliberately NOT taken from the other factory

- Evidence in the runner's own words — our server writes and hashes it; the verdict cites it (P26).
- A runner verdict nobody above judges — ours goes to the analyst at S7 (P27, AR-29).
- Whole-value `fill` and no `surprise:` facts — the card 2/3 class of bugs hides from that.
- One case per subagent strictly in turn — we group by account set and (Slice 2) run lanes in parallel; the cap of 3 items per dispatch keeps the
  fresh-context benefit (F42).
- "Do NOT continue remaining steps after a failure" for the whole case — dependent Thens stop, independent Thens and the next items go on.
- A profile built partly from sources and used as a quasi-oracle — our app card is routes/data only and says so (FR-58).
- Credentials typed by the agent — our code types accounts (`fill-account`, `fill-new-account`); the role never sees values.
- Accounts assumed from the environment — ours are a project fact asked once and kept in the registry.
- Their exploration agent; ours walks plan-named cells. `qa-explore` (F20) is unrelated and untouched.
- Hooks cost (`cost_capture` at Stop 60 s, F1) is NOT in this spec — an analog for a separate row (AR-12).
- From the plain agent (F45): its speed technique IS taken where steps are known in advance (S6 cases) — all steps of an item in one go — but as
  DATA the recorder runs, never a script the agent writes; its blind run to the end is NOT taken — our call stops at the first deviation and the
  role looks; and where steps are found on the page (S7, exploration) we do not imitate it at all: one step, look, decide.

---

## Reading trail (revision, 05.11.2026)

Given: the draft (whole); the verdict t-1960 (whole); t-1955 spec (grep of names, owns, N3 :345-389); t-1937 spec (:1-8, :170-194, :283-311);
`thinking-roles.md` :131-152; the coordinator's message with the two owner's words (old versions not supported; MyBooks self sign-up).
Code (wt-fbfix): `story_run.py` :2787-2911, :3856-3955, :11455-11494, :12173-12252 (+ grep of `def` sites, `driver-runs.jsonl`); `manual_evidence.py`
:1367-1380, :1527-1558 (+ def grep); `manual_capture.py` :1-60, :724-762, :829-858, :2486-2515, :2945-2985 (+ def grep); `test_judgment_census.py`
:10-90, :185-264, :296-400; `judgment-census.json` (ratchet :4, rows :489-543, grep); `refusal_registry.py` (grep :57-58); `story_progress.py`
:380-409; `story_step.py` :1005-1046 (+ FORM_REL :297-298); `exit_gate.py` :783-838, :941-943 (+ grep); `stages.json` S6 :188-212;
`artifact-writers.json` :148-232; `brief_pack.py` def list, :2912-2935, :3300-3329; `project_decisions.py` :866-879 (+ grep); `cost_capture.py` def
list, :304-318, :1254-1283; `question-prices.json` (grep); `inject-map.json` :74-85; `role_load.py` (grep); `slow_tests.json` (grep); `stand_lease`
readers (grep over `scripts\*.py`); `phases/s6.md` (grep); `manual-capture-steps.json` (grep); test file globs. Stand (read only): arm B
`qa-factory/config.json` (grep :301-315, :532); `add-to-cart-disputed-places.md` (headings); MyBooks `src\lib\routes.ts` (grep), `src\app\api\register\route.ts`
(grep), `src\lib\validation\schemas.ts` (grep; `registerSchema` itself not read — the body fields come from `route.ts:21`).
Batch revision (05.11.2026 evening): this spec whole; `experiments/mybooks/disputed-check-plain-agent/SUMMARY.md` whole; `manual-capture-steps.json`
whole (Read); `manual_capture.py` :25-64, :1060-1169, :3196-3275, :3560-3699 (Read), and Grep for `def _run_steps|def parse_steps|OBSERVE_MAX_STEPS|
DEFAULT_TIMEOUT_S|ELEMENT_WAIT_S|_is_ours|_ours|surprise kinds|timeout`; `test_judgment_census.py:58-61` (Grep, `UNIT_NAME_RE`); the coordinator's
mid-task message carrying the owner's word of ≈21:20 (batches an option; per-place numbers; §7 comparison S6-like only).
Negatives with their positive controls: `S5Scheduler|s5_parallel|parallel_windows` over PKG empty — the same Grep found `MANUAL_WINDOW_CASES` in
PKG; the new test names absent from `slow_tests.json` — the same Grep found `test_brief_pack.py` etc.; `exit_gate.py` has no "manual" — the same
tool found `required_outputs_errors`. "No step word compares a read with an expected value" (F44, F12) rests on a Read of the WHOLE `steps`
object of `manual-capture-steps.json` (:7-23), not on a search.

Still not established (named, with who settles it): the config setting of the walker's model for §7 (Lead); whether `finalize_task.py` writes
`run-report.json` with zero blocks (N5s E5s.3 covers both worlds); the transcript locator `walk_timing.py` uses for a `claude -p` session (N2 names
the `cost_capture` function it reuses); the field a prepared request uses for a device (`app`) surface — the walker serves the browser only, so
N5s keeps such a case on today's road once the builder names the field; the `--resolution-ref` form existing callers use (N8; §7 uses a plain
label); the exact `registerSchema` limits of MyBooks (name/password rules) — the walker reads the page's refusal if the generated values miss them;
WHICH quantity the host's `subagent_tokens` counts for the plain agent (F45; the Lead settles it from the host's documentation or one control
dispatch before the token row of §7 step 5 is compared); the host's per-shell-call time limit on this machine (`batch_max_s` 100 assumes 120 s);
the per-step time of today's recorder with the detector (P0 (c) measures it); every number of §3.10 (2) and (3) — no S7 control or exploration
walk has a measured counterpart, the Slice 3 run measures them.

Needed beyond the manifest: `exit_gate.py`, `stages.json`, `artifact-writers.json`, `refusal_registry.py`, `cost_capture.py`, `story_progress.py`,
`story_step.py`, `role_load.py`, `slow_tests.json`, `inject-map.json`, `question-prices.json`, `execution_scheduler.py` (grep); MyBooks sign-up
source (for the owner's word 2); for the batch revision: `manual_capture.py` beyond the two files given (`_run_steps`, `_candidates`,
`_surprises_after`, `Attempt.surprise`, constants) and `test_judgment_census.py` (`UNIT_NAME_RE`).
Analogs noticed, not widened: `cost_capture.py` at Stop 60.5 s per session (F1); the analyst reading application sources (F17) — N6 removes its
tool lines, not the craft; `project_decisions.FINDING_SCOPES` is closed variety in code, a recorded FR-13 debt (`:39`); the `ui` road's
summary carries every step's excerpt (≤ 8 000 chars) while a step call's answer carries only the last and the stopped one — a role on the
fallback road pays more context per step (not changed here); the analyst's charter (N6, Slice 3) will need the same step-call paragraph or a
pointer to `walk-charter.md` — N6's owns name `qa-failure-analyst.md` already, the Lead decides at Slice 3.
