# FV1-21 code critic: is a driver-journal code-move row counted as a sessionless call (task_price `no_call_kinds`)

Tree `C:\QAFactory\forge-repo\.claude\worktrees\fv121`, commit 4921f13 on be2c988. Money diff, so I started with control values and read code only to answer the writer questions.

## Verdict

**Accept with fixes** (`fit_with_fixes`). Nothing blocks: the money behaviour is right on all four DoD rows (control values below). Three fixes for this round, all small, none blocking the merge (F1 errs on the safe side; F2 and F3 are text that is wrong). Two queue lines (Q1, Q2) and one question for the Lead (Q3). Accepting is the Lead's call (rule 6).

## Control values (my own journals built in a temp dir, called `task_price.task_price(root, T)`; rows shaped like the real writers)

| row | journal | got | expected | match |
|---|---|---|---|---|
| (a) | launched + role end row a1 $1 + gate_repair (driver_gates.py:822 shape), a1 cost file present | `agrees`, rows_without_session 0, no "no session id" finding, price 1.0..1.0 | agrees, 0, no finding | yes |
| (b) | (a) + `{"kind":"something_new","session_id":""}` | `incomplete`, 1, finding present | incomplete, counted | yes |
| (c) | plugin root with no references/; delivery + launched + gate_repair | `incomplete`, 1 (gate_repair alone counted) | delivery/launched skipped, gate_repair counted | yes |
| (d) | gate_repair WITH session_id a2, total 0.4, a2 cost file present | `agrees`, 0, sessions [a1, a2], price 1.4 | bound as before | yes |
| (e) | the four unsigned kinds (trace_failed, rows_given_up, stopped_by_person, note), shipped list | `incomplete`, 4 | still counted (unsigned, per spec) | yes |
| (f) | a real role end row with session_id "" | `incomplete`, 1 | counted (money unrecorded) | yes |
| (g) | made-up row: listed kind carrying money + exit_code, no session | skipped (agrees) | no writer writes this shape (see per-kind table) | n/a |

Reader edge probe: `{"no_call_kinds": []}` -> `[]` (**F1**); `["gate_repair"]` -> `['gate_repair']`; `"delivery"` -> fallback `['delivery','launched']`.

## Findings

**F1 (fix this round, does not block; errs on the safe side).** `task_price.py:556` takes an EMPTY list as valid: `isinstance(kinds, list) and all(...)` is true for `[]`, so `_no_call_kinds()` returns `frozenset()`. Then every `delivery`/`launched` row counts again and every driver story reads `incomplete` (the t-363 B2 false mark comes back). The spec says "never an empty list", and so does the function's own docstring (`task_price.py:570` "never to an empty list"). Fix: `if isinstance(kinds, list) and kinds and all(...)`, plus one KIND_CASES row `'{"no_call_kinds": []}'` -> fallback (`incomplete`, 1 with GATE_REPAIR + launched).

**F2 (fix before merge, wrong text in the data the Lead signs from).** `references/driver-journal-kinds.json:6` (`why.gate_repair`) says "no model is called". The changelog (`changelog.d/fv1-21.md:1`) and the `task_price.py` docstring say "a round of code moves". Both are false. Inside a gate_repair round, `review_move` (`driver_gates.py:541-581`) runs `self.rework("S4", role, ...)` at `:578` with role `qa-case-critic` or `qa-case-designer`. That is a paid role dispatch inside the same round whose `record_round` writes the gate_repair rows (`:937`, `:955`, `:964`, `:968`). Skipping the row is still SAFE: the row is a dict literal with no `session_id` or cost (`:822-825`), and the dispatched role writes its own `launched` + end row through `run_claude` (`driver_runner.py:843`, `:901`). If that role's output is not JSON, its own `kind: role` row with `session_id: ""` still counts (control (f)). The wrong part is the stated criterion. "The writer launches no model call" does not hold for gate_repair. The criterion that does hold, and should be written into `why` and the docstring for the Lead to sign by: **the row carries no session and no money of its own, and every model call its writer starts is journalled by its own `run_claude` end row.**

**F3 (fix before merge, the docstring contradicts itself).** `driver_journal.py:9-10` was inserted as "For a resumed session the CLI returns the CUMULATIVE price ... `task_price` is the reader that accounts for it". The next sentence of the same paragraph (`:10-15`) says the figure is NOT the same in every journal: in three measured runs it FALLS, because there it is the cost of one call. The module also calls ITSELF "the one reader" of what a total means (`:1`, `:19`; `driver_runner.py:655`): `root_charged` / `entry_charged` / `total_falls` live here, not in task_price. Suggested wording: "Where a resumed session's totals never fall (cmp1; LR2-1 12.11, session 634b0a20: 0.424 -> 0.455) the figure is the running total of the session, so a naive sum over rows overcounts ($64.34 against $24.32 on LR2-1); price a session through this module (`root_charged` / `entry_charged`), never by summing rows."

