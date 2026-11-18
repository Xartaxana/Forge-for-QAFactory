# RD1-33 - readers of the `probe_verdict` and `test_identity` words: draft card (designer, t-1366)

Status: DRAFT for the Lead. Forks in §3 are not decided. Line numbers are those of the checkout `C:/QAFactory/forge-repo` read on
18.11.2026 (HEAD 8ee90ea3 per the session's git snapshot; estimate that it equals origin/main - the Lead checks with
`git -C C:/QAFactory/forge-repo rev-parse HEAD origin/main`). Builders cite `path::symbol`, never these numbers. Size: about 37.5 KB,
estimate (the designer has no shell; the Lead measures with `python -B -c "import os,sys;print(os.path.getsize(sys.argv[1]))" <this path>`).
D13 deltas below are estimates from reading; every step measures its own.

## 1. Frame

Goal (pile row RD1-33, fork F5 of `docs/tasks/specs/20261117-rd1-26-28-registry-words-card.md`): every reader of a word of the rows
`probe_verdict` and `test_identity` (`references/gate-registry.json`) is (R) a registered site of that row, or (P) reads the word through
the row's predicate or producer, or (H) reads another vocabulary that only shares the spelling, and is left. No dead reader was found (no D class).

How A26 counts (read in `scripts/gate_registry.py::analyse`, `::_scan_tree`, `::_walk`): a comparison or bare token display counts
when a word is an anchor, or a word of a row that registers the OUTERMOST def it sits in (nested defs belong to the outer one). A
registered non-accept site (produce / validate / dispatch / measure / vocabulary) allows its literals; a converted accept site must
call `acceptable` and allow-list every literal. `acceptable` never accepts class `unknown` or `mismatched` (`gate_template.py::acceptable`),
so only `intended_failure` can be routed through it (`proof_level.probe_fired`). An unregistered function comparing non-anchor words is
the stated BLIND SPOT: invisible, so (P)-routed readers get a structural row (item T-S) that the scanner's raw items hold no row word there.

Principle the classification follows (one rule for every file, P31):
- the function COMPUTES the word it writes into a record or answer -> (R) `produce`, literals stay (like `_judge_rows` today);
- the read LETS SOMETHING THROUGH on `intended_failure` (attach or publish a receipt, skip a run, count proved, a repeat) -> (P) `proof_level.probe_fired`;
  invariant I-MASK: no non-accept registration may cover such a read;
- the read PROTECTS a stored record or REFUSES (judge refusals, keep-standing) -> (R) `validate`, literals stay (fork F4);
- the read only PICKS a message, door, exit or display -> (R) `dispatch`; the judged set used by three exits -> `probe_judged` (fork F1);
- another field or vocabulary -> (H), with the field named.

AR invariants touched and the change check each one owes (DoD of every step):
- AR-13 (one reader): every (P) site calls `probe_fired` / `probe_judged`; check: T-S rows show no row word left in a routed function.
- AR-15 (one survivor): the judged set lives in one function (F1 a); check: `PROBE_JUDGED_VERDICTS` is gone, grep `scripts/` for the tuple shape
  `"intended_failure", "no_failure", "wrong_location"` with a positive control on `proof_level.py` before the edit.
- AR-1: the judged set and the unknown set stay lists in code at registered sites (cost named in F1); no new hard-coded list elsewhere.
- AR-20: every D13 raise is named row by row in the D13 comment of `test_gate_registry.py` (old -> new, triples added, measured before/after).
- AR-22: no producer is removed; the `decides` text of `probe_verdict` is reworded in the same commit as the sites it names.
- AR-28: every (P) route errs toward "not fired" (rerun, nothing published, not counted); each site's direction is in its step's edges.
- AR-29: checks added or altered and their owner and census class: `probe_judged` - a word-list over a code-produced token, owner data;
  every routed read - unchanged class (it compares a code token), owner data; registrations add no check. No census row is expected
  (precedent: `probe_found_defect` has none; `judgment-census.json` holds no `proof_level` row, Grep of `proof_level` there: 0 hits,
  positive control `"[a-z_]+\.py` -> rows found). `test_judgment_census.py` is canon-judged (slow list): report line, not a run.

`variety: none -- the change registers and routes readers of two factory-internal code vocabularies (the probe verdict, the test
identity word); it reads and adds no value of any project axis`.

Commit lines: the only carrier of the form is `tools/architecture_gate.py`. Content per step: `architecture:` naming AR-1, AR-13, AR-15,
AR-20, AR-22, AR-28, AR-29 with one clause each (as listed above), and `judgment: none -- the probe verdict and the identity word are
tokens produced by code (probe_by_code, red_sandbox, same_test, compare_identity); this step only registers or routes their readers and no
check reads a role's content`.

## 2. Classification of the digest (verified against the checkout)

Digest `docs/tasks/specs/reports/t-1362-rd1-33-digest.md`; `a-nn` = found here, not in the digest. Step = §4.

