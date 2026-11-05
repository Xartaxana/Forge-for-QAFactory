# Feature fragility since 26.09 - defects and fixes of fixes, by feature (task t-296)

Generated 2026-10-02 11:26 from the sources named in the dispatch; data only, no judgment (non-goals). Every file name in a table cell is a token the source text itself quotes (extracted from the backticks of the row, the commit message, or the journal note); no file was inferred. Built by a script over `plans/BACKLOG.md`, the cmp2/rehearsal/cmp1/run-5 documents, `logs/routing-log.jsonl` and `git log`; the files it read are listed in the handoff report.

## 0. Counts, commands, conventions

| what | value | command / carrier |
|---|---|---|
| `\| B-` rows in BACKLOG.md (parent rows) | 217 | `grep -c "^\| B-" plans/BACKLOG.md` (BACKLOG changed during this run: B-255..B-257 were appended 02.10 11:11 by another session; first parse had 214) |
| rows after `## Закрыто` | 0 | `L=$(grep -n "^## Закрыто" plans/BACKLOG.md \| cut -d: -f1); awk -v n=$L 'NR>n' plans/BACKLOG.md \| grep -c "^\| B-"` -> 0; positive control with the same awk/grep shape and pattern `"^\| "` -> 1 (the table header). So the "closed" table is empty and a B-row's status below comes only from marks inside the row or from a commit/journal that names it |
| B rows in Table A | 244 | parent rows minus 7 split parents (B-190, B-193, B-207, B-247, B-253, B-255, B-256) plus 34 sub-item rows (one per sub-item; B-190 has 3 because its item (б) is marked "снято") |
| B rows with an explicit date >= 26.09 | 158 | date = last `DD.MM` (month 09/10, not preceded by `$`, a letter or a digit) found scanning the row's cells from the last (source) cell backwards; B-015 forced to 29.09 (the "Решение владельца 29.09" date, not "27-28.09"); sub-item rows take the parent's date. **Cross-check with a plain grep:** `grep -c -E "^\| B-.*(^|[^0-9.$A-Za-z])(2[6-9]\.09|30\.09|0[12]\.10)([^0-9]|$)" plans/BACKLOG.md` -> 131 parent rows (my cell-wise rule also gives 131); 7 of them are split parents, so 124 + 34 sub-item rows = 158 |
| B rows dated `n/d` | 85 | no date in any cell and no dated section header (the section headers carry no date; the file header says "Собран 29.09.2026"). These are B-001..B-133 carried from older plans and the 13877 run; kept in Table A and marked so the Lead can filter. The 13877-run rows (B-012..B-014, B-120..B-133) come from a carrier file named `factory-backlog-testproject1-sdk-2026-09-27.md` (BACKLOG section 10), i.e. 27.09 by file name only |
| B rows dated before 26.09 | 1 (`B-106`, 24.09 = the owner's deferral date) | |
| F-cmp2 rows | 30 | `grep -c "^- \*\*F-cmp2-" experiments/cmp2-15045/cmp2.md` (ids 1..30, 14 and 6 stand last in the source) |
| rehearsal rows | 13 | defects 1-13 in "Итог для владельца" of `experiments/cmp2-15045/rehearsal.md` |
| journal `rejected` | 12 (8 of them `failure_class: spec`, 4 `capability`) + 1 `defect_found` | `grep -c '"event":"rejected"' logs/routing-log.jsonl` -> 12; `grep -c '"event":"defect_found"' ...` -> 1; rejected events with empty notes: 0 (the "n/d" rule was not needed) |
| package commits in the window | 56 | `git -C D:/ws1/yml-text-factory log --since="2026-09-26 00:00" --format=%h -- ai-packages/qa-factory \| wc -l`. **The dispatched `--since=2026-09-26` is time-of-day dependent** (git fills the missing time with the current time): it returned 49 at ~10:20 today and 48 at ~11:20, because the commit `2289055` (26.09 11:20) fell out; with `00:00` the window holds 56 commits - the 7 extra are of 26.09 morning (`1090eea`, `5bacf2f`, `5782744`, `06e669b`, `3416cc7`, `b048984`, `fd9584f`) and are in Table A8. One commit, `4116add`, touches 369 files |
| rows matched by the dispatch's verification regex | 524 | expected minimum = B rows dated >= 26.09 (158) + 30 + 13 + 12 = 213. The surplus: 86 B rows without a date or before the window, 56 commit rows, 13 journal rows in A7, 3 cmp1 `t-` rows, and the D1 (13) and D2 (152) journal rows |

Conventions used in the cells:

- **F** = primary feature, the feature of the file that carries the defect (a file named only as the place where the symptom showed, or as a correct example, does not decide; the ambiguous cases are listed in section 5). **also** = the other features whose files/stage words the item names.
- **found by**: `live run` (cmp1/cmp2/run 5/13877/s01), `rehearsal` (02.10 night), `critic`, `scout`, `builder`, `test`, `owner`, `designer`; added because the sources use them: `lead (...)` (the Lead in a session / own measurement), `older plan/map (not a run)` (B rows carried from `factory-plans`), `rules walk`.
- **class**: my controlled tags (the source words behind each are in the cited row): silent loss, refusal without door, no way out / no zero outcome / no executor, absolute path, project-specific, code decides for role/person, role fights the code, race / timing / buffering, text to a person, unknown as fact, second copy / twin, wrong measurement / cost, unchecked claim, false pass / false ok, stale state / not portable, repeat spend / slow, field without producer, missing check / no guard, idea (not a defect), environment.
- **status**: only what the source row says (closed marks, commit hashes, task ids). `open` = no closure mark in the source; it does NOT prove the code is unfixed (e.g. `B-007` is closed by `1df9fcc`; the BACKLOG row was not moved).
- **fix-of-fix** (only when the source text says so; quote in the cell): `yes` = the item is a defect of / caused by an earlier fix; `sib` = twin / neighbour / remainder left by an earlier fix; `rec` = same defect named earlier and present again; `self` = the first attempt at the same fix failed (inside one task/commit).

Features F01-F18 are the dispatch taxonomy. **Two features were added because nothing fitted** (stated per the dispatch): **F19** dev system and experiment tooling (files under `tools/`, `experiments/`, `.claude/`, `docs/`, `plans/`, hooks of this repository, dispatch discipline, measurers outside the package) and **F20** jev/judge layer (`judge_*.py`; B-110, B-111 only).

| F | feature | | F | feature |
|---|---|---|---|---|
| F01 | ticket read S0 | | F11 | execution |
| F02 | sources S1 | | F12 | S7 triage and handoff forms |
| F03 | stand access and identity | | F13 | report and delivery |
| F04 | onboarding and reinstall | | F14 | cost, telemetry, dashboard |
| F05 | controller and dispatch packets | | F15 | package hygiene and self-checks |
| F06 | driver headless | | F16 | hooks and guard |
| F07 | questions to a person, gates A/B | | F17 | role texts and controller blocks |
| F08 | coverage and traceability | | F18 | Jira agents / write side |
| F09 | oracle provenance P20 | | F19 | dev system and experiment tooling (ADDED) |
| F10 | manual evidence | | F20 | jev / judge layer (ADDED) |

## 1. Table A - one row per defect / finding

### A1. BACKLOG rows (B-nnn, sub-items split)

| id | date | F | also | file(s)/function named in the source | found by | class | status | fix-of-fix |
|---|---|---|---|---|---|---|---|---|
| B-001 | n/d | F14 | F19 | `references/model-rates.json` | older plan/map (not a run) | wrong measurement | closed (7abde94) | - |
| B-002 | n/d | F03 | F11,F08 | `probe_by_code`, `acceptance.validate_window`, `red_sandbox`, `references/field-producers.json` | older plan/map (not a run) | field without producer; false blocker | closed by code, proven only live (9a16c31) | - |
| B-003 | n/d | F06 | F13,F03 | `story_run.py:2026` | older plan/map (not a run) | no zero outcome; false pass | closed (1df9fcc) | - |
| B-004 | n/d | F06 |  | `Person("halt")`, `s0()` | older plan/map (not a run) | refusal without door (empty promise) | closed (1df9fcc) | - |
| B-005 | n/d | F06 | F03 | `story_run.py:1620` | older plan/map (not a run) | second copy (code vs four documents); stand stops the story | closed (1df9fcc) | - |
| B-007 | n/d | F12 | F06 | `rework()` | older plan/map (not a run) | code decides for the role (cause always test_defect) | closed (1df9fcc) | - |
| B-008 | n/d | F06 | F01,F05 | `story_run.py`, `work/ticket-snapshot.md`, `brief_pack.py:59`, `ticket-snapshot.json` | older plan/map (not a run) | silent loss (snapshot not in brief); second copy (.md vs .json) | closed (1df9fcc) | - |
| B-009 | n/d | F07 | F06 | `references/human-questions.md` | older plan/map (not a run) | text to a person | closed (1df9fcc), remainder B-171 | - |
| B-010 | n/d | F08 | F13 | `ledger.py:237` | older plan/map (not a run) | text to a person (verdict meaning changed) | closed (9a16c31) | - |
| B-011 | n/d | F14 | F19 | `code_friction.py` | older plan/map (not a run) | measurement missing (friction) | closed (7abde94, 1df9fcc) | - |
| B-012 | n/d | F06 | F08,F16 | `plan_row`, `test-plan.json`, `story_run.py:376` | live run | text to a person; silent loss (partial artifact); role fights the code (cp1252) | closed (1df9fcc) | - |
| B-013 | n/d | F08 | F17,F05 | `s5_precheck`, `contract.case_ids` | live run | project-specific (case id regex) | closed (88346e7) | - |
| B-014 | n/d | F06 | F16,F17,F04 | — | live run | absolute path; two generations (hooks vs scripts) | closed (1df9fcc); remainders B-142/B-165/B-166/B-167 | - |
| B-015 | 29.09 | F19 |  | — | older plan/map (not a run) | idea (the comparison run itself) | done: cmp1 30.09, cmp2 01.10 (row not updated) | - |
| B-020 | n/d | F02 | F13,F12,F17 | `context-manifest.json`, `requirements-register.md`, `understanding.md`, `test-report.md` | older plan/map (not a run) | role fights the code (hand-written patchers) | open | - |
| B-021 | n/d | F12 | F17 | — | older plan/map (not a run) | role fights the code; repeat spend (form price) | open | - |
| B-022 | n/d | F17 |  | — | older plan/map (not a run) | measurement missing | open | - |
| B-023 | n/d | F12 |  | `handoff_check.CLAIMS` | older plan/map (not a run) | unchecked claim | open | - |
| B-024 | n/d | F05 | F17 | — | older plan/map (not a run) | refusal without door (109 command blocks unproven) | open | - |
| B-025 | n/d | F16 |  | — | older plan/map (not a run) | refusal without door | open | - |
| B-026 | n/d | F16 | F12 | `state/story-case-links.json` | older plan/map (not a run) | unguarded (script-written artifacts) | open | - |
| B-027 | n/d | F08 |  | — | older plan/map (not a run) | unknown as fact (binding not derived) | open | - |
| B-028 | n/d | F11 |  | `run_suite.py:372` | older plan/map (not a run) | false blocker | open | - |
| B-029 | n/d | F08 | F11 | `s5_precheck._why_no_row` | older plan/map (not a run) | id mismatch (hand-typed fragment); silent loss | narrowed (a2298f8), remainder open | - |
| B-030 | n/d | F16 | F05 | — | older plan/map (not a run) | silent loss (json.dump drops keys) | open | - |
| B-040 | n/d | F12 | F06 | `triage.json` | older plan/map (not a run) | no way out (S7 loop success predicate) | open | - |
| B-041 | n/d | F13 | F06 | — | older plan/map (not a run) | false stop (S9 question) | open | - |
| B-042 | n/d | F08 | F01,F06 | `ticket_adapter`, `traceability.py`, `test-report.md` | older plan/map (not a run) | stale state (driver does not call steps) | open | - |
| B-043 | n/d | F13 | F18 | — | older plan/map (not a run) | hard-coded decision in prompt | open | - |
| B-044 | n/d | F01 |  | — | older plan/map (not a run) | second copy (doc contradicts code) | open | - |
| B-045 | n/d | F06 | F12 | `runtime_policy` | older plan/map (not a run) | second copy (three counters) | open | - |
| B-046 | n/d | F06 | F17 | — | older plan/map (not a run) | code decides for the role; repeat spend (conductor as command runner) | open | - |
| B-047 | 27.09 | F07 |  | `gate_preflight` | older plan/map (not a run) | no executor for a person's word | open | - |
| B-048 | n/d | F03 | F05 | `test_stand_lease.py` | older plan/map (not a run) | unknown as fact; no way out; test fails only under load | open (narrowed in debt file) | - |
| B-049 | n/d | F11 | F06 | — | older plan/map (not a run) | silent loss (repair does not reach person) | open | - |
| B-050 | n/d | F07 |  | — | older plan/map (not a run) | idea (single criterion) | open | - |
| B-006 | 29.09 | F06 | F10,F12,F13 | `test-report.md`, `story_run.py:1788` | older plan/map (not a run) | refusal without door; no zero outcome (manual route) | planned (d3bf441) | - |
| B-051 | n/d | F15 |  | `design/factory-map.md` | older plan/map (not a run) | idea (map in package, FR-54) | open | - |
| B-060 | n/d | F04 | F13 | `runtime_paths.py` | older plan/map (not a run) | second copy (path in gate vs contract) | open | - |
| B-061 | n/d | F08 | F13 | `check_delivery.py:568` | older plan/map (not a run) | false pass (skipped blocks nothing) | open | - |
| B-062 | n/d | F13 | F12 | — | older plan/map (not a run) | no way out (no road to a bug) | open | - |
| B-063 | n/d | F07 |  | — | older plan/map (not a run) | text to a person (ambiguous word) | open | - |
| B-064 | n/d | F07 | F05 | — | older plan/map (not a run) | idea (mechanism with no calls) | open | - |
| B-070 | n/d | F12 | F05 | — | older plan/map (not a run) | repeat spend | open | - |
| B-071 | n/d | F15 |  | — | older plan/map (not a run) | idea (switched-off mechanism) | open | - |
| B-072 | n/d | F17 |  | — | older plan/map (not a run) | repeat spend (constant prompt part) | open | - |
| B-073 | n/d | F02 |  | — | older plan/map (not a run) | repeat spend (context peak) | open | - |
| B-074 | n/d | F05 |  | — | older plan/map (not a run) | repeat spend (cache window) | open | - |
| B-075 | n/d | F05 |  | `controller.py:106` | older plan/map (not a run) | repeat spend (window size) | open | - |
| B-076 | n/d | F17 |  | `common-rules.md` | older plan/map (not a run) | repeat spend (rules injected) | open | - |
| B-077 | n/d | F14 |  | — | older plan/map (not a run) | idea (threshold awaiting owner) | open | - |
| B-078 | n/d | F02 |  | — | older plan/map (not a run) | repeat spend (unused material) | open | - |
| B-079 | n/d | F14 |  | `retro_numbers.py` | older plan/map (not a run) | measurement missing | open | - |
| B-080 | n/d | F11 |  | — | older plan/map (not a run) | idea (parallel windows) | open | - |
| B-081 | n/d | F03 |  | — | older plan/map (not a run) | idea (cost lever) | open | - |
| B-082 | n/d | F15 |  | — | older plan/map (not a run) | slow tests | open | - |
| B-084 | 29.09 | F14 |  | — | owner | idea | open | - |
| B-085 | 29.09 | F14 |  | — | owner | idea | open | - |
| B-083 | n/d | F14 |  | `sizing.json` | older plan/map (not a run) | idea | open | - |
| B-090 | n/d | F08 | F11 | `diff_scope`, `execution_fingerprint`, `manifest_from_tests`, `s5_precheck.py:327` | older plan/map (not a run) | project-specific (pytest) | open | - |
| B-091 | n/d | F14 |  | `cost_capture`, `cost_capture.py:385` | older plan/map (not a run) | project-specific (testproject1 CLI regex) | open | - |
| B-092 | n/d | F04 |  | — | older plan/map (not a run) | idea | open | - |
| B-093 | n/d | F11 | F03 | — | older plan/map (not a run) | project-specific (build not a witness) | open | - |
| B-094 | n/d | F08 | F13 | `testcase-<x>-NN.json`, `TC-NNN.md` | older plan/map (not a run) | project-specific (case file format) | open | - |
| B-095 | n/d | F02 | F07 | — | older plan/map (not a run) | idea | open | - |
| B-096 | n/d | F04 | F16 | — | older plan/map (not a run) | idea | open | - |
| B-097 | n/d | F16 | F04 | — | older plan/map (not a run) | idea (parallel stories) | open | - |
| B-100 | n/d | F19 |  | `RELEASE.md` | older plan/map (not a run) | idea (release) | open | - |
| B-101 | n/d | F15 |  | — | older plan/map (not a run) | project-specific (OS) | open | - |
| B-102 | n/d | F19 |  | — | older plan/map (not a run) | idea | open | - |
| B-103 | n/d | F19 | F17 | — | older plan/map (not a run) | idea | open | - |
| B-104 | n/d | F11 | F03 | — | older plan/map (not a run) | idea (no live acceptance) | open | - |
| B-105 | n/d | F14 |  | — | older plan/map (not a run) | idea | open (deferred by owner) | - |
| B-106 | 24.09 | F18 |  | — | older plan/map (not a run) | idea | open (deferred by owner) | - |
| B-107 | n/d | F14 |  | — | older plan/map (not a run) | repeat spend (telemetry files) | open | - |
| B-108 | 29.09 | F16 | F19 | — | lead (session) | refusal without door (guard blocks operator session) | open | - |
| B-134 | 29.09 | F15 | F19 | `tools/controller-blocks-gen.py` | lead (session) | absolute path | open | - |
| B-135 | 29.09 | F19 |  | `tools/session_context.py`, `CLAUDE.md`, `PROJECT.md`, `docs/FACTORY_RULES_INDEX.md` | lead (session) | measurement wrong (boot budget misses imports) | open | - |
| B-136 | 29.09 | F19 |  | `tools/factory_rules_index.py` | critic | false pass (working tree read, not staged) | open | - |
| B-138 | 29.09 | F19 | F14 | `tools/usage_report.py`, `references/model-rates.json`, `tools/usage_report.py:262-276` | scout | second copy (price table) | open | - |
| B-139 | 29.09 | F14 |  | `retro_numbers.cache_read_rate`, `cost_capture.resolve_rate`, `retro_numbers.py:379-396` | scout | unknown as fact (price fallback) | open | - |
| B-140 | 29.09 | F19 | F14 | `experiments/measurers/check_all_contracts.py` | critic | wrong measurement (false CATCH); hard-coded constants | open | - |
| B-141 | 29.09 | F19 | F14 | — | critic | unknown as fact (cost or 0) | open | - |
| B-142 | 29.09 | F17 | F16,F04 | `runtime_paths.py` | lead (session) | absolute path (unexpanded plugin root) | open | sib: "В драйвере закрывается экспортом `CLAUDE_PLUGIN_ROOT` (B-014); в десктопе — открыто" |
| B-143 | 29.09 | F19 | F14 | `experiments/measurers/code_friction.py`, `scripts/friction.py` | critic | wrong measurement (recovery kind, listing vs traceback) | open | - |
| B-145 | 29.09 | F06 | F03,F07 | `ticket_adapter` | critic | silent loss (stand named by person not carried) | open | - |
| B-146 | 29.09 | F11 |  | `execution_request.green_over_same_bytes`, `diff_scope` | scout | repeat spend (comment forces rerun) | open | - |
| B-147 | 29.09 | F05 | F11 | — | scout | repeat spend (62 executions, 19 instances) | open | - |
| B-148 | 29.09 | F11 | F05 | `run_suite`, `diff_scope` | scout | repeat spend | open | - |
| B-149 | 29.09 | F17 | F03,F05 | `red_sandbox.py` | scout | second copy (two contradicting probe instructions) | open | - |
| B-150 | 29.09 | F11 | F03 | — | scout | unknown as fact (stale reuse); stale state | open | - |
| B-151 | 29.09 | F07 |  | `gate_preflight.py` | scout | repeat spend (rehearsal each run) | open | - |
| B-152 | 29.09 | F08 | F11 | — | scout | code vs owner decision conflict | open (owner decision) | - |
| B-153 | 29.09 | F03 | F17,F13 | `readiness.py`, `tracker_write.probe` | critic | leaves a trace in the project (tracker GET in no-trace run) | open | sib: "Прогон без следов (B-003): `readiness.py` берёт `no_trace` только из командной строки" |
| B-154 | 30.09 | F12 | F17,F08,F16 | `artifact_supersede.py`, `plan_row.py`, `role-commands.json`, `/work/test-plan.md` | builder | refusal without door (role without Bash) | open | sib: "Для B-012 ей оставлена дверь точечных правок (Edit); «начать заново» по слову человека через драйвер — не сделано" |
| B-155 | 30.09 | F15 | F06 | `test_story_run.py`, `story_run_common.py`, `experiments/dev-speed/split_witness.py`, `docs/tasks/specs/t-089-split-test-story-r...` | lead (session) | slow tests | closed (21e2e74) | - |
| B-214 | 30.09 | F15 | F06 | `test_infra_failure.py`, `test_run_budget.py`, `test_story_run_s0.py`, `test_story_run_delivery_b.py` | critic | slow tests | open | sib: "Соседи B-155" |
| B-215 | 30.09 | F19 | F15 | `scripts/tests/test_story_run.py`, `docs/RUNBOOK.md` | critic | stale state (release copy keeps removed test) | open | sib: "Остаток — B-214, B-215" |
| B-156 | 30.09 | F19 |  | — | lead (session) | repeat spend (rerun scope) | closed (PROJECT.md rule 2) | - |
| B-157 | 30.09 | F19 |  | — | lead (session) | repeat spend (late commits) | in progress | - |
| B-158 | 30.09 | F19 |  | — | lead (session) | slow hooks (measure first) | open | - |
| B-159 | 30.09 | F19 |  | — | lead (session) | repeat spend (big reports) | closed (PROJECT.md rule 2) | - |
| B-160 | 30.09 | F19 |  | — | lead (session) | repeat spend (full canon run) | closed (PROJECT.md rule 2) | - |
| B-161 | 30.09 | F12 |  | `handoffs/vocabulary.yaml` | builder | second copy (one vocabulary for S4 and S5) | open | yes: "после t-016 C критик кейсов (S4) тоже может сказать `unverified`" |
| B-162 | 30.09 | F19 |  | `stage_compare.py`, `report_run.py`, `paths.py`, `prepare_copy.py` | scout | project-specific (hard-coded run tables) | open | - |
| B-163 | 30.09 | F03 |  | `stand_health` | lead (session) | unknown as fact (stand hang vs slow); refusal without door | open | - |
| B-164 | 30.09 | F06 | F05,F12 | `story_run.py`, `repair_route.route` | critic | second copy (resume path vs repair_route) | open | yes: "комментарий «the same rule stage_S5 applies» после B-007 неверен" |
| B-165 | 30.09 | F06 | F07 | `factory-backlog.md` | builder | silent loss (person's word not in backlog) | open | yes: "Проход по слову человека через вопрос «поколение пакета» / «режим прогона» (B-014) пишет только `defect_found`" |
| B-166 | 30.09 | F16 | F19 | `guard_pre_tool.py`, `experiments/measurers/run_headless.py:48-51` | critic | absolute path (literal plugin root in refusals) | open | sib: "в драйвере работает благодаря экспорту B-014, в десктопе — нет" |
| B-167 | 30.09 | F06 | F12 | `run()`, `story_step` | critic | false refusal (mode checked only at start) | open | yes: "Режим прогона (B-014) проверяется только при старте `run()`" |
| B-168 | 30.09 | F11 |  | `exit_gate.py:796-804` | builder | stale state (released without recheck) | open | - |
| B-169 | 30.09 | F11 | F12,F15 | `run_suite.py:10`, `story_step.py:148`, `form_selftest.py:244`, `evals/plugin-eval-benchmark.json:103` | builder | project-specific (TC-n form leftovers) | open | sib: "Остатки формы `TC-n` в текстах кода" |
| B-170 | 30.09 | F10 | F11,F05 | — | builder | false completion (manual half skipped) | open | - |
| B-171 | 30.09 | F06 | F07 | `conductor()`, `human-questions.md`, `ask()` | builder | text to a person (raw relays) | open | sib: "оставшиеся после B-009 ч. 2" |
| B-172 | 30.09 | F02 | F06,F05,F17 | `source_inventory.completeness`, `scripts/source_inventory.py:904-977`, `story_run.record_gaps`, `story_run.py:1481-1493` | live run | false pass (inspection closed by accepted gap); self-declared manifest keys unread | open | - |
| B-173 | 30.09 | F19 | F08,F06 | `stage_compare.py`, `test-plan.md`, `pipeline.json` | live run | unknown as fact (None vs 0 in measurer); missing stamp | open | - |
| B-174 | 30.09 | F06 | F02,F07 | — | live run | code did not do what the earlier fix promised; loop to conductor | open | yes: "хотя после прогона 3 запись `accept-gap` должна идти кодом" |
| B-175 | 30.09 | F12 | F06,F17 | `handoff_check` | live run | role fights the code (claims without Bash); conductor instead of resume | open | - |
| B-176 | 30.09 | F16 | F15,F12,F06 | `artifact-writers.json`, `work/test-cases/critic-findings.md`, `work/test-code/critic-findings.md`, `guard_pre_tool.py` | builder | second copy (five readers of one registry) | open | yes: "После t-078 в `artifact-writers.json` появились ключи-пути" |
| B-177 | 30.09 | F07 | F06 | `critic_rollcall.py` | live run | text to a person (factory-fixable shown to person) | open | - |
| B-178 | 30.09 | F06 |  | `story_run.py`, `driver-runs.json`, `print(..., flush=True)`, `run()` | live run | race (block-buffered log) | open | - |
| B-179 | 30.09 | F11 | F08,F06 | `window_record`, `acceptance.validate_window` | live run | false pass (window accepted with no results) | open | - |
| B-180 | 30.09 | F11 |  | `run_suite.py`, `red_sandbox` | builder | repeat spend (cannot reparse) | open | yes: "после исправления правила rootdir (t-080) старые блоки S5 cmp1 нельзя перепарсить кодом" |
| B-181 | 30.09 | F07 | F03 | `gate_brief.attribute`, `requirements-readiness.json` | live run | silent loss (answer by id does not close registry question) | open | - |
| B-182 | 30.09 | F13 | F12 | — | live run | no way out (no road to bug without red test) | open | rec: "та же находка была у владельца в driver3" |
| B-183 | 30.09 | F12 |  | `handoff_init` | live run | field without producer (no handoff contract) | open | - |
| B-184 | 30.09 | F14 | F19 | `report_run.py`, `driver-runs.json`, `retro_numbers` | live run | wrong measurement (cumulative total summed) | open | - |
| B-185 | 30.09 | F17 | F08 | `runs/cmp1-case-quality.md` | critic | weak oracle (Then cannot tell a broken twin) | open | - |
| B-186 | 30.09 | F14 | F06 | `factory_dashboard.py`, `cost_capture`, `state/driver-runs.json`, `report_run.py` | owner | wrong measurement (roles collapsed to orchestrator) | closed (83cb92b) | - |
| B-187 | 30.09 | F14 |  | — | owner | idea (optional --task view) | closed (83cb92b) | - |
| B-188 | 30.09 | F17 |  | — | owner | idea (P16 in role texts) | open | - |
| B-189 | 30.09 | F08 | F17 | — | critic | coverage gap (grammar partitions) | open | - |
| B-191 | 30.09 | F17 | F08,F14 | `s5.md`, `manifest_from_tests` | owner | role text lacks the principle; code may force one-instance-one-case | open | - |
| B-192 | 30.09 | F14 |  | `metric_signals.refresh`, `qa-factory/state/metric-signals.json` | owner | second copy (duplicate warning id) | closed (3bfe8fd) | - |
| B-194 | 30.09 | F09 | F11,F12 | `s5-notes.md`, `ticket-snapshot.json`, `TP1-13797_TC_002.md`, `s5-notes.md:7` | live run | unchecked claim; expectation changed to the code (code as oracle) | open; cause checked 30.09, factory defect stays | - |
| B-195 | 30.09 | F14 |  | `dashboard_cost_groups.group_cost` | critic | wrong measurement (session counted whole under each label) | open | - |
| B-196 | 30.09 | F14 | F06 | `artifacts/<T>/state/driver-runs.json` | critic | wrong grouping (driver sessions Unclassified) | open | - |
| B-197 | 30.09 | F14 |  | `factory_dashboard.py`, `metrics.json`, `metrics_projection.project` | critic | validator writes (FR-45) | open | - |
| B-198 | 30.09 | F14 |  | — | lead (session) | absolute path (file:/// links) | open | - |
| B-199 | 30.09 | F14 |  | `factory_dashboard.py:2197`, `retro_numbers.orchestrator_by_stage` | builder | wrong measurement (neighbour of B-186) | open | sib: "Соседи B-186, не починенные в t-083" |
| B-200 | 30.09 | F19 |  | `.claude/settings.json`, `AGENTS.md`, `$CLAUDE_PROJECT_DIR/tools/<x>.py`, `tools/wiring_check.py:242` | lead (session) | absolute path (relative hook path locks session) | open (low priority) | - |
| B-204 | 30.09 | F19 |  | `tools/dispatch_manifest.py`, `docs/SIBLING_MAP.md`, `scratchpad/t093/probe.py` | critic | second copy (two readers of one dispatch text) | open | - |
| B-206 | 30.09 | F13 | F08 | `test-report.md` | owner | text to a person (verdict without numbers); second copy (bugs dir) | open | - |
| B-208 | 30.09 | F11 | F13,F17 | `work/run-report.json`, `finalize_task.py:262-269`, `finalize_task.py:133-166`, `finalize_task.py` | owner | ghost rows; text to a person (factory reason put to person) | open | - |
| B-209 | 30.09 | F13 | F17,F08 | `references/templates/test-report.md`, `qa-doc-scribe.md` | owner | stale report; text to a person | open | - |
| B-210 | 30.09 | F13 | F14,F06 | `pipeline.json`, `driver-runs.json` | owner | unknown as fact (size not recorded though known) | open | - |
| B-211 | 30.09 | F13 | F08 | `test-report.md` | owner | idea (composite task: report tells the truth) | open | - |
| B-212 | 30.09 | F13 | F08,F06 | `retro.md`, `traceability.py`, `references/templates/test-report.md:81-83` | owner | stale report; silent loss (open questions have no place) | open | - |
| B-213 | 30.09 | F13 | F17,F12 | `templates/test-report.md:61`, `agents/qa-doc-scribe.md:82`, `grammar.py:98`, `test-report.md:37-43` | owner | field without producer (risk of unproven) | open | - |
| B-216 | 30.09 | F07 | F08,F13,F17 | — | owner | silent loss (answer not carried to plan row and case) | decided by owner 30.09 (spec t-113) | - |
| B-217 | 30.09 | F11 |  | `execution_fingerprint.py:274-291`, `github_webhook_filter_test_data.py`, `manifest_from_tests` | designer | detector hole (function_sha blind to data module) | open | yes: "проверка B-194 этого не увидит" |
| B-218 | 30.09 | F12 |  | `s7-automator-to-analyst.yaml:65`, `s7-analyst-to-scribe.yaml:106`, `s5-automator-to-runner.yaml:89`, `s5-automator-to-critic.yaml:74` | designer | unchecked claim | open | sib: "Соседи B-194" |
| B-219 | 30.09 | F14 |  | `cost_capture.collapse_requests`, `scripts/cost_capture.py:295-325` | designer | wrong measurement (driver sessions collapsed at capture) | open | - |
| B-220 | 30.09 | F07 | F04 | `config.json`, `work/briefs/S5-qa-automator-1-decisions.m...`, `story_run` | designer | no executor for a person's word; role edits project config | open | - |
| B-221 | 30.09 | F08 |  | `s5_precheck`, `s5_precheck.py:695-703` | designer | false pass (docstring counts as evidence) | open | - |
| B-222 | 30.09 | F06 | F14 | `driver-runs.json` | critic | unknown as fact (meaning of total_cost_usd differs per run) | open | yes: "Посылка B-184 «суммировать неверно» верна только для нарастающего журнала" |
| B-223 | 30.09 | F14 |  | `retro_numbers.cost_files`, `story_budget.py:116` | critic | wrong measurement (sessions dropped from story spend) | open | - |
| B-224 | 30.09 | F05 | F07 | `pipeline.json`, `controller.py:1087`, `state/controller.json` | critic | silent loss (design review author empty) | open | - |
| B-225 | 30.09 | F14 | F04 | `qa-factory/config.json`, `cost_capture`, `cost_capture.py:141-142`, `references/model-rates.json` | owner | wrong measurement (project price table over catalog) | open | - |
| B-226 | 30.09 | F14 |  | — | owner | wrong measurement (price must converge from two sources) | open (decision P18) | - |
| B-227 | 30.09 | F10 | F11,F08 | — | owner | no executor (ladder steps 3 and 5) | open (decision P19) | - |
| B-228 | 30.09 | F14 |  | `main()`, `cost_capture.py:1274-1285` | designer | race (lock gives up silently); silent loss (session tail) | open | - |
| B-229 | 30.09 | F19 | F14 | — | owner | idea (skill) | open | - |
| B-230 | 30.09 | F19 |  | `BACKLOG.md` | owner | idea (work organisation) | open | - |
| B-231 | 30.09 | F02 | F01 | `ticket_adapter.py` | owner | no way to give the word before the run | open | - |
| B-232 | 30.09 | F02 |  | — | lead (session) | own output read as source | open | - |
| B-233 | 01.10 | F04 | F03,F16,F15 | `readiness.json`, `docs/tasks/specs/t-232-reinstall-equals-f...` | owner | stale state (generations); two copies of versions | in progress (spec t-232) | - |
| B-234 | 01.10 | F04 |  | `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md` | owner | idea (onboarding takes project rules) | open | - |
| B-235 | 01.10 | F02 | F01,F06 | `source_inventory.py:279`, `ticket.json`, `story_run.py:3244`, `references/jira-direct-access.md:69-76` | owner | repeat spend (noise in ticket); LLM agent as data source | open (D-06) | - |
| B-236 | 01.10 | F01 | F06,F19 | `experiments/cmp2-15045/answers/cmp2-s0-ti...`, `state/driver-tmp/ticket-TP1-15045.md`, `story_run.py:3238`, `cmp2.md` | lead (session) | unknown as fact (provenance "file"); two copies of the ticket | open | - |
| B-237 | 01.10 | F05 | F02 | `comments.md`, `context-bundle.json`, `source-inventory.json`, `context-manifest.json` | owner | repeat spend (JSON form of lists) | open (measure first) | - |
| B-238 | 01.10 | F14 | F01 | — | lead (session) | wrong measurement (ticket fetch unpriced) | open | - |
| B-239 | 01.10 | F18 | F04 | `ai-teammate.yml`, `external_writes.py`, `story_run` | owner | no guard (second run of a story) | open | - |
| B-240 | 01.10 | F02 |  | `source_inventory.py:423` | owner | repeat spend (attachment policy) | open | - |
| B-241 | 01.10 | F18 |  | `external_writes.py` | owner | text format (markup to Jira) | open | - |
| B-242 | 01.10 | F04 | F16 | — | owner | idea (pinned model id check) | open | - |
| B-243 | 01.10 | F18 | F19 | `CLAUDE.md`, `tools/kb_publish.py` | owner | idea (KB publication by REST) | open (owner experiment first) | - |
| B-244 | 01.10 | F19 |  | `ai-teammate.yml`, `experiments/measurers/run_headless.py` | owner | idea (CI run) | open (low priority) | - |
| B-245 | 01.10 | F19 |  | `templates/config.json`, `references/templates/config.json`, `tools/dispatch_manifest.py` | lead (session) | missing check (given paths after send) | open | - |
| B-246 | 01.10 | F02 | F01 | `mr-access-routes.md` | critic | unknown as fact (lost login = not found) | open | sib: "Близнец потери авторизации на пути VCS/MR" |
| B-248 | 01.10 | F04 | F08,F13 | `onboard_apply`, `check_coverage`, `event_store.py:26`, `bug_records.py:63` | builder | wrong order (check before retire); second copy (path normalisers) | open | - |
| B-250 | 02.10 | F04 | F14,F16 | `rehearsal.md`, `state/dashboard-dirty.json`, `state/dashboard-refresh.json` | rehearsal | race (hook-rewritten files in yes-hash) | open | - |
| B-251 | 02.10 | F05 | F04 | `controller` | rehearsal | absolute path; stale state (not portable) | open | sib: "класс B-249" |
| B-252 | 02.10 | F10 | F03 | `manual_capture`, `PlaywrightBackend.login()` | rehearsal | false ok before landing (race) | open | - |
| B-257 | 02.10 | F03 | F11,F07 | `runtime_probe.py:283`, `run_suite.probe_runtime`, `execution_request`, `qa-factory/records/stand-identity.json` | owner | code decides for the person (env_blocked); project-specific (one nginx path) | open (t-300) | - |
| B-254 | 02.10 | F10 | F03 | `manual_capture`, `references/manual-capture-steps.json`, `docs/SIBLING_MAP.md` | rehearsal | second copy (two descriptions of stand login) | open | - |
| B-249 | 01.10 | F16 | F04,F14,F03,F12 | `runtime_paths`, `host_probe.py:33`, `metric_signals`, `metrics_projection` | scout | second copy (layout literal in ten places) | open | sib: "переезд папки (как `journal.jsonl` state/ → records/) чинится в десятке мест" |
| B-205 | 30.09 | F15 | F12 | `design/state-exits.md`, `test_story_run.py`, `test_gate_brief_and_retro.py` | designer | claim without proof (doc names a test) | open | - |
| B-203 | 30.09 | F19 |  | `experiments/dev-speed/hook-latency.md` | builder | slow hooks | open (low priority) | - |
| B-201 | 30.09 | F19 |  | `dispatch_gate.py` | lead (session) | missing check (dispatch completeness) | open | - |
| B-202 | 30.09 | F19 |  | — | owner | repeat spend (review at the end) | open | - |
| B-144 | 29.09 | F15 | F19 | `test_human_questions.py:172`, `tests/harness.py`, `no_claude.py` | builder | repeat spend (tests start real claude) | closed by code (t-036); remainder open | - |
| B-137 | 29.09 | F19 |  | `tools/factory_rules_index.py` | critic | silent pass (malformed rule line) | open | - |
| B-110 | n/d | F20 |  | — | older plan/map (not a run) | idea (unbuilt judgments) | open | - |
| B-111 | n/d | F20 |  | `judge_diff.py` | older plan/map (not a run) | idea (judge without call point) | open | - |
| B-112 | n/d | F12 | F08 | `contract`, `vocabulary.yaml`, `candidate_evidence.py:7` | older plan/map (not a run) | second copy (vocabulary) | open | - |
| B-120 | n/d | F06 | F01 | `story_run.py:1536` | live run | false refusal (check always true) | open | - |
| B-121 | n/d | F05 | F16,F14 | `cost_capture.py:1260`, `host_dispatch.py:29` | live run | wrong source (parent transcript) | open | - |
| B-122 | n/d | F08 | F13 | `check_delivery.reason_owner()` | live run | text to a person; wrong owner (our bookkeeping as product) | open | - |
| B-123 | n/d | F08 |  | — | live run | false "not planned"; silent loss (key swallowed) | open | - |
| B-124 | n/d | F13 |  | `build_report.py` | live run | role fights the code (self-made builders) | open | - |
| B-125 | n/d | F03 | F16 | `env_probe.py` | live run | silent flag ignore | open | - |
| B-126 | 29.09 | F16 | F12 | `vocabulary.yaml` | live run | text to a role; code decides by phrase (FR-12) | open | - |
| B-127 | n/d | F02 |  | — | live run | role fights the code | open | - |
| B-128 | n/d | F14 | F07 | — | live run | code decides for the person (size by ticket type) | open | - |
| B-129 | n/d | F02 |  | — | live run | text to a person (route not stated) | open | - |
| B-130 | n/d | F14 | F16,F17 | — | live run | noise to roles (hook text each write) | open | - |
| B-131 | n/d | F11 |  | `exit_gate.py:223` | live run | truncated text (waiver cannot be found) | open | - |
| B-132 | n/d | F05 |  | — | live run | stale state (legacy story) | open | - |
| B-133 | n/d | F17 |  | — | live run | role text lacks fact | open | - |
| B-190а | 30.09 | F05 | F02 | — | critic | role lacks the precedent helpers (brief) | open | - |
| B-190в | 30.09 | F17 |  | — | critic | role text (critic looks for duplicate helpers) | open | - |
| B-190г | 30.09 | F07 | F10,F09 | — | critic | silent loss (oracle_unknown rows not reassessed after gate A) | open | - |
| B-193а | 30.09 | F04 | F11,F17 | `config.json`, `qa-factory/config.json` | live run | role fights the code (profile command not on PATH); role edits project config | open | - |
| B-193б | 30.09 | F11 |  | — | live run | project-specific (junit id vs rootdir) | closed (t-080); remainder B-180 | - |
| B-193в | 30.09 | F08 | F17 | `s5_precheck` | live run | role fights the code (requirement learned by refusal) | open | - |
| B-193г | 30.09 | F12 |  | `handoff_check` | live run | role fights the code (handoff form 8 turns) | open | - |
| B-193д | 30.09 | F08 |  | `manifest_from_tests` | live run | role fights the code (manifest_from_tests data module) | open | - |
| B-207а | 30.09 | F03 | F11,F05 | `probe_by_code` | scout | no way out (probe passed, receipt not issued, nobody returns) | open | - |
| B-207б | 30.09 | F11 | F08,F17 | `proof_level.proof_required()`, `scripts/proof_level.py:258-273`, `manifest_from_tests.py:696` | scout | false pass (new row decided by absent flag) | open | - |
| B-207в | 30.09 | F08 | F11,F05 | `check_delivery.py:449`, `window_record.py:448`, `controller.py:2925`, `templates/test-report.md:30` | scout | false pass (gates skip rows with proof_required false) | open | - |
| B-247а | 01.10 | F02 |  | `source_inventory.py:218`, `work/source-inventory.json` | critic | repeat spend (login probe per process) | open | sib: "Мелочи пути REST после критика t-280" |
| B-247б | 01.10 | F06 |  | `py_stdout` | critic | unbounded wait (no timeout) | open | sib: "Мелочи пути REST после критика t-280" |
| B-247в | 01.10 | F02 |  | `source_exclusions.py:217` | critic | false alarm (verified not cutting) | closed (t-282 verified) | sib: "Мелочи пути REST после критика t-280" |
| B-247г | 01.10 | F02 | F01,F03,F07 | `source_exclusions._BROWSE_PATH_RE`, `reference-kinds.json`, `source_inventory`, `rsplit("/browse/")` | builder | second copy (hand-written twins of reference-kinds rule; /browse/ in ~5 places) | open | sib: "аналоги от t-282" |
| B-253а | 02.10 | F12 |  | `scope: []` | rehearsal | no way out (no zero outcome in S7 form) | open | - |
| B-253б | 02.10 | F12 |  | `project_decisions add-finding` | rehearsal | refusal without door (invalid finding scope) | open | - |
| B-253в | 02.10 | F17 | F06 | `finish --ignore-handoff` | rehearsal | refusal without door (conductor stops instead of the named door) | open | - |
| B-253г | 02.10 | F06 |  | `sys.stdout.reconfigure(line_buffering=True)`, `driver-runs.jsonl` | rehearsal | race (block-buffered stdout); silent death | open | - |
| B-253д | 02.10 | F07 | F06 | `human-questions.md`, `waiver.py` | rehearsal | text to a person (5 human-questions rules broken) | open | - |
| B-253е | 02.10 | F07 |  | — | rehearsal | text to a person (form of word not shown next to card) | open | - |
| B-253ж | 02.10 | F11 | F07 | `waiver --block "review is missing"` | rehearsal | false promise (window does not read the word) | open | - |
| B-253з | 02.10 | F03 | F04 | `--suggest --write`, `--checkout` | rehearsal | absolute path (--checkout) | open | - |
| B-255а | 02.10 | F03 |  | `probe_by_code.py:479`, `run_suite.probe_runtime` | critic | second copy (probe check requires matched) | open (cluster t-298) | sib: "Аналоги, обещанные приёмками t-279/t-287 как «B-line», но не записанные" |
| B-255б | 02.10 | F11 | F03 | `environment_preparation.py:325` | critic | false alarm (verified: leave as is) | closed (verified, leave as is) | sib: "Аналоги, обещанные приёмками t-279/t-287 как «B-line», но не записанные" |
| B-255в | 02.10 | F08 | F07 | `planning_contract._unmet_preconditions`, `gate_preflight:2652` | critic | second copy (preconditions prepared twice) | open | sib: "Аналоги, обещанные приёмками t-279/t-287 как «B-line», но не записанные" |
| B-255г | 02.10 | F06 | F01 | `story_run.py:3028` | critic | text to a person (shape claim wrong for wiki paste) | open | sib: "Аналоги, обещанные приёмками t-279/t-287 как «B-line», но не записанные" |
| B-255д | 02.10 | F03 |  | — | critic | n/d (item names only username_ref) | open | sib: "Аналоги, обещанные приёмками t-279/t-287 как «B-line», но не записанные" |
| B-255е | 02.10 | F07 | F03 | `gate_preflight:2068` | critic | unknown as fact (gate A skips profile, stand unchecked unsaid) | open (cluster t-298) | sib: "Аналоги, обещанные приёмками t-279/t-287 как «B-line», но не записанные" |
| B-255ж | 02.10 | F06 | F03 | `story_run.py:5651` | critic | unknown as fact (printed "proved" on unknown) | open (cluster t-298) | sib: "Аналоги, обещанные приёмками t-279/t-287 как «B-line», но не записанные" |
| B-256а | 02.10 | F01 |  | `ticket_adapter.py:157` | critic | silent loss (h2. Comments parsed as empty); wrong numbers compared | open | sib: "Хвосты t-287 по критику t-295" |
| B-256б | 02.10 | F01 |  | — | critic | wrong owner (config error owned by tracker with retry); no error object under --json | open | sib: "Хвосты t-287 по критику t-295" |
| B-256в | 02.10 | F01 | F02 | — | critic | silent choice (first of two); one function two rules | open | sib: "Хвосты t-287 по критику t-295" |
| B-256г | 02.10 | F06 | F07 | `story_run.py:3508`, `human-questions.md`, `human_text` | critic | text to a person (key names in question body) | open | sib: "Хвосты t-287 по критику t-295" |

### A2. cmp2 findings F-cmp2-1..30 (`experiments/cmp2-15045/cmp2.md`, run 01.10)

| id | date | F | also | file(s)/function named in the source | found by | class | status | fix-of-fix |
|---|---|---|---|---|---|---|---|---|
| F-cmp2-1 | 01.10 | F18 |  | `jira-assistant`, `~/bin/testproject1` | live run | environment (owner machine); role cannot call CLI | closed (shim outside package) | - |
| F-cmp2-2 | 01.10 | F18 |  | `testproject1 assistants chat` | live run | environment (owner machine); assistant not registered | open (owner action) | - |
| F-cmp2-3 | 01.10 | F01 |  | `ac_source: heading <name>` | live run | project-specific (heading list in code); agent fallback | open (tracked t-267 / B-236 item 2) | - |
| F-cmp2-4 | 01.10 | F02 |  | `test_repo`, `implementation_repos` | live run | project-specific; MR head not found in test repo | open | - |
| F-cmp2-5 | 01.10 | F19 |  | `prepare_copy.py` | live run | tool lacks --base | closed (rehearsal step 1 uses --base) | - |
| F-cmp2-7 | 01.10 | F02 |  | `work/source-exclusions.json`, `skip_sources_late` | live run | text to a person (false statement "ignored") | open | - |
| F-cmp2-8 | 01.10 | F02 |  | `*_QA_Factory_Test_Review_*.md` | live run | own output read as source | closed by word (stop 3) | - |
| F-cmp2-9 | 01.10 | F11 | F06 | — | live run | code rejects tolerable output (form + prose); repeat spend | closed by word | - |
| F-cmp2-10 | 01.10 | F17 | F08,F05 | `artifact-contract-plan.md`, `coverage-observation-v1` | live run | contract not told to role (FR-38/FR-11); role fights the code (tool map for no-Bash roles) | closed (t-206), remainder open | - |
| F-cmp2-11 | 01.10 | F05 | F06 | `recover`, `driver-runs.jsonl` | live run | unknown as fact (question the factory could answer) | open | - |
| F-cmp2-12 | 01.10 | F05 | F07 | `briefs/<dispatch>-decisions.md` | live run | silent loss (person's word truncated ~300 chars) | open | - |
| F-cmp2-13 | 01.10 | F06 | F12 | — | live run | repeat spend (rework loop, new session each time) | open | - |
| F-cmp2-14 | 01.10 | F08 |  | `coverage_contract.py` | live run | refusal without door (names no field/value) | open | - |
| F-cmp2-15 | 01.10 | F08 |  | `planning_contract.row_requirements` | live run | false refusal (key not read) | closed (t-209), remainder open | - |
| F-cmp2-16 | 01.10 | F06 | F12 | `story_step finish` | live run | repeat spend (loop without cap; refusal text not carried) | open | - |
| F-cmp2-17 | 01.10 | F07 | F06,F12 | `gate_preflight`, `case_versions --all` | live run | text to a person (gate shown with 15 factory_fixable); stage closed before rework | open (t-211/t-214 gate_repair follows) | - |
| F-cmp2-18 | 01.10 | F07 |  | `gate_preflight` | live run | text to a person (21 cards, 16 not the person's) | open | - |
| F-cmp2-19 | 01.10 | F19 |  | `prepare_copy.py`, `poetry install` | live run | unknown as fact (install exit 0, SDK not importable) | closed (rehearsal step 1 checks import) | - |
| F-cmp2-20 | 01.10 | F07 | F03 | `gate_preflight.check_s5_credentials` (:1568), `env_probe` | live run | second detector with same flaw; project-specific (all config keys asked) | open | sib: "(FR-54, возврат проблемы 23.09)" and "это уже фиксили" |
| F-cmp2-21 | 01.10 | F11 | F06,F08 | `s5_precheck.py:1890`, `role_cli.REPAIR_MARKER`, `story_run.match_known` (:333) | live run | refusal without marker; text to a person (conductor x3) | closed (t-213) | sib: "Класс: любой скрипт, печатающий отказ роли без маркера" |
| F-cmp2-22 | 01.10 | F06 | F07 | `story_run.py:5040-5050` | live run | wrong attribution (quoted dispatch id parsed) | open | - |
| F-cmp2-23 | 01.10 | F06 | F05 | `story_run.handle_refusal` (:2411) | live run | no move for state (FR-42) | open | sib: "(FR-42, аналог t-210)" |
| F-cmp2-24 | 01.10 | F03 | F11,F07 | `execution.runtime_probes.<profile>`, `execution_request.py:1856`, `runtime_probe.py --suggest` | live run | late discovery ($2.3 wasted); silent unknown (FR-15) | open | - |
| F-cmp2-25 | 01.10 | F07 | F03,F11,F04 | `run_mapping`, `--reparse-block`, `execution_prerequisites.package_manager` | live run | no executor for a person's word; refusal advice false | open | - |
| F-cmp2-26 | 01.10 | F03 | F07,F11 | `environments[localhost].limits` | live run | stand limit unknown until after dispatches | open | - |
| F-cmp2-27 | 01.10 | F07 | F06,F11 | `waiver.py`, `record_by_code` | live run | no executor for a person's word (conductor did not record) | open | - |
| F-cmp2-28 | 01.10 | F11 | F06 | `window_record.py`, `story_step finish`, `REPAIR_MARKER` | live run | no way out (null outcome FR-23); loop without cap ($7.28) | open | sib: "(как F-cmp2-16/17)" |
| F-cmp2-29 | 01.10 | F03 | F06,F07 | `runtime_probe.py` | owner question | unknown as fact (liveness is not identity) | open | - |
| F-cmp2-30 | 01.10 | F19 | F01 | `driver-tmp/`, `story_run.py:3238` | lead (self) | provenance read from carrier name; unknown as fact | closed (B-236, D-06, t-267 s0) | - |
| F-cmp2-6 | 01.10 | F15 | F03,F14,F16 | `selftest.py`, `stand_lease`, `test_slices_on_demand`, `test_dashboard_task_binding`, `test_refusal_registry` | test | test fails only under load; stale anchor / golden after re-cut | open | yes: "закреплённая фраза контракта ушла из среза критика после ночной нарезки" |

### A3. rehearsal defects 1-13 (`experiments/cmp2-15045/rehearsal.md`, night 01->02.10)

| id | date | F | also | file(s)/function named in the source | found by | class | status | fix-of-fix |
|---|---|---|---|---|---|---|---|---|
| rehearsal-1 | 02.10 | F16 | F04,F15 | `guard_pre_tool.py:1701`, `refusal_registry.REGISTRY`, `install_smoke.py` | rehearsal | second copy (refusal missing from registry) | closed (t-286) | - |
| rehearsal-2 | 02.10 | F04 |  | `onboard_apply --listing` | rehearsal | refusal catches the session that must pass it (FR-57/FR-2/FR-4) | closed (t-288) | - |
| rehearsal-3 | 02.10 | F04 | F14,F16 | `state/dashboard-dirty.json`, `dashboard-refresh.json` | rehearsal | race (hook rewrites vs yes-hash) | open (B-250) | - |
| rehearsal-4 | 02.10 | F11 | F07 | `waiver --block "review is missing"` | rehearsal | false promise (word not read by window) | open (B-253ж) | - |
| rehearsal-5 | 02.10 | F05 | F04 | `known_paths`, `%TEMP%\cmp2-pkg` | rehearsal | absolute path; stale state (not portable) | open (B-251) | - |
| rehearsal-6 | 02.10 | F10 | F11,F06 | `S6-qa-runner-1` | rehearsal | false refusal (lanes for manual cases); conductor for deterministic action (FR-48) | closed (t-290) | - |
| rehearsal-7 | 02.10 | F10 | F05,F06 | `run_manual_block`, `controller.prepare`, `story_run.py:4887`, `controller.py:793` | rehearsal | traceback instead of refusal (P1) | closed (t-289) | - |
| rehearsal-8 | 02.10 | F10 | F03 | `manual_capture ui`, `login by code` | rehearsal | false ok before landing; race | open (B-252) | - |
| rehearsal-9 | 02.10 | F12 |  | S7 handoff form | rehearsal | no way out (no zero outcome, FR-23) | open (B-253а) | - |
| rehearsal-10 | 02.10 | F12 |  | `project_decisions add-finding` | rehearsal | refusal without door (invalid finding scope) | open (B-253б) | - |
| rehearsal-11 | 02.10 | F17 | F06 | `finish --ignore-handoff` | rehearsal | refusal without door (conductor stops instead of the named door) | open (B-253в) | - |
| rehearsal-12 | 02.10 | F06 |  | `flush=True` | rehearsal | race (block-buffered stdout); silent death of driver | open (B-253г) | rec: "FR-43 — B-линия" |
| rehearsal-13 | 02.10 | F07 | F06 | `human-questions.md` | rehearsal | text to a person (5 rules broken by factory text) | open (B-253д) | - |

### A4. run-5 (driver3) findings 14-25 of 27.09 (`experiments/measurers/runs/driver3-s8-findings.md`; no B id, ids written `run5-nn`)

| id | date | F | also | file(s)/function named in the source | found by | class | status | fix-of-fix |
|---|---|---|---|---|---|---|---|---|
| run5-14 | 27.09 | F08 | F11 | `finalize_task.py:264`, `node_ids.py`, `manifest_from_tests.py`, `manifest_put.py`, `s5_precheck.py` | live run | id mismatch; tool not wired (FR-17) | closed (a2298f8), remainder open | sib: "Это тот же урок, что и снятые 8 строк, только слоем глубже" |
| run5-15 | 27.09 | F08 | F13 | `ledger.py:237` | live run | text to a person (unverified shown as rejected) | closed (9a16c31) | - |
| run5-16 | 27.09 | F03 | F11 | `red_sandbox.py --probe`, `probe_by_code.py` | live run | field without producer (FR-11) | closed by code (9a16c31), proven only live | - |
| run5-17 | 27.09 | F08 | F13,F12 | `check_delivery.py:568`, `reason_owner()`, `FACTORY_BOOKKEEPING_PHRASES` | live run | false pass (skipped blocks nothing); text to a person (our bookkeeping as product) | layer 2 closed (b409fc4); layers 1,3 open | - |
| run5-18 | 27.09 | F05 | F06 | `next_action`, `retro_pending` | live run | silent loss (closed + retro_pending) | closed (c406b0a) | - |
| run5-19 | 27.09 | F18 | F06,F13 | `tracker_write.py --record confirmed` | live run | capability probed and advertised against standing decision (FR-36) | open (debt FR-36) | - |
| run5-20 | 27.09 | F07 | F13 | `bug-drafts/` | live run | packet contradicts itself (FR-10) | closed (22c8663) | - |
| run5-21 | 27.09 | F06 | F05,F07,F15 | `story_run.py:2153`, `dispatch_action`, `controller.py:3488` | live run | silent loss (answer swallowed); code decides by phrase list (FR-12); eaten escape byte | closed (c406b0a) | rec: "ловушка №1 сработала в четвёртый раз, и не сегодня" |
| run5-22 | 27.09 | F13 | F06 | — | live run | no zero outcome (nothing goes out) | closed (1df9fcc B-003) | - |
| run5-23 | 27.09 | F04 | F13 | `qa-factory/bugs`, `bugs/` | live run | second copy (path in decision vs contract) | open (B-060) | - |
| run5-24 | 27.09 | F14 |  | `cost_files()`, `story_spend()`, `driver_sessions(troot)` | live run | wrong measurement (operator session as story money) | closed (db39837) | self: "без него сужение молча не работало, на чём первая попытка и провалилась" |
| run5-25 | 27.09 | F19 | F14 | `report_run.py --left-cache`, `runs/compare-off.json` | live run | wrong measurement (cache applied to any run) | closed (fix named in source) | - |

### A5. cmp1 defects fixed during the run (`experiments/measurers/runs/cmp1.md` "6 дефектов", commit `f73a5ae`; the three without a B id)

| id | date | F | also | file(s)/function named in the source | found by | class | status | fix-of-fix |
|---|---|---|---|---|---|---|---|---|
| t-078 | 30.09 | F16 | F17 | `references/artifact-writers.json`, `guard_pre_tool._owner_of_path` | live run | refusal without door (role blocked from its own file) | closed (f73a5ae) | - |
| t-079 | 30.09 | F11 | F12,F06 | `story_step finish --window`, `window_record.py` | live run | contract field with no producer (FR-5/FR-48) | closed (f73a5ae) | - |
| t-080 | 30.09 | F11 |  | `execution_request.node_report_id` | live run | project-specific (id relative to cwd, not rootdir) | closed (f73a5ae); remainders B-179/B-180 | - |

### A6. other carriers: `docs/FINDINGS.md` F-1..F-3, `design/factory-rules-debt.md` (only the entry no other row carries), `answers-13797.md` (one finding)

| id | date | F | also | file(s)/function named in the source | found by | class | status | fix-of-fix |
|---|---|---|---|---|---|---|---|---|
| F-1 | 29.09 | F19 |  | PROCESS/BOOT_REPORT_PROTOCOL.md | lead (operator saw) | mandatory output skipped | closed (operator word 29.09) | - |
| F-2 | 29.09 | F19 |  | PROJECT.md item 6 | critic | spec amendment without measurement or critic-on-plan | carried as rule (PROJECT.md 6) | yes: "all traced to the Lead's own amendments" |
| F-3 | 30.09 | F19 | F15 | `test_story_run.py`, PostToolUse hooks | lead (measured) | repeat spend (verification reruns) | open (proposals) | - |
| debt-1 | 28.09 | F11 |  | `stages.json witness`, `exit_gate.witness_errors`, `check_witness.RULES` | lead (rules walk) | false pass (exit 0 for "no rule") | open | - |
| ans-13797-1 | 02.10 | F02 | F01 | `ticket-references.json`, `vcs_evidence` | live run | unknown as fact (MR rows stay not_fetched after read) | open (no B id) | - |

### A7. journal: 12 `rejected` + 1 `defect_found` (`logs/routing-log.jsonl`; details in Table D1)

| id | date | F | also | file(s)/function named in the source | found by | class | status | fix-of-fix |
|---|---|---|---|---|---|---|---|---|
| t-021 | 29.09 | F06 | F01,F15 | `story_run.py`, `ticket_adapter.py` | critic | attempt 1, failure_class capability: critic t-028: S0 block deviation goes stale and captures a later non-door S0 stop; pooled tests share a process-wide stdout redirect (FR-31); evergree | rejected/defect (journal) | - |
| t-023 | 29.09 | F03 | F11 | `probe_by_code`, `proof_level.py`, `window_record`, `red_sandbox` | critic | attempt 1, failure_class spec: critic t-030: edge rows 6/7 treated bytes only as a tie-break - dispatcher spec defect | rejected/defect (journal) | yes: "all traced to the Lead's own amendments" (F-2) |
| t-023 | 29.09 | F03 | F11 | `probe_by_code`, `proof_level.py`, `window_record`, `red_sandbox` | critic | attempt 2, failure_class spec: critic t-035: Lead's MEASURED BYTES amendment assumed one meaning of test_content_sha; second rejection -> escalation | rejected/defect (journal) | yes: "all traced to the Lead's own amendments" (F-2) |
| t-033 | 29.09 | F06 | F03,F07 | `story_run.py` | critic | attempt 1, failure_class capability: critic t-037: violates spec t-017 D2 item 5; witness not reproducible under default locale; docs contradict spec item 7 | rejected/defect (journal) | - |
| t-023 | 29.09 | F03 | F11 | `probe_by_code`, `proof_level.py`, `window_record`, `red_sandbox` | critic | attempt 3, failure_class spec: critic t-048: blocker traces to Lead's Amendment 3 (same predicate as classify) making a line heuristic load-bearing | rejected/defect (journal) | yes: "all traced to the Lead's own amendments" (F-2) |
| t-045 | 29.09 | F11 |  | `diff_scope.executable_sha` | critic | attempt 1, failure_class capability: critic t-049: B2/B3 deviate from spec text; B1/B4 are dispatcher gaps | rejected/defect (journal) | - |
| t-083 | 30.09 | F14 | F06 | `factory_dashboard.py`, `driver-runs.jsonl` | builder | attempt 1, failure_class spec: returned by builder before work: no given/owns, no --out; resubmitted under same task_id | rejected/defect (journal) | - |
| t-090 | 30.09 | F19 |  | `tools/dispatch_gate.py` | critic | attempt 1, failure_class spec: critic-on-plan REJECT: rule blocks 41 of 41 real builder prompts; extract_owns_paths errs by false pass | rejected/defect (journal) | - |
| t-149 | 30.09 | F11 | F08 | `run_history.py` | critic | attempt 1, failure_class capability: critic: builder's own "retired parameter" rule passes a renamed parameter on changed bytes with pairs=[]; verdict change without note keeps old note | rejected/defect (journal) | - |
| t-166 | 30.09 | F14 |  | `task_price()`, `driver_journal` | critic | attempt 1, failure_class spec: critic Q3: with rate_overrides range mixes list-price B with override-priced A; dispatch E2 wording caused it | rejected/defect (journal) | - |
| t-165 | 30.09 | F14 |  | `cost_capture` | critic | attempt 1, failure_class spec: critic Q2: two new stale reasons send file to unattended recapture that drops recorded money; dispatch edge wording | rejected/defect (journal) | - |
| t-214 | 01.10 | F06 | F07 | `story_run.py` gate_repair | critic | attempt 1, failure_class spec: critic C1-C3: binding override C11 not built; C2/C3 edges named only by invariant (spec defect) | rejected/defect (journal) | - |
| t-143 | 30.09 | F11 | F07 | `window_record.py`, `acceptance.py` | critic | defect_found: critic pass on accepted piece F: after waiver --block the finding is gone but brief says "1 to judge", window gaps "no critic verdict"; word must be s | rejected/defect (journal) | - |

### A8. package commits since 26.09 (the fixes; 56 = the dispatched 49 plus the 7 commits of 26.09 morning; `class` starts with the commit subject)

| id | date | F | also | file(s)/function named in the source | found by | class | status | fix-of-fix |
|---|---|---|---|---|---|---|---|---|
| 4116add | 02.10 | F04 | F09,F10,F01,F02,F11,F08,F07,F15,F03 | `ticket_light`, `controller`, `onboard_apply`, `refusal_registry` | rehearsal + cmp2 + critics | subj: Factory fixes, night integration: reinstall equals fresh (two folders records/ vs state/, runtime_pa ; reinstall equals fresh; oracle provenance; manual evidence; ticket REST; wave-3 gates; rehearsal fixes ; files 369 | closed (commit) | - |
| 21e2e74 | 30.09 | F15 | F06 | `story_run_common.py`, `split_witness.py`, `selftest` | owner/Lead measurement (F-3) | subj: Split test_story_run.py into eleven files and a shared module (B-155) ; slow tests ; files 20 | closed (commit) | - |
| 83cb92b | 30.09 | F14 | F06 | — | owner screenshot | subj: Dashboard: roles from the driver journal, optional --task view, --out and --read-only ; wrong measurement (roles collapsed) ; files 2 | closed (commit) | - |
| 015e899 | 30.09 | F14 |  | `test_metric_signals.py` | owner | subj: Dashboard: one hot-cache warning per task label, its cold sessions listed inside ; noisy warning (one per session) ; files 5 | closed (commit) | - |
| 3bfe8fd | 30.09 | F14 |  | `handoff` | owner screenshot | subj: Dashboard: each metric warning id appears once in the signals receipt (B-192) ; second copy (duplicate id) ; files 2 | closed (commit) | - |
| f73a5ae | 30.09 | F11 | F16,F12 | `window_record.py`, `controller`, `guard_pre_tool`, `story_step` | live run (cmp1) | subj: Three factory defects found by the cmp1 run of TP1-13797, fixed while the story waited ; refusal without door; contract without producer; project-specific rootdir ; files 14 | closed (commit) | - |
| 88346e7 | 30.09 | F17 | F08,F15,F04 | `case_forms.py`, `contract_slices.py`, `brief_pack`, `probe_by_code` | live run + critics | subj: Case id form as data, role texts on proof levels and the run budget, CHANGELOG ; project-specific (case id as data); role texts ; files 62 | closed (commit) | - |
| 1df9fcc | 30.09 | F06 | F12,F03,F14,F07 | `friction.py`, `infra_failure.py`, `artifact_supersede.py`, `repair_route.py` | live run (13877/cmp) | subj: Driver: infra failures, no-trace, stand entry, typed repair cause, human texts, one package generati ; infra failure as role result; text to a person; one generation ; files 25 | closed (commit) | - |
| 9a16c31 | 30.09 | F11 | F08,F03,F12,F14 | `red_sandbox`, `ledger`, `window_record`, `acceptance` | live run + critics | subj: Run budget and proof levels per test instance (D-0017..D-0020, B-002, B-010) ; repeat spend; false blocker; proof levels ; files 120 | closed (commit) | - |
| 7abde94 | 30.09 | F14 | F19 | `paths.py`, `friction.py`, `retro_numbers.py`, `code_friction.py` | owner (pre-run) | subj: Measurement ready for the comparison run (B-001, B-011, B-011b) ; wrong measurement ; files 5 | closed (commit) | - |
| d3bf441 | 29.09 | F15 |  | `selftest` | owner principles | subj: Owner's principles become factory rules FR-47...FR-57 ; rules FR-47..FR-57 ; files 3 | closed (commit) | - |
| 122d7d9 | 29.09 | F19 |  | `controller` | Lead | subj: Restructure into the factory development repo: one backlog instead of plans ; restructure ; files 1 | closed (commit) | - |
| 5a66517 | 28.09 | F15 |  | `selftest.py` | rules walk | subj: qa-factory: the build reads every file's bytes for an eaten escape sequence (FR-29) ; eaten escape byte; silent green ; files 3 | closed (commit) | rec: "Tonight it mattered twice within an hour." |
| a07c96e | 28.09 | F07 | F06 | `gate_brief`, `waiver`, `selftest` | live run (15045 earlier) | subj: qa-factory: an answer is read against the packet, and what it does not name is printed (P3) ; silent loss (answer not read against packet) ; files 4 | closed (commit) | - |
| 22c8663 | 28.09 | F07 | F13 | `critic_rollcall`, `gate_brief`, `gate_preflight`, `check_delivery` | rules walk | subj: qa-factory: one packet, one source per fact (FR-10, P21.11) ; packet contradicts itself ; files 4 | closed (commit) | sib: "gate_preflight's bug-draft check still treated silence as a review" |
| 691ee83 | 28.09 | F12 |  | `red_sandbox.py`, `probe_by_code.py`, `handoff_check`, `acceptance` | rules walk | subj: qa-factory: every required field has a producer, or the gap is declared (FR-11, P21.6) ; field without producer ; files 5 | closed (commit) | - |
| a2298f8 | 28.09 | F08 | F06,F17 | `node_ids.py`, `manifest_from_tests.py`, `manifest_put.py`, `s5_precheck` | live run 5 | subj: qa-factory: the id the manifest writes is the id pytest collects (FR-16, FR-17, P21.9) ; id mismatch ; files 7 | closed (commit) | - |
| dada152 | 28.09 | F08 | F07 | `waiver.py`, `controller`, `manifest_put`, `session_handoff` | rules walk | subj: qa-factory: every state walked, with the command that reverses it (FR-40, P21.5) ; no way out (state without reverse) ; files 8 | closed (commit) | self: "Found by writing the FR-40 walk's test" (debt file) |
| 62e5089 | 28.09 | F16 |  | `manifest_put.py`, `finalize_task.py`, `guard_pre_tool`, `controller` | rules walk | subj: qa-factory: who may write an artifact is the registry's answer, and every row is exercised (FR-39, P ; second copy (guard map vs registry) ; files 4 | closed (commit) | - |
| 3d137cd | 28.09 | F08 | F07,F15,F17 | `contract`, `manifest_put.py`, `gate_brief`, `s5_precheck` | rules walk | subj: qa-factory: five detectors stop reading prose and read a field (FR-12, P21.7) ; code reads prose by phrase list (FR-12) ; files 20 | closed (commit) | - |
| 94e8329 | 28.09 | F06 | F11,F08,F03,F12 | `node_ids.py`, `waiver.py`, `story_step`, `controller` | live run 5 | subj: qa-factory: a refusal the role's own work closes says so in the marker (P4b) ; refusal without marker travels to person ; files 8 | closed (commit) | - |
| b409fc4 | 28.09 | F13 | F08 | `check_delivery.py`, `ledger`, `acceptance`, `selftest` | live run 5 | subj: qa-factory: whose problem each delivery reason is, in data (FR-19, FR-20, P21.12) ; text to a person (our bookkeeping as product) ; files 5 | closed (commit) | - |
| b273ef1 | 28.09 | F15 | F05 | `controller` | Lead | subj: qa-factory: name the classifier that built the controller walk ; doc names its classifier ; files 1 | closed (commit) | - |
| 15c83ea | 28.09 | F05 | F03,F06,F08,F15 | `contract.py`, `selftest`, `brief_pack`, `waiver` | live run 5 | subj: qa-factory: the paths a role guesses at, and the unknowns we called facts (P22) ; paths a role guesses at; unknown as fact ; files 11 | closed (commit) | - |
| 1556e9b | 28.09 | F07 | F06,F05 | `controller`, `selftest` | rules walk | subj: qa-factory: a question answered once never comes back word for word (FR-7, P22) ; same question asked twice ; files 6 | closed (commit) | self: "the first version of the hash used re.S in the head pattern" |
| 99dd8e5 | 28.09 | F05 |  | `waiver.py`, `controller`, `acceptance`, `event_store` | rules walk | subj: qa-factory: a named route through every block of the controller (P21.4, FR-4, FR-5) ; refusal without door (blocks) ; files 8 | closed (commit) | sib: "now read the person's word like S5 does" (debt file) |
| 0febcf7 | 27.09 | F07 | F06,F15 | `human_text.py`, `story_step`, `refusal_registry`, `contract` | live run 5 | subj: qa-factory: a question is a question, and our own words go beside it (P13, FR-6) ; text to a person ; files 8 | closed (commit) | - |
| ee3150a | 27.09 | F06 | F11 | `controller`, `story_step`, `selftest` | rules walk | subj: qa-factory: a move for every state the other side can return (FR-42) ; no move for state (FR-42) ; files 5 | closed (commit) | - |
| 315e47d | 27.09 | F17 | F05 | `brief_pack.py`, `ticket_adapter.py`, `critic_rollcall`, `source_preflight` | live run 5 | subj: qa-factory: the rules code will apply, said to all twelve roles before the work (FR-38) ; rules told after the work (FR-38) ; files 7 | closed (commit) | - |
| 636b1c2 | 27.09 | F15 |  | `story_run`, `selftest` | rules walk | subj: qa-factory: finish the rules walk — FR-7 is unenforced, and the role contracts are clean ; rules walk ; files 1 | closed (commit) | - |
| c20793b | 27.09 | F15 |  | `controller.py`, `selftest.py`, `check_delivery.py`, `factory_manifest` | rules walk | subj: qa-factory: design/ for the documents nothing loads, and the list of rules this factory still breaks ; design/ documents; debt list ; files 32 | closed (commit) | - |
| 177af88 | 27.09 | F15 |  | `contract` | rules walk | subj: qa-factory: the rules every change to the factory must satisfy (FR-1 … FR-43) ; FR-1..FR-43 written ; files 4 | closed (commit) | rec: "the same defect family was fixed in the runner, the sandbox and the probe, and then happened again in the manifest" |
| db39837 | 27.09 | F14 |  | `selftest` | live run 5 | subj: TP1-13797: the story's money is the sessions the driver launched, not every session on the ticke ; wrong measurement (operator session as story money) ; files 1 | closed (commit) | self: "which is how the first attempt at this failed" |
| c406b0a | 27.09 | F06 |  | `controller` | live run 5 | subj: TP1-13797: a closed story still has its retro, and the person's order is not read by a phrase li ; silent loss (order dropped); phrase list ; files 2 | closed (commit) | - |
| e64b329 | 27.09 | F05 | F11 | `window_record.py`, `acceptance`, `waiver`, `selftest` | live run 5 | subj: TP1-13797: the S5 window gate reads a person's word like every other check ; no key for a person's word (window gate) ; files 1 | closed (commit) | - |
| 4351f4e | 27.09 | F06 |  | `story_step`, `selftest` | live run 5 | subj: TP1-13797: a refusal names its dispatch in three spellings, and all three are read ; refusal read in one spelling ; files 1 | closed (commit) | self: "The first version of the filing read the packet's `\"dispatch_id\"` key alone" |
| 4547ae7 | 27.09 | F03 | F11 | `probe_by_code.py`, `window_record.py`, `red_sandbox.py`, `manifest_put.py` | live run 5 | subj: TP1-13797: the critic's only probe can reach the window record ; critic's probe cannot reach window record ; files 2 | closed (commit) | - |
| 7f84cb1 | 27.09 | F06 | F07 | `controller`, `selftest` | live run 5 | subj: TP1-13797: an answered boundary is never re-asked with the same text ; answered boundary re-asked ; files 1 | closed (commit) | - |
| e03051a | 27.09 | F06 |  | `controller`, `selftest` | live run 5 | subj: TP1-13797: resolve_return had no move, so the person's word looped back to the same refusal ; no move (resolve_return loops) ; files 1 | closed (commit) | - |
| 808f18d | 27.09 | F08 |  | `window_record.py`, `manifest_from_tests.py`, `selftest` | live run 5 | subj: TP1-13797: the tool the automator is told to use now emits the binding the receipt requires ; field without producer (binding) ; files 2 | closed (commit) | - |
| e662eee | 27.09 | F05 |  | `dispatch_liveness`, `selftest` | live run 5 | subj: TP1-13797: the driver's own record of a session ending is liveness evidence ; unknown as fact (liveness) ; files 1 | closed (commit) | - |
| 0a43333 | 27.09 | F08 |  | `selftest` | live run 5 | subj: TP1-13797: a number that measures something is not a status code ; measure read as status code ; files 2 | closed (commit) | - |
| ccaf27a | 27.09 | F08 | F17 | `manifest_put.py`, `contract`, `selftest`, `run_suite` | live run 5 | subj: TP1-13797: one stale test row can leave the manifest — the door the role did not have ; no way out (stale test row) ; files 3 | closed (commit) | - |
| e25dc1e | 27.09 | F16 | F17,F05 | `contract`, `selftest` | live run 5 | subj: TP1-13797: the guard refused references/, the one place it calls readable ; refusal without door (guard refused readable dir) ; files 3 | closed (commit) | - |
| 3692d1f | 27.09 | F05 | F17 | `planning_contract.py`, `observation_contract.py`, `selftest` | live run 5 | subj: TP1-13797: the strategist is told what the two detectors demand, in fields, before it writes ; contract not told before the work ; files 1 | closed (commit) | - |
| 1b6c6a9 | 27.09 | F07 | F08,F17,F12,F18 | `manifest_put.py`, `case_versions.py`, `critic_rollcall.py`, `plan_row.py` | live run 5 | subj: TP1-13797: a refusal keeps its shape in every role command, and a question to a person is writte ; refusal shape; text to a person ; files 8 | closed (commit) | - |
| 4db868f | 27.09 | F17 | F16,F05,F11,F10 | `plan_row.py`, `execution_fingerprint.py`, `manual_evidence.py`, `artifact_producer.py` | live run 5 | subj: TP1-13797: an artifact is changed where it changed, and a refusal names a way the role has ; refusal naming a way the role has not ; files 20 | closed (commit) | - |
| 4b222bc | 26.09 | F12 |  | `case_versions.py`, `contract`, `plan_row`, `selftest` | live run 5 | subj: TP1-13797: a fact keeps its name, so code fills it wherever a contract puts it ; fact renamed between contracts ; files 2 | closed (commit) | - |
| 2289055 | 26.09 | F06 |  | `role_digest`, `handoff_check`, `selftest` | live run 5 | subj: TP1-13797: code helps the role, and never decides for it in silence ; code decides for the role in silence ; files 2 | closed (commit) | - |
| fd9584f | 26.09 | F12 | F16,F05,F02,F06 | `plan_row.py`, `brief_pack`, `contract`, `selftest` | live run 4 (its own numbers) | subj: TP1-13797: the form is edited field by field, the plan row too, and the material travels ; role fights the code (form rewritten with Write, $16.53 for two booleans); material not carried ; files 16 | closed (commit) | - |
| b048984 | 26.09 | F05 | F07 | `selftest` | live run | subj: TP1-13797: an unverifiable plan row owes no design review ; false refusal (unverifiable row owes design review) -> gate loop ; files 2 | closed (commit) | sib: "`skip` and `manual-human` were already exempt from the independent-review requirement for exactly this reason (FB-7, run 1); `unverifiable` ... was not" |
| 3416cc7 | 26.09 | F12 | F06 | `handoff_check`, `selftest` | live run | subj: TP1-13797: a word outside a closed list is the role's repair, not a question ; refusal without marker travels to conductor and person (closed-list word) ; files 3 | closed (commit) | - |
| 06e669b | 26.09 | F06 | F02,F07 | — | live run | subj: TP1-13797: the gap question reads an attachment's own fields ; text to a person (attachment: ? - no cause recorded) ; files 1 | closed (commit) | - |
| 5782744 | 26.09 | F06 | F02 | `selftest` | live run | subj: TP1-13797: the ladder runs on any complaint about material, not only a declared gap ; ladder did nothing on a complaint without a source id ; files 2 | closed (commit) | yes: "so the collection ladder, which parsed ids out of the refusal, did nothing" |
| 5bacf2f | 26.09 | F02 | F06 | `source_inventory`, `selftest` | live run 4 (watching S1) | subj: TP1-13797: an escaped URL is still an MR, an attachment owes a cause, a skip is not a failure ; escaped URL not an MR; unavailable without cause; skip recorded as unavailable ; files 5 | closed (commit) | sib: "Three more of the same family" |
| 1090eea | 26.09 | F02 | F06,F01 | `vcs_evidence.py`, `contract`, `selftest` | live run 4 | subj: TP1-13797: every route before the person, a cause for every gap, no filler question ; unavailable with any prose; ladder never tried; filler question ; files 6 | closed (commit) | - |

## 2. Table B - per feature

Items = A1-A6 rows + the `defect_found` row (journal `rejected` rows and commits are counted in their own columns, not as items). open = not closed per the source status. found live = `live run` + `rehearsal`. ideas = rows tagged "idea (not a defect)" (subtract for defects only). ff = fix-of-fix columns (yes / sib / rec / self, see conventions). top files = by number of items naming the file (module name without `.py`). also = number of rows that list the feature in `also`.

| F | feature | items | ideas | open | found live | ff yes | ff sib | ff rec | ff self | top 3 files by mentions | distinct class words (count) | commits (primary) | journal rejected | also |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F01 | ticket read S0 | 6 | 0 | 6 | 1 | 0 | 3 | 0 | 0 | `story_run` x1, `cmp2.md` x1, `ticket.json` x1 | second copy / twin (3); silent loss (2); unknown as fact (1); wrong measurement / cost (1); missing check / no guard / unguarded (1); project-specific (1) | 0 | 0 | 12 |
| F02 | sources S1 | 19 | 1 | 17 | 7 | 0 | 4 | 0 | 0 | `source_inventory` x5, `story_run` x2, `ticket_adapter` x2 | repeat spend / slow (5); role fights the code (2); false pass / false ok / gate lets through (2); unknown as fact (2); text to a person (2); unchecked claim / claim without proof (1) | 2 | 0 | 4 |
| F03 | stand access and identity | 15 | 1 | 13 | 5 | 0 | 3 | 0 | 0 | `probe_by_code` x4, `runtime_probe` x3, `red_sandbox` x2 | unknown as fact (4); field without producer / contract not told (2); no way out / no zero outcome / no executor (2); false pass / false ok / gate lets through (1); wrong measurement / cost (1); race / timing / buffering (1) | 1 | 3 | 21 |
| F04 | onboarding and reinstall | 12 | 4 | 11 | 5 | 0 | 0 | 0 | 0 | `runtime_paths` x2, `onboard_apply` x2, `readiness` x1 | second copy / twin (4); race / timing / buffering (2); stale state / not portable (1); missing check / no guard / unguarded (1); role fights the code (1); refusal without door (1) | 1 | 0 | 12 |
| F05 | controller and dispatch packets | 14 | 0 | 13 | 7 | 0 | 1 | 0 | 0 | `controller` x3, `pipeline.json` x1, `comments.md` x1 | repeat spend / slow (4); silent loss (3); stale state / not portable (3); absolute path (2); refusal without door (1); wrong measurement / cost (1) | 6 | 0 | 17 |
| F06 | driver headless | 29 | 0 | 23 | 12 | 5 | 6 | 2 | 0 | `story_run` x14, `ticket_adapter` x2, `story_step` x2 | silent loss (8); refusal without door (5); second copy / twin (5); text to a person (4); race / timing / buffering (4); no way out / no zero outcome / no executor (3) | 10 | 3 | 38 |
| F07 | questions to a person, gates A/B | 21 | 2 | 20 | 11 | 0 | 2 | 0 | 0 | `gate_preflight` x6, `human-questions.md` x2, `waiver` x2 | text to a person (9); no way out / no zero outcome / no executor (4); silent loss (3); repeat spend / slow (1); role fights the code (1); unknown as fact (1) | 5 | 0 | 22 |
| F08 | coverage and traceability | 22 | 0 | 19 | 10 | 0 | 2 | 0 | 0 | `s5_precheck` x6, `check_delivery` x3, `manifest_from_tests` x3 | false pass / false ok / gate lets through (5); text to a person (4); project-specific (3); silent loss (2); missing check / no guard / unguarded (2); role fights the code (2) | 6 | 0 | 19 |
| F09 | oracle provenance P20 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | `s5-notes.md` x1, `ticket-snapshot.json` x1, `TP1-13797_TC_002.md` x1 | unchecked claim / claim without proof (1) | 0 | 0 | 1 |
| F10 | manual evidence | 7 | 0 | 5 | 5 | 0 | 0 | 0 | 0 | `manual_capture` x3, `references/manual-capture-steps.json` x1, `controller` x1 | false pass / false ok / gate lets through (3); race / timing / buffering (3); refusal without door (2); no way out / no zero outcome / no executor (1); second copy / twin (1) | 0 | 0 | 2 |
| F11 | execution | 27 | 2 | 23 | 10 | 2 | 4 | 0 | 0 | `run_suite` x4, `window_record` x4, `execution_request` x3 | false pass / false ok / gate lets through (8); repeat spend / slow (5); project-specific (4); silent loss (3); stale state / not portable (2); text to a person (2) | 2 | 2 | 22 |
| F12 | S7 triage and handoff forms | 16 | 0 | 15 | 7 | 1 | 2 | 0 | 0 | `handoff_check` x4, `project_decisions` x2, `triage.json` x1 | role fights the code (3); no way out / no zero outcome / no executor (3); refusal without door (3); repeat spend / slow (2); unchecked claim / claim without proof (2); second copy / twin (2) | 4 | 0 | 20 |
| F13 | report and delivery | 12 | 1 | 11 | 3 | 0 | 0 | 1 | 0 | `test-report.md` x3, `references/templates/test-report.md` x2, `qa-doc-scribe.md` x1 | no way out / no zero outcome / no executor (3); text to a person (2); stale state / not portable (2); false pass / false ok / gate lets through (1); project-specific (1); second copy / twin (1) | 1 | 0 | 17 |
| F14 | cost, telemetry, dashboard | 29 | 6 | 23 | 4 | 0 | 1 | 0 | 1 | `cost_capture` x6, `retro_numbers` x5, `factory_dashboard` x3 | wrong measurement / cost (13); second copy / twin (2); silent loss (2); project-specific (1); repeat spend / slow (1); unknown as fact (1) | 5 | 3 | 14 |
| F15 | package hygiene and self-checks | 10 | 2 | 9 | 0 | 1 | 1 | 0 | 0 | `selftest` x2, `design/factory-map.md` x1, `plans/builder-rules.md` x1 | repeat spend / slow (4); project-specific (1); absolute path (1); unchecked claim / claim without proof (1); stale state / not portable (1) | 7 | 0 | 8 |
| F16 | hooks and guard | 11 | 1 | 9 | 3 | 1 | 2 | 0 | 0 | `guard_pre_tool` x5, `artifact-writers.json` x1, `contract_slices` x1 | refusal without door (3); second copy / twin (3); missing check / no guard / unguarded (1); silent loss (1); absolute path (1); code decides for role/person (1) | 2 | 0 | 13 |
| F17 | role texts and controller blocks | 13 | 1 | 13 | 4 | 0 | 1 | 0 | 0 | `common-rules.md` x1, `runtime_paths` x1, `red_sandbox` x1 | repeat spend / slow (2); second copy / twin (2); refusal without door (2); absolute path (1); missing check / no guard / unguarded (1); role fights the code (1) | 3 | 0 | 21 |
| F18 | Jira agents / write side | 7 | 2 | 6 | 3 | 0 | 0 | 0 | 0 | `external_writes` x2, `ai-teammate.yml` x1, `story_run` x1 | missing check / no guard / unguarded (2); environment (2); text to a person (1) | 0 | 0 | 1 |
| F19 | dev system and experiment tooling (ADDED) | 35 | 7 | 26 | 4 | 1 | 1 | 0 | 0 | `RELEASE.md` x1, `CLAUDE.md` x1, `PROJECT.md` x1 | repeat spend / slow (8); wrong measurement / cost (6); unknown as fact (4); missing check / no guard / unguarded (3); false pass / false ok / gate lets through (2); second copy / twin (2) | 1 | 1 | 9 |
| F20 | jev / judge layer (ADDED) | 2 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | `judge_diff` x1 | — | 0 | 0 | 0 |
| | **total** | 308 | 32 | 265 | 102 | 11 | 33 | 3 | 1 | | | 56 | 12 | 273 |

Primary -> also pairs (extra data; rows of A1-A6, journal and commits excluded from the commit side), top 20:

| primary | also | rows |
|---|---|---|
| F06 | F07 | 7 |
| F03 | F11 | 6 |
| F07 | F06 | 6 |
| F08 | F13 | 6 |
| F06 | F12 | 6 |
| F11 | F06 | 6 |
| F19 | F14 | 6 |
| F08 | F11 | 5 |
| F04 | F16 | 5 |
| F02 | F01 | 5 |
| F06 | F03 | 4 |
| F06 | F05 | 4 |
| F16 | F12 | 4 |
| F13 | F06 | 4 |
| F11 | F03 | 4 |
| F07 | F03 | 4 |
| F13 | F08 | 4 |
| F03 | F07 | 4 |
| F14 | F19 | 3 |
| F12 | F06 | 3 |

Fix-of-fix rows by marker (ids; feature in brackets):

- **yes** (15): B-161(F12), B-164(F06), B-165(F06), B-167(F06), B-174(F06), B-176(F16), B-180(F11), B-217(F11), B-222(F06), F-cmp2-6(F15), F-2(F19), t-023(F03), t-023(F03), t-023(F03), 5782744(F06)
- **sib** (37): B-142(F17), B-153(F03), B-154(F12), B-214(F15), B-215(F19), B-166(F16), B-169(F11), B-171(F06), B-199(F14), B-218(F12), B-246(F02), B-251(F05), B-249(F16), B-247а(F02), B-247б(F06), B-247в(F02), B-247г(F02), B-255а(F03), B-255б(F11), B-255в(F08), B-255г(F06), B-255д(F03), B-255е(F07), B-255ж(F06), B-256а(F01), B-256б(F01), B-256в(F01), B-256г(F06), F-cmp2-20(F07), F-cmp2-21(F11), F-cmp2-23(F06), F-cmp2-28(F11), run5-14(F08), 22c8663(F07), 99dd8e5(F05), b048984(F05), 5bacf2f(F02)
- **rec** (5): B-182(F13), rehearsal-12(F06), run5-21(F06), 5a66517(F15), 177af88(F15)
- **self** (5): run5-24(F14), dada152(F08), 1556e9b(F07), db39837(F14), 4351f4e(F06)

## 3. Table C - files touched by >= 3 package commits since 26.09

Command (as dispatched but with `--since="2026-09-26 00:00"` (see section 0) and without `head`; the counting is done in Python over the same `git log --name-only` output): `git -C D:/ws1/yml-text-factory log --since="2026-09-26 00:00" --name-only --format= -- ai-packages/qa-factory | sort | uniq -c | sort -rn` -> 516 distinct files, 66 with count >= 3 (the dispatch's `head -40` is the first 40 rows below). The integration commit `4116add` (369 files) counts once for every file it touches; the column "ex-4116add" is the same count without it (computed from `git log --name-only` per commit). Feature = by the file (tests by the module they test; docs by what they document).

| file (under `ai-packages/qa-factory/`) | commits | ex-4116add | F |
|---|---|---|---|
| `scripts/story_run.py` | 21 | 20 | F06 |
| `CHANGELOG.md` | 19 | 18 | F15 |
| `design/factory-rules-debt.md` | 18 | 17 | F15 |
| `scripts/tests/test_story_run.py` | 13 | 13 | F06 |
| `scripts/brief_pack.py` | 7 | 6 | F05 |
| `scripts/guard_pre_tool.py` | 7 | 6 | F16 |
| `design/factory-rules.md` | 6 | 5 | F15 |
| `scripts/controller.py` | 6 | 5 | F05 |
| `scripts/handoff_check.py` | 6 | 5 | F12 |
| `scripts/selftest.py` | 6 | 6 | F15 |
| `design/README.md` | 5 | 4 | F15 |
| `scripts/audit_factory.py` | 5 | 4 | F15 |
| `scripts/contract.py` | 5 | 4 | F08 |
| `scripts/gate_brief.py` | 5 | 4 | F07 |
| `agents/qa-code-critic.md` | 4 | 3 | F17 |
| `design/controller-blocks.md` | 4 | 3 | F17 |
| `design/state-exits.md` | 4 | 3 | F15 |
| `references/ahead-cards.json` | 4 | 3 | F17 |
| `references/artifact-writers.json` | 4 | 3 | F16 |
| `references/conductor.md` | 4 | 3 | F17 |
| `references/human-questions.md` | 4 | 4 | F07 |
| `references/role-commands.json` | 4 | 3 | F17 |
| `scripts/critic_rollcall.py` | 4 | 3 | F07 |
| `scripts/manifest_from_tests.py` | 4 | 3 | F08 |
| `scripts/run_suite.py` | 4 | 3 | F11 |
| `scripts/s5_precheck.py` | 4 | 3 | F08 |
| `scripts/source_inventory.py` | 4 | 3 | F02 |
| `scripts/story_step.py` | 4 | 3 | F12 |
| `scripts/tests/test_brief_pack.py` | 4 | 3 | F05 |
| `scripts/tests/test_gate_brief_and_retro.py` | 4 | 3 | F07 |
| `scripts/tests/test_human_questions.py` | 4 | 4 | F07 |
| `scripts/tests/test_manifest_from_tests.py` | 4 | 3 | F08 |
| `scripts/window_record.py` | 4 | 3 | F11 |
| `agents/qa-case-critic.md` | 3 | 3 | F17 |
| `agents/qa-doc-scribe.md` | 3 | 2 | F17 |
| `agents/qa-runner.md` | 3 | 2 | F17 |
| `design/driver.md` | 3 | 2 | F06 |
| `design/metric-signal-policy.md` | 3 | 2 | F14 |
| `references/artifact-contract-automation.md` | 3 | 2 | F17 |
| `references/slices/qa-automator/artifact-contract-automation.md` | 3 | 2 | F17 |
| `references/slices/qa-automator/index.md` | 3 | 2 | F17 |
| `scripts/check_delivery.py` | 3 | 2 | F08 |
| `scripts/execution_request.py` | 3 | 2 | F11 |
| `scripts/external_writes.py` | 3 | 2 | F18 |
| `scripts/factory_dashboard.py` | 3 | 2 | F14 |
| `scripts/gate_preflight.py` | 3 | 2 | F07 |
| `scripts/manifest_put.py` | 3 | 2 | F08 |
| `scripts/metric_signals.py` | 3 | 2 | F14 |
| `scripts/plan_row.py` | 3 | 3 | F12 |
| `scripts/probe_by_code.py` | 3 | 2 | F03 |
| `scripts/refusal_registry.py` | 3 | 2 | F16 |
| `scripts/retro_numbers.py` | 3 | 2 | F14 |
| `scripts/tests/test_ahead_cards.py` | 3 | 2 | F17 |
| `scripts/tests/test_audit_rules.py` | 3 | 2 | F15 |
| `scripts/tests/test_delivery_ownership.py` | 3 | 2 | F13 |
| `scripts/tests/test_guard_write_owners.py` | 3 | 2 | F16 |
| `scripts/tests/test_handoff.py` | 3 | 2 | F12 |
| `scripts/tests/test_infra_failure.py` | 3 | 2 | F06 |
| `scripts/tests/test_metric_signals.py` | 3 | 2 | F14 |
| `scripts/tests/test_package_generation.py` | 3 | 2 | F06 |
| `scripts/tests/test_role_commands.py` | 3 | 2 | n/c |
| `scripts/tests/test_run_suite_mine.py` | 3 | 2 | F11 |
| `scripts/tests/test_s5_precheck.py` | 3 | 2 | F08 |
| `scripts/tests/test_source_inventory.py` | 3 | 2 | F02 |
| `scripts/tests/test_window_record.py` | 3 | 2 | F11 |
| `scripts/ticket_adapter.py` | 3 | 2 | F01 |

Sum of commit counts of the files above, by feature: F15=66, F06=43, F17=41, F08=26, F07=24, F05=17, F16=17, F11=17, F12=16, F14=15, F02=7, F18=3, F03=3, F13=3, n/c=3, F01=3.

## 4. Table D - the journal (`logs/routing-log.jsonl`)

### D1. every `rejected` and every `defect_found` (reason = first 200 characters of the event's notes, verbatim)

| task_id | ts | event | attempt | failure_class / ref | reason |
|---|---|---|---|---|---|
| t-021 | 2026-09-29T18:15:44 | rejected | 1 | capability | critic:t-028 F1: the builder's own s0_block deviation goes stale and captures a later non-door S0 stop (answer misrouted, stale false question); F2 pooled tests share a process-wide stdout redirect (F |
| t-023 | 2026-09-29T18:15:44 | rejected | 1 | spec | critic:t-030 blockers F1/F2 trace to the spec (edge rows 6/7 treated bytes only as a tie-break) - a dispatcher spec defect, not the builder's; spec amended by Lead; returned to the same builder for at |
| t-023 | 2026-09-29T19:48:06 | rejected | 2 | spec | critic:t-035 blocker F3 traces to the Lead's MEASURED BYTES amendment (one meaning assumed for test_content_sha) plus F4/F5; second rejection on the same tier -> escalation mandatory (rule 6) |
| t-033 | 2026-09-29T20:27:40 | rejected | 1 | capability | critic:t-037 F1 violates the invariant written in spec t-017 D2 item 5 (environment_job questions never take the stand branch); F2 witness not reproducible under the default locale; F3 docs contradict |
| t-023 | 2026-09-29T23:30:38 | rejected | 3 | spec | critic:t-048 blocker F1 traces to the Lead's Amendment 3 ('same predicate as classify'), which made the line heuristic load-bearing; the builder implemented the spec. First rejection on the Opus tier  |
| t-045 | 2026-09-29T23:46:08 | rejected | 1 | capability | critic:t-049 B2 (a result is passed/failed per spec section 0, skips counted) and B3 (a second identity against the one-predicate rule) are deviations from the spec text; B1 (which of several results) |
| t-083 | 2026-09-30T11:35:18 | rejected | 1 | spec | returned by the builder before work: the dispatch had no given/owns fields, no --out on the dashboard, driver-runs.jsonl lives per task under artifacts/<T>/state, and the dashboard writes into the roo |
| t-090 | 2026-09-30T13:57:45 | rejected | 1 | spec | critic-on-plan (agent a29eaef2df3befd5f) REJECT: measured on 41 real builder prompts the rule blocks 41 of 41 (relative owns 29, command without backticks 16, no edges line), 36 even with absolute own |
| t-149 | 2026-09-30T19:55:24 | rejected | 1 | capability | critic verdict on the rest of B-194 (worker af87288bdb4b4e2a6, 19:52): BLOCKER. This task's blocker: F3b - the builder's own 'retired parameter' rule (chosen for cmp1's renamed parameter ids, outside  |
| t-143 | 2026-09-30T19:55:24 | defect_found | - | ref t-143 | critic pass (19:52) on the accepted piece F together with E: after a person's word (waiver --block changed-after-red) the finding is gone but the brief still says '1 to judge', the window still gaps ' |
| t-166 | 2026-09-30T20:11:15 | rejected | 1 | spec | critic verdict on Q3 (worker a447adde416b1cced, 20:10): fit with fixes, two MUST. Empirics reproduce the builder's cmp1 figures exactly, the partition holds, the recaptured copy gives agrees low = hig |
| t-165 | 2026-09-30T20:23:00 | rejected | 1 | spec | critic verdict on Q2 (worker a20b152a18fa00029, 20:20): BLOCKER. Tail detection is right (the 16 flagged, 17.4240782 = B, idempotent, the plan-review fixture holds), but two new stale reasons (gone fi |
| t-214 | 2026-10-01T07:48:25 | rejected | 1 | spec | Rejected on the critic's C1-C3: the binding override C11 (pin then revise_plan) was in the spec and not built (builder miss), C2/C3 are edges the spec named only by invariant (re-render after a round; |

### D2. every `accepted` / `delegated` whose notes contain (substring, case-insensitive) `again`, `re-applied`, `wiped`, `regress`, `leftover`, `second time`, `the same`, `twin` or `sibling`: 152 notes in 117 task ids at generation time 2026-10-02 11:26 (the journal keeps growing from other sessions); 123 of them match as whole words (so `against`, `agains` are the other 29); phrase = first whole-word match (else first substring match) with 60 characters of context each side

Counts by word over these notes (a note can hold several): again=52, the same=44, sibling=42, twin=23, leftover=7, regress=2, second time=1, wiped=1. The words `the same`, `again`, `sibling` are mostly routine ("same builder", "sibling sweep"); `regress`, `wiped`, `leftover`, `second time` are the rare ones.

| task_id | event | ts | words | whole word | phrase |
|---|---|---|---|---|---|
| t-005 | accepted | 2026-09-29T15:45:59 | again/sibling | yes | ...verdict ACCEPT WITH FIXES: F1 blocking (SIBLING_MAP axis 4 lacks the generated index) - fixed by Lead in docs/S... |
| t-006 | accepted | 2026-09-29T15:48:52 | the same | yes | ...d; keys fixed in the dispatch before the run; Lead rerun of the same script: RESULT 0 FAIL, exit=0; critic: skipped, doc-only ni... |
| t-007 | accepted | 2026-09-29T16:06:33 | the same | yes | ...' confirmed by Grep -i '5-5/fable-5-1' (positive control in the same call: fable-5-1 found at :175); positive 'old worktree path... |
| t-009 | accepted | 2026-09-29T16:06:33 | the same | yes | ...ONTWRITEBYTECODE' (control: PYTHONDONTWRITEBYTECODE hits in the same call, no PYTHONUTF8)... |
| t-013 | delegated | 2026-09-29T16:06:33 | sibling | yes | ...est_usage_activity.py, experiments/measurers/*.py + README, SIBLING_MAP axis 6... |
| t-027 | accepted | 2026-09-29T17:36:14 | the same | yes | ...'-' literal, minor 5) -> sent back to the t-022 builder in the same task; Q1 per-call config stat cost in quadratic loops -> D2... |
| t-030 | delegated | 2026-09-29T17:55:32 | the same | yes | ...gent:PENDING - Lead error: the previous line was written in the same move as the dispatch call, before it returned, with a place... |
| t-022 | accepted | 2026-09-29T17:56:50 | the same | yes | ...leading/trailing '-' rejected, linear-time test) applied by the same builder in this task; Lead answers Q1 (capability in readin... |
| t-021 | delegated | 2026-09-29T18:15:44 | the same | yes | ...attempt 2 after rejected (resumed the same worker by SendMessage at ~18:05): fix F1 clear s0_block/s0_... |
| t-023 | delegated | 2026-09-29T18:15:44 | the same | yes | ...attempt 2 after rejected (resumed the same worker by SendMessage): BYTES RULE, MEASURED BYTES with rea... |
| t-035 | accepted | 2026-09-29T19:48:06 | the same | yes | ...-023 attempt 2: F3 MEASURED BYTES compares two semantics of the same bytes (raw file sha256 in trace_binding vs run fingerprint... |
| t-033 | delegated | 2026-09-29T20:28:55 | the same | yes | ...attempt 2, the same builder resumed with context: amendment R1-R7 of t-017 D2 (... |
| t-039 | accepted | 2026-09-29T20:40:07 | twin | yes | ...uman-questions.md (FR-38). Queued: F3 gate_brief.py (axis-5 twin, 12 ids journaled on a real gate A brief) -> B-009 part 2 s... |
| t-042 | delegated | 2026-09-29T20:53:37 | again | no | ...path in the package (working tree incl. section-0 changes) against the owner's run budget D-0018: author run, critic red pro... |
| t-042 | accepted | 2026-09-29T21:17:30 | again | yes | ...s read directly (S5-qa-automator-2 ...:87cdaab9d40f and ...:again-2; three S6-qa-runner-1 repair_verify jobs). Findings vs D-... |
| t-023 | delegated | 2026-09-29T23:31:38 | the same | yes | ...attempt 4, the same Opus builder resumed: Amendment 5 - tokenize-based executab... |
| t-045 | delegated | 2026-09-29T23:46:08 | again/the same | yes | ...attempt 2, the same builder resumed: B1-B4 + F1-F6 + begin/metrics_projection l... |
| t-045 | accepted | 2026-09-30T01:19:17 | again | yes | ...input: B1 newest result wins, B2 per-row results (the 13797 again-2 replay is now a rerun: its block rows are not_run), B3 on... |
| t-054 | delegated | 2026-09-30T01:20:50 | again | no | ...C changes what counts as a current review/probe): freshness against accepted t-023/t-045 code, invariant per C-item, error di... |
| t-063 | accepted | 2026-09-30T02:26:16 | sibling/the same | yes | ...regenerate (PROJECT.md edited after the build) sent back to the same builder as round 2 (SendMessage to agent:ab04d43eabb0e1432,... |
| t-051 | accepted | 2026-09-30T02:33:28 | sibling | yes | ...in .githooks/pre-commit and the AGENTS.md row + eol rule on SIBLING_MAP axis 4 (enforcement file placed by Lead at acceptance).... |
| t-064 | accepted | 2026-09-30T02:33:28 | the same | yes | ...resets counted, probe 7 cases -> 0). Lead decisions sent to the same builder as round 2 (SendMessage agent:a81f2a2090ffd75b0): D... |
| t-067 | delegated | 2026-09-30T02:40:31 | sibling/the same | yes | ...140/140, story_run 779/779, audit 75/75; M1-M3 killed; two sibling tests red from receipt-less stubs, fix sent back to the sam... |
| t-066 | accepted | 2026-09-30T02:43:28 | sibling/the same | yes | ...ead decision: close them in function_sha itself (round 2 to the same builder via SendMessage agent:a4c0f6265fd762fe6: line split... |
| t-067 | accepted | 2026-09-30T02:57:18 | the same | yes | ...t == --plugin-dir literal, 8.3 names normalize). Round 2 to the same builder (SendMessage agent:a232efb1e5d630042): closed token... |
| t-072 | delegated | 2026-09-30T03:28:27 | the same | yes | ...3 (Lead decision: an id linked to its openable case file on the same line counts as explained, as data in human-text.json). Para... |
| t-075 | accepted | 2026-09-30T05:01:47 | the same | yes | ...ectional (why dropped from the review identity). Round 2 to the same builder (SendMessage agent:a380b1fddc72710f2) with Lead dec... |
| t-074 | accepted | 2026-09-30T05:01:47 | again | yes | ...ering). run_suite.py:1978 hint is true (no budget file -> --again repeats).... |
| t-081 | delegated | 2026-09-30T11:13:46 | the same | yes | ...of existing project material, would a strong engineer write the same, optimality, fit to the ACs, correctness risks; report to s... |
| t-081 | accepted | 2026-09-30T11:28:46 | twin | yes | ...Factory improvement: the designer names per Then the broken twin it kills -> backlog B-185.... |
| t-082 | accepted | 2026-09-30T11:35:18 | sibling/the same | yes | ...irmed by Lead. Dispatch defect noted: no given/owns fields (the same builder returned t-083 for it). critic: skipped, experiment... |
| t-085 | delegated | 2026-09-30T12:15:44 | again/the same | yes | ...nd come back as not_evaluated, then _hot_cache_signals adds the same id again; measured on the cmp1 receipt: 28 signals, 7 ids t... |
| t-086 | delegated | 2026-09-30T12:26:19 | again | no | ...d whole in both, <= on the cold list, new current_raw field against rounding re-activating an acknowledged signal. B-194 veri... |
| t-090 | delegated | 2026-09-30T13:49:12 | again | no | ...s F1b F2a F3a F4a F5-queued F6-code decided by Lead): facts against the code, the rule measured on four real dispatch prompts... |
| t-092 | delegated | 2026-09-30T13:57:45 | the same | yes | ...-090 and corrected before any commit: the validator forbids the same critic re-entering that id): the same critic resumed by mes... |
| t-093 | delegated | 2026-09-30T14:13:23 | again | no | ...st variants of the form, the complete-read invariant, texts against the spec, the builder's eight unfixed decisions. Builder'... |
| t-101 | delegated | 2026-09-30T14:13:23 | twin | yes | ...B-201 piece B: wiring through .next twins of dispatch_gate.py and its tests, two literals in warn_lay... |
| t-093 | accepted | 2026-09-30T14:27:26 | the same | yes | ...ued to the backlog: the gate and the owns registry can read the same prompt differently.... |
| t-103 | accepted | 2026-09-30T14:34:25 | again | yes | ...erted the trial edit of .claude/settings.json; commits pass again.... |
| t-101 | delegated | 2026-09-30T14:38:59 | twin | yes | ...try on the finished piece B (dispatch_gate.py.next and test twins; builder's witness on the scratch tree: 620 passed in 45.61... |
| t-106 | delegated | 2026-09-30T15:07:25 | twin | yes | ...) in main(), UNCHECKED note for malformed JSON and timeout, twins for hook_liveness_probe.py, mechanism_gate.py, warn_layers.... |
| t-106 | accepted | 2026-09-30T15:29:10 | again | no | ...TS.md regenerated. D-0022 was appended with a shell printf, against command hygiene point 4 - content is as shown in the comm... |
| t-107 | delegated | 2026-09-30T15:31:45 | sibling | yes | ...importers, stale instructions to run the old file, FR pass, siblings. Builder t-107 reported: old file moved with an equal sha25... |
| t-108 | delegated | 2026-09-30T16:10:42 | again | no | ...passes silently; facts with a trail, a measurement command against the cmp1 copy, named edges, finished pieces with one witn... |
| t-112 | accepted | 2026-09-30T16:26:40 | the same | yes | ...3 files (context_bundle.py and two tests), a reader only - the same search is its own positive control. Cause written into plan... |
| t-108 | accepted | 2026-09-30T16:30:20 | twin | yes | ...; backlog rows B-217 (data-module blind spot) and B-218 (S7 twin and unverified claims) added.... |
| t-119 | delegated | 2026-09-30T16:43:25 | again | no | ...the launch classifier's error direction, the precedent skip against D-0018, the partition-binding meaning change, claims fill... |
| t-123 | delegated | 2026-09-30T17:00:04 | again | no | ...Deviation recorded: P1 (t-124) and P3 (t-125) were started against P0 on the rerun witness, before this critic's verdict - t... |
| t-123 | accepted | 2026-09-30T17:05:59 | the same | yes | ...out $5.1). They go to a follow-up builder dispatch t-130 on the same two files.... |
| t-126 | delegated | 2026-09-30T17:21:06 | again | no | ...alse-alarm on other runners - given to the critic to settle against P2.... |
| t-133 | delegated | 2026-09-30T17:23:00 | the same | yes | ...five mutations killed, cmp1 copy gives one record BUG-1) - the same critic dispatch as t-125's entry, separate verdict.... |
| t-126 | accepted | 2026-09-30T17:34:29 | again | no | ...it_factory.py stays Lead's line (factory-fixes decision 4), against the critic's reading of the spec.... |
| t-116 | delegated | 2026-09-30T17:45:39 | the same | yes | ...critic entry on B-194 piece A - the same critic dispatch as t-117's entry (one verdict for both piec... |
| t-140 | delegated | 2026-09-30T17:45:39 | again | no | ...not regenerated by the builder (Lead at integration). Built against piece B's shapes while its critic runs (owner's rule: the... |
| t-143 | delegated | 2026-09-30T17:45:39 | again | yes | ...st; a case made automatable goes through the pyramid ladder again; onboarding may run a collect.... |
| t-137 | accepted | 2026-09-30T18:01:21 | again | no | ...: cost files re-priced at the catalogue rate sum to 16.6491 against the driver's 17.4241; 16 of 35 sessions differ, the cost... |
| t-146 | delegated | 2026-09-30T18:01:21 | again | no | ...of the new rate order on old stories, the chat attribution against the owner's words, the status logic, and whether Q1 and Q... |
| t-132 | delegated | 2026-09-30T18:10:19 | again | no | ...lled, I3 shown on 27 hand-built and 1500 random inventories against the frozen old function; on a temp copy of cmp1 the new r... |
| t-116 | accepted | 2026-09-30T18:39:50 | sibling | yes | ...ts reparse rows with instance_content_sha - queued with the sibling readers.... |
| t-117 | accepted | 2026-09-30T18:39:50 | sibling/the same | yes | ...ct after an author rewrite, module home, verdict patch key, sibling readers, long path. Fixes F1-F6 and F8 go to t-149; F7 (acc... |
| t-135 | accepted | 2026-09-30T18:39:50 | again | no | ...ivated, doors by audience, two markers, onboarding text run against project_decisions). critic: the topic pass over B-193 run... |
| t-154 | delegated | 2026-09-30T18:56:41 | again | yes | ...(a) removes the shadowing keys so the question is not asked again (FR-7), no separate remove-the-table answer, rows show both... |
| t-143 | accepted | 2026-09-30T19:02:11 | sibling | yes | ...names a waiver the controller never reads for window gaps (sibling, all window gaps). Needed at integration: vocabulary word g... |
| t-142 | accepted | 2026-09-30T19:06:08 | again | no | ...with piece F's note: such a pair still gaps at the window - against the person's word passing a gate).... |
| t-145 | delegated | 2026-09-30T19:10:57 | again | no | ...Lead 19:09, equality table of 294 legacy rows x 9 manifests against the old function): error direction hunt, replay of cmp1 a... |
| t-151 | accepted | 2026-09-30T19:10:57 | sibling | yes | ...stands); the edge meant 'no readable name closes nothing'. Sibling for piece P5: gate_brief.py:226 runs after S1 is completed... |
| t-127 | accepted | 2026-09-30T19:10:57 | regress/sibling | yes | ...ls is 'ran, nothing to report' and must stay a precedent (a regression for reporter-less profiles - Lead's spec edge K6 was wrong... |
| t-153 | delegated | 2026-09-30T19:20:44 | again/sibling | yes | ...rity; then the builder's seven decisions and three reported siblings. Q2 (same file) and Q3 (imports revalue_document) wait for... |
| t-154 | accepted | 2026-09-30T19:22:30 | again | yes | ...(a) cleans the shadowing keys so the question is not asked again). critic: the config migration is schema-class - its pass i... |
| t-150 | accepted | 2026-09-30T19:28:10 | the same | yes | ...got a new mtime (19:07:34) - the known B-197 path rewrites the same bytes; content equality not proven for this run (the file i... |
| t-144 | accepted | 2026-09-30T19:39:29 | sibling | yes | ...(readers fall back to HEAD now; FR-40 row at integration). Siblings queued: gate_preflight check_vcs strips the leading space o... |
| t-156 | accepted | 2026-09-30T19:41:49 | sibling | yes | ...stion IS flagged (E-19 - the builder read O3 too narrowly). Sibling for A2: gate_brief _patch_for/_then_effect should import pl... |
| t-155 | accepted | 2026-09-30T19:46:34 | the same | yes | ...xts that name a question id give named too, never answered (the same rule as the gate's words) - queued for the wiring follow-up... |
| t-167 | delegated | 2026-09-30T19:55:24 | sibling | yes | ...itch to run_history before the B-194 commit, and a proposed SIBLING_MAP axis row.... |
| t-167 | accepted | 2026-09-30T19:58:16 | sibling | yes | ...ime, a corrupt block still raises); display readers queued; SIBLING_MAP axis 8 row as proposed, written by Lead at integration. Ana... |
| t-168 | delegated | 2026-09-30T20:00:28 | again | no | ...s and conftests up to the project root (V4), unchanged only against a recorded S0 base (V2), untracked-at-S0 never unchanged.... |
| t-165 | delegated | 2026-09-30T20:08:51 | sibling | yes | ...ure, the two control values), the builder's four decisions, siblings, and what measurement M6 of the main() lock must be.... |
| t-170 | accepted | 2026-09-30T20:54:09 | sibling | yes | ...3/t-164/t-166/t-169 (B-202), money diff. Red neighbours and siblings the builder listed go to the follow-up (carrier: factory-fi... |
| t-149 | delegated | 2026-09-30T21:01:20 | sibling | yes | ...invariant across every reader of the pair, F-cj, the three siblings; also covering critic:t-140 critic:t-158 for acceptance (te... |
| t-140 | accepted | 2026-09-30T21:24:20 | the same | yes | ...ic:t-149, its second critic entry named critic:t-140): fit. The same verdict: t-149 att. 2 fit with fixes (blank-note patch stri... |
| t-175 | delegated | 2026-09-30T21:31:18 | the same | yes | ...son on rows, V10 no unmeasured line, V7 delivery_summary on the same map. Parallel with t-174 and t-176 on disjoint files.... |
| t-169 | accepted | 2026-09-30T21:40:49 | sibling | yes | ...ession, money under the role; agent_label on the Cost tab). Siblings queued: raw WHY words in task_price's finding; Q9 formula v... |
| t-165 | accepted | 2026-09-30T21:44:36 | sibling | yes | ...ure drops a gone subagent's rows (recover_codex_usage.py:71 sibling); the lock held 17.8-99 s for a 1.2 s write; a marker with... |
| t-175 | accepted | 2026-09-30T21:48:05 | the same | yes | ...n every ledger row, delivery_summary counts by reason under the same level id (V7), no unmeasured line (V10); plus the reader fi... |
| t-181 | delegated | 2026-09-30T21:48:05 | the same | yes | ...stion_register.record with where S2_stop/S3_stop, resume in the same session with its own text, rework fallback with the words v... |
| t-179 | accepted | 2026-09-30T21:59:25 | sibling | yes | ...5 reword (the code names no authoritative record, per P18), SIBLING_MAP axis 'readers of money on one rate base', Q9 formula-versio... |
| t-181 | accepted | 2026-09-30T22:20:58 | again/the same | yes | ...on_register.record(where='S2 stop', by='person'), resume in the same session with its own text, rework of the same dispatch with... |
| t-189 | delegated | 2026-09-30T22:34:25 | again | no | ...te-A suffix through question_register (R-216a.1). P7 builds against it next.... |
| t-188 | accepted | 2026-09-30T22:57:44 | again/twin | yes | ...'Why some reasons are listed as the factory's' with the run-again door. Builder's fork (edge ii): a case with ZERO current ro... |
| t-191 | delegated | 2026-09-30T23:15:52 | again | no | ...py: the one facts builder, the deterministic block renderer against P8's contract, --write (conversion of an unmarked report... |
| t-189 | accepted | 2026-09-30T23:17:14 | twin | yes | ...ite); test_ahead_cards red until P10. Analogs: no validator twin for the gate A block quoting authorization_source; project-... |
| t-192 | accepted | 2026-10-01T00:16:53 | twin | yes | ...s on cmp2), orchestrator-path scout 'Left out' line (axis 5 twin), gate A wording for ref words, unguarded record Write (axi... |
| t-191 | accepted | 2026-10-01T00:24:03 | sibling | yes | ...ct-writers (report_facts/stage_done, state/report-history), SIBLING_MAP report blocks. critic: the report topic pass after P9/P10.... |
| t-197 | accepted | 2026-10-01T00:47:46 | the same | yes | ...order (before t-195's acceptance) and moved to the tail in the same turn, before any commit.... |
| t-199 | delegated | 2026-10-01T00:49:26 | again | yes | ...and say today's truth (not switched by itself yet; decided again from an automated test after the answer; the report says wh... |
| t-199 | accepted | 2026-10-01T00:54:24 | again | yes | ...(the factory does not switch the row by itself yet; decided again from an automated test after the answer; the report says wh... |
| t-201 | delegated | 2026-10-01T01:18:07 | second time | yes | ...eck:` refusal move (write once + S9 once, counter in state, second time the conductor, never the person), and the S5 window `finish... |
| t-202 | delegated | 2026-10-01T02:19:24 | sibling | yes | ...rebuild on the role path keeping appended prose, P10 texts, SIBLING_MAP enumeration, the four questions. Read-only on the live cmp2... |
| t-203 | delegated | 2026-10-01T02:43:56 | again/sibling/twin | yes | ...presence against live cmp2 dispatch shapes, the skill-road twin (story_step start -> prepare), SIBLING_MAP enumeration, the... |
| t-203 | accepted | 2026-10-01T03:08:05 | again | no | ...credited by the roll-call; F2 - the R-224.4 packet guarded against the two contradicting sentences; both sent to the t-198 b... |
| t-206 | delegated | 2026-10-01T03:35:16 | the same | yes | ...d. The live run was unblocked by the Lead's answer carrying the same vocabulary (answers/cmp2-s3-shapes.md).... |
| t-210 | delegated | 2026-10-01T04:40:57 | again/the same | yes | ...esumed ONCE with the refusal verbatim, then finish retried; the same refusal again -> the person (never the conductor, never a f... |
| t-211 | delegated | 2026-10-01T05:54:57 | again | yes | ...set -> conductor; forks returned (second reject -> designer again or person; question_branches before the gate). Observed 05:... |
| t-211 | accepted | 2026-10-01T06:09:28 | sibling | yes | ...tradictions corrected by the designer (stage_done DID fire; sibling axis missing from the map). Critic-on-plan dispatched next... |
| t-212 | delegated | 2026-10-01T06:09:28 | twin | yes | ...y stability across rehearsals, F0 b loop check, edges, S8/B twin, mutation-vs-fixture. Verdict form accept / overrides C1..C... |
| t-214 | delegated | 2026-10-01T06:23:10 | sibling/twin | yes | ...driver-state.json, F0 KNOWN_REFUSALS row first, docs rows, SIBLING_MAP axis-5 twin row, new test_story_run_gate_repair.py (M1-M11)... |
| t-215 | delegated | 2026-10-01T07:35:47 | twin | yes | ...4 false positives, critic ledger vs cause=test_defect, S8/B twin, the builder's 8 decisions and listed analogs (fix-now vs q... |
| t-214 | accepted | 2026-10-01T08:13:47 | again/sibling/twin | yes | ...s rows (driver.md, conductor.md row 34, state-exits row 26, SIBLING_MAP axis-5 twin row). critic:t-215 (accept with fixes on attemp... |
| t-218 | delegated | 2026-10-01T10:38:28 | sibling | yes | ...ly when a case or row names them (the owner's 23.09 return, sibling of the env_probe fix); F-cmp2-24 runtime probes per automat... |
| t-219 | accepted | 2026-10-01T10:59:39 | the same | yes | ...ine; duplicate helpers by behaviour; unregistered marks) in the same owned texts.... |
| t-221 | delegated | 2026-10-01T10:59:39 | sibling | yes | ...ntent match / apply_fix / handed door, edges, the env_probe sibling pairs, fixture-vs-mutations, cost.... |
| t-228 | delegated | 2026-10-01T11:38:23 | twin | yes | ...idence, S7 bug drafts, report expected/observed, gate_brief twin), fixture-blind mutations, the three-builder split.... |
| t-233 | delegated | 2026-10-01T12:59:59 | sibling | yes | ...older plugin over newer manifest), the merge-never-removes sibling class.... |
| t-233 | accepted | 2026-10-01T13:17:45 | sibling | yes | ..._with_fixes; blockers G1/C1/C3 and overrides C2-C11, E1-E4, siblings folded into t-232 section 0c with Lead decisions (one APPLY... |
| t-239 | delegated | 2026-10-01T13:56:22 | twin | yes | ...achine_local false positives, nested notes + the written_by twin. Mechanical layer attached (Lead reruns 144/144, 239/239, 1... |
| t-238 | accepted | 2026-10-01T13:56:22 | sibling | yes | ...ver mismatched), plus W5 = t-232 B5 portable argv; the FR-9 sibling (accept-as-blocked has no S5 reader) folded into t-227 sect... |
| t-243 | accepted | 2026-10-01T14:40:19 | sibling | yes | ...ls moved 1) -> exempt only entries with no explicit status; sibling story_step.py:973-976 caller's-pair branch lacks ran-red ma... |
| t-247 | delegated | 2026-10-01T14:46:24 | again | no | ...swer is never a stand block), critic + rubric (ran red read against the change; unverified is not a pass), handoff yaml, arti... |
| t-244 | accepted | 2026-10-01T14:56:52 | again | yes | ...mp2-26/27 shapes trace as intended; overrides O1 (handoff's again/third results saved as the dispatch's saved result — else a... |
| t-249 | accepted | 2026-10-01T15:15:23 | twin | yes | ...report slot, hand-written JSON, doc/validator drift, rung-5 twin, no S6 state-exits row). Designer brief next id.... |
| t-250 | delegated | 2026-10-01T15:15:23 | twin | yes | ...ction at gate B and in the report, drift closed, the rung-5 twin (fork), a rehearsal on one cmp2 case before the run. Spec b... |
| t-251 | delegated | 2026-10-01T15:33:09 | again | no | ...nown-Then manual case), manual-human class, owns collisions against t-241/t-245/t-246/t-247/t-248.... |
| t-246 | accepted | 2026-10-01T16:29:49 | leftover | yes | ...ck text recorded for S3 and S4 by the orchestrator. Unowned leftover: the register shape in artifact-contract-plan.md (section 2... |
| t-256 | delegated | 2026-10-01T17:00:16 | leftover | yes | ...2-exit register re-check), gate_preflight (two card lines + leftover-raise refusal), the S4-exit re-pin site, designer text + co... |
| t-257 | delegated | 2026-10-01T18:00:21 | again | no | ...mestamps and stated costs, numbers list, tools list, verify-against-repo questions, negative-form control, trail. Writes only... |
| t-257 | accepted | 2026-10-01T18:04:24 | again | no | ...1:38:45, 11 ideas A / 15 ideas B, numbers, tools, 13 verify-against-repo questions). Trail: six Read windows covering all 424... |
| t-256 | accepted | 2026-10-01T18:19:04 | leftover | yes | ...re/now card, raise_questions form + S4-exit raise_pending + leftover-raise rehearsal step, remedy from precondition items, md re... |
| t-259 | accepted | 2026-10-01T18:22:39 | again/the same | yes | ...'s 11,107 B is another SRC copy or pretty-printed; both say the same thing.... |
| t-265 | accepted | 2026-10-01T19:14:44 | the same | yes | ...ratch probes, 78 passed rerun. Fixes dispatched as t-266 to the same builder (context intact) plus --force for the owner's appro... |
| t-268 | delegated | 2026-10-01T19:45:20 | sibling | yes | ...lt; F-VERSION line with the live triple 0.7.9/0.7.19/0.7.4; SIBLING_MAP axes; the cheap live-proof command list over a copy. Mechan... |
| t-269 | delegated | 2026-10-01T19:45:20 | sibling | yes | ...viations D1-D3 (must-fix before the fresh run vs can wait); SIBLING_MAP axes. t-261 edits planning_contract/story_run concurrently... |
| t-270 | delegated | 2026-10-01T19:57:17 | sibling | yes | ...nce (P13), keys' determinism, builder split vs t-261/t-263, SIBLING_MAP.... |
| t-270 | accepted | 2026-10-01T20:12:14 | the same | yes | ...ions. All folded into the spec as §0c C1-C16 (Lead's edits, the same task — a continuation); the person's text is the requiremen... |
| t-276 | accepted | 2026-10-01T21:27:45 | again | yes | ...efix_probes/proof_key persisted at S0 (S1 never asks /field again), auth_gate (401/login page/403/404-on-proven-prefix -> re-... |
| t-279 | delegated | 2026-10-01T22:14:04 | leftover | yes | ...` INFO -> factory_fixable flip + 8 test assertions (t-261's leftover); t-250 §0d F2 (c) the honest image-digest identity on a so... |
| t-280 | delegated | 2026-10-01T22:51:26 | sibling | yes | ...erson question — FR-3, the private helper); temporal paths; SIBLING_MAP; the fresh-run proof artefacts. Mechanical layer attached v... |
| t-280 | accepted | 2026-10-01T23:07:03 | twin | yes | ...t_adapter + story_run); F7, F8, F9-SSO, F11 + the extractor twin (extract_ticket_keys → TL.references) → builder t-282 (tick... |
| t-282 | delegated | 2026-10-01T23:10:02 | twin | yes | ...F11 KEY_RE excludes lowercase on both sides, the extractor twin (extract_ticket_keys delegates to TL.references), B-247(c)... |
| t-283 | delegated | 2026-10-01T23:14:50 | leftover | yes | ...Freshness pass (checklist p.5) over the integration leftovers of State 22:55 before ONE batched builder dispatch: A22 flo... |
| t-284 | delegated | 2026-10-01T23:24:34 | leftover/twin | yes | ...small-work batch: the integration leftovers of State 22:55, fresh facts from scout t-283 — A22 trim of... |
| t-282 | accepted | 2026-10-01T23:44:04 | twin | yes | .../auth half (spec t-267 §0d F7/F8/F9-SSO/F11 + the extractor twin). Interpretations accepted: /field and /remotelink are read... |
| t-284 | accepted | 2026-10-01T23:52:21 | twin | yes | ...785 entry + loud-failure guard + regenerate 189/109 + count twins (README:30, debt :63/:65/:72/:76/:220, test_controller_door... |
| t-289 | delegated | 2026-10-02T05:08:48 | the same | yes | ...un.py + test_story_run_s6.py (t-287 edits the S0 section of the same file — Edit-tool, disjoint regions). Third and fourth defec... |
| t-289 | accepted | 2026-10-02T05:29:41 | again | no | ...— B-line. critic: skipped — a two-line contract fix proven against the real controller + the live rerun that follows.... |
| t-287 | accepted | 2026-10-02T05:59:36 | wiped | yes | ...r byte-copy restores of story_run.py during mutation probes wiped t-289's parallel edit twice — the live file now = its copy... |
| t-279 | accepted | 2026-10-02T06:23:09 | leftover | yes | ...Wave 3 of t-218 + planning_contract leftovers: not_applicable:no_changed_file through writer and four gat... |
| t-291 | delegated | 2026-10-02T07:04:08 | again | yes | ...est reds at 07:02 (296/301) — A22 doc-scribe headroom 883 B again (sources grew after t-284), the automator 9,000-byte cap in... |
| t-291 | accepted | 2026-10-02T07:24:38 | sibling | yes | ...on, 6 fixture dirs) — the remedy is the commit, not a rule. Siblings queued: test_report_texts.py:43 CHARTER_MAX_BYTES 9000 (sam... |
| t-296 | delegated | 2026-10-02T10:52:30 | regress | yes | ...per feature; Table C files by commit count; Table D journal regressions. Writes plans/feature-fragility-2026-10-02.md only. The arc... |
| t-292 | accepted | 2026-10-02T10:58:34 | sibling | yes | ...h controls: `^def test_` 43 files, manual_capture absent in SIBLING_MAP (whole file read) and in the cmp2r config (env_file control... |
| t-294 | accepted | 2026-10-02T11:12:50 | again | no | ...Draft accepted by trail (load-bearing facts table checked against carriers; 3 negative claims with controls; the cmp2r cond... |
| t-300 | delegated | 2026-10-02T11:12:50 | again | no | ...the owner's word, image rebuilding). Designer drafts t-300 against B-257 + critic t-295 F1/F2/F3/K-NA. Builder after t-297/t... |

## 5. Items I could not classify cleanly, and why

Nothing was left without a feature; the following needed a decision the sources do not make for me (all listed with the alternative):

- `B-024`: F05 (controller blocks) vs F17 (`design/controller-blocks.md`): row names no file in backticks.
- `B-030`: F16 chosen; no file named; could equally be F12 (handoff forms) or F05 (artifact edits by a role).
- `B-051`: F15 chosen (package `design/factory-map.md`); the same map is also F19 (`docs/SIBLING_MAP.md`).
- `B-011`: F14 chosen (friction in the retro); the first file named, `code_friction.py`, is the experiments copy (F19).
- `B-141, B-143`: F19 by file (`experiments/measurers/*.py`) while the topic is F14 cost measurers / friction.
- `B-184`: F14 chosen (retro takes a cumulative self-report); first backticked file `report_run.py` is F19.
- `B-121`: F05 chosen (digest of a returned role from its transcript); the files the row names (`cost_capture.py:1260`, `host_dispatch.py:29`) are cited as the correct examples, not as the defective code.
- `B-128`: F14 chosen (size by ticket type); also F07 (the person was asked to reclassify).
- `B-149`: F17 (first file named is `qa-code-critic.md`); the two probes are F03 (`red_sandbox`, `probe_by_code`) and F05 (`brief_pack.py`).
- `B-194`: F09 chosen (expectation changed to the code, oracle provenance); the detector pieces are F11 (`function_sha`) and F12 (claims); no code file named.
- `B-205`: F15 chosen (design doc claims a test proof); alternative F12.
- `B-225`: F14 chosen (cost_capture takes the project table over the catalog); first backticked file is `config.json` (F04).
- `B-231`: `ticket_adapter.py assess` is S1 source relevance, so F02; the taxonomy lists `ticket_adapter` under F01 (S0). The module serves both stages.
- `B-249`: F16 chosen because the first file named is `host_probe.py`; the text is about the layout carrier `runtime_paths` / `install-paths.json` (F04).
- `B-250`: F04 chosen (yes-hash of `onboard_apply`); only data files (`dashboard-dirty.json`) are named, the code is unnamed.
- `B-237`: F05 (`context-bundle.json` first code-owned file named) vs F02 (`source-inventory.json`).
- `B-255д`: the item is only the identifier `username_ref`; F03 is a guess (stand login keys).
- `F-cmp2-10`: F17 (`artifact-contract-plan.md`); the validator it names is F08.
- `F-cmp2-24`: F03 (`runtime_probe.py --suggest`); the first code file named, `execution_request.py:1856`, is only where the symptom surfaced (F11).
- `F-cmp2-30`: F19: an error of the Lead's own reading; its code half is B-236 (F01).
- `probe_by_code / red_sandbox`: the taxonomy puts `probe_by_code` in F03 (stand access); semantically it is the critic's test-liveness receipt. Kept in F03 as dispatched; rows that name either file and sit in F03: B-002, B-207а, B-255а, run5-16, t-023, t-023, t-023, 4547ae7.

Rows with no file at all (feature by stage words, `file: —`): 82 rows of A1 (list: B-014, B-015, B-021, B-022, B-024, B-025, B-027, B-030, B-041, B-043, B-044, B-046, B-049, B-050, B-062, B-063, B-064, B-070, B-071, B-072, B-073, B-074, B-077, B-078, B-080, B-081, B-082, B-084, B-085, B-092, B-093, B-095, B-096, B-097, B-101, B-102, B-103, B-104, B-105, B-106, B-107, B-108, B-141, B-147, B-150, B-152, B-156, B-157, B-158, B-159, B-160, B-170, B-174, B-182, B-187, B-188, B-189, B-198, B-216, B-226, B-227, B-229, B-232, B-238, B-242, B-202, B-110, B-123, B-127, B-128, B-129, B-130, B-132, B-133, B-190а, B-190в, B-190г, B-193б, B-253е, B-255д, B-256б, B-256в).

Rows that enumerate sub-items but were kept whole (the dispatch named only B-247 and B-253 as lists; I also split B-190, B-193, B-207, B-255, B-256, whose sub-items are distinct defects): B-140 (five constants issues), B-143 (three), B-169 (four sites), B-171 (five relays), B-172 (three causes of one finding), B-191 (four requirements of one principle), B-206 (four requirements of one verdict), B-216 (a/b of one defect), B-218 (six self-declarations), B-235 (four steps of one task).

Cross-references I made that the source text does not make (so they are NOT in the fix-of-fix column):

- `F-cmp2-17` (gate shown with factory-fixable items) is the same symptom as `B-177` (cmp1 06:38, 30.09); `t-211/t-214 gate_repair` was the fix.
- `F-cmp2-25`, `F-cmp2-27` (a person's word recorded, nothing executes it) repeat `B-047` (27.09) and `B-220` (30.09).
- `F-cmp2-28` (S5 window with all instances blocked) is the window-gate family of `e64b329` (27.09) and `t-079` (cmp1).
- `rehearsal-10` (`project_decisions add-finding` "invalid finding scope") already happened at cmp1 stop 5 (`cmp1.md`, 06:29: "`project_decisions.py add-finding` - «invalid finding scope»").
- `rehearsal-13` (gate B question breaks `human-questions.md`) already happened at cmp1 stops 2 and 7 and in `B-171`.
- `rehearsal-12` / `B-253г` (block-buffered stdout) is `B-178` (cmp1, 30.09); the rehearsal text itself says "FR-43 - B-линия" (that one is marked `rec`).
- `1556e9b` (28.09) and `7f84cb1` (27.09) fix the same rule ("an answered boundary is never re-asked with the same text") twice.
- eaten-escape-byte (heredoc `\b`): `MEASUREMENTS.md` 6.1 and `driver3-state-before-compact.md` count 8 occurrences in 27-28.09; rows: `run5-21` (rec), `c406b0a` (swept "no eaten escape byte remains"), `5a66517` (found another, rec).
- Refusal-without-repair-marker chain (a role-closable refusal reaches the conductor and the person): `3416cc7` (26.09, `handoff_check` ends closed-list refusals with REPAIR_MARKER), `fd9584f` (26.09, length refusal gets the marker), `94e8329` (28.09, P4b, the same marker rule across scripts), `F-cmp2-21` (01.10, `s5_precheck.py:1890` footer without the marker, t-213). Only `F-cmp2-21` carries a fix-of-fix quote ("Класс: любой скрипт, печатающий отказ роли без маркера").
- S1 material chain of 26.09 (same family within one day): `1090eea` -> `5bacf2f` ("Three more of the same family") -> `5782744` (the ladder of `1090eea` did nothing without a source id) -> `06e669b` (attachment fields in the gap question); later `B-246`/`B-247` (the REST/VCS auth-loss twins).
- `B-182` / `run5-17` layer 3 / `B-062`: the road to a bug exists only from a red test - listed three times (B-182 itself marks it `rec`).

Sources read in full or in the relevant parts and what they yielded: `plans/BACKLOG.md` (all 217 parent rows), `experiments/cmp2-15045/cmp2.md` (findings block, lines 76-247, and the head), `experiments/cmp2-15045/rehearsal.md` (whole), `docs/FINDINGS.md` (whole; F-1..F-3 are process findings about this repository), `ai-packages/qa-factory/design/factory-rules-debt.md` (whole; its open rows duplicate B/FR rows except the FR-41 witness-gate row -> `debt-1`; its "Fixed since this walk" entries are folded into commit rows), `experiments/measurers/answers-13797.md` (lines 140-193 and headings: comparison facts, one finding -> `ans-13797-1`; the sixteen fixes of 24-25.09 are before the window), `plans/MEASUREMENTS.md` (sections 2.4, 3, 4, 6; lessons carried from older plans - only 2 lines carry a date >= 26.09 and they are statements about the 27-28.09 fixes and the heredoc trap, no new id-ed finding; control: the same `grep -c -E` on BACKLOG.md gives 136), `experiments/measurers/runs/cmp1.md`, `driver3-s8-findings.md`, `driver3-handoff.md`, `driver3-state-before-compact.md` (run 5 and cmp1 findings), `driver2-findings.md` (run 4, 23-24.09, outside the window: not tabulated), `cmp1-case-quality.md` / `cmp1-stage-role.md` (quality and cost reviews: their findings are carried by B-185, B-189..B-191, B-184).

