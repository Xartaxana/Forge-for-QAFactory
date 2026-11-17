digest: v1 t-1273
## Objects
| id | kind | gist | paths | status | owner | links | ev |
|---|---|---|---|---|---|---|---|
| q1a | fact | Loop dispatches stage via getattr(self, f"stage_{stage}")() in _act_prepare_stage; S6 and S7 both enter there | ai-packages/qa-factory/scripts/driver_machine.py:1342-1355 | found | — | q1b | T6 |
| q1b | fact | stage_S6 closes S6 by code at several sites (close_by_code); no single S6->S7 hook | ai-packages/qa-factory/scripts/driver_stage_s6.py:511-620 | found | — | q1a,q1c | T7 |
| q1c | fact | S6 close sites: s6.accepted 531, s6.nothing 541, s6.results_stand 580, s6.reprobed 830, s6.manual_close 1084 | ai-packages/qa-factory/scripts/driver_stage_s6.py:531-1085 | found | — | q1b | T7,T8,T9 |
| q1d | fact | Manual half: runner block via run_manual_block (1638); manual_close runs finalize_task then consumer_need_record then close_by_code | ai-packages/qa-factory/scripts/driver_stage_s6.py:1060-1085 | found | — | q1c | T8 |
| q1e | fact | close_by_code(stage, reason, evidence, finalize, site...) is the shared close writer for S6 and S7 | ai-packages/qa-factory/scripts/driver_stage_s7.py:763-786 | found | — | q1c | T10 |
| q1f | fact | S7 entry is Driver.stage_S7; first code reads state, s7_closed_by_scribe, then failures_to_triage (which reads run-report.json), then s7_pretriage, then run_role qa-failure-analyst | ai-packages/qa-factory/scripts/driver_stage_s7.py:48-145 | found | — | q1a | T5 |
| q1g | fact | Candidate positions (facts only): inside manual_close after finalize_task.py (1079-1081) before close_by_code (1084); or top of stage_S7 before failures_to_triage (74); stage_S7 line 74 call is the only S7 pre-dispatch code | ai-packages/qa-factory/scripts/driver_stage_s6.py:1079-1085 | found | — | q1d,q1f | T8,T5 |
| q1h | fact | S6 auto-half runner dispatch: run_role("S6","qa-runner",...) then returns if manual_scope; loop re-enters stage_S6 for manual block | ai-packages/qa-factory/scripts/driver_stage_s6.py:603-620 | found | — | q1b | T7 |
| q2a | fact | qa-runner page rules: unresolved_question recorded and go on; env_blocked with owner and remedy, halt block | ai-packages/qa-factory/agents/qa-runner.md:71-74 | found | — | q2e | T11 |
| q2b | fact | driver code never reads env_blocked or unresolved_question for the runner: only hits are S5 text (driver_machine 1731,1748), S7 text (driver_stage_s7 740,744) and a claims key (driver_dispatch 1592) | ai-packages/qa-factory/scripts/driver_machine.py:1731 | found | — | q2e | T12 |
| q2c | fact | KNOWN_REFUSALS table: 22 rows matching refusal text; none names runner/S6/unprepared; ask_person rows: story_budget, executor, readiness | ai-packages/qa-factory/scripts/driver_dispatch.py:38-107 | found | — | q2e | T13 |
| q2d | fact | Runner unprepared record is read downstream only (coverage_contract, finalize_task, contract.py:4662, s7_pretriage:163, ledger:1668); none calls no_move | ai-packages/qa-factory/scripts/s7_pretriage.py:163 | found | — | q4c | T3 |
| q2e | fact | No road found from a runner mid-S6 turn to no_move or the person: no S6/runner site among no_move callers (driver_dispatch 3291,3356,3879 are refusal/repair/exit caps by stage var) | ai-packages/qa-factory/scripts/driver_dispatch.py:3291 | absent | — | q2a,q2b,q2c | T2,T4,T12,T13,T14 |
| q3a | fact | def no_move(self, state: dict, moves=None) -> str; returns continue/retry after conductor move, else raises Person | ai-packages/qa-factory/scripts/driver_conductor.py:617-642 | found | — | q3b | T1 |
| q3b | fact | State keys documented: why, kind, stage, dispatch, text, words, words_file, files, call, block, lead, keep, fallback, move, token, lines (docstring); sites also pass site_doors and site_fallback | ai-packages/qa-factory/scripts/driver_conductor.py:622-628 | found | — | q3a | T1 |
| q3c | fact | Model site: s7_open_work_ask calls self.no_move({why threshold, kind open_work, call False, stage S7, dispatch life, lead, site_doors ("close",), site_fallback lambda said: self.s7_open_work_person(...)}) | ai-packages/qa-factory/scripts/driver_stage_s7.py:463-480 | found | — | q3d | T15 |
| q3d | fact | Fallback builds Person("open_work", self.closed_question("s7.open_work", lead, [close, dict(self.STOP_OPTION)]), "S7", life) | ai-packages/qa-factory/scripts/driver_stage_s7.py:482-489 | found | — | q3e | T15 |
| q3e | fact | Answer executor _answer_open_work: tokens close/stop; other words go to self.unread(...); state kept in self.state["s7_open_work"][life] | ai-packages/qa-factory/scripts/driver_stage_s7.py:491-506 | found | — | q3c | T15 |
| q3f | fact | Registration 1: question priced in question-prices.json key s7.open_work (rows answer/factory/person/delivery[/unverified]) | ai-packages/qa-factory/references/question-prices.json:197-200 | found | — | q3c | T16 |
| q3g | fact | Registration 2: driver-layers.json row per new Driver method {name, kind, home, row, note}; model rows for s7_open_work_ask/person | ai-packages/qa-factory/scripts/tests/fixtures/driver-layers.json:729-730 | found | — | q3c | T17 |
| q3h | fact | Registration 3: census in test_conductor_doors.py PINNED_ELSEWHERE and census (both ways, site must raise key; K15 for s7.open_work) | ai-packages/qa-factory/scripts/tests/test_conductor_doors.py:662,869-877 | found | — | q3f | T18 |
| q3i | fact | Seam sites are discovered by scan AF.a27_scan(...), not a static list file; test_no_move_seam_sites.py line 604 uses scan.sites; no_move_sites list file not found by grep | ai-packages/qa-factory/scripts/tests/test_no_move_seam_sites.py:604 | found | — | q3h | T19 |
| q3j | fact | dry_exits.py is at scripts/tests/dry_exits.py (not scripts/); scans Person/site_seam_person calls (PERSON_CALLS line 51), WHY_VALUES line 78, loads no_move.load_question_prices | ai-packages/qa-factory/scripts/tests/dry_exits.py:51 | found | — | q3f | T20 |
| q3k | fact | The seam argument `moves` is conductor-actions row ids; hygiene: _no_move reads site_check(site_doors, NM.data()) so a site door must not be a move's word | ai-packages/qa-factory/scripts/driver_conductor.py:644-655 | found | — | q3a | T1 |
| q4a | fact | CLI verb unprepared: args --task-root, --case (required), --not-walked (non-blank when given; required if no recorder step exists), --observations-file; prints {written, case, block} | ai-packages/qa-factory/scripts/manual_evidence.py:2217-2228 | found | — | q4b | T21 |
| q4b | fact | write_unprepared record fields: schema_version 2, case, obligation_ids, unprepared {reason, walked, not_walked?}, observations, dispatch_id, attempt_started_at, attempt_ended_at, source_revision, attempt_id? | ai-packages/qa-factory/scripts/manual_evidence.py:1536-1541 | found | — | q4a | T22 |
| q4c | fact | No closed/enumerated field in the record today: unprepared.reason comes from request.json marker, not_walked free text (cut at NOT_WALKED_MAX); only walked is bool | ai-packages/qa-factory/scripts/manual_evidence.py:1531-1537 | found | — | q4b | T22 |
| q4d | fact | Reader unprepared_rows(report) over current_manual_checks; yields case, obligation_ids, reason, observations, finding, walked, not_walked | ai-packages/qa-factory/scripts/manual_evidence.py:1251-1269 | found | — | q4e | T3,T23 |
| q4e | fact | unprepared_rows non-test caller: ledger.py:1668 ("unprepared_walks"); other callers are tests only (test_unprepared_outcome 187,250; test_manual_projection 166; test_manual_evidence 1143) | ai-packages/qa-factory/scripts/ledger.py:1668 | found | — | q4d | T3 |
| q4f | fact | Direct get("unprepared") readers: coverage_contract.py 663,666,757,776 and 1370 area; finalize_task.py 543,553,556,569; contract.py 4662; s7_pretriage.py 163; manual_evidence.py 1256,1370,1247; check_delivery.py unprepared_records 1885 (reads ledger unprepared_walks) | ai-packages/qa-factory/scripts/coverage_contract.py:663 | found | — | q4d | T3 |
| q4g | fact | Request-side marker reader unprepared_request(task, case): request.json unprepared dict or None; used by write_unprepared 1507, coverage_contract 759, manual_evidence 1599,1619 | ai-packages/qa-factory/scripts/manual_evidence.py:1240-1248 | found | — | q4d | T23 |
| q4h | fact | Driver S6 prints unprepared at plan and gives the runner the command text for `manual_evidence.py unprepared` | ai-packages/qa-factory/scripts/driver_stage_s6.py:1369,1958-1964 | found | — | q4a | T3 |
| q5a | fact | def state(root, key, environment="", element="", cfg=None) -> dict: pure, never raises; keys state,row,source,problem,twins,malformed | ai-packages/qa-factory/scripts/project_knowledge.py:295-312 | found | — | q5b | T24 |
| q5b | fact | def record(root, *, key, environment, element, state, scope, value, words, source, story, by, where="", task_root=None, only_if_latest=None) -> (row, problem, created) | ai-packages/qa-factory/scripts/project_knowledge.py:766-785 | found | — | q5c | T25 |
| q5c | fact | Stand-scoped key: a KEYS entry derived from config-keys.json row with scope "stand" (_derive_keys 109-122); _usable requires environment non-empty for stand scope (211) | ai-packages/qa-factory/scripts/project_knowledge.py:109-122 | found | — | q5b | T24 |
| q5d | fact | Constants: STATES (known, not_needed, noticed_unconfirmed), SOURCES (person, role, legacy_config), BY = ("conductor","driver"), comparators role_form and exact | ai-packages/qa-factory/scripts/project_knowledge.py:126-163 | found | — | q5b | T24 |
| q5e | fact | knowledge row quoted: "environments.stand_lessons": {"store": "registry", "compare": "exact", "scope": "stand", "needed_by": [project_knowledge.py:lessons, gate_preflight.py:check_stand_lessons, brief_pack.py:stand_lesson_lines], "ask_when": null} | ai-packages/qa-factory/references/config-keys.json:711 | found | — | q5c | T26 |
| q5f | fact | brief_pack.stand_lesson_lines(project, stand): PK.lessons(project, stand); returns ["- Stand lessons: " + line]; unreadable gives one line "could not be read"; none gives [] | ai-packages/qa-factory/scripts/brief_pack.py:2881-2893 | found | — | q5e | T27 |
| q5g | fact | Reaches runner: manual_stand_lines (2896) builds `## The stand`; docstring says stand_lesson_lines is the one formatter for it and for S5 automator/critic head | ai-packages/qa-factory/scripts/brief_pack.py:2884,2896 | found | — | q5f | T27 |
| q5h | fact | conductor-actions.json line 8 whole (the spec's "row 8", rework): {"says": "rows go back to qa-test-strategist at S3 / cases go back to qa-case-designer at S4 / the question packet goes back to qa-requirements-tester at S2 / S7 re-triages / a bug candidate (a place the code reads wrong that no executed check covers) goes to the failure analyst at S7 as a bug report (the rework names the candidate's ref, not a case) / the case designer rewrites a `preconditions` line", "run": "controller.py --task-root <r> --operation rework --stage S<n> --role <that role> [--rows <ids> \| --cases <ids> \| --candidates <refs>] --reason \"<the finding, verbatim>\" --brief"} | ai-packages/qa-factory/references/conductor-actions.json:8 | found | — | q5i | T28 |
| q5i | fact | conductor-actions.json line 29 whole (stand lesson): {"says": "the person teaches how the stand behaves (an operation that takes long, how to narrow it), meant for the next runs too", "run": "project_knowledge.py lesson --task <T> --subject \"<a few words>\" [--stand <name>] [--wait-s <seconds>] --words-file <file holding their words>; a story that leaves no trace refuses it"} | ai-packages/qa-factory/references/conductor-actions.json:29 | found | — | q5h | T29 |
| q5j | analog | rework row 8 has no "id" key; rows are unnamed objects at lines 8 and 29 (other rows at 66+ use "id"); spec cites them as line numbers | ai-packages/qa-factory/references/conductor-actions.json:25 | found | — | q5h | T30 |
| q5k | fact | spec cited rework row mentions --cases for S6; row 8 text lists stages S3,S4,S2,S7 and `--stage S<n>`, S6 is not named in its says | ai-packages/qa-factory/references/conductor-actions.json:8 | found | — | q5h | T28 |

