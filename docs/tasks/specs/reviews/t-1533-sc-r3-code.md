# t-1533 critic: re-review of the S-C fix round 3 (t-1521) against verdict t-1530 R1-R4

Tree: `.claude/worktrees/agent-aab6815809df7010e`, HEAD d0fb17e3 (clean). Fix diff `d705436c..d0fb17e3` (3 files: `tools/dispatch_manifest.py`
+4/-3, `tools/test_dispatch_manifest.py` +4/-1, the report); merge d705436c (parents 2b389a03, 9ee5c5e2 = origin/main today).
Spec/DoD: verdict t-1530 R1-R4, spec `20261117-forge-test-rules-spec.md` 5.1 (PASS/REFUSED lists `:503-511`), dispatch edges.

## Verdict

**ACCEPT** (fit) -- R1-R4 and the merge fixed, each reproduced; 0 blocking findings, 0 fixes. Acceptance stays the Lead's (rule 6).

| item | status | carrier |
|---|---|---|
| R1 | fixed | `tools/dispatch_manifest.py:970` `_TEST_KEY_RE` takes `` `? `` before the colon; row `pass-backticked-word` `tools/test_dispatch_manifest.py:1218`; probe m1 killed |
| R2 | fixed | `tools/dispatch_manifest.py:1065-1067` skip only when `got is not None and not got[2]`; row `tools/test_dispatch_manifest.py:1447` (`- Test: <canon run>` in the DoD -> 2 `test_canon_x.py whole`); probe m2 killed |
| R3 | fixed | `tools/test_dispatch_manifest.py:1446`: the well-formed line is now the DoD's second line (`dod="DoD: `...`\n`test: ...`"`, via `test_dod_run_check :1472`); probe m3 (skip removed) killed |
| R4 | fixed | `CLAUDE.md:82` R11-f: "... over COORDINATOR.md rule 2's threshold, `designer:` (...) and, for a builder, `test:` (...)" -- matches the gate `dispatch_manifest.py:1184` `if is_builder and max(counts) >= DESIGNER_THRESHOLD` |
| merge | fixed | `git diff 9ee5c5e2 d0fb17e3 -- CLAUDE.md`: only the R11-f row differs; R11-h row sha256 b7833fa2... identical on main and branch; AGENTS.md differs from main only in the byte-count line and the R11-f row; `agents_md.py --check` -> up to date (114879 bytes) |

## Findings

None blocking, none to fix.

Notes (no action): (1) R11-f reads "and, for a builder, `test:`" inside the "over ... threshold" clause -- the nesting is the
natural reading and matches the gate; no finding. (2) The spec 5.1 item 1 `test_lines(cut)` seam note of t-1530 stands for
the Lead (spec text, no reader). (3) The well-formed `test: <canon cmd> | expected from: x` inside the DoD is still skipped
-- accepted by the t-1530 dispatch edge.

## Standing questions

- Q1 fit: R1-R4 as stated; spec 5.1 PASS forms walked in-process: `` `test`: ``, `` - `test`: ``, `` **`test`:** `` -> well-formed;
  REFUSED forms stay refused: `Test row: x` -> None, `` `test`: tools/x.py `` -> bad, `` test`: none | expected from: x `` -> bad;
  the full TEST_ROWS table (PASS and REFUSED rows `:1211-1239`) green.
