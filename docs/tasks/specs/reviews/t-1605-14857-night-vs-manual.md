# t-1605 — TP1-14857: the night driver run (0.10.6 + t-1603) against the owner's manual run (0.10.5)

Critic (Opus), 30.10.2026. Read-only: nothing in the stand was written or run. Times are local (UTC+1) unless they say UTC.
Reused, not redone: t-1597 (manual run time sinks), t-1598 (manual gate A answers lost), t-1602/t-1604 (the night blocker and its fix).
Scripts that produced the numbers are in the Appendix (scratchpad `.../scratchpad/t1605/*.py`, run with `python -I`).

Carriers, short names used below:
- **MA** = `D:/ws1/archive\testproject1-dev-010-run-14857-20261030\` (manual run archive; `artifacts-TP1-14857\`, `cost-moved\`, `state-full\`).
- **NA** = `D:/ws1/testproject1-dev-010\testproject1-sdk\test-harness\qa-factory\artifacts\TP1-14857\` (night run, live).
- **SC** = `D:/ws1/testproject1-dev-010\testproject1-sdk\test-harness\qa-factory\state\cost\` (cost files).
- **NB** = `experiments/run-14857/run-14857.md` (night notebook); **RL-n** = `experiments/run-14857/runs/r14857-n.log`.
- **PKG** = `D:/ws1/run-14857-pkg\qa-factory\` (the frozen 0.10.6 copy the night ran).

One correction to the dispatch: the manual run did not stop at gate B. Its `pipeline.json` has S0–S9 `done` and gates A, B
`approved` (MA `artifacts-TP1-14857/pipeline.json`), and t-1597 §1.1 shows gate B 00:24:57–00:27:47 UTC and S9 to 00:36:28 UTC.
It finished with no MR, as the night did.

## 1. Side by side

| Measure | Manual (0.10.5, conductor in an interactive session) | Night (0.10.6 + t-1603, `story_run.py` headless) | Carrier |
|---|---|---|---|
| Wall, whole run | 5 h 50 min (19:46:32 → 01:36:28) | 4 h 46 min (01:57 → 06:43) | t-1597 §0; NB «Итог»; RL-16 last line 06:42:58 |
| S1 | 33.6 min (person 17.4) | 27.8 min (scout session 21.5 min) | t-1597 §1.1; stages.py over NA `state/events.jsonl` |
| S2 | 5.0 | 5.5 | same |
| S3 | 28.3 | 23.0 | same |
| S4 | 27.1 | 6.8 | same |
| gate A | 25.7 (4× gate-decision, person 11.5) | ≈5 (03:03 → 03:08, 3 asks) | t-1597; driver-questions.jsonl rows 3–5, driver-answers row 3 |
| S5 (incl. gate A in the night figure) | 188.2 | 144.9 (03:00 → 05:25; ≈31 min of it stood on the t-1602 blocker, 04:47 → 05:18) | same; NB |
| S6 | 11.1 (runner ran nothing) | 16.1 | same |
| S7 | 3.4 (code only) | 19.3 (includes an S5 automator on TC-002, 05:48–06:00, finding 7) | same; RL-11:17-36 |
| S8 + gate B | 11.3 + 2.8 | 4.3 + ≈3 (gate B asked twice) | same |
| S9 | 8.7 | ≈38 (06:05 → 06:43; 7 retro analysts, finding 8) | RL-15, RL-16 |
| Cost | **$22.34** for the session (`priced_subtotal_usd` 22.3358521; `by_task` TP1-14857 $22.22) | **$15.63** (36 sessions, sum of cost files = sum of per-session max in `driver-runs.jsonl`, both 15.626) | cost.py over MA `cost-moved/54dd49d9…json`; night.py over SC; runs.py over NA `state/driver-runs.jsonl` |
| Cost by stage | not split (one conductor session; `by_activity` has one story activity + `unclassified`) | S1 1.44 · S2 0.61 · S3 3.02 · S4 1.17 · S5 6.00 · S6 0.33 · S7 0.62 · S8 0.63 · S9 1.81 | runs.py (per-session max, keyed by the session's stage) |
| Naive sum of `driver-runs.jsonl` rows | — | $28.74 (resumed rows carry the cumulative session cost; documented in PKG `scripts/driver_journal.py:9`, not a defect) | runs.py |
| Output tokens | 420,848 | 382,786 | cost.py / night.py |
| Cache write | 3,094,677 (5m 2,737,333 + 1h 357,344) | 2,183,610 (1h only) | same |
| Cache read | 98,517,196 of 102.03M total (96.6 %) | 30,619,691 of 33.19M total (92.3 %) | same |
| Questions to the person | ≈11 person messages (t-1597 §1.2), of which ≈6 factory-caused | 15 questions (`driver-questions.jsonl`): s1_review, s1_gap, gate A ×3, repair_limit, conductor, refusal ×3 (S5), gate B ×2, report_match, retro, refusal (S9) | t-1597 §1.2; NA `state/driver-questions.jsonl` |
| Re-asks of the same thing | gate A: `approve` refused → `approve as is` (1); OB-3 hash passed by word (1) | gate A 2 re-asks, gate B 1 re-ask, s1_gap after s1_review answered it (1), critic-4 receipt 3 asks | same; findings 5, 12, 1 |
| Person time | 72.9 min (≈60 factory-caused) | ≈50 min of operator turnaround (q→a deltas), 27 of them the t-1602/t-1603 repair | t-1597 §1.1; driver-questions vs driver-answers ts |
| Requirements in the register | 11 (R-1…R-11) | 9 (R-1…R-9) | `work/requirements-register.md` both |
| Plan rows | 4 (3 automate, 1 skip) | 6 (3 automate, 3 skip) | `test-plan.md` both; `work/ledger.md` both |
| Cases | 3: TC-001 api code-datasource stamp; TC-002 api other base-processor type (R-5); TC-003 UI details view | 3: TC-001 api manual reindex stamp; TC-002 e2e-ui details page; TC-003 api scheduled reindex (R-5) | `work/test-cases/cases/*/cv_*.md` titles |
| Test files | 2 new (`test_datasource_last_indexed.py`, `…_details.py`) + 2 changed (page object, `datasource_utils.py`) | 2 new (`tests/assistant/datasource/test_code_datasource_reindex_last_indexed.py`, `tests/ui/datasource/…`) + 3 changed (+ `tests/scheduler/test_scheduler_service.py`) | MA `worktree-untracked/`, `worktree-tracked-tests.diff`; `git -C …/testproject1-sdk status --porcelain -- test-harness` |
| Test outcomes | 3 of 3 green and proven (TS-1, TS-2, TS-4 `passed_green`) | 0 proven: TS-1 `not_executed:contradicts_requirement` (TC-001), TS-2 `passed_green` but critic `rejected` (TC-002), TS-4 `failed:ENV_ISSUE` (TC-003) | `work/ledger.md` both; NA `test-report.md:18-22` |
| Report verdict | `delivery_ready: no` — "4 on the product side that no single requirement explains"; 7 of 11 proven, 0 not proven, 4 deferred | `delivery_ready: no` — "12 on the product side …; 2 waiting …; 2 factory bookkeeping"; 0 of 9 proven, 4 not proven, 2 waiting, 3 deferred | `test-report.md:7-10` both |
| Product bugs | 0 | 0 | same, section «Product bugs» |
| Open questions in the report | 2 (Q1, Q2 "recorded no answer", t-1598) | 1 (Q3, "factory recorded no answer") + 2 left with the person | same, section «Open questions» |

## 2. Quality differences

**Requirements.** Manual S1 halted on the trigger-vs-completion conflict and the person settled it (R-6, R-7 are "person's S1
decision"); the night's scout read the dev comment and settled it without a question (night R-2 "trigger time (dev comment,
implementation, ETC-4)"). Night is better on the S1 stop (roles-context finding of 29.10 did not recur), and its register names
three diff-only behaviours (R-7 creation does not stamp, R-8 provider progress, R-9 failed reindex still stamps) as Q3. Manual had
R-10 (SVN) and R-11 (targeted UPDATE, no `update_date` bump) that the night folded into R-6 or dropped. Not a defect either way:
two readings of the same ticket by two scouts.

**Plan / coverage.** Night lost R-7 (TS-5) and R-8/R-9 (TS-6) because Q3 had no lettered answer: every branch of
"per Q3: a -> …; b -> skip; not needed -> skip" resolved to skip (NA `work/ledger.md` TS-5, TS-6; `test-report.md:82-83,240-241`).
That is a factory defect (finding 6), not run noise: the answer existed as words. Manual's TC-002 (another base-processor type for
R-5) went green on the stand; the night chose the scheduler flow for R-5 (TC-003), which this stand cannot run (no scheduler service,
NA `work/triage.json` TC-003 `our_signal`) — the factory learned that only at S7 (finding 15).

**Test code.** Night TC-002 was written against page-object methods that did not exist (critic-4 F-1, NA
`work/test-code/critic-findings.md:13`); the author never saw the AttributeError because its own run died in fixture setup. The
critic caught it statically — the review works. Night TC-001's Then compares the server's stamp with the host's `t_after_1` with no
tolerance; a 2.3 ms excess became `contradicts_requirement` (finding 14). Manual TC-001 hit the project's pytest-timeout and the
person dictated `timeout(900)` + `files_filter` (t-1597 sink 2); the night re-hit the same slow indexing at the default 180 s wait
(finding 16).

**Report.** Manual: OB-3 hash mismatch passed by the person's word (t-1597 N1, known), Q1/Q2 lost (t-1598, known), verdict "not
ready" although every requirement was proven or deferred by the person (finding 24). Night: 0 proven; TC-002 "pass" in the appendix
next to "rejected by the code critic" and "the critic's remarks were not recorded" (finding 7); the appendix marker inside the
regression block made S9 loop (finding 8); gate A words printed twice (finding 23).

Factory defect vs run noise: the scenario choice for R-5 and the R-10/R-11 split are noise (role judgment); the 2.3 ms red, the
skipped Q3 rows, the S9 loop, the TC-002 contradiction and the gate re-asks are factory defects (findings below).

## 3. Finding list

Dedup method: `grep -ril -E "<pattern>" plans/piles/*/findings/*.md plans/piles/*/batch-*.md` (case-insensitive, extended).
Positive control of this exact form: pattern `s1_gap` returned 8 files (`conductor/findings/20261016-tekst-s1-gap-pokazyvaet-imya-skripta.md`
among them); pattern `cache_read|чтени[ея] кэша` returned 8. "new" below means the named grep returned no file about this defect.

| # | Title (factory class) | Evidence | Run | Sev. | Pile | Dedup |
|---|---|---|---|---|---|---|
| 1 | A review that rejects a test gets no window receipt, so the window can neither close nor go back to its author | t-1602 review; RL-8 `window_record.py:923-934` refusal; fix `b7b9d728` (t-1603), its queue t-1604 F3–F5 | night | blocker (fixed on main, unreleased) | driver-controller | recorded only in the t-1602/t-1604 reviews and NB; no pile file (grep `send-back\|sent back\|возвращено автору\|stand-blocked` → 0). F3 (end-to-end proof) and F4/F5 need a finding row |
| 2 | With a critic dispatch still open, a rejected S5 window has no repair move: `finish --not-complete` ("no role left to close S5"), `checkpoint` ("host worker still active"), `rework` ("active dispatch") are all refused | RL-10; NB 05:22; NA `state/driver-state.json` `window_rounds["S5\|TC-002"]` 04:19:23 `cap` | night (and 12586 on 29.10) | major (worked around by `go on`) | hotfix-12586 → wherever HF8-15 lands | **known**: `hotfix-12586/findings/20261029-dirizhyor-zhdyot-uzhe-vernuvshegosya-kritika.md` item 2 (HF8-15, status `ожидает`, was P1 for 0.10.6 and did not ship). Night = second instance, on the driver road |
| 3 | The window's rework cap is spent by conductor rounds on a refusal that is the factory's own (missing receipt), so the first real author round meets "cap of 2 rounds is spent" | NA `state/driver-state.json` `window_rounds["S5\|TC-002"]`: 03:46:03 and 03:50:24 `to_conductor` on "the qa-code-critic window is not receipted", 04:19:23 `cap`; PKG `story_run.py:5586-5629` (`window_round_gate`, cap per window key, `story_run.py:5572-5584`). **Correction to NB**: the cap is per window, not per stage; what is wrong is what it counts | night | major | driver-controller | new (grep `cap of 2\|repair_limit\|кап раунд\|кап.*окн\|per window` → only C3-2/C3-6 rows about round journaling, not this) |
| 4 | The S5 repair cap counts rounds that carry no `test_defect`, against the package's own rule "only a repair whose cause is test_defect spends the cap of two"; the person is then offered a `round` that cannot fix tooling/environment | RL-6:64-76 (03:26:49 "For TC-001, TC-003: the critic sent the tests back 2 times … used up"); critic causes in transcripts `c7f0b25a` (F-1 mechanical, F-2 environment, F-3 tooling), `4f6371e3` (mechanical/tooling/environment), `18e69b0b` (tooling, tooling, environment); rule: PKG `references/config-keys.json` `dispatch_windows_note`, `controller.py:204-209`. Root not traced; candidate: an absent cause reads as `test_defect` (`controller.py:208-209`) while the critics' handoff YAML still holds the template line (`work/handoffs/S5-qa-code-critic-1.yaml:88`) and the causes live only in `critic-findings.md` | night | major | driver-controller (or test-code-quality) | new (grep `cap of 2\|repair_limit\|…` as in 3; the TP1-15045 origin of the rule is in the code comment, not a finding) |
| 5 | A gate answer that starts with `approve` and then answers the items in the packet's own forms is not recorded: unread item lines send the WHOLE answer to the conductor, who can only offer `approve` again; `approve as is` works on the conductor road and not on the driver road | RL-4:8 "9 line(s) of the answer look like a stand-gap answer and could not be read; the answer goes to the conductor: vcs-1: go on on this branch; case_environment-1: accept the gap; …"; RL-5 (`approve as is` refused); RL-12 (gate B: "delivery-1: deliver with known gaps" unread → second ask); design says "approval only by the token `approve` on the first non-empty line" (`conductor/batch-1-p22-seams.md:108,143`); manual: t-1597 sink 11 | both | major | gates-and-words | **known class**: `gates-and-words/findings/20261028-gejt-a-pyat-form-otveta-v-odnom-pakete.md` (which words code reads, P2). The mechanism (unread item lines demote a leading `approve`; two roads, two closed words, AR-15) is new (grep `stand-gap answer\|look like a stand`, `vcs-1`, `accept the gap`, `approve as is` → 0) |
| 6 | A free-text answer to a register question at a gate has no reader on the driver road: the plan's conditional rows all resolve to skip and the report prints the raw branch text | NA `work/question-answers.jsonl` holds Q1, Q2 only; gate A words `state/words/driver-gateA-1793326086985.txt` hold "Q3: not confirmed by the owner - keep … open gaps"; NA `test-report.md:71-78` Q3 "recorded no answer"; ledger TS-5 `skipped:per Q3: a -> automate api …; b -> skip; not needed -> skip` | night | major (R-7 lost) | gates-and-words (+ TQ1-20 for the branch text) | sibling of `driver-controller/findings/20261030-doroga-dirizhyora-ne-zapisyvaet-otvety-cheloveka-na-voprosy-gejta.md` (conductor road, lettered answers); branch accounting known as TQ1-20 (`test-code-quality/findings/20261029-skvoznoj-uchyot-vetok-ot-s2-do-otchyota.md`). The driver-road free-text instance is new |
| 7 | A test the critic rejected is repaired after S7 by a fresh S5 automator and accepted with no re-review; the report then counts it `pass` in the appendix while saying "rejected by the code critic" and "the critic's remarks were not recorded" although they were | RL-11:27-36 (`S5-qa-automator-5 scope=TC-002` during S7, accepted, then S8); NA `test-report.md:42,203,232,235`; remarks exist: NA `work/test-code/critic-findings.md:13` (F-1 test_defect) | night | major | report-delivery (report) + driver-controller (dispatch without review) | new (grep `remarks`, `rejected by the code critic`, `без повторного ревью\|without re-review\|no re-review` → nothing about this) |
| 8 | A known refusal row whose action cannot fix the cause loops with no bound: S9 `report_check → rebuild_report` re-dispatched the retro analyst 7 times after S9 was already accepted, then asked the person a refusal marked "not for the person" | RL-15:16-97 (7 cycles, "S9 is already accepted by the controller"); runs.py: S9 7 sessions $1.805, 05:17–05:40 UTC; cause: marker `<!-- qa-factory:case-appendix:start -->` inside `facts:regression` (NA `test-report.md:58-68`) | night | major | driver-controller (loop) + hotfix-12586 HF8-17 (marker) | **cause known**: `hotfix-12586/findings/20261029-otchyot-ne-zaschityvaet-ruchnye-proverki-trebovaniyu.md` item 4 → HF8-17 (`ожидает`, P1 for 0.10.6, not shipped); HF8-22 (S9 check rebuilds code-owned blocks). The unbounded loop is new (grep `rebuild_report`, `report_check` → 0) |
| 9 | Role ends without the handoff form and is resumed once per dispatch | RL-15 (7 of 7 retro analysts), RL-11:22 (S7 analyst) | night | minor | speed-cost | **known**: `speed-cost/findings/20261027-21-iz-26-blokov-gejta-format-dajdzhesta-handoff.md` |
| 10 | The conductor's paraphrase changes the person's words | gate A question RL-4: "the missing integration keys and stand users are accepted" vs the answer "the stand has this user" (`experiments/run-14857/answers/gate-a.md`); gate B RL-12: "One run of the scheduled reindex test, TC-001" (TC-001 is the manual reindex, TC-003 the scheduled one) | night | minor (the person may approve a wrong summary) | conductor | new (grep `пересказ` → unrelated files) |
| 11 | The gate A rehearsal says "the stand records no such account" for the configured default user | RL-3:204-208 "PC-1 the stand records no such account (`default_user` is not one of the accounts it lists)" while config `credentials_by_role` names the default user and `.env` has AUTH_USERNAME/AUTH_PASSWORD (gate-a.md) | night (manual had the 12586 twin) | minor | gates-and-words | **known**: `gates-and-words/findings/20261028-gejt-a-predusloviya-sprashivaet-izvestnoe-i-ne-daet-dorogi.md`; `hotfix-12586/findings/20261029-preduprezhdeniya-geita-a-stend-ne-uznan.md` |
| 12 | Words given on one S1 question are not carried to the next question on the same sources | `driver-answers.jsonl` row 1 (01:22:09) "Go on without those 4 attachments of TP1-10937"; RL-2 s1_gap at 01:23:04 asks about plan.md, spec.md of TP1-10937 | night | minor | conductor | class known (D-0043: one recorded decision covers its class; `gates-and-words/findings/20261013-fabrika-ne-obeshchaet-nevozmozhnogo.md`); the s1_review → s1_gap road is new |
| 13 | Real ticket attachments are unreadable by our own limits/policy (screenshots over 30,000 B, `.md` skipped by type); the night now records the screenshots as gaps without a question | RL-2 "Already recorded as gaps, without a question … screenshot-1.png; screenshot-3.png"; "plan.md skipped_by_policy:type" | both | major (requirement material lost on every ticket with attachments) | speed-cost | **known**: SC2-41 `speed-cost/findings/20261029-limit-chteniya-nizhe-vlozhenij-realnogo-tiketa.md`, status `ожидает` (was P1 for 0.10.6, not shipped) |
| 14 | A Then that compares a server timestamp with a host timestamp has no tolerance, so a 2.3 ms clock difference becomes `contradicts_requirement`; the ledger and the triage then disagree on the same case | NA `work/triage.json` TC-001 `unverified` (2.3 ms, attempt 73f580c5…); ledger TS-1 `not_executed:contradicts_requirement` vs triage verdict `ENV_ISSUE`; report «Left with you» item 1; critic approved TC-001 | night | major | test-code-quality | new (grep `clock\|skew\|расхождени[ея] часов`, `2[.,]3 ?(мс\|ms)` → only `codex/batch-1-overhead-fixes.md`, unrelated) |
| 15 | A stand capability a case depends on (a scheduler that fires datasource cron) is not checked before S5; S7 finds it | NA `work/triage.json` TC-003: "docker ps shows no scheduler service on the stand"; gate A rehearsal asked only for a user for P-cron (RL-3:208) | night | major | execution-probes (or stand-and-sources) | new (grep `scheduler\|планировщик` → codex/execution-probes files about other things; `execution-probes/findings/20261029-runtime-probes-ne-zapisany-do-s5.md` is about a config key, not this) |
| 16 | What a person taught the factory about the stand in one run (indexing a real repo exceeds the default waits; `files_filter`, `timeout(900)`) is not kept for the next run of the same project | t-1597 sink 2 (manual, person 28 min); night `triage.json` TC-001 "wait_for_indexing, 180 s" | both | minor | stand-and-sources | new (grep `files_filter\|timeout\(900\)` → 0). The timeout misread itself is known: RH2-9 |
| 17 | Cost capture re-creates a moved session's cost file from the transcript (the project folder is rescanned), and the re-capture loses the activity attribution; there is no factory move that archives or restarts a story's run | SC `54dd49d9….json` mtime 02:31:52 after the move at 02:21:52 (MA `cost-moved/`, NB 02:21); fresh file: `has_factory_activity` False, `by_task` TP1-14857 $12.35 + `(no task)` $9.98 (archived: $22.22 + $0.12) | both runs (manual's cost, night's capture) | major (P18) | cost-dashboard | new (grep `архив.{0,60}(cost\|цен)` → 0) |
| 18 | The task's price is not one true number: the dashboard row for TP1-14857 shows only the night ($15.63, 36 sessions, duration "—"); the manual run's $22.34 sits in "Unclassified"; inside the night, 12 of 36 sessions are attributed to `(no task)` only ($3.28) and `by_task` puts $5.95 of $15.63 on `(no task)`; no driver session has `has_factory_activity` | SC dashboard `state/factory-dashboard.html` (06:41:04): rows "Unclassified 3 · 102.20M · $22.59" and "TP1-14857 36 · — · 33.19M · $15.63"; night.py. **Correction to claim (a)**: the "1 session, 4h10m, 101.95M, $22.22" row is in the ARCHIVED dashboard (MA `state-full/factory-dashboard.html`, 01:55:13), not in the stand's current one, which does show the 36 driver sessions | both | major (P18) | cost-dashboard | new (grep `has_factory_activity\|claude -p.*дашборд\|driver.*dashboard` → `cost-dashboard/findings/20261019-factory-types-kopii-v-hooklib-i-cost-capture.md`, B-268: different defects) |
| 19 | Tokens on the dashboard are dominated by near-free cache reads and mislead as a cost proxy | manual cache read 98.52M of 102.03M (96.6 %), night 30.62M of 33.19M (92.3 %), cost.py/night.py; the dashboard prints the total ("101.95M", "33.19M") beside the price | both | minor | cost-dashboard | new (grep `токен.{0,60}(вводят\|мера\|прокси\|чтени.{0,10}кэш)\|tokens.{0,40}(proxy\|misleading)` → only `speed-cost/findings/20261026-zamer-stoki-tokenov-12586.md:22`, a measuring note) |
| 20 | Per-tool counts in a cost file grow on every incremental capture (subagent tools added again each pass); the dashboard sums them | archived 54dd `tools.Bash` 17,065 vs 405 on the fresh rescan (162 main + 243 subagents); `c8b73507` Bash 73,429; main-only tools (Agent 21, SendMessage 15) are not inflated; PKG `cost_capture.py:1244` adds, `factory_dashboard.py:2724` sums | both | minor | cost-dashboard | new (grep `счётчик.{0,30}инструмент\|tool count\|tools.{0,20}(завыш\|inflat)` → 0) |
| 21 | `human_wait_s` is non-zero for headless `claude -p` role sessions, where no human exists | SC `891815a0` 1,176 s, `455a9cd8` 1,902 s, `d5f5be2d` 1,960 s; read by PKG `factory_dashboard.py:2686,2708` | night | minor | cost-dashboard | **known class**: `hotfix-12586/findings/20261028-cena-na-dashborde-lozhnye-krasnye-metki.md:10` (person wait counts notifications and service lines); headless is new evidence |
| 22 | `duration_ms` of a driver row is not the session's time | `driver-runs.jsonl` row 2: launched 00:59:08, returned 01:20:41 UTC (21.5 min), `duration_ms` 6075, `num_turns` 1 | night | minor | driver-controller | new (grep `duration_ms` → 0) |
| 23 | The report prints the gate A words twice and lists 14 identical "accepted, bound to nothing" lines | NA `test-report.md:98-184` ("(earlier answers, as given:)" then "Earlier answer at this gate:"), `:166-179` | night | minor | report-delivery | new (no grep hit for the duplication; not grepped beyond `Decided at gate`) — low confidence on dedup |
| 24 | The verdict is not in the task's terms and stays "not ready" when every requirement is proven or deferred by the person | MA `test-report.md:7` "4 on the product side that no single requirement explains … 7 proven, 0 not proven, 4 deferred"; NA `test-report.md:7` "12 on the product side …" with 0 bugs | both | major (P21: the third outcome is never reached) | report-delivery | **known**: HF8-17 item 6 (bookkeeping vs not proven), `report-delivery/findings/B-122-prichiny-nedostavki-nasha-bukhgalteriya-i.md` |
| 25 | Regression commands carry this machine's absolute path | NA `test-report.md:62` `python "D:/ws2/run-14857-pkg/qa-factory/scripts/run_suite.py" …` | both | minor (AR-4) | hotfix-12586 | **known**: HF8-17 item 5 |
| 26 | Question texts break `human-questions.md` and are asked anyway; gate B packet is 67,805 B | `driver-questions.jsonl` gate_B row `bytes` 67805, problems flag/exit_code/explained_ids; RL-11:51-54 (`--label`, `exit 1`); s1_gap names `vcs_evidence.py` | night | minor | gates-and-words / conductor | s1_gap part **known** C3-16 (`conductor/findings/20261016-tekst-s1-gap-pokazyvaet-imya-skripta.md`); gate B size/flags not found (grep `asked anyway\|recorded as ours\|explained_ids` → only C3-16) |
| 27 | Each code critic overwrites `critic-findings.md`; rounds 1–3 remarks survive only in transcripts | NA `work/test-code/critic-findings.md:1` "S5-qa-code-critic-4" only | night | minor (feeds 4 and 7) | test-code-quality | new (grep `critic-findings.{0,40}(перезапис\|overwrit\|затира)` → 0) |
| 28 | Manual-run defects already analysed | t-1597 sinks 1–13 and N1/N2 (story_step latency SC2-40, OB-3 hash `speed-cost/findings/20261030-hesh-obyazatelstva-dva-smysla-…`, S6 empty runner `speed-cost/findings/20261030-s6-dispatchit-…`, RH2-9, TQ1-21, DC1-18, HF9-1, CD1-24); t-1598 → `driver-controller/findings/20261030-doroga-dirizhyora-…` | manual | as filed | as filed | **known** (files named in t-1597 §2-3 and t-1598 §3) |

NB's 11 night defects, checked: 1 (receipt) confirmed = #1; 2 (cap per stage) **corrected** = #3 (per window; counts the factory's own
refusal rounds) and #2 (no-move, known HF8-15); 3 (gate words lost) confirmed, root = #5 and #6; 4 (paraphrase) confirmed = #10 and a
second instance at gate B; 5 (rehearsal user) confirmed = #11 (known); 6 (cap without test_defect) confirmed = #4 (rounds 1–2 had
`mechanical`, which per the rule also spends no cap); 7 (TC-002 report) confirmed and widened = #7 (the repair after S7 had no
re-review); 8 (S9 marker) confirmed = #8 (cause known, loop new); 9 (S1 words) confirmed = #12; 10 (archive cost) confirmed = #17;
11 (`human_wait_s`, `duration_ms`) confirmed = #21, #22.

Morning dashboard claims: (a) **not reproduced** on the stand's current dashboard (it has the 36-session row); the quoted numbers
are the archived 01:55 dashboard; the real residue is #18. (b) confirmed with a different shape: the re-created file puts $12.35 on
the task and $9.98 on `(no task)`, and the dashboard shows it under "Unclassified" (#17, #18). (c) confirmed (#19).

## 4. 0.10.5 → 0.10.6 on this ticket

Better:
- Cheaper and shorter: $15.63 vs $22.34 (−30 %), 4 h 46 min vs 5 h 50 min, though 31 min of the night stood on a blocker.
- S1 did not halt on a conflict the comments settle (manual lost 17 min of the person's time there).
- S3 23.0 vs 28.3 min and S4 6.8 vs 27.1 min: no two-pass S3 gate, no empty rework form, no missing `extend` target.
- Gate A lettered answers Q1/Q2 recorded (driver road, `question-answers.jsonl`); manual lost them (t-1598).
- No `pytest-timeout` misread as a stand failure; no OB-3 hash rebinding; S6 ran real tests.
- The S5 code critic caught a real test defect (TC-002 page object) statically.

Worse (or new on this run):
- 0 requirements proven (manual 7 of 11): TC-001 red on 2.3 ms (#14), TC-003 on a stand without a scheduler (#15), TC-002 green but
  unreviewed after repair (#7).
- A blocker in S5 (#1, fixed by t-1603 at night) and a no-move state after it (#2, known HF8-15, not shipped), a cap spent on the
  factory's own refusal (#3) and a cap spent without `test_defect` (#4).
- More questions: 15 vs ≈11, with 7 re-asks (gate A ×2, gate B ×1, s1_gap, S5 receipt ×3).
- S9: 38 min and 7 paid retro analysts on a known report-layout defect (#8) that was planned for 0.10.6 (HF8-17) and did not ship.
- The dashboard now splits one task's price across two rows (#17, #18).
- Not changed (planned for 0.10.6, still `ожидает`): SC2-41 attachments, HF8-15 no-move, HF8-17 report — all three reproduced.

## 5. Для владельца (по-русски)

Ночной прогон дешевле ($15.63 против $22.34) и короче (4 ч 46 мин против 5 ч 50 мин), S1–S4 стали заметно лучше, ответы Q1/Q2 на гейте A
записались. Но доказано 0 требований из 9 (у вас — 7 из 11): TC-001 покраснел на 2,3 мс разницы часов хоста и стенда (тест сравнивает
время двух машин без допуска), TC-003 требует планировщика, которого на стенде нет (фабрика узнала это только на S7), а TC-002 после
отказа критика починил новый автоматор уже после S7, и повторного ревью не было — отсюда «pass» рядом с «rejected» в отчёте. Три пункта,
запланированных в 0.10.6 (вложения SC2-41, тупик при открытом критике HF8-15, отчёт HF8-17), не вышли и повторились. Из утренних
замечаний по дашборду: строка «1 сессия, $22.22» — из архивной копии дашборда в 01:55; в текущем дашборде стенда ночная строка есть
(36 сессий, $15.63), зато ваш ручной прогон после переноса в архив пересчитан заново и ушёл в «Unclassified» ($22.59) — цена задачи
разъехалась на две строки. Новых находок — 17 (строки 3–7, 10, 12, 14–20, 22, 23, 27), известных — 11.

## 6. Trail

Read: NB (whole); t-1597 §0–§3; t-1598 §1, §3; t-1604 (whole); NA `state/driver-runs.jsonl` (runs.py), `state/driver-questions.jsonl`,
`state/driver-answers.jsonl`, `state/driver-state.json` (`window_rounds`), `state/events.jsonl` (stages.py), `state/words/` listing,
`work/question-answers.jsonl`, `work/ledger.md`, `work/triage.json`, `work/test-code/critic-findings.md`, `work/handoffs/` listing and
critic-1..4 grep, `work/review-receipts/S5-qa-code-critic-4.json`, `work/requirements-register.md`, `test-plan.md`, `test-report.md`
(lines 1-110, 125-240); MA `pipeline.json`, `events.jsonl` (stages.py), `test-report.md:7` + sections, `work/ledger.md`,
`requirements-register.md`, `cost-moved/` (cost.py), `state-full/factory-dashboard.html` (grep); SC all 39 files (cost.py, night.py),
`state/factory-dashboard.html` (grep, mtime), `state/activities/`; RL-2, 4, 5, 6 (64-76), 9, 11 (1-54), 12, 15, 16; transcripts
`c7f0b25a`, `4f6371e3`, `18e69b0b` (grep `cause:`), manual `54dd49d9….jsonl` (grep tool_use count 162); PKG `story_run.py:5572-5632,
8500-8530`, `controller.py:200-225`, `cost_capture.py:1140-1165,1225-1255,1880-1905`, `factory_dashboard.py:2718-2730`,
`references/config-keys.json` `dispatch_windows_note`; piles: findings named above opened at their headers; HF8-15/16/17/22 rows of
`hotfix-12586/batch-8-ostatki-hf3.md`; SC2-41 row status; C3-16 row; `conductor/batch-1-p22-seams.md:108,143`.
Not done: root cause of #4 and #7 in code (candidates named); the gate A packet's full text beyond RL-3 lines 76-208; per-stage cost
of the manual run.

## Appendix — scripts (verbatim)

### cost.py
```
# read-only: summarize cost files
import json,sys,glob,os
rows=[]
for f in sorted(glob.glob(os.path.join(sys.argv[1],'*.json'))):
    if os.path.basename(f).startswith('activities'): continue
    d=json.load(open(f,encoding='utf-8'))
    bm=d.get('by_model',{})
    tok={k:sum(v.get(k,0) or 0 for v in bm.values()) for k in ('input','output','cache_read','cache_write_5m','cache_write_1h','requests')}
    acts=list((d.get('by_activity') or {}).keys())
    rows.append((d.get('started'),d.get('ended'),os.path.basename(f)[:8],d.get('tasks'),d.get('has_factory_activity'),float(d.get('priced_subtotal_usd') or 0),tok,acts[:4],len(d.get('agents') or [])))
