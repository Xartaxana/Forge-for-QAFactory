# t-1483 -- critic review of CD2-1 (diff origin/main...d003cfdb, branch worktree-agent-abf9b5edd8ecc8514)

Verdict: **NEEDS WORK** -- 1 blocking finding (F1, failure_class: spec), 2 fix-before-merge (F2, F3), remarks R1-R3.
The decision to accept belongs to the coordinator (rule 6).

## Findings

**F1 (blocks) -- the node builds a second list of service kinds, and it disagrees with the one the factory already has.**
`experiments/measurers/journal_kinds.py:11`:
`SERVICE_KINDS = frozenset({"window_round", "process", "launched", "gate_repair", "held"})`.
The package already keeps this list as data: `ai-packages/qa-factory/references/driver-journal-kinds.json` `no_call_kinds` =
`delivery, launched, gate_repair, trace_failed, rows_given_up, stopped_by_person, note, window_round, process, repeat_stop`. Each kind
has a `why` there, and the package reads it through `task_price.py::_no_call_kinds` (task_price.py:551-558). Its `window_round` and
`process` rows came in with commit e7dee9e5, "CL4-1 N1: ... its price rows (window_round, process)". That is the place finding item 1
names: "перечень служебных видов -- один ... рядом с прайс-строкой вида из CL4-1 N1". The handoff says "no existing per-kind price row
in the measurers (grep found none)". That is true only of `experiments/measurers/`. The dispatch edge also said "in the measurers",
so this is a dispatcher defect that the builder carried out to the letter. It is still the opposite of what the finding asks for:
the repository now holds two lists (P18, AR-1, Q6, Q12).
- The new list misses six kinds that the driver writes today. They are still counted as calls in `by_kind` / `by_role` and in
  `report_run`'s buckets, so the node's own defect stays open for these kinds. The writers: `delivery` (driver_stage_s8s9.py:377,
  driver_machine.py:3681), `note` (driver_runner.py:683), `trace_failed` (driver_runner.py:247, :302; driver_conductor.py:147),
  `rows_given_up` (driver_conductor.py:160), `stopped_by_person` (driver_machine.py:1860), `repeat_stop` (driver_runner.py:442).
- The new list adds `held`. No writer in the repository makes it: `"kind": "held"`, case-insensitive, over `ai-packages experiments
  tools` gives 0 hits, while the control `"kind": "gate_repair"` with the same search shape gives 8. The batch plan's CD2-1 row and the
  finding do not have it either. It is a member with no carrier: harmless today, wrong as data.
- Failing scenario (probe, verbatim output below). A journal with one `role` call (with a session and $1.00) plus one `delivery`, one
  `note` and one `trace_failed` row gives `by_kind: {'role': 1, 'delivery': 1, 'note': 1, 'trace_failed': 1} bookkeeping: 0` in
  `compare.driver_report`, and `{'role first work': {'calls': 4, ...}}, 0` in `report_run.journal_from`. Expected: calls 1,
  bookkeeping 3. Every current driver run ends with a `delivery` row, so every new report over-counts calls by at least one.
- Fix (inside this node; no package file is written): `journal_kinds.py` reads `no_call_kinds` from
  `paths.PACKAGE / "references" / "driver-journal-kinds.json`. The measurers already read package data this way: `compare.RATES =
  paths.RATES`, which is under `PACKAGE/references`. Delete the hard-coded list and `held`. Two edges are for the Lead, not for the
  builder to guess: what happens when the file is absent or unreadable (mirror task_price's fallback `delivery, launched`, or print a
  refusal line -- never an empty set, FR-41), and whether the test table reads its service kinds from the same file instead of
  `JK_SERVICE`. Empirical basis (rule 13): in the two distinct real journals on disk, `launched` (120 rows) and `gate_repair` (3 rows)
  carry 0 sessions and 0 cost, and `role` / `conductor` carry both. This matches the JSON's `why` texts. Those journals predate the
  newer kinds, so the six missing kinds are attested by their writers' source, not by data.

**F2 (fix before merge) -- `report_run.journal` is dead code.**
`report_run.py:142-144`: `journal()` is kept "for its signature", but `main` now calls `journal_from` (report_run.py:220). A search for
`journal(` / `report_run.journal` over `experiments tools` finds only the definition and a docstring mention in `journal_kinds.py:3`.
The same search shape finds the known caller `report_to_gate.py:67` of `report_run.session_roles`. Delete `journal()` and point the
`journal_kinds.py` docstring at `journal_from`, or have `main` call it. Today it is a second entry point that nobody reads (Q7).

