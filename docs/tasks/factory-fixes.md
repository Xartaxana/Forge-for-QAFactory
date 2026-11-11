# Factory fixes after cmp1 — task graph (30.09, owner: launch independent tasks in parallel)

Carrier of the work that follows the development-system fixes. A node's status moves in the same turn
as its journal event. Specs: `docs/tasks/specs/`. Drafts t-109, t-113, t-114 are the designers' texts
copied verbatim; THIS file holds Lead's decisions on their forks — where a draft says "fork", the
table below is the decision. Owner-level forks are marked OWNER and carry the interim choice.

## Specs

| backlog | spec | drafted | critic-on-plan | state |
|---|---|---|---|---|
| B-194 | `specs/t-108-expectation-change-after-red.md` | t-108 | t-115 accept with changes (written in) | building |
| B-196, B-199, B-195, B-197 | `specs/t-111-dashboard-driver-binding.md` | t-111 | t-118 running | waits for critic |
| B-193 | `specs/t-110-automator-friction.md` | t-110 | t-119 running | waits for critic |
| B-211 (B-207, B-208, B-206, B-209, B-210, B-212, B-213) | `specs/t-109-report-truth.md` | t-109 | t-120 | waits for critic |
| B-216, B-190(d), B-181 | `specs/t-113-open-questions.md` | t-113 | t-121 | waits for critic |
| B-172 (and B-174's root) | `specs/t-114-s1-gap-points.md` | t-114 | t-122 | waits for critic |

## Builder nodes

| node | piece | owns (under `ai-packages/qa-factory/`) | status |
|---|---|---|---|
| t-116 | B-194 A | `scripts/run_suite.py`, `scripts/tests/test_run_block_producer.py` | handed over 16:42, witness 39/39 rerun by Lead; acceptance with the critic pass of piece B |
| t-117 | B-194 B | `scripts/s5_precheck.py`, `scripts/manifest_put.py`, `handoffs/vocabulary.yaml`, `design/state-exits.md`, `references/judge.md`, `references/judgments.d/code.json`, `scripts/tests/test_s5_precheck.py`, `scripts/tests/test_state_exits.py` | in flight |
| — | B-194 C, D, E, F | per spec section 6 | after B |
| — | B-194 G (ledger words) | HELD: see "Cross-spec decisions" 1 | — |
| t-123 | dashboard P0 | `scripts/driver_journal.py`, `scripts/tests/test_driver_journal.py` | accepted 17:05 on critic (accept with changes) |
| t-130 | dashboard P0 follow-up | same two files | in flight |
| t-124 | dashboard P1 | `scripts/factory_dashboard.py`, `scripts/dashboard_cost_groups.py`, `scripts/metric_signals.py`, `design/metric-signal-policy.md`, `scripts/tests/test_dashboard_task_binding.py` | in flight |
| t-125 | dashboard P3 | `scripts/retro_numbers.py`, `scripts/tests/test_retro_orchestrator_driver.py` | in flight |
| — | dashboard P2, P4, P5 | per spec | after P1 |
| t-126 | B-193 P1 | `scripts/launch_check.py`, `references/launch-causes.json`, `scripts/tests/test_launch_check.py`, `skills/qa-onboarding/phases/p4-generate.md` | in flight |
| t-127 | B-193 P2 | `scripts/execution_request.py`, `scripts/tests/test_run_suite_mine.py` | in flight |
| t-128 | B-193 P5 | `scripts/guard_pre_tool.py`, `scripts/tests/test_guard_write_owners.py` | in flight |
| t-129 | B-193 P6 | `scripts/story_step.py`, `scripts/tests/test_story_step.py` | in flight |
| — | B-193 P3, P4, P7–P11 | per spec section 4 | after their predecessors |
| t-131 | open questions A1 | `scripts/question_register.py`, `references/question-vocabulary.json`, `scripts/tests/test_question_register.py` | handed over 17:39 (251/251); critic running |
| — | open questions A0 (B-224), A2–A6, B1–B3 | per draft + overrides | A0 needs its own spec |
| t-132 | B-172 P1 | `scripts/source_inventory.py`, `scripts/ticket_adapter.py`, `scripts/tests/test_gap_points.py` | in flight |
| — | B-172 P2–P6 | per draft + overrides | after P1 |
| t-133 | report P4 | `scripts/bug_records.py`, `scripts/tests/test_bug_records.py` | in flight |
| t-134 | report P5+P6 redraft (designer) | — | in flight |
| — | report P1, P2, P7–P10 | per draft + overrides | P1 after B-194 B; P2 after P1 |

### State at 18:12 (30.09) — what is running, what waits for Lead

Running (results arrive as notifications; each must be accepted with a journal event):

| task | what | note |
|---|---|---|
| t-117 + t-116 (critic) | B-194 pieces B and A, one verdict | piece B handed over 17:40, 290/290; report `specs/t-108-piece-B-report.md` |
| t-140, t-141, t-142, t-143 (builders) | B-194 pieces C, D, E, F | built against piece B's shapes while its critic runs |
| t-124 (critic) | dashboard P1 binding | handed over 17:56; asked to render cmp1 read-only |
| t-138 (builder) | retro share follow-up | one source per ratio, root rule, control layer = conductor, resumed roles as role spend |
| t-135 (builder) | launch check follow-up | collect forms as data, doors by audience |
| t-127 (builder) | B-193 P2 precedent | in flight since 17:00 |
| t-131 + t-128 (critic) | question register A1 and the config guard P5 | deciding question for the guard: can it tell a driver-launched role from the main session |
| t-132 (critic) | B-172 P1 gap points | handed over 18:08, 185/185; NO caller passes `s1_closed` yet — must not merge alone |
| t-144, t-145 (builders) | B-207 P5-A (S0 base) and P5-C (predicate) | spec `specs/t-134-proof-by-code.md` + V1–V8 above |
| t-146 (critic) | plan of the true price (spec `specs/t-137-task-price.md`) | Q1 (`cost_capture.py` rate order + re-price at read) and Q7 (`config_contract.py` question) start after it |

Accepted and done: t-123 + t-130 (journal reader), t-126 (launch check, follow-up t-135 open), t-125
(retro share, follow-up t-138 open), t-133 + t-139 (bug reader), t-129 (config change detector).

Waiting for Lead after the verdicts: dashboard P2, P4, P5 (after t-124 and with the true-price
pieces Q5); B-193 P3, P4, P7–P11; open questions A0 (B-224, needs a spec), A2–A6, B1–B3 and the
onboarding question about thresholds; B-172 P2–P6 and the `s1_closed` callers; report P1, P2, P7–P10;
B-207 P5-B, P5-D, P5-E, P5-F, P5-G, P6-A, P6-B, P6-C; B-194 piece G (held).

At integration (Lead): `audit_factory.py` `CLI_SCRIPTS` lines for `launch_check`, `question_register`
(and later `test_repo_base`, `probe_debt`); `refusal_registry.py` entry `PT-config-write` (text in
the t-128 hand-over: `test_refusal_registry.py` is 112/115 until then); `references/artifact-writers.json`
entries; `design/state-exits.md` rows (question statuses, `gap_acceptance.accepted_points[]`,
`human_review`, the B-207 states); `contract_slices.py --write` once; the debt lines; FR-24 / FR-25
wording and the bug-home sentence of FR-37 in `design/factory-rules.md` (mechanism commit, index
regenerated); CHANGELOG; the small slip `request ={` in `run_suite.py`; then the full `selftest.py`
and `install_smoke.py` once per topic, and commits by topic. NOTHING of today's package work is
committed yet.

## State at 13:20 (02.10) — the morning: stop, fix, redesign; READ THIS FIRST, then 06:55

**Owner's words since 06:55 (all in force):** 10:24 «Останавливаем и чиним все проблемы. Надо было чинить
баги, которые в любом случае надо чинить до прогона или до релиза, а не просто останавливаться» (gate B of the
rehearsal closed by that word; P8 — nothing filed). 10:50 the Forge analysis: «проанализируй все фиксы и
проблемы с момента прогона с yaml, выдели места, которые часто ломались — архитектурно неверные; раздели
фабрику на фичи, собирай метрики по фичам (баги по фичам, переделки, фиксы, породившие проблемы); дашборд;
ходы по этапам/фичам». 11:05 (reply 2) stand build identity is **a question, not a blocker**; a registry of
stands × builds × methods (one file for all stands, copied by a new teammate), answers «вот как определить /
я проверил на этой задаче / на этом стенде всегда подтверждаю сам»; «OCI label at build — сделай сам, пусть
метод будет записан». 11:40 `mismatched` is ALSO a message to the person (redeploy / test what is there /
stop). 11:45 «имеет ли смысл прогонять фабрику, которую переделаем? Сначала эксперимент с мануальным тестом
(UI-свидетельства до/после), потом большая переделка, потом полный прогон» → the plan is manual experiment →
redesign → full run; «дизайнеров переделки запускай уже». 12:00 Forge metrics must be collected by any clone
by itself; the parallel Codex-integration developer = a new feature; «проверять при мерже ветки»; CI only on
GitLab (checked: project 100001, Owner, jobs enabled, shared runners; the first pipeline `#7860114` forge-check
**Passed** 22 s). 12:50 answers: t-303 Q14 scrub secrets; t-305 Q10 a null stage IS deliverable (the report
keeps all sections, «осталось вам»); t-305 Q14 an empty plan = a halt for the person's word, re-shown on
resume with the «did the story change» check. 12:55 the retro keeps three jobs (numbers; «что хорошо / что
плохо» → factory-backlog finding, dashboard until fixed, upstream to the Forge; promotion of per-story answers
to standing). 13:05 **ONE runtime** — «код тестовых прогонов и реальной работы не должен отличаться;
оркестратора нет — есть дирижёр и драйвер» (B-261; the skill `qa-story` becomes entry + conductor over the
driver; roles stay `claude -p`; progress visibility via the driver log/dashboard — «добавляй», t-310). 13:15
«Ты говорил нужно запустить критика батча и критиков на план» → six critics launched. Name of our system:
**Forge** proposed (Factory Forge); not yet confirmed by the owner.

**Measured this morning:** the login race — `experiments/cmp2-15045/rehearsal/11-login-probe.txt` (the night's
B-252 wording was wrong: the route exists; `login()` returns on `networkidle` before the landing; `environment.access`
is unrelated); `strategy/faq.md` is 66 bytes (empty) on all three live copies — the retro's prose fold never fired;
the headless driver has NO ticket re-read on resume (B-259; the skill phase s0.md has it) — two heads (B-261);
`tools/test_hook_liveness_probe.py` 3 tests red only in the full `pytest tools/` run, green alone (flaky, tools-side);
GitLab: user 21089, `can_create_group: false`, `can_create_project: true`, project 100001 Owner.

**Committed:** `6ba43b6` (pushed to origin/main, CI green) — the Forge batch ONLY: plans/features.json F01–F21,
tools/forge_metrics.py (+43 tests), journal `feature` WARN, `.gitattributes` union merge, `.githooks/pre-merge-commit`
+ the pre-commit WARN tail, wiring_check three hooks, `.gitlab-ci.yml` forge-check, the fragility data + reading,
specs t-292/t-293/t-294/t-300/t-301..t-306/t-310 (+ designer drafts verbatim under specs/drafts/), backlog
B-255..B-262, SIBLING_MAP login row, journal t-292..t-311. **NOT committed (package, working tree):** t-297+t-308
(login landing + stand_login question), t-298 (reinstall: hook_written, asked_until_answered, portable_checkout),
t-299+t-309 (S7 null_outcome, scope words, conductor door, window B′, one `triage_targets`), the Lead's integration
edits (qa-runner.md Q13 sentence, scope words in ticket_adapter/SKILL.md, `--ignore-handoff` framing ×5, conductor
`stop` clause, SKILL.md trimmed to 19000), compose `docker-compose.yaml` label (owner's stand, done, image rebuilt
sha256:bd65792b…). Quick canon at 13:20: `selftest --limits --lang --slices` 4/4, audit 95/95; the full selftest and
install_smoke NOT yet run on this tree.

**Alive now (accept in a batch):** builders **t-310** (story_progress line, spec t-310) and **t-311** (check_delivery
reads triage by `triage_targets`); critics **t-312** (batch t-298/t-299/t-308/t-309), **t-313** (plan R-2+t-300),
**t-314** (plan R-1 + the phases→driver inventory), **t-315** (plan R-3 + the live measurement), **t-316** (plan
R-4 + X1), **t-317** (plan R-6). Next free id **t-318**. Every new journal event carries `feature`.

**Open with the owner:** the name (Forge?); t-302 Q10 (my proposal: unknown novelty = new → `rerun`, no debt,
no question — pending her objection); B-244, F7 of t-227 (old); push of the package batch (after the critics).

**Next, in order:** (1) accept t-310/t-311 (+ a second critic pass over them with t-312's method), apply t-312's
blocking findings, Lead integration (CHANGELOG lines from t-297/t-298/t-299/t-308/t-309/t-310 reports in the
scratchpad, UPGRADE cost-of-answering note, BACKLOG closures B-250/B-252/B-253(а,б,в,з)/B-257 partly, SIBLING_MAP
rows: reinstall, stand_login twin, forge_metrics axis 6, RUNBOOK: CI + the label method), full selftest +
install_smoke once, the package commit with the mechanism block + `tier: fable`, push; (2) **the manual
experiment**: a new copy by the rehearsal's procedure (worktree + cmp2's state before S6), one S6 manual block on
TC_005/007/009 with before/after screenshots → S7 → S8 → the report for the owner; the registry row for our stand
is written by the first non-rehearsal probe only after t-300 N1 — for the experiment the manual half still
proceeds on the image digest (t-279), fine; (3) the critic-on-plan verdicts → edits to t-301..t-305/t-300; the
owner's two open answers; (4) the redesign: R-2 (t-300 N1 first) → R-1 → R-3 → R-4 → R-6 → R-5 → R-7, each node
with its own dispatch spec; (5) the full comparative run on the new factory.

**Rules learned today (keep):** mutation probes only on a scratch copy; a designer brief's `given` anchors go
stale within hours on a hot file — map by function name; the dispatch_gate needs header lines `given/owns/
non-goals/handoff/edges/DoD`; `glab` cannot read the owner's keyring from my process (401) — her terminal can;
no ` 2>&1` ever; the journal ids go in dispatch order (t-311 before t-310 was an echo WARN, no collision).

## State at 06:55 (02.10) — the night: critic fixes, the live rehearsal, the 13797 check; then 22:55

Owner's words since 22:55 (all in force): 23:4x «проверь S0–S1 на TP1-13797 и сравни с прошлыми
прогонами, все ли источники собраны (MRы прецедентов в комментариях)»; «Докер уже нужен?» → no for S0–S1;
23:50 **«(а) оставляем D-06 как есть, но проверяем, что никакие источники не теряем»** (after Lead's
confession F-cmp2-30: the 15045 cmp2 snapshot was LEAD's own paste, not the agent's — B-236/D-06/FR-50
re-grounded); ~23:55 «Я подняла докер, доделывай тесты, потом репетицию, потом 13797. Утром посмотрю
отчёт по кейсам и по 13797». Both reports exist: `experiments/cmp2-15045/rehearsal.md` (the morning
section "Итог для владельца") and `experiments/measurers/answers-13797.md` (the last section).

Journal: next free id **t-292**. No agent alive. Accepted tonight: t-280 (critic), t-281, t-282, t-283
(scout), t-284 (integration batch), t-285 (critic over t-281/t-282), t-286, t-287, t-288, t-289, t-290,
t-279, t-291 (the full-selftest reds + the `shown=` line). One `dispatch_skipped` (designer).

**COMMITTED 07:45 (02.10):** records `26ad691`, the whole package `4116add` (372 files, one mechanism
block naming six mechanisms + `tier: fable`; the `config_merge` pair deleted), journal `9d978db`.
Canon after the commit: `install_smoke` PASSED (07:26), full `selftest.py` **301/301** (07:44). The
working tree is clean except hook state (`.claude/critic_snapshot.json`, `.claude/dod_track/`,
`logs/.search-ledger/`, `logs/owns_registry.jsonl`) and a stray `qa-factory/state/cost/.writers/` at
the repo root from 30.09 (cwd-relative writer; B-249; never deleted by a session). The "Next (Lead)"
list below is reduced to: the owner's morning answers → B-252 (the login route for the manual UI
capture) → a critic pass over t-279's gate flips + t-287's class → the fresh run on 15045.

