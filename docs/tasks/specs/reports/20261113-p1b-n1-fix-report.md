# P1-b N1 fix round (after the code critic, fit_with_fixes): report

Branch wip/p1b-n1, base 68c49c6. Owns touched: `scripts/tests/dry_exits.py`, `fixtures/driver-exits/{classes,gates,s0,s5,s6-s9}.json`, this report. No driver or package code touched. Until N3's test file exists the census runs on no CI path (`canon.yml` runs only `dry_world.py --spike`); `--check` / `--selftest` are run by hand.

## Findings -> what changed, where

| F | change (all in `dry_exits.py` unless named) |
|---|---|
| F1 / Q1 | `check` -> `_classes_and_doors`: `class unknown` is a RED line `route <name>: class unknown; name a class_source ...` (joints too: same class). `class_of` accepts any `by_source` key named directly (one branch). Docstring and `classes.json` `_about` say RED. Data: `marked_person` row has `class_source: route:marked_person`, `classes.json` by_source `route:marked_person: gate` (Lead decision). `readiness`, `story_budget`, `executor`: NOT named, see "Routes left red". |
| F2 | `raised_by` entries are `"<count> | <row> | <who, where>"` (`RAISE_RE`, `_raise_entry`; a malformed entry is refused by `load` naming the file). `_raised` checks each entry's row exists with that count's reach (hook_layer: a scanned registry id) and appears once; `_ratchets` requires per count `count == base + valid entries`: above = unnamed raise, below base = stale base, surplus entries = `stale raise credit`, a gone row = `stale raise`, two entries for one row = refused. |
| F3 | `_walk_problems`: a census row with reach `story`/`seed` and no walk row whose id-subject is its name is red with the door. Group file with no row and zero counts is refused naming the file (`_empty_problems`); a census row with reach `hook_layer` is red. |
| F4 | `minted_routes(source)` reads the literal `return "<name>", "<action>"` tuples of `match_known` by AST (`scan_minted`, `scan_routes`); none found -> `ExitsUnreadable` "could not read the routes of match_known". Rows `marked_repair`, `marked_person` in `gates.json`. |
| F5 | `class_counts(universe, classes)`: `gate_questions` = `question:<key>` sources of `classes.json` whose key is in the prices (was the literal 2). Every NUMBER line carries a recount command that prints its own figures (below). |
| F6 | `ban_doors(universe)` and `class_counts` use `Universe.unpassable` = ids from `refusal_registry.unpassable()` (the one reader); no blank-override predicate left in the file. |
| F7 | `check` split: `_code_rows`, `_walk_problems`, `_raised`, `_ratchets`, `_classes_and_doors`, `_ledger`, `_numbers` (max 3 nesting levels). Walk rows with reach `unwalked` / `hook_layer` are red (`COUNT_ONLY`). `TIME_KEYS` has a comment saying why it is a closed list kept here. |
| F8 / Q2 | `_PersonSites`: a site is keyed when its text argument (2nd positional or `text=`) calls `closed_question`/`priced_section` or is built from a name bound IN THE SAME FUNCTION (`_bindings`, own scope only) to such a call; a name bound both ways gives the site both values (MIXED). Group files: 7 kind rows removed, `package` raised_at shrunk, ratchets lowered. |
| F11 | in the commit message (`architecture:` line). |

## Verification (verbatim, after the last edit)

`python -B ...\scripts\tests\dry_exits.py --check` (exit 1, the 3 routes left red by Q1):

