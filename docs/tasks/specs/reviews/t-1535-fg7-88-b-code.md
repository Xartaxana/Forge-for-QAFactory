# t-1535 -- critic: code review of FG7-88 card B (t-1534), head f3ce26c5

Spec: docs/tasks/specs/20261118-fg7-88-resumed-round-returned-card.md 2.5, 3 (QE1-QE4), 4.B, 12 (F6 (b)).
Tree: C:/QAFactory/forge-repo/.claude/worktrees/agent-a8f4b7e2089baa140, HEAD f3ce26c5, `git status --porcelain` empty before and after the probes.

**Verdict: NEEDS WORK (fit_with_fixes) -- 0 blocking findings, 2 fixes before merge (M3, F1).**

The grammar is right, the three readers take one road, the validator adds no FAIL to the live journal, the DoD set is
green (491 passed). The one hole is the one the dispatch asked about: the echo test that was cut was the only row
guarding the echo's own reading of a malformed cited id, and a probe shows it (M3 survived).

## Findings

**M3 (fix before merge) -- the echo's reading of a malformed `critic:<id>` has no row; the cut test was load-bearing.**
Carrier: tools/journal_echo.py:2193 (`is_critic, cited = journal_validator.critic_basis(basis)`), tools/test_journal_echo_r3.py:121-130.
The QE2 rows in MATRIX_ROWS (test_journal_validator.py:609-613) guard `critic_basis` itself (probe M1: 9 rows kill a loosened
id check). They do not guard the echo's call of it. Probe M3 replaces the echo's call with a local loose parse
(`(True, basis[7:])` for any `critic:` prefix): test_journal_echo_r3.py stays 93 passed, outcome survived. The failure it
lets through is in the wrong direction: an `accepted` with basis `critic:t-77` (malformed: 2 digits) and a critic
`delegated` under `t-77` goes SILENT under the mutant, where the spec (QE2: the verdict of basis None) wants M1
`no_input`. So the answer to the dispatch's edge question: the matrix rows cover the shared grammar, not the echo's door.
Fix, budget-neutral: in the parametrised test add `basis` as a parameter and replace the `(None, ...)` row -- it is
subsumed by the `t-778` row (both expect the M2 literal; every mutant the None row kills, the t-778 row kills) -- by the
row `basis="critic:t-77", delegated_under="t-77" -> [("no_input", "t-001")]` (expected from QE2 + the echo's M1 rule).

**F1 (fix before merge, small) -- three docstrings now state the old rule as exact.**
tools/journal_validator.py:158 `(e) basis=="critic": legal iff ...`, :676 `5) basis == "critic": legal iff ...`,
tools/r3_integration_check.py:206 `- event == "accepted" and basis == "critic"`. The spec lets comments keep the word
for the grep, but these three lines describe what the code accepts, and after the diff it accepts `critic:<task id>` too
(Q7: an annotation that lies). Fix: add "or `critic:<task id>` (critic_basis)" to each; the acceptance grep stays 0
code lines (these are docstring lines either way).

## Standing questions

- Q1 FIT TO SPEC: yes. `critic_basis` matches 2.5 exactly (journal_validator.py:336-347): `"critic"` -> (True, None);
  `"critic:"+tid` with `TASK_ID_RE.fullmatch` -> (True, tid); anything else, non-str included -> (False, None).
  TASK_ID_RE = journal_keys.ID_RE `^t-([0-9]{3,9})([a-z]{0,2})\Z` (ASCII digits, so fullwidth/Cyrillic fail). Branch 5
  at the same position (:726), after judge (:702) and FLOOR (:714-722): QE4 holds by position; the `-cited` twins of the
  FLOOR and UNKNOWN_BY rows assert it. QE3: no join in the validator; the echo confirms by `cited in critic_task_ids`
  (:2195). Bare `critic` keeps its verdict in all three readers (unchanged rows green). Generic FAIL text names the form (:760).
- Q2 BUILDER'S OWN DECISIONS: `word = "critic"` local and `_CRITIC_MARKER[:-1]` in the r3 fallback exist only to keep the
  acceptance grep at 0; disclosed in the report, behaviour identical, not a finding. The lazy import's fallback errs
  toward fewer trails (stricter report): safe direction.
- Q3 SEAMS: journal_echo already imports journal_validator (:253); r3 imports it lazily. The two FAIL texts changed by
  insertion; no pin on them (grep `own rank -- this would` / `by ranked below lead` over tools: only the source).
- Q4 CLASS-WIDE: readers of the basis field in tools/ (grep `get("basis")|["basis"]`, non-test): journal_echo:2185,
  journal_validator:700, :798 (queued-to-lead only), r3_integration_check:248 -- all three critic readers moved; the
  others are other fields (dup_ratchet, language_sites). journal_write.py `--basis` passes any string (spec: unchanged).
  `BASIS_VALUES` (:326) has no reader. Complete.
- Q5 TESTS: (a) killing power: M1 and M2 killed, M3 survived -> finding M3. (b) expected values: twins = the bare row's
  verdict (QE1/QE4); QE2 rows = GENERIC, the verdict of `after-builder-sonnet-bare` (QE2); echo kinds from 2.5/QE3; r3
  from 2.5. (c) rows at every door: matrix, echo, r3 trail -- yes. (d) no test rewritten (f6d7cd78 trimmed the builder's own
  new test, before merge). (e) the echo `(None, ...)` row duplicates `t-778`'s verdict through the same door (fold into M3).
  (f) +29 test lines vs +37 product lines; within budget. (g) no new file.
- Q6 DUPLICATION AND CONSISTENCY: one grammar, three callers; the r3 exact-compare fallback is spec-mandated (2.5).
  none other found: grep `basis *== *"critic"` over the three files = docstring lines only; control `basis *== *"queued-to-lead"` finds :740.
- Q7 CODE QUALITY: new functions are 12 and 8 lines, no deep nesting, no dead branch; F1 only.
- Q8 HYGIENE: not a package path; n/a.
- Q9 RATCHETS: no ratchet file touched (diff stat: 7 files, none a baseline). The forge-check result is the pipeline's; not re-run.
- Q10 ARCHITECTURE: the AR map (ai-packages/qa-factory/design/architecture.md) names none of the three files; no AR-n touched.
  VARIETY: forge journal tooling only; no project shape reaches it; an unknown basis falls to the generic FAIL as before.
- Q11 JUDGMENT: a form check of a string field; moves no judgment into code.
- Q12 ONE ROAD: three readers on one function; none found otherwise (same greps as Q4).

## Spot-checks

- Live journal, branch vs main validator (logs/journal/dev1.jsonl, 4314 lines, `decide(text, None, drift=False)`, same
  config text): both `1 3`, outputs byte-identical (`diff` -> IDENTICAL); the 3 are pre-existing (ts non-monotonic x2, attempt x1).
  Positive control that the matrix sees the critic forms: 329 accepted lines with basis `critic`/`critic:...`, 0 malformed
  under the strict regex, `_matrix_d0058_violation` FAIL 0 under main and 0 under branch (matches the spec's M10 claim that every
  live `critic:t-` accept passes by rank).
- Report witness `492 passed` predates f6d7cd78's trim; my run at f3ce26c5: `491 passed` -- consistent (one test removed).
- Report says the mechanism files are staged, not committed; f3ce26c5 commits them ("Committed before the critic so the
  review has a base"). The commit message says "accepted/rejected basis"; the matrix applies only to accepted (:679) -- the
  message overstates, the code is right.
- Acceptance greps: `critic_basis(` non-test = def :336 + validator :726 + echo :2193 + r3 :154 (via `_is_critic_basis`, called :248).

## Trail

Read: spec 2.5, 3, 4.B, 9, 12; the diff origin/main...f3ce26c5; journal_validator.py :150-160, :316-347, :665-760, :1056-1080;
journal_echo.py :2160-2205; r3_integration_check.py :144-157, :195-255; test_journal_validator.py :528-630;
test_journal_echo_r3.py :91-130; t-1534 report; journal_keys.py:80.

Runs (verbatim tails):
- `python -B -m pytest tools/test_journal_validator.py tools/test_journal_echo_r3.py tools/test_r3_integration_check.py -q` (in the tree) -> `491 passed in 5.17s`
- branch vs main validator over dev1.jsonl -> `1 3` / `1 3`, `IDENTICAL`; matrix over critic-basis accepts -> `n 329 malformed 0 fail 0` (both)
- probes: see the block.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "M3: tools/test_journal_echo_r3.py:121-130 -- add a basis parameter and replace the (None, ...) row (subsumed by t-778) with basis critic:t-77 + critic delegated under t-77 -> [(no_input, t-001)]; the echo's reading of a malformed cited id has no row (probe M3 survived). Fix before merge, not blocking.",
    "F1: tools/journal_validator.py:158, :676 and tools/r3_integration_check.py:206 -- docstrings state basis == critic as the exact rule; add 'or critic:<task id> (critic_basis)'. Fix before merge, not blocking."
  ],
  "class_completeness": "Complete: every non-test reader of the basis field in tools/ (journal_validator:700, journal_echo:2185, r3_integration_check:248) reads critic_basis; journal_write --basis unchanged per spec; BASIS_VALUES has no reader. Control: same grep shape finds queued-to-lead at journal_validator:740.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261118-fg7-88-resumed-round-returned-card.md (2.5, 3, 4.B, 9, 12)",
      "git diff origin/main...f3ce26c5",
      "tools/journal_validator.py :150-160, :316-347, :665-760, :1056-1080",
      "tools/journal_echo.py :2160-2205",
      "tools/r3_integration_check.py :144-157, :195-255",
      "tools/test_journal_validator.py :528-630",
      "tools/test_journal_echo_r3.py :91-130",
      "tools/journal_keys.py :80",
      "docs/tasks/handoffs/t-1534-fg7-88-b-report.md"
    ],
    "reruns": [
      {
        "command": "python -B -m pytest tools/test_journal_validator.py tools/test_journal_echo_r3.py tools/test_r3_integration_check.py -q (cwd $W = W=C:/QAFactory/forge-repo/.claude/worktrees/agent-a8f4b7e2089baa140, HEAD f3ce26c5; $W is that path in every probe command below)",
        "result": "491 passed in 5.17s"
      },
      {
        "command": "journal_validator.decide(dev1.jsonl, None, drift=False, config_text=delegation.config.yaml) with tools of origin/main and of f3ce26c5 (git archive), diff of outputs",
        "result": "main: 1 3; branch: 1 3; IDENTICAL"
      },
      {
        "command": "_matrix_d0058_violation over every accepted with a critic-prefixed basis in dev1.jsonl, main and branch",
        "result": "n 329 malformed 0 fail 0 (both)"
      },
      {
        "command": "python -B $W/ai-packages/qa-factory/scripts/tests/mutate_once.py --root $W --id M-cb-anyid --target tools/journal_validator.py --old \"        if TASK_ID_RE.fullmatch(tid):\" --new \"        if tid:\" --test tools/test_journal_validator.py --pytest",
        "result": "9 failed, 347 passed; FAILED test_matrix_by_function_rank[qe2-short-id] ...; sha256 equal=True; outcome: killed"
      },
      {
        "command": "python -B $W/ai-packages/qa-factory/scripts/tests/mutate_once.py --root $W --id M-echo-cited --target tools/journal_echo.py --old \" or (cited is not None and cited in critic_task_ids):\" --new \":\" --test tools/test_journal_echo_r3.py --pytest",
        "result": "1 failed, 92 passed; FAILED test_s1_basis_cited_critic_task_id[t-777-kinds0]; sha256 equal=True; outcome: killed"
      },
      {
        "command": "python -B $W/ai-packages/qa-factory/scripts/tests/mutate_once.py --root $W --id M-echo-loose --target tools/journal_echo.py --old \"    is_critic, cited = journal_validator.critic_basis(basis)\" --new \"    is_critic, cited = (True, basis[7:]) if isinstance(basis, str) and basis.startswith('critic:') else journal_validator.critic_basis(basis)\" --test tools/test_journal_echo_r3.py --pytest",
        "result": "93 passed; FAIL lines: 0; sha256 equal=True; outcome: survived"
      }
    ]
  },
  "mutants": [
    {
      "place": "tools/journal_validator.py critic_basis, the task id check",
      "change": "if TASK_ID_RE.fullmatch(tid): -> if tid:",
      "run": "python -B $W/ai-packages/qa-factory/scripts/tests/mutate_once.py --root $W --id M-cb-anyid --target tools/journal_validator.py --old \"        if TASK_ID_RE.fullmatch(tid):\" --new \"        if tid:\" --test tools/test_journal_validator.py --pytest",
      "outcome": "killed",
      "killed_by": "test_journal_validator.py::test_matrix_by_function_rank[qe2-short-id] and 8 other qe2 rows"
    },
    {
      "place": "tools/journal_echo.py _check_accepted_r3, S1 confirmation by the cited id",
      "change": "drop 'or (cited is not None and cited in critic_task_ids)'",
      "run": "python -B $W/ai-packages/qa-factory/scripts/tests/mutate_once.py --root $W --id M-echo-cited --target tools/journal_echo.py --old \" or (cited is not None and cited in critic_task_ids):\" --new \":\" --test tools/test_journal_echo_r3.py --pytest",
      "outcome": "killed",
      "killed_by": "test_journal_echo_r3.py::test_s1_basis_cited_critic_task_id[t-777-kinds0]"
    },
    {
      "place": "tools/journal_echo.py _check_accepted_r3, the call of critic_basis",
      "change": "a local loose parse: any 'critic:' prefix -> (True, basis[7:])",
      "run": "python -B $W/ai-packages/qa-factory/scripts/tests/mutate_once.py --root $W --id M-echo-loose --target tools/journal_echo.py --old \"    is_critic, cited = journal_validator.critic_basis(basis)\" --new \"    is_critic, cited = (True, basis[7:]) if isinstance(basis, str) and basis.startswith('critic:') else journal_validator.critic_basis(basis)\" --test tools/test_journal_echo_r3.py --pytest",
      "outcome": "survived",
      "remark": "M3"
    }
  ]
}
```
