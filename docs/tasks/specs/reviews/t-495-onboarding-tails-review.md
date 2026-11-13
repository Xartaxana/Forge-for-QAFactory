# t-495 — critic, diff gate, topic "onboarding tails" (OF5-7, OF4-19, OF5-10 + OF5-11, integration commits)

Reviewed: `git -C .claude/worktrees/fix-main diff refs/remotes/origin/main...HEAD` (branch fix/main-tests, 14 commits, 24 files, +466/-26).
Rule text: `docs/tasks/critic-diff-brief.md` questions 1-12; specs/DoD as given inline in the dispatch.

## Verdict

**fit_with_fixes** — no blocking (must) findings. Four "should" findings (one test-form defect, one refusal-shape defect on a touched line,
one role-facing card gap with an unsupported test comment, one class-completeness residual to queue) and six notes.
Accepting the work is the coordinator's decision, not mine (critic rule 6).

## Per-node verdict lines

- **OF5-7 (handoff_init `--purpose`, `_door_to`, handoffs.md, census row)** — fit. The DoD is met (23/23 re-run below). The battery covers
  empty, whitespace-only, 64 (AT), 65 and 10000 (BEYOND), non-ASCII, a leading dash (both forms), upper case, and a space. `--contract` wins
  and the purpose is not judged. The door prints `--to X --purpose s5_plan` only for a row found by its purpose. Notes N1, N3, N5, N6.
- **OF4-19 (walk_timing.report, gate_brief._proved_warnings through project_for_task)** — fit. 8/8 re-run. An unresolvable root keeps the
  old outcome (`{}` / every line stays), and no new refusal is added. Should S4 (siblings to queue). Notes N2, N4.
- **OF5-10 (card `manual_evidence.py validate`, registry test over manual-evidence.md)** — fit. The card's claims are checked: exit 0 +
  `"valid": true`; exit 1 + `"valid": false` for a record with a field missing. The census rows (B13, file) exist; battery row B13 is at
  test_validator_class.py:185.
- **OF5-11 (RefusingParser in five CLIs)** — fit_with_fixes. Exit 2 is kept, and no call that was accepted before is now refused:
  RefusingParser overrides only `error()`, and `exact_options`/abbreviation behaviour is unchanged. Shoulds S1, S2, S3.
- **Integration commits (features.json, test-layers covers, `__main__` entry, role-load raise)** — fit. The ratchet raise is named row by
  row (below).

## Findings

**S1 (should, fix before merge) — the bare-parser guard is a source pin and carries a negative control inside a test.**
`ai-packages/qa-factory/scripts/tests/test_role_commands.py:999-1019` (`bare_parser_table`, second half) reads every carded script's
`.py` source for the token `ArgumentParser(`. It also self-checks that reading against an inline sample (lines 1013-1017). The control
tests a *copy* of the predicate, not the code that runs, so it proves nothing about the guard.
`docs/TESTING.md:94` ("Пин исходника": a regex counted in code → a line in a shared structural ratchet, not a per-node test) and
`:98` ("Отрицательный контроль внутри теста" → nothing) put both forms on the "not written" list. Brief question 5 makes them a finding.
Expected: move the bare-parser count into one shared structural ratchet (e.g. beside `dup_ratchet`/`lint_ratchet`), or keep it only as a
shrink-only allow-list row there. Delete the self-control lines in either case. The behavioural table (lines 965-997) is fine and stays.

**S2 (should, fix before merge) — red_sandbox's refusal opens with the whole module docstring as "usage".**
`ai-packages/qa-factory/scripts/red_sandbox.py:2231`: `role_cli.RefusingParser(__doc__, command=...)`. The first positional argument of
`ArgumentParser` is `prog`, so the docstring becomes the program name. The quirk existed on main, but this diff rewrote the line and kept it.
Reproduced: `CLAUDE_PROJECT_DIR=<tmp> python -B scripts/red_sandbox.py --diagnostic` → exit 2, **63 lines** of output. It starts
`usage: Prepare an isolated exact-byte test tree; ...` (the full docstring), and the card ("what to write: --diagnostic --repo ...") comes
only in the last 4 lines. A role pays ~55 lines of noise before the door (FR-1 is still met, but AR-12 friction applies).
Expected: `RefusingParser(description=__doc__, command=..., ...)`, which gives the standard prog `red_sandbox.py`.

