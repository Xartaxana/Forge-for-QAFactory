# T0 spike — the wide refusal scan and its numbers (told-before-work, node T0)

Branch `wip/tbw-t0`. Owns: `refusal_registry.py`, `test_refusal_registry.py`, this report, `changelog.d/tbw-t0.md`.
Architecture: AR-13 (one scanner, widened in place), AR-20 (no ratchet moved; census still 1142 units, ceilings untouched).
All numbers below are from base commit `5c16666` plus this branch; reproduce with the commands named. Measurer scripts are NOT
committed (scratch, `…\scratchpad\{measure,baseline,fixture_before,m4,summ,norow}.py`); `measure.py` reads the wide report and prints
M1/M2/M3/M5/M7/M8, `m4.py` prints M4's facts.

## 0. What the scan does (read this before the numbers)

`python -B ai-packages/qa-factory/scripts/refusal_registry.py --sites --wide --census ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json --json`
(37 s). One switch: `raise_family(..., wide=True)` puts `WIDE_TRANSPORTS` in every spec; `sites(raises=spec)` reads it. Without it the
output is today's: proven by table rows (stored expectation from the unmodified module) and by hashes of the live scans before/after
the edit (section 5). Wide records carry `transport`, `state` (`sourced` / `tagged` / `bare`, `walk_error`) and, for a `refusal`
call, `check`. Bounded list transport: `sites(..., blocking=<set of (file, function)>)`; None = every function (over-count).

## 1. M1-M8

**M1 — sites per transport per (file, function)** (`measure.py ... m1`; full per-unit data is the `units` array of the wide JSON):

| transport | sites | units | files |
|---|---|---|---|
| deny | 21 | 6 | 1 |
| block | 54 | 30 | 7 |
| refuse | 101 | 29 | 16 |
| run_guarded (family raise in a file that calls `run_guarded`) | 325 | 112 | 15 |
| raises (family raise elsewhere) | 1100 | 450 | 121 |
| sys.exit(str) | 0 | 0 | 0 |
| SystemExit(str) | 0 | 0 | 0 |
| stderr-print+return | 328 | 127 | 88 |
| stderr-write+return | 0 | 0 | 0 |
| list (append/extend/+= in a census-blocking unit) | 1188 | 270 | 85 |
| TOTAL | 3117 | 848 units | 279 files scanned |

deny+block+raises+run_guarded = 1500 = today's census-style `sites(files=all, raises=family)` count (control: equal). Zeros are real:
Grep `sys\.exit\((f?["']|...)|SystemExit\(f?["']|sys\.stderr\.write` over `scripts/*.py` finds 24 hits, all under `scripts/tests/`
or in `refusal_registry.py` itself (positive control: the same pattern found them). States: sourced 0, tagged 0, bare 3117.
Largest units: `controller.py:validate` 115 (74 raises + 41 list), `execution_request.py:validate_request` 57, `ticket_adapter.py:main` 44,
`execution_request.py:build_mine_request` 43, `acceptance.py:validate_window` 34.

**M2 — role-reachable share by the census join** (`measure.py ... m2`): units 848; with a census row 732 (86.3 %); no row 116;
role-reachable units (row lists any role besides `conductor`) 170; conductor-only 562. Role-reachable SITES 697 of 3117 = 22.4 %
(list 564, block 45, raises 40, stderr 22, deny 21, run_guarded 5). Per role (units / sites): qa-automator 149/584, qa-test-strategist
138/552, qa-case-critic 134/514, qa-requirements-tester 128/484, the other eight 115-117 / 436-443. Caveat that moves the numbers:
guard units list all 12 roles (census over-label, spec 0.3), so each role's count is an upper bound; the conductor-only 562 are the
controller/driver units (spec 0.4 under-labels unknown here).
The 116 units with no row are ALL units that exist only because of the new transports: 90 stderr-only, 22 refuse-only, 4 both
(CLI `main`s such as `ticket_adapter.py:main`, `manual_evidence.py:main`, `manifest_put.py:run`, `stage_done.py:run`...). Units with a
census-visible transport (deny/block/raises/run_guarded/list) and no row: 0.

