# t-1529 -- critic: code review of FG7-88 card A (t-1527, builder), head 7ae89de7

Reviewed: `git -C <worktree agent-a5775220a29f5925e> diff origin/main...7ae89de7` (merge base 29add319) against the card
`docs/tasks/specs/20261118-fg7-88-resumed-round-returned-card.md` sections 0, 2.1-2.4, 3 (E1-E18), 4.A, 12, L0.

**Verdict: NEEDS WORK (fit_with_fixes) -- 0 blocking findings, 3 fix-before-merge findings.** The mechanism is correct on
every traced scenario; the fixes are a missing door row, an unproven builder-picked limit, and two stray whitespace edits.
Whether to accept stays the Lead's (rule 6).

## Findings

**F1 (fix before merge; Q5 (c)) -- the door the factory uses, mode `post-send` of `main`, has no row.**
`tools/journal_hooks.py:597-601` (the `elif mode == "post-send"` branch) is the only way the L1 settings command
`python tools/journal_hooks.py post-send` reaches `post_send`. Every new row calls `jh.post_send(...)` directly
(`tools/test_journal_hooks.py:324`, `:347`); the F3 deadline table `tools/test_journal_hooks.py:490` has rows for
`post-agent` and `pre-edit` only, and a `post-send` silence row there would not catch a missing branch either (silence both
ways). Failure scenario: the mode string misspelled or the branch dropped in a later edit -> the hook writes nothing after L1,
every test stays green, the FG7-22 WARN goes back to the E3 miss with no signal. The card's test line ("the existing F3 test
covers `main`") rests on a premise that does not hold; the builder flagged it ("the `post-send` branch of `main` is untested
directly"). Fix: one flavour in `RESUME_ROWS` (e.g. `send:main`) that drives the send through `run_main("post-send", ...)`
and asserts the `JOURNAL: resumed` text in `additionalContext`. My probe shows it would pass today
(`test_p_main_post_send`, trail).

**F2 (fix before merge; Q5 (b), Q6, rule 12) -- `AGENT_ID_MAX = 64` is a builder-picked limit whose stated reason does not
reproduce, and it makes a second id-acceptance form.** `tools/journal_hooks.py:52`, used at `:300`. Report deviation 2:
"otherwise the file-name probe raises and the hook prints NOT checked". Probe with the cap lifted
(`monkeypatch.setattr(jh, "AGENT_ID_MAX", 10**9)`): `to` = 100000 x "a" -> `[]`, 300 x "a" -> `[]` (no exception, no line).
The other two producers accept an id by `transcripts.AGENT_ID_RE` alone with no length bound (`_record_returned`
`tools/journal_hooks.py:439`, `post_agent` through the response parser), so a worker with a 65-character id gets
`delegated` and `returned` but never `resumed` (probe: 65 x "c" -> `[]`, journal `delegated, returned`; 64 x "b" -> written).
Real ids are ~17 characters, so this is a latent asymmetry, not a live miss. Also CLAUDE.md rule 11: a limit applied to outside
input owes a case AT and BEYOND it; the only row is 100000. Fix: drop the cap (the E13 row `to-huge` still passes: probe),
or keep it with the reason re-measured and rows at 64 (written) and 65 (`[]`). The value is spec-silent: the choice is the
Lead's.

**F3 (fix before merge; Q7) -- two stray whitespace edits outside the task.** `tools/journal_hooks.py:53`
`SESSION_RE =re.compile(...)` (main has `SESSION_RE = re.compile`) and `tools/test_session_context.py:1713`
`_ACC =lambda ...` (main has `_ACC = lambda`). Unrelated churn in a mechanism file, pycodestyle E225 class; the lint ratchet
result is the forge-check job's, not re-run here. Fix: restore the space on both lines.

## Builder deviations, judged against the card

1. `category` on `resumed` (copied from the delegated, else `jw._category`): NECESSARY and safe. Rule 2 requires `category`
   on every line (`tools/journal_validator.py:925`); `journal_write._fill_returned` fills it only for `returned`
   (`tools/journal_write.py:484-498`). The card's 2.1 field list omitted it -- a spec gap, resolved in the only legal way.