```
NUMBER routes: 21 KNOWN_REFUSALS + 2 minted by match_known (marked_person, marked_repair) + 2 (unmatched, known_false) = 25   [recount: python -B -c "import driver_dispatch as D; print(len(D.KNOWN_REFUSALS))" in scripts/ prints 21; grep -cE 'return .marked_' driver_machine.py prints 2]
NUMBER price keys: 61, options: 188   [recount: python -B -c "import no_move as N; p=N.load_question_prices(); print(len(p), sum(map(len, p.values())))" in scripts/]
NUMBER joints: 43 (detector 8, exit 8, window 27)   [recount: python -B -c "import null_outcomes as O, stage_joints as J; print(len(O.load_data(J.DATA)[0]['joints']))" in scripts/]
NUMBER kinds without a key: 14 of 29 literal kinds (13 keyless, 1 mixed: package); sites with a kind that arrives as a value: 9 (driver_conductor:_person_of, driver_conductor:pass_to_person, driver_dialog:held_question, driver_gates:gate, driver_machine:_act_wait_existing_job, driver_machine:handle_refusal, driver_runner:site_seam_person, driver_s0:s0_again, driver_s0:s0_stop)   [recount: grep -ohE "(Person|site_seam_person)\(\s*['\"][a-z_0-9]+['\"]" driver_*.py | sort -u | wc -l prints the literal kinds; the rows are the kinds_without_key keys of the group files]
NUMBER classes, bans: word-does-not-pass 58 / word-passes 19   [recount: python -B -c "import refusal_registry as R; b=[r for r in R.REGISTRY if r.get('file') in R.SCANNED and r.get('kind')!='operation']; u=R.unpassable(); print(sum(r in u for r in b), sum(r not in u for r in b))" in scripts/]
NUMBER classes, gates: operations 25 (of them override '': 0) / joints 43 / questions 2   [recount: python -B -c "import refusal_registry as R, no_move as N, json; o=[r for r in R.REGISTRY if r.get('kind')=='operation']; c=json.load(open('tests/fixtures/driver-exits/classes.json')); p=N.load_question_prices(); print(len(o), sum(r in R.unpassable() for r in o), sum(s[9:] in p for s in c['by_source'] if s.startswith('question:')))" in scripts/]
NUMBER ban_doors without a named door: 0   [recount: python -B -c "import refusal_registry as R; print(sum(1 for r in R.unpassable() if r.get('file') in R.SCANNED and r.get('kind')!='operation' and not str(r.get('unpassable_because') or '').strip()))" in scripts/]
NUMBER ratchet (rows now / base): live_only 0/0, after 0/0, unwalked 82/82, hook_layer 77/77; raised_by 0
NUMBER groups: gates, hooks, s0, s1-s4, s5, s6-s9
NOTE walk rows: none (...\fixtures\stories\dry-1\exits holds no rows yet; the walk nodes N4 write them)
FAIL route executor: class unknown; name a class_source for the row (a joint check, a REGISTRY id, question:<key> or a by_source key) and its class in fixtures/driver-exits/classes.json - the class is never guessed (FR-59)
FAIL route readiness: class unknown; name a class_source for the row (a joint check, a REGISTRY id, question:<key> or a by_source key) and its class in fixtures/driver-exits/classes.json - the class is never guessed (FR-59)
FAIL route story_budget: class unknown; name a class_source for the row (a joint check, a REGISTRY id, question:<key> or a by_source key) and its class in fixtures/driver-exits/classes.json - the class is never guessed (FR-59)
dry_exits --check: 3 discrepancies
```

`--selftest` (every non-PASS line, then the total; exit 0): `dry_exits selftest: 82/82 cases`.

Recount commands run as printed (in `scripts/`, subshell): routes `21` and `2`; literal kinds `29`; bans `58 19`; gates `25 0 2`; ban_doors `0`; kind rows in the group files `14`.

NEGATIVE control: byte copy of the 8 files into the scratchpad `neg/`, route `active_dispatch` deleted from the COPY of `gates.json`, `--check --dir neg`:

```
FAIL route active_dispatch: the driver has it and no row names it; add a row to fixtures/driver-exits/<group>.json with reach seed or live_only (or unwalked, counted in that group's ratchet) and a why_unreached
FAIL ratchet unwalked: stale base: 81 rows, below the base 82; lower the base to 81 in the group files
... (the same 3 class unknown lines)
dry_exits --check: 5 discrepancies
```
Hash-equal check of the originals (sha256 taken before the control, `sha256sum -c` after): `classes.json: OK gates.json: OK hooks.json: OK known_red.json: OK s0.json: OK s1-s4.json: OK s5.json: OK s6-s9.json: OK`. The originals were never modified by the control.

`selftest.py --lang` (package dir, subshell): `PASS lang: no Cyrillic anywhere in the package`, `PASS lang: no control byte left by an eaten escape sequence (FR-29)`, `=== qa-factory selftest: 2/2 ok ===`. Files are ASCII (max byte < 128, positive control on a non-ASCII sample detected).

Selftest rows added (82 = 62 - 4 rows removed or replaced (the old raise row, the unwalked-above-base row it duplicated, the NOTE-style class row, the no-override ban row) + 24 new; ids name the input): `scan:` 4 (bound text keys the site; bound plain string stays keyless; name bound twice = MIXED; other/enclosing function and `text=`), `ratchet:` 9 (at base green; base+1 with raise green; base+1 without red; base+2 with one raise red; raise at base = stale credit; cross-count; row gone; two entries one row; malformed entry), `walk:` 4 (seed row without walk row red; with walk row green; walk row reach unwalked/hook_layer red; census row hook_layer red), `load:` 1 (empty group file), `minted routes:` 3 (read from source; third marker branch red until a row; rewritten function refused), `class:` 3 (E19 red; by_source key direct; joint without class red) and the counts/ban rows rewritten for the new signatures.

## Numbers before -> after

| number | before (first round) | after | printed by |
|---|---|---|---|
| routes | 23 (21 + 2) | 25 (21 + 2 minted + 2) | `--check` NUMBER routes |
| kinds without a key | 21 of 29 | 14 of 29 (13 keyless + 1 mixed: package) | NUMBER kinds; recount rows = 14 |
| unwalked rows / base | 87 / 87 | 82 / 82 | NUMBER ratchet |
| hook_layer | 77 | 77 | same |
| gate questions | the literal 2 | 2, counted from `classes.json` x prices | NUMBER classes, gates |
| discrepancies | 0 (3 as NOTE) | 3 (E19 red) | `--check` last line |
| selftest | 62/62 | 82/82 | `--selftest` |

