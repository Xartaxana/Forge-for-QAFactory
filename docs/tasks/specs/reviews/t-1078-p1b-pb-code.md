# t-1078 — code critic of P-b (builder t-1076, commit 61595eec)

Tree: `C:/QAFactory/forge-repo/.claude/worktrees/agent-a3398935dd81f7c74`, branch `worktree-agent-a3398935dd81f7c74`, based on
`9344a58c` (origin/main with P-a merged). Spec: card `docs/tasks/specs/20261117-p1b-pb-runtime-provenance-card.md`, read
binding section first, then Lead fork decisions, §3, §4, §1. Plan verdict t-1075.

**Verdict: accept with fixes — 0 BLOCKING, 2 FIX (both small enough for a fix round of the same node), 7 NOTE.**
The decision to accept is the coordinator's (rule 6).

## Findings

### FIX-1 — J6 reads `runtime_required` more strictly than run_suite, which decides whether a reading is taken (key 3)

`ai-packages/qa-factory/scripts/handoff_check.py:631`:
`if done and all(job["request"].get("runtime_required") is False for job in done):`

run_suite decides whether to take the launch reading by truthiness: `if request.get("runtime_required", True):`
(`run_suite.py:2904`, also `:2350`), and `validate_request` reads it the same way (`execution_request.py:151,187`). It never
checks that the value is a bool (no "runtime_required must ..." refusal anywhere in `execution_request.py`). So a request with
`runtime_required: null` or `0` passes validation, runs with no stand, and gets no `runtime_probe_before`. The deriver then
gives J3b, which names `probe_by_code.py` as the door. Running that probe again gives the same J3b, so the door cannot close
the blank (FR-2, AR-9). The blank itself is still on the safe side (never a pass), which is why this does not block.

Probe I ran (scratchpad `probe_j6.py`: one completed own `red_probe` job with no reading, `runtime_required` set as shown):
```
False -> J6 | door: False
None -> J3b | door: True
0 -> J3b | door: True
'MISSING' -> J3b | door: True
True -> J3b | door: True
```
The absent-key case is right: it is read as required, which is run_suite's own default. False is right too. Only falsy
values that are not the bool False come out wrong.
Correction: `not job["request"].get("runtime_required", True)` at :631, plus one row next to E22 (`test_handoff.py:584`) with
`required=None`, expecting J6 and no door. The expected value comes from run_suite:2904, not from the deriver.
(Inside `execution_request.py` itself both readings exist: `is False` at :164/:169/:2850, truthy at :187/:387. That split
predates this diff. The rule that matters for "was a reading taken" is run_suite:2904.)

### FIX-2 — F-6 wording was not applied to the probe producer text or to the changelog (key 1, F-6)

`handoff_check.py:521-523` `_PROBE_RECORD_PRODUCER` = "the record is the stand reading run_suite takes when it launches this
review's own probe ...". The changelog fragment `changelog.d/p1b-pb-probe-run-record.md:1` says the same thing ("filled ... from
the stand reading run_suite takes when it launches"). Binding F-6 requires "the record the launch reading cites" "everywhere
(§4.1, E8, docstrings, reasons)". The producer text is the tail of every probe-road reason, J1–J5. Saying "the record IS the
reading taken at launch" is the exact conflation F-6 removes (a project's probe may cite one file for every launch). The
docstrings got it right (:556, :602, :660). Item 2 fixed the text verbatim before F-6 existed, and the binding section
overrides it.
Correction: e.g. "the record is the file the stand reading cites, which run_suite takes when it launches this review's own
probe: ..."; in the changelog, "from the record cited by the stand reading run_suite takes when it launches ...". Text only. No
row asserts these words: the table asserts only `probe_by_code.py`, which stays.

### NOTE-1 — J3b's count and newest status are produced but no row pins them (F-3)
`handoff_check.py:634-636` prints `{len(red)} red_probe run(s) ... newest job <id>: status <s>`. P8/P9
(`test_handoff.py:500,505`) assert only the clause "none completed with a stand reading". A regression that dropped the count
would pass. Brief 5(f) says a pin on text is not a finding, so this is optional. If wanted: one P8 row asserts
`"1 red_probe run(s)"` and `f"status {status}"`.

### NOTE-2 — duplication inside the diff (q6/q7), spec-prescribed
`_probe_run_record` :638-650 (newest → `evidence_refs[0]` → blank check → strip → `_story_record` → J4/J5/source) repeats
`window_runtime_record` :585-598 step for step. Only the reason wording differs. `_probe_runtime_provenance` :659-663 repeats
`_runtime_provenance` :653-656 apart from one keyword. Both shapes are prescribed verbatim by card items 3-4, and merging them
would touch the run-block reasons, which must stay byte-identical (C5). Severity: queue. The natural home is the F-5 node "one
road for the three provenance fields". When that node unifies the source, the newest→ref→story tail becomes one helper.

