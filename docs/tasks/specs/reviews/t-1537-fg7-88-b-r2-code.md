# t-1537 -- critic: re-review of FG7-88 card B fix round 2 (t-1534), head 939dcb88

Base: t-1535 verdict (docs/tasks/specs/reviews/t-1535-fg7-88-b-code.md, M3 + F1), reviewed head f3ce26c5.
Tree: C:/QAFactory/forge-repo/.claude/worktrees/agent-a8f4b7e2089baa140, HEAD 939dcb88, `git status --porcelain` empty before and after the probe.
Scope: `git diff f3ce26c5 939dcb88` (4 files, +16/-9): the report's "Round 2", two docstrings in journal_validator.py, one in r3_integration_check.py, the parametrised echo test.

**Verdict: NEEDS WORK (fit_with_fixes) -- 0 blocking findings; M3 fixed, F1 fixed; 1 new small fix before merge (F2, introduced by the fix diff).**

## M3 -- fixed

Carrier: tools/test_journal_echo_r3.py:121-131. `basis` is now a parameter; the row
`("critic:t-77", "t-77", [("no_input", "t-001")])` is present (:125) with the expected value from QE2 + the echo's M1 rule,
as asked. The `(None, ...)` row is gone; it was subsumed by `("critic:t-777", "t-778", [("phantom_basis", "t-001")])` (:123):
same door, same expected kinds, a critic absent under the cited id in both -- every mutant the None row killed, the t-778 row kills.
Row count unchanged (3), budget-neutral.
My own probe M3 (the echo's `journal_validator.critic_basis(basis)` call at tools/journal_echo.py:2193 swapped for a loose
`critic:` prefix parse), run by mutate_once.py with its byte copy: `1 failed, 92 passed`, FAILED
`test_s1_basis_cited_critic_task_id[critic:t-77-t-77-kinds2]`, sha256 before = after =
e02065f6924c1813f2c89b9000071c48981fb87aba380ba0b7a3d649dab9e181, outcome **killed** (in t-1535 the same mutant survived).
The builder's reported sha256 (same value) matches mine.

## F1 -- fixed

tools/journal_validator.py:158 `(e) basis=="critic" or \`critic:<task id>\` (critic_basis): ...`, :676 `5) basis == "critic" or
\`critic:<task id>\` (critic_basis): ...`, tools/r3_integration_check.py:206 `- event == "accepted" and basis == "critic" or
\`critic:<task id>\` (critic_basis)`. Each now states what the code accepts. Acceptance grep `basis *== *"critic"` over the three
files: validator :158, :676 (docstrings), r3 :206 (docstring), journal_echo :1978/:2009/:2013/:2017 (comments) and :2171/:2174
(docstring) -- the echo hits are pre-existing and outside this diff; no code line. Positive control, same shape:
`basis *== *"queued-to-lead"` finds the code line journal_validator.py:740.

## F2 (new, fix before merge, small) -- a dead branch left by the M3 fix

tools/test_journal_echo_r3.py:129 `base = [] if delegated_under is None else [...]`: after the `(None, ...)` row was dropped,
no row passes `delegated_under=None`, so the `[] if ... is None` arm is unreachable (Q7: dead branch). Introduced by this diff
(it removed the only None row). Fix: `base = [_l(event="delegated", agent="critic", task_id=delegated_under)]`.

## Other changes in the diff

Only the report's "Round 2" section (docs/tasks/handoffs/t-1534-fg7-88-b-report.md, +6) -- the hand-back itself; its witness
`491 passed` matches my run. Nothing else changed: no product code line, no other test.

## Standing questions (scoped to the fix diff)

- Q5 TESTS: (a) M3 probe killed; (b) the new row's value traces to QE2 (malformed id = not a critic basis) + the echo's M1 rule;
  (d) the dropped row's behaviour is still checked by :123; (e) no duplicate; (f) row count unchanged.
- Q6 DUPLICATION: none introduced: the diff adds no code (grep above).
- Q7 CODE QUALITY: F2 only.
- Q4/Q9/Q10/Q11/Q12: unchanged from t-1535; the diff touches no reader, ratchet or AR-n.

## Trail

