# t-600 — exam and calibration duties owed (scout digest, 09.10.2026)

Recon for forge batch 2: the owner's word 09.10 — exams are deferred to a weightier occasion (they eat the
weekly limit); ALL exam debts go into ONE separate task. Lead spot-checks 09.10 09:54: `calibrated` events
0 / 0 in both journals (control `delegated` 727 / 8); PROCESS/ has only DEPLOYMENT_ECONOMY_EXAM.md and
LEAD_RANKING_EXAM.md (no CRITIC_EXAM.md, no SCOUT_GOLDEN_SET.md); role files last edited: critic/scout/builder/judge
`3bb09674` 2026-09-29, designer `6340a924` 2026-09-30.

## Bottom line
- `PROCESS/CRITIC_EXAM.md` and `PROCESS/SCOUT_GOLDEN_SET.md` do not exist anywhere in the repo. No critic or scout exam has ever run, so no pass exists for either.
- `calibrated` events: zero, in both journals. `Last calibration: NONE` is therefore the live state.
- The Runs logs of `LEAD_RANKING_EXAM.md` and `DEPLOYMENT_ECONOMY_EXAM.md` are empty.
- The judge has no calibration record. `accepted(basis:"judge")` appears 0 times, so the judge is not in use.

## Waiver on record (a fact, not a verdict)
- `docs/DECISIONS_ARCHIVE.md:10-14` holds D-0004, archived 06.10.2026 as "superseded by the exam protocol": "Entrance exams skipped at onboarding by the operator's explicit word (29.09.2026)... until a scout exam pass, scout digests are accepted under the strict form of rule 1 (R1 b)."
- D-0005 (same archive): "Designer bound to claude-opus-5-5 without exam coverage - no designer set by design."
- The live `DECISIONS.md:19-21` holds D-0002 and D-0003 (bindings), and no waiver of exam duty.

## PROCESS/*.md, each file once ("names an exam duty")
| file | exam duty |
|---|---|
| BOOT_REPORT_PROTOCOL.md | no (defines the Last Calibration line; :51-52 says the detector for a missing calibration lives outside calibration) |
| DEPLOYMENT_ECONOMY_EXAM.md | yes |
| DOCUMENTATION_PROTOCOL.md | no |
| JUDGE_CALIBRATION_PROTOCOL.md | yes |
| LEAD_RANKING_EXAM.md | yes |
| PATCH_PROTOCOL.md | no |
| PRE_COMMIT_PROTOCOL.md | no (:4 only cites calibration check 8) |
| README.md | yes (index; :22-25 names CRITIC_EXAM and SCOUT_GOLDEN_SET as "generated at onboarding", which are absent) |
| SESSION_PROTOCOL.md | no |
| WEEKLY_CALIBRATION_PROTOCOL.md | yes |
| ZERO_CONTEXT_PROTOCOL.md | no |

`delegation.config.yaml:52-76` binds critic opus-5-5, builder and scout sonnet-5-5, matching the frontmatter. Only critic.md and scout.md carry a "run the exam before the commit" rule (critic.md:57-62, scout.md:55-59). designer.md and builder.md carry no exam clause. `judge.md` frontmatter uses the alias `sonnet`, every other role file a full id.