**M3 — 30 stderr sites sampled, for the LEAD to classify (refusal or not; I did not).** Every `print(.., file=sys.stderr)` and
`sys.stderr.write` of the three files (26 in run_suite.py, 38 in stage_done.py, 16 in manifest_put.py), 10 per file at even spacing
`hits[i*len//10]`. `fn_fails` = function has a failing return/exit; `scanned` = the wide scan counts it (needs fn_fails). Line shown
with 2 lines before. Site text is cut at 150 chars.

run_suite.py
1. :970 `_refuse_phantom_story` fails=T scanned=T — `except StoryRootError as exc:` / `print(json.dumps({"status": "invalid_request", "error": str(exc)}...), file=sys.stderr)` / next line `sys.exit(2)`
2. :1927 `_say_phases` fails=F scanned=F — `try:` / `print(_phases_line(phases_of(), total_of() ...), file=sys.stderr)` / `except Exception as exc:` (docstring: "whatever goes wrong, the call goes on")
3. :2032 `mine` fails=T scanned=T — `shown = str(path)` / `print(f"MINE: {shown} - dispatch {request['dispatch_id']}, {request['purpose']}, ... instance(s)", file=sys.stderr)` / `for note in notes:`
4. :2110 `run` fails=T scanned=T — `except Exception as exc:` / `print(f"PHASES (note): not measured: {type(exc).__name__}: {exc}", file=sys.stderr)` / `summary_path = ev / ...`
5. :2307 `run` fails=T scanned=T — comment "Its own line, and on stderr like RUN REPORT GAP" / `print("STAND SIGNAL: " + str(signal.get("sentence") ...), file=sys.stderr)` / `if getattr(args, "job_store"...`
6. :2730 `main` fails=T scanned=T — `skeleton, legend = template(args.template)` / `print("\n".join(legend), file=sys.stderr)` / `print(json.dumps(skeleton...))`
7. :2758 `main` fails=T scanned=T — `except Exception as exc:` / `print(json.dumps({"status": "invalid_schedule", "error": str(exc), "notes": notes}), file=sys.stderr)` / `sys.exit(2)`
8. :2867 `main` fails=T scanned=T — `if policy is None and not args.mine:` / `print(f"RUN BUDGET (note): {budget_note}", file=sys.stderr)` / `if policy is not None ...`
9. :2891 `main` fails=T scanned=T — `for note in (checked or {}).get("notes") or []:` / `print(f"NODE IDS (note): {note}", file=sys.stderr)` / `launched = apply_resolved_ids(...)`
10. :2925 `main` fails=T scanned=T — `if removed:` / `print("RUN BUDGET (note): " + say(policy, "reruns_removed", flags=..., purpose=...), file=sys.stderr)` / comment about a placeholder

stage_done.py
11. :384 `s9_exit` fails=F scanned=F — `except OSError as exc:` / `print(f"note: the record of the standing refusal could not be kept ({exc}); a word recorded against it reads as not verified", file=sys.stderr)` / `return code`
12. :466 `gate_rehearsal_pairs` fails=F scanned=F — `except Exception as exc:` / `print(f"stage_done: the gate {gate} rehearsal could not run (...); the stage closes without it", file=sys.stderr)` / `return []`
13. :975 `record_acceptance` fails=T scanned=T — `if not stage_def.get("roles"):` / `print(f"stage_done: {stage} has no roles in references/stages.json; ...", file=sys.stderr)` / `return EXIT_BAD_ARGS`
14. :1008 `record_acceptance` fails=T scanned=T — `if not form_path.is_file():` / `print(f"stage_done: the stage critic's form {rel} does not exist; expected work/handoffs/<critic dispatch>.yaml", file=sys.stderr)` / `return EXIT_BAD_ARGS`
15. :1034 `record_acceptance` fails=T scanned=T — `else:` / `print(f"stage_done: the stage critic's form {rel} does not say which dispatch of {author_role} it reviewed: ...", file=sys.stderr)` / `return EXIT_BAD_ARGS`
16. :1107 `run` fails=T scanned=T — `if refusal:` / `print(refusal, file=sys.stderr)` / `return EXIT_BAD_ARGS`
17. :1131 `run` fails=T scanned=T — `if source_check["gaps"]:` / `print("stage_done: S1 continues with explicit source gap(s): " + "; ".join(source_check["gaps"]), file=sys.stderr)` / comment "The stage in front of a gate does not close while..."
18. :1181 `run` fails=T scanned=T — `if passed:` / `print("stage_done: closing S9 over a running stage on the person's word: " + ..., file=sys.stderr)` / comment "The report check stands AFTER..."
19. :1251 `run` fails=T scanned=T — `return EXIT_BAD_ARGS` (previous branch) / `print("stage_done: closing a stage the controller has not accepted, on the person's word: " + ..., file=sys.stderr)` / comment "The other half of that rule..."
20. :1551 `main` fails=T scanned=T — `if not args.stage:` / `print("stage_done.py: --acceptance needs --stage (S2, S3 or S4)", file=sys.stderr)` / `return EXIT_BAD_ARGS`

