# t-879 landing report (attempt 2)

## Item 1 -- liveness CLI tail (verbatim)
[OK] 16a-handoff_gate-passes-its-own-handoff-path (tools/handoff_gate.py) -- tree unchanged (3 fixture files), no report file written
[OK] 17-journal_hooks-post-agent-writes-delegated (tools/journal_hooks.py) -- delegated t-001 written by the hook
[OK] 18-dod_gate-passing-stop-writes-returned (tools/dod_gate.py) -- delegated, then returned, written once
[OK] 19-journal_hooks-pre-edit-warns (tools/journal_hooks.py) -- {"hookSpecificOutput": {...pre-edit warns...}}
23/23 alive, no silences
SCOPE: code liveness only, not wiring liveness (see module docstring).
OVERALL: OK

## Item 2 done
git rm of both .proposed twins (rc=0). test_mechanism_gate.py: PROPOSED_SETTINGS_PATH removed; closure test is now plain
(single-value parametrize removed); `test_b23_the_live_settings_carry_each_journal_hook_entry_exactly_once` (parametrized over the two entries);
hop_metrics test iterates live only. mechanism_gate.py: two comments reworded.

## Item 3 done
journal_keys.py now holds ID_NUMBER_MAX, ID_GRAMMAR_TEXT, ID_NOT_CANONICAL_TEXT, fmt_id (no other private names needed; no cycle).
journal_write binds the three old names from jk; its not-canonical refusal prints jk.ID_NOT_CANONICAL_TEXT then `; take one from ...`.
journal_validator prints the same constant. Pins in non-owned tests are substring "not canonical" only (test_journal_write.py:266,
test_journal_validator.py:1641-1693) -- still satisfied. piles.py: HAD a copy (line ~3257, the --task grammar text);
replaced with journal_keys.ID_GRAMMAR_TEXT (text identical). New param test in test_journal_keys.py (3 names are the same objects;
fmt_id(7,"")=="t-007", fmt_id(1234,"a")=="t-1234a").

## Item 4 done (docstring only, tools/streams.py)

## Item 5 done
ASSIGN_RE now also strips `export NAME=v;` / `export NAME=v &&` (chained); shape() collapses a bare `export X=y` to `export`
and strips one trailing `;`. Rows added to the existing test_counts transcript/asserts: {"git -C": 4, "export": 1, "ls": 1}.

## DoD run (verbatim tail)
FAILED tools/test_hook_liveness_probe.py::test_fixture_world_10_commands_yields_stale_case_not_case_missing
FAILED tools/test_hook_liveness_probe.py::test_main_cli_json_flag_produces_parseable_json
2 failed, 962 passed, 1 skipped in 176.63s (0:02:56)

Expected red: test_main_cli_json_flag_produces_parseable_json (`23 == 21`, line 1015).
UNEXPECTED red: test_fixture_world_10_commands_yields_stale_case_not_case_missing, tools/test_hook_liveness_probe.py:482
`assert len(ten) == 11` -> 13 == 11: the fixture list _ALL_KIT_COMMANDS now holds 13 after the two journal_hooks entries
were added (previous worker). The file is forbidden to me; likely fix is `== 13` at line 482 (comment at 475-476 "live set is 13" also
stale). Question for Lead.

## git status --short (excluding the compact-snapshots deletions)
 M .claude/settings.json
D  .claude/settings.json.proposed
 M .claude/skills/next-task/SKILL.md
 M .claude/skills/permission-audit/SKILL.md
 M .claude/skills/session-handoff/SKILL.md
 M .githooks/commit-msg
D  .githooks/commit-msg.proposed
 M AGENTS.md
 M CLAUDE.md
 M PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md
 M PROJECT.md
 M docs/DECISIONS_ARCHIVE.md
 M docs/RUNBOOK.md
 M docs/SIBLING_MAP.md
 M plans/piles/forge/README.md
 M plans/piles/forge/batch-7-vhodyashchie-4.md
 M tools/hook_liveness_probe.py
 M tools/install_parity_anchors.json
 M tools/journal_keys.py
 M tools/journal_validator.py
 M tools/journal_write.py
 M tools/mechanism_gate.py
 M tools/piles.py
 M tools/session_retro.py
 M tools/streams.py
 M tools/test_hook_liveness_probe.py
 M tools/test_journal_keys.py
 M tools/test_mechanism_gate.py
 M tools/test_session_retro.py
?? plans/piles/forge/findings/20261116-razgruzka-koordinatora-ostatki-bez-vladeltsa-posle-posadki.md

## Siblings noticed
None beyond the id-grammar copies (piles.py handled). Needed beyond manifest: tools/test_journal_validator.py, test_journal_write.py (pin check), tools/test_streams.py, tools/piles.py, tools/test_hook_liveness_probe.py (read).