| id | where (`path::symbol`) | verified | class | step, D13 estimate |
|---|---|---|---|---|
| f-pv01/02 | proof_level::PROBE_JUDGED_VERDICTS, ::probe_record_state | yes | P: `probe_judged` (F1 a); constant deleted; `probe_record_state` R produce (its `plan_unfinished` literal and the state compares stay) | S1, +4 |
| f-pv03 | proof_level::tooling_gap_key | DIGEST WRONG: it reads `record.get('verdict') not in ('not_executed', 'incomplete')` | R validate (grants a class key, errs to "") | S1, +1 |
| a-01 | proof_level::probe_could_not_run, ::probe_owes_judgment, ::probe_plain_call_owed | compare `state` words | P: read through the producer `probe_record_state` (its `state` field); leave | - |
| f-id01 | proof_level::held_words | yes | R dispatch, test_identity (picks the words shown) | S1, +2 |
| f-id02/03 | proof_level::_HOLDS_RANK, ::reached | yes; a dict lookup, invisible to A26 | H-derived: a tiebreak among words already accepted (all `matched`); leave (F5) | - |
| a-02 | proof_level::compare_identity | unregistered producer of `same`/`different`/`unknown` | R produce, test_identity (in reach: F6) | S1, +4 |
| f-id04 | execution_request::same_instance_bytes | yes; a budget count (flaky cap) with the opposite safe side | R measure, test_identity (keeps its own error direction) | S1, +1 |
| f-id05 | run_history::_make_pair | yes | H-derived: the pair word of `_compare_shas` (`same`/`changed`/`unknown`; `changed` is no row word); leave | - |
| f-id06 | window_record::_run_freshness_unknown | yes | H-derived: run-freshness state `fresh`/`stale`/`unknown` (the row's own allow `why` at `_run_freshness` says so); leave | - |
| f-id07 | ledger::test_state (digest: unresolved) | resolved: def `test_state`, reads `_row_freshness` | H-derived: run-freshness state; leave | - |
| f-pv04 | red_sandbox::request_status | yes | R produce (F2 a) | S2, +2 |
| f-pv05/09 | red_sandbox::verify | yes (`semantic_verdict`, `p['verdict']`) | R produce (the product judge upstream of `product_verdict`) | S2, +2 |
| f-pv06 | red_sandbox::write_sensitivity_receipts | yes | R validate (raises on `probe_defect`) | S2, +1 |
| f-pv07 | red_sandbox::probe | yes, 4 compares | R dispatch | S2, +4 |
| f-pv08 | red_sandbox::main | yes | R dispatch (exit) | S2, +1 |
| a-03 | red_sandbox::target_result; window_record::_receipt_block, ::probe_gap_block | producers by dict value (0 counted) | F6 | S2/S5, 0 |
| f-pv17 | probe_by_code::_judge_joint_rows | yes (nested `passed`) | R produce | S4, +1 |
| f-pv18 | probe_by_code::_receipt_core | yes | P probe_fired | S3, 0 |
| f-pv19/27/30 | probe_by_code `_SURVIVOR_ORDER`, `_CARRIED_VERDICTS`, `_AGG_KNOWN` | yes | R `probe_by_code.py:<module>` vocabulary (`_AGG_KNOWN` is read only in compares, counted at `_aggregate_rows`) | S4, +2 |
| f-pv20 | probe_by_code::_worst_of_rows | yes | R produce | S4, +2 |
| f-pv21 | probe_by_code::_proved_standing | yes | R validate (protects a stored proof; F4) | S3, +3 |
| f-pv22 | probe_by_code::_finish_record | yes | P probe_fired (receipt) | S3, 0 |
| f-pv23 | probe_by_code::_judge_alt_row | yes; output read only by `_print_alternatives` (`--alternatives`) | R dispatch (display state) | S3, +4 |
| f-pv24 | probe_by_code::keep_standing_record | yes | R validate (F4: its invariant "a proved record is replaced only by a judged run") | S3, +2 |
| f-pv25 | probe_by_code::_attempt_why | yes | R dispatch (picks which note speaks) | S3, +1 |
| f-pv26 | probe_by_code::_check_proved | yes | P probe_fired | S3, 0 |
| f-pv28 | probe_by_code::_walk_attempt | yes (nested `settle`) | R produce | S4, +2 |
| f-pv29 | probe_by_code::_walk_plan | yes | P probe_fired for the two proved reads; R dispatch for `standing in _CARRIED_VERDICTS` | S3, +1 |
| f-pv31 | probe_by_code::_aggregate_rows | yes | R produce | S4, ~+12 |
| f-pv32 | probe_by_code::_aggregate_verdict | yes (+ returned tuple displays) | R produce | S4, ~+11 |
| f-pv33 | probe_by_code::_judgment_fold | yes | R produce | S4, +2 |
| f-pv34 | probe_by_code::_aggregate_record | yes | P probe_fired for the receipt read (`verdict == 'intended_failure' and not unfinished and ...`); R produce for the rest | S3 route, S4 ~+7 |
| f-pv35 | probe_by_code::_repeat_same_entries | yes | P probe_fired (a repeat) | S3, 0 |
| f-pv36 | probe_by_code::publish_binding | yes | P probe_fired | S3, 0 |
| f-pv37/38/39 | probe_by_code::_unsettled_checks, ::_judge_walk, ::_judged_record | yes | R validate (judge refusals) | S3, +3 |
| f-pv40/41/42 | probe_by_code::_judge_cli, ::_finish_alternative, ::main | yes | P probe_judged (F1 a) | S3, 0 |
| f-pv10 | driver_stage_s6::s6_reprove (a method; bare name) | yes | P probe_fired for "proved again"; R dispatch for the `incomplete`+`judgment` line | S5, +1 |
| f-pv11/12 | probe_debt::_scan, ::_owed_words | yes | P probe_fired | S5, 0 |
| f-pv13 | probe_debt::_classify | yes | P probe_fired (`published`); R dispatch for `not_executed` -> stop | S5, +1 |
| f-pv14 | probe_debt::_previous_attempts (+ a-04 ::settle `result['result'] == 'not_executed'`) | yes | H-derived: the settle memory's `result` word; leave | - |
| f-pv15/16 | window_record::_probe_scope_notes, ::unproved_keys_text | yes | P probe_fired | S5, 0 |
| a-05 | contract::PROBE_GAP_VERDICTS | not in digest | H-derived: words of a person's probe-gap record (`not_run` included = `probe_record_state` states); leave | - |
| a-06 | check_delivery, contract, retro_numbers, report_facts, run_suite, controller, exit_gate, story_step (`not_executed` / `incomplete`) | homonym family | H: execution status, ledger state, dispatch status; leave | - |

Digest gaps closed here: `tooling_gap_key` read (f-pv03); `unknown` closed by its producers, not by spelling: every
`test_identity` `unknown` reaches a reader only through `compare_identity`, `same_test`, `_run_freshness`/`run_freshness` or
`_compare_shas`, and their callers were read (§6 trail): the only compares of `unknown` are f-id06/f-id07 (derived) and the registered
allow entries. Variable-held sets: the four module tuples above are all there are in the six probe files (Grep of `^_[A-Z_]+ =` in
`probe_by_code.py`, and of the word tuple shape over `scripts/`, see trail).

Words in the row's `verdict` field that are NOT row words (fork F3): `not_reached`, `not_owed` (per-check rows), `gap` (alternative
record), `already_probed` (probe answer). Second carrier of the words: `handoffs/vocabulary.yaml` `probe_verdicts` (5 words).