rows.sort(key=lambda r:r[0] or '')
T={'usd':0}
for r in rows:
    print(r[0][:19] if r[0] else None, (r[1] or '')[11:19], r[2], r[3], 'fa=',r[4], '$%.3f'%r[5], r[6], r[7], 'agents',r[8])
    T['usd']+=r[5]
    for k,v in r[6].items(): T[k]=T.get(k,0)+v
print('TOTAL',len(rows),T)
```

### night.py
```
import json,sys,glob,os
T={}
n=0; notask=0; notask_usd=0
for f in glob.glob(os.path.join(sys.argv[1],'*.json')):
    if os.path.basename(f).startswith('activities'): continue
    d=json.load(open(f,encoding='utf-8'))
    if (d.get('started') or '')<'2026-10-30T00:50': continue
    n+=1
    usd=float(d['priced_subtotal_usd']); T['usd']=T.get('usd',0)+usd
    bt=d.get('by_task',{})
    T['task_usd']=T.get('task_usd',0)+float((bt.get('TP1-14857') or {}).get('cost') or 0)
    T['notask_usd']=T.get('notask_usd',0)+float((bt.get('(no task)') or {}).get('cost') or 0)
    if 'TP1-14857' not in d.get('tasks',[]): notask+=1; notask_usd+=usd
    for v in d['by_model'].values():
        for k in ('input','output','cache_read','cache_write_5m','cache_write_1h'): T[k]=T.get(k,0)+(v.get(k) or 0)
