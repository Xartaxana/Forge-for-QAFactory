# C3-b2 (t-1080, rules-debt/1/RD1-5) - test_identity through the predicate - report

Status: NOT COMMITTED. Stopped on ONE question (below): the card's item 1 + item 7 measurement is contradicted by the code. Everything
else of the card is implemented in the worktree `C:/QAFactory/forge-repo/.claude/worktrees/agent-a792e825fd0ee2fb6` (branch
`worktree-agent-a792e825fd0ee2fb6`, base `e6961849`), uncommitted, and the tree is RED on A26 by exactly the two findings of the question.

## The question (card fact contradicted by the code)

Card item 7: "`_run_freshness:939` is not counted after the change (its literal is gone)"; D13 expected +2 triples (`same_test`,
`_evaluate`), count +2 from the base. Measured (`GR.analyse`, base 145 items / 49 triples, after the card's items 1-6):

    findings 2, items 149, triples 52; test_identity triples: _evaluate, _run_freshness, already_probed, same_test

Cause: F-T1 (a) adds the word `unknown` to the row's `words`; `_run_freshness` is now a registered accept site, and its two
`return "unknown", ...` tuples (`proof_level.py:973` `('unknown', WHY_RUN_NO_IDENTITY)`, `:980` `('unknown', why or WHY_RUN_NOT_COMPARED)`)
are counted as hidden token sets: A26 F-a "in no registered gate" (not allowed, the site is converted accept). They are the freshness STATE
the function returns (E4: run rows without both shas stay `unknown`), not an acceptance. The card says "a different measurement is a stop and
a question", so nothing was decided.

Options (measured, not applied to the tree):
- (A) two `allow` entries on the `_run_freshness` site, the WHOLE tuple texts above, why "the freshness state the function returns, not an
  acceptance". Probed on a scratch COPY of the tree (`.../scratchpad/probeA`): `gate_registry.py --check` -> "no violations", 0 findings;
  D13 = 149 items / 52 triples, i.e. +4 items, +3 triples from the base (card said +2 / +2): the extra triple `("proof_level.py",
  "_run_freshness", "test_identity")`, 2 extra items. Needs a D13 comment line `145 -> 149 (C3-b2, t-1080)` naming them.
- (B) change the code so the tuples hold no row word (e.g. return a named constant): a code-form change in `_run_freshness`, not in the card.
- (C) drop `unknown` from the row's words: contradicts F-T1 (a).
Recommendation: (A). Also confirm the pins: `D13_TRIPLES` + `_run_freshness`, `D13_ITEM_COUNT = 149`.

## What is done (uncommitted)

1. `references/gate-registry.json`, row `test_identity` only: `same_test` re-roled `produce`; `green_over_same_bytes` re-roled `validate`
   (F-T1 (a)); new sites `_product_receipt_repeat`, `_run_freshness`, `_evaluate` (accept), `_stale_receipt` (produce); `already_probed` and
   `_evaluate` carry one `allow` each (`hit['holds'] in ('instance_code', 'file_code')`, `how in ('instance_code', 'file_code')`); words gain
   `same` (matched), `different` (mismatched), `unknown` (unknown, owner environment); `accepts`: `probe_repeat`, `run_reuse`, `run_fresh`,
   `receipt_holds` = `["matched"]`; `status: converted`, `debt_ref: ""`. Leaves the debt block (5 left).
2. `proof_level.py`: import `from gate_template import acceptable, registry_problem`; `already_probed` two reuse tests (probe record
   `no_failure`/`wrong_location`, product record `survived`) and `_product_receipt_repeat` call `acceptable(same_test(...),
   "test_identity.probe_repeat")` after the verdict check and before `_mutated_files_hold` (E2); `_run_freshness` calls `acceptable(...,
   "test_identity.run_fresh")` after the file/identity/measurement checks (E7), and on False with a non-empty `registry_problem()` returns
   `stale` with `WHY_RUN_REGISTRY` ("the gate registry cannot be read (<reason>): a factory defect, not a change of the test"); `_evaluate`
   calls `acceptable(how, "test_identity.receipt_holds")` and, on a non-empty `registry_problem()`, says `WHY_RECEIPT_REGISTRY` instead of the bytes
   sentence (the `: probe the current bytes again ...` suffix is kept). Not touched: `holds_over_comments`, `_stale_receipt`, the `holds` display
   recomputes, the receipt path of `already_probed`.
3. `execution_request.py`: `from gate_template import acceptable, registry_problem` (module level, beside the hooklib import; no cycle: gate_template
   -> gate_registry -> hooklib); `_match` (with `import proof_level` at the top of the function) calls `acceptable(proof_level.compare_identity(a,
   b)[0], "test_identity.run_reuse")` inside the same `author_run_reading != "per_story"` condition, after the `identical` short-circuit (E1); on a
   non-empty `registry_problem()` the why is "the gate registry cannot be read (<reason>): a factory defect, the earlier run was not judged", rank
   `bytes` in both cases. The `same_instance_bytes` docstring sentence names its one caller `_same_identity_for_count` and says `_match` reads
   `compare_identity` through the predicate (R14); its code is untouched.
4. Test rows, all in the existing files, expectations from the card / row `decides`: `test_proof_level.py` one function
   `c3_b2_a_reuse_is_accepted_through_the_registry_row_and_an_unknown_runs_again` (item 2: `no_failure` and `survived` records, same bytes vs other
   bytes vs unreadable registry; item 3: product record + holding receipt, same vs other bytes vs registry, direct and via `already_probed(kind=product)`;
   item 6: receipt of other code, same receipt under an unreadable registry -> not valid and the issue names the registry, not "other bytes"; controls
   beside every refusal). `test_execution_request.py` `c3_b2_match_reads_the_identity_through_the_registry_row` (item 5 (i), (ii), control, no identity,
   E1 short-circuit under an unreadable registry). `test_run_freshness.py` one row K1 (p) (registry unreadable -> stale, why names the registry, not
   "changed since"; control fresh again). The existing pins K1 (b) :80-86, K1 (f) :104-106, K1 (d) :92-98 are named and got no new row (S-b). Item 6's
   "other code -> not valid" is also already pinned at `test_proof_level.py` "an assert changed: not reached" (comment_only_changes_keep_the_receipt); my
   row repeats it as the control of the registry row (card item 6 lists two rows).
5. S-f pins in `test_gate_registry.py` (deltas from this base): `EXPECTED_DEBT` loses `test_identity`; `EXPECTED_CONVERTED` gains it; K-T1.2 "6" -> "5";
   K-T1.14 text and split 21/6/6 -> 22/5/6 (AR-20 comment line); F4 unchanged (row already `code`); `D13_TRIPLES` gains `_evaluate` and `same_test` (the card's
   two); the allow-list pin "S1's data-seed shape check is the one allow entry" extended with the two new allow entries (a pin the card did not name; it
   follows from item 1's allow entries). NOT moved, pending the question: `D13_TRIPLES` `_run_freshness`, `D13_ITEM_COUNT` (145 now; measured 149), its comment.
6. `changelog.d/rules-debt-c3-b2-test-identity.md`: one English ASCII bullet.

## Witness (verbatim tails)

`python -B ai-packages/qa-factory/scripts/gate_registry.py --check` (RED, the two findings of the question; `test_identity` is already absent from the debt block):

    A26 gate registry: VIOLATIONS (2)  owner: factory
    - proof_level.py:973 (_run_freshness): the verdict token set `('unknown', WHY_RUN_NO_IDENTITY)` is in no registered gate ...
    - proof_level.py:980 (_run_freshness): the verdict token set `('unknown', why or WHY_RUN_NOT_COMPARED)` is in no registered gate ...
    5 gate(s) left as debt:   (stand_identity, provenance_acceptance, s5_window, baseline_identity, s5_stand_limits)

Own tests (cwd = scripts/tests, `python -B <file>`):
- test_proof_level.py: `=== test_proof_level: 627/627 ok ===` (the new rows: all PASS, e.g. `PASS item 6 (E8): ...and the issue names the registry`)
- test_execution_request.py: `=== test_execution_request: 667/667 ok ===`
- test_run_freshness.py: `=== run freshness: 100/100 ok ===`
- test_judgment_census.py: `=== judgment_census: 25/25 ok ===` (no census row moves, no refusal site added)
- `selftest.py --limits --lang`: `PASS limits: ...` `=== qa-factory selftest: 4/4 ok ===`
- test_gate_registry.py: `483/497 ok`; the 14 FAILs are ALL consequences of the two A26 findings (K-T1.1 "live registry is clean", K-T1.2/K-T1.14 exit and
  first line, "every comparison is attributed", F1 and K-N2.12 NEG "exactly one finding" -> 3, D13 set/count/NEG) plus the D13 pins pending the question.
  Control: the BASE tree (`git archive HEAD` into the scratchpad) runs `=== test_gate_registry: 493/493 ok ===`.

Negative control (on a scratch COPY, hygiene 7d; the live tree was not corrupted): in the option-A probe copy `_product_receipt_repeat`'s `acceptable(...)`
reverted to the bare `same_test(...)` -> `gate_registry.py --check` exit 1: "test_identity: converted accept site proof_level.py:_product_receipt_repeat calls no
acceptable() ...". The same copy before the revert: "A26 gate registry: no violations", 0 findings (so (A) turns the registry check green).

NOT RUN (pending the answer, the tree being red): `scenario_walk.py --witness-for <owns>` (its printed list is large: covers of `proof_level.py` and
`execution_request.py` pull dozens of keep files) and each printed non-slow file alone; `test_stage_joints.py`; the green `--check`. They run once after the
question is settled.

## FR walk (touched sections)

A - refusals: unreadable registry refuses the reuse (cost, never a pass); the why names the registry and is a factory defect, not a person's choice (FR-1, FR-3,
FR-4 not applicable: no new refusal site, no person gate). B - text a person reads: the three new whys are the one family "the gate registry cannot be read
(<reason>): a factory defect, ...", no script, no question (FR-6 holds). C - contracts: every consumer is fed by exactly one producer (E11): `probe_repeat`,
`run_fresh`, `receipt_holds` <- `same_test`; `run_reuse` <- `compare_identity` (FR-14 shape unchanged). D - identity: the identity words are read through the
one predicate (FR-17/AR-13); FR-40 n/a. E, F - not touched (FR-41: the registry why never claims a change). G - English ASCII, no heredoc code (FR-29/30), tests
are rows of existing files (FR-32).

## Siblings, analogs, R12

- axis 5 prose twins, grep `instance_code|file_code|same_test|compare_identity` (-i -E, positive control `person_confirmed|probe` found 8-37 hits per file) over
  `references/execution-lifecycle.md` + both slices (`slices/qa-automator`, `slices/qa-code-critic`), `manual-evidence.md`, `environment-preparation.md`,
  `skills/qa-story/phases/s5.md`, `s6.md`: ONE hit, `s5.md:193` (`instance_code_sha`, "Staleness is per test function"): checked, no edit (meaning unchanged: the
  sha name, not a row word). All other files: no hit.
- Analogs noticed, NOT fixed (outside owns): `same_test` truthiness read outside the row's sites: `acceptance.py:176` (`!= "raw"`), `acceptance.py:210` (bare
  truthiness), `window_record.py:1906` (`how = proof_level.same_test(...)`, display); `holds_over_comments` (`in ("instance_code","file_code")`, no production
  caller; F-T10 finding). R12 waiting finding (a): `probe_verdict` words accepted in `already_probed` (`== "intended_failure"`, `in ("no_failure","wrong_location")`),
  `_product_receipt_repeat` (`== "intended_failure"`), `acceptance.validate_window`; after C3-b2 these functions are converted accept sites of `test_identity`, and A26
  refuses a second registration of a converted accept site: a later fix needs a function split. One finding. R12 (d) `holds_over_comments`: one finding.