## 3. Forks (the Lead decides; recommendation marked)

**F1 - the judged set (intended_failure / no_failure / wrong_location) read at four places in two files** (`probe_record_state`, the exits
of `probe_by_code::main`, `::_finish_alternative`, `::_judge_cli`). `acceptable` cannot carry it (mismatched words).
- (a, recommended) New `proof_level.probe_judged(record) -> bool`: `isinstance(record, dict) and record.get('verdict') in
  ('intended_failure', 'no_failure', 'wrong_location', 'survived')` - every word of class matched or mismatched in the row; registered under
  `probe_verdict` role `validate`; `PROBE_JUDGED_VERDICTS` deleted. Error direction: False (exit 1, state not `judged`). `survived` joins
  (unreachable today: only `red_sandbox` writes it, to `work/probes/product/`). Cost: AR-1 met as "one registered site", not "in data".
- (b) No new function: register the three exits as `dispatch` and `proof_level.py:<module>` as `vocabulary` for the constant. Four copies stay.
- (c) A class reader beside `acceptable` in `gate_template` (C3-0 grammar change; a mechanism node with a plan critic, as RD1-28 F1 (b)).

**F2 - the red_sandbox request `status` words** (`accepted`, `survived`, `probe_defect`, `not_executed`, `incomplete`, `already_probed`;
`verify` returns `accepted`/`probe_defect`/`incomplete`). The code says the status "never contradicts a `survived` product record (FR-35)".
- (a, recommended) The same vocabulary as `probe_verdict` (P31): register `verify`, `request_status` produce; `write_sensitivity_receipts`
  validate; `probe`, `main` dispatch. `accepted` / `already_probed` stay no row words (not counted). No new row.
- (b) A new row `product_probe_status` with its own words and these sites (RD1-25: one row per function; `survived` in two rows needs a same-class pin).
- (c) Call it another vocabulary; leave unregistered; `decides` names it. Readers stay invisible.

**F3 - non-row words written into the `verdict` field** (`not_reached`, `not_owed`, `gap`, `already_probed`).
- (a, recommended) Leave them outside the row; the `decides` of `probe_verdict` names them as states of the walk and of the answer, not
  verdicts on the test. Cost: a comparison of them only stays invisible (the stated blind spot).
- (b) Add them to `words` / `verdict_map` (`not_reached` unknown/factory, `not_owed` not_applicable, `gap` unknown/factory, `already_probed`
  to be decided) and to `handoffs/vocabulary.yaml` `probe_verdicts` and the two handoff carriers (`s5-critic-to-automator.yaml`,
  `references/slices/qa-code-critic/handoff-keys.md`). Every registered probe site then counts them: D13 rises further.
- (c) A row split `probe_check_state` for the per-check rows.