## Trail
| tid | op | target | pattern / range | flags | result | control |
|---|---|---|---|---|---|---|
| T1 | read | ai-packages/qa-factory/scripts/driver_conductor.py | 600-675 | — | read ai-packages/qa-factory/scripts/driver_conductor.py:600-675 | — |
| T2 | grep | ai-packages/qa-factory/scripts | `def no_move\|no_move\(` | glob=*.py | found 48; driver_conductor.py:617, driver_stage_s7.py:479, driver_dispatch.py:3291, driver_machine.py:1721 | — |
| T3 | grep | ai-packages/qa-factory | `unprepared` | -i glob=*.py | found 80; manual_evidence.py, coverage_contract.py:663, finalize_task.py:543, s7_pretriage.py:163, ledger.py:1668 | — |
| T4 | grep | ai-packages/qa-factory/scripts | `unprepared_rows` | glob=*.py | found 12; ledger.py:1668, manual_evidence.py:1251 | — |
| T5 | read | ai-packages/qa-factory/scripts/driver_stage_s7.py | 1-150, 458-507 | — | read ai-packages/qa-factory/scripts/driver_stage_s7.py:1-150 | — |
| T6 | read | ai-packages/qa-factory/scripts/driver_machine.py | 1335-1404, 4170-4228 | — | read ai-packages/qa-factory/scripts/driver_machine.py:1335-1404 | — |
| T7 | read | ai-packages/qa-factory/scripts/driver_stage_s6.py | 511-700, 805-854 | — | read ai-packages/qa-factory/scripts/driver_stage_s6.py:511-700 | — |
| T8 | read | ai-packages/qa-factory/scripts/driver_stage_s6.py | 1060-1100 | — | read ai-packages/qa-factory/scripts/driver_stage_s6.py:1060-1100 | — |
| T9 | grep | ai-packages/qa-factory/scripts | `def (finalize_task\|...)\|finalize_task` | glob=driver_*.py | found 40; driver_stage_s6.py:538, 575, 823, 1079 | — |
| T10 | grep | ai-packages/qa-factory/scripts | `def (stage_close\|...)` listing of S7 members | glob=driver_stage_s7.py | found 45; close_by_code at 763 | — |
| T11 | read | ai-packages/qa-factory/agents/qa-runner.md | 69-75 | — | read ai-packages/qa-factory/agents/qa-runner.md:69-75 | — |
| T12 | grep | ai-packages/qa-factory/scripts | `env_blocked\|unresolved_question` | -i glob=driver*.py | found 5; driver_machine.py:1731, driver_stage_s7.py:740 | — |
| T13 | read | ai-packages/qa-factory/scripts/driver_dispatch.py | 38-136 | — | read ai-packages/qa-factory/scripts/driver_dispatch.py:38-136 | — |
| T14 | grep | ai-packages/qa-factory/scripts/handoff.py | `status` | -i | absent | T3 |
| T15 | read | ai-packages/qa-factory/scripts/driver_stage_s7.py | 458-507 | — | read ai-packages/qa-factory/scripts/driver_stage_s7.py:458-507 | — |
| T16 | read | ai-packages/qa-factory/references/question-prices.json | 195-208 | — | read ai-packages/qa-factory/references/question-prices.json:195-208 | — |
| T17 | grep | ai-packages/qa-factory | `s7_open_work_ask\|s7_open_work_person` | glob=*.{json,py,md} | found 8; driver-layers.json:729 | — |
| T18 | grep | ai-packages/qa-factory | `s7\.open_work` | glob=!*.md | found 15; test_conductor_doors.py:662, question-prices.json:197 | — |
| T19 | grep | ai-packages/qa-factory/scripts/tests | `scan = \|import .*scan\|SITE_LIST\|site_list\|no_move_sites\|seam-sites` | glob=*seam*.py | found 1; test_no_move_seam_sites.py:604 | — |
| T20 | grep | ai-packages/qa-factory/scripts/tests/dry_exits.py | `no_move\|seam` | -i | found 15; dry_exits.py:51, 78 | — |
| T21 | read | ai-packages/qa-factory/scripts/manual_evidence.py | 2170-2235 | — | read ai-packages/qa-factory/scripts/manual_evidence.py:2170-2235 | — |
| T22 | read | ai-packages/qa-factory/scripts/manual_evidence.py | 1500-1555 | — | read ai-packages/qa-factory/scripts/manual_evidence.py:1500-1555 | — |
| T23 | read | ai-packages/qa-factory/scripts/manual_evidence.py | 1245-1270 | — | read ai-packages/qa-factory/scripts/manual_evidence.py:1245-1270 | — |
| T24 | read | ai-packages/qa-factory/scripts/project_knowledge.py | 100-215, 295-325 | — | read ai-packages/qa-factory/scripts/project_knowledge.py:100-215 | — |
| T25 | read | ai-packages/qa-factory/scripts/project_knowledge.py | 766-790 | — | read ai-packages/qa-factory/scripts/project_knowledge.py:766-790 | — |
| T26 | grep | ai-packages/qa-factory/references/config-keys.json | `"knowledge"` | — | found 1; config-keys.json:705 | — |
| T27 | read | ai-packages/qa-factory/scripts/brief_pack.py | 2878-2898 | — | read ai-packages/qa-factory/scripts/brief_pack.py:2878-2898 | — |
| T28 | read | ai-packages/qa-factory/references/conductor-actions.json | 8 | — | read ai-packages/qa-factory/references/conductor-actions.json:8 | — |
| T29 | read | ai-packages/qa-factory/references/conductor-actions.json | 29 | — | read ai-packages/qa-factory/references/conductor-actions.json:29 | — |
| T30 | grep | ai-packages/qa-factory/references/conductor-actions.json | `"id"` | — | found 12; conductor-actions.json:25, 66, 81 | — |
| T31 | read | docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r4-7b-7c-e7.md | 323-367, 440-447 | — | read docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r4-7b-7c-e7.md:323-367 | — |