**F3 (fix before merge, small) -- the printed `bookkeeping rows: N` line has no row at its door.**
The dispatch edge "every report prints a line bookkeeping rows: N, also when N is 0" is CLI output: compare.py:360 and
report_run.py:230. So is the accepted deviation (a present but empty journal now prints the table header plus `bookkeeping rows: 0`).
The table asserts `driver_report()["bookkeeping_rows"]` and `journal_from()`, but neither printed line (Q5c). Add one row: the
empty-journal case through `report_run.main`'s journal block or `compare.main`, asserting the line text. If driving `main` costs too
much in this file, the Lead can waive this in writing.

## Deviations (as asked)

- `journal_from` added beside `journal`: the split itself is sound. `None` (no file) and `({}, 0)` (empty file) keep "absent" apart
  from "empty", which the dispatch's empty-journal edge needs. The leftover `journal()` is F2.
- A present empty journal now prints its header and `bookkeeping rows: 0`: this is consistent with the dispatch edge ("also when N is
  0"). Traced: `total = ... or 1` (report_run.py:225) avoids division by zero, and `table([])` prints the header and separator only. An
  absent file still prints nothing, as before. Acceptable; its missing test row is F3.

## Same class: report_run.py::session_roles (remark R1 -- harmless)

`session_roles` (report_run.py:45-61) maps `session_id -> role` only for rows with a truthy `session_id` (line 58). No service-kind
writer sets one. Checked: process_start_row / process_end_row (driver_journal.py:552-592) state they have NO session_id, and the
window_round (driver_machine.py:395-432), gate_repair (driver_gates.py:840-850) and launched (driver_runner.py:920-932) records have no
`session` field. Real data: with_session = 0 for launched and gate_repair. The function makes a label map, not a count. The counts in
`money()` come from transcripts, and an unlabelled session is skipped there with a note. So the function inflates no call or role
count. If a future service row carried a session, it would relabel that session, not count it twice. No fix in this node.

## Seam and class notes

- R2: AR-13 -- `collect_stall.py:27` says `driver_journal` calls itself the one reader of driver-runs.jsonl. The measurers in
  `experiments/` have always parsed the file directly. This is not new in this diff and is outside the node; named only.
- Class completeness: compare.driver_report and report_run.journal are the two readers the finding names, and both go through
  `split_rows`. The other measurers are listed by the finding as already filtering, and they are a non-goal. The axis of the defect that
  remains open is the list's content (F1), not a reader.
- Siblings: batch 1's true-price rows read the same journals through `task_price._no_call_kinds`, the list F1 says to reuse. That
  reuse is what keeps the two cost views agreeing.

## Standing questions

- Q1 fit: items 2 and 3 of the finding are met. Item 1 is not ("one list", F1). The edges are met: exact-case match, non-ASCII,
  absent / empty / unknown / non-string kind stays a call, non-JSON line skipped in both readers as before, empty journal 0/0, 10000
  service rows.
- Q2 builder's decisions: `is_service` requires `dict` and `str` kind, which errs safe (an unknown becomes a call). Non-dict JSON still
  crashes later, as before; the handoff states this.
- Q3 seams: additive. The `--json` output gains `bookkeeping_rows`. No reader of `quality.driver` was found in experiments/tools
  (`by_kind|["driver"]|bookkeeping` grep).
- Q4: F1.
- Q5 tests: (a) killing power yes -- reverting `split_rows` in either reader fails the "call plus four" row. (b) The values trace to
  the DoD rows. (c) F3. (d) No test rewritten. (e) No duplicate: there was no earlier `driver_report` test. (f) Volume: 35 test lines
  against about 50 product lines added; within budget. (g) No new file.
- DUPLICATION AND CONSISTENCY (Q6): F1. A second list duplicates `references/driver-journal-kinds.json::no_call_kinds`, which is read
  at `task_price.py:551-558`.
- CODE QUALITY (Q7): F2 (dead `journal()`). New functions are short, with nesting of 2 or less. No copy-paste: the two readers share
  `split_rows`.
- Q8: not a package diff. Q9: no in-tree ratchet row touched. The forge-check job result was not attached and not re-run (rule 21).
- Q10: AR-1 (one list) is broken by F1; AR-13 remark R2. VARIETY: n/a. This is a forge-side measurer, it runs on no project's stage,
  and no unknown value is blocked or defaulted (an unknown kind counts as a call).
- Q11 judgment: none -- a data list, with no classification of a role's output.
- ONE ROAD (Q12): F1 is a second road for the same action ("is this journal row a call"). The package and the measurers would answer
  differently for six kinds. A fix in this round.

## Spot-checks

- Witness "314 passed": reproduced, `314 passed in 8.41s` at HEAD d003cfdb, clean tree.
- "no existing per-kind price row": not reproduced repo-wide. It holds only inside experiments/measurers (F1).
- "held" has a writer: 0 hits, control 8 hits (F1).
- `journal()` has callers: 0 besides its definition; control `report_run.session_roles` has 1 hit (F2).

## Trail

- Read: d-1482.txt; handoff t-1482-cd2-1.md; the finding; batch-2 plan rows 16 and 26; diff origin/main...d003cfdb (5 files);
  report_run.py:40-100, 142-162, 165-171, 217-231; compare.py:304-360; task_price.py:530-600; driver-journal-kinds.json (whole);
  driver_journal.py def index and 552-592; driver_runner.py:920-932, 975-990; driver_machine.py:395-432, 1795-1811;
  driver_gates.py:840-850; journal_run writer list (grep).
- `python -m pytest <wt>/experiments/measurers/test_measurers.py -q -p no:cacheprovider` -> `314 passed in 8.41s`.
- Probe `scratchpad/probe.py` (role + delivery + note + trace_failed) -> `by_kind: {'role': 1, 'delivery': 1, 'note': 1,
  'trace_failed': 1} bookkeeping: 0`; `report_run: ({'role first work': {'calls': 4, 'cost': 1.0, 'turns': 0, 'seconds': 0}}, 0)`.
- Kind census `scratchpad/kinds.py` over the 2 distinct real journals (forge-repo experiments/mybooks factory-out; mybooks-stand
  LOCAL-1), each: launched 120 / 0 session / 0 cost; role 81 / 81 / 81; conductor 39 / 39 / 39; gate_repair 3 / 0 / 0.
- grep `"kind": *"held"` -i -> 0; control `"kind": *"gate_repair"` -i -> 8.

```json
{
  "verdict": "blocker",
  "blockers": [
    "F1: experiments/measurers/journal_kinds.py:11 builds a second service-kind list instead of reading ai-packages/qa-factory/references/driver-journal-kinds.json no_call_kinds (the CL4-1 N1 price row the finding names); it misses delivery, note, trace_failed, rows_given_up, stopped_by_person, repeat_stop (still counted as calls: probe gives 4 calls / 0 bookkeeping for 1 call + 3 service rows) and adds held, which no writer produces"
  ],
  "fixes": [
    "F1 (blocks): journal_kinds.py reads no_call_kinds from paths.PACKAGE/references/driver-journal-kinds.json; drop the literal list and held; Lead states the absent/unreadable-file edge",
    "F2 (fix before merge): delete dead report_run.journal (report_run.py:142-144) or route main through it; fix journal_kinds.py:3 docstring",
    "F3 (fix before merge): one row asserting the printed bookkeeping rows line (empty journal) at the CLI door, or a written Lead waiver"
  ],
  "class_completeness": "Both readers named by the finding go through split_rows; the open axis is the list content (F1), not a reader. session_roles is harmless: it keys only on session_id and no service writer sets one (remark R1).",
  "trail": {
    "read": [
      "d-1482.txt",
      "docs/tasks/handoffs/t-1482-cd2-1.md",
      "plans/piles/cost-dashboard/findings/20261114-driver-report-schitaet-sluzhebnye-stroki-zhurnala-vyzovami.md",
      "experiments/measurers/journal_kinds.py",
      "experiments/measurers/compare.py:304-360",
      "experiments/measurers/report_run.py:40-231",
      "experiments/measurers/test_measurers.py:3475-3508",
      "ai-packages/qa-factory/references/driver-journal-kinds.json",
      "ai-packages/qa-factory/scripts/task_price.py:530-600",
      "ai-packages/qa-factory/scripts/driver_runner.py:920-990"
    ],
    "reruns": [
      {"command": "python -m pytest <worktree>/experiments/measurers/test_measurers.py -q", "result": "314 passed in 8.41s"},
      {"command": "python -B scratchpad/probe.py <worktree>/experiments/measurers", "result": "by_kind role 1, delivery 1, note 1, trace_failed 1; bookkeeping 0; report_run calls 4"}
    ]
  }
}
```