2. `AGENT_ID_MAX = 64`: see F2.
3. Send outside a git repo -> `[]`: safe direction (no journal, nothing owed; same as `_record_returned` `:442-444`).
4. `_round_step(` = def + 3 calls (`:846`, `:1188`, `:1400`): consistent with the card's intent ("used by
   `validate_new_lines` and `returned_order_warnings`" -- two functions; `validate_new_lines` needs one call for the
   head/seed state and one per new line). Not a finding.
5. `session` copied from the delegated: equal to the sender's or the sender's is absent (F3 (b)); fine.

## Edges probed (dispatch `edges:`)

- X1/X2 cross-session: delegated `session=sess1234`, send with `session_id=zzzz9999-...` -> `[]`, journal unchanged; the
  own session's send afterwards -> one `resumed` (probe `test_p_other_session_then_own`). Row `other-session` covers the first
  half. A delegated or payload with no session writes (card F3 (b) "or one of them is absent").
- Accepted task -> `[]` (row `accepted-task`); unknown agent id `ffffff` -> `[]` (probe); two sends -> one `resumed`
  (row `two-sends`); send while running -> `[]` (row `send-while-running`); after `rejected` -> `resumed` written (probe,
  E7); two full resume rounds -> `delegated, returned, resumed, returned, resumed, returned`, then a third stop writes
  nothing (probe, E9).
- E13 battery: 12 rows, `[]` and journal bytes equal (rows at `tools/test_journal_hooks.py:340-352`); not-JSON stdin
  through `main` -> exit 0, no output (probe).
- Live journal: the branch validator and main's over the SAME file (`C:/QAFactory/forge-repo/logs/journal/dev1.jsonl`, 4290
  lines, 0 `resumed`, 577 `returned` by the same grep shape) give byte-identical results: `decide` at splits 0 / 2157 / 4000
  and the FG7-22 WARN list (probe.py, trail). No new FAIL, no new WARN.

## Standing questions

- Q1 FIT TO THE SPEC: met. 2.1 steps 1-6 in order (`:298-330`), never raises (`post_send` wrapper), silent on deadline
  (`:587`); 2.2 one branch in `_find_delegated` (`:128-129`); 2.3 `EVENTS`, `TASK_ID_REQUIRED_EVENTS`, rule 12 (`:1012`),
  `_round_step` (`:800-816`), 9f "and no resumed since", 9h three refusals with door, WARN step (`:847-850`), docstring 9f/9h/
  item 21; 2.4 both readers. Traced: `_round_step` gives exactly the old states on a journal without `resumed` (setdefault on a
  re-seen delegated == the old set membership; an orphan `returned` closes the pair in both), confirmed by the identical
  live-journal run.