## Forks
- Whether the check "typed need, no registry answer" sits in manual_close (driver_stage_s6.py:1079-1084), at the top of stage_S7 (driver_stage_s7.py:74), or elsewhere is a design choice; facts above: S6 has five close sites (q1c), so only manual_close covers the manual half; stage_S7 is the single S7 entry (q1f).
- The spec asks for a typed need field; no closed field exists on unprepared today (q4c); adding one is a design choice.
this needs a decision from a tier above.

## Not done
- Q2 negative (q2e) is a conclusion over greps of driver*.py for env_blocked/unresolved_question, KNOWN_REFUSALS read in full, and handoff.py `status` (absent, control T3 is a different file/pattern, so T14's control is weak: a same-target control was not run). I did not read the handoff form schemas under references/ for status fields, nor consumer_* helpers (driver_stage_s6.py:163-480) in full.
- Did not read run_manual_block (driver_stage_s6.py:1638 onward) or driver_stage_s6.py:1797-1970 (run_s6_lanes), so what runs between the runner's last manual turn and manual_close is not traced beyond the close site.
- Did not locate where test_no_move_seam_sites.py enumerates required sites beyond line 604's a27_scan use; audit_factory.py:2424 a27_no_move and its scan were not read. dry_exits `--check` rows were not read.
- Row 8 and row 29 are quoted by file line (they have no "id" key); the spec calls them "rows 8 and 29".
- The unprepared direct-reader list in q4f is from the grep window (head_limit 80), may be incomplete beyond it; ledger.py:1668 is the one non-test unprepared_rows caller found by the full-count grep T4.