print(n,T,'sessions without the task:',notask,'$%.3f'%notask_usd)
```
Output: `36 {'usd': 15.6264371, 'task_usd': 9.6756, 'notask_usd': 5.9509, 'input': 1084, 'output': 382786, 'cache_read': 30619691, 'cache_write_5m': 0, 'cache_write_1h': 2183610} sessions without the task: 12 $3.282`

### runs.py
```
# read-only: driver-runs.jsonl per-session max cost, per stage
import json,sys,collections
rows=[json.loads(l) for l in open(sys.argv[1],encoding='utf-8') if l.strip()]
kinds=collections.Counter(r['kind'] for r in rows); print(kinds)
mx={}; st={}; role={}; first={}; last={}
for r in rows:
    if 'session_id' in r and r.get('total_cost_usd') is not None:
        s=r['session_id']; mx[s]=max(mx.get(s,0),r['total_cost_usd']); st[s]=r.get('stage'); role[s]=r.get('role') or r.get('call') or r['kind']
        first.setdefault(s,r['ts']); last[s]=r['ts']
print('sessions',len(mx),'sum max $%.3f'%sum(mx.values()),'naive sum $%.3f'%sum(r.get('total_cost_usd') or 0 for r in rows))
by=collections.defaultdict(float); n=collections.Counter()
for s,v in mx.items(): by[st[s]]+=v; n[st[s]]+=1
for k in sorted(by,key=str): print(k,n[k],'$%.3f'%by[k])
for s in sorted(mx,key=lambda s:first[s]): print(first[s][11:19],last[s][11:19],s[:8],st[s],role[s],'$%.3f'%mx[s])
```
Output head: `sessions 36 sum max $15.626 naive sum $28.738`; S1 2 $1.444 · S2 1 $0.608 · S3 3 $3.024 · S4 4 $1.173 · S5 14 $5.999 · S6 1 $0.327 · S7 1 $0.622 · S8 3 $0.625 · S9 7 $1.805.

### stages.py
```
# read-only: stage windows from controller events.jsonl (prev stage done -> own done), local time UTC+1
import json,sys,datetime
ev=[json.loads(l) for l in open(sys.argv[1],encoding='utf-8') if l.strip()]
t0=ev[0]['created_at']; done={}; disp={}
for e in ev:
    p=e.get('payload') or {}
    if e['type']=='stage_transition' and p.get('status')=='done': done[p['stage']]=e['created_at']
    if e['type']=='dispatch': disp[p.get('stage')]=disp.get(p.get('stage'),0)+1
