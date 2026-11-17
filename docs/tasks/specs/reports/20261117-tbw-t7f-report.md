# TBW-T7f report (t-1061) - stage_done census relabel

## Units relabelled (10, all units of `stage_done.py`; census lines 1044-1053)
coerce_value, gate_rehearsal_errors, parse_sets, record_computed_size, refused (selftest helper, note says so),
report_problems, run (its `ref` kept), main, record_acceptance, set_facts.
Each: `roles` -> `["conductor"]`; `note` -> `no agent file and no role-commands entry names stage_done (wave0 §3e trail §T)`
(`refused`: the same plus `; a selftest helper (the inner helper of selftest), not a refusal to a role`). main,
record_acceptance, set_facts had an old T1a note; it was replaced. E1: no unit lacked `roles`/`note` keys other than the
ones that got `note` added (7 had none). class/owner untouched.

## Ceilings (blocking_per_role), old -> new (all 10 units block, so each of the 12 roles loses 10)
qa-automator 137->127, qa-bug-reporter 97->87, qa-case-critic 113->103, qa-case-designer 101->91, qa-code-critic 103->93,
qa-doc-scribe 106->96, qa-failure-analyst 107->97, qa-requirements-tester 118->108, qa-retro-analyst 98->88, qa-runner
108->98, qa-scout 96->86, qa-test-strategist 131->121. conductor stays 748 (unchanged, no raise: the units were already
counted there). No other ceiling touched. E-T4b-1: nothing rose.

## Step 0 (premise, before any edit)
- Grep `stage_done` (case-insensitive) over `ai-packages/qa-factory` with glob `{agents/*.md,skills/**/*.md,**/role-commands*}`:
  0 matches.
- Positive control, same tool and glob shape: `manifest_put` -> 1 file (`references/role-commands.json`); `\.py` -> 49
  matches in that file. So the invocation finds what exists; agents/skills name no scripts by these patterns, and
  `stage_done` is in none of them. No role road found; proceeded.

## Witness
`scenario_walk.py --witness-for scripts/tests/fixtures/judgment-census.json` prints:
```
scripts/tests/fixtures/judgment-census.json: keep test_judgment_census.py (layer register, covers it)
scripts/tests/fixtures/judgment-census.json: keep test_stage_joints.py (layer gate_named, covers it)
```
Both are in `scripts/slow_tests.json` (96.9 s, 259.4 s): judged by the batch canon, not run.
Fast row function instead: `test_judgment_census.analyse(PLUGIN_ROOT, load_census())` (the one scan every C1-C5 test
reads), called alone via a scratch script (not committed).
- BEFORE: `{'C1': [], 'C2': [], 'C3': [], 'C4': [], 'C5': []}`; `census: 280 files scanned, 1264 units; ... breach=0;
  blocks_overrides=10; blocking_per_role: conductor=748 qa-automator=137 ...`
- After relabel, ceilings not yet lowered: C3 lists 12 "`blocking_per_role.<role>` is N, below its ceiling M: lower the
  ceiling to N" (e.g. qa-automator 127 below 137); the numbers above are those.
- AFTER (ceilings lowered): `{'C1': [], 'C2': [], 'C3': [], 'C4': [], 'C5': []}`; `census: 280 files scanned, 1264 units;
  shape=932 xref=214 word-list=0 meaning-proxy=7 meaning=24 safety=87; breach=0; blocks_overrides=10;
  blocking_per_role: conductor=748 qa-automator=127 qa-bug-reporter=87 qa-case-critic=103 qa-case-designer=91
  qa-code-critic=93 qa-doc-scribe=96 qa-failure-analyst=97 qa-requirements-tester=108 qa-retro-analyst=88 qa-runner=98
  qa-scout=86 qa-test-strategist=121; subclass_family=55`. E2: the census accepts a conductor-only unit (C2 empty).

BEFORE and AFTER (identical):
```
stage_joints.py --check: stage joints: walked exit 8, detector 5, window 27 | rows 267, gaps 4 (producer 2, told 1, demands 1), joints held 4 of 267 | role leg not walked (code-to-code rows): 26 | stages with no detector: S0, S1, S6, S7, S9 | told counters: hand_cards 12, legacy_legs 0, unsited 17
stage joints: clean
selftest.py --limits --lang: PASS limits: SKILL.md / agents / references within size caps
PASS limits: every mandatory role rule of design/role-rules.json holds in its carrier
=== qa-factory selftest: 4/4 ok ===
```
No `told_ratchet.unsited` finding line appeared; the told counter `unsited 17` is the same before and after.

## Negative control (byte copy)
Copy taken after the edit: sha256 `0121D3F26FE410864C005EA8AFC7151038CEE3ECD122C1CD82CC7BDF8F029093`. `run` put back to
`["qa-scout", "conductor"]` -> `analyse` C3: "`blocking_per_role.qa-scout` is 87, above its ceiling 86: a ratchet only
shrinks ...". Restored from the copy: hash `0121D3F2...F029093`, equal = True.
(Original file before any edit: `A6612D81...AB55476F`.)

## FR walk
F (measurement): the ceilings are recomputed from the census check's own measure, not estimated; no number reported
as fact without that run. G (code): no code written; the file is JSON, English only, no control bytes; FR-54 siblings:
the other census relabel nodes (T9c, T9a) are separate cards, merge order T4b -> T7f -> T9c -> T9a. A, B, C, D, E: not
applicable (no refusal, text, contract, identity, delivery change).
census: no new blocking unit (1264 units before and after; blocking_units unchanged; breach 0).

## Notes
- Needed beyond the manifest: `test_judgment_census.py` (to measure per-role counts), `slow_tests.json`.
- Analogs noticed: none beyond the 10 units; no other `stage_done` census lines exist.
- Not done: no changelog fragment (per card); no CI; slow files not run.