**S3 (should; fix now or queue with a node) — grounding_section.py is handed to a role but has no card, and the test claims the gap is named.**
`guard_pre_tool.py:821-823` hands a role, in the big-read door, either `plan_row.py --show ...` or `grounding_section.py --show ...`.
`role-commands.json` has a card for `plan_row.py` (grep: `"plan_row.py"`) and none for `grounding_section.py`. After this diff a usage
error of grounding_section ends with "no command card is registered ... `--help` of the script lists every registered shape". But its
`--help` epilog is empty (`role_cli.epilog` returns "" when no row exists, role_cli.py:64-71), so that door points at nothing extra.
The comment at `test_role_commands.py:979` says "(the registry test names the gap)", but no test does. Search trail: `grep -rln
grounding_section scripts/tests/*.py` → test_artifact_sections, test_grounding_section, test_guard_big_read_sections, test_role_commands,
test_task_root_parents. Within test_role_commands the only mentions are lines 960/979-981, all in this new table; `grep -niE "no card|NO_CARD|uncarded"` found
no registry list. The finding `plans/piles/onboarding-forge/findings/20261113-skripty-s-kartoj-na-golom-argparse.md:8` assumed the
script *had* a card. Also, the new guard only scans scripts that have a card, so grounding_section going back to a bare parser would not
be caught.
Expected: a card `grounding_section.py` (the twin of `plan_row.py`, AR-8/AR-19), or a node row with its owner. Correct the comment at :979 either way.

**S4 (should; queue — class completeness, rule 9 / brief q.4) — depth readers missing from the known list.**
The dispatch's known list (`branch_accounting.py:486, traceability.py:1837, report_facts.py:127, walk_timing.py:216`) was gathered by a
`parents[` grep. The same class written as `.parent.parent` escaped it:
- `scripts/s5_precheck.py:3501` `project_integrations`: `config = _load(task_root.parent.parent / "config.json")`. This is the project config
  read by folder depth, the exact twin of the `walk_timing.report` line OF4-19 fixed. A story under a configured `artifact_root` reads no
  (or a wrong) config here.
- `scripts/judge_diff.py:70` and `scripts/judge_results.py:278`: `nearest_project(...)` with a depth fallback `task_root.parent.parent`.
  These are the same shape as branch_accounting:486 / traceability:1837, which are on the list.
Search trail: `grep -rnE "\.parent\.parent\b" scripts/*.py | grep -v /tests/ | grep -v __file__`. The positive control is the same tool,
which found the known `handoff_init.py:311`. The other hits are story-relative layouts (`<story>/work/...`, `<story>/state/...`), not
project-by-depth.
Expected: Остатки lines `s5_precheck.project_integrations reads config by depth | узел: <id>` and `judge_diff:70, judge_results:278 depth
fallback | узел: <id>` in an untaken onboarding-forge batch (brief q.4 form). The Lead opens the node.

**N1 (note) — stale numbers in a commit message.** 56481ca says "conductor is 477 vs ceiling 476". Those are the wip-base numbers. The
raise that actually landed (680 → 681) is named in merge 6bdde0e: `judgment: adds data check handoff_init.clean_purpose --
blocking_per_role.conductor 680 -> 681 (AR-20 raise named by the Lead)`. The raise is honestly named at the point it lands.

**N2 (note) — gate_brief: one behaviour change in the safe direction, without a test row.** Before, a story at
`<p>/qa-factory/artifacts/<T>` whose project has **no** `qa-factory/config.json` used `parents[2]` evidence and could lift lines. Now
`project_for_task` refuses (`_admits`, runtime_paths.py:776), and every line stays. This is AR-28's allowed error, and a factory project
always has a config, so "unchanged for the standard layout" holds for real projects. On that road `hooklib.project_root()` may shell out to
git (runtime_paths.py:819-820 says up to 10 s) in both readers.

**N3 (note) — handoff_init.py.** (a) :394: a valid word with a leading or trailing space gets the hint "with no space inside", which is not
quite true. (b) `known_purposes_note` (:401-411) repeats the row filter of `handoff.contract_of` (handoff.py:367-372: stage-or-gate +
from). A `handoff.purposes_of(stage, role)` beside `contract_of` would keep one reader of that predicate. Queue or leave.

**N4 (note)** — `test_project_for_task_readers.py:89,115`: `cwd0`/`os.chdir(cwd0)` is dead (nothing changes cwd).

**N5 (note)** — the `test-layers.json` row `test_handoff_init.py` covers `handoff.py`, `handoff_init.py` and `tests/harness.py`. The door
table also drives `handoff_check._door_to`, but `handoff_check.py` is not listed.

**N6 (note)** — the unknown-purpose refusal (handoff_init.py:453-460) still ends "A handover without a contract is a gap of the factory:
add the row and the file". For a role's typo that sentence misleads. The known purposes printed before it give the right door.

## Standing questions

- **1 Fit** — see the per-node lines.
- **2 Builder's own decisions** — whitespace-only reads as none; `--contract` skips the purpose check; the refusal goes to stdout like the
  existing `no contract` line. All three are in the safe direction.
