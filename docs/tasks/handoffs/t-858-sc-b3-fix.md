# t-858 sc-b3 fix round - DONE (supersedes the earlier partial)

Worktree C:\QAFactory\forge-repo\.claude\worktrees\sc-b3, branch wip/sc-b3, pushed 030ba406..780c5295 (one commit 780c5295: the merge of origin/main carrying the F2 and F7 edits; no separate fix commit, since the edits were made while the merge was open). No force push.

## Done
- Merge conflict: only `references/role-load.json`. Resolved by taking main's file, then re-measuring with `role_load.py --all --json` on the merged tree. ratchet_tokens: main's rows kept, all within slack, no raise. AR-20 raise, process rows, old -> new: qa-failure-analyst 20204 -> 20262; qa-doc-scribe 18992 -> 19084. Other 10 rows unchanged (equal to the measure).
- F7 (a): scribe Tools line appended "...; an `unresolved` item of the analyst's form naming what it could not use from the run goes there too."
- F7 (b), per Lead's later decision: "...one of the returns item 5 lists, or the unexplained-merge return under «Where bugs hide»; anything else you name in the report." (no second literal of the role-rules anchor; role-rules.json untouched).

## Witness (verbatim tails, run in the worktree)
- test_role_load.py: `=== role_load (the one measure of a role's start load): 186/186 ok ===`
- test_role_rules.py: `PASS shipped register holds in the shipped text` / `=== role rules: 57/57 ok ===`
- selftest.py --lang: `=== qa-factory selftest: 2/2 ok ===`
- `git merge-tree --write-tree origin/main origin/wip/sc-b3` -> prints only tree hash fde404ba5fc872861a28a122f2535ae09d1c91cf, no CONFLICT lines.
- pre-commit hooks passed (piles check ok, indices up to date).

Note: a first run after the F7(b) rewording was 184/186 (scribe process 19,084 vs row 19,085); row lowered to 19084 and re-run green.

Product lines: qa-doc-scribe.md (2 lines), role-load.json (2 numbers). Test lines: none. FR: B/G only (role text, English, selftest --lang ok). Architecture: AR-20 (raise named), AR-10; judgment: none. Axes: not a mechanism. Siblings: none seen. Beyond manifest: role_load.py, role-rules.json (read only).