## Table (classes 1-7)
| # | class | what is owed | why (trigger) | evidence | who pays (est. runs) |
|---|---|---|---|---|---|
| 1 | critic exam | Generate `PROCESS/CRITIC_EXAM.md` (seeded diff: D1, D2, D3, T-K5, T-K3, intact control; key pre-registered). Dispatch one unmarked review in a fresh session. Add a Runs log line in the same commit as the `critic.md` edit. Pass: both traps independently reproduced, D1 found, zero hallucinated blockers. | B-419 edits `critic.md` (rule 10; critic-exam-gen "Re-run triggers" 1-3). Onboarding "before first real review" was waived (D-0004). | No pass exists: the file is absent. `critic-exam-gen/SKILL.md:35-44,191-201`; `critic.md:57-62`; `BACKLOG.md:441` (B-419); `CLAUDE.md:33`; `forge/README.md:17`. `critic.md` has rules 12-17 and its :82 names "the critic exam's two mandatory traps", so the file was extended with no exam on record (check 14(a) not satisfiable). | 1 Lead-tier generation session (Fable), 1 Opus critic run, +1 Opus run if contaminated or failed. |
| 1b | designer coverage | None separate: the designer is bound to the same model as the critic and "inherits the critic exam when the model is the same". | `onboarding/SKILL.md:219-234`, `SIBLING_MAP.md:50,59-60`. | Closed by row 1 only. Builder: no set by design (`SKILL.md:214-218`, `SIBLING_MAP.md:49`). | 0 extra |
| 2 | scout exam | Generate `PROCESS/SCOUT_GOLDEN_SET.md` (7 questions: Q1-5 point or multi-hop, Q6 usage-vs-mention trap, Q7 judgment refusal; keys pinned by the Lead). Dispatch unmarked. Pass: at least 6/7, with Q6 and Q7 each passing. | Never run; `scout.md:55-59`; scout-exam-gen "Re-run triggers"; `next-task/SKILL.md:52`. | File absent. Journal: `routing-log.jsonl:172` "no scout exam pass, D-0004"; `:1212` "strict form, no scout exam pass". 80 scout-agent lines in the routing log. | 1 Fable generation turn, 1-2 Sonnet scout runs. |
| 2b | R1 currency | Not current by the R1 definition: R1 a requires a CURRENT PASS, none exists; the R1 b strict form is in force. | `CLAUDE.md` rule 1 table R1 a/b. | `defect_found` with agent scout/critic/judge: 0 (control: 31 designer/builder events). | n/a |
| 3 | designer/builder exams | Nothing owed per the protocol (designer inherits row 1). | See 1b. | `onboarding/SKILL.md:214-234`. | 0 |
| 4 | Lead exam | `LEAD_RANKING_EXAM.md`: 6 cases K1-K6, no tools for the candidate, a chief judge one tier below because Lead is the top tier (`:28-36`), pass at least 10/12 with no zero. Owed "when binding or swapping the model bound to lead" (`onboarding/SKILL.md:242-244`). | `lead` = claude-fable-5-1 (`delegation.config.yaml:19-21`, D-0003). | Runs log (`LEAD_RANKING_EXAM.md:167-173`) holds only a comment template. No waiver other than archived D-0004. | 1 candidate dispatch + 1 judge grading. |
| 5 | judge calibration | Subscription judge-subagent: all 13 pairs of `gateway/judge_calibration.json` with `JUDGE_SYSTEM_PROMPT` verbatim; bar 13/13; record date, model, score, prompt-equality confirmation. The gateway-alias form needs a live proxy. | Needed only for `accepted(basis:"judge")` (rule 13; Protocol rule 8, `:77-101`). | 13 `"verdict"` entries; no equivalence record (0 hits for judge_calibration/shadow_eval/JUDGE_SYSTEM_PROMPT in both journals; control: 18 hits in `shadow_eval.py`). `basis:"judge"` events: 0. D-0003: "judge stays as shipped (deferred, subscription contour)". Usable now: no (`:96-99`). | 1 Sonnet judge run (13 pairs). |
| 6 | weekly calibration | Run all checks (1-33) and write a `calibrated` event. Overdue by the >7-day rule. | `WEEKLY_CALIBRATION_PROTOCOL.md:952-963`; `session_context.py:577`. | 0 `calibrated` events; `compact-snapshots/2026-10-08-current-context-archive.md:604`: "The weekly calibration has never run". | 1 Lead-tier session; check 26 routed to a scout; check 30 every 4th run; checks 18 and 11 run scripts. |
| 6b | economy exam | Absent from the weekly protocol (no check names `DEPLOYMENT_ECONOMY_EXAM`, `exam_runner`, `LEAD_RANKING`; control: 15 hits for Forge/PreCompact/Piles). The doc (`:253-274`) says the SMALL exam goes into every calibration cycle, the LARGE at most once per release. | Release 0.9.0 dated 2026-10-07. | Runs log empty (`:294-298`). | Expensive per the doc: 3 arms times a task set, headless sessions; not estimable from the doc. |
| 7 | B-457 | 8 "pre-release 0.9 calibration cases" for the nearest weekly calibration. | Row: "в файлы PROCESS не переносятся". | `BACKLOG.md:482`; forge batch 2. Cases: (1) B-415 owns omitted 6 paths; (2) B-405/406 owns omitted 2; (3) B-407 D scope wider than spec; (4) B-373 (c) edges said `incomplete`; (5) worktree cut from pushed origin/main; (6) `sed` confession cited the wrong line; (7) false "B-410 had landed"; (8) witness misquoted 340 vs 339. | Rides on row 6. |
| 8 | other mentions | B-111: no `evals/judgments/` calibration set (package judge_diff; not a factory-dev exam). B-138: usage_report price table diverges from `model-rates.json` (feeds calibration check 18). Others are descriptions, not duties. | | `BACKLOG.md:272,141`; `plans/piles/roles-context/findings/B-111-...md:5`. | n/a |