- Q2 builder decisions: merge resolution by `checkout --theirs AGENTS.md` then regenerate -- safe (regenerated, check green).
- Q3 seams: `_dod_commands` (the DoD-run reader) now narrower skip: a malformed test-key line is read as a run again -- the FR-41 direction.
- Q4 class: `_test_line_parse` has two callers (`:1011` `_test_line_state`, `:1065` `_dod_commands`); grep `_test_line_parse|_TEST_KEY_RE` (case-insensitive) over tools/*.py: only these sites (positive control: the def at `:975` found). `_test_line_state` already treats `got[2]` as bad (`:1015`). No sibling left.
- Q5 tests: (a) three probes, all killed (below); builder's red-before lines reproduce the same three FAIL ids. (b) values: rows' expected 0/2 and `test_canon_x.py whole` trace to t-1530 R2/R3 and spec 5.1. (c) every new behaviour has a row (R1 pass row, R2 refuse row). (d) the old S-C-2 row rewritten into the R3 row; its behaviour checked at `:1446`. (e) none: `pass-backticked-word` vs `pass-backticked-key` are different forms. (f) +3/-1 table rows, one line each, minimum t-1530 asked; no pin. (g) no new file.
- DUPLICATION AND CONSISTENCY: none found -- the fix reuses `_test_line_parse`, no second parser (grep above).
- CODE QUALITY: none found -- 2 changed code lines, no new function.
- Q8: tools/, not package. Q9: no ratchet file in the diff stat (3 files). Q10: no AR-n touched; VARIETY: forge-only tools, no project shape affected.
- Q11: none (form check). Q12: none found -- the builder-only scope is spec 5.1 item 2 / `:1184`; grep over the diff for language/runner names: none.

## Trail

Read: t-1530 verdict; spec 5.1 `:473-511`; `git diff d705436c d0fb17e3` (whole); `git diff 9ee5c5e2 d0fb17e3 -- CLAUDE.md AGENTS.md`;
`tools/dispatch_manifest.py :965-1015, :1060-1070`; `tools/test_dispatch_manifest.py :1205-1245, :1430-1475`; report section Round 3.
Runs (verbatim tails, in the worktree):
- `git status --porcelain` -> (empty), before and after the probes.
- `python -m pytest tools/test_dispatch_manifest.py tools/test_dispatch_new.py tools/test_dispatch_gate_md.py -q` -> `500 passed in 2.00s`.
- `python -B tools/agents_md.py --check` -> `AGENTS.md: up to date (114879 bytes)`.
- control: `python -m pytest tools/test_dispatch_manifest.py -q` -> `371 passed in 1.35s`.
- R11-h: `grep "^   | h |"` on `9ee5c5e2:CLAUDE.md` and `d0fb17e3:CLAUDE.md` -> sha256 b7833fa287a6... both.
- in-process `_test_line_parse` probe of 7 key forms (results under Q1).
- mutate_once.py m1/m2/m3 -> `outcome: killed` each, sha256 9cf42a89... equal=True.

```json
{
  "verdict": "fit",
  "blockers": [],
  "class_completeness": "R1 key forms walked (backtick before/after colon, bullet, bold, prose Test row, none, no source); R2 both callers of _test_line_parse checked, _test_line_state already treats a malformed parse as bad; R4 text matched to the gate condition dispatch_manifest.py:1184; merge: R11-h byte-identical to origin/main 9ee5c5e2, AGENTS.md regenerated and checked.",
  "trail": {
    "read": [
      "docs/tasks/specs/reviews/t-1530-sc-sd-r2-code.md",
      "docs/tasks/specs/20261117-forge-test-rules-spec.md 473-511",
      "git diff d705436c d0fb17e3 (tools/dispatch_manifest.py, tools/test_dispatch_manifest.py, t-1521-sc-report.md Round 3)",
      "git diff 9ee5c5e2 d0fb17e3 -- CLAUDE.md AGENTS.md",
      "tools/dispatch_manifest.py 965-1015 1060-1070 1184; tools/test_dispatch_manifest.py 1205-1245 1430-1475"
    ],
    "reruns": [
      {
        "command": "python -m pytest tools/test_dispatch_manifest.py tools/test_dispatch_new.py tools/test_dispatch_gate_md.py -q",
        "result": "500 passed in 2.00s"
      },
      {
        "command": "python -B tools/agents_md.py --check",
        "result": "AGENTS.md: up to date (114879 bytes)"
      },
      {
        "command": "python -m pytest tools/test_dispatch_manifest.py -q (control before probes)",
        "result": "371 passed in 1.35s"
      },
      {
        "command": "python -B <wt>/ai-packages/qa-factory/scripts/tests/mutate_once.py --root <wt> --id m1-key-backtick --target tools/dispatch_manifest.py --old 'r\"test(?:\\*\\*)?`?[ \t]*:' --new 'r\"test(?:\\*\\*)?[ \t]*:' --test tools/test_dispatch_manifest.py --pytest",
        "result": "1 failed, 370 passed; FAILED test_test_line_table[pass-backticked-word]; equal=True; outcome: killed"
      },
      {
        "command": "python -B <wt>/ai-packages/qa-factory/scripts/tests/mutate_once.py --root <wt> --id m2-malformed-skip --target tools/dispatch_manifest.py --old 'if got is not None and not got[2]:' --new 'if got is not None:' --test tools/test_dispatch_manifest.py --pytest",
        "result": "1 failed, 370 passed; FAILED test_dod_run_check[... - Test: `python -m pytest test_canon_x.py -q--builder-cls4-2-...]; equal=True; outcome: killed"
      },
      {
        "command": "python -B <wt>/ai-packages/qa-factory/scripts/tests/mutate_once.py --root <wt> --id m3-no-skip --target tools/dispatch_manifest.py --old 'if got is not None and not got[2]:' --new 'if False:' --test tools/test_dispatch_manifest.py --pytest",
        "result": "1 failed, 370 passed; FAILED test_dod_run_check[... `test: test_canon_x.py | expected from: owner--builder-cls3-0--]; equal=True; outcome: killed"
      },
      {
        "command": "sha256 of the R11-h row on 9ee5c5e2:CLAUDE.md and d0fb17e3:CLAUDE.md",
        "result": "b7833fa287a64f5c... both"
      }
    ]
  },
  "mutants": [
    {
      "place": "tools/dispatch_manifest.py:970 _TEST_KEY_RE",
      "change": "optional backtick before the colon removed",
      "run": "python -B <wt>/ai-packages/qa-factory/scripts/tests/mutate_once.py --root <wt> --id m1-key-backtick --target tools/dispatch_manifest.py --old 'r\"test(?:\\*\\*)?`?[ \t]*:' --new 'r\"test(?:\\*\\*)?[ \t]*:' --test tools/test_dispatch_manifest.py --pytest",
      "outcome": "killed",
      "killed_by": "test_test_line_table[pass-backticked-word]"
    },
    {
      "place": "tools/dispatch_manifest.py:1066 _dod_commands",
      "change": "well-formed conjunct dropped (malformed lines skipped again)",
      "run": "python -B <wt>/ai-packages/qa-factory/scripts/tests/mutate_once.py --root <wt> --id m2-malformed-skip --target tools/dispatch_manifest.py --old 'if got is not None and not got[2]:' --new 'if got is not None:' --test tools/test_dispatch_manifest.py --pytest",
      "outcome": "killed",
      "killed_by": "test_dod_run_check malformed Test: canon row (:1447)"
    },
    {
      "place": "tools/dispatch_manifest.py:1066 _dod_commands",
      "change": "skip removed (if False)",
      "run": "python -B <wt>/ai-packages/qa-factory/scripts/tests/mutate_once.py --root <wt> --id m3-no-skip --target tools/dispatch_manifest.py --old 'if got is not None and not got[2]:' --new 'if False:' --test tools/test_dispatch_manifest.py --pytest",
      "outcome": "killed",
      "killed_by": "test_dod_run_check well-formed in-DoD row (:1446)"
    }
  ]
}
```