manifest_put.py
21. :2247 `_seed_from_legacy` fails=T scanned=T — comment "Told apart from the fragment's by WHICH commit raised" / `print("manifest_put: your fragment was NOT committed. The legacy manifest was copied into the journal ... projection failed ...", file=sys.stderr)` / `return EXIT_BAD_FRAGMENT`
22. :2361 `run` fails=T scanned=T — `except Exception as e:` / `print(f"manifest_put: cannot read the fragment ({type(e).__name__}: {e})", file=sys.stderr)` / `return EXIT_BAD_FRAGMENT`
23. :2388 `run` fails=T scanned=T — `if novelty_problems:` / `print("manifest_put: " + _problems_text(task_root, "novelty", ...) + ". A tests[] row's novelty is written by manifest_from_tests.py alone ... " + REPAIR_MARKER + ".", file=sys.stderr)` / `return EXIT_BAD_FRAGMENT`
24. :2399 `run` fails=T scanned=T — `if base_problems:` / `print("manifest_put: " + _problems_text(..., "base-outcome", ...) + ". A tests[] row's base_outcome is ... " + REPAIR_MARKER + ".", file=sys.stderr)` / `return EXIT_BAD_FRAGMENT`
25. :2422 `run` fails=T scanned=T — `if problems:` / `print("manifest_put: " + _problems_text(task_root, "expectation", problems) + ". " + REPAIR_MARKER + ". " + _word_door(...), file=sys.stderr)` / `return EXIT_BAD_FRAGMENT`
26. :2435 `run` fails=T scanned=T — `if approval_problems:` / `print("manifest_put: " + _problems_text(task_root, "critic-approval", ...) + ". " + REPAIR_MARKER + ".", file=sys.stderr)` / `return EXIT_BAD_FRAGMENT`
27. :2442 `run` fails=T scanned=T — `if line_problems:` / `print("manifest_put: " + _problems_text(task_root, "assertion-line", ...) + ". Correct the row's assertion_id ... " + REPAIR_MARKER + ".", file=sys.stderr)` / `return EXIT_BAD_FRAGMENT`
28. :2463 `run` fails=T scanned=T — `if reason_conflicts:` / `print("manifest_put: " + _problems_text(task_root, "unresolved-reasons", ...) + ". " + REPAIR_MARKER + ".", file=sys.stderr)` / `return EXIT_BAD_FRAGMENT`
29. :2504 `run` fails=T scanned=T — comment "the door is a command the role runs: the replay" / `print("manifest_put: event committed; projection stale - the fragment is in the journal, do not send it again; ...", file=sys.stderr)` / `return EXIT_COMMITTED_STALE`
30. :2513 `run` fails=T scanned=T — `except (ValueError, OSError) as exc:` / `print(f"manifest_put: {exc}", file=sys.stderr)` / `return EXIT_BAD_FRAGMENT`

