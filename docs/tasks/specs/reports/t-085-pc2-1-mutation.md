# t-085 PC2-1 mutation report

Ceiling: ONE product expression, ai-packages/qa-factory/scripts/brief_pack.py:54 `BRIEF_MAX_BYTES = 6 * 1024`; read by the ladder at :4414, :4417, :4442, :4453. Digests-to-side-file and gate-line-fold are both rungs of that one ladder, so there is one mutation, not two. The S5 pins (s5_build_at, test_brief_pack.py:2306) overwrite brief_pack.BRIEF_MAX_BYTES, restore it in finally, and bisect it.

Clean tree: `python -B ai-packages/qa-factory/scripts/tests/test_brief_pack.py` -> `=== test_brief_pack: 882/882 ok ===` (30 s).

Mutation (sed on line 54, rolled back by byte copy):
```
54c54
< BRIEF_MAX_BYTES = 6 * 1024
---
> BRIEF_MAX_BYTES = 6 * 1024 + 1
```
Under mutation: exit 0, no FAIL lines, `=== test_brief_pack: 882/882 ok ===`. NOT red: the S5 AT/BEYOND pins do not bite. No real 6 KB check went red either.

Restore sha256 (copy taken before mutation vs worktree file after restore):
0b1b3b52dfea60fc2f91f1c93991bcbe47ed273253c81485a312e83555006298 *brief_pack.py (worktree, after restore)
0b1b3b52dfea60fc2f91f1c93991bcbe47ed273253c81485a312e83555006298 *brief_pack.orig.py (scratch copy)

Verdict: step 4 case. The pins are self-fulfilling: the ceiling they judge is overwritten and then bisected from the same code, so any value of the product constant passes.

Test NOT edited. Reason (question to Lead): the form step 4 prescribes ("build at the bisected ceiling, assert the relation to 6144") cannot kill. The fixture's bisected ceiling is not 6144 (the fixture sits over it, 6168/6070 per the file comment), and any relation to 6144 at that value would be read off the implementation (FR-58). Requirement-derived candidates:
 (a) value pin: `check_eq("the brief ceiling is the 6144 B of the requirement", brief_pack.BRIEF_MAX_BYTES, 6144)` before the S5 pins. The value comes from finding item 1, not the code. Would be red under the mutation (6145 != 6144; reasoned, not run). Pins the value, not the behaviour.
 (b) behavioural: a fixture whose brief is tuned to exactly 6144 / 6145 B at the real ceiling, assert inline vs side file. Needs a new filler design; a design decision.
Recommendation (a). Not applied because the form of the check is a fork.

FR pass: A-G n/a (no package file edited; report only).

Analogs noticed: the other s5_ceiling users (:2872 digests, :2935 none-yet pop, :2965 gate line) share the same blind spot; one value pin covers all. Lines :770, :873, :1818, :2203-:2254 compare to a literal 6*1024 against budget_bytes: not mutation-sensitive by themselves. Env note: the run prints "references/test-path-markers.json is missing" in the worktree; result unaffected.

## Round 2 (Lead answered: option (a))

Edit, test_brief_pack.py only: one `check_eq("the brief ceiling is the 6144 B of the requirement", brief_pack.BRIEF_MAX_BYTES, 6144)` with a 2-line source comment (finding 20261102 item 1, PC2-1), placed right before `digests_ceiling = s5_ceiling(...)`, the first S5 pin using s5_ceiling.
Edge: `s5_build_at` DOES restore BRIEF_MAX_BYTES in its `finally` (test_brief_pack.py:2306-2312); the earlier 7 KB override in the same scenario also restores in `finally`. So the value read at the check is the original.

Clean: `=== test_brief_pack: 883/883 ok ===`
Mutation `BRIEF_MAX_BYTES = 6 * 1024 + 1` (byte copy kept): exit 1,
`FAIL the brief ceiling is the 6144 B of the requirement — expected 6144, got 6145`, `=== test_brief_pack: 882/883 ok ===`.
Restore sha256 equal: 0b1b3b52dfea60fc2f91f1c93991bcbe47ed273253c81485a312e83555006298 (worktree) == same (scratch copy).
pyflakes: no output (exit 0). lint_ratchet: `36 findings, 36 in the baseline, 0 new`. dup_ratchet: scripts 0 new/0 grown, tools 0 new/0 grown. selftest --limits --lang: `=== qa-factory selftest: 4/4 ok ===`.
git status --porcelain: ` M ai-packages/qa-factory/scripts/tests/test_brief_pack.py`, `?? docs/tasks/specs/reports/t-085-pc2-1-mutation.md` (owned paths only).