**Q1 (queue; axis 6, a second road for "which journal row is a model call").** `experiments/measurers/compare.py:274-284` and `report_run.py:141-158` read `driver-runs.jsonl` straight from the file. They count EVERY row as a call (report_run files `launched`, `gate_repair`, `note`, `trace_failed` ... under "role first work") and add `total_cost_usd` over all rows, which is the naive overcount F3 warns about. The bug predates this diff. It is not in owns, and the builder report says it did not check. Line for «Остатки»: `experiments/measurers compare.py/report_run.py count every driver-journal row as a call and sum cumulative totals: read call kinds and prices through driver_journal (and no_call_kinds) | узел: <the Lead opens it in an untaken live-run-fvf batch>`. When that node is opened, move `_no_call_kinds` into `driver_journal` (the one reader of what a row means, AR-13) so the measurers, retro and task_price share one reader.

**Q2 (queue, duplication that was there before).** The check "is this session id bindable" (`isinstance(sid, str) and sid and REPLACEMENT_CHAR not in sid`) is written out four times: `driver_journal.py:400-401`, `retro_numbers.py:194`, `retro_numbers.py:474`, `task_price.py:580-581`. The diff did not add one. It should become one DJ predicate. Line: `bindable-session predicate repeated 4x -> DJ.bindable(sid) | узел: <Lead>`.

**Q3 (question for the Lead; not verified).** `stopped_by_person.cut` names `launched` rows that never got an end row: calls the person cut off. They are already skipped by the shipped list (t-363 B2), so their money is neither bound nor flagged by `task_price`, unless cost capture binds the transcript some other way. This diff does not change that. If it matters, it is a separate node, not grounds to keep `stopped_by_person` counted: one counted row per stop says nothing about how many calls were cut. Estimate, not verified.

## Per-kind verdict (the Lead's question)

Complete list of writers: `driver-runs.jsonl` has one writer, `driver_runner.py:402-404 journal_run`. Positive control: the grep finds the known `launched` writer at `:843`, and no other append targets the file. Every `journal_run` call passes a literal dict. The ONLY row that carries `session_id`/`total_cost_usd` is the `run_claude` end row (`driver_runner.py:901`), and its `kind` is the call kind. Every caller passes the literal `"role"` or `"conductor"`: `driver_conductor.py:336`, `driver_stage_s8s9.py:447`, `driver_dispatch.py:546/575/706/1035/2078`, `driver_machine.py:546`. The audit A27 I-one refuses a non-literal kind (`test_audit_rules.py:1295`). So no listed or proposed kind name can ever label a paid row. The only process launcher of a model in the package is `driver_runner._launch` (`:692`). A grep for Popen/subprocess.run with claude/codex/cmd found no other model launch.

| kind | writer file:line | what the writer does | money behind it? | verdict |
|---|---|---|---|---|
| `trace_failed` | `driver_runner.py:247` (owed_rows state not a list, no script run); `:297` (`py_trace`: a factory script exited non-zero, callers run only `stage_done.py`, `log_append.py`, `factory_dashboard.py`, `estimate_record.py`; none starts a process, grep for subprocess/Popen/claude finds nothing); `:1235` (`file_defect`: `log_append.py` refused); `driver_conductor.py:147` (an unreadable owed row set aside, no script run) | records that a deterministic script failed | none: the literal has no session/cost, and no road from these writers reaches `run_claude` | **may be signed** |
| `rows_given_up` | `driver_conductor.py:160` | bookkeeping: owed journal rows given up on the person's word | none | **may be signed** |
| `stopped_by_person` | `driver_machine.py:1799` (docstring `:1787-1790` says it has no session/cost/exit_code) | Ctrl-C record listing the cut `launched` calls | none of its own (see Q3 for the cut calls) | **may be signed** |
| `note` | `driver_runner.py:647` (`host_note`, called from inside `run_claude` at `:851`, `:868`) | a host fact written during a call | none: the call's money is on its own `:901` end row, which counts if it has no session | **may be signed** |
| `gate_repair` | `driver_gates.py:822` (`record_round`) | round bookkeeping; the round may dispatch qa-case-critic/designer (`:578`) | none of its own; dispatched roles journal their own rows | **safe as shipped; the `why` wording is wrong (F2)** |