Lead-tier edits done by Lead: FR-50 reworded for D-06 (an agent is never a read route; the Why now tells
the true 15045 story), NEW **FR-58 "Code is never an oracle"** (P20, section D), debt rows FR-13/FR-50,
P5 in PROJECT.md with the D-06 clause, FACTORY_RULES_INDEX regenerated (58 rules), `contract_slices
--write` (0 stale), audit 95/95.

**The live rehearsal** (copy `testproject1-sdk-cmp2r` = worktree 9a6a1a79 + cmp2's qa-factory + its 6 S5 test
files; Docker up): reinstall-equals-fresh proven live through the onboarding role headless (4 legs,
$2.10; records moved sha-equal, `git rm --cached` lines run, check-ignore both ways); probes registered
with tokens (api `matched`; uitest e2e-ui `image:sha256:728da536…` honest unknown + remedy); gate A
re-recorded (`rehearsal/regate_a.py`) → OB-5/7/9/12 executable by hand; S5 closed on the person's word
(`critic_unverified.py`); S6: automation runner, then the manual block of 4 → **TC_012 (api) pass with
before/now; TC_005/007/009 (ui) inconclusive — the capture hit the sign-in page** (B-252, the main
finding: `manual_capture ui` has no login route; `environment.access` empty after re-onboard); S7 triage:
2 APP_BUG exactly the P20 pair (R-17 details shape; R-19 400 vs 403 "both readings tenable"); S8 report
with "Checked by hand — 4 of 13" + "Left with you"; **the story stands at gate B waiting for the owner**
(bugs by number, 3 stand gaps). Thirteen package defects caught live: 7 fixed tonight (A24 row t-286;
own-session locks t-288; prepare without execution_kind t-289; the S6 half-stage exit gate t-290 incl.
the manual-block scope; …), the rest queued **B-250…B-253** + B-246…B-249 (see `rehearsal.md` list).
Cost ≈ $6.6, the manual block itself $0.90.

**The 13797 check** (copy `testproject1-sdk-s01-13797`, S0–S1 only, stopped at the S2 dispatch — its role
process was killed; S2 is `running` in that copy's state, ignore): nothing lost vs judge-off/judge-on/cmp1
(4 tickets, 8 comments, 1 attachment, 6 media, MR 4243 with diff) and MORE read (3 of the 4 precedent
MRs of 8384 via local git — every earlier run had all 4 as an accepted gap); the owner's "MRs in
comments" live in 8384's text, not in 13797's comments; S0 by REST in seconds, 0 LLM. One role-framing
difference (`cm.requirement_sources` 2 vs 4–5: only read sources listed) — not a data loss. B-line: MR
rows in `ticket-references.json` stay `not_fetched` after S1.

**Open for the owner (morning):** (1) gate B of the rehearsal — bug 1 / bug 2 "file or not a bug",
the 3 stand gaps (a/b/c/d), or just "stop" (P8: nothing is filed anyway); (2) the login route for the
manual UI capture (B-252) — her call on how the capture logs in (the harness's keycloak helper with
`environment.access`, values never read by a role); (3) the two `Dockerfile.test` lines for uitest
(the probe printed the exact remedy); (4) the stand for the fresh run; (5) F7 of t-227; (6) B-244.

**Next (Lead):** the full `selftest.py` (running at 06:55) + `install_smoke.py`; the topic commits of the
package (mechanism gate: axis blocks + `tier: fable`; `git rm` config_merge pair is staged by the
deletion); the `shown=` line in `record_by_code` (t-279 Q3, one line, story_run free now); a critic pass
over t-279 gates + t-287 class before the fresh run; B-252 before the fresh run's S6; then the fresh run
on 15045 (date gate OK from today) with the post-run keys (K2/K16 via `stage_compare s0 --story
TP1-15045 --driver-run`, the roles' input tokens, B-235…B-240 closure).

Hygiene slips tonight (recorded in the journal): Lead — one heredoc append to `rehearsal.md` and one
`cat >>` append to `answers-13797.md` (Edit anchor misses, content verified); builders — t-287 restored
`story_run.py` from a byte copy 4× and wiped t-289's edit twice (re-applied, verified); one `sed` (t-279);
three `cd` in read-only calls. Rule for the next specs: mutation probes only on a scratch copy of the
package, never the live file (builder-rules addendum queued).

## State at 22:55 (01.10) — delta over 18:40; then 18:40, then 17:35

Owner's words since 18:40 (all in force): Docker is STOPPED (owner's RAM; restart only before the
rehearsal: `docker compose up -d testproject1` + `--profile uitest up -d --no-deps testproject1-ui-static`);
the KB PAT lives in the user-level env var `KB_PAT` (read from the registry by code, never printed);
19:10 «проверяй. Обнови страницу Architecture» → DONE: `tools/kb_publish.py push kb/02-architecture.xhtml
--yes --force` → page 2944344247 v7→v8, verify green (B-243 proven live); **D-06 (19:35): the Jira
agent is NOT a data source** — ticket/links/comments/attachments by the API in a light form,
repositories by API/git, the agent only for writes where the project does that; 19:50 both typed
fields AND text mentions, the junk share dropped explicitly; 19:55 the factory runs on ANY project —
no hard-coded key, nothing lost at the entrance; 20:00 per-prefix probes, never per-key GETs (a
request storm happened before); 20:05 a 403/404 may be a lost login — tell it apart by code;
B-236 corrected: the 15045 snapshot came from the Jira AGENT's markdown (`provenance source: file`
misled; «я точно ничего не вставляла»), REST had all 15 AC under "What needs to be tested".

Journal: next free id **t-281**. ALIVE: **t-279** (wave 3: `not_applicable:no_changed_file`, the
gate_preflight INFO→factory_fixable flip + 8 assertions, the honest image-digest identity on uitest,
planning_contract F4/F5/F6/POLICIES import, vocabulary.yaml — judging file `test_gate_preflight.py`),
**t-280** (critic, one pass over t-273/t-276/t-278 — the t-267 topic; expect findings on
`RETRY_AT_RE`, `TableError` exit 3 as a person question, the private helper, the title-less paste).
Accept by witness (control-rerun the judging file, `by: fable`); the critic by trail; its fixes →
one follow-up builder (t-281+).

Accepted since 18:40: t-253, t-255, t-256, t-257/258/259 (DMtools scouts), t-260, t-261, t-262/t-266
(kb_publish + fixes), t-263, t-264, t-265 (critic), t-267 (designer), t-268/t-269/t-270 (critics),
t-271, t-272, t-273, t-274, t-275 (critic, BLOCKER now fixed in t-271), t-276, t-277, t-278.
Specs updated with critic sections + Lead decisions: t-232 §0e, t-227 §0e, t-250 §0d, t-267 (new:
§0 + §0c). Research: `docs/research/dmtools/` (3 files), `docs/RELATED_WORK.md` (new), backlog
B-235…B-245 + D-06; `experiments/measurers/jira_light_check.py` + `stage_compare s0 --story` (STOP
today by design: the light snapshot exists only after the fresh run).

Owner decisions OPEN: (1) the stand for the UI half of the manual rehearsal — (a) dev stand / (b) wait
for her two `Dockerfile.test` lines / (c) Lead's recommendation: the image-digest identity (t-279
builds it; manual capture proceeds on `unknown+image`, automation keeps `env_blocked`); (2) F7 of
t-227 (a gap does not hold delivery_ready — the default in code); (3) B-244 (CI launch) — she asked
what it gives; Lead answered "nothing now"; drop it if she says so.

After t-279/t-280: the t-267 fix follow-up; then INTEGRATION (Lead): `contract_slices.py --write`
(9 stale), A22 doc-scribe 833 B (trim `common-rules.md`), `tools/controller-blocks-gen.py` ROOT
repoint + regenerate, `git rm config_merge.py` + test, CLI_SCRIPTS, the config template keys
(`direct_api.custom_fields/acceptance_headings`, `adapters.ticket.attachments`, `journal_path`
records/ spelling, `runtime_probes` tokens), FR-50 + P5 wording (reads: API → person; mechanism
commit with axes + `tier: fable`), the P20 FR line + FR-13 debt lines (`ledger.EXPECTATION_UNCONFIRMED`
→ now contract; `NOT_TRACKER_PREFIXES` moved to data), UPGRADE/CHANGELOG (the version line fires only
from this version on; reinstall = fresh; REST-only reads), RUNBOOK §3 table titles + :224 old-path
line, dashboard golden sections 13/20 (formula v2 — re-cut), `host_probe.py:415` KeyError, the
check_coverage-REJECT-before-retire order bug (B-line), the stray cwd-relative writes
`test-harness/state/` (scout question), the VCS/MR auth twin (B-line), `prepare_copy` + the live
reinstall proof checklist (t-232 §0e, a worktree copy), `selftest.py` + `install_smoke.py` full,
commits by topic (reinstall / P20 / manual / REST / kb_publish / records). Then the rehearsal
(t-250 §0d sequence: block = TC_005/007/009/012, automation runner first) and the fresh run on or
after 02.10 (the P20 date gate counts by day — F1 of t-269).

## State at 18:40 (01.10) — delta over 17:35; then 17:35

Owner 17:57: a new FUTURE task — study the DMtools lecture (VTT in Downloads) + IstiN repos, write
backlog plans for the build system (KB publication slow/dear) and the factory (Jira payload noise),
nothing slower or dearer. DONE: scouts t-257 (lecture digest), t-258 (repo map; connector code is in the
submodule `dmtools-cli`; GitHub API 403 — trees not obtained), t-259 (our Jira baseline on the cmp2 copy:
`fields=*all`, ~75 % custom-field junk, snapshot ≠ REST read, agent cost unattributed) — all accepted by
trail with Lead spot-checks; Lead's second pass in `docs/RELATED_WORK.md` (new; 4 raw files + the
ticket.json measurement; rejected items with reasons); backlog rows **B-235…B-245** in `plans/BACKLOG.md`
section 7 (B-243 KB-by-REST starts with ONE experiment the owner runs herself: a PAT + one curl; I never
enter her credentials). Nothing of this is code; no dispatch owed except on the owner's word.

Builders: t-253 (B6 two folders) accepted 18:13 — forks decided: tracker-write.json → `records/` (task
data), template `journal_path` → records/ spelling + value migration on the exact old default only,
dashboard golden re-cut → all three to **t-260** (B4, alive: fixture + `test_reinstall_equals_fresh.py`
K1–K14/K7 + one install_smoke step; path slip corrected by message: the template is
`references/templates/config.json`). t-256 (P20 fixes O1–O12) accepted 18:19 (deviations D1–D7 accepted).
**t-261 alive** = t-250 B1 (gate A manual pass, `manual-policy-by-level.json`, S6 blocks of 5 with resume,
gate_text slot guarded) + the story_run fix wave (t-217 §0d O1/O2/K11, t-218 §0f repair row flip +
`resolve_argv`) + the integration lines from t-253/t-256 (gate_preflight:1228 readiness path,
story_run:4602 `configured()`, :3956 `--apply-fixes` on `raise`, :1785 case tokens, `plan_created` at
gate_preflight:1184/1202 + stage_done:360/371). **t-255 still alive** (readers + automator/critic texts
+ rubric; `test_s5_precheck` F-cj reads its rubric). Next free id **t-262**.

After t-255: t-250 B3 (`manual-checks` report block; owns report_facts/grammar/ledger render/test-report
template/doc-scribe/s8). After t-260: nothing of t-232 but the texts batch (stale old-path texts listed
in the t-253 acceptance notes) and B5 is done (t-241). Critics, one pass each: B3+B6+B4 (t-248/t-253/
t-260); t-255+t-256 (P20); t-252+t-261 (manual + story_run); wave 2+3 of t-218. Then the uitest
built-bundle probe builder, the §2-of-t-217 builder, the rehearsal (t-250 §7), the fresh run.
Integration list of 17:35 unchanged, plus: `contract_slices.py --write` (9 stale now), A22 doc-scribe
still 8 B under the floor after `--write` (trim `common-rules.md`), `story_run.py:3956` is in t-261.

## State at 17:35 (01.10) — the fix wave before the fresh run, three builders alive; then 11:45

Owner's words since 11:45 (all in force): «Прогон больше не возобновляй» (10:25); P20; «ответы на вопросы
гейта A … починить до прогона» (11:50, DONE in code by t-246 + fixes t-256); 12:35 reinstall over an old
installation must equal a fresh install (spec t-232, B-233); 14:00 task data stays, the factory's
technical data is deleted, undetermined → `state/retired/<date>/`; `docs/superpowers/` is NOT ours
(the team's dev factory) — never touched, never a "generation"; THE MAIN PROBLEM = version drift (cache
0.7.9 / marketplace 0.7.19 / readiness 0.7.4) — now printed by code at SessionStart (t-248); 14:10
two folders (`records/` tracked, `state/` ignored) — B6 t-253; B-234 onboarding ingests existing project
rules only after the person's confirmation; 15:40 the manual-agent rehearsal = YES, two cases of
different evidence types (TC_007 ui + TC_012 api via the manual word), on the fast `uitest` build; the
owner switched the stand to `uitest` at 16:42 (checked: 5173 → 200 nginx, /api/v1/user → 401, sign-in
page load 2.2 s / 7 resources; the dev `testproject1-ui-1` container is stopped on purpose); the owner
interrupted a read of the harness `.env` test account — do NOT log in by hand, the rehearsal logs in by
code; the two `Dockerfile.test` lines for a build sha (t-250 §0c) are the owner's call, unanswered.