### NOTE-3 — row E23 asserts what P6 asserts, through the same door (brief 5(e)), but the binding asked for it
E23 (`test_handoff.py:590-594`: only another dispatch's job → J3a, substring "belongs to another dispatch") and P6 (:466-471:
other dispatches' jobs → J3a) take the same input class and give the same outcome. Binding F-2 explicitly asks for "a test
row", so this is no finding against the builder. It could be folded into P6 by adding the clause to P6's `said`.

### NOTE-4 — E14 has no row: acceptable
The card makes it optional (§4 E14). The `except Exception` at :613-615 covers the import, the glob and `jobs()`, and `jobs()`
already skips OSError/ValueError per file, which J2 then counts. Nothing reachable from outside is left untested.

### NOTE-5 — P21's "today's text" is partly self-referential, but the row still has killing power
`test_handoff.py:607-609` compares `_runtime_provenance`'s reason with `window_runtime_record(task, A)[1]`, i.e. the code with
itself. The row would still fail if the automator's field took the probe road: it asserts `runtime_probe.py` is present and
`probe_by_code.py` is absent, and the reasons differ. Byte-identity with the pre-change text rests on reading the diff. I traced
it: the not-own text at :580-583 is unchanged, and `producer` is `_RECORD_PRODUCER` when `probe_run` is False (:560). It holds.

### NOTE-6 — sibling carriers are not on main yet (class completeness; proposed nodes, owner: Lead)
On `origin/main`, `git grep -il -e "artifacts.probes" -e "runtime_probe_before" -- plans/piles docs/tasks/lead-queue.md`
returns nothing. A positive control of the same form with `runtime_provenance` finds pile files. So the three carriers the
card, the binding and the report name exist only in the card and the report:
(a) F-5, the run-block twin (`live-run-fvf` finding, axis 5), which the binding says is "queued";
(b) the card §7 scout question (`artifacts.probes` on s5-automator-to-critic first, then the other "scout" DERIVERS entries:
`run.witness`, `review.rollcall`, `run.*`, `delivery.*`, `scope[].case_version`, `grounding.*`);
(c) wiring the reserved null outcome `no_runtime_record` (`null-outcomes.json:178`) as the eventual home of J6/J3.
Proposed: the Lead files (a)-(c) as findings in `live-run-fvf` in the same move as accepting this work. Filing is the
coordinator's step, not the builder's, so this does not block this diff.

### NOTE-7 — a resumed critic dispatch gets a blank (safe side, inherited)
If a critic dispatch is resumed under a new id (`execution_request.find_active_dispatch` :939 "resumed as"), its earlier probe
job carries the old id, and the form's dispatch gives J3a. The run-block road behaves the same way. This is the permitted
direction of error (blank, never a foreign record). Recorded only.

## Acceptance keys

1. **Fixes and notes of t-1075 taken by the binding section**
   - F-1 (J6, no door): done, `handoff_check.py:629-633`. J6 carries no `{producer}`. Row E22 at `test_handoff.py:582-584`
     asserts no door through `no_door` (:452, :597-601). E22b (:585-588): mixed → J3b. The reading needs a fix (FIX-1).
   - F-2 (E23 blank + J3a): done. J3a text at :622-626 matches the binding word for word. Row at `test_handoff.py:590-594`.
   - F-3 (J3a/J3b split, count and newest status): done at :622-626 / :629-636. `last = red[-1]` is the newest of all own
     red_probe jobs in `JobStore.jobs()` order. Rows P8×4 and P9×4 assert J3b (count/status not pinned, NOTE-1).
   - F-6 (wording): docstrings done (:556, :602, :660). Producer constant and changelog not done (FIX-2).
   - N-1 (import): done. `from pathlib import PurePosixPath` is at :529 inside `_story_record`, gone from
     `window_runtime_record`.
   - N-3: done (docstring :607-608).
   - N-4 (constructor): done. Tests use `H.Artifacts(task, dispatch=...)` (`test_handoff.py:445, :649`), the signature
     `__init__(self, root, dispatch="")` that origin/main has after P-a (handoff_check.py:77 in both).
   - N-5 (membership): done, P11 at `test_handoff.py:514-518` asserts membership in `{a, b}`.
2. **Semantics**
   - Positional invariant holds: no dispatch (:561-563) and unreadable blocks (:564-571) return before the job store. An own
     block with a record returns its path or named reason (:585-598) without reaching `_probe_run_record`. The probe branch
     only replaces the `if not own` return (:579-584).
   - The job filter matches all of these on the SAME job (rule 15 scoping): dispatch id (stripped, exact), purpose
     `red_probe`, status `completed`, a non-empty dict `runtime_probe_before` (:620-628).
   - Unreadable job files: glob count minus `jobs()` count gives J2 blank (:611-619). A concurrent `begin` (O_EXCL, then the
     write) also gives a blank, never a pass.
   - Callers: `window_runtime_record` / `_runtime_provenance` are called only inside `handoff_check.py` (Grep over the
     package without tests: def + 3 call sites). `probes.runtime_provenance` exists only on `s5-critic-to-automator.yaml:53-56`.
     The automator's `artifacts.probes` (s5-automator-to-critic.yaml:64) is a different key. The automator and runner keys
     stay bound to `_runtime_provenance` (:722, :729).
   - Empirics on real data (rule 13): in the kept dry world, the critic job `44bcd10c384267c69a56` (file `230891e480ca...`,
     red_probe, completed, `runtime_required: True` present) has `runtime_probe_before` → `...075258Z.json`. The automator's
     initial job → `...075205Z.json`. The deriver answers 075258Z, the same as the report's witness.
3. **J6 judgment call:** an absent key read as required is correct (run_suite:2904/:2350 default True). False is correct.
   A falsy non-bool diverges from run_suite (FIX-1, probe above).
4. **Tests**
   - Expected values come from the card or the test's own input: file names the test writes, J-texts from the binding,
     "no evidence_refs" / "not a file of this story" / "names no dispatch" from §3 J4/J5/E1.
   - No row can only pass. The negative control in the report turned P1, P10, P11 and the reason rows red, quoted with
     sha256-identical restore.
   - E14 without a row is fine (NOTE-4). E23 duplicates P6 (NOTE-3).
   - Volume: +236 test lines against +106 net product lines. `tests-over: rows per edge of the deriver` is in the commit and
     the report, and the reason holds: the card fixes one row per edge P1–P21 + E22/E23.
5. **One reader:** the tail rule `parts[::-1].index(root.name)` occurs once (:535). Grep across `scripts/` for
   "tail after the last" and `[::-1].index(` (case-insensitive) finds only :527/:534/:535 plus unrelated test prose.
   - Census: the new names `_story_record`, `_probe_run_record`, `_probe_runtime_provenance` do not match `UNIT_NAME_RE`
     (`test_judgment_census.py:77`). No `refusal(` is added. The census run is green per the report.
6. **Class completeness:** within `DERIVERS`, the existence class is covered by card §7's sweep and its scout question. The
   source-semantics class is F-5. Neither carrier is on main yet (NOTE-6, proposed nodes).
   - Map walk:
     - axis 5 (stage twins): F-5, queued by the binding.
     - axis 16 (one JSON reader): the jobs are read through `JobStore.jobs()`, no new reader.
     - axis 24 (record of an execution): not touched.
     - axis 33 (which dispatch): uses `_form_dispatch` (P-a).
     - axis 34 (one road): see below.
     - axis 38 (dry census): `known_red` is relabelled by the coordinator per F-4, not by the builder.
     - The other axes do not apply (forge/tooling axes 1-4, 6-15, 17-23, 25-32, 35-37: no file of theirs is touched).
7. **Duplication and code quality**
   - DUPLICATION AND CONSISTENCY: two in-diff clones, spec-prescribed and queued to F-5 (NOTE-2). No new reader, path
     resolver or refusal builder: the jobs go through `JobStore.jobs()` and the story path through `_story_record` /
     `_story_relative`. Grepped: `tail after the last`, `[::-1].index(`, `window_runtime_record|_story_record|PurePosixPath`
     over the package.
   - CODE QUALITY: `_probe_run_record` is :601-650, 50 lines, at most 2 nesting levels. There are no dead branches.
     `max(0, files - len(jobs))` guards the case where a file is created between the glob and `jobs()`. The one name or text
     that says the wrong thing is the producer text (FIX-2).

## Other standing questions

- ONE ROAD (q12): none found. The probe road is a branch inside the one reader for a field whose contract meaning differs
  ("this review's own probe run"), which is an ordinary condition of the task, not a language/project/case exclusion. The
  automator and runner keep the shared road. Grepped `DERIVERS` and the two S5 handoff forms.
- RATCHETS (q9): none touched. The commit stat shows 4 files, with no known_red, census or role-load file.
- ARCHITECTURE (q10): AR-22, AR-13 and AR-28 are named in the commit and kept: a producer for the field the critic reads;
  one tail rule; an unknown leads to a named blank. AR-9 (a door the receiver can use) is touched by FIX-1. AR-4 is kept via
  `_story_record` (P15).
- JUDGMENT (q11): none. Joins only, no check added. The commit's `judgment: none` holds.
- Hygiene (q8): no non-ASCII byte in the added lines (`git show | grep -P '^\+.*[^\x00-\x7F]'` → 0). handoff_check.py already
  had 9 such lines before this commit. Changelog: 0.

## Trail

- Read: `git show 61595eec` (handoff_check.py, test_handoff.py, changelog diffs); the card's §3 items 1-6, §4 E1-E23 + 4.1, §7,
  the Lead decisions and the binding section; report `docs/tasks/specs/reports/20261117-p1b-pb-report.md`;
  `execution_request.py:145-200, 404-540`; `run_suite.py:2340-2360, 2890-2935`; `handoffs/s5-critic-to-automator.yaml:50-60`,
  `s5-automator-to-critic.yaml:55-75`; handoff_check.py :712-760; `docs/SIBLING_MAP.md` axis headings;
  `docs/tasks/critic-diff-brief.md` q5-q12; `test_judgment_census.py:77`; `probe_by_code.py:8066`, `red_sandbox.py:2266`
  (door flags exist).
- Grep: callers of `window_runtime_record|_story_record|_probe_run_record|PurePosixPath` in the package (excluding tests);
  `probes.runtime_provenance` across the package; the tail-rule clones; `artifacts.probes` / `runtime_probe_before` in piles on
  origin/main (empty), with the positive control `runtime_provenance` (2+ hits).
- Reruns:
  - `python -B scratchpad/probe_j6.py`: output quoted under FIX-1.
  - `python -B scratchpad/dry_list.py` (read-only over DRY-1):
    `230891e480ca 44bcd10c384267c69a56 S5-qa-code-critic-1 red_probe completed 2026-11-17T07:53:03+00:00 pytest-20261117T075258Z.json True` /
    `3cfdedf79422 66bd1d15b5fe5da442d7 S5-qa-automator-1 initial completed ... pytest-20261117T075205Z.json True` /
    `('evidence/runtime-provenance-dry-pytest-20261117T075258Z.json', 'the stand reading of red_probe run 44bcd10c384267c69a56 (dispatch S5-qa-code-critic-1, state/execution-jobs/)')`.
    This matches the report's section D.
  - `test_handoff.py` was not re-run, as the dispatch instructed. The builder's report quotes 749/749.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "FIX-1 handoff_check.py:631 J6 must read runtime_required as run_suite does (run_suite.py:2904 truthy, default True): use not job['request'].get('runtime_required', True); add a row beside E22 (test_handoff.py:584) with required=None expecting J6 and no door",
    "FIX-2 handoff_check.py:521-523 _PROBE_RECORD_PRODUCER and changelog.d/p1b-pb-probe-run-record.md:1: apply binding F-6 wording (the record the launch reading cites), not 'the record is the stand reading run_suite takes'"
  ],
  "class_completeness": "In-diff: one tail rule (_story_record, handoff_check.py:535 only). DERIVERS existence class: card section 7 sweep plus scout question; source-semantics class: F-5 (axis 5). Neither carrier, nor the no_runtime_record null-outcome wiring, is on origin/main piles yet (git grep empty with positive control): proposed findings in live-run-fvf, owner Lead. Axes 16, 24, 33, 34, 38 walked; the others do not apply.",
  "trail": {
    "read": [
      "git show 61595eec (handoff_check.py, test_handoff.py, changelog, report)",
      "docs/tasks/specs/20261117-p1b-pb-runtime-provenance-card.md sections 3, 4, 7, Lead decisions, binding fix round",
      "ai-packages/qa-factory/scripts/execution_request.py:145-200,404-540",
      "ai-packages/qa-factory/scripts/run_suite.py:2340-2360,2890-2935",
      "ai-packages/qa-factory/handoffs/s5-critic-to-automator.yaml, s5-automator-to-critic.yaml",
      "ai-packages/qa-factory/scripts/handoff_check.py:520-664,712-760",
      "docs/SIBLING_MAP.md axis headings; docs/tasks/critic-diff-brief.md q5-q12"
    ],
    "reruns": [
      {"command": "python -B scratchpad/probe_j6.py (runtime_required False/None/0/absent/True on one completed own red_probe job without a reading)", "result": "False->J6 no door; None->J3b door; 0->J3b door; absent->J3b door; True->J3b door"},
      {"command": "python -B scratchpad/dry_list.py (read-only over the kept DRY-1 world)", "result": "critic red_probe job 44bcd10c384267c69a56 before=...075258Z, automator job before=...075205Z; deriver answers evidence/runtime-provenance-dry-pytest-20261117T075258Z.json, matching report section D"}
    ]
  }
}
```
