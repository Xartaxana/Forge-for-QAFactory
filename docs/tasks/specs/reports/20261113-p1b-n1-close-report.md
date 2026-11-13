# P1-b N1 close round: report

Branch wip/p1b-n1. Owns touched: `scripts/tests/dry_exits.py`, `fixtures/driver-exits/{classes,s0}.json`, this report (the previous fix-round report `20261113-p1b-n1-fix-report.md` is committed with it). No driver or package code touched.

## What changed

1. Routes `readiness`, `story_budget`, `executor` (rows in `s0.json`) name a source: `question:s0.readiness`, `route:story_budget`, `route:executor`. `classes.json` by_source gains the three keys, each `gate`; `_about` gains the one sentence on `route:<name>` sources. `class_of` is unchanged (the existing `by_source`-key-directly branch, same door as `route:marked_person`). `default` stays `null`.
2. Person-site keyed rule follows names transitively in the SAME function (`_bindings` now keeps every bound expression; `_name_keyed` follows them; `_text_keyed` starts it). Cycle -> keyless (terminates); more than `MAX_HOPS = 8` bindings in a chain -> keyless (said in the docstring); a name bound twice, once reaching a call and once not -> MIXED. Never across functions, attributes of `self`, parameters.
3. Selftest rows: +5 (82 -> 87): two-hop chain keyed; chain through a name bound twice MIXED; cycle keyless; 8 hops keyed / 9 hops keyless; parameter and `self.` attribute not followed. The item-3 negative row already existed and stays: `class: an ask_person route naming a by_source key directly takes its class; a key nobody holds is red` (`route:nobody` absent from by_source -> `class unknown`, red); the E19 rows (no `class_source`, and `""`/None -> class unknown) also stay. An empty `class_source` string is already the same as absent (red): no change.

## Numbers before -> after

| number | before | after | recount |
|---|---|---|---|
| discrepancies | 3 (class unknown x3) | 0 | `--check` last line |
| kinds without a key | 14 of 29 (13 keyless, 1 mixed: package) | 14 of 29 (12 keyless, 2 mixed: package, questions) | rows of the group files (14, unchanged) + the grep printed in the NUMBER line; split has no one-line recount (needs the binding rule) |
| classes, gates: questions | 2 | 3 (`question:s0.readiness` is a price key) | recount command in the NUMBER line prints `25 0 3` |
| selftest | 82/82 | 87/87 | `--selftest` |
| unwalked / hook_layer ratchets | 82/82, 77/77 | 82/82, 77/77 | NUMBER ratchet (no ratchet rose) |

The real tree gives exactly the Lead's expected 12 keyless + 2 mixed (`package`, `questions`).

## Verification (verbatim, after the last edit; package dir, subshell)

`python -B scripts/tests/dry_exits.py --selftest` (non-PASS lines): `dry_exits selftest: 87/87 cases`

`python -B scripts/tests/dry_exits.py --check` (exit 0):

```
NUMBER routes: 21 KNOWN_REFUSALS + 2 minted by match_known (marked_person, marked_repair) + 2 (unmatched, known_false) = 25
NUMBER price keys: 61, options: 188
NUMBER joints: 43 (detector 8, exit 8, window 27)
NUMBER kinds without a key: 14 of 29 literal kinds (12 keyless, 2 mixed: package, questions); sites with a kind that arrives as a value: 9 (driver_conductor:_person_of, driver_conductor:pass_to_person, driver_dialog:held_question, driver_gates:gate, driver_machine:_act_wait_existing_job, driver_machine:handle_refusal, driver_runner:site_seam_person, driver_s0:s0_again, driver_s0:s0_stop)
NUMBER classes, bans: word-does-not-pass 58 / word-passes 19
NUMBER classes, gates: operations 25 (of them override '': 0) / joints 43 / questions 3
NUMBER ban_doors without a named door: 0
NUMBER ratchet (rows now / base): live_only 0/0, after 0/0, unwalked 82/82, hook_layer 77/77; raised_by 0
NUMBER groups: gates, hooks, s0, s1-s4, s5, s6-s9
NOTE walk rows: none (...\fixtures\stories\dry-1\exits holds no rows yet; the walk nodes N4 write them)
dry_exits --check: 0 discrepancies
```
(the recount brackets of each NUMBER line are unchanged from the fix report and omitted here; the line is otherwise verbatim.)

`python -B scripts/tests/scenario_walk.py --witness-for scripts/tests/dry_exits.py`:
```
no scenario or keep row covers scripts/tests/dry_exits.py: run the whole scenario layer
scripts/tests/dry_exits.py: test_scenario_cart_1.py / test_scenario_local_1_0108.py / test_scenario_local_1_arm_b.py / test_scenario_walk.py / test_scenario_world.py
```
Non-slow among them (`slow_tests.json` lists cart_1, local_1_0108, arm_b): `test_scenario_walk.py` -> `=== test_scenario_walk: 93/93 ok ===`; `test_scenario_world.py` -> `=== test_scenario_world: 33/33 ok ===`. (Run as scripts; under pytest they collect no tests.) Deviation: I also ran `test_scenario_local_1_0108.py` under pytest by mistake before checking the slow list (slow file, collected nothing, 80 s, no effect).

`python -B scripts/selftest.py --lang`: `PASS lang: no Cyrillic anywhere in the package`, `PASS lang: no control byte left by an eaten escape sequence (FR-29)`, `=== qa-factory selftest: 2/2 ok ===`. Non-ASCII grep over `dry_exits.py` and the driver-exits JSON: no hit.

## Siblings

- Routes with move `ask_person` whose `class_source` resolves only through a default or a guess: none (`--check` reports no `class unknown`; `default` is `null`).
- Other rules in `dry_exits.py` reading bindings one hop only: none found. `_bindings`/`_text_keyed` were the only binding reader; the other ASTs (`scan_minted` / `scan_routes` read literal return tuples, `_calls_keyed` walks one expression) read no names. Verdict: no neighbors.
- Unchanged analog (queued by Lead): `run_suite.py` / `story_budget.py` have no `refusal_registry.py` record; the `route:<name>` rows stand until that node.

## FR walk

A: FR-57/59 an unnamed source stays red (negative row). B: no person text. C: FR-13 class words are data rows (`classes.json`). D: FR-17 unchanged readers. F: FR-28 table of cases, 87. G: FR-29/30 `--lang` 2/2, ASCII. Hop limit 8 is a guard against pathological input, not a variety list.

## Needed beyond the manifest

`ai-packages/qa-factory/scripts/slow_tests.json`.