On `trace_failed`, which the Lead doubts: none of its four writers can stand for a paid call. Counting it does not detect hidden money either, because a script that called a model outside `run_claude` would be invisible whether or not it failed. The decision to sign stays with the Lead.

## Standing questions

1. **Fit to the spec**: matches except F1. The list is data, the fallback covers absent / unreadable / not-an-object / key absent / non-string items, kind absent or not a string still counts, a gate_repair row with a session id binds as before, and the driver_journal sentence is there (F3 is about what it says).
2. **Builder's own decisions**: a sibling `why` object (safe; nothing reads it, it is documentation, see F2); the `isinstance(dict)` guard over `load_ref_json` (needed: that reader returns any parsed value); registering the file in features.json F14 (correct). Proposed kinds were reported and not added, as the spec says.
3. **Seams**: additive. task_price output shape unchanged; `retro_numbers.py:1194` and `factory_dashboard.py:2354` still read `rows_without_session` the same way.
4. **Class-wide completeness**: inside the artifact, the writer list is complete (table above). Axis 6 is not covered: Q1 is unfixed and was not queued. Axis 16 (one JSON reader) is covered: it reuses `hooklib.load_ref_json` (`hooklib.py:831`). Axis 29 n/a (no writer). Axis 34 n/a.
5. **Tests**: row (a) of KIND_CASES catches the defect the node exists for, through `task_price` on a disk journal (the door the progress line uses); (c) swaps `hooklib.PLUGIN_ROOT`, the real lookup path. It is one parameterised table, the right form. There are more test lines (55) than product lines (24 + 8 json), but the extra rows are the spec's own named edges. Missing: the empty-list row (F1). No test-layer rows touched.
6. **DUPLICATION AND CONSISTENCY**: no new reader or helper copy. It reuses `hooklib.load_ref_json` (`hooklib.py:831`), `DJ._journal_paths`, `DJ.read_rows`. Repeats that were there before: Q2 (session predicate, 4 places), Q1 (measurers' own row reading). Grep shapes: `rows_without_session|"delivery", "launched"|kind.{0,20}(delivery|launched|gate_repair)` (-i, *.py, whole tree; positive control: it found `task_price.py:548`) and `session_id|without_session|sessionless|no session` (-i) over `retro_numbers.py`.
7. **CODE QUALITY**: new functions are 8 and 25 lines, nesting 2. No dead branches. One annotation is wrong: the docstring "never to an empty list" (F1), and the `why`/docstring "no model is called" (F2). Severity: fix before merge.
8. **Hygiene**: FR-30, all new text is English (read in full; builder's `selftest --lang` 2/2). CRLF consistent in every touched file (`grep -c $'\r'` equals the line count: task_price 1233/1233, driver_journal 419/419, json 8/8). No control bytes.
9. **IN-TREE RATCHETS**: none touched. The diff stat names no baseline, census, role-load or dup-baseline file.
10. **ARCHITECTURE**: AR-1 named and kept (the hardcoded tuple became a data row, and the fallback constant is the only code copy). AR-28 named and kept (an unlisted kind counts; control (b)). AR-13 touched, not named, and not broken: there is one reader of the new file. Still, "what a journal row means" belongs to `driver_journal` (`:1`), so put the reader there when Q1 opens. AR-22: the new file has its reader. Both ways checked.
11. **JUDGMENT**: none. A shape check on `kind` and session-id presence; no census row added; `judgment: none` holds.
12. **ONE ROAD**: none found. I read the whole diff for a branch on a language, host, runner or project name: there is none (the `codex` mentions are in code the diff does not touch). The kinds list is one data row read the same way for every host.

## Trail

- Read: diff `git -C <tree> show 4921f13` (all 7 files); `task_price.py:546-585`; `driver_journal.py:1-32`, `:400-401`; `driver_runner.py:225-419`, `:620-919`, `:1215-1237`; `driver_gates.py:502-600`, `:740-992`; `driver_conductor.py:125-169`; `driver_machine.py:1780-1804`; `driver_s0.py:398-414`; `hooklib.py:831-838`; `retro_numbers.py:180-219`, `:458-477`, `:1690-1719`; `experiments/measurers/compare.py:265-289`, `report_run.py:140-158`; the finding; the builder report; `docs/SIBLING_MAP.md` axis 6 and the axis list; `docs/tasks/critic-diff-brief.md`.
- Greps: `"kind"|kind=|journal_run\(` over `driver_*.py` (writer list); `run_claude\(` over scripts (call kinds); `py_trace\(` (script list); subprocess/Popen with claude|codex|cmd (-i) over scripts (only `driver_runner.py:692` launches a model); `driver-runs.jsonl|JOURNAL_NAME` writers (only `driver_runner.py:404`); measurers `driver-runs|JOURNAL_NAME|"kind"|session_id`.
- Rerun: `( cd <tree>/ai-packages/qa-factory && python -B scripts/tests/test_task_price.py )` -> `=== task_price: 321/321 ok ===` (matches the builder's tail).
- Control values: a stdin python payload that builds the journals and cost files in a temp dir and calls `TP.task_price`; output in the table above, verbatim numbers. A second payload probed `_no_call_kinds()` on `[]`, `["gate_repair"]`, `"delivery"`.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "F1 task_price.py:556 - an empty no_call_kinds list is taken as valid and yields frozenset(); spec and docstring (:570) say never empty; add `kinds and` and a KIND_CASES row for []. Safe direction, does not block.",
    "F2 references/driver-journal-kinds.json:6, changelog.d/fv1-21.md:1, task_price.py docstring - 'no model is called' is false: review_move (driver_gates.py:541-581, rework at :578) dispatches qa-case-critic/designer inside a gate_repair round; restate the criterion as 'the row carries no session or money of its own; every call its writer starts is journalled by its own run_claude end row (driver_runner.py:901)'. Fix before merge.",
    "F3 driver_journal.py:9-10 - the new sentence says total_cost_usd of a resumed session is CUMULATIVE categorically and names task_price as its reader; the next sentence says it falls (per-call) in three measured runs, and driver_journal is the one reader of totals. Reword as conditional on non-falling totals, pointing at root_charged/entry_charged. Fix before merge."
  ],
  "class_completeness": "Writer list complete: driver-runs.jsonl has one writer (driver_runner.py:404); the only paid row is run_claude's end row (:901) whose kind is the literal role/conductor. All four proposed kinds (trace_failed, rows_given_up, stopped_by_person, note) carry no money and may be signed; gate_repair is safe but its why text is wrong (F2). Axis 6 NOT covered and not queued: experiments/measurers compare.py:274-284 and report_run.py:141-158 count every row as a call and sum cumulative totals (Q1, a node for the Lead). Duplication from before: bindable-session predicate 4x (driver_journal.py:400, retro_numbers.py:194, :474, task_price.py:580) (Q2). Axis 16 covered by reuse of hooklib.load_ref_json.",
  "trail": {
    "read": [
      "git show 4921f13 (all files)",
      "ai-packages/qa-factory/scripts/task_price.py:546-585",
      "ai-packages/qa-factory/scripts/driver_journal.py:1-32,400-401",
      "ai-packages/qa-factory/scripts/driver_runner.py:225-419,620-919,1215-1237",
      "ai-packages/qa-factory/scripts/driver_gates.py:502-600,740-992",
      "ai-packages/qa-factory/scripts/driver_conductor.py:125-169",
      "ai-packages/qa-factory/scripts/driver_machine.py:1780-1804",
      "ai-packages/qa-factory/scripts/hooklib.py:831-838",
      "ai-packages/qa-factory/scripts/retro_numbers.py:180-219,458-477,1690-1719",
      "experiments/measurers/compare.py:265-289",
      "experiments/measurers/report_run.py:140-158",
      "plans/piles/live-run-fvf/findings/20261112-cena-lozhno-nepolnaya-iz-za-shagov-koda.md",
      "docs/tasks/specs/reports/20261113-fv1-21-report.md",
      "docs/SIBLING_MAP.md axis 6",
      "docs/tasks/critic-diff-brief.md"
    ],
    "reruns": [
      {"command": "( cd <tree>/ai-packages/qa-factory && python -B scripts/tests/test_task_price.py )", "result": "=== task_price: 321/321 ok ==="},
      {"command": "stdin python control payload: task_price over temp journals (a)-(g)", "result": "(a) agrees 0 no-finding 1.0; (b) incomplete 1; (c) incomplete 1; (d) agrees 0 sessions [a1,a2] 1.4; (e) incomplete 4; (f) incomplete 1; (g) agrees 0"},
      {"command": "stdin python probe: _no_call_kinds() on [] / [gate_repair] / \"delivery\"", "result": "[] -> []; ['gate_repair']; fallback ['delivery','launched']"}
    ]
  }
}
```