Mechanical observation only (not a classification): 3 of 30 are not counted by the scan (#2, #11, #12: functions with no failing
return); the 27 counted include progress/notes printed in a function that fails elsewhere (#3, #4, #5, #6, #8, #9, #10) — these are
where a "scan precision" below 100 % would come from. Lead: M3 precision = (counted sites you classify as refusals) / 27.

**M4 — detector scripts of `stages.json` (`detectors`, `advice`): is the family set a module-level tuple like `s5_precheck.CHECKS`?**
(`m4.py`; module-level str tuples and the `detector_verdict` calls found, then a read of how each names its findings)
- `s5_precheck.py` — YES: `CHECKS` (9 families).
- `planning_contract.py` — YES: `BRANCH_KINDS` (12) and `S3_EXIT_KINDS` (8), the `kind` of every finding (`planning_contract.py:1528, 1537, 3244`).
- `branch_accounting.py` — YES, by stage: `STAGE_CHECKS = ("S2","S3","S4","S5")`, one runner (one check) per stage (`:70`); no per-problem family tuple.
- `critic_rollcall.py` — NO: module tuples are verdict words and columns only.
- `check_coverage.py` — NO: no module-level str tuple at all.
- `sizing.py` (detector at S2 and adviser) — NO: columns and stopwords only.
Count: yes 3, no 3 (of 6). Not "mostly no"; borderline, the Lead reads it.

**M5 — sizes (all ESTIMATES: rows = sites x a stated mean line length; one row per CHECK is what ships, so sites over-count).**
Carrier: `measure.py ... m5`. Mean length of the 496 `- ` lines of the 12 existing key pages = 82 chars (81 used). `inject_context.MAX_BLOCK_CHARS` =
26000 is per injected FILE (`inject_context.py:45, 267`); `native_context.py:174-175` refuses a whole context over 100000 chars.
Current: key pages 3460-6626 chars (qa-case-critic has none); per-role injected total (first kind) 20119-46927 chars.
END-STATE estimate of the requirement section per role (sites = role-reachable sites by the census join, over-labelled; units = the
same join by unit, a closer proxy for rows):

| role | sites | sites x 81 | sites x 250 | units | units x 81 | units x 250 | current page | current injected |
|---|---|---|---|---|---|---|---|---|
| qa-automator | 584 | 47833 | 146000 | 149 | 12204 | 37250 | 4585 | 46913 |
| qa-bug-reporter | 439 | 35957 | 109750 | 116 | 9501 | 29000 | 3555 | 33136 |
| qa-case-critic | 514 | 42100 | 128500 | 134 | 10975 | 33500 | 0 | 36784 |
| qa-case-designer | 439 | 35957 | 109750 | 116 | 9501 | 29000 | 3851 | 26345 |
| qa-code-critic | 441 | 36121 | 110250 | 117 | 9583 | 29250 | 3958 | 46227 |
| qa-doc-scribe | 436 | 35711 | 109000 | 115 | 9419 | 28750 | 3460 | 42596 |
| qa-failure-analyst | 440 | 36039 | 110000 | 117 | 9583 | 29250 | 4612 | 40152 |
| qa-requirements-tester | 484 | 39643 | 121000 | 128 | 10484 | 32000 | 5046 | 20119 |
| qa-retro-analyst | 439 | 35957 | 109750 | 116 | 9501 | 29000 | 4142 | 30907 |
| qa-runner | 443 | 36284 | 110750 | 117 | 9583 | 29250 | 5292 | 34221 |
| qa-scout | 439 | 35957 | 109750 | 116 | 9501 | 29000 | 4185 | 30793 |
| qa-test-strategist | 552 | 45212 | 138000 | 138 | 11303 | 34500 | 6626 | 35794 |

Reading: a row per SITE at 81 chars exceeds `MAX_BLOCK_CHARS` (26000) for all 12 roles (35.7K-47.8K) and, added to the current
injected total, reaches 94.7K for qa-automator (limit 100000 on the whole native context) and passes it at 250 chars for every role.
A row per UNIT at 81 chars is 9.4K-12.2K (fits 26000 for all; page + rows <= 18K); at 250 chars it is 28.8K-37.3K (over 26000 for all
roles). The deciding unknown is rows per check, which T0 cannot measure: sites repeat a check, and the census over-labels guard
units with all 12 roles. The page is ONE file: the 26000 ceiling binds the section plus the existing page content.
Automator section as T4+T5 would draft it: A24 line entries 77, of them in a unit the census gives qa-automator 49; rows drafted from
their `refuses` = 13987 chars (full text, upper bound) or 9005 (each sentence capped at 220); T5: 9 `s5_precheck.CHECKS` families x 250 =
2250, manifest row from `window_record.REQUIRED_ROW_FIELDS` 160, role-commands rows (31 commands, `input`+`verify` text) 28378 chars
for all commands (upper bound: the automator calls fewer). Total 39.8K (capped T4) to 44.8K (full T4) with all 31 command rows;
without the command rows 11.4K-16.4K. Over 26000 only if the command rows ship whole.

**M6 — N0 landed?** NO. `git -C <worktree> fetch origin main` (origin/main = `c50d2f4`), then
`git grep -n "check_id\|with_check" origin/main -- scripts/detector_verdict.py scripts/driver_core.py` -> no output; positive control
`git grep -n "^class Record" origin/main -- ...detector_verdict.py` -> `detector_verdict.py:90:class Record(str):`.

**M7 — units on road (b) of 2.8** (AST over every non-test script: the NAME `REPAIR_MARKER` in a function, or a string constant
matching `S\d structured .* invalid`): `controller.py` has 3: `_code_review_refusal` (REPAIR_MARKER :6459; census row: NONE),
`_s3_completion_gate` (structured head :7513, a wide site; census `["conductor"]`), `_s5_plan_accept_problems` (:6855; census
`["conductor"]`). The spec's `_plan_rework_rows_problems` / `_plan_review_problems` do NOT name the marker or the head themselves
(they are reached through `_s5_plan_accept_problems`): the AST read finds 3, not 5. 36 functions in all files name the marker; of
them with a census row: `handoff_check.py::check` and `_blocked_row_problems` (12 roles), `manifest_put.py::run`, `run_suite.py::run`,
`red_sandbox.py::check_node_ids`/`refuse_same_path`, `window_record.py::build`/`run`/`write_review_receipt`, `story_step.py::start`/
`_stage_card` (all `["conductor"]`); with no row at all: `story_step.py::finish`, `decide`, `bind`, `_needs_author`, `_decide_refusal`,
`_gate_refusal`, `_open_window_refusal`, `_stamp_plan_review`, `_unresolved_refusal`, `plan_row.py::add_row/put_row/set_fields`,
`driver_dispatch.py::*`, `s5_precheck.py::report`, others. `controller.py:_code_review_refusal` having no census row means it is not
a census unit (its refusals are a returned list, not a raise): the units of this road are larger than the controller's.

**M8 — hook events per `stage_guard` / `inject_context` / `native_context` unit** (`measure.py ... m8`: intra-file call graph from the
entry functions; entries and events read from `hooks.json:49` (`Agent|Task|SendMessage` -> `inject_context.py`), `hooks.json:9-39`
(`Bash|PowerShell`, Write/Edit, Read, Grep/Glob -> `guard_pre_tool.py`, which calls `stage_guard.check` at `guard_pre_tool.py:1880`),
`codex.json:134-139` (`SubagentStart` -> `native_context.py`), `stage_guard.py:_check`):
- stage_guard: `check_dispatch` (deny 9), `_check_exploration` (5), `dispatch_errors`/`rule_order` (lists) -> PreToolUse `Agent|Task`;
  `check_resume` (3), `_unidentified_resume` (1) -> `SendMessage`; `check_command` (2), `rule_pathspec`, `rule_typed_runner` -> `Bash|PowerShell`
  (role-facing: roles call Bash); `check` (1 deny: the command walker's crash door) is reached for `Bash|PowerShell` (a walker error)
  — the scan could not place it by the call graph, I read `check` at `stage_guard.py:1222-1243`.
- inject_context: `collect_blocks`, `map_problems`, `dispatch`, `refuse_*` -> `Agent|Task|SendMessage`.
- native_context: `stage` (4 raises) is called by `inject_context.dispatch` (Agent|Task); no wide site in `deliver` (SubagentStart).
- Roles' tool lines (`host_adapter.role_tools`, 12 roles read): none lists Task, Agent or SendMessage -> the dispatch-time units
  (`check_dispatch`, `_check_exploration`, `check_resume`, `_unidentified_resume`, `inject_context.*`, `native_context.stage`) are
  conductor-facing by 2.8; `check_command` and the `rule_*` units under it are on a role's tool (Bash). Their census rows today list all
  12 roles + conductor (over-label), so T4's relabel applies to the first set only.

## 2. GATE (spec T0 row)

| number | measured | bound | verdict |
|---|---|---|---|
| walk errors / scanned files | 0 parse errors + 0 check-argument errors / 279 = 0.0 % | <= 5 % | go |
| `--census` join over site units | 732 / 848 = 86.3 % | >= 90 % | STOP |
| M3 precision | pending — the Lead classifies the 30 sites (27 counted) | >= 80 % | not computable by the builder |
| M4 | yes 3 / no 3 | "mostly no" -> narrow | not mostly no (borderline) |

Computed verdict by the rule as written: **stop** (join 86.3 % < 90 %). What the number is made of, for the Lead: all 116 units without
a row are units created ONLY by the new transports (90 stderr-only, 22 refuse-only, 4 both); the census cannot hold a row for them
because its units come from `sites()` without those transports. Over the units the census can know (a deny/block/raise/run_guarded/list
site) the join is 732/732. If the Lead reads the gate as "join over census-visible units", it is go on join, with M3 deciding go/narrow.
That reading is the Lead's, not mine: the T0 row says "site units". Either way T1's `told_ratchet` needs rows for those 116 units
(a census edit or its own table).

## 3. Differences from the spec / findings

1. **`check_of` NOT implemented (question).** The T0 row lists `check_of`; its name matches the census `UNIT_NAME_RE` (`check_*`), so
   it is a new census unit and `test_judgment_census.py` goes red (C1: "check unit with no row") until the fixture gets a row; the
   fixture is in this dispatch's non-goals. I implemented it, saw C1 red, removed it. Text to apply with a row
   `{"file": "refusal_registry.py", "function": "check_of", "class": "shape", "roles": ["conductor"], "owner": "data"}`:
   `def check_of(entry): return f"{Path(str(entry['file'])).stem}:{entry['id']}"`. The private call-id reader was renamed `_record_id`
   for the same reason (`_record_check` also matched `_check$`).
2. **The name `refusal` is not unique in the package.** `session_identity.refusal`, `role_digest.refusal`, `FR.refusal` (onboarding_notes),
   `RD.refusal` (exit_gate) already exist: a first version counting any `refusal(...)` found 6 false walk errors and 1+1 false
   sourced/tagged sites. The scan now counts a call only when the file binds it to `detector_verdict` (`from detector_verdict import
   refusal [as X]`, `import detector_verdict as DV; DV.refusal`, or inside `detector_verdict.py`). T2's constructor will collide by name
   with those four; the binding rule is what keeps them apart. Also for T2: inside `detector_verdict.refusal` the call
   `with_check(Record(problem), check)` passes a PARAMETER as the check, which the scan counts as a walk error (row pins it): T2 must
   either name that site or exempt a parameter pass-through inside the constructor.
3. **Blocking units for the list transport.** The spec says "a unit the census marks blocking", but `blocks` is computed by
   `test_judgment_census.units_of`, not stored in census rows. Gap, returned as a question; what I did so the measurement exists:
   `sites(..., blocking=)` takes a set (None = every function, over-count); the CLI `--wide` computes it by importing
   `test_judgment_census.units_of` lazily (dev-time path under `scripts/tests`, a layering the Lead may dislike: FR-44 keeps the
   census test-only), and falls back to None with a stderr line if the import fails. The 1188 list sites are counted under that set.
4. **`RECORD_SINKS` is populated, not empty** (`block`, `deny`, `refuse`, `run_guarded`): the DoD asks sourced fixtures, which need the
   sinks. No package site is `sourced` today (0), as the spec's "before T2" requires.
5. **Spec T0 row vs dispatch:** no difference found in the T0 row read (spec on disk at the start); the dispatch's M5 extension and the
   `sys.exit/SystemExit(str)` transports match §2.5. The spec's walk-error definition (§2.5) names a `refusal`/`with_check` call with a
   non-literal check; implemented per binding (item 2).
6. `raise_family(wide=True)` also catches `ValueError`/`RecursionError`/`MemoryError` from `ast.parse` (and `sites` wide does); the
   default path keeps raising exactly as before (a deliberate non-change). A 4000-term message and a 300-deep paren fixture do not crash.
7. `--census` without `--wide` joins the default A24 scan (tested). `--wide` alone prints no join.
8. Slow witnesses: `test_scenario_cart_1.py` (no output in 100 s), `test_scenario_local_1_0108.py` (> 180 s, backgrounded) are not
   awaited (PROJECT.md: slow files are CI's). `test_words_doors.py` took about 3 minutes (598/598 ok).

## 4. Blind spots of the wide scan (named, counted in the report: `blind_spots` of the JSON, `BLIND SPOT n` lines of the text)
Counts on the live package (279 files): `sys.exit`/`SystemExit` of a non-text expression 184; `raise` of a call to a factory function or
method 333 (upper bound; census says 52 rowless functions); stderr text in a function that returns an expression (not a literal
non-zero) 76; stderr text in a function with no failing return/exit 50; `raise A` / `raise exc` with no call 28 (upper bound: re-raises);
class with a stdlib exception base 49 (upper bound); transport call with no message argument 38; class base that is neither a plain
name nor `alias.Name` 2; class defined only under `scripts/tests` with a refusal-exception base 4. Alias of a transport and yield of an
error text: 0 on the live package, each pinned by a fixture row. Every census blind spot of the header is a table row with verdict
"named blind spot" or "seen" (section 6).

## 5. Witness (verbatim, run from this branch; paths shortened to `PKG` = `...\.claude\worktrees\tbw-t0\ai-packages\qa-factory`)

```
$ python -B PKG\scripts\tests\scenario_walk.py --witness-for scripts/refusal_registry.py
scripts/refusal_registry.py: scenario test_scenario_cart_1.py (story cart-1)
scripts/refusal_registry.py: scenario test_scenario_local_1_0108.py (story local-1-0108)
scripts/refusal_registry.py: scenario test_scenario_local_1_arm_b.py (story local-1-arm-b)
scripts/refusal_registry.py: keep test_guard_command_text.py (layer detector, covers it)
scripts/refusal_registry.py: keep test_judgment_census.py (layer register, covers it)
scripts/refusal_registry.py: keep test_refusal_registry.py (layer register, covers it)
scripts/refusal_registry.py: keep test_resume_stopped.py (layer detector, covers it)
scripts/refusal_registry.py: keep test_s0_close_order.py (layer detector, covers it)
scripts/refusal_registry.py: keep test_whole_identifier.py (layer detector, covers it)
scripts/refusal_registry.py: keep test_words_doors.py (layer detector, covers it)
$ python -B PKG\scripts\tests\test_refusal_registry.py                ->  === test_refusal_registry: 480/480 ok ===
$ python -B PKG\scripts\tests\test_judgment_census.py                 ->  === judgment_census: 24/24 ok ===   (census: 279 files scanned, 1142 units; ratchet untouched)
$ python -B PKG\scripts\tests\test_guard_command_text.py              ->  === test_guard_command_text: 197/197 ok ===
$ python -B PKG\scripts\tests\test_resume_stopped.py                  ->  === test_resume_stopped: 123/123 ok ===
$ python -B PKG\scripts\tests\test_s0_close_order.py                  ->  === S0 close order: 29/29 ok ===
$ python -B PKG\scripts\tests\test_whole_identifier.py                ->  === whole identifier and the revoked word: 166/166 ok ===
$ python -B PKG\scripts\tests\test_words_doors.py                     ->  === test_words_doors: 598/598 ok ===
$ python -B PKG\scripts\refusal_registry.py --check                   ->  A24 refusal registry: no violations
$ python -B PKG\scripts\selftest.py --lang                            ->  PASS lang: no cyrillic ... PASS lang: no control byte ...  === qa-factory selftest: 2/2 ok ===
```
Scenario tests (each under `timeout 100`): `test_scenario_local_1_arm_b.py` -> `=== scenario local-1-arm-b: 5/5 ok ===`;
`test_scenario_cart_1.py` and `test_scenario_local_1_0108.py` were cut by the 100 s timeout with no output (not a pass, not a fail:
no verdict; CI judges them, item 8 of section 3).
Byte-identical defaults on the LIVE package (hashes of `json.dumps(sites, sort_keys=True)` before my first edit and after the last):
```
default            n=80    eab4deb23b9f849e4af5d83c4c5867937e17c90d221cfc10a8476eedf198c200   (before == after)
raises_scanned     n=82    ed3eee25e376f00d468d78514db87c5e17f4b792d94fa4ab017371cedcd532fb   (before == after)
census_style       n=1500  e2d0e058b743c7f1e0ec1e5da320d3389e91d81ed7879532d95ed2eab80e9c87   (before == after)
cli --sites --json 14126 bytes c3c168166c35bdb5c4e18628a5bed20a01c0a54bfc643e287d7667491fae6737 (before == after)
cli --sites         8280 bytes 328e36ac45bfe3ac929c2bd7d9ed2f4fd3de868ca5e8c2f91fb8af8a6da7df28 (before == after)
diff before after -> DEFAULTS-IDENTICAL-TO-BEFORE-EDIT
```
Wide scan run: `python -B PKG\scripts\refusal_registry.py --sites --wide --census PKG\scripts\tests\fixtures\judgment-census.json --json` -> rc 0;
totals `{"files_scanned": 279, "sites": 3117, "units": 848, "walk_errors": 0, "check_arg_errors": 0, "walk_error_share": 0.0,
"units_with_row": 732, "units_no_row": 116, "join_share": 0.8632, "role_reachable_units": 170, "conductor_only_units": 562,
"role_reachable_sites": 697, "role_reachable_share": 0.2236}`.

## 6. Test rows added (all in `test_refusal_registry.py`, parts `part_wide_*`, existing style; no new file)
(a) defaults: stored expectation of `sites()` and `sites(raises=raise_family())` on a fixture computed on the unmodified module; no
`transports` key without `wide`. (b) one fixture row per transport of `WIDE_TRANSPORTS` (10) + stderr-without-failing-return and
returns-an-expression as named blind spots + `EXIT_` name / `sys.exit(2)` / `return -1` as sites + list vs `blocking`. (c) 15 state
rows (sourced/tagged/bare, joined/str()-ed list downgrade, `from` alias, module attribute, another module's `refusal` stays bare),
module-constant id, parameter id as walk error. (d) 20 adversarial/blind-spot rows (alias, message from another function,
`print(json.dumps)`+return 2, `sys.stderr.write`, `sys.exit(str)`, `sys.exit(name)`, `SystemExit(str)`, lists under any name, `+= [..]`,
yield, package subclass, stdlib subclass, non-plain base, assignment alias, `raise A`, `raise A()`, factory call, method call, `deny()`,
class only under tests) each "seen" or "named blind spot"; input rows: null byte, 300-deep parens, syntax error, non-UTF-8, empty file,
comments-only, unparsable beside a good file, 4000-term message, 100000-char message, empty scan = zero counts. (e) `--census`: union of
roles of two rows, unit with no row -> `roles` null and counted, join share, role-reachable, no census -> no join totals, absent /
directory / not-JSON / not-a-census / rows-not-a-list -> exit 2 + reason on stderr + empty stdout, `--sites --census` exit 0.

## 7. FR pass (factory-rules sections A-G)
A — refusals: the `--census` failure says what is wrong and exits 2 with the reason (FR-1); no refusal text of the package changed.
B — text shown to a person: not changed (a developer CLI's lines only).
C — contracts: the wide record shape is new output of a dev tool read by the census test only through the unchanged default path (FR-14); no role reads it.
D — identity and evidence: no identifier produced; sourced/tagged/bare is read by binding to `detector_verdict`, not by a text (FR-16).
E — delivery and reporting: not applicable (no report a person reads).
F — measurement: every number carries its command; unknowns (M3 precision, per-check rows) are stated as unknown, not as facts (FR-41, FR-26).
G — code: English only, `selftest.py --lang` green (FR-30); no heredoc code (FR-29); test added to the keep file (FR-28/32); FR-12/13: no phrase list, closed variety (`WIDE_TRANSPORTS`, `RECORD_CALLS`) is a code constant by design C1.
Four questions: (a) cost: none at run time (dev-time scan only); (b) axes: SIBLING_MAP axis 32 (the one scanner) is the same scanner widened;
(c) detector: `test_refusal_registry.py` default-identity rows + census test; (d) skipped? the wide path is entered only by `wide=True`/`--wide`.

## 8. Analogs noticed (not fixed)
- `refusal_registry.sites()` default path still raises `SyntaxError` out of an unparsable file (spec 0.9); only the wide path names it.
- `test_judgment_census.py` blind-spot text and `refusal_registry` docstring each list the blind spots by prose; the wide report's
  `blind_spots` is a third list (AR-22 risk: three carriers of one fact).
- `UNIT_NAME_RE` makes any helper named `*_check` / `check_*` a census unit: a new private helper in a scanned file needs a row.
- `host_adapter` / the A24 `HA-*` entries and `PT-patch-*` re-raise chains (E5) will show as separate units in M1.