**Journal: next free id t-257.** Agents alive at the compact (accept each by its witness: control-rerun
the ONE judging file, journal `accepted` with `by: fable`):
- **t-253** (builder, B6 of t-232): `records/` vs `state/`, one path module, literal rewrite (the ten
  files held by other builders reported for the integrator), old→new table rows + `retired/**` row,
  gitignore from the table, the move on reinstall before retire, + B3 follow-ups (session_env version
  line call, `--fold` writer, memory merge, two wordings). Judging file `test_two_folders.py`. Then B4
  (compare_trees + the old-generation fixture; K5/K6 extras per §0d) and ONE critic for B3+B6+B4.
- **t-255** (builder, t-227c): the readers (traceability `wait`, ledger `not_verified:expectation_unconfirmed`
  before passed_green, check_delivery non-blocking F7, coverage_contract C3 person-debt, report_facts
  "Left with you", manifest_from_tests reasons + question/observed, stage_guard one source) + automator/
  critic/rubric/vocabularies texts. Judging: test_ledger.py / test_traceability_report.py. Then t-250 B3
  (the `manual-checks` report block; owns report_facts/grammar/ledger render/template/scribe/s8) and
  ONE critic for t-247 + t-255 texts.
- **t-256** (builder, t-227 §0d O1–O12): P20 leaks after an answer (confirmed only on reading `a`), the
  before/now on the gate card, `raise_questions` + the S4-exit raise, the S2-exit register re-check,
  the whole-line `<case>: accept as blocked` token + the cards printing it + partitions + remedy from
  precondition items, md/json re-render of every mapped column, F22 presence checks, date-gated
  missing_branch. Judging: test_question_branches.py. Then t-250 B1 (the gate A pass making manual
  obligations executable with C1/C2 refusals; S6 blocks of 5, only the last completes, C4; gate text)
  and ONE critic for t-252 B2 + B1.

**Then, in order (each with disjoint owns):** the story_run fix builder (t-217 §0d O1 handoff saves
again/third, O2 legacy filing kinds, K11 test 1→2 + pin; the t-218 §3 repair row flip: `_probe_derived`
→ FACTORY_FIXABLE, `GATE_REPAIRS` row, `CHECK_WORDS`, `resolve_argv` before executing the INFO argv) —
after t-256 (planning_contract) is in; wave 3 of t-218 §0f (reason-coded `not_applicable:no_changed_file`
through validate_request / probe_runtime / the four local_source gates) — after t-255 (coverage_contract)
and t-252 (manual_evidence); the uitest built-bundle probe (reads `/usr/share/nginx/html/build-sha.txt`,
absent → `unknown` with the two-line remedy) — after wave 3; the §2-of-t-217 builder (a person's word on
a named block → waiver by code, `go on`/`retry`/`stop`, controller `_passed_by_person`); the rehearsal
(t-250 §7: a fresh `prepare_copy` of cmp2, S5 closed through the new blocked-window record = live proof
of t-219, gate A re-recorded with cmp2-s4-gate-a.md in the TOKEN form, S6 on TC_007 + TC_012, TC_015 as
the free negative) — after B1/B3 and the critics.

**Integration (Lead, before the fresh run):** A22 is RED (floor 1,000 B; doc-scribe 835, case-critic
952, strategist 1,008; A25 qa-automator 933) → the `common-rules.md` lever or trims; `contract_slices.py
--write` ONCE after every text builder; `tools/controller-blocks-gen.py`: repoint ROOT from the old
`QAFactory-driver` checkout to this repo, add the COMMAND entry "this window holds instances
the stand blocked", regenerate (counts 188→189, command 108→109; design/README.md by hand);
`audit_factory.CLI_SCRIPTS` (`install_paths` and `onboard_apply` already registered by Lead; optional
`manual_capture`); `git rm scripts/config_merge.py scripts/tests/test_config_merge.py`; the FR-12 debt
line for `account_keys`; config template keys from t-224 (`measured.e2e_page_load_s`, `page_object_max_wait_s`,
`required_by`, `gate_rehearsal.skip_*`) + the two argv tokens in config-keys.json:421 / templates/config.json:112;
the fresh copy's config carries `measured.e2e_page_load_s` (uitest: sign-in 2.2 s; the editor page not yet
measured — the rehearsal measures it) and `page_object_max_wait_s: 30`; CHANGELOG lines from every
report; P20 FR line + FR-13 house-pattern debt line (mechanism commit, axes enumerated, `tier: fable`);
backlog rows for every "queued" line of the critics t-229/t-233/t-234/t-238/t-239/t-243/t-244/t-251/
t-254 and B-233/B-234 updates; full `selftest.py` + `install_smoke.py` on an idle machine; commits by
topic; the frozen run package rebuilt from the repo. Owner decisions still open: the two
`Dockerfile.test` lines (build sha); F7 of t-227 (the gap does not hold delivery_ready).

**Accepted today after 11:45 (all UNCOMMITTED package code):** t-224/t-231/t-241 (gate A measures the
stand, waves 1–2, portable probe argv, A20), t-226/t-237/t-240/t-247 (the blocked S5 window closes in
one record; ran-red marks; receipt reader; texts), t-225 (driver cluster §1/3/4/5), t-235/t-236/t-242/
t-248 (reinstall = fresh: manifest, classification, config migration, onboard_apply, version line),
t-245/t-246 (P20 §1–3: then_oracles, behaviour claims, gate A answers applied by code), t-252 (manual
capture by code). Specs with Lead decisions + critic overrides: t-217 §0d, t-218 §0d/0e/0f, t-219 §0d,
t-227 §0d, t-232 §0/0c/0d, t-250 §0/0c. Findings: F-cmp2-29 (the stand ran S0–S4 without the story's
backend and the factory never said so — S0 identity probe queued after wave 3).

## State at 11:45 (01.10) — the owner stopped cmp2 for good; fixes BEFORE the fresh run; then 10:20, 05:15

Owner (10:25): «Прогон больше не возобновляй… Надо починить все важные проблемы которые нашли и потом
перезапустим прогон заново». Owner (11:30, P20 in PROJECT.md): code is never an oracle. Owner (11:35):
an unanswered before/now question is a GAP in the report. Owner (11:50): «ответы на вопросы гейта A
сегодня никуда не записываются — это надо починить до прогона».

**MUST land before the fresh run (the owner's conditions + Lead's):**
1. t-227 §3 — gate A answers recorded and applied by code (`apply_gate_answers` from `record_by_code`;
   rows resting on a question carry `if_answered` for every reading; the S3 exit refuses otherwise) —
   OWNER'S CONDITION 11:50.
2. t-227 §1/§2 — oracle provenance per Then (P20), implementation-only register rows as behaviour claims
   with before/now questions.
3. t-225 — driver: resume once per dispatch+session with the stand clause, dispatch from the field,
   honest window note, window_rounds cap (S5).
4. t-226 + t-230 — the blocked S5 window closes in one record (code, then the role texts).
5. t-224 — gate A rehearsal measures the stand (precondition cards, keys only when a case needs them,
   runtime probes derived, the e2e page-load limit card).
6. t-228 (after t-226) — a person's word on a named block recorded by code (`go on`/`retry`/`stop`),
   controller shape errors read stage_overrides.
7. The stand: `uitest` profile (nginx build) for e2e — the owner switches (RUNBOOK §1); the copy from
   `prepare_copy --base` with the SDK/collect check; `execution.runtime_probes` for api and e2e-ui;
   profile commands through `poetry run`.
8. Package integration: full `selftest.py` + `install_smoke.py` on an idle machine, commits by topic
   with axis blocks and `tier: fable`, the frozen run package rebuilt from the repo.
9. F-cmp2-29 (owner's question 11:59): the stand ran S0–S4 WITHOUT the story's backend and the factory
   never said so — S0's stand probe is liveness only; the identity probe (`runtime_probe.py`, diff files
   vs container) lives only in S5. Fix: S0 runs the identity probe per impl repo right after the diffs
   are taken and prints the fact to the person (one line; S1–S4 go on, the fact travels in the handoff);
   gate A rehearsal repeats it (t-218) and S5 does not open without `matched` or the person's word.
   Builder AFTER t-224 lands (owns overlap: `runtime_probe.py`, `gate_preflight.py`); its own spec row,
   not folded into t-224.

Queued (not blocking the run): t-218 §4 (`poetry run` applied by code, F4), the driver second pass
(F-cmp2-3/-4/-7), the S3/S4/S7 loop caps, the ledger/traceability reconciliation of blocked instances,
the backlog rows for F-cmp2-17..28 and every "queued" line of the t-221/t-222/t-223/t-228 critics.

Specs (all with Lead's fork decisions in §0 and the critic overrides in §0c): `docs/tasks/specs/`
t-211 (built: t-214), t-217 (building: t-225), t-218 (building: t-224), t-219 (building: t-226; texts
t-230 next), t-227 (critic t-228 running; three builders after t-226/t-225). Journal through t-228.

**Agents alive at the compact (11:55) — their reports arrive as task notifications; accept each by its
witness, control-rerun the ONE judging test file, journal `accepted` with `by: fable`:**
- t-224 builder (sonnet) — gate_preflight.py, runtime_probe.py, their tests, artifact-contract.md + two
  slices, qa-case-designer.md + its index slice. Judging file: `scripts/tests/test_gate_preflight.py`.
  Critic after (diff > 100 lines).
- t-225 builder (sonnet) — story_run.py, test_story_run_refusals.py, test_story_run_loop_b.py,
  driver.md, a NEW table at the end of state-exits.md. Judging files: the two tests. Critic after.
- t-226 builder (sonnet) — window_record, story_step, s5_precheck, controller, acceptance, contract,
  manifest_put + their tests + new test_blocked_by_env_window.py + the S5 row of state-exits.md.
  Judging file: `scripts/tests/test_blocked_by_env_window.py`. Critic after.
- t-228 critic — DONE (11:53): C1-C12 folded into t-227 §0c. NEXT: dispatch the three t-227 builders
  in order per §0c C12's per-builder owns (a: validate_artifacts/contract/the register section/tester+
  designer texts — after t-226 lands for contract.py; b: planning_contract missing_branch + one resolver +
  apply_gate_answers BEFORE gate-decision + the record_by_code call + strategist text — after t-225 for
  story_run.py; c: traceability/ledger/check_delivery/coverage_contract/report_facts/manifest_from_tests/
  stage_guard + automator/critic/rubric/vocabularies texts). Then the §2-of-t-217 builder (a person's word
  on a named block -> waiver by code, `go on`/`retry`/`stop`, controller shape errors read stage_overrides;
  after t-226) and the t-219 texts builder (B9; after t-226). Critics after each builder; the t-227 B10
  critic rule uses `expectation_unconfirmed` (F6) — P20, never "check against the source".
Each dispatch carries the header lines `given:`/`owns:`/`non-goals:`/`handoff:`/`edges:`/`DoD:`; the
label starts with the model; next free task id = max in the journal + 1 (re-read the tail); owns must
stay disjoint between live builders (story_run.py: t-225 only; contract.py/controller.py: t-226 only).
The journal_echo hook refuses non-sequential ids and `delegated` on a closed id: a critic review is its
own task id, never the builder's.

## State at 10:20 (01.10) — cmp2 STOPPED at S5 (blocked UI window, no exit); then 05:15

Owner (06:3x): «Я ушла спать. Продолжай прогон» — the standing word: fix blockers, record findings, answer
the factory's questions on her behalf. Run log: `experiments/cmp2-15045/cmp2.md` (stops #16-#27, findings
F-cmp2-17..28). The driver is NOT running (stopped by Lead at 10:08, pid 23988; the orphaned role session
of S5-qa-code-critic-4 killed). No MR, no Jira write (P8).

**Where the run stands.** S0-S4 done; gate A recorded by code 06:00 (Q1 a, Q2 b = the owner's own word
«позиция в графе, не координаты», Q3-Q6 as built; answers in `experiments/cmp2-15045/answers/`). S5:
window 1 (API, TC_010/012/014/015) done — automator-4 ran the tests (`poetry run pytest`), code critic-1
accepted; TC_012 green, TC_010 red (error details string vs list), TC_015 red (PUT multi-project 400 vs
a guessed 403), TC_014 partly (second-user partitions blocked). Window 2 (e2e-ui, TC_004/TC_008):
BLOCKED by the stand — measured in a real browser (F-cmp2-26): a full page load of
`/workflows/<id>/edit` on the Vite dev stand renders after 70-110 s, client-side navigation 1 s; the
page objects wait 5-30 s. No sanctioned exit exists for a window whose every instance is
`blocked_by_env` (F-cmp2-28): the conductor looped automator 5-11 / code critic 2-4 ($7.28 for S5,
$22.38 for all roles so far, conductors not counted). Controller state is consistent:
`S5-qa-code-critic-5` registered and checkpointed `blocked` (reason + remaining "run on preview"),
`next` = `resume_checkpoint`. Stand: backend `0cc6c4f11` (owner, 05:25) + `customer-config.yaml`
tweak kept; UI container restarted by Lead 06:05 (loses its network when the backend restarts —
RUNBOOK §1 line owed); `/v1/workflows/{id}/validate` live; `execution.runtime_probes.api` and
`.e2e-ui` written into the copy's `qa-factory/config.json` (both matched); all profile pytest commands
there now `poetry run pytest` (F-cmp2-25); the copy's poetry env reinstalled (SDK was missing,
F-cmp2-19). Jira assistants registered in the CLI config by Lead (owner switched the mode for it),
`alive` verified.

