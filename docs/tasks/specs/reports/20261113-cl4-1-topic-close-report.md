# CL4-1 topic close report (merge N1, F1, N3)

Branch `wip/cl4-1-n4`. Commits in order: ddccce9 (merge of `wip/cl4-1-n1` e7dee9e; no conflict, auto-merge of `collect_stall.py`; the
merge commit carries `architecture: AR-1, AR-14, AR-22 -- N1's row goes through journal_run -> _append_jsonl, one writer (corrects AR-13 in e7dee9e)`;
no features.json edit was needed, the merge gate printed "new package files 0"), 4e6f7a6 (F1), de885ca (N3), then this report and the N1 report.

## F1
`tools/collect_intake.py` `ignored_lines`: `if got is None or got == []` -> `if key not in story or got == []`. Absent key or `[]` prints nothing;
explicit `null` or any non-list prints `<label>: unreadable (<type>)`. One I-row `T13` in `test_the_layout_text_of_a_looped_only_story_says_stalled_no`
(both keys `ignored` and `loop_ignored` null): `stalled: no\nignored: unreadable (NoneType)\nlooped: yes\nloop ignored: unreadable (NoneType)`.
Not touched: `clean()` of where/why, non-dict list entries (Q2).

## N3
The three phrases were found by their quoted text (no drift problem), edited once each: `kb/04-onboarding-doctor.xhtml` (408, 417), `SKILL.md` line 4
(about 113 characters, no re-wrap). Fragment `changelog.d/collect-4-cl4-1.md` is the spec text verbatim; the spec text holds no non-ASCII byte, nothing replaced.

## Verification (verbatim)

### 1. `python -m pytest tools/test_collect_intake.py -q` (worktree subshell), after the last code edit
```
........................................................................ [ 94%]
....                                                                     [100%]
76 passed in 10.79s
```
(76 before and after: F1 is a row inside an existing test.)

### 2. `scenario_walk.py --witness-for ... collect_stall.py collect_pack.py driver_machine.py`
Printed 77 `keep` rows for driver_machine.py, `keep test_driver_stop_record.py` for collect_stall.py, and for collect_pack.py
`no scenario or keep row covers scripts/collect_pack.py: run the whole scenario layer` with test_scenario_cart_1, test_scenario_local_1_0108,
test_scenario_local_1_arm_b, test_scenario_walk, test_scenario_world. Full printout was written to a scratch file; slow files
(`slow_tests.json` > 10 s: the story_run_*, controller, infra, scenario_cart/local, etc.) were not run. The 25 non-slow files printed were run one by one
from `ai-packages/qa-factory/scripts/tests` as `python -B <file>.py`:
```
== test_audit_rules exit=0 :: === audit rules (...): 375/375 ok ===
== test_codex_tool_guidance exit=0 :: 217/217 ok
== test_dispatch_identity exit=0 :: 114/114 ok
== test_driver_stop_record exit=0 :: 255/255 ok
== test_exploratory_answers exit=0 :: 107/107 ok
== test_first_look_code_look exit=0 :: 127/127 ok
== test_first_look_step exit=0 :: 102/102 ok
== test_gate_question_form exit=0 :: 297/297 ok
== test_human_questions exit=0 :: 291/291 ok
== test_login_need exit=0 :: 33 passed in 0.99s
== test_null_outcomes exit=0 :: 337/337 ok
== test_person_owned exit=0 :: 82/82 ok
== test_probe_marker_judgment exit=0 :: 46 passed in 10.89s
== test_probe_not_proved exit=0 :: 47 passed in 5.62s
== test_reference_window exit=0 :: 85/85 ok
== test_s5_window_leftovers exit=0 :: 148/148 ok
== test_scenario_walk exit=0 :: 93/93 ok
== test_scenario_world exit=0 :: 33/33 ok
== test_story_run_first_look exit=0 :: 27/27 ok
== test_story_run_monorepo exit=0 :: 71/71 ok
== test_story_run_s6_w1_frozen exit=1 :: === test_story_run_s6_w1_frozen: 5/6 ok ===
== test_walk_account exit=0 :: 190/190 ok
== test_walk_lanes_parallel exit=0 :: 196/196 ok
== test_walk_supply exit=0 :: 261/261 ok
== test_whole_list_sites exit=0 :: 292/292 ok
```
ONE RED: `test_story_run_s6_w1_frozen` `w1_frozen_console`: first difference at entry #0, the line `note: brief: ...S6-qa-runner-1.md (5,737 B)` where the
frozen capture, masked, holds `(<bytes> B, <bytes> budget B against the ceiling)`. This is the brief-size note wording, unrelated to the stall/loop
code. The same file run in the `cl4-1-n1` worktree (e7dee9e alone) and the `cl4-1-n2` worktree (482b9db alone) gives the same `5/6 ok`, so it is NOT
caused by the meeting of N1 and N2/N4. I did not run it at base 22c3948 itself (no base tree at hand): probable base failure, the Lead or CI to confirm.
`test_audit_rules.py` has 9.6 s in `slow_tests.json` (under 10), so it was run.