Read: t-1535 verdict; `git diff f3ce26c5 939dcb88` (all of it); tools/test_journal_echo_r3.py:115-135; report "Round 2".
Runs:
- `python -B -m pytest tools/test_journal_echo_r3.py tools/test_journal_validator.py tools/test_r3_integration_check.py -q` (in the tree, HEAD 939dcb88) -> `491 passed in 4.91s`
- grep `basis *== *"critic"` / control `basis *== *"queued-to-lead"` over the three files -> as above
- probe M3, see the block.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "F2: tools/test_journal_echo_r3.py:129 -- 'base = [] if delegated_under is None else [...]' is a dead arm now that the (None, ...) row is gone; make it 'base = [_l(event=\"delegated\", agent=\"critic\", task_id=delegated_under)]'. Introduced by the M3 fix. Fix before merge, not blocking."
  ],
  "class_completeness": "M3 and F1 of t-1535 fixed at their carriers (test_journal_echo_r3.py:125; journal_validator.py:158, :676; r3_integration_check.py:206). The fix diff adds no code line; the three docstrings named in F1 are all the code-describing docstrings of the old exact rule in the three files (grep basis == critic; control queued-to-lead finds journal_validator.py:740). The journal_echo comment hits are pre-existing and outside t-1535's findings.",
  "trail": {
    "read": [
      "docs/tasks/specs/reviews/t-1535-fg7-88-b-code.md",
      "git -C $W diff f3ce26c5 939dcb88 (W=C:/QAFactory/forge-repo/.claude/worktrees/agent-a8f4b7e2089baa140)",
      "tools/test_journal_echo_r3.py :115-135",
      "docs/tasks/handoffs/t-1534-fg7-88-b-report.md (Round 2)"
    ],
    "reruns": [
      {
        "command": "python -B -m pytest tools/test_journal_echo_r3.py tools/test_journal_validator.py tools/test_r3_integration_check.py -q (cwd $W, HEAD 939dcb88; control run, names the --test path of the probe)",
        "result": "491 passed in 4.91s"
      },
      {
        "command": "grep -nE 'basis *== *\"critic\"' tools/journal_validator.py tools/journal_echo.py tools/r3_integration_check.py; control grep -nE 'basis *== *\"queued-to-lead\"' tools/journal_validator.py",
        "result": "validator :158, :676 docstrings; r3 :206 docstring; echo :1978 :2009 :2013 :2017 comments, :2171 :2174 docstring; control: :159, :677, :740 (code)"
      },
      {
        "command": "python -B $W/ai-packages/qa-factory/scripts/tests/mutate_once.py --root $W --id M3-echo-loose --target tools/journal_echo.py --old \"    is_critic, cited = journal_validator.critic_basis(basis)\" --new \"    is_critic, cited = (True, basis[7:]) if isinstance(basis, str) and basis.startswith('critic:') else journal_validator.critic_basis(basis)\" --test tools/test_journal_echo_r3.py --pytest",
        "result": "1 failed, 92 passed; FAILED tools/test_journal_echo_r3.py::test_s1_basis_cited_critic_task_id[critic:t-77-t-77-kinds2]; sha256 before e02065f6...e181 after e02065f6...e181 equal=True; outcome: killed; git status --porcelain empty after"
      }
    ]
  },
  "mutants": [
    {
      "place": "tools/journal_echo.py:2193 _check_accepted_r3, the call of critic_basis",
      "change": "a local loose parse: any 'critic:' prefix -> (True, basis[7:])",
      "run": "python -B $W/ai-packages/qa-factory/scripts/tests/mutate_once.py --root $W --id M3-echo-loose --target tools/journal_echo.py --old \"    is_critic, cited = journal_validator.critic_basis(basis)\" --new \"    is_critic, cited = (True, basis[7:]) if isinstance(basis, str) and basis.startswith('critic:') else journal_validator.critic_basis(basis)\" --test tools/test_journal_echo_r3.py --pytest",
      "outcome": "killed",
      "killed_by": "test_journal_echo_r3.py::test_s1_basis_cited_critic_task_id[critic:t-77-t-77-kinds2]"
    }
  ]
}
```
