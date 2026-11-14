# t-856 A2 fix round -- report

Written in the worktree (same relative path), not the main checkout.

Done: fixes 3, 4, 6 as quoted in the edges. Commit 36ab846c, pushed fast-forward 36a7ed89..36ab846c to origin/offload/a2.
commit-msg gate accepted both files (critic-diff-brief.md was not refused); both files landed in one commit.

Deviation: local branch name offload/a2 was held by another worktree, so I used local branch a2-fix-t856 tracking
origin/offload/a2 and pushed HEAD:offload/a2. Also ran the Lead note's fetch/checkout (equivalent).

Witness (key-presence script /tmp-scratchpad keys.py, not committed; source in the scratchpad:
C:\Users\i_mas\AppData\Local\Temp\claude\b3e3188b390a00d9\9408e840-5521-4070-9616-fa75174d792f\scratchpad\keys.py).
Keys verbatim: `tests-over: <причина>`, `хук commit-msg без неё предупреждает`, `test_fixes_<тикет>.py` (TESTING.md);
`Бюджет / Объём`, `ai-packages/` (critic-diff-brief.md). Absent: old sentence, `test_fix_13797.py`.
Output (console shows cp1251 mojibake for the key text; results are what matter):

    PRESENT x5 (all five keys)
    ABSENT-OK old sentence; ABSENT-OK test_fix_13797.py
    RUN: PASS
    MISSING 'tests-over: <причина>' (key dropped from text)
    NEGATIVE CONTROL: FAIL (expected)

Old sentence also checked: `grep -c "отчёта, критик судит её" docs/TESTING.md` -> 0 (the sentence was line-wrapped, so
the script's single-line check alone is weak; the grep covers the wrapped form).

git diff --stat: docs/TESTING.md 7 lines, docs/tasks/critic-diff-brief.md 6 lines (2 files, 8 insertions, 5 deletions).
Hooks output at commit: factory rules index, architecture index, AGENTS.md up to date; WARN ok.

Wrapping notes: TESTING.md fix-3 text is rewrapped across lines (content as specified, key phrase kept on one line);
the «Плохо:» line is wrapped at two lines. Brief Q5 (a) wording: "(ratio and door: `docs/TESTING.md` «Бюджет / Объём») with
no reason named — the finding is the missing `tests-over:` line in the commit message".

Siblings noticed: none beyond the spec's list. Needed beyond manifest: none.