- Decision note: for `_run_freshness` and `_evaluate` the registry why replaces the bytes/changed sentence whenever `registry_problem()` is non-empty, as the card
  says, even if the word was `""` (truly other bytes): the registry cannot judge either way. Not a fork the card left open; stated for the critic.

## Needed beyond the manifest

`gate_registry.py` (the allow/F-a/F-b rules and `analyse`), `test_gate_preflight.py:5199-5239` (the `GT._READ` seam precedent), `docs/SIBLING_MAP.md:143`,
`test_probe_product_publish.py` (product receipt fixtures), the prose-twin files above, `acceptance.py` / `window_record.py` greps (analogs).

## RESOLUTION (Lead decision on the question: option A) - supersedes "NOT COMMITTED" and "RED" above

Applied: two `allow` entries on the `_run_freshness` site (whole texts `('unknown', WHY_RUN_NO_IDENTITY)` and `('unknown', why or WHY_RUN_NOT_COMPARED)`,
why "a state the function returns to its caller, not an acceptance of an identity word"; the two returns mean the same thing). S-f: D13 145 -> 149, triples
49 -> 52 - card estimate +2/+2, measured +4/+3 (`GR.analyse` on the final tree: items 149, triples 52), cause: the F-T1 (a) word `unknown` makes the two state
returns token sets; extra triple `("proof_level.py", "_run_freshness", "test_identity")`. The allow-list pin carries the two entries.
Witness on the final tree:
- `gate_registry.py --check`: "A26 gate registry: no violations", exit 0; debt block lists 5 rows, `test_identity` absent.
- test_gate_registry 497/497 ok; test_proof_level 627/627 ok; test_execution_request 667/667 ok; test_run_freshness 100/100 ok;
  test_judgment_census 25/25 ok and selftest --limits --lang 4/4 ok (earlier passes; code unchanged since except the registry allow entries).
- NOT run to the end (budget cap): test_stage_joints.py and the final-tree census re-run (backgrounded, not awaited); the per-file non-slow scenario_walk list.
- Negative control: above (scratch copy, F-b finding on `_product_receipt_repeat`, exit 1); the live tree was never corrupted.