**Owner's decision in the morning (one of):** (a) build the exit — `window_record` writes a `blocked`
record for a window whose every instance is `blocked_by_env` with a remedy, `story_step finish` accepts
it, S5 closes with those as not executed (P19 step 5); the marker-bearing note is not raised as a
refusal; a cap on the conductor's rework rounds per window — then sync and relaunch without `--answer`
(the registered critic-5 checkpoint will resume: answer it «blocked, close»); or (b) accept cmp2 as
measured up to S5 (the comparison's purpose is the findings: 12 new ones) and stop. Lead's
recommendation: (a) as a designer-drafted spec (3 files, the S5 window contract) — not built at night
without her word, because it changes what a closed stage means.

**Package work accepted since 05:15 (uncommitted, in the repo; the frozen run package at
`%TEMP%\cmp2-pkg` carries only t-213 of these):** t-213 (s5_precheck footer carries REPAIR_MARKER,
F-cmp2-21); t-211 spec (`docs/tasks/specs/t-211-gate-stage-rehearsal.md`, designer + Lead's forks §0 +
critic-on-plan overrides §0b, t-212) and its implementation t-214 (critic t-215 accept with fixes; attempt
2 accepted 08:13: `gate_repair` step at await_gate, series/cap/stop reasons, F0 KNOWN_REFUSALS row,
kept gate answer, docs rows, `test_story_run_gate_repair.py` 247/247) — FR-33 unproven live (no gate
stage passed through it yet). Queued from t-215/t-214: C5 approve_with_fixes under F0, C6 conductor.md
wording at B, C7 declared_verdict stale file, state-exits rows (gate_repair, gate_answer_kept,
gate_entry_owed), `(exit N)` regex -> field, 3x gate_preflight per gate, F0(c), F3(c), F9, a debt line for
KNOWN_REFUSALS (FR-13). From the run: F-cmp2-18 (precondition cards), -19 (prepare_copy SDK check), -20
(check_s5_credentials vs cases — the owner's 23.09 return), -22 (pending_words filed to a quoted
dispatch id), -23 (resume_* after the role stopped — t-210 analog), -24 (runtime probes derived at gate
A), -25 (gate card `apply` executed by code), -26 (stand: Vite dev UI), -27 (the conductor does not
execute the person's waiver words — record by code), -28 (blocked window exit). Journal through t-215
(validator exit 0). A22 scribe headroom (890 B) still owed.

## State at 05:15 (01.10) — cmp2 at S4; then 01:45, 00:31, 23:50

Owner (05:14): «готовся к компакту». The run goes on; the owner wakes up to it.

**cmp2 (TP1-15045) at 05:15: S0–S3 done, S4 designer accepted (19 evidence files), the case critic
`S4-qa-case-critic-1` running** (pid 17296, log `experiments/cmp2-15045/runs/cmp2-16.log`; every stop,
answer and finding: `experiments/cmp2-15045/cmp2.md` — 15 stops so far, F-cmp2-1…16). The driver runs
the FROZEN package `%TEMP%\cmp2-pkg\qa-factory`, last synced 05:02 with everything accepted (nothing is
pending in the repo package now). Relaunch command after an exit 3: the one in cmp2.md "Команда"
WITHOUT `--skip-sources` (C5a; F-cmp2-7) with `--answer <file>`; answers live in
`experiments/cmp2-15045/answers/`. Standing: a `conductor` question about a dead role session → "it is
dead, go on" (F-cmp2-11); on a structured-plan refusal the driver now resumes the role itself (t-210).
The stand backend is still on 13797's commit (the owner switches it; the UI is right) — expect the
runner (S6) to meet a backend without the story's /validate endpoint.

**Accepted since 01:45 (all package code still UNCOMMITTED):** t-201 (P9b), t-202 (report critic →
fixes), t-203 (B-224 critic → fixes), t-204 (F1 window_gap + F6), t-205 (F2–F5 + texts), t-206
(plan contract names the validator's fields), t-207 (validator messages name fields; decisions side file),
t-208 (a person's words whole in the journal notes), t-209 (`row_requirements` reads `requirement_refs`),
t-210 (driver row `resume_structured`); t-198 B-224 P1 with the critic's F1/F2 applied. Lead
integration done: slices regenerated (3×), `CLI_SCRIPTS` +10. Audit: 74/75 — A22 the scribe's headroom
890 B (needs −110 B in `agents/qa-doc-scribe.md`).

**Running builders: none. Owed:** a driver-topic critic (t-204, t-208, t-210 on `story_run.py`); the
open-questions critic (t-153..t-157, t-181, t-200); the B-231 follow-up (t-193) critic entry; backlog
rows (F-cmp2-1…16 + the journal's queued analogs); RUNBOOK (the shim `~/bin/testproject1`, `testproject1 setup
assistants`, `prepare_copy --base`, the exclusion list, the attachments-of-old-runs exclusion by URL);
the rest of the 23:50 integration list; commits by topic; full `selftest.py` when the machine is idle
(the 01:40 run: 274/288, reds listed in cmp2.md F-cmp2-6).

## State at 01:45 (01.10) — cmp2 RUNNING; read this, then 00:31, then 23:50

Owner 00:40: «не хочу ещё откладывать прогон … после завершения исправлений сразу запускай фабрику на
стори TP1-15045 … блокеры чинишь, ошибки записываешь в план исправлений и отвечаешь на вопросы
фабрики по стори … утром посмотрю». B-224/A4/A5 after the run; the gate A card softened instead (t-199).

**cmp2 started 01:40** (pid 28532; notes, command, question log: `experiments/cmp2-15045/cmp2.md`; list
`experiments/cmp2-15045/skip-sources.txt`; copy `testproject1-dev-fresh/testproject1-sdk-cmp2`; the package FROZEN at
01:39:51 into `%TEMP%\cmp2-pkg\qa-factory` — the driver runs `--plugin-dir` there; fixes are robocopied
into it only at a driver stop (exit 3) after green tests). The stand backend is NOT on the story's commit
(`92f699901` instead of `0cc6c4f11`): the session may not switch it (classifier: shared resource) — the
owner does it in the morning; the UI is on `e6532059c` already.

**Accepted since 00:31:** t-193 (B-231 fixes 431/431, 313/313 + the `work/sources/` skip except
`mr-*.json`), t-194 (P9a/P9c + record_size at S9), t-195 (P10 texts), t-196 (P6-C brief line + Q9
formula_version 2), t-197 (B-224 spec, forks decided in the spec), t-199 (gate A card words), t-200
(open-questions wiring). Integration done by Lead: `contract_slices.py --write` (A9 green), `CLI_SCRIPTS`
+10 (A1 green), `test_audit_rules` 75/75. `pytest tools/` 3252 passed / 4 failed, all four environmental
(two timing tests under builder load, two hook-liveness tests seeing this session's own search ledger).
Full `selftest.py` running in the background at 01:40 (result → cmp2.md).

**Running:** t-198 (B-224 P1, controller.py — lands in the run's package only after a critic), t-201
(report P9b, story_run.py stage_S9/finish — synced into the frozen package at the next driver stop).

**Still owed before release:** the report topic critic (t-183, t-188, t-189, t-191, t-194, t-195, t-201),
the B-224 critic (t-198), the open-questions critic (t-153..t-157, t-181, t-200); B-224 landing; the rest
of the 23:50 integration list (artifact-writers, state-exits, vocabulary, driver.md, SKILL.md, RUNBOOK,
SIBLING_MAP, debt lines, FR-24/25 reword, CHANGELOG, `install_smoke.py`); commits by topic; backlog rows
(23:50 list + tonight's analogs in the journal notes of t-191, t-193, t-194, t-195, t-196, t-200).

## State at 00:31 (01.10) — the delta over 23:50; read both

Accepted after the compact: **t-192** (critic B-231: `fit_with_fixes`, no blockers; cmp2 rehearsal without
network passed on every step; six fixes → t-193; queued: `jira_ticket get/children` + `probe_jira_direct`
doors (Jira-only, 0 GitLab bytes on cmp2), the orchestrator-path scout "Left out" line (axis 5 twin),
gate A wording for `ref` words, the unguarded record Write (axis 4 debt), RUNBOOK flag/format/
`prepare_copy --ticket` and the printed start command) and **t-191** (report P7 `report_facts.py`, 266/266,
Lead's control rerun 266/266 + 215/215; builder's decisions 1–8 accepted; fork R-210.3 `record_size` → t-194;
analogs queued: `REPORT_FORBIDDEN` substring false positives (`work/` in `framework/`, `ti_` in `multi_`),
S5–S7 `stage_overrides` in no block, traceability's 110-char bug title, the appendix not refreshed after
gate B, `grammar.heading_spans` public).

**Running at 00:31 (all builders, sonnet):** t-193 (B-231 fixes 1–6: detector shapes, `_has_token` on
id-like fields only, `excluded_heads` null + branch words resolved, the `source_list` question's two groups,
`_door` full commands + conductor.md `--revoke`, `s0_list_too_late` on `s1_completed`; owns
`source_exclusions.py`, `story_run.py` exclusion functions only, its three tests, conductor.md); t-194
(report P9a S9 exit + `record_size` at S9 + P9c size at S2; owns `stage_done.py`, `test_story_closed.py`,
`test_sizing.py`); t-195 (report P10 texts: scribe charter under 9,000 B, s8.md §2, s9.md §0a, the yaml,
the scribe's card with all `REPORT_SECTIONS`; NEW `test_report_texts.py` doc witness); t-196 (P6-C
`brief_pack.proof_required_lines` + Q9 `formula_version` 2 on money metrics; owns `brief_pack.py`,
`metrics_projection.py`, `metrics-contract.md`, their tests).

**After they land:** P9b (driver `stage_S9`: the rebuild trigger `report_facts.write` after the retro,
the S9 refusal move — `--write` once then S9 again, other refusals a printed finding; plus the
`story_run.finish` `unresolved=(word, reason)` → `--unresolved --reason` line owed to t-185) — waits for
t-193 (same file `story_run.py`); then the report topic critic (covers t-183, t-188, t-189, t-191, t-194,
t-195, P9b) and a B-231 fix critic entry only if t-193's diff is over ~100 lines; A4/A5 or the softer
gate A card; B-224 spec; the wiring follow-up; then the integration list of 23:50 and the commits by topic.

**cmp2 list, third line (t-192):** `135699ae2c182eccd49ba6c66f469fc1c55359f1 — head of that draft MR`
makes sha matching and the `git_route` skip independent of ls-remote. cmp2's own check after S1
(runbook): the record's X1 `head_sha` not null; the inventory's 1924 item `excluded`/X1 with no
`local_ref`; no `work/**/mr-1924*`; `grep -ril "merge_requests/1924\|testproject1-ui!1924\|135699ae2\|visual-workflow-diff-validation" work/`
hits only in the snapshot comment, the inventory, the record and free text; the manifest's
`requirement_sources`/`existing_test_candidates`/`implementations`/`existing_tests` clean; the scout's
transcript without `glab`, `git show 135699`, `origin/TP1-15045-visual…` or a WebFetch of the MR
(manual; no code gate).

## State at 23:50 (30.09) — superseded only by the 00:31 delta above; READ BOTH

Owner's last words (30.09 20:30): tell her when cmp2 can run (on TP1-15045); the stale Draft MRs
linked to it are handled by B-231 (built: waves A/B/C accepted); release/MR/push only on her word.

**Running at 23:50:** t-191 (builder, report P7 `report_facts.py` — resumed after a watchdog stall
at its start; it may report or stall again: if stalled, relaunch it as a NEW task with the same
dispatch text, journal id max+1) and t-192 (critic, the B-231 topic pass with a full cmp2 rehearsal
without network). Both report by SendMessage; accept each with a journal event (`accepted`, witness
verbatim, `by: fable`); a critic's fixes go back to the builder as a follow-up (SendMessage) or a
new task.

**Accepted today, ALL PACKAGE CODE UNCOMMITTED (~110 paths):** true price (t-153, t-164, t-165 att.2,
t-166 att.2, t-169, t-170, t-171, t-182; critic t-179 accepted, its fixes done in t-182); B-194
(t-116, t-117, t-140, t-141, t-142, t-143, t-149 att.2, t-158; critic t-149 second entry); B-207
proof-by-code (t-144, t-145/t-161, t-168, t-174, t-175, t-176, t-177, t-178, t-185, t-187; critic
t-184 accepted, its fixes done in t-187); open questions A1-A3, B1, B2 (t-153-t-157, t-181), dashboard
(t-124/t-150, t-162, t-163, t-169), B-172 P1 (t-132/t-151/t-159), B-231 (t-172 designer, t-173
critic-on-plan, t-180, t-186, t-190), report truth P1, P2, P4, P8 (t-183, t-188, t-163, t-189).

**Still to build before cmp2 (each: dispatch → builder → critic per topic):**
1. Report P7 (t-191, running) → then P9a (S9 exit check in `stage_done`), P9b (driver: the rebuild
   trigger at S9 + the `story_run.finish` `unresolved=(word, reason)` line owed to t-185), P9c (size at
   S2), P10 (scribe texts; `test_ahead_cards` is red 230/231 until then); then the report topic critic.
2. Open questions A4/A5 (need A0 = B-224 spec — a designer brief) OR softer words on the gate A card
   ("the factory decides anew"); decide with the owner if time is short: soften the card.
3. B-224 (the designer dispatch's `scope: []` at S4) — spec first.
4. Q9 formula-version bump in `metrics_projection` (t-179: history points at the old 1.5x prices).
5. P6-C's brief list of predicate-required instances (FR-38) in `brief_pack.py` (t-184).
6. The wiring follow-up: `variant_errors` at the S3 exit; E-19 stale reason; waiver/remark ids give
   `named`; backslash before an id.

**Integration by Lead (once, when the wave lands — Lead-tier, no dispatch needed):**
`contract_slices.py --write` on the live tree (A9 stale slices; A22 headroom measured 1,134 B after
t-185); `audit_factory.py` `CLI_SCRIPTS` += launch_check, question_register, question_stop, bug_records,
test_repo_base, task_price, test_novelty, probe_debt, source_exclusions, report_facts (A1 red until
then); `refusal_registry.py` `PT-config-write` (guard_pre_tool.py:1692; test_s0_close_order 27/28);
`references/artifact-writers.json` (question-answers.jsonl, test-repo-base.json, probe-debt.json,
source-exclusions.json, test-report.md by report_facts/stage_done); `design/state-exits.md` rows
(exclusion `--revoke`, `source_list` block, S5 `unresolved` done by t-185); `handoffs/vocabulary.yaml`
(`gap_unknown_verdict`, `source_exclusion_origins`); `design/driver.md` `source_list`; `conductor.md`
the `--revoke` road; SKILL.md the `--skip-sources` flag; `docs/RUNBOOK.md` (flag, list format,
`prepare_copy.py --ticket TP1-15045` REQUIRED for cmp2, cmp2's own check from t-192's verdict);
SIBLING_MAP axes (run-block readers axis 8; readers of money on one rate base; writers of
state/cost/<session>.json; price readers; function_sha reader on axis 7); debt lines (B-217, F-2 stored
novelty trust incl. the F-B hole, B-172 interim, case_stamp:184, contract:1982, a role's Write of
script-owned artifacts); FR-24/FR-25 reword (the code names NO authoritative record, per P18) +
`tools/factory_rules_index.py` (mechanism commit: four questions); `references/templates/config.json`
`questions.stop_at`; onboarding p3/p4 price-table answers; `contract.trace_row_errors` empty case with
`plan_row`; `ahead-cards.json:76` + `artifact-contract-results.md` the two report sections;
`finalize_task._ghost_cases` public; a `hooklib` helper taking a project root (`FACTORY_FOLDER` in
test_repo_base); `TP._own_requests` public; `role-commands.json` `manifest_from_tests.py` entry check;
the `request ={` slip in run_suite.py; CHANGELOG; full `selftest.py` + `install_smoke.py`; commits by
topic (price / B-194 / B-207 / open questions / dashboard / B-172 / B-231 / report), each mechanism
commit with its axis block and `tier: fable`.

**Backlog rows to add at integration (not yet in BACKLOG.md):** `_pair_tag` 12-char truncation
(`external-<hex>`); the Stop capture drops a gone subagent's rows (+ `recover_codex_usage.py:71`);
the session lock held 17.8-99 s for a 1.2 s write; a marker with no cost file has nowhere to record;
raw WHY words in task_price's finding; Q4 double count; `story_budget`'s `_plural`; `session(s)`
strings (factory_dashboard/friction/metric_signals, pinned by test_factory_dashboard_task_view
:139/:149/:248, test_orchestrator_share :243/:260); By task/By model/By day cents; one flaky run of
test_dashboard_task_price (FR-31); `ticket_adapter get/children/probe` uncovered by exclusions; Jira
remote links never enter the inventory (M4); `customfield_31100` URLs not scanned; `orchestrator_totals`
by task tag; jev judge spend in no price; a `--read-only` render lists no stale files; settle keeps no
memory across critic starts beyond `same_bytes`; the halt/s1_review roads may finish a saved halting
digest on a re-run; `halt_text` says "continue from where you stopped"; `s5_precheck.py:1527` private
import; project-home-only bug readers (audit_factory:397, exit_gate:469, judge_results:263); no
validator twin for the gate A block; A14 `hooklib.py` diverged (which builder? check at integration);
test_scout_reliability KeyError `factory_diagnostic` and test_doctor_context red (seen by t-180's
builder — cause unknown).

**Owner-facing, for the cmp2 runbook:** the owner writes a plain-text file, one line per source
(`testproject1-ui!1924 — Draft MR of an earlier factory run, not a product change`;
`branch:TP1-15045-visual-workflow-diff-validation — the branch of that draft MR`; reasons may be in
Russian), prepares the copy with `prepare_copy.py --ticket TP1-15045` (removes the tracked
`artifacts/TP1-15045` inside the copy — testproject1-sdk HEAD tracks 114 files of a judge run), and starts
the driver with `--skip-sources <file>`. VPN on for `git ls-remote` at S0 (failure only prints).

## State at 20:35 (30.09) — superseded by 23:50; kept for the record

Owner decisions since 18:45: t-134 F-1 (unmeasured green tests are proven, V9-V12); a person's
answer replaces an existing own price (t-164); B-207 P5-D + P6 are built BEFORE the trial run;
the trial run (cmp2) is on **TP1-15045**; before it the person must be able to say which linked
sources are stale (B-231, Draft MRs of earlier runs) — build it before cmp2.

Running at 20:35 (accept each with a journal event; critic passes per topic at integration):

| task | what |
|---|---|
| t-149 attempt 2 — ACCEPTED 21:38 (kept for the record) | critic verdict 21:20: fit with fixes. Road of the word reproduced (0 findings, `passed_by_word`, no gap after the own tag); F3b and F-order confirmed. Fixes sent to the builder: blank-note patch strips the `could_not_judge` note (check the MERGED record); `manifest_put` refusal names only the broad door (print the own tag; "already passed" when a word exists); Lead's decision on the critic's finding 5: a broad `changed-after-red` word passes only pairs whose green run predates the word's `at` (the threshold-stop rule); the A22 trim (qa-automator 41,135 B after `--write`, t-158's DoD not met because t-149's contract text grew). t-140 ACCEPTED 21:24 on this verdict. QUEUED BEFORE cmp2: `story_step finish` has no `--unresolved/--reason` door for the S5 window (`could_not_judge`, `fitted_to_code`, `handed_to_person`; controller accepts at :2665; no state-exits row). Queued: `_pair_tag` 12-char truncation collides for `external-<hex>` attempts; t-109 P7 must read `word_passed_pairs` |
| t-173 — ACCEPTED 21:44 (kept for the record) | the B-231 spec `docs/tasks/specs/t-172-source-exclusions.md` (designer t-172 accepted 21:23; Lead's fork decisions at its top): facts by trail, every inventory writer and fetch site, S0 feasibility, 17 edges, the matchers' error direction, the three-wave cut |
| t-165 attempt 2 — ACCEPTED 21:44 (kept for the record) | critic verdict 21:25: fit with fixes; empirics reproduce (16 flagged, A = B, probes 4.0 / 6.0 with no double count). F1 REVERSES the dispatch: a lock whose owner record is dead is NOT broken (the OS lock dies with its process; a busy lock + dead record = stale record + live holder; measured 9/12 overlapping captures) — drop the stale record, retry, never capture lock-less. F3: marker + gone transcript gets `recapture_status: not_recomputed` and the explicit door clears the marker (FR-40/41). F5: an in-place rewritten transcript keeps rows whose `request_key` the rebuild lacks. QUEUED (backlog rows at integration): F2 the session lock is held 17.8-99 s for a 1.17 s cost write (release after the write; the 8 s wait loses every collision, the marker saves the money); F4 the ordinary Stop capture drops a gone subagent's rows (4.0 -> 2.0; move the carry into `_capture`; `recover_codex_usage.py:71` is a sibling writer); SIBLING_MAP needs an axis "writers of state/cost/<session>.json"; the dashboard discards `recapture_stale` results at `factory_dashboard.py:3296-3297` (t-169's file) |
| t-174 (builder, 21:31) | B-207 P5-D the switch (`manifest_from_tests` writes `novelty` + `generated_from`; V2, V3) |
| t-175 (builder, fix round 21:42) | B-207 P5-E done (ledger 167/167); fork found in P5-C's `not_required_why` (`handed` decided after `_wanted`, so a keyless or fresh-unchanged handed row read "unchanged test"): Lead added `proof_level.py` and `case_stamp.py` (:186 analog) to its owns — `handed` first |
| t-177 (builder, 21:33) | B-207 P6-A `probe_debt.py` find + settle (R11, R12, V1, V6, F-3/F-4/F-8) |
| t-178 (builder, 21:40) | B-207 P5-G window items carry resolved novelty (R8 under V10/V12) |
| t-179 (critic, 21:40) | the TRUE PRICE topic pass before commit: t-153, t-164, t-166, t-169, t-170, t-171 (+ t-165's money): empirics on both copies, every money reader enumerated, the semantics questions |
| t-180 (builder, 21:44) | B-231 wave A: `source_exclusions.py`, inventory marks, library-level fetch doors, guard (spec t-172 + C1-C8) |
| t-181 (builder, 21:48) | open questions B2: threshold stop wired into `story_run.py` (R15 wiring, R17, Q8); serial before B-231 wave B on the same file |
| t-182 (builder, 21:59) | price fixes after t-179's verdict (fit with fixes): F1 MUST — under `rate_overrides` the ceiling and every B-derived figure on the price base (recaptured + override, cap $20 must STOP at $26.14; today "87%"); F2 override wording; F3 largest-remainder cents; F4 cache-read rate from the story's model (sonnet-5-5 $0.2, not sonnet-4 $0.3); F5 contested amount; F6 tolerance from `TOLERANCE_USD`; F7 field names |
| t-192 (critic, 23:42) | the B-231 topic pass before commit and cmp2: a full cmp2 rehearsal without network (list → prepare_copy → S0 → S1 inventory → brief → S1 exit gate on the M5 manifest → gate A / retro → revoke), every fetch site, matchers, C5c vs F2d, cmp2's own check spelled out for the runbook |
| t-186 — ACCEPTED 23:42 (277/277, 150/150, 208/208, 28/28, 27/27, 16/16; the stall left nothing mutated) | B-231 wave B: `--skip-sources` + S0 block (C1/C5), brief masking (P5/C7), the net (P8: vcs_evidence, exit_gate manifest detector, receipt leak), the git channel (C2), `prepare_copy` removes the ticket's tracked artifacts in the copy (C1) |
| t-180 — ACCEPTED 22:24 (wave A, 329/329) · t-181 — ACCEPTED 22:21 (B2, 172/172, Lead's rerun) | wave A decisions confirmed; B2: free words write no register record (kept whole; error toward open), `where` = "S2 stop", `by` = person, fallback = the same dispatch in a new session |
| t-190 — ACCEPTED 23:04 (187/187) | B-231 wave C: gate A and retro name the left-out sources (applied / unmatched / taken back), `sources_left_out` fact, the `factory_marker` origin branch |
| t-191 (builder, 23:15) | report P7 `report_facts.py`: facts + deterministic blocks + `--write`/`--check`/`--json`; conversion of the unmarked cmp1 report with report-history |
| t-185 — ACCEPTED 23:15 (215/215, 259/259; card 9146 → 9143 B; A22 free 1134) | P6-B + the `finish --unresolved --reason` door DONE (203/203; real-Controller road shown); the V1 addition with a deviation accepted (the probe gets the remaining budget as its own `--timeout`, a kill only as a net at +120 s — a kill would skip `probe_by_code`'s in-place restore); P6-C decided: option 2 (replace the Witness sentence, -3 B); plus: the debt file gated on its dispatch id, rebinds bounded by the budget. Driver line owed to `story_run.finish` (t-186's file): `unresolved=(word, reason)` → `--unresolved --reason` on `complete is True` |
| t-182 — ACCEPTED 22:43 (price fixes; recaptured + override cap $20 now STOPS at $26.14; cents add up on every copy) | left cosmetic: `usage_status xN`, `session(s)` strings pinned by two test files outside owns; By task / By model / By day cents (plain rounding); one flaky run of `test_dashboard_task_price` (FR-31) |
| t-188 — ACCEPTED 22:57 (249/249) | report P2 owner lift; a case with zero rows stays `product` (the critic's override over the dispatch's edge); interim told-not-asked line until P7; integration: `finalize_task._ghost_cases` public |
| t-189 — ACCEPTED 23:17 (215/215; prose cap excludes block bytes; integration: `contract.trace_row_errors` empty case with `plan_row`, ahead-cards :76 + results contract gain the two sections, `test_ahead_cards` red until P10) | report P8 the contract: template blocks + `facts` markers, `grammar.REPORT_BLOCKS`/`find_blocks`/`replace_block`, heading order (gate A section, open questions after "Left with you", gate B absent before the gate), validate_artifacts report checks, traceability (bug reader, F32/F33, the answered-at-gate-A suffix). P7 (`report_facts.py`) after it |
| t-183 — ACCEPTED 22:34 (90/90, Lead's rerun; cmp1: 8 red ghosts visible without the record, all 13 quenched with it) | |
| t-187 — ACCEPTED 23:08 (240/240, 187/187, Lead's reruns; dirty scan on the live cmp1 copy 4063 → 8) | B-207 fixes after t-184: F-A (a measurer exception must not let the merge drop a stored `new`/`changed`), F-B (`manifest_put` refuses the item form on a row), 3e (the dirty scan excludes `qa-factory/` — cmp1's worktree has 4063 dirty paths, 2825 in telemetry; cmp2 would fall to `head_now` and lose the measurement) |
| t-184 — ACCEPTED 22:31 (fit with fixes) | the PROOF-BY-CODE topic pass before commit: P5-A..G, P6-A (t-144, t-145/t-161, t-168, t-174, t-175, t-176, t-177, t-178): end-to-end road on a temp git fixture, the cmp1 copy, every reader of novelty/not_required, the semantics questions |
| t-185 (builder, 22:11; its text says t-184) | B-207 P6-B (the settle in `story_step start`, V1) + P6-C (one charter sentence) + the `finish --unresolved --reason` door for the S5 window with its state-exits row |
| t-177 — ACCEPTED 22:07 (P6-A + fixes; Lead's control reruns 198/198, 407/407) | |
| t-183 (builder, 22:03) | report P1 reducer: `finalize_task` onto `read_run_blocks`, per-pair supersession, `raw_status`, quench by retraction, one definition of red over the whole history (13 cmp1 ghosts with an unconfirmed red stay visible) |
| t-174 — ACCEPTED 22:00 (P5-D + the merge drop and idempotence fixes) | P5-D done (165/165, +0.8 s for 20 functions); fixes: `manifest_put._merge_entry` drops `novelty` when the writer's row (with `generated_from`) carries none (V2 on a re-run); identical measurement keeps `measured_at` |
| t-177 (fix round 21:57) | P6-A done (186/186; cmp1: 0 items today, 16 `reprobe` once novelty is written); fixes: `probe_by_code` never lets a `not_executed` run overwrite an `intended_failure` record (`last_attempt` instead); the critic's card gains `--oracle`; a stale `probe-debt.json` is rewritten empty; the scope pre-check honours a waiver |

t-178 (P5-G) ACCEPTED 21:59 (pure 156/156, full 277/277; Lead's control rerun 156/156). t-179 (price critic)
ACCEPTED 21:59. Integration items from t-179: FR-24/FR-25 reword (the code names NO authoritative record,
per P18 — the rule text still says "names the authoritative one"), SIBLING_MAP axis "readers of money on one
rate base", Q9 formula-version bump BEFORE cmp2 (history points at the old 1.5x prices); later: jev judge spend
(`judge.py cost_usd`) in no price, a `--read-only` render lists none of the 16 stale files.

t-175 (P5-E) ACCEPTED 21:48 with the P5-C reader fix (`handed` before `_wanted`) and the `case_stamp` analog.
Order on `story_run.py`: t-181 (B2) → B-231 wave B (t-182: P4, P5, P8, `git_route`, `prepare_copy`) → later
the wiring follow-up. Order on `story_step.py`: P6-B together with the `finish --unresolved --reason` door
(before cmp2). Wave C of B-231 (P6, `gate_brief`/`retro_numbers`) after t-179's verdict.

ACCEPTED 21:24-21:44: t-140 (piece C), t-149 att. 2 (+ the critic's fixes: merged-record note check, `_word_door`,
the broad word bounded by its `at`, the A22 trim), t-158 (cap: automator 40,972 B / critic 40,866 B on a temp
copy after `--write`), t-165 att. 2 (+ F1 lock never broken, F3 marker road, F5 carry every stream), t-169
(dashboard + the banner crash fixed), t-176 (P5-F), t-173 (critic-on-plan B-231: C1-C8 in the spec).
QUEUED BEFORE cmp2 (from t-149's critic): `story_step finish` has no `--unresolved/--reason` door for the S5
window. QUEUED (backlog rows at integration): `_pair_tag` truncation for `external-<hex>`; the Stop capture drops
a gone subagent's rows; the session lock held 17.8-99 s for a 1.2 s write; a marker with no cost file has
nowhere to record; `TP._own_requests` public; raw WHY words in task_price's finding; Q9 formula version; Q4
double count; `story_budget`'s own `_plural`; `session(s)` strings in factory_dashboard/friction/metric_signals;
`ticket_adapter get/children/probe` uncovered by exclusions (C4); a role's direct Write of script-owned
artifacts unguarded (debt line, axis 4); Jira remote links never enter the inventory (M4); `orchestrator_totals`
by task tag. A14 `hooklib.py` diverged (t-175's audit run) — check at integration which builder touched it.

t-168 (P5-B) ACCEPTED 21:28: `test_novelty.measure` / `measure_many`, 162/162, ten mutations; the
builder's four decisions confirmed (untracked test file at S0 = `new`, untracked helper = `changed`;
raw `cat-file --batch` with newline-normalised compare; empty `code_sha` now = `unknown`; the three
extra pytest config names). Optional follow-ups: memoize `project_module` in `function_sha`'s cache
(33 stats per call); make `test_repo_base._sha256_file` public. t-171 ACCEPTED 21:28 (fixtures by
evidence; `cost_files` = `{usd, sessions=bound, unpriced, of}`; one `_plural`; floor; stage_compare).
P5-G (window items) waits for t-149's fixes on `window_record.py`; P6-A/B/C next.

t-170 (Q6) ACCEPTED 20:54: retro price line "Story price: from $16.65 to $17.42" on the plain cmp1 copy /
"$17.42" two records agree on the recaptured one, 35 of 35 sessions (old code 22, $21.10); ceiling on B
else A with the disputed notice. Q1 decided by Lead: ratio exactly 1.0 = reached, stop; one cent under =
warn. Deferred from t-170's siblings: `orchestrator_totals` still picks requests by task tag (change it
after t-169 lands, since `test_orchestrator_share.py` pins its numbers); B-223 closes at integration
(hash), t-111 line 173 too. Critic pass for the price topic at integration covers t-153, t-164, t-166,
t-169, t-170, t-171.

Accepted since 18:45 (all UNCOMMITTED package code): t-124/t-150 (dashboard P1 + fixes), t-116/t-117
(B-194 A, B), t-132/t-151/t-159 (B-172 P1 + fixes), t-135, t-138, t-141 (D), t-142 (E), t-143 (F,
defect_found -> t-149 att. 2), t-147, t-148, t-144 (P5-A), t-145/t-161 (P5-C + fixes), t-153 (Q1),
t-154/t-164 (Q7), t-155 (A2), t-156 (A3), t-157 (B1), t-160 (P2 fixes), t-162 (P5), t-163 (P4),
t-166 (Q3, att. 2), t-152/t-167 (scouts). NOT accepted: t-140 (piece C) and t-158 (cap trim) wait for
t-149 att. 2 (the critic's pass covered them: fit).

Next after the running ones: B-207 P5-D (the switch; needs P5-B), P5-E (words: V9/V11), P5-F,
P5-G (after t-149), P6-A/B/C; open questions A4 + A5 (need A0 = B-224 spec), B2 (threshold wiring),
B3, the onboarding thresholds question, the wiring follow-up (variant_errors at the S3 exit; E-19
stale reason; waiver/remark ids give `named`; backslash before an id); report P1, P2, P7-P10;
finalize_task onto run_history; Q4, Q8, Q9; B-193 P3, P4, P7-P11 (check the spec); B-231.

Integration by Lead (once, when the wave lands): `contract_slices.py --write`; `audit_factory.py`
`CLI_SCRIPTS` (launch_check, question_register, question_stop, bug_records, test_repo_base,
task_price, test_novelty); `refusal_registry.py` `PT-config-write` (test_s0_close_order 27/28 until
then); `artifact-writers.json` (question-answers.jsonl, test-repo-base.json, report_facts/stage_done);
`state-exits.md` rows; vocabulary `gap_unknown_verdict`; SIBLING_MAP axes (run-block readers = axis 8
as t-167 proposed; price readers; function_sha reader on axis 7); debt lines (B-217, F-2 stored
novelty trust, B-172 interim); FR-24/FR-25/FR-37 texts (mechanism commit); `references/templates/
config.json` `questions.stop_at`; onboarding p3/p4 carry the price-table answers; CHANGELOG; the slip
`request ={` in run_suite.py; full `selftest.py` + `install_smoke.py`; commits by topic.

Before cmp2 (owner's question 30.09 20:30): live run is the gate; the card's promise "the factory
decides anew" needs A4/A5 or softer words; B2 wiring; report P7-P10; B-207 P5-D + P6; B-224; B-231.

## Cross-spec decisions (Lead)

1. **Where a person reads the expectation-change words.** The two drafts disagree, and so does the
   package: the scribe's ahead card says "Section 1 is ledger.md's table pasted verbatim"
   (`references/ahead-cards.json:76`), the scribe's charter says none of the ledger files is shown to
   the person and "Proven" is built from the appendix's basis column (`agents/qa-doc-scribe.md:40-43,
   67-71`; read by Lead 30.09). Decision: B-194 piece G is held; the words reach the person through
   B-211's report facts (t-109 P7 reads `expectation_changes[]`), and the scribe's card is corrected
   in t-109 P10.
2. **One owner of question status (B-181).** t-109 P3 (`gate_brief.question_status`) and t-113 A1/A2
   (`question_register.load`, `_decision_text`) do the same thing. Owner: t-113 A1 (the reader and the
   answers file) and A2 (`gate_brief`). t-109 P3 is dropped; t-109 P7 reads through
   `question_register.load()`. Consequence: t-113 A1 is built before t-109 P7. For a story older than
   the change an id found in the person's words yields `named`, never `answered` (t-113 R12).
3. **Shared files are written by one builder at a time.** `scripts/story_run.py`: t-109 P9b, t-113 A5
   and B2, t-114 P3 — serial. `scripts/gate_brief.py`: t-113 A2, t-114 P5 — serial.
   `scripts/gate_preflight.py`: t-110 P4, t-113 A3 — serial. `scripts/story_step.py`: t-110 P6,
   t-114 P4 — serial. `scripts/manifest_from_tests.py`: t-109 P5, then t-110 P7.
   `scripts/s5_precheck.py`: t-108 B, then t-110 P8. `references/ahead-cards.json`: t-108 C, then
   t-110 P10, t-113 A6, t-114 P2 — serial. `scripts/factory_dashboard.py`: t-111 P1, P2, P5 — serial.
   `scripts/retro_numbers.py`: t-111 P3 before anything of t-109 touching it.
4. **Files no builder owns in these specs; Lead writes them at integration:** `design/state-exits.md`
   rows other than t-108 B's, `scripts/audit_factory.py` `CLI_SCRIPTS` lines, `references/artifact-writers.json`
   entries, `design/factory-rules-debt.md` lines, `CHANGELOG.md`, `scripts/contract.py`. A builder
   reports what is needed under "Needed from integration".
5. **Parallel builders share one working tree.** Each runs only its own witness file while working;
   a red neighbour caused by another builder's uncommitted work is reported, not fixed. The full
   `selftest.py` and `install_smoke.py` run once per integration, by Lead.

## Forks of t-109 (report truth) — decisions

| fork | decision |
|---|---|
| F1 shape | code-owned blocks between markers + scribe prose |
| F2 base for novelty | the test repository's HEAD and dirty flag recorded at S0; fallback "HEAD now" with a printed label |
| F3 stories in flight | the new default applies (required); novelty is measured at read time; the person's word passes |
| F4 unpublished probe | code rebinds and re-runs the critic's stored request; its own spec after t-108 (P6) |
| F5 bug home | OWNER. Interim: the reader reads both homes; texts unchanged |
| F6 which bugs belong to the story | the task folder plus project files whose front matter names the task or one of its cases |
| F7 verdict counts | as recommended in the draft |
| F8 planned manual cases | shown as "wait", fixed now |
| F9 requirements of case-less plan rows | mapped through the row's disposition, fixed now |
| F10 gate A decision | OWNER. Interim: a new section "Decided at gate A" |
| F11 gate B section before the gate | absent |
| F12 what "Fact" size means | OWNER. Interim: the template's counts (requirements, rows, cases, tests); money stays in the retro |
| F13 where size is recorded | `stage_done` S2 exit |
| F14 strength of the S9 check | refuses, with doors and the person's word, for a stale block, gate B words without the block, a factory-owned item in "Left with you", a missing risk; size only when computable; its own crash never refuses |
| F15 where the rebuild is triggered | inside `stage_done` S9, before its check |
| F16 source of risk | the plan row's impact class and defect hypothesis in words now; a strategist column later (backlog) |
| F17 environment finding bound to no requirement | quoted in "Decided at gate A" |
| F18 open questions at the end | OWNER. Interim: its own section after "Left with you" |
| F19 "answered at gate A" suffix | now |
| F20 the cut | three specs by piece boundaries (I: P1, P2, P4; II: P5; III: P7–P10), P6 separate |
| F21 expectation-change words | P7 reads `expectation_changes[]` |

Wave 1 of t-109: P1, P2, P4, P5 (P3 dropped, decision 2).

### t-109 after critic-on-plan (t-120, 30.09 17:00) — these OVERRIDE the draft and the table above

Verdict: P1, P2, P4 accept with changes; P5 REJECTED as drafted; P7–P10 accept with changes.

- **P5 (B-207) goes back to design** (a new draft under its own task id). Why: `proof_required(entry, manifest)`
  has no project root and no base, and `acceptance.py:224` / `window_record.py:508` call it on window
  items with `{}` — under the drafted default every item a role marked `unchanged` becomes "required"
  (red: `test_acceptance_semantics.py:78-80`, `test_proof_level.py:274-276`,
  `test_controller_release.py:291`, `test_ledger.py:282-286`, owned by no piece) and stories in flight
  are refused over a missing field (builder-rules 9). No piece records the S0 base; with "HEAD now" a
  test committed at delivery reads `unchanged` — the forbidden direction. Novelty without the conftest
  chain and package `__init__` files misses a changed fixture (`execution_fingerprint.py:373-383`
  falls back to the file only when the function is not found). `coverage_contract.py:139-147,
  320-321` is a second predicate on the binding layer. Decisions for the redraft: F3 is REVERSED —
  novelty is read only from a field stored on the row where the row is written; a row without the
  field keeps today's rule with a printed line (stories in flight are not refused); a base that is
  "HEAD now" may give `new` or `changed`, never `unchanged` (it gives `unknown`); a piece that records
  the test repository's base at S0 is named with its owner; the conftest chain and `__init__` files
  are hashed at the base and now; the binding-layer predicate is named and the winner stated. Cost on
  cmp1 measured by the critic: 16 rows move to "needs a live check", "Proven" 24 -> 8, the cause being
  our own unpublished receipts — so P5 and P6 (the unpublished-probe exit) land together.
  **Redraft: `specs/t-134-proof-by-code.md`; critic-on-plan t-136 (17:50): ACCEPT WITH CHANGES.**
  Lead's fork decisions: F-1 legacy unmeasured green tests are a separate group, not counted in
  "Proven" (owner-level, interim); F-2 stored `novelty` has the trust of `critic_verdict` (debt
  line); F-3 code replays, hand oracles go to the critic; F-4 always re-probe; F-5 the existing critic
  rework before gate B — its command to be verified before it is named; F-8 a stale published receipt
  is probe debt too. These changes OVERRIDE the redraft:
  - V1 (P6-A, P6-B; replaces F-7). The settle inside `story_step start` has a WALL-CLOCK budget of
    about 90 s, not a count of 25: one probe may take up to 1860 s and the stand lease may wait
    1800 s, while the skill road runs `start` through a shell call that times out at 120 s. The stand
    is checked once first; the settle stops at the first `not_executed` or busy stand; leftovers go to
    the critic as its work. It sits right after the dispatch is registered (`story_step.py:498`) and
    before the brief is built (:503). The budget test belongs to P6-B's witness (P6-A's probes are
    stubbed).
  - V2 (P5-B, P5-D; replaces F-6 and R2.7's effect). When the base is NOT a recorded S0 base (a story
    in flight, a project without git), `novelty` is written only for `new` or `changed`; a reused
    test gets NO key, so today's rule applies to it and it reads "unmeasured". Otherwise every reused
    test of every such story would need a probe (builder-rules 9).
  - V3 (P5-B, P5-D; FR-55). Measured on this machine: about 0.5 s per git call and 0.66 s per
    `function_sha`; a mirror per test would cost 4–5 s per function. The measurer has `measure_many`:
    ONE `git cat-file --batch` process, one mirror and one parse cache per `manifest_from_tests` call;
    P5-D's DoD carries a time bound.
  - V4 (P5-B). The measured set also holds the pytest config files and the conftests up to the PROJECT
    root (`_conftest_chain` stops at the run's cwd); a fixture living in a `pytest_plugins` module is
    a named residual. The order of "untracked at S0" against "unchanged" is stated.
  - V5 (P5-A). `repo_prefix` comes from `git rev-parse --show-prefix`; the dirty status covers the
    whole repository, not only the tests root; the hook's position in `stage_done.run` relative to
    the refusal at :480-502 is stated.
  - V6 (P6-A). A replay passes `--oracle <file>::<function>` whenever the record has an oracle
    function; it is handed to the critic only when that function is gone. A replay is a FRESH probe
    on the current bytes, valid through the receipt's equality — the spec says so.
  - V7 (P5-E). `delivery_summary.py:315` gives the "unchanged test" words to every not-required row;
    its words move with the ledger's in P5-E, so gate B's summary and the ledger agree (FR-10).
  - V8. "0 role turns" is claimed only as "0 critic probe turns" until the route from a refused
    window to the next critic start is traced. The landing-rule sentence is corrected: P5-E changes
    the WORDS of legacy rows before P5-D lands, on purpose.
  - V9 (owner 30.09 + critic of P5-C, t-145). A row without the `novelty` key keeps today's WORDS
    ("not probed (unchanged test)") and stays in "Proven" on every surface. `unmeasured` survives
    only as a reason code; `proof_level.words_for(reason)` maps it to today's words. P5-E's mutation
    "legacy words equal the unchanged words" is INVERTED (they must be equal); `test_ledger.py:286`
    stays green; R9's invariant is rewritten accordingly; t-109 P7's "Proven" counts rows whose
    reason is `unchanged` or `unmeasured`.
  - V10. `unmeasured_line(manifest)` (R6, R8, R9) is dropped: it would print the group the owner
    declined.
  - V11. Handed rows DO get their own words (`handed_words`) on keyed and keyless rows alike: "not
    probed (unchanged test)" on a case handed to the person is a false statement, and the owner's
    decision was about unmeasured tests, not about handed ones.
  - V12 (landing rule). P5-F (the binding-layer predicate in `coverage_contract.py`) and P5-G land in
    or before P5-D's integration: otherwise `coverage_contract` calls a measured-new test witnessed
    while the ledger says a check is owed (FR-10). `resolved: true` is honoured only on item-form
    novelty blocks (t-161); the debt line for stored-novelty trust (F-2) is still owed.
  Startable now: P5-A (with V5) and P5-C. P5-C's neighbour `test_factory_dashboard_joins.py` runs
  after the dashboard pieces merge.
- **P1 waits for t-108 piece B.** All 13 cmp1 ghosts carry a `not_run` row in the failed block
  `5a24a4a3` (t-108's unconfirmed red); R-208.4/.5 look only at the latest row's `raw_status` and
  would quench them. Change: ONE definition of red — t-108's R5/R5a, imported from `s5_precheck` —
  checked over the identity's whole history; a ghost is quenched or superseded only when its history
  holds no red, or the red is paired in `expectation_changes[]`.
- **P2 runs after P1 and lands with P7** (or prints an interim line): lift to "factory" only when
  every named case has at least one row and no row's history holds a red (needs P1's `raw_status`);
  rows of an old report with no `raw_status` are never lifted; the spec names where the
  requirement -> case and plan row -> case mapping comes from. "The person is told, not asked" must
  exist in the same merge, otherwise the question disappears and nothing tells the person.
- **P4 may start now, with this change to R-206.3 / fork F6.** Case ids are numbered per story
  (`TC_003`–`TC_005` exist in both the 13797 and the 15045 manifests) and `BUG-1.md` has no `task` and
  no case id in its front matter, so "files whose front matter names the task or a case id" would
  count a foreign story's bug and drop or double-count its own. A bug file belongs to the story when
  it lies in the task folder's `bugs/`, or when its front matter `gate_b_decision_id` (required by
  `artifact_producer.py:91`) equals the id of THIS story's gate B record. A project-home file that
  joins to no story's gate B is listed as "unattributed" and not counted. The same bug present in
  both homes (same file name and same `gate_b_decision_id`) is one record. Sibling noted:
  `judge_results.py:265,315` picks the next BUG number from the project home only.
- **P7–P10:** `report_facts` / `stage_done` are added to `references/artifact-writers.json` as
  machinery of `test-report.md` (Lead); a `--write` that replaces bytes someone edited inside a block
  saves them to report-history and prints a line; because the rebuild runs before the check, the
  stale-block refusal is removed from `stage_done`; what stays refusable (an item with no "How:",
  damaged markers) is the factory's own problem — the driver's door is the scribe's rework or a
  printed finding, never a question to the person (FR-3, FR-42); if the rebuild after gate B changes
  the verdict sentence, the block prints the old and the new text.
- For the owner: the definitions of the verdict counts and the order of the "first reason" decide
  what a person reads first — shown to her with the first rendered report, before release.

## Forks of t-113 (open questions) — decisions

| fork | decision |
|---|---|
| F1 answer grammar | strict tokens plus the lenient "one id at the line start, one `(x)`" form |
| F2 a case made automatable by an answer that does not mention it | the variant is applied and the consequence printed (the owner's accepted scheme); a case the person NAMED outside a token goes to the conductor |
| F3 where answers live | code-owned `work/question-answers.jsonl`, joined by `load()` |
| F4 variant shape | a patch with a closed key list in a data file |
| F5 free text at gate A | the gate decision is held until designer and critic finish, then recorded with the same words |
| F6 question cap | every card printed; one sentence in `human-questions.md` that a batch is one decision |
| F7 three answers | a reading letter, `not needed`, own words; "I will find out" = no answer yet, the story waits |
| F8 default thresholds | OWNER (numbers). Interim: more than 6 open questions, or more than 0.34 of the register's requirements resting on open questions; project value in `qa-factory/config.json` |
| F9 owner of B-181 | this spec (decision 2) |
| F10 the cut | Part A (A1–A6), then Part B (B1–B3) |
| F11 scope question reaching gate A | code applies nothing; conductor and the CLI |
| F12 open conditional Then in an automate row | verify the existing `deferred_by_decision:gate-A` door first; if `s5_precheck` refuses it, back to Lead |
| F13 low confidence | a new stop reason, not the existing `confidence` field |
| F14 question raised after gate A | the generic halt road |

A1's `state-exits.md`, `audit_factory.py` and `artifact-writers.json` lines go to Lead (decision 4).

### t-113 after critic-on-plan (t-121, 30.09 17:00) — these OVERRIDE the draft and the table above

Verdict: Part A and Part B accept with changes; six blockers. Measurements M1–M3, M6, M7 re-run by
the critic and hold.

- **Q1 (new piece A0, blocks A4 and A5).** On cmp1 no switch of TS-6/7/9/11 to `automate` can be
  recorded: the designer's dispatch `S4-qa-case-designer-1` has `scope: []`, so `_covers`
  (`controller.py:1087`) falls back to the critic roll-call, the only findings file left (round 2) is
  scoped to TC_005/008/010, and the other cases get design-review author `''` — which
  `_design_review_problems` (:1149) refuses. Root-cause fix is its own piece, backlog B-224: the
  designer's dispatch records its scope (or round-1 roll-calls are kept). A4 and A5 wait for it.
- **Q2 (A1, A2, A4).** `contract.case_ids("TC_009 …")` returns nothing under the project's id form;
  only `TP1-13797_TC_009` is recognised. The gate card prints FULL case ids in every token it
  offers. The parser resolves a short id only when exactly one case id of this story ends with it
  after an underscore; otherwise the words go to the conductor.
- **Q3 (A4, A5).** Order and rollback: (a) `check_decision` on the UNPATCHED state first; (b) the
  design-review check run in memory on the patched rows (`_design_review_problems` takes rows and
  pins as parameters); (c) byte copies of the plan and of the pins are taken before writing and
  restored if `gate-decision` still refuses — without (c) "no substitution without a gate-A record"
  is false; (d) the rehearsal and the card (R7, R8) run the same check, so the card never promises a
  consequence that cannot be recorded. The driver's `revise_plan()` returns early on an unchanged
  scope (`story_run.py:2699`) and its idempotency key would repeat S4's with other inputs
  (`event_store.py:143` refuses that): the new call has its own key, and the person's words go into
  `reason` (today `_after_commit` stamps code's text, `controller.py:908-910`).
- **Q4 (fork F1 CHANGED; A1).** The drafted grammar errs toward applying ("Q3 a scope question…" reads
  Q3=a; "Q1: a question for later" reads Q1=a; "Q1 – not (a)…" reads Q1=a). The grammar is STRICT
  ONLY: `<qid>: <letter>` where the letter is followed by the end of the line or one of `, ; .`;
  `<qid>: not needed`; `<full case id>: manual` / `<full case id>: automate`. No space-separated
  form, no lenient "(x)" form. Ids are case-sensitive. Everything else — including the replayed cmp1
  gate A words — goes to the conductor, which is a role and reads meaning. The card states the form.
- **Q5 (A1).** A1 owns its own data file `references/question-vocabulary.json` (question statuses,
  stop reasons); it does not wait for `handoffs/vocabulary.yaml`.
- **Q6 (R11).** The CLI gains `--keep-manual <full case id>` ("apply the reading's Then, keep the case
  manual"). F5's hold of the gate decision applies only to questions that have variants.
- **Q7 (R6, R9, R13).** An empty reading keeps the Then's number and writes "not asserted (Qn=x)" —
  deleting the item would renumber the Thens and break `## Obligation coverage` and S5's binding.
  R13's door list adds `disputes: derivation` (`s5_precheck.py:1485`).
- **Q8 (B1, B2).** A threshold stop is recorded in DRIVER state, not in the role's file; an answer
  given at a threshold stop is the informed pass — the same count does not stop again, only a larger
  one; the resume has its own text (not "continue from where you stopped" to a role that had
  finished).
- **Q9 (B3, A6).** Readers of `verdict: blocked` that B3 owns: `validate_artifacts.py:143`, the
  requirements-tester ahead card, `phases/s2.md:62-128`. The four cards are at 1188, 1147, 1074 and
  1077 B of 1,200: the boundary and branch text goes into the roles' contract documents (the slices),
  a card gets one REPLACED sentence.
- **Q10 (t-109 joins).** `question_register.load()` also returns `line` (the line of the person's
  words carrying the id) and `where` with the values gate A, gate B, S2 stop, S3 stop, waiver, remark,
  conductor. `named` (an old story: the id stands in the recorded words, no answer record) is shown
  in the report's open-questions list with the note "named in your gate A words; the factory recorded
  no answer" — never as answered. The "answered at gate A" suffix is attached for `answered` only.
  Ids are matched exactly and case-sensitively in both specs; aliases (`Q-R14`) resolve nowhere.
- **Q11 (owners).** A6 is serial behind t-108 piece C (`ahead-cards.json`). No builder regenerates
  the slices: `contract_slices.py --write` touches every role's slices, so Lead runs it at
  integration. The patch-key data file belongs to A3; the writer of `questions_answered` to A5; A4
  imports the controller's design-review check read-only (if that is impossible it reports, it does
  not edit `controller.py`).
- **Q12 (carrier cost).** A variant patch that replaces the whole `coverage_obligations` costs about
  1.6–1.8 KB per row per reading (13–16 KB on cmp1's 47 KB plan). When every reading gives the same
  patch, it is written ONCE under the key `*`; per-reading Thens live only in the case.
- **OWNER (fork F2).** Her own backlog row reads cmp1's "as they stand — no edits" as "the cases
  stayed manual by the person's word", and code cannot read that sentence. Interim: a reading chosen
  by a strict token applies its variant; a case stays manual only by the token `<full case id>:
  manual`; any other wording goes to the conductor.

Startable now: A1 (with Q2, Q4, Q5, Q10). Then A3 and B1; A2 after A1; A4, A5 after A0, A1, A3.

## Forks of t-114 (S1 gap points) — decisions

| fork | decision |
|---|---|
| F1 passing an uninspected source on a person's word | `accept-gap --point source:not_inspected` only after the person is shown it; stored as factory-owned; a finding is filed |
| F2 free-word answer | numbered closed answers read by code; prose goes to the conductor, which picks the ids |
| F3 the inspection receipt | stays `assess --relevance relevant` after `collect`, stated to the role; a separate `inspect --source-id` is a debt line |
| F4 accepted points across a revision | gap-class points persist by id; work-class points lapse |
| F5 stories past S1 under the old rule | re-blocked at every reader, doors named |
| F6 the three manifest keys | dropped from the charter; coverage readiness derived from v2 `coverage_search`; old keys still read when present |
| F7 way out of an accepted point | a state-exits row naming the natural exits; `--revoke` is a backlog row |
| F8 legacy words-only acceptance | closes open gap-class points only |
| F9 points per question | 15 |
| F10 `context_bundle` inventory branch | backlog row |

Measurement M2 of the draft (today's verdict on the cmp1 inventory) was run by the critic t-122:
`gate_blocked False, complete False, incomplete [], unavailable_materials [], accepted_gaps
[SRC-606b…, SRC-a9a37…]`; M1–M5 all as the draft says; M6: `source_inventory.py` last changed 26.09
(fd9584f), so the code did not change between driver3 and cmp1.

### t-114 after critic-on-plan (t-122, 30.09 17:00) — these OVERRIDE the draft and the table above

Verdict: ACCEPT WITH CHANGES; four blockers for P1.

- **G1 (R1, invariant I3).** The old `completeness()` never reads media ITEMS, only the block status
  (probe: block `pending` with one `unavailable` item gives `incomplete_materials [SRC-x]`,
  `unavailable_materials []`). Media points are created only when the block is `unavailable` or
  `partial`. "An item that explains the block" = an item whose own status is `unavailable`,
  `partial` or `skipped`. The escaped and unescaped spellings of one URL are ONE point; it is open if
  any of its spellings is open.
- **G2 (new, in P1).** `collect_jira_source:445` reuses a source only when it is `complete`, so every
  source with an open or accepted gap is re-collected on each `refresh` (ordered before gate A,
  `phases/s1.md:229`), which resets the inspection receipt (:525) and every media item (:530-534) —
  under the new rule gate A would re-block each time. On an UNCHANGED revision whose files verify,
  the source is reused and its inspection and media receipts are carried over, whatever
  `completeness` says.
- **G3 (fork F5 CHANGED).** The legacy re-block would reach every S5+ dispatch
  (`controller.py:2262 -> 1862`, also :806, :825) with a refusal that names no door, and every door
  would force gate A to be decided again. A story whose S1 is already `completed` keeps the OLD
  meaning of its recorded acceptance (nothing re-blocks; builder-rules 9); `completeness` prints one
  line "S1 closed under the earlier acceptance rule: <sources> not inspected". The new rule applies
  to stories whose S1 is not completed. `controller.py` stays a non-goal.
- **G4 (fork F1 made real).** Accepting a work-class point (`--point source:not_inspected`) REQUIRES
  `--shown-text "<the sentence the person was shown>"`; without it the CLI refuses and says so. The
  text is stored with the point (`shown_text`), and the point is `factory_owned: true`. Gate A prints
  such points under the factory's own findings ("passed on your word: <source> was not inspected") —
  piece P5. The driver's finding line (R17) carries the `--ref` that `log_append.py:46` requires.
- **G5 (R14, R16).** The three ANSWERS are lettered (a, b, c), the POINTS numbered — today's answers
  are numbered 1/2/3, so "2" would accept point 2. One grammar with t-113: strict tokens only;
  anything else goes to the conductor.
- **G6 (R16, R4).** Before recording, the driver intersects the ids it showed with the ids still
  open; `record_gap_acceptance` with `points` accepts the open ones and prints the ones that are no
  longer open — it does not refuse the whole call.
- **G7 (answer battery, expected outcomes).** `0`, `16` of 15, `1-3` -> nothing is accepted by code,
  the words go to the conductor; `1,1` -> point 1 once; a BOM is stripped before reading.
- **G8 (fork F9 CHANGED).** No cap: every open point is printed (as t-113 prints every card).
- **G9 (R5).** A legacy `"materials unavailable: <names>"` string closes a point by name only when
  that name is unique within the source.
- **G10 (R10).** The receipt command names the role's reading note as `--assessment-ref` (the file
  where it wrote what it read), not the snapshot itself. The debt line is Lead's.
- **G11 (R13).** `agents/qa-scout.md` is 9,005 B and the per-file cap is a warning (audit A25
  governs): new sentences REPLACE old ones, the file does not grow.
- **G12 (R21).** Coverage readiness from `coverage_search` needs at least one row with status
  `complete`.
- **G13.** R9 (the state-exits rows) moves to "Needed from integration".
- **OWNER.** The form of the S1 gap question (numbered points, lettered answers) is shown to her as
  rendered text before release.

## Forks of t-137 (the true price of a task: B-225, B-226) — decisions

Spec: `specs/t-137-task-price.md` (the designer's draft, copied verbatim; its own title says t-136 —
the task id is t-137). Lead ran its measurement M1 on cmp1 (30.09 18:01): re-priced at the catalogue
rate the 35 cost files give $16.6491 against the driver's $17.4241; 19 sessions agree to four
decimals, 16 differ and in every one the cost file is LOWER, $0.775 in all — the cost file stops
before the session ended (session `1338701d`: 1 request captured of 6). So cmp1 has TWO defects of
the price record: the project's price table (B-225) and a capture that misses the tail of a session
(backlog B-228).

| fork | decision |
|---|---|
| F1 which rates are the truth when a project has contract prices | OWNER. Interim: checked and shown at the catalogue's list price (no project has contract prices today; cmp1's table says "list prices") |
| F2 what is shown when the two records differ | OWNER 30.09 18:10: the price is STILL printed — as a RANGE (the lower and the higher of the two records) with the note that the sources differ, plus the finding in plain words (which sessions, by how much) and two columns by agent. The price is sometimes the most important fact of a run and must not be lost. Replaces the draft's R8 "price not established" and `price_usd: None` when `differs`: `task_price` returns `price_low_usd` and `price_high_usd` (equal when the records agree), never a single figure presented as exact while they differ |
| F3 a story run by the orchestrator in chat (no second record) | OWNER. Interim: the one-record price, labelled "not cross-checked" |
| F4 which chat requests belong to a task | OWNER. Interim: the prompt turns that contain a `story_run.py --task T` call; the rest of that chat is shown as "chat, not attributed to a task" |
| F5 remote agent calls with no receipt | a row "cost unknown"; the price says it covers the model sessions |
| F6 tolerance | $0.001 per session; a story agrees only if every comparable session agrees — confirmed by the critic's M2 / M9 before the build |
| F7 where record A comes from | complete cost files, re-priced at read |
| F8 rule texts | FR-24 and FR-25 are reworded by Lead at integration (mechanism commit) |
| F9 a session priced by one record only | counted in the price and listed "not cross-checked" |
| F10 a family rate for a model the catalogue lacks | used and labelled |
| F11 `retro.md` carries money and lives in the task folder | OWNER (she said money does not belong in the repository) |
| F12 the budget ceiling's figure | per session the larger of the two records |
| F13 the driver records who launched it | after measurement M7 |
| F14 root-cause fix of the missed tail | after measurement M6 (B-228) |

OWNER 30.09 18:12 on the four open forks: F3 — yes, a one-record price labelled "not cross-checked";
F4 — yes, only the chat turns that launched the task's driver, "and we check it in practice" (the
next live run is the proof); F11 — `retro.md` IS committed and keeps its money ("for a retro that is
normal"; the rule "no money in the repository" is about the test report); F1 — there is always ONE
price: onboarding says it takes the models' default prices (the catalogue) and the person may correct
them if they want (for example, prices changed). So a project rate exists only as a person's explicit
correction of a named model (`rate_overrides`), never as a family table; when it exists it IS the
price, and the comparison with the CLI's charge then shows a range and says the project's prices
differ from the CLI's list prices. Onboarding gains the sentence and the question (piece Q7).

### t-137 after critic-on-plan (t-146, 30.09 18:50) — these OVERRIDE the draft

Verdict: ACCEPT WITH CHANGES. Premise confirmed on cmp1: transcripts at catalogue rates equal the
CLI's charge for all 35 sessions within $0.00005; cheapest request $0.0105 (tolerance $0.001 holds);
the 16 differing cost files end before the transcript; recapture on a copy gives A = B = $17.4241.

- **P1 (Q2, R3).** "Size exceeds the checkpoint offset" flags all 35 sessions (Claude Code writes
  `stop_hook_summary`, `last-prompt`, `cost-state` lines after the Stop capture). A file is stale only
  when the bytes past the offset hold an `assistant` record carrying usage. Test: a tail of only
  `stop_hook_summary` is NOT flagged. Recapture must honour the metric-signals skip flag.
- **P2 (Q1, R2).** A collapsed file with ONE `by_task` key gets the exact session total; None only
  with more than one key (33 of 35 cmp1 files are single-key). In Q1's dispatch (t-153).
- **P3 (Q3, R7, section 3).** A journal row with an empty session id sets status `incomplete` (its
  money is in neither record); the page says what was compared ("the CLI's own charge for the N
  sessions the driver's journal names; K from one record"); the word "attribution" leaves section 3;
  E7's claim about a crashed call is dropped.
- **P4 (Q4, R10).** Only the `story_run.py` invocation's own arguments bind a turn (not a `grep` of
  the text, not another command's `--task`); `--dry-run` excluded; a person's prompt is a user record
  with no `origin` and no `isMeta` (a background task's notification is NOT a prompt, so the turn that
  relays the driver's question stays in the task). Same root queued: `human_wait` at
  `cost_capture.py:405` counts notifications as the person's waiting time.
- **P5 (Q7, R13).** Answer (a) must not be re-asked: (a) removes the shadowing keys. In t-154.
- **P6 (Q6, R12; replaces Lead's F12).** The ceiling polices B where known, else A; when the two
  differ the notice says the figure is disputed. A double count in A must not stop a story (P1 of the
  owner's principles).
- **P7 (Q3, dashboard P2).** Ticket rows are labelled `qa-scout` by ONE helper in `driver_journal`
  used by both the dashboard and `task_price`; the draft's `<agent> (remote)` row for data fetching
  goes under the scout too (owner).
- **P8.** E15 is corrected (after Q1 new captures are at the catalogue rate while old pinned figures
  stay until the readers re-price); Q9 bumps the formula version of the money metrics; Q8 (friction
  on the list rate) is scheduled, not conditional.

Running: Q1 = t-153, Q7 = t-154. Then Q2 (same file as Q1), Q3, Q8.

Owner's later answer applied to the draft: a session of kind `ticket` and every other data-fetching
call is grouped under the SCOUT's row (the draft's E11 gives it a row of its own).

## Owner answers (30.09, about 17:40)

- **Bug home (t-109 F5).** Bugs live in the PROJECT's `qa-factory/bugs/`: they are not pushed together
  with the tests — in real projects bugs are filed separately; only an experiment sometimes pushes
  them. Consequences: the reporter writing `BUG-1.md` into the task folder in cmp1 was a defect of the
  factory's texts (`design/factory-rules.md:289-292` names the task root; the reporter's charter,
  `references/stages.json:237` and the path table name the project home — the rule text is the one to
  correct); `bug_records.story_bugs` fills `outside_home` with records found ONLY in the task folder;
  the report says where each bug file is.
- **New report sections (F10, F18).** Yes — provided a section does not repeat what the report already
  says elsewhere. "Decided at gate A" and "Open questions" carry only what no other section holds; an
  empty one is not printed as a heading with "none" when another section already says it.
- **Size "Fact" (F12).** Counts only. Money does not belong in a file that lives in the repository:
  prices change. It stays in the retro.
- **Thresholds for "stop and ask" (t-113 F8).** Either condition stops: more than 6 open questions OR
  more than a third of the requirements resting on open questions. Onboarding proposes these numbers
  as the default and ASKS whether the project wants others; the project's numbers live in its config.
  (New piece in t-113 Part B: the onboarding question.)
- **Management vs a role's work (t-111 F5).** Choosing a role and handing it something to redo is the
  conductor's management. The extra work the role then does is the ROLE's cost. So: the orchestrator's
  share is the conductor's own sessions (plus code, which costs nothing); a role resumed after a
  question is role spend. The retro's "Control layer" line, which adds resumed roles to the conductor
  (72.6% on cmp1), contradicts this: it becomes "conductor" only, and the money of resumed roles is
  shown as its own line of role spend ("rework the conductor handed back"). This is a follow-up piece
  on `retro_numbers.py` after P3 (it replaces B-184's arithmetic for that line).

- **The price of a task (t-111 F2 is REPLACED; principle P18 in PROJECT.md).** There is no choice of
  "which record leads". The task's price on the dashboard and in the retro must be TRUE — it includes
  the roles, the conductor, the answers given to the person in chat, the calls of agents (Jira and
  others) — and it must EQUAL the sum of the costs by agent. That equality, computed from two
  independent sources, is the check of our arithmetic; a gap is a defect to fix, never a caption under
  a wrong number. Consequences: B-225 (the project's family price table overriding the catalogue's
  exact rate) is fixed NOW, not shown; the interim "cost-file figure + gap sentence" of R7 becomes
  "the two sums, and a finding when they differ"; the S0 ticket call and the person's chat sessions
  are part of the task's price and have their own rows by agent; how a chat session is attributed to
  a task by evidence (not by a mere mention of the ticket — the $1,911 lesson behind FR-24) is
  designed in the spec for B-225/B-226 (t-136).

- **Data fetching is the scout's cost (answers "is the ticket call part of the orchestrator").** The
  S0 ticket call, and every other call that fetches tickets or materials — the scout asks for several
  tickets to decide whether they are needed — is counted as the SCOUT's spend, not the orchestrator's
  and not a row of its own. In the dashboard and the retro a journal row of kind `ticket` is grouped
  under the scout (t-111 C3 is changed accordingly; goes into the design t-137 and the dashboard
  piece P2).
- **A case an answer makes automatable (t-113 F2) — principle P19.** Neither "automated by default"
  nor "manual by default": the case goes through the ladder again, bottom of the pyramid first —
  API or component test; else e2e (extend a fitting existing e2e check or write a new one); else, when
  automation is impossible or not needed (not regression), an AGENT checks it by hand and shows the
  person before / after; else, when the judgment is subjective or a person judges it faster and
  cheaper, a person by hand; and a test that can be automated but cannot run on this environment is
  written and a person runs it elsewhere. For t-113: after the answer the case enters S5 and the
  automator walks the ladder and records its rung and reason; code checks that a rung and a reason
  are recorded (completeness), the code critic judges the choice. The tokens `<case>: manual` /
  `<case>: automate` stay as the person's explicit word (P13). Whether every rung has an executor
  today (rungs 3 and 5 in particular) is backlog B-227.
- **Onboarding may run a collect of the project's tests** (it already reads all the tests to derive
  the project's code patterns and rules).

## State at 18:45 (30.09) — supersedes the running table of "State at 18:12"

Accepted since 18:12 (journal): t-124 dashboard P1 (critic: accept with changes), t-116 + t-117 B-194
A and B (critic: accept with changes), t-132 B-172 P1 (critic: two must-fix — does NOT merge without
t-151), t-135 launch check follow-up (593/593), t-138 retro follow-up (177/177), t-141 B-194 D
(137/137). The last three get their critic pass as the topic pass at integration.

Running:

| task | what |
|---|---|
| t-149 (builder) | B-194 fixes after the critic: inline `--fragment`, tag-scoped word, three silent passes, verdict dropped on an author rewrite, detector moved to `scripts/run_history.py` (re-exported from `s5_precheck`), subset match for a verdict patch, long path, piece D's fork (owed + unmeasured = FALSE) |
| t-150 (builder) | dashboard P1 fixes: `root_charged` once in `main`, ticket sessions under the scout, one priced set, floor sentence, small items |
| t-151 (builder) | B-172 P1 fixes: `s1_closed` wired at `controller.source_inputs` / `project`, legacy record kept through migration, legacy name split, `original_ref` in ids, MR text, refresh, dead `open_points` |
| t-127 (critic) | B-193 P2 command precedent (handed over 18:38, 210/210) |
| t-142, t-143 (builders) | B-194 E (critic brief), F (acceptance gate; also switches `acceptance.py` `_run_blocks` per critic F7) |
| t-144, t-145 (builders) | B-207 P5-A, P5-C |
| t-146 (critic) | plan of the true price; then Q1 and Q7 |
| t-147, t-148 (builders) | question register and config guard follow-ups |

Handed over, NOT accepted: t-140 B-194 C (texts; `test_ahead_cards` 230/231). Needs from Lead:
(1) `references/role-commands.json` — `qa-code-critic` added to the roles of `manifest_put.py --fragment`;
(2) audit A22 (injection cap 42,000 B, 1,000 B headroom): after slices are regenerated the critic is
at 42,525 and the automator at 42,085. Lead's decision: no cap raise — the `review_receipt_ref`
paragraph (about 1,046 B) becomes critic-only and the duplicated `disputes` sentence in "What is
checked" goes; done as one small builder piece AFTER piece E lands (E also edits `qa-code-critic.md`),
then slices regenerated once.

Lead decisions of this batch: golden page — the piece that changes the page re-cuts the golden and
states the diff; module home of the detector — `run_history.py`; verdict patch — subset of exactly
one record with the same attempts; launch check — the interpreter guard stays, `--scope local-urgent`.

Queued (no owner yet): sibling readers of run-block order (`probe_by_code`, `proof_level`,
`retro_numbers`, `finalize_task`, the open-oracle `triage.json` text); SIBLING_MAP axis 7 row for the
new `function_sha` reader; `retro_numbers.driver_rows` sums raw row totals (increments); S5 builds
`pytest -m` for `-m <test-id>`; `project_decisions.resolve` cannot set a pointer through a list
index; `execution_request.ran_before` treats any `completed` job as having run; the no-verdict reason
of a handoff claim does not reach a role on the `--json` path; B-172 interim debt line (until P3 the
conductor's acceptance closes partial merge requests); `test_orchestrator_share` still pins the old
`control_layer()`.

## Owner questions

All six questions of 30.09 (price shown first, resumed roles, bug home, new report sections, size
"Fact", thresholds) are answered — see "Owner answers". t-134 F-1, OWNER 30.09 (after 18:45): green
tests whose novelty was not measured (stories begun before the fix, projects without git) ARE
COUNTED AS PROVEN — "soon there will be none, everyone will update the factory". This REVERSES Lead's
interim F-1 (a separate group outside "Proven"): no separate group; a row without the `novelty` key
keeps today's rule and today's place in "Proven". Goes into the dispatches of P5-D / P5-E (words of
legacy rows) and the report pieces; check t-145's hand-over (P5-C predicate) against it. To show before release, not questions yet:
the rendered S1 gap question form; the verdict-count definitions with the first rendered report.