f=lambda t: datetime.datetime.utcfromtimestamp(t+3600).strftime('%H:%M')
prev=t0
for s in sorted(done,key=lambda s:done[s]):
    print(s, f(prev),'-',f(done[s]), '%.1f min'%((done[s]-prev)/60), 'dispatches',disp.get(s,0)); prev=done[s]
print('first',f(t0),'last',f(ev[-1]['created_at']),'total %.1f min'%((ev[-1]['created_at']-t0)/60))
```
Night output: S1 27.8 · S2 5.5 · S3 23.0 · S4 6.8 · S5 144.9 · S6 16.1 · S7 19.3 · S8 4.3 (no S9 `done` event; S9 closed by the person's `go on`, RL-16).

## Verdict

On the night notebook's defect list as an input to filing: **NEEDS WORK (fit_with_fixes)** — 0 blocking; 2 of its 11 items need
correcting before they are filed (item 2 cap "per stage" → #3/#2; claim (a) of the morning → #18), 17 new findings and 11 known ones
are listed with their pile. The decision to file and prioritise belongs to the Lead.

DUPLICATION AND CONSISTENCY: not applicable as a diff gate (no diff under review); the duplications seen in the factory are findings
#5 (two roads, two closed approval words, AR-15) and #23. CODE QUALITY: none reviewed (no new code).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "Classes walked per finding: gate words (A, B, register questions, S1 stop words) on both roads -- driver road A/B item lines (#5), register free text (#6), S1 review to gap (#12), conductor road known (t-1598); S5 round counting (window cap #3, repair cap #4, no-move #2 known HF8-15); report/S9 contradictions (#7, #8, #23, #24, #25); cost attribution (archive #17, task row #18, tokens #19, tool counts #20, human wait #21, duration #22). Not walked by the map: SIBLING_MAP axes for the cost readers beyond factory_dashboard.py and cost_capture.py -- a scout request if the Lead wants every reader of human_wait_s and tools listed.",
  "trail": {
    "read": [
      "experiments/run-14857/run-14857.md",
      "docs/tasks/specs/reviews/t-1597-14857-why-slow.md",
      "docs/tasks/specs/reviews/t-1598-14857-gate-a-answers-lost.md",
      "docs/tasks/specs/reviews/t-1604-t1603-diff-critic.md",
      "NA state/driver-runs.jsonl, driver-questions.jsonl, driver-answers.jsonl, driver-state.json, events.jsonl",
      "NA work/question-answers.jsonl, ledger.md, triage.json, test-code/critic-findings.md, requirements-register.md, test-report.md",
      "MA artifacts-TP1-14857 pipeline.json, events.jsonl, test-report.md, ledger.md; cost-moved; state-full/factory-dashboard.html",
      "SC 39 cost files; state/factory-dashboard.html",
      "experiments/run-14857/runs r14857-2,4,5,6,9,11,12,15,16",
      "PKG story_run.py 5572-5632, controller.py 200-225, cost_capture.py 1140-1165 1225-1255 1880-1905, factory_dashboard.py 2718-2730",
      "plans/piles findings and batch rows named in section 3"
    ],
    "reruns": [
      {"command": "python -I night.py SC", "result": "36 sessions, $15.626, task $9.68, (no task) $5.95, 12 sessions without the task $3.28"},
      {"command": "python -I runs.py NA/state/driver-runs.jsonl", "result": "36 sessions, sum of max $15.626, naive sum $28.738"},
      {"command": "python -I cost.py MA/cost-moved", "result": "54dd49d9 $22.336, cache_read 98,517,196, output 420,848"},
      {"command": "python -I stages.py (both events.jsonl)", "result": "manual S5 213.8 min incl. gate A; night S5 144.9 min incl. gate A"}
    ]
  },
  "fixes": [
    "File NB item 2 as #3 (window cap spent by the factory's own refusal rounds) plus #2 (known HF8-15), not as 'cap per stage'",
    "File dashboard claim (a) as #18 (task price split across rows; duration missing), not as 'no row for driver sessions'",
    "Open finding rows for t-1604 F3-F5 (#1) and for the 17 new findings in the piles named in section 3"
  ]
}
```
