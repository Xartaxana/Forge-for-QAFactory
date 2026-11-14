# t-859 report: B1 changelog fragment (F8)

Done: new fragment `ai-packages/qa-factory/changelog.d/consumer-round-cap-is-data.md` in worktree sc-b1; committed daaa9ae8, pushed origin wip/sc-b1.

Claims verified against 104b122a:
- S6/S7 cap 2 -> 1: stages.json adds `acceptance_rounds: 1` to S6 and S7; the old value was DEFAULT_LIMITS `repair_cycles: 2` (runtime_policy.py line 13).
- `repair_cap` is the one reader, called by controller prepare/validate, `cumulative_budget`, `stage_status.round_cap` (status line).
- A project's `limits.repair_cycles` does not lift it: test row "a project's limits do not lift the row" gives 1 with limits repair_cycles 5.
- A person's words lift it: `person_words=True` falls through to the default; the controller passes `person_words` from options. The claim "a person's recorded word still passes the stage" is the existing X2-5 acceptance gate (`_passed_by_person`), only a comment changed in the diff. I worded the fragment as "passes the stage and lifts the cap".
- Malformed row ignored; S4/S5 unchanged: test rows C3, C4, C5.
- Not in the diff and left out: nothing else claimed. The README's `<pile>-<batch>-<slug>` name form was not followed because the dispatch fixed the name.

Witness (inside the worktree, subshell):
`python -B ai-packages/qa-factory/scripts/selftest.py --lang`
```
PASS lang: no Cyrillic anywhere in the package
PASS lang: no control byte left by an eaten escape sequence (FR-29)

=== qa-factory selftest: 2/2 ok ===
```
Fragment form check: `changelog_assemble.py --list` lists `consumer-round-cap-is-data.md` with no REFUSED.
`git diff --cached --stat`: 1 file changed, 5 insertions(+) (the one new file).
Commit hook printed a pre-existing WARN (12 test files matching no feature, door (d)); not caused by this change; commit and push succeeded.

Siblings: none. Needed beyond the manifest: `ai-packages/qa-factory/scripts/runtime_policy.py` (DEFAULT_LIMITS).
