# t-086 PC2-2 report: one release-note reader

## Diff summary
- harness.py: new `release_note(fragment, marker, changelog=None)`. Fragment present -> its text. Else the CHANGELOG.md block (lines up to the next blank line) that carries `marker`. Missing/unreadable changelog or no block -> "". Two blocks -> ValueError naming both line numbers. stdlib only (`Path` already imported), no import-time effect.
- test_codex_tool_guidance.py: `NOTE_MARKER = "A role without Bash is never sent to a command its guard refuses"`; K5 asks the reader, a red check names the fragment and the marker; the `folded or` escape on the heading check is gone; the needle assertions are unchanged.
- test_role_policy_reads.py: `NOTE_MARKER = "The two command guards read a command with one tokenizer"`; same shape.
- Block granularity: both fragments folded into a block of two adjacent bullets (cx1-06: CHANGELOG lines 3320-3342; cx1-5: lines 3668-3681, the second bullet carries SHELL_OPAQUE_BAN and "(CX1-5)"). The needles of each test live across both bullets, so the unit is the blank-line block, not a single bullet. No git history of the fragments exists to compare with (git log of both paths is empty), so the block identification rests on the needles + the "(CX1-5)" tag; flagged for acceptance.
- Model `release_note()` of test_retro_always_full.py is NOT present in this worktree's copy of that file (grep for `release_note` over scripts/tests: only unrelated prose hits); shape written from the spec description. harness.py/story_run_common.py had no changelog helper (grep -i "changelog" in harness.py: none).

## Witness
```
=== test_codex_tool_guidance: 217/217 ok ===
=== test_role_policy_reads: 198/198 ok ===
```
pyflakes on the 3 files: exit 0, no output. `lint_ratchet --check`: 36 findings, 36 in the baseline, 0 new. `dup_ratchet --check`: scripts 9 known 0 new 0 grown; tools 16 known 0 new. `selftest --limits --lang`: PASS limits ... "=== qa-factory selftest: 4/4 ok ===".
scenario_walk --witness-for: harness.py has ~all keep tests as dependants (list printed, >30 rows); not run, judged by CI (the change is one added function). The two own files run above.

## Red probes (byte copy of CHANGELOG.md in the worktree, restored from it)
sha256 before: ad1c4ddb8921a3343ccaeb71f20308403dbe451a9e4c606a3b42fa1f2f308325
```
== probe test_codex_tool_guidance (line with 'A role without Bash is never sent' removed)
FAIL K5 the release note exists (the fragment, or its CHANGELOG.md block) - neither codex-1-cx1-06-no-shell-roles.md nor a CHANGELOG.md block carrying 'A role without Bash is never sent to a command its guard refuses'
... 7 more K5 needle FAILs
=== test_codex_tool_guidance: 209/217 ok ===
sha256 after restore: ad1c4ddb8921a3343ccaeb71f20308403dbe451a9e4c606a3b42fa1f2f308325
== probe test_role_policy_reads (line with 'The two command guards read a command with one tokenizer' removed)
FAIL K5 the release note exists (the fragment, or its CHANGELOG.md block) - neither codex-1-cx1-5-one-tokenizer.md nor a CHANGELOG.md block carrying 'The two command guards read a command with one tokenizer'
... 7 more K5 needle FAILs
=== test_role_policy_reads: 190/198 ok ===
sha256 after restore: ad1c4ddb8921a3343ccaeb71f20308403dbe451a9e4c606a3b42fa1f2f308325
```
`git status --porcelain`: only the three owned files modified (CHANGELOG.md clean).

## FR pass
A - no refusal text changed (test only; the red check names what was not found). B - no text to a person. C - no contract between code and role. D - n/a. E - n/a. F - n/a. G - FR-30 ASCII only in additions; FR-31/FR-18: the check no longer passes on a non-empty CHANGELOG.md.

## Analogs noticed (not fixed)
- test_story_step_materialize.py:557 `folded = not CHANGELOG_FRAGMENT.is_file()` (quarantined, the node's third file; edit forbidden).
- The ValueError-to-red-check try/except is duplicated in the two tests (4 lines each); a third caller would justify moving it into harness.

## Needed beyond the manifest
Reading CHANGELOG.md sections and harness.py head; the two test files' FRAGMENT/imports.