- **3 Seams** — additive. `handoff_check._door_to` adds one branch after the two existing ones, and no order changes.
- **4 Class completeness** — S4. The OF5-11 class (carded scripts on a bare parser) is closed by the guard, with critic_rollcall
  allow-listed with a reason. Cardless twins: S3. OF5-10: `manual_evidence.py <sub>` handed by `manual-evidence-app.md`,
  `explore-charter.md`, `agents/`, `phases/` → only `build`, which has a card (grep trail in the Trail section).
- **5 Tests** — S1. The other new tables are one parameterised table per behaviour, and red lines name their row.
- **6 DUPLICATION AND CONSISTENCY** — N3(b) only. The try/`except ValueError` around `project_for_task` matches 7 existing callers
  (`grep -A2 "project_for_task(" | grep -c "except ValueError"` → 7 of 21 call lines). RefusingParser is reused, not re-implemented.
  clean_purpose has no existing twin: `grep -rnE "PURPOSE|purpose.*re\.(compile|fullmatch|match)|--purpose"` finds `controller.PURPOSES`,
  a closed set of dispatch words, and handoff_init checks the index rows instead, which is the authority for contracts.
- **7 CODE QUALITY** — no new function over 60 lines (`bare_parser_table` is ~62 lines, mostly table rows; acceptable). S2 is a misleading
  call on a touched line. N4 is dead code.
- **8 Hygiene** — no non-ASCII added in the package diff (`grep -cP "[^\x00-\x7F]"` → 0; positive control on a Cyrillic sample → 1). The
  Cyrillic test value is built from code points.
- **9 IN-TREE RATCHETS** — named row by row. (a) `judgment-census.json` `blocking_per_role.conductor` 680 → 681, from the new row
  `handoff_init.py::clean_purpose` (shape, data), named in merge 6bdde0e, Lead decision, AR-20. (b) `role-load.json`
  `qa-failure-analyst` ratchet 18361 → 18426 and process 16322 → 16401, cause TR4-15 (on main in wave 21, commit 1d36f5a), named in
  c9f6e02. test_role_load re-run 171/171. No other ratchet changes.
- **10 ARCHITECTURE** — the commits name AR-9/AR-22 (OF5-7), AR-4/AR-13/AR-15 (OF4-19), AR-8/AR-22 (OF5-10) and AR-9/AR-15 (OF5-11).
  AR-13 holds for the two converted readers; AR-13/AR-15 residuals are listed in S4. AR-20: see q.9. FR-1/FR-2: every new refusal names
  what is wrong and what is expected, and its door is a usable flag (the exception is S3, where the door is empty). FR-46: a call error
  stays exit 2 as a refusal of the call. FR-38: `--purpose` is told in handoffs.md:15 and `--help`.
- **11 JUDGMENT** — one census row added, `clean_purpose` as shape/data: length and charset of a CLI flag value, no role wording. The class
  is honest. No `blocks_override`, no scan-constant edit, no craft marker. The `judgment:` lines are correct.
- **12 ONE ROAD** — none found. I read the whole diff for language, runner or project-name branches, and there are none. The only
  conditional road is "no project holds the story", which reaches the shared resolver first.

## Re-runs (verbatim tails)

```
( cd .../fix-main/ai-packages/qa-factory/scripts && python -B tests/test_handoff_init.py | tail -n 3 )
PASS door: a two-contract stage form (S4 secondary) still prints --to alone
=== handoff_init purpose: 23/23 ok ===
python -B tests/test_project_for_task_readers.py
PASS gate_brief: outside any project: the line stays, nothing is asked
=== test_project_for_task_readers: 8/8 ok ===
python -B tests/test_judgment_census.py
PASS test_blind_spot_states_the_subclass_clause
=== judgment_census: 24/24 ok ===
python -B tests/test_role_load.py
PASS K10-a: qa-failure-analyst: craft + process == tokens (the shipped numbers)
=== role_load (the one measure of a role's start load): 171/171 ok ===
```

The five CLIs were run with bad calls (`CLAUDE_PROJECT_DIR=<tmp>`), every one exit 2 with no traceback:
- `case_versions.py`: usage + "no command card is registered" + "the following arguments are required: --task-root".
- `case_versions.py --task-root T`: "provide --case-file, --cases-dir, --all or --pin".
- `manifest_put.py` / `--recover`: usage + no-card line + its own `ap.error` sentence.
- `execution_fingerprint.py`: usage + "required: spec" + the card "what to write: the ONE argument is a path ...".
- `grounding_section.py`: usage + no-card line + "required: --task".
- `red_sandbox.py --diagnostic`: 63 lines with the card in the last 4 (S2).

## Not checked

- I did not re-run `test_role_commands.py` (963), `test_validator_class.py` (51), `test_gate_brief_and_retro.py` (975),
  `test_audit_rules.py` or `selftest --limits --lang`. I took them from the attached layer and the CI run 43450623643 (package-fast/full/
  install-smoke green on c9f6e02). Full selftest, install_smoke and test_quarantine were not run, per the dispatch.