### 3. `python -B scripts/selftest.py --lang` (package-dir subshell)
```
PASS lang: no Cyrillic anywhere in the package
PASS lang: no control byte left by an eaten escape sequence (FR-29)

=== qa-factory selftest: 2/2 ok ===
```

### 4. Doc witness (N3)
Keys quoted from the dispatch BEFORE the run: kb `where it stalled or looped, what it cost`; kb `The transcripts of stalled or looped stories are in a
file of their own`; SKILL.md `where it stalled or looped, what it cost`; fragment `` `window_round` row `` and `collect_stall.loop_state`; negative control key
`stalled or looped or halted`. Script (scratchpad, NOT committed), full source:
```python
import sys, io
W = "C:/QAFactory/forge-repo/.claude/worktrees/cl4-1-n4/"
KB = W + "kb/04-onboarding-doctor.xhtml"
SK = W + "ai-packages/qa-factory/skills/qa-collect/SKILL.md"
FR = W + "ai-packages/qa-factory/changelog.d/collect-4-cl4-1.md"
def run(keys):
    bad = 0
    for path, key in keys:
        text = io.open(path, encoding="utf-8").read()
        ok = key in text
        print(("PASS" if ok else "FAIL"), path.split("/")[-1], repr(key))
        bad += not ok
    t = io.open(FR, "rb").read()
    na = [b for b in t if b > 127]
    print("fragment non-ASCII bytes:", len(na))
    return bad + len(na)
keys = [
    (KB, "where it stalled or looped, what it cost"),
    (KB, "The transcripts of stalled or looped stories are in a file of their own"),
    (SK, "where it stalled or looped, what it cost"),
    (FR, "`window_round` row"),
    (FR, "collect_stall.loop_state"),
]
print("== real run"); r = run(keys); print("failures:", r)
print("== negative control (key deliberately absent)")
c = run(keys[:4] + [(FR, "stalled or looped or halted")]); print("failures:", c)
sys.exit(0 if (r == 0 and c > 0) else 1)
```
Output:
```
== real run
PASS 04-onboarding-doctor.xhtml 'where it stalled or looped, what it cost'
PASS 04-onboarding-doctor.xhtml 'The transcripts of stalled or looped stories are in a file of their own'
PASS SKILL.md 'where it stalled or looped, what it cost'
PASS collect-4-cl4-1.md '`window_round` row'
PASS collect-4-cl4-1.md 'collect_stall.loop_state'
fragment non-ASCII bytes: 0
failures: 0
== negative control (key deliberately absent)
PASS (the four present keys, as above)
FAIL collect-4-cl4-1.md 'stalled or looped or halted'
fragment non-ASCII bytes: 0
failures: 1
exit=0   (0 = real run clean AND control failed, as required)
```
`changelog_assemble.py --list` lists `collect-4-cl4-1.md`, no `REFUSED` line anywhere in its output.

### 5. N1 report copy
`sha256sum` of the source and the copy: both `fe7cba8fc428e50a2108471e419c5bf35fe5276022562da0df8beb60b0c9de18`.

## Siblings (grep `\bstalled\b`, case-insensitive, `kb/` and `skills/qa-collect/`; positive control: the same call finds the lines I edited)
- `kb/04-onboarding-doctor.xhtml:408`, `:417`, `SKILL.md:4`: the three named, edited.
- `kb/06-roadmap.xhtml:15`: "the run of TP1-12586, which stalled" is about a run, not the collector: no change.
- Plain `stalled` (no word boundary) also matched `installed` in `07-user-guide`, `02-architecture`, `05-dashboard-metrics`, `01-overview`, `04:412`, SKILL.md `:18`, `:27`:
  false hits, no change. No other stalled-only collector text found.
- Aside (not a sibling by grep): the critic's Q1 (the real unknown stall still worded "stalled" in the gap text) stays the Lead's node.

## Deviations / needed beyond the manifest
- The step 2 spec said "one parameterised row covers both keys": done as a single row T13 with both keys null.
- Beyond the manifest I read: `ai-packages/qa-factory/scripts/slow_tests.json`, the other two worktrees' test runs (cl4-1-n1, cl4-1-n2) for the red-test comparison.