Different from the critic's expectation (12 keyless + 2 mixed `package`, `questions`): I get 13 keyless + 1 mixed (`package`). `questions` stays keyless: `driver_dispatch:question_threshold` raises `Person("questions", text, ...)` with `text = Priced(body, section.priced)` and `section = self.priced_section("questions", ...)` two bindings earlier (a one-hop transitive key). The rule as the Lead worded it (bound to an expression that CALLS closed_question/priced_section) does not follow that hop; extending it to transitive names would make `questions` MIXED (its other site `driver_machine:_act_wait_existing_job` is keyless) and 12 + 2. Not forced; Lead decides.

## Routes left red by Q1 (the candidates did not verify) - QUESTION for the Lead

Positive control for the registry search: the same `"file": "(run_suite|waiver|readiness|stage_guard)\.py"` shape finds 27 records, so the empty results below are real.

- `readiness` (pattern `readiness: .*missing|capabilit(y|ies) .*missing|--require`): candidate `SG-tracker-route` does NOT verify. It is a stage_guard refusal of an S1 dispatch with call `{ticket}: {route}`; the text the route matches is the output of `readiness.py --require` (S0). That text reaches the person as the closed question `s0.readiness` (`driver_s0.py` s0_rest, `question-prices.json` `s0.readiness`: retry / go on / stop). A verified candidate exists in the existing scheme: `class_source: question:s0.readiness` + a by_source row `question:s0.readiness`; its class word is the Lead's call (gate by the word-passes-it reading).
- `story_budget` (pattern `STORY BUDGET`, case-insensitive): matches `story_budget.py:263/268/274` (notice text) and the controller sentence at `controller.py:6218` ("stopped on the story budget"). Neither is a joint check, a registry id or a question key (`refusal_registry.py` has no record for story_budget; its only hit is a comment at line 130). Candidate "controller sentence" is not a source in the by_source vocabulary; naming one would be a new source kind. `references/person-owned.json` `code_routes` already names `story_budget` -> `money`, but that is the person-owned vocabulary (money/access), not the gate/ban classes of `classes.json`.
- `executor` (pattern `executor[_ ]unavailable`): candidate `contract.py:117` is `HANDED_MATCH_PREFIX = "executor unavailable:"`, the prefix of a stage-override `match` the waiver writes, not the producer of the matched text; the matched text `executor_unavailable` is the status JSON of `run_suite.py:1567`, which has no registry record. `person-owned.json` `code_routes`: `executor` -> `access`.

Questions: (1) for each of the three: which source id and class word (or a new source kind in `classes.json` / spec 3.6)? The three stay red until named. (2) `questions`: transitive binding or not (above).

## FR walk (touched sections)

A: FR-1/2 every new red names what was expected and a door (`class unknown` names class_source and classes.json; stale raise names the entry; `claims reach seed` names the walk dir or `unwalked`); FR-57 `ban_doors` unchanged in meaning. B: no text for a person. C: FR-13 closed variety in data (classes, rows, raised_by form); `RAISE_RE`/`COUNT_ONLY`/`EXECUTABLE` are the layer's short grammar (as in round 1); FR-14 one output shape. D: FR-17 one reader of "word does not pass" (`unpassable()`); FR-59 unknown never a pass: class unknown red, no tuple in match_known red, empty group file red; FR-58 no expectation from code. E: not applicable (no delivery/report). F: FR-28 the measurer has a table of cases (82); FR-41 every NUMBER has a recount that prints its figure. G: FR-29/30 `--lang` 2/2, ASCII; FR-45 writes nothing outside temp dirs; FR-47 code is an instrument; FR-54 siblings below.

## Deviations

- The format of `raised_by` entries (`<count> | <row> | <who, where>`) is mine within the Lead's "each naming its row"; the spec text said only "a `raised_by` line".
- Recount of "kinds without a key" is the group-file row count (14) plus the grep of literal kinds (29); the keyless/mixed split has no independent one-line recount (it needs the same-function binding rule).
- Edits only through Edit/Write; one stray `cd` in a Bash call was refused by the hook (no state changed).

## Analogs noticed (not fixed)

- Hand-rolled "word does not pass" predicate (`not str(e.get("override") or "").strip()`): `refusal_registry.py:1281` (beside `unpassable()` in the same file), `scripts/tests/test_refusal_registry.py:170`, `scripts/tests/test_whole_identifier.py:304`. Out of my owns.
- F9 (strict JSON reader clone with `known_red._read`) and F10 (`dry_stub` prompt hash vs `author_input_sha`) stay queued as the Lead said.
- Class unknown for a JOINT is now red too (same class as E19); no joint is in that state today.

## Needed beyond the manifest

`scripts/refusal_registry.py`, `scripts/driver_machine.py`, `scripts/driver_dispatch.py`, `scripts/driver_s0.py`, `scripts/driver_runner.py`, `scripts/story_budget.py`, `scripts/controller.py`, `scripts/contract.py`, `scripts/run_suite.py`, `references/person-owned.json`, `references/question-prices.json`.