## Notes for the task writer (facts)
- critic-exam-gen requires the generator to run the canonical test command "right now" for the T-K5 baseline (`SKILL.md:82-95`); suites do not run on the owner's machine (CI only, memory).
- Both skills require a fresh session (agent-definition cache) and forbid mentioning the exam in the dispatch. Scope the critic dispatch away from `PROCESS/` and `docs/`.
- Failure path: `critic-exam-gen/SKILL.md:180-189`: show the warning, then the owner decides replace or keep. "Keep" appends a DECISIONS line.
- ESTIMATE of cost per debt (from the protocols' own counts; estimate, not measured). `BACKLOG.md:567` (B-464): 81 Opus runs = 19% of the week, about 0.23% per Opus run.

| debt | estimate |
|---|---|
| critic exam | 1 Opus (+1 on fail), plus 1 Fable generation |
| scout set | 1-2 Sonnet, plus 1 Fable generation and key pinning |
| Lead ranking | 1 candidate run plus 1 judge grading |
| judge | 1 Sonnet |
| weekly calibration | 1 Fable session plus about 1 Sonnet scout |
| economy exam | not estimable from the doc |

## Analogs noticed (not pursued)
- `WEEKLY_CALIBRATION_PROTOCOL.md` has no check for the economy exam, though that doc asks the host protocol to carry one.
- `PROCESS/README.md:22-25` lists two files that do not exist; `SIBLING_MAP.md:45-46` lists the same two as instruments.
- `judge.md` frontmatter uses the alias `sonnet`, while every other role file uses a full id.

## Trail (scout)
Controls: Glob `**/CRITIC_EXAM*` 0, `**/SCOUT_GOLDEN*` 0, control `**/LEAD_RANKING_EXAM*` found PROCESS plus ~45 worktree copies; Grep `CRITIC_EXAM|SCOUT_GOLDEN_SET` 11 files, all mentions. Journals: `calibrated` 0/0 (control `delegated` 737/7); `calibrat -i` 31/1, every hit prose; `defect_found` agent scout/critic/judge 0 (control designer/builder 31). Greps over DECISIONS.md, ADOPTION_LEDGER.md, FINDINGS.md, factory-rules-debt.md, CURRENT_CONTEXT.md, BACKLOG.md, plans/piles, PROCESS files. Files read: PROCESS/README, WEEKLY_CALIBRATION_PROTOCOL, JUDGE_CALIBRATION_PROTOCOL, LEAD_RANKING_EXAM (all), DEPLOYMENT_ECONOMY_EXAM (:250-307); agents critic/scout (all), judge (:1-12); skills critic-exam-gen, scout-exam-gen (all), onboarding (:148-272,345-360); DELEGATION_TABLE.md, delegation.config.yaml, DECISIONS.md (:1-30), DECISIONS_ARCHIVE.md (:1-40), SIBLING_MAP.md (:40-80), tools/exam_runner.py (:1-120), BACKLOG.md (:439-461,480-483), forge/README.md, next-task/SKILL.md (:45-59), routing-log.jsonl (lines 1-5, 96, 646, 823, 1088, 1163, 1225), dev1.jsonl (:1-5).
