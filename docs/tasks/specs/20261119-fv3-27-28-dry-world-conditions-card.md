# FV3-27 + FV3-28 (t-1548): one `asked_open` predicate; the conditions of the dropped answers

Node `live-run-fvf/3` (FV3-27, FV3-28), feature F19. Designer draft for the Lead. The two builder headers in §3 and §4 run
SERIALLY, FV3-27 first (FV3-28's returned row reads the predicate FV3-27 lands). Forks: §5. Trail: §7.

## 1. Architecture, variety, measured state

AR-n touched, the check each demands (put into the DoDs below), the owner and census class of each check added or altered:
- AR-13 (one reader per fact). FV3-27 replaces two copies of "is something still asked at S1" (`driver_sources.py:754-762`,
  `dry_world.py:1287-1299`) with one product predicate. Change check: grep the package for the shape
  `unavailable_materials` (done, §7: 3 package hits; the third, `source_inventory.sources_with_open_gaps`, is another fact,
  see §6). New reader -> SIBLING_MAP row: fork F7.
- AR-28 (an unknown never passes). The predicate's error direction is "asked" (offered): missing, unreadable or malformed
  inventory reads True. Change check: the spec states missing / unreadable / empty behaviour (§3 edges) and a test pins it.
- AR-29 (a code check judges data). `asked_open`: class `shape`, owner `data` (it reads the inventory's completeness, never a
  role's words). It is no census unit (name outside `UNIT_NAME_RE`, no judge call, no raise site; `test_judgment_census.py`
  docstring u1-u3), so the census is unchanged; the canon judges it. The walker's offered_if outcome (`dry_exits._offered_if_outcome`):
  class `xref`, owner `data`, altered only by F4 (b). FV3-28 adds data rows judged by existing checks: no check added.
- AR-1 (closed variety is data). FV3-28: a condition is a key in the row (`offered_if`), read through the one table
  `dry_world.WORLD_FACTS`; no list of answers in code.
- Commit lines: in the form `tools/architecture_gate.py` checks (do not copy its grammar here). The judgment line of both nodes
  is `judgment: none -- <why>`; why for FV3-27: "the predicate reads inventory completeness, no role output is classified";
  for FV3-28: "walk rows and ledger labels are data; no role output is classified".

`variety: none -- a product predicate over the story's own source-inventory file and test-layer data rows; no project-shape
value (language, tracker, stand, host) is read or branched on.`

Measured on the root checkout (HEAD 60325f73 per the session snapshot; the Lead confirms it equals `origin/main`):
- The facts of the brief hold: `dry_world.py:1287` `inventory_unavailable`, `:1304` `WORLD_FACTS = {"inventory_unavailable": ...}`,
  `:1307` `offered_if_fact`; `driver_sources.py:754-762` the local copy with `except Exception` -> asked; no `asked_open`
  in `source_inventory.py` (def list, §7). FV3-17's F4 already landed: the walker copy catches `(OSError, ValueError)` -> None
  and lets the rest propagate (`dry_world.py:1297`).
- Walker condition grammar on main (FV3-17 + t-1225 fixes): a walk row MAY carry `offered_if`: ONE non-blank string that is a
  key of `dry_world.WORLD_FACTS` (`dry_exits._walk_offered_if_problems`, `:1204-1217`; a number, object, list, blank or
  unknown key is refused at load naming the known keys and the door). A reader is `(World) -> True | False | None`, read AT
  the ask before the answer (`run_exit_row`, `:1340`). Judge (`_offered_if_outcome`, `:1560-1580`, called first in
  `judge_row`): no `offered_if` or no pending ask -> judged as before; value None -> FAIL "condition named, no world for it";
  False + token not offered -> NOTE tagged `unreached`, and the ask's always-checks still run, a FAIL wins (F1); False + token
  offered -> FAIL "does not hold, yet <token> was offered" (F2, the drift detector); True -> judged as before (C2 FAIL if not
  offered). A row with no token (free words, empty) skips the condition.
- The 19 answers: the row FV3-28 and verdict t-1217 F5 enumerate 18, not 19 (s5 report round 2 `:57-62` lists 12, not the
  13 F5 says; s6-s9 6). Question Q1. None of the 18 has a walk row today: grep of ids over `fixtures/stories/dry-1` (§7)
  finds only the siblings. `exits/s6-s9.json` does not exist in `stories/dry-1` on this checkout (glob, §7), though FV3-8
  is "принято 9418c560"; no row of any s6-s9 key named below exists there (count 0, control: same grep finds 15 s6.* ids
  in `exits/s5.json`).

## 2. The 18 dropped answers: road per answer

"plain" = a row with no `offered_if`: the seed and the stub of its siblings fix the condition, so C2 judges the offer
directly (fork F3). Sibling labels from `driver-exits/known_red/s5.json` (pins 57).

| # | answer | offer condition (ask site) | rows today (file) | road (recommended) |
|---|---|---|---|---|
| 1 | `s5.repair_limit/round` | route code != `unknown` (`driver_dispatch.py:3304,3310-3311`) | none; siblings debt/stop/free words/empty in `exits/s5.json`, red -> FV3-35 | plain, seed `to-s5-repair-limit`, stub of `/debt`; label FV3-35 |
| 2 | `s5.repair_limit/fixed` | same | same | same |
| 3-5 | `exit.resume_limit/round`, `/fresh`, `/go on` | round: a session id and why != `session_gone`; fresh: not `exit_fresh_blocked`; go on: no form errors (`driver_dispatch.py:3971-3981,4017`) | none; siblings stop/free words/empty, red -> FV3-35 | plain, seed `to-exit-resume-limit`, stub of `/stop`; label FV3-35 |
| 6-8 | `exit.resume_limit_halted/round`, `/fresh`, `/go on` | same, halted variant | same, red -> FV3-35 | plain, seed `to-exit-resume-limit-halted`, stub of `/stop`; label FV3-35 |
| 9 | `code_close.behind/go on` | fact `awaits` (`no_move.py:554-558`) | none; siblings retry/stop/free words/empty, red -> FV3-33 | plain, seed `to-code-close-behind`; label FV3-33 (whether `awaits` holds is FV3-33's seed) |
| 10-12 | `code_close.closed_story/full retro`, `/retry`, `/go on` | block: `full retro` iff block == `no accepted controller stage`, `retry` iff not (exactly one per world), `go on` iff block non-empty and not passed/refused (`no_move.py:561-578`) | none; siblings start S8, not labelled (NOTE `after:` by the main stop, estimate) | stays dropped: one seed offers at most one of full retro/retry, and no module predicate takes `task_root` for the block (a reader would copy `Driver.no_move_facts`, AR-13). Owner: fork F6 |
| 13-14 | `s6.stand_confirm/retry`, `/stand name` | stand name iff another configured stand exists (`driver_stage_build.py:123-128`); retry in most branches (`:102-122`) | none; no row of the key | stays dropped here: the s6-s9 group file is absent. Owner: fork F6 |
| 15-16 | `s6.stand_confirm.login/find the way in`, `/stand name` | find the way in iff login class `way` and not searched (`driver_stage_build.py:102-108`) | none | same |
| 17 | `s7.repair_limit/round` | budget countable (`driver_stage_s7.py:1391`) | none | same (plain once the group lands) |
| 18 | `s6.gate_a_dry/reapprove` | not a dry run, no role running, gate A approved on the current revision, cases in scope (`driver_stage_s6.py:916-927`) | none | same |

Plus FV3-17 item 2: `s1.review/unavailable` returns to `exits/s1-s4.json` with `offered_if: inventory_unavailable` (FV3-9,
owner of that file, is merged: batch row FV3-9 "принято").

## 3. Builder header FV3-27

designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261119-fv3-27-28-dry-world-conditions-card.md
given: this card §1, §3, §5 (F1, F2, F4 as the Lead decided them); `ai-packages/qa-factory/scripts/driver_sources.py::Driver.s1_review_text`; `ai-packages/qa-factory/scripts/source_inventory.py::completeness`, `::class_kwargs`, `::load_inventory`; `ai-packages/qa-factory/scripts/tests/dry_world.py::inventory_unavailable`, `::WORLD_FACTS`, `::offered_if_fact`; `ai-packages/qa-factory/scripts/tests/dry_exits.py::_offered_if_outcome` and its selftest rows "FV3-17"; `ai-packages/qa-factory/scripts/tests/test_story_run_s0_c29.py::c29_source`, `::c29_write`; verdict `docs/tasks/specs/reviews/t-1217-p1b-groups-and-fv3-17-code.md` F2, F3, F4
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/source_inventory.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_sources.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/dry_world.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/dry_exits.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_story_run_s0_c29.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/changelog.d/fv3-27-asked-open-one-predicate.md
non-goals: no walk row (FV3-28); no other `completeness` caller changes (`sources_with_open_gaps`, `_defaulted_vcs`, `source_preflight`: §6); no change to the `offered_if` grammar or to the outcomes other than F4; no new WORLD_FACTS key
handoff: C:/QAFactory/forge-repo/docs/tasks/specs/reports/20261119-fv3-27-report.md (red-before line, witness tails, readers answered, `not run locally:` lines)
edges: see the edge list right under this header
DoD: `python -B ai-packages/qa-factory/scripts/tests/dry_exits.py --selftest` + the narrow c29 call `python -B -c "import sys; sys.path.insert(0, 'ai-packages/qa-factory/scripts/tests'); import harness, test_story_run_s0_c29 as T; T.c29_s1_review_offer(); harness.finish('c29 narrow')"` + `python -B ai-packages/qa-factory/scripts/selftest.py --lang`
test: ai-packages/qa-factory/scripts/tests/test_story_run_s0_c29.py::c29_s1_review_offer (new scenario of the C2-9 file, one variant table) | expected from: card §3 edges a-c; `driver_sources.py:752-753` (C2-9: offered only while something is ASKED); Lead brief t-1548 (missing/unreadable reads as asked)
test: ai-packages/qa-factory/scripts/tests/dry_exits.py selftest table, rows next to "FV3-17" (`:2921-2936`) | expected from: card §3 edges d-e; verdict t-1217 F3, F4
siblings: axis 38 (dry census) unchanged; axis 34: no new road (one predicate, two callers); AR-13 analog `source_inventory.sources_with_open_gaps` left as is (§6)
readers: §3 readers table below; `tools/owns_readers.py` block not attached to the brief (Q2)

What changes (the shape is fork F2; the recommended form):
- `source_inventory.py`: `inventory_summary(task_root) -> dict | None` = `completeness(load_inventory(<task_root>/work/source-inventory.json),
  **class_kwargs(task_root))`, None when the file is absent or the read/compute fails (catch width: fork F1);
  `asked_in(summary) -> bool` = `summary is None or bool(summary.get("unavailable") or summary.get("unavailable_materials"))`;
  `asked_open(task_root) -> bool` = `asked_in(inventory_summary(task_root))`. Docstring states the error direction.
- `driver_sources.py` `s1_review_text`: the block `:754-762` becomes one `inventory_summary` call, `asked_open = SI.asked_in(summary)`,
  `defaulted` from the same summary (0 when None). Position invariant: the `defaulted` line is printed only when nothing is asked,
  and `unavailable` is appended to the options iff `asked_open`; the "not on disk yet" line (`:750-751`) is untouched.
- `dry_world.py`: `inventory_unavailable(copy)` returns `SI.asked_open(copy.task_root)`; its docstring drops "None = no world";
  the WORLD_FACTS key name stays (rows name it). With F4 (b): `offered_if_fact` catches a reader's exception and returns
  `{"key", "value": None, "error": "<type>: <text cut at 200>"}`; `dry_exits._offered_if_outcome` FAILs
  `<id>: offered_if <key>: the reader raised <error>` before the "no world" branch.

Edges (each with its invariant):
- a. Inventory readable, `unavailable` and `unavailable_materials` both empty -> False: `unavailable` NOT offered, the
  defaulted line printed when defaulted > 0. Invariant: this is the ONLY input that yields False; it is also the detector of a
  broken reader (a reader that always raises reads True, and this row then fails).
- b. Missing file; a directory at the path; empty file; bytes not UTF-8; invalid JSON; JSON `[]`, `null`, `"x"`, `1`;
  `{"sources": "x"}`; `{"sources": [1]}` -> True (offered), defaulted 0, no exception out of `s1_review_text`. Invariant: an
  inventory the factory cannot read never hides the answer (AR-28; `test_conductor_doors.py:760-761` already relies on
  missing -> offered). Under F1 (b) the last three shapes raise instead: the Lead's choice decides which rows of this list the
  table carries.
- c. `work/gap-classes.json` unreadable -> `class_kwargs` gives `class_problem`, completeness ignores the classes -> more is
  asked, never less. Invariant: a damaged class record never closes a question.
- d. Walker: a copy with no inventory -> `inventory_unavailable` reads True (before: None = FAIL "no world"). A row with
  `offered_if: inventory_unavailable` in that world is judged as before (C2 FAIL if the product did not offer). Invariant:
  walker fact and product offer read the same bytes through the same function, so a disagreement is the product site no
  longer calling it, and F2's drift FAIL stays armed.
- e. Walker, the four cases the Lead named: an unknown fact name -> refused at load (unchanged), and if it reaches the judge
  -> value None -> FAIL "condition named, no world" (unchanged); a reader that raises -> fork F4 (today: the exception leaves
  `walk_exits` and the whole group run dies, `_run_judged_row` catches only `MainPassError`, `StateUnreadable`,
  `SnapshotError`, `StoryError`); value True / False / None -> as §1 grammar, unchanged; a row with `offered_if` and no
  world -> for `inventory_unavailable` no longer reachable (missing reads True); for any other key None -> FAIL. Invariant: no
  condition outcome is ever a PASS or a NOTE by default.
- f. Temporal: before the merge the walker copy and F2 guard the drift; after it, no copy exists (grep `unavailable_materials`
  over `scripts/` finds `source_inventory.py` only, plus `gate_brief`/`source_preflight` hits of other facts). No walk row
  names `inventory_unavailable` until FV3-28.

Test lines, strongest first (write top-down until test lines reach code lines; the rest `tests not written: <line> -- over budget`):
- c29 `c29_s1_review_offer`: a table of (inventory bytes -> `unavailable` in the options?, defaulted line?) over edges a, b
  (missing, invalid JSON, `[]`), c. The product's offer does not change on these inputs (the rows pin the values edges a-c
  name, not "as before"), so this line has no red-before; it is the table the shared predicate must keep green.
- dry_exits selftest: `offered_if_fact` on a namespace with a `task_root` holding no inventory -> value True; with F4 (b), a
  reader that raises -> FAIL naming the raise. This is the defect line (verdict t-1217 F3): `red-before: python -B
  ai-packages/qa-factory/scripts/tests/dry_exits.py --selftest -> <tail>` (value None before the code).
- Not run locally: `test_story_run_s0_c29.py` whole, `test_conductor_doors.py`, `test_scenario_dry_1.py`,
  `test_judgment_census.py` -> report lines `not run locally: <file>, canon judges`.

Readers of the touched files (hand greps, commands in §7; answers per `.claude/agents/critic.md` rule 24 Q13 (d)):

| touched | reader | answer |
|---|---|---|
| `source_inventory.py` new names | no reader yet (grep `asked_open\|inventory_summary\|asked_in` 0 hits before) | new; importers of the module unchanged |
| `source_inventory.py` | `references/config-keys.json` needed_by (`source_inventory.py:runtime_credential_values`, `_tracker_state`, `requirement_source_lines` only) | unchanged: the new names read no config key directly |
| `source_inventory.py` | `test_judgment_census.py` / `fixtures/judgment-census.json` | unchanged: no new unit (§1) |
| `driver_sources.py::s1_review_text` | callers `driver_dispatch.py:426,779`, `driver_machine.py:496` | unchanged: same text and options on the same inputs |
| same | `fixtures/driver-layers.json:277,1297-1298`, `test_driver_layers.py:66,69` | unchanged: no Driver method added, no method-to-method call added |
| same | `test_conductor_doors.py:760-761` (missing inventory -> offered), `test_story_run_refusals_sources.py:146-148`, `test_story_run_stand_c.py:106,123` | unchanged by edge b (missing still offered) |
| `dry_world.py::inventory_unavailable`, `WORLD_FACTS`, `offered_if_fact` | `dry_exits.py:60` comment, `:1204-1217` grammar, `:1560-1580` judge, selftest `:2563-2569`, `:2921-2936` | unchanged except F4 (b) in `_offered_if_outcome` and the new selftest row (this stream) |
| `dry_world.py` | `test_scenario_dry_1.py` (keep row covers it), FV3-28 | FV3-28 changes no dry_world line under F3 (a) |
| `dry_exits.py` | `test_conductor_doors.py:824` (`driven_keys`), `test_scenario_dry_1.py` | unchanged: no loader or `driven_keys` change |

## 4. Builder header FV3-28 (after FV3-27 is merged)

designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261119-fv3-27-28-dry-world-conditions-card.md
given: this card §1, §2, §4, §5 (F3, F5, F6 as decided); `ai-packages/qa-factory/scripts/tests/fixtures/stories/dry-1/exits/s5.json` rows `s5.repair_limit/debt`, `exit.resume_limit/stop`, `exit.resume_limit_halted/stop`, `code_close.behind/retry` (the patterns); `.../exits/s1-s4.json` rows `s1.review/*`; `.../seeds/s5.json`; `ai-packages/qa-factory/scripts/tests/fixtures/driver-exits/known_red/s5.json`; `ai-packages/qa-factory/scripts/tests/dry_exits.py::driven_keys`; `ai-packages/qa-factory/scripts/tests/test_conductor_doors.py::PINNED_ELSEWHERE`; `ai-packages/qa-factory/references/question-prices.json` keys of §2
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/stories/dry-1/exits/s1-s4.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/stories/dry-1/exits/s5.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/driver-exits/known_red/s5.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_conductor_doors.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/changelog.d/fv3-28-dropped-answers-walked.md
non-goals: no WORLD_FACTS reader (F3 (a)); no row for the 9 answers §2 marks "stays dropped" (F6 owners); no seed change (existing recipes reuse); no product code; no `start` change of an existing row
handoff: C:/QAFactory/forge-repo/docs/tasks/specs/reports/20261119-fv3-28-report.md (row list, `--check` tail, narrow-call output, `not run locally:` lines, the `tests-over:` reason for the Lead)
edges: see the edge list right under this header
DoD: `python -B ai-packages/qa-factory/scripts/tests/dry_exits.py --check` (0 discrepancies) + `python -B ai-packages/qa-factory/scripts/tests/dry_exits.py --selftest` + the narrow call `python -B -c "import sys; sys.path.insert(0, 'ai-packages/qa-factory/scripts/tests'); import dry_exits, test_conductor_doors as T; d = dry_exits.driven_keys(); print(sorted(d & {'s1.review','s5.repair_limit','exit.resume_limit','exit.resume_limit_halted','code_close.behind'})); print(sorted(set(T.PINNED_ELSEWHERE) & d))"` (first line the five keys, second `[]`)
test: ai-packages/qa-factory/scripts/tests/fixtures/stories/dry-1/exits/s1-s4.json row `s1.review/unavailable` | expected from: finding `findings/20261117-p1b-uslovnyj-otvet-bez-usloviya-u-hodoka.md` «Что именно менять» item 2; card §1 grammar
test: ai-packages/qa-factory/scripts/tests/fixtures/stories/dry-1/exits/s5.json, the 9 rows of §2 #1-9, labelled in `known_red/s5.json` | expected from: `question-prices.json` rows of the four keys; the ask sites of §2; verdict t-1217 F5
siblings: axis 38 (dry census): the four keys move from PINNED_ELSEWHERE to driven, as FV3-10 did for others; axis 5 twins `exit.resume_limit` / `_halted` both get rows
readers: §4 readers table below

What changes:
- `exits/s1-s4.json`: after `s1.review/flip` add `{"id": "s1.review/unavailable", "start": "S0", "seed": null, "answer": {"token": "unavailable",
  "words": null, "words_file": null}, "reach": "story", "offered_if": "inventory_unavailable", "expect": {"checks": ["C2", "C3"]}}`.
- `exits/s5.json`: nine rows, each a copy of its sibling pattern (start, seed, stub, `expect.checks` `["C2", "C3"]`) with its
  token; placed after the sibling group in file order.
- `known_red/s5.json`: one row per new id, node of its siblings (FV3-35 for #1-8, FV3-33 for #9), `raised_by` in the file's
  same-reason form (`t-1548 FV3-28: same reason as <sibling id>`, never a cut sentence; verdict t-1217 F9); `pins.known_red`
  57 -> 66 (a ledger raise the Lead names at merge).
- `test_conductor_doors.py`: drop from `PINNED_ELSEWHERE` the keys `s5.repair_limit`, `exit.resume_limit`,
  `exit.resume_limit_halted`, `code_close.behind` (they become driven: `dry_exits.driven_keys` takes a key whose every price
  answer has a `story`/`seed` row, a known_red row included). `REPAIR_LIMIT_KEYS` and the EL13/`:854` checks stay.

Edges (each with its invariant):
- g. `s1.review/unavailable` in today's world: inventory complete at S0 -> NOTE `unreached` (expected, estimate: the N4 report
  measured offered `['agree', 'flip']`); incomplete -> judged C2/C3 as `/agree`; offered while the fact is False -> FAIL
  drift. Invariant: the row never turns green without the product offering the token in a world where it must.
- h. `s1.review` becomes driven: it is in no `PINNED_ELSEWHERE` entry (grep §7), and `test_conductor_doors` already drives
  it (`:761`): the census union is unchanged. Invariant: no key is both pinned and driven.
- i. The nine s5 rows are red today with their siblings' cause (seed not reached). Invariant: a new row is never green by
  default and never unlabelled red: each has its ledger row in the same commit, and `--check` reconciles (a labelled row
  that turns green is reported stale, `known_red.py`).
- j. Once FV3-35/FV3-33 make the rows reachable, a plain row whose answer the world does not offer is C2 FAIL `was not
  offered`. Invariant: that FAIL is a measured fact for the node that reached it (it names the condition from §2 and decides:
  seed, reader, or `live_only` with the measured cause); it is never silenced by this node.
- k. A key whose rows are all labelled red counts as driven (FV3-10's rule). Invariant: its pin file still exists and still
  runs in the canon; only the census pointer moves.
- l. Positional: new rows go after their sibling group; `driven_keys` and the ledger are order-free, the order only keeps
  diffs readable. No existing row's `start`, `seed` or `stub` changes.

Test volume: the node is data rows (11 walk/ledger rows + 4 removed dict entries, 0 product code lines), so the walk rows
outnumber code by construction; the Lead names the `--tests-over` reason at merge, as for FV3-7.

Readers of the touched files:

| touched | reader | answer |
|---|---|---|
| `exits/s1-s4.json`, `exits/s5.json` | `dry_exits.load_walk_rows` / `--check` / `driven_keys`; `dry_world.walk_exits`; `test_scenario_dry_1.py`; `test_conductor_doors.py` keep covers `.../stories/dry-1/exits` (`test-layers.json:708`) | changes in this stream: driven set +5 keys, PINNED_ELSEWHERE -4 (same commit) |
| `known_red/s5.json` | `known_red.py` reconcile, `dry_exits.merged_ledger_rows`, `--check` pin | changes in this stream: +9 rows, pin 66 |
| `test_conductor_doors.py` | canon only (slow list `slow_tests.json:20`) | changes in this stream |
| `driver-exits/s5.json` census ratchet | `dry_exits --check` | unchanged: `reach: story` rows raise no ratchet |

## 5. Forks (questions for the Lead)

- F1 (FV3-27) catch width of the shared read. (a) RECOMMENDED: any exception from reading or computing -> None -> asked
  (product behaviour today, `driver_sources.py:761-762`); a broken reader is caught by edge a's row (it would read True where
  the table expects False). (b) catch `(OSError, ValueError)`, reject a non-dict top level as None, let the rest propagate
  (F4's literal wish): then a malformed inner shape (`{"sources": [1]}` -> AttributeError) crashes `s1_review_text` in the
  product instead of asking. Error direction either way: toward "asked" (an extra `unavailable` option); the adversarial
  inputs of edge b must stay on that side.
- F2 (FV3-27) shape. (A) RECOMMENDED: `inventory_summary` + `asked_in` + `asked_open` (one read in `s1_review_text`, `defaulted`
  from the same summary). (B) only `asked_open(task_root) -> bool` (the brief's literal form): `s1_review_text` then reads the
  inventory a second time for `defaulted`, and the copied call shape stays there for that second fact.
- F3 (FV3-28) road for the 18. (a) RECOMMENDED: plain rows where the sibling seed fixes the condition (#1-9), stays dropped
  with a named owner for the rest (#10-18). (b) a WORLD_FACTS reader per condition, as the batch row reads: no product
  predicate with a `task_root` signature exists for route code, session/fresh/form, `awaits`, the close block, countable, the
  other stand or the gate-A facts (all are Driver-method facts, §2 sites), so each reader is a copy (AR-13, the F3 class this
  node removes) or a product refactor across `driver_dispatch.py`, `no_move.py` callers, `driver_stage_build.py`,
  `driver_stage_s6.py`, `driver_stage_s7.py`, outside FV3-28's owns. Cost of (a): edge j.
- F4 (FV3-27) a reader that raises. (a) propagate (today: the group run dies, every row unjudged). (b) RECOMMENDED: row-local
  FAIL naming the raise (§3 "What changes"); AR-28 holds, the other rows are judged, and the message never says "add a reader".
- F5 (FV3-28) labels of the nine red rows. (i) RECOMMENDED: `reach: story` + `known_red/s5.json` rows under the siblings'
  nodes (one road with the siblings; four keys become driven, edge k). (ii) `reach: after:FV3-35|FV3-33` + nine `after`
  raises in `driver-exits/s5.json` ratchet: keys stay pinned, `test_conductor_doors.py` untouched, but the rows are not run.
- F6 (FV3-28) owners of the nine "stays dropped" answers (rule 6: a residual is a node with owns and a test).
  `code_close.closed_story/*` (#10-12): a new batch row (owns `stories/dry-1/{exits,seeds}/s5.json`, two seeds, one per block)
  RECOMMENDED, or FV3-33 widened. s6-s9 (#13-18): the node that lands `stories/dry-1/exits/s6-s9.json` on main; first the Lead
  measures why it is absent (`git -C C:/QAFactory/forge-repo ls-tree origin/main ai-packages/qa-factory/scripts/tests/fixtures/stories/dry-1/exits/`).
- F7 (AR-13 change check) a SIBLING_MAP axis row "is something still asked at S1: `source_inventory.asked_open` <->
  `Driver.s1_review_text` <-> `dry_world.WORLD_FACTS`": Lead adds it at FV3-27 acceptance (RECOMMENDED) or records why not.
- Q1 the count: 18 answers enumerated, the row says 19 (F5's s5 "13" sums to 12). Is a 19th intended (for example
  `s5.repair_limit/debt` is NOT conditional: offered for every code, `driver_dispatch.py:3304,3311`)?
- Q2 the `tools/owns_readers.py` block was not attached; §3 and §4 readers are hand greps (§7). Attach the block, or accept these.

## 6. Small choices closed; analogs noticed

Closed: the names `asked_open` / `asked_in` / `inventory_summary` stay outside the census unit pattern; the WORLD_FACTS key
`inventory_unavailable` keeps its name (rows are data); the product offer rows live in `test_story_run_s0_c29.py` (the C2-9
file; `test_source_inventory.py` is quarantined, `test-layers.json:11151`; `test_gap_points.py` is held only by import);
each node writes its own changelog.d entry in English (the FV3-17 precedent); new s5 rows copy their sibling's stub so the
seed fixes the condition; the builder headers stay over the designer threshold because the Lead's own FV3-27 row already
owns three files and FV3-28 needs four data/test files (no numbered lists inside the headers).
Analogs (not widened): `source_inventory.sources_with_open_gaps` (`:3774-3776`) unions the same two lists without
`class_kwargs` (its fact is "ids to accept-gap", `ticket_adapter.py:2910`); `Driver._defaulted_vcs` (`driver_dispatch.py:2245-2255`)
reads the same summary with `except Exception: return False` (another fact, other direction). Neither reads "is something asked".

## 7. Trail

Read: batch rows FV3-17, FV3-27, FV3-28 and «Ход» (`plans/piles/live-run-fvf/batch-3-live-run-fvf.md:46,56-57,75`); finding
FV3-17; verdict t-1217 whole; `dry_world.py:1110-1541`; `dry_exits.py:1200-1221,1556-1605,899-910` and selftest hits;
`driver_sources.py:715-772,95-109`; `source_inventory.py:2723-2725,3215-3237,3327-3356,3651-3710,3772-3776`; `driver_dispatch.py:2244-2256,3292-3336,3958-3987`;
`no_move.py:505-579`; `driver_stage_build.py:100-138`; `driver_stage_s6.py:895-934`; `driver_stage_s7.py:1378-1393`;
`question-prices.json:150-269`; `exits/s5.json:1-75,1200-1360,1736-1866`; `exits/s1-s4.json:5-28`; `seeds/s5.json` recipes;
`known_red/s5.json:118-236`; `known_red.json` (main/S6 -> FV3-23); `test_conductor_doors.py:645-669,750-770,824-828`;
`test_story_run_s0_c29.py:1-70,365-383`; `harness.py:225-229`; `test-layers.json:10-39,695-711,1844-1850,2912-2928,5245-5260,5461-5479,11151`;
`slow_tests.json` hits; `docs/TESTING.md:36-260`; `design/architecture.md:33-92,173-212,316-321`; `COORDINATOR.md:94-106`;
`tools/dispatch_manifest.py::designer_threshold`; `test_judgment_census.py:1-35`; s5 report `20261117-p1b-n4-s5-report.md:27-64`.
Searches (Grep tool; each negative with a positive control of the same form):
- `^def |^class |raise ` in `source_inventory.py`: no `asked_open` (control: `completeness`, `class_kwargs` found).
- ids `"id": "(s6\.stand_confirm|...|code_close\.closed_story)[^"]*"` over `stories/dry-1`: 17 hits, all siblings in `exits/s5.json`;
  none of the 18 (control: the same call found the siblings). `"id": "(s6|s7|s8|s9|closed)\.` count: 15 in `exits/s5.json`
  (s6.walk_*/data_change), 1 in selftest; glob `stories/dry-1/**/*.json`: no `exits/s6-s9.json`.
- `closed_story|code_close` case-insensitive over `driver-exits`: 24, all in `known_red/s5.json`, none `closed_story` (case-sensitive call 0 first).
- `get me access|cannot reach by itself` -i over `scripts/`: only `driver_sources.py:764,770` and a `source_inventory.py:3918` comment (no test pins the text).
- `inventory_unavailable|WORLD_FACTS` over the repo (py/json/md/yml): package hits `dry_exits.py` 19, `dry_world.py` 4, `changelog.d/fv3-17-walk-row-condition.md` 1.
- `get\("unavailable"\)|\["unavailable"\]|unavailable_materials"\)` over `scripts/*.py`: `driver_sources.py:759`, `dry_world.py:1299`,
  `source_inventory.py:3776`, `source_preflight.py:50`, `gate_brief.py:528-529,3187` (other facts), tests.
- `"s1\.review"|...` over `test_conductor_doors.py`: PINNED_ELSEWHERE holds all four s5 keys, `s6.stand_confirm*`, `s6.gate_a_dry`,
  `s7.repair_limit`, `code_close.closed_story`; `s1.review` only at `:528-530,761` (not pinned).
- `source_inventory\.py:[a-z_]+` -o over `config-keys.json`: 3 names, none touched.
Not measured (no shell): HEAD == origin/main; the canon outcome of edge g; the dry project's configured stand count (#13-14);
whether importing `test_conductor_doors` at module level is side-effect free (the FV3-28 narrow call; estimate).
Needed beyond the manifest: the files of the Read list outside the brief's `given:` (architecture.md, TESTING.md, COORDINATOR.md,
test-layers.json, slow_tests.json, question-prices.json, the driver_* and no_move sites, test_conductor_doors.py, known_red files, the s5 report).