**F4 - reads that protect a stored proof** (`keep_standing_record`, `_proved_standing`).
- (a, recommended) R `validate`, literals stay. On an unreadable registry a proved record is still not overwritten by an unjudged run
  (`keep_standing_record`'s invariant, t-177); the kept record is judged again by its readers through `probe_fired`.
- (b) Route through `probe_fired` (one accept road). An unreadable registry then overwrites a proved record with `not_executed`: the
  evidence `probe_debt.py` settles is lost.

**F5 - `_HOLDS_RANK`** (`raw` 3, `instance` 2, `instance_code`/`file_code` 1).
- (a, recommended) Leave in code: a tiebreak among accepted words, one reader. (b) A `rank` key in `verdict_map` (a schema change: `MAP_KEYS`
  in `gate_registry.py`, the C3-0 tables; a mechanism node).

**F6 - unregistered producers met on the way** (a-02 `compare_identity`; a-03 `target_result`, `_receipt_block`, `probe_gap_block`).
- (a, recommended) Register them as `produce` in the steps that already edit their row (S1: `compare_identity` under test_identity, ~+4 items;
  S2: `target_result`; S5: the two window producers, 0 items each) - the registry then lists every producer (AR-22). In the node's reach.
- (b) Leave them; only readers are in scope.

Small choices closed here (no design weight): routing a bare word through `probe_fired({'verdict': word})` at `_check_proved`,
`_walk_plan`, `_aggregate_record` (the predicate takes a record; no signature change, so its readers stay as they are); S3 and S4 are
separate steps so the D13 raise of the producers is reviewed apart from the routing (they may merge if the Lead prefers fewer rounds);
the structural row extends RD1-28's E28-6 check into one table instead of a new test.

## 4. Steps (cards for builders)

Ordering invariants (state, not a sequence):
- I1: at any moment at most ONE open branch holds `references/gate-registry.json` or `scripts/tests/test_gate_registry.py` in its owns:
  every RD1-33 step holds both, and so does each of RD1-14 k1-k4. No two steps write gate-registry.json at once. A step starts from a main
  that contains every earlier merged writer, and measures D13 there.
- I2: a step that registers or edits a function of `probe_by_code.py` or `red_sandbox.py` starts only when no other open branch holds that
  file (RD1-37, RD1-38; RD1-39 for `reporters.py` is disjoint unless it widens to these files). A renamed or rewritten function changes A26's
  sites and counts.
- I3: `probe_judged` exists before any caller (S1 before S3).
Sequence meeting them (recommended): S1 -> S5 (neither waits for RD1-37/38) -> S2 -> S3 -> S4 (after RD1-37/38 merge), each after the
previous writer of the registry (an RD1-33 step or an RD1-14 k-step) has merged.

Common to every step:
- D13 measure, before the edit and after it, from the worktree root `<wt>`:
  `python -B -c "import sys; sys.path.insert(0, r'<wt>/ai-packages/qa-factory/scripts'); import gate_registry as G; r=G.analyse(); print(len(r['items']), len({(i['file'],i['function'],x) for i in r['items'] for x in i['rows']}), len(r['findings']))"`
  Base on this checkout: 160 items (`D13_ITEM_COUNT`), 61 triples (counted by reading `D13_TRIPLES`), 0 findings; RD1-14 may move it - the
  step's own "before" is the base, never this number.
- `gate_registry.py --check` expectation: exit 0, no finding, the `debt` and `exempt` lists identical to the base's; no `allow` entry is added
  (none of the new sites is an accept site; the allow pin in `part_live_registry` stays).
- Edge E-D13: a measured delta that differs from the card's estimate is pinned as measured, and the report and the D13 comment list every
  extra or missing item (file, function, source). Invariant: the D13 count and triple set equal what `analyse` measures on the merged tree.
  A new FINDING is never pinned: stop and return it as a question.
- Edge E-STALE: an F-c (stale site) or F-e (two defs of one name) finding on a site this step adds -> stop and return (I2 was broken).
- T-S (structural row, register layer): the RD1-28 check `left(file, function)` in `test_gate_registry.py::part_site_attribution`
  becomes one parameterised table `(file, function, literals left)`; each step adds its routed functions. Expected from: this card §2.
- Witness of the canon-class files (`test_gate_registry.py`, `test_proof_level.py`, `test_probe_debt.py`, `test_window_record.py`,
  `test_red_sandbox_*.py` are on the slow list, `scripts/slow_tests.json`): a narrow call, e.g.
  `python -B -c "import sys; sys.path[:0]=[r'<wt>/ai-packages/qa-factory/scripts/tests', r'<wt>/ai-packages/qa-factory/scripts']; import test_gate_registry as T; T.part_site_attribution(); T.part_live_registry(); T.finish('narrow')"`,
  and the report line `not run locally: <file>, canon judges`.

### S1 - proof_level readers, test_identity registrations, `probe_judged`

given: this card §1-§3 (F1, F6 as decided); `scripts/gate_registry.py`; `scripts/gate_template.py`; `references/gate-registry.json` rows `probe_verdict`, `test_identity`
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/proof_level.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_proof_level.py
non-goals: `execution_request.py` code (registration only); `probe_could_not_run` / `probe_owes_judgment` / `probe_plain_call_owed` (read the producer's state); `_HOLDS_RANK` (F5); probe_by_code callers (S3); a new test file
handoff: commit on the node branch + C:/QAFactory/forge-repo/docs/tasks/specs/reports/20261118-rd1-33-s1-report.md
edges: E-D13, E-STALE, E1-1..E1-5 below
DoD: `python -B <wt>/ai-packages/qa-factory/scripts/gate_registry.py --check` exit 0 + the narrow calls of `test_gate_registry.part_site_attribution` / `part_live_registry` and of the new table in `test_proof_level.py` + `python -m pytest <wt>/ai-packages/qa-factory/scripts/tests/test_probe_readers.py <wt>/ai-packages/qa-factory/scripts/tests/test_probe_marker_judgment.py -q`
siblings: axis 34 (one road for the judged set: F1); RD1-28 (`probe_found_defect` is the precedent form); RD1-14 k1-k4 (I1)

Items:
1. `proof_level.probe_judged(record)` beside `probe_found_defect`, as F1 (a) states; docstring names the row and the error direction.
2. `probe_record_state`: the judged branch asks `probe_judged(record)`; `PROBE_JUDGED_VERDICTS` deleted. Branch order unchanged.
3. Registry, row `probe_verdict`: sites + `probe_judged` validate, `tooling_gap_key` validate, `probe_record_state` produce; `decides`:
   the "Registered here" list names them. Row `test_identity`: sites + `held_words` dispatch, `compare_identity` produce (F6 a),
   `execution_request.py:same_instance_bytes` measure.
4. `test_gate_registry.py`: `D13_TRIPLES` gains the six triples; `D13_ITEM_COUNT` measured, with its comment (old -> new, why, before/after).
Estimate: +13 items, +6 triples (probe_judged 1, tooling_gap_key 1, probe_record_state 4, held_words 2, compare_identity 4 (returned tuple
displays), same_instance_bytes 1). Product files: 1 (`proof_level.py`) + the registry.

Edges:
- E1-1 (adversarial inputs, the new consequential role): `probe_judged` is False for a non-dict, a missing / None / non-str verdict, a case or
  padding variant (`Intended_failure`, ` no_failure`), every unknown word (`not_executed`, `incomplete`, `probe_defect`) and every non-row
  word (`not_reached`, `not_owed`, `gap`, `already_probed`). Invariant: an unknown-class word is never "judged".
- E1-2 POSITIONAL (`probe_record_state`): `plan_unfinished` before the unjudged branch, before the judged one, as today. Invariant: an
  `incomplete` walk left unfinished never reads as could-not-run, and a judged record never reads `not_run`.
- E1-3 `survived` at the live path: state `judged` (was `not_run`). Unreachable (no live writer); stated so a reader of the state knows.
- E1-4 `tooling_gap_key` keeps its literal: an unreadable registry does not change it (no registry read). Invariant: a record of other bytes never gives a key.
- E1-5 `same_instance_bytes` keeps its budget-side direction: "unknown" is False here and its caller folds it (no route through `acceptable`, which would add a registry dependency to a budget).

Tests, strongest first (one parameterised row per behaviour; builder stops when test lines reach code lines):
- `test: test_proof_level.py::<the consumer table> + rows for probe_judged (7 row words, the adversarial inputs of E1-1) | expected from: §3 F1 (a), registry verdict_map`
- `test: test_gate_registry.py::D13_TRIPLES, D13_ITEM_COUNT | expected from: this card §2 and the measured delta (AR-20)`
Test cost: 2 rows (one table of ~16 entries in a canon file, checked by a narrow call; one pin change). No T-S row (no routed function outside a registered site).

### S5 - routing in driver_stage_s6, probe_debt, window_record

given: this card §1-§2; S1 merged (I1); `proof_level.probe_fired` docstring
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_stage_s6.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/probe_debt.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/window_record.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py
non-goals: `probe_debt::_previous_attempts` and `::settle` (settle memory word, H); `window_record::_run_freshness_unknown` (H); the window producers unless F6 (a); a new test file
handoff: commit on the node branch + C:/QAFactory/forge-repo/docs/tasks/specs/reports/20261118-rd1-33-s5-report.md
edges: E-D13, E-STALE, E5-1..E5-4
DoD: `python -B <wt>/ai-packages/qa-factory/scripts/gate_registry.py --check` exit 0 + narrow calls of `test_gate_registry.part_site_attribution`, of `test_probe_debt.py` and `test_window_record.py` cases that call the changed functions + `python -m pytest <wt>/ai-packages/qa-factory/scripts/tests/test_probe_every_check.py -q` (estimate: not slow-listed; the Lead confirms the witness files with `scenario_walk.py --witness-for` before dispatch)
siblings: axis 34; RD1-28 (window/acceptance already ask `probe_fired`); `test_s6_reprove_manual.py` is in quarantine (not run, not edited)

Items:
1. `driver_stage_s6::s6_reprove`: "proved again" asks `proof_level.probe_fired(record)` (keeps `not code and`); the `incomplete` + `judgment`
   line stays; register `s6_reprove` dispatch.
2. `probe_debt::_scan` (both reads), `::_owed_words`, `::_classify` (`published` branch) ask `PL.probe_fired(...)`; `_classify`'s
   `not_executed` -> stop stays; register `_classify` dispatch.
3. `window_record::_probe_scope_notes`, `::unproved_keys_text` ask `proof_level.probe_fired(...)`.
4. Registry `probe_verdict.decides`: name the settled readers; F6 (a): `_receipt_block`, `probe_gap_block` produce. Pins as in S1 item 4.
Estimate: +2 items, +2 triples (+2 triples, 0 items more under F6 a). Product files: 3.

Edges (unreadable registry = `gate_template.registry_problem()` non-empty; `probe_fired` False):
- E5-1 `s6_reprove`: the probe is NOT counted proved again. The line then reads `<iid>: not proved again - ` +
  `gate_template.registry_why(problem, "the probe record was not judged")`, never "gave `intended_failure`, not `intended_failure`".
  POSITIONAL: the fired check stays first. Invariant: a non-zero exit is never counted proved.
- E5-2 `probe_debt::_classify`: neither `published` nor `unpublished`; the answer falls to the generic branch with `settled: False` and
  words `registry_why(problem, "the probe record was not judged")`. Invariant: nothing is settled on an unread registry. `_scan`: the record is not an item (no settle on it).
- E5-3 `unproved_keys_text`: every check whose verdict is not fired is listed, with its verdict word. Invariant (AR-28): an unproved check is never hidden.
- E5-4 `_probe_scope_notes`: no info line (info only; the block's verdict and level are untouched, as the function's docstring states).

Tests:
- `test: test_gate_registry.py::<T-S table> rows (_scan, _owed_words, _probe_scope_notes, unproved_keys_text: 0 left; _classify, s6_reprove: 1 left) | expected from: §2, I-MASK`
- `test: one row in an existing s6/probe_debt case table: unreadable registry -> s6_reprove line carries the registry sentence | expected from: E5-1`
- `test: test_gate_registry.py::D13_TRIPLES, D13_ITEM_COUNT | expected from: §2 (AR-20)`
Test cost: 3 rows (1 table extension, 1 behaviour row, 1 pin change).

### S2 - red_sandbox registrations (data only)

given: this card §2, F2 and F6 as decided; RD1-37 and RD1-38 merged (I2)
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py
non-goals: any edit of `red_sandbox.py`; `reporters.py`; a new row (F2 b is not this card's unless decided)
handoff: commit on the node branch + C:/QAFactory/forge-repo/docs/tasks/specs/reports/20261118-rd1-33-s2-report.md
edges: E-D13, E-STALE, E2-1
DoD: `python -B <wt>/ai-packages/qa-factory/scripts/gate_registry.py --check` exit 0 + the narrow call of `test_gate_registry.part_site_attribution` / `part_live_registry`
siblings: RD1-28 F2 (one row for both probe tools); RD1-37/38 (I2)

Items: row `probe_verdict` sites + `verify` produce, `request_status` produce, `write_sensitivity_receipts` validate, `probe` dispatch,
`main` dispatch (+ `target_result` produce under F6 a); `decides` names the red_sandbox readers and drops `request_status` / `main` from the
"not sites yet" clause. Pins. Estimate: +10 items, +5 triples (+1 triple, 0 items under F6 a). Product files: 0.
- E2-1 `main`'s `status in ('accepted', 'survived', 'already_probed')` counts as one item (one row word): exit 0 for a survivor is the
  tool's design (a valid answer), unchanged. Invariant: `probe_defect`, `not_executed`, `incomplete` still exit 1.
Tests: `test: test_gate_registry.py::D13_TRIPLES, D13_ITEM_COUNT | expected from: §2 (AR-20)`. Test cost: 1 pin change.

### S3 - probe_by_code routing, its validate and dispatch sites

given: this card §1-§3; S1 merged (`probe_judged`, I3); RD1-37 and RD1-38 merged (I2)
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/probe_by_code.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py
non-goals: the producers' literals (S4); `_CARRIED_VERDICTS` and its test pin in `test_probe_fix_round.py`; `judge_probe_row` / `_judge_rows` (registered); a new test file
handoff: commit on the node branch + C:/QAFactory/forge-repo/docs/tasks/specs/reports/20261118-rd1-33-s3-report.md
edges: E-D13, E-STALE, E3-1..E3-5
DoD: `python -B <wt>/ai-packages/qa-factory/scripts/gate_registry.py --check` exit 0 + the narrow call of `test_gate_registry.part_site_attribution` + `python -m pytest <wt>/ai-packages/qa-factory/scripts/tests/test_probe_fix_round.py <wt>/ai-packages/qa-factory/scripts/tests/test_probe_walk.py <wt>/ai-packages/qa-factory/scripts/tests/test_probe_readers.py -q` (estimate: not slow-listed; the Lead confirms)
siblings: axis 34; RD1-28 E28-6 (one accept site `probe_fired`); `probe_debt.py` (reads the records this step writes)

Items:
1. Route to `proof_level.probe_fired`: `_receipt_core` (copy of `proved_by`), `_finish_record` (receipt), `_aggregate_record` (receipt
   read only), `_check_proved`, `_walk_plan` (both proved reads), `_repeat_same_entries` (the three reads; `not_owed` stays a plain
   compare - no row word), `publish_binding`.
2. Route to `proof_level.probe_judged`: the exits of `main`, `_finish_alternative`, `_judge_cli`.
3. Register validate: `_proved_standing`, `keep_standing_record` (F4 a), `_unsettled_checks`, `_judge_walk`, `_judged_record`; dispatch:
   `_judge_alt_row`, `_attempt_why`, `_walk_plan`. `decides`: drop `keep_standing_record`, `publish_binding`, `main` from the clause.
4. Pins. Estimate: +14 items, +8 triples. Product files: 1.

Edges (unreadable registry: `probe_fired` False):
- E3-1 receipt reads (`_finish_record`, `_aggregate_record`, `_receipt_core`) and `publish_binding`: no receipt attached, nothing published.
  Invariant: no receipt or binding is written on an unread registry; the record itself is still written (its verdict word is the producer's).
- E3-2 `_check_proved`, `_walk_plan`, `_repeat_same_entries`: the check runs again; not a repeat. Invariant (AR-28): an unread registry never skips a run.
- E3-3 POSITIONAL `_walk_plan`: the fired test stays before `standing in _CARRIED_VERDICTS`. Invariant: a proved check is never carried as a survivor.
- E3-4 `_judge_cli`: the set widens from {intended_failure, wrong_location} to the judged set; `no_failure` / `survived` cannot reach it (a
  judge writes `intended_failure`, `wrong_location` or leaves `incomplete`: `judge_record`). Invariant: an `incomplete` record never exits 0.
- E3-5 the exits of `main` / `_finish_alternative`: unchanged for every word written today; `survived` would exit 0 (unreachable).
Tests:
- `test: test_gate_registry.py::<T-S table> rows (the seven routed functions of item 1 and the three of item 2: 0 left) | expected from: §2, I-MASK`
- `test: one row in test_probe_readers.py (or the receipt table it holds): unreadable registry -> publish_binding returns "" and no receipt | expected from: E3-1`
- `test: test_gate_registry.py::D13_TRIPLES, D13_ITEM_COUNT | expected from: §2 (AR-20)`
Test cost: 3 rows.

### S4 - probe_by_code producers and its token sets (data only)

given: this card §2; S3 merged (the routed reads are gone, so they are not counted); RD1-37/38 merged (I2)
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py
non-goals: any edit of `probe_by_code.py`; F3 words
handoff: commit on the node branch + C:/QAFactory/forge-repo/docs/tasks/specs/reports/20261118-rd1-33-s4-report.md
edges: E-D13, E-STALE, E4-1
DoD: `python -B <wt>/ai-packages/qa-factory/scripts/gate_registry.py --check` exit 0 + the narrow call of `test_gate_registry.part_site_attribution` / `part_live_registry`
siblings: RD1-28 (the row's producers); t-598 D13 note (a helper split only to avoid a count is not done)

Items: register produce: `_judge_joint_rows`, `_worst_of_rows`, `_walk_attempt`, `_aggregate_rows`, `_aggregate_verdict`, `_judgment_fold`,
`_aggregate_record`; `probe_by_code.py:<module>` vocabulary. `decides` loses the "not sites yet" clause if S2-S5 emptied it. Pins.
Estimate: ~+39 items, +8 triples (the largest raise; every item named in the D13 comment by function).
- E4-1 `<module>` registration counts every module-level display with a probe word in `probe_by_code.py`, not only the three tuples: the
  measured list is pinned (E-D13). Invariant: no module-level probe-word set stays outside a site.
Tests: `test: test_gate_registry.py::D13_TRIPLES, D13_ITEM_COUNT | expected from: §2 (AR-20)`. Test cost: 1 pin change.

## 5. Readers of the touched files (rule 7)

The `owns_readers.py` block was NOT attached to the brief: the Lead runs
`python -B tools/owns_readers.py --paths ai-packages/qa-factory/scripts/proof_level.py ai-packages/qa-factory/scripts/probe_by_code.py ai-packages/qa-factory/scripts/driver_stage_s6.py ai-packages/qa-factory/scripts/probe_debt.py ai-packages/qa-factory/scripts/window_record.py ai-packages/qa-factory/references/gate-registry.json ai-packages/qa-factory/scripts/tests/test_gate_registry.py --names PROBE_JUDGED_VERDICTS probe_judged D13_ITEM_COUNT D13_TRIPLES`
and the plan critic answers its lines. Hand grep meanwhile (known misses: `.claude/` not searched - worktree copies flood it; `.githooks/`
Grep `gate-registry\.json|gate_registry|PROBE_JUDGED_VERDICTS` 0 hits, no positive control of that shape there):

| file / name | reader | answer |
|---|---|---|
| gate-registry.json | `gate_registry.load_registry` (A26, `gate_template`), `test_gate_registry.py` | changes in each step (sites, decides) |
| gate-registry.json | `tools/source_split.py` + `tools/source-split-carriers.json` (site carriers by file/function), `tools/test_quarantine.py` (path list), `tools/controller-blocks-gen.py:355` (comment) | unchanged: they read any row; Grep over `tools/` 17 hits in 4 files |
| test_gate_registry.py `D13_*` | RD1-14 k1-k4 (same pins) | I1: never two open writers |
| proof_level::PROBE_JUDGED_VERDICTS | `proof_level.probe_record_state` only (Grep over `scripts/` incl. tests: 2 hits, 1 file) | deleted in S1 with its one reader |
| proof_level (new `probe_judged`) | probe_by_code (S3) | S3 |
| probe_by_code.py | `probe_debt.py` (imports PBC), `window_record.py` (lazy import: `_entry_sha`, JUDGE_DOOR), tests | unchanged API: only bodies change; RD1-37/38 (I2) |
| driver_stage_s6.py, probe_debt.py, window_record.py | their importers and test files | bodies only; no name changes |
| `handoffs/vocabulary.yaml` probe_verdicts | `handoff_check.py:2134` | unchanged unless F3 (b) |

## 6. Reading trail

- Digest t-1362 (whole); pile row RD1-33 (`plans/piles/rules-debt/batch-1-phase-2.md:61`); card RD1-26/28 §3 F1-F5 (:130-174), m1/m2 (:76-77).
- `gate-registry.json:1-5` (note), `:124-176` (test_identity), `:638-666` (probe_verdict); site list by Grep of `"file": "(probe_by_code|red_sandbox|driver_stage_s6|probe_debt|window_record|execution_request|proof_level)\.py"` (25 hits, none of the new functions already a site).
- `gate_registry.py:1-153` (docstring, roles), `:205-264` (`_walk`: outermost def), `:313-415` (`_scan_tree`), `:426-444`, `:751-850`, `:853-984` (`analyse`).
- `gate_template.py:1-107` (`acceptable` refuses unknown/mismatched).
- `test_gate_registry.py:800-830`, `:1000-1025`, `:1028-1195` (D13 pins; 61 triples counted by reading), `:1290-1322` (`main`, `part_*`).
- proof_level: `:240-253`, `:850-885`, `:965-990`, `:1088-1237`, `:1740-1806`; def index by Grep `^def \w+`.
- red_sandbox: Grep of the seven words (33 lines); `:700-744`, `:836-849`, `:1245-1263`, `:1500-1536`, `:1790-1861`; def index.
- probe_by_code: comparison-shape Grep (52 lines), tuple-shape Grep, def index (persisted); `:4036-4067`, `:4261-4283`, `:4372-4391`, `:4698-4746`,
  `:5899-6005`, `:6050-6065`, `:6284-6294`, `:6318-6335`, `:6476-6489`, `:6696-6745`, `:6750-6799`, `:6840-6859`, `:6940-6957`, `:7322-7364`,
  `:7600-7611`, `:7677-7758`, `:7896-7903`, `:7936-7943`, `:8302-8324`, `:8390-8402`; `JUDGE_VERDICTS` `:196`.
- driver_stage_s6 `:660-689` + def index; probe_debt `:294-333`, `:355-363`, `:661-702`, `:733-747` + def index; window_record `:700-760`,
  `:1950-1967` + def index; execution_request `:2066-2110`, `:2394-2402`; run_history `:252-269`, `:690-719`; ledger `:1138-1159`,
  `:1255-1279` + def index.
- Homonym check: Grep of `(==|!=|in)\s*"(not_executed|incomplete)"` over 7 files (11 hits, all other vocabularies); `"(raw|instance|same)"`
  compare shape over `scripts/` (control: acceptance.py:179 found); `"(instance_code|file_code|different)"` over `scripts/`.
- Unique probe words per file (Grep count, non-homonym words): driver_stage_s6 1, probe_debt 4, probe_by_code 49, proof_level 5,
  red_sandbox 22, window_record 3 - no other production file.
- `not_reached` / `not_owed` / `gap` / `already_probed` producers: Grep over `scripts/`; `vocabulary.yaml` probe_verdicts and its carriers.
- `design/architecture.md` AR-1, AR-2, AR-13..AR-22, AR-29 (`ai-packages/qa-factory/design/architecture.md:20-99`, `:173-282`).
- `docs/TESTING.md:36-250`; `test-layers.json` sections (`keep` 42-7353, `quarantine` 7408-), canon_only masks; `slow_tests.json` `files`.
- Facts cited from the Lead (not re-measured): RD1-28 at 2a125072; RD1-14 k1 (t-1361) on profile_contract.py / gate-registry.json /
  test_gate_registry.py; RD1-37/38/39 files. `D13_ITEM_COUNT = 160` re-read at `test_gate_registry.py:1162`.

needed beyond the manifest: `scripts/proof_level.py`, `scripts/probe_by_code.py`, `scripts/red_sandbox.py`, `scripts/probe_debt.py`,
`scripts/window_record.py`, `scripts/driver_stage_s6.py`, `scripts/execution_request.py`, `scripts/run_history.py`, `scripts/ledger.py`,
`scripts/tests/test_gate_registry.py`, `design/architecture.md`, `scripts/tests/test-layers.json`, `scripts/slow_tests.json`.

## Lead decisions (18.11, Lead 501cb4e0; designer t-1366 accepted)

- F1 (a): `proof_level.probe_judged` with `survived` in the judged set; `PROBE_JUDGED_VERDICTS` deleted.
- F2 (a): the red_sandbox status words register under `probe_verdict`; no new row.
- F3 (a): `not_reached`, `not_owed`, `gap`, `already_probed` stay outside the row; `decides` names them.
- F4 (a): `keep_standing_record` / `_proved_standing` stay `validate` with literals; an unreadable registry never overwrites a proved record.
- F5 (a): `_HOLDS_RANK` stays in code.
- F6 (a): the unregistered producers register as `produce` in the steps that already edit their row.
- Order (I1, one registry writer at a time): RD1-14 k1 -> RD1-33 S1 -> RD1-14 k2 -> RD1-33 S5 -> RD1-14 k3 -> k4 ->
  RD1-37/38 S2+S3 wave (I2) -> RD1-33 S2 -> S3 -> S4. Each step starts from a main holding every earlier merged writer and
  measures D13 there. S3 and S4 stay separate steps.
