# tbw fix round (t-787) - B1, F1, F2, F3, F4

Worktree `.claude/worktrees/tbw-t1r`, branch `wip/tbw-t1r`, from 60ddb66d plus `git merge origin/main`.

## Merge from main
Two conflicts, both in generated/data files, no source file:
- `references/role-load.json`: the `ratchet_tokens` / `process_ratchet_tokens` blocks. Resolved by taking the branch block (it carries `native_headroom`), regenerating the slices after the merge, then setting every row to the measure (`role_load.py --all --json`, script in the scratchpad, not committed). Rows that ROSE against the branch (all from main's charter/common changes, named, AR-20): ratchet_tokens requirements-tester +43, test-strategist +63, case-critic +492, code-critic +22, failure-analyst +29; process_ratchet_tokens requirements-tester +43, test-strategist +12, case-critic +506, code-critic +22, failure-analyst +29. The rest fell by 2-7. Slack-0 process rows equal the measure.
- `judgment-census.json`: the `ratchet` line. Took main's line (bug-reporter 153, case-critic 173, conductor 764) with the branch's two narrowings kept (152, 172); conductor stays at main's 764, which is the F4 restore (main's number includes +3 of its own, the branch's 760 was 761 less the conductor row).

## B1
`stage-joints.json` row `run_suite:phantom_story`: `stages` S5 -> S5,S6,S7 (union of `stage_guard.stages_of_role` over the 4 roles: automator S5, code-critic S5, runner S6, analyst S7). Producers split: automator + runner `{"page": true, "call": true}` (road `run_suite` proved F in S-1b; automator's other road `import_test_receipt` carries only `validate_request` ids); code-critic + failure-analyst `{"page": true}` (red_sandbox / probe_by_code unproved). `test_contract_slices.py` `counted` runner (10,2) -> (10,3) (runner now has phantom_story told at the call). `T1rs/marked-by-proof` data row already recomputes this per (row, role) from the proof constants and passes.
K5 probe (read-only, `scratchpad/k5probe.py`, source below the witness): output `UNITS 14 MISSING []`; `run_suite.py::_refuse_phantom_story ids=1 census_roles=4 missing=[]`.

## F1
Doors/texts with a code line number found by grep (positive control: the two known doors matched, count 2): `handoff_check:cli` door `(:3040-3041)`, `execution_request:profile` door `:1707-1708, :1728`, and two siblings in the same file: `run_suite:recover` door `run_suite.py:3026-3027`, and the `requirement` of the S3 exit-kinds row `(the messages :1786-2035 ...)`. All four dropped; `--write` regenerated the pages. Test row `T1r/no-code-line-number` (`test_contract_slices.py`, `test_pages_carry_no_code_line_number`): every generated key page against `:\d{3,4}`, fails naming page:line; control: the pattern finds `(:3040-3041)`. False hits: none (the row is green on the real pages), so the pattern stands as written.

## F2
`stage_joints.told_line`: adds "." only when `expected.rstrip()` is non-empty and does not end in `.`, `!`, `?` (a backtick or closing bracket gets the stop after it). Rows in `renderers()` of `test_stage_joints.py` (never run): no stop / backtick / bracket / `!` / trailing blanks after `.` / a carrier row renders `...x. Door: d.`. The empty-`expected` case cannot be reached through `told_text` (an unreadable row says so in words), so only the code guard states it, no row.

## F3
`contract_slices.catalogue`: the `keys_targets` loop removed (key pages are inline in every mode). Row `X1-7` flipped to `check_not_in`. A role with no key page: unchanged output.

## F4
Census row `exit_gate.py::required_outputs_errors`: `conductor` back in `roles` (note says so). Ceiling: 764 (main's). `test_judgment_census.py`: 23/25; both FAILs are on origin/main too (verified in the wave13 worktree, identical output): `test_c1` six stale rows `exploratory_findings.py::_check_probe/_closed/_judge_refs/_link/_nested_keys/_origin` and `test_c3` "conductor is 758, below its ceiling 764". Not this topic's; not touched.

## Witness block (verbatim, from the final run)

```
$ python -B scripts/tests/test_contract_slices.py   (cwd ai-packages/qa-factory)
=== contract slices (markup, generation, freshness, shipped map): 458/463 ok ===
FAIL rows (all K10 = B2, not this round): T3a (h) / T3a (j) / keys/findings-clean / SHIPPED / CLI
  (each carries "K10 qa-test-strategist: the plugin share is 55,976 bytes, over ... baseline 46,008 ...")

$ python -B scripts/contract_slices.py --check   (only K10 findings)
SLICE: K10 qa-test-strategist: the plugin share is 55,976 bytes, over its native-context headroom 42,400 ... and over its baseline 46,008 ...
SLICE: K10 qa-automator: the plugin share is 81,385 bytes, over its native-context headroom 68,400 ... and over its baseline none ...
SLICE: K10 qa-code-critic: the plugin share is 74,417 bytes, over its native-context headroom 68,400 ... and over its baseline none ...

$ python -B scripts/stage_joints.py --check
stage joints: walked exit 8, detector 5, window 27 | rows 267, gaps 4 (producer 2, told 1, demands 1), joints held 4 of 267 | ... told counters: hand_cards 12, legacy_legs 0, unsited 119
stage joints: clean

$ python -B scripts/tests/test_judgment_census.py | tail -1
=== judgment_census: 23/25 ok ===      (2 FAILs identical on origin/main, see F4)

$ python -B scripts/selftest.py --limits --lang
=== qa-factory selftest: 4/4 ok ===

$ python -B scripts/tests/test_role_load.py | tail -1
=== role_load (the one measure of a role's start load): 186/186 ok ===

A22 findings (audit_factory._a22_findings): errors [] (info lines only)

$ python -B scratchpad/k5probe.py | tail -1
UNITS 14 MISSING []
```

K10 numbers (bytes, after the merge): strategist 55,976 (+252 vs the critic's 55,724, from main's charter), automator 81,385, code-critic 74,417 (+90 vs 74,327). Failure-analyst and runner stay under H. B2 untouched; no baseline raised, no page row cut.

Slow files not run: test_stage_joints.py (rows edited: F2 told-line/stop), test_audit_rules.py, test_hooks_wiring.py, test_brief_pack.py: judged by the batch canon.

K5 probe source: scratchpad `k5probe.py` (read-only join of `SJ.check_ids()` ER/RS ids, `judgment-census.json` roles minus conductor, and `SJ._row_names` over the rows that state a requirement).

## Review lines
FR pass: A - the requirement reaches code-critic/failure-analyst/runner/automator for the phantom-story refusal; no door changed except dropping line numbers. C - FR-38 kept; FR-37: catalogue no longer names the in-prompt pages. G - code touched is `told_line` and `catalogue` only; English only (`selftest --lang` 4/4).
architecture: AR-10, AR-18, AR-20 -- the requirement reaches every role that meets the refusal; one rendered sentence; the census ceiling restored
judgment: none -- rows, markers and rendered text only

Siblings noticed: (1) the F1 sweep found two more line numbers in stage-joints.json (run_suite:recover door, S3 exit-kinds requirement), fixed here. (2) census test_c1/test_c3 are red on main itself (exploratory_findings rows, conductor 758 vs 764): a main defect, not queued by this round. (3) No changelog.d fragment added (rows/text only).
