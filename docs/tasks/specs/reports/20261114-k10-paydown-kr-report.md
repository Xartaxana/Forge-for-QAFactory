# K10 pay-down, card KR report

U-CMD output (after K2, identical to the K2 report):
qa-automator 79909
qa-code-critic 72828
qa-test-strategist 53552

Rows (native_headroom, old -> new): qa-automator none -> 79909; qa-code-critic none -> 72828 (TEMPORARY until K1b, fork F-KR); qa-test-strategist 46008 -> 53552.

Price: Codex refuses the role when its project files together exceed 94,400 - U characters: automator 14,491 (framework-rules.md); code critic 21,572 (framework-rules.md); strategist 40,848 (test-strategy.md + project-profile.md).

Witness tails:
- contract_slices.py --check: "slices: 44 declared, all present and fresh; ..." exit 0, no K10 line
- test_contract_slices.py: "=== contract slices ...: 522/522 ok ==="
- test_role_load.py: "=== role_load ...: 186/186 ok ==="
- selftest.py --limits --lang: "=== qa-factory selftest: 4/4 ok ==="

FR walk: A-G not touched (a ratchet value; no text). Slow files: none run. Deviations: none.