- I did not measure whether the role-load raise is tight to the byte. test_role_load passes and the commit says "tight".
- I did not check the census `roles` list of `clean_purpose` (["conductor"]) against who actually runs handoff_init. It matches the
  existing `handoff_init.py::task_root` row.
- I did not review commits already on main (waves 16-21).

## Trail

Read: the full diff of the branch; runtime_paths.py:193-213, 768-850, 920-927; handoff.py:354-380; role_cli.py:64-112, 134-164;
hooklib.py:583-594, 772-800; handoff_check.py:2975-3010; handoff_init.py (diff, :379-460); guard_pre_tool.py:812-826;
s5_precheck.py:3497-3510; judge_diff.py:62-72; judge_results.py:270-279; controller.py:53-58; walk_timing.py:214-218;
test_validator_class.py:171-185; docs/TESTING.md:89-99; critic-diff-brief.md; SIBLING_MAP grep (rows 209, 214);
commit messages 56481ca, a7710b4, 4fffe52, a074794, 9fa78b5, 6c75984, c9f6e02, 6bdde0e, 41bdeab.
Searches: `parents\[` and `\.parent\.parent` over scripts/*.py (see S4); `grounding_section` over tests (S3);
`manual_evidence\.py [a-z]` over references/agents/phases; purpose-word checks; non-ASCII in the diff.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "OF5-11 class closed by the new guard for carded scripts; cardless twin grounding_section.py (handed by guard_pre_tool.py:821-823 beside carded plan_row.py) left open (S3). OF4-19: depth readers outside the known list - s5_precheck.py:3501 (config by depth, twin of the fixed walk_timing line), judge_diff.py:70 and judge_results.py:278 (nearest_project + parent.parent fallback) - to queue as Ostatki lines with a node (S4). OF5-10: every manual_evidence.py subcommand handed by references/agents/phases has a card.",
  "trail": {
    "read": [
      "git diff refs/remotes/origin/main...HEAD (fix-main worktree, 24 files)",
      "ai-packages/qa-factory/scripts/runtime_paths.py:193-213,768-850,920-927",
      "ai-packages/qa-factory/scripts/handoff.py:354-380",
      "ai-packages/qa-factory/scripts/role_cli.py:64-164",
      "ai-packages/qa-factory/scripts/hooklib.py:583-594,772-800",
      "ai-packages/qa-factory/scripts/handoff_check.py:2975-3010",
      "ai-packages/qa-factory/scripts/handoff_init.py:379-460",
      "ai-packages/qa-factory/scripts/guard_pre_tool.py:812-826",
      "ai-packages/qa-factory/scripts/s5_precheck.py:3497-3510",
      "ai-packages/qa-factory/scripts/judge_diff.py:62-72",
      "ai-packages/qa-factory/scripts/judge_results.py:270-279",
      "ai-packages/qa-factory/scripts/tests/test_validator_class.py:171-185",
      "docs/TESTING.md:89-99",
      "docs/tasks/critic-diff-brief.md",
      "docs/SIBLING_MAP.md (grep rows 209, 214)",
      "commit messages 56481ca a7710b4 4fffe52 a074794 9fa78b5 6c75984 c9f6e02 6bdde0e 41bdeab"
    ],
    "reruns": [
      {"command": "python -B tests/test_handoff_init.py", "result": "handoff_init purpose: 23/23 ok"},
      {"command": "python -B tests/test_project_for_task_readers.py", "result": "test_project_for_task_readers: 8/8 ok"},
      {"command": "python -B tests/test_judgment_census.py", "result": "judgment_census: 24/24 ok"},
      {"command": "python -B tests/test_role_load.py", "result": "role_load: 171/171 ok"},
      {"command": "python -B scripts/red_sandbox.py --diagnostic (CLAUDE_PROJECT_DIR=tmp)", "result": "exit 2, 63 lines, usage is the whole module docstring, card in last 4 lines"},
      {"command": "bad calls of case_versions, manifest_put, execution_fingerprint, grounding_section", "result": "each exit 2, no traceback, usage + card or no-card line + argparse sentence"}
    ]
  },
  "fixes": [
    "S1 test_role_commands.py:999-1019 - bare-parser source scan is a source pin with an in-test negative control (TESTING.md:94,98): move to a shared structural ratchet, drop the self-control",
    "S2 red_sandbox.py:2231 - RefusingParser(__doc__, ...) makes the docstring the prog; use description=__doc__",
    "S3 grounding_section.py has no card though guard_pre_tool.py:821-823 hands it to a role (twin plan_row.py is carded); add the card or open a node; correct the unsupported comment test_role_commands.py:979",
    "S4 queue as Ostatki lines with a node: s5_precheck.py:3501 config by depth; judge_diff.py:70 and judge_results.py:278 depth fallback"
  ]
}
```