- Q2 BUILDER DECISIONS: above; all safe except the unproven F2 reason.
- Q3 SEAMS: additive; `_returned_pair` removed with no remaining reader (case-insensitive grep `_returned_pair|returned_refs`
  over tools/*.py = 0; control `open_pairs` in the same file = 14).
- Q4 CLASS-WIDE COMPLETENESS: the card's siblings all walked -- `post_agent` (replay branch reads `_find_delegated`; after a
  resume it sees `done=False` and only retries a pending marker, harmless), `record_returned` (one change), the WARN, both
  RESULT PENDING readers, `journal_echo` (through `decide`), merge mode (`validate_new_lines`). Residuals that leave (card
  section 10, not widened), for the Lead to write into «Остатки»:
  `calibration_counts.py:85-86 hand-copies MODEL/TASK_ID_REQUIRED_EVENTS without resumed | узел: <Lead opens>`;
  `hook_liveness_probe.py has no post-send case | узел: <Lead opens>`. Neither starves a reader today (a `resumed` without
  `task_id` is refused before history). Controls: case-insensitive grep `post-send` in tools/hook_liveness_probe.py = 0 (`post-agent`, same file = 6); `resumed` in tools/calibration_counts.py = 0 (`returned`, same file = 3).
- Q5 TESTS: (a) killing power -- `resume-then-stop` dies without the `_find_delegated` branch; the RETURNED_ROWS/RETURN_ROWS
  rows die without `_round_step`/9h/the WARN step; the session and compact rows die without 2.4; the `main` door has none (F1).
  (b) needles trace to 2.3 texts; the 64 limit is builder-picked (F2). (c) F1. (d) the compact test's `== 2` became `== 3`
  by an added row; behaviour still checked there. (e) `returned-twice-after-one-resume` is not a duplicate of
  `twice-for-one-pair` (per round vs per pair). (f) ~98 test lines vs ~165 code lines; no pins. (g) no new file.
- Q6 DUPLICATION AND CONSISTENCY: the write/refuse/door block of `_post_send` (`:323-330`) mirrors `_write_returned`
  (`:363-374`) in 6 lines with different door texts and no race branch -- below a helper's worth, not a finding. The
  `AGENT_ID_MAX` second acceptance form: F2. `_find_delegated` keeps its own two-line copy of the round rule, as the card
  allows (AR-13 note in section 1).
- Q7 CODE QUALITY: no new function over 60 lines (`_post_send` 33 lines, nesting 1); F3.
- Q8 HYGIENE: no package path; n/a.
- Q9 IN-TREE RATCHETS: none touched (diff stat: 9 files, none a ratchet file).
- Q10 ARCHITECTURE: AR-22 producer/reader walked both ways -- producer `post_send` (activated by L1), readers 9f/9h, WARN,
  session_context, compact_snapshot, `_find_delegated`; no reader starved. The commit names axes 1 and 29, not AR-n by number;
  the card names them by analogy (forge tool). VARIETY: n/a -- a forge journal tool, no project shape is met.
- Q11 JUDGMENT: 9h judges journal form and a join (owner data), not a role's output; `judgment: none` in the commit holds.
- Q12 ONE ROAD: none found beyond F2: case-insensitive grep `python|java|kotlin|typescript|pytest|jest|maven|gradle|language|runner` over the added lines of the diff = 5 hits, all door texts (`python -B tools/...`) or `@pytest.mark` decorators, no branch on a language/runner/project name; the `agent_id`-in-payload skip
  is the card's E3 (a send inside a worker), a task condition, not an exclusion from a shared mechanism.

## Seam and class notes (not findings)

- Verdict written during a resumed round, then the worker stops: the stop's `returned` is refused by 9f (closed task), the
  hook keeps a pending marker and its prune later logs "returned lost" (probe output). This is the same path as a first-round
  verdict before the first stop today (FG7-22's subject); the WARN already fired at the verdict. The card is silent on this
  stop; noted for the Lead, no change asked.
- `session_context` keys RESULT PENDING per task (`_task_key`), so a resume of worker A also hides an older `returned` of
  worker B on the same task; `compact_snapshot` is per (task, ref). The card's 2.4 asks exactly this ("like returned_last").

## Spot-checks (claims and their carriers)

- Builder witness 820 + 1: reproduced 116 + 369 + 335 = 820, and 1 (trail).
- Acceptance 3: branch 115, main 115 (each from its own root; the two journal copies differ: 4264 vs 4290 lines), and the
  same-file comparison above is identical.
- Deviation 1 claim "without category every write is refused": holds (carriers above).
- Deviation 2 claim "the file-name probe raises": does not reproduce (F2).

## Trail

Read: the card (whole); diff of the four mechanism files and four test files; `tools/journal_hooks.py:78-200, 236-282,
357-389, 425-520, 575-620`; `tools/journal_validator.py:819-860, 1185-1262` + grep of the loop's `continue`s (only
`:1210`, `:1219`, both before any state); `tools/journal_write.py:149-155, 484-498, 804-816`; `tools/transcripts.py:44, 84-88`;
`tools/test_journal_hooks.py:1-140, 360-375, 475-506`; builder report; commit messages a4194ab0, 7ae89de7; SIBLING_MAP axis 37.

Commands (verbatim tails):
- `( cd <wt> && python -m pytest tools/test_journal_hooks.py -q )` -> `116 passed in 27.42s`
- `( cd <wt> && python -m pytest tools/test_session_context.py -q )` -> `369 passed in 29.46s`
- `( cd <wt> && python -m pytest tools/test_journal_validator.py -q )` -> `335 passed in 4.80s`
- `( cd <wt> && python -m pytest "tools/test_compact_snapshot.py::test_the_open_list_marks_a_dispatch_whose_worker_returned_and_a_returned_never_closes_it" -q )` -> `1 passed in 0.39s`
- Acceptance 3 narrow call: `branch: 115`, `main: 115` (root HEAD cde00072 == origin/main)
- `/tmp/t1529/probe.py` (decide at splits 0/2157/4000 + WARN, branch tools vs root tools, same journal file):
  both `{'0': (1, 3), '2157': (0, 0), '4000': (0, 0), 'warn': 115}`, `cmp` -> `IDENTICAL`
- `/tmp/t1529/test_probe_t1529.py` (7 scenarios on the builder's `repo` fixture) -> `7 passed`
- `/tmp/t1529/test_probe2_t1529.py` -> `uncapped 100000: []`, `uncapped 300: []`, `at 64: ['JOURNAL: resumed t-001a written
  (logs/journal/dev1.jsonl:4)']`, `at 65: [] ['delegated', 'returned', 'resumed', 'delegated', 'returned']`

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "Card siblings walked: post_agent replay branch, record_returned, returned_order_warnings, session_context and compact_snapshot RESULT PENDING, journal_echo via decide, merge mode via validate_new_lines. Leaving residuals for the Lead: calibration_counts.py:85-86 required-set copies lack resumed; hook_liveness_probe has no post-send case (card section 10).",
  "fixes": [
    "F1 tools/test_journal_hooks.py:312 -- add a RESUME_ROWS flavour that sends through run_main('post-send', ...) so the main branch tools/journal_hooks.py:597-601 has a row (fix before merge)",
    "F2 tools/journal_hooks.py:52,300 -- AGENT_ID_MAX=64: stated reason does not reproduce (uncapped 100000 -> []); drop it or re-justify and add rows at 64 and 65 (fix before merge; value is the Lead's)",
    "F3 tools/journal_hooks.py:53 and tools/test_session_context.py:1713 -- restore the space in 'SESSION_RE = re.compile' and '_ACC = lambda' (fix before merge)"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/20261118-fg7-88-resumed-round-returned-card.md",
      "tools/journal_hooks.py",
      "tools/journal_validator.py",
      "tools/session_context.py",
      "tools/compact_snapshot.py",
      "tools/journal_write.py",
      "tools/transcripts.py",
      "tools/test_journal_hooks.py",
      "tools/test_journal_validator.py",
      "tools/test_session_context.py",
      "tools/test_compact_snapshot.py",
      "docs/tasks/handoffs/t-1527-fg7-88-a-report.md"
    ],
    "reruns": [
      {"command": "python -m pytest tools/test_journal_hooks.py -q (worktree)", "result": "116 passed"},
      {"command": "python -m pytest tools/test_session_context.py -q (worktree)", "result": "369 passed"},
      {"command": "python -m pytest tools/test_journal_validator.py -q (worktree)", "result": "335 passed"},
      {"command": "python -m pytest tools/test_compact_snapshot.py::test_the_open_list_marks_a_dispatch_whose_worker_returned_and_a_returned_never_closes_it -q", "result": "1 passed"},
      {"command": "Acceptance 3 narrow call, worktree root and main root", "result": "115 and 115"},
      {"command": "probe.py: decide + WARN, branch vs main validator over the same live journal", "result": "IDENTICAL"},
      {"command": "temp probe tests on the repo fixture (cross-session, unknown id, rejected, main door, two rounds, 64/65 cap)", "result": "all as stated in Findings and Edges"}
    ]
  }
}
```
